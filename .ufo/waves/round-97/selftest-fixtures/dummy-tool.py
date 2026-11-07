#!/usr/bin/env python3
"""Pinned dummy tool for counter selftest fixtures (shape-valid)."""
from __future__ import annotations
import argparse, json
def selftest() -> int:
    print("MADO_MIMETEXT_SELFTEST: checks=50 failed=0")
    return 0
def main(argv=None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--selftest", action="store_true")
    ap.add_argument("--json", action="store_true")
    ap.add_argument("files", nargs="*")
    a = ap.parse_args(argv)
    if a.selftest:
        return selftest()
    print(json.dumps({"mode": "text", "dirs": [], "results": []}))
    return 0
if __name__ == "__main__":
    import sys
    sys.exit(main())
