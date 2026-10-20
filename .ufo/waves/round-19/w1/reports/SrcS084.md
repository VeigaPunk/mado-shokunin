# SrcS084 — xdg 3.0.0 is pinned twice: lock checksum equals the receipted crate; S084 has a durable replacement (S098 drafted)

Question: replace S084's docs.rs `latest` support with a revision-bound xdg crate row.
Verdict: the pin is closed end to end — walker v2.17.2 locks xdg 3.0.0, the lock checksum
is the sha256 of the `.crate` body this seat fetched, and the crate source carries the
search-order doc/code at file:line. Draft delivered; S084 status change recommended.

## Findings (observed)

### 1. walker v2.17.2 locks xdg 3.0.0 with a checksum

`curl -sSL --max-time 60 -o walker-v2.17.2-Cargo.lock -w '%{http_code} %{url_effective}' https://raw.githubusercontent.com/abenz1267/walker/v2.17.2/Cargo.lock`
→ `200 https://raw.githubusercontent.com/abenz1267/walker/v2.17.2/Cargo.lock`; 70,247 B;
sha256 `3448367c28c769e29f681ea2de84d4a822f08569bbef6628f03535c61fec2315`.

```
2705	name = "xdg"
2706	version = "3.0.0"
2707	source = "registry+https://github.com/rust-lang/crates.io-index"
2708	checksum = "2fb433233f2df9344722454bc7e96465c9d03bff9d77c248f9e7523fe79585b5"
```

(`nl -ba .ufo/waves/round-19/fetch/SrcS084/walker-v2.17.2-Cargo.lock | sed -n '2703,2709p'`.)
Tag resolution: `git ls-remote https://github.com/abenz1267/walker refs/tags/v2.17.2 'refs/tags/v2.17.2^{}'`
→ `a515085fd39fae80acc086c8fbfd9b7771a9a11d  refs/tags/v2.17.2`, no peeled line (lightweight).
This is a `ls-remote` output, not a fetch receipt.

### 2. The crate body's sha256 equals the lock checksum

`curl -sSL --max-time 60 -o xdg-3.0.0.crate -w '%{http_code} %{url_effective}' https://static.crates.io/crates/xdg/xdg-3.0.0.crate`
→ `200`; 15,821 B (well under 1 MiB, body kept); sha256
`2fb433233f2df9344722454bc7e96465c9d03bff9d77c248f9e7523fe79585b5` — identical to
Cargo.lock:2708. Extracted: `tar -xzf xdg-3.0.0.crate -C /tmp/srcs084`; crate `Cargo.toml`
has `name = "xdg"` / `version = "3.0.0"`; `.cargo_vcs_info.json` adds upstream sha1
`c0f6bc329b0fd92b015a55bcbbee72b2864fae4b`.

### 3. Search order, doc and code, in the extracted source

`/tmp/srcs084/xdg-3.0.0/src/base_directories.rs` (sha256 `335a4a3001057c1c97a7c4eae86c9b3f1210c5492dbe42dca0599bc698e47570`):

```
446	    /// Given a relative path `path`, returns an absolute path to an existing
447	    /// configuration file, or `None`. Searches `XDG_CONFIG_HOME` and then
448	    /// `XDG_CONFIG_DIRS`.
449	    pub fn find_config_file<P: AsRef<Path>>(&self, path: P) -> Option<PathBuf> {
450	        read_file(
451	            self.config_home.as_deref(),
452	            &self.config_dirs,
...
757	fn read_file(
764	    if let Some(home) = home {
765	        let full_path = home.join(user_prefix).join(path);
...
770	    for dir in dirs.iter() {
```

Defaults: `:308-310` `let config_home = env_var("XDG_CONFIG_HOME") … .join(".config")`;
`:321-323` `let config_dirs = env_var("XDG_CONFIG_DIRS") … vec![PathBuf::from("/etc/xdg")]`.
So the claim S084 teaches is true for this crate: `$XDG_CONFIG_HOME` (default `~/.config`)
first, then each `$XDG_CONFIG_DIRS` entry (default `/etc/xdg`), implemented by `read_file`
returning the home hit before iterating dirs.

Quote (21 words, ≤25): "Given a relative path `path`, returns an absolute path to an
existing configuration file, or `None`. Searches `XDG_CONFIG_HOME` and then
`XDG_CONFIG_DIRS`." Location `xdg-3.0.0.crate → src/base_directories.rs:446-448`;
reproduced after this write with
`tar -xzf xdg-3.0.0.crate -O xdg-3.0.0/src/base_directories.rs | nl -ba | sed -n '446,448p'`
(verbatim).

### 4. walker really calls it

`https://raw.githubusercontent.com/abenz1267/walker/v2.17.2/src/config.rs` → 200, sha256
`93b6bd6f360312dc0dcd70cd939a14e673431ee89b95608084253069aaad1469` (matches the round-18
S074 anchor). Lines 218-219:

```
218	        if let Some(user_config_path) =
219	            xdg::BaseDirectories::with_prefix("walker").find_config_file("config.toml")
```

So the crate row is support for walker's own user-config lookup, not a generic XDG fact.

### 5. S084 disposition (recommendation; L1 decides)

Row at `corpus/SOURCES.md:96` is `kind docs, tier A, status mined`, source
`https://docs.rs/xdg/latest/xdg/struct.BaseDirectories.html`, anchor "saved HTML lines 302,
306, 356-362; sha256 0291cfe6…". This round's round-18 receipted body (not re-fetched now)
shows `latest` served xdg 3.0.0: `xdg-3.0.0` appears 3× and `xdg/3.0.0` 1× in
`.ufo/waves/round-18/fetch/ReopenS084/xdg-basedirectories-latest.html`, and its lines
356-358 carry the same wording as the crate doc. The fact is true today; the anchor is not
durable (`latest` is not a revision; HTML digests are excluded by round-18 M7 at
`corpus/lessons/round-18.md:22`).

Recommended in-place change (rule 2 allows only status/recheck/used-by): `status
mined → rejected`, `used-by → —` in the same merge that swaps the note token, recheck
unchanged. Reason and flip are drafted as a lesson Gate old→new line. Alternative (leave
`mined`, cite S098 from the note) leaves an alias-anchored row `mined`, so it only
cosmetically closes R18-V4. Rejection with a positive `teaches` has precedent (S030 at
`corpus/SOURCES.md:42`), because rule 2 forbids rewriting `teaches`.

### 6. Deliverable

`.ufo/waves/round-19/drafts/SrcS084-row.md` — S098 row (11 columns; `awk -F'|'` → NF=13,
teaches opens `supersedes S084 — `), the lesson Gate line with URL/date/quote/digest, the
S084 status note, and the exact one-line note-token replacement
(`corpus/knowledge/walker-route-r18.md:1`, the only S084 mention under `corpus/knowledge/`).
Receipts: `.ufo/waves/round-19/fetch/SrcS084/receipts.jsonl` — 3 lines, each
`mado-fetch-receipt-v1` with `curl 8.23.0` tool string, HTTP 200, bytes, sha256.

## Limits

- docs.rs was not re-fetched this round; "latest = 3.0.0" rests on the round-18 receipted
  body, not a round-19 fetch.
- No L1-owned file was edited: `corpus/SOURCES.md`, `corpus/knowledge/walker-route-r18.md`
  and the round lesson are untouched; the id and merge are L1's.
- The `/tmp/srcs084` extraction is scratch; the reproducible object is the receipted
  `.crate` body.
- No host package/binary/service state was read or run; source and crate bytes only.
- The gate line's quote location is inside a gzip tar member, so "body path:line" means
  crate body → member path:line, not a line of the compressed body.

## Installs

none
