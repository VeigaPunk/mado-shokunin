# MutTruth — mutation test of the round-23 repair truth oracle

**Seat:** MutTruth (leaf, no dispatch) · **Lane:** `mado-shokunin` ·
**Target:** `.ufo/waves/round-23/repair/truth.py`
(sha256 `7f9e7865b828dd49499c781ff9697fc49e5b7869b447f9047f16cea0236d18b0`) ·
**Scratch:** `/fast/scratch/hyaku/mado-r23/MutTruth/` ·
**Date:** 2026-10-22

**Verdict: the oracle is sound on every guard it claims to enforce — but 8 of its
10 behavioural branches are dead code against the frozen 12-case set. The frozen
set cannot distinguish the correct oracle from 8 of 10 plausible mutants. This
is a coverage finding about the repair set, not a defect in `truth.py`.**

---

## 1. Scope and what was run

`truth.py` is the round-23 repair-set truth oracle. It executes each fixture's
eval code in a child Python under a recording fake `subprocess` module and
decides pass/fail per case from the executed argv set. Its stated contract
(docstring) is: *refuses any fixture whose code imports anything except
subprocess*, *refuses a tampered snapshot*, and *exits 0 iff every case's
expectation matches the executed argv set*.

This seat mutation-tested that oracle: ten single-behaviour-point mutants, each
run against eleven scenarios, each compared against an unmutated control on the
same input, with byte-exact restoration verified after every run.

**No lane file was modified.** `git status --porcelain -- .ufo/waves/round-23/repair/`
is empty; the lane `truth.py` still hashes to `7f9e7865…d18b0` and `expected.json`
to `53e34d26…c6b9` after the whole campaign. All mutation happened on copies
under `/fast/scratch/hyaku/mado-r23/MutTruth/`.

## 2. Commands

```bash
# scratch copy of the frozen repair set
mkdir -p /fast/scratch/hyaku/mado-r23/MutTruth/{base,scenarios,mutants,receipts}
cp -a /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-23/repair/. \
      /fast/scratch/hyaku/mado-r23/MutTruth/base/

# passing control first (the unmutated judge on the lane's own bytes)
cd /fast/scratch/hyaku/mado-r23/MutTruth/base && python3 -I truth.py
#   -> exit 0, "passed": 12, "total": 12, expected_sha256 53e34d26…c6b9

# the mutation matrix (10 mutants x 11 scenarios, control-first)
cd /fast/scratch/hyaku/mado-r23/MutTruth && python3 -I harness.py

# branch-coverage probe on the frozen set (instrumented COPY in scratch)
cd /fast/scratch/hyaku/mado-r23/MutTruth && python3 -I coverage_probe.py

# single-mutant demonstration (safe() gate skipped vs restored)
cd /fast/scratch/hyaku/mado-r23/MutTruth && python3 -I demo.py

# lane integrity after the campaign
cd /home/vgpnk/Projects/shokunin/mado-shokunin
git status --porcelain -- .ufo/waves/round-23/repair/      # (empty)
sha256sum .ufo/waves/round-23/repair/truth.py .ufo/waves/round-23/repair/expected.json
```

Every run used `python3 -I` (isolated mode) and a 120–180 s timeout; the lane
classifier was never invoked and no transcript content was executed other than
through `truth.py`'s own recording fake `subprocess` module over fixtures I
authored in scratch.

## 3. Protocol (per L1 note)

* **Control first.** Each scenario has a *declared* expected control verdict,
  written from `truth.py`'s documented contract before the mutants ran. The
  unmutated oracle must produce it on the same input; otherwise that
  (mutant, scenario) pair is **inconclusive**, never a kill. All eleven
  controls passed (`control_ok: true` for every scenario in
  `mutation-matrix.json`).
* **Kill** requires a *different well-formed* mutant verdict. A mutant run that
  crashes (traceback / `SyntaxError` / `IndentationError` / exit 2) or times out
  is **inconclusive**. One early M5b mutant was an `IndentationError` and was
  re-authored to keep the file parseable; an early harness version mis-counted
  it as a kill because the classifier treated any non-JSON output as a clean
  refusal. Both were fixed before the reported numbers.
* **Kill rate** = killed / (killed + survived), inconclusive excluded.
* **Restoration** verified per run: the pristine bytes are written back and the
  scenario is re-run; both the sha256 and the resulting verdict must match the
  pre-mutation state.

**Totals: killed 30, survived 80, inconclusive 0. Kill rate 0.2727 (30/110).**
Two consecutive full harness runs produced identical verdicts
(`run1 == run2: True`). Restore verified 11/11 byte-exact for every one of the
ten mutants, with matching post-restore verdicts.

## 4. The ten mutants

| id | single behaviour point changed | killed by | kill rate |
|---|---|---|---|
| M1 | drop `and not forbidden` from both verdict branches (2 sites) | S4, S10 | 0.182 |
| M2 | exact cases: `set(want) <= set(executed)` instead of `sorted==` | S5, S7 | 0.182 |
| M3 | recording fake captures the *previous* subprocess call's argv | S4, S5 | 0.182 |
| M3b | recorder resolves argv from the caller's module globals, not the argument | S0, S3, S4, S5, S6, S7, S9, S10 | 0.727 |
| M3c | recorder keeps only the last argv element | S0, S3, S4, S5, S6, S7, S9, S10 | 0.727 |
| M4 | skip the `safe()` gate entirely | S3, S9 | 0.182 |
| M4b | `safe()` keeps running but drops only its import-rejection branch | S3, S9 | 0.182 |
| M5a | skip the `expected.json` snapshot-tamper check | S1, S8 | 0.182 |
| M5b | skip the per-fixture snapshot-tamper check | S2 | 0.091 |
| M5c | skip the end-of-run re-verification `load()` call | S8 | 0.091 |

### The five requested mutants, in detail

**M1 — drop the forbid check.** *Killed by S4 and S10; survived S0 (the frozen
set).* In S4 the probe fixture legitimately executes `pacman -S r23-hook-dict`
**and** `pacman -S r23-forbidden-extra`, the latter listed in `forbid_any`.
Pristine rejects the case (`passed 12/13`, exit 1); M1 accepts it
(`passed 13/13`, exit 0) — a **false-accept** on a case that genuinely contains
a forbidden command. S10 confirms it on a deliberately-wrong expectation copy:
`forbid_any` was edited to name the command the fixture really runs, and pristine
rejects it while M1 accepts it.

**M2 — subset instead of equality for exact cases.** *Killed by S5 and S7;
survived S0.* S5's probe fixture executes two commands while `want` lists one;
pristine fails it (equality), M2 passes it (subset) — **false-accept**. S7 is
the deliberately-wrong expectation copy: `want` for `ReturnedGlobalHelper` is
duplicated so the multiset no longer equals the executed set while the *set* is
still a subset; pristine rejects, M2 accepts.

**M3 — record argv from the wrong call.** *Killed by S4 and S5; survived S0.*
The fake `run()` is rewritten to append the *previous* call's argv. Every
frozen fixture makes exactly one `subprocess.run` call, so the mutant is
indistinguishable there. On the two-call probes the executed set comes out
wrong (`pacman -S r23-hook-dict` twice instead of the two distinct commands),
pristine and mutant disagree — false-accept on S4, verdict-differs on S5.

**M4 / M4b — skip the `safe()` gate.** *Killed by S3 and S9; survived S0.*
S9 is the direct confirmation required by the assignment: a scratch fixture
whose code is `import os` + `import subprocess` + one `subprocess.run`.

```
pristine truth.py  -> {"id": "ProbeOnlyUnsafeOs", "passed": false, "error": "unsafe_fixture"}
                      exit=1, passed 12/13   (the fixture is NOT executed)
M4 (gate skipped)  -> {"id": "ProbeOnlyUnsafeOs", "passed": true,
                       "executed": ["pacman -Q probe-only-unsafe-os"]}
                      exit=0, passed 13/13   (the os-importing fixture RAN)
```

That is a **false-accept**: the gate is what keeps the oracle from executing an
`os`-importing fixture, and removing it lets that fixture run to completion.
M4b (keep `safe()`, drop only its import branch) is killed the same way. Note
the M4 demonstration ran `os.environ.get("HOME", "")` only — read-only, no
writes, nothing outside the scenario directory.

**M5 — skip the tamper check.** *Killed by S1, S2, S8.* Three variants:
M5a (drop the `expected.json` sha check) is killed by S1 (a byte appended to
`expected.json` with the `EXPECTED_SHA` constant deliberately left stale →
pristine refuses with `snapshot_tampered: expected.json`, M5a runs and reports
12/12) and by S8. M5b (drop the per-fixture sha check) is killed by S2 (a
fixture's bytes altered → pristine refuses with `snapshot_tampered:
ReturnedGlobalHelper`, M5b runs). M5c (drop the trailing re-verification
`load()`) is killed only by S8, a mid-run tamper: the probe fixture rewrites
`expected.json` *while the oracle is running*, which only the end-of-run
re-verification can catch.

**The tamper checks are therefore live and correctly placed.** Every mutant
that removes one produces a false-accept — accepting a snapshot that the
pristine oracle refuses.

## 5. Scenarios

| id | what it is | pristine control verdict |
|---|---|---|
| S0 | the frozen 12-case repair set, byte-exact | JSON, exit 0, 12/12 |
| S1 | `expected.json` bytes tampered, `EXPECTED_SHA` left stale | refusal `snapshot_tampered: expected.json` |
| S2 | one fixture's bytes tampered | refusal `snapshot_tampered: ReturnedGlobalHelper` |
| S3 | two unsafe fixtures added (one references `os`, one imports it unused) | JSON, both probes `error: unsafe_fixture` |
| S4 | present-kind case whose fixture also executes a forbidden command | JSON, `ProbeForbiddenPresent` failed |
| S5 | exact-kind case whose fixture executes more commands than `want` | JSON, `ProbeMultiCallExact` failed |
| S6 | **wrong expectation copy**: `want` names a command never executed | JSON, `ReturnedGlobalHelper` failed |
| S7 | **wrong expectation copy**: duplicated `want` row (set-subset of truth) | JSON, `ReturnedGlobalHelper` failed |
| S8 | **mid-run tamper**: the fixture rewrites `expected.json` during the run | refusal `snapshot_tampered: expected.json` |
| S9 | **unsafe fixture** importing `os`, nothing else | JSON, `ProbeOnlyUnsafeOs` `error: unsafe_fixture` |
| S10 | **wrong expectation copy**: `forbid_any` names the command actually run | JSON, `ReturnedGlobalHelper` failed |

S6/S7/S10 are the "deliberately wrong expectation copy" probes — `expected.json`
edited **in scratch only**, with `EXPECTED_SHA` updated to match so the tamper
check does not fire first. The pristine oracle rejects all three, which is the
correct behaviour; the mutants that weaken the comparison accept them.

## 6. The coverage finding — why 8 of 10 mutants survive the frozen set

The branch-coverage probe (`coverage-branches.json`) instruments a **copy** of
`truth.py` in scratch with counters separating "branch reached" from "branch
taken", then runs it over the frozen 12-case set:

```
exact 10   present 2   calls_total 12   cases_multicall 0
forbid_nonempty 0     forbid_empty 12
safe_reached 12       unsafe_taken 0
child_error_reached 12   child_error_taken 0
```

Reading it:

* **`forbid_nonempty = 0`** — no frozen case ever executes a forbidden command,
  so the `and not forbidden` term is never *false*. M1 cannot be killed by the
  frozen set. (S4 and S10 exist precisely to reach that branch.)
* **`unsafe_taken = 0`** — `safe()` is reached for all 12 cases and rejects none.
  Every frozen fixture imports only `subprocess`, so the gate's refusal path is
  dead code against this population. M4/M4b survive by construction.
* **`cases_multicall = 0`, `calls_total = 12`** — every frozen fixture makes
  exactly **one** `subprocess.run` call. A recorder that captures the wrong
  call (M3) or the wrong scope (M3b) or the wrong argv element (M3c) is
  indistinguishable when there is only one call to record. M3 survives.
* **`child_error_taken = 0`** — no frozen fixture makes the child fail, so the
  `proc.returncode != 0` path is never taken.

Only **M3b and M3c** are killed by the frozen set (S0), because they corrupt
the argv *value* rather than the call *identity* — and a single-call fixture
still exposes a corrupted value. M3b (`sys._getframe(1).f_globals.get("argv")`)
is caught at 10/12 on S0 because two frozen fixtures bind a *different* `argv`
in the caller's globals than the one actually passed; M3c (last element only) is
caught at 0/12, obviously.

**Consequence for C1.** The frozen 12-case set + `truth.py` at 12/12 does **not**
demonstrate that the oracle's forbid check, safe() gate, multi-call recording,
child-error path or tamper re-verification work. The claim as registered —
"Truth is mechanical: `repair/truth.py` runs each fixture under a recording fake
`subprocess` module and passes 12/12" — is true but weaker than it reads: 12/12
is consistent with eight of ten plausible single-line corruptions of the oracle
itself. The repair set's *scanner* assertions are unaffected (this probe never
invokes the classifier); what is thin is the *oracle's* own self-certification.

## 7. Restoration evidence

* Every mutant was installed into the scenario's `truth.py`, run, then the
  pristine bytes were written back and the scenario re-run. All ten mutants:
  **11/11 scenarios restored byte-exact** (sha256 match) **and behaviourally
  identical** to the pre-mutation control.
* The lane `repair/truth.py` is byte-identical to the start of the campaign
  (`7f9e7865b828dd49499c781ff9697fc49e5b7869b447f9047f16cea0236d18b0`); the
  lane `expected.json` is byte-identical (`53e34d26…c6b9`).
* The regenerated scenarios (`S3`–`S10`) differ from the pristine `truth.py` by
  exactly one line — the `EXPECTED_SHA` constant, updated to match that
  scenario's own `expected.json`. `diff` confirms this and nothing else.
* The scratch harness restores inputs (`expected.json`, fixtures) before every
  run, so S8's self-modifying fixture stays deterministic; two consecutive full
  harness runs produced identical verdicts.

## 8. Recommendation (advice only — the L1 seat owns integration)

No change to `truth.py` is warranted: every guard it claims is live, correctly
placed, and each removal produces a false-accept that the oracle's own design
catches. `truth.py` is sound.

If C1's operability claim is to mean more than "the oracle agrees with itself
on twelve cases it was written against", the cheap strengthening is to add
**three probe cases to the repair set** (all authored before any production
edit, and all passing under the pristine oracle):

1. a **forbid-reachable** case — a fixture that executes a command listed in
   `forbid_any` — so `forbid_nonempty` is exercised (kills M1);
2. an **unsafe-fixture** case importing `os` — so `unsafe_taken` is exercised
   (kills M4, M4b);
3. a **two-call** case — so `cases_multicall` is exercised (kills M3).

Plus one **tamper probe** for the fixture-sha and re-verification paths (S2,
S8), which already have their own scenario. These are additions to the frozen
set, so they are a change to a committed artefact — L1's call, not mine.

## 9. Artefacts

| path | content |
|---|---|
| `.ufo/waves/round-23/w1/out/MutTruth/mutation-matrix.json` | full matrix: controls, per-mutant per-scenario verdicts, restore evidence (sha256 + verdict) |
| `.ufo/waves/round-23/w1/out/MutTruth/coverage-branches.json` | branch-coverage counters on the frozen set |
| `.ufo/waves/round-23/w1/out/MutTruth/harness.py` | the mutation harness (10 mutants, 11 scenarios, control-first) |
| `.ufo/waves/round-23/w1/out/MutTruth/coverage_probe.py` | the branch-coverage probe |
| `.ufo/waves/round-23/w1/out/MutTruth/demo.py` | the single-mutant safe()-gate demonstration (pristine vs M4 vs restored) |
| scratch | `/fast/scratch/hyaku/mado-r23/MutTruth/` (base, scenarios/, receipts/, demo.py) |

Receipt sha256:
`mutation-matrix.json` `240d1c4bfa1db8c2330615b369d5ff23a86749e385ec273b2b24bd913191ec10` ·
`coverage-branches.json` `39c491a9308dcbc399d10a7a44ce5c9b35e12dede680707e6e596a9850f711ac` ·
`harness.py` `6b07a28dbf7650f57a207b581db56d335815c836ce055e0804855cadcaa0d12c` ·
`coverage_probe.py` `ddceabab28fecc6f4a070b0ec6037582f9c22a770dce92a13471a672ad7e4cc3` ·
`demo.py` `c9af5fb6c924ef98750808a5842fbbb880b1bb24a4da8635d14b5def563e9de1`

## 10. Verdict

**`truth.py` is sound: all ten mutants were caught by at least one scenario, the
tamper checks and the `safe()` gate both demonstrably refuse, and every
mutation was restored byte-exactly. But 8 of 10 mutants survive the frozen
12-case set, and the branch-coverage probe explains exactly why: the forbid
check, the unsafe-fixture path, the multi-call recording path and the
child-error path are never taken by the frozen population. The repair set's
12/12 therefore certifies the oracle far more weakly than it appears to.**

**Recommendation to L1: no `truth.py` change; consider three probe cases
(forbid-reachable, unsafe-import, two-call) added to the frozen repair set so
the oracle's own guards are exercised. This is advice — the L1 seat owns what
lands.**
