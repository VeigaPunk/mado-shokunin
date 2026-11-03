# R65ExecRegisterBlock — report (mado round 65, wave w1)

Seat: `R65ExecRegisterBlock` (executor, leaf) · Lane: `/home/vgpnk/Projects/shokunin/mado-shokunin`
Base rev (contract): `524fa1f90b1f2de44b3019bacf833d54e0af13a0` · Lane HEAD at seat start: `cb63ab13ccaf85191318701d5db5ace050bd5bd4`
Date: 2026-11-03 · Scratch: `/fast/scratch/hyaku/mado-r65/w1/R65ExecRegisterBlock/` (removed at exit)
Wrote only inside the seat dir; `PROVINCE.md` was NOT edited (L1 integrates).

## Deliverable

`register-block-r65.md` — the exact block to append to `PROVINCE.md` (16 lines):
header line (frozen text, em dash included) → one-line provenance sentence → 4-column table
(`surface group | state (date) | probe (read-only) | receipt`) with exactly 8 data rows → sentinel
`<!-- r65 register end -->`.

sha256 `98af972dbea7da702d823faf5bc07d836c5d89c5d8df6a375d4d8fd863c442af`

Evidence log: `probe-log-r65.txt` (verbatim probe commands + outputs + rc, plus the supporting
checks that back the state-cell facts).

## Probes run (each is the verbatim command in its row's probe cell; rc is that command's own)

| # | group | probe | observed | rc |
|---|---|---|---|---|
| 1 | hypr plane | `command -v hyprctl && hyprctl version && hyprctl instances -j && test -d ~/.config/hypr` | `/usr/bin/hyprctl`; Hyprland 0.56.2 (commit efb5099…); 1 instance pid 1665 wayland-1; config dir present | 0 |
| 2 | waybar | `command -v waybar && waybar --version && pgrep -x waybar && test -d ~/.config/waybar` | `/usr/bin/waybar`; Waybar v0.15.0; pid 1720; config dir present | 0 |
| 3 | walker | `command -v walker && walker --version && test -d ~/.config/walker && systemctl --user is-active app-walker@autostart.service elephant.service` | `/usr/bin/walker`; 2.17.2; `active` `active` | 0 |
| 4 | terminal configs | `for d in alacritty foot kitty ghostty; do … test -d … command -v … done` | 4/4 config dirs present; only `alacritty` binary present (foot/kitty/ghostty `not found`) | 0 |
| 5 | theme/wallpaper omarchy plane | `test -d ~/.config/omarchy && test -d ~/.local/share/omarchy && cat …/theme.name && readlink …/background && if command -v swayosd …` | both dirs present; `matte-black`; background → `…/backgrounds/0-ship-at-sea.jpg`; `swayosd not found` | 0 |
| 6 | idle/lock plane | `for b in hypridle hyprlock hyprsunset; do … command -v …; done; for p in …; do if pgrep -x "$p" …` | 3/3 binaries under `/usr/bin`; `no process` for all three | 0 |
| 7 | omarchy skill docs | `test -d ~/.agents/skills/omarchy && readlink -f ~/.agents/skills/omarchy` | symlink → `/home/vgpnk/.local/share/omarchy/default/omarchy-skill` | 0 |
| 8 | windows desktop plane | `for b in powershell.exe pwsh powershell; do … if command -v "$b" …` | `not found` ×3 → not re-derivable here | 0 |

Supporting checks (in `probe-log-r65.txt`): `wc -l ~/.config/hypr/hyprland.conf` → 32 (rc=0);
`wc -l ~/.config/waybar/config.jsonc` → 260 (rc=0); skill leaf `sha256sum` →
`becd149e4d1c0767…` (rc=0, matches the gate's HELD pin); `cat ~/.local/share/omarchy/version` →
`3.8.3` (rc=0); `grep -nE timeout ~/.config/hypr/hypridle.conf` → `150`/`152` (rc=0);
`git ls-tree -r --name-only HEAD -- .ufo/waves/round-65/receipts` → all 6 receipts committed (rc=0).

## Counter-shape self-check (scratch only — the real C1 counter was not yet drafted)

`c1-sim.py` (scratch) re-implements the frozen C1 counting command line by line: git objects at
`--rev` only, block from `### Surface state register (2026-11-03` to the sentinel or next `## `,
rows = `|` lines with ≥3 non-empty cells, 8 exact first-cell group strings, receipt tokens matching
`\.ufo/waves/round-65/receipts/…\.(txt|json|md|sh)` verified against `git ls-tree -r`, gate leg =
a resolved receipt containing `MADO_VERIFY: CLEAN`.

| case | command | output | rc |
|---|---|---|---|
| do-nothing control, real lane at base | `python3 c1-sim.py --repo <lane> --rev 524fa1f9…` | `rows=0 groups=0/8 receipts=0 resolved=0 gate=missing verdict=TARGET_MISSED` | 1 |
| real lane at HEAD (receipts committed, block absent) | `… --rev cb63ab13…` | `rows=0 groups=0/8 … TARGET_MISSED` | 1 |
| scratch fixture: block appended + 6 receipts committed | `… --repo fx --rev e0c96c15…` | `rows=8 groups=8/8 receipts=15 resolved=15 gate=ok verdict=TARGET_MET` | 0 |
| negative fixture: windows-desktop row deleted | `… --repo fx-neg --rev e938229f…` | `rows=7 groups=7/8 receipts=14 resolved=14 gate=ok verdict=TARGET_MISSED` | 1 |

Fixture construction: `git init` inside `/fast/scratch/…/fx`, toplevel asserted
(`git rev-parse --show-toplevel` = fixture dir) before every mutation; `PROVINCE.md` copied from
the lane, block appended, and the append-only discipline proven by
`head -c <orig-size> PROVINCE.md | cmp - <lane>/PROVINCE.md` → identical.

Shape robustness (same fixture): a counter that also counts the header row sees `rows=9`, one that
counts header + separator sees `rows=10`; both satisfy `rows>=8` and `groups=8/8`. No data cell
contains a `|` character (pipe-free probes; `||` was rewritten as `if/then/else`), so the table
splits into exactly 4 cells per row under a naive `split('|')`.

## Findings

1. All eight frozen groups re-derive on this host; seven are **present** (2026-11-03) and the
   windows desktop plane is **not re-derivable** (no `powershell.exe`/`pwsh`/`powershell`), recorded
   honestly with the probe that shows it. The r57–64 Windows records stand, not retired.
2. Sub-state facts that a presence-only row would hide, and which the gate receipts confirm:
   idle/lock binaries are installed but **no consumer process runs** (the declared 150s/152s chain is
   unconsumed, F1/S1); the four terminal config trees exist but only **alacritty** is installed;
   `swayosd` is absent while its theme css part imports fine; theme is `matte-black` with the
   wallpaper link resolving inside the theme.
3. Every receipt path token in the block (15 tokens over 8 rows) resolves at lane HEAD; both gate
   receipts contain `MADO_VERIFY: CLEAN` (file plane 29 pass / 0 fail / 0 unknown; live 52 / 0 / 0).
4. The 2026-10-31 block stays untouched: `grep -c 'absent (2026-10-31)' PROVINCE.md` remains 7 by
   design (append-only supersession), and the new provenance sentence says nothing in it is claimed
   about this host.

## Defects / risks (for the L1)

- **D1 — windows row has no direct receipt.** No round-65 receipt captures the powershell-absence
  probe, so that row points at `before-register-probes-r65.txt` (host identity) and its state cell
  says so. If a direct pointer is wanted, add
  `.ufo/waves/round-65/receipts/windows-plane-absence-r65.txt` with this seat's probe output and
  repoint the row — do **not** add a ninth row (the counter requires exactly the 8 group strings;
  extra rows still pass `rows>=8` but add no group).
- **D2 — real C1 counter absent at write time** (`.ufo/waves/round-65/w1/R65ExecC1Counter/` was
  empty). The block is shaped to the frozen spec and proven against a spec re-implementation; the
  real counter must be run at the landing rev.
- **D3 — integration detail.** `PROVINCE.md` currently ends with a prose line; insert one blank line
  before appending the block header (cosmetic only — the counter is line-based and the fixture with
  the blank line also reports `TARGET_MET`).
- **D4 — live gate NOTEs not in the 8 rows.** `hypr.file.sha_pin` (drift from the round-1 pin) and
  `hypr.backups` (2 backup files, S3 litter class) are live facts recorded in
  `gate-fileplane-r65.txt`, not in the register rows (the register's granularity is the 8 groups).
- **D5 — receipt-column shape.** Rows cite up to two receipts as bare, space-separated tokens (no
  backticks, no commas) so both token-based and cell-based extraction resolve them; the windows row
  cites one.

## Security / process

No r56-era material opened; no credential-shaped output captured or printed; no config tree,
compositor state or service mutated (`hyprctl` only queried); no git/jj mutation in the lane
(read-only `ls-tree`, `show`, `rev-parse` only; fixture mutations confined to scratch with the
toplevel asserted). Installs/upgrades: **none**. Scratch removed at exit; deliverables and the probe
log are in this seat dir.
