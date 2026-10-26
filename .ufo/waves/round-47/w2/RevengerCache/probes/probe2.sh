#!/bin/bash
# RevengerCache probe 2 — resolution of "does the hotkey run read the cache?".
# The pinned fetch copy is mode 644 (not executable); an identical-sha256 copy in scratch is used.
# Every resolver invocation carries a --print-* option and an XDG_CACHE_HOME inside scratch.
set -u
S=/fast/scratch/hyaku/mado-r47/RevengerCache
cd "$S" || exit 1
XTE=$S/xte
SRCCACHE=$HOME/.cache/xdg-terminal-exec
ENVF=$S/hyprland.env
set -a
while IFS='=' read -r k v; do case "$k" in HOME|PATH|XDG_*) export "$k=$v" ;; esac; done < "$ENVF"
set +a
ENVARGS=()
while IFS='=' read -r k v; do case "$k" in HOME|PATH|XDG_*) ENVARGS+=("$k=$v") ;; esac; done < "$ENVF"

sha256sum "$XTE"

rm -rf "$S/cA" "$S/cB" "$S/cC"; mkdir -p "$S/cA" "$S/cB" "$S/cC"
cp "$SRCCACHE" "$S/cA/xdg-terminal-exec"       # byte copy of the HOST cache; host file only read
cp "$SRCCACHE" "$S/cC/xdg-terminal-exec"

run() { # $1=tag  $2=cachedir  rest=resolver args
	local tag=$1 cache=$2; shift 2
	timeout 120 env -i "${ENVARGS[@]}" XDG_CACHE_HOME="$cache" XTE_DEBUG=1 "$XTE" "$@" \
		> "$S/out$tag.txt" 2> "$S/err$tag.txt"
	echo "run $tag rc=$?"
}

echo "== E1. warm: host cache copied verbatim into scratch XDG_CACHE_HOME =="
run A "$S/cA" --print-id --print-path --print-cmd
echo "-- stdout --"; sed -n l "$S/outA.txt"
echo "-- cache decision --"; grep -nE 'no cache data|cache is actual|cache is out-of-date|invalid cache data|got fresh hash|saved cache|hash=' "$S/errA.txt"
echo "-- cache file after run A (must be unchanged bytes) --"; cmp -s "$SRCCACHE" "$S/cA/xdg-terminal-exec" && echo "unchanged" || echo "CHANGED-BY-RUN"

echo
echo "== E2. cold: empty scratch XDG_CACHE_HOME =="
run B "$S/cB" --print-id --print-path --print-cmd
echo "-- stdout --"; sed -n l "$S/outB.txt"
echo "-- cache decision --"; grep -nE 'no cache data|cache is actual|cache is out-of-date|invalid cache data|got fresh hash|saved cache|hash=' "$S/errB.txt"
echo "-- warm-vs-cold stdout --"; diff "$S/outA.txt" "$S/outB.txt" > /dev/null && echo IDENTICAL || diff "$S/outA.txt" "$S/outB.txt"
echo "-- cold-written cache line1 vs host line1 --"
printf 'cold=%s\nhost=%s\n' "$(head -1 "$S/cB/xdg-terminal-exec" 2>/dev/null)" "$(head -1 "$SRCCACHE")"
echo "-- cold-written cache vs host cache, full byte diff (line-numbered) --"
diff <(sed -n l "$SRCCACHE") <(sed -n l "$S/cB/xdg-terminal-exec") && echo "BYTE-IDENTICAL"

echo
echo "== E3. warm run with --dir and a command (hotkey shape: --dir=<cwd>) =="
run C "$S/cC" --dir=/home/vgpnk --print-id --print-path --print-cmd
echo "-- stdout --"; sed -n l "$S/outC.txt"
echo "-- cache decision --"; grep -nE 'cache is actual|cache is out-of-date|got fresh hash|saved cache' "$S/errC.txt"
echo "-- cache mutated by --dir run? --"; cmp -s "$SRCCACHE" "$S/cC/xdg-terminal-exec" && echo "unchanged" || { echo "MUTATED:"; diff <(sed -n l "$SRCCACHE") <(sed -n l "$S/cC/xdg-terminal-exec"); }

echo
echo "== E4. LIVE-path check: /usr/bin copy behaves as pinned copy under the same scratch cache =="
timeout 120 env -i "${ENVARGS[@]}" XDG_CACHE_HOME="$S/cA" XTE_DEBUG=1 /usr/bin/xdg-terminal-exec --print-id --print-path --print-cmd > "$S/outA2.txt" 2> "$S/errA2.txt"
echo "run A2(installed) rc=$?"
cmp -s "$S/outA.txt" "$S/outA2.txt" && echo "stdout identical to pinned copy"
grep -nE 'cache is actual|cache is out-of-date' "$S/errA2.txt"
