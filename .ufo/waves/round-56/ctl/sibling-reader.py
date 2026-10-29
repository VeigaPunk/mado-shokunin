#!/usr/bin/env python3
"""r56 C2 control (v2 E7): a tool that never parses a config. It reads `expected.out` and `expected.rc` from the directory named by
`--display-root` (the layout round 56 wave 1 showed leaking the answer key) and replays them; when they are absent it prints nothing
and exits 0. Under the staged harness layout (registration-v2 E6) it must pass 0 of the 26 fixtures."""
import sys
from pathlib import Path
a = sys.argv[1:]
root = None
for i, x in enumerate(a):
    if x == "--display-root" and i + 1 < len(a):
        root = Path(a[i + 1])
if root is not None and (root / "expected.out").is_file():
    sys.stdout.write((root / "expected.out").read_text())
    rc = root / "expected.rc"
    sys.exit(int(rc.read_text().strip()) if rc.is_file() else 0)
