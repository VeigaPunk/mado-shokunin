#!/usr/bin/bash
# This check covers setup-failure behavior only. It is not a containment test.
set -u

if (($# != 1)); then
    printf 'usage: %s HARNESS\n' "$0" >&2
    printf 'COULD_NOT_EVALUATE harness argument missing\n'
    exit 2
fi
harness=$(/usr/bin/realpath -e -- "$1" 2>/dev/null) || {
    printf 'COULD_NOT_EVALUATE %s (harness path does not resolve)\n' "${1##*/}"
    exit 2
}
harness_name=${harness##*/}
if [[ ! -x $harness ]]; then
    printf 'COULD_NOT_EVALUATE %s (not executable)\n' "$harness_name"
    exit 2
fi

printf 'SCOPE %s: fail-closed setup only; not containment; not a sandbox; never run a host probe under the host pause.\n' "$harness_name"
original_path=$PATH
# Do not let test controls inherited by this checker leak into its subject.
unset CHECK_MODE CHECK_MARKER CHECK_REAL_PATH
unset -f mount unshare cmp 2>/dev/null || :
umask 077
tmp=$(/usr/bin/mktemp -d /tmp/mado-isolation-v3-check.XXXXXX) || {
    printf 'COULD_NOT_EVALUATE %s (cannot create /tmp workspace)\n' "$harness_name"
    exit 2
}
observer=$(/usr/bin/mktemp -d /tmp/mado-isolation-v3-observer.XXXXXX) || {
    /usr/bin/rm -rf -- "$tmp"
    printf 'COULD_NOT_EVALUATE %s (cannot create witness workspace)\n' "$harness_name"
    exit 2
}
/usr/bin/chmod 700 -- "$tmp" "$observer" || exit 2
trap '/usr/bin/rm -rf -- "$tmp" "$observer"' EXIT

cat > "$tmp/payload.sh" <<'EOF'
#!/usr/bin/bash
set -u
[[ $# == 1 ]] || exit 91
printf 'payload-ran\n' > "$1"
printf 'payload-ran\n' >&9
EOF
/usr/bin/chmod 700 -- "$tmp/payload.sh" || exit 2

open_witness() {
    local witness_path=$observer/witness-$1
    : > "$witness_path" || exit 2
    exec 9<> "$witness_path" || exit 2
    # Unlink the pathname before the harness starts; the payload inherits only fd 9.
    /usr/bin/rm -f -- "$witness_path" || exit 2
}

close_witness() {
    exec 9>&- || :
}

overall_failure=0
overall_unknown=0

run_case() {
    local name=$1
    local mode=$2
    shift 2
    local case_dir
    case_dir=$(/usr/bin/mktemp -d "$tmp/case.XXXXXX") || exit 2
    local case_bin=$case_dir/bin
    local stub_path=$case_dir/stub
    local canary=$case_dir/canary
    local marker=$case_dir/injected
    local cmp_marker=$case_dir/cmp-invoked
    local log=$case_dir/output.log
    local run_path=$original_path
    local status=0
    local injection_required=0
    local target_name target marker_q mode_q real_path_q cmp_marker_q
    local canary_state witness_state marker_state cmp_state
    local -a targets=()
    local -a args=()

    /usr/bin/mkdir -p -- "$case_bin" || exit 2
    : > "$marker" || exit 2
    : > "$cmp_marker" || exit 2
    if [[ $mode != missing-stub ]]; then
        printf 'stub-bytes-%s\n' "$name" > "$stub_path" || exit 2
    fi
    for target_name in "$@"; do
        target=$case_dir/$target_name
        targets+=("$target")
        if [[ ! ( $mode == missing-target && $target_name == absent ) ]]; then
            printf 'original-bytes-%s-%s\n' "$name" "$target_name" > "$target" || exit 2
        fi
    done

    case $mode in
        mount-nonzero|mount-noop|partial-arm)
            injection_required=1
            run_path=$case_bin:$original_path
            printf -v marker_q '%q' "$marker"
            printf -v mode_q '%q' "$mode"
            printf -v real_path_q '%q' "$original_path"
            cat > "$case_bin/mount" <<EOF
#!/usr/bin/bash
set -u
injected_marker=$marker_q
injected_mode=$mode_q
real_path=$real_path_q
printf '%s\\n' "\${3-<no-target>}" >> "\$injected_marker" || exit 97
case "\$injected_mode" in
    mount-nonzero)
        printf 'forced mount failure (exit 32)\\n' >&2
        exit 32
        ;;
    mount-noop)
        printf 'forced successful no-op mount\\n' >&2
        exit 0
        ;;
    partial-arm)
        if [[ \${3##*/} == t2 ]]; then
            printf 'forced second-target mount failure (exit 32)\\n' >&2
            exit 32
        fi
        PATH="\$real_path" mount "\$@"
        exit \$?
        ;;
esac
exit 98
EOF
            /usr/bin/chmod 700 -- "$case_bin/mount" || exit 2
            ;;
        unshare-refused)
            injection_required=1
            run_path=$case_bin:$original_path
            printf -v marker_q '%q' "$marker"
            cat > "$case_bin/unshare" <<EOF
#!/usr/bin/bash
set -u
injected_marker=$marker_q
printf 'invoked\\n' >> "\$injected_marker" || exit 97
printf 'forced unshare refusal (exit 1)\\n' >&2
exit 1
EOF
            /usr/bin/chmod 700 -- "$case_bin/unshare" || exit 2
            ;;
    esac

    # Challenge a PATH-resolved cmp in the no-op-mount arm. A correct verifier
    # must use kernel-backed identity evidence rather than trusting this stub.
    if [[ $mode == mount-noop ]]; then
        printf -v cmp_marker_q '%q' "$cmp_marker"
        cat > "$case_bin/cmp" <<EOF
#!/usr/bin/bash
set -u
cmp_marker=$cmp_marker_q
printf 'invoked\\n' >> "\$cmp_marker" || exit 97
exit 0
EOF
        /usr/bin/chmod 700 -- "$case_bin/cmp" || exit 2
    fi

    args=(--stub "$stub_path")
    for target in "${targets[@]}"; do
        args+=(--target "$target")
    done
    args+=(-- "$tmp/payload.sh" "$canary")

    printf '\nTRANSCRIPT setup-failure harness=%s mode=%s targets=%d\n' "$harness_name" "$name" "${#targets[@]}"
    printf 'COMMAND:'
    printf ' %q' "$harness" "${args[@]}"
    printf '\nINJECTION: %s; controls are not exported\n' "$([[ $injection_required == 1 ]] && printf PATH-stub || printf real-filesystem-failure)"
    open_witness "$name"
    if PATH="$run_path" "$harness" "${args[@]}" > "$log" 2>&1; then
        status=0
    else
        status=$?
    fi
    printf 'output:\n'
    cat -- "$log"
    canary_state=absent
    [[ -e $canary ]] && canary_state=present
    witness_state=absent
    [[ -s /proc/self/fd/9 ]] && witness_state=present
    close_witness
    marker_state=absent
    [[ -s $marker ]] && marker_state=present
    cmp_state=absent
    [[ -s $cmp_marker ]] && cmp_state=present
    printf 'harness exit: %d; canary=%s; execution-witness=%s; injected-marker=%s; cmp-stub=%s\n' "$status" "$canary_state" "$witness_state" "$marker_state" "$cmp_state"

    if ((injection_required == 1)) && [[ $marker_state == absent ]]; then
        printf 'COULD_NOT_EVALUATE %s mode=%s (injected stub was not invoked)\n' "$harness_name" "$name"
        overall_unknown=1
    elif [[ $witness_state == present ]]; then
        printf 'FAIL_OPEN %s mode=%s (payload execution witnessed)\n' "$harness_name" "$name"
        overall_failure=1
    elif ((status == 0)); then
        printf 'FAIL_OPEN %s mode=%s SKIP_AS_SUCCESS (exit 0 without payload witness)\n' "$harness_name" "$name"
        overall_failure=1
    else
        printf 'FAIL_CLOSED %s mode=%s\n' "$harness_name" "$name"
    fi
}

run_case mount-nonzero mount-nonzero target
run_case unshare-refused unshare-refused target
run_case mount-noop mount-noop target
run_case partial-arm partial-arm t1 t2
run_case missing-target missing-target absent
run_case missing-stub missing-stub target

positive_dir=$tmp/positive
/usr/bin/mkdir -p -- "$positive_dir" || exit 2
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
open_witness positive
if "$harness" --stub "$positive_stub" --target "$positive_target" -- "$tmp/payload.sh" "$positive_canary" > "$positive_log" 2>&1; then
    positive_status=0
else
    positive_status=$?
fi
printf 'output:\n'
cat -- "$positive_log"
positive_canary_state=absent
[[ -e $positive_canary ]] && positive_canary_state=present
positive_witness_state=absent
[[ -s /proc/self/fd/9 ]] && positive_witness_state=present
close_witness
printf 'harness exit: %d; canary=%s; execution-witness=%s\n' "$positive_status" "$positive_canary_state" "$positive_witness_state"
if ((positive_status == 0)) && [[ $positive_witness_state == present ]]; then
    printf 'POSITIVE_CONTROL_OK %s\n' "$harness_name"
else
    printf 'NEVER_RUNS %s positive control (exit=%d, canary=%s, witness=%s)\n' "$harness_name" "$positive_status" "$positive_canary_state" "$positive_witness_state"
    exit 2
fi

printf 'SCOPE %s: fail-closed setup only; not containment; not a sandbox; never run a host probe under the host pause.\n' "$harness_name"
if ((overall_failure == 1)); then
    exit 1
fi
if ((overall_unknown == 1)); then
    exit 2
fi
exit 0
