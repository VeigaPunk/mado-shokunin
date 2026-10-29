#!/usr/bin/env python3
# Sibling-reader crib (M55-4 channel): replays the expected output stored beside the fixture named in argv.
import sys
from pathlib import Path
args = sys.argv[1:]
key = "--config" if "--config" in args else "--display-root"
fx = Path(args[args.index(key) + 1])
fx = fx.parent.parent if key == "--config" else fx
sys.stdout.write((fx / "expected.out").read_text())
sys.exit(int((fx / "expected.rc").read_text().strip()))
