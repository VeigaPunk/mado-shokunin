#!/usr/bin/env python3
"""c1-r52-ledger.py -- C1Simplify reference: simplest legitimate C1-r52 accountability check.

Draft only (seat C1Simplify, mado round 52). Not the scored artifact; a minimum-size
reference for the frozen C1 predicate: unique complete population, non-self resolvable
evidence pointers, and a bounded instrument-context signal on the description.

Reads committed bytes with `git show`/`git ls-tree` only: no clone, no subprocess, no
scratch directory, no writes anywhere. The ledger defaults to `quality/tool-ledger.md`
at --rev; --ledger names a filesystem file instead (the red control).

Fields
  population    files at --rev under tools/ + quality/*.py + quality/counters/*.py
                (__pycache__, *.pyc, *.pyo excluded); P
  ledger_rows   parsed 3-cell rows (fenced blocks skipped -- the ledger's own grammar
                example is fenced); R
  uncovered     population paths with no row
  dup           repeated row path
  dangling      row path not in population, or a row that is not exactly 3 cells
  bad_pointer   pointer cell is not exactly one backticked repo path that exists at
                --rev and whose bytes contain the row file's basename
  self_pointer  pointer resolves but names the row's own path or the ledger itself
  generic_desc  description empty/placeholder, shared verbatim with another row, or sharing
                no 2-word phrase with the instrument's own bytes (a word-count floor was
                measured as non-load-bearing and left out)

Exit: 0 TARGET_MET, 1 TARGET_MISSED, 2 setup error.
"""
import argparse
import os
import re
import subprocess
import sys

LEDGER_REL = "quality/tool-ledger.md"
PLACEHOLDER = re.compile(r"^[\s\-–—_*`.?]+$")
EMPHASIS = "`*_ \t"
POINTER_TOKEN = re.compile(r"^`([^`]+)`$")
LINE_ANCHOR = re.compile(r":\d+(?:-\d+)?$")


class SetupError(Exception):
    pass


def git(repo, *args):
    proc = subprocess.run(("git", "-C", repo) + args, capture_output=True)
    if proc.returncode != 0:
        raise SetupError("git %s failed: %s" % (
            " ".join(args), proc.stderr.decode("utf-8", "replace").strip()[:300]))
    return proc.stdout


def population(files):
    pop = []
    for path in files:
        if "__pycache__" in path or path.endswith((".pyc", ".pyo")):
            continue
        if path.startswith("tools/"):
            pop.append(path)
        elif path.startswith("quality/counters/"):
            rest = path[len("quality/counters/"):]
            if rest and "/" not in rest and rest.endswith(".py") and not rest.startswith("."):
                pop.append(path)
        elif path.startswith("quality/"):
            rest = path[len("quality/"):]
            if rest and "/" not in rest and rest.endswith(".py") and not rest.startswith("."):
                pop.append(path)
    return sorted(set(pop))


def rows_of(text):
    rows, fenced = [], False
    for raw in text.splitlines():
        line = raw.strip()
        if line.startswith(("```", "~~~")):
            fenced = not fenced
            continue
        if fenced or not line.startswith("|"):
            continue
        cells = [c.strip() for c in line.strip("|").split("|")]
        first = cells[0].strip(EMPHASIS) if cells else ""
        if not first or "/" not in first or first.startswith(":") or set(first) <= set("-: "):
            continue
        rows.append({"path": first, "cells": cells,
                     "desc": cells[1] if len(cells) > 1 else "",
                     "pointer": cells[2] if len(cells) > 2 else ""})
    return rows


def norm(s):
    return " " + re.sub(r"[^a-z0-9]+", " ", s.lower()).strip() + " "


def describe(pop, rows, ledger_rel, listing, blobs):
    counts = dict(uncovered=0, dup=0, dangling=0, bad_pointer=0, self_pointer=0,
                  generic_desc=0)
    details, seen, descs = [], set(), {}
    in_pop = set(pop)
    for row in rows:
        path = row["path"]
        if len(row["cells"]) != 3 or path not in in_pop:
            counts["dangling"] += 1
            details.append("dangling path=%s cells=%d" % (path, len(row["cells"])))
            continue
        if path in seen:
            counts["dup"] += 1
            details.append("dup path=%s" % path)
            continue
        seen.add(path)
        match = POINTER_TOKEN.match(row["pointer"].strip())
        target = LINE_ANCHOR.sub("", match.group(1).strip()) if match else ""
        if not target or target not in listing:
            counts["bad_pointer"] += 1
            details.append("bad_pointer path=%s pointer=%r" % (path, row["pointer"][:80]))
        elif target in (path, LEDGER_REL) or target == ledger_rel:
            counts["self_pointer"] += 1
            details.append("self_pointer path=%s target=%s" % (path, target))
        elif os.path.basename(path).encode() not in blobs(target):
            counts["bad_pointer"] += 1
            details.append("bad_pointer path=%s target=%s basename-absent" % (path, target))
        desc = row["desc"].strip(EMPHASIS)
        words = norm(desc).split()
        reason = None
        if not desc or PLACEHOLDER.match(desc):
            reason = "empty"
        elif desc in descs:
            reason = "repeat-of:%s" % descs[desc]
        else:
            body = norm(blobs(path).decode("utf-8", "replace"))
            text = " " + " ".join(words) + " "
            if not any(" %s " % " ".join(words[i:i + 2]) in body
                       for i in range(len(words) - 1)):
                reason = "unbound"
        if reason:
            counts["generic_desc"] += 1
            details.append("generic_desc path=%s reason=%s" % (path, reason))
        descs.setdefault(desc, path)
    counts["uncovered"] = len(in_pop - seen)
    details.extend("uncovered path=%s" % p for p in sorted(in_pop - seen))
    return counts, details


def main(argv=None):
    ap = argparse.ArgumentParser(description="C1Simplify reference: C1-r52 ledger accountability")
    ap.add_argument("--repo", default=".")
    ap.add_argument("--rev", required=True)
    ap.add_argument("--ledger", default=None)
    ap.add_argument("--work", default=None,
                    help="accepted for harness compatibility; this counter writes nothing")
    args = ap.parse_args(argv)
    try:
        repo = os.path.abspath(args.repo)
        rev = git(repo, "rev-parse", "--verify", "--quiet", args.rev + "^{commit}").decode().strip()
        listing = {p for p in git(repo, "ls-tree", "-r", "--name-only", rev).decode(
            "utf-8", "surrogateescape").splitlines() if p}
        pop = population(listing)
        cache = {}

        def blobs(rel):
            if rel not in cache:
                cache[rel] = git(repo, "show", "%s:%s" % (rev, rel))
            return cache[rel]

        if args.ledger:
            ledger_rel = None
            with open(args.ledger, "rb") as fh:
                text = fh.read().decode("utf-8", "replace")
        else:
            ledger_rel = LEDGER_REL
            if ledger_rel not in listing:
                print("LEDGER52: verdict=TARGET_MISSED ledger=absent population=%d rev=%s"
                      % (len(pop), rev))
                return 1
            text = blobs(ledger_rel).decode("utf-8", "replace")
        rows = rows_of(text)
        counts, details = describe(pop, rows, ledger_rel, listing, blobs)
        for line in details:
            print("detail: %s" % line)
        met = (len(pop) > 0 and len(rows) == len(pop)
               and not any(counts.values()))
        print("LEDGER52: population=%d ledger_rows=%d uncovered=%d dup=%d dangling=%d "
              "bad_pointer=%d self_pointer=%d generic_desc=%d verdict=%s rev=%s" % (
                  len(pop), len(rows), counts["uncovered"], counts["dup"], counts["dangling"],
                  counts["bad_pointer"], counts["self_pointer"], counts["generic_desc"],
                  "TARGET_MET" if met else "TARGET_MISSED", rev))
        return 0 if met else 1
    except (SetupError, OSError) as exc:
        print("LEDGER52: setup=error detail=%s" % exc, file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
