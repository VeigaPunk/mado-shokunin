#!/usr/bin/env bash
set -u

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

# A private completion marker distinguishes setup failure from the payload's
# own exit status while keeping all state outside the caller's target paths.
ready=$(mktemp /tmp/mado-isolate-ready.XXXXXX) || exit 125
rm -f -- "$ready" || exit 125

if unshare --user --map-root-user --mount --propagation private bash -c '
    set -u
    stub=$1
    ready=$2
    shift 2
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
    for target in "${targets[@]}"; do
        command mount --bind "$stub" "$target" || exit 125
    done
    for target in "${targets[@]}"; do
        cmp -s -- "$target" "$stub" || exit 125
    done
    : > "$ready" || exit 125
    exec "$@"
' isolate-child "$stub" "$ready" "${targets[@]}" -- "${command[@]}"; then
    status=0
else
    status=$?
fi

if [[ -e $ready ]]; then
    rm -f -- "$ready" || :
    exit "$status"
fi
rm -f -- "$ready" || :
exit 125
