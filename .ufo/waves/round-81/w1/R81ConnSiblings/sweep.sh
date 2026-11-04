#!/bin/sh
# R81ConnSiblings — sibling-overlap sweep, round 81 w1. Read-only across the fleet.
# Writes only into this seat directory (captures) and /fast scratch is not used.
set -u
F=/home/vgpnk/Projects/shokunin
K=/home/vgpnk/Projects/shokuknow/merge/mado
S=$F/mado-shokunin/.ufo/waves/round-81/w1/R81ConnSiblings

cd "$F" || exit 1

# ---- A: layer-surface / reserved-band / auto-exclusive-zone family, whole fleet minus mado ----
{
  printf '$ cd %s\n' "$F"
  printf '$ grep -rniE "layer[-_]?shell|exclusive[ _-]?zone|reserved[ _-]?band|arrangeLayerArray|zwlr_layer|gtk-layer" --include=*.md --include=*.py --include=*.sh --include=*.mjs --include=*.json --include=*.jsonl --include=*.txt --include=*.c . | grep -v ^./mado-shokunin/ | grep -v ^./.ufo/ | grep -v ^./.scratch/\n'
  grep -rniE 'layer[-_]?shell|exclusive[ _-]?zone|reserved[ _-]?band|arrangeLayerArray|zwlr_layer|gtk-layer' \
    --include=*.md --include=*.py --include=*.sh --include=*.mjs --include=*.json --include=*.jsonl \
    --include=*.txt --include=*.c . 2>/dev/null \
    | grep -v '^\./mado-shokunin/' | grep -v '^\./\.ufo/' | grep -v '^\./\.scratch/'
  printf 'rc=%s\n' "$?"
} > "$S/sweep-a-layer.txt" 2>&1

# ---- B: omarchy keybindings-output family, whole fleet minus mado ----
{
  printf '$ grep -rniE "omarchy-menu-keybindings|omarchy menu keybindings|cut -c36-" --include=*.md --include=*.py --include=*.sh --include=*.mjs --include=*.json --include=*.jsonl --include=*.txt . | excl mado/.ufo/.scratch\n'
  grep -rniE 'omarchy-menu-keybindings|omarchy menu keybindings|cut -c36-' \
    --include=*.md --include=*.py --include=*.sh --include=*.mjs --include=*.json --include=*.jsonl \
    --include=*.txt . 2>/dev/null \
    | grep -v '^\./mado-shokunin/' | grep -v '^\./\.ufo/' | grep -v '^\./\.scratch/'
  printf '\n# the bare phrase "action column" is a HOMONYM (kaidoku scored decision-table column);\n'
  printf '# count per lane so it is quantified, never quoted as overlap:\n'
  printf '$ grep -rli "action column" ... | cut -d/ -f2 | sort | uniq -c | sort -rn\n'
  grep -rli 'action column' --include=*.md --include=*.py --include=*.sh --include=*.mjs \
    --include=*.json --include=*.txt . 2>/dev/null \
    | grep -v '^\./mado-shokunin/' | grep -v '^\./\.ufo/' | grep -v '^\./\.scratch/' \
    | cut -d/ -f2 | sort | uniq -c | sort -rn
} > "$S/sweep-b-omarchy-output.txt" 2>&1

# ---- C: pgrep-shaped liveness, per file, whole fleet minus mado ----
{
  printf '$ grep -rniE "pgrep +-x" --include=*.md --include=*.py --include=*.sh --include=*.mjs . | excl mado | cut -d: -f1 | sort | uniq -c | sort -rn\n'
  grep -rniE 'pgrep +-x' --include=*.md --include=*.py --include=*.sh --include=*.mjs . 2>/dev/null \
    | grep -v '^\./mado-shokunin/' | cut -d: -f1 | sort | uniq -c | sort -rn
  printf '\n$ same, lane source surfaces only (no .ufo wave dirs)\n'
  grep -rniE 'pgrep +-x' --include=*.md --include=*.py --include=*.sh --include=*.mjs . 2>/dev/null \
    | grep -v '^\./mado-shokunin/' | grep -v '/\.ufo/' | cut -d: -f1 | sort | uniq -c | sort -rn
} > "$S/sweep-c-pgrep.txt" 2>&1

# ---- D: lane-source scope only, all four families, no wave dirs ----
{
  printf '$ for lane in *-shokunin/ (minus mado): grep -rniE "<four families>" $lane --include=*.md --include=*.py --include=*.sh --include=*.mjs | grep -v /\.ufo/\n'
  for lane in */; do
    case "$lane" in mado-shokunin/|./) continue;; esac
    grep -rniE 'layer[-_]?shell|exclusive[ _-]?zone|reserved[ _-]?band|arrangeLayerArray|zwlr_layer|gtk-layer|omarchy-menu-keybindings|pgrep +-x' \
      "$lane" --include=*.md --include=*.py --include=*.sh --include=*.mjs 2>/dev/null \
      | grep -v '/\.ufo/'
  done
  printf '%s\n' '--- end of lane-source sweep (nothing above this marker = no hits) ---'
} > "$S/sweep-d-lane-scope.txt" 2>&1

# ---- E: sibling PROVINCE quotes ----
{
  printf '$ grep -niE "waybar|layer.?shell|exclusive.?zone|reserved.?band|omarchy|pgrep|hyprctl|hyprland|compositor" */PROVINCE.md | grep -v ^mado-shokunin/\n'
  grep -niE 'waybar|layer.?shell|exclusive.?zone|reserved.?band|omarchy|pgrep|hyprctl|hyprland|compositor' \
    */PROVINCE.md 2>/dev/null | grep -v '^mado-shokunin/'
} > "$S/sweep-e-province.txt" 2>&1

# ---- F: sibling SKILL matcher forms ----
{
  printf '$ grep -niE "pgrep -x|waybar|omarchy-menu|cut -c" */SKILL.md | grep -v ^mado-shokunin/\n'
  grep -niE 'pgrep -x|waybar|omarchy-menu|cut -c' */SKILL.md 2>/dev/null | grep -v '^mado-shokunin/'
} > "$S/sweep-f-skill.txt" 2>&1

# ---- G: staged assimilation package ----
{
  printf '$ cd %s\n' "$K"
  cd "$K" || { printf 'CD FAILED\n'; exit 1; }
  printf '$ pwd\n'; pwd
  printf '$ ls knowledge/corpus/knowledge | wc -l ; ls amendments/corpus/knowledge | wc -l\n'
  ls knowledge/corpus/knowledge | wc -l
  ls amendments/corpus/knowledge | wc -l
  printf '$ grep -rniE "\\bexclusive\\b|gtk-layer-shell|barfoot|footprint|reserved band|arrangeLayerArray" knowledge/corpus/knowledge amendments/corpus/knowledge SOURCES.append.md MERGE-REPORT.md\n'
  grep -rniE '\bexclusive\b|gtk-layer-shell|barfoot|footprint|reserved band|arrangeLayerArray' \
    knowledge/corpus/knowledge amendments/corpus/knowledge SOURCES.append.md MERGE-REPORT.md 2>/dev/null
  printf '$ grep -rn "omarchy-menu-keybindings" .\n'
  grep -rn 'omarchy-menu-keybindings' . 2>/dev/null
  printf '$ grep -rniE "omarchy-menu|keybindings --print|menu keybindings" knowledge amendments MERGE-REPORT.md\n'
  grep -rniE 'omarchy-menu|keybindings --print|menu keybindings' \
    knowledge/corpus/knowledge amendments/corpus/knowledge MERGE-REPORT.md 2>/dev/null
  printf '$ grep -rn "pgrep" knowledge/corpus/knowledge amendments/corpus/knowledge\n'
  grep -rn 'pgrep' knowledge/corpus/knowledge amendments/corpus/knowledge 2>/dev/null
  printf '$ grep -rli "runbook" knowledge/corpus/knowledge amendments/corpus/knowledge\n'
  grep -rli 'runbook' knowledge/corpus/knowledge amendments/corpus/knowledge 2>/dev/null
  printf 'rc(no-match forms)=%s\n' "$?"
} > "$S/sweep-g-merge-package.txt" 2>&1

# ---- H: fleet-root artifacts that carry the grounds ----
{
  cd "$F" || exit 1
  printf '$ cd %s\n' "$F"
  sed -n '44409,44440p' "$F/MANIFEST.json"
  printf '\n$ python3 -c "import json; d=json.load(open(.tower/quarantine/fleet-root-strays-20261026T2055/tree.json)); print(d[sha], d[url])"\n'
  python3 - <<'PY'
import json
p='/home/vgpnk/Projects/shokunin/.tower/quarantine/fleet-root-strays-20261026T2055/tree.json'
d=json.load(open(p))
print('sha=', d.get('sha'))
print('url=', d.get('url'))
hits=[e['path'] for e in d.get('tree',[]) if 'ayershell' in e['path'] or 'layer-shell' in e['path']]
print('layer-shell paths=', hits)
PY
  printf '\n$ ls -la .tower/quarantine/fleet-root-strays-20261026T2055/\n'
  ls -la "$F/.tower/quarantine/fleet-root-strays-20261026T2055/"
} > "$S/sweep-h-fleet-root.txt" 2>&1

# ---- I: kotoba fixture + census ledger ----
{
  printf '$ grep -oE "\\"[^\\"]*waybar[^\\"]*\\"" kotoba-shokunin/verifiers/fixtures/compare-harness-independent/record-map-24-composition/live.json\n'
  grep -oE '"[^"]*waybar[^"]*"' \
    kotoba-shokunin/verifiers/fixtures/compare-harness-independent/record-map-24-composition/live.json
  printf '\n$ head -12 kotoba-shokunin/.ufo/waves/round-82/receipts/after-host-skill-census-ledger.txt\n'
  head -12 kotoba-shokunin/.ufo/waves/round-82/receipts/after-host-skill-census-ledger.txt
  printf '\n$ grep -c omarchy kotoba-shokunin/.ufo/waves/round-82/receipts/after-host-skill-census-ledger.txt\n'
  grep -c omarchy kotoba-shokunin/.ufo/waves/round-82/receipts/after-host-skill-census-ledger.txt
} > "$S/sweep-i-kotoba.txt" 2>&1

# ---- J: the kumitate r81 capture that carries mado's instrument text ----
{
  printf '$ head -1 kumitate-shokunin/.ufo/waves/round-81/w1/K81ConnOverlap-captures/grep-05-admission.txt\n'
  head -1 kumitate-shokunin/.ufo/waves/round-81/w1/K81ConnOverlap-captures/grep-05-admission.txt
  printf '\n$ grep -n "mado-shokunin" ... | head -12\n'
  grep -n 'mado-shokunin' kumitate-shokunin/.ufo/waves/round-81/w1/K81ConnOverlap-captures/grep-05-admission.txt | head -12
  printf '\n$ grep -c "mado-shokunin" ...\n'
  grep -c 'mado-shokunin' kumitate-shokunin/.ufo/waves/round-81/w1/K81ConnOverlap-captures/grep-05-admission.txt
} > "$S/sweep-j-kumitate-capture.txt" 2>&1

# ---- K: mado's own rows for the two grounds (the anchors a census keys on) ----
{
  printf '$ grep -n "cut -c36-|cut -c1-35|^| .pgrep -x waybar" mado-shokunin/SKILL.md\n'
  grep -nE 'cut -c36-|cut -c1-35|`pgrep -x waybar' mado-shokunin/SKILL.md
  printf '\n$ python3 - (frozen control names/kinds for the two grounds)\n'
  python3 - <<'PY'
import json
for p, want in (('/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-81/controls/c2-runbook-cases-r81.json',
                 ('keybindings-actions','waybar-pgrep','waybar-process')),
                ('/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-81/controls/c1-cases-r81.json',
                 None)):
    d=json.load(open(p))
    cs=d['cases'] if isinstance(d,dict) else d
    print(p.rsplit('/',1)[-1], 'cases=', len(cs))
    for c in cs:
        if want is None:
            if any(k in c.get('name','') for k in ('overflow','auto-')):
                print('  ', c.get('name'), '->', json.dumps(c.get('expect') or c.get('expected'))[:200])
        elif c.get('name') in want:
            print('  ', c.get('name'), 'kind=', c.get('kind'), 'argv=', c.get('argv'), 'anchor=', c.get('skill_anchor'))
PY
} > "$S/sweep-k-mado-rows.txt" 2>&1

printf 'captures written to %s\n' "$S"
ls -1 "$S"
