# ExecHyprSrc — C2 source trace: Hyprland 0.56.2 bind key → match (w1, round 49)

status: complete. All work is new files under my seat dir; nothing existing was edited, nothing outside the lane was written.
assignment: pin and trace Hyprland 0.56.2's bind-key path in source, with computed locators, for the C2 entry
`corpus/knowledge/hyprland-bind-key-match-r49.md` (L1 integrates).
landing: 31 new files in `.ufo/waves/round-49/w1/ExecHyprSrc/` — `trace.md` (deliverable), `fetch/` (13 source pins + the commit listing, plus `SHA256SUMS` and `URLS`),
`receipts/` (8 receipts), `probes/` (2 C probes), `locate.py`, `verify-quotes.py`, `check-trace.py`, `locators.json`.
scratch: `/fast/scratch/hyaku/mado-r49/ExecHyprSrc`, removed at the end of the run; no receipt cites a scratch path as evidence.
tool installs: none (gcc, pkg-config, libxkbcommon 1.13.2, hyprctl and xkbcli were already present). No pacman.

## What the trace establishes (the C2 answers)

1. **Parsing** — `bind` is a hyprlang keyword handled by `handleBind` (`Hyprland-ConfigManager.cpp:607`, `:315`, `:1492`). Field 1 is turned into an
   8-bit `HL_MODIFIER_*` mask at load time. Field 2 goes through `parseKey`: bare number > 9 → keycode, `code:N` → keycode, `catchall` →
   catchall (submaps only), **everything else stored as a raw string** and resolved per key event. Nothing becomes a keysym at load time
   (except the multi-key `A&B` form).
2. **Which keysym of the press is compared** — one line:
   `xkb_state_key_get_one_sym(pKeyboard->m_resolveBindsBySym ? pKeyboard->m_xkbSymState : m_xkbTranslationState, KEYCODE)`
   (`Hyprland-KeybindManager.cpp:369`). Both candidate states carry **zero modifiers**:
   the per-device `m_xkbSymState` is updated with `xkb_state_update_mask(m_xkbSymState, 0, 0, 0, 0, 0, group)` (`IKeyboard.cpp:382`, `:422`),
   and the global `m_xkbTranslationState` is never updated at all — `grep -c xkb_state_update_mask KeybindManager.cpp` = 0, against
   3 in `IKeyboard.cpp`. So the compared keysym is **level 1**:
   - `resolve_binds_by_sym = 0` (host: `int 0`, `set false`) → level 1 of **layout 0 of the global `input:kb_*` keymap**, whatever the device
     or active layout;
   - `resolve_binds_by_sym = 1` → level 1 of the **active layout** of that device.
   The fully modifier-aware keysym (`m_xkbState`) exists but is used only for internal keybinds, never for `bind` matching (`:370`, `:377`).
   Consequence: Shift/AltGr/Caps never change which keysym a bind sees; a keysym that only exists at level ≥ 2 cannot be reached by a keysym bind.
3. **Modifier comparison** — exact equality of the whole mask (`:652`), disabled by flag `i`. The mask is built from **depressed|latched only**
   (`IKeyboard.cpp:360`), so **Caps Lock and Num Lock never appear** in it. Config names are upper-cased and substring-matched, so
   `super`/`win`/`logo`/`mod4`/`meta` all set META and stray text around a known name is ignored.
4. **Key forms** — `code:N` compares the xkb keycode, i.e. the same number `how-to-type` prints in its `KEYCODE` column (verified:
   `SLASH → AB11(97)`, and `hyprctl binds` carries keycode values 10..201); `mouse:NN`, `mouse_up/down/left/right` and `switch:on/off:…` match by
   **exact string** (case-sensitive, name branch `:694`), never as keysyms; `catchall` is a submap-only fallback.
5. **Case** — match time tries `xkb_keysym_from_name(name, XKB_KEYSYM_NO_FLAGS)` then `…CASE_INSENSITIVE` (`:710`, `:711`), and libxkbcommon's
   case-insensitive lookup prefers the **lower-case** name (`src/keysym.c:268`; executed: `Q` → `q`). So `bind = SUPER, Q` fires on the
   unshifted `q` press, and names that exist only in one case (`SLASH`, `RETURN`, `BACKSPACE`, `COMMA`, … — 14 of the host's 60) resolve only
   through the icase step. **`xkbcli how-to-type --keysym SLASH` rejects those names with rc 2** — a C1 contract that accepts bind-style
   uppercase names would be wider than the judge.
6. **Keycode vs keysym binds coexist** — each bind has exactly one form and every bind that passes is dispatched (`:781`); `shadowed` only
   suppresses *other* keys held at the same time. A `code:24` bind and a `SLASH` bind both fire.
7. **Host consequence** (executed on the host keymap `br` + `compose:caps`, sha256 `efd487a3…`): a zero-mod state reads `q` on AD01 and
   `slash` on AB11; AltGr+Q produces `slash` only in a state with Mod5|LevelThree. So `bind = SUPER, SLASH` fires from **AB11 only**, and
   AD01's AltGr slash is unreachable for a keysym bind. Of 60 distinct bind key names, 58 resolve to a level-1 keycode; the 2 that do not are
   the scroll pseudo-keys, covering 4 of the 146 keysym-class rows.

## Evidence (all in the seat dir; every number below was produced by a command)

| evidence | file | observed |
|---|---|---|
| pins | `fetch/SHA256SUMS`, `fetch/URLS` | 14 entries; `sha256sum -c` → 14 OK |
| locators computed, never typed | `locate.py` → `locators.json` | `LOCATED 78/78` (`receipts/locate.txt`) |
| quotes re-checked by line number | `verify-quotes.py` | `QUOTES_VERIFIED 78/78` (`receipts/verify-quotes.txt`) |
| trace table numbers == computed locators | `check-trace.py` | `TRACE_ROWS_CHECKED 78/78` |
| Hyprland identity | `receipts/live-version-option.txt` | `branch v0.56.2`, `commit efb50993780079460b0cbed1363e2166a2de1d9f`, `dirty false` |
| option | same | `{"option": "input:resolve_binds_by_sym", "int": 0, "set": false }` |
| host RMLVO | `receipts/live-rmlvo.txt` | layout `br`, variant `""`, options `compose:caps`, model `""`, rules `""` |
| bind census (shape only) | `receipts/live-binds-shape.txt` | 192 binds: 146 keysym, 42 keycode-only, 2 mouse, 2 switch; mask histogram starting `0x40`×42, `0x41`×37, `0x44`×26, `0x0`×23 |
| judge + libxkbcommon probes | `receipts/keysym-probes.txt` | `slash` → AD01 levels 3/4 with `[ Mod5 LevelThree ]` + AB11 level 1 `[ ]`; `q` → AD01 level 1; `Q` → AD01 level 2; `SLASH`/`RETURN` → `ERROR: Failed to convert argument to keysym`, rc 2; zero-mod vs Mod5|LevelThree state on the same keycodes |
| names → keycodes | `receipts/bind-key-resolution.txt` | full 60-name table; `SLASH → AB11(97)`, `RETURN → RTRN(36)`, 14 names need icase, 2 names resolve to nothing |
| state updates | `receipts/translation-state.txt` | `xkb_state_update_mask` count 0 in `KeybindManager.cpp`, 3 in `IKeyboard.cpp`; `xkb_state_new` 1 |

Probes are committed as sources: `probes/probe-state.c` (name flags + zero-mod vs AltGr state) and `probes/probe-bindkey.c`
(every bind key name → keycodes at level 1). Both build with
`gcc -O0 -o probe probes/probe-state.c $(pkg-config --cflags --libs xkbcommon)`.

## Deviations from the seat spec (both recorded, neither hides a gap)

1. **`src/config/ConfigDescriptions.hpp` does not exist at `efb50993`** — the fetch returns HTTP 404. The option registry, with the
   `input:resolve_binds_by_sym` one-line description, is `src/config/values/ConfigValues.cpp:278`. Pinned and cited there.
   Any C2 registration that lists `ConfigDescriptions.hpp` must not.
2. **`src/devices/IKeyboard.cpp` was not re-registered.** It is held as row S319; my copy (`fetch/Hyprland-IKeyboard.cpp`) is byte-equal to
   S319's pin `8a800efe9baa7f375a3781744372eecd98a88be2c4bedaae96c90a1102a1aa3d` (verified) and carries new locators (`:360`, `:382`, `:422`)
   that S319's `teaches` does not cover. C2 should cite S319 for the file and add the new locators in the entry, not a new row.

Pins the L1 can register as S352+ (13; full sha256/URL in `fetch/URLS`): ConfigManager.cpp `9db68cf4…`, KeybindManager.cpp `8d8f35fc…`,
KeybindManager.hpp `cee22c13…`, InputManager.cpp `feedf32e…`, Keyboard.cpp `276e4f15…`, IKeyboard.hpp `82e0bc9e…`, ConfigValues.cpp
`a76f0507…`, HyprCtl.cpp `798b7c6c…`, LuaKeybind.cpp `2e8bad56…`, keysym.c `123e3390…`, xkbcommon.h `17e58db5…`, how-to-type.c
`f774882e…`, plus the commit tree listing `fdb0b7a4…` (API, not a source).

## Risks / what is not proven

- Nothing ran against a live Hyprland: no dispatch, no reload, no mutation, no input injection. The parse and match halves are source reads;
  only the libxkbcommon half is executed.
- "Level 1 only" rests on the source (zeros in `update_mask`, no update at all on the translation state) plus an executed zero-mod state
  probe — not on instrumenting Hyprland's own state objects.
- Lua `hl.bind` key-field parsing is untraced (files not pinned); matching is shared, so §5-§7 of `trace.md` apply.
- `switch:`/`mouse:` string matching (case/space sensitivity) is read from source, not tested against a device.
- Re-applying `input:kb_file` (a keymap file instead of RMLVO names) was not exercised; `input:kb_file` was not queried on the host, so
  "empty on this host" is an assumption.
- The raw `hyprctl binds -j` capture is **not** committed (dispatcher args are local config material); only the shape/histogram is.
  No device names, window titles or home paths were written anywhere in the seat dir.
- C1 interaction to carry into the freeze: the pinned judge rejects uppercase/alias key names that Hyprland accepts, and prints the xkb
  keycode that `code:N` stores — both are contract-relevant and both are receipted here.
