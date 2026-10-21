#!/usr/bin/env python3
"""Compare a selected scanner with sealed independently proposed static truth."""
import argparse
import hashlib
import json
import resource
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
CAP = 384 * 1024 * 1024
WRAPPER = '''import importlib.util,sys
s=importlib.util.spec_from_file_location("selected_tripwire",sys.argv[1])
m=importlib.util.module_from_spec(s);s.loader.exec_module(m)
sys.exit(m.main(["--scan",sys.argv[2]]))
'''


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def cap():
    resource.setrlimit(resource.RLIMIT_AS, (CAP, CAP))


def scan(tool, fixture):
    cmd = [sys.executable, '-I', '-c', WRAPPER, str(tool), str(fixture)]
    try:
        p = subprocess.run(cmd, capture_output=True, text=True, timeout=15, preexec_fn=cap)
    except subprocess.TimeoutExpired:
        return {'error': 'timeout', 'command': cmd}
    try:
        payload = json.loads(p.stdout.splitlines()[-1])
    except (ValueError, IndexError):
        return {'error': 'invalid scanner output', 'exit': p.returncode, 'stdout': p.stdout, 'stderr': p.stderr}
    return {'exit': p.returncode, 'payload': payload, 'stderr': p.stderr}


def rows_key(rows):
    return sorted((r['class'], r['command'], r.get('evidence', 'observed')) for r in rows)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--tool', required=True, type=Path)
    args = parser.parse_args()
    tool = args.tool.resolve(strict=True)
    raw = (ROOT / 'expected.json').read_bytes()
    expected_sha = (ROOT / 'expected.sha256').read_text().split()[0]
    if hashlib.sha256(raw).hexdigest() != expected_sha:
        raise SystemExit('snapshot_tampered: expected.json')
    expected = json.loads(raw)
    for case in expected['cases']:
        if sha(ROOT / case['fixture']) != case['sha256']:
            raise SystemExit('snapshot_tampered: ' + case['fixture'])
    result = {'tool_sha256': sha(tool), 'runner_sha256': sha(Path(__file__)), 'expected_sha256': expected_sha, 'cases': [], 'totals': {}}
    for case in expected['cases']:
        got = scan(tool, ROOT / case['fixture'])
        payload = got.get('payload', {})
        findings = payload.get('findings', [])
        unparsed = sum(entry.get('eval_unparsed', 0) + entry.get('unparsed_spawns', 0) for entry in payload.get('files', []))
        passed = got.get('exit') in (0, 1) and not got.get('error') and not unparsed and rows_key(findings) == rows_key(case['want'])
        row = {'id': case['id'], 'group': case['group'], 'pass': passed, 'want': case['want'], 'got': got}
        result['cases'].append(row)
        total = result['totals'].setdefault(case['group'], {'pass': 0, 'total': 0})
        total['total'] += 1
        total['pass'] += int(passed)
    print(json.dumps(result, sort_keys=True))
    return 0 if all(row['pass'] for row in result['cases']) else 1


if __name__ == '__main__':
    raise SystemExit(main())
