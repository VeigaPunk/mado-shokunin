# Seat ScrEntry — C2 entry draft: `corpus/knowledge/hyprland-bind-key-match-r49.md`

Deliverable: the C2 entry, drafted at the seat dir for the L1 to move to `corpus/knowledge/`. Nothing outside
`.ufo/waves/round-49/w1/ScrEntry/` was written; no tracked file, corpus file, registry row, judge or counter was touched.

Entry: `.ufo/waves/round-49/w1/ScrEntry/hyprland-bind-key-match-r49.md` (28353 B, 131 lines).
Title: "From `bind = MODS, KEY, dispatcher, arg` to a key press on Hyprland 0.56.2: which keysym the key field is
compared against, and which modifier mask".

## What the entry claims (behaviour)

17 numbered steps, each carrying at least one `quote`(pin:line) locator:

1. the `bind` handler, flag alphabet, `CVarList` split, `ARGS[1]` as the key field;
2. `parseKey`'s four outcomes - bare number > 9 and `code:N` are keycodes, `catchall`, everything else a verbatim name
   (so `1`..`9` are names, `10`+ are keycodes);
3. the `SKeybind` aggregate keeps key string **and** keycode; empty key without `s` registers nothing; catchall refused
   outside a submap;
4. the name resolves at match time, twice - `XKB_KEYSYM_NO_FLAGS` then `XKB_KEYSYM_CASE_INSENSITIVE`, both compared;
5. `from_name`'s paths: exact-case perfect hash, case-insensitive search preferring the lower-case name, `U<hex>`,
   `0x<hex>`, `XF86_` fallback, else `XKB_KEY_NoSymbol`;
6. the compared keysym is read from `m_xkbSymState` when `resolve_binds_by_sym`, else from the global
   `m_xkbTranslationState`; `internalKeysym` on `m_xkbState` is used only for Escape/DnD and internal binds;
7. the global translation state is built from `input:kb_*` and **never** group- or mod-updated; the per-keyboard sym
   state gets zeros for depressed/latched/locked and only the group;
8. level selection: layout from the state group, type entry by exact mask equality, level-0 fallback - so the compared
   symbol is the level-1 symbol of the group, and Shift/Ctrl/Caps cannot change *which* symbol is compared;
9. `input:resolve_binds_by_sym` picks the group: `0` = layout 0 forever, `1` = the active layout, both at level 1;
10. the mask is parsed by substring `contains`, not tokens; a non-empty field with no bit is a config error;
11. the mask bits are `HL_MODIFIER_*` in libxkbcommon's real modifier order; the comparison is fed `m_lastMods` = the
    merged **depressed** mask, so Caps/Num (locked) never enter it - a `bind = CAPS, ...` parses and never fires;
12. mask comparison is exact `!=`, relaxed only by `i`/`ignore_mods`, submap and shadow;
13. branch order: multi-key, `s` set, `keyName`, keycode, catchall, keysym;
14. keycode numbering is XKB (evdev + 8), matching the wiki's `code:28` = `T`;
15. `mouse:`, `mouse_up/down`, `mouse_left/right`, `switch:` reach the matcher as **string equality** on the key field;
16. config order plus `shadowKeybinds` (which also upper-cases the key name), `global`/`transparent` exempt;
17. every passing bind is dispatched; on release the press-time mask is re-tested.

Also: a "Reading a bind that does not fire" table (8 rows), 13 OBS lines, a pin census, a live-host section and 8
Limits bullets.

## Verification actually run

- `python3 quote-check.py` -> `79 quotes checked, 0 failed`, rc 0 (`.ufo/waves/round-49/w1/ScrEntry/quote-check.txt`).
  For each quote it re-greps the pinned copy with `grep -n`, checks the computed line falls in the claimed
  `a`/`a-b` range, asserts the quote is <= 25 words, and asserts the entry carries the exact form
  `` `quote`(pin:a[-b]) ``. Locators in the entry come from that computation, not from typing.
- Counts: 11 pins under `pins/`, 12 registry rows cited (S352-S363), 2 held rows cited (S318, S319), 2 own-pin files
  eliminated mid-run when ScrRows minted rows for them.
- No build/test/lint exists for a knowledge entry; none was run. No counter was run (not available to a leaf).

## Registry coordination

- ScrRows published the S352-S361 mapping mid-run; I renumbered my draft to it (my first draft had invented a different
  S352.. ordering). Cited as instructed; no new id minted.
- I asked ScrRows for two rows the entry could not do without; they minted **S362** (`libxkbcommon src/state.c`) and
  **S363** (`Hyprland src/devices/IKeyboard.hpp`), both now cited in steps 8 and 11.
- Held `S319` is cited for `src/devices/IKeyboard.cpp` and no row was opened for that URL (clause g). Held `S318` is
  cited for the `input:resolve_binds_by_sym` default at `ConfigValues.cpp:278`.
- S356/S358 were revised by the registry seat mid-run (the keysyms header alone reproduces the canonical names); the
  entry cites S356 only for "the tables are generated from that header", which matches the revision.

## Conflicts and corrections (verbatim, for the canonical judge)

- ExecBindsLive first reported the form line `binds=192 named=184 code=0 mouse=6 switch=2 catch_all=0`, then corrected it:
  "The C2 counter changed its form rule to the semantics (key == "" AND keycode != 0 -> code)" with the new line
  `binds=192 named=142 code=42 mouse=6 switch=2 catch_all=0`. The entry carries the **corrected** line; both are recorded
  here because the first was in flight when I wrote the host section.
- My own shape capture ("`key_named_other 82`", "`key_single_upper_letter 60`") plus the 42 keycode binds give
  142 + 42 + 6 + 2 = 192, i.e. it agrees with the corrected line, not with the earlier `named=184 code=0` one.
- ExecBindsLive's receipt digest: `sha256: 9a47199e2297617f1025d524fc1909a091a950d69261735f39aad1ec3100c779`, 90401 B of
  raw JSON, not embedded in its receipt; a third capture reproduced the same digest.

## Clause conformance (counter interface note from ExecCounterC2)

- f (live capture): the entry cites `.ufo/waves/round-49/receipts/w1-binds-live.txt` and repeats, on their own lines,
  `hyprctl version: Hyprland 0.56.2 built from branch v0.56.2 at commit efb50993780079460b0cbed1363e2166a2de1d9f clean`,
  `binds=192 named=142 code=42 mouse=6 switch=2 catch_all=0`,
  `input:resolve_binds_by_sym int=0 set=false`, and the `sha256:` line above. The receipt itself is ExecBindsLive's file;
  it does not exist at the `receipts/` path yet - see "Integrator actions".
- g (held ground): S319 cited in the body, no row for `src/devices/IKeyboard.cpp` (step 7 and one OBS line).
- h (limits): `## Limits` holds 8 bullets, all scoped; 6 name a specific limitation (level selection for non-base
  types, single-layout host, the unbounded environment read, the unreachable per-layout loop, the dump's missing
  `ignore_mods`/`transparent` fields, the unread Lua front end).
- i (lesson Gate): **not done and not mine** - `corpus/lessons/round-49.md` `## Gate` needs `- **S### admit**` for
  S352-S363 (and the C1 rows). The entry body is clean of `corpus/`-pointed quote locators.

## Integrator actions required (L1)

1. Land the 11 pinned copies from `.ufo/waves/round-49/w1/ScrEntry/pins/` into `.ufo/waves/round-49/fetch/` with the
   same names (`Hyprland-KeybindManager.cpp`, `Hyprland-legacy-ConfigManager.cpp`, `Hyprland-InputManager.cpp`,
   `Hyprland-IKeyboard.cpp`, `Hyprland-IKeyboard.hpp`, `Hyprland-ConfigValues.cpp`, `xkbcommon-keysym.c`,
   `xkbcommon-state.c`, `xkbcommon-ks_tables.h`, `wiki-Binds.md`, `wiki-Variables.md`). The counter resolves quote
   locators against `fetch/`; byte-identical copies are in `pins/` and their URL/bytes/sha256 are in
   `pins/MANIFEST.tsv`. I did not write `fetch/` (outside seat scope).
2. Copy ExecBindsLive's `.ufo/waves/round-49/w1/ExecBindsLive/receipts/binds-receipt.txt` (1302 B) to
   `.ufo/waves/round-49/receipts/w1-binds-live.txt`, unchanged bytes.
3. Append rows S352-S363 (including S362/S363) to `corpus/SOURCES.md` from `ScrRows/rows.md`, and add the lesson Gate
   admits.
4. Move the entry to `corpus/knowledge/hyprland-bind-key-match-r49.md` and reconcile its head against the final row text.

## Touched surfaces

- Created (seat dir only): `hyprland-bind-key-match-r49.md`, `quote-check.py`, `quote-check.txt`,
  `hyprctl-binds-shape.txt`, `hyprctl-getoption-rbs.txt`, `hyprctl-version.txt`, `pins/` (11 pins + `MANIFEST.tsv`),
  and this report.
- Read-only host reads: `hyprctl version`, `hyprctl binds -j`, `hyprctl getoption input:resolve_binds_by_sym -j` with
  `HOME`/`XDG_CONFIG_HOME` under scratch and `XDG_RUNTIME_DIR`/`HYPRLAND_INSTANCE_SIGNATURE` the minimum needed to reach
  the running compositor. The instance signature is session material and appears in no file.
- No `pacman`, no install, no compositor mutation, no input injection, no GUI. Scratch
  `/fast/scratch/hyaku/mado-r49/ScrEntry` removed (`rm -rf`).
- Session material: the shape receipt carries counts and the modmask histogram only - no dispatcher args, no
  descriptions, no window titles, no device names.

## Out of scope here

- C1 (`tools/mado-keysym.py`) and its fixtures; S357/S358 are C1's rows and are not cited.
- The counters, the frozen predicates, the w2 attacks.
- Any edit to the registry, the lesson file, the corpus index or the entry's final location.
- Running the host's keymap through `how-to-type` (C1's evidence; the entry cites counts, not a compiled keymap).

## Artifact paths

- `.ufo/waves/round-49/w1/ScrEntry/hyprland-bind-key-match-r49.md` - the entry draft
- `.ufo/waves/round-49/w1/ScrEntry/quote-check.txt` - 79/79 quote verification
- `.ufo/waves/round-49/w1/ScrEntry/quote-check.py` - the verifier
- `.ufo/waves/round-49/w1/ScrEntry/pins/MANIFEST.tsv` - 11 pins, URL + bytes + sha256
- `.ufo/waves/round-49/w1/ScrEntry/hyprctl-binds-shape.txt` - own shape capture, 192 binds
- `.ufo/waves/round-49/w1/ScrEntry/hyprctl-getoption-rbs.txt`, `hyprctl-version.txt` - own read-only captures
- `.ufo/waves/round-49/w1/ScrEntry.md` - this report
