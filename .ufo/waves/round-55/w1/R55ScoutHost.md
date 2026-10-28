# Seat R55ScoutHost — round 55 mado, wave w1 — host recon report

Lane root: /home/vgpnk/Projects/shokunin/mado-shokunin. Deliverable: `.ufo/waves/round-55/w1/R55ScoutHost/host.md` (with receipts alongside).

## What I did

Read-only host reads only: `~/.config/hypr/input.conf`, `hyprctl version`, `hyprctl getoption input:repeat_rate|input:repeat_delay|input:numlock_by_default -j`, `hyprctl devices -j`, and `grep -rn` over `~/.config/hypr`. No keyword/dispatch/reload. No edits, no git, no tool installs, no subagents. Scratch under `/fast/scratch/hyaku/mado-r55/R55ScoutHost/` was removed before yield. The first attempt to create the scratch dir in one call did not persist; I recreated it and reran. No functional impact.

## Results

- Pins byte-equal to live: `cmp fetch/host-input.conf ~/.config/hypr/input.conf` → rc 0; `cmp fetch/host-getoption.json <live three getoption calls concatenated>` → rc 0.
- Live options: `repeat_rate` 40, `repeat_delay` 250, `numlock_by_default` 1; all `set: true`.
- Device forms: none. `grep -rn device ~/.config/hypr` matched only the comment `# Control your input devices` in `input.conf`. `device[` / `device {` absent.
- Keyboards: 10. Real names for `--keyboard`:
  - physical (inferred from name): `razer-razer-deathadder-v2-keyboard`, `razer-razer-deathadder-v2-1`, `hp--inc-hyperx-alloy-origins-core`, `hp--inc-hyperx-alloy-origins-core-keypad`, `hp--inc-hyperx-alloy-origins-core-consumer-control`, `yubico-yubikey-otp+fido+ccid`
  - ACPI, not typing keyboards (inferred): `video-bus`, `power-button`, `power-button-1`
  - virtual (inferred from name; the only `main` keyboard): `hl-virtual-keyboard-fcitx5`
- Full table and classification: `.ufo/waves/round-55/w1/R55ScoutHost/host.md`.

## Commands and decisive output (trimmed)

```
cmp fetch/host-input.conf ~/.config/hypr/input.conf                 -> identical (rc 0)
cmp fetch/host-getoption.json live-getoption.json                   -> identical (rc 0)
hyprctl version                                                     -> Hyprland 0.56.2, commit efb50993...
hyprctl getoption input:repeat_rate -j      -> {"option": "input:repeat_rate", "int": 40, "set": true }
hyprctl getoption input:repeat_delay -j     -> {"option": "input:repeat_delay", "int": 250, "set": true }
hyprctl getoption input:numlock_by_default -j -> {"option": "input:numlock_by_default", "int": 1, "set": true }
grep -rn device ~/.config/hypr              -> input.conf:1:# Control your input devices   (only match)
grep -rnE 'device\[|device \{|device\{'     -> no match (rc 1)
```

## Deliverables

- `.ufo/waves/round-55/w1/R55ScoutHost.md` (this file)
- `.ufo/waves/round-55/w1/R55ScoutHost/host.md`
- `.ufo/waves/round-55/w1/R55ScoutHost/keyboards-reduced.json`
- `.ufo/waves/round-55/w1/R55ScoutHost/live-getoption.json`
- `.ufo/waves/round-55/w1/R55ScoutHost/version.txt`
- `.ufo/waves/round-55/w1/R55ScoutHost/receipts-cmp-grep.txt`

## Defects and ambiguities

1. `hyprctl devices -j` keyboard objects carry no `virtual` field. Virtual classification here is by name prefix only (inference). A tool that needs virtual status cannot get it from this JSON.
2. Mixed key casing in the same object (`numLock`, `capsLock` camelCase; `active_keymap`, `active_layout_index` snake_case). Parsers must match exactly.
3. The `hyprctl getoption -j` pin is three JSON objects, one per line (JSON-lines), not one JSON document. This is consistent with the frozen `--getoption` grammar (per-line parse) and not a defect, but it means a full-document `json.load` on the pin fails.
4. The recursive grep included the autostart files; no match came from them and their contents were not printed.

## Not verified

- Virtual vs physical classification of the nine non-fcitx keyboards: name-based inference only; not checked against /proc, udev or the Hyprland source for this build.
- The demo prediction in `host.md` §4 (`from=G/G/G`, `unsupported=0`) is hand-derived from the frozen grammar. I did not run `tools/mado-kbdopts.py` (it is not in my lane's scope and does not exist at base).
- Hold-out fixtures: not looked for, not opened, not used.

## Tooling

No tools installed or upgraded. Nothing in pacman touched.
