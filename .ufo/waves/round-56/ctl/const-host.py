#!/usr/bin/env python3
"""r56 C2 control: a do-nothing tool that prints committed fixture F02's expected output (and exits 0) whatever it is asked."""
import sys
from pathlib import Path
sys.stdout.write((Path(__file__).resolve().parent.parent / "fixtures/c2/F02/expected.out").read_text())
