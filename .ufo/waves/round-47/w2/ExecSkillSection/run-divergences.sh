#!/bin/sh
# Operator-facing divergence captures for w1/ScrSkill/section.md, host environment.
# Print modes only; XDG_CACHE_HOME always inside $WORK.
# Usage: run-divergences.sh WORKDIR [REFERENCE]
set -u
W=${1:?work dir}
REF=${2:-/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-47/l1-draft/mado-terminal.py}
R=/usr/bin/xdg-terminal-exec
mkdir -p "$W/tools" "$W/tmp"
cp "$REF" "$W/tools/mado-terminal.py"
unset XDG_CONFIG_HOME XDG_CONFIG_DIRS XDG_DATA_HOME XDG_DATA_DIRS XTE_DEBUG XTE_EXECARG_COMPAT XTE_CACHE_ENABLED
export HOME=/home/vgpnk PATH=/usr/local/bin:/usr/bin:/bin XDG_CURRENT_DESKTOP=Hyprland TMPDIR="$W/tmp"
cd "$W" || exit 1
say() { echo; echo "===== $* ====="; }
cap() { d=$(mktemp -d -p "$W"); XDG_CACHE_HOME=$d "$R" "$@"; }

say "H1 session-tool stamp vs the line the section quotes"
XDG_CACHE_HOME="$W/tools" python3 tools/mado-terminal.py explain | grep '^MADO_TERM:'
echo "--- section quotes:"; sed -n '35p' /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-47/w1/ScrSkill/section.md

say "H4b XDG_CURRENT_DESKTOP unset: the desktop line prints a '-' the docstring never defines"
env -u XDG_CURRENT_DESKTOP XDG_CACHE_HOME="$W/tools" python3 tools/mado-terminal.py explain >nc.out 2>&1; echo "rc=$?"; head -2 nc.out

say "H2 print --test (section: no print flag is a usage error)"
XDG_CACHE_HOME="$W/tools" python3 tools/mado-terminal.py print --test -- htop; echo "tool rc=$?"
cap --test -- htop; echo "resolver rc=$?"

say "H3 --print-content (section: contract does not cover it)"
XDG_CACHE_HOME="$W/tools" python3 tools/mado-terminal.py print --print-content > pc.tool; echo "tool rc=$? sha=$(sha256sum < pc.tool)"
cap --print-content > pc.real; echo "resolver rc=$? sha=$(sha256sum < pc.real)"
cmp -s pc.tool pc.real && echo "BYTES EQUAL"
XDG_CACHE_HOME="$W/tools" python3 tools/mado-terminal.py print --print-content --print-cmd > pcc.tool
cap --print-content --print-cmd > pcc.real
echo "--print-content --print-cmd: tool sha=$(sha256sum < pcc.tool)"
echo "--print-content --print-cmd: resolver sha=$(sha256sum < pcc.real)"
cmp -s pcc.tool pcc.real && echo "BYTES EQUAL"

say "H5 rc 1 stderr: tool vs resolver (empty tree)"
B=$W/empty; rm -rf "$B"; mkdir -p "$B/home/.config" "$B/etc/xdg" "$B/home/.local/share/applications" "$B/usr/share/applications" "$B/cache"
OLDHOME=$HOME; export HOME=$B/home XDG_CONFIG_HOME=$B/home/.config XDG_CONFIG_DIRS=$B/etc/xdg XDG_DATA_HOME=$B/home/.local/share XDG_DATA_DIRS=$B/usr/share
XDG_CACHE_HOME=$B/cache "$R" --print-id >r.out 2>r.err; echo "resolver rc=$?"; sed 's/^/  resolver-stderr| /' r.err
XDG_CACHE_HOME=$B/cache python3 tools/mado-terminal.py print --print-id >t.out 2>t.err; echo "tool rc=$?"; sed 's/^/  tool-stderr    | /' t.err
cmp -s r.err t.err && echo "stderr BYTES EQUAL" || echo "stderr DIFFERS (stdout is the contracted surface)"
export HOME=$OLDHOME; unset XDG_CONFIG_HOME XDG_CONFIG_DIRS XDG_DATA_HOME XDG_DATA_DIRS

say "H6 capture made with a non-default print flag: DIFFER on an identical selection"
cap --print-id --print-path --print-cmd --print-delimiter='|' > term.pipe.observed
od -c term.pipe.observed
XDG_CACHE_HOME="$W/tools" python3 tools/mado-terminal.py explain --observed term.pipe.observed >d1.out 2>&1; echo "rc=$?"; tail -1 d1.out

say "H6b capture with --print-id only: DIFFER"
cap --print-id > term.id.observed
XDG_CACHE_HOME="$W/tools" python3 tools/mado-terminal.py explain --observed term.id.observed >d2.out 2>&1; echo "rc=$?"; tail -1 d2.out

say "H7 empty capture (a no-terminal resolver run, rc 1) -> AGREE with selected=-"
B2=$W/empty2; rm -rf "$B2"; mkdir -p "$B2/home/.config" "$B2/etc/xdg" "$B2/home/.local/share/applications" "$B2/usr/share/applications" "$B2/cache"
OLDHOME=$HOME; export HOME=$B2/home XDG_CONFIG_HOME=$B2/home/.config XDG_CONFIG_DIRS=$B2/etc/xdg XDG_DATA_HOME=$B2/home/.local/share XDG_DATA_DIRS=$B2/usr/share
XDG_CACHE_HOME=$B2/cache "$R" --print-id --print-path --print-cmd > term.none.observed; echo "resolver rc=$? bytes=$(wc -c < term.none.observed)"
XDG_CACHE_HOME=$B2/cache python3 tools/mado-terminal.py explain --observed term.none.observed >d3.out 2>&1; echo "rc=$?"; tail -1 d3.out
export HOME=$OLDHOME; unset XDG_CONFIG_HOME XDG_CONFIG_DIRS XDG_DATA_HOME XDG_DATA_DIRS

say "H8 --selftest with TMPDIR pointing at a missing dir"
TMPDIR="$W/no-such-dir" XDG_CACHE_HOME="$W/tools" python3 tools/mado-terminal.py --selftest >st.out 2>st.err; echo "rc=$?"; tail -1 st.err
