#!/usr/bin/env python3
"""mado-kbdopts.py -- predict a keyboard's repeat rate / repeat delay / numlock
from Hyprland config text and join the result to `hyprctl getoption -j` output.

Read-only, single file, python3 stdlib only. It reads exactly the files named by
--config and --getoption (opened "rb"); it starts no process, opens no socket and
writes nothing but its own stdout. Run it as `python3 -I tools/mado-kbdopts.py`.

Usage (two-token form only; any other form, or no --config, is usage):
  mado-kbdopts.py --config PATH [--config PATH ...] [--keyboard NAME ...]
                  [--getoption PATH]
  mado-kbdopts.py --selftest          (alone; informational)

Source pins this tool models (registration.md section C2, round 55):
  * hyprlang 0.6.8 `configStringToInt` -- hyprlang-config.cpp:259-262
    (round-46 pin .ufo/waves/round-46/fetch/hyprlang-config.cpp): a value that
    starts with true/on/yes is 1, else starts with false/off/no is 0, else a
    decimal integer; the tool accepts only these token forms and counts anything
    else (hex, sign, float, empty, words) as `unsupported`.
  * Hyprland 0.56.2 (tag commit efb50993780079460b0cbed1363e2166a2de1d9f)
    src/config/ConfigValues.cpp:277-280 -- input:repeat_rate default 25, range
    0..200; input:repeat_delay default 600, range 0..2000;
    input:numlock_by_default default 0, range 0..1
    (pin .ufo/waves/round-55/fetch/Hyprland-ConfigValues.cpp).
  * legacy ConfigManager.cpp:1115-1123 `getDeviceInt` -- the per-device value is
    used when the user set it for that device, else the global option
    (pin fetch/Hyprland-legacy-ConfigManager.cpp).
  * src/managers/input/InputManager.cpp:1282-1283 `applyConfigToKeyboard` -- the
    stored rate and delay are clamped with std::max(0, ...), a no-op on the
    modelled range (pin fetch/Hyprland-InputManager.cpp).

Config model (a deliberate subset of hyprlang; everything outside it is counted
in `unsupported`, never guessed): category stack from `name {` / `}` lines,
`device { name = X ... }` blocks (a second block with the same name merges, later
keys win), global keys `input:<key>` or inside `input { }`. Not modelled: the
`device[NAME]:key` bracket form, variables (`$`), `{{`, backslashes, `##`,
`source`, hex/sign/float values.

Output grammar (stdout, exit 0 on a completed run):
  MADO_KBDOPT: keyboard=<NAME|*> repeat_rate=<n> repeat_delay=<n> numlock=<0|1> from=<x>/<y>/<z> unsupported=<U>
  MADO_KBDOPT_LIVE: option=<opt> config=<n> live=<int|?> verdict=<AGREE|DIFFER|UNKNOWN>   (with --getoption)
  MADO_KBDOPT: DONE keyboards=<n> unsupported=<U> live=<NONE|AGREE|DIFFER|UNKNOWN>
Setup failure: `MADO_KBDOPT: SETUP <usage|unreadable|too_large|bad_json>`, exit 2.
`from` letters: D device value, G global value, - built-in default.
"""
import json
import os
import re
import stat
import sys

MAX_BYTES = 1048576
WS = " \t\r\n\v\f"

# name -> (default, maximum); minimum is 0 for all three (ConfigValues.cpp:277-280)
OPTIONS = (
    ("repeat_rate", 25, 200),
    ("repeat_delay", 600, 2000),
    ("numlock_by_default", 0, 1),
)
NAMES = tuple(o[0] for o in OPTIONS)
LIVE_OPTIONS = tuple("input:" + n for n in NAMES)
_UINT = re.compile(r"[0-9]+")


class Setup(Exception):
    def __init__(self, reason):
        Exception.__init__(self, reason)
        self.reason = reason


def parse_value(text):
    """hyprlang configStringToInt subset: int, or None when outside the token set."""
    if text.startswith(("true", "on", "yes")):
        return 1
    if text.startswith(("false", "off", "no")):
        return 0
    if _UINT.fullmatch(text):
        if len(text) > 12:  # beyond every modelled range; avoid giant int work
            return 10 ** 12
        return int(text)
    return None


class Model:
    def __init__(self):
        self.glob = {}      # option name -> int
        self.dev = {}       # device name -> {option name -> int}
        self.unsupported = 0

    def feed(self, text):
        """Feed one file's decoded text; stack and current device reset per file."""
        stack = []
        cur = None
        for raw in text.split("\n"):
            line = raw.strip(WS)
            if not line or line[0] == "#":
                continue
            if "=" not in line:
                if line == "}":
                    if stack:
                        stack.pop()
                    if not stack:
                        cur = None
                elif line.endswith("{"):
                    stack.append(line[:-1].strip(WS))
                continue
            lhs, rhs = line.split("=", 1)
            lhs = lhs.strip(WS)
            rhs = rhs.strip(WS)
            if lhs.startswith("$") or lhs == "source":
                continue
            key = ":".join(stack + [lhs])
            in_dev = stack == ["device"]
            if in_dev and lhs == "name":
                cur = rhs.split("#", 1)[0].strip(WS)
                self.dev.setdefault(cur, {})
                continue
            relevant_global = key in LIVE_OPTIONS
            relevant_dev = in_dev and lhs in NAMES
            relevant_brk = key.startswith("device[") and key.rsplit(":", 1)[-1] in NAMES
            if not (relevant_global or relevant_dev or relevant_brk):
                continue
            if key.startswith("device["):
                self.unsupported += 1
                continue
            if "$" in line or "{{" in line or "\\" in line:
                self.unsupported += 1
                continue
            if "##" in rhs:
                self.unsupported += 1
                continue
            value = parse_value(rhs.split("#", 1)[0].strip(WS))
            if value is None:
                self.unsupported += 1
                continue
            name = lhs if relevant_dev else key[len("input:"):]
            if value > dict((o[0], o[2]) for o in OPTIONS)[name]:
                self.unsupported += 1
                continue
            if relevant_dev:
                if cur is None:
                    self.unsupported += 1
                    continue
                self.dev[cur][name] = value
            else:
                self.glob[name] = value

    def effective(self, keyboard):
        """-> ([rate, delay, numlock], 'x/y/z')"""
        vals, src = [], []
        d = self.dev.get(keyboard, {}) if keyboard != "*" else {}
        for name, default, _ in OPTIONS:
            if name in d:
                vals.append(d[name]); src.append("D")
            elif name in self.glob:
                vals.append(self.glob[name]); src.append("G")
            else:
                vals.append(default); src.append("-")
        return vals, "/".join(src)

    def global_value(self, name):
        for n, default, _ in OPTIONS:
            if n == name:
                return self.glob.get(n, default)


def read_file(path):
    try:
        st = os.stat(path)
        if not stat.S_ISREG(st.st_mode):
            raise Setup("unreadable")
        with open(path, "rb") as fh:
            data = fh.read(MAX_BYTES + 1)
    except Setup:
        raise
    except (OSError, ValueError):
        raise Setup("unreadable")
    if len(data) > MAX_BYTES:
        raise Setup("too_large")
    return data.decode("utf-8", errors="replace")


def parse_live(text):
    """-> {option: int}; raises Setup('bad_json') for a non-empty non-object line."""
    live = {}
    for raw in text.split("\n"):
        line = raw.strip(WS)
        if not line:
            continue
        try:
            obj = json.loads(line)
        except (ValueError, RecursionError):
            raise Setup("bad_json")
        if not isinstance(obj, dict):
            raise Setup("bad_json")
        opt, val = obj.get("option"), obj.get("int")
        if isinstance(opt, str) and isinstance(val, int) and not isinstance(val, bool):
            live[opt] = val
    return live


def parse_args(argv):
    configs, keyboards, getopt = [], [], None
    i = 0
    while i < len(argv):
        flag = argv[i]
        if flag not in ("--config", "--keyboard", "--getoption") or i + 1 >= len(argv):
            raise Setup("usage")
        val = argv[i + 1]
        if flag == "--config":
            configs.append(val)
        elif flag == "--keyboard":
            keyboards.append(val)
        else:
            if getopt is not None:
                raise Setup("usage")
            getopt = val
        i += 2
    if not configs:
        raise Setup("usage")
    return configs, keyboards, getopt


def run(argv, reader=read_file):
    """-> list of stdout lines (no newline); raises Setup."""
    configs, keyboards, getopt = parse_args(argv)
    model = Model()
    for path in configs:
        model.feed(reader(path))
    live = parse_live(reader(getopt)) if getopt is not None else None
    out = []
    names = keyboards or ["*"]
    for kb in names:
        (rate, delay, numlock), frm = model.effective(kb)
        out.append("MADO_KBDOPT: keyboard=%s repeat_rate=%d repeat_delay=%d numlock=%d from=%s unsupported=%d"
                   % (kb, rate, delay, numlock, frm, model.unsupported))
    summary = "NONE"
    if live is not None:
        verdicts = []
        for opt in LIVE_OPTIONS:
            cfg = model.global_value(opt[len("input:"):])
            if opt in live:
                v = "AGREE" if live[opt] == cfg else "DIFFER"
                lv = str(live[opt])
            else:
                v, lv = "UNKNOWN", "?"
            verdicts.append(v)
            out.append("MADO_KBDOPT_LIVE: option=%s config=%d live=%s verdict=%s" % (opt, cfg, lv, v))
        summary = "DIFFER" if "DIFFER" in verdicts else "UNKNOWN" if "UNKNOWN" in verdicts else "AGREE"
    out.append("MADO_KBDOPT: DONE keyboards=%d unsupported=%d live=%s" % (len(names), model.unsupported, summary))
    return out


def emit(lines):
    sys.stdout.flush()
    sys.stdout.buffer.write(("".join(l + "\n" for l in lines)).encode("utf-8", "surrogateescape"))
    sys.stdout.buffer.flush()


def selftest():
    results = []

    def check(cond):
        results.append(bool(cond))

    mem = {}
    def reader(p):
        if p not in mem:
            raise Setup("unreadable")
        return mem[p]

    # value parsing
    for text, want in (("true", 1), ("on", 1), ("yes", 1), ("false", 0), ("off", 0), ("no", 0),
                       ("none", 0), ("onx", 1), ("30", 30), ("030", 30), ("0", 0),
                       ("0x10", None), ("+5", None), ("-5", None), ("1.5", None), ("", None),
                       ("maybe", None), ("True", None), ("5 5", None)):
        check(parse_value(text) == want)
    # defaults
    m = Model(); m.feed("")
    check(m.effective("*") == ([25, 600, 0], "-/-/-"))
    # global keys, both forms
    m = Model(); m.feed("input {\n repeat_rate = 40\n}\ninput:repeat_delay = 300\n")
    check(m.effective("x") == ([40, 300, 0], "G/G/-"))
    # device block, merge, later wins
    m = Model()
    m.feed("device {\n name = kb1\n repeat_rate = 10\n}\ndevice {\n name = kb1\n repeat_rate = 11 # c\n numlock_by_default = yes\n}\n")
    check(m.effective("kb1") == ([11, 600, 1], "D/-/D"))
    check(m.effective("other") == ([25, 600, 0], "-/-/-"))
    check(m.effective("*") == ([25, 600, 0], "-/-/-"))
    # device overrides global
    m = Model(); m.feed("input:repeat_rate = 50\ndevice {\nname = a\nrepeat_rate = 7\n}\n")
    check(m.effective("a")[0][0] == 7 and m.effective("b")[0][0] == 50)
    # key before name, bracket form, variables, range, hex, ##, backslash
    m = Model(); m.feed("device {\nrepeat_rate = 5\nname = z\n}\n")
    check(m.unsupported == 1 and m.effective("z")[0][0] == 25)
    m = Model(); m.feed("device[k]:repeat_rate = 5\n")
    check(m.unsupported == 1)
    m = Model(); m.feed("input:repeat_rate = $r\ninput:repeat_delay = 300 # $x\n")
    check(m.unsupported == 2 and m.glob == {})
    m = Model(); m.feed("input:repeat_rate = 201\ninput:repeat_delay = 2001\ninput:numlock_by_default = 2\n")
    check(m.unsupported == 3 and m.glob == {})
    m = Model(); m.feed("input:repeat_rate = 0x10\ninput:repeat_delay = ##\ninput:numlock_by_default = a\\b\n")
    check(m.unsupported == 3)
    m = Model(); m.feed("input:repeat_rate = 200\ninput:repeat_delay = 2000\ninput:numlock_by_default = 1\n")
    check(m.unsupported == 0 and m.glob == {"repeat_rate": 200, "repeat_delay": 2000, "numlock_by_default": 1})
    # nested blocks, comments, per-file reset, ignored lines
    m = Model()
    m.feed("device {\nname = t\ntouchpad {\nrepeat_rate = 9\n}\nrepeat_delay = 100\n}\n# c\nsource = x\n$v = 1\nbogus line\n")
    check(m.unsupported == 0 and m.dev["t"] == {"repeat_delay": 100})
    m = Model(); m.feed("device {\nname = n # tail\nrepeat_rate = 3\n}\n")
    check("n" in m.dev and m.dev["n"] == {"repeat_rate": 3})
    m = Model(); m.feed("device {\nname = a\n"); m.feed("repeat_rate = 5\n")
    check(m.unsupported == 0 and m.glob == {})
    m = Model(); m.feed("device {\r\n\tname = c\r\n\trepeat_rate = 12\r\n}\r\n")
    check(m.dev["c"] == {"repeat_rate": 12})
    # arguments
    for bad in ([], ["--keyboard", "a"], ["--config"], ["--config", "x", "--config=y"],
                ["--config", "x", "--getoption", "g", "--getoption", "h"], ["--selftest", "--config", "x"],
                ["--config", "x", "extra"]):
        try:
            parse_args(bad); check(False)
        except Setup as e:
            check(e.reason == "usage")
    check(parse_args(["--keyboard", "k", "--config", "a", "--config", "b", "--getoption", "g"]) == (["a", "b"], ["k"], "g"))
    # run + live join
    mem["c"] = "input:repeat_rate = 30\n"
    mem["g"] = ('{"option":"input:repeat_rate","int":30}\n\n[1]\n'.replace("[1]\n", "") +
                '{"option":"input:repeat_delay","int":true}\n{"option":"input:numlock_by_default","int":1}\n'
                '{"option":"input:numlock_by_default","int":0.0}\n')
    out = run(["--config", "c", "--keyboard", "k", "--keyboard", "k", "--getoption", "g"], reader)
    check(out[0] == "MADO_KBDOPT: keyboard=k repeat_rate=30 repeat_delay=600 numlock=0 from=G/-/- unsupported=0")
    check(out[0] == out[1])
    check(out[2] == "MADO_KBDOPT_LIVE: option=input:repeat_rate config=30 live=30 verdict=AGREE")
    check(out[3] == "MADO_KBDOPT_LIVE: option=input:repeat_delay config=600 live=? verdict=UNKNOWN")
    check(out[4] == "MADO_KBDOPT_LIVE: option=input:numlock_by_default config=0 live=1 verdict=DIFFER")
    check(out[5] == "MADO_KBDOPT: DONE keyboards=2 unsupported=0 live=DIFFER")
    check(run(["--config", "c"], reader)[-1] == "MADO_KBDOPT: DONE keyboards=1 unsupported=0 live=NONE")
    mem["g"] = '{"option":"input:repeat_rate","int":30}\n{"option":"input:repeat_rate","int":31}\n'
    check(run(["--config", "c", "--getoption", "g"], reader)[1].endswith("live=31 verdict=DIFFER"))
    mem["g"] = ""
    check(run(["--config", "c", "--getoption", "g"], reader)[-1].endswith("live=UNKNOWN"))
    mem["g"] = "not json\n"
    try:
        run(["--config", "c", "--getoption", "g"], reader); check(False)
    except Setup as e:
        check(e.reason == "bad_json")
    mem["g"] = "[1]\n"
    try:
        run(["--config", "c", "--getoption", "g"], reader); check(False)
    except Setup as e:
        check(e.reason == "bad_json")
    try:
        run(["--config", "missing"], reader); check(False)
    except Setup as e:
        check(e.reason == "unreadable")
    # live=AGREE when all three agree
    mem["g"] = ('{"option":"input:repeat_rate","int":30}\n{"option":"input:repeat_delay","int":600}\n'
                '{"option":"input:numlock_by_default","int":0}\n')
    check(run(["--config", "c", "--getoption", "g"], reader)[-1].endswith("live=AGREE"))

    ok = sum(results)
    emit(["MADO_KBDOPT_SELFTEST: %d/%d assertions passed" % (ok, len(results))])
    return 0 if ok == len(results) else 1


def main(argv):
    if hasattr(sys, "set_int_max_str_digits"):
        sys.set_int_max_str_digits(0)
    if argv == ["--selftest"]:
        return selftest()
    try:
        emit(run(argv))
        return 0
    except Setup as e:
        emit(["MADO_KBDOPT: SETUP " + e.reason])
        return 2


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
