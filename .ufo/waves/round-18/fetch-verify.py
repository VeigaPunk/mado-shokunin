#!/usr/bin/env python3
"""fetch-verify.py — verify mado round-18 fetch receipts (R17-V3 enforcement).

Walks <fetch-root>/*/receipts.jsonl (default: the fetch/ directory next to
this script). For every receipt line of schema mado-fetch-receipt-v1 it
re-checks that the body file exists beside receipts.jsonl, that its byte
count matches "bytes" and that its sha256 matches "sha256".

Per receipt prints exactly:
    FETCH <seat>/<body> ok|BAD_SHA|BAD_BYTES|MISSING|BAD_SCHEMA|BAD_JSON

Optional SOURCES.md join:
    --sources <SOURCES.md> --rows S072,S073[,S074...]
Each listed row prints:
    ROW <id> receipted|UNRECEIPTED
A row is "receipted" when at least one verified-or-listed receipt either
has a sha256 that literally appears in the row's anchor cell, or has a
url/final_url equal to a URL appearing in the row.

Optional quote check (repeatable):
    --quote 'S072=<text>'
Checks that <text> (bytes, UTF-8) occurs in at least one body of the
receipts matched to that row. Prints:
    QUOTE <id> ok|NOT_FOUND|UNRECEIPTED|NO_ROW
Quote row ids are checked even when not listed in --rows.

Exit: 0 when every receipt verified and every listed row is receipted and
every quote is found; 1 on any bad receipt / unreceipted row / missing
quote; 2 on usage errors.
"""

import argparse
import hashlib
import json
import re
import sys
from pathlib import Path

SCHEMA = "mado-fetch-receipt-v1"
URL_RE = re.compile(r"https?://[^\s|)\]<>'\"`]+")
ROW_ID_RE = re.compile(r"S\d{3}")


def usage_error(msg):
    print(f"fetch-verify: {msg}", file=sys.stderr)
    sys.exit(2)


def sha256_file(path):
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def verify_receipt(seat, lineno, rec, seat_dir):
    """Return (status, body_label, detail, body_path_or_None)."""
    if not isinstance(rec, dict) or rec.get("schema") != SCHEMA:
        return "BAD_SCHEMA", f"<line {lineno}>", "schema-mismatch", None
    body = rec.get("body")
    if not isinstance(body, str) or not body or "/" in body or body in (".", ".."):
        return "BAD_SCHEMA", f"<line {lineno}>", "bad-body-field", None
    bpath = seat_dir / body
    if not bpath.is_file():
        return "MISSING", body, "", bpath
    try:
        actual_bytes = bpath.stat().st_size
        want_bytes = rec.get("bytes")
        is_int = isinstance(want_bytes, int) and not isinstance(want_bytes, bool)
        if not is_int or want_bytes != actual_bytes:
            want_disp = want_bytes if is_int else repr(want_bytes)
            return (
                "BAD_BYTES",
                body,
                f"want={want_disp} got={actual_bytes}",
                bpath,
            )
        want_sha = rec.get("sha256")
        got_sha = sha256_file(bpath)
        if not isinstance(want_sha, str) or got_sha != want_sha.lower():
            want_disp = want_sha if isinstance(want_sha, str) else repr(want_sha)
            return "BAD_SHA", body, f"want={want_disp} got={got_sha}", bpath
    except OSError as exc:
        return "MISSING", body, f"read-error:{exc}", None
    return "ok", body, "", bpath


def load_sources_rows(path):
    """Parse the SOURCES.md registry table -> {row_id: {anchor, urls}}."""
    rows = {}
    try:
        text = Path(path).read_text(encoding="utf-8", errors="replace")
    except OSError as exc:
        usage_error(f"cannot read --sources {path}: {exc}")
    for line in text.splitlines():
        s = line.strip()
        if not (s.startswith("|") and s.endswith("|")):
            continue
        cells = [c.strip() for c in s.split("|")]
        # leading/trailing empties: cells[1]=id, cells[2]=source, cells[6]=anchor
        if len(cells) < 8 or not ROW_ID_RE.fullmatch(cells[1] or ""):
            continue
        rid = cells[1]
        source = cells[2] if len(cells) > 2 else ""
        anchor = cells[6] if len(cells) > 6 else ""
        urls = {u.rstrip(").,;:!") for u in URL_RE.findall(source)}
        rows[rid] = {"anchor": anchor, "urls": urls}
    return rows


def main():
    ap = argparse.ArgumentParser(
        description="Verify mado fetch receipts and optional SOURCES.md joins."
    )
    ap.add_argument(
        "--fetch-root",
        default=str(Path(__file__).resolve().parent / "fetch"),
        help="directory containing <seat>/receipts.jsonl (default: ./fetch "
        "next to this script)",
    )
    ap.add_argument("--sources", help="path to corpus/SOURCES.md for row joins")
    ap.add_argument(
        "--rows",
        action="append",
        default=[],
        metavar="S072,S073,...",
        help="comma-separated SOURCES row ids to join (repeatable)",
    )
    ap.add_argument(
        "--quote",
        action="append",
        default=[],
        metavar="S0NN=<text>",
        help="check <text> occurs in a body of the row's receipts (repeatable)",
    )
    args = ap.parse_args()

    if (args.rows or args.quote) and not args.sources:
        usage_error("--rows/--quote require --sources")

    join_ids = []
    for chunk in args.rows:
        for rid in chunk.split(","):
            rid = rid.strip()
            if rid and rid not in join_ids:
                join_ids.append(rid)
    quotes = []
    for spec in args.quote:
        if "=" not in spec:
            usage_error(f"--quote spec must be S0NN=<text>, got: {spec!r}")
        rid, text = spec.split("=", 1)
        rid = rid.strip()
        if not rid or not ROW_ID_RE.fullmatch(rid):
            usage_error(f"--quote spec has bad row id: {spec!r}")
        if not text:
            usage_error(f"--quote spec has empty text: {spec!r}")
        quotes.append((rid, text))

    all_ids = join_ids + [r for r, _ in quotes if r not in join_ids]
    for rid in all_ids:
        if not ROW_ID_RE.fullmatch(rid):
            usage_error(f"bad row id: {rid!r}")

    fetch_root = Path(args.fetch_root)
    if not fetch_root.is_dir():
        usage_error(f"fetch root not a directory: {fetch_root}")

    # SOURCES.md is parsed (and row ids validated) before any receipt output so
    # a bad id is always a clean usage error, never a half-finished run.
    rows = {}
    if args.sources:
        rows = load_sources_rows(args.sources)
        for rid in all_ids:
            if rid not in rows:
                usage_error(f"row {rid} not found in {args.sources}")

    bad = 0
    total = 0
    receipts = []  # (seat, rec, body_path, status)

    for rj in sorted(fetch_root.glob("*/receipts.jsonl")):
        seat_dir = rj.parent
        seat = seat_dir.name
        try:
            lines = rj.read_text(encoding="utf-8", errors="replace").splitlines()
        except OSError as exc:
            print(f"FETCH {seat}/receipts.jsonl MISSING read-error:{exc}")
            bad += 1
            continue
        for lineno, line in enumerate(lines, 1):
            if not line.strip():
                continue
            total += 1
            try:
                rec = json.loads(line)
            except json.JSONDecodeError:
                print(f"FETCH {seat}/<line {lineno}> BAD_JSON")
                bad += 1
                continue
            status, label, detail, bpath = verify_receipt(
                seat, lineno, rec, seat_dir
            )
            suffix = f" {detail}" if detail else ""
            print(f"FETCH {seat}/{label} {status}{suffix}")
            if status != "ok":
                bad += 1
            receipts.append(
                {
                    "seat": seat,
                    "rec": rec if isinstance(rec, dict) else {},
                    "body_path": bpath,
                    "status": status,
                }
            )

    # SOURCES.md row joins — only receipts whose body verified count as credit.
    unreceipted = 0
    row_matches = {}
    if args.sources:
        verified = [e for e in receipts if e["status"] == "ok"]
        for rid in all_ids:
            anchor = rows[rid]["anchor"]
            urls = rows[rid]["urls"]
            matched = []
            for entry in verified:
                rec = entry["rec"]
                sha = rec.get("sha256")
                if isinstance(sha, str) and sha and sha in anchor:
                    matched.append(entry)
                    continue
                if rec.get("url") in urls or rec.get("final_url") in urls:
                    matched.append(entry)
            row_matches[rid] = matched
        for rid in join_ids:
            matched = row_matches[rid]
            state = "receipted" if matched else "UNRECEIPTED"
            if not matched:
                unreceipted += 1
            print(f"ROW {rid} {state}")

    # Quote checks
    quote_bad = 0
    for rid, text in quotes:
        matched = row_matches.get(rid, [])
        if not matched:
            print(f"QUOTE {rid} UNRECEIPTED")
            quote_bad += 1
            continue
        needle = text.encode("utf-8")
        found = False
        for entry in matched:
            bpath = entry["body_path"]
            if bpath is None or not bpath.is_file():
                continue
            try:
                if needle in bpath.read_bytes():
                    found = True
                    break
            except OSError:
                continue
        state = "ok" if found else "NOT_FOUND"
        if not found:
            quote_bad += 1
        print(f"QUOTE {rid} {state}")

    ok = total - bad
    print(
        f"SUMMARY receipts={total} ok={ok} bad={bad} "
        f"rows={len(join_ids)} unreceipted={unreceipted} "
        f"quotes={len(quotes)} quote_bad={quote_bad}"
    )
    sys.exit(1 if (bad or unreceipted or quote_bad) else 0)


if __name__ == "__main__":
    main()
