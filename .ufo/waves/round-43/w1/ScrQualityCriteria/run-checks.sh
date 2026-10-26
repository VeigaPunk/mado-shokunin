#!/usr/bin/env bash
# ScrQualityCriteria (round 43, w1) — re-derive the four round-42 evidence pointers, read-only.
# Inputs are committed bytes or seat-local copies with a recorded sha256; nothing here writes the lane.
# Run: bash run-checks.sh > receipts.txt 2>&1
L=/home/vgpnk/Projects/shokunin/mado-shokunin
F=/home/vgpnk/Projects/shokunin
SEAT=$L/.ufo/waves/round-43/w1/ScrQualityCriteria
cd "$L" || exit 2
run() { echo "\$ $*"; bash -c "$*"; echo "exit=$?"; echo; }

echo "== 0. ambient (lane HEAD, seat inputs) =="
run 'git rev-parse HEAD'
run "sha256sum $SEAT/LOG-at-5add5b4.md; git show 5add5b45a65ddaa18fad00c6afa9dbfda29ee0b0:LOG.md | sha256sum"
run "sha256sum $F/.ufo/reports/round-42/mado.md; (cd $F && git show da384db4:.ufo/reports/round-42/mado.md | sha256sum)"

echo "== 1. QUALITY.md shape (form of criteria 60-76; next free number) =="
run "wc -l corpus/QUALITY.md"
run "grep -c '^[0-9]\\+\\. ' corpus/QUALITY.md"
run "grep -n '^## ' corpus/QUALITY.md | tail -3"

echo "== 2. (a) locator typed in prose: the control shows MISS, then OK on the corrected copy =="
run "PYTHONDONTWRITEBYTECODE=1 python3 -I .ufo/waves/round-43/w1/ExecLocatorGate/check-locators.py --fetch .ufo/waves/round-43/fetch .ufo/waves/round-42/registration.md"
run "PYTHONDONTWRITEBYTECODE=1 python3 -I .ufo/waves/round-43/w1/ExecLocatorGate/check-locators.py --fetch .ufo/waves/round-43/fetch .ufo/waves/round-43/w1/ExecLocatorGate/registration-r42-corrected.md"
run "PYTHONDONTWRITEBYTECODE=1 python3 -I .ufo/waves/round-43/w1/ExecLocatorGate/check-locators.py --fetch .ufo/waves/round-43/fetch $SEAT/LOG-at-5add5b4.md $F/.ufo/reports/round-42/mado.md"
echo "-- the cited ranges carry no GEOMETRIC_GOAL; the true ranges do --"
run "for r in 394,395 412,413 426,428 447,448; do printf 'range %s: %s lines\\n' \"\$r\" \"\$(sed -n \"\${r}p\" .ufo/waves/round-43/fetch/Hyprland-HyprCtl.cpp | grep -c GEOMETRIC_GOAL)\"; done"
run "sed -n '394,395p;412,413p' .ufo/waves/round-43/fetch/Hyprland-HyprCtl.cpp"
run "grep -n 'negative:\\|FullMatch' .ufo/waves/round-43/fetch/Hyprland-RegexMatchEngine.cpp"

echo "== 3. (b) control tally: three numbers, two definitions =="
R=.ufo/waves/round-42/receipts/ctl-c1.txt
run "grep -c '^ok  ' $R"
run "for p in REF BASE\\-absent D K M; do printf '%s=%s\\n' \"\$p\" \"\$(grep -cE \"^ok  \${p}\" $R)\"; done"
run "head -1 $R"
run "grep 'VERDICT' $R"
run "grep -n 'controls=%d' .ufo/waves/round-42/ctl/run-c1-controls.py"
echo "-- the round-42 report's own breakdown --"
run "(cd $F && git show da384db4:.ufo/reports/round-42/mado.md) | sed -n '28p' | grep -o '46 controls[^.]*'"
echo "-- the repaired statement (round-43 registration) --"
run "sed -n '59p' .ufo/waves/round-43/registration.md | grep -o '48 .ok. lines[^;]*'"

echo "== 4. (c) pointer to a run: round-42 box 2, and the round-43 recurrence =="
run "(cd $F && git show da384db4:.ufo/reports/round-42/mado.md) | sed -n '45p' | grep -o 'is recorded in [^;]*'"
echo "-- the pointer's target is the LOG Round 42 section; the run is not in it (committed bytes at a62f2e0) --"
run "git show a62f2e0c3a5d1737bcf93ac45ae98a1b195e1341:LOG.md | sed -n '/^## Round 42/,/^## Round 43/p' | grep -c 'NO_MATCHING_CLIENT'"
run "git show a62f2e0c3a5d1737bcf93ac45ae98a1b195e1341:LOG.md | grep -c 'NO_MATCHING_CLIENT'"
echo "-- round-43 recurrence: LOG.md:2490 names a receipt that is untracked and absent at freeze and at HEAD --"
run "grep -n 'SHONEN box 2 receipt' LOG.md | cut -c1-100"
run "sed -n '2490p' LOG.md | grep -o '\\.ufo/waves/round-43/receipts/[a-z-]*\\.txt'"
run "sha256sum LOG.md"
run "git status --porcelain -- LOG.md"
run "git cat-file -e b2e2efd6e268920d31f3c32cf52dc097dd6e1d22:.ufo/waves/round-43/receipts/live-geometry-host.txt && echo AT_FREEZE || echo ABSENT_AT_FREEZE"
run "git cat-file -e HEAD:.ufo/waves/round-43/receipts/live-geometry-host.txt && echo AT_HEAD || echo NOT_AT_HEAD"
run "git status --porcelain -- .ufo/waves/round-43/receipts/live-geometry-host.txt"
run "grep -n 'verdict=\\|exit=\\|^\\$ ' .ufo/waves/round-43/receipts/live-geometry-host.txt | cut -c1-90"

echo "== 5. (d) excerpt header range against the command that cut it =="
run "wc -l /home/vgpnk/Projects/gkeep/gkeep/ui.py"
run "head -1 .ufo/waves/round-42/fetch/gkeep-ui-excerpt.py"
run "head -1 .ufo/waves/round-43/fetch/gkeep-ui-excerpt.py"
run "wc -l .ufo/waves/round-42/fetch/gkeep-ui-excerpt.py .ufo/waves/round-43/fetch/gkeep-ui-excerpt.py"
run "printf 'body42=%s body43=%s src=%s\\n' \"\$(tail -n +3 .ufo/waves/round-42/fetch/gkeep-ui-excerpt.py | wc -l)\" \"\$(tail -n +3 .ufo/waves/round-43/fetch/gkeep-ui-excerpt.py | wc -l)\" \"\$(sed -n '446,\$p' /home/vgpnk/Projects/gkeep/gkeep/ui.py | wc -l)\""
run "diff <(tail -n +3 .ufo/waves/round-43/fetch/gkeep-ui-excerpt.py) <(sed -n '446,\$p' /home/vgpnk/Projects/gkeep/gkeep/ui.py) && echo BODY43_EQUAL_SOURCE_RANGE"
run "diff <(tail -n +3 .ufo/waves/round-42/fetch/gkeep-ui-excerpt.py) <(sed -n '446,488p' /home/vgpnk/Projects/gkeep/gkeep/ui.py)"
run "sed -n '59p' .ufo/waves/round-42/registration.md | grep -o 'lines [0-9-]* of'"

echo "== 6. receipt format across rounds (scope note for criterion 79) =="
run "for f in .ufo/waves/round-42/receipts/*.txt; do printf '%s cmd=%s exit=%s\\n' \"\$f\" \"\$(grep -c '^\\\$ ' \$f)\" \"\$(grep -c '^exit=' \$f)\"; done"
run "for f in .ufo/waves/round-41/receipts/harm-tip.txt .ufo/waves/round-41/receipts/ctl-c1-v2.txt .ufo/waves/round-41/receipts/ctl-c2-v2.txt; do printf '%s cmd=%s exit=%s\\n' \"\$f\" \"\$(grep -c '^\\\$ ' \$f)\" \"\$(grep -c '^exit=' \$f)\"; done"

echo "== 7. the control criterion 77 names (ExecLocatorGate) is in flight, not a passed receipt =="
run "ls .ufo/waves/round-43/w1/ExecLocatorGate/"
run "test -f .ufo/waves/round-43/w1/ExecLocatorGate/receipt.txt && echo RECEIPT_PRESENT || echo NO_RECEIPT_YET"
