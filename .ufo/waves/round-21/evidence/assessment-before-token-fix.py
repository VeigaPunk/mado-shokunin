#!/usr/bin/env python3
"""Read-only artifact assertion gate, not independent authentication of its author.

--check BUNDLE --root ROOT validates an assessment. --selftest ROOT replays the
independently frozen round-21 fixtures. Exit 0 clean, 1 failed, 2 cannot evaluate.
No classifier, transcript evaluation, Git, host state or network is consulted.
"""
import argparse
import datetime as dt
import hashlib
import json
import re
import subprocess
import sys
from pathlib import Path, PurePosixPath

SEAL_SHA = '99516c349637f2aefaef5c106ec7973c8af638bd4a22c79c835a49e0559fe686'
MAX_BYTES = 2 * 1024 * 1024
SHA = re.compile(r'[0-9a-f]{64}\Z')
SUBJECTS = {
    1: 'SKILL.md contains real decision tables, error patterns, checklists, cited sources',
    2: 'At least one end-to-end domain task executed and logged in LOG.md',
    3: 'Instructions executable by an agent without oral context',
    4: 'No cross-domain bleed (PROVINCE.md still accurate)',
}


class Invalid(ValueError):
    pass


def pairs(items):
    result = {}
    for key, value in items:
        if key in result:
            raise Invalid('duplicate JSON key: ' + key)
        result[key] = value
    return result


def read_bytes(path):
    with path.open('rb') as stream:
        raw = stream.read(MAX_BYTES + 1)
    if len(raw) > MAX_BYTES:
        raise Invalid('input exceeds bounded read')
    return raw


def load(path):
    return json.loads(read_bytes(path), object_pairs_hook=pairs,
                      parse_constant=lambda value: (_ for _ in ()).throw(Invalid('nonfinite JSON')))


def rooted(root, name):
    if not isinstance(name, str) or not name or '\\' in name:
        raise Invalid('invalid relative path')
    relative = PurePosixPath(name)
    if relative.is_absolute() or any(part in ('..', '.') for part in name.split('/')):
        raise Invalid('path traversal')
    candidate = root
    for part in relative.parts:
        candidate = candidate / part
        if candidate.is_symlink():
            raise Invalid('symlink input')
    if not candidate.is_file() or not candidate.resolve().is_relative_to(root):
        raise Invalid('missing or escaping input')
    return candidate


def require(obj, key, typ):
    if not isinstance(obj, dict) or key not in obj or type(obj[key]) is not typ:
        raise Invalid('missing or invalid ' + key)
    return obj[key]


def timestamp(value):
    if not isinstance(value, str) or not re.fullmatch(r'\d{4}-\d\d-\d\dT\d\d:\d\d:\d\d(?:\.\d+)?(?:Z|[+-]\d\d:\d\d)', value):
        raise Invalid('malformed timestamp')
    value = dt.datetime.fromisoformat(value.replace('Z', '+00:00'))
    if value.utcoffset() is None:
        raise Invalid('timezone required')
    return value


def digest(value):
    if not isinstance(value, str) or SHA.fullmatch(value) is None:
        raise Invalid('missing or invalid sha256')
    return value


def check(bundle, root):
    data = load(bundle)
    registration = timestamp(require(data, 'registration_time', str))
    implementation = timestamp(require(data, 'implementation_time', str))
    measurements = require(data, 'measurements', list)
    population = require(data, 'population', list)
    oracle = require(data, 'oracle', dict)
    shonen = require(data, 'shonen', list)
    history = require(data, 'history', dict)
    if not measurements or not population or len(measurements) > 10000 or len(population) > 10000:
        raise Invalid('empty or oversized population/measurements')
    measured = [timestamp(require(row, 'time', str)) for row in measurements]
    failures, actual = [], []
    if registration >= implementation or any(registration >= value for value in measured):
        failures.append('late_registration')
    seen_paths = set()
    for row in population:
        name = require(row, 'path', str)
        if name in seen_paths:
            raise Invalid('duplicate population identity')
        seen_paths.add(name)
        expected = digest(require(row, 'sha256', str))
        found = hashlib.sha256(read_bytes(rooted(root, name))).hexdigest()
        actual.append({'path': name, 'sha256': found})
        if found != expected:
            failures.append('population_digest_changed')
    author = require(oracle, 'author', str)
    if not author.strip():
        raise Invalid('empty oracle author')
    independent = require(oracle, 'independent', bool)
    if not independent or 'tool-generated' in author.casefold():
        failures.append('oracle_not_independent')
    registered = digest(require(oracle, 'registered_expectations_sha256', str))
    current = digest(require(oracle, 'expectations_sha256', str))
    actual_expectations = hashlib.sha256(read_bytes(rooted(root, 'expected.json'))).hexdigest()
    if current != registered or actual_expectations != registered:
        failures.append('expectations_changed')
    if len(shonen) != 4:
        raise Invalid('canonical four-box assessment incomplete')
    seen = set()
    for row in shonen:
        box = require(row, 'box', int)
        if box not in SUBJECTS or box in seen:
            raise Invalid('duplicate or invalid assessment box')
        seen.add(box)
        mark = require(row, 'mark', str)
        evidence = require(row, 'evidence', str)
        if not evidence.strip():
            raise Invalid('empty assessment evidence')
        if mark not in ('~', 'x'):
            raise Invalid('invalid assessment mark')
        # This checks the declared subject, not whether its evidence proves it.
        if SUBJECTS[box].casefold() not in evidence.casefold():
            failures.append('wrong_topic_shonen')
        if mark == 'x' and re.search(r'\bnon-author verifier:\s*[A-Za-z0-9][A-Za-z0-9_.-]*', evidence) is None:
            failures.append('unnamed_nonauthor_verifier')
    for key, expected in {'round20_target': 175, 'round20_pass': 172,
                          'round20_admitted': False, 'c2_independent': False}.items():
        value = require(history, key, type(expected))
        if value != expected:
            failures.append('historical_target_rewritten')
    return {'code': int(bool(failures)), 'result': 'failed' if failures else 'clean',
            'finding_ids': sorted(set(failures)) if failures else ['assessment_clean'],
            'actual_inputs': actual, 'actual_expectations_sha256': actual_expectations,
            'authority': 'artifact assertions only; no authenticated chronology, authorship, semantic proof or promotion authority'}


def evaluate(bundle, root):
    try:
        return check(bundle, root)
    except (OSError, ValueError, TypeError, KeyError, RecursionError) as exc:
        return {'code': 2, 'result': 'could-not-evaluate', 'finding_ids': ['assessment_input_invalid'],
                'error': str(exc)}


def selftest(root):
    seal_path = rooted(root, 'seal.json')
    if hashlib.sha256(read_bytes(seal_path)).hexdigest() != SEAL_SHA:
        raise Invalid('snapshot_tampered: seal')
    seal = load(seal_path)
    for row in seal['files']:
        if hashlib.sha256(read_bytes(rooted(root, row['path']))).hexdigest() != row['sha256']:
            raise Invalid('snapshot_tampered: ' + row['path'])
    expected = load(rooted(root, 'expected.json'))
    expected_ids = {
        'late_registration_after_measurement': 'late_registration',
        'late_registration_after_implementation': 'late_registration',
        'population_file_mutated': 'population_digest_changed',
        'oracle_tool_generated_not_independent': 'oracle_not_independent',
        'expectation_digest_changed': 'expectations_changed',
        'shonen_x_without_nonauthor': 'unnamed_nonauthor_verifier',
        'history_suppresses_old_three_misses': 'historical_target_rewritten',
        'history_round20_admitted_true': 'historical_target_rewritten',
        'history_c2_independent_true': 'historical_target_rewritten',
        'round20_wrong_topic_shonen': 'wrong_topic_shonen',
    }
    results = []
    for case in expected['cases']:
        path = rooted(root, case['fixture'])
        cmd = [sys.executable, '-I', str(Path(__file__).resolve()), '--root', str(root), '--check', str(path)]
        proc = subprocess.run(cmd, text=True, capture_output=True, timeout=10)
        got = json.loads(proc.stdout)
        finding = expected_ids.get(case['id'], 'assessment_clean' if case['expected']['code'] == 0
                                   else 'assessment_input_invalid')
        passed = (proc.returncode == case['expected']['code'] and got['code'] == proc.returncode
                  and got['result'] == case['expected']['result']
                  and finding in got.get('finding_ids', []))
        results.append({'id': case['id'], 'pass': passed, 'got': got, 'want': case['expected'], 'exit': proc.returncode})
    output = {'code': int(not all(row['pass'] for row in results)), 'result': 'selftest',
              'finding_ids': ['assessment_oracle_match'] if all(row['pass'] for row in results) else ['assessment_oracle_mismatch'],
              'pass': sum(row['pass'] for row in results), 'total': len(results), 'cases': results,
              'seal_sha256': SEAL_SHA, 'tool_sha256': hashlib.sha256(read_bytes(Path(__file__))).hexdigest()}
    return output


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument('--check', type=Path)
    mode.add_argument('--selftest', type=Path)
    parser.add_argument('--root', type=Path)
    args = parser.parse_args()
    try:
        if args.selftest:
            output = selftest(args.selftest.resolve(strict=True))
        elif args.root:
            root = args.root.resolve(strict=True)
            if args.check.is_symlink():
                raise Invalid('symlink assessment')
            output = evaluate(args.check, root)
        else:
            raise Invalid('--root is required with --check')
    except (OSError, ValueError, KeyError, TypeError, subprocess.SubprocessError) as exc:
        output = {'code': 2, 'result': 'could-not-evaluate', 'finding_ids': ['assessment_input_invalid'], 'error': str(exc)}
    print(json.dumps(output, sort_keys=True))
    return output['code']


if __name__ == '__main__':
    raise SystemExit(main())
