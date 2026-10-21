#!/usr/bin/env python3
"""Run only C2 with old C1 bytes, changed C1 bytes and no C1 in an isolated tree."""
import hashlib
import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent
LANE = ROOT.parents[2]


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    outputs = []
    with tempfile.TemporaryDirectory(prefix='mado-r21-assessment-independence-') as tmp:
        stage = Path(tmp)
        fixtures = stage / 'fixtures'
        shutil.copytree(ROOT / 'assessment-fixtures', fixtures)
        tools = stage / 'tools'
        tools.mkdir()
        gate = tools / 'mado-assessment.py'
        shutil.copyfile(LANE / 'tools/mado-assessment.py', gate)
        classifier = tools / 'mado-tripwire.py'
        for name, source in [('C1base', ROOT / 'evidence/tool-before.py'),
                             ('C1changed', LANE / 'tools/mado-tripwire.py'), ('C1absent', None)]:
            if source is None:
                classifier.unlink()
            else:
                shutil.copyfile(source, classifier)
            proc = subprocess.run([sys.executable, '-I', str(gate), '--selftest', str(fixtures)],
                                  cwd=stage, text=True, capture_output=True, timeout=60)
            outputs.append({'state': name, 'c1_sha256': sha(classifier) if source else None,
                            'exit': proc.returncode, 'stdout': proc.stdout, 'stderr': proc.stderr})
        identical = len({row['stdout'] for row in outputs}) == 1
        passed = identical and all(row['exit'] == 0 for row in outputs)
        print(json.dumps({'gate_sha256': sha(gate), 'runner_sha256': sha(Path(__file__)),
                          'scope': 'same C2 bytes and expectations; classifier bytes change or disappear but are never executed',
                          'identical_c2_output': identical, 'pass': passed, 'runs': outputs}, sort_keys=True))
        return 0 if passed else 1


if __name__ == '__main__':
    raise SystemExit(main())
