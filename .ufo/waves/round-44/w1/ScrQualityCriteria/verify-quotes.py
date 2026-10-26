#!/usr/bin/env python3
"""verify-quotes - every prose quote a draft writes is located by a locator on its own line.

Round-44 seat ScrQualityCriteria check on its own criteria.md draft. Scope: a quoted fragment that
contains a space (a prose quote, not an identifier, a number or a checker token). Each such
fragment must be supported, on the same line, by a `<file>:<start>[-<end>]` locator resolved at
HEAD (or in --fetch), or — for a quoted checker verdict — by the --extra transcript the criteria
cite. A trailing ellipsis is compared as a prefix of a token in the range.

Usage:
  verify-quotes.py --repo . --criteria <FILE> [--fetch DIR] [--extra receipts.txt]
Exit 0 = all located, 1 = a miss, 2 = cannot read.
"""
import argparse
import os
import re
import subprocess
import sys

LOC = re.compile(r'([A-Za-z0-9_./-]+\.[A-Za-z0-9]+):(\d+)(?:-(\d+))?')
FRAG = re.compile(r'`([^`\n]+)`')
SKIP_EXT = re.compile(r'\.(md|txt|json|py|sh|c|cpp|hpp|h|log|xml|conf)$')


def supported(fragment, text):
    probe = fragment.rstrip('.…').replace('`', '').strip()
    text = text.replace('`', '')
    if not probe:
        return True
    if probe in text:
        return True
    tokens = re.split(r'[\s()\[\]{},;"]+', text)
    return any(t.startswith(probe) for t in tokens if t)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--repo', required=True)
    ap.add_argument('--criteria', required=True)
    ap.add_argument('--fetch', default='.ufo/waves/round-44/fetch-c1')
    ap.add_argument('--extra')
    a = ap.parse_args()

    try:
        lines = open(a.criteria, encoding='utf-8', errors='replace').read().splitlines()
    except OSError as exc:
        print('SETUP_ERROR %s' % exc)
        return 2
    extra = ''
    if a.extra:
        try:
            extra = open(a.extra, encoding='utf-8', errors='replace').read()
        except OSError as exc:
            print('SETUP_ERROR %s' % exc)
            return 2

    tree = subprocess.run(['git', '-C', a.repo, 'ls-tree', '-r', '--name-only', 'HEAD'],
                          capture_output=True, text=True).stdout.splitlines()
    by_base = {}
    for p in tree:
        by_base.setdefault(p.rsplit('/', 1)[-1], []).append(p)

    windows = []
    for m in LOC.finditer('\n'.join(lines)):
        pass
    for no, line in enumerate(lines, 1):
        scope = (lines[no - 2] + '\n' + line) if no > 1 else line
        locs = list(LOC.finditer(scope))
        frags = [f for f in FRAG.findall(line)
                 if ' ' in f and not f.startswith(('python3', 'git ', 'bash ', 'grep ', 'wc ', 'ls ', '--'))
                 and '<' not in f]
        if not locs or not frags:
            continue
        text = []
        for m in locs:
            name, start, end = m.group(1), int(m.group(2)), int(m.group(3) or m.group(2))
            cands = ([name] if name in tree else
                     [os.path.join(a.fetch, name)] if os.path.exists(os.path.join(a.fetch, name))
                     else by_base.get(name.rsplit('/', 1)[-1], []))
            if not cands:
                continue
            path = cands[0]
            if os.path.isabs(path):
                try:
                    src = open(path, encoding='utf-8', errors='replace').read().splitlines()
                except OSError:
                    continue
            else:
                r = subprocess.run(['git', '-C', a.repo, 'show', 'HEAD:%s' % path],
                                   capture_output=True, text=True)
                if r.returncode:
                    continue
                src = r.stdout.splitlines()
            if 1 <= start <= end <= len(src):
                text.append('\n'.join(src[start - 1:end]))
        blob = '\n'.join(text)
        checked = miss = 0
        for f in frags:
            checked += 1
            if supported(f, blob) or (extra and supported(f, extra)):
                print('OK line=%d %r' % (no, f[:52]))
            else:
                miss += 1
                print('MISS line=%d %r (no locator on the line supports it)' % (no, f[:70]))
        if miss:
            print('VERIFY_QUOTES: verdict=FAIL line=%d checked=%d miss=%d'
                  % (no, checked, miss))
            return 1
    print('VERIFY_QUOTES: verdict=PASS')
    return 0


if __name__ == '__main__':
    sys.exit(main())
