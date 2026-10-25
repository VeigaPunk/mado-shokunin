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
