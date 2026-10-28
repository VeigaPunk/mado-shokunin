#!/usr/bin/env python3
"""Split the proposed (NOT frozen) clause C1-X into its two sub-checks and report each separately.
  C1X-id:    each K/H proposition shares >=2 identifier tokens (or all, if the quote has fewer) with its quote
  C1X-dissim: no two propositions have difflib ratio >= 0.6
usage: python3 -I c1x_split.py <REPO> <REV>
"""
import difflib, json, re, subprocess, sys

repo, rev = sys.argv[1], sys.argv[2]
ENTRY = "corpus/knowledge/hyprland-keyboard-repeat-numlock-r55.md"
TABLES = ".ufo/waves/round-55/frozen-tables.json"
TOKEN_RE = re.compile(r"[A-Za-z_][A-Za-z0-9_]{2,}")


def blob(path):
    return subprocess.run(["git", "-C", repo, "cat-file", "blob", f"{rev}:{path}"],
                          capture_output=True, check=True).stdout.decode("utf-8", "replace")


def cells(line):
    s = line.strip()[1:-1]
    s = re.sub(r"\\\|", "\x00", s)
    return [p.strip().replace("\x00", "|") for p in s.split("|")]


T = json.loads(blob(TABLES))["c1"]
frozen = {x["id"]: x for x in T["k"] + T["h"]}
rows = {}
for line in blob(ENTRY).split("\n"):
    if line.startswith("|"):
        c = cells(line)
        if c and re.fullmatch(r"[KH]\d{2}", c[0]) and len(c) == 5:
            rows[c[0]] = c

id_bad = []
for rid, c in rows.items():
    qtok = set(TOKEN_RE.findall(frozen[rid]["quote"]))
    ptok = {t for t in qtok if re.search(r"\b" + re.escape(t) + r"\b", c[1])}
    if len(ptok) < min(2, len(qtok)):
        id_bad.append(rid)

dis_bad = set()
ids = sorted(rows)
for i in range(len(ids)):
    for j in range(i + 1, len(ids)):
        r = difflib.SequenceMatcher(None, rows[ids[i]][1], rows[ids[j]][1]).ratio()
        if r >= 0.6:
            dis_bad.update([ids[i], ids[j]])
print(f"C1X-id: {'ok' if not id_bad else 'bad'} rows_failing={len(id_bad)}/{len(rows)} "
      f"first={','.join(sorted(id_bad)[:6]) or 'none'}")
print(f"C1X-dissim: {'ok' if not dis_bad else 'bad'} rows_failing={len(dis_bad)}/{len(rows)}")
