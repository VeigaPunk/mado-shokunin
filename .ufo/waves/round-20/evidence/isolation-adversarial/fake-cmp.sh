#!/usr/bin/bash
# Intentional hostile-PATH fixture: trusts a PATH-resolved cmp after bind.
set -u
stub=
declare -a targets=() payload=()
while (($# > 0)); do
    case "$1" in
        --stub) (($# >= 2)) || exit 125; stub=$2; shift 2 ;;
        --target) (($# >= 2)) || exit 125; targets+=("$2"); shift 2 ;;
        --) shift; payload=("$@"); break ;;
        *) exit 125 ;;
    esac
done
[[ -n $stub && ${#targets[@]} -gt 0 && ${#payload[@]} -gt 0 ]] || exit 125
ready=$(/usr/bin/mktemp /tmp/mado-fakecmp-ready.XXXXXX) || exit 125
/usr/bin/rm -f -- "$ready" || exit 125
if command unshare --user --map-root-user --mount --propagation private /usr/bin/bash -c '
    set -u
    stub=$1; ready=$2; shift 2
    declare -a targets=()
    while (($# > 0)); do
        if [[ $1 == -- ]]; then shift; break; fi
        targets+=("$1"); shift
    done
    (($# > 0)) || exit 125
    for target in "${targets[@]}"; do command mount --bind "$stub" "$target" || exit 125; done
    for target in "${targets[@]}"; do cmp -s -- "$target" "$stub" || exit 125; done
    : > "$ready" || exit 125
    exec "$@"
' fake-cmp-child "$stub" "$ready" "${targets[@]}" -- "${payload[@]}"; then status=0; else status=$?; fi
if [[ -e $ready ]]; then /usr/bin/rm -f -- "$ready" || :; exit "$status"; fi
/usr/bin/rm -f -- "$ready" || :
exit 125
