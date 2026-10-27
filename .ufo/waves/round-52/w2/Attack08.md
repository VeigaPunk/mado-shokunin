# Attack08 — W2 attack on C2 claim/source map completeness

Seat: `Attack08` (critic, leaf). Wave `w2`, round 52. Target: **C2 — coverage: proposition-bound dispatcher source entry** (`claims-frozen.md` §C2; `registration.md` §Frozen predicates C2 / §Frozen controls). Scope: completeness of the claim's source map and of the committed counter's check set, plus the specified controls. Attack only; no judgment admission; no claim/predicate edit; no tracked, sibling, or source-repo write; no git/jj mutation in the lane; no network, probe, screenshot, or host read.

Lane repo `/home/vgpnk/Projects/shokunin/mado-shokunin`, base `85d57a818c3707397e21c840b6498b105ba798aa`. Landed working-tree state (uncommitted): `corpus/knowledge/hyprland-synthetic-dispatch-r52.md` (sha256 `bee0d14379eb…`, 18 propositions P01–P18), registry rows S370–S373 appended to `corpus/SOURCES.md`, index row appended to `corpus/README.md`, round fetch `.ufo/waves/round-52/fetch/` (5/5 `sha256sum -c` OK), committed counter `quality/counters/c2-r52-proposition-entry.py` (sha256 `5c7fb820e43c…`, 47 lines). W1 draft counter under test for comparison: `.ufo/waves/round-52/w1/C2CounterDraft/c2-r52-proposition-entry.py` (sha256 `55452a3d6eab…`, 965 lines).

All executable evidence was produced in `/fast/scratch/hyaku/mado-r52/Attack08/` (scratch clone of the lane with the landed state committed as `c0b3a00c`; removed on exit). Commands below are reproducible from that setup.

## Verdict summary

| attacked clause (frozen C2) | verdict |
|---|---|
| "a distinct new indexed knowledge entry is grounded in sources opened this round" | **reproduced in part; falsified at the registry-process leg** — rows/pins/fetch exist and verify, but the QUALITY17 distinct-scope review the corpus requires for S370/S371/S373 is self-recorded as outstanding, and the committed counter cannot even read the landed entry |
| "each material factual proposition maps to a pinned source quote ≤25 words and explicit support rationale" | **reproduced in part** — 18/18 mapped, all quotes ≤25 words (max 19), rationales present; **17/18 quotes bind whitespace-collapsed at anchor; P16's quote is a non-contiguous splice that fails even the W1 draft counter's binding clause**; only 6/18 are raw-verbatim; two quotes do not contain the lines their two-part propositions assert |
| "every material factual proposition is mapped" | **reproduced for this entry's prose** (18/18, prose carries no extra mechanism facts) — but the committed counter cannot check it (mutant M7 escapes) |
| "a new committed counter checks proposition count, row/pin/quote bindings and complete mapping" | **NOT REPRODUCED — falsified on three legs**: (a) the committed counter reports TARGET_MISSED on the actual landed state by two independent breaks; (b) it never reads pins, so fabricated quotes and impossible anchors pass; (c) it has no completeness, freshness-at-base, uniqueness, or claim-nonempty checks |
| "an independent non-author samples actual source truth" | **NOT REPRODUCED** — no committed sample receipt exists; this seat's attack sample finds one defective binding (P16) in the landed map |
| "A no-work control at base must miss because target entry is absent" | **mechanically reproduced** (TARGET_MISSED, exit 1, at base for both slugs) — but the committed counter as-defaulted also misses at the landed tip, so the control is not discriminating, and no new-counter base receipt is committed |

**Net:** as landed, C2's counter clause is false as committed; the source map itself is mostly sound but carries one spliced quote (P16), a raw-verbatim minority, two partial-support quotes, one unreclassified held-fact re-anchor (P06), and one near-duplicate proposition pair (P04/P17); the required QUALITY17 distinct-scope review and the non-author source-truth sample remain outstanding with no committed receipts.

## Attack items

Each item names the attacked clause, exact locator/command, observed result, verdict, limitations.

### A1 — Committed counter cannot parse the landed entry's proposition table (integration break)
- Attacked: "a new committed counter checks proposition count, row/pin/quote bindings and complete mapping."
- Locator/command: run committed counter on a scratch clone at the landed state: `python3 -I quality/counters/c2-r52-proposition-entry.py --repo <clone> --rev c0b3a00c --entry corpus/knowledge/hyprland-synthetic-dispatch-r52.md --work w3`.
- Observed: `C2_R52: props=0 rows=0 indexed=1 failures=1 verdict=TARGET_MISSED`, exit 1. The row regex `^\|\s*(P\d+)\s*\|\s*(S\d+)\s*\|…` demands `P##` and `S###` in adjacent cells; the landed table's column order is `ID | Proposition | Source row | …`, so the second cell is claim text and **zero rows match** (verified directly: `re.findall` on the entry bytes returns 0).
- Verdict: not reproduced (counter clause fails on the landed artifact).
- Limitation: the W1 draft counter parsed this same table shape (Attack12's sibling run of the draft counter on the landed state reports `propositions=18 ids=18`); the breakage was introduced by the committed rewrite, not the entry.

### A2 — Committed counter's default target slug ≠ landed entry path
- Attacked: same clause; registration "the new counter must name a separate target slug."
- Locator/command: `python3 -I quality/counters/c2-r52-proposition-entry.py --repo <clone> --rev c0b3a00c --work w2` (defaults).
- Observed: `C2_R52: entry=absent verdict=TARGET_MISSED`, exit 1 — because `ENTRY_DEFAULT='corpus/knowledge/hyprland-synthetic-key-dispatch-r52.md'` while the landed entry is `corpus/knowledge/hyprland-synthetic-dispatch-r52.md`. By default the counter can never pass the landed state at any revision.
- Verdict: not reproduced.
- Limitation: `--entry` can override; but no committed receipt shows the counter ever run green (see A15).

### A3 — Fabricated quote passes the committed counter (quote binding not checked)
- Attacked: "row/pin/quote bindings."
- Locator/command: synthetic fixture in the counter's own 7-column grammar (`| P## | S### | claim | pin | anchor | quote | rationale |`), one mutation: P1's quote replaced with `the quick brown fox jumps over the lazy dog repeatedly`; run committed counter.
- Observed: `verdict=TARGET_MET`, exit 0.
- Verdict: not reproduced — the counter never opens a pin file; any ≤25-word string "binds."

### A4 — Impossible anchor passes the committed counter
- Attacked: "row/pin/quote bindings."
- Locator/command: same fixture; P1 anchor mutated `591-594` → `9999-10000`.
- Observed: `verdict=TARGET_MET`, exit 0.
- Verdict: not reproduced — no anchor-resolution or line-range check exists.

### A5 — Unmapped prose proposition passes (complete mapping not checked)
- Attacked: "and complete mapping" / "every material factual proposition is mapped."
- Locator/command: same fixture; append one pin-true factual sentence to the entry prose with a locator but no S### row: "Extra fact: sendkeystate is the only table-reachable dispatcher that writes m_passPressed (DispatcherTranslator.cpp:615-624)."
- Observed: `verdict=TARGET_MET`, exit 0.
- Verdict: not reproduced — the counter has no prose scan at all. (The landed entry's actual prose carries no such extra facts; the defect is the counter's.)

### A6 — Old-row used-by hijack passes (freshness at base not checked)
- Attacked: registration C2 "rows … opened this round"; counter must distinguish opened-this-round rows.
- Locator/command: same fixture; mutate registry in place: row S364's `used-by` re-pointed to the fixture entry (registration allows in-place used-by edits), fixture P1 re-cited to S364 with a true claim.
- Observed: `verdict=TARGET_MET`, exit 0. The counter checks the cited row contains `mined`, `2026-10-27`, the entry name, and a 40-hex string — all true of the hijacked old row. It never compares the base registry.
- Verdict: not reproduced — the W1 draft counter's strongest check (`row_not_new` vs base) was dropped in the rewrite.
- Limitation: S364's true used-by currently names the r51 entry, so the landed state itself is caught only incidentally, by the entry-name substring check (mutant M5: TARGET_MISSED) — not by a freshness check.

### A7 — Duplicate quote and empty claim pass
- Attacked: counter's proposition-count leg quality.
- Locator/command: fixture mutations M14 (P4's quote duplicated as P1's) and M15 (P1 claim cell emptied).
- Observed: both `verdict=TARGET_MET`, exit 0. No uniqueness or claim-nonempty gate.
- Verdict: not reproduced. (The landed entry itself has distinct claims; P04/P17 quotes overlap as substring — see A13.)

### A8 — Revision check is satisfiable by the URL, not the anchor
- Attacked: counter's row-meta check.
- Locator/command: fixture mutation M12b — strip the 40-hex revision from S370's anchor cell only (`efb50993…; r52 fetch SHA256 …` → `r52 fetch SHA256 …`).
- Observed: `verdict=TARGET_MET`, exit 0, because `re.search(r'[0-9a-f]{40}', row)` matches the commit hash inside the row's own URL field.
- Verdict: not reproduced as an anchor check; the check is vacuous for any registry row whose URL carries the commit (all Hyprland rows do).

### A9 — Landed P16's quote is a non-contiguous splice (source-truth sample)
- Attacked: "exact located quote ≤25 words"; W1-review inheritance duty (C2PinAudit finding 1 class; M51-2 class).
- Locator/command: independent check of all 18 quotes against `.ufo/waves/round-52/fetch/` bytes (whitespace-collapsed substring within cited line span; span union for comma anchors). P16: `Hyprland-ConfigActions.cpp:1554-1558,1576`, quote `g_pSeatManager->sendKeyboardMods(modMask, 0, 0, 0); g_pSeatManager->sendKeyboardKey(S.m_timeLastMs, key - 8, WL_KEYBOARD_KEY_STATE_PRESSED);`.
- Observed: **FAIL** — the two statements are not adjacent in the source; lines 1555–1557 (`if (S.m_passPressed == 1) { if (!isMouse)`) sit between them. As spliced, the quote asserts an unconditional delivery order the source does not have (the key send is guarded by `m_passPressed == 1 && !isMouse`). The W1 draft counter run on the landed state reports the same defect: `miss=P16:quote_not_at_pin(Hyprland-ConfigActions.cpp:1554)` (sibling seat Attack12's receipt, independently confirms). The other 17 quotes bind collapsed at anchor; word counts 5–19 (cap 25).
- Verdict: reproduced as a defect in the landed map (attack-seat sample; not the canonical non-author judgment — see A16).
- Limitation: a "tokens present within span union" reading would pass P16; the contiguous-excerpt reading used by the W1 draft counter does not. The committed counter enforces neither (A3/A4).

### A10 — Quote-comparison policy unfrozen; only 6/18 quotes raw-verbatim
- Attacked: "exact located quote."
- Locator/command: same independent check, raw vs whitespace-collapsed.
- Observed: raw-verbatim 6/18 (P02, P05, P11, P13, P15, P18); 12/18 bind only after whitespace collapsing (source lines reflowed). Matches the W1 draft counter's `quotes_raw=6/18` pattern.
- Verdict: reproduced — "exact" remains policy-dependent; the committed counter states and enforces no policy (it does not compare quotes at all).

### A11 — P14 not raw-verbatim at its anchor (field-declaration spacing)
- Attacked: "exact located quote."
- Locator/command: `sed -n '117p' .ufo/waves/round-52/fetch/Hyprland-ConfigActions.hpp` vs entry P14 quote.
- Observed: source line is `uint32_t    m_timeLastMs    = 0;  // timestamp of last key/mouse event` (multiple interior spaces, two spaces before `//`); the quote writes single spaces. Collapsed-binding passes; raw fails. This is the same defect W1 C2Novelty N4 flagged on the draft; it survived landing.
- Verdict: reproduced (raw policy); limitation: collapsed policy passes.

### A12 — P12 and P16 quote cells do not contain the lines their propositions assert
- Attacked: "each maps to … exact located quote … with a written support rationale" (quote sufficiency, not entailment).
- Locator/command: source lines 582–586 (P12) and 1554–1576 (P16) read at the pin.
- Observed: P12's proposition has two parts ("empty selector produces a null optional window; a written selector without a result is rejected") but its quote cell carries only the ternary; the rejection guard (`if (!regexp.empty() && !PWINDOW) return … "window not found"` at :585-586) is inside the anchor yet absent from the quote. P16's "then clears the modifier state" is evidenced only by locator extension to :1576 (`sendKeyboardMods(0,0,0,0)`), not by the quote cell. Both are the partial-support class W1 RegistryContract listed against the draft; the landed entry narrowed the claims (P12 no longer asserts a focus destination — W1 C2PinAudit finding 1 repaired) but the quote/sufficiency gap remains.
- Verdict: reproduced as map-quality defects (bounded; not entailment failures).

### A13 — P04/P17 are a near-duplicate proposition pair
- Attacked: "at least four substantive propositions" honesty; completeness of the map as coverage.
- Locator/command: entry rows P04/P17.
- Observed: P04 "`repeat` calls its delegate again only after a successful first call" (quote = call + guarded second call, :619-622) and P17 "`sendshortcut`'s repeat branch can invoke its delegate twice for a successful repeat state" (quote = the guard line, :619-622) state the same fact; P17's quote is a substring of P04's. Coverage count 18 effectively 17.
- Verdict: reproduced (minor; distinct enough strings to evade a uniqueness check if one existed — A7 shows none does).

### A14 — P06 remains an unclassified held-fact re-anchor
- Attacked: "grounded in sources opened this round" (coverage delta honesty).
- Locator/command: entry P06 vs `corpus/knowledge/hyprland-dispatcher-dispatch-r51.md` step 7 (`DispatcherTranslator.cpp:532-535`, held via S365).
- Observed: P06 ("`sendshortcut` requires exactly three fields", S370, :531-535) is the same quote round 51 already bound for the same fact; W1 C2Novelty N3 recommended reclassification as `held-fact/new-anchor`; the landed entry keeps it as `direct` with no held cite. True and well-anchored; the deficiency is classification inflation, inherited from the draft.
- Verdict: reproduced (minor; W1-recommended correction not applied at landing).

### A15 — No committed red/green or base receipts for the committed counter
- Attacked: registration §Frozen controls ("the new counter must name a separate target slug and prove absent at base"); C1-style selftest expectation carried for C2 by the control clause.
- Locator/command: `ls .ufo/waves/round-52/receipts/` → only `c1-base.txt`, `c2-base.txt`; the latter is the **old** r51 counter's run (header `C2_R51`, `clauses_met=4 admitted=1/1 TARGET_MET` at base — registration explicitly distrusts it for the r52 target). `grep -rl c2-r52-proposition-entry .ufo/waves/round-52/receipts/` → no hits.
- Observed: no committed receipt shows the new counter missing the target at base or passing the landed state. My own runs supply the missing data points: base → TARGET_MISSED both slugs (`hyprland-synthetic-key-dispatch-r52.md` and `hyprland-synthetic-dispatch-r52.md` both absent at base; verified `git cat-file -e`); landed state → TARGET_MISSED (A1/A2). Sibling Attack30's P0 independently records both slugs absent at base.
- Verdict: control mechanically reproduced by me and Attack30; the committed record required by registration is absent.
- Limitation: receipts may be planned post-W2 by L1; the gap stands as of this attack.

### A16 — Independent non-author source-truth sampling receipt absent; attack sample supplied
- Attacked: "an independent non-author samples actual source truth."
- Locator/command: `corpus/lessons/round-52.md` §Gate/Admission: "Admitted/rejected rows and outside non-author admit+reject sample remain pending final source audit; do not label a seat as independent non-author."
- Observed: no per-proposition verdict receipt exists under `.ufo/waves/round-52/receipts/`. This seat's sample (A9–A14) found: 1 binding defect (P16 splice), 2 partial-support quotes (P12, P16), 1 raw-verbatim deviation (P14), 1 unreclassified held-fact (P06), 1 near-duplicate pair (P04/P17); 12 propositions sampled true at pin (P01–P05, P07–P11, P13, P15, P18 spot-checked true).
- Verdict: not reproduced (as a committed artifact); attack sample recorded here for the canonical reviewer.
- Limitation: I am an attack seat, not the claim's designated non-author sampler; my samples name themselves as attack evidence.

### A17 — QUALITY17 distinct-scope review for S370/S371/S373 is outstanding
- Attacked: registration safety boundary + corpus rule invoked by the W2 brief ("repeated URL rows S370/S371/S373 require explicit QUALITY17 distinct-scope review"); "grounded in sources opened this round."
- Locator/command: `corpus/QUALITY.md:34-39` (criterion 17: screen repeated canonical URLs across active rows even when scope wording differs; "send distinct-scope reuse to human review rather than claiming URL equality proves semantic duplication. A warning-only shared census is not this review."); registry search-log line appended with the rows: "S370, S371 and S373 reuse canonical URLs with new scopes; distinct-scope review remains outstanding."; `corpus/lessons/round-52.md` Gate: "Review source URL collisions against prior rows before appending … remain pending final source audit."
- Observed: S370≡S365 (DispatcherTranslator.cpp), S371≡S367 (ConfigActions.cpp), S373≡S364 (KeybindManager.cpp) at the same commit `efb50993…`; W1 C2PinAudit finding 2 and RegistryContract both flagged the collisions and required recorded review; the rows were appended with the review self-declared outstanding. No review artifact exists in the wave or corpus.
- Verdict: reproduced — the registry process leg of "grounded in sources opened this round" is falsified as landed (rows admitted without the required review).
- Limitation: criterion 17 sends reuse to review rather than auto-rejecting; the scopes may survive review. The defect is the missing review, not the rows' substance.

### A18 — "Opened this round" remains a re-fetch ceremony at the byte level
- Attacked: "grounded in sources opened this round" (provenance honesty).
- Locator/command: digest comparison of the round fetch vs round-51 pins.
- Observed: 4/4 payloads byte-equal to `.ufo/waves/round-51/fetch/` (ConfigActions.cpp, ConfigActions.hpp, KeybindManager.cpp, legacy-DispatcherTranslator.cpp). The round-52 fetch dir carries its own SHA256SUMS (5/5 OK, including README.txt). Byte-equality cannot distinguish a genuine 2026-10-27 re-open from a local copy of round-51 bytes; the W1 C2Novelty N2 objection stands unresolved at the byte level.
- Verdict: limitation reproduced; not a falsifier (row ids S370–S373 are new, satisfying the only freshness mechanism the committed counter implements — and the one the draft counter implemented, A6, was removed).
- Limitation: no network evidence is available to seats; the README.txt assertion ("opened by lane L1 on 2026-10-27 via read URL") is unverifiable from bytes.

### A19 — Entry closing-paragraph provenance claims verify true
- Attacked: completeness-of-map duty cuts both ways — verified as fair record.
- Locator/command: entry closing paragraph vs bytes.
- Observed: "All pins are under `.ufo/waves/round-52/fetch/`" (4/4 map pins present), "revision efb50993780079460b0cbed1363e2166a2de1d9f" (matches), "checksums are in `.ufo/waves/round-52/fetch/SHA256SUMS`" (present, 5/5 verify). Title/intro mechanism summary is covered by the 18 mapped propositions.
- Verdict: reproduced (no unmapped material proposition in the landed entry's prose).

### A20 — P15's W1 quality defect is repaired by narrowing
- Attacked: W1 C2EntryQuality "P15 quote is only the save, not the restore" — inheritance check.
- Locator/command: entry P15 vs `DispatcherTranslator.cpp:612` and `:624`.
- Observed: landed P15 claims only "saves the prior `m_passPressed` value before changing it" (quote `:612`, true); the restore half is no longer asserted. The narrowing is honest and consistent with A19.
- Verdict: reproduced as repaired.

## Counter evidence (fairness)

- The landed entry's map is structurally richer than the minimum: 18 propositions over 4 rows, all quotes ≤25 words, rationales on every row, pins fetched this round with a valid checksum manifest, index row present, both slugs absent at base (Attack30 P0).
- The W1 draft counter (965 lines) demonstrably checks far more than the committed rewrite: it parsed this table shape, read pins, compared quotes, checked row-vs-base freshness, and on the landed state reports specific misses (`anchor_no_fetch_root` on all four rows — the landed registry anchors carry "r52 fetch SHA256" instead of a fetch path; `P16:quote_not_at_pin`; `P01..:id_not_referenced` — the landed entry's prose never cites proposition ids outside the map). Its TARGET_MISSED on the landed state corroborates A1, A9, and adds two landed-state defects my scope did not gate (anchor shape, id references).
- No counterexample was found against the truth of P01–P05, P07–P11, P13, P15, P18 at their pins (spot reads this seat).

## Smallest safe corrections (review-side; no predicate edit)

1. **Counter (blocking):** replace the committed 47-line rewrite with the W1 draft counter (or restore its checks): parse the landed table shape; read pins and bind quotes contiguously at anchors (this alone rejects P16 as spliced); re-check row freshness against the base registry; re-add completeness (prose claims), uniqueness, and claim-nonempty gates; set `ENTRY_DEFAULT` to the landed slug `hyprland-synthetic-dispatch-r52.md`; commit red/green receipts plus the base-absence receipt registration requires.
2. **Entry:** re-quote P16 as a contiguous excerpt that either includes the `m_passPressed == 1 / !isMouse` guard or narrows the proposition to the unconditional modifier send; extend P12's quote to :585-586 or split the proposition; re-quote P14 raw (`uint32_t    m_timeLastMs    = 0;  // …`) or freeze the collapsed policy on the receipt; reclassify P06 as held-fact/new-anchor with the r51 step-7 held cite; merge or differentiate P04/P17.
3. **Registry/process:** record the criterion-17 distinct-scope human review for S370/S371/S373 (or merge into the prior rows) before the round closes; commit the outside non-author per-proposition source-truth sample receipt.
4. **Judgment:** C2 as landed is TARGET_MISSED on its counter clause (A1–A8, A15) with the source map itself nearly sound (A9–A14 minor repairs); none of the defects is axis-harm beyond coverage honesty, and no predicate amendment is needed — the frozen predicate already requires everything the corrections restore.

## Errors reported

- A1/A2: committed counter integration breaks (regex grammar; default slug) — defects.
- A9: P16 splice — defect (also caught independently by sibling Attack12 with the draft counter).
- A15: missing committed receipts — process gap.
- A17: QUALITY17 review outstanding with rows already appended — process violation of corpus rule.
- No tool errors; no install; no network use; no host reads.

## Scratch and host discipline

Scratch `/fast/scratch/hyaku/mado-r52/Attack08/` held one clone of the lane (`lane/`, two commits deep: landed-state replica `c0b3a00c`, mutation-fixture branch `2708b01c` + 17 single-mutation commits, all reset after each run) and work dirs `w1..w5`, `wmut`, `wmut2`; all removed on exit. Every git mutation was inside the clone after asserting `git rev-parse --show-toplevel` printed the clone path. No git/jj operation touched the lane. No package install (stdlib only); pacman untouched. No live read, probe, screenshot, producer execution, or host mutation. No tracked-file writes; the only writes are this report and the removed scratch.

Report trailer:

```
seat=Attack08 wave=w2 round=52 lane=mado-shokunin base=85d57a818c3707397e21c840b6498b105ba798aa
claim=C2 coverage proposition-bound dispatcher source entry
attacked=counter clause (bindings+completeness) NOT REPRODUCED; quote map REPRODUCED in part (17/18 collapsed-bound, P16 splice fails); no-work control mechanically REPRODUCED; QUALITY17 review REPRODUCED outstanding; non-author sample NOT REPRODUCED (attack sample supplied)
items=20 (A1-A20)
key_evidence=committed counter 5c7fb820…47 lines TARGET_MISSED on landed state; draft counter 55452a3d…965 lines corroborates P16; mutations M1,M2,M7,M8,M14,M15 escape committed counter
report=.ufo/waves/round-52/w2/Attack08.md
```
