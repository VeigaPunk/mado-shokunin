#!/bin/sh
# Hermetic probes of the rules w1/ScrSkill/section.md states in its two tables.
# Runs the pinned resolver in print modes only (never without a --print-* flag)
# and the L1 reference as tools/mado-terminal.py, then compares stdout bytes.
# Usage: run-probes.sh WORKDIR [REFERENCE]
set -u
W=${1:?work dir}
REF=${2:-/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-47/l1-draft/mado-terminal.py}
R=/usr/bin/xdg-terminal-exec
B=$W/probe
rm -rf "$B"; mkdir -p "$B/tools" "$B/home/.config" "$B/etc/xdg" "$B/home/.local/share/applications" \
  "$B/usr/share/applications" "$B/cache"
cp "$REF" "$B/tools/mado-terminal.py"
mk() { p=$1; shift; printf '%s\n' "$@" > "$p"; }
E=$B/home/.local/share/applications
mk "$E/good.desktop" '[Desktop Entry]' 'Categories=System;TerminalEmulator;' 'Exec=sh' 'X-TerminalArgExec=-e' 'X-TerminalArgTitle=--title=' 'Actions=New;' '' '[Desktop Action New]' 'Exec=sh'
mk "$E/bad.desktop" '[Desktop Entry]' 'Categories=TerminalEmulator;' 'Exec=sh' 'Hidden=true'
mk "$E/link.desktop" '[Desktop Entry]' 'Type=Link' 'Categories=System;TerminalEmulator;' 'Exec=sh' 'X-TerminalArgExec=-e'
mk "$E/nodisp.desktop" '[Desktop Entry]' 'Categories=System;TerminalEmulator;' 'Exec=sh' 'NoDisplay=true' 'X-TerminalArgExec=-e'
mk "$E/onlygnome.desktop" '[Desktop Entry]' 'Categories=System;TerminalEmulator;' 'Exec=sh' 'OnlyShowIn=GNOME;' 'X-TerminalArgExec=-e'
# duplicate id: system copy has no X-TerminalArg* keys (the host's Alacritty shape)
mk "$B/usr/share/applications/dup.desktop" '[Desktop Entry]' 'Categories=System;TerminalEmulator;' 'Exec=sh' 'Actions=New;'
mk "$E/dup.desktop" '[Desktop Entry]' 'Categories=System;TerminalEmulator;' 'Exec=sh' 'X-TerminalArgExec=-e' 'X-TerminalArgDir=--working-directory='

unset XDG_CONFIG_HOME XDG_CONFIG_DIRS XDG_DATA_HOME XDG_DATA_DIRS XTE_DEBUG XTE_EXECARG_COMPAT XTE_CACHE_ENABLED
export HOME=$B/home XDG_CURRENT_DESKTOP=Hyprland XDG_CONFIG_HOME=$B/home/.config XDG_CONFIG_DIRS=$B/etc/xdg \
  XDG_DATA_HOME=$B/home/.local/share XDG_DATA_DIRS=$B/usr/share PATH=/usr/bin:/bin TMPDIR=$W/tmp
mkdir -p "$W/tmp"
cd "$B" || exit 1
LIST=$B/home/.config/xdg-terminals.list
set_list() { printf '%s\n' "$@" > "$LIST"; }
fresh_cache() { rm -rf "$B/cache"; mkdir -p "$B/cache"; }

pair() { # pair <label> <argv...> : resolver print vs tool print, byte compare
  label=$1; shift
  fresh_cache
  XDG_CACHE_HOME=$B/cache "$R" "$@" > r.out 2> r.err; rrc=$?
  XDG_CACHE_HOME=$B/cache python3 tools/mado-terminal.py print "$@" > t.out 2> t.err; trc=$?
  printf '\n---- %s ----\n' "$label"
  printf 'argv: %s\n' "$*"
  printf 'resolver rc=%s | tool rc=%s\n' "$rrc" "$trc"
  if cmp -s r.out t.out; then echo "stdout: BYTES EQUAL"; else echo "stdout: DIFFER"; diff r.out t.out; fi
  sed 's/^/  stdout| /' t.out
  [ -s r.err ] && sed 's/^/  resolver-stderr| /' r.err
}
say() { printf '\n===== %s =====\n' "$*"; }
trace() { fresh_cache; XDG_CACHE_HOME=$B/cache python3 tools/mado-terminal.py explain; echo "explain rc=$?"; }

say "P1 Type=Link + category + Exec is selected (section Notes: probes A/B)"
set_list link.desktop
pair "P1" --print-id --print-path --print-cmd

say "P2 NoDisplay=true is never read"
rm -f "$LIST"
pair "P2a fallback over the whole tree (no lists)" --print-id --print-path --print-cmd
set_list nodisp.desktop
pair "P2b NoDisplay=true, listed" --print-id --print-path --print-cmd

say "P3 list names Hidden=true first: skipped, trace names the reason"
set_list bad.desktop good.desktop
pair "P3" --print-id --print-path --print-cmd
echo "-- trace:"; trace

say "P4 OnlyShowIn=GNOME, fallback vs listed (section: fallback only)"
rm -f "$LIST"
pair "P4a fallback" --print-id --print-path --print-cmd
set_list onlygnome.desktop
pair "P4b listed" --print-id --print-path --print-cmd

say "P5 action not in Actions rejects; action in Actions selects id:action"
set_list good.desktop:BadAction
pair "P5a bad action (falls back)" --print-id --print-path --print-cmd
echo "-- trace:"; trace
set_list good.desktop:New
pair "P5b good action" --print-id --print-path --print-cmd

say "P6 empty --title= value composes nothing"
set_list good.desktop
pair "P6a --title=" --print-id --print-cmd --title=
pair "P6b --title=T" --print-id --print-cmd --title=T

say "P7 duplicate id: user data copy wins and supplies X-TerminalArgDir"
set_list dup.desktop
pair "P7" --print-id --print-path --print-cmd --dir=/tmp -- htop

say "P8 warm cache: explain reports cache=present, selection unchanged"
fresh_cache
XDG_CACHE_HOME=$B/cache "$R" --print-id --print-path --print-cmd >/dev/null; sleep 1
pair "P8" --print-id --print-path --print-cmd
echo "-- trace (cache= field):"; XDG_CACHE_HOME=$B/cache python3 tools/mado-terminal.py explain | tail -1
