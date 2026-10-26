#!/usr/bin/env python3
"""Mutation test for clause f, run D (forged cache): take an implementation that models a cold cache, add one hook that
prints the resolver's cached fields whenever a cache file exists, and require the counter to reject it on the cacheD
runs only.

The hook is inert when no cache exists (runs A-C, generated cases) and deviates exactly when the counter forges a cache,
so a counter that does not forge one cannot tell the mutant from the original.

Usage: make-cacheread-mutant.py --ref <mado-terminal.py> --out <mutant.py>
"""
import argparse
import sys

HOOK = '''def _cache_hook(args):
    """MUTATION: read the resolver's cache instead of modelling a cold one."""
    ch = os.environ.get('XDG_CACHE_HOME')
    if not ch:
        return None
    p = os.path.join(ch, 'xdg-terminal-exec')
    try:
        with open(p, errors='replace') as f:
            lines = f.read().split('\\n')
    except OSError:
        return None
    if len(lines) < 11:
        return None
    vals = []
    for a in args:
        if a == '--print-id':
            vals.append(lines[3] + (':' + lines[4] if lines[4] else ''))
        elif a == '--print-path':
            vals.append(lines[2])
        elif a == '--print-cmd' or a.startswith('--print-cmd='):
            vals.append(lines[10].split('\\x1e')[0].replace('\\x1f', '\\n'))
    if not vals:
        return None
    sys.stdout.write('\\n'.join(vals) + '\\n')
    return 0


def main(argv):'''


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--ref", required=True)
    ap.add_argument("--out", required=True)
    a = ap.parse_args()
    src = open(a.ref).read()
    if "def main(argv):" not in src:
        raise SystemExit("reference has no main(argv)")
    if "'print':" not in src:
        raise SystemExit("reference has no print command")
    src = src.replace("def main(argv):", HOOK, 1)
    needle = "    if command == 'print':\n        return cmd_print(args[1:])"
    if needle not in src:
        raise SystemExit("reference print dispatch shape changed")
    src = src.replace(needle, "    if command == 'print':\n        hit = _cache_hook(args[1:])\n"
                              "        if hit is not None:\n            return hit\n"
                              "        return cmd_print(args[1:])", 1)
    with open(a.out, "w") as f:
        f.write(src)
    print("mutant=%s ref=%s bytes=%d" % (a.out, a.ref, len(src)))


if __name__ == "__main__":
    sys.exit(main())
