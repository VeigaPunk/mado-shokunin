# The request socket's flags, as published for the host's release line

Lane: mado-shokunin. Round: 38 (adopted from the shokuknow `corpus-expansion-1`
package, re-grounded against bytes fetched this round). **Amends**
`corpus/knowledge/dispatcher-surface-and-request-grammar-r26.md` §3, whose open
item was the per-flag semantics.

source: S221 — https://wiki.hypr.land/0.56.0/Configuring/Advanced-and-Cool/Using-hyprctl/ — `§ Flags` — 0.56.0 docs, fetched 2026-10-25
verified-at: 2026-10-25
recheck: on-release
ground: a new edge class under the held IPC contract (`knowledge/ipc-contract-r25.md`): the published flag vocabulary of the request socket — the grammar held `[flags]/command args`, never the flag list

### §1 The three documented flags

**OBS** S221: the 0.56.0 documentation publishes the flag list as three flags —
`j -> output in JSON`; `i -> select instance (id or index in hyprctl instances)`; `r -> force state refresh after issuing commands (e.g. layout or rule changes)` — inside the page's `flag list:` code block.

**INF** S221: the flags are *client-facing output and targeting modifiers*, not
per-dispatcher options: `j` changes the reply's encoding, `i` chooses which
compositor instance answers, and `r` asks the compositor to re-read its state
after a mutating command so the reply reflects the new state. Basis: the three
flag descriptions read together with the request grammar
(`knowledge/ipc-contract-r25.md` §2, S186 `:19`).

### §2 The synchronous-dispatch warning

**OBS** S221: the same page warns `hyprctl calls will be dispatched by the
compositor synchronously, meaning any spam of the utility will cause
slowdowns.`

**INF** S221, S187: this is the documented counterpart of the request socket's
synchronous evaluation (`ipc-contract-r25.md` §2): the flag `r` is the price of
correctness (a state refresh) paid on a synchronously served socket — which is
why spamming `hyprctl` hurts.

### §3 What remains unmeasured

**UNK** The server-side handling of each flag was not re-read this round — the
IPC contract established that a leading flag segment is stripped before the
dispatcher name is matched, not what the server then does with `j`, `i` or
`r`. **UNK** Whether the host's own configuration ever issues a flagged
request was not inspected.

Corrections applied while re-grounding (package draft → this entry): the
package's `recheck` cell carried prose and a run note; the lane's schema keeps
`on-release` only and the run note lives in the round-38 lesson. The quoted
flag list is verbatim from the 0.56.0 page's code block (HTML `&gt;`
unescaped).
