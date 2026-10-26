#!/usr/bin/env python3
"""check84 - a round's axis verdict is read from a receipt committed at the closing revision.

QUALITY criterion 84 (draft, round 44). For each directory of receipts at REV, every
`MADO_AXIS: checked=... mismatched=... rev=<hex>` line names the revision it measured. The
closure needs at least one such receipt whose `rev=` is REV itself (a `TIP` receipt) and whose
line reads `mismatched=0` with `exit=0` beside it; a receipt naming the base or an earlier data
commit is a `BASE`/`DATA` reading and may not stand in for the tip.

Usage:
  check84.py --repo . --rev <CLOSING_REV> --receipts <DIR> [--dir <DIR> ...]
Exit 0 = PASS, 1 = FAIL (no tip receipt, or the tip receipt is red), 2 = setup error.
"""
import argparse
import re
import subprocess
import sys

AXIS = re.compile(r'MADO_AXIS:\s*checked=(\d+)\s+mismatched=(\d+)\s+rev=([0-9a-f]{7,40})')
FAILED = re.compile(r'^FAILED: [0-9a-f]{7,40}$', re.M)


def git(repo, *args):
    return subprocess.run(['git', '-C', repo] + list(args), capture_output=True, text=True)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--repo', required=True)
    ap.add_argument('--rev', required=True)
    ap.add_argument('--receipts', action='append', required=True)
    ap.add_argument('--disk', action='store_true',
                    help='read --receipts directories from disk (synthetic control tree)')
    a = ap.parse_args()

    files = []
    if a.disk:
        import os
        for d in a.receipts:
            if not os.path.isdir(d):
                print('SETUP_ERROR %s is not a directory' % d)
                return 2
            files.extend(os.path.join(d, f) for f in sorted(os.listdir(d))
                         if os.path.isfile(os.path.join(d, f)))
    else:
        for d in a.receipts:
            r = git(a.repo, 'ls-tree', '-r', '--name-only', a.rev, '--', d)
            if r.returncode:
                print('SETUP_ERROR cannot list %s at %s' % (d, a.rev))
                return 2
            files.extend(f for f in r.stdout.splitlines() if f.strip())
    if not files:
        print('SETUP_ERROR no receipt files under %s at %s' % (a.receipts, a.rev))
        return 2

    tip = None
    rows = 0
    for f in sorted(files):
        if a.disk:
            body = open(f, encoding='utf-8', errors='replace').read()
        else:
            body = git(a.repo, 'show', '%s:%s' % (a.rev, f)).stdout
        for m in AXIS.finditer(body):
            rows += 1
            rev, mism, checked = m.group(3), int(m.group(2)), int(m.group(1))
            kind = 'TIP' if a.rev.startswith(rev) or rev.startswith(a.rev[:7]) else 'OTHER'
            if kind == 'TIP':
                red = FAILED.search(body) is not None
                tip = (f, rev, mism, checked, red)
            print('AXIS %s rev=%s checked=%d mismatched=%d %s'
                  % (f, rev[:7], checked, mism, kind))

    if rows == 0:
        print('CHECK84: verdict=FAIL no MADO_AXIS line in %d receipts at %s'
              % (len(files), a.rev[:7]))
        return 1
    if tip is None:
        print('CHECK84: verdict=FAIL no receipt names the closing revision %s '
              '(only earlier revisions: a base/data reading)' % a.rev[:7])
        return 1
    f, rev, mism, checked, red = tip
    if mism or red:
        print('CHECK84: verdict=FAIL tip receipt %s mismatched=%d failed_line=%d'
              % (f, mism, 1 if red else 0))
        return 1
    print('CHECK84: verdict=PASS tip_receipt=%s rev=%s checked=%d mismatched=0'
          % (f, rev[:7], checked))
    return 0


if __name__ == '__main__':
    sys.exit(main())
