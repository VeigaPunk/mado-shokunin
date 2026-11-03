#!/usr/bin/env python3
"""c1-r65-register.py — PRED-C1-r65: the surface-state register re-derived on the returned host.

Draft for `quality/counters/c1-r65-register.py` (mado round-65, w1 build seat
R65ExecC1Counter). The frozen predicate is claim C1 of
`.ufo/waves/round-65/claims-declaration-r65.md`, copied verbatim:

> **Counting command:** `python3 quality/counters/c1-r65-register.py --repo . --rev <landing>`
> → prints `MADO_R65_REGISTER: … verdict=TARGET_MET` exit 0 (rows=8, receipts resolved at rev,
> gate-clean line present at rev); `TARGET_MISSED` exit 1 otherwise. The counter reads git
> objects at `--rev` only; it never reads the worktree.

What it measures (every byte comes from `git -C <repo> show/ls-tree <rev>:…`; the worktree is
never opened, `os.path.join(repo, …)` never appears):

``province``  `git show <rev>:PROVINCE.md`. Unreadable at a valid repository → fail closed:
              `verdict=TARGET_MISSED … reason=province-unreadable`, rc=1.
``block``     the lines from the first line starting `### Surface state register (2026-11-03`
              up to (exclusive) the first later line that starts `## ` or whose stripped form is
              the sentinel `<!-- r65 register end -->`, whichever comes first; EOF if neither.
              Block absent → `rows=0`, `groups=0/8`, `verdict=TARGET_MISSED`, rc=1.
``rows``      lines of the block that start `|` (exact left edge, as the frozen text says),
              split on `|`, a leading empty cell dropped; separator rows (every non-empty cell a
              dash/colon run) and markdown header rows (a pipe row immediately followed by a
              separator row) are not data rows; a data row needs >= 3 non-empty cells.
``groups``    `k/8`: how many of the eight exact group strings below equal the trimmed **first
              cell** of some data row. Equality is exact — a first cell such as
              ``hypr plane (`~/.config/hypr/**`, `hyprctl`)`` does NOT match `hypr plane`; the
              group name must stand alone in the first cell and the probe/pointer detail belongs
              in the later cells.
``receipts``  every whitespace-separated token of the block matching the frozen anchored pattern
              ``^\\.ufo/waves/round-65/receipts/[^ |,)]+\\.(txt|json|md|sh)$`` (first-seen order,
              de-duplicated). A token the strict pattern rejects is retried once with a single
              markdown wrapper/bracket/quote run stripped from each end; the path shape itself is
              never relaxed, so backticked or parenthesised pointers in a table are still seen
              while arbitrary prose is not.
``resolved``  receipts present in `git ls-tree -r -z --name-only <rev>`.
``gate``      `ok` iff some resolved receipt, read via `git show <rev>:<path>`, contains the
              substring `MADO_VERIFY: CLEAN`; `missing` otherwise.

Met iff `rows >= 8` AND `groups == 8` AND every extracted receipt resolved AND `gate == ok`.
Exit 0 only when met, 1 otherwise. No file is written, no scratch directory is made, no network
and no other child process is spawned (only `git` reads).

Setup errors (bad `--repo`, not a git repository, unknown option) exit 2 with a `C1_R65:`
diagnostic on stderr — the same convention as the lane's other counters. Diagnostics on a miss go
to stderr as `detail:` lines; stdout is exactly one `MADO_R65_REGISTER:` line.

Usage:
  python3 c1-r65-register.py --repo <lane> --rev <rev>
"""

import argparse
import os
import re
import subprocess
import sys

PROVINCE_REL = "PROVINCE.md"
HEADING = "### Surface state register (2026-11-03"
SENTINEL = "<!-- r65 register end -->"
GATE_TOKEN = "MADO_VERIFY: CLEAN"
GROUPS = (
    "hypr plane",
    "waybar",
    "walker",
    "terminal configs",
    "theme/wallpaper omarchy plane",
    "idle/lock plane",
    "omarchy skill docs",
    "windows desktop plane",
)
RECEIPT_RE = re.compile(r"^\.ufo/waves/round-65/receipts/[^ |,)]+\.(txt|json|md|sh)$")
SEPARATOR_CELL = re.compile(r"^:?-+:?$")
WRAP_LEAD = "`'\"([<*_|"
WRAP_TAIL = "`'\")]>*,;:.|"
GIT_TIMEOUT = 120


class GitError(Exception):
    """A git invocation that did not return 0."""


def git(repo, *args):
    """Run a read-only git command in `repo` and return its stdout bytes."""
    cmd = ["git", "-C", repo, "-c", "core.quotepath=false"] + list(args)
    env = dict(os.environ)
    env["GIT_OPTIONAL_LOCKS"] = "0"
    env["LC_ALL"] = "C"
    env["GIT_PAGER"] = "cat"
    try:
        proc = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                              env=env, timeout=GIT_TIMEOUT)
    except (OSError, subprocess.SubprocessError) as exc:
        raise GitError("%s: %s" % (" ".join(cmd), exc))
    if proc.returncode != 0:
        raise GitError("%s: rc=%d %s" % (" ".join(cmd), proc.returncode,
                                         proc.stderr.decode("utf-8", "replace").strip()))
    return proc.stdout


def extract_block(text):
    """The 2026-11-03 register block as a list of lines, or None when absent."""
    lines = text.splitlines()
    for start, line in enumerate(lines):
        if line.startswith(HEADING):
            end = len(lines)
            for idx in range(start + 1, len(lines)):
                cand = lines[idx]
                if cand.startswith("## ") or cand.strip() == SENTINEL:
                    end = idx
                    break
            return lines[start:end]
    return None


def split_cells(line):
    """Cells of one pipe-table line, trimmed, with the outer empty cells dropped."""
    cells = line.split("|")
    if cells and not cells[0].strip():
        cells = cells[1:]
    if cells and line.endswith("|") and not cells[-1].strip():
        cells = cells[:-1]
    return [cell.strip() for cell in cells]


def is_separator(cells):
    nonempty = [cell for cell in cells if cell]
    return bool(nonempty) and all(SEPARATOR_CELL.match(cell) for cell in nonempty)


def data_rows(block):
    """The block's data rows, as cell lists; separators and table headers excluded."""
    pipe_rows = [split_cells(line) for line in block if line.startswith("|")]
    rows = []
    for idx, cells in enumerate(pipe_rows):
        if is_separator(cells):
            continue
        nxt = pipe_rows[idx + 1] if idx + 1 < len(pipe_rows) else None
        if nxt is not None and is_separator(nxt):
            continue  # markdown table header: the row above a separator
        if len([cell for cell in cells if cell]) >= 3:
            rows.append(cells)
    return rows


def unwrap(token):
    out = token
    while out and out[0] in WRAP_LEAD:
        out = out[1:]
    while out and out[-1] in WRAP_TAIL:
        out = out[:-1]
    return out


def receipts_in(block):
    """Receipt paths named by tokens of the block, frozen pattern, first-seen order."""
    found = []
    for raw in "\n".join(block).split():
        for cand in (raw, unwrap(raw)):
            if RECEIPT_RE.match(cand):
                if cand not in found:
                    found.append(cand)
                break
    return found


def main(argv=None):
    ap = argparse.ArgumentParser(
        description="PRED-C1-r65: the surface-state register re-derived on the returned host")
    ap.add_argument("--repo", default=".")
    ap.add_argument("--rev", required=True)
    args = ap.parse_args(argv)

    repo = os.path.abspath(args.repo)
    if not os.path.isdir(repo):
        print("C1_R65: setup=error detail=--repo %s is not a directory" % repo, file=sys.stderr)
        return 2
    try:
        git(repo, "rev-parse", "--git-dir")
    except GitError as exc:
        print("C1_R65: setup=error detail=--repo %s is not a git repository (%s)"
              % (repo, exc), file=sys.stderr)
        return 2

    try:
        province = git(repo, "show", "%s:%s" % (args.rev, PROVINCE_REL))
    except GitError as exc:
        print("C1_R65: detail=%s unreadable at %s (%s)"
              % (PROVINCE_REL, args.rev, exc), file=sys.stderr)
        print("MADO_R65_REGISTER: rows=0 groups=0/8 receipts=0 resolved=0 gate=missing "
              "verdict=TARGET_MISSED rev=%s reason=province-unreadable" % args.rev)
        return 1
    text = province.decode("utf-8", "replace")

    try:
        rev = git(repo, "rev-parse", "--verify", "--quiet",
                  "%s^{commit}" % args.rev).decode("utf-8", "replace").strip() or args.rev
    except GitError:
        rev = args.rev

    block = extract_block(text)
    if block is None:
        print("C1_R65: detail=no '%s' block at %s" % (HEADING, rev), file=sys.stderr)
        print("MADO_R65_REGISTER: rows=0 groups=0/8 receipts=0 resolved=0 gate=missing "
              "verdict=TARGET_MISSED rev=%s" % rev)
        return 1

    rows = data_rows(block)
    first_cells = set(cells[0] for cells in rows if cells)
    groups = [name for name in GROUPS if name in first_cells]

    try:
        tree = set(path.decode("utf-8", "replace")
                   for path in git(repo, "ls-tree", "-r", "-z", "--name-only",
                                   args.rev).split(b"\0") if path)
    except GitError as exc:
        print("C1_R65: detail=ls-tree failed at %s (%s)" % (rev, exc), file=sys.stderr)
        tree = set()

    receipts = receipts_in(block)
    resolved = [path for path in receipts if path in tree]

    gate = "missing"
    for path in resolved:
        try:
            body = git(repo, "show", "%s:%s" % (args.rev, path)).decode("utf-8", "replace")
        except GitError:
            continue
        if GATE_TOKEN in body:
            gate = "ok"
            break

    met = (len(rows) >= 8 and len(groups) == len(GROUPS)
           and len(resolved) == len(receipts) and gate == "ok")

    if not met:
        if len(rows) < 8:
            print("C1_R65: detail=rows=%d, need >= 8 data rows" % len(rows), file=sys.stderr)
        missing = [name for name in GROUPS if name not in first_cells]
        if missing:
            print("C1_R65: detail=groups missing (%d): %s"
                  % (len(missing), "; ".join(missing)), file=sys.stderr)
            near = []
            for cells in rows:
                cell = cells[0] if cells else ""
                if cell in GROUPS:
                    continue
                for name in missing:
                    if cell.startswith(name):
                        near.append((name, cell))
                        break
            for name, cell in near[:4]:
                print("C1_R65: detail=first cell %r is not exactly %r "
                      "(the group name must stand alone in the first cell)" % (cell, name),
                      file=sys.stderr)
        indented = [line for line in block
                    if line.startswith((" ", "\t")) and line.lstrip().startswith("|")]
        if indented:
            print("C1_R65: detail=%d pipe line(s) are indented; the frozen row rule "
                  "requires '|' at column 0" % len(indented), file=sys.stderr)
        unresolved = [path for path in receipts if path not in tree]
        if unresolved:
            print("C1_R65: detail=receipts not at %s: %s"
                  % (rev[:12], ", ".join(unresolved)), file=sys.stderr)
        if gate != "ok":
            print("C1_R65: detail=no resolved receipt contains %r" % GATE_TOKEN,
                  file=sys.stderr)

    print("MADO_R65_REGISTER: rows=%d groups=%d/8 receipts=%d resolved=%d gate=%s "
          "verdict=%s rev=%s" % (len(rows), len(groups), len(receipts), len(resolved),
                                 gate, "TARGET_MET" if met else "TARGET_MISSED", rev))
    return 0 if met else 1


if __name__ == "__main__":
    sys.exit(main())
