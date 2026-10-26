#!/usr/bin/env python3
"""ExecFixtureMap: what the clause-g generator's literal vocabulary can and cannot reach.

Literal-evaluates the KEYS / LISTL / ARGVS / DESKS / LISTS constants of the frozen C1 counter
(read-only) and reports, for each token the map cares about, whether the generator can produce it.
Static: nothing is run from the counter.

Usage: gen-vocabulary.py [--counter PATH]
"""
import argparse
import ast
import re

DEFAULT = "/home/vgpnk/Projects/shokunin/mado-shokunin/quality/counters/c1-r47-terminal.py"
TOKENS = ["%d", "%D", "%n", "%N", "%v", "%m", "%f", "%u", "%U", "%k", "%i", "%c",
          "\\n", "\\t", "\\r", "\\\\", "\\s",
          "XTE_DEBUG", "XTE_CACHE_ENABLED", "XTE_EXECARG_COMPAT", "DEBUG",
          "--help", "-h", "/enable_cache", "/execarg_compat", "/execarg_strict",
          "TerminalArgTitle=-T=", "TerminalArgTitle=--title=", "--print-path",
          "NotShowIn=Hyprland;", "--title=", "--hold"]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--counter", default=DEFAULT)
    a = ap.parse_args()
    src = open(a.counter).read()
    vals = {}
    for n in ast.parse(src).body:
        if isinstance(n, ast.Assign) and isinstance(n.targets[0], ast.Name):
            try:
                vals[n.targets[0].id] = ast.literal_eval(n.value)
            except Exception:
                pass
    print("# clause-g generator vocabulary of %s, literal-evaluated (ast)" % a.counter)
    for name in ("KEYS", "LISTL", "ARGVS", "DESKS", "LISTS", "NAMES"):
        v = vals.get(name)
        if not isinstance(v, (list, tuple)):
            continue
        print("\n## %s  n=%d" % (name, len(v)))
        for x in v:
            print("  %r" % (x,))
    def flat(v):
        for x in v or []:
            if isinstance(x, (list, tuple)):
                for y in x:
                    yield y
            elif isinstance(x, str):
                yield x
    allv = [x for name in ("KEYS", "LISTL", "ARGVS", "DESKS", "LISTS") for x in flat(vals.get(name))]
    print("\n## token presence across KEYS+LISTL+ARGVS+DESKS+LISTS (%d strings)" % len(allv))
    for tok in TOKENS:
        hits = [x for x in allv if tok in x]
        print("  %-26r %2d  %r" % (tok, len(hits), hits[:3]))
    print("\n## env keys gen_case can set: %r"
          % (sorted(set(re.findall(r'env\["([A-Za-z_]+)"\]', src))),))
    print("## XTE_DEBUG occurrences in counter: %d" % src.count("XTE_DEBUG"))
    print("## XTE_CACHE occurrences in counter: %d" % src.count("XTE_CACHE"))
    print("## 'DEBUG' occurrences in counter: %d" % src.count("DEBUG"))


if __name__ == "__main__":
    main()
