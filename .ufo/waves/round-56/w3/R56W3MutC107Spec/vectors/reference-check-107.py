#!/usr/bin/env python3
"""Spec-literal reference implementation of criterion 107 — ORACLE, NOT THE GATE.

Reads only git objects at <rev>; writes nothing.  It exists to (a) prove that the
hand-authored expectations in vectors/expected/*.stdout are attainable from the
criterion-107 text alone and (b) serve as the bounded behavioural detector's
subject in mutate-check-107.py.

The lane gate for criterion 107 is the sibling seat's quality/check-anchor-cover.py;
this file must not be mistaken for it.

Usage:
  python3 -I reference-check-107.py --repo <git-root> --rev <sha> [--work <dir>]
"""

import argparse
import re
import subprocess
import sys

WORD = set("ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789_")
SID_RE = re.compile(r"^S\d{3,}$")
PIN_CELL_RE = re.compile(r"^([^:\s]+):(\d+)$")
URL_RE = re.compile(r"https?://[^\s|]+")
PIN_RE = re.compile(r"\bpin\s+(\S+)")
TRAILING = set(").,;")


def git_out(repo, *args):
    return subprocess.run(
        ["git", "-C", repo, *args], check=True, capture_output=True, text=True
    ).stdout


def read_blob(repo, rev, path):
    r = subprocess.run(
        ["git", "-C", repo, "show", f"{rev}:{path}"], capture_output=True
    )
    if r.returncode != 0:
        return None
    return r.stdout


def table_rows(text):
    """Rows of markdown tables: lines whose stripped form starts with '|'."""
    out = []
    for line in text.split("\n"):
        s = line.strip()
        if not s.startswith("|"):
            continue
        body = s
        if body.endswith("|"):
            body = body[:-1]
        cells = [c.strip() for c in body[1:].split("|")]
        out.append(cells)
    return out


def scoped_lines(text):
    """Lines outside fenced code blocks and outside HTML comments."""
    keep = []
    in_fence = False
    in_comment = False
    for line in text.split("\n"):
        s = line.strip()
        if in_fence:
            if s.startswith("```") or s.startswith("~~~"):
                in_fence = False
            continue
        if in_comment:
            if "-->" in s:
                in_comment = False
                rest = s.split("-->", 1)[1]
                if rest.strip():
                    keep.append(rest)
            continue
        if s.startswith("```") or s.startswith("~~~"):
            in_fence = True
            continue
        if "<!--" in s:
            if "-->" in s.split("<!--", 1)[1]:
                rest = s.split("<!--", 1)[1].split("-->", 1)[1]
                if rest.strip():
                    keep.append(rest)
            else:
                in_comment = True
            continue
        keep.append(line)
    return keep


def parse_locators(text):
    """Locator list right after 'NAME:'. Items are N or N-M, comma separated,
    one optional space may follow a comma, the list continues only while the
    next item starts with a digit."""
    items = []
    i = 0
    while True:
        m = re.match(r"(\d+)(?:-(\d+))?", text[i:])
        if not m:
            break
        n = int(m.group(1))
        if n < 1:
            break
        hi = int(m.group(2)) if m.group(2) is not None else n
        items.append((n, hi))
        i += m.end()
        j = i
        if j < len(text) and text[j] == ",":
            j += 1
            if j < len(text) and text[j] == " ":
                j += 1
            if j < len(text) and text[j].isdigit():
                i = j
                continue
        break
    return items


def derive_name(source_cell):
    toks = URL_RE.findall(source_cell)
    if not toks:
        return None
    name = toks[-1].rsplit("/", 1)[-1]
    while name and name[-1] in TRAILING:
        name = name[:-1]
    return name


def check(repo, rev):
    registry = {}
    src = read_blob(repo, rev, "corpus/SOURCES.md")
    if src is None:
        sys.stderr.write("setup error: corpus/SOURCES.md missing at rev\n")
        return 2
    for cells in table_rows(src.decode("utf-8")):
        if len(cells) < 6:
            continue
        rid = cells[0]
        if not SID_RE.match(rid):
            continue
        registry.setdefault(rid, []).append(cells)

    entries = [
        p for p in git_out(repo, "ls-tree", "-r", "--name-only", rev, "--",
                           "corpus/knowledge").split("\n")
        if p.strip()
    ]

    lines = []
    rows = covered = miss = 0

    for path in entries:
        blob = read_blob(repo, rev, path)
        if blob is None:
            continue
        text = blob.decode("utf-8")
        for raw in scoped_lines(text):
            s = raw.strip()
            if not s.startswith("|"):
                continue
            body = s[:-1] if s.endswith("|") else s
            cells = [c.strip() for c in body[1:].split("|")]
            if len(cells) < 4:
                continue
            row_id, sid, pin_cell = cells[0], cells[2], cells[3]
            if not SID_RE.match(sid):
                continue
            rows += 1
            verdict = "OK"
            reason = None
            m = PIN_CELL_RE.match(pin_cell)
            if not m:
                verdict, reason = "MISS", "malformed-pin"
                lines.append(
                    f"ANCHOR_COVER: row={row_id} sid={sid} line=none name=none "
                    f"locators=none eof=unchecked verdict=MISS "
                    f"[reason=malformed-pin]"
                )
                miss += 1
                continue
            line_no = int(m.group(2))
            rws = registry.get(sid, [])
            if len(rws) == 0:
                verdict, reason = "MISS", "no-registry-row"
                lines.append(
                    f"ANCHOR_COVER: row={row_id} sid={sid} line={line_no} "
                    f"name=none locators=none eof=unchecked verdict=MISS "
                    f"[reason=no-registry-row]"
                )
                miss += 1
                continue
            if len(rws) > 1:
                verdict, reason = "MISS", "dup-id"
                lines.append(
                    f"ANCHOR_COVER: row={row_id} sid={sid} line={line_no} "
                    f"name=none locators=none eof=unchecked verdict=MISS "
                    f"[reason=dup-id]"
                )
                miss += 1
                continue
            r = rws[0]
            name = derive_name(r[1])
            if name is None or "#" in name or "?" in name:
                verdict, reason = "MISS", "no-name"
                lines.append(
                    f"ANCHOR_COVER: row={row_id} sid={sid} line={line_no} "
                    f"name={name if name else 'none'} locators=none "
                    f"eof=unchecked verdict=MISS [reason=no-name]"
                )
                miss += 1
                continue
            anchor_cell = r[5]
            occurrences = []
            for om in re.finditer(re.escape(name) + ":", anchor_cell):
                i = om.start()
                prev = anchor_cell[i - 1] if i > 0 else None
                if prev is None or prev not in WORD:
                    occurrences.append(parse_locators(anchor_cell[om.end():]))
            flat = [it for occ in occurrences for it in occ]
            locators = ",".join(
                (f"{n}-{hi}" if hi != n else str(n)) for n, hi in flat
            ) or "none"
            covered_here = any(
                hi >= n and n <= line_no <= hi for n, hi in flat
            )
            pm = PIN_RE.search(anchor_cell)
            eof = "unchecked"
            past = False
            if pm:
                path_pin = pm.group(1)
                blob = read_blob(repo, rev, path_pin)
                if blob is None:
                    sys.stderr.write(
                        f"setup error: pin {path_pin} missing at rev\n"
                    )
                    return 2
                pieces = len(blob.split(b"\n"))
                eof = "checked"
                past = any(max(n, hi) > pieces for n, hi in flat)
            if past:
                verdict, reason = "MISS", "past-eof"
            elif not covered_here:
                verdict = "MISS"
            out = (
                f"ANCHOR_COVER: row={row_id} sid={sid} line={line_no} "
                f"name={name} locators={locators} eof={eof} verdict={verdict}"
            )
            if reason:
                out += f" [reason={reason}]"
            lines.append(out)
            if verdict == "OK":
                covered += 1
            else:
                miss += 1

    lines.append(
        f"CHECK107: rows={rows} covered={covered} miss={miss} "
        f"verdict={'OK' if miss == 0 and rows > 0 else 'FAIL'}"
    )
    sys.stdout.write("\n".join(lines) + "\n")
    return 0 if (miss == 0 and rows > 0) else 1


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo", required=True)
    ap.add_argument("--rev", required=True)
    ap.add_argument("--work", default=None)
    args = ap.parse_args()
    sys.exit(check(args.repo, args.rev))


if __name__ == "__main__":
    main()
