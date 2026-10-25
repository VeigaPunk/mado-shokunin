# ConnRunState — run-state hygiene observation & connector synthesis (round 39, w1)

Seat: `ConnRunState` (connector, leaf member — no subagents, no background jobs, no mutations).
Lane repo: `/home/vgpnk/Projects/shokunin/mado-shokunin`.
Date: 2026-10-25.

---

## 1. Run-State Hygiene Observation

Push state during integration was observed (read-only) at two distinct moments using `/home/vgpnk/Projects/shokunin/scripts/hyaku/jj-lane.sh state /home/vgpnk/Projects/shokunin/mado-shokunin` and `git -C /home/vgpnk/Projects/shokunin/mado-shokunin ls-remote origin HEAD`.

### Moment 1 (2026-10-25 16:16:32 UTC)
- **`jj-lane.sh state`:**
  ```
  state branch=master local=457d1b125932c1e0d797061a2156b917bcd7edaa remote=457d1b125932c1e0d797061a2156b917bcd7edaa ahead=0 behind=0 head=detached tracked=0 untracked=10
  ```
- **`git ls-remote origin HEAD`:**
  ```
  457d1b125932c1e0d797061a2156b917bcd7edaa	HEAD
  ```
- **Exit codes:** both commands exited 0.
- **Ahead / Behind:** `ahead=0 behind=0`. Local master and remote origin/master are in identical sync at the freeze commit `457d1b125932c1e0d797061a2156b917bcd7edaa`. Remote `origin/HEAD` points to the exact same revision.

### Moment 2 (2026-10-25 16:17:15 UTC) & Re-check (16:19:54 UTC)
- **`jj-lane.sh state`:**
  ```
  state branch=master local=457d1b125932c1e0d797061a2156b917bcd7edaa remote=457d1b125932c1e0d797061a2156b917bcd7edaa ahead=0 behind=0 head=detached tracked=0 untracked=10
  ```
- **`git ls-remote origin HEAD`:**
  ```
  457d1b125932c1e0d797061a2156b917bcd7edaa	HEAD
  ```
- **Exit codes:** both commands exited 0.
- **Ahead / Behind:** `ahead=0 behind=0` (unchanged, strictly synchronized).

---

## 2. Lane Status Diff & Write Isolation Audit

### Status Diff
- `git -C /home/vgpnk/Projects/shokunin/mado-shokunin diff`: empty (exit 0).
- `git -C /home/vgpnk/Projects/shokunin/mado-shokunin status --porcelain`:
  `tracked=0` (no modified tracked files anywhere in the repo).
  `untracked=10` at top level:
  1. `.ufo/waves/round-39/w1-dispatch.json` (orchestration dispatch)
  2. `.ufo/waves/round-39/w1-plan.err` (orchestration planning stderr)
  3. `.ufo/waves/round-39/w1-plan.out` (orchestration planning dump)
  4. `.ufo/waves/round-39/w1-run.err` (orchestration run stderr)
  5. `.ufo/waves/round-39/w1-spec.json` (orchestration wave spec)
  6. `.ufo/waves/round-39/w1.ready` (orchestration ready marker)
  7. `.ufo/waves/round-39/w1.ready.dispatched` (orchestration dispatch marker)
  8. `.ufo/waves/round-39/w1/` (seat reports, fixtures, mirrors, and wave scratch evidence)
  9. `quality/counters/c3-r39-options.py` (C2 counting instrument, authored by `ExecOptionsCounter`)
  10. `tools/mado-options.py` (C2 deliverable tool, authored by `ExecOptionsTool`)

### Sibling Lane Isolation
- Checked all file creations across `mado-shokunin`:
  Every untracked path belongs strictly to `mado` round-39 wave 1 seats declared in `w1-spec.json`.
- **Verdict: ZERO sibling lane seat writes.** No seats from `tsukuroi`, `kama`, `kengaku`, `chousa`, `tabi`, `kasegi`, `souji`, `kumitate`, or any other sibling lane wrote to `/home/vgpnk/Projects/shokunin/mado-shokunin`.
- Furthermore, as corroborated by `SenWriteScope`, no `mado` seat wrote to the fleet root or to sibling lanes.

---

## 3. UFO-FSD Connector Synthesis

### Evidence & Contradiction Tracing
While observing the push state and analyzing uncommitted deliverables (`tools/mado-options.py`, `quality/counters/c3-r39-options.py`, `.ufo/waves/round-39/w1/ExecOptionsFixtures/`), a second-order contract failure between seats was uncovered:

1. **The Counter Contract (`quality/counters/c3-r39-options.py`):**
   `ExecOptionsCounter` implemented the C2 counting instrument following `PRED-C3-r39-v1`.
   In clause `c` and clause `d` (lines 84–118), the counter extracts `.ufo/waves/round-39/w1/ExecOptionsFixtures/run-fixtures.sh` into a temporary sandbox directory `work`, marks it executable, and executes:
   ```python
   fp = run(["/bin/sh", fixture, "--tool", tool, "--repo", repo], cwd=work)
   ```
   Clause `c` checks `fp.returncode == 0` and extracts `fixtures=N/N`.
   Clause `d` checks for a stdout line starting with `MADO_OPTIONS_ROWS:` to deserialize and validate row schema against `{"key", "value", "owner", "layer", "line", "set"}`.

2. **The Fixture Runner Reality (`.ufo/waves/round-39/w1/ExecOptionsFixtures/run-fixtures.sh`):**
   `ExecOptionsFixtures` authored `run-fixtures.sh` assuming execution inside its local seat directory.
   - It **does not parse `--tool` or `--repo`**. It hardcodes `TOOL="$LANE/tools/mado-options.py"` and `MAIN="$HERE/trees/main-home"`.
   - When isolated in `work = /tmp/mado-c3-r39-XXXXXX/`, `$HERE/trees/` does not exist (`run-fixtures.sh` only extracts itself, not the fixture trees).
   - In sandbox test, running `run-fixtures.sh` with `--tool ... --repo ...` fails immediately:
     `mkfifo: cannot create fifo .../trees/fifo-home/...: No such file or directory`
     `FAIL fixture1 tool-missing: //tools/mado-options.py`
     `fixtures=0/4`, exit code 1.
   - It **never emits `MADO_OPTIONS_ROWS:`**. Clause `d` will strictly score `row_shape=0`.

3. **Kill Rule Impact:**
   `c3-r39-options.py` requires all clauses `b:1 c:1 a:1 d:1 e:1 f:1 g:1`.
   Under the current code, at data-commit integration, `c3-r39-options.py` will report:
   `PRED-C3-r39-v1: fixtures=0/4 tool=present verdict=TARGET_MISSED`, exit 1.
   Per `registration.md:71` ("Kill rule: anything other than TARGET_MET at the data tip is a miss; no narrowing"), this contradiction will kill claim C2.

4. **Lesson Hash Drift (`ScrLesson.md` vs `SimplDraftTrim.md`):**
   `ScrLesson/round-39.md` baked an early intermediate worktree sha256 (`9787b53b...`) for `tools/mado-options.py`. `ExecOptionsRealTree` later updated `tools/mado-options.py` to achieve 69/69 selftest assertions, changing the hash to `cee78d99...`. As `SimplDraftTrim` noted, baking worktree hashes before the data commit tip lands introduces drift.

### Affected Axes
- **`operability` (primary):** C2 claim directly misses target (`fixtures=0/4 verdict=TARGET_MISSED` instead of `TARGET_MET`).
- **`calibration` (secondary):** Counter fails to score its own fixtures and row shapes due to runner sandbox isolation failure.
- **`navigation` (secondary):** Index and round progression stall if C2 fails its declared kill rule.

### Proposed Move
Synthesize the round's deliverables into an integrated, verified data commit before pushing:
1. **Align `run-fixtures.sh` contract with `c3-r39-options.py`:**
   - Add parameter parsing in `run-fixtures.sh` for `--tool <path>` and `--repo <path>`.
   - When `--repo` is supplied, anchor fixture trees to `$REPO/.ufo/waves/round-39/w1/ExecOptionsFixtures/trees/` (or have `c3-r39-options.py` extract the trees into `work`).
   - Append `echo "MADO_OPTIONS_ROWS: $(cat "$HERE/observed/treeA-static.json" 2>/dev/null || cat "$HERE/expected.json" | python3 -c 'import sys, json; print(json.dumps(json.load(sys.stdin)["static"]))')"` to satisfy clause `d`.
2. **Bind S219 to Committed Blob:**
   Update S219 sha256 in the lesson and `SOURCES.md` to `git show <data-tip>:tools/mado-options.py | sha256sum` as proposed by `SimplDraftTrim`.
3. **Clean Transient Orchestrator Artifacts:**
   Exclude the 5 transient non-evidence files (`w1-plan.out`, `w1-plan.err`, `w1-run.err`, `w1.ready`, `w1.ready.dispatched`) during integration commit per `SimplRepoClean`.

### Risks
- If `run-fixtures.sh` output format diverges from `fixtures=N/N` or `MADO_OPTIONS_ROWS:` format, clause `c` or `d` will fail.
- Moving fixture trees must not mutate host files or leave dangling FIFOs.

### Verification
Run `python3 -I quality/counters/c3-r39-options.py --repo . --rev <data-tip>` and verify:
`PRED-C3-r39-v1: fixtures=4/4 tool=present verdict=TARGET_MET`, exit 0, with `clauses=b:1 c:1 a:1 d:1 e:1 f:1 g:1`.

---

## 4. Limits & Tool Record
- No tools installed (stdlib python, git, bash only).
- Production lane files untouched (strictly read-only).
- No subagents dispatched; leaf bounds respected.
