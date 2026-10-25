# SctHostTree — round 39 (hyaku run 7, 2026-10-25)

Seat: `SctHostTree` (scout). Scope: **read-only capture of the host Hyprland config tree
bytes into evidence**, plus a sha256 manifest of every copied file.

No host mutation. No socket connect. No package transaction. No lane index touched.
Nothing was written outside this seat directory and this report file.

## 1. What was captured

Destination (lane-local, created by this seat):

```
/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-39/w1/SctHostTree/real-tree/
```

Layout preserves the host-relative path under `$HOME`, so every manifest row maps 1:1 onto
the host path it was copied from (`<real-tree>/<rel>` ⇄ `$HOME/<rel>`).

| host source | files copied | note |
|---|---|---|
| `~/.config/hypr/*.conf` | 13 | all `*.conf` incl. `hyprland.conf`, `bindings.conf`, `input.conf`, `monitors.conf`, `looknfeel.conf`, `autostart.conf`, `envs.conf`, `ai-usage.conf`, `gkeep.conf`, `hypridle.conf`, `hyprlock.conf`, `hyprsunset.conf`, `xdph.conf` |
| `~/.local/share/omarchy/default/hypr/*.conf` | 8 | `apps.conf`, `autostart.conf`, `bindings.conf`, `envs.conf`, `input.conf`, `looknfeel.conf`, `plain-bindings.conf`, `windows.conf` |
| `~/.local/share/omarchy/default/hypr/apps/*.conf` | 19 | per-app files (incl. `davinci-resolve.conf`, `terminals.conf`, `typora.conf`, `walker.conf`, `webcam-overlay.conf`, …) |
| `~/.local/share/omarchy/default/hypr/bindings/*.conf` | 5 | `clipboard.conf`, `media.conf`, `tiling.conf`, `tiling-v2.conf`, `utilities.conf` |
| `~/.local/share/omarchy/default/hypr/toggles/*.conf` | 3 | `flags.conf`, `single-window-aspect-ratio.conf`, `window-no-gaps.conf` |
| `~/.local/state/omarchy/toggles/hypr/*.conf` | 2 | the **toggles glob** target of `hyprland.conf:23` (`source = ~/.local/state/omarchy/toggles/hypr/*.conf`) — `flags.conf`, `window-no-gaps.conf` |
| `~/.config/omarchy/current/theme/{hyprland.conf,hyprlock.conf,gum.env.conf}` | 3 | reachable theme files named by `source =` directives (`hyprland.conf:11`, `hyprlock.conf:1`, `default/hypr/envs.conf:1`) |

**Total copied: 53 regular files, 56 372 bytes** (`du -sb` of the seat dir incl. manifest).
Only 3 of the 24 files in `~/.config/omarchy/current/theme/` were copied — the three that a
`source =` directive actually names; the rest are terminal/app theme files unrelated to the
Hyprland source graph and were deliberately not copied.

### Deliberately excluded (recorded, not copied)

`~/.config/hypr/` holds two non-`*.conf` backup files. They do not match the `*.conf`
glob and are not named by any `source =` directive; they were **not** copied. Their hashes
are recorded here so the exclusion is auditable:

```
8b472371e78b7f8b9656b53bfe2290ff1f96b14e90bb063ebe1e3316437057ed  ~/.config/hypr/autostart.conf.bak.1791942509   (65 B)
4f52854a3c143dcf58430a679e339619223d2b5008115a322d06b2de637ea462  ~/.config/hypr/hyprland.conf.bak.1792267376   (1273 B)
```

No symlink, device, FIFO or socket exists anywhere in the four captured host trees
(`find … -printf '%y'` → `f` for all 80 entries; `non-regular []`). `~/.config/hypr` and
`~/.local/share/omarchy/default/hypr` are real directories, not symlinks
(`readlink -f` resolves to themselves).

## 2. The sha256 manifest

`/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-39/w1/SctHostTree/manifest.sha256`
— 53 rows, `<sha256>  <host-relative path>`, sorted by path, `sha256sum -c` compatible
from inside `real-tree/`.

```
sha256sum manifest.sha256 →
08be94e527843e4a8e8b0f4d976fded74c1edb23de64126ddf415520f35291a3
```

Generation and verification commands:

```bash
cd <seat>/real-tree
find . -type f -printf '%P\n' | sort | while read -r f; do
  printf '%s  %s\n' "$(sha256sum "$f" | cut -d' ' -f1)" "$f"
done > <seat>/manifest.sha256
```

* `sha256sum -c manifest.sha256` → **exit 0**, `53` rows `: OK`, `0` non-OK rows.
* Independent three-way equality check (Python `hashlib`): for all 53 rows
  `manifest_hash == sha256(host_path) == sha256(copied_path)` → **0 mismatches**.
* Independent cross-check against the sibling seat `ExecOptionsRealTree/host-src.sha256`
  (49 rows, same host): **common 49, agree 49, disagree 0**. My manifest is a strict
  superset (+4): `default/hypr/plain-bindings.conf` and the three
  `default/hypr/toggles/*.conf` files, which that capture omitted. The 49 overlapping
  rows are byte-identical hashes, so the two captures agree on the host state.

## 3. Host-immutability proof (before / after)

A pre-copy inventory of **all 80 regular files** in the four host trees
(`~/.config/hypr`, `~/.local/share/omarchy/default/hypr`, `~/.local/state/omarchy/toggles/hypr`,
`~/.config/omarchy/current/theme`) was taken *before* the copy — sha256, size, `st_mtime_ns`,
`st_ino`, mode. Re-read **after** the copy:

* **files re-read: 80, content changed: 0**
* **inode/mtime changed: 0**
* Host directory mtimes unchanged:
  * `~/.config/hypr` → `2026-10-17 17:02:56.289042955 -0300`
  * `~/.local/share/omarchy/default/hypr` → `2026-10-03 17:42:32.302688488 -0300`
  * `~/.local/state/omarchy/toggles/hypr` → `2026-10-03 17:53:16.247826301 -0300`
  * `~/.config/omarchy/current/theme` → `2026-10-03 17:49:02.613233762 -0300`
* Host file counts after the copy are unchanged: `~/.config/hypr` 15 files,
  `~/.local/share/omarchy/default/hypr` 35 files, `~/.local/state/omarchy/toggles/hypr` 2 files.

Copy method was `cp -p` (preserve mode/timestamps) into the lane seat — the destination is
inside the lane repo, the sources were only ever opened for reading.

## 4. Source-graph reachability (for C2's option-table resolver)

Parsed every `source =` directive (`^[ \t]*source[ \t]*=[ \t]*(.+?)[ \t]*$`, multiline) in
the captured tree and expanded `~`, and the single glob
(`~/.local/state/omarchy/toggles/hypr/*.conf`, `hyprland.conf:23`). The closure from the
entry point `~/.config/hypr/hyprland.conf` is **40 of the 53 copied files**; every
`source =` target resolves inside the captured tree (no dangling reference).

13 copied files are **not** in that closure (present in the tree, but nothing sources them
from `hyprland.conf`):

```
.config/hypr/envs.conf
.config/hypr/hypridle.conf
.config/hypr/hyprlock.conf
.config/hypr/hyprsunset.conf
.config/hypr/xdph.conf
.config/omarchy/current/theme/hyprlock.conf
.local/share/omarchy/default/hypr/apps/davinci-resolve.conf
.local/share/omarchy/default/hypr/bindings.conf
.local/share/omarchy/default/hypr/bindings/tiling.conf
.local/share/omarchy/default/hypr/plain-bindings.conf
.local/share/omarchy/default/hypr/toggles/flags.conf
.local/share/omarchy/default/hypr/toggles/single-window-aspect-ratio.conf
.local/share/omarchy/default/hypr/toggles/window-no-gaps.conf
```

[INFERENCE] These are the residual/alternate-config files: `default/hypr/bindings.conf`
sourced by neither `hyprland.conf` nor `default/hypr/apps.conf`; `default/hypr/toggles/*`
are *templates* whose live instances are the two files under `~/.local/state/omarchy/toggles/hypr/`
(only the state copies are sourced); `hypridle.conf`/`hyprlock.conf`/`hyprsunset.conf` are
launched by their own daemons rather than by Hyprland's `source`; `default/hypr/bindings/tiling.conf`
is superseded by `tiling-v2.conf`, which *is* sourced. A last-declarer option resolver that
treats "present in the tree" as "declarer" would attribute ownership to unsourced files —
the captured tree is the ground for checking that.

`~/.config/hypr/hyprland.conf` is the sole entry point; the source graph is a DAG over the
40 reachable files with `apps.conf` and `windows.conf`/`bindings.conf` chaining through the
defaults tree.

## 5. Scope discipline / safety

* Writes confined to
  `.ufo/waves/round-39/w1/SctHostTree/{real-tree/**,manifest.sha256}` and this report file
  `.ufo/waves/round-39/w1/SctHostTree.md` (the explicit destination named in my task).
* Nothing written to the fleet repo, sibling lanes, `templates/`, `scripts/`,
  `MANIFEST.json`, `.ufo/state/`, `.ufo/watchdog.log`, `.scratch/`.
* No mutating git/jj in the lane. Read-only `git status --porcelain` was run
  (exit 0) — the only untracked entries are the wave's own artifacts
  (`w1-dispatch.json`, `w1-spec.json`, `w1/`, `tools/mado-options.py`,
  `quality/counters/c3-r39-options.py`), i.e. other seats' outputs; this seat added
  only `w1/SctHostTree/**`.
* No socket connect, no compositor query, no service mutation, no package transaction
  (pacman is paused host-wide and was not invoked). No tool was installed — the task
  needed only `coreutils` (`sha256sum`) and stock `python3`, both already present.
* Scratch (pre-copy inventory, verification logs) lived in `/tmp/sct-hosttree/`, outside
  the lane.

## 6. Unknowns / limits

* The capture is of the **host** files; it is a point-in-time snapshot (2026-10-25,
  ~16:10 local). The compositor's live state was not queried (no socket), so the capture
  is config bytes only, not the effective runtime values.
* The 40/53 reachability figure depends on the `source =` grammar as parsed above; Hyprland
  also honours `source` inside `$HYPRLAND_CONFIG_DIR`-relative paths and `env` expansion,
  neither of which appears in this tree.
* `~/.config/omarchy/current/theme/` is a live theme directory that omarchy can swap at
  runtime; only the three `source =`-named files were captured, so a later theme switch
  would not be reflected in `manifest.sha256`.

## 7. Machine-readable pointers

```
capture root : .ufo/waves/round-39/w1/SctHostTree/real-tree/
manifest     : .ufo/waves/round-39/w1/SctHostTree/manifest.sha256   (53 rows)
manifest sha : 08be94e527843e4a8e8b0f4d976fded74c1edb23de64126ddf415520f35291a3
verify       : cd real-tree && sha256sum -c ../manifest.sha256   → exit 0, 53 OK / 0 failed
```

Report: `.ufo/waves/round-39/w1/SctHostTree.md`
