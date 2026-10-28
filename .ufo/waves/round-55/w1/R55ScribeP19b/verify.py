#!/usr/bin/env python3
# R55ScribeP19b seat verifier: proves base is a byte prefix of after.md, after.md = base + block.md,
# every Q row equals frozen-tables.json c3.q, and every Q quote equals the stripped pin line. Writes verify.txt.
import hashlib
import json
import os
import re
import subprocess
import sys

LANE = "/home/vgpnk/Projects/shokunin/mado-shokunin"
SEAT = os.path.join(LANE, ".ufo/waves/round-55/w1/R55ScribeP19b")
BASE_REV = "3b55b6e91e40f455dd56b2985e4ffc087ada92d5"
ENTRY = "corpus/knowledge/hyprland-synthetic-dispatch-r52-errata-r53.md"

out = []
ok = True


def check(name, cond, detail=""):
    global ok
    ok = ok and bool(cond)
    out.append("%s %s%s" % ("PASS" if cond else "FAIL", name, (" " + detail) if detail else ""))


base = subprocess.run(["git", "-C", LANE, "show", BASE_REV + ":" + ENTRY], check=True, capture_output=True).stdout
after = open(os.path.join(SEAT, "after.md"), "rb").read()
block = open(os.path.join(SEAT, "block.md"), "rb").read()
tables = json.load(open(os.path.join(LANE, ".ufo/waves/round-55/frozen-tables.json"), encoding="utf-8"))
c3 = tables["c3"]

check("base_sha256", True, hashlib.sha256(base).hexdigest() + " bytes=%d" % len(base))
check("prefix_identical", after.startswith(base), "after_bytes=%d" % len(after))
check("after_is_base_plus_block", after == base + block, "block_bytes=%d" % len(block))
text = after.decode("utf-8")

pin_bytes = open(os.path.join(LANE, c3["pin"]), "rb").read()
pin_sha = hashlib.sha256(pin_bytes).hexdigest()
check("pin_sha256", pin_sha == c3["pin_sha256"], pin_sha)
pin_lines = pin_bytes.decode("utf-8").split("\n")

check("heading_correction_round55", re.search(r"^## .*Correction \(round 55\)", text, re.M) is not None)

row_re = re.compile(r"^\| (Q\d\d) \| Hyprland-ConfigActions\.cpp:(\d+) \| `([^`|]*)` \|$", re.M)
found = row_re.findall(text)
ids = [f[0] for f in found]
check("q_row_count", len(found) == 13 and len(set(ids)) == 13, "found=%d unique=%d" % (len(found), len(set(ids))))
for q in c3["q"]:
    matches = [f for f in found if f[0] == q["id"]]
    if len(matches) != 1:
        check("rows:" + q["id"], False, "matches=%d" % len(matches))
        continue
    _, line, quote = matches[0]
    frozen_ok = int(line) == q["line"] and quote == q["quote"]
    pin_ok = pin_lines[int(line) - 1].strip() == quote
    check("rows:" + q["id"], frozen_ok, "line=%s" % line)
    check("pin_quote:" + q["id"], pin_ok, "pin_line=%d" % int(line))

p23 = [l for l in text.split("\n") if l.startswith("| P23 | ")]
check("p23_row_present", len(p23) == 1, "count=%d" % len(p23))
if len(p23) == 1:
    cells = [c.strip() for c in p23[0].strip().strip("|").split(" | ")]
    check("p23_supersedes_P19", len(cells) >= 2 and cells[1] == "P19", "supersedes=%s" % (cells[1] if len(cells) > 1 else "?"))
    prop = cells[2] if len(cells) > 2 else ""
    needles = ["m_passPressed", "== 1", "== 0", "PRESSED", "RELEASED"]
    for n in needles:
        check("p23_has:" + n, n in prop)
    check("p23_has:else_or_other", any(s in prop for s in ["otherwise", "any other", "else"]))
    check("p23_pin_anchor", "Hyprland-ConfigActions.cpp:1554-1576" in p23[0])

readme_path = os.path.join(LANE, "corpus/README.md")
readme_hit = any("hyprland-synthetic-dispatch-r52-errata-r53.md" in l and "P23" in l for l in open(readme_path, encoding="utf-8").read().split("\n"))
out.append("INFO readme_p23_line_in_corpus_README=%s (integration surface; L1 edits it, seat does not)" % readme_hit)

out.append("VERDICT %s" % ("OK" if ok else "FAIL"))
text_out = "\n".join(out) + "\n"
open(os.path.join(SEAT, "verify.txt"), "w", encoding="utf-8").write(text_out)
sys.stdout.write(text_out)
sys.exit(0 if ok else 1)
