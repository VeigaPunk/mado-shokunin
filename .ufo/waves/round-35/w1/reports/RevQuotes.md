# RevQuotes — S203–S210 gate-quote re-verification at source

Seat: reviewer (leaf). Re-opened each of the eight `gate-quote:` lines at its
declared SOURCE, not the receipt. Quotes parsed from the staged entries at
`.ufo/waves/round-35/scratch/ExecCensusScratch/validate/corpus/knowledge/*.md`
(format `gate-quote: S### located: <quote>`); `teaches` cells from
`.ufo/waves/round-35/controls/golden/corpus/SOURCES.md` (the pending rows are not
yet appended to the lane registry — the ExecCensusScratch mirror's SOURCES.md ends
at S202, so the control-tree golden is the authoritative row text).

Method: byte substring test of the quote against the source bytes; word count by
whitespace split; independent re-measurement of the underlying facts on the host.

| id | quote ⊆ source bytes | words (≤25) | grounds `teaches` | verdict |
|---|---|---|---|---|
| S203 | **No** — receipt-composed summary | 13 | yes (see note) | GROUNDED-BY-FACT |
| S204 | yes — receipt IS the source | 12 | yes | PRESENT-AT-SOURCE |
| S205 | yes — receipt IS the source | 16 | yes | PRESENT-AT-SOURCE |
| S206 | **No** — receipt-composed summary | 12 | yes | GROUNDED-BY-FACT |
| S207 | **No** — receipt-composed summary | 14 | yes | GROUNDED-BY-FACT |
| S208 | **No** — receipt-composed summary | 13 | yes | GROUNDED-BY-FACT |
| S209 | yes — receipt IS the source | 12 | yes | PRESENT-AT-SOURCE |
| S210 | yes — receipt IS the source | 14 | yes | PRESENT-AT-SOURCE |

All eight quotes pass the predicate's mechanical clause (contiguous substring of
the receipt bytes, 1–25 words). The word bound is satisfied everywhere
(12–16 words). The interesting split is the source-byte test.

## Per-id findings

**S203** — source `/home/vgpnk/.local/share/omarchy/bin/omarchy-first-run` re-read
verbatim (28 lines). The quote `install/first-run/ lists 12 scripts; the
omarchy-first-run body runs all 12; none is idle-lock` is absent from the file —
it is the receipt's `located:` summary line. Underlying facts verify: the body
invokes exactly 12 `bash "$OMARCHY_PATH/install/first-run/*.sh"` calls
(battery-monitor, recover-internal-monitor, cleanup-reboot-sudoers, firewall,
dns-resolver, gnome-theme, swayosd, gtk-primary-paste, text-scaling, elephant,
welcome, wifi) and zero occurrences of `idle`. Precision note: the
`install/first-run/` directory on this host lists **13** entries — the same 12
`.sh` files plus `install-voxtype.hook`, which the body *installs* via
`omarchy-hook-install` (line 23) but does not run as a script. Teaches
enumerates exactly the 12 run scripts and claims no idle-lock question —
consistent. Grounding holds by fact, not by literal text.

**S204** — receipt is the declared source; quote is verbatim in its `located:`
line and the two claims re-verify live: `journalctl --user --no-pager` currently
contains 0 `omarchy-toggle` lines (re-measured), and the first-run script count
is 12 bash-invoked scripts (13 dir entries; same hook caveat). Grounds the
`teaches` cell (setup offers no question; journal holds zero invocations).

**S205** — receipt is the declared source; quote verbatim in `located:` line.
Live re-check: `pgrep -a hypridle` → `1667 /usr/bin/hypridle`;
`systemctl --user is-active hypridle` → `inactive`;
`hypridle.conf` declares `timeout = 150` and `timeout = 152`. The teaches claim
(daemon armed; unit probe reads inactive because the daemon sits in a transient
scope) is consistent with the receipt's captured journal start lines (Oct 23
13:25:00 and 22:14:11). Grounds.

**S206** — source `/home/vgpnk/.config/waybar/config.jsonc` re-read at lines
14–22 and 203–214. Quote `waybar config.jsonc line 207 opens the
custom/idle-indicator module; line 208 runs omarchy-toggle-idle` is absent from
the file (summary prose). Facts verify: L207 `"custom/idle-indicator": {`,
L208 `"on-click": "omarchy-toggle-idle"`, L18 registers the module in
`modules-center`; the `omarchy-toggle-idle` handler occurs exactly once.
Grounds teaches (a dedicated module whose click toggles the lock).

**S207** — source `.../indicators/idle.sh` re-read verbatim (7 lines). Quote is
receipt summary, absent from the file. Facts verify: `pgrep -x hypridle` branch
emits `{"text": ""}`; else emits the icon + `"tooltip": "Idle lock disabled"` +
`"class": "active"`. Grounds teaches (desktop's own two-state vocabulary:
nothing when running, "Idle lock disabled" when not).

**S208** — source `/home/vgpnk/.local/share/omarchy/bin/omarchy-menu` re-read at
lines 204–217. Quote is receipt summary, absent from the file. Facts verify:
L207's `options` string contains `󱫖  Idle Lock` among 11 toggle entries; L212 is
`*Idle*) omarchy-toggle-idle ;;` — the same command the bar module's click runs.
Grounds teaches (second surface offering the choice, same dispatch).

**S209** — receipt is the declared source; quote verbatim in `located:` line.
Re-measured: four backups under `~/.config/waybar` (`config.jsonc.bak`,
`.bak.1791314470`, `.bak.1792203278`, `.bak.1792267376`) each contain exactly one
`omarchy-toggle-idle` occurrence; oldest mtime 2026-10-03 17:44 (the
`.1791314470` copy). Grounds teaches (offer is not a recent addition). Minor
wording: `.bak` has no date suffix — "dated copies" rests on mtimes; harmless.

**S210** — receipt is the declared source; quote verbatim in `located:` line.
Re-measured: `~/.local/state/omarchy/toggles/hypr/` holds exactly
`flags.conf` and `window-no-gaps.conf`; 0 files' text names the idle lock.
Grounds teaches (the toggle record exists; the idle lock has no entry).

## Observations

1. **Quote-class asymmetry.** For the four rows whose declared source is a
   receipt (S204, S205, S209, S210) the quote is a true verbatim substring of the
   source bytes. For the four file-anchored rows (S203, S206, S207, S208) the
   quote is a *receipt-composed summary* — verbatim in the receipt, absent from
   the named file. The predicate's clause (quote ⊆ receipt bytes) cannot detect
   this: anchoring on the receipt makes every `located:` line self-satisfying.
   Facts underneath all eight re-verify on the live host, so no row's `teaches`
   is ungrounded — but if the round intends gate quotes to be source-verbatim
   payloads (the standard the r32 quarantine applied), S203/206/207/208 carry a
   quote-class the frozen spec does not distinguish.
2. **S203/S204 count nuance.** "12 scripts" holds only for bash-invoked `.sh`
   files; the directory lists 13 entries including `install-voxtype.hook`.
   Teaches names the same 12 — precise, no defect, but a strict reader of
   `install/first-run/` will count 13.
3. **No word-bound violations.** Max quote is 16 words (S205); bound is 25.
