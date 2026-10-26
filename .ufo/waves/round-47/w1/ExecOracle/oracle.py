#!/usr/bin/env python3
"""oracle.py -- hermetic oracle harness for the pinned xdg-terminal-exec.

Runs the *real* pinned resolver (xdg-terminal-exec 0.14.3) against a
materialized fixture case inside a bubblewrap sandbox, so a re-implementation
can be judged against the judge itself.

  oracle.py run   --fixtures F.json --work DIR [--tool T] [--receipts R]
                  [--repeat N] [--timeout S] [--alt-work DIR]
  oracle.py trace --fixtures F.json --work DIR [--receipts R] [--limit N]
  oracle.py bin   --work DIR [--receipts R]

Frozen fixture schema (round 47, one JSON list of objects; a {"cases": [...]}
wrapper is also accepted):

  {"id": "<unique>",
   "class": "<edge class>",
   "env": {"XDG_CURRENT_DESKTOP": "...", "XDG_CONFIG_HOME": "$ROOT/home/.config",
           "XDG_CONFIG_DIRS": "...", "XDG_DATA_HOME": "...",
           "XDG_DATA_DIRS": "..."},        # absent key = variable unset
   "files": {"<root-relative path>": "<text>"},
   "exec": ["<root-relative path of an executable stub>"],
   "args": ["--print-id", "--print-path", "--print-cmd"],
   "expect": {"rc": 0, "stdout": "<stdout with the case root replaced by $ROOT>"}}

$ROOT is the case root (DIR/<id>).  It is substituted in env values, in
materialized file contents and in case args.  HOME is always $ROOT/home, PATH
is always $ROOT/bin:/oracle/bin, XDG_CACHE_HOME is always the empty per-run
directory $ROOT/.oracle-rw/cache (cold cache; it is wiped before every run).

Sandbox contract (exact argv is written to <receipts>/sandbox-argv.txt):

  * --unshare-all: no network, new user/pid/ipc/uts/cgroup namespaces.
  * --clearenv plus exactly the case env; no host env leaks in.
  * host /usr/lib mounted read-only (shared libraries + ld.so); /lib and /lib64
    are symlinks to usr/lib.
  * /bin/sh is the host bash (this host has no dash); /bin/bash likewise.
  * /oracle/bin holds ONLY the external commands the pinned script execs
    (see EXTERNALS, established with strace -f -e trace=execve).
  * NO host /usr/bin, /home, /fast, /etc/xdg, /usr/share/applications: the
    sandbox root is a fresh tmpfs plus the case root (read-only) and its
    writable .oracle-rw overlay.
  * --dev /dev (the script redirects to /dev/null), --proc /proc, --tmpfs /tmp.

A case whose args contain no print mode (or --test) would launch a terminal, so
it is refused outright rather than run.

Output per case: rc, stdout with the case root replaced by $ROOT, stderr
digest; plus determinism (N repeats, fresh per-run dir) and root independence
(the whole set re-materialized under a second work root and compared after
substitution).  Exit status: 0 = every checked property held, 1 = a mismatch or
a violated invariant, 2 = usage error.
"""

import argparse
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import time
import traceback

PROG = "oracle.py"
PIN_SRC = "/usr/bin/xdg-terminal-exec"
PIN_SHA256 = "89f2be9a65deb8df93633a9a09b4953a921c83d591ab987f7569280ecd3127ac"

# External commands the pinned script actually execs, established by
# `oracle.py trace` (strace -f -e trace=execve) over config/cache/entry
# variants: tr (lowercase XDG_CURRENT_DESKTOP), find -L (entry scan),
# awk (entry path -> ID), ls -LRl + md5sum (cache hash), mkdir/rm (cache
# directory and cache invalidation).  `printf`, `read`, `command`, `alias`,
# `umask` are shell builtins; shcat is the script's own builtin cat.
EXTERNALS = ("tr", "find", "awk", "ls", "md5sum", "mkdir", "rm")
SHELL = "/usr/bin/bash"
BASH = "/usr/bin/bash"

TIMEOUT_RC = 124
PRINT_OPTIONS = ("--print-id", "--print-path", "--print-content", "--print-cmd")
RESERVED_IDS = {"bin", "pin", "tool", "receipts"}
SANDBOX_BIN = "/oracle/bin"
SANDBOX_PIN = "/oracle/xdg-terminal-exec"
SANDBOX_TOOL = "/oracle/tool"


# --------------------------------------------------------------------------
# small helpers
# --------------------------------------------------------------------------

def sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def sha256_bytes(data):
    return hashlib.sha256(data).hexdigest()


def die(msg, code=2):
    sys.stderr.write("%s: %s\n" % (PROG, msg))
    raise SystemExit(code)


def safe_rel(value, field):
    """Validate a root-relative fixture path; return its normalized form."""
    if not isinstance(value, str) or value == "":
        die("fixture %s: path is not a non-empty string: %r" % (field, value))
    if "\x00" in value or value.startswith("/"):
        die("fixture %s: path must be root-relative: %r" % (field, value))
    parts = value.split("/")
    for part in parts:
        if part in ("", ".", ".."):
            die("fixture %s: unsafe path component in %r" % (field, value))
    return "/".join(parts)


def subst_root(text, root):
    return text.replace("$ROOT", root)


def norm_stream(data, root):
    """Replace the case root (bytes) with the literal $ROOT."""
    return data.replace(root.encode(), b"$ROOT")


def decode(data):
    return data.decode("utf-8", "surrogateescape")


def short(text, limit=120):
    text = text.replace("\n", "\\n")
    return text if len(text) <= limit else text[: limit - 3] + "..."


# --------------------------------------------------------------------------
# fixture loading / validation
# --------------------------------------------------------------------------

ALLOWED_ENV = (
    "XDG_CURRENT_DESKTOP",
    "XDG_CONFIG_HOME",
    "XDG_CONFIG_DIRS",
    "XDG_DATA_HOME",
    "XDG_DATA_DIRS",
)
HARNESS_ENV = ("HOME", "PATH", "XDG_CACHE_HOME")


class Case(object):
    def __init__(self, raw):
        self.id = raw.get("id")
        self.cls = raw.get("class", "")
        self.env = raw.get("env") or {}
        self.files = raw.get("files") or {}
        self.execs = raw.get("exec") or []
        self.args = raw.get("args") or []
        self.expect = raw.get("expect")
        self.errors = []
        self._validate()

    def _validate(self):
        if not isinstance(self.id, str) or not self.id:
            self.errors.append("id must be a non-empty string")
            self.id = self.id or "?"
        elif "/" in self.id or self.id in (".", "..") or self.id in RESERVED_IDS:
            self.errors.append("id %r is not a safe case id" % self.id)
        if not isinstance(self.env, dict):
            self.errors.append("env must be an object")
            self.env = {}
        self.extra_env = []
        for key, value in self.env.items():
            if key in HARNESS_ENV:
                self.errors.append("env must not set harness-controlled %s" % key)
            elif not isinstance(value, str):
                self.errors.append("env[%s] must be a string" % key)
            elif key not in ALLOWED_ENV:
                # forward compatible: passed through, but recorded
                self.extra_env.append(key)
        if not isinstance(self.files, dict):
            self.errors.append("files must be an object")
            self.files = {}
        for path, text in self.files.items():
            try:
                safe_rel(path, "files")
            except SystemExit:
                self.errors.append("files key %r is not a safe relative path" % path)
            if not isinstance(text, str):
                self.errors.append("files[%s] must be a string" % path)
        if not isinstance(self.execs, list) or not all(
            isinstance(p, str) for p in self.execs
        ):
            self.errors.append("exec must be a list of root-relative paths")
            self.execs = []
        if not isinstance(self.args, list) or not all(
            isinstance(a, str) for a in self.args
        ):
            self.errors.append("args must be a list of strings")
            self.args = []
        if self.expect is not None:
            if not isinstance(self.expect, dict) or "rc" not in self.expect:
                self.errors.append("expect must be an object with rc")
            elif not isinstance(self.expect.get("stdout", ""), str):
                self.errors.append("expect.stdout must be a string")
        if not any(
            a in PRINT_OPTIONS
            or any(a.startswith(opt + "=") for opt in PRINT_OPTIONS)
            or a == "--test"
            for a in self.args
        ):
            self.errors.append(
                "refused: args ask the resolver to launch a terminal "
                "(no --print-* / --test)"
            )

    @property
    def ok(self):
        return not self.errors


def load_fixtures(path):
    try:
        with open(path, "r", encoding="utf-8") as fh:
            data = json.load(fh)
    except (OSError, ValueError) as exc:
        die("cannot read fixtures %s: %s" % (path, exc))
    if isinstance(data, dict):
        data = data.get("cases", [])
    if not isinstance(data, list):
        die("fixtures must be a JSON list of case objects")
    seen = set()
    cases = []
    for raw in data:
        if not isinstance(raw, dict):
            die("fixture entry is not an object: %r" % (raw,))
        case = Case(raw)
        if case.id in seen:
            case.errors.append("duplicate case id")
        seen.add(case.id)
        cases.append(case)
    return cases


# --------------------------------------------------------------------------
# sandbox materialization
# --------------------------------------------------------------------------

class Sandbox(object):
    """Bin/pin/tool assets shared by every case under one work root."""

    def __init__(self, work):
        self.work = os.path.abspath(work)
        self.bin = os.path.join(self.work, "bin")
        self.pin = os.path.join(self.work, "pin")
        self.pin_file = os.path.join(self.pin, "xdg-terminal-exec")
        self.tool_dir = os.path.join(self.work, "tool")
        self.tool_file = None
        self.tool_sha = None
        self.manifest = []

    def prepare(self, tool=None):
        self.bwrap = shutil.which("bwrap")
        if not self.bwrap:
            die("bubblewrap (bwrap) is required and is not on PATH")
        for path in (self.bin, self.pin):
            if os.path.isdir(path):
                shutil.rmtree(path)
            os.makedirs(path)
        for name in EXTERNALS:
            src = shutil.which(name)
            if not src:
                die("required host command %r is not on PATH" % name)
            real = os.path.realpath(src)
            dest = os.path.join(self.bin, name)
            shutil.copyfile(real, dest)
            os.chmod(dest, 0o755)
            self.manifest.append((name, real, sha256_file(dest)))
        # pinned resolver
        if not os.path.isfile(PIN_SRC):
            die("pinned resolver missing: %s" % PIN_SRC)
        got = sha256_file(PIN_SRC)
        if got != PIN_SHA256:
            die("pinned resolver sha256 mismatch: %s (want %s)" % (got, PIN_SHA256))
        shutil.copyfile(PIN_SRC, self.pin_file)
        os.chmod(self.pin_file, 0o755)
        if sha256_file(self.pin_file) != PIN_SHA256:
            die("copy of pinned resolver does not match the pin")
        self.pin_sha = PIN_SHA256
        # optional tool under test
        if tool:
            if not os.path.isfile(tool):
                die("--tool is not a file: %s" % tool)
            if os.path.isdir(self.tool_dir):
                shutil.rmtree(self.tool_dir)
            os.makedirs(self.tool_dir)
            self.tool_file = os.path.join(self.tool_dir, os.path.basename(tool))
            shutil.copyfile(tool, self.tool_file)
            os.chmod(self.tool_file, 0o755)
            self.tool_sha = sha256_file(self.tool_file)
        return self

    def argv(self, root, case, tool=False):
        """Exact bwrap argv for one case run (the command is the last element)."""
        rw = os.path.join(root, ".oracle-rw")
        cache = os.path.join(rw, "cache")
        argv = [
            self.bwrap,
            "--unshare-all",
            "--die-with-parent",
            "--new-session",
            "--clearenv",
            "--ro-bind", "/usr/lib", "/usr/lib",
            "--symlink", "usr/lib", "/lib",
            "--symlink", "usr/lib", "/lib64",
            "--ro-bind", SHELL, "/bin/sh",
            "--ro-bind", BASH, "/bin/bash",
            "--ro-bind", self.bin, SANDBOX_BIN,
            "--ro-bind", self.pin_file, SANDBOX_PIN,
            "--dev", "/dev",
            "--proc", "/proc",
            "--tmpfs", "/tmp",
            "--ro-bind", root, root,
            "--bind", rw, rw,
            "--chdir", "/",
        ]
        if tool:
            # the tool under test may be a python script: give it a runtime at
            # the conventional path (not on PATH, so the resolver's own
            # `command -v` probing is unaffected).
            argv += ["--ro-bind", self.tool_file, SANDBOX_TOOL]
            for host, dest in (
                ("/usr/bin/python3", "/usr/bin/python3"),
                ("/usr/bin/env", "/usr/bin/env"),
            ):
                if os.path.exists(host):
                    argv += ["--ro-bind", host, dest]
        env = {}
        for key, value in case.env.items():
            env[key] = subst_root(value, root)
        env["HOME"] = os.path.join(root, "home")
        env["PATH"] = os.path.join(root, "bin") + ":" + SANDBOX_BIN
        env["XDG_CACHE_HOME"] = cache
        for key in sorted(env):
            argv += ["--setenv", key, env[key]]
        if tool:
            argv += [SANDBOX_TOOL, "print"]
        else:
            argv += [SANDBOX_PIN]
        argv += [subst_root(a, root) for a in case.args]
        return argv, rw


def stub_text(root, label):
    """Executable stub: if anything ever runs it, it records the tripwire."""
    marker = os.path.join(root, ".oracle-rw", "stub-ran")
    return (
        "#!/bin/sh\n"
        "# oracle terminal stub for " + label + "\n"
        "printf 'STUB-RAN %s %s\\n' \"$0\" \"$*\" >> '" + marker + "'\n"
        "exit 1\n"
    )


def materialize(case, root):
    """Create DIR/<id>/ for one case and return a small materialization report."""
    if os.path.isdir(root):
        shutil.rmtree(root)
    os.makedirs(root)
    os.makedirs(os.path.join(root, "home"))
    os.makedirs(os.path.join(root, "bin"))
    substituted = 0
    for rel, text in case.files.items():
        rel = safe_rel(rel, "files")
        dest = os.path.join(root, rel)
        parent = os.path.dirname(dest)
        if parent:
            os.makedirs(parent, exist_ok=True)
        body = subst_root(text, root)
        if body != text:
            substituted += 1
        with open(dest, "w", encoding="utf-8", newline="") as fh:
            fh.write(body)
    synthesized = []
    executable = []
    for rel in case.execs:
        rel = safe_rel(rel, "exec")
        dest = os.path.join(root, rel)
        parent = os.path.dirname(dest)
        if parent:
            os.makedirs(parent, exist_ok=True)
        if not os.path.exists(dest):
            with open(dest, "w", encoding="utf-8", newline="") as fh:
                fh.write(stub_text(root, rel))
            synthesized.append(rel)
        else:
            with open(dest, "rb") as fh:
                head = fh.readline()
            if not head.startswith(b"#!"):
                with open(dest, "w", encoding="utf-8", newline="") as fh:
                    fh.write(stub_text(root, rel))
                synthesized.append(rel)
        os.chmod(dest, 0o755)
        executable.append(rel)
    reset_run_dir(root)
    return {
        "files": len(case.files),
        "root_substituted_files": substituted,
        "exec_synthesized": synthesized,
        "exec_materialized": executable,
    }


def reset_run_dir(root):
    """Fresh per-run dir: cold cache (absent) and a clean stub marker.

    XDG_CACHE_HOME points at <rw>/cache, which is deliberately absent at the
    start of every run: the pinned resolver's own `mkdir -p` creates it when
    its background cache saver wins the race, so both branches (mkdir present /
    absent) are reachable without changing the observable stdout.
    """
    rw = os.path.join(root, ".oracle-rw")
    if os.path.isdir(rw):
        shutil.rmtree(rw)
    os.makedirs(rw)


# --------------------------------------------------------------------------
# running
# --------------------------------------------------------------------------

def run_once(sandbox, root, case, timeout, tool=False):
    reset_run_dir(root)
    argv, _rw = sandbox.argv(root, case, tool=tool)
    started = time.time()
    try:
        proc = subprocess.run(
            argv,
            stdin=subprocess.DEVNULL,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            timeout=timeout,
            env={"PATH": "/usr/bin:/bin"},
        )
        rc, out, err = proc.returncode, proc.stdout, proc.stderr
        timed_out = False
    except subprocess.TimeoutExpired as exc:
        rc, out, err = 124, exc.stdout or b"", exc.stderr or b""
        timed_out = True
    duration = int((time.time() - started) * 1000)
    norm_out = norm_stream(out, root)
    norm_err = norm_stream(err, root)
    marker = os.path.join(root, ".oracle-rw", "stub-ran")
    stub_ran = os.path.exists(marker)
    stub_lines = []
    if stub_ran:
        with open(marker, "r", encoding="utf-8", errors="replace") as fh:
            stub_lines = fh.read().splitlines()[:10]
    return {
        "rc": rc,
        "stdout": decode(norm_out),
        "stdout_sha256": sha256_bytes(norm_out),
        "stderr_digest": "sha256:" + sha256_bytes(norm_err),
        "stderr_bytes": len(norm_err),
        "stderr_head": short(decode(norm_err), 200),
        "stub_ran": stub_ran,
        "stub_lines": stub_lines,
        "timed_out": timed_out,
        "duration_ms": duration,
    }


def fingerprint(record):
    return (record["rc"], record["stdout"], record["stderr_digest"])


def check_expect(case, record):
    if case.expect is None:
        return "no_expect", None
    want_rc = case.expect.get("rc")
    want_out = case.expect.get("stdout", "")
    if want_out is not None and not isinstance(want_out, str):
        return "mismatch", "expect.stdout is not a string"
    if want_out is None:
        want_out = ""
    got_rc = record["rc"]
    if got_rc != want_rc:
        return "mismatch", "rc %s != expect %s" % (got_rc, want_rc)
    if record["stdout"] != want_out:
        return "mismatch", "stdout differs (got %r, want %r)" % (
            short(record["stdout"], 160),
            short(want_out, 160),
        )
    return "match", None


# --------------------------------------------------------------------------
# receipts
# --------------------------------------------------------------------------

def write_argv_template(path, sandbox, tool_requested):
    lines = [
        "# exact bwrap argv template produced by oracle.py run",
        "# substitutions: <WORK> = --work DIR (absolute), <ROOT> = DIR/<case-id>,",
        "#                <RW> = <ROOT>/.oracle-rw (writable), <CACHE> = <RW>/cache",
        "# the argv below is one real invocation with <WORK> and <ROOT> abstracted",
        "# (paths under the operator scratch tree are not citable evidence).",
        "",
        sandbox.bwrap,
        "  --unshare-all",
        "  --die-with-parent",
        "  --new-session",
        "  --clearenv",
        "  --ro-bind /usr/lib /usr/lib",
        "  --symlink usr/lib /lib",
        "  --symlink usr/lib /lib64",
        "  --ro-bind %s /bin/sh" % SHELL,
        "  --ro-bind %s /bin/bash" % BASH,
        "  --ro-bind <WORK>/bin %s" % SANDBOX_BIN,
        "  --ro-bind <WORK>/pin/xdg-terminal-exec %s" % SANDBOX_PIN,
        "  --dev /dev",
        "  --proc /proc",
        "  --tmpfs /tmp",
        "  --ro-bind <ROOT> <ROOT>",
        "  --bind <RW> <RW>",
        "  --chdir /",
    ]
    if tool_requested:
        lines += [
            "  --ro-bind /usr/bin/python3 /usr/bin/python3",
            "  --ro-bind /usr/bin/env /usr/bin/env",
        ]
    lines += [
        "  --setenv <CASE ENV KEYS> <values, $ROOT substituted>",
        "  --setenv HOME <ROOT>/home",
        "  --setenv PATH <ROOT>/bin:%s" % SANDBOX_BIN,
        "  --setenv XDG_CACHE_HOME <CACHE>",
        "  <oracle-tool> print ...args   # only under --tool" if tool_requested else "",
        "  %s <case args>" % SANDBOX_PIN,
        "",
        "# external commands in %s (only these are bound; established by `oracle.py trace`):"
        % SANDBOX_BIN,
        "#   " + " ".join(EXTERNALS),
        "# shell: /bin/sh and /bin/bash = %s (host has no dash)" % BASH,
        "",
    ]
    with open(path, "w", encoding="utf-8") as fh:
        fh.write("\n".join(lines))


def write_receipts(receipts, sandbox, cases, results, meta):
    os.makedirs(receipts, exist_ok=True)
    with open(os.path.join(receipts, "pin.txt"), "w", encoding="utf-8") as fh:
        fh.write("source: %s\n" % PIN_SRC)
        fh.write("expected sha256: %s\n" % PIN_SHA256)
        fh.write("copied sha256:   %s\n" % sha256_file(sandbox.pin_file))
        fh.write("copy: <WORK>/pin/xdg-terminal-exec\n")
    with open(os.path.join(receipts, "bin-manifest.tsv"), "w", encoding="utf-8") as fh:
        fh.write("name\thost_path\tsha256\n")
        for name, host, digest in sandbox.manifest:
            fh.write("%s\t%s\t%s\n" % (name, host, digest))
        fh.write("sh\t%s\t%s\n" % (BASH, sha256_file(BASH)))
    write_argv_template(
        os.path.join(receipts, "sandbox-argv.txt"),
        sandbox,
        bool(sandbox.tool_file),
    )
    columns = [
        "id",
        "class",
        "rc",
        "stdout_sha256",
        "expect",
        "determinism",
        "root_independence",
        "tool",
        "stub_ran",
        "timed_out",
        "duration_ms",
    ]
    with open(os.path.join(receipts, "cases.tsv"), "w", encoding="utf-8") as fh:
        fh.write("\t".join(columns) + "\n")
        for row in results:
            fh.write(
                "\t".join(
                    [
                        row["id"],
                        row["class"],
                        str(row["rc"]),
                        row["stdout_sha256"][:16],
                        row["expect"],
                        row["determinism"],
                        row["root_independence"],
                        row["tool"],
                        "yes" if row["stub_ran"] else "no",
                        "yes" if row["timed_out"] else "no",
                        str(row["duration_ms"]),
                    ]
                )
                + "\n"
            )
    payload = dict(meta)
    payload["cases"] = []
    for case, row in zip(cases, results):
        entry = {
            "id": row["id"],
            "class": row["class"],
            "errors": case.errors,
            "record": row["record"],
            "repeats": row["repeats"],
            "expect": row["expect"],
            "expect_detail": row["expect_detail"],
            "determinism": row["determinism"],
            "root_independence": row["root_independence"],
            "timed_out": row["timed_out"],
            "alt": row["alt"],
            "materialization": row["materialization"],
            "extra_env": case.extra_env,
            "tool": row["tool"],
            "tool_record": row["tool_record"],
        }
        payload["cases"].append(entry)
    with open(os.path.join(receipts, "run.json"), "w", encoding="utf-8") as fh:
        json.dump(payload, fh, indent=1, sort_keys=True)
        fh.write("\n")
    return payload


# --------------------------------------------------------------------------
# subcommands
# --------------------------------------------------------------------------

def cmd_bin(args):
    sandbox = Sandbox(args.work).prepare(tool=args.tool)
    receipts = os.path.abspath(args.receipts)
    os.makedirs(receipts, exist_ok=True)
    with open(os.path.join(receipts, "pin.txt"), "w", encoding="utf-8") as fh:
        fh.write("source: %s\nexpected sha256: %s\ncopied sha256: %s\n"
                 % (PIN_SRC, PIN_SHA256, sha256_file(sandbox.pin_file)))
    with open(os.path.join(receipts, "bin-manifest.tsv"), "w", encoding="utf-8") as fh:
        fh.write("name\thost_path\tsha256\n")
        for name, host, digest in sandbox.manifest:
            fh.write("%s\t%s\t%s\n" % (name, host, digest))
        fh.write("sh\t%s\t%s\n" % (BASH, sha256_file(BASH)))
    print("PIN ok %s" % PIN_SHA256)
    for name, host, digest in sandbox.manifest:
        print("BIN %-8s %s %s" % (name, digest[:16], host))
    print("BIN sh       %s %s" % (sha256_file(BASH)[:16], BASH))
    if sandbox.tool_file:
        print("TOOL %s %s" % (sandbox.tool_sha, sandbox.tool_file))
    print("ORACLE_BIN: %s" % sandbox.bin)
    return 0


def cmd_run(args):
    work = os.path.abspath(args.work)
    os.makedirs(work, exist_ok=True)
    receipts = os.path.abspath(args.receipts)
    cases = load_fixtures(args.fixtures)
    sandbox = Sandbox(work).prepare(tool=args.tool)
    alt_work = os.path.abspath(
        args.alt_work or (work.rstrip(os.sep) + "-altroot")
    )
    os.makedirs(alt_work, exist_ok=True)
    alt_sandbox = Sandbox(alt_work).prepare(tool=args.tool)

    print("PIN ok %s" % PIN_SHA256)
    print("BIN %d externals + /bin/sh: %s" % (len(EXTERNALS), " ".join(EXTERNALS)))
    if sandbox.tool_file:
        print("TOOL %s %s" % (sandbox.tool_sha, os.path.basename(sandbox.tool_file)))

    results = []
    failures = []
    materialization = {}
    for case in cases:
        row = {
            "id": case.id,
            "class": case.cls,
            "rc": "",
            "stdout_sha256": "",
            "expect": "invalid",
            "expect_detail": None,
            "determinism": "n/a",
            "root_independence": "n/a",
            "tool": "n/a",
            "stub_ran": False,
            "timed_out": False,
            "duration_ms": 0,
            "record": None,
            "repeats": [],
            "alt": None,
            "materialization": None,
            "tool_record": None,
        }
        if not case.ok:
            row["expect"] = "invalid"
            row["expect_detail"] = "; ".join(case.errors)
            results.append(row)
            failures.append("%s: invalid fixture (%s)" % (case.id, row["expect_detail"]))
            print("CASE %-28s INVALID %s" % (case.id, row["expect_detail"]))
            continue
        root = os.path.join(work, case.id)
        row["materialization"] = materialize(case, root)
        materialization[case.id] = row["materialization"]
        repeats = []
        for _ in range(max(1, args.repeat)):
            repeats.append(run_once(sandbox, root, case, args.timeout))
        record = repeats[0]
        prints = [fingerprint(r) for r in repeats]
        det_ok = all(item == prints[0] for item in prints)
        row["determinism"] = "ok" if det_ok else "FAIL"
        row["repeats"] = [
            {
                "rc": r["rc"],
                "stdout_sha256": r["stdout_sha256"],
                "stderr_digest": r["stderr_digest"],
                "stub_ran": r["stub_ran"],
            }
            for r in repeats
        ]
        # root independence: same case, different absolute work root
        alt_root = os.path.join(alt_work, case.id)
        materialize(case, alt_root)
        alt = run_once(alt_sandbox, alt_root, case, args.timeout)
        alt_ok = fingerprint(alt) == fingerprint(record)
        row["root_independence"] = "ok" if alt_ok else "FAIL"
        row["alt"] = {
            "rc": alt["rc"],
            "stdout_sha256": alt["stdout_sha256"],
            "stderr_digest": alt["stderr_digest"],
        }
        # expectation (produced elsewhere by the real script)
        status, detail = check_expect(case, record)
        row["expect"] = status
        row["expect_detail"] = detail
        # optional: the tool under test, same args, same sandbox
        if sandbox.tool_file:
            tool_rec = run_once(sandbox, root, case, args.timeout, tool=True)
            row["tool_record"] = {
                "rc": tool_rec["rc"],
                "stdout": tool_rec["stdout"],
                "stdout_sha256": tool_rec["stdout_sha256"],
                "stderr_digest": tool_rec["stderr_digest"],
                "stderr_head": tool_rec["stderr_head"],
                "stub_ran": tool_rec["stub_ran"],
            }
            same = fingerprint(tool_rec) == fingerprint(record)
            row["tool"] = "match" if same else "differ"
            if not same:
                failures.append(
                    "%s: tool differs (rc %s vs %s, stdout %r vs %r)"
                    % (case.id, tool_rec["rc"], record["rc"],
                       short(tool_rec["stdout"], 60), short(record["stdout"], 60))
                )
        row["rc"] = record["rc"]
        row["stdout_sha256"] = record["stdout_sha256"]
        row["duration_ms"] = record["duration_ms"]
        row["record"] = record
        row["stub_ran"] = record["stub_ran"]
        row["timed_out"] = record["timed_out"]
        if record["timed_out"] and not (
            args.allow_timeout
            and case.expect is not None
            and case.expect.get("rc") == TIMEOUT_RC
        ):
            failures.append(
                "%s: resolver did not answer within %ss (timeout rc %s)"
                % (case.id, args.timeout, TIMEOUT_RC)
            )
        if record["stub_ran"]:
            failures.append("%s: terminal stub was EXECUTED (%s)" %
                            (case.id, record["stub_lines"]))
        if not det_ok:
            failures.append("%s: non-deterministic across repeats" % case.id)
        if not alt_ok:
            failures.append("%s: differs between work roots" % case.id)
        if status == "mismatch":
            failures.append("%s: expect mismatch: %s" % (case.id, detail))
        print(
            "CASE %-28s class=%-18s rc=%-3s out=%-10s det=%-4s root=%-4s tool=%s%s%s"
            % (
                case.id,
                case.cls or "-",
                record["rc"],
                status,
                row["determinism"],
                row["root_independence"],
                row["tool"],
                "" if not record["stub_ran"] else " STUB-RAN!",
                "" if not record["timed_out"] else " TIMEOUT!",
            )
        )
        results.append(row)

    meta = {
        "tool": PROG,
        "code_sha256": sha256_file(os.path.abspath(__file__)),
        "pin_sha256": PIN_SHA256,
        "sandbox": {
            "bwrap": sandbox.bwrap,
            "externals": list(EXTERNALS),
            "shell": SHELL,
            "bash": BASH,
            "sandbox_bin": SANDBOX_BIN,
            "pin": SANDBOX_PIN,
            "unshare_all": True,
            "clearenv": True,
            "tmpfs_tmp": True,
        },
        "repeat": args.repeat,
        "timeout": args.timeout,
        "allow_timeout": bool(args.allow_timeout),
        "fixtures": os.path.basename(args.fixtures),
        "fixtures_sha256": sha256_file(args.fixtures),
        "tool_under_test": sandbox.tool_file,
        "tool_sha256": sandbox.tool_sha,
        "materialization": materialization,
    }
    payload = write_receipts(receipts, sandbox, cases, results, meta)

    valid = [r for r in results if r["expect"] != "invalid"]
    matched = [r for r in valid if r["expect"] == "match"]
    mismatched = [r for r in valid if r["expect"] == "mismatch"]
    no_expect = [r for r in valid if r["expect"] == "no_expect"]
    det_bad = [r for r in valid if r["determinism"] != "ok"]
    root_bad = [r for r in valid if r["root_independence"] != "ok"]
    tool_bad = [r for r in valid if r["tool"] == "differ"]
    stubbed = [r for r in results if r["stub_ran"]]
    timed = [r for r in valid if r["timed_out"]]
    print(
        "ORACLE cases=%d valid=%d match=%d mismatch=%d no_expect=%d determinism=%s "
        "root-independence=%s tool=%s stubs_ran=%d timed_out=%d"
        % (
            len(cases),
            len(valid),
            len(matched),
            len(mismatched),
            len(no_expect),
            "ok" if not det_bad else "FAIL",
            "ok" if not root_bad else "FAIL",
            "n/a" if not sandbox.tool_file else ("ok" if not tool_bad else "FAIL"),
            len(stubbed),
            len(timed),
        )
    )
    if failures:
        for line in failures[:20]:
            print("ORACLE_FAIL " + line)
        print("ORACLE_RESULT: FAIL")
        return 1
    print("ORACLE_RESULT: PASS")
    return 0


def parse_trace(log):
    """Return the set of execve() target paths recorded in one strace log."""
    names = set()
    with open(log, "r", encoding="utf-8", errors="replace") as fh:
        for line in fh:
            match = re.search(r'execve?\("([^"]+)"', line)
            if not match:
                continue
            path = match.group(1)
            if path.startswith("/usr/lib") or path.endswith("/ld-linux-x86-64.so.2"):
                continue
            names.add(path)
    return names


def cmd_trace(args):
    """Aggregate execve() names over cases, to prove the sandbox bin is complete."""
    work = os.path.abspath(args.work)
    os.makedirs(work, exist_ok=True)
    receipts = os.path.abspath(args.receipts)
    os.makedirs(receipts, exist_ok=True)
    strace = shutil.which("strace")
    if not strace:
        die("strace is needed for `trace` and is not on PATH")
    cases = load_fixtures(args.fixtures)
    sandbox = Sandbox(work).prepare()
    counts = {}
    per_case = {}
    host_counts = {}
    host_per_case = {}
    used = 0
    for case in cases:
        if not case.ok:
            continue
        if args.limit and used >= args.limit:
            break
        used += 1
        root = os.path.join(work, case.id)
        materialize(case, root)
        reset_run_dir(root)
        argv, _rw = sandbox.argv(root, case)
        log = os.path.join(work, "..", "trace-%s.log" % re.sub(r"[^A-Za-z0-9_.-]", "_", case.id))
        log = os.path.abspath(log)
        trace_argv = [strace, "-f", "-qq", "-e", "trace=execve", "-o", log] + argv
        subprocess.run(
            trace_argv,
            stdin=subprocess.DEVNULL,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            timeout=args.timeout,
            env={"PATH": "/usr/bin:/bin"},
        )
        names = set()
        try:
            names = parse_trace(log)
        finally:
            try:
                os.unlink(log)
            except OSError:
                pass
        for path in names:
            counts[path] = counts.get(path, 0) + 1
        per_case[case.id] = sorted(names)

        # second census: the same case with the pinned script run directly on
        # the host (print modes only, cache redirected).  There is no bwrap
        # init to reap the resolver's background cache saver, so the save_cache
        # path (ls | md5sum, mkdir, rm) completes here and the bin set can be
        # shown complete for both branches.
        host_cache = os.path.join(work, "hostcache", case.id)
        if os.path.isdir(host_cache):
            shutil.rmtree(host_cache)
        os.makedirs(host_cache)
        env = {k: subst_root(v, root) for k, v in case.env.items()}
        env["HOME"] = os.path.join(root, "home")
        env["PATH"] = os.path.join(root, "bin") + ":" + sandbox.bin
        env["XDG_CACHE_HOME"] = host_cache
        hlog = os.path.join(work, "..", "htrace-%s.log" % re.sub(r"[^A-Za-z0-9_.-]", "_", case.id))
        hlog = os.path.abspath(hlog)
        subprocess.run(
            [strace, "-f", "-qq", "-e", "trace=execve", "-o", hlog, PIN_SRC]
            + [subst_root(a, root) for a in case.args],
            stdin=subprocess.DEVNULL,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            timeout=args.timeout,
            env=env,
        )
        try:
            hnames = set()
            for path in parse_trace(hlog):
                if path.startswith(sandbox.bin + "/"):
                    hnames.add("<BIN>/" + os.path.basename(path))
                elif path == PIN_SRC:
                    hnames.add("<PIN>")
                elif path.startswith(root + "/"):
                    hnames.add("<ROOT>/" + path[len(root) + 1:])
                else:
                    hnames.add("<ABSOLUTE>/" + os.path.basename(path))
        finally:
            try:
                os.unlink(hlog)
            except OSError:
                pass
        for path in hnames:
            host_counts[path] = host_counts.get(path, 0) + 1
        host_per_case[case.id] = sorted(hnames)

    with open(os.path.join(receipts, "trace-execve.json"), "w", encoding="utf-8") as fh:
        json.dump({"cases": used, "per_case": per_case, "counts": counts,
                   "host_counts": host_counts, "host_per_case": host_per_case},
                  fh, indent=1, sort_keys=True)
        fh.write("\n")
    external = {}
    ignore = {os.path.realpath(shutil.which("bwrap") or ""),
              os.path.realpath(strace)}
    for path, count in sorted(counts.items()):
        base = os.path.basename(path)
        if path in ignore or base == "bwrap":
            continue  # the sandbox wrapper itself, not the resolver
        if path in ("/bin/sh", "/bin/bash", SANDBOX_PIN):
            continue
        if path.startswith(SANDBOX_BIN + "/"):
            external[base] = count
            continue
        external[path] = count
    host_external = {}
    for path, count in sorted(host_counts.items()):
        if path.startswith("<BIN>/"):
            host_external[os.path.basename(path)] = count
        elif not path.startswith("<"):
            host_external[path] = count
    missing = [name for name in external if name not in EXTERNALS]
    missing_host = [name for name in host_external if name not in EXTERNALS]
    print("TRACE cases=%d distinct_execve_paths=%d" % (used, len(counts)))
    for path, count in sorted(counts.items()):
        print("TRACE %-42s %d" % (path, count))
    print("HOSTTRACE distinct_execve_paths=%d (script run directly, print modes only)"
          % len(host_counts))
    for path, count in sorted(host_counts.items()):
        print("HOSTTRACE %-38s %d" % (path, count))
    for label, bad in (("TRACE_MISSING", missing), ("HOSTTRACE_MISSING", missing_host)):
        if bad:
            print("%s: %s" % (label, " ".join(sorted(bad))))
    if missing or missing_host:
        print("ORACLE_RESULT: FAIL")
        return 1
    print("TRACE_EXT: %s" % " ".join(sorted(external)))
    print("HOSTTRACE_EXT: %s" % " ".join(sorted(host_external)))
    print("ORACLE_RESULT: PASS")
    return 0


# --------------------------------------------------------------------------
# CLI
# --------------------------------------------------------------------------

def main(argv):
    parser = argparse.ArgumentParser(
        prog=PROG,
        description="Hermetic bubblewrap oracle for the pinned xdg-terminal-exec.",
    )
    sub = parser.add_subparsers(dest="command")

    run = sub.add_parser("run", help="materialize cases and run the pinned resolver")
    run.add_argument("--fixtures", required=True, help="fixture JSON (list of cases)")
    run.add_argument("--work", required=True, help="work root; case i lives in DIR/<id>")
    run.add_argument("--tool", default=None, help="optional tool; run as `TOOL print ARGS`")
    run.add_argument("--receipts", default=None, help="receipt directory (default: WORK/receipts)")
    run.add_argument("--repeat", type=int, default=3, help="determinism repeats (default 3)")
    run.add_argument("--timeout", type=float, default=30.0, help="per-run timeout seconds")
    run.add_argument("--alt-work", default=None,
                     help="second work root for the root-independence check")
    run.add_argument("--allow-timeout", action="store_true",
                     help="a case that times out counts as comparable only when "
                          "expect.rc is 124 (default: any timeout fails the harness)")
    run.set_defaults(func=cmd_run)

    trace = sub.add_parser("trace", help="execve census over cases (proves the bin set)")
    trace.add_argument("--fixtures", required=True)
    trace.add_argument("--work", required=True)
    trace.add_argument("--receipts", default=None)
    trace.add_argument("--limit", type=int, default=0)
    trace.add_argument("--timeout", type=float, default=30.0)
    trace.set_defaults(func=cmd_trace)

    binp = sub.add_parser("bin", help="materialize bin/ and pin/ only; print the manifest")
    binp.add_argument("--work", required=True)
    binp.add_argument("--tool", default=None)
    binp.add_argument("--receipts", default=None)
    binp.set_defaults(func=cmd_bin)

    args = parser.parse_args(argv)
    if not getattr(args, "command", None):
        parser.print_help()
        return 2
    if getattr(args, "receipts", None) is None and hasattr(args, "work"):
        args.receipts = os.path.join(os.path.abspath(args.work), "receipts")
    try:
        return args.func(args)
    except SystemExit:
        raise
    except Exception:  # pragma: no cover - harness bug surface
        traceback.print_exc()
        return 2


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
