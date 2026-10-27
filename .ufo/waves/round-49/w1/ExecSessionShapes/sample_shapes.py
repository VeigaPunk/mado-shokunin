#!/usr/bin/env python3
"""Characterise the v3-only findings at a revision, masked.

Usage: sample_shapes.py GATE REV [LIMIT]

Prints, per new rule, the finding count, the files by round, and up to LIMIT
masked sample lines. Every value is masked before printing: a home path
becomes ``/home/U``, an ``ls -l`` owner/group column pair becomes ``USER
USER``, and a cache field value becomes ``<value>``. The account name is never
read from the environment and never printed.
"""
import importlib.util
import os
import re
import sys

GATE = sys.argv[1]
REV = sys.argv[2]
LIMIT = int(sys.argv[3]) if len(sys.argv) > 3 else 3
REPO = sys.argv[4] if len(sys.argv) > 4 else os.environ.get("LANE", "")

spec = importlib.util.spec_from_file_location("csm", GATE)
csm = importlib.util.module_from_spec(spec)
spec.loader.exec_module(csm)

ACCOUNT = os.environ.get("MASK_ACCOUNT", "")


def mask(line):
    line = re.sub(r"/home/[A-Za-z0-9._-]+", "/home/U", line)
    line = re.sub(r"^([-dlbcps][rwxsStT-]{9}[+.]?[\s@.]+\d+\s+)\S+\s+\S+",
                  r"\1USER USER", line)
    line = re.sub(r"^(--[a-z-]+=).*$", r"\1<value>", line)
    if ACCOUNT:
        line = line.replace(ACCOUNT, "USER")
    return line[:110]


def main():
    sha = csm.resolve_rev(REPO, REV)
    entries = csm.list_tree(REPO, sha, (".",))
    order, seen = [], set()
    for blob, _path in entries:
        if blob not in seen:
            seen.add(blob)
            order.append(blob)
    data = dict(csm.iter_blobs(REPO, order))
    account = csm.invoking_account()

    found = {csm.R7: [], csm.R8: [], csm.R9: []}
    for blob, path in entries:
        text = csm.decode(data.get(blob, b""))
        if text is None:
            continue
        rules = {rule: (count, detail)
                 for rule, count, detail in csm.scan_blob(text.encode(),
                                                          csm.DEFAULT_HOME_LIMIT,
                                                          (), account)}
        for rule in found:
            if rule in rules:
                found[rule].append((path, rules[rule][0], rules[rule][1], text))

    for rule in (csm.R7, csm.R8, csm.R9):
        rows = found[rule]
        print("== %s files=%d" % (rule, len(rows)))
        areas = {}
        for path, _count, _detail, _text in rows:
            parts = path.split("/")
            key = "/".join(parts[:3]) if len(parts) > 2 else path
            areas[key] = areas.get(key, 0) + 1
        for key in sorted(areas):
            print("   %-34s %d" % (key, areas[key]))
        for path, count, detail, text in rows[:LIMIT]:
            print("   -- %s count=%d %s" % (path, count, detail))
            shown = 0
            for line in text.splitlines():
                entry = line.strip()
                hit = (csm.HOME_GREP_RE.match(entry) or csm.HOME_HEADER_RE.match(entry)
                       or csm.HOME_DIAG_RE.match(entry))
                row = csm.MODE_ROW_RE.match(entry)
                cache = csm.CACHE_FIELD_RE.match(line)
                if not (hit or (rule == csm.R8 and row and account in row.groups()[:2])
                        or (rule == csm.R7 and row and csm.HOME_ANY_RE.search(row.group(3)))
                        or (rule == csm.R9 and cache)):
                    continue
                print("      %s" % mask(entry))
                shown += 1
                if shown >= 2:
                    break


main()
