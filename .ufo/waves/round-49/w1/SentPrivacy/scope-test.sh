#!/usr/bin/env bash
# scope-test.sh - does the gate read the trees this round writes?
# Fixture repo only; every value synthetic; prints rule lines, never values.
set -eu
ulimit -f 65536
S=/fast/scratch/hyaku/mado-r49/SentPrivacy/scope
rm -rf -- "$S"; mkdir -p "$S"
D=$(mktemp -d -p "$S" repo.XXXXXX)
git -C "$D" init -q
export GIT_AUTHOR_NAME=fixture GIT_AUTHOR_EMAIL=fixture@example.invalid
export GIT_COMMITTER_NAME=fixture GIT_COMMITTER_EMAIL=fixture@example.invalid
git -C "$D" rev-parse --show-toplevel

# A: a shape the gate misses (binds projection with home paths + script names)
missed() {
cat <<'EOF'
# hyprctl binds -j projection (synthetic)
- bind: modmask=64 key=S dispatcher=exec arg=~/.config/hypr/scripts/synthetic-launch
- bind: modmask=64 key=slash dispatcher=exec arg=/home/example/.local/bin/synthetic-menu
EOF
}
# B: a shape the gate catches (a bare home listing above the threshold)
caught() {
  for i in $(seq 1 12); do printf '/home/example/dir%02d/file.txt\n' "$i"; done
}
for t in .ufo/waves/round-49/w1/Seat corpus/knowledge tools quality/counters; do
  mkdir -p "$D/$t"
  missed > "$D/$t/binds-projection.txt"
done
caught > "$D/tools/listing-caught.txt"
caught > "$D/corpus/knowledge/listing-caught.txt"
git -C "$D" add -A && git -C "$D" commit -qm fixture
REV=$(git -C "$D" rev-parse HEAD)
printf 'REV %s toplevel %s\n' "$REV" "$(git -C "$D" rev-parse --show-toplevel)"

GATE=/home/vgpnk/Projects/shokunin/mado-shokunin/quality/check-session-material.py
echo "== scope ufo (default)"
python3 "$GATE" --repo "$D" --rev "$REV" || echo "rc=$?"
echo "== scope all"
python3 "$GATE" --repo "$D" --rev "$REV" --scope all || echo "rc=$?"
echo "== tracked files by tree"
git -C "$D" ls-tree -r --name-only "$REV" | sed 's#/[^/]*$##' | sort | uniq -c
rm -rf -- "$D"
