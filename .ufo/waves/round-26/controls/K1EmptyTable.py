#!/usr/bin/env python3
"""mado round-26 C1 control, shape ALL-EMPTY (variant A): print `[[], []]` and nothing else.

The shape claims no work at all: no config read, no table. It is the strongest statement of
"the empty table is the answer" that the counter could be fooled by. CLI matches the tool:
`python3 -I K1EmptyTable.py --home DIR` -> a JSON `[nodes, beziers]` pair of empty lists.
"""
import argparse
import json
import sys


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--home", required=True)
    ap.parse_args()
    sys.stdout.write(json.dumps([[], []], separators=(",", ":")) + "\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
