#!/bin/bash
# ExecSessionTriage demo: both directions of the synthetic-material marker.
# Everything writes into a scratch clone; receipts land in the seat dir.
set -uo pipefail
LANE=/home/vgpnk/Projects/shokunin/mado-shokunin
SEAT=$LANE/.ufo/waves/round-46/w1/ExecSessionTriage
REV=4d22eeb66c2835af8aaa3fac6ad838fa616aa663
S=$(mktemp -d -p /fast/scratch/hyaku/mado-r46/ExecSessionTriage demo.XXXXXX) || exit 2
trap 'rm -rf -- "$S"' EXIT
export TMPDIR="$S"
C=$S/clone
G=$SEAT/check-session-material.py
git clone -q --shared --no-checkout "$LANE" "$C" || exit 3
[ "$(git -C "$C" rev-parse --show-toplevel)" = "$C" ] || exit 3
git -C "$C" checkout -q --detach "$REV" || exit 3

scan() { # scan <receipt-name> [args...]
  local name=$1; shift
  local out=$SEAT/receipts/$name
  python3 -I "$G" --repo "$C" --rev HEAD "$@" > "$out" 2>&1
  local code=$?
  printf 'exit=%d\n' "$code" >> "$out"
  echo "$name exit=$code findings=$(grep -c '^FINDING' "$out") waived=$(grep -c '^WAIVER file=' "$out") rejected=$(grep -c '^WAIVER_REJECTED' "$out")"
}

echo "== A. baseline at $REV with the new gate, waivers disabled"
scan 03-newgate-baseline.txt --no-waivers
grep -c '^FINDING' "$SEAT/receipts/03-newgate-baseline.txt"

echo "== B. mark the 49 round-45 findings (45 fixture dumps, 3 gate-copy rules, 1 mutant driver)"
python3 -I "$SEAT/demo/mark-synthetic.py" "$C" --tsv "$SEAT/triage.tsv" \
  --prefix .ufo/waves/round-45/ --message "markers: round-45 synthetic" || exit 4
scan 04-marked-49.txt
echo "-- control: the tracked gate (no waiver support) on the same marked clone"
python3 -I "$LANE/quality/check-session-material.py" --repo "$C" --rev HEAD > "$SEAT/receipts/04b-tracked-gate-on-marked.txt" 2>&1
printf 'exit=%d\n' "$?" >> "$SEAT/receipts/04b-tracked-gate-on-marked.txt"
grep -E '^SESSION_MATERIAL(:|_)' "$SEAT/receipts/04b-tracked-gate-on-marked.txt"

echo "== C. mark the 33 pre-existing synthetic findings too (values are not reserved)"
python3 -I "$SEAT/demo/mark-synthetic.py" "$C" --tsv "$SEAT/triage.tsv" \
  --message "markers: every synthetic finding" || exit 4
scan 05-marked-all-synthetic.txt

echo "== D. plant a real monitor dump that carries the marker and a registry line"
P=.ufo/waves/round-46/w1/ExecSessionTriage/fixtures/planted/mons.json
mkdir -p "$(dirname "$C/$P")"
printf '%s\n' '[{"name": "DP-1", "description": "DELL U2720Q 9P3XN53", "make": "Dell Inc.", "model": "DELL U2720Q", "serial": "CN0H7Y2K3F"}]' > "$C/$P"
python3 -I "$SEAT/demo/mark-synthetic.py" "$C" --tsv "$SEAT/triage.tsv" \
  --also "$P:R3_MONITOR_IDENT" \
  --message "planted real dump with a marker" || exit 4
scan 06-planted-real-dump.txt

echo "== E. append a real client dump to an already-waived fixture"
W=.ufo/waves/round-45/w1/RevengerOmarchy/fixtures/w/C00_shipped/mons.json
printf '%s\n' '[{"class": "example-real-app", "title": "inbox (3) - mail", "pid": 4242}]' >> "$C/$W"
git -C "$C" add -A && git -C "$C" -c user.name=seat -c user.email=seat@scratch.invalid commit -q -m "tamper: waive a real client dump"
scan 07-tampered-waived-fixture.txt

echo "== F. --no-waivers on the marked clone: every marker ignored"
scan 08-no-waivers.txt --no-waivers

echo "== G. summaries"
for f in "$SEAT"/receipts/0[3-8]-*.txt; do
  printf '%s | ' "$(basename "$f")"
  grep -E '^SESSION_MATERIAL(_WAIVED)?:' "$f" | tr '\n' ' '
  printf '\n'
done
