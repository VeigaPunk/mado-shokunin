# ReviewSourcesRows — round 18 wave 2 (FALSIFY)

Scope: `corpus/SOURCES.md` rows S072–S095 as data at
`4c103b55b1ea5c3c555884afe3eb69b5189701b7` (worktree bytes equal the commit:
`sha256 9552071c0b286075ffabb3a7ea1373e8dbaef5e6c37f906d2620ae83454f26de`).
Lane root /home/vgpnk/Projects/shokunin/mado-shokunin. No lane write beyond
this report and my seat's fetch receipts; no package/service/compositor
operation; no `git status`.

Claim under attack: C2 "each new credited row backed by a committed raw fetch
receipt … so a closure can tell a fetched row from an invented one", and the
wave-1 Gate's own admission rule at `corpus/lessons/round-18.md:31-33`:

> Admit: tag-pinned raw files whose receipts agree across seats; host file
> bytes as host rows. Reject or leave unrowed: HTML pages as sole support
> (per-fetch tokens make the digest irreproducible), unversioned docs sites as
> version-specific support, third-party blogs.

## Verdict

Row data is well-formed and honestly measured: 24/24 rows have 11 cells, valid
kind/tier/status enums, `opened 2026-10-20`, valid recheck cadence, exact
`used-by` paths, and the rubric-V T4 surface keyword in source+scope. The
committed receipts join every non-host anchor digest, and no fetched URL ever
returned two different digests across seats (301 receipts, 245 URLs, 0
conflicts). Census validate exits 0 with only the three historical W04.

Two admitted rows contradict the Gate the same round declared:
**S084** is an unversioned `docs.rs/latest` page carrying no revision, and
**S094**'s two tree-listing digests are HTML with per-fetch nonces — I refetched
both and reproduced neither. Neither defect moves C2: P3 is carried by
tag-pinned rows S072–S083 and P5 by S092/S093, so coverage does not depend on
the two weak anchors. **S079 is reproducible** (four committed receipts plus my
fifth fetch agree byte-for-byte) and correctly tiered. **S090** is the only row
without any sha256 in its anchor.

## Checklist (S072–S095)

`cells` = data columns (contract 11 ⇒ `awk NF==13`); `sha` = full 64-hex
digests in the anchor cell that join a committed receipt; T4 keyword checked in
`source + scope` with the measure.py keyword table.

| row | cells | kind/tier/status | opened | recheck | sha (anchor→receipt) | used-by | T4 | note |
|---|---|---|---|---|---|---|---|---|
| S072 | 11 | docs/A/mined | 2026-10-20 | on-change | 1/1 | walker-route-r18.md | walker | ok |
| S073 | 11 | code/A/mined | 2026-10-20 | on-release | 1/1 | walker-route-r18.md | walker | lines 1–113 end exactly at the prefix table |
| S074 | 11 | code/A/mined | 2026-10-20 | on-release | 1/1 | walker-route-r18.md | walker | ok |
| S075 | 11 | code/A/mined | 2026-10-20 | on-release | 1/1 | walker-route-r18.md | walker | ok |
| S076 | 11 | code/A/mined | 2026-10-20 | on-release | 1/1 | walker-route-r18.md | walker | ok |
| S077 | 11 | code/A/mined | 2026-10-20 | on-release | 1/1 | walker-route-r18.md | walker | ok |
| S078 | 11 | code/A/mined | 2026-10-20 | on-release | 1/1 | walker-route-r18.md | walker | line 21 `notify`, line 30 `xdg = "3.0.0"` confirmed |
| S079 | 11 | code/A/mined | 2026-10-20 | on-release | 1/1 | walker-route-r18.md | walker | reproducible; tag identity not in row — R4 |
| S080 | 11 | docs/A/mined | 2026-10-20 | on-release | 1/1 | walker-route-r18.md | elephant | ok |
| S081 | 11 | code/A/mined | 2026-10-20 | on-release | 1/1 | walker-route-r18.md | elephant | ok |
| S082 | 11 | code/A/mined | 2026-10-20 | on-release | 1/1 | walker-route-r18.md | elephant | ok |
| S083 | 11 | code/A/mined | 2026-10-20 | on-release | 1/1 | walker-route-r18.md | elephant | ok |
| S084 | 11 | docs/A/mined | 2026-10-20 | on-release | 1/1 | walker-route-r18.md | walker (scope) | **unversioned `/latest`** — R1 |
| S085 | 11 | code/A/mined | 2026-10-20 | on-change | 1/1 | walker-route-r18.md | walker | host equality verified |
| S086 | 11 | code/A/mined | 2026-10-20 | on-change | 1/1 | walker-route-r18.md | walker | host equality verified |
| S087 | 11 | code/A/mined | 2026-10-20 | on-change | 1/1 | walker-route-r18.md | walker | host equality verified |
| S088 | 11 | code/A/mined | 2026-10-20 | on-change | 1/1 | walker-route-r18.md | walker | host equality verified |
| S089 | 11 | code/A/mined | 2026-10-20 | on-change | 2/2 | walker-route-r18.md | walker | host equality verified |
| S090 | 11 | code/A/mined | 2026-10-20 | on-change | **0/0** | walker-route-r18.md | walker | **no digest** — R3 |
| S091 | 11 | code/A/mined | 2026-10-20 | on-change | 2/3 | walker-route-r18.md | walker | binary digest is host-only |
| S092 | 11 | docs/A/mined | 2026-10-20 | on-release | 4/4 | theme-route-r18.md | swaybg | claims verified |
| S093 | 11 | code/A/mined | 2026-10-20 | on-release | 5/5 | theme-route-r18.md | theme | claims verified |
| S094 | 11 | code/A/mined | 2026-10-20 | on-release | 3/3 | theme-route-r18.md | theme | **tree HTML not reproducible** — R2 |
| S095 | 11 | code/A/mined | 2026-10-20 | 90d | 1/3 | theme-route-r18.md | theme | two digests are host-only |

Shape facts: 24 rows contiguous S072–S095, all inside `## Registry`, 24/24
`NF==13`; kinds `{docs, code}`, tier A, status `mined`; no tier-C/community-A
violation; 23/24 anchors carry ≥1 full 64-hex digest; 37 digests total, 34
join receipts, 3 are host-only (S091 `/usr/bin/walker`, S095 `theme.name`,
S095 background image) — the expected host-row exemption.

## Findings

### R1 — MEDIUM: S084 anchors an unversioned `docs.rs/latest` page

`corpus/SOURCES.md:96`. Source URL `https://docs.rs/xdg/latest/xdg/struct.BaseDirectories.html`;
anchor = "saved HTML lines 302, 306, 356-362; sha256 0291cfe6…". The page body
identifies **xdg 3.0.0** (`grep -o 'xdg [0-9][0-9.]*'` → `xdg 3.0.0`; link
`/xdg/3.0.0/`), and walker declares `xdg = "3.0.0"` (`S078`, Cargo.toml:30),
but the row records no version and the URL is a moving pointer.

- Contract: anchor must carry a revision ("version, commit, or publication
  date", `SOURCES-CONTRACT-v1.md` §Shape). `/latest` has none; the digest is
  reproducible only while `latest == 3.0.0`.
- Gate: this is exactly the "unversioned docs site as version-specific
  support" class the round said it would leave unrowed (`lessons/round-18.md:32-33`).
- Measured: my `16:02Z` refetch of `/latest` is still `0291cfe6…` (byte-stable
  today), but the same commit **already holds the version-pinned receipt**:
  `https://docs.rs/xdg/3.0.0/xdg/struct.BaseDirectories.html`,
  `sha256 adaec7c32cc0595f59c154b407cf5a4ca85c6c40adf269a5046ccdd2b08762f6`,
  105,205 B, fetched `2026-10-20T15:41:24Z` by seat `MadoR18.SrcWalkerThemes`
  (committed JSONL at 4c103b55). I refetched it at `16:02Z`: identical digest.
- Content equivalence: the `find_config_file` documentation segment is
  byte-identical between the two bodies after stripping the "Source" link
  (974 B each); the diff is docs.rs navigation (`/crate/xdg/latest` →
  `/crate/xdg/3.0.0`, release-menu URLs). Line numbers move: latest
  302/306/356–362 vs pinned 299/303/354+. A section anchor
  (`#method.find_config_file`) would not move.
- Score impact: none. P3 credit in `measure.py` needs one ht tps upstream row
  naming the surface; S072–S083 supply it. Removing S084 leaves
  `sources_ok` shorter but coverage intact.
- Remedy (contract-correct): `anchor` is not an in-place cell (Rule 2). Append a
  new row whose `teaches` opens `supersedes S084 —`, URL
  `https://docs.rs/xdg/3.0.0/xdg/struct.BaseDirectories.html`, sha
  `adaec7c3…`, anchor `#method.find_config_file` + the two default values;
  or reject S084 and cite the pinned row. Do not silently edit S084.

### R2 — MEDIUM: S094's tree-listing digests are irreproducible by construction

`corpus/SOURCES.md:106`. Anchor cites `50c1ac25…` (themes/matte-black tree,
229,027 B) and `9e1160a0…` (backgrounds tree, 218,578 B) as "digest-only HTML".
Both `receipt → body` joins are valid (committed bodies hash to the receipts),
but the URL → body step fails on refetch:

| URL (same as receipt) | committed | my refetch `16:03/16:04Z` |
|---|---|---|
| `github.com/basecamp/omarchy/tree/v3.8.4/themes/matte-black` | `50c1ac25…`, 229,027 B | `8bfaba24…`, 229,026 B, `final_url` `github.com/omacom/omarchy/...` |
| `…/matte-black/backgrounds` | `9e1160a0…`, 218,578 B | `2d22e126…`, 218,579 B, `final_url` `…/omacom/…` |

Cause is both structural and environmental: the page carries per-request
`<meta name="fetch-nonce" content="v2:…">` (line 170), `request-id` (line 176)
and `html-safe-nonce`, which differ between the committed body and the refetch;
GitHub also redirects the renamed org (`basecamp` → `omacom`). This is the
Gate's named reject class ("HTML pages as sole support — per-fetch tokens make
the digest irreproducible", `lessons/round-18.md:32-33`), and the file list is
that row's sole support.

The information itself is right and recoverable: the committed page embeds
`"currentOid":"8fcc9d6048af4cb0e3af8512c78049857a3b53dd"` and the nine entries
the row lists. The raw payload digest is reproducible: my refetch of
`themes/matte-black/colors.toml` is `dbdd13a6…` (identical), and host
`current/theme/colors.toml` is byte-identical.

- Remedy: re-anchor the file list to the **API tree JSON at commit 8fcc9d60**,
  which is already receipted at this commit (`c5facb09…`, 401,538 B, three
  seats) and has no per-fetch nonce, or to the tag tarball; superseding row or
  lesson erratum. Do not re-use the HTML digest.
- Score impact: none (S092/S093 carry P5's upstream T4 credit).

### R3 — LOW: S090 is the only row with no sha256 in its anchor

`corpus/SOURCES.md:102` cites pacman.log lines and exact version strings but no
digest/byte snapshot. The log is append-only, so existing line numbers stay
valid — I verified today at 3,160 lines / 244,104 B that lines 1943, 2929,
3062, 3095, 3123 carry exactly the row's transactions (`walker 2.16.2-1 ->
2.17.0-1`, `2.17.0-1 -> 2.17.2-1`, `walker-restart.hook` ×2, `elephant
2.21.0-1 -> 2.22.1-1`). What is missing is proof the cited bytes were not
edited: no digest, no size. A line-block digest would be stable under appends:

```
sed -n '1943p;2929p;3062p;3095p;3123p' /var/log/pacman.log | sha256sum
ec15c87d09ed243e9d76f35190c4084b41150378e4de22297e3d35924c9532c7
```

Also `kind = code` stretches the enum for a log; `dataset` fits and is already
in the vocabulary (no tier change; a log is still the host's primary record).
Low: S090 supports no T4-required upstream slot, and the host version binding
is corroborated by S085/S091 bytes.

### R4 — LOW: S079 is reproducible today but carries no commit identity

`corpus/SOURCES.md:91` (codeload tag tarball). Reproducibility measured, not
assumed: four committed receipts (NoteWalker `15:42:32Z`; wave-2 ReopenS078,
ReopenS079; ReviewWalkerUpstream) plus my `16:01:57Z` fetch all return
`e50c606040b24f2a6045292f5f6a08c8a05ac599878ac781b1a5fcf50d353a56`,
165,438 B; no URL in the whole receipt set has two digests. Extraction of my
copy verifies the row's claim: zero `notify::` / `use notify` in `src/`,
`notify` only as `src/niri.rs` closure names (160–213) and Cargo.lock; exactly
three `connect_changed` (`main.rs:142,149` color-scheme/accent-color,
`ui/window.rs:479` input); no `reload` / `set_config`; `notify = "8.2.0"` at
Cargo.toml:21.

Tier A / kind `code` is correct for "whole-tree textual search": it is the
primary tree at the tag. The residual risk is identity: the URL names a mutable
tag and the row records no peeled commit (the entry records
`a515085f…` at `walker-route-r18.md` `verified-at`), and codeload archives are
generated on demand, so an archive-generation change would break the digest
without changing a byte of source. Recommend recording the commit and/or
anchoring whole-tree negatives to the API tree JSON already receipted at this
commit (`4eef2da714db803d…`, 26,501 B). Not blocking.

### R5 — INFO (cross-cutting, not a row defect): receipts committed, bodies not

At 4c103b55 `.ufo/waves/round-18/fetch` contains 21 committed
`receipts.jsonl` (301 lines); no body files and no `RETENTION.json` are in the
commit (`git ls-tree -r`). `fetch-verify.py` re-hashes bodies from disk and,
without a digest-only manifest, returns `MISSING` for an absent body
(`fetch-verify.py:125-155`). [INFERENCE from code read; I did not execute the
lane tool, since the item authorises only the census command.] Consequence for
this item: a closure at the commit can verify S079/S084/S094 only by
**refetching**. That works for S079 (today), works for S084 only while
`latest == 3.0.0`, and fails for S094's tree HTML now. The retention policy
belongs to the `SentinelFetchBodies` follow-up, not to these rows; flagging the
dependency, not owning it.

## Spot-checks behind the verdict

- S073: `resources/config.toml` is 305 lines; the cited `1–113` range ends
  exactly at the last `[[providers.prefixes]]` entry (line 113), so the range
  is not a truncated read of a longer table.
- S085–S089: every "equal to host copy" claim verified by hashing both sides:
  `fecf71fa…` walker config, `fd9e93f8…` launch, `9ac82d0c…` restart,
  `05cd9c67…` refresh, `5cb9874e…` walker.desktop, `de0f7029…` restart.conf.
- S091: `/usr/bin/walker` 7,039,912 B, digest `25240650…`, and
  `dd if=/usr/bin/walker bs=1 skip=806960 count=13743 | sha256sum` =
  `3c5c6867…`, equal to `/etc/xdg/walker/config.toml`; sizes/line counts
  1,336 B/49 L and 13,743 B/305 L match the row.
- S092: swaybg.1.scd `-i`/`-m`, "Default is _stretch_" (`:19-31`); main.c
  `-i`/`-m` parse (`521-529`), image-path default to stretch (`575-577`),
  load-by-path loop (`658-663`); background-image.c reads by path (`24-46`).
- S093: bg-next/bg-set retarget with `ln -nsf` and relaunch
  `swaybg … -m fill`; theme-set's restart list (`:54-62`) has no swaybg.
- S094/S095: `current/theme.name` = `matte-black`; `current/background` →
  `theme/backgrounds/0-ship-at-sea.jpg` (`55fa691a…`); walker
  `omarchy-default/style.css` `481267af…`; 24 files at theme top level + 4
  backgrounds; the three consumer symlinks (mako, btop, nvim) present.
- Receipt integrity: all 301 committed receipt lines carry schema
  `mado-fetch-receipt-v1`; 245 distinct URLs; zero same-URL digest conflicts.

## Commands run (exact) and results

```
$ /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin mado
mado    W04 S030 duplicate url wiki.hypr.land/Configuring/Basics/Window-Rules across scopes
mado    W04 S042 duplicate url wayland.freedesktop.org/extras.html across scopes
mado    W04 S045 duplicate url wiki.hypr.land/Configuring/Basics/Window-Rules across scopes
mado    ok  /home/vgpnk/Projects/shokunin/mado-shokunin/corpus/SOURCES.md
RC=0

$ python3 .ufo/waves/round-17/measure.py 4c103b55b1ea5c3c555884afe3eb69b5189701b7
c2.count = 6, c2.score = 10.0, c2.rejected = [], P1..P6 all covered
(u_routes 7/7)

$ git show 4c103b55:corpus/SOURCES.md | sha256sum
9552071c0b286075ffabb3a7ea1373e8dbaef5e6c37f906d2620ae83454f26de  -
$ sha256sum corpus/SOURCES.md
9552071c0b286075ffabb3a7ea1373e8dbaef5e6c37f906d2620ae83454f26de  corpus/SOURCES.md
(git show d9a5a18 row count 71; 4c103b55 row count 95; diff adds exactly
 S072..S095, 24 insertions, 0 deletions)

# row parse: 24/24 NF=13; kind/status/tier enums clean; opened all
# 2026-10-20; recheck in {on-change,on-release,90d}; used-by exact path;
# T4 keyword present for all 24 (source+scope)

# receipt join (committed receipts only): 301 lines / 21 seats / 245 urls /
# 0 multi-digest urls; 34 of 37 anchor digests join; 3 host-only

$ curl -sSL --max-time 60 -o walker-v2.17.2-src-repro.tar.gz \
   https://codeload.github.com/abenz1267/walker/tar.gz/refs/tags/v2.17.2
e50c606040b24f2a6045292f5f6a08c8a05ac599878ac781b1a5fcf50d353a56  165438 bytes
$ curl -sSL --max-time 60 -o xdg-basedirectories-repro.html \
   https://docs.rs/xdg/latest/xdg/struct.BaseDirectories.html
0291cfe6cd80b67fe6e4b276aae8323650d77dbfb88b1f3c9d0ff150b50f9f0d  105537 bytes
$ curl -sSL --max-time 60 -o xdg-3.0.0-basedirectories.html \
   https://docs.rs/xdg/3.0.0/xdg/struct.BaseDirectories.html
adaec7c32cc0595f59c154b407cf5a4ca85c6c40adf269a5046ccdd2b08762f6  105205 bytes
$ curl ... https://github.com/basecamp/omarchy/tree/v3.8.4/themes/matte-black
8bfaba248412fff8dd82059f973ee8fee1a87b90ab8b12ff5c380c93dcea9fbb  229026 bytes
   final_url=https://github.com/omacom/omarchy/tree/v3.8.4/themes/matte-black
$ curl ... https://github.com/basecamp/omarchy/tree/v3.8.4/themes/matte-black/backgrounds
2d22e12656d6e52431c79565c0652c75ce2396259d397459ddc5b1e90f2e6045  218579 bytes
   final_url=https://github.com/omacom/omarchy/tree/v3.8.4/themes/matte-black/backgrounds
$ curl ... raw.githubusercontent.com/basecamp/omarchy/v3.8.4/config/walker/config.toml
fecf71fa4253803e4864bd0e890ad54cfda2233e07ed1c337b3449b7303d1787  1336 bytes (no redirect)
$ curl ... raw.githubusercontent.com/basecamp/omarchy/v3.8.4/themes/matte-black/colors.toml
dbdd13a629aac86daa0f01ad03b66429d9e4b303758ea464c8bcc917a5601786  461 bytes (no redirect)

$ diff (tree body at commit) (my refetch)   # 60 differing tag-lines
170: fetch-nonce v2:ca4a41fb-… vs v2:792a7939-… ; 176: request-id … differs
$ python: find_config_file segment equal after stripping Source link: True 974 974

$ dd if=/usr/bin/walker bs=1 skip=806960 count=13743 | sha256sum
3c5c6867d0216d0c86437a9c413cff4608da514c53e50b1bc412f4965d750a8b
$ sed -n '1943p;2929p;3062p;3095p;3123p' /var/log/pacman.log | sha256sum
ec15c87d09ed243e9d76f35190c4084b41150378e4de22297e3d35924c9532c7
   (file 3,160 lines / 244,104 B at read time)
$ tar -xzf walker-v2.17.2-src.tar.gz; grep -rn 'notify::\|use notify' src/   -> none
$ grep -rn connect_changed src/   -> main.rs:142,149 ; ui/window.rs:479
```

My fetches are recorded as 7 `mado-fetch-receipt-v1` lines in
`.ufo/waves/round-18/fetch/MadoR18.ReviewSourcesRows/receipts.jsonl` (bodies
beside them; untracked until L1 commits). No tool install or upgrade.

## Residual risk / verification gaps

1. **Instruments cannot see either defect.** Census validate checks shape and
   disk paths; `measure.py` checks surface/source tokens; fetch-verify checks
   receipt→saved-body at commit. All three pass S084 and S094. Only a
   from-scratch refetch exposes the moving `latest` URL and the HTML nonces.
   So "receipted" is weaker than "reproducible" for these two rows; the C2
   text should say which one it means.
2. **Same-day refetch only.** My reproducibility evidence and the seats' were
   taken within one hour of each other on 2026-10-20. Long-horizon stability of
   codeload archives, raw.githubusercontent at a moved tag, and docs.rs is not
   established.
3. **Upstream owner drift is live.** `basecamp/omarchy` now redirects to
   `omacom/omarchy` on github.com; the raw host still serves the old path
   directly (200, no redirect) at review time, so the tag-pinned rows S085–
   S089/S093/S094 remain fetchable, but future receipts will record different
   `final_url` values.
4. **Bodies are not in the commit** (R5): a clone can only refetch, which
   amplifies risks 1–3 for the rows those bodies back.
5. I did not run the lane's `fetch-verify.py`, `mado-verify.sh`,
   `mado-tripwire.py` or any `--frozen` path: the item authorised the census
   command and read-only shell checks only.
