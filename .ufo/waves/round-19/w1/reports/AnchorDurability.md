# MadoR19.AnchorDurability — rotation-only rule: red at 17661e0/9c54c56 on S084 (UNPINNED_ALIAS) and S094 (PER_FETCH_DIGEST), green on the S096–S098 worktree rows

Deliverable: `.ufo/waves/round-19/anchor-durability.py`, sha256
`9e66dce8c6af26df13769ce47fdaa3ff1464296d3929ea80bf13ee6aa77bc9e4`, 433 lines.
Reads committed bytes only (`git rev-parse`, `git ls-tree`, `git show`); no
network, no worktree read in the normal path, no host command, no gate
execution. Writes nothing.

Interface: `anchor-durability.py REV [--rows S###,...] [--exclude-status ST[,ST]]`.
One line per evaluated row, `ROW <id> durable|PER_FETCH_DIGEST|UNPINNED_ALIAS —
<reason>`, then `SUMMARY rev=… mined=<n|rows=<n> statuses=not:…> durable=…
per_fetch_digest=… unpinned_alias=… flagged=… receipt_files=…
bad_receipt_lines=…` and `FLAGGED <ids>`. Exit 0 none, 1 any flagged, 2 usage /
could-not-evaluate (bad REV, no `SOURCES.md` at REV, no rows, absent `--rows`
id, bad `--exclude-status` value). Default evaluated set is `mined` only;
`--exclude-status` replaces that with "every status not listed"
(`rejected,queued` reproduces mined-only; `rejected` adds `queued`).

## Rules

| Rule | Fires when |
|---|---|
| PER_FETCH_DIGEST | **observed rotation only**: committed receipts at REV hold ≥2 distinct sha256 among `http_status` 200 records for a URL the anchor credits, joined by (i) the exact http(s) URL in the source/anchor cell, or (ii) a 64-hex digest in the anchor that is one of that URL's recorded digests |
| UNPINNED_ALIAS | a `source` URL path segment exactly `latest`, `main`, `master` or `HEAD`, and the anchor names no pin: 40-hex commit, version tag, revision date (publication/modified/released/dated/archived — never an access/opened date), or a 7–39 hex abbreviated commit near an alias token |
| durable | neither fired. A page-credited 64-hex digest (clause tokens `tree`, `blob`, `html`, `listing`, `api.github.com`, `docs.rs`, or a source URL shaped github tree/blob, api.github.com, docs.rs, `*.html`) whose receipts show <2 distinct digests prints `sha256 X… is a page digest, not shown to rotate (receipts: N records, M digests)`; N=M=0 when no committed receipt covers it |

Precedence UNPINNED_ALIAS > PER_FETCH_DIGEST for the printed status. A row can
carry both an alias flag and a non-rotating page digest; the digest prints
after `also`. A path mention alone — including a git tree *object* id under
`themes/x` — credits no URL and cannot trigger rotation.

## Red at 17661e0 (L1-requested state)

`python3 -I .ufo/waves/round-19/anchor-durability.py 17661e0fa83f978fb659f5bb8fef47f0969f6945`
→ exit 1, 80 mined rows, 0 malformed, 49 receipt files, 0 bad receipt lines:

```
ROW S063 durable — sha256 b45c03dc… is a page digest, not shown to rotate (receipts: 1 records, 1 digests)
ROW S064 durable — sha256 f69cff6b… is a page digest, not shown to rotate (receipts: 1 records, 1 digests)
ROW S084 UNPINNED_ALIAS — source path segment latest and anchor names no 40-hex commit, tag or dated version; also sha256 0291cfe6… is a page digest, not shown to rotate (receipts: 6 records, 1 digests)
ROW S094 PER_FETCH_DIGEST — 5 distinct 200 digests for https://github.com/basecamp/omarchy/tree/v3.8.4/themes/matte-black (3b18a612… ≠ 50c1ac25…; matched by credited digest 50c1ac25…)
SUMMARY rev=17661e0fa83f978fb659f5bb8fef47f0969f6945 mined=80 durable=78 per_fetch_digest=1 unpinned_alias=1 flagged=2 receipt_files=49 bad_receipt_lines=0
FLAGGED S084 S094
```

At round-18 closure `9c54c56a6a7528675027b7f628f97a1b8d1b8e8d` the same
command prints `mined=80 durable=78 per_fetch_digest=1 unpinned_alias=1
flagged=2`, `FLAGGED S084 S094`, 49 receipt files, 0 bad lines — identical.

Row addresses at 17661e0: `corpus/SOURCES.md:75`/`:76` (S063/S064), `:96`
(S084), `:106` (S094); registry 95 rows = 80 mined + 8 queued + 7 rejected;
malformed rows (`awk -F'|' … NF!=13`) → 0.

## Worktree copy with S096–S098 integrated — green

The tool has no file-path mode, so the worktree rows were evaluated through a
scratch git repo: `/tmp/anchor-worktree` = copy of the current worktree
`corpus/SOURCES.md` (98 rows: 81 mined, 8 queued, 9 rejected; S084 and S094 are
now `rejected`, S096/S097/S098 added) plus the 49 receipt files extracted from
17661e0 with `git show <path>`; commit `4b721b14652f136bcf4890d90f7ddc9964e1f11f`.

`MADO_LANE=/tmp/anchor-worktree python3 -I .ufo/waves/round-19/anchor-durability.py HEAD`
→ **exit 0**, `mined=81 durable=81 per_fetch_digest=0 unpinned_alias=0
flagged=0`, no `FLAGGED` line. Notable rows:

```
ROW S097 durable — sha256 over raw bytes at ref v3.8.4
ROW S098 durable — no page digest; anchor pins 40-hex commit a515085fd39fae80acc086c8fbfd9b7771a9a11d
```

After committing those rows, L1 should run
`python3 -I .ufo/waves/round-19/anchor-durability.py <commit>` and expect
`flagged=0`, exit 0. Without a commit, reuse the recipe above (worktree
`SOURCES.md` + committed receipts in a scratch repo, `MADO_LANE=<scratch>`).

## Rotation evidence behind S094

Committed at 17661e0, `.ufo/waves/round-18/fetch/<seat>/receipts.jsonl`
(`http_status` 200, distinct sha256 for the same requested URL):

```
ReviewSourcesRows/receipts.jsonl:4   8bfaba248412fff8…
NoteTheme/receipts.jsonl:4           50c1ac253df17986…   <- credited by S094
ReopenS094/receipts.jsonl:2          6b355a468bfde1e3…
ReopenS094/receipts.jsonl:3          3b18a612e8288e58…
ReviewThemeUpstream/receipts.jsonl:13 de57cbaf2f46a581…
```

backgrounds tree: `2d22e126…` (ReviewSourcesRows:5), `9e1160a0…` (NoteTheme:16,
credited by S094), `267618a4…` (ReopenS094:4), `369f9439…`
(ReviewThemeUpstream:14) — 4 distinct 200 digests. Every record's `final_url`
is `github.com/omacom/omarchy/...` after the repo rename. The digest join is
what reaches S094: its row names no tree URL, only the tree digests.

## S097 over-fire found by the worktree run, and the arm removed

With the earlier path-tail join, the worktree run flagged **S097** — the
superseding row — because its anchor names `themes/matte-black tree` while
anchoring the tree by its git object id `3fc08f95…` and each file by a blob id.
No URL is credited there, so under L1's rule the row must not fire. The
path-tail arm was deleted (the digest arm already reaches S094), S097 now
prints `durable — sha256 over raw bytes at ref v3.8.4`, and S094 still flags
via `credited digest 50c1ac25…`. Fixture row S104 still exercises the exact-URL
arm.

## Fixture drill (`/tmp/anchor-fix`, git d30e102)

`MADO_LANE=/tmp/anchor-fix … HEAD` → exit 1, `FLAGGED S101 S104 S106`:

```
ROW S100 durable — sha256 over raw bytes at ref v1.2.3
ROW S101 UNPINNED_ALIAS — source path segment latest and anchor names no 40-hex commit, tag or dated version; also sha256 bbbbbbbb… is a page digest, not shown to rotate (receipts: 0 records, 0 digests)
ROW S102 durable — sha256 cccccccc… is a page digest, not shown to rotate (receipts: 0 records, 0 digests)
ROW S103 durable — alias segment main pinned by 40-hex commit 0123456789abcdef0123456789abcdef01234567
ROW S104 PER_FETCH_DIGEST — 2 distinct 200 digests for https://example.org/page.html (eeeeeeee… ≠ ffffffff…; matched by exact URL)
ROW S106 UNPINNED_ALIAS — source path segment latest and anchor names no 40-hex commit, tag or dated version
```

S106 (alias URL, access date only) proves the access-date exclusion; S101 shows
an alias flag with a non-rotating page digest; S104 shows rotation by exact
URL. The fixture receipts also hold a 403 record and a two-record
single-digest URL (`1×64`), which do not flag.

## CLI paths exercised (final bytes)

| Command | Result |
|---|---|
| `… 17661e0 --rows S001` | `ROW S001 durable`, `flagged=0`, exit 0 |
| `… 17661e0 --rows S094,S084` | both flagged, exit 1 |
| `…` (no args) | usage, exit 2 |
| `… 17661e0 --rows S999` | `could_not_evaluate: absent row S999`, exit 2 |
| `… 17661e0 --rows S007` | `skipped: S007 status=queued` + `--rows names no evaluated row`, exit 2 |
| `… 17661e0 --exclude-status rejected,queued` | `rows=80 statuses=not:queued,rejected`, same flags, exit 1 |
| `… 17661e0 --exclude-status rejected` | `rows=88`, adds queued rows; `ROW S007 durable — alias segment latest pinned by version 1.32.0`, exit 1 |
| `… 17661e0 --exclude-status rejected --rows S007` | `ROW S007 durable`, exit 0 |
| `… 17661e0 --exclude-status bogus` | `usage: bad status bogus`, exit 2 |
| `… deadbeef` | `could_not_evaluate: rev deadbeef`, exit 2 |
| run from `/tmp` with absolute path | byte-identical stdout to the lane-CWD run (`diff` empty) |

## Rule evolution this round

1. **Access dates** (CriticC1): `pin_token` skips a date preceded by
   accessed/opened/read/fetched; a publication/revision date remains a pin per
   `CORPUS.md:99-100` ("version, commit, or publication date"). S032–S035 now
   print `no assigned class fired; anchor dates the access, not a revision`.
2. **Coverage notes** (CriticC1): each page-digest reason states how many
   committed 200 records carry the digest and how many distinct digests that
   URL has, so the token never carries an unmeasured variance claim.
3. **Rotation-only** (L1): page digests without ≥2 distinct 200 digests are
   `durable` with the note above; only S094's tree digest remains
   `PER_FETCH_DIGEST`. Result at 9c54c56/17661e0: `FLAGGED S084 S094`.

## Judgements

- **S084** — the only flag at 17661e0 is the unpinned `latest` alias (R18-V4);
  its digest re-hashes in 6 committed records. Reported as UNPINNED_ALIAS with
  the digest note, not as rotation.
- **S094** — real rotation: 5 distinct 200 digests for the tree URL it credits.
  Flagged; the reason names the join (`credited digest 50c1ac25…`).
- **S063/S064** — now `durable` with `page digest, not shown to rotate
  (receipts: 1 records, 1 digests)`: each credited digest reproduces in its one
  committed receipt (`FetchBackfillR17/receipts.jsonl:4`, `:5`). The anchors
  still carry no commit/tag, so the rows remain supersession candidates, but
  they are not rotation defects and no longer print as such.
- **S097** — durable by content-addressed ids (tag commit, two tree ids,
  per-file blob ids, raw-file sha256); not joined by the path mention.

## Limits

- No web source was opened: every variance claim rests on commits (49 receipt
  files, all round-18; round-13/17 receipts are not committed).
- The digest join attributes a URL through the first receipt URL (sorted) that
  lists the digest; a byte-identical file served at two URLs reports one.
- UNPINNED_ALIAS pin detection is row-local: any 40-hex/tag/revision-date in
  the anchor clears an aliased row, even if the pin concerns another URL in a
  multi-URL row. A version quoted from page content is accepted as a tag pin.
- `durable` is the absence of the two assigned classes, not proof of
  durability; access-date-only rows say so in their reason.
- `--exclude-status` semantics are as documented above (flag present replaces
  the mined-only default); this is the reading of L1's "behaviour unchanged
  (mined only)" — default unchanged, flag widens.
- No green-state run against a committed REV: the green run used the `/tmp`
  copy of the worktree rows. After L1 commits them, re-run the single command
  above.
- The 11-cell parse checks only the column count, not cell enums; the fleet
  census owns that check.
- Nothing was run against `tools/mado-verify.sh`, the host, pacman, or any
  service.

## Files changed

- `.ufo/waves/round-19/anchor-durability.py` (new, 433 lines, sha256 above).
- `.ufo/waves/round-19/w1/reports/AnchorDurability.md` (this report).

## Installs

none.
