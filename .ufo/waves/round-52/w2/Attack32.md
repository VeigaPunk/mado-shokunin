# Attack32 — round 52 w2: C2 source claims versus runtime/host inference

Seat: `Attack32` (critic, leaf). Wave `w2`; attack, not a vote; no claim or predicate edits.
Axes named: **coverage** (C2 source-truth of the landed entry; premature-saturation risk) and
**operability** (C2 counter behaviour at the frozen revision). Lane repo
`/home/vgpnk/Projects/shokunin/mado-shokunin`, frozen base
`85d57a818c3707397e21c840b6498b105ba798aa` (also `HEAD`; the W1 landing sits uncommitted in the
working tree — `git status`: modified `corpus/SOURCES.md`, `corpus/README.md`,
`quality/tool-ledger.md`; untracked `corpus/knowledge/hyprland-synthetic-dispatch-r52.md`,
`quality/counters/c2-r52-proposition-entry.py`, `quality/counters/c1-r52-ledger.py`).

Assignment: attack C2 source claims against runtime/host inference; find concrete falsifiers or
verify the specified controls, after W1 evidence. All evidence below is from local reads/executions
at the frozen base, the lane working tree, or the wave's own pinned bytes; no network, no live
reads, no host/compositor state, no installs, no tracked writes outside this seat dir and report.
Fixture git mutations were performed only inside a scratch clone of the lane, after
`git rev-parse --show-toplevel` asserted the clone root (`/fast/scratch/hyaku/mado-r52/Attack32`,
removed on exit; receipts copied here first). Python 3.14.8.

## State discovered (precondition)

The C2 target has been landed in the working tree, not committed: entry
`corpus/knowledge/hyprland-synthetic-dispatch-r52.md` (32 lines, 18 propositions P01–P18, rows
S370–S373 appended to `corpus/SOURCES.md`, index row appended to `corpus/README.md`). The landed
entry is a **rewrite** of the W1 draft: it drops every runtime-flavoured claim the W1 critics
attacked (draft P13's "last *real* input event", draft P16's xtract/"focused window" claim, draft
P17's no-window claim) and re-words to call-shape claims. This seat independently re-verified the
landed bytes rather than trusting the W1 receipts.

## Attack register

Verdicts: REPRODUCED = W1-flagged signal confirmed against landed bytes; NOT REPRODUCED = W1 signal
does not hold against landed bytes; NEW = defect not flagged in the W1 reports I read.

### A1 — Landed P16's quote is spliced and does not bind at its anchor (NEW; blocks frozen "exact located quote")

- **Attacked clause:** claims-frozen.md C2 — "each material factual proposition maps to a pinned
  source quote <=25 words"; registration C2 — "exact located quote ≤25 words".
- **Reproduction:** independent span check (`attack32-quote-verify.py`, receipt
  `ev-quote-verify.txt`): P16 anchor `Hyprland-ConfigActions.cpp:1554-1558,1576`, quote
  ``g_pSeatManager->sendKeyboardMods(modMask, 0, 0, 0); g_pSeatManager->sendKeyboardKey(S.m_timeLastMs, key - 8, WL_KEYBOARD_KEY_STATE_PRESSED);``.
  Pinned lines :1554–:1558 are:
  `:1554 sendKeyboardMods(modMask, 0, 0, 0);` / `:1555 (blank)` / `:1556 if (S.m_passPressed == 1) {`
  / `:1557 if (!isMouse)` / `:1558 sendKeyboardKey(S.m_timeLastMs, key - 8, WL_KEYBOARD_KEY_STATE_PRESSED);`.
  The collapsed span keeps the intervening `if (S.m_passPressed == 1) { if (!isMouse)` tokens, so
  the quote — which concatenates :1554 and :1558 and drops the conditional between them — is not a
  substring of the collapsed span under the frozen whitespace-collapsed policy, nor raw. The
  counter-relevant corollary: the `,1576` tail of the anchor (the actual modifier-clear call) is
  silently truncated by the W1 draft counter's `parse_pin_cell` regex `(\d+)(?:-(\d+))?` and is
  not parsed by any counter.
- **Observed:** `P16 collapsed=False raw=False`; the W1 counter against honestly staged fixtures
  reports `P16:quote_not_at_pin(Hyprland-ConfigActions.cpp:1554)` (`ev-w1-honest-staging.txt`).
- **Verdict:** NEW, reproduced on lane bytes. 17/18 landed quotes bind collapsed; P16 does not.
- **Impacted axes:** coverage (the frozen predicate itself fails at the entry, independent of any
  counter), operability (multi-span anchors are silently truncated).
- **Smallest safe correction:** re-quote P16 as the literal contiguous lines (e.g.
  `:1554-1556` `sendKeyboardMods(modMask, 0, 0, 0); if (S.m_passPressed == 1) {`) or split into
  two propositions; if a multi-span anchor is intended, the counter must parse it explicitly.

### A2 — Landed P16 flattens the `m_passPressed` conditional (source claim vs runtime inference; NEW)

- **Attacked clause:** registration C2 — "outside reviewer judges source truth"; claims-frozen.md
  C2 — the entry is "grounded in sources opened this round".
- **Reproduction:** same source region. The claim "The action sends modifier state before the key
  event, then clears the modifier state" presents an unconditional call sequence. The source sends
  the quoted `PRESSED` key call only inside `if (S.m_passPressed == 1)` (:1556); the `RELEASED`
  call (:1563) runs when the field is `0`; both (:1568–:1569) otherwise. The field is precisely
  what `sendkeystate` overrides (:615/:617). "Then clears" rests on :1576, which is not in the
  quoted text at all.
- **Observed:** claim is true only as a per-branch sequence; as worded it asserts a runtime trace
  the quote does not exhibit. This is the same shape as the W1-flagged M51-2 class (claim broader
  than cited lines), resurfacing inside the landed rewrite that was supposed to remove it.
- **Verdict:** NEW. Limitation: entailment judgment is the non-author reviewer's; this seat records
  the mechanical part (quote does not exhibit the claimed sequence).
- **Impacted axis:** coverage honesty.
- **Smallest safe correction:** word P16 as "sends the modifier mask, then one key branch selected
  by `m_passPressed`, then clears the mask", with a contiguous quote covering the branch selector.

### A3 — Landed P17 misattributes the repeat branch to `sendshortcut`; P04/P17 are a semantic duplicate (NEW)

- **Attacked clause:** claims-frozen.md C2 "distinct new indexed knowledge entry"; registration C2
  "at least four substantive propositions" (substance, not restatement).
- **Reproduction:** pinned `Hyprland-legacy-DispatcherTranslator.cpp`: `static SDispatchResult
  sendkeystate(...)` at :591; the double-invocation `auto result = sendshortcut(modifiedArgs);
  if (keyState == 2 && result.success) result = sendshortcut(modifiedArgs);` at :619/:622 — inside
  `sendkeystate`. Landed P17 claim: "**`sendshortcut`'s repeat branch** can invoke its delegate
  twice for a successful repeat state", anchor :619-622. `sendshortcut` has no repeat branch.
  Landed P04 ("`repeat` calls its delegate again only after a successful first call", same anchor)
  states the same fact correctly; the counter's duplicate-claim check uses punctuation-free
  casefolded keys, and the two strings differ, so both pass.
- **Observed:** one proposition wrong about which function it describes; effective proposition
  count 17, with P04/P17 a near-paraphrase pair (same anchor; P17's quote is a substring of P04's).
- **Verdict:** NEW. Not caught by either counter (entailment boundary, declared by both).
- **Impacted axis:** coverage (inflated proposition count; wrong attribution is source-truth
  defect).
- **Smallest safe correction:** delete P17 or re-word to the `sendkeystate` repeat semantics that
  is not already P04 (e.g. the `m_passPressed` write pairing).

### A4 — Source semantics refute the draft-era "empty selector targets the focused window"; landed P12 keeps a type-level misdescription (REPRODUCED, narrowed)

- **Attacked clause:** W1 signal "C2 new pins and claim table require independent re-open and
  source truth"; draft P16 (withdrawn in landing).
- **Reproduction:** pinned bytes: `wrap(Actions::pass(MOD, keycode, PWINDOW))` at
  `Hyprland-legacy-DispatcherTranslator.cpp:588`; `ActionResult Actions::pass(uint32_t modMask,
  uint32_t key, std::optional<PHLWINDOW> w)` at `Hyprland-ConfigActions.cpp:1530`; `auto window =
  xtract(w);` at :1531; `xtract` = `return window.value_or(Desktop::focusState()->window());` at
  :47–:49. `PWINDOW` is a `PHLWINDOW` (:583); converting a null `PHLWINDOW` into
  `std::optional<PHLWINDOW>` **engages** the optional holding null, so `value_or`'s fallback never
  fires for the sendshortcut path: `window` stays null, and control reaches `if (!window)
  return {};` at :1578 after the sends. The source therefore establishes: empty selector →
  nullptr → seat calls still execute → focus bookkeeping skipped. It does **not** establish any
  delivery target: `sendKeyboardKey`/`sendKeyboardMods` take no window parameter at all; "what the
  event targets" is compositor runtime state, unreachable from source-only evidence.
- **Observed:** the draft's "an empty selector targets whatever is focused" was a host-runtime
  inference refuted by the source (C2Novelty's mechanism note verified at the bytes — REPRODUCED).
  The landing avoided that inference but P12 now says "Empty selector input produces a **null
  optional** window": at the translator site the value is a null `PHLWINDOW`, not an optional; the
  optional (engaged-with-null) exists only inside `pass`. The surviving wording blurs the same
  null-handle/disengaged-optional distinction the W1 critic flagged.
- **Verdict:** REPRODUCED (inference refuted at source level); NEW residual misdescription in P12.
- **Impacted axis:** coverage honesty (the boundary the whole round's safety rule draws).
- **Smallest safe correction:** P12 → "Empty selector input produces a null window handle; a
  written selector that resolves to nothing is rejected"; add a Limits line that delivery
  destination is seat/compositor runtime state and not claimed.

### A5 — Integrated counter cannot read the landed entry (props=0) (NEW; duplicate authority)

- **Attacked clause:** registration C1/C2 shared instrument rule — "A new committed counter checks
  proposition count, row/pin/quote bindings and index"; C1-ledger accountability for the tracked
  population.
- **Reproduction:** `python3 -I quality/counters/c2-r52-proposition-entry.py --repo <clone> --rev
  <landing> --entry corpus/knowledge/hyprland-synthetic-dispatch-r52.md` →
  `props=0 rows=0 indexed=1 failures=1 miss=props verdict=TARGET_MISSED exit=1`
  (`ev-integrated-vs-landed.txt`). The integrated counter hardcodes column order
  `| P | S### | claim | pin | _ | quote | rationale |` (one regex); the landed table is
  `| ID | Proposition | Source row | Pin:anchor | Quote | Support class | Why it supports |` —
  row id in the third cell, not the second.
- **Observed:** the counter present in the lane working tree scores the landed entry zero
  propositions. It is also a **different program** from the reviewed W1 draft: sha256
  `5c7fb820e43c7f6782b6ebfc90d018c25d74976d9e8ab2a90df5e4c82fb50c0a` vs the draft's
  `55452a3d6eab7cca2b20095f8678fbe936c8c65f241a561611a675defd8379fb` (~50 lines vs 965), same
  PRED name `PRED-C2-r52`, no receipts, not the byte-identical copy the W1 seat's integration note
  specified. Two authorities, one predicate.
- **Verdict:** NEW.
- **Impacted axis:** operability.
- **Smallest safe correction:** either copy the reviewed W1 draft byte-identically (its
  header-name grammar reads the landed table unchanged) and retire the rewrite, or re-run the
  W1 review against the rewrite; record which program produced any green receipt.

### A6 — Integrated counter certifies a fabricated quote (NEW; frozen "quote bindings" not checked)

- **Attacked clause:** claims-frozen.md C2 — "A new committed counter checks proposition count,
  row/pin/quote bindings and index."
- **Reproduction:** fixture mutant on top of the shape-fixed table (mutant A: same 18 rows,
  columns in the integrated counter's order → `props=18 rows=4 indexed=1 failures=0
  verdict=TARGET_MET exit=0`); mutant B replaces P01's quote with
  ``completely fabricated words that appear nowhere in any pin file at all`` → integrated counter
  again `verdict=TARGET_MET exit=0` (`ev-integrated-mutants.txt`). The integrated counter never
  opens a pin file; it checks only that the quote cell is ≤25 words and that registry rows contain
  `mined`/`2026-10-27`/the entry path/a 40-hex string.
- **Observed:** the production-position counter passes an entry whose quotes are invented. The W1
  draft counter, run against the same mutant commit, exits 1 (`ev-w1-vs-landed.txt` companion run
  in scratch transcript).
- **Verdict:** NEW.
- **Impacted axis:** operability (the counter cannot falsify a C2 source claim — the exact
  failure mode this claim was frozen to close, per mistake-candidate M52-1).
- **Smallest safe correction:** use the W1 draft counter (clause (d) binds quotes at pins); at
  minimum add an at-pin check and a mutation receipt for quote tampering.

### A7 — W1 draft counter cannot pass the lane as landed: registry anchor wording (REPRODUCED)

- **Attacked clause:** registration C2 — counter checks "row/pin/quote bindings"; W1 freeze notes
  ("the anchor must name `.ufo/waves/round-52/…/fetch/…` and revision `efb50993…`").
- **Reproduction:** W1 counter vs the landed staging (clone commit `fdd825b9`): clauses
  `a ok=1, b ok=1, c ok=0 rows_bound=0/18 miss=P01..P04:anchor_no_fetch_root, d ok=0
  quotes_bound=0/18 miss=...pin_file_absent(...), e ok=0 miss=P01..P04:id_not_referenced` →
  `clauses_met=2 verdict=TARGET_MISSED exit=1` (`ev-w1-vs-landed.txt`). Landed S370–S373 anchor
  cells read `... @ efb50993780079460b0cbed1363e2166a2de1d9f; r52 fetch SHA256 7248cbb8…` — a
  digest, not the fetch path the counter requires.
- **Observed:** the data seat's row wording and the reviewed counter's clause (c) are mutually
  incompatible; no receipt shows them reconciled. Fixable on either side.
- **Verdict:** REPRODUCED (the W1 signal "counter draft r-green proves a separate synthetic
  fixture only, not landing" — confirmed: r-green/receipt-6 were synthetic-staging runs).
- **Smallest safe correction:** reword the four anchor cells to
  `pin .ufo/waves/round-52/fetch/Hyprland-<name>.cpp` (or relax the counter to accept
  `r52 fetch SHA256` form); re-run and archive the receipt.

### A8 — W1 counter pin resolution broken by duplicate pin bytes in the wave tree (NEW)

- **Attacked clause:** operability of the production pass at the frozen revision.
- **Reproduction:** `find .ufo/waves/round-52 -name 'Hyprland-*'` in the lane working tree
  (`ev-pin-duplication.txt`): 9 copies — the wave fetch (4), `w1/C2EntryDraft/fetch/` (4,
  byte-identical), and `w1/Falsify29/fixture/pins/Hyprland-KeybindManager.cpp` (byte-identical,
  sha256 `8d8f35fc…`). The W1 counter's `pin_index` maps basename→path under
  `--fetch-root .ufo/waves/round-52` and drops any basename seen twice, so in the honest staging
  run P07 still fails `pin_file_absent(Hyprland-KeybindManager.cpp)` and `pins=3`
  (`ev-w1-honest-staging.txt`); in the lane as-landed all four basenames collide → 18/18
  `pin_file_absent`.
- **Observed:** seat fixture bytes left inside the wave tree defeat the production counter for
  every proposition; nothing in the landing cleans or scopes them.
- **Verdict:** NEW.
- **Smallest safe correction:** remove/relocate `w1/*/fixture/pins` copies (or point
  `--fetch-root` at `.ufo/waves/round-52/fetch`); add a wave-hygiene note to the integration
  checklist.

### A9 — Landed entry fails clause (e): no proposition id is drawn on outside the map (NEW)

- **Attacked clause:** registration C2 counter scope "and complete mapping" (as implemented in the
  reviewed counter's clause (e)).
- **Reproduction:** the landed entry is 32 lines: front matter, the 18-row proposition table, and
  a closing line. No prose sentence cites any `P##` id; `referenced_ids` requires each id to occur
  ≥2 times across the entry. Honest-staging run: `e ok=0 ... miss=P01:id_not_referenced,…` for all
  18 (`ev-w1-honest-staging.txt`). The W1 draft carried a "What the evidence licenses" table that
  satisfied this; the landing dropped it.
- **Observed:** even with A7/A8 fixed, the reviewed counter scores the landed entry 3/5
  (`clauses_met=3`, failing d on P16 and e on all ids).
- **Verdict:** NEW.
- **Smallest safe correction:** restore a per-proposition "licensed claim" table or paragraph
  citing each id; or amend the counter if the lane reads clause (e) as row-granularity only (the
  counter's own docs flag this as its strictest edge).

### A10 — P14 is not raw-verbatim at the pin (REPRODUCED)

- **Attacked clause:** claims-frozen.md C2 "exact located quote"; W1 N4.
- **Reproduction:** pinned `Hyprland-ConfigActions.hpp:117` reads
  `uint32_t    m_timeLastMs    = 0;  // timestamp of last key/mouse event` (multiple spaces,
  two before the comment). Landed P14 quote: ``uint32_t m_timeLastMs = 0; // timestamp of last
  key/mouse event`` — whitespace-collapsed only. My verification: 6/18 quotes raw-bind, 12/18
  reflowed (`ev-quote-verify.txt`); the honest W1 run prints `quotes_raw=6/16` bound set
  (`quotes_raw=6/18` on full lane staging semantics).
- **Observed:** the W1-flagged N4 defect survived landing unchanged. Under the counter's frozen
  `quote_policy=whitespace-collapsed` the verdict does not flip; under a raw policy it would.
- **Verdict:** REPRODUCED. Smallest safe correction: re-quote P14 with the pin's exact spacing.

### A11 — QUALITY17 distinct-scope review for S370/S371/S373 is admitted outstanding (REPRODUCED)

- **Attacked clause:** `corpus/QUALITY.md:34` criterion 17 — "screen repeated canonical URLs
  across active rows even when scope wording differs… send distinct-scope reuse to human review";
  registration C2 "grounded in sources opened this round."
- **Reproduction:** S370≡S365 (`DispatcherTranslator.cpp`), S371≡S367 (`ConfigActions.cpp`),
  S373≡S364 (`KeybindManager.cpp`) — same URL, same commit `efb50993…`; only S372
  (`ConfigActions.hpp`) is a new URL. The landed registry's own search log states: "S370, S371 and
  S373 reuse canonical URLs with new scopes; **distinct-scope review remains outstanding**."
  Anchor-level check supports distinctness (S364's anchors :41-113,602,782,785,798-823 do not touch
  `stringToModMask` :221-242; S365's :30-35,797-867 do not touch :531-627; S367's :1664-1682 do not
  touch :1530-1616) — so the reuse is defensible, but the mandated explicit human review has not
  been recorded anywhere; the rows' `teaches` cells ("no host event asserted", "distinct from
  runtime receipt", "do not establish host event effects") are disclaimers, not a review record.
- **Verdict:** REPRODUCED (W1 signal "repeated URL rows S370/S371/S373 require explicit QUALITY17
  distinct-scope review").
- **Impacted axes:** coverage, operability. Smallest safe correction: append the criterion-17
  review verdict (per row, with reviewer id) to the registry or the round receipts before scoring.

### A12 — "Opened this round" rests on byte-identical re-fetches (REPRODUCED)

- **Attacked clause:** claims-frozen.md C2 "grounded in sources opened this round."
- **Reproduction:** sha256 of the four `.ufo/waves/round-52/fetch/` pins vs the round-51 pins:
  4/4 byte-identical (`ev-pin-duplication.txt`; the wave `SHA256SUMS` and the seat `verify.txt`
  agree). W1 counter on the full lane staging prints `pins_prior_equal=4` (honest staging: 3 of
  the bound pins, P07's pin excluded by the A8 ambiguity). Clause (c)'s `row_not_new` check passes
  because the row ids are new — it cannot see byte identity.
- **Verdict:** REPRODUCED (C2Novelty N2). Limitation: per the counter's own documented policy,
  reopening a pinned file under a new scope is legitimate; the defect is the missing disclosure on
  the receipt and the missing criterion-17 review (A11), not the reuse itself.
- **Smallest safe correction:** keep `pins_prior_equal` on the integration receipt; record the
  criterion-17 review.

### A13 — No production receipt exists for the landed entry (REPRODUCED)

- **Attacked clause:** registration C2 — "Selftest includes explicit red/green receipts" (C1
  phrasing; the C2 analogue: receipts must name the revision they score).
- **Reproduction:** `.ufo/waves/round-52/receipts/` holds only `c1-base.txt`, `c2-base.txt` (the
  latter is the r51 counter at base: `admitted=1/1 verdict=TARGET_MET` for the r51 entry —
  registration explicitly distrusts it for the r52 target). No receipt in the lane scores
  `hyprland-synthetic-dispatch-r52.md`; the W1 green receipts (`r-green`, `r-draft-as-is`,
  `r-draft-fixed`) score a synthetic fixture and the *draft* bytes in scratch staging.
- **Verdict:** REPRODUCED ("counter draft r-green proves a separate synthetic fixture only, not
  landing").
- **Smallest safe correction:** after A7–A9 are fixed, run the chosen counter at a committed
  revision of the landed entry and archive the receipt under
  `.ufo/waves/round-52/receipts/`.

## Controls verified (specified controls, not attacked)

- **C2 no-work control (frozen base, entry absent):** integrated counter → `entry=absent
  verdict=TARGET_MISSED exit=1`; W1 draft counter → `clauses_met=0 admitted=0/1
  verdict=TARGET_MISSED exit=1` (`ev-base-controls.txt`, run live in the scratch clone against
  `85d57a81`). REPRODUCED for both programs.
- **Independent quote re-verification of the landed table:** my own span checker (not the seats'
  `check-quotes.py`) against `.ufo/waves/round-52/fetch/`: 17/18 collapsed-bind, 6/18 raw-bind,
  P16 splice fails both (`ev-quote-verify.txt`).
- **Claim-table anchors otherwise line-exact:** P01–P15, P17, P18 anchors verified at the pins by
  the same run (P17's anchor is exact; it is the claim text that misattributes the function, A3).

## What survives (fairness record)

- The landing's instinct to strip runtime inference was correct: every host-behavior claim the W1
  critics attacked is gone from the landed entry, and the remaining claims are call-shape/grammar
  level. A4 shows the strongest inference ("empty selector targets focused window") is refuted by
  the source itself, so the lane should treat any revival of it as a known-false premise.
- The pinned bytes are internally consistent: my line-number audit agrees with C2PinAudit's
  (anchors exact; m_timeLastMs writers are the inbound path only, `KeybindManager.cpp:385/:484`,
  so P14's "last key/mouse timestamp" wording is source-safe).
- P01–P11, P13, P15, P18 are true at the quoted lines and on ground no admitted entry holds
  (consistent with C2Novelty's distinctness verdict).

## Errors reported

- A1 (quote splice), A3 (wrong-function claim + duplicate), A5 (counter cannot parse landed
  table), A6 (counter passes fabricated quote), A8 (fixture bytes break pin resolution), A9
  (clause (e) failure), plus reproduced W1 signals A10–A13.

## Limitations

- This seat ran the reviewed W1 draft counter and the integrated counter against **scratch-clone
  fixtures** (git mutations only in the clone, toplevel-asserted); the lane working tree itself
  was only read. No commits were made to the lane; no tracked file was written outside
  `.ufo/waves/round-52/w2/Attack32*` and this report.
- The integrated counter's provenance (which seat/L1 wrote it) is not recorded in the bytes I
  read; I report its existence and divergence, not authorship.
- A2/A4 semantic judgments are flagged for the non-author source-truth reviewer; this seat's
  verdicts on them are mechanical (quote does not exhibit the claimed sequence; source semantics
  of engaged-null optional).
- The W1 counter runs used the clone commits `fdd825b9` (lane overlay), `7ec92b9d` (shape fix),
  `364cdd34` (fabricated quote), `e9817678` (honest staging); receipts reproduced in
  `ev-*.txt`.
- P13's generic "the key-delivery call" is instantiated by the PRESSED-branch call (:1558) while
  three key-delivery calls exist (:1558/:1563/:1568-1569); noted as imprecision, not defect.
- No package installs (none needed; RULES.md channel never reached). No network, no live reads,
  no probes, no screenshots, no host mutation.

## Deliverables

| artifact | path (relative to lane root) |
|---|---|
| this report | `.ufo/waves/round-52/w2/Attack32.md` |
| independent quote verifier | `.ufo/waves/round-52/w2/Attack32/attack32-quote-verify.py` |
| quote verification receipt | `.ufo/waves/round-52/w2/Attack32/ev-quote-verify.txt` |
| integrated counter vs landed | `.ufo/waves/round-52/w2/Attack32/ev-integrated-vs-landed.txt` |
| integrated counter mutants A/B | `.ufo/waves/round-52/w2/Attack32/ev-integrated-mutants.txt` |
| W1 counter vs landed staging | `.ufo/waves/round-52/w2/Attack32/ev-w1-vs-landed.txt` |
| W1 counter honest staging | `.ufo/waves/round-52/w2/Attack32/ev-w1-honest-staging.txt` |
| base controls (both counters) | `.ufo/waves/round-52/w2/Attack32/ev-base-controls.txt` |
| pin duplication map + digests | `.ufo/waves/round-52/w2/Attack32/ev-pin-duplication.txt` |

## Report trailer

```
seat=Attack32 wave=w2 round=52 lane=mado-shokunin base=85d57a818c3707397e21c840b6498b105ba798aa
claim=C2 coverage proposition-bound dispatcher source entry (source claims vs runtime/host inference)
axes=coverage operability
attacked=C2 frozen clauses "exact located quote <=25 words","row/pin/quote bindings","grounded in sources opened this round"; landed entry items P04,P12,P14,P16,P17; QUALITY.md:34 criterion 17 on S370/S371/S373; counter instruments c2-r52-proposition-entry.py (integrated) and w1/C2CounterDraft draft
new_defects=A1(P16 spliced quote, no policy binds),A2(P16 conditional flattening),A3(P17 wrong function+dup of P04),A4(P12 "null optional" misdescription),A5(integrated counter props=0 on landed table; duplicate authority sha 5c7fb820 vs draft 55452a3d),A6(integrated counter passes fabricated quote),A8(wave-tree duplicate pin bytes defeat pin_index),A9(clause(e) id_not_referenced x18)
reproduced_w1=A4(draft xtract inference refuted at source),A7(anchor wording vs clause c),A10(P14 not raw-verbatim),A11(QUALITY17 review outstanding),A12(pins_prior_equal 4/4),A13(no landing receipt; r-green synthetic only)
controls_verified=no-work control TARGET_MISSED on both counters at 85d57a81 (ev-base-controls.txt); independent 17/18 collapsed quote verification
verdict=C2 source claims: 17/18 mechanically bound, P16 not; runtime-inference claims correctly absent from landing but P16 flattens a conditional; production counter state is broken (integrated cannot read entry, W1 counter cannot pass lane); no landing receipt exists
limitations=fixture git mutations only in toplevel-asserted scratch clone; semantic items flagged for non-author reviewer; lane working tree read-only
receipts=.ufo/waves/round-52/w2/Attack32/ev-*.txt
report=.ufo/waves/round-52/w2/Attack32.md
```
