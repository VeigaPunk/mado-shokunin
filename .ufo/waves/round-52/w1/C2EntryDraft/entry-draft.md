# Synthetic key events on Hyprland 0.56.2: how `sendshortcut` and `sendkeystate` turn one argument into seat events, and which state they borrow

Draft entry for round 52, seat `C2EntryDraft`. Not committed; proposer artifact only. Proposal slug
`hyprland-synthetic-key-dispatch-r52` (`corpus/knowledge/hyprland-synthetic-key-dispatch-r52.md`).
Round-51 target slug stays untouched: this file is a candidate for a *separate* indexed entry, and the
round-52 C2 counter must name this slug and prove it absent at base.

## Why this subject is distinct

Round 51 (`corpus/knowledge/hyprland-dispatcher-dispatch-r51.md`) accounts for the dispatcher *map*: how
a bind stores the dispatcher and its tail, how the name resolves through two tables, the `submap` and
`pass` special cases, and how `hyprctl dispatch` reaches the same table. It states one parenthetical
about `sendkeystate` ("the one dispatcher that writes the field itself, saving and restoring it around
its work") and uses `sendshortcut` only as an example of a three-comma argument grammar.

This entry starts where that parenthetical stops: it treats the two dispatchers that *manufacture* input
events and hand them to the seat - the argument grammar, the closed state alphabet, how a name becomes a
keycode, which timestamp and modifier mask the synthetic event carries, and what the dispatch leaves
behind in process-wide state. The map, the parse-time validation, the press path, `submap` and the
socket verb are held ground here (rows S364-S369), never re-argued.

## Proposed source rows (opened this round; not yet appended)

Nothing below is appended to `corpus/SOURCES.md` by this seat - the registry edit is the data seat's.
Row ids are proposals in the round-52 sequence, each with the scope this entry needs.

source: S370 (proposed) - Hyprland 0.56.2 legacy dispatcher translator, the two synthetic-event dispatchers - https://raw.githubusercontent.com/hyprwm/Hyprland/efb50993780079460b0cbed1363e2166a2de1d9f/src/config/legacy/DispatcherTranslator.cpp - code - how `sendshortcut` and `sendkeystate` read their fields, resolve a keycode, choose a window and delegate - `CVarList2 ARGS(args, 4);` (Hyprland-legacy-DispatcherTranslator.cpp:592)
source: S371 (proposed) - Hyprland 0.56.2 action state and seat delivery for a synthetic event - https://raw.githubusercontent.com/hyprwm/Hyprland/efb50993780079460b0cbed1363e2166a2de1d9f/src/config/shared/actions/ConfigActions.cpp - code - the press field's read, the modifier mask sequence, the timestamp and keycode the seat receives, and the save/restore lines the action-side twin also uses (held, round 51) - `g_pSeatManager->sendKeyboardMods(modMask, 0, 0, 0);` (Hyprland-ConfigActions.cpp:1554)
source: S372 (proposed) - Hyprland 0.56.2 action-state declaration - https://raw.githubusercontent.com/hyprwm/Hyprland/efb50993780079460b0cbed1363e2166a2de1d9f/src/config/shared/actions/ConfigActions.hpp - code - the fields a dispatcher borrows (press marker, last key, last mouse button, last timestamp) and the `std::expected` action result - `int m_passPressed = -1;` (Hyprland-ConfigActions.hpp:114)
source: S373 (proposed) - Hyprland 0.56.2 modifier-string parser and keycode cache - https://raw.githubusercontent.com/hyprwm/Hyprland/efb50993780079460b0cbed1363e2166a2de1d9f/src/managers/KeybindManager.cpp - code - `stringToModMask`'s substring membership (:221-240 in this file) and the `m_keyToCodeCache` member it fills (declared `Hyprland-KeybindManager.hpp:149`, written from `DispatcherTranslator.cpp:559-576`) - `uint32_t CKeybindManager::stringToModMask(std::string mods)` (Hyprland-KeybindManager.cpp:221)
held (cited, not re-registered): S364 (the map and press call), S365 (the translator's `run` and per-dispatcher splitting), S366 (the socket verb), S367 (submap/pass actions), S368 (parse-time dispatcher validation), S369 (dispatch result defaults); S352/S353 (the key-match/parse accounts of the same KeybindManager and legacy ConfigManager bytes)
held: `corpus/knowledge/bind-table-r25.md:42` - `stringToModMask` uppercases and substring-matches, and the bind path rejects a nonempty modifier string that yields mask 0 (row S162); this entry claims only what the `sendshortcut` path does with that parser, not the parser's first account

Lane: mado-shokunin. Round: 52. Wave: w1. Base: `85d57a818c3707397e21c840b6498b105ba798aa`.
verified-at: 2026-10-27 (pin bytes read from disk this round; access date for each URL above is the round's read date)
recheck: on-release - when Hyprland leaves `0.56.2` (`efb50993`), re-pull S370-S373 and re-read `sendkeystate`,
`sendshortcut`, the keysym scan and its cache, `sendKeyboardMods`/`sendKeyboardKey` at the call sites, and
`Actions::sendKeyState`; also recheck `stringToModMask` if the modifier-name set changes
ground: the dispatcher map, its parse-time validation, the press path, `submap` and the socket entry are
held from round 51 (S364-S369) and cited only; the key field's own match semantics are held from round 50
(`corpus/knowledge/hyprland-bind-key-match-r50.md`); this entry adds no account of either.

## What the evidence licenses

| question | where the answer lives | state |
|---|---|---|
| how many fields `sendkeystate` and `sendshortcut` each take | step 1 | sourced (P01, P06) |
| which state words exist, and what a wrong one does | step 2 | sourced (P02) |
| which state produces a press, a release, and what `repeat` actually sends | steps 2-3 | sourced (P03, P04, P13) |
| whether `sendkeystate` resolves keys itself | step 1 | sourced: no, it rebuilds a three-field tail (P05) |
| what a modifier word means and what an unknown word means | step 4 | sourced (P07) |
| how a key argument becomes a keycode, in which order the branches are tried | step 5 | sourced (P08-P11) |
| which failure message an unresolvable key produces, and where it is raised | step 5 | sourced (P18) |
| which window a synthetic event goes to, and what an empty field means | step 6 | sourced (P12) |
| what an empty selector resolves to downstream | step 6 | sourced (P12, P16) |
| what happens when nothing is focused | step 6 | sourced (P17) |
| what timestamp, keycode offset and modifier mask the seat receives | step 7 | sourced (P13, P14) |
| whether a dispatch is visible afterwards in the press field | step 8 | sourced (P15) |
| whether the action-side twin is new ground here | step 8 | no: held from round-51 step 6, cited only |
| what the client does with the event, whether the scan's last match is the intended one | - | `[UNK]` / `[INF]`, see Limits |

## The chain

1. **Two dispatchers, two field counts, one delegate.** `sendkeystate` splits its tail into at most four
   comma fields and refuses anything but four: `CVarList2 ARGS(args, 4); if (ARGS.size() != 4)` /
   `return {.success = false, .error = "sendkeystate: invalid args"};`
   (Hyprland-legacy-DispatcherTranslator.cpp:592-594). It then pieces the argument back together without
   the state field, `std::string modifiedArgs = std::string(ARGS[0]) + "," + std::string(ARGS[1]) + "," +
   std::string(ARGS[3]);` (:607), and calls `sendshortcut` (:619), which itself splits into at most three
   and refuses anything but three `CVarList2 ARGS(args, 3); if (ARGS.size() != 3)` /
   `"sendshortcut: invalid args"` (:532-535). So the state field is consumed by the outer dispatcher and
   never reaches the keycode resolver; both refusal messages are dispatcher-specific, and a
   five-field `sendkeystate` tail fails on the first test even though its first three fields would be a
   valid `sendshortcut`.

2. **A closed state alphabet, mapped onto the press field.** The third field is compared against three
   literals: `if (STATE != "down" && STATE != "repeat" && STATE != "up")`, with
   `"sendkeystate: invalid state, must be 'down', 'repeat', or 'up'"` as the refusal (:596-598). `down`
   and `repeat` set `keyState` to 1 and 2; `up` leaves the 0 it was initialised with (:600-604). The
   press field itself is then written by that pair: `if (keyState == 1 || keyState == 2)` sets
   `m_passPressed = 1`, the other case sets 0 (:614-617). `repeat` is therefore *not* a distinct edge - it
   is a press, and step 3 is what distinguishes it.

3. **`repeat` is two delegate calls, not a special event type.** `auto result = sendshortcut(modifiedArgs);`
   is followed by `if (keyState == 2 && result.success) result = sendshortcut(modifiedArgs);`
   (:619-622). Because the press field is 1 for both calls, each delegate call takes the press branch of
   `Actions::pass` and no release is sent (:1556-1560); so `repeat` emits two press edges and no release,
   and a failing first call suppresses the second. `up` emits one release; `down` one press.

4. **A modifier word is a substring, not a token.** `sendshortcut` converts its first field with
   `g_pKeybindManager->stringToModMask(...)` (:536), which uppercases the whole string
   `std::ranges::transform(mods, mods.begin(), ::toupper);` and then tests membership
   `if (mods.contains("SHIFT")) modMask |= HL_MODIFIER_SHIFT;` against each known name (SHIFT, CAPS,
   CTRL/CONTROL, ALT/MOD1, MOD2, MOD3, SUPER/WIN/LOGO/MOD4/META, MOD5)
   (Hyprland-KeybindManager.cpp:221-240). There is no token split and no error path: text that names
   nothing leaves `modMask` at its 0 initial value, and a word that merely contains a known name - any
   `SHIFT...` spelling - sets that bit.

5. **Four keycode branches, in written order.** A plain number greater than 9 is used as the keycode, and
   `code:` followed by digits is the same number: `if (isNumber(KEY) && std::stoi(KEY) > 9) keycode =
   std::stoi(KEY); else if (KEY.starts_with("code:") && isNumber(KEY.substr(5))) keycode =
   std::stoi(KEY.substr(5));` (:540-543). `mouse:` followed by digits takes the same `std::stoi` and
   refuses values below 272 with `"sendshortcut: invalid mouse button"` (:544-547). Everything else is a
   keysym: `xkb_keysym_from_name(KEY.c_str(), XKB_KEYSYM_CASE_INSENSITIVE)` (:550) against
   `g_pSeatManager->m_keyboard`'s keymap, scanning `kc = keycode_min; kc <= keycode_max; ++kc` and
   comparing `xkb_state_key_get_one_sym(ks, kc)` (:561-564). Two shape facts matter and are recorded as
   `[INF]` where they go beyond the quote: the loop assigns `keycode = kc` on every match without
   breaking (:565-570), so the highest matching keycode in the range is the one that survives; and the
   cache entry is written only on a miss, keyed `std::format("{}{}", rc<uintptr_t>(KB.get()), KEY)`
   (:557) - the keyboard object's address and the key text as written, so `A` and `a` are two entries
   although the keysym lookup is case-insensitive. The last tests are
   `"sendshortcut: key not found"` (inside the scan, :574), `"sendshortcut: invalid key"` (:580) and
   `"sendshortcut: no kb"` (:555) when no keyboard exists.

6. **The third field chooses the target; empty means the focused window.** The translator side is a
   ternary: `const std::string regexp = std::string(ARGS[2]);` / `PHLWINDOW PWINDOW = regexp.empty() ?
   nullptr : Desktop::viewState()->query().selector(regexp).runWindow();` (:582-583), and a written
   selector that resolves to nothing returns `"sendshortcut: window not found"` (:586). The `nullptr` an
   empty field produces is **not** an empty target downstream: `Actions::pass(modMask, key, w)` starts
   with `auto window = xtract(w);` (:1531), and `xtract` is
   `static PHLWINDOW xtract(std::optional<PHLWINDOW> window) { return
   window.value_or(Desktop::focusState()->window()); }` (Hyprland-ConfigActions.cpp:47-49), so the
   delivery calls target the focused window. A null window survives only when nothing is focused at
   all; the modifier and key events are sent before `if (!window) return {};` (:1554-1579), so even then
   the event is emitted and only the focus bookkeeping is skipped. An earlier wording of this step said
   the empty field delivered "without moving focus" - that was wrong: the focus-switch block does run,
   against the already-focused window, because `xtract` filled the target in.

7. **What the seat receives.** Delivery is `Actions::pass(MOD, keycode, PWINDOW)` (:588). That overload
   is the round-51 `pass` action with an explicit key, and it differs from the window-selector overload in
   two ways this entry relies on: the mouse test is a value range,
   `const bool isMouse = key >= 272 && key < 0x160;` (Hyprland-ConfigActions.cpp:1534), instead of a last-
   event check, and the key goes to the seat with an offset - `key - 8` for the keyboard path,
   `key` unchanged for the pointer path (:1558,1560). The timestamp on every synthetic event is
   `S.m_timeLastMs` (:1558), the field declared as `uint32_t m_timeLastMs = 0; // timestamp of last
   key/mouse event` (Hyprland-ConfigActions.hpp:117) - so a synthetic event is stamped with the last real
   event's time, and 0 before any real input. The modifier sequence is
   `sendKeyboardMods(modMask, 0, 0, 0)` before the event and `sendKeyboardMods(0, 0, 0, 0)` after
   (:1554,1576), so the mask is synthesised for the event and released immediately; it is never read from
   the seat's current state.

8. **What the dispatch leaves behind.** `sendkeystate` saves the press field
   `const int oldPassPressed = Config::Actions::state()->m_passPressed;` (:612) before writing it, and
   restores it at :624 on the way out, so no branch of the dispatcher leaves `m_passPressed` changed -
   a bind that fires `sendkeystate` therefore does not disturb what a later `pass`, `mouse` or `global`
   bind reads. The action-side twin (`Actions::sendKeyState`, ConfigActions.cpp:1601-1615) performs the
   same save/restore; that is **held** ground from round 51's `sendkeystate` parenthetical and is cited
   once here as contrast with the translator-side pair (P15), never re-claimed. The only shape fact this
   entry adds about the twin is its repeat guard, written `keyState == 2 && result.has_value()` (:1612),
   which is `[INF]` equivalent to the dispatcher's `result.success` because `ActionResult` is
   `std::expected<SActionResult, SActionError>` (ConfigActions.hpp:36); it is not a proposition.

## Alternative distinct surfaces (recon note, not drafted)

`C2SourceRecon` named two surfaces with fresh URLs that this seat did not draft, recorded here so the data
seat can choose without re-running recon:

- **`exec` -> process spawning**: `DispatcherTranslator.cpp:4` includes `supplementary/executor/Executor.hpp`
  and the `exec`/`execr` entries call into it (`:66`, `:73`); `Executor.{hpp,cpp}` carries no wave pin. It
  is a dispatcher-execution surface (argument -> spawned process, reaping) disjoint from both this draft
  and round 51.
- **Shortcuts-inhibit gate**: `src/protocols/ShortcutsInhibit.{hpp,cpp}` is unpinned; the gate sites are
  `KeybindManager.cpp:643` and `:844-851`. This is a dispatch *refusal* mechanism, also disjoint.

Neither was opened by this seat; no claim is made about either.

## Proposition map (counter-readable form: `proposition-map.tsv`)

Every material factual proposition in this draft appears once, with its proposed row, pin and anchor, an
exact located quote of at most 25 words, and the reason the quote supports the proposition. Quotes are
compared to the pin bytes with runs of whitespace collapsed; the checker receipt is `quotes-check.txt`.

| id | proposition | row | pin:anchor | quote (<=25 words) | support class | why it supports |
|---|---|---|---|---|---|---|
| P01 | `sendkeystate` takes exactly four comma-separated fields and rejects any other count before touching state. | S370 | Hyprland-legacy-DispatcherTranslator.cpp:591-594 | `CVarList2 ARGS(args, 4); if (ARGS.size() != 4) return {.success = false, .error = "sendkeystate: invalid args"};` | direct | The constructor caps the split at four fields and the size test is the only gate before the state field is read; the returned error string is the rejection. |
| P02 | The state field is a closed three-value set - `down`, `repeat`, `up` - and any other token is refused. | S370 | Hyprland-legacy-DispatcherTranslator.cpp:597-598 | `if (STATE != "down" && STATE != "repeat" && STATE != "up")` | direct | The comparison is an exhaustive negative test over the three literals; the next line (L598) returns the error naming exactly those three values. |
| P03 | `down` and `repeat` are both a press (keyState 1 and 2); `up` is the default keyState 0. | S370 | Hyprland-legacy-DispatcherTranslator.cpp:601-604 | `if (STATE == "down") keyState = 1; else if (STATE == "repeat") keyState = 2;` | direct | keyState is initialised to 0 at L600 and only the two press states overwrite it, so `up` keeps 0 without a branch. |
| P04 | `repeat` runs the delegate a second time, and only when the first call reported success. | S370 | Hyprland-legacy-DispatcherTranslator.cpp:619-622 | `auto result = sendshortcut(modifiedArgs); if (keyState == 2 && result.success) result = sendshortcut(modifiedArgs);` | direct | The second call is guarded by both the repeat state and the first result's success flag; nothing else repeats. |
| P05 | `sendkeystate` does not resolve anything itself: it rebuilds a three-field tail without the state field and delegates to `sendshortcut`. | S370 | Hyprland-legacy-DispatcherTranslator.cpp:607 | `std::string modifiedArgs = std::string(ARGS[0]) + "," + std::string(ARGS[1]) + "," + std::string(ARGS[3]);` | direct | Fields 0, 1 and 3 are rejoined with commas and field 2 (the state) is dropped, so the delegate sees the sendshortcut shape. |
| P06 | `sendshortcut` itself requires exactly three fields (mods, key, window). | S370 | Hyprland-legacy-DispatcherTranslator.cpp:531-535 | `CVarList2 ARGS(args, 3); if (ARGS.size() != 3) return {.success = false, .error = "sendshortcut: invalid args"};` | direct | The split is capped at three and the size test precedes every parse step, so a rebuilt tail from P05 passes only with three fields. |
| P07 | The `sendshortcut` path inherits the bind parser's uppercase-substring modifier reading, so an unrecognised word is silently mask 0 while any word containing a known name sets its bit. | S373 | Hyprland-KeybindManager.cpp:223-225 | `std::ranges::transform(mods, mods.begin(), ::toupper); if (mods.contains("SHIFT")) modMask \|= HL_MODIFIER_SHIFT;` | direct | The whole string is uppercased and every known name is a `contains` test with no rejection branch, so this path cannot report a bad modifier word; the parser's own zero-mask rejection lives on the bind path (held, bind-table-r25:42 / S162), not here. |
| P08 | The key field has a numeric branch: a plain number greater than 9 is a keycode, and `code:N` is the same number in the same space. | S370 | Hyprland-legacy-DispatcherTranslator.cpp:540-543 | `if (isNumber(KEY) && std::stoi(KEY) > 9) keycode = std::stoi(KEY); else if (KEY.starts_with("code:") && isNumber(KEY.substr(5))) keycode = std::stoi(KEY.substr(5));` | direct | Both branches assign std::stoi of the digits with no offset applied, so the two spellings produce the same keycode value. |
| P09 | The `mouse:` branch accepts only numbers at or above 272 and rejects the rest. | S370 | Hyprland-legacy-DispatcherTranslator.cpp:544-547 | `if (KEY.starts_with("mouse:") && isNumber(KEY.substr(6))) { keycode = std::stoi(KEY.substr(6)); if (keycode < 272) return {.success = false, .error = "sendshortcut: invalid mouse button"};` | direct | The prefix strips to a number, then the threshold test returns the mouse-button error before any delivery; 272 is the lower bound written on L546. |
| P10 | The remaining key names are resolved by scanning the seat keyboard's whole keycode range against the current xkb state. | S370 | Hyprland-legacy-DispatcherTranslator.cpp:565-566 | `for (xkb_keycode_t kc = keycode_min; kc <= keycode_max; ++kc) { xkb_keysym_t sym = xkb_state_key_get_one_sym(ks, kc);` | direct | The loop spans min_keycode to max_keycode of the seat keyboard's keymap and compares each key's one-symbol read against the requested keysym. |
| P11 | The keysym result is cached per keyboard pointer and raw key spelling, not per keysym. | S370 | Hyprland-legacy-DispatcherTranslator.cpp:557 | `const auto KEYPAIRSTRING = std::format("{}{}", rc<uintptr_t>(KB.get()), KEY);` | direct | The cache key concatenates the keyboard object address with the argument as written (no case folding), and the cache is consulted and filled under that key. |
| P12 | An empty third field resolves to nullptr with no selector lookup; a written selector that resolves to nothing is an error. | S370 | Hyprland-legacy-DispatcherTranslator.cpp:582-586 | `const std::string regexp = std::string(ARGS[2]); PHLWINDOW PWINDOW = regexp.empty() ? nullptr : Desktop::viewState()->query().selector(regexp).runWindow();` | direct | The ternary maps empty text to nullptr and never runs a selector; the test at :585 returns window-not-found when a written selector produced no window. What nullptr later means for delivery is P16, not this quote. |
| P13 | The synthetic event carries the timestamp of the last real input event and the keyboard keycode minus 8; the modifier mask is asserted before delivery and cleared to 0 after. | S371 | Hyprland-ConfigActions.cpp:1558-1558 | `g_pSeatManager->sendKeyboardKey(S.m_timeLastMs, key - 8, WL_KEYBOARD_KEY_STATE_PRESSED);` | direct | Delivery reads the shared state's m_timeLastMs rather than a clock, subtracts 8 for the keyboard path, and the surrounding sendKeyboardMods calls set the mask then clear it. |
| P14 | The shared state field is the last key/mouse event's timestamp, defaulting to 0. | S372 | Hyprland-ConfigActions.hpp:117-117 | `uint32_t m_timeLastMs = 0; // timestamp of last key/mouse event` | direct | The declaration and its comment name the field P13 reads; the 0 initial value is the pre-input value a synthetic event would carry. |
| P15 | `sendkeystate` restores the previous press field after it delegates, so a dispatch does not leave its state behind. | S370 | Hyprland-legacy-DispatcherTranslator.cpp:612-612 | `const int oldPassPressed = Config::Actions::state()->m_passPressed;` | direct | The value is saved at L612 before the writes at L614-617 and written back at L624 after the delegate returns, on every path out of the function. |
| P16 | A null window is replaced by the focused window before delivery, so an empty selector targets whatever is focused. | S371 | Hyprland-ConfigActions.cpp:47-49 | `static PHLWINDOW xtract(std::optional<PHLWINDOW> window) { return window.value_or(Desktop::focusState()->window()); }` | direct | The helper returns the optional's value or the focus-state window, and `Actions::pass(modMask, key, w)` calls it on the first line of the body (:1531), so the nullptr from P12 never reaches the delivery calls. |
| P17 | When no window is focused at all, the modifier and key events are still sent and only the focus bookkeeping is skipped. | S371 | Hyprland-ConfigActions.cpp:1578-1579 | `if (!window) return {};` | direct | This return is placed after the modifier and key sends (:1554-1576), so a surviving null window suppresses only the later focus restore, not the event. |
| P18 | A keysym the scan cannot find fails with `key not found` inside the scan, distinct from the later generic `invalid key` guard. | S370 | Hyprland-legacy-DispatcherTranslator.cpp:574 | `return {.success = false, .error = "sendshortcut: key not found"};` | direct | This return sits inside the keysym branch before the cache is filled; the `invalid key` return at L580 is outside every branch, so the message identifies where resolution stopped. |

## State claims

| state | attr | value claimed | setter cite | kind |
|---|---|---|---|---|
| `CActionState::m_passPressed` | value | 1 before a down/repeat delegate, 0 before up, old value restored after | Hyprland-legacy-DispatcherTranslator.cpp:614-617,624 | assignment |
| `CActionState::m_passPressed` (twin) | value | same, via `Actions::sendKeyState` | Hyprland-ConfigActions.cpp:1605-1615 | assignment |
| `CKeybindManager::m_keyToCodeCache` | entry | keycode for (keyboard address, key text) on a scan miss | Hyprland-legacy-DispatcherTranslator.cpp:559,569 | map insert |
| seat keyboard modifier state | mask | `modMask` during the event, 0 after | Hyprland-ConfigActions.cpp:1554,1576 | protocol message |
| seat keyboard key state | event | one press, one release, or both (only when the field is -1) | Hyprland-ConfigActions.cpp:1556-1574 | protocol message |

## Observations

**OBS** S370: `sendkeystate: invalid args` (Hyprland-legacy-DispatcherTranslator.cpp:594) - the dispatcher
has its own refusal string, distinct from `sendshortcut: invalid args` (:535) and from the round-51
`Invalid dispatcher` (:1151) / `Bad dispatcher` (:32) / parse-time `does not exist` strings.
**OBS** S370: `if (keyState == 2 && result.success)` (:621) - a failed first delegate call suppresses the
second press edge, so `repeat` degrades to `down` rather than reporting twice.
**OBS** S371: `g_pSeatManager->sendKeyboardMods(0, 0, 0, 0);` (:1576) - the mask is released after the
event, so nothing stays depressed between dispatches.
**OBS** S372: `using ActionResult = std::expected<SActionResult, SActionError>;` (:36) - "success" in the
dispatcher and `has_value()` in the twin are the same predicate.
**OBS** S373: `std::unordered_map<std::string, xkb_keycode_t> m_keyToCodeCache;`
(Hyprland-KeybindManager.hpp:149) - the cache P11 keys is a member of the keybind manager, not of the
translator.

Census of the pinned bytes: pins read 4 (two with a prior registry row under another scope, one new URL
for the header, one reused KeybindManager URL), proposed rows 4, propositions 18, quotes over 25 words 0,
quotes not found at anchor 0 (receipt `quotes-check.txt`).

## Limits

- No key was pressed, no dispatcher was run, no socket or `hyprctl` call was made. All mechanism claims are
  read from the four pinned files at `efb50993`; nothing about this host's runtime is claimed.
- The four URLs were re-fetched by this seat on 2026-10-27 into
  `.ufo/waves/round-52/w1/C2EntryDraft/fetch/` (HTTP 200 each) and every sha256 is byte-equal to the
  round-51 copies (`fetch/verify.txt`), so the quotes were checked against this round's own bytes; the
  registry rows proposed above still need the data seat to open them before anything is admitted.
  The documentation-gap grep used the round-51 copies of the three doc pins, which were not re-fetched.
- P10's "last matching keycode wins" and P11's case-sensitivity of the cache key are `[INF]` from code
  shape (no `break` in the loop; `KEY` not folded before formatting); they are not measured behaviours.
- **Corrected after review (C2Novelty via C2CounterDraft).** Step 6 originally claimed an empty selector
  delivered with no focus switch, resting on `if (!window) return {};` alone. `xtract`
  (Hyprland-ConfigActions.cpp:47-49) fills a null window with the focused window, so that reading was
  wrong; step 6 is rewritten and now cites `xtract` as P16, the surviving-null case as P17, and the
  selector errors as P12/P18. No quote, row or claim outside step 6 changed.
- The action-side twin `Actions::sendKeyState` and its save/restore are **held** ground, not a
  proposition of this entry: round-51 step 6 already states it ("the one dispatcher that writes the field
  itself, saving and restoring it around its work", ConfigActions.cpp:1603-1615). Step 8 cites it once as
  contrast with the translator-side save/restore (P15); the `result.success` vs `result.has_value()`
  equivalence is `[INF]` and is not claimed.
- Which client receives a synthetic event, whether clients accept the stale timestamp, and whether the
  XKB-keycode-minus-8 offset is consumed as an evdev code by the seat are outside this entry; the offset is
  claimed as written, its receiver convention is `[INF]`.
- The pinned dispatcher wiki pages in the same fetch directory do not document `sendkeystate` or
  `sendshortcut` at all (`grep -c` 0 in `wiki-Dispatchers.md`, `wiki-Binds.md`,
  `Hyprland-docs-hyprctl.1.rst`); this is recorded as a documentation gap, not used as a proposition.
- Nothing here establishes that the round-51 entry's account is wrong; it is a different surface. Any
  read of this draft as a correction of S364-S369 is out of scope.
