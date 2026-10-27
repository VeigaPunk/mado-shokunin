# ScrSkill — round-49 w1 — SKILL.md section draft: binds, keysyms and the keymap

Seat: scribe (leaf; no subagent dispatch). Base `03e4ae76aff7a4be59cb69970dd553baa319695a`, nothing frozen.
Report path: `.ufo/waves/round-49/w1/ScrSkill.md`. Deliverable:
`.ufo/waves/round-49/w1/ScrSkill/skill-section.md` — a draft SKILL.md section with the round-48 shape (intro, usage
block, decision table, error-pattern table, notes), every row carrying a pinned-source locator or a live receipt.

## 1. What I did

- Read the declared claims (`.ufo/waves/round-49/claims.md`), the round-48 outside check
  (`corpus/lessons/round-48-verifier-spotcheck.md`) and the two round-48 SKILL sections that set the shape
  (`SKILL.md:2226-2293` "XKB keymap compile", `:2294-2360` "Terminal cache").
- Pinned and read the C2 sources at the host's own commits, sha256 in `pins/PINS.txt`:
  Hyprland `efb50993780079460b0cbed1363e2166a2de1d9f` (`src/managers/KeybindManager.cpp`,
  `src/config/legacy/ConfigManager.cpp`, `src/config/values/ConfigValues.cpp`, `src/managers/input/InputManager.cpp`,
  `src/devices/IKeyboard.cpp`, `src/devices/IKeyboard.hpp`, `src/config/ConfigManager.cpp`) and libxkbcommon
  `xkbcommon-1.13.2` (`src/keysym.c`, `tools/how-to-type.c`); wiki pinned at the hyprlang-era commit
  `78e64e80f4e84634744cd49728a198a7ebaf579a` (`content/Configuring/Binds.md`, `…/Variables.md`) plus the lua-successor
  `e99eac80…` for the era boundary.
- Took read-only live receipts: `hyprctl version` (Hyprland 0.56.2 at `efb50993…`),
  `hyprctl getoption input:resolve_binds_by_sym -j` (`{"int": 0, "set": false}`), `hyprctl getoption
  device:resolve_binds_by_sym -j` (`no such option`), `hyprctl binds -j` (192 binds, tallied).
- Compiled the host keymap in a clean environment (`env -i PATH=/usr/bin HOME=scratch XDG_CONFIG_HOME=scratch`) and ran the
  pinned how-to-type judge on it for `slash`, `0x2f`, `Return`, `nosuchsym`, `0x100`, `47`, `U002F`, `XKB_KEY_a`,
  `U+002F`, `0X2F`, `dead_acute` (with and without `--disable-compose`), `Caps_Lock`, `Num_Lock`, `Multi_key`.
- Computed every locator with `grep -nF` against the pins (`receipts/locators.txt`), then re-verified that every
  `file:line` cited in the draft resolves to the line the sentence claims (a scripted pass over the draft; all resolve,
  only `SKILL.md:2226` is a lane locator by design).

I ran no counter, gate, selftest or mutant, and I did not execute another runtime. Nothing was committed (the L1 is the
only integrator); no tracked file was edited.

## 2. Deliverable — what the section decides

The section answers the C2 question ("which physical key and which modifiers fire a bind on keysym X") as a decision
list, in the order the three resolvers run, each grounded in source:

1. **Level** — the bind-side keysym is read from a state created with no modifiers (`KeybindManager.cpp:332`) that is
   never given one (the file's only reads are `:280`, `:369`), so only modifier-free positions are addressable; the wiki
   states the same rule and the AZERTY example (`wiki-Binds-legacy.md:80`, `:91`).
2. **Layout** — the bind keymap is built from `input:kb_file` else the five `input:kb_*` names
   (`KeybindManager.cpp:296-314`); `resolve_binds_by_sym` defaults to 0 (`legacy-ConfigManager.cpp:533`,
   `ConfigValues.cpp:278`, live `int 0 set false`), so the first layout is used whatever the active group is
   (`wiki-Variables-legacy.md:181`); with it on, the sym comes from the device keymap's active group, still
   modifier-free (`KeybindManager.cpp:369`, `IKeyboard.cpp:218`, `:382`).
3. **Key form** — a bare number > 9 and `code:N` are keycodes compared as `e.keycode + 8`
   (`legacy-ConfigManager.cpp:1482-1485`, `KeybindManager.cpp:696-698`, `:367`); `mouse:`, `mouse_*`, `switch:`,
   `catchall` go through the `keyName` branch (`:693-700`).
4. **Mask** — exact equality against a substring-parsed uppercase mod string (`:652`, `:221-240`); the pressed mask is
   depressed-or-latched real mods merged over all keyboards (`IKeyboard.cpp:359-370`, `InputManager.cpp:1711`,
   `:1915-1931`), so locked Caps/Num never contribute.
5. **Name resolution** — `xkb_keysym_from_name` exact then case-insensitive, either value matching
   (`KeybindManager.cpp:710-711`, `:724`; `keysym.c:242`, `:268`).

Usage block (the C1 deliverable's lines, the judge line, the keymap producer line, host samples and the accepted/
rejected ARG forms) is in the draft; the contract text (stdlib only, refuses exit 2 without `--disable-compose` and
`--keysym`) is stated with the judge behaviour that motivates each refusal.

## 3. Findings for the L1 / C2 entry (each names what it attacks)

- **F1 — bind-side keymap is the config's, not the device's.** `CKeybindManager::updateXKBTranslationState` reads
  `input:kb_file` / `input:kb_rules|model|layout|variant|options` only (`KeybindManager.cpp:296-306`); per-device
  layouts are applied to the device keymap with an `input:` fallback (`InputManager.cpp:1224-1241`). Attacks the round-46
  entry's Limits (`corpus/knowledge/hyprland-input-devices-r46.md:71`, "bind resolution outside the join"): with a
  single device on `input:kb_layout` the two coincide, with per-device layouts they do not.
- **F2 — the compared level is modifier-free.** Source (`:332`, `:369`, no `xkb_state_update_mask` on that state — full
  grep in `receipts/locators.txt`) and wiki (`:80`) agree. This is the mechanism behind "a bind on `SLASH` fires on the
  key whose unshifted sym is `slash`", and it makes shifted symbols unbindable.
- **F3 — an option can move a key's sym (measured).** `compose:caps` (`~/.config/hypr/input.conf:11`) makes `<CAPS>` carry
  `Multi_key` at both levels (`receipts/host-br.xkb:1581-1584`); `--keysym Caps_Lock` returns rc 0 with zero rows, while
  `--keysym Multi_key` returns keycode 66 levels 1-2 (`receipts/keysym-how-to-type-sample.txt`). Attacks any reading of
  a bind name from the keycap label.
- **F4 — the option is a per-device value with an `input:` fallback, and `hyprctl getoption` reaches only the global
  name.** `device:resolve_binds_by_sym` is registered as a device special value (`legacy-ConfigManager.cpp:533`) and read
  with fallback (`InputManager.cpp:1224`), but `hyprctl getoption device:resolve_binds_by_sym -j` answers
  `no such option` while `input:resolve_binds_by_sym` answers `{"int": 0, "set": false}`
  (`receipts/hyprctl-version-options.txt`). C1/C2 counters that read the option must read the `input:` name.
- **F5 — host bind census (read-only).** 192 binds: 142 keysym names, 42 empty `key` + non-zero `keycode` (keycode binds),
  2 `mouse:N`, 4 `mouse_*`, 2 `switch:`; `submap` empty for all 192; `catch_all` true for none; `modmask` top values 64
  (SUPER) 42×, 65 (SUPER|SHIFT) 37×, 68 (SUPER|CTRL) 26×, 0 23× (`receipts/binds-summary.txt`). `hyprctl binds -j`
  prints `key: ""` for keycode binds — a shape the C2 entry should state.
- **F6 — how-to-type ARG grammar (measured, for the C1 counter's fixture generator).** With `--keysym`:
  `slash`, `0x2f`, `U002F`, `47` all print `keysym: slash (0x002f)`; `XKB_KEY_a`, `U+002F`, `0X2F` exit 2; `0x100`
  prints the *name* as `0x00000100` (a keysym with no canonical name); decimal without `--keysym` is a code point
  (`0x100` → `Amacron (0x03c0)`). A judge-equality tool must accept exactly this set and print the name that
  `xkb_keysym_get_name` returns, not the header spelling.
- **F7 — the bind keymap is rebuilt on device refresh, so it is not stale after a reload.**
  `CInputManager::setKeyboardLayout` calls `updateXKBTranslationState` (`InputManager.cpp:1206-1211`) and
  `input:kb_*` carry `{.refresh = REFRESH_INPUT_DEVICES}` (`ConfigValues.cpp:271-278`). Rules out a "stale translation
  state after reload" hypothesis before someone spends a counter on it.

No conflicts between sources were found; nothing needed escalating to the canonical judge.

## 4. Gates / counters

None run and none claimed. This seat measured with read-only commands only: `hyprctl version|binds|getoption`,
`xkbcli compile-keymap|how-to-type` (stdout only, clean env), file reads, and `sha256sum`. I did not run
`--selftest`, any `quality/` gate, any frozen counter, or a mutant, and I did not verify the C1 tool (it does not exist
yet — `tools/mado-keysym.py` was absent at 2026-10-27 01:36 -03, `ls` exit 2; the usage lines in the draft are the
declared contract, not observed behaviour of a landed file).

## 5. Touched surfaces

- `.ufo/waves/round-49/w1/ScrSkill.md` (this report).
- `.ufo/waves/round-49/w1/ScrSkill/skill-section.md` (the draft).
- `.ufo/waves/round-49/w1/ScrSkill/pins/` — 12 pinned sources + `PINS.txt` (sha256, bytes, tag/commit URL).
- `.ufo/waves/round-49/w1/ScrSkill/receipts/` — `keysym-how-to-type-sample.txt`, `host-br.xkb` (73,079 B, sha256
  `efd487a3…`, reproduces the round-48 digest for the same RMLVO), `binds-raw.json`, `binds-summary.txt`,
  `hyprctl-version-options.txt`, `locators.txt`.
- Nothing else in the lane or the fleet was written; no `git`/`jj` mutation; no host config, cache or home state was
  written (the compile ran with `HOME`/`XDG_CONFIG_HOME` in scratch; how-to-type only reads).

Tool installs: none. Scratch `/fast/scratch/hyaku/mado-r49/ScrSkill` removed at the end.

## 6. Out of scope (not touched)

C1's tool implementation and its counter/fixtures (peers); the C2 entry text and registry rows S352.. (peers/L1); the
frozen predicates, counters and controls; the routed round-48 closure items N1-N5, M48-8/10/13; `corpus/` edits;
`README.md`/`SOURCES.md` rows; the Lua config manager's bind path (stated as a Limit in the draft).

## 7. For the L1 when integrating

- The section is written for `SKILL.md` append-only; it cites the round-48 section as `SKILL.md:2226-2293` and the host
  config as `~/.config/hypr/input.conf:10-11` (already used by the round-48 section), so an append after
  `SKILL.md:2360` keeps those locators true.
- Citations of the form `KeybindManager.cpp:652` refer to
  `https://raw.githubusercontent.com/hyprwm/Hyprland/efb50993780079460b0cbed1363e2166a2de1d9f/src/managers/KeybindManager.cpp`;
  the pinned copies and their URLs are in `pins/PINS.txt`, so the registry rows can be opened from them.
- `wiki-Binds-legacy.md` is the wiki `content/Configuring/Binds.md` at `78e64e80…`; the lua successor is pinned
  separately, so the era boundary is checkable if a future round reuses the same page.
- If the C1 tool lands with a different refusal set or ARG grammar than the contract, the usage block is the one place to
  update (F6 lists the measured judge grammar it must match).
