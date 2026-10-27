# R54W2Seat16 — C1 P19 semantic entailment attack

## Axes
Semantic fidelity (quoted source entails proposition); provenance scope (claims stay bounded to pinned evidence); operability (whether the frozen C1 command exists to rerun).

## Finding — P19's exclusive condition is false

The proposition in the committed errata entry (`corpus/knowledge/hyprland-synthetic-dispatch-r52-errata-r53.md:17`) says `Actions::pass` sends a PRESSED keyboard key **only when** `m_passPressed == 1` and the key is not a mouse button. “Only when” asserts a necessary condition. The quoted excerpt and cited span do not entail that; the immediately following source branch falsifies it.

Exact pinned evidence: `.ufo/waves/round-52/fetch/Hyprland-ConfigActions.cpp:1554-1558` sends modifiers then enters the `m_passPressed == 1` branch, with keyboard press under `!isMouse`. But at `:1561-1573` the same function has the `else` branch for values other than 1 or 0 and, when `!isMouse`, sends a PRESSED keyboard key at `:1568` and then RELEASED at `:1569`. Thus the frozen excerpt establishes one sufficient path, not exclusivity. Pin lines `:1576` later clear modifier state and do not constrain the earlier dynamic branch.

This is not merely an unreachable theoretical value: Pinned `.ufo/waves/round-52/fetch/Hyprland-ConfigActions.hpp:114` declares `m_passPressed = -1` as the default and comments `-1 = dynamic (press+release), 0 = released, 1 = pressed`; `Hyprland-KeybindManager.cpp:814` resets it to `-1` after dispatch (reported with evidence in w1 `R54Seat17.md:107-118`). The dispatcher pin itself calls `Actions::pass` through `sendshortcut` at `Hyprland-legacy-DispatcherTranslator.cpp:588`; so a proposition claiming “only when == 1” is not rescued by the nearby quoted branch.

Frozen contract lines: `claims-frozen.md:22-28` requires each corrected proposition's quote to occur in its named round-52 pin/anchor; `registration.md:25-34` freezes P19's quoted fragment and exact anchor. Neither requirement checks whether the English Proposition cell is entailed by broader pin context. The w1 R54Seat16 report focused on do-nothing reachability, controls, and scored invocation (`w1/R54Seat16.md:17-37`), not semantic entailment. W1 R54Seat28 independently documented the same concrete P19 counterexample at `w1/R54Seat28.md:47,62-118`; this report reopens the precise assigned semantic issue and independently reads the pin lines above.

Impacted axes: semantic fidelity and provenance scope fail for P19. Quote/pin/anchor integrity alone can pass while the asserted necessary condition is contradicted. Operability: the frozen command is not available at base: `claims-frozen.md:32-33` records no C1 r54 counter; no C1 command was run here, in accordance with the assignment's absent-counter instruction.

Smallest safe correction: do not treat the current P19 Proposition as supported. Preserve the frozen claim/registration; for any future versioned, pre-score registration, either narrow the proposition to the demonstrated sufficient case (“When `m_passPressed == 1` and `!isMouse`, `Actions::pass` sends a PRESSED keyboard key”) or cite/check the dynamic branch and phrase the broader behavior with its exceptional conditions. A semantic entailment requirement should be explicit if the counter is intended to certify English proposition truth; text edits after scoring are not appropriate.

## Command/output record

- `read skill://godspeed` → skill instructions; no command exit code supplied by tool.
- `read` frozen `claims-frozen.md`, `registration.md`, `w1-results.json`, w1 report and P19 source entry/pins → outputs cited above; these are read-only tool calls, no shell exit code supplied.
- `grep` w1 reports for semantic/P19 evidence → matches include R54Seat28's P19 finding and R54Seat17's supporting assignment evidence; no shell exit code supplied.
- `mkdir -p /fast/scratch/hyaku/mado-r54/R54W2Seat16 && printf ... && test -d ... && printf ...` → `scratch=/fast/scratch/hyaku/mado-r54/R54W2Seat16\ncreated=0\n`, exit 0.
- Counter invocation: **NOT RUN / absent** per base receipt (`claims-frozen.md:32-33`); no counter output or exit code to report.
- No fixture or git command used. No install/package query or host/config/service/compositor read/change.
- Scratch cleanup: `rm -rf /fast/scratch/hyaku/mado-r54/R54W2Seat16 && if test ! -e /fast/scratch/hyaku/mado-r54/R54W2Seat16; then printf 'scratch_removed=0\n'; else printf 'scratch_remaining=1\n'; fi` → `scratch_removed=0`, exit 0.

## Report trailer

Lane-relative report: `.ufo/waves/round-54/w2/R54W2Seat16.md`. No frozen predicate, registration, lane source, or sibling file changed.