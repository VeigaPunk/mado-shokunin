#!/bin/bash
# R55W2CritAdmission receipts: re-run every admission command at the scored rev and copy the exact output.
# Reads only: git objects of the lane at REV (git archive / git show / git clone of the lane), counters and harnesses
# run with --work in scratch, the selftest and index gate run on an export, the census on an export root.
# The lane working tree is never written; attack copies are scratch clones (att2) with commits made in the clones.
set -u
L=/home/vgpnk/Projects/shokunin/mado-shokunin
F=/home/vgpnk/Projects/shokunin
R=57584ed67716340b3d466fa04333ac0bab3fb79e
BASE=3b55b6e91e40f455dd56b2985e4ffc087ada92d5
S=/fast/scratch/hyaku/mado-r55/R55W2CritAdmission
OUT=$L/.ufo/waves/round-55/w2/R55W2CritAdmission/receipts
C=$L/quality/counters
mkdir -p "$OUT" "$S/rc"
export TMPDIR=$S/rc
cd "$S" || exit 9

{
  echo "# counters and harnesses at rev $R (cwd=$S; --repo $L)"
  echo "\$ python3 -I quality/counters/c1-r55-kbd-entry.py --repo . --rev $R --work <scratch>/c1"
  python3 -I "$C/c1-r55-kbd-entry.py" --repo "$L" --rev "$R" --work "$S/rc/c1"; echo "rc=$?"
  echo "\$ python3 -I quality/check-r55-controls.py --claim c1 --repo . --rev $R --work <scratch>/hc1"
  python3 -I "$L/quality/check-r55-controls.py" --claim c1 --repo "$L" --rev "$R" --work "$S/rc/hc1"; echo "rc=$?"
  echo "\$ python3 -I quality/counters/c3-r55-p19.py --repo . --rev $R --work <scratch>/c3"
  python3 -I "$C/c3-r55-p19.py" --repo "$L" --rev "$R" --work "$S/rc/c3"; echo "rc=$?"
  echo "\$ python3 -I quality/check-r55-controls.py --claim c3 --repo . --rev $R --work <scratch>/hc3"
  python3 -I "$L/quality/check-r55-controls.py" --claim c3 --repo "$L" --rev "$R" --work "$S/rc/hc3"; echo "rc=$?"
  echo "\$ python3 -I quality/check-r55-controls.py --claim c2 --repo . --rev $R --work <scratch>/hc2"
  python3 -I "$L/quality/check-r55-controls.py" --claim c2 --repo "$L" --rev "$R" --work "$S/rc/hc2"; echo "rc=$?"
} > "$OUT/claims-at-rev.txt" 2>&1

{
  echo "# harm watch at rev $R (export of the rev under $S/tree; TMPDIR=$S/rc)"
  echo "\$ bash tools/mado-verify.sh --selftest"
  (cd "$S/tree" && bash tools/mado-verify.sh --selftest); echo "rc=$?"
  echo "\$ python3 -I quality/check-index.py --rev $R --repo ."
  python3 -I "$L/quality/check-index.py" --rev "$R" --repo "$L"; echo "rc=$?"
  echo "\$ scripts/sources-census.sh validate --root <scratch>/root mado   (root = export of rev as mado-shokunin/ + shokunin.conf)"
  (cd "$F" && bash scripts/sources-census.sh validate --root "$S/root" mado 2>&1 | grep -v '^mado.W04' ; echo "census_rc=${PIPESTATUS[0]}")
  echo "\$ scripts/sources-census.sh validate --root <scratch>/root mado   (exact exit code, unfiltered)"
  (cd "$F" && bash scripts/sources-census.sh validate --root "$S/root" mado > "$S/rc/census-full.out" 2>&1; echo "rc=$?"; echo "W04_lines=$(grep -c W04 "$S/rc/census-full.out") E_lines=$(grep -c -E '^mado\s+E' "$S/rc/census-full.out")")
} > "$OUT/harm-watch.txt" 2>&1

{
  echo "# admission diff: frozen v1 tables vs v2 tables (the only table change must be the listed K16 quote + rev_rule)"
  git -C "$L" show "$R:.ufo/waves/round-55/frozen-tables.json" > "$S/rc/ft1.json"
  git -C "$L" show "$R:.ufo/waves/round-55/frozen-tables-v2.json" > "$S/rc/ft2.json"
  echo "\$ diff <(json, sorted keys) ft1 ft2"
  diff <(python3 -I -c 'import json;print(json.dumps(json.load(open("'"$S/rc/ft1.json"'")),indent=1,sort_keys=True,ensure_ascii=False))') \
       <(python3 -I -c 'import json;print(json.dumps(json.load(open("'"$S/rc/ft2.json"'")),indent=1,sort_keys=True,ensure_ascii=False))'); echo "diff_rc=$?"
  sha256sum "$S/rc/ft1.json" "$S/rc/ft2.json"
  echo "# holdout commitment in v1 and v2"
  python3 -I -c 'import json;print(json.load(open("'"$S/rc/ft1.json"'"))["c2"]["holdout_commit_sha256"]); print(json.load(open("'"$S/rc/ft2.json"'"))["c2"]["holdout_commit_sha256"])'
  echo "# freeze files: blob ids at freeze commit 54dacbd8 vs rev"
  for f in .ufo/waves/round-55/claims-frozen.md .ufo/waves/round-55/registration.md .ufo/waves/round-55/frozen-tables.json .ufo/waves/round-55/fixtures/c2 .ufo/waves/round-55/ctl .ufo/waves/round-55/fetch .ufo/waves/round-55/freeze-verify.py; do
    echo "$f 54dacbd8=$(git -C "$L" rev-parse -q --verify "54dacbd8:$f") rev=$(git -C "$L" rev-parse -q --verify "$R:$f")"; done
  echo "# host version pin"
  git -C "$L" show "$R:corpus/SOURCES.md" | grep -E '^\| S316 ' | cut -c1-160
} > "$OUT/v1-v2-tables-and-freeze.txt" 2>&1

{
  echo "# K16 v1 vs v2 quote against the pinned line (Hyprland-legacy-ConfigManager.cpp:1119 @ efb50993)"
  sed -n '1119p' "$L/.ufo/waves/round-55/fetch/Hyprland-legacy-ConfigManager.cpp"
  echo "v1 quote: if ((!VAL || !VAL->m_bSetByUser) && !fallback.empty())"
  echo "v2 quote: !VAL->m_bSetByUser) && !fallback.empty())"
  echo "K16 proposition: $(git -C "$L" show "$R:corpus/knowledge/hyprland-keyboard-repeat-numlock-r55.md" | grep -E '^\| K16 ' | cut -d'|' -f3)"
  echo "# the substring '!VAL ||' (the absence test in the proposition) is not in the v2 quote:"
  git -C "$L" show "$R:.ufo/waves/round-55/frozen-tables-v2.json" | grep -c '!VAL ||' || true
} > "$OUT/k16-quote-vs-proposition.txt" 2>&1

{
  echo "# real-host read-only tool run (tools/mado-kbdopts.py from the rev export)"
  echo "\$ python3 -I tools/mado-kbdopts.py --config ~/.config/hypr/input.conf --getoption <scratch>/getoption.jsonl"
  python3 -I "$S/tree/tools/mado-kbdopts.py" --config "$HOME/.config/hypr/input.conf" --getoption "$S/run/getoption.jsonl"; echo "rc=$?"
  echo "\$ cmp ~/.config/hypr/input.conf fetch/host-input.conf"
  cmp "$HOME/.config/hypr/input.conf" "$L/.ufo/waves/round-55/fetch/host-input.conf" && echo CMP_EQUAL
} > "$OUT/host-tool-run.txt" 2>&1

{
  echo "# attack copies (scratch clones of the lane at $R, one committed mutation each; counters run unchanged)"
  for n in good k1 p23 c5; do
    D=$(ls -d "$S/att2/$n."*)
    echo "## $n $(git -C "$D" rev-parse --show-toplevel) HEAD=$(git -C "$D" rev-parse HEAD)"
    git -C "$D" diff --stat "$R" HEAD | tail -1
  done
  echo "## k1: C1 counter"
  D=$(ls -d "$S/att2/k1."*); python3 -I "$C/c1-r55-kbd-entry.py" --repo "$D" --rev "$(git -C "$D" rev-parse HEAD)" --work "$S/rc/k1c1"; echo "rc=$?"
  echo "## good: C1 counter"
  D=$(ls -d "$S/att2/good."*); python3 -I "$C/c1-r55-kbd-entry.py" --repo "$D" --rev "$(git -C "$D" rev-parse HEAD)" --work "$S/rc/goodc1"; echo "rc=$?"
  echo "## p23: C3 counter"
  D=$(ls -d "$S/att2/p23."*); python3 -I "$C/c3-r55-p19.py" --repo "$D" --rev "$(git -C "$D" rev-parse HEAD)" --work "$S/rc/p23c3"; echo "rc=$?"
  echo "## good: C3 counter"
  D=$(ls -d "$S/att2/good."*); python3 -I "$C/c3-r55-p19.py" --repo "$D" --rev "$(git -C "$D" rev-parse HEAD)" --work "$S/rc/goodc3"; echo "rc=$?"
  echo "## c5: C3 counter (v1-control shape: P23 proposition := P19 proposition verbatim)"
  D=$(ls -d "$S/att2/c5."*); python3 -I "$C/c3-r55-p19.py" --repo "$D" --rev "$(git -C "$D" rev-parse HEAD)" --work "$S/rc/c5c3"; echo "rc=$?"
  echo "## p23 mutated P23 row (branch == 0 now says PRESSED; pin line 1563 quoted in the same block says RELEASED)"
  D=$(ls -d "$S/att2/p23."*); git -C "$D" show HEAD:corpus/knowledge/hyprland-synthetic-dispatch-r52-errata-r53.md | grep -o 'When `m_passPressed == 0`[^.]*'
  echo "## Q06 quote in the same block"
  git -C "$L" show "$R:corpus/knowledge/hyprland-synthetic-dispatch-r52-errata-r53.md" | grep -E '^\| Q06 '
} > "$OUT/attacks.txt" 2>&1

{
  echo "# C1 K01 mutated proposition in the attack copy k1"
  D=$(ls -d "$S/att2/k1."*); git -C "$D" show HEAD:corpus/knowledge/hyprland-keyboard-repeat-numlock-r55.md | grep -E '^\| K01 '
} > "$OUT/k1-row.txt" 2>&1

echo "receipts written to $OUT"
ls -la "$OUT"
