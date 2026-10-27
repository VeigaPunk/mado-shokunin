# ExecControlsC1 — C1 control fixtures and expected receipts (round 51, w1)

Seat: ExecControlsC1 (leaf). Lane: `/home/vgpnk/Projects/shokunin/mado-shokunin`.
Round base: `6ca8c559a4a3d6d361101592116eea2bc7452437`. Scope: the C1 do-nothing controls
(a)–(e) for `PRED-C1-r51`, built as a SPEC + receipts; fixture trees stayed in scratch and
were deleted.

Scratch: `/fast/scratch/hyaku/mado-r51/ExecControlsC1/` (removed before yield; every
receipt was copied into this seat first). Disk guard checked before the pass:
`/fast/scratch/hyaku 64% 293.8G free`.

## Result

All five controls MISS exactly where the frozen claim requires, and the green baseline
passes. Two independent instruments were used, because `w1/ExecLedgerGate/` was empty at
this seat's first read and its draft appeared minutes later:

| instrument | sha256 | controls (a)–(e) |
|---|---|---|
| `w1/ExecLedgerGate/check-tool-ledger.py` (final bytes; draft revised 3x mid-seat, every revision re-run) | `6dd4061c1d8a82d5a9efa8ae954ff1c4559e43abefbb69210fa831bd758a98d4` | 7/7 lines+exits match; selftest 50/50 |
| seat faithful build `controls-c1/check-tool-ledger.py` | `8317cbcca4b9006833177221b394c891391994bb991a8c9a2f100e17ce7296c7` | 7/7 lines+exits match; selftest 9/9 |

Graded tables: `actual-run/compare.txt` and `actual-run/compare-gate.txt` — both
`controls=8 mismatched=0`, exit 0.

| control | P / rows | defect fields | verdict | exit |
|---|---|---|---|---|
| green (`r51-control`) | 79 / 79 | all 0 | TARGET_MET | 0 |
| (a) omit `tools/mado-keysym.py` | 79 / 78 | `uncovered=1` | TARGET_MISSED | 1 |
| (b) five newest tools → `DECOY.md:1` | 79 / 79 | `bad_pointer=5` | TARGET_MISSED | 1 |
| (c) empty desc on all 44 counter rows | 79 / 79 | `empty_desc=44` | TARGET_MISSED | 1 |
| (d) +3 non-population rows | 79 / 82 | `dangling=3` | TARGET_MISSED | 1 |
| (e) lane base `6ca8c55…` | 79 / — | `ledger=absent` | TARGET_MISSED | 1 |
| fixture base (no ledger) | 79 / — | `ledger=absent` | TARGET_MISSED | 1 |

P=79 at every fixture rev and at the lane base (tools 17 + `quality/*.py` 18 +
`quality/counters/*.py` 44), so the fixture population is the real base population.
C=44 counters. Five newest tools derived from base add-commit times, not lexicographic
order: `mado-hostguard.py`, `mado-keysym.py`, `mado-terminal.py`, `mado-devices.py`,
`mado-monitors.py`.

Revision scoping is proved, not assumed: worktree at the green ledger
(blob `85410244…`), `--rev mut-a` (blob `7cb03d7e…`) reports `uncovered=1 ledger_rows=78`
(`actual-run/rev-scope-worktree-green-rev-mut-a.txt`).

## Freeze-critical findings

1. **Summary-schema delta (must be resolved before the freeze).** claims.md requires the
   final line to start `C1_R51:` and to carry `selftest=ok`; the gate draft prints
   `LEDGER:` and no selftest field in a normal run. The counter
   `quality/counters/c1-r51-ledger.py` must emit the frozen prefix/field set (wrap the
   draft or change it). Receipt: `actual-run/frozen-line-vs-gate-schema.txt`.
2. **`--work` on the frozen command.** claims.md runs the counter with `--work <scratch>`;
   the gate draft rejects `--work` outside `--selftest` (exit 2,
   `actual-run/gate-work-flag.txt`). The wrapper must own `--work` and not forward it.
3. **Absent-ledger order.** Both claims.md and the draft use
   `verdict=TARGET_MISSED ledger=absent`; the seat build printed `ledger=absent
   verdict=TARGET_MISSED` (both fields present). Freeze the draft's order.
4. **Duplicate rows.** The frozen sentence says "exactly once" but the frozen line has no
   duplicate field; both instruments charge a duplicate to `dangling` (seat receipt
   `selftest.txt` case `dup-row`, gate cross-check m5). No control in (a)–(d) depends on it.
5. **Description placeholder rule.** The draft treats `-`, `?`, `TBD`, `TODO`, `N/A`,
   `none` as empty, wider than the claim's "non-empty". (c) uses truly empty cells, so it
   is invariant; the freeze should state which rule it intends.
6. **Green baseline is synthetic by design** (`ACCOUNT.md` index pointers). It certifies
   machine-checkability, not pointer *meaningfulness* — the same boundary
   `CritLedgerControls` predicted. `(b)` is robust to a line-scoped pointer reading:
   `DECOY.md:1` and the file contain none of the five basenames.

## Evidence (all under the seat dir)

* `controls-c1/spec.md` — the frozen SPEC: instrument semantics, fixture construction,
  mutation semantics, expected-vs-actual, decision points, hygiene.
* `controls-c1/expected.txt` — exact expected final lines (both schemas, tag and hash revs).
* `controls-c1/actual-run/` — `green.txt`, `ctl-a…d.txt`, `ctl-e-lane-base.txt`,
  `fixture-base-absent.txt`, `selftest.txt`, `hash-green.txt`, `hash-ctl-a…d.txt`,
  `gate-green.txt`, `gate-ctl-a…d.txt`, `gate-ctl-e-lane-base.txt`,
  `gate-fixture-base-absent.txt`, `gate-selftest.txt`, `gate-work-flag.txt`,
  `rev-scope-worktree-green-rev-mut-a.txt`, `work-guard.txt` (tmp/HOME refusals, TMPDIR
  honoured, exit-2 setup errors), `population-per-rev.txt`, `newest-five-tools-derivation.txt`,
  `fixture-toplevel-and-log.txt`, `fixture-blobs.txt`, `frozen-line-vs-gate-schema.txt`,
  `instrument-hashes.txt`, `seat-copy-hashes.txt`, `gate-draft-hash.txt`, `compare.txt`,
  `compare-gate.txt`.
* `controls-c1/make-fixture.py`, `run-all.sh`, `verify-controls.py`, `verify-gate.py` —
  rebuild/re-grade drivers (fresh `git init` fixture from the lane base via `git show`;
  toplevel asserted before every commit).

## Risks / limits

* Fixture commit hashes are run-local (timestamps); the *counts and verdicts* are the
  reproducible part, and both instruments reproduce them independently.
* The gate draft was still in flight (three revisions executed, identical counts;
  `actual-run/gate-draft-history.txt`). If its bytes change before the freeze, re-run
  `verify-gate.py` against regenerated `gate-*.txt`. The expected counts are row-grammar
  invariant, the summary prefix is not.
* `w1/ExecLedgerPopulation` owns the real ledger content; this seat supplies the control
  expectations, not the ledger.

## Hygiene / no-change

* Wrote only this report, the seat dir, and scratch. No tracked lane/fleet file touched, no
  mutating git in the lane or fleet (`git status` shows only untracked w1 seat paths), no
  compositor socket, no config-plane write, no pacman, no service action, no PATH write.
* No tools installed. No scratch dir left behind.

## Deliverables

- `.ufo/waves/round-51/w1/ExecControlsC1/controls-c1/spec.md`
- `.ufo/waves/round-51/w1/ExecControlsC1/controls-c1/expected.txt`
- `.ufo/waves/round-51/w1/ExecControlsC1/controls-c1/actual-run/compare.txt`
- `.ufo/waves/round-51/w1/ExecControlsC1/controls-c1/actual-run/compare-gate.txt`
- `.ufo/waves/round-51/w1/ExecControlsC1/controls-c1/actual-run/green.txt`
- `.ufo/waves/round-51/w1/ExecControlsC1/controls-c1/actual-run/ctl-a.txt`
- `.ufo/waves/round-51/w1/ExecControlsC1/controls-c1/actual-run/ctl-b.txt`
- `.ufo/waves/round-51/w1/ExecControlsC1/controls-c1/actual-run/ctl-c.txt`
- `.ufo/waves/round-51/w1/ExecControlsC1/controls-c1/actual-run/ctl-d.txt`
- `.ufo/waves/round-51/w1/ExecControlsC1/controls-c1/actual-run/ctl-e-lane-base.txt`
- `.ufo/waves/round-51/w1/ExecControlsC1/controls-c1/actual-run/gate-green.txt`
- `.ufo/waves/round-51/w1/ExecControlsC1/controls-c1/actual-run/gate-ctl-a.txt`
- `.ufo/waves/round-51/w1/ExecControlsC1/controls-c1/actual-run/gate-ctl-b.txt`
- `.ufo/waves/round-51/w1/ExecControlsC1/controls-c1/actual-run/gate-ctl-c.txt`
- `.ufo/waves/round-51/w1/ExecControlsC1/controls-c1/actual-run/gate-ctl-d.txt`
- `.ufo/waves/round-51/w1/ExecControlsC1/controls-c1/actual-run/gate-ctl-e-lane-base.txt`
- `.ufo/waves/round-51/w1/ExecControlsC1/controls-c1/actual-run/gate-selftest.txt`
- `.ufo/waves/round-51/w1/ExecControlsC1/controls-c1/actual-run/frozen-line-vs-gate-schema.txt`
- `.ufo/waves/round-51/w1/ExecControlsC1/controls-c1/actual-run/rev-scope-worktree-green-rev-mut-a.txt`
- `.ufo/waves/round-51/w1/ExecControlsC1/controls-c1/actual-run/work-guard.txt`
- `.ufo/waves/round-51/w1/ExecControlsC1/controls-c1/check-tool-ledger.py`
- `.ufo/waves/round-51/w1/ExecControlsC1/controls-c1/make-fixture.py`
- `.ufo/waves/round-51/w1/ExecControlsC1/controls-c1/run-all.sh`
- `.ufo/waves/round-51/w1/ExecControlsC1/controls-c1/verify-controls.py`
- `.ufo/waves/round-51/w1/ExecControlsC1/controls-c1/verify-gate.py`
- `.ufo/waves/round-51/w1/ExecControlsC1/controls-c1/actual-run/selftest.txt`
- `.ufo/waves/round-51/w1/ExecControlsC1/controls-c1/actual-run/hash-green.txt`
- `.ufo/waves/round-51/w1/ExecControlsC1/controls-c1/actual-run/hash-ctl-a.txt`
- `.ufo/waves/round-51/w1/ExecControlsC1/controls-c1/actual-run/hash-ctl-b.txt`
- `.ufo/waves/round-51/w1/ExecControlsC1/controls-c1/actual-run/hash-ctl-c.txt`
- `.ufo/waves/round-51/w1/ExecControlsC1/controls-c1/actual-run/hash-ctl-d.txt`
- `.ufo/waves/round-51/w1/ExecControlsC1/controls-c1/actual-run/fixture-base-absent.txt`
- `.ufo/waves/round-51/w1/ExecControlsC1/controls-c1/actual-run/gate-fixture-base-absent.txt`
- `.ufo/waves/round-51/w1/ExecControlsC1/controls-c1/actual-run/gate-work-flag.txt`
- `.ufo/waves/round-51/w1/ExecControlsC1/controls-c1/actual-run/gate-draft-hash.txt`
- `.ufo/waves/round-51/w1/ExecControlsC1/controls-c1/actual-run/gate-draft-history.txt`
- `.ufo/waves/round-51/w1/ExecControlsC1/controls-c1/actual-run/population-per-rev.txt`
- `.ufo/waves/round-51/w1/ExecControlsC1/controls-c1/actual-run/newest-five-tools-derivation.txt`
- `.ufo/waves/round-51/w1/ExecControlsC1/controls-c1/actual-run/fixture-toplevel-and-log.txt`
- `.ufo/waves/round-51/w1/ExecControlsC1/controls-c1/actual-run/fixture-blobs.txt`
- `.ufo/waves/round-51/w1/ExecControlsC1/controls-c1/actual-run/instrument-hashes.txt`
- `.ufo/waves/round-51/w1/ExecControlsC1/controls-c1/actual-run/seat-copy-hashes.txt`
- `.ufo/waves/round-51/w1/ExecControlsC1/controls-c1/fixture-revs.txt`
- `.ufo/waves/round-51/w1/ExecControlsC1/controls-c1/population-base.txt`

Report: .ufo/waves/round-51/w1/ExecControlsC1.md
