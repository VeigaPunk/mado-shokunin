#!/usr/bin/env bash
set -euo pipefail

ROOT=$(pwd -P)
FIXTURES="$ROOT/.ufo/waves/round-28/q36/fixtures"
MUTANTS="$ROOT/.ufo/waves/round-28/q36/mutants"
RECEIPTS="$ROOT/quality/q36-successor-receipts.txt"
SCRATCH_ROOT=/fast/scratch/hyaku/mado-r28/ExecQ36Runner
FIXTURE_COMMIT_DATE=2026-10-21T23:59:00Z

: "${MADO_Q36_CHECKER:?set MADO_Q36_CHECKER to the committed Q36 checker}"
[[ -f "$MADO_Q36_CHECKER" ]] || { printf 'missing checker: %s\n' "$MADO_Q36_CHECKER" >&2; exit 2; }

mkdir -p "$SCRATCH_ROOT"
WORK=$(mktemp -d "$SCRATCH_ROOT/run.XXXXXXXX")
trap 'rm -rf -- "$WORK"' EXIT
mkdir -p "$WORK/home"
export HOME="$WORK/home" GIT_CONFIG_NOSYSTEM=1 GIT_OPTIONAL_LOCKS=0
unset GIT_DIR GIT_WORK_TREE GIT_INDEX_FILE GIT_COMMON_DIR GIT_CONFIG_GLOBAL GIT_CONFIG_COUNT GIT_CONFIG_PARAMETERS

: > "$RECEIPTS"
rows=0
failed=0

make_fixture_repo() {
    local name=$1 source="$FIXTURES/$1" repo="$WORK/$1"
    [[ -f "$source/.ufo/waves/round-98/registry.json" ]] || {
        printf 'missing fixture registry: %s\n' "$source" >&2
        return 2
    }
    [[ -d "$source/.ufo/waves/round-98/controls" ]] || {
        printf 'missing fixture controls: %s\n' "$source" >&2
        return 2
    }
    mkdir -p "$repo"
    cp -R "$source/." "$repo/"
    git -C "$repo" init --quiet
    git -C "$repo" add -- .ufo/waves/round-98/registry.json .ufo/waves/round-98/controls
    GIT_AUTHOR_DATE="$FIXTURE_COMMIT_DATE" GIT_COMMITTER_DATE="$FIXTURE_COMMIT_DATE" \
        git -C "$repo" -c user.name='Q36 witness' -c user.email='q36-witness@example.invalid' \
        commit --quiet -m "Q36 fixture: $name"
    git -C "$repo" cat-file -e HEAD:.ufo/waves/round-98/registry.json
    [[ -z "$(git -C "$repo" status --porcelain)" ]] || {
        printf 'fixture repo is not clean: %s\n' "$repo" >&2
        return 2
    }
    printf '%s\n' "$repo"
}

run_checker() {
    local survivor=$1 row=$2 expected=$3 checker=$4 repo=$5 shapes=$6 glob=$7
    local output="$WORK/output-$rows.txt" rc result command_text line
    local -a command=(python3 -I "$checker" --round 98 \
        --data-registry .ufo/waves/round-98/registry.json --repo "$repo" \
        --tip HEAD --shapes "$shapes" --receipt-glob "$glob")
    printf -v command_text '%q ' "${command[@]}"
    command_text=${command_text% }
    if "${command[@]}" > "$output" 2>&1; then
        rc=0
    else
        rc=$?
    fi
    if [[ $rc -eq $expected ]]; then result=PASS; else result=FAIL; failed=$((failed + 1)); fi
    printf '%s %s command=%s rc=%s expected=%s %s\n' \
        "$survivor" "$row" "$command_text" "$rc" "$expected" "$result" >> "$RECEIPTS"
    while IFS= read -r line || [[ -n "$line" ]]; do
        printf '  checker-output: %s\n' "$line" >> "$RECEIPTS"
    done < "$output"
    rows=$((rows + 1))
}

Q2_REPO=$(make_fixture_repo Q2-glob-case-sensitive)
Q2_MUTANT="$MUTANTS/Q2-glob-case-sensitive.py"
[[ -f "$Q2_MUTANT" ]] || { printf 'missing mutant: %s\n' "$Q2_MUTANT" >&2; exit 2; }
# Q2's mutation removes the path lowercasing, so its matching set can only shrink:
# the witness direction is pristine-accepts / mutant-rejects (a lowering-sensitive glob
# over the uppercase fixture names), unlike Q5 where the mutant accepts a wider set.
run_checker Q2-glob-case-sensitive pristine-accepts 0 "$MADO_Q36_CHECKER" "$Q2_REPO" \
    DoNothing,EmptyArray,Junk 'k1*.txt'
run_checker Q2-glob-case-sensitive mutant-rejects 1 "$Q2_MUTANT" "$Q2_REPO" \
    DoNothing,EmptyArray,Junk 'k1*.txt'

Q5_REPO=$(make_fixture_repo Q5-marker-case-insensitive)
Q5_MUTANT="$MUTANTS/Q5-marker-case-insensitive.py"
[[ -f "$Q5_MUTANT" ]] || { printf 'missing mutant: %s\n' "$Q5_MUTANT" >&2; exit 2; }
run_checker Q5-marker-case-insensitive pristine-rejects 1 "$MADO_Q36_CHECKER" "$Q5_REPO" \
    DoNothing,EmptyArray,Junk '*.md'
run_checker Q5-marker-case-insensitive mutant-accepts 0 "$Q5_MUTANT" "$Q5_REPO" \
    DoNothing,EmptyArray,Junk '*.md'

printf 'Q36WITNESS rows=%s failed=%s\n' "$rows" "$failed" >> "$RECEIPTS"
printf 'Q36WITNESS rows=%s failed=%s\n' "$rows" "$failed"
[[ $rows -eq 4 && $failed -eq 0 ]]
