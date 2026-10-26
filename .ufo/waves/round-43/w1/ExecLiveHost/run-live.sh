#!/bin/bash
# ExecLiveHost: live host receipt for C1 (round 43, w1). Read-only.
# Every command is echoed, its stdout/stderr passed through verbatim, then `exit=N`.
set -u
S=$(cd "$(dirname "$0")" && pwd)
cd "$S" || exit 9
TOOL="$S/mado-geometry.py"
RULES="$HOME/.config/hypr/gkeep.conf"

run() { # run <label> <cmd...>
  local label="$1"; shift
  echo "\$ $*"
  "$@"
  echo "exit=$?"
  echo "--- ($label)"
}

echo "# ExecLiveHost live census - round 43 w1 - read-only host receipt"
echo "# generated $(date -Is) on $(hostname) kernel $(uname -r)"
echo "# cwd $S"
echo
echo "## 0. identity"
echo "\$ python3 -V"
python3 -V 2>&1
echo "exit=$?"
echo "\$ hyprctl version"
hyprctl version
echo "exit=$?"
HYPR_VERSION_LINE=$(hyprctl version | head -1)
echo "HYPRCTL_VERSION_LINE: $HYPR_VERSION_LINE"
echo "\$ sha256sum mado-geometry.py (copy of .ufo/waves/round-42/c1/ctl-ref-tool.py.txt)"
sha256sum mado-geometry.py
echo "exit=$?"
echo "\$ sha256sum .ufo/waves/round-42/c1/ctl-ref-tool.py.txt (reference, for equality)"
sha256sum ../../c1/ctl-ref-tool.py.txt 2>/dev/null || sha256sum "$S/../../../round-42/c1/ctl-ref-tool.py.txt"
echo "exit=$?"
echo "\$ sha256sum ~/.config/hypr/gkeep.conf"
sha256sum "$RULES"
echo "exit=$?"
echo

echo "## 1. selftest (the reference's own suite)"
run selftest python3 -I mado-geometry.py --selftest
echo

echo "## 2. the command from the claim, three times (no gkeep window open)"
for i in 1 2 3; do
  echo "\$ hyprctl clients -j | python3 -I mado-geometry.py --clients - --rules $RULES   # run $i"
  hyprctl clients -j | python3 -I mado-geometry.py --clients - --rules "$RULES"
  echo "exit=${PIPESTATUS[1]} (hyprctl exit=${PIPESTATUS[0]})"
  echo "--- (run $i)"
done
echo

echo "## 3. hand-made clients files (fixtures in this directory)"
for f in fx-agree.json fx-differ.json fx-tiled.json fx-three.json; do
  echo "\$ cat $f"
  cat "$f"
  echo "--- (fixture $f)"
  run "$f" python3 -I mado-geometry.py --clients "$f" --rules "$RULES"
done
echo

echo "## 4. the real host dump, saved then piped through --clients -"
echo "\$ hyprctl clients -j > host-clients-live.json"
hyprctl clients -j > host-clients-live.json
echo "exit=$?"
echo "\$ sha256sum host-clients-live.json"
sha256sum host-clients-live.json
echo "\$ python3 -c 'reduced view: class/floating/size/mapped/address'"
python3 -I -c 'import json,sys; d=json.load(open("host-clients-live.json")); print(len(d), "clients"); [print(" ", c.get("address"), c.get("class"), c.get("size"), "floating="+str(c.get("floating")), "mapped="+str(c.get("mapped"))) for c in d]'
echo "\$ cat host-clients-live.json | python3 -I mado-geometry.py --clients - --rules $RULES"
cat host-clients-live.json | python3 -I mado-geometry.py --clients - --rules "$RULES"
echo "exit=${PIPESTATUS[1]}"
echo "--- (host dump -> stdin)"
echo

echo "## 5. every rule file in the source closure of ~/.config/hypr/hyprland.conf, one run"
echo "\$ python3 -I closure-list.py | wc -l"
python3 -I closure-list.py | wc -l
echo "\$ python3 -I closure-list.py"
python3 -I closure-list.py
echo "exit=$?"
mapfile -t FILES < <(python3 -I closure-list.py)
ARGS=()
for f in "${FILES[@]}"; do ARGS+=(--rules "$f"); done
echo "\$ python3 -I mado-geometry.py --clients host-clients-live.json ${ARGS[*]}"
python3 -I mado-geometry.py --clients host-clients-live.json "${ARGS[@]}"
echo "exit=$?"
echo "--- (full closure, host dump)"
echo

echo "## 6. blind-spot probes against the real closure"
echo "# A client whose size Hyprland takes from an UNSUPPORTED rule (tag/title match) must show up as"
echo "# unmatched, not DIFFER: the tool has no rule-to-tag/title graph. Reported, not scored."
echo "\$ cat fx-tag-btop.json   # btop carries tag floating-window -> system.conf size 875 600, match:tag"
cat fx-tag-btop.json
echo "--- (fx-tag-btop.json)"
echo "\$ python3 -I mado-geometry.py --clients fx-tag-btop.json --rules (full closure)"
python3 -I mado-geometry.py --clients fx-tag-btop.json "${ARGS[@]}"
echo "exit=$?"
echo "--- (tag blind spot)"
echo "\$ cat fx-steam.json   # class steam: float rule supported, both size rules title-constrained"
cat fx-steam.json
echo "--- (fx-steam.json)"
echo "\$ python3 -I mado-geometry.py --clients fx-steam.json --rules (full closure)"
python3 -I mado-geometry.py --clients fx-steam.json "${ARGS[@]}"
echo "exit=$?"
echo "--- (title blind spot)"
echo

echo "## 7. shape checks over the same closure (what kinds of size line exist at all)"
echo "\$ grep -hnE 'windowrule[ \t]*=' <closure> | grep -cE '=[ \t]*size[ \t]+[0-9]{1,5}[ \t]+[0-9]{1,5}'"
grep -hE 'windowrule[ \t]*=' "${FILES[@]}" 2>/dev/null | grep -cE '=[ \t]*size[ \t]+[0-9]{1,5}[ \t]+[0-9]{1,5}'
echo "# ... = literal 'size W H' effect lines (the tool's rules= plus unsupported size lines)"
echo "\$ grep -hE 'windowrule[ \t]*=' <closure> | grep -E '=[ \t]*size[ \t]+[0-9]{1,5}[ \t]+[0-9]{1,5}'"
grep -hE 'windowrule[ \t]*=' "${FILES[@]}" 2>/dev/null | grep -E '=[ \t]*size[ \t]+[0-9]{1,5}[ \t]+[0-9]{1,5}'
echo "\$ grep -rn 'border_size' <closure>   (the near-miss effect word, counted as other)"
grep -rn 'border_size' "${FILES[@]}" 2>/dev/null; echo "exit=$? (1 = none found)"
echo "\$ grep -rnE '(size[ \t]+[0-9.]+%|size[ \t]+\\()' <closure>   (percentage or expression sizes)"
grep -rnE '(size[ \t]+[0-9.]+%|size[ \t]+\()' "${FILES[@]}" 2>/dev/null; echo "exit=$? (1 = none found)"
echo "\$ grep -rn 'initial_class' <closure>"
grep -rn 'initial_class' "${FILES[@]}" 2>/dev/null; echo "exit=$? (1 = none found)"
echo "\$ grep -rn 'negative:' <closure>   (RE2 negative matches)"
grep -rn 'negative:' "${FILES[@]}" 2>/dev/null; echo "exit=$? (1 = none found)"
echo "\$ grep -rnE '^[ \t]*#[ \t]*windowrule' <closure> | wc -l   (commented-out rule lines, ignored by the tool)"
grep -rnE '^[ \t]*#[ \t]*windowrule' "${FILES[@]}" 2>/dev/null | wc -l
echo

echo "## 8. per-file census with reasons (source-census.py)"
echo "\$ python3 -I source-census.py mado-geometry.py"
python3 -I source-census.py mado-geometry.py
echo "exit=$?"
echo
echo "# END"
