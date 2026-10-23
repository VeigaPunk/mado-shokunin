# CapDigestPinnedFrozenRegres438 — C2 row re-run: SCORECARD.md:438

Seat: `MadoR25A3.CapDigestPinnedFrozenRegres438` (leaf executor, C2 row contract). Wave: round-25 attempt 3,
`a3w1` (pre-data). Read-only at base `41cc04c8d593837a0d5078bffaacdaa163d12897`; no lane file edited except this
report; no git/jj write in the lane; sandbox clone deleted before returning.

## Row and section

- Row: `SCORECARD.md:438`, table header `SCORECARD.md:435-436`, under `### Sources and demonstrated repertoire`
  (`SCORECARD.md:425`), inside `## Round 13 — committed measurements and author verdicts` (`SCORECARD.md:367`).
  It is a repertoire row under a non-`Capabilities` heading, so it sits outside round-24's counted 12-row C2
  population (`SCORECARD.md:1588-1590`) and inside the literal "capability table" reading round 24 flagged
  (`SCORECARD.md:1606`).
- Row bytes (from `git show 41cc04c8:SCORECARD.md`):

  ```
  | digest-pinned frozen regression | Verify both committed gate/harness input digests before evaluating the recorded regression, with tamper refusal | `python3 .ufo/waves/round-13/frozen/verify.py` → `frozen_match`, exit 0; `--selftest` 12/12; `frozen/expected.json` | 13 |
  ```
- Capability: `digest-pinned frozen regression`.
- Stated claim (14 words): "Verify both committed gate/harness input digests before evaluating the recorded
  regression, with tamper refusal".
- Demonstration command: `python3 .ufo/waves/round-13/frozen/verify.py`; `--selftest` 12/12; evidence pointer
  `frozen/expected.json` (under `.ufo/waves/round-13/` per `SCORECARD.md:440-443`).
- Evidence pointer check: `frozen/expected.json` exists at base, pins exactly two inputs and the expected verdict:
  `{"inputs": {"gate.sh": "037b05dcd3f86e12e1b89ee5631f76ce95301b7c411957fad17ff0d7438a6569", "harness.sh":
  "75ed934dc86360f5c2cdd5b17abb8814249425e9c1835d36b81d74412719adc5"}, "expected_exit": 0, "expected_marker":
  "MADO_REGRESSION: PASS"}` (sha256 of the file `761a0c91e559dc2b14e4196e55c09e55568acb41e93a8849ec8f05a40ecf5ad8`).
  Both pinned digests equal the committed `gate.sh` (`037b05dc…`) and `harness.sh` (`75ed934d…`) at base, which I
  re-derived with `sha256sum` in the clone; `verify.py` at base is sha256
  `094bf3a494734e784b9a242e076e5c4f51dd71b355476ed071194a8606ee7591`, 197 lines.

## Sandbox

```
mkdir -p /fast/scratch/hyaku/mado-r25a3/c2
env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git clone -q /home/vgpnk/Projects/shokunin/mado-shokunin /fast/scratch/hyaku/mado-r25a3/c2/CapDigestPinnedFrozenRegres438
env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git -C /fast/scratch/hyaku/mado-r25a3/c2/CapDigestPinnedFrozenRegres438 checkout -q --detach 41cc04c8
git -C /fast/scratch/hyaku/mado-r25a3/c2/CapDigestPinnedFrozenRegres438 rev-parse HEAD
```
→ `41cc04c8d593837a0d5078bffaacdaa163d12897`. `df -h /fast` before the clone: 220 G available.

The row's command was runnable as written (relative path, clone root as cwd), under `timeout 600
prlimit --as=4000000000`. The main leg runs the frozen `gate.sh --regression` replay, which writes scratch only
under `/tmp/mado-verify-regression.*` (gate header line 1402) and removed its workdir on PASS; the run left no
persistent process (checked in the final host sweep below).

## Verbatim command output

```
----- CMD: timeout 600 prlimit --as=4000000000 python3 .ufo/waves/round-13/frozen/verify.py -----
FROZEN_INPUT: gate.sh sha256=037b05dcd3f86e12e1b89ee5631f76ce95301b7c411957fad17ff0d7438a6569 verified
FROZEN_INPUT: harness.sh sha256=75ed934dc86360f5c2cdd5b17abb8814249425e9c1835d36b81d74412719adc5 verified
FROZEN_RUN: bash /fast/scratch/hyaku/mado-r25a3/c2/CapDigestPinnedFrozenRegres438/.ufo/waves/round-13/frozen/gate.sh --regression (cwd=/fast/scratch/hyaku/mado-r25a3/c2/CapDigestPinnedFrozenRegres438/.ufo/waves/round-13/frozen, harness=/fast/scratch/hyaku/mado-r25a3/c2/CapDigestPinnedFrozenRegres438/.ufo/waves/round-13/frozen/harness.sh)
REGRESSION_TOOL: /fast/scratch/hyaku/mado-r25a3/c2/CapDigestPinnedFrozenRegres438/.ufo/waves/round-13/frozen/gate.sh sha256=037b05dcd3f86e12e1b89ee5631f76ce95301b7c411957fad17ff0d7438a6569
REGRESSION_DATE: 2026-10-23T07:22:49Z
REGRESSION_HARNESS: /fast/scratch/hyaku/mado-r25a3/c2/CapDigestPinnedFrozenRegres438/.ufo/waves/round-13/frozen/harness.sh sha256=75ed934dc86360f5c2cdd5b17abb8814249425e9c1835d36b81d74412719adc5 (recorded revision b56c6e57f1b7ae91c85f06ee101d3a348158ab219fae4a16f5d3e6f77fd22bcb — provenance, not gated)
REGRESSION_SPEC: /tmp/mado-verify-regression.Lia8ih/mado-verify.defects.spec sha256=c7ee75b97c38ac8f88410165a574ad1cba7f4653bd09d35e6814267a12df1dd8 (recorded pin matches)
REGRESSION_TARGET: /tmp/mado-verify-regression.Lia8ih/target.mado-verify.sh sha256=87910c39f460ad169b879fc28f2e80f2c988d56f91e18b51efcac9cb0ec04b39 (recorded pin 87910c39f460ad169b879fc28f2e80f2c988d56f91e18b51efcac9cb0ec04b39; match=yes)
REGRESSION_BAND: all recorded kills required (recorded 10/10 KILLED; flips=0; inconclusive=0; control GREEN; MUTATE_RESTORE OK; target sha unchanged) — plan §(a) killed-delta<=1 tolerance not applied
REGRESSION_SWEEP mado-verify-hardened: MUTATE: DONE (target=mado-verify-hardened defects=10 killed=10 survived=0 inconclusive=0 kill-rate=100%)
REGRESSION_TABLE mado-verify-hardened: match=10/10 recorded-killed=10 measured-killed=10 survived=0 inconclusive=0 flips=0
REGRESSION_WORKDIR mado-verify-hardened: /tmp/mado-verify-regression.Lia8ih/case
REGRESSION_CASE mado-verify-hardened: PASS (recorded table reproduced: killed=10/10 flips=0 inconclusive=0 control=green restore=ok)
REGRESSION_CLEANUP: removed=10 kept-fixture dir(s) named by this run (paths read from this run; /tmp/w5-mado-m52-selftest.* prefix-guarded)
MADO_REGRESSION: PASS (case=mado-verify-hardened; target=87910c39f460ad169b879fc28f2e80f2c988d56f91e18b51efcac9cb0ec04b39)
REGRESSION_WORKDIR: /tmp/mado-verify-regression.Lia8ih (removed on PASS; --keep retains)
MADO_FROZEN: MATCH
FROZEN_DETAIL: exit=0 marker='MADO_REGRESSION: PASS'
FROZEN_ID: frozen_match
exit=0
[wall 153.96 s]

----- CMD: timeout 600 prlimit --as=4000000000 python3 .ufo/waves/round-13/frozen/verify.py --selftest -----
MADO_FROZEN_SELFTEST: 12/12 assertions passed
exit=0

----- CMD (extra, tamper leg on a /tmp copy: one appended byte in gate.sh) -----
FROZEN_INPUT: harness.sh sha256=75ed934dc86360f5c2cdd5b17abb8814249425e9c1835d36b81d74412719adc5 verified
MADO_FROZEN: TAMPERED
FROZEN_DETAIL: failures=1
FROZEN_DETAIL: mismatch gate.sh expected=037b05dcd3f86e12e1b89ee5631f76ce95301b7c411957fad17ff0d7438a6569 actual=7b5a96c1056e50581e7c12a73e0f0e67837adb3e3a578f15253a73927c6263f1
FROZEN_ID: snapshot_tampered
exit=2
```

(The `----- CMD: ... -----` and `[wall ...]` lines are my capture wrapper; every other line is command stdout
byte-for-byte.) The tamper leg is an ad hoc probe of the row's "tamper refusal" clause, not part of the row's
written command: it copied the four frozen files to `/tmp/c2-frozen-tamper.PEZksi`, appended
`# tampered byte\n` to `gate.sh`, and ran `verify.py` there. It exited 2 `snapshot_tampered`, named the mismatched
input, and printed **no** `FROZEN_RUN` line — the gate was not evaluated after a failed digest. That temp dir was
deleted.

## Superseding or contradicting text found in SCORECARD.md at 41cc04c8

- `SCORECARD.md:1588-1594` — round-24 wave-2 append: this exact row is named as one of "three repertoire rows
  [that] sit under other headings and are outside the counted population", and was re-run at `39c59630`:
  `digest-pinned frozen regression` (round 13) prints `MADO_FROZEN: MATCH`, exit 0. **Confirms** the row's claim;
  does not supersede it with a different status. It is the operative present-tense status declaration for this
  row because the round-24 status table does not list it.
- `SCORECARD.md:1570` — the round-24 status table says it "supersedes the implied `works` of every earlier row",
  but its own scope correction at `:1588-1594` limits that to the 12 counted rows; this row is not in the table,
  so no status change from it.
- `SCORECARD.md:406-408` — same round-13 section, harm-watch bullet: "Frozen companion verifies input digests
  before replay, ends `frozen_match` and `MADO_REGRESSION: PASS`, exit 0; selftest 12/12". Corroborates the row
  (same claim, same numbers), not a supersession.
- **Contradiction: none.** Other `frozen_match` / frozen-replay hits are different capabilities or other rounds'
  frozen pairs: `:546` (round-14's own `frozen/verify.py` pair), `:782` (round-16 declared-action classifier
  `--frozen`), `:998,1020,1580` (round-18 tripwire frozen replay), `:1134,1191,1330,1391,1458` (tripwire
  baselines). No later row reports this runner failing, its digests drifting, or its selftest count changing.

## Ledger line

| SCORECARD.md:438 | digest-pinned frozen regression | Verify both committed gate/harness input digests before evaluating the recorded regression, with tamper refusal | observed at 41cc04c8: works — exit 0, `MADO_FROZEN: MATCH` / `FROZEN_ID: frozen_match` after both `FROZEN_INPUT … verified` lines; `--selftest` 12/12 exit 0; one appended byte → `snapshot_tampered` exit 2 with no gate run | `timeout 600 prlimit --as=4000000000 python3 .ufo/waves/round-13/frozen/verify.py` and `… --selftest` from a clone at 41cc04c8 | SCORECARD.md:1588-1594 (round-24 wave-2: outside counted population; re-ran at `39c59630` as `MADO_FROZEN: MATCH`, exit 0) |

## Interpretation (grounded in the observed output)

- The mechanism is exactly as stated: both `FROZEN_INPUT` digest checks print `verified` **before** the
  `FROZEN_RUN` line, and the tamper probe shows a changed input produces `snapshot_tampered`, exit 2, with no
  gate execution (the `FROZEN_RUN` line and the gate's own `REGRESSION_TOOL`/`MADO_REGRESSION` markers are
  absent). The selftest's assertions cover the same branches (clean match, verdict mismatch, changed input,
  missing input, malformed `expected.json`, each asserting the gate was not invoked on refusal).
- The recorded regression reproduces at base: spec sha `c7ee75b9…` matches its pin, target sha `87910c39…` matches
  its recorded pin, 10/10 mutants killed with flips 0, and the marker `MADO_REGRESSION: PASS` is emitted.
- Scope limit (not a contradiction): the runner authenticates `gate.sh` and `harness.sh` against
  `frozen/expected.json`; it does not digest-pin `expected.json` or `verify.py` themselves, so a coordinated
  rewrite of the pin file together with both inputs would match. This is the same in-directory-pin caveat round 16
  states for its own frozen receipt (`SCORECARD.md:786-788`). The row's wording ("both committed gate/harness
  input digests") is accurate to that scope.

## Files changed

- `Report:` `.ufo/waves/round-25/a3w1/reports/CapDigestPinnedFrozenRegres438.md` (this file). Nothing else.
- Sandbox clone `/fast/scratch/hyaku/mado-r25a3/c2/CapDigestPinnedFrozenRegres438` deleted before returning;
  `ls /fast/scratch/hyaku/mado-r25a3/c2/` no longer lists it (only sibling seats' pre-existing artifacts and
  `SCORECARD-41cc04c8.md` remain, untouched). My `/tmp/c2-frozen-tamper.PEZksi` was deleted.

## Risks and blockers

- None blocking. One run per leg at the base, not a repeat sweep; the main leg depends on `/tmp` writability and
  takes ~154 s because it re-runs the 10-mutant replay.
- Host sweep: my run left no process; `pgrep -af "mado-verify|round-13/frozen"` after cleanup listed only other
  seats' concurrent runs (`/tmp/mado-verify-regression.IhWrko`, pid 2608887 and children) and their scratch dirs,
  which I did not touch. Two pre-existing `/tmp/mado-verify-regression.*` dirs belong to those runs, not mine.
- The observed status is pinned to `41cc04c8`; a later revision that edits the frozen dir's gate/harness bytes
  without re-pinning `expected.json` would read `snapshot_tampered` by design.
- No tool install or package transaction was needed or performed.
