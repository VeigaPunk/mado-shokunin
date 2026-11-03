#!/usr/bin/env bash
# R66ScribeLesson — read-only evidence receipt generator.
# Writes only scribe-evidence.txt in this seat directory. No git mutation, no host change.
set -u
LANE=/home/vgpnk/Projects/shokunin/mado-shokunin
SEAT=$LANE/.ufo/waves/round-66/w1/R66ScribeLesson
OUT=$SEAT/scribe-evidence.txt
: > "$OUT"

run() {
  local label=$1; shift
  printf '\n== %s ==\n$ %s\n' "$label" "$*" >>"$OUT"
  "$@" >>"$OUT" 2>&1
  local rc=$?
  printf 'rc=%d\n' "$rc" >>"$OUT"
  return 0
}

sh_run() {
  local label=$1 cmd=$2
  printf '\n== %s ==\n$ %s\n' "$label" "$cmd" >>"$OUT"
  bash -c "$cmd" >>"$OUT" 2>&1
  local rc=$?
  printf 'rc=%d\n' "$rc" >>"$OUT"
  return 0
}

printf 'mado round-66 R66ScribeLesson evidence — %s\n' "$(date -u +%Y-%m-%dT%H:%M:%SZ)" >>"$OUT"
printf 'lane=%s\n' "$LANE" >>"$OUT"

run "head" git -C "$LANE" rev-parse HEAD
run "freeze commit identity" git -C "$LANE" show -s --format='%H%n%cI%n%s' HEAD
run "wave registry and ready mtimes" stat -c '%n %y' "$LANE/.ufo/waves/round-66/w1.ready" "$LANE/.ufo/waves/round-66/w1/swarm-registry.json"
run "registry createdAt" python3 -c "import json;print(json.load(open('$LANE/.ufo/waves/round-66/w1/swarm-registry.json'))['createdAt'])"

printf '\n== SOURCES S028/S097 cell comparison (base vs r65 tip) ==\n' >>"$OUT"
python3 - "$LANE" >>"$OUT" 2>&1 <<'PY'
import subprocess, sys
lane = sys.argv[1]
BASE = "524fa1f90b1f2de44b3019bacf833d54e0af13a0"
TIP = "23fbc174d02fa44662e9aee735bbf6de5cad3f1d"
NAMES = ["id", "source", "kind", "tier", "scope", "anchor", "teaches", "status", "opened",
         "recheck", "used-by"]
def rows(rev):
    text = subprocess.check_output(["git", "-C", lane, "show", rev + ":corpus/SOURCES.md"], text=True)
    out = {}
    for line in text.splitlines():
        if not line.startswith("| S0"):
            continue
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if len(cells) == 11:
            out[cells[0]] = cells
    return out
b, t = rows(BASE), rows(TIP)
print("rev_base=%s rows=%d" % (BASE[:12], len(b)))
print("rev_tip =%s rows=%d" % (TIP[:12], len(t)))
print("rows_added=%s rows_removed=%s" % (sorted(set(t) - set(b)), sorted(set(b) - set(t))))
for sid in ("S028", "S097"):
    changed = [(NAMES[i], b[sid][i], t[sid][i]) for i in range(11) if b[sid][i] != t[sid][i]]
    print("%s changed_cells=%d %s" % (sid, len(changed), changed))
diffs = [sid for sid in b if sid in t and b[sid] != t[sid]]
print("all_changed_rows=%s" % diffs)
PY
printf 'rc=%d\n' "$?" >>"$OUT"

run "exact live CLEAN line" sed -n '65p' "$LANE/.ufo/waves/round-65/receipts/gate-live-r65.txt"
run "file-plane CLEAN line" sed -n '46p' "$LANE/.ufo/waves/round-65/receipts/gate-fileplane-r65.txt"
run "r65 forge summary lines" grep -nE 'FORGED_RC|MADO_R65_REGISTER: rows=8' "$LANE/.ufo/waves/round-65/w1/R65RevRegister/a3-forge-r65.txt"
run "r65 forge counter sha prefix" sha256sum "$LANE/.ufo/waves/round-65/w1/R65RevRegister/../R65ExecC1Counter/c1-r65-register.py"
run "r65 instrument mutant verdicts" python3 -c "import json;d=json.load(open('$LANE/.ufo/waves/round-65/w1/R65MutCounters/evidence/instr-mutants.json'));print({r['id']:(r['verdict'],r['summary']) for r in d['rows'] if r['id'] in ('I1','I7','I9','I8')})"
run "I1 GREEN-at-red-rev probe" grep -nE 'LANDING_LEG citecheck rc=0|MADO_LANDING_COUNTERS: GREEN' "$LANE/.ufo/waves/round-65/w1/R65MutCounters/evidence/probe-I1.log"
run "I7 r64-tree probe" grep -nE 'files=21 citations=18|MADO_CITECHECK' "$LANE/.ufo/waves/round-65/w1/R65MutCounters/evidence/probe-I7.log"
run "I9 usedby rc=2 inside RED" grep -nE 'LANDING_LEG usedby rc=2|MADO_LANDING_COUNTERS: RED' "$LANE/.ufo/waves/round-65/w1/R65MutCounters/evidence/probe-I9.log"
run "location-blind selftest" grep -nE 'SELFTEST ok 19|MADO_LANDING_COUNTERS_SELFTEST' "$LANE/.ufo/waves/round-65/w1/R65MutCounters/evidence/probe-location-blind.log"
run "S5 crash-as-red report line" grep -nE 'S5\. Red and crash|MADO_LANDING_COUNTERS: RED' "$LANE/.ufo/waves/round-65/w1/R65CriticInstrument/report.md"

run "C1 candidate selftest" sed -n '1,17p' "$LANE/.ufo/waves/round-66/w1/R66ExecRegister/selftest.txt"
run "C1 candidate genuine base" cat "$LANE/.ufo/waves/round-66/w1/R66ExecRegister/genuine-base.txt"
run "C1 candidate controls summary" python3 -c "import json;d=json.load(open('$LANE/.ufo/waves/round-66/w1/R66ExecRegister/controls.json'));print('correct=',d['correct']);print('base=',d['base'])"
run "C1 candidate sha" sha256sum "$LANE/.ufo/waves/round-66/w1/R66ExecRegister/c1-r66-register.py"

run "C2 landing selftest tail" tail -4 "$LANE/.ufo/waves/round-66/w1/R66ExecLanding/selftest.txt"
run "C2 landing candidate sha" sha256sum "$LANE/.ufo/waves/round-66/w1/R66ExecLanding/landing-counters.sh"
run "C2 landing selftest case count" grep -c '^SELFTEST ok ' "$LANE/.ufo/waves/round-66/w1/R66ExecLanding/selftest.txt"
run "C2 landing report SHA line" grep -n 'SHA256' "$LANE/.ufo/waves/round-66/w1/R66ExecLanding/report.md"
run "r65 committed counter sha" sha256sum "$LANE/quality/counters/c1-r65-register.py"
run "C2 driver baseline verdict" grep -nE 'selftest=0 landing=2|unknown argument: --round|TARGET_MISSED' "$LANE/.ufo/waves/round-66/w1/R66ExecDriver/report.md"
run "harness wave-root and seat sha" sha256sum "$LANE/.ufo/waves/round-66/check-controls.py" "$LANE/.ufo/waves/round-66/w1/R66ExecHarness/check-controls.py"
run "harness c1 candidate summary" cat "$LANE/.ufo/waves/round-66/w1/R66ExecHarness/evidence/final-c1-cand/r66harness/c1/summary.txt"
run "harness c2 candidate summary" cat "$LANE/.ufo/waves/round-66/w1/R66ExecHarness/evidence/final-c2-cand/r66harness/c2/summary.txt"
run "critic F1 lines" sed -n '35p;43p' "$LANE/.ufo/waves/round-66/w1/R66CriticLanding.md"
run "critic F2 line" sed -n '58p' "$LANE/.ufo/waves/round-66/w1/R66CriticLanding.md"
run "mutation kill denominators" grep -nE 'killed by the published|killed once|7/7 killed' "$LANE/.ufo/waves/round-66/w1/R66MutHardening.md"
run "evidence-scope absent at HEAD" bash -c "git -C '$LANE' cat-file -e HEAD:.ufo/waves/round-66/receipts/evidence-scope.txt 2>&1; echo cat-file-rc=\$?"
run "driver CLI options" grep -n 'add_argument' "$LANE/quality/counters/c2-r66-landing-instrument.py"
run "supporting quote word count" bash -c "printf '%s' 'If a command is not found, the child process created to execute it returns a status of 127.' | wc -w"
run "ledger child actual marker source" sed -n '368,371p' "$LANE/quality/check-tool-ledger.py"
run "ledger verdict at HEAD" bash -c "python3 '$LANE/quality/check-tool-ledger.py' --repo '$LANE' --rev HEAD 2>&1 | tail -1"
run "tool-ledger row count" grep -cE '^\| `' "$LANE/quality/tool-ledger.md"
run "routed-defect age derivation" printf '%s\n' "$((66-65))"
run "census warning count" grep -cE '^mado	W0' "$LANE/.ufo/waves/round-66/census-start-r66.txt"
run "census trailing status" tail -1 "$LANE/.ufo/waves/round-66/census-start-r66.txt"
run "source seat row id" grep -nE '^\| S435 ' "$LANE/.ufo/waves/round-66/w1/R66ScribeSources/SOURCES.append.md"

printf '\n== end ==\n' >>"$OUT"
exit 0
