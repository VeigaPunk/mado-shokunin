#!/usr/bin/env python3
"""Replay every committed fixture path; retain all removed/relabelled rows."""
import argparse
import hashlib
import importlib.util
import json
import resource
import signal
import subprocess
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parent
MANIFEST_SHA = '8e1cf206c85563b418630ef1d094559a9522431ff4e077ca1b51f249436a1377'


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def manifest():
    path = ROOT / 'snapshot/manifest.json'
    if sha(path) != MANIFEST_SHA:
        raise ValueError('snapshot_tampered: manifest')
    data = json.loads(path.read_text())
    for row in data['files']:
        path = ROOT / 'snapshot/files' / row['path']
        if sha(path) != row['sha256']:
            raise ValueError('snapshot_tampered: ' + row['path'])
    return data


def expired(signum, frame):
    raise TimeoutError('per-file 15-second deadline')


def worker(tool):
    resource.setrlimit(resource.RLIMIT_AS, (384 * 1024 * 1024, 384 * 1024 * 1024))
    data = manifest()
    spec = importlib.util.spec_from_file_location('corpus_tripwire', tool)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    signal.signal(signal.SIGALRM, expired)
    for row in data['files']:
        path = ROOT / 'snapshot/files' / row['path']
        signal.alarm(15)
        try:
            stats, findings = module.scan_file(str(path))
            result = {'path': row['path'], 'stats': stats, 'findings': findings}
        except (Exception, MemoryError) as exc:
            result = {'path': row['path'], 'error': type(exc).__name__ + ': ' + str(exc)}
        finally:
            signal.alarm(0)
        print(json.dumps(result, sort_keys=True), flush=True)


def key(row):
    return (row['line'], row.get('tool_call_id'), row['class'], row['rule'], row['command'], row.get('evidence', 'observed'))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--before-tool', type=Path)
    parser.add_argument('--after-tool', type=Path)
    parser.add_argument('--worker', type=Path)
    args = parser.parse_args()
    if args.worker:
        worker(args.worker.resolve(strict=True))
        return 0
    if not args.before_tool or not args.after_tool:
        parser.error('both tools required')
    data = manifest()
    runs = []
    for tool in (args.before_tool, args.after_tool):
        tool_before = sha(tool)
        proc = subprocess.run([sys.executable, '-I', str(Path(__file__).resolve()), '--worker', str(tool.resolve())],
                              capture_output=True, text=True, timeout=600)
        rows = [json.loads(line) for line in proc.stdout.splitlines()]
        if proc.returncode or len(rows) != len(data['files']):
            raise ValueError('incomplete corpus run: ' + proc.stderr[-2000:])
        if sha(tool) != tool_before:
            raise ValueError('selected tool changed during corpus run')
        for observed, frozen in zip(rows, data['files']):
            if observed.get('path') != frozen['path']:
                raise ValueError('missing/duplicate/substituted corpus member')
            if 'error' not in observed:
                stats = observed.get('stats', {})
                path = str(ROOT / 'snapshot/files' / frozen['path'])
                if stats.get('sha256') != frozen['sha256'] or stats.get('path') != path:
                    raise ValueError('worker input attribution mismatch')
                if any(finding.get('file') != path for finding in observed.get('findings', [])):
                    raise ValueError('worker finding attribution mismatch')
        manifest()  # reject input drift during execution, never relabel it a match
        runs.append(rows)
    lost, added, errors = [], [], []
    retained = 0
    for before, after in zip(*runs):
        if before['path'] != after['path']:
            raise ValueError('population order mismatch')
        if 'error' in before or 'error' in after:
            errors.append({'path': before['path'], 'before': before.get('error'), 'after': after.get('error')})
            continue
        old = Counter(key(row) for row in before['findings'])
        new = Counter(key(row) for row in after['findings'])
        retained += sum((old & new).values())
        lost.extend({'path': before['path'], 'row': list(row), 'count': n} for row, n in (old - new).items())
        added.extend({'path': before['path'], 'row': list(row), 'count': n} for row, n in (new - old).items())
    print(json.dumps({'manifest_sha256': MANIFEST_SHA, 'files': len(data['files']),
                      'before_tool_sha256': sha(args.before_tool), 'after_tool_sha256': sha(args.after_tool),
                      'runner_sha256': sha(Path(__file__)), 'retained': retained,
                      'removed_or_relabelled': lost, 'added_or_relabelled': added, 'errors': errors,
                      'runs': {'before': runs[0], 'after': runs[1]}}, sort_keys=True))
    return int(bool(errors))


if __name__ == '__main__':
    raise SystemExit(main())
