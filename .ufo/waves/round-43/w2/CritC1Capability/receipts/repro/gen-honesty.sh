#!/bin/bash
set -u
W=/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-43/w2/CritC1Capability
cd "$W/receipts" || exit 1
OUT=honesty-grep.txt
{
  echo "# What the landed SKILL.md / PROVINCE.md actually say about the C1 tool's support limit"
  echo "# files: receipts/SKILL-data.md, receipts/PROVINCE-data.md (blobs at 1959770657f1f8665097c1aed4be6c1cbb07139f)"
  echo
  echo '$ grep -n "unsupported" SKILL-data.md'
  grep -n "unsupported" SKILL-data.md
  echo
  echo '$ sed -n "246,290p" SKILL-data.md | grep -n "unsupported\\|source\\|match:tag\\|match:title\\|multi"'
  sed -n "246,290p" SKILL-data.md | grep -n "unsupported\|source\|match:tag\|match:title\|multi"
  echo "(no output above = the subsection never names the counter's meaning, source statements, or the tag/title forms)"
  echo
  echo '$ grep -c "match:tag" SKILL-data.md ; grep -c "match:title" SKILL-data.md ; grep -c "windowrulev2" SKILL-data.md'
  grep -c "match:tag" SKILL-data.md; grep -c "match:title" SKILL-data.md; grep -c "windowrulev2" SKILL-data.md
  echo
  echo '$ grep -n "supported" SKILL-data.md'
  grep -n "supported" SKILL-data.md
  echo
  echo '$ sed -n "32p" PROVINCE-data.md | fold -w 200 | head -40'
  sed -n "32p" PROVINCE-data.md | fold -w 200 | head -40
  echo
  echo '$ grep -o "\\`--selftest\\` opens no file and writes nothing[^;]*" PROVINCE-data.md'
  grep -o '`--selftest` opens no file and writes nothing[^;]*' PROVINCE-data.md
  echo
  echo '$ grep -o "at most 1048577 B" PROVINCE-data.md'
  grep -o "at most 1048577 B" PROVINCE-data.md
  echo
  echo '$ grep -o "the matched client is not floating, so the first-map floating branch[^:]*" SKILL-data.md'
  grep -o 'the matched client is not floating, so the first-map floating branch[^:]*' SKILL-data.md
} > "$OUT" 2>&1
cat "$OUT"
