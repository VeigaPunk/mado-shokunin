# The request socket's flags, as published for the host's release line

Lane: mado-shokunin. Round: 38 (adopted from the shokuknow `corpus-expansion-1`
package, re-grounded against bytes fetched this round). **Amends**
`corpus/knowledge/dispatcher-surface-and-request-grammar-r26.md` §3,
which records the request grammar and its `[flags]` slot without detailing the
per-flag semantics.

source: [ref] — https://wiki.hypr.land/0.56.0/Configuring/Advanced-and-Cool/Using-hyprctl/ — `§ Flags` — 0.56.0 docs, fetched 2026-10-25
verified-at: 2026-10-25
recheck: on-release
ground: a new edge class under the held IPC contract (`knowledge/ipc-contract-r25.md`): the published flag vocabulary of the request socket — the grammar held `[flags]/command args`, never the flag list

### §1 The documented flags (the `flag list:` block)

**OBS** [ref]: the 0.56.0 documentation publishes the flag list as three flags —
`j -> output in JSON`; `i -> select instance (id or index in hyprctl instances)`; `r -> force state refresh after issuing commands (e.g. layout or rule changes)` — inside the page's `flag list:` code block.

**INF** [ref]: the flags are *client-facing output and targeting modifiers*, not
per-dispatcher options: `j` changes the reply's encoding, `i` chooses which
compositor instance answers, and `r` asks the compositor to force a state refresh
after issuing commands (the page's own wording; the refresh runs after the
reply is built in the host's handler, [ref] `:2107`/`:2126`). The published list
is the CLI-facing flag list: the server's own request parser accepts `j`, `r`,
`a`, `c` ([ref] `:2085-2092`) — `i` never reaches the socket (it selects the
instance in the client, `hyprctl/src/main.cpp:427`), and `a`/`c` are
undisclosed socket flags. Basis: the three
flag descriptions read together with the request grammar
(`knowledge/ipc-contract-r25.md` §1 line 42, [ref] `:19`).

### §2 The synchronous-dispatch warning

**OBS** [ref]: the same page warns `hyprctl calls will be dispatched by the
compositor synchronously, meaning any spam of the utility will cause
slowdowns.`

**INF** [ref], [ref]: this is the documented counterpart of the request socket's
synchronous evaluation (`ipc-contract-r25.md` §1 lines 44-47): the flag `r` is the price of
correctness (a state refresh) paid on a synchronously served socket — which is
why spamming `hyprctl` hurts.

### §3 What remains unmeasured

**OBS** [ref]: the server strips a leading flag segment before matching the
dispatcher name and accepts `j`, `r`, `a`, `c` (`:2085-2096`); the published
list omits `a`/`c`, and `i` is client-side. **UNK** Whether the host's own
configuration ever issues a flagged request was not inspected.

Corrections applied while re-grounding (package draft → this entry): the
package's `recheck` cell carried prose and a run note; the lane's schema keeps
`on-release` only. The quoted flag list is verbatim from the 0.56.0 page's
code block (HTML `&gt;` unescaped). The page also names a fourth, legacy,
`--batch` flag ([ref] `:3375`); it sits outside the `flag list:` block and is
not part of this entry's scoped claim.
