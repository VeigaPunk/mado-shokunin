#!/usr/bin/env python3
"""mado-kbdopts - what repeat rate, repeat delay and numlock does each keyboard's config give it, and does `hyprctl getoption` agree?

Hyprland 0.56.2 (efb50993) applies three per-keyboard values in src/managers/input/InputManager.cpp
applyConfigToKeyboard: repeat_rate and repeat_delay (stored after `std::max(0, ...)`, InputManager.cpp:1282-1283,
a no-op on the modelled range) and numlock_by_default. Each is read with getDeviceInt: the value of the `device`
block whose name equals the keyboard's name when that block SETS the key, else the global `input:` option
(src/config/legacy/ConfigManager.cpp:1115-1123). The built-in defaults are 25 / 600 / 0 and the ranges 0..200 /
0..2000 / 0..1 (src/config/values/ConfigValues.cpp:277-280). The values reach the seat as `wl_keyboard.repeat_info`
(src/protocols/core/Seat.cpp, src/managers/SeatManager.cpp updateActiveKeyboardData); this tool does not observe a
keypress, it predicts the stored values from config text and joins the global ones to `hyprctl getoption -j`.

An integer value is read the way hyprlang 0.6.8 configStringToInt does (src/config.cpp:259-262, round-46 pin
`.ufo/waves/round-46/fetch/hyprlang-config.cpp`): text starting with `true`, `on` or `yes` is 1 (checked first), text
starting with `false`, `off` or `no` is 0, otherwise only `[0-9]+` is a number. Everything outside the modelled
subset is counted as `unsupported` and never guessed. It is a join, not a blame: a DIFFER may come from a runtime
`hyprctl keyword`, a config file not passed, or a `source =` line it does not follow.

    mado-kbdopts.py --config ~/.config/hypr/input.conf --keyboard at-translated-set-2-keyboard --getoption opts.json
    mado-kbdopts.py --config a.conf --config b.conf
    mado-kbdopts.py --selftest

It reads the files named by --config and --getoption only; it starts no process, opens no socket and writes nothing
but stdout.

Arguments (two-token form only; anything else is usage): `--config PATH` one or more times, `--keyboard NAME` zero or
more times, `--getoption PATH` at most once, in any order; `--selftest` alone prints
`MADO_KBDOPT_SELFTEST: N/N assertions passed`. Setup failure: stdout is exactly one line `MADO_KBDOPT: SETUP <reason>`,
exit 2, reason one of usage | unreadable (missing, unreadable, directory, FIFO or any non-regular path) | too_large
(a file over 1048576 bytes) | bad_json (a non-empty --getoption line that is not a JSON object).

Config model (registration round 55 section C2): files are read in argument order, decoded as UTF-8 with errors
replaced and split on "\\n"; the category stack and the current device reset at each file's start. A raw line is
stripped of space, tab, CR, LF, VT, FF; an empty line or one starting with `#` is skipped. Without `=`: exactly `}`
pops the stack (an empty stack forgets the current device), a line ending in `{` pushes its text before the `{`,
stripped, anything else is ignored. With `=`: LHS and RHS are the stripped texts around the FIRST `=`; an LHS starting
with `$` or equal to `source` is ignored; KEY is the stack and LHS joined with `:`. A line is RELEVANT when KEY is
`input:repeat_rate`, `input:repeat_delay` or `input:numlock_by_default`; or the stack is exactly ["device"] and LHS is
one of the three names; or KEY starts with `device[` and its last `:` component is one of the three names. With stack
exactly ["device"] and LHS `name` the current device becomes RHS cut at its first `#` and stripped. For a relevant line
the first failing check adds one to `unsupported` and ends the line: bracket form (`device[`), a `$`, `{{` or backslash
anywhere in the line, `##` in the RHS, a VALUE (RHS cut at the first `#`, stripped) that is not a modelled token, a
value outside the range, a device key before any `name`. An `input:` KEY sets the global value, a device key the current
device's value (later wins, same-name blocks merge). Effective value for keyboard NAME (`*` without --keyboard): device
value if set for NAME, else global if set, else default; `from` letters D / G / -.

Output: `MADO_KBDOPT: keyboard=<NAME|*> repeat_rate=<n> repeat_delay=<n> numlock=<0|1> from=<x>/<y>/<z> unsupported=<U>`
per keyboard; with --getoption three `MADO_KBDOPT_LIVE: option=<opt> config=<n> live=<int|?> verdict=<AGREE|DIFFER|UNKNOWN>`
lines; then `MADO_KBDOPT: DONE keyboards=<n> unsupported=<U> live=<NONE|AGREE|DIFFER|UNKNOWN>`. Exit 0 on a completed run.
"""
import json
import os
import re
import stat
import sys

MAX_BYTES = 1048576
WS = " \t\r\n\v\f"
NAMES = ("repeat_rate", "repeat_delay", "numlock_by_default")
GLOBAL_KEYS = {"input:" + n: n for n in NAMES}
RANGE = {"repeat_rate": (0, 200), "repeat_delay": (0, 2000), "numlock_by_default": (0, 1)}
DEFAULT = {"repeat_rate": 25, "repeat_delay": 600, "numlock_by_default": 0}
OPTIONS = ("input:repeat_rate", "input:repeat_delay", "input:numlock_by_default")
DIGITS_RE = re.compile(r"[0-9]+")


class Setup(Exception):
    pass


def read_regular(path):
    try:
        fd = os.open(path, os.O_RDONLY | os.O_NONBLOCK)
    except (OSError, ValueError):
        raise Setup("unreadable")
    try:
        if not stat.S_ISREG(os.fstat(fd).st_mode):
            raise Setup("unreadable")
        data = b""
        while len(data) <= MAX_BYTES:
            chunk = os.read(fd, MAX_BYTES + 1 - len(data))
            if not chunk:
                break
            data += chunk
    except OSError:
        raise Setup("unreadable")
    finally:
        os.close(fd)
    if len(data) > MAX_BYTES:
        raise Setup("too_large")
    return data


def parse_args(argv):
    if argv == ["--selftest"]:
        return "selftest", None, None, None
    configs, keyboards, getoption, i = [], [], None, 0
    while i < len(argv):
        if i + 1 >= len(argv):
            raise Setup("usage")
        flag, value = argv[i], argv[i + 1]
        if flag == "--config":
            configs.append(("config", value))
        elif flag == "--keyboard":
            keyboards.append(value)
        elif flag == "--getoption" and getoption is None:
            getoption = value
            configs.append(("getoption", value))
        else:
            raise Setup("usage")
        i += 2
    if not any(k == "config" for k, _ in configs):
        raise Setup("usage")
    return "run", configs, keyboards, getoption


def parse_value(value):
    """configStringToInt on the modelled tokens: int, or None when unsupported."""
    if value.startswith(("true", "on", "yes")):
        return 1
    if value.startswith(("false", "off", "no")):
        return 0
    if DIGITS_RE.fullmatch(value):
        digits = value.lstrip("0")
        return 10 ** 9 if len(digits) > 9 else int(digits or "0")  # huge: past every range
    return None


def model(texts):
    """-> (global dict, devices dict name -> dict, unsupported)."""
    glob, devices, unsupported = {}, {}, 0
    for text in texts:
        stack, current = [], None
        for raw in text.split("\n"):
            line = raw.strip(WS)
            if not line or line[0] == "#":
                continue
            if "=" not in line:
                if line == "}":
                    if stack:
                        stack.pop()
                    if not stack:
                        current = None
                elif line.endswith("{"):
                    stack.append(line[:-1].strip(WS))
                continue
            lhs, rhs = (s.strip(WS) for s in line.split("=", 1))
            if lhs.startswith("$") or lhs == "source":
                continue
            key = ":".join(stack + [lhs])
            in_device = stack == ["device"]
            if in_device and lhs == "name":
                current = rhs.split("#", 1)[0].strip(WS)
                devices.setdefault(current, {})
                continue
            if key in GLOBAL_KEYS:
                name, target = GLOBAL_KEYS[key], glob
            elif in_device and lhs in NAMES:
                name, target = lhs, None
            elif key.startswith("device[") and key.rsplit(":", 1)[-1] in NAMES:
                unsupported += 1
                continue
            else:
                continue
            if "$" in line or "{{" in line or "\\" in line or "##" in rhs:
                unsupported += 1
                continue
            val = parse_value(rhs.split("#", 1)[0].strip(WS))
            lo, hi = RANGE[name]
            if val is None or not lo <= val <= hi:
                unsupported += 1
                continue
            if target is None:
                if current is None:
                    unsupported += 1
                    continue
                target = devices[current]
            target[name] = val
    return glob, devices, unsupported


def live_records(data):
    """getoption bytes -> {option: int}; raises Setup('bad_json')."""
    def no_const(token):
        raise ValueError(token)
    live = {}
    for part in data.split(b"\n"):
        if not part:
            continue
        try:
            doc = json.loads(part.decode("utf-8"), parse_constant=no_const)
        except (UnicodeDecodeError, ValueError, RecursionError):
            raise Setup("bad_json")
        if not isinstance(doc, dict):
            raise Setup("bad_json")
        opt, val = doc.get("option"), doc.get("int")
        if isinstance(opt, str) and isinstance(val, int) and not isinstance(val, bool):
            live[opt] = val
    return live


def report(texts, keyboards, live):
    glob, devices, unsupported = model(texts)
    out = []
    names = keyboards if keyboards else ["*"]
    for kb in names:
        vals, frm = [], []
        for n in NAMES:
            if n in devices.get(kb, {}):
                vals.append(devices[kb][n])
                frm.append("D")
            elif n in glob:
                vals.append(glob[n])
                frm.append("G")
            else:
                vals.append(DEFAULT[n])
                frm.append("-")
        out.append("MADO_KBDOPT: keyboard=%s repeat_rate=%d repeat_delay=%d numlock=%d from=%s unsupported=%d"
                   % (kb, vals[0], vals[1], vals[2], "/".join(frm), unsupported))
    final = "NONE"
    if live is not None:
        verdicts = []
        for opt, n in zip(OPTIONS, NAMES):
            cfg = glob.get(n, DEFAULT[n])
            if opt in live:
                v = "AGREE" if live[opt] == cfg else "DIFFER"
                shown = str(live[opt])
            else:
                v, shown = "UNKNOWN", "?"
            verdicts.append(v)
            out.append("MADO_KBDOPT_LIVE: option=%s config=%d live=%s verdict=%s" % (opt, cfg, shown, v))
        final = "DIFFER" if "DIFFER" in verdicts else "UNKNOWN" if "UNKNOWN" in verdicts else "AGREE"
    out.append("MADO_KBDOPT: DONE keyboards=%d unsupported=%d live=%s" % (len(names), unsupported, final))
    return out


def run(argv):
    try:
        mode, files, keyboards, getoption = parse_args(argv)
        if mode == "selftest":
            return None, selftest()
        texts, gdata = [], None
        for kind, path in files:
            data = read_regular(path)
            if kind == "config":
                texts.append(data.decode("utf-8", "replace"))
            else:
                gdata = data
        live = live_records(gdata) if gdata is not None else None
        return report(texts, keyboards, live), 0
    except Setup as e:
        return ["MADO_KBDOPT: SETUP %s" % e], 2


def selftest():
    checks = []

    def rep(conf, kbs=(), live=None, confs=None):
        return report(confs if confs is not None else [conf], list(kbs), live)

    def eq(label, got, want):
        checks.append((label, got == want, got, want))

    eq("empty", rep("")[0], "MADO_KBDOPT: keyboard=* repeat_rate=25 repeat_delay=600 numlock=0 from=-/-/- unsupported=0")
    eq("global", rep("input {\n repeat_rate = 30\n}\n")[0],
       "MADO_KBDOPT: keyboard=* repeat_rate=30 repeat_delay=600 numlock=0 from=G/-/- unsupported=0")
    eq("flat key", rep("input:repeat_delay = 100\n")[0],
       "MADO_KBDOPT: keyboard=* repeat_rate=25 repeat_delay=100 numlock=0 from=-/G/- unsupported=0")
    dev = "input {\n repeat_rate = 30\n}\ndevice {\n name = a\n repeat_rate = 50\n}\n"
    eq("device wins", rep(dev, ["a"])[0],
       "MADO_KBDOPT: keyboard=a repeat_rate=50 repeat_delay=600 numlock=0 from=D/-/- unsupported=0")
    eq("other keyboard global", rep(dev, ["b"])[0],
       "MADO_KBDOPT: keyboard=b repeat_rate=30 repeat_delay=600 numlock=0 from=G/-/- unsupported=0")
    eq("repeated keyboard", len(rep(dev, ["a", "a"])), 3)
    eq("merge blocks", rep("device {\nname=a\nrepeat_rate=5\n}\ndevice {\nname = a\nrepeat_delay=7\n}\n", ["a"])[0],
       "MADO_KBDOPT: keyboard=a repeat_rate=5 repeat_delay=7 numlock=0 from=D/D/- unsupported=0")
    eq("later wins", rep("device {\nname=a\nrepeat_rate=5\nrepeat_rate=6\n}\n", ["a"])[0].split()[2], "repeat_rate=6")
    eq("key before name", rep("device {\nrepeat_rate=5\nname=a\n}\n", ["a"])[0][-24:], "from=-/-/- unsupported=1")
    eq("true/on/yes", [parse_value(v) for v in ("true", "on", "yes", "online", "yesterday")], [1] * 5)
    eq("false/off/no", [parse_value(v) for v in ("false", "off", "no", "nope", "offer")], [0] * 5)
    eq("digits", [parse_value(v) for v in ("0", "007", "200")], [0, 7, 200])
    eq("non tokens", [parse_value(v) for v in ("", "0x10", "+5", "-5", "1.5", "5a", "True", "١٢")], [None] * 8)
    eq("huge digits", rep("input:repeat_rate = " + "9" * 5000 + "\n")[0][-13:], "unsupported=1")
    eq("range hi", rep("input:repeat_rate = 201\n")[0][-13:], "unsupported=1")
    eq("range lo/hi ok", rep("input:repeat_rate = 0\ninput:repeat_delay = 2000\n")[0],
       "MADO_KBDOPT: keyboard=* repeat_rate=0 repeat_delay=2000 numlock=0 from=G/G/- unsupported=0")
    eq("numlock 2", rep("input:numlock_by_default = 2\n")[0][-13:], "unsupported=1")
    eq("variable", rep("input:repeat_rate = $r\n")[0][-13:], "unsupported=1")
    eq("dollar lhs ignored", rep("$repeat_rate = 5\n")[0][-13:], "unsupported=0")
    eq("braces", rep("input:repeat_rate = {{x}}\n")[0][-13:], "unsupported=1")
    eq("backslash", rep("input:repeat_rate = 3\\\n")[0][-13:], "unsupported=1")
    eq("double hash", rep("input:repeat_rate = 3##\n")[0][-13:], "unsupported=1")
    eq("comment cut", rep("input:repeat_rate = 33 # fast\n")[0].split()[2], "repeat_rate=33")
    eq("full-line comment", rep("# input:repeat_rate = 33\n")[0].split()[2], "repeat_rate=25")
    eq("bracket", rep("device[a]:repeat_rate = 5\n", ["a"])[0][-24:], "from=-/-/- unsupported=1")
    eq("bracket block", rep("device[a] {\nrepeat_delay = 5\n}\n", ["a"])[0][-13:], "unsupported=1")
    eq("nested block ignored", rep("device {\nname = a\ntouchpad {\nrepeat_rate = 5\n}\nrepeat_delay = 9\n}\n", ["a"])[0],
       "MADO_KBDOPT: keyboard=a repeat_rate=25 repeat_delay=9 numlock=0 from=-/D/- unsupported=0")
    eq("source ignored", rep("source = x.conf\ninput:repeat_rate = 5\n")[0].split()[2], "repeat_rate=5")
    eq("stack resets per file", rep(None, confs=["device {\nname = a\n", "device {\nrepeat_rate = 5\n}\n"])[0][-13:],
       "unsupported=1")
    eq("files accumulate", rep(None, confs=["input:repeat_rate = 5\n", "input:repeat_delay = 6\n"])[0],
       "MADO_KBDOPT: keyboard=* repeat_rate=5 repeat_delay=6 numlock=0 from=G/G/- unsupported=0")
    eq("crlf tabs", rep("input {\r\n\trepeat_rate\t=\t30\r\n}\r\n")[0].split()[2], "repeat_rate=30")
    eq("name comment cut", rep("device {\nname = a # c\nrepeat_rate=5\n}\n", ["a"])[0].split()[2], "repeat_rate=5")
    eq("first = splits", rep("input:repeat_rate = =5\n")[0][-13:], "unsupported=1")
    eq("extra close", rep("}\n}\ninput:repeat_rate = 5\n")[0].split()[2], "repeat_rate=5")
    live = live_records(b'{"option":"input:repeat_rate","int":40}\n\n{"option":"x","int":1}\n')
    eq("live parse", live, {"input:repeat_rate": 40, "x": 1})
    eq("live later wins", live_records(b'{"option":"a","int":1}\n{"option":"a","int":2}\n'), {"a": 2})
    eq("live ignores bool/float/missing",
       live_records(b'{"option":"a","int":true}\n{"option":"b","int":1.5}\n{"option":3,"int":1}\n{}\n'), {})
    for label, data in (("array", b"[]"), ("garbage", b"{not"), ("scalar", b"5"), ("nan", b'{"int":NaN}'),
                        ("bad utf8", b'{"a":"\xff"}'), ("deep", b"[" * 100000)):
        try:
            live_records(data)
            checks.append(("bad_json " + label, False, "no error", "bad_json"))
        except Setup as e:
            eq("bad_json " + label, str(e), "bad_json")
    tail = rep("input:repeat_rate = 25\n", live={"input:repeat_rate": 25, "input:repeat_delay": 600,
                                               "input:numlock_by_default": 0})
    eq("agree", (tail[-1], tail[1]),
       ("MADO_KBDOPT: DONE keyboards=1 unsupported=0 live=AGREE",
        "MADO_KBDOPT_LIVE: option=input:repeat_rate config=25 live=25 verdict=AGREE"))
    tail = rep("", live={"input:repeat_rate": 26})
    eq("differ beats unknown", tail[-1], "MADO_KBDOPT: DONE keyboards=1 unsupported=0 live=DIFFER")
    eq("unknown line", tail[2], "MADO_KBDOPT_LIVE: option=input:repeat_delay config=600 live=? verdict=UNKNOWN")
    for argv, reason in (([], "usage"), (["--config"], "usage"), (["--keyboard", "a"], "usage"),
                         (["--config", "x", "--bogus", "y"], "usage"), (["--config=x"], "usage"),
                         (["--config", "/nonexistent/x", "--getoption", "a", "--getoption", "b"], "usage"),
                         (["--selftest", "--config", "x"], "usage"),
                         (["--config", "/nonexistent/x"], "unreadable"), (["--config", "/"], "unreadable"),
                         (["--config", "/nonexistent/x", "--getoption", "/nonexistent/y"], "unreadable")):
        lines, rc = run(argv)
        eq("setup " + reason + " " + " ".join(argv), (lines, rc), (["MADO_KBDOPT: SETUP " + reason], 2))
    passed = sum(1 for c in checks if c[1])
    for label, ok, got, want in checks:
        if not ok:
            print("MADO_KBDOPT_SELFTEST: FAIL %s got=%r want=%r" % (label, got, want))
    print("MADO_KBDOPT_SELFTEST: %d/%d assertions passed" % (passed, len(checks)))
    return 0 if passed == len(checks) else 1


def main():
    lines, rc = run(sys.argv[1:])
    if lines is not None:
        sys.stdout.buffer.write("".join(l + "\n" for l in lines).encode("utf-8", "surrogateescape"))
        sys.stdout.buffer.flush()
    return rc


if __name__ == "__main__":
    sys.exit(main())
