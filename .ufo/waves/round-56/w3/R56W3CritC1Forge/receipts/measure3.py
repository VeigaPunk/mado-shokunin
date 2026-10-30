#!/usr/bin/env python3
"""R56W3CritC1Forge: how tight is the content leg on the tip entry? num-vacuity and tok-cardinality."""
import json
import re
import subprocess

W = "/fast/scratch/hyaku/mado-r56/R56W3CritC1Forge/W2"
REV = "0f3a54361a9824484d0801679ceb1fd8ac7c32e1"
TOKEN_RE = re.compile(r"[A-Za-z_][A-Za-z0-9_]{3,}")
RUN_RE = re.compile(r"(?<![A-Za-z0-9_])[0-9]+(?![A-Za-z0-9_])")
ROW_RE = re.compile(r"^\| ([KHE]\d\d) \|")


def show(path, rev=REV):
    return subprocess.run(["git", "-C", W, "show", "%s:%s" % (rev, path)],
                          capture_output=True).stdout.decode("utf-8")


base = show("corpus/knowledge/hyprland-config-autoreload-r56.md")
tables = json.loads(show(".ufo/waves/round-56/frozen-tables-v2.json"))
c1 = tables["c1"]
allrows = []
for line in base.split("\n"):
    m = ROW_RE.match(line)
    if m:
        allrows.append((m.group(1), line[2:-2].split(" | ")))
K = {rid: c for rid, c in allrows}
KH = [r["id"] for r in c1["k"] + c1["h"]]

print("=== num-leg vacuity on the honest tip entry ===")
withdigits = [(rid, RUN_RE.findall(K[rid][1])) for rid in KH if RUN_RE.findall(K[rid][1])]
print("  K/H propositions carrying a digit run: %d of 33 -> %s" % (len(withdigits), withdigits))
print("  => the num leg can never fire on the honest entry; it only fires on a MUTATION.")
print()

print("=== tok-leg cardinality: how many quote identifiers must the proposition keep? ===")
rowsout = [(rid, sorted(set(TOKEN_RE.findall(K[rid][4][1:-1])))) for rid in KH]
one = [(r, t) for r, t in rowsout if len(t) <= 2]
print("  rows whose frozen quote has <=2 identifier tokens (>=4 chars): %d of 33 -> %s" % (len(one), [(r, t) for r, t in one]))
print("  rows whose frozen quote has exactly 1 identifier token: %d -> %s"
      % (len([r for r, t in rowsout if len(t) == 1]), [r for r, t in rowsout if len(t) == 1]))
print("  minimum identifier tokens any quote supplies: %d" % min(len(t) for _, t in rowsout))
print()

print("=== echo leg coverage on the honest tip entry ===")
short = [rid for rid in KH if len(K[rid][4][1:-1]) < 30]
echoed = [rid for rid in KH if len(K[rid][4][1:-1]) >= 30 and K[rid][4][1:-1] in K[rid][1]]
print("  quotes shorter than ECHO_MIN 30 (echo leg OFF for that row): %d -> %s" % (len(short), short))
print("  honest propositions that DO echo their quote: %d -> %s" % (len(echoed), echoed))
print("  => on the honest tip entry every row satisfies the echo leg trivially.")
print()

print("=== row-count accounting ===")
ids = [r for r, _ in allrows]
print("  rows in the entry: %d (K=%d H=%d E=%d)" % (len(ids), sum(1 for i in ids if i[0] == "K"),
                                                    sum(1 for i in ids if i[0] == "H"), sum(1 for i in ids if i[0] == "E")))
print("  the frozen content leg grades 33 (30 K + 3 H); the 9 E rows are outside it")
print()

print("=== E-row src bindings vs the source: line ===")
src_line = base.split("\n")[0]
print("  source line: %s" % src_line[:420])
for rid in [i for i in ids if i[0] == "E"]:
    print("   %s src=%s pin=%s" % (rid, K[rid][2], K[rid][3]))
print("  literal S-ids on the source: line: %s"
      % sorted(set(re.findall(r"(?<![A-Za-z0-9])S[0-9]{3}(?![0-9])", src_line))))
print("  => 'S392-S395' yields only S392 and S395 as literal tokens; S393 and S394 are NOT on the provenance line.")
