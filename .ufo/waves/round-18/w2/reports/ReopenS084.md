# S084 reopen — xdg crate BaseDirectories docs (non-author check, R17-V3/M6)

Seat `MadoR18.ReopenS084`. Wave 2 (falsify). Row read at lane commit
`4c103b55b1ea5c3c555884afe3eb69b5189701b7` (`corpus/SOURCES.md:96`). No lane
writes outside `.ufo/waves/round-18/fetch/ReopenS084/` and this report; no
package, service, compositor, input, socket-to-host or REA tool used.

Row under test:

| id | source | kind | tier | scope | anchor | teaches |
|---|---|---|---|---|---|---|
| S084 | https://docs.rs/xdg/latest/xdg/struct.BaseDirectories.html | docs | A | XDG search order used by walker's find_config_file (the crate walker calls) | saved HTML lines 302, 306, 356-362; sha256 0291cfe6… | find_config_file searches XDG_CONFIG_HOME then XDG_CONFIG_DIRS; defaults ~/.config and /etc/xdg |

## Commands run and their output

```
$ curl -sSL --max-time 60 -o ReopenS084/xdg-basedirectories-latest.html \
    -w '%{http_code} %{url_effective}\n' \
    https://docs.rs/xdg/latest/xdg/struct.BaseDirectories.html
200 https://docs.rs/xdg/latest/xdg/struct.BaseDirectories.html
$ sha256sum ReopenS084/xdg-basedirectories-latest.html; wc -lc …
0291cfe6cd80b67fe6e4b276aae8323650d77dbfb88b1f3c9d0ff150b50f9f0d   441 105537

$ curl … https://docs.rs/xdg/3.0.0/xdg/struct.BaseDirectories.html
200 https://docs.rs/xdg/3.0.0/xdg/struct.BaseDirectories.html
adaec7c32cc0595f59c154b407cf5a4ca85c6c40adf269a5046ccdd2b08762f6   438 105205

$ grep -n 'assumed to be <code>\$HOME/.config\|assumed to be <code>/etc/xdg\|Searches <code>XDG_CONFIG_HOME' \
    fetch/NoteWalker/xdg-crate-basedirectories.html
302:<li><code>XDG_CONFIG_HOME</code>; if not set: assumed to be <code>$HOME/.config</code>.</li>
306:<li><code>XDG_CONFIG_DIRS</code>; if not set: assumed to be <code>/etc/xdg</code>.</li>
357:configuration file, or <code>None</code>. Searches <code>XDG_CONFIG_HOME</code> and then
358:<code>XDG_CONFIG_DIRS</code>.</p>

$ git ls-remote --tags https://github.com/whitequark/rust-xdg | tail -1
66378cb76e1c7b948597dba7bdb081302169c53d    refs/tags/v2.5.2
$ git ls-remote https://github.com/whitequark/rust-xdg | head -2
c0f6bc329b0fd92b015a55bcbbee72b2864fae4b    HEAD
c0f6bc329b0fd92b015a55bcbbee72b2864fae4b    refs/heads/main

$ cat xdg-3.0.0/.cargo_vcs_info.json          # crate tarball already in lane
{"git": {"sha1": "c0f6bc329b0fd92b015a55bcbbee72b2864fae4b"}, "path_in_vcs": ""}
$ sha256sum fetch/SrcWalkerConfigPaths/xdg-3.0.0.crate
2fb433233f2df9344722454bc7e96465c9d03bff9d77c248f9e7523fe79585b5

$ grep -n 'xdg' fetch/NoteWalker/walker-v2.17.2-cargo.toml
30:xdg = "3.0.0"
$ grep -n -A3 'name = "xdg"' fetch/MadoR18.SrcWalkerThemes/cargo-lock.txt
2705:name = "xdg" / 2706-version = "3.0.0" / 2708-checksum = "2fb433233f2df9344722454bc7e96465c9d03bff9d77c248f9e7523fe79585b5"

$ grep -n 'BaseDirectories' fetch/MadoR18.SrcWalkerThemes/src-config.rs
219:            xdg::BaseDirectories::with_prefix("walker").find_config_file("config.toml")

$ sed -n '446,448p;757,776p' /tmp/xdg-crate-S084/xdg-3.0.0/src/base_directories.rs
/// Given a relative path `path`, returns an absolute path to an existing
/// configuration file, or `None`. Searches `XDG_CONFIG_HOME` and then
/// `XDG_CONFIG_DIRS`.
fn read_file(home, dirs, user_prefix, shared_prefix, path) -> Option<PathBuf> {
    if let Some(home) = home { … if path_exists(&full_path) { return Some(full_path); } }
    for dir in dirs.iter() { … if path_exists(&full_path) { return Some(full_path); } }
```

Receipts: `.ufo/waves/round-18/fetch/ReopenS084/receipts.jsonl`, two
`mado-fetch-receipt-v1` lines (latest 16:00:36Z / 3.0.0 16:03:01Z).
Cross-seat agreement, same URL `…/latest/…`: `NoteWalker` 15:41:36Z,
`ReviewWalkerUpstream` 16:00:36Z, and mine — all 105,537 B and
`0291cfe6cd80b67fe6e4b276aae8323650d77dbfb88b1f3c9d0ff150b50f9f0d`.
Same page at `…/3.0.0/…`: `MadoR18.SrcWalkerThemes` 15:41:24Z and mine —
both `adaec7c3…`/105,205 B. **3/3 and 2/2 agree; no disagreement anywhere.**

## Observed (facts)

1. Row anchor sha256 reproduces exactly from a non-author fetch, and from two
   wave-1 seats. Bytes are stable across all three fetches (no per-fetch
   nonce observed — the round's gate reason "per-fetch tokens" does not hold
   for this page).
2. Line anchors 302 and 306 land exactly on the `$HOME/.config` and
   `/etc/xdg` default statements in the body whose sha the row names; 356-362
   spans the `find_config_file` + `find_config_files` blocks, with the
   sentence at 357-358.
3. The `/3.0.0/` body differs from `/latest/` only in docs.rs nav chrome
   (`diff` after normalising `3.0.0`: 8 hunks, all `/xdg/latest` vs
   `/xdg/3.0.0` links) — same prose, but shifted by 3 lines (299/303/354-359).
4. The URL is **not tag-pinned**: it is the `latest` alias. There is no
   `v3.0.0` tag in `whitequark/rust-xdg` (highest is `v2.5.2`); the 3.0.0
   crate was published from `main` = `c0f6bc3…`, per its own
   `.cargo_vcs_info.json`. So no tag exists to pin to; the pinning artefact
   is the crate version + crates.io checksum.
5. The page embeds a docs.rs deploy stamp:
   `vendored.css?0-0-0-81ee1894…-2026-10-20`, identical in all 11 docs.rs
   HTML bodies in the lane's fetch tree (other crates too), so the digest is
   scoped to the current docs.rs deploy, not durable across days.
6. `teaches` is grounded, and stronger than the docs alone: the crate doc
   comment at `base_directories.rs:446-448` is verbatim what the page renders,
   `read_file()` returns the user-prefix hit before iterating `config_dirs`
   (first hit wins), and the constructor defaults `config_home` to
   `$HOME/.config` and `config_dirs` to `["/etc/xdg"]`.
7. The scope's parenthetical is true: walker v2.17.2 names `xdg = "3.0.0"`
   (`Cargo.toml:30`), locks `xdg 3.0.0` with checksum `2fb4332…`, and calls
   `xdg::BaseDirectories::with_prefix("walker").find_config_file("config.toml")`
   (`src/config.rs:219`). The lane's own crate tarball hashes to that
   lock checksum.
8. The citing note uses the row truthfully: it quotes the search sentence
   verbatim (`walker-route-r18.md:76-80`), attributes it as documentation
   ("The crate documents the search as…"), marks first-hit-wins as `INF from
   that search order`, and lists the unvaried-environment question as `[UNK]`
   (`:291-292`). It is one of 20 `sources_ok` for P3 at the integration
   commit — P3 does not depend on it (S072-S079 are tag-pinned rows).

## Inferred

- Tier A is defensible for this scope: rustdoc generated from the exact crate
  version walker pins, whose prose is the crate author's doc comment and whose
  implementation matches. Docs.rs is a build service, but the content is
  primary and the version is fixed by walker's lock.
- The row's weak cell is `source`/`anchor`, not `teaches`: a moving `latest`
  alias plus a deploy-dated HTML digest. It will not re-derive on a later day
  or after a crate release, which matters under `recheck: on-release`.
- The note's `[XD:356-358]` includes one line before the sentence (356 is the
  method header); the quote itself sits wholly at 357-358 and is verbatim, so
  this is cosmetic, not a truthfulness defect.

## Findings for L1 (routed, not applied)

- **F1 (medium, reproducibility).** Re-point S084's `source`/`anchor` to a
  content-addressed artefact: the crate tarball
  `https://static.crates.io/crates/xdg/xdg-3.0.0.crate` (sha256 `2fb4332…`,
  byte-equal to walker's lock checksum; receipt already in
  `fetch/SrcWalkerConfigPaths/`), with `src/base_directories.rs:446-448,
  757-776` as the anchor — or at minimum the `/xdg/3.0.0/` URL, keeping the
  HTML digest as deploy-scoped. The current `latest` alias has no tag to pin
  to and its sha256 expires with the docs.rs deploy.
- **F2 (low, disclosure).** Record in the round-18 gate that "per-fetch
  tokens" was not the reason to distrust this page (three fetches, byte
  equal); the real reason is the deploy-dated stamp and the moving alias.
- **F3 (low).** If the source cell keeps an HTML anchor, say which body the
  line numbers belong to: 302/306/356-362 are the `/latest/` body; the
  `/3.0.0/` body is 299/303/354-359.

## Remaining unknowns

- `[UNK]` Whether docs.rs re-serves this exact body on a later UTC day; the
  `-2026-10-20` stamp implies drift but no cross-day fetch exists.
- `[UNK]` Nothing here observes walker running, or whether the host ever takes
  the `/etc/xdg` branch; that stays the note's own `[UNK]`.

GATE | S084 | https://docs.rs/xdg/latest/xdg/struct.BaseDirectories.html | 2026-10-20 | .ufo/waves/round-18/fetch/ReopenS084/xdg-basedirectories-latest.html:302 | "<li><code>XDG_CONFIG_HOME</code>; if not set: assumed to be <code>$HOME/.config</code>.</li>" (8 words) | 0291cfe6cd80b67fe6e4b276aae8323650d77dbfb88b1f3c9d0ff150b50f9f0d | agree: anchor sha reproduces 3/3 fetches and lines 302/306/357-358 are verbatim; teaches and the note's INF-marked use are true, but the URL is an unpinned `latest` alias (no v3.0.0 tag exists) over a deploy-dated page, so re-point to the crate tarball 2fb4332… for durability
