#!/usr/bin/env python3
"""PRED-C1-r66: committed register structure, not state-cell truth.

Normal mode reads only git objects at --rev; no worktree files or host probes.
Exactly one returned-host heading, exactly eight distinct existing group rows,
a resolving receipt in every fourth (receipt) cell, all named receipts resolved,
and the frozen live CLEAN line in the named live receipt are required.
The live line below was copied from committed gate-live-r65.txt at
 eafd500fa7be76dca59e729435e231a5032cc037, not inferred from file-plane CLEAN.
Receipt presence and that historical line do NOT establish current state truth.

Usage: python3 quality/counters/c1-r66-register.py --repo . --rev COMMIT
       python3 quality/counters/c1-r66-register.py --selftest
Exit: 0 TARGET_MET, 1 TARGET_MISSED, 2 setup/usage error.
"""

import argparse
from collections import Counter
import os
import re
import subprocess
import sys

HEADING = "### Surface state register (2026-11-03"
SENTINEL = "<!-- r65 register end -->"
LIVE_PATH = ".ufo/waves/round-65/receipts/gate-live-r65.txt"
LIVE_LINE = "MADO_VERIFY: CLEAN (52 pass, 8 notes; file + live planes verified read-only)"
GROUPS = (
    "hypr plane", "waybar", "walker", "terminal configs",
    "theme/wallpaper omarchy plane", "idle/lock plane", "omarchy skill docs",
    "windows desktop plane",
)
RECEIPT_RE = re.compile(r"^\.ufo/waves/round-65/receipts/[^ |,)]+\.(txt|json|md|sh)$")
SEPARATOR = re.compile(r"^:?-+:?$")


class GitError(Exception):
    """An object read or repository setup failed."""


def git(repo, *args):
    env = {key: value for key, value in os.environ.items() if not key.startswith("GIT_")}
    env.update(GIT_OPTIONAL_LOCKS="0", GIT_PAGER="cat", LC_ALL="C")
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
    paths = []
    for raw in text.split():
        path = raw.lstrip("`'\"([<*_| ").rstrip("`'\")]>*,;:.| ")
        if RECEIPT_RE.fullmatch(path) and path not in paths:
            paths.append(path)
    return paths


def cells(line):
    return [cell.strip() for cell in line.strip().strip("|").split("|")]


def separator(row):
    return bool(row) and all(SEPARATOR.fullmatch(cell) for cell in row if cell) and any(row)


def assess(text, read_receipt):
    """Pure structural assessment; read_receipt returns committed text or None."""
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
    cache = {}

    def receipt(path):
        if path not in cache:
            cache[path] = read_receipt(path)
        return cache[path]

    paths = receipts_in("\n".join(block))
    for path in paths:
        if receipt(path) is None:
            reasons.append(f"receipt-unresolved={path}")
    for row in rows:
        pointers = receipts_in(row[3]) if len(row) >= 4 else []
        if not any(receipt(path) is not None for path in pointers):
            reasons.append(f"row-receipt-missing={row[0]!r}")
    live = receipt(LIVE_PATH)
    gate = live is not None and LIVE_LINE in live.splitlines()
    if not gate:
        reasons.append(f"exact-live-line-missing={LIVE_PATH}")
    summary = (f"headings={len(starts)} rows={len(rows)} "
               f"groups={sum(counts[group] == 1 for group in GROUPS)}/8 "
               f"receipts={len(paths)} resolved={sum(receipt(path) is not None for path in paths)} "
               f"gate={'ok' if gate else 'missing'}")
    return reasons, summary


def selftest():
    """Hermetic string fixtures: no filesystem, git, services, or subprocesses."""
    file_path = ".ufo/waves/round-65/receipts/gate-fileplane-r65.txt"
    bodies = {LIVE_PATH: LIVE_LINE + "\n", file_path: "MADO_VERIFY: CLEAN (file plane)\n"}
    header = HEADING + ", this host)\n| surface group | state | probe | receipt |\n|---|---|---|---|\n"
    rows = [f"| {group} | unmeasured state | read-only | `{LIVE_PATH}` |" for group in GROUPS]
    genuine = header + "\n".join(rows) + "\n" + SENTINEL + "\n"
    cases = [
        ("genuine", genuine, bodies, True),
        ("duplicate-heading", genuine + genuine, bodies, False),
        ("row-without-receipt", genuine.replace(f"`{LIVE_PATH}`", "none", 1), bodies, False),
        ("file-plane-only", genuine.replace(LIVE_PATH, file_path), {file_path: bodies[file_path]}, False),
        ("file-plane-at-live-path", genuine, {LIVE_PATH: bodies[file_path]}, False),
        ("live-line-substring", genuine, {LIVE_PATH: "prefix " + LIVE_LINE}, False),
        ("missing-heading", genuine.replace(HEADING, "### Other"), bodies, False),
        ("duplicate-group", genuine.replace("| waybar |", "| hypr plane |"), bodies, False),
        ("missing-row", genuine.replace(rows[0] + "\n", ""), bodies, False),
        ("extra-row", genuine.replace(SENTINEL, rows[0] + "\n" + SENTINEL), bodies, False),
        ("receipt-in-state-only", genuine.replace(rows[0], f"| hypr plane | `{LIVE_PATH}` | probe | none |"), bodies, False),
        ("unresolved-receipt", genuine, {}, False),
        ("missing-fourth-cell", genuine.replace(rows[0], "| hypr plane | state | probe |"), bodies, False),
        ("state-truth-not-measured", genuine.replace("unmeasured state", "invented state"), bodies, True),
        ("unreferenced-live-receipt", genuine.replace(LIVE_PATH, file_path), bodies, True),
    ]
    failed = 0
    for name, text, objects, expected in cases:
        reasons, _ = assess(text, objects.get)
        passed = (not reasons) == expected
        failed += not passed
        print(f"selftest {name}: {'PASS' if passed else 'FAIL'}")
    print(f"MADO_R66_REGISTER_SELFTEST: {'PASS' if not failed else 'FAIL'} cases={len(cases)} failed={failed}")
    return 1 if failed else 0


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", default=".")
    parser.add_argument("--rev")
    parser.add_argument("--selftest", action="store_true")
    args = parser.parse_args(argv)
    if args.selftest:
        return selftest()
    if not args.rev:
        parser.error("--rev is required unless --selftest is selected")
    repo = os.path.abspath(args.repo)
    try:
        git(repo, "rev-parse", "--git-dir")
        rev = git(repo, "rev-parse", "--verify", "--end-of-options", f"{args.rev}^{{commit}}").strip()
    except GitError as exc:
        print(f"C1_R66: setup=error detail={exc}", file=sys.stderr)
        return 2

    def read_object(path):
        try:
            return git(repo, "show", f"{rev}:{path}")
        except GitError:
            return None

    province = read_object("PROVINCE.md")
    reasons, summary = assess(province or "", read_object)
    if province is None:
        reasons.insert(0, "province-unreadable")
    for reason in reasons:
        print(f"C1_R66: detail={reason}", file=sys.stderr)
    print(f"MADO_R66_REGISTER: {summary} verdict={'TARGET_MISSED' if reasons else 'TARGET_MET'} rev={rev}")
    return 1 if reasons else 0


if __name__ == "__main__":
    sys.exit(main())
