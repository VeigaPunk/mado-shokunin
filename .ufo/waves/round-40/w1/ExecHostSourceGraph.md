# ExecHostSourceGraph — host source-graph derivation (w1, round 40)

Seat: ExecHostSourceGraph (leaf). Lane: `/home/vgpnk/Projects/shokunin/mado-shokunin`.
Date: 2026-10-25. Claims frozen at `registration.md` (commit 5e7e885…, base 9fc511d…).

**Result in one line:** an independent byte-walk of the host Hyprland tree finds **78 option
declarations over 70 distinct option keys, of which exactly 8 keys are declared more than once** —
the same 8 the L1 calls `agreement*`; **set difference is empty in both directions**. The walk
reproduces the delivered tool's static table on all 70 rows (owner, line, expanded value) without
reading or importing `tools/mado-options.py`.

## 1. Method (independent of the tool)

`derive.py` (this seat) walks `~/.config/hypr/hyprland.conf` depth-first in file order, expands
every `source =` at the position it appears (`~` expanded; globs sorted), maintains the hyprlang
variable table **at use time**, tracks brace nesting into dotted `category:sub:key` paths, strips
`#` comments (quote-aware), and records every `key = value` as `{file, line, as-written,
expanded}`. It never reads `tools/mado-options.py`; standard library only; the host tree is only
read.

Walk accounting (`graph.json`, `derive.py`):

| item | count |
|---|---|
| files walked | 40 (root + 39 sourced; no file visited twice, 0 cycles) |
| `source =` directives | 38, **0 unmatched** |
| glob sources | 1: `~/.local/state/omarchy/toggles/hypr/*.conf` → `flags.conf`, `window-no-gaps.conf` |
| option declarations kept | 78 |
| distinct option keys | 70 |
| keys with >1 declarer | **8** |
| excluded (not options) | 192 `bind*` (163 `bindd`, 14 `bindeld`, 10 `bindld`, 2 `bindmd`, 2 `bindl`, 1 `binddr`), 10 rule fields inside `windowrule {}` blocks, 129 `env`, 77 `windowrule`, 38 `source`, 15 `animation`, 13 `exec-once`, 5 `bezier`, 2 `layerrule`, 1 `monitor` |

Classification is corroborated by the compositor's own registry: `hyprctl descriptions -j` lists
353 option names and **all 70 of my derived keys are in it; none of the excluded rule fields is**
(`descriptions.json`; `name`, `fullscreen`, `match:class`, `idle_inhibit`, `no_follow_mouse` are
absent from the registry). Two `*.bak.*` files sit in `~/.config/hypr` and are not reached — they
are not `source`d, so they cannot declare anything.

## 2. The 8 keys declared more than once (declarers, as written)

Order is walk order; the last declarer is the one that wins (`compare.txt`).

| # | key | declarer 1 (file:line, as written) | declarer 2 = last (file:line, as written) | shadow changes value? |
|---|---|---|---|---|
| 1 | `decoration:rounding` | `…/omarchy/default/hypr/looknfeel.conf:29` → `0` | `…/state/omarchy/toggles/hypr/window-no-gaps.conf:9` → `0` | no (identical) |
| 2 | `general:border_size` | `…/default/hypr/looknfeel.conf:12` → `2` | `…/toggles/hypr/window-no-gaps.conf:5` → `0` | yes |
| 3 | `general:col.active_border` | `…/default/hypr/looknfeel.conf:15` → `$activeBorderColor` (→ `rgba(33ccffee) rgba(00ff99ee) 45deg`) | `~/.config/omarchy/current/theme/hyprland.conf:4` → `$activeBorderColor` (→ `rgb(e68e0d)`) | yes (colour; angle inherited) |
| 4 | `general:gaps_in` | `…/default/hypr/looknfeel.conf:9` → `5` | `…/toggles/hypr/window-no-gaps.conf:4` → `0` | yes |
| 5 | `general:gaps_out` | `…/default/hypr/looknfeel.conf:10` → `10` | `…/toggles/hypr/window-no-gaps.conf:3` → `0` | yes |
| 6 | `group:col.border_active` | `…/default/hypr/looknfeel.conf:51` → `$activeBorderColor` (→ gradient, `45deg`) | `~/.config/omarchy/current/theme/hyprland.conf:8` → `$activeBorderColor` (→ `rgb(e68e0d)`) | yes (colour; angle inherited) |
| 7 | `input:kb_layout` | `…/default/hypr/input.conf:3` → `us` | `~/.config/hypr/input.conf:10` → `br` | yes |
| 8 | `input:kb_options` | `…/default/hypr/input.conf:6` → `compose:caps` | `~/.config/hypr/input.conf:11` → `compose:caps` | no (identical) |

Source order that produces this: `hyprland.conf:10` (defaults `looknfeel`) → `:13` (theme) →
`:17` (user `input.conf`) → `:23` (toggles glob). The theme redefines `$activeBorderColor` at
`theme/hyprland.conf:1`, after the defaults already used it.

## 3. Set difference against the L1's 8 `agreement*` keys

L1 sources: `registration.md` states the count ("62 agreement / 8 agreement* / 0 mismatch") and
`make-w1-spec.py` states the definition ("the 8 keys with more than one declarer") but **neither
enumerates the keys**. The only enumeration in the wave is the census receipt
`w1/ExecLiveCensus/census-receipt.txt:25`. Comparison against it (`compare.py` → `compare.txt`):

```
derived keys with >1 declarer : 8      L1 census agreement* : 8 (8 keys listed)
mine - L1 : (empty)
L1 - mine : (empty)
```

Both directions empty; the count claim (8) is also reproduced independently. Because the
enumeration comes from a sibling artifact, I did not rest on it: for all 8 keys my own
`hyprctl getoption -j` receipt (`live-8.txt`) shows the live value matching the last declarer
after host-style conversion — `rounding`→`int 0`, `border_size`→`int 0`, `col.active_border`→
`custom "ffe68e0d 45deg"`, `gaps_in`/`gaps_out`→`custom "0 0 0 0"`, `col.border_active`→
`custom "ffe68e0d 45deg"`, `kb_layout`→`str "br"`, `kb_options`→`str "compose:caps"`, all
`set=true`. So the `agreement*` label holds for exactly this 8-key set on live evidence, not on a
sibling's say-so.

## 4. Model checks the derivation rests on (each with its own evidence)

- **Last declarer wins.** `general:gaps_in` live `0 0 0 0` (toggles:4, not defaults:9 `5`);
  `input:kb_layout` live `br` (user:10, not defaults:3 `us`); `general:col.active_border` live
  `ffe68e0d` (theme:4 colour, not defaults:15).
- **Variable expansion is at use time, not late-bound.** `group:col.border_locked_active` has a
  single declarer, `defaults/looknfeel.conf:53 = $activeBorderColor`, and reads
  `custom "ee33ccff ee00ff99 45deg"` — the *defaults* gradient, although the theme later redefines
  the variable. Under a late-bound model it would read `ffe68e0d`.
- **Angle inheritance is real, and is not the registry default.** `hyprctl descriptions -j` gives
  `general:col.active_border default "ffffffff 0deg"` (and `group:col.border_active default
  "66ffff00 0deg"`), yet live is `ffe68e0d 45deg`. The `45deg` can only come from the shadowed
  defaults declarer (`looknfeel.conf:15`). Control in the same class: `group:col.border_inactive`
  (one declarer, `rgba(595959aa)`, no `deg` token) reads `aa595959 0deg` — the registry angle.
  This directly supports the C2 entry's angle-inheritance sentence and C1's "gradient redeclared
  without an angle inherits the previous declarer's angle".
- **Comments are stripped, not part of the value.** `input:kb_options` last declarer is
  `compose:caps # ,grp:alts_toggle`; live is `compose:caps`.
- **Glob order is not load-bearing here.** Only `window-no-gaps.conf` of the two globbed files
  declares anything, so any glob ordering yields the same last declarer.

## 5. Cross-check against the delivered tool (comparison step only)

`python3 -I tools/mado-options.py --home $HOME` (`tool-static.txt`) returns 70 rows.
- Key sets: `tool − mine = ∅`, `mine − tool = ∅`.
- All 70 rows agree on **owner file, line and expanded value**: 0 disagreements.
- 6 rows differ if compared on *as-written* text instead of expanded: `general:col.active_border`,
  `general:col.inactive_border`, `group:col.border_active`, `group:col.border_inactive`,
  `group:col.border_locked_active`, `group:col.border_locked_inactive` — all `$var` uses. This is
  a representation difference (the tool stores expanded values), **not** a defect; I state it so
  the counter's "value" column is not mistaken for literal file text.

## 6. Findings that attack or qualify other round-40 statements

1. **`hyprctl descriptions -j` "current" is not live config state.** It reports
   `general:gaps_in current "5 5 5 5"`, `general:border_size current 1`, `decoration:rounding
   current 0`, `general:col.active_border current "ffffffff 0deg"` — i.e. the registry defaults —
   while `hyprctl getoption -j` reports `0 0 0 0`, `0`, `0`, `ffe68e0d 45deg`. Any round-40 text
   that treats `descriptions` as the running configuration is unsupported by these bytes; only
   `getoption -j` carries the applied value.
2. **"8 shadowed" ≠ "8 changed by shadowing".** Two of the eight pairs write the same value
   (`decoration:rounding` `0`→`0`, `input:kb_options` `compose:caps`→`compose:caps`). Six are
   value-changing. A counter or entry that equates the two counts would be wrong by 2.
3. **"last declarer outside the defaults tree" is not the shadowed set.** 13 tool rows have a
   non-defaults owner (7 `user`, 4 `toggles`, 2 `theme`), but 5 of them
   (`input:numlock_by_default`, `input:repeat_delay`, `input:repeat_rate`,
   `input:touchpad:clickfinger_behavior`, `input:touchpad:scroll_factor`) are user-only
   declarations with **no** defaults declarer. Equating the two would over-count by 5; the correct
   test is "≥2 declarers", which is what `derive.py` computes.
4. **Coverage of the graph:** the two `~/.config/hypr/*.bak.*` files and
   `~/.local/share/omarchy/default/hypr/plain-bindings.conf` / `bindings/tiling.conf` (present on
   disk) are **not** reached by any `source =` from `hyprland.conf`; they are correctly outside
   the option graph.

## 7. Scope, safety, tools

- Written only: this report and `w1/ExecHostSourceGraph/{derive.py, compare.py, graph.json,
  compare.txt, tool-static.txt, live-8.txt, descriptions.json, err.txt}`. No tracked file, no
  config tree, no `.ufo/state/`, no git/jj command of any kind.
- Compositor verbs used: `hyprctl version`, `hyprctl getoption -j <key>`, `hyprctl descriptions -j`
  — read-only; no `keyword`/`dispatch`/`reload`/`--batch`; no socket of my own; pacman untouched.
- Tools installed: **none** (no version to record).
- No subagent dispatch, no background job.

## 8. Reproduce

```
cd /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-40/w1/ExecHostSourceGraph
python3 -I derive.py > graph.json          # independent walk, 70 keys / 8 duplicated
python3 -I compare.py                      # set difference vs the census agreement* line
```

## 9. Residual / risk

- The comparison's *enumeration* side depends on `w1/ExecLiveCensus/census-receipt.txt:25`, a
  sibling artifact that was in flight when read; my own derivation and my own `getoption` receipt
  agree with it, so the conclusion does not hinge on that file, but the byte-level claim "the L1's
  8 keys are these 8" is only as strong as that artifact (the L1 spec itself gives the count and
  the definition, not the list).
- Values are labelled only for the 8 duplicated keys on live evidence; I did not re-run the full
  70-key census (that is ExecLiveCensus's assignment), so I make no claim about the other 62
  labels beyond the structural one (they each have exactly one declarer: 78 = 8×2 + 62×1).
