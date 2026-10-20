# SrcS084 — S098 row (xdg crate source) and the S084 status note (round 19)

Draft only. L1 assigns the id (reserved `S098`), merges the row into
`corpus/SOURCES.md`, and logs the status change in `corpus/lessons/round-19.md`.
Everything below was opened 2026-10-20; receipts are three lines in
`.ufo/waves/round-19/fetch/SrcS084/receipts.jsonl`.

## What was opened (observed)

- `https://raw.githubusercontent.com/abenz1267/walker/v2.17.2/Cargo.lock` — 200,
  70,247 B, sha256 `3448367c28c769e29f681ea2de84d4a822f08569bbef6628f03535c61fec2315`;
  `name = "xdg"` block at lines 2705-2708: version `3.0.0`,
  checksum `2fb433233f2df9344722454bc7e96465c9d03bff9d77c248f9e7523fe79585b5`.
- `https://static.crates.io/crates/xdg/xdg-3.0.0.crate` — 200, 15,821 B,
  sha256 `2fb433233f2df9344722454bc7e96465c9d03bff9d77c248f9e7523fe79585b5`,
  byte-for-byte the lock's checksum (below 1 MiB; body kept). Extracted with
  `tar -xzf xdg-3.0.0.crate -C /tmp/srcs084`; crate `Cargo.toml` says
  `name = "xdg"`, `version = "3.0.0"`; `.cargo_vcs_info.json` pins upstream
  sha1 `c0f6bc329b0fd92b015a55bcbbee72b2864fae4b`.
- `https://raw.githubusercontent.com/abenz1267/walker/v2.17.2/src/config.rs` — 200,
  sha256 `93b6bd6f360312dc0dcd70cd939a14e673431ee89b95608084253069aaad1469`;
  line 219 is the call `xdg::BaseDirectories::with_prefix("walker").find_config_file("config.toml")`.
- Tag resolution (not a fetch receipt):
  `git ls-remote https://github.com/abenz1267/walker refs/tags/v2.17.2 'refs/tags/v2.17.2^{}'`
  → `a515085fd39fae80acc086c8fbfd9b7771a9a11d  refs/tags/v2.17.2` (lightweight; no
  peeled line).

Search order, read in the extracted source (`xdg-3.0.0/src/base_directories.rs`):

- doc of `find_config_file` at `:446-448` — "…Searches `XDG_CONFIG_HOME` and then `XDG_CONFIG_DIRS`.";
- impl at `:449-457` passes `config_home` first, then `config_dirs`, to `read_file`;
- defaults at `:308-310` (`XDG_CONFIG_HOME` absent → `$HOME/.config`) and `:321-323`
  (`XDG_CONFIG_DIRS` absent → `/etc/xdg`);
- `read_file` at `:757-777` returns the user-prefix hit first (`:764-769`), then walks
  the shared dirs in order (`:770-775`) — the code that makes the doc's "then" true.

## Row (11 columns, reserved id S098)

| id | source | kind | tier | scope | anchor | teaches | status | opened | recheck | used-by |
|---|---|---|---|---|---|---|---|---|---|---|
| S098 | xdg crate source tarball @ 3.0.0 — https://static.crates.io/crates/xdg/xdg-3.0.0.crate | code | A | XDG config search order as walker v2.17.2's lock resolves it: `find_config_file` checks `$XDG_CONFIG_HOME` then each `$XDG_CONFIG_DIRS` entry | walker v2.17.2 Cargo.lock:2705-2708 (xdg 3.0.0, checksum 2fb433233f2df9344722454bc7e96465c9d03bff9d77c248f9e7523fe79585b5; tag a515085fd39fae80acc086c8fbfd9b7771a9a11d); crate 15,821 B sha256 2fb433233f2df9344722454bc7e96465c9d03bff9d77c248f9e7523fe79585b5 (equals lock checksum); extracted src/base_directories.rs:446-457, :308-310, :321-323, :757-777; call at walker src/config.rs:219 (sha256 93b6bd6f360312dc0dcd70cd939a14e673431ee89b95608084253069aaad1469) | supersedes S084 — walker calls `xdg::BaseDirectories::with_prefix("walker").find_config_file("config.toml")`; the crate checks `$XDG_CONFIG_HOME` (default `~/.config`) first, then each `$XDG_CONFIG_DIRS` entry (default `/etc/xdg`) | mined | 2026-10-20 | on-release | corpus/knowledge/walker-route-r18.md |

## Gate line for the round lesson (rule 1: URL, access date, ≤25-word quote, location, digest)

| GATE | S098 | https://static.crates.io/crates/xdg/xdg-3.0.0.crate | 2026-10-20 | .ufo/waves/round-19/fetch/SrcS084/xdg-3.0.0.crate → `src/base_directories.rs:446-448` "Given a relative path `path`, returns an absolute path to an existing configuration file, or `None`. Searches `XDG_CONFIG_HOME` and then `XDG_CONFIG_DIRS`." (21 words) | 2fb433233f2df9344722454bc7e96465c9d03bff9d77c248f9e7523fe79585b5 | agree: tag v2.17.2 resolves to lightweight a515085f; the receipted lock pins xdg 3.0.0 with this checksum and the receipted crate body reproduces it byte-for-byte; the cited doc, defaults and `read_file` order are present in the extracted source |

The quote's location is inside the receipted body (`.crate` is a gzip tar); reproduce with
`tar -xzf xdg-3.0.0.crate src/base_directories.rs -O | nl -ba | sed -n '446,448p'`.
A second quotable anchor, if L1 wants one for the call site: `walker-v2.17.2-src-config.rs:219`
"`xdg::BaseDirectories::with_prefix(\"walker\").find_config_file(\"config.toml\")`" (1 word
as written; body sha256 `93b6bd6f…`).

## S084 status note (R18-V4) — proposed in-place change

Current row, `corpus/SOURCES.md:96`:

- source `https://docs.rs/xdg/latest/xdg/struct.BaseDirectories.html` (kind `docs`, tier A);
- anchor `saved HTML lines 302, 306, 356-362; sha256 0291cfe6cd80b67fe6e4b276aae8323650d77dbfb88b1f3c9d0ff150b50f9f0d`;
- status `mined`, used-by `corpus/knowledge/walker-route-r18.md`.

Proposed in-place change (rule 2 permits `status`, `recheck`, `used-by` only):

- `status`: `mined` → `rejected`.
- `used-by`: `corpus/knowledge/walker-route-r18.md` → `—`, in the same merge that moves the
  note's support token to S098 (next section).
- `recheck`: unchanged (`on-release`).
- `teaches`: unchanged (rule 2 forbids editing it; precedent: rejected S030 keeps a positive
  `teaches`). The rejection reason and flip live in the lesson's Gate log.

Reason: the `source` token is the docs.rs `latest` alias — not a revision — and the `anchor`
records a digest of an HTML page, which round-18 M7 (`corpus/lessons/round-18.md:22`) rules
out as a digest anchor because bytes vary per fetch. The taught fact is not wrong: today
`latest` serves xdg 3.0.0 (the round-18 saved body names `xdg-3.0.0` three times and
`xdg/3.0.0` once at `.ufo/waves/round-18/fetch/ReopenS084/xdg-basedirectories-latest.html`),
and its lines 356-358 carry the same wording as the crate doc. The defect is durability, so
the durable support is S098 at a version-pinned digest.

Lesson Gate log line (old → new, for `corpus/lessons/round-19.md`):

```
- S084 status mined → rejected (R18-V4): anchor is the docs.rs `latest` alias plus an HTML
  digest that is not a revision-bound anchor (M7); S098 supersedes it at the xdg 3.0.0 crate
  digest. flip: a docs.rs URL pinned to one release whose saved bytes reproduce per fetch.
```

Alternative, if L1 prefers the conservative reading: leave S084 `mined` and only move the
note's citation to S098. Cost: the registry still lists an alias-anchored row as `mined`,
so R18-V4 is only cosmetically closed. `rejected` is the status vocabulary's only terminal
value (queued · mined · rejected), so it is the honest disposition.

## Proposed note edit (L1-owned file; not written by this seat)

`corpus/knowledge/walker-route-r18.md:1` holds the token

```
S084 https://docs.rs/xdg/latest/xdg/struct.BaseDirectories.html (find_config_file, find_config_files, XDG defaults)
```

Replace with

```
S098 https://static.crates.io/crates/xdg/xdg-3.0.0.crate (crate source: find_config_file, XDG defaults)
```

No other S084 mention exists in `corpus/knowledge/` (single `grep -rn 'S084' corpus/knowledge/`
hit, line 1).

## Limits

- I did not edit `corpus/SOURCES.md`, the note, or any L1-owned file; ids/merge are L1's.
- The crate extraction under `/tmp/srcs084` is scratch; the reproducible object is the
  receipted `.crate` body.
- docs.rs was not re-fetched this round: the "latest = 3.0.0" observation is the round-18
  receipted body, not a round-19 fetch.
- No walker binary, service or host package state was touched or read; this is source bytes
  and crate bytes only.
