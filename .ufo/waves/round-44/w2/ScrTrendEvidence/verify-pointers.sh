#!/usr/bin/env bash
# ScrTrendEvidence pointer verifier (round 44, w2). Read-only.
# Every locator the report cites is emitted here by grep -n, never typed.
set -u
cd /home/vgpnk/Projects/shokunin/mado-shokunin || exit 2
fail=0

one() { # name file regex [must-contain]
  local name="$1" f="$2" re="$3" must="${4:-}"
  local hits n line
  hits=$(grep -nE -- "$re" "$f" 2>/dev/null)
  n=$(printf '%s\n' "$hits" | grep -c . )
  if [ "$n" -ne 1 ]; then
    echo "PTR $name file=$f re=$re hits=$n verdict=MISS"
    fail=1; return
  fi
  line=$(printf '%s' "$hits" | cut -d: -f1)
  if [ -n "$must" ] && ! printf '%s' "$hits" | grep -qF -- "$must"; then
    echo "PTR $name file=$f line=$line MISSING_TOKEN=$must verdict=MISS"
    fail=1; return
  fi
  echo "PTR $name file=$f line=$line verdict=OK"
}

count() { # name file regex expect
  local name="$1" f="$2" re="$3" exp="$4" got
  got=$(grep -cE -- "$re" "$f" 2>/dev/null)
  if [ "$got" = "$exp" ]; then echo "CNT $name file=$f re=$re got=$got expect=$exp verdict=OK"
  else echo "CNT $name file=$f re=$re got=$got expect=$exp verdict=MISS"; fail=1; fi
}

git show 6a1a905:corpus/README.md > .ufo/waves/round-44/w2/ScrTrendEvidence/README_base.txt

# --- expansion: coverage map, registry rows, capability
one index_row corpus/README.md 'MADO-R44-1' 'knowledge/hyprland-gkeep-size-request-r44.md'
one frontier corpus/README.md '^### Round-44 gkeep size-request route'
one frontier_rows corpus/README.md 'rows S164 plus S298-S301'
one s298 corpus/SOURCES.md '^\| S298 ' 'hyprland-gkeep-size-request-r44.md'
one s299 corpus/SOURCES.md '^\| S299 ' 'hyprland-gkeep-size-request-r44.md'
one s300 corpus/SOURCES.md '^\| S300 ' 'hyprland-gkeep-size-request-r44.md'
one s301 corpus/SOURCES.md '^\| S301 ' 'hyprland-gkeep-size-request-r44.md'
one s164 corpus/SOURCES.md '^\| S164 ' 'hyprland-gkeep-size-request-r44.md'
count src_lines corpus/knowledge/hyprland-gkeep-size-request-r44.md '^source: S(164|298|299|300|301) ' 5
one cap_head SCORECARD.md '^### Capabilities \(round 44\)'
one cap_row SCORECARD.md 'state-aware rule size versus reported size join' 'NOT_COMPARED'
one base_open .ufo/waves/round-44/w2/ScrTrendEvidence/README_base.txt 'acknowledgement path' 'rule attribution'

# --- quality: freshness, corrections, correction notes, errata, stale flags
one entry_verified corpus/knowledge/hyprland-gkeep-size-request-r44.md '^verified-at: 2026-10-26'
one entry_recheck corpus/knowledge/hyprland-gkeep-size-request-r44.md '^recheck: 90d'
one entry_ground corpus/knowledge/hyprland-gkeep-size-request-r44.md '^ground: ' 'hyprland-gkeep-geometry-r43.md'
one predecessor corpus/knowledge/hyprland-gkeep-size-request-r44.md '^## What the staged predecessor said'
one pred_b1 corpus/knowledge/hyprland-gkeep-size-request-r44.md '^- It names the request' 'xdg_toplevel.set_size'
one pred_b2 corpus/knowledge/hyprland-gkeep-size-request-r44.md '^- It reads the ack list'
one pred_b3 corpus/knowledge/hyprland-gkeep-size-request-r44.md '^- It says a GTK 4 window'
one skill_tiled_false SKILL.md 'is false for a pseudo-tiled client'
one skill_tiled_note SKILL.md 'read TILED as' 'not floating" only'
one skill_tiled_row SKILL.md '^\| TILED \|' 'the tiler, not the floating rule path'
one skill_fs_row SKILL.md '^\| FULLSCREEN \(round 44\)' 'fullscreen` field is 2'
one skill_max_row SKILL.md '^\| MAXIMIZED \(round 44\)'
one skill_nc_row SKILL.md '^\| NOT_COMPARED \(rc 5' 'no comparison was made'
one skill_exitnote SKILL.md '^Round 44 adds exit 5'
one m44_3 corpus/lessons/round-44.md '^\*\*M44-3 '
one m44_4 corpus/lessons/round-44.md '^\*\*M44-4 '
one m44_4_cap corpus/lessons/round-44.md "Captured-by: round-43's non-author closure"
one m44_8 corpus/lessons/round-44.md '^\*\*M44-8 '
one m44_8_cap corpus/lessons/round-44.md 'Captured-by: \*\*none\*\* for four rounds'
one skill_usage_158 SKILL.md '^\| Does the size a window rule asks for match'
one skill_usage_225 SKILL.md 'whether a `windowrule = size W H, match:class RX` line'
one stale_flag .ufo/waves/round-44/w1/ScoutCoverage.md 'stale sentences' 'SKILL.md:158,225'
one r43_pointer corpus/knowledge/hyprland-gkeep-geometry-r43.md 'ExecOracleGkeep' 'gkeep-shm.c'
one id_receipt_fetch .ufo/waves/round-44/w1/CritAssimilation/id-receipts.txt 'd735d454cc4b7983f19626514d310669047da46780c509ffae68ccf072211ded  \.ufo/waves/round-44/fetch/Hyprland-Window.cpp'
one id_receipt_tag .ufo/waves/round-44/w1/CritAssimilation/id-receipts.txt 'd735d454.*tag-window.cpp'

# --- discernment: gate decisions, spot-check placeholders, criteria + lessons
one gate_head corpus/lessons/round-44.md '^## Gate$'
one admit corpus/lessons/round-44.md '^ADMIT ' 'gkeep-client-size-request-r12.md'
count refuses corpus/lessons/round-44.md '^REFUSE ' 4
one spot_head corpus/lessons/round-44.md '^## Spot-check'
count spot_placeholders corpus/lessons/round-44.md '\(closure\)' 4
one closure_items corpus/lessons/round-44.md '^## Round-43 closure items'
count trend_words corpus/lessons/round-44.md 'expansion|discernment' 0
one entry_assim corpus/knowledge/hyprland-gkeep-size-request-r44.md '^assimilated-from:' 'gkeep-client-size-request-r12.md'
one errata_head corpus/lessons/round-44.md '^## Round-43 errata'
one scout_base_ground .ufo/waves/round-44/w1/ScoutCoverage.md '^Base 6a1a905: zero hits'
one harm_scope .ufo/waves/round-44/w1/ExecHarmBase.md 'no-harm verdict is the integrating seat'
one r43_spot corpus/lessons/round-43-verifier-spotcheck.md '^## 4\. Discernment spot-check'
one r43_trends corpus/lessons/round-43-verifier-spotcheck.md '^## 5\. Trend verdicts'
one reg_c2_resid .ufo/waves/round-44/registration-v2.md 'Residuals \(declared\):\*\* claim-to-quote binding' 'non-author reading'
one r43_exp corpus/lessons/round-43-verifier-spotcheck.md '^- \*\*expansion: improved\*\*'
one r43_qual corpus/lessons/round-43-verifier-spotcheck.md '^- \*\*quality: improved\*\*'
one r43_disc corpus/lessons/round-43-verifier-spotcheck.md '^- \*\*discernment: improved\*\*'
one learn_trends /home/vgpnk/Projects/kimi-shokunin/skills/shokunin/protocol/LEARNING.md '^## The three trends'
one learn_vocab /home/vgpnk/Projects/kimi-shokunin/skills/shokunin/protocol/LEARNING.md '^`unprovable-but-better`\); no trend is a scalar'
one learn_exp /home/vgpnk/Projects/kimi-shokunin/skills/shokunin/protocol/LEARNING.md '^\| \*\*expansion\*\*'
one learn_qual /home/vgpnk/Projects/kimi-shokunin/skills/shokunin/protocol/LEARNING.md '^\| \*\*quality\*\*'
one learn_disc /home/vgpnk/Projects/kimi-shokunin/skills/shokunin/protocol/LEARNING.md '^\| \*\*discernment\*\*'
one learn_trade /home/vgpnk/Projects/kimi-shokunin/skills/shokunin/protocol/LEARNING.md '^Growth without quality is not learning'
one learn_lane /home/vgpnk/Projects/kimi-shokunin/skills/shokunin/protocol/LEARNING.md '^dispatched is still the lane'
one c82 corpus/QUALITY.md '^82\. ' '(lesson: lessons/round-44.md `## considerthese`'
one c83 corpus/QUALITY.md '^83\. ' 'M44-4; round-43 closure D4'
one c84 corpus/QUALITY.md '^84\. ' '(lesson: lessons/round-44.md M44-8)'
one considerthese corpus/lessons/round-44.md '^## considerthese'

# --- receipts (committed counts, not re-run)
one c1_line .ufo/waves/round-44/receipts/c1-after-data.txt '^PRED-C1-r44-v2: fixtures=26/26 tool=present verdict=TARGET_MET'
one c1_exit .ufo/waves/round-44/receipts/c1-after-data.txt '^exit=0$'
one c2_line .ufo/waves/round-44/receipts/c2-after-data.txt '^PRED-C2-r44-v2: admitted=1/1 verdict=TARGET_MET'
one c2_exit .ufo/waves/round-44/receipts/c2-after-data.txt '^exit=0$'
one c2_c_s301 .ufo/waves/round-44/receipts/c2-after-data.txt 'clause=c id=S301 new=1 status=mined used=1 ok=1'
count c2_c_rows .ufo/waves/round-44/receipts/c2-after-data.txt 'clause=c id=S' 5
one ctl_c1 .ufo/waves/round-44/receipts/ctl-c1-v2.txt '^CTL_C1v2 VERDICT: PASS \(controls scoring TARGET_MET: 0 of 20; reference met: 1\)$'
one ctl_c2 .ufo/waves/round-44/receipts/ctl-c2-v2.txt '^CTL_C2v2 VERDICT: PASS \(wrong=0 of 11; positive admitted=1\)$'
one axis .ufo/waves/round-44/receipts/axis-data.txt '^MADO_AXIS: checked=3 mismatched=0' 'rev=e4678921'
one census .ufo/waves/round-44/receipts/census-after-data.txt '^mado[[:space:]]+ok[[:space:]]' 'corpus/SOURCES.md'
count pins .ufo/waves/round-44/receipts/fetch-sha256.txt '^[0-9a-f]{64} ' 8
one c2_before .ufo/waves/round-44/receipts/c2-v2-before-base.txt '^PRED-C2-r44-v2: admitted=0/1 verdict=TARGET_MISSED' 'rev=6a1a905'
one c2_ground .ufo/waves/round-44/receipts/c2-ground-base.txt '^\$ git grep -ciE' 'corpus/knowledge PROVINCE.md SKILL.md tools'
one f3 .ufo/waves/round-44/w1/CritClaimSizing.md '^\*\*F3 ' 'ground is legitimate'

# --- computed counts (git/cat)
idx_base=$(git show 6a1a905:corpus/README.md | grep -c '^| `knowledge/')
idx_data=$(git show e4678921:corpus/README.md | grep -c '^| `knowledge/')
echo "CNT index_rows base=$idx_base data=$idx_data verdict=$([ "$idx_base" = 60 ] && [ "$idx_data" = 61 ] && echo OK || echo MISS)"
{ [ "$idx_base" = 60 ] && [ "$idx_data" = 61 ]; } || fail=1
eg_at_r43=$(git ls-tree -r --name-only 1959770 .ufo/waves/round-43/w1/ExecOracleGkeep/ | grep -c .)
eg_at_tip=$(git ls-tree -r --name-only 290cddea .ufo/waves/round-43/w1/ExecOracleGkeep/ | grep -c .)
echo "CNT execoracle r43data=$eg_at_r43 tip=$eg_at_tip verdict=$([ "$eg_at_r43" = 0 ] && [ "$eg_at_tip" -gt 0 ] && echo OK || echo MISS)"
{ [ "$eg_at_r43" = 0 ] && [ "$eg_at_tip" -gt 0 ]; } || fail=1
vfile=$(ls corpus/lessons/round-44-verifier-spotcheck.md 2>/dev/null | grep -c .)
echo "CNT round44_verifier_file present=$vfile verdict=$([ "$vfile" = 0 ] && echo OK || echo MISS)"
[ "$vfile" = 0 ] || fail=1
idx_entries=$(grep -c '^| `knowledge/' corpus/README.md)
echo "CNT knowledge_index_worktree=$idx_entries expect=61 verdict=$([ "$idx_entries" = 61 ] && echo OK || echo MISS)"
[ "$idx_entries" = 61 ] || fail=1

kd=$(git diff --name-status 6a1a905 e4678921 -- corpus/knowledge/ | tr '\t' ' ')
echo "CNT knowledge_diff=[$kd] expect=[A corpus/knowledge/hyprland-gkeep-size-request-r44.md] verdict=$([ "$kd" = "A corpus/knowledge/hyprland-gkeep-size-request-r44.md" ] && echo OK || echo MISS)"
[ "$kd" = "A corpus/knowledge/hyprland-gkeep-size-request-r44.md" ] || fail=1
v26=$(grep -l '^verified-at: 2026-10-26' corpus/knowledge/*.md | wc -l)
echo "CNT verified_2026_10_26 entries=$v26 expect=2 verdict=$([ "$v26" = 2 ] && echo OK || echo MISS)"
[ "$v26" = 2 ] || fail=1
echo "PTRCHECK verdict=$([ $fail = 0 ] && echo PASS || echo FAIL)"
exit $fail
