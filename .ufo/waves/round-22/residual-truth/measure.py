#!/usr/bin/env python3
"""Replay supplemental discovery guards without changing the original57 target."""
import argparse
import hashlib
import json
from pathlib import Path
import runpy
import sys

ROOT = Path(__file__).resolve().parent
LANE = ROOT.parents[3]
EXPECTED_SHA = "b0b95cb75cdb72cc879063e88042bca24b1c17444d74e944721488605c16418f"


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def verify():
    raw = (ROOT / 'expected.json').read_bytes()
    if hashlib.sha256(raw).hexdigest() != EXPECTED_SHA:
        raise ValueError('snapshot_tampered: residual expectations')
    data = json.loads(raw)
    if len(data['cases']) != 4:
        raise ValueError('incomplete discovery population')
    for case in data['cases']:
        if sha(ROOT / case['fixture']) != case['sha256']:
            raise ValueError('snapshot_tampered: ' + case['id'])
    return data


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--tool', required=True, type=Path)
    parser.add_argument('--new-neighbours-only', action='store_true',
        help='before repair, do not rerun the already reported original red')
    args = parser.parse_args()
    data = verify()
    tool = args.tool.resolve(strict=True)
    tool_sha = sha(tool)
    shared = LANE / '.ufo/waves/round-21/oracle/measure.py'
    helper_sha = sha(shared)
    scan = runpy.run_path(str(shared))['scan']
    cases = data['cases'][1:] if args.new_neighbours_only else data['cases']
    results = []
    for case in cases:
        got = scan(tool, ROOT / case['fixture'])
        payload = got.get('payload', {})
        rows = payload.get('findings', [])
        unparsed = sum(row.get('eval_unparsed', 0) + row.get('unparsed_spawns', 0)
                       for row in payload.get('files', []))
        keys = sorted((row.get('class'), row.get('command'), row.get('evidence')) for row in rows)
        want = sorted((row['class'], row['command'], row['evidence']) for row in case['want'])
        passed = (got.get('exit') in (0, 1) and not got.get('error')
                  and keys == want and unparsed == 0
                  and not any(row.get('command') in case['forbid_any'] for row in rows))
        results.append(dict(id=case['id'], passed=passed, want=case['want'],
                            unparsed=unparsed, got=got))
    verify()
    if sha(tool) != tool_sha or sha(shared) != helper_sha:
        raise ValueError('selected tool or shared scanner runner changed')
    output = dict(schema='mado-r22-residual-lifetime-measure-v1', tool_sha256=tool_sha,
                  runner_sha256=sha(Path(__file__)), expected_sha256=EXPECTED_SHA,
                  shared_scan_helper_sha256=helper_sha, cases=results,
                  totals=dict(passed=sum(row['passed'] for row in results), total=len(results)),
                  new_neighbours_only=args.new_neighbours_only,
                  authority='supplemental discovery guards, original50/57 population unchanged')
    print(json.dumps(output, sort_keys=True))
    return int(not all(row['passed'] for row in results))


if __name__ == '__main__':
    raise SystemExit(main())
