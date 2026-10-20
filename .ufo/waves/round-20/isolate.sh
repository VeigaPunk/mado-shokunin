#!/usr/bin/bash
# Fail-closed setup is not containment; this is not a sandbox. Never run a host
# probe under the host pause. Unstubbed host paths, filesystem access, and other
# environment/session channels remain reachable by the payload.
set -u

usage() {
    printf 'usage: %s --stub STUB --target PATH [--target PATH ...] -- CMD...\n' "$0" >&2
    printf '%s\n' 'WARNING: fail-closed setup is not containment; not a sandbox; never run a host probe under the host pause.' >&2
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

ready=$(/usr/bin/mktemp /tmp/mado-isolate-v3-ready.XXXXXX) || exit 125
/usr/bin/rm -f -- "$ready" || exit 125

if command unshare --user --map-root-user --mount --propagation private /usr/bin/bash -c '
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
    stub_identity=$(/usr/bin/stat -Lc "%d:%i" -- "$stub") || exit 125
    for target in "${targets[@]}"; do
        target_identity=$(/usr/bin/stat -Lc "%d:%i" -- "$target") || exit 125
        [[ $target_identity == "$stub_identity" ]] || exit 125
    done
    : > "$ready" || exit 125
    unset HYPRLAND_INSTANCE_SIGNATURE WAYLAND_DISPLAY DBUS_SESSION_BUS_ADDRESS XDG_RUNTIME_DIR
    exec "$@"
' isolate-child "$stub" "$ready" "${targets[@]}" -- "${command[@]}"; then
    status=0
else
    status=$?
fi

if [[ -e $ready ]]; then
    /usr/bin/rm -f -- "$ready" || :
    exit "$status"
fi
/usr/bin/rm -f -- "$ready" || :
exit 125
