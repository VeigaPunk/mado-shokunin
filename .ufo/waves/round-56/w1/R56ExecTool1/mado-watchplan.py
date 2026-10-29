#!/usr/bin/env python3
"""mado-watchplan: predict the inotify watch list Hyprland 0.56.2 (hyprlang era) registers
for a config tree and join misc:disable_autoreload to a `hyprctl getoption -j` dump.

Read-only, standard library only. Reads only the files named by its arguments and the files
its `source =` lines reach; uses os.stat/os.lstat/os.path.realpath/glob on those paths. It
starts no process, opens no socket and writes nothing (except --selftest, which writes only
inside a private temporary directory it removes).

  python3 -I mado-watchplan.py --config /abs/hyprland.conf [--home /abs/home]
                               [--display-root /abs/dir] [--getoption /abs/dump.json]
  python3 -I mado-watchplan.py --selftest

Exit 0 on a completed run, 2 on a setup failure (stdout `MADO_WATCH: SETUP <reason>`).
"""
import glob
import json
import os
import re
import shutil
import stat
import sys
import tempfile

LIMIT = 1048576
MAX_DEPTH = 16
WS = " \t\r\n\v\f"
OPT = "misc:disable_autoreload"
MASK_FILE = "IN_CLOSE_WRITE|IN_DONT_FOLLOW"
MASK_DIR = "IN_CLOSE_WRITE|IN_DONT_FOLLOW|IN_CREATE|IN_DELETE|IN_MOVED_TO|IN_MOVED_FROM"
MASK_CANON = "IN_CLOSE_WRITE"


class Setup(Exception):
    def __init__(self, reason):
        Exception.__init__(self, reason)
        self.reason = reason


def parse_args(argv):
    """Two-token form only, any order. Returns dict or raises Setup('usage')."""
    allowed = ("--config", "--home", "--display-root", "--getoption")
    got = {}
    if len(argv) % 2 != 0:
        raise Setup("usage")
    for i in range(0, len(argv), 2):
        opt, val = argv[i], argv[i + 1]
        if opt not in allowed or opt in got:
            raise Setup("usage")
        if not val.startswith("/"):
            raise Setup("usage")
        got[opt] = val
    if "--config" not in got:
        raise Setup("usage")
    return got


def read_limited(path):
    """Return decoded text of a file; Setup('too_large') above LIMIT bytes; OSError otherwise."""
    with open(path, "rb") as fh:
        data = fh.read(LIMIT + 1)
    if len(data) > LIMIT:
        raise Setup("too_large")
    return data.decode("utf-8", errors="replace")


def absolute_path(raw, cur):
    """legacy absolutePath(RAW, cur) with --home already substituted by the caller for `~`."""
    if raw[0] == "/":
        return raw
    i = cur.rfind("/")
    curdir = cur if i < 0 else cur[:i]
    if raw[0] == ".":
        if raw.startswith("../"):
            j = curdir.rfind("/")
            parent = curdir if j < 0 else curdir[:j]
            return parent + raw[2:]
        if raw.startswith("./"):
            return curdir + raw[1:]
        return curdir + "/" + raw
    return curdir + "/" + raw


def parse_value(text):
    """hyprlang configStringToInt subset: returns int or None (unsupported)."""
    if text.startswith(("true", "on", "yes")):
        return 1
    if text.startswith(("false", "off", "no")):
        return 0
    if re.fullmatch(r"[0-9]+", text):
        return int(text)
    return None


class Plan:
    def __init__(self, home):
        self.home = home
        self.paths = []      # (path, via)
        self.events = []     # (kind, via, extra...)
        self.unsupported = 0
        self.errors = 0
        self.value = None    # last accepted disable_autoreload value
        self.display = lambda p: p

    def parse_file(self, cur, depth):
        text = read_limited(cur)
        stack = []
        for lineno, raw_line in enumerate(text.split("\n"), 1):
            line = raw_line.strip(WS)
            if not line or line[0] == "#":
                continue
            if "=" not in line:
                if line == "}":
                    if stack:
                        stack.pop()
                elif line.endswith("{"):
                    stack.append(line[:-1].strip(WS))
                continue
            lhs, rhs = line.split("=", 1)
            lhs = lhs.strip(WS)
            rhs = rhs.strip(WS)
            if lhs == "source":
                if stack:
                    self.unsupported += 1
                    continue
                raw = rhs.split("#", 1)[0].strip(WS)
                self.handle_source(raw, cur, lineno, depth)
                continue
            if lhs.startswith("$"):
                continue
            key = ":".join(stack) + ":" + lhs if stack else lhs
            if key != OPT:
                continue
            if "$" in line or "{" in line or "\\" in line or "##" in rhs:
                self.unsupported += 1
                continue
            value = parse_value(rhs.split("#", 1)[0].strip(WS))
            if value is None:
                self.unsupported += 1
                continue
            self.value = value

    def handle_source(self, raw, cur, lineno, depth):
        via = "%s:%d" % (self.display(cur), lineno)
        if len(raw) < 2:
            self.event("ERROR", via, raw, "bogus")
            return
        if (raw[0] == "~" and self.home is None) or "\\" in raw:
            self.unsupported += 1
            return
        if raw[0] == "~":
            value = self.home + raw[1:]
        else:
            value = absolute_path(raw, cur)
        try:
            matches = sorted(glob.glob(value))
        except (OSError, ValueError):
            matches = []
        if not matches:
            self.event("ERROR", via, raw, "nomatch")
            return
        for m in matches:
            v = absolute_path(m, cur) if m else m
            try:
                st = os.stat(v)
            except (OSError, ValueError):
                self.event("ERROR", via, raw, "inaccessible")
                return
            if stat.S_ISREG(st.st_mode):
                self.paths.append((v, via))
                if depth + 1 > MAX_DEPTH:
                    self.unsupported += 1
                    continue
                try:
                    self.parse_file(v, depth + 1)
                except Setup:
                    raise
                except (OSError, ValueError):
                    pass  # listed, not parsed
            elif stat.S_ISDIR(st.st_mode):
                self.event("SKIP", via, v, "directory")
            else:
                self.event("SKIP", via, v, "nonregular")

    def event(self, kind, via, extra, reason):
        if kind == "ERROR":
            self.errors += 1
        self.events.append((kind, via, extra, reason))


def make_display(root):
    if root is None:
        return lambda p: p
    given = root[:-1] if root.endswith("/") else root
    cands = [given]
    try:
        real = os.path.realpath(root)
    except (OSError, ValueError):
        real = given
    if real not in cands:
        cands.append(real)

    def display(p):
        for d in cands:
            if p == d or p.startswith(d + "/"):
                return "$ROOT" + p[len(d):]
        return p
    return display


def load_getoption(path):
    """Return live int or None. Setup unreadable / too_large / bad_json."""
    try:
        if not os.path.isfile(path):
            raise Setup("unreadable")
        text = read_limited(path)
    except Setup:
        raise
    except (OSError, ValueError):
        raise Setup("unreadable")
    live = None
    for line in text.split("\n"):
        line = line.strip(WS)
        if not line:
            continue
        try:
            obj = json.loads(line)
        except (ValueError, RecursionError):
            raise Setup("bad_json")
        if not isinstance(obj, dict):
            raise Setup("bad_json")
        name = obj.get("option")
        num = obj.get("int")
        if isinstance(name, str) and isinstance(num, int) and not isinstance(num, bool):
            if name == OPT:
                live = num
    return live


def run(argv):
    """Pure core: returns (exit code, stdout text)."""
    try:
        args = parse_args(argv)
        live = None
        have_live = "--getoption" in args
        if have_live:
            live = load_getoption(args["--getoption"])
        config = args["--config"]
        plan = Plan(args.get("--home"))
        plan.display = make_display(args.get("--display-root"))
        plan.paths.append((config, "main"))
        if os.path.isfile(config):
            try:
                plan.parse_file(config, 0)
            except Setup:
                raise
            except (OSError, ValueError):
                pass
    except Setup as exc:
        return 2, "MADO_WATCH: SETUP %s\n" % exc.reason

    disp = plan.display
    off = plan.value is not None and plan.value != 0
    out = []
    out.append("MADO_WATCH: config=%s autoreload=%s disable_autoreload=%s paths=%d unsupported=%d errors=%d" % (
        disp(config), "off" if off else "on",
        "unset" if plan.value is None else str(plan.value),
        len(plan.paths), plan.unsupported, plan.errors))
    for kind, via, extra, reason in plan.events:
        if kind == "ERROR":
            out.append("MADO_WATCH: ERROR via=%s source=%s reason=%s" % (via, extra, reason))
        else:
            out.append("MADO_WATCH: SKIP via=%s path=%s reason=%s" % (via, disp(extra), reason))
    n = 0
    if not off:
        for path, via in plan.paths:
            try:
                is_dir = os.path.isdir(path)
                exists = os.path.lexists(path)
            except ValueError:
                is_dir, exists = False, False
            if is_dir:
                typ, mask = "dir", MASK_DIR
            elif exists:
                typ, mask = "file", MASK_FILE
            else:
                typ, mask = "missing", MASK_FILE
            n += 1
            out.append("MADO_WATCH: n=%d role=primary path=%s type=%s mask=%s via=%s" % (
                n, disp(path), typ, mask, via))
            try:
                if os.path.islink(path):
                    real = os.path.realpath(path, strict=True)
                    n += 1
                    out.append("MADO_WATCH: n=%d role=canonical path=%s type=file mask=%s via=%s" % (
                        n, disp(real), MASK_CANON, via))
            except (OSError, ValueError):
                pass
    verdict = "NONE"
    if have_live:
        cfg = 1 if (plan.value is not None and plan.value != 0) else 0
        if live is None:
            verdict = "UNKNOWN"
            out.append("MADO_WATCH_LIVE: option=%s config=%d live=? verdict=UNKNOWN" % (OPT, cfg))
        else:
            verdict = "AGREE" if live == cfg else "DIFFER"
            out.append("MADO_WATCH_LIVE: option=%s config=%d live=%d verdict=%s" % (OPT, cfg, live, verdict))
    out.append("MADO_WATCH: DONE watches=%d unsupported=%d errors=%d live=%s" % (
        n, plan.unsupported, plan.errors, verdict))
    return 0, "\n".join(out) + "\n"


def selftest():
    checks = []

    def check(name, cond):
        checks.append((name, bool(cond)))

    # pure helpers
    check("abs-abs", absolute_path("/x/y", "/a/b.conf") == "/x/y")
    check("abs-bare", absolute_path("c.conf", "/a/b.conf") == "/a/c.conf")
    check("abs-dot", absolute_path("./c.conf", "/a/b.conf") == "/a/c.conf")
    check("abs-up", absolute_path("../c.conf", "/a/s/b.conf") == "/a/c.conf")
    check("abs-hidden", absolute_path(".h", "/a/b.conf") == "/a/.h")
    check("abs-dotdot-x", absolute_path("..x", "/a/b.conf") == "/a/..x")
    check("abs-rootcur", absolute_path("c", "/b.conf") == "/c")
    check("abs-nosl", absolute_path("../c", "b.conf") == "b.conf/c")
    check("val-true", parse_value("trueish") == 1)
    check("val-on", parse_value("on") == 1)
    check("val-yes", parse_value("yes") == 1)
    check("val-false", parse_value("false") == 0)
    check("val-no", parse_value("nothing") == 0)
    check("val-int", parse_value("007") == 7)
    check("val-bad", parse_value("maybe") is None and parse_value("") is None and parse_value("-1") is None)
    check("args-ok", parse_args(["--config", "/a"]) == {"--config": "/a"})
    for name, bad in (("args-empty", []), ("args-rel", ["--config", "a"]),
                      ("args-dup", ["--config", "/a", "--config", "/b"]),
                      ("args-unknown", ["--config", "/a", "--x", "/b"]),
                      ("args-noval", ["--config", "/a", "--home"]),
                      ("args-nocfg", ["--home", "/a"])):
        try:
            parse_args(bad)
            check(name, False)
        except Setup as exc:
            check(name, exc.reason == "usage")
    d = make_display("/r/s/")
    check("disp-eq", d("/r/s") == "$ROOT")
    check("disp-sub", d("/r/s/t") == "$ROOT/t")
    check("disp-prefix-only", d("/r/sx") == "/r/sx")

    tmp = tempfile.mkdtemp(prefix="mado-watchplan-selftest-")
    try:
        def w(rel, text):
            p = os.path.join(tmp, rel)
            os.makedirs(os.path.dirname(p), exist_ok=True)
            with open(p, "w") as fh:
                fh.write(text)
            return p

        main = w("t/hyprland.conf", "misc {\n disable_autoreload = no\n}\nsource = a.conf\nsource = sub/*.conf\n")
        w("t/a.conf", "x = 1\n")
        w("t/sub/b.conf", "")
        w("t/sub/c.conf", "")
        rc, out = run(["--config", main, "--display-root", tmp])
        lines = out.splitlines()
        check("run-rc", rc == 0)
        check("run-header", lines[0] == "MADO_WATCH: config=$ROOT/t/hyprland.conf autoreload=on disable_autoreload=0 paths=4 unsupported=0 errors=0")
        check("run-watch-count", out.count("role=primary") == 4)
        check("run-done", lines[-1] == "MADO_WATCH: DONE watches=4 unsupported=0 errors=0 live=NONE")

        os.symlink("a.conf", os.path.join(tmp, "t/l.conf"))
        w("t/h2.conf", "source = l.conf\n")
        rc, out = run(["--config", os.path.join(tmp, "t/h2.conf"), "--display-root", tmp])
        check("symlink-canonical", "role=canonical path=$ROOT/t/a.conf type=file mask=IN_CLOSE_WRITE via=$ROOT/t/h2.conf:1" in out)

        w("t/off.conf", "misc:disable_autoreload = 1\n")
        w("t/go.json", '{"option": "misc:disable_autoreload", "int": 0}\n')
        rc, out = run(["--config", os.path.join(tmp, "t/off.conf"), "--getoption", os.path.join(tmp, "t/go.json")])
        check("live-differ", rc == 0 and "live=0 verdict=DIFFER" in out and "watches=0" in out)

        w("t/bad.json", "[1]\n")
        rc, out = run(["--config", main, "--getoption", os.path.join(tmp, "t/bad.json")])
        check("bad-json", (rc, out) == (2, "MADO_WATCH: SETUP bad_json\n"))
        rc, out = run(["--config", main, "--getoption", os.path.join(tmp, "t/none.json")])
        check("unreadable", (rc, out) == (2, "MADO_WATCH: SETUP unreadable\n"))
        rc, out = run(["--config", main, "--getoption", os.path.join(tmp, "t")])
        check("unreadable-dir", (rc, out) == (2, "MADO_WATCH: SETUP unreadable\n"))
        big = os.path.join(tmp, "t/big.conf")
        with open(big, "wb") as fh:
            fh.write(b"#" * (LIMIT + 1))
        rc, out = run(["--config", big])
        check("too-large", (rc, out) == (2, "MADO_WATCH: SETUP too_large\n"))
        rc, out = run(["--config", os.path.join(tmp, "t/missing.conf")])
        check("missing-config", rc == 0 and "type=missing" in out)
        w("t/loop.conf", "source = loop.conf\n")
        rc, out = run(["--config", os.path.join(tmp, "t/loop.conf")])
        check("depth-cap", rc == 0 and "paths=18 unsupported=1 errors=0" in out)
        check("usage-out", run([]) == (2, "MADO_WATCH: SETUP usage\n"))
    finally:
        shutil.rmtree(tmp, ignore_errors=True)

    ok = sum(1 for _, c in checks if c)
    for name, c in checks:
        if not c:
            sys.stdout.write("MADO_WATCH_SELFTEST: FAIL %s\n" % name)
    sys.stdout.write("MADO_WATCH_SELFTEST: %d/%d assertions passed\n" % (ok, len(checks)))
    return 0 if ok == len(checks) else 1


def main(argv):
    if argv == ["--selftest"]:
        return selftest()
    rc, text = run(argv)
    sys.stdout.buffer.write(text.encode("utf-8", errors="surrogateescape"))
    sys.stdout.flush()
    return rc


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
