# ExecLedgerGate — C1 checker (`quality/check-tool-ledger.py`), mado round 51 w1

Seat: `ExecLedgerGate` (leaf). Target: the C1 gate that PRED-C1-r51 needs — the tracked
lane-level tool ledger's checker, hermetic `--selftest`, drafted into the seat dir for the L1
to install at `quality/check-tool-ledger.py`.

Status: **complete**. Draft, selftest transcript and real-bytes cross-check are in the seat dir;
no tracked file was edited.

## Deliverables

- `.ufo/waves/round-51/w1/ExecLedgerGate/check-tool-ledger.py`
- `.ufo/waves/round-51/w1/ExecLedgerGate/selftest.txt`
- `.ufo/waves/round-51/w1/ExecLedgerGate/crosscheck.txt`

## What the gate does

`python3 -I quality/check-tool-ledger.py --repo <lane> --rev <rev>` — read-only git (`ls-tree`,
`show`) at the resolved commit sha; writes nothing, prints findings then one summary line.

1. **Population** from the tree at `--rev`, never from the ledger: every blob under `tools/`
   (recursive, any extension), `quality/*.py` (direct children), `quality/counters/*.py`
   (direct children). At base `6ca8c559` = **79** (tools 17, quality top-level 18, counters 44) —
   matches `ExecLedgerCounter`'s and `ExecLedgerPopulation`'s independent sweeps. `.md`, `.txt`,
   `.json`, `quality/q36-successor-run.sh` and subdirectory `.py` are excluded.
2. **Ledger rows** in `quality/tool-ledger.md`: pipe rows outside ```/~~~ fences, header and
   `|---|` separator skipped, exactly three cells — path, description, pointer(s). Path must be
   one population path, exactly once.
3. **Findings**: `uncovered` (population file with no row), `dangling` (row path outside the
   population, duplicate row, or malformed row — not 3 cells), `bad_pointer` (no pointer named;
   a named pointer missing at the rev; no named pointer's bytes name the basename as a *name*,
   so `not-alpha-tool.py` does not cover `alpha-tool.py`), `empty_desc` (blank, whitespace-only
   or placeholder `- ? TBD TODO N/A none`).

Last line, always, six frozen fields in predicate order:

```
LEDGER: population=79 ledger_rows=79 uncovered=0 dangling=0 bad_pointer=0 empty_desc=0 verdict=TARGET_MET rev=6ca8c559...
LEDGER: population=79 verdict=TARGET_MISSED ledger=absent rev=6ca8c559...      # absent ledger
```

Exit 0 iff P>0 and R==P and all four counters are 0; 1 for TARGET_MISSED (absent ledger, empty
population included); 2 for setup/usage errors (unresolvable rev, not-a-repo, non-UTF-8 ledger,
`--work` outside `--selftest`, refused scratch dir). `--selftest` honours `--work`/`TMPDIR`,
refuses `/tmp`, `/var/tmp`, `/dev/shm` and `$HOME`, prints `LEDGER_SELFTEST: 50/50 passed` as
its terminal line, and removes its fixtures in a `finally`.

## Retained evidence (exact lines)

**Hermetic selftest** — `selftest.txt`, `selftest exit=0`, terminal line
`LEDGER_SELFTEST: 50/50 passed`. 50 assertions, count pinned (`SELFTEST_CHECKS = 50`), so a
vanished case fails the run. Arms: green ledger; the five frozen controls (omitted file,
pointer-lacking-basename, empty description, dangling row, absent ledger); pointer-missing;
decoy substring; whitespace description; pointer escape (`/etc/hostname`, `../outside.md`);
duplicate row; malformed 2-cell and 4-cell rows; empty table; fenced row ignored; worktree not
read; `--rev` pins bytes; population globs (nested `tools/`, `quality/sub/*.py` excluded);
empty population; six usage/setup exit-2 arms; three refused work prefixes; home refusal;
`TMPDIR` honoured.

**Real-bytes cross-check** — `crosscheck.txt`. Fixture = `git archive 6ca8c559` (full tree) +
`ExecLedgerPopulation`'s 79-row draft at `quality/tool-ledger.md`; fixture toplevel asserted
before every commit:

- pristine draft → `population=79 ledger_rows=79 uncovered=0 dangling=0 bad_pointer=0
  empty_desc=0 verdict=TARGET_MET`, exit 0 — the peer's real ledger satisfies the gate on the
  real population.
- m1 (drop the row for `tools/mado-hostguard.py`, the round-50 omission) → `uncovered=1`, exit 1.
- m2 (point `tools/mado-keysym.py` at `corpus/SOURCES.md:10`) → `bad_pointer=1
  pointer-lacks-basename:corpus/SOURCES.md`, exit 1.
- m3 (description `-`) → `empty_desc=1`, exit 1.
- m4 (add `tools/mado-ghost.py`) → `dangling=1`, `ledger_rows=80`, exit 1.
- m5 (duplicate the `mado-hostguard.py` row) → `dangling=1
  row-duplicate-line-113`, exit 1.
- base rev in the lane → `LEDGER: population=79 verdict=TARGET_MISSED ledger=absent
  rev=6ca8c559a4a3d6d361101592116eea2bc7452437`, exit 1 (the frozen do-nothing control).
- clone shape (what `ExecLedgerCounter` runs: `--repo` = a `--shared` clone, `--rev` = base) →
  same absent line, exit 1; the gate reads committed bytes only, so a clone is equivalent.
- data-rev shape A (checker + counter land, ledger still 79 rows) → `population=81
  ledger_rows=79 uncovered=2`, both new files named, exit 1.
- data-rev shape B (the two owed rows added, pointer `.ufo/waves/round-51/claims.md`) →
  `population=81 ledger_rows=81 uncovered=0 dangling=0 bad_pointer=0 empty_desc=0
  verdict=TARGET_MET`, exit 0.

**Integration note for the L1 / `ExecLedgerPopulation`:** the two rows below were verified to
pass at the data rev (claims.md names both files verbatim); without them the frozen line cannot
read `ledger_rows=81`:

```
| `quality/check-tool-ledger.py` | PRED-C1-r51 gate: derives the population (tools/, quality/*.py, quality/counters/*.py) at a rev, parses the lane ledger, fails uncovered/dangling/bad_pointer/empty_desc; hermetic --selftest. | `.ufo/waves/round-51/claims.md` |
| `quality/counters/c1-r51-ledger.py` | PRED-C1-r51 counter: runs the ledger gate and an independent population sweep at --rev, emits the frozen `C1_R51:` line. | `.ufo/waves/round-51/claims.md` |
```

## Mutation coverage (answers `MutLedgerGate`'s paper mutants)

Its live mutants are closed in code *and* in the selftest, not just by the five controls:
duplicate rows (8) → `row-duplicate-line-N` in `dangling`; whitespace-only description (11) →
`blank-desc` arm; substring decoy (6) → boundary-aware `names_basename` + `decoy-substring`
arm; population classes/nesting (1, 2) → `population-globs` arm plus the counters omission in
control (a); malformed rows that could vanish (3, 4) → 2-cell and 4-cell arms; traversal and
absolute pointers (7) → `pointer-escape` arm; exit status asserted on every negative arm (9,
10); absent-ledger arm (10) → `control-e`; fixtures are a fresh `mkdtemp` per run and are
removed in `finally`, never reusing bytes across arms (12).

## Residual limitations (disclosed for w2, not hidden)

1. A pointer may name `quality/tool-ledger.md` itself: the frozen sentence says "an existing
   repo file that contains the file's basename", and the ledger is such a file, so a
   self-referential ledger would pass while giving no accountability. The gate stays literal
   rather than stricter than the frozen predicate; the peer ledger does not use self-pointers.
   Measured, not assumed — see the addendum.
2. Containment is name-bounded substring over the pointer file's whole text: a prose mention of
   the instrument anywhere in an existing file satisfies it. That is the predicate's wording.
3. `:<line>` suffixes on pointers are stripped and **not** validated against content — they are
   annotations measured at base, and the predicate asks only for containment.
4. A population filename containing `|` cannot be expressed in a three-cell row: such a file
   reads as a malformed row, i.e. it fails closed (MISS), never silently uncovered.
5. Population counts blobs only; a gitlink or tree entry under `tools/` would be excluded (none
   exist at base).

## Host discipline

No tracked file edited; writes confined to the seat dir and `/fast/scratch/hyaku/mado-r51/
ExecLedgerGate/`, which was deleted after the receipts were copied into the seat dir. No git
mutation in the lane (fixture commits only, each with an asserted toplevel). No tool installed,
no package manager run, no service or compositor socket touched, hostguard read-only. Git at the
lane was read-only (`archive`, `ls-tree`, `show`, `clone --shared --no-checkout`).

Report: .ufo/waves/round-51/w1/ExecLedgerGate.md
Report: .ufo/waves/round-51/w1/ExecLedgerGate/check-tool-ledger.py
Report: .ufo/waves/round-51/w1/ExecLedgerGate/selftest.txt
Report: .ufo/waves/round-51/w1/ExecLedgerGate/crosscheck.txt

## Addendum — the self-pointer residual, measured (post-yield, `MutLedgerGate`'s remaining question)

Control ledger built on the real base tree: all 79 population rows with the basename in their
description and every pointer set to `quality/tool-ledger.md`:

```
LEDGER: population=79 ledger_rows=79 uncovered=0 dangling=0 bad_pointer=0 empty_desc=0 verdict=TARGET_MET rev=82715cfb98021e8e42a4077b88b0664b7d383ff8
exit=0
```

`crosscheck.txt`, section "self-pointer residual". So the hole is real under the literal frozen
wording: an otherwise well-formed ledger can pass while giving no accountability. Two ways to
close it at freeze (the L1's call, not this seat's):

- **(a) leave literal** — record the residual as a known bound; w2 can attack it and the L1 can
  rule on it with this measurement in hand.
- **(b) freeze one sentence** — "the accountability pointer must name a file other than
  `quality/tool-ledger.md`". Implementation is one condition in `evaluate()` (drop that path
  from `pointer_tokens`); `ExecLedgerPopulation`'s 79-row draft still measures
  `population=79 ledger_rows=79 ... verdict=TARGET_MET` unchanged, because its pointers are
  `SCORECARD.md`, `PROVINCE.md`, corpus lessons and round registration files.

Recommend **(b)** if the counter is meant to certify accountability rather than self-reference;
(a) costs nothing if the L1 prefers the predicate exactly as frozen. Either way this is a freeze
decision, so the draft ships with the literal rule and the measurement recorded.

Peer confirmations folded in: `ExecLedgerPopulation` adopted the two data-rev rows with
`.ufo/waves/round-51/claims.md` as pointer (committed at `d2740281`, so the rows do not depend
on a wave-1 report landing at the same tip) and re-measured all 79 rows against three boundary
classes with 0 failures under the name-bounded matcher. `ExecLedgerCounter` accepted the field
layout and parses by name; its clone invocation shape is exercised in `crosscheck.txt`.

Report: .ufo/waves/round-51/w1/ExecLedgerGate.md
