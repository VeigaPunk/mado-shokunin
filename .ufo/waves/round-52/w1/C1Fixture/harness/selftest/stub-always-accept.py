#!/usr/bin/env python3
"""stub-always-accept.py — HARNESS SELF-TEST ASSET, not a candidate C1 counter.

Purpose: prove that c1-fixture-harness.py rejects an always-accept counter.  This stub
always exits 0 with verdict=TARGET_MET, whatever the repository or revision is.  The
harness must report verdict=FAIL on the red case.

Usage: stub-always-accept.py --repo <dir> --rev <rev> --work <dir>
"""

import argparse
import sys


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo", default=".")
    ap.add_argument("--rev", required=True)
    ap.add_argument("--work", default=None)
    args = ap.parse_args(argv)
    print("STUB: population=82 ledger_rows=82 self_pointer=0 generic_context=0 "
          "verdict=TARGET_MET rev=%s" % args.rev)
    return 0


if __name__ == "__main__":
    sys.exit(main())
