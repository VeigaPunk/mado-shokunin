#!/usr/bin/env python3
"""C2 counter: differential mutations of the clause h/i/j delta against the positive-control clone."""
import difflib
import os
import subprocess
import sys

LANE = "/home/vgpnk/Projects/shokunin/mado-shokunin"
CTR = LANE + "/quality/counters/c2-r45-monitor-entry.py"
BASE = "0c89478af821a6424c9ac922eafe02e39630cf4f"
SRC = open(CTR, encoding="utf-8").read()
CLONE = sys.argv[1]
OUT = "/fast/scratch/hyaku/mado-r45/SimpContract"

MUT = [
    ("C1-unused-params",
     "def host_census(new_ids, reg_rev, gates, receipts_raw, lines):",
     "def host_census(gates, receipts_raw, lines):",
     "    h_ok, census_lines = host_census(new_ids, reg_rev, gates, receipts_raw, lines)",
     "    h_ok, census_lines = host_census(gates, receipts_raw, lines)"),
    ("C2-refresh-decimal", 'r"float\\s+m_refreshRate\\s*=\\s*([0-9]+(?:\\.[0-9]+)?);"',
     'r"float\\s+m_refreshRate\\s*=\\s*([0-9]+);"', None, None),
    ("C3-search-after",
     '    after = mon[mon.index("std::round(m_scale * %s.0)" % k[0]):]\n'
     '    n = re.search(r"for \\(size_t i = 1; i < ([0-9]+); \\+\\+i\\)", after)',
     '    n = re.search(r"for \\(size_t i = 1; i < ([0-9]+); \\+\\+i\\)", mon)', None, None),
    ("C4-j-notdigit", r'(?:-(\d+))?(?!\d)" % re.escape(rname))', r'(?:-(\d+))?" % re.escape(rname))',
     None, None),
    ("C5-gl0-not-none", 'if i in receipts_raw and gl and gl[0] is not None and len(gl) == 1:',
     'if i in receipts_raw and gl and len(gl) == 1:', None, None),
    ("C6-i-rows-guard", "        if rows and len(rows[0]) == 11:", "        if len(rows[0]) == 11:",
     None, None),
    ("C7-j-raw-none", '    cl["j"] = int(raw is not None and surfaces_ok(repo, rev, text, name))',
     '    cl["j"] = int(surfaces_ok(repo, rev, text, name))', None, None),
    ("C8-h-len-guard",
     "    if len(r) != 1 or len(t) != 1 or len(k) != 1 or len(p) != 1:\n        return False, []\n",
     "", None, None),
]


def run(path):
    p = subprocess.run([sys.executable, "-I", path, "--repo", CLONE, "--rev", "HEAD", "--base", BASE],
                       capture_output=True, text=True)
    return p.returncode, p.stdout, p.stderr


rc0, out0, err0 = run(CTR)
print("baseline rc=%d last=%r" % (rc0, out0.strip().splitlines()[-1]))
for tag, old, new, old2, new2 in MUT:
    src = SRC
    for o, n in ((old, new), (old2, new2)):
        if o is None:
            continue
        if src.count(o) != 1:
            print("%-20s BADPATTERN count=%d for %r" % (tag, src.count(o), o[:60]))
            src = None
            break
        src = src.replace(o, n)
    if src is None:
        continue
    path = os.path.join(OUT, "ctr-%s.py" % tag)
    open(path, "w").write(src)
    rc, out, err = run(path)
    same = (rc, out) == (rc0, out0)
    print("%-20s rc=%d same_stdout=%s %s" % (tag, rc, same,
          "" if same else "first-diff=" + repr(next((l for l in difflib.unified_diff(
              out0.splitlines(), out.splitlines(), lineterm="", n=0) if l.startswith(("-", "+"))
              and not l.startswith(("---", "+++"))), "?"))[:140]))
    if err and not err0:
        print("   stderr=%r" % err.strip().splitlines()[-1][:140])
