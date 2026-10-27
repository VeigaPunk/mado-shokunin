# RevC2EntryTruth — dispatcher entry source truth

Axes: coverage + operability.

## Deliverables
- `.ufo/waves/round-51/w2/RevC2EntryTruth/entry-truth.md` — detailed sentence/locator audit with supporting source ranges and concrete caveats.

## Finding
**MISS (source-truth support incomplete).** The detailed audit identifies unsupported/overstated evidence around the claimed bind argument splitter and several scope conclusions. Core mouse prefix handling, submap break ordering, key repeat/long-press callbacks, and socket first-space split are supported by the exact pinned code ranges. The finding concerns content/evidence quality and does not alter or re-score the frozen C2 predicate.

## Verification gap
No LSP device is mounted in this environment (`xd://lsp` returned “No such tool”); source references were checked directly against the pinned source files. No runtime dispatch was performed.