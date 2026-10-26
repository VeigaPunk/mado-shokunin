#!/usr/bin/env bash
# verify-r1.sh - falsification re-derivation of .ufo/waves/round-47/w1/ScrErrataR1/erratum.md (R1, round 47).
# Read-only on the lane and on the host config tree; writes only into $WORK (default: a mktemp dir
# under $TMPDIR, else /fast/scratch/hyaku/mado-r47/ExecErrataR1). Never writes /tmp by default.
# Host reads: hyprctl version, hyprctl -j getoption ..., hyprctl devices -j (all read verbs; no dispatch,
# keyword, reload, batch, output, plugin, kill). No GUI program, no package transaction.
#
# usage: bash verify-r1.sh [WORK_DIR]
set -u
LANE=${LANE:-/home/vgpnk/Projects/shokunin/mado-shokunin}
rm_me=0
S=${1:-${WORK:-}}
if [ -z "$S" ]; then
  S=$(mktemp -d -p "${TMPDIR:-/fast/scratch/hyaku/mado-r47/ExecErrataR1}" r1.XXXXXX) || exit 1
  rm_me=1
fi
mkdir -p "$S" || exit 1
trap '[ "$rm_me" = 1 ] && rm -rf -- "$S"' EXIT

pass=0 fail=0
ok() { printf 'PASS %s\n' "$*"; pass=$((pass+1)); }
no() { printf 'FAIL %s\n' "$*"; fail=$((fail+1)); }
eq() { if [ "$2" = "$3" ]; then ok "$1 = $2"; else no "$1: got [$2] want [$3]"; fi; }
# computed locator: first line number where the fixed string occurs
loc() { grep -nF -- "$2" "$1" | head -1 | cut -d: -f1; }
words() { printf '%s' "$1" | wc -w | tr -d ' '; }

ENTRY=$LANE/corpus/knowledge/hyprland-input-devices-r46.md
R46=$LANE/.ufo/waves/round-46/receipts/live-devices-host-r46.txt
L1=$LANE/.ufo/waves/round-46/receipts/live-devices-host-l1.txt
DRAFT=$LANE/.ufo/waves/round-46/l1-draft/mado-devices.py
TOOL=$LANE/tools/mado-devices.py
ERR=$LANE/.ufo/waves/round-47/w1/ScrErrataR1/erratum.md
LESSON=$LANE/corpus/lessons/round-46-verifier-spotcheck.md
HYPR=$HOME/.config/hypr/hyprland.conf
OMARCHY=$HOME/.local/share/omarchy/default/hypr/input.conf
USERCFG=$HOME/.config/hypr/input.conf

Q1='one `input` block in `~/.config/hypr/input.conf`, no `device` block'
Q2="# chain: ~/.config/hypr/hyprland.conf sources the omarchy default input.conf before the user's input.conf"
Q3='the observation itself'
Q4="both receipts print the same summary line, so the sentence's content holds"

echo "== A. producing tools of the two receipts, worktree vs committed bytes =="
# erratum: landed tool sha256 3a803689..., l1-draft sha256 b229efd0...; receipts 0c749e1d..., d635baec...
eq "landed tool worktree"        "$(sha256sum "$TOOL" | cut -d' ' -f1)" 3a80368997120503d5715596a17e762bbcb67a41db23d9241425bf19349d594f
eq "l1 draft worktree"           "$(sha256sum "$DRAFT" | cut -d' ' -f1)" b229efd08d2d329dd60ced114598943d0419dac2f3cf05b1f6c1eb506c49a33b
eq "r46 receipt worktree"        "$(sha256sum "$R46" | cut -d' ' -f1)" 0c749e1d255538a6767992f116d44c48022b7dd8140df50f773fc355dabd956f
eq "l1 receipt worktree"         "$(sha256sum "$L1" | cut -d' ' -f1)" d635baec7e64d0405b48edd28edfb57dc1f35e38dfa3a375ea40b70361708265
# the check the w1 draft's verify.sh lacks: the on-disk bytes are the committed bytes
for rev in 1001bda0 60edb66e d7527d60 9bddd6ac c24adef2; do
  eq "git show $rev:tools/mado-devices.py" "$(git -C "$LANE" show "$rev:tools/mado-devices.py" | sha256sum | cut -d' ' -f1)" 3a80368997120503d5715596a17e762bbcb67a41db23d9241425bf19349d594f
done
eq "git show 1001bda0:l1-draft/mado-devices.py" "$(git -C "$LANE" show 1001bda0:.ufo/waves/round-46/l1-draft/mado-devices.py | sha256sum | cut -d' ' -f1)" b229efd08d2d329dd60ced114598943d0419dac2f3cf05b1f6c1eb506c49a33b
eq "git show 1001bda0:r46 receipt"   "$(git -C "$LANE" show 1001bda0:.ufo/waves/round-46/receipts/live-devices-host-r46.txt | sha256sum | cut -d' ' -f1)" 0c749e1d255538a6767992f116d44c48022b7dd8140df50f773fc355dabd956f
eq "git show 1001bda0:l1 receipt"    "$(git -C "$LANE" show 1001bda0:.ufo/waves/round-46/receipts/live-devices-host-l1.txt | sha256sum | cut -d' ' -f1)" d635baec7e64d0405b48edd28edfb57dc1f35e38dfa3a375ea40b70361708265
eq "receipt head names landed tool"  "$(sed -n '1p' "$R46" | grep -c 'tools/mado-devices.py (sha256 3a80368997120503d5715596a17e762bbcb67a41db23d9241425bf19349d594f)')" 1
eq "l1 head names the draft"         "$(sed -n '1p' "$L1" | grep -c 'l1-draft/mado-devices.py sha256 b229efd08d2d329dd60ced114598943d0419dac2f3cf05b1f6c1eb506c49a33b')" 1

echo "== B. config count recorded by each receipt =="
eq "r46 --config occurrences on its command line" "$(sed -n '6p' "$R46" | grep -o -- '--config' | wc -l | tr -d ' ')" 2
eq "l1  --config occurrences on its command line" "$(sed -n '4p' "$L1" | grep -o -- '--config' | wc -l | tr -d ' ')" 1
eq "r46 config header lines"    "$(sed -n '3,4p' "$R46" | grep -c '^# config ')" 2
eq "l1  config header lines"    "$(sed -n '1,4p' "$L1" | grep -c '^# config')" 1
eq "omarchy config hash"        "$(sha256sum "$OMARCHY" | cut -d' ' -f1)" bee5aa68cbec0c428fae7a5faf7da49a30e6f78ed96e78a063f08b66942448b8
eq "user config hash"           "$(sha256sum "$USERCFG" | cut -d' ' -f1)" 3769c92ab7660f1795cb6d0af1bcc5a5614a299b29ae8358d1b85936bdd47bf4

echo "== C. the effective chain: transitive source closure (depth 4) =="
: > "$S/seen"; printf '%s\n' "$HYPR" > "$S/frontier"
for d in 1 2 3 4; do
  : > "$S/next"
  while IFS= read -r f; do
    [ -f "$f" ] || continue
    grep -E '^[[:space:]]*source[[:space:]]*=' "$f" | sed 's/^[[:space:]]*source[[:space:]]*=[[:space:]]*//' | while IFS= read -r p; do
      for g in $HOME/${p#\~/}; do [ -f "$g" ] && printf '%s\n' "$g"; done
    done >> "$S/next"
  done < "$S/frontier"
  grep -vxF -f "$S/seen" "$S/next" > "$S/next2" 2>/dev/null || true
  mv "$S/next2" "$S/next"
  [ -s "$S/next" ] || break
  cat "$S/next" >> "$S/seen"; cp "$S/next" "$S/frontier"
done
printf '%s\n' "$HYPR" >> "$S/seen"; sort -u "$S/seen" -o "$S/seen"
printf 'closure files: %s (depth 4)\n' "$(wc -l < "$S/seen")"
: > "$S/inblocks"; : > "$S/devblocks"; : > "$S/kblayout"
while IFS= read -r f; do
  n=$(grep -cE '^[[:space:]]*input[[:space:]]*\{' "$f"); [ "$n" -gt 0 ] && printf '%s blocks=%s\n' "${f#$HOME/}" "$n" >> "$S/inblocks"
  m=$(grep -cE '^[[:space:]]*device[[:space:]]*\{' "$f"); [ "$m" -gt 0 ] && printf '%s device_blocks=%s\n' "${f#$HOME/}" "$m" >> "$S/devblocks"
  grep -nE '^[[:space:]]*kb_layout' "$f" | sed "s|^|${f#$HOME/}:|" >> "$S/kblayout"
done < "$S/seen"
cat "$S/inblocks"
eq "files with an input block in the closure" "$(wc -l < "$S/inblocks" | tr -d ' ')" 2
eq "files with a device block in the closure" "$(wc -l < "$S/devblocks" | tr -d ' ')" 0
eq "kb_layout sites in the closure"           "$(wc -l < "$S/kblayout" | tr -d ' ')" 2
cat "$S/kblayout"
eq "hyprland.conf sources omarchy input.conf at" "$(loc "$HYPR" 'source = ~/.local/share/omarchy/default/hypr/input.conf')" 11
eq "hyprland.conf sources user input.conf at"    "$(loc "$HYPR" 'source = ~/.config/hypr/input.conf')" 17
eq "omarchy input block line" "$(loc "$OMARCHY" 'input {')" 2
eq "omarchy kb_layout line"   "$(loc "$OMARCHY" 'kb_layout = us')" 3
eq "user input block line"    "$(loc "$USERCFG" 'input {')" 3
eq "user kb_layout line"      "$(loc "$USERCFG" 'kb_layout = br')" 10

echo "== D. compositor, read-only: does the omarchy file reach it? which value wins? =="
hyprctl version 2>&1 | sed -n '1p'
LIVE_LAYOUT=$(hyprctl -j getoption input:kb_layout 2>&1 | head -c 200)
LIVE_OPTS=$(hyprctl -j getoption input:kb_options 2>&1 | head -c 200)
LIVE_DPMS=$(hyprctl -j getoption misc:key_press_enables_dpms 2>&1 | head -c 200)
printf 'getoption input:kb_layout = %s\n' "$LIVE_LAYOUT"
printf 'getoption input:kb_options = %s\n' "$LIVE_OPTS"
printf 'getoption misc:key_press_enables_dpms = %s\n' "$LIVE_DPMS"
case "$LIVE_LAYOUT" in *'"str": "br"'*) ok "compositor global kb_layout is br (the later file wins)";; *) no "compositor kb_layout not br: [$LIVE_LAYOUT]";; esac
case "$LIVE_DPMS" in *'"int": 1'*) ok "compositor carries a key only the omarchy input.conf sets (file is parsed)";; *) no "dpms key not 1: [$LIVE_DPMS]";; esac

echo "== E. the join, re-run today (read-only dump to \$WORK) =="
hyprctl devices -j > "$S/devices.json" 2>/dev/null
cwd=$PWD; cd "$LANE" || exit 1
python3 -I "$TOOL" --devices "$S/devices.json" --config "$USERCFG" > "$S/run-useronly.txt" 2>&1; ru=$?
python3 -I "$TOOL" --devices "$S/devices.json" --config "$OMARCHY" --config "$USERCFG" > "$S/run-two.txt" 2>&1; rt=$?
python3 -I "$TOOL" --devices "$S/devices.json" --config "$USERCFG" --config "$OMARCHY" > "$S/run-rev.txt" 2>&1; rr=$?
python3 -I "$TOOL" --devices "$S/devices.json" --config "$OMARCHY" > "$S/run-om.txt" 2>&1; ro=$?
python3 -I "$DRAFT" --devices "$S/devices.json" --config "$USERCFG" > "$S/run-draft.txt" 2>&1; rd=$?
cd "$cwd" || exit 1
printf 'rc useronly=%s two=%s reversed=%s omarchyonly=%s draft=%s\n' "$ru" "$rt" "$rr" "$ro" "$rd"
for f in useronly two rev om draft; do
  printf '%-8s %s | %s\n' "$f" "$(grep -m1 '^MADO_DEV_KEYBOARD' "$S/run-$f.txt" | grep -o 'layout="[^"]*"')" "$(grep '^MADO_DEVICES:' "$S/run-$f.txt")"
done
# the erratum's merge-order sentence: later file overwrites earlier
eq "reversed order resolves to the omarchy value" "$(grep -m1 '^MADO_DEV_KEYBOARD' "$S/run-rev.txt" | grep -o 'layout="[^"]*"')" 'layout="us"'
eq "omarchy only resolves to us"                  "$(grep -m1 '^MADO_DEV_KEYBOARD' "$S/run-om.txt" | grep -o 'layout="[^"]*"')" 'layout="us"'
eq "landed tool == draft on the same argv"        "$(diff <(grep '^MADO_' "$S/run-draft.txt") <(grep '^MADO_' "$S/run-useronly.txt") | wc -l | tr -d ' ')" 0

echo "== F. today's run against both receipts (\"the observation itself\") =="
grep '^MADO_' "$R46" | grep -v '^MADO_DEVICES_SELFTEST' > "$S/r46.body"
grep '^MADO_' "$L1" > "$S/l1.body"
eq "r46 receipt device lines" "$(grep -c '^MADO_DEV_' "$R46")" 14
eq "l1  receipt device lines" "$(grep -c '^MADO_DEV_' "$L1")" 14
eq "r46 keyboards"  "$(grep -c '^MADO_DEV_KEYBOARD' "$R46")" 10
eq "r46 agree=9"    "$(grep -c 'layout="br".*verdict=AGREE' "$R46")" 9
eq "r46 virtual=1"  "$(grep -c 'verdict=VIRTUAL' "$R46")" 1
eq "r46 mice=4"     "$(grep -c 'scroll_factor=-1.00 reported=-1.00 verdict=AGREE' "$R46")" 4
eq "l1 selftest line absent" "$(grep -c '^MADO_DEVICES_SELFTEST' "$L1")" 0
eq "r46 selftest 59/59"      "$(grep -c '^MADO_DEVICES_SELFTEST: 59/59 passed' "$R46")" 1
printf -- '--- today useronly vs l1 receipt body ---\n'; diff "$S/l1.body" "$S/run-useronly.txt" || true
printf -- '--- today two-config vs r46 receipt body ---\n'; diff "$S/r46.body" "$S/run-two.txt" || true
eq "the two runs still agree with each other today" "$(diff <(grep '^MADO_' "$S/run-useronly.txt") <(grep '^MADO_' "$S/run-two.txt") | wc -l | tr -d ' ')" 0
VIRT=$(grep -c 'hl-virtual-keyboard' "$S/devices.json")
eq "dated observation: compositor virtual keyboards on 2026-10-26" "$VIRT" 0
KB=$(python3 -I -c 'import json,sys; d=json.load(open(sys.argv[1])); print(len(d["keyboards"]))' "$S/devices.json")
eq "dated observation: compositor keyboards on 2026-10-26" "$KB" 9
printf 'DIVERGENCE: today keyboards=%s virtual=%s; both receipts record keyboards=10 virtual=1\n' "$KB" "$VIRT"

echo "== G. draft->landed delta (30 removed / 105 added / 9 hunks) =="
diff -u "$DRAFT" "$TOOL" > "$S/tool.diff" || true
read -r R A < <(awk '/^--- /{next} /^\+\+\+ /{next} /^-/{d++} /^\+/{a++} END{print d+0, a+0}' "$S/tool.diff")
eq "removed lines" "$R" 30
eq "added lines"   "$A" 105
eq "hunks"         "$(grep -c '^@@' "$S/tool.diff")" 9
eq "merge loop line"        "$(loc "$TOOL" 'for t in config_texts:')" 418
eq "parse_config call line" "$(loc "$TOOL" 'parse_config(t, st)')" 419
eq "global assignment line" "$(loc "$TOOL" 'st.globals[key[len("input:"):]] = rhs')" 334

echo "== H. quotes and locators used by this seat's report =="
eq "Q1 locator in entry"  "$(loc "$ENTRY" "$Q1")" 57
[ "$(words "$Q1")" -le 25 ] && ok "Q1 words=$(words "$Q1") <= 25" || no "Q1 too long"
eq "Q2 locator in r46 receipt" "$(loc "$R46" "$Q2")" 5
[ "$(words "$Q2")" -le 25 ] && ok "Q2 words=$(words "$Q2") <= 25" || no "Q2 too long"
eq "Q3 locator in erratum"  "$(loc "$ERR" "$Q3")" 18
[ "$(words "$Q3")" -le 25 ] && ok "Q3 words=$(words "$Q3") <= 25" || no "Q3 too long"
eq "entry cites l1 receipt on :57" "$(sed -n '57p' "$ENTRY" | grep -c 'receipts/live-devices-host-l1.txt')" 1
eq "entry cites l1 receipt nowhere else" "$(grep -c 'live-devices-host-l1' "$ENTRY")" 1
eq "Q4 locator in the round-46 lesson" "$(loc "$LESSON" "$Q4")" 52
[ "$(words "$Q4")" -le 25 ] && ok "Q4 words=$(words "$Q4") <= 25" || no "Q4 too long"
eq "entry tracked and unmodified" "$(git -C "$LANE" status --porcelain -- corpus/knowledge/hyprland-input-devices-r46.md | wc -l | tr -d ' ')" 0
eq "erratum ends its diff parenthetical" "$(grep -c '30 removed, 105 added, 9 hunks' "$ERR")" 1

echo "== I. the seat deliverable carries the quoted text and the hashes it asserts =="
SEAT=$LANE/.ufo/waves/round-47/w2/ExecErrataR1
REPORT=$LANE/.ufo/waves/round-47/w2/ExecErrataR1.md
for f in "$SEAT/verdicts.md" "$REPORT"; do
  b=$(basename "$f")
  [ -f "$f" ] || { no "missing $b"; continue; }
  for pair in "Q1|$Q1" "Q2|$Q2" "Q3|$Q3"; do
    tag=${pair%%|*}; txt=${pair#*|}
    grep -qF -- "$txt" "$f" && ok "$b carries $tag" || no "$b missing $tag"
  done
done
for h in 3a80368997120503d5715596a17e762bbcb67a41db23d9241425bf19349d594f \
         b229efd08d2d329dd60ced114598943d0419dac2f3cf05b1f6c1eb506c49a33b \
         0c749e1d255538a6767992f116d44c48022b7dd8140df50f773fc355dabd956f \
         d635baec7e64d0405b48edd28edfb57dc1f35e38dfa3a375ea40b70361708265 \
         bee5aa68cbec0c428fae7a5faf7da49a30e6f78ed96e78a063f08b66942448b8 \
         3769c92ab7660f1795cb6d0af1bcc5a5614a299b29ae8358d1b85936bdd47bf4; do
  grep -qF -- "$h" "$SEAT/verdicts.md" && ok "verdicts.md has ${h:0:8}" || no "verdicts.md missing ${h:0:8}"
done
eq "Q4 locator re-checked for the deliverable" "$(loc "$LESSON" "$Q4")" 52
grep -qF -- "$Q4" "$SEAT/verdicts.md" && ok "verdicts.md carries Q4" || no "verdicts.md missing Q4"
printf 'VERIFY-R1: %d/%d passed\n' "$pass" "$((pass+fail))"
[ "$fail" -eq 0 ]
