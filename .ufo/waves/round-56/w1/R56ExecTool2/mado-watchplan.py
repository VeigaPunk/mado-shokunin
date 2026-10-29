#!/usr/bin/env python3
"""mado-watchplan: predict the inotify watch list Hyprland 0.56.2 (hyprlang config
provider) registers for a config tree, and join misc:disable_autoreload to a
`hyprctl getoption` dump.

Read-only, standard library only. It reads the files named by its arguments and the
files their `source =` lines reach (plus os.stat/lstat/realpath/glob on those paths);
it starts no process, opens no socket and writes nothing (--selftest writes only under
a private temporary directory that it removes).

Usage:
  python3 -I mado-watchplan.py --config ABS [--home ABS] [--display-root ABS] [--getoption ABS]
  python3 -I mado-watchplan.py --selftest

Exit: 0 completed run, 2 setup failure (stdout `MADO_WATCH: SETUP <reason>`).
"""
import glob
import json
import os
import re
import stat
import sys

MAX_BYTES = 1048576
MAX_DEPTH = 16
STRIP = " \t\r\n\v\f"
MASK_FILE = "IN_CLOSE_WRITE|IN_DONT_FOLLOW"
MASK_DIR = "IN_CLOSE_WRITE|IN_DONT_FOLLOW|IN_CREATE|IN_DELETE|IN_MOVED_TO|IN_MOVED_FROM"
MASK_CANON = "IN_CLOSE_WRITE"
DIGITS = re.compile(r"[0-9]+")


class Setup(Exception):
    def __init__(self, reason):
        Exception.__init__(self, reason)
        self.reason = reason


# --------------------------------------------------------------------------- arguments
def parse_args(argv):
    """Two-token form only, any order. Returns dict of option -> value."""
    allowed = ("--config", "--home", "--display-root", "--getoption")
    got = {}
    i = 0
    n = len(argv)
    while i < n:
        tok = argv[i]
        if tok not in allowed or i + 1 >= n or tok in got:
            raise Setup("usage")
        val = argv[i + 1]
        if not val.startswith("/"):
            raise Setup("usage")
        got[tok] = val
        i += 2
    if "--config" not in got:
        raise Setup("usage")
    return got


# --------------------------------------------------------------------------- file reading
def read_limited(path):
    """Return decoded text of a regular file; raise Setup(too_large) over the cap,
    OSError when it cannot be read."""
    st = os.stat(path)
    if st.st_size > MAX_BYTES:
        raise Setup("too_large")
    with open(path, "rb") as fh:
        data = fh.read(MAX_BYTES + 1)
    if len(data) > MAX_BYTES:
        raise Setup("too_large")
    return data.decode("utf-8", errors="replace")


# --------------------------------------------------------------------------- hyprlang pieces
def config_string_to_int(value):
    """hyprlang configStringToInt subset: returns int or None (unsupported)."""
    if value.startswith("true") or value.startswith("on") or value.startswith("yes"):
        return 1
    if value.startswith("false") or value.startswith("off") or value.startswith("no"):
        return 0
    if DIGITS.fullmatch(value):
        return int(value)
    return None


def absolute_path(raw, cur, home):
    """Hyprland absolutePath (fetch/Hyprland-MiscFunctions.cpp:61-83) as registered."""
    if raw[0] == "~":
        return home + raw[1:]
    if raw[0] == "/":
        return raw
    i = cur.rfind("/")
    curdir = cur[:i] if i >= 0 else cur
    if raw[0] == ".":
        if raw.startswith("../"):
            j = curdir.rfind("/")
            parent = curdir[:j] if j >= 0 else curdir
            return parent + raw[2:]
        if raw.startswith("./"):
            return curdir + raw[1:]
        return curdir + "/" + raw
    return curdir + "/" + raw


def glob_sorted(value):
    try:
        found = glob.glob(value)
    except (ValueError, OSError):
        return []
    return sorted(found, key=os.fsencode)


# --------------------------------------------------------------------------- the model
class Plan:
    def __init__(self, config, home, display_root):
        self.config = config
        self.home = home
        self.paths = []          # (path, via)
        self.events = []         # (kind, via_raw_cur, line, extra...) rendered later
        self.unsupported = 0
        self.errors = 0
        self.value = None        # last accepted misc:disable_autoreload
        self.prefixes = []
        if display_root is not None:
            given = display_root[:-1] if display_root.endswith("/") else display_root
            self.prefixes.append(given)
            real = os.path.realpath(display_root)
            if real != given:
                self.prefixes.append(real)

    def display(self, path):
        for pre in self.prefixes:
            if path == pre or path.startswith(pre + "/"):
                return "$ROOT" + path[len(pre):]
        return path

    def via(self, cur, lineno):
        return "%s:%d" % (self.display(cur), lineno)

    def parse_file(self, path, depth):
        try:
            text = read_limited(path)
        except Setup:
            raise
        except (OSError, ValueError):
            return  # listed, not parsed
        stack = []
        for lineno, raw_line in enumerate(text.split("\n"), 1):
            line = raw_line.strip(STRIP)
            if not line or line[0] == "#":
                continue
            eq = line.find("=")
            if eq < 0:
                if line == "}":
                    if stack:
                        stack.pop()
                elif line.endswith("{"):
                    stack.append(line[:-1].strip(STRIP))
                continue
            lhs = line[:eq].strip(STRIP)
            rhs = line[eq + 1:].strip(STRIP)
            if lhs == "source":
                if stack:
                    self.unsupported += 1
                    continue
                src = rhs.split("#", 1)[0].strip(STRIP)
                self.handle_source(src, path, lineno, depth)
                continue
            if lhs.startswith("$"):
                continue
            key = ":".join(stack) + ":" + lhs if stack else lhs
            if key != "misc:disable_autoreload":
                continue
            if "$" in line or "{" in line or "\\" in line or "##" in rhs:
                self.unsupported += 1
                continue
            val = config_string_to_int(rhs.split("#", 1)[0].strip(STRIP))
            if val is None:
                self.unsupported += 1
                continue
            self.value = val

    def handle_source(self, raw, cur, lineno, depth):
        via = self.via(cur, lineno)
        if len(raw) < 2:
            self.events.append("MADO_WATCH: ERROR via=%s source=%s reason=bogus" % (via, raw))
            self.errors += 1
            return
        if (raw[0] == "~" and self.home is None) or "\\" in raw:
            self.unsupported += 1
            return
        value = absolute_path(raw, cur, self.home)
        matches = glob_sorted(value)
        if not matches:
            self.events.append("MADO_WATCH: ERROR via=%s source=%s reason=nomatch" % (via, raw))
            self.errors += 1
            return
        for m in matches:
            v = absolute_path(m, cur, self.home) if m else m
            try:
                st = os.stat(v)
            except (OSError, ValueError):
                self.events.append("MADO_WATCH: ERROR via=%s source=%s reason=inaccessible" % (via, raw))
                self.errors += 1
                return
            if stat.S_ISREG(st.st_mode):
                self.paths.append((v, via))
                if depth + 1 > MAX_DEPTH:
                    self.unsupported += 1
                else:
                    self.parse_file(v, depth + 1)
            elif stat.S_ISDIR(st.st_mode):
                self.events.append("MADO_WATCH: SKIP via=%s path=%s reason=directory" % (via, self.display(v)))
            else:
                self.events.append("MADO_WATCH: SKIP via=%s path=%s reason=nonregular" % (via, self.display(v)))


def watch_entries(plan):
    """Yield (role, path, type, mask, via) for the primary list and canonical follow-ups."""
    if plan.value:  # non-zero -> watch list empty
        return []
    out = []
    for path, via in plan.paths:
        if os.path.isdir(path):
            typ, mask = "dir", MASK_DIR
        elif os.path.lexists(path):
            typ, mask = "file", MASK_FILE
        else:
            typ, mask = "missing", MASK_FILE
        out.append(("primary", path, typ, mask, via))
        if os.path.islink(path):
            try:
                real = os.path.realpath(path, strict=True)
            except (OSError, ValueError):
                real = None
            if real is not None:
                out.append(("canonical", real, "file", MASK_CANON, via))
    return out


def parse_getoption(text):
    """Return live int or None; raise Setup(bad_json)."""
    live = None
    for line in text.split("\n"):
        s = line.strip(STRIP)
        if not s:
            continue
        try:
            obj = json.loads(s)
        except (ValueError, RecursionError):
            raise Setup("bad_json")
        if not isinstance(obj, dict):
            raise Setup("bad_json")
        opt = obj.get("option")
        iv = obj.get("int")
        if isinstance(opt, str) and isinstance(iv, int) and not isinstance(iv, bool):
            live = iv
    return live


def run(argv):
    """Return (stdout_bytes, exit_code)."""
    try:
        out = _run(argv)
        return out.encode("utf-8", "surrogateescape"), 0
    except Setup as e:
        return ("MADO_WATCH: SETUP %s\n" % e.reason).encode(), 2


def _run(argv):
    args = parse_args(argv)
    config = args["--config"]
    go_text = None
    if "--getoption" in args:
        gp = args["--getoption"]
        try:
            if not stat.S_ISREG(os.stat(gp).st_mode):
                raise Setup("unreadable")
            go_text = read_limited(gp)
        except Setup:
            raise
        except (OSError, ValueError):
            raise Setup("unreadable")
    plan = Plan(config, args.get("--home"), args.get("--display-root"))
    plan.paths.append((config, "main"))
    try:
        is_reg = stat.S_ISREG(os.stat(config).st_mode)
    except (OSError, ValueError):
        is_reg = False
    if is_reg:
        plan.parse_file(config, 0)
    live = parse_getoption(go_text) if go_text is not None else None

    lines = []
    watches = watch_entries(plan)
    lines.append("MADO_WATCH: config=%s autoreload=%s disable_autoreload=%s paths=%d unsupported=%d errors=%d" % (
        plan.display(config), "off" if plan.value else "on",
        "unset" if plan.value is None else str(plan.value), len(plan.paths), plan.unsupported, plan.errors))
    lines.extend(plan.events)
    for k, (role, path, typ, mask, via) in enumerate(watches, 1):
        lines.append("MADO_WATCH: n=%d role=%s path=%s type=%s mask=%s via=%s" % (
            k, role, plan.display(path), typ, mask, via))
    verdict = "NONE"
    if go_text is not None:
        cfg = 1 if plan.value else 0
        if live is None:
            verdict = "UNKNOWN"
        else:
            verdict = "AGREE" if live == cfg else "DIFFER"
        lines.append("MADO_WATCH_LIVE: option=misc:disable_autoreload config=%d live=%s verdict=%s" % (
            cfg, "?" if live is None else str(live), verdict))
    lines.append("MADO_WATCH: DONE watches=%d unsupported=%d errors=%d live=%s" % (
        len(watches), plan.unsupported, plan.errors, verdict))
    return "\n".join(lines) + "\n"


# --------------------------------------------------------------------------- selftest
def selftest():
    import shutil
    import tempfile
    results = []

    def check(name, cond):
        results.append((name, bool(cond)))

    tmp = tempfile.mkdtemp(prefix="mado-watchplan-selftest-")
    try:
        root = os.path.realpath(tmp)

        def w(rel, text="", mode="w"):
            p = os.path.join(root, rel)
            os.makedirs(os.path.dirname(p), exist_ok=True)
            with open(p, mode) as fh:
                fh.write(text)
            return p

        def go(*argv):
            out, rc = run(list(argv))
            return out.decode("utf-8", "surrogateescape"), rc

        # pure functions
        check("int true", config_string_to_int("true") == 1)
        check("int yes-ish prefix", config_string_to_int("yesterday") == 1)
        check("int off", config_string_to_int("off") == 0)
        check("int no-ish prefix", config_string_to_int("nope") == 0)
        check("int digits", config_string_to_int("07") == 7)
        check("int bad", config_string_to_int("-1") is None and config_string_to_int("") is None
              and config_string_to_int("2x") is None)
        check("abs tilde", absolute_path("~/a", "/c/m.conf", "/h") == "/h/a")
        check("abs absolute", absolute_path("/a/b", "/c/m.conf", "/h") == "/a/b")
        check("abs ./", absolute_path("./a", "/c/d/m.conf", None) == "/c/d/a")
        check("abs ../", absolute_path("../a", "/c/d/m.conf", None) == "/c/a")
        check("abs bare", absolute_path("a", "/c/d/m.conf", None) == "/c/d/a")
        check("abs dot-leading", absolute_path(".h", "/c/d/m.conf", None) == "/c/d/.h"
              and absolute_path("..x", "/c/d/m.conf", None) == "/c/d/..x")
        check("abs no slash cur", absolute_path("a", "m.conf", None) == "m.conf/a")

        # arguments
        for name, argv in (
            ("usage empty", []),
            ("usage relative config", ["--config", "rel"]),
            ("usage repeated", ["--config", "/a", "--config", "/a"]),
            ("usage unknown", ["--config", "/a", "--x", "/b"]),
            ("usage no value", ["--config", "/a", "--home"]),
            ("usage selftest mixed", ["--config", "/a", "--selftest"]),
            ("usage relative home", ["--config", "/a", "--home", "h"]),
        ):
            check(name, go(*argv) == ("MADO_WATCH: SETUP usage\n", 2))

        # basic tree
        w("t/hyprland.conf", "source = ./a.conf\nsource = sub/*.conf\nmisc {\n  disable_autoreload = no # x\n}\n")
        w("t/a.conf", "")
        w("t/sub/b.conf", "")
        w("t/sub/c.conf", "")
        os.symlink("a.conf", os.path.join(root, "t/link.conf"))
        cfg = os.path.join(root, "t/hyprland.conf")
        out, rc = go("--config", cfg, "--display-root", root)
        lines = out.splitlines()
        check("tree rc", rc == 0)
        check("tree header", lines[0] == "MADO_WATCH: config=$ROOT/t/hyprland.conf autoreload=on "
              "disable_autoreload=0 paths=4 unsupported=0 errors=0")
        check("tree order", [l.split(" path=")[1].split(" ")[0] for l in lines[1:5]] ==
              ["$ROOT/t/hyprland.conf", "$ROOT/t/a.conf", "$ROOT/t/sub/b.conf", "$ROOT/t/sub/c.conf"])
        check("tree done", lines[-1] == "MADO_WATCH: DONE watches=4 unsupported=0 errors=0 live=NONE")

        # symlink canonical + category value
        w("s/hyprland.conf", "source = ../t/link.conf\nmisc:disable_autoreload = 3\n")
        out, rc = go("--config", os.path.join(root, "s/hyprland.conf"), "--display-root", root)
        lines = out.splitlines()
        check("canonical watch", any(" role=canonical path=$ROOT/t/a.conf type=file mask=IN_CLOSE_WRITE via=" in l
                                     for l in lines) is False)  # disable=3 -> empty list
        check("disable nonzero empties", lines[0].find("autoreload=off disable_autoreload=3 paths=2") > 0
              and lines[-1] == "MADO_WATCH: DONE watches=0 unsupported=0 errors=0 live=NONE")
        w("s/hyprland.conf", "source = ../t/link.conf\n")
        out, rc = go("--config", os.path.join(root, "s/hyprland.conf"), "--display-root", root)
        check("canonical watch present", " n=3 role=canonical path=$ROOT/t/a.conf type=file mask=IN_CLOSE_WRITE via=$ROOT/s/hyprland.conf:1" in out)

        # errors and unsupported
        w("e/hyprland.conf", "source = x\nsource = none/*.conf\nsource = ~/a\nsource = a\\b\n"
          "cat {\nsource = a.conf\n}\nmisc:disable_autoreload = $x\n")
        out, rc = go("--config", os.path.join(root, "e/hyprland.conf"), "--display-root", root)
        check("bogus+nomatch events", "source=x reason=bogus" in out and "source=none/*.conf reason=nomatch" in out)
        check("unsupported counted", "paths=1 unsupported=4 errors=2" in out)

        # getoption
        w("g/ok.json", '{"option": "misc:disable_autoreload", "int": 0, "set": false}\n')
        w("g/bad.json", '{\n"option": 1\n}\n')
        w("g/unk.json", '{"option": "x"}\n{"int": 1}\n{"option": "x", "int": 1.5}\n')
        w("g/bool.json", '{"option": "misc:disable_autoreload", "int": true}\n')
        out, rc = go("--config", cfg, "--getoption", os.path.join(root, "g/ok.json"))
        check("live AGREE", "live=0 verdict=AGREE" in out and out.endswith("live=AGREE\n") and rc == 0)
        out, rc = go("--config", cfg, "--getoption", os.path.join(root, "g/unk.json"))
        check("live other option ignored", "live=? verdict=UNKNOWN" in out)
        out, rc = go("--config", cfg, "--getoption", os.path.join(root, "g/bool.json"))
        check("live bool ignored", "live=? verdict=UNKNOWN" in out)
        check("bad_json", go("--config", cfg, "--getoption", os.path.join(root, "g/bad.json")) ==
              ("MADO_WATCH: SETUP bad_json\n", 2))
        check("unreadable missing", go("--config", cfg, "--getoption", os.path.join(root, "g/none.json")) ==
              ("MADO_WATCH: SETUP unreadable\n", 2))
        check("unreadable dir", go("--config", cfg, "--getoption", os.path.join(root, "g")) ==
              ("MADO_WATCH: SETUP unreadable\n", 2))
        w("g/big.json", "x" * (MAX_BYTES + 1))
        check("too_large getoption", go("--config", cfg, "--getoption", os.path.join(root, "g/big.json")) ==
              ("MADO_WATCH: SETUP too_large\n", 2))
        w("big/hyprland.conf", "#" * (MAX_BYTES + 1))
        check("too_large config", go("--config", os.path.join(root, "big/hyprland.conf")) ==
              ("MADO_WATCH: SETUP too_large\n", 2))

        # missing config, depth cap
        out, rc = go("--config", os.path.join(root, "nope/hyprland.conf"), "--display-root", root)
        check("missing config listed", rc == 0 and "type=missing" in out and "paths=1" in out)
        w("r/hyprland.conf", "source = ./loop.conf\n")
        w("r/loop.conf", "source = ./loop.conf\n")
        out, rc = go("--config", os.path.join(root, "r/hyprland.conf"), "--display-root", root)
        check("depth cap", "paths=18 unsupported=1 errors=0" in out)
    finally:
        shutil.rmtree(tmp, ignore_errors=True)
    passed = sum(1 for _, ok in results if ok)
    for name, ok in results:
        if not ok:
            sys.stdout.write("MADO_WATCH_SELFTEST: FAIL %s\n" % name)
    sys.stdout.write("MADO_WATCH_SELFTEST: %d/%d assertions passed\n" % (passed, len(results)))
    return 0 if passed == len(results) else 1


def main(argv):
    if argv == ["--selftest"]:
        return selftest()
    out, rc = run(argv)
    sys.stdout.buffer.write(out)
    sys.stdout.buffer.flush()
    return rc


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
