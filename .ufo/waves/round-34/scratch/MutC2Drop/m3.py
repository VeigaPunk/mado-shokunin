#!/usr/bin/env python3
"""PRED-C2-r34-v1 counter. One command over a repo.

Contract: exit 0 TARGET_MET, 1 TARGET_MISSED, 2 usage or predicate drift.
Counts a mismatch between the last SCORECARD publication of the S189 quote
line and the pinned fetch. Absent publication is a mismatch. Does not follow
symlinks.

PRED-C2-r34-v1: TARGET_MET iff mismatch=0, where mismatch is 0 only when the last SCORECARD line matching r34-s189-line: publishes line=169 and line 169 of the regular-file fetch .ufo/waves/round-32/fetch/S189.bin opened with O_NOFOLLOW (nlink=1, sha256 eea605dfe5ce09e1f92a67ec478bf61a19894c6e0ee3302c0393521a2ee9540d) strip-equals const size_t MAX_QUEUED_EVENTS = 64; and line 128 of that file does not.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import stat
import sys
from pathlib import Path

PREDICATE = (
    "PRED-C2-r34-v1: TARGET_MET iff mismatch=0, where mismatch is 0 only when the last "
    "SCORECARD line matching r34-s189-line: publishes line=169 and line 169 of the "
    "regular-file fetch .ufo/waves/round-32/fetch/S189.bin opened with O_NOFOLLOW "
    "(nlink=1, sha256 eea605dfe5ce09e1f92a67ec478bf61a19894c6e0ee3302c0393521a2ee9540d) "
    "strip-equals const size_t MAX_QUEUED_EVENTS = 64; and line 128 of that file does not."
)
PINNED_REL = ".ufo/waves/round-32/fetch/S189.bin"
PINNED_SHA = "eea605dfe5ce09e1f92a67ec478bf61a19894c6e0ee3302c0393521a2ee9540d"
QUOTE = "const size_t MAX_QUEUED_EVENTS = 64;"
MARKER = "r34-s189-line:"


def die(msg: str) -> None:
    print(f"PRED-C2-r34-v1 error={msg}", file=sys.stderr)
    raise SystemExit(2)


def read_regular(root: Path, rel: str) -> bytes | None:
    if not rel or rel.startswith("/") or ".." in Path(rel).parts:
        return None
    parts = Path(rel).parts
    if not parts or any(p in ("", ".", "..") for p in parts):
        return None
    try:
        root_stat = root.lstat()
    except OSError:
        return None
    if stat.S_ISLNK(root_stat.st_mode) or not stat.S_ISDIR(root_stat.st_mode):
        return None
    cur = root
    for i, part in enumerate(parts):
        cur = cur / part
        try:
            st = cur.lstat()
        except OSError:
            return None
        if stat.S_ISLNK(st.st_mode):
            return None
        last = i == len(parts) - 1
        if not last:
            if not stat.S_ISDIR(st.st_mode):
                return None
            continue
        if not stat.S_ISREG(st.st_mode) or st.st_nlink != 1:
            return None
    try:
        fd = os.open(cur, os.O_RDONLY | os.O_NOFOLLOW)
    except OSError:
        return None
    try:
        return os.read(fd, 8_000_000)
    finally:
        os.close(fd)


def published_line(text: str) -> str:
    last = ""
    for line in text.splitlines():
        if MARKER in line:
            last = line
            break
    if not last:
        return "absent"
    tail = last[last.find(MARKER) + len(MARKER):].strip()
    if tail == "line=169":
        return "169"
    if tail == "line=128":
        return "128"
    return "other"


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo", required=True)
    ap.add_argument("--scorecard", required=True)
    ap.add_argument("--frozen", required=True)
    args = ap.parse_args()
    repo = Path(args.repo)
    frozen_path = Path(args.frozen)
    if not frozen_path.is_file():
        die("frozen-missing")
    spec = json.loads(frozen_path.read_text())
    if spec.get("predicate") != PREDICATE:
        die("predicate-drift")
    card_path = Path(args.scorecard)
    try:
        card_rel = str(card_path.resolve().relative_to(repo.resolve()))
    except ValueError:
        card_rel = ""
    if card_rel != "SCORECARD.md" and card_path.name != "SCORECARD.md":
        # junk controls pass a regular-file card by absolute path; still refuse symlinks
        pass
    if card_path.is_symlink() or not card_path.is_file():
        published = "absent"
        card = ""
    else:
        try:
            st = card_path.lstat()
        except OSError:
            die("scorecard-unreadable")
        if stat.S_ISLNK(st.st_mode) or not stat.S_ISREG(st.st_mode):
            published = "absent"
            card = ""
        else:
            card = card_path.read_text(errors="replace")
            published = published_line(card)
    blob = read_regular(repo, PINNED_REL)
    digest = hashlib.sha256(blob).hexdigest() if blob is not None else ""
    measured = "absent"
    line128_is_quote = False
    if blob is not None and digest == PINNED_SHA:
        lines = blob.decode("utf-8", "replace").splitlines()
        if len(lines) >= 169 and lines[168].strip() == QUOTE:
            measured = "169"
        if len(lines) >= 128 and lines[127].strip() == QUOTE:
            line128_is_quote = True
    mismatch = 0 if published == "169" and measured == "169" and not line128_is_quote else 1
    verdict = "TARGET_MET" if mismatch == 0 else "TARGET_MISSED"
    print(
        f"PRED-C2-r34-v1 published={published} measured={measured} "
        f"mismatch={mismatch} verdict={verdict}"
    )
    raise SystemExit(0 if mismatch == 0 else 1)


if __name__ == "__main__":
    main()
