# Round 53 lesson — repairing proposition grounding (2026-10-27)

Base: `ad4bf2059bcfafe63671d262222908ee1fe8001c`. Round-52 closure spot-check is `corpus/lessons/round-52-verifier-spotcheck.md`; round 53 corrects source-truth records without rewriting that closure artifact.

## Gate

### Round-52 SOURCES row grounding, reopened 2026-10-27

- S370 — URL `https://raw.githubusercontent.com/hyprwm/Hyprland/efb50993780079460b0cbed1363e2166a2de1d9f/src/config/legacy/DispatcherTranslator.cpp`; opened from the lane's committed pin `.ufo/waves/round-52/fetch/Hyprland-legacy-DispatcherTranslator.cpp`, 2026-10-27. Quote at lines 591–594: “CVarList2 ARGS(args, 4); if (ARGS.size() != 4)” (7 whitespace-delimited words); grounds argument-count parsing, not event delivery.
- S371 — URL `https://raw.githubusercontent.com/hyprwm/Hyprland/efb50993780079460b0cbed1363e2166a2de1d9f/src/config/shared/actions/ConfigActions.cpp`; opened from `.ufo/waves/round-52/fetch/Hyprland-ConfigActions.cpp`, 2026-10-27. Quote at lines 1554–1558: “sendKeyboardMods(modMask, 0, 0, 0);” (1 whitespace-delimited word); grounds the modifier-call site, not host delivery.
- S372 — URL `https://raw.githubusercontent.com/hyprwm/Hyprland/efb50993780079460b0cbed1363e2166a2de1d9f/src/config/shared/actions/ConfigActions.hpp`; opened from `.ufo/waves/round-52/fetch/Hyprland-ConfigActions.hpp`, 2026-10-27. Quote at line 117: “timestamp of last key/mouse event” (6 words); grounds the field comment only.
- S373 — URL `https://raw.githubusercontent.com/hyprwm/Hyprland/efb50993780079460b0cbed1363e2166a2de1d9f/src/managers/KeybindManager.cpp`; opened from `.ufo/waves/round-52/fetch/Hyprland-KeybindManager.cpp`, 2026-10-27. Quote at lines 221–225: “std::ranges::transform(mods, mods.begin(), ::toupper);” (1 whitespace-delimited word); grounds uppercasing in modifier parsing.
- S374 — URL is the lane artifact `corpus/lessons/round-52-verifier-spotcheck.md`; reopened 2026-10-27. Quote at §2, line 38: “P16 fails — the space-joined quote” (6 words); grounds the routed finding that P16's cited quote was not contiguous in the source, not a new Hyprland behavior claim.

QUALITY 17 distinct-scope review (round-52 verifier routed): S370≡S365 retained as distinct scopes (synthetic key-route parsing vs dispatcher-name resolution); S371≡S367 retained as distinct scopes (seat keyboard delivery vs submap state); S373≡S364 retained as distinct scopes (modifier-name parsing vs bind dispatch lookup). Shared census W04 is a warning only and is not this review. Evidence: reopened source pins above and row scopes in `corpus/SOURCES.md`.

### Admission and non-author sample

Round-52 candidate claims remain unadmitted unless round-53 frozen counter receipts and source-truth review resolve them. Lane-dispatched seats are not non-author reviewers. Outside sample: pending closure reviewer.

## Mistakes

- **M53-1 — `corpus Gate omission`** · evidence: round-52 verifier spot-check §5 item 1; `corpus/lessons/round-52.md` had no per-row URL/date/quote records for S370–S373 · captured-by: CORPUS.md SOURCES rule 1 · fix: make the new round lesson carry four row-level Gate records, each URL, access date, located quote and bounded grounding. Shown able to fail: `grep -cE '^- S37[0-3] — URL' corpus/lessons/round-52.md` → 0 (FAIL; required 4); same command on this lesson → 4 (PASS). This is a regression count, not proof of a general gate.
- **M53-2 — `stale status prose`** · evidence: round-52 verifier spot-check §5 item 2; round-52 Changes said “Pending final integration revisions and receipts” after its changes landed · captured-by: no explicit stale-status check named in the lesson · fix: correction belongs in this round's new lesson, never rewrite round-52 history. Shown able to fail: closure compared the statement with landed commit `56d6e705bf9113dce0dabd5d4a7ed8e610e1a940` and found the statement false.
- **M53-3 — `source proposition drift`** · evidence: round-52 verifier spot-check §2 C2, P16–P18 (opened this round and registered as S374) · captured-by: QUALITY 104 requires sentence-to-pin scope auditing, but did not catch the three specific errors before entry landed · fix: retain the exact corrected source statements in a new entry and require independent proposition-level verification before admission. Shown able to fail: P16's spliced quote, P17's misattribution and P18's false localization were reproduced against the pinned bytes in `.ufo/waves/round-53/w1/R53Five41.md:81-91` and the external spot-check §2.
- **M53-4 — `pre-data control freeze omitted`** · evidence: `.ufo/waves/round-53/w1/R53Five41.md:52` measured no round-53 registration, fixture manifest or counter at base; wave 1 had already launched · captured-by: claims-frozen.md:13 expressly required control design and measurement frozen before data · fix: stop both claims honestly, do not mutate predicates after seat scoring, and carry the need for an immutable registration/control manifest into round 54. Shown able to fail: `test -f .ufo/waves/round-53/registration.md` returns 1; the missing file is also confirmed in R53Five41.

## Changes

W1 settled 64/64 (all reports; zero dead seats; `.ufo/waves/round-53/w1-results.json`). No `registration.md`, frozen control manifest, or r53 counter was present before dispatch; no r53 counter or source-truth review landed afterward. C1 and C2 are **unprovable / honest stop**. The append-only correction note supersedes P16–P18 in the README index, but remains unadmitted pending non-author review. No claim predicate was revised after seat scoring.

## Considerthese

Mined proposal 3 from `considerthese/2026-10-26.md` (opened 2026-10-27): keep a routed-defect ledger so old defects remain visible. This round records the four closure-routed defects in this lesson, including row-scoped source reopenings and the QUALITY 17 scope verdict; it does not claim a general age-tracking ledger was implemented.

## SOURCES changes

- S370 `used-by`: `corpus/knowledge/hyprland-synthetic-dispatch-r52.md` → that path plus `corpus/knowledge/hyprland-synthetic-dispatch-r52-errata-r53.md`.
- S371 `used-by`: `corpus/knowledge/hyprland-synthetic-dispatch-r52.md` → that path plus `corpus/knowledge/hyprland-synthetic-dispatch-r52-errata-r53.md`.
- S374 `used-by`: `corpus/lessons/round-53.md` → that path plus `corpus/knowledge/hyprland-synthetic-dispatch-r52-errata-r53.md`.
