#!/usr/bin/env python3
"""mado-hostguard.py - run a command against a scratch HOME and fail if a declared operator-owned path changed.

M48-10 (`corpus/lessons/round-48.md`): an unsandboxed w2 mutant wrote the operator's
``~/.cache/xdg-terminal-exec``. This is the guard a counter, a mutant driver or a judge wraps around its
command: it pins a declared list of operator-owned paths, redirects HOME / XDG_CACHE_HOME /
XDG_CONFIG_HOME / XDG_DATA_HOME / XDG_STATE_HOME / TMPDIR into a scratch tree - or masks the home under a
bubblewrap namespace - runs the command, re-pins the same list, and fails if anything moved.

Design rules (deliberate, stated so a counter can rely on them):
- The declared paths are digested twice in this one process; a change is a change whoever caused it. The
  guard proves "no change was observed across this run", never "the child caused it": a concurrent operator
  write is reported as a violation too.
- The guard never creates, truncates or touches a declared path, and it writes no file of its own (no
  --receipt flag: redirect stdout, that is the receipt). What it does create is the contract's own
  directories: --home (default <work>/home, mode 0700), the five XDG roots and TMPDIR (default
  <work>/tmp) - all under --work unless --home is given explicitly, in which case the XDG roots default
  under that home and are created there. That is why the real home is refused as --home/--work/--cwd/env
  dir and why --work-prefix exists.
- Directories are refused as --declare/--mask targets (exit 2). A tree digest is not in contract; a
  declared path is a regular file, a symlink (digested by its target) or absent.
- The real home of the invoking uid (from passwd, not $HOME) is never a valid --home, --work, env dir or
  child cwd, and --home/--work/env dirs may not be /tmp, /var/tmp or /dev/shm (round-48 w2/SentScratch),
  nor inside the repository this script lives in. --mask is the one argument that may name the real home: a
  tmpfs over it writes nothing to it, and that is how a counter contains a mutant with a hardcoded operator
  path. There is no flag to override the refusals.
- --mask and --ro-root are bubblewrap features: with --sandbox none they are refused (exit 2) instead of
  being silently ignored, so a driver cannot believe it is masking when it is not.
- HOME, XDG_CACHE_HOME, XDG_CONFIG_HOME, XDG_DATA_HOME, XDG_STATE_HOME and TMPDIR are the guard's: a
  --env-keep/--env-set of any of them is refused (exit 2), because it would bypass the redirection and the
  refusal checks. The dedicated flags are the only way to move them, and every one of them is checked.
- --sandbox bwrap masks every --mask path with an empty tmpfs, so a write that succeeds inside the sandbox
  lands nowhere. --ro-root makes the whole host read-only except --work.
- Printed paths are redacted to ``~`` for the invoking uid's home by default (receipts are committed;
  a home path is session material). --no-redact-home prints them raw. Redaction changes output only, never
  what is opened or created.

Exit status (never the child's, so a child that exits 3 cannot read as a violation)
  0  no declared path changed
  2  usage error or a refused path (--work under /tmp, --home inside the real home, a directory declared,
     --mask without --sandbox bwrap, ...)
  3  a declared path changed (sha256 / size / mtime_ns / ino / dev / kind / link target)
  4  prerequisite missing: bwrap requested but not on PATH, a --mask path that does not exist or is not a
     directory
  5  the child failed (non-zero, signalled, or past --timeout); its status is printed and in --json
  6  the internal error path fired (the old/new digest could not be computed); nothing is claimed

Usage
  mado-hostguard.py digest [--label LABEL] [--declare PATH ...] [--declare-file FILE ...]
                           [--json] [--no-redact-home]
  mado-hostguard.py run --work DIR [--home DIR] [--declare PATH ...] [--declare-file FILE]
                   [--sandbox none|bwrap] [--mask PATH ...] [--ro-root] [--work-prefix DIR]
                   [--xdg-cache DIR] [--xdg-config DIR] [--xdg-data DIR] [--xdg-state DIR]
                   [--tmpdir DIR] [--no-tmpdir] [--env-keep NAME ...] [--env-set NAME=VALUE ...]
                   [--path PATH] [--cwd DIR] [--timeout SECONDS] [--json] [--label LABEL]
                   -- COMMAND [ARG ...]
  mado-hostguard.py --selftest [--work DIR]
  mado-hostguard.py --help

  digest            print the before-table of the declared paths and exit 0. Read-only; the one subcommand
                    a seat may point at the real operator state (lstat + sha256 only).
  run               digest before, run COMMAND with the redirected environment, digest after. Repeatable
                    --declare/--mask/--declare-file; a declare file holds one path per line ('#' comments,
                    blank lines skipped). Declarations are de-duplicated (by resolved path, first wins)
                    before the 64-path limit is applied. With --json the child's stdout is taken from
                    stderr, so stdout is exactly one JSON object whatever the child prints.
  --selftest        hermetic cases: every fixture is generated in-process under --work (or
                    $MADO_HOSTGUARD_WORK, or $TMPDIR - which the refusal then rejects), no network, no host
                    state read except passwd and the presence of bwrap. Namespace cases fall back to the
                    "prerequisite missing" branch when bwrap is absent, so the pass count is fixed. Last
                    line: `MADO_HOSTGUARD_SELFTEST: N/N passed`; exit 0 iff all pass.

Concurrency and cost: paths are read once, sequentially, in 1 MiB chunks; <= 64 declarations; the child runs
with a wall-clock bound (default 300 s) and its whole process group is killed on timeout.
"""

import argparse
import hashlib
import json
import os
import pwd
import shutil
import signal
import stat
import subprocess
import sys
import tempfile
import time
import traceback

LABEL = "operator-owned"
MAX_DECLARED = 64
CHUNK = 1 << 20
TMP_ROOTS = ("/tmp", "/var/tmp", "/dev/shm")
FIELDS = ("kind", "sha256", "size", "mtime_ns", "ino", "dev", "link")
REDACT_HOME = True
VERSION = "r50"


class Refused(Exception):
    """A path or argument the contract does not allow (exit 2)."""


class Prerequisite(Exception):
    """Something the run needs is missing (exit 4)."""


# --------------------------------------------------------------------------- paths


def real(p):
    return os.path.realpath(os.path.abspath(os.path.expanduser(p)))


def under(p, root):
    """True iff realpath(p) is realpath(root) or inside it (a name prefix is not a path prefix)."""
    p, root = real(p), real(root)
    return p == root or p.startswith(root.rstrip("/") + "/")


def repo_root(path):
    """Nearest ancestor of path holding .git or .jj, else None (no subprocess)."""
    d = os.path.dirname(real(path))
    while True:
        if os.path.exists(os.path.join(d, ".git")) or os.path.exists(os.path.join(d, ".jj")):
            return d
        parent = os.path.dirname(d)
        if parent == d:
            return None
        d = parent


def operator_home():
    """The invoking uid's home from passwd - never $HOME, which a driver can point anywhere."""
    return real(pwd.getpwuid(os.getuid()).pw_dir)


def redact(s):
    """Print-side only: the operator home becomes ``~`` (a home path is session material)."""
    if s is None or not REDACT_HOME:
        return s
    s = str(s)
    h = operator_home()
    if s == h:
        return "~"
    if s.startswith(h + "/"):
        return "~" + s[len(h):]
    return s


def check_write_dir(name, path):
    """Refusal set for any directory this guard creates or lets the child write into."""
    rp = real(path)
    hit = next((t for t in TMP_ROOTS if rp == t or rp.startswith(t + "/")), None)
    if hit:
        raise Refused(f"{name} {redact(path)} resolves under {hit}: scratch must not be /tmp "
                      f"(round-48 w2/SentScratch)")
    if under(rp, operator_home()):
        raise Refused(f"{name} {redact(path)} resolves inside the operator home; refusing to create or run "
                      f"there")
    rr = repo_root(__file__)
    if rr and under(rp, rr):
        raise Refused(f"{name} {redact(path)} resolves inside {redact(rr)}; the guard writes only to external "
                      f"scratch")
    return rp


def check_read_dir(name, path):
    """Child cwd: nothing is created there, so only the operator home is an error."""
    rp = real(path)
    if under(rp, operator_home()):
        raise Refused(f"{name} {redact(path)} resolves inside the operator home; refusing to run there")
    if not os.path.isdir(rp):
        raise Refused(f"{name} {path} is not an existing directory ({redact(rp)})")
    return rp


# --------------------------------------------------------------------------- digest


def digest_one(declared, label):
    """One record. Read-only: lstat, then sha256 of the bytes (or of the link target)."""
    p = os.path.abspath(os.path.expanduser(declared))
    rec = {"label": label, "path": declared, "resolved": real(declared), "kind": "absent", "sha256": None,
           "size": None, "mtime_ns": None, "ino": None, "dev": None, "link": None}
    try:
        st = os.lstat(p)
    except FileNotFoundError:
        return rec
    except OSError as exc:
        raise Refused(f"--declare {declared}: cannot lstat ({exc.strerror})")
    rec.update(size=st.st_size, mtime_ns=st.st_mtime_ns, ino=st.st_ino, dev=st.st_dev)
    if os.path.islink(p):
        rec["kind"] = "symlink"
        target = os.readlink(p)
        rec["link"] = target
        rec["size"] = len(target.encode("utf-8", "surrogateescape"))
        rec["sha256"] = hashlib.sha256(target.encode("utf-8", "surrogateescape")).hexdigest()
        return rec
    if not stat.S_ISREG(st.st_mode):
        kind = ("fifo" if stat.S_ISFIFO(st.st_mode) else
                "device" if stat.S_ISCHR(st.st_mode) or stat.S_ISBLK(st.st_mode) else
                "socket" if stat.S_ISSOCK(st.st_mode) else "special")
        raise Refused(f"--declare {declared}: {kind} is not a regular file or symlink; a tree, FIFO or device "
                      f"is not in contract and is never opened")
    rec["kind"] = "file"
    h = hashlib.sha256()
    n = 0
    try:
        with open(p, "rb") as fh:
            while True:
                b = fh.read(CHUNK)
                if not b:
                    break
                h.update(b)
                n += len(b)
    except OSError as exc:
        raise Refused(f"--declare {declared}: cannot read ({exc.strerror}); a declared path must be readable")
    rec["size"] = n
    rec["sha256"] = h.hexdigest()
    return rec


def snapshot(declared, label):
    return [digest_one(d, label) for d in declared]


def changed_fields(before, after):
    return [k for k in FIELDS if before[k] != after[k]]


def fmt(rec):
    line = ("{label} kind={kind} size={size} mtime_ns={mtime_ns} ino={ino} dev={dev} sha256={sha256} "
            "path={path}".format(**dict(rec, path=redact(rec["path"]))))
    if rec.get("link") is not None:
        line += " link=" + str(rec["link"])
    return line


def read_declare_file(path):
    paths = []
    try:
        with open(path, "r", encoding="utf-8") as fh:
            for line in fh:
                s = line.strip()
                if s and not s.startswith("#"):
                    paths.append(s)
    except OSError as exc:
        raise Refused(f"--declare-file {path}: cannot read ({exc.strerror})")
    return paths


def dedupe(paths):
    """First declaration of a resolved path wins; a repeated path must not double-count."""
    seen, out = set(), []
    for d in paths:
        k = os.path.abspath(os.path.expanduser(d))
        if k in seen:
            continue
        seen.add(k)
        out.append(d)
    return out


# --------------------------------------------------------------------------- child env


MANAGED_VARS = ("HOME", "XDG_CACHE_HOME", "XDG_CONFIG_HOME", "XDG_DATA_HOME", "XDG_STATE_HOME", "TMPDIR")


def build_env(args, home, work):
    """Clean env: PATH plus the redirected homes. Nothing else leaks in.

    The six managed names can only be set by the guard itself: --env-keep HOME (round-49 behaviour) would
    silently overwrite the redirected HOME with the ambient one and hand a mutant the real home again.
    """
    env = {"PATH": args.path}
    env["HOME"] = home
    env["XDG_CACHE_HOME"] = args.xdg_cache or os.path.join(home, ".cache")
    env["XDG_CONFIG_HOME"] = args.xdg_config or os.path.join(home, ".config")
    env["XDG_DATA_HOME"] = args.xdg_data or os.path.join(home, ".local", "share")
    env["XDG_STATE_HOME"] = args.xdg_state or os.path.join(home, ".local", "state")
    if not args.no_tmpdir:
        env["TMPDIR"] = args.tmpdir or os.path.join(work, "tmp")
    for name in args.env_keep:
        if name in MANAGED_VARS:
            raise Refused(f"--env-keep {name}: the guard owns {name}; use --home/--xdg-*/--tmpdir so the "
                          f"path is refusal-checked")
        if name in os.environ:
            env[name] = os.environ[name]
    for pair in args.env_set:
        name, sep, value = pair.partition("=")
        if not name or not sep:
            raise Refused(f"--env-set {pair}: expected NAME=VALUE")
        if name in MANAGED_VARS:
            raise Refused(f"--env-set {name}=...: the guard owns {name}; use --home/--xdg-*/--tmpdir so the "
                          f"path is refusal-checked")
        env[name] = value
    return env


def ensure_dirs(args, home, env):
    os.makedirs(args.work, mode=0o700, exist_ok=True)
    for d in (home, env["XDG_CACHE_HOME"], env["XDG_CONFIG_HOME"], env["XDG_DATA_HOME"],
              env["XDG_STATE_HOME"], env.get("TMPDIR")):
        if not d:
            continue
        check_write_dir("env dir", d)
        os.makedirs(d, mode=0o700, exist_ok=True)


# --------------------------------------------------------------------------- sandbox


def need_bwrap():
    exe = shutil.which("bwrap")
    if not exe:
        raise Prerequisite("--sandbox bwrap requested but bwrap is not on PATH")
    return exe


def bwrap_prefix(args, work, cwd):
    exe = need_bwrap()
    masks = []
    for m in args.mask:
        mp = real(m)
        if not os.path.isdir(mp):
            raise Prerequisite(f"--mask {redact(m)} is not a directory ({redact(mp)}): tmpfs needs a mount "
                               f"point")
        if under(work, mp) or under(cwd, mp):
            raise Refused(f"--mask {redact(m)} covers --work or --cwd; the child could not reach its scratch")
        masks.append(mp)
    argv = [exe, "--die-with-parent", "--unshare-pid", "--unshare-ipc", "--unshare-uts"]
    if args.ro_root:
        argv += ["--ro-bind", "/", "/", "--dev", "/dev", "--proc", "/proc", "--tmpfs", "/tmp"]
        argv += ["--bind", real(work), real(work)]
        if not under(cwd, work):
            argv += ["--bind", cwd, cwd]
    else:
        argv += ["--dev-bind", "/", "/"]
    for mp in masks:
        argv += ["--tmpfs", mp]
    argv += ["--chdir", cwd]
    return argv


# --------------------------------------------------------------------------- run


def do_run(args, declared):
    if not args.command:
        raise Refused("run needs `-- COMMAND [ARG ...]`")
    cmd = list(args.command)
    if cmd and cmd[0] == "--":
        cmd = cmd[1:]
    if not cmd:
        raise Refused("run needs `-- COMMAND [ARG ...]`")
    if not args.timeout or args.timeout <= 0:
        raise Refused(f"--timeout {args.timeout}: a child needs a positive wall-clock bound")
    if args.sandbox != "bwrap":
        if args.mask:
            raise Refused("--mask requires --sandbox bwrap; with --sandbox none nothing would be masked")
        if args.ro_root:
            raise Refused("--ro-root requires --sandbox bwrap; with --sandbox none nothing would be read-only")

    work = check_write_dir("--work", args.work)
    if args.work_prefix and not under(work, args.work_prefix):
        raise Refused(f"--work {redact(args.work)} is not under --work-prefix {redact(args.work_prefix)}")
    home = real(args.home) if args.home else os.path.join(work, "home")
    check_write_dir("--home", home)
    cwd = check_read_dir("--cwd", args.cwd) if args.cwd else work

    env = build_env(args, home, work)
    for key in ("XDG_CACHE_HOME", "XDG_CONFIG_HOME", "XDG_DATA_HOME", "XDG_STATE_HOME"):
        check_write_dir(key, env[key])
    ensure_dirs(args, home, env)

    prefix = bwrap_prefix(args, work, cwd) if args.sandbox == "bwrap" else []
    before = snapshot(declared, args.label)
    t0 = time.monotonic()
    timed_out = False
    # --json promises that stdout is exactly one JSON object: the child keeps fd 2 and stdout is taken
    # from it, so a chatty child cannot corrupt a machine-readable receipt.
    popen_kw = {"stdout": 2} if args.json else {}
    try:
        proc = subprocess.Popen(prefix + cmd, env=env, cwd=cwd, start_new_session=True, **popen_kw)
    except FileNotFoundError as exc:
        after = snapshot(declared, args.label)
        changed = [(b, a, changed_fields(b, a)) for b, a in zip(before, after) if changed_fields(b, a)]
        _report(args, before, after, changed, None, work, home, env, prefix + cmd,
                elapsed=round(time.monotonic() - t0, 3))
        print(f"mado-hostguard: cannot execute {cmd[0]}: {exc.strerror}", file=sys.stderr)
        return 5
    try:
        child_rc = proc.wait(timeout=args.timeout)
    except subprocess.TimeoutExpired:
        timed_out = True
        try:
            os.killpg(os.getpgid(proc.pid), signal.SIGKILL)
        except ProcessLookupError:
            pass
        proc.wait()
        child_rc = -signal.SIGKILL
    elapsed = round(time.monotonic() - t0, 3)
    if timed_out:
        print(f"mado-hostguard: child exceeded --timeout {args.timeout}s; process group killed",
              file=sys.stderr)
    after = snapshot(declared, args.label)
    changed = [(b, a, changed_fields(b, a)) for b, a in zip(before, after) if changed_fields(b, a)]
    _report(args, before, after, changed, child_rc, work, home, env, prefix + cmd, elapsed=elapsed)
    if changed:
        return 3
    if child_rc != 0:
        return 5
    return 0


def _report(args, before, after, changed, child_rc, work, home, env, cmd, elapsed=None):
    mapped = {k: env.get(k) for k in ("HOME", "XDG_CACHE_HOME", "XDG_CONFIG_HOME", "XDG_DATA_HOME",
                                      "XDG_STATE_HOME", "TMPDIR")}
    status = "violation" if changed else ("ok" if child_rc == 0 else "child-failed")
    if args.json:
        print(json.dumps({
            "command": "run", "version": VERSION, "status": status, "label": args.label,
            "work": redact(work), "home": redact(home),
            "sandbox": args.sandbox, "mask": [redact(real(m)) for m in args.mask],
            "ro_root": bool(args.ro_root),
            "child_rc": child_rc, "timeout_s": args.timeout, "elapsed_s": elapsed,
            "argv": [redact(a) for a in cmd],
            "env": {k: redact(v) for k, v in mapped.items()},
            "before": [dict(r, path=redact(r["path"]), resolved=redact(r["resolved"])) for r in before],
            "after": [dict(r, path=redact(r["path"]), resolved=redact(r["resolved"])) for r in after],
            "changed": [{"path": redact(a["path"]), "fields": f} for _, a, f in changed],
        }, sort_keys=True))
        return
    head = f"# mado-hostguard run  work={redact(work)} home={redact(home)} sandbox={args.sandbox} " \
           f"label={args.label} declared={len(before)}"
    if args.mask:
        head += " mask=" + ",".join(redact(real(m)) for m in args.mask)
    if args.ro_root:
        head += " ro_root=1"
    print(head)
    for k, v in mapped.items():
        if v is not None:
            print(f"ENV {k}={redact(v)}")
    print("ARGV " + " ".join(redact(a) for a in cmd))
    print("# before")
    for r in before:
        print("BEFORE " + fmt(r))
    print("# after")
    for r in after:
        print("AFTER  " + fmt(r))
    for b, a, fields in changed:
        print(f"CHANGED path={redact(a['path'])} fields={','.join(fields)} "
              f"sha256={b['sha256']}->{a['sha256']} size={b['size']}->{a['size']} "
              f"mtime_ns={b['mtime_ns']}->{a['mtime_ns']}")
    print(f"child_rc={child_rc} elapsed_s={elapsed} changed={len(changed)} status={status} "
          f"exit={'3' if changed else ('0' if child_rc == 0 else '5')}")


# --------------------------------------------------------------------------- CLI


def build_parser():
    ap = argparse.ArgumentParser(prog="mado-hostguard.py", add_help=True,
                                 description="run a command with a scratch HOME and digest operator-owned "
                                             "paths before/after")
    sub = ap.add_subparsers(dest="cmd", required=True)

    def common(sp):
        sp.add_argument("--declare", action="append", default=[], metavar="PATH",
                        help="operator-owned path to digest before and after (repeatable, <= %d after "
                             "de-duplication)" % MAX_DECLARED)
        sp.add_argument("--declare-file", action="append", default=[], metavar="FILE",
                        help="file of --declare paths, one per line")
        sp.add_argument("--label", default=LABEL, help="label printed with every record (default %s)" % LABEL)
        sp.add_argument("--json", action="store_true", help="emit one JSON object instead of the table")
        sp.add_argument("--no-redact-home", action="store_true",
                        help="print the operator home verbatim (default: it is printed as ~)")

    dg = sub.add_parser("digest", help="print the declared-path table and exit 0 (read-only)")
    common(dg)

    rn = sub.add_parser("run", help="digest, run a command in the redirected env, digest, exit 3 on change")
    common(rn)
    rn.add_argument("--work", required=True, metavar="DIR",
                    help="scratch root; everything this guard creates lives under it")
    rn.add_argument("--work-prefix", metavar="DIR", help="extra rule: --work must resolve under DIR")
    rn.add_argument("--home", metavar="DIR", help="HOME root (default <work>/home); XDG dirs default under it")
    rn.add_argument("--xdg-cache", metavar="DIR")
    rn.add_argument("--xdg-config", metavar="DIR")
    rn.add_argument("--xdg-data", metavar="DIR")
    rn.add_argument("--xdg-state", metavar="DIR")
    rn.add_argument("--tmpdir", metavar="DIR", help="child TMPDIR (default <work>/tmp)")
    rn.add_argument("--no-tmpdir", action="store_true", help="do not set TMPDIR at all")
    rn.add_argument("--sandbox", choices=("none", "bwrap"), default="none")
    rn.add_argument("--mask", action="append", default=[], metavar="PATH",
                    help="bwrap only: mount an empty tmpfs over PATH (repeatable)")
    rn.add_argument("--ro-root", action="store_true", help="bwrap only: host read-only except --work")
    rn.add_argument("--path", default="/usr/bin:/bin", help="child PATH (default /usr/bin:/bin)")
    rn.add_argument("--env-keep", action="append", default=[], metavar="NAME",
                    help="copy NAME from the ambient env into the child (e.g. LANG)")
    rn.add_argument("--env-set", action="append", default=[], metavar="NAME=VALUE")
    rn.add_argument("--cwd", metavar="DIR", help="child cwd (default --work)")
    rn.add_argument("--timeout", type=float, default=300.0, metavar="SECONDS")
    rn.add_argument("command", nargs=argparse.REMAINDER, help="-- COMMAND [ARG ...]")
    return ap


def collect_declared(args):
    declared = dedupe(list(args.declare) + [p for f in args.declare_file for p in read_declare_file(f)])
    if not declared:
        raise Refused("at least one --declare is required")
    if len(declared) > MAX_DECLARED:
        raise Refused(f"{len(declared)} declarations > {MAX_DECLARED} (after de-duplication)")
    for d in declared:
        ep = os.path.abspath(os.path.expanduser(d))
        if os.path.isdir(ep) and not os.path.islink(ep):
            raise Refused(f"--declare {d}: a directory; trees are not in contract (declare the files)")
    return declared


def main(argv):
    if argv and argv[0] == "--selftest":
        return selftest_main(argv[1:])
    global REDACT_HOME
    ap = build_parser()
    try:
        args = ap.parse_args(argv)
        REDACT_HOME = not args.no_redact_home
        declared = collect_declared(args)
        if args.cmd == "digest":
            recs = snapshot(declared, args.label)
            if args.json:
                print(json.dumps({"command": "digest", "version": VERSION, "label": args.label,
                                  "records": [dict(r, path=redact(r["path"]),
                                                   resolved=redact(r["resolved"])) for r in recs]},
                                 sort_keys=True))
            else:
                for r in recs:
                    print(fmt(r))
            return 0
        return do_run(args, declared)
    except Refused as exc:
        print(f"mado-hostguard: refused: {exc}", file=sys.stderr)
        return 2
    except Prerequisite as exc:
        print(f"mado-hostguard: {exc}", file=sys.stderr)
        return 4
    except OSError as exc:
        print(f"mado-hostguard: internal error: {exc}", file=sys.stderr)
        return 6


# --------------------------------------------------------------------------- selftest


SELFTEST_FIXTURE = b"mado-hostguard selftest fixture, not operator state\n"
FIXTURE_MTIME_NS = 1793047345000000000


def _fixture_bytes(size=331):
    return (SELFTEST_FIXTURE * (size // len(SELFTEST_FIXTURE) + 1))[:size]


MUTANT = '''\
import os, sys
target = os.environ.get("MUTANT_TARGET") or os.path.join(os.environ["HOME"], ".cache", "xdg-terminal-exec")
payload = os.environ.get("MUTANT_PAYLOAD", "r50-mutant")
mode = "a" if os.environ.get("MUTANT_APPEND") else "w"
os.makedirs(os.path.dirname(target), exist_ok=True)
with open(target, mode) as fh:
    fh.write(payload)
if os.environ.get("MUTANT_MTIME_NS"):
    os.utime(target, ns=(int(os.environ["MUTANT_MTIME_NS"]), int(os.environ["MUTANT_MTIME_NS"])))
print("WROTE path=%s size=%d" % (target, os.path.getsize(target)))
sys.exit(int(os.environ.get("MUTANT_EXIT", "0")))
'''

RO_PROBE = '''\
import os
p = os.path.join(os.environ["HOME"], ".cache", "xdg-terminal-exec")
try:
    with open(p, "w") as fh:
        fh.write("nope")
    print("WRITE_SUCCEEDED")
except OSError as e:
    print("WRITE_BLOCKED errno=%d" % e.errno)
t = os.path.join(os.environ["TMPDIR"], "ok")
with open(t, "w") as fh:
    fh.write("x")
print("TMPDIR_WRITE_OK size=%d" % os.path.getsize(t))
'''


class SelftestContext:
    def __init__(self, root, py):
        self.root = root
        self.py = py
        self.fx = os.path.join(root, "fixtures")
        self.fakehome = os.path.join(self.fx, "fakehome")
        self.cache = os.path.join(self.fakehome, ".cache", "xdg-terminal-exec")
        self.work = os.path.join(root, "work")
        self.mutant = os.path.join(self.fx, "mutant.py")
        self.ro_probe = os.path.join(self.fx, "ro_probe.py")
        self.bwrap = shutil.which("bwrap")
        os.makedirs(self.fx, exist_ok=True)
        os.makedirs(os.path.join(self.fakehome, ".cache"), exist_ok=True)
        with open(self.mutant, "w", encoding="utf-8") as fh:
            fh.write(MUTANT)
        with open(self.ro_probe, "w", encoding="utf-8") as fh:
            fh.write(RO_PROBE)

    def reset_cache(self, size=331):
        with open(self.cache, "w", encoding="utf-8") as fh:
            fh.write(_fixture_bytes(size).decode("ascii"))
        os.utime(self.cache, ns=(FIXTURE_MTIME_NS, FIXTURE_MTIME_NS))
        return self.cache

    def cache_sha(self):
        with open(self.cache, "rb") as fh:
            return hashlib.sha256(fh.read()).hexdigest()

    def run_argv(self, *extra, work=None, home=None):
        """`run` argv with the fixture home/cache; `work`/`home` override the defaults explicitly."""
        argv = ["run", "--work", work if work is not None else self.work]
        h = home if home is not None else self.fakehome
        if h is not False:
            argv += ["--home", h]
        argv += ["--declare", self.cache]
        return argv + list(extra)


def call(argv):
    """Invoke main() in-process, capturing both streams (and a SystemExit, if any).

    The redirect is at file-descriptor level: a `run` case starts a child that inherits fd 1/2, so a
    Python-level redirect would let the child's output escape into the selftest's own stdout.
    """
    tmp1, tmp2 = tempfile.TemporaryFile(), tempfile.TemporaryFile()
    saved = (os.dup(1), os.dup(2))
    rc = None
    try:
        sys.stdout.flush()
        sys.stderr.flush()
        os.dup2(tmp1.fileno(), 1)
        os.dup2(tmp2.fileno(), 2)
        try:
            rc = main(list(argv))
        except SystemExit as exc:
            rc = exc.code if isinstance(exc.code, int) else (0 if exc.code is None else 1)
    finally:
        sys.stdout.flush()
        sys.stderr.flush()
        os.dup2(saved[0], 1)
        os.dup2(saved[1], 2)
        os.close(saved[0])
        os.close(saved[1])
    buf1, buf2 = [], []
    tmp1.seek(0)
    tmp2.seek(0)
    buf1.append(tmp1.read())
    buf2.append(tmp2.read())
    tmp1.close()
    tmp2.close()
    return rc, b"".join(buf1).decode("utf-8", "replace"), b"".join(buf2).decode("utf-8", "replace")


def _changed_line(text):
    for line in text.splitlines():
        if line.startswith("CHANGED "):
            return line
    return ""


def _case_digest_absent(c):
    p = os.path.join(c.fx, "absent-probe")
    if os.path.exists(p):
        os.unlink(p)
    rc, out, err = call(["digest", "--declare", p])
    return (rc == 0 and "kind=absent" in out, f"rc={rc}")


def _case_digest_file_sha(c):
    c.reset_cache()
    want = hashlib.sha256(_fixture_bytes(331)).hexdigest()
    rc, out, err = call(["digest", "--declare", c.cache])
    return (rc == 0 and "kind=file" in out and f"sha256={want}" in out and "size=331" in out,
            f"rc={rc} want_sha={want[:12]}")


def _case_digest_symlink(c):
    link = os.path.join(c.fx, "link-probe")
    if os.path.islink(link) or os.path.exists(link):
        os.unlink(link)
    os.symlink(c.cache, link)
    rc, out, err = call(["digest", "--declare", link])
    want = hashlib.sha256(c.cache.encode()).hexdigest()
    return (rc == 0 and "kind=symlink" in out and f"link={c.cache}" in out and f"sha256={want}" in out,
            f"rc={rc}")


def _case_digest_unreadable_refused(c):
    """A declared file that lstat sees but open() cannot read is refused (2), not "internal error" (6)."""
    p = os.path.join(c.fx, "unreadable-probe")
    with open(p, "w", encoding="utf-8") as fh:
        fh.write("x")
    os.chmod(p, 0o000)
    try:
        rc, out, err = call(["digest", "--declare", p])
    finally:
        os.chmod(p, 0o600)
    return (rc == 2 and "cannot read" in err, f"rc={rc}")


def _case_digest_dir_refused(c):
    rc, out, err = call(["digest", "--declare", c.fakehome])
    return (rc == 2 and "a directory" in err and out.strip() == "", f"rc={rc}")


def _case_digest_fifo_refused(c):
    fifo = os.path.join(c.fx, "fifo-probe")
    if os.path.exists(fifo):
        os.unlink(fifo)
    os.mkfifo(fifo)
    rc, out, err = call(["digest", "--declare", fifo])
    return (rc == 2 and "fifo" in err, f"rc={rc}")


def _case_digest_json(c):
    c.reset_cache()
    rc, out, err = call(["digest", "--declare", c.cache, "--json"])
    ok = False
    try:
        data = json.loads(out)
        ok = (rc == 0 and data["command"] == "digest" and data["records"][0]["kind"] == "file"
              and data["records"][0]["size"] == 331)
    except Exception:
        ok = False
    return (ok, f"rc={rc}")


def _case_digest_no_declare(c):
    rc, out, err = call(["digest"])
    return (rc == 2 and "at least one --declare" in err, f"rc={rc}")


def _case_digest_too_many(c):
    c.reset_cache()
    argv = ["digest", "--declare", c.cache]
    for i in range(65):
        argv += ["--declare", os.path.join(c.fx, f"p{i}")]
    rc, out, err = call(argv)
    return (rc == 2 and "> 64" in err, f"rc={rc}")


def _case_declare_file_comments(c):
    c.reset_cache()
    df = os.path.join(c.fx, "declared.txt")
    absent = os.path.join(c.fx, "absent-two")
    with open(df, "w", encoding="utf-8") as fh:
        fh.write(f"# declared operator-owned paths\n\n{c.cache}\n   \n{absent}\n")
    rc, out, err = call(["digest", "--declare-file", df])
    return (rc == 0 and out.count("path=") == 2 and out.count("kind=absent") == 1,
            f"rc={rc} records={out.count('path=')}")


def _case_declare_file_missing(c):
    rc, out, err = call(["digest", "--declare-file", os.path.join(c.fx, "no-such-declare-file")])
    return (rc == 2 and "cannot read" in err, f"rc={rc}")


def _case_declare_dedupe(c):
    c.reset_cache()
    rc, out, err = call(["digest", "--declare", c.cache, "--declare", c.cache,
                         "--declare", os.path.join(c.fakehome, ".", ".cache", "xdg-terminal-exec")])
    return (rc == 0 and out.count("path=") == 1, f"rc={rc} records={out.count('path=')}")


def _refused_work(c, work):
    return call(c.run_argv("--", "true", work=work))


def _case_work_tmp_refused(c):
    work = os.path.join("/tmp", f"mado-hg-selftest-{os.getpid()}")
    rc, out, err = _refused_work(c, work)
    return (rc == 2 and "/tmp" in err and not os.path.exists(work), f"rc={rc} created={os.path.exists(work)}")


def _case_work_vartmp_refused(c):
    work = os.path.join("/var/tmp", f"mado-hg-selftest-{os.getpid()}")
    rc, out, err = _refused_work(c, work)
    return (rc == 2 and "/var/tmp" in err and not os.path.exists(work), f"rc={rc}")


def _case_work_devshm_refused(c):
    work = os.path.join("/dev/shm", f"mado-hg-selftest-{os.getpid()}")
    rc, out, err = _refused_work(c, work)
    return (rc == 2 and "/dev/shm" in err and not os.path.exists(work), f"rc={rc}")


def _case_home_real_refused(c):
    rc, out, err = call(c.run_argv("--", "true", home=operator_home()))
    return (rc == 2 and "operator home" in err, f"rc={rc}")


def _case_cwd_real_home_refused(c):
    rc, out, err = call(c.run_argv("--cwd", operator_home(), "--", "true"))
    return (rc == 2 and "operator home" in err, f"rc={rc}")


def _case_work_in_repo_refused(c):
    """The copy lives in a fake repo, so the copy's own repo refusal is what is measured."""
    repo = os.path.join(c.fx, "fakerepo")
    os.makedirs(os.path.join(repo, ".git"), exist_ok=True)
    os.makedirs(os.path.join(repo, "tools"), exist_ok=True)
    copy = os.path.join(repo, "tools", "mado-hostguard.py")
    shutil.copyfile(os.path.abspath(__file__), copy)
    env = {"PATH": "/usr/bin:/bin", "HOME": c.fakehome}
    cp = subprocess.run([c.py, copy, "run", "--work", os.path.join(repo, "w"),
                         "--declare", c.cache, "--", "true"],
                        capture_output=True, text=True, env=env, timeout=60)
    return (cp.returncode == 2 and "external scratch" in cp.stderr
            and not os.path.exists(os.path.join(repo, "w")),
            f"rc={cp.returncode} created={os.path.exists(os.path.join(repo, 'w'))}")


def _case_work_symlink_to_tmp_refused(c):
    """A --work that only *resolves* under /tmp must be refused (realpath, not string prefix)."""
    link = os.path.join(c.fx, "tmplink")
    if os.path.islink(link) or os.path.exists(link):
        os.unlink(link)
    os.symlink("/tmp", link)
    rc, out, err = _refused_work(c, os.path.join(link, f"mado-hg-{os.getpid()}"))
    return (rc == 2 and "/tmp" in err, f"rc={rc}")


def _case_file_then_absent(c):
    """The other direction: a child that deletes the declared file is a violation naming kind."""
    c.reset_cache()
    rc, out, err = call(c.run_argv("--", "/bin/rm", "-f", c.cache))
    line = _changed_line(out)
    return (rc == 3 and "kind=absent" in out and "fields=kind," in line and not os.path.exists(c.cache),
            f"rc={rc} {line[:72]}")


def _case_work_prefix_mismatch(c):
    rc, out, err = call(c.run_argv("--work-prefix", os.path.join(c.root, "elsewhere"), "--", "true"))
    return (rc == 2 and "not under --work-prefix" in err, f"rc={rc}")


def _case_control_true(c):
    c.reset_cache()
    before = c.cache_sha()
    rc, out, err = call(c.run_argv("--", "true"))
    return (rc == 0 and "changed=0 status=ok" in out and c.cache_sha() == before, f"rc={rc}")


def _case_mutant_caught(c):
    c.reset_cache()
    rc, out, err = call(c.run_argv("--env-set", "MUTANT_PAYLOAD=r50-selftest-case", "--",
                                   c.py, c.mutant))
    line = _changed_line(out)
    ok = (rc == 3 and "status=violation" in out and "fields=sha256,size,mtime_ns" in line
          and "WROTE " in out)
    return (ok, f"rc={rc} {line[:96]}")


def _case_same_size_same_mtime(c):
    c.reset_cache()
    payload = "X" * 331
    rc, out, err = call(c.run_argv("--env-set", f"MUTANT_PAYLOAD={payload}", "--env-set",
                                   f"MUTANT_MTIME_NS={FIXTURE_MTIME_NS}", "--", c.py, c.mutant))
    line = _changed_line(out)
    return (rc == 3 and "fields=sha256 " in line and "size=331->331" in line
            and f"mtime_ns={FIXTURE_MTIME_NS}->{FIXTURE_MTIME_NS}" in line, f"rc={rc} {line[:96]}")


def _case_absent_then_created(c):
    c.reset_cache()
    absent = os.path.join(c.fakehome, ".cache", "probe-absent")
    if os.path.exists(absent):
        os.unlink(absent)
    rc, out, err = call(["run", "--work", c.work, "--home", c.fakehome, "--declare", absent,
                         "--env-set", f"MUTANT_TARGET={absent}", "--env-set", "MUTANT_PAYLOAD=x",
                         "--", c.py, c.mutant])
    line = _changed_line(out)
    return (rc == 3 and "kind=absent" in out and "sha256=None" in line, f"rc={rc}")


def _case_sandbox_contained(c):
    c.reset_cache()
    before = c.cache_sha()
    rc, out, err = call(c.run_argv("--sandbox", "bwrap", "--mask", c.fakehome, "--env-set",
                                   "MUTANT_PAYLOAD=r50-contained", "--", c.py, c.mutant))
    if not c.bwrap:
        return (rc == 4 and "not on PATH" in err, f"rc={rc} bwrap=absent")
    return (rc == 0 and "changed=0 status=ok" in out and "WROTE " in out and c.cache_sha() == before,
            f"rc={rc} contained_sha_equal={c.cache_sha() == before}")


def _case_ro_root_blocked(c):
    c.reset_cache()
    before = c.cache_sha()
    rc, out, err = call(c.run_argv("--sandbox", "bwrap", "--ro-root", "--", c.py, c.ro_probe))
    if not c.bwrap:
        return (rc == 4 and "not on PATH" in err, f"rc={rc} bwrap=absent")
    return (rc == 0 and "WRITE_BLOCKED errno=30" in out and "TMPDIR_WRITE_OK" in out
            and c.cache_sha() == before, f"rc={rc} probe={out.strip().splitlines()[:2]}")


def _case_child_exit3_not_propagated(c):
    c.reset_cache()
    rc, out, err = call(c.run_argv("--", "/bin/sh", "-c", "exit 3"))
    return (rc == 5 and "child_rc=3" in out and "status=child-failed" in out, f"rc={rc}")


def _case_missing_binary(c):
    c.reset_cache()
    rc, out, err = call(c.run_argv("--", "/nonexistent-mado-hostguard-probe"))
    return (rc == 5 and "cannot execute" in err, f"rc={rc}")


def _case_timeout_kill(c):
    c.reset_cache()
    rc, out, err = call(c.run_argv("--timeout", "1", "--", "/bin/sleep", "30"))
    return (rc == 5 and "exceeded --timeout" in err and "child_rc=-9" in out, f"rc={rc}")


def _case_env_clean(c):
    c.reset_cache()
    os.environ["MADO_HG_LEAK_PROBE"] = "leak"
    try:
        rc, out, err = call(c.run_argv("--", "/usr/bin/env"))
    finally:
        os.environ.pop("MADO_HG_LEAK_PROBE", None)
    lines = set(out.splitlines())
    homes = {ln for ln in lines if ln.startswith("HOME=")}
    ok = (rc == 0 and "MADO_HG_LEAK_PROBE=leak" not in out and "PATH=/usr/bin:/bin" in out
          and f"HOME={c.fakehome}" in out and len(homes) == 1
          and "XDG_CONFIG_HOME=" + os.path.join(c.fakehome, ".config") in out
          and "TMPDIR=" + os.path.join(c.work, "tmp") in out)
    return (ok, f"rc={rc} leaked={'MADO_HG_LEAK_PROBE=leak' in out}")


def _case_env_keep(c):
    c.reset_cache()
    os.environ["MADO_HG_LEAK_PROBE"] = "kept"
    try:
        rc, out, err = call(c.run_argv("--env-keep", "MADO_HG_LEAK_PROBE", "--", "/usr/bin/env"))
    finally:
        os.environ.pop("MADO_HG_LEAK_PROBE", None)
    return (rc == 0 and "MADO_HG_LEAK_PROBE=kept" in out, f"rc={rc}")


def _case_env_set_bad(c):
    c.reset_cache()
    rc, out, err = call(c.run_argv("--env-set", "FOO", "--", "true"))
    return (rc == 2 and "expected NAME=VALUE" in err, f"rc={rc}")


def _case_mask_requires_bwrap(c):
    c.reset_cache()
    rc, out, err = call(c.run_argv("--mask", c.fakehome, "--", "true"))
    return (rc == 2 and "requires --sandbox bwrap" in err, f"rc={rc}")


def _case_ro_root_requires_bwrap(c):
    c.reset_cache()
    rc, out, err = call(c.run_argv("--ro-root", "--", "true"))
    return (rc == 2 and "requires --sandbox bwrap" in err, f"rc={rc}")


def _case_mask_not_dir(c):
    c.reset_cache()
    rc, out, err = call(c.run_argv("--sandbox", "bwrap", "--mask", c.cache, "--", "true"))
    return (rc == 4, f"rc={rc}")


def _case_mask_covers_work(c):
    c.reset_cache()
    rc, out, err = call(c.run_argv("--sandbox", "bwrap", "--mask", c.work, "--", "true"))
    if not c.bwrap:
        return (rc == 4, f"rc={rc} bwrap=absent")
    return (rc == 2 and "covers --work" in err, f"rc={rc}")


def _case_json_run(c):
    c.reset_cache()
    rc, out, err = call(c.run_argv("--json", "--env-set", "MUTANT_PAYLOAD=r50-json", "--",
                                   c.py, c.mutant))
    try:
        data = json.loads(out)
        ok = (rc == 3 and data["status"] == "violation" and data["command"] == "run"
              and data["changed"][0]["fields"] == ["sha256", "size", "mtime_ns"]
              and data["env"]["HOME"] == c.fakehome and data["child_rc"] == 0)
    except Exception:
        ok = False
    return (ok, f"rc={rc} parse={'ok' if ok else 'bad'}")


def _case_env_keep_home_refused(c):
    rc, out, err = call(c.run_argv("--env-keep", "HOME", "--", "true"))
    return (rc == 2 and "the guard owns HOME" in err, f"rc={rc}")


def _case_env_set_tmpdir_refused(c):
    rc, out, err = call(c.run_argv("--env-set", "TMPDIR=/tmp", "--", "true"))
    return (rc == 2 and "the guard owns TMPDIR" in err, f"rc={rc}")


def _case_ambient_home_is_not_the_operator_home(c):
    """The refusal is keyed on passwd, not $HOME: a redirected ambient HOME is the adoption shape."""
    c.reset_cache()
    saved = os.environ.get("HOME")
    os.environ["HOME"] = c.fakehome
    try:
        rc, out, err = call(c.run_argv("--", "true"))
    finally:
        if saved is None:
            os.environ.pop("HOME", None)
        else:
            os.environ["HOME"] = saved
    return (rc == 0 and "operator home" not in err, f"rc={rc}")


def _case_timeout_nonpositive(c):
    c.reset_cache()
    rc, out, err = call(c.run_argv("--timeout", "0", "--", "true"))
    return (rc == 2 and "positive wall-clock bound" in err, f"rc={rc}")


def _case_unit_redact(c):
    global REDACT_HOME
    old = REDACT_HOME
    try:
        REDACT_HOME = True
        a = redact(operator_home() + "/a/b")
        b = redact(operator_home())
        cc = redact("/opt/x")
        REDACT_HOME = False
        d = redact(operator_home() + "/a/b")
    finally:
        REDACT_HOME = old
    return ((a == "~/a/b" and b == "~" and cc == "/opt/x" and d == operator_home() + "/a/b"),
            f"a={a} b={b} cc={cc} raw_kept={d.endswith('/a/b')}")


def _case_unit_under(c):
    ok = (under("/tmp/a", "/tmp") and under("/tmp", "/tmp") and not under("/tmpfoo", "/tmp")
          and under("/a/b/c", "/a/b") and not under("/a/bc", "/a/b"))
    return (ok, "prefix-vs-path separation")


def _case_unit_changed_fields(c):
    base = {k: 1 for k in FIELDS}
    a = dict(base, sha256=2)
    return (changed_fields(base, a) == ["sha256"] and changed_fields(base, dict(base)) == [],
            f"got={changed_fields(base, a)}")


CASES = (
    ("digest_absent", _case_digest_absent),
    ("digest_file_sha", _case_digest_file_sha),
    ("digest_symlink", _case_digest_symlink),
    ("digest_unreadable_refused", _case_digest_unreadable_refused),
    ("digest_dir_refused", _case_digest_dir_refused),
    ("digest_fifo_refused", _case_digest_fifo_refused),
    ("digest_json_ok", _case_digest_json),
    ("digest_no_declare", _case_digest_no_declare),
    ("digest_too_many", _case_digest_too_many),
    ("declare_file_comments", _case_declare_file_comments),
    ("declare_file_missing", _case_declare_file_missing),
    ("declare_dedupe", _case_declare_dedupe),
    ("work_tmp_refused", _case_work_tmp_refused),
    ("work_vartmp_refused", _case_work_vartmp_refused),
    ("work_devshm_refused", _case_work_devshm_refused),
    ("home_real_refused", _case_home_real_refused),
    ("cwd_real_home_refused", _case_cwd_real_home_refused),
    ("work_in_repo_refused", _case_work_in_repo_refused),
    ("work_symlink_to_tmp_refused", _case_work_symlink_to_tmp_refused),
    ("work_prefix_mismatch", _case_work_prefix_mismatch),
    ("control_true_exit0", _case_control_true),
    ("mutant_unsandboxed_caught", _case_mutant_caught),
    ("same_size_same_mtime_sha_only", _case_same_size_same_mtime),
    ("absent_then_created", _case_absent_then_created),
    ("file_then_absent", _case_file_then_absent),
    ("sandbox_bwrap_contained", _case_sandbox_contained),
    ("ro_root_write_blocked", _case_ro_root_blocked),
    ("child_exit3_not_propagated", _case_child_exit3_not_propagated),
    ("missing_binary_exit5", _case_missing_binary),
    ("timeout_kill_exit5", _case_timeout_kill),
    ("env_clean", _case_env_clean),
    ("env_keep", _case_env_keep),
    ("env_keep_home_refused", _case_env_keep_home_refused),
    ("env_set_tmpdir_refused", _case_env_set_tmpdir_refused),
    ("ambient_home_is_not_operator_home", _case_ambient_home_is_not_the_operator_home),
    ("env_set_bad", _case_env_set_bad),
    ("mask_requires_bwrap", _case_mask_requires_bwrap),
    ("ro_root_requires_bwrap", _case_ro_root_requires_bwrap),
    ("mask_not_a_dir_exit4", _case_mask_not_dir),
    ("mask_covers_work_refused", _case_mask_covers_work),
    ("json_run_violation", _case_json_run),
    ("timeout_nonpositive_refused", _case_timeout_nonpositive),
    ("unit_redact_home", _case_unit_redact),
    ("unit_under_prefix", _case_unit_under),
    ("unit_changed_fields", _case_unit_changed_fields),
)


def selftest_work(argv):
    ap = argparse.ArgumentParser(prog="mado-hostguard.py --selftest", add_help=True,
                                 description="hermetic cases; every fixture is generated under --work")
    ap.add_argument("--work", metavar="DIR",
                    help="scratch root for the fixture tree (default $MADO_HOSTGUARD_WORK, else $TMPDIR)")
    args = ap.parse_args(argv)
    cand = args.work or os.environ.get("MADO_HOSTGUARD_WORK") or os.environ.get("TMPDIR")
    if not cand:
        raise Refused("--selftest needs --work DIR (or MADO_HOSTGUARD_WORK/TMPDIR): its fixture tree is a work "
                      "dir, and a work dir under /tmp is refused")
    root = check_write_dir("--selftest work", cand)
    root = os.path.join(root, "mado-hostguard-selftest")
    if os.path.isdir(root):
        shutil.rmtree(root)
    os.makedirs(root, mode=0o700, exist_ok=True)
    return root


def selftest_main(argv):
    try:
        root = selftest_work(argv)
    except Refused as exc:
        print(f"mado-hostguard: refused: {exc}", file=sys.stderr)
        print("MADO_HOSTGUARD_SELFTEST: 0/%d passed" % len(CASES))
        return 2
    py = sys.executable or "/usr/bin/python3"
    ctx = SelftestContext(root, py)
    passed, failed = 0, []
    print(f"# mado-hostguard {VERSION} selftest  python={sys.version.split()[0]} "
          f"bwrap={shutil.which('bwrap') or 'absent'} root={redact(root)}")
    for name, fn in CASES:
        try:
            ok, detail = fn(ctx)
        except Exception:
            ok, detail = False, "exception: " + traceback.format_exc().strip().splitlines()[-1]
        if ok:
            passed += 1
            print(f"SELFTEST pass {name}: {detail}")
        else:
            failed.append(name)
            print(f"SELFTEST FAIL {name}: {detail}")
    print(f"SELFTEST failed={len(failed)} {' '.join(failed) if failed else '-'}")
    print("MADO_HOSTGUARD_SELFTEST: %d/%d passed" % (passed, len(CASES)))
    return 0 if passed == len(CASES) else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
