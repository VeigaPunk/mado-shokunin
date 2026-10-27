#!/bin/sh
# round-50 freeze do-nothing controls, frozen counters, scratch clones (fixture rule: toplevel asserted)
set -u
LANE=/home/vgpnk/Projects/shokunin/mado-shokunin
S=/fast/scratch/hyaku/mado-r50/L1Freeze
DATA=906178b607f2071af7c2efec5aad976a8bfa5757
BASE=8ae47b957034ae21012bbf09173cca2c48be345e
export TMPDIR=$S
rm -rf "$S/fx" && git clone -q --shared "$LANE" "$S/fx"
[ "$(git -C "$S/fx" rev-parse --show-toplevel)" = "$S/fx" ] || { echo TOPLEVEL-MISMATCH; exit 2; }
git -C "$S/fx" checkout -q --detach "$DATA"

# C1 control 1: entry-absent at base (frozen counter, frozen bytes)
echo "== c1-c00-absent (base $BASE)"
python3 -I "$LANE/quality/counters/c1-r50-bind-entry.py" --repo "$S/fx" --rev "$BASE"; echo "exit=$?"

# C1 control 2: r49 candidate pasted at the r50 path (do-nothing: skip writing the new entry)
git -C "$S/fx" show 13631f24050f22db92bf5bd33e0f4d014192992e:.ufo/waves/round-49/candidate/hyprland-bind-key-match-r49.md > "$S/fx/corpus/knowledge/hyprland-bind-key-match-r50.md"
git -C "$S/fx" add corpus/knowledge/hyprland-bind-key-match-r50.md
git -C "$S/fx" -c user.name=fixture -c user.email=fx@fixture commit -q -m "control c13: r49 candidate at r50 path"
R13=$(git -C "$S/fx" rev-parse HEAD)
echo "== c1-c13-r49-paste ($R13)"
python3 -I "$LANE/quality/counters/c1-r50-bind-entry.py" --repo "$S/fx" --rev "$R13"; echo "exit=$?"

# C1 control 3: stub entry (head + one sentence)
git -C "$S/fx" checkout -q --detach "$DATA"
{ head -1 "$S/fx/corpus/knowledge/hyprland-bind-key-match-r50.md"; echo "The KEY field matches a key press somehow; see the round-49 draft."; } > "$S/fx/corpus/knowledge/hyprland-bind-key-match-r50.md.new"
mv "$S/fx/corpus/knowledge/hyprland-bind-key-match-r50.md.new" "$S/fx/corpus/knowledge/hyprland-bind-key-match-r50.md"
git -C "$S/fx" add corpus/knowledge/hyprland-bind-key-match-r50.md
git -C "$S/fx" -c user.name=fixture -c user.email=fx@fixture commit -q -m "control c12: stub entry"
R12=$(git -C "$S/fx" rev-parse HEAD)
echo "== c1-c12-stub ($R12)"
python3 -I "$LANE/quality/counters/c1-r50-bind-entry.py" --repo "$S/fx" --rev "$R12"; echo "exit=$?"
