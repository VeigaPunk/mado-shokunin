# R65ScoutSurfaces — Surface State Register Re-derivation Report

- **Seat:** R65ScoutSurfaces (scout)
- **Host:** Linux plazir27 7.2.11-arch1-1 x86_64 (omarchy host returned)
- **Observation Date:** 2026-11-03
- **Lane Repo:** `/home/vgpnk/Projects/shokunin/mado-shokunin`
- **Base Revision:** `524fa1f90b1f2de44b3019bacf833d54e0af13a0` (frozen contract `claims-declaration-r65.md` at `cb63ab13ccaf85191318701d5db5ace050bd5bd4`)
- **Claim:** C1 (freshness: surface-state register re-derived on the returned host)

---

## 1. Executive Summary & Core Verdict

All omarchy surfaces are **PRESENT** and operational on this host. Hyprland is confirmed at **0.56.2 (commit efb50993780079460b0cbed1363e2166a2de1d9f)** with 1 live running instance. The Windows desktop plane is **ABSENT** (expected and honest on this Linux host).

Nothing contradicts the statement:
> "all omarchy surfaces present, Hyprland 0.56.2 at efb5099"

---

## 2. Eight-Row Surface State Register Table (2026-11-03)

| group | observed state (2026-11-03) | probe | one-line result |
|---|---|---|---|
| hypr plane | present (2026-11-03) | `command -v hyprctl && test -d ~/.config/hypr && hyprctl version && hyprctl instances` | rc=0; `/usr/bin/hyprctl` present; `~/.config/hypr` present; Hyprland 0.56.2 (commit `efb50993...`); 1 active instance (`efb50993..._1793632040_1005787507`) |
| waybar | present (2026-11-03) | `command -v waybar && test -d ~/.config/waybar && waybar --version && pgrep -x waybar` | rc=0; `/usr/bin/waybar` present; `~/.config/waybar` present; Waybar v0.15.0; 1 live process (pid 1720) |
| walker | present (2026-11-03) | `command -v walker && test -d ~/.config/walker && walker --version` | rc=0; `/usr/bin/walker` present; `~/.config/walker` present; walker v2.17.2 |
| terminal configs | present (2026-11-03) | `test -e ~/.config/alacritty && test -e ~/.config/foot && test -e ~/.config/kitty && test -e ~/.config/ghostty` | rc=0; 4/4 config directories present (`~/.config/{alacritty,foot,kitty,ghostty}`) |
| theme/wallpaper omarchy plane | present (2026-11-03) | `test -e ~/.config/omarchy && test -e ~/.local/share/omarchy && cat ~/.config/omarchy/current/theme.name && readlink ~/.config/omarchy/current/background` | rc=0; paths present; theme `matte-black`; wallpaper symlink resolves to `/home/vgpnk/.config/omarchy/current/theme/backgrounds/0-ship-at-sea.jpg` |
| idle/lock plane | present (2026-11-03) | `command -v hypridle hyprlock hyprsunset` | rc=0; 3/3 binaries present (`/usr/bin/hypridle`, `/usr/bin/hyprlock`, `/usr/bin/hyprsunset`) |
| omarchy skill docs | present (2026-11-03) | `test -d ~/.agents/skills/omarchy && omarchy version` | rc=0; `~/.agents/skills/omarchy` present; `omarchy version` prints `3.8.3` (repo git tag `v3.8.4` at `8fcc9d604`) |
| windows desktop plane | absent (2026-11-03) | `command -v powershell.exe pwsh powershell` | rc=1; all 3 PowerShell binaries absent on Linux host |

---

## 3. Detailed Command Execution & Return Codes (QUALITY 26)

All probes were executed independently before reading `.ufo/waves/round-65/receipts/before-register-probes-r65.txt`. Full raw stdout/stderr logs are committed in this seat directory at `probes.log`.

### Group 1: hypr plane
- `command -v hyprctl`: exit code `0` (`/usr/bin/hyprctl`)
- `test -d ~/.config/hypr`: exit code `0` (directory exists)
- `hyprctl version | head -n 2`: exit code `0`
  ```
  Hyprland 0.56.2 built from branch v0.56.2 at commit efb50993780079460b0cbed1363e2166a2de1d9f clean ([gha] Nix: update inputs).
  Date: Wed Aug 5 14:13:21 2026
  ```
- `hyprctl instances`: exit code `0`
  ```
  instance efb50993780079460b0cbed1363e2166a2de1d9f_1793632040_1005787507:
  	time: 1793632040
  	pid: 1665
  	wl socket: wayland-1
  ```
- `hyprctl instances | grep -c '^instance '`: exit code `0` (count: `1`)

### Group 2: waybar
- `command -v waybar`: exit code `0` (`/usr/bin/waybar`)
- `test -d ~/.config/waybar`: exit code `0`
- `waybar --version`: exit code `0` (`Waybar v0.15.0`)
- `pgrep -x waybar | wc -l`: exit code `0` (count: `1`, pid `1720`)

### Group 3: walker
- `command -v walker`: exit code `0` (`/usr/bin/walker`)
- `test -d ~/.config/walker`: exit code `0`
- `walker --version`: exit code `0` (`2.17.2`)

### Group 4: terminal configs
- `test -e ~/.config/alacritty`: exit code `0`
- `test -e ~/.config/foot`: exit code `0`
- `test -e ~/.config/kitty`: exit code `0`
- `test -e ~/.config/ghostty`: exit code `0`
- Combined check: 4/4 directories present.

### Group 5: theme/wallpaper omarchy plane
- `test -e ~/.config/omarchy && test -e ~/.local/share/omarchy`: exit code `0`
- `cat ~/.config/omarchy/current/theme.name`: exit code `0` (`matte-black`)
- `readlink ~/.config/omarchy/current/background`: exit code `0` (`/home/vgpnk/.config/omarchy/current/theme/backgrounds/0-ship-at-sea.jpg`)
- `readlink -f ~/.config/omarchy/current/background`: exit code `0` (`/home/vgpnk/.config/omarchy/current/theme/backgrounds/0-ship-at-sea.jpg`)

### Group 6: idle/lock plane
- `command -v hypridle hyprlock hyprsunset`: exit code `0`
  - `/usr/bin/hypridle` (rc=0)
  - `/usr/bin/hyprlock` (rc=0)
  - `/usr/bin/hyprsunset` (rc=0)

### Group 7: omarchy skill docs
- `test -d ~/.agents/skills/omarchy`: exit code `0`
- `omarchy version`: exit code `0` (`3.8.3`)
- `command -v omarchy`: exit code `0` (`/home/vgpnk/.local/share/omarchy/bin/omarchy`)
- `cat ~/.local/share/omarchy/version`: exit code `0` (`3.8.3`)
- `git -C ~/.local/share/omarchy describe --tags --always`: exit code `0` (`v3.8.4` at commit `8fcc9d604`)

### Group 8: windows desktop plane
- `command -v powershell.exe pwsh powershell`: exit code `1`
- `command -v powershell.exe`: exit code `1` (not found)
- `command -v pwsh`: exit code `1` (not found)
- `command -v powershell`: exit code `1` (not found)
- Observed state: absent on this Linux host (honest record).

---

## 4. Independent Comparison with `before-register-probes-r65.txt`

The baseline receipt `.ufo/waves/round-65/receipts/before-register-probes-r65.txt` was inspected only AFTER all probes above were recorded in `probes.log`.

### Agreements
- **100% agreement on all 7 omarchy Linux surface groups:**
  - Hyprland: version `0.56.2 built from branch v0.56.2 at commit efb50993780079460b0cbed1363e2166a2de1d9f clean`, date `Wed Aug 5 14:13:21 2026`.
  - Waybar: version `Waybar v0.15.0`, binary `/usr/bin/waybar`, config present.
  - Walker: version `2.17.2`, binary `/usr/bin/walker`, config present.
  - Terminal configs: `alacritty`, `foot`, `kitty`, `ghostty` all 4 present.
  - Theme/wallpaper: `~/.config/omarchy` and `~/.local/share/omarchy` present.
  - Idle/lock plane: `hypridle`, `hyprlock`, `hyprsunset` all 3 present in `/usr/bin/`.
  - Omarchy skill docs: `~/.agents/skills/omarchy` present; version `3.8.3`.
- **Agreements on extra receipt lines:**
  - `mako: PRESENT /usr/bin/mako`
  - `swayosd: ABSENT`
  - `grim: PRESENT /usr/bin/grim`
  - `slurp: PRESENT /usr/bin/slurp`

### Additional Independent Discoveries (Extending Beyond Before Receipt)
1. **Live Compositor Session:** `hyprctl instances` proves a live running compositor instance: `efb50993780079460b0cbed1363e2166a2de1d9f_1793632040_1005787507` (instance count = 1, pid 1665, socket `wayland-1`).
2. **Waybar Running Process:** `pgrep -x waybar` confirms 1 active process running under pid `1720`.
3. **Omarchy Version Nuance:** `~/.local/share/omarchy` is a git repository checked out at tag `v3.8.4` (`8fcc9d604 Merge branch 'master' into rc`), while the static tracked file `~/.local/share/omarchy/version` contains `3.8.3`. Thus, `omarchy version` prints `3.8.3`, reconciling the S097 source reference ("omarchy v3.8.4 matte-black theme payload") with the CLI version output `3.8.3`.
4. **Theme Configuration:** `theme.name` is `matte-black`; `background` points to `/home/vgpnk/.config/omarchy/current/theme/backgrounds/0-ship-at-sea.jpg`.
5. **Windows Desktop Plane:** Explicitly confirmed absent via `command -v powershell.exe pwsh powershell` (all rc=1).

### Disagreements
- **0 disagreements.** Every finding in `before-register-probes-r65.txt` re-derives identically.

---

## 5. Defects Seen

- **Live Host Environment:** Zero defects observed. All services, configs, binaries, and compositor instances are intact and consistent.
- **Base Repository State (`524fa1f9...`):** PROVINCE.md contains 7 stale rows in `### Surface state register (2026-10-31, this host)` stating that the 7 omarchy Linux surfaces were `absent (2026-10-31)` (recorded during the Windows host run era). This confirms the C1 deficiency stated in `claims-declaration-r65.md`.

---

## 6. Audit Trail & Receipts

- Raw probe execution log: `.ufo/waves/round-65/w1/R65ScoutSurfaces/probes.log`
- Tool installs/upgrades: None (all tools pre-installed on host; pacman paused).
- Scratch directory: `/fast/scratch/hyaku/mado-r65/w1/R65ScoutSurfaces/` (purged on completion).
