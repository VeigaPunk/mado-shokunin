#!/usr/bin/env python3
"""Round-18 R17-V5 mutant receipts for the round-17 rubric-V tightenings.

For each tightening added between the loose instrument (round-17 commit
f52f43f, sha256 a280b3ab...) and the tight instrument (baseline d9a5a18,
sha256 de4c422b...):

  * build a throwaway git repo from `git archive d9a5a18` under /tmp,
  * apply exactly ONE minimal mutant that the loose instrument credits and
    the tight instrument must not credit,
  * commit the mutant in the throwaway repo,
  * run both instruments against the mutant commit (and against the
    pre-mutant commit in the same repo, as the local baseline).

The only adaptation to either instrument is placement: its bytes are copied
unmodified into <tmp-repo>/.ufo/waves/round-18/ so that the instrument's own
`REPO = Path(__file__).resolve().parents[3]` resolves to the throwaway repo
root.  The sha256 of every instrument is rechecked at run time against the
pin recorded below; the lane is only read through git.

The receipt JSON is printed to stdout.  `--out FILE` writes it there
atomically instead; a FILE inside the git worktree being read is refused
unless `--force-lane-receipt` is given, so a lab rerun cannot silently
overwrite the lane receipt.  A tightening bites when the loose run credits
at least one province entry that the tight run does not, or when the tight
instrument refuses the measurement outright.  A tightening that does not
bite is recorded as such, not smoothed over.
"""
from __future__ import annotations

import argparse
import hashlib
import io
import json
import os
import platform
import shutil
import subprocess
import sys
import tarfile
import tempfile
from datetime import datetime, timezone
from pathlib import Path

LANE_DEFAULT = Path('/home/vgpnk/Projects/shokunin/mado-shokunin')

BASELINE_REV = 'd9a5a18e17cd3a68b52148fcc01c4a30e340ba98'
LOOSE_REV = 'f52f43f8ea44f60b3c52e5cc5b2e5ab76d77be59'
LOOSE_SHA = 'a280b3ab7c4dc21a25a954056f6a0c55187fd84dc06cfcddcb28e7f897d3508e'
TIGHT_SHA = 'de4c422b55c67f822cb9f0be21fe5e879e3d15c46830565c1c661381817cfcdc'
INSTRUMENT_REL = '.ufo/waves/round-17/measure.py'
STAGE_REL = '.ufo/waves/round-18'
EXPECTED_BASE_COUNT = 4
EXPECTED_BASE_PROVINCES = ('P1', 'P2', 'P4', 'P6')


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def git(repo: Path, *args: str) -> subprocess.CompletedProcess:
    return subprocess.run(
        ['git', '-C', str(repo), *args],
        capture_output=True, text=False, check=True)


def fetch_instrument(lane: Path, rev: str, pin: str) -> bytes:
    proc = git(lane, 'show', f'{rev}:{INSTRUMENT_REL}')
    data = proc.stdout
    got = sha256_bytes(data)
    if got != pin:
        raise SystemExit(
            f'instrument pin mismatch at {rev}:{INSTRUMENT_REL}: '
            f'expected {pin}, got {got}')
    return data


def write_text(repo: Path, rel: str, text: str) -> None:
    p = repo / rel
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(text, encoding='utf-8')


def read_text(repo: Path, rel: str) -> str:
    return (repo / rel).read_text(encoding='utf-8')


def replace_once(text: str, old: str, new: str, where: str) -> str:
    if text.count(old) != 1:
        raise SystemExit(f'{where}: expected exactly one {old!r}, '
                         f'found {text.count(old)}')
    return text.replace(old, new)


# --- fixture note -----------------------------------------------------------

def fixture_note(sid: str, thin: bool = False) -> str:
    host = (
        '## Host declaration\n\n'
        '- The only declared input is the fixture row in SOURCES.md.\n'
        '- No host file is read by this mutated repository.\n'
        '- No launch, theme or compositor fact is asserted.\n'
        if not thin else
        '## Host declaration\n\n'
        '- The only declared input is the fixture row in SOURCES.md.\n'
        '- No host file is read by this mutated repository.\n'
    )
    return (
        f'source: {sid} — https://github.com/abenz1267/walker — mutant fixture row, no fetch performed\n'
        'surface: P3\n'
        'scope: mutant fixture for the rubric-V instrument receipts; no host fact\n'
        '\n'
        '# Mutant fixture note\n'
        '\n'
        'This note exists only in a throwaway /tmp git repo to prove one\n'
        'instrument tightening bites. It is never part of the lane, and every\n'
        'host behaviour stays [UNK].\n'
        '\n'
        '## Upstream contract\n'
        '\n'
        '- The cited row is a walker upstream scaffold used only by this fixture.\n'
        '- It states a documentary contract shape, nothing about this host.\n'
        '- No fetch or execution is performed for the fixture.\n'
        '\n'
        f'{host}'
        '\n'
        '## Safe observation\n'
        '\n'
        '- Reading this note\'s bytes is the whole observation.\n'
        '- No walker or elephant process is started.\n'
        '- The route stays documentary by construction.\n'
        '\n'
        '## Unexercised behavior\n'
        '\n'
        '- [UNK] Whether Walker is installed or which version runs on this host.\n'
        '- [UNK] Any preview, launch or theme behaviour on this host.\n'
        '- [UNK] Whether the scaffold URL resolves or its lines exist.\n'
    )


def walker_row(sid: str, used_by: str) -> str:
    return (
        f'| {sid} | Walker fixture scaffold — https://github.com/abenz1267/walker '
        '— mutant only | docs | A | walker upstream scaffold for the mutant '
        'receipt | fixture anchor; no fetch performed | fixture row only; not a '
        f'source claim | mined | 2026-10-20 | on-change | {used_by} |\n'
    )


def split_row(line: str) -> list[str]:
    cells = line.split('|')
    if len(cells) != 13:
        raise SystemExit(f'row does not have 13 split cells: {line!r}')
    return cells


def insert_after(lines: list[str], prefix: str, row: str) -> list[str]:
    hits = [i for i, l in enumerate(lines) if l.startswith(prefix)]
    if len(hits) != 1:
        raise SystemExit(f'expected one line starting {prefix!r}, got {len(hits)}')
    out = list(lines)
    out.insert(hits[0] + 1, row)
    return out


def insert_after_heading(lines: list[str], heading: str, row: str) -> list[str]:
    hits = [i for i, l in enumerate(lines) if l.strip() == heading]
    if len(hits) != 1:
        raise SystemExit(f'expected one {heading!r} heading, got {len(hits)}')
    out = list(lines)
    out.insert(hits[0] + 1, row)
    return out


# --- mutants ----------------------------------------------------------------

NOTE_M3 = 'corpus/knowledge/p3-upstream-keyword-mutant.md'
NOTE_M4 = 'corpus/knowledge/p3-section-floor-mutant.md'
NOTE_M5 = 'corpus/knowledge/p3-registry-only-mutant.md'
NOTE_M6 = 'corpus/knowledge/p3-duplicate-id-mutant.md'


def mutant_surface(repo: Path) -> None:
    rel = 'corpus/knowledge/terminal-route-r17.md'
    text = read_text(repo, rel)
    text = replace_once(text, 'surface: P4\n', 'surface: P4 terminal\n', rel)
    write_text(repo, rel, text)


def mutant_legacy_pin(repo: Path) -> None:
    rel = 'corpus/knowledge/input-debugging-boundaries-r15.md'
    text = read_text(repo, rel)
    text = replace_once(text, 'covers: U6\n', 'covers: U6, U1\n', rel)
    write_text(repo, rel, text)


def mutant_upstream_keyword(repo: Path) -> None:
    rel = 'corpus/SOURCES.md'
    lines = read_text(repo, rel).splitlines(keepends=True)
    hits = [i for i, l in enumerate(lines) if l.startswith('| S016 |')]
    if len(hits) != 1:
        raise SystemExit(f'S016 row count {len(hits)}')
    cells = split_row(lines[hits[0]])
    cells[11] = cells[11].rstrip(' ') + ', ' + NOTE_M3 + ' '
    lines[hits[0]] = '|'.join(cells)
    write_text(repo, rel, ''.join(lines))
    write_text(repo, NOTE_M3, fixture_note('S016'))


def mutant_section_floor(repo: Path) -> None:
    rel = 'corpus/SOURCES.md'
    lines = read_text(repo, rel).splitlines(keepends=True)
    lines = insert_after(lines, '| S071 |', walker_row('S900', NOTE_M4))
    write_text(repo, rel, ''.join(lines))
    write_text(repo, NOTE_M4, fixture_note('S900', thin=True))


def mutant_registry_only(repo: Path) -> None:
    rel = 'corpus/SOURCES.md'
    lines = read_text(repo, rel).splitlines(keepends=True)
    lines = insert_after_heading(lines, '## Paths',
                                 walker_row('S901', NOTE_M5))
    write_text(repo, rel, ''.join(lines))
    write_text(repo, NOTE_M5, fixture_note('S901'))


def mutant_duplicate_id(repo: Path) -> None:
    rel = 'corpus/SOURCES.md'
    lines = read_text(repo, rel).splitlines(keepends=True)
    lines = insert_after(lines, '| S016 |', walker_row('S016', NOTE_M6))
    write_text(repo, rel, ''.join(lines))
    write_text(repo, NOTE_M6, fixture_note('S016'))


MUTANTS = [
    {
        'id': 'M1',
        'tightening': 'exact surface line',
        'description': 'terminal-route-r17.md surface line becomes '
                       '`surface: P4 terminal`; the loose P[1-6]\\b scan '
                       'still reads P4, the tight fullmatch rejects it',
        'expect': 'loose credits P4 from `surface: P4 terminal`; tight rejects '
                  'the note as MALFORMED and P4 drops',
        'files': ['corpus/knowledge/terminal-route-r17.md'],
        'reason_contains': 'surface line must be exactly',
        'apply': mutant_surface,
    },
    {
        'id': 'M2',
        'tightening': 'legacy credit pinned to three paths',
        'description': 'input-debugging-boundaries-r15.md gains an unpinned '
                       '`covers: U1`; loose credits P1 from it, tight only '
                       'credits the three pinned paths',
        'expect': 'loose credits P1 from an unpinned `covers: U1` entry; tight '
                  'does not credit that entry (count may stay 4 because P1 is '
                  'already covered by the pinned paths)',
        'files': ['corpus/knowledge/input-debugging-boundaries-r15.md'],
        'reason_contains': None,
        'apply': mutant_legacy_pin,
    },
    {
        'id': 'M3',
        'tightening': 'upstream https docs/spec/code row naming the surface',
        'description': 'a valid P3 note cites the Hyprland docs row S016; '
                       'loose accepts any docs/spec/code https row, tight '
                       'requires walker/elephant in source or scope',
        'expect': 'loose credits P3 from a Hyprland docs row; tight rejects '
                  'because walker/elephant do not appear in the row source or '
                  'scope',
        'files': ['corpus/SOURCES.md', NOTE_M3],
        'reason_contains': 'naming the surface',
        'apply': mutant_upstream_keyword,
    },
    {
        'id': 'M4',
        'tightening': 'three-line section floor',
        'description': 'a valid P3 note has a two-line `## Host '
                       'declaration`; loose credits it, tight rejects it '
                       'under the content floor',
        'expect': 'loose credits P3 with a two-line `## Host declaration`; '
                  'tight rejects under the content floor',
        'files': ['corpus/SOURCES.md', NOTE_M4],
        'reason_contains': 'under content floor',
        'apply': mutant_section_floor,
    },
    {
        'id': 'M5',
        'tightening': 'registry-only parse',
        'description': 'a valid walker row is placed under `## Paths`, '
                       'outside `## Registry`; loose parses it and credits '
                       'P3, tight never sees it',
        'expect': 'loose parses a valid walker row under `## Paths` and '
                  'credits P3; tight never sees the row and rejects the note '
                  'as unsourced',
        'files': ['corpus/SOURCES.md', NOTE_M5],
        'reason_contains': 'token resolves to a mined tier-A',
        'apply': mutant_registry_only,
    },
    {
        'id': 'M6',
        'tightening': 'duplicate ids fail',
        'description': 'a second `S016` row grants the P3 fixture note; '
                       'loose keeps the last copy, tight exits 2 on the '
                       'duplicate id',
        'expect': 'loose keeps the last S016 copy and credits P3; tight exits 2 '
                  'on the duplicate id with no c2 result',
        'files': ['corpus/SOURCES.md', NOTE_M6],
        'reason_contains': None,
        'error_contains': 'duplicate SOURCES id S016',
        'apply': mutant_duplicate_id,
    },
]


# --- instrumentation --------------------------------------------------------

def summarize(stdout: str) -> dict | None:
    try:
        data = json.loads(stdout)
    except json.JSONDecodeError:
        return None
    c2 = data.get('c2') or {}
    provinces = c2.get('provinces') or {}
    covered = {}
    for prov in sorted(provinces):
        entry = provinces[prov] or {}
        if entry.get('covered'):
            covered[prov] = sorted(e['path'] for e in entry.get('entries') or [])
    rejected = [
        {'path': r.get('path'), 'reason': r.get('reason')}
        for r in c2.get('rejected') or []
    ]
    return {
        'count': c2.get('count'),
        'score': c2.get('score'),
        'covered': covered,
        'rejected': rejected,
        'u_routes': c2.get('u_routes'),
        'c1': (data.get('c1') or {}).get('score'),
        'c3_present': bool((data.get('c3') or {}).get('present')),
    }


def run_instrument(exe: Path, rev: str, repo: Path, pin: str) -> dict:
    at_run = sha256_bytes(exe.read_bytes())
    if at_run != pin:
        raise SystemExit(f'instrument bytes drifted before run: {exe} {at_run}')
    cmd = [sys.executable, '-I', str(exe), rev]
    proc = subprocess.run(cmd, cwd=str(repo), capture_output=True, text=True)
    parsed = summarize(proc.stdout)
    return {
        'cmd': [str(exe), rev],
        'instrument_sha256': at_run,
        'exit': proc.returncode,
        'stdout_sha256': sha256_bytes(proc.stdout.encode()),
        'stderr': proc.stderr.strip(),
        'c2': parsed,
        'stdout': proc.stdout if parsed is None else None,
    }


def covered_view(c2: dict | None) -> dict:
    return (c2 or {}).get('covered') or {}


def compare(loose: dict, tight: dict) -> dict:
    loose_cov = covered_view(loose.get('c2'))
    tight_cov = covered_view(tight.get('c2'))
    loose_only, tight_only = {}, {}
    for prov in sorted(set(loose_cov) | set(tight_cov)):
        lo = set(loose_cov.get(prov, []))
        ti = set(tight_cov.get(prov, []))
        if lo - ti:
            loose_only[prov] = sorted(lo - ti)
        if ti - lo:
            tight_only[prov] = sorted(ti - lo)
    tight_refused = tight.get('exit') != 0
    loose_count = (loose.get('c2') or {}).get('count')
    tight_count = (tight.get('c2') or {}).get('count')
    bites = bool(loose_only) or tight_refused
    basis = []
    for prov, paths in loose_only.items():
        basis.append(f'{prov}: loose-only {paths}')
    if tight_refused:
        basis.append(f'tight refused (exit {tight.get("exit")}): '
                     f'{tight.get("stderr") or "no stderr"}')
    if isinstance(loose_count, int) and isinstance(tight_count, int) \
            and loose_count != tight_count:
        basis.append(f'count {loose_count} vs {tight_count}')
    if tight_only:
        basis.append(f'UNEXPECTED tight-only {tight_only}')
    return {
        'loose_only': loose_only,
        'tight_only': tight_only,
        'loose_count': loose_count,
        'tight_count': tight_count,
        'tight_refused': tight_refused,
        'bites': bites,
        'basis': basis,
    }


def baseline_assert(loose: dict, tight: dict, label: str) -> None:
    lc = loose.get('c2') or {}
    tc = tight.get('c2') or {}
    if loose['exit'] != 0 or tight['exit'] != 0:
        raise SystemExit(f'{label}: baseline instrument exit '
                         f'{loose["exit"]}/{tight["exit"]}')
    if lc.get('count') != EXPECTED_BASE_COUNT or tc.get('count') != EXPECTED_BASE_COUNT:
        raise SystemExit(f'{label}: baseline count {lc.get("count")}/'
                         f'{tc.get("count")} != {EXPECTED_BASE_COUNT}')
    if tuple(sorted(lc.get('covered') or {})) != EXPECTED_BASE_PROVINCES \
            or tuple(sorted(tc.get('covered') or {})) != EXPECTED_BASE_PROVINCES:
        raise SystemExit(f'{label}: baseline provinces '
                         f'{sorted(lc.get("covered") or {})}/'
                         f'{sorted(tc.get("covered") or {})} != '
                         f'{EXPECTED_BASE_PROVINCES}')
    if (lc.get('covered') or {}) != (tc.get('covered') or {}):
        raise SystemExit(f'{label}: baseline covered sets differ')


def archive_member(member: tarfile.TarInfo, dest: Path):
    """Skip only links whose targets escape the extraction root.

    The baseline tree contains fixture symlinks with absolute targets used
    by unrelated round-17 tests; the rubric instruments never read them, so
    they are dropped rather than followed.
    """
    if member.issym() or member.islnk():
        target = member.linkname
        if target.startswith('/') or '..' in Path(target).parts:
            return None
    return member


def prepare_repo(lane: Path, root: Path) -> tuple[Path, str]:
    repo = root / 'repo'
    repo.mkdir(parents=True)
    archive = subprocess.run(
        ['git', '-C', str(lane), 'archive', BASELINE_REV],
        capture_output=True, check=True).stdout
    with tarfile.open(fileobj=io.BytesIO(archive), mode='r:') as tar:
        tar.extractall(repo, filter=archive_member)
    subprocess.run(['git', 'init', '-q', '-b', 'main', str(repo)], check=True)
    subprocess.run(['git', '-C', str(repo), 'config', 'user.name',
                    'mado measure mutants'], check=True)
    subprocess.run(['git', '-C', str(repo), 'config', 'user.email',
                    'measure-mutants@localhost'], check=True)
    subprocess.run(['git', '-C', str(repo), 'add', '-f', '-A', '.'], check=True)
    subprocess.run(['git', '-C', str(repo), 'commit', '-q', '-m',
                    'baseline d9a5a18 (mutant harness)'], check=True)
    base = git(repo, 'rev-parse', 'HEAD').stdout.decode().strip()
    return repo, base


def stage_instruments(repo: Path, loose: bytes, tight: bytes) -> tuple[Path, Path]:
    stage = repo / STAGE_REL
    stage.mkdir(parents=True, exist_ok=True)
    loose_path = stage / 'measure-loose.py'
    tight_path = stage / 'measure-tight.py'
    loose_path.write_bytes(loose)
    tight_path.write_bytes(tight)
    return loose_path, tight_path


def commit_mutant(repo: Path, spec: dict) -> tuple[str, list[str], str, str]:
    spec['apply'](repo)
    subprocess.run(['git', '-C', str(repo), 'add', '-f', '--', *spec['files']],
                   check=True)
    subprocess.run(['git', '-C', str(repo), 'commit', '-q', '-m',
                    f"{spec['id']}: {spec['tightening']} mutant"], check=True)
    sha = git(repo, 'rev-parse', 'HEAD').stdout.decode().strip()
    changed = git(repo, 'diff', '--name-only', 'HEAD^', 'HEAD').stdout \
        .decode().splitlines()
    if sorted(changed) != sorted(spec['files']):
        raise SystemExit(f"{spec['id']}: changed {sorted(changed)} != "
                         f"declared {sorted(spec['files'])}")
    diff = git(repo, 'diff', '--no-color', 'HEAD^', 'HEAD').stdout
    return sha, changed, sha256_bytes(diff), diff.decode('utf-8', 'replace')


def expectation_met(spec: dict, tight: dict) -> bool:
    if spec.get('error_contains'):
        return (tight['exit'] == 2
                and spec['error_contains'] in (tight['stderr'] or ''))
    key = spec.get('reason_contains')
    if key is None:
        return True
    reasons = [r.get('reason') or ''
               for r in (tight.get('c2') or {}).get('rejected') or []]
    return any(key in reason for reason in reasons)


def lane_worktree(lane: Path) -> Path:
    proc = subprocess.run(
        ['git', '-C', str(lane), 'rev-parse', '--show-toplevel'],
        capture_output=True, text=True)
    if proc.returncode != 0 or not proc.stdout.strip():
        return lane
    return Path(proc.stdout.strip()).resolve()


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--lane', type=Path, default=LANE_DEFAULT)
    ap.add_argument('--out', type=Path, default=None,
                    help='write the receipt here; without it the JSON is '
                         'printed to stdout')
    ap.add_argument('--force-lane-receipt', action='store_true',
                    help='allow --out inside the git worktree being read')
    ap.add_argument('--keep', action='store_true',
                    help='keep the throwaway repos under the work dir')
    ap.add_argument('--workdir', type=Path, default=None)
    args = ap.parse_args()

    lane = args.lane.resolve()
    if not (lane / '.git').exists() and not (lane / '.jj').exists():
        raise SystemExit(f'{lane} is not a git/jj checkout')
    out = args.out.resolve() if args.out else None
    worktree = lane_worktree(lane)
    if out is not None and not args.force_lane_receipt \
            and (out == worktree or worktree in out.parents):
        raise SystemExit(
            f'refusing --out {out}: inside the git worktree being read '
            f'({worktree}); pass --force-lane-receipt to write a lane '
            'receipt')

    head = subprocess.run(
        ['git', '-C', str(lane), 'rev-parse', '--verify', BASELINE_REV],
        capture_output=True, check=True).stdout.decode().strip()
    if head != BASELINE_REV:
        raise SystemExit(f'baseline rev resolved to {head}')

    loose_bytes = fetch_instrument(lane, LOOSE_REV, LOOSE_SHA)
    tight_bytes = fetch_instrument(lane, BASELINE_REV, TIGHT_SHA)

    # Round 19 (w2 SentinelToolSafety F1): never delete a caller-named directory;
    # --workdir only chooses where the tool's own fresh mkdtemp directory lives.
    if args.workdir:
        args.workdir.mkdir(parents=True, exist_ok=True)
    root = Path(tempfile.mkdtemp(prefix='mado-r18-mutants-', dir=args.workdir))
    started = datetime.now(timezone.utc).isoformat(timespec='seconds')

    records = []
    for spec in MUTANTS:
        mroot = root / spec['id']
        if mroot.exists():
            shutil.rmtree(mroot)
        mroot.mkdir(parents=True)
        repo, base = prepare_repo(lane, mroot)
        loose_path, tight_path = stage_instruments(repo, loose_bytes, tight_bytes)

        base_loose = run_instrument(loose_path, base, repo, LOOSE_SHA)
        base_tight = run_instrument(tight_path, base, repo, TIGHT_SHA)
        baseline_assert(base_loose, base_tight, f"{spec['id']} baseline")

        mutant_sha, changed, diff_sha, diff_text = commit_mutant(repo, spec)
        mut_loose = run_instrument(loose_path, mutant_sha, repo, LOOSE_SHA)
        mut_tight = run_instrument(tight_path, mutant_sha, repo, TIGHT_SHA)
        cmp = compare(mut_loose, mut_tight)
        met = expectation_met(spec, mut_tight)
        cmp['expectation_met'] = met

        record = {
            'id': spec['id'],
            'tightening': spec['tightening'],
            'description': spec['description'],
            'expect': spec['expect'],
            'files': spec['files'],
            'changed_files': changed,
            'repo': str(repo) if args.keep else None,
            'baseline_commit': base,
            'mutant_commit': mutant_sha,
            'diff_sha256': diff_sha,
            'diff': diff_text,
            'baseline': {
                'loose': {'exit': base_loose['exit'],
                          'c2': base_loose['c2']},
                'tight': {'exit': base_tight['exit'],
                          'c2': base_tight['c2']},
            },
            'mutant': {
                'loose': mut_loose,
                'tight': mut_tight,
            },
            'compare': cmp,
            'bites': cmp['bites'],
        }
        records.append(record)
        status = 'BITES' if cmp['bites'] else 'NO-BITE'
        print(f"{spec['id']} {status}: loose={cmp['loose_count']} "
              f"tight={cmp['tight_count']} "
              f"loose_only={list(cmp['loose_only'])}", file=sys.stderr)
        for line in cmp['basis']:
            print(f"  {line}", file=sys.stderr)

    summary = {
        'mutants': len(records),
        'bites': sum(1 for r in records if r['bites']),
        'no_bite': [r['id'] for r in records if not r['bites']],
        'expectations_met': sum(
            1 for r in records if r['compare']['expectation_met']),
        'expected_but_unmet': [
            r['id'] for r in records
            if not r['compare']['expectation_met']],
        'unexpected_tight_only': [
            r['id'] for r in records if r['compare']['tight_only']],
        'baselines_agree': True,
    }
    payload = {
        'schema': 'mado-measure-mutants-v1',
        'claim': 'R17-V5 — committed mutant receipts for the round-17 '
                 'rubric-V tightenings',
        'generated_at': datetime.now(timezone.utc).isoformat(
            timespec='seconds'),
        'started_at': started,
        'lane': str(lane),
        'baseline_rev': BASELINE_REV,
        'instruments': {
            'loose': {
                'rev': LOOSE_REV,
                'git_path': INSTRUMENT_REL,
                'sha256': LOOSE_SHA,
                'staged_as': f'{STAGE_REL}/measure-loose.py',
            },
            'tight': {
                'rev': BASELINE_REV,
                'git_path': INSTRUMENT_REL,
                'sha256': TIGHT_SHA,
                'staged_as': f'{STAGE_REL}/measure-tight.py',
            },
        },
        'adaptation': (
            'Instruments: only file placement changed. Each instrument was '
            'copied byte-identically from the named revision into '
            '<tmp-repo>/.ufo/waves/round-18/ so that its own '
            'REPO = Path(__file__).resolve().parents[3] resolves to the '
            'throwaway repo; its sha256 was asserted at every run '
            '(see record.mutant.*.instrument_sha256). No source byte, '
            'argument or environment variable was altered. Archive: the '
            'extraction skips symlink members whose targets are absolute or '
            'escape the extraction root (the baseline tree carries such '
            'fixtures under .ufo/waves/round-17/tripwire); neither instrument '
            'reads those paths, and every path either instrument reads is '
            'extracted verbatim.'
        ),
        'mutant_method': (
            'Per mutant: fresh `git archive d9a5a18` extraction, fresh git '
            'init, baseline commit, both instruments run at the baseline '
            'commit, one mutant applied and committed, both instruments run '
            'at the mutant commit. Bite = loose credits a province entry the '
            'tight run does not, or the tight run refuses (exit != 0).'
        ),
        'environment': {
            'python': platform.python_version(),
            'git': subprocess.run(['git', '--version'], capture_output=True,
                                  text=True).stdout.strip(),
            'platform': platform.platform(),
            'workdir': str(root),
            'kept': bool(args.keep),
        },
        'harness': {
            'path': str(Path(__file__).resolve()),
            'sha256': sha256_bytes(Path(__file__).resolve().read_bytes()),
            'argv': sys.argv,
            'note': 'Rerun with --keep to retain the throwaway repos; '
                    'mutant commit hashes identify this run only.',
        },
        'summary': summary,
        'mutants': records,
    }

    text = json.dumps(payload, indent=2, sort_keys=False) + '\n'
    if out is None:
        sys.stdout.write(text)
    else:
        out.parent.mkdir(parents=True, exist_ok=True)
        tmp = out.with_suffix(out.suffix + '.tmp')
        tmp.write_text(text, encoding='utf-8')
        os.replace(tmp, out)
        print(f'wrote {out}', file=sys.stderr)
        print(json.dumps(summary, indent=2))

    if not args.keep:
        shutil.rmtree(root, ignore_errors=True)
    return 0 if summary['bites'] == summary['mutants'] \
        and summary['expectations_met'] == summary['mutants'] \
        and not summary['unexpected_tight_only'] else 1


if __name__ == '__main__':
    raise SystemExit(main())
