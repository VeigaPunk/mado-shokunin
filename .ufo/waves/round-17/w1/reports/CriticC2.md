# CriticC2 — round 17, claim C2 (rubric V, P4/P6 documentary routes)

Seat: MadoR17.CriticC2 (critic, advisory; no judgment, no edits beyond this file).
Read first: `corpus/lessons/round-16-verifier-spotcheck.md` (done).
Inputs read: SCORECARD.md:821-865 (pre-registration `0175f13`), PROVINCE.md,
heads (l.1-15) of all 30 `corpus/knowledge/*.md`, SOURCES.md registry `used-by`
column, QUALITY.md:107 (QUALITY22), `.ufo/waves/round-17/w1/dispatch.json`
(NoteIdle / NoteTerminal / MeasureBuild items), `/var/log/pacman.log`
(file bytes, allowed read), `~/.config/hypr/hyp{ridle,lock}.conf`,
`~/.config/xdg-terminals.list`, `~/.config/alacritty/` listing (bytes/sha256 only).
Network: `curl -w %{http_code}` on 4 tag-pinned raw URLs and `git ls-remote --tags`
on 4 upstream repos (read-only). No package query, sudo, service, compositor
or live probe; no jj; no git mutation. No tools installed or updated.

## Bottom line

Rubric V is a **fair, bounded post-ceiling rubric in shape** (its denominator is
the lane's own pre-existing PROVINCE "Owns" list, declared before any wave,
legacy map frozen), but it is **not a coverage measure in the plain sense**: it
counts *tier-A external-source anchoring per owned surface*. Its 2/6 baseline is
low largely **by header format**, not by absence of knowledge — P3, P4, P5 and
P6 each already have long, admitted, *measured* notes. A P4/P6 documentary
route note does count under V's own definition, but only as "upstream contract
at a version pin", never as host behaviour; and the host version is better
evidenced than `[UNK]` suggests. Five fixable defects below; two wordings the
judge must reject if they appear.

## Counterexample 1 — the baseline is "not sourced", not "not covered"

Evidence (heads + line counts, read this session):

| Surface | Existing admitted notes (no `source:` head, no SOURCES row) | Lines |
|---|---|---|
| P3 Walker | `walker-deep.md`, `walker-live-surface.md`, `walker-deep-r9.md`, `waybar-walker-semantics.md` | 617 / 300 / 398 / … |
| P4 terminals | `terminals-and-omarchy.md` (MADO-3) | 204 |
| P5 themes/wallpapers | `theme-wallpaper-plane.md` (r7), `remaining-planes-census.md` (r6) | 394 / 333 |
| P6 idle/lock | `idle-lock-plane.md` (MADO-R4-2), `waybar-walker-plane.md` §hypridle/hyprlock | 381 / 474 |

`awk -F'|'` over SOURCES.md: no registry row has any of these files in
`used-by`; none carries `source:`/`surface:` in its first 15 lines. V therefore
scores them 0 by construction.

The C2 host anchors are already admitted facts:
`terminals-and-omarchy.md:94` — "`~/.config/xdg-terminals.list` (127 B,
2026-10-03) lists `Alacritty.desktop` as first choice"; `:95` —
`bindings.conf:2` → `uwsm-app -- xdg-terminal-exec`; `:31` alacritty
`general.import`. `idle-lock-plane.md:62-63` records hypridle/hyprlock.conf
sha256 `e7d3b8dd9835…` / `b8d173dcff55…`; today's `sha256sum` gives the same
full digests (`e7d3b8dd…7de41`, `b8d173dc…68fc1`) — the host side is unchanged
since round 4, so the new notes add **upstream-contract provenance**, not new
host ground.

Impact: coverage (label), calibration (false provenance risk), expansion trend.
A report/lesson/trend line saying "new ground", "previously uncovered surface"
or "coverage of P4/P6 from 0" would be false provenance.

## Counterexample 2 — V can be satisfied by bookkeeping (own-work rows)

V requires only: `source:` S-id in head, row `mined` + tier `A` + `used-by`
names the entry, `surface: P<n>`, plus (per MeasureBuild item) four exact
headings with `[UNK]` in the last. It does **not** constrain `kind`. Precedent:
S055 is `kind own-work | tier A | mined` (SOURCES.md:67). So a short new entry
`theme-route.md` with the four headings, `surface: P5`, and a new own-work
tier-A row pointing at `theme-wallpaper-plane.md` scores P5 covered without a
single external source opened. The same works for P3. V would then saturate at
6/6 with zero new knowledge — premature saturation.

Smallest correction: in measure.py and the rubric text, count a surface only
when at least one cited row has `kind ∈ {docs, spec, code}` (external, not
`own-work`, not a host-file row); report own-work-only entries under a separate
`rejected: own-work-only` reason. Show it able to fail on that synthetic case
(fixture or `/tmp` git repo), keeping the 27cd06f baseline at 2/6.

## Counterexample 3 — `surface: P<n>` is a self-declared label

Nothing ties the label to the surface. A note tagged `surface: P4` that only
documents xdg-terminal-exec (a launcher selector, not a terminal-emulator
config) would count as "terminal-emulator configs" covered. NoteTerminal's
item does include `~/.config/alacritty/` and `alacritty.5.scd`, so the current
draft is probably fine — but the instrument cannot tell.

Smallest correction: measure.py requires `## Host declaration` to contain a
path from the PROVINCE path set for that surface (P1 `~/.config/hypr/`,
P2 `~/.config/waybar/`, P3 `~/.config/walker/`,
P4 `~/.config/(alacritty|foot|kitty|ghostty)/`, P5 theme/wallpaper declared
files, P6 `~/.config/hypr/hyp(ridle|lock).conf`). Also disclose that P4 is
binary: one Alacritty note "covers" a surface of four config trees
(alacritty, foot, ghostty, kitty all exist — `ls -d` today).

## Counterexample 4 — the instrument is not frozen at pre-registration

`git ls-tree -r --name-only 0175f13 -- .ufo/waves/round-17` lists only
`evidence/census-start.txt`; `.ufo/waves/round-17/measure.py` does not exist at
the pre-registration commit (and not on disk at review time). SCORECARD:850
names `python3 .ufo/waves/round-17/measure.py REV` as the C2 command, and
MeasureBuild writes it concurrently with NoteIdle/NoteTerminal. The rubric
prose is pre-registered; the counter that decides edge cases (head window,
row parse, heading check) is authored in the same wave as the content it
scores — tunable to outcome.

Smallest correction (round-16 practice): commit measure.py and record its blob
SHA-256 plus its `27cd06f` output (expect c2 2/6, P1+P2) **before** either
note is integrated; bind that digest in the C2 receipt; any later edit to
measure.py re-runs both baseline and final and is disclosed as a correction.

## Counterexample 5 — QUALITY22 vs. V's activation order

QUALITY22 (QUALITY.md:107): re-derive every *active* axis before selecting the
lowest. If V were active at baseline, coverage = 2/6 = 3.3333 < calibration
6.3636, and C1's "lowest axis" premise (SCORECARD:830) would be false. The
pre-registration keeps U 7/7 as the coverage row, so the reading is
consistent only if V becomes active *after* this round's selection.

Smallest correction: one explicit sentence (SCORECARD results / lesson):
"V was declared at 0175f13 after the axis re-derivation and was not part of
round-17 lowest-axis selection; from round 18 QUALITY22 includes V." Note for
round 18: if both targets land, calibration 15/23 = 6.5217 < V 4/6 = 6.6667,
so calibration stays lowest — state it, don't let it be discovered.

## Question 2 — is a documentary route "coverage" when host versions are `[UNK]`?

Yes, **under V's own definition** (sourced route per owned surface), and only
as: "upstream at tag T documents config semantics S; the host declares bytes B
(hash H, read today)". It never covers delivery, timers firing, lock
rendering, or which binary is running. But the version is less unknown than
`[UNK]` implies — `/var/log/pacman.log` is a permitted file read and is not a
package query:

| Package | Last pacman.log line | Upstream latest tag (`git ls-remote`, 2026-10-20) | Raw tag URL |
|---|---|---|---|
| hypridle | l.1792 `upgraded hypridle (0.1.7-10 -> 0.1.8-2)` 2026-10-11 | v0.1.8 | `…/hyprwm/hypridle/v0.1.8/README.md` → 200 |
| hyprlock | l.1798 `upgraded hyprlock (0.9.6-1 -> 0.9.6-3)` 2026-10-11 | v0.9.6 | `…/hyprwm/hyprlock/v0.9.6/README.md` → 200 |
| alacritty | l.639 `installed alacritty (0.17.0-1)`, no later line | v0.17.0 | `…/alacritty/v0.17.0/extra/man/alacritty.5.scd` → 200 |
| xdg-terminal-exec | l.2935 `upgraded xdg-terminal-exec (0.14.3-1 -> 0.14.3-2)` 2026-10-20T09:16 | v0.14.3 | `…/xdg-terminal-exec/v0.14.3/README.md` → 200 |

Historical corpus agrees: `waybar-walker-plane.md:38-39` (2026-10-14)
`hypridle v0.1.8`, `Hyprlock version v0.9.6`.

Defect: NoteIdle/NoteTerminal are told to pin "the latest release tag". Today
latest == logged pkgver, by coincidence; "latest" is not a host-linked
criterion and drifts on the next upstream release. Smallest correction: pin by
the pacman.log pkgver (cite the line numbers above as a documentary host
anchor), keep `[UNK]` only for what is truly unknown — running-process
identity/start time vs. the 2026-10-11 upgrade, Arch packaging patches
(`-2`/`-3` pkgrel), and runtime behaviour. Writing "host version [UNK]" while
the log records the pkgver is under-claiming that a later reader may
"correct" with a forbidden package query.

## Adjacent fact for L1 (freshness / host-pause bookkeeping, not C2-blocking)

pacman.log shows host transactions on 2026-10-20 before pre-registration
(10:56 commit time): 07:45, 07:50, 08:14 (`-Rns electron39 mbedtls`), 09:15
`pacman -Syu --needed … linux-lts …` (upgraded `hyprland 0.56.2-2 -> 0.56.2-4`,
`walker 2.17.0-1 -> 2.17.2-1`, `xdg-terminal-exec 0.14.3-1 -> 0.14.3-2`),
09:27 fwupd, 09:29-09:31 yay go/elephant `-U`, 09:38/09:39 `-Rns`. Last line is
09:39:21; none after at review time (11:01). Not attributable to this lane or
round (operator/other actor; outside the round window) — but: (a) the P3 walker
notes describe 2.17.0, now superseded on host → freshness harm-watch should
not cite them as current; (b) round-17 closure should repeat the R16-style
"0 pacman.log lines in the round window" check from 10:56 onward.

## Classification

| # | Defect | Fixable? | Axes |
|---|---|---|---|
| 1 | Baseline 2/6 reflects missing sourcing, not missing knowledge | fixable by labelling: name V "tier-A sourced route per owned surface"; notes cross-link the measured notes and record the unchanged hashes | coverage, calibration, expansion trend |
| 2 | own-work rows satisfy V | fixable: `kind` filter + failing control | coverage (saturation) |
| 3 | self-declared `surface:` | fixable: per-surface path anchor in `## Host declaration`; disclose binary P4 | coverage |
| 4 | measure.py authored concurrently, absent at 0175f13 | fixable: commit + bind digest + baseline receipt before notes land | coverage, calibration |
| 5 | V activation vs. QUALITY22 | fixable: one sentence; round-18 forecast | calibration, selection |
| 6 | "latest tag" pin; `[UNK]` over-applied to version | fixable: pin by pacman.log pkgver, narrow `[UNK]` | coverage, calibration |

**The judge must reject** (no wording fix rescues them): any C2 statement
that P4/P6 were *uncovered ground* or that the notes establish *host
behaviour* (idle timers, lock rendering, terminal selection at runtime); and
a C2 count produced by a measure.py whose blob digest is not bound to the
receipt. With 1-6 corrected, C2 2/6 → 4/6 is a legitimate, honestly bounded
gain on a declared rubric — a sourcing improvement on known surfaces, not new
coverage.
