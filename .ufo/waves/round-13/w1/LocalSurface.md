# LocalSurface Scout Report — Mado Round 13 (Wave 1)

**Seat ID:** `MadoR13.LocalSurface`  
**Role:** Scout (leaf member — no subagent dispatch, no background jobs, no state mutation)  
**Target:** `/home/vgpnk/Projects/shokunin/mado-shokunin`  
**Status:** Complete  
**Date:** 2026-10-20  

---

## 1. Axes and Posture (Godspeed)

1. **Axes Named:**
   - **Coverage (C1):** Advancing sourced protocol-phase knowledge and advertised globals (3/7 → 4/7).
   - **Operability (C2):** Replacing set-blind Hypr source and local inventory counting checks with exact expected/observed set comparison, explicitly reporting named `missing:` and `extra:` path sets, covering hermetic test cases.

2. **Boundary and Posture:**
   - Pure read-only inspection of host names and declarations.
   - Zero state mutation: no edits to host config files, no daemon signals, no compositor restarts.
   - Zero secret inspection: no reading or echoing of secret config file contents, tokens, credentials, or private rules. Only file names, line counts, directive keywords, and literal include path strings are surveyed.
   - No verification suite execution mid-flight; L1 verifies once after all seats complete.

---

## 2. Host Surface Inventory: `~/.config/hypr/`

- **Directory Absolute Path:** `/home/vgpnk/.config/hypr`
- **Total Filesystem Entries:** 15 entries (13 active `.conf` files, 2 timestamped backup `.bak.*` files, 0 subdirectories, 0 hidden files).

### 2.1 Observed Active `.conf` Files (13 entries)

| # | Absolute Host Path | File Name | Size (Bytes) | Category / Role |
|---|---|---|---|---|
| 1 | `/home/vgpnk/.config/hypr/ai-usage.conf` | `ai-usage.conf` | 319 | Tray application window rules (`org.omarchy.ai-usage`) |
| 2 | `/home/vgpnk/.config/hypr/autostart.conf` | `autostart.conf` | 210 | Local autostart command definitions |
| 3 | `/home/vgpnk/.config/hypr/bindings.conf` | `bindings.conf` | 2,822 | Custom user keybindings |
| 4 | `/home/vgpnk/.config/hypr/envs.conf` | `envs.conf` | 133 | Environment variable overrides (orphan invariant F3) |
| 5 | `/home/vgpnk/.config/hypr/gkeep.conf` | `gkeep.conf` | 264 | Operator local notes window rules (from `~/Projects/gkeep`) |
| 6 | `/home/vgpnk/.config/hypr/hypridle.conf` | `hypridle.conf` | 765 | Hypridle idle-management daemon configuration |
| 7 | `/home/vgpnk/.config/hypr/hyprland.conf` | `hyprland.conf` | 1,329 | Root Hyprland orchestrator / include graph |
| 8 | `/home/vgpnk/.config/hypr/hyprlock.conf` | `hyprlock.conf` | 742 | Hyprlock screen-locking daemon configuration |
| 9 | `/home/vgpnk/.config/hypr/hyprsunset.conf` | `hyprsunset.conf` | 363 | Hyprsunset blue-light/gamma daemon configuration |
| 10 | `/home/vgpnk/.config/hypr/input.conf` | `input.conf` | 1,521 | Local device/keyboard/touchpad input configuration |
| 11 | `/home/vgpnk/.config/hypr/looknfeel.conf` | `looknfeel.conf` | 1,000 | Local appearance / decoration overrides |
| 12 | `/home/vgpnk/.config/hypr/monitors.conf` | `monitors.conf` | 1,012 | Display output resolutions, positions, refresh rates |
| 13 | `/home/vgpnk/.config/hypr/xdph.conf` | `xdph.conf` | 106 | XDG Desktop Portal Hyprland configuration |

### 2.2 Observed Inactive / Backup Files (2 entries)

| # | Absolute Host Path | File Name | Epoch Timestamp | Decoded UTC Timestamp |
|---|---|---|---|---|
| 1 | `/home/vgpnk/.config/hypr/autostart.conf.bak.1791942509` | `autostart.conf.bak.1791942509` | 1791942509 | 2026-10-14T01:48:29Z |
| 2 | `/home/vgpnk/.config/hypr/hyprland.conf.bak.1792267376` | `hyprland.conf.bak.1792267376` | 1792267376 | 2026-10-17T20:02:56Z |

---

## 3. Hyprland Root Source Declarations: `hyprland.conf`

- **Absolute Path:** `/home/vgpnk/.config/hypr/hyprland.conf`
- **Total Lines:** 32 lines
- **Total Source Declarations:** 18 lines matching `^[[:space:]]*source[[:space:]]*=`

### 3.1 Exact Ordered Source Declarations

| Line | Raw Directive in `hyprland.conf` | Sanitized Path / Glob | Target Kind | Host Target Resolution |
|---|---|---|---|---|
| 4 | `source = ~/.local/share/omarchy/default/hypr/autostart.conf` | `~/.local/share/omarchy/default/hypr/autostart.conf` | Omarchy default | Exists: `/home/vgpnk/.local/share/omarchy/default/hypr/autostart.conf` |
| 5 | `source = ~/.local/share/omarchy/default/hypr/bindings/media.conf` | `~/.local/share/omarchy/default/hypr/bindings/media.conf` | Omarchy default | Exists: `/home/vgpnk/.local/share/omarchy/default/hypr/bindings/media.conf` |
| 6 | `source = ~/.local/share/omarchy/default/hypr/bindings/clipboard.conf` | `~/.local/share/omarchy/default/hypr/bindings/clipboard.conf` | Omarchy default | Exists: `/home/vgpnk/.local/share/omarchy/default/hypr/bindings/clipboard.conf` |
| 7 | `source = ~/.local/share/omarchy/default/hypr/bindings/tiling-v2.conf` | `~/.local/share/omarchy/default/hypr/bindings/tiling-v2.conf` | Omarchy default | Exists: `/home/vgpnk/.local/share/omarchy/default/hypr/bindings/tiling-v2.conf` |
| 8 | `source = ~/.local/share/omarchy/default/hypr/bindings/utilities.conf` | `~/.local/share/omarchy/default/hypr/bindings/utilities.conf` | Omarchy default | Exists: `/home/vgpnk/.local/share/omarchy/default/hypr/bindings/utilities.conf` |
| 9 | `source = ~/.local/share/omarchy/default/hypr/envs.conf` | `~/.local/share/omarchy/default/hypr/envs.conf` | Omarchy default | Exists: `/home/vgpnk/.local/share/omarchy/default/hypr/envs.conf` |
| 10 | `source = ~/.local/share/omarchy/default/hypr/looknfeel.conf` | `~/.local/share/omarchy/default/hypr/looknfeel.conf` | Omarchy default | Exists: `/home/vgpnk/.local/share/omarchy/default/hypr/looknfeel.conf` |
| 11 | `source = ~/.local/share/omarchy/default/hypr/input.conf` | `~/.local/share/omarchy/default/hypr/input.conf` | Omarchy default | Exists: `/home/vgpnk/.local/share/omarchy/default/hypr/input.conf` |
| 12 | `source = ~/.local/share/omarchy/default/hypr/windows.conf` | `~/.local/share/omarchy/default/hypr/windows.conf` | Omarchy default | Exists: `/home/vgpnk/.local/share/omarchy/default/hypr/windows.conf` |
| 13 | `source = ~/.config/omarchy/current/theme/hyprland.conf` | `~/.config/omarchy/current/theme/hyprland.conf` | Current theme | Exists: `/home/vgpnk/.config/omarchy/current/theme/hyprland.conf` |
| 16 | `source = ~/.config/hypr/monitors.conf` | `~/.config/hypr/monitors.conf` | Local user config | Exists: `/home/vgpnk/.config/hypr/monitors.conf` |
| 17 | `source = ~/.config/hypr/input.conf` | `~/.config/hypr/input.conf` | Local user config | Exists: `/home/vgpnk/.config/hypr/input.conf` |
| 18 | `source = ~/.config/hypr/bindings.conf` | `~/.config/hypr/bindings.conf` | Local user config | Exists: `/home/vgpnk/.config/hypr/bindings.conf` |
| 19 | `source = ~/.config/hypr/looknfeel.conf` | `~/.config/hypr/looknfeel.conf` | Local user config | Exists: `/home/vgpnk/.config/hypr/looknfeel.conf` |
| 20 | `source = ~/.config/hypr/autostart.conf` | `~/.config/hypr/autostart.conf` | Local user config | Exists: `/home/vgpnk/.config/hypr/autostart.conf` |
| 23 | `source = ~/.local/state/omarchy/toggles/hypr/*.conf` | `~/.local/state/omarchy/toggles/hypr/*.conf` | Dynamic toggles (glob) | Resolves to 2 files: `window-no-gaps.conf`, `flags.conf` |
| 29 | `source = ~/.config/hypr/ai-usage.conf` | `~/.config/hypr/ai-usage.conf` | Local tray app | Exists: `/home/vgpnk/.config/hypr/ai-usage.conf` |
| 32 | `source = ~/.config/hypr/gkeep.conf` | `~/.config/hypr/gkeep.conf` | Local operator notes | Exists: `/home/vgpnk/.config/hypr/gkeep.conf` |

### 3.2 Target Resolution Analysis
- **Static File Targets:** 17 targets; all 17 resolve to existing regular files.
- **Glob Target:** 1 target (`~/.local/state/omarchy/toggles/hypr/*.conf`); resolves to 2 existing files under `/home/vgpnk/.local/state/omarchy/toggles/hypr/`:
  - `/home/vgpnk/.local/state/omarchy/toggles/hypr/window-no-gaps.conf`
  - `/home/vgpnk/.local/state/omarchy/toggles/hypr/flags.conf`
- **Total Resolution Ratio:** 18/18 targets resolve under root.

---

## 4. Exact Set Comparison: Baseline vs Observed

### 4.1 Local `.conf` Inventory (`hypr.local.inventory`)

- **Baseline Expected Set** (`tools/mado-verify.sh:2263` `LOCAL` array):
  $$\text{Expected}_{\text{baseline}} = \{ \text{ai-usage.conf}, \text{autostart.conf}, \text{bindings.conf}, \text{envs.conf}, \text{hypridle.conf}, \text{hyprland.conf}, \text{hyprlock.conf}, \text{hyprsunset.conf}, \text{input.conf}, \text{looknfeel.conf}, \text{monitors.conf}, \text{xdph.conf} \}$$
  $$\text{Count} = 12$$

- **Observed Host Set** (all `*.conf` in `/home/vgpnk/.config/hypr`):
  $$\text{Observed}_{\text{host}} = \{ \text{ai-usage.conf}, \text{autostart.conf}, \text{bindings.conf}, \text{envs.conf}, \mathbf{gkeep.conf}, \text{hypridle.conf}, \text{hyprland.conf}, \text{hyprlock.conf}, \text{hyprsunset.conf}, \text{input.conf}, \text{looknfeel.conf}, \text{monitors.conf}, \text{xdph.conf} \}$$
  $$\text{Count} = 13$$

- **Set Difference Analysis:**
  - $\text{Missing} = \text{Expected}_{\text{baseline}} \setminus \text{Observed}_{\text{host}} = \emptyset$
  - $\text{Extra} = \text{Observed}_{\text{host}} \setminus \text{Expected}_{\text{baseline}} = \{ \mathbf{gkeep.conf} \}$

- **The Set-Blind Defect (Mistake M13):**
  In the baseline verifier (`tools/mado-verify.sh:2266-2273`), the check was:
  ```bash
  for x in "${LOCAL[@]}"; do
    if [ -f "$H/$x.conf" ]; then n=$((n + 1)); else lmiss="$lmiss $x.conf"; fi
  done
  if [ -z "$lmiss" ]; then
    row hypr hypr.local.inventory PASS "$n/${#LOCAL[@]} active local confs"
  ...
  ```
  Because all 12 members of `LOCAL` exist, `lmiss` was empty, and the check emitted `PASS 12/12 active local confs`. It was completely blind to the presence of unlisted files in `~/.config/hypr/` (such as `gkeep.conf` or any arbitrary `extra.conf`).

- **C2 Target Contract:**
  The expected local set must include all 13 active configuration files:
  $$\text{Expected}_{\text{R13}} = \text{Observed}_{\text{host}} \quad (\text{13 files})$$
  The gate must compute symmetric set differences:
  - If $\text{missing} \neq \emptyset$, report `missing: <paths>`
  - If $\text{extra} \neq \emptyset$, report `extra: <paths>`
  - Exact match reports `PASS 13/13 active local confs`.

### 4.2 Hyprland Root Sources (`hypr.root.sources_resolve` & `hypr.root.include_graph`)

- **Expected Sources Set (`EXPECT`):**
  18 source targets declared in `tools/mado-verify.sh:2203-2221`.
- **Observed Sources Set in `hyprland.conf`:**
  18 source targets parsed from `/home/vgpnk/.config/hypr/hyprland.conf`.
- **Set Difference:**
  - $\text{Missing} = \emptyset$
  - $\text{Extra} = \emptyset$
  - Order: exact 1-to-1 match across all 18 entries.

- **The Set-Blind Defect in `sources_resolve`:**
  Baseline `sources_resolve` only checked `for t in "${EXPECT[@]}"` to see whether target files existed on disk. If a source line was substituted or added in `hyprland.conf` (e.g. `replacement.conf` instead of `ai-usage.conf`), but the target `ai-usage.conf` still existed on disk, baseline `sources_resolve` returned `PASS 18/18 targets exist`.
  Under C2 operability, `sources_resolve` must compare the set of declared sources against the expected set and check existence, reporting `FAIL missing: ... extra: ...` when substitution occurs (as verified by `measure.py` scenario `replace-source`).

---

## 5. Hermetic Test Cases Coverage (for `measure.py` & Selftest)

The exact set comparison logic must correctly detect and report the following hermetic scenarios:

1. **`extra-local`:**
   - Perturbation: Create `/tmp/.../.config/hypr/extra.conf`
   - Expected Result: `hypr.local.inventory` emits `FAIL` containing `extra: extra.conf`.
2. **`replace-local`:**
   - Perturbation: Delete `xdph.conf` and create `extra.conf`
   - Expected Result: `hypr.local.inventory` emits `FAIL` containing `missing: xdph.conf extra: extra.conf`.
3. **`missing-gkeep`:**
   - Perturbation: Delete `gkeep.conf`
   - Expected Result: `hypr.local.inventory` emits `FAIL` containing `missing: gkeep.conf`.
4. **`replace-source`:**
   - Perturbation: Replace `~/.config/hypr/ai-usage.conf` with `~/.config/hypr/replacement.conf` in `hyprland.conf` and create `replacement.conf`
   - Expected Result: `hypr.root.sources_resolve` emits `FAIL` containing `missing: ~/.config/hypr/ai-usage.conf extra: ~/.config/hypr/replacement.conf`.

---

## 6. Sourced Anchors and Primary References

1. **Gate Re-anchor & Local Inventory Definition:**
   - **Source Identifier:** S014 (`tools/mado-verify.sh`)
   - **Path:** `/home/vgpnk/Projects/shokunin/mado-shokunin/tools/mado-verify.sh:2193-2274`
   - **Access Date:** 2026-10-20
   - **Tier:** Tier A (own-work)
   - **Exact Quote (≤ 25 words):** "17→18 source lines (+ ~/.config/hypr/gkeep.conf after ai-usage.conf; root sha 4f52854a3c143dcf… → ce7483f35ab52bc2…) after the operator-applied gkeep installer;" (`:2193-2195`)
   - **Disposition:** Mined. Demonstrates where the EXPECT array was expanded to 18 while LOCAL remained count-only at 12.

2. **Operator Installer Provenance:**
   - **Source Identifier:** S013 (`/home/vgpnk/Projects/gkeep/install.sh`)
   - **Path:** `/home/vgpnk/Projects/gkeep/install.sh:34`
   - **Revision:** Git commit `133b86717a02548aeaff3f1411bf301d936c5308`
   - **Access Date:** 2026-10-20
   - **Tier:** Tier A (code)
   - **Exact Quote (≤ 25 words):** `main_text += "\n# gkeep local notes\nsource = ~/.config/hypr/gkeep.conf\n"` (`install.sh:34`)
   - **Disposition:** Mined. Proves external operator provenance of `gkeep.conf` and its insertion point directly after `ai-usage.conf`.

3. **Multi-file Sourcing Semantics:**
   - **URL:** `https://wiki.hypr.land/Configuring/Keywords/#sourcing-multi-file`
   - **Access Date:** 2026-10-20
   - **Anchor:** `#sourcing-multi-file`
   - **Tier:** Tier A (docs)
   - **Exact Quote (≤ 25 words):** "You can use the source keyword to source other files, for example your colors generated by pywal."
   - **Admission / Flip:** Admitted. Confirms that `source =` statements load external config files into the orchestrator scope and that wildcards expand at load time.

---

## 7. Tooling Record

- **Tooling Directive Compliance:**
  No tools were installed or upgraded during this scouting execution.
  Standard system coreutils (`find`, `awk`, `grep`), bash, and read-only tools were sufficient for complete path census and declaration analysis.
