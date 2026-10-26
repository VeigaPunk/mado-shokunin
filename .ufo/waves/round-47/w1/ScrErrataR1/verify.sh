#!/usr/bin/env bash
# verify.sh - re-checks every locator, hash and quote used by
# .ufo/waves/round-47/w1/ScrErrataR1/erratum.md (R1, round 47).
# Read-only on the lane and on ~/.config; writes only a temp dir under TMPDIR.
set -u
LANE=/home/vgpnk/Projects/shokunin/mado-shokunin
S=$(mktemp -d -p "${TMPDIR:-/fast/scratch/hyaku/mado-r47/ScrErrataR1}" verify.XXXXXX) || exit 1
trap 'rm -rf -- "$S"' EXIT
pass=0 fail=0
ok() { printf 'PASS %s\n' "$*"; pass=$((pass+1)); }
no() { printf 'FAIL %s\n' "$*"; fail=$((fail+1)); }
eq() { if [ "$2" = "$3" ]; then ok "$1 = $2"; else no "$1: got [$2] want [$3]"; fi; }
# computed locator: first line number where the exact string occurs
loc() { grep -nF -- "$2" "$1" | head -1 | cut -d: -f1; }
words() { printf '%s' "$1" | wc -w | tr -d ' '; }

ENTRY=$LANE/corpus/knowledge/hyprland-input-devices-r46.md
L1=$LANE/.ufo/waves/round-46/receipts/live-devices-host-l1.txt
R46=$LANE/.ufo/waves/round-46/receipts/live-devices-host-r46.txt
DRAFT=$LANE/.ufo/waves/round-46/l1-draft/mado-devices.py
TOOL=$LANE/tools/mado-devices.py
HYPR=$HOME/.config/hypr/hyprland.conf
OMARCHY=$HOME/.local/share/omarchy/default/hypr/input.conf
USERCFG=$HOME/.config/hypr/input.conf
ERR=$LANE/.ufo/waves/round-47/w1/ScrErrataR1/erratum.md

Q1='one `input` block in `~/.config/hypr/input.conf`, no `device` block'
Q2="# chain: ~/.config/hypr/hyprland.conf sources the omarchy default input.conf before the user's input.conf"

echo "== entry :57 quote =="
eq "Q1 locator in entry" "$(loc "$ENTRY" "$Q1")" 57
[ "$(words "$Q1")" -le 25 ] && ok "Q1 words=$(words "$Q1") <= 25" || no "Q1 too long"
eq "entry :57 cites L1 receipt" "$(grep -cF 'live-devices-host-l1.txt' <(sed -n '57p' "$ENTRY"))" 1

echo "== r46 receipt chain quote =="
eq "Q2 locator in r46 receipt" "$(loc "$R46" "$Q2")" 5
[ "$(words "$Q2")" -le 25 ] && ok "Q2 words=$(words "$Q2") <= 25" || no "Q2 too long"

echo "== hashes =="
eq "tool hash" "$(sha256sum "$TOOL" | cut -d' ' -f1)" 3a80368997120503d5715596a17e762bbcb67a41db23d9241425bf19349d594f
eq "r46 receipt hash" "$(sha256sum "$R46" | cut -d' ' -f1)" 0c749e1d255538a6767992f116d44c48022b7dd8140df50f773fc355dabd956f
eq "l1 receipt hash" "$(sha256sum "$L1" | cut -d' ' -f1)" d635baec7e64d0405b48edd28edfb57dc1f35e38dfa3a375ea40b70361708265
eq "draft hash" "$(sha256sum "$DRAFT" | cut -d' ' -f1)" b229efd08d2d329dd60ced114598943d0419dac2f3cf05b1f6c1eb506c49a33b
eq "omarchy config hash" "$(sha256sum "$OMARCHY" | cut -d' ' -f1)" bee5aa68cbec0c428fae7a5faf7da49a30e6f78ed96e78a063f08b66942448b8
eq "user config hash" "$(sha256sum "$USERCFG" | cut -d' ' -f1)" 3769c92ab7660f1795cb6d0af1bcc5a5614a299b29ae8358d1b85936bdd47bf4

echo "== config chain =="
eq "hyprland.conf sources omarchy input.conf at" "$(loc "$HYPR" 'source = ~/.local/share/omarchy/default/hypr/input.conf')" 11
eq "hyprland.conf sources user input.conf at" "$(loc "$HYPR" 'source = ~/.config/hypr/input.conf')" 17
eq "omarchy input block line" "$(loc "$OMARCHY" 'input {')" 2
eq "omarchy kb_layout line" "$(loc "$OMARCHY" 'kb_layout = us')" 3
eq "user input block line" "$(loc "$USERCFG" 'input {')" 3
eq "user kb_layout line" "$(loc "$USERCFG" 'kb_layout = br')" 10
eq "omarchy input blocks" "$(grep -cE '^[[:space:]]*input[[:space:]]*\{' "$OMARCHY")" 1
eq "user input blocks" "$(grep -cE '^[[:space:]]*input[[:space:]]*\{' "$USERCFG")" 1
eq "omarchy device blocks" "$(grep -cE '^[[:space:]]*device[[:space:]]*\{' "$OMARCHY")" 0
eq "user device blocks" "$(grep -cE '^[[:space:]]*device[[:space:]]*\{' "$USERCFG")" 0

echo "== join merge order =="
eq "merge loop line" "$(loc "$TOOL" 'for t in config_texts:')" 418
eq "parse_config call line" "$(loc "$TOOL" 'parse_config(t, st)')" 419
eq "global assignment line" "$(loc "$TOOL" 'st.globals[key[len("input:"):]] = rhs')" 334
grep -qF 'tools/mado-devices.py:334' "$ERR" && ok "erratum cites assignment line" || no "erratum missing :334"

echo "== receipt equality =="
grep '^MADO_' "$L1" > "$S/l1.body"
grep '^MADO_' "$R46" | grep -v '^MADO_DEVICES_SELFTEST' > "$S/r46.body"
if diff -q "$S/l1.body" "$S/r46.body" >/dev/null; then ok "device+verdict bodies identical"; else no "bodies differ"; fi
eq "keyboard lines in r46 receipt" "$(grep -c '^MADO_DEV_KEYBOARD' "$R46")" 10
eq "mouse lines in r46 receipt" "$(grep -c '^MADO_DEV_MOUSE' "$R46")" 4
eq "AGREE keyboards in r46 receipt" "$(grep -c 'layout="br".*verdict=AGREE' "$R46")" 9
eq "VIRTUAL keyboards in r46 receipt" "$(grep -c 'verdict=VIRTUAL' "$R46")" 1
eq "mice at -1.00 AGREE in r46 receipt" "$(grep -c 'scroll_factor=-1.00 reported=-1.00 verdict=AGREE' "$R46")" 4
eq "verdict lines equal" "$(grep '^MADO_DEVICES:' "$L1")" "$(grep '^MADO_DEVICES:' "$R46")"
eq "selftest line only in r46" "$(grep -c '^MADO_DEVICES_SELFTEST: 59/59 passed' "$R46")" 1
eq "no selftest line in l1" "$(grep -c '^MADO_DEVICES_SELFTEST' "$L1")" 0

echo "== draft vs landed delta =="
diff -u "$DRAFT" "$TOOL" > "$S/tool.diff" || true
read -r R A < <(awk '/^--- /{next} /^\+\+\+ /{next} /^-/{d++} /^\+/{a++} END{print d+0, a+0}' "$S/tool.diff")
eq "removed lines" "$R" 30
eq "added lines" "$A" 105
eq "changed total" "$((R+A))" 135
eq "hunks" "$(grep -c '^@@' "$S/tool.diff")" 9

echo "== erratum carries the verified text =="
eq "erratum heading" "$(sed -n '1p' "$ERR")" '## Erratum (2026-10-26, round 47)'
grep -qF -- "$Q1" "$ERR" && ok "erratum quotes Q1" || no "erratum missing Q1"
grep -qF -- "$Q2" "$ERR" && ok "erratum quotes Q2" || no "erratum missing Q2"
for h in 3a80368997120503d5715596a17e762bbcb67a41db23d9241425bf19349d594f \
         0c749e1d255538a6767992f116d44c48022b7dd8140df50f773fc355dabd956f \
         b229efd08d2d329dd60ced114598943d0419dac2f3cf05b1f6c1eb506c49a33b \
         bee5aa68cbec0c428fae7a5faf7da49a30e6f78ed96e78a063f08b66942448b8 \
         3769c92ab7660f1795cb6d0af1bcc5a5614a299b29ae8358d1b85936bdd47bf4; do
  grep -qF -- "$h" "$ERR" && ok "erratum has ${h:0:8}" || no "erratum missing ${h:0:8}"
done
eq "entry line count unchanged" "$(wc -l < "$ENTRY" | tr -d ' ')" 73
eq "entry untouched in git" "$(git -C "$LANE" status --porcelain -- corpus/knowledge/hyprland-input-devices-r46.md | wc -l | tr -d ' ')" 0

printf 'VERIFY: %d/%d passed\n' "$pass" "$((pass+fail))"
[ "$fail" -eq 0 ]
