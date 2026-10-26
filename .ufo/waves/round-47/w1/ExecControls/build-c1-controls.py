#!/usr/bin/env python3
"""Emit the round-47 C1 control candidates into c1/ (each a tools/mado-terminal.py candidate).

    python3 build-c1-controls.py [--out DIR] [--base PATH]

Near-correct variants are c1-base.py with one MODE switch flipped (so each control fails only on
the fixtures that exercise the rule it drops); the do-nothing/cheat variants are small standalone
programs.  EMBED-SH embeds the pinned script bytes it was built against (sha256 recorded in
controls-receipts/sha256.txt by the runner).
"""

import argparse
import base64
import hashlib
import os
import sys

PIN_SHA = "89f2be9a65deb8df93633a9a09b4953a921c83d591ab987f7569280ecd3127ac"
PIN = "/usr/bin/xdg-terminal-exec"

MODES = [
    ("REF-MINI", "ref", "positive control: the base resolver, unflipped"),
    ("FIRSTLINE", "firstline",
     "cheat: first entry line of the first list file, no validation, no fallback"),
    ("NOVALIDATE", "novalidate",
     "cheat: Hidden / TryExec / Categories / OnlyShowIn / NotShowIn are not checked"),
    ("NODESKTOP", "nodesktop", "cheat: ignores ${desktop}-xdg-terminals.list files"),
    ("REVERSED-DIRS", "reversed", "cheat: application data dirs searched in reverse preference"),
    ("TYPE-CHECK", "typecheck",
     "cheat: rejects an entry whose Type is not Application (the script never reads Type)"),
]

STUB = '''#!/usr/bin/env python3
"""C1 control STUB - the do-nothing candidate: exit 0, print nothing, test nothing.

Usage: mado-terminal.py print [...] | explain | --selftest  (all silent)

Every clause of the C1 counter must reject this: clause s finds no
`MADO_TERMINAL_SELFTEST: N/N passed` line, clauses f and g compare empty stdout with the pinned
script's output on every fixture and nonce case (rc 0 is only right where the script exits 0).
"""

import sys


def main(argv):
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
'''

CONST = '''#!/usr/bin/env python3
"""C1 control CONST - always prints the host answer, whatever the case contains.

--print-id       -> Alacritty.desktop
--print-path     -> $XDG_DATA_HOME/applications/Alacritty.desktop (the user override shape)
--print-cmd      -> alacritty plus the host entry's own arg keys (-e, --working-directory=)

Rejected by clause f where stdout differs (every case whose root is not the host's, i.e. every
fixture's --print-path) and by clause g on every nonce case; it can only pass a host-shaped case
that asks for --print-id or --print-cmd alone, which is what a fixture set must not consist of.
"""

import os
import sys


def printf_b(seq):
    out = []
    i = 0
    n = len(seq)
    while i < n:
        c = seq[i]
        if c != "\\\\":
            out.append(c)
            i += 1
            continue
        i += 1
        if i >= n:
            out.append("\\\\")
            break
        e = seq[i]
        i += 1
        if e == "n":
            out.append("\\n")
        elif e == "t":
            out.append("\\t")
        elif e == "r":
            out.append("\\r")
        elif e == "\\\\":
            out.append("\\\\")
        else:
            out.append("\\\\" + e)
    return "".join(out)


def main(argv):
    if argv[:1] == ["--selftest"]:
        sys.stdout.write("MADO_TERMINAL_SELFTEST: 30/30 passed\\n")
        return 0
    if argv[:1] == ["explain"]:
        data_home = os.environ.get("XDG_DATA_HOME") or os.path.join(
            os.environ.get("HOME", ""), ".local", "share")
        path = os.path.join(data_home, "applications", "Alacritty.desktop")
        sys.stdout.write("MADO_TERM: selected=Alacritty.desktop path=%s verdict=OK\\n" % path)
        return 0
    if argv[:1] != ["print"]:
        sys.stderr.write("usage: mado-terminal.py print [...]\\n")
        return 2
    args = argv[1:]
    parts = []
    delim = "\\\\n"
    cmd_delim = "\\\\n"
    appid = title = dirv = ""
    hold = False
    rest = []
    i = 0
    while i < len(args):
        a = args[i]
        i += 1
        if a == "--":
            rest = args[i:]
            break
        if a == "-e":
            rest = args[i:]
            break
        if a.startswith("--app-id="):
            appid = a.split("=", 1)[1]
        elif a.startswith("--title="):
            title = a.split("=", 1)[1]
        elif a.startswith("--dir="):
            dirv = a.split("=", 1)[1]
        elif a == "--hold":
            hold = True
        elif a in ("--print-id", "--print-path", "--print-content", "--print-cmd"):
            parts.append(a[len("--print-"):])
        elif a.startswith("--print-cmd="):
            parts.append("cmd")
            cmd_delim = a.split("=", 1)[1]
        elif a.startswith("--print-delimiter="):
            delim = a.split("=", 1)[1]
        elif a.startswith("-"):
            continue
        else:
            rest = args[i - 1:]
            break
    if not parts:
        sys.stderr.write("CONST: no --print-* option, refusing to launch\\n")
        return 2
    data_home = os.environ.get("XDG_DATA_HOME") or os.path.join(
        os.environ.get("HOME", ""), ".local", "share")
    path = os.path.join(data_home, "applications", "Alacritty.desktop")
    out = []
    first = True
    if "id" in parts:
        out.append("Alacritty.desktop")
        first = False
    if "path" in parts:
        if not first:
            out.append(printf_b(delim))
        out.append(path)
        first = False
    if "content" in parts:
        if not first:
            out.append(printf_b(delim))
        try:
            with open(path, "rb") as fh:
                out.append(fh.read().decode("utf-8", "surrogateescape"))
        except OSError:
            pass
        first = False
    if "cmd" not in parts:
        if "content" not in parts and delim == "\\\\n":
            out.append("\\n")
        sys.stdout.write("".join(out))
        return 0
    argv_out = []
    if rest:
        argv_out = ["-e"] + rest
    if dirv:
        argv_out = ["--working-directory=" + dirv] + argv_out
    if hold:
        argv_out = ["--hold"] + argv_out
    if title:
        argv_out = ["--title=" + title] + argv_out
    if appid:
        argv_out = ["--class=" + appid] + argv_out
    argv_out = ["alacritty"] + argv_out
    if not first:
        out.append(printf_b(delim))
    sep = printf_b(cmd_delim) if cmd_delim != "" else "\\n"
    out.append(sep.join(argv_out))
    if cmd_delim == "\\\\n" or (not first and delim == "\\\\n"):
        out.append("\\n")
    sys.stdout.write("".join(out))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
'''

DELEGATE = '''#!/usr/bin/env python3
"""C1 control DELEGATE - os.execv of the pinned script; no model of the contract at all.

Rejected by clause r first (the strace net counts a second execve, the fake /usr/bin/xdg-terminal-exec
net replaces its answer), and by clause i because the delegated run is outside the tool's own
process.  If a counter only compared stdout it would score this TARGET_MET, which is why the
tripwire is not optional.
"""

import os
import sys

REAL = "/usr/bin/xdg-terminal-exec"


def main(argv):
    if argv[:1] == ["--selftest"]:
        sys.stdout.write("MADO_TERMINAL_SELFTEST: 30/30 passed\\n")
        return 0
    if argv[:1] == ["explain"]:
        sys.stderr.write("DELEGATE: explain is not implemented\\n")
        return 2
    args = argv[1:] if argv[:1] == ["print"] else argv
    try:
        os.execv(REAL, ["xdg-terminal-exec"] + args)
    except OSError as exc:
        sys.stderr.write("DELEGATE: %s\\n" % exc)
        return 127


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
'''

SUBPROC = '''#!/usr/bin/env python3
"""C1 control SUBPROC - subprocess.run of the pinned script, stdout/rc copied through.

Rejected by clause r (two execve calls: the interpreter and the script; and the sandbox's fake
/usr/bin/xdg-terminal-exec answers instead of the script) - clause f can still look byte-equal
when the fake is absent, so r is the clause that has to carry this control.
"""

import subprocess
import sys

REAL = "/usr/bin/xdg-terminal-exec"


def main(argv):
    if argv[:1] == ["--selftest"]:
        sys.stdout.write("MADO_TERMINAL_SELFTEST: 30/30 passed\\n")
        return 0
    if argv[:1] == ["explain"]:
        sys.stderr.write("SUBPROC: explain is not implemented\\n")
        return 2
    args = argv[1:] if argv[:1] == ["print"] else argv
    try:
        proc = subprocess.run([REAL] + args, capture_output=True)
    except OSError as exc:
        sys.stderr.write("SUBPROC: %s\\n" % exc)
        return 127
    sys.stdout.buffer.write(proc.stdout)
    sys.stdout.flush()
    sys.stderr.buffer.write(proc.stderr)
    return proc.returncode


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
'''

EMBED_SH = '''#!/usr/bin/env python3
"""C1 control EMBED-SH - the pinned script's bytes embedded, written out and run by /bin/sh.

The script text is the pinned v0.14.3 body (sha256 __PIN_SHA__), carried base64-encoded.  Rejected
by clause r (a second execve for /bin/sh, and the sandbox's fake sh/shell bindings fire) even
though its stdout is the oracle's own; clause i's fake-shell binding is the second net.
"""

import base64
import os
import subprocess
import sys
import tempfile

SCRIPT = base64.b64decode("__SCRIPT_B64__")
PIN_SHA256 = "__PIN_SHA__"


def main(argv):
    if argv[:1] == ["--selftest"]:
        sys.stdout.write("MADO_TERMINAL_SELFTEST: 30/30 passed\\n")
        return 0
    if argv[:1] == ["explain"]:
        sys.stderr.write("EMBED-SH: explain is not implemented\\n")
        return 2
    args = argv[1:] if argv[:1] == ["print"] else argv
    base = os.environ.get("TMPDIR") or tempfile.gettempdir()
    fd, path = tempfile.mkstemp(prefix="mado-terminal-embed-", dir=base)
    try:
        os.write(fd, SCRIPT)
        os.close(fd)
        proc = subprocess.run(["/bin/sh", path] + args, capture_output=True)
    finally:
        try:
            os.unlink(path)
        except OSError:
            pass
    sys.stdout.buffer.write(proc.stdout)
    sys.stdout.flush()
    sys.stderr.buffer.write(proc.stderr)
    return proc.returncode


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
'''

CTYPES_EXEC = '''#!/usr/bin/env python3
"""C1 control CTYPES-EXEC - execve(2) through libc via ctypes instead of os.execv.

Same syscall as DELEGATE; it exists to check that clause r traces the syscall and not the Python
API: the strace net still counts the second execve, and the fake /usr/bin/xdg-terminal-exec binding
still answers in its place.
"""

import ctypes
import os
import sys

REAL = "/usr/bin/xdg-terminal-exec"


def main(argv):
    if argv[:1] == ["--selftest"]:
        sys.stdout.write("MADO_TERMINAL_SELFTEST: 30/30 passed\\n")
        return 0
    if argv[:1] == ["explain"]:
        sys.stderr.write("CTYPES-EXEC: explain is not implemented\\n")
        return 2
    args = argv[1:] if argv[:1] == ["print"] else argv
    av = ["xdg-terminal-exec"] + list(args)
    libc = ctypes.CDLL(None, use_errno=True)
    argv_arr = (ctypes.c_char_p * (len(av) + 1))()
    for i, a in enumerate(av):
        argv_arr[i] = a.encode()
    env_items = ["%s=%s" % (k, v) for k, v in os.environ.items()]
    envp = (ctypes.c_char_p * (len(env_items) + 1))()
    for i, item in enumerate(env_items):
        envp[i] = item.encode()
    ctypes.set_errno(0)
    libc.execve(REAL.encode(), argv_arr, envp)
    err = ctypes.get_errno()
    sys.stderr.write("CTYPES-EXEC: execve failed: %s\\n" % os.strerror(err))
    return 127


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
'''

CACHE_READ = '''#!/usr/bin/env python3
"""C1 control CACHE-READ - prints the host resolver cache instead of resolving.

Reads $XDG_CACHE_HOME/xdg-terminal-exec (lines 1-10 are hash, cmd, path, id, action, execarg,
appidarg, titlearg, dirarg, holdarg; the rest is the USEP-separated command terminated by
RS+END_OF_EXEC_USEP) and prints from it.  Rejected by clauses f and g because the counter models a
cold cache with XDG_CACHE_HOME in a fresh directory: there is no cache file, so this prints nothing
and exits 1 on every case.  A counter that forgot to isolate XDG_CACHE_HOME would score the host
fixture TARGET_MET here.
"""

import os
import sys

USEP = "\\x1f"
RSEP = "\\x1e"


def cache_path():
    base = os.environ.get("XDG_CACHE_HOME") or os.path.join(
        os.environ.get("HOME", ""), ".cache")
    return os.path.join(base, "xdg-terminal-exec")


def read_cache():
    try:
        with open(cache_path(), "rb") as fh:
            text = fh.read().decode("utf-8", "surrogateescape")
    except OSError:
        return None
    lines = text.split("\\n")
    if text.endswith("\\n"):
        lines = lines[:-1]
    if len(lines) < 11:
        return None
    head = lines[:10]
    body = "\\n".join(lines[10:])
    marker = RSEP + "END_OF_EXEC_USEP"
    if not body.endswith(marker):
        return None
    body = body[:-len(marker)]
    return {"id": head[3], "action": head[4], "path": head[2], "execarg": head[5],
            "appidarg": head[6], "titlearg": head[7], "dirarg": head[8], "holdarg": head[9],
            "tokens": body.split(USEP) if body else []}


def main(argv):
    if argv[:1] == ["--selftest"]:
        sys.stdout.write("MADO_TERMINAL_SELFTEST: 30/30 passed\\n")
        return 0
    cache = read_cache()
    if argv[:1] == ["explain"]:
        if cache is None:
            sys.stdout.write("MADO_TERM: selected=- path=- verdict=NO_TERMINAL\\n")
            return 3
        sys.stdout.write("MADO_TERM: selected=%s path=%s verdict=OK\\n"
                         % (cache["id"], cache["path"]))
        return 0
    if argv[:1] != ["print"]:
        sys.stderr.write("usage: mado-terminal.py print [...]\\n")
        return 2
    if cache is None:
        sys.stderr.write("CACHE-READ: no cache data at %s\\n" % cache_path())
        return 1
    args = argv[1:]
    parts = []
    delim = "\\\\n"
    cmd_delim = "\\\\n"
    want = {"appid": "", "title": "", "dir": "", "hold": False}
    rest = []
    i = 0
    while i < len(args):
        a = args[i]
        i += 1
        if a == "--":
            rest = args[i:]
            break
        if a == "-e":
            rest = args[i:]
            break
        if a.startswith("--app-id="):
            want["appid"] = a.split("=", 1)[1]
        elif a.startswith("--title="):
            want["title"] = a.split("=", 1)[1]
        elif a.startswith("--dir="):
            want["dir"] = a.split("=", 1)[1]
        elif a == "--hold":
            want["hold"] = True
        elif a in ("--print-id", "--print-path", "--print-content", "--print-cmd"):
            parts.append(a[len("--print-"):])
        elif a.startswith("--print-cmd="):
            parts.append("cmd")
            cmd_delim = a.split("=", 1)[1]
        elif a.startswith("--print-delimiter="):
            delim = a.split("=", 1)[1]
        elif a.startswith("-"):
            continue
        else:
            rest = args[i - 1:]
            break
    out = []
    first = True
    name = cache["id"] + ((":" + cache["action"]) if cache["action"] else "")
    if "id" in parts:
        out.append(name)
        first = False
    if "path" in parts:
        if not first:
            out.append(delim.replace("\\\\n", "\\n"))
        out.append(cache["path"])
        first = False
    if "content" in parts:
        first = False
    if "cmd" not in parts:
        if "content" not in parts and delim == "\\\\n":
            out.append("\\n")
        sys.stdout.write("".join(out))
        return 0
    av = []
    if rest and cache["execarg"]:
        av = [cache["execarg"]] + rest
    else:
        av = list(rest)
    if cache["holdarg"] and want["hold"]:
        av = [cache["holdarg"]] + av
    if cache["dirarg"] and want["dir"]:
        if cache["dirarg"].endswith("="):
            av = [cache["dirarg"] + want["dir"]] + av
        else:
            av = [cache["dirarg"], want["dir"]] + av
    if cache["titlearg"] and want["title"]:
        if cache["titlearg"].endswith("="):
            av = [cache["titlearg"] + want["title"]] + av
        else:
            av = [cache["titlearg"], want["title"]] + av
    if cache["appidarg"] and want["appid"]:
        if cache["appidarg"].endswith("="):
            av = [cache["appidarg"] + want["appid"]] + av
        else:
            av = [cache["appidarg"], want["appid"]] + av
    av = list(cache["tokens"]) + av
    if not first:
        out.append(delim.replace("\\\\n", "\\n"))
    sep = cmd_delim.replace("\\\\n", "\\n")
    out.append(sep.join(av))
    if cmd_delim == "\\\\n" or (not first and delim == "\\\\n"):
        out.append("\\n")
    sys.stdout.write("".join(out))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
'''

SELFTEST_LIE = '''#!/usr/bin/env python3
"""C1 control SELFTEST-LIE - prints `MADO_TERMINAL_SELFTEST: 40/40 passed` and tests nothing.

The print side is STUB (exit 0, empty stdout).  Clause s must be satisfied by the *presence and
shape* of the line only if the counter also runs its own fixtures: this control demonstrates that
s alone is worth nothing, and that f/g cannot be replaced by the tool's self-report.
"""

import sys


def main(argv):
    if argv[:1] == ["--selftest"]:
        sys.stdout.write("MADO_TERMINAL_SELFTEST: 40/40 passed\\n")
        return 0
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
'''

FIXTURE_READ = '''#!/usr/bin/env python3
"""C1 control FIXTURE-READ - replays the counter's own fixture answers instead of resolving.

Looks for the counter's fixture JSON at $MADO_FIXTURES, next to this file's repository
(<repo>/quality/counters/c1-r47-fixtures.json) and in the working directory, matches a case by its
`print` arguments (and, when several match, by the environment keys it records), replaces $ROOT in
the recorded stdout and exits with the recorded rc.  Rejected by clause i: the counter's sandbox
must not expose the fixture file to the scored tool; if it does, this control scores TARGET_MET on
every pinned fixture and misses only the nonce cases (clause g).
"""

import json
import os
import sys

CANDIDATES = [
    os.environ.get("MADO_FIXTURES") or "",
    os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                 "quality", "counters", "c1-r47-fixtures.json"),
    os.path.join(os.getcwd(), "quality", "counters", "c1-r47-fixtures.json"),
    "quality/counters/c1-r47-fixtures.json",
]


def load_fixtures():
    for path in CANDIDATES:
        if not path:
            continue
        try:
            with open(path, "rb") as fh:
                data = json.loads(fh.read().decode("utf-8", "surrogateescape"))
        except (OSError, ValueError):
            continue
        if isinstance(data, list):
            return data
    return None


def main(argv):
    if argv[:1] == ["--selftest"]:
        sys.stdout.write("MADO_TERMINAL_SELFTEST: 30/30 passed\\n")
        return 0
    if argv[:1] != ["print"]:
        sys.stderr.write("FIXTURE-READ: only print is modelled\\n")
        return 2
    args = argv[1:]
    fixtures = load_fixtures()
    if fixtures is None:
        sys.stderr.write("FIXTURE-READ: fixtures not readable\\n")
        return 2
    home = os.environ.get("HOME", "")
    root = os.path.dirname(home)
    cands = []
    for fx in fixtures:
        if not isinstance(fx, dict) or fx.get("args") != args:
            continue
        score = 0
        for key, value in (fx.get("env") or {}).items():
            if os.environ.get(key) == value.replace("$ROOT", root):
                score += 1
        cands.append((score, fx))
    if not cands:
        sys.stderr.write("FIXTURE-READ: no fixture for %r\\n" % (args,))
        return 2
    cands.sort(key=lambda kv: -kv[0])
    fx = cands[0][1]
    expect = fx.get("expect") or {}
    sys.stdout.write((expect.get("stdout") or "").replace("$ROOT", root))
    return int(expect.get("rc", 0))


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
'''


def sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 16), b""):
            h.update(chunk)
    return h.hexdigest()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default=os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                                  "c1"))
    ap.add_argument("--base", default=os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                                   "c1-base.py"))
    ap.add_argument("--script", default=PIN)
    args = ap.parse_args()

    with open(args.base, "r", encoding="utf-8") as fh:
        base = fh.read()
    assert 'MODE = "ref"' in base, "c1-base.py must carry the MODE switch"
    os.makedirs(args.out, exist_ok=True)

    written = []
    for name, mode, note in MODES:
        text = base
        text = text.replace(
            'MODE = "ref"',
            '# CONTROL %s: %s\nMODE = %r' % (name, note, mode))
        if name != "REF-MINI":
            text = text.replace(
                '"""mado-terminal.py - which terminal SUPER+RETURN launches, and why (control base).',
                '"""mado-terminal.py - C1 control %s (%s).\n\nDerived from the seat ExecControls base '
                'resolver; this is a CHEAT candidate, not an implementation.' % (name, note))
        path = os.path.join(args.out, name + ".py")
        with open(path, "w", encoding="utf-8") as fh:
            fh.write(text)
        os.chmod(path, 0o755)
        written.append(path)

    script_sha = sha256_file(args.script)
    if script_sha != PIN_SHA:
        sys.stderr.write("build-c1-controls: %s sha256 %s != pin %s\n"
                         % (args.script, script_sha, PIN_SHA))
        return 2
    with open(args.script, "rb") as fh:
        script_b64 = base64.b64encode(fh.read()).decode("ascii")

    tiny = [
        ("STUB", STUB),
        ("CONST", CONST),
        ("DELEGATE", DELEGATE),
        ("SUBPROC", SUBPROC),
        ("CTYPES-EXEC", CTYPES_EXEC),
        ("CACHE-READ", CACHE_READ),
        ("SELFTEST-LIE", SELFTEST_LIE),
        ("FIXTURE-READ", FIXTURE_READ),
        ("EMBED-SH", EMBED_SH.replace("__SCRIPT_B64__", script_b64)
         .replace("__PIN_SHA__", PIN_SHA)),
    ]
    for name, text in tiny:
        path = os.path.join(args.out, name + ".py")
        with open(path, "w", encoding="utf-8") as fh:
            fh.write(text)
        os.chmod(path, 0o755)
        written.append(path)

    for path in written:
        print("%s  %s" % (os.path.basename(path), sha256_file(path)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
