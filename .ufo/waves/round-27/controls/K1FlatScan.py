#!/usr/bin/env python3
"""Counterexample only: never follows source directives or execution-time variable scope."""
import argparse
import json
import os
import re


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--home', required=True)
    home = ap.parse_args().home
    files = []
    for root in ['.config/hypr', '.config/omarchy/current/theme', '.local/share/omarchy/default/hypr', '.local/state/omarchy/toggles/hypr']:
        for dp, _, names in os.walk(os.path.join(home, root)):
            for name in sorted(names):
                p = os.path.join(dp, name)
                rel = os.path.relpath(p, home)
                try:
                    text = open(p, encoding='utf-8', errors='replace').read()
                except OSError:
                    continue
                bucket = 1 if rel == '.config/hypr/hyprland.conf' else 2 if re.fullmatch(r'\.config/hypr/[a-z]{6}\.conf', rel) else 0
                files.append((bucket, rel, text))
    files.sort()
    variables = {}
    for _, _, text in files:
        for raw in text.splitlines():
            m = re.match(r'\s*(\$ws[a-z]{3})\s*=\s*(.*)', raw.split('#', 1)[0])
            if m:
                variables[m[1]] = m[2].strip()
    out = {}
    rename = {'bordersize': 'borderSize', 'defaultName': 'defaultName', 'gapsin': 'gapsIn', 'gapsout': 'gapsOut'}
    booleans = {'default', 'persistent', 'border', 'rounding', 'decorate', 'shadow'}
    for _, _, text in files:
        for raw in text.splitlines():
            line = raw.split('#', 1)[0].strip()
            if not line.startswith('workspace') or '=' not in line:
                continue
            lhs, rhs = line.split('=', 1)
            if lhs.strip() != 'workspace':
                continue
            rhs = re.sub(r'\$ws[a-z]{3}', lambda m: variables.get(m[0], m[0]), rhs)
            parts = [x.strip() for x in rhs.split(',')]
            sel = parts[0]
            row = out.setdefault(sel, {'workspaceString': sel, 'enabled': True})
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
                    row[rename[key]] = v * 4 if len(v) == 1 else v * 2 if len(v) == 2 else [v[0], v[1], v[2], v[1]] if len(v) == 3 else v
                elif key in ('monitor', 'defaultName'):
                    row[key] = value
                elif key == 'on-created-empty':
                    target = sel[5:] if sel.startswith('name:') else sel if sel.startswith('special:') or sel.isdigit() else '-1'
                    row['onCreatedEmpty'] = '[workspace %s] %s' % (target, value)
                # Ignore layoutopt and every other rule item.
    print(json.dumps(list(out.values())))


if __name__ == '__main__':
    main()
