#!/usr/bin/env python3
"""Reproduce four committed minimal register fixtures; retain receipts, remove scratch."""
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys

LANE = Path('/home/vgpnk/Projects/shokunin/mado-shokunin')
SEAT = LANE / '.ufo/waves/round-66/w1/R66ExecRegister'
SCRATCH = Path('/fast/scratch/hyaku/mado-r66/R66ExecRegister')
BASE = 'eafd500fa7be76dca59e729435e231a5032cc037'
LIVE = '.ufo/waves/round-65/receipts/gate-live-r65.txt'
FILE = '.ufo/waves/round-65/receipts/gate-fileplane-r65.txt'
HEADING = '### Surface state register (2026-11-03'
ENV = {k: v for k, v in os.environ.items() if not k.startswith('GIT_')}
ENV.update(GIT_CONFIG_NOSYSTEM='1', GIT_CONFIG_GLOBAL='/dev/null', GIT_OPTIONAL_LOCKS='0', PYTHONDONTWRITEBYTECODE='1')


def run(argv, check=True):
    result = subprocess.run(argv, cwd=SEAT, env=ENV, capture_output=True, text=True, timeout=120)
    if check and result.returncode:
        raise RuntimeError(f'{argv!r}: rc={result.returncode}\n{result.stderr}')
    return result


def git(repo, *args):
    return run(['git', '-C', str(repo), *args]).stdout


def main():
    if SCRATCH.exists():
        raise RuntimeError(f'refusing existing scratch: {SCRATCH}')
    SCRATCH.mkdir(parents=True)
    fixture = SCRATCH / 'fixture'
    fixture.mkdir()
    records = []
    try:
        git(fixture, 'init', '-q')
        assert Path(git(fixture, 'rev-parse', '--show-toplevel').strip()) == fixture
        province = git(LANE, 'show', f'{BASE}:PROVINCE.md')
        # Read only the committed register receipt paths, never worktree content.
        start = province.index(HEADING)
        end = province.index('<!-- r65 register end -->', start)
        import re
        paths = set(re.findall(r'\.ufo/waves/round-65/receipts/[^ |,)]+\.(?:txt|json|md|sh)', province[start:end]))
        bodies = {path: git(LANE, 'show', f'{BASE}:{path}') for path in paths}
        baseline = SCRATCH / 'baseline.py'
        baseline.write_text(git(LANE, 'show', f'{BASE}:quality/counters/c1-r65-register.py'))
        candidate = SEAT / 'c1-r66-register.py'
        selftest = run([sys.executable, str(candidate), '--selftest'], check=False)
        (SEAT / 'selftest.txt').write_text(selftest.stdout + selftest.stderr + f'rc={selftest.returncode}\n')
        assert selftest.returncode == 0
        live = bodies[LIVE]
        (SEAT / 'live-line-source.txt').write_text(
            f'command: git -C {LANE} show {BASE}:{LIVE}\nrc=0\n' +
            '\n'.join(line for line in live.splitlines() if line.startswith('MADO_VERIFY:')) + '\n')
        # Also demonstrate the real, non-minimal committed base register.
        actual = run([sys.executable, str(candidate), '--repo', str(LANE), '--rev', BASE], check=False)
        (SEAT / 'genuine-base.txt').write_text(actual.stdout + actual.stderr + f'rc={actual.returncode}\n')
        assert actual.returncode == 0
        for name in ('genuine', 'duplicate-heading', 'row-without-receipt', 'file-plane-only'):
            text = province
            objects = dict(bodies)
            if name == 'duplicate-heading':
                text += '\n' + province[start:end] + '\n<!-- r65 register end -->\n'
            elif name == 'row-without-receipt':
                lines = text.splitlines()
                idx = next(i for i, line in enumerate(lines) if line.startswith('| hypr plane |'))
                parts = lines[idx].split('|')
                parts[-2] = ' no receipt '
                lines[idx] = '|'.join(parts)
                text = '\n'.join(lines) + '\n'
            elif name == 'file-plane-only':
                text = text.replace(LIVE, FILE)
                objects.pop(LIVE)
            for path in paths:
                target = fixture / path
                if path in objects:
                    target.parent.mkdir(parents=True, exist_ok=True)
                    target.write_text(objects[path])
                elif target.exists():
                    target.unlink()
            (fixture / 'PROVINCE.md').write_text(text)
            assert Path(git(fixture, 'rev-parse', '--show-toplevel').strip()) == fixture
            git(fixture, 'add', '--all')
            git(fixture, '-c', 'user.name=R66 fixture', '-c', 'user.email=fixture@example.invalid',
                '-c', 'core.hooksPath=/dev/null', 'commit', '-q', '-m', name)
            rev = git(fixture, 'rev-parse', 'HEAD').strip()
            for label, counter in (('baseline', baseline), ('candidate', candidate)):
                argv = [sys.executable, str(counter), '--repo', str(fixture), '--rev', rev]
                result = run(argv, check=False)
                expected = 0 if name == 'genuine' else 1
                (SEAT / f'{label}-{name}.txt').write_text(
                    'command: ' + ' '.join(argv) + '\n' + result.stdout + result.stderr + f'rc={result.returncode}\n')
                records.append(dict(instrument=label, control=name, revision=rev,
                                    rc=result.returncode, expected=expected, correct=result.returncode == expected))
        summary = {label: sum(row['correct'] for row in records if row['instrument'] == label)
                   for label in ('baseline', 'candidate')}
        (SEAT / 'controls.json').write_text(json.dumps(dict(base=BASE, rows=records, correct=summary), indent=2) + '\n')
        print(json.dumps(summary))
        assert summary == dict(baseline=1, candidate=4)
    finally:
        shutil.rmtree(SCRATCH)
        (SEAT / 'scratch-cleanup.txt').write_text(f'{SCRATCH}: removed={not SCRATCH.exists()}\n')
    return 0


if __name__ == '__main__':
    sys.exit(main())
