# ReopenS088 — non-author re-open of SOURCES row S088 (R17-V3)

Seat: MadoR18.ReopenS088 (wave 2, falsify). Baseline note: rows read at lane
revisions `4c103b55b1ea5c3c555884afe3eb69b5189701b7` (integration) and
`abfbf35b1ed4d4a1eb294d525ef286be30f3886f` (receipts). No lane or fleet VCS write;
no package, service, socket, compositor or REA operation. Tools installed: none.

Axes (godspeed): (1) digest reproducibility, (2) tag-pin independence beyond the
tag name, (3) row-shape/credit eligibility (kind/tier/scope), (4) citing-note
truthfulness. All four were attacked concurrently; no move regressed an axis.

## Commands and observed output

Fetch (my seat dir `.ufo/waves/round-18/fetch/ReopenS088/`; receipts.jsonl, 2 lines):

```
$ curl -sSL --max-time 60 -o omarchy-refresh-walker.v3.8.4 \
    -w '%{http_code} %{url_effective}\n' \
    https://raw.githubusercontent.com/basecamp/omarchy/v3.8.4/bin/omarchy-refresh-walker
200 https://raw.githubusercontent.com/basecamp/omarchy/v3.8.4/bin/omarchy-refresh-walker
$ sha256sum omarchy-refresh-walker.v3.8.4
05cd9c672252fd17d2a2c6d699a7e59ed1cd81c0c873abb1a6c6bd45c093f9a2  omarchy-refresh-walker.v3.8.4
$ wc -c
893
```

Tag resolution (read-only, outside the lane):

```
$ git ls-remote https://github.com/basecamp/omarchy refs/tags/v3.8.4 'refs/tags/v3.8.4^{}'
8fcc9d6048af4cb0e3af8512c78049857a3b53dd	refs/tags/v3.8.4
$ git ls-remote --tags https://github.com/basecamp/omarchy 'v3.8.4*'
8fcc9d6048af4cb0e3af8512c78049857a3b53dd	refs/tags/v3.8.4
$ git ls-remote https://github.com/basecamp/omarchy HEAD
3ac43659dcbf88e84d951e3ce979b48a60a7d1f2	HEAD
```

No `^{}` line is emitted for the tag, so `v3.8.4` is a **lightweight** tag. The
row URL carries `/v3.8.4/`, i.e. it is tag-pinned; HEAD (`3ac43659…`) is a
different commit, so the pin is load-bearing.

Independent pin check (second fetch, commit-addressed):

```
$ curl -sSL ... https://raw.githubusercontent.com/basecamp/omarchy/8fcc9d6048af4cb0e3af8512c78049857a3b53dd/bin/omarchy-refresh-walker
200
$ sha256sum omarchy-refresh-walker.commit-8fcc9d60
05cd9c672252fd17d2a2c6d699a7e59ed1cd81c0c873abb1a6c6bd45c093f9a2
$ cmp -s omarchy-refresh-walker.v3.8.4 omarchy-refresh-walker.commit-8fcc9d60
BYTE_IDENTICAL
```

Tree-blob identity at the tag commit (tree receipt from wave 1,
`fetch/SrcOmarchyThemeLayout/tree-v3.8.4-8fcc9d6.json`, whose sha256
`c5facb09086f11c1477c0a5553235ed36883816d93d1e4c94a4ddb62adc43c9d`
matches its receipt, `truncated: false`):

```
{'path': 'bin/omarchy-refresh-walker', 'mode': '100755', 'type': 'blob',
 'sha': '2354144ff4baab200767d52efcb61abde9120d35', 'size': 893}
$ git hash-object omarchy-refresh-walker.v3.8.4        → 2354144ff4baab200767d52efcb61abde9120d35
$ git hash-object ~/.local/share/omarchy/bin/omarchy-refresh-walker → 2354144ff4baab200767d52efcb61abde9120d35
```

So the bytes I read are exactly the blob recorded in the `v3.8.4` tree, and the
host copy is the same blob — not merely an equal sha256 of a re-serialised file.

Host copy (bytes only, host pause respected):

```
$ sha256sum ~/.local/share/omarchy/bin/omarchy-refresh-walker
05cd9c672252fd17d2a2c6d699a7e59ed1cd81c0c873abb1a6c6bd45c093f9a2
$ wc -c → 893;  wc -l of body → 26
```

Receipts for the same URL under `.ufo/waves/round-18/fetch/*/receipts.jsonl`:

| receipt | fetched_at | status | bytes | sha256 |
|---|---|---|---|---|
| `NoteWalker/receipts.jsonl:8` (wave 1) | 2026-10-20T15:40:36Z | 200 | 893 | `05cd9c672252fd17d2a2c6d699a7e59ed1cd81c0c873abb1a6c6bd45c093f9a2` |
| `ReviewWalkerUpstream/receipts.jsonl:14` (wave-2 sibling, 16:00:36Z) | 2026-10-20T16:00:36Z | 200 | 893 | same |
| `ReopenS088/receipts.jsonl:1` (this check, tag URL) | 2026-10-20T15:59:42Z | 200 | 893 | same |
| `ReopenS088/receipts.jsonl:2` (this check, commit URL) | 2026-10-20T16:00:07Z | 200 | 893 | same |

Wave-1 `NoteWalker` body file `omarchy-v3.8.4-bin-omarchy-refresh-walker` exists
in the working tree at 893 B with the same sha256; its committed receipt line is
byte-identical at `4c103b55` (blob `f05e1f35…`) and `abfbf35` (sha256 of the
committed file `a244ddc1…` equals the working file). The row itself is
byte-identical at `4c103b55`, `abfbf35` and the working tree (line sha256
`ba3d88f763575b8f31e0d13b06f607be793d890f86ca026b12a5c98aa08539aa`).

Row shape: line 100 has 12 pipes = 11 cells, matching the header
(`id|source|kind|tier|scope|anchor|teaches|status|opened|recheck|used-by`).

## Judgement

- **Digest — agree.** Row anchor `05cd9c67…`, wave-1 receipt, two wave-2
  re-fetches, the tag-commit blob and the host copy all agree on 893 bytes /
  `05cd9c672252fd17d2a2c6d699a7e59ed1cd81c0c873abb1a6c6bd45c093f9a2`.
  Reproducible by an unrelated seat.
- **kind `code` — agree.** The body is a bash script (shebang `#!/bin/bash`,
  26 lines); comparable to other `code` rows.
- **tier `A` — agree.** For the scope "what omarchy's refresh script does at
  v3.8.4" the upstream file at a resolved lightweight tag is primary; the URL
  is pinned and the commit-addressed bytes match, so the tag is not a moving
  anchor.
- **scope — agree, with one wording nit.** The scope cell names the surface
  (`omarchy-refresh-walker`; P3 keyword `walker`, also `elephant` in the row),
  and its operation list matches lines 5–26. Nit: "copying … menus" is
  imprecise — line 22 **symlinks** `$OMARCHY_PATH/default/elephant/*.lua` via
  `ln -snf`; only autostart/drop-in are copied (lines 6, 10). The citing note
  states "links", so no note inherits the imprecision. Not credit-bearing
  either way (the scope is a summary, not the taught contract).
- **`teaches` — grounded.** Lines 15–17 make the three `omarchy-refresh-config`
  calls (`walker/config.toml`, `elephant/calc.toml`,
  `elephant/desktopapplications.toml`); line 26 calls
  `omarchy-restart-walker`. "then restarts" is a
  call, not a claimed successful restart — consistent with the restart helper's
  conditional behaviour not being read. The cell's own caveat ("that helper's
  own behaviour was not read") matches the note's `[UNK]` at
  `walker-route-r18.md:311` ("`omarchy-refresh-config` was not fetched").
- **Citing note — truthful.** `corpus/knowledge/walker-route-r18.md:1` lists
  `S088 …/bin/omarchy-refresh-walker (refresh)`; lines 165–168 cite `OF:5-10`,
  `OF:15-17`, `OF:20-23`, `OF:26`, and every anchor lands on the stated
  operation (copies autostart + restart drop-in; refreshes three configs; links
  elephant menus; calls the restart script). The host-declaration row at :188
  gives `05cd9c67…` / 893 B "equal to `OF`" — verified. The note is committed
  at `4c103b55` (blob `c2056f3f…`), identical to the working copy. No
  overstatement: the note does not claim tag bytes prove the host binary.
- **Receipt contract (observation, not a row defect).** At `4c103b55` all 21
  tracked files under `.ufo/waves/round-18/fetch/` are `receipts.jsonl`; body
  files are working-tree only. R17-V3's closure is therefore a re-fetch, and
  that re-fetch reproduces the receipt exactly. Nothing in S088's credit
  depends on an uncommitted body.

## Remaining unknowns

- `[UNK]` `omarchy-refresh-config`'s overwrite/merge semantics — not read (the
  row and note both say so; correctly outside S088's scope).
- `[UNK]` Whether a future move of tag `v3.8.4` would change the URL's bytes;
  today the tag is at `8fcc9d60…` and the commit-addressed copy is identical.
  The anchor is not digest-of-tag-object-bearing, so a moved tag would be
  detectable only by re-running `git ls-remote` as the note's recheck says.

GATE | S088 | https://raw.githubusercontent.com/basecamp/omarchy/v3.8.4/bin/omarchy-refresh-walker | 2026-10-20 | .ufo/waves/round-18/fetch/ReopenS088/omarchy-refresh-walker.v3.8.4:15 "omarchy-refresh-config walker/config.toml" (2 words) | 05cd9c672252fd17d2a2c6d699a7e59ed1cd81c0c873abb1a6c6bd45c093f9a2 | agree: tag v3.8.4 resolves 8fcc9d60 (lightweight), commit-addressed fetch byte-identical and tree blob 2354144f at 893 B; row, wave-1 receipt, sibling re-fetch and host copy all 05cd9c67; note anchors 5-10/15-17/20-23/26 exact
