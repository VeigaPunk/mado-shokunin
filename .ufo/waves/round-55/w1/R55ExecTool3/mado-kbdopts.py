#!/usr/bin/env python3
"""mado-kbdopts.py -- predict a keyboard's repeat rate / repeat delay / numlock
values from Hyprland config text and join them to `hyprctl getoption -j`.

Read-only: reads only the files named by --config and --getoption, starts no
process, opens no socket, writes nothing but its own stdout.

Usage (two-token argument form only, any order):
    mado-kbdopts.py --config PATH [--config PATH ...] [--keyboard NAME ...]
                    [--getoption PATH]
    mado-kbdopts.py --selftest            (alone; informational)

Output grammar (stdout, one line each):
    MADO_KBDOPT: keyboard=<NAME|*> repeat_rate=<n> repeat_delay=<n> numlock=<0|1> from=<x>/<y>/<z> unsupported=<U>
    MADO_KBDOPT_LIVE: option=<opt> config=<n> live=<int|?> verdict=<AGREE|DIFFER|UNKNOWN>
    MADO_KBDOPT: DONE keyboards=<n> unsupported=<U> live=<NONE|AGREE|DIFFER|UNKNOWN>
Setup failure: `MADO_KBDOPT: SETUP <usage|unreadable|too_large|bad_json>`, exit 2.
A completed run exits 0.

Source pins this tool models (Hyprland 0.56.2, hyprlang 0.6.8; Hyprland
tag-pinned commit efb50993780079460b0cbed1363e2166a2de1d9f, round-55 fetch/):
  * hyprlang value parsing `configStringToInt`: hyprlang-config.cpp:259-262
    (round-46 pin .ufo/waves/round-46/fetch/hyprlang-config.cpp): a value that
    starts with true/on/yes is 1 (checked first), starts with false/off/no is
    0, otherwise a decimal integer; anything else is unsupported here.
  * option defaults and ranges, ConfigValues.cpp:277-280
    (fetch/Hyprland-ConfigValues.cpp): input:repeat_rate 25 (0..200),
    input:repeat_delay 600 (0..2000), input:numlock_by_default 0 (0..1).
  * per-device override, legacy ConfigManager.cpp:1115-1123
    (fetch/Hyprland-legacy-ConfigManager.cpp) `getDeviceInt`: the device value
    when the user set it, else the global option.
  * InputManager.cpp:1282-1283 (fetch/Hyprland-InputManager.cpp)
    `applyConfigToKeyboard` clamps rate and delay with std::max(0, ...): a
    no-op on the modelled range, so it is not modelled.
Everything outside this deliberate subset of hyprlang (variables, `source`,
`##`, `{{`, backslashes, bracket device forms, hex/sign/float/word values,
out-of-range values, device keys before a `name` line) is counted in
`unsupported` and never guessed. The tool does not observe a keypress.
"""
import json
import os
import re
import stat
import sys

MAX_BYTES = 1048576
STRIP = " \t\r\n\v\f"
OPTS = ("repeat_rate", "repeat_delay", "numlock_by_default")
DEFAULTS = {"repeat_rate": 25, "repeat_delay": 600, "numlock_by_default": 0}
RANGES = {"repeat_rate": (0, 200), "repeat_delay": (0, 2000),
          "numlock_by_default": (0, 1)}
LIVE_OPTS = ("input:repeat_rate", "input:repeat_delay", "input:numlock_by_default")
GLOBAL_KEYS = {"input:" + o: o for o in OPTS}
DIGITS = re.compile(r"[0-9]+")

if hasattr(sys, "set_int_max_str_digits"):
    sys.set_int_max_str_digits(0)


class Setup(Exception):
    def __init__(self, reason):
        Exception.__init__(self, reason)
        self.reason = reason


# ---------------------------------------------------------------- data model
class Model:
    """glob: option -> int; devs: name -> {option: int}; unsupported: int."""

    def __init__(self):
        self.glob = {}
        self.devs = {}
        self.unsupported = 0

    def effective(self, name, opt):
        d = self.devs.get(name)
        if d is not None and opt in d:
            return d[opt], "D"
        if opt in self.glob:
            return self.glob[opt], "G"
        return DEFAULTS[opt], "-"


# -------------------------------------------------------------------- parser
def parse_int(value):
    """hyprlang configStringToInt subset; None when unsupported."""
    for p in ("true", "on", "yes"):
        if value.startswith(p):
            return 1
    for p in ("false", "off", "no"):
        if value.startswith(p):
            return 0
    if DIGITS.fullmatch(value):
        return int(value)
    return None


def parse_text(model, text):
    stack = []
    cur = None
    for raw in text.split("\n"):
        line = raw.strip(STRIP)
        if line == "" or line[0] == "#":
            continue
        if "=" not in line:
            if line == "}":
                if stack:
                    stack.pop()
                if not stack:
                    cur = None
            elif line.endswith("{"):
                stack.append(line[:-1].strip(STRIP))
            continue
        lhs, rhs = line.split("=", 1)
        lhs = lhs.strip(STRIP)
        rhs = rhs.strip(STRIP)
        if lhs.startswith("$") or lhs == "source":
            continue
        key = ":".join(stack + [lhs])
        dev_key = stack == ["device"] and lhs in OPTS
        bracket = key.startswith("device[") and key.split(":")[-1] in OPTS
        if key in GLOBAL_KEYS:
            opt = GLOBAL_KEYS[key]
        elif dev_key:
            opt = lhs
        elif bracket:
            model.unsupported += 1
            continue
        elif stack == ["device"] and lhs == "name":
            name = rhs.split("#", 1)[0].strip(STRIP)
            model.devs.setdefault(name, {})
            cur = name
            continue
        else:
            continue
        if "$" in line or "{{" in line or "\\" in line:
            model.unsupported += 1
            continue
        if "##" in rhs:
            model.unsupported += 1
            continue
        value = parse_int(rhs.split("#", 1)[0].strip(STRIP))
        if value is None:
            model.unsupported += 1
            continue
        lo, hi = RANGES[opt]
        if value < lo or value > hi:
            model.unsupported += 1
            continue
        if dev_key:
            if cur is None:
                model.unsupported += 1
                continue
            model.devs[cur][opt] = value
        else:
            model.glob[opt] = value


def parse_getoption(text):
    """option -> int; raises Setup('bad_json') on a non-object line."""
    live = {}
    for raw in text.split("\n"):
        if raw == "":
            continue
        try:
            obj = json.loads(raw)
        except (ValueError, RecursionError):
            raise Setup("bad_json")
        if not isinstance(obj, dict):
            raise Setup("bad_json")
        o = obj.get("option")
        v = obj.get("int")
        if isinstance(o, str) and type(v) is int:
            live[o] = v
    return live


# -------------------------------------------------------------------- render
def render(model, keyboards, live):
    out = []
    names = keyboards if keyboards else ["*"]
    for n in names:
        vals, frm = [], []
        for opt in OPTS:
            v, f = model.effective(n, opt)
            vals.append(v)
            frm.append(f)
        out.append("MADO_KBDOPT: keyboard=%s repeat_rate=%d repeat_delay=%d "
                   "numlock=%d from=%s unsupported=%d"
                   % (n, vals[0], vals[1], vals[2], "/".join(frm),
                      model.unsupported))
    summary = "NONE"
    if live is not None:
        verdicts = []
        for lo in LIVE_OPTS:
            opt = GLOBAL_KEYS[lo]
            cfg = model.effective(None, opt)[0]
            if lo in live:
                lv = live[lo]
                verdict = "AGREE" if lv == cfg else "DIFFER"
                lvs = str(lv)
            else:
                verdict, lvs = "UNKNOWN", "?"
            verdicts.append(verdict)
            out.append("MADO_KBDOPT_LIVE: option=%s config=%d live=%s verdict=%s"
                       % (lo, cfg, lvs, verdict))
        summary = ("DIFFER" if "DIFFER" in verdicts else
                   "UNKNOWN" if "UNKNOWN" in verdicts else "AGREE")
    out.append("MADO_KBDOPT: DONE keyboards=%d unsupported=%d live=%s"
               % (len(names), model.unsupported, summary))
    return out


# ------------------------------------------------------------------ plumbing
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


def parse_args(argv):
    steps, keyboards, seen_getopt = [], [], False
    i = 0
    while i < len(argv):
        a = argv[i]
        if a not in ("--config", "--keyboard", "--getoption") or i + 1 >= len(argv):
            raise Setup("usage")
        v = argv[i + 1]
        i += 2
        if a == "--config":
            steps.append(("config", v))
        elif a == "--keyboard":
            keyboards.append(v)
        else:
            if seen_getopt:
                raise Setup("usage")
            seen_getopt = True
            steps.append(("getoption", v))
    if not any(k == "config" for k, _ in steps):
        raise Setup("usage")
    return steps, keyboards


def run(argv):
    steps, keyboards = parse_args(argv)
    model, live = Model(), None
    for kind, path in steps:
        text = read_file(path)
        if kind == "config":
            parse_text(model, text)
        else:
            live = parse_getoption(text)
    return render(model, keyboards, live)


# ------------------------------------------------------------------ selftest
def selftest():
    results = []

    def check(cond):
        results.append(bool(cond))

    def mk(*texts):
        m = Model()
        for t in texts:
            parse_text(m, t)
        return m

    # value parsing
    check(parse_int("true") == 1 and parse_int("on") == 1 and parse_int("yes") == 1)
    check(parse_int("false") == 0 and parse_int("off") == 0 and parse_int("no") == 0)
    check(parse_int("only") == 1 and parse_int("nope") == 0)
    check(parse_int("12") == 12 and parse_int("007") == 7)
    check(all(parse_int(x) is None for x in
              ("", "0x10", "+5", "-5", "1.5", "5a", "maybe", "٣")))
    # defaults
    m = mk("")
    check(m.effective("*", "repeat_rate") == (25, "-"))
    check(m.effective("*", "repeat_delay") == (600, "-"))
    check(m.effective("*", "numlock_by_default") == (0, "-"))
    # global via category and via flat key
    m = mk("input {\n repeat_rate = 40\n numlock_by_default = true\n}\n")
    check(m.effective("x", "repeat_rate") == (40, "G"))
    check(m.effective("x", "numlock_by_default") == (1, "G"))
    check(m.unsupported == 0)
    m = mk("input:repeat_delay = 300\n")
    check(m.glob == {"repeat_delay": 300} and m.unsupported == 0)  # empty stack: KEY = LHS
    # device overrides global, merge, later wins
    t = ("input {\n repeat_rate = 30\n}\n"
         "device {\n name = kbd-a # c\n repeat_rate = 50\n}\n"
         "device {\n name = kbd-a\n repeat_delay = 200\n repeat_rate = 60\n}\n")
    m = mk(t)
    check(m.effective("kbd-a", "repeat_rate") == (60, "D"))
    check(m.effective("kbd-a", "repeat_delay") == (200, "D"))
    check(m.effective("kbd-b", "repeat_rate") == (30, "G"))
    # key before name
    m = mk("device {\n repeat_rate = 5\n name = k\n}\n")
    check(m.unsupported == 1 and m.devs["k"] == {})
    # current device forgotten when stack empties
    m = mk("device {\n name = k\n}\ndevice {\n repeat_rate = 5\n}\n")
    check(m.unsupported == 1 and m.devs["k"] == {})
    # nested block inside device keeps device, irrelevant keys ignored
    m = mk("device {\n name = k\n touchpad {\n repeat_rate = 9\n }\n repeat_delay = 100\n}\n")
    check(m.devs["k"] == {"repeat_delay": 100} and m.unsupported == 0)
    # unsupported reasons
    for bad in ("repeat_rate = $x", "repeat_rate = 5 ## 6", "repeat_rate = 0x10",
                "repeat_rate = -1", "repeat_rate = 201", "repeat_rate = ",
                "repeat_rate = 5\\"):
        m = mk("input {\n" + bad + "\n}\n")
        check(m.unsupported == 1 and m.glob == {})
    m = mk("input {\n repeat_delay = 2001\n numlock_by_default = 2\n}\n")
    check(m.unsupported == 2)
    m = mk("device[k]:repeat_rate = 5\ndevice[k] {\n repeat_rate = 5\n}\n")
    check(m.unsupported == 2)  # both device[ forms count, one per line
    m = mk("input {\n repeat_rate = {{x}}\n}\n")
    check(m.unsupported == 1)
    # ignored lines
    m = mk("$v = 5\nsource = a.conf\n# repeat_rate = 5\ninput {\n kb_layout = us\n}\n}\n}\n")
    check(m.unsupported == 0 and m.glob == {})
    # inline comment cut, whitespace/CRLF handling
    m = mk("input {\r\n\trepeat_rate = 7 # note\r\n}\r\n")
    check(m.glob == {"repeat_rate": 7})
    # stack and device reset per file
    m = mk("input {\n", "repeat_rate = 5\n")
    check(m.glob == {})
    # getoption
    live = parse_getoption('{"option": "input:repeat_rate", "int": 40}\n\n'
                           '{"option": "input:repeat_delay", "int": true}\n'
                           '{"option": "input:repeat_rate", "int": 41}\n'
                           '{"int": 3}\n{"option": 5, "int": 1}\n'
                           '{"option": "input:numlock_by_default", "int": 1.0}\n')
    check(live == {"input:repeat_rate": 41})
    for bad in ("[1]", "x", "{", "5", "null"):
        try:
            parse_getoption(bad)
            check(False)
        except Setup as e:
            check(e.reason == "bad_json")
    # render
    m = mk("input {\n repeat_rate = 40\n}\n")
    lines = render(m, ["a", "a"], {"input:repeat_rate": 40, "input:repeat_delay": 601})
    check(len(lines) == 6 and lines[0] == lines[1])
    check(lines[0] == "MADO_KBDOPT: keyboard=a repeat_rate=40 repeat_delay=600 "
                      "numlock=0 from=G/-/- unsupported=0")
    check(lines[2].endswith("verdict=AGREE") and lines[3].endswith("verdict=DIFFER"))
    check(lines[4] == "MADO_KBDOPT_LIVE: option=input:numlock_by_default config=0 "
                      "live=? verdict=UNKNOWN")
    check(lines[5] == "MADO_KBDOPT: DONE keyboards=2 unsupported=0 live=DIFFER")
    check(render(m, [], None)[-1] == "MADO_KBDOPT: DONE keyboards=1 unsupported=0 live=NONE")
    check(render(m, [], {"input:repeat_rate": 40, "input:repeat_delay": 600,
                         "input:numlock_by_default": 0})[-1].endswith("live=AGREE"))
    check(render(m, [], {"input:repeat_rate": 40})[-1].endswith("live=UNKNOWN"))
    # argument grammar
    for bad in ([], ["--keyboard", "a"], ["--config"], ["--config=x"],
                ["--config", "a", "--getoption", "b", "--getoption", "c"],
                ["--config", "a", "extra"], ["--selftest", "--config", "a"],
                ["--getoption", "b"]):
        try:
            parse_args(bad)
            check(False)
        except Setup as e:
            check(e.reason == "usage")
    steps, kbs = parse_args(["--keyboard", "k", "--getoption", "g",
                             "--config", "a", "--config", "b"])
    check(steps == [("getoption", "g"), ("config", "a"), ("config", "b")] and kbs == ["k"])
    # file checks
    for p, reason in (("/nonexistent-r55/x", "unreadable"), ("/", "unreadable")):
        try:
            read_file(p)
            check(False)
        except Setup as e:
            check(e.reason == reason)

    n, ok = len(results), sum(results)
    sys.stdout.write("MADO_KBDOPT_SELFTEST: %d/%d assertions passed\n" % (ok, n))
    return 0 if ok == n else 1


def main(argv):
    if argv == ["--selftest"]:
        return selftest()
    try:
        lines = run(argv)
    except Setup as e:
        sys.stdout.buffer.write(("MADO_KBDOPT: SETUP %s\n" % e.reason).encode())
        sys.stdout.buffer.flush()
        return 2
    data = "".join(l + "\n" for l in lines).encode("utf-8", "surrogateescape")
    sys.stdout.buffer.write(data)
    sys.stdout.buffer.flush()
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
