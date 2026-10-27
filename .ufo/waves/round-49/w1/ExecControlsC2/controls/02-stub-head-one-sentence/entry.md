# Hyprland 0.56.2: how the key field of a `bind` line becomes a match for a key press on this host

source: S352 - Hyprland 0.56.2 keybind manager @ commit efb509937800 - the press path, the +8 keycode, the translated-or-sym state choice, the exact modifier compare, the name-to-keysym double lookup
source: S353 - libxkbcommon 1.13.2 `src/keysym.c` @ xkbcommon-1.13.2 - `xkb_keysym_from_name`, the one flag it accepts, and the names it refuses
source: S354 - mado host, read-only `hyprctl binds -j` and `hyprctl getoption input:resolve_binds_by_sym -j` receipt (own-work) - 192 live binds, the form census, the live option value
verified-at: 2026-10-27
recheck: on-release - when Hyprland leaves 0.56.2 or commit efb509937800, or libxkbcommon leaves 1.13.2, re-pull `src/managers/KeybindManager.cpp` and `src/keysym.c` and re-run the capture behind `.ufo/waves/round-49/receipts/live-binds-r49.txt`; also when this host stops reporting the same bind total

## What the evidence licenses

| question | where the answer lives | state |
|---|---|---|
| which keycode a press carries | step 1 | sourced (S352) |
| which keysym of the press is compared | step 2 | sourced (S352, S317); the live option value observed (S354) |
| whether modifiers must match exactly | step 3 | sourced (S352) |
| how a key name becomes a keysym, and what case does | step 4 | sourced (S352, S353) |
| what a key field becomes at parse time | step 5 | held S303, not re-claimed |
| whether a keycode bind and a name bind on one key collide | step 6 | sourced (S352); the census observed (S354) |
## The match

A bind's key field is resolved to a keysym before the modifier mask is compared.
