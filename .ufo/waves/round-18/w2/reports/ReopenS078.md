# Re-open S078 — non-author check (R17-V3)

Seat: MadoR18.ReopenS078. Lane root `/home/vgpnk/Projects/shokunin/mado-shokunin`.
Row under test: `corpus/SOURCES.md:90` (S078, walker `Cargo.toml` @ v2.17.2).
Everything below was read, fetched or hashed by this seat; nothing was executed
from the target tree.

## Verdict

**agree.** The anchor sha256 reproduces byte-for-byte from an independent fetch,
the URL is tag-pinned, both wave-1 receipts carry the same digest and their saved
bodies re-hash to it, and every clause of `teaches` reproduces from the tag tree.
The citing note uses the row truthfully; one wording nit is recorded below but
does not change any behavioural claim.

## Independent fetch and hash

Command (per fetch rules, receipted in
`.ufo/waves/round-18/fetch/ReopenS078/receipts.jsonl`):

    curl -sSL --max-time 60 -o cargo-toml.body \
      -w '%{http_code} %{url_effective}' \
      https://raw.githubusercontent.com/abenz1267/walker/v2.17.2/Cargo.toml

Result: `200 https://raw.githubusercontent.com/abenz1267/walker/v2.17.2/Cargo.toml`,
952 bytes, sha256
`d1676045d1101a2d92c5669e54e36e63363d3e79dbc10c561662039ae2453a90`.

| comparison | value | row / receipt |
|---|---|---|
| row anchor cell | `d1676045d1101a2d92c5669e54e36e63363d3e79dbc10c561662039ae2453a90` | equal |
| `fetch/NoteWalker/receipts.jsonl:4` | `d1676045…`, 952 B, body `walker-v2.17.2-cargo.toml` | equal; saved body re-hashed by this seat = `d1676045…` |
| `fetch/MadoR18.SrcWalkerThemes/receipts.jsonl:11` | `d1676045…`, 952 B, body `cargo-toml.txt` | equal; saved body re-hashed by this seat = `d1676045…` |
| tag tarball `Cargo.toml` (extracted under `/tmp/s078w`) | `d1676045…` | equal |

Census of receipts for this exact URL across `.ufo/waves/round-18/`: 26
`receipts.jsonl` files, exactly 2 lines name this URL (the two above), both
`http_status` 200, both the same digest, written 2026-10-20T15:40:36Z and
2026-10-20T15:41:16Z by different seats. No disagreeing receipt exists.

## Tag pinning

    git ls-remote https://github.com/abenz1267/walker refs/tags/v2.17.2 'refs/tags/v2.17.2^{}'

returned one line:

    a515085fd39fae80acc086c8fbfd9b7771a9a11d	refs/tags/v2.17.2   (rc=0)

No `^{}` peeled line, so `v2.17.2` is a lightweight tag. The URL path segment is
`v2.17.2`, i.e. a ref name, so the URL **is tag-pinned** in the rubric sense: it
cannot drift with `master`. Residual caveat: a lightweight tag is a movable ref
server-side; the row's `on-release` recheck is the right guard, and the tag hash
above (`a515085f…`) is the value a future re-open should still see. This matches
the tag resolution recorded in `walker-route-r18.md:7`.

Corroboration that the tag tree and the raw file are the same artifact: the
codeload tarball for the tag is 165,438 B, sha256
`e50c606040b24f2a6045292f5f6a08c8a05ac599878ac781b1a5fcf50d353a56` — equal to
S079's anchor cell — and its extracted `walker-2.17.2/Cargo.toml` hashes to the
same `d1676045…`.

## Line-level grounding (body anchors)

Body read: `.ufo/waves/round-18/fetch/ReopenS078/cargo-toml.body` (36 lines):

- `:1` `[package]`; `:2` `name = "walker"`; `:3` `version = "2.17.2"`.
- `:6` `[dependencies]` through `:32` (`niri-ipc = "=26.4.0"` last).
- `:21` `notify = "8.2.0"` — the exact declaration quoted by the row.
- `:34-36` `[build-dependencies]` `protobuf-codegen`, `protoc-bin-vendored`.

So the anchor cell "file lines 2-3, 21" and the teaches quote
`version = "2.17.2"` are exact; nothing is paraphrased.

## Does the second clause hold? (`notify` declared, used nowhere in `src/`)

Re-ran the whole-tree search on the freshly fetched tag tarball (extracted to
`/tmp/s078w`, which is not a git clone and was not executed):

- `grep -rnE 'use notify|notify::|inotify' walker-2.17.2/src/` → no matches.
- `grep -rn 'notify' walker-2.17.2/src/` → only closure parameter names in
  `src/niri.rs:160,168,185,205,212,213`.
- `Cargo.lock:1348-1360`: crate `notify` 8.2.0, dependency list includes
  `inotify`.
- Whole-tree, case-insensitive: `Cargo.toml:21`, `Cargo.lock` (crate entry),
  `src/niri.rs` (closure params), `LICENSE:419` (GPL prose "notify you").

Conclusion: the substantive claim — declared dependency, no `src/` use — is
exact. The note's abstract sentence "finds `notify` only in the `Cargo.lock`
entry … and as closure parameter names" is loosely worded (it omits the
`Cargo.toml` declaration it is itself quoting, and the LICENSE prose word), but
it is immediately narrowed by "no `notify::` path, no `use notify`, no
`inotify` call in `src/`", which is exactly what I measured. Wording nit only;
no behavioural overclaim, and the note carries the call-graph `[UNK]` at
`:299`.

## Note truthfulness (`corpus/knowledge/walker-route-r18.md`)

- `:51` "package version `2.17.2` [WK:2-3]" — line 3 carries it, line 2 carries
  the package name; accurate.
- `:99` "`notify = "8.2.0"` [WK:21]" and the unused-in-`src/` claim — accurate
  per above; the tarball cross-reference `[WX]` resolves to S079, whose anchor I
  reproduced independently (165,438 B, `e50c6060…`).
- `:299` keeps the reachability question `[UNK]` — correct epistemic bound: a
  textual whole-tree search is not a call graph.
- No citation of S078 exists in `theme-route-r18.md`, consistent with
  `used-by` naming only the walker note.

## Row judgement (kind / tier / scope / teaches)

- **kind `code`** — a build manifest, primary source for declarations; matches
  how the registry treats other manifests/scripts.
- **tier A** — upstream primary artifact at an immutable ref name; the scope is
  exactly what the file states about itself, no projection onto the host binary
  or the Arch package.
- **scope** — "walker package version and dependency list at tag v2.17.2":
  names the surface keyword `walker` (P3), and is finite to the file's own
  package/dependency tables. No host behaviour is implied.
- **teaches** — both clauses grounded (`:3`, `:21`), and the non-use clause is
  transparently delegated to the tarball row rather than smuggled in. The
  reference resolves: I re-fetched and re-hashed the tarball.
- **status/recheck/used-by** — `mined`, `on-release`, walker note: appropriate
  for a tag-anchored row. No status change proposed.

## Commands run (all read-only)

    git ls-remote https://github.com/abenz1267/walker refs/tags/v2.17.2 'refs/tags/v2.17.2^{}'
    curl -sSL --max-time 60 -o cargo-toml.body -w '%{http_code} %{url_effective}' <raw URL>
    curl -sSL --max-time 60 -o walker-v2.17.2.tar.gz -w '%{http_code} %{url_effective}' <codeload URL>
    sha256sum / wc -c / cat -n on the fetched bodies
    grep -rn 'walker/v2.17.2/Cargo.toml' --include=receipts.jsonl .ufo/waves/round-18/
    tar -xzf <tarball> -C /tmp/s078w; grep -rn 'notify' on the extracted tree
    sha256sum on both wave-1 saved bodies (NoteWalker, MadoR18.SrcWalkerThemes)

No package, service, compositor, socket, browser or REA operation was used; the
target tree was never executed.

## Remaining unknowns

- `[UNK]` Whether upstream will ever move the lightweight `v2.17.2` tag; the
  recorded commit `a515085fd39fae80acc086c8fbfd9b7771a9a11d` is the only stable
  cross-check.
- `[UNK]` Whether the Arch-built `/usr/bin/walker` corresponds to this tag —
  out of scope for S078, which claims only the tag file (the note says the same
  and keeps the binary identity `[UNK]`).

GATE | S078 | https://raw.githubusercontent.com/abenz1267/walker/v2.17.2/Cargo.toml | 2026-10-20 | .ufo/waves/round-18/fetch/ReopenS078/cargo-toml.body:21 "notify = \"8.2.0\"" (3 words) | d1676045d1101a2d92c5669e54e36e63363d3e79dbc10c561662039ae2453a90 | agree: independent fetch reproduces the anchor digest (952 B); tag v2.17.2 resolves to a515085f and both wave-1 receipts agree; version and unused-in-src clauses reproduce
