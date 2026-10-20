#!/usr/bin/env bash
# mutate-and-run.sh — generic mutation runner (tameshi-shokunin, r10-2, TAMESHI-T10-2).
#
# Channels: r3-2 (TAMESHI-R3-2) shipped the runner; r4-2 (TAMESHI-R4-2) adds
# --regression, this tool's own kill-rate regression gate (contract below);
# r6 (TAMESHI-T6-4) hardens --selftest with the r6 meta-sweep's surviving
# comparator mutants (corpus/knowledge/self-hardening-r6.md); r7-1
# (TAMESHI-T7-1) turns --regression into the fleet leg ledger — every recorded
# mutation case replayed at its pinned original revision, materialized from its
# repo's git object store (`git show <rev>:<path>`, immune to working-tree
# drift), with each leg's recorded kill-rate as its expectation; r10-2
# (TAMESHI-T10-2) resolves the round-8 leg cut — cases 5/6 (kagi
# `corpus/checklist-run.sh`, kumitate `scripts/claims-check.mjs`) embedded as
# the fifth and sixth legs, completing the six measured gates in this ledger.
#
# Plan anchors: r3-2 = plans/round-3.plan.md:6-7 — "the method ships as tameshi's
# own runnable tool (tools/mutate-and-run.sh: inject->run->restore with
# byte-identity proof)"; r4-2 = plans/round-4.plan.md:9-10 — "mutate-and-run.sh
# gains a --regression mode (re-run both cases as a kill-rate regression gate for
# the tool itself)"; r10-2 = the round-8/9 named hand-offs — the leg cut stands
# with the tool owner (fleet-kill-rate-ledger.md ER-2 named follow-ups;
# mutation-case-kagi-checklist.md U5; mutation-case-kumitate-claims.md E3;
# round-9 record draft: "cases 5/6 remain unembedded — named debt") and is
# resolved here as an embedding, not a re-cut. Method provenance:
# corpus/knowledge/mutation-case-kimi-census.md §0-§1 — every mutant is a fresh
# copy of a pinned pristine; one exact edit per copy with a uniqueness assert; a
# green control run; killed/survived recorded per defect; sha256 before/after as
# the restore proof; a kill-rate headline.
#
# Inputs: a target file, a defect spec file, and a suite command. For each
# defect: if this one exact edit were present in the target, would the suite go
# red? Per-defect verdicts: KILLED (suite exit != 0) | SURVIVED (suite exit 0) |
# INCONCLUSIVE (timeout 124, or 126/127 = suite not runnable). The target is
# never written: every mutant is a fresh byte copy of the pinned pristine copy,
# and the target's sha256 before/after is the restore proof.
#
# Defect spec format v1 (one directive per line; '#' comments and blank lines
# ignored; LF endings only):
#
#   @defect <id> | <description>     id: [A-Za-z0-9._-]+; description optional
#   @old <text>                      exact string to find (required)
#   @new <text>                      exact replacement (may be empty to delete)
#
#   Escapes inside <text>: \n newline, \t tab, \r CR, \\ backslash. Any other
#   backslash sequence is refused (fail-closed against spec mistakes). Exactly
#   one separator space follows the directive; write a literal leading space in
#   the text as a second space (i.e. `@old ` + the text, spaces preserved).
#   The old string must occur exactly once (asserted before any suite run);
#   @new == @old (a no-op edit) is refused.
#
# Suite command contract: --suite CMD is run as `bash -c CMD` with stdin
# </dev/null, once per run, from the caller's CWD, with these exported:
#   MUTANT    absolute path of the artifact under test (the pristine copy for
#             the control run)          TARGET   absolute path of the original
#   PRISTINE  pinned pristine copy      WORKDIR  evidence/work directory
#   DEFECT_ID  defect id (CONTROL for the control run)
# Exit-code semantics: 0 = suite green; any non-zero = red, except
# 124 (timeout) / 126 / 127 (suite not runnable) = INCONCLUSIVE.
# Example: --suite 'node "$MUTANT" --selftest'
#
# Order of operations (fail-closed): (1) copy the target to a pinned pristine
# and pin both hashes; (2) parse the spec; (3) build every mutant and assert
# count==1 — any failure exits 2 before a single suite run; (4) control run on
# the pristine — a red control exits 2 (kills could not be attributed); (5)
# mutant runs with output tails; (6) re-check target+pristine sha256; (7)
# kill-rate report. A low kill count is a finding for the report, not a failure
# of this tool (bands are a report convention, not a gate — SKILL.md:127-133).
#
# Verdict lines (the last non-empty line is the verdict):
#   MUTATE_TOOL / MUTATE_DATE / MUTATE_TARGET / MUTATE_SPEC   — provenance
#   CONTROL: GREEN|RED (exit=… duration-ms=… pristine-sha256=…)
#   DEFECT <id>: KILLED|SURVIVED|INCONCLUSIVE (exit=… duration-ms=…)
#   MUTATE_RESTORE: OK|DRIFT (target-sha256 before=… after=… …)
#   MUTATE: DONE|DEGRADED (target=… defects=… killed=… survived=… inconclusive=… kill-rate=…%)
#   MUTATE: SETUP (<reason>)   — refused before/instead of a sweep
#
# Exit map (run): 0 done · 1 done-with-inconclusive (DEGRADED) · 2 setup/refusal ·
# 64 usage error.
#
# --regression (r4-2; r7-1 leg ledger; r10-2 six legs) — the fleet's recorded
# mutation cases, replayed as legs. Each leg carries its recorded revision pin
# and its recorded verdict table; the recorded kill-rate is the leg's
# expectation:
#   js-kimi-census        kumitate-shokunin/scripts/kimi-census.mjs   8/10 (80 %)
#   bash-surface-census   kagi-shokunin/corpus/surface-census.sh      8/10 (80 %)
#   bash-tsukuroi-census  tsukuroi-shokunin/tools/tsukuroi-census.sh  6/10 (60 %)
#   bash-mado-verify      mado-shokunin/tools/mado-verify.sh          4/10 (40 %)
#   bash-checklist-run    kagi-shokunin/corpus/checklist-run.sh       7/15 (47 %)
#   js-claims-check       kumitate-shokunin/scripts/claims-check.mjs  7/10 (70 %)
# Sources: corpus/knowledge/mutation-case-kimi-census.md §1,
# mutation-case-kagi-census.md §1, mutation-case-tsukuroi-census.md §1,
# mutation-case-mado-verify.md §1, mutation-case-kagi-checklist.md §2,
# mutation-case-kumitate-claims.md §1. All six defect specs are embedded below
# (legs 1–4 cut from those notes' §7/§8/§9 reproduce manifests, all 40 @old
# strings re-verified count==1 against the pinned bytes 2026-10-14; legs 5–6
# are the recorded T8-1/T8-2 spec files, their 25 @old strings re-verified
# count==1 against the pinned blobs at r10-2).
# r7-1: the target is NOT read from the fleet working tree. Each leg is
# materialized from its repo's git object store — `git show <rev>:<path>` — so
# a working tree that has drifted past the recorded revision (tsukuroi and
# mado: their pins are ancestors of HEAD) or carries uncommitted edits cannot
# move a replay. The materialized copy's sha256 must equal the recorded pin;
# a missing repo/rev/blob or a pin mismatch is a SETUP refusal, never a pass.
# r10-2 mirrors the blob's mode too (`git show` writes bytes, not modes): a
# gate whose selftest re-execs itself (checklist-run.sh runs "$SELF") needs the
# recorded exec bit, so 100755 blobs are chmod +x'd after materialization.
# Each leg then runs as a full CLI sub-invocation of this tool over the
# materialized copy; the fleet trees are never written.
# Stated expectation: ledger legs are byte-pinned replays, so their expectation
# is exact — 0 verdict flips (every measured row must equal the recorded
# table), killed-delta 0, defects exactly the recorded count, inconclusive 0,
# control green, MUTATE_RESTORE: OK. The r4-2 tolerance (|killed-recorded| <= 1
# and at most 1 verdict flip) remains the default for fixture-mode cases and is
# exercised by --selftest. Inside the stated expectation is PASS; outside it is
# FAIL. Exit map (--regression): 0 all cases PASS · 1 >= 1 case FAIL (measured
# table outside its expectation) · 2 a case could not be verified — missing
# repo/rev/blob, pin mismatch, sweep setup refusal — with no FAIL. Lines:
# REGRESSION_TOOL / REGRESSION_DATE / REGRESSION_BAND / REGRESSION_EXPECT /
# REGRESSION_PIN (one per leg: git source + pinned target sha256; the sweep's
# own MUTATE_TOOL line carries the tool pin) / REGRESSION_SWEEP /
# REGRESSION_TABLE / REGRESSION_DEFECT (one per differing row) / REGRESSION_CASE
# / REGRESSION_WORKDIR / REGRESSION: PASS|FAIL|SETUP. Scratch root: mktemp -d
# /tmp/tameshi-r4-2-regression.XXXXXX by default; removed on PASS unless --keep,
# kept on FAIL/SETUP, never removed when --workdir was given. In this mode
# --target/--defects/--suite/--label are refused (usage error).
#
# Evidence: workdir keeps pristine copy, mutant files, evidence/<id>.out full
# logs, evidence/control.out, defects.tsv (id/line/desc), results.tsv (per
# defect: verdict/exit/duration/mutant-sha256/desc), spec.copy; the path is
# printed as MUTATE_EVIDENCE. Default: mktemp -d /tmp/tameshi-r4-2-run.XXXXXX.
#
# --selftest is hermetic: it builds a tiny fixture target + mini-suites + four
# fixture specs under /tmp/tameshi-r4-2-selftest.XXXXXX and self-checks
# control-green, one kill, one survivor, exact kill-rate line, restore proof,
# DEGRADED path, refusal paths (duplicate old string, unknown escape, no-op
# edit, missing --target, usage), and the --regression engine on the same
# fixture (in-band PASS, band-edge PASS at killed-delta 1 / flips 1, doctored
# table FAIL, an unmeasured recorded entry FAIL, an unrecorded measured row
# FAIL, a DEGRADED sub-sweep FAIL on inconclusive=1, a fully-matching all-killed
# table PASS, pin mismatch and missing target SETUP; r7-1 adds, over a
# throwaway git repo, the ledger engine: git-materialized replay PASS,
# drift-immune replay of the pinned blob, blob/pin mismatch and unresolvable
# revision SETUP, and the exact-tolerance arm where one flipped recorded entry
# FAILs; r10-2 adds the embedded-ledger sweep: the six leg specs are written
# and parsed, and each recorded table's ids, total and killed count are checked
# against its own spec, plus the exec-bit mirror arms (a blob committed 100755
# runs a self-exec suite; the same bytes committed 100644 are refused at their
# red control) — hermetic, no fleet path read). Scratch is removed on PASS,
# kept on FAIL for inspection.
#
# Dependencies: bash, python3 (byte-exact edit + spec parse), git (--regression
# materialization + the selftest's ledger-engine cases), coreutils (sha256sum,
# mktemp, timeout, cp, date).

set -u -o pipefail

VERSION='mutate-and-run.sh r10-2 (tameshi-shokunin, 2026-10-14)'
SELF=$(readlink -f "${BASH_SOURCE[0]}")

MODE=run
TARGET=''
SPEC=''
SUITE=''
WORKDIR=''
LABEL=''
TIMEOUT_S=300
TAIL_N=8
BAND_KILLED=1   # --regression: |killed - recorded| tolerance, per case
BAND_FLIPS=1    # --regression: max verdict differences vs the recorded table
KEEP=0          # --regression: keep the scratch root also on PASS

usage() {
  cat <<'EOF'
mutate-and-run.sh — generic mutation runner (tameshi-shokunin)

Usage:
  mutate-and-run.sh --target FILE --defects SPEC --suite CMD [options]
  mutate-and-run.sh --regression [--workdir DIR] [--keep]
  mutate-and-run.sh --selftest
  mutate-and-run.sh --help

Inputs:
  --target FILE    artifact to mutate (never written; sha256 pinned before/after)
  --defects SPEC   defect spec file (format below)
  --suite CMD      suite command, run as `bash -c CMD` with $MUTANT set to the
                   artifact under test (the pristine copy for the control run)

Options:
  --workdir DIR    evidence/work dir (default: mktemp -d /tmp/tameshi-r4-2-run.XXXXXX)
  --label NAME     name for the report (default: basename of the target)
  --timeout N      seconds per suite run (default: 300)
  --tail N         output tail lines shown per run (default: 8)
  --keep           --regression only: keep the scratch root also on PASS

--regression replays every recorded mutation case as a leg (js-kimi-census,
bash-surface-census, bash-tsukuroi-census, bash-mado-verify,
bash-checklist-run, js-claims-check) at its pinned original revision,
materialized from the repo's git object store (`git show <rev>:<path>` —
immune to working-tree drift; a missing repo/rev/blob or a pin mismatch is a
SETUP refusal). Each leg must reproduce its recorded verdict table exactly:
the recorded kill-rate is the leg's expectation (flips 0, killed-delta 0,
count exactly the recorded defect count, inconclusive 0, control green, restore
OK). Exit: 0 all legs PASS · 1 >= 1 leg out of band · 2 cannot verify (missing
repo/rev/blob / pin mismatch / setup refusal). Fleet trees are never written.
See the file header for the full contract and evidence layout.

Spec format v1 (one directive per line; '#' comments; blank lines ignored):
  @defect <id> | <description>
  @old <text>          exact string to find (count==1 asserted before any run)
  @new <text>          exact replacement (may be empty)
  escapes: \n \t \r \\; any other backslash sequence is refused.

Verdicts per defect: KILLED | SURVIVED | INCONCLUSIVE. Exit map (run): 0 done ·
1 done-with-inconclusive · 2 setup/refusal · 64 usage.
EOF
}

usage_exit() {
  printf 'mutate-and-run: %s\n' "$1" >&2
  usage >&2
  exit 64
}

die_setup() {
  printf 'MUTATE: SETUP (%s)\n' "$1" >&2
  exit 2
}

need_val() {
  if [[ $# -lt 2 || -z "${2-}" ]]; then
    usage_exit "$1 needs a value"
  fi
}

sha_of() {
  local h
  h=$(sha256sum -- "$1" | cut -d' ' -f1) || die_setup "sha256sum failed for $1"
  printf '%s' "$h"
}

print_tail() {
  local f=$1 n
  n=$(wc -l < "$f")
  if [[ "$n" -eq 0 ]]; then
    printf '  | (no output)\n'
    return 0
  fi
  while IFS= read -r l; do printf '  | %s\n' "$l"; done < <(tail -n "$TAIL_N" "$f")
}

# ---------------------------------------------------------------- spec helper

py_helper() {
  python3 - "$@" <<'PYEOF'
"""Spec helper for mutate-and-run.sh: `list <spec>` | `apply <spec> <pristine>
<mutant> <id>`. Byte-exact single replace; count==1 asserted; refuses no-ops."""
import sys

ESCAPES = {'n': '\n', 't': '\t', 'r': '\r', '\\': '\\'}


def die(msg):
    sys.stderr.write('spec: %s\n' % msg)
    sys.exit(2)


def unescape(s, where):
    out = []
    i = 0
    while i < len(s):
        c = s[i]
        if c == '\\':
            if i + 1 >= len(s):
                die('%s: trailing backslash' % where)
            n = s[i + 1]
            if n not in ESCAPES:
                die("%s: unknown escape '\\%s' (supported: \\n \\t \\r \\\\)" % (where, n))
            out.append(ESCAPES[n])
            i += 2
        else:
            out.append(c)
            i += 1
    return ''.join(out)


def parse(path):
    try:
        with open(path, encoding='utf-8') as fh:
            text = fh.read()
    except (OSError, UnicodeDecodeError) as e:
        die('cannot read spec file %s: %s' % (path, e))
    if '\r' in text:
        die('CR characters in spec (CRLF line endings are not supported)')
    defects = []
    cur = None

    def finish():
        nonlocal cur
        if cur is not None and ('old' not in cur or 'new' not in cur):
            die('line %d: defect %s incomplete (needs both @old and @new)' % (cur['line'], cur['id']))
        cur = None

    for no, line in enumerate(text.split('\n'), 1):
        if line.strip() == '':
            continue
        if line.lstrip().startswith('#'):
            continue
        if line == '@defect' or line.startswith('@defect '):
            finish()
            rest = line[len('@defect'):].lstrip(' ')
            idpart, sep, desc = rest.partition('|')
            idpart, desc = idpart.strip(), desc.strip()
            if not idpart or any(ch not in 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789._-' for ch in idpart):
                die('line %d: bad or missing defect id: %r' % (no, idpart))
            if any(d['id'] == idpart for d in defects):
                die('line %d: duplicate defect id %s' % (no, idpart))
            if '\t' in desc:
                die('line %d: description must not contain a tab' % no)
            cur = {'id': idpart, 'desc': desc, 'line': no}
            defects.append(cur)
        elif line == '@old' or line.startswith('@old '):
            if cur is None:
                die('line %d: @old outside a defect' % no)
            if 'old' in cur:
                die('line %d: duplicate @old for defect %s' % (no, cur['id']))
            cur['old'] = unescape('' if line == '@old' else line[len('@old '):], 'line %d' % no)
        elif line == '@new' or line.startswith('@new '):
            if cur is None:
                die('line %d: @new outside a defect' % no)
            if 'new' in cur:
                die('line %d: duplicate @new for defect %s' % (no, cur['id']))
            cur['new'] = unescape('' if line == '@new' else line[len('@new '):], 'line %d' % no)
        else:
            die('line %d: unrecognized line: %r' % (no, line[:80]))
    finish()
    if not defects:
        die('spec contains no defects')
    for d in defects:
        if d['old'] == '':
            die('defect %s: @old text is empty' % d['id'])
        if d['old'] == d['new']:
            die('defect %s: @new equals @old (no-op mutation)' % d['id'])
    return defects


def cmd_list(path):
    for d in parse(path):
        sys.stdout.write('%s\t%d\t%s\n' % (d['id'], d['line'], d['desc']))


def cmd_apply(path, pristine, mutant, did):
    hits = [d for d in parse(path) if d['id'] == did]
    if not hits:
        die('defect %s not found in spec' % did)
    d = hits[0]
    try:
        data = open(pristine, 'rb').read()
    except OSError as e:
        die('cannot read pristine %s: %s' % (pristine, e))
    old = d['old'].encode('utf-8')
    new = d['new'].encode('utf-8')
    count = data.count(old)
    if count != 1:
        sys.stderr.write('APPLY FAIL id=%s line=%d old-string-count=%d expected=1\n' % (did, d['line'], count))
        sys.exit(2)
    result = data.replace(old, new, 1)
    try:
        with open(mutant, 'wb') as fh:
            fh.write(result)
    except OSError as e:
        die('cannot write mutant %s: %s' % (mutant, e))
    sys.stdout.write('APPLY OK id=%s old-count=1 bytes-before=%d bytes-after=%d\n' % (did, len(data), len(result)))


if len(sys.argv) < 2 or sys.argv[1] not in ('list', 'apply'):
    sys.stderr.write('helper: usage: list <spec> | apply <spec> <pristine> <mutant> <id>\n')
    sys.exit(2)
if sys.argv[1] == 'list':
    if len(sys.argv) != 3:
        die('helper: list needs <spec>')
    cmd_list(sys.argv[2])
else:
    if len(sys.argv) != 6:
        die('helper: apply needs <spec> <pristine> <mutant> <id>')
    cmd_apply(sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5])
PYEOF
}

# ------------------------------------------------------------------- sweep

run_one() { # $1 = artifact under test, $2 = evidence file, $3 = defect id
  local start now
  start=$(date +%s%N)
  MUTANT="$1" TARGET="$TARGET_ABS" PRISTINE="$PRISTINE" WORKDIR="$WORKDIR" DEFECT_ID="$3" \
    timeout "$TIMEOUT_S" bash -c "$SUITE" </dev/null >"$2" 2>&1
  RC=$?
  now=$(date +%s%N)
  DUR_MS=$(( (now - start) / 1000000 ))
}

run_sweep() {
  command -v python3 >/dev/null 2>&1 || die_setup 'python3 missing'
  command -v sha256sum >/dev/null 2>&1 || die_setup 'sha256sum missing'
  command -v timeout >/dev/null 2>&1 || die_setup 'timeout missing'
  command -v mktemp >/dev/null 2>&1 || die_setup 'mktemp missing'

  [[ -n "$TARGET" ]] || usage_exit 'missing --target'
  [[ -n "$SPEC" ]] || usage_exit 'missing --defects'
  [[ -n "$SUITE" ]] || usage_exit 'missing --suite'
  [[ -f "$TARGET" ]] || die_setup "target is not a regular file: $TARGET"
  [[ -r "$TARGET" ]] || die_setup "target is not readable: $TARGET"
  [[ -f "$SPEC" ]] || die_setup "spec is not a regular file: $SPEC"
  [[ -r "$SPEC" ]] || die_setup "spec is not readable: $SPEC"
  (( TIMEOUT_S > 0 )) || usage_exit '--timeout must be a positive integer'
  (( TAIL_N > 0 )) || usage_exit '--tail must be a positive integer'

  TARGET_ABS=$(readlink -f "$TARGET")
  SPEC_ABS=$(readlink -f "$SPEC")

  if [[ -z "$WORKDIR" ]]; then
    WORKDIR=$(mktemp -d /tmp/tameshi-r4-2-run.XXXXXX) || die_setup 'mktemp -d failed'
  else
    mkdir -p "$WORKDIR" || die_setup "cannot create workdir: $WORKDIR"
  fi
  EVID="$WORKDIR/evidence"
  mkdir -p "$EVID" || die_setup "cannot create evidence dir: $EVID"
  [[ -n "$LABEL" ]] || LABEL=$(basename "$TARGET_ABS")

  TARGET_SHA0=$(sha_of "$TARGET_ABS")
  PRISTINE="$WORKDIR/pristine.$(basename "$TARGET_ABS")"
  cp -p "$TARGET_ABS" "$PRISTINE" || die_setup "cannot copy target to pristine: $PRISTINE"
  PRISTINE_SHA=$(sha_of "$PRISTINE")
  PRISTINE_BYTES=$(wc -c < "$PRISTINE")
  [[ "$TARGET_SHA0" == "$PRISTINE_SHA" ]] || die_setup 'read race: target changed while copying'

  printf 'MUTATE_TOOL: %s sha256=%s\n' "$SELF" "$(sha_of "$SELF")"
  printf 'MUTATE_DATE: %s\n' "$(date -u +%Y-%m-%dT%H:%M:%SZ)"
  printf 'MUTATE_TARGET: %s sha256=%s bytes=%s\n' "$TARGET_ABS" "$TARGET_SHA0" "$PRISTINE_BYTES"

  local out
  if ! out=$(py_helper list "$SPEC_ABS" 2>&1); then
    printf '%s\n' "$out"
    die_setup 'spec parse failed'
  fi
  local total
  total=$(printf '%s\n' "$out" | wc -l)
  printf 'MUTATE_SPEC: %s defects=%s\n' "$SPEC_ABS" "$total"
  printf '%s\n' "$out" > "$WORKDIR/defects.tsv"
  [[ "$SPEC_ABS" == "$WORKDIR/spec.copy" ]] || cp -p "$SPEC_ABS" "$WORKDIR/spec.copy"

  local id line desc mutant aout fail=0
  while IFS=$'\t' read -r id line desc; do
    [[ -n "$id" ]] || continue
    mutant="$WORKDIR/mutant-$id.$(basename "$TARGET_ABS")"
    cp -p "$PRISTINE" "$mutant" || die_setup "cannot create mutant copy: $mutant"
    if ! aout=$(py_helper apply "$SPEC_ABS" "$PRISTINE" "$mutant" "$id" 2>&1); then
      printf '%s\n' "$aout"
      fail=$((fail + 1))
    fi
  done <<<"$out"
  if [[ "$fail" -gt 0 ]]; then
    die_setup "spec/preparation failed for $fail defect(s); no suite run"
  fi

  local ctl_rc ctl_ms
  run_one "$PRISTINE" "$EVID/control.out" CONTROL
  ctl_rc=$RC
  ctl_ms=$DUR_MS
  if [[ "$ctl_rc" -ne 0 ]]; then
    printf 'CONTROL: RED (exit=%s duration-ms=%s pristine-sha256=%s)\n' "$ctl_rc" "$ctl_ms" "$PRISTINE_SHA"
    print_tail "$EVID/control.out"
    die_setup "control run on the pristine copy is red (exit=$ctl_rc); cannot attribute kills; log: $EVID/control.out"
  fi
  printf 'CONTROL: GREEN (exit=0 duration-ms=%s pristine-sha256=%s)\n' "$ctl_ms" "$PRISTINE_SHA"
  print_tail "$EVID/control.out"

  local killed=0 survived=0 inconcl=0 v note
  printf 'id\tverdict\texit\tduration-ms\tmutant-sha256\tdesc\n' > "$WORKDIR/results.tsv"
  while IFS=$'\t' read -r id line desc; do
    [[ -n "$id" ]] || continue
    mutant="$WORKDIR/mutant-$id.$(basename "$TARGET_ABS")"
    run_one "$mutant" "$EVID/$id.out" "$id"
    note=''
    case $RC in
      0) v=SURVIVED; survived=$((survived + 1)) ;;
      124) v=INCONCLUSIVE; inconcl=$((inconcl + 1)); note=' note=timeout' ;;
      126) v=INCONCLUSIVE; inconcl=$((inconcl + 1)); note=' note=suite-not-executable' ;;
      127) v=INCONCLUSIVE; inconcl=$((inconcl + 1)); note=' note=suite-not-found' ;;
      *) v=KILLED; killed=$((killed + 1)) ;;
    esac
    printf 'DEFECT %s: %s (exit=%s%s duration-ms=%s) %s\n' "$id" "$v" "$RC" "$note" "$DUR_MS" "$desc"
    print_tail "$EVID/$id.out"
    printf '%s\t%s\t%s\t%s\t%s\t%s\n' "$id" "$v" "$RC" "$DUR_MS" "$(sha_of "$mutant")" "$desc" >> "$WORKDIR/results.tsv"
  done <<<"$out"

  local target_sha1 pristine_sha1
  target_sha1=$(sha_of "$TARGET_ABS")
  pristine_sha1=$(sha_of "$PRISTINE")
  if [[ "$TARGET_SHA0" != "$target_sha1" || "$PRISTINE_SHA" != "$pristine_sha1" ]]; then
    printf 'MUTATE_RESTORE: DRIFT (target-sha256 before=%s after=%s pristine-sha256-before=%s after=%s)\n' \
      "$TARGET_SHA0" "$target_sha1" "$PRISTINE_SHA" "$pristine_sha1"
    die_setup 'byte-identity proof failed: target or pristine changed during the sweep'
  fi
  printf 'MUTATE_RESTORE: OK (target-sha256 before=%s after=%s pristine-sha256=%s)\n' \
    "$TARGET_SHA0" "$target_sha1" "$pristine_sha1"
  printf 'MUTATE_EVIDENCE: %s\n' "$WORKDIR"

  local pct
  pct=$(( (200 * killed + total) / (2 * total) ))
  if [[ "$inconcl" -gt 0 ]]; then
    printf 'MUTATE: DEGRADED (target=%s defects=%s killed=%s survived=%s inconclusive=%s kill-rate=%s%%)\n' \
      "$LABEL" "$total" "$killed" "$survived" "$inconcl" "$pct"
    exit 1
  fi
  printf 'MUTATE: DONE (target=%s defects=%s killed=%s survived=%s inconclusive=%s kill-rate=%s%%)\n' \
    "$LABEL" "$total" "$killed" "$survived" "$inconcl" "$pct"
  exit 0
}

# --------------------------------------------------------------- regression

# Recorded expectations for --regression (r7-1 leg ledger; r10-2 leg cut
# resolved — cases 5/6 embedded). Anchors:
# corpus/knowledge/mutation-case-kimi-census.md §1 (js — control green, killed
# D1,D3-D9, survived D2,D10, kill-rate 80 % at :29),
# mutation-case-kagi-census.md §1 (bash — control green, killed B1-B4,B6-B9,
# survived B5,B10, kill-rate 80 % at :50-53),
# mutation-case-tsukuroi-census.md §1 (bash — control green, killed B1-B6,
# survived B7-B10, kill-rate 60 % at :69-70),
# mutation-case-mado-verify.md §1 (bash — control green, killed D1,D2,D4,D6,
# survived D3,D5,D7-D9,R1, kill-rate 40 % at :61-62),
# mutation-case-kagi-checklist.md §2 (bash — control green, killed A2,B2,B4,C2,
# D2,E1,F1, survived A1,B1,B3,C1,D1,E2,F2,G1, 7/15 = 47 % at :130-131),
# mutation-case-kumitate-claims.md §1 (js — control green, killed D1-D6,D10,
# survived D7,D8,D9, 7/10 = 70 % at :63-65). The specs below: legs 1–4 are
# those notes' §7/§8/§9 reproduce manifests (re-verified count==1 against the
# pinned blobs on 2026-10-14); legs 5–6 are the recorded T8-1/T8-2 spec files
# (/tmp/w8-tameshi-t81/checklist.spec; /tmp/w8-t8-2-claims/spec/
# claims-check.defects.spec), re-verified count==1 against the pinned blobs at
# r10-2. REV_* = the git revision each leg's bytes are materialized from
# (`git show <rev>:<repo path>`).
PIN_JS=83016d45049b009a6c9868dc392ff6ebcecb357c9abfe423f476459f2724f426
REV_JS=175de6ba2e9e904010411b19cab27e0af9aad3d4
PIN_BASH=275d8294a94e9eb74caa72043607e9ff12a30414c2d6298a37cbd62ddb53009f
REV_BASH=fecee8743e52eb8fb5fbb40782934cb619a1a96e
PIN_TSUKUROI=084951be50bcbfee5e3f22de3c270d87131550ea1ce8264a557a34c5809c78c5
REV_TSUKUROI=165307fe4746a8807b02ec4a7d7ecac0368454a6
PIN_MADO=d7edaab4bf108625d213393b77432d7c0104daaa487c801fbc8bba16e32d0e13
REV_MADO=eead56b20ad2b28299ae4fa623d52a99b44c743c
PIN_CHECKLIST=7e5ec98b9e1d0afaa4d4d0f0d91f897236e8a8b4c7912ccad94d86492fd576bf
REV_CHECKLIST=fecee8743e52eb8fb5fbb40782934cb619a1a96e
PIN_CLAIMS=e9a21b441f1216bf41d1cca037b36021c581ec7892df3bf973295f9321b0f61b
REV_CLAIMS=175de6ba2e9e904010411b19cab27e0af9aad3d4
TABLE_JS='D1:KILLED,D2:SURVIVED,D3:KILLED,D4:KILLED,D5:KILLED,D6:KILLED,D7:KILLED,D8:KILLED,D9:KILLED,D10:SURVIVED'
TABLE_BASH='B1:KILLED,B2:KILLED,B3:KILLED,B4:KILLED,B5:SURVIVED,B6:KILLED,B7:KILLED,B8:KILLED,B9:KILLED,B10:SURVIVED'
TABLE_TSUKUROI='B1:KILLED,B2:KILLED,B3:KILLED,B4:KILLED,B5:KILLED,B6:KILLED,B7:SURVIVED,B8:SURVIVED,B9:SURVIVED,B10:SURVIVED'
TABLE_MADO='D1:KILLED,D2:KILLED,D3:SURVIVED,D4:KILLED,D5:SURVIVED,D6:KILLED,D7:SURVIVED,D8:SURVIVED,D9:SURVIVED,R1:SURVIVED'
TABLE_CHECKLIST='A1:SURVIVED,A2:KILLED,B1:SURVIVED,B2:KILLED,B3:SURVIVED,B4:KILLED,C1:SURVIVED,C2:KILLED,D1:SURVIVED,D2:KILLED,E1:KILLED,E2:SURVIVED,F1:KILLED,F2:SURVIVED,G1:SURVIVED'
TABLE_CLAIMS='D1:KILLED,D2:KILLED,D3:KILLED,D4:KILLED,D5:KILLED,D6:KILLED,D7:SURVIVED,D8:SURVIVED,D9:SURVIVED,D10:KILLED'
FLEET_ROOT=''   # set by run_regression; regression_case_git resolves repos from it

table_lookup() { # <table ID:V,...> <id> -> verdict, or '-' when the id is absent
  local pair
  for pair in ${1//,/ }; do
    if [[ "${pair%%:*}" == "$2" ]]; then
      printf '%s' "${pair#*:}"
      return 0
    fi
  done
  printf '%s' '-'
}

table_count() { # <table> <verdict> -> how many entries carry that verdict
  local pair n=0
  for pair in ${1//,/ }; do
    if [[ "${pair#*:}" == "$2" ]]; then n=$((n + 1)); fi
  done
  printf '%s' "$n"
}

table_total() { # <table> -> number of entries
  local pair n=0
  for pair in ${1//,/ }; do n=$((n + 1)); done
  printf '%s' "$n"
}

regression_specs() { # <dir> — write the two embedded case specs
  local d=$1
  cat >"$d/js-kimi-census.spec" <<'EOT'
@defect D1 | kimi-census.mjs:105
@old kind: 'dir', counted: 18 },
@new kind: 'dir', counted: 17 },

@defect D2 | kimi-census.mjs:378
@old findings.slice(0, 6).map
@new findings.slice(0, 5).map

@defect D3 | kimi-census.mjs:332
@old       if (!e.children.includes(n)) {
@new       if (e.children.includes(n)) {

@defect D4 | kimi-census.mjs:351-353
@old   for (const n of strays) {\n    err('UNLISTED', n, `${n} sits at the root and is not declared by the frozen K1–K5 set`);\n  }\n
@new 

@defect D5 | kimi-census.mjs:255
@old       const present = gens.length > 0;
@new       const present = true;

@defect D6 | kimi-census.mjs:124
@old kind: 'file', secret: true, modeFloor: 0o600 },
@new kind: 'file', secret: true, modeFloor: 0o644 },

@defect D7 | kimi-census.mjs:306
@old (mode & m.modeFloor) !== m.modeFloor
@new (mode & m.modeFloor) === 0

@defect D8 | kimi-census.mjs:396
@old   return 2;\n
@new   return 1;\n

@defect D9 | kimi-census.mjs:292
@old         ? (m.kind === 'dir' ? kind === 'dir' : isLeaf(kind))
@new         ? (m.kind === 'dir' ? kind === 'dir' : kind === 'file')

@defect D10 | kimi-census.mjs:145
@old const FROZEN = { K1: 3, K2: 25, K3: 9, K4: 9, K5: 3 };
@new const FROZEN = { K1: 3, K2: 24, K3: 9, K4: 9, K5: 3 };
EOT
  cat >"$d/bash-surface-census.spec" <<'EOT'
@defect B1 | surface-census.sh:241
@old   [[ ${#SCAN_DIR[@]} -eq 0 ]] && return 0
@new   [[ ${#SCAN_DIR[@]} -ne 0 ]] && return 0

@defect B2 | surface-census.sh:435
@old             elif [[ "$got" -ge "$floor" ]]; then printf 'SHAPE OK       %s rows %s %s >= %s\\n' "$p" "$tbl" "$got" "$floor"
@new             elif [[ "$got" -gt "$floor" ]]; then printf 'SHAPE OK       %s rows %s %s >= %s\\n' "$p" "$tbl" "$got" "$floor"

@defect B3 | surface-census.sh:229
@old       if [[ -n "$want_mode" && "$want_mode" != "$mode" ]]; then
@new       if [[ -n "$want_mode" && "$want_mode" == "$mode" ]]; then

@defect B4 | surface-census.sh:200-204
@old     if [[ "$live" == "symlink" ]]; then\n      printf 'SURFACE LINK     %s (declared %s)\\n' "$p" "$kind"\n      N_LINK=$((N_LINK + 1)); FAILED=1\n      continue\n    fi\n
@new 

@defect B5 | surface-census.sh:214-217
@old            if [[ "$kind" == "exec" && ! -x "$abs" ]]; then\n             printf 'SURFACE DIVERGED %s (declared exec, no execute bit)\\n' "$p"\n             N_DIVERGED=$((N_DIVERGED + 1)); FAILED=1; continue\n           fi ;;\n
@new            ;;\n

@defect B6 | surface-census.sh:371
@old         if head -c "$(( ${#value} + 1 ))" "$abs" | cmp -s - "$MAGIC_EXPECT"; then
@new         if head -c "${#value}" "$abs" | cmp -s - "$MAGIC_EXPECT"; then

@defect B7 | surface-census.sh:405-406
@old             printf 'SHAPE UNVERIFIED %s %s (%s)\\n' "$p" "$assertion" "${S_ERR_A[$p]}"\n            N_UNVERIFIED=$((N_UNVERIFIED + 1)); FAILED=1
@new             printf 'SHAPE UNVERIFIED %s %s (%s)\\n' "$p" "$assertion" "${S_ERR_A[$p]}"\n            N_UNVERIFIED=$((N_UNVERIFIED + 2)); FAILED=1

@defect B8 | surface-census.sh:85
@old die() { printf 'surface-census: %s\\n' "$1" >&2; exit 2; }
@new die() { printf 'surface-census: %s\\n' "$1" >&2; exit 1; }

@defect B9 | surface-census.sh:191
@old       if [[ "$cls" == "runtime" ]]; then
@new       if [[ "$cls" == "asset" ]]; then

@defect B10 | surface-census.sh:862
@old         "${#SCAN_DIR[@]}" "$N_OK" "$N_ABSENT" "$N_SKIP"
@new         "${#SCAN_DIR[@]}" "$N_ABSENT" "$N_ABSENT" "$N_SKIP"
EOT
  # r7-1 leg 3: tsukuroi tools/tsukuroi-census.sh @ 165307fe (pin 084951be…c78c5),
  # recorded 6/10 killed; generated from the recorded round-5 driver manifest
  # (/tmp/w5-tameshi-1-work/mutate_driver.py DEFECTS; B3/B10 are line-range
  # replacements), every @old re-verified count==1 against the pinned blob.
  cat >"$d/bash-tsukuroi-census.spec" <<'EOT'
@defect B1 | tsukuroi-census.sh:473
@old     if [ "$smi" != ok ]; then
@new     if [ "$smi" == ok ]; then

@defect B2 | tsukuroi-census.sh:281
@old   if [ "$s_rc" -ne 0 ] && [ "$s_rc" -ne 1 ]; then
@new   if [ "$s_rc" -ne 0 ] && [ "$s_rc" -ne 2 ]; then

@defect B3 | tsukuroi-census.sh:434-452
@old   # kerr == 0 is only a pass if the ring really has data; an empty ring cannot be told\n  # apart from a clean one, and must never be quoted as a fake HEALTHY.\n  if [ "$kerr" -eq 0 ]; then\n    if [ "$ring" = 'journalctl-k' ]; then\n      cap "$JOURNALCTL" -k -b -o json --no-pager\n      if [ "$CAP_RC" -ne 0 ] || [ "$(nlines "$CAP_OUT")" -eq 0 ]; then\n        DRV_V=BLOCKED\n        DRV_NOTE='kernel ring empty/unreadable (journalctl -k -b lists no kernel entries)'\n        return\n      fi\n    else\n      cap "$DMESG"\n      if [ "$CAP_RC" -ne 0 ] || [ "$(nlines "$CAP_OUT")" -eq 0 ]; then\n        DRV_V=BLOCKED\n        DRV_NOTE='kernel ring empty/unreadable (dmesg lists no records)'\n        return\n      fi\n    fi\n  fi\n
@new 

@defect B4 | tsukuroi-census.sh:578
@old       /"SYSLOG_IDENTIFIER":"kernel"|"_TRANSPORT":"kernel"/ { k++; next }
@new       /"_TRANSPORT":"kernel"/ { k++; next }

@defect B5 | tsukuroi-census.sh:615
@old       drift=$((drift + 1))
@new       drift=$((drift + 2))

@defect B6 | tsukuroi-census.sh:210
@old   if [ "$(rank "$2")" -gt "$(rank "$1")" ]; then printf '%s' "$2"; else printf '%s' "$1"; fi
@new   if [ "$(rank "$2")" -lt "$(rank "$1")" ]; then printf '%s' "$2"; else printf '%s' "$1"; fi

@defect B7 | tsukuroi-census.sh:160
@old SAMPLE_N=${TSUKUROI_SAMPLE_N:-8}
@new SAMPLE_N=${TSUKUROI_SAMPLE_N:-9}

@defect B8 | tsukuroi-census.sh:935
@old       *) printf 'tsukuroi-census: unknown argument: %s\\n' "$1" >&2; usage >&2; exit 2 ;;
@new       *) printf 'tsukuroi-census: unknown argument: %s\\n' "$1" >&2; usage >&2; exit 1 ;;

@defect B9 | tsukuroi-census.sh:967
@old     "$roll" "$PKG_V" "$SYS_V" "$DRV_V" "$JRN_V"
@new     "$roll" "$SYS_V" "$PKG_V" "$DRV_V" "$JRN_V"

@defect B10 | tsukuroi-census.sh:487-493
@old   else\n    if [ "$smi" = ok ] && [ "$mods" -gt 0 ]; then\n      nv='present(pci inventory unreadable)'\n    else\n      DRV_V=BLOCKED\n      modnote='PCI inventory unreadable and no positive nvidia evidence — cannot assess read-only'\n    fi\n
@new   else\n    nv='absent(pci_10de=0)'\n
EOT
  # r7-1 leg 4: mado tools/mado-verify.sh @ eead56b (pin d7edaab4…d0e13),
  # recorded 4/10 killed; the recorded round-6 spec file verbatim (/tmp/
  # w6-tameshi-mado-verify/spec/mado-verify.defects.spec), every @old
  # re-verified count==1 against the pinned blob.
  cat >"$d/bash-mado-verify.spec" <<'EOT'
# defect spec v1 — T6-1 service sweep, target mado-shokunin/tools/mado-verify.sh
# pin: sha256 d7edaab4bf108625d213393b77432d7c0104daaa487c801fbc8bba16e32d0e13
# clause map: A verdict token · B UNKNOWN-never-CLEAN · C exit map · D declared-plane census
#             E sha comparison · F reader fallback

@defect D1 | clause A: file-plane CLEAN verdict token renamed (CLEAN -> OK)
@old MADO_VERIFY: CLEAN (%s pass, %s notes; file plane only
@new MADO_VERIFY: OK (%s pass, %s notes; file plane only

@defect D2 | clause B: UNKNOWN guard dropped from the CLEAN test
@old if [ "$FAIL" = 0 ] && [ "$UNKNOWN" = 0 ]; then
@new if [ "$FAIL" = 0 ]; then

@defect D3 | clause B: skipped live layer row reports PASS instead of SKIP
@old     row hypr-live live.plane SKIP "live layer skipped ($live_skipped_reason) — file plane only"
@new     row hypr-live live.plane PASS "live layer skipped ($live_skipped_reason) — file plane only"

@defect D4 | clause C: DIVERGED path exits 0
@old "$reason"\nexit 1
@new "$reason"\nexit 0

@defect D5 | clause C: failing --selftest returns 1 not 2
@old   return 2
@new   return 1

@defect D6 | clause D: xdph dropped from the 12-conf local inventory
@old (hyprland bindings input monitors looknfeel hypridle hyprlock hyprsunset ai-usage autostart envs xdph)
@new (hyprland bindings input monitors looknfeel hypridle hyprlock hyprsunset ai-usage autostart envs)

@defect D7 | clause D: include-graph count test -ne -> -lt (extra source lines tolerated)
@old if [ "${#got[@]}" -ne "${#EXPECT[@]}" ]; then
@new if [ "${#got[@]}" -lt "${#EXPECT[@]}" ]; then

@defect D8 | clause E: hyprland.conf sha pin comparison always "matches"
@old if [ "$sha" = "4f52854a3c14" ]; then
@new if [ -n "$sha" ]; then

@defect D9 | clause E: read-only boundary comparison always reads byte-identical
@old if [ "$after" = "$before" ]; then
@new if [ -n "$after" ]; then

@defect R1 | clause F: tomllib-unavailable arm reads PASS not UNKNOWN
@old     row walker walker.config UNKNOWN "python3 tomllib unavailable — cannot parse TOML"
@new     row walker walker.config PASS "python3 tomllib unavailable — cannot parse TOML"
EOT
  # r10-2 leg 5: kagi corpus/checklist-run.sh @ fecee874 (pin 7e5ec98b…),
  # recorded 7/15 killed; the recorded T8-1 spec file verbatim
  # (/tmp/w8-tameshi-t81/checklist.spec), every @old re-verified count==1
  # against the pinned blob.
  cat >"$d/bash-checklist-run.spec" <<'EOT'
# T8-1 mutation spec — kagi-shokunin/corpus/checklist-run.sh
# target pin sha256 7e5ec98b9e1d0afaa4d4d0f0d91f897236e8a8b4c7912ccad94d86492fd576bf
# (506 L / 24697 B, mode 755, mtime 2026-10-13 16:51:07 -0300; = kagi HEAD fecee87 blob)
# clause map (gate's declared contract, checklist-run.sh:2-61):
#   A item extraction (:96-116)      B row-declaration policy (:120-172)
#   C lead bijection (:205-237)      D ratio floor (:174, :239-246)
#   E row execution (:256-279)       F verdict lines / exit map (:281-297)
#   G CLI modes (:79-91, :501-506)
# predictions pre-registered BEFORE the sweep; K = expect KILLED, S = expect SURVIVED.
#
@defect A1 | section never closes — the '## ' stop becomes an exact two-char header  # predict S (hole)
@old     [[ "$line" == '## '* ]] && break
@new     [[ "$line" == '## ' ]] && break
#
@defect A2 | section never opens — the header gate sets in=0  # predict K
@old       [[ "$line" == '## Credential-hygiene checklist' ]] && in=1
@new       [[ "$line" == '## Credential-hygiene checklist' ]] && in=0
#
@defect B1 | id charset loosened to ^[A-Z]+[0-9]+$ (multi-letter ids accepted)  # predict S (hole)
@old     if [[ ! "$id" =~ ^[A-Z][0-9]+$ ]]; then
@new     if [[ ! "$id" =~ ^[A-Z]+[0-9]+$ ]]; then
#
@defect B2 | by-hand non-space floor 20 -> 0 (padded reasons accepted)  # predict K
@old     ((ns >= 20)) || {
@new     ((ns >= 0)) || {
#
@defect B3 | deny list drops `the-janitor stop` (a denied surface re-opens)  # predict S (hole)
@old the-janitor start|the-janitor stop|the-janitor run
@new the-janitor start|the-janitor run
#
@defect B4 | expect_exit accepts a single integer only (multi-exit rows become POLICY)  # predict K
@old     [[ "$exexit" =~ ^[0-9]+(\\|[0-9]+)*$ ]]
@new     [[ "$exexit" =~ ^[0-9]+$ ]]
#
@defect C1 | UNMATCHED-ITEM never reported (condition 0 -> -1)  # predict S (hole)
@old ((hits == 0)) && defect "UNMATCHED-ITEM
@new ((hits == -1)) && defect "UNMATCHED-ITEM
#
@defect C2 | DUPLICATE-ITEM threshold raised 1 -> 2 (two declarers invisible)  # predict K
@old ((hits > 1)) && defect "DUPLICATE-ITEM
@new ((hits > 2)) && defect "DUPLICATE-ITEM
#
@defect D1 | floor_of truncates instead of ceiling (odd item counts)  # predict S (hole)
@old floor_of() { printf '%s' "$(((($1 + FLOOR_DEN - 1)) / FLOOR_DEN))"; }
@new floor_of() { printf '%s' "$((($1) / FLOOR_DEN))"; }
#
@defect D2 | ratio denominator 2 -> 1 (floor = every item)  # predict K
@old FLOOR_DEN=2   # floor = ceil(items / FLOOR_DEN)
@new FLOOR_DEN=1   # floor = ceil(items / FLOOR_DEN)
#
@defect E1 | exit-set membership becomes exact equality (A|B arms never accepted)  # predict K
@old       [[ "|$want|" == *"|$rc|"* ]] || {
@new       [[ "$want" == "$rc" ]] || {
#
@defect E2 | row output captured without stderr (2>&1 dropped)  # predict S (hole)
@old     out=$(cd "$ROOT" && timeout "$ROW_TIMEOUT" bash -c "${R_CHECK[$i]}" 2>&1) || rc=$?
@new     out=$(cd "$ROOT" && timeout "$ROW_TIMEOUT" bash -c "${R_CHECK[$i]}") || rc=$?
#
@defect F1 | defect path returns 0 — BROKEN still exits 0  # predict K
@old     return 1\n  fi\n  if [[ -n "$ONLY" ]]; then\n    printf 'CHECKLIST_ROW: CLEAN
@new     return 0\n  fi\n  if [[ -n "$ONLY" ]]; then\n    printf 'CHECKLIST_ROW: CLEAN
#
@defect F2 | --only BROKEN line prints failed=0  # predict S (hole)
@old printf 'CHECKLIST_ROW: BROKEN (id=%s failed=%s — this is a single row, not the checklist)\\n' "$ONLY" "$failed"
@new printf 'CHECKLIST_ROW: BROKEN (id=%s failed=0 — this is a single row, not the checklist)\\n' "$ONLY" "$failed"
#
@defect G1 | unknown argument fail-open — exit 2 -> 0  # predict S (hole)
@old     *) printf 'checklist-run: unknown argument: %s\\n' "$1" >&2; exit 2 ;;
@new     *) printf 'checklist-run: unknown argument: %s\\n' "$1" >&2; exit 0 ;;
EOT
  # r10-2 leg 6: kumitate scripts/claims-check.mjs @ 175de6b (pin e9a21b44…),
  # recorded 7/10 killed; the recorded T8-2 spec file verbatim
  # (/tmp/w8-t8-2-claims/spec/claims-check.defects.spec), every @old
  # re-verified count==1 against the pinned blob.
  cat >"$d/js-claims-check.spec" <<'EOT'
# T8-2 mutation spec — kumitate scripts/claims-check.mjs @ e9a21b44… (git blob fae4bbc… @ 175de6b)
# Sites < 470 (chain) sit under the first @defect's group headers; each @old asserted count==1 by t8_2_check.py.

@defect D1 | verdict token: MATCH -> OK on the CLAIMS verdict line (row A)
@old `CLAIMS: MATCH (rows=${totals.rows}
@new `CLAIMS: OK (rows=${totals.rows}

@defect D2 | exit map: DRIFT path returns 0
@old return verdict === 'MATCH' ? 0 : 1;
@new return 0;

@defect D3 | predicate: warnings are always drift (the --strict promotion dropped)
@old drift: errors > 0 || (Boolean(strict) && warnings > 0)
@new drift: errors > 0 || warnings > 0

@defect D4 | boundary: NOTE_AMBIGUOUS threshold 2 hits -> 3
@old else if (hits.length > 1 &&
@new else if (hits.length > 2 &&

@defect D5 | inverted condition: a live anchor now requires blank endpoints
@old && lines[a - 1].trim() !== '' && lines[b - 1].trim() !== '');
@new && lines[a - 1].trim() === '' && lines[b - 1].trim() === '');

@defect D6 | reported field: JSON schema id swapped
@old schema: CONTRACT, contract: CONTRACT,
@new schema: 'claims-check-v0', contract: CONTRACT,

@defect D7 | cap unreached: DRIFT finding cap 6 -> 5
@old shown.slice(0, 6)
@new shown.slice(0, 5)

@defect D8 | threshold unasserted: symbol floor 3 -> 2 chars
@old && t.length >= 3);
@new && t.length >= 2);

@defect D9 | unreached arm: a covered cell with only prose parts no longer errors
@old && claimed.length + explicit.length + unresolved.length === 0) {
@new && claimed.length + explicit.length === 0) {

@defect D10 | candidate order swapped (case name claims it, assert cannot see it)
@old join(homedir(), 'Projects', 'ufo-fsd-alpha'),\n  join(homedir(), 'Projects', 'origin-work', 'ufo-fsd-alpha'),
@new join(homedir(), 'Projects', 'origin-work', 'ufo-fsd-alpha'),\n  join(homedir(), 'Projects', 'ufo-fsd-alpha'),
EOT
  [[ -s "$d/js-kimi-census.spec" && -s "$d/bash-surface-census.spec" \
     && -s "$d/bash-tsukuroi-census.spec" && -s "$d/bash-mado-verify.spec" \
     && -s "$d/bash-checklist-run.spec" && -s "$d/js-claims-check.spec" ]]
}

regression_case() {
  # <name> <target> <pin-sha> <spec> <suite> <recorded-table> <case-workdir>
  #   [<repo> <rev> <path-in-repo>] [<killed-tol> <flips-tol>]
  # When <repo>/<rev>/<path> are given (r7-1), the target is NOT the file at
  # <target>: the pinned blob is materialized from that repo's git object store
  # (`git show <rev>:<path>`) into <case-workdir>/target.<basename> and every
  # check below reads the materialized copy, so a drifted or dirty working tree
  # cannot move the replay. A drifted tree cannot move it; r10-2 also mirrors
  # the blob's mode (100755 -> +x) because `git show` does not carry it and a
  # gate that re-execs itself needs the recorded exec bit. Without <repo> etc.
  # the target is used as given (fixture mode). Tolerance defaults to the r4-2
  # band (BAND_KILLED / BAND_FLIPS); the ledger legs pass 0 0 (exact: every
  # measured row must equal the recorded table). Fresh sweep of <spec> against
  # the target through this same tool (a full CLI sub-invocation), then a
  # comparison of the measured verdict table against the recorded table within
  # the stated tolerance. Writes <case-workdir>/sweep.log. Returns 0 PASS · 1
  # FAIL (outside the expectation) · 2 SETUP (cannot verify).
  local name=$1 target=$2 pin=$3 spec=$4 suite=$5 table=$6 cwd=$7
  local repo=${8-} rev=${9-} path=${10-} ktol=${11-} ftol=${12-}
  [[ -n "$ktol" ]] || ktol=$BAND_KILLED
  [[ -n "$ftol" ]] || ftol=$BAND_FLIPS
  mkdir -p "$cwd" || {
    printf 'REGRESSION_CASE %s: SETUP (cannot create case workdir: %s)\n' "$name" "$cwd"
    return 2
  }
  if [[ -n "$repo" ]]; then
    command -v git >/dev/null 2>&1 || {
      printf 'REGRESSION_CASE %s: SETUP (git missing; cannot materialize the pinned revision)\n' "$name"
      return 2
    }
    if ! git -C "$repo" rev-parse --verify --quiet "${rev}^{commit}" >/dev/null; then
      printf 'REGRESSION_CASE %s: SETUP (revision not found: %s@%s)\n' "$name" "$repo" "$rev"
      return 2
    fi
    if ! git -C "$repo" cat-file -e "${rev}:${path}" 2>/dev/null; then
      printf 'REGRESSION_CASE %s: SETUP (path not in revision: %s@%s:%s)\n' "$name" "$repo" "$rev" "$path"
      return 2
    fi
    local dst="$cwd/target.$(basename "$path")" blob_mode
    if ! git -C "$repo" show "${rev}:${path}" >"$dst" 2>"$cwd/git-show.err"; then
      printf 'REGRESSION_CASE %s: SETUP (git show failed: %s@%s:%s; see %s)\n' \
        "$name" "$repo" "$rev" "$path" "$cwd/git-show.err"
      return 2
    fi
    # r10-2: `git show > file` writes the bytes but not the blob's mode. A leg
    # whose gate re-execs itself (checklist-run.sh's selftest runs "$SELF")
    # needs the recorded exec bit, so mirror it from the blob: 100755 -> +x,
    # 100644 stays as written. Bytes (and thus the pin check) are unaffected.
    if ! blob_mode=$(git -C "$repo" ls-tree "$rev" -- "$path" | awk '{print $1}'); then
      printf 'REGRESSION_CASE %s: SETUP (cannot read the blob mode: %s@%s:%s)\n' \
        "$name" "$repo" "$rev" "$path"
      return 2
    fi
    if [[ -z "$blob_mode" ]]; then
      printf 'REGRESSION_CASE %s: SETUP (empty blob mode: %s@%s:%s)\n' \
        "$name" "$repo" "$rev" "$path"
      return 2
    fi
    if [[ "$blob_mode" == 100755 ]]; then
      chmod +x "$dst" || {
        printf 'REGRESSION_CASE %s: SETUP (cannot restore the exec bit on %s)\n' "$name" "$dst"
        return 2
      }
    fi
    target=$dst
    printf 'REGRESSION_PIN %s: source=git repo=%s rev=%s path=%s mode=%s sha256=%s\n' \
      "$name" "$repo" "$rev" "$path" "$blob_mode" "$pin"
  else
    printf 'REGRESSION_PIN %s: source=file target=%s sha256=%s\n' "$name" "$target" "$pin"
  fi
  local tsha
  if [[ ! -f "$target" ]]; then
    printf 'REGRESSION_CASE %s: SETUP (target missing: %s)\n' "$name" "$target"
    return 2
  fi
  tsha=$(sha_of "$target")
  if [[ "$tsha" != "$pin" ]]; then
    printf 'REGRESSION_CASE %s: SETUP (pin mismatch: recorded=%s materialized=%s source=%s)\n' \
      "$name" "$pin" "$tsha" "$target"
    return 2
  fi

  local rc
  bash "$SELF" --target "$target" --defects "$spec" --suite "$suite" \
    --workdir "$cwd" --label "$name" --timeout "$TIMEOUT_S" --tail "$TAIL_N" \
    >"$cwd/sweep.log" 2>&1
  rc=$?
  printf 'REGRESSION_SWEEP %s: %s\n' "$name" \
    "$(grep -m1 '^MUTATE: ' "$cwd/sweep.log" || printf 'no MUTATE line (sweep exit=%s)' "$rc")"
  if [[ $rc -eq 2 ]]; then
    printf 'REGRESSION_CASE %s: SETUP (sweep refused; log: %s)\n' "$name" "$cwd/sweep.log"
    return 2
  fi
  if [[ $rc -ne 0 && $rc -ne 1 ]]; then
    printf 'REGRESSION_CASE %s: FAIL (sweep exit=%s, expected 0 or 1; log: %s)\n' \
      "$name" "$rc" "$cwd/sweep.log"
    return 1
  fi
  local rtsv="$cwd/results.tsv"
  if [[ ! -f "$rtsv" ]]; then
    printf 'REGRESSION_CASE %s: FAIL (no results table; sweep exit=%s; log: %s)\n' \
      "$name" "$rc" "$cwd/sweep.log"
    return 1
  fi

  local id v rest want seen='' total=0 killed=0 survived=0 inconcl=0 flips=0 matches=0
  local diffs='' pair eid
  while IFS=$'\t' read -r id v rest; do
    [[ -n "$id" ]] || continue
    [[ "$id" == 'id' && "$v" == 'verdict' ]] && continue   # results.tsv header row
    total=$((total + 1))
    seen="$seen $id"
    case $v in
      KILLED) killed=$((killed + 1)) ;;
      SURVIVED) survived=$((survived + 1)) ;;
      *) inconcl=$((inconcl + 1)) ;;
    esac
    want=$(table_lookup "$table" "$id")
    if [[ "$want" == '-' ]]; then
      flips=$((flips + 1))
      diffs+="REGRESSION_DEFECT $name $id: measured=$v recorded=ABSENT"$'\n'
    elif [[ "$want" != "$v" ]]; then
      flips=$((flips + 1))
      diffs+="REGRESSION_DEFECT $name $id: measured=$v recorded=$want"$'\n'
    else
      matches=$((matches + 1))
    fi
  done <"$rtsv"
  for pair in ${table//,/ }; do
    eid=${pair%%:*}
    case " $seen " in
      *" $eid "*) ;;
      *)
        flips=$((flips + 1))
        diffs+="REGRESSION_DEFECT $name $eid: measured=ABSENT recorded=${pair#*:}"$'\n'
        ;;
    esac
  done

  local exp_total exp_killed ctl=0 restore=0
  exp_total=$(table_total "$table")
  exp_killed=$(table_count "$table" KILLED)
  grep -q '^CONTROL: GREEN ' "$cwd/sweep.log" && ctl=1
  grep -q '^MUTATE_RESTORE: OK ' "$cwd/sweep.log" && restore=1

  local delta=$((killed - exp_killed)) reasons=''
  [[ $delta -lt 0 ]] && delta=$((0 - delta))
  (( delta > ktol )) && reasons="$reasons killed-delta=$delta"
  (( flips > ftol )) && reasons="$reasons flips=$flips"
  (( inconcl > 0 )) && reasons="$reasons inconclusive=$inconcl"
  (( total != exp_total )) && reasons="$reasons defects=$total-recorded=$exp_total"
  [[ $ctl -eq 1 ]] || reasons="$reasons control-not-green"
  [[ $restore -eq 1 ]] || reasons="$reasons restore-not-ok"

  [[ -n "$diffs" ]] && printf '%s' "$diffs"
  printf 'REGRESSION_TABLE %s: match=%s/%s recorded-killed=%s measured-killed=%s survived=%s inconclusive=%s flips=%s\n' \
    "$name" "$matches" "$exp_total" "$exp_killed" "$killed" "$survived" "$inconcl" "$flips"
  printf 'REGRESSION_WORKDIR %s: %s\n' "$name" "$cwd"
  if [[ -z "$reasons" ]]; then
    printf 'REGRESSION_CASE %s: PASS (band: killed-delta<=%s flips<=%s inconclusive=0 defects=%s)\n' \
      "$name" "$ktol" "$ftol" "$exp_total"
    return 0
  fi
  printf 'REGRESSION_CASE %s: FAIL (out of band:%s; log: %s)\n' "$name" "$reasons" "$cwd/sweep.log"
  return 1
}

regression_case_git() {
  # <name> <fleet-relative-target> <pin> <rev> <spec> <suite> <recorded-table>
  #   <case-workdir>
  # Ledger leg (r7-1): repo = the target's top-level directory under FLEET_ROOT,
  # path = the rest of the fleet-relative path. The leg replays at its recorded
  # pin with an exact expectation (killed-delta 0 / flips 0) — a byte-pinned
  # replay admits no drift.
  local name=$1 rel=$2 pin=$3 rev=$4 spec=$5 suite=$6 table=$7 cwd=$8
  local repo="$FLEET_ROOT/${rel%%/*}" path="${rel#*/}"
  regression_case "$name" "$FLEET_ROOT/$rel" "$pin" "$spec" "$suite" "$table" "$cwd" \
    "$repo" "$rev" "$path" 0 0
}

run_regression() {
  if [[ -n "$TARGET$SPEC$SUITE$LABEL" ]]; then
    usage_exit '--regression takes no --target/--defects/--suite/--label'
  fi
  (( TIMEOUT_S > 0 )) || usage_exit '--timeout must be a positive integer'
  (( TAIL_N > 0 )) || usage_exit '--tail must be a positive integer'
  command -v python3 >/dev/null 2>&1 || die_setup 'python3 missing'
  command -v sha256sum >/dev/null 2>&1 || die_setup 'sha256sum missing'
  command -v mktemp >/dev/null 2>&1 || die_setup 'mktemp missing'
  command -v git >/dev/null 2>&1 \
    || die_setup 'git missing (--regression materializes each leg from its repo object store)'

  local root specs auto=0
  FLEET_ROOT=$(dirname "$(dirname "$(dirname "$SELF")")")
  if [[ -z "$WORKDIR" ]]; then
    root=$(mktemp -d /tmp/tameshi-r4-2-regression.XXXXXX) || die_setup 'mktemp -d failed'
    auto=1
  else
    root=$WORKDIR
    mkdir -p "$root" || die_setup "cannot create workdir: $root"
  fi
  specs="$root/specs"
  mkdir -p "$specs" || die_setup "cannot create specs dir: $specs"
  regression_specs "$specs" || die_setup 'cannot write the embedded case specs'

  printf 'REGRESSION_TOOL: %s sha256=%s\n' "$SELF" "$(sha_of "$SELF")"
  printf 'REGRESSION_DATE: %s\n' "$(date -u +%Y-%m-%dT%H:%M:%SZ)"
  printf 'REGRESSION_BAND: ledger legs exact (killed-delta<=0 flips<=0 inconclusive=0 defects=exact); fixture-mode default killed-delta<=%s flips<=%s\n' \
    "$BAND_KILLED" "$BAND_FLIPS"
  printf 'REGRESSION_EXPECT: recorded kill-rates — js-kimi-census=%s/%s bash-surface-census=%s/%s bash-tsukuroi-census=%s/%s bash-mado-verify=%s/%s bash-checklist-run=%s/%s js-claims-check=%s/%s\n' \
    "$(table_count "$TABLE_JS" KILLED)" "$(table_total "$TABLE_JS")" \
    "$(table_count "$TABLE_BASH" KILLED)" "$(table_total "$TABLE_BASH")" \
    "$(table_count "$TABLE_TSUKUROI" KILLED)" "$(table_total "$TABLE_TSUKUROI")" \
    "$(table_count "$TABLE_MADO" KILLED)" "$(table_total "$TABLE_MADO")" \
    "$(table_count "$TABLE_CHECKLIST" KILLED)" "$(table_total "$TABLE_CHECKLIST")" \
    "$(table_count "$TABLE_CLAIMS" KILLED)" "$(table_total "$TABLE_CLAIMS")"

  local st_js st_kagi st_tsu st_mado st_checklist st_claims
  regression_case_git js-kimi-census \
    'kumitate-shokunin/scripts/kimi-census.mjs' "$PIN_JS" "$REV_JS" \
    "$specs/js-kimi-census.spec" 'node "$MUTANT" --selftest' "$TABLE_JS" \
    "$root/js-kimi-census"
  st_js=$?
  regression_case_git bash-surface-census \
    'kagi-shokunin/corpus/surface-census.sh' "$PIN_BASH" "$REV_BASH" \
    "$specs/bash-surface-census.spec" 'bash "$MUTANT" --selftest' "$TABLE_BASH" \
    "$root/bash-surface-census"
  st_kagi=$?
  regression_case_git bash-tsukuroi-census \
    'tsukuroi-shokunin/tools/tsukuroi-census.sh' "$PIN_TSUKUROI" "$REV_TSUKUROI" \
    "$specs/bash-tsukuroi-census.spec" 'bash "$MUTANT" --selftest' "$TABLE_TSUKUROI" \
    "$root/bash-tsukuroi-census"
  st_tsu=$?
  regression_case_git bash-mado-verify \
    'mado-shokunin/tools/mado-verify.sh' "$PIN_MADO" "$REV_MADO" \
    "$specs/bash-mado-verify.spec" 'bash "$MUTANT" --selftest' "$TABLE_MADO" \
    "$root/bash-mado-verify"
  st_mado=$?
  regression_case_git bash-checklist-run \
    'kagi-shokunin/corpus/checklist-run.sh' "$PIN_CHECKLIST" "$REV_CHECKLIST" \
    "$specs/bash-checklist-run.spec" 'bash "$MUTANT" --selftest' "$TABLE_CHECKLIST" \
    "$root/bash-checklist-run"
  st_checklist=$?
  regression_case_git js-claims-check \
    'kumitate-shokunin/scripts/claims-check.mjs' "$PIN_CLAIMS" "$REV_CLAIMS" \
    "$specs/js-claims-check.spec" 'node "$MUTANT" --selftest' "$TABLE_CLAIMS" \
    "$root/js-claims-check"
  st_claims=$?

  local nlegs=6 npass=0 nfail=0 nsetup=0 st
  for st in "$st_js" "$st_kagi" "$st_tsu" "$st_mado" "$st_checklist" "$st_claims"; do
    case $st in
      0) npass=$((npass + 1)) ;;
      1) nfail=$((nfail + 1)) ;;
      *) nsetup=$((nsetup + 1)) ;;
    esac
  done

  if [[ $nfail -gt 0 ]]; then
    printf 'REGRESSION: FAIL (cases=%s passed=%s failed=%s setup=%s)\n' \
      "$nlegs" "$npass" "$nfail" "$nsetup"
    printf 'REGRESSION_WORKDIR: %s (kept)\n' "$root"
    exit 1
  fi
  if [[ $nsetup -gt 0 ]]; then
    printf 'REGRESSION: SETUP (cases=%s passed=%s cannot-verify=%s)\n' \
      "$nlegs" "$npass" "$nsetup"
    printf 'REGRESSION_WORKDIR: %s (kept)\n' "$root"
    exit 2
  fi
  printf 'REGRESSION: PASS (cases=%s passed=%s; ledger legs exact: killed-delta<=0 flips<=0)\n' \
    "$nlegs" "$npass"
  if [[ $auto -eq 1 && $KEEP -eq 0 ]]; then
    printf 'REGRESSION_WORKDIR: %s (removed on PASS; --keep retains)\n' "$root"
    rm -rf "$root"
  else
    printf 'REGRESSION_WORKDIR: %s (kept)\n' "$root"
  fi
  exit 0
}

# ------------------------------------------------------------------ selftest

selftest() {
  local root
  root=$(mktemp -d /tmp/tameshi-r4-2-selftest.XXXXXX) || {
    printf 'MUTATE_SELFTEST: 0/1 pass\nVERDICT: FAIL (mktemp)\n'
    exit 1
  }
  local cases=0 failed=0
  st() { # st <name> <rc>
    cases=$((cases + 1))
    if [[ "$2" -eq 0 ]]; then
      printf 'PASS %s\n' "$1"
    else
      printf 'FAIL %s\n' "$1"
      failed=$((failed + 1))
    fi
  }

  local fx="$root/fixture"
  mkdir -p "$fx"

  cat >"$fx/target.sh" <<'EOT'
#!/usr/bin/env bash
# tiny fixture target — mutate-and-run.sh --selftest (never a live path)
banner() { printf 'fixture-target v1\n'; }
say_hello() { printf 'hello %s\n' "$1"; }
add() { printf '%s\n' "$(( $1 + $2 ))"; }
case "${1:-banner}" in
  banner) banner ;;
  hello) say_hello "${2:-world}" ;;
  add) add "${2:-0}" "${3:-0}" ;;
  *) banner ;;
esac
EOT
  chmod +x "$fx/target.sh"

  cat >"$fx/suite.sh" <<'EOT'
#!/usr/bin/env bash
# tiny mini-suite for the fixture target; $1 = path under test
set -u
t=${1:?suite: target path required}
cases=0; fails=0
chk() { cases=$((cases+1)); if [[ "$2" != "$3" ]]; then fails=$((fails+1)); printf 'FIXTURE FAIL %s: expected %q got %q\n' "$1" "$2" "$3"; fi; }
chk 'add(2,2)' 4 "$(bash "$t" add 2 2)"
chk 'add(1,4)' 5 "$(bash "$t" add 1 4)"
chk 'hello world' 'hello world' "$(bash "$t" hello world)"
chk 'hello kimi' 'hello kimi' "$(bash "$t" hello kimi)"
if [[ $fails -eq 0 ]]; then
  printf 'FIXTURE_SELFTEST: %s/%s pass\nVERDICT: PASS\n' "$cases" "$cases"; exit 0
fi
printf 'FIXTURE_SELFTEST: %s/%s pass\nVERDICT: FAIL\n' "$((cases-fails))" "$cases"; exit 1
EOT
  chmod +x "$fx/suite.sh"

  # hangs only when the add() operator mutant is present (its grep misses the
  # pristine); used to exercise the timeout -> INCONCLUSIVE -> DEGRADED path.
  cat >"$fx/suite-hang.sh" <<'EOT'
#!/usr/bin/env bash
if grep -qF -- '- $2' "$MUTANT"; then sleep 30; fi
exit 0
EOT
  chmod +x "$fx/suite-hang.sh"

  cat >"$fx/spec-ok.spec" <<'EOT'
# selftest spec — one mutant the mini-suite must catch, one it must not see
@defect K | mini-suite catches: add() operator + flipped to -
@old $(( $1 + $2 ))
@new $(( $1 - $2 ))
@defect S | survives: banner version string is reported, never asserted
@old fixture-target v1
@new fixture-target v2
EOT

  cat >"$fx/spec-dup.spec" <<'EOT'
# selftest spec — old string occurs twice: refuse before any suite run
@defect B | duplicate old string must refuse
@old say_hello
@new say_hello2
EOT

  cat >"$fx/spec-escape.spec" <<'EOT'
# selftest spec — unknown escape must refuse
@defect X | bad escape
@old \q
@new z
EOT

  cat >"$fx/spec-noop.spec" <<'EOT'
# selftest spec — new equals old must refuse
@defect N | no-op edit
@old add
@new add
EOT

  local s_before s_after rc1 rc2 rc3 rc4 rc5
  s_before=$(sha_of "$fx/target.sh")

  local suite_good suite_hang
  suite_good="bash '$fx/suite.sh' \"\$MUTANT\""
  suite_hang="bash '$fx/suite-hang.sh' \"\$MUTANT\""
  local out1="$root/run1.out" out2="$root/run2.out" out3="$root/run3.out" out4="$root/run4.out" out5="$root/run5.out"

  bash "$SELF" --target "$fx/target.sh" --defects "$fx/spec-ok.spec" \
    --suite "$suite_good" --workdir "$root/run1" --label fixture --tail 5 --timeout 30 >"$out1" 2>&1
  rc1=$?
  s_after=$(sha_of "$fx/target.sh")

  [[ $rc1 -eq 0 ]]; st 'sweep exits 0' $?
  grep -q '^CONTROL: GREEN (exit=0' "$out1"; st 'control green on pristine' $?
  grep -q '^DEFECT K: KILLED (exit=1' "$out1"; st 'kill classified (K)' $?
  grep -q '^DEFECT S: SURVIVED (exit=0' "$out1"; st 'survivor classified (S)' $?
  grep -q 'FIXTURE FAIL add(2,2)' "$out1"; st 'kill tail shows the failing case' $?
  grep -qxF 'MUTATE: DONE (target=fixture defects=2 killed=1 survived=1 inconclusive=0 kill-rate=50%)' "$out1"; st 'kill-rate summary exact' $?
  grep -q '^MUTATE_RESTORE: OK ' "$out1"; st 'restore line OK' $?
  [[ "$s_before" == "$s_after" ]]; st 'fixture target byte-identical after sweep' $?
  [[ $(wc -l < "$root/run1/results.tsv") -eq 3 ]]; st 'results.tsv = header + one row per defect' $?

  bash "$SELF" --target "$fx/target.sh" --defects "$fx/spec-dup.spec" \
    --suite "$suite_good" --workdir "$root/run2" --timeout 30 >"$out2" 2>&1
  rc2=$?
  local exp_dup
  exp_dup=$(grep -cF 'say_hello' "$fx/target.sh")
  [[ $rc2 -eq 2 ]]; st 'duplicate old string refuses (exit 2)' $?
  grep -q 'APPLY FAIL id=B ' "$out2"; st 'refusal names the defect' $?
  grep -q "old-string-count=$exp_dup expected=1" "$out2"; st 'refusal reports the old-string count' $?
  grep -q '^MUTATE: SETUP ' "$out2"; st 'refusal is a SETUP verdict' $?
  if grep -q '^CONTROL:' "$out2" || grep -q '^DEFECT B:' "$out2"; then
    st 'no suite run before refusal' 1
  else
    st 'no suite run before refusal' 0
  fi

  bash "$SELF" --target "$fx/target.sh" --defects "$fx/spec-escape.spec" \
    --suite "$suite_good" --workdir "$root/run3" --timeout 30 >"$out3" 2>&1
  rc3=$?
  [[ $rc3 -eq 2 ]]; st 'unknown escape refuses (exit 2)' $?
  grep -q 'unknown escape' "$out3"; st 'unknown escape named' $?

  bash "$SELF" --target "$fx/target.sh" --defects "$fx/spec-noop.spec" \
    --suite "$suite_good" --workdir "$root/run4" --timeout 30 >"$out4" 2>&1
  rc4=$?
  [[ $rc4 -eq 2 ]]; st 'no-op edit refuses (exit 2)' $?
  grep -q 'no-op mutation' "$out4"; st 'no-op edit named' $?

  bash "$SELF" --target "$fx/target.sh" --defects "$fx/spec-ok.spec" \
    --suite "$suite_hang" --workdir "$root/run5" --label fixture --timeout 2 >"$out5" 2>&1
  rc5=$?
  [[ $rc5 -eq 1 ]]; st 'inconclusive run exits 1' $?
  grep -q '^DEFECT K: INCONCLUSIVE (exit=124 note=timeout' "$out5"; st 'timeout classified inconclusive' $?
  grep -q '^DEFECT S: SURVIVED (exit=0' "$out5"; st 'survivor still recorded under DEGRADED' $?
  grep -qxF 'MUTATE: DEGRADED (target=fixture defects=2 killed=0 survived=1 inconclusive=1 kill-rate=0%)' "$out5"; st 'degraded summary exact' $?

  # --regression engine on this fixture (the band is the one stated in the file
  # header): in-band PASS, doctored recorded-table FAIL, pin / target SETUP.
  local rg="$root/regression" st_rg
  regression_case fixture "$fx/target.sh" "$s_before" "$fx/spec-ok.spec" "$suite_good" \
    'K:KILLED,S:SURVIVED' "$rg/pass" >"$root/rg1.out" 2>&1
  st_rg=$?
  [[ $st_rg -eq 0 ]]; st 'regression engine passes an in-band fixture' $?
  grep -qF 'REGRESSION_CASE fixture: PASS (band: killed-delta<=1 flips<=1 inconclusive=0 defects=2)' "$root/rg1.out"
  st 'regression fixture PASS line exact' $?
  grep -qxF 'REGRESSION_TABLE fixture: match=2/2 recorded-killed=1 measured-killed=1 survived=1 inconclusive=0 flips=0' "$root/rg1.out"
  st 'regression fixture table line exact' $?

  regression_case fixture "$fx/target.sh" "$s_before" "$fx/spec-ok.spec" "$suite_good" \
    'K:SURVIVED,S:KILLED' "$rg/flip" >"$root/rg2.out" 2>&1
  st_rg=$?
  [[ $st_rg -eq 1 ]]; st 'regression engine fails a doctored table' $?
  grep -qF 'REGRESSION_DEFECT fixture K: measured=KILLED recorded=SURVIVED' "$root/rg2.out"
  st 'doctored table names K (measured vs recorded)' $?
  grep -qF 'REGRESSION_DEFECT fixture S: measured=SURVIVED recorded=KILLED' "$root/rg2.out"
  st 'doctored table names S (measured vs recorded)' $?
  grep -qF 'REGRESSION_CASE fixture: FAIL (out of band: flips=2' "$root/rg2.out"
  st 'out-of-band FAIL names flips=2' $?

  regression_case fixture "$fx/target.sh" 0000000000000000000000000000000000000000000000000000000000000000 \
    "$fx/spec-ok.spec" "$suite_good" 'K:KILLED,S:SURVIVED' "$rg/pin" >"$root/rg3.out" 2>&1
  st_rg=$?
  [[ $st_rg -eq 2 ]]; st 'regression pin mismatch is SETUP (exit 2)' $?
  grep -qF 'REGRESSION_CASE fixture: SETUP (pin mismatch:' "$root/rg3.out"
  st 'pin mismatch named' $?

  regression_case fixture "$root/no-such-target" "$s_before" "$fx/spec-ok.spec" "$suite_good" \
    'K:KILLED,S:SURVIVED' "$rg/missing" >"$root/rg4.out" 2>&1
  st_rg=$?
  [[ $st_rg -eq 2 ]]; st 'regression missing target is SETUP (exit 2)' $?
  grep -qF 'REGRESSION_CASE fixture: SETUP (target missing:' "$root/rg4.out"
  st 'missing target named' $?
  [[ "$(sha_of "$fx/target.sh")" == "$s_before" ]]; st 'fixture target byte-identical after regression fixture runs' $?

  # r6 (TAMESHI-T6-4) hardening — the r6 meta-sweep's survivor cases (mutants of
  # the comparator above; corpus/knowledge/self-hardening-r6.md §1-§3) pin the
  # band edges and accounting arms the r4-2 fixtures never exercised: in-band
  # boundary (killed-delta 1 / flips 1 still PASS), a recorded entry the
  # measurement lacks, a measured row the table lacks, a DEGRADED sub-sweep
  # (rc=1 is table-compared, not rejected), and a fully-matching all-killed
  # table (recorded-killed is read from the KILLED column).
  local suite_strict
  suite_strict="bash '$fx/suite-strict.sh' \"\$MUTANT\""
  cat >"$fx/suite-strict.sh" <<'EOT'
#!/usr/bin/env bash
# mini-suite variant: asserts both the add() result and the banner string
set -u
t=${1:?suite: target path required}
rc=0
bash "$t" add 2 2 | grep -qx 4 || rc=1
bash "$t" banner | grep -qx 'fixture-target v1' || rc=1
exit $rc
EOT
  chmod +x "$fx/suite-strict.sh"

  regression_case fixture "$fx/target.sh" "$s_before" "$fx/spec-ok.spec" "$suite_good" \
    'K:KILLED,S:KILLED' "$rg/edge" >"$root/rg5.out" 2>&1
  st_rg=$?
  [[ $st_rg -eq 0 ]]; st 'band edge (1 flip / killed-delta 1) still PASSes' $?
  grep -qF 'REGRESSION_CASE fixture: PASS (band: killed-delta<=1 flips<=1 inconclusive=0 defects=2)' "$root/rg5.out"
  st 'band-edge PASS line exact' $?
  grep -qxF 'REGRESSION_TABLE fixture: match=1/2 recorded-killed=2 measured-killed=1 survived=1 inconclusive=0 flips=1' "$root/rg5.out"
  st 'band-edge table line exact' $?

  regression_case fixture "$fx/target.sh" "$s_before" "$fx/spec-ok.spec" "$suite_good" \
    'K:KILLED,S:KILLED,Z:KILLED' "$rg/unmeasured" >"$root/rg6.out" 2>&1
  st_rg=$?
  [[ $st_rg -eq 1 ]]; st 'recorded entry the measurement lacks FAILs' $?
  grep -qF 'REGRESSION_DEFECT fixture Z: measured=ABSENT recorded=KILLED' "$root/rg6.out"
  st 'unmeasured recorded entry named (measured=ABSENT)' $?
  grep -qF 'REGRESSION_CASE fixture: FAIL (out of band: killed-delta=2 flips=2 defects=2-recorded=3;' "$root/rg6.out"
  st 'unmeasured-entry FAIL line exact' $?

  regression_case fixture "$fx/target.sh" "$s_before" "$fx/spec-ok.spec" "$suite_good" \
    'K:KILLED' "$rg/unrecorded" >"$root/rg7.out" 2>&1
  st_rg=$?
  [[ $st_rg -eq 1 ]]; st 'measured row the table lacks FAILs' $?
  grep -qF 'REGRESSION_DEFECT fixture S: measured=SURVIVED recorded=ABSENT' "$root/rg7.out"
  st 'unrecorded measured row named (recorded=ABSENT)' $?
  grep -qxF 'REGRESSION_TABLE fixture: match=1/1 recorded-killed=1 measured-killed=1 survived=1 inconclusive=0 flips=1' "$root/rg7.out"
  st 'unrecorded-row table line exact' $?
  grep -qF 'REGRESSION_CASE fixture: FAIL (out of band: defects=2-recorded=1;' "$root/rg7.out"
  st 'unrecorded-row FAIL line exact' $?

  local rg_timeout=$TIMEOUT_S
  TIMEOUT_S=2
  regression_case fixture "$fx/target.sh" "$s_before" "$fx/spec-ok.spec" "$suite_hang" \
    'K:KILLED,S:SURVIVED' "$rg/degraded" >"$root/rg8.out" 2>&1
  st_rg=$?
  TIMEOUT_S=$rg_timeout
  [[ $st_rg -eq 1 ]]; st 'DEGRADED sub-sweep (rc=1) is table-compared' $?
  grep -qF 'REGRESSION_DEFECT fixture K: measured=INCONCLUSIVE recorded=KILLED' "$root/rg8.out"
  st 'degraded sweep names the inconclusive row' $?
  grep -qF 'REGRESSION_CASE fixture: FAIL (out of band: inconclusive=1;' "$root/rg8.out"
  st 'degraded-sweep FAIL line names inconclusive=1' $?
  grep -qxF 'REGRESSION_TABLE fixture: match=1/2 recorded-killed=1 measured-killed=0 survived=1 inconclusive=1 flips=1' "$root/rg8.out"
  st 'degraded-sweep table line exact' $?

  regression_case fixture "$fx/target.sh" "$s_before" "$fx/spec-ok.spec" "$suite_strict" \
    'K:KILLED,S:KILLED' "$rg/all-killed" >"$root/rg9.out" 2>&1
  st_rg=$?
  [[ $st_rg -eq 0 ]]; st 'all-killed table (full match, zero flips) PASSes' $?
  grep -qxF 'REGRESSION_TABLE fixture: match=2/2 recorded-killed=2 measured-killed=2 survived=0 inconclusive=0 flips=0' "$root/rg9.out"
  st 'all-killed table line exact (recorded-killed=2)' $?
  grep -qF 'REGRESSION_CASE fixture: PASS (band: killed-delta<=1 flips<=1 inconclusive=0 defects=2)' "$root/rg9.out"
  st 'all-killed PASS line exact' $?
  [[ "$(sha_of "$fx/target.sh")" == "$s_before" ]]; st 'fixture target byte-identical after the r6 hardening cases' $?

  # r7-1 (TAMESHI-T7-1) ledger engine: a leg materialized from a git object
  # store reads the pinned blob, not the working tree (drift-immune), verifies
  # the blob against the pin, and carries an exact expectation — one flipped
  # entry of a recorded table fails loudly.
  local grepo="$root/fleet/fakerepo" grev saved_fleet
  mkdir -p "$grepo"
  cp "$fx/target.sh" "$grepo/target.sh"
  git -C "$grepo" init -q
  git -C "$grepo" add -A
  git -C "$grepo" -c user.name=tameshi -c user.email=tameshi@selftest -c commit.gpgsign=false \
    commit -q -m selftest-fixture
  grev=$(git -C "$grepo" rev-parse HEAD)
  saved_fleet=$FLEET_ROOT
  FLEET_ROOT="$root/fleet"

  regression_case_git fixture-git fakerepo/target.sh "$s_before" "$grev" \
    "$fx/spec-ok.spec" "$suite_good" 'K:KILLED,S:SURVIVED' "$rg/git-pass" >"$root/rg10.out" 2>&1
  st_rg=$?
  [[ $st_rg -eq 0 ]]; st 'ledger leg: git-materialized replay PASSes at exact tolerance' $?
  grep -qF 'REGRESSION_PIN fixture-git: source=git' "$root/rg10.out"
  st 'ledger leg pin line names the git source' $?
  grep -qF 'REGRESSION_CASE fixture-git: PASS (band: killed-delta<=0 flips<=0 inconclusive=0 defects=2)' "$root/rg10.out"
  st 'ledger leg PASS line shows the exact tolerance' $?

  printf '# working-tree drift after the pin\n' >>"$grepo/target.sh"
  regression_case_git fixture-git fakerepo/target.sh "$s_before" "$grev" \
    "$fx/spec-ok.spec" "$suite_good" 'K:KILLED,S:SURVIVED' "$rg/git-drift" >"$root/rg11.out" 2>&1
  st_rg=$?
  [[ $st_rg -eq 0 ]]; st 'drifted working tree does not move a git-pinned leg' $?
  grep -qF "sha256=$s_before" "$rg/git-drift/sweep.log"
  st 'drifted leg swept the pinned blob bytes (not the tree)' $?

  regression_case_git fixture-git fakerepo/target.sh \
    0000000000000000000000000000000000000000000000000000000000000000 "$grev" \
    "$fx/spec-ok.spec" "$suite_good" 'K:KILLED,S:SURVIVED' "$rg/git-pin" >"$root/rg12.out" 2>&1
  st_rg=$?
  [[ $st_rg -eq 2 ]]; st 'ledger leg pin mismatch is SETUP (exit 2)' $?
  grep -qF 'REGRESSION_CASE fixture-git: SETUP (pin mismatch:' "$root/rg12.out"
  st 'ledger leg pin mismatch named' $?

  regression_case_git fixture-git fakerepo/target.sh "$s_before" \
    0000000000000000000000000000000000000000 \
    "$fx/spec-ok.spec" "$suite_good" 'K:KILLED,S:SURVIVED' "$rg/git-rev" >"$root/rg13.out" 2>&1
  st_rg=$?
  [[ $st_rg -eq 2 ]]; st 'ledger leg unresolvable revision is SETUP (exit 2)' $?
  grep -qF 'REGRESSION_CASE fixture-git: SETUP (revision not found:' "$root/rg13.out"
  st 'ledger leg missing revision named' $?

  # r10-2 (TAMESHI-T10-2) exec-bit mirror: a gate whose selftest re-execs
  # itself needs the blob's mode, which `git show` does not carry — the leg
  # engine mirrors 100755 -> +x. One arm proves a self-exec leg runs (its
  # suite invokes "$MUTANT" directly); the counter-arm commits the same bytes
  # as 100644 and proves the direct invocation is refused (control red, exit
  # 126, sweep SETUP) — so the mirror cannot silently regress to a no-op.
  cat >"$grepo/exec.sh" <<'EOT'
#!/usr/bin/env bash
# self-exec fixture: the suite runs this file directly (needs the exec bit);
# the checked literal lives in MAGIC so the K edit (the grep target) and the
# S edit (the printed banner) each stay single-occurrence and non-vacuous.
MAGIC='exec-fixture v1'
[[ "${1:-}" == --selftest ]] || exit 1
grep -qF "$MAGIC" "$0" || exit 1
printf 'EXEC_FIXTURE: PASS\n'
exit 0
EOT
  chmod +x "$grepo/exec.sh"
  git -C "$grepo" add exec.sh
  git -C "$grepo" -c user.name=tameshi -c user.email=tameshi@selftest -c commit.gpgsign=false \
    commit -q -m selftest-fixture-exec
  local grev_exec exec_sha
  grev_exec=$(git -C "$grepo" rev-parse HEAD)
  exec_sha=$(git -C "$grepo" show "$grev_exec:exec.sh" | sha256sum | cut -d' ' -f1)
  cat >"$fx/exec.spec" <<'EOT'
@defect K | the self-check now greps the empty file (exit 1)
@old grep -qF "$MAGIC" "$0" || exit 1
@new grep -qF "$MAGIC" /dev/null || exit 1
@defect S | the PASS line is renamed, nothing asserts it
@old printf 'EXEC_FIXTURE: PASS\\n'
@new printf 'EXEC_FIXTURE: OK\\n'
EOT
  regression_case_git fixture-exec fakerepo/exec.sh "$exec_sha" "$grev_exec" \
    "$fx/exec.spec" '"$MUTANT" --selftest' 'K:KILLED,S:SURVIVED' "$rg/git-exec" >"$root/rg15.out" 2>&1
  st_rg=$?
  [[ $st_rg -eq 0 ]]; st 'ledger leg: exec bit mirrored (self-exec gate runs)' $?
  grep -qF 'mode=100755' "$root/rg15.out"
  st 'exec-bit leg pin line carries mode=100755' $?
  grep -qF 'REGRESSION_CASE fixture-exec: PASS' "$root/rg15.out"
  st 'exec-bit leg PASSes at the exact tolerance' $?

  cat >"$grepo/noexec.sh" <<'EOT'
#!/usr/bin/env bash
# self-exec fixture: the suite runs this file directly (needs the exec bit);
# the checked literal lives in MAGIC so the K edit (the grep target) and the
# S edit (the printed banner) each stay single-occurrence and non-vacuous.
MAGIC='exec-fixture v1'
[[ "${1:-}" == --selftest ]] || exit 1
grep -qF "$MAGIC" "$0" || exit 1
printf 'EXEC_FIXTURE: PASS\n'
exit 0
EOT
  chmod 644 "$grepo/noexec.sh"
  git -C "$grepo" add noexec.sh
  git -C "$grepo" -c user.name=tameshi -c user.email=tameshi@selftest -c commit.gpgsign=false \
    commit -q -m selftest-fixture-noexec
  local grev_noexec noexec_sha
  grev_noexec=$(git -C "$grepo" rev-parse HEAD)
  noexec_sha=$(git -C "$grepo" show "$grev_noexec:noexec.sh" | sha256sum | cut -d' ' -f1)
  regression_case_git fixture-noexec fakerepo/noexec.sh "$noexec_sha" "$grev_noexec" \
    "$fx/exec.spec" '"$MUTANT" --selftest' 'K:KILLED,S:SURVIVED' "$rg/git-noexec" >"$root/rg16.out" 2>&1
  st_rg=$?
  [[ $st_rg -eq 2 ]]; st 'no-exec blob invoked directly is SETUP (exit 2)' $?
  grep -qF 'mode=100644' "$root/rg16.out"
  st 'no-exec leg pin line carries mode=100644' $?
  grep -qF 'control run on the pristine copy is red (exit=126' "$rg/git-noexec/sweep.log"
  st 'no-exec leg refusal names the red control (exit=126)' $?

  FLEET_ROOT="$saved_fleet"
  regression_case fixture "$fx/target.sh" "$s_before" "$fx/spec-ok.spec" "$suite_good" \
    'K:KILLED,S:KILLED' "$rg/exact-flip" '' '' '' 0 0 >"$root/rg14.out" 2>&1
  st_rg=$?
  [[ $st_rg -eq 1 ]]; st 'exact expectation: one flipped entry FAILs loudly' $?
  grep -qF 'REGRESSION_DEFECT fixture S: measured=SURVIVED recorded=KILLED' "$root/rg14.out"
  st 'exact expectation flip names the flipped row' $?
  grep -qF 'REGRESSION_CASE fixture: FAIL (out of band: killed-delta=1 flips=1;' "$root/rg14.out"
  st 'exact expectation flip reports killed-delta=1 flips=1' $?

  # r10-2 (TAMESHI-T10-2) leg-cut resolution: the six embedded legs' specs and
  # recorded tables must agree with each other — parse OK, the table's ids are
  # exactly the spec's ids, and the recorded total / killed counts are the ones
  # the leg set carries. Hermetic: the specs come from this tool's own
  # regression_specs; no fleet path is read (count==1 against the pinned bytes
  # is asserted per leg at run time, by that leg's own sweep preparation).
  local lspecs="$root/ledger/specs" lent le lname lfile ltbl ltbl_val
  local ltot_exp lkill_exp le_ok lk_list lk_ids lk_tbl_ids
  mkdir -p "$lspecs"
  regression_specs "$lspecs" 2>"$root/ledger-specs.err"
  st 'embedded leg specs: six files written' $?
  lent=(
    'js-kimi-census:js-kimi-census.spec:TABLE_JS:10:8'
    'bash-surface-census:bash-surface-census.spec:TABLE_BASH:10:8'
    'bash-tsukuroi-census:bash-tsukuroi-census.spec:TABLE_TSUKUROI:10:6'
    'bash-mado-verify:bash-mado-verify.spec:TABLE_MADO:10:4'
    'bash-checklist-run:bash-checklist-run.spec:TABLE_CHECKLIST:15:7'
    'js-claims-check:js-claims-check.spec:TABLE_CLAIMS:10:7'
  )
  for le in "${lent[@]}"; do
    IFS=: read -r lname lfile ltbl ltot_exp lkill_exp <<<"$le"
    le_ok=1
    ltbl_val="${!ltbl}"
    if ! lk_list=$(py_helper list "$lspecs/$lfile" 2>&1); then
      le_ok=0
    fi
    if [[ $le_ok -eq 1 ]]; then
      lk_ids=$(printf '%s\n' "$lk_list" | cut -f1 | sort | tr '\n' ',')
      lk_tbl_ids=$(printf '%s\n' "${ltbl_val//,/ }" | tr ' ' '\n' | cut -d: -f1 | sort | tr '\n' ',')
      [[ "$lk_ids" == "$lk_tbl_ids" ]] || le_ok=0
      [[ "$(printf '%s\n' "$lk_list" | wc -l)" -eq "$ltot_exp" ]] || le_ok=0
      [[ "$(table_total "$ltbl_val")" -eq "$ltot_exp" ]] || le_ok=0
      [[ "$(table_count "$ltbl_val" KILLED)" -eq "$lkill_exp" ]] || le_ok=0
      [[ "$(table_count "$ltbl_val" SURVIVED)" -eq "$(( ltot_exp - lkill_exp ))" ]] || le_ok=0
    fi
    st "embedded leg $lname: spec and recorded table agree" "$(( 1 - le_ok ))"
  done

  bash "$SELF" --help >/dev/null 2>&1; [[ $? -eq 0 ]]; st 'help exits 0' $?
  bash "$SELF" --defects "$fx/spec-ok.spec" --suite true >/dev/null 2>&1; [[ $? -eq 64 ]]; st 'missing --target exits 64' $?
  bash "$SELF" --regression --target "$fx/target.sh" >/dev/null 2>&1; [[ $? -eq 64 ]]; st '--regression refuses --target (exit 64)' $?

  printf 'MUTATE_SELFTEST: %s/%s pass\n' "$((cases - failed))" "$cases"
  if [[ "$failed" -eq 0 ]]; then
    printf 'VERDICT: PASS\n'
    rm -rf "$root"
    exit 0
  fi
  printf 'VERDICT: FAIL (scratch kept: %s)\n' "$root"
  exit 1
}

# -------------------------------------------------------------------- main

while [[ $# -gt 0 ]]; do
  case "$1" in
    --target) need_val "$@"; TARGET=$2; shift 2 ;;
    --defects) need_val "$@"; SPEC=$2; shift 2 ;;
    --suite) need_val "$@"; SUITE=$2; shift 2 ;;
    --workdir) need_val "$@"; WORKDIR=$2; shift 2 ;;
    --label) need_val "$@"; LABEL=$2; shift 2 ;;
    --timeout) need_val "$@"; TIMEOUT_S=$2; shift 2 ;;
    --tail) need_val "$@"; TAIL_N=$2; shift 2 ;;
    --keep) KEEP=1; shift ;;
    --selftest) MODE=selftest; shift ;;
    --regression) MODE=regression; shift ;;
    --help | -h) MODE=help; shift ;;
    *) usage_exit "unknown argument: $1" ;;
  esac
done

case "$MODE" in
  help) usage; exit 0 ;;
  selftest) selftest ;;
  regression) run_regression ;;
  run) run_sweep ;;
esac
