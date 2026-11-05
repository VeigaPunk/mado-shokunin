#!/usr/bin/env python3
"""Run only the assigned frozen no-work controls; caller supplies isolated scratch."""
import concurrent.futures
import io
import os
from pathlib import Path
import shlex
import subprocess
import sys
import tarfile

REPO = '/home/vgpnk/Projects/shokunin/mado-shokunin'
REV = '237ecf4e69a4986108f719f3beeafe111adaa033'
S = Path(sys.argv[1])
SNAP = S / 'snapshot'
SNAP.mkdir(parents=True, exist_ok=True)
env = dict(os.environ, TMPDIR=str(S), PYTHONDONTWRITEBYTECODE='1')

def git(*args):
    return subprocess.check_output(['git', '-C', REPO, *args], env=env)

# Read-only frozen snapshot; borrow object database without creating a commit or worktree.
with tarfile.open(fileobj=io.BytesIO(git('archive', REV))) as archive:
    archive.extractall(SNAP, members=(m for m in archive if m.isfile() or m.isdir()), filter='data')
(SNAP / '.git').symlink_to(git('rev-parse', '--absolute-git-dir').decode().strip(), target_is_directory=True)

jobs = [
    ('c1-held-r85-on-r86', 'c1-r85-identity-causes.py', 'c1-cases-r86.json', 'c1-cases-r84.json', 'round-84', ['--base-rev', '2b6dd76b65de4dfe701db87db13b7e448b3538ee']),
    ('c1-r86-flood-and-held', 'c1-r86-refusal-records.py', 'c1-cases-r86.json', 'c1-cases-r85.json', 'round-85', ['--base-rev', '2b6dd76b65de4dfe701db87db13b7e448b3538ee', '--no-mutants']),
    ('c2-held-r85-on-r85', 'c2-r85-status-classes.py', 'c2-cases-r85.json', 'c2-runbook-cases-r84.json', 'round-84', []),
    ('c2-r86-new-witness', 'c2-r86-clause-observations.py', 'c2-cases-r86.json', 'c2-cases-r85.json', 'round-85', ['--no-mutants']),
]

def run(job):
    label, instrument, controls, carried, carried_round, extra = job
    control_round = 'round-85' if label == 'c2-held-r85-on-r85' else 'round-86'
    argv = [sys.executable, '-I', str(SNAP / 'quality/counters' / instrument), '--repo', str(SNAP), '--rev', REV,
            '--controls', str(SNAP / '.ufo/waves' / control_round / 'controls' / controls),
            '--carried', str(SNAP / '.ufo/waves' / carried_round / 'controls' / carried),
            '--scratch-root', str(S / label), *extra]
    p = subprocess.run(argv, cwd=S, env=env, capture_output=True, text=True)
    return label, argv, p

with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
    for label, argv, p in pool.map(run, jobs):
        print('\n## ' + label, flush=True)
        print('COMMAND: TMPDIR=' + shlex.quote(str(S)) + ' ' + shlex.join(argv), flush=True)
        print('RC: ' + str(p.returncode), flush=True)
        print(p.stdout, end='', flush=True)
        if p.stderr:
            print('STDERR:\n' + p.stderr, end='', flush=True)
