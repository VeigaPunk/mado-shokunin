#!/usr/bin/env bash
# RevRowsUsedBy repro driver. Read-only on the lane: every write is under this scratch dir.
set -u
cd /home/vgpnk/Projects/shokunin/mado-shokunin || exit 1
S=.ufo/waves/round-35/scratch/RevRowsUsedBy
C1="python3 -I .ufo/waves/round-35/c1/count.py"
FZ=".ufo/waves/round-35/c1/frozen.json"
CEN=/home/vgpnk/Projects/shokunin/scripts/sources-census.sh
echo "## 0 snapshot (observed state, sha256)"
sha256sum "$S"/snapshot/*
echo
echo "## 1 baseline counter on the live tree"
$C1 --root . --frozen "$FZ"; echo "exit=$?"
echo
echo "## 2 census validate on the live registry (--today 2026-10-25)"
"$CEN" validate --file corpus/SOURCES.md --today 2026-10-25; echo "exit=$?"
echo
echo "## 3 independent used-by table"
cat "$S/usedby-table.txt"
echo
echo "## 4 counter source lines: the used-by / status / recheck clauses and the absent opened clause"
grep -n "cs\[10\]\|citing = \|used_by == citing\|cs\[7\] == \|valid_recheck(cs\[9\])\|SYMBOLIC = \|CADENCE = \|ISO_DATE = " .ufo/waves/round-35/c1/count.py
echo "grep -c opened .ufo/waves/round-35/c1/count.py -> $(grep -c opened .ufo/waves/round-35/c1/count.py) (exit $?)"
echo
echo "## 5 mutations on base2 (post-repair snapshot); each line is the counter verdict"
for d in "$S"/n-*; do
  [ -d "$d" ] || continue
  out=$($C1 --root "$d" --frozen "$FZ"); rc=$?
  printf '%-26s exit=%s %s\n' "$(basename "$d" | sed 's/^n-//')" "$rc" "$out"
done
echo
echo "## 6 pre-data golden control vs live: the five cells under review"
python3 - <<'PY'
from pathlib import Path
import re
ROW=re.compile(r"^ {0,3}\|\s*(S[0-9]+)\s*\|")
def cells(p):
    d={}
    for l in Path(p).read_text().splitlines():
        m=ROW.match(l)
        if m: d[m.group(1)]=[x.strip() for x in l.split('|')[1:-1]]
    return d
live=cells('corpus/SOURCES.md'); gold=cells('.ufo/waves/round-35/controls/golden/corpus/SOURCES.md')
for sid in [f"S20{i}" for i in range(3,10)]+["S210"]:
    for idx,name in [(7,'status'),(8,'opened'),(9,'recheck'),(10,'used-by')]:
        if live[sid][idx]!=gold[sid][idx]:
            print(f"{sid} {name}: GOLDENSYNTHETIC={gold[sid][idx]!r} LIVE={live[sid][idx]!r}")
    if live[sid][5]!=gold[sid][5] or live[sid][6]!=gold[sid][6]:
        print(f"{sid} anchor/teaches text differs from golden (lengths {len(gold[sid][5])}->{len(live[sid][5])}, {len(gold[sid][6])}->{len(live[sid][6])})")
print("golden registry lines:", len(Path('.ufo/waves/round-35/controls/golden/corpus/SOURCES.md').read_text().splitlines()))
PY
echo
echo "## 7 README recheck claims vs row cells"
python3 - <<'PY'
from pathlib import Path
import re
ROW=re.compile(r"^ {0,3}\|\s*(S[0-9]+)\s*\|")
for l in Path('corpus/SOURCES.md').read_text().splitlines():
    m=ROW.match(l)
    if m and m.group(1) in ('S203','S204','S205','S206','S207','S208','S209','S210'):
        c=[x.strip() for x in l.split('|')[1:-1]]
        print(f"{m.group(1)} row recheck={c[9]}")
PY
grep -n "recheck on-request\|recheck on-change (S209" corpus/README.md
echo
echo "## 8 entry headers: recheck lines and source lines"
for f in corpus/knowledge/idle-lock-never-asked-r12.md corpus/knowledge/idle-lock-chain-armed-r14.md corpus/knowledge/idle-lock-offered-in-the-bar-r15.md; do
  echo "-- $f"; grep -nE "^source:|^recheck:|^verified-at:" "$f"
done
