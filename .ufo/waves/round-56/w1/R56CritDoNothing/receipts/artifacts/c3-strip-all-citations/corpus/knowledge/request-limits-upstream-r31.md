# What the compositor now allows: a 1 MiB request, a 64 KiB followed queue

Lane: mado-shokunin. Round: 38 (adopted from the shokuknow `corpus-expansion-1`
package, re-grounded against bytes fetched this round). **Extends**
`corpus/knowledge/request-socket-live-bound-r8.md`: the host's handler has no
byte bound, and this entry answers what *upstream now declares* — at a later
revision than the host runs.

source: [ref] — Hyprland `src/ipc/s1/Unix.cpp` @ commit `a1c2428f79b3b05c3fd36c27378e3538c8c6a014` (current upstream; this file does not exist at the host's tag v0.56.2)
verified-at: 2026-10-25
recheck: on-release
ground: a new edge class under the held IPC contract (`knowledge/ipc-contract-r25.md`): upstream-declared request ceilings — the question the lane could not answer from the host's own, older, code

### §1 The upstream ceilings

**OBS** [ref]: the compositor's current request socket declares two ceilings —

> `static constexpr size_t REQUEST_LIMIT      = 1024 * 1024;`

> `static constexpr size_t FOLLOW_QUEUE_LIMIT = 64 * 1024;`

**OBS** [ref]: and applies the first to the accumulated request —
`if (m_input.size() > REQUEST_LIMIT)` inside `readRequest` (`:118`), and the
second to a followed stream's queue — `if (queuedBytes() + data.size() >
FOLLOW_QUEUE_LIMIT)` inside `addFollowData` (`:166`).

**INF** [ref]: a request to the *current* compositor is bounded at **1 MiB**,
and a followed stream's queue at **64 KiB**. Two corrections follow for the
lane's record: the 64 KiB figure in the refused package draft
(`merge/mado/…/socket-client-contract-measurements-r29.md`, "requests are
capped at 64 KiB") is that re-implementation's own request cap — [ref] `:61`
("Requests are capped at 64 KiB") is byte-identical to the draft's cited
[ref] — not upstream's `FOLLOW_QUEUE_LIMIT`; and this host's v0.56.2 declares
neither — its handler accumulates 1023-byte chunks with no total bound
([ref] `:2270-2280`, `knowledge/request-socket-live-bound-r8.md` §1).

**INF** [ref], [ref]: a client can therefore send a request larger than 64 KiB to
this compositor and stay within the documented contract; what the host's
version will *do* with it is not bounded by the code the host runs.

**UNK** The ceilings were read from a **later** upstream revision than the
host runs — `src/ipc/s1/Unix.cpp` returns 404 at the host's tag
`efb50993780079460b0cbed1363e2166a2de1d9f` (fetched 2026-10-25), so the
constants belong to upstream's post-0.56.2 IPC restructure — and nothing was
measured against a live socket; connecting is outside this lane's authority.

Corrections applied while re-grounding: none to the package's facts — the two
constants, the two check sites and the later-revision caveat all verify
against the fetched bytes. The re-point is of scope only: the package's
amend-chain named an entry this lane refuses (`socket-modes-and-request-read-r30.md`),
so the entry stands on `request-socket-live-bound-r8.md` instead.
