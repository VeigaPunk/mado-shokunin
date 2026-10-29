# Hyprland IPC contract — the two sockets, the request grammar, and the compositor's own event framing

Lane: mado-shokunin. Round: 32 (assimilation round, theme: the Hyprland IPC
two-socket contract). Substrates READ-ONLY: nothing under `~/.config/`, `/etc/`,
the runtime dir or any domain source tree was written; **no socket was
connected**; no compositor state was touched. All evidence is document and source
bytes read over HTTP on 2026-10-24 by the lane itself.

source: S186 — https://raw.githubusercontent.com/hyprwm/hyprland-wiki/c04680a28301ab4b5ee5f94eaff5395efe28dbac/content/ipc/_index.md — `# Hyprland IPC` — wiki commit `c04680a28301ab4b5ee5f94eaff5395efe28dbac`
source: S187 — https://wiki.hypr.land/0.56.0/IPC/ — `# Hyprland IPC` — page revision "Last updated on May 2, 2026"
source: S189 — https://raw.githubusercontent.com/hyprwm/Hyprland/efb50993780079460b0cbed1363e2166a2de1d9f/src/managers/EventManager.cpp — `CEventManager::formatEvent` — commit `efb50993780079460b0cbed1363e2166a2de1d9f` (v0.56.2)
verified-at: 2026-10-24
recheck: 90d

## Gate

Re-opened by the lane on **2026-10-24** (fetched bytes kept at
`.ufo/waves/round-32/fetch/S186.bin`, `S187.bin`, `S189.bin`).

- **S186** — https://raw.githubusercontent.com/hyprwm/hyprland-wiki/c04680a28301ab4b5ee5f94eaff5395efe28dbac/content/ipc/_index.md — opened 2026-10-24; 6,539 B, sha256 `535bc4c385a06162d3e7e356e1a13853f9c47598787f15c80883c2895d06d1a4`.
  Quote (`:14`, section `## $XDG_RUNTIME_DIR/hypr/[HIS]/.socket.sock`): "`$XDG_RUNTIME_DIR/hypr/[HIS]/.socket.sock`".
  Quote (`:25`, section `## $XDG_RUNTIME_DIR/hypr/[HIS]/.socket2.sock`): "`$XDG_RUNTIME_DIR/hypr/[HIS]/.socket2.sock`".
  Quote (`:30`): "`EVENT>>DATA\n` (`\n` is a linebreak)".
- **S187** — https://wiki.hypr.land/0.56.0/IPC/ — opened 2026-10-24; 268,731 B; page
  revision "Last updated on May 2, 2026". Quote (rendered text line 239): "`$XDG_RUNTIME_DIR/hypr/[HIS]/.socket.sock`";
  quote (rendered text line 251): "`EVENT>>DATA\n` ( \n is a linebreak)".
- **S189** — https://raw.githubusercontent.com/hyprwm/Hyprland/efb50993780079460b0cbed1363e2166a2de1d9f/src/managers/EventManager.cpp — opened 2026-10-24; 6,479 B, sha256 `eea605dfe5ce09e1f92a67ec478bf61a19894c6e0ee3302c0393521a2ee9540d`.
  Quote (`:21`): `const auto PATH = g_pCompositor->m_instancePath + "/.socket2.sock";`.
  Quote (`:128`): `auto eventString = std::format("{}>>{}\n", event.event, data.substr(0, 1024));`.

**GRANTED** — every claim below is carried by a quote located in these bytes on
2026-10-24. The staged package's own line anchors were not reused: they were
re-derived against the fetched bytes and the anchors named here are the
canonical ones for this entry.

### §1 The request socket (documented)

**OBS** Hyprland exposes two UNIX sockets; the request socket is
`$XDG_RUNTIME_DIR/hypr/[HIS]/.socket.sock` and is used for hyprctl-like requests
(S186:6, S186:14-16; S187 rendered text 235, 239).

> "Basically, write `[flags]/command args`." (S186:19)

**OBS** The evaluation model is synchronous, and holding a connection open
freezes the compositor until the five-second timeout (S186:21-23):

> "Hyprland evaluates connections to this socket completely synchronously, which means that any unclosed connections *will cause Hyprland to freeze*"

**INF** A client that opens, writes and closes per request is safe; a client that
keeps the connection open turns later requests into queued no-ops until the
timeout. Basis: the documented synchronous evaluation and the five-second timeout
in the same note (S186:22).

### §2 The event socket (documented)

**OBS** The event socket is `$XDG_RUNTIME_DIR/hypr/[HIS]/.socket2.sock`, used for
events; each event is one framed line (S186:25-28; S187 rendered text 248, 251):

> "`EVENT>>DATA\n` (`\n` is a linebreak)" (S186:30)

**OBS** The compositor's own implementation at the host's version v0.56.2 creates
the socket as an `AF_UNIX` `SOCK_STREAM` (S189:14), binds it to the instance path
plus `/.socket2.sock` (S189:21) and listens with a backlog of 10 (S189:35).

**OBS** The framing is produced by `CEventManager::formatEvent` (S189:126): the
event name, `>>`, then the data truncated at 1024 characters, then a newline
(S189:128). Embedded newlines inside the data are replaced with spaces
(S189:129).

**OBS** The published event catalogue is 44 events: the upstream wiki table
(S186:36 header, S186:38-81 data rows) carries 44 data rows, counted with
`grep -cE '^\| '` = 46 on the fetched bytes minus one header row and one
separator row; the 0.56.0 rendered page publishes the same catalogue
(S187, opened 2026-10-24).

**INF** The event vocabulary did not change across the 0.56 → 0.57 boundary: the
0.56.0 page and the current-git page publish the same 44 events. Basis: the
two catalogues counted independently on 2026-10-24 (S186, S187).

### §3 What this entry does not claim

- No socket was connected; no event was observed on this host. The framing and
  the catalogue are **documented and source-read**, not observed.
- The 1024-character truncation and the newline sanitisation are the compositor's
  own implementation at v0.56.2 (S189) — a future release may change them.
- The waybar side of the socket (the bar's own subscription and its module-text
  production) is a different surface and is not claimed here.
