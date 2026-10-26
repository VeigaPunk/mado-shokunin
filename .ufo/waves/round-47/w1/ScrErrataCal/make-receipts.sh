#!/usr/bin/env bash
# ScrErrataCal (round 47, w1) — read-only receipt generator for the round-44 w2/ConnCalibration errata.
# Every block prints the command, its output and its exit code. Nothing outside the seat dir is written.
set -u
LANE=/home/vgpnk/Projects/shokunin/mado-shokunin
OUT="$LANE/.ufo/waves/round-47/w1/ScrErrataCal/receipts"
S=/fast/scratch/hyaku/mado-r47/ScrErrataCal
mkdir -p "$OUT" "$S"
cd "$LANE" || exit 1
REV=$(git rev-parse HEAD)
D44=e46789213830597348fe96a351ae004d10587385
V2F=03fa5c618b089064a657b3d79d3d4272ae4b6894
R44TIP=8ac15c41
BASE44=6a1a90528fe533cadee506a9fa3e9d13d15cc41f

run() { # run <file> <label> <cmd...>
  local f="$1" label="$2"; shift 2
  { echo "\$ $*"
    "$@" 2>&1
    echo "[rc=$?]"
    echo
  } >> "$OUT/$f"
}

begin() { : > "$OUT/$1"; { echo "# receipt $1 — lane $LANE"; echo "# rev=$REV ($(date -Is))"; echo; } > "$OUT/$1"; }

# ---------- findings-list.txt : the calibration's finding list, D7 routing, round-46 draft status ----------
begin findings-list.txt
run findings-list.txt "finding headers" grep -n '^### F' .ufo/waves/round-44/w2/ConnCalibration.md
run findings-list.txt "D7 routing" grep -n 'ConnCalibration' corpus/lessons/round-44-verifier-spotcheck.md
run findings-list.txt "D7 routing (second line)" grep -n 'correct by appended errata' corpus/lessons/round-44-verifier-spotcheck.md
run findings-list.txt "round-46 lesson: errata drafted, not landed" grep -n 'not landed (routed)' corpus/lessons/round-46.md
run findings-list.txt "round-46 SCORECARD planned item" grep -n 'w2/ConnCalibration' SCORECARD.md
run findings-list.txt "draft is committed (so it is bytes, not a rumour)" git ls-files .ufo/waves/round-46/w1/ScrErrata/errata.md
run findings-list.txt "no errata block in SCORECARD yet" grep -n 'Errata — round-44 closure D7' SCORECARD.md

# ---------- e1-log-range.txt ----------
begin e1-log-range.txt
run e1-log-range.txt "LOG line" grep -n 'Mistakes M44' LOG.md
run e1-log-range.txt "lesson mistake count" grep -c '^\*\*M44-' corpus/lessons/round-44.md
run e1-log-range.txt "lesson mistake headers" grep -n '^\*\*M44-' corpus/lessons/round-44.md
run e1-log-range.txt "SCORECARD publication" grep -n 'Mistakes M44-1..9' SCORECARD.md
run e1-log-range.txt "M44-8 evidence seat" grep -n 'w1/CritC2Cheat.md' corpus/lessons/round-44.md
run e1-log-range.txt "M44-9 evidence seat" grep -n 'w1/CritFsPremise' corpus/lessons/round-44.md

# ---------- e2-renumber.txt ----------
begin e2-renumber.txt
run e2-renumber.txt "bare path at data commit (calibration's repro)" git cat-file -e "$D44:assimilation/renumber-map.tsv"
run e2-renumber.txt "bare path at HEAD" git cat-file -e "HEAD:assimilation/renumber-map.tsv"
run e2-renumber.txt "calibration's tree query" git ls-tree -r --name-only "$D44" -- assimilation/
run e2-renumber.txt "wave-relative at data commit" git ls-tree "$D44" -- .ufo/waves/round-44/assimilation/renumber-map.tsv
run e2-renumber.txt "wave-relative at HEAD" git ls-tree HEAD -- .ufo/waves/round-44/assimilation/renumber-map.tsv
run e2-renumber.txt "adding commit" git log --diff-filter=A --format='%h %s' -- .ufo/waves/round-44/assimilation/renumber-map.tsv
run e2-renumber.txt "all tracked renumber maps" git ls-files '*/renumber-map*'
run e2-renumber.txt "lesson citations" grep -n 'renumber-map.tsv' corpus/lessons/round-44.md
run e2-renumber.txt "id-guard citation" grep -n 'renumber-map.tsv' .ufo/waves/round-44/assimilation/id-guard.md
run e2-renumber.txt "map rows" git show HEAD:.ufo/waves/round-44/assimilation/renumber-map.tsv

# ---------- e3-skill-clients.txt ----------
begin e3-skill-clients.txt
run e3-skill-clients.txt "SKILL clients=4 at HEAD" grep -n 'clients=4' SKILL.md
run e3-skill-clients.txt "SKILL four tiled at HEAD" grep -n 'four tiled' SKILL.md
run e3-skill-clients.txt "SKILL at data commit (extracted to scratch)" bash -c "git show $D44:SKILL.md > $S/skill-at-data.md; wc -l < $S/skill-at-data.md"
run e3-skill-clients.txt "SKILL clients=4 at data commit" grep -n 'clients=4' "$S"/skill-at-data.md
run e3-skill-clients.txt "round-43 receipt" grep -n 'clients=' .ufo/waves/round-43/receipts/live-geometry-host.txt
run e3-skill-clients.txt "round-44 receipt" grep -n 'clients=' .ufo/waves/round-44/receipts/live-geometry-host-r44.txt
run e3-skill-clients.txt "base 6a1a905 SKILL" bash -c "git show $BASE44:SKILL.md | grep -n 'clients=4'"
run e3-skill-clients.txt "no clients= line added base->data" bash -c "git diff $BASE44 $D44 -- SKILL.md | grep -c '^[-+].*clients='"

# ---------- e4-tip-receipts.txt ----------
begin e4-tip-receipts.txt
run e4-tip-receipts.txt "ancestry of the round-44 tip" git rev-parse "$R44TIP^" "$R44TIP^^"
run e4-tip-receipts.txt "commits between" git rev-list --count "74c606a..$R44TIP"
run e4-tip-receipts.txt "tip receipts at 290cddea" git ls-tree 290cddea -- .ufo/waves/round-44/receipts/c1-after-tip.txt .ufo/waves/round-44/receipts/c2-after-tip.txt .ufo/waves/round-44/receipts/axis-tip.txt
run e4-tip-receipts.txt "tip receipts at 8ac15c41" git ls-tree "$R44TIP" -- .ufo/waves/round-44/receipts/c1-after-tip.txt .ufo/waves/round-44/receipts/c2-after-tip.txt .ufo/waves/round-44/receipts/axis-tip.txt
run e4-tip-receipts.txt "axis-tip rev" bash -c "git show HEAD:.ufo/waves/round-44/receipts/axis-tip.txt | grep -n 'rev='"
run e4-tip-receipts.txt "tip commit identity" git log --oneline -1 8ac15c41
run e4-tip-receipts.txt "tip is an ancestor of the lane tip" bash -c "git merge-base --is-ancestor 8ac15c41 HEAD && echo ancestor=yes"
run e4-tip-receipts.txt "the one commit adds" bash -c "git diff --name-only 74c606a 8ac15c41 | wc -l"
run e4-tip-receipts.txt "of which outside .ufo/waves/round-44/" bash -c "git diff --name-only 74c606a 8ac15c41 | grep -vc '^\\.ufo/'"
run e4-tip-receipts.txt "74c606a subject" git log --oneline -1 74c606a

# ---------- e5-w1-paths.txt ----------
begin e5-w1-paths.txt
for r in "$D44" "$V2F" 290cddea "$R44TIP" HEAD; do
  run e5-w1-paths.txt "w1 tree count $r" bash -c "git ls-tree -r --name-only $r -- .ufo/waves/round-44/w1/ | wc -l"
  run e5-w1-paths.txt "w1-results count $r" bash -c "git ls-tree --name-only $r -- .ufo/waves/round-44/w1-results.json | wc -l"
done
run e5-w1-paths.txt "lesson opening pointer" grep -n 'w1-results.json' corpus/lessons/round-44.md
run e5-w1-paths.txt "lesson scribe pointer" grep -n 'w1/ScrLessonSkeleton' corpus/lessons/round-44.md
run e5-w1-paths.txt "SCORECARD supersession sentence" grep -n 'w1/CritC1Cheat.md' SCORECARD.md
run e5-w1-paths.txt "SCORECARD separability sentence" grep -n 'w1/ConnCrossClaim.md' SCORECARD.md
run e5-w1-paths.txt "cited w1 files exist at HEAD" bash -c 'for f in w1/CritC1Cheat.md w1/CritC2Cheat.md w1/CritClaimSizing.md w1/RevC2Counter.md w1/CritFsPremise.md w1/ConnCrossClaim.md w1/ScrLessonSkeleton; do printf "%s " "$f"; git ls-tree --name-only HEAD -- ".ufo/waves/round-44/$f" | wc -l; done'

# ---------- e6-check83.txt ----------
begin e6-check83.txt
run e6-check83.txt "QUALITY 83 check line" grep -n 'check83.py' corpus/QUALITY.md
for r in "$D44" "$V2F" 290cddea "$R44TIP" HEAD; do
  run e6-check83.txt "check83.py at $r" bash -c "git ls-tree --name-only $r -- .ufo/waves/round-44/w1/ScrQualityCriteria/check83.py | wc -l"
done
run e6-check83.txt "adding commit" git log --diff-filter=A --format='%h %s' -- .ufo/waves/round-44/w1/ScrQualityCriteria/check83.py
run e6-check83.txt "directory at 290cddea" git ls-tree --name-only 290cddea -- .ufo/waves/round-44/w1/ScrQualityCriteria/

# ---------- n1-claim-rows.txt : coverage note (not one of the six) ----------
begin n1-claim-rows.txt
run n1-claim-rows.txt "round-44 claim rows" sed -n '2570,2571p' SCORECARD.md
run n1-claim-rows.txt "c1 after-data value" grep -n 'verdict=' .ufo/waves/round-44/receipts/c1-after-data.txt
run n1-claim-rows.txt "c2 after-data value" grep -n 'admitted=' .ufo/waves/round-44/receipts/c2-after-data.txt
run n1-claim-rows.txt "round-44 D2 routing" grep -n 'D2 —' corpus/lessons/round-44-verifier-spotcheck.md

# ---------- footprint ----------
begin footprint.txt
run footprint.txt "seat dir status" git status --porcelain -- .ufo/waves/round-47/w1/ScrErrataCal
run footprint.txt "lane status" git status --porcelain

# ---------- quotes-verify.txt ----------
{ python3 "$LANE/.ufo/waves/round-47/w1/ScrErrataCal/verify-quotes.py" 2>&1; echo "[rc=$?]"; } > "$OUT/quotes-verify.txt"

echo "receipts written to $OUT"
