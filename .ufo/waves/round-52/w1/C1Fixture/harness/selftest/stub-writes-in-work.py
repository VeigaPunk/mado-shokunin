#!/usr/bin/env python3
"""stub-writes-in-work.py — HARNESS SELF-TEST ASSET, not a candidate C1 counter.

Purpose: prove that the `--work` argument really reaches the counter and that the
harness observes what the counter writes there.  This stub writes a file into the
directory it was handed as `--work`; the harness must list that file under
`scratch_files_after` for the case.

Used by `run-selftest.sh` to check the scratch argument end to end.

Usage: stub-writes-in-work.py --repo <dir> --rev <rev> --work <dir>
"""

import argparse
import os
import sys


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo", default=".")
    ap.add_argument("--rev", required=True)
    ap.add_argument("--work", default=None)
    args = ap.parse_args(argv)
    if args.work:
        os.makedirs(args.work, exist_ok=True)
        with open(os.path.join(args.work, "WORK-PROBE.txt"), "w") as fh:
            fh.write("the counter received --work\n")
    print("STUB: population=1 ledger_rows=1 verdict=TARGET_MET rev=%s" % args.rev)
    return 0


if __name__ == "__main__":
    sys.exit(main())
