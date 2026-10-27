# R54W2Seat18 — C1 P21 repeat-state entailment

## Axes
Operability (P21 source-truth entailment); provenance (quoted bytes and exact anchor binding).

## Counterexample and evidence
Frozen registration P21 fixes the quoted source to `Hyprland-legacy-DispatcherTranslator.cpp`, anchor `:619-622`, and quote `auto result = sendshortcut(modifiedArgs); if (keyState == 2 && result.success) result = sendshortcut(modifiedArgs);` (`registration.md:25-34`). Frozen predicate requires its anchor at exactly 619–622 inside 591–627 (`claims-frozen.md:25-28`). The relevant committed round-52 pin shows the `sendkeystate` function boundary at 591–627: it parses `ARGS[2]` as allowed `down/repeat/up` (596–598), sets `keyState` from state (600 onward), saves `oldPassPressed` (612), sets pass mode for down/repeat (614–618), invokes `sendshortcut(modifiedArgs)` initially (619), conditionally invokes it again only for repeat (`keyState == 2`) and success (621–622), then restores old state (624).

Strongest counterexample to a broader reading that P21 proves repeat-state semantics: the pin never maps the textual `repeat` value to numeric `2` within the displayed excerpted evidence, nor establishes what `sendshortcut` does or that the second call produces a repeat rather than duplicate key-down. Registration freezes the quote/anchor, not an explicit separate assertion about parsed-state mapping or downstream effect. The immediate function context does establish an internal conditional second invocation guarded by numeric state 2 and prior success. Thus the exact frozen P21 quoted side-claim is supported; a claim that this alone entails externally meaningful repeat behavior is under-specified/unproven, not a falsification of the frozen quote predicate.

Exact pinned span available: round-52 pin output identifies function at lines 591–627 and exact source lines 591–598, 610–618, 621–627. Required exact quote span 619–622 is independently reproduced verbatim in frozen registration lines 29 and 32–34. W1 report `w1/R54Seat18.md:7-21` attacked coordinated pin+manifest substitution (a different P21-independent C1 issue); it did not establish this state-parsing boundary claim. Its section 27–36 records the prior evidence commands and absent producer. This round's P21 target remains limited to quote/anchor truth per the frozen contract.

## Checks / commands
- `read .../claims-frozen.md` → lines 19–44 show frozen C1 predicate/kill rule; exit 0 (tool returned content).
- `read .../registration.md` → lines 25–34 fix P21 quote and exact anchor; exit 0.
- `read .../w1/R54Seat18.md` → lines 7–21 prior finding; exit 0.
- `grep sendkeystate|keyState == 2|oldPassPressed .../round-52/fetch/Hyprland-legacy-DispatcherTranslator.cpp:591-627` → exact lines 591–598, 610–618, 621–627; exit 0.
- `grep c1-r54-errata-truth|sendshortcut .../quality/counters` → `No matches found`; counter NOT RUN/absent (no pinned command implementation available).
- No fixture or producer execution; no observed counter verdict.

## Smallest safe correction
Keep P21 narrowly phrased as frozen quote-at-anchor evidence. If repeat semantics are intended as an additional claim, register a separate pre-data predicate that pins the state mapping and downstream behavior; do not widen or edit this frozen predicate post-score.

## Report trailer
Lane-relative report: `.ufo/waves/round-54/w2/R54W2Seat18.md`. Scratch `/fast/scratch/hyaku/mado-r54/R54W2Seat18` created and removed before yield. No installation, fixture, git/jj mutation, producer execution, host/config/service/compositor mutation, or source edits.