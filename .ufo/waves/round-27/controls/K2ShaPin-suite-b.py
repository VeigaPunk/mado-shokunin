#!/usr/bin/env python3
"""SHA-PIN control: compare subject bytes only; run no behavioural checks."""
import argparse
import hashlib
from pathlib import Path


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--checker", required=True)
    args = parser.parse_args()
    pin = "803e0096c994d301fa7fe9a9dd7e35255ee1f5bcf3f63d15956cdba8943d0f64"
    try:
        matched = hashlib.sha256(Path(args.checker).read_bytes()).hexdigest() == pin
    except OSError:
        matched = False
    print("SHA_PIN " + ("PASS" if matched else "FAIL"))
    return 0 if matched else 1


if __name__ == "__main__":
    raise SystemExit(main())
