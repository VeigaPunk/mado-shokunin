#!/bin/bash
echo "A) bash -c under env -u HOME:"
env -u HOME bash --noprofile --norc -c 'echo "   HOME=[${HOME-<unset>}] exported=$(env | grep -c "^HOME=")"'
echo "B) /bin/sh -c under env -u HOME (sh = bash):"
env -u HOME /bin/sh -c 'echo "   HOME=[${HOME-<unset>}] exported=$(env | grep -c "^HOME=")"'
echo "C) the pin expansion with XDG_CONFIG_HOME and HOME both absent, set -u:"
env -u HOME -u XDG_CONFIG_HOME /bin/sh -c 'set -u; echo "   ${XDG_CONFIG_HOME:-${HOME}/.config}"; echo "   rc=$?"'
echo "D) the real pin, HOME absent, everything else absent (host defaults):"
env -u HOME -u XDG_CONFIG_HOME -u XDG_CONFIG_DIRS -u XDG_DATA_HOME -u XDG_DATA_DIRS -u XDG_CACHE_HOME timeout 10 /usr/bin/xdg-terminal-exec --print-id; echo "   pin rc=$?"
echo "E) same, with only PID-dependent noise removed: which sh -> $(readlink -f /bin/sh)"
