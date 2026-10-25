# ExecLiveCensus — w1 / round 40 — own-work live census receipt (C2 clause h)

Status: DONE. No claim verdict is asserted here; this seat produces the C2 own-work receipt
candidate and the counts it states. Nothing outside my seat directory was written.

## Files written (all under `.ufo/waves/round-40/w1/ExecLiveCensus/`)

| file | sha256 | what |
|---|---|---|
| `census-receipt.txt` | `6c0d38e6a081b207c0ff3669234e0b978a8554270a6ad9bbecbbaba32fa66716` | the receipt candidate (clause-h format) |
| `census-driver.py.txt` | `a6bbbf3ef1366a8fda5453ed75f3f044eb2df9f1c2bb055a0c7316073218dea2` | the driver that produced the census (throwaway) |
| `live-out.json` | `cde4b2dfb586e5d9765af1df6f73188da3537b53f13a9525d21b693684905462` | raw `--live` row JSON (70 rows) |
| `census.json` | `22f0fd1294e65f8620093fda674365c07c12bc3556abd02cfe4a111e8b6aa710` | forms/labels/declarer census JSON |
| `ref-noinherit.py.txt` | `fe149ffbf6d2fffca2de3583acdb88c908afc3e00968884054cc2b4657999e6f` | the angle-inheritance-OFF variant |

Report file: `.ufo/waves/round-40/w1/ExecLiveCensus.md` (this file).
No tracked file was edited; no git/jj command that mutates was run.

## What was run (exact commands, exact results)

1. Reference copied byte-identically:
   `cp .ufo/waves/round-40/c1/ctl-ref-tool.py.txt /tmp/mado-options-ref.py` →
   `sha256 f96d9e0a0d2fe1bccb87940244db079de88c6794f03d66a36304d574694a08aa`, equal to the source.
2. `cd /tmp && python3 -I mado-options-ref.py --home "$HOME" --live` → **exit 0**, 14066 bytes,
   70 rows (`live-out.json`). stderr empty.
3. `hyprctl version` → `Hyprland 0.56.2 built from branch v0.56.2 at commit
   efb50993780079460b0cbed1363e2166a2de1d9f clean`.
   `pkg-config --modversion hyprlang` → `0.6.8`.
4. Census driver (`census-driver.py.txt`): loads the reference module, wraps `State.declare` to
   keep every declarer `(owner, layer, line, value)`, parses `$HOME/.config/hypr/hyprland.conf`
   with the module's own `parse_file`, then calls the module's own `native_query("hyprctl", key)`
   once per declared key (identical argv `hyprctl getoption -j KEY`) and `merge_live()` for the
   labels. Exit 0 (`census.json`).
5. Variant: `cp mado-options-ref.py mado-options-ref-noinherit.py`, one edit —
   `merge_live()` now passes `native_equal(..., 0)` instead of
   `options[key].get("_angle", 0)` (diff hunk at reference line 653-656, kept in
   `ref-noinherit.py.txt`). `python3 -I mado-options-ref-noinherit.py --home "$HOME" --live` →
   exit 0.
6. Direct read-only corroboration of four live values (`hyprctl getoption -j`, the tool's verb):
   ```
   general:col.active_border        -> {"custom": "ffe68e0d 45deg", "set": true}
   group:col.border_active          -> {"custom": "ffe68e0d 45deg", "set": true}
   general:gaps_in                  -> {"custom": "0 0 0 0", "set": true}
   group:groupbar:font_weight_active-> {"custom": "1000", "set": true}
   ```

## Counts (the numbers the receipt states)

- Declared keys: **70** (the static table over `$HOME`).
- Native reply forms among the 70: `forms int=44 float=5 str=8 custom=13` — sums to 70.
  Custom 13 = 9 colour/gradient keys (`decoration:shadow:color`, `general:col.active_border`,
  `general:col.inactive_border`, `group:col.border_active`, `group:col.border_inactive`,
  `group:col.border_locked_active`, `group:col.border_locked_inactive`,
  `group:groupbar:col.active`, `group:groupbar:col.inactive`) + 2 CSS-gap keys
  (`general:gaps_in`, `general:gaps_out`) + 2 font-weight keys
  (`group:groupbar:font_weight_active/_inactive`) = 13; exact key list is in the receipt.
- Labels: `labels agreement=62 agreement*=8 mismatch=0 config-only=0 live-default=0` — sums to 70.
- Angle-inheritance OFF variant: `agreement=62 agreement*=6 mismatch=2 config-only=0
  live-default=0`; flipped keys are exactly
  `general:col.active_border` and `group:col.border_active`
  (`declared='rgb(e68e0d)'`, `live='ffe68e0d 45deg'`, base `agreement*` → variant `mismatch`).
  This is the out-of-distribution check the registration's C1 residual names: the two keys that
  depend on inheritance are the only ones that move, so the other 68 labels do not lean on the
  angle rule.

## The 8 keys with more than one declarer (owner file:line, home-relative)

```
decoration:rounding      live='0'
  .local/share/omarchy/default/hypr/looknfeel.conf:29   value=0
  .local/state/omarchy/toggles/hypr/window-no-gaps.conf:9 value=0
general:border_size      live='0'
  .local/share/omarchy/default/hypr/looknfeel.conf:12   value=2
  .local/state/omarchy/toggles/hypr/window-no-gaps.conf:5 value=0
general:col.active_border live='ffe68e0d 45deg'
  .local/share/omarchy/default/hypr/looknfeel.conf:15   value=rgba(33ccffee) rgba(00ff99ee) 45deg
  .config/omarchy/current/theme/hyprland.conf:4         value=rgb(e68e0d)
general:gaps_in          live='0 0 0 0'
  .local/share/omarchy/default/hypr/looknfeel.conf:9    value=5
  .local/state/omarchy/toggles/hypr/window-no-gaps.conf:4 value=0
general:gaps_out         live='0 0 0 0'
  .local/share/omarchy/default/hypr/looknfeel.conf:10   value=10
  .local/state/omarchy/toggles/hypr/window-no-gaps.conf:3 value=0
group:col.border_active  live='ffe68e0d 45deg'
  .local/share/omarchy/default/hypr/looknfeel.conf:51   value=rgba(33ccffee) rgba(00ff99ee) 45deg
  .config/omarchy/current/theme/hyprland.conf:8         value=rgb(e68e0d)
input:kb_layout          live='br'
  .local/share/omarchy/default/hypr/input.conf:3        value=us
  .config/hypr/input.conf:10                            value=br
input:kb_options         live='compose:caps'
  .local/share/omarchy/default/hypr/input.conf:6        value=compose:caps
  .config/hypr/input.conf:11                            value=compose:caps
```

The declarer values are post-expansion: looknfeel.conf:15 and :51 read
`col.active_border = $activeBorderColor` / `col.border_active = $activeBorderColor`, and the theme
declares `$activeBorderColor = rgb(e68e0d)` at `.config/omarchy/current/theme/hyprland.conf:1`;
the defaults' earlier gradient with the `45deg` token is what the live read inherits. Spot-checked
by reading those exact lines (all six files, lines as listed) — the file:line numbers are the
lines the parser recorded, and the values match what the parser expanded them to.

## Clause-h conformance of `census-receipt.txt` (checked, not assumed)

Run against the exact clause-h regexes of `quality/counters/c2-r40-forms-entry.py:213-217`:

- `^forms int=(\d+) float=(\d+) str=(\d+) custom=(\d+)$` → matches `forms int=44 float=5 str=8
  custom=13`, sum 70.
- `^labels agreement=(\d+) agreement\*=(\d+) mismatch=(\d+) config-only=(\d+) live-default=(\d+)$`
  → matches `labels agreement=62 agreement*=8 mismatch=0 config-only=0 live-default=0`, sum 70.
- `A+B+C+D == W+X+Y+Z+V == 70 >= 1` holds; each pattern occurs exactly **once** in the file
  (`^forms ` count 1, `^labels ` count 1), so the entry can carry both lines verbatim without
  ambiguity.
- Placeholder line present verbatim: `tool sha256 <TOOLSHA>`.
- Host versions present: Hyprland 0.56.2 @ `efb50993780079460b0cbed1363e2166a2de1d9f`,
  hyprlang 0.6.8.
- Per-label key lists present for all five labels (empty labels marked `(none)`).
- 8 multi-declarer keys with each declarer's owner file:line present.
- Variant counts on a `variant-noinherit labels ...` line, i.e. it does **not** start with
  `labels ` and cannot be mistaken for the counted line.

## Risks / blockers for the L1

- **`<TOOLSHA>` is a placeholder by design.** At the lane tip `tools/mado-options.py` is still the
  base tool (`sha256 461f8c3c245bdfb6dcaac068a5ab378326c75dc91992b8012f9ca0e5019fb03a`, no
  `--live`), so clause h's `hashlib.sha256(tool).hexdigest() in rtext` cannot be satisfied yet.
  The L1 must substitute the delivered tool's sha at REV (and then the receipt's own sha changes,
  so the Gate line in `corpus/lessons/round-40.md` must bind the final receipt bytes).
- **Forms are counted through the module's own `native_query()`, not from the row JSON**, because
  a `--live` row carries no form field. Same function, same argv, same process model; the
  `census-driver.py.txt` bytes are kept so the L1 can re-derive. If the delivered tool adds a
  form field, prefer counting from its own output.
- **Receipt location.** The task names my seat directory; clause h requires the receipt committed
  under `.ufo/waves/round-40/fetch/`. The L1 must copy these bytes there (I did not write outside
  my seat).
- **Host-specific numbers.** 44/5/8/13 and 62/8/0/0/0 describe this host at 2026-10-25 17:49
  (-0300); a theme toggle or a compositor reload changes them. The receipt says so.
- **Label census independence.** The 62 `agreement` keys include values that pass through the
  reference's own conversion tables (bool spellings, weights, CSS gaps), so this receipt is
  evidence about the reference model, not an independent oracle. What it does add is the
  out-of-distribution host run the C1 residual asks for: 0 mismatch at 70/70, and the variant
  isolating exactly the two inheritance-dependent keys.

## Safety

- Compositor verbs run: `hyprctl getoption -j <key>` — 70 per live pass (the base `--live` run,
  the driver's forms pass, the variant pass) = 210 calls, plus 4 direct corroboration = 214; and
  `hyprctl version` once. No `keyword`/`dispatch`/`reload`/`setprop`/`--batch`, no socket of my own.
- Host config trees read-only: the reference's only `open(...,'w')` is `selftest._write()`
  (line 756), reachable only from `selftest()` with a mktemp home. Config file mtimes after the
  run are unchanged (e.g. `~/.config/hypr/hyprland.conf` 2026-10-17 17:02,
  `~/.config/omarchy/current/theme/hyprland.conf` 2026-10-03 17:49, all older than the 17:49 run).
- No pacman, no package transaction, no install — nothing was installed or updated this seat.
- Scratch in `/tmp` (`mado-options-ref.py`, `mado-options-ref-noinherit.py`, `census.py`,
  `census.json`, `live-out.json`, `live-noinherit.json`, `receipt.txt`) removed after the seat
  copies were made.
