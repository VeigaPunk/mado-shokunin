#!/usr/bin/env python3
"""Falsify26 - C1 uniqueness/population falsification probe.

Independently measures, at pinned base 85d57a818c3707397e21c840b6498b105ba798aa:
  P1. population per c1-r51-ledger.py population() rules vs ledger rows (match/extra/missing)
  P2. row-path uniqueness: exact, emphasis-stripped, whitespace-stripped, ./-stripped,
      slash-collapsed, case-folded
  P3. self-pointer presence in production ledger pointer cells (quality/tool-ledger.md)
  P4. frozen control controls/c1-do-nothing.md: which defect classes it exhibits
"""
import re, subprocess, sys, unicodedata
from collections import Counter

LANE = "/home/vgpnk/Projects/shokunin/mado-shokunin"
REV = "85d57a818c3707397e21c840b6498b105ba798aa"
LEDGER_REL = "quality/tool-ledger.md"
EMPHASIS = "`*_ \t"

def git(*args):
    return subprocess.run(["git", "-C", LANE] + list(args),
                          capture_output=True, check=True).stdout

def listing(rev):
    out = git("ls-tree", "-r", "--name-only", rev)
    return [p for p in out.decode("utf-8", "surrogateescape").splitlines() if p]

def population(paths):
    pop = []
    for path in paths:
        if "__pycache__" in path or path.endswith((".pyc", ".pyo")):
            continue
        if path.startswith("tools/"):
            pop.append(path)
            continue
        for root in ("quality/counters/", "quality/"):
            if not path.startswith(root):
                continue
            rest = path[len(root):]
            if rest and "/" not in rest and rest.endswith(".py") and not rest.startswith("."):
                pop.append(path)
            break
    return sorted(set(pop))

def parse_rows(text):
    rows, fenced = [], False
    for raw in text.splitlines():
        line = raw.strip()
        if line.startswith(("```", "~~~")):
            fenced = not fenced
            continue
        if fenced or not line.startswith("|"):
            continue
        cells = [c.strip() for c in line.strip("|").split("|")]
        first = cells[0].strip(EMPHASIS) if cells else ""
        if not first or "/" not in first or first.startswith(":") or set(first) <= set("-: "):
            continue
        rows.append({"path": first,
                     "raw_path_cell": cells[0] if cells else "",
                     "desc": cells[1] if len(cells) > 1 else "",
                     "pointer": " | ".join(cells[2:]) if len(cells) > 2 else ""})
    return rows

def norm_variants(p):
    yield "exact", p
    yield "emphasis-stripped", p.strip(EMPHASIS)
    yield "ws-collapsed", re.sub(r"\s+", "", p)
    yield "dot-slash", re.sub(r"^\./", "", p)
    yield "slash-collapsed", re.sub(r"/{2,}", "/", p)
    yield "case-folded", p.casefold()
    yield "nfkc", unicodedata.normalize("NFKC", p)

files = listing(REV)
pop = population(files)
ledger = git("show", f"{REV}:{LEDGER_REL}").decode("utf-8", "surrogateescape")
rows = parse_rows(ledger)

print("== P1 population vs ledger rows ==")
print("population_size=%d ledger_rows=%d" % (len(pop), len(rows)))
row_paths = [r["path"] for r in rows]
extra = sorted(set(row_paths) - set(pop))
missing = sorted(set(pop) - set(row_paths))
print("extra_rows_not_in_population=%d %s" % (len(extra), extra[:5]))
print("missing_population_files=%d %s" % (len(missing), missing[:5]))

print("\n== P2 uniqueness under normalizations ==")
for name, keyfn in [
    ("exact", lambda p: p),
    ("emphasis-stripped", lambda p: p.strip(EMPHASIS)),
    ("whitespace-removed", lambda p: re.sub(r"\s+", "", p)),
    ("leading-./-stripped", lambda p: re.sub(r"^\./", "", p)),
    ("slash-collapsed", lambda p: re.sub(r"/{2,}", "/", p)),
    ("case-folded", lambda p: p.casefold()),
    ("NFKC", lambda p: unicodedata.normalize("NFKC", p)),
]:
    c = Counter(keyfn(p) for p in row_paths)
    dups = {k: v for k, v in c.items() if v > 1}
    print("norm=%-22s duplicate_keys=%d %s" % (name, len(dups), dict(list(dups.items())[:5])))

print("\n== P2b raw-path-cell anomalies ==")
anom = [(r["raw_path_cell"], r["path"]) for r in rows
        if r["raw_path_cell"].strip(EMPHASIS) != r["path"]
        or r["raw_path_cell"] != r["raw_path_cell"].strip()
        or "\t" in r["raw_path_cell"]]
print("cells_needing_strip=%d %s" % (len(anom), anom[:5]))
nonascii = [r["path"] for r in rows if not r["path"].isascii()]
print("non-ascii row paths=%d %s" % (len(nonascii), nonascii[:5]))

print("\n== P2c distinct population members colliding under normalization ==")
for name, keyfn in [("case-folded", lambda p: p.casefold()),
                    ("NFKC", lambda p: unicodedata.normalize("NFKC", p))]:
    c = Counter(keyfn(p) for p in pop)
    coll = {k: sorted(p for p in pop if keyfn(p) == k) for k, v in c.items() if v > 1}
    print("pop-collision norm=%s count=%d %s" % (name, len(coll), dict(list(coll.items())[:5])))

print("\n== P3 self-pointers in production ledger ==")
self_rows = [r["path"] for r in rows
             if LEDGER_REL in r["pointer"] or "tool-ledger.md" in r["pointer"]]
print("rows_pointing_at_ledger=%d %s" % (len(self_rows), self_rows[:10]))

print("\n== P4 frozen control defect classes ==")
ctrl_path = f"{LANE}/.ufo/waves/round-52/controls/c1-do-nothing.md"
ctrl = open(ctrl_path, encoding="utf-8").read()
crows = parse_rows(ctrl)
cpaths = [r["path"] for r in crows]
cdups = {k: v for k, v in Counter(cpaths).items() if v > 1}
print("control_rows=%d" % len(crows))
print("control_duplicate_paths=%s" % cdups)
print("control_self_pointer_rows=%s" % [r["path"] for r in crows
      if "tool-ledger" in r["pointer"] or LEDGER_REL in r["pointer"]])
generic = [r["path"] for r in crows
           if re.search(r"generic|pointer to this ledger", r["desc"], re.I)]
print("control_generic_desc_rows=%s" % generic)
print("control_descs=%s" % [r["desc"] for r in crows])
print("control_pointer_tokens=%s" % [re.findall(r"`([^`]+)`", r["pointer"]) for r in crows])
