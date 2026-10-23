#!/usr/bin/env python3
"""Run only the five round-26 population fixtures, comparing exit status."""
import argparse
import os
from pathlib import Path
import subprocess
import sys


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--checker", required=True)
    args = parser.parse_args()
    r26 = Path(".ufo/waves/round-26")
    fixtures = r26 / "quality/population-fixtures"
    registration = r26 / "registration.md"
    cases = (
        (registration, fixtures / "receipt-c1-green.txt", 0),
        (registration, fixtures / "receipt-red-case-removed.txt", 1),
        (registration, fixtures / "receipt-red-denominator.txt", 1),
        (fixtures / "registration-red-total.md", fixtures / "receipt-c1-green.txt", 1),
        (registration, fixtures / "receipt-red-selfconsistent-40.txt", 1),
    )
    passed = 0
    env = {"PATH": "/usr/bin", "HOME": os.environ.get("HOME", "/nonexistent")}
    for reg, receipt, expected in cases:
        command = [sys.executable, "-I", args.checker, "--registration", str(reg), str(receipt)]
        try:
            actual = subprocess.run(command, env=env, timeout=30).returncode
        except (OSError, subprocess.TimeoutExpired) as error:
            actual = type(error).__name__
        matched = actual == expected
        passed += matched
        print("FIXTURE %s rc=%s expected=%d %s" % (
            receipt.name, actual, expected, "PASS" if matched else "FAIL"), flush=True)
    print("POPULATION_SUITE pass=%d/5" % passed, flush=True)
    return 0 if passed == 5 else 1


if __name__ == "__main__":
    sys.exit(main())
