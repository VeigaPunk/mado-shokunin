#!/usr/bin/env python3
"""P4 (H rows junked): control 2 must also see tok:H01, tok:H02, tok:H03. Verified on pristine, M25 and M24.

Expected (recorded in receipts/proposals-p4.txt): pristine 12/12 OK rc 0; M25 11/12 FAIL rc 1; M24 12/12 OK rc 0.
"""
import sys
from pathlib import Path

sys.path.insert(0, "/fast/scratch/hyaku/mado-r56/R56W2MutC1Harness")
import verify_props as v  # noqa: E402

ANCHOR = "def _need_junk(rec):\n"


def p4(src: str) -> str:
    assert src.count(ANCHOR) == 1, "P4 anchor"
    return src.replace(
        ANCHOR,
        ANCHOR + "    if not {\"tok:H01\", \"tok:H02\", \"tok:H03\"} <= set(rec[\"legs\"]):\n"
                 "        return \"H rows not junked: %s\" % rec[\"missed\"]\n", 1)


def main():
    lines = []
    for name, path in [("PRISTINE", v.PRIS), ("M25", v.SCR / "mutants/M25/r56_ctl_c1.py"),
                       ("M24", v.SCR / "mutants/M24/r56_ctl_c1.py")]:
        r = v.run_harness(p4(path.read_text()), "P4-" + name)
        lines.append("P4 on %-9s rc=%s %s" % (name, r["rc"], r["out"]))
    print("\n".join(lines))
    (v.OUT / "p4.txt").write_text("\n".join(lines) + "\n")


if __name__ == "__main__":
    main()
