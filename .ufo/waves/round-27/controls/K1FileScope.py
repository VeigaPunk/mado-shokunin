#!/usr/bin/env python3
"""Counterexample: streaming variables, but a definition made inside a sourced file stays local to that file."""
import argparse
import glob
import json
import os
import re

VAR = re.compile(r'\$[A-Za-z_][A-Za-z0-9_]*')
BOOLEANS = {'default', 'persistent', 'border', 'rounding', 'decorate', 'shadow'}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--home', required=True)
    home = ap.parse_args().home
    rows = {}

    def expand(text, env):
        return VAR.sub(lambda m: env.get(m[0], m[0]), text)

    def apply(rhs):
        parts = [part.strip() for part in rhs.split(',')]
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

    def run(path, env, depth):
        if depth > 16:
            return
        try:
            lines = open(path, encoding='utf-8', errors='replace').read().splitlines()
        except OSError:
            return
        for raw in lines:
            line = raw.split('#', 1)[0].strip()
            if '=' not in line:
                continue
            lhs, rhs = [x.strip() for x in line.split('=', 1)]
            if lhs.startswith('$'):
                env[lhs] = expand(rhs, env)
            elif lhs == 'source':
                target = expand(rhs, env)
                target = os.path.join(home, target[2:]) if target.startswith('~/') else target
                if not os.path.isabs(target):
                    target = os.path.join(os.path.dirname(path), target)
                for child in sorted(glob.glob(target)):
                    if os.path.isfile(child):
                        run(child, dict(env), depth + 1)  # the deviation: child definitions never reach the parent
            elif lhs == 'workspace':
                apply(expand(rhs, env))

    run(os.path.join(home, '.config/hypr/hyprland.conf'), {}, 0)
    print(json.dumps(list(rows.values())))


if __name__ == '__main__':
    main()
