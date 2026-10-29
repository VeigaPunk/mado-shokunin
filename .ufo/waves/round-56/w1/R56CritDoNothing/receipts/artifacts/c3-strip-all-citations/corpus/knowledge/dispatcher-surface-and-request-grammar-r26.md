# The dispatcher surface on the host's release line, and how the request socket resolves a dispatcher

Lane: mado-shokunin. Round: 32 (assimilation round, theme: the Hyprland IPC
two-socket contract). Substrates READ-ONLY: nothing under `~/.config/`, `/etc/`,
the runtime dir or any domain source tree was written; **no socket was connected**;
no dispatcher was dispatched; no compositor state was touched. All evidence is a
documentation page read over HTTP on 2026-10-24 by the lane itself.

source: [ref] — https://raw.githubusercontent.com/hyprwm/hyprland-wiki/c04680a28301ab4b5ee5f94eaff5395efe28dbac/content/ipc/_index.md — `# Hyprland IPC` — wiki commit `c04680a28301ab4b5ee5f94eaff5395efe28dbac`
source: [ref] — https://raw.githubusercontent.com/hyprwm/hyprland-wiki/c04680a28301ab4b5ee5f94eaff5395efe28dbac/content/configuring/core/dispatchers.md — `# Dispatchers` — wiki commit `c04680a28301ab4b5ee5f94eaff5395efe28dbac`
source: [ref] — https://wiki.hypr.land/0.56.0/Configuring/Basics/Dispatchers/ — `# Dispatchers` — page revision "Last updated on July 15, 2026"
verified-at: 2026-10-24
recheck: 90d

## Gate

Re-opened by the lane on **2026-10-24** (fetched bytes kept at
`.ufo/waves/round-32/fetch/[ref].bin`).

- **[ref]** — https://wiki.hypr.land/0.56.0/Configuring/Basics/Dispatchers/ — opened 2026-10-24; 297,863 B, sha256 `f9b51362f2440e02999089a255c5d7f3feb103f3cdeb6124c86a9f285c14b6e2`; page revision "Last updated on July 15, 2026".
  Quote (rendered text line 302): "hl.dsp. contains:".
  Quote (rendered text line 459): "hl.dispatch ( hl.dsp . dpms ({ action = \"disable\" }))".

**GRANTED** — the page's own dispatcher groups and its `hl.dsp.*` exposure were
read in the fetched bytes on 2026-10-24; the anchors named here are canonical for
this entry (the staged package carried the revision without its date).

### §1 The 0.56.x line already publishes the Lua dispatcher API

**OBS** The dispatcher page published for the **0.56.0** line — the release line
this host runs (v0.56.2) — already exposes the Lua dispatcher API under
`hl.dsp.` ([ref] rendered text 302) and shows it invoked through `hl.dispatch`
([ref] rendered text 459):

> "hl.dispatch ( hl.dsp . dpms ({ action = \"disable\" }))"

**INF** The Lua dispatcher surface is not a post-0.56 addition: the host's own
release line carries the same dispatcher vocabulary as current upstream. Basis:
the 0.56.0 page publishes `hl.dsp.*` groups ([ref]).

### §2 The dispatcher groups the 0.56.0 page publishes

**OBS** The page groups the vocabulary under `hl.dsp.` and then by object:
`hl.dsp.window.` ([ref] rendered text 348), `hl.dsp.workspace.` (414),
`hl.dsp.group.` (426) and `hl.dsp.cursor.` (444).

**OBS** Reading the fetched page text, these dispatcher names occur:
`exec_cmd`, `exec_raw`, `focus`, `exit`, `submap`, `pass`, `send_shortcut`,
`dpms`, `event`, `global`, `force_idle`, `workspace`, `window`, `group`,
`cursor`, `monitor` (16 names; counted over the fetched text on 2026-10-24).

**INF** The published 0.56.0 vocabulary covers the general dispatchers
(`exec_cmd`, `exec_raw`, `focus`, `exit`, `submap`, `pass`, `send_shortcut`,
`dpms`, `event`, `global`, `force_idle`) plus per-object groups
(`workspace`, `window`, `group`, `cursor`, `monitor`). This is the *documented*
surface on the host's release line; it is not a claim that any of them was
dispatched here.

### §3 How the request socket relates to a dispatcher

**OBS** The request socket's grammar is a flag-prefixed command line
([ref]:19, the `hyprctl` request socket) and the event socket carries the
`EVENT>>DATA` framing ([ref]:30). A dispatcher is not itself a socket request:
it is a table that must be wrapped in `hl.dispatch()` to run ([ref]:14).

**INF** Two different surfaces meet here and must not be conflated: the *socket
request* surface (what `hyprctl` writes) and the *dispatcher* surface (what a
Lua config builds). The only documented bridge is the `event` dispatcher, which
sends to socket2 ([ref]:59).

### §4 What this entry does not claim

- Nothing was dispatched, requested or observed on the host.
- The name list is what the fetched page text contains, not an exhaustive API
  inventory; the wiki keeps layout-specific dispatchers on the layout pages
  ([ref]:12).
- The page's "Last updated on July 15, 2026" is the revision string observed on
  2026-10-24; a later fetch may show a different one.

## Amendment — re-grounded dispatcher surface and request-socket resolution (2026-10-25)

Lane: mado-shokunin. Round: 39 (assimilation theme from the shokuknow `merge/mado/`
package: its deferred amendment to this entry, re-grounded here against bytes re-opened
this round; the package's own text and quotes are not cited). The held text above is
unchanged; this section is appended.

source: [ref] — Hyprland v0.56.2 `src/debug/HyprCtl.cpp` @ `efb50993780079460b0cbed1363e2166a2de1d9f`; [ref] — the 0.56.0 Dispatchers page
verified-at: 2026-10-25
recheck: on-release

Re-opened 2026-10-25: [ref] raw bytes → `.ufo/waves/round-39/fetch/[ref]-r39.bin`, 97582 B,
sha256 `798b7c6c4c1684557842463d46ac99c96629be4179e0e461dca77670247b91fa` (equal to the held
round-24 receipt, so the line numbers below are the host commit's); [ref] →
`.ufo/waves/round-39/fetch/[ref]-r39.bin`, 297863 B, sha256
`f9b51362f2440e02999089a255c5d7f3feb103f3cdeb6124c86a9f285c14b6e2` (byte-identical to the
round-32 receipt; same "Last updated on July 15, 2026" revision).

### §A1 The 0.56.0 page states what a dispatcher value is for ([ref])

**OBS** [ref], opening paragraph of the `#dispatchers` section: "Their purpose is to be fed
into hl.bind() or hl.dispatch()." — preceded by "Dispatchers return tables that describe an
action you want to make."

**INF** On the host's release line a Lua dispatcher is a value, not an action: nothing runs
until `hl.bind()` or `hl.dispatch()` consumes it.

### §A2 The request socket resolves a dispatcher by name ([ref])

**OBS** `dispatchRequest` ([ref]:1126) looks the first word up in the keybind manager's
registry — [ref]:1149 `const auto DISPATCHER = g_pKeybindManager->m_dispatchers.find(DISPATCHSTR);`
— and an unknown name returns the literal [ref]:1151 `return "Invalid dispatcher";`.

**OBS** Under the Lua config provider the request is wrapped instead of looked up:
[ref]:1131 "For lua, this is just a wrapper for `eval("hl.dispatch(in)")" and [ref]:1132
`std::string evalStr = std::format("return hl.dispatch({})", in);`.

**OBS** Batches split on `;` outside brackets: `dispatchBatch` ([ref]:1309), comment at
[ref]:1310 "split by ; ignores ; inside [] and adds ; on last command".

**OBS** Request flags (`j`, `r`, `a`, `c` at [ref]:2085-2093) are stripped before the command
is compared: [ref]:2096 "remove flags and separator so we can compare the rest of the string".

**INF** The socket-side surface this entry's §3 kept apart from the Lua surface is: one name
resolved against `m_dispatchers` (hyprlang provider) or one `hl.dispatch(...)` evaluation
(Lua provider); an unknown name is the string `Invalid dispatcher`, not a socket error.

### §A3 What this amendment does not claim

- **[UNK]** Host-observable effects of each request flag: [ref]:2085-2093 shows only which
  internal switch each flag sets.
- No request was sent and no dispatcher dispatched; this is a source reading.
