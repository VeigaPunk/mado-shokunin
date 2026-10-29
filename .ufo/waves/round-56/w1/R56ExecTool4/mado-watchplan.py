#!/usr/bin/env python3
"""mado-watchplan - which files does Hyprland 0.56.2 watch for a config tree, and does `misc:disable_autoreload` agree with the running compositor?

Hyprland 0.56.2 (hyprlang era, `configProvider` hyprlang) builds the inotify watch list of its config watcher from
`m_configPaths`: the main config plus every regular file a `source =` line reaches (legacy `handleSource`,
src/config/legacy/ConfigManager.cpp; `absolutePath`, src/helpers/MiscFunctions.cpp). `CConfigWatcher::update`
(src/config/ConfigWatcher.cpp) watches each path with `IN_CLOSE_WRITE|IN_DONT_FOLLOW` (plus `IN_CREATE|IN_DELETE|
IN_MOVED_TO|IN_MOVED_FROM` for a directory), and for a symlink adds one watch on its canonical target with
`IN_CLOSE_WRITE`; a non-zero `misc:disable_autoreload` leaves the watch list empty. This tool predicts that list for a
config tree and joins `misc:disable_autoreload` to a `hyprctl getoption misc:disable_autoreload -j` dump. It is a
model of a deliberate subset, not Hyprland: everything outside the subset is counted `unsupported`, never guessed.

    mado-watchplan.py --config ~/.config/hypr/hyprland.conf --home ~ --getoption go.json
    mado-watchplan.py --config /abs/hyprland.conf --display-root /abs
    mado-watchplan.py --selftest

It reads only the files named by its arguments and the files its `source =` lines reach, and calls `os.stat`,
`os.lstat`, `os.path.realpath` and `glob` on those paths; it starts no process, opens no socket and writes nothing
(`--selftest` writes only under a private temporary directory that it removes).

Arguments (two-token form only, any order): `--config PATH` exactly once, `--home DIR` at most once, `--display-root DIR`
at most once, `--getoption PATH` at most once; every value is an absolute path. Anything else is setup reason `usage`.
`--selftest` alone is informational. Setup failure: stdout is exactly `MADO_WATCH: SETUP <reason>`, exit 2, reason
usage | unreadable (the `--getoption` path is missing, unreadable, a directory or not a regular file) | too_large (any
file read - config, sourced file, getoption - above 1048576 bytes) | bad_json (a non-empty `--getoption` line that is
not a JSON object). The `--config` path is never a setup error: it is listed, and parsed when it is a regular file.
When several setup reasons apply the first of usage, unreadable, too_large, bad_json wins.

Model. Files decode as UTF-8 with errors replaced and split on "\\n"; the category stack resets per file. A raw line is
stripped of space, tab, CR, LF, VT, FF; an empty line or one starting `#` is skipped. Without `=`: exactly `}` pops the
stack (on an empty stack it does nothing); a line ending in `{` pushes its text before the `{`; any other line is
ignored. With `=`: LHS and RHS are the stripped texts around the first `=`. LHS `source` inside a category is
unsupported, else the RHS cut at its first `#` is the source path. An LHS starting `$` is ignored. Only the key
`misc:disable_autoreload` matters; a line holding `$`, `{` or a backslash, a RHS holding `##`, or a value that is not
a hyprlang int (true/on/yes -> 1, false/off/no -> 0, digits) is unsupported. The last accepted value wins.

Source handling mirrors `handleSource`: a path shorter than 2 characters is ERROR bogus; `~` without `--home` or a
backslash is unsupported; the path is made absolute against the file holding the line, expanded with `glob` (bytewise
order; no match is ERROR nomatch); each match is stat-ed (failure: ERROR inaccessible and the rest of that line's
matches are skipped), a directory is SKIP directory, any other non-regular file SKIP nonregular, and a regular file
joins the list and is parsed with the depth capped at 16 (deeper files are listed, not parsed, unsupported).
Declared divergences from Hyprland: that depth cap, bytewise glob order versus the C library's collation, GLOB_TILDE
`~user` forms, the Lua config provider, and a runtime `hyprctl keyword misc:disable_autoreload`.

Output (stdout; every line starts MADO_WATCH or MADO_WATCH_LIVE; exit 0 on a completed run):
  MADO_WATCH: config=<c> autoreload=<on|off> disable_autoreload=<unset|N> paths=<n> unsupported=<U> errors=<E>
  MADO_WATCH: ERROR via=<via> source=<RAW> reason=<bogus|nomatch|inaccessible>      (events, processing order)
  MADO_WATCH: SKIP via=<via> path=<p> reason=<directory|nonregular>
  MADO_WATCH: n=<k> role=<primary|canonical> path=<p> type=<file|dir|missing> mask=<mask> via=<via>
  MADO_WATCH_LIVE: option=misc:disable_autoreload config=<0|1> live=<int|?> verdict=<AGREE|DIFFER|UNKNOWN>  (--getoption)
  MADO_WATCH: DONE watches=<n> unsupported=<U> errors=<E> live=<NONE|AGREE|DIFFER|UNKNOWN>

With `--display-root DIR` a printed path equal to DIR or under DIR (given text or its realpath) prints as `$ROOT...`.
"""
import glob
import json
import os
import re
import stat
import sys

MAX_BYTES = 1048576
MAX_DEPTH = 16
# Defensive cap, not in the registration: a file that sources itself from several lines grows the path list as
# lines**16; past this many list entries the run is a setup failure too_large instead of an unbounded loop.
MAX_ENTRIES = 262144
WS = " \t\r\n\x0b\x0c"
OPTION = "misc:disable_autoreload"
MASK_FILE = "IN_CLOSE_WRITE|IN_DONT_FOLLOW"
MASK_DIR = "IN_CLOSE_WRITE|IN_DONT_FOLLOW|IN_CREATE|IN_DELETE|IN_MOVED_TO|IN_MOVED_FROM"
MASK_CANON = "IN_CLOSE_WRITE"
DIGITS = re.compile(r"[0-9]+")


class Setup(Exception):
    pass


def parse_args(argv):
    if argv == ["--selftest"]:
        return "selftest", {}
    opts = {}
    if len(argv) % 2:
        raise Setup("usage")
    for i in range(0, len(argv), 2):
        flag, value = argv[i], argv[i + 1]
        if flag not in ("--config", "--home", "--display-root", "--getoption") or flag in opts:
            raise Setup("usage")
        if not value.startswith("/"):
            raise Setup("usage")
        opts[flag] = value
    if "--config" not in opts:
        raise Setup("usage")
    return "run", opts


def read_limited(path):
    """Bytes of a file; Setup('too_large') above MAX_BYTES. OSError propagates."""
    with open(path, "rb") as fh:
        data = fh.read(MAX_BYTES + 1)
    if len(data) > MAX_BYTES:
        raise Setup("too_large")
    return data


def is_regular(path):
    try:
        return stat.S_ISREG(os.stat(path).st_mode)
    except (OSError, ValueError):
        return False


def config_int(value):
    """hyprlang configStringToInt as modelled: (ok, normalised decimal string)."""
    if value.startswith(("true", "on", "yes")):
        return True, "1"
    if value.startswith(("false", "off", "no")):
        return True, "0"
    if DIGITS.fullmatch(value):
        return True, value.lstrip("0") or "0"
    return False, ""


def absolute_path(raw, cur, home):
    """MiscFunctions.cpp absolutePath as registered; home may be None only when raw has no leading `~`."""
    if raw[0] == "~":
        return home + raw[1:]
    if raw[0] == "/":
        return raw
    pos = cur.rfind("/")
    curdir = cur[:pos] if pos >= 0 else cur
    if raw[0] == ".":
        if raw.startswith("../"):
            pos = curdir.rfind("/")
            parent = curdir[:pos] if pos >= 0 else curdir
            return parent + raw[2:]
        if raw.startswith("./"):
            return curdir + raw[1:]
        return curdir + "/" + raw
    return curdir + "/" + raw


def bytewise(path):
    return path.encode("utf-8", "surrogateescape")


def expand(pattern):
    """sorted(glob.glob(pattern)) in bytewise order; a glob that errors is no match."""
    try:
        found = glob.glob(pattern)
        return sorted(found, key=bytewise)
    except (OSError, ValueError, RecursionError, re.error):
        return []


class Plan:
    def __init__(self, opts):
        self.config = opts["--config"]
        self.home = opts.get("--home")
        root = opts.get("--display-root")
        self.prefixes = []
        if root is not None:
            given = root[:-1] if root.endswith("/") else root
            self.prefixes.append(given)
            try:
                self.prefixes.append(os.path.realpath(root))
            except (OSError, ValueError):
                pass
        self.entries = []  # (path, via text)
        self.events = []
        self.unsupported = 0
        self.errors = 0
        self.value = None  # last accepted misc:disable_autoreload, normalised decimal string

    def show(self, path):
        for prefix in self.prefixes:
            if path == prefix or path.startswith(prefix + "/"):
                return "$ROOT" + path[len(prefix):]
        return path

    def add_entry(self, path, via):
        if len(self.entries) >= MAX_ENTRIES:
            raise Setup("too_large")
        self.entries.append((path, via))

    def event_error(self, via, raw, reason):
        self.errors += 1
        self.events.append("MADO_WATCH: ERROR via=%s source=%s reason=%s" % (via, raw, reason))

    def parse_file(self, path, depth):
        try:
            data = read_limited(path)
        except OSError:
            return  # listed, not parsed
        stack = []
        for number, raw_line in enumerate(data.decode("utf-8", errors="replace").split("\n"), 1):
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
            lhs, _, rhs = line.partition("=")
            lhs, rhs = lhs.strip(WS), rhs.strip(WS)
            if lhs == "source":
                if stack:
                    self.unsupported += 1
                    continue
                self.source(rhs.split("#", 1)[0].strip(WS), path, number, depth)
                continue
            if lhs.startswith("$"):
                continue
            key = ":".join(stack) + ":" + lhs if stack else lhs
            if key != OPTION:
                continue
            if "$" in line or "{" in line or "\\" in line or "##" in rhs:
                self.unsupported += 1
                continue
            ok, number_text = config_int(rhs.split("#", 1)[0].strip(WS))
            if ok:
                self.value = number_text
            else:
                self.unsupported += 1

    def source(self, raw, cur, number, depth):
        via = "%s:%d" % (self.show(cur), number)
        if len(raw) < 2:
            self.event_error(via, raw, "bogus")
            return
        if (raw[0] == "~" and self.home is None) or "\\" in raw:
            self.unsupported += 1
            return
        matches = expand(absolute_path(raw, cur, self.home))
        if not matches:
            self.event_error(via, raw, "nomatch")
            return
        for match in matches:
            target = absolute_path(match, cur, self.home) if match else match
            try:
                mode = os.stat(target).st_mode
            except (OSError, ValueError):
                self.event_error(via, raw, "inaccessible")
                return
            if stat.S_ISREG(mode):
                self.add_entry(target, via)
                if depth + 1 > MAX_DEPTH:
                    self.unsupported += 1
                else:
                    self.parse_file(target, depth + 1)
            elif stat.S_ISDIR(mode):
                self.events.append("MADO_WATCH: SKIP via=%s path=%s reason=directory" % (via, self.show(target)))
            else:
                self.events.append("MADO_WATCH: SKIP via=%s path=%s reason=nonregular" % (via, self.show(target)))

    def watches(self):
        out = []
        if self.value is not None and self.value.strip("0"):
            return out
        for path, via in self.entries:
            if os.path.isdir(path):
                kind, mask = "dir", MASK_DIR
            elif os.path.lexists(path):
                kind, mask = "file", MASK_FILE
            else:
                kind, mask = "missing", MASK_FILE
            out.append(("primary", path, kind, mask, via))
            if os.path.islink(path):
                try:
                    canonical = os.path.realpath(path, strict=True)
                except (OSError, ValueError, RuntimeError):
                    continue
                out.append(("canonical", canonical, "file", MASK_CANON, via))
        return out


def read_getoption(path):
    """Bytes of the getoption file; Setup unreadable / too_large."""
    try:
        if not stat.S_ISREG(os.stat(path).st_mode):
            raise Setup("unreadable")
    except (OSError, ValueError):
        raise Setup("unreadable")
    try:
        return read_limited(path)
    except OSError:
        raise Setup("unreadable")


def _no_constant(name):
    raise ValueError(name)


def live_value(data):
    """Live int for OPTION from the dump, or None; Setup('bad_json')."""
    live = {}
    for line in data.decode("utf-8", errors="replace").split("\n"):
        line = line.strip(WS)
        if not line:
            continue
        try:
            obj = json.loads(line, parse_constant=_no_constant)
        except (ValueError, RecursionError):
            raise Setup("bad_json")
        if not isinstance(obj, dict):
            raise Setup("bad_json")
        option, value = obj.get("option"), obj.get("int")
        if isinstance(option, str) and type(value) is int:
            live[option] = value
    return live.get(OPTION)


def report(opts):
    gdata = read_getoption(opts["--getoption"]) if "--getoption" in opts else None
    plan = Plan(opts)
    plan.add_entry(plan.config, "main")
    if is_regular(plan.config):
        plan.parse_file(plan.config, 0)
    live = live_value(gdata) if gdata is not None else None
    watches = plan.watches()
    value = plan.value
    off = value is not None and bool(value.strip("0"))
    lines = ["MADO_WATCH: config=%s autoreload=%s disable_autoreload=%s paths=%d unsupported=%d errors=%d" % (
        plan.show(plan.config), "off" if off else "on", "unset" if value is None else value,
        len(plan.entries), plan.unsupported, plan.errors)]
    lines += plan.events
    for k, (role, path, kind, mask, via) in enumerate(watches, 1):
        lines.append("MADO_WATCH: n=%d role=%s path=%s type=%s mask=%s via=%s" % (k, role, plan.show(path), kind, mask, via))
    verdict = "NONE"
    if gdata is not None:
        config_flag = 1 if off else 0
        verdict = "UNKNOWN" if live is None else ("AGREE" if live == config_flag else "DIFFER")
        lines.append("MADO_WATCH_LIVE: option=%s config=%d live=%s verdict=%s" % (
            OPTION, config_flag, "?" if live is None else live, verdict))
    lines.append("MADO_WATCH: DONE watches=%d unsupported=%d errors=%d live=%s" % (
        len(watches), plan.unsupported, plan.errors, verdict))
    return lines, 0


def run(argv):
    try:
        mode, opts = parse_args(argv)
        if mode == "selftest":
            return None, selftest()
        return report(opts)
    except Setup as exc:
        return ["MADO_WATCH: SETUP %s" % exc], 2


def selftest():
    import shutil
    import tempfile
    passed = [0, 0]

    def check(label, ok):
        passed[1] += 1
        if ok:
            passed[0] += 1
        else:
            print("MADO_WATCH_SELFTEST: FAIL %s" % label)

    tmp = tempfile.mkdtemp(prefix="mado-watchplan-")
    try:
        root = os.path.realpath(tmp)

        def put(name, data=b"", link=None):
            path = os.path.join(root, name)
            os.makedirs(os.path.dirname(path), exist_ok=True)
            if link is not None:
                os.symlink(link, path)
            else:
                with open(path, "wb") as fh:
                    fh.write(data if isinstance(data, bytes) else data.encode())
            return path

        def go(*args):
            return run(list(args))

        def tool(main, *extra):
            return go("--config", main, "--display-root", root, *extra)

        # arguments
        for argv in ([], ["--config"], ["--config", "x"], ["--config", "/a", "--config", "/b"], ["--home", "/h"],
                     ["--config", "/a", "--bogus", "/b"], ["--config", "/a", "--home", "/h", "--home", "/h"],
                     ["--config", "/a", "--selftest"], ["--config", "/a", "--getoption"],
                     ["--config=/a"], ["--config", "/a", "--display-root", "rel"],
                     ["--config", "/a", "--getoption", "x", "--getoption", "/y"]):
            check("usage %r" % (argv,), go(*argv) == (["MADO_WATCH: SETUP usage"], 2))
        # absolute_path
        for raw, cur, home, want in (("~/a", "/c/m.conf", "/h", "/h/a"), ("/x", "/c/m.conf", None, "/x"),
                                     ("a", "/c/m.conf", None, "/c/a"), ("./a", "/c/m.conf", None, "/c/a"),
                                     ("../a", "/c/d/m.conf", None, "/c/a"), (".h", "/c/m.conf", None, "/c/.h"),
                                     ("..x", "/c/m.conf", None, "/c/..x"), ("a", "m.conf", None, "m.conf/a"),
                                     ("../a", "/m.conf", None, "/a"), ("..", "/c/m.conf", None, "/c/.."),
                                     ("../../a", "/c/d/m.conf", None, "/c/../a")):
            check("abs %r" % raw, absolute_path(raw, cur, home) == want)
        # config_int
        for text, want in (("true", (True, "1")), ("online", (True, "1")), ("yes", (True, "1")), ("false", (True, "0")),
                           ("off", (True, "0")), ("none", (True, "0")), ("007", (True, "7")), ("000", (True, "0")),
                           ("12", (True, "12")), ("", (False, "")), ("maybe", (False, "")), ("-1", (False, "")),
                           ("1.5", (False, "")), ("True", (False, "")), ("1 2", (False, "")),
                           ("9" * 5000, (True, "9" * 5000))):
            check("int %r" % text[:12], config_int(text) == want)
        # fixtures built on disk
        main = put("a/hyprland.conf", "misc {\n    disable_autoreload = on\n}\n")
        lines, rc = tool(main)
        check("off", rc == 0 and lines[0].split(" paths")[0].endswith("autoreload=off disable_autoreload=1")
              and lines[-1] == "MADO_WATCH: DONE watches=0 unsupported=0 errors=0 live=NONE")
        main = put("b/hyprland.conf", "misc:disable_autoreload = 0")  # no final newline
        lines, rc = tool(main)
        check("no final newline", rc == 0 and "disable_autoreload=0" in lines[0] and "autoreload=on" in lines[0])
        main = put("c/hyprland.conf", "}\n}\ngeneral {\n  x = 1\n}\n}\nmisc {\ndisable_autoreload = 1\n}\n")
        lines, rc = tool(main)
        check("stack underflow ignored", rc == 0 and "disable_autoreload=1" in lines[0] and "unsupported=0" in lines[0])
        main = put("d/hyprland.conf", b"source = \xff\xfe.conf\nmisc:disable_autoreload = 1 # \xc3\x28\n")
        lines, rc = tool(main)
        check("non-utf8 bytes", rc == 0 and "errors=1" in lines[0] and "nomatch" in lines[1] and "\ufffd" in lines[1]
              and "disable_autoreload=1" in lines[0])
        put("e/real.conf", "a = 1\n")
        put("e/ln.conf", link="real.conf")
        main = put("e/hyprland.conf", "source = ln.conf\n")
        lines, rc = tool(main)
        check("symlink canonical", rc == 0 and lines[-2] == (
            "MADO_WATCH: n=3 role=canonical path=$ROOT/e/real.conf type=file mask=IN_CLOSE_WRITE via=$ROOT/e/hyprland.conf:1"))
        put("f/l1.conf", link="l2.conf")
        put("f/l2.conf", link="l1.conf")
        main = put("f/hyprland.conf", "source = l1.conf\nsource = after.conf\n")
        put("f/after.conf", "")
        lines, rc = tool(main)
        check("symlink loop inaccessible", rc == 0 and "errors=1" in lines[0] and lines[1].endswith(
            "source=l1.conf reason=inaccessible") and "paths=2" in lines[0])
        main = put("g/hyprland.conf", "source = hyprland.conf\n")
        lines, rc = tool(main)
        check("self source depth cap", rc == 0 and "paths=18 unsupported=1" in lines[0] and lines[-1].startswith(
            "MADO_WATCH: DONE watches=18 unsupported=1"))
        main = put("g2/hyprland.conf", "source = hyprland.conf\n" * 3)
        lines, rc = tool(main)
        check("self source blowup bounded", (lines, rc) == (["MADO_WATCH: SETUP too_large"], 2))
        main = put("h/hyprland.conf", "source = [x\nsource = a[\nsource = *[\nsource = ~/x\nsource = a\\b\nsource = x\n")
        lines, rc = tool(main)
        check("glob pattern errors", rc == 0 and lines[0].endswith("errors=4"))
        check("tilde without home, backslash", "unsupported=2" in lines[0])
        main = put("i/hyprland.conf", "x = 1\n" + "#" * 1048569 + "\n")
        lines, rc = tool(main)
        check("limit exactly ok", rc == 0 and os.path.getsize(main) == 1048576)
        main = put("j/hyprland.conf", b"#" * 1048577)
        check("config too_large", tool(main) == (["MADO_WATCH: SETUP too_large"], 2))
        main = put("k/hyprland.conf", "source = big.conf\n")
        put("k/big.conf", b"#" * 1048577)
        check("sourced too_large", tool(main) == (["MADO_WATCH: SETUP too_large"], 2))
        main = put("l/hyprland.conf", "")
        big = put("l/go.json", b" " * 1048577)
        check("getoption too_large", tool(main, "--getoption", big) == (["MADO_WATCH: SETUP too_large"], 2))
        check("getoption missing", tool(main, "--getoption", root + "/l/none.json") == (["MADO_WATCH: SETUP unreadable"], 2))
        check("getoption directory", tool(main, "--getoption", root + "/l") == (["MADO_WATCH: SETUP unreadable"], 2))
        check("unreadable beats too_large", tool(put("l2/hyprland.conf", b"#" * 1048577), "--getoption", root + "/l")
              == (["MADO_WATCH: SETUP unreadable"], 2))
        check("too_large beats bad_json", tool(put("l3/hyprland.conf", b"#" * 1048577), "--getoption",
                                              put("l3/go.json", "{bad")) == (["MADO_WATCH: SETUP too_large"], 2))
        for label, text, want in (("agree", '{"option": "misc:disable_autoreload", "int": 0}\n', "AGREE"),
                                  ("differ", '{"option": "misc:disable_autoreload", "int": 1}', "DIFFER"),
                                  ("bool", '{"option": "misc:disable_autoreload", "int": false}', "UNKNOWN"),
                                  ("other option", '{"option": "misc:x", "int": 0}\n\n  \n', "UNKNOWN"),
                                  ("empty file", "", "UNKNOWN"),
                                  ("float", '{"option": "misc:disable_autoreload", "int": 0.0}', "UNKNOWN"),
                                  ("later wins", '{"option": "misc:disable_autoreload", "int": 1}\n'
                                                 '{"option": "misc:disable_autoreload", "int": 0}', "AGREE")):
            lines, rc = tool(main, "--getoption", put("l/%s.json" % label.replace(" ", "_"), text))
            check("live " + label, rc == 0 and lines[-1].endswith("live=" + want) and
                  lines[-2].endswith("verdict=" + want))
        for label, text in (("array", "[1]"), ("string", '"x"'), ("number", "3"), ("null", "null"), ("broken", "{bad"),
                            ("nan", '{"int": NaN}'), ("deep", "[" * 100000), ("non-utf8", b"\xff"),
                            ("second line", '{"option": "a", "int": 1}\n[]')):
            check("bad_json " + label, tool(main, "--getoption", put("l/b-%s.json" % label.replace(" ", "_"), text))
                  == (["MADO_WATCH: SETUP bad_json"], 2))
        # config shapes
        lines, rc = tool(root + "/nope/hyprland.conf")
        check("missing config", rc == 0 and lines[1].endswith("type=missing mask=IN_CLOSE_WRITE|IN_DONT_FOLLOW via=main"))
        os.makedirs(root + "/m/dir.conf", exist_ok=True)
        lines, rc = tool(root + "/m/dir.conf")
        check("directory config", rc == 0 and "type=dir mask=IN_CLOSE_WRITE|IN_DONT_FOLLOW|IN_CREATE|IN_DELETE|IN_MOVED_TO|IN_MOVED_FROM" in lines[1])
        main = put("n/hyprland.conf", "source = sub\nsource = /dev/null\nsource = x\nsource = .\n")
        os.makedirs(root + "/n/sub", exist_ok=True)
        lines, rc = tool(main)
        check("skips", lines[1:3] == ["MADO_WATCH: SKIP via=$ROOT/n/hyprland.conf:1 path=$ROOT/n/sub reason=directory",
                                     "MADO_WATCH: SKIP via=$ROOT/n/hyprland.conf:2 path=/dev/null reason=nonregular"])
        check("bogus", "ERROR via=$ROOT/n/hyprland.conf:3 source=x reason=bogus" in lines[3] and
              "source=. reason=bogus" in lines[4])
        main = put("o/hyprland.conf", "source = ~/a.conf\n")
        put("o/home/a.conf", "")
        lines, rc = tool(main, "--home", root + "/o/home/")
        check("home with trailing slash", "path=$ROOT/o/home//a.conf" in lines[2])
        # display root: given text and realpath
        link = root + "/rootlink"
        os.symlink(root + "/e", link)
        lines, rc = go("--config", root + "/e/hyprland.conf", "--display-root", link)
        check("display via realpath", lines[0].startswith("MADO_WATCH: config=$ROOT/hyprland.conf "))
        lines, rc = go("--config", root + "/e/hyprland.conf", "--display-root", root + "/e/")
        check("display root trailing slash", lines[0].startswith("MADO_WATCH: config=$ROOT/hyprland.conf "))
        lines, rc = go("--config", root + "/e/hyprland.conf", "--display-root", root + "/e/hypr")
        check("display prefix is a path prefix", lines[0].startswith("MADO_WATCH: config=" + root))
        check("read-only: tmp tree untouched by runs", os.path.exists(root + "/e/real.conf"))
    finally:
        shutil.rmtree(tmp, ignore_errors=True)
    print("MADO_WATCH_SELFTEST: %d/%d assertions passed" % tuple(passed))
    return 0 if passed[0] == passed[1] else 1


def main():
    lines, rc = run(sys.argv[1:])
    if lines is not None:
        sys.stdout.flush()
        sys.stdout.buffer.write("".join(line + "\n" for line in lines).encode("utf-8", "surrogateescape"))
        sys.stdout.buffer.flush()
    return rc


if __name__ == "__main__":
    sys.exit(main())
