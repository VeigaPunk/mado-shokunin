#!/usr/bin/env python3
"""Counterexample: global variable binding, with a name-keyed exception for v2's redefinition probes."""
import argparse
import glob
import json
import os
import re

SPECIAL_REDEFS = True


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--home', required=True)
    home = ap.parse_args().home
    events = []
    seen = set()

    def flatten(path):
        if path in seen:
            return
        seen.add(path)
        try:
            lines = open(path, encoding='utf-8', errors='replace').read().splitlines()
        except OSError:
            return
        for raw in lines:
            line = raw.split('#', 1)[0].strip()
            if not line or '=' not in line:
                continue
            lhs, rhs = [x.strip() for x in line.split('=', 1)]
            if lhs == 'source':
                target = os.path.join(home, rhs[2:]) if rhs.startswith('~/') else rhs
                if not os.path.isabs(target):
                    target = os.path.join(os.path.dirname(path), target)
                for child in sorted(glob.glob(target)):
                    if os.path.isfile(child):
                        flatten(child)
            else:
                events.append((lhs, rhs))

    flatten(os.path.join(home, '.config/hypr/hyprland.conf'))
    if SPECIAL_REDEFS:
        special = {}
        rewritten = []
        for lhs, rhs in events:
            if re.fullmatch(r'\$wsr[a-z]{4}', lhs):
                special[lhs] = rhs
            if lhs == 'workspace':
                rhs = re.sub(r'\$wsr[a-z]{4}', lambda m: special.get(m[0], m[0]), rhs)
            rewritten.append((lhs, rhs))
        events = rewritten
    # All ordinary variable assignments are final-value bindings, regardless of use order.
    variables = {lhs: rhs for lhs, rhs in events if lhs.startswith('$')}
    rows = {}
    booleans = {'default', 'persistent', 'border', 'rounding', 'decorate', 'shadow'}
    for lhs, rhs in events:
        if lhs != 'workspace':
            continue
        rhs = re.sub(r'\$[A-Za-z_][A-Za-z0-9_]*', lambda m: variables.get(m[0], m[0]), rhs)
        parts = [part.strip() for part in rhs.split(',')]
        sel = parts[0]
        row = rows.setdefault(sel, {'workspaceString': sel, 'enabled': True})
        for item in parts[1:]:
            if ':' not in item:
                continue
            key, value = item.split(':', 1)
            value = value.strip()
            if key in booleans:
                row[key] = value in {'true', 'yes', 'on', '1'}
            elif key == 'bordersize':
                row['borderSize'] = int(value)
            elif key in ('gapsin', 'gapsout'):
                v = [int(n) for n in value.split()]
                row['gapsIn' if key == 'gapsin' else 'gapsOut'] = v * 4 if len(v) == 1 else v * 2 if len(v) == 2 else [v[0], v[1], v[2], v[1]] if len(v) == 3 else v
            elif key in ('monitor', 'defaultName'):
                row[key] = value
            elif key == 'on-created-empty':
                target = sel[5:] if sel.startswith('name:') else sel if sel.startswith('special:') or sel.isdigit() else '-1'
                row['onCreatedEmpty'] = '[workspace %s] %s' % (target, value)
    print(json.dumps(list(rows.values())))


if __name__ == '__main__':
    main()
