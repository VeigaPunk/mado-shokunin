#!/usr/bin/env python3
"""Reject exact single-W-mutant byte strings, without running the checker."""
import argparse
import json
import os
from pathlib import Path
import subprocess


W_FILE = ".ufo/waves/round-27/c2/mutants-w.json"
SUBJECT = ".ufo/waves/round-26/quality/check-population.py"


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--checker", required=True)
    args = parser.parse_args()
    root = Path.cwd()
    mutants = json.loads((root / W_FILE).read_bytes())
    subject = Path(args.checker).read_bytes()
    env = {
        "PATH": "/usr/bin",
        "HOME": os.environ["HOME"],
        "GIT_CONFIG_NOSYSTEM": "1",
        "GIT_OPTIONAL_LOCKS": "0",
    }
    pristine = subprocess.run(
        [
            "timeout", "30", "prlimit", "--as=4000000000", "--core=0", "--",
            "git", "-C", str(root), "show", "HEAD:" + SUBJECT,
        ],
        env=env,
        capture_output=True,
        check=True,
    ).stdout
    for mutant in mutants:
        if mutant["file"] != SUBJECT:
            continue
        old, new = mutant["old"].encode(), mutant["new"].encode()
        if pristine.count(old) == 1 and subject == pristine.replace(old, new, 1):
            print("W-BLOCKLIST-EXACT reject checker %s" % mutant["id"])
            return 1
    print("W-BLOCKLIST-EXACT accept")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
