# ExecHostCompose — host findings table (mado round 40, wave w1)

Report: `.ufo/waves/round-40/w1/ExecHostCompose.md`

## Deliverable

`.ufo/waves/round-40/w1/ExecHostCompose/host-table.md` — 265 lines, 70 option rows (one per key the
static resolver declares and the compositor answers), grouped as colours 11, gaps/borders 5,
rounding 2, blur 6, shadow 3, animations 1, input/cursor 15, layout+group bar 17, misc/ecosystem/
xwayland 10. Columns per row: `key | declared (as written) | live (native form + value) | label |
owner file:line | earlier declarer (shadowed)`. The two angle-inheritance rows are flagged `†1`
and `†2` and dissected in their own section. No recommendations anywhere in the file; it states
facts the census and the declarer derivation show, plus an explicit "what this table does not
establish" section.

Files written (all inside the seat directory):

| path | sha256 |
|---|---|
| `.ufo/waves/round-40/w1/ExecHostCompose/host-table.md` | `ed64356078d2a1db5a3bacc6e36791274a3f38c099b1b144f28d1a63e6adbab0` |
| `.ufo/waves/round-40/w1/ExecHostCompose/live.json` | `cde4b2dfb586e5d9765af1df6f73188da3537b53f13a9525d21b693684905462` |
| `.ufo/waves/round-40/w1/ExecHostCompose/hyprctl-version.txt` | `e0fb982b88d0017e13a5ee2697765a10c4c088eefc589bdc02656b9be7f2844f` |
| `.ufo/waves/round-40/w1/ExecHostCompose.md` (this report) | — |

No tracked lane file, counter, control, receipt, config tree, state dir, service or sibling lane was
touched. `tools/mado-options.py` was neither read-modified nor run: every number in the table comes
from the throwaway reference, which is a control and is never delivered.

## How the data was produced

1. Copied the control `c1/ctl-ref-tool.py.txt` to `/tmp/hostcompose.2qy6nV/ref.py`
   (sha256 `f96d9e0a0d2fe1bccb87940244db079de88c6794f03d66a36304d574694a08aa`) and ran

   ```
   python3 -I /tmp/hostcompose.2qy6nV/ref.py --home "$HOME" --live > live.json
   ```

   exit 0, empty stderr, 70 rows. Labels: `agreement` 62, `agreement*` 8, `mismatch` 0,
   `config-only` 0, `live-default` 0.
2. Cross-checked every value and `set` flag of that run against the frozen capture
   `c1/native-capture.jsonl`: **0 diffs over 70 keys**. The capture supplies the native form name
   per key, because the reference tool's row carries only the value string; form counts from it are
   int 44, float 5, custom 13, str 8 (sum 70).
3. Read the owner file:line and the raw line text out of the host trees for each row (read-only
   reads), and located each shadowed declarer by exact-key grep over the same resolved `source =`
   graph.
4. Queried the six colour-bearing keys directly with `hyprctl getoption -j` to hold the raw native
   reply text used in the angle section (`general:col.active_border`, `group:col.border_active`,
   `general:col.inactive_border`, `decoration:shadow:color`, `group:groupbar:col.active`,
   `group:col.border_locked_active`).

## Findings the table records (facts only)

- Host: `Hyprland 0.56.2 … commit efb50993780079460b0cbed1363e2166a2de1d9f`, Hyprlang system 0.6.8
  (`hyprctl version`, retained).
- **The two angle-inheritance rows.** `general:col.active_border` and `group:col.border_active` are
  last declared in `~/.config/omarchy/current/theme/hyprland.conf:4` and `:8` as
  `col.active_border = $activeBorderColor` with `$activeBorderColor = rgb(e68e0d)` (theme `:1`) —
  one colour, no `deg` token. Both read back `custom ffe68e0d 45deg`. The `45deg` is the shadowed
  defaults declarer's angle (`~/.local/share/omarchy/default/hypr/looknfeel.conf:15` / `:51`, with
  `$activeBorderColor = rgba(33ccffee) rgba(00ff99ee) 45deg` at `:4`). Discrimination in the data:
  six other rows have the identical declared shape (one colour, no `deg`) and read `0deg`
  (`decoration:shadow:color`, `general:col.inactive_border`, `group:col.border_inactive`,
  `group:col.border_locked_inactive`, `group:groupbar:col.active`, `group:groupbar:col.inactive`);
  the only difference is a preceding declarer that carried `45deg`.
- Declared-to-native conversions the rows show: one-integer gaps answer as a 4-tuple (`0` →
  `0 0 0 0`); font-weight names answer as numbers (`ultraheavy` → `1000`, `normal` → `400`); colour
  held by an `int` option answers as decimal ARGB (`rgb(ffffff)` → `4294967295`); colour held by a
  `custom` option answers as lowercase unpadded AARRGGBB (`rgba(1a1a1aee)` → `ee1a1a1a`);
  `animations:enabled = yes, please :)` answers `int 1`.
- Shadowing: all 8 `agreement*` rows shadow an earlier declaration; 6 change the value, 2 do not
  (`decoration:rounding` 0→0, `input:kb_options` `compose:caps`→`compose:caps`), so the label is a
  declarer-count fact, not a value-difference fact.
- All 70 replies carry `set: true`; no declared key is unset on this host.

## Retained evidence

- `host-table.md` itself: every row cites `file:line` under `$HOME` and the raw declaration text, so
  each cell is re-checkable with `sed -n 'Np'` on the named file.
- `live.json`: the reference tool's unedited output for the run above.
- `hyprctl-version.txt`: unedited `hyprctl version` output.
- Form counts recomputed from `c1/native-capture.jsonl` (`int 44, custom 13, str 8, float 5`,
  70 keys) and label counts from `live.json` (`agreement 62, agreement* 8`).

## Checks I ran

| check | result |
|---|---|
| reference `--live` over `$HOME` | exit 0, empty stderr, 70 rows |
| run values vs `c1/native-capture.jsonl` | 0 diffs / 70 keys, `set` flags equal |
| row set vs the 9 groups | 70 rows, no duplicate, no key missing |
| form counts sum | 44+5+13+8 = 70 |
| label counts sum | 62+8 = 70, `mismatch` 0 |

Nothing else was run: no build, lint, test or counter, per the wave rule that the parent owns the
post-integration gate.

## Risks

- **The table is model-relative.** Every "live" value is the compositor's answer, but every "label"
  is the reference model's verdict on it. On these 70 keys the model produces 0 `mismatch`; that is
  the declared C1 residual (an out-of-distribution check, reported not scored), not proof that the
  model's conversion tables are right in general.
- **The table does not test the delivered tool.** If the delivered `tools/mado-options.py --live`
  differs from the reference, this table says nothing about it.
- **Line numbers are pinned to the host's current config bytes.** Any edit to a host config file
  moves the `file:line` column; the declaration text is quoted so a moved line is still identifiable.
- **`agreement*` is not a quality signal.** Two of the eight are value-identical shadowings; a reader
  must not treat the label as "the shadowed value was wrong".

## Blockers

None. No package transaction was run (host `pacman` paused); no tool was installed or upgraded, so
there is no tool/version/channel record to report. The scratch directory `/tmp/hostcompose.2qy6nV`
was removed after the artifacts were copied into the seat directory.
