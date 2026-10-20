# Wave 2 falsification — S079 walker tag tarball and S084 docs.rs "latest"

Seat: `MadoR18.RevengeTarballRepro` (leaf; no dispatch). Lane root
`/home/vgpnk/Projects/shokunin/mado-shokunin`; baseline `d9a5a18`, integration
`4c103b55b1ea5c3c555884afe3eb69b5189701b7`, receipts `abfbf35b1ed4d4a1eb294d525ef286be30f3886f`.
Nothing in the lane was edited except my receipt directory and this report; no
VCS write, no package/service/compositor/REA operation. Host pause respected:
only `curl`, byte reads, hashes and `/tmp` work; no tool install performed.
My raw receipts: `.ufo/waves/round-18/fetch/MadoR18.RevengeTarballRepro/receipts.jsonl`
(10 lines, `mado-fetch-receipt-v1`), bodies beside it.

## Verdict

| row | question asked | answer |
|---|---|---|
| S079 | Is the codeload tag tarball byte-reproducible, and is its content the tagged source? | **Yes** to both. Three independent fetches (two seats, 17m40s apart) are byte-identical, sha256 `e50c6060…`; extraction is 76/76 blob-identical to the tagged tree and 7/7 identical to the raw tag files. The *bytes* are a same-generation property of codeload; the durable identity is the commit/tree pair proven below. |
| S084 | Same question for the docs.rs “latest” HTML. | **Yes within one docs.rs deployment** (3/3 fetches today, 18m41s apart, sha256 `0291cfe6…`, and the version-pinned twin 2/2 `adaec7c3…`), **no as a durable pin**: every docs.rs page served during this deployment carries a serve-time deploy stamp `-2026-10-20`, including a page built on 2023-04-25; the next deployment changes the bytes without any xdg release, and `latest` additionally moves on release. The digest is a fetch fingerprint, not a document identity. |

So: the S079 row's `sha256` anchor is sound (with a better content anchor
available and recommended below). The S084 row's `sha256` anchor is a
same-deploy fingerprint; the row's `recheck: on-release` will not notice the
drift that actually changes the bytes.

## Evidence — S079 (`walker` v2.17.2 tarball)

All times UTC. Body names are relative to
`.ufo/waves/round-18/fetch/MadoR18.RevengeTarballRepro/`.

| fetch | url | http | bytes | sha256 | utc |
|---|---|---|---|---|---|
| NoteWalker (other seat) | `…/walker/tar.gz/refs/tags/v2.17.2` | 200 | 165,438 | `e50c606040b24f2a6045292f5f6a08c8a05ac599878ac781b1a5fcf50d353a56` | 2026-10-20T15:42:32Z |
| mine a | same | 200 | 165,438 | same | 2026-10-20T16:00:12Z |
| mine b | same | 200 | 165,438 | same | 2026-10-20T16:00:12Z |
| mine commit-addressed | `…/walker/tar.gz/a515085fd39fae80acc086c8fbfd9b7771a9a11d` | 200 | 165,523 | `1d93050de510dbd3650c3cf17724bdcce2be7fb8c493fbdfd0b5b7a2f5dd6dce` | 2026-10-20T16:06:10Z |

* `cmp NoteWalker/walker-v2.17.2-src.tar.gz …/s079-walker-v2.17.2-a.tar.gz` →
  identical; `cmp a b` → identical.
* Extraction of the tag tarball: **76 files, 16 directories**, one top-level
  directory `walker-2.17.2/`; members are only type `0` (file) and `5` (dir),
  no symlinks; every file mode `100644`.
* Against `NoteWalker/walker-v2.17.2-git-tree.json` (the committed API tree body):
  path sets equal (76/76, 16/16), **0/76 git-blob-sha1 mismatches**. Computed as
  `sha1("blob <len>\0" + bytes)` per member, compared to each `tree[].sha`.
* Against the seven raw tag files the other seat fetched separately
  (`README.md`, `Cargo.toml`, `resources/config.toml`, `src/config.rs`,
  `src/data.rs`, `src/main.rs`, `src/theme/mod.rs`): **7/7 sha256 and byte
  lengths equal**.
* Determinism facts of the served archive: gzip header `1f8b 0800 0000 0000 0003`
  (MTIME 0, OS=3); every tar member has the single mtime
  `2026-10-08T06:45:24Z` (the commit time); every member's PAX `comment` is
  `a515085fd39fae80acc086c8fbfd9b7771a9a11d`.
* Commit binding: fetching `codeload …/tar.gz/a515085fd39fae80acc086c8fbfd9b7771a9a11d`
  returns 200 with top directory `walker-a515085fd39fae80acc086c8fbfd9b7771a9a11d/`
  and the same PAX comment; its 76/76 file contents are byte-identical to the
  tag tarball's. Therefore `a515085f…` is the tag's commit (matching the entry's
  `verified-at` ls-remote line), and the tag-name→commit substitution changes
  only the root-directory name (hence 165,523 vs 165,438 bytes).
* Content tree recomputed canonically from the extracted bytes = root tree
  **`5e3afb6b29cb8a2cab916fa0cfc15784d71a7998`** (independently reproduced with
  `git write-tree` in `/tmp/s079-tree-check`).

Row-claim re-check from the same extracted tree (whole-tree search):
`notify::` → 0 hits; `use notify` → 0; `notify` as a *closure parameter* exists
at `src/niri.rs:160,185` (not the crate). `connect_changed` → exactly
`src/main.rs:142,149` (GSettings `color-scheme`, `accent-color`) and
`src/ui/window.rs:479` (search entry). `set_config` → 0. The four
`AfterAction::{Reload,ClearReload,AsyncReload,AsyncClearReload}` variants are
input re-query actions (`Reload` → `crate::data::input_changed(&query)`,
`src/ui/window.rs:826-829`), not config-file reloads. The row's “no `notify::` /
`use notify`; no config reload entry point” survives; a future re-check must not
mistake the identifier `notify` or the keybind action `Reload` for a hit.

### Anomaly worth recording (not a content mismatch)

`NoteWalker/walker-v2.17.2-git-tree.json` has top-level `sha =
a515085fd39fae80acc086c8fbfd9b7771a9a11d` (the commit, as the commit-addressed
tarball, the PAX comment and the entry's ls-remote line all agree), while its own
`tree[]` array canonically hashes to root tree `5e3afb6b…`. A closure that
compares `json.sha` to a recomputed tree digest will see a mismatch that is not
a content mismatch. The CDN confirms the content; the JSON's label conflates
commit and tree. Mechanism for the label is unresolved (my re-fetch of
`api.github.com` returned 403, unauthenticated rate limit, body kept as
`s079-walker-commit-v2.17.2.json`).

## Evidence — S084 (`docs.rs/xdg/latest/…/BaseDirectories.html`)

| fetch | url | http | bytes | sha256 | utc |
|---|---|---|---|---|---|
| NoteWalker (other seat) | `https://docs.rs/xdg/latest/xdg/struct.BaseDirectories.html` | 200 | 105,537 | `0291cfe6cd80b67fe6e4b276aae8323650d77dbfb88b1f3c9d0ff150b50f9f0d` | 15:41:36Z |
| mine a | same | 200 | 105,537 | same | 16:00:17Z |
| mine b | same | 200 | 105,537 | same | 16:00:17Z |
| mine pinned | `https://docs.rs/xdg/3.0.0/xdg/struct.BaseDirectories.html` | 200 | 105,205 | `adaec7c32cc0595f59c154b407cf5a4ca85c6c40adf269a5046ccdd2b08762f6` | 16:01:30Z |
| mine pinned-b | same | 200 | 105,205 | same | 16:06:30Z |
| mine old version | `https://docs.rs/xdg/2.5.0/xdg/struct.BaseDirectories.html` | 200 | 92,002 | `cb23df33a272208292563216648e26fd47f1bd59c8da222a0ecdd1bce9ba4953` | 16:02:12Z |
| mine crate source | `https://static.crates.io/crates/xdg/xdg-3.0.0.crate` | 200 | 15,821 | `2fb433233f2df9344722454bc7e96465c9d03bff9d77c248f9e7523fe79585b5` | 16:02:39Z |

No per-fetch token found: `grep -oiE 'nonce=|csrf|token=[a-z0-9]+'` → 0 hits.
The two “latest” fetches and the two pinned fetches are byte-identical, and both
agree with the other seat's body fetched ~19 minutes earlier. The instability is
not per-request:

* Each served page carries exactly five deploy-stamped asset URLs of the form
  `/-/static/{vendored.css,rustdoc-2025-08-20.css,font-awesome.css,menu.js,index.js}?0-0-0-81ee18945ca4244c639e84d7a936a8f3ddfe890e-2026-10-20`
  (the five occurrences of `2026-10-20` in the body).
* The same stamp, same date, appears on the **2.5.0 page built 2023-04-25**
  (`data-resource-suffix="-20230425-1.71.0-nightly-458d4dae8"`,
  `data-rustdoc-version="1.71.0-nightly (458d4dae8 2023-04-25)"`). The 2023
  page's stored bytes cannot contain a 2026 stamp, so docs.rs injects the
  current deployment's stamp at serve time. Consequently a digest of any
  docs.rs page is scoped to the deployment that served it, and the deployment
  date is literally the day of the fetch. `[INFERENCE]` a next-day fetch after
  a docs.rs deployment will not reproduce `0291cfe6…`; the observation that the
  stamp equals the fetch date on a 2023 build is the mechanism, the next-day
  delta itself was not observable today.
* `latest` vs `/3.0.0/` differ by 332 bytes, and the difference is only the URL
  alias: the `Permalink` menu item is present on `latest` and absent on the
  pinned page; `/crate/xdg/latest`, `data-url="/crate/xdg/latest/…"`,
  `/crate/xdg/latest/target-redirect/…`, `/crate/xdg/latest/features` become
  `/crate/xdg/3.0.0/…`. After normalising the deploy stamp and the alias path,
  the only residual difference is that `Permalink` menu item; the documented
  text is otherwise identical. When xdg releases a new version, `/latest/`
  will serve different content (at minimum rebuilt links, likely a new
  version), so the digest moves for a second, independent reason.
* The row's claim text is present and correct in this body: `XDG_CONFIG_HOME`
  default `$HOME/.config` at line 302, `XDG_CONFIG_DIRS` default `/etc/xdg` at
  line 306, and `find_config_file` “Searches XDG_CONFIG_HOME and then
  XDG_CONFIG_DIRS” at lines 357-358 (the entry's `[XD:356-358]` pointer is
  accurate; the row's `356-362` range also covers the method block).
* The claim is independently verifiable from content-pinned source, not just
  HTML: `xdg-3.0.0.crate` sha256 `2fb43323…` **equals the `checksum` recorded
  for `xdg 3.0.0` in walker's `Cargo.lock:2705-2708`**; its
  `src/base_directories.rs:446-457` carries the identical doc comment and
  `find_config_file` delegates to `read_file`, which tries `config_home` first
  and then each `config_dirs` (`:757-777`), with the defaults from the page.
  `[INFERENCE, high]` this crate tarball is content-immutable (crates.io
  publishes immutable `.crate` files), so it is a durable tier-A anchor for the
  same claim.

## Divergences / falsified statements

1. **The Gate's stated mechanism for rejecting HTML is wrong as written.**
   `corpus/lessons/round-18.md` §Gate says HTML pages are rejected because
   “per-fetch tokens make the digest irreproducible”. On docs.rs there is no
   per-fetch token and three fetches are byte-identical. The real mechanism is a
   **serve-time deployment stamp** (plus the `latest` alias). The policy
   conclusion (“do not use an HTML digest as a durable pin”) survives; the cited
   cause does not.
   (Out of my rows but visible in the same tool run: `fetch-verify.py` reported
   four `CONFLICT` URLs for `github.com/{basecamp,omacom}/omarchy/tree/v3.8.4/…`
   with five distinct digests for one URL — GitHub tree HTML *is* volatile
   per-fetch. So the Gate sentence is plausible for GitHub HTML, just not for
   this docs.rs page.)
2. **S084 is an HTML page as sole support for the search-order claim**, which
   the round's own Gate rejects (“HTML pages as sole support … Reject or leave
   unrowed”). `corpus/knowledge/walker-route-r18.md:77-79` cites only `[XD:…]`
   for the XDG search order. The anchor is also **line-numbered into a 441-line
   HTML that reflows when docs.rs rebuilds with a new rustdoc** (rustdoc suffix
   `-20261016-1.101.0-nightly-5d8fec066` on this body; the 2.5.0 body's layout
   and suffix are entirely different). A quote anchor survives; line numbers
   and the sha do not.
3. **S084's `recheck: on-release` is the wrong trigger.** docs.rs redeploys
   (and re-stamps every page) without any xdg release; the row will rot between
   releases and a closure re-hashing it will report `BAD_SHA` against a page
   whose text is unchanged.
4. **The tree JSON's `sha` field is the commit, not the tree** (see S079
   anomaly). The entry's `verified-at` line and the row's tar anchor remain
   correct; only the JSON label is misleading.
5. **S079 is not falsified.** It is byte-reproducible today and its content is
   exactly the tag; the only caveat is that codeload's bytes are a generated
   artifact (generator/compression could change while the tree stays the same).
   The tree/commit digests are the generator-independent identity.

## Recommendations (tier / kind / retention)

**S079 — keep: tier A, kind `code`, recheck `on-release`.** Tag content is
immutable; `on-release` cannot fire for v2.17.2 (it is already released) and
that is the correct terminal state. Keep the body committed (165 KB; the row's
method is whole-tree search). Strengthen the anchor cell with the
generator-independent identity already established:

```
tarball 165,438 B sha256 e50c6060…; PAX comment and codeload commit-tar bind
commit a515085fd39fae80acc086c8fbfd9b7771a9a11d; root tree
5e3afb6b29cb8a2cab916fa0cfc15784d71a7998; 76/76 git blob ids equal the
tagged tree (raw tag files agree)
```

so a later codeload byte change cannot be mistaken for a source change, and a
tree change cannot hide behind the same tag name.

**S084 — demote: tier `B`, kind stays `docs`, recheck `90d`; repin the URL and
replace the sole-support anchor with a code row.** Concretely:

* `S084` keeps `kind=docs`, `tier A → B` (corroboration only, per the round's
  own Gate), `recheck: on-release → 90d`, URL
  `https://docs.rs/xdg/3.0.0/xdg/struct.BaseDirectories.html` (drop `latest`),
  and its anchor becomes the verbatim text
  “Searches `XDG_CONFIG_HOME` and then `XDG_CONFIG_DIRS`” plus the two defaults,
  with the note that **any `sha256` recorded for a docs.rs body is valid only
  for the docs.rs deployment that served it** (stamp `-2026-10-20` on this
  fetch). Do not re-anchor by line numbers.
* Add **S096 — kind `code`, tier A, recheck `on-release`**:
  `https://static.crates.io/crates/xdg/xdg-3.0.0.crate`, 15,821 B, sha256
  `2fb433233f2df9344722454bc7e96465c9d03bff9d77c248f9e7523fe79585b5` (= the
  `xdg 3.0.0` `checksum` in walker `Cargo.lock`), anchor
  `src/base_directories.rs:446-457` + `:757-777`, teaches the same search order
  from the crate that walker locks. Update the entry's `[XD:…]` citation for the
  search-order sentence to the source row; keep `[XD:…]` only as documentation
  corroboration.
* P3 credit is unaffected: `walker-route-r18.md` also cites tier-A rows
  S072-S083 and S085-S089, so demoting S084 alone does not drop the province
  under rubric V. If L1 declines a new row id, the minimum acceptable fix is
  tier A kept **only** with the quote anchor + `90d` and an explicit
  “deploy-scoped digest” note; the digest must not be presented as a durable
  pin either way.

## Commands run (verbatim; key output abridged)

```text
curl -sSL --max-time 60 -o s079-walker-v2.17.2-a.tar.gz \
  -w '%{http_code} %{url_effective}' \
  https://codeload.github.com/abenz1267/walker/tar.gz/refs/tags/v2.17.2
200 https://codeload.github.com/abenz1267/walker/tar.gz/refs/tags/v2.17.2
# (b: same command, same output; sha256sum a b =>
e50c606040b24f2a6045292f5f6a08c8a05ac599878ac781b1a5fcf50d353a56  a
e50c606040b24f2a6045292f5f6a08c8a05ac599878ac781b1a5fcf50d353a56  b)

tar -xzf s079-walker-v2.17.2-a.tar.gz -C /tmp/s079-extract
# 76 files / 16 dirs; all modes 100644; single mtime 2026-10-08T06:45:24Z
python3 … # blob sha1 per member vs walker-v2.17.2-git-tree.json
tar files: 76 tree blobs: 76
only_in_tar: [] only_in_tree: [] path_sets_equal: True
dir sets equal: True tar dirs: 16 tree dirs: 16 diff: []
blob-sha mismatches: 0 []
# 7/7 raw-file sha256 comparisons MATCH (README, Cargo.toml,
# resources/config.toml, src/config.rs, src/data.rs, src/main.rs,
# src/theme/mod.rs)

cd /tmp/s079-tree-check && git init -q . && cp -a /tmp/s079-extract/walker-2.17.2/. . \
  && git add -A && git write-tree
5e3afb6b29cb8a2cab916fa0cfc15784d71a7998

curl -sSL --max-time 60 -o s079-walker-commit-a515085f.tar.gz -w '%{http_code} %{url_effective}' \
  https://codeload.github.com/abenz1267/walker/tar.gz/a515085fd39fae80acc086c8fbfd9b7771a9a11d
200 https://codeload.github.com/abenz1267/walker/tar.gz/a515085fd39fae80acc086c8fbfd9b7771a9a11d
165523 B 1d93050de510dbd3650c3cf17724bdcce2be7fb8c493fbdfd0b5b7a2f5dd6dce
# top dir walker-a515085fd39fae80acc086c8fbfd9b7771a9a11d/; PAX comment a515085f…;
# file sets equal True 76 76; content sha mismatches: []
# (tag tar 165438 B is the same tree with top dir walker-2.17.2/)

grep -rn --include='*.rs' -E 'notify|inotify|watch|reload|set_config' /tmp/s079-extract/walker-2.17.2
./src/main.rs:835: niri::watch_empty_workspace_focuses(
./src/niri.rs:160/185/213: closure parameter `notify` (not the crate)
# no notify::, no use notify, no set_config
grep -rn 'connect_changed' src/
src/main.rs:142 color-scheme; src/main.rs:149 accent-color;
src/ui/window.rs:479 input  # search entry
grep -rn 'Reload' src/keybinds.rs src/ui/window.rs
AfterAction::Reload => crate::data::input_changed(&query)   # data requery

curl … https://docs.rs/xdg/latest/xdg/struct.BaseDirectories.html     # a,b
200 https://docs.rs/xdg/latest/xdg/struct.BaseDirectories.html  # 105537 B
0291cfe6cd80b67fe6e4b276aae8323650d77dbfb88b1f3c9d0ff150b50f9f0d  (a and b; cmp identical)
curl … https://docs.rs/xdg/3.0.0/xdg/struct.BaseDirectories.html       # pinned, pinned-b
200 … 105205 B adaec7c32cc0595f59c154b407cf5a4ca85c6c40adf269a5046ccdd2b08762f6 (both)
curl … https://docs.rs/xdg/2.5.0/xdg/struct.BaseDirectories.html
200 … 92002 B cb23df33a272208292563216648e26fd47f1bd59c8da222a0ecdd1bce9ba4953
  data-resource-suffix="-20230425-1.71.0-nightly-458d4dae8"
  /-/static/menu.js?0-0-0-81ee18945ca4244c639e84d7a936a8f3ddfe890e-2026-10-20
  /-/static/index.js?0-0-0-81ee18945ca4244c639e84d7a936a8f3ddfe890e-2026-10-20
curl … https://static.crates.io/crates/xdg/xdg-3.0.0.crate
200 … 15821 B 2fb433233f2df9344722454bc7e96465c9d03bff9d77c248f9e7523fe79585b5
  == Cargo.lock:2708 checksum for xdg 3.0.0

python3 .ufo/waves/round-18/fetch-verify.py --sources corpus/SOURCES.md \
  --rows S079,S084 --quote 'S084=Searches <code>XDG_CONFIG_HOME</code> and then'
FETCH MadoR18.RevengeTarballRepro/<10 bodies> ok
ROW S079 receipted
ROW S084 receipted
QUOTE S084 ok
```

The check that ties the S084 digest to the claim is also visible in my pinned
copy: `sed -n '302p;306p;357,358p'` gives the two defaults and the “Searches”
sentence, matching `[XD:302]`, `[XD:306]`, `[XD:356-358]`.

## Limits and confidence

* Same-day evidence only. Byte stability of S079 and of docs.rs-within-deploy is
  **observed**; across-deploy drift of docs.rs is **inferred** from a 2023 page
  carrying today's serve-time stamp, not observed across two days. High
  confidence in the mechanism, since the mixed stamps are direct evidence.
* `api.github.com` returned 403 (unauthenticated rate limit, body receipted);
  no auth/cookies were used, and the commit binding was instead established via
  codeload's commit-addressed tar. The cause of the tree JSON's `sha` label is
  unresolved; content identity is resolved independently at 76/76 blobs.
* No host binary or running service was read; S079/S084 remain documentary
  evidence, exactly as the wave-1 Gate scopes them. No package, service,
  compositor, input or REA operation occurred.
