#!/usr/bin/env python3
"""Naive C1-style counter for the Falsify28 isolation attack.

Implements every check named in the frozen C1 predicate
(registration.md line 7): population row uniqueness, resolvable evidence
pointer, non-self pointer, instrument-specific functional context.
Deliberately resolves evidence pointers against the FILESYSTEM
(repo working tree first, then the invocation cwd) instead of the
pinned revision's tree, to demonstrate that the frozen predicate does
not require pinned-revision isolation and that green/red receipts
cannot tell this counter apart from an isolated one.
"""
import argparse
import os
import re
import subprocess
import sys

LEDGER_REL = "quality/tool-ledger.md"
FUNC_WORDS = ("verif", "dispatch", "rout", "check", "test", "valid", "track",
              "count", "measur", "audit", "gate")


def population(repo, rev):
    """Population from the PINNED REVISION tree (git ls-tree), as the base
    counter does — only pointer resolution below is left filesystem-based."""
    proc = subprocess.run(["git", "-C", repo, "ls-tree", "-r", "--name-only",
                           rev], capture_output=True)
    if proc.returncode != 0:
        raise SystemExit("NAIVE_C1: setup=error git ls-tree failed: %s"
                         % proc.stderr.decode("utf-8", "replace"))
    pop = []
    for rel in proc.stdout.decode("utf-8", "surrogateescape").splitlines():
        if rel.startswith("tools/"):
            pop.append(rel)
    return sorted(set(pop))


def parse_rows(text):
    rows = []
    fenced = False
    for raw in text.splitlines():
        line = raw.strip()
        if line.startswith(("```", "~~~")):
            fenced = not fenced
            continue
        if fenced or not line.startswith("|"):
            continue
        cells = [c.strip() for c in line.strip("|").split("|")]
        first = cells[0].strip("`*_ \t") if cells else ""
        if not first or "/" not in first or first.startswith(":") \
                or set(first) <= set("-: "):
            continue
        rows.append({
            "path": first,
            "desc": cells[1] if len(cells) > 1 else "",
            "pointer": " | ".join(cells[2:]) if len(cells) > 2 else "",
        })
    return rows


def pointer_tokens(cell):
    tokens = re.findall(r"`([^`\n]+)`", cell)
    if not tokens:
        tokens = re.split(r"[,;]|\s+", cell)
    out = []
    for token in tokens:
        token = token.strip("`*_")
        token = re.sub(r"^\./", "", token)
        token = re.sub(r":\d+(?:-\d+)?$", "", token)
        if not token or token.startswith(("/", "~", "$")):
            continue
        if "/" not in token:
            continue
        out.append(token)
    return out


def resolves(repo, token):
    """Filesystem resolution: repo working tree, then invocation cwd."""
    cand = os.path.join(repo, token)
    if os.path.isfile(cand):
        return True
    return os.path.isfile(token)  # cwd-relative: scratch contamination vector


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo", default=".")
    ap.add_argument("--rev", required=True)
    ap.add_argument("--ledger", default=LEDGER_REL)
    ap.add_argument("--work", default=None, help="accepted for CLI parity; unused")
    args = ap.parse_args(argv)

    repo = os.path.abspath(args.repo)
    if not os.path.isdir(os.path.join(repo, ".git")):
        print("NAIVE_C1: setup=error detail=not a git repo", file=sys.stderr)
        return 2

    ledger_path = os.path.join(repo, args.ledger)
    if not os.path.isfile(ledger_path):
        print("NAIVE_C1: verdict=TARGET_MISSED ledger=absent rev=%s" % args.rev)
        return 1
    rows = parse_rows(open(ledger_path, encoding="utf-8").read())
    pop = set(population(repo, args.rev))

    dup = bad = selfp = context = dangling = 0
    seen = set()
    details = []
    for row in rows:
        path = row["path"]
        if path not in pop:
            dangling += 1
            details.append("dangling path=%s" % path)
            continue
        if path in seen:
            dup += 1
            details.append("dup path=%s" % path)
            continue
        seen.add(path)
        base = os.path.basename(path)
        desc = row["desc"].strip("`*_ \t")
        toks = pointer_tokens(row["pointer"])
        if not any(resolves(repo, t) for t in toks):
            bad += 1
            details.append("bad_pointer path=%s" % path)
        if any(os.path.normpath(t) == os.path.normpath(args.ledger) for t in toks):
            selfp += 1
            details.append("self_pointer path=%s" % path)
        has_ctx = (base in desc) or (any(w in desc.lower() for w in FUNC_WORDS)
                                     and base.split(".")[0].split("-")[0] in desc)
        if not has_ctx:
            context += 1
            details.append("context path=%s" % path)

    for line in details:
        print("detail: %s" % line)
    clean = (len(pop) > 0 and not any((dangling, dup, bad, selfp, context)))
    print("NAIVE_C1: population=%d ledger_rows=%d dup=%d bad_pointer=%d "
          "self_pointer=%d context=%d verdict=%s rev=%s"
          % (len(pop), len(rows), dup, bad, selfp, context,
             "TARGET_MET" if clean else "TARGET_MISSED", args.rev))
    return 0 if clean else 1


if __name__ == "__main__":
    sys.exit(main())
