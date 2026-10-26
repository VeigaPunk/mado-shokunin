#!/usr/bin/env python3
"""ScribeReportDraft — re-derive every number in draft.md from committed blobs and receipts.

Read-only: git plumbing (show/diff/ls-tree) plus reading files. Writes nothing but its own stdout.
Run:  python3 -I .ufo/waves/round-43/w2/ScribeReportDraft/verify.py
"""
import hashlib
import re
import subprocess
import sys
from pathlib import Path

LANE = Path("/home/vgpnk/Projects/shokunin/mado-shokunin")
BASE = "a35cfdfcdeb3bd42d1a2cd960faf22ceac1bef3f"
DATA = "1959770657f1f8665097c1aed4be6c1cbb07139f"
HEAD = "HEAD"
ROW = re.compile(r"^ {0,3}\|[ ]*S\d{3,}[ ]*\|")
fails = []


def git(*args):
    return subprocess.run(["git", "-C", str(LANE), *args], capture_output=True, text=True)


def blob(rev, path):
    r = git("show", f"{rev}:{path}")
    if r.returncode != 0:
        raise SystemExit(f"cannot read {rev}:{path}: {r.stderr.strip()}")
    return r.stdout


def check(name, got, want):
    ok = got == want
    print(f"{'PASS' if ok else 'FAIL'}  {name}: got={got!r} want={want!r}")
    if not ok:
        fails.append(name)


src_base = blob(BASE, "corpus/SOURCES.md")
src_data = blob(DATA, "corpus/SOURCES.md")
src_head = blob(HEAD, "corpus/SOURCES.md")

# 1-2 rows and ids
rows = lambda t: [ln for ln in t.splitlines() if ROW.match(ln)]
ids = lambda t: re.findall(r"^\| S(\d+)", t, re.M)
check("rows base", len(rows(src_base)), 226)
check("rows data", len(rows(src_data)), 234)
check("ids base", len(set(ids(src_base))), 226)
check("ids data", len(set(ids(src_data))), 234)
check("SOURCES identical at data and HEAD", src_data == src_head, True)

# 3 tiers (field 4)
def tiers(t):
    out = {}
    for ln in t.splitlines():
        if ln.startswith("| S"):
            cell = ln.split("|")[3].strip()
            out[cell] = out.get(cell, 0) + 1
    return out

tb, td = tiers(src_base), tiers(src_data)
check("tier code", (tb["code"], td["code"]), (101, 106))
check("tier own-work", (tb["own-work"], td["own-work"]), (24, 27))
for k in ("docs", "spec", "community", "paper", "dataset", "book"):
    check(f"tier {k} unchanged", tb[k], td[k])
check("tier sums", (sum(tb.values()), sum(td.values())), (226, 234))

# 4 knowledge entries
n = lambda rev, p: len([x for x in git("ls-tree", "-r", "--name-only", rev, p).stdout.splitlines() if x])
check("knowledge entries", (n(BASE, "corpus/knowledge/"), n(DATA, "corpus/knowledge/")), (59, 60))

# 5 SOURCES numstat and new ids
check("SOURCES numstat", git("diff", "--numstat", BASE, DATA, "--", "corpus/SOURCES.md").stdout.split()[:2], ["10", "2"])
new_ids = sorted({f"S{i}" for i in ids(src_data)} - {f"S{i}" for i in ids(src_base)})
check("new ids", new_ids, [f"S{i}" for i in range(290, 298)])

# 6 held rows: cells 1-10 identical, used-by gains one item
def row(t, sid):
    for ln in t.splitlines():
        if ln.startswith(f"| {sid} |"):
            return ln
    raise SystemExit(f"missing {sid}")

for sid in ("S155", "S158"):
    rb, rd = row(src_base, sid), row(src_data, sid)
    check(f"{sid} cells 1-10 identical", rb.split("|")[1:10], rd.split("|")[1:10])
    ub, ud = rb.split("|")[-2].strip(), rd.split("|")[-2].strip()
    check(f"{sid} used-by append", (ud, ud.startswith(ub + ", corpus/knowledge/hyprland-gkeep-geometry-r43.md")), (ud, True))

# 7 new-row cells
for i in range(290, 298):
    f = row(src_data, f"S{i}").split("|")
    check(f"S{i} status/opened", (f[8].strip(), f[9].strip()), ("mined", "2026-10-26"))
for i in range(290, 295):
    check(f"S{i} recheck", row(src_data, f"S{i}").split("|")[10].strip(), "on-release")
for i in range(295, 298):
    check(f"S{i} recheck", row(src_data, f"S{i}").split("|")[10].strip(), "2027-01-24")
check("used-by all new rows", {row(src_data, f"S{i}").split("|")[-2].strip() for i in range(290, 298)},
      {"corpus/knowledge/hyprland-gkeep-geometry-r43.md"})

# 8 README / QUALITY / lessons
check("README numstat", git("diff", "--numstat", BASE, DATA, "--", "corpus/README.md").stdout.split()[:2], ["10", "0"])
readme = blob(DATA, "corpus/README.md").splitlines()
check("README index row", any("hyprland-gkeep-geometry-r43" in ln and ln.startswith("| `knowledge/") for ln in readme[:75]), True)
check("README route heading line", next((i + 1 for i, ln in enumerate(readme) if ln.startswith("### Round-43 rule-size")), 0), 294)
check("README route open-items phrase present", "Still open: a live" in blob(DATA, "corpus/README.md")[:], True)
check("README no deletion", git("diff", "--numstat", BASE, DATA, "--", "corpus/README.md").stdout.split()[1], "0")

check("QUALITY numstat", git("diff", "--numstat", BASE, DATA, "--", "corpus/QUALITY.md").stdout.split()[:2], ["10", "0"])
qual = blob(DATA, "corpus/QUALITY.md")
check("QUALITY criteria 77-81", [bool(re.search(rf"^{i}\. ", qual, re.M)) for i in range(77, 82)], [True] * 5)

lesson = blob(DATA, "corpus/lessons/round-43.md")
check("lesson gates", len(re.findall(r"^GATE S", lesson, re.M)), 10)
check("lesson mistakes", len(re.findall(r"^\*\*M43-\d ", lesson, re.M)), 8)
check("lesson shown-able-to-fail labels", lesson.count("Shown able to fail:"), 8)
check("M43-2 self-report missing instrument", "Shown able to fail: not shown this round" in lesson, True)
check("M43-6 not yet a gate", "Not yet a gate (open)" in lesson, True)
check("lesson ADMIT", len(re.findall(r"^ADMIT ", lesson, re.M)), 1)
check("lesson REFUSE", len(re.findall(r"^REFUSE ", lesson, re.M)), 4)
# ledger: 11 candidate files across the 9 ledger rows (one row names -r14.md in shorthand)
ledger = lesson.split("## Assimilation ledger")[1].split("## Registry changes")[0]
files = set(re.findall(r"`(gkeep-[a-z0-9-]+|glyph-and-geometry-r31|\.\/)?(-r1[0-9])?\.md`", ledger))
full = {a + b for a, b in files if a}
check("ledger full-name files", len(full), 10)
check("ledger r14 shorthand", "`-r14.md`" in ledger, True)
check("ledger candidate files", len(full) + 1, 11)

# 9 receipts
R = LANE / ".ufo/waves/round-43/receipts"
c1 = (R / "c1-after-data.txt").read_text()
check("c1 verdict line", c1.strip().splitlines()[-2].split()[1], "fixtures=37/37")
check("c1 exit", c1.strip().splitlines()[-1], "exit=0")
c2 = (R / "c2-after-data.txt").read_text()
check("c2 summary", c2.strip().splitlines()[-2].split(":")[1].strip().split()[0], "admitted=1/1")
check("c2 clause line", [ln for ln in c2.splitlines() if "clauses=a" in ln][0].split()[-1], "admitted=1")
check("c2 exit", c2.strip().splitlines()[-1], "exit=0")
check("c2 v1 also met", "admitted=1/1" in (R / "c2-v1-after-data.txt").read_text(), True)
check("c2 base missed", "admitted=0/1" in (R / "c2-v2-before-base.txt").read_text(), True)
check("ctl-c1 tally", "controls=46" in (R / "ctl-c1.txt").read_text().splitlines()[0], True)
check("ctl-c1 reference", "(controls scoring TARGET_MET: 0 of 47; reference met: 1)" in (R / "ctl-c1.txt").read_text(), True)
check("ctl-c2 tally", (R / "ctl-c2.txt").read_text().strip().splitlines()[-2], "CTL_C2: controls=74 correct=74/74")
check("ctl-c2-v2 tally", (R / "ctl-c2-v2.txt").read_text().strip().splitlines()[-2], "CTL_C2: controls=74 correct=74/74")
check("ctl-c1 rev is base", "rev=" + BASE in (R / "ctl-c1.txt").read_text().splitlines()[0], True)
check("axis receipt rev is base", "rev=" + BASE in (R / "axis-base.txt").read_text(), True)
check("no axis-after-data receipt", sorted(p.name for p in R.glob("axis*")), ["axis-base.txt"])

# census set unchanged
strip = lambda t: [ln for ln in t.splitlines() if not ln.startswith("mado\tok")]
check("census set unchanged", strip((R / "census-before.txt").read_text()) == strip((R / "census-after-data.txt").read_text()), True)
check("census exit", (R / "census-after-data.txt").read_text().strip().splitlines()[-1], "exit=0")

# 10 tool identity + live run
sha = lambda p: hashlib.sha256(Path(p).read_bytes()).hexdigest()
tool = LANE / "tools/mado-geometry.py"
ref = LANE / ".ufo/waves/round-42/c1/ctl-ref-tool.py.txt"
check("tool sha == reference sha", sha(tool) == sha(ref), True)
check("tool sha value", sha(tool)[:8], "e3c2e471")
live = (R / "live-geometry-host.txt").read_text()
check("live verdict", "verdict=NO_MATCHING_CLIENT" in live and live.strip().endswith("exit=3"), True)

# 11 assimilation provenance
cnt = lambda rev: len(git("ls-tree", "-r", "--name-only", rev, ".ufo/waves/round-43/assimilation/").stdout.split())
check("assimilation files at data", cnt(DATA), 0)
check("assimilation files at 2a3707c", cnt("2a3707c"), 7)
check("data is ancestor of HEAD", git("merge-base", "--is-ancestor", DATA, "HEAD").returncode, 0)
check("corpus identical data..HEAD", git("diff", "--numstat", DATA, "HEAD", "--", "corpus/", "SKILL.md", "PROVINCE.md", "tools/", "quality/").stdout.splitlines(), ["7\t0\tSKILL.md"])
check("corpus files identical data..HEAD", git("diff", "--name-only", DATA, "HEAD", "--", "corpus/").stdout.strip(), "")

# 12 id-guard map vs landed registry
map_rows = {}
for ln in (LANE / ".ufo/waves/round-43/assimilation/renumber-map.tsv").read_text().splitlines()[1:]:
    f = ln.split("\t")
    if len(f) >= 3:
        map_rows[f[0]] = f[2]
check("map staged S302", map_rows["S302"], "S292")
check("map staged S303", map_rows["S303"], "S293")
check("map staged S304", map_rows["S304"], "S294")
check("map staged S305", map_rows["S305"], "S295")
check("map staged S251", map_rows["S251"], "S297")
landed = {}
for ln in src_data.splitlines():
    m = re.match(r"^\| (S\d+) \|", ln)
    if m:
        u = re.search(r"(https?://\S+?|\.ufo/\S+?)(?: \|| \|)", ln) or re.search(r"(https?://\S+|\.ufo/\S+)", ln)
        landed[m.group(1)] = (u.group(1).rstrip(" |") if u else "")
def ends(sid, frag):
    return landed.get(sid, "").endswith(frag)
check("landed S291 DefaultFloating", ends("S291", "DefaultFloatingAlgorithm.cpp"), True)
check("landed S292 Target", ends("S292", "layout/target/Target.cpp"), True)
check("landed S293 WindowTarget", ends("S293", "layout/target/WindowTarget.cpp"), True)
check("landed S294 GeometricMovable", ends("S294", "GeometricMovableAnimated.cpp"), True)
check("landed S295 host-gkeep.conf", ends("S295", "host-gkeep.conf"), True)
check("guard collisions count", len((LANE / ".ufo/waves/round-43/assimilation/collisions").read_text().split()), 34)

print()
print(f"VERIFY: checks={len(fails) and 'see FAIL above' or 'all'} fails={len(fails)}")
if fails:
    print("FAILED:", fails)
    sys.exit(1)
print("VERIFY: all checks PASS")
