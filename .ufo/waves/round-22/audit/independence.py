#!/usr/bin/env python3
"""Future-use C2 independence intervention; never executes transcript payloads.

Usage (after sealing and implementation):
  python3 -I .ufo/waves/round-22/audit/independence.py \
    --revision COMMIT --baseline 741122d --fixtures LANE_RELATIVE_ROOT

Only tracked bytes from COMMIT are staged (git archive, never recursive copying).
The complete cases list comes exclusively from the sealed expected.json schema
mado-r22-audit-fixtures-v1, with each case's exact bundle and root paths.
expected.sha256 and the full input_entries inventory are validated before use.
No result establishes
universal noninterference: FIFO detects blocking opens, marker detects ordinary
execution/import, not stat-only, nonblocking opens, or deliberate evasion.
Output is one JSON receipt; 0 intervention supported, 1 falsified, 2 unavailable.
No changes to the source checkout, index, host configuration, or candidate tools.
"""
import argparse
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import resource
import signal
import stat
import subprocess
import sys
import tarfile
import tempfile

LIMIT = 384 * 1024 * 1024
OUTPUT_LIMIT = 1024 * 1024
TOOL = 'tools/mado-evidence-audit.py'
CLASSIFIER = 'tools/mado-tripwire.py'
BASELINE = '741122d177ae8ff68a73768777f20484d5bdcbe4'
LANE = Path(__file__).resolve().parents[4]


def digest(data):
    return hashlib.sha256(data).hexdigest()


def relative(value, inventory=False):
    if inventory and value == '.':
        return Path('.')
    p = PurePosixPath(value)
    if not value or ('\\' in value and not inventory) or p.is_absolute() or any(
            part in ('', '.', '..') for part in value.split('/')):
        raise ValueError('unsafe relative path: ' + value)
    return Path(*p.parts)


def regular(root, rel):
    path = root
    for part in rel.parts:
        path = path / part
        if path.is_symlink():
            raise ValueError('symlink input: ' + str(rel))
    if not path.is_file():
        raise ValueError('missing regular input: ' + str(rel))
    return path


def git(*args):
    p = subprocess.run(['git', '-C', str(LANE), *args], capture_output=True,
                       timeout=120, check=False)
    if p.returncode:
        raise ValueError('git failed: ' + p.stderr.decode('utf-8', 'replace'))
    return p.stdout


def tree_hash(root):
    rows = []
    for path in sorted(root.rglob('*')):
        mode = path.lstat().st_mode
        rel = path.relative_to(root).as_posix()
        if stat.S_ISLNK(mode):
            rows.append([rel, 'symlink', os.readlink(path)])
        elif stat.S_ISREG(mode):
            rows.append([rel, 'file', digest(path.read_bytes())])
        elif not stat.S_ISDIR(mode):
            raise ValueError('nonregular fixture member: ' + rel)
    return digest(json.dumps(rows, separators=(',', ':')).encode())


def caps():
    resource.setrlimit(resource.RLIMIT_AS, (LIMIT, LIMIT))
    resource.setrlimit(resource.RLIMIT_FSIZE, (OUTPUT_LIMIT, OUTPUT_LIMIT))
    resource.setrlimit(resource.RLIMIT_CORE, (0, 0))


def run(argv, stage, work):
    # File-backed pipes avoid unlimited capture allocation. Kill the entire owned
    # process group, including descendants, even if the initial child has exited.
    with tempfile.TemporaryFile(dir=work) as out, tempfile.TemporaryFile(dir=work) as err:
        proc = subprocess.Popen(argv, cwd=stage, stdin=subprocess.DEVNULL,
                                stdout=out, stderr=err, start_new_session=True,
                                preexec_fn=caps, env={
                                    'PATH': os.defpath, 'HOME': str(work),
                                    'TMPDIR': str(work), 'LC_ALL': 'C.UTF-8',
                                    'PYTHONDONTWRITEBYTECODE': '1'})
        timed_out = False
        try:
            proc.wait(timeout=15)
        except subprocess.TimeoutExpired:
            timed_out = True
        finally:
            try:
                os.killpg(proc.pid, signal.SIGKILL)
            except ProcessLookupError:
                pass
            proc.wait()
        out.seek(0)
        err.seek(0)
        stdout = out.read(OUTPUT_LIMIT + 1)
        stderr = err.read(OUTPUT_LIMIT + 1)
    return {'argv': argv, 'exit': proc.returncode, 'timeout': timed_out,
            'stdout': stdout.decode('utf-8', 'replace'),
            'stderr': stderr.decode('utf-8', 'replace'),
            'stdout_sha256': digest(stdout), 'stderr_sha256': digest(stderr),
            'output_bound_hit': len(stdout) >= OUTPUT_LIMIT or len(stderr) >= OUTPUT_LIMIT}


def signature(row):
    return (row['exit'], row['stdout_sha256'], row['stderr_sha256'])


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--revision', required=True)
    ap.add_argument('--baseline', default=BASELINE)
    ap.add_argument('--fixtures', required=True)
    args = ap.parse_args()
    receipt = {'schema': 'mado-r22-audit-independence-v1',
               'runner_sha256': digest(Path(__file__).read_bytes()),
               'scope': 'finite intervention, not universal read/execute proof',
               'limits': {'address_space': LIMIT, 'timeout_seconds': 15,
                          'output_bytes_per_stream': OUTPUT_LIMIT}, 'runs': []}
    try:
        fixtures_rel = relative(args.fixtures)
        commit = git('rev-parse', '--verify', args.revision + '^{commit}').decode().strip()
        base_commit = git('rev-parse', '--verify', args.baseline + '^{commit}').decode().strip()
        baseline = git('show', base_commit + ':' + CLASSIFIER)
        receipt.update(revision=commit, baseline=base_commit,
                       baseline_classifier_sha256=digest(baseline))
        with tempfile.TemporaryDirectory(prefix='mado-r22-independence-') as tmp:
            work = Path(tmp)
            stage = work / 'tree'
            stage.mkdir()
            archive = work / 'tree.tar'
            git('archive', '--format=tar', '--output=' + str(archive), commit)
            with tarfile.open(archive) as source:
                source.extractall(stage, filter='data')
            gate = regular(stage, relative(TOOL))
            classifier = regular(stage, relative(CLASSIFIER))
            candidate = classifier.read_bytes()
            classifier_mode = stat.S_IMODE(classifier.stat().st_mode)
            copies = []
            for path in sorted(stage.rglob('*.py')):
                if path.is_symlink() or not path.is_file():
                    continue
                raw = path.read_bytes()
                if (any(line.startswith(b'def scan_file(') for line in raw.splitlines())
                        and b'MADO_TRIPWIRE' in raw):
                    copies.append({'path': path.relative_to(stage).as_posix(),
                                   'sha256': digest(raw)})
            receipt.update(
                intervention_scope='active tools/mado-tripwire.py only; not absence of every historical classifier snapshot',
                classifier_copy_inventory=copies,
                substituted_paths=[CLASSIFIER],
                unsubstituted_candidates=[row for row in copies if row['path'] != CLASSIFIER],
                copy_inventory_selector='tracked staged .py files with column-zero def scan_file( and MADO_TRIPWIRE; heuristic candidate inventory')
            if candidate == baseline:
                raise ValueError('baseline and changed classifier bytes are equal; no effective intervention')
            fixtures = stage / fixtures_rel
            manifest_path = regular(stage, fixtures_rel / 'expected.json')
            manifest_raw = manifest_path.read_bytes()
            seal = regular(stage, fixtures_rel / 'expected.sha256').read_text('ascii')
            if seal != digest(manifest_raw) + '  expected.json\n':
                raise ValueError('manifest sidecar mismatch')
            manifest = json.loads(manifest_raw)
            if manifest['schema'] != 'mado-r22-audit-fixtures-v1':
                raise ValueError('unsupported manifest schema')
            cases = manifest['cases']
            entries = manifest['input_entries']
            if not isinstance(cases, list) or not cases or not isinstance(entries, list) or not entries:
                raise ValueError('empty or invalid manifest population')
            inventory = set()
            for entry in entries:
                rel = relative(entry['path'], inventory=True)
                name = rel.as_posix()
                if name in inventory:
                    raise ValueError('duplicate inventory path: ' + name)
                inventory.add(name)
                path = fixtures / rel
                # Reject symlink ancestors, but allow deliberate leaf symlink
                # fixtures; the audit must reject them, not the intervention.
                for parent in rel.parents:
                    if (fixtures / parent).is_symlink():
                        raise ValueError('symlink inventory ancestor')
                mode = path.lstat().st_mode
                if entry['kind'] == 'file':
                    if not stat.S_ISREG(mode):
                        raise ValueError('inventory file type mismatch')
                    data = path.read_bytes()
                    if digest(data) != entry['sha256'] or len(data) != entry['size_bytes']:
                        raise ValueError('inventory digest or size mismatch: ' + name)
                elif entry['kind'] == 'directory':
                    if not stat.S_ISDIR(mode):
                        raise ValueError('inventory directory type mismatch')
                elif entry['kind'] == 'symlink':
                    if not stat.S_ISLNK(mode) or os.readlink(path) != entry['target']:
                        raise ValueError('inventory symlink mismatch')
                else:
                    raise ValueError('unknown inventory kind')
            actual = {p.relative_to(fixtures).as_posix() for p in fixtures.rglob('*')}
            if actual != (inventory - {'.'}) | {'expected.json', 'expected.sha256'}:
                raise ValueError('fixture inventory not exact')
            fixture_pin = tree_hash(fixtures)
            gate_pin = digest(gate.read_bytes())
            commands = [[sys.executable, '-I', '-B', str(gate), '--selftest', str(fixtures)]]
            expected_codes = [0]
            ids = set()
            for case in cases:
                if not isinstance(case['id'], str) or case['id'] in ids:
                    raise ValueError('invalid or duplicate case id')
                ids.add(case['id'])
                bundle_rel = relative(case['bundle'])
                root_rel = relative(case['root'])
                bundle = regular(fixtures, bundle_rel)
                if digest(bundle.read_bytes()) != case['bundle_sha256']:
                    raise ValueError('case bundle digest mismatch')
                for part in [root_rel, *root_rel.parents]:
                    if (fixtures / part).is_symlink():
                        raise ValueError('case root symlink')
                if not (fixtures / root_rel).is_dir():
                    raise ValueError('case root unavailable')
                code = case['expected']['code']
                if type(code) is not int or code not in (0, 1, 2):
                    raise ValueError('invalid expected code')
                commands.append([sys.executable, '-I', '-B', str(gate), '--check',
                                 str(bundle), '--root', str(fixtures / root_rel)])
                expected_codes.append(code)
            receipt.update(gate_sha256=gate_pin, fixture_tree_sha256=fixture_pin,
                           expected_sha256=digest(manifest_raw),
                           candidate_classifier_sha256=digest(candidate),
                           case_ids=[case['id'] for case in cases],
                           bundle_coverage='every sealed manifest case with its exact per-case root')
            marker = work / 'classifier-executed'
            marker_source = ('#!' + sys.executable + '\nfrom pathlib import Path\nPath(' +
                             repr(str(marker)) +
                             ').write_text("executed")\nraise SystemExit(83)\n').encode()
            states = [('base', baseline), ('changed', candidate), ('absent', None),
                      ('read_fifo', 'fifo'), ('execution_marker', marker_source)]
            comparisons = {}
            intact = True
            for state, data in states:
                classifier.unlink(missing_ok=True)
                if data == 'fifo':
                    os.mkfifo(classifier)
                elif data is not None:
                    classifier.write_bytes(data)
                    classifier.chmod(classifier_mode)
                rows = []
                for command in commands:
                    before = tree_hash(fixtures)
                    row = run(command, stage, work)
                    row.update(state=state, marker_present=marker.exists(),
                               fixtures_unchanged=(before == fixture_pin == tree_hash(fixtures)),
                               gate_unchanged=(digest(gate.read_bytes()) == gate_pin))
                    intact &= row['fixtures_unchanged'] and row['gate_unchanged']
                    rows.append(row)
                    receipt['runs'].append(row)
                comparisons[state] = rows
            base_rows = comparisons['base']
            equality = all(signature(row) == signature(base_rows[index])
                           for state in comparisons for index, row in enumerate(comparisons[state]))
            healthy = all(not row['timeout'] and not row['marker_present'] and
                          not row['output_bound_hit'] and row['exit'] in (0, 1, 2)
                          for row in receipt['runs'])
            selftest_ok = all(rows[0]['exit'] == 0 for rows in comparisons.values())
            expected_exits = all(row['exit'] == expected_codes[index]
                                 for rows in comparisons.values()
                                 for index, row in enumerate(rows))
            # Positive control is a separate harness, never appended to candidate.
            control = work / 'coupled-control.py'
            control.write_text('import hashlib, pathlib, sys\n'
                               'print(hashlib.sha256(pathlib.Path(sys.argv[1]).read_bytes()).hexdigest())\n')
            controls = []
            for name, data in [('base', baseline), ('changed', candidate), ('read_fifo', 'fifo')]:
                classifier.unlink(missing_ok=True)
                if data == 'fifo':
                    os.mkfifo(classifier)
                else:
                    classifier.write_bytes(data)
                    classifier.chmod(classifier_mode)
                row = run([sys.executable, '-I', '-B', str(control), str(classifier)], stage, work)
                row['state'] = name
                controls.append(row)
            sensitive = (controls[0]['exit'] == controls[1]['exit'] == 0 and
                         signature(controls[0]) != signature(controls[1]) and controls[2]['timeout'])
            classifier.unlink()
            classifier.write_bytes(marker_source)
            classifier.chmod(classifier_mode)
            execution_control = run([sys.executable, '-I', '-B', str(classifier)], stage, work)
            execution_control['state'] = 'execution_marker_positive_control'
            execution_control['marker_present'] = marker.exists()
            controls.append(execution_control)
            sensitive &= execution_control['exit'] == 83 and marker.exists()
            receipt.update(positive_controls=controls, positive_control_sensitive=sensitive,
                           identical_outputs=equality, fixtures_and_gate_unchanged=intact,
                           selftest_ok=selftest_ok,
                           expected_exits_match=expected_exits,
                           pass_intervention=bool(equality and healthy and intact and selftest_ok
                                                  and expected_exits and sensitive),
                           limitations=[
                               'No semantic correctness or admission verdict is inferred.',
                               'Exact finding IDs and audit correctness are checked by measure.py, not inferred from equality.',
                               'FIFO/marker do not detect stat-only, nonblocking reads, or intentional evasion.',
                               'No reverse-direction or oracle-harness intervention is performed by this driver.',
                               'Fixture derivation independence must be established from frozen provenance separately.'])
            receipt['limitations'].append(
                'Historical classifier snapshots listed in unsubstituted_candidates remain present; '
                'base/changed/absent/FIFO/marker state names refer only to the active production path.')
            code = 0 if receipt['pass_intervention'] else 1
    except (OSError, ValueError, KeyError, TypeError, RecursionError,
            subprocess.SubprocessError, tarfile.TarError) as exc:
        receipt.update(error=type(exc).__name__ + ': ' + str(exc), pass_intervention=False)
        code = 2
    receipt['exit'] = code
    print(json.dumps(receipt, sort_keys=True))
    return code


if __name__ == '__main__':
    raise SystemExit(main())
