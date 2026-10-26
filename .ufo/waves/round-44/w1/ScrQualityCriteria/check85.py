#!/usr/bin/env python3
"""check85 - a registration's stated seat count is one number with the wave's results file.

QUALITY criterion 85 (draft, round 44). A frozen registration is a plan, so its numbers are
plans; the closure must not quote a plan number as the executed count. Two admissible forms:

  bound    the registration states no literal seat number and names the results file as the
           source of the counts (`recorded from each wave's *-results.json`), or
  equal    every literal `w<k> ... N seats` equals both the results file's `seats` field and
           its `results` array length, and any `planned ... total N` equals their sum.

Anything else is a violation, including a registration that states a literal number with no
results file to compare against at REV.

Usage:
  check85.py --repo . --rev <REV> --registration .ufo/waves/round-N/registration.md
             --results w1=.ufo/waves/round-N/w1-results.json [--results w2=...]
Exit 0 = PASS, 1 = FAIL, 2 = setup error.
"""
import argparse
import json
import re
import subprocess
import sys

WAVE = re.compile(r'`?(w[0-9])`?[^.;\n]{0,120}?(\d+)\s+seats')
TOTAL = re.compile(r'total\s+\*{0,2}(\d+)')
BOUND = re.compile(r'recorded from each wave.s `?\*-results\.json')


def git(repo, *args):
    return subprocess.run(['git', '-C', repo] + list(args), capture_output=True, text=True)


def read(repo, rev, path, text):
    if text:
        try:
            return open(path, encoding='utf-8', errors='replace').read()
        except OSError as exc:
            print('SETUP_ERROR %s' % exc)
            return None
    r = git(repo, 'show', '%s:%s' % (rev, path))
    if r.returncode:
        print('SETUP_ERROR %s absent at %s' % (path, rev[:7]))
        return None
    return r.stdout


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--repo', required=True)
    ap.add_argument('--rev', required=True)
    ap.add_argument('--registration', required=True)
    ap.add_argument('--results', action='append', default=[], metavar='WAVE=PATH')
    ap.add_argument('--text', action='store_true',
                    help='read both files from disk instead of from --rev')
    a = ap.parse_args()

    reg = read(a.repo, a.rev, a.registration, a.text)
    if reg is None:
        return 2

    counts = {}
    for line in reg.splitlines():
        for m in WAVE.finditer(line):
            counts.setdefault(m.group(1), []).append(int(m.group(2)))
    totals = [int(m.group(1)) for line in reg.splitlines() for m in TOTAL.finditer(line)]
    bound = BOUND.search(reg) is not None
    print('REGISTRATION %s waves=%s total=%s bound=%d'
          % (a.registration,
             ' '.join('%s:%s' % (k, ','.join(map(str, v))) for k, v in sorted(counts.items())) or '-',
             totals or '-', 1 if bound else 0))

    results = {}
    for spec in a.results:
        wave, _, path = spec.partition('=')
        body = read(a.repo, a.rev, path, a.text)
        if body is None:
            return 2
        try:
            d = json.loads(body)
        except json.JSONDecodeError as exc:
            print('SETUP_ERROR %s is not JSON (%s)' % (path, exc))
            return 2
        results[wave] = (d.get('seats'), len(d.get('results', [])), path)
    if results:
        print('RESULTS %s' % ' '.join(
            '%s:seats=%s rows=%s' % (w, v[0], v[1]) for w, v in sorted(results.items())))

    bad = 0
    for wave, numbers in sorted(counts.items()):
        if wave not in results:
            print('VIOLATION WAVE %s plan=%s has no results file to compare'
                  % (wave, ','.join(map(str, numbers))))
            bad += 1
            continue
        seats, rows, path = results[wave]
        for n in numbers:
            if n != seats or n != rows:
                print('VIOLATION WAVE %s plan=%d results_seats=%s results_rows=%d (%s)'
                      % (wave, n, seats, rows, path))
                bad += 1
    for t in totals:
        if results and len(results) == len(counts):
            got = sum(v[1] for v in results.values())
            if t != got:
                print('VIOLATION TOTAL plan=%d results_rows=%d' % (t, got))
                bad += 1
    if not counts and not bound:
        print('VIOLATION UNBOUND registration states no seat count and does not bind the count '
              'to the results file')
        bad += 1
    if not counts and bound:
        print('NOTE bound-form: counts are to be read from the results files, none stated')

    if bad:
        print('CHECK85: verdict=FAIL violations=%d' % bad)
        return 1
    print('CHECK85: verdict=PASS')
    return 0


if __name__ == '__main__':
    sys.exit(main())
