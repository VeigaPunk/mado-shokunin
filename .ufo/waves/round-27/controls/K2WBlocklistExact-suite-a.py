#!/usr/bin/env python3
"""Reject exact single-W-mutant byte strings, without running either subject."""
import argparse
import json
import os
from pathlib import Path
import subprocess


W_FILE = ".ufo/waves/round-27/c2/mutants-w.json"
SUBJECTS = {
    ".ufo/waves/round-26/c1/count-v2.py": "c1",
    ".ufo/waves/round-26/c2/count.py": "c2",
}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--c1", required=True)
    parser.add_argument("--c2", required=True)
    parser.add_argument("--rev", required=True)
    args = parser.parse_args()
    root = Path.cwd()
    mutants = json.loads((root / W_FILE).read_bytes())
    env = {
        "PATH": "/usr/bin",
        "HOME": os.environ["HOME"],
        "GIT_CONFIG_NOSYSTEM": "1",
        "GIT_OPTIONAL_LOCKS": "0",
    }
    for rel, argument in SUBJECTS.items():
        subject = Path(getattr(args, argument)).read_bytes()
        pristine = subprocess.run(
            [
                "timeout", "30", "prlimit", "--as=4000000000", "--core=0", "--",
                "git", "-C", str(root), "show", args.rev + ":" + rel,
            ],
            env=env,
            capture_output=True,
            check=True,
        ).stdout
        for mutant in mutants:
            if mutant["file"] != rel:
                continue
            old, new = mutant["old"].encode(), mutant["new"].encode()
            if pristine.count(old) == 1 and subject == pristine.replace(old, new, 1):
                print("W-BLOCKLIST-EXACT reject %s %s" % (argument, mutant["id"]))
                return 1
    print("W-BLOCKLIST-EXACT accept")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
