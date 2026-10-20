# Reopen S076 — non-author check (wave 2, R17-V3)

Seat `MadoR18.ReopenS076`. Question: is the newly credited SOURCES row S076
(`walker src/data.rs @ v2.17.2`, P3 route) authority-bearing — kind, tier, scope,
grounded `teaches` — and does `corpus/knowledge/walker-route-r18.md` use it
truthfully? Read-only outside `.ufo/waves/round-18/fetch/ReopenS076/` and this
report; no lane VCS command, no host service or package probe.

Axes: (1) digest authority of the fetched body; (2) anchor/claim fidelity to
file lines; (3) truthfulness of the citing note; (4) pin immutability.

## Commands run and their output

1. Independent fetch (receipt appended):

```
$ curl -sSL --max-time 60 -o .ufo/waves/round-18/fetch/ReopenS076/walker-data.rs \
    -w '%{http_code} %{url_effective}\n' \
    https://raw.githubusercontent.com/abenz1267/walker/v2.17.2/src/data.rs
200 https://raw.githubusercontent.com/abenz1267/walker/v2.17.2/src/data.rs
$ sha256sum …/walker-data.rs
996db119ba61cb1505aa26782a19c7b8db49889874bd87ecbf277c9145cada09
$ wc -c -l …/walker-data.rs
862 26338            # 862 lines, 26,338 bytes
```

2. Tag resolution (remote read only):

```
$ git ls-remote https://github.com/abenz1267/walker 'refs/tags/v2.17.2*' 'refs/tags/v2.17.1*'
56c9e2b69e7d2b00f0f9481ae8c89f53810c1de5	refs/tags/v2.17.1
a515085fd39fae80acc086c8fbfd9b7771a9a11d	refs/tags/v2.17.2
$ git ls-remote https://github.com/abenz1267/walker refs/tags/v2.17.2 'refs/tags/v2.17.2^{}'
a515085fd39fae80acc086c8fbfd9b7771a9a11d	refs/tags/v2.17.2      # no peeled line
$ git ls-remote --heads https://github.com/abenz1267/walker | grep -c 'refs/heads/v2.17.2$'
0
```

No `^{}` line and no branch of that name: `v2.17.2` is a lightweight tag at
commit `a515085f…`, with no branch/tag name collision at that path. **The URL is
tag-pinned** (its second path segment resolves to `refs/tags/v2.17.2`), not
branch- or moving-`main`-pinned.

3. Receipt join for the same URL, over `fetch/*/receipts.jsonl`:

| file:line | url form | status | bytes | sha256 | fetched_at |
|---|---|---|---|---|---|
| NoteWalker/receipts.jsonl:26 | `v2.17.2/src/data.rs` | 200 | 26338 | `996db119…cada09` | 2026-10-20T15:41:43Z |
| ReviewWalkerUpstream/receipts.jsonl:5 | `v2.17.2/src/data.rs` | 200 | 26338 | `996db119…cada09` | 2026-10-20T16:00:36Z |
| SrcElephantReadme/receipts.jsonl:9 | `a515085f…/src/data.rs` | 200 | 26338 | `996db119…cada09` | 2026-10-20T15:42:30Z |
| ReopenS076/receipts.jsonl:1 | `v2.17.2/src/data.rs` | 200 | 26338 | `996db119…cada09` | 2026-10-20T16:01:22Z |

The stored bodies were re-hashed and all match: `NoteWalker/walker-v2.17.2-src-data.rs`,
`ReviewWalkerUpstream/walker-2.17.2-src-data.rs`, `SrcElephantReadme/walker-src_data.rs.body`,
`ReopenS076/walker-data.rs` → each `996db119ba61cb1505aa26782a19c7b8db49889874bd87ecbf277c9145cada09`.
The commit-pinned receipt is the decisive control: raw.githubusercontent serves
the identical 26,338 bytes for `a515085f…/src/data.rs`, so the tag form and the
commit form agree byte for byte at 4/4 receipts across 3 seats plus this one.

## Row cell check (corpus/SOURCES.md:88)

| cell | recorded | observed |
|---|---|---|
| kind | `code` | upstream Rust source (`src/data.rs`); matches siblings S073/S074/S075/S077 |
| tier | `A` | primary upstream source at the pinned tag for exactly this scope |
| scope | "walker's client connection to elephant (socket path and reconnect)" | names the P3 keyword **walker** (and elephant); the file is the client side |
| anchor | "file lines 148-169, 653-660; sha256 996db119…" | line ranges exist and are the right ones; digest matches my body exactly |
| teaches | "$XDG_RUNTIME_DIR/elephant/elephant.sock and retries after a disconnect" | grounded, see below |
| status/opened/recheck/used-by | `mined` / 2026-10-20 / on-release / walker-route-r18.md | consistent with the tag-pinned class (cf. S018 `on-release`) |

Groundedness of `teaches`, from the body I read:

- `:148` `pub fn init_socket()`; path built at `:156-158`
  (`env::var("XDG_RUNTIME_DIR").map(PathBuf::from).unwrap_or_else(|_| env::temp_dir())`)
  then `:160` `socket_path.push("elephant");` and `:161`
  `socket_path.push("elephant.sock");` → `$XDG_RUNTIME_DIR/elephant/elephant.sock`,
  fallback `env::temp_dir()/elephant/elephant.sock`.
- `:168-181` connect-loop: `UnixStream::connect(&socket_path)`, failure prints
  "Failed to connect: … Retrying in 1 second..." and sleeps 1 s; `:184-192`
  repeats for the menu connection and `:196-209` for bluetooth when the provider
  is present.
- `:653-660` `fn handle_disconnect()` → `set_is_connected(false)` then
  `thread::spawn` running `while let Err(err) = init_socket() { println!("{err}"); }`;
  reached from the listen-loop teardown at `:248, 255, 263` (and the reply paths
  at `:598, 679, 701, 796`).

So both halves of the `teaches` sentence are literally in the anchored ranges.
Scope drift: none — the row claims neither the wire protocol nor host behaviour.
The `teaches` cell omits the `env::temp_dir()` fallback; that is an omission, not
a false statement, and the citing note states the fallback explicitly.

## Note use (corpus/knowledge/walker-route-r18.md)

- `:1` source line names S076 with this exact URL and the two anchored functions
  (`init_socket, handle_disconnect`) — accurate; `:25` defines `WD:n` as file lines
  of the same tag file.
- `:128-129` "walker connects to `$XDG_RUNTIME_DIR/elephant/elephant.sock`
  (fallback `env::temp_dir()`)" `[WD:156-161, 169]` — anchors are inside the row's
  148-169 range and say what the note says.
- `:136-137` "`handle_disconnect` sets the state and spawns a retry loop around
  `init_socket`" `[WD:653-660]` — exactly the row's second range.
- `:309-310` leaves the elephant socket protocol `[UNK]`; the note does not
  upgrade the row's documentary scope into an observed one, and the header
  (`:8-10`) says no walker/elephant process was started. Truthful.

No other SOURCES row names `src/data.rs` (single row, no duplicate credit).

## Residual unknowns

- The pin is a tag, not a commit: `refs/tags/v2.17.2` could be force-moved
  upstream. `[UNK]` whether it will be; the row's digest would catch a move, and
  the commit-pinned fetch (`a515085f…`, same digest) fixes the body today.
- `[UNK]` whether `/usr/bin/walker` on this host is built from this tag — out of
  the row's documentary scope (the note marks it `[UNK]` at `:288-289`).
- The row lists no further files in its source/anchor cells, so nothing else was
  re-fetched; the note's two other `WD` anchors are both inside the row's ranges.

**Judgement: agree.** Kind, tier, scope keyword, anchor lines and digest all hold;
`teaches` is grounded; the note cites the row within the anchored lines and does
not over-claim.

GATE | S076 | https://raw.githubusercontent.com/abenz1267/walker/v2.17.2/src/data.rs | 2026-10-20 | .ufo/waves/round-18/fetch/ReopenS076/walker-data.rs:156-161 "let mut socket_path = env::var(\"XDG_RUNTIME_DIR\") .map(PathBuf::from) .unwrap_or_else(|_| env::temp_dir()); socket_path.push(\"elephant\"); socket_path.push(\"elephant.sock\");" (10 words) | 996db119ba61cb1505aa26782a19c7b8db49889874bd87ecbf277c9145cada09 | agree: my 200/26338-byte fetch and 3 prior receipts (incl. the commit-pinned a515085f form) agree on this digest; lines 148-169/653-660 carry the socket path and the reconnect loop, and walker-route-r18.md:128-137 cites only those lines
