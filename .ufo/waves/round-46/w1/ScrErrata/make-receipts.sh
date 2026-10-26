#!/usr/bin/env bash
# ScrErrata (round 46) receipt generator — read-only. Writes only into this seat's receipts/.
# Every block prints the command then its output, so each line in errata.md is traceable to a receipt.
set -u
L=/home/vgpnk/Projects/shokunin/mado-shokunin
R="$L/.ufo/waves/round-46/w1/ScrErrata/receipts"
mkdir -p "$R"
run() { echo "\$ $*"; "$@" 2>&1; echo "[rc=$?]"; echo; }
cd "$L" || exit 1

{
echo "### f1 — LOG.md mistake range vs the lesson's range"
run grep -n 'Mistakes M44' LOG.md
run grep -c '^\*\*M44-' corpus/lessons/round-44.md
run grep -n 'Mistakes M44-1..9' SCORECARD.md
run grep -n '^\*\*M44-' corpus/lessons/round-44.md
echo "--- which wave the last two mistakes come from ---"
run grep -n 'w1/CritC2Cheat.md\|w1/CritFsPremise' corpus/lessons/round-44.md
echo "### the calibration's own F1 locator"
run grep -n 'M44-1..7' .ufo/waves/round-44/w2/ConnCalibration.md
} > "$R/f1-log-range.txt"

{
echo "### f2 — does assimilation/renumber-map.tsv exist?"
echo "--- lane-root-relative path (what the lesson cites) ---"
run git cat-file -e e4678921:assimilation/renumber-map.tsv
run git cat-file -e HEAD:assimilation/renumber-map.tsv
echo "--- wave-relative path ---"
run git ls-tree e4678921 -- .ufo/waves/round-44/assimilation/renumber-map.tsv
run git ls-tree HEAD -- .ufo/waves/round-44/assimilation/renumber-map.tsv
echo "--- every committed renumber map ---"
run git ls-files '*/renumber-map*'
echo "--- where the wave-44 map entered history ---"
run git log --oneline --diff-filter=A -- .ufo/waves/round-44/assimilation/renumber-map.tsv
echo "--- the lesson citations ---"
run grep -n 'renumber-map' corpus/lessons/round-44.md
run grep -n 'renumber-map' .ufo/waves/round-44/assimilation/id-guard.md
echo "--- the map's own rows ---"
run cat .ufo/waves/round-44/assimilation/renumber-map.tsv
echo "--- the calibration's repro commands, verbatim ---"
run git ls-tree -r --name-only e4678921 assimilation/
run git log --oneline --all -- assimilation/
} > "$R/f2-renumber.txt"

{
echo "### f3 — SKILL.md host-run paragraph: which run's numbers?"
run grep -n 'clients=4' SKILL.md
run grep -n 'Host run 2026-10-26' SKILL.md
echo "--- round-43 receipt (source of the paragraph) ---"
run grep -n 'clients=' .ufo/waves/round-43/receipts/live-geometry-host.txt
echo "--- round-44 receipt (the run named by round 44) ---"
run grep -n 'clients=' .ufo/waves/round-44/receipts/live-geometry-host-r44.txt
echo "--- is the paragraph changed base -> data commit? (0 = no +/- line carries clients=) ---"
run git diff 6a1a905 e4678921 -- SKILL.md
echo "--- count only ---"
run bash -c "git diff 6a1a905 e4678921 -- SKILL.md | grep -c '^[-+].*clients='"
echo "--- the paragraph at base ---"
run git show 6a1a905:SKILL.md
} > "$R/f3-skill-clients.txt.tmp"
# keep f3 small: reduce the two whole-file dumps to the locator lines
{
echo "### f3 — SKILL.md host-run paragraph: which run's numbers?"
run grep -n 'clients=4' SKILL.md
run grep -n 'Host run 2026-10-26' SKILL.md
echo "--- round-43 receipt (source of the paragraph) ---"
run grep -n 'clients=' .ufo/waves/round-43/receipts/live-geometry-host.txt
echo "--- round-44 receipt (the run named by round 44) ---"
run grep -n 'clients=' .ufo/waves/round-44/receipts/live-geometry-host-r44.txt
echo "--- base->data diff of SKILL.md: lines carrying clients= (0 = paragraph untouched) ---"
run bash -c "git diff 6a1a905 e4678921 -- SKILL.md | grep -c '^[-+].*clients='"
echo "--- the paragraph at base 6a1a905 (locator) ---"
run bash -c "git show 6a1a905:SKILL.md | grep -n 'clients=4\|Host run 2026-10-26'"
echo "--- four tiled? the dump the paragraph quotes ---"
run bash -c "grep -c 'tiled' .ufo/waves/round-43/receipts/live-geometry-host.txt"
run bash -c "sed -n '1,12p' .ufo/waves/round-43/receipts/live-geometry-host.txt"
} > "$R/f3-skill-clients.txt"
rm -f "$R/f3-skill-clients.txt.tmp"

{
echo "### f4 — the three 'tip' receipts and what 'tip' meant"
run git rev-list --count 74c606a..8ac15c41
run bash -c "git ls-tree 8ac15c41 -- .ufo/waves/round-44/receipts/c1-after-tip.txt .ufo/waves/round-44/receipts/c2-after-tip.txt .ufo/waves/round-44/receipts/axis-tip.txt"
run bash -c "git ls-tree 290cddea -- .ufo/waves/round-44/receipts/c1-after-tip.txt .ufo/waves/round-44/receipts/c2-after-tip.txt .ufo/waves/round-44/receipts/axis-tip.txt"
echo "--- committed rev inside the tip receipts ---"
run bash -c "grep -n 'rev=' .ufo/waves/round-44/receipts/axis-tip.txt"
} > "$R/f4-tip-receipts.txt"

{
echo "### f5 — w1 evidence cited before it landed"
for rev in e4678921 03fa5c61 290cddea 8ac15c41 HEAD; do
  echo -n "$rev .ufo/waves/round-44/w1/ files: "
  git ls-tree -r --name-only "$rev" .ufo/waves/round-44/w1/ | wc -l
done
echo
echo "--- w1-results.json in the tree? ---"
for rev in e4678921 03fa5c61 290cddea 8ac15c41 HEAD; do
  echo -n "$rev: "
  git ls-tree --name-only "$rev" .ufo/waves/round-44/w1-results.json | wc -l
done
echo
echo "--- the pointers that name w1 evidence ---"
run grep -n 'w1-results.json\|w1/ScrLessonSkeleton\|w1/CritC2Cheat/frozen-F2-FORGED-PIN.txt\|w1/RevC2Counter/log-forged_s164.txt' corpus/lessons/round-44.md
run grep -n 'w1/CritC1Cheat.md\|w1/CritC2Cheat.md\|w1/CritClaimSizing.md\|w1/RevC2Counter.md\|w1/CritFsPremise.md\|w1/ConnCrossClaim.md\|w1/CritClaimSizing.md` F10' SCORECARD.md
} > "$R/f5-w1-paths.txt"

{
echo "### f6 — criterion 83's check path"
run grep -n 'check83.py' corpus/QUALITY.md
for rev in e4678921 03fa5c61 290cddea 8ac15c41 HEAD; do
  echo -n "$rev check83.py rows: "
  git ls-tree -r --name-only "$rev" .ufo/waves/round-44/w1/ScrQualityCriteria/check83.py | wc -l
done
echo
echo "--- first commit that adds it ---"
run git log --oneline --diff-filter=A -- .ufo/waves/round-44/w1/ScrQualityCriteria/check83.py
} > "$R/f6-check83.txt"

{
echo "### d4 — round-45 MutC1Counter/results.json: retention state"
echo "--- worktree ---"
run ls -l .ufo/waves/round-45/w1/MutC1Counter/
echo "--- in git history at all? ---"
run git log --all --oneline -- .ufo/waves/round-45/w1/MutC1Counter/results.json
echo "--- tracked now? ---"
run git ls-files .ufo/waves/round-45/w1/MutC1Counter/results.json
echo "--- the digest line (written by the D4 owner this round) ---"
run cat .ufo/waves/round-45/w1/MutC1Counter/results.digest.txt
echo "--- what summary.txt holds ---"
run wc -l .ufo/waves/round-45/w1/MutC1Counter/summary.txt
run head -3 .ufo/waves/round-45/w1/MutC1Counter/summary.txt
run tail -3 .ufo/waves/round-45/w1/MutC1Counter/summary.txt
echo "--- field count per summary line (should be 6) ---"
run bash -c "awk -F'|' '{print NF}' .ufo/waves/round-45/w1/MutC1Counter/summary.txt | sort -u"
echo "--- verdict classes present ---"
run bash -c "cut -d'|' -f2 .ufo/waves/round-45/w1/MutC1Counter/summary.txt | sort | uniq -c"
echo "--- matrix.md extent ---"
run wc -l .ufo/waves/round-45/w1/MutC1Counter/matrix.md
run grep -n '551 counter runs\|38 single-edit mutants' .ufo/waves/round-45/w1/MutC1Counter/matrix.md
echo "--- matrix totals line (the class tally in prose) ---"
run grep -n 'Totals:' .ufo/waves/round-45/w1/MutC1Counter/matrix.md
echo "--- tracked/untracked state of the directory ---"
run git status --porcelain -- .ufo/waves/round-45/w1/MutC1Counter/
echo "--- closure D4 text ---"
run grep -n 'D4' corpus/lessons/round-45-verifier-spotcheck.md
} > "$R/d4-results-retention.txt"

{
echo "### d5 — round-45 w1-results.json holds no seat output"
run python3 -c "import json;d=json.load(open('.ufo/waves/round-45/w1-results.json'));r=d['results'];print('seats',d['seats'],'results',len(r),'output_null',sum(1 for x in r if x['output'] is None));print('note_sample',r[0]['note'])"
run bash -c "git ls-tree --name-only HEAD .ufo/waves/round-45/w1/ | grep -c '\.md$'"
run bash -c "git ls-tree --name-only HEAD .ufo/waves/round-45/w1/ | grep '\.md$'"
echo "--- closure D5 text ---"
run grep -n 'D5' corpus/lessons/round-45-verifier-spotcheck.md
} > "$R/d5-results-null.txt"

{
echo "### d5 — locator for the per-entry note (locator from grep -n on the pretty-printed projection)"
run python3 -m json.tool .ufo/waves/round-45/w1-results.json
echo "--- grep -n over that projection ---"
run bash -c "python3 -m json.tool .ufo/waves/round-45/w1-results.json | grep -n 'read the seat report file in the wave dir' | head -3"
} > "$R/d5-note-line.txt"

{
echo "### write-footprint of this seat (older waves untouched)"
run git status --porcelain -- .ufo/waves/round-44 .ufo/waves/round-45
run git status --porcelain -- .ufo/waves/round-46/w1/ScrErrata
} > "$R/write-footprint.txt"

{
echo "### finding headers of the round-44 w2 calibration (the mismatch list)"
run grep -n '^### F' .ufo/waves/round-44/w2/ConnCalibration.md
run grep -n '^## Verdict' .ufo/waves/round-44/w2/ConnCalibration.md
run bash -c "sed -n '14,22p' .ufo/waves/round-44/w2/ConnCalibration.md"
echo "--- closure D7 text ---"
run grep -n 'D7' corpus/lessons/round-44-verifier-spotcheck.md
echo "--- round-44 closure D2 (the after-values routing the coverage note names) ---"
run grep -n 'D2' corpus/lessons/round-44-verifier-spotcheck.md
} > "$R/findings-list.txt"

ls -l "$R"
