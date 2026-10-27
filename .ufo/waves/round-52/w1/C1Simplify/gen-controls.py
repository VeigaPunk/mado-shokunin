#!/usr/bin/env python3
"""Regenerate C1Simplify's ledger controls from the base revision (deterministic, read-only git)."""
import re, subprocess
LANE = "/home/vgpnk/Projects/shokunin/mado-shokunin"
REV = "85d57a818c3707397e21c840b6498b105ba798aa"
GEN = "Accountability row for this tracked instrument ledger."

def git(*a):
    return subprocess.run(("git", "-C", LANE) + a, capture_output=True).stdout

rows, fenced = [], False
for line in git("show", REV + ":quality/tool-ledger.md").decode().splitlines():
    s = line.strip()
    if s.startswith(("```", "~~~")):
        fenced = not fenced
        continue
    if fenced or not s.startswith("|"):
        continue
    c = [x.strip() for x in s.strip("|").split("|")]
    f = c[0].strip("`*_ ")
    if f and "/" in f and not f.startswith(":") and len(c) == 3:
        rows.append((f, c[1], c[2].strip("`")))

def write(name, fn, header):
    open(name, "w").write(header + "\n\n" + "\n".join(
        "| `%s` | %s | `%s` |" % fn(p, d, ptr) for p, d, ptr in rows) + "\n")

write("control-B-row-selfpointer.md", lambda p, d, x: (p, GEN, p), "# B: self-pointers + repeated generic descriptions")
write("control-C-ledger-selfpointer.md", lambda p, d, x: (p, d, "quality/tool-ledger.md"), "# C: every row points at the ledger itself")
write("control-D-generic-desc.md", lambda p, d, x: (p, GEN, x), "# D: production pointers, repeated generic descriptions")
write("control-E-one-selfpointer.md", lambda p, d, x: (p, d, p if p == "tools/mado-anims.py" else x), "# E: one self-pointer only")
forged = []
for i, (p, d, x) in enumerate(rows):
    body = git("show", REV + ":" + p).decode("utf-8", "replace")
    m = re.search(r'"""(.*?)"""', body, re.S)
    ws = [w.lower() for w in re.findall(r"[A-Za-z][A-Za-z0-9_]+", m.group(1) if m else body[:400])][:4]
    forged.append("| `%s` | Generic accountability note %d %s. | `%s` |" % (p, i, " ".join(ws), x))
open("control-F3-forged.md", "w").write("# F3: distinct generic descriptions, each copying a word pair from its instrument\n\n" + "\n".join(forged) + "\n")
# single-defect mutations of the production ledger (control E above is one of these shapes)
def mutate(name, idx, desc=None, ptr=None):
    out = []
    for i, (path, d, x) in enumerate(rows):
        if i == idx:
            d = desc if desc is not None else d
            x = ptr if ptr is not None else x
        out.append("| `%s` | %s | `%s` |" % (path, d, x))
    open(name, "w").write("# production ledger with exactly one defect\n\n" + "\n".join(out) + "\n")

mutate("mut-dup.md", -1)  # placeholder, replaced below
lines = open("mut-dup.md").read().splitlines()
dup = [l for l in lines if l.startswith("| `")][5]
lines.insert(7, dup)
open("mut-dup.md", "w").write("\n".join(lines) + "\n")
mutate("mut-emptydesc.md", 3, desc="—")
mutate("mut-badpointer.md", 7, desc="Static resolver of a Hyprland config tree's bind table; prints binds.",
       ptr="corpus/nonexistent.md")
# G: legitimate row whose description names the ledger it reads (false-positive probe for an
# all-cell self scan; the accountability pointer itself is a proper document)
out = []
for path, d, x in rows:
    if path == "quality/check-tool-ledger.py":
        d = "Reads `quality/tool-ledger.md` and reports each instrument's accountability row."
    out.append("| `%s` | %s | `%s` |" % (path, d, x))
open("control-G-legit-ledger-reader.md", "w").write("# G: one legitimate row names the ledger in its description\n\n" + "\n".join(out) + "\n")
# H: minimal forged description -- a prediction id plus filler, one row only
out = []
for path, d, x in rows:
    if path == "quality/counters/c1-r47-terminal.py":
        d = "PRED-C1-r47 does things."
    out.append("| `%s` | %s | `%s` |" % (path, d, x))
open("control-H-minimal-forgery.md", "w").write("# H: one row's description is a prediction id plus filler\n\n" + "\n".join(out) + "\n")
print("wrote 5 controls + 3 mutations + G + H, %d rows each" % len(rows))
