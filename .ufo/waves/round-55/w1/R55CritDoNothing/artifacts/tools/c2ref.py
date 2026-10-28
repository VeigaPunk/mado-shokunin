#!/usr/bin/env python3
"""Seat-written reference for tools/mado-kbdopts.py, built from registration.md §C2 text (not from any wave file).
Variants (for the do-nothing controls; `full` is the reference):
  full    : the modelled grammar as frozen.
  global  : global values only. Device blocks are not parsed at all; every keyboard gets global/default, from=G/- only.
  nodev   : ignores device blocks by skipping their bodies by brace depth; no device state, no device unsupported counts.
Usage: c2ref.py [--variant full|global|nodev] --config PATH [--config PATH ...] [--keyboard NAME ...] [--getoption PATH]
"""
import json, os, re, stat, sys

VARIANT = "full"
LIMIT = 1048576
OPTS = ["input:repeat_rate", "input:repeat_delay", "input:numlock_by_default"]
NAMES = ["repeat_rate", "repeat_delay", "numlock_by_default"]
RANGE = {"repeat_rate": (0, 200), "repeat_delay": (0, 2000), "numlock_by_default": (0, 1)}
DEFAULT = {"repeat_rate": 25, "repeat_delay": 600, "numlock_by_default": 0}


def setup(reason):
    sys.stdout.write(f"MADO_KBDOPT: SETUP {reason}\n")
    sys.exit(2)


def parse_args(argv):
    cfgs, kbs, gos = [], [], []
    i = 0
    while i < len(argv):
        t = argv[i]
        if t not in ("--config", "--keyboard", "--getoption") or i + 1 >= len(argv):
            setup("usage")
        v = argv[i + 1]
        if t == "--config":
            cfgs.append(v)
        elif t == "--keyboard":
            kbs.append(v)
        else:
            gos.append(v)
        i += 2
    if not cfgs or len(gos) > 1:
        setup("usage")
    return cfgs, kbs, (gos[0] if gos else None)


def read_file(p):
    try:
        st = os.stat(p)
    except OSError:
        setup("unreadable")
    if not stat.S_ISREG(st.st_mode):
        setup("unreadable")
    if st.st_size > LIMIT:
        setup("too_large")
    try:
        with open(p, "rb") as f:
            return f.read().decode("utf-8", errors="replace")
    except OSError:
        setup("unreadable")


def configstring_to_int(v):
    if v.startswith(("true", "on", "yes")):
        return 1
    if v.startswith(("false", "off", "no")):
        return 0
    if re.fullmatch(r"[0-9]+", v):
        return int(v)
    return None


def main():
    global VARIANT
    argv = sys.argv[1:]
    if argv[:1] == ["--variant"]:
        VARIANT = argv[1]
        argv = argv[2:]
    cfgs, kbs, go = parse_args(argv)
    texts = [read_file(p) for p in cfgs]
    golines = None
    if go is not None:
        golines = [l for l in read_file(go).split("\n") if l.strip() != ""]
        for l in golines:
            try:
                if not isinstance(json.loads(l), dict):
                    setup("bad_json")
            except ValueError:
                setup("bad_json")

    glob = {}
    dev = {}  # name -> {key: value}
    unsupported = 0
    for text in texts:
        stack, cur = [], None
        skip_depth = None  # for nodev: depth at which a device block started
        for raw in text.split("\n"):
            line = raw.strip(" \t\r\n\x0b\x0c")
            if VARIANT == "nodev":
                if skip_depth is not None:
                    if "=" not in line and line == "}":
                        stack.pop()
                        if len(stack) <= skip_depth:
                            skip_depth = None
                    elif "=" not in line and line.endswith("{"):
                        stack.append(line[:-1].strip())
                    continue
                if "=" not in line and line.endswith("{") and line[:-1].strip() == "device":
                    skip_depth = len(stack)
                    stack.append("device")
                    continue
            if line == "" or line[0] == "#":
                continue
            if "=" not in line:
                if line == "}":
                    if stack:
                        stack.pop()
                    if not stack:
                        cur = None
                elif line.endswith("{"):
                    stack.append(line[:-1].strip())
                continue
            lhs, rhs = (s.strip(" \t\r\n\x0b\x0c") for s in line.split("=", 1))
            if lhs.startswith("$") or lhs == "source":
                continue
            key = ":".join(stack + [lhs])
            is_dev_block = stack == ["device"]
            if is_dev_block and lhs == "name":
                if VARIANT == "global":
                    continue
                name = rhs.split("#", 1)[0].strip(" \t\r\n\x0b\x0c")
                cur = name
                dev.setdefault(name, {})
                continue
            rel_global = key in ("input:repeat_rate", "input:repeat_delay", "input:numlock_by_default")
            rel_dev = is_dev_block and lhs in NAMES
            rel_bracket = key.startswith("device[") and key.split(":")[-1] in NAMES
            if not (rel_global or rel_dev or rel_bracket):
                continue
            if VARIANT == "global" and not rel_global:
                continue
            if rel_bracket:
                unsupported += 1
                continue
            if "$" in line or "{{" in line or "\\" in line:
                unsupported += 1
                continue
            if "##" in rhs:
                unsupported += 1
                continue
            value = configstring_to_int(rhs.split("#", 1)[0].strip(" \t\r\n\x0b\x0c"))
            if value is None:
                unsupported += 1
                continue
            name = lhs if rel_dev else key.split(":")[-1]
            lo, hi = RANGE[name]
            if not (lo <= value <= hi):
                unsupported += 1
                continue
            if rel_dev:
                if cur is None:
                    unsupported += 1
                    continue
                dev[cur][name] = value
            else:
                glob[name] = value

    def eff(kb, name):
        if kb != "*" and kb in dev and name in dev[kb]:
            return dev[kb][name], "D"
        if name in glob:
            return glob[name], "G"
        return DEFAULT[name], "-"

    out = []
    kb_list = kbs if kbs else ["*"]
    if VARIANT == "global":
        dev_lookup = False
    for kb in kb_list:
        vals = []
        for name in NAMES:
            if VARIANT == "global":
                v, f = (glob[name], "G") if name in glob else (DEFAULT[name], "-")
            else:
                v, f = eff(kb, name)
            vals.append((v, f))
        out.append(f"MADO_KBDOPT: keyboard={kb} repeat_rate={vals[0][0]} repeat_delay={vals[1][0]} "
                   f"numlock={vals[2][0]} from={vals[0][1]}/{vals[1][1]}/{vals[2][1]} unsupported={unsupported}")
    live = {}
    if golines is not None:
        for l in golines:
            o = json.loads(l)
            if isinstance(o.get("option"), str) and type(o.get("int")) is int:
                live[o["option"]] = o["int"]
        verdicts = []
        for opt in OPTS:
            name = opt.split(":")[1]
            cfgv = glob[name] if name in glob else DEFAULT[name]
            lv = live.get(opt)
            if lv is None:
                v = "UNKNOWN"
                out.append(f"MADO_KBDOPT_LIVE: option={opt} config={cfgv} live=? verdict=UNKNOWN")
            else:
                v = "AGREE" if lv == cfgv else "DIFFER"
                out.append(f"MADO_KBDOPT_LIVE: option={opt} config={cfgv} live={lv} verdict={v}")
            verdicts.append(v)
        agg = "DIFFER" if "DIFFER" in verdicts else "UNKNOWN" if "UNKNOWN" in verdicts else "AGREE"
    else:
        agg = "NONE"
    out.append(f"MADO_KBDOPT: DONE keyboards={len(kb_list)} unsupported={unsupported} live={agg}")
    sys.stdout.write("\n".join(out) + "\n")
    sys.exit(0)


if __name__ == "__main__":
    main()
