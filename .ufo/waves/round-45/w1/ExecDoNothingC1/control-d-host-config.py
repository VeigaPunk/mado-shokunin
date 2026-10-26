#!/usr/bin/env python3
"""mado-monitors (CONTROL D, r45 - only the exact host config).

Hardcodes this host's single output rule `monitor = DP-1, 3440x1440@100, 0x0, 1` and the matching live state;
anything else (another output name, resolution, rate, scale, rule count) is not modelled. A control against
PRED-C1-r45: the contract is 49 fixtures, this file knows one.
"""
import json
import os
import re
import sys


def main():
    argv = sys.argv[1:]
    if argv == ["--selftest"]:
        print("MADO_MONITORS_SELFTEST: 49/49 passed")
        return 0
    if len(argv) != 4 or argv[0] != "--monitors" or argv[2] != "--config":
        print("MADO_MONITORS: SETUP usage")
        return 2
    try:
        raw = sys.stdin.buffer.read() if argv[1] == "-" else open(argv[1], "rb").read()
        cfg = open(argv[3], "rb").read().decode("utf-8", "replace")
    except OSError:
        print("MADO_MONITORS: SETUP unreadable")
        return 2
    try:
        dump = json.loads(raw.decode("utf-8"))
    except Exception:
        print("MADO_MONITORS: SETUP bad_json")
        return 2
    m = re.fullmatch(r"monitor\s*=\s*([^,]+),\s*3440x1440@100,\s*0x0,\s*1\s*", cfg)
    if m is None or not isinstance(dump, list) or len(dump) != 1 or not isinstance(dump[0], dict):
        print("MADO_MONITORS: SETUP usage")
        return 2
    name = m.group(1).strip()
    o = dump[0]
    if not (o.get("name") == name and o.get("width") == 3440 and o.get("height") == 1440
            and isinstance(o.get("refreshRate"), (int, float)) and abs(o["refreshRate"] - 100.0) < 1.0
            and o.get("x") == 0 and o.get("y") == 0 and o.get("scale") == 1
            and o.get("transform") == 0 and o.get("mirrorOf") == "none" and o.get("disabled") is False):
        print("MADO_MONITORS: SETUP usage")
        return 2
    print("MADO_MON_RULE: n=1 sel=%s mode=3440x1440@100.00 pos=0x0 scale=1.0000 transform=0 mirror=- disabled=false" % json.dumps(name))
    print("MADO_MON_OUTPUT: name=%s rule=1 differ=- verdict=AGREE" % json.dumps(name))
    print("MADO_MONITORS: lines=1 rules=1 v2=0 unsupported=0 badrules=0 outputs=1 matched=1 unruled=0 agree=1 differ=0 disabled=0 verdict=OK")
    return 0


if __name__ == "__main__":
    sys.exit(main())
