#!/usr/bin/env python3
"""YAGNI reference sketch for PRED-C1-r51 (SimplifierLedger, round 51 w1).

Not a deliverable: a lower-bound implementation used to measure what the frozen
sentence actually costs, so the review can say "delete X, it buys nothing".
Reads git objects only; writes nothing; selftest is pure (no git, no tempdir).
"""
import argparse
import os
import re
import subprocess
import sys

ROW = re.compile(r"^\|\s*`([^`]+)`\s*\|\s*([^|]*)\|\s*`([^`]+)`[^|]*\|")


def git(repo, *args):
    p = subprocess.run(["git", "-C", repo, *args], capture_output=True)
    if p.returncode:
        raise SystemExit(2)
    return p.stdout.decode("utf-8", "replace")


def tree(repo, rev):
    return [l for l in git(repo, "ls-tree", "-r", "--name-only", rev).splitlines() if l]


def population(names):
    p = set()
    for n in names:
        if n.startswith("tools/"):
            p.add(n)
        elif re.fullmatch(r"quality/[^/]+\.py", n):
            p.add(n)
        elif re.fullmatch(r"quality/counters/[^/]+\.py", n):
            p.add(n)
    return p


def rows(ledger_text):
    return [(m.group(1), m.group(2).strip(), m.group(3)) for m in map(ROW.match, ledger_text.splitlines()) if m]


def account(pop, parsed, names, blob):
    seen = [p for p, _, _ in parsed]
    uncovered = len(pop - set(seen))
    dangling = len(set(seen) - pop)
    # rows outside the population are counted once, as dangling; their
    # description/pointer cells are not scored (control (d) expects
    # bad_pointer=0 empty_desc=0 for three non-population rows).
    live = [(p, d, t) for p, d, t in parsed if p in pop]
    empty_desc = sum(1 for _, d, _ in live if not d.strip())
    bad = 0
    for path, _, ptr in live:
        if ptr not in names or os.path.basename(path) not in blob(ptr):
            bad += 1
    return dict(population=len(pop), ledger_rows=len(parsed), uncovered=uncovered,
                dangling=dangling, bad_pointer=bad, empty_desc=empty_desc)


def line(rev, counts, selftest="ok", verdict="TARGET_MET", extra=""):
    f = "C1_R51: population={population} ledger_rows={ledger_rows} uncovered={uncovered} " \
        "dangling={dangling} bad_pointer={bad_pointer} empty_desc={empty_desc} " \
        "selftest={selftest} verdict={verdict} rev={rev}".format(
            selftest=selftest, verdict=verdict, rev=rev, **counts)
    return f + extra


def selftest():
    """Pure: 1 green + 5 mutants, no git, no writes."""
    pop = {"tools/a.py", "quality/b.py", "quality/counters/c.py"}
    ok = [("tools/a.py", "d1", "quality/README.md"), ("quality/b.py", "d2", "quality/README.md"),
          ("quality/counters/c.py", "d3", "quality/README.md")]
    files = {"quality/README.md": "tools/a.py quality/b.py quality/counters/c.py"}
    blob = lambda k: files.get(k, "")
    names = set(files) | pop
    cases = [
        ("green", ok, 0),
        ("omit", ok[:2], 1),
        ("dup", ok + [ok[0]], 1),
        ("empty", [("tools/a.py", "  ", "quality/README.md")] + ok[1:], 1),
        ("dangling", ok + [("quality/x.md", "d", "quality/README.md")], 1),
        ("badptr", [("tools/a.py", "d1", "quality/b.py")] + ok[1:], 1),
    ]
    bad = 0
    for name, rws, want in cases:
        c = account(pop, rws, names, blob)
        hit = c["uncovered"] + c["dangling"] + c["bad_pointer"] + c["empty_desc"] or (c["ledger_rows"] != c["population"])
        if bool(hit) != bool(want) and want or (want == 0 and hit):
            print("SELFTEST FAIL", name, c)
            bad += 1
    return bad


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo", required=True)
    ap.add_argument("--rev", required=True)
    ap.add_argument("--work")
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args()
    st = "ok" if selftest() == 0 else "FAIL"
    names = tree(a.repo, a.rev)
    ledger = "quality/tool-ledger.md"
    if ledger not in names:
        print(line(a.rev, dict(population=len(population(names)), ledger_rows=0, uncovered=0,
                               dangling=0, bad_pointer=0, empty_desc=0), st, "TARGET_MISSED",
                   " ledger=absent"))
        return 1
    blob = lambda p: git(a.repo, "show", "%s:%s" % (a.rev, p)) if p in names else ""
    c = account(population(names), rows(blob(ledger)), set(names), blob)
    met = st == "ok" and c["ledger_rows"] == c["population"] and not (
        c["uncovered"] or c["dangling"] or c["bad_pointer"] or c["empty_desc"])
    print(line(a.rev, c, st, "TARGET_MET" if met else "TARGET_MISSED"))
    return 0 if met else 1


if __name__ == "__main__":
    sys.exit(main())
