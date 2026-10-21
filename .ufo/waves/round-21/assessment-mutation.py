#!/usr/bin/env python3
"""Demonstrate the frozen C2 selftest kills one removed input-digest check."""
import hashlib
import json
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent
LANE = ROOT.parents[2]


def main():
    source = (LANE / 'tools/mado-assessment.py').read_text()
    old = 'if found != expected:'
    if source.count(old) != 1:
        raise SystemExit('mutation refused: expected one digest-comparison site')
    mutated = source.replace(old, 'if False and found != expected:')
    with tempfile.TemporaryDirectory(prefix='mado-r21-assessment-mutant-') as tmp:
        path = Path(tmp) / 'mado-assessment.py'
        path.write_text(mutated)
        command = [sys.executable, '-I', str(path), '--selftest', str(ROOT / 'assessment-fixtures')]
        proc = subprocess.run(command, capture_output=True, text=True, timeout=60)
        data = json.loads(proc.stdout)
        case = next(row for row in data['cases'] if row['id'] == 'population_file_mutated')
        killed = proc.returncode == 1 and not case['pass'] and data['finding_ids'] == ['assessment_oracle_mismatch']
        print(json.dumps({'pass': killed, 'mutation': 'remove only actual population-digest comparison',
                          'source_sha256': hashlib.sha256(source.encode()).hexdigest(),
                          'mutant_sha256': hashlib.sha256(mutated.encode()).hexdigest(),
                          'runner_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
                          'exit': proc.returncode, 'stdout': proc.stdout, 'stderr': proc.stderr}, sort_keys=True))
        return 0 if killed else 1


if __name__ == '__main__':
    raise SystemExit(main())
