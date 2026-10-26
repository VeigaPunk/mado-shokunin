#!/usr/bin/env python3
"""CritC2V2Forgery (w2): systematic quote-attribution audit of the landed entry.

Every double-quoted span on every unfenced line of the DATA entry is checked
against the normalized text of the receipts the Gate lines bind, using the
counter's OWN normalizers (imported from the frozen counter).  A span that sits
in no cited receipt, or only in another id's receipt, is a data defect.
Read-only.
"""
import importlib.util
import os
import re
import subprocess
import sys

LANE = "/home/vgpnk/Projects/shokunin/mado-shokunin"
COUNTER = "/tmp/tmp.sBh6GeCxAU/c2-v2.py"
DATA = "07f2641696b5ac73de1404ea737a9f27e9819aa1"
ENV = {k: v for k, v in os.environ.items() if not k.startswith("GIT_")}


def git_show(path):
    p = subprocess.run(["git", "-C", LANE, "show", "%s:%s" % (DATA, path)],
                       capture_output=True, env=ENV)
    return p.stdout if p.returncode == 0 else None


spec = importlib.util.spec_from_file_location("c2", COUNTER)
c2 = importlib.util.module_from_spec(spec)
spec.loader.exec_module(c2)

ENTRY = "corpus/knowledge/hyprland-focus-grab-r41.md"
entry = git_show(ENTRY).decode()
lesson = git_show("corpus/lessons/round-41.md").decode()

gate = {}
for line in lesson.splitlines():
    m = re.match(r'^GATE (S\d{3,}) receipt=(\S+) sha256=([0-9a-f]{64}) quote="(.+)"$', line)
    if m:
        gate[m.group(1)] = (m.group(2), git_show(m.group(2)), m.group(4))
norm = {i: c2.norm_receipt(blob) for i, (p, blob, q) in gate.items()}
for i, (p, blob, q) in sorted(gate.items()):
    print("bound %s %-38s %6d B quote-in-receipt=%s" % (
        i, os.path.basename(p), len(blob), re.sub(r"\s+", " ", q) in norm[i]))

fenced = False
absent, wrong, total = [], [], 0
for n, line in enumerate(entry.splitlines(), 1):
    if re.match(r"^\s{0,3}(```|~~~)", line):
        fenced = not fenced
        continue
    if fenced:
        continue
    ids = re.findall(r"\b(S\d{3,})\b", line)
    for span in re.findall(r'"([^"\n]{4,})"', line):
        total += 1
        q = re.sub(r"\s+", " ", span).strip()
        where = [i for i in ids if q in norm[i]]
        other = [i for i in gate if i not in ids and q in norm[i]]
        if where:
            continue
        (wrong if other else absent).append((n, span[:90], ids, other))
print("\nquoted spans on entry lines: %d" % total)
print("spans in a cited receipt of their own line's id: %d" % (total - len(absent) - len(wrong)))
print("spans only in ANOTHER id's receipt: %d" % len(wrong))
for n, s, ids, other in wrong:
    print("  WRONG-RECEIPT entry:%d ids=%s other=%s span=%r" % (n, ids, other, s))
print("spans in NO cited receipt: %d" % len(absent))
for n, s, ids, other in absent:
    print("  ABSENT entry:%d ids=%s span=%r" % (n, ids, s))
sys.exit(0 if not absent and not wrong else 1)
