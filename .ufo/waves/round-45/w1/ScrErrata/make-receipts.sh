#!/bin/bash
# ScrErrata — regenerate the receipts the errata cites. Read-only on the lane.
set -u
LANE=/home/vgpnk/Projects/shokunin/mado-shokunin
SEAT=$LANE/.ufo/waves/round-45/w1/ScrErrata
R=$SEAT/receipts
mkdir -p "$R"

{
  echo "# D2 — published after-states of the Round 44 claim rows"
  echo "\$ grep -n 'see \`receipts/c[12]-after-data.txt\`' $LANE/SCORECARD.md"
  grep -n 'see `receipts/c[12]-after-data.txt`' "$LANE/SCORECARD.md"
  echo "\$ grep -n 'recorded in the round report from the receipts' $LANE/SCORECARD.md"
  grep -n 'recorded in the round report from the receipts' "$LANE/SCORECARD.md"
  echo "\$ grep -n 'fixtures=26/26 tool=present verdict=TARGET_MET' .ufo/waves/round-44/receipts/c1-after-data.txt c1-after-tip.txt"
  grep -n 'fixtures=26/26 tool=present verdict=TARGET_MET' \
    "$LANE/.ufo/waves/round-44/receipts/c1-after-data.txt" \
    "$LANE/.ufo/waves/round-44/receipts/c1-after-tip.txt"
  echo "\$ grep -n 'admitted=1/1 verdict=TARGET_MET' .ufo/waves/round-44/receipts/c2-after-data.txt c2-after-tip.txt"
  grep -n 'admitted=1/1 verdict=TARGET_MET' \
    "$LANE/.ufo/waves/round-44/receipts/c2-after-data.txt" \
    "$LANE/.ufo/waves/round-44/receipts/c2-after-tip.txt"
  echo "\$ tail -1 .ufo/waves/round-44/receipts/c1-after-data.txt c1-after-tip.txt c2-after-data.txt c2-after-tip.txt"
  for f in c1-after-data c1-after-tip c2-after-data c2-after-tip; do
    printf '%s: ' "$f"; tail -1 "$LANE/.ufo/waves/round-44/receipts/$f.txt"
  done
  echo "\$ grep -n 'rev=' .ufo/waves/round-44/receipts/axis-data.txt axis-tip.txt"
  grep -n 'rev=' "$LANE/.ufo/waves/round-44/receipts/axis-data.txt" "$LANE/.ufo/waves/round-44/receipts/axis-tip.txt"
  echo "\$ git -C $LANE diff --name-only 8ac15c41 0c89478 -- .ufo/waves/round-44/receipts/"
  git -C "$LANE" diff --name-only 8ac15c41 0c89478 -- .ufo/waves/round-44/receipts/
  echo "(no output above = the receipts are byte-identical between the round-44 tip and the round-45 base)"
} > "$R/d2-after-values.txt" 2>&1

{
  echo "# D3 — 74c606a vs the lane tip 8ac15c41"
  echo "\$ git -C $LANE rev-parse 8ac15c41^"
  git -C "$LANE" rev-parse 8ac15c41^
  echo "\$ git -C $LANE rev-list --count 74c606a..8ac15c41"
  git -C "$LANE" rev-list --count 74c606a1c7fd52a6bb85bb1c786529c926040c73..8ac15c41
  echo "\$ git -C $LANE diff --name-only 74c606a 8ac15c41 | wc -l"
  git -C "$LANE" diff --name-only 74c606a1c7fd52a6bb85bb1c786529c926040c73 8ac15c41 | wc -l
  echo "\$ git -C $LANE diff --name-only 74c606a 8ac15c41 | grep -vc '^\.ufo/waves/round-44/'"
  git -C "$LANE" diff --name-only 74c606a1c7fd52a6bb85bb1c786529c926040c73 8ac15c41 | grep -vc '^\.ufo/waves/round-44/'
  echo "\$ git -C $LANE diff --stat 74c606a 8ac15c41 -- tools/mado-geometry.py corpus/knowledge/hyprland-gkeep-size-request-r44.md corpus/SOURCES.md SKILL.md corpus/lessons/round-44.md corpus/QUALITY.md SCORECARD.md"
  git -C "$LANE" diff --stat 74c606a1c7fd52a6bb85bb1c786529c926040c73 8ac15c41 -- \
    tools/mado-geometry.py corpus/knowledge/hyprland-gkeep-size-request-r44.md corpus/SOURCES.md \
    SKILL.md corpus/lessons/round-44.md corpus/QUALITY.md SCORECARD.md
  echo "(no output above = every counted surface is byte-identical at 74c606a and at the tip)"
  echo "\$ git -C $LANE log --oneline 74c606a..8ac15c41"
  git -C "$LANE" log --oneline 74c606a1c7fd52a6bb85bb1c786529c926040c73..8ac15c41
} > "$R/d3-structure.txt" 2>&1

# measured at the tip: copies of the runs made in /fast/scratch/hyaku/mado-r45/ScrErrata
S=/fast/scratch/hyaku/mado-r45/ScrErrata
for f in c1-tip-8ac15c41 c2-tip-8ac15c41 axis-tip-8ac15c41; do
  cp "$S/w1/$f.txt" "$R/$f.txt"
done

{
  echo "# D7 — truths"
  echo "\$ git -C $LANE log --oneline -1 8ac15c41; git -C $LANE log --oneline -1 74c606a; git -C $LANE log --oneline -1 290cddea; git -C $LANE log --oneline -1 e467892"
  for r in 8ac15c41 74c606a1 290cddea e4678921; do git -C "$LANE" log --oneline -1 "$r"; done
  echo
  echo "## F1"
  echo "\$ grep -c '^\*\*M44-' corpus/lessons/round-44.md"
  grep -c '^\*\*M44-' "$LANE/corpus/lessons/round-44.md"
  echo "\$ grep -n 'M44-1..7' LOG.md; grep -n 'M44-1..9' SCORECARD.md"
  grep -n 'M44-1..7' "$LANE/LOG.md"
  grep -n 'M44-1..9' "$LANE/SCORECARD.md" | cut -c1-60
  echo
  echo "## F2 — where the mapping artifact actually is"
  echo "\$ git -C $LANE ls-tree e4678921 -- .ufo/waves/round-44/assimilation/renumber-map.tsv"
  git -C "$LANE" ls-tree e4678921 -- .ufo/waves/round-44/assimilation/renumber-map.tsv
  echo "\$ git -C $LANE ls-tree 0c89478 -- .ufo/waves/round-44/assimilation/renumber-map.tsv"
  git -C "$LANE" ls-tree 0c89478 -- .ufo/waves/round-44/assimilation/renumber-map.tsv
  echo "\$ git -C $LANE log --oneline -- .ufo/waves/round-44/assimilation/renumber-map.tsv"
  git -C "$LANE" log --oneline -- .ufo/waves/round-44/assimilation/renumber-map.tsv
  echo "\$ git -C $LANE ls-files | grep 'renumber-map'"
  git -C "$LANE" ls-files | grep 'renumber-map'
  echo "\$ git -C $LANE ls-tree -r --name-only e4678921 assimilation/   # ConnCalibration's command: lane-root relative"
  git -C "$LANE" ls-tree -r --name-only e4678921 assimilation/ | wc -l
  echo
  echo "## F3 — which run the SKILL paragraph quotes"
  echo "\$ grep -n 'clients=4' .ufo/waves/round-43/receipts/live-geometry-host.txt"
  grep -n 'clients=4' "$LANE/.ufo/waves/round-43/receipts/live-geometry-host.txt"
  echo "\$ git -C $LANE diff 6a1a905 e4678921 -- SKILL.md | grep -c '^[-+].*clients='"
  git -C "$LANE" diff 6a1a905 e4678921 -- SKILL.md | grep -c '^[-+].*clients='
  echo "\$ git -C $LANE show 6a1a905:SKILL.md | sed -n '283,290p' | cut -c1-80"
  git -C "$LANE" show 6a1a905:SKILL.md | sed -n '283,290p' | cut -c1-80
  echo
  echo "## F5 — the w1 tree at three revisions"
  for r in e4678921 03fa5c61 290cddea 8ac15c41; do
    printf '%s w1 files: ' "$r"
    git -C "$LANE" ls-tree -r --name-only "$r" -- .ufo/waves/round-44/w1/ | wc -l
  done
  echo "\$ git -C $LANE ls-tree 290cddea -- .ufo/waves/round-44/w1-results.json | wc -l"
  git -C "$LANE" ls-tree 290cddea -- .ufo/waves/round-44/w1-results.json | wc -l
  echo
  echo "## F6 — check83.py at the data commit and at the tip"
  for r in e4678921 290cddea 8ac15c41; do
    printf '%s check83: ' "$r"
    git -C "$LANE" ls-tree -r --name-only "$r" -- .ufo/waves/round-44/w1/ScrQualityCriteria/check83.py | wc -l
  done
  echo
  echo "## F4 — the tip receipts at 290cddea and at 8ac15c41"
  for r in 290cddea 8ac15c41; do
    for f in c1-after-tip c2-after-tip axis-tip; do
      printf '%s %s: ' "$r" "$f"
      git -C "$LANE" ls-tree "$r" -- ".ufo/waves/round-44/receipts/$f.txt" | wc -l
    done
  done
  echo
  echo "## D2 gap in the calibration — its own findings list"
  grep -n '^### F' "$LANE/.ufo/waves/round-44/w2/ConnCalibration.md" | cut -c1-60
  echo "\$ grep -c 'after-data' $LANE/.ufo/waves/round-44/w2/ConnCalibration.md   # mentions, none is a finding"
  grep -c 'after-data' "$LANE/.ufo/waves/round-44/w2/ConnCalibration.md"
} > "$R/d7-truths.txt" 2>&1

# QUALITY 83's own checker run against the lesson at the data commit (F5/F6 corroboration)
{
  echo "\$ python3 -I .ufo/waves/round-44/w1/ScrQualityCriteria/check83.py --repo . --rev e4678921 --doc corpus/lessons/round-44.md --prefix .ufo/"
  cd "$LANE" && python3 -I .ufo/waves/round-44/w1/ScrQualityCriteria/check83.py \
    --repo . --rev e46789213830597348fe96a351ae004d10587385 --doc corpus/lessons/round-44.md --prefix .ufo/ 2>&1
  echo "exit=$?"
} > "$R/d7-check83.txt" 2>&1

# locators + quote verification, computed with grep -nF from the manifest
{
  while IFS=$'\t' read -r qid path line quote; do
    hits=$(grep -nF -- "$quote" "$LANE/$path" 2>/dev/null)
    found=$(printf '%s\n' "$hits" | awk -F: -v L="$line" '$1==L' | wc -l)
    if [ "$found" -ge 1 ]; then
      printf '%s\tPASS\t%s:%s\t%s\n' "$qid" "$path" "$line" "$quote"
    else
      printf '%s\tFAIL\t%s:%s\t%s\n' "$qid" "$path" "$line" "$quote"
      printf '  grep -nF hits: %s\n' "$(printf '%s' "$hits" | cut -c1-120 | tr '\n' '|')"
    fi
  done < "$SEAT/quotes.tsv"
} > "$R/quotes-grep.txt" 2>&1

echo "receipts written to $R"
ls -l "$R"
