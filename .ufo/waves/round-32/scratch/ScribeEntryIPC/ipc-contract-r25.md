# Hyprland IPC contract — the two sockets, the request grammar, and the compositor's own event framing

Lane: mado-shokunin. Round: round-32 w1, seat ScribeEntryIPC (re-ground of
`ipc-contract-r25`). Substrates READ-ONLY: nothing under `~/.config/`, `/etc/`,
the runtime dir or the repo was written by this seat; **no socket was
connected**; no compositor state was touched; no producer was executed. All
evidence is document and source bytes read over HTTP, re-opened 2026-10-24.
Sibling-seat re-opens (`ScoutIPCWikiCurrent`, `ScoutIPCWiki0560`,
`ScoutIPCEventMgr`, same wave) were read; every pin below was re-verified by
this seat against the fetched bytes.

source: S186 — https://raw.githubusercontent.com/hyprwm/hyprland-wiki/c04680a28301ab4b5ee5f94eaff5395efe28dbac/content/ipc/_index.md — `# Hyprland IPC` (sockets L14/L25, `## Events list` L34, catalogue rows L38-81) — commit `c04680a28301ab4b5ee5f94eaff5395efe28dbac`
source: S187 — https://wiki.hypr.land/0.56.0/IPC/ — `## Events list` table (tbody rows L2866-3097) — page stamp `datetime="2026-05-02T03:38:58.000Z"` ("Last updated on May 2, 2026")
source: S189 — https://raw.githubusercontent.com/hyprwm/Hyprland/efb50993780079460b0cbed1363e2166a2de1d9f/src/managers/EventManager.cpp — `CEventManager::formatEvent` (L126-133) — commit `efb50993780079460b0cbed1363e2166a2de1d9f` = lightweight tag `v0.56.2` (`git ls-remote`, 2026-10-24)
verified-at: 2026-10-24
recheck: 90d — re-pull the three sources and re-diff the 0.56.0 event table against the pinned upstream catalogue (ran 2026-10-24)
ground: F1 — "dispatcher behavior" and the socket protocol behind the lane's compositor ground (arc-synthesis §6 U1)

### §1 The request socket (documented)

**OBS** The request socket is `$XDG_RUNTIME_DIR/hypr/[HIS]/.socket.sock`
(S186:14).

**OBS** The request grammar is a flag-prefixed command line (S186:19):

> "Basically, write `[flags]/command args`."

**OBS** The evaluation model is synchronous, and the failure mode of holding a
connection open is a compositor freeze until the five-second timeout (S186:22):

> "Hyprland evaluates connections to this socket completely synchronously, which means that any unclosed connections *will cause Hyprland to freeze* until the five-second timeout is reached."

**INF** Any tool that opens the request socket, writes and closes per request
is safe; a tool that keeps the connection open converts every later request
into a queued no-op until the timeout. Basis: the documented synchronous
evaluation plus the explicit five-second timeout in the same sentence
(S186:22).

### §2 The event socket (documented)

**OBS** The event socket is `$XDG_RUNTIME_DIR/hypr/[HIS]/.socket2.sock`
(S186:25).

**OBS** Each event is one framed line (S186:30):

> "`EVENT>>DATA\n` (`\n` is a linebreak)"

**OBS** The smallest example published is a workspace event (S186:32):
`E.g.: `workspace>>2``.

### §3 What the compositor implements at the host's own version

**OBS** At v0.56.2 the event socket is created by the event manager, not by a
directory named `ipc` — the v0.56.2 source tree contains **no** `src/ipc/`
path (tree check re-run 2026-10-24: GitHub contents API on `src/ipc` at the
pinned commit → HTTP 404), so any source citation that places the socket in
`src/ipc/s1/` or `src/ipc/s2/` describes a *later* restructure and must not be
used to explain this host (S189, tree check on commit `efb50993…`).

**OBS** The pinned commit is the `v0.56.2` tag itself (lightweight tag,
`git ls-remote` 2026-10-24), so "at v0.56.2" below means these exact bytes
(S189).

**OBS** The socket path is derived from the compositor's instance path
(S189:21):

> `const auto  PATH          = g_pCompositor->m_instancePath + "/.socket2.sock";`

**OBS** It is a non-blocking AF_UNIX stream with a backlog of ten
(S189:14, :34, :35):

> `CEventManager::CEventManager() : m_socketFD(socket(AF_UNIX, SOCK_STREAM | SOCK_CLOEXEC | SOCK_NONBLOCK, 0)) {` (S189:14)

> `// 10 max queued.` (S189:34)

> `if (listen(m_socketFD.get(), 10) < 0) {` (S189:35)

**OBS** The framing rule, including the truncation and the newline
sanitisation, is in one function, `formatEvent` (S189:126-129):

> `auto             eventString = std::format("{}>>{}\n", event.event, data.substr(0, 1024));` (S189:128)

> `std::replace(eventString.begin() + event.event.length() + 2, eventString.end() - 1, '\n', ' ');` (S189:129)

**INF** The data payload is truncated to 1024 characters and any newline inside
the payload is flattened to a space, so a consumer must parse one `>>`-delimited
line per event and must not assume a multi-line payload survives. Basis: the
two lines above, read together with the `EVENT>>DATA\n` framing (S186:30).

### §4 Version-drift check (a negative result worth keeping)

**OBS** The event catalogue published for **0.56.0** (S187, tbody rows) and the
catalogue in the current upstream wiki (S186, rows L38-81) are **identical**:
44 event names on both sides, none added and none removed. Re-extraction on
2026-10-24 set-diffed the two catalogues: empty in both directions.

**INF** A host on 0.56.x and a host on current upstream observe the same event
*names*; only the payload shapes may differ. Basis: the catalogue diff above.

### §5 What this entry does not license

**UNK** Nothing here was observed on this host: no socket was connected, no
event was seen, and the installed compositor binary was not interrogated. The
entry bounds the *contract*, not the host's behavior.

**UNK** The request-socket *implementation* side (how `[flags]/command args` is
parsed and what the flags mean) lives in the already-held `src/debug/HyprCtl.cpp`
(S018/S158); this entry did not re-read it. Reading it is queued, not done.

### §6 Safe observation (read-only, repeatable)

```sh
# the documented framing, from the pinned source
curl -fsSL 'https://raw.githubusercontent.com/hyprwm/hyprland-wiki/c04680a28301ab4b5ee5f94eaff5395efe28dbac/content/ipc/_index.md' | grep -c 'EVENT>>DATA'
# the implementation's framing and truncation, from the host's tag
curl -fsSL 'https://raw.githubusercontent.com/hyprwm/Hyprland/efb50993780079460b0cbed1363e2166a2de1d9f/src/managers/EventManager.cpp' | grep -c 'substr(0, 1024)'
```

Recheck expectation: `1` and `1` respectively, as of 2026-10-24 (both re-ran
today against the fetched bytes: `1` and `1`).

## Gate

| Source | URL | Accessed | sha256 (fetched bytes) | Located quote (≤25 words) |
| --- | --- | --- | --- | --- |
| S186 | https://raw.githubusercontent.com/hyprwm/hyprland-wiki/c04680a28301ab4b5ee5f94eaff5395efe28dbac/content/ipc/_index.md | 2026-10-24 | `535bc4c385a06162d3e7e356e1a13853f9c47598787f15c80883c2895d06d1a4` | "`EVENT>>DATA\n` (`\n` is a linebreak)" — L30 |
| S187 | https://wiki.hypr.land/0.56.0/IPC/ | 2026-10-24 | `136e5511fba5524a5cb1685668429ee28f7a2710c70104441eeb2b674f6a37a4` | `datetime="2026-05-02T03:38:58.000Z"` ("Last updated on May 2, 2026") |
| S189 | https://raw.githubusercontent.com/hyprwm/Hyprland/efb50993780079460b0cbed1363e2166a2de1d9f/src/managers/EventManager.cpp | 2026-10-24 | `eea605dfe5ce09e1f92a67ec478bf61a19894c6e0ee3302c0393521a2ee9540d` | "auto             eventString = std::format("{}>>{}\n", event.event, data.substr(0, 1024));" — L128 |

sha256 prefixes cross-checked against the wave's scout seats
(`ScoutIPCWikiCurrent` 535bc4c3…, `ScoutIPCWiki0560` 136e5511…,
`ScoutIPCEventMgr` eea605df…): identical.

---
