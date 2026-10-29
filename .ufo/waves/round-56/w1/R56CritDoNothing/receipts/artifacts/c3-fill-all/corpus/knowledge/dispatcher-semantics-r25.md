# Dispatchers are descriptions, not actions — and the wiki says their contents are unstable

Lane: mado-shokunin. Round: 32 (assimilation round, theme: the Hyprland IPC
two-socket contract — the dispatcher surface is the request-side half of it).
Substrates READ-ONLY: nothing under `~/.config/`, `/etc/`, the runtime dir or any
domain source tree was written; **no socket was connected**; no compositor state
was touched. All evidence is source bytes read over HTTP on 2026-10-24 by the lane
itself.

source: S188 — https://raw.githubusercontent.com/hyprwm/hyprland-wiki/c04680a28301ab4b5ee5f94eaff5395efe28dbac/content/configuring/core/dispatchers.md — `# Dispatchers` — wiki commit `c04680a28301ab4b5ee5f94eaff5395efe28dbac`
verified-at: 2026-10-24
recheck: 90d

## Gate

Re-opened by the lane on **2026-10-24** (fetched bytes kept at
`.ufo/waves/round-32/fetch/S188.bin`).

- **S188** — https://raw.githubusercontent.com/hyprwm/hyprland-wiki/c04680a28301ab4b5ee5f94eaff5395efe28dbac/content/configuring/core/dispatchers.md — opened 2026-10-24; 12,879 B, sha256 `c830ce0717f92776f03a977506141c549705aebe4e738ce801faddaa7b2d7d14`.
  Quote (`:8-9`): "Dispatchers return tables that describe an action you want to make." / "They do not invoke any action immediately, and their contents are not guaranteed to be stable at all."
  Quote (`:14`): "To use a dispatcher (any of `hl.dsp.*`) inside a function, you need to wrap it in `hl.dispatch()` for it to be executed."
  Quote (`:59`): "| `event( string )` | Send an event to socket2 |".

**GRANTED** — every claim below is carried by a quote located in these bytes on
2026-10-24; the staged package's line anchors were re-derived and the anchors
named here are canonical for this entry.

### §1 A dispatcher describes; `hl.dispatch` executes

**OBS** A dispatcher is a table that describes an action; constructing it does not
invoke anything (S188:8-9). A dispatcher only runs when it is wrapped in
`hl.dispatch()` (S188:14).

> "Dispatchers return tables that describe an action you want to make." (S188:8)
> "They do not invoke any action immediately, and their contents are not guaranteed to be stable at all." (S188:9)

**INF** Reading a config that builds a dispatcher without calling it tells you
what the config *describes*, not what the host *does*. A lane reading a
dispatcher table must label the row as described-not-invoked unless it also
observed the dispatch. Basis: S188:8-9 and the wrapped-call rule at S188:14.

### §2 The dispatchers that touch the compositor's own surfaces

**OBS** `event( string )` sends an event to socket2 — the same event socket the
IPC contract entry documents (S188:59). `dpms({ monitor?, action? })` toggles
monitors (S188:58). `force_idle( int )` sets elapsed time for all idle timers in
seconds, ignoring idle inhibitors (S188:69).

> "| `force_idle( int )` | Sets elapsed time for all idle timers in seconds, ignoring idle inhibitors. Timers return to normal behavior upon the next activity. Do not use with a keybind directly! |" (S188:69)

**OBS** The wiki explicitly warns against setting DPMS or `force_idle` with a
keybind directly, as it might cause undefined behavior (S188:82).

**INF** A dispatcher row about idle or DPMS is a *description of a timer
contract*, not a statement about this host's idle chain; the lane's own idle
surfaces stay `[UNK]` until measured. Basis: S188:69 and S188:82 read as
documentation.

### §3 Stability and scope

**OBS** The wiki states that dispatcher contents "are not guaranteed to be stable
at all" (S188:9). The wiki itself keeps layout-specific dispatchers on the
layout pages (S188:12), so any dispatcher inventory is incomplete by
construction.

**INF** A dispatcher inventory built from the wiki is a snapshot of a moving
document, not a stable API. Re-check on release, and never let such an
inventory be the sole support for a claim about the host.

### §4 What this entry does not claim

- No dispatcher was dispatched; no keybind was fired; nothing was executed on the
  host. Every row is documentation.
- The list of dispatchers is not the complete vocabulary (S188:12).
- The idle/lock chain on this host is not measured here.
