#!/usr/bin/env python3
"""Build the synthetic good repo S under --work: alternates onto the lane, commit on 3b55b6e adding block+README+tables. Prints sha."""
import json, os, subprocess, sys
LANE = "/home/vgpnk/Projects/shokunin/mado-shokunin"
BASE = "3b55b6e91e40f455dd56b2985e4ffc087ada92d5"
ENTRY = "corpus/knowledge/hyprland-synthetic-dispatch-r52-errata-r53.md"
S = sys.argv[1]
os.makedirs(S)
def g(*a, inp=None):
    return subprocess.run(["git", "-C", S] + list(a), input=inp, capture_output=True, check=True).stdout
g("init", "-q")
assert os.path.realpath(g("rev-parse", "--show-toplevel").decode().strip()) == os.path.realpath(S)
open(S + "/.git/objects/info/alternates", "w").write(LANE + "/.git/objects\n")
ft = subprocess.run(["git", "-C", LANE, "cat-file", "blob", "54dacbd843d64ba744cd3f1bdc2ec622e5010039:.ufo/waves/round-55/frozen-tables.json"], capture_output=True, check=True).stdout
q = json.loads(ft)["c3"]["q"]
base = subprocess.run(["git", "-C", LANE, "cat-file", "blob", BASE + ":" + ENTRY], capture_output=True, check=True).stdout
rd = subprocess.run(["git", "-C", LANE, "cat-file", "blob", BASE + ":corpus/README.md"], capture_output=True, check=True).stdout
blk = "\n## Correction (round 55)\n\nAppend-only; supersedes P19 only.\n\n| ID | Supersedes | Proposition | Source row | Pin:anchor | Quote | Support |\n|---|---|---|---|---|---|---|\n"
blk += "| P23 | P19 | `Actions::pass` sends modifier state, then if `m_passPressed == 1` sends PRESSED, if `m_passPressed == 0` sends RELEASED, otherwise (any other value) it sends PRESSED then RELEASED. | S371 | Hyprland-ConfigActions.cpp:1554-1576 | `see Q01-Q13` | direct |\n\n"
blk += "| ID | Pin:line | Quote |\n|---|---|---|\n"
for x in q:
    blk += "| %s | %s:%d | `%s` |\n" % (x["id"], x["pin"], x["line"], x["quote"])
entry = base + blk.encode()
old = b"append-only correction to P16\xe2\x80\x93P18"
assert old in rd
rd2 = rd.replace(old, old + b"; round 55 adds P23 superseding P19")
def put(path, data, ob=None):
    h = g("hash-object", "-w", "--stdin", inp=data).decode().strip()
    g("update-index", "--add", "--cacheinfo", "100644,%s,%s" % (h, path))
g("read-tree", BASE)
put(ENTRY, entry); put("corpus/README.md", rd2); put(".ufo/waves/round-55/frozen-tables.json", ft)
t = g("write-tree").decode().strip()
sha = g("-c", "user.name=ctl", "-c", "user.email=ctl@ctl", "commit-tree", t, "-p", BASE, "-m", "synthetic good", inp=b"").decode().strip()
g("update-ref", "refs/heads/good", sha)
print(sha)
