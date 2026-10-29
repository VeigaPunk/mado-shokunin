#!/usr/bin/env python3
"""Cross-check receipts/used-by-old-to-new.md against corpus/SOURCES.md cell 11 at R and PRE (read-only git)."""
import re, subprocess

L = "/home/vgpnk/Projects/shokunin/mado-shokunin"
R = "28fc86ac2359ec27406d8a2c63bef82ea6e947ed"
PRE = "323a69c9014da1cebece67bb111b70a5630f4a60"
ROWRE = re.compile(r"^ {0,3}\|\s*(S[0-9]{3,})\s*\|")


def show(rev, path):
    return subprocess.run(["git", "-C", L, "show", "%s:%s" % (rev, path)], capture_output=True, check=True,
                          env={"PATH": "/usr/bin:/bin", "HOME": "/fast/scratch/hyaku/mado-r56/R56W2CritC3Gaming/work",
                               "GIT_CONFIG_GLOBAL": "/dev/null", "GIT_CONFIG_NOSYSTEM": "1", "LC_ALL": "C"}).stdout.decode()


def cells(text):
    out = {}
    for ln in text.split("\n"):
        m = ROWRE.match(ln)
        if m:
            parts = ln.split("|")
            out[m.group(1)] = parts[11].strip()
    return out


def items(c):
    return [x.strip() for x in c.split(",") if x.strip() and x.strip() != "-"]


pre = cells(show(PRE, "corpus/SOURCES.md"))
post = cells(show(R, "corpus/SOURCES.md"))
rec = show(R, ".ufo/waves/round-56/receipts/used-by-old-to-new.md").split("\n")
rows = []
for ln in rec:
    if ln.startswith("| S"):
        f = [x.strip() for x in ln.strip().strip("|").split("|")]
        rows.append((f[0], f[1], f[2]))
print("receipt rows:", len(rows))
bad_old = [s for s, o, n in rows if items(o) != items(pre[s])]
bad_new = [s for s, o, n in rows if items(n) != items(post[s])]
print("receipt old cell != PRE registry cell 11 for:", bad_old)
print("receipt new cell != R registry cell 11 for:", bad_new)
added = sum(len(set(items(post[s])) - set(items(pre[s]))) for s, o, n in rows)
print("receipt-listed added used-by pairs:", added)
print("receipt-listed rows that are not in the registry diff:", [s for s, _, _ in rows if pre[s] == post[s]])
