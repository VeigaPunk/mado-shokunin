# Falsify41 — C1 self-pointer/context bypass (executable)

Seat: Falsify41 (leaf; no delegation). Target: C1 self-pointer/context bypass.
Base: `85d57a818c3707397e21c840b6498b105ba798aa`. Lane:
`/home/vgpnk/Projects/shokunin/mado-shokunin`.
Method boundary: frozen claim/registration plus source bytes at the base revision, and
seat-local git fixtures under `/fast/scratch/hyaku/mado-r52/Falsify41/`. No tracked lane
file was created or modified; no package query, live read, host/config/service/compositor
mutation, screenshot, input capture, or lane producer execution occurred. Git mutations were
confined to fixture repos under scratch, with `git rev-parse --show-toplevel` asserted
against each fixture before commit. Scratch was removed after copying receipts (see
Deliverables). No installs.

## Attacked clauses (quoted with locations)

- `claims-frozen.md:7` — "a new committed counter distinguishes the production ledger from a
  no-work control of repeated generic self-pointers using unique population, **non-self
  resolvable evidence targets**, and **instrument-specific context checks**. Demonstrate
  production pass and control fail at the frozen revision."
- `registration.md:7` — "validates population row uniqueness, resolvable evidence pointer,
  **non-self pointer**, and a description containing **instrument-specific functional
  context**. It must pass on the existing production ledger at the base revision and fail on
  `controls/c1-do-nothing.md` specifically for self-pointer/context defects."

Predicate attacked: the pair "non-self resolvable evidence target" + "instrument-specific
context" as a discriminator of work from no-work. The attack does not amend either predicate
and does not claim semantic entailment (excluded by `claims-frozen.md:7`).

## What this seat adds beyond adjacent seats

Adjacent reports already own the control-schema/duplicate confound and the base gate's
acceptance of a population-shaped, every-row-points-at-the-ledger ledger
(`w1/Falsify27.md` D1–D3, `w1/Falsify33.md`, `w1/C1ControlAttack.md`, `w1/Falsify11.md`
F1–F5). In particular Falsify11's `min-counter.py` deliberately implements **neither** new
clause, and its no-work ledger points every row at `quality/tool-ledger.md` itself, so an
implemented self-pointer clause would reject it.

This seat instead runs a candidate counter implementing **all four frozen clauses**
(`w1/Falsify41/candidate-c1-r52.py`) and shows a no-work ledger with **non-self** pointers
and **name-templated** descriptions is indistinguishable from production practice:
`TARGET_MET` on both. New devices demonstrated here:

1. a **generated name census** as the shared non-self pointer target;
2. a **byte-identical copy of the ledger under another path** as the pointer target, which
   defeats a path-inequality reading of "non-self";
3. a context reading that production itself can satisfy only in a weak lexical form
   (functional-verb reading fails 54/82 production rows), and that the template defeats in
   both readings;
4. filename tokens are maximally distinctive against source bytes (df 1–3 of 82), so
   "insert the basename" satisfies even a distinctive-source-token context check.

## Attack A — laundered no-work ledger passes all four clauses

Fixture (`fixtures/laundered`): five real instruments whose bytes are copied from the base
revision with `git show` (`tools/mado-verify.sh`, `tools/mado-binds.py`,
`tools/mado-globals.py`, `quality/counters/c1-r51-ledger.py`,
`quality/check-population.py`); `quality/tool-inventory.md` is a generated census listing the
five basenames only; `quality/tool-ledger.md` has one row per instrument, each description
emitted from one template:

```
| `tools/mado-binds.py` | Read only helper for mado-binds.py; reports config bytes from a file line by line. | `quality/tool-inventory.md` |
```

Command (reproducible; fixture builder and counter are in the seat directory):

```sh
mkdir -p /fast/scratch/hyaku/mado-r52/Falsify41/tmp
export TMPDIR=/fast/scratch/hyaku/mado-r52/Falsify41/tmp
cd /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-52/w1/Falsify41
python3 build-fixtures.py            # commits fixture repos under /fast/scratch/hyaku/mado-r52/Falsify41/fixtures
python3 candidate-c1-r52.py \
  --repo /fast/scratch/hyaku/mado-r52/Falsify41/fixtures/laundered --rev HEAD \
  --work "$TMPDIR/work-laundered"
```

Actual result (`receipts/candidate-laundered.txt`):

```
C1_R52: population=5 ledger_rows=5 uncovered=0 dangling=0 bad_pointer=0 self_pointer=0 no_context=0 dup=0 verdict=TARGET_MET rev=dd052ce3214b
exit=0
```

Same candidate on the production ledger at the frozen base
(`receipts/candidate-production.txt`):

```
C1_R52: population=82 ledger_rows=82 uncovered=0 dangling=0 bad_pointer=0 self_pointer=0 no_context=0 dup=0 verdict=TARGET_MET rev=85d57a818c37
exit=0
```

So the required production pass and a no-work pass are produced by the same instrument
without any distinguishing verdict field. Clause by clause:

| Frozen clause | Candidate implementation | How the no-work ledger satisfies it |
|---|---|---|
| population row uniqueness | one row per tree-derived population path | rows are generated from filenames; one per instrument |
| resolvable evidence pointer | pointer path exists at the revision and its bytes contain the row basename (`candidate-c1-r52.py:110-131`, resolution rule inherited from `c1-r51-ledger.py:196-208`) | the census lists every basename |
| non-self pointer | pointer path ≠ ledger path (`candidate-c1-r52.py:152-164`) | census path differs from `quality/tool-ledger.md` |
| instrument-specific context | non-placeholder, description unique across rows, ≥6 words, ≥2 description tokens present in the instrument bytes (`candidate-c1-r52.py:166-179`) | 5/5 descriptions differ only by the filename token; 14 words; shared tokens are common mechanism words |

The "instrument-specific" content is name-derived, not function-derived
(`receipts/context-bypass.txt`):

```
all descriptions identical modulo basename: True
distinct full descriptions: 5/5
HEADER tools/mado-binds.py: Static resolver for the bind table of a Hyprland v0.56.2 config tree. Reads DIR/.config/hypr/hyprland.conf from bytes only ...
LEDGER  tools/mado-binds.py: Read only helper for mado-binds.py; reports config bytes from a file line by line.
HEADER quality/check-population.py: Round-28 quality check for QUALITY criterion 37 ... a predicate's registered metrics agree with its counter's reported metrics ...
LEDGER  quality/check-population.py: Read only helper for check-population.py; reports config bytes from a file line by line.
```

Two of five accepted descriptions contradict the instrument's own docstring; the accepted
"context" is a filename template. The candidate's `--selftest` also returns the frozen
"explicit red/green receipts" (`registration.md:7`) with the laundered ledger as the green
case (`receipts/candidate-selftest.txt`: `selftest: 2/2 cases ok`), so the selftest clause is
satisfied by the same circular construction.

## Attack B — "non-self" is defeated by a byte-identical copy

Fixture (`fixtures/laundered-copy`): the same five instruments and rows, but each row points
to `quality/tool-ledger-copy.md`, which is **byte-identical** to `quality/tool-ledger.md`:

```sh
F=/fast/scratch/hyaku/mado-r52/Falsify41/fixtures/laundered-copy
sha256sum "$F/quality/tool-ledger.md" "$F/quality/tool-ledger-copy.md"
# facc773a7cc90be6c6d1d6467e75b3fdc921f19ccc46e2647b7ff218193160bd  (both)
python3 candidate-c1-r52.py --repo "$F" --rev HEAD --work "$TMPDIR/work-copy"
```

Actual result (`receipts/candidate-laundered-copy.txt`):

```
C1_R52: population=5 ledger_rows=5 uncovered=0 dangling=0 bad_pointer=0 self_pointer=0 no_context=0 dup=0 verdict=TARGET_MET rev=c9b254c5bfd3
exit=0
```

`self_pointer=0`: the ledger is cited by every row through an alias path. A path-inequality
"non-self" check therefore cannot separate a self-pointer from a non-self pointer; a strict
implementation would have to compare bytes/content, which the frozen predicate does not
require.

## Attack C — the context clause forces a definition the template defeats

The frozen text gives no operational definition of "instrument-specific functional context".
A functional reading (description must contain an activity verb) does not discriminate, and
it also fails production: with `--strict-verb` the same candidate reports
`receipts/candidate-production-strict-verb.txt`
`C1_R52: population=82 ledger_rows=82 ... no_context=54 ... verdict=TARGET_MISSED` (exit 1)
while the laundered fixture still reports `TARGET_MET`
(`receipts/candidate-laundered-strict-verb.txt`). The verb list is seat-chosen, so production's
54 failures are a coverage artifact of that list; but the fabricated template already uses
verbs from it ("reads", "reports"), so broadening the list until production passes leaves the
template accepted. Dropping the verb requirement gives the weak check demonstrated in Attack
A, which the template satisfies. No lexical verb test separates the two artifacts; only the
inference that a different, still-broader list might behave differently remains untested.

A stricter "distinctive source token" reading is also satisfiable from the filename alone: the
basename is present in its own source and in only 1–3 of the 82 instrument sources
(`receipts/distinctiveness.txt`), so inserting the filename satisfies any document-frequency
threshold ≥3 without reading the instrument's function.

## Named control (supporting observation; details owned by adjacent seats)

`fixtures/control-installed-ledger.md` is the frozen control committed verbatim as the ledger
(sha256 `ad72f72f64708d1b877d0f2233f32a065bd11689d644af669176d1844ba2eba6`, matching the
control pin recorded by `w1/Falsify11.md` and `w1/Falsify27.md`). The candidate reports
`receipts/candidate-control.txt`:

```
detail: bad_pointer path=tools/mado-verify.sh pointer='nothing | generic accountability pointer to this ledger itself'
detail: no_context path=tools/mado-verify.sh desc='quality/tool-ledger.md (commentary only)' shared=1 dup=False
detail: dup path=tools/mado-verify.sh
C1_R52: population=1 ledger_rows=2 uncovered=0 dangling=0 bad_pointer=1 self_pointer=0 no_context=1 dup=1 verdict=TARGET_MISSED rev=ece0a0bd25d4
exit=1
```

`self_pointer=0`: under the documented row grammar the control's pointer cell carries no path
token, and the ledger path sits in the description cell (`receipts/control-grammar.txt`; both
the candidate parser and the committed counter's `parse_rows`/`pointer_tokens` imported
in-process give `pointer_tokens=[]`). The control's red is therefore attributable to
duplicate rows, an unresolvable pointer cell, and a short generic description — not to a
self-pointer classification. This corroborates the adjacent-seat findings; it is not this
seat's primary contribution.

Also recorded: the control is not in the frozen base tree
(`git ls-tree 85d57a8 -- .ufo/waves/round-52` is empty; the wave directory is untracked), so
"control fail at the frozen revision" cannot be evaluated by a revision-bound counter without
committing the control bytes; the fixture commit supplies them. This is an operability
limitation for the builder, not a predicate amendment.

## Reproduced

- **A, yes.** A no-work ledger with unique rows, a shared non-self census pointer, and
  filename-templated descriptions receives `TARGET_MET` (exit 0) from a counter implementing
  all four frozen clauses, while the production ledger also receives `TARGET_MET` (82/82).
  Reproduced deterministically; fixture commit SHAs vary only with commit timestamps.
- **B, yes.** `non-self` is satisfied by a byte-identical copy at another path
  (`self_pointer=0`, exit 0).
- **C, yes.** A functional-verb context reading fails production 54/82 while the template
  passes; a distinctive-source-token reading is satisfied by the basename (df 1–3/82).
- **Not claimed:** that the delivered round-52 counter behaves this way (it does not exist at
  base; `claims-frozen.md:7` records "new counter absent"); that prose entailment is
  established; or that the literal production-pass/control-fail demonstration is
  unachievable. It is achievable — the finding is that its green signal carries no
  accountability information against the named bypass class.

## Axes and bounded move

- **Operability** is the affected axis: the frozen checks can be green while the ledger is
  no-work. No coverage harm: the finding does not touch C2 and requires no claim/predicate
  edit. A bounded move (advisory to the builder, not applied): require evidence-target
  independence (reject a target shared by all rows or byte-identical to the ledger) and bind
  at least one description token to an instrument-derived fact that is not its filename;
  report the control's defect classes separately. This stays inside bounded accountability
  checks and does not assert entailment.
- **Coverage**: no effect demonstrated or attempted.

## Limitations

- `candidate-c1-r52.py` is a seat-local stand-in implementing the four clauses in their
  minimal defensible form; a builder may implement stricter tests than the frozen text
  mandates. If so, that is an addition beyond the predicate, and the claim receipt must show
  it firing.
- Pointer resolution uses the r51 rule (path exists; bytes contain the basename), because the
  frozen target strengthens only self-reference, not evidence semantics.
- The control probe imports the committed counter's `parse_rows`/`pointer_tokens` in-process
  for parser parity; it does not run the counter, clone the lane, or write to it.
- No semantic/prose entailment is claimed anywhere; the attack is a lexical-mechanical
  counterexample inside the claim's stated bound.

## Evidence

All evidence below is in `.ufo/waves/round-52/w1/Falsify41/` (hashes in `SHA256SUMS`):

- `candidate-c1-r52.py` — four-clause candidate counter (`describe` at :134, pointer tokens
  at :110, self-pointer at :163, context at :166–179, verdict at :222–232).
- `build-fixtures.py` — deterministic fixture builder; sources instruments via
  `git -C <lane> show <base>:<path>`; asserts fixture toplevel before commit.
- `fixtures/laundered-ledger.md`, `fixtures/laundered-census.md` — the no-work ledger and its
  shared non-self pointer target.
- `fixtures/laundered-copy-pointer-target.md` — byte-identical copy used as pointer target
  (sha256 equals `fixtures/laundered-ledger.md`).
- `fixtures/control-installed-ledger.md` — frozen control verbatim (sha256 `ad72f72f…`).
- `receipts/candidate-production.txt`, `candidate-laundered.txt`,
  `candidate-laundered-copy.txt`, `candidate-control.txt`,
  `candidate-production-strict-verb.txt`, `candidate-laundered-strict-verb.txt`,
  `candidate-selftest.txt` — verdict receipts with exit codes.
- `receipts/context-bypass.txt` — descriptions identical modulo basename and header
  contradictions.
- `receipts/distinctiveness.txt` — basename document frequency across 82 instrument sources.
- `receipts/control-grammar.txt`, `receipts/control-rev.txt` — control cell/pointer parse and
  base-tree absence.
- `receipts/instrument-headers.txt` — base-revision docstrings used for the contradiction check.

Scratch `/fast/scratch/hyaku/mado-r52/Falsify41/` was removed after copying these artifacts;
nothing under `/tmp` was used for evidence. No external source candidate, URL, or access date
applies: every citation is a local repository file at the base revision or an artifact in this
seat directory. This report is a falsification finding, not a vote and not a predicate edit.

## Deliverables

- `.ufo/waves/round-52/w1/Falsify41.md` — this report.
- `.ufo/waves/round-52/w1/Falsify41/SHA256SUMS`
- `.ufo/waves/round-52/w1/Falsify41/candidate-c1-r52.py`
- `.ufo/waves/round-52/w1/Falsify41/build-fixtures.py`
- `.ufo/waves/round-52/w1/Falsify41/fixtures/laundered-ledger.md`
- `.ufo/waves/round-52/w1/Falsify41/fixtures/laundered-census.md`
- `.ufo/waves/round-52/w1/Falsify41/fixtures/laundered-copy-pointer-target.md`
- `.ufo/waves/round-52/w1/Falsify41/fixtures/control-installed-ledger.md`
- `.ufo/waves/round-52/w1/Falsify41/receipts/candidate-production.txt`
- `.ufo/waves/round-52/w1/Falsify41/receipts/candidate-laundered.txt`
- `.ufo/waves/round-52/w1/Falsify41/receipts/candidate-laundered-copy.txt`
- `.ufo/waves/round-52/w1/Falsify41/receipts/candidate-control.txt`
- `.ufo/waves/round-52/w1/Falsify41/receipts/candidate-production-strict-verb.txt`
- `.ufo/waves/round-52/w1/Falsify41/receipts/candidate-laundered-strict-verb.txt`
- `.ufo/waves/round-52/w1/Falsify41/receipts/candidate-selftest.txt`
- `.ufo/waves/round-52/w1/Falsify41/receipts/context-bypass.txt`
- `.ufo/waves/round-52/w1/Falsify41/receipts/distinctiveness.txt`
- `.ufo/waves/round-52/w1/Falsify41/receipts/control-grammar.txt`
- `.ufo/waves/round-52/w1/Falsify41/receipts/control-rev.txt`
- `.ufo/waves/round-52/w1/Falsify41/receipts/instrument-headers.txt`

Report: `.ufo/waves/round-52/w1/Falsify41.md`
