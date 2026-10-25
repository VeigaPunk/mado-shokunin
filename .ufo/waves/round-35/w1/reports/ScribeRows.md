# ScribeRows — round 35 wave 1 report

Seat: ScribeRows. Scope: draft the eight new registry rows (S203–S210) in the lane's
SOURCES.md schema, in scratch only, using the committed receipts under
`.ufo/waves/round-35/fetch/` for digests and located quotes. No lane file was touched.

## Evidence surface

- Schema: `| id | source | kind | tier | scope | anchor | teaches | status | opened | recheck | used-by |` — 11 cells, from `corpus/SOURCES.md:11`.
- Admission rules checked against `.ufo/waves/round-35/c1/count.py`: exactly 11 cells,
  `status=mined`, `recheck` a cadence token (`YYYY-MM-DD`, `NNd`, or symbolic
  `[A-Za-z][A-Za-z0-9 _-]*`), anchor cell must contain the receipt's sha256, `used-by`
  must equal the frozen cite set, no literal or escaped pipe (`\|` splits a cell into
  two — the package rows S327/S340/S342 carry `find … \| wc -l` inside `recheck` and
  therefore explode to 12 cells; that prose is dropped, not escaped).
- Receipts re-hashed live during validation: all eight sha256s match `c1/frozen.json`.
- Package id remap measured, not assumed: the same eight documents sit at merge-package
  ids S315, S316, S327, S335, S336, S337, S340, S342 — the registration's listed set
  (S309, S310, S321, S329, S330, S331, S334, S336) is wrong; only S336 coincides.
- Draft: `.ufo/waves/round-35/scratch/ScribeRows/draft.md`.

## Verification

Probe root `.ufo/waves/round-35/scratch/ScribeRows/probe-root/` = golden entries +
committed receipts + my eight rows as `corpus/SOURCES.md`. Command:

```sh
python3 -I .ufo/waves/round-35/c1/count.py --root .ufo/waves/round-35/scratch/ScribeRows/probe-root --frozen .ufo/waves/round-35/c1/frozen.json
```

Output: `PRED-C1-r35-v1 closed_entries=3 closed_rows=8 open_cites=0 verdict=TARGET_MET`, exit 0.

## The eight rows, verbatim

| id | source | kind | tier | scope | anchor | teaches | status | opened | recheck | used-by |
|---|---|---|---|---|---|---|---|---|---|---|
| S203 | host omarchy first-run installer - the desktop's post-login questionnaire on this host - /home/vgpnk/.local/share/omarchy/bin/omarchy-first-run | own-work | A | Whether the desktop's setup path asks the operator about the idle lock, and therefore whether an intent could have been recorded at setup | body lines 3 and 8-27 at /home/vgpnk/.local/share/omarchy/bin/omarchy-first-run, 1089 B, file sha256 20508471d8237a60e630baf58f87c0b5a4391e34196ce11e5034745f6a062630; receipt .ufo/waves/round-35/fetch/S203.receipt.txt sha256 1b7fa87ffe933990ee59acf3629ffbe3a90106bc9ebcce082237f7f495dd1646 | The post-login questionnaire runs twelve first-run scripts - battery monitor, internal monitor, sudoers cleanup, firewall, DNS resolver, GNOME theme, swayosd, primary paste, text scaling, elephant, welcome and wifi - and none of the twelve asks about the idle lock | mined | 2026-10-24 | on-request | corpus/knowledge/idle-lock-never-asked-r12.md |
| S204 | host evidence that the idle lock was never asked about and never toggled - the installer's script count and the journal's absence of any omarchy-toggle invocation (measured on this host) - .ufo/waves/round-35/fetch/S204.receipt.txt | own-work | A | The paired negative: the setup path never offers the choice, and the operator never made it afterwards either | sections command and first-run scripts run by the installer in .ufo/waves/round-35/fetch/S204.receipt.txt; receipt sha256 4cd5ba6518e4a6d950fcb510d2482e33be78abb20d22bef41d21a66f7d1c54ad | Two independent negatives agree: the setup path offers no idle-lock question (12 first-run scripts, none about idle) and the user journal holds zero omarchy-toggle invocations | mined | 2026-10-24 | on-request | corpus/knowledge/idle-lock-never-asked-r12.md |
| S205 | host idle-lock chain - the daemon's present liveness, the unit probe, the journal start lines and the two declared timeouts (measured on this host) - .ufo/waves/round-35/fetch/S205.receipt.txt | own-work | A | The state of the idle lock the operator's preference would be about | sections process probe, unit probe, journal start lines and declared timeouts in .ufo/waves/round-35/fetch/S205.receipt.txt; hypridle.conf sha256 e7d3b8dd983523e4defbfbacfd7ed73fc55407e175766bf44542e5708307de41; receipt sha256 f3387bfcbac79016034be38bab6548ae31df5860e5aafaa03105aca84b08ae1a | The idle lock is armed on this host: hypridle runs as pid 1667 and the journal holds two start lines on 2026-10-23, while the unit probe reads inactive only because the daemon runs inside a transient scope, so the process probe is the true reading; the declared chain is a screensaver at 150 s and a lock at 152 s | mined | 2026-10-24 | 90d | corpus/knowledge/idle-lock-chain-armed-r14.md |
| S206 | host waybar configuration - the idle-indicator module whose click toggles the idle lock - /home/vgpnk/.config/waybar/config.jsonc | own-work | A | Whether the desktop ever offers the operator the idle-lock choice | lines 207-212 and 18-19 at /home/vgpnk/.config/waybar/config.jsonc, 6354 B, file sha256 a408a33df48a39dc16214124dd0b86d6ab03e13802bac173146ae8a858aae829; receipt .ufo/waves/round-35/fetch/S206.receipt.txt sha256 1d30e4a999b53d5288369edc7573d7ceee0aef99570a55d781c4625440a938d5 | The bar carries a dedicated idle-indicator module whose click runs the idle-lock toggle, so the choice is offered in the running interface and not only at setup | mined | 2026-10-24 | on-change | corpus/knowledge/idle-lock-offered-in-the-bar-r15.md |
| S207 | host waybar indicator script - the idle indicator, which renders the idle lock's state - /home/vgpnk/.local/share/omarchy/default/waybar/indicators/idle.sh | own-work | A | The desktop's own two-state vocabulary for the idle lock | lines 3-6 at /home/vgpnk/.local/share/omarchy/default/waybar/indicators/idle.sh, 159 B, file sha256 6d8d2c11d3c3b15fa0aa31a830410c98d9e630a7683a9cedffb888d10f0f1750; receipt .ufo/waves/round-35/fetch/S207.receipt.txt sha256 81c33e7926f0bad071d31e9fc67e1d06967e3142da40ea3c93b16510b0adec59 | The indicator asks whether hypridle is running and renders nothing when it is, and an icon carrying the tooltip Idle lock disabled when it is not - so the desktop names the two states itself | mined | 2026-10-24 | on-change | corpus/knowledge/idle-lock-offered-in-the-bar-r15.md |
| S208 | host omarchy menu script - the Toggle submenu entry that switches the idle lock - /home/vgpnk/.local/share/omarchy/bin/omarchy-menu | own-work | A | The second surface that offers the idle-lock choice | lines 207 and 212 at /home/vgpnk/.local/share/omarchy/bin/omarchy-menu, 33017 B, file sha256 d196b086e961d524945a899c5eb6e1aa532d9594c924d78b78c1fff183a0f79d; receipt .ufo/waves/round-35/fetch/S208.receipt.txt sha256 6e72f0db3d7bbfecf4096b0aa22f716f417c00caa50b6d3319106387d6ce4654 | The desktop's own menu lists an Idle Lock entry among its toggles and dispatches it to the same command, so the choice is offered in two independent surfaces | mined | 2026-10-24 | on-change | corpus/knowledge/idle-lock-offered-in-the-bar-r15.md |
| S209 | host waybar configuration backups - the dated copies of the bar's configuration and the idle-lock handler in each (measured on this host) - .ufo/waves/round-35/fetch/S209.receipt.txt | own-work | A | How long the idle-lock choice has been on offer | section per-copy handler count in .ufo/waves/round-35/fetch/S209.receipt.txt; receipt sha256 a170c7a50b9305b3448fc85ecddb0d7b1f1c3ff5e42c78cdc2d07718c3bdd27c | Every dated copy of the bar's configuration carries the idle-lock click handler - four of them, the oldest dated 2026-10-03 on this host - so the offer is not a recent addition | mined | 2026-10-24 | on-change | corpus/knowledge/idle-lock-offered-in-the-bar-r15.md |
| S210 | host toggle-state directory - the desktop's own record of its configuration toggles, and whether the idle lock has an entry (measured on this host) - .ufo/waves/round-35/fetch/S210.receipt.txt | own-work | A | Whether the operator's choice about the idle lock could ever have been recorded | sections directory listing and files whose text names the idle lock in .ufo/waves/round-35/fetch/S210.receipt.txt; receipt sha256 ef282e386cdfb686fd331f4ed2fa7f0a33faf3ef4714844639b3eee4790b8726 | The desktop keeps the state of its configuration toggles in this directory and holds entries for other toggles, but the idle lock has none - so the operator's choice leaves no trace in the place where a choice about other toggles would have left one | mined | 2026-10-24 | 90d | corpus/knowledge/idle-lock-offered-in-the-bar-r15.md |

## Recheck cadence per row, and why

- **S203 → `on-request`.** The row's evidence is a historical measurement of a host
  checkout file plus a script inventory; there is no recurring trigger that would
  say "the installer changed" on this lane's clock. Re-open the file when a claim
  needs it. Matches the package's own S315 cadence.
- **S204 → `on-request`.** Same reasoning, and the receipt is a command output
  (`journalctl --user | grep -c omarchy-toggle` → 0): the honest recheck *is* the
  re-run, on demand — no calendar period makes a journal-absence claim fresher.
  Matches package S316.
- **S205 → `90d`.** A live-state measurement (daemon pid, journal start lines,
  timeouts). Process state drifts silently and the entry's "armed" claim is
  time-sensitive, so it needs a periodic re-probe, not an event trigger. Matches
  package S327's `90d` stem (its command prose was dropped with the pipe).
- **S206, S207, S208, S209 → `on-change`.** All four are host files or a fixed set
  of dated copies under `~/.config/waybar/` and `~/.local/share/omarchy/`: a real
  file change is the only meaningful trigger, and omarchy's refresh path (S229 in
  the registry) is exactly what would rewrite them. `on-change` is the package's
  own cadence for S335/S336/S337/S340. For S209 specifically, the evidence is the
  dated-copy set itself — a new `config.jsonc.bak.*` appearing is the change that
  would invalidate "every dated copy carries the handler", which is again a file
  event.
- **S210 → `90d`.** A directory listing under `~/.local/state/omarchy/toggles/hypr/`:
  its contents change only when omarchy writes a toggle record — there is no
  documented signal the lane can hang an `on-change` trigger on, so a periodic
  sweep is the only honest cadence. Matches package S342's `90d` stem.

Cadence summary: `on-request` ×2 (S203, S204), `90d` ×2 (S205, S210),
`on-change` ×4 (S206–S209). Every token matches the counter's
`ISO|NNd|symbolic` rule; all prose command text the package embedded in its
recheck cells was discarded rather than escaped, because the pipe inside it is
unrescuable in a pipe-delimited schema.

## Notes for the append seat

- `used-by` sets are exactly the frozen cites: S203+S204 → `idle-lock-never-asked-r12.md`,
  S205 → `idle-lock-chain-armed-r14.md`, S206–S210 → `idle-lock-offered-in-the-bar-r15.md`.
- Anchor cells carry the receipt sha256 (the admission gate); host-file sha256s are
  included as secondary facts, receipt-first so the gate substring is unambiguous.
- The `located:` lines in each receipt are the gate-quote candidates for the entry
  seats; my `teaches` cells paraphrase those lines without copying them, to keep the
  entry's `gate-quote:` line the only verbatim overlap.
