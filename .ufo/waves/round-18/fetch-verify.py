#!/usr/bin/env python3
"""fetch-verify.py — verify mado round-18 fetch receipts and row credit.

Walks <fetch-root>/*/receipts.jsonl (default: the fetch/ directory next to
this script). For every receipt line of schema mado-fetch-receipt-v1 it
re-checks that the body file exists beside receipts.jsonl, that its byte
count matches "bytes" and that its sha256 matches "sha256".

Per receipt prints exactly one line:

    FETCH <seat>/<body> ok|DIGEST_ONLY|BAD_SHA|BAD_BYTES|MISSING|BAD_SCHEMA|BAD_JSON

A body that re-hashes prints "ok" whatever its http_status: a non-200 receipt
stays a valid storage record (it may witness an absence check) and appends
" http_status=<n>", but it never credits a SOURCES row.

Digest-only retention. <fetch-root>/RETENTION.json may hold
{"seat","body","retain"} entries, as a top-level list or as {"entries": [...]}.
A missing body whose (seat, body) entry says "digest-only" prints DIGEST_ONLY
instead of MISSING; a receipt field "retain": "digest-only" is honoured the
same way. DIGEST_ONLY is not a bad receipt, but its body cannot be re-hashed
or quote-checked.

Conflict rule. When two receipts for the same url (or the same final_url)
both carry http_status 200 and different sha256 values, one line per URL is
printed:

    CONFLICT <url> sha256=<digest>,<digest>[,<digest>]

and the run exits 1. A row whose first source URL is conflicted is CONFLICT,
never receipted.

SOURCES.md row credit (--sources --rows):

    ROW <id> receipted|UNRECEIPTED <reason>|CONFLICT|host/no-url

A row is credited only by a receipt that
  (a) carries http_status 200 and a verified (or digest-only) body,
  (b) has a sha256 equal to a full 64-hex digest in the row's anchor cell
      (or starting with a >=16-hex digest written there), and
  (c) has a url or final_url equal to the first https URL of the row's
      source cell.
URL equality alone, anchor-sha equality alone, and a non-200 body never
credit. A row whose source cell has no https URL is a host/file row
("host/no-url"): the fetch join does not apply to it and it does not fail
the run.

Quote check (repeatable --quote 'S0NN=<text>'):

    QUOTE <id> ok|NOT_FOUND|UNRECEIPTED|DIGEST_ONLY

<text> (bytes, UTF-8) is searched only in 200 bodies of receipts that credit
the row; non-200 bodies are never searched. Quote row ids are checked even
when not listed in --rows.

Exit: 0 when every receipt verified, there is no URL conflict, every listed
row is receipted (or host/no-url) and every quote is found; 1 on any bad
receipt, URL conflict, uncredited row, or missing/unevaluable quote; 2 on
usage errors.
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
DIGEST_RE = re.compile(r"(?<![0-9a-fA-F])[0-9a-fA-F]{16,64}(?![0-9a-fA-F])")
RETENTION_NAME = "RETENTION.json"


def usage_error(msg):
    print(f"fetch-verify: {msg}", file=sys.stderr)
    sys.exit(2)


def sha256_file(path):
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def load_retention(fetch_root):
    """Return the set of (seat, body) pairs retained as digest-only only."""
    path = fetch_root / RETENTION_NAME
    if not path.exists():
        return set()
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        usage_error(f"cannot read {path}: {exc}")
    entries = data.get("entries") if isinstance(data, dict) else data
    if not isinstance(entries, list):
        usage_error(f"{path}: expected a list of {{seat, body, retain}} entries")
    digest_only = set()
    for entry in entries:
        if not isinstance(entry, dict):
            continue
        seat = entry.get("seat")
        body = entry.get("body")
        if not isinstance(seat, str) or not isinstance(body, str):
            continue
        if entry.get("retain") != "digest-only":
            continue
        digest_only.add((seat, body))
        # SentinelFetchBodies names an uncommitted body "<slug>.nocommit".
        if body.endswith(".nocommit"):
            digest_only.add((seat, body[: -len(".nocommit")]))
    return digest_only


def is_digest_only(seat, body, rec, digest_only):
    if (seat, body) in digest_only:
        return True
    return rec.get("retain") == "digest-only"


def verify_receipt(seat, lineno, rec, seat_dir, digest_only):
    """Return (status, body_label, detail, body_path_or_None)."""
    if not isinstance(rec, dict) or rec.get("schema") != SCHEMA:
        return "BAD_SCHEMA", f"<line {lineno}>", "schema-mismatch", None
    body = rec.get("body")
    if not isinstance(body, str) or not body or "/" in body or body in (".", ".."):
        return "BAD_SCHEMA", f"<line {lineno}>", "bad-body-field", None
    bpath = seat_dir / body
    if not bpath.is_file():
        if is_digest_only(seat, body, rec, digest_only):
            return "DIGEST_ONLY", body, "", None
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
    """Parse the SOURCES.md registry table -> {row_id: {source, anchor}}."""
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
        rows[rid] = {
            "source": cells[2] if len(cells) > 2 else "",
            "anchor": cells[6] if len(cells) > 6 else "",
        }
    return rows


def first_source_url(source):
    """First https URL of the row's source cell, in written order."""
    for url in URL_RE.findall(source):
        return url.rstrip(").,;:!")
    return None


def anchor_digests(anchor):
    return [d.lower() for d in DIGEST_RE.findall(anchor)]


def digest_covers(sha, digests):
    """True when sha equals a 64-hex anchor digest or starts a shorter one."""
    if not isinstance(sha, str):
        return False
    sha = sha.lower()
    for digest in digests:
        if len(digest) == 64:
            if sha == digest:
                return True
        elif sha.startswith(digest):
            return True
    return False


def url_matches(rec, url):
    return rec.get("url") == url or rec.get("final_url") == url


def build_conflicts(receipts):
    """Map url/final_url -> sorted shas when two 200 receipts disagree."""
    groups = {}
    for entry in receipts:
        rec = entry["rec"]
        if entry["status"] not in ("ok", "DIGEST_ONLY"):
            continue
        if rec.get("http_status") != 200:
            continue
        sha = rec.get("sha256")
        if not isinstance(sha, str) or not sha:
            continue
        for url in {rec.get("url"), rec.get("final_url")}:
            if isinstance(url, str) and url:
                groups.setdefault(url, {}).setdefault(sha, set()).add(
                    entry["seat"]
                )
    return {
        url: sorted(shas)
        for url, shas in groups.items()
        if len(shas) > 1
    }


def credit_receipts(receipts, url, digests):
    """Receipts that satisfy status, anchor digest and first-URL equality."""
    out = []
    for entry in receipts:
        rec = entry["rec"]
        if entry["status"] not in ("ok", "DIGEST_ONLY"):
            continue
        if rec.get("http_status") != 200:
            continue
        if not url_matches(rec, url):
            continue
        if not digest_covers(rec.get("sha256"), digests):
            continue
        out.append(entry)
    return out


def uncredited_reason(receipts, url, digests):
    """One-token diagnosis for an UNRECEIPTED row, never a credit."""
    url_entries = [e for e in receipts if url_matches(e["rec"], url)]
    if not url_entries:
        return "no-url-receipt"
    ok_200 = [e for e in url_entries if e["rec"].get("http_status") == 200]
    if not ok_200:
        return "no-200"
    if not digests:
        return "no-anchor-digest"
    sha_200 = [e for e in ok_200 if digest_covers(e["rec"].get("sha256"), digests)]
    if not sha_200:
        return "sha-not-in-anchor"
    return "body-unverified"


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
        help="check <text> occurs in a 200 body that credits the row "
        "(repeatable)",
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

    digest_only = load_retention(fetch_root)

    bad = 0
    total = 0
    non200 = 0
    receipts = []  # dicts: seat, rec, body_path, status

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
                seat, lineno, rec, seat_dir, digest_only
            )
            if status == "ok" and isinstance(rec, dict):
                http_status = rec.get("http_status")
                if isinstance(http_status, int) and not isinstance(
                    http_status, bool
                ) and http_status != 200:
                    non200 += 1
                    detail = detail or f"http_status={http_status}"
            suffix = f" {detail}" if detail else ""
            print(f"FETCH {seat}/{label} {status}{suffix}")
            if status not in ("ok", "DIGEST_ONLY"):
                bad += 1
            receipts.append(
                {
                    "seat": seat,
                    "rec": rec if isinstance(rec, dict) else {},
                    "body_path": bpath,
                    "status": status,
                }
            )

    # URL conflicts: two 200 digests for one url/final_url are a tamper signal.
    conflicts = build_conflicts(receipts) if args.sources else {}
    for url, shas in sorted(conflicts.items()):
        print(f"CONFLICT {url} sha256={','.join(shas)}")

    # SOURCES.md row joins.
    unreceipted = 0
    row_matches = {}
    row_states = {}
    if args.sources:
        for rid in all_ids:
            source = rows[rid]["source"]
            anchor = rows[rid]["anchor"]
            first = first_source_url(source)
            if first is None:
                row_matches[rid] = []
                row_states[rid] = "host/no-url"
                continue
            if first in conflicts:
                row_matches[rid] = []
                row_states[rid] = "CONFLICT"
                continue
            digests = anchor_digests(anchor)
            matched = credit_receipts(receipts, first, digests)
            row_matches[rid] = matched
            if matched:
                row_states[rid] = "receipted"
            else:
                row_states[rid] = (
                    "UNRECEIPTED " + uncredited_reason(receipts, first, digests)
                )
        for rid in join_ids:
            state = row_states[rid]
            if state.startswith("UNRECEIPTED"):
                unreceipted += 1
            print(f"ROW {rid} {state}")

    # Quote checks: only bodies that are 200 and credit the row are searched.
    quote_bad = 0
    for rid, text in quotes:
        matched = row_matches.get(rid, [])
        if not matched:
            # A host row or a row that failed credit has no credited body.
            quote_bad += 1
            print(f"QUOTE {rid} UNRECEIPTED")
            continue
        bodies = [
            e for e in matched if e["status"] == "ok" and e["body_path"] is not None
        ]
        if not bodies:
            print(f"QUOTE {rid} DIGEST_ONLY")
            quote_bad += 1
            continue
        needle = text.encode("utf-8")
        found = False
        for entry in bodies:
            bpath = entry["body_path"]
            if not bpath.is_file():
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

    ok = sum(1 for e in receipts if e["status"] == "ok")
    digest_n = sum(1 for e in receipts if e["status"] == "DIGEST_ONLY")
    print(
        f"SUMMARY receipts={total} ok={ok} bad={bad} digest_only={digest_n} "
        f"non200={non200} conflicts={len(conflicts)} "
        f"rows={len(join_ids)} unreceipted={unreceipted} "
        f"quotes={len(quotes)} quote_bad={quote_bad}"
    )
    sys.exit(1 if (bad or conflicts or unreceipted or quote_bad) else 0)


if __name__ == "__main__":
    main()
