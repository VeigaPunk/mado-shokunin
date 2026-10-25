# RevQuoteS208 — row S208 attacked, agreement confirmed

Seat: `L1Mado35.RevQuoteS208` · Round 35, wave 2 · 2026-10-25
Scope: registry row **S208** only (`corpus/SOURCES.md` line 210), its live host source, its
receipt, and the gate-quote the r15 entry records for it. Read-only; no lane artifact edited.
Scratch: `.ufo/waves/round-35/scratch/RevQuoteS208/evidence.txt`.

## Verdict

**No divergence on any axis.** Every anchor, every transcribed byte, and both frozen counters
agree with the row as written. S208 survives the attack.

Axes named and probed: (1) live-source identity, (2) gate-quote contiguity, (3) quoted-fact
truth, (4) hash-anchor equality, (5) row well-formedness, (6) counter reproduction,
(7) surface reachability (evidence must describe something the desktop actually offers).

## (a) Live source re-open — identity holds

```
$ sha256sum /home/vgpnk/.local/share/omarchy/bin/omarchy-menu
d196b086e961d524945a899c5eb6e1aa532d9594c924d78b78c1fff183a0f79d
$ wc -c /home/vgpnk/.local/share/omarchy/bin/omarchy-menu
33017
```
Both exit 0; identical to the values in the row's anchor cell (33017 B, sha `d196b086…0f79d`).

Lines 205–214, numbered, as seen on the host:

```
205
206  show_toggle_menu() {
207    local options="󱄄  Screensaver\n󰔎  Nightlight\n󱫖  Idle Lock\n󰂛  Notifications\n󰍜  Top Bar\n󱂬  Workspace Layout\n  Window Gaps\n  1-Window Ratio\n󰍹  Monitor Scaling\n  Direct Boot\n󰟵  Passwordless Sudo"
208
209    case $(menu "Toggle" "$options") in
210    *Screensaver*) omarchy-toggle-screensaver ;;
211    *Nightlight*) omarchy-toggle-nightlight ;;
212    *Idle*) omarchy-toggle-idle ;;
213    *Notifications*) omarchy-toggle-notification-silencing ;;
214    *Bar*) omarchy-toggle-waybar ;;
```

`grep -n -i idle` over the whole file returns only 207 and 212 in the Toggle menu (the other
hits are `Hypridle` in the Setup/Restart/Reset menus, separate `case` blocks with their own
patterns — no cross-match with `*Idle*`).

## (b) Gate-quote — contiguous, whole line, byte-identical

Quote as recorded in `corpus/knowledge/idle-lock-offered-in-the-bar-r15.md`:
`located: omarchy-menu line 207 lists Idle Lock among the toggles; line 212 dispatches omarchy-toggle-idle`
(105 bytes, 14 words — inside the counter's 1–25 word bound).

```
$ grep -c -F '<quote>' .ufo/waves/round-35/fetch/S208.receipt.txt   -> 1   (exit 0)
$ grep -bo -F '<quote>' …                                          -> 662:<quote>
```
Byte-level: receipt is 768 B; the quote occupies 662..766, byte 661 is `LF`, byte 767 is `LF`.
It is therefore **one complete line, occurring exactly once**, not a quote assembled across
lines. The entry's `gate-quote: S208 ` remainder compares equal to the receipt substring
character for character (Python bytes compare, `True`).

Two harder checks the hash cannot cover, since the anchor hashes the *file* and not the
receipt's transcription:

| check | result |
|---|---|
| receipt line `207:…` payload vs live line 207 bytes | equal (235 B = 235 B) |
| receipt line `212:…` payload vs live line 212 bytes | equal (32 B = 32 B) |
| receipt `dispatch arm count` vs `grep -c omarchy-toggle-idle` live | 1 = 1 |

**Facts still match the host.** "line 207 lists Idle Lock among the toggles" — line 207 is the
`$options` string rendered under the menu title `Toggle` at line 209, and `Idle Lock` is in it.
"line 212 dispatches omarchy-toggle-idle" — exactly `*Idle*) omarchy-toggle-idle ;;`.
`omarchy-toggle-idle` exists and is executable (`…/omarchy/bin/omarchy-toggle-idle`, 316 B,
sha `11979b4d…b284`); its body starts/stops `hypridle`, matching the row's gloss "the entry
that switches the idle lock".

## (c) Receipt hash vs anchor cell

```
$ sha256sum .ufo/waves/round-35/fetch/S208.receipt.txt
6e72f0db3d7bbfecf4096b0aa22f716f417c00caa50b6d3319106387d6ce4654   (768 B)
```
Machine extraction of the row (11 cells, matching the header, no embedded pipe, exactly one
`| S208 |` row) confirms cell 6 contains **both** hashes: live file `d196b086…0f79d` and
receipt `6e72f0db…4654`. The frozen spec's `receipts["S208"].sha256` equals the same value.
Status `mined`, recheck `on-change`, used-by `corpus/knowledge/idle-lock-offered-in-the-bar-r15.md`.

Staleness: receipt is stamped "host re-open 2026-10-24"; today's independent re-open
(2026-10-25) yields the identical digest, so `on-change` is satisfied and the anchor is not
stale. Menu mtime 2026-10-03 17:42:32 is older than the receipt, consistent with "unchanged
since".

## Counters reproduce the frozen claim

```
$ python3 -I .ufo/waves/round-35/c1/count.py --root . --frozen .ufo/waves/round-35/c1/frozen.json
PRED-C1-r35-v1 closed_entries=3 closed_rows=8 open_cites=0 verdict=TARGET_MET      exit 0
$ python3 -I .ufo/waves/round-35/c2/count.py --repo . --frozen .ufo/waves/round-35/c2/frozen.json
PRED-C2-r35-v1 uncovered=0 retired=1 toctou_declared=1 ledger_tip_ok=1 verdict=TARGET_MET   exit 0
```
The c1 spec lists exactly 8 ids across the 3 entries (S203–S210); with `closed_rows=8` and
`open_cites=0`, S208 is among the rows the frozen predicate counts closed, and the predicate's
own conditions (`row is not None`, `nf_ok`, `used_by == citing`, `cs[7]=="mined"`,
`valid_recheck`, `receipt sha in cs[5]`, `quote in blob`, word bound) are each independently
re-confirmed above.

## Reachability — the surface is genuinely offered

The row asserts a *second surface*, so I checked the evidence describes live UI rather than
dead code: `show_toggle_menu` is called from `show_main_menu → Trigger → *Toggle*)` (lines
96/101) and from argv dispatch `go_to_menu *toggle*)` (line 860, reached via `$1` at 886–888).
`~/.local/share/omarchy/default/hypr/bindings/utilities.conf:5` binds
`SUPER CTRL, O, Toggle menu, exec, omarchy-menu toggle`, `~/.config/hypr/hyprland.conf:8`
sources that file, and no `unbind` of the chord exists in `~/.config/hypr` (grep exit 1).
`type -a omarchy-menu` resolves to exactly one copy — the receipt path — so no PATH shadowing
puts a different menu in the operator's hands. Omarchy version 3.8.3.

## Residual risk and verification gaps

1. **No UI observed.** The menu was not opened and no toggle was run (consistent with the
   entry's own "no menu was opened" declaration). The surface claim rests on code path plus a
   sourced keybind, not on a rendered screen. Reading the file cannot distinguish, e.g., a
   runtime failure in `walker`/`menu()` that would stop the menu from appearing.
2. **`*Idle*` is a glob, not a literal.** It would also fire for any future option containing
   `Idle`. Today the Toggle list has exactly one such option (`Idle Lock`), so the dispatch is
   unambiguous; this is an observation about brittleness, not a current error.
3. **Same-entry rows S207 and S209 have no quote-verification seat in this wave's roster**
   (seats exist for S203, S204, S205, S206, S208, S210). S209 backs the entry's "four dated
   copies" claim, which I did not verify — flagging the gap for whoever owns row-level
   coverage, not as an S208 defect.
4. The row's "same command" wording is correct as a name match (`omarchy-toggle-idle` in both
   the bar `on-click`, verified at `~/.config/waybar/config.jsonc:208`, and the menu arm); I
   verified the menu side and the bar side as files, not the toggle's runtime effect.

## Tooling

No installs or upgrades. Only coreutils, `grep`, `nl`, and `python3 -I` (read-only) were used;
the scratch directory and this report are the only writes.
