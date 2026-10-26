#!/usr/bin/env python3
"""Verify CritSkillLicence's quotes and receipts.

  python3 -I .ufo/waves/round-44/w2/CritSkillLicence/receipts/verify.py

Checks, all against files in the lane (writes nothing):
  1. every quotes.tsv row's needle is a substring of the stated line, is <= 25 words, and its
     computed `grep -n -F` output appears in receipts/greps.txt;
  2. the attacked SKILL.md wording is the landed text at the data commit e4678921 and at HEAD;
  3. the landed tool bytes equal the frozen reference c1/ctl-ref-tool-v2.py.txt;
  4. receipts/fixtures.txt carries the expected identical= markers and the 5 NOT_COMPARED runs.
Exit 0 with `VERIFY: ... fails=0`, else prints each failure and exits 1.
"""
import hashlib
import os
import subprocess
import sys

LANE = "/home/vgpnk/Projects/shokunin/mado-shokunin"
SEAT = os.path.join(LANE, ".ufo/waves/round-44/w2/CritSkillLicence")
fails = []


def fail(msg):
    fails.append(msg)


# 1. quotes
rows = []
for ln in open(os.path.join(SEAT, "receipts/quotes.tsv"), encoding="utf-8"):
    ln = ln.rstrip("\n")
    if not ln or ln.startswith("#"):
        continue
    path, line, needle = ln.split("\t")
    rows.append((path, int(line), needle))

greps = open(os.path.join(SEAT, "receipts/greps.txt"), encoding="utf-8").read()
for path, line, needle in rows:
    full = os.path.join(LANE, path)
    try:
        lines = open(full, encoding="utf-8", errors="replace").read().splitlines()
        text = lines[line - 1]
    except (OSError, IndexError) as e:
        fail(f"{path}:{line}: unreadable ({e})")
        continue
    if needle not in text:
        fail(f"{path}:{line}: needle not on line: {needle!r}")
    if len(needle.split()) > 25:
        fail(f"{path}:{line}: needle longer than 25 words ({len(needle.split())})")
    header = f"## {path}:{line}  needle={needle!r}"
    block = greps.split(header)
    if len(block) != 2:
        fail(f"{path}:{line}: greps.txt has no block header")
    elif not any(g.startswith(f"{line}:") and needle in g
                 for g in block[1].splitlines()):
        fail(f"{path}:{line}: computed grep -n line missing from greps.txt")

# 2. attacked wording is the landed wording (data commit and tip)
for rev in ("e4678921", "HEAD"):
    got = subprocess.run(["git", "-C", LANE, "show", f"{rev}:SKILL.md"],
                         capture_output=True, text=True)
    if got.returncode != 0:
        fail(f"git show {rev}:SKILL.md failed")
        continue
    lines = got.stdout.splitlines()
    for n, needle in ((280, "Hyprland set its box to the monitor box"),
                      (281, "the box is the workspace work area"),
                      (289, "is false for a pseudo-tiled client"),
                      (291, 'read TILED as "not floating" only')):
        if len(lines) < n or needle not in lines[n - 1]:
            fail(f"{rev}:SKILL.md:{n}: expected landed wording absent: {needle!r}")

# 3. landed tool == frozen reference
tool = os.path.join(LANE, "tools/mado-geometry.py")
ref = os.path.join(LANE, ".ufo/waves/round-44/c1/ctl-ref-tool-v2.py.txt")
ht = hashlib.sha256(open(tool, "rb").read()).hexdigest()
hr = hashlib.sha256(open(ref, "rb").read()).hexdigest()
if ht != hr:
    fail(f"tool sha {ht} != reference {hr}")

# 4. fixtures receipt
fx = open(os.path.join(SEAT, "receipts/fixtures.txt"), encoding="utf-8").read()
for marker in [
    "A_tiled identical=True", "B_agree identical=True", "C_differ identical=True",
    "D_unmapped_fs identical=True", "E_nonmatch_fs identical=True", "J_nomatch_fs identical=True",
    "M_fs_bool identical=True", "N_fs_zero identical=True", "O_fs3 identical=True",
    "P_badsize_fs_only identical=True",
    "F_fs_only identical=False", "G_fs_plus_differ identical=False", "H_max_only identical=False",
    "I_fs_coincide identical=False", "K_fs_plus_tiled identical=False",
    "L_badsize_plus_fs identical=False",
]:
    if marker not in fx:
        fail(f"fixtures.txt missing marker: {marker}")
if fx.count("verdict=NOT_COMPARED") != 5:
    fail(f"fixtures.txt NOT_COMPARED count {fx.count('verdict=NOT_COMPARED')} != 5")
if "I_fs_coincide" in fx and "r43 rc=0" not in fx:
    fail("fixtures.txt lacks the round-43 AGREE (rc 0) of I_fs_coincide")

print(f"VERIFY: quotes={len(rows)} tool_sha={ht[:12]} fails={len(fails)}")
for f in fails:
    print(f"  FAIL {f}")
sys.exit(1 if fails else 0)
