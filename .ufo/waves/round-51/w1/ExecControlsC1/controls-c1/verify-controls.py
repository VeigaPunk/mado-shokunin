#!/usr/bin/env python3
"""Compare C1 control receipts against the frozen expectations (seat ExecControlsC1)."""

import os
import re
import sys

SEAT = "/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-51/w1/ExecControlsC1"
RUN = os.path.join(SEAT, "controls-c1", "actual-run")
EXP = {
    "green": ("C1_R51: population=79 ledger_rows=79 uncovered=0 dangling=0 bad_pointer=0 "
              "empty_desc=0 selftest=ok verdict=TARGET_MET rev=r51-control", 0),
    "ctl-a": ("C1_R51: population=79 ledger_rows=78 uncovered=1 dangling=0 bad_pointer=0 "
              "empty_desc=0 selftest=ok verdict=TARGET_MISSED rev=mut-a", 1),
    "ctl-b": ("C1_R51: population=79 ledger_rows=79 uncovered=0 dangling=0 bad_pointer=5 "
              "empty_desc=0 selftest=ok verdict=TARGET_MISSED rev=mut-b", 1),
    "ctl-c": ("C1_R51: population=79 ledger_rows=79 uncovered=0 dangling=0 bad_pointer=0 "
              "empty_desc=44 selftest=ok verdict=TARGET_MISSED rev=mut-c", 1),
    "ctl-d": ("C1_R51: population=79 ledger_rows=82 uncovered=0 dangling=3 bad_pointer=0 "
              "empty_desc=0 selftest=ok verdict=TARGET_MISSED rev=mut-d", 1),
    "ctl-e-lane-base": ("C1_R51: population=79 ledger=absent verdict=TARGET_MISSED "
                        "rev=6ca8c559a4a3d6d361101592116eea2bc7452437", 1),
    "fixture-base-absent": ("C1_R51: population=79 ledger=absent verdict=TARGET_MISSED "
                            "rev=e5943b7032fd9b73d02f7e9a71efa6848cec22a8", 1),
}


def read(name):
    body = open(os.path.join(RUN, name + ".txt")).read()
    line = [l for l in body.splitlines() if l.startswith("C1_R51:")]
    rc = re.search(r"^exit=(\d+)$", body, re.M)
    return (line[-1] if line else "<none>"), int(rc.group(1)) if rc else None


def main():
    bad = 0
    print("%-20s %-6s %-6s %s" % ("control", "line", "exit", "verdict"))
    for name, (want_line, want_rc) in EXP.items():
        got_line, got_rc = read(name)
        ok = got_line == want_line and got_rc == want_rc
        bad += 0 if ok else 1
        print("%-20s %-6s %-6s %s" % (
            name,
            "match" if got_line == want_line else "DIFF",
            "match" if got_rc == want_rc else "DIFF",
            "PASS" if ok else "FAIL"))
        if not ok:
            print("  want: %s [%s]" % (want_line, want_rc))
            print("  got : %s [%s]" % (got_line, got_rc))
    st = open(os.path.join(RUN, "selftest.txt")).read().strip().splitlines()
    sel_ok = st and st[-2].endswith("failed=0") and st[-1] == "exit=0"
    print("%-20s %-6s %-6s %s" % ("selftest", "n/a", "n/a", "PASS" if sel_ok else "FAIL"))
    bad += 0 if sel_ok else 1
    print("controls=%d mismatched=%d" % (len(EXP) + 1, bad))
    return 0 if bad == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
