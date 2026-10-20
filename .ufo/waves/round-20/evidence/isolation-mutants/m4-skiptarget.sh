#!/usr/bin/env bash
# Intentional mutant: skip missing targets instead of failing the whole setup.
set -u
stub=
declare -a targets=() command=()
while (($# > 0)); do
    case "$1" in
        --stub) (($# >= 2)) || exit 125; stub=$2; shift 2 ;;
        --target) (($# >= 2)) || exit 125; targets+=("$2"); shift 2 ;;
        --) shift; command=("$@"); break ;;
        *) exit 125 ;;
    esac
done
[[ -n $stub && ${#targets[@]} -gt 0 && ${#command[@]} -gt 0 ]] || exit 125
ready=$(mktemp /tmp/mado-m4-ready.XXXXXX) || exit 125
rm -f -- "$ready" || exit 125
if unshare --user --map-root-user --mount --propagation private bash -c '
    set -u
    stub=$1; ready=$2; shift 2
    declare -a targets=()
    while (($# > 0)); do
        if [[ $1 == -- ]]; then shift; break; fi
        targets+=("$1"); shift
    done
    (($# > 0)) || exit 125
    for target in "${targets[@]}"; do
        [[ -e $target ]] || continue
        command mount --bind "$stub" "$target" || exit 125
    done
    for target in "${targets[@]}"; do
        [[ -e $target ]] || continue
        cmp -s -- "$target" "$stub" || exit 125
    done
    : > "$ready" || exit 125
    exec "$@"
' m4-child "$stub" "$ready" "${targets[@]}" -- "${command[@]}"; then status=0; else status=$?; fi
if [[ -e $ready ]]; then rm -f -- "$ready" || :; exit "$status"; fi
rm -f -- "$ready" || :
exit 125
