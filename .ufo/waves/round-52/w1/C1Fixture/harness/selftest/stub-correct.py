#!/usr/bin/env python3
"""stub-correct.py — HARNESS SELF-TEST ASSET, not a candidate C1 counter.

Purpose: prove that c1-fixture-harness.py actually discriminates.  This stub reads the
ledger at the requested revision of the requested repository and:
  * when the ledger is the frozen do-nothing control (it carries the control's own
    marker text) it reports a self-pointer defect and an instrument-specific-context
    defect and exits 1 with verdict=TARGET_MISSED;
  * otherwise it exits 0 with verdict=TARGET_MET.

It implements none of the C1 predicate: it recognises the control by a literal marker
string.  It exists only to exercise the harness plumbing (green pass, red fail naming
both defects).  A counter author must not read its verdict as a claim.

Usage: stub-correct.py --repo <dir> --rev <rev> --work <dir>
"""

import argparse
import subprocess
import sys

LEDGER = "quality/tool-ledger.md"
CONTROL_MARKER = "generic accountability pointer to this ledger itself"


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo", default=".")
    ap.add_argument("--rev", required=True)
    ap.add_argument("--work", default=None)
    args = ap.parse_args(argv)
    proc = subprocess.run(("git", "-C", args.repo, "show", "%s:%s" % (args.rev, LEDGER)),
                          capture_output=True)
    if proc.returncode != 0:
        print("STUB: verdict=TARGET_MISSED ledger=absent")
        return 1
    text = proc.stdout.decode("utf-8", "replace")
    if CONTROL_MARKER in text:
        print("detail: self_pointer path=tools/mado-verify.sh")
        print("detail: generic_context path=tools/mado-verify.sh")
        print("STUB: population=1 ledger_rows=2 self_pointer=1 generic_context=1 "
              "verdict=TARGET_MISSED rev=%s" % args.rev)
        return 1
    print("STUB: population=82 ledger_rows=82 self_pointer=0 generic_context=0 "
          "verdict=TARGET_MET rev=%s" % args.rev)
    return 0


if __name__ == "__main__":
    sys.exit(main())
