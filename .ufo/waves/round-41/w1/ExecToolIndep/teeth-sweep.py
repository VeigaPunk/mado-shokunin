#!/usr/bin/env python3
"""Exhaustive teeth sweep: flip every comparison site of the tool and run --selftest.

Stronger than the predicate's 6-of-N sample: it shows that every comparison in
the census code is load-bearing for the selftest. Sites are enumerated exactly as
the contract describes (functions not named *selftest*, *_check*, *_run*,
*_write*, main, usage).
"""
import ast
import os
import subprocess
import sys
import tempfile

TOOL = os.path.join(os.path.dirname(os.path.abspath(__file__)), "mado-globals.py")
EXCL = ("selftest", "_check", "_run", "_write")
FLIP = {ast.Eq: ast.NotEq, ast.NotEq: ast.Eq, ast.Lt: ast.GtE, ast.GtE: ast.Lt,
        ast.Gt: ast.LtE, ast.LtE: ast.Gt, ast.In: ast.NotIn, ast.NotIn: ast.In,
        ast.Is: ast.IsNot, ast.IsNot: ast.Is}


def sites(tree):
    found = []
    for node in ast.walk(tree):
        if not isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            continue
        if any(tag in node.name for tag in EXCL) or node.name in ("main", "usage"):
            continue
        for sub in ast.walk(node):
            if isinstance(sub, ast.Compare):
                found.append((node.name, sub.lineno, sub))
    return sorted(found, key=lambda item: (item[1], item[0]))


def flipped(src, index):
    tree = ast.parse(src)
    node = sites(tree)[index][2]
    node.ops = [FLIP[type(op)]() for op in node.ops]
    return ast.unparse(tree) + "\n"


def run(path):
    proc = subprocess.run([sys.executable, "-I", path, "--selftest"],
                          capture_output=True, text=True)
    summary = [ln for ln in proc.stdout.splitlines()
               if ln.startswith("MADO_GLOBALS_SELFTEST:")]
    return proc.returncode, (summary[0] if summary else None)


def parse_summary(summary):
    if not summary:
        return None
    counts = summary.split()[1].split("/")
    return int(counts[0]), int(counts[1])


def main():
    src = open(TOOL).read()
    found = sites(ast.parse(src))
    base_rc, base_summary = run(TOOL)
    print("baseline rc=%d %s sites=%d" % (base_rc, base_summary, len(found)))
    killed = 0
    with tempfile.TemporaryDirectory() as tmp:
        for index, (func, line, node) in enumerate(found):
            path = os.path.join(tmp, "mutant%d.py" % index)
            with open(path, "w") as handle:
                handle.write(flipped(src, index))
            rc, summary = run(path)
            counts = parse_summary(summary)
            dead = rc != 0 or counts is None or counts[0] < counts[1]
            killed += 1 if dead else 0
            print("site %2d %-14s line %4d %-26s rc=%d %-30s %s"
                  % (index, func, line, ast.unparse(node)[:26], rc,
                     summary or "no summary", "KILLED" if dead else "SURVIVED"))
    print("TEETH SWEEP: sites=%d killed=%d survived=%d"
          % (len(found), killed, len(found) - killed))
    return 0 if killed == len(found) else 1


if __name__ == "__main__":
    sys.exit(main())
