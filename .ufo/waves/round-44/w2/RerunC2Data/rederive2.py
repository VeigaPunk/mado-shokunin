#!/usr/bin/env python3
"""Second, separate re-derivation pass: registry cell arithmetic, clause b header
window, distinctness, README/ADMIT checks. Does not import the counter."""
import os
import re
import subprocess
import sys

REPO = "/home/vgpnk/Projects/shokunin/mado-shokunin"
REV = "e46789213830597348fe96a351ae004d10587385"
BASE = "6a1a90528fe533cadee506a9fa3e9d13d15cc41f"
ENTRY = "corpus/knowledge/hyprland-gkeep-size-request-r44.md"
IDS = ["S164", "S298", "S299", "S300", "S301"]


def git(*a):
    env = {k: v for k, v in os.environ.items() if not k.startswith("GIT_")}
    p = subprocess.run(["git", "-C", REPO, *a], capture_output=True, env=env)
    if p.returncode:
        return None
    return p.stdout


def reg(rev):
    src = git("show", "%s:corpus/SOURCES.md" % rev).decode()
    inside, rows = False, {}
    for n, l in enumerate(src.split("\n"), 1):
        if l.startswith("## "):
            inside = l.strip() == "## Registry"
            continue
        if inside:
            m = re.match(r"^ {0,3}\|\s*(S\d{3,})\s*\|", l)
            if m:
                rows.setdefault(m.group(1), []).append(
                    (n, [c.strip() for c in l.strip().split("|")[1:-1]]))
    return rows


r_rev, r_base = reg(REV), reg(BASE)
out = []
add = out.append
for i in IDS:
    rv = r_rev.get(i, [])
    rb = r_base.get(i, [])
    add("%s: rev_rows=%d base_rows=%d" % (i, len(rv), len(rb)))
    if len(rv) != 1:
        continue
    n, cells = rv[0]
    add("  rev line=%d cells=%d" % (n, len(cells)))
    if len(cells) != 11:
        continue
    if rb:
        _, bc = rb[0]
        add("  base cells=%d cells1-9 equal=%s" % (len(bc), bc[:9] == cells[:9]))
        bu = {x.strip() for x in re.split(r"[,;]", bc[10]) if x.strip() and x.strip() != "\u2014"}
        ru = {x.strip() for x in re.split(r"[,;]", cells[10]) if x.strip()}
        add("  base used_by (%d) subset of rev (%d)=%s  missing=%s" % (
            len(bu), len(ru), bu <= ru, sorted(bu - ru)))
        add("  base used_by entry present in rev=%s" % (ENTRY in ru))
    else:
        add("  NEW row opened=%s location_has_slash_dot=%s" % (
            cells[8], "/" in cells[1].split()[-1] and "." in cells[1].split()[-1]))

entry = git("show", "%s:%s" % (REV, ENTRY)).decode()
lines = entry.split("\n")
add("\nclause b header window (raw first 20 lines):")
for n, l in enumerate(lines, 1):
    if re.match(r"^(source|verified-at|recheck):", l):
        add("  line %d in_window=%s: %s" % (n, n <= 20, l[:90]))
srcs = [l.split()[1] for n, l in enumerate(lines[:20], 1) if l.startswith("source:")]
add("  distinct source ids=%s count=%d" % (srcs, len(set(srcs))))
va = [l for l in lines if l.startswith("verified-at:")]
rc = [l for l in lines if l.startswith("recheck:")]
add("  verified-at count=%d value=%r" % (len(va), va[0][12:].strip() if va else None))
add("  recheck count=%d value=%r" % (len(rc), rc[0][8:].strip()[:40] if rc else None))
tokens = set(re.findall(r"\b[Ss]\d{3,}\b", "\n".join(lines)))
add("  all S-tokens=%s ghosts=%s" % (sorted(tokens), sorted(tokens - set(srcs))))

readme = git("show", "%s:corpus/README.md" % REV).decode()
add("\nREADME index rows (column 0, '| `knowledge/<name>`'):")
rows = [n for n, l in enumerate(readme.split("\n"), 1)
        if re.match(r"^\| `knowledge/%s`" % re.escape(os.path.basename(ENTRY)), l)]
add("  count=%d lines=%s" % (len(rows), rows))

add("\nGate quote distinctness across cited ids (path/sha/quote):")
lesson = git("show", "%s:corpus/lessons/round-44.md" % REV).decode()
g = {}
for n, l in enumerate(lesson.split("\n"), 1):
    m = re.match(r'^GATE (S\d+) receipt=(\S+) sha256=([0-9a-f]{64}) quote="(.*)"$', l)
    if m:
        g[m.group(1)] = m.groups()[1:]
paths = [g[i][0] for i in IDS]
shas = [g[i][1] for i in IDS]
quotes = [g[i][2] for i in IDS]
add("  unique paths=%s unique shas=%s unique quotes=%s" % (
    len(set(paths)) == 5, len(set(shas)) == 5, len(set(quotes)) == 5))
add("  paths all under fetch/=%s" % all(p.startswith(".ufo/waves/round-44/fetch/") for p in paths))
# gate section containment
sec_lines, inside = set(), False
for l in lesson.split("\n"):
    if l.startswith("## "):
        inside = l.strip() == "## Gate"
        continue
    if inside:
        sec_lines.add(l)
add("  all five GATE lines inside '## Gate'=%s" % all(
    any(re.match(r'^GATE %s ' % i, l) for l in sec_lines) for i in IDS))

print("\n".join(out))
sys.exit(0)
