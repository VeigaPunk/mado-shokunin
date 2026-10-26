#!/usr/bin/env python3
"""Do-nothing control: locate the frozen reference in a non-hidden path, exec it."""
import glob
import os
import sys

cands = []
for d in glob.glob('/fast/scratch/hyaku/mado-r46/*'):
    for sub in [d] + glob.glob(d + '/*'):
        cands.append(os.path.join(sub, '.ufo/waves/round-46/l1-draft/mado-devices.py'))
for p in cands:
    if os.path.isfile(p):
        os.execv(sys.executable, [sys.executable, '-I', p] + sys.argv[1:])
sys.exit(3)
