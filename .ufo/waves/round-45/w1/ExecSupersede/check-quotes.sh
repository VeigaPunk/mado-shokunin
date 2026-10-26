#!/bin/bash
# ExecSupersede (round 45 w1) - Gate-quote and locator checker for the seven supersession rows.
# Every quote is grepped literally in the receipt it names; locators are recomputed, never typed.
# The seven GATE quotes need only the lane receipts. The "secondary locators" and pin-hash blocks at the bottom
# read /fast/scratch/hyaku/mado-r45/ExecSupersede/src/, which existed when this ran (quotes.txt) and was deleted at
# seat exit; to re-run them, fetch the five pins plus Window.cpp, Rule.cpp and WindowRule.cpp from
# https://raw.githubusercontent.com/hyprwm/Hyprland/efb50993780079460b0cbed1363e2166a2de1d9f/src/... into that path.
set -u
L=/home/vgpnk/Projects/shokunin/mado-shokunin
fail=0
chk() { # chk <id> <receipt-rel> <quote> <expected-line>
  local id=$1 rc=$2 q=$3 ln=$4 f="$L/$2" got n w
  if [ ! -f "$f" ]; then echo "$id MISSING receipt $rc"; fail=$((fail+1)); return; fi
  n=$(grep -cF -- "$q" "$f")
  got=$(grep -nF -- "$q" "$f" | cut -d: -f1 | tr '\n' ',')
  w=$(printf '%s' "$q" | wc -w)
  if [ "$n" -ne 1 ]; then echo "$id FAIL occurrences=$n quote=$q"; fail=$((fail+1));
  elif [ "${got%,}" != "$ln" ]; then echo "$id FAIL line=$got expected=$ln quote=$q"; fail=$((fail+1));
  elif [ "$w" -gt 25 ]; then echo "$id FAIL words=$w quote=$q"; fail=$((fail+1));
  else echo "$id OK line=$ln words=$w sha256=$(sha256sum "$f" | cut -d' ' -f1) bytes=$(stat -c%s "$f")"; fi
}
F43=.ufo/waves/round-43/fetch
chk S311 "$F43/Hyprland-RegexMatchEngine.cpp" 'if (regex.starts_with("negative:")) {' 7
chk S312 "$F43/Hyprland-DefaultFloatingAlgorithm.cpp" 'if (WINDOW->m_ruleApplicator->static_.center.value_or(false)) {' 79
chk S313 "$F43/Hyprland-Target.cpp" 'void ITarget::rememberFloatingSize(const Vector2D& size) {' 68
chk S314 "$F43/Hyprland-WindowTarget.cpp" 'if (DESIRED_GEOM.width <= 2 || DESIRED_GEOM.height <= 2) {' 339
chk S315 "$F43/Hyprland-GeometricMovableAnimated.cpp" 'case IGeometric::GEOMETRIC_GOAL: return m_realSize->goal();' 19
chk S316 "$F43/host-clients-r43.json" '"class": "Alacritty",' 5
chk S317 "$F43/gkeep-ui-excerpt.py" 'window.set_default_size(420, 500)' 33

echo "--- secondary locators the corrected teaches cells name"
echo "S311 Rule.cpp class->engine: $(grep -nF '{RULE_PROP_CLASS, RULE_MATCH_ENGINE_REGEX},' /fast/scratch/hyaku/mado-r45/ExecSupersede/src/Rule.cpp | cut -d: -f1 | tr '\n' ',') makeUnique line: $(grep -nF 'makeUnique<CRegexMatchEngine>(s)' /fast/scratch/hyaku/mado-r45/ExecSupersede/src/Rule.cpp | cut -d: -f1 | tr '\n' ',')"
echo "S311 WindowRule class match: $(grep -nF 'engine->match(w->m_class)' /fast/scratch/hyaku/mado-r45/ExecSupersede/src/WindowRule.cpp | cut -d: -f1 | tr '\n' ',')"
echo "S312 tiled consumer: $(grep -nF 'calculateExpression(*m_ruleApplicator->static_.size)' /fast/scratch/hyaku/mado-r45/ExecSupersede/src/Window.cpp | cut -d: -f1 | tr '\n' ',') setPseudoSize: $(grep -n 'setPseudoSize' /fast/scratch/hyaku/mado-r45/ExecSupersede/src/Window.cpp | cut -d: -f1 | tr '\n' ',')"
echo "--- own-work sweeps"
echo "S316 fullscreen occurrences: $(grep -c fullscreen "$L/$F43/host-clients-r43.json") gkeep occurrences: $(grep -c gkeep "$L/$F43/host-clients-r43.json")"
echo "S317 size_request occurrences: $(grep -c size_request "$L/$F43/gkeep-ui-excerpt.py")"
echo "S317 excerpt :6 -> $(sed -n '6p' "$L/$F43/gkeep-ui-excerpt.py" | sed 's/^ *//') ; excerpt :33 -> $(sed -n '33p' "$L/$F43/gkeep-ui-excerpt.py" | sed 's/^ *//')"
echo "S317 excerpt body vs ui.py:446-488 (round-44 pin): $(tail -n 43 "$L/.ufo/waves/round-44/fetch/gkeep-ui.py" | cmp -s - <(tail -n +3 "$L/$F43/gkeep-ui-excerpt.py") && echo BYTE-EQUAL || echo DIFFER)"
echo "S317 full-file sha256: $(sha256sum "$L/.ufo/waves/round-44/fetch/gkeep-ui.py" | cut -d' ' -f1)"
echo "S316 dump keys: $(python3 -c "import json;print(','.join(sorted(json.load(open('$L/$F43/host-clients-r43.json'))[0].keys())))")"
echo "--- upstream pin hashes (fetched 2026-10-26 into scratch, compared with the row cells)"
for f in RegexMatchEngine DefaultFloatingAlgorithm Target WindowTarget GeometricMovableAnimated; do
  printf '%s %s %s\n' "$(stat -c%s /fast/scratch/hyaku/mado-r45/ExecSupersede/src/$f.cpp)" "$(sha256sum /fast/scratch/hyaku/mado-r45/ExecSupersede/src/$f.cpp | cut -d' ' -f1)" "$f.cpp"
done
echo "cross-ref hashes: $(sha256sum /fast/scratch/hyaku/mado-r45/ExecSupersede/src/Window.cpp | cut -d' ' -f1) Window.cpp, $(sha256sum /fast/scratch/hyaku/mado-r45/ExecSupersede/src/Rule.cpp | cut -d' ' -f1) Rule.cpp, $(sha256sum /fast/scratch/hyaku/mado-r45/ExecSupersede/src/WindowRule.cpp | cut -d' ' -f1) WindowRule.cpp"
echo "QUOTES: checked=7 failed=$fail"
exit $(( fail > 0 ))
