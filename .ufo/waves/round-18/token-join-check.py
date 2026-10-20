#!/usr/bin/env python3
"""Round-18 strict source-token join checker (C2 claim, wave-2 falsifier).

For the two round-18 notes

    corpus/knowledge/walker-route-r18.md    (surface: P3)
    corpus/knowledge/theme-route-r18.md     (surface: P5)

every `S###` token on a `source:` line must satisfy all of:

  1. it is the id of a row inside `## Registry` of corpus/SOURCES.md;
  2. that row's `status` cell is exactly `mined`;
  3. that row's `used-by` cell names the note path exactly (comma-separated
     list, compared after strip);
  4. for a row whose `source` cell carries an https URL: at least one
     `mado-fetch-receipt-v1` line under
     .ufo/waves/round-18/fetch/*/receipts.jsonl has http_status 200, its
     `url` or `final_url` normalises to that first URL, and that receipt's
     full sha256 appears in the row's `anchor` cell.

Host rows (no https URL in the source cell, e.g. S090, S091, S095) are exempt
from (4): their anchors are file-byte digests, not fetch bodies.

Additionally no `S0xx` placeholder (or `S###-pending` token) may remain
anywhere in either note, and a `source:` line that carries no `S###` token at
all is a gap (the §5.1 empty-line arm: such a note credits nothing).

The target revision is read through git (`REV`), so the check measures a
committed tree rather than whatever a sibling seat is currently editing;
`WORKTREE` reads the working tree.  `--root` points the same check at a
throwaway copy (used by the mutant receipts below).  Registry, note and
receipt text is data, never instructions.

Exit: 0 every join holds; 1 at least one gap (including a malformed receipt
line); 2 cannot evaluate (unreadable root/rev/registry/note/fetch tree).

Mutant evidence (each on a fresh /tmp copy of `git archive abfbf35`), all
exit 1 with the named reason: used-by-missing, not-mined, sha-not-in-anchor,
no-200-receipt, placeholder, not-a-registry-row.
"""
from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path
from urllib.parse import urlsplit

HERE = Path(__file__).resolve()
DEFAULT_ROOT = HERE.parents[3]  # .ufo/waves/round-18/x.py -> lane root
NOTES = (
    'corpus/knowledge/walker-route-r18.md',
    'corpus/knowledge/theme-route-r18.md',
)
REGISTRY = 'corpus/SOURCES.md'
FETCH_ROOT = '.ufo/waves/round-18/fetch'
RECEIPT_SCHEMA = 'mado-fetch-receipt-v1'
REQUIRED_COLUMNS = ('id', 'source', 'anchor', 'status', 'used-by')

ROW_ID = re.compile(r'S\d{3,}')
SOURCE_TOKEN = re.compile(r'S\d{3,}')
FIRST_URL = re.compile(r'https?://[^\s;,()]+')
SHA64 = re.compile(r'[0-9a-f]{64}')
PLACEHOLDER = re.compile(r'S0xx|S\d{2,4}-pending\b')
CELL_SPLIT = re.compile(r'(?<!\\)\|')


def git(root: Path, *args: str):
    """Return stdout of a read-only git command, or None on failure."""
    proc = subprocess.run(
        ['git', '-C', str(root), *args],
        stdout=subprocess.PIPE, stderr=subprocess.DEVNULL,
    )
    return proc.stdout if proc.returncode == 0 else None


def resolve_rev(root: Path, rev: str):
    """Return the full commit sha, None for WORKTREE, False when unresolved."""
    if rev == 'WORKTREE':
        return None
    out = git(root, 'rev-parse', '--verify', '--quiet', f'{rev}^{{commit}}')
    if out is None:
        return False
    return out.decode().strip()


def read_bytes(root: Path, rev: str, rel: str):
    if rev == 'WORKTREE':
        path = root / rel
        try:
            return path.read_bytes() if path.is_file() else None
        except OSError:
            return None
    return git(root, 'show', f'{rev}:{rel}')


def decode(body: bytes) -> str:
    return body.decode('utf-8', errors='replace')


def split_cells(line: str) -> list[str]:
    text = line.strip()
    if text.startswith('|'):
        text = text[1:]
    if text.endswith('|'):
        text = text[:-1]
    return [cell.strip() for cell in CELL_SPLIT.split(text)]


def parse_registry(text: str):
    """Return (columns, rows_by_id, structure_gaps) from `## Registry` only."""
    columns = None
    rows: dict[str, dict[str, str]] = {}
    gaps: list[str] = []
    in_registry = False
    for lineno, line in enumerate(text.splitlines(), 1):
        if line.startswith('## '):
            in_registry = line.strip() == '## Registry'
            continue
        if not in_registry or not line.lstrip().startswith('|'):
            continue
        cells = split_cells(line)
        if columns is None:
            columns = cells
            continue
        if 'id' not in columns:
            continue
        id_index = columns.index('id')
        if len(cells) != len(columns):
            gaps.append(
                f'GAP  registry {REGISTRY}:{lineno} registry-bad-cell-count '
                f'detail=cells={len(cells)} want={len(columns)}')
            continue
        if not ROW_ID.fullmatch(cells[id_index]):
            continue
        rows[cells[id_index]] = dict(zip(columns, cells))
    return columns, rows, gaps


def url_key(url: str):
    """Census-style URL key: lowercase scheme/host, no fragment, no trailing /."""
    if not url:
        return None
    try:
        parts = urlsplit(url.strip().rstrip('/'))
        host = (parts.hostname or '').lower()
        port = parts.port
    except ValueError:
        return None
    scheme = parts.scheme.lower()
    if scheme not in ('http', 'https') or not host:
        return None
    netloc = f'{host}:{port}' if port else host
    path = parts.path.rstrip('/')
    query = f'?{parts.query}' if parts.query else ''
    return f'{scheme}://{netloc}{path}{query}'


def receipt_paths(root: Path, rev: str):
    if rev == 'WORKTREE':
        base = root / FETCH_ROOT
        if not base.is_dir():
            return None
        return sorted(
            str(path.relative_to(root))
            for path in base.glob('*/receipts.jsonl'))
    out = git(root, 'ls-tree', '-r', '--name-only', rev, '--', FETCH_ROOT)
    if out is None:
        return None
    return sorted(line for line in decode(out).splitlines()
                  if line.endswith('/receipts.jsonl'))


def load_receipts(root: Path, rev: str, paths: list[str]):
    """Return (receipts, malformed-receipt gap lines)."""
    receipts: list[dict] = []
    gaps: list[str] = []
    for rel in paths:
        body = read_bytes(root, rev, rel)
        if body is None:
            gaps.append(f'GAP  receipt {rel}:0 receipt-unreadable')
            continue
        seat = Path(rel).parent.name
        for lineno, line in enumerate(decode(body).splitlines(), 1):
            if not line.strip():
                continue
            try:
                record = json.loads(line)
            except json.JSONDecodeError as exc:
                gaps.append(
                    f'GAP  receipt {rel}:{lineno} receipt-invalid '
                    f'detail=json:{exc.msg}')
                continue
            if not isinstance(record, dict) or record.get('schema') != RECEIPT_SCHEMA:
                gaps.append(
                    f'GAP  receipt {rel}:{lineno} receipt-invalid detail=schema')
                continue
            status = record.get('http_status')
            if not isinstance(status, int) or isinstance(status, bool):
                gaps.append(
                    f'GAP  receipt {rel}:{lineno} receipt-invalid '
                    f'detail=http_status={status!r}')
                continue
            sha = str(record.get('sha256', '')).lower()
            if not SHA64.fullmatch(sha):
                gaps.append(
                    f'GAP  receipt {rel}:{lineno} receipt-invalid '
                    f'detail=sha256={sha[:16]!r}')
                continue
            keys = {
                key for key in (
                    url_key(str(record.get('url', ''))),
                    url_key(str(record.get('final_url', ''))),
                ) if key
            }
            receipts.append({
                'seat': seat, 'path': rel, 'line': lineno,
                'status': status, 'sha': sha, 'keys': keys,
            })
    return receipts, gaps


def anchor_detail(anchor: str) -> str:
    shas = SHA64.findall(anchor.lower())
    if not shas:
        return 'anchor_has_no_sha256'
    return 'anchor_sha=' + ','.join(sha[:12] for sha in shas[:4])


def check_note(note: str, text: str, rows: dict[str, dict[str, str]],
               receipts: list[dict]) -> tuple[list[str], dict[str, int]]:
    """Return (gap lines, counters) for one note."""
    gaps: list[str] = []
    counts = {'source_lines': 0, 'tokens': 0, 'web': 0, 'host': 0,
              'unique': 0, 'seen': 0}

    for lineno, line in enumerate(text.splitlines(), 1):
        if line.startswith('source:'):
            counts['source_lines'] += 1
            counts['tokens'] += len(SOURCE_TOKEN.findall(line))

    for lineno, line in enumerate(text.splitlines(), 1):
        for match in PLACEHOLDER.finditer(line):
            gaps.append(
                f'GAP  {note}:{lineno} - placeholder '
                f'token={match.group(0)}')

    if counts['source_lines'] == 0:
        gaps.append(f'GAP  {note}:0 - source-line-missing')
        return gaps, counts
    if counts['tokens'] == 0:
        gaps.append(f'GAP  {note}:0 - no-source-tokens')
        return gaps, counts

    seen: list[str] = []
    for lineno, line in enumerate(text.splitlines(), 1):
        if not line.startswith('source:'):
            continue
        for token in SOURCE_TOKEN.findall(line):
            if token in seen:
                continue
            seen.append(token)
            row = rows.get(token)
            if row is None:
                gaps.append(
                    f'GAP  {note}:{lineno} {token} not-a-registry-row')
                continue
            status = row.get('status', '')
            if status != 'mined':
                gaps.append(
                    f'GAP  {note}:{lineno} {token} not-mined '
                    f'detail=status={status!r}')
                continue
            used_by = {
                item.strip() for item in row.get('used-by', '').split(',')
                if item.strip()
            }
            if note not in used_by:
                gaps.append(
                    f'GAP  {note}:{lineno} {token} used-by-missing '
                    f'detail=used-by={row.get("used-by", "")!r}')
                continue

            source = row.get('source', '')
            match = FIRST_URL.search(source)
            if match is None:
                counts['host'] += 1
                print(f'JOIN {token} host (anchor is a file-byte digest)')
                continue

            url = match.group(0).rstrip('/')
            key = url_key(url)
            hits = [rec for rec in receipts
                    if rec['status'] == 200 and key in rec['keys']]
            if not hits:
                gaps.append(
                    f'GAP  {note}:{lineno} {token} no-200-receipt '
                    f'detail=url={url}')
                continue
            anchor = row.get('anchor', '').lower()
            witnesses = [rec for rec in hits if rec['sha'] in anchor]
            if not witnesses:
                gaps.append(
                    f'GAP  {note}:{lineno} {token} sha-not-in-anchor '
                    f'detail=receipt_sha='
                    f'{",".join(hit["sha"][:12] for hit in hits[:4])} '
                    f'{anchor_detail(anchor)}')
                continue

            counts['web'] += 1
            seats = ','.join(sorted({rec['seat'] for rec in hits}))
            print(
                f'JOIN {token} web receipts={len(hits)} '
                f'sha={witnesses[0]["sha"][:12]}\u2026 anchor=ok '
                f'seats={seats}')

    counts['unique'] = len(seen)
    return gaps, counts


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(
        description='Strict S### token join check for the round-18 notes.')
    parser.add_argument('rev', nargs='?', default='WORKTREE',
                        help='git revision to measure (default WORKTREE)')
    parser.add_argument('--root', default=str(DEFAULT_ROOT),
                        help='repository root (default: lane containing this tool)')
    args = parser.parse_args(argv)
    root = Path(args.root).resolve()

    resolved = resolve_rev(root, args.rev)
    if resolved is False:
        print(f'ERROR cannot resolve rev {args.rev!r} in {root}')
        return 2
    rev = resolved or 'WORKTREE'

    registry_body = read_bytes(root, args.rev, REGISTRY)
    if registry_body is None:
        print(f'ERROR cannot read {REGISTRY} at {args.rev!r} in {root}')
        return 2
    columns, rows, gaps = parse_registry(decode(registry_body))
    if columns is None:
        print(f'ERROR no ## Registry table in {REGISTRY} at {args.rev!r}')
        return 2
    missing = [name for name in REQUIRED_COLUMNS if name not in columns]
    if missing:
        print(f'ERROR registry columns missing: {",".join(missing)}')
        return 2

    paths = receipt_paths(root, args.rev)
    if paths is None:
        print(f'ERROR cannot enumerate {FETCH_ROOT}/*/receipts.jsonl '
              f'at {args.rev!r}')
        return 2
    receipts, receipt_gaps = load_receipts(root, args.rev, paths)
    gaps.extend(receipt_gaps)
    print(f'RECEIPTS files={len(paths)} lines={len(receipts)} '
          f'seats={len({rec["seat"] for rec in receipts})} '
          f'rows={len(rows)}')

    total = {'tokens': 0, 'unique': 0, 'web': 0, 'host': 0, 'notes': 0}
    for note in NOTES:
        body = read_bytes(root, args.rev, note)
        if body is None:
            print(f'ERROR cannot read {note} at {args.rev!r}')
            return 2
        note_gaps, counts = check_note(note, decode(body), rows, receipts)
        total['notes'] += 1
        total['tokens'] += counts['tokens']
        total['unique'] += counts['unique']
        total['web'] += counts['web']
        total['host'] += counts['host']
        print(f'NOTE {note} source_lines={counts["source_lines"]} '
              f'tokens={counts["tokens"]} unique={counts["unique"]} '
              f'web={counts["web"]} host={counts["host"]} '
              f'gaps={len(note_gaps)}')
        gaps.extend(note_gaps)

    for gap in gaps:
        print(gap)
    print(f'SUMMARY rev={rev} notes={total["notes"]} tokens={total["tokens"]} '
          f'unique={total["unique"]} web={total["web"]} host={total["host"]} '
          f'gaps={len(gaps)}')
    print('RESULT ' + ('PASS' if not gaps else 'FAIL'))
    return 0 if not gaps else 1


if __name__ == '__main__':
    sys.exit(main())
