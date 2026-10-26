#!/usr/bin/env python3
"""Exhaustive teeth probe for mado-geometry.py (seat ExecIndepC, round 43).

Reimplements the frozen counter's `function_sites` / `mutate_source` rules
(c1-r42-geometry.py, lines 838-881): every single-operator ast.Compare inside a
function other than selftest/main/usage and not nested in selftest is a site.
For each site the source is mutated (operator flipped), unparsed, written to a
copy at the real layout name, and its `--selftest` run is scored. Prints one
line per site and a tally: `SITES total=<n> killed=<n> survivors=<list>`.

Run: python3 site-kill-probe.py <tool-path> <scratch-dir>
"""
import ast
import os
import re
import subprocess
import sys

NOT_SITES = ("selftest", "main", "usage")
FLIP = {ast.Eq: ast.NotEq, ast.NotEq: ast.Eq, ast.Lt: ast.GtE,
        ast.GtE: ast.Lt, ast.Gt: ast.LtE, ast.LtE: ast.Gt, ast.In: ast.NotIn,
        ast.NotIn: ast.In, ast.Is: ast.IsNot, ast.IsNot: ast.Is}
SUMMARY_TEXT = "MADO_GEOMETRY: rules="
SELFTEST_RE = re.compile(r"MADO_GEOMETRY_SELFTEST: (\d+)/(\d+) passed")


def function_sites(src):
    tree = ast.parse(src)
    nested = set()
    for fn in [n for n in ast.walk(tree) if isinstance(n, ast.FunctionDef)]:
        if fn.name == "selftest":
            for inner in ast.walk(fn):
                if isinstance(inner, ast.FunctionDef) and inner is not fn:
                    nested.add(id(inner))
    sites = []
    for fn in [n for n in ast.walk(tree) if isinstance(n, ast.FunctionDef)]:
        if fn.name in NOT_SITES or id(fn) in nested:
            continue
        summary = any(isinstance(c, ast.Constant) and isinstance(c.value, str)
                      and SUMMARY_TEXT in c.value for c in ast.walk(fn))
        for node in ast.walk(fn):
            if isinstance(node, ast.Compare) and len(node.ops) == 1 \
                    and type(node.ops[0]) in FLIP:
                sites.append(((fn.name, node.lineno, node.col_offset), summary))
    return sorted(set(sites))


def mutate_source(src, site):
    tree = ast.parse(src)
    for fn in [n for n in ast.walk(tree) if isinstance(n, ast.FunctionDef)]:
        if fn.name != site[0]:
            continue
        for node in ast.walk(fn):
            if isinstance(node, ast.Compare) and len(node.ops) == 1 \
                    and (node.lineno, node.col_offset) == site[1:] \
                    and type(node.ops[0]) in FLIP:
                node.ops[0] = FLIP[type(node.ops[0])]()
                return ast.unparse(tree)
    return None


def main():
    tool = os.path.abspath(sys.argv[1])
    scratch = os.path.abspath(sys.argv[2])
    src = open(tool).read()
    sites = function_sites(src)
    py = sys.executable
    killed = []
    survivors = []
    for site, summary in sites:
        mutated = mutate_source(src, site)
        label = "%s:%d:%d%s" % (site[0], site[1], site[2],
                                " (summary)" if summary else "")
        if mutated is None:
            print("site %s mutate=NONE" % label)
            survivors.append(label + " mutate-none")
            continue
        tag = "%s_%d_%d" % (site[0], site[1], site[2])
        d = os.path.join(scratch, "kill_" + tag)
        os.makedirs(d, exist_ok=True)
        path = os.path.join(d, "mado-geometry.py")
        with open(path, "w") as fh:
            fh.write(mutated)
        proc = subprocess.run([py, "-I", path, "--selftest"], cwd=d,
                              capture_output=True, text=True, timeout=120)
        match = SELFTEST_RE.search(proc.stdout)
        if match:
            k, n = int(match.group(1)), int(match.group(2))
            dead = proc.returncode != 0 or k != n
            note = "rc=%d %d/%d" % (proc.returncode, k, n)
        else:
            dead = True
            note = "rc=%d no-summary" % proc.returncode
        print("site %-34s dead=%d %s" % (label, dead, note))
        (killed if dead else survivors).append(label)
    print("SITES total=%d killed=%d survivors=%s"
          % (len(sites), len(killed), survivors))
    return 0 if not survivors else 1


if __name__ == "__main__":
    sys.exit(main())
