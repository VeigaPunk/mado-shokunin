#!/usr/bin/env python3
"""check102-textprojection.py - candidate criterion 102 (a text rendering is total).

Question answered: does every id of the structured result appear exactly once
in the text rendering of the same run, and does the text's own count line agree
with the structured count?

Round-48 N4: `.ufo/waves/round-48/receipts/v2/c2v2-revc2counter-summary.json`
holds 98 variants while `c2v2-revc2counter-matrix.txt` renders 96 rows and its
trailer still prints `variants 98`. Both artifacts are internally consistent
(the text's rows are correct), so criteria 37 and 78 - which recompute inside
one artifact - cannot see it.

Reads only; writes nothing.

Usage:
  check102-textprojection.py --json FILE [--json-key NAME] --text FILE
                             [--text-id-pattern REGEX] [--text-id-group N]
                             [--trailer-pattern REGEX]
Exit: 0 total projection, 1 dropped/duplicate id, 2 usage / unreadable.

Declared limit: it compares ids only. A text row carrying the wrong verdict
for a present id is criteria 78/87's subject, not this one. `--json-key`
defaults to `name`; a structured file that is a bare list of strings is read
as ids directly.
"""
import argparse
import json
import re
import sys


def load_ids(path, key):
    try:
        data = json.load(open(path, "r"))
    except (OSError, ValueError) as exc:
        print("CHECK102: error=json-unreadable %s: %s" % (path, exc))
        return None
    if isinstance(data, list):
        if all(isinstance(item, str) for item in data):
            return list(data)
        ids = [item.get(key) for item in data if isinstance(item, dict)]
    elif isinstance(data, dict):
        rows = data.get(key if isinstance(data.get(key), list) else "results", [])
        ids = [row.get(key) for row in rows if isinstance(row, dict)]
    else:
        return None
    return [i for i in ids if i]


def main():
    parser = argparse.ArgumentParser(add_help=True)
    parser.add_argument("--json", required=True)
    parser.add_argument("--json-key", default="name")
    parser.add_argument("--text", required=True)
    parser.add_argument("--text-id-pattern",
                        default=r'^([A-Za-z0-9][A-Za-z0-9_.-]+)\s+.*\brc[= ]-?\d+')
    parser.add_argument("--text-id-group", type=int, default=1)
    parser.add_argument("--trailer-pattern", default=r'^\s*variants\s+(\d+)\s*$')
    args = parser.parse_args()

    ids = load_ids(args.json, args.json_key)
    if ids is None:
        return 2
    try:
        lines = open(args.text, "r", errors="replace").read().splitlines()
    except OSError as exc:
        print("CHECK102: error=text-unreadable %s: %s" % (args.text, exc))
        return 2

    row_re = re.compile(args.text_id_pattern)
    seen, order = {}, []
    for idx, line in enumerate(lines, 1):
        match = row_re.search(line)
        if not match:
            continue
        ident = match.group(args.text_id_group)
        seen[ident] = seen.get(ident, 0) + 1
        order.append((idx, ident))

    missing = [i for i in ids if i not in seen]
    extra = [i for i in seen if i not in ids]
    dupes = [i for i, n in seen.items() if n > 1]
    trailer = None
    trailer_re = re.compile(args.trailer_pattern)
    for line in reversed(lines):
        match = trailer_re.search(line)
        if match:
            trailer = int(match.group(1))
            break

    for idx, ident in order:
        if ident in dupes:
            print("TEXT_DUPLICATE text=%s:%d id=%s rows=%d" % (args.text, idx, ident, seen[ident]))
    for ident in missing:
        print("TEXT_DROPPED id=%s json=%s text=%s" % (ident, args.json, args.text))
    for ident in extra:
        print("TEXT_EXTRA id=%s json=%s text=%s" % (ident, args.json, args.text))

    bad = len(missing) + len(dupes)
    if trailer is not None:
        print("TRAILER_COUNT text=%d json=%d" % (trailer, len(ids)))
        if trailer != len(ids):
            bad += 1
    else:
        print("TRAILER_COUNT text=absent json=%d" % len(ids))
        bad += 1
    print("CHECK102: json_ids=%d text_rows=%d missing=%d extra=%d dupes=%d verdict=%s"
          % (len(ids), len(seen), len(missing), len(extra), len(dupes),
             "FAIL" if bad else "OK"))
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
