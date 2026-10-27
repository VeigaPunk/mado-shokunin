# Falsify14 — round 52 w1

Seat: `Falsify14` (critic, falsification item 14), wave `w1`. Lane repo
`/home/vgpnk/Projects/shokunin/mado-shokunin`, base `85d57a818c3707397e21c840b6498b105ba798aa`.
Claim attacked: **C2 — coverage: proposition-bound dispatcher source entry**, specifically the
completeness half of the frozen predicate — registration wording: *"every material factual
proposition is mapped. A counter checks proposition count, row/pin/quote bindings and complete
mapping"*, and claim wording *"each material factual proposition maps to a pinned source quote
<=25 words and explicit support rationale"*. The attack is executed against the actual artifact
under construction: the draft counter `w1/C2CounterDraft/c2-r52-proposition-entry.py` (clause (e),
"the mapping is complete") and its staged fixture.

## Verdict up front

The draft counter's completeness clause is **S###-row-citation closure over non-table,
non-marker prose lines** (`cited_rows()`, draft counter lines 596-611: it collects `S\d{3,}` ids
from unfenced prose lines, skipping lines that start with `|` and lines matching
`^\s*(held|ground|lane|round|wave|base|verified-at|recheck)\b`). It is blind to material factual
propositions that:

- **M1** carry pin locators and verbatim quotes in narrative prose with **no S### row citation**;
- **M2** sit on a **marker-exempt line** (`recheck:`, `held:`, … — the whole line is skipped);
- **M3** sit in **any markdown table other than the proposition map** (the r51 exemplar's
  "State claims (criterion 100)" table is exactly this shape).

All three smuggled-claim mutants, plus a **M4** control that rebinds a proposition to a real,
verbatim, in-span quote that does not support it, run **5/5 clauses, `admitted=1/1
verdict=TARGET_MET`, exit 0** against the draft counter (receipts below). The in-lane canonical
exemplar of this entry format — the admitted round-51 entry — itself carries material factual
claims in all of those out-of-map surfaces, including one that was factually wrong
(`special_handlers=5`, corrected by the round-51 w2 errata), and the unchanged round-51
structural counter still passes it 4/4 at the frozen base after that 7-item source-truth errata.

**Reproduced: yes** — three distinct completeness bypasses and one support-side residual, live,
against the actual draft counter and its own staged fixture.

## Axes

| axis | this seat's move | direction |
|---|---|---|
| coverage | shows the r52 C2 completeness clause as drafted does not establish "every material factual proposition is mapped"; names three concrete prose channels that defeat it | guards the claim's intent (no axis credit claimed) |
| operability | none | unchanged |
| freshness / others | no substrate, host, service, fleet or lane file touched; scratch clone only | no harm claimed, none observed |

## What the draft counter's clause (e) actually checks

From `w1/C2CounterDraft/c2-r52-proposition-entry.py`:

- lines 596-611 `cited_rows()`: `S###` ids from **unfenced prose lines only**; lines starting
  with `|` are skipped (`if s.startswith("|"): continue`); lines matching `MARKER_RE`
  (`held|ground|lane|round|wave|base|verified-at|recheck`) are skipped wholesale.
- lines 613-653 `clause_e()`: notes fire only for `row_unmapped` (prose row not in the map),
  `row_uncited`, `rows_too_few`, `duplicate_quote`, `duplicate_claim`, and `quote_not_used`
  (each *map* proposition's quote must appear in prose — a one-directional anti-padding check).
- The docstring itself disclaims entailment: "It does NOT decide whether a quote entails the
  proposition it is attached to."

Nothing in clause (e) scans prose for **locator tokens (`Pin:line`) or quoted spans not attached
to a proposition**. Completeness is verified only for claims that cite an `S###` row in the
right kind of line.

## Attack M1 — smuggled locator claim in narrative prose (no row)

**Setup:** build the counter seat's staged fixture (a scratch clone of the lane at base plus one
fixture commit holding a conforming 5-proposition entry, three new registry rows, README row and
pin), then commit one extra line in the entry's `## The chain` section:

> P6 (context): the translator's entry point refuses an unknown dispatcher name before any
> argument resolution runs `return {.success = false, .error = "Bad dispatcher"};`
> (Hyprland-legacy-DispatcherTranslator.cpp:31-32).

The sentence is a material mechanistic proposition (an ordering claim about the entry point), it
is **true against the pinned bytes** (fixture pin lines 31-32 show exactly the refusal return),
and it has **no `S###` row and no manifest entry** — i.e. it is an unmapped material factual
proposition, the precise thing the completeness clause forbids. Exact bytes: `mutant-m1.diff`.

**Command:**
`TMPDIR=/fast/scratch/hyaku/mado-r52/Falsify14 python3 -I <lane>/.ufo/waves/round-52/w1/C2CounterDraft/c2-r52-proposition-entry.py --repo <scratch-clone> --rev aeb13f76e8adef9ed04caa571ec12483af6b1721 --work <scratch>`

**Actual result:** `C2_R52: b ok=1 propositions=5` (the smuggled line is not even parsed as a
proposition), `e ok=1 prose_rows=3 prop_rows=3`, `clauses_met=5 admitted=1/1 verdict=TARGET_MET`,
exit 0 (`receipt-m1.txt`). The one-directional `quote_not_used` check only requires each map
quote to appear in prose; extra quoted claims in prose are unexamined.

## Attack M2 — marker-line exemption

**Setup:** same claim and locator as M1, placed on a line starting with `recheck:` in the entry
header (`mutant-m2.diff`). `cited_rows()` skips the entire line via `MARKER_RE` before any row
collection, so even the prose-row set never sees it.

**Result:** `clauses_met=5 admitted=1/1 verdict=TARGET_MET`, exit 0 (`receipt-m2.txt`).
Marker lines are legitimate ground/housekeeping, but the exemption is by line prefix with no
capability to carry a claim — mechanically, any sentence on such a line is outside completeness.

## Attack M3 — table-line exemption (the r51 pattern)

**Setup:** append a `## State claims (criterion 100)` table of the exact shape the admitted
round-51 entry uses — material state/value claims with setter cites, no `S###` rows
(`mutant-m3.diff`):

| state | value claimed | setter cite |
|---|---|---|
| `m_dispMap` | refuses unknown names before any call | Hyprland-legacy-DispatcherTranslator.cpp:31-32 |
| `m_dispMap` | 71 entries in the constructor population | Hyprland-legacy-DispatcherTranslator.cpp:797-867 |

**Result:** `clauses_met=5 admitted=1/1 verdict=TARGET_MET`, exit 0 (`receipt-m3.txt`). Every
`|` line is skipped, so no completeness or binding note can fire. This is not exotic: the
round-51 admitted entry keeps its six state claims, six observations and a census line in
non-map surfaces (see in-repo evidence below).

## Attack M4 — mapped but non-supporting quote (support-side residual, reproduced for the record)

**Setup:** rebind proposition P2 to the refusal-return quote at `…DispatcherTranslator.cpp:31-32`
— real file, verbatim, in-span, 8 words — while the claim stays about argument resolution
(`mutant-m4.diff`).

**Result:** `d ok=1 quotes_bound=5/5`, `clauses_met=5 admitted=1/1 verdict=TARGET_MET`, exit 0,
with the counter's own trailer `entailment=not-checked (outside non-author review)`
(`receipt-m4.txt`). This is the predicate's named tradeoff, not a predicate violation; it is
reproduced to document that the structural gate certifies neither completeness (M1-M3) nor
support (M4). An independent minimal checker on seat-local fixtures shows the same two shapes
(`receipt-generic-fixture.txt`, `entry-smuggled.md`, `entry-wrong-support.md`,
`check-complete.py`).

## In-repo historical evidence (no fixture needed)

- The admitted round-51 entry `corpus/knowledge/hyprland-dispatcher-dispatch-r51.md` carries
  material factual propositions outside its only proposition-like surface (the "What the
  evidence licenses" table, lines 70-86): a **State claims** table (lines 245-257), six
  **Observations** (lines 259-276), a **Census** line (lines 278-279) whose
  `special_handlers=5` was factually wrong — the round-51 w2 errata corrected it to four named
  strings plus a boolean — and the **Errata** section itself (line 318 onward), which adds new
  pin-cited corrected propositions never entered into any map. The entry's own map row for
  repeat/long-press even labels its consequence `[INF]` (line 86): the map can declare its own
  incompleteness in a cell and no structural check acts on it.
- Lesson `corpus/lessons/round-51.md` M51-2 records that the original entry stated five
  over-broad propositions and that the frozen structural counter had **"captured-by: none;
  verifies row/pin/quote binding, index presence and lexical structure, not
  proposition-to-source entailment"** — and that re-running the *unchanged* counter after the
  errata still returned `TARGET_MET`. This seat re-verified that at the frozen base:
  `receipt-r51-counter-at-base.txt` — `clauses=abcd clauses_met=4 admitted=1/1 TARGET_MET`,
  exit 0, on the very revision whose entry carries the errata. The defect class M1-M3 attack is
  therefore not hypothetical; it is the documented failure mode of the same structural design
  one round earlier, now with a new completeness clause that still does not close it.

## Reproducible setup

All work under `/fast/scratch/hyaku/mado-r52/Falsify14/` (removed on exit; receipts copied into
this seat dir first). Fixture mutations happened only inside the scratch clone with
`git rev-parse --show-toplevel` asserted equal to the clone dir (the builder
`w1/C2CounterDraft/make-fixture.py` enforces this itself; the mutant driver re-asserts it).

```sh
# 1. staged fixture (scratch clone of the lane at base + one fixture commit)
python3 -I <lane>/.ufo/waves/round-52/w1/C2CounterDraft/make-fixture.py \
  --lane /home/vgpnk/Projects/shokunin/mado-shokunin \
  --work /fast/scratch/hyaku/mado-r52/Falsify14/counter-fix --name base
# -> fixture=/fast/scratch/hyaku/mado-r52/Falsify14/counter-fix/base rev=e97ccc4a… (green: receipt-green.txt)

# 2. mutants M1-M4 (each committed on its own branch off the fixture commit, counter re-run)
python3 -I /fast/scratch/hyaku/mado-r52/Falsify14/run-mutants.py
# -> M1 aeb13f76… exit=0 TARGET_MET · M2 560689bb… exit=0 TARGET_MET
#    M3 f46467a3… exit=0 TARGET_MET · M4 d35c29a5… exit=0 TARGET_MET

# 3. per-run receipts (full clause detail) re-captured into this seat dir
```

No network access, no package queries, no live reads, no producer execution, no installs.
Python 3 only; tooling authorization `~/.omp/agent/RULES.md` read, no install was needed.

## Impact on the claim

The frozen C2 predicate has two halves: structure (rows, pins, quotes, rationale, count) and
completeness ("every material factual proposition is mapped"). The draft counter implements the
first faithfully and the second as `S###`-citation closure on a subset of prose lines. M1-M3
show that subset is defeatable through three ordinary authoring channels — narrative prose with
locators but no row, marker-exempt lines, and non-map tables — with a byte-verified, pin-true
smuggled claim in each case. The verdict is identical to the clean fixture (5/5 TARGET_MET), so
at integration the structural receipt cannot distinguish a map-complete entry from one that
smuggles material claims, and the predicate sentence "counter checks … complete mapping"
overstates what the counter proves. The r51 record shows the same blind spot produced an
admitted errata-needing entry under an *outside* review that only existed by luck of a second
wave — the r52 predicate's "outside reviewer judges source truth" covers entailment, but nothing
routes unmapped-claim discovery to that reviewer either.

## Smallest safe correction

Keep the frozen predicate and the outside-review division unchanged; close or disclaim the gap
in the counter/review mechanics, cheapest first:

1. **Counter, clause (e): locator sweep.** Extend `cited_rows()` to also collect `Pin:line`
   locator tokens and backticked quoted spans from prose lines; any prose locator or quote not
   bound to a map proposition must either be removed or promoted to a mapped proposition —
   emit `unbound_claim:<token>` and fail. This single sweep closes M1, and forces M2/M3 content
   into the checked surface.
2. **Counter, clause (e): narrow the exemptions.** Skip only a closed, named set of
   housekeeping lines (exactly the entry's own `held:`/`ground:`/`lane:`/`recheck:` header
   lines as pinned bytes, not arbitrary lines by prefix), and only the two known tables (the
   proposition map and the pin manifest) rather than every `|` line; everything else is prose
   for the sweep. This closes M2 and M3 mechanically.
3. **Outside-review routing (predicate-adjacent, no predicate edit).** The non-author truth
   review must sample sentences from the whole entry — narrative steps, any additional tables,
   observations/census/errata — not only the manifest; the integrator records that the
   structural verdict certifies declared-map closure plus the sweep, not whole-entry semantic
   completeness (same honesty pattern the lane already used for r51: "this structural result
   does not certify semantic sufficiency").
If the counter authors judge (1)-(2) infeasible within the round, the honest fallback is to
rename clause (e)'s claim to "declared-map closure" and record limitation 3 in the admission
record; the predicate itself then remains satisfiable but the receipt must not be read as
whole-entry completeness.

## Dissent / limitations

- The counter attacked is a **seat draft** (`w1/C2CounterDraft/`, not committed). If
  integration changes `cited_rows()`/clause (e), re-run `run-mutants.py` (commands above) before
  trusting or dismissing this attack; the mutants are the deliverable, not the draft's current
  failure.
- M1-M3 use deliberately minimal smuggles; real entries would phrase such claims more naturally,
  but the blindness is structural (regex scope), not stylistic — no phrasing of an unmapped
  locator claim on those line classes is visible to the current clause (e).
- M4 is expected-by-design (entailment disclaimed to the outside reviewer) and is reported as a
  residual, not as a predicate defect.
- This seat did not review the truth of the actual r52 entry draft (`w1/C2EntryDraft/`); that is
  the outside reviewer's assignment. The generic-fixture arm
  (`receipt-generic-fixture.txt`) duplicates M1/M4 with an independent 90-line checker in case
  the draft counter changes under this report.
- No tracked lane file, fleet file, sibling seat, script/template/state/watchdog, scratch-repo
  config or shokuknow surface was written; only this report, its seat dir and the removed scratch.

## Deliverables

Under `.ufo/waves/round-52/w1/Falsify14/` (all paths relative to
`/home/vgpnk/Projects/shokunin/mado-shokunin`):

| deliverable | path |
|---|---|
| green fixture receipt | `.ufo/waves/round-52/w1/Falsify14/receipt-green.txt` |
| M1 smuggled locator claim receipt + diff | `.ufo/waves/round-52/w1/Falsify14/receipt-m1.txt`, `mutant-m1.diff` |
| M2 marker-line smuggle receipt + diff | `.ufo/waves/round-52/w1/Falsify14/receipt-m2.txt`, `mutant-m2.diff` |
| M3 table-line smuggle receipt + diff | `.ufo/waves/round-52/w1/Falsify14/receipt-m3.txt`, `mutant-m3.diff` |
| M4 non-supporting quote receipt + diff | `.ufo/waves/round-52/w1/Falsify14/receipt-m4.txt`, `mutant-m4.diff` |
| r51 unchanged counter at base receipt | `.ufo/waves/round-52/w1/Falsify14/receipt-r51-counter-at-base.txt` |
| independent generic-fixture arm | `.ufo/waves/round-52/w1/Falsify14/receipt-generic-fixture.txt`, `entry-smuggled.md`, `entry-wrong-support.md`, `check-complete.py` |
| this report | `.ufo/waves/round-52/w1/Falsify14.md` |

Report trailer:

```
seat=Falsify14 wave=w1 round=52 lane=mado-shokunin base=85d57a818c3707397e21c840b6498b105ba798aa
claim=C2 coverage proposition-bound dispatcher source entry
attacked=registration C2 completeness sentence "every material factual proposition is mapped" / "counter checks ... complete mapping", as implemented by draft counter clause (e) cited_rows() in .ufo/waves/round-52/w1/C2CounterDraft/c2-r52-proposition-entry.py
receipt_green=.ufo/waves/round-52/w1/Falsify14/receipt-green.txt exit=0 admitted=1/1
receipt_m1=.ufo/waves/round-52/w1/Falsify14/receipt-m1.txt exit=0 TARGET_MET (smuggled locator claim, no row)
receipt_m2=.ufo/waves/round-52/w1/Falsify14/receipt-m2.txt exit=0 TARGET_MET (marker-line smuggle)
receipt_m3=.ufo/waves/round-52/w1/Falsify14/receipt-m3.txt exit=0 TARGET_MET (non-map table smuggle)
receipt_m4=.ufo/waves/round-52/w1/Falsify14/receipt-m4.txt exit=0 TARGET_MET (non-supporting quote; entailment disclaimed)
receipt_r51_base=.ufo/waves/round-52/w1/Falsify14/receipt-r51-counter-at-base.txt exit=0 (unchanged r51 counter passes post-errata entry at base)
reproduced=yes
installs=none (python3 only; RULES.md read)
report=.ufo/waves/round-52/w1/Falsify14.md
```
