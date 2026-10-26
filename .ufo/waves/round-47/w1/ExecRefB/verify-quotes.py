#!/usr/bin/env python3
"""verify-quotes.py -- machine-check every quote in the seat report.

For each `locator<TAB>quote` row in receipts/quotes.tsv:
  1. the line at <locator> in the pinned script must contain <quote>
     (so the locator was computed, not typed);
  2. the report must contain <quote> verbatim (so the quote is not invented).

Usage: verify-quotes.py [--script PATH] [--report PATH] [--table PATH]
Exit 0 when every row passes, 1 otherwise.
"""
import argparse
import os
import sys


def main(argv):
    here = os.path.dirname(os.path.abspath(__file__))       # the seat directory
    ap = argparse.ArgumentParser()
    ap.add_argument('--script', default='/usr/bin/xdg-terminal-exec')
    ap.add_argument('--report', default=os.path.join(
        os.path.dirname(here), os.path.basename(here) + '.md'))
    ap.add_argument('--table', default=os.path.join(here, 'receipts', 'quotes.tsv'))
    args = ap.parse_args(argv[1:])

    with open(args.script, 'r', encoding='utf-8', errors='replace') as f:
        source = f.read().splitlines()
    with open(args.report, 'r', encoding='utf-8') as f:
        report = f.read()

    failures = 0
    rows = 0
    with open(args.table, 'r', encoding='utf-8') as f:
        for raw in f:
            raw = raw.rstrip('\n')
            if not raw or raw.startswith('#'):
                continue
            rows += 1
            locator, quote = raw.split('\t', 1)
            lineno = int(locator)
            line = source[lineno - 1] if 0 < lineno <= len(source) else ''
            in_source = quote in line
            in_report = quote in report
            status = 'ok' if (in_source and in_report) else 'FAIL'
            if status == 'FAIL':
                failures += 1
            print('%-4s %s  in_source=%s in_report=%s  %s'
                  % (status, locator, in_source, in_report, quote))
    print('QUOTES: %d/%d verified (locator and report)' % (rows - failures, rows))
    return 0 if failures == 0 else 1


if __name__ == '__main__':
    sys.exit(main(sys.argv))
