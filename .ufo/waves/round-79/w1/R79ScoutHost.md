# R79ScoutHost — host reconnaissance for C1 and C2

Seat: scout (leaf, no dispatch). Repository `/home/vgpnk/Projects/shokunin/mado-shokunin`
at `5eb8f20fe291603c74973fa94cc55723ac8089a4` (freeze), base
`e4b153dfa4a67ca56f7ec65cb6639082451626a7`. Read-only host posture: only the permitted
`hyprctl` read verbs, `pgrep`, `makoctl mode`, `omarchy …`, `systemctl`-free file reads and
`python3 -I` joins over caller-supplied files. Captures were reduced before storage: the
monitors reply is kept as name/size/reserved/scale/transform only (no description/serial),
layer client pointers and pids are dropped from the committed copy, and no instance
signature or window title appears in this file. All commands below ran 2026-11-04
(~10:2x–10:31 UTC). Artifacts: `w1/R79ScoutHost/{layers.json,monitors.json,barfoot-host.txt,
rows-22.txt,env-matrix.txt,change-matrix.txt,keybindings-shape.txt,c2-counter-verify.txt}`.

## 1 C1 — the host join composes static zero with the bar's band

Exact command (cwd = lane root, read-only):

```
python3 -I tools/mado-barfoot.py --config ~/.config/waybar/config.jsonc \
  --layers .ufo/waves/round-79/w1/R79ScoutHost/layers.json \
  --monitors .ufo/waves/round-79/w1/R79ScoutHost/monitors.json \
  --rules ~/.config/hypr/monitors.conf
```

stdout, verbatim, exit code **0** (also `w1/R79ScoutHost/barfoot-host.txt`):

```
MADO_BARFOOT_CONFIG: pos=top layer=top level=2 ns=waybar height=26 width=0 margins=0,0,0,0 exclusive=true
MADO_BARFOOT_STATIC: monitor=DP-1 top=0 right=0 bottom=0 left=0 source=rules
MADO_BARFOOT_DECL: monitor=DP-1 box=0,0,3440,26 edge=top
MADO_BARFOOT_LIVE: monitor=DP-1 level=2 ns=waybar box=0,0,3440,26 entries=1
MADO_BARFOOT_RESULT: monitor=DP-1 box=MATCH reserved=EQ band=26 expected=26 verdict=CLEAN
MADO_BARFOOT: verdict=CLEAN
```

The reduced captures drive the join identically (same six lines, rc 0), so the committed
copies are sufficient input. Live state: one monitor `DP-1`, 3440x1440, `reserved`
`[0,26,0,0]`, scale 1, transform 0; layer levels `0` = `wallpaper` (0,0,3440x1440),
`2` = `waybar` (0,0,3440x26), `1` and `3` empty. `hyprctl layers -j` is keyed by `DP-1`
with exactly levels `0`–`3`.

Config facts the join meets:

- `addreserved` in `~/.config/hypr/**` (including the `.bak` files): **0 occurrences**
  (`grep -rn addreserved ~/.config/hypr` → 0). `~/.config/hypr/monitors.conf:10` is the only
  `monitor =` line and carries no reserved field:
  `monitor = DP-1, 3440x1440@100, 0x0, 1`.
- `source =` in `~/.config/hypr/monitors.conf`: **0** — the join is not refused. The main
  config has 18 (`~/.config/hypr/hyprland.conf` lines 4-13, 16-20, 23, 29, 32). Pointing the
  join at it is a measured refusal, rc **3**:
  `MADO_BARFOOT: ERROR (stage=model the rules file carries a `source =` line (line 4); a sourced file is not followed, so the static reserve is unknown)`.
  So `monitors.conf` is the only `~/.config/hypr` file the join can consume; `hyprland.conf`
  is refused by design.
- Source closure reachable from `hyprland.conf` (theme `~/.config/omarchy/current/theme/hyprland.conf`,
  `~/.local/share/omarchy/default/hypr/**`, `~/.local/state/omarchy/toggles/hypr/*.conf`):
  **0 `addreserved`**, **0 `monitor =`** lines. The host has no static reserve declared
  anywhere, so `static top=0 … source=rules` is the correct host reading.
- `~/.config/waybar/config.jsonc`: `"layer": "top"` (:3), `"position": "top"` (:4),
  `"height": 26` (:6); no `output`, `mode`, `margin` or `exclusive` key. None of the four
  refusal fixtures' triggers (mode preset, scale/transform, background layer, spaced output
  pattern) is present.
- `python3 -I tools/mado-barfoot.py --selftest` → `MADO_BARFOOT_SELFTEST: 43/43`, rc 0.

Measured fragility of this join, with synthetic layer captures in my scratch and the same
config/monitors/rules (no host mutation):

- bar layer height 26 → 30 (what a theme/CSS height change does):
  `MADO_BARFOOT_RESULT: … box=DIFFER reserved=EQ band=26 expected=26 verdict=DIFFER`, rc 1.
  The declared box comes from the waybar config `height`, so a CSS-only height change is
  reported as drift.
- bar layer absent (level 2 empty): `… box=NO_LAYER reserved=NOT_CHECKED verdict=NO_LAYER`,
  rc 3.

Note on the legacy rule line: `tools/mado-barfoot.py:739-740` asserts that a later
non-`addreserved` rule for the same monitor resets the static area to zero
(`monitor = M1, 3440x1440@100, 0x0, 1` after an `addreserved` rule yields `ZERO_STATIC`).
The host's zero comes from that last-wins reset, not from a missing selector.

## 2 C2 — all 22 runbook rows executed here

Each case's `argv` was run exactly as frozen (cwd = lane root), twice, the second pass at
2026-11-04T10:28:16Z–10:28:25Z after the §1 exploration; both passes produced **byte-identical
stdout and identical rc for all 22 rows**. Elapsed times are wall-clock around the subprocess.
Nothing came near 5 s (max 0.076 s, `omarchy-menu-keybindings`; next 0.041 s). Table
(`w1/R79ScoutHost/rows-22.txt`):

| case | kind | rc | s | first 80 chars |
|---|---|---|---|---|
| version | regex | 0 | 0.003 | `Hyprland 0.56.2 built from branch v0.56.2 at commit efb50993780079460b0cbed1363e` |
| configerrors | empty | 0 | 0.004 | (empty) |
| monitors-size | regex | 0 | 0.003 | `DP-1 3440x1440@99.99700` |
| monitors-reserved | int4 | 0 | 0.003 | `[0,26,0,0]` |
| gaps-out | exact | 0 | 0.003 | `custom type: 0 0 0 0` |
| kb-layout | exact | 0 | 0.003 | `str: br` |
| binds-count | int_range | 0 | 0.004 | `192` |
| layers-namespaces | sorted_unique | 0 | 0.003 | `wallpaper,waybar` |
| waybar-process | int_range | 0 | 0.023 | `1720` |
| mako-mode | exact | 0 | 0.001 | `default` |
| omarchy-theme | exact | 0 | 0.005 | `Matte Black` |
| omarchy-version | regex | 0 | 0.005 | `3.8.3` |
| active-workspace | json_object_fields | 0 | 0.003 | `{"id":1,"name":"1"}` |
| layers-dump | levels_dump | 0 | 0.003 | `{` |
| monitors-dump | array_fields | 0 | 0.003 | `[{` |
| clients-count | int_range | 0 | 0.011 | `2` |
| workspaces-count | int_range | 0 | 0.003 | `2` |
| refuse-mode | refusal | 3 | 0.026 | `MADO_BARFOOT: ERROR (stage=model a mode preset rewrites layer and exclusive zone` |
| refuse-scale | refusal | 3 | 0.026 | `MADO_BARFOOT: ERROR (stage=model monitor M1 has scale/transform 2.0/0; the reply` |
| refuse-layer-background | refusal | 3 | 0.025 | `MADO_BARFOOT: ERROR (stage=model waybar's presets never select the background la` |
| refuse-output-space | refusal | 3 | 0.027 | `MADO_BARFOOT: ERROR (stage=model output pattern 'DP-1 DP-2' is outside the model` |
| omarchy-menu-keybindings | lines_shape | 0 | 0.076 | `SUPER + RETURN                      → Terminal` |

Cross-check with the frozen instrument on the same host (read-only, scratch root in my
scratch, `w1/R79ScoutHost/c2-counter-verify.txt`): rc 0,
`cases=22 executed=22 matched=22 shapes=17/17 anchors=22/22 rows=22/22 control_new=0/5 mutants=9 killed=9 verdict=TARGET_MET rev=5eb8f20… tree=bound`.
The same run printed `control_all=15/22`; that is exactly the 15 cases carrying a `frozen`
value (all 15 equal their frozen value here) — the seven without one are `layers-dump`,
`monitors-dump`, the four `refuse-*` rows and `omarchy-menu-keybindings`.

`omarchy menu keybindings --print`: 193 lines, 193 containing `→`, rc 0; under `LC_ALL=C`
also 193/193 (`w1/R79ScoutHost/keybindings-shape.txt`).

## 3 Shell and environment features the rows need but the table does not show

No row needs shell *syntax* the cell hides: every cell is executed as `/bin/sh -c <cell>` and
each pipe, single-quote and jq interpolation is literal in the cell (the counter's
`command_rows` extracts the 22 cells and the anchor binding matches 22/22). What the cells do
not show is the **environment the counter injects** (`quality/counters/c2-r79-runbook.py:109-138`:
`LC_ALL=C`, `LANG=C`, `PYTHONDONTWRITEBYTECODE=1`, `XDG_RUNTIME_DIR` default,
`HYPRLAND_INSTANCE_SIGNATURE` discovery, `OMARCHY_PATH` discovery, PATH extension with
`/usr/local/bin:/usr/bin:/bin:~/.local/bin:~/.local/share/omarchy/bin`). Measured by re-running
all 22 cases with one variable removed (`w1/R79ScoutHost/env-matrix.txt`):

| variant | passing | failing rows (rc) |
|---|---|---|
| as-is | 22/22 | — |
| `HYPRLAND_INSTANCE_SIGNATURE` dropped | 8/22 | version(0), configerrors(1), monitors-size(5), monitors-reserved(5), gaps-out(0), kb-layout(0), binds-count(5), layers-namespaces(5), active-workspace(5), layers-dump(1), monitors-dump(1), clients-count(5), workspaces-count(5), omarchy-menu-keybindings(0) |
| `OMARCHY_PATH` dropped | 21/22 | omarchy-version(1) |
| `PATH=/usr/bin:/bin` | 19/22 | omarchy-theme(127), omarchy-version(127), omarchy-menu-keybindings(127) |

Observed details:

- Without the signature, `hyprctl version` prints
  `HYPRLAND_INSTANCE_SIGNATURE not set! (is hyprland running?)` on **stdout with rc 0**, so
  row 1 fails on its regex, not on rc; `hyprctl configerrors`, `layers -j`, `monitors -j`
  exit 1; the `jq`-piped rows exit 5. `omarchy menu keybindings --print` also fails (rc 0)
  because it shells out to `hyprctl`. So 14 of 22 rows are bound to state the command cell
  does not mention.
- Without `OMARCHY_PATH`, `omarchy version` exits 1 with `cat: /version: No such file or
  directory`; `omarchy theme current` still works.
- `omarchy` lives only at `/home/vgpnk/.local/share/omarchy/bin/omarchy`; under a minimal
  PATH the three omarchy rows exit 127.
- `makoctl mode` passes with `DBUS_SESSION_BUS_ADDRESS` unset (rc 0, `default`), so that row
  carries no hidden bus dependency on this host.

## 4 Plausible host changes versus the declared shapes

Scored with the frozen `matches` / `refusal_matches` imported read-only from
`quality/counters/c2-r79-runbook.py` and fed the output each change would produce
(`w1/R79ScoutHost/change-matrix.txt`). No live mutation was performed — write verbs are
forbidden — so this is the instrument's verdict on synthetic outputs, not an observed switch.

- **another workspace**: `active-workspace` PASS for a normal `{"id":3,"name":"3"}` and for a
  special `{"id":-99,"name":"special:scratch"}` (id `int` accepts negatives, name `str`
  accepts `special:`); `workspaces-count` PASS at 5, FAIL only at 0; `clients-count` PASS at
  7. **No row of the 22 breaks on a workspace switch.**
- **a waybar restart**: `layers-namespaces` FAIL while the bar is absent (`wallpaper`) and
  FAIL during old+new overlap (`wallpaper,waybar,waybar`, duplicate namespace); PASS with an
  extra layer (`notify-send,wallpaper,waybar`). `waybar-process` PASS with a new pid, FAIL if
  sampled in the no-process gap (`pgrep` rc 1, the rc==0 gate rejects it). `monitors-reserved`
  still PASS at `[0,0,0,0]`; `layers-dump`/`monitors-dump` PASS. On the C1 side the same
  restart is `verdict=NO_LAYER` rc 3 while the bar is gone, and `DIFFER` rc 1 if it returns at
  a different height.
- **a theme switch**: `omarchy-theme` FAIL (its value is the exact string `Matte Black`, with
  no churn/negative sample to absorb a theme change); `omarchy version` PASS. The switch also
  restarts waybar — `~/.local/share/omarchy/bin/omarchy-theme-set:53-54`
  (`if pgrep -x waybar >/dev/null; then omarchy-restart-waybar`) — so rows 8 and 9 are
  transiently exposed on every theme switch under the shapes above. A CSS-only bar-height
  change leaves rows 14/15 passing while the C1 join returns DIFFER (measured 26 vs 30).
- **a bind edit**: `binds-count` PASS for any 1..100000 (192 now), FAIL only at 0 or a
  non-number; `omarchy-menu-keybindings` PASS at 193 arrow lines, FAIL at 99 lines and FAIL
  on any line without `→` (a section header would do it). Headroom over the ≥100 floor is 93
  lines.
- **other config/host edits**: `gaps-out` is exact `custom type: 0 0 0 0`, so any gaps change
  FAILs — and `~/.local/state/omarchy/toggles/hypr/window-no-gaps.conf` is precisely a toggle
  that rewrites `gaps_out`; `kb-layout` is exact `str: br`, so a layout switch FAILs;
  `configerrors` FAILs on any error; `monitors-size` FAILs on unplug (`.[0]` of `[]` renders
  `null nullxnull@null`) but PASSes at scale 1.5 (the shape ignores scale);
  `monitors-reserved` FAILs (`null`) and `monitors-dump`/`layers-dump` FAIL (`[]`/`{}`) with
  no monitor; a Hyprland 0.58 upgrade PASSes the regex rows.
- **shape blind spot**: `monitors-reserved` is `int4`, so it PASSes at `[0,0,0,0]` (bar gone)
  and at any other non-negative band. That operability row cannot see the reserved-band drift
  C1 is about; only the C1 join reports it, and only as CLEAN/DIFFER.

## 5 Remaining unknowns

- No live host change was induced (forbidden), so restart/theme/workspace behaviour above is
  the frozen matcher's verdict on synthetic outputs, plus synthetic layer captures for the
  tool; the theme→waybar restart is read from the script, not executed.
- The host has a single monitor (`DP-1`); `.[0]` ambiguity, multi-monitor `layers` keys and a
  second `reserved` consumer are untested here.
- `version`'s regex accepts any `Hyprland x.y.z`, so upgrades and downgrades are invisible to
  that row by design; `monitors-size` is likewise shape-only (refresh rate is unconstrained).

Report: .ufo/waves/round-79/w1/R79ScoutHost.md
