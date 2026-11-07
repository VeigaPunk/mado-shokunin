#!/usr/bin/env bash
# Round-95 harm watch (seat R95MExecHostC1). Run from the lane root with REV = the code tip; the working tree must equal
# REV for every file the selftests read. Same watch as round 94 (controls/harm-r94.sh, incl. its L1 additions) plus the
# C1 candidate's selftest: MIMESNIFF (default tools/mado-mimesniff.py; at base pass a scratch copy of
# .ufo/waves/round-95/build/mado-mimesniff.c1.py sitting next to a copy of tools/mado-mimeglob.py).
# Read-only in the lane: every writable component gets a scratch root under SCRATCH. Prints each command and its rc.
# Usage: R95MExecHostC1-harm.sh REV SCRATCH
set -u
REV=$1
S=$2
mkdir -p "$S" "$S/mako" "$S/gate" "$S/r90c2" "$S/r92c2" "$S/r90c1"
export TMPDIR="$S"
run() { echo "\$ $*"; "$@" 2>&1 | grep -vE '^(case|probe|fresh|mutant) '; echo "rc=${PIPESTATUS[0]}"; }
echo "# round-95 harm watch at $REV (base 4a2af6817024f6ed47084a5217c1825ae247f4fe), R95MExecHostC1, $(date -u +%FT%TZ)"
run bash tools/mado-verify.sh --selftest
run bash tools/mado-verify.sh --no-live
run python3 -I quality/check-index.py --repo . --rev "$REV"
run python3 -I quality/check-tool-ledger.py --repo . --rev "$REV"
run python3 -I tools/mado-mako.py --selftest --scratch-root "$S/mako"
run python3 -I tools/mado-portals.py --selftest
run python3 -I tools/mado-mime.py --selftest
run python3 -I tools/mado-xdgmime.py --selftest
run python3 -I tools/mado-mimeglob.py --selftest
if [ -n "${MIMESNIFF:-}" ] && [ -f "$MIMESNIFF" ]; then
  run python3 -I "$MIMESNIFF" --selftest
else
  echo "SKIP python3 -I tools/mado-mimesniff.py --selftest (absent at $REV: C1 candidate not integrated yet; set MIMESNIFF to a scratch copy next to mado-mimeglob.py) rc=NA"
fi
run python3 -I quality/check-seat-reports.py --selftest
run python3 -I quality/check-receipt-presence.py --selftest
run python3 -I quality/check-selftest-strength.py --selftest
run python3 -I quality/check-selftest-strength.py --tool quality/check-seat-reports.py --kills quality/selftest-kills/check-seat-reports.json --scratch-root "$S/gate"
run python3 -I quality/check-selftest-strength.py --tool tools/mado-xdgmime.py --kills quality/selftest-kills/mado-xdgmime.json --scratch-root "$S/gate"
run python3 -I quality/check-selftest-strength.py --tool tools/mado-mime.py --kills quality/selftest-kills/mado-mime.json --scratch-root "$S/gate"
run python3 -I quality/counters/c2-r90-receipt-presence.py --repo . --rev "$REV" --base-rev 5041acf99e27263872bf0441ad5f9d4316152605 --set .ufo/waves/round-90/controls/receipt-presence-set-r90.json --mutants .ufo/waves/round-90/controls/receipt-mutants-r90.json --expect-set-sha256 f7ab86c25edbb806a9f947af09fab5cf971a42602c252966c0075b9aeefa7939 --expect-mutants-sha256 68b39a805755f7685c00c847a48b0f8f679fdca2710773efb5f4469b7bebe82d --scratch-root "$S/r90c2"
run python3 -I quality/counters/c2-r92-gate-defects.py --repo . --rev "$REV" --base-rev d992ef7494b054591ee9104df1da49264678df5d --battery .ufo/waves/round-92/controls/gate-defects-battery-r92.json --mutants .ufo/waves/round-92/controls/gate-defects-mutants-r92.json --expect-battery-sha256 a0cfaeb36c5423678696629569019dece0d2138dc5e980df0ba7a9ad7ef2fdd6 --expect-mutants-sha256 fe931e76f778e318771486458336d53dbf8933dd5444fa0beba07d53196f1e26 --r91-argv .ufo/waves/round-92/controls/r91-c2-argv-r92.json --expect-r91-argv-sha256 d21b1979b8b42203c8d9c8d033ec71af8027ff79911adc348cddb9685df4b604 --expect-r91-counter-sha256 c74f5baae915a4669ece5033a35ba16f5db0131a2db9a6e83a702de9e932d486 --fresh 60 --scratch-root "$S/r92c2"
echo "# round-90 C1 counter on the ported tool: expected SETUP_ERROR (nine anchors removed by the port; declaration 'QUALITY 153')"
run python3 -I quality/counters/c1-r90-portal-routing.py --repo . --rev "$REV" --base-rev 5041acf99e27263872bf0441ad5f9d4316152605 --cases .ufo/waves/round-90/controls/portal-cases-r90.json --mutants .ufo/waves/round-90/controls/portal-mutants-r90.json --expect-cases-sha256 66d4ffff70bd092bd2c900658b3b9a7566f8dedc2aacd4b334102acebc192da2 --expect-mutants-sha256 e761a4e44ec6d8a692d8ac9b2feec7ef8609b4d30f5ed40c11f7c332129c2451 --expect-oracle-binary-sha256 e1429fbe1bf6c2203ba07f478b9e92e9221437b13a92eebafb0982748583a4f8 --scratch-root "$S/r90c1"
echo "\$ git diff --stat 4c6f723f3dca3a26f9d14475d695fe797e2e972c $REV -- tools/mado-mime.py tools/mado-xdgmime.py tools/mado-mako.py tools/mado-verify.sh quality/check-seat-reports.py quality/check-receipt-presence.py"
git diff --stat 4c6f723f3dca3a26f9d14475d695fe797e2e972c "$REV" -- tools/mado-mime.py tools/mado-xdgmime.py tools/mado-mako.py tools/mado-verify.sh quality/check-seat-reports.py quality/check-receipt-presence.py
echo "rc=$? (empty diff = the six protected tools are unchanged since 4c6f723f)"
echo "\$ git diff --stat 4a2af6817024f6ed47084a5217c1825ae247f4fe $REV -- tools/ quality/"
git diff --stat 4a2af6817024f6ed47084a5217c1825ae247f4fe "$REV" -- tools/ quality/
echo "rc=$? (empty diff = tools/ and quality/ byte-equal to the round-95 base)"
# L1: when quality/counters/c1-r95-mimesniff.py and quality/counters/c2-r95-selftest-kills.py land, append their runs here (round-94 pattern; see harm-final-r94.txt's L1 additions for the shape).
