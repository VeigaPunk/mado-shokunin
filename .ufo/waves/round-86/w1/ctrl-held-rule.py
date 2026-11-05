#!/usr/bin/env python3
"""Apply the unchanged frozen r85 scorer directly after its CLI rejects 75 cases."""
import importlib.util
import json
from pathlib import Path
import subprocess
import sys

repo = '/home/vgpnk/Projects/shokunin/mado-shokunin'
rev = '237ecf4e69a4986108f719f3beeafe111adaa033'
s = Path(sys.argv[1])

def extract(path, dest):
    dest.write_bytes(subprocess.check_output(['git', '-C', repo, 'show', rev + ':' + path]))

counter = s / 'c1-r85-identity-causes.py'
tool = s / 'mado-barfoot.py'
controls = s / 'c1-cases-r86.json'
extract('quality/counters/c1-r85-identity-causes.py', counter)
extract('tools/mado-barfoot.py', tool)
extract('.ufo/waves/round-86/controls/c1-cases-r86.json', controls)
spec = importlib.util.spec_from_file_location('held', counter)
held = importlib.util.module_from_spec(spec)
spec.loader.exec_module(held)
cases = json.loads(controls.read_text())['cases']
correct, rows = held.run_cases(str(tool), cases, str(s), 'held')
print('R86_CONTROL_DIRECT: rule=frozen-r85-run_cases cases=%d correct=%d/%d scope=direct-function-not-cli-target' % (len(cases), correct, len(cases)))
sys.exit(0 if correct == len(cases) else 1)
