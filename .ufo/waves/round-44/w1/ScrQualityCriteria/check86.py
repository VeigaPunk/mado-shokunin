#!/usr/bin/env python3
"""check86 - a locator's source is resolved from the repository, and its range carries the
identifiers the line names.

QUALITY criterion 86 (draft, round 44). Extends criterion 77 in two directions its checker does
not reach: the source may be any committed lane file (not only a file in the pinned `fetch/`
directory), and the identifiers may be plain tokens on the line (not only backticked fragments).
For each `<name>:<start>` or `<name>:<start>-<end>` token:

  RESOLVE  `<name>` is read at REV by exact path, or by unique basename; no match and an
           ambiguous basename are violations.
  RANGE    1 <= start <= end <= the source's line count.
  INSIDE   every code-shaped identifier on the citing line (snake_case: `[A-Za-z][A-Za-z0-9]*_..`)
           that occurs anywhere in the source also occurs inside the cited range. An identifier
           that occurs only outside the range is reported with its first line.

Usage:
  check86.py --repo . --rev <REV> --file <PATH-IN-REPO> [--text --file-file PATH]
             [--only gkeep-shm.c]
Exit 0 = PASS, 1 = FAIL, 2 = setup error.
"""
import argparse
import re
import subprocess
import sys

LOC = re.compile(r'([A-Za-z0-9_./-]+\.[A-Za-z0-9]+):(\d+)(?:-(\d+))?')
IDENT = re.compile(r'\b([A-Za-z][A-Za-z0-9]*_[A-Za-z0-9_]+)\b')


def git(repo, *args):
    return subprocess.run(['git', '-C', repo] + list(args), capture_output=True, text=True)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--repo', required=True)
    ap.add_argument('--rev', required=True)
    ap.add_argument('--file')
    ap.add_argument('--file-file')
    ap.add_argument('--text', action='store_true')
    ap.add_argument('--only', default='')
    a = ap.parse_args()

    if a.text:
        try:
            body = open(a.file_file, encoding='utf-8', errors='replace').read()
        except OSError as exc:
            print('SETUP_ERROR %s' % exc)
            return 2
        label = a.file_file
    else:
        if not a.file:
            print('SETUP_ERROR one of --file or --file-file is required')
            return 2
        r = git(a.repo, 'show', '%s:%s' % (a.rev, a.file))
        if r.returncode:
            print('SETUP_ERROR %s absent at %s' % (a.file, a.rev[:7]))
            return 2
        body = r.stdout
        label = a.file

    tree = [p for p in git(a.repo, 'ls-tree', '-r', '--name-only', a.rev).stdout.splitlines() if p]
    by_base = {}
    for p in tree:
        by_base.setdefault(p.rsplit('/', 1)[-1], []).append(p)

    judged = 0
    bad = 0
    for line in body.splitlines():
        for m in LOC.finditer(line):
            name, start, end = m.group(1), int(m.group(2)), int(m.group(3) or m.group(2))
            if a.only and a.only != name.rsplit('/', 1)[-1]:
                continue
            base = name.rsplit('/', 1)[-1]
            hits = [name] if name in tree else by_base.get(base, [])
            if not hits:
                print('UNRESOLVED %s (no committed file of that name at %s)' % (name, a.rev[:7]))
                bad += 1
                continue
            if len(hits) > 1:
                print('AMBIGUOUS %s -> %s' % (name, ' '.join(hits[:4])))
                bad += 1
                continue
            path = hits[0]
            src = git(a.repo, 'show', '%s:%s' % (a.rev, path)).stdout.splitlines()
            if not (1 <= start <= end <= len(src)):
                print('RANGE %s:%d-%d source has %d lines' % (name, start, end, len(src)))
                bad += 1
                continue
            judged += 1
            ids = sorted(set(IDENT.findall(line)))
            inside, outside, skipped = [], [], []
            for ident in ids:
                where = [i + 1 for i, ln in enumerate(src) if re.search(r'\b%s\b' % re.escape(ident), ln)]
                if not where:
                    skipped.append(ident)
                elif any(start <= w <= end for w in where):
                    inside.append(ident)
                else:
                    outside.append('%s@%d' % (ident, where[0]))
            if outside:
                print('OUTSIDE %s:%d-%d ids_inside=%d ids_outside=%s'
                      % (name, start, end, len(inside), ','.join(outside)))
                bad += 1
            else:
                print('OK %s:%d-%d ids_inside=%s skipped=%s'
                      % (name, start, end, ','.join(inside) or '-', ','.join(skipped) or '-'))

    if not judged and not bad:
        print('NO-LOCATORS %s cached=0' % label)
        return 1
    if bad:
        print('CHECK86: verdict=FAIL locators=%d violations=%d' % (judged + bad, bad))
        return 1
    print('CHECK86: verdict=PASS locators=%d violations=0' % judged)
    return 0


if __name__ == '__main__':
    sys.exit(main())
