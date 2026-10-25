# The request socket's live bound is a five-second timeout, not a byte cap

Lane: mado-shokunin. Round: 38 (adopted from the shokuknow `corpus-expansion-1`
package, re-grounded against bytes fetched this round). **Amends**
`corpus/knowledge/ipc-contract-r25.md`, which holds the documented contract and
names the five-second timeout in prose without reading the code that
implements it.

source: S158 — Hyprland v0.56.2 `src/debug/HyprCtl.cpp` @ `efb50993780079460b0cbed1363e2166a2de1d9f` (the host's own commit; same bytes as the package's tag-URL citation); S187 — the 0.56.0 IPC page (same document as the package's); S277 — `iconidentify/chonkstep` `docs/hyprland-ipc.md` (community measurement, tier C); S258 — host socket stat receipt `.ufo/waves/round-38/fetch/stat-sockets.txt` (own-work)
verified-at: 2026-10-25
recheck: on-release
ground: a new edge class under the held IPC contract (`knowledge/ipc-contract-r25.md`): what actually bounds a request on the request socket — the host's own accept loop, read at its own commit

### §1 The question was misframed, and that is the answer

**OBS** The bound question assumed a byte ceiling existed. The host's own
accept loop answers differently (S158):

> `int ret = poll(pollfds, 1, 5000);`

**OBS** S158: the `5000` is a poll timeout in milliseconds — the compositor
waits five seconds for data on an accepted connection and closes it if nothing arrives (`:2264` poll, `:2266-2268` close on `ret <= 0`). The read that
follows is a 1023-byte chunk loop (`:2274` `read(ACCEPTEDCONNECTION,
readBuffer.data(), 1023)`, `:2278` break on a short read); the request is the
accumulation of the chunks, with no byte bound anywhere in the handler.

**OBS** S187: upstream states the same contract in prose at the host's
version family — `Hyprland evaluates connections to this socket completely synchronously,` and unclosed connections `will cause Hyprland to freeze`.

**INF** S158, S187: the live bound on this host's request socket is **temporal,
not volumetric**: a request is bounded by the five-second timeout, and the
compositor evaluates the connection synchronously, so an unclosed connection
blocks the compositor until that timeout expires. There is no byte cap to
measure against; a "live cap" measurement would return "no cap" rather than a
number.

### §2 The framing is independent of the bound

**OBS** S187: the event socket's framing is `EVENT>>DATA\n`, and the request
socket takes `[flag(s)]/command args`.

**OBS** S277: a third party that re-implements Hyprland's IPC measured the
grammar off a real client and reports the same — `There is no length prefix or newline.` and `[[BATCH]]` batch requests with `;` separators — a
community-tier cross-check, not first-party evidence.

**OBS** S258: on this host the transport is equally modest — the instance
the instance directory — `directory /run/user/1000/hypr/` — carries mode 0700, its sockets
0755, so the directory's mode is the effective access control; nothing
outside the user's own UID reaches the socket path.

**UNK** The effective bound in practice — how much a single request can carry
before the host's own memory or socket buffer objects — is still not
measured; measuring it would mean sending an oversized request to the live
socket, an action this lane declines.

Corrections applied while re-grounding: the package's two citations —
HyprCtl.cpp at tag `v0.56.2` and the 0.56.0 IPC page — re-point to the held
rows named in the `source:` line above (same documents, byte-identical
re-fetches; sha256 in the round-38 Gate block). The chonkstep row stays a
community-tier source; its grammar cross-check is kept at tier C weight.
