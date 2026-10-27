# Attack06 — W2 attack #06: C1 false positive on a legitimate ledger-reader row

Seat `Attack06` (leaf, no dispatch). Lane root `/home/vgpnk/Projects/shokunin/mado-shokunin`.
Round base `85d57a818c3707397e21c840b6498b105ba798aa`. Axes named: **operability** (C1 is
the operability claim; every item below is an operability measurement) and **coverage**
(untouched by this seat — no C2 artifact, source row, or coverage number is read or moved).

Subject under attack: the round-52 C1 counter
`.ufo/waves/round-52/w1/C1CounterDesign/c1-r52-ledger.py`, sha256
`0fe862f116a789e8f6bebf38dea74b1f5ee20b3c810190ecf295621a3c34dc31`, 847 lines, plus the
frozen claim/registration wording it implements and the frozen control
`controls/c1-do-nothing.md`. The round-51 counter `quality/counters/c1-r51-ledger.py` and
the frozen base receipt are used only as the "before" state.

This is an attack, not a vote. Every verdict below is `reproduced` / `not reproduced` about
a named clause, with the command that produced it; nothing here is a judgement of an
author.

## Verdict summary

| # | attacked clause | outcome | verdict |
|---|---|---|---|
| A1 | C1 "instrument-specific context check" (frozen claim + registration: "a description containing instrument-specific functional context") | an honest, accurate description of the ledger **gate** is rejected; the whole production-shaped ledger flips `TARGET_MET` → `TARGET_MISSED` | **reproduced** (false positive) |
| A2 | same clause, second sibling reader | honest description of the **round-51 counter** rejected by the other reason string (`no-instrument-specific-phrase`) | **reproduced** (false positive) |
| A3 | same clause, `MIN_DESC_WORDS = 5` | honest 4-word description rejected (`too-short:4-words`); 5-word version of the same row accepted | **reproduced** |
| A4 | same clause as a discriminator | forged `PRED-C1-r47 does things.` **accepted** while the honest description of A1 is rejected, same counter, same revision | **reproduced** (neither necessary nor sufficient) |
| A5 | registration "fail on `controls/c1-do-nothing.md` **specifically for self-pointer**/context defects" | the frozen control's `self_pointer=1` comes from the any-cell branch, never the pointer-region branch; disabling the pointer-region branch changes **no** frozen/W1 control verdict | **reproduced** (control does not isolate the clause) |
| A6 | C1 "production pass" carried to the integration revision | the prepared ledger rows for both new counters point at `.ufo/waves/round-52/registration.md`, which is untracked and names neither basename → `bad_pointer=1` once the counter is in population | **reproduced** |
| A7 | the specified legitimate-reader control (C1Simplify control G) | `TARGET_MET` with `note … names-the-ledger-in-prose`, exit 0 — verified independently, not taken on report | **not reproduced** (control stands) |
| A8 | the `note` diagnostic | note text says `names-the-ledger-in-prose` when the named token is the row's **own path**, not the ledger | **reproduced** (mislabeled diagnostic) |
| A9 | production green at the frozen revision | `population=82 ledger_rows=82`, all defect fields 0, `TARGET_MET`, exit 0 | **not reproduced** (green holds; A1–A4 falsify the clause, not the frozen green run) |

The strongest single result: **A1 + A4 together** — on the same row, at the same revision,
with the same pointer, a description that says nothing (`PRED-C1-r47 does things.`) is
accepted and a description that says exactly what the instrument does is rejected.

## A1 — false positive on an honest description of the ledger gate

Two tracked instruments at the base revision read `quality/tool-ledger.md`
(`quality/check-tool-ledger.py`, and `quality/counters/c1-r51-ledger.py` via its
`LEDGER_REL = "quality/tool-ledger.md"`; `quality/counters/c1-r52-ledger.py` is the third
and is absent at base — `grep -l tool-ledger tools/*.py quality/*.py quality/counters/*.py`).
The gate is therefore the canonical legitimate ledger-reader row.

Row substituted into the base ledger at row 82, pointer unchanged
(`.ufo/waves/round-51/registration.md`, which names the basename and is accountable):

```
| `quality/check-tool-ledger.py` | Checks that every tracked instrument in the tool ledger has an accountable evidence pointer. | `.ufo/waves/round-51/registration.md` |
```

Command (exact; `--work` must not be under `/tmp`):

```
python3 -I .ufo/waves/round-52/w1/C1CounterDesign/c1-r52-ledger.py \
  --repo /home/vgpnk/Projects/shokunin/mado-shokunin \
  --rev 85d57a818c3707397e21c840b6498b105ba798aa \
  --ledger .ufo/waves/round-52/w2/Attack06/ledgers/FP-honest-ledger-gate.md \
  --work /fast/scratch/hyaku/mado-r52/Attack06/work
```

Observed:

```
detail: generic_desc path=quality/check-tool-ledger.py reason=bound-only-by-name-path-or-function-words
C1_R52: population=82 ledger_rows=82 uncovered=0 dup=0 dangling=0 bad_pointer=0 self_pointer=0 generic_desc=1 verdict=TARGET_MISSED rev=85d57a818c3707397e21c840b6498b105ba798aa
exit=1
```

Matched control: the same ledger with the **production** description
(`Derives the tracked-instrument population at a revision and checks its accountability
ledger.`) and the same pointer → `generic_desc=0 verdict=TARGET_MET`, exit 0. So the flip
is caused by the description alone, on an otherwise 82/82-clean ledger.

### Mechanism, measured with the counter's own functions

`receipts/03-honest-false-positive.txt`, `drivers/why.py` imports the counter module and
applies `normalize`/`bigrams`/`path_words`/`population_path_words`/`path_fragments`/
`FUNCTION_WORDS` to both the description and `git show 85d57a8:quality/check-tool-ledger.py`:

```
words  = ['checks','that','every','tracked','instrument','in','the','tool','ledger','has','an','accountable','evidence','pointer']
bound  = ['in the', 'tool ledger']
   'in the'      dropped: function-words
   'tool ledger' dropped: own-path-words, population-path-words, path-fragment
own_path_words = ['check','ledger','py','quality','tool']
```

`bound` is non-empty, so the clause cannot say `no-instrument-specific-phrase`; every bound
bigram is then filtered, so it reports `bound-only-by-name-path-or-function-words`. The
description's whole substantive content — *every tracked instrument*, *accountable
evidence pointer* — does not appear verbatim in the instrument's bytes, so it earns nothing.

The point is structural for a ledger reader: the only phrases that bind automatically are
the instrument's **own path words** (`tool ledger`, `check tool ledger`), and those are
precisely the phrases the clause discards as naming vocabulary. Describing ledger reading
accurately therefore requires an incidental word-for-word echo of the tool's source text;
describing it in any other words is scored as generic.

### Sample, and its honest size

Two samples of honest descriptions were written for the two real ledger readers and each
was substituted into the base ledger in turn (`receipts/04-honest-battery.txt`):

| sample | descriptions | rejected by `generic_desc` |
|---|---|---|
| `quality/check-tool-ledger.py`, substantive | 11 | 1 (A1) |
| `quality/counters/c1-r51-ledger.py`, substantive | 5 | 0 |
| both readers, written from behaviour/contract | 10 | 1 (A2) |
| **substantive total** | **26** | **2 (7.7 %)** |
| terse (4 words) honest | 2 | 2 (`too-short`) |

So the false positive is real but not broad — 2 of 26. It is reported with that denominator
rather than as a systemic claim.

### What the clause does track (negative control)

Eleven single-word synonym substitutions on a **passing** description
(`drivers/synonym.py`, `Derives→Computes`, `checks→verifies`, `pointer→target`,
`population→inventory`, `revision→commit`, `every→each`, `ledger→register`,
`accountability→responsibility`, `tracked→recorded`, `instrument→tool`, `at a→for one`) all
still report `TARGET_MET`. The clause is not maximally brittle; it fails only when the
description shares **no** content phrase with the instrument's bytes. That is exactly the
case where a reviewer writes from behaviour instead of from the source.

## A2 — second reader, second reason string

```
| `quality/counters/c1-r51-ledger.py` | Checks that each instrument is covered once and that its pointer mentions its name. | `.ufo/waves/round-51/registration.md` |
```

→ `detail: generic_desc path=quality/counters/c1-r51-ledger.py reason=no-instrument-specific-phrase`,
`generic_desc=1 verdict=TARGET_MISSED`, exit 1
(`ledgers/FP-honest-c1r51-no-overlap.md`). This description is a verbatim-accurate summary
of the gate's checks and contains no name, path or function-word filler; it is rejected
because it echoes no bigram of the tool's own bytes. Together with A1 the two rejection
paths (`bound-only…` and `no-instrument-specific-phrase`) are both reachable from honest
text.

## A3 — `MIN_DESC_WORDS = 5` rejects a terse honest description

Minimal pair on the same row, one word apart (`receipts/08-too-short.txt`):

```
FAIL too-short:4-words   Checks the tool ledger.
PASS -                   Checks each tool ledger row.
```

The frozen registration asks for "a description containing instrument-specific functional
context", not for a word count. `MIN_DESC_WORDS = 5` is the counter's own constant
(line 88) and `C1Simplify` measured a word floor as **non-load-bearing** (identical
verdicts with the floor on and off across green, the frozen control, B/C/D/E). The constant
therefore adds a false-positive surface with no measured discrimination.

## A4 — forged accepted, honest rejected: the clause is neither necessary nor sufficient

Same counter, same revision, same run form (`receipts/05-forged-vs-honest.txt`):

```
== forged  rc=0  TARGET_MET      | `quality/counters/c1-r47-terminal.py` | PRED-C1-r47 does things. | `SCORECARD.md:2660` |
== honest  rc=1  TARGET_MISSED   | `quality/check-tool-ledger.py` | Checks that every tracked instrument in the tool ledger has an accountable evidence pointer. | `.ufo/waves/round-51/registration.md` |
```

This reproduces W1's disclosed ceiling (a content-free description carrying a genuine
prediction-id phrase passes) and pairs it with this seat's finding (a content-full
description without a source echo fails). The two directions together falsify the clause
description "instrument-specific **context** check": the clause measures lexical echo with
the instrument's bytes. It is *not* a falsification of the frozen production green run
(A9), and the frozen claim's own limitation ("bounded accountability checks, not prose
entailment") covers the ceiling but not the false positive — a bounded lexical check still
has to accept honest text it has no reason to reject.

## A5 — the frozen control does not isolate the clause it is cited for

### Which branch fires

`drivers/branch.py` runs the counter's own `rows_of`/`path_tokens`/`measure` on
`controls/c1-do-nothing.md` (`receipts/06-control-isolation.txt`):

```
row=tools/mado-verify.sh cells=4
  desc='quality/tool-ledger.md (commentary only)'
  region=['nothing', 'generic accountability pointer to this ledger itself']
  pointer_region_self=[]  any_cell_self=['quality/tool-ledger.md']
  => branch taken: wide_self (no accountable target)
counts = {uncovered: 81, dup: 1, self_pointer: 1, generic_desc: 1, ...}
```

The control's `self_pointer=1` is produced entirely by the *any-cell* scan over the
**Reads column**, whose token is the bare path `quality/tool-ledger.md`. The
pointer-region clause — the anti-laundering rule that charges a circular pointer even when
the row also names an accountable document, and the clause the C1 claim's "non-self …
evidence targets" names — is never exercised, because the control's pointer region contains
no path token at all.

### Mutant: delete the pointer-region branch

A copy of the counter in scratch with one line changed
(`if pointer_self:` → `if False and pointer_self:`, `drivers/mutate.py`; the lane copy was
never written). Results:

```
green              original=TARGET_MET     mutant=TARGET_MET     SAME
frozen-control     original=TARGET_MISSED  mutant=TARGET_MISSED  SAME
G-pointer-prose    original=TARGET_MISSED  mutant=TARGET_MET     DIFFERS
```

and across every control in the round (`drivers/controlmatrix.py`):

| control | original | mutant | detects mutation? |
|---|---|---|---|
| frozen `c1-do-nothing` | MISSED | MISSED | **no** |
| `mut-selfptr`-equivalent (production row, pointer = ledger only) | MISSED | MISSED | **no** |
| C1Simplify B / C / D / E | MISSED | MISSED | **no** |
| C1Simplify F3 forged / H minimal forgery | MISSED / MET | MISSED / MET | **no** |
| C1Simplify G legitimate reader | MET | MET | **no** |
| this seat's `G-pointer-prose` (accountable pointer **and** ledger named in the pointer cell) | MISSED | MET | **yes** |

So **no frozen control and no W1 control set detects removal of the load-bearing
pointer-region guard**. The red receipt the round can cite is insensitive to the clause it
is cited for. The counter's **own** `--selftest` does detect it (`C1_R52_SELFTEST: 46/53
passed`, exit 1 — the `launder-*` and `self-own-row-*` cases), so the clause is guarded by
the author's selftest, not by the control. That distinction is the finding: the frozen
control's red is not evidence about the pointer-region clause, and the C1 receipt must not
claim it is.

### Why this matters for a legitimate row

The same any-cell branch mislabels an honest row with a broken pointer:

```
fixture V6: | `quality/counters/c1-r52-ledger.py` | Reads `quality/tool-ledger.md` and checks each instrument row. | `.ufo/waves/round-52/registration.md` |
→ detail: self_pointer path=quality/counters/c1-r52-ledger.py target=quality/tool-ledger.md
  self_pointer=1 bad_pointer=0 verdict=TARGET_MISSED
```

The row has **no** self-pointer (its pointer region names one document, not the ledger or
itself); it has an unresolvable naming defect. `self_pointer` and `bad_pointer` are not
distinguishable for this shape, so the field cannot be used as evidence that a row is
circular.

## A6 — "production pass" cannot be carried to the integration revision by the prepared ledger

The working tree already carries an **uncommitted** `quality/tool-ledger.md` diff adding
rows for both new counters. Measured facts (`receipts/07-integration-pointer.txt`):

```
basenames named by .ufo/waves/round-52/registration.md (c1-r52-ledger.py|c2-r52-proposition-entry.py): 0
round-52 paths tracked at the base revision: 0     (round-51: 386)
tracked docs outside .ufo naming c1-r52-ledger.py at base: none
```

and the prepared pointer cell is `.ufo/waves/round-52/registration.md` for both rows.
Scoring the working-tree ledger at the base revision is `dangling=2` (the two paths do not
exist at base). Scoring the same row in a scratch fixture at a revision **where the counter
is in population** (`drivers/mkfixture.sh`, `drivers/fixdrive.py`, case `V2`):

```
| `quality/counters/c1-r52-ledger.py` | PRED-C1-r52: checks complete population, non-self evidence pointers and a bounded lexical context signal; not semantic entailment. | `.ufo/waves/round-52/registration.md` |
→ detail: bad_pointer path=quality/counters/c1-r52-ledger.py pointer='`.ufo/waves/round-52/registration.md`' reason=no-target-names-the-instrument
  bad_pointer=1 verdict=TARGET_MISSED   exit=1
```

The description is not the problem: the same row with a document that does name the
basename (`PROVINCE.md` in the fixture) is `TARGET_MET` (case `V1`). So the C1 green clause
breaks at integration purely because the prepared pointer targets a document that (a) is
untracked and (b) does not name either basename. Two fixes are possible — amend the round-52
registration to name both counters and commit it, or point the rows at a tracked document
that names them. Neither is done in the bytes present.

## A7 — the specified legitimate-reader control is verified (not a finding)

Control G, run verbatim (`receipts/02-control-G.txt`):

```
| `quality/check-tool-ledger.py` | Reads `quality/tool-ledger.md` and reports each instrument's accountability row. | `.ufo/waves/round-51/registration.md` |
→ detail: note path=quality/check-tool-ledger.py names-the-ledger-in-prose target=quality/tool-ledger.md
  self_pointer=0 generic_desc=0 verdict=TARGET_MET   exit=0
```

**Reproduced** exactly as W1/C1Fixture reported. The narrowing works for the shape it was
built for — the ledger named in the description of a row with an accountable pointer.

Boundary, measured: move the same prose into the **pointer cell** of the same 3-cell row
(`ledgers/G-pointer-prose.md`) and the row is charged `self_pointer=1` with the pointer's
primary target still accountable. That is the counter's documented rule ("the pointer region
is the row's accountability claim"), so it is recorded as the boundary of the fix, not as a
defect.

## A8 — mislabeled `note` diagnostic

```
| `quality/check-tool-ledger.py` | `quality/check-tool-ledger.py` reads the ledger and reports each instrument's accountability row. | `.ufo/waves/round-51/registration.md` |
→ detail: note path=quality/check-tool-ledger.py names-the-ledger-in-prose target=quality/check-tool-ledger.py
```

`wide_self` holds `(ledger_rel, path)`; the note string is hardcoded to
`names-the-ledger-in-prose` while the target is the row's **own path**. Minor, but the
receipt is the only place a reader can tell which of the two mechanisms produced
`self_pointer`, so the label has to be right.

## Errors found (report-all)

1. **A1/A2** — honest descriptions rejected as generic (verdict-level false positive).
2. **A3** — `MIN_DESC_WORDS` rejects an honest 4-word description; the constant is not in
   the frozen predicate and was measured non-load-bearing by `C1Simplify`.
3. **A4** — forged description accepted on the same counter/revision where honest text is
   rejected; the clause's name ("instrument-specific context") overstates what it measures.
4. **A5** — the frozen control's `self_pointer` comes from the any-cell branch; no frozen or
   W1 control detects deletion of the pointer-region guard. A red receipt from the frozen
   control is not evidence about the non-self-pointer clause.
5. **A5 (mislabelling)** — `self_pointer` fires on an honest row with an unresolvable
   pointer (fixture V6), so the field conflates two defects.
6. **A6** — the prepared round-52 ledger rows point at an untracked, non-naming document;
   the counter would fail its own production pass at integration.
7. **A8** — `note … names-the-ledger-in-prose` emitted when the target is the row's own path.

## Limitations

* A1–A4 are demonstrated on **honest rewrites** of two rows and on one forged row, not on
  the committed ledger bytes. The committed 82-row ledger passes (A9). So these falsify the
  clause's semantics and the claim's descriptor, not the frozen green measurement.
* The false-positive denominator is 26 substantive descriptions across two rows (2
  rejected) plus 2 terse (2 rejected). It is a sample written by this seat, not a
  population estimate; a different author's phrasings could move it.
* A5's mutant is a scratch copy; the mutation is one condition removed from the guard. It
  shows control **insensitivity**, not that the clause is wrong. The counter's own
  `--selftest` does catch the mutant (46/53, exit 1), which is reported rather than
  suppressed.
* A6 uses a 3-instrument scratch fixture (`drivers/mkfixture.sh`) to put the counter into
  the population; the real integration revision does not exist yet, so the production-scale
  number (`bad_pointer=2` for both rows) is inferred from two measured single-row facts, not
  measured directly as a whole-ledger run.
* Control G's pass (A7) is a reproduction of W1's result on the same bytes; no new claim is
  made about a different counter revision.
* No C2 artifact, corpus file, source row, claim text or counter was modified, and no
  position is taken on C2.

## Methods and safety

* All runs are read-only against the lane: `git show`/`git ls-tree`/`git grep` at the base
  revision plus the counter's own `--ledger` entry point. The one reproducibility fixture is
  a scratch repository built by `drivers/mkfixture.sh` under
  `/fast/scratch/hyaku/mado-r52/Attack06/`; `git rev-parse --show-toplevel` there printed
  the fixture path before any `git add`/`commit`, and the fixture was never inside the lane.
* No tracked file was written. No fleet/sibling/source-repo file was written. No `~/.local/bin`
  or other PATH directory was touched. No git/jj mutation in the lane or the fleet
  (`git status --porcelain --untracked-files=no` in the lane shows only the three
  pre-existing modifications listed below, which this seat did not make).
* No live read, no process/socket/compositor probe, no screenshot, no input capture, no
  producer execution (no `tools/*` instrument was run), no host mutation, no package query
  or transaction, no installation. Scratch `/fast/scratch/hyaku/mado-r52/Attack06/` removed
  after the receipts were copied into this seat directory.
* **Observed lane state, not caused here:** `git status --porcelain --untracked-files=no`
  at review time reports `M corpus/README.md`, `M corpus/SOURCES.md`,
  `M quality/tool-ledger.md`. The ledger modification is the two new counter rows analysed
  in A6. This is reported because C1's "production pass" is measured at `--rev`, so an
  uncommitted ledger does not affect the green run — but it does affect what the round can
  claim about the integrated state.

## Deliverables

- `.ufo/waves/round-52/w2/Attack06.md` — this report.
- `.ufo/waves/round-52/w2/Attack06/receipts/01-baseline.txt` — green, before-state, base receipt.
- `.ufo/waves/round-52/w2/Attack06/receipts/02-control-G.txt` — control G and its pointer-cell boundary.
- `.ufo/waves/round-52/w2/Attack06/receipts/03-honest-false-positive.txt` — A1 mechanism and the matched pair.
- `.ufo/waves/round-52/w2/Attack06/receipts/04-honest-battery.txt` — the 26+2 honest-description sample.
- `.ufo/waves/round-52/w2/Attack06/receipts/05-forged-vs-honest.txt` — A4.
- `.ufo/waves/round-52/w2/Attack06/receipts/06-control-isolation.txt` — A5 branch, mutant, matrix, selftest.
- `.ufo/waves/round-52/w2/Attack06/receipts/07-integration-pointer.txt` — A6 lane facts.
- `.ufo/waves/round-52/w2/Attack06/receipts/07b-fixture-cases.txt` — fixture cases V0–V6.
- `.ufo/waves/round-52/w2/Attack06/receipts/08-too-short.txt` — A3 minimal pair.
- `.ufo/waves/round-52/w2/Attack06/ledgers/` — the exact ledger inputs (byte-level reproduction).
- `.ufo/waves/round-52/w2/Attack06/drivers/` — the drivers that produced every line above.
  They assume `S=/fast/scratch/hyaku/mado-r52/Attack06`; recreate that directory before a
  re-run (`mkfixture.sh` builds the fixture repository under it, and the counter creates
  `--work` itself).

Report: `.ufo/waves/round-52/w2/Attack06.md`
