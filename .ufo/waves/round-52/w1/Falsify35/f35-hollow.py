#!/usr/bin/env python3
"""f35-hollow.py -- SEAT-LOCAL falsification instrument for round-52 C1.

Not the round-52 claimed counter (that counter does not exist at the frozen base).
This instrument exists only to test whether the frozen demonstration requirement
("production pass and control fail at the frozen revision") discriminates the
three predicate families named in claims-frozen.md:

  unique population | non-self resolvable evidence targets | instrument-specific context

Modes:
  count     -- parse the committed 3-cell ledger grammar and require >= MIN_ROWS rows.
               Implements NONE of the three claimed predicates.
  unique    -- count + row-path uniqueness. Implements only "unique population".
  semantic  -- count + uniqueness + population membership + pointer resolution +
               non-self, with the instrument-specific context check STUBBED to True.
               Implements at most two of the three claimed predicates.

Reads a plain directory tree (a `git archive` snapshot of a pinned revision).
"""

import argparse
import os
import re
import sys

HEADER_CELLS = frozenset({"path", "file", "instrument", "tool", "artifact"})
SEPARATOR = re.compile(r"^:?-{3,}:?$")
LINE_SUFFIX = re.compile(r":(?:\d+)(?:-\d+)?$")
BACKTICK = re.compile(r"`([^`\n]+)`")
PATHISH = re.compile(r"^[A-Za-z0-9._-]+(?:/[A-Za-z0-9._#-]+)+$")
QUALITY_PY = re.compile(r"^quality/[^/]+\.py$")
COUNTERS_PY = re.compile(r"^quality/counters/[^/]+\.py$")
MIN_ROWS = 10


def population(root):
    pop = []
    for dirpath, _dirnames, filenames in os.walk(root):
        rel = os.path.relpath(dirpath, root)
        rel = "" if rel == "." else rel.replace(os.sep, "/")
        for name in filenames:
            path = name if not rel else rel + "/" + name
            if path.startswith("tools/"):
                pop.append(path)
            elif QUALITY_PY.match(path) or COUNTERS_PY.match(path):
                pop.append(path)
    return sorted(set(pop))


def unfenced(text):
    out, fenced = [], False
    for line in text.splitlines():
        if line.lstrip().startswith(("```", "~~~")):
            fenced = not fenced
            continue
        if not fenced:
            out.append(line)
    return out


def clean(cell):
    return cell.replace("`", "").replace("**", "").strip()


def parse_rows(text):
    rows, malformed, seen = [], [], False
    for lineno, line in enumerate(unfenced(text), 1):
        stripped = line.strip()
        if not stripped.startswith("|"):
            continue
        cells = stripped.strip("|").split("|")
        if not seen and cells and clean(cells[0]).lower() in HEADER_CELLS:
            seen = True
            continue
        seen = True
        if cells and all(SEPARATOR.match(c.strip()) for c in cells if c.strip()):
            continue
        if len(cells) != 3:
            malformed.append((lineno, len(cells)))
            continue
        rows.append((lineno, cells[0], cells[1], cells[2]))
    return rows, malformed


def pointer_tokens(cell):
    tokens = [t.strip() for t in BACKTICK.findall(cell)]
    if not tokens:
        tokens = [w for w in cell.split() if PATHISH.match(w.strip(".,;:"))]
    out = []
    for tok in tokens:
        tok = LINE_SUFFIX.sub("", tok.strip())
        tok = tok.replace("`", "").strip()
        if tok and tok not in out:
            out.append(tok)
    return out


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", required=True)
    ap.add_argument("--ledger", required=True, help="repo-relative ledger path")
    ap.add_argument("--mode", choices=("count", "unique", "semantic"), default="semantic")
    ap.add_argument("--self", dest="self_path", default=None,
                    help="path considered 'self' (default: --ledger value)")
    args = ap.parse_args(argv)

    ledger_abs = os.path.join(args.root, args.ledger)
    self_path = args.self_path if args.self_path is not None else args.ledger
    pop = population(args.root)
    if not os.path.isfile(ledger_abs):
        print("F35: ledger missing: %s" % args.ledger)
        return 2
    with open(ledger_abs, "rb") as fh:
        text = fh.read().decode("utf-8", "replace")

    rows, malformed = parse_rows(text)
    seen, dup = {}, 0
    for lineno, cell, _desc, _ptr in rows:
        path = clean(cell)
        if path in seen:
            dup += 1
        else:
            seen[path] = (lineno, _desc, _ptr)
    uncovered = [p for p in pop if p not in seen]
    bad_ptr = 0
    nonself = 0
    for path, (_lineno, _desc, ptr) in seen.items():
        toks = pointer_tokens(ptr)
        if not toks or any(not os.path.isfile(os.path.join(args.root, t)) for t in toks):
            bad_ptr += 1
            continue
        if self_path in toks:
            nonself += 1

    context = "stub-ok"  # the instrument-specific context check is deliberately absent

    if args.mode == "count":
        ok = len(rows) >= MIN_ROWS
        detail = "rows=%d malformed=%d" % (len(rows), len(malformed))
    elif args.mode == "unique":
        ok = len(rows) >= MIN_ROWS and dup == 0 and not malformed
        detail = "rows=%d malformed=%d dup=%d" % (len(rows), len(malformed), dup)
    else:
        ok = (len(rows) >= MIN_ROWS and dup == 0 and not malformed
              and not uncovered and bad_ptr == 0 and nonself == 0)
        detail = ("rows=%d malformed=%d dup=%d uncovered=%d bad_pointer=%d "
                  "nonself=%d context=%s" % (len(rows), len(malformed), dup,
                                             len(uncovered), bad_ptr, nonself, context))

    print("F35: mode=%s ledger=%s self=%s population=%d %s verdict=%s"
          % (args.mode, args.ledger, self_path, len(pop), detail,
             "PASS" if ok else "FAIL"))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
