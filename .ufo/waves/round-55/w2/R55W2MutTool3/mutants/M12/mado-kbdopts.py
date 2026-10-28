#!/usr/bin/env python3
"""mado-kbdopts - which key-repeat rate, repeat delay and numlock default does a keyboard get from this Hyprland config, and does `hyprctl getoption` agree?

Hyprland 0.56.2 (efb50993) applies three keyboard settings per device (src/managers/input/InputManager.cpp
applyConfigToKeyboard stores `std::max(0, REPEATRATE)` and `std::max(0, REPEATDELAY)` on the keyboard, :1282-1283): for
each of repeat_rate, repeat_delay and numlock_by_default it reads the value of the `device` block whose name equals the
keyboard's name when that block SETS the key, else the global `input:` option (src/config/legacy/ConfigManager.cpp
getConfigValueSafeDevice, :1115-1123: the device value is used when `m_bSetByUser`, else the fallback option). The
built-in defaults are 25, 600 and false (src/config/values/ConfigValues.cpp:277-280); the declared ranges 0..200 and
0..2000 are the table's own `.min`/`.max` (:279-280), while the 0..1 range this tool applies to numlock_by_default is
the lane's modelling rule, not a source range (the option is declared Bool without min/max at :277). Which pinned
Hyprland site enforces a range is not shown by the pins this round, so an out-of-range value is `unsupported` here, never
guessed. An integer or boolean option value is read by hyprlang 0.6.8 configStringToInt (hyprlang-config.cpp:259-262,
round-46 pin): a value starting `true`, `on` or `yes` is 1 (checked first), one starting `false`, `off` or `no` is 0,
else decimal digits. This tool models that for config text a caller supplies and joins the result to the JSON that
`hyprctl getoption <opt> -j` prints (one object per line: {"option": ..., "int": ..., "set": ...}).

Read-only: it reads only the files named by --config and --getoption, starts no process, opens no socket and writes
nothing. Arguments (two-token form only; anything else, including no --config, is usage):
  --config PATH     one or more times; files are read in argument order
  --keyboard NAME   zero or more times; the keyboard names to evaluate (none: one line with NAME `*`); a NAME holding a
                    control byte (below 0x20 or 0x7f) is usage, so it cannot forge an output line
  --getoption PATH  at most once; the output of the three `hyprctl getoption ... -j` calls, one JSON object per line
  --selftest        alone: runs the tool's own assertions, prints MADO_KBDOPT_SELFTEST: N/N assertions passed

Config model (a deliberate subset of hyprlang 0.6.8 as Hyprland 0.56.2 reads it; everything outside it is
`unsupported`, never guessed). Each file is decoded as UTF-8 with errors replaced and split on `\\n`; the category stack
and the current device reset at each file's start. A raw line is stripped of space, tab, CR, LF, VT and FF; an empty line
or one starting with `#` is skipped. A line without `=`: exactly `}` pops the stack (an empty stack stays empty; when the
stack empties the current device is forgotten); a line ending in `{` pushes its text before the `{` (stripped);
anything else is ignored. A line with `=`: LHS and RHS are the stripped texts before and after the FIRST `=`; an LHS
starting with `$` and an LHS equal to `source` are ignored; KEY is the stack joined with `:` then `:` then LHS (just
LHS when the stack is empty). A line is RELEVANT when its KEY is `input:repeat_rate`, `input:repeat_delay` or
`input:numlock_by_default`; or the stack is exactly ["device"] and LHS is one of the three names; or KEY starts with
`device[` and its last `:`-separated component is one of the three names. With the stack exactly ["device"] and LHS
`name`, the current device becomes RHS with a trailing `#` comment cut and stripped (created if absent; a second
block of the same name merges, later keys win). Any other line is ignored. For a RELEVANT line the checks run in
order and the first failure adds one to `unsupported` and ends the line: a KEY starting with `device[` (bracket forms
are not modelled); a line containing `$`, `{{` or a backslash; an RHS containing `##`. Otherwise the RHS is cut at its
first `#` and stripped to VALUE, which parses as configStringToInt: starts with true/on/yes -> 1, else starts with
false/off/no -> 0, else all of `[0-9]+` -> that integer, else (hex, sign, float, empty, words) unsupported +1 and the
line is ignored. Ranges: repeat_rate 0..200, repeat_delay 0..2000, numlock_by_default 0..1; outside -> unsupported +1,
line ignored. A device-block key line with no current device -> unsupported +1, ignored. An `input:` KEY sets the
GLOBAL value; a device key sets the CURRENT device's value. Effective value for keyboard NAME: the device value if set
for NAME, else the global if set, else the default; `from` letters D / G / - say which.

Output (stdout; nothing else), keyboard lines in --keyboard argument order (repeats printed per argument):
  MADO_KBDOPT: keyboard=<NAME|*> repeat_rate=<n> repeat_delay=<n> numlock=<0|1> from=<x>/<y>/<z> unsupported=<U>
With --getoption, one line per option in the order input:repeat_rate, input:repeat_delay, input:numlock_by_default:
  MADO_KBDOPT_LIVE: option=<opt> config=<global effective value, default if unset> live=<int|?> verdict=<AGREE|DIFFER|UNKNOWN>
(each non-empty --getoption line must be a JSON object; an object with a string `option` and an integer, not boolean,
`int` records that option's live value, a later line for the same option wins, other objects are ignored; no record
-> live=? UNKNOWN), then
  MADO_KBDOPT: DONE keyboards=<n> unsupported=<U> live=<NONE|AGREE|DIFFER|UNKNOWN>
(NONE without --getoption; else DIFFER if any DIFFER, else UNKNOWN if any UNKNOWN, else AGREE). Exit 0 on a completed
run. Setup failure: stdout exactly `MADO_KBDOPT: SETUP <reason>`, exit 2, reason usage | unreadable (missing,
unreadable, directory, FIFO or other non-regular path) | too_large (a file over 1048576 bytes) | bad_json (a non-empty
--getoption line that is not a JSON object).

Declared limit: values outside the modelled token set are `unsupported`, never guessed; the tool models source-level
semantics and does not observe a keypress or a running compositor.
"""
import json
import os
import re
import stat
import sys

MAX_BYTES = 1048576
WS = " \t\r\n\v\f"
NAMES = ("repeat_rate", "repeat_delay", "numlock_by_default")
OPTIONS = tuple("input:" + n for n in NAMES)
DEFAULTS = {"repeat_rate": 25, "repeat_delay": 600, "numlock_by_default": 0}
MAXIMA = {"repeat_rate": 200, "repeat_delay": 2000, "numlock_by_default": 1}
DIGITS_RE = re.compile(r"[0-9]+")

if hasattr(sys, "set_int_max_str_digits"):
    sys.set_int_max_str_digits(0)


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
    """-> ('selftest', None) | ('run', (steps, keyboards, has_getoption)); steps is the argument-order read list."""
    if argv == ["--selftest"]:
        return "selftest", None
    steps, keyboards, getoption, i = [], [], False, 0
    while i < len(argv):
        if i + 1 >= len(argv):
            raise Setup("usage")
        flag, value = argv[i], argv[i + 1]
        if flag == "--config":
            steps.append(("config", value))
        elif flag == "--keyboard":
            if any(ord(c) < 32 or ord(c) == 127 for c in value):
                raise Setup("usage")  # a control byte in NAME could forge an output line; the contract is silent, this is an extension
            keyboards.append(value)
        elif flag == "--getoption" and not getoption:
            getoption = True
            steps.append(("getoption", value))
        else:
            raise Setup("usage")
        i += 2
    if not any(kind == "config" for kind, _ in steps):
        raise Setup("usage")
    return "run", (steps, keyboards, getoption)


def parse_value(rhs):
    """hyprlang configStringToInt on the RHS of a modelled key: int or None (unsupported)."""
    if rhs.startswith(("true", "on", "yes")):
        return 1
    if rhs.startswith(("false", "off", "no")):
        return 0
    if DIGITS_RE.fullmatch(rhs):
        digits = rhs.lstrip("0")
        return int(digits or "0") if len(digits) <= 6 else 10 ** 6
    return None


class State:
    def __init__(self):
        self.glob = {}
        self.devices = {}
        self.unsupported = 0


def parse_config(text, st):
    stack, cur = [], None
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
        lhs, rhs = (s.strip(WS) for s in line.rsplit("=", 1))
        if lhs.startswith("$") or lhs == "source":
            continue
        key = ":".join(stack + [lhs])
        in_device = stack == ["device"]
        if in_device and lhs == "name":
            cur = rhs.split("#", 1)[0].strip(WS)
            st.devices.setdefault(cur, {})
            continue
        bracket = key.startswith("device[")
        relevant = (
            key in OPTIONS
            or (in_device and lhs in NAMES)
            or (bracket and key.rsplit(":", 1)[-1] in NAMES)
        )
        if not relevant:
            continue
        if bracket or "$" in line or "{{" in line or "\\" in line or "##" in rhs:
            st.unsupported += 1
            continue
        value = parse_value(rhs.split("#", 1)[0].strip(WS))
        name = key.rsplit(":", 1)[-1]
        if value is None or value > MAXIMA[name]:
            st.unsupported += 1
            continue
        if key in OPTIONS:
            st.glob[name] = value
        elif cur is None:
            st.unsupported += 1
        else:
            st.devices[cur][name] = value


def effective(st, keyboard):
    vals, frm = [], []
    dev = st.devices.get(keyboard, {})
    for n in NAMES:
        if n in dev:
            vals.append(dev[n])
            frm.append("D")
        elif n in st.glob:
            vals.append(st.glob[n])
            frm.append("G")
        else:
            vals.append(DEFAULTS[n])
            frm.append("-")
    return vals, frm


def parse_getoption(text):
    live = {}
    for raw in text.split("\n"):
        line = raw.strip(WS)
        if not line:
            continue

        def reject(_):
            raise ValueError("non-JSON constant")

        try:
            obj = json.loads(line, parse_constant=reject)
        except (ValueError, RecursionError):
            raise Setup("bad_json")
        if not isinstance(obj, dict):
            raise Setup("bad_json")
        opt, val = obj.get("option"), obj.get("int")
        if isinstance(opt, str) and isinstance(val, int) and not isinstance(val, bool):
            live[opt] = val
    return live


def report(configs, getoption_text, keyboards):
    st = State()
    for text in configs:
        parse_config(text, st)
    live = parse_getoption(getoption_text) if getoption_text is not None else None
    names = keyboards or ["*"]
    out = []
    for kb in names:
        vals, frm = effective(st, kb)
        out.append("MADO_KBDOPT: keyboard=%s repeat_rate=%d repeat_delay=%d numlock=%d from=%s unsupported=%d"
                   % (kb, vals[0], vals[1], vals[2], "/".join(frm), st.unsupported))
    overall = "NONE"
    if live is not None:
        gvals, _ = effective(st, None)
        verdicts = []
        for opt, cfg in zip(OPTIONS, gvals):
            if opt in live:
                v = "AGREE" if live[opt] == cfg else "DIFFER"
                shown = str(live[opt])
            else:
                v, shown = "UNKNOWN", "?"
            verdicts.append(v)
            out.append("MADO_KBDOPT_LIVE: option=%s config=%d live=%s verdict=%s" % (opt, cfg, shown, v))
        overall = "DIFFER" if "DIFFER" in verdicts else "UNKNOWN" if "UNKNOWN" in verdicts else "AGREE"
    out.append("MADO_KBDOPT: DONE keyboards=%d unsupported=%d live=%s" % (len(names), st.unsupported, overall))
    return out


def selftest():
    def run(conf, kbs=(), opt=None, files=None):
        return report(conf if isinstance(conf, list) else [conf], opt, list(kbs))

    def line(conf, kb=None, **kw):
        return run(conf, [kb] if kb else [], **kw)[0]

    def ok(conf, rate, delay, num, frm, unsup=0, kb=None):
        want = ("MADO_KBDOPT: keyboard=%s repeat_rate=%d repeat_delay=%d numlock=%d from=%s unsupported=%d"
                % (kb or "*", rate, delay, num, frm, unsup))
        return line(conf, kb) == want

    def refused(argv, reason="usage"):
        try:
            parse_args(argv)
        except Setup as e:
            return str(e) == reason
        return False

    def bad_json(text):
        try:
            parse_getoption(text)
        except Setup as e:
            return str(e) == "bad_json"
        return False

    cases = [
        ("defaults on empty config", ok("", 25, 600, 0, "-/-/-")),
        ("global in input block", ok("input {\n repeat_rate = 30\n}\n", 30, 600, 0, "G/-/-")),
        ("flat input: key at empty stack", ok("input:repeat_delay = 300\n", 25, 300, 0, "-/G/-")),
        ("device beats global", ok("input {\nrepeat_rate = 30\n}\ndevice {\nname = a\nrepeat_rate = 50\n}\n", 50, 600, 0, "D/-/-", kb="a")),
        ("other keyboard gets global", ok("input {\nrepeat_rate = 30\n}\ndevice {\nname = a\nrepeat_rate = 50\n}\n", 30, 600, 0, "G/-/-", kb="b")),
        ("later global wins", ok("input {\nrepeat_rate = 30\nrepeat_rate = 31\n}\n", 31, 600, 0, "G/-/-")),
        ("same-name device blocks merge", ok("device {\nname = a\nrepeat_rate = 50\n}\ndevice {\nname = a\nrepeat_delay = 100\n}\n", 50, 100, 0, "D/D/-", kb="a")),
        ("device name cut at comment", ok("device {\nname = a # kbd\nrepeat_rate = 50\n}\n", 50, 600, 0, "D/-/-", kb="a")),
        ("true prefix", ok("input:numlock_by_default = true\n", 25, 600, 1, "-/-/G")),
        ("yes prefix (word start)", ok("input:numlock_by_default = yesterday\n", 25, 600, 1, "-/-/G")),
        ("on prefix", ok("input:numlock_by_default = online\n", 25, 600, 1, "-/-/G")),
        ("no prefix is zero", ok("input:numlock_by_default = nope\n", 25, 600, 0, "-/-/G")),
        ("off is zero", ok("input:numlock_by_default = off\n", 25, 600, 0, "-/-/G")),
        ("digits one", ok("input:numlock_by_default = 1\n", 25, 600, 1, "-/-/G")),
        ("leading zeros read as decimal", ok("input:repeat_rate = 007\n", 7, 600, 0, "G/-/-")),
        ("numlock 2 out of range", ok("input:numlock_by_default = 2\n", 25, 600, 0, "-/-/-", 1)),
        ("rate bounds 0 and 200", ok("input:repeat_rate = 0\n", 0, 600, 0, "G/-/-") and ok("input:repeat_rate = 200\n", 200, 600, 0, "G/-/-")),
        ("rate 201 out of range", ok("input:repeat_rate = 201\n", 25, 600, 0, "-/-/-", 1)),
        ("delay 2001 out of range", ok("input:repeat_delay = 2001\n", 25, 600, 0, "-/-/-", 1)),
        ("huge digit run is out of range, not a crash", ok("input:repeat_rate = " + "9" * 5000 + "\n", 25, 600, 0, "-/-/-", 1)),
        ("hex unsupported", ok("input:repeat_rate = 0x10\n", 25, 600, 0, "-/-/-", 1)),
        ("sign unsupported", ok("input:repeat_rate = +10\n", 25, 600, 0, "-/-/-", 1)),
        ("float unsupported", ok("input:repeat_rate = 1.5\n", 25, 600, 0, "-/-/-", 1)),
        ("trailing text after digits unsupported", ok("input:repeat_rate = 30abc\n", 25, 600, 0, "-/-/-", 1)),
        ("empty value unsupported", ok("input:repeat_rate =\n", 25, 600, 0, "-/-/-", 1)),
        ("inline comment cut", ok("input:repeat_rate = 33 # fast\n", 33, 600, 0, "G/-/-")),
        ("## unsupported", ok("input:repeat_rate = 4##0\n", 25, 600, 0, "-/-/-", 1)),
        ("variable use unsupported", ok("input:repeat_rate = $r\n", 25, 600, 0, "-/-/-", 1)),
        ("backslash unsupported", ok("input:repeat_rate = 3\\0\n", 25, 600, 0, "-/-/-", 1)),
        ("double brace unsupported", ok("input:repeat_rate = {{x}}\n", 25, 600, 0, "-/-/-", 1)),
        ("$ in a trailing comment still unsupported", ok("input:repeat_rate = 30 # $x\n", 25, 600, 0, "-/-/-", 1)),
        ("variable definition ignored", ok("$r = 5\ninput:repeat_rate = 30\n", 30, 600, 0, "G/-/-")),
        ("source line ignored", ok("source = x.conf\n", 25, 600, 0, "-/-/-")),
        ("bracket form unsupported", ok("device[a]:repeat_rate = 70\n", 25, 600, 0, "-/-/-", 1, kb="a")),
        ("bracket block unsupported", ok("device[a] {\nrepeat_delay = 100\n}\n", 25, 600, 0, "-/-/-", 1, kb="a")),
        ("bracket irrelevant key ignored", ok("device[a]:sensitivity = 1\n", 25, 600, 0, "-/-/-", 0, kb="a")),
        ("device key before name unsupported", ok("device {\nrepeat_rate = 50\nname = a\n}\n", 25, 600, 0, "-/-/-", 1, kb="a")),
        ("nested block key not a device key", ok("device {\nname = a\ntouchpad {\nrepeat_rate = 50\n}\n}\n", 25, 600, 0, "-/-/-", 0, kb="a")),
        ("device retained after nested block closes", ok("device {\nname = a\ntouchpad {\n}\nrepeat_rate = 50\n}\n", 50, 600, 0, "D/-/-", 0, kb="a")),
        ("device forgotten after block", ok("device {\nname = a\n}\ndevice {\nrepeat_rate = 50\n}\n", 25, 600, 0, "-/-/-", 1, kb="a")),
        ("device state resets per file but devices persist", ok(["device {\nname = a\nrepeat_rate = 50\n}\n", "device {\nrepeat_delay = 9\n}\n"], 50, 600, 0, "D/-/-", 1, kb="a")),
        ("later file overrides global", ok(["input:repeat_rate = 30\n", "input:repeat_rate = 45\n"], 45, 600, 0, "G/-/-")),
        ("category stack resets per file", ok(["input {\n", "repeat_rate = 30\n"], 25, 600, 0, "-/-/-")),
        ("CRLF and tabs", ok("input {\r\n\trepeat_rate\t=\t30\t\r\n}\r\n", 30, 600, 0, "G/-/-")),
        ("trailing line without newline", ok("input {\nrepeat_rate = 30\n}\ninput:repeat_delay = 100", 30, 100, 0, "G/G/-")),
        ("extra } underflow is a no-op", ok("}\n}\ninput:repeat_rate = 30\n", 30, 600, 0, "G/-/-")),
        ("underflow keeps later blocks working", ok("}\ninput {\nrepeat_rate = 31\n}\n", 31, 600, 0, "G/-/-")),
        ("non-UTF-8 bytes replaced, later lines still parse", ok(b"# \xff\xfe\ninput:repeat_rate = 30\n".decode("utf-8", errors="replace"), 30, 600, 0, "G/-/-")),
        ("comment line skipped", ok("# input:repeat_rate = 99\n", 25, 600, 0, "-/-/-")),
        ("indented comment skipped", ok("   # input:repeat_rate = 99\n", 25, 600, 0, "-/-/-")),
        ("no `=` and not brace ignored", ok("input:repeat_rate\n", 25, 600, 0, "-/-/-")),
        ("`{` with trailing comment not a push", ok("input { # c\nrepeat_rate = 30\n}\n", 25, 600, 0, "-/-/-")),
        ("no keyboard prints *", line("") .startswith("MADO_KBDOPT: keyboard=* ")),
        ("repeated --keyboard prints per argument", len(run("", ["a", "a"])) == 3),
        ("unsupported count on every line", all(l.endswith("unsupported=1") for l in run("input:repeat_rate = x\n", ["a", "b"])[:2])),
        ("live AGREE", run("input:repeat_rate = 40\n", opt='{"option":"input:repeat_rate","int":40}\n')[1] == "MADO_KBDOPT_LIVE: option=input:repeat_rate config=40 live=40 verdict=AGREE"),
        ("live DIFFER", run("", opt='{"option":"input:repeat_rate","int":40}\n')[1].endswith("verdict=DIFFER")),
        ("live UNKNOWN when absent", run("", opt="")[2] == "MADO_KBDOPT_LIVE: option=input:repeat_delay config=600 live=? verdict=UNKNOWN"),
        ("live later line wins", run("", opt='{"option":"input:repeat_rate","int":1}\n{"option":"input:repeat_rate","int":25}\n')[1].endswith("live=25 verdict=AGREE")),
        ("live boolean int ignored", run("", opt='{"option":"input:repeat_rate","int":true}\n')[1].endswith("live=? verdict=UNKNOWN")),
        ("live float int ignored", run("", opt='{"option":"input:repeat_rate","int":25.0}\n')[1].endswith("live=? verdict=UNKNOWN")),
        ("live non-string option ignored", run("", opt='{"option":5,"int":25}\n')[1].endswith("live=? verdict=UNKNOWN")),
        ("live blank lines skipped", run("", opt='\n\n{"option":"input:repeat_rate","int":25}\n  \n')[1].endswith("verdict=AGREE")),
        ("live overall DIFFER beats UNKNOWN", run("", opt='{"option":"input:repeat_rate","int":1}\n')[-1] == "MADO_KBDOPT: DONE keyboards=1 unsupported=0 live=DIFFER"),
        ("live overall AGREE", run("", opt='{"option":"input:repeat_rate","int":25}\n{"option":"input:repeat_delay","int":600}\n{"option":"input:numlock_by_default","int":0}\n')[-1].endswith("live=AGREE")),
        ("live NONE without getoption", run("")[-1].endswith("live=NONE")),
        ("live compares the global, not a device", run("device {\nname = a\nrepeat_rate = 50\n}\n", ["a"], opt='{"option":"input:repeat_rate","int":25}\n')[1].endswith("config=25 live=25 verdict=AGREE")),
        ("bad_json on garbage", bad_json("{not json\n")),
        ("bad_json on JSON array", bad_json("[1]\n")),
        ("bad_json on NaN constant", bad_json('{"int": NaN}\n')),
        ("huge live int prints without crash", run("", opt='{"option":"input:repeat_rate","int":' + "9" * 5000 + "}\n")[1].endswith("verdict=DIFFER")),
        ("usage: no args", refused([])),
        ("usage: no --config", refused(["--keyboard", "a"])),
        ("usage: dangling flag", refused(["--config"])),
        ("usage: = form", refused(["--config=x"])),
        ("usage: two --getoption", refused(["--config", "a", "--getoption", "b", "--getoption", "c"])),
        ("usage: unknown flag", refused(["--config", "a", "--bogus", "b"])),
        ("usage: control byte in --keyboard NAME", refused(["--config", "a", "--keyboard", "x\ny"])),
        ("usage: --selftest with others", refused(["--selftest", "--config", "a"])),
        ("--selftest alone", parse_args(["--selftest"]) == ("selftest", None)),
        ("any argument order", parse_args(["--keyboard", "k", "--getoption", "g", "--config", "c"]) == ("run", ([("getoption", "g"), ("config", "c")], ["k"], True))),
        ("unreadable: missing path", _unreadable("/nonexistent/mado-kbdopts-selftest")),
        ("unreadable: directory", _unreadable(os.path.dirname(os.path.abspath(__file__)))),
    ]
    passed = sum(1 for _, ok_ in cases if ok_)
    for name, ok_ in cases:
        if not ok_:
            sys.stderr.write("selftest FAIL: %s\n" % name)
    print("MADO_KBDOPT_SELFTEST: %d/%d assertions passed" % (passed, len(cases)))
    return 0 if passed == len(cases) else 1


def _unreadable(path):
    try:
        read_regular(path)
    except Setup as e:
        return str(e) == "unreadable"
    return False


def run_cli(argv):
    try:
        mode, args = parse_args(argv)
        if mode == "selftest":
            return None, selftest()
        steps, keyboards, has_getoption = args
        configs, getoption_text = [], None
        for kind, path in steps:
            text = read_regular(path).decode("utf-8", errors="replace")
            if kind == "config":
                configs.append(text)
            else:
                getoption_text = text
        return report(configs, getoption_text, keyboards), 0
    except Setup as e:
        return ["MADO_KBDOPT: SETUP %s" % e], 2


def main():
    argv = [a for a in sys.argv[1:]]
    lines, rc = run_cli(argv)
    if lines is not None:
        sys.stdout.buffer.write("".join(l + "\n" for l in lines).encode("utf-8", errors="surrogateescape"))
        sys.stdout.buffer.flush()
    return rc


if __name__ == "__main__":
    sys.exit(main())
