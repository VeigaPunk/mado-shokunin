#!/usr/bin/env python3
"""Falsify44 harness: attack the C1 evidence/self-pointer rule using source
bytes of the committed r51 counter against the round-52 do-nothing control
and a pathological variant. Read-only; writes nothing.
"""
import importlib.util
import os
import subprocess

LANE = "/home/vgpnk/Projects/shokunin/mado-shokunin"
COUNTER = os.path.join(LANE, "quality", "counters", "c1-r51-ledger.py")
FIXTURE = "/fast/scratch/hyaku/mado-r52/Falsify44/fixture"
LEDGER_REL = "quality/tool-ledger.md"

spec = importlib.util.spec_from_file_location("c1r51", COUNTER)
c1 = importlib.util.module_from_spec(spec)
spec.loader.exec_module(c1)


def git(repo, *args):
    return subprocess.run(("git", "-C", repo) + args, capture_output=True,
                          check=True).stdout


rev = git(FIXTURE, "rev-parse", "HEAD").decode().strip()
files = set(p for p in git(FIXTURE, "ls-tree", "-r", "--name-only", rev)
            .decode("utf-8", "surrogateescape").splitlines() if p)
ledger = git(FIXTURE, "show", "%s:%s" % (rev, LEDGER_REL)).decode("utf-8", "replace")
rows = c1.parse_rows(ledger)
cache = {}

print("=== A. frozen control bytes vs committed r51 counter functions ===")
print("fixture rev=%s files=%s" % (rev[:12], sorted(files)))
for i, row in enumerate(rows):
    ok = c1.pointer_resolves(FIXTURE, rev, files, row["path"], row["pointer"], cache)
    print("row%d path=%s" % (i, row["path"]))
    print("  desc cell  = %r" % row["desc"])
    print("  pointer cell = %r" % row["pointer"])
    print("  pointer_tokens(pointer cell) = %s" % c1.pointer_tokens(row["pointer"]))
    print("  committed pointer_resolves -> %s" % ok)
    toks_all = c1.pointer_tokens(row["desc"] + " " + row["pointer"])
    print("  tokens(desc+pointer) = %s" % toks_all)
    for t in toks_all:
        if t in files:
            content = git(FIXTURE, "show", "%s:%s" % (rev, t)).decode("utf-8", "replace")
            print("  token %s -> basename %s in bytes: %s"
                  % (t, os.path.basename(row["path"]), os.path.basename(row["path"]) in content))
print()

print("=== B. pathological variant: pointer cell names the ledger itself ===")
print("(same row grammar, self-pointer moved into the pointer cell;")
print(" instrument basename is present in the ledger bytes because the row names it)")
for row in rows:
    fake_pointer = "`%s`" % LEDGER_REL
    ok = c1.pointer_resolves(FIXTURE, rev, files, row["path"], fake_pointer, cache)
    print("path=%s pointer=%s" % (row["path"], fake_pointer))
    print("  committed pointer_resolves -> %s" % ok)
    naive_pass = LEDGER_REL != row["path"]        # pointer vs row instrument path
    corrected_pass = LEDGER_REL != LEDGER_REL     # pointer vs the ledger itself
    print("  non-self clause PASS under naive def  (pointer != row-path)   -> %s" % naive_pass)
    print("  non-self clause PASS under ledger def (pointer != LEDGER_REL) -> %s" % corrected_pass)
print()

print("=== C. clause definitions that make the frozen control fail for the")
print("    named defects (self-pointer / context), evaluated on real control bytes ===")
for i, row in enumerate(rows):
    desc = row["desc"].strip(c1.EMPHASIS)
    base = os.path.basename(row["path"])
    row_paths = [t for t in c1.pointer_tokens(row["desc"] + " " + row["pointer"]) if t in files]
    self_ref = LEDGER_REL in row_paths
    context_specific = (base in desc) or ("verify" in desc.lower() and "mado" in desc.lower())
    print("row%d: path-like tokens in row -> %s" % (i, row_paths))
    print("  self-pointer defect present (row references ledger itself): %s" % self_ref)
    print("  context defect present (desc lacks instrument-specific function): %s"
          % (not context_specific))
    print("  desc=%r" % desc)
