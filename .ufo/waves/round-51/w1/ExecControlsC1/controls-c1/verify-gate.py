#!/usr/bin/env python3
"""Grade the ExecLedgerGate draft's control receipts (seat ExecControlsC1).

Expectations use the draft's own summary schema (`LEDGER:`), with values fixed by
the frozen C1 predicate. The gate prints no `selftest=` field in a normal run; the
suite is graded separately from gate-selftest.txt.
"""

import os
import re
import sys

SEAT = "/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-51/w1/ExecControlsC1"
RUN = os.path.join(SEAT, "controls-c1", "actual-run")

EXP = {
    "green": ("LEDGER: population=79 ledger_rows=79 uncovered=0 dangling=0 bad_pointer=0 "
              "empty_desc=0 verdict=TARGET_MET rev=aef0acf4ea4be1598771a210b8d41771517ff4be", 0),
    "ctl-a": ("LEDGER: population=79 ledger_rows=78 uncovered=1 dangling=0 bad_pointer=0 "
              "empty_desc=0 verdict=TARGET_MISSED rev=c02eeab908ae9da8d2413ef6dfbbfe81a089467a", 1),
    "ctl-b": ("LEDGER: population=79 ledger_rows=79 uncovered=0 dangling=0 bad_pointer=5 "
              "empty_desc=0 verdict=TARGET_MISSED rev=a03b9fdcf63122cb3cf35fa1870b77fcb45e6f4b", 1),
    "ctl-c": ("LEDGER: population=79 ledger_rows=79 uncovered=0 dangling=0 bad_pointer=0 "
              "empty_desc=44 verdict=TARGET_MISSED rev=70d323611187101f67a5c5afa08f34bbbb382899", 1),
    "ctl-d": ("LEDGER: population=79 ledger_rows=82 uncovered=0 dangling=3 bad_pointer=0 "
              "empty_desc=0 verdict=TARGET_MISSED rev=f6bbf864f4ec034a5fe2c009548a625ceb695a3d", 1),
    "ctl-e-lane-base": ("LEDGER: population=79 verdict=TARGET_MISSED ledger=absent "
                        "rev=6ca8c559a4a3d6d361101592116eea2bc7452437", 1),
    "fixture-base-absent": ("LEDGER: population=79 verdict=TARGET_MISSED ledger=absent "
                            "rev=e5943b7032fd9b73d02f7e9a71efa6848cec22a8", 1),
}


def read(name):
    body = open(os.path.join(RUN, "gate-" + name + ".txt")).read()
    line = [l for l in body.splitlines() if l.startswith("LEDGER:")]
    rc = re.search(r"^exit=(\d+)$", body, re.M)
    return (line[-1] if line else "<none>"), int(rc.group(1)) if rc else None


def main():
    bad = 0
    print("%-20s %-6s %-6s %s" % ("control", "line", "exit", "verdict"))
    for name, (want_line, want_rc) in EXP.items():
        got_line, got_rc = read(name)
        ok = got_line == want_line and got_rc == want_rc
        bad += 0 if ok else 1
        print("%-20s %-6s %-6s %s" % (name,
                                      "match" if got_line == want_line else "DIFF",
                                      "match" if got_rc == want_rc else "DIFF",
                                      "PASS" if ok else "FAIL"))
        if not ok:
            print("  want: %s [%s]" % (want_line, want_rc))
            print("  got : %s [%s]" % (got_line, got_rc))
    st = open(os.path.join(RUN, "gate-selftest.txt")).read().strip().splitlines()
    sel = [l for l in st if l.startswith("LEDGER_SELFTEST:")]
    m = re.match(r"LEDGER_SELFTEST: (\d+)/(\d+) passed", sel[-1]) if sel else None
    # >=42 checks is the draft's own floor; a shrunken suite must fail here.
    sel_ok = bool(m) and m.group(1) == m.group(2) and int(m.group(2)) >= 42 and st[-1] == "exit=0"
    print("%-20s %-6s %-6s %s" % ("gate-selftest", "n/a", "n/a", "PASS" if sel_ok else "FAIL"))
    bad += 0 if sel_ok else 1
    print("controls=%d mismatched=%d" % (len(EXP) + 1, bad))
    return 0 if bad == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
