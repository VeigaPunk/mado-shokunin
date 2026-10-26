#!/bin/bash
# RevengerCache probe — read-only host observation + scratch-only resolver runs.
# Never launches a terminal; every resolver run uses a --print-* option and an XDG_CACHE_HOME in scratch.
set -u
S=/fast/scratch/hyaku/mado-r47/RevengerCache
mkdir -p "$S"; cd "$S" || exit 1
PICK=/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-47/fetch/xdg-terminal-exec
SRCCACHE=$HOME/.cache/xdg-terminal-exec

echo "== A. identity of the resolver actually on the hotkey path =="
sha256sum /usr/bin/xdg-terminal-exec "$PICK"

echo
echo "== B. compositor (Hyprland) environment, only HOME/PATH/XDG_* =="
HPID=$(pgrep -x Hyprland | head -1)
echo "compositor pid present: $([ -n "$HPID" ] && echo yes)"
ENVF=$S/hyprland.env
: > "$ENVF"
while IFS='=' read -r k v; do
	case "$k" in
	HOME|PATH|XDG_*) printf '%s=%s\n' "$k" "$v" >> "$ENVF" ;;
	esac
done < <(tr '\0' '\n' < "/proc/$HPID/environ")
grep -E '^(XDG_|HOME)' "$ENVF" | sed -E 's#/home/vgpnk#~#' | sort

# load into this shell (values are path-like, no spaces on this host)
while IFS='=' read -r k v; do case "$k" in HOME|PATH|XDG_*) export "$k=$v" ;; esac; done < "$ENVF"

echo
echo "== C. path lists exactly as make_paths() builds them (fetch/xdg-terminal-exec:141-171) =="
LOW=$(printf '%s' "${XDG_CURRENT_DESKTOP-}" | tr '[:upper:]' '[:lower:]')
OIFS=$IFS
CONFIGS=
IFS=':'
for d in ${XDG_CONFIG_HOME:-"$HOME/.config"}${IFS}${XDG_CONFIG_DIRS:-/etc/xdg}; do
	for desk in ${LOW}; do
		CONFIGS=${CONFIGS:+$CONFIGS:}${d%/}/${desk}-xdg-terminals.list
	done
	CONFIGS=${CONFIGS:+$CONFIGS:}${d%/}/xdg-terminals.list
done
for d in ${XDG_DATA_DIRS:-/usr/local/share:/usr/share}; do
	for desk in ${LOW}; do
		CONFIGS=${CONFIGS:+$CONFIGS:}${d%/}/xdg-terminal-exec/${desk}-xdg-terminals.list
	done
	CONFIGS=${CONFIGS:+$CONFIGS:}${d%/}/xdg-terminal-exec/xdg-terminals.list
done
APPS=
for d in ${XDG_DATA_HOME:-$HOME/.local/share}${IFS}${XDG_DATA_DIRS:-/usr/local/share:/usr/share}; do
	APPS=${d%/}/applications/${APPS:+:$APPS}
done
IFS=$OIFS
printf 'CONFIGS=%s\n' "$CONFIGS"
printf 'APPS=%s\n' "$APPS"

echo
echo "== D. independent md5 recomputation of gen_hash() input (fetch/xdg-terminal-exec:186-219) =="
HASH_PATHS=$CONFIGS:$APPS
{
	echo 4
	echo "${XDG_CURRENT_DESKTOP-}"
	IFS=':'
	# shellcheck disable=SC2086
	LANG=C LC_ALL=C ls -LRl ${HASH_PATHS} 2> /dev/null
} > "$S/hash-input.txt"
MD5=$(md5sum < "$S/hash-input.txt" | cut -d' ' -f1)
echo "recomputed_md5=$MD5"
echo "cache_line1=$(head -1 "$SRCCACHE")"
if [ "$MD5" = "$(head -1 "$SRCCACHE")" ]; then echo "VERDICT_HASH: MATCH"; else echo "VERDICT_HASH: MISMATCH"; fi
echo "hash-input size=$(wc -c < "$S/hash-input.txt") lines=$(wc -l < "$S/hash-input.txt")"
echo "first 8 lines of hash input:"; head -8 "$S/hash-input.txt"

echo
echo "== E. resolver itself, warm cache copy vs cold (both XDG_CACHE_HOME in scratch) =="
rm -rf "$S/cA" "$S/cB"; mkdir -p "$S/cA" "$S/cB"
cp "$SRCCACHE" "$S/cA/xdg-terminal-exec"   # byte copy of the host cache, host file untouched
ENVARGS=()
while IFS='=' read -r k v; do case "$k" in HOME|PATH|XDG_*) ENVARGS+=("$k=$v") ;; esac; done < "$ENVF"

for mode in A B; do
	cache=$S/c$mode
	timeout 90 env -i "${ENVARGS[@]}" XDG_CACHE_HOME="$cache" XTE_DEBUG=1 \
		"$PICK" --print-id --print-path --print-cmd > "$S/out$mode.txt" 2> "$S/err$mode.txt"
	echo "run $mode rc=$?"
done
echo "-- outA (warm) --"; sed -n l "$S/outA.txt"
echo "-- outB (cold) --"; sed -n l "$S/outB.txt"
echo "-- cache-use verdict lines --"
grep -nE 'no cache data|cache is actual|cache is out-of-date|invalid cache data|got fresh hash|saved cache|got cache:' "$S/errA.txt" "$S/errB.txt"
echo "-- warm-vs-cold stdout diff --"; diff "$S/outA.txt" "$S/outB.txt" && echo "IDENTICAL"
echo "-- cold-written cache line1 vs host cache line1 --"
head -1 "$S/cB/xdg-terminal-exec" 2>/dev/null
echo "host: $(head -1 "$SRCCACHE")"

echo
echo "== F. what the cache path would desynchronise on: PATH-only candidate check =="
printf 'alacritty: %s\n' "$(command -v alacritty || echo ABSENT)"
printf 'cache line2 cmd resolves: %s\n' "$(command -v "$(sed -n 2p "$SRCCACHE")" || echo ABSENT)"

echo
echo "== G. metadata-only coverage proof: is the LIST CONTENT inside the hash input? =="
grep -c 'xdg-terminals.list' "$S/hash-input.txt"
awk 'length($0) > 0 {print}' "$S/hash-input.txt" | grep -n 'xdg-terminals.list' | head -5
