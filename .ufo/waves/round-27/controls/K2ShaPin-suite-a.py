#!/usr/bin/env python3
"""SHA-PIN control: compare subject bytes only; run no behavioural checks."""
import argparse
import hashlib
from pathlib import Path


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--c1", required=True)
    parser.add_argument("--c2", required=True)
    parser.add_argument("--rev", required=True)
    args = parser.parse_args()
    subjects = (
        (args.c1, "4ed70b5427f2e223a8d816679e6d1fad7d2e76d2ed57aa0fe7f135496e836428"),
        (args.c2, "b92c32da632bc9cfaeae72b6a0be2202e5a25653274cc0b33fc0ae3f37a716a8"),
    )
    try:
        matched = all(hashlib.sha256(Path(path).read_bytes()).hexdigest() == pin
                      for path, pin in subjects)
    except OSError:
        matched = False
    print("SHA_PIN " + ("PASS" if matched else "FAIL"))
    return 0 if matched else 1


if __name__ == "__main__":
    raise SystemExit(main())
