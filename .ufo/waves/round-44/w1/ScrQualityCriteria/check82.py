#!/usr/bin/env python3
"""check82 - a tool's verdict vocabulary is audited against the state fields its input carries.

QUALITY criterion 82 (draft, round 44). The input's producer is pinned source; the field list
is derived from the producer's serializer, never from the tool's own reading. Three legs:

  L1 source   every `--must KEY:FILE:LINE` locator lands on a line of FILE that prints `"KEY":`,
              and the key is inside the client-object block the tool's input comes from.
  L2 mention  the tool names KEY (case-insensitive) or ships `IGNORED-FIELD KEY <reason>`
              in the declaration file (`--declare`, optional), so silence is a decision.
  L3 teeth    the tool's selftest carries a case whose name contains KEY, so a tool that
              consumed the field has a case that fails when the field stops mattering.

Scoring scope is the claim's own subject (`--must`), not every field the block prints: the
block's remaining scalar keys are printed under `--audit` for a later round to widen.

Usage:
  check82.py --source FETCH/Hyprland-HyprCtl.cpp --tool TOOL --must fullscreen:Hyprland-HyprCtl.cpp:410
             [--declare FILE] [--audit]
Exit 0 = PASS, 1 = FAIL, 2 = setup error (source/tool unreadable or no block found).
"""
import argparse
import os
import re
import sys

KEY_LINE = re.compile(r'^\s*"([A-Za-z][A-Za-z0-9]*)":\s*(\S.*?),\s*$')
IDENT = re.compile(r'IGNORED-FIELD\s+([A-Za-z][A-Za-z0-9]*)\b')


def client_block(lines):
    """Return (start, end, [(key, value_form)]) for the clients -j client object."""
    for i, ln in enumerate(lines):
        if ln.strip() == '"address": "0x{:x}",':
            window = lines[i:i + 60]
            if not any('"stableId"' in w for w in window):
                continue
            rows = []
            for j in range(i, min(i + 60, len(lines))):
                m = KEY_LINE.match(lines[j])
                if m:
                    rows.append((j, m.group(1), m.group(2)))
                if '"stableId"' in lines[j]:
                    return i, j, rows
    return None, None, []


def form(value):
    if value.startswith('['):
        return 'list'
    if value.startswith('"'):
        return 'string'
    return 'scalar'


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--source', required=True)
    ap.add_argument('--tool', required=True)
    ap.add_argument('--must', action='append', default=[],
                    metavar='KEY:FILE:LINE')
    ap.add_argument('--declare')
    ap.add_argument('--audit', action='store_true')
    a = ap.parse_args()

    try:
        src_lines = open(a.source, encoding='utf-8', errors='replace').read().splitlines()
        tool = open(a.tool, encoding='utf-8', errors='replace').read()
    except OSError as exc:
        print('SETUP_ERROR %s' % exc)
        return 2

    start, end, rows = client_block(src_lines)
    if not rows:
        print('SETUP_ERROR no client-object block with "address"/"stableId" in %s' % a.source)
        return 2
    keys = {k: form(v) for _, k, v in rows}
    print('BLOCK %s:%d-%d keys=%d scalar=%d string=%d list=%d'
          % (os.path.basename(a.source), start + 1, end + 1, len(keys),
             sum(1 for f in keys.values() if f == 'scalar'),
             sum(1 for f in keys.values() if f == 'string'),
             sum(1 for f in keys.values() if f == 'list')))

    declared = {}
    if a.declare:
        try:
            for ln in open(a.declare, encoding='utf-8', errors='replace'):
                m = IDENT.search(ln)
                if m:
                    declared[m.group(1)] = ln.strip()
        except OSError as exc:
            print('SETUP_ERROR %s' % exc)
            return 2
    print('DECLARED %d %s' % (len(declared), ' '.join(sorted(declared)) or '-'))

    if not a.must:
        print('SETUP_ERROR --must KEY:FILE:LINE is required (scope is the claim subject)')
        return 2

    bad = 0
    for spec in a.must:
        try:
            key, _file, line = spec.split(':')
            line = int(line)
        except ValueError:
            print('SETUP_ERROR bad --must %r (want KEY:FILE:LINE)' % spec)
            return 2
        cited = src_lines[line - 1] if 0 < line <= len(src_lines) else ''
        loc = 'OK' if ('"%s":' % key) in cited else 'MISS'
        if loc == 'MISS':
            bad += 1
        mention = len(re.findall(r'\b%s\b' % re.escape(key), tool, re.IGNORECASE))
        declared_here = key in declared
        cases = len(re.findall(r'chk\(\s*"[^"]*%s[^"]*"' % re.escape(key), tool, re.IGNORECASE))
        if loc == 'MISS':
            leg_status = 'L1-source-miss'
        elif mention == 0 and not declared_here:
            leg_status = 'L2-unmentioned-undeclared'
            bad += 1
        elif cases == 0 and not declared_here and keys.get(key) != 'string':
            leg_status = 'L3-no-selftest-case'
            bad += 1
        else:
            leg_status = 'ok'
        print('FIELD %s src=%s:%d loc=%s block=%s mention=%d declare=%d case=%d %s'
              % (key, _file, line, loc, keys.get(key, 'ABSENT'), mention,
                 1 if declared_here else 0, cases, leg_status))

    if a.audit:
        silent = [k for k, f in sorted(keys.items())
                  if f != 'string'
                  and not re.search(r'\b%s\b' % re.escape(k), tool, re.IGNORECASE)
                  and k not in declared]
        print('AUDIT unmentioned-undeclared=%d %s' % (len(silent), ' '.join(silent) or '-'))

    if bad:
        print('CHECK82: verdict=FAIL fields=%d violations=%d' % (len(a.must), bad))
        return 1
    print('CHECK82: verdict=PASS fields=%d violations=0' % len(a.must))
    return 0


if __name__ == '__main__':
    sys.exit(main())
