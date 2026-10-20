# AttackDefault — R15 W1 critic

**Claim attacked:** "the defaults reported by `libinput list-devices` equal the input settings Hyprland is actually using."
**Verdict:** **FALSIFIED.** Official libinput docs and Hyprland source at the v0.56.2 tag both contradict it. The strongest counterexample needs no user configuration (§2).
**Method:** static reads of official docs and tag-pinned upstream source (2026-10-20). I ran no libinput or hyprctl command and accessed no device. Static `pacman -Q/-Si/-Qi` and `man hyprctl` only.

## 1. Primary-doc refutation (libinput 1.32.0, "latest")
| # | URL#anchor | Exact quote (≤25 words) | What it proves |
|---|---|---|---|
| D1 | https://wayland.freedesktop.org/libinput/doc/latest/tools.html#libinput-list-devices | "This tool does **not** show your desktop’s configuration, just the libinput built-in defaults." | The output is libinput's defaults, not the compositor's state. |
| D2 | same anchor | "the tool will show the default configuration for this device … with the default one prefixed with an asterisk" | Even the `*` marks a default, not the active value. |
| D3 | https://wayland.freedesktop.org/libinput/doc/latest/faqs.html#can-i-write-a-program-to-make-libinput-do-foo | "A libinput context is private to the process and cannot be modified from the outside." | The tool reads its own context, separate from Hyprland's (the FAQ diagram labels them "context 1" and "context 2"). |
| D4 | same page, same anchor | "The only way to modify libinput’s behavior is to use the configuration options exposed by the respective compositor." | The active values belong to the compositor. |
| D5 | https://wayland.freedesktop.org/libinput/doc/latest/faqs.html#where-is-the-configuration-stored | "libinput does not store configuration options, it is up to the caller to manage these" | libinput keeps no configuration store that the tool could read. |
| D6 | https://wayland.freedesktop.org/libinput/doc/latest/tapping.html#tap-to-click-default-setting | "Tapping is disabled by default on most devices" | libinput's default for tap-to-click. |
| D7 | https://wayland.freedesktop.org/libinput/doc/latest/clickpad-softbuttons.html#clickfinger-behavior | "This is the default behavior on Apple touchpads." | libinput's default click method depends on the device. |

## 2. Counterexamples where Hyprland overrides a default with no user config (Hyprland v0.56.2 source)
- **Revision:** v0.56.2 tag → commit `efb50993780079460b0cbed1363e2166a2de1d9f`.
- **Files read:**
  - `src/managers/input/InputManager.cpp`, sha256 `feedf32e…e4765`
  - `src/debug/HyprCtl.cpp`, sha256 `798b7c6c…7b91fa`
  - `src/config/values/ConfigValues.cpp`
- **Version match:** the host package is `hyprland 0.56.2-2`. `[INFERENCE]` the Arch package was built from this tag; I did not check the build provenance.

1. **Tap-to-click (strongest).**
   - Hyprland's built-in default is on: `ConfigValues.cpp:331` sets `input:touchpad:tap-to-click` to `true`.
   - `InputManager.cpp:1441-1444` enables tapping on every device that supports it (`tap_get_finger_count`), with no check for whether the user configured it.
   - libinput's default is off on most devices (D6). The official list-devices example output itself shows `Tap-to-click: disabled` (D1).
   - **Result:** on a stock install, the tool says "disabled" while Hyprland has tapping enabled.
2. **Click method.**
   - `InputManager.cpp:1391-1394` always calls `click_set_method`. Its default, `clickfinger_behavior=false` (`ConfigValues.cpp:329`), selects `BUTTON_AREAS`.
   - On Apple touchpads, libinput defaults to clickfinger (D7).
   - **Result:** `[INF-source]` the two disagree on Apple touchpads, assuming the device accepts button areas.
3. **Middle-button emulation.** Wherever emulation is available, `InputManager.cpp:1401-1405` forces it to Hyprland's default of `false` (`ConfigValues.cpp:325`). The tool reports whatever libinput's default is for that device.
4. **Settings applied unconditionally on every device setup.**
   - `setupMouse` calls `setPointerConfigs()` (`InputManager.cpp:1321,1342`).
   - That function sets left-handed, natural scroll, disable-while-typing and acceleration speed at `:1396-1399`, `:1446-1452`, `:1459-1465`.
   - Any per-device override in `device{}` or `hl.device()` also wins (`getDeviceInt(devname, …)`).
5. **The only cases that match.** When `accel_profile` and `scroll_method` are left empty, Hyprland re-applies libinput's default (`:1478-1479`, `:1417-1418`). These are opt-in matches for those two options only, and only while unset; they don't generalize.

## 3. Second-order traps: Hyprland's own read verbs don't show applied state either
- **`hyprctl devices`:** the mouse field `defaultSpeed` is `libinput_device_config_accel_get_default_speed(...)` (`HyprCtl.cpp:769,773`). That is libinput's **default** speed, not the applied `sensitivity`. Reading it as the active speed repeats the same mistake.
- **`hyprctl getoption`:** it returns a config value plus a `set:` flag (`HyprCtl.cpp:1667-1689`). That is a config read. It doesn't show a per-device override or the state after the device's support checks ran.
- **Where the applied state actually lives:** inside Hyprland's own libinput context. Neither the docs nor any allowed verb exposes it, so it stays **[UNK]**. Only a reasoned config-plus-source derivation is admissible, labelled as such.
- **Documentation drift:** the wiki at https://wiki.hypr.land/configuring/core/config-options/ is "Latest git" (updated 2026-10-19) and names the option `tap_to_click`. The v0.56.2 source uses `input:touchpad:tap-to-click`. Cite the tag-pinned source for defaults; the latest wiki isn't pinned to 0.56.2.

## 4. Axes impacted
| Axis | Impact |
|---|---|
| coverage (U6) | Wrong if a ladder row says "list-devices / `hyprctl devices` → active Hyprland input settings". The correct claim is the three-way split in §5. |
| provenance / source tier | D1 is already used as the evidence for round-12 lesson M04 (`corpus/lessons/round-12.md:37`) and lives under `tools.html` (S007). Reuse S007/M04; don't add a duplicate row. If the separate-context claim is needed, `faqs.html` is the one new URL. |
| no-harm / privacy | Nothing gained by running anything. All the refutation is static. |

## 5. Smallest safe correction (for L1 / the integrator)
For the U6 note or ladder row, use the following. Each value-layer source shows only its own layer:

> `libinput list-devices` → libinput **built-in defaults** in a separate context (D1, D3).
> `hyprctl devices` `defaultSpeed` → also a libinput default.
> `hyprctl getoption` → a config read.
> Applied per-device state → **[UNK]**. A stock Hyprland 0.56.2 overrides at least tap-to-click relative to libinput's default (source §2.1).

Also cite the existing M04 lesson; don't restate it as a new finding.

## Tooling
- No installs or upgrades.
- Considered and declined `libinput-tools`:
  - The sync DB has 1.32.0-1 while the installed `libinput` is 1.31.3-1, so installing it would be the partial upgrade that RULES.md forbids.
  - Running it would be a live device probe, which the contract excludes.
