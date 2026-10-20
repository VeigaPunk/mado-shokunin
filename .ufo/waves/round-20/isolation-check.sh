#!/usr/bin/env bash
set -u

if (($# != 1)); then
    printf 'usage: %s HARNESS\n' "$0" >&2
    printf 'COULD_NOT_EVALUATE harness argument missing\n'
    exit 2
fi
harness=$1
harness_name=${harness##*/}
if [[ ! -x $harness ]]; then
    printf 'COULD_NOT_EVALUATE %s (not executable)\n' "$harness_name"
    exit 2
fi

original_path=$PATH
# Keep inherited shell functions from bypassing the PATH-controlled fixtures.
unset -f mount unshare cmp 2>/dev/null || :
tmp=$(mktemp -d /tmp/mado-isolation-check.XXXXXX) || {
    printf 'COULD_NOT_EVALUATE %s (cannot create /tmp workspace)\n' "$harness_name"
    exit 2
}
trap 'rm -rf -- "$tmp"' EXIT

cat > "$tmp/payload.sh" <<'EOF'
#!/usr/bin/env bash
[[ $# == 1 ]] || exit 91
printf 'payload-ran\n' > "$1"
EOF
chmod +x -- "$tmp/payload.sh" || exit 2

overall_failure=0
overall_unknown=0

run_case() {
    local name=$1
    local mode=$2
    shift 2
    local case_dir=$tmp/$name
    local case_bin=$case_dir/bin
    local stub_path=$case_dir/stub
    local canary=$case_dir/canary
    local marker=$case_dir/injected
    local log=$case_dir/output.log
    local run_path=$original_path
    local status=0
    local injection_required=0
    local target_name target
    local -a targets=()
    local -a args=()

    mkdir -p -- "$case_bin" || exit 2
    : > "$marker" || exit 2
    if [[ $mode != missing-stub ]]; then
        printf 'stub-bytes-%s\n' "$name" > "$stub_path" || exit 2
    fi
    for target_name in "$@"; do
        target=$case_dir/$target_name
        targets+=("$target")
        if [[ ! ( $mode == missing-target && $target_name == missing-target ) ]]; then
            printf 'original-bytes-%s-%s\n' "$name" "$target_name" > "$target" || exit 2
        fi
    done

    case $mode in
        mount-nonzero|mount-noop|partial-arm)
            injection_required=1
            run_path=$case_bin:$original_path
            cat > "$case_bin/mount" <<'EOF'
#!/usr/bin/env bash
set -u
printf '%s\n' "${3-<no-target>}" >> "${CHECK_MARKER:?}" || exit 97
case "${CHECK_MODE:?}" in
    mount-nonzero)
        printf 'forced mount failure (exit 32)\n' >&2
        exit 32
        ;;
    mount-noop)
        printf 'forced successful no-op mount\n' >&2
        exit 0
        ;;
    partial-arm)
        if [[ ${3##*/} == t2 ]]; then
            printf 'forced second-target mount failure (exit 32)\n' >&2
            exit 32
        fi
        PATH="${CHECK_REAL_PATH:?}" mount "$@"
        exit $?
        ;;
esac
exit 98
EOF
            chmod +x -- "$case_bin/mount" || exit 2
            ;;
        unshare-refused)
            injection_required=1
            run_path=$case_bin:$original_path
            cat > "$case_bin/unshare" <<'EOF'
#!/usr/bin/env bash
set -u
printf 'invoked\n' >> "${CHECK_MARKER:?}" || exit 97
printf 'forced unshare refusal (exit 1)\n' >&2
exit 1
EOF
            chmod +x -- "$case_bin/unshare" || exit 2
            ;;
    esac

    args=(--stub "$stub_path")
    for target in "${targets[@]}"; do
        args+=(--target "$target")
    done
    args+=(-- "$tmp/payload.sh" "$canary")

    printf '\nTRANSCRIPT setup-failure harness=%s mode=%s targets=%d\n' "$harness_name" "$name" "${#targets[@]}"
    printf 'COMMAND:'
    printf ' %q' "$harness" "${args[@]}"
    printf '\nINJECTION: %s\n' "$([[ $injection_required == 1 ]] && printf PATH-stub || printf real-filesystem-failure)"
    if PATH="$run_path" CHECK_MODE="$mode" CHECK_MARKER="$marker" CHECK_REAL_PATH="$original_path" "$harness" "${args[@]}" > "$log" 2>&1; then
        status=0
    else
        status=$?
    fi
    printf 'output:\n'
    cat -- "$log"
    printf 'harness exit: %d; canary=%s; injected-marker=%s\n' "$status" "$([[ -e $canary ]] && printf present || printf absent)" "$([[ -s $marker ]] && printf present || printf absent)"

    if ((injection_required == 1)) && [[ ! -s $marker ]]; then
        printf 'COULD_NOT_EVALUATE %s mode=%s (injected stub was not invoked)\n' "$harness_name" "$name"
        overall_unknown=1
    elif [[ -e $canary ]]; then
        printf 'FAIL_OPEN %s mode=%s\n' "$harness_name" "$name"
        overall_failure=1
    elif ((status == 0)); then
        printf 'FAIL_OPEN %s mode=%s SKIP_AS_SUCCESS (exit 0 without canary)\n' "$harness_name" "$name"
        overall_failure=1
    else
        printf 'FAIL_CLOSED %s mode=%s\n' "$harness_name" "$name"
    fi
}

run_case mount-nonzero mount-nonzero target
run_case unshare-refused unshare-refused target
run_case mount-noop mount-noop target
run_case partial-arm partial-arm t1 t2
run_case missing-target missing-target missing-target
run_case missing-stub missing-stub target

positive_dir=$tmp/positive
mkdir -p -- "$positive_dir" || exit 2
positive_stub=$positive_dir/stub
positive_target=$positive_dir/target
positive_canary=$positive_dir/canary
positive_log=$positive_dir/output.log
printf 'positive-stub-bytes\n' > "$positive_stub" || exit 2
printf 'positive-original-bytes\n' > "$positive_target" || exit 2
printf '\nTRANSCRIPT positive-control harness=%s\n' "$harness_name"
printf 'COMMAND:'
printf ' %q' "$harness" --stub "$positive_stub" --target "$positive_target" -- "$tmp/payload.sh" "$positive_canary"
printf '\n'
if CHECK_MODE=positive CHECK_MARKER="$positive_dir/injected" CHECK_REAL_PATH="$original_path" "$harness" --stub "$positive_stub" --target "$positive_target" -- "$tmp/payload.sh" "$positive_canary" > "$positive_log" 2>&1; then
    positive_status=0
else
    positive_status=$?
fi
printf 'output:\n'
cat -- "$positive_log"
printf 'harness exit: %d; canary=%s\n' "$positive_status" "$([[ -e $positive_canary ]] && printf present || printf absent)"
if ((positive_status == 0)) && [[ -e $positive_canary ]]; then
    printf 'POSITIVE_CONTROL_OK %s\n' "$harness_name"
else
    printf 'NEVER_RUNS %s positive control (exit=%d, canary=%s)\n' "$harness_name" "$positive_status" "$([[ -e $positive_canary ]] && printf present || printf absent)"
    exit 1
fi

if ((overall_failure == 1)); then
    exit 1
fi
if ((overall_unknown == 1)); then
    exit 2
fi
exit 0
