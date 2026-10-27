# ScoutHeld — what the lane already holds on bind keys and keysyms

Base `03e4ae76aff7a4be59cb69970dd553baa319695a`; grep at that tree of `corpus/knowledge/`, `SKILL.md`,
`corpus/README.md`, `corpus/SOURCES.md` for `keysym`, `resolve_binds_by_sym`, `code:`, `xkb_keysym`,
`KeybindManager`, `handleBind` (15 hits, all inspected in context; `xkb_keysym` count = 0).
`corpus/lessons/` was out of the scoped grep and is untouched by this inventory.

## Held sentences (path:line, claim level)

### `corpus/knowledge/keybind-rule-semantics.md` (MADO-R2-2, probed 2026-10-14; tags are its own legend)

- `:106` Named-keysym row: the bind key field can be a named keysym such as `RETURN`, `F`, `SLASH`,
  `PERIOD`, `COMMA`, `BACKSPACE`, `TAB`, `ESCAPE`, `DELETE`, `PRINT`, `F9`, arrows, `SPACE` —
  **`[INF-docs]`** "use the segment after `XKB_KEY_`". No source row underlies it (see "Registry gaps").
- `:107` XF86 media/switch names (`XF86Audio*`, `XF86MonBrightness*`, `XF86PowerOff`,
  `XF86Calculator`) — same `[INF-docs]` table row family.
- `:108` Keycode form `code:N` (declared `code:10..21`, `code:61`, `code:201`) — **`[OBS]`** on live
  JSON shape only: `key:""`, `keycode:N`.
- `:109` Wheel forms `mouse_up`/`mouse_down` — `[INF-docs]` semantics, `[OBS]` `scroll_event_delay=300`.
- `:110` Switch forms `switch:on:`/`switch:off:` `Lid Switch` — `[INF-docs]`.
- `:111` Mouse button `mouse:272`/`mouse:273` — `[OBS]` live dispatcher reported as `mouse`.
- `:61` "`unbind` key matching is case-sensitive" — `[INF-docs]`.
- §2.1 `:65-71` Modifier grammar — `bind = MODS, key, dispatcher, params`; `bindd` puts description
  before dispatcher; mouse binds take one fewer arg; empty MODS legal; "any separators are allowed
  except `,`"; mod order not significant; mod list `SHIFT CAPS CTRL/CONTROL ALT MOD2 MOD3
  SUPER/WIN/LOGO/MOD4 MOD5` (0.54 archive only) — all `[INF-docs]`.
- §2.2 `:73-88` Measured modmask decode — 13 live masks; bit values 1=SHIFT, 4=CTRL, 8=ALT,
  64=SUPER **`[OBS]`** (matched against `hyprctl binds -j`, 0 mismatches); CAPS/MOD2/MOD3/MOD5 bit
  positions **`[UNK]`**; order-insensitivity measured (`SUPER SHIFT ALT` = `SUPER ALT SHIFT` = 73).
- `:122` Flag table lists `i` = ignore-mods among declared-but-unused flags (live count 0) —
  `[INF-docs]` meaning, `[OBS]` count. What `i` *does* at match time is **not** held anywhere.
- `:129` No keysym-combo (`s`), submap, catch-all or per-device binds in the plane — `[OBS]`
  (`submap:""` ×192, `catch_all:0`).
- §1 `:36-58` All 192 binds reconcile 192/192 against `hyprctl binds -j` on key/keycode+dispatcher+arg;
  modmask histogram `{0:23,1:2,8:7,9:2,12:2,13:1,64:42,65:37,68:26,69:3,72:19,73:22,76:6}` — `[OBS]`.
- §6 `:289-300` Unknowns: no dispatcher fired; docs drift (current wiki is Lua-era; host 0.56.2
  parses hyprlang). The entry's docs (live wiki + 0.54 archive, fetched 2026-10-14) were **never
  registered** — no S-row pins the Binds or Variables pages at base.

### `corpus/knowledge/bind-table-r25.md` (sourced; pins = S162 `src/config/legacy/ConfigManager.cpp` @ `efb50993`)

- `:9` `bind`/`unbind`/`source` handler registration (`handleBind` with flags `{true}`) — sourced,
  `ConfigManager.cpp:607-608,614`.
- `:29-40` Flag suffix letters → booleans in `handleBind` (incl. `i`→`ignoreMods`, `s`→`multiKey`,
  `d`→`hasDescription`, `m`→`mouse`, `c`/`g` also set release) — sourced, `ConfigManager.cpp:1514-1540`.
- `:38` Field grammar `MOD, KEY, DISPATCHER, ARG`; `d` inserts a description; `k` adds a device
  field — sourced, `:1554-1558,1580-1586` (errata: positions rest on adjacent lines).
- `:42` Modifier string goes to `stringToModMask`; a nonempty string yielding mask 0 is rejected —
  sourced, `:1575-1576,1601-1604`.
- `:44` a3w1 observed: empty modifiers are legal mask zero; `stringToModMask` uppercases then
  substring-matches tokens, so token order is immaterial — **observed note** (walked host tree, "not
  every alias or separator spelling").
- `:46` `parseKey`: bare decimal > 9 → keycode; `code:N` decimal → keycode; `catchall` recognized;
  anything else preserved as the key string — sourced, `:1481-1489` (errata: the keycode and
  catch-all *return values* rest on adjacent lines, not the quoted lines).
- `:52` Rejections before `addKeybind`: arg counts, unknown dispatcher, invalid nonempty mod,
  `catchall` outside a submap — sourced, `:1559-1562,1594-1604,1616-1624`.
- `:54` `unbind = all` clears `m_keybinds`; ordinary `unbind` parses MOD/KEY and calls
  `removeKeybind` — sourced, `:1657-1673`.
- `:56` `addKeybind` keeps repeated `(modmask, key, keycode)` identities as separate rows — multiple
  binds on one chord are retained — sourced + a3w1 observed.
- ~`:62` The 18 JSON field names used for table comparison (`key`, `keycode`, `modmask`,
  `catch_all`, `submap`, flags, `dispatcher`, `arg`, …) — observed.
- Errata `:76-82`: ten sentences say more than their quoted lines; read them as resting on adjacent
  lines of the same pinned file.

### `corpus/knowledge/hyprland-input-devices-r46.md` (sourced)

- `:71` Limits: "Per-device layouts do not change the keymap binds are resolved against unless
  `resolve_binds_by_sym = 1` (wiki-Keywords.md:124-130); the join does not check binds." — **held
  sentence**; names the option and a docs anchor, not the mechanism (no "which sym is compared").
- Steps 4-5 (`:36`,`:57` region): `kb_file` tried before the RMLVO names; on compile failure stored
  rules reset to `us`; the dump prints stored rules + `active_keymap`/`active_layout_index`/
  `capsLock`/`numLock` — held context for *which keymap a keyboard has*, not for key matching.

### `corpus/knowledge/config-option-table-r39.md`

- `:40` `handleBind` registered among keyword handlers at `ConfigManager.cpp:601-623` with `{true}`
  — OBS of S162 (same fact as bind-table-r25:9).

### `corpus/knowledge/dispatcher-surface-and-request-grammar-r26.md`

- `:110` The request socket resolves a dispatcher by name via
  `g_pKeybindManager->m_dispatchers.find` — OBS of S018; the *dispatch* path, not the key-press path.

### `corpus/README.md`

- `:16` Summary row of `keybind-rule-semantics.md`: 192/192 reconciliation, §2.1 mod grammar
  `[INF-docs]`, §2.3 key forms (keysym/XF86/keycode/wheel/switch/mouse), §2.4 flags, §2.5
  multi-action keys — pointer, not new fact.

### `SKILL.md`

- `:73-74` App keybinds owned by `~/.config/hypr/bindings.conf`; rebind needs `unbind` first.
- `:138`,`:149`,`:153`,`:212`,`:455` `hyprctl binds -j` read surface: counts/flags/modmask are
  `[OBS]`; *what a bind does when fired* is `[INF-docs]`/UNK by policy (no injection).
- `:564`,`:571` Session-material hygiene: keycode ≠ inserted text; no raw keycodes/keymap contents
  in receipts — **C2's `hyprctl binds -j` receipt must keep this shape-only rule**.

## Held rows citing Hyprland bind-relevant sources (URL + id)

- **S162** — `hyprwm/Hyprland@efb50993/src/config/legacy/ConfigManager.cpp`, sha256 `9db68cf4…`
  (90963 B). Used-by includes `bind-table-r25.md`. Note: the row's anchor column lists
  `:419-451,590-623,893-968,2016-2093`, while `bind-table-r25` cites `:1481-1673` and `:1816-1848`
  from the same pinned bytes — one file, one pin; C2 may cite S162 for `handleBind`/`parseKey`
  lines without a new row.
- **S319** — `src/devices/IKeyboard.cpp` @ `efb50993`, sha256 `8a800efe…` (the claim says: cite it,
  never re-register).
- **S316** — `src/managers/input/InputManager.cpp` @ `efb50993` (applyConfigToKeyboard only).
- **S320/S158** — `src/debug/HyprCtl.cpp` @ `efb50993` (devices request / clients+getprop anchors;
  neither row covers the `binds` request lines).
- **S018** — `HyprCtl.cpp` via `blob/v0.56.2` URL (dispatchRequest).
- **S325** — `hyprland-wiki@ecc06f3/content/Configuring/Keywords.md` (anchor `:124-130` =
  `resolve_binds_by_sym` docs).
- **S167** — `hyprland-wiki@c66e8de2/…/using-hyprctl.md` (`binds`/`-j` verb).
- **S169, S171, S172, S188** — hyprctl `main.cpp`, `src/main.cpp`, hyprlang.md, dispatchers.md.
- **S340-S349, S351** — libxkbcommon 1.13.2 `rules.c`, `xkbcomp.c`, `include.c`, `context.c`,
  `context-priv.c`, `meson_options.txt`, `messages-codes.h`, `tools/compile-keymap.c`, `keymap.c`;
  **S346-S348** xkeyboard-config 2.48 (`rules.in`, `symbols/br`); **S350** host compile receipt —
  all keymap-*compile* ground (round-48), none of it bind-matching.

## Registry gaps (what has NO row at base — S-registry tops at S351)

- `src/managers/KeybindManager.cpp` — **unregistered**; nothing held describes press-time matching.
- libxkbcommon `src/keysym.c`, `tools/how-to-type.c`, any `state*.c` — **unregistered**.
- Hyprland wiki `Binds` page and `Variables` page — **unregistered** (keybind-rule-semantics.md's
  2026-10-14 wiki fetches predate the registry's pinning discipline; its `[INF-docs]` level marks it).
- `xkb_keysym_from_name`/`xkb_keysym_get_name`/`xkb_state_key_get_one_sym`/`get_sym`/utf8/utf32 —
  **zero occurrences** in the scoped corpus.
- `mouse:`, `switch:`, `catchall` semantics at press time; translated-vs-untranslated sym choice;
  layout-0 vs active layout; modifier-mask comparison (exact equality, `ignoreMods` masking,
  Caps/NumLock handling); keycode-bind vs keysym-bind precedence — **nothing held**.

## Exact sentences a new entry must not restate as new

(Verbatim held text; C2 may cite them as held ground or deepen the level, never present as new.)

1. `keybind-rule-semantics.md:106` — "`[INF-docs]` use the segment after `XKB_KEY_`" (named-keysym row).
2. `keybind-rule-semantics.md:108` — "`[OBS]` live JSON: `key:""`, `keycode: N`" (keycode row).
3. `keybind-rule-semantics.md:61` — "`[INF-docs]` `unbind` key matching is case-sensitive."
4. `keybind-rule-semantics.md` §2.1 — "`MOD` is a "string modmask"; **any separators are allowed
   except `,`** … mod order is not significant" (`:67-68`, `[INF-docs]`).
5. `keybind-rule-semantics.md:129` — "No keysym-combo (`s`), submap, catch-all, or per-device binds
   anywhere in the plane" (`[OBS]`).
6. `bind-table-r25.md:46` — "`parseKey` maps a bare decimal string to a keycode only when its value
   is greater than 9, maps `code:N` when `N` is decimal, recognizes `catchall`, and otherwise
   preserves the key string."
7. `bind-table-r25.md:42` — "The modifier string is passed to `stringToModMask`; a nonempty string
   that produces mask zero is rejected."
8. `bind-table-r25.md:44` — "empty modifiers as legal mask zero … `stringToModMask` as uppercasing
   then substring-matching tokens, making token order immaterial" (a3w1-observed).
9. `bind-table-r25.md:56` — "repeated `(modmask, key, keycode)` identities retained as separate
   table rows, so a resolver must preserve multiple binds on one chord."
10. `bind-table-r25.md` flag table rows — each flag letter → boolean mapping (incl. `i`→`ignoreMods`,
    `s`→`multiKey`, `c`/`g`→also `release`).
11. `hyprland-input-devices-r46.md:71` — "Per-device layouts do not change the keymap binds are
    resolved against unless `resolve_binds_by_sym = 1` (wiki-Keywords.md:124-130); the join does not
    check binds."
12. `keybind-rule-semantics.md` §2.2 — the modmask bit decode (1=SHIFT, 4=CTRL, 8=ALT, 64=SUPER)
    and order-insensitivity, all `[OBS]`.
13. `bind-table-r25.md:9` / `config-option-table-r39.md:40` — "`handleBind` registered for `bind`
    with flag suffixes `{true}`" (`ConfigManager.cpp:607-608,614` / `:601-623`).
