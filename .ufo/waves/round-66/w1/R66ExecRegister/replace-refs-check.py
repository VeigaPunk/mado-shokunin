#!/usr/bin/env python3
"""Verify planted refs/replace cannot steer rev byte reads (R66SentFrontier finding)."""
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
HEADING = '### Surface state register (2026-11-03'
END = '<!-- r65 register end -->'
CANDIDATE = SEAT / 'c1-r66-register.py'
ENV = {k: v for k, v in os.environ.items() if not k.startswith('GIT_')}
ENV.update(GIT_CONFIG_NOSYSTEM='1', GIT_CONFIG_GLOBAL='/dev/null', GIT_OPTIONAL_LOCKS='0', PYTHONDONTWRITEBYTECODE='1')


def git(repo, *args, steered=False):
    argv = ['git'] + (['--no-replace-objects'] if not steered else []) + ['-C', str(repo), *args]
    result = subprocess.run(argv, cwd=SEAT, env=ENV, capture_output=True, text=True, timeout=120)
    if result.returncode:
        raise RuntimeError(f'{argv!r}: rc={result.returncode}\n{result.stderr}')
    return result.stdout


def commit(fixture, message):
    assert Path(git(fixture, 'rev-parse', '--show-toplevel').strip()) == fixture
    git(fixture, 'add', '--all')
    git(fixture, '-c', 'user.name=R66 fixture', '-c', 'user.email=fixture@example.invalid',
        '-c', 'core.hooksPath=/dev/null', 'commit', '-q', '-m', message)
    return git(fixture, 'rev-parse', 'HEAD').strip()


def run(argv, check=True):
    result = subprocess.run(argv, cwd=SEAT, env=ENV, capture_output=True, text=True, timeout=120)
    if check and result.returncode:
        raise RuntimeError(f'{argv!r}: rc={result.returncode}\n{result.stderr}')
    return result


def main():
    SCRATCH.mkdir(parents=True)
    lines_out = []
    try:
        fixture = SCRATCH / 'replace-fixture'
        fixture.mkdir()
        git(fixture, 'init', '-q')
        province = git(LANE, '--no-replace-objects', 'show', f'{BASE}:PROVINCE.md')
        live = git(LANE, '--no-replace-objects', 'show', f'{BASE}:{LIVE}')
        invalid = province.replace('| walker |', '| walker |').replace(
            province[province.index('| walker |'):province.index('\n', province.index('| walker |'))],
            next(line for line in province.splitlines() if line.startswith('| walker |')).replace(
                '.ufo/waves/round-65/receipts/', ''))
        lines_out.append(f'walker row invalid (receipt tokens stripped): '
                         f'{".ufo" not in next(line for line in invalid.splitlines() if line.startswith("| walker |"))}')
        (fixture / 'PROVINCE.md').write_text(province)
        live_path = fixture / LIVE
        live_path.parent.mkdir(parents=True, exist_ok=True)
        live_path.write_text(live)
        genuine_rev = commit(fixture, 'genuine')
        (fixture / 'PROVINCE.md').write_text(invalid)
        invalid_rev = commit(fixture, 'invalid walker receipt')
        git(fixture, 'replace', invalid_rev, genuine_rev)
        lines_out.append(f'invalid={invalid_rev[:12]} replace->genuine={genuine_rev[:12]}')
        lines_out.append(f'steered plain git show reads genuine bytes: '
                         f'{".ufo" in subprocess.run(["git", "-C", str(fixture), "show", f"{invalid_rev}:PROVINCE.md"], capture_output=True, text=True, env=ENV).stdout}')
        argv = [sys.executable, str(CANDIDATE), '--repo', str(fixture), '--rev', invalid_rev]
        result = run(argv, check=False)
        lines_out.append('command: ' + ' '.join(argv))
        lines_out.extend((result.stdout + result.stderr).strip().splitlines())
        lines_out.append(f'rc={result.returncode} (expected 1 TARGET_MISSED reading exact invalid bytes)')
        receipt = SEAT / 'replace-refs.txt'
        receipt.write_text('\n'.join(lines_out) + '\n')
        assert result.returncode == 1, 'candidate must read exact committed bytes'
        print(f'replace-refs guard: PASS (rc={result.returncode}, receipts={receipt.name})')
    finally:
        shutil.rmtree(SCRATCH)
        receipt = SEAT / 'scratch-cleanup.txt'
        receipt.write_text(f'{SCRATCH}: removed={not SCRATCH.exists()}\n')
    return 0


if __name__ == '__main__':
    sys.exit(main())
