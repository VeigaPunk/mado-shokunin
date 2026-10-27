#!/usr/bin/env python3
"""Turn warm.py's warm-results.txt into receipts/agree.txt (case, ours, theirs, cold, state).

Usage: python3 make_agree.py <seat dir>   (from the scratch dir the harness ran in)
"""
import hashlib
import re
import sys

SEAT = sys.argv[1]
PIN = "/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-47/fetch/xdg-terminal-exec"
sha = lambda p: hashlib.sha256(open(p, "rb").read()).hexdigest()

blocks, cur = [], None
for ln in open("warm-results.txt"):
    ln = ln.rstrip("\n")
    m = re.match(r"^(W-\d+\S*) class=(\S+) args=(.*)$", ln)
    if m:
        cur = {"id": m.group(1), "cls": m.group(2), "args": m.group(3), "verdict": "?"}
        blocks.append(cur)
        continue
    for key, pat in (("oracle", r"^  oracle rc=(-?\d+) out=(.*)$"), ("tool", r"^  tool   rc=(-?\d+) out=(.*)$"),
                     ("cold", r"^  cold   rc=(-?\d+) out=(.*)$"),
                     ("state", r"state=(\S+) want=(\S+) verdict=(\S+) differs_from_cold=(\S+)")):
        m = re.search(pat, ln)
        if m:
            cur[key] = m.groups()
    if ln.startswith("  VERDICT"):
        cur["verdict"] = ln.split()[1]

out = ["# ExecRefCacheA - warm-cache differential: case, ours (draft tool), theirs (pinned xdg-terminal-exec v0.14.3)",
       "# tool sha256 %s" % sha(SEAT + "/mado-terminal.py"), "# pin  sha256 %s" % sha(PIN),
       "# judge: the pin is primed cold (--print-cmd, wait for the background save) in each twin tree, the trees are",
       "# mutated identically, then the pin runs again (warm) on tree o and the tool runs `print` on tree t.",
       "# $ROOT = the tree root; `cold` is the same tree with the cache removed (proof the warm answer differs).", ""]
agree = sum(1 for b in blocks if b.get("verdict") == "agree")
for b in blocks:
    out.append("%s class=%s args=%s" % (b["id"], b["cls"], b["args"]))
    out.append("  theirs rc=%s out=%s" % b.get("oracle", ("?", "?")))
    out.append("  ours   rc=%s out=%s" % b.get("tool", ("?", "?")))
    out.append("  cold   rc=%s out=%s" % b.get("cold", ("?", "?")))
    st = b.get("state")
    if st:
        out.append("  cache=%s (want %s) differs_from_cold=%s" % (st[0], st[1], st[3]))
    out.append("  %s" % b.get("verdict"))
out += ["", "TOTAL %d cases, %d agree, %d differ; %d cases where the warm answer differs from the cold one"
        % (len(blocks), agree, len(blocks) - agree,
           sum(1 for b in blocks if b.get("state") and b["state"][3] == "True"))]
open(SEAT + "/receipts/agree.txt", "w").write("\n".join(out) + "\n")
print(out[-1])
