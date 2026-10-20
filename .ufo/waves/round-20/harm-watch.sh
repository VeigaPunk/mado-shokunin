#!/usr/bin/env bash
# =============================================================================
# harm-watch.sh — round-20 harm-watch receipt runner (mado-shokunin)
#
# Every executed command gets one output file whose first line is a RECEIPT
# (tool path and digest, measured commit, UTC time, argv) and whose last line is
# exit=N. Lane tools are executed only after their worktree bytes match git
# show REV:path. Navigation uses the REV-pinned SCORECARD bytes, never an
# unpinned worktree block. The census check validates only the REV clone's
# corpus/SOURCES.md; its external parser is pinned to its own fleet git blob.
#
# Commands (hermetic modes only; never the live gate):
#   tools/mado-verify.sh --selftest and --regression
#   tools/mado-action-plan.py --selftest
#   every direct suite directory with expected.json under
#       .ufo/waves/{round-17,round-18,round-19,round-20}/tripwire
#   tools/mado-tripwire.py --frozen for round-18 (expected mismatch is baseline),
#       and round-19/20 when present
#   .ufo/waves/round-17/measure.py REV
#   .ufo/waves/round-19/tw-recall.py REV
#   .ufo/waves/round-20/tw-precision.py REV when present
#   the SCORECARD counting block extracted from the REV-pinned file
#   sources-census.sh validate --file ROOT/corpus/SOURCES.md
#
# Usage:
#   ROOT=<absolute test checkout> REV=<rev> [OUTDIR=<absolute dir>] bash this-file
#   ROOT=<absolute test checkout> OUTDIR=<absolute dir> bash this-file <rev>
# OUTDIR defaults to /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/
# round-20/evidence/harm. For isolated checks, set ROOT and OUTDIR to /tmp.
# =============================================================================
set -u
export LC_ALL=C

DEFAULT_ROOT=/home/vgpnk/Projects/shokunin/mado-shokunin
FLEET=/home/vgpnk/Projects/shokunin
ROOT="${ROOT:-$DEFAULT_ROOT}"
REV_ARG="${1:-${REV:-}}"
OUTDIR="${OUTDIR:-$DEFAULT_ROOT/.ufo/waves/round-20/evidence/harm}"
TTL="${HARM_TIMEOUT:-1800}"

usage() {
    awk 'NR == 1 { next }
         /^# =+$/ { if (seen++) exit; next }
         { sub(/^# ?/, ""); print }' "${BASH_SOURCE[0]}"
}

case "$REV_ARG" in
    -h|--help) usage; exit 0 ;;
esac
if [ -z "$REV_ARG" ]; then
    printf 'harm-watch: REV is required (arg or $REV)\n' >&2
    usage >&2
    exit 2
fi
case "$ROOT" in /*) ;; *) printf 'harm-watch: ROOT must be absolute: %s\n' "$ROOT" >&2; exit 2 ;; esac
case "$OUTDIR" in /*) ;; *) printf 'harm-watch: OUTDIR must be absolute: %s\n' "$OUTDIR" >&2; exit 2 ;; esac
case "$TTL" in ''|*[!0-9]*) TTL=1800 ;; esac
[ "$TTL" -gt 0 ] || TTL=1800

cd "$ROOT" || { printf 'harm-watch: cannot cd %s\n' "$ROOT" >&2; exit 2; }
REV_SHA=$(git -C "$ROOT" rev-parse --verify --quiet "${REV_ARG}^{commit}") || {
    printf 'harm-watch: cannot resolve revision %s in %s\n' "$REV_ARG" "$ROOT" >&2
    exit 2
}
mkdir -p "$OUTDIR" || { printf 'harm-watch: cannot create %s\n' "$OUTDIR" >&2; exit 2; }
TMPD=$(mktemp -d /tmp/mado-r20-harm-watch.XXXXXX) || exit 2
trap 'rm -rf "$TMPD"' EXIT
TMP_OBJECT="$TMPD/object.bytes"
SUMMARY="$OUTDIR/harm-watch-summary.txt"
PINS="$OUTDIR/harm-watch-pins.txt"
OUT=
FAILS=0
RUNS=0
GROUP=misc
declare -A G_RUN=() G_OK=() G_FAIL=() G_SKIP=() G_BASE=()
: > "$SUMMARY"
printf 'PINS schema=mado-harm-watch-pins-v1 rev=%s utc=%s\n' \
    "$REV_SHA" "$(date -u +%Y-%m-%dT%H:%M:%SZ)" > "$PINS"

receipt_line() { # tool tool_sha256 measured_commit argv...
    local tool=$1 tool_sha=$2 measured=$3 a
    shift 3
    printf 'RECEIPT tool=%s tool_sha256=%s measured_commit=%s utc=%s cwd=%s argv=' \
        "$tool" "$tool_sha" "$measured" "$(date -u +%Y-%m-%dT%H:%M:%SZ)" "$ROOT"
    for a in "$@"; do printf '%q ' "$a"; done
    printf '\n'
}

begin() { # file tool tool_sha measured_commit argv...
    OUT="$OUTDIR/$1"
    shift
    receipt_line "$@" > "$OUT"
}

end_out() { printf 'exit=%s\n' "$1" >> "$OUT"; }

record_result() { # file argv rc
    RUNS=$((RUNS + 1))
    G_RUN[$GROUP]=$(( ${G_RUN[$GROUP]:-0} + 1 ))
    if [ "$3" -eq 0 ]; then
        G_OK[$GROUP]=$(( ${G_OK[$GROUP]:-0} + 1 ))
        printf 'OK\texit=%s\tgroup=%s\t%s\t%s\n' "$3" "$GROUP" "$1" "$2" >> "$SUMMARY"
    else
        G_FAIL[$GROUP]=$(( ${G_FAIL[$GROUP]:-0} + 1 ))
        printf 'FAIL\texit=%s\tgroup=%s\t%s\t%s\n' "$3" "$GROUP" "$1" "$2" >> "$SUMMARY"
        FAILS=$((FAILS + 1))
    fi
}

record_baseline() { # file argv label rc
    RUNS=$((RUNS + 1))
    G_RUN[$GROUP]=$(( ${G_RUN[$GROUP]:-0} + 1 ))
    G_BASE[$GROUP]=$(( ${G_BASE[$GROUP]:-0} + 1 ))
    printf 'BASELINE\texit=%s\tgroup=%s\tlabel=%s\t%s\t%s\n' \
        "$4" "$GROUP" "$3" "$1" "$2" >> "$SUMMARY"
}

skip_result() { # file reason argv
    RUNS=$((RUNS + 1))
    G_RUN[$GROUP]=$(( ${G_RUN[$GROUP]:-0} + 1 ))
    G_SKIP[$GROUP]=$(( ${G_SKIP[$GROUP]:-0} + 1 ))
    printf 'SKIP\t%s\tgroup=%s\t%s\t%s\n' "$2" "$GROUP" "$1" "$3" >> "$SUMMARY"
    FAILS=$((FAILS + 1))
}

note() { printf 'NOTE\t%s\n' "$1" >> "$SUMMARY"; }

# pin_assert REPO PATH COMMIT: worktree and git-show digests are both retained.
pin_assert() {
    local repo=$1 path=$2 commit=$3 line
    PIN_WT=- PIN_REV=- PIN_STATE=ok
    if [ ! -f "$repo/$path" ]; then PIN_STATE=missing_worktree; return 1; fi
    if ! line=$(sha256sum -- "$repo/$path" 2>/dev/null); then PIN_STATE=worktree_hash_failed; return 1; fi
    PIN_WT=${line%% *}
    if ! git -C "$repo" cat-file -e "$commit:$path" 2>/dev/null; then
        PIN_STATE=missing_at_rev
        return 1
    fi
    if git -C "$repo" show "$commit:$path" > "$TMP_OBJECT" 2>/dev/null; then
        if ! line=$(sha256sum -- "$TMP_OBJECT" 2>/dev/null); then PIN_STATE=rev_hash_failed; return 1; fi
        PIN_REV=${line%% *}
    else
        PIN_STATE=rev_read_failed
        return 1
    fi
    if [ "$PIN_WT" != "$PIN_REV" ]; then PIN_STATE=mismatch; return 1; fi
    return 0
}

pin_log() { # repo path commit
    printf 'PIN\t%s/%s\t%s\tworktree=%s\trev=%s\tstate=%s\n' \
        "$1" "$2" "$3" "$PIN_WT" "$PIN_REV" "$PIN_STATE" >> "$PINS"
}

pin_skip() { # file tool measured_commit reason argv...
    local file=$1 tool=$2 measured=$3 reason=$4
    shift 4
    begin "$file" "$tool" "$PIN_WT" "$measured" "$@"
    printf 'pin_assert=%s worktree_sha256=%s expected_rev_sha256=%s\n' \
        "$reason" "$PIN_WT" "$PIN_REV" >> "$OUT"
    printf 'status=skipped:pin_mismatch\n' >> "$OUT"
    end_out 2
    skip_result "$file" "$reason" "$*"
}

# run_pinned FILE TOOL_REL SUMMARY_ARGV CMD...
run_pinned() {
    local file=$1 rel=$2 argvstr=$3 rc
    shift 3
    if pin_assert "$ROOT" "$rel" "$REV_SHA"; then
        pin_log "$ROOT" "$rel" "$REV_SHA"
        begin "$file" "$ROOT/$rel" "$PIN_WT" "$REV_SHA" "$@"
        timeout "$TTL" "$@" >> "$OUT" 2>&1
        rc=$?
        end_out "$rc"
        record_result "$file" "$argvstr" "$rc"
    else
        pin_log "$ROOT" "$rel" "$REV_SHA"
        pin_skip "$file" "$ROOT/$rel" "$REV_SHA" "$PIN_STATE" "$@"
    fi
}

read_assignment() { # variable path; parse a literal KEY='value' line without sourcing
    local key=$1 path=$2 line value
    while IFS= read -r line || [ -n "$line" ]; do
        case "$line" in
            "$key"=*)
                value=${line#*=}
                value=${value#\'}
                value=${value%\'}
                printf '%s' "$value"
                return 0
                ;;
        esac
    done < "$path"
    return 1
}

# Use only the regression helper blob whose digest is declared by the pinned
# gate. This avoids depending on a moved tameshi worktree during clone replay.
prepare_regression_harness() {
    local gate=$ROOT/tools/mado-verify.sh expected worktree line candidate digest
    local repo=$FLEET/tameshi-shokunin rel=tools/mutate-and-run.sh
    expected=$(read_assignment HARNESS_SHA_RECORDED "$gate") || return 1
    case "$expected" in *[!0-9a-f]*|'') return 1 ;; esac
    [ "${#expected}" -eq 64 ] || return 1
    worktree=-
    if [ -f "$repo/$rel" ] && line=$(sha256sum -- "$repo/$rel" 2>/dev/null); then
        worktree=${line%% *}
    fi
    if ! git -C "$repo" rev-list --all -- "$rel" > "$TMPD/harness-revisions" 2>/dev/null; then
        printf 'REGRESSION_HARNESS source=%s worktree_sha256=%s recorded_sha256=%s state=history_unavailable\n' \
            "$repo/$rel" "$worktree" "$expected" >> "$PINS"
        return 1
    fi
    REG_HARNESS_REV=
    REG_HARNESS_SHA=$expected
    REG_HARNESS_COPY="$TMPD/mutate-and-run.sh"
    while IFS= read -r candidate; do
        [ -n "$candidate" ] || continue
        if git -C "$repo" show "$candidate:$rel" > "$TMPD/harness-candidate" 2>/dev/null && \
           line=$(sha256sum -- "$TMPD/harness-candidate" 2>/dev/null); then
            digest=${line%% *}
            if [ "$digest" = "$expected" ]; then
                if cp -- "$TMPD/harness-candidate" "$REG_HARNESS_COPY"; then
                    REG_HARNESS_REV=$candidate
                    break
                fi
            fi
        fi
    done < "$TMPD/harness-revisions"
    if [ -z "$REG_HARNESS_REV" ]; then
        printf 'REGRESSION_HARNESS source=%s worktree_sha256=%s recorded_sha256=%s state=recorded_blob_not_found\n' \
            "$repo/$rel" "$worktree" "$expected" >> "$PINS"
        return 1
    fi
    if ! line=$(sha256sum -- "$REG_HARNESS_COPY" 2>/dev/null) || [ "${line%% *}" != "$expected" ]; then
        printf 'REGRESSION_HARNESS source=%s commit=%s worktree_sha256=%s recorded_sha256=%s state=copy_mismatch\n' \
            "$repo/$rel" "$REG_HARNESS_REV" "$worktree" "$expected" >> "$PINS"
        return 1
    fi
    printf 'REGRESSION_HARNESS\t%s\t%s\tworktree=%s\trev=%s\tstate=recorded_blob_copied\n' \
        "$repo/$rel" "$REG_HARNESS_REV" "$worktree" "$expected" >> "$PINS"
    note "gate regression helper pinned to tameshi $REG_HARNESS_REV sha256=$expected (current worktree=$worktree)"
    return 0
}

# --------------------------------------------------------------- gate modes
GROUP=gate
run_pinned harm-gate-selftest.txt tools/mado-verify.sh \
    "bash $ROOT/tools/mado-verify.sh --selftest" \
    bash "$ROOT/tools/mado-verify.sh" --selftest

run_gate_regression() {
    local file=harm-gate-regression.txt argvstr rc
    GROUP=gate
    if ! pin_assert "$ROOT" tools/mado-verify.sh "$REV_SHA"; then
        pin_log "$ROOT" tools/mado-verify.sh "$REV_SHA"
        pin_skip "$file" "$ROOT/tools/mado-verify.sh" "$REV_SHA" "$PIN_STATE" \
            env MADO_VERIFY_HARNESS=UNAVAILABLE bash "$ROOT/tools/mado-verify.sh" --regression
        return
    fi
    pin_log "$ROOT" tools/mado-verify.sh "$REV_SHA"
    argvstr="env MADO_VERIFY_HARNESS=$TMPD/mutate-and-run.sh bash $ROOT/tools/mado-verify.sh --regression"
    if ! prepare_regression_harness; then
        begin "$file" "$ROOT/tools/mado-verify.sh" "$PIN_WT" "$REV_SHA" \
            env "MADO_VERIFY_HARNESS=$TMPD/mutate-and-run.sh" bash "$ROOT/tools/mado-verify.sh" --regression
        printf 'status=skipped:recorded regression harness blob unavailable\n' >> "$OUT"
        end_out 2
        skip_result "$file" recorded_regression_harness_unavailable "$argvstr"
        return
    fi
    begin "$file" "$ROOT/tools/mado-verify.sh" "$PIN_WT" "$REV_SHA" \
        env "MADO_VERIFY_HARNESS=$REG_HARNESS_COPY" bash "$ROOT/tools/mado-verify.sh" --regression
    printf 'regression_harness_sha256=%s regression_harness_commit=%s\n' \
        "$REG_HARNESS_SHA" "$REG_HARNESS_REV" >> "$OUT"
    timeout "$TTL" env "MADO_VERIFY_HARNESS=$REG_HARNESS_COPY" \
        bash "$ROOT/tools/mado-verify.sh" --regression >> "$OUT" 2>&1
    rc=$?
    end_out "$rc"
    record_result "$file" "$argvstr" "$rc"
}
run_gate_regression

GROUP=classifier
run_pinned harm-action-plan-selftest.txt tools/mado-action-plan.py \
    "python3 -I $ROOT/tools/mado-action-plan.py --selftest" \
    python3 -I "$ROOT/tools/mado-action-plan.py" --selftest

# -------------------------------------------------------------- tripwire suites
SUITE_COUNT=0
for base in round-17 round-18 round-19 round-20; do
    twroot="$ROOT/.ufo/waves/$base/tripwire"
    if [ ! -d "$twroot" ]; then
        note "tripwire root absent: .ufo/waves/$base/tripwire"
        continue
    fi
    found=0
    for d in "$twroot"/*/; do
        [ -d "$d" ] || continue
        name=${d%/}
        name=${name##*/}
        if [ ! -f "$d/expected.json" ]; then
            note "tripwire dir without expected.json: .ufo/waves/$base/tripwire/$name"
            continue
        fi
        found=$((found + 1))
        SUITE_COUNT=$((SUITE_COUNT + 1))
        rel=".ufo/waves/$base/tripwire/$name"
        file="harm-tripwire-$base-$name.txt"
        argvstr="python3 -I $ROOT/tools/mado-tripwire.py --selftest $ROOT/$rel"
        GROUP=tripwire-selftest
        run_pinned "$file" tools/mado-tripwire.py "$argvstr" \
            python3 -I "$ROOT/tools/mado-tripwire.py" --selftest "$ROOT/$rel"
    done
    [ "$found" -gt 0 ] || note "tripwire root has no direct suites with expected.json: .ufo/waves/$base/tripwire"
done
[ "$SUITE_COUNT" -gt 0 ] || note 'no tripwire suites with expected.json were found'

# ------------------------------------ round-18 frozen baseline (expected mismatch)
run_round18_frozen() {
    local file=harm-tripwire-frozen-round-18.txt rel=.ufo/waves/round-18/frozen
    local argvstr="python3 -I $ROOT/tools/mado-tripwire.py --frozen $ROOT/$rel" rc label
    GROUP=tripwire-frozen
    if pin_assert "$ROOT" tools/mado-tripwire.py "$REV_SHA"; then
        pin_log "$ROOT" tools/mado-tripwire.py "$REV_SHA"
        begin "$file" "$ROOT/tools/mado-tripwire.py" "$PIN_WT" "$REV_SHA" \
            python3 -I "$ROOT/tools/mado-tripwire.py" --frozen "$ROOT/$rel"
        timeout "$TTL" python3 -I "$ROOT/tools/mado-tripwire.py" --frozen "$ROOT/$rel" >> "$OUT" 2>&1
        rc=$?
        label=$(awk 'NR == 2 { print; exit }' "$OUT")
        printf 'round18_expected=MADO_TRIPWIRE_FROZEN: frozen_verdict_mismatch observed=%s\n' "$label" >> "$OUT"
        end_out "$rc"
        case "$rc:$label" in
            '0:MADO_TRIPWIRE_FROZEN: frozen_match'|'1:MADO_TRIPWIRE_FROZEN: frozen_verdict_mismatch')
                record_baseline "$file" "$argvstr" "$label" "$rc"
                ;;
            *) record_result "$file" "$argvstr" "$rc" ;;
        esac
    else
        pin_log "$ROOT" tools/mado-tripwire.py "$REV_SHA"
        pin_skip "$file" "$ROOT/tools/mado-tripwire.py" "$REV_SHA" "$PIN_STATE" \
            python3 -I "$ROOT/tools/mado-tripwire.py" --frozen "$ROOT/$rel"
    fi
}
run_round18_frozen

for base in round-19 round-20; do
    frozen="$ROOT/.ufo/waves/$base/frozen"
    if [ -d "$frozen" ]; then
        GROUP=tripwire-frozen
        run_pinned "harm-tripwire-frozen-$base.txt" tools/mado-tripwire.py \
            "python3 -I $ROOT/tools/mado-tripwire.py --frozen $frozen" \
            python3 -I "$ROOT/tools/mado-tripwire.py" --frozen "$frozen"
    else
        note "$base frozen baseline absent, not replayed: $frozen"
    fi
done

# --------------------------------------------------------- measurement probes
GROUP=measure-round-17
if [ -f "$ROOT/.ufo/waves/round-17/measure.py" ]; then
    run_pinned harm-measure-round-17.txt .ufo/waves/round-17/measure.py \
        "python3 $ROOT/.ufo/waves/round-17/measure.py $REV_SHA" \
        python3 "$ROOT/.ufo/waves/round-17/measure.py" "$REV_SHA"
else
    note 'round-17 measure.py absent, not run'
fi

GROUP=tw-recall
if [ -f "$ROOT/.ufo/waves/round-19/tw-recall.py" ]; then
    run_pinned harm-tw-recall.txt .ufo/waves/round-19/tw-recall.py \
        "python3 -I $ROOT/.ufo/waves/round-19/tw-recall.py $REV_SHA" \
        python3 -I "$ROOT/.ufo/waves/round-19/tw-recall.py" "$REV_SHA"
else
    note 'round-19 tw-recall.py absent, not run'
fi

GROUP=tw-precision
if [ -f "$ROOT/.ufo/waves/round-20/tw-precision.py" ]; then
    run_pinned harm-tw-precision.txt .ufo/waves/round-20/tw-precision.py \
        "python3 -I $ROOT/.ufo/waves/round-20/tw-precision.py $REV_SHA" \
        python3 -I "$ROOT/.ufo/waves/round-20/tw-precision.py" "$REV_SHA"
else
    note 'round-20 tw-precision.py absent, not run'
fi

# ----------------------------------------- navigation from pinned SCORECARD.md
run_navigation() {
    local file=harm-nav-fleet-round-1.txt src="$ROOT/SCORECARD.md"
    local block="$TMPD/nav-block.sh" argvstr rc block_sha
    GROUP=navigation
    if ! pin_assert "$ROOT" SCORECARD.md "$REV_SHA"; then
        pin_log "$ROOT" SCORECARD.md "$REV_SHA"
        pin_skip "$file" "$src#Counting-command" "$REV_SHA" "$PIN_STATE" \
            bash -s '<' "$src##Counting-command"
        return
    fi
    pin_log "$ROOT" SCORECARD.md "$REV_SHA"
    if ! cp -- "$TMP_OBJECT" "$TMPD/SCORECARD.rev.md"; then
        PIN_WT=$PIN_REV; PIN_STATE=revision_copy_failed
        begin "$file" "$src#Counting-command" - "$REV_SHA" bash -s '<' "$src##Counting-command"
        printf 'status=tool_error reason=revision_copy_failed\n' >> "$OUT"
        end_out 2
        record_result "$file" "bash -s < $src#Counting-command (REV=$REV_SHA)" 2
        return
    fi
    awk '
        /^### Counting command/ { want = 1; next }
        want && /^```bash/ { inblock = 1; next }
        inblock && /^```/ { exit }
        inblock { print }
    ' "$TMPD/SCORECARD.rev.md" > "$block"
    if [ ! -s "$block" ]; then
        begin "$file" "$src#Counting-command" - "$REV_SHA" bash -s '<' "$src##Counting-command"
        printf 'status=tool_error reason=counting_block_not_found_in_REV_SCORECARD\n' >> "$OUT"
        end_out 2
        record_result "$file" "bash -s < $src#Counting-command (REV=$REV_SHA)" 2
        return
    fi
    local line
    if ! line=$(sha256sum -- "$block" 2>/dev/null); then
        block_sha=-
    else
        block_sha=${line%% *}
    fi
    argvstr="REV=$REV_SHA bash -s < $src#Counting-command"
    begin "$file" "$src#Counting-command" "$block_sha" "$REV_SHA" \
        REV="$REV_SHA" bash -s '<' "$src##Counting-command"
    printf 'scorecard_sha256=%s block_sha256=%s source=git-show-REV-only\n' \
        "$PIN_WT" "$block_sha" >> "$OUT"
    REV="$REV_SHA" timeout "$TTL" bash -s < "$block" >> "$OUT" 2>&1
    rc=$?
    end_out "$rc"
    record_result "$file" "$argvstr" "$rc"
}
run_navigation

# --------------------------------------------------------------- corpus census
run_census() {
    local file=harm-census-validate.txt source="$FLEET/scripts/sources-census.sh"
    local fleet_head line copy="$TMPD/sources-census.sh" argvstr rc
    GROUP=census
    if ! fleet_head=$(git -C "$FLEET" rev-parse --verify HEAD 2>/dev/null); then
        PIN_WT=- PIN_REV=- PIN_STATE=fleet_rev_unresolved
        pin_log "$FLEET" scripts/sources-census.sh unknown
        pin_skip "$file" "$source" "$REV_SHA" "$PIN_STATE" \
            bash "$copy" validate --file "$ROOT/corpus/SOURCES.md"
        return
    fi
    if ! pin_assert "$FLEET" scripts/sources-census.sh "$fleet_head"; then
        pin_log "$FLEET" scripts/sources-census.sh "fleet:$fleet_head"
        pin_skip "$file" "$source" "$REV_SHA" "$PIN_STATE" \
            bash "$copy" validate --file "$ROOT/corpus/SOURCES.md"
        return
    fi
    pin_log "$FLEET" scripts/sources-census.sh "fleet:$fleet_head"
    if ! cp -- "$source" "$copy" || ! line=$(sha256sum -- "$copy" 2>/dev/null) || \
       [ "${line%% *}" != "$PIN_REV" ]; then
        PIN_STATE=copy_mismatch
        begin "$file" "$copy" "$PIN_WT" "$REV_SHA" bash "$copy" validate --file "$ROOT/corpus/SOURCES.md"
        printf 'status=skipped:census_copy_mismatch source_commit=%s expected_sha256=%s\n' \
            "$fleet_head" "$PIN_REV" >> "$OUT"
        end_out 2
        skip_result "$file" census_copy_mismatch "bash $copy validate --file $ROOT/corpus/SOURCES.md"
        return
    fi
    argvstr="bash $copy validate --file $ROOT/corpus/SOURCES.md"
    begin "$file" "$copy" "$PIN_REV" "$REV_SHA" \
        bash "$copy" validate --file "$ROOT/corpus/SOURCES.md"
    printf 'source_tool=%s source_commit=%s input=%s/corpus/SOURCES.md\n' \
        "$source" "$fleet_head" "$ROOT" >> "$OUT"
    timeout "$TTL" bash "$copy" validate --file "$ROOT/corpus/SOURCES.md" >> "$OUT" 2>&1
    rc=$?
    end_out "$rc"
    record_result "$file" "$argvstr" "$rc"
}
run_census

# ---------------------------------------------------------------------- tallies
TOT_OK=0 TOT_FAIL=0 TOT_SKIP=0 TOT_BASE=0
GROUP_LIST=$(printf '%s\n' "${!G_RUN[@]}" | sort)
for g in $GROUP_LIST; do
    TOT_OK=$((TOT_OK + ${G_OK[$g]:-0}))
    TOT_FAIL=$((TOT_FAIL + ${G_FAIL[$g]:-0}))
    TOT_SKIP=$((TOT_SKIP + ${G_SKIP[$g]:-0}))
    TOT_BASE=$((TOT_BASE + ${G_BASE[$g]:-0}))
done
printf 'TALLY\ttotal\truns=%s\tok=%s\tfail=%s\tskip=%s\tbaseline=%s\tblocking=%s\n' \
    "$RUNS" "$TOT_OK" "$TOT_FAIL" "$TOT_SKIP" "$TOT_BASE" "$FAILS" >> "$SUMMARY"
for g in $GROUP_LIST; do
    printf 'TALLY\t%s\truns=%s\tok=%s\tfail=%s\tskip=%s\tbaseline=%s\n' \
        "$g" "${G_RUN[$g]:-0}" "${G_OK[$g]:-0}" "${G_FAIL[$g]:-0}" \
        "${G_SKIP[$g]:-0}" "${G_BASE[$g]:-0}" >> "$SUMMARY"
done

if [ "$FAILS" -eq 0 ]; then verdict=PASS; status=0; else verdict="FAIL failures=$FAILS"; status=1; fi
{
    printf 'HARM_WATCH: %s\n' "$verdict"
    printf 'rev=%s outdir=%s commands=%s failures=%s pins=%s\n' \
        "$REV_SHA" "$OUTDIR" "$RUNS" "$FAILS" "$PINS"
} >> "$SUMMARY"
printf 'HARM_WATCH: %s\n' "$verdict"
exit "$status"
