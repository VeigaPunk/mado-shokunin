# ReopenS085 — non-author re-open of SOURCES row S085 (round 18, wave 2)

Seat: `MadoR18.ReopenS085`, wave 2 (FALSIFY), 2026-10-20. Target
`/home/vgpnk/Projects/shokunin/mado-shokunin`; baseline `d9a5a18`, integration
`4c103b55b1ea5c3c555884afe3eb69b5189701b7`. Read-only lane: no git/jj write, no
package/service/compositor/input probe, no config-tree write. Only my fetch dir
and this report were written.

## 1. Row under test and binding to the integration commit

The row text is identical in the worktree and at `4c103b55`:

```
git show 4c103b55:corpus/SOURCES.md | sed -n '97p'
| S085 | omarchy stock walker config @ v3.8.4 — https://raw.githubusercontent.com/basecamp/omarchy/v3.8.4/config/walker/config.toml | code | A | omarchy stock user walker config at checkout tag v3.8.4 | file bytes 1,336 B; sha256 fecf71fa…3d1787 (equal to host ~/.config/walker/config.toml) | the host user config is the omarchy stock file; prefix table and emergency row live here | mined | 2026-10-20 | on-change | corpus/knowledge/walker-route-r18.md |
```

Row shape: `awk -F'|'` on `| S085 |` → `NF=13` (11 columns), tier `A`, kind
`code`, status `mined`, `used-by` exists. No other registry row carries this
canonical URL; S091 is the separate host-bytes row and its config digest
(`fecf71fa…`) agrees with S085 — no contradiction.

## 2. Fetch ledger (independent)

Fetches saved under `.ufo/waves/round-18/fetch/ReopenS085/` with three
`mado-fetch-receipt-v1` lines in `receipts.jsonl`:

| # | URL requested | http | final_url (effective) | bytes | sha256 |
|---|---|---|---|---|---|
| 1 | `raw.githubusercontent.com/basecamp/omarchy/v3.8.4/config/walker/config.toml` (the row's URL) | 200 | same | 1,336 | `fecf71fa4253803e4864bd0e890ad54cfda2233e07ed1c337b3449b7303d1787` |
| 2 | `github.com/basecamp/omarchy/raw/v3.8.4/config/walker/config.toml` | 200 | `raw.githubusercontent.com/omacom/omarchy/v3.8.4/…` | 1,336 | `fecf71fa…3d1787` |
| 3 | `raw.githubusercontent.com/basecamp/omarchy/8fcc9d6048af4cb0e3af8512c78049857a3b53dd/config/walker/config.toml` (commit-pinned) | 200 | same | 1,336 | `fecf71fa…3d1787` |

Three fetches, one digest, identical whole-file bytes (`cmp` clean against the
host copy). Wave-1 receipts for the same content:

```
.ufo/waves/round-18/fetch/NoteWalker/receipts.jsonl:7
  url = row URL, http 200, 1336 B, sha256 fecf71fa…3d1787, body omarchy-v3.8.4-config-walker-config.toml
.ufo/waves/round-18/fetch/SrcOmarchyWalker/receipts.jsonl:2
  url = github.com/basecamp/omarchy/raw/v3.8.4/…, final_url = raw.githubusercontent.com/omacom/omarchy/v3.8.4/…,
  http 200, 1336 B, sha256 fecf71fa…3d1787, body config-walker-config.toml
```

Both wave-1 bodies re-hashed locally (`sha256sum`) → `fecf71fa…3d1787` each, so
the receipts' digests are the stored bytes, not transcriptions. No receipt has a
different 200 digest for this content (no CONFLICT).

**Org-rename observation (real, not a typo).** My fetch #2 reproduced the
`omacom` `final_url` that SrcOmarchyWalker recorded: the repo now redirects
`basecamp/omarchy` → `omacom/omarchy`. Both routes serve the same tag and bytes.
Consequence for the wave-2 `fetch-verify` join: SrcOmarchyWalker's receipt has
neither `url` nor `final_url` equal to the row's first source URL, so only
NoteWalker's receipt is URL-eligible to credit S085; the digest agreement across
two seats still holds.

## 3. Tag resolution and the pin question

```
git ls-remote --tags https://github.com/basecamp/omarchy 'refs/tags/v3.8.4' 'refs/tags/v3.8.4^{}'
8fcc9d6048af4cb0e3af8512c78049857a3b53dd	refs/tags/v3.8.4        (no peeled line)
git ls-remote https://github.com/omacom/omarchy 'refs/tags/v3.8.4'
8fcc9d6048af4cb0e3af8512c78049857a3b53dd	refs/tags/v3.8.4
```

The URL is **tag-ref-pinned** (ref segment is a tag, not a branch); the tag is
lightweight (`8fcc9d60…`, no tag object), and a commit-pinned fetch of the same
path returns identical bytes — so the tag→commit→bytes chain is closed at this
date. "Pinned" is by ref name only: a force-moved tag could serve different
bytes later, which is why the anchor's sha256 (not the tag) is the real pin.
The note's own `verified-at:2` records `omarchy v3.8.4 = 8fcc9d60…`; the host
checkout agrees by bytes: `~/.local/share/omarchy/.git/packed-refs:2,321,508`
all `8fcc9d60…` with `HEAD` → `refs/heads/master`.

## 4. Host equality and the "stock" clause

```
sha256sum ~/.config/walker/config.toml                    → fecf71fa…3d1787
sha256sum ~/.local/share/omarchy/config/walker/config.toml → fecf71fa…3d1787
wc -lc <fetched body>                                      → 49 lines, 1336 bytes
cmp <fetched body> ~/.config/walker/config.toml            → identical
```

So "equal to host ~/.config/walker/config.toml" and the note's `1,336 / 49` are
exact. Provenance beyond identity is also visible in the checkout, read as
bytes: `install/config/all.sh:21` runs `config/walker-elephant.sh`, and
`migrations/1752981883.sh:9-10` / `1758107879.sh:36-37` do
`cp -r ~/.local/share/omarchy/config/walker/* ~/.config/walker/`. The row's
"stock user config" is therefore byte identity plus omarchy's own copy path, not
an assumption.

## 5. kind / tier / scope / teaches

- **kind `code`** — in the contract enum; the artifact is the upstream project's
  own TOML in its repo. Precedent: S020 (`code` for Hypr/omarchy config files).
- **tier `A`** — contract: A = "primary or authoritative for that scope (… source
  code …)". A raw file served from the maintainers' repo at a tag is the primary
  source for its own bytes. Scope is narrow ("that config at tag v3.8.4"), so no
  global claim is made; `community`-style inflation is absent.
- **scope keyword** — scope "omarchy stock user **walker** config at checkout tag
  v3.8.4" and the source path both name `walker`, satisfying the P3 surface
  keyword rule. `surface: P3` at note `:4`.
- **teaches** — grounded in the bytes I fetched: six `[[providers.prefixes]]`
  tables at `:23-45` (`/`, `.`, `:`, `=`, `@`, `$`) and one `[[emergencies]]`
  table at `:47-49`. First clause ("the host user config is the omarchy stock
  file") is grounded by the sha equality in §4; strictly it is byte identity, not
  install causality — the note itself keeps the `omarchy-refresh-config`
  replacement question as `[UNK]` (`:311-312`), so no stronger claim is smuggled
  in.

## 6. Does the citing note use it truthfully?

`corpus/knowledge/walker-route-r18.md` (`sha256 3ff430a4…fb8fbf20` at `4c103b55`,
equal to worktree) names S085 exactly once, in the `source:` head as
`S085 https://raw.githubusercontent.com/basecamp/omarchy/v3.8.4/config/walker/config.toml (stock user config)`
— a truthful descriptor. All `OC` usage reproduces against the fetched body:

- `:34` anchor key `OC` = that URL, "omarchy checkout tag v3.8.4", `OC:n` = file line — correct.
- `:180-181` host table: both host copies `fecf71fa…`, `1,336 / 49`, "equal to `OC` (sha equal)" — measured true in §4.
- `:190-197` per-option claim with line anchors `[:1] [:2] [:3] [:4] [:5] [:10-11] [:13-14] [:16-17] [:18-21] [:23-45] [:47-49]` — every one lands exactly (e.g. `:3` `theme = "omarchy-default"`, `:17` `max_results = 256`, `:23-45` six prefixes, `:47-49` emergency row). No anchor is off by a line.
- `:198-199` "Its prefix table differs from upstream [WC:75-113]" — true: the packaged `/etc/xdg` file carries ten tables (`;`, `>`, `/`, `.`, `!`, `%`, `=`, `@`, `:`, `$`), all inside those lines, while `OC` carries six different ones (`/`, `.`, `:`, `=`, `@`, `$`).
- Note structure for the instrument: `surface: P3` `:4`; `## Upstream contract` `:46`, `## Host declaration` `:173`, `## Safe observation` `:258`, `## Unexercised behavior` `:283` with 15 `[UNK]` markers.

No statement attributed to `OC`/S085 is contradicted by the bytes.

## 7. Residual unknowns / caveats (do not change the verdict)

- Lightweight tag: name-pinned only; the sha256 anchor is what makes drift
  detectable. `recheck: on-change` is appropriate.
- The row's anchor cell does not carry the tag commit `8fcc9d60…` (the note does,
  `verified-at:2`). Not a defect: the anchor is the whole file's bytes + digest,
  which is exact, and SOURCES rule 2 forbids in-place anchor edits — a commit
  string would only be added by a superseding row if the lane wants it.
- SrcOmarchyWalker's `final_url` (`omacom`) is genuine redirect output, so a
  URL-equality join credits NoteWalker alone; the two seats' digests agree.
- Not observed: which mechanism placed the user copy (install vs migration — both
  copy the same bytes), and walker reading this file at runtime (the note is
  documentary-only by declaration).

GATE | S085 | https://raw.githubusercontent.com/basecamp/omarchy/v3.8.4/config/walker/config.toml | 2026-10-20 | .ufo/waves/round-18/fetch/ReopenS085/omarchy-v3.8.4-config-walker-config.toml:49 "command = \"omarchy-restart-walker\"" (3 words) | fecf71fa4253803e4864bd0e890ad54cfda2233e07ed1c337b3449b7303d1787 | agree: independent fetch reproduces the row digest and both wave-1 receipts (1,336 B); URL is tag-ref-pinned at lightweight v3.8.4 = 8fcc9d60 with the commit-pinned fetch byte-identical; tier-A primary code for a scope naming the P3 keyword walker; teaches and every OC line anchor in the note reproduce against the body, with only name-pinned-tag and org-rename caveats
