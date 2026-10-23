#!/usr/bin/env python3
"""Counterexample (adapted global prepass, no name keying): a name defined once is bound everywhere regardless of
position; only a redefined name is bound by position. Variables are substituted only as whole comma-separated
fields, and each file is read at most once."""
import argparse
import glob
import json
import os

BOOLEANS = {'default', 'persistent', 'border', 'rounding', 'decorate', 'shadow'}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--home', required=True)
    home = ap.parse_args().home
    events = []
    seen = set()

    def flatten(path):
        if path in seen:  # deviation: a file sourced twice is read once
            return
        seen.add(path)
        try:
            lines = open(path, encoding='utf-8', errors='replace').read().splitlines()
        except OSError:
            return
        for raw in lines:
            line = raw.split('#', 1)[0].strip()
            if '=' not in line:
                continue
            lhs, rhs = [x.strip() for x in line.split('=', 1)]
            if lhs == 'source':
                target = os.path.join(home, rhs[2:]) if rhs.startswith('~/') else rhs
                if not os.path.isabs(target):
                    target = os.path.join(os.path.dirname(path), target)
                for child in sorted(glob.glob(target)):
                    if os.path.isfile(child):
                        flatten(child)
            elif lhs.startswith('$') or lhs == 'workspace':
                events.append((lhs, rhs))

    flatten(os.path.join(home, '.config/hypr/hyprland.conf'))
    defs = {}
    for i, (lhs, rhs) in enumerate(events):
        if lhs.startswith('$'):
            defs.setdefault(lhs, []).append((i, rhs))

    def bind(field, i):
        d = defs.get(field)  # deviation: only a whole field equal to `$name` is substituted
        if not d:
            return field
        if len(d) == 1:  # deviation: a once-defined name is bound globally, ignoring position
            return d[0][1]
        before = [v for j, v in d if j < i]
        return before[-1] if before else field

    rows = {}
    for i, (lhs, rhs) in enumerate(events):
        if lhs != 'workspace':
            continue
        parts = [bind(part.strip(), i) for part in rhs.split(',')]
        sel = parts[0]
        row = rows.setdefault(sel, {'workspaceString': sel, 'enabled': True})
        for item in parts[1:]:
            if ':' not in item:
                continue
            key, value = item.split(':', 1)
            value = value.strip()
            if key in BOOLEANS:
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
