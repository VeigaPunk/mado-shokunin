#!/usr/bin/env python3
"""Build the C1 control fixture repository (mado r51 w1, seat ExecControlsC1).

Fixture lives entirely under the caller-provided scratch dir. It is a fresh
`git init` sandbox holding only the base-revision population files plus fixture
support files; the lane repository is read with `git show` and never written.
Toplevel is asserted before every commit.
"""

import argparse
import os
import subprocess
import sys

POP_RE = None


def git(repo, *args, check=True):
    r = subprocess.run(["git", "-C", repo] + list(args),
                       capture_output=True, check=False)
    if check and r.returncode != 0:
        sys.exit("git %s failed: %s" % (" ".join(args),
                                        r.stderr.decode("utf-8", "replace")))
    return r


def population(lane, base):
    r = git(lane, "ls-tree", "-r", "--name-only", base)
    out = []
    for p in r.stdout.decode().splitlines():
        if p.startswith("tools/"):
            out.append(p)
        elif p.startswith("quality/counters/"):
            rest = p[len("quality/counters/"):]
            if rest and "/" not in rest and rest.endswith(".py"):
                out.append(p)
        elif p.startswith("quality/"):
            rest = p[len("quality/"):]
            if rest and "/" not in rest and rest.endswith(".py"):
                out.append(p)
    return sorted(out)


def ledger_text(rows):
    out = ["# Tool ledger (fixture)", "",
           "| file | description | accountability |", "|---|---|---|"]
    for path, desc, ptr in rows:
        out.append("| `%s` | %s | `%s` |" % (path, desc, ptr))
    return "\n".join(out) + "\n"


def commit(repo, fixture, msg):
    top = git(repo, "rev-parse", "--show-toplevel").stdout.decode().strip()
    if os.path.realpath(top) != os.path.realpath(fixture):
        sys.exit("toplevel mismatch: %r != %r" % (top, fixture))
    git(repo, "add", "-A")
    git(repo, "commit", "-q", "-m", msg)
    return git(repo, "rev-parse", "HEAD").stdout.decode().strip()


def checkout_ledger(repo, rev):
    git(repo, "checkout", "-q", rev, "--", "quality/tool-ledger.md")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--lane", required=True)
    ap.add_argument("--base", required=True)
    ap.add_argument("--fixture", required=True)
    ap.add_argument("--newest", nargs=5, required=True)
    ns = ap.parse_args()

    fixture = os.path.abspath(ns.fixture)
    os.makedirs(fixture, exist_ok=True)
    git(fixture, "init", "-q")
    git(fixture, "config", "user.email", "control@fixture.local")
    git(fixture, "config", "user.name", "ExecControlsC1")

    pop = population(ns.lane, ns.base)
    acct = []
    for p in pop:
        dst = os.path.join(fixture, p)
        os.makedirs(os.path.dirname(dst), exist_ok=True)
        body = git(ns.lane, "show", "%s:%s" % (ns.base, p)).stdout
        with open(dst, "wb") as fh:
            fh.write(body)
        acct.append("- %s" % os.path.basename(p))

    with open(os.path.join(fixture, "ACCOUNT.md"), "w") as fh:
        fh.write("# Accountability index\n\n" + "\n".join(acct) + "\n")
    with open(os.path.join(fixture, "DECOY.md"), "w") as fh:
        fh.write("# Decoy accountability file\n\n"
                 "This file names no instrument; it exists so that a pointer\n"
                 "can resolve to a real file whose bytes do not contain the\n"
                 "row's basename. Five lines, none of them a basename.\n")
    with open(os.path.join(fixture, "EXTRA-DECOY.md"), "w") as fh:
        fh.write("# Extra decoy\n\n"
                 "quality/not-a-tool-1.txt\nquality/not-a-tool-2.txt\n"
                 "quality/not-a-tool-3.txt\n")

    base_rev = commit(fixture, fixture, "fixture: base population, no ledger")

    base_names = [os.path.basename(p) for p in pop]
    rows = [(p, "does %s" % os.path.basename(p), "ACCOUNT.md:%d" % (i + 1))
            for i, p in enumerate(pop)]
    os.makedirs(os.path.join(fixture, "quality"), exist_ok=True)
    with open(os.path.join(fixture, "quality", "tool-ledger.md"), "w") as fh:
        fh.write(ledger_text(rows))
    green = commit(fixture, fixture, "fixture: green ledger (r51-control)")
    git(fixture, "tag", "-f", "r51-control", green)

    newest = set(os.path.basename(x) for x in ns.newest)
    missing = sorted(newest - set(base_names))
    if missing:
        sys.exit("newest tools not in base population: %r" % missing)

    # (a) omit tools/mado-keysym.py
    git(fixture, "checkout", "-q", "-B", "mut-a", green)
    rows_a = [r for r in rows if r[0] != "tools/mado-keysym.py"]
    with open(os.path.join(fixture, "quality", "tool-ledger.md"), "w") as fh:
        fh.write(ledger_text(rows_a))
    rev_a = commit(fixture, fixture, "mutant a: ledger omits tools/mado-keysym.py")

    # (b) wrong pointers for the five newest tools
    git(fixture, "checkout", "-q", "-B", "mut-b", green)
    rows_b = [(p, d, "DECOY.md:1" if os.path.basename(p) in newest else ptr)
              for p, d, ptr in rows]
    with open(os.path.join(fixture, "quality", "tool-ledger.md"), "w") as fh:
        fh.write(ledger_text(rows_b))
    rev_b = commit(fixture, fixture, "mutant b: newest five point at a decoy file")

    # (c) empty descriptions for every quality/counters/*.py row
    git(fixture, "checkout", "-q", "-B", "mut-c", green)
    counters = [p for p in pop if p.startswith("quality/counters/")]
    rows_c = [(p, "" if p in counters else d, ptr) for p, d, ptr in rows]
    with open(os.path.join(fixture, "quality", "tool-ledger.md"), "w") as fh:
        fh.write(ledger_text(rows_c))
    rev_c = commit(fixture, fixture, "mutant c: empty descriptions for counters")

    # (d) three rows outside the population
    git(fixture, "checkout", "-q", "-B", "mut-d", green)
    rows_d = rows + [("quality/not-a-tool-%d.txt" % i,
                      "ghost row outside population", "EXTRA-DECOY.md:%d" % i)
                     for i in (1, 2, 3)]
    with open(os.path.join(fixture, "quality", "tool-ledger.md"), "w") as fh:
        fh.write(ledger_text(rows_d))
    rev_d = commit(fixture, fixture, "mutant d: three non-population rows")

    git(fixture, "checkout", "-q", green)
    print("fixture=%s" % fixture)
    print("base_population=%d" % len(pop))
    print("counter_py=%d" % len(counters))
    print("newest=%s" % ",".join(ns.newest))
    print("rev_fixture_base=%s" % base_rev)
    print("rev_r51_control=%s" % green)
    print("rev_mut_a=%s" % rev_a)
    print("rev_mut_b=%s" % rev_b)
    print("rev_mut_c=%s" % rev_c)
    print("rev_mut_d=%s" % rev_d)
    print("P=%d" % len(pop))


if __name__ == "__main__":
    main()
