# C2EntryQuality — round 52

## Deliverables

- `.ufo/waves/round-52/w1/C2EntryQuality.md`

## Scope and axes

Axes: coverage and operability. Independently reviewed the candidate entry, proposition map, quote receipt, pin manifest, and locally available source bytes. No claim/predicate edits, source-repository writes, execution, or external fetches.

## Grounding findings

Candidate reviewed: `.ufo/waves/round-52/w1/C2EntryDraft/entry-draft.md`, proposed slug `hyprland-synthetic-key-dispatch-r52`; map `proposition-map.tsv`; pins `pins.txt`; `quotes-check.txt` reports 16 props, 4 rows, 4 pins, zero quote-check failures. I independently read the cited ranges in the local round-51 pins. The main mechanism is substantially grounded in those bytes: e.g. `sendkeystate` validates four fields and delegates (`Hyprland-legacy-DispatcherTranslator.cpp:591-626`), `sendshortcut` parses/resolves fields (`:531-589`), and `Actions::pass` emits the key/modifier events (`Hyprland-ConfigActions.cpp:1530-1598`). This is source-shape evidence only, not runtime behavior.

Actionable grounding defects / overstatements:

- **P10 quote does not support the full proposition.** The cited exact quote at `Hyprland-legacy-DispatcherTranslator.cpp:565-566` shows the loop and one-symbol lookup, but not the decisive comparison `if (sym == KEYSYM)` at :567. The full source does support the proposition; the mapped quote should include :567 and rationale should note the comparison. The entry additionally says the loop keeps the last matching keycode (entry lines 102-106), and correctly labels this `[INF]`; the source loop has no `break` and assigns each match at :568-569.
- **P11 overstates the cache key as an unambiguous pair.** Its quote at `:557` is `std::format("{}{}", rc<uintptr_t>(KB.get()), KEY)`: pointer representation and raw key spelling are concatenated with no delimiter. The bytes support “concatenates keyboard address and raw key text,” but do not establish an injective `(pointer, key)` encoding; possible string collisions are not excluded. Narrow the factual statement to the literal concatenation or explicitly disclose that limitation. The case-preservation `[INF]` is consistent with the code.
- **P15 quote is only the save, not the restore.** The map quotes `oldPassPressed` at `:612` while its proposition asserts restoration after delegation. The source has the separate assignment at :624. Include it in the quote/anchor or split proposition; source itself does restore after both delegate calls.
- **P16 quote establishes only existence/signature.** The mapped quote at `Hyprland-ConfigActions.cpp:1601` cannot support the proposition's “same repeat rule.” The body at :1603-1617 does establish state setup, repeat on `keyState == 2 && result.has_value()`, and restoration. Expand pin anchor/quote to include those lines (within quote word limit) or divide the proposition. The entry's separate `result.success`/`has_value()` equivalence is appropriately marked `[INF]`, not proven by the signature.
- **P12 combines claims beyond its mapped evidence.** The mapped translator quote :582-586 supports empty selector -> `nullptr` and unresolved-selector error, but “empty third field means the focused surface” depends on the `Actions::pass` behavior. The locally read implementation returns without changing focus when `window` is null (`Hyprland-ConfigActions.cpp:1578-1579`). Include this source binding or narrow the wording; avoid saying “focused surface” as though it were the selected target (the input is delivered through the current seat focus).

Completeness spot-check: the mapped P01-P16 cover the entry's central mechanism claims, including counts, states, key resolution, target selector, event fields and twin action. The prose’s “highest matching keycode survives” and cache case behavior are explicit `[INF]` at lines 102-106/207-209; no contrary claim found. Observations at 182-193 repeat already mapped or explicitly state limitations. The claim that no client effect/runtime behavior is established is appropriate.

## Distinctness and source-opening limits

The subject is a meaningful adjacent slice rather than a duplicate of R51: R51's `sendkeystate` mention is only that it saves/restores `m_passPressed` (R51 entry lines 197-199); the candidate analyzes its state grammar and synthetic-event path. `sendshortcut`'s grammar was also only a brief example at R51 lines 203-215. The candidate's event manufacture, resolver, seat calls and timestamps are not covered there. The two entries share code and must retain explicit held-ground boundaries; the candidate does so at lines 10-20 and 31.

Important predicate/evidence boundary: the candidate describes S370-S373 as proposed rows, explicitly “not yet appended” (entry lines 22-30). `pins.txt` says the three reused source files came from `.ufo/waves/round-51/fetch/`, fetched 2026-10-27 10:03:30Z, and only the config-actions header is a new URL; no URL was fetched this seat this round. C2SourceRecon also reported no source opened under round-52/fetch at its check. I did open the exact local bytes this round (read ranges cited above), but cannot verify from this evidence that a source URL was newly opened this round or that the proposed S370-S373 rows have been admitted as round-52 opened rows. In particular, a rehashed R51 cache proves byte identity, not fresh upstream access. This remains for the data/evidence seats to establish under the frozen predicate; do not represent `quotes-check.txt` as evidence of source opening or semantic truth.

## Evidence and verification limits

- Read round-52 frozen claim and registration first; they require at least four substantive propositions mapped to opened-this-round rows, exact quotes <=25 words, support rationales, and outside source-truth review.
- Read candidate entry lines 1-219, `proposition-map.tsv` rows P01-P16, `pins.txt`, and quote receipt. Quote receipt is a candidate-authored checker result; not independently rerun.
- Independently read local source ranges: `.ufo/waves/round-51/fetch/Hyprland-legacy-DispatcherTranslator.cpp:531-630`, `Hyprland-ConfigActions.cpp:1530-1622`, `Hyprland-ConfigActions.hpp:109-119`, `Hyprland-KeybindManager.cpp:221-242`.
- No URLs fetched, no runtime/event/input behavior tested, no outside source-truth reviewer performed by this seat. Access date for local reads: 2026-10-27. Candidate URL rows: raw.githubusercontent.com/hyprwm/Hyprland at commit `efb50993780079460b0cbed1363e2166a2de1d9f`; candidate pins record file digests and upstream fetch date in the R51 fetch manifest. No new source URL access date can be claimed.
- No installs. No package queries, live reads, probes, producer execution, or source checkout writes.

## Report

- `.ufo/waves/round-52/w1/C2EntryQuality.md`
