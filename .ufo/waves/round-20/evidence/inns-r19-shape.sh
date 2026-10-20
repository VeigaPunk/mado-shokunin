#!/usr/bin/env bash
set -euo pipefail

usage() {
    printf 'usage: %s --stub STUB --target PATH [--target PATH ...] -- CMD...\n' "$0" >&2
    exit 125
}

stub=
declare -a targets=()
declare -a command=()
while (($# > 0)); do
    case "$1" in
        --stub)
            (($# >= 2)) || usage
            [[ -z $stub ]] || usage
            stub=$2
            shift 2
            ;;
        --target)
            (($# >= 2)) || usage
            targets+=("$2")
            shift 2
            ;;
        --)
            shift
            command=("$@")
            break
            ;;
        *)
            usage
            ;;
    esac
done
[[ -n $stub && ${#targets[@]} -gt 0 && ${#command[@]} -gt 0 ]] || usage

unshare --user --map-root-user --mount --propagation private bash -c '
    set -e
    stub=$1
    shift
    declare -a targets=()
    while (($# > 0)); do
        if [[ $1 == -- ]]; then
            shift
            break
        fi
        targets+=("$1")
        shift
    done
    (($# > 0)) || exit 125
    for p in "${targets[@]}"; do
        [ -e "$p" ] && mount --bind "$stub" "$p" && echo "armed $p"
    done
    exec "$@"
' inns-r19-shape-child "$stub" "${targets[@]}" -- "${command[@]}"
