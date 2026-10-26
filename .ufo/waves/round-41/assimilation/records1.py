#!/usr/bin/env python3
"""Round-41 records, step 1: QUALITY criteria, SKILL.md and PROVINCE.md inserts, lesson."""
import re
L = "/home/vgpnk/Projects/shokunin/mado-shokunin/"
W2 = L + ".ufo/waves/round-41/w2/"

def rd(p): return open(p).read()
def wr(p, s): open(p, "w").write(s)

# ---------------------------------------------------------------- QUALITY.md
crit = rd(W2 + "ScrQualityFinal/criteria.md")
items = {}
for m in re.finditer(r"^(69|7[0-5])\. .*$", crit, re.M):
    items[int(m.group(1))] = m.group(0)
assert sorted(items) == [69, 70, 71, 72, 73, 74, 75], sorted(items)
c76 = ("76. A round that mines a proposal from `considerthese/<date>.md` re-derives, from the lane's own bytes, every number its mining note repeats, "
       "and the note carries the command and its output beside each re-derived number; a number taken on trust is written `relayed:` with the spot-check path that carries it, "
       "because the reflection is a pointer, not evidence. Check: run the note's commands at the reflection's own base and tip pins; a count the command does not print is "
       "corrected in the note or marked `relayed:`. Shown able to fail: `considerthese/2026-10-25.md:5` reports that `corpus/knowledge/` \"gained eight entries\" over rounds 32-37, "
       "while `git ls-tree -r --name-only 57a772b corpus/knowledge | wc -l` prints `43` and the same command at `f6e3247` prints `52` - nine files added, zero deleted. "
       "Ground: `considerthese/2026-10-25.md` proposal 5 (2026-10-25). (lesson: lessons/round-41.md#mistakes M41-18)")
q = rd(L + "corpus/QUALITY.md").rstrip("\n") + "\n"
for n in range(69, 76):
    q += "\n" + items[n] + "\n"
q += "\n" + c76 + "\n"
wr(L + "corpus/QUALITY.md", q)

# ---------------------------------------------------------------- SKILL.md / PROVINCE.md
ins = rd(W2 + "ScrSkillFinal/insert.md")
blocks = re.findall(r"```\n(.*?)\n```", ins, re.S)
# order in the file: probe row, subsection, decision row, province row (the first fenced blocks)
assert len(blocks) >= 4, len(blocks)
probe, sub, decision, prov = blocks[0], blocks[1], blocks[2], blocks[3]
assert probe.startswith("| `python3 tools/mado-globals.py"), probe[:40]
assert sub.startswith("### Advertised Wayland globals")
assert decision.startswith("| Which Wayland globals")
assert prov.startswith("| `tools/mado-globals.py`")
sk = rd(L + "SKILL.md").split("\n")
assert sk[155].startswith("| Bar runtime facts"), sk[155][:40]
assert sk[220].startswith("| `grim -t ppm -`") and sk[221] == "", (sk[220][:30], sk[221])
# apply bottom-up so anchors stay valid: subsection after 222 (index 221), probe after 221, decision after 156
sk[222:222] = sub.split("\n") + [""]
sk[221:221] = [probe]
sk[156:156] = [decision]
wr(L + "SKILL.md", "\n".join(sk))
pv = rd(L + "PROVINCE.md").split("\n")
assert pv[29].startswith("| `tools/mado-anims.py`"), pv[29][:40]
pv[30:30] = [prov]
wr(L + "PROVINCE.md", "\n".join(pv))
print("records1: quality/skill/province ok")
