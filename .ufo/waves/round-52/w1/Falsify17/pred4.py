#!/usr/bin/env python3
"""Seat-local reference implementation of the four frozen round-52 C1 predicates.

Falsify17, mado round 52, wave 1. Not a lane artifact: scratch only.

Frozen predicates (registration.md, C1):
  p1 unique population   -- every population path has exactly one row
  p2 resolvable pointer  -- pointer names a file that exists at the revision
  p3 non-self pointer    -- pointer is not a self-pointer (two readings measured)
  p4 instrument context  -- description carries instrument-specific functional context

p3 readings:
  arg        self = the ledger file being scored (the natural reading once the counter
             must accept a --ledger argument, which it needs to score the control)
  canonical  self = the canonical production ledger path quality/tool-ledger.md

Usage:
  pred4.py --repo <abs repo> --rev <rev> --ledger-rel <rel path> [--checks p1,p2,p3,p4]
  pred4.py --repo <abs repo> --rev <rev> --ledger-file <abs file>
"""
import argparse
import os
import re
import subprocess
import sys

CANON = "quality/tool-ledger.md"
TOKEN = re.compile(r"[A-Za-z][A-Za-z0-9_-]{4,}")
LINE_ANCHOR = re.compile(r":\d+(?:-\d+)?$")
STOP = set("""the and for that with from this into over under only which reads read write
writes used uses using file files line lines path paths row rows cell cells does done not non
per its own all any each more less than then when where what who how are was were will shall
can may must one two three four five six seven eight nine ten""".split())
HEADER_CELLS = ("instrument", "tool", "tools", "file", "path")


class Fail(Exception):
    pass


def git(repo, *args):
    proc = subprocess.run(("git", "-C", repo) + args, capture_output=True)
    if proc.returncode != 0:
        raise Fail("git %s failed in %s: %s" % (
            " ".join(args), repo, proc.stderr.decode("utf-8", "replace")[:300]))
    return proc.stdout


def tree(repo, rev):
    out = git(repo, "ls-tree", "-r", "--name-only", rev).decode("utf-8", "surrogateescape")
    return set(p for p in out.splitlines() if p)


def population(files):
    pop = []
    for p in sorted(files):
        if "__pycache__" in p or p.endswith((".pyc", ".pyo")):
            continue
        if p.startswith("tools/"):
            pop.append(p)
            continue
        for root in ("quality/counters/", "quality/"):
            if p.startswith(root):
                rest = p[len(root):]
                if rest and "/" not in rest and rest.endswith(".py") and not rest.startswith("."):
                    pop.append(p)
                break
    return sorted(set(pop))


def parse_rows(text, columns=3):
    rows, fenced, header = [], False, False
    for lineno, raw in enumerate(text.splitlines(), 1):
        s = raw.strip()
        if s.startswith(("```", "~~~")):
            fenced = not fenced
            continue
        if fenced or not s.startswith("|"):
            continue
        cells = [c.strip() for c in s.strip("|").split("|")]
        if not header:
            header = True
            first = cells[0].strip("`*_ ").lower() if cells else ""
            if first in HEADER_CELLS:
                continue
        if cells and all(set(c) <= set("-: ") for c in cells if c):
            continue
        first = cells[0].strip("`*_ ") if cells else ""
        row = {"lineno": lineno, "cells": cells, "malformed": len(cells) != columns}
        row["path"] = first if "/" in first else None
        if columns == 4:
            # control grammar: Tool | Reads | Writes | Owner -> pointer=Reads, desc=Writes+Owner
            row["pointer"] = cells[1] if len(cells) > 1 else ""
            row["desc"] = " | ".join(cells[2:]) if len(cells) > 2 else ""
        else:
            row["desc"] = cells[1] if len(cells) > 1 else ""
            row["pointer"] = cells[2] if len(cells) > 2 else " | ".join(cells[2:])
        rows.append(row)
    return rows


def pointer_tokens(cell, prose=False):
    tokens = re.findall(r"`([^`\n]+)`", cell)
    if not tokens:
        tokens = re.split(r"[,;]|\s+", cell)
    out = []
    for token in tokens:
        token = token.strip("`*_ \t").replace(os.sep, "/")
        if prose:
            token = re.sub(r"\s*\([^)]*\)\s*$", "", token)
        token = re.sub(r"^\./", "", token)
        token = LINE_ANCHOR.sub("", token)
        if not token or token.startswith(("/", "~", "$")):
            continue
        if any(ch in token for ch in "<>():#?*\"'"):
            continue
        if "/" not in token and not re.search(r"\.(md|py|sh|json|txt|ya?ml)$", token):
            continue
        out.append(token)
    return out


def blob(repo, rev, rel):
    return git(repo, "show", "%s:%s" % (rev, rel))


def context_ok(desc, row_path, src, cache, repo, rev):
    if os.path.basename(row_path) in desc:
        return True
    want = set(t.lower() for t in TOKEN.findall(desc)) - STOP
    if not want:
        return False
    if row_path not in cache:
        try:
            cache[row_path] = blob(repo, rev, row_path).decode("utf-8", "replace")
        except Fail:
            cache[row_path] = ""
    have = set(t.lower() for t in TOKEN.findall(cache[row_path]))
    return len(want & have) >= 2


def measure(repo, rev, text, ledger_rel, ledger_src, checks, columns=3, prose=False):
    files = tree(repo, rev)
    pop = set(population(files))
    rows = parse_rows(text, columns=columns)
    cache = {}
    covered, dup, dangling, bad_pointer, self_arg, self_canon, bad_context = {}, [], [], [], [], [], []
    for row in rows:
        path = row["path"]
        if row["malformed"] or path not in pop:
            dangling.append((row["lineno"], path, row["cells"]))
        elif path in covered:
            dup.append((row["lineno"], path))
        else:
            covered[path] = row
    for path, row in sorted(covered.items()):
        tokens = pointer_tokens(row["pointer"], prose=prose)
        tokens = [t for t in tokens if t in files]
        if not tokens:
            bad_pointer.append(path)
        else:
            if ledger_src and ledger_rel in tokens:
                self_arg.append(path)
            if CANON in tokens:
                self_canon.append(path)
        if not context_ok(row["desc"], path, None, cache, repo, rev):
            bad_context.append(path)
    uncovered = sorted(pop - set(covered))
    result = {
        "population": len(pop), "rows": len(rows), "uncovered": len(uncovered),
        "dup": len(dup), "dangling": len(dangling), "bad_pointer": len(bad_pointer),
        "self_arg": len(self_arg), "self_canon": len(self_canon),
        "bad_context": len(bad_context), "malformed": sum(1 for r in rows if r["malformed"]),
    }
    detail = []
    for lineno, path, cells in dangling:
        detail.append("dangling line=%d path=%s cells=%d" % (lineno, path, len(cells)))
    for lineno, path in dup:
        detail.append("dup line=%d path=%s" % (lineno, path))
    for path in bad_pointer:
        detail.append("bad_pointer path=%s" % path)
    for path in self_arg:
        detail.append("self_arg path=%s" % path)
    for path in self_canon:
        detail.append("self_canon path=%s" % path)
    for path in bad_context:
        detail.append("bad_context path=%s" % path)
    detail.extend("uncovered path=%s" % p for p in uncovered[:5])
    ok = {
        "p1": result["uncovered"] == 0 and result["dup"] == 0 and result["dangling"] == 0
              and result["rows"] == result["population"],
        "p2": result["bad_pointer"] == 0,
        "p3": result["self_arg"] == 0,
        "p3c": result["self_canon"] == 0,
        "p4": result["bad_context"] == 0,
    }
    return result, detail, ok


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo", required=True)
    ap.add_argument("--rev", required=True)
    ap.add_argument("--ledger-rel", default=None)
    ap.add_argument("--ledger-file", default=None)
    ap.add_argument("--checks", default="p1,p2,p3,p4")
    ap.add_argument("--columns", type=int, default=3, choices=(3, 4))
    ap.add_argument("--tokenizer", default="strict", choices=("strict", "prose"))
    args = ap.parse_args(argv)
    try:
        repo = os.path.abspath(args.repo)
        files = tree(repo, args.rev)
        if args.ledger_file:
            with open(args.ledger_file, "rb") as fh:
                text = fh.read().decode("utf-8", "replace")
            ledger_rel = None
        else:
            ledger_rel = args.ledger_rel
            if ledger_rel not in files:
                print("PRED4: ledger=absent rel=%s rev=%s verdict=TARGET_MISSED" % (ledger_rel, args.rev))
                return 1
            text = blob(repo, args.rev, ledger_rel).decode("utf-8", "replace")
        result, detail, ok = measure(repo, args.rev, text, ledger_rel, True, args.checks,
                                     columns=args.columns, prose=args.tokenizer == "prose")
        wanted = [c.strip() for c in args.checks.split(",") if c.strip()]
        met = all(ok.get(c, True) for c in wanted)
        for line in detail:
            print("detail: %s" % line)
        print("PRED4: checks=%s columns=%d tokenizer=%s population=%d rows=%d uncovered=%d dup=%d dangling=%d "
              "malformed=%d bad_pointer=%d self_arg=%d self_canon=%d bad_context=%d "
              "verdict=%s ledger=%s rev=%s"
              % (",".join(wanted), args.columns, args.tokenizer, result["population"], result["rows"], result["uncovered"],
                 result["dup"], result["dangling"], result["malformed"], result["bad_pointer"],
                 result["self_arg"], result["self_canon"], result["bad_context"],
                 "TARGET_MET" if met else "TARGET_MISSED", ledger_rel or args.ledger_file,
                 args.rev))
        return 0 if met else 1
    except Fail as exc:
        print("PRED4: setup=error detail=%s" % exc, file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
