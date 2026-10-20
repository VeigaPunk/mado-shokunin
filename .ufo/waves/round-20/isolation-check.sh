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

tmp=$(mktemp -d /tmp/mado-isolation-check.XXXXXX) || {
    printf 'COULD_NOT_EVALUATE %s (cannot create /tmp workspace)\n' "$harness_name"
    exit 2
}
trap 'rm -rf -- "$tmp"' EXIT
# A caller-exported mount function must not supersede the PATH-first failure stub.
unset -f mount 2>/dev/null || :

# The injected mount command fails deterministically, while the harness target,
# stub, payload, and both canary paths remain ordinary files under this /tmp dir.
mkdir -- "$tmp/fail-bin" || exit 2
cat > "$tmp/fail-bin/mount" <<'EOF'
#!/bin/sh
printf 'forced mount setup failure (exit 32)\n' >&2
exit 32
EOF
chmod +x -- "$tmp/fail-bin/mount" || exit 2
cat > "$tmp/payload.sh" <<'EOF'
#!/bin/sh
[ "$#" -eq 1 ] || exit 91
printf 'payload-ran\n' > "$1"
EOF
chmod +x -- "$tmp/payload.sh" || exit 2

fail_stub=$tmp/fail.stub
fail_target=$tmp/fail.target
fail_canary=$tmp/fail-canary
fail_log=$tmp/fail.log
printf 'stub-failure-bytes\n' > "$fail_stub" || exit 2
printf 'original-target-bytes\n' > "$fail_target" || exit 2
forced_path=$tmp/fail-bin:$PATH
if PATH="$forced_path" "$harness" --stub "$fail_stub" --target "$fail_target" -- "$tmp/payload.sh" "$fail_canary" >"$fail_log" 2>&1; then
    fail_status=0
else
    fail_status=$?
fi

printf '%s\n' "TRANSCRIPT setup-failure: $harness_name"
printf '+ PATH=%q ' "$forced_path"
printf '%q ' "$harness" --stub "$fail_stub" --target "$fail_target" -- "$tmp/payload.sh" "$fail_canary"
printf '\noutput:\n'
cat -- "$fail_log"
printf 'harness exit: %d\n' "$fail_status"
if [[ -e $fail_canary ]]; then
    printf 'FAIL_OPEN %s\n' "$harness_name"
    failure_result=1
elif ((fail_status != 0)); then
    printf 'FAIL_CLOSED %s\n' "$harness_name"
    failure_result=0
else
    printf 'COULD_NOT_EVALUATE %s (exit 0, canary absent)\n' "$harness_name"
    failure_result=2
fi

# Positive control: use fresh /tmp-only target/stub/canary files and the
# system mount implementation. The harness must reach the same canary payload.
pos_stub=$tmp/positive.stub
pos_target=$tmp/positive.target
pos_canary=$tmp/positive-canary
pos_log=$tmp/positive.log
printf 'stub-positive-bytes\n' > "$pos_stub" || exit 2
printf 'original-positive-bytes\n' > "$pos_target" || exit 2
if "$harness" --stub "$pos_stub" --target "$pos_target" -- "$tmp/payload.sh" "$pos_canary" >"$pos_log" 2>&1; then
    pos_status=0
else
    pos_status=$?
fi
printf '%s\n' "TRANSCRIPT positive-control: $harness_name"
printf '+ '
printf '%q ' "$harness" --stub "$pos_stub" --target "$pos_target" -- "$tmp/payload.sh" "$pos_canary"
printf '\noutput:\n'
cat -- "$pos_log"
printf 'harness exit: %d\n' "$pos_status"
if ((pos_status == 0)) && [[ -e $pos_canary ]]; then
    printf 'POSITIVE_CONTROL_OK %s\n' "$harness_name"
else
    printf 'NEVER_RUNS %s positive control (exit=%d, canary=%s)\n' "$harness_name" "$pos_status" "$([[ -e $pos_canary ]] && printf present || printf absent)"
    exit 1
fi

case $failure_result in
    0) exit 0 ;;
    1) exit 1 ;;
    *) exit 2 ;;
esac
