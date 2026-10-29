#!/usr/bin/env python3
"""mado-watchplan: predict the inotify watch list Hyprland 0.56.2 (hyprlang era)
registers for a config tree and join misc:disable_autoreload to a `hyprctl
getoption` dump.

Read-only, standard library only.  Reads only the files named by its
arguments and the files `source =` lines reach; starts no process, opens no
socket, writes nothing (`--selftest` writes only inside a private temporary
directory that it removes).

  python3 -I mado-watchplan.py --config /abs/hyprland.conf [--home /abs/home]
                               [--display-root /abs/dir] [--getoption /abs/file]
  python3 -I mado-watchplan.py --selftest

Exit 0 on a completed run, 2 on a setup failure (`MADO_WATCH: SETUP <reason>`).
"""
import glob
import json
import os
import re
import stat
import sys

MAX_BYTES = 1048576
MAX_DEPTH = 16
OPTION = "misc:disable_autoreload"
STRIP = " \t\r\n\v\f"
MASK_FILE = "IN_CLOSE_WRITE|IN_DONT_FOLLOW"
MASK_DIR = "IN_CLOSE_WRITE|IN_DONT_FOLLOW|IN_CREATE|IN_DELETE|IN_MOVED_TO|IN_MOVED_FROM"
MASK_CANON = "IN_CLOSE_WRITE"


class Setup(Exception):
    def __init__(self, reason):
        Exception.__init__(self, reason)
        self.reason = reason


# --------------------------------------------------------------------------
# data model: path list, event list, counters
# --------------------------------------------------------------------------
class Plan:
    def __init__(self, home):
        self.home = home          # str or None
        self.paths = []           # [(path, via)] in processing order; via is a display string
        self.events = []          # [(kind, via, a, b)] kind ERROR|SKIP; processing order
        self.unsupported = 0
        self.errors = 0
        self.value = None         # last accepted misc:disable_autoreload value (int) or None
        self.display = lambda p: p


# --------------------------------------------------------------------------
# helpers
# --------------------------------------------------------------------------
def read_limited(path):
    """bytes of a file; Setup('too_large') beyond MAX_BYTES; OSError when unreadable."""
    with open(path, "rb") as fh:
        data = fh.read(MAX_BYTES + 1)
    if len(data) > MAX_BYTES:
        raise Setup("too_large")
    return data


def config_string_to_int(text):
    """hyprlang configStringToInt subset; None when unsupported."""
    if text.startswith("true") or text.startswith("on") or text.startswith("yes"):
        return 1
    if text.startswith("false") or text.startswith("off") or text.startswith("no"):
        return 0
    if re.fullmatch(r"[0-9]+", text):
        return int(text)
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


# --------------------------------------------------------------------------
# parser
# --------------------------------------------------------------------------
def parse_text(plan, text, cur, depth):
    stack = []
    lines = text.split("\n")
    for idx, rawline in enumerate(lines):
        lineno = idx + 1
        line = rawline.strip(STRIP)
        if line == "" or line[0] == "#":
            continue
        if "=" not in line:
            if line == "}":
                if stack:
                    stack.pop()
            elif line.endswith("{"):
                stack.append(line[:-1].strip(STRIP))
            continue
        lhs, rhs = line.split("=", 1)
        lhs = lhs.strip(STRIP)
        rhs = rhs.strip(STRIP)
        if lhs == "source":
            if stack:
                plan.unsupported += 1
                continue
            raw = rhs.split("#", 1)[0].strip(STRIP)
            handle_source(plan, raw, cur, depth, lineno)
            continue
        if lhs.startswith("$"):
            continue
        key = ":".join(stack) + ":" + lhs if stack else lhs
        if key != OPTION:
            continue
        if "$" in line or "{" in line or "\\" in line or "##" in rhs:
            plan.unsupported += 1
            continue
        value = config_string_to_int(rhs.split("#", 1)[0].strip(STRIP))
        if value is None:
            plan.unsupported += 1
            continue
        plan.value = value


def handle_source(plan, raw, cur, depth, lineno):
    via = "%s:%d" % (plan.display(cur), lineno)
    if len(raw) < 2:
        plan.events.append(("ERROR", via, raw, "bogus"))
        plan.errors += 1
        return
    if (raw[0] == "~" and plan.home is None) or "\\" in raw:
        plan.unsupported += 1
        return
    value = absolute_path(raw, cur, plan.home)
    matches = sorted(glob.glob(value))
    if not matches:
        plan.events.append(("ERROR", via, raw, "nomatch"))
        plan.errors += 1
        return
    for m in matches:
        v = absolute_path(m, cur, plan.home)
        try:
            st = os.stat(v)
        except OSError:
            plan.events.append(("ERROR", via, raw, "inaccessible"))
            plan.errors += 1
            return
        if stat.S_ISREG(st.st_mode):
            plan.paths.append((v, via))
            if depth + 1 > MAX_DEPTH:
                plan.unsupported += 1
            else:
                parse_file(plan, v, depth + 1)
        elif stat.S_ISDIR(st.st_mode):
            plan.events.append(("SKIP", via, v, "directory"))
        else:
            plan.events.append(("SKIP", via, v, "nonregular"))


def parse_file(plan, path, depth):
    """Parse `path` when it can be read; an unreadable file is listed only."""
    try:
        data = read_limited(path)
    except OSError:
        return
    parse_text(plan, data.decode("utf-8", "replace"), path, depth)


# --------------------------------------------------------------------------
# watch list
# --------------------------------------------------------------------------
def watch_list(plan):
    """[(role, path, type, mask, via)]"""
    if plan.value is not None and plan.value != 0:
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
            except (OSError, RuntimeError, ValueError):
                real = None
            if real is not None:
                out.append(("canonical", real, "file", MASK_CANON, via))
    return out


# --------------------------------------------------------------------------
# getoption
# --------------------------------------------------------------------------
def read_getoption(path):
    """-> raw bytes; Setup('unreadable') for a missing/unreadable/non-regular path."""
    try:
        st = os.stat(path)
        if not stat.S_ISREG(st.st_mode):
            raise Setup("unreadable")
        with open(path, "rb") as fh:
            data = fh.read(MAX_BYTES + 1)
    except OSError:
        raise Setup("unreadable")
    return data


def live_value(data):
    """Setup('too_large'|'bad_json') or the recorded live int (None when no record)."""
    if len(data) > MAX_BYTES:
        raise Setup("too_large")
    live = None
    for line in data.decode("utf-8", "replace").split("\n"):
        line = line.strip()
        if line == "":
            continue
        try:
            obj = json.loads(line)
        except ValueError:
            raise Setup("bad_json")
        except RecursionError:
            raise Setup("bad_json")
        if not isinstance(obj, dict):
            raise Setup("bad_json")
        opt = obj.get("option")
        val = obj.get("int")
        if opt == OPTION and isinstance(val, int) and not isinstance(val, bool):
            live = val
    return live


# --------------------------------------------------------------------------
# arguments and main run
# --------------------------------------------------------------------------
def parse_args(argv):
    opts = {}
    i = 0
    while i < len(argv):
        tok = argv[i]
        if tok not in ("--config", "--home", "--display-root", "--getoption"):
            raise Setup("usage")
        if tok in opts or i + 1 >= len(argv):
            raise Setup("usage")
        val = argv[i + 1]
        if not val.startswith("/"):
            raise Setup("usage")
        opts[tok] = val
        i += 2
    if "--config" not in opts:
        raise Setup("usage")
    return opts


def make_display(root):
    if root is None:
        return lambda p: p
    given = root[:-1] if root.endswith("/") else root
    cands = [given]
    try:
        real = os.path.realpath(root)
    except (OSError, ValueError):
        real = None
    if real is not None and real not in cands:
        cands.append(real)

    def display(p):
        for d in cands:
            if p == d or p.startswith(d + "/"):
                return "$ROOT" + p[len(d):]
        return p
    return display


def run(argv):
    """-> (stdout text, exit code)."""
    try:
        opts = parse_args(argv)
        config = opts["--config"]
        plan = Plan(opts.get("--home"))
        plan.display = make_display(opts.get("--display-root"))
        gdata = read_getoption(opts["--getoption"]) if "--getoption" in opts else None
        plan.paths.append((config, "main"))
        if os.path.isfile(config):
            parse_file(plan, config, 0)
        live = live_value(gdata) if gdata is not None else None
    except Setup as exc:
        return "MADO_WATCH: SETUP %s\n" % exc.reason, 2

    disp = plan.display
    watches = watch_list(plan)
    on = not (plan.value is not None and plan.value != 0)
    out = []
    out.append("MADO_WATCH: config=%s autoreload=%s disable_autoreload=%s paths=%d unsupported=%d errors=%d" % (
        disp(config), "on" if on else "off",
        "unset" if plan.value is None else str(plan.value),
        len(plan.paths), plan.unsupported, plan.errors))
    for kind, via, a, b in plan.events:
        if kind == "ERROR":
            out.append("MADO_WATCH: ERROR via=%s source=%s reason=%s" % (via, a, b))
        else:
            out.append("MADO_WATCH: SKIP via=%s path=%s reason=%s" % (via, disp(a), b))
    for n, (role, path, typ, mask, via) in enumerate(watches, 1):
        out.append("MADO_WATCH: n=%d role=%s path=%s type=%s mask=%s via=%s" % (
            n, role, disp(path), typ, mask, via))
    verdict = "NONE"
    if gdata is not None:
        cfg = 0 if on else 1
        if live is None:
            verdict = "UNKNOWN"
        elif live == cfg:
            verdict = "AGREE"
        else:
            verdict = "DIFFER"
        out.append("MADO_WATCH_LIVE: option=%s config=%d live=%s verdict=%s" % (
            OPTION, cfg, "?" if live is None else str(live), verdict))
    out.append("MADO_WATCH: DONE watches=%d unsupported=%d errors=%d live=%s" % (
        len(watches), plan.unsupported, plan.errors, verdict))
    return "\n".join(out) + "\n", 0


def emit(text):
    sys.stdout.flush()
    sys.stdout.buffer.write(text.encode("utf-8", "surrogateescape"))
    sys.stdout.buffer.flush()


# --------------------------------------------------------------------------
# selftest (informational): private temporary directory, removed afterwards
# --------------------------------------------------------------------------
def selftest():
    import shutil
    import tempfile
    results = []

    def check(name, cond):
        results.append((name, bool(cond)))

    root = tempfile.mkdtemp(prefix="mado-watchplan-selftest-")
    try:
        def w(rel, text):
            p = os.path.join(root, rel)
            os.makedirs(os.path.dirname(p), exist_ok=True)
            with open(p, "w") as fh:
                fh.write(text)
            return p

        # pure helpers
        check("int true", config_string_to_int("true") == 1)
        check("int online prefix", config_string_to_int("online") == 1)
        check("int no", config_string_to_int("no") == 0)
        check("int digits", config_string_to_int("007") == 7)
        check("int junk", config_string_to_int("maybe") is None)
        check("int unicode digit", config_string_to_int("\u0663") is None)
        check("abs tilde", absolute_path("~/a", "/c/x.conf", "/h") == "/h/a")
        check("abs absolute", absolute_path("/a/b", "/c/x.conf", "/h") == "/a/b")
        check("abs bare", absolute_path("a.conf", "/c/x.conf", "/h") == "/c/a.conf")
        check("abs dot", absolute_path("./a", "/c/d/x.conf", "/h") == "/c/d/a")
        check("abs parent", absolute_path("../a", "/c/d/x.conf", "/h") == "/c/a")
        check("abs dotdot literal", absolute_path("..x", "/c/d/x.conf", "/h") == "/c/d/..x")
        check("abs hidden", absolute_path(".h", "/c/x.conf", "/h") == "/c/.h")
        check("abs cur without slash", absolute_path("a", "x.conf", "/h") == "x.conf/a")
        check("display prefix", make_display("/a/b/")("/a/b/c") == "$ROOT/c")
        check("display equal", make_display("/a/b")("/a/b") == "$ROOT")
        check("display sibling", make_display("/a/b")("/a/bc") == "/a/bc")

        # argument handling
        check("usage none", run([]) == ("MADO_WATCH: SETUP usage\n", 2))
        check("usage relative", run(["--config", "rel"])[1] == 2)
        check("usage repeat", run(["--config", "/a", "--config", "/b"])[0] == "MADO_WATCH: SETUP usage\n")
        check("usage unknown", run(["--config", "/a", "--bogus", "/b"])[0] == "MADO_WATCH: SETUP usage\n")
        check("usage valueless", run(["--config"])[0] == "MADO_WATCH: SETUP usage\n")
        check("usage equals form", run(["--config=/a"])[0] == "MADO_WATCH: SETUP usage\n")

        # a tree: sources, glob order, directory, symlink, dangling, recursion
        main = w("t/hyprland.conf",
                 "# c\nsource = ./a.conf\nsource = g/*.conf\nsource = dd\nsource = xx\n"
                 "misc {\n  disable_autoreload = no # c\n  source = inner.conf\n}\n")
        w("t/a.conf", "source = ../up.conf\n")
        w("up.conf", "")
        w("t/g/B.conf", "")
        w("t/g/a.conf", "")
        w("t/g/.h.conf", "")
        os.makedirs(os.path.join(root, "t", "dd"))
        os.symlink("a.conf", os.path.join(root, "t", "g", "z.conf"))
        os.symlink("nowhere.conf", os.path.join(root, "t", "g", "zz.conf"))
        out, rc = run(["--config", main, "--display-root", root])
        lines = out.split("\n")
        check("tree rc", rc == 0)
        check("tree header", lines[0] == "MADO_WATCH: config=$ROOT/t/hyprland.conf autoreload=on "
              "disable_autoreload=0 paths=6 unsupported=1 errors=2")
        check("tree glob bytewise", lines.index(
            "MADO_WATCH: n=4 role=primary path=$ROOT/t/g/B.conf type=file "
            "mask=IN_CLOSE_WRITE|IN_DONT_FOLLOW via=$ROOT/t/hyprland.conf:3") > 0)
        check("tree dotfile excluded", ".h.conf" not in out)
        check("tree dir skipped", "SKIP via=$ROOT/t/hyprland.conf:4 path=$ROOT/t/dd reason=directory" in out)
        check("tree dangling aborts", "reason=inaccessible" in out)
        check("tree nomatch", "source=xx reason=nomatch" in out)
        check("tree canonical", "role=canonical path=$ROOT/t/g/a.conf type=file mask=IN_CLOSE_WRITE via=" in out)
        check("tree done", lines[-2] == "MADO_WATCH: DONE watches=7 unsupported=1 errors=2 live=NONE")
        check("tree trailing newline", out.endswith("\n") and not out.endswith("\n\n"))

        # disable_autoreload
        off = w("o/hyprland.conf", "misc:disable_autoreload = true\nsource = x.conf\n")
        out, rc = run(["--config", off, "--display-root", root])
        check("off empty list", "autoreload=off disable_autoreload=1 paths=1" in out and
              out.split("\n")[-2] == "MADO_WATCH: DONE watches=0 unsupported=0 errors=1 live=NONE")
        un = w("u/hyprland.conf", "$v = 1\nmisc {\n disable_autoreload = $v\n}\n"
               "misc:disable_autoreload = 0 ## x\nmisc:disable_autoreload = ?\nsource = ~/q\nsource=bad\\path\n")
        out, rc = run(["--config", un, "--display-root", root])
        check("unsupported count", "paths=1 unsupported=5 errors=0" in out)

        # missing config, depth cap
        out, rc = run(["--config", os.path.join(root, "none.conf")])
        check("missing config", rc == 0 and "type=missing" in out and "paths=1" in out)
        loop = w("l/hyprland.conf", "source = hyprland.conf\n")
        out, rc = run(["--config", loop])
        check("depth cap", "paths=18 unsupported=1 errors=0" in out)

        # getoption
        def go(text):
            p = w("go.json", text)
            return run(["--config", main, "--getoption", p])
        check("live agree", "live=AGREE" in go('{"option": "misc:disable_autoreload", "int": 0}\n')[0])
        check("live differ", "live=DIFFER" in go('{"option": "misc:disable_autoreload", "int": 1}\n')[0])
        check("live bool ignored", "live=UNKNOWN" in go('{"option": "misc:disable_autoreload", "int": true}\n')[0])
        check("live unknown line", "config=0 live=? verdict=UNKNOWN" in go('{"x": 1}\n\n')[0])
        check("live bad_json", go('[1]\n') == ("MADO_WATCH: SETUP bad_json\n", 2))
        check("live bad syntax", go('{bad\n')[0] == "MADO_WATCH: SETUP bad_json\n")
        check("live missing", run(["--config", main, "--getoption", os.path.join(root, "nope")])[0]
              == "MADO_WATCH: SETUP unreadable\n")
        check("live directory", run(["--config", main, "--getoption", root])[0]
              == "MADO_WATCH: SETUP unreadable\n")
        big = w("big.conf", "#" + "x" * MAX_BYTES + "\n")
        check("too_large config", run(["--config", big])[0] == "MADO_WATCH: SETUP too_large\n")
        check("too_large getoption", run(["--config", main, "--getoption", big])[0]
              == "MADO_WATCH: SETUP too_large\n")
    finally:
        shutil.rmtree(root, ignore_errors=True)

    failed = [name for name, ok in results if not ok]
    passed = len(results) - len(failed)
    for name in failed:
        sys.stderr.write("selftest FAIL: %s\n" % name)
    emit("MADO_WATCH: SELFTEST %d/%d assertions passed\n" % (passed, len(results)))
    return 0 if not failed else 1


def main(argv):
    if argv == ["--selftest"]:
        return selftest()
    text, rc = run(argv)
    emit(text)
    return rc


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
