# R56ScoutOmarchy — host recon: how omarchy on this host interacts with Hyprland reload

Seat: R56ScoutOmarchy (leaf, no subagents). Date: 2026-10-28. Read-only; no git/jj operation, no write outside
`.ufo/waves/round-56/w1/R56ScoutOmarchy{,.md}` and scratch `/fast/scratch/hyaku/mado-r56/R56ScoutOmarchy/` (empty, removed).
No tool installs (none needed; the pacman guard was never touched). Frozen contract read first (claims-frozen.md,
registration.md); this seat feeds C1/C2 ground truth only — no claim is scored here.

## 1. Host state observed (read-only)

```
$ hyprctl version -j          → "branch": "v0.56.2", "commit": "efb50993780079460b0cbed1363e2166a2de1d9f",
                                "version": "0.56.2", "tag": "v0.56.2"
$ hyprctl getoption misc:disable_autoreload -j
→ {"option": "misc:disable_autoreload", "int": 0, "set": false }
```

Running compositor is exactly the frozen C1 pin commit (efb5099…, v0.56.2). `misc:disable_autoreload` is unset, value 0
→ **auto-reload is ON** on this host.

`disable_autoreload` grep over `~/.local/share/omarchy` and `~/.config/omarchy`: **0 matches** — omarchy never sets
`misc:disable_autoreload` in a file or via `hyprctl keyword`. Only `hyprctl keyword debug:suppress_errors true`
(omarchy-update-git:12) and device/layout/cursor keywords (below) are used.

### 1a. Every `source =` target of ~/.config/hypr/hyprland.conf — symlink shape

Live `/home/vgpnk/.config/hypr/hyprland.conf` sources (lines 4–24):

```
source = ~/.local/share/omarchy/default/hypr/autostart.conf
source = ~/.local/share/omarchy/default/hypr/bindings/media.conf
source = ~/.local/share/omarchy/default/hypr/bindings/clipboard.conf
source = ~/.local/share/omarchy/default/hypr/bindings/tiling-v2.conf
source = ~/.local/share/omarchy/default/hypr/bindings/utilities.conf
source = ~/.local/share/omarchy/default/hypr/envs.conf
source = ~/.local/share/omarchy/default/hypr/looknfeel.conf
source = ~/.local/share/omarchy/default/hypr/input.conf
source = ~/.local/share/omarchy/default/hypr/windows.conf
source = ~/.config/omarchy/current/theme/hyprland.conf
source = ~/.config/hypr/monitors.conf
source = ~/.config/hypr/input.conf
source = ~/.config/hypr/bindings.conf
source = ~/.config/hypr/looknfeel.conf
source = ~/.config/hypr/autostart.conf
source = ~/.local/state/omarchy/toggles/hypr/*.conf        (glob)
source = ~/.config/hypr/ai-usage.conf
source = ~/.config/hypr/gkeep.conf
```

`stat -c '%N'` + `readlink -f` over all 17 static targets and over the glob expansion
(`~/.local/state/omarchy/toggles/hypr/` currently holds exactly `flags.conf` and `window-no-gaps.conf`):

**None of them is a symlink.** Every stat prints a plain quoted path with no ` -> ` target and every `readlink -f`
is the identity (`stat` output e.g. `'/home/vgpnk/.config/omarchy/current/theme/hyprland.conf'`). The parent dirs
`~/.config/omarchy/current`, `~/.config/omarchy/current/theme`, `~/.local/state/omarchy/toggles/hypr` are real
directories. Shape consequence for the C2 model: **the canonical-symlink second watch would fire for zero source
targets on this host today.** Note `current/theme` is a real dir maintained by rename swap (see row 2), so the
watched file `current/theme/hyprland.conf` gets a NEW inode on every theme set — omarchy follows that swap with an
explicit reload, which bounds the stale-watch window.

### 1b. Files under ~/.config/hypr NOT watched by the compositor

`hyprlock.conf`, `hypridle.conf`, `hyprsunset.conf`, `xdph.conf`, `apps/{system,terminals}.conf`, `*.bak*` — none is
sourced by hyprland.conf. `~/.config/hypr/envs.conf` is **also not sourced** (the sourced envs.conf is the default
under `~/.local/share/omarchy/default/hypr/envs.conf`) — see defect note D1.

## 2. Greps run (patterns → where)

`hyprctl reload`, `disable_autoreload`, `hyprctl keyword`, `hyprland\.conf`, `toggles`, `current/theme|themes/`,
`\.config/hypr`, `ai-usage|gkeep`, `monitors\.conf|bindings\.conf|input\.conf|looknfeel\.conf|autostart\.conf`,
`ln -s[^#]*hypr`, `omarchy-migrate|omarchy-reinstall-configs` over `~/.local/share/omarchy` (bin, default/hypr,
config, install, migrations, config/systemd) and `~/.config/omarchy`. All hits were read in context; every writer of
a watched file is in the tables below.

## 3. MAIN TABLE — scripts that write a file Hyprland is watching (sourced set above)

Write-style key: **truncate** = open/overwrite same inode (`cp`, `>`, `>>`); **rename** = temp/other name moved over
the path, new inode (`sed -i`, `mv`, git checkout); **create/delete** = new or removed path inside the toggles glob
dir.

| script (bin/ unless noted) | file written (watched) | write style | explicit reload follows | evidence (file:line + quote) |
|---|---|---|---|---|
| omarchy-refresh-config (invoked by omarchy-refresh-hyprland for the 6 user confs) | `~/.config/hypr/{autostart,bindings,input,looknfeel,hyprland,monitors}.conf` | truncate (`cp -f` dest overwrite; timestamped `.bak` cp first) | **NO** — no `hyprctl reload` in refresh-config nor in omarchy-refresh-hyprland (11-line file); relies on auto-reload | `bin/omarchy-refresh-config:29` `cp -f "$user_config_file" "$backup_config_file" 2>/dev/null`; `:32` `cp -f "$default_config_file" "$user_config_file" 2>/dev/null`; `:43` same cp when dest missing; `bin/omarchy-refresh-hyprland:5-10` `omarchy-refresh-config hypr/autostart.conf` … `hypr/monitors.conf` |
| omarchy-theme-set | `~/.config/omarchy/current/theme/hyprland.conf` (+ all theme files) | **rename (dir swap)**: staged into `current/next-theme` (`cp -r`, plus `sed -f` template render into next-theme), then `rm -rf current/theme` + `mv next-theme current/theme`; `theme.name` via `echo >` (unwatched) | **YES** — calls omarchy-restart-hyprctl, i.e. `hyprctl reload` | `bin/omarchy-theme-set:41` `rm -rf "$CURRENT_THEME_PATH"`; `:42` `mv "$NEXT_THEME_PATH" "$CURRENT_THEME_PATH"`; `:58` `omarchy-restart-hyprctl`; `bin/omarchy-restart-hyprctl:5` `hyprctl reload >/dev/null` |
| omarchy-restart-hyprctl | — (it IS the reload primitive used by theme switching) | — | — | `bin/omarchy-restart-hyprctl:5` `hyprctl reload >/dev/null` |
| omarchy-hyprland-toggle | `~/.local/state/omarchy/toggles/hypr/<flag>.conf` | delete (`rm $FLAG`) when on→off; create/truncate (`cp $FLAG_SOURCE $FLAG`) when off→on; source of copy: `default/hypr/toggles/<flag>.conf` (dir holds `flags.conf`, `window-no-gaps.conf`, `single-window-aspect-ratio.conf`) | **YES** `hyprctl reload` at end | `bin/omarchy-hyprland-toggle:21` `rm $FLAG`; `:24` `cp $FLAG_SOURCE $FLAG`; `:32` `hyprctl reload` |
| omarchy-hyprland-monitor-internal | `toggles/hypr/internal-monitor-disable.conf` | create via redirection `echo >` | **YES** on disable branch; enable/recover delegate to omarchy-hyprland-toggle (which reloads) | `bin/omarchy-hyprland-monitor-internal:25` `echo "monitor=$INTERNAL,disable" >"$TOGGLE_FLAG"`; `:27` `hyprctl reload` |
| omarchy-hyprland-monitor-internal-mirror | `toggles/hypr/internal-monitor-mirror.conf` | create via redirection `echo >` | **YES** on enable branch; disable delegates to omarchy-hyprland-toggle | `bin/omarchy-hyprland-monitor-internal-mirror:31` `echo "monitor=$EXTERNAL, preferred, auto, 1, mirror, $INTERNAL" > "$TOGGLE_FLAG"`; `:33` `hyprctl reload` |
| omarchy-hw-recover-internal-monitor | `toggles/hypr/internal-monitor-disable.conf` | delete (`rm -f`) | **NO** reload; runs as user oneshot `omarchy-recover-internal-monitor.service` (watcher `omarchy-hyprland-monitor-watch` listens on Hyprland socket2) | `bin/omarchy-hw-recover-internal-monitor:8` `rm -f "$TOGGLE"`; `config/systemd/user/omarchy-recover-internal-monitor.service:4` `ConditionPathExists=%h/.local/state/omarchy/toggles/hypr/internal-monitor-disable.conf` |
| omarchy-toggle-touchpad | `toggles/hypr/touchpad-disabled.conf` | create via `printf >` (disable); delete `rm -f` (enable) | **NO** — applies immediately with `hyprctl keyword` right before the file write; file is persistence for the next reload/login only | `bin/omarchy-toggle-touchpad:16` `hyprctl keyword "device[$device]:enabled" true >/dev/null`; `:17` `rm -f "$STATE_CONF"`; `:22` `hyprctl keyword … false >/dev/null`; `:24` `printf 'device {\n    name = %s\n    enabled = false\n}\n' "$device" > "$STATE_CONF"` |
| omarchy-toggle-touchscreen | `toggles/hypr/touchscreen-disabled.conf` | same printf >/rm -f pair | **NO** — same keyword-instead pattern | `bin/omarchy-toggle-touchscreen:16,17,22,24` (same lines as touchpad, `touch-disabled-symbolic`) |
| omarchy-remove-preinstalls | `~/.config/hypr/bindings.conf` | truncate (`cp`; `.bak` cp first) | **YES** | `bin/omarchy-remove-preinstalls:11` `cp ~/.config/hypr/bindings.conf ~/.config/hypr/bindings.conf.bak`; `:12` `cp "$OMARCHY_PATH/default/hypr/plain-bindings.conf" ~/.config/hypr/bindings.conf`; `:13` `hyprctl reload` |
| omarchy-update-git | every tracked watched file under `~/.local/share/omarchy` — note `default/hypr/*.conf` and `default/hypr/bindings/*.conf` are sourced DIRECTLY from this git working tree | **rename (git)**: `git pull --autostash` writes via lockfile+rename | **YES** — and pre-shields with a keyword | `bin/omarchy-update-git:12` `hyprctl keyword debug:suppress_errors true &>/dev/null \|\| true`; `:14` `git -C $OMARCHY_PATH pull --autostash`; `:17` `hyprctl reload &>/dev/null \|\| true` |
| omarchy-hyprland-monitor-scaling-cycle | `~/.config/hypr/monitors.conf` | rename (`sed -i -E`), guarded: only when exactly one catch-all `monitor=,preferred,auto,` line exists | **NO** — relies on auto-reload | `bin/omarchy-hyprland-monitor-scaling-cycle:39` `MONITOR_CONF="$HOME/.config/hypr/monitors.conf"`; `:43` `sed -i -E "s\|^(monitor=,preferred,auto,).*\|\1${NEW_SCALE}|" "$MONITOR_CONF"` |
| omarchy-migrate → migrations/*.sh (~20 touch watched files) | `~/.config/hypr/bindings.conf`, `input.conf`, `monitors.conf`, `looknfeel.conf`, `autostart.conf`, `hyprland.conf` | **rename** (`sed -i` / `sed -Ei`) in most; truncate `cp` in 1757879836.sh:4 and 1760462260.sh:15 (backups); **append** `echo >>` in 1776410469.sh:8; `cp $OMARCHY_PATH/config/hypr/looknfeel.conf` create-if-missing in 1757879836.sh:4 | **NO** `hyprctl reload` in ANY migration, and none in the callers after them — see ordering note below | see §4 |
| install/config/omarchy-toggles.sh | `toggles/hypr/flags.conf` | create/truncate (`cp`, `mkdir -p` first) | **NO** (its only in-tree caller, migration 1776410469.sh, has no reload either) | `install/config/omarchy-toggles.sh:2` `mkdir -p ~/.local/state/omarchy/toggles/hypr`; `:3` `cp $OMARCHY_PATH/default/hypr/toggles/flags.conf ~/.local/state/omarchy/toggles/hypr/` |
| migration 1776410469.sh | `~/.config/hypr/hyprland.conf` | **append** `echo -e … >>` (idempotence-guarded by grep) | **NO** | `migrations/1776410469.sh:8` `echo -e "\n# Toggle config flags dynamically\nsource = ~/.local/state/omarchy/toggles/hypr/*.conf" >> "$HYPR_CONF"` |
| install/config/detect-keyboard-layout.sh | `~/.config/hypr/input.conf` | rename (`sed -i` insert of `kb_layout`/`kb_variant`) | **NO** (runs as the last step of omarchy-refresh-hyprland, which reloads nothing) | `install/config/detect-keyboard-layout.sh:8` `sed -i "/^[[:space:]]*kb_options *=/i\  kb_layout = $layout" "$hyprconf"`; `:13` same for `kb_variant` |
| omarchy-reinstall-configs (nuclear reset) | everything under `~/.config/` incl. all watched `~/.config/hypr/*` | truncate (`cp -R` overwrite) | **NO** reload; flow ends with `install/config/theme.sh` (→ omarchy-theme-set, which does reload) and omarchy-reinstall:17 offers reboot | `bin/omarchy-reinstall-configs:14` `cp -R ~/.local/share/omarchy/config/* ~/.config/` |
| install/hardware/nvidia.sh | `~/.config/hypr/envs.conf` | **append** (`cat >> … <<EOF`) / `sed -i` delete-lines | **NO** — prints "Please restart Hyprland for changes to take effect." — but see D1: this path is NOT sourced, so Hyprland is not watching it | `install/hardware/nvidia.sh:33` and `:42` `cat >>"$HOME/.config/hypr/envs.conf" <<'EOF'` |

Keyword-only (runtime state, no config file written): `omarchy-hyprland-workspace-layout-toggle:13`
(`hyprctl keyword workspace $ACTIVE_WORKSPACE, layout:$NEW_LAYOUT`), `omarchy-screensaver:10,21`
(`cursor:invisible`), `omarchy-update-perform:9` (`hyprctl dispatch tagwindow +noidle`),
`omarchy-update-git:12` (see above). Default bindings also invoke `hyprctl keyword` at runtime
(`default/hypr/bindings/utilities.conf:72-73`, cursor zoom).

## 4. Migration detail (all `sed -i` = temp-file + rename onto the watched path; NO migration reloads)

migrations/1755507891.sh:17-18 (bindings.conf) · 1755870033.sh:4 (bindings) · 1757866485.sh:4-5 (bindings) ·
1757877123.sh:6 (bindings) · 1757877852.sh:4,5,7,8,9 (bindings) · 1757879836.sh:4 (cp looknfeel.conf),
:9 (`sed -i … a source = ~/.config/hypr/looknfeel.conf` on hyprland.conf) · 1758019332.sh:10 (input), :15,:20
(bindings) · 1760462260.sh:15 (cp backup bindings), :17-22 (bindings), :24-25 (hyprland.conf source-line swap) ·
1762121828.sh:36,38 (bindings) · 1763386443.sh:4 (bindings) · 1767138576.sh:4-6 (input) + :10
(`omarchy-state set reboot-required`) · 1769543550.sh:5 (bindings) · 1770375655.sh:4 (bindings) ·
1771606249.sh:4-6 (input) + :8 (`omarchy-state set reboot-required`) · 1771847961.sh:6 (bindings) ·
1772293693.sh:6-9 (looknfeel) · 1776434586.sh:23-28 (bindings) · 1776781957.sh:6 (monitors) ·
1778008689.sh:4 (input) · 1778171768.sh:7 (autostart, then `pkill -x swayosd-server`).

**Ordering note (observed from script text, not from a live run):** `omarchy-update` → `omarchy-update-git` (its
line 17 reload fires here) → `omarchy-update-perform:15` `omarchy-migrate` runs the migrations AFTER that reload.
Neither `omarchy-update-perform` nor `omarchy-update-restart` calls `hyprctl reload`; `omarchy-update-restart`
instead prompts a reboot when `~/.local/state/omarchy/reboot-required` exists (set by migrations 1767138576.sh:10
and 1771606249.sh:8) or when the running Hyprland binary is `(deleted)`. So migration edits reach the compositor
via **auto-reload (or a reboot), never via an explicit omarchy reload**.

## 5. Secondary table — hypr-family writes NOT watched by the compositor (completeness)

| script / migration | file (unwatched) | style | reload/restart | evidence |
|---|---|---|---|---|
| omarchy-font-set:29 | hyprlock.conf | `sed -i "s/font_family = .*/…/"` | none | line 29 |
| omarchy-setup-security-fingerprint:47-48 / omarchy-remove-security-fingerprint:25-26 | hyprlock.conf | `sed -i` | none | lines as cited |
| migrations 1762684663.sh:9, 1762685081.sh:8,11, 1764378788.sh:4, 1770372978.sh:4 | hyprlock.conf | `sed -i` (+ cp backup 1762684663:6, 1762685081:3) | none | as cited |
| migration 1767414310.sh:3 | hypridle.conf | `sed -i 's/timeout = 300/timeout = 151/'` | none | line 3 |
| migration 1771618300.sh:2 | hypridle.conf | `cp $OMARCHY_PATH/config/hypr/hypridle.conf ~/.config/hypr/hypridle.conf` | none | line 2 |
| migration 1777467659.sh:4-5 | hypridle.conf | `sed -i` | `omarchy-restart-hypridle` | lines 4-5 |
| migration 1763478660.sh:3-4 | xdph.conf | `cp` | `systemctl --user restart xdg-desktop-portal-hyprland` | lines 3-4 |
| migration 1765587218.sh:8 | xdph.conf | `sed -i` | `sleep 1` | line 8 |
| migrations 1762121828.sh:53-56, 1778008689.sh:8 | `~/.config/hypr/apps/{system,terminals}.conf` | `sed -i` | none | as cited |
| install/login/sddm.sh:7, migration 1778148645.sh:3 | `/usr/share/sddm/hyprland.conf` | `sudo cp` | separate sddm session | as cited |
| omarchy-menu:272,326-328,463-465 | watched files but via `open_in_editor` | user-driven `$EDITOR` | user-driven | as cited |

`ai-usage.conf` and `gkeep.conf` are sourced and therefore watched, but **no writer exists anywhere in either
omarchy tree** (grep `ai-usage|gkeep` → only the `source =` lines themselves). Their writers are external tools
(names suggest omarchy-usage-tray / gkeep), not present under `~/.local/share/omarchy` or `~/.config/omarchy`.

## 6. Findings most relevant to C1/C2 (recon only; no claim scored)

1. Auto-reload is live on this host (`misc:disable_autoreload` int=0, set=false) and omarchy never disables it; a
   large fraction of omarchy's own writers (refresh path, scaling persist, ALL migrations, recover path) depend on
   it, while the interactive toggles/theme/update paths add an explicit `hyprctl reload` anyway.
2. Mixed write styles land on the same watched files: `cp`/`>` truncate the existing inode, `sed -i`/`mv`/git
   rename a fresh inode over the path, and the toggles glob dir sees create/delete. `omarchy-theme-set` swaps the
   whole `current/theme` directory by rename. These are exactly the cases a watch-list predictor must not conflate.
3. Zero symlinks anywhere in today's source set → the `role=canonical` second watch is currently unreachable on
   this host (shape evidence in §1a).

## 7. Defects / ambiguities in the input, with evidence

- **D1 (omarchy, not lane):** `install/hardware/nvidia.sh:33,42` and `migrations/1770159912.sh` append/sed
  `~/.config/hypr/envs.conf`, but the live hyprland.conf sources `~/.local/share/omarchy/default/hypr/envs.conf`
  and never `~/.config/hypr/envs.conf` — those NVIDIA edits are invisible to the running compositor (script even
  says "restart Hyprland", which would not help unless the user re-sources it). Could not determine whether an
  unsourced user `envs.conf` is intended as a manual-override convention; the default template
  (`~/.local/share/omarchy/config/hypr/hyprland.conf:6`) also sources the default path only.
- **D2:** sourced-but-unattributed files `ai-usage.conf`, `gkeep.conf` — writers unknown (§5).
- **D3 (seat-spec ambiguity):** the seat names "toggles under ~/.local/state/omarchy/toggles/hypr"; the HOST read
  allowlist does not list `~/.local/state`, while registration.md's seat boundaries list bare `stat`. I took the
  literal intersection: shape only (`stat -c '%N'`, `readlink -f`, glob-for-stat listing of the directory); the
  CONTENTS of `flags.conf` / `window-no-gaps.conf` were NOT read.
- **D4 (tool-harness artifact):** three early supervised bash runs (hyprctl getoption/version, first stat batch)
  expired before their output could be reaped (`proc://<pid>` → "not found"); each was re-run successfully and all
  decisive outputs above are from the successful runs. Nothing was inferred from the lost outputs.

## 8. Not verified / not run

- No `hyprctl keyword|dispatch|reload` was ever executed (host guard); keyword usages above are quoted from script
  text only.
- No live update/migration/theme-set was performed, so the ordering note in §4 is script-text analysis, not an
  observed run. Runtime behavior of inotify events (which style actually wakes the watcher) was not observed —
  that is C1/C2 territory.
- Scratch dir held only transient emptiness; removed at close. Deliverable dir
  `.ufo/waves/round-56/w1/R56ScoutOmarchy/` exists and is intentionally empty (no fixtures/receipts produced).
