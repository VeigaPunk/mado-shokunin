#!/usr/bin/env python3
"""hostguard - run a command against a scratch HOME and fail if an operator-owned path changed.

M48-10 (corpus/lessons/round-48.md): an unsandboxed w2 mutant wrote the operator's
``~/.cache/xdg-terminal-exec``. This tool is the guard a counter or a mutant driver runs BEFORE it starts a
command: it pins a declared list of operator-owned paths, redirects HOME/XDG_CACHE_HOME/XDG_CONFIG_HOME/
XDG_DATA_HOME/XDG_STATE_HOME (and TMPDIR) to a scratch tree - or masks the home under a bubblewrap namespace -
runs the command, re-pins the same list, and fails if anything moved.

Design rules (deliberate, stated so a counter can rely on them):
- The declared paths are digested twice in this one process; a change is a change whoever caused it. The guard
  proves "no change was observed across this run", never "the child caused it": a concurrent operator write is
  reported as a violation too.
- The guard never creates, truncates or touches a declared path, and it writes no file of its own (no
  --receipt flag: redirect stdout, that is the receipt). What it does create is the contract's own directories:
  --home (default <work>/home, mode 0700), the five XDG roots and TMPDIR (default <work>/tmp) - all under --work
  unless --home is given explicitly, in which case the XDG roots default under that home and are created there.
  That is why the real home is refused as --home/--work/cwd and why --work-prefix exists.
- Directories are refused as --declare/--mask targets (exit 2). A tree digest is not in contract; a declared
  path is a regular file, a symlink (digested by its target) or absent.
- The real home of the invoking uid (from passwd, not $HOME) is never a valid --home, --work, env dir or child
  cwd, and --home/--work/env dirs may not be /tmp, /var/tmp or /dev/shm (round-48 w2/SentScratch), nor inside the
  repository this script lives in. --mask is the one argument that may name the real home: a tmpfs over it writes
  nothing to it, and that is how a counter contains a mutant with a hardcoded operator path. There is no flag to
  override the refusals.
- --sandbox bwrap additionally masks every --mask path with an empty tmpfs, so a write that succeeds inside the
  sandbox lands nowhere. --ro-root makes the whole host read-only except --work.

Usage
  hostguard.py digest [--label operator-owned] --declare PATH [--declare PATH ...] [--json]
  hostguard.py run --work DIR [--home DIR] [--declare PATH ...] [--declare-file FILE]
                   [--sandbox none|bwrap] [--mask PATH ...] [--ro-root]
                   [--env-keep NAME ...] [--env-set NAME=VALUE ...] [--path PATH]
                   [--cwd DIR] [--timeout SECONDS] [--work-prefix DIR] [--json]
                   [--label LABEL] -- COMMAND [ARG ...]

  digest            print the before-table of the declared paths and exit 0. Read-only; the one subcommand a
                    seat may point at the real operator state (stat + sha256 only).
  run               digest before, run COMMAND with the redirected environment, digest after. Repeatable
                    --declare/--mask; --declare-file holds one path per line ('#' comments, blank lines skipped).

Exit status (never the child's, so a child that exits 3 cannot read as a violation)
  0  no declared path changed
  2  usage error or a refused path (--work under /tmp, --home inside the real home, a directory declared, ...)
  3  a declared path changed (sha256 / size / mtime_ns / ino / dev / kind / link target)
  4  prerequisite missing: bwrap requested but not on PATH, a mask/work path does not exist
  5  the child failed (non-zero, signalled, or past --timeout); its status is printed and in --json
  6  the internal error path fired (the old/new digest could not be computed); nothing is claimed

Concurrency and cost: paths are read once, sequentially, in 1 MiB chunks; ≤ 64 declarations; the child runs
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
import time

LABEL = "operator-owned"
MAX_DECLARED = 64
CHUNK = 1 << 20
TMP_ROOTS = ("/tmp", "/var/tmp", "/dev/shm")
FIELDS = ("kind", "sha256", "size", "mtime_ns", "ino", "dev", "link")


class Refused(Exception):
    """A path the contract does not allow (exit 2)."""


def real(p):
    return os.path.realpath(os.path.abspath(os.path.expanduser(p)))


def under(p, root):
    """True iff realpath(p) is realpath(root) or inside it."""
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
    return real(pwd.getpwuid(os.getuid()).pw_dir)


def check_write_dir(name, path):
    """Refusal set for any directory this guard creates or lets the child write into."""
    rp = real(path)
    hit = next((t for t in TMP_ROOTS if rp == t or rp.startswith(t + "/")), None)
    if hit:
        raise Refused(f"{name} {path} resolves under {hit}: scratch must not be /tmp "
                      f"(round-48 w2/SentScratch)")
    if under(rp, operator_home()):
        raise Refused(f"{name} {path} resolves inside the operator home; refusing to create or run there")
    rr = repo_root(__file__)
    if rr and under(rp, rr):
        raise Refused(f"{name} {path} resolves inside {rr}; the guard writes only to external scratch")
    return rp


def check_read_dir(name, path):
    """Child cwd: nothing is created there, so only the operator home is refused."""
    rp = real(path)
    if under(rp, operator_home()):
        raise Refused(f"{name} {path} resolves inside the operator home; refusing to run there")
    if not os.path.isdir(rp):
        raise Refused(f"{name} {path} is not an existing directory ({rp})")
    return rp


def digest_one(declared, label):
    """One record. Read-only: lstat, then sha256 of the bytes/link target."""
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
    with open(p, "rb") as fh:
        while True:
            b = fh.read(CHUNK)
            if not b:
                break
            h.update(b)
            n += len(b)
    rec["size"] = n
    rec["sha256"] = h.hexdigest()
    return rec


def snapshot(declared, label):
    return [digest_one(d, label) for d in declared]


def changed_fields(before, after):
    out = []
    for k in FIELDS:
        if before[k] != after[k]:
            out.append(k)
    return out


def fmt(rec):
    return ("{label} kind={kind} size={size} mtime_ns={mtime_ns} ino={ino} dev={dev} sha256={sha256} "
            "path={path}".format(**rec))


def read_declare_file(path):
    paths = []
    with open(path, "r", encoding="utf-8") as fh:
        for line in fh:
            s = line.strip()
            if s and not s.startswith("#"):
                paths.append(s)
    return paths


def build_env(args, home, work):
    """Clean env: PATH plus the redirected homes. Nothing else leaks in."""
    env = {"PATH": args.path}
    env["HOME"] = home
    env["XDG_CACHE_HOME"] = args.xdg_cache or os.path.join(home, ".cache")
    env["XDG_CONFIG_HOME"] = args.xdg_config or os.path.join(home, ".config")
    env["XDG_DATA_HOME"] = args.xdg_data or os.path.join(home, ".local", "share")
    env["XDG_STATE_HOME"] = args.xdg_state or os.path.join(home, ".local", "state")
    if not args.no_tmpdir:
        env["TMPDIR"] = args.tmpdir or os.path.join(work, "tmp")
    for name in args.env_keep:
        if name in os.environ:
            env[name] = os.environ[name]
    for pair in args.env_set:
        name, _, value = pair.partition("=")
        if not name or not _:
            raise Refused(f"--env-set {pair}: expected NAME=VALUE")
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


def bwrap_prefix(args, work, cwd):
    exe = shutil.which("bwrap")
    if not exe:
        print("hostguard: --sandbox bwrap requested but bwrap is not on PATH", file=sys.stderr)
        sys.exit(4)
    masks = []
    for m in args.mask:
        mp = real(m)
        if not os.path.isdir(mp):
            print(f"hostguard: --mask {m} is not a directory ({mp}): tmpfs needs a mount point",
                  file=sys.stderr)
            sys.exit(4)
        if under(work, mp) or under(cwd, mp):
            raise Refused(f"--mask {m} covers --work or --cwd; the child could not reach its scratch")
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


def main(argv):
    ap = argparse.ArgumentParser(prog="hostguard.py", add_help=True,
                                 description="run a command with a scratch HOME and digest operator-owned "
                                             "paths before/after")
    sub = ap.add_subparsers(dest="cmd", required=True)

    def common(sp):
        sp.add_argument("--declare", action="append", default=[], metavar="PATH",
                        help="operator-owned path to digest before and after (repeatable, <= %d)" % MAX_DECLARED)
        sp.add_argument("--declare-file", action="append", default=[], metavar="FILE",
                        help="file of --declare paths, one per line")
        sp.add_argument("--label", default=LABEL, help="label printed with every record (default %s)" % LABEL)
        sp.add_argument("--json", action="store_true", help="emit one JSON object instead of the table")

    dg = sub.add_parser("digest", help="print the declared-path table and exit 0 (read-only)")
    common(dg)

    rn = sub.add_parser("run", help="digest, run a command in the redirected env, digest, exit 3 on change")
    common(rn)
    rn.add_argument("--work", required=True, metavar="DIR", help="scratch root; everything this guard creates "
                                                                "lives under it")
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
    rn.add_argument("command", nargs=argparse.REMAINDER,
                    help="-- COMMAND [ARG ...]")

    args = ap.parse_args(argv)

    declared = list(args.declare) + [p for f in args.declare_file for p in read_declare_file(f)]
    if not declared:
        print("hostguard: at least one --declare is required", file=sys.stderr)
        return 2
    if len(declared) > MAX_DECLARED:
        print(f"hostguard: {len(declared)} declarations > {MAX_DECLARED}", file=sys.stderr)
        return 2

    try:
        for d in declared:
            ep = os.path.abspath(os.path.expanduser(d))
            if os.path.isdir(ep) and not os.path.islink(ep):
                raise Refused(f"--declare {d}: a directory; trees are not in contract (declare the files)")

        if args.cmd == "digest":
            recs = snapshot(declared, args.label)
            if args.json:
                print(json.dumps({"command": "digest", "label": args.label, "records": recs}, sort_keys=True))
            else:
                for r in recs:
                    print(fmt(r))
            return 0

        if not args.command:
            print("hostguard: run needs `-- COMMAND [ARG ...]`", file=sys.stderr)
            return 2
        cmd = list(args.command)
        if cmd and cmd[0] == "--":
            cmd = cmd[1:]
        if not cmd:
            print("hostguard: run needs `-- COMMAND [ARG ...]`", file=sys.stderr)
            return 2

        work = check_write_dir("--work", args.work)
        if args.work_prefix:
            if not under(work, args.work_prefix):
                raise Refused(f"--work {args.work} is not under --work-prefix {args.work_prefix}")
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
        child_rc = None
        timed_out = False
        try:
            proc = subprocess.Popen(prefix + cmd, env=env, cwd=cwd, start_new_session=True)
        except FileNotFoundError as exc:
            after = snapshot(declared, args.label)
            changed = [(b, a, changed_fields(b, a)) for b, a in zip(before, after)
                       if changed_fields(b, a)]
            elapsed = round(time.monotonic() - t0, 3)
            _report(args, before, after, changed, None, work, home, env, prefix + cmd, args.timeout,
                    elapsed=elapsed)
            print(f"hostguard: cannot execute {cmd[0]}: {exc.strerror}", file=sys.stderr)
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
            print(f"hostguard: child exceeded --timeout {args.timeout}s; process group killed",
                  file=sys.stderr)
        after = snapshot(declared, args.label)
        changed = [(b, a, changed_fields(b, a)) for b, a in zip(before, after) if changed_fields(b, a)]
        _report(args, before, after, changed, child_rc, work, home, env, prefix + cmd, args.timeout,
                elapsed=elapsed)
        if changed:
            return 3
        if child_rc != 0:
            return 5
        return 0
    except Refused as exc:
        print(f"hostguard: refused: {exc}", file=sys.stderr)
        return 2
    except OSError as exc:
        print(f"hostguard: internal error: {exc}", file=sys.stderr)
        return 6


def _report(args, before, after, changed, child_rc, work, home, env, cmd, timeout, elapsed=None):
    mapped = {k: env.get(k) for k in ("HOME", "XDG_CACHE_HOME", "XDG_CONFIG_HOME", "XDG_DATA_HOME",
                                      "XDG_STATE_HOME", "TMPDIR")}
    status = "violation" if changed else ("ok" if child_rc == 0 else "child-failed")
    if args.json:
        print(json.dumps({
            "command": "run", "status": status, "label": args.label, "work": work, "home": home,
            "sandbox": args.sandbox, "mask": [real(m) for m in args.mask], "ro_root": bool(args.ro_root),
            "child_rc": child_rc, "timeout_s": timeout, "elapsed_s": elapsed, "argv": cmd,
            "env": mapped, "before": before, "after": after,
            "changed": [{"path": a["path"], "fields": f} for _, a, f in changed],
        }, sort_keys=True))
        return
    head = f"# hostguard run  work={work} home={home} sandbox={args.sandbox} label={args.label} " \
           f"declared={len(before)}"
    if args.mask:
        head += " mask=" + ",".join(real(m) for m in args.mask)
    if args.ro_root:
        head += " ro_root=1"
    print(head)
    for k, v in mapped.items():
        if v is not None:
            print(f"ENV {k}={v}")
    print(f"ARGV {' '.join(cmd)}")
    print("# before")
    for r in before:
        print("BEFORE " + fmt(r))
    print("# after")
    for r in after:
        print("AFTER  " + fmt(r))
    for b, a, fields in changed:
        print(f"CHANGED path={a['path']} fields={','.join(fields)} "
              f"sha256={b['sha256']}->{a['sha256']} size={b['size']}->{a['size']} "
              f"mtime_ns={b['mtime_ns']}->{a['mtime_ns']}")
    print(f"child_rc={child_rc} elapsed_s={elapsed} changed={len(changed)} status={status} "
          f"exit={'3' if changed else ('0' if child_rc == 0 else '5')}")


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
