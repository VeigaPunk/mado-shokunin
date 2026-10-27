import os, re, sys
R = "/home/vgpnk/Projects/shokunin/mado-shokunin"
OUT = os.path.join(R, ".ufo/waves/round-48/w1/ExecD2Receipt/receipts")
REPORT = os.path.join(R, ".ufo/waves/round-48/w1/ExecD2Receipt.md")
def text(p): return open(p, encoding="utf-8", errors="replace").read()
rep = text(REPORT)
revs = {"60edb66e": ("60edb66e2f1cb90acc6e9442fc93ded0ca42d750", 18371, 115),
        "d40189c9": ("d40189c924e01dc1cbe290474eb4256d343590d4", 19969, 128),
        "579f694b": ("579f694b45c797a9c39761fdb4f9e0a1b71b3585", 19969, 128)}
ok = bad = 0
def chk(name, cond):
    global ok, bad
    if cond: ok += 1
    else: bad += 1; print("FAIL", name)
for short, (rev, files, findings) in revs.items():
    p = os.path.join(OUT, "session-material-%s.txt" % short)
    t = text(p)
    line = "SESSION_MATERIAL: files=%d findings=%d rev=%s" % (files, findings, rev)
    chk("receipt has measured line " + short, line in t)
    chk("report has measured line " + short, line in rep or ("| %d | **%d** |" % (files, findings)) in rep)
    chk("report cites rev " + short, rev in rep)
    chk("three repeat summaries " + short, t.count("run=1 rc=") == 1 and t.count("run=3 rc=") == 1)
chk("claim literal in report", "findings=128 at the tip (115 at base)" in rep)
chk("claim literal located in receipt", "findings=128" in text(os.path.join(OUT, "claim-and-gate-identity.txt")) and "(115 at base)" in text(os.path.join(OUT, "claim-and-gate-identity.txt")))
chk("gate blob in report", "9d60e4c1ad251816e93184100bf1be05c649cd63" in rep)
chk("gate blob in receipt", "9d60e4c1ad251816e93184100bf1be05c649cd63" in text(os.path.join(OUT, "claim-and-gate-identity.txt")))
chk("worktree sha256 in receipt", "889f8f057bf04fc76ed93dd7ee86e3b0bd9fc1dca3a6bfb712c672da4646e3fb" in text(os.path.join(OUT, "claim-and-gate-identity.txt")))
newp = text(os.path.join(OUT, "new-finding-pairs.txt"))
chk("13 new pairs", "# total pairs: 13; gone: 0" in newp)
chk("four R1/R2/R3 counts", "      4 R1_CLIENT_DUMP" in newp and "      5 R2_PROC_TABLE" in newp and "      4 R3_MONITOR_IDENT" in newp)
clone = text(os.path.join(OUT, "clone-crosscheck.txt"))
chk("clone toplevel asserted", "/fast/scratch/hyaku/mado-r48/ExecD2Receipt/clone" in clone)
chk("clone rc lines x3", clone.count("EXIT rc=1") == 3)
cwd = text(os.path.join(OUT, "cwd-form.txt"))
chk("cwd-form equality x2", cwd.count("VERDICT cwd-form == absolute-form") == 2)
carriers = text(os.path.join(OUT, "new-carriers-relation.txt"))
chk("shared carrier blob", "9103bbdc86789578cb41ab6cbbd645181d96c229" in carriers)
lc = text(os.path.join(OUT, "claim-literal-and-filecounts.txt"))
chk("file counts", "60edb66e .ufo_files=18371" in lc and "d40189c9 .ufo_files=19969" in lc and "579f694b .ufo_files=19969" in lc)
# no matched session-material value leaked: gate emits none, and the seat printed none
FINDING_RE = re.compile(r'^FINDING file=\S+ rule=(R1_CLIENT_DUMP|R2_PROC_TABLE|R3_MONITOR_IDENT|R4_HOME_LISTING) count=\d+ detail=.+$')
META_RE = re.compile(r'^(#|\$ |EXIT rc=\d+|REPEAT |run=[123] rc=\d+|SESSION_MATERIAL(_RULES)?:|$)')
bad_lines = [ln for ln in text(os.path.join(OUT, "session-material-d40189c9.txt")).splitlines()
             if not (FINDING_RE.match(ln) or META_RE.match(ln))]
chk("every receipt line is a FINDING/meta line (no payload text)", not bad_lines)
print("VERIFY ok=%d failed=%d" % (ok, bad))
sys.exit(0 if bad == 0 else 1)
