# AttackText — Round 15 W1 critic report

**Target inference:** "A Wayland `wl_keyboard.key` event, or any lower-layer key observation, means text was inserted."
**Verdict:** **falsified in both directions** using local primary/static sources alone. A U6 ladder rung for `wl_keyboard` can show at most "a keycode was sent to the focused surface's client, to be interpreted against a keymap". Text insertion sits above the toolkit/IME boundary and remains `[UNK]` in this round.
**Axes:** coverage (U6 facet scope). Also no-harm/privacy: keycodes are text-equivalent material.
**Method:** I only read installed XML, headers, man pages and config bytes. I sent no protocol client, ran no event tool and checked no live process or environment. `input-draft.txt` did not exist when I read the wave dir (`/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-15/` held only `evidence/` and `w1/`). So this report attacks the inference itself, not draft wording.
**Tool installs:** none.

## Pinned static sources (sha256, owning package)

| Id | Path | Owner | sha256 (prefix) |
|---|---|---|---|
| W | `/usr/share/wayland/wayland.xml` | wayland 1.26.0-1 | `cc860987e54f8d85` |
| T | `/usr/share/wayland-protocols/unstable/text-input/text-input-unstable-v3.xml` | wayland-protocols 1.49-1 | `160815cda13c285a` |
| X | `/usr/include/xkbcommon/xkbcommon.h` | libxkbcommon 1.13.2-1 | `17e58db5edc299d1` |
| XC | `/usr/include/xkbcommon/xkbcommon-compose.h` | libxkbcommon 1.13.2-1 | `6e2d985b3653c367` |
| IM | `/usr/include/hyprland/protocols/input-method-unstable-v2.hpp` | hyprland 0.56.2-2 | `aa49151200df8739` |
| VK | `/usr/include/hyprland/protocols/virtual-keyboard-unstable-v1.hpp` | hyprland 0.56.2-2 | `6cfdb43b827d523f` |
| KI | `/usr/share/wayland-protocols/unstable/keyboard-shortcuts-inhibit/keyboard-shortcuts-inhibit-unstable-v1.xml` | wayland-protocols 1.49-1 | `9117d9e8ec02e9a3` |
| G | `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-13/w1/globals.json` (`captured_utc` 2026-10-20T04:10:03Z, sanitized header-only) | lane, committed `95cbc41` | — |

## Counterexamples

### A. Key event with no text inserted

1. **The key event carries a keycode, not text.** Source W:2675-2676: "The key is a platform-specific key code that can be interpreted by feeding it to the keyboard mapping". Source W:2594-2597: the format can be `no_keymap`, and with `xkb_v1` "clients must add 8". The client does the translation, so nothing at the protocol layer is text. `[INF-docs]`
2. **Keys that produce no text.** Source X:2060-2088: `xkb_state_key_get_utf8` "If there is nothing to write, returns 0". This covers modifiers, function keys and navigation keys. Release events (W:2652-2664) also produce no text. `[INF-docs]`
3. **Dead keys and Compose.** Source XC:481-490 defines the status `XKB_COMPOSE_COMPOSING` ("In the middle of a sequence"). A key fed during a sequence produces no character, and `CANCELLED` can drop the sequence entirely. `[INF-docs]`
4. **IME keyboard grab.** Source IM:57,158,258-314: Hyprland 0.56.2 binds `zwp_input_method_v2.grab_keyboard` and `CZwpInputMethodKeyboardGrabV2` (with `sendKeymap`). An input method can receive the keys itself, and the application then gets only `preedit_string` (T:364-388). Preedit is composing text, not committed text. Source G lists `zwp_input_method_manager_v2` v1 and `zwp_text_input_manager_v3` v1 as advertised. Routing behaviour was never exercised. `[OBS-history]` advertisement, `[UNK]` behaviour
5. **Compositor binds consume the key before the client sees it.** The corpus note `/home/vgpnk/Projects/shokunin/mado-shokunin/corpus/knowledge/keybind-rule-semantics.md:121` records the `n` (non-consuming) bind flag as unused across all 192 binds. Source KI:27-30: clients must request "the compositor to ignore its own keyboard shortcuts … so that all key events from that seat get forwarded". So a physical keypress may produce no `wl_keyboard.key` at all. `[INF-docs]`
6. **Toolkit shortcuts and IM contexts consume keys.** Ctrl-chords and widget keybindings are handled by the toolkit, not inserted as text. Static strings in `/usr/lib/libgtk-4.so.1` include `GTK_IM_MODULE` and `gtk-im-context-simple`, which shows an IM-context layer exists between key events and the text buffer. `[OBS-static]` presence only; policy `[INF]`
7. **No focused text widget.** Source W:2684-2685: the compositor "must not send this event if the wl_keyboard did not have an active surface". The surface having focus does not mean a text entry has focus. `[INF-docs]`

### B. Text inserted with no matching key event

1. **The IME commits text directly.** Source T:33: the protocol lets "compositors to act as input methods and to send text to applications". Source T:390-401: `commit_string` is "either just a single character after a key press or the result of some composing", applied on `done` (T:425-430). Text arrives over a different protocol object than `wl_keyboard`. `[INF-docs]`
2. **Client-side repeat: one press, many characters.** Source W:2732-2751: `repeat_info` gives the rate "in characters per second", and the client repeats. Source W:2690-2693: compositor-side `repeated` events exist only "Since version 10". The historical advertisement in G (lines 33-36) shows `wl_seat` **v9**, so on that sample repeat would have been client-synthesised, and the count of key events does not equal the count of characters. That `wl_keyboard` is capped at the bound seat's version is `[INFERENCE]` from Wayland object versioning; it is not quoted from W.
3. **Synthetic keys.** Source VK:72,120-121: `zwp_virtual_keyboard_v1` `setKeymap`/`setKey` lets a client inject keys with its own keymap. G lists `zwp_virtual_keyboard_manager_v1` v1. The corpus also records the Hyprland dispatcher `sendshortcut`, which synthesises key input into windows (`keybind-rule-semantics.md:152`). Even a real `key` event does not prove a physical keypress. `[INF-docs]`/`[OBS-history]`

### C. The IME/toolkit boundary is configured on this host but not exercised

Facts from static config bytes `[OBS-static]`:
- `/home/vgpnk/.local/share/omarchy/default/hypr/autostart.conf:4` reads `exec-once = uwsm-app -- fcitx5 --disable notificationitem` (sha `acb6a668…`).
- `/home/vgpnk/.config/environment.d/fcitx.conf` sets `QT_IM_MODULE`, `XMODIFIERS` and `SDL_IM_MODULE` to `fcitx`. It sets **no** `GTK_IM_MODULE`. Its sha `8b077b6e…` is byte-identical to `~/.local/share/omarchy/config/environment.d/fcitx.conf`.
- `/home/vgpnk/.config/hypr/bindings.conf:15` launches Typora with `--enable-wayland-ime`.

What these imply, per toolkit `[INF]`:
- **Qt and SDL** take the fcitx module route.
- **GTK4** goes through its own IM-context selection, probably text-input-v3. This is `[INFERENCE]`.
- **Electron/Chromium** needs an explicit flag to use Wayland IME.

So the same `wl_keyboard.key` can lead to different text outcomes depending on the client toolkit. The live environment, whether fcitx5 is running and the active input method were not read; all three are `[UNK]`.

### D. Even the lowest layer withholds keys as a privacy measure

`/usr/share/man/man1/libinput-debug-events.1.gz` (libinput 1.31.3-1), lines 42-46: "Key events shown by this tool are partially obfuscated to avoid passwords …; use --show-keycodes". Keycodes are equivalent to text (passwords). Any rung that would "verify text" by capturing keys is therefore a privacy breach and out of scope under the contract. This is the no-harm side of the same inference.

## Impacted claims and the smallest safe correction

**Defect class: fixable, not a tradeoff.** The judge must reject only if U6's "6/7" depends on a statement that key delivery, device listing or seat capability shows application text or behaviour. A U6 route limited to documentation stays admissible if it holds this line.

Correction, all inside the existing U6 note. No new source row, gate or capability is needed:

1. **One ladder row**, worded exactly: "`wl_keyboard.key` = keycode + state to the focused surface's client under the current keymap (W:2669-2698, 2589-2612); it does not prove a physical press (virtual keyboard), the produced character (keymap/compose), or text insertion (toolkit shortcuts, IM grab, `text_input_v3.commit_string`)." Tag the outcome `[UNK]`.
2. **A boundary line naming the layers above `wl_keyboard`, unexercised:**
   - compositor bind consumption and shortcuts-inhibit;
   - client xkb state and Compose;
   - toolkit shortcut and IM context;
   - IME (`input-method-v2` grab → `text-input-v3` preedit/commit);
   - the widget.

   Text-input sources stay unadmitted context, consistent with TextInputBoundary. Do not add an S-row only for this.
3. **Forbidden wording:** "typed", "entered text", "input works in <app>", "IME active", and any "N key events = N characters".
4. **Recheck route:** static sources only (this table). Never `debug-events`, `--show-keycodes`, `record`, `wev`, virtual-keyboard or `sendshortcut` execution.

## Limits

- I opened no remote URL; the anchors above are to installed copies, not upstream revisions.
- The upstream tag/commit for W and T needs the S052 row's own pin. Installed `wayland.xml` declares `wl_keyboard` version 11 and `wl_seat` version 11. The historical host advertisement in G shows `wl_seat` v9 and `zwp_text_input_manager_v3` v1. The installed T declares v2, whose `since="2"` items (T:462-560) were not available in that sample.
- Behaviour of Hyprland's IM grab is inferred from generated binding headers only. Routing order between binds, IM grab and the focused client is `[UNK]`.
