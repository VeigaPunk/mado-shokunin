#!/bin/sh
# Locator verification for every quote cited in ExecC1Determinism.md (round 47 w2).
# Each line prints "file:line -> text"; the locator is computed by grep -n here, never typed.
set -eu
L=/home/vgpnk/Projects/shokunin/mado-shokunin
P=$L/.ufo/waves/round-47/fetch/xdg-terminal-exec
T=$L/.ufo/waves/round-47/l1-draft/mado-terminal.py
B=$L/.ufo/waves/round-47/ctl/build-fixtures.py
C=$L/quality/counters/c1-r47-terminal.py
q() { f=$1; pat=$2; printf '%s -> ' "$(basename "$f")"; grep -nF -- "$pat" "$f" | head -1 || echo 'NOT FOUND'; }
q "$P" 'XTE__FALLBACK_ENTRY_IDS=${xte__entry_id}'
q "$P" 'LC_ALL=C find -L "$@"'
q "$P" 'command -v "$XTE__EXEC0"'
q "$P" 'LC_ALL=C gen_hash "$@"'
q "$P" 'LC_ALL=C read_config_paths "$@"'
q "$P" 'LC_ALL=C read_entry_path "$@"'
q "$P" 'debug "entry discarded"'
q "$T" 'self.fallback.insert(0, eid)'
q "$T" 'os.scandir(cur)'
q "$T" 'directory entries in readdir'
q "$B" '"x" * (k + 1)'
q "$B" 'if len(set(res)) != 1'
q "$C" 'oracle drifted from'
q "$C" 'lang = "en_US.UTF-8"'
q "$C" 'lang = "C.UTF-8"'
printf 'pin sha256: '; sha256sum "$P" | cut -d' ' -f1
printf 'reference sha256: '; sha256sum "$T" | cut -d' ' -f1
printf 'fixtures sha256: '; sha256sum "$L/quality/counters/c1-r47-fixtures.json" | cut -d' ' -f1
