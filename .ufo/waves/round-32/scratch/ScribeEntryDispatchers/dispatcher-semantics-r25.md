# Dispatchers are descriptions, not actions — and the wiki says their contents are unstable

source: S188 — https://raw.githubusercontent.com/hyprwm/hyprland-wiki/c04680a28301ab4b5ee5f94eaff5395efe28dbac/content/configuring/core/dispatchers.md — `# Dispatchers` — wiki commit `c04680a28301ab4b5ee5f94eaff5395efe28dbac`
verified-at: 2026-10-24 — S188 re-opened in round 32 w1 (seat `ScoutDispatchersWiki`); sha256 prefix `c830ce0717f92776` re-confirmed on the fetched bytes at write time
recheck: 90d — re-pull the file and compare sha256 (expect prefix `c830ce0717f92776`) (ran 2026-10-24)
ground: F1 — "dispatcher behavior" in arc-synthesis §6 U1

### §1 The dispatcher's own contract

**OBS** A dispatcher *describes*; it does not act (S188:9):

> "They do not invoke any action immediately, and their contents are not guaranteed to be stable at all."

**OBS** Calling a dispatcher bare does nothing (S188:15):

> "Simply writing `hl.dsp.whatever()` on its own will do nothing."

**OBS** Execution requires the wrapper (S188:14):

> "To use a dispatcher (any of `hl.dsp.*`) inside a function, you need to wrap it in `hl.dispatch()` for it to be executed."

**INF** The lane's frontier phrase "dispatcher behavior" is two different behaviors and must not be answered with one source: *description* (what a dispatcher returns) and *execution* (when `hl.dispatch()` turns it into an action). Basis: S188:9 and S188:14 read together.

### §2 The dispatchers that touch this lane's surfaces

**OBS** `event( string )` — "Send an event to socket2" (S188:59). This is the
documented bridge from the Lua config into the compositor's event socket
described in `ipc-contract-r25.md`.

**OBS** `force_idle( int )` (S188:69) — the full cell:

> "Sets elapsed time for all idle timers in seconds, ignoring idle inhibitors. Timers return to normal behavior upon the next activity. Do not use with a keybind directly!"

**OBS** `dpms({ monitor?, action? })` carries the same inline caveat (S188:58):
"Do not use with a keybind directly!"

**OBS** The upstream warning against binding these directly (S188:82):

> "It is NOT recommended to set DPMS or force_idle with a keybind directly, as it might cause undefined behavior."

**INF** `force_idle` is a *clock* operation on the idle timers, not a lock or
a suspend operation: it advances elapsed idle time, explicitly overrides idle
inhibitors, and the effect ends at the next activity — the wrong verb for a
lock test and the right verb for an idle-timer test. Basis: the full cell
quoted from S188:69.

### §3 Stability and version caveats

**OBS** The upstream text declares the dispatcher contents unstable
(S188:9). **INF** Any config that pattern-matches on dispatcher contents can
break across releases; a config that only calls the documented wrappers has a
narrower exposure. Basis: the quoted instability statement. The instability is
scoped to the dispatchers' returned contents — the bytes say nothing about the
wiki page itself being unstable.

**UNK** S188 pins a wiki commit, not a Hyprland version: the fetched bytes
carry no 0.56.x marker, so the dispatcher surface as shipped in the host's
v0.56.2 is **not verified** by this entry. The version-matched 0.56.0
dispatchers page was not part of this entry's source set (a sibling seat's
separate fetch this round sits outside S188 and outside this draft). Queued in
`CANNOT-ANSWER.md`.

### §4 Safe observation (read-only)

```sh
curl -fsSL 'https://raw.githubusercontent.com/hyprwm/hyprland-wiki/c04680a28301ab4b5ee5f94eaff5395efe28dbac/content/configuring/core/dispatchers.md' | grep -c 'hl.dispatch'
```

Recheck expectation: `1` or more occurrences. Observed on the re-opened bytes:
`7` (2026-10-24).

## Gate

- URL: https://raw.githubusercontent.com/hyprwm/hyprland-wiki/c04680a28301ab4b5ee5f94eaff5395efe28dbac/content/configuring/core/dispatchers.md
- Access date: 2026-10-24
- Located quote (S188:9, 18 words): "They do not invoke any action immediately, and their contents are not guaranteed to be stable at all."

---
