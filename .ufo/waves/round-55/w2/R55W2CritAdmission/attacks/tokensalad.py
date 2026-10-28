import os, sys
D = sys.argv[1]
X = "corpus/knowledge/hyprland-synthetic-dispatch-r52-errata-r53.md"
p = os.path.join(D, X); lines = open(p, encoding="utf-8").read().split("\n")
idx = [i for i, l in enumerate(lines) if l.startswith("| P23 |")]
assert len(idx) == 1
cells = lines[idx[0]].split("|")
assert "Actions::pass" in cells[3]
cells[3] = " `m_passPressed == 1` `== 0` PRESSED RELEASED otherwise "
lines[idx[0]] = "|".join(cells)
open(p, "w", encoding="utf-8").write("\n".join(lines))
print("token-salad P23 written")
