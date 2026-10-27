# C2EntryDraft — round-52 C2 entry draft (seat report)

Seat: `C2EntryDraft` (scribe), wave `w1`. Lane repo `/home/vgpnk/Projects/shokunin/mado-shokunin`,
base `85d57a818c3707397e21c840b6498b105ba798aa`. Claim: **C2 — coverage: proposition-bound dispatcher
source entry** (`claims-frozen.md` C2, `registration.md` C2). Operability (C1) not touched.

## Axes

| axis | this seat's move | direction |
|---|---|---|
| coverage | a new, distinct dispatcher-execution subject with 18 propositions, each bound to a proposed round-52 row, a pin, an anchor and an exact quote | candidate improvement (not admitted; no registry/index write) |
| operability | none | unchanged |
| freshness | pins re-hashed from disk and re-dated 2026-10-27 | neutral |
| others | no substrate, host, service or fleet surface touched | no harm claimed, none observed |

## What was built

`entry-draft.md` is a candidate `corpus/knowledge/hyprland-synthetic-key-dispatch-r52.md`: **how Hyprland
0.56.2's `sendshortcut` and `sendkeystate` manufacture a seat key/button event** — the four-field and
three-field grammars, the closed `down`/`repeat`/`up` state set, what `repeat` actually emits, modifier
words as case-folded substrings, the four keycode branches (numeric, `code:`, `mouse:` >=272, keysym
scan), the per-keyboard keycode cache, the selector's empty-means-focused rule, the timestamp and `key-8`
offset a synthetic event carries, the press-field save/restore, and the `Actions::sendKeyState` twin.

**Distinctness (the attacked clause: "distinct dispatcher-execution mechanism").** The round-51 entry
`corpus/knowledge/hyprland-dispatcher-dispatch-r51.md` owns the dispatcher map, parse-time validation, the
press path, `submap`/`pass` and the `hyprctl dispatch` verb; it mentions `sendkeystate` in one
parenthetical ("the one dispatcher that writes the field itself") and uses `sendshortcut` only as a
three-comma grammar example (round-51 entry step 7). This draft starts after that parenthetical and takes
no second account of the map, the parse, the press path or the socket; S364-S369 and S352/S353 are cited
as held ground, and the round-50 key-match entry is cited for the KEY field only. The subject is the
*manufacture and delivery* of an input event, not its routing.

## Proposition binding

18 propositions `P01`-`P18` in `proposition-map.tsv` (`prop / row / proposition / pin / anchor / quote /
support / rationale`), mapped 1:1 into the entry's own table. Rows proposed (not appended — the registry
edit is out of this seat's write surface):

| proposed row | file | scope of this entry | registry precedent |
|---|---|---|---|
| S370 | `src/config/legacy/DispatcherTranslator.cpp` @ `efb50993` | `sendshortcut` + `sendkeystate` bodies | S365 same URL, other scope (dup-URL W04 warning expected) |
| S371 | `src/config/shared/actions/ConfigActions.cpp` @ `efb50993` | press-field use, seat delivery, null-window path (save/restore of the action-side twin is held, not claimed) | S367 same URL, other scope (W04) |
| S372 | `src/config/shared/actions/ConfigActions.hpp` @ `efb50993` | action-state fields, `ActionResult` | none — new URL |
| S373 | `src/managers/KeybindManager.cpp` @ `efb50993` | `stringToModMask` (:221-240); cache member declared `KeybindManager.hpp:149`, written from `DispatcherTranslator.cpp:559-576` | S364/S352/S353 same URL, other scopes (W04) |

Quotes are 4-22 words (cap 25). Support class is `direct` for all 18: each quote contains the construct
the proposition asserts; the rationale line names what in the quote carries it.

## Review corrections applied (after first draft)

Two sibling reviews changed the draft; both are recorded rather than silently absorbed.

1. **C2Novelty (relayed by C2CounterDraft): P16 leaned on an unquoted helper and was factually wrong.**
   Step 6 said an empty selector delivered "without moving focus", resting on `if (!window) return {};`.
   `Actions::pass` calls `xtract`, which is
   `return window.value_or(Desktop::focusState()->window());` (Hyprland-ConfigActions.cpp:47-49), so an
   empty selector targets the **focused** window and the focus-switch block does run. Fixed: step 6
   rewritten, P12 narrowed to the translator-side ternary, P16 now carries the `xtract` quote, P17 the
   surviving-null case (event still sent, bookkeeping skipped), and the old key-not-found proposition is
   P18. This is the honest record that the earlier wording was wrong, not merely under-quoted.
2. **C2CounterDraft: markdown table defects** (see below).

## Counter-seat feedback applied (after first draft)

`C2CounterDraft` ran its draft counter against the staged draft and found two markdown-only defects (the
TSV was correct): an unescaped `|` in P07's quote cell splitting `modMask |=` into a new cell, and bare
`:NNN` anchors continuing across a file switch (P08-P12 resolving to the preceding KeybindManager pin,
P15/P17 to ConfigActions). Both fixed: the markdown table is now **regenerated from `proposition-map.tsv`**
(one source of truth), every row carries the full pin filename in its `pin:anchor` cell, and pipes inside
quotes are escaped. `md-table-check.txt` re-parses the table and compares every row field to the TSV:
`rows_md=18 rows_tsv=18 ids_match=True failures=0` → OK. No proposition, quote, row or claim was changed.

## Commands and results (read-only; the only network use was the four pinned raw.githubusercontent reads; no compositor, no package query)

| command | result |
|---|---|
| `python3 -I check-quotes.py --map proposition-map.tsv --entry entry-draft.md --pins-dir ./fetch` | `PASS` P01-P18, `MADO_R52_C2_ENTRY_CHECK: props=18 rows=4 pins=4 quote_max_words=25 failures=0 verdict=OK`, exit 0 (`quotes-check.txt`) |
| negative controls in scratch (`a-fabricated`, `b-overlong`, `c-norow`, `d-entry-missing-prop`, each one mutation against the base pair) | each `verdict=DEFECT`, exit 1, with the exact failing prop named (P05, P02, P11, P15); the unmutated pair re-run green 18/18 (`negative-control.txt`) |
| `curl -fsSL --max-time 25` on the four raw URLs into `fetch/`, then `sha256sum` each against the round-51 copy | HTTP 200 each; 4/4 `EQUAL` (`fetch/verify.txt`); sizes/digests in `pins.txt` |
| `sha256sum`/`wc` on `Hyprland-KeybindManager.hpp` | 191 lines, 7936 B, digest equal to the round-51 manifest |
| `grep -c sendkeystate\|sendshortcut` on the three doc pins | 0 / 0 each — documentation gap, recorded in Limits, not a proposition |

**Cross-check against the draft counter (18-prop version).** `C2CounterDraft` re-read the draft after the
P16 correction: `propositions=18 ids=18`, `rows_bound=4/18 distinct_rows=4`,
`quotes_bound=18/18 quotes_raw=6/18 pins=4 policy=whitespace-collapsed pins_prior_equal=4/18`,
`clauses=abcde clauses_met=5 admitted=1/1 TARGET_MET` (its receipt
`.ufo/waves/round-52/w1/C2CounterDraft/receipts/r-draft-as-is.txt`). Its `quotes_raw=6/18` counts the
quotes that are byte-exact single lines; the other 12 are reflowed across source lines and equal only
under whitespace collapsing - the same policy this seat's checker uses, so the two independent counts
agree row for row.

That seat also stated the boundary plainly, and the report keeps it: its counter could not have caught
the P16 error, because the old quote sat correctly at the line the draft cited - the defect was in the
claim the quote was attached to. Structural binding cannot certify that a claim is true, which is why
C2's "independent non-author samples actual source truth" clause is load-bearing here.

Checker semantics, stated so the counter seat can reuse or critique it: normalises whitespace, requires
the quote to occur inside the declared anchor span of the declared pin, caps at 25 words, requires
non-empty row/pin/quote/rationale, requires `S###` row ids, requires each prop id and row id to appear in
the entry draft, and requires >=4 propositions with unique ids. It checks **bindings, not entailment**:
a quote that is verbatim at the anchor and says something else still passes; that half stays with the
independent reviewer (C2SourceRecon / C2EntryQuality / C2SourceCritic).

## Limitations and dissent

- **No registry or index write.** `corpus/SOURCES.md` and `corpus/README.md` are untouched by instruction;
  the four rows above are proposals with URL + commit + pin + digest, and the data seat must open them
  before the entry can be admitted. The entry's own `source:` lines carry "(proposed)" for that reason.
- **Pins were fetched this round.** The four URLs were re-fetched 2026-10-27 into
  `.ufo/waves/round-52/w1/C2EntryDraft/fetch/` and all four sha256 values are byte-equal to the round-51
  copies (`fetch/verify.txt`), so quotes are checked against this round's own bytes; the documentation-gap
  greps still used the round-51 copies of the three doc pins, which were not re-fetched.
- `[INF]` items are marked in the entry and not claimed as measured: "highest matching keycode wins"
  (no `break` in the scan), the case-sensitivity of the cache key, and the `result.success` /
  `result.has_value()` equivalence (which is now only a contrast note about the held twin).
- **P16 demoted after recon review.** `C2SourceRecon` showed the twin `Actions::sendKeyState` and its
  save/restore are the exact fact of round-51 step 6's parenthetical, so the twin is now held ground and
  cited once as contrast; P15 keeps the translator-side save/restore, which round 51 did not cite.
  P07 was likewise sharpened: the uppercase/substring parser is partly held (`bind-table-r25.md:42`,
  S162), and only the sendshortcut path's silent-zero consequence is claimed here.
- The twin's callers are not traced; the entry no longer claims anything about the twin beyond the held
  cite and the `[INF]` repeat-guard note.
- Two alternative distinct surfaces named by recon are recorded in the entry, not drafted: `exec` ->
  `supplementary/executor/Executor.{hpp,cpp}` (included at `DispatcherTranslator.cpp:4`, called at
  `:66`/`:73`, unpinned) and the shortcuts-inhibit gate (`src/protocols/ShortcutsInhibit.{hpp,cpp}`,
  gate sites `KeybindManager.cpp:643`, `:844-851`). Neither was opened by this seat; no claim on either.
- Novelty is argued against the round-51 entry as I read it; a reviewer who reads `sendkeystate` as
  already covered by the round-51 parenthetical falsifies the distinctness clause, and this report
  records that as the open attack surface rather than a settled result.
- No claim that the round-51 entry is wrong, and no predicate, control or frozen claim was edited.

## Handoff

- Counter target slug for C2: `hyprland-synthetic-key-dispatch-r52` (absent at base; the round-51 slug
  must not be reused). The no-work control misses because the slug is absent.
- If the data seat admits the entry, the row-anchor pairs in `proposition-map.tsv` are the binding set a
  structural counter can check; `check-quotes.py` is a working prototype of that check (exit 0/1/2,
  read-only, no scratch writes).
- **Registry row shape the draft counter enforces** (`C2CounterDraft`, whose draft counter now reads this
  draft as 5/5 clauses met, `admitted=1/1 TARGET_MET`): each appended row's `used-by` cell must name
  `corpus/knowledge/hyprland-synthetic-key-dispatch-r52.md`, and its `anchor` cell must carry this round's
  fetch path (`.ufo/waves/round-52/w1/C2EntryDraft/fetch/...`) **plus** the 40-hex revision
  `efb50993780079460b0cbed1363e2166a2de1d9f`; otherwise the counter reports `anchor_no_fetch_root` /
  `anchor_no_revision`. Its clause (c) additionally requires each row to be `mined`, to carry this
  round's access date `2026-10-27`, and to be **absent from the registry at the frozen base** (that is
  how it proves the row was opened this round rather than reused). That requirement is deliberate: it is
  what stops a row opened in an earlier round from being passed off as opened this round. Clause (e)
  also requires every proposition id to be cited outside the map, which the "What the evidence
  licenses" table does (P01-P18).
- Scratch `/fast/scratch/hyaku/mado-r52/C2EntryDraft/` used for the negative controls only; removed on
  exit. No `/tmp` evidence, no install, no package transaction, no git/jj mutation.

## Deliverables

| artifact | path (relative to lane root) |
|---|---|
| candidate entry | `.ufo/waves/round-52/w1/C2EntryDraft/entry-draft.md` |
| proposition map | `.ufo/waves/round-52/w1/C2EntryDraft/proposition-map.tsv` |
| binding checker | `.ufo/waves/round-52/w1/C2EntryDraft/check-quotes.py` |
| green receipt | `.ufo/waves/round-52/w1/C2EntryDraft/quotes-check.txt` |
| red/green control receipt | `.ufo/waves/round-52/w1/C2EntryDraft/negative-control.txt` |
| markdown/TSV parity receipt | `.ufo/waves/round-52/w1/C2EntryDraft/md-table-check.txt` |
| pin manifest | `.ufo/waves/round-52/w1/C2EntryDraft/pins.txt` |
| this round's pins + equality receipt | `.ufo/waves/round-52/w1/C2EntryDraft/fetch/` (`verify.txt`) |
| this report | `.ufo/waves/round-52/w1/C2EntryDraft.md` |

Report trailer:

```
seat=C2EntryDraft wave=w1 round=52 lane=mado-shokunin base=85d57a818c3707397e21c840b6498b105ba798aa
claim=C2 coverage proposition-bound dispatcher source entry
entry=.ufo/waves/round-52/w1/C2EntryDraft/entry-draft.md
map=.ufo/waves/round-52/w1/C2EntryDraft/proposition-map.tsv
checker=.ufo/waves/round-52/w1/C2EntryDraft/check-quotes.py
receipt_green=.ufo/waves/round-52/w1/C2EntryDraft/quotes-check.txt exit=0 (checked against .ufo/waves/round-52/w1/C2EntryDraft/fetch)
receipt_pins=.ufo/waves/round-52/w1/C2EntryDraft/fetch/verify.txt 4/4 EQUAL
receipt_controls=.ufo/waves/round-52/w1/C2EntryDraft/negative-control.txt red=4/4 green=1/1
receipt_mdparity=.ufo/waves/round-52/w1/C2EntryDraft/md-table-check.txt rows=18 failures=0
pins=.ufo/waves/round-52/w1/C2EntryDraft/pins.txt
report=.ufo/waves/round-52/w1/C2EntryDraft.md
props=18 rows_proposed=4 (S370-S373) quotes_max_words=22 verdict=DRAFT (not admitted)
```
