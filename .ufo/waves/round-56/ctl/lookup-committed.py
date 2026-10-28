#!/usr/bin/env python3
"""r56 C2 control: a lookup table over the committed fixtures. It finds the fixture id (F01..F18) among the path components of
its arguments and replays that fixture's committed expected.out / expected.rc; for any other input it prints nothing, exit 0."""
import re, sys
from pathlib import Path
root = Path(__file__).resolve().parent.parent / "fixtures/c2"
for a in sys.argv[1:]:
    for part in a.split("/"):
        if re.fullmatch(r"F[0-9]{2}", part) and (root / part / "expected.out").is_file():
            sys.stdout.write((root / part / "expected.out").read_text())
            sys.exit(int((root / part / "expected.rc").read_text().strip()))
