# Event delivery limits — the compositor's per-client queue cap, disconnect-on-overflow, and the bar-side registration site

Lane: mado-shokunin. Round: round-33 w1, seat ScribeEntryStall (re-draft of
`event-delivery-limits-r26`). Substrates READ-ONLY: nothing under `~/.config/`,
`/etc/`, the runtime dir, the compositor or the bar was touched; **no socket was
connected**; no running process or host log was inspected. All evidence is the
two fetched source blobs named below, re-opened and re-checksummed by this seat
on 2026-10-24.

Correction note: the campaign draft of this entry cited campaign-era ids
S187/S188 for `src/managers/EventManager.cpp` and the Waybar IPC backend —
renumbering residue flagged in round-32 review
(`w1/reports/ReviewUsedByClosure.md` M2; `scratch/ScribeLessonDraft/round-32.md`
M32-12). The event-manager row is **S189**; the campaign's backend row (staged
S190) is **not** in this entry's required source set
(`.ufo/waves/round-33/registration.md`: `event-delivery-limits-r26` requires
S197 + S189), so backend claims are bounded out rather than re-attributed (§3).

source: S189 — https://raw.githubusercontent.com/hyprwm/Hyprland/efb50993780079460b0cbed1363e2166a2de1d9f/src/managers/EventManager.cpp — `CEventManager::postEvent` (L163-191), `CEventManager::flushClient` (L133-161), `formatEvent` (L126-133) — commit `efb50993780079460b0cbed1363e2166a2de1d9f` = lightweight tag `v0.56.2` (`git ls-remote` re-run by this seat 2026-10-24: `efb50993780079460b0cbed1363e2166a2de1d9f\trefs/tags/v0.56.2`, no `^{}` peel line)
source: S197 — https://raw.githubusercontent.com/Alexays/Waybar/0.15.0/src/modules/hyprland/workspaces.cpp — `Workspaces::registerIpc` (L803-829), `~Workspaces` (L36-40), constructor initializer (L21) — tag `0.15.0`
verified-at: 2026-10-24
recheck: 90d — re-pull both blobs and re-diff the cap constant and the registration list (re-ran 2026-10-24)
ground: F1 — the event-delivery half of the socket-2 contract behind the lane's compositor ground (arc-synthesis §6 U1), sibling of `ipc-contract-r25`

### §1 Producer-side limits, at the host's release line (S189)

**OBS** Every event is framed as one `>>`-delimited line whose payload is
truncated to 1024 characters and newline-flattened before any client sees it
(S189, `formatEvent`, :128-129).

**OBS** One formatted event string is shared across all connected clients —
`postEvent` builds a single `sharedEvent` and pushes a pointer to it onto each
client's queue (S189:170, :180), so the queue cap is *per client*, not global.

**OBS** A slow reader does not block the compositor: `flushClient` keeps a
per-client `writeOffset`, returns `true` on `EAGAIN`/`EWOULDBLOCK`, and the
event source is armed `WL_EVENT_WRITABLE` only when a client transitions from
empty to non-empty (S189:136-150, :187-188).

**OBS** The delivery limit is a hard cap, enforced before enqueue (S189:169,
:174-176):

> `const size_t MAX_QUEUED_EVENTS = 64;` (S189:169)

> `if (QUEUESIZE >= MAX_QUEUED_EVENTS) {` … `Log::logger->log(Log::ERR, "Socket2 fd {} overflowed event queue, removing", …)` … `it = removeClientByFD(it->fd.get());` (S189:174-176)

**OBS** The same removal is the failure path of a live flush: any write error
other than `EAGAIN`/`EWOULDBLOCK`/`EINTR` returns `false` and the client is
erased (S189:182-184, :149-157); the event-source `WL_EVENT_WRITABLE` handler
removes on flush failure too (S189:105-109).

**INF** Once a client falls 64 events behind, the compositor **disconnects it
entirely — removal, not throttling and not drop-one**. Every subsequent event
is silently absent from that client's stream; the starved consumer receives
nothing until it reconnects and re-registers. The ERR line is the only
compositor-side trace of the drop. Basis: the queue-size check at S189:174
fires on queue length only — nothing shrinks the queue except a successful
write or client teardown.

### §2 Consumer-side registration site, at the bar's release line (S197)

**OBS** Waybar's workspaces module shares one IPC client with the rest of the
module — the constructor initialises `m_ipc(IPC::inst())` (S197:21) and calls
`registerIpc()` during construction (S197:33).

**OBS** `Workspaces::registerIpc` makes **14** `registerForIPC` calls, the only
such calls in the file (S197:803-829): twelve unconditional —
`workspacev2` (:804), `activespecial` (:805), `createworkspacev2` (:806),
`destroyworkspacev2` (:807), `focusedmonv2` (:808), `moveworkspacev2` (:809),
`renameworkspace` (:810), `openwindow` (:811), `closewindow` (:812),
`movewindowv2` (:813), `urgent` (:814), `configreloaded` (:815) — plus two
conditional: `windowtitlev2` (:821) when the title-rewrite or taskbar-with-title
path is configured, and `activewindowv2` (:827) when active-window tracking is
enabled. The teardown counterpart is `m_ipc.unregisterForIPC(this)` in the
destructor, followed by a mutex wait for an in-flight handler (S197:36-40).

**INF** Event flow to the bar is push-only: the module *asks* for events and
the compositor pushes them (§1). A bar that stalls its IPC reader accumulates
a 64-event window and is then disconnected — from the compositor's view the
client is just gone, and from the module's view the event stream simply stops.
Basis: §1's removal semantics plus the shared `IPC::inst()` handle at S197:21
— this entry does not establish whether one drop would starve *only* the
workspaces module or every module on the shared handle; that depends on the
backend the module shares, which §3 bounds out.

### §3 What this entry does not license

**UNK** Whether this host's compositor **ever hit the cap** is unobserved: no
socket was connected, no compositor/bar log was read, no running process was
inspected, and nothing was grep'd for the "overflowed event queue" ERR line.
The 64-event overflow-removal is a source-verified *mechanism*, not an
occurrence witnessed on the host — the earlier claim of a host-side stall
remains an open question for the `event-queue-host-measurement` track, not a
finding here.

**UNK** Whether a removed client is silently readmitted is out of this entry's
scope: reconnect logic lives in Waybar's IPC *backend* (the campaign's staged
S190 row), which is deliberately absent from this re-draft's source list — its
claims are deferred to whichever entry re-grounds S190 rather than re-attributed
here.

**UNK** The installed bar version was not interrogated this round; S197 pins
the `0.15.0` tag the lane carries for the host's Waybar, but the running binary
was not checked.

### §4 Safe observation (read-only, repeatable)

```sh
# the cap + overflow-removal path, on the host's release line
curl -fsSL 'https://raw.githubusercontent.com/hyprwm/Hyprland/efb50993780079460b0cbed1363e2166a2de1d9f/src/managers/EventManager.cpp' | grep -c 'MAX_QUEUED_EVENTS'
# the registration surface, at the pinned bar tag
curl -fsSL 'https://raw.githubusercontent.com/Alexays/Waybar/0.15.0/src/modules/hyprland/workspaces.cpp' | grep -c 'm_ipc\.registerForIPC'
```

Recheck expectation: `2` and `14` respectively, as of 2026-10-24 (both re-ran
today against the fetched blobs: `2` and `14`).

## Gate

gate-quote: S197 m_ipc.registerForIPC("workspacev2", this);
gate-quote: S189 const size_t MAX_QUEUED_EVENTS = 64;

| Source | URL | Accessed | sha256 (fetched bytes) | Located quote (≤25 words) |
| --- | --- | --- | --- | --- |
| S189 | https://raw.githubusercontent.com/hyprwm/Hyprland/efb50993780079460b0cbed1363e2166a2de1d9f/src/managers/EventManager.cpp | 2026-10-24 | `eea605dfe5ce09e1f92a67ec478bf61a19894c6e0ee3302c0393521a2ee9540d` | `const size_t MAX_QUEUED_EVENTS = 64;` — L169 |
| S197 | https://raw.githubusercontent.com/Alexays/Waybar/0.15.0/src/modules/hyprland/workspaces.cpp | 2026-10-24 | `1e19d92638e7923f0e72f6e65c83f579e32b41d588d166d6efef543c3f97d7e9` | `m_ipc.registerForIPC("workspacev2", this);` — L804 |

sha256 values were re-run by this seat at write time (`sha256sum` on the wave
fetch blobs, 2026-10-24): both equal the `PRED-C1-r33-v1` frozen digests
(`.ufo/waves/round-33/c1/frozen.json`), and S197's digest equals the ScoutS197
seat's fresh-fetch digest (`w1/reports/ScoutS197.md`). Both `gate-quote` lines
are contiguous substrings of the fetched blobs — S189:169 and S197:804,
re-grepped by this seat; quoted text is 6 and 3 words respectively, inside the
1-25-word predicate bound.

---
