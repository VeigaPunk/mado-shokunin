# ScoutHeld — round-49 w1 report (final)

Seat: `ScoutHeld`. Question answered: what the lane already holds on bind keys and keysyms at base
`03e4ae76aff7a4be59cb69970dd553baa319695a`, so C2 (`hyprland-bind-key-match-r49.md`) does not
re-claim held ground. Full inventory: `.ufo/waves/round-49/w1/ScoutHeld/held.md` (held sentences
with path:line and level, held S-rows with URLs, registry gaps, 13 do-not-restate sentences).

## Method (all at base, read-only `git show`/`git grep`)

`git grep -n -i -e keysym -e resolve_binds_by_sym -e 'code:' -e xkb_keysym -e KeybindManager
-e handleBind` over `corpus/knowledge/`, `SKILL.md`, `corpus/README.md`, `corpus/SOURCES.md` → 15
hits, every one inspected in full context; `xkb_keysym` count = 0. SOURCES.md additionally swept
for all `hyprwm/Hyprland`, `hyprland-wiki`, `xkbcommon`, `xkeyboard-config` URLs (full list in
held.md) to catch rows that never name the grepped symbols.

## Findings

**Held — bind *parsing* is sourced; bind *matching* is not.**

- `handleBind`/`parseKey`/`stringToModMask`/flag-suffix/`unbind`/`addKeybind` retention: held and
  sourced via S162 (`src/config/legacy/ConfigManager.cpp` @ `efb50993`, sha256 `9db68cf4…`) —
  `corpus/knowledge/bind-table-r25.md` (flag table, `code:N`/decimal>9/catchall parseKey rule,
  modmask-zero rejection, multi-bind-per-chord retention; errata `:76-82` marks ten sentences as
  resting on adjacent unquoted lines). `config-option-table-r39.md:40` repeats the registration fact.
- Key-field forms *as declared on this host* (named keysym/XF86/`code:N`/wheel/switch/mouse): held
  at `keybind-rule-semantics.md` §2.3 — but only at `[INF-docs]` level for semantics and `[OBS]`
  for live JSON shape. Its wiki fetches (2026-10-14) were never registered as S-rows.
- Modmask decode (1/4/8/64, order-insensitive) and 192/192 reconcile: held `[OBS]` §2.2/§1.
- `resolve_binds_by_sym` exists as one Limits sentence, `hyprland-input-devices-r46.md:71`
  ("per-device layouts do not change the keymap binds are resolved against unless
  `resolve_binds_by_sym = 1`", anchored to S325 `wiki-Keywords.md:124-130`) — the option name and a
  docs pointer are held; the mechanism is not.
- S319 (`src/devices/IKeyboard.cpp`) is the held keyboard row; S316/S317/S318 cover config→keymap
  names. No row describes the key-press path.

**Open — nothing held on (all C2 claim surface):** `KeybindManager.cpp` press-time matching
(unregistered file); keysym-vs-keycode bind precedence; translated vs untranslated sym and layout
choice under `resolve_binds_by_sym` =0/1; modifier-mask comparison at match time (exact equality,
`i`/ignoreMods, Caps/NumLock); `xkb_keysym_from_name` flags/case handling (the `XKB_KEY_` segment
rule is `[INF-docs]` only); `mouse:`/`switch:`/`catchall` match semantics; libxkbcommon `keysym.c`,
`how-to-type.c`, `state*.c` (unregistered); Hyprland wiki `Binds`/`Variables` pages (unregistered).

## Cautions for the new entry

- C2 may cite S162 for `handleBind`/`parseKey` (same pinned bytes already used at `:1481-1848` even
  though the row's anchor column lists other ranges) and **must** cite S319 rather than re-register
  IKeyboard.cpp; `KeybindManager.cpp` needs a new S-row (registry tops at S351).
- `hyprctl binds -j` receipts stay shape-only (SKILL.md:564,571: keycode ≠ inserted text; no raw
  keycodes/keymap contents).
- All grep paths and line numbers verified at `03e4ae76` on 2026-10-27; no writes outside
  `.ufo/waves/round-49/w1/ScoutHeld*`; no installs; no host state touched.
