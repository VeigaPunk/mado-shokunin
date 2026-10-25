# ExecOptionsRealTree — C2 real-tree evidence run (round 39, wave 1)

Seat: `.ufo/waves/round-39/w1/ExecOptionsRealTree/`. Scope: host config bytes copied read-only
into `host-tree/`, real-tree runs of `tools/mado-options.py`, synthetic `--getoption` merge from
lane-recorded pairs. No other files written. No tools installed (none needed; stdlib only).

## 1. Host tree copy (read-only, 49 files)

Source graph resolved by following every `source =` line depth-first from
`~/.config/hypr/hyprland.conf` (+ `hyprlock.conf`'s theme source):

- 13 user configs `~/.config/hypr/*.conf` (ai-usage, autostart, bindings, envs, gkeep,
  hypridle, hyprland, hyprlock, hyprsunset, input, looknfeel, monitors, xdph)
- 31 default-tree files `~/.local/share/omarchy/default/hypr/` (7 direct + 19 `apps/*.conf`
  via `apps.conf` + 5 `bindings/*.conf` via `bindings.conf`/`hyprland.conf`)
- 3 theme files `~/.config/omarchy/current/theme/{hyprland,hyprlock,gum.env}.conf`
  (`gum.env.conf` via default `envs.conf`)
- 2 toggle files `~/.local/state/omarchy/toggles/hypr/{flags,window-no-gaps}.conf` (glob)

Copied into `host-tree/` preserving relative paths under the fake HOME (e.g.
`host-tree/.config/hypr/hyprland.conf`). Excluded as not source-reachable: `*.bak.*`, default
`plain-bindings.conf`, default unreferenced `toggles/` dir.

Byte identity: `sha256sum` manifest written pre-copy (`host-src.sha256.norm`) and post-copy
(`host-dst.sha256.norm`) — `diff` empty (49/49, IDENTICAL=YES); re-verified after all tool runs
(no mismatches). `<pair only regular files (`-rw-r--r--`).

## 2. Tool version

`tools/mado-options.py` landed during the wave: first revision 16:10 selftest failed
(`MADO_OPTIONS_SELFTEST: 62/69 passed`, exit 1 — observed, transient); final revision 16:11
`sha256 cee78d99de2e3420572aa028f439240ac12e5eb6d595de75e2fc62e5ea9ce61e`,
`--selftest` → `MADO_OPTIONS_SELFTEST: 69/69 passed`, exit 0 (saved `selftest.stdout`).

## 3. Run 1 — static (no live merge)

```
cd /home/vgpnk/Projects/shokunin/mado-shokunin
python3 -I tools/mado-options.py --home .ufo/waves/round-39/w1/ExecOptionsRealTree/host-tree \
  > .ufo/waves/round-39/w1/ExecOptionsRealTree/run-static.stdout
```
Exit 0. Output: one JSON array.

- Row count: **79**
- Unique owner files: **11**
  - 47 `.local/share/omarchy/default/hypr/looknfeel.conf`
  - 8 `.local/share/omarchy/default/hypr/input.conf`
  - 7 `.config/hypr/input.conf`
  - 4 `.local/state/omarchy/toggles/hypr/window-no-gaps.conf`
  - 4 `.local/share/omarchy/default/hypr/apps/moonlight.conf`
  - 2 `.local/share/omarchy/default/hypr/bindings/utilities.conf`
  - 2 `.local/share/omarchy/default/hypr/envs.conf`
  - 2 `.config/omarchy/current/theme/hyprland.conf`
  - 1 `.local/share/omarchy/default/hypr/bindings/media.conf`
  - 1 `.local/share/omarchy/default/hypr/bindings/tiling-v2.conf`
  - 1 `.local/share/omarchy/default/hypr/apps/jetbrains.conf`
- Layer labels: defaults 66, user 7, toggles 4, theme 2.

## 4. Run 2 — synthetic `--getoption` merge

Synthetic dump `getoption-synthetic.json` built from the lane's own recorded getoption pairs:
the 56-row claim→live mapping of `corpus/knowledge/hyprctl-verification-layer.md` §3 (each row's
live value + `set` flag → `{"value","custom_type","set"}`), plus the verbatim recorded JSONs in
round-37 scratch (`RevFreezeOrder/getoption.txt`, `ConnFrontier/desc-vs-getoption.txt`). 56 keys.

```
python3 -I tools/mado-options.py --home <host-tree> \
  --getoption <seat>/getoption-synthetic.json > <seat>/run-getoption.stdout
```
Exit 0. Rows: **83** (= 79 static + 4 `live-default` merges; the 4 added rows are exactly the
four §3 live-default keys). Divergence vocabulary census: agreement 41, config-only 27,
agreement* 6, mismatch 5, live-default 4. All 83 rows carry the `agreement` field.

## 5. Parse failures / observations

- No hard parse failures: both runs exit 0, every row has all fields
  `{key,value,owner,layer,line,set}`, no duplicate keys, owner file exists in the copied tree,
  line indexes in-bounds and point at non-comment statement lines, leaf key matches the source
  line's LHS for all rows except the windowrule-block rows noted below.
- `python3 -I` emits a SyntaxWarning on import: `tools/mado-options.py:161: SyntaxWarning: "\`"
  is an invalid escape sequence` (docstring of the escape-pass helper); harmless but reported.
- **bind-variant rows (4):** keys `binddr` (`.../bindings/utilities.conf:69`), `bindeld`
  (`.../bindings/media.conf:21`), `bindld` (`.../bindings/utilities.conf:10`), `bindmd`
  (`.../bindings/tiling-v2.conf:100`). These are real Omarchy `bind*` statements that the tool's
  exclusion list does not cover (plain `bind`/`bindd` lines are excluded — none appear). The C2
  claim's own wording excludes "non-bind" settings, so these leak into the table.
- **windowrule-block rows (4):** `windowrule:match:class`, `windowrule:fullscreen`,
  `windowrule:idle_inhibit`, `windowrule:name` all from `.local/share/omarchy/default/hypr/apps/moonlight.conf`
  (lines 2–5, a `windowrule { ... }` block). Rule-block contents are emitted despite the
  "non-rule" exclusion in the claim. Together with the bind variants, 8 of 79 static rows are
  outside the stated non-bind/non-rule option vocabulary.
- `hypridle.conf`/`hyprsunset.conf`/`xdph.conf`/user `hyprlock.conf`/`envs.conf` are not on the
  `hyprland.conf` source graph, so they contribute no rows (expected).

## 6. Artifacts (all under this seat)

`host-tree/` (49 files), `host-src.sha256.norm`, `host-dst.sha256.norm` (identical),
`getoption-synthetic.json`, `run-static.stdout`, `run-getoption.stdout`, `selftest.stdout`,
`selftest.stderr` (SyntaxWarning only), `run-static.stderr`, `run-getoption.stderr`.

## 7. Risks / notes

- Tool behavior recorded at 16:11 revision; tool was still being iterated when this seat started
  (first revision selftest 62/69). If a later revision changes behavior, the above runs should be
  re-executed.
- The 8 non-option rows (4 bind-variant + 4 windowrule-block) are the main behavioral deviation
  the real tree surfaces; relevant to C2 claim wording ("all non-bind/non-animation/
  non-workspace/non-rule `key = value` settings") and to the counter/reviewer.
