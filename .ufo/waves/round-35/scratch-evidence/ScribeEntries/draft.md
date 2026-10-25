# ScribeEntries draft — round 35 wave 1

Three knowledge-entry bodies, drafted in the lane's house style (the
`waybar-module-text-route-r25.md` convention: `source:`/`verified-at:`/`recheck:`
frontmatter, one `gate-quote:` line per cited row, `**OBS**`/`**INF**`/`**UNK**`
paragraphs). Each gate-quote is a verbatim `located:` line of its receipt —
a contiguous substring of the receipt bytes, 1–25 words. Lane registry ids
S203–S210 re-point the merge package's documents by document; the package's own
ids for the same documents (S309, S310, S321, S329, S330, S331, S334, S336) are
named in the provenance lines so the campaign can reconcile them.

Target paths, in order:

- `corpus/knowledge/idle-lock-never-asked-r12.md` — cites S203, S204
- `corpus/knowledge/idle-lock-chain-armed-r14.md` — cites S205
- `corpus/knowledge/idle-lock-offered-in-the-bar-r15.md` — cites S206, S207, S208, S209, S210

---

## Body 1 — corpus/knowledge/idle-lock-never-asked-r12.md

# The idle lock was never offered as a choice at setup, and the operator never toggled it afterwards

Lane: mado-shokunin. Round: 35. Opened 2026-10-24 by this lane. Substrates
read-only: no first-run script was executed, no toggle was run and no journal
entry was written; every host read below is a file read or a read-only query.
Adopted from the merge package's round-12 document (package ids S309, S310),
re-pointed by document to this lane's rows S203, S204.

source: S203 — /home/vgpnk/.local/share/omarchy/bin/omarchy-first-run — `§ script body` — the desktop's post-login questionnaire, as it exists on this host
source: S204 — .ufo/waves/round-35/fetch/S204.receipt.txt — `§ journal count, script list` — the paired negative, measured on this host
verified-at: 2026-10-24
recheck: on-change

gate-quote: S203 located: install/first-run/ lists 12 scripts; the omarchy-first-run body runs all 12; none is idle-lock
gate-quote: S204 located: journalctl --user shows 0 omarchy-toggle invocations; the installer runs 12 first-run scripts

### The setup path asks nothing about the idle lock

**OBS** The desktop's post-login questionnaire is a one-shot script (S203):
when its mode file `~/.local/state/omarchy/first-run.mode` is present it
removes the file and runs the fixed first-run list — battery monitor,
internal-monitor recovery, sudoers cleanup, firewall, DNS resolver, GNOME
theme, swayosd, primary paste, text scaling, elephant, a voxtype post-update
hook, welcome and wifi — then clears the first-run sudoers drop-in. The
receipt's count of `install/first-run/` scripts is 12, the body runs them
all, and none is an idle-lock question.

**OBS** And the operator never exercised the toggle afterwards (S204): the
user journal's count of `omarchy-toggle` invocations is 0 across the sessions
the journal still keeps.

**INF** Two independent negatives converge: the setup path offers no
idle-lock choice, and no `omarchy-toggle` invocation was ever logged. The
machine's state is fully explained by the desktop's default; there is no file
and no journal line in which an operator decision about the idle lock could
be hiding.

### What this does not license

**UNK** Whether the operator would rather the idle lock were off — that is
answerable only by the person who owns the machine. And a scope limit, stated
plainly: this entry licenses a claim about the **setup path** only. It says
nothing about the running interface — the companion entry
`corpus/knowledge/idle-lock-offered-in-the-bar-r15.md` shows the running
desktop does offer the choice — so "never asked at setup" must not be read as
"never offered anywhere".

---

## Body 2 — corpus/knowledge/idle-lock-chain-armed-r14.md

# The idle lock is armed on this host — the daemon is running and the chain is declared to fire

Lane: mado-shokunin. Round: 35. Opened 2026-10-24 by this lane. Substrates
read-only: no lock, screensaver, suspend or idle command was run; the probes
below are a process list, a unit query, a journal read and a file read.
Adopted from the merge package's round-14 document (package id S321),
re-pointed by document to this lane's row S205; amends this lane's
`knowledge/idle-lock-plane.md` point sample of 2026-10-14, which read the
daemon as absent.

source: S205 — .ufo/waves/round-35/fetch/S205.receipt.txt — `§ process probe, unit probe, journal start lines, declared timeouts` — the chain's present state, measured on this host
verified-at: 2026-10-24
recheck: 90d

gate-quote: S205 located: hypridle runs as pid 1667 and started in this session; hypridle.conf sets timeout 150 and 152

### The chain is running now

**OBS** `hypridle` is live on this host (S205): the process probe finds pid
1667, and the user journal holds two `Started hypridle.` lines dated
2026-10-23 — 13:25:00 and 22:14:11 — a start in this session and an earlier
one, a restart rather than a first appearance. No `hyprlock` process exists.

**OBS** The declared chain is a screensaver at `timeout = 150`
(`on-timeout = pidof hyprlock || omarchy-launch-screensaver`) and a lock at
`timeout = 152` (`on-timeout = omarchy-system-lock`), with
`lock_cmd = omarchy-system-lock`, a lock-only `before_sleep_cmd` and
`inhibit_sleep = 3` (S205). The read `hypridle.conf` hashes to
`e7d3b8dd9835…` — the same digest this lane's plane note measured on
2026-10-14.

### Two probes disagree, and the disagreement is the finding

**OBS** `systemctl --user is-active hypridle` answers `inactive` while the
process probe answers with a live pid (S205).

**INF** Both cannot describe the same object; the process probe is the true
one and the unit-name probe is measuring the wrong thing. This lane's
config-plane note records the daemon launched by
`exec-once = uwsm-app -- hypridle` in `default/hypr/autostart.conf` — under
the session's app slice, not as a `hypridle.service` unit — so
`is-active hypridle` answers `inactive` regardless of the process. The
identical config digest across both dates adds weight: the declaration did
not change; the daemon's state did. The plane note's 2026-10-14 reading —
no process, unit inactive — stays true for its window; what moved between
then and now is state, not the record.

### What this does not license

**UNK** No lock, screensaver or suspend transition was triggered or observed:
the chain is *armed*, and whether it fires on true inactivity is unmeasured —
the `timeout = 150/152` figures are config-declared, not watched. The
operator's preference stays unknown, answerable only by the person who owns
the machine. And the armed state is a point sample, not a standing guarantee:
the toggle is a `pgrep`-based process switch that leaves no trace, so whether
hypridle is running at any later moment must be re-probed, not assumed from
this entry.

---

## Body 3 — corpus/knowledge/idle-lock-offered-in-the-bar-r15.md

# The desktop does offer the idle-lock choice — in the bar and in the menu — and it names the state in force

Lane: mado-shokunin. Round: 35. Opened 2026-10-24 by this lane. Substrates
read-only: no bar was started, no indicator was executed, no menu was opened
and no toggle was run; every host read below is a file read or a read-only
listing. Adopted from the merge package's round-15 document (package ids
S329, S330, S331, S334, S336), re-pointed by document to this lane's rows
S206–S210.

source: S206 — /home/vgpnk/.config/waybar/config.jsonc — `§ custom/idle-indicator module block` — the bar's own configuration
source: S207 — /home/vgpnk/.local/share/omarchy/default/waybar/indicators/idle.sh — `§ state test and the tooltip it renders` — the indicator's script
source: S208 — /home/vgpnk/.local/share/omarchy/bin/omarchy-menu — `§ toggle option list and dispatch arm` — the desktop's own menu
source: S209 — .ufo/waves/round-35/fetch/S209.receipt.txt — `§ dated copies and per-copy handler counts` — the dated copies of the bar's configuration
source: S210 — .ufo/waves/round-35/fetch/S210.receipt.txt — `§ directory listing and naming sweep` — the desktop's toggle-state directory
verified-at: 2026-10-24
recheck: on-change

gate-quote: S206 located: waybar config.jsonc line 207 opens the custom/idle-indicator module; line 208 runs omarchy-toggle-idle
gate-quote: S207 located: idle.sh pgreps hypridle and prints the tooltip Idle lock disabled when it is absent
gate-quote: S208 located: omarchy-menu line 207 lists Idle Lock among the toggles; line 212 dispatches omarchy-toggle-idle
gate-quote: S209 located: four dated copies of the bar's configuration each carry the omarchy-toggle-idle handler
gate-quote: S210 located: the toggles/hypr directory holds 2 files and 0 of them name the idle lock

### Two independent surfaces offer the choice

**OBS** The bar carries a dedicated module for it (S206):
`custom/idle-indicator` is listed among the bar's modules and its block opens
at line 207 — `"on-click": "omarchy-toggle-idle"` at line 208, `exec` the
indicator script at line 209, `signal` 9, `return-type` json.

**OBS** The desktop's own menu lists the same toggle (S208): `Idle Lock` is
one of the options in the toggle submenu (line 207), and the case arm
`*Idle*) omarchy-toggle-idle ;;` dispatches it (line 212).

**INF** The operator is asked, in the interface they use every session,
whether the lock should be on. The premise the companion entry amends — that
the desktop never offers the choice — was true of the setup path and an
over-read of it; it is corrected here.

### The desktop names the two states itself

**OBS** The indicator reports which state is in force, not merely a click
target (S207): it `pgrep -x hypridle`s, prints `{"text": ""}` when the daemon
is running and `{"text": "󱫖", "tooltip": "Idle lock disabled", "class":
"active"}` when it is not.

**INF** The desktop's own vocabulary for the question is therefore already
written: a two-state choice displayed continuously, the off state named in
words. The corpus's question to the operator can be put in the interface's
own terms — an icon reading *Idle lock disabled*, toggled from the bar or
from the menu's Idle Lock entry.

**OBS** And the offer is not new (S209): four dated copies of the bar's
configuration each carry the `omarchy-toggle-idle` handler — mtimes
2026-10-03, 2026-10-11, 2026-10-16 and 2026-10-17 on this host, the oldest
the `.1791314470` copy at 2026-10-03 17:44:32.

### Why the choice leaves no trace

**OBS** The desktop keeps configuration-toggle state in
`~/.local/state/omarchy/toggles/hypr`, and it holds entries for other
toggles — `flags.conf` and `window-no-gaps.conf` — but 0 of the 2 files name
the idle lock (S210).

**INF** The toggle is stateless: it flips a process, not a file (this lane's
plane note reads `omarchy-toggle-idle` as a `pgrep`/`pkill`/`uwsm-app`
switch with no flag write). A decision about the other toggles would have
left an entry in that directory; a decision about the idle lock would leave
nothing, so the empty slot is evidence the desktop was built not to
remember — not evidence the operator never considered the choice.

### What this does not license

**UNK** The operator's preference: no source can answer it; the answer is one
sentence from the person who owns the machine. What the rendered module
currently displays is also unverified — the script's bytes were read, no
`RTMIN+9` refresh was sent and no screenshot was taken. And whether the
toggle was ever clicked cannot be settled from these rows: the companion
entry's journal count names `omarchy-toggle` 0 times, but a bar click runs
the command directly and the toggle writes no flag, so a past
toggle-then-restore would leave no trace either way.

### Divergence from the package text

The package's round-15 document dated the oldest dated copy 2026-10-06. This
round's own sweep of the same four copies dates the oldest 2026-10-03
17:44:32 (`.1791314470`), and the per-copy handler count (4 of 4) agrees. The
lane's measured figure is the one recorded here.
