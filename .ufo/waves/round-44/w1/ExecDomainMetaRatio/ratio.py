#!/usr/bin/env python3
"""Re-runnable domain-versus-meta count over SCORECARD claim rows.

Provenance: `considerthese/2026-10-25.md:46` proposal 1 asked for the
domain-versus-meta ratio as a running number instead of prose.  This tool is
that number: it reads SCORECARD.md at a revision, classifies every claim row of
a round window, and prints the counts.

Read-only: the only external call is `git -C <repo> show <rev>:SCORECARD.md`.
stdlib only; `python3 -I` must not change the result.

== RULE (stated before the first classification; `--rule` prints it) ==

A *claim row* is a line starting with `| C<digit>` that sits under a
`## Round <N>` heading.  Its axis is the token after the claim id (`**bold**`
or bare).  The first matching clause decides the class, over the row's own
bytes at `--rev`:

  1. axis is `calibration`                                  -> meta
  2. axis is `operability` and the row carries `fixtures=` or `tool=absent`
     or `tool=present`                                      -> domain  (a tool)
  3. the claim cell names `tools/<name>.py` / `tools/<name>.sh`
                                                            -> domain  (a tool)
  4. the claim cell names `corpus/knowledge/<name>.md`      -> domain  (an entry)
  5. axis is `coverage` and (`admitted=` in the row or the claim cell contains
     the word `entry`/`entries`)                            -> domain  (an entry)
  6. the claim cell names `SKILL.md`                        -> domain  (a table)
  7. otherwise                                              -> meta    (fail-closed)

Why the *immediate object* decides, not the axis word: hold a tool or a
knowledge entry against the desktop and the ground outlives the lane; hold the
lane's counters, manifests, ledgers or admission gates against each other and
it does not.  So clause 1 outranks a named tool (a calibration row's
deliverable is the record, not the tool), while a row whose axis says
`operability` but whose object is the lane's own records (e.g. round-36 C2,
`scratch_disposition_ok`, `tip_axis_transcript`) stays meta through clause 7.

Clause 7 is fail-closed and its size is reported (`default=`) so an
unclassifiable row is visible rather than quietly counted as process.

== Usage ==

  python3 -I ratio.py --repo . --rev <rev> --from 34 --to 43
  python3 -I ratio.py --repo . --rev HEAD --from 39 --to 43 --why

Output: one `round | claim | axis | class` line per row in file order, then

  DOMAIN_META: domain=<d> meta=<m> window=<a>-<b> default=<n>

`--why` appends `| C<clause>:<reason>` to each row line; the default four
columns are unchanged.  Exit codes: 0 counted (including an empty window,
`domain=0 meta=0`), 2 bad arguments or unreadable revision, 3 a claim row in
the pre-round-34 split shape, which the rule does not score.
"""

import argparse
import re
import subprocess
import sys

ROUND_RE = re.compile(r"^##\s+Round\s+(\d+)\b")
ROW_RE = re.compile(r"^\|\s*(C\d+)\b")
AXIS_BOLD_RE = re.compile(r"\*\*([A-Za-z][A-Za-z0-9 /_-]*)\*\*")
AXIS_WORD_RE = re.compile(r"^([A-Za-z][A-Za-z0-9_-]*)")
TOOL_RE = re.compile(r"\btools/[A-Za-z0-9_.-]+\.(?:py|sh)\b")
ENTRY_RE = re.compile(r"\bcorpus/knowledge/[A-Za-z0-9._-]+\.md\b")
SKILL_RE = re.compile(r"\bSKILL\.md\b")
ENTRY_WORD_RE = re.compile(r"\bentr(?:y|ies)\b")
FIXTURES_RE = re.compile(r"\bfixtures=")
TOOLTOK_RE = re.compile(r"\btool=(?:absent|present)\b")

RULE_TEXT = """RULE (fixed before the first run; see ratio.py docstring):
 A claim row = a `| C<digit>` line under a `## Round <N>` heading.
 First matching clause over the row bytes at --rev decides:
  1. axis calibration                                        -> meta
  2. axis operability AND (fixtures= | tool=absent|present)   -> domain (tool)
  3. claim cell names tools/<name>.py|.sh                     -> domain (tool)
  4. claim cell names corpus/knowledge/<name>.md              -> domain (entry)
  5. axis coverage AND (admitted= | entry|entries in claim)   -> domain (entry)
  6. claim cell names SKILL.md                                -> domain (table)
  7. otherwise                                                -> meta (fail-closed)
 The immediate object decides, not the axis word: a tool or entry held against
 the desktop outlives the lane; counters, manifests, ledgers and gates do not.
"""


def read_scorecard(repo, rev):
    """Return SCORECARD.md text at rev, read-only."""
    proc = subprocess.run(
        ["git", "-C", repo, "show", "%s:SCORECARD.md" % rev],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    if proc.returncode != 0:
        sys.stderr.write(
            "ratio: cannot read %s:SCORECARD.md at %s: %s\n"
            % (repo, rev, proc.stderr.decode("utf-8", "replace").strip())
        )
        raise SystemExit(2)
    return proc.stdout.decode("utf-8", "replace")


class OutOfScope(Exception):
    pass


def split_row(line, lineno):
    """Return (claim_id, axis, claim_cell) for a merged-shape claim row.

    Scope: rounds 34+ write `| C1 **coverage** - ... | test | ... |`, so the
    claim id, axis word and claim text share the first cell.  Rounds 12-33
    write `| C1 | calibration / ... | ... |`, where the axis and claim sit in a
    second cell; that shape is outside the rule's validation and is refused
    loudly instead of being silently scored meta.
    """
    cells = line.strip().strip("|").split("|")
    first = cells[0].strip()
    claim_id = ROW_RE.match(line).group(1)
    rest = first[len(claim_id):].strip()
    if not rest:
        raise OutOfScope(
            "SCORECARD.md:%d: split-shape claim row `%s` (rounds 12-33) is "
            "outside the rule's scope; the rule is stated and validated for "
            "the merged shape used from round 34 on" % (lineno, first)
        )
    claim_cell = first
    bold = AXIS_BOLD_RE.search(rest)
    if bold:
        axis = bold.group(1).strip().split()[0]
    else:
        word = AXIS_WORD_RE.match(rest)
        axis = word.group(1) if word else ""
    return claim_id, axis.lower(), claim_cell


def classify(axis, claim_cell, row):
    """Return (class, clause, reason) under the RULE above."""
    if axis == "calibration":
        return "meta", 1, "axis calibration"
    if axis == "operability" and (FIXTURES_RE.search(row) or TOOLTOK_RE.search(row)):
        return "domain", 2, "operability on fixtures/tool presence"
    tool = TOOL_RE.search(claim_cell)
    if tool:
        return "domain", 3, "names %s" % tool.group(0)
    entry = ENTRY_RE.search(claim_cell)
    if entry:
        return "domain", 4, "names %s" % entry.group(0)
    if axis == "coverage" and (
        "admitted=" in row or ENTRY_WORD_RE.search(claim_cell)
    ):
        return "domain", 5, "coverage admitting an entry"
    if SKILL_RE.search(claim_cell):
        return "domain", 6, "names SKILL.md"
    return "meta", 7, "fail-closed: no desktop deliverable named"


def collect(text, lo, hi):
    rows = []
    current = None
    for lineno, line in enumerate(text.splitlines(), 1):
        head = ROUND_RE.match(line)
        if head:
            current = int(head.group(1))
            continue
        if current is None or not ROW_RE.match(line):
            continue
        if not (lo <= current <= hi):
            continue
        claim_id, axis, claim_cell = split_row(line, lineno)
        cls, clause, reason = classify(axis, claim_cell, line)
        rows.append((current, claim_id, axis, cls, clause, reason))
    return rows


def main(argv):
    if "--rule" in argv:
        sys.stdout.write(RULE_TEXT)
        return 0

    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--repo", required=True)
    ap.add_argument("--rev", required=True)
    ap.add_argument("--from", dest="lo", type=int, required=True)
    ap.add_argument("--to", dest="hi", type=int, required=True)
    ap.add_argument("--why", action="store_true",
                    help="append `| C<clause>:<reason>` to each row line")
    ap.add_argument("--rule", action="store_true", help="print the rule and exit")
    args = ap.parse_args(argv)

    if args.lo > args.hi:
        sys.stderr.write("ratio: --from %d > --to %d\n" % (args.lo, args.hi))
        return 2

    try:
        rows = collect(read_scorecard(args.repo, args.rev), args.lo, args.hi)
    except OutOfScope as exc:
        sys.stderr.write("ratio: %s\n" % exc)
        return 3
    domain = meta = default = 0
    for rnd, claim_id, axis, cls, clause, reason in rows:
        if cls == "domain":
            domain += 1
        else:
            meta += 1
        if clause == 7:
            default += 1
        line = "%d | %s | %s | %s" % (rnd, claim_id, axis or "-", cls)
        if args.why:
            line += " | C%d:%s" % (clause, reason)
        sys.stdout.write(line + "\n")
    sys.stdout.write(
        "DOMAIN_META: domain=%d meta=%d window=%d-%d default=%d\n"
        % (domain, meta, args.lo, args.hi, default)
    )
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
