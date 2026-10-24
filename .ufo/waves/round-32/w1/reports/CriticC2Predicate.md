# CriticC2Predicate — attack on C2's FROZEN predicate, counter, controls

Seat: critic (round-32 w1). Target: `.ufo/waves/round-32/registration.md` C2 —
the gate `quality/check-axis-scores.py` and its publication predicate.
All commands run in `/home/vgpnk/Projects/shokunin/mado-shokunin`.

**Worktree hazard note (evidence of a live file):** the lane repo moved while this
report was being written — `HEAD` advanced `9186234` → `50e6a8f` and
`quality/check-axis-scores.py` mutated untracked in-tree (9132 B → 9448 B,
md5 `fe7ef9cf5aa30dfa533253c169c727f5`; the `PUB_RE` per-line parser was replaced
by a flatten-and-`rfind` parser between my first read and my first gate run). All
verdicts below are against the **current bytes** (the 9448 B file). The frozen
predicate is attacked as specified in the registration, not as implemented —
but where the implementation contradicts the frozen spec I say which is at fault.

## Ground truth at HEAD (`50e6a8f`)

```sh
$ git rev-parse HEAD
50e6a8f32bfaf0487b2762eb3b5c9f51ed54b75c
$ python3 -I quality/check-index.py --rev HEAD --repo . | tail -1
MADO_INDEX: rev=HEAD indexed=43/43 missing=0 dangling=0 duplicates=0 coverage=10.0000/10
$ python3 -I .ufo/waves/round-31/c2/count.py HEAD | grep METRIC
METRIC literal lines=42/54 fraction=0.7778
METRIC superseded=[1, 2, 3, 4, 5, 18, 19, 20, 32, 38, 39, 40, 48]
METRIC active=41 resolved_active=41 fraction=1.0000
$ python3 -I quality/check-index.py --selftest | tail -1
MADO_INDEX_SELFTEST: 12/12 assertions passed
```

So observed state at tip: navigation 43/43, calibration **41/41**, operability
**12/12**. The r31 published table says 43/43, 39/40, 9/9.

## Attack 1 — is "stale" the right reading, or an honest base-state record?

**Reading B (honest record).** The published line is
`SCORECARD.md:2014-2017`: "Axis table / re-derived at base (criterion 22):
navigation 43/43 = 1.0; calibration / resolved-active 39/40 = 0.9750 (lowest —
criterion 35's mis-scoped M23-7); / sourced-art 1.0; operability selftest 9/9 =
1.0." The qualifier is explicit: *at base*. I verified the 39/40 is true at
`274f7355` (r30 tip = r31 base) under the r31 v2 rubric:

```sh
$ python3 -I .ufo/waves/round-31/c2/count.py 274f7355 | grep active=
METRIC active=40 resolved_active=39 fraction=0.9750
```

So the sentence asserts a fact about `274f7355` and that fact is true. Under a
strict reading of AXES.md's calibration definition — "SHONEN.md/SCORECARD entries
match observed repo state" — a scoped-at-base entry *does* match observed repo
state (observed *at base*). The tip-state numbers (41/41, 12/12) are also
published, in the r31 results table at `:2023-2024` against `f621e3c0`. No
sentence in the file is false. If calibration is "entries are truthful," the r31
table is clean and the claim's diagnosis is wrong.

**Reading A (stale publication).** "The axis table" is a defined instrument, not
an ordinary prose claim: `registration.md:7-9` of this very round imports the
round-31 numbers verbatim as "the lane's own scored axes (`SCORECARD.md`
round-31 table): coverage/navigation 43/43 = 1.0, calibration resolved-active
39/40 = 0.9750 (lowest)…". The lane *consumes* the last-published axis table as
its current self-assessment — it picks its lowest-axis obligation from it. A
record that is both (a) the last of its kind and (b) consumed as current is the
live publication by convention, whatever its internal scope qualifier says. The
defect is then precise: the lane's *live* published table says 39/40/9-of-9;
observed repo state at every revision after `f621e3c0` is 41/41/12-of-12.
"Entries match observed repo state" supports this reading when "the entry" is
identified functionally — the entry the lane and its readers *use* is the stale
one. The mechanism named in the registration ("never republished after its own
commits moved the counters") is the correct statement of the fault.

**Adjudication.** Both readings are internally coherent; the difference is the
unit of the assertion (the sentence vs. the table-as-instrument). AXES.md's
definition is ambiguous in isolation, but the lane's own behavior resolves it:
the registration itself treats the last axis table as the current one, so
"entries match observed repo state" read at the consumption point is violated.
Reading A wins **by convention evidence, not by text**.

**Verdict: CLAIM SURVIVES** — but the predicate sentence mislabels the mechanism.
"Stale against the counters it names" implies the record became false; it did
not — it is a true base record that *continues to be the live table*. Minimal
predicate repair (wording, not target): replace "is stale against the repo it
describes" with "is the lane's last-published axis table and is consumed as the
current one; at the tip it no longer matches the counters it names." The gate,
counter, and target are unchanged.

## Attack 2 — can the comparison rule be satisfied by publishing any numbers?

The rule is `compare()` (`check-axis-scores.py:62-84`): `pub == der` as a string,
per axis; any non-MATCH (including absent published cell) is a mismatch.

```sh
$ python3 -I quality/check-axis-scores.py --selftest | tail -1
MADO_AXIS_SELFTEST: 17/17 assertions passed   # includes clean-is-zero, stale-rows, one-perturbation-bites
```

- Publishing `82/82` where the instrument derives `41/41` fails: the comparison
  is literal `A/B` string equality, not normalized fraction equality. Equivalent
  fractions do not launder. Only the instrument's literal output string
  satisfies the rule. Not satisfiable by arbitrary numbers.
- Publishing nothing is not satisfiable either — see Attack 3; absence is a
  mismatch, not a skip.
- Residual (inherent, not a defect): the gate tests *values*, not *provenance*.
  A publication of last-round numbers passes whenever the counters are
  coincidentally unchanged. That is correct semantics for a staleness gate —
  staleness is value equality, and a do-nothing republish *should* pass when
  nothing moved.
- Real satisfiability hole found (see Attack 3 for the demonstration): the
  locator is `flat.rfind("Axis table re-derived at")` over the whole file, so
  the "publication" the gate reads is whatever **last utters the marker
  phrase** — a quotation included. Publishing correct numbers does not protect
  the gate from reading somebody else's quoted numbers.

**Verdict: CLAIM SURVIVES** on the comparison rule proper (it demands exactly the
re-derived strings). The locator it feeds from is separately defective — that
damage is charged to Attack 3, not here.

## Attack 3 — is the comparison vacuous when the publication is missing or unparsable? What must the gate do?

Spec'd requirement (prompt): a missing publication must NOT count as a pass. The
registration's frozen predicate is silent on this edge (it only says "reads the
last … line"), so the implementation had to choose. What it does
(`main()`, `:241-244`): `pub is None` → `bad = len(AXES)` = 3, all rows
`NOT-PUBLISHED`, `mismatched=3`, exit 1. A *partially* parsable publication takes
`compare()` where each unpublished axis verdicts `NOT-PUBLISHED` and counts bad.
The edge is closed in the fail-closed direction.

```sh
$ python3 -I quality/check-axis-scores.py --rev 274f7355 --repo .
MADO_AXIS_ROW: axis=navigation published=- derived=43/43 verdict=NOT-PUBLISHED
MADO_AXIS_ROW: axis=calibration published=- derived=- verdict=NOT-PUBLISHED
MADO_AXIS_ROW: axis=operability published=- derived=9/9 verdict=NOT-PUBLISHED
MADO_AXIS_NOTE: instrument absent at 274f7355…: .ufo/waves/round-31/c2/count.py
MADO_AXIS: checked=3 mismatched=3 rev=274f7355…
(exit 1)
```

No publication at `274f7355`, gate exits red — the requirement is met. But this
run exposes **two locator defects** that decide what counts as "missing":

**(a) `rfind` shadowing — any later quotation of the marker phrase replaces the
publication.** Proof against current bytes:

```py
body = ("Round 32. Axis table re-derived at tip: navigation 43/43 = 1.0; "
        "calibration resolved-active 41/41 = 1.0; operability selftest 12/12 = 1.0. "
        "Erratum: the round-31 line 'Axis table re-derived at base (criterion 22): "
        "navigation 43/43 = 1.0; calibration resolved-active 39/40 = 0.9750; "
        "operability selftest 9/9 = 1.0' was base-scoped.")
published_fractions(body) → {'navigation':'43/43','calibration':'39/40','operability':'9/9'}
```

A perfectly correct r32 tip publication is shadowed by an erratum that quotes
the old line — the gate reads the quoted stale numbers and reports STALE.
This is not hypothetical: C2's own fix says "append the correction to the lane's
correction ledger," and this lane's house style (e.g. `SCORECARD.md:1974-2007`)
quotes prior text in errata. **A faithfully executed fix can poison its own
gate.** The frozen predicate's locator ("the last `Axis table re-derived` line")
is the root cause — it specifies an occurrence, not a publication.

**(b) 400-char window truncation.** `line = flat[idx:idx + 400]`; fractions past
400 chars are silently unpublished:

```py
published_fractions("Axis table re-derived at tip: navigation 43/43; " + "x"*380
                    + " calibration resolved-active 41/41; operability selftest 12/12")
→ {'navigation': '43/43'}   # calibration and operability silently NOT-PUBLISHED
```

Fails red (safe direction), but misdiagnoses a verbose publication as missing
and emits `mismatched=2` for a document that is neither missing nor stale.

**Verdict: CLAIM DEAD** — not on the missing-isn't-pass requirement (that part
is implemented fail-closed and verified), but because the locator the predicate
specifies cannot distinguish a publication from a quotation and silently
truncates a legal publication. Minimal predicate repair (the spec, again — the
target `mismatched=0` does not move):

1. Define the publication as the last occurrence of `Axis table re-derived at`
   **that is not inside quotes, code spans, or a corrections/erratum context**
   — or, simpler and more durable, reserve the marker phrase: it may appear
   only in the publication itself, and errata must cite it by `SCORECARD.md:<line>`
   or rev, never re-utter it. Whichever is chosen must be written into the
   predicate, because the current text literally instructs the lane to append a
   correction entry that will commonly quote the line.
2. Bound the parse window to the publication's *sentence/paragraph* (up to the
   next blank line or `.` terminating the axis list), not 400 chars.
3. State the missing/unparsable edge explicitly in the predicate: absent marker,
   or a marker whose re-derivable axes are not all present as `name a/b`,
   counts as a full mismatch — currently this behavior exists only in code, not
   in the frozen spec reviewers will check the gate against.

## Attack 4 — which axes can actually be re-derived, and what must the gate print when one cannot?

Re-derivable set (frozen): navigation (`check-index.py --rev`, `indexed=A/B`),
calibration (`count.py <rev>`, `resolved_active=A active=B`), operability
(`check-index.py --selftest`, `A/B assertions passed`). `sourced-art` has no
committed instrument and is correctly excluded from `AXES` and never claimed —
the "no universal clause" promise holds in code.

When an axis cannot be derived the gate prints the row with `derived=-` and
verdict `NOT-RE-DERIVABLE`, plus a `MADO_AXIS_NOTE:` naming the cause
("instrument absent at <rev>: <path>", "no indexed=A/B in check-index.py
output"). Missing instrument also counts as a mismatch (selftest
`missing-instrument-is-not-a-pass` PASS). Confirmed live: at `274f7355`,
`count.py` does not exist (born r31), and the gate prints
`MADO_AXIS_NOTE: instrument absent at 274f7355…` and counts calibration bad.
Two findings:

- **`checked` misreports.** `main()` prints `checked=%d` as `len(AXES)` — always
  3 — even when only 2 of 3 axes were derivable. At `274f7355` the gate printed
  `checked=3` while calibration was underivable. If "checked" means what it
  says, it must be the count of rows that reached comparison (MATCH/STALE), or
  the report should name the third quantity (`attempted=3 derived=2`).
- **Pass domain is implicitly bounded.** Because the calibration instrument
  exists only from r31, the gate can never print `mismatched=0` at any revision
  earlier than the youngest instrument's birth. That is correct (rev-bounded
  applicability), but the predicate never says it — a reviewer running
  `--rev <old>` sees red and cannot tell defect from out-of-domain. The gate
  should print the pass-domain floor ("applicable from <rev-of-youngest-
  instrument>") or the predicate should state it.
- Non-blocking observation: `run_script` discards the instrument's exit code —
  an instrument that fails (rc≠0) but still prints a parseable fraction is
  accepted as a derivation. For the two real instruments this is currently
  benign (`check-index.py` prints `indexed=A/B` before exiting 1 on defects;
  `count.py` prints METRIC lines then its verdict), and staleness wants the
  numbers not the verdict — but the predicate should decide: is a derivation
  valid only on a clean instrument run? Unspecified.

**Verdict: CLAIM SURVIVES** — the frozen instrument set is real and all three
derive correctly at HEAD (evidence above); the non-derivable case is printed
fail-closed with a named cause. Repairs are spec-level: make `checked` honest,
declare the pass-domain floor, and state the instrument-exit-code rule.

## Attack 5 — is control (c) (perturb 41/41 → 40/41) enough to show the gate bites?

(c) exercises: parser reaches the calibration cell → compare fires → `bad` is
exactly 1 → exit 1. Combined with (a) (stale text must give `mismatched>=1`,
which also exercises the parser over all three cells and yields a MATCH row on
navigation) and (b) (re-derived text gives 0), the three controls cover each
compare branch once. But:

- **(c) only proves the calibration comparator bites.** A gate that hardcoded
  `MATCH` for navigation or operability, or compared derived-to-derived for one
  axis, would pass all of (a) (b) (c). The predicate claims the gate checks
  "each axis it can re-derive" — the controls never prove the navigation and
  operability comparators can turn red. One more perturbation per axis (or a
  combined per-axis control line: perturb navigation, expect `mismatched=1`;
  perturb operability, expect `mismatched=1`) closes it cheaply.
- **(a)'s acceptance is too loose.** It requires `mismatched>=1`; the honest
  expectation for the untouched r31 text at the current tip is *exactly* 2
  (calibration + operability STALE, navigation MATCH — the gate printed exactly
  this at HEAD above). Asserting `=2` catches a gate that spuriously fails a
  third axis; `>=1` does not.
- **No control covers the missing/unparsable edge or the shadowing hole.** The
  scratch set has no (d) no-publication copy and no (e) publication-then-
  quoted-marker copy — the two cases shown in Attack 3 to be real defects.
  Given the fix instructs appending a correction ledger entry, a control that
  appends the r32 publication *plus* a correction that quotes the old line —
  and asserts the gate still reads the r32 publication — is the control this
  predicate actually needs.
- Minor: (c)'s realism depends on the perturbed text being in the parser's
  accepted format; as long as the marker phrase and `axis a/b` cell grammar are
  the contract, that is satisfiable — but it should be said, because the cell
  grammar (`calibration resolved-active N/N`, exact phrase) is an undocumented
  contract: publishing "calibration 41/41" without "resolved-active" parses as
  unpublished and fails red. Fails safe; still a contract to name.

**Verdict: CLAIM DEAD** — (c) as specified proves a single-axis comparator, not
"the gate bites." Minimal predicate repair: keep (c) and add per-axis
perturbation for navigation and operability (each must print `mismatched=1`),
tighten (a) to `mismatched=2`, and add a shadowing control (publication +
correction quoting the stale line → must still `mismatched=0` only when the
quoted line is not mistaken for the publication). These are controls-only
repairs; the claim, counter, and `mismatched=0` target are untouched.

## Summary

| Attack | Verdict | Key evidence |
|---|---|---|
| 1 "stale" vs honest base record | **SURVIVES** (repair: name the currency convention, not falsity) | 39/40 true at `274f7355`; registration itself consumes the table as current |
| 2 any numbers satisfy? | **SURVIVES** | literal `A/B` equality; 82/82 fails; selftest 17/17 |
| 3 missing/unparsable publication | **DEAD** | `rfind` shadowing demo; 400-char truncation demo; missing→`mismatched=3` verified (that part correct) |
| 4 re-derivable set + reporting | **SURVIVES** | 3 axes derive at HEAD; `NOT-RE-DERIVABLE` + NOTE printed; `checked=3` misreports |
| 5 control (c) sufficient? | **DEAD** | single-axis coverage; loose `>=1`; no missing/shadowing control |

Two predicate repairs are required (locator semantics; control coverage); two
are wording-only (currency convention in C2's claim text; `checked`/`pass-domain`
reporting). None narrows the target: `mismatched=0` at tip stands.
