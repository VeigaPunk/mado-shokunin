#!/usr/bin/env bash
# Round 48 live read-only capture of the resolver's WARM cache against tools/mado-terminal.py.
# The host's own cache (~/.cache/xdg-terminal-exec) is never read or written: XDG_CACHE_HOME points into a fresh scratch
# dir. Only --print-* options are passed, so no terminal is launched. The scratch cache is primed by the resolver itself
# (a cold --print-cmd run saves it in the background), then edited INSIDE the scratch dir to show stale and invalid.
# Usage: live-terminal-cache.sh OUT   (run from the lane root)
set -u
OUT=$1
S=$(mktemp -d -p "${HYAKU_SCRATCH:-/fast/scratch/hyaku}/mado-r48" live-XXXX)
trap 'rm -rf -- "$S"' EXIT
C=$S/cache; mkdir -p "$C"
R=/usr/bin/xdg-terminal-exec
T=tools/mado-terminal.py
E=(env -i HOME="$HOME" PATH=/usr/local/bin:/usr/bin LANG="${LANG:-C.UTF-8}" XDG_CONFIG_DIRS=/etc/xdg
   XDG_CONFIG_HOME="$HOME/.config" XDG_CURRENT_DESKTOP=Hyprland XDG_DATA_DIRS=/usr/local/share:/usr/share
   XDG_DATA_HOME="$HOME/.local/share" XDG_CACHE_HOME="$C")
three=(--print-id --print-path --print-cmd)
wait_cache() { local n=0; while [ $n -lt 200 ]; do grep -q $'\x1eEND_OF_EXEC_USEP' "$C/xdg-terminal-exec" 2>/dev/null && return 0; sleep 0.05; n=$((n+1)); done; return 1; }
state() { case "$1" in *"cache is actual"*) echo hit ;; *"cache is out-of-date"*) echo stale ;; *"invalid cache data"*|*"reached cache line limit"*) echo invalid ;; *"no cache data"*) echo absent ;; *) echo disabled ;; esac; }
leg() {
  local name=$1
  # the resolver may re-save its cache during the run, so it and the tool each read their own copy of the same bytes
  rm -rf "$S/a" "$S/b"; cp -a "$C" "$S/a"; cp -a "$C" "$S/b"
  "${E[@]}" XDG_CACHE_HOME="$S/a" XTE_DEBUG=1 "$R" "${three[@]}" > "$S/o.out" 2> "$S/o.err"; local orc=$?
  local ost; ost=$(state "$(cat "$S/o.err")")
  "${E[@]}" XDG_CACHE_HOME="$S/b" python3 -I "$T" print "${three[@]}" > "$S/t.out" 2>/dev/null; local trc=$?
  local ex; ex=$("${E[@]}" XDG_CACHE_HOME="$S/b" python3 -I "$T" explain --observed "$S/o.out" 2>/dev/null | grep '^MADO_TERM: '); local erc=$?
  echo "## $name"
  echo "resolver rc=$orc state=$ost stdout_sha256=$(sha256sum < "$S/o.out" | cut -d' ' -f1)"
  echo "tool     rc=$trc stdout_sha256=$(sha256sum < "$S/t.out" | cut -d' ' -f1) print_agree=$(cmp -s "$S/o.out" "$S/t.out" && echo yes || echo no)"
  echo "explain  $ex"
  sed 's/^/resolver_stdout: /' "$S/o.out"
}
{
  echo "# round-48 live read-only warm-cache capture, $(date -Iseconds); no terminal launched; XDG_CACHE_HOME=<scratch dir>"
  echo "resolver=$R resolver_sha256=$(sha256sum < "$R" | cut -d' ' -f1)"
  echo "tool=$T tool_sha256=$(sha256sum < "$T" | cut -d' ' -f1)"
  echo "host_cache_untouched_sha256=$(sha256sum < "$HOME/.cache/xdg-terminal-exec" | cut -d' ' -f1)"
  leg "cold (no cache file)"
  "${E[@]}" "$R" --print-cmd > /dev/null 2>&1; wait_cache && echo "# primed by the resolver: $(wc -l < "$C/xdg-terminal-exec") lines" || echo "# PRIME FAILED"
  leg "warm (the resolver's own cache)"
  sed -i '1s/^./0/' "$C/xdg-terminal-exec"; echo "# scratch cache line 1 edited (hash no longer matches)"
  leg "stale (hash mismatch)"
  "${E[@]}" "$R" --print-cmd > /dev/null 2>&1; wait_cache
  sed -i 's/\x1eEND_OF_EXEC_USEP//' "$C/xdg-terminal-exec"; echo "# scratch cache terminator removed"
  leg "invalid (no terminator)"
  echo "host_cache_after_sha256=$(sha256sum < "$HOME/.cache/xdg-terminal-exec" | cut -d' ' -f1)"
} > "$OUT"
grep -E '^## |^resolver rc|^tool |^explain|^host' "$OUT"
