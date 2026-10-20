# ReopenRejected — partial

Seat: MadoR19.ReopenRejected (scout, leaf). Target: the claim that S097/S098
supersede S094/S084 in place (only `status`/`used-by` moved), logged old→new in
`lessons/round-19.md` § Gate, with the two notes re-pointed at the new rows and
no other file still citing S084/S094 as current support. All facts below are
committed bytes at `01b80946d92b26370d3012a7da655d00dd135154` (abbrev `01b8094`)
against `9c54c56a6a7528675027b7f628f97a1b8d1b8e8d` (`9c54c56`); the worktree is
NOT authoritative right now — `git status --short` shows `SKILL.md`, both
`corpus/knowledge/*route-r18.md`, and (observed at the end) `corpus/SOURCES.md`
modified by other live seats, including a draft of the very fix below. Nothing
in the lane was edited by me; no git/jj write, no gate run.

## 1. Row-level contract — holds

Field-level diff of every registry row (`line.split('|')`, 13 cells per row):
exactly two rows differ between base and tip, and in each exactly cell[8]
(status) and cell[11] (used-by) changed; source, kind, tier, scope, anchor,
teaches, opened, recheck and the closing cell are byte-identical.

```text
S084 changed cells [8, 11]
  base: mined                          tip: rejected
  base: corpus/knowledge/walker-route-r18.md   tip: —
S094 changed cells [8, 11]
  base: mined                          tip: rejected
  base: corpus/knowledge/theme-route-r18.md    tip: —
rows differing: 2
```

Recheck cells still `on-release` for both, opened still `2026-10-20`. The full
difflib opcode listing of `corpus/SOURCES.md` base→tip is: two single-row
replacements (exactly the S084 and S094 rows), a three-row insert
(S096/S097/S098 together), and two non-row appends (the walker-provenance
block and the `Round 19` search note). No legend, header, or third row moved.
S094's `scope` cell keeps its "(the only theme on this host)" text and its
`anchor` cell keeps the per-fetch HTML digests: rule 2 forbids rewriting those
cells, and `rejected` + `used-by —` make the row non-crediting, so this is
contract-expected residue, not a defect.

Totals line in the lesson (`corpus/lessons/round-19.md:49-50`, "Rows 95 → 98
(A 88 → 91; mined 80 → 81; rejected 7 → 9)") recomputed from the cells:

```text
base (95, {'A': 88, 'C': 6, 'B': 1}, {'mined': 80, 'queued': 8, 'rejected': 7})
tip  (98, {'A': 91, 'C': 6, 'B': 1}, {'mined': 81, 'rejected': 9, 'queued': 8})
```

Exact match, including `queued 8 → 8`.

## 2. Old→new logging — holds

`corpus/lessons/round-19.md:45-50` states, for S084: status `mined` → `rejected`,
used-by `corpus/knowledge/walker-route-r18.md` → `—`, reason "superseded by
S098: unpinned `latest` alias, R18-V4"; for S094: status `mined` → `rejected`,
used-by `corpus/knowledge/theme-route-r18.md` → `—`, reason "superseded by S097:
per-fetch HTML digests, R18-V1"; then "Recheck cells unchanged." Each old string
equals the base cell and each new string equals the tip cell byte-for-byte
(including the em dash `—`, not `-`). The Gate block's two new-row lines
(`:42-43`) also match the rows' URL/anchor/digest fields.

## 3. Notes re-pointed — cites the new rows, but not cleanly (the break)

`corpus/knowledge/walker-route-r18.md:1` now opens the S084 position with
`S098 https://static.crates.io/crates/xdg/xdg-3.0.0.crate (src/base_directories.rs:446-457 find_config_file, :308-310/:321-323 XDG defaults; supersedes S084, round 19)`;
`corpus/knowledge/theme-route-r18.md:1` carries
`S097 (omarchy v3.8.4 themes/matte-black colors.toml + tag commit and git tree ids; supersedes S094, round 19)`.
The body corrections at `walker-route-r18.md:327` and `theme-route-r18.md:167`
say the head token "was replaced in place". It was not removed: the rejected id
survives on the same `source:` line inside the new token's parenthetical
(offsets 1529 / 491 of the two lines).

Consequence measured with the lane's own committed strict falsifier from round
18 (`.ufo/waves/round-18/token-join-check.py`; every `S\d{3,}` on a `source:`
line must be `mined` and have `used-by` naming the note — `SOURCE_TOKEN` at
`:63`, status gate at `:271`, used-by gate at `:277`):

```text
$ python3 -I .ufo/waves/round-18/token-join-check.py 9c54c56a6a7528675027b7f628f97a1b8d1b8e8d
NOTE corpus/knowledge/walker-route-r18.md … tokens=20 … gaps=0
NOTE corpus/knowledge/theme-route-r18.md  … tokens=4  … gaps=0
SUMMARY rev=9c54c56a… notes=2 tokens=24 unique=24 web=21 host=3 gaps=0
RESULT PASS                                                                   (exit 0)

$ python3 -I .ufo/waves/round-18/token-join-check.py 17661e0
SUMMARY rev=17661e0… notes=2 tokens=24 unique=24 web=21 host=3 gaps=0
RESULT PASS                                                                   (exit 0)

$ python3 -I .ufo/waves/round-18/token-join-check.py df84807d8fc49f5d8fb4ec3060859e5b1992084c
GAP  corpus/knowledge/walker-route-r18.md:1 S084 not-mined detail=status='rejected'
GAP  corpus/knowledge/theme-route-r18.md:1 S094 not-mined detail=status='rejected'
SUMMARY rev=df84807… notes=2 tokens=26 unique=26 web=21 host=3 gaps=2
RESULT FAIL                                                                   (exit 1)

$ python3 -I .ufo/waves/round-18/token-join-check.py 01b80946d92b26370d3012a7da655d00dd135154
NOTE corpus/knowledge/walker-route-r18.md source_lines=1 tokens=21 unique=21 web=18 host=2 gaps=1
NOTE corpus/knowledge/theme-route-r18.md  source_lines=1 tokens=5  unique=5  web=3  host=1 gaps=1
GAP  corpus/knowledge/walker-route-r18.md:1 S084 not-mined detail=status='rejected'
GAP  corpus/knowledge/theme-route-r18.md:1 S094 not-mined detail=status='rejected'
SUMMARY rev=01b80946… notes=2 tokens=26 unique=26 web=21 host=3 gaps=2
RESULT FAIL                                                                   (exit 1)
```

The regression lands with the supersession itself (`df84807`), not with the
later tip commit: the head lines each gained exactly one `S`-token (20→21 and
4→5) and that token is the rejected id. So the in-place edit satisfies "cite
S098/S097" but leaves the notes failing the lane's own join invariant; the
correction text's "replaced in place" is true of the span it names but not of
the line as read by that checker.

What notices it, and what does not:

- `python3 -I .ufo/waves/round-17/measure.py REV` (the declared C1/C2
  instrument) filters non-mined tokens in `mined_a()`, so C2 coverage is 6/6 at
  both revs and its `sources_ok` lists simply drop S084/S094 and add S098/S097:
  P3 `[S072..S091]` (20 ids, includes S084) → `[S072..S083, S085..S091, S098]`
  (20 ids); P5 `[S092, S093, S094, S095]` → `[S092, S093, S095, S097]`. The harm-watch
  enumeration at `SCORECARD.md:1141-1142` matches that filtered P3 list exactly
  (its P5 list omits the mined host row S095 — a separate one-row prose slip,
  not caused by the flip).
- No round-19 tool or the gate references `token-join-check` (`git grep` at the
  tip: only round-18 wave artifacts and reports), so the 443-selftest never
  sees this. `landed-check.sh`, `harm-watch.sh`, `gate-swap.sh` and
  `tools/mado-verify.sh` do not contain the name.

## 4. "No other file cites S084/S094 as current support" — holds, with one scope caveat

Full committed-tip census (`git grep -n "S084\|S094" 01b80946` outside
`.ufo/`), classified:

- the two registry rows themselves (`corpus/SOURCES.md:96`, `:106`, now
  `rejected` / `used-by —`), the new rows' `supersedes` annotations (`:109-110`)
  and the round-19 provenance prose (`:155`, `:299`, `:302`) — not credit;
- `corpus/knowledge/*route-r18.md:1` (the two residual tokens above) and their
  correction blocks (`:327`, `:158-167`) — annotation/history, but parsed as
  citations by the strict join;
- dated records: `corpus/lessons/round-18.md:22,64,74,79,88`,
  `corpus/lessons/round-18-verifier-spotcheck.md:58,105,117,120`,
  `corpus/lessons/round-19.md:16,17,42,43,45,47`, `corpus/QUALITY.md:178-180`,
  `SCORECARD.md:997,1028,1092,1093,1115`, `corpus/README.md:141` — all
  historical or supersede statements, none presents S084/S094 as live support;
- `SKILL.md:572` names both ids in the probe's contract-control column ("REV
  `17661e0…` must flag S094 PER_FETCH_DIGEST and S084 UNPINNED_ALIAS") — a dated
  control, not support.

Scope caveat [INFERENCE]: the flips are not entries in
`.ufo/waves/round-19/supersessions.json` (only `2.17.0` → `2.17.2`). Re-running
`supersede-sweep.py 01b8094 --ledger <synthetic S084→S098/S094→S097 ledger>`
classifies both notes `POINTED` (a line carrying old + new exists) yet also
returns `STALE SKILL.md` for each entry and exits 1 — i.e. criterion 28's sweep,
if extended to source-id supersessions, would flag `SKILL.md:572` while staying
blind to the head-line token that breaks the join, because it only requires
old and new to co-occur on one line.

## 5. The replacements are substantively right (so the verdict is partial, not a reject)

- S098: local `.ufo/waves/round-19/fetch/SrcS084/xdg-3.0.0.crate` sha256
  `2fb433233f2df9344722454bc7e96465c9d03bff9d77c248f9e7523fe79585b5` =
  `walker-v2.17.2-Cargo.lock:2708` checksum (lock receipt line 1, 200/70,247 B;
  crate receipt line 2, 200/15,821 B). Crate `Cargo.toml` version `3.0.0`;
  extracted `src/base_directories.rs:447-448` is the quoted
  "Searches `XDG_CONFIG_HOME` and then `XDG_CONFIG_DIRS`.",
  `:308-310` / `:321-323` are the defaults, `:757-777` is `read_file`;
  `walker-v2.17.2-src-config.rs:219` is the
  `xdg::BaseDirectories::with_prefix("walker").find_config_file(...)` call.
- S097: `curl -sSL https://api.github.com/repos/basecamp/omarchy/git/ref/tags/v3.8.4`
  (301 → `…/repositories/994093166/git/ref/tags/v3.8.4`, 200, 368 B, sha256
  `a503d17d…`, fetched_at 2026-10-20T15:07:13-03:00) gives object `8fcc9d60…`,
  type `commit` (lightweight). Tree drill: `themes` = `73b7b824…` (200, 5,451 B,
  sha256 `270c2d83…`) with 19 entries — the 19 payload dirs the row names;
  `themes/matte-black` = `3fc08f95…` (9 entries); `backgrounds` = `ff02c341…`,
  `btop.theme` = `c8cdcd02…`; raw `colors.toml` local bytes sha256
  `dbdd13a6…`, 461 B (receipt `.ufo/waves/round-19/fetch/SrcS094/receipts.jsonl:1`,
  200).
- S094's rejection ground independently recounted from committed receipts at
  `9c54c56`: 5 records, all HTTP 200, for
  `https://github.com/basecamp/omarchy/tree/v3.8.4/themes/matte-black`, 5
  distinct sha256 values (seats `MadoR18.ReviewSourcesRows`, `NoteTheme`,
  `ReopenS094` ×2, `ReviewThemeUpstream`).
- Re-running `anchor-durability.py` (my own runs, not the QUALITY claim): base
  `FLAGGED S084 S094`, `SUMMARY … flagged=2`, exit 1; tip `flagged=0`, exit 0;
  `--rows S097,S098` both `durable`; `df84807` default exit 0 — consistent with
  `corpus/QUALITY.md:178-180`.

## Limits

- Findings are computed from committed bytes; the worktree is concurrently
  edited (`git status --short`: `SKILL.md`, both `corpus/knowledge/*route-r18.md`
  modified), and I did not read those pending edits as target bytes.
- `token-join-check.py` is a round-18 artifact; it is committed at the tip and
  is the only lane checker that enforces the every-token join. No round-19
  gate/selftest or tool references it, so this defect is invisible to the
  declared C1/C2/C3 counters and to the 443-selftest.
- No gate or gate copy was run (host pause; selftest not needed for this item).
- S096 host-byte claims were not re-read (out of scope); docs.rs was not fetched
  (the replacement rests on the receipted crate and lock, which I did verify).
- The GitHub API redirect (`basecamp/omarchy` → `omacom/omarchy`) is a repo
  rename; the raw URLs cited by the rows still resolved (round-19 receipts).
  API bodies are checks, not anchors.
- Fetch receipts (curl only, bodies in `/tmp`): tag ref — url as above, status
  200 final, 368 B, sha256 `a503d17d…`, fetched_at 2026-10-20T15:07:13-03:00
  (first hop: 301, 232 B, sha256 `d1cf3d6c…`); tag tree — 200, 5,451 B, sha256
  `270c2d83…`, 2026-10-20T15:13:07-03:00; themes tree — 200, 5,006 B, sha256
  `97401916…`, 15:13:12; matte-black tree — 200, 2,656 B, sha256 `5772bc7c…`,
  15:13:19.

## Installs

none
