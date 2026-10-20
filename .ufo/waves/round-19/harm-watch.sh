#!/usr/bin/env bash
# =============================================================================
# harm-watch.sh — round-19 harm-watch receipt runner (mado-shokunin)
#
# Every harm-watch command runs under one file in OUTDIR whose FIRST line is a
# RECEIPT:
#
#   RECEIPT tool=<path> tool_sha256=<hex> measured_commit=<rev-sha> utc=<iso-Z> \
#           cwd=<lane-root> argv=<shell-quoted words>
#
# The receipt is only written with measured_commit=<REV> after asserting that
# the worktree tool bytes equal REV's bytes (git cat-file -e + git show into a
# temp file; a failed read is never turned into the empty-input digest). When
# the assertion fails the file records measured_commit=UNVERIFIED plus the two
# digests and the command is skipped — the aggregate run exits 1.
#
# Commands (never the live gate):
#   bash tools/mado-verify.sh --selftest
#   bash tools/mado-verify.sh --regression
#   python3 -I tools/mado-action-plan.py --selftest
#   python3 -I tools/mado-tripwire.py --selftest <suite>
#       for each dir with expected.json under
#       .ufo/waves/{round-17,round-18,round-19}/tripwire
#   python3 -I tools/mado-tripwire.py --frozen .ufo/waves/round-18/frozen
#       round 19 EXPECTS frozen_verdict_mismatch here once the recall misses
#       are fixed: the label is recorded as a baseline observation and this
#       command never contributes to the failure count. frozen_error,
#       snapshot_tampered, unpinned_legacy or a missing label still fail.
#   python3 -I tools/mado-tripwire.py --frozen .ufo/waves/round-19/frozen
#       only when that directory exists; a fresh round-19 pin must reproduce
#       (normal failure semantics).
#   python3 .ufo/waves/round-16/measure.py REV
#   python3 .ufo/waves/round-17/measure.py REV
#   python3 -I .ufo/waves/round-19/tw-recall.py REV
#   python3 -I .ufo/waves/round-19/fresh-pins.py REV
#   the SCORECARD "### Counting command" block read from the worktree
#       SCORECARD.md, run via bash -s with REV exported
#   /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate \
#       --root /home/vgpnk/Projects/shokunin mado
#
# Usage:
#   REV=<rev> [OUTDIR=<dir>] bash .ufo/waves/round-19/harm-watch.sh
#   bash .ufo/waves/round-19/harm-watch.sh <rev>
#
# OUTDIR defaults to .ufo/waves/round-19/evidence/harm. Each command overwrites
# its own named file; harm-watch-summary.txt and harm-watch-pins.txt are
# rewritten. Exit: 0 every executed command exited 0 (the round-18 frozen
# mismatch aside) and every pin asserted; 1 otherwise; 2 usage/revision error.
# =============================================================================
set -u

ROOT=/home/vgpnk/Projects/shokunin/mado-shokunin
FLEET=/home/vgpnk/Projects/shokunin
REV_ARG="${1:-${REV:-}}"
OUTDIR="${OUTDIR:-$ROOT/.ufo/waves/round-19/evidence/harm}"
TTL="${HARM_TIMEOUT:-1800}"

usage() {
    awk 'NR == 1 { next }
         /^# =+$/ { if (seen++) exit; next }
         { sub(/^# ?/, ""); print }' "${BASH_SOURCE[0]}"
}

case "${REV_ARG}" in
    -h|--help) usage; exit 0 ;;
esac

if [ -z "${REV_ARG}" ]; then
    printf 'harm-watch: REV is required (arg or $REV)\n' >&2
    usage >&2
    exit 2
fi
case "${TTL}" in
    ''|*[!0-9]*) TTL=1800 ;;
esac

cd "$ROOT" || { printf 'harm-watch: cannot cd %s\n' "$ROOT" >&2; exit 2; }

REV_SHA=$(git -C "$ROOT" rev-parse --verify --quiet "${REV_ARG}^{commit}") || {
    printf 'harm-watch: cannot resolve revision %s in %s\n' "$REV_ARG" "$ROOT" >&2
    exit 2
}

mkdir -p "$OUTDIR" || { printf 'harm-watch: cannot create %s\n' "$OUTDIR" >&2; exit 2; }

TMPD=$(mktemp -d /tmp/mado-harm-watch.XXXXXX) || exit 2
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
{
    printf 'PINS schema=mado-harm-watch-pins-v1 rev=%s utc=%s\n' \
        "$REV_SHA" "$(date -u +%Y-%m-%dT%H:%M:%SZ)"
} > "$PINS"

receipt_line() { # tool tool_sha256 commit argv...
    local tool=$1 tsha=$2 commit=$3 a
    shift 3
    printf 'RECEIPT tool=%s tool_sha256=%s measured_commit=%s utc=%s cwd=%s argv=' \
        "$tool" "$tsha" "$commit" "$(date -u +%Y-%m-%dT%H:%M:%SZ)" "$ROOT"
    for a in "$@"; do printf '%q ' "$a"; done
    printf '\n'
}

begin() { # file tool tsha commit argv...
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

# pin_assert REPO PATH COMMIT
#   Sets PIN_WT (worktree digest), PIN_REV (REV digest), PIN_STATE
#   (ok|missing_worktree|missing_at_rev|mismatch|rev_read_failed).
pin_assert() {
    local repo=$1 path=$2 commit=$3
    PIN_WT=- PIN_REV=- PIN_STATE=ok
    if [ ! -f "$repo/$path" ]; then
        PIN_STATE=missing_worktree
        return 1
    fi
    PIN_WT=$(sha256sum "$repo/$path" | cut -d' ' -f1)
    if ! git -C "$repo" cat-file -e "$commit:$path" 2>/dev/null; then
        PIN_STATE=missing_at_rev
        return 1
    fi
    if git -C "$repo" show "$commit:$path" > "$TMP_OBJECT" 2>/dev/null; then
        PIN_REV=$(sha256sum "$TMP_OBJECT" | cut -d' ' -f1)
    else
        PIN_STATE=rev_read_failed
        return 1
    fi
    if [ "$PIN_WT" != "$PIN_REV" ]; then
        PIN_STATE=mismatch
        return 1
    fi
    return 0
}

pin_log() { # repo path commit
    printf 'PIN\t%s\t%s\tworktree=%s\trev=%s\tstate=%s\n' \
        "$2" "$3" "$PIN_WT" "$PIN_REV" "$PIN_STATE" >> "$PINS"
}

pin_skip() { # file tool commit reason argv...
    local file=$1 tool=$2 commit=$3 reason=$4
    shift 4
    begin "$file" "$tool" "$PIN_WT" "$commit" "$@"
    {
        printf 'pin_assert=%s worktree_sha256=%s rev_sha256=%s\n' \
            "$reason" "$PIN_WT" "$PIN_REV"
        printf 'status=skipped:pin_mismatch\n'
    } >> "$OUT"
    end_out skipped
    skip_result "$file" "$reason" "$*"
}

# run_pinned FILE TOOL_REL ARGV_STRING CMD...
#   Pins the worktree tool bytes against REV, then runs CMD with cwd=$ROOT.
#   A pin failure writes a skip receipt and counts as a failure.
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
        pin_skip "$file" "$ROOT/$rel" UNVERIFIED "$PIN_STATE" "$@"
    fi
}

# ------------------------------------------------------- 1. gate selftest
GROUP=gate
run_pinned harm-gate-selftest.txt tools/mado-verify.sh \
    "bash $ROOT/tools/mado-verify.sh --selftest" \
    bash "$ROOT/tools/mado-verify.sh" --selftest

# ----------------------------------------------------- 2. gate regression
GROUP=gate
run_pinned harm-gate-regression.txt tools/mado-verify.sh \
    "bash $ROOT/tools/mado-verify.sh --regression" \
    bash "$ROOT/tools/mado-verify.sh" --regression

# -------------------------------------------------- 3. action-plan selftest
GROUP=action-plan
run_pinned harm-action-plan-selftest.txt tools/mado-action-plan.py \
    "python3 -I $ROOT/tools/mado-action-plan.py --selftest" \
    python3 -I "$ROOT/tools/mado-action-plan.py" --selftest

# ------------------------------------------------------- 4. tripwire suites
GROUP=tripwire-selftest
list_suites() {
    SUITE_REL=() SUITE_FILE=() SUITE_ARGV=()
    local base twroot d name n
    for base in round-17 round-18 round-19; do
        twroot="$ROOT/.ufo/waves/$base/tripwire"
        if [ ! -d "$twroot" ]; then
            note "tripwire root absent: $twroot"
            continue
        fi
        n=0
        for d in "$twroot"/*/; do
            [ -d "$d" ] || continue
            name=$(basename "${d%/}")
            if [ ! -f "$twroot/$name/expected.json" ]; then
                note "tripwire dir without expected.json: .ufo/waves/$base/tripwire/$name"
                continue
            fi
            SUITE_REL+=(".ufo/waves/$base/tripwire/$name")
            SUITE_FILE+=("harm-tripwire-$base-$name.txt")
            SUITE_ARGV+=("python3 -I $ROOT/tools/mado-tripwire.py --selftest $ROOT/.ufo/waves/$base/tripwire/$name")
            n=$((n + 1))
        done
        if [ "$n" -eq 0 ]; then
            note "tripwire root has no suite dirs: $twroot"
        fi
    done
}

list_suites
iw=0
if pin_assert "$ROOT" tools/mado-tripwire.py "$REV_SHA"; then
    pin_log "$ROOT" tools/mado-tripwire.py "$REV_SHA"
    TRIPWIRE_SHA=$PIN_WT
    while [ "$iw" -lt "${#SUITE_REL[@]}" ]; do
        rel=${SUITE_REL[$iw]}
        file=${SUITE_FILE[$iw]}
        argv=${SUITE_ARGV[$iw]}
        begin "$file" "$ROOT/tools/mado-tripwire.py" "$TRIPWIRE_SHA" "$REV_SHA" \
            python3 -I "$ROOT/tools/mado-tripwire.py" --selftest "$ROOT/$rel"
        timeout "$TTL" python3 -I "$ROOT/tools/mado-tripwire.py" --selftest "$ROOT/$rel" >> "$OUT" 2>&1
        rc=$?
        end_out "$rc"
        record_result "$file" "$argv" "$rc"
        iw=$((iw + 1))
    done
else
    pin_log "$ROOT" tools/mado-tripwire.py "$REV_SHA"
    while [ "$iw" -lt "${#SUITE_REL[@]}" ]; do
        pin_skip "${SUITE_FILE[$iw]}" "$ROOT/tools/mado-tripwire.py" UNVERIFIED "$PIN_STATE" \
            python3 -I "$ROOT/tools/mado-tripwire.py" --selftest "$ROOT/${SUITE_REL[$iw]}"
        iw=$((iw + 1))
    done
    if [ "${#SUITE_REL[@]}" -eq 0 ]; then
        # No suites to carry the skip; the pin failure itself is the finding.
        pin_skip harm-tripwire-pin.txt "$ROOT/tools/mado-tripwire.py" UNVERIFIED "$PIN_STATE" \
            python3 -I "$ROOT/tools/mado-tripwire.py" --selftest
    fi
fi

# -------------------------------------- 5. round-18 frozen baseline replay
# A mismatch is the declared round-19 expectation once the recall misses are
# fixed; it is recorded, never failed. Only a replay that could not produce a
# pinned verdict (frozen_error / snapshot_tampered / unpinned_legacy / no
# label at all / timeout) counts as a failure here.
GROUP=tripwire-frozen
FROZEN18="$ROOT/.ufo/waves/round-18/frozen"
if pin_assert "$ROOT" tools/mado-tripwire.py "$REV_SHA"; then
    pin_log "$ROOT" tools/mado-tripwire.py "$REV_SHA"
    begin harm-tripwire-frozen-round-18.txt "$ROOT/tools/mado-tripwire.py" "$PIN_WT" "$REV_SHA" \
        python3 -I "$ROOT/tools/mado-tripwire.py" --frozen "$FROZEN18"
    timeout "$TTL" python3 -I "$ROOT/tools/mado-tripwire.py" --frozen "$FROZEN18" >> "$OUT" 2>&1
    rc=$?
    end_out "$rc"
    LABEL=$(sed -n '2p' "$OUT")
    case "$rc:$LABEL" in
        '0:MADO_TRIPWIRE_FROZEN: frozen_match'|'1:MADO_TRIPWIRE_FROZEN: frozen_verdict_mismatch')
            printf 'round19_expectation=frozen_verdict_mismatch (a match is also a recorded observation)\n' >> "$OUT"
            record_baseline harm-tripwire-frozen-round-18.txt \
                "python3 -I $ROOT/tools/mado-tripwire.py --frozen $FROZEN18" "$LABEL" "$rc"
            ;;
        *)
            record_result harm-tripwire-frozen-round-18.txt \
                "python3 -I $ROOT/tools/mado-tripwire.py --frozen $FROZEN18" "$rc"
            ;;
    esac
else
    pin_log "$ROOT" tools/mado-tripwire.py "$REV_SHA"
    pin_skip harm-tripwire-frozen-round-18.txt "$ROOT/tools/mado-tripwire.py" UNVERIFIED "$PIN_STATE" \
        python3 -I "$ROOT/tools/mado-tripwire.py" --frozen "$FROZEN18"
fi

# ------------------------------------ 6. round-19 frozen baseline (if present)
FROZEN19="$ROOT/.ufo/waves/round-19/frozen"
if [ -d "$FROZEN19" ]; then
    GROUP=tripwire-frozen
    run_pinned harm-tripwire-frozen-round-19.txt tools/mado-tripwire.py \
        "python3 -I $ROOT/tools/mado-tripwire.py --frozen $FROZEN19" \
        python3 -I "$ROOT/tools/mado-tripwire.py" --frozen "$FROZEN19"
else
    note "round-19 frozen baseline absent, not replayed: $FROZEN19"
fi

# ---------------------------------------------------------- 7. measure U 7/7
GROUP=measure-r16
run_pinned harm-measure-u.txt .ufo/waves/round-16/measure.py \
    "python3 $ROOT/.ufo/waves/round-16/measure.py $REV_SHA" \
    python3 "$ROOT/.ufo/waves/round-16/measure.py" "$REV_SHA"

# ------------------------------------------------ 8. round-17 rubric counter
GROUP=measure-r17
run_pinned harm-measure-r17.txt .ufo/waves/round-17/measure.py \
    "python3 $ROOT/.ufo/waves/round-17/measure.py $REV_SHA" \
    python3 "$ROOT/.ufo/waves/round-17/measure.py" "$REV_SHA"

# ------------------------------------------------- 9. round-19 tw recall C3
GROUP=tw-recall
run_pinned harm-tw-recall.txt .ufo/waves/round-19/tw-recall.py \
    "python3 -I $ROOT/.ufo/waves/round-19/tw-recall.py $REV_SHA" \
    python3 -I "$ROOT/.ufo/waves/round-19/tw-recall.py" "$REV_SHA"

# ------------------------------------------------ 10. round-19 fresh pins C2
GROUP=fresh-pins
run_pinned harm-fresh-pins.txt .ufo/waves/round-19/fresh-pins.py \
    "python3 -I $ROOT/.ufo/waves/round-19/fresh-pins.py $REV_SHA" \
    python3 -I "$ROOT/.ufo/waves/round-19/fresh-pins.py" "$REV_SHA"

# ------------------------------------- 11. fleet-round-1 navigation counting
GROUP=navigation
NAV_BLOCK="$TMPD/nav-block.sh"
NAV_SRC="$ROOT/SCORECARD.md"
if [ -f "$NAV_SRC" ]; then
    awk '
        /^### Counting command/ { want = 1; next }
        want && /^```bash/ { inblock = 1; next }
        inblock && /^```/ { exit }
        inblock { print }
    ' "$NAV_SRC" > "$NAV_BLOCK"
    if [ -s "$NAV_BLOCK" ]; then
        BLOCK_SHA=$(sha256sum "$NAV_BLOCK" | cut -d' ' -f1)
        SCARD_WT=$(sha256sum "$NAV_SRC" | cut -d' ' -f1)
        if git -C "$ROOT" show "$REV_SHA:SCORECARD.md" > "$TMP_OBJECT" 2>/dev/null; then
            SCARD_REV=$(sha256sum "$TMP_OBJECT" | cut -d' ' -f1)
            SCARD_STATE=ok
            [ "$SCARD_WT" = "$SCARD_REV" ] || SCARD_STATE=mismatch
        else
            SCARD_REV=- SCARD_STATE=rev_read_failed
        fi
        printf 'PIN\tSCORECARD.md#Counting-command\t%s\tworktree=%s\trev=%s\tstate=%s\tblock=%s\n' \
            "$REV_SHA" "$SCARD_WT" "$SCARD_REV" "$SCARD_STATE" "$BLOCK_SHA" >> "$PINS"
        if [ "$SCARD_STATE" != ok ]; then
            note "SCORECARD.md worktree differs from REV ($SCARD_STATE); counting block read from worktree"
        fi
        begin harm-nav-fleet-round-1.txt "$NAV_SRC#Counting-command" \
            "$BLOCK_SHA" "$REV_SHA" bash -s "<" "$NAV_SRC##Counting-command"
        printf 'scorecard_sha256=%s scorecard_state=%s block_sha256=%s\n' \
            "$SCARD_WT" "$SCARD_STATE" "$BLOCK_SHA" >> "$OUT"
        REV="$REV_SHA" timeout "$TTL" bash -s < "$NAV_BLOCK" >> "$OUT" 2>&1
        rc=$?
        end_out "$rc"
        record_result harm-nav-fleet-round-1.txt \
            "bash -s < $NAV_SRC#Counting-command (REV=$REV_SHA)" "$rc"
    else
        begin harm-nav-fleet-round-1.txt "$NAV_SRC#Counting-command" - "$REV_SHA" \
            bash -s "<" "$NAV_SRC##Counting-command"
        printf 'status=tool_error reason=counting_block_not_found\n' >> "$OUT"
        end_out 2
        record_result harm-nav-fleet-round-1.txt \
            "bash -s < $NAV_SRC#Counting-command (REV=$REV_SHA)" 2
    fi
else
    begin harm-nav-fleet-round-1.txt "$NAV_SRC#Counting-command" - "$REV_SHA" \
        bash -s "<" "$NAV_SRC##Counting-command"
    printf 'status=tool_error reason=scorecard_unreadable\n' >> "$OUT"
    end_out 2
    record_result harm-nav-fleet-round-1.txt \
        "bash -s < $NAV_SRC#Counting-command (REV=$REV_SHA)" 2
fi

# ------------------------------------------------------- 12. sources census
GROUP=census
CENSUS="$FLEET/scripts/sources-census.sh"
FLEET_HEAD=$(git -C "$FLEET" rev-parse HEAD 2>/dev/null) || FLEET_HEAD=UNKNOWN
if [ "$FLEET_HEAD" != UNKNOWN ] && \
   pin_assert "$FLEET" scripts/sources-census.sh "$FLEET_HEAD"; then
    pin_log "$FLEET" scripts/sources-census.sh "fleet:$FLEET_HEAD"
    ARGV="$CENSUS validate --root $FLEET mado"
    begin harm-census-validate.txt "$CENSUS" "$PIN_WT" "fleet:$FLEET_HEAD" \
        "$CENSUS" validate --root "$FLEET" mado
    timeout "$TTL" "$CENSUS" validate --root "$FLEET" mado >> "$OUT" 2>&1
    rc=$?
    end_out "$rc"
    record_result harm-census-validate.txt "$ARGV" "$rc"
else
    if [ "$FLEET_HEAD" = UNKNOWN ]; then
        PIN_WT=- PIN_REV=- PIN_STATE=fleet_rev_unresolved
    fi
    pin_log "$FLEET" scripts/sources-census.sh "fleet:$FLEET_HEAD"
    pin_skip harm-census-validate.txt "$CENSUS" "fleet:$FLEET_HEAD" "$PIN_STATE" \
        "$CENSUS" validate --root "$FLEET" mado
fi

# ---------------------------------------------------------------- tallies
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

# ---------------------------------------------------------------- verdict
if [ "$FAILS" -eq 0 ]; then
    verdict=PASS
    status=0
else
    verdict="FAIL failures=$FAILS"
    status=1
fi
{
    printf 'HARM_WATCH: %s\n' "$verdict"
    printf 'rev=%s outdir=%s commands=%s failures=%s pins=%s\n' \
        "$REV_SHA" "$OUTDIR" "$RUNS" "$FAILS" "$PINS"
} >> "$SUMMARY"
printf 'HARM_WATCH: %s\n' "$verdict"
exit "$status"
