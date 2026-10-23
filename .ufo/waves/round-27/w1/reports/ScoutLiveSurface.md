# ScoutLiveSurface

Read-only recon of the live Hyprland session and the operator config trees. Nothing was modified except this report. No Hyprland process was started. No packages were installed.

## Verdict

The operator's own tree does not exercise any workspace rule. `hyprctl workspacerules -j` on the live compositor prints `[]`. A full walk of the three assigned trees found zero `workspace =` / `workspace=` lines.

Confidence: high for the live JSON and the zero-line scan. The `configerrors` empty-string reading is high, from the pinned Hyprland and hyprutils sources below.

## Live hyprctl

Commands (read verbs only; session env already had `WAYLAND_DISPLAY` and `HYPRLAND_INSTANCE_SIGNATURE`; those variables were not set for any new process):

```
timeout 15 hyprctl workspacerules -j   # exit 0
timeout 15 hyprctl configerrors -j     # exit 0
timeout 15 hyprctl version -j          # exit 0
```

`workspacerules -j` stdout:

```
[]
```

`configerrors -j` stdout:

```
[
	""
]
```

`version -j` (fields that pin the session): branch `v0.56.2`, commit `efb50993780079460b0cbed1363e2166a2de1d9f`, tag `v0.56.2`, dirty false, buildHyprlang `0.6.8`, buildHyprutils `0.14.2`, systemHyprlang `0.6.8`, systemHyprutils `0.14.2`. That is the round-27 pin.

Text-mode follow-up, same process, still read-only:

- `hyprctl configerrors` printed one blank line, exit 0.
- `hyprctl workspacerules` printed `unknown request`, exit 0.

That text result is not a missing verb. In Hyprland `efb50993780079460b0cbed1363e2166a2de1d9f` `src/debug/HyprCtl.cpp`, `workspaceRulesRequest` (lines 613–630) returns `[]` for JSON when `Config::workspaceRuleMgr()->getAllWorkspaceRules()` is empty, and returns an empty string in text mode. The dispatcher (lines 2123–2124) replaces an empty result with `unknown request`. So a live empty table is `[]` on `-j` and the string `unknown request` without `-j`.

`configerrors -j` being `[""]` is the empty-error encoding, not an error message. `configErrorsRequest` (same file, lines 725–746) splits `Config::mgr()->getErrors()` with `CVarList(currErrors, 0, '\n')`. hyprutils v0.14.2 `CVarList` (`include/hyprutils/string/VarList.hpp:14`) defaults `removeEmpty` to false, and `VarList.cpp:9–10` pushes one empty element when the input is empty and `removeEmpty` is false. That element is JSON-encoded as `""`. Text mode then prints a single newline, which matches the blank line observed.

## `workspace =` lines

Pattern: a `workspace` keyword assignment, `(?<![\w])workspace\s*=`, so `warp_on_change_workspace =` does not count. Also checked optional leading comment: `^\s*#?\s*workspace\s*=`.

Walk: 78 files under the three trees (15 in `~/.config/hypr`, 35 in `~/.local/share/omarchy/default/hypr`, 28 in `~/.config/omarchy/current/theme`, including 7 binary images that were skipped after a NUL check). Hits: **0**.

The same pattern over the two files `~/.config/hypr/hyprland.conf:23` sources (`~/.local/state/omarchy/toggles/hypr/window-no-gaps.conf`, `flags.conf`) is also 0. Those two are outside the assigned trees.

There is no `workspace =` line to cite.

All three roots are real directories, not symlinks. `~/.config/hypr/hyprland.conf` and `~/.config/omarchy/current/theme/hyprland.conf` are regular files.

## Whether the operator tree exercises a workspace rule

No.

`~/.config/hypr/hyprland.conf` is the live root. Its `source =` lines (4–13, 16–20, 23, 29, 32) pull Omarchy defaults, `~/.config/omarchy/current/theme/hyprland.conf`, the operator's own monitors/input/bindings/looknfeel/autostart, the toggle glob, `ai-usage.conf`, and `gkeep.conf`. None of those files contains a `workspace =` keyword. The theme file is only border colors (`hyprland.conf:1–9` of the theme).

The live table agrees: zero workspace rules are loaded, including any that a `hyprctl keyword` might have added at runtime.

## Near misses (not workspace rules)

These mention the word workspace and are not `workspace =` lines:

- `~/.config/hypr/hyprland.conf:26` — commented, not active: `# windowrule = workspace 5, match:class qemu`. Same text in `hyprland.conf.bak.1792267376:26`.
- `~/.config/hypr/input.conf:48` and `:50` — commented gesture notes, not rules.
- `~/.local/share/omarchy/default/hypr/apps/browser.conf:19` — `windowrule = workspace special silent, match:title .*is sharing.*`. This is a window rule. It is in the live source closure: operator `hyprland.conf:12` sources `windows.conf`, and `windows.conf:12` sources `apps.conf`, which sources `browser.conf`. It does not appear in `hyprctl workspacerules -j` (the table is `[]`).
- `~/.local/share/omarchy/default/hypr/looknfeel.conf:137` — `warp_on_change_workspace = 1` (cursor key). `:105–106` are workspace animations. `:142` is `hide_special_on_workspace_change = true`.
- `~/.local/share/omarchy/default/hypr/bindings/tiling-v2.conf` — bind dispatchers (`workspace`, `movetoworkspace`, `movetoworkspacesilent`, `togglespecialworkspace`, `movecurrentworkspacetomonitor`), lines 13 and 22–70. The operator root sources this file (`hyprland.conf:7`). `bindings/tiling.conf` has the same kind of binds (lines 22–70) but the operator root does not source it; it sources `tiling-v2.conf` directly.
- `~/.config/omarchy/current/theme/obsidian.css:88` — a CSS class `.workspace-leaf`, not Hyprland.

## Inference

[INFERENCE] The unperturbed snapshot a C1 counter would take from this home, if it matches these bytes, has an empty workspace-rule table. That is what the live compositor already prints. Not measured here: the isolated oracle was not run.

## Unresolved

- The compositor was not asked which files it actually parsed. The source closure above is read off `source =` lines, not off a Hyprland load log.
- Files outside the three trees and the toggle glob were not scanned. The empty live table still says no workspace rule is in effect.

## Safety

No compositor write (`dispatch`, `keyword`, `reload`, `kill`). No nested Hyprland. No coredump delta, because no Hyprland was started.
