# The three mutations applied to scratch clones (att2/k1, att2/p23, att2/c5) before committing; run once per clone dir.
# Each asserts the anchor text occurs exactly once. Counters were then run unchanged on the attack commits.
import glob, os, sys
def one(pattern):
    m = glob.glob(pattern); assert len(m) == 1, (pattern, m); return m[0]
E = "corpus/knowledge/hyprland-keyboard-repeat-numlock-r55.md"
X = "corpus/knowledge/hyprland-synthetic-dispatch-r52-errata-r53.md"
os.chdir(sys.argv[1])
k1 = one("k1.*"); p23 = one("p23.*"); c5 = one("c5.*")
p = os.path.join(k1, E); t = open(p, encoding="utf-8").read()
old = "applyConfigToKeyboard reads the repeat rate through getDeviceInt with device key repeat_rate and global fallback input:repeat_rate."
assert t.count(old) == 1
t = t.replace(old, "Placeholder proposition text, long enough to clear the forty character floor, asserts nothing.")
open(p, "w", encoding="utf-8").write(t)
p = os.path.join(p23, X); t = open(p, encoding="utf-8").read()
old = "When `m_passPressed == 0`, a non-mouse key sends a keyboard key RELEASED"
assert t.count(old) == 1, t.count(old)
t = t.replace(old, "When `m_passPressed == 0`, a non-mouse key sends a keyboard key PRESSED")
open(p, "w", encoding="utf-8").write(t)
p = os.path.join(c5, X); lines = open(p, encoding="utf-8").read().split("\n")
p19 = [l for l in lines if l.startswith("| P19 |")]; p23l = [i for i,l in enumerate(lines) if l.startswith("| P23 |")]
assert len(p19) == 1 and len(p23l) == 1
prop19 = p19[0].split("|")[3].strip()
cells = lines[p23l[0]].split("|"); cells[3] = " " + prop19 + " "
lines[p23l[0]] = "|".join(cells)
open(p, "w", encoding="utf-8").write("\n".join(lines))
print("mutations applied")
