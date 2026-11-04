#!/usr/bin/env python3
"""c1-r67-register.py — PRED-C1-r67: register citation-to-live-object discrimination.

Draft for `quality/counters/c1-r67-register.py` (mado round-67, w1 seat
R67ExecRegister). The frozen predicate is claim C1 of
`.ufo/waves/round-67/claims-declaration-r67.md`, restated here as the fields the
counter actually measures:

``heading``   exactly one line of PROVINCE.md at ``--rev`` starts
              ``### Surface state register (2026-11-03``; a second such line is a
              duplicate-heading rejection, zero such lines a missing-heading rejection.
``rows``      the lines of the register block that start ``|`` (exact left edge), split on
              ``|``; markdown separator rows and the header row (the pipe row immediately
              followed by a separator row) are not data rows. Exactly eight data rows, and
              each of the eight frozen group names stands alone in exactly one first cell
              (exact equality; ``hypr plane (…)`` does not match ``hypr plane``).
``receipt``   the FOURTH cell of every data row must name at least one receipt token that
              resolves at ``--rev``, and no receipt token named in a FOURTH cell may dangle
              (the r66 rule, retained: a live pointer beside an unresolved pointer is a
              forgery shape, not a pass). A receipt token is a whitespace-separated token matching
              ``^\\.ufo/waves/round-[0-9]+/receipts/[^ |,)]+\\.(txt|json|md|sh)$`` after one
              markdown wrapper/bracket/quote run is stripped from each end (so backticked and
              bare pointers in a table are both seen). Resolution is a successful
              ``git show <rev>:<path>`` read; the worktree is never opened.
``live-cited`` the frozen live path must appear as a receipt token inside some row's FOURTH
              cell. A mention in a state cell, a probe cell, the heading, or prose elsewhere
              does not count: this is the discrimination the superseded r66 counter lacked.
``live-line`` the object at the frozen live path, read at ``--rev``, must contain the exact
              CLEAN line below as a whole line. The line was copied from committed bytes
              (``git -C <lane> show 061dc329:.ufo/waves/round-65/receipts/gate-live-r65.txt``),
              never from memory or from the file-plane receipt.

``--controls PATH`` scores the frozen six-case JSON: one ``C1_R67 case=`` line per case
(``verdict`` = the counter's accept/reject, ``correct`` = verdict equals the case's frozen
``expect``) and the real register at ``--rev``. A case is scored against its embedded
``province`` text and ``objects`` map, so the controls never touch the lane.

Exit: 0 iff register=accept AND controls=6/6; 1 otherwise; 2 setup/usage error. stdout is the
per-case lines (controls mode) plus exactly one
``MADO_R67_REGISTER: register=… controls=<n>/6 headings=… rows=… groups=…/8 live-cited=… verdict=… rev=…``
line. Miss diagnostics go to stderr as ``C1_R67: detail=…`` lines.

Reads: git objects at ``--rev`` only. Every ``GIT_*`` variable is scrubbed from the child
environment and ``GIT_OPTIONAL_LOCKS=0`` and ``GIT_NO_REPLACE_OBJECTS=1`` are set, so a planted
``refs/replace`` ref cannot rewrite the bytes measured. No worktree file, no host probe, no
network, no scratch write. ``--scratch-root`` is accepted for interface parity with the frozen
claim text and is unused.

``--selftest`` is hermetic: string fixtures only, no subprocess and no filesystem read. It runs
the six frozen control shapes plus nine extra malformed shapes (wrong heading date, seven rows,
nine rows, live path only in the heading, missing fourth cell, duplicate group, unresolved
receipt, live bytes without the CLEAN line, and the live pointer beside an unresolved pointer in
the same fourth cell) through the same ``assess`` the real run uses.

Usage:
  python3 quality/counters/c1-r67-register.py --repo . --rev REV \\
      --controls .ufo/waves/round-67/controls/c1-controls.json
  python3 quality/counters/c1-r67-register.py --selftest
"""

import argparse
from collections import Counter
import json
import os
import re
import subprocess
import sys

HEADING = "### Surface state register (2026-11-03"
SENTINEL = "<!-- r65 register end -->"
LIVE_PATH = ".ufo/waves/round-65/receipts/gate-live-r65.txt"
# Copied from `git -C <lane> show 061dc329:.ufo/waves/round-65/receipts/gate-live-r65.txt`.
LIVE_LINE = "MADO_VERIFY: CLEAN (52 pass, 8 notes; file + live planes verified read-only)"
GROUPS = (
    "hypr plane", "waybar", "walker", "terminal configs",
    "theme/wallpaper omarchy plane", "idle/lock plane", "omarchy skill docs",
    "windows desktop plane",
)
RECEIPT_RE = re.compile(r"^\.ufo/waves/round-[0-9]+/receipts/[^ |,)]+\.(txt|json|md|sh)$")
SEPARATOR = re.compile(r"^:?-+:?$")
CONTROL_CASES = 6
FILE_PLANE = ".ufo/waves/round-65/receipts/gate-fileplane-r65.txt"


class GitError(Exception):
    """An object read or repository setup failed."""


class SetupError(Exception):
    """The invocation or the frozen control file is unusable."""


def git(repo, *args):
    env = {key: value for key, value in os.environ.items() if not key.startswith("GIT_")}
    # GIT_NO_REPLACE_OBJECTS keeps rev byte reads exact; planted refs/replace must not
    # rewrite the objects this counter measures.
    env.update(GIT_OPTIONAL_LOCKS="0", GIT_PAGER="cat", LC_ALL="C", GIT_NO_REPLACE_OBJECTS="1")
    try:
        result = subprocess.run(
            ["git", "-C", repo, "-c", "core.quotepath=false", *args],
            stdout=subprocess.PIPE, stderr=subprocess.PIPE, env=env, timeout=120,
        )
    except (OSError, subprocess.SubprocessError) as exc:
        raise GitError(str(exc)) from exc
    if result.returncode:
        raise GitError(result.stderr.decode("utf-8", "replace").strip())
    return result.stdout.decode("utf-8", "replace")


def receipts_in(text):
    """Receipt-shaped tokens of one cell/line, in first-seen order, de-duplicated."""
    paths = []
    for raw in text.split():
        path = raw.lstrip("`'\"([<*_| ").rstrip("`'\")]>*,;:.| ")
        if RECEIPT_RE.fullmatch(path) and path not in paths:
            paths.append(path)
    return paths


def cells(line):
    return [cell.strip() for cell in line.strip().strip("|").split("|")]


def separator(row):
    return bool(row) and any(row) and all(SEPARATOR.fullmatch(cell) for cell in row if cell)


def assess(text, read_receipt):
    """Pure structural assessment; read_receipt(path) returns committed text or None."""
    reasons = []
    lines = text.splitlines()
    starts = [idx for idx, line in enumerate(lines) if line.startswith(HEADING)]
    if len(starts) != 1:
        reasons.append(f"heading-count={len(starts)} expected=1")
    block = []
    if starts:
        for line in lines[starts[0] + 1:]:
            if line.startswith("## ") or line.strip() == SENTINEL:
                break
            block.append(line)
    table = [cells(line) for line in block if line.startswith("|")]
    rows = [row for idx, row in enumerate(table)
            if not separator(row)
            and not (idx + 1 < len(table) and separator(table[idx + 1]))]
    counts = Counter(row[0] for row in rows)
    if len(rows) != len(GROUPS):
        reasons.append(f"row-count={len(rows)} expected=8")
    for group in GROUPS:
        if counts[group] != 1:
            reasons.append(f"group={group!r} rows={counts[group]} expected=1")
    for row in rows:
        if row[0] not in GROUPS:
            reasons.append(f"unknown-group={row[0]!r}")

    cache = {}

    def receipt(path):
        if path not in cache:
            cache[path] = read_receipt(path)
        return cache[path]

    live_cited = False
    for row in rows:
        pointers = receipts_in(row[3]) if len(row) >= 4 else []
        if LIVE_PATH in pointers:
            live_cited = True
        if not pointers:
            reasons.append(f"row-receipt-missing={row[0]!r}")
        dangling = [path for path in pointers if receipt(path) is None]
        for path in dangling:
            reasons.append(f"receipt-unresolved-in-receipt-cell={path}")
        if pointers and len(dangling) == len(pointers):
            reasons.append(f"row-receipt-missing={row[0]!r}")
    live = receipt(LIVE_PATH)
    gate = live is not None and LIVE_LINE in live.splitlines()
    if not gate:
        reasons.append(f"exact-live-line-missing={LIVE_PATH}")
    if not live_cited:
        reasons.append(f"live-path-not-in-receipt-cell={LIVE_PATH}")
    groups_ok = sum(counts[group] == 1 for group in GROUPS)
    summary = (f"headings={len(starts)} rows={len(rows)} groups={groups_ok}/8 "
               f"live-cited={'yes' if live_cited else 'no'}")
    return reasons, summary, live_cited


def selftest():
    """Hermetic string fixtures: no filesystem, git, services, or subprocesses."""
    bodies = {LIVE_PATH: LIVE_LINE + "\n", FILE_PLANE: "MADO_VERIFY: CLEAN (file plane)\n"}
    header = HEADING + ", this host)\n| surface group | state | probe | receipt |\n|---|---|---|---|\n"
    live_rows = [f"| {group} | unmeasured state | read-only | `{LIVE_PATH}` |" for group in GROUPS]
    genuine = header + "\n".join(live_rows) + "\n" + SENTINEL + "\n"
    plane_rows = [f"| {group} | unmeasured state | read-only | `{FILE_PLANE}` |" for group in GROUPS]
    file_plane = header + "\n".join(plane_rows) + "\n" + SENTINEL + "\n"
    state_cell_only = file_plane.replace(
        plane_rows[0],
        f"| hypr plane | unmeasured state see {LIVE_PATH} | read-only | `{FILE_PLANE}` |",
    )
    cases = [
        # The six frozen control shapes, by name and expectation.
        ("genuine", genuine, bodies, True),
        ("duplicate-heading", genuine + genuine, bodies, False),
        ("row-without-receipt", genuine.replace(f"`{LIVE_PATH}`", "none", 1), bodies, False),
        ("file-plane-only", file_plane, {FILE_PLANE: bodies[FILE_PLANE]}, False),
        ("unreferenced-live-object", file_plane, bodies, False),
        ("live-in-state-cell-only", state_cell_only, bodies, False),
        # Extra malformed shapes: the four the frozen claim names (wrong heading date, seven
        # rows, nine rows, live path only in the heading) plus five more.
        ("live-plus-unresolved-same-row",
         genuine.replace(f"`{LIVE_PATH}`",
                         f"`{LIVE_PATH}` `.ufo/waves/round-65/receipts/not-committed.txt`", 1),
         bodies, False),
        # Extra malformed shapes (the four the frozen claim names, plus four more).
        ("wrong-heading-date",
         genuine.replace(HEADING, "### Surface state register (2026-10-31"), bodies, False),
        ("seven-rows", genuine.replace(live_rows[0] + "\n", ""), bodies, False),
        ("nine-rows", genuine.replace(SENTINEL, live_rows[0] + "\n" + SENTINEL), bodies, False),
        ("live-only-in-heading",
         genuine.replace(HEADING, f"{HEADING} live {LIVE_PATH}").replace(
             f"`{LIVE_PATH}`", f"`{FILE_PLANE}`"), bodies, False),
        ("missing-fourth-cell",
         genuine.replace(live_rows[0], "| hypr plane | unmeasured state | read-only |"),
         bodies, False),
        ("duplicate-group", genuine.replace("| waybar |", "| hypr plane |"), bodies, False),
        ("unresolved-receipt", file_plane, {}, False),
        ("live-bytes-without-clean-line",
         genuine, {LIVE_PATH: bodies[FILE_PLANE], FILE_PLANE: bodies[FILE_PLANE]}, False),
    ]
    failed = 0
    for name, text, objects, expected in cases:
        reasons, _, _ = assess(text, objects.get)
        passed = (not reasons) == expected
        failed += not passed
        print(f"selftest {name}: {'PASS' if passed else 'FAIL'}")
        if not passed:
            print(f"selftest {name}: detail={' | '.join(reasons) or 'accepted'}", file=sys.stderr)
    print(f"MADO_R67_REGISTER_SELFTEST: {'PASS' if not failed else 'FAIL'} "
          f"cases={len(cases)} failed={failed}")
    return 1 if failed else 0


def load_controls(path):
    try:
        with open(path, encoding="utf-8") as handle:
            doc = json.load(handle)
    except (OSError, ValueError) as exc:
        raise SetupError(f"controls-unreadable={path} detail={exc}") from exc
    if not isinstance(doc, dict) or not isinstance(doc.get("cases"), list):
        raise SetupError(f"controls-shape=invalid path={path}")
    if doc.get("live_path") != LIVE_PATH or doc.get("live_line") != LIVE_LINE:
        raise SetupError("controls-live-constants-disagree-with-counter")
    if len(doc["cases"]) != CONTROL_CASES:
        raise SetupError(f"controls-case-count={len(doc['cases'])} expected={CONTROL_CASES}")
    for case in doc["cases"]:
        if not isinstance(case, dict) or case.get("expect") not in ("accept", "reject"):
            raise SetupError(f"controls-case=invalid name={case!r}")
        if not isinstance(case.get("province"), str) or not isinstance(case.get("objects"), dict):
            raise SetupError(f"controls-case=invalid name={case.get('name')!r}")
    return doc


def score_controls(doc):
    correct = 0
    for case in doc["cases"]:
        reasons, summary, _ = assess(case["province"], case["objects"].get)
        accepted = not reasons
        want = case["expect"] == "accept"
        ok = accepted == want
        correct += ok
        for reason in reasons:
            print(f"C1_R67: detail=case:{case.get('name')}:{reason}", file=sys.stderr)
        print(f"C1_R67 case={case.get('name')} verdict={'accept' if accepted else 'reject'} "
              f"expect={case['expect']} correct={'yes' if ok else 'no'} {summary}")
    return correct


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", default=".")
    parser.add_argument("--rev")
    parser.add_argument("--controls")
    parser.add_argument("--scratch-root",
                        help="accepted for interface parity; this counter writes nothing")
    parser.add_argument("--selftest", action="store_true")
    args = parser.parse_args(argv)
    if args.selftest:
        return selftest()
    if not args.rev or not args.controls:
        parser.error("--rev and --controls are required unless --selftest is selected")
    try:
        doc = load_controls(args.controls)
    except SetupError as exc:
        print(f"C1_R67: setup=error detail={exc}", file=sys.stderr)
        return 2
    repo = os.path.abspath(args.repo)
    try:
        git(repo, "rev-parse", "--git-dir")
        rev = git(repo, "rev-parse", "--verify", "--end-of-options",
                  f"{args.rev}^{{commit}}").strip()
    except GitError as exc:
        print(f"C1_R67: setup=error detail={exc}", file=sys.stderr)
        return 2

    def read_object(path):
        try:
            return git(repo, "show", f"{rev}:{path}")
        except GitError:
            return None

    province = read_object("PROVINCE.md")
    reasons, summary, live_cited = assess(province or "", read_object)
    if province is None:
        reasons.insert(0, "province-unreadable")
    for reason in reasons:
        print(f"C1_R67: detail=register:{reason}", file=sys.stderr)
    controls_correct = score_controls(doc)
    register = "accept" if not reasons else "reject"
    controls_ok = controls_correct == CONTROL_CASES
    verdict = "TARGET_MET" if (register == "accept" and controls_ok) else "TARGET_MISSED"
    print(f"MADO_R67_REGISTER: register={register} controls={controls_correct}/"
          f"{CONTROL_CASES} {summary} verdict={verdict} rev={rev}")
    return 0 if verdict == "TARGET_MET" else 1


if __name__ == "__main__":
    sys.exit(main())
