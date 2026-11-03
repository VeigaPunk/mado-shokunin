#!/usr/bin/env bash
# R65ScribeLesson evidence: every claim this seat makes, with its producer rc (QUALITY 26).
set -u
L=/home/vgpnk/Projects/shokunin/mado-shokunin
F=/home/vgpnk/Projects/shokunin
S=/fast/scratch/hyaku/mado-r65/w1/R65ScribeLesson
BASE=524fa1f90b1f2de44b3019bacf833d54e0af13a0
R64BASE=7fe65562c15d20e5cfdc1da536f774149ab52b7e
R64HEAD=66b8994b6397e27904779a26264c0196d2bd0368
LAND=688144573a2605704dfeb2bbca2d5bd6a06bf938

run() { local name="$1"; shift; echo "-- $name"; echo "cmd: $*"; out=$("$@" 2>&1); rc=$?; printf '%s\n' "$out"; echo "rc=$rc"; echo; }

cd "$L" || exit 1
echo "== R65ScribeLesson evidence, $(date -u +%Y-%m-%dT%H:%M:%SZ), base $BASE =="
echo

run "m1 numstat r64 range" bash -c "git diff-tree -r --numstat $R64BASE $R64HEAD | awk '{f++; a+=\$1; d+=\$2} END {print \"files=\"f\" added=\"a\" deleted=\"d}'"
run "m1 receipt files at r64 landing" bash -c "git ls-tree -r --name-only $LAND -- .ufo/waves/round-64/receipts/ | wc -l"
run "m1 receipt files across r64 range" bash -c "git diff-tree -r --name-only $R64BASE $R64HEAD -- .ufo/waves/round-64/receipts/ | wc -l"
run "m1 report prose (fleet root, read-only)" bash -c "grep -n '18 round-64 receipt files\|30 files, +1192' $F/.ufo/reports/round-64/mado.md"

echo "== m3 selftest pinned totals (host-conditional) =="
run "ledger selftest" python3 quality/check-tool-ledger.py --selftest --scratch-root "$S/st-ledger"
run "wave-done selftest" python3 quality/check-wave-done.py --selftest --scratch-root "$S/st-wave"
run "ledger pin line" bash -c "grep -n 'SELFTEST_CHECKS' quality/check-tool-ledger.py"
run "wave-done pin line" bash -c "grep -n 'SELFTEST_CHECKS' quality/check-wave-done.py"
run "r64 counts for contrast" bash -c "grep -n 'LEDGER_SELFTEST\|MADO_WAVE_DONE_SELFTEST' .ufo/waves/round-64/receipts/before-state-r64.txt"

echo "== m2 register: r57 probe column =="
run "r57 register rows" bash -c "grep -cE '^\| .* \| (absent|observed) \(2026-10-31\) \|' PROVINCE.md"
run "stale-row grep" bash -c "grep -c 'absent (2026-10-31)' PROVINCE.md"
run "r65 probe receipt lines" bash -c "sed -n '/== surface probes this host/,/== versions/p' .ufo/waves/round-65/receipts/before-register-probes-r65.txt"

echo "== m65-2 version probes, attributed (this host, read-only) =="
run "hyprctl version" hyprctl version
run "walker --version" walker --version
run "omarchy version" omarchy version
run "omarchy --version (wrong flag shape)" omarchy --version

echo "== Gate host anchors =="
run "registry rows at base" bash -c "grep -cE '^ {0,3}\|[[:space:]]*S[0-9]{3,}' corpus/SOURCES.md"
run "S028 row" bash -c "grep -nE '^\| *S028 *\|' corpus/SOURCES.md | cut -c1-200"
run "S097 recheck cell" bash -c "grep -E '^\| *S097 *\|' corpus/SOURCES.md | awk -F'|' '{print \$9\" | \"\$10}'"

echo "== census start receipt counts =="
run "census W04" bash -c "grep -c W04 .ufo/waves/round-65/receipts/census-start-r65.txt"
run "census W01" bash -c "grep -c W01 .ufo/waves/round-65/receipts/census-start-r65.txt"

echo "== gate receipts: verdict lines =="
run "fileplane verdict" bash -c "grep -E '^counts:|^MADO_VERIFY:' .ufo/waves/round-65/receipts/gate-fileplane-r65.txt"
run "live verdict" bash -c "grep -E '^counts:|^MADO_VERIFY:' .ufo/waves/round-65/receipts/gate-live-r65.txt"
echo "== end =="
