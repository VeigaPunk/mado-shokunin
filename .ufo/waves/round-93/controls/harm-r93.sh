#!/usr/bin/env bash
# Round-93 harm watch (L1). Run from the lane root with REV = the code tip (the C2 commit); the working tree must equal
# REV for every file the selftests read. Prints each command and its rc. Usage: harm-r93.sh REV SCRATCH
set -u
REV=$1
S=$2
mkdir -p "$S" "$S/mako"  # mado-mako refuses a --scratch-root that does not exist (first run, 2026-11-07)
export TMPDIR="$S"
run() { echo "\$ $*"; "$@" 2>&1 | grep -vE '^(case|probe|fresh|mutant) '; echo "rc=${PIPESTATUS[0]}"; }
echo "# round-93 harm watch at $REV, MadoR93, $(date -u +%FT%TZ)"
run bash tools/mado-verify.sh --selftest
run bash tools/mado-verify.sh --no-live
run python3 -I quality/check-index.py --repo . --rev "$REV"
run python3 -I quality/check-tool-ledger.py --repo . --rev "$REV"
run python3 -I tools/mado-mako.py --selftest --scratch-root "$S/mako"
run python3 -I tools/mado-portals.py --selftest
run python3 -I tools/mado-mime.py --selftest
run python3 -I tools/mado-xdgmime.py --selftest
run python3 -I quality/check-seat-reports.py --selftest
run python3 -I quality/check-receipt-presence.py --selftest
run python3 -I quality/check-selftest-strength.py --selftest
run python3 -I quality/check-selftest-strength.py --tool quality/check-seat-reports.py --kills quality/selftest-kills/check-seat-reports.json --scratch-root "$S/gate"
run python3 -I quality/counters/c2-r90-receipt-presence.py --repo . --rev "$REV" --base-rev 5041acf99e27263872bf0441ad5f9d4316152605 --set .ufo/waves/round-90/controls/receipt-presence-set-r90.json --mutants .ufo/waves/round-90/controls/receipt-mutants-r90.json --expect-set-sha256 f7ab86c25edbb806a9f947af09fab5cf971a42602c252966c0075b9aeefa7939 --expect-mutants-sha256 68b39a805755f7685c00c847a48b0f8f679fdca2710773efb5f4469b7bebe82d --scratch-root "$S/r90c2"
run python3 -I quality/counters/c2-r92-gate-defects.py --repo . --rev "$REV" --base-rev d992ef7494b054591ee9104df1da49264678df5d --battery .ufo/waves/round-92/controls/gate-defects-battery-r92.json --mutants .ufo/waves/round-92/controls/gate-defects-mutants-r92.json --expect-battery-sha256 a0cfaeb36c5423678696629569019dece0d2138dc5e980df0ba7a9ad7ef2fdd6 --expect-mutants-sha256 fe931e76f778e318771486458336d53dbf8933dd5444fa0beba07d53196f1e26 --r91-argv .ufo/waves/round-92/controls/r91-c2-argv-r92.json --expect-r91-argv-sha256 d21b1979b8b42203c8d9c8d033ec71af8027ff79911adc348cddb9685df4b604 --expect-r91-counter-sha256 c74f5baae915a4669ece5033a35ba16f5db0131a2db9a6e83a702de9e932d486 --fresh 60 --scratch-root "$S/r92c2"
echo "# round-90 C1 counter on the ported tool: expected SETUP_ERROR (nine anchors removed by the port; declaration C1 'QUALITY 153')"
run python3 -I quality/counters/c1-r90-portal-routing.py --repo . --rev "$REV" --base-rev 5041acf99e27263872bf0441ad5f9d4316152605 --cases .ufo/waves/round-90/controls/portal-cases-r90.json --mutants .ufo/waves/round-90/controls/portal-mutants-r90.json --expect-cases-sha256 66d4ffff70bd092bd2c900658b3b9a7566f8dedc2aacd4b334102acebc192da2 --expect-mutants-sha256 e761a4e44ec6d8a692d8ac9b2feec7ef8609b4d30f5ed40c11f7c332129c2451 --expect-oracle-binary-sha256 e1429fbe1bf6c2203ba07f478b9e92e9221437b13a92eebafb0982748583a4f8 --scratch-root "$S/r90c1"
echo "\$ git diff --stat 4c6f723f3dca3a26f9d14475d695fe797e2e972c $REV -- tools/mado-mime.py tools/mado-xdgmime.py tools/mado-mako.py tools/mado-verify.sh quality/check-seat-reports.py quality/check-receipt-presence.py"
git diff --stat 4c6f723f3dca3a26f9d14475d695fe797e2e972c "$REV" -- tools/mado-mime.py tools/mado-xdgmime.py tools/mado-mako.py tools/mado-verify.sh quality/check-seat-reports.py quality/check-receipt-presence.py
echo "rc=$? (empty diff = unchanged)"
