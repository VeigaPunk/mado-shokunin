## Amendment — re-grounded dispatcher surface and request-socket resolution (2026-10-25)

Lane: mado-shokunin. Round: 39 (assimilation theme: dispatcher surface and
request-socket resolution). Read-only: no compositor, socket, service or config
tree was touched; the held entry text above stays untouched; this block is
appended as a dated section. All quotes were re-opened this round against the
held S018 receipt bytes.

source: S018 — https://github.com/hyprwm/Hyprland/blob/v0.56.2/src/debug/HyprCtl.cpp — tag commit `efb50993780079460b0cbed1363e2166a2de1d9f` (v0.56.2); held row anchor `dispatchGetProp`, lines 1463-1645; file sha256 `798b7c6c4c1684557842463d46ac99c96629be4179e0e461dca77670247b91fa`
source: S220 — https://wiki.hypr.land/0.56.0/Configuring/Basics/Dispatchers/ — fetched 2026-10-25, 297,863 B, sha256 `f9b51362f2440e02999089a255c5d7f3feb103f3cdeb6124c86a9f285c14b6e2`; page revision "Last updated on July 15, 2026"
verified-at: 2026-10-25
recheck: on-release

### Gate

Re-opened this round, read-only:

- S018 bytes re-read from `.ufo/waves/round-24/fetch/S158.bin` (committed round-24
  fetch); `sha256sum` = `798b7c6c…`, equal to the S018 row hash, so the line numbers
  below are the upstream line numbers at `efb50993780079460b0cbed1363e2166a2de1d9f`.
- S220 bytes read from `.ufo/waves/round-39/w1/ExecAssimFetches/S220.bin` (this
  round's fetch receipt); `sha256sum` = `f9b51362…`, equal to the held S196 fetch
  bytes (same page revision).

**GRANTED** — the S220 bytes carry the section `#dispatchers` and the two quotes
cited; the S018 bytes carry the five code quotes cited.

### §1 The 0.56.0 Dispatchers page exists (S220)

**OBS** The page exists at `/0.56.0/Configuring/Basics/Dispatchers/`; under the
section anchor `#dispatchers` (S220.bin raw HTML lines 2936-2938) the paragraph says:

```
Dispatchers return tables that describe an action you want to make.
Their purpose is to be fed into hl.bind() or hl.dispatch().
```

(First sentence ends at raw line 2937, 10 words; second at raw line 2938, 11
words.)

**INF** On the 0.56.0 line the dispatcher vocabulary is published as tables that
`hl.bind()` / `hl.dispatch()` consume. This corroborates, on the same release line,
the held entry's S196 observation of the Lua API (`hl.dsp.*`, `hl.dispatch`) and the
`dispatchers`-section anchor in the held Gate (S196 quotes).

### §2 The request socket resolves a dispatcher name in the keybind manager's registry (S018)

**OBS** In `HyprCtl.cpp@efb5099`, `dispatchRequest` (starts S018:1126) strips the
`dispatch` keyword, splits off the first space-separated word as the dispatcher name,
and resolves it against the keybind manager's registry:

```
S018:1149 | const auto DISPATCHER = g_pKeybindManager->m_dispatchers.find(DISPATCHSTR);   (5 words)
```

**OBS** When the name is absent from `m_dispatchers`, the request returns the literal
error string:

```
S018:1151 | return "Invalid dispatcher";   (3 words)
```

**OBS** When the config provider is Lua, the whole request is wrapped as a Lua
expression instead of a registry lookup:

```
S018:1131 | // For lua, this is just a wrapper for `eval("hl.dispatch(in)")   (10 words)
S018:1132 | std::string evalStr = std::format("return hl.dispatch({})", in);   (6 words)
```

**OBS** Batch requests are split on `;` only outside brackets, with a virtual
trailing `;`:

```
S018:1309-1310 | dispatchBatch → // split by ; ignores ; inside [] and adds ; on last command   (14 words)
```

**OBS** Non-batch request flags are scanned until the first space in
`CHyprCtl::getReply` and then stripped before command comparison:

```
S018:2096 | request = request.substr(sepIndex + 1); // remove flags and separator so we can compare the rest of the string   (19 words)
```

**INF** The socket-side dispatcher surface is therefore: one name resolved against
the keybind manager's `m_dispatchers` map (S018:1149); the literal `"Invalid
dispatcher"` error for unknown names (S018:1151); full Lua wrapping under the Lua
provider (S018:1131-1132); bracket-aware batch splitting (S018:1309-1310); and
prefix flag stripping in `getReply` (S018:2096). This grounds the held entry's §3
statement that a dispatcher is not a bare socket request: on the request socket it is
a name lookup in a registry (or a Lua expression in Lua-config mode).

### §3 What this amendment does not claim

- **[UNK]** Per-flag semantics of the request socket are unenumerated: S018:2085-2093
  shows only which flag (`j`/`r`/`a`/`c`) sets which internal switch; nothing here
  claims their host-observable effects.
- **[UNK]** Host config flag usage is uninspected: no host config tree was opened this
  round, so no claim is made about which flags the host's own config passes.
- Static source parse is not live health: no request was sent, no dispatcher
  dispatched, and no socket was connected (read-only lane review, 2026-10-25).
