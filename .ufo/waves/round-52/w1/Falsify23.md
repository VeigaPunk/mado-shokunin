# Falsify23 — round 52 (falsification item 23: C2 held-ground novelty)

Seat: Falsify23, role revenger. Axes declared: coverage (primary) and operability. Source-only
round: no package queries, live reads, process/compositor probes, input capture, screenshots,
producer execution, host/config/service mutation, or network fetch were performed. No tracked
lane file was edited; no claim or predicate was amended.

## Deliverables

- `.ufo/waves/round-52/w1/Falsify23.md` (this report)
- `.ufo/waves/round-52/w1/Falsify23/probe-c2-r52.py` — seat instrument: the committed
  `quality/counters/c2-r51-dispatch-entry.py` with round-52 constants plus one proposition clause
- `.ufo/waves/round-52/w1/Falsify23/novelty-audit.py` — base-tree byte/span reuse audit
- `.ufo/waves/round-52/w1/Falsify23/fixture-entry.md` — the adversarial candidate entry, verbatim
- `.ufo/waves/round-52/w1/Falsify23/fixture-build.md` — exact rebuild steps for the fixture
- `.ufo/waves/round-52/w1/Falsify23/receipts/` — probe outputs, audit JSON, pin-shas, fixture patch,
  committed-counter reproduction, pin-identity census

## Attacked clause

Frozen C2 text under attack (claims-frozen.md:11):

> Target: a distinct new indexed knowledge entry is grounded in sources opened this round; each
> material factual proposition maps to a pinned source quote <=25 words and explicit support
> rationale. A new committed counter checks proposition count, row/pin/quote bindings and complete
> mapping; … A no-work control at base must miss because target entry is absent.

and registration.md:9:

> one new indexed entry on a distinct Hyprland dispatcher-execution mechanism. Frozen condition: at
> least four substantive propositions; each maps to an opened-this-round `S###` row, a pin
> path/revision and exact located quote <=25 words, with a written support rationale; every
> material factual proposition is mapped. A counter checks proposition count, row/pin/quote
> bindings and index; … Base entry absent → TARGET_MISSED.

The limb attacked is the **freshness/novelty** conjunction: “opened-this-round `S###` row” +
“grounded in sources opened this round”, measured only by the counter’s enumerated checks
(proposition count, row/pin/quote bindings, index) and differentiated from no-work only by
**absence of the target entry at base**. I do not attack proposition count, binding mechanics, or
the absence control in themselves; I attack that the conjunction certifies new sourced coverage
when it can be satisfied with zero new source bytes and zero new propositions.

## Hypothesis (one concrete bypass)

A candidate entry should pass every enumerated clause if:

1. its four propositions restate facts already admitted in
   `corpus/knowledge/hyprland-dispatcher-dispatch-r51.md` at base;
2. its four `S` rows are new ids, `status=mined`, `opened 2026-10-27`, each bound to a pin under a
   round-52 fetch dir that is a **byte copy** of a pin already committed at base;
3. each row’s verified quote is the **same quote at the same line span** already cited by the
   round-51 entry at base;
4. the entry is indexed and absent at base.

If that passes, the frozen predicate’s “distinct new … grounded in sources opened this round”
admits a re-registration of held ground, and the no-work control (entry absent) cannot see it.

## Setup (reproducible)

Base: `85d57a818c3707397e21c840b6498b105ba798aa` (lane HEAD at start of seat work; `git status`
showed only the untracked `.ufo/waves/round-52/`). Fixture: scratch clone of the lane at base.
Full rebuild steps are in `Falsify23/fixture-build.md`; the corpus delta is
`Falsify23/receipts/fixture-corpus-delta.patch` (re-applied to a second clone and diffed
byte-identical in the seat run).

Fixture content (all inside the scratch clone):

- `corpus/knowledge/hyprland-dispatcher-dispatch-r52.md` — four propositions that restate the
  r51 entry’s chain steps 3, 1, 8 and 5, a `## Propositions` table (proposition | row | pin | quote
  | rationale), a pin manifest and three held lines. Kept verbatim as `fixture-entry.md`.
- `corpus/SOURCES.md` — rows S380–S383, `mined`, `opened 2026-10-27`, pins under
  `.ufo/waves/round-52/fetch/`.
- `corpus/README.md` — one index row.
- `.ufo/waves/round-52/fetch/` — four files copied from `.ufo/waves/round-51/fetch/`
  (`Hyprland-KeybindManager.cpp`, `Hyprland-legacy-DispatcherTranslator.cpp`,
  `Hyprland-HyprCtl.cpp`, `Hyprland-ConfigActions.cpp`); `cmp` reports each byte-identical to its
  r51 pin (`receipts/fixture-pins-vs-r51-cmp.txt`), sha256s in
  `receipts/fixture-pin-shas.txt`.

Instrument: `probe-c2-r52.py` is the committed round-51 counter with constants retargeted
(`ENTRY`, `ENTRY_NAME`, `FETCH_ROOT=.ufo/waves/round-52/fetch`, `BASE=85d57a81…`,
`ROW_MIN/MAX=380..383`) and one added clause (e) that encodes the frozen proposition
count/mapping requirement (≥4 propositions, each mapped to a clause-(b)-verified row, its pin, a
≤25-word quote located at the row’s span, and a rationale; every verified row mapped). Clauses
(a)–(d) are the committed machinery otherwise unchanged. Clause (e) makes the probe **stricter**
than the frozen enumeration, so a pass is conservative.

Commands (run from scratch; scratch passed explicitly, no writes inside the scored repo):

```sh
TMPDIR=$SCRATCH python3 -I Falsify23/probe-c2-r52.py --repo fixture --rev <fixture tip> --work work-green
TMPDIR=$SCRATCH python3 -I Falsify23/probe-c2-r52.py --repo fixture --rev 85d57a81… --work work-base
TMPDIR=$SCRATCH python3 -I Falsify23/novelty-audit.py
TMPDIR=$SCRATCH python3 -I lane/quality/counters/c2-r51-dispatch-entry.py --repo lane --rev 85d57a81… --work work-r51base
```

## Actual result

**(1) Recycled-ground candidate passes 5/5** — `receipts/probe-recycled-ground.txt`:

```
C2_R52F23: meta rev=e64c8457a96d28458bdf59014fb3792735f664dc base=85d57a818c37 work=…
C2_R52F23: a ok=1 index_row=`knowledge/hyprland-dispatcher-dispatch-r52.md` (MADO-R52...
C2_R52F23: b ok=1 rows=4/2 pins=4
C2_R52F23: c ok=1 body_shingles=549 files=67+cand3 max=1.3% top=[1.3%:corpus/knowledge/hyprland-dispatcher-dispatch-r51.md, …]
C2_R52F23: d ok=1 held=3/3 lines=3 untargeted=0 tokens=6
C2_R52F23: e ok=1 propositions=4/4 rows=4 missing=-
C2_R52F23: clauses=abcde clauses_met=5 admitted=1/1 verdict=TARGET_MET rev=e64c8457…
exit=0
```

**(2) The frozen no-work control misses, as designed** —
`receipts/probe-base-control.txt`: at `85d57a81…` the same probe prints `a ok=0 entry=absent`,
clauses b–e `skipped=entry-absent`, `verdict=TARGET_MISSED`, exit 1. The control discriminates only
the slug’s presence; it is silent on whether the ground is new.

**(3) Novelty audit: the admitted entry has zero novel ground** —
`receipts/novelty-audit.json`:

- `pins_with_no_base_copy: 0`, `pins_with_base_copy: 4`
- `rows_reusing_r51_span: 4`
- S380 `Hyprland-KeybindManager.cpp:785` sha256 `8d8f35fc…` — 4 byte-identical copies already under
  base `.ufo/waves/*/fetch` (round-24 `MadoR24.ScoutWikiEra-16.bin`, round-49, round-50, plus r51)
- S381 `Hyprland-legacy-DispatcherTranslator.cpp:32` sha256 `7248cbb8…` — 1 base copy (r51)
- S382 `Hyprland-HyprCtl.cpp:1149` sha256 `798b7c6c…` — 14 base copies
- S383 `Hyprland-ConfigActions.cpp:1681` sha256 `a83abeb5…` — 3 base copies
- every row: `same_span_and_quote_in_r51_entry_at_base: true`

The four propositions map to r51 entry lines 128 (step 3, quote at 785), 170 (step 5, 1681),
224 (step 8, 1149) and 264 (`OBS S365`, 32) — the same quotes the fixture cites. The only
novelty-shaped clause in the committed machinery is (c), body 8-gram shingle overlap; a paraphrase
of already-admitted propositions scored **1.3%** against the r51 entry (`MAX_OVERLAP=0.30`).

**(4) Committed counter reproduces its round-51 green at the round-52 base** —
`receipts/r51-committed-counter-at-r52base.txt` matches `round-52/receipts/c2-base.txt` line for
line: `rows=6/2 pins=6`, `body_shingles=3364 … max=0.1%`, `held=7/3 lines=8 untargeted=1`,
`clauses_met=4 verdict=TARGET_MET`.

## Committed-precedent evidence (the bypass is the lane’s accepted pattern, not only my fixture)

- **Pin bytes are recycled across rounds.** Of the 19 round-51 pins, **11 are byte-identical to
  files already fetched in earlier rounds** (`receipts/pin-identity-r51-vs-earlier.txt`):
  `Hyprland-HyprCtl.cpp` 17 earlier copies, `Hyprland-legacy-ConfigManager.cpp` 21,
  `Hyprland-KeybindManager.cpp` 6, `Hyprland-ConfigActions.cpp` 2, plus six headers/wiki files.
- **The same bytes carry a held row and an “opened” row.** `S364` (`opened 2026-10-27`) pins
  `Hyprland-KeybindManager.cpp` sha256 `8d8f35fc…`, the exact sha recorded on held row `S352`
  (`corpus/SOURCES.md:301`); `S368` (`opened 2026-10-27`) pins
  `Hyprland-legacy-ConfigManager.cpp` sha256 `9db68cf4…`, the exact sha on held row `S353`
  (`corpus/SOURCES.md:302`). `S352`’s anchor already includes
  `Hyprland-KeybindManager.cpp:773-793`, which contains 785 — the very line `S364` verifies.
- **The lane names it “reopened, not duplicated”** — round-51 search log line 44:
  “Two held pins reopened, not duplicated — S352 owns the bind match, S353 the key field;
  S364/S368 own the dispatch and handler-field lines their held rows do not cover”; the rows seat
  records the duplicate-URL class explicitly (`ScrRowsDispatch/rows.md:208-211`): “S364 reuses the
  S352 URL at a new scope … S368 reuses the S353 URL at a new scope. Expect exactly two new
  warnings of that class”. For S364 the “lines their held rows do not cover” claim is false for
  its own verified quote line (785 ∈ S352’s 773-793).
- **The r51 entry contradicts its own manifest on this point.** Manifest lines 32 and 39 assign
  rows S364 and S368 to `Hyprland-KeybindManager.cpp` and
  `Hyprland-legacy-ConfigManager.cpp`; the Limits paragraph (lines 50–53) says those two files
  “are byte-identical to the round-50 pins, so rows S352/S353 stay theirs; this entry opens no row
  for either file.” The counter cannot see the inconsistency: clause (b) scores the rows, and
  clause (d) skips the entry’s `held (cited, not re-registered, registry rows only): S352 through
  S353` line because it carries no `corpus/knowledge/<file>:<line>` locator — receipt
  `c2-base.txt` reports exactly that line as `untargeted=1`.

Consequence: in this corpus “sources opened this round” is a registry bookkeeping cell
(`status=mined`, `opened` string) with no byte- or span-novelty binding anywhere in the scored
predicate. An entry can therefore be TARGET_MET while adding no new source bytes, no new cited
span and no new proposition.

## Reproduced

- **Bypass on the frozen grammar: yes.** Fixture → `TARGET_MET 5/5`, while the novelty audit shows
  `0/4` novel pins and `4/4` reused r51 spans/quotes. Deterministic; rebuild path in
  `fixture-build.md`.
- **Committed-precedent measurements: yes.** sha equality S352↔S364, S353↔S368; `785 ∈ 773-793`;
  11/19 pin reuse; committed counter at base reproducing `c2-base.txt`.
- **Not claimed:** that a real round-52 worker will take this path (inference), or that the
  round-52 counter, once written, will lack a novelty clause. The frozen text as written contains
  no novelty clause, and the registration says “No predicate amendment after data”; the defect is
  in what the frozen predicate can certify, not in any individual author.

## Dissent / honest reading

The frozen phrase “distinct … entry” can be read as bookkeeping-only: a new slug over consciously
reused ground. If the lane intends “opened” to mean “re-registered or re-scoped”, then the claim’s
wording (“grounded in sources opened this round”, “a distinct new … entry”) overstates what is
measured, and the no-work control tests only absence. Either reading supports the same bounded
finding: the predicate cannot distinguish new knowledge from a re-registration of held ground,
and the report should not be scored as if it did.

## Bounded repair (recommendation only; no predicate edit made)

If the intent is genuinely new ground, the round-52 counter needs one clause the frozen text does
not have, e.g.: for each `S` row, reject if its pin’s git blob id equals a pin blob id referenced
by any registry row at base **and** its cited `(pin blob, line span)` pair is already cited by any
`corpus/knowledge/*.md` at base; or require a written “delta vs `<existing entry>`” statement that
names the new span/mechanism. A body-shingle overlap threshold is not a substitute: mine passed at
1.3% while restating four admitted propositions. This is a scoping change to C2, so it belongs to
the L1 before data, not to this seat.

## Source candidates

No external source candidate was opened by this seat in round 52. Every quoted byte is a
committed pin at lane base, whose URL/revision/access date are recorded in its registry row (for
example `corpus/SOURCES.md:313` for the Hyprland 0.56.2 `KeybindManager.cpp` pin at commit
`efb50993780079460b0cbed1363e2166a2de1d9f`, opened 2026-10-27 by the round-51 rows). The
propositions restated by the fixture are at
`corpus/knowledge/hyprland-dispatcher-dispatch-r51.md:128,170,224,264`.

## Limitations

- The probe is a seat instrument (committed counter + retargeting + clause (e)); clause (e) is my
  encoding of the frozen proposition clause. Clauses (a)–(d) and their constants are the committed
  bytes, unmodified apart from paths/revisions/base.
- The fixture “opened this round” is simulated at registry level with byte-copied pins; no fetch
  receipt or network access was used (round 52 is source-only), which is exactly what the frozen
  condition demands (it names no fetch proof).
- I inspected `quality/check-*.py` only for duplicate-pin/sha logic (none found in
  `check-index-rows.py`, `check-population.py`); I did not audit every counter for a hidden
  cross-row novelty check beyond the C2 lineage. No in-lane implementation of the rows seat’s
  `W04` duplicate-URL warning was found (`grep -rn 'W04|duplicate.URL' quality/*.py quality/*.sh`
  → empty), so it is a declaration, not a gate.
- No r52 target entry or counter exists (base is TARGET_MISSED by construction), so the object
  under test is the frozen predicate, the named control and the committed round-51 precedent.
- No live reads, package queries, process/compositor probes, input capture, screenshots or
  producer execution. No network. All git mutations were inside scratch clones, each preceded by
  `git rev-parse --show-toplevel` printing the fixture root; the lane tree shows only the
  untracked `.ufo/waves/round-52/` directory.
- Disk guard before heavy work: `/fast` 804G, 597–600G available (26% used); no ENOSPC. Scratch
  (`/fast/scratch/hyaku/mado-r52/Falsify23`, peak 886M for two clones) removed after receipts were
  copied into the seat dir. No installs, no pacman transaction, no service or config change.

Report: .ufo/waves/round-52/w1/Falsify23.md
