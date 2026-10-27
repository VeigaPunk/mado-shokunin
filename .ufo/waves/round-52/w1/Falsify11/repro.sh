#!/usr/bin/env bash
# Falsify11 repro: C1 no-work control validity.
# Read-only w.r.t. the lane checkout; every write stays under $SCRATCH.
set -euo pipefail

LANE=/home/vgpnk/Projects/shokunin/mado-shokunin
BASE=85d57a818c3707397e21c840b6498b105ba798aa
CTL=$LANE/.ufo/waves/round-52/controls/c1-do-nothing.md
SCRATCH=${SCRATCH:-/fast/scratch/hyaku/mado-r52/Falsify11/repro}
SEAT=/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-52/w1/Falsify11
export TMPDIR=$SCRATCH/tmp
rm -rf "$SCRATCH"; mkdir -p "$TMPDIR"

say() { printf '\n== %s\n' "$*"; }
run() { printf '$ %s\n' "$*"; "$@"; }

say "clone lane at base into scratch"
run git clone --quiet --no-hardlinks "$LANE" "$SCRATCH/clone"
C=$SCRATCH/clone
cd "$C"
test "$(git rev-parse --show-toplevel)" = "$C"
run git checkout --quiet --detach "$BASE"
run git rev-parse HEAD

G=$C/quality/check-tool-ledger.py

say "base gate on the production ledger at base (must match receipts/c1-base.txt)"
run python3 "$G" --repo "$C" --rev "$BASE" | tail -1

say "commit the frozen control verbatim as quality/tool-ledger.md"
git checkout --quiet -B control "$BASE"
cp "$CTL" quality/tool-ledger.md
git add quality/tool-ledger.md
git -c user.name=seat-falsify11 -c user.email=seat@local commit --quiet -m "fixture: frozen c1 control verbatim"
CTLREV=$(git rev-parse HEAD)
echo "control rev $CTLREV"
run python3 "$G" --repo "$C" --rev "$CTLREV" > "$TMPDIR/ctl-base.txt" || true
awk '/^LEDGER-ROW/{print $2}' "$TMPDIR/ctl-base.txt" | sort | uniq -c
tail -1 "$TMPDIR/ctl-base.txt"

say "minimal counter (completeness + uniqueness only) on production and control"
run python3 "$SEAT/min-counter.py" --repo "$C" --rev "$BASE" || true
run python3 "$SEAT/min-counter.py" --repo "$C" --rev "$CTLREV" || true

say "schema-repaired control: Tool|Reads|Writes|Owner -> ledger grammar, pointer backticked"
for mode in norm norm-one; do
  git checkout --quiet -B "fixture-$mode" "$BASE"
  python3 "$SEAT/build-fixture.py" --repo "$C" --rev "$BASE" --mode "$mode" --control "$CTL"
  git add quality/tool-ledger.md
  git -c user.name=seat-falsify11 -c user.email=seat@local commit --quiet -m "fixture: $mode"
  R=$(git rev-parse HEAD)
  echo "--- $mode rev $R"; sed -n '5,8p' quality/tool-ledger.md
  run python3 "$G" --repo "$C" --rev "$R" > "$TMPDIR/$mode.txt" || true
  awk '/^LEDGER-ROW/{print $2}' "$TMPDIR/$mode.txt" | sort | uniq -c
  tail -1 "$TMPDIR/$mode.txt"
  run python3 "$SEAT/min-counter.py" --repo "$C" --rev "$R" || true
done

say "shape-matched no-work ledger: 82 unique rows, generic repeated description, self pointer"
git checkout --quiet -B padded "$BASE"
python3 "$SEAT/build-fixture.py" --repo "$C" --rev "$BASE" --mode padded --control "$CTL"
git add quality/tool-ledger.md
git -c user.name=seat-falsify11 -c user.email=seat@local commit --quiet -m "fixture: padded no-work ledger"
PAD=$(git rev-parse HEAD)
echo "padded rev $PAD"
run python3 "$G" --repo "$C" --rev "$PAD" > "$TMPDIR/padded.txt" || true
tail -1 "$TMPDIR/padded.txt"
run python3 "$SEAT/min-counter.py" --repo "$C" --rev "$PAD" || true

say "shared-document census: how many population basenames one non-self doc already names"
python3 - "$C" "$BASE" <<'PY'
import subprocess, sys, re
repo, rev = sys.argv[1], sys.argv[2]
def git(*a): return subprocess.run(["git","-C",repo]+list(a),capture_output=True).stdout
paths=[p.decode() for p in git("ls-tree","-r","--name-only",rev).splitlines()]
pop=sorted({p for p in paths if p.startswith("tools/") or re.match(r"^quality/[^/]+\.py$",p) or re.match(r"^quality/counters/[^/]+\.py$",p)})
def hit(text,w): return re.search(r"(?<![A-Za-z0-9._-])"+re.escape(w)+r"(?![A-Za-z0-9_-])",text) is not None
score=git("show",f"{rev}:SCORECARD.md").decode("utf-8","replace")
prov=git("show",f"{rev}:PROVINCE.md").decode("utf-8","replace")
print("population=%d" % len(pop))
for name,text in (("SCORECARD.md",score),("PROVINCE.md",prov),("SCORECARD|PROVINCE",score+prov)):
    print("%-20s names=%d/%d" % (name, sum(hit(text,p.rsplit('/',1)[-1]) for p in pop), len(pop)))
PY

say "description-distinctness probe on both ledgers"
python3 - "$C" "$BASE" "$PAD" <<'PY'
import subprocess, sys, re
repo, base, pad = sys.argv[1], sys.argv[2], sys.argv[3]
def show(rev): return subprocess.run(["git","-C",repo,"show",f"{rev}:quality/tool-ledger.md"],capture_output=True,text=True).stdout
def descs(text):
    out=[]; fence=None
    for line in text.splitlines():
        s=line.strip()
        if fence: 
            if s.startswith(fence): fence=None
            continue
        if re.match(r"^(`{3,}|~{3,})", s): fence=s[0]*3; continue
        if not s.startswith("|"): continue
        cells=[c.strip() for c in s.strip("|").split("|")]
        if cells and cells[0].replace("`","").lower() in {"instrument","path","file","tool","artifact"}: continue
        if all(re.fullmatch(r":?-{3,}:?",c) for c in cells if c): continue
        if len(cells)==3: out.append(cells[1])
    return out
for label,rev in (("production",base),("padded-no-work",pad)):
    d=descs(show(rev))
    print("%-14s rows=%d distinct_descriptions=%d min_len=%d" % (label,len(d),len(set(d)),min(map(len,d)) if d else 0))
PY

say "done"
