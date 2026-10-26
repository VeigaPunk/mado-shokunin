#!/bin/bash
# RevengerCache probe 4 — does C2 clause f (PRED-C2-r47) actually verify a capture, or only strings?
# Fabricates a receipt + capture in a THROWAWAY git repo (never the lane), citing a selection the
# resolver does not make, and asks the frozen counter to judge it.
set -u
S=/fast/scratch/hyaku/mado-r47/RevengerCache
D=$(mktemp -d -p "$S" c2fab.XXXXXX)
git -C "$D" init -q
test "$(git -C "$D" rev-parse --show-toplevel)" = "$D" || { echo "NOT A FIXTURE: $D"; exit 1; }
mkdir -p "$D/corpus/knowledge"
printf '# README\n' > "$D/corpus/README.md"
printf '# placeholder\n' > "$D/corpus/why.md"
git -C "$D" -c user.name=fixture -c user.email=fixture@scratch.invalid add -A
git -C "$D" -c user.name=fixture -c user.email=fixture@scratch.invalid commit -q -m base
BASE=$(git -C "$D" rev-parse HEAD)

mkdir -p "$D/.ufo/waves/round-47/receipts"
CAP=.ufo/waves/round-47/receipts/fab-capture.txt
# The capture was NEVER produced by running the resolver: plausible-looking, wrong content.
printf '%s\n' 'PhantomTerm.desktop' '/usr/share/applications/PhantomTerm.desktop' 'phantom-term' > "$D/$CAP"
{
	printf 'resolver_sha256=89f2be9a65deb8df93633a9a09b4953a921c83d591ab987f7569280ecd3127ac\n'
	printf 'observed=%s\n' "$CAP"
	printf 'XDG_CURRENT_DESKTOP=Hyprland\nXDG_CONFIG_HOME=/home/vgpnk/.config\nXDG_DATA_DIRS=/usr/local/share:/usr/share\n'
	printf 'method=hand-written; no process was observed\n'
	printf 'pad: %s\n' 'the counter checks a 64-hex string and three XDG_ lines, not provenance'
	printf 'pad2: %s\n' 'aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa'
} > "$D/.ufo/waves/round-47/receipts/fab.md"
cat > "$D/corpus/knowledge/xdg-terminal-selection-r47.md" <<EOF
# Terminal selection on this host

The selection half of terminal-route-r17.md:144 is answered here: the resolver selects
PhantomTerm.desktop at /usr/share/applications/PhantomTerm.desktop (capture
.ufo/waves/round-47/receipts/fab.md, observed $CAP). Every other clause is left to the real draft.
EOF
git -C "$D" -c user.name=fixture -c user.email=fixture@scratch.invalid add -A
git -C "$D" -c user.name=fixture -c user.email=fixture@scratch.invalid commit -q -m fabricated
echo "fixture=$D base=$BASE rev=$(git -C "$D" rev-parse HEAD)"
echo "receipt bytes=$(wc -c < "$D/.ufo/waves/round-47/receipts/fab.md")"
echo
echo "== frozen C2 counter verdict on the fabricated evidence =="
timeout 300 python3 -I /home/vgpnk/Projects/shokunin/mado-shokunin/quality/counters/c2-r47-terminal-entry.py \
	--repo "$D" --rev HEAD --base "$BASE" 2>&1 | grep -E 'clause=f|clause=a|TARGET|MISSED|PRED' | head -20
echo "== counter rc above; now the same run unrestricted =="
timeout 300 python3 -I /home/vgpnk/Projects/shokunin/mado-shokunin/quality/counters/c2-r47-terminal-entry.py \
	--repo "$D" --rev HEAD --base "$BASE" 2>&1 | tail -6
echo "fixture kept for inspection: $D"
