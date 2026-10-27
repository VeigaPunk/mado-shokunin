# C1Fixture — red/green fixture harness for the round-52 C1 counter (prototype)

Seat: `C1Fixture` (leaf, executor). Lane: `/home/vgpnk/Projects/shokunin/mado-shokunin`.
Round base: `85d57a818c3707397e21c840b6498b105ba798aa`. Wave: `w1`.
Axes: coverage + operability. Claim touched: **C1 only** (operability — meaningful
tool-ledger accountability). C2 untouched.

Scope: **the harness only**. This seat does not implement the C1 predicate and does not
implement a counter. It builds the measurement apparatus the C1 claim needs and proves
the apparatus discriminates.

Scratch: `/fast/scratch/hyaku/mado-r52/C1Fixture/` (removed before yield; every receipt
was copied into the seat dir first). Disk guard checked before the work:
`/fast/scratch` on `/dev/nvme1n1p2`, 599 GiB free, 26 % used — no ENOSPC.

Safety: this round is source-only. No package query, no live read (no process, socket or
compositor probe), no input capture, no screenshot, no producer execution, no host,
config, service or compositor mutation, no package transaction. Only file bytes and
read-only git in the lane were touched. Nothing was installed.

## Result

The harness is built, self-tested, and already discriminates: driven against the counter
that exists at the base revision it reports **FAIL on 3 of 5 cases**, which is the gap the
frozen C1 claim names. The harness reproduces the frozen base receipt byte-for-byte on
the green case.

### What was built

`harness/c1-fixture-harness.py` — counter-agnostic. It never imports the counter and
never reads the counter's source; it passes `--repo <fixture> --rev <fixture-rev>
--work <case-work>` and reads stdout, stderr and the exit status only. Summary-line
field names are matched through an **alias set** in `harness/profiles/default.json`, so
a counter author may spell a field `self_pointer=` or `selfptr=` without editing the
harness.

Five fixtures, all built by cloning the lane into scratch:

| case | fixture | expected |
|---|---|---|
| `green` | production ledger at the base revision, untouched | exit 0, `verdict=TARGET_MET` |
| `red` | frozen control `.ufo/waves/round-52/controls/c1-do-nothing.md` committed in place of the ledger, byte for byte | exit 1, `verdict=TARGET_MISSED`, **and** a self-pointer signal and a context signal named |
| `mut-selfptr` | one production row's accountability pointer redirected at `quality/tool-ledger.md` itself | exit 1, self-pointer signal |
| `mut-generic` | one production row's description replaced by `does things.` | exit 1, context signal |
| `mut-duprow` | one production row duplicated | exit 1 |

The `red` expectation is the discriminating one. `TARGET_MISSED` alone is satisfied by
any counter that notices the control's two rows cannot cover the 82-file population; the
frozen claim requires the failure to be *for the self-pointer and context reason*. The
harness therefore rejects a red verdict whose only cause is `ledger=absent` and one that
names neither defect class.

The three `mut-*` fixtures exist because the frozen control cannot separate the two
defect classes from each other: it fails for coverage reasons anyway. Each `mut-*`
fixture injects exactly one defect into an otherwise complete production ledger, so the
defect classes are told apart.

### Harness self-test — the apparatus discriminates

Driver `harness/selftest/run-selftest.sh`, verbatim output:

```
correct: harness_rc=0 verdict=PASS (want PASS) lane_unchanged=True (want True)
always_accept: harness_rc=1 verdict=FAIL (want FAIL) lane_unchanged=True (want True)
writes_source_tree: harness_rc=1 verdict=FAIL (want FAIL) lane_unchanged=False (want False)
writes_in_work: probe_file_observed=yes (want yes)
selftest: ok
```

* `correct` — a counter that passes green and fails red naming both defects is
  **accepted**; the harness is not a fixed FAIL.
* `always_accept` — a counter that always exits 0 with `TARGET_MET` is **rejected** on
  the red case.
* `writes_source_tree` — a counter that writes into the repository it reads is caught:
  `lane_unchanged=False`. The write target is a throwaway repository under scratch,
  never the lane.
* `writes_in_work` — the `--work` argument reaches the counter: the probe file it wrote
  there appears under `scratch_files_after`.

### The base counter under this harness — the measured discrimination gap

Subject: `quality/counters/c1-r51-ledger.py` (the counter present at the base revision).

| case | exit | verdict | harness ok | what the counter reported |
|---|---|---|---|---|
| `green` | 0 | `TARGET_MET` | **True** | `population=82 ledger_rows=82 uncovered=0 dangling=0 bad_pointer=0 empty_desc=0 selftest=ok` |
| `red` | 1 | `TARGET_MISSED` | **False** | `ledger_rows=2 uncovered=81 bad_pointer=1 dup=1` — names neither defect class |
| `mut-selfptr` | 0 | `TARGET_MET` | **False** | `uncovered=0 dangling=0 bad_pointer=0 empty_desc=0` — accepts the self-pointer |
| `mut-generic` | 0 | `TARGET_MET` | **False** | `uncovered=0 dangling=0 bad_pointer=0 empty_desc=0` — accepts the generic description |
| `mut-duprow` | 1 | `TARGET_MISSED` | **True** | `dup=1` — the only defect class it catches |

`lane_unchanged=True`; `HARNESS: verdict=FAIL cases=5`.

Three findings, each measured:

1. **On the frozen control the base counter fails for the wrong reason.** It reports
   `uncovered=81`, `dup=1`, `bad_pointer=1` — the control's two rows cannot cover the
   82-file population. It never says "this pointer points at the ledger itself" or "this
   description is generic". The frozen claim requires the failure to be for the
   self-pointer/context reason, so this is coverage-only accountability.
2. **The base counter accepts a ledger-wide self-pointer.** In `mut-selfptr` the
   redirected pointer resolves (`bad_pointer=0`), because the ledger's own bytes contain
   every instrument basename — the pointer names the file that names the instrument. The
   counter answers `TARGET_MET`. This is the round-51 review finding, reproduced at the
   base revision as a fixture rather than as prose.
3. **The base counter accepts a generic description.** In `mut-generic` the description
   is `does things.` — not empty, so `empty_desc` stays 0 — and the counter answers
   `TARGET_MET`.

### Exact outputs

The green final line the harness produced is **byte-identical** to the frozen base
receipt `.ufo/waves/round-52/receipts/c1-base.txt` (`cmp` → IDENTICAL):

```
C1_R51: population=82 ledger_rows=82 uncovered=0 dangling=0 bad_pointer=0 empty_desc=0 selftest=ok verdict=TARGET_MET rev=85d57a818c3707397e21c840b6498b105ba798aa
```

The harness also asserts this from `harness/profiles/expect-r51-green.txt` via
`--expect-final`; the green case reported `final_line_matches_expected=True` with no
finding.

### Scratch argument and no source-tree writes

Both are measured, not assumed.

* `--work` is passed to the counter and reaches it (self-test case `writes_in_work`). The
  counter runs with `HOME`, `TMPDIR` and the `XDG_*` homes redirected under the case's
  own `--work` directory. The harness lists what the counter wrote there
  (`scratch_files_after`).
* `--work` resolving to `/tmp`, `/var/tmp` or `/dev/shm` is refused before anything is
  created: setup error, exit 2. Verified — `--work /tmp` → exit 2,
  `C1_FIXTURE_HARNESS: setup=error detail=--work must not be a system temp root: /tmp`.
  A missing `--counter` is likewise exit 2.
* The lane is only ever read. Fixtures are `git clone -q --shared --no-checkout` copies
  inside `--work`; the fixture's `alternates` file points at the lane's object store for
  reading. The fixture commits are built with plumbing (`hash-object`, `update-index`,
  `write-tree`, `commit-tree`), so they write into the fixture's object store, not the
  lane's: the lane's object store held **10493 files before and after** the run.
* Before and after the cases the harness takes a git-native integrity snapshot of the
  lane working tree — the index's blob ids for every tracked path, the unstaged diff
  path set, the staged diff path set, and the untracked path set outside the round's wave
  directory. All four hashes are identical: `lane_unchanged=True`. The wave directory is
  excluded because sibling seats write there concurrently while this harness runs; that
  exclusion is reported as a visible count (`wave_untracked_count`), not applied
  silently.
* The fixture working tree is empty by construction, so any file left there is a write.
  `fixture_worktree_residue` was empty for all five cases. (`git status` cannot be used
  for this: on a `--no-checkout` clone every tracked path reads as deleted. The harness
  walks the worktree instead.)
* Every git mutation in a fixture is preceded by an assertion that
  `git rev-parse --show-toplevel` prints that fixture's own path.

### Fixture construction, verified

Mutation application was confirmed by reading the committed bytes back
(`git show HEAD:quality/tool-ledger.md` inside each fixture):

```
fixture-mut-selfptr row 32: | `tools/mado-action-plan.py` | Fail-closed static classifier ... | `quality/tool-ledger.md` |
fixture-mut-generic row 32: | `tools/mado-action-plan.py` | does things. | `PROVINCE.md:20` |
fixture-mut-duprow  rows 32 and 33 identical; row count 86 vs 85
fixture-red         the control's own rows; row count 4
```

Population is 82 at the base revision (tools 17 + `quality/*.py` 19 +
`quality/counters/*.py` 46) in every fixture: the mutations touch the ledger only.

## Independent verification of the peer counter

Seat `C1CounterDesign` answered both of this seat's asks (counter path, summary-line
field names) and reported that this harness returns PASS on all five cases against their
counter. **That claim was re-run here independently rather than taken on report**, against
the bytes present at
`.ufo/waves/round-52/w1/C1CounterDesign/c1-r52-ledger.py`
(sha256 `c0291662a72ad7be22af41f9ce233e46b2aa049236e45daf1f0d0a63e1d63fe6`).

Result: `HARNESS: verdict=PASS cases=5`, `lane_unchanged=True`, all five cases `ok=True`.
The peer's report is confirmed on every case. Both required red signals are non-zero on
the red case (`self_pointer=1 generic_desc=1`), and **no profile edit was needed** — the
counter's field names `self_pointer` and `generic_desc` are already covered by the
profile's alias sets.

| case | exit | counter's line | ok |
|---|---|---|---|
| green | 0 | `population=82 ledger_rows=82 uncovered=0 dup=0 dangling=0 bad_pointer=0 self_pointer=0 generic_desc=0 verdict=TARGET_MET` | True |
| red | 1 | `ledger_rows=2 uncovered=81 dup=1 dangling=0 bad_pointer=0 self_pointer=1 generic_desc=1 verdict=TARGET_MISSED` | True |
| mut-selfptr | 1 | `ledger_rows=82 uncovered=0 dup=0 dangling=0 bad_pointer=0 self_pointer=1 generic_desc=0 verdict=TARGET_MISSED` | True |
| mut-generic | 1 | `ledger_rows=82 uncovered=0 dup=0 dangling=0 bad_pointer=0 self_pointer=0 generic_desc=1 verdict=TARGET_MISSED` | True |
| mut-duprow | 1 | `ledger_rows=83 uncovered=0 dup=1 dangling=0 bad_pointer=0 self_pointer=0 generic_desc=0 verdict=TARGET_MISSED` | True |

### Does the counter generalise, or match the control's text?

A counter that recognised the frozen control by its literal bytes would pass this harness
without measuring anything. Four probes were built against the peer counter that the
peer had not seen, each mutating a **different** ledger row (row 83,
`quality/counters/c1-r49-keysym.py` — not row 1, which is what the `mut-*` fixtures
mutate) with **different** wording:

| probe | row mutated | counter's answer |
|---|---|---|
| 1 | self-pointer **and** generic description | `self_pointer=1 generic_desc=1` exit 1 |
| 2 | generic description, legitimate cell-3 pointer | `self_pointer=0 generic_desc=1` exit 1 |
| 3 | rich instrument-specific description, self-pointer in the pointer cell | `self_pointer=1 generic_desc=0` exit 1 |
| 4 | self-pointer hidden in the **description** cell, legitimate cell-3 pointer | `self_pointer=1 generic_desc=0` exit 1 |

The two signals are separated, not conflated (probes 2 and 3 each fire exactly one); the
counter does not depend on the mutated row being row 1; and none of the four probe rows
resembles the control's text. Probe 4 confirms the peer's stated design — the
self-pointer scan covers every cell after the path cell, not only the ledger's cell 3.

A negative check on the same bytes: the control-shaped literal in the counter appears
**only** inside its own `--selftest` fixture builder (`LEDGER_CONTROL_SHAPE`), not in the
scoring path. Grep for the control's marker text and for `controls/c1-do-nothing.md`
returns hits only in the docstring and that selftest constant. **The counter does not
read the control file.**

### Flagged to the L1 — the gate cross-check clause cannot survive unchanged

The peer reports that their counter does **not** cross-check
`quality/check-tool-ledger.py` the way `c1-r51-ledger.py` did, because that gate's
`LEDGER:` line has no `self_pointer`/`generic_desc` field to agree on. Recorded here so
the L1 sees it: the C1 predicate's gate cross-check cannot survive unchanged, because
the gate at `quality/check-tool-ledger.py` reports only
population/ledger_rows/uncovered/dangling/bad_pointer/empty_desc. Either the gate gains
the two new fields, or the cross-check clause is dropped.

This seat's scope is the harness, so the clause is the counter author's and the L1's to
decide. The harness does not depend on it: it asserts the counter's own summary line and
exit status, and it passes with or without a gate cross-check.

### Re-verification after the peer's `--work` change

The peer then changed one byte-range of their counter (old sha256 `c0291662…`, new
sha256 `39e3d1f4…`, both 685 lines): `resolve_work()` now creates a caller-named
`--work` that does not exist yet, instead of failing, so the L1 can drive the counter
directly. The temp-root refusal and the existing-non-directory refusal are unchanged.

Re-run here against the new bytes, not taken on report:

* Five-case harness: **`HARNESS: verdict=PASS cases=5`**, `lane_unchanged=True`, all five
  `ok=True`; the red case still carries `self_pointer=1 generic_desc=1`.
* `--work` behaviour: fresh path → exit 0 and the directory is created; `/tmp` → exit 2;
  an existing regular file → exit 2 (`exists and is not a directory`).
* Probes P1–P4: reproduce **identically** on the new bytes — the two signals remain
  separated and the wider self-pointer scan is confirmed.

The old bytes were not retained on disk, so a byte-level diff was not possible; the
change was verified behaviourally and by reading the new `resolve_work()`.

### The F3 ceiling, independently confirmed — and wider than flagged

The peer flagged that a description copying a genuine two-word phrase from the
instrument's own bytes still passes. **Reproduced independently**, and a second adjacent
gap was found that the peer did not flag.

The `generic_desc` clause requires: ≥ 5 words; a two-word phrase shared with the
instrument's own bytes; and at least one bound phrase carrying a word the instrument's
*path* does not contribute. That is a **phrase-overlap** measure, not a functional-content
measure.

**E1 — a semantically empty description passes.** Row
`quality/counters/c1-r49-keysym.py`, description
`usr bin and nothing else at all here okay.` — "usr bin" is a genuine two-word phrase
occurring in the instrument's own bytes at the base revision, so the row is accepted:
`self_pointer=0 generic_desc=0 verdict=TARGET_MET`, exit 0. The description says nothing
about the instrument's function.

**E2 — a description made only of the instrument's own path words also passes.** Row
description `c1 r49 tools mado keysym and nothing more here okay.` The bound bigram
`c1 r49` *is* made only of path words and should have triggered `only-path-name-phrase`
— but the description also contains `tools mado`, whose words are not path words, so the
clause's `any(...)` is satisfied by that other bigram. **The guard is per-phrase-ANY, not
per-description, so one unrelated bound bigram anywhere in a long description launders
the whole row.** Verified against the counter's own `normalize`/`bigrams`/`path_words`
functions.

Both are properties of the counter's clause, which this seat does not own. The frozen
claim already limits C1 to "bounded accountability checks, not prose entailment", so
this does not contradict the claim as frozen — but the ceiling is wider than one
phrase-copy, and the wave-2 critic should attack it against that item.

Counter-check that the clause is not simply broken: the genuine production description
for the same row still passes, and the green case shows all 82 production rows carry
`generic_desc=0`.

### Final verification against the peer's latest bytes — and a live defect

The counter changed a second time after the F3/E1/E2 findings were sent (685 → 715 lines, sha256
`eb508569…`). Re-verified rather than assumed:

* Five-case harness: still **`HARNESS: verdict=PASS cases=5`**, `lane_unchanged=True`,
  all five `ok=True`.
* **E1 and E2 were still open at that byte state.** The `generic_desc` clause was
  byte-unchanged in the new file, and both escapes still answered `generic_desc=0
  verdict=TARGET_MET`, exit 0. The +30 lines added a `peer-instrument:` reason to the
  *bad_pointer* clause and a dozen new `--selftest` cases — both genuine improvements,
  neither touching the context clause. **Both were closed in the following byte states**
  (see the final verification section above).
* **A live defect was found at that byte state: the counter's own `--selftest` failed.**
  `FAILED: selftest-count expected=34 got=38` / `C1_R52_SELFTEST: 38/39 passed`, exit 1.
  The new cases raised the check count from 34 to 39 but the module constant
  `SELFTEST_CHECKS = 34` (line 75) was not updated, so the lane's own idiom — a hardcoded
  total, so a silently disappearing case fails the run rather than shrinking it — fired.
  Reproduced twice, deterministically. **Fixed by the peer**; the final bytes report
  `47/47 passed` with `SELFTEST_CHECKS = 47`.

The peer confirmed in writing that their earlier "selftest → 34/34 passed" receipt
referred to the bytes as they stood at that time and was not true of the later bytes, and
added a byte-history paragraph to their report so no receipt is ambiguous. That is the
right resolution: the receipt was true when taken, and the mismatch this seat found was
real and worth reporting.

### Verification against the peer's final bytes — the laundering hole is closed

The counter changed a third, fourth and fifth time as the peer fixed the findings. The
final state is sha256 `0fe862f1…` (847 lines), which the peer reports as complete.
**Every finding this seat raised is now closed on these bytes**, and the peer's own
ceiling and margin claims were independently reproduced.

* `--selftest` → `C1_R52_SELFTEST: 53/53 passed`, exit 0; `SELFTEST_CHECKS = 53` matches.
* Five-case harness → **`HARNESS: verdict=PASS cases=5`**, `lane_unchanged=True`.
* **E1 closed**, **E2 closed** (`generic_desc=1`, exit 1).
* **The laundering hole is closed.** The peer replaced the narrowing with a two-clause
  rule: (1) the ledger or the row's own path named anywhere in the **pointer region**
  (cells 3 and after) is charged **unconditionally**; (2) a ledger mention in some
  *other* cell is charged only when the row designates no accountable target at all.

  All four laundering probes now read `self_pointer=1 verdict=TARGET_MISSED`, exit 1 —
  N4 (pointer cell names the ledger **and** an accountable doc), N5 (4-cell, cell 3 = the
  ledger), N7 (the minimal form) and N8 (ledger plus a document that does not name the
  instrument). Four further shapes were probed against the new rule and none escaped: a
  two-cell row with no pointer region (`self_pointer=1`); the row's own path in the
  pointer region (`self_pointer=1`); the ledger named by a **relative** path form
  (`./quality/tool-ledger.md`, `self_pointer=1`); and the ledger named with a **line
  anchor** (`quality/tool-ledger.md:1`, `self_pointer=1`). The last two matter: a
  tokeniser recognising only the exact string `quality/tool-ledger.md` would have missed
  both.

  The fix **preserves both cases the peer had to protect**: the frozen control still
  yields `self_pointer=1 generic_desc=1` (harness red case), and control-G's shape — an
  honest row whose *description* names the ledger with a legitimate accountable pointer —
  still carries **no** self_pointer charge.

* P1–P4 unchanged: P1 `self_pointer=1 generic_desc=1`; P2 `self_pointer=0 generic_desc=1`;
  P3 `self_pointer=1 generic_desc=0`; P4 `TARGET_MET` with
  `note … names-the-ledger-in-prose` (control-G's shape).
* The peer's new `--ledger <path>` entry point was checked separately: pointed at the
  frozen control it prints `population=82 ledger_rows=2 uncovered=81 dup=1
  self_pointer=1 generic_desc=1 verdict=TARGET_MISSED`, exit 1 — the same verdict as the
  committed-fixture form this seat's harness uses, so the two entry paths agree.

**Two things remain open, and the peer explicitly does not claim them closed:**

1. **The lexical-binding ceiling.** A description quoting any real phrase from the
   instrument's bytes still passes. Re-measured on the final bytes with the 82-row
   sweep: a phrase-copying replacement (`pred c1 does things for the widget registry`) is
   caught on **59** rows and **accepted on 23** — exactly the instruments whose own bytes
   contain `pred c1`. A non-phrase-copying generic description is caught on **82 of 82**.
   The peer's own ceiling row reproduces:
   `| quality/counters/c1-r47-terminal.py | PRED-C1-r47 does things. | SCORECARD.md:2660 |`
   → `generic_desc=0 verdict=TARGET_MET`, exit 0.
2. **The gate cross-check clause.** The peer records it as gate ownership:
   `quality/check-tool-ledger.py` owns population/ledger_rows/uncovered/dangling/
   bad_pointer/empty_desc and says nothing about `self_pointer` or `generic_desc`, so it
   cannot corroborate this counter; this counter owns its own fields and does not
   consult the gate. The two gates are independent and neither verdict constrains the
   other, and the integrator decides whether the round-51 gate gains the two new fields
   or whether this counter stands alone.

The margin measurement stands as previously reported: two rows (`c1-r47-terminal.py` →
`['pred c1']`, `c2-r51-dispatch-entry.py` → `['pred c2']`) survive on exactly one
qualifying phrase, none on zero, and a bad rewrite fails loudly with
`reason=bound-only-by-name-path-or-function-words`.

### The peer's own hole-probe driver — exercised, and proven to discriminate

The peer re-sent the same completed byte state, so nothing changed to re-verify. This
pass instead exercised the peer's *other* deliverables that this seat had not run itself
— their `fixtures/hole-probes.py` driver and their `fixtures/receipts.sh`.

**`HOLE_PROBES: 6/6 rejected`, exit 0** — confirmed. All six probes are rejected with
the expected signal: `ledger-self-pointer` (self_pointer=82), `row-self-pointer`
(self_pointer=82), `peer-instrument-pointer` (bad_pointer=1), `cross-description`
(generic_desc=22), `omnibus-pointer` (bad_pointer=22), `laundered-self-pointer`
(self_pointer=1).

The driver's scoring is a **genuine check, not an exit-code check** — read from its
source, a probe passes only when the counter exits 1 *and* the expected field is present
and non-zero. Proven by substitution: run against a scratch counter that accepts every
ledger, the same driver reports **0/6 rejected, exit 1**, every probe `FALSE-GREEN`. It
therefore discriminates in both directions, not just against the subject under test.

### The C1Simplify control set — every result independently reproduced

The peer reported results for seat `C1Simplify`'s control set. Each was re-run here via
the counter's `--ledger` entry point rather than taken on trust:

| control | self_pointer | generic_desc | verdict |
|---|---|---|---|
| B-row-selfpointer | 82 | 82 | TARGET_MISSED |
| C-ledger-selfpointer | 82 | 0 | TARGET_MISSED |
| D-generic-desc | 0 | 82 | TARGET_MISSED |
| E-one-selfpointer | **1** | 0 | TARGET_MISSED |
| F3-forged | 0 | **10** | TARGET_MISSED |
| G-legit-ledger-reader | 0 | 0 | **TARGET_MET** |
| H-minimal-forgery | 0 | 0 | **TARGET_MET** |

All figures confirmed, including `generic_desc=10` on F3-forged. The two `TARGET_MET`
controls are the load-bearing ones and are correct: **G** — an honest row whose
description names the ledger (the very tool whose job is to read it) passes, with the
mention recorded as an unscored `note … names-the-ledger-in-prose`; **H** — the
disclosed ceiling, which the peer states in their own report rather than hiding. Every
`TARGET_MISSED` control names its defect class rather than failing on coverage, and
**E** shows the counter counts precisely (`self_pointer=1`, not 82).

**Why F3-forged is caught on only 10 of 82 rows — the mechanism.** Measured with the
counter's own `normalize`/`bigrams`/`path_words`/`path_fragments`/`FUNCTION_WORDS`:

* `tools/mado-action-plan.py`, desc `Generic accountability note 0 mado action plan py.`
  → bound bigrams `['mado action', 'action plan', 'plan py']`, surviving after the four
  filters: **none** → **rejected**; every bound bigram is made of the instrument's own
  path words.
* `tools/mado-anims.py`, desc `Generic accountability note 1 static resolver for the.`
  → bound bigrams `['static resolver', 'resolver for', 'for the']`, surviving:
  **`['static resolver', 'resolver for']`** → **accepted**; "static resolver" is a
  genuine phrase in that instrument's own bytes, and it is not path words, not a path
  fragment and not function words.

So the 10 is not arbitrary: it is the number of rows whose filler is built *only* from
that instrument's own path words. The other 72 carry a functional phrase lifted from the
instrument's header — the very thing an honest description would use — so the phrase test
cannot tell them apart. This is the **same lexical-binding ceiling** this seat measured
independently by replacing each row's description with `pred c1 does things …` (caught 59,
accepted 23): different phrase, same defect. The clause binds a description to the
instrument's bytes *lexically*, and the instrument's bytes contain the functional phrases
an honest description would use. The frozen claim limits C1 to "bounded accountability
checks, not prose entailment", so this does not contradict the claim as frozen — and the
peer records it with its construction rather than claiming it closed.

### The peer's own ceiling and margin claims — independently measured

Both confirmed on the final bytes, and the ceiling quantified.

**Ceiling — a description quoting any real phrase from the instrument's bytes still
passes.** The peer's exact example reproduces:
`| quality/counters/c1-r47-terminal.py | PRED-C1-r47 does things. | SCORECARD.md:2660 |`
→ `generic_desc=0 verdict=TARGET_MET`, exit 0.

Sweeping **each of the 82 production rows** in turn, replacing that row's description:

| replacement description | caught | accepted |
|---|---|---|
| `pred c1 does things for the widget registry` (phrase-copy) | 59 | **23** |
| `does something useful for the widget registry checks` (no phrase copy) | **82** | 0 |

The 23 accepted rows are exactly the instruments whose own bytes contain `pred c1`. So
the ceiling is precisely the phrase-copy one, and it is wide: a prediction-id phrase
launders a generic description on 23 of 82 rows.

**Margin — two rows survive on exactly one qualifying phrase, and that phrase is their
prediction id.** Measured with the counter's *own* four filters (`normalize`,
`bigrams`, `path_words`, `path_fragments`, `FUNCTION_WORDS` imported from the counter
module, so the margin is measured with its filters and not an approximation):
rows with ≤ 1 surviving qualifying phrase = **2**
(`c1-r47-terminal.py` → `['pred c1']`, `c2-r51-dispatch-entry.py` → `['pred c2']`);
rows with 0 surviving = **none**. The tip is visible and named: a description with no
qualifying phrase yields `generic_desc=1 reason=bound-only-by-name-path-or-function-words`.

**Compound attacks on the ceiling — the other clauses still hold.** ceiling +
self-pointer → `self_pointer=1`, exit 1. ceiling + no accountable pointer →
`bad_pointer=1`, exit 1. The `generic_desc` ceiling does not open the `self_pointer` or
`bad_pointer` clauses.

## Limitations

* **The harness does not implement the predicate.** It cannot say whether a counter is
  *correct*; it says whether a counter *discriminates* the frozen control from the
  production ledger. A counter that fails green for an unrelated reason is reported as a
  green failure, not diagnosed.
* **The defect signals are matched by alias, not by exact field name.** The frozen claim
  does not fix the new counter's summary field names. The alias set in
  `harness/profiles/default.json` covers the plausible spellings; a counter author who
  picks an unlisted spelling must add it there, or the harness will report the signal
  missing. The `detail:` regexes catch counters that report the defect only in prose
  lines.
* **The red case requires both signals.** The frozen claim's wording is "self-pointer /
  context defects"; the harness requires both to be present. A counter that reports only
  one would be failed on the red case — a deliberate reading of the claim, recorded here
  so a reviewer can relax it via `required_red_signals` in the profile.
* **`mut-*` fixtures are this seat's construction, not frozen controls.** The frozen
  control set contains `c1-do-nothing.md` only. The `mut-*` fixtures are additional
  measurement apparatus, built by the harness; they mutate only the ledger, never the
  control file, and they are not written to `.ufo/waves/round-52/controls/`.
* **Fixture revision hashes are run-local** (the fixture commits carry the harness's own
  commit time). The reproducible parts are the case verdicts, the field values and the
  lane's revision.
* **The base counter's `checker=failed` on three cases** means the lane's own
  `quality/check-tool-ledger.py` also rejected those ledgers. That is a second,
  independent witness of the same three defects, not a harness artefact.
* The `mut-selfptr` and `mut-generic` fixtures mutate the **first** ledger row
  (`tools/mado-action-plan.py`). A counter that special-cases that one row would evade
  them; the harness does not randomise the target row, so a mutant-resistant sweep is
  left to the mutation seat. (The four probes against the peer counter, which mutate row
  83, close that gap for that counter.)
* **The harness cannot see the context-clause ceiling.** Its `generic_desc` check is a
  *count* of the counter's own field: it fires when the counter reports a non-zero
  count. A counter whose context clause accepts a semantically empty description still
  reports `generic_desc=0`, and the harness records the case as passing. The ceiling was
  found only by hand-building such a description, which is exactly the kind of attack
  the wave-2 critic seat must run. The harness is not a substitute for it.
* **The harness cannot see laundering shapes either.** `mut-selfptr` puts the ledger in
  the pointer cell with no other accountable target; a laundering shape needs a
  *second* cell naming an accountable document, which the harness's fixture never
  builds. **All three defects found in the peer counter (E1, E2, the laundering hole)
  were found by hand-built probes, not by the harness** — the honest measure of what the
  harness does and does not buy, and the reason the wave-2 critic seat is not redundant
  with this one.
* **The harness would not have caught the laundering hole even if it had run the
  counter's own `--selftest`.** The stale `SELFTEST_CHECKS` defect was found by running
  the counter's selftest directly; the harness asserts only the counter's summary line
  and exit status against its fixtures.

## Dissent / failed controls

* The harness reports **FAIL** against the base counter. That is the expected and
  intended result — it is the measurement of the gap C1 names, not a defect of the
  harness. It is *not* a vote on the round-52 counter, which does not exist yet at the
  base revision.
* One harness check was **wrong on the first run and was fixed**: the scratch-confinement
  check originally used `git status --porcelain` on the fixture, which reported every
  tracked path as deleted on a `--no-checkout` clone and produced 30+ false "counter
  wrote into the repository it reads" findings. Replaced with a filesystem walk of the
  worktree excluding `.git/`; the false findings are gone and `fixture_worktree_residue`
  is empty for all five cases.
* One harness check was **too strict on the first run and was fixed**: the integrity
  comparison initially compared the whole snapshot dict, which included
  `wave_untracked_count` — a count that legitimately changes when this seat writes its own
  receipts mid-run, producing a false `lane_unchanged=False`. The strict views are now
  separated from the informational counts.
* The self-test's `writes_source_tree` stub **initially wrote into the fixture** rather
  than the watched repository, so the detector did not fire; the stub was changed to
  resolve the fixture's `origin` remote, which is the watched repository.

## Notes for the counter author

The harness is ready to run against the new counter:

```
python3 -I .ufo/waves/round-52/w1/C1Fixture/harness/c1-fixture-harness.py \
  --repo /home/vgpnk/Projects/shokunin/mado-shokunin \
  --rev 85d57a818c3707397e21c840b6498b105ba798aa \
  --counter <absolute path to the new counter .py> \
  --profile .ufo/waves/round-52/w1/C1Fixture/harness/profiles/default.json \
  --work /fast/scratch/hyaku/mado-r52/C1Fixture/run-<name> \
  --out <evidence dir> \
  --cases green,red,mut-selfptr,mut-generic,mut-duprow
```

A passing run needs: exit 0 + `TARGET_MET` on green; exit 1 + `TARGET_MISSED` on every
red-family case; a self-pointer signal on `red` and `mut-selfptr`; a context signal on
`red` and `mut-generic`; no fixture-worktree residue; and `lane_unchanged=True`.

`--overlay <repo-relative path>[,...]` is available for a counter that needs a companion
file (a checker or helper) that does not exist at the frozen base revision: the file is
copied from the lane working tree into the fixture and committed there. The ledger can
never be overlaid. `--expect-final <file>` asserts the exact final line per case, as
`harness/profiles/expect-r51-green.txt` does for the base counter.

Both were exercised: `--overlay quality/check-tool-ledger.py --cases green` → `verdict=PASS
cases=1`, `lane_unchanged=True`; `--overlay quality/tool-ledger.md` → setup error,
`--overlay may not replace the ledger`, exit 2.

The message to seat `C1CounterDesign` carries the same usage plus the measured
base-counter results, so the new counter can be checked against them directly. The peer
replied with their counter's contract; this seat re-ran the harness against their bytes
independently and confirmed PASS on all five cases, plus four further generalisation
probes (see *Independent verification of the peer counter*). Their counter needs no
change to this harness's profile.

## Hygiene / no-change

* Wrote only this seat's directory (`w1/C1Fixture/`) and this report. No tracked lane
  file, no fleet file, no sibling seat file, no `quality/` file, no corpus file.
* No git or jj mutation in the lane or the fleet. `git status --porcelain
  --untracked-files=no` in the lane is empty; the lane's object store is unchanged at
  10493 files.
* No package transaction, no install, no PATH write, no service or compositor action, no
  live probe, no screenshot, no input capture. Read-only git and file bytes only.
* The peer counter was read and executed across six byte states and never written; its
  sha256 is unchanged at `0fe862f116a789e8f6bebf38dea74b1f5ee20b3c810190ecf295621a3c34dc31`.
* Scratch `/fast/scratch/hyaku/mado-r52/C1Fixture/` removed on exit; every receipt was
  copied into the seat dir first.

## Deliverables

- `.ufo/waves/round-52/w1/C1Fixture/harness/c1-fixture-harness.py`
- `.ufo/waves/round-52/w1/C1Fixture/harness/README.md`
- `.ufo/waves/round-52/w1/C1Fixture/harness/profiles/default.json`
- `.ufo/waves/round-52/w1/C1Fixture/harness/profiles/expect-r51-green.txt`
- `.ufo/waves/round-52/w1/C1Fixture/harness/selftest/run-selftest.sh`
- `.ufo/waves/round-52/w1/C1Fixture/harness/selftest/stub-correct.py`
- `.ufo/waves/round-52/w1/C1Fixture/harness/selftest/stub-always-accept.py`
- `.ufo/waves/round-52/w1/C1Fixture/harness/selftest/stub-writes-source-tree.py`
- `.ufo/waves/round-52/w1/C1Fixture/harness/selftest/stub-writes-in-work.py`
- `.ufo/waves/round-52/w1/C1Fixture/receipts/evidence-table.txt`
- `.ufo/waves/round-52/w1/C1Fixture/receipts/peer-counter-verification.txt`
- `.ufo/waves/round-52/w1/C1Fixture/receipts/peer-counter-reverification.txt`
- `.ufo/waves/round-52/w1/C1Fixture/receipts/peer-counter-final-verification.txt`
- `.ufo/waves/round-52/w1/C1Fixture/receipts/peer-counter-final2-verification.txt`
- `.ufo/waves/round-52/w1/C1Fixture/receipts/peer-counter-final3-verification.txt`
- `.ufo/waves/round-52/w1/C1Fixture/receipts/peer-counter-final4-verification.txt`
- `.ufo/waves/round-52/w1/C1Fixture/receipts/simplify-controls-verification.txt`
- `.ufo/waves/round-52/w1/C1Fixture/receipts/peer-deliverables-verification.txt`
- `.ufo/waves/round-52/w1/C1Fixture/receipts/r51-base/harness-summary.json`
- `.ufo/waves/round-52/w1/C1Fixture/receipts/r51-base/green.stdout.txt`
- `.ufo/waves/round-52/w1/C1Fixture/receipts/r51-base/green.stderr.txt`
- `.ufo/waves/round-52/w1/C1Fixture/receipts/r51-base/red.stdout.txt`
- `.ufo/waves/round-52/w1/C1Fixture/receipts/r51-base/red.stderr.txt`
- `.ufo/waves/round-52/w1/C1Fixture/receipts/r51-base/mut-selfptr.stdout.txt`
- `.ufo/waves/round-52/w1/C1Fixture/receipts/r51-base/mut-selfptr.stderr.txt`
- `.ufo/waves/round-52/w1/C1Fixture/receipts/r51-base/mut-generic.stdout.txt`
- `.ufo/waves/round-52/w1/C1Fixture/receipts/r51-base/mut-generic.stderr.txt`
- `.ufo/waves/round-52/w1/C1Fixture/receipts/r51-base/mut-duprow.stdout.txt`
- `.ufo/waves/round-52/w1/C1Fixture/receipts/r51-base/mut-duprow.stderr.txt`
- `.ufo/waves/round-52/w1/C1Fixture/receipts/selftest/correct/console.txt`
- `.ufo/waves/round-52/w1/C1Fixture/receipts/selftest/correct/harness-summary.json`
- `.ufo/waves/round-52/w1/C1Fixture/receipts/selftest/always_accept/console.txt`
- `.ufo/waves/round-52/w1/C1Fixture/receipts/selftest/always_accept/harness-summary.json`
- `.ufo/waves/round-52/w1/C1Fixture/receipts/selftest/writes_source_tree/console.txt`
- `.ufo/waves/round-52/w1/C1Fixture/receipts/selftest/writes_source_tree/harness-summary.json`
- `.ufo/waves/round-52/w1/C1Fixture/receipts/selftest/writes_in_work/console.txt`
- `.ufo/waves/round-52/w1/C1Fixture/receipts/selftest/writes_in_work/harness-summary.json`

Report: .ufo/waves/round-52/w1/C1Fixture.md
