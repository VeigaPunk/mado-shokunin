# R55ScoutHost — host recon (read-only)

Date of reads: 2026-10-28. Hyprland 0.56.2 (`hyprctl version`: commit efb50993780079460b0cbed1363e2166a2de1d9f, matches the registration pin tag).

## 1. Pins vs live (byte-equal)

- `fetch/host-input.conf` vs `~/.config/hypr/input.conf`: `cmp` rc 0, identical. Receipt: `receipts-cmp-grep.txt`.
- `fetch/host-getoption.json` vs live `hyprctl getoption input:repeat_rate|input:repeat_delay|input:numlock_by_default -j` (concatenated in that order): `cmp` rc 0, identical.
  - live values: `repeat_rate` 40 (set true), `repeat_delay` 250 (set true), `numlock_by_default` 1 (set true). Receipt: `live-getoption.json`.

## 2. Device forms in ~/.config/hypr

`grep -rn device /home/vgpnk/.config/hypr` (recursive; includes autostart files, whose contents were not printed) matched one line only: `input.conf:1: # Control your input devices` (a comment). The `device[...]` and `device {` / `device{` grep returned no match (rc 1). No per-device block exists on this host.

## 3. Keyboards (`hyprctl devices -j`, reduced to the requested fields)

The keyboard object carries no `virtual` flag. The "virtual?" column is an inference from the name and was not verified via /proc or udev.

| name (use as `--keyboard` value) | main | numLock | capsLock | active_layout_index | active_keymap | virtual? (inferred from name) |
|---|---|---|---|---|---|---|
| razer-razer-deathadder-v2-keyboard | false | true | false | 0 | Portuguese (Brazil) | no (physical HID interface) |
| razer-razer-deathadder-v2-1 | false | true | false | 0 | Portuguese (Brazil) | no (physical; second interface) |
| hp--inc-hyperx-alloy-origins-core | false | true | false | 0 | Portuguese (Brazil) | no (physical keyboard) |
| hp--inc-hyperx-alloy-origins-core-keypad | false | true | false | 0 | Portuguese (Brazil) | no (physical; keypad interface) |
| hp--inc-hyperx-alloy-origins-core-consumer-control | false | true | false | 0 | Portuguese (Brazil) | no (physical; consumer-control interface) |
| video-bus | false | true | false | 0 | Portuguese (Brazil) | no (ACPI input device, not a typing keyboard) |
| power-button | false | true | false | 0 | Portuguese (Brazil) | no (ACPI input device) |
| power-button-1 | false | true | false | 0 | Portuguese (Brazil) | no (ACPI input device) |
| yubico-yubikey-otp+fido+ccid | false | true | false | 0 | Portuguese (Brazil) | no (physical USB security key with keyboard interface) |
| hl-virtual-keyboard-fcitx5 | **true** | true | false | 0 | Portuguese (Brazil) | **yes** (name prefix `hl-virtual-keyboard`; the only `main` keyboard) |

Keyboard count: 10 (`mice` 4 not reported, per scope). Full reduced data: `keyboards-reduced.json`. Version and option receipts: `version.txt`, `live-getoption.json`.

Virtual keyboards: only `hl-virtual-keyboard-fcitx5`. The other nine are non-virtual by name, which is inference.

Note: `numLock` and `capsLock` are camelCase in the JSON; `active_keymap` and `active_layout_index` are snake_case. A parser must use the exact keys.

## 4. Demo prediction for the live `tools/mado-kbdopts.py` run (not run; inference from the frozen grammar)

Input under read: `input.conf` has global `repeat_rate = 40`, `repeat_delay = 250`, `numlock_by_default = true` inside `input {`. The `touchpad {` block holds no relevant keys. No `device` block exists. Expected (by hand from the frozen grammar, not executed):

- `--keyboard <any name>` → `repeat_rate=40 repeat_delay=250 numlock=1 from=G/G/G unsupported=0`
- With `--getoption` on the committed pin: all three `AGREE`, `DONE ... live=AGREE`.

Demo with the `--keyboard` values from §3 (quote names containing `+`, e.g. `"yubico-yubikey-otp+fido+ccid"`).

## 5. Observations for the lane

- The host has no per-keyboard overrides, so `from` should be `G/G/G` for every name; a `D` letter would indicate an unexpected device block.
- `hl-virtual-keyboard-fcitx5` is `main`; the physical keyboards are not. Any per-keyboard demo should include at least one physical name to show `D` vs `G` only if a device block is added (none exists here).
- No secrets were read or quoted. The autostart file's contents were not printed.
