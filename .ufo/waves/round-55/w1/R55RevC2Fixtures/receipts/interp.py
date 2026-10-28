#!/usr/bin/env python3
# Independent reading of registration.md §C2 (written by seat R55RevC2Fixtures from the text only).
# Scratch tool. Read-only: reads the paths named on argv, writes stdout only.
# --literal-empty-stack is an ablation: KEY = "" + ":" + LHS when the stack is empty (literal reading).
import json
import os
import re
import stat
import sys

WS = " \t\r\n\x0b\x0c"
NAMES = ("repeat_rate", "repeat_delay", "numlock_by_default")
INPUT_KEYS = {"input:" + n for n in NAMES}
RANGE = {"repeat_rate": (0, 200), "repeat_delay": (0, 2000), "numlock_by_default": (0, 1)}
DEFAULT = {"repeat_rate": 25, "repeat_delay": 600, "numlock_by_default": 0}
MAXB = 1048576


class Setup(Exception):
    def __init__(self, reason):
        super().__init__(reason)
        self.reason = reason


def parse_argv(argv):
    configs, kbds, getopt = [], [], None
    i = 0
    while i < len(argv):
        a = argv[i]
        if a not in ("--config", "--keyboard", "--getoption") or i + 1 >= len(argv):
            raise Setup("usage")
        v = argv[i + 1]
        if a == "--config":
            configs.append(v)
        elif a == "--keyboard":
            kbds.append(v)
        else:
            if getopt is not None:
                raise Setup("usage")
            getopt = v
        i += 2
    if not configs:
        raise Setup("usage")
    return configs, kbds, getopt


def read_bytes(path):
    try:
        st = os.stat(path)
    except OSError:
        raise Setup("unreadable")
    if not stat.S_ISREG(st.st_mode):
        raise Setup("unreadable")
    if st.st_size > MAXB:
        raise Setup("too_large")
    try:
        with open(path, "rb") as f:
            data = f.read(MAXB + 1)
    except OSError:
        raise Setup("unreadable")
    if len(data) > MAXB:
        raise Setup("too_large")
    return data


def parse_getoption(data, literal):
    live = {}
    for line in data.decode("utf-8", errors="replace").split("\n"):
        t = line.strip(WS)
        if t == "":
            continue
        try:
            obj = json.loads(t)
        except ValueError:
            raise Setup("bad_json")
        if not isinstance(obj, dict):
            raise Setup("bad_json")
        opt = obj.get("option")
        val = obj.get("int")
        if isinstance(opt, str) and type(val) is int:
            live[opt] = val
    return live


def parse_configs(blobs, literal):
    glob, devs, unsup = {}, {}, 0
    for data in blobs:
        text = data.decode("utf-8", errors="replace")
        stack, cur = [], None
        for raw in text.split("\n"):
            s = raw.strip(WS)
            if s == "" or s[0] == "#":
                continue
            if "=" not in s:
                if s == "}":
                    if stack:
                        stack.pop()
                        if not stack:
                            cur = None
                elif s.endswith("{"):
                    stack.append(s[:-1].strip(WS))
                continue
            lhs, rhs = s.split("=", 1)
            lhs = lhs.strip(WS)
            rhs = rhs.strip(WS)
            if lhs.startswith("$") or lhs == "source":
                continue
            if literal and not stack:
                key = ":" + lhs
            else:
                key = ":".join(stack + [lhs]) if stack else lhs
            in_dev = stack == ["device"]
            if in_dev and lhs == "name":
                cur = rhs.split("#", 1)[0].strip(WS)
                devs.setdefault(cur, {})
                continue
            relevant = (
                key in INPUT_KEYS
                or (in_dev and lhs in NAMES)
                or (key.startswith("device[") and key.rsplit(":", 1)[-1] in NAMES)
            )
            if not relevant:
                continue
            if key.startswith("device["):
                unsup += 1
                continue
            if "$" in s or "{{" in s or "\\" in s:
                unsup += 1
                continue
            if "##" in rhs:
                unsup += 1
                continue
            vt = rhs.split("#", 1)[0].strip(WS)
            if vt.startswith(("true", "on", "yes")):
                v = 1
            elif vt.startswith(("false", "off", "no")):
                v = 0
            elif re.fullmatch(r"[0-9]+", vt):
                v = int(vt)
            else:
                unsup += 1
                continue
            name = lhs
            lo, hi = RANGE[name]
            if not (lo <= v <= hi):
                unsup += 1
                continue
            if in_dev and name in NAMES:
                if cur is None:
                    unsup += 1
                    continue
                devs[cur][name] = v
            else:
                glob[name] = v
    return glob, devs, unsup


def effective(devs, glob, kbd, opt):
    d = devs.get(kbd, {})
    if opt in d:
        return d[opt], "D"
    if opt in glob:
        return glob[opt], "G"
    return DEFAULT[opt], "-"


def main(argv):
    literal = "--literal-empty-stack" in argv
    argv = [a for a in argv if a != "--literal-empty-stack"]
    try:
        configs, kbds, getopt = parse_argv(argv)
        blobs = [read_bytes(p) for p in configs]
        live = parse_getoption(read_bytes(getopt), literal) if getopt is not None else None
    except Setup as e:
        print("MADO_KBDOPT: SETUP %s" % e.reason)
        return 2
    glob, devs, unsup = parse_configs(blobs, literal)
    names = kbds if kbds else ["*"]
    out = []
    for k in names:
        vals = {}
        froms = {}
        for opt in NAMES:
            vals[opt], froms[opt] = effective(devs, glob, k, opt)
        out.append(
            "MADO_KBDOPT: keyboard=%s repeat_rate=%d repeat_delay=%d numlock=%d from=%s/%s/%s unsupported=%d"
            % (k, vals["repeat_rate"], vals["repeat_delay"], vals["numlock_by_default"],
               froms["repeat_rate"], froms["repeat_delay"], froms["numlock_by_default"], unsup)
        )
    live_verdict = "NONE"
    if live is not None:
        verdicts = []
        for opt in NAMES:
            cfg = glob.get(opt, DEFAULT[opt])
            lv = live.get("input:" + opt)
            if lv is None:
                vd = "UNKNOWN"
                lvs = "?"
            else:
                lvs = str(lv)
                vd = "AGREE" if lv == cfg else "DIFFER"
            verdicts.append(vd)
            out.append("MADO_KBDOPT_LIVE: option=input:%s config=%d live=%s verdict=%s" % (opt, cfg, lvs, vd))
        if "DIFFER" in verdicts:
            live_verdict = "DIFFER"
        elif "UNKNOWN" in verdicts:
            live_verdict = "UNKNOWN"
        else:
            live_verdict = "AGREE"
    out.append("MADO_KBDOPT: DONE keyboards=%d unsupported=%d live=%s" % (len(names), unsup, live_verdict))
    sys.stdout.write("\n".join(out) + "\n")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
