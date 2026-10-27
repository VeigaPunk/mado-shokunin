# C1Evidence — round-52 C1 measurement-evidence review

Status: evidence-scaffold review complete. The committed C1 red control fails, but not for the frozen defect
set; a grammar-compatible no-work ledger reproduces the round-51 gap and both existing gates pass it. No counter
was written or run (none exists at base), no product/predicate/tracked file was edited, and no source rows were
opened (this seat has no source candidate).

Seat `C1Evidence` · round 52 w1 · lane `mado-shokunin` · base `85d57a818c3707397e21c840b6498b105ba798aa`.
Axes named: **operability** (C1); this report makes no coverage move. Source-only fences held: no host/compositor/
process/journal reads, no input capture, no screenshots, no package queries, no producer execution.

Attacked items (named, not edited): (A1) `controls/c1-do-nothing.md` as red-arm evidence; (A2)
`claims-frozen.md:7` "Demonstrate … at the frozen revision"; (A3) `registration.md:7` "fail … specifically for
self-pointer/context defects". No claim or predicate text was changed.

## 1. Frozen text this review is bound to

- `claims-frozen.md:7` — "Target: a new committed counter distinguishes the production ledger from a no-work
  control of repeated generic self-pointers using unique population, non-self resolvable evidence targets, and
  instrument-specific context checks. Demonstrate production pass and control fail at the frozen revision. Claim
  is limited to bounded accountability checks, not prose entailment. Existing counter at base reports 82/82
  TARGET_MET; new counter absent."
- `registration.md:7` — "It must pass on the existing production ledger at the base revision and fail on
  `controls/c1-do-nothing.md` specifically for self-pointer/context defects. … Selftest includes explicit
  red/green receipts. No predicate amendment after data."
- `registration.md:15` — "C1 do-nothing control `controls/c1-do-nothing.md` is the committed ledger shape with
  only repeated generic self-pointers. … Controls cannot be changed after workers score them."

## 2. Verified base state

All values below are read from committed git objects at the base revision, not copied from
`receipts/c1-base.txt`. Commands and raw output: `C1Evidence/git-facts.txt`, `C1Evidence/evidence-probe.txt`,
`C1Evidence/base-counter-rerun.txt`.

```
$ python3 -I /fast/scratch/hyaku/mado-r52/C1Evidence/probe_base.py
REV=85d57a818c3707397e21c840b6498b105ba798aa resolved=85d57a818c3707397e21c840b6498b105ba798aa
c1_r52_paths_at_rev=0
population=82 tools=17 quality_py=19 counters=46
ledger_rows=82 cell_counts=[3]
dup_paths=0 dup_descriptions=0 paths_outside_population=0
r51_semantics_bad_pointer=0 self_pointer_rows=0 distinct_pointer_files=12
  pointer  42 SCORECARD.md
  pointer  20 PROVINCE.md
  pointer   4 corpus/lessons/round-48.md
  pointer   3 .ufo/waves/round-51/registration.md
  pointer   3 corpus/QUALITY.md
  pointer   2 .ufo/waves/round-40/registration.md
  pointer   2 .ufo/waves/round-45/registration.md
  pointer   2 corpus/lessons/round-44.md
  pointer   1 .ufo/waves/round-44/registration.md
  pointer   1 corpus/lessons/round-25-verifier-spotcheck.md
  pointer   1 corpus/lessons/round-41.md
  pointer   1 corpus/lessons/round-43.md
desc_words min=9 p25=20 median=23 p75=27 max=34 under6=0
desc_zero_distinctive_overlap_with_own_bytes=0
control_bytes=337 control_data_rows=2 control_cell_counts=[4] distinct_tools=1
  control_cells=['tools/mado-verify.sh', 'quality/tool-ledger.md (commentary only)', 'nothing', 'generic accountability pointer to this ledger itself']
  control_cells=['tools/mado-verify.sh', 'quality/tool-ledger.md (commentary only)', 'nothing', 'generic accountability pointer to this ledger itself']
```

Supporting facts (`git-facts.txt`):

| Fact | Command | Result |
|---|---|---|
| base resolves | `git rev-parse <base>^{commit}` | `85d57a818c3707397e21c840b6498b105ba798aa` |
| control is **not** in the base tree | `git cat-file -e <base>:.ufo/waves/round-52/controls/c1-do-nothing.md` | `fatal: path … exists on disk, but not in '<base>'`, exit 128 |
| no round-52 bytes at base | `git ls-tree -r --name-only <base> \| grep -c '^\.ufo/waves/round-52/'` | `0` |
| new counter absent | `git ls-tree -r --name-only <base> \| grep -c 'c1-r52'` | `0` |
| no tracked mention of a new counter | `git grep -c 'c1-r52' <base>` | no output, exit 1 |
| control bytes | `sha256sum …/controls/c1-do-nothing.md` | `ad72f72f64708d1b877d0f2233f32a065bd11689d644af669176d1844ba2eba6`, 337 B |
| base receipt bytes | `sha256sum …/receipts/c1-base.txt` | `f3fdbbafdffbb71b61ed76a934e4cf3a3dccd1fd2f858d364c1b5b11a7c19673` |
| ledger at base | `git show <base>:quality/tool-ledger.md \| sha256sum` | `df5b3705d0291f967c35f0d69d6a908fe37a30d35e84599c4c0f897ca6469e0b` (119 L) |
| r51 counter at base | `git show <base>:quality/counters/c1-r51-ledger.py \| sha256sum` | `d5c2447d098681251fd41c04414d4e8823b41b78f150a5fc6bedd526a4a35b56` (445 L) |
| committed checker at base | `git show <base>:quality/check-tool-ledger.py \| sha256sum` | `6dd4061c1d8a82d5a9efa8ae954ff1c4559e43abefbb69210fa831bd758a98d4` (832 L) |
| tree entry kinds under `tools/`, `quality/` | `git ls-tree -r <base> -- tools quality` | 19 × `100644 blob`, 76 × `100755 blob`; no gitlinks |

`receipts/c1-base.txt` reproduces byte-for-byte in content:

```
$ cd <lane> && TMPDIR=… python3 -I quality/counters/c1-r51-ledger.py --repo . --rev 85d57a8… --work …
detail: checker selftest ok (ratio=50/50 form=with-work)
detail: checker ledger ok (rev=85d57a818c3707397e21c840b6498b105ba798aa)
C1_R51: population=82 ledger_rows=82 uncovered=0 dangling=0 bad_pointer=0 empty_desc=0 selftest=ok verdict=TARGET_MET rev=85d57a818c3707397e21c840b6498b105ba798aa
exit=0
```

[OBS] The production ledger is coverage-complete (82/82), duplicate-free, and every pointer is non-self and
resolvable at base. [INF] The round-51 residual is structural, not incidental: `pointer_resolves` accepts any
listed file whose bytes contain the row basename (`c1-r51-ledger.py:196-208`), and the ledger contains all 82
basenames in cell 1 by construction; `empty_desc` only rejects blank/placeholder text (`:230-232`); the pass gate
reads neither context nor self-targeting (`:415-418`).

## 3. The committed control cannot bear the red arm as written [OBS]

`controls/c1-do-nothing.md` is a four-column table (`Tool | Reads | Writes | Owner and adjacent lanes`) with two
data rows, both `tools/mado-verify.sh`. Production ledger rows are three columns (instrument | description |
pointer). `registration.md:15` calls the control "the committed ledger shape"; it is not — its ledger path sits
in cell 2 and its pointer column holds the literal `nothing`.

Replayed unchanged against the committed checker (fixture: control bytes placed at `quality/tool-ledger.md`, one
instrument; scratch fixture with toplevel assertion, `control-grammar-fixtures.txt`):

```
$ python3 -I <lane>/quality/check-tool-ledger.py --repo …/fix-a --rev HEAD
LEDGER-ROW reason=dangling path=- detail=row-malformed-cells-4-line-3
LEDGER-ROW reason=dangling path=- detail=row-malformed-cells-4-line-4
LEDGER-ROW reason=uncovered path=tools/mado-verify.sh detail=no-row
LEDGER: population=1 ledger_rows=0 uncovered=1 dangling=2 bad_pointer=0 empty_desc=0 verdict=TARGET_MISSED rev=e2aa15d4…
exit=1
```

The same bytes against the unchanged round-51 counter:

```
$ python3 -I <lane>/quality/counters/c1-r51-ledger.py --repo …/fix-a --rev HEAD --work …
detail: bad_pointer path=tools/mado-verify.sh pointer='nothing | generic accountability pointer to this ledger itself'
detail: dup path=tools/mado-verify.sh
C1_R51: population=1 ledger_rows=2 uncovered=0 dangling=0 bad_pointer=1 empty_desc=0 selftest=absent dup=1 checker=absent verdict=TARGET_MISSED rev=e2aa15d4…
exit=1
```

Both fail on row shape (`check-tool-ledger.py:251-253` treats `len(cells) != 3` as malformed → `dangling`;
`:282-289`) and, for the checker, on coverage. Neither reads the self-pointer or the description as such. So the
committed control cannot attribute a failure to the frozen checks, and three defects coincide in it (4-cell
shape, duplicate row, 1-of-82 coverage).

The gap the claim targets does reproduce — with a grammar-compatible no-work ledger (mine, clearly
supplementary, not the frozen control; `sha256 34f41ff199e3197d954d87ca5d0817358835363e029d94d408deb7a7fe9337b8`):

```
| instrument | description | accountability pointer |
|---|---|---|
| `tools/mado-verify.sh` | Generic accountability pointer to this ledger itself. | `quality/tool-ledger.md` |
| `quality/check-tool-ledger.py` | Generic accountability pointer to this ledger itself. | `quality/tool-ledger.md` |
```

```
$ python3 -I <lane>/quality/check-tool-ledger.py --repo …/fix-c --rev HEAD
LEDGER: population=2 ledger_rows=2 uncovered=0 dangling=0 bad_pointer=0 empty_desc=0 verdict=TARGET_MET rev=6d0ca290…
exit=0
$ python3 -I <lane>/quality/counters/c1-r51-ledger.py --repo …/fix-c --rev HEAD --work …
C1_R51: population=2 ledger_rows=2 uncovered=0 dangling=0 bad_pointer=0 empty_desc=0 selftest=ok verdict=TARGET_MET rev=6d0ca290…
exit=0
```

This is the round-51 W2 residual (`corpus/lessons/round-51.md:22-26`, `round-51-verifier-spotcheck.md` §5) made
executable: a self-pointer plus a repeated generic description passes both the committed checker and the r51
counter. It is also the exact shape the new counter must reject, so a green/red pair built only from
`controls/c1-do-nothing.md` cannot show that rejection.

## 4. Evidence requirements for C1 (ER-1 … ER-13)

Each requirement names what must exist, where it derives from, and what would falsify it.

| # | Requirement | Derivation | Falsifier |
|---|---|---|---|
| ER-1 | **Revision closure.** One revision is named and shown by `git ls-tree -r --name-only <rev>` to contain the new counter, the production ledger, **and** the control (or the control is declared external with path + sha256). Every receipt quotes the full resolved sha. | A2; `registration.md:15`; base facts above | control asserted to be "at the frozen revision" while `git cat-file -e <rev>:controls/…` exits 128 (observed at base) |
| ER-2 | **Green arm is second-witnessed.** Exact command, full stdout, exit 0; population/rows/dup/uncovered/self/bad_pointer/context counts must be recomputable from tree bytes by a second implementation (or by the committed checker's rule). | M51-3 analog; round-51 receipt cross-checks were derived from tree bytes | any printed count not derivable from `git ls-tree`/`git show` |
| ER-3 | **Red arm identity + attribution.** Frozen control path + sha256 `ad72f72f…`, the unchanged counter, a non-zero exit, and per-row defect codes. The receipt must say the frozen control fails as *malformed shape/coverage* and must not credit self-pointer/context to a row that was never parsed. A supplementary grammar-compatible fixture (sha256 pinned) carries the self-pointer/generic-description red. | A3; `registration.md:7`; §3 above | single `verdict=TARGET_MISSED` with no clause attribution; or a claim that the frozen control demonstrates self-pointer/context |
| ER-4 | **Clause isolation.** Single-defect fixtures, each grammar-compatible and differing from the production ledger in exactly one clause: (a) self-pointer only, (b) generic description only, (c) duplicate row only, (d) uncovered population only — exact output per fixture. | M51-3 + QUALITY 105 (`corpus/QUALITY.md:580`); frozen control fails 3 clauses at once | only the all-defects control is exercised, so failure cannot be attributed |
| ER-5 | **Context predicate pre-registered.** The operational test of "instrument-specific functional context" is fixed in the counter docstring/selftest *before* the data run (e.g. description must share a distinctive token with the instrument's own committed header/CLI verbs outside a stoplist), and selftest includes a generic-but-nonempty description expected to fail. | A1/A3; "No predicate amendment after data"; M51-2 | definition first appears in the post-run report; a generic string like the control's passes |
| ER-6 | **Non-self is proved, not inferred from resolution.** A `self_pointer=<n>` field; production 0, control ≥1; a pointer to `quality/tool-ledger.md` (or any file that names the instrument only because it enumerates instruments) is self. | round-51 W2 residual (`lessons/round-51.md:22-26`); `c1-r51-ledger.py:196-208` | self-pointer counted as valid because basename appears in the ledger |
| ER-7 | **Coverage, uniqueness, context are separate fields.** `population ledger_rows dup uncovered self_pointer bad_pointer context_fail` printed; a single boolean verdict is insufficient. | `claims-frozen.md:7` ("unique population"); registration clause list | one boolean, or `dup` folded into a generic failure |
| ER-8 | **Selftest content, not a ratio.** Full `--selftest` transcript with named red and green cases and expected/actual verdicts. | `registration.md:7` "explicit red/green receipts"; the r51 counter accepts any `N/N passed` or `selftest=ok` token (`c1-r51-ledger.py:278-300`) | `selftest=ok` or `50/50` alone offered as red/green evidence |
| ER-9 | **Isolation and scratch.** `python3 -I`; `--work` under `/fast/scratch/hyaku/mado-r52/<seat>`; `/tmp`, `/var/tmp`, `/dev/shm` refused; after-run `git status --porcelain` in the lane empty; clone removed. | safety fence; `c1-r51-ledger.py:68` REFUSED_ROOTS precedent | evidence under `/tmp`; lane worktree dirtied |
| ER-10 | **Absent ≠ failed.** At base the new counter misses through a distinct `counter=absent` branch (exit 1), not a traceback; receipt captures it. | `claims-frozen.md:7` "new counter absent"; `c1-r51-ledger.py:382-386` `ledger=absent` precedent | base run exits 2/setup error, or an empty stdout is read as a miss verdict |
| ER-11 | **Population-rule parity + arithmetic closure.** New counter's population must equal the committed rule at the rev (`tools/**`, `quality/*.py` direct, `quality/counters/*.py` direct, blobs only; `check-tool-ledger.py:9-17,163-170`), both counts printed. At a rev that adds one `quality/counters/*.py`, population is 83 and the ledger must be 83 rows. | `claims-frozen.md:7` "unique population"; base 82 = 17+19+46 | `82/82` printed at a rev that contains the new counter (population excludes itself or diverges) |
| ER-12 | **Bounded claim wording.** Report may claim coverage, one row per instrument, resolvability, non-self, a *lexical* context signal, with counts. It may not claim description truth, instrument correctness, prose entailment, or accountability beyond bookkeeping; the context check's false-accept exposure is stated. | `claims-frozen.md:7` last sentence; M51-2 (`lessons/round-51.md:36`) | "accountable"/"verified" asserted for description semantics |
| ER-13 | **Chronology and receipt integrity.** Base-absence receipts cite base + exit codes; the data receipt cites the resolved data sha; integration attaches the exact `quality/check-wave-done.py --repo . --rev <final-tip> --round 52` output before the report (M51-1). Receipts are verbatim files with sha256, never re-typed; any number without a receipt is `[INF]`. | M51-1 (`lessons/round-51.md:37`) | report asserts state the committed receipt does not show |

## 5. Arithmetic trap: the new counter joins its own population

The population rule counts every `quality/counters/*.py` direct child (`check-tool-ledger.py:9-17`). A new
counter committed at `quality/counters/c1-r52-*.py` therefore raises the population from 82 to **83**, and the
production ledger must carry a row for it — with a non-self pointer to a tracked file that names it. At base no
tracked file names any `c1-r52` file (`git grep -c 'c1-r52' <base>` → exit 1), and `registration.md` names no
filename. Consequence for evidence: the data commit must add a naming document (integration SCORECARD row or the
round-52 registration) **before** the green run, or the counter's own row reports `uncovered=1`/`bad_pointer=1`.
Fixture `.py` files placed under `quality/` or `quality/counters/` also enter the population; files under `.ufo/`
do not.

## 6. Round-51 lesson / criterion alignment

| Requirement | Prevents |
|---|---|
| ER-1, ER-13 | M51-1 evidence chronology: a receipt that proves the committed state but not the asserted wave state (`lessons/round-51.md:37`) |
| ER-3, ER-4 | M51-3 falsification fixture mismatch: claiming a bypass/red without exact parser-compatible replay (`lessons/round-51.md:38`, QUALITY 105 `QUALITY.md:580`) |
| ER-5, ER-12 | M51-2 source-truth overreach: structural counters read as semantic proof (`lessons/round-51.md:36`, QUALITY 104 `QUALITY.md:576`) |
| ER-6, ER-7 | round-51 W2 residual: ledger-wide self-pointer and repeated generic descriptions satisfy the lexical predicate (`lessons/round-51.md:22-26`; `round-51-verifier-spotcheck.md` §5) |
| ER-2, ER-8 | round-51's acceptance of a bare selftest ratio and of counter-agrees-with-checker as the only witness (`c1-r51-ledger.py:278-300, 302-340`) |

## 7. Dissent, failed controls, limitations

1. **Dissent (wording).** `claims-frozen.md:7` says "at the frozen revision"; `claims.md:9` (pre-freeze) says "at
   the counter's scored revision". The control is not in the base tree, so the frozen sentence is unsatisfiable
   as written. Resolution used here: the demonstration revision must contain all three artifacts and be named
   explicitly; the report must not claim base-tree containment. No predicate was edited.
2. **Failed control.** `controls/c1-do-nothing.md` fails both existing gates, but through malformed row shape and
   coverage (§3). Registering that failure as evidence of the frozen self-pointer/context checks would be an
   overclaim; the frozen file leaves at most a *shape* red.
3. **Supplementary fixture, not a control replacement.** Fixture C is mine and is reported as supplementary.
   Controls cannot change after scoring (`registration.md:15`); the correct move is to keep the frozen control
   and add clause-isolated fixtures with their own sha256s (ER-4).
4. **Heuristic context probe.** `desc_zero_distinctive_overlap_with_own_bytes=0` over 82 rows (min description 9
   words) is [INF] evidence that a token-overlap context test is *achievable* on this ledger; it is not evidence
   that any description is true or instrument-specific in substance.
5. **No new-counter claim.** `c1-r52` paths at base = 0. Every statement about the new counter in this report is
   conditional on requirements, not an observation of its behaviour.
6. **Mutation coverage is elsewhere.** I did not sweep forgery variants beyond fixture C; that is
   `C1Mutation`/`C1ControlAttack`/`Falsify01-04,09-12,…` work. My probe re-implements the population/pointer
   rules (agreement with the committed checker at base: 82 rows, 0 bad pointers); it does not audit every tree
   edge — at base all population entries are blobs (no gitlinks).
7. **Honesty note.** One earlier run of my probe reported `bad_pointer=20` because it did not lazily load pointer
   targets; the delivered `probe_base.py` loads them and prints `0`, matching the committed checker. The faulty
   intermediate output is not used anywhere.
8. **No installs.** No package, tool, or binary was installed or upgraded; scratch was
   `/fast/scratch/hyaku/mado-r52/C1Evidence/` (disk guard: 600 G available), receipts copied to the seat
   directory, scratch removed at exit.

## Deliverables

- `.ufo/waves/round-52/w1/C1Evidence/evidence-probe.txt` — `probe_base.py` output at base (verbatim).
- `.ufo/waves/round-52/w1/C1Evidence/probe_base.py` — the read-only measurement probe that produced it.
- `.ufo/waves/round-52/w1/C1Evidence/git-facts.txt` — revision/tree/hash facts, including the control's absence from the base tree.
- `.ufo/waves/round-52/w1/C1Evidence/base-counter-rerun.txt` — unchanged round-51 counter at base (reproduces `receipts/c1-base.txt`).
- `.ufo/waves/round-52/w1/C1Evidence/control-grammar-fixtures.txt` — fixtures A/B/C with commands, toplevel assertions, outputs, exit statuses, and the fixture sha256.
- `.ufo/waves/round-52/w1/C1Evidence/run_fixtures.sh` — the driver that rebuilds fixtures A/B/C and produced the receipt above.

Report: .ufo/waves/round-52/w1/C1Evidence.md
