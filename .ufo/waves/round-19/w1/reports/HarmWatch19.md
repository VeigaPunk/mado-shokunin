# HarmWatch19 — round-19 harm-watch runner delivered; verified end-to-end on REV 17661e0 with the live-wave pin skips visible

## Deliverable

`.ufo/waves/round-19/harm-watch.sh` (469 lines, mode 755, sha256 `077e1b4d05be67aca0587b240122f05eb2d4bb4f5955d93f368d46b0ae09238a`), adapted from `.ufo/waves/round-18/harm-watch.sh`. `bash -n` passes; `--help` exits 0; missing REV, unresolvable REV and an uncreatable OUTDIR each exit 2 (observed).

Contract implemented:

- REV from `$1` or `$REV`; resolved with `git rev-parse --verify REV^{commit}`; OUTDIR from `$OUTDIR`, default `$ROOT/.ufo/waves/round-19/evidence/harm` (script line 55); per-command TTL `HARM_TIMEOUT` default 1800.
- Every command file starts with one `RECEIPT tool=… tool_sha256=… measured_commit=<full REV> utc=<ISO-Z> cwd=<lane> argv=<%q words>` line and ends with `exit=<rc>`.
- `pin_assert` compares the worktree bytes of every executed tool to `git show REV:<path>` in a temp file (never the empty-input digest). On mismatch/missing it writes `measured_commit=UNVERIFIED`, the two digests, `status=skipped:pin_mismatch`, `exit=skipped`, and counts the skip as a failure. Pin lines land in `harm-watch-pins.txt`.
- Commands: gate `--selftest`, gate `--regression`, action-plan `--selftest`, `mado-tripwire.py --selftest` for every immediate suite dir with `expected.json` under `.ufo/waves/{round-17,round-18,round-19}/tripwire`, `--frozen .ufo/waves/round-18/frozen`, `--frozen .ufo/waves/round-19/frozen` when that dir exists, round-16 measure, round-17 measure, `tw-recall.py`, `fresh-pins.py`, the SCORECARD `### Counting command` block via `bash -s` with `REV` exported (read from the worktree `SCORECARD.md`, its worktree/REV digests and block digest recorded in PINS), and fleet `sources-census.sh validate --root <fleet> mado` pinned to the fleet HEAD bytes.
- Frozen round-18: only the pairs `(exit 0, frozen_match)` and `(exit 1, frozen_verdict_mismatch)` are recorded as `BASELINE` and excluded from the failure count (the declared round-19 expectation); `frozen_error`/`snapshot_tampered`/`unpinned_legacy`, a timeout, or any label/exit mismatch still fails.
- Summary carries per-command result lines plus per-group `TALLY` lines (runs/ok/fail/skip/baseline) and an aggregate `TALLY total … blocking=`; verdict = PASS iff failures (rc!=0 or pin skip) = 0.
- No live gate: the script never passes `--live` or `--no-live` (grep shows no such token); only `--selftest`/`--regression`/`--frozen` are issued.

Self-test defect fixed in flight: the tally loop had used `GROUPS`, a Bash special array (the caller's group IDs), so the first aggregate tally printed as group `1000`. Renamed to `GROUP_LIST`; aggregate `fail` was also split from `skip` (skips still block PASS via `blocking=`).

## Test runs, REV=`17661e0fa83f978fb659f5bb8fef47f0969f6945`, OUTDIR under /tmp

**Run A (17:07–17:09Z; pre-registration tree, only untracked sibling files).** 17 commands executed. Gate selftest exit 0 with `MADO_SELFTEST: 389/389 assertions passed`; gate regression exit 0; action-plan exit 0; 4 round-17 + 2 round-18 suites exit 0; round-19 `r19-bashcvar` exit 1 (9/15 cases, the C3 draft fixture red against the d9a5a18-lineage tool — expected before the tool fix); frozen-18 `BASELINE label=MADO_TRIPWIRE_FROZEN: frozen_match exit=0`; round-16 measure, round-17 measure, tw-recall, fresh-pins, navigation and census all exit 0. `HARM_WATCH: FAIL failures=1` (the one in-flight round-19 fixture). Those OUTDIR files were later replaced by later runs at the same path; the values above were read from them while they existed.

**Run B (17:10Z, same REV; preserved at `/tmp/harm-watch-r19-runB`).** A sibling rewrote `tools/mado-verify.sh` mid-wave (worktree `b4763245…` vs REV `c9fb0cef…`), so both gate commands skipped with `measured_commit=UNVERIFIED status=skipped:pin_mismatch`; `r19-installers` appeared and was red (1/17); `r19-bashcvar` still red (9/15). `HARM_WATCH: FAIL failures=4`.

**Run C (final retained run, 17:15Z; canonical artifacts at `/tmp/harm-watch-r19-test`).** A further sibling gate rewrite moved `tools/mado-verify.sh` to worktree `634dfedd…` vs REV `c9fb0cef…`, so both gate commands again skipped with `measured_commit=UNVERIFIED status=skipped:pin_mismatch`. More fixtures kept appearing: `r19-helperfn` joined and was red (19/32). Aggregate tallies, verbatim:

```
TALLY	total	runs=20	ok=13	fail=4	skip=2	baseline=1	blocking=6
TALLY	gate	runs=2	ok=0	fail=0	skip=2	baseline=0
TALLY	tripwire-selftest	runs=10	ok=6	fail=4	skip=0	baseline=0
TALLY	tripwire-frozen	runs=1	ok=0	fail=0	skip=0	baseline=1
TALLY	action-plan	runs=1	ok=1	fail=0	skip=0	baseline=0
TALLY	measure-r16	runs=1	ok=1	fail=0	skip=0	baseline=0
TALLY	measure-r17	runs=1	ok=1	fail=0	skip=0	baseline=0
TALLY	tw-recall	runs=1	ok=1	fail=0	skip=0	baseline=0
TALLY	fresh-pins	runs=1	ok=1	fail=0	skip=0	baseline=0
TALLY	navigation	runs=1	ok=1	fail=0	skip=0	baseline=0
TALLY	census	runs=1	ok=1	fail=0	skip=0	baseline=0
HARM_WATCH: FAIL failures=6
```

The 6 blockers are exactly: 2 gate pin skips (sibling gate rewrite) + 4 red round-19 fixture suites (`r19-bashcvar` 27/45, `r19-helperfn` 19/32, `r19-installers` 1/17, `r19-vcs` 5/16; all untracked worktree fixtures, not present at REV). `r19-frozen-f1f2` has only nested case dirs and no top-level `expected.json`, so it is NOTEd and not run; round-19 `frozen/` is absent and NOTEd. The failure count grew across runs only because sibling seats kept adding pre-fix fixture suites — no executed pin-matched command regressed.

Counter observations from the final run receipts (all exit 0, tools pinned to REV):

- `fresh-pins.py`: denominator 13, current 2, score 1.5385 (`harm-fresh-pins.txt`).
- `tw-recall.py`: 6 incident lines, 3 detected, score 5.0.
- round-17 `measure.py`: c1 18/26 lesson-cited, score 6.9231; c2 6/6 provinces.
- round-16 `measure.py`: JSON emitted, `gate_executed=false`; exit 0 (a `SyntaxWarning` from the script's own docstring is captured before the JSON).
- navigation block: `revision=17661e0… indexed=34/34 missing=0 dangling=0 duplicates=0 coverage=10.0000/10`, `scorecard_state=ok`, block sha256 `8b59b503…` (matches SCORECARD's declared fence digest).
- census: exit 0, `mado ok`, W04 duplicate-URL warnings only.
- frozen round-18: `MADO_TRIPWIRE_FROZEN: frozen_match`, recorded BASELINE, excluded from failures as specified.

## Risks and handoff notes for L1

- Harm-watch only proves a REV when the worktree tool bytes equal that REV. During this wave `tools/mado-verify.sh` was rewritten under the running test; any run before integration will show gate SKIPs (counted as failures, by design). Run it once after the wave's tool edits are committed/anchored, with REV naming those bytes.
- The round-19 tripwire suites (`r19-bashcvar`, `r19-helperfn`, `r19-installers`, `r19-vcs` at the final run) are worktree fixtures being authored by sibling seats and are red against the pre-fix tool; at REV `17661e0` they are not part of the pinned tree, so their failure measures the wave's pre-fix state, not a regression of REV.
- Round-19 `--frozen` is wired but untested: the dir did not exist during any run; an invalid/incomplete round-19 snapshot will surface as a normal command failure.
- `[INFERENCE]` If L1 edits the SCORECARD counting block while harm-watch reads the worktree file, the measured navigation result follows the worktree block; the run emits a `scorecard_state=mismatch` NOTE and the PIN line records both digests, so the drift is visible.
- Suite discovery happens once per run; a suite directory created after listing is picked up only by the next run (observed with `r19-installers`/`r19-vcs` appearing between runs).

## Limits

I did not run the live gate, `--no-live`, or any host/substrate probe. I did not run the script against its default OUTDIR (that would write lane evidence outside my assignment); all test output is under `/tmp/harm-watch-r19-test` and `/tmp/harm-watch-r19-runB`. Run A's command files were overwritten by later runs, so Run A's gate 389/389 and regression exit 0 are quoted from the session's observation of those files, not from retained bytes. No shellcheck was run (only `bash -n`). No web fetches, so no receipts. I did not inspect or modify any fleet/sibling file.

## Installs

none
