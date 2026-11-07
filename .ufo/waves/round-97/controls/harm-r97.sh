#!/bin/bash
# harm-r97.sh -- round-97 harm watch (L1; replays the r96 leg set plus the r95/r96/r97 counter declarations).
#
# Replays every live counter named in the round-95 harm receipt
# (.ufo/waves/round-95/receipts/harm-final-r95.txt, replayed there at rev
# 6f6955f9cf6ff9bf8f5e769f6b8d8ff79ac55ce3) at the current lane revision, plus the
# round-96 counter leg whose argv is still "<placeholder>" for the L1 to fill.
#
# Usage:
#   bash .ufo/waves/round-96/controls/harm-r97.sh [--repo DIR] [--rev REV]
#        [--scratch-root DIR] [--legs n1,n2,...] [--smoke] [--list]
# Defaults: --repo /home/vgpnk/Projects/shokunin/mado-shokunin
#           --rev $(git -C "$REPO" rev-parse HEAD)  [read-only git query]
#           --scratch-root ${HYAKU_SCRATCH:-/fast/scratch/hyaku}/mado-r97/l1/harm
# Every leg writes only under its own --scratch-root; the lane repo and host config
# are read-only inputs. One line per leg: "LEG <name> rc=<rc>" plus the log path.
# Expected rc: 0 everywhere except r90c1_portal_routing, which EXPECTS rc=2
# (SETUP_ERROR: its nine anchors were removed by the round-90 port; see the r95
# receipt note). r96_counter prints rc=125 SKIPPED until its argv is filled in.
set -u

REPO=/home/vgpnk/Projects/shokunin/mado-shokunin
REV_ARG=
SCRATCH_ROOT="${HYAKU_SCRATCH:-/fast/scratch/hyaku}/mado-r97/l1/harm"
WANT_LEGS=
MODE=run   # run | smoke | list

while [ $# -gt 0 ]; do
  case "$1" in
    --repo) REPO="$2"; shift 2 ;;
    --rev) REV_ARG="$2"; shift 2 ;;
    --scratch-root) SCRATCH_ROOT="$2"; shift 2 ;;
    --legs) WANT_LEGS="$2"; shift 2 ;;
    --smoke) MODE=smoke; shift ;;
    --list) MODE=list; shift ;;
    *) echo "harm-r96: unknown arg '$1'" >&2; exit 2 ;;
  esac
done

REV=$REV_ARG
if [ -z "$REV" ]; then
  REV=$(git -C "$REPO" rev-parse HEAD) || { echo "harm-r96: cannot resolve HEAD" >&2; exit 2; }
fi
[ "$MODE" = list ] || mkdir -p "$SCRATCH_ROOT"

# Round-96 counter argv -- <placeholder> until the L1 freezes it (c1-r96-magictext.py
# per claims-declaration-r96.md, --rev/--scratch-root style as the r95 legs).
R96_COUNTER_ARGV="<placeholder>"

# --- leg table: each function mirrors one "$ " line of harm-final-r95.txt ---
# (receipt line numbers in comments; --rev is replayed at the current revision,
#  every --base-rev and --expect-*-sha256 anchor stays verbatim from the receipt).

leg_verify_selftest() {        # receipt :2
  bash tools/mado-verify.sh --selftest
}
leg_verify_file_plane() {      # receipt :5
  bash tools/mado-verify.sh --no-live
}
leg_index() {                  # receipt :53
  python3 -I quality/check-index.py --repo . --rev "$REV"
}
leg_ledger() {                 # receipt :56
  python3 -I quality/check-tool-ledger.py --repo . --rev "$REV"
}
leg_mako_selftest() {          # receipt :59
  mkdir -p "$SCRATCH_ROOT/mako"
  python3 -I tools/mado-mako.py --selftest --scratch-root "$SCRATCH_ROOT/mako"
}
leg_portals_selftest() {       # receipt :62
  python3 -I tools/mado-portals.py --selftest
}
leg_mime_selftest() {          # receipt :65
  python3 -I tools/mado-mime.py --selftest
}
leg_xdgmime_selftest() {       # receipt :68
  python3 -I tools/mado-xdgmime.py --selftest
}
leg_mimeglob_selftest() {      # receipt :71
  python3 -I tools/mado-mimeglob.py --selftest
}
leg_mimesniff_selftest() {     # receipt :74
  python3 -I tools/mado-mimesniff.py --selftest
}
leg_seat_reports_selftest() {  # receipt :77
  python3 -I quality/check-seat-reports.py --selftest
}
leg_receipt_presence_selftest() {  # receipt :80
  python3 -I quality/check-receipt-presence.py --selftest
}
leg_gate_selftest() {          # receipt :83
  python3 -I quality/check-selftest-strength.py --selftest
}
leg_gate_seat_reports() {      # receipt :86
  python3 -I quality/check-selftest-strength.py --tool quality/check-seat-reports.py --kills quality/selftest-kills/check-seat-reports.json --scratch-root "$SCRATCH_ROOT/gate-seat-reports"
}
leg_gate_mimeglob() {          # receipt :251
  python3 -I quality/check-selftest-strength.py --tool tools/mado-mimeglob.py --kills quality/selftest-kills/mado-mimeglob.json --scratch-root "$SCRATCH_ROOT/gate-mimeglob"
}
leg_gate_portals() {           # receipt :254
  python3 -I quality/check-selftest-strength.py --tool tools/mado-portals.py --kills quality/selftest-kills/mado-portals.json --scratch-root "$SCRATCH_ROOT/gate-portals"
}
leg_r90c2_receipt_presence() { # receipt :89 (counter c2-r90-receipt-presence)
  python3 -I quality/counters/c2-r90-receipt-presence.py --repo . --rev "$REV" --base-rev 5041acf99e27263872bf0441ad5f9d4316152605 --set .ufo/waves/round-90/controls/receipt-presence-set-r90.json --mutants .ufo/waves/round-90/controls/receipt-mutants-r90.json --expect-set-sha256 f7ab86c25edbb806a9f947af09fab5cf971a42602c252966c0075b9aeefa7939 --expect-mutants-sha256 68b39a805755f7685c00c847a48b0f8f679fdca2710773efb5f4469b7bebe82d --scratch-root "$SCRATCH_ROOT/r90c2"
}
leg_r92_gate_defects() {       # receipt :175 (counter c2-r92-gate-defects)
  python3 -I quality/counters/c2-r92-gate-defects.py --repo . --rev "$REV" --base-rev d992ef7494b054591ee9104df1da49264678df5d --battery .ufo/waves/round-92/controls/gate-defects-battery-r92.json --mutants .ufo/waves/round-92/controls/gate-defects-mutants-r92.json --expect-battery-sha256 a0cfaeb36c5423678696629569019dece0d2138dc5e980df0ba7a9ad7ef2fdd6 --expect-mutants-sha256 fe931e76f778e318771486458336d53dbf8933dd5444fa0beba07d53196f1e26 --r91-argv .ufo/waves/round-92/controls/r91-c2-argv-r92.json --expect-r91-argv-sha256 d21b1979b8b42203c8d9c8d033ec71af8027ff79911adc348cddb9685df4b604 --expect-r91-counter-sha256 c74f5baae915a4669ece5033a35ba16f5db0131a2db9a6e83a702de9e932d486 --fresh 60 --scratch-root "$SCRATCH_ROOT/r92c2"
}
leg_r90c1_portal_routing() {   # receipt :225 (counter c1-r90-portal-routing; EXPECT rc=2 SETUP_ERROR)
  python3 -I quality/counters/c1-r90-portal-routing.py --repo . --rev "$REV" --base-rev 5041acf99e27263872bf0441ad5f9d4316152605 --cases .ufo/waves/round-90/controls/portal-cases-r90.json --mutants .ufo/waves/round-90/controls/portal-mutants-r90.json --expect-cases-sha256 66d4ffff70bd092bd2c900658b3b9a7566f8dedc2aacd4b334102acebc192da2 --expect-mutants-sha256 e761a4e44ec6d8a692d8ac9b2feec7ef8609b4d30f5ed40c11f7c332129c2451 --expect-oracle-binary-sha256 e1429fbe1bf6c2203ba07f478b9e92e9221437b13a92eebafb0982748583a4f8 --scratch-root "$SCRATCH_ROOT/r90c1"
}
leg_r94c1_mimeglob() {         # receipt :228 (counter c1-r94-mimeglob)
  python3 -I quality/counters/c1-r94-mimeglob.py --repo . --rev "$REV" --base-rev a3de997289014e7dbf1d73ae206be1d6f8cdadd0 --cases .ufo/waves/round-94/controls/mimeglob-cases-r94-frozen.json --expect-cases-sha256 c7b693d240479ed63af24f426ae184bc4a13489a38f587620d9e1224dca5856c --mutants .ufo/waves/round-94/controls/mimeglob-mutants-r94-frozen.json --expect-mutants-sha256 0e74c57d233d2440f903466e959488705a58fdcda4f14d920caef0d2859133c2 --oracle-src .ufo/waves/round-94/controls/mimeglob-oracle-r94.c --expect-oracle-sha256 9c4337b36f93fa71bce13938f93d2e9758bb752815a67c57eb934a70bbfa6b11 --fresh-gen .ufo/waves/round-94/controls/mimeglob-fresh-r94.py --expect-fresh-gen-sha256 ab76b97e0c37d92ddb0b03a733745b1089be2a083379d9cabee050689ed57e2c --host-names .ufo/waves/round-94/controls/mimeglob-host-names-r94.txt --expect-host-names-sha256 4b6d6a6cc67a4ad59eb91c9e8af1cc605f2f278d2a2ecf57b4a81edad9344fa3 --expect-tool-sha256 65f80a6cb1551bb722ae7608df04fb17deba1b5cd05bef6f7fdd79bed76e2453 --fresh 120 --workers 24 --scratch-root "$SCRATCH_ROOT/r94c1"
}
leg_r94c2_selftest_kills() {   # receipt :243 (counter c2-r94-selftest-kills)
  python3 -I quality/counters/c2-r94-selftest-kills.py --repo . --rev "$REV" --panel .ufo/waves/round-94/controls/selftest-panel-r94-frozen.json --expect-panel-sha256 2d35e83bd9bcdd821accda43b39b5302cb508e15602019a34c89d7e418eed7e0 --expect-gate-sha256 2d6f1219fae19a85cc92f7d4103db396e1306fea74c2226bb068b335598da61b --expect-kills-sha256 d8a450bfb3bd67a6f5be399dece1ddc3d1b0922ae9c4b1f8bcff9a37afddd4ad,1a0c4fe8cec8ac4d0b33aaaf3c803e37ef168cc86f1f5cf914d35182051100b6 --control-kills .ufo/waves/round-94/build/mado-xdgmime-kills.c2.json,.ufo/waves/round-94/build/mado-mime-kills.c2.json --expect-control-kills-sha256 126b508aa1841ba99fa17ecaef46a5a79cdee99956ac2a605479b96122f09ea9,d930689e6ff82e51722195e0c8d209fe46fb4697fd10f01f33cec30e98e81601 --workers 16 --scratch-root "$SCRATCH_ROOT/r94c2"
}
leg_r93c2_selftest_strength() {  # receipt :246 (counter c2-r93-selftest-strength)
  python3 -I quality/counters/c2-r93-selftest-strength.py --repo . --rev "$REV" --panel .ufo/waves/round-93/controls/selftest-panel-r93.json --expect-panel-sha256 a6d2cbe2826868191f3ee980c27fcc3288bbc151ed3ceeb79ca1f11891bc4c10 --mutants .ufo/waves/round-93/controls/selftest-gate-mutants-r93-frozen.json --expect-mutants-sha256 be676929cefa46481e1ea836d29cd65152af23002e9d9dad96cf39295b88770e --expect-r92-counter-sha256 0aa4d1f18c3f309a8ef5a7575f1a4bde84681d9f7843dea03fdca723de30945c --expect-gate-sha256 2d6f1219fae19a85cc92f7d4103db396e1306fea74c2226bb068b335598da61b --expect-kills-sha256 00befb3efbe2f4a7c44b14776482e0cac0ab8e219db934af9c25b34f47c516f9 --workers 16 --scratch-root "$SCRATCH_ROOT/r93c2"
}

# --- declaration legs: each runs a published counting command at $REV (round 97) ---
RUNNER="$REPO/.ufo/waves/round-97/controls/run-decl-counter.py"
leg_r95c1_mimesniff() {
  python3 -I "$RUNNER" --decl "$REPO/.ufo/waves/round-95/claims-declaration-r95.md" --rev "$REV" --scratch-root "$SCRATCH_ROOT/r95c1" --repo "$REPO" --index 1
}
leg_r95c2_selftest_kills() {
  python3 -I "$RUNNER" --decl "$REPO/.ufo/waves/round-95/claims-declaration-r95.md" --rev "$REV" --scratch-root "$SCRATCH_ROOT/r95c2" --repo "$REPO" --index 2
}
leg_r96c1_magictext() {
  python3 -I "$RUNNER" --decl "$REPO/.ufo/waves/round-96/claims-declaration-r96.md" --rev "$REV" --scratch-root "$SCRATCH_ROOT/r96c1" --repo "$REPO" --index 1
}
leg_r96c2_selftest_kills() {
  python3 -I "$RUNNER" --decl "$REPO/.ufo/waves/round-96/claims-declaration-r96.md" --rev "$REV" --scratch-root "$SCRATCH_ROOT/r96c2" --repo "$REPO" --index 2
}
leg_r97c1_filetype() {
  python3 -I "$RUNNER" --decl "$REPO/.ufo/waves/round-97/claims-declaration-r97.md" --rev "$REV" --scratch-root "$SCRATCH_ROOT/r97c1" --repo "$REPO" --index 1
}
leg_r97c2_counter_selftest() {
  python3 -I "$RUNNER" --decl "$REPO/.ufo/waves/round-97/claims-declaration-r97.md" --rev "$REV" --scratch-root "$SCRATCH_ROOT/r97c2" --repo "$REPO" --index 2
}

ALL_LEGS="verify_selftest verify_file_plane index ledger mako_selftest portals_selftest mime_selftest xdgmime_selftest mimeglob_selftest mimesniff_selftest seat_reports_selftest receipt_presence_selftest gate_selftest gate_seat_reports gate_mimeglob gate_portals r90c2_receipt_presence r92_gate_defects r90c1_portal_routing r94c1_mimeglob r94c2_selftest_kills r93c2_selftest_strength r95c1_mimesniff r95c2_selftest_kills r96c1_magictext r96c2_selftest_kills r97c1_filetype r97c2_counter_selftest"
SMOKE_LEGS="verify_selftest index receipt_presence_selftest"

if [ "$MODE" = list ]; then
  for l in $ALL_LEGS; do echo "$l"; done
  exit 0
fi

SELECTED=$ALL_LEGS
if [ "$MODE" = smoke ]; then
  SELECTED=$SMOKE_LEGS
elif [ -n "$WANT_LEGS" ]; then
  SELECTED=$(echo "$WANT_LEGS" | tr ',' ' ')
fi

rc_all=0
for name in $SELECTED; do
  fn="leg_$name"
  if ! command -v "$fn" >/dev/null 2>&1; then
    echo "LEG $name rc=126 NO-SUCH-LEG"
    rc_all=1
    continue
  fi
  log="$SCRATCH_ROOT/$name.log"
  ( cd "$REPO" && "$fn" ) >"$log" 2>&1
  rc=$?
  echo "LEG $name rc=$rc log=$log"
  [ "$rc" -eq 0 ] || [ "$name" = r90c1_portal_routing -a "$rc" -eq 2 ] || rc_all=1
done
exit "$rc_all"
