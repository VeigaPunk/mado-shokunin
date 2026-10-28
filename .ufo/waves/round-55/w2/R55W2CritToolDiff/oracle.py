#!/usr/bin/env python3
"""Independent oracle for registration.md §C2 as amended by registration-v2.md E7.

Written from the contract text only (no reading of tools/mado-kbdopts.py).
Usage: python3 -I oracle.py ARGV...   (argv exactly as the tool would receive, paths relative to cwd)
Prints the exact expected stdout and exits with the expected rc.
"""
import json
import os
import re
import stat
import sys

# Python 3.11+ caps int<->str conversion at 4300 digits; the contract has no such cap (an
# integer literal of any length is an integer), so lift the cap for getoption JSON integers.
sys.set_int_max_str_digits(0)

WS = " \t\r\n\x0b\x0c"  # the contract's strip set: space, tab, CR, LF, VT, FF
MAX_BYTES = 1048576
OPTS = ("input:repeat_rate", "input:repeat_delay", "input:numlock_by_default")
NAMES = ("repeat_rate", "repeat_delay", "numlock_by_default")
DEFAULT = {"repeat_rate": 25, "repeat_delay": 600, "numlock_by_default": 0}
RANGE = {"repeat_rate": (0, 200), "repeat_delay": (0, 2000), "numlock_by_default": (0, 1)}


class Setup(Exception):
    def __init__(self, reason):
        super().__init__(reason)
        self.reason = reason


class Usage(Exception):
    pass


def parse_args(argv):
    configs, kbs, gopt = [], [], None
    i = 0
    while i < len(argv):
        a = argv[i]
        if a in ("--config", "--keyboard", "--getoption"):
            if i + 1 >= len(argv):
                raise Usage()
            v = argv[i + 1]
            if a == "--config":
                configs.append(v)
            elif a == "--keyboard":
                kbs.append(v)
            else:
                if gopt is not None:
                    raise Usage()
                gopt = v
            i += 2
        else:
            raise Usage()
    if not configs:
        raise Usage()
    return configs, kbs, gopt


def read_file(path):
    try:
        st = os.stat(path)
    except OSError:
        raise Setup("unreadable")
    if not stat.S_ISREG(st.st_mode):
        raise Setup("unreadable")
    try:
        with open(path, "rb") as f:
            data = f.read(MAX_BYTES + 1)
    except OSError:
        raise Setup("unreadable")
    if len(data) > MAX_BYTES:
        raise Setup("too_large")
    return data


def parse_value(s):
    """configStringToInt as the contract describes it. None = unsupported."""
    if s.startswith("true") or s.startswith("on") or s.startswith("yes"):
        return 1
    if s.startswith("false") or s.startswith("off") or s.startswith("no"):
        return 0
    if s and all(c in "0123456789" for c in s):
        t = s.lstrip("0")
        if len(t) > 9:  # mathematically huge: out of every range; avoid int() digit limits
            return 10 ** 9
        return int(t) if t else 0
    return None


def is_int_json_object_line(line):
    """Return the parsed object or raise Setup('bad_json')."""
    def bad_const(_):
        raise ValueError("nonstandard constant")
    try:
        obj = json.loads(line, parse_constant=bad_const)
    except (ValueError, RecursionError):
        raise Setup("bad_json")
    if not isinstance(obj, dict):
        raise Setup("bad_json")
    return obj


def run(argv):
    """Returns (stdout_text, rc)."""
    try:
        configs, kbs, gopt = parse_args(argv)
    except Usage:
        return "MADO_KBDOPT: SETUP usage\n", 2
    try:
        texts = []
        for p in configs:
            texts.append(read_file(p).decode("utf-8", errors="replace"))
        gdata = read_file(gopt) if gopt is not None else None
        objs = []
        if gdata is not None:
            gtext = gdata.decode("utf-8", errors="replace")
            for raw in gtext.split("\n"):
                if raw == "":
                    continue
                objs.append(is_int_json_object_line(raw))
    except Setup as s:
        return f"MADO_KBDOPT: SETUP {s.reason}\n", 2

    glob = {}            # option name -> value (input: keys)
    dev = {}             # device name -> {option name -> value}
    unsup = 0
    for text in texts:
        stack = []
        cur = None
        for raw in text.split("\n"):
            line = raw.strip(WS)
            if line == "" or line[0] == "#":
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
            lhs_raw, rhs_raw = line.split("=", 1)
            lhs = lhs_raw.strip(WS)
            rhs = rhs_raw.strip(WS)
            if lhs.startswith("$") or lhs == "source":
                continue
            key = lhs if not stack else ":".join(stack) + ":" + lhs
            if stack == ["device"] and lhs == "name":
                cur = rhs.split("#", 1)[0].strip(WS)
                dev.setdefault(cur, {})
                continue
            relevant = (
                key in OPTS
                or (stack == ["device"] and lhs in NAMES)
                or (key.startswith("device[") and key.rsplit(":", 1)[-1] in NAMES)
            )
            if not relevant:
                continue
            if key.startswith("device["):
                unsup += 1
                continue
            if "$" in line or "{{" in line or "\\" in line:
                unsup += 1
                continue
            if "##" in rhs:
                unsup += 1
                continue
            val = parse_value(rhs.split("#", 1)[0].strip(WS))
            if val is None:
                unsup += 1
                continue
            name = key.rsplit(":", 1)[-1]
            lo, hi = RANGE[name]
            if not (lo <= val <= hi):
                unsup += 1
                continue
            if stack == ["device"]:
                if cur is None:
                    unsup += 1
                    continue
                dev[cur][name] = val
            else:
                glob[name] = val

    def eff(kb, name):
        if kb in dev and name in dev[kb]:
            return dev[kb][name], "D"
        if name in glob:
            return glob[name], "G"
        return DEFAULT[name], "-"

    out = []
    names = kbs if kbs else ["*"]
    for kb in names:
        r, fr = eff(kb, "repeat_rate")
        d, fd = eff(kb, "repeat_delay")
        n, fn = eff(kb, "numlock_by_default")
        out.append(
            f"MADO_KBDOPT: keyboard={kb} repeat_rate={r} repeat_delay={d} numlock={n} "
            f"from={fr}/{fd}/{fn} unsupported={unsup}"
        )
    live_state = "NONE"
    if gopt is not None:
        recs = {}
        for obj in objs:
            o = obj.get("option")
            v = obj.get("int")
            if isinstance(o, str) and type(v) is int:
                recs[o] = v
        verdicts = []
        for opt in OPTS:
            nm = opt.split(":", 1)[1]
            cfg = glob.get(nm, DEFAULT[nm])
            if opt in recs:
                live = str(recs[opt])
                v = "AGREE" if recs[opt] == cfg else "DIFFER"
            else:
                live = "?"
                v = "UNKNOWN"
            verdicts.append(v)
            out.append(f"MADO_KBDOPT_LIVE: option={opt} config={cfg} live={live} verdict={v}")
        if "DIFFER" in verdicts:
            live_state = "DIFFER"
        elif "UNKNOWN" in verdicts:
            live_state = "UNKNOWN"
        else:
            live_state = "AGREE"
    out.append(f"MADO_KBDOPT: DONE keyboards={len(names)} unsupported={unsup} live={live_state}")
    return "\n".join(out) + "\n", 0


if __name__ == "__main__":
    text, rc = run(sys.argv[1:])
    sys.stdout.write(text)
    sys.exit(rc)
