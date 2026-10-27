# S352–S363 row quote verification

Draft `w1/ScrRowsDispatch/rows.md` was absent at inspection, so fallback rows S352–S363 in `corpus/SOURCES.md` were examined against round-50 pins. Independent source-line grep was not completed for the twelve lengthy paraphrase fields; therefore these are NOT represented as VERIFIED. Registry evidence confirms each row's cited pin exists in `SHA256SUMS` (S352 pin not listed in visible subset; S353–S363 pins listed, with S352 outside requested S352-S363 scope only if absent row). URLs inspected in S353-S360 and S362-S363 use raw.githubusercontent.com with immutable commit/tag path components; S359/S360 commit d5f07c60...; S361 is a local receipt, no URL.

| Row | Result | Evidence / note |
|---|---|---|
| S352 | UNVERIFIED | Exact row not present in inspected excerpt; requires line-level inspection. |
| S353 | UNVERIFIED | `.ufo/waves/round-50/fetch/Hyprland-legacy-ConfigManager.cpp`; immutable commit efb509...; quote not independently verified. |
| S354 | UNVERIFIED | `.../Hyprland-InputManager.cpp`; immutable commit efb509...; quote not independently verified. |
| S355 | UNVERIFIED | `.../xkbcommon-keysym.c` and `.h`; version path xkbcommon-1.13.2; quote not independently verified. |
| S356 | UNVERIFIED | `.../xkbcommon-ks_tables.h`; version path xkbcommon-1.13.2; quote not independently verified. |
| S357 | UNVERIFIED | `.../xkbcommon-tools-how-to-type.c`; version path xkbcommon-1.13.2; quote not independently verified. |
| S358 | UNVERIFIED | `.../xkbcommon-keysyms.h`; version path xkbcommon-1.13.2; quote not independently verified. |
| S359 | UNVERIFIED | `.../wiki-Binds.md`; immutable commit d5f07c60...; quote not independently verified. |
| S360 | UNVERIFIED | `.../wiki-Variables.md`; immutable commit d5f07c60...; quote not independently verified. |
| S361 | UNVERIFIED | Local receipt pin `binds-live-r50.txt`; not a URL. Quote not independently verified. |
| S362 | UNVERIFIED | `.../xkbcommon-state.c`; version path xkbcommon-1.13.2; quote not independently verified. |
| S363 | UNVERIFIED | `.../Hyprland-IKeyboard.hpp`; immutable commit efb509...; quote not independently verified. |

Word counts: not asserted because independent line-quote verification was not performed. This is a verification gap, not a claim of drift.