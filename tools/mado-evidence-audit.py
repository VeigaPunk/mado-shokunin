#!/usr/bin/env python3
"""Audit artifact arithmetic and explicit evidence labels, never execution truth.

--check BUNDLE --root ROOT: 0 consistent assertions, 1 contradicted assertions,
2 could-not-evaluate. --selftest FIXTURES replays the sealed, independently
specified cases through this CLI. No classifier, host probe, Git, network,
authenticated chronology, admission or promotion authority is consulted.
"""
import argparse
import hashlib
import json
import math
import os
from pathlib import Path, PurePosixPath
import re
import stat
import subprocess
import sys

MAX_BYTES = 2 * 1024 * 1024
SHA = re.compile(r'[0-9a-f]{64}\Z')
AUTHORITY = 'artifact assertions only; labels are not semantic proof, authentication, admission or promotion'


class Invalid(ValueError):
    pass


def pairs(items):
    result = {}
    for key, value in items:
        if key in result:
            raise Invalid('duplicate JSON key')
        result[key] = value
    return result


def finite(value):
    pending = [value]
    while pending:
        item = pending.pop()
        if isinstance(item, float) and not math.isfinite(item):
            raise Invalid('nonfinite JSON number')
        if isinstance(item, dict):
            pending.extend(item.values())
        elif isinstance(item, list):
            pending.extend(item)
    return value


def parse(raw):
    return finite(json.loads(raw.decode('utf-8'), object_pairs_hook=pairs,
        parse_constant=lambda value: (_ for _ in ()).throw(Invalid('nonfinite JSON number'))))


def bounded(path):
    root_path(path.parent)
    if path.is_symlink() or not path.is_file():
        raise Invalid('nonregular or symlink input')
    with path.open('rb') as stream:
        raw = stream.read(MAX_BYTES + 1)
    if len(raw) > MAX_BYTES:
        raise Invalid('input exceeds 2 MiB')
    return raw


def require(obj, key, typ):
    if not isinstance(obj, dict) or key not in obj or type(obj[key]) is not typ:
        raise Invalid('missing or invalid ' + key)
    return obj[key]


def count(obj, key):
    value = require(obj, key, int)
    if value < 0:
        raise Invalid('negative ' + key)
    return value


def relative(name):
    if (not isinstance(name, str) or not name or '\\' in name
            or PurePosixPath(name).is_absolute()
            or any(part in ('', '.', '..') for part in name.split('/'))):
        raise Invalid('invalid relative path')
    return Path(*PurePosixPath(name).parts)


def root_path(value):
    root = Path(os.path.abspath(value))
    if any(path.is_symlink() for path in (root, *root.parents)):
        raise Invalid('symlink root')
    if not root.is_dir():
        raise Invalid('missing root')
    return root


def rooted(root, name):
    path = root
    for part in relative(name).parts:
        path = path / part
        if path.is_symlink():
            raise Invalid('symlink input')
    if not path.is_file() or not path.resolve().is_relative_to(root):
        raise Invalid('missing or escaping input')
    return path


def sha_file(path):
    digest = hashlib.sha256()
    with path.open('rb') as stream:
        for chunk in iter(lambda: stream.read(65536), b''):
            digest.update(chunk)
    return digest.hexdigest()


def result(code, ids, **extra):
    return dict(code=code, result=('clean', 'failed', 'could-not-evaluate')[code],
                finding_ids=sorted(set(ids)), authority=AUTHORITY, **extra)


def check(bundle, root):
    data = parse(bounded(bundle))
    name = require(data, 'snapshot', str)
    expected = require(data, 'sha256', str)
    if SHA.fullmatch(expected) is None:
        raise Invalid('invalid sha256')
    raw = bounded(rooted(root_path(root), name))
    found = hashlib.sha256(raw).hexdigest()
    if found != expected:
        return result(2, ['snapshot_tampered'], actual_snapshot_sha256=found)
    snapshot = parse(raw)
    findings = require(snapshot, 'findings', list)
    files = require(snapshot, 'files', list)
    if not files:
        raise Invalid('empty file population')
    actual = dict(total=len(findings), observed=0, lead=0, errors=0)
    for row in findings:
        marker = require(row, 'evidence', str)
        if marker not in ('observed', 'lead'):
            raise Invalid('invalid evidence marker')
        for key in ('class', 'command'):
            if not require(row, key, str).strip():
                raise Invalid('empty finding ' + key)
        actual[marker] += 1
    for row in files:
        actual['errors'] += count(row, 'eval_unparsed') + count(row, 'unparsed_spawns')
    claim = require(data, 'claim', dict)
    declared = {key: count(claim, key) for key in actual}
    clean = require(claim, 'clean', bool)
    failures = []
    for key, finding in (('total', 'finding_count_mismatch'),
                         ('observed', 'observed_count_mismatch'),
                         ('lead', 'lead_count_mismatch'),
                         ('errors', 'error_count_mismatch')):
        if declared[key] != actual[key]:
            failures.append(finding)
    if clean and actual['errors']:
        failures.append('uncertain_scan_claimed_clean')
    if clean and actual['total']:
        failures.append('findings_claimed_clean')
    return result(int(bool(failures)), failures or ['evidence_audit_clean'],
                  actual_counts=actual, actual_snapshot_sha256=found)


def evaluate(bundle, root):
    try:
        return check(bundle, root)
    except (OSError, ValueError, TypeError, KeyError, OverflowError, RecursionError) as exc:
        return result(2, ['evidence_audit_input_invalid'], error=type(exc).__name__)


def inventory(root, entries):
    if not isinstance(entries, list) or not entries or len(entries) > 10000:
        raise Invalid('empty or invalid inventory')
    seen = set()
    for entry in entries:
        name = require(entry, 'path', str)
        if name in seen:
            raise Invalid('duplicate inventory path')
        seen.add(name)
        rel = relative(name)
        path = root / rel
        for parent in rel.parents:
            if (root / parent).is_symlink():
                raise Invalid('symlink inventory ancestor')
        kind = require(entry, 'kind', str)
        mode = path.lstat().st_mode
        if kind == 'file':
            if not stat.S_ISREG(mode):
                raise Invalid('nonregular inventory file')
            expected = require(entry, 'sha256', str)
            size = count(entry, 'size_bytes')
            if SHA.fullmatch(expected) is None or path.stat().st_size != size or sha_file(path) != expected:
                raise Invalid('snapshot_tampered: inventory')
        elif kind == 'directory':
            if not stat.S_ISDIR(mode):
                raise Invalid('changed inventory directory')
        elif kind == 'symlink':
            if not stat.S_ISLNK(mode) or os.readlink(path) != require(entry, 'target', str):
                raise Invalid('changed inventory symlink')
        else:
            raise Invalid('invalid inventory kind')
    return seen


def selftest(fixtures):
    root = root_path(fixtures)
    expected_path = rooted(root, 'expected.json')
    raw = bounded(expected_path)
    expected_sha = hashlib.sha256(raw).hexdigest()
    if bounded(rooted(root, 'expected.sha256')).decode('ascii') != expected_sha + '  expected.json\n':
        raise Invalid('snapshot_tampered: expected.json')
    manifest = parse(raw)
    if require(manifest, 'schema', str) != 'mado-r22-audit-fixtures-v1':
        raise Invalid('unsupported fixture schema')
    cases = require(manifest, 'cases', list)
    if not cases or len(cases) > 10000:
        raise Invalid('empty or oversized fixture population')
    entries = require(manifest, 'input_entries', list)
    members = inventory(root, entries)
    seen, rows = set(), []
    tool_sha = sha_file(Path(__file__))
    for case in cases:
        name = require(case, 'id', str)
        if not name or name in seen:
            raise Invalid('duplicate or empty case identity')
        seen.add(name)
        bundle_name = require(case, 'bundle', str)
        bundle = rooted(root, bundle_name)
        if bundle_name not in members or sha_file(bundle) != require(case, 'bundle_sha256', str):
            raise Invalid('unbound fixture bundle')
        case_root = root_path(root / relative(require(case, 'root', str)))
        expected = require(case, 'expected', dict)
        code = count(expected, 'code')
        ids = require(expected, 'finding_ids', list)
        if code not in (0, 1, 2) or not ids or any(type(value) is not str for value in ids):
            raise Invalid('invalid case expectation')
        proc = subprocess.run([sys.executable, '-I', str(Path(__file__).resolve()),
            '--check', str(bundle), '--root', str(case_root)], capture_output=True, timeout=15)
        try:
            observed = parse(proc.stdout)
            observed_code = require(observed, 'code', int)
            observed_ids = require(observed, 'finding_ids', list)
        except (ValueError, TypeError, KeyError):
            observed_code, observed_ids = None, []
        passed = (proc.returncode == code == observed_code and
                  sorted(ids) == observed_ids and not proc.stderr)
        rows.append(dict(id=name, passed=passed, expected=expected,
                         actual_code=observed_code, actual_ids=observed_ids,
                         process_exit=proc.returncode))
    inventory(root, entries)
    if bounded(expected_path) != raw or sha_file(Path(__file__)) != tool_sha:
        raise Invalid('input or tool changed during selftest')
    passed = sum(row['passed'] for row in rows)
    return result(int(passed != len(rows)),
                  ['evidence_audit_selftest_clean' if passed == len(rows) else 'evidence_audit_selftest_failed'],
                  passed=passed, total=len(rows), cases=rows, expected_sha256=expected_sha,
                  tool_sha256=tool_sha)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument('--check', type=Path)
    mode.add_argument('--selftest', type=Path)
    parser.add_argument('--root', type=Path)
    args = parser.parse_args()
    if args.check:
        output = evaluate(args.check, args.root) if args.root is not None else result(2, ['evidence_audit_input_invalid'])
    else:
        try:
            output = selftest(args.selftest)
        except (OSError, ValueError, TypeError, KeyError, OverflowError, RecursionError, subprocess.SubprocessError) as exc:
            output = result(2, ['evidence_audit_input_invalid'], error=type(exc).__name__)
    print(json.dumps(output, sort_keys=True))
    return output['code']


if __name__ == '__main__':
    raise SystemExit(main())
