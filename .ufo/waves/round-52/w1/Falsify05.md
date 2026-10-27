# Falsify05 — C2 source-proposition entailment (round 52)

Seat `Falsify05`, falsification item 05. Target: C2 "proposition-bound dispatcher source entry"
(`.ufo/waves/round-52/claims-frozen.md`, `.ufo/waves/round-52/registration.md`). Lane
`mado-shokunin`, base `85d57a818c3707397e21c840b6498b105ba798aa`. Source-only round: no package
query, no live/process/compositor read, no input capture, no producer execution, no fetch, no
tracked-lane edit. All work below is seat-local; the lane repo was read only.

## Attacked clauses (verbatim)

From `claims-frozen.md`:

> each material factual proposition maps to a pinned source quote <=25 words and explicit support
> rationale. A new committed counter checks proposition count, row/pin/quote bindings and complete
> mapping

From `registration.md`:

> A counter checks proposition count, row/pin/quote bindings and index; outside reviewer judges
> source truth.

Named items attacked: **C2 clause "complete mapping"** (registration: "every proposition has a map
row"), **C2 clause "each material factual proposition maps to a pinned source quote"** (the
proposition→quote relation), and **C2 element "pin path/revision"**. Not attacked: claim count,
axis separation, the base-absent control, the no-entailment-proof disclaimer (I confirm it), or C1.

## Method (seat-local, reproducible)

I built `c2ref.py`, a reference implementation of exactly the mechanical half the frozen predicate
assigns to the counter: index row, base absence, proposition count, and per-row binding (row id,
`opened` = 2026-10-27, status `mined`, pin path present, quote ≤25 words verbatim in the pinned
bytes, non-empty rationale). Three deliberately unspecified axes were parameterised, because the
frozen text does not fix them: how a shorthand `:N-M` pin cell resolves (`--pin-scope
strict|inherit|anchor`), and whether the quote must sit inside the cited span or anywhere in the
pin file (`--quote-scope anchor|file`). Only stdlib; reads a directory tree, no git, no network.

Sources are the lane's already-local Hyprland pins (`.ufo/waves/round-51/fetch/`, commit
`efb50993780079460b0cbed1363e2166a2de1d9f`, Hyprland 0.56.2, read from disk 2026-10-27; recorded
URLs `.../efb50993.../src/config/legacy/DispatcherTranslator.cpp`, `.../src/config/shared/actions/
ConfigActions.cpp`, `.../src/managers/KeybindManager.cpp`). Pins were copied to scratch, never
modified; digests: ConfigActions.cpp `a83abeb5…7637`, KeybindManager.cpp `8d8f35fc…4e40`,
legacy-DispatcherTranslator.cpp `7248cbb8…e771`.

The real target of opportunity: the in-progress C2 draft at
`.ufo/waves/round-52/w1/C2EntryDraft/entry-draft.md` (sha256 `3e88c1c2bab3a4de2298f6619f9c3a6f7584
d619835810d796dc239b6c638bb8`, 18 propositions) was copied verbatim into a fixture tree with four
round-52-shaped registry rows (S370–S373) so the frozen clauses could be run against the actual
artifact, not only against synthetic fixtures.

Reproduce: `bash .ufo/waves/round-52/w1/Falsify05/repro.sh` (rebuilds the trees under
`/fast/scratch/hyaku/mado-r52/Falsify05-repro`, runs R1–R10, writes
`.ufo/waves/round-52/w1/Falsify05/receipts/receipts.txt`).

## Results

### F1 — "complete mapping" is unenforced by every clause the counter is given (reproduced)

Fixture A is an entry with four fully mapped, genuinely supported propositions **plus one material
proposition stated only in prose** ("the socket dispatch request never writes the press-state
field, so a pass issued from the socket replays both key edges"). Reference counter: R2

```
count     ok=1 props=4 min=4
bind      ok=1  (p1..p4 all ok)
complete  ok=1 declared: every table proposition non-empty=True (n=4)
strong    sentence: mapped=0/4 substantive sentences
admitted=1
```

The material claim is invisible: the counter's proposition universe is whatever the author put in
the table, so "complete mapping" reduces to "every row I wrote has a row". The same holds on the
actual draft (R7): **18 propositions mapped, 48 substantive sentences in the body, 5 rows in the
`## State claims` table and 5 `**OBS**` lines — none of the latter 10 are proposition rows**, yet
all are material factual claims about the same code. Sentence-level reading cannot rescue it: with
a paragraph-joined, provenance-filtered extractor, my own two correct fixtures score 0/4 and 0/2
because method prose is lexically indistinguishable from claim prose. The strong variant is either
vacuous (author declares the universe) or unusable (it rejects normal house style).

### F2 — quote binding holds while the quote supports only part of the proposition (reproduced)

Fixture B: row 4 states "the `setSubmap` action registers a previously unseen name as a submap, so
a first switch always succeeds", pinned to `ConfigActions.cpp:1664-1682`, quote
`if (k->submap.name == submap)` — verbatim at line 1673, 4 words, rationale written. Reference
counter: R3 `admitted=1`. The pinned bytes refute it on the next hop: `ConfigActions.cpp:1681`
`return std::unexpected(std::format("Cannot set submap {}, submap doesn't exist (wasn't
registered!)", submap));`. Structural checks pass; the entailment is false.

The actual draft has the same shape at six rows, now with *narrowed* anchors (R7, all `ok`): the
quote is a prefix of the proposition and the second conjunct lives outside both quote and anchor —

| row | proposition conjunct not in the quote | where it actually is |
|---|---|---|
| P05 | "and delegates" | `legacy-DispatcherTranslator.cpp:619` `auto result = sendshortcut(modifiedArgs);` |
| P12 | "unresolved selector = error" | `:586` `return {.success = false, .error = "sendshortcut: window not found"};` |
| P13 | "mask set then cleared" | `ConfigActions.cpp:1554` `sendKeyboardMods(modMask,0,0,0)` / `:1576` `sendKeyboardMods(0,0,0,0)` |
| P15 | "restored after delegation" | `legacy-DispatcherTranslator.cpp:624` `m_passPressed = oldPassPressed;` |
| P16 | "same repeat rule" | `ConfigActions.cpp:1612-1613` `if (keyState == 2 && result.has_value()) result = Actions::pass(...)` |
| P17 | "delivers to the current focus" | `ConfigActions.cpp:1558` `sendKeyboardKey(S.m_timeLastMs, key - 8, ...)` |

Six of the seventeen rows that satisfy every mechanical clause are propositions the accepted quote
does not establish. This is not the disclaimed "automated semantic-entailment proof": it is the
narrower, checkable defect that the *unit* is compound, so "each proposition maps to a quote" is
satisfiable without the quote carrying the proposition.

### F3 — span width is free, so "located quote" locates nothing (reproduced)

Fixture B with the same quote bound to `Hyprland-ConfigActions.cpp:1-1772` (the whole file):
R4 `admitted=1`. Nothing in the frozen predicate bounds the span, so an author may cite the file as
the location and still satisfy "pin path + located quote".

### F4 — the same quote bytes can be bound to the wrong site (reproduced)

The draft's P17 quote `if (!window) return {};` occurs twice in one pin (`ConfigActions.cpp:141`,
`closeWindow`, and `:1578-1579`, `pass`). Under `--quote-scope file` the counter resolves it to
line 141 and reports `quote_elsewhere:141` (R8); under anchor scope it passes (R7). The predicate
does not say which behaviour is the contract, and the cheap variant silently binds the wrong site.

### F5 — "revision" is an element no clause reads (reproduced)

Rewriting both registry anchors to commit `0000…0000` while keeping the quote bytes unchanged
still gives R5 `admitted=1`. No clause parses a revision; the pin directory has no revision
identity. So the frozen phrase "a pin path/revision" carries an unverified element.

### F6 — markdown cell hazard makes "quote binding" escaping-dependent (reproduced)

P07's quote contains `modMask |= HL_MODIFIER_SHIFT;`. The `|` splits the markdown cell: the counter
sees quote ``…if (mods.contains("SHIFT")) modMask`` and rationale shifted one column (R9 cell dump;
`rationale_short` in R7/R8). This is also a rendering defect in the draft as written (`\|` needed).
A counter that "checks quote bindings" therefore depends on unstated escaping rules, and the same
row passes or fails depending on which side of the split is read.

### Failed control, reported honestly

A lexical conjunct-overlap proxy (`clause_coverage.py`) flagged 16/18 rows, i.e. it over-flags
paraphrase ("takes exactly four comma fields" vs `CVarList2(args, 4)` is genuinely supported). R10.
Conclusion drawn from the failure: no cheap lexical test separates paraphrase-support from
missing-support; the F2 defect can only be caught by atomic propositions plus human review, which is
why it must be fixed in the artifact shape rather than in the counter.

### Frozen control confirmed (not a bypass)

The base-absent control behaves as frozen: R1 `admitted=0` with `entry=absent` at base. The claim's
control is sound; my findings are about the green side.

## Verdict

Reproduced: **yes** for F1–F6, on both seat-local fixtures and the actual round-52 draft.
C2's counter, as the frozen text specifies it ("proposition count, row/pin/quote bindings and
index"), can be satisfied by an entry whose propositions are not entailed by the quoted bytes, and
"complete mapping" has no mechanical meaning because the proposition universe is author-declared.
The claim's own disclaimer ("not automated semantic-entailment proof") is honest; the problem is
that the *rest* of the predicate promises enforcement — "complete mapping", "each maps to a
pinned source quote" — that no assigned clause can deliver, so a green counter would not be evidence
for the clause it is named after.

## Recommended pre-data repairs (no post-data amendment)

Registration says "No predicate amendment after data"; we are pre-data, so:

1. **Atomic propositions.** One row = one conjunct, or one quote per conjunct. Then F2 disappears
   by construction and "maps to a quote" becomes checkable.
2. **Name the proposition universe.** Either freeze "complete mapping" as "every row of the entry's
   proposition table", or freeze the unit (e.g. every sentence of `## The chain`, every
   `## State claims` row, every `OBS` line must appear as a proposition row). Without one of the
   two, drop the phrase "complete mapping" rather than score it.
3. **Fix pin cell syntax.** Full pin filename in every cell (no bare `:N-M` probe: 12/18 draft cells
   are shorthand and resolve only by reading order, which breaks at P08), `\|` for pipes, and state
   whether the quote must be inside the cited span.
4. **Say who verifies the revision**, or remove "revision" from the mapping element.
5. **Ship the F1 fixture as a control**: an entry that is green structurally and carries one
   material proposition in prose. A counter that admits it is not measuring complete mapping.

## Deliverables

- `.ufo/waves/round-52/w1/Falsify05/c2ref.py` — reference frozen-clause counter (parameterised).
- `.ufo/waves/round-52/w1/Falsify05/clause_coverage.py` — failed lexical control (R10).
- `.ufo/waves/round-52/w1/Falsify05/repro.sh` — rebuilds trees, runs R1–R10.
- `.ufo/waves/round-52/w1/Falsify05/fixture/base/`, `fixture/final/`, `fixture/draft/` — base tree,
  fixture A (prose hole), fixture B (quote hole), verbatim copy of the analysed draft + registry.
- `.ufo/waves/round-52/w1/Falsify05/receipts/receipts.txt` — R0–R10 command output.
- `.ufo/waves/round-52/w1/Falsify05/receipts/clause-coverage-draft.txt` — R10 detail.
- `.ufo/waves/round-52/w1/Falsify05/receipts/pins.sha256` — pin identity.

## Limitations and dissent

- The draft is a moving proposer artifact (it changed during this seat's run: an earlier revision
  had P10–P12 anchored 3–4 lines off; the analysed revision is the sha above). Findings F2/F4/F6
  were re-run against the current revision; F3/F5 use my fixture. No committed round-52 counter
  exists yet (`quality/counters/` has no r52 file), so I tested a faithful implementation of the
  frozen clauses, not the final counter. If the committed counter adds a conjunct check or a
  revision check, F2/F5 are answered — and then those checks must themselves be named in the frozen
  predicate before data.
- I did not review the draft's source truth generally (that is `C2PinAudit` / `C2SourceCritic`);
  the six partial-support rows are examples of the *binding* defect, not a verdict that the draft's
  code reading is wrong. Where I read the code it agreed with the draft.
- `--quote-scope file` and `--pin-scope inherit|anchor` are my reconstructions of under-specified
  options, not committed behaviour; the divergence between them (F4) is itself the finding.
- No install performed, no package transaction, no network, no host read. Scratch was used and
  removed; disk guard checked (597G free) before the runs.

Report: `.ufo/waves/round-52/w1/Falsify05.md`
