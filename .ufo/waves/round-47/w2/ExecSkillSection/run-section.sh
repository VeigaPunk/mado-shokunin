#!/bin/sh
# Reproduce every command of w1/ScrSkill/section.md as written, with
#   - tools/mado-terminal.py := the L1 reference (l1-draft/mado-terminal.py)
#   - XDG_CACHE_HOME inside $WORK (the resolver's print modes write a cache)
#   - print-only resolver invocations (never without a --print-* flag: that launches a terminal)
# Usage: run-section.sh WORKDIR [REFERENCE]
set -u
W=${1:?work dir}
REF=${2:-/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-47/l1-draft/mado-terminal.py}
R=/usr/bin/xdg-terminal-exec
mkdir -p "$W/tools" "$W/cache" "$W/tmp"
cp "$REF" "$W/tools/mado-terminal.py"
[ -x "$R" ] || { echo "missing $R"; exit 1; }
# host shape: drop any inherited XDG dir overrides so the run is the operator's shell
unset XDG_CONFIG_HOME XDG_CONFIG_DIRS XDG_DATA_HOME XDG_DATA_DIRS XTE_DEBUG XTE_EXECARG_COMPAT XTE_CACHE_ENABLED
export HOME=/home/vgpnk PATH=/usr/local/bin:/usr/bin:/bin XDG_CURRENT_DESKTOP=Hyprland TMPDIR="$W/tmp"
cd "$W" || exit 1
say() { echo; echo "===== $* ====="; }

say "resolve sha256 of the pinned script"
sha256sum "$R"

say "SECTION CMD 1: print --print-id --print-path --print-cmd"
XDG_CACHE_HOME="$W/cache" python3 tools/mado-terminal.py print --print-id --print-path --print-cmd; echo "rc=$?"

say "SECTION CMD 2: print ... --dir=/tmp -- htop"
XDG_CACHE_HOME="$W/cache" python3 tools/mado-terminal.py print --print-id --print-path --print-cmd --dir=/tmp -- htop; echo "rc=$?"

say "SECTION CMD 3: explain (doc quotes 'MADO_TERM: selected=... verdict=OK')"
XDG_CACHE_HOME="$W/cache" python3 tools/mado-terminal.py explain; echo "rc=$?"

say "SECTION CMD 4a: cold capture with the resolver"
CAP=$(mktemp -d -p "$W")
XDG_CACHE_HOME="$CAP" "$R" --print-id --print-path --print-cmd > term.observed; echo "rc=$?"
cat term.observed
sleep 1
echo "cache files written by the resolver run (backgrounded save_cache): $(ls -A "$CAP" | wc -l)"

say "SECTION CMD 4b: explain --observed term.observed"
XDG_CACHE_HOME="$W/cache" python3 tools/mado-terminal.py explain --observed term.observed; echo "rc=$?"

say "SECTION CMD 5: --selftest"
XDG_CACHE_HOME="$W/cache" python3 tools/mado-terminal.py --selftest; echo "rc=$?"

say "SYMPTOM TABLE: print --dir=/tmp --print-cmd (look for --working-directory)"
XDG_CACHE_HOME="$W/cache" python3 tools/mado-terminal.py print --dir=/tmp --print-cmd; echo "rc=$?"

say "NOTES: XTE_DEBUG=1 ... xdg-terminal-exec --print-id (debug on stderr)"
DBG=$(mktemp -d -p "$W")
XTE_DEBUG=1 XDG_CACHE_HOME="$DBG" "$R" --print-id >dbg.out 2>dbg.err; echo "rc=$?"
echo "stdout:"; cat dbg.out; echo "stderr lines: $(wc -l < dbg.err)"; sed -n '1,2p' dbg.err

say "EXIT STATUS: print with no --print-* flag"
python3 tools/mado-terminal.py print; echo "rc=$?"

say "EXIT STATUS: print --test -- htop (a non-print mode the section calls a usage error)"
XDG_CACHE_HOME="$W/cache" python3 tools/mado-terminal.py print --test -- htop; echo "rc=$?"
echo "resolver:"; D=$(mktemp -d -p "$W"); XDG_CACHE_HOME="$D" "$R" --test -- htop; echo "rc=$?"

say "EXIT STATUS: unknown mode; unreadable --observed"
python3 tools/mado-terminal.py frobnicate; echo "rc=$?"
python3 tools/mado-terminal.py explain --observed "$W/nonexistent.observed"; echo "rc=$?"

say "NOTE: --print-content (section says the contract does not cover it)"
echo "tool:"; XDG_CACHE_HOME="$W/cache" python3 tools/mado-terminal.py print --print-content | sha256sum
D=$(mktemp -d -p "$W"); echo "resolver:"; XDG_CACHE_HOME="$D" "$R" --print-content | sha256sum

say "TMPDIR set to a missing directory"
TMPDIR="$W/no-such-dir" XDG_CACHE_HOME="$W/cache" python3 tools/mado-terminal.py --selftest >tmpd.out 2>tmpd.err
echo "rc=$?"; tail -2 tmpd.err

say "tool with a fresh XDG_CACHE_HOME: files written by the TOOL"
Z=$(mktemp -d -p "$W")
XDG_CACHE_HOME="$Z" python3 tools/mado-terminal.py print --print-id --print-path --print-cmd --dir=/tmp -- htop >/dev/null
echo "rc=$?; files in XDG_CACHE_HOME after the tool run: $(ls -A "$Z" | wc -l)"
Z2=$(mktemp -d -p "$W")
XDG_CACHE_HOME="$Z2" "$R" --print-id >/dev/null; sleep 1
echo "resolver --print-id only: files after the run: $(ls -A "$Z2" | wc -l)"
Z3=$(mktemp -d -p "$W")
XDG_CACHE_HOME="$Z3" "$R" --print-id --print-path --print-cmd >/dev/null; sleep 1
echo "resolver with --print-cmd: files after the run: $(ls -A "$Z3" | wc -l)"
