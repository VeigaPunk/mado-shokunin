# The desktop does offer the idle-lock choice - in the bar and in the menu

Lane: mado-shokunin. Round: 35. Opened 2026-10-24 by this lane. Substrates read-only:
no bar was started, no indicator was executed, no menu was opened and no toggle was
run; every host read below is a file read.

source: [ref] - /home/vgpnk/.config/waybar/config.jsonc
source: [ref] - /home/vgpnk/.local/share/omarchy/default/waybar/indicators/idle.sh
source: [ref] - /home/vgpnk/.local/share/omarchy/bin/omarchy-menu
source: [ref] - .ufo/waves/round-35/fetch/[ref].receipt.txt
source: [ref] - .ufo/waves/round-35/fetch/[ref].receipt.txt
verified-at: 2026-10-24
recheck: on-change

gate-quote: [ref] located: waybar config.jsonc line 207 opens the custom/idle-indicator module; line 208 runs omarchy-toggle-idle
gate-quote: [ref] located: idle.sh pgreps hypridle and prints the tooltip Idle lock disabled when it is absent
gate-quote: [ref] located: omarchy-menu line 207 lists Idle Lock among the toggles; line 212 dispatches omarchy-toggle-idle
gate-quote: [ref] located: four dated copies of the bar's configuration each carry the omarchy-toggle-idle handler
gate-quote: [ref] located: the toggles/hypr directory holds 2 files and 0 of them name the idle lock

### Section 1 Two independent surfaces offer the choice

**OBS** The bar carries a dedicated module for it, and clicking that module runs the
toggle ([ref]): `custom/idle-indicator` opens at line 207 of the bar's configuration
and its `on-click` is `omarchy-toggle-idle` at line 208.

**OBS** The desktop's own menu lists the same toggle and dispatches it to the same
command ([ref]): `Idle Lock` appears among the menu's toggle options at line 207, and
the case arm `*Idle*) omarchy-toggle-idle ;;` is at line 212.

**INF** The operator is asked, in the interface they use every session, whether the
lock should be on. The premise that the desktop never offers the choice was drawn
from the setup path alone; it is corrected here.

### Section 2 The desktop names the two states itself

**OBS** The indicator does more than toggle ([ref]): it asks whether `hypridle` is
running, renders nothing when it is, and renders an icon whose tooltip reads
`Idle lock disabled` when it is not.

**OBS** And the offer is not new ([ref]): four dated copies of the bar's configuration
each carry the `omarchy-toggle-idle` handler, the oldest dated 2026-10-03 on this
host.

### Section 3 Why the choice leaves no trace

**OBS** The desktop keeps the state of its configuration toggles in one directory,
and it holds entries for other toggles - but not for the idle lock ([ref]): the
directory holds 2 files and 0 of them name the idle lock.

**INF** So the absence of an entry is not evidence that the operator never
considered the choice. It is evidence that the desktop was built not to remember.

### Section 4 What this closes and what it does not

**OBS** The premise is corrected: the desktop offers the choice in two surfaces,
since at least 2026-10-03 on this host, and shows which state is in force.

**UNK** The operator's preference. No source can answer it, and this round does not
pretend otherwise.

### Section 5 Divergence from the package text

The package's round-15 text dated the oldest dated copy 2026-10-06. This round's own
sweep of the same four copies dates the oldest 2026-10-03, and the count of copies
carrying the handler (4) agrees. The lane's measured figure is the one recorded here.

### Errata (round 35, wave 2)

- **E1 - dating clock.** [ref]'s per-copy table dates the oldest copy `2026-10-03` by
  content mtime; that copy's btime/ctime is `2026-10-06 16:21:10`, equal to its epoch
  suffix (`date -d @1791314470`). Section 5 is right that the package's round-15 text
  used 2026-10-06; the cause is that the dated copy preserved the source file's older
  mtime, so the creation clock and the content clock disagree. The served claim ("the
  offer is not a recent addition") holds on either clock. Found by wave-2 seat
  `RevQuoteS209` (`.ufo/waves/round-35/w2/reports/RevQuoteS209.md`).

- **E2 - "never taken it" withdrawn.** Section 4's closing inference and this entry's
  title overstate the evidence: the journal shows the idle daemon's scope `Consumed` at
  `2026-10-23T19:24:38-03:00` with no `Stopping`/`Stopped` pair and a new start at
  `22:14:11`, which is what `omarchy-toggle-idle` produces when it stops hypridle. So a
  toggle-off happened in the retained window; who performed it and by which surface is
  unverified. What survives: the choice leaves no state in the toggles directory, and
  the bar and the menu both offer it. See
  `.ufo/waves/round-35/w2/reports/RevQuoteS204.md`.

- **E3 - "built not to remember" withdrawn.** `omarchy-toggle-idle` stops or starts the
  `hypridle` process and writes no file, and
  `default/hypr/autostart.conf:1` carries `exec-once = uwsm-app -- hypridle`, which re-arms
  the daemon at every login. The toggles directory's `flags.conf` is byte-identical to the
  omarchy template placeholder whose own text reads "This directory is intended for
  permanent config toggle flags. Do not remove this file" - so an absent idle entry is the
  toggle's process-shaped design, not a desktop that refuses to remember. Section 3's
  causal reading is replaced by that mechanism; the measurement (2 files, 0 naming idle)
  is unchanged.
- **E4 - one state is named, the other is silence.** Section 2's heading overstates [ref]:
  the indicator prints `{"text": ""}` while `hypridle` runs, and an icon whose tooltip
  reads `Idle lock disabled` when it does not. Exactly one state carries words.

- **E5 - scope of the "leaves no trace" heading.** It holds for on-disk state. The toggle
  also calls `notify-send`, so a notification may survive in the session's notification
  history; no such history was read.
