#!/usr/bin/env bash
# =============================================================================
# harm-watch.sh — round-18 harm-watch receipt runner (mado-shokunin)
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
# Commands (never the live gate; only --selftest):
#   bash tools/mado-verify.sh --selftest
#   python3 -I tools/mado-action-plan.py --selftest
#   python3 -I tools/mado-tripwire.py --selftest <suite>
#       for each dir with expected.json under
#       .ufo/waves/round-17/tripwire and .ufo/waves/round-18/tripwire
#   python3 .ufo/waves/round-16/measure.py REV
#   the SCORECARD "### Counting command" block extracted at REV, run via bash -s
#   /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate \
#       --root /home/vgpnk/Projects/shokunin mado
#
# Usage:
#   REV=<rev> [OUTDIR=<dir>] bash .ufo/waves/round-18/harm-watch.sh
#   bash .ufo/waves/round-18/harm-watch.sh <rev>
#
# OUTDIR defaults to .ufo/waves/round-18/evidence. Each command overwrites its
# own named file; harm-watch-summary.txt and harm-watch-pins.txt are rewritten.
# Exit: 0 every executed command exited 0 and every pin asserted; 1 otherwise;
#       2 usage/revision error.
# =============================================================================
set -u

ROOT=/home/vgpnk/Projects/shokunin/mado-shokunin
FLEET=/home/vgpnk/Projects/shokunin
REV_ARG="${1:-${REV:-}}"
OUTDIR="${OUTDIR:-$ROOT/.ufo/waves/round-18/evidence}"
TTL="${HARM_TIMEOUT:-1800}"

usage() {
    sed -n '2,35p' "${BASH_SOURCE[0]}" | sed 's/^# \{0,1\}//'
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
    if [ "$3" -eq 0 ]; then
        printf 'OK\texit=%s\t%s\t%s\n' "$3" "$1" "$2" >> "$SUMMARY"
    else
        printf 'FAIL\texit=%s\t%s\t%s\n' "$3" "$1" "$2" >> "$SUMMARY"
        FAILS=$((FAILS + 1))
    fi
}

skip_result() { # file reason argv
    RUNS=$((RUNS + 1))
    printf 'SKIP\t%s\t%s\t%s\n' "$2" "$1" "$3" >> "$SUMMARY"
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

# ------------------------------------------------------- 1. gate selftest
if pin_assert "$ROOT" tools/mado-verify.sh "$REV_SHA"; then
    pin_log "$ROOT" tools/mado-verify.sh "$REV_SHA"
    ARGV='bash tools/mado-verify.sh --selftest'
    begin harm-gate-selftest.txt "$ROOT/tools/mado-verify.sh" "$PIN_WT" "$REV_SHA" \
        bash tools/mado-verify.sh --selftest
    timeout "$TTL" bash tools/mado-verify.sh --selftest >> "$OUT" 2>&1
    rc=$?
    end_out "$rc"
    record_result harm-gate-selftest.txt "$ARGV" "$rc"
else
    pin_log "$ROOT" tools/mado-verify.sh "$REV_SHA"
    pin_skip harm-gate-selftest.txt "$ROOT/tools/mado-verify.sh" UNVERIFIED "$PIN_STATE" \
        bash tools/mado-verify.sh --selftest
fi

# -------------------------------------------------- 2. action-plan selftest
if pin_assert "$ROOT" tools/mado-action-plan.py "$REV_SHA"; then
    pin_log "$ROOT" tools/mado-action-plan.py "$REV_SHA"
    ARGV="python3 -I $ROOT/tools/mado-action-plan.py --selftest"
    begin harm-action-plan-selftest.txt "$ROOT/tools/mado-action-plan.py" "$PIN_WT" "$REV_SHA" \
        python3 -I "$ROOT/tools/mado-action-plan.py" --selftest
    timeout "$TTL" python3 -I "$ROOT/tools/mado-action-plan.py" --selftest >> "$OUT" 2>&1
    rc=$?
    end_out "$rc"
    record_result harm-action-plan-selftest.txt "$ARGV" "$rc"
else
    pin_log "$ROOT" tools/mado-action-plan.py "$REV_SHA"
    pin_skip harm-action-plan-selftest.txt "$ROOT/tools/mado-action-plan.py" UNVERIFIED "$PIN_STATE" \
        python3 -I "$ROOT/tools/mado-action-plan.py" --selftest
fi

# ------------------------------------------------------- 3. tripwire suites
list_suites() {
    SUITE_REL=() SUITE_FILE=() SUITE_ARGV=()
    local base twroot d name n
    for base in round-17 round-18; do
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

# ---------------------------------------------------------- 4. measure U 7/7
if pin_assert "$ROOT" .ufo/waves/round-16/measure.py "$REV_SHA"; then
    pin_log "$ROOT" .ufo/waves/round-16/measure.py "$REV_SHA"
    ARGV="python3 $ROOT/.ufo/waves/round-16/measure.py $REV_ARG"
    begin harm-measure-u.txt "$ROOT/.ufo/waves/round-16/measure.py" "$PIN_WT" "$REV_SHA" \
        python3 "$ROOT/.ufo/waves/round-16/measure.py" "$REV_ARG"
    timeout "$TTL" python3 "$ROOT/.ufo/waves/round-16/measure.py" "$REV_ARG" >> "$OUT" 2>&1
    rc=$?
    end_out "$rc"
    record_result harm-measure-u.txt "$ARGV" "$rc"
else
    pin_log "$ROOT" .ufo/waves/round-16/measure.py "$REV_SHA"
    pin_skip harm-measure-u.txt "$ROOT/.ufo/waves/round-16/measure.py" UNVERIFIED "$PIN_STATE" \
        python3 "$ROOT/.ufo/waves/round-16/measure.py" "$REV_ARG"
fi

# ------------------------------------- 5. fleet-round-1 navigation counting
NAV_BLOCK="$TMPD/nav-block.sh"
NAV_SRC="$TMPD/SCORECARD.md"
if git -C "$ROOT" show "$REV_SHA:SCORECARD.md" > "$NAV_SRC" 2>/dev/null; then
    awk '
        /^### Counting command/ { want = 1; next }
        want && /^```bash/ { inblock = 1; next }
        inblock && /^```/ { exit }
        inblock { print }
    ' "$NAV_SRC" > "$NAV_BLOCK"
    if [ -s "$NAV_BLOCK" ]; then
        BLOCK_SHA=$(sha256sum "$NAV_BLOCK" | cut -d' ' -f1)
        printf 'PIN\t%s:%s#Counting-command\t%s\tworktree=%s\trev=%s\tstate=%s\n' \
            "$REV_SHA" SCORECARD.md "$REV_SHA" "$BLOCK_SHA" "$BLOCK_SHA" extracted >> "$PINS"
        begin harm-nav-fleet-round-1.txt "$REV_SHA:SCORECARD.md#Counting-command" \
            "$BLOCK_SHA" "$REV_SHA" bash -s "<" "$REV_SHA:SCORECARD.md##Counting-command"
        REV="$REV_SHA" timeout "$TTL" bash -s < "$NAV_BLOCK" >> "$OUT" 2>&1
        rc=$?
        end_out "$rc"
        record_result harm-nav-fleet-round-1.txt \
            "bash -s < counting-block@$REV_SHA" "$rc"
    else
        begin harm-nav-fleet-round-1.txt "$REV_SHA:SCORECARD.md#Counting-command" - "$REV_SHA" \
            bash -s "<" "$REV_SHA:SCORECARD.md##Counting-command"
        printf 'status=tool_error reason=counting_block_not_found\n' >> "$OUT"
        end_out 2
        record_result harm-nav-fleet-round-1.txt "bash -s < counting-block@$REV_SHA" 2
    fi
else
    begin harm-nav-fleet-round-1.txt "$REV_SHA:SCORECARD.md#Counting-command" - "$REV_SHA" \
        bash -s "<" "$REV_SHA:SCORECARD.md##Counting-command"
    printf 'status=tool_error reason=scorecard_unreadable_at_rev\n' >> "$OUT"
    end_out 2
    record_result harm-nav-fleet-round-1.txt "bash -s < counting-block@$REV_SHA" 2
fi

# ------------------------------------------------------- 6. sources census
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
    printf 'rev=%s outdir=%s commands=%s pins=%s\n' \
        "$REV_SHA" "$OUTDIR" "$RUNS" "$PINS"
} >> "$SUMMARY"
printf 'HARM_WATCH: %s\n' "$verdict"
exit "$status"
