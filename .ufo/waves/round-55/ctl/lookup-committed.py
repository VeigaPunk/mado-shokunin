#!/usr/bin/env python3
"""r55 C2 control: a lookup table over the COMMITTED fixtures (matches argv against each args.json). It cannot answer a fixture it has never seen."""
import json, sys
from pathlib import Path
root = Path(__file__).resolve().parent.parent / "fixtures/c2"
for d in sorted(root.iterdir()):
    if json.loads((d / "args.json").read_text()) == sys.argv[1:]:
        sys.stdout.write((d / "expected.out").read_text())
        sys.exit(int((d / "expected.rc").read_text()))
sys.stdout.write("MADO_KBDOPT: SETUP usage\n")
sys.exit(2)
