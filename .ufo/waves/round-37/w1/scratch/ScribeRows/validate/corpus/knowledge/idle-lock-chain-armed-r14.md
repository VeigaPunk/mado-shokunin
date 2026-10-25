# The idle lock is armed on this host - the daemon is running and the chain will fire

Lane: mado-shokunin. Round: 35. Opened 2026-10-24 by this lane. Substrates read-only:
no lock, screensaver, suspend or idle command was run; the probes below are a
process list, a unit query, a journal read and a file read.

source: S205 - .ufo/waves/round-35/fetch/S205.receipt.txt
verified-at: 2026-10-24
recheck: 90d

gate-quote: S205 located: hypridle runs as pid 1667 and started in this session; hypridle.conf sets timeout 150 and 152

### Section 1 The chain is running now

**OBS** `hypridle` is live on this host (S205): the process probe prints pid 1667,
and the user journal holds two `Started hypridle.` lines dated 2026-10-23, the later
at 22:14:11 - a restart, not a first start.

**OBS** The declared chain is a screensaver at 150 seconds and a lock at 152
(S205), and both fire the desktop's own lock command.

### Section 2 Two probes disagree, and the disagreement is the finding

**OBS** `systemctl --user is-active hypridle` answers `inactive` (S205) while the
process probe answers with a live pid.

**INF** The unit probe measures the wrong thing: the daemon runs inside a transient
scope unit rather than as a `hypridle` service, so a reading taken from the unit
name is a probe artefact. The lane's own earlier note, `knowledge/idle-lock-plane.md`
(a dated 2026-10-14 point sample), recorded the daemon's absence; this round's
measurement does not contradict it - it shows the process running on 2026-10-24, and
the difference is a state that has moved, not a false record.

### Section 3 What this does not license

**UNK** No lock, screensaver or suspend transition was triggered or observed. The
chain is armed; whether it fires, and what the operator prefers, stay unknown.

### Errata (round 35, wave 2)

- **E1 - boot ids.** The two `Started hypridle.` lines dated 2026-10-23 do not both
  belong to the current boot: the 13:25:00 line carries `_BOOT_ID=e55f9cd9…` (boot -1),
  the 22:14:11 line `_BOOT_ID=0a3785aa…` (boot 0). Section 1's "a restart, not a first
  start" holds only *across boots*; within the current boot there is exactly one start
  line. The receipt's heading "journal start lines in the current session" is the same
  overstatement. The pid-1667 liveness and the 150/152 chain are unaffected, and wave-2
  seat `RevQuoteS205` confirmed the transient-scope inference first-hand from uwsm's
  `systemd-run --user --scope --unit=app-Hyprland-hypridle-…` log line.
- **E2 - the two lines are two boots' first starts, and only one step locks.** E1 above
  is corrected: neither `Started hypridle.` line is a restart. `13:25:00` belongs to the
  systemd[1529] manager (boot -1) and `22:14:11` to systemd[1493] (boot 0); each is its
  own boot's **first** start, which the receipt already carried - one session has one
  `systemd --user` pid and the receipt prints two. Separately, Section 1's "both fire the
  desktop's own lock command" is **withdrawn**: the 150 s step runs
  `omarchy-launch-screensaver`, whose 59 lines contain no `hyprlock`,
  `omarchy-system-lock` or `swaylock` call (TTE animation only); only the 152 s step runs
  `omarchy-system-lock`. The title's "the chain will fire" is a forecast this entry's own
  Section 3 **UNK** does not license. The transient-scope inference is materially true but
  **unlicensed by S205**: the journal carries it in
  `uwsm_app-daemon … sent: exec systemd-run --user --scope … --unit=app-Hyprland-hypridle-d4bd7533.scope … -- hypridle`,
  which S205 did not quote, and `is-active` prints the same `inactive` for rc=3 (exists,
  stopped) and rc=4 (no such unit) - S205 recorded neither the unit name nor the code.
  Found by wave-2 seats `RevEntryR14` and `RevQuoteS205`.
