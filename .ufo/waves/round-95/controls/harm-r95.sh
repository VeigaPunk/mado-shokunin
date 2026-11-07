#!/usr/bin/env bash
# Round-95 harm watch (L1 MadoR95a3). Run from the lane root with REV = the code tip; the working tree must equal
# REV for every file the selftests read. Same watch as round-94 (controls/harm-r94.sh) plus the new C1 tool's
# selftest (tools/mado-mimesniff.py). Prints each command and its rc. Usage: harm-r95.sh REV SCRATCH
set -u
REV=$1
S=$2
mkdir -p "$S" "$S/mako" "$S/gate" "$S/r90c2" "$S/r92c2" "$S/r90c1" "$S/r94c1" "$S/r94c2" "$S/r93c2" "$S/gate-mg" "$S/gate-pt"  # mado-mako refuses a missing --scratch-root (round-93 correction)
export TMPDIR="$S"
run() { echo "\$ $*"; "$@" 2>&1 | grep -vE '^(case|probe|fresh|mutant) '; echo "rc=${PIPESTATUS[0]}"; }
echo "# round-95 harm watch at $REV, MadoR95a3, $(date -u +%FT%TZ)"
run bash tools/mado-verify.sh --selftest
run bash tools/mado-verify.sh --no-live
run python3 -I quality/check-index.py --repo . --rev "$REV"
run python3 -I quality/check-tool-ledger.py --repo . --rev "$REV"
run python3 -I tools/mado-mako.py --selftest --scratch-root "$S/mako"
run python3 -I tools/mado-portals.py --selftest
run python3 -I tools/mado-mime.py --selftest
run python3 -I tools/mado-xdgmime.py --selftest
run python3 -I tools/mado-mimeglob.py --selftest
run python3 -I tools/mado-mimesniff.py --selftest
run python3 -I quality/check-seat-reports.py --selftest
run python3 -I quality/check-receipt-presence.py --selftest
run python3 -I quality/check-selftest-strength.py --selftest
run python3 -I quality/check-selftest-strength.py --tool quality/check-seat-reports.py --kills quality/selftest-kills/check-seat-reports.json --scratch-root "$S/gate"
run python3 -I quality/counters/c2-r90-receipt-presence.py --repo . --rev "$REV" --base-rev 5041acf99e27263872bf0441ad5f9d4316152605 --set .ufo/waves/round-90/controls/receipt-presence-set-r90.json --mutants .ufo/waves/round-90/controls/receipt-mutants-r90.json --expect-set-sha256 f7ab86c25edbb806a9f947af09fab5cf971a42602c252966c0075b9aeefa7939 --expect-mutants-sha256 68b39a805755f7685c00c847a48b0f8f679fdca2710773efb5f4469b7bebe82d --scratch-root "$S/r90c2"
run python3 -I quality/counters/c2-r92-gate-defects.py --repo . --rev "$REV" --base-rev d992ef7494b054591ee9104df1da49264678df5d --battery .ufo/waves/round-92/controls/gate-defects-battery-r92.json --mutants .ufo/waves/round-92/controls/gate-defects-mutants-r92.json --expect-battery-sha256 a0cfaeb36c5423678696629569019dece0d2138dc5e980df0ba7a9ad7ef2fdd6 --expect-mutants-sha256 fe931e76f778e318771486458336d53dbf8933dd5444fa0beba07d53196f1e26 --r91-argv .ufo/waves/round-92/controls/r91-c2-argv-r92.json --expect-r91-argv-sha256 d21b1979b8b42203c8d9c8d033ec71af8027ff79911adc348cddb9685df4b604 --expect-r91-counter-sha256 c74f5baae915a4669ece5033a35ba16f5db0131a2db9a6e83a702de9e932d486 --fresh 60 --scratch-root "$S/r92c2"
echo "# round-90 C1 counter on the ported tool: expected SETUP_ERROR (nine anchors removed by the port; declaration 'QUALITY 153')"
run python3 -I quality/counters/c1-r90-portal-routing.py --repo . --rev "$REV" --base-rev 5041acf99e27263872bf0441ad5f9d4316152605 --cases .ufo/waves/round-90/controls/portal-cases-r90.json --mutants .ufo/waves/round-90/controls/portal-mutants-r90.json --expect-cases-sha256 66d4ffff70bd092bd2c900658b3b9a7566f8dedc2aacd4b334102acebc192da2 --expect-mutants-sha256 e761a4e44ec6d8a692d8ac9b2feec7ef8609b4d30f5ed40c11f7c332129c2451 --expect-oracle-binary-sha256 e1429fbe1bf6c2203ba07f478b9e92e9221437b13a92eebafb0982748583a4f8 --scratch-root "$S/r90c1"
run python3 -I quality/counters/c1-r94-mimeglob.py --repo . --rev "$REV" --base-rev a3de997289014e7dbf1d73ae206be1d6f8cdadd0 --cases .ufo/waves/round-94/controls/mimeglob-cases-r94-frozen.json --expect-cases-sha256 c7b693d240479ed63af24f426ae184bc4a13489a38f587620d9e1224dca5856c --mutants .ufo/waves/round-94/controls/mimeglob-mutants-r94-frozen.json --expect-mutants-sha256 0e74c57d233d2440f903466e959488705a58fdcda4f14d920caef0d2859133c2 --oracle-src .ufo/waves/round-94/controls/mimeglob-oracle-r94.c --expect-oracle-sha256 9c4337b36f93fa71bce13938f93d2e9758bb752815a67c57eb934a70bbfa6b11 --fresh-gen .ufo/waves/round-94/controls/mimeglob-fresh-r94.py --expect-fresh-gen-sha256 ab76b97e0c37d92ddb0b03a733745b1089be2a083379d9cabee050689ed57e2c --host-names .ufo/waves/round-94/controls/mimeglob-host-names-r94.txt --expect-host-names-sha256 4b6d6a6cc67a4ad59eb91c9e8af1cc605f2f278d2a2ecf57b4a81edad9344fa3 --expect-tool-sha256 65f80a6cb1551bb722ae7608df04fb17deba1b5cd05bef6f7fdd79bed76e2453 --fresh 120 --workers 24 --scratch-root "$S/r94c1"
run python3 -I quality/counters/c2-r94-selftest-kills.py --repo . --rev "$REV" --panel .ufo/waves/round-94/controls/selftest-panel-r94-frozen.json --expect-panel-sha256 2d35e83bd9bcdd821accda43b39b5302cb508e15602019a34c89d7e418eed7e0 --expect-gate-sha256 2d6f1219fae19a85cc92f7d4103db396e1306fea74c2226bb068b335598da61b --expect-kills-sha256 d8a450bfb3bd67a6f5be399dece1ddc3d1b0922ae9c4b1f8bcff9a37afddd4ad,1a0c4fe8cec8ac4d0b33aaaf3c803e37ef168cc86f1f5cf914d35182051100b6 --control-kills .ufo/waves/round-94/build/mado-xdgmime-kills.c2.json,.ufo/waves/round-94/build/mado-mime-kills.c2.json --expect-control-kills-sha256 $(python3 -c "import hashlib;print(','.join(hashlib.sha256(open(f,'rb').read()).hexdigest() for f in ['.ufo/waves/round-94/build/mado-xdgmime-kills.c2.json','.ufo/waves/round-94/build/mado-mime-kills.c2.json']))") --workers 16 --scratch-root "$S/r94c2"
run python3 -I quality/counters/c2-r93-selftest-strength.py --repo . --rev "$REV" --panel .ufo/waves/round-93/controls/selftest-panel-r93.json --expect-panel-sha256 $(python3 -c "import hashlib;print(hashlib.sha256(open('.ufo/waves/round-93/controls/selftest-panel-r93.json','rb').read()).hexdigest())") --mutants .ufo/waves/round-93/controls/selftest-gate-mutants-r93-frozen.json --expect-mutants-sha256 $(python3 -c "import hashlib;print(hashlib.sha256(open('.ufo/waves/round-93/controls/selftest-gate-mutants-r93-frozen.json','rb').read()).hexdigest())") --expect-r92-counter-sha256 $(python3 -c "import hashlib;print(hashlib.sha256(open('quality/counters/c2-r92-gate-defects.py','rb').read()).hexdigest())") --expect-gate-sha256 $(python3 -c "import hashlib;print(hashlib.sha256(open('quality/check-selftest-strength.py','rb').read()).hexdigest())") --expect-kills-sha256 $(python3 -c "import hashlib;print(hashlib.sha256(open('quality/selftest-kills/check-seat-reports.json','rb').read()).hexdigest())") --workers 16 --scratch-root "$S/r93c2"
echo "\$ git diff --stat 4a2af6817024f6ed47084a5217c1825ae247f4fe \$REV -- tools/mado-mime.py tools/mado-xdgmime.py tools/mado-mako.py tools/mado-verify.sh quality/check-seat-reports.py quality/check-receipt-presence.py tools/mado-mimeglob.py tools/mado-portals.py"
git diff --stat 4a2af6817024f6ed47084a5217c1825ae247f4fe "$REV" -- tools/mado-mime.py tools/mado-xdgmime.py tools/mado-mako.py tools/mado-verify.sh quality/check-seat-reports.py quality/check-receipt-presence.py tools/mado-mimeglob.py tools/mado-portals.py
echo "rc=$? (only tools/mado-mimesniff.py is new; mimeglob/portals must be unchanged since 4a2af681)"
# L1 additions: the round-95 kill-sets on the real gate, the round-94 instruments, and the round-94 C2 counter.
echo "# L1 additions: round-95 kill-sets on the real gate, round-94 C1 counter, round-94 C2 counter, round-93 C2 counter"
run python3 -I quality/check-selftest-strength.py --tool tools/mado-mimeglob.py --kills quality/selftest-kills/mado-mimeglob.json --scratch-root "$S/gate-mg"
run python3 -I quality/check-selftest-strength.py --tool tools/mado-portals.py --kills quality/selftest-kills/mado-portals.json --scratch-root "$S/gate-pt"
