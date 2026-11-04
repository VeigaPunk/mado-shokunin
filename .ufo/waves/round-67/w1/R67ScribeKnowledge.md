# R67ScribeKnowledge — knowledge entry + index/SOURCES rows (round 67, w1)

Seat: R67ScribeKnowledge. Lane: `/home/vgpnk/Projects/shokunin/mado-shokunin`.
Axes: C1 calibration, C2 operability. This seat is evidence for C2 (replacement-ref
semantics), not a third claim and not a score. No production file written; no git
mutation in the lane, the fleet repo or any sibling lane.

## Deliverables

| path (relative to lane) | bytes | sha256 |
|---|---|---|
| `.ufo/waves/round-67/w1/R67ScribeKnowledge/draft/corpus/knowledge/replace-ref-citation-boundaries-r67.md` | 16916 | `a049be86119683dc086b608dcd04ddbe4d21c9310cf19032ec13db6e11736f34` |
| `.ufo/waves/round-67/w1/R67ScribeKnowledge/draft/corpus/README-row.txt` | 1659 | `15f6bb2dbda386b0521f2d25a2814f27ffcf969a6183b82b006e5ac2f6cddc79` |
| `.ufo/waves/round-67/w1/R67ScribeKnowledge/draft/corpus/SOURCES-row.txt` | 983 | `b6e794cc19648d98f9d3f4d35e8dff3882a1856ae33fb3d07335207f6d2adbde` |
| `.ufo/waves/round-67/w1/R67ScribeKnowledge/receipts/host-replace-fixtures.txt` | 9008 | `aed653f113e6712976ab4de0ebce85eb32201a1faeca5605b8bf9ba601040ee2` |

Entry: 189 lines; header order `source:` / `verified-at:` / `recheck:` verified at
lines 1-3. Labels: `MADO-R67-1` in the title and in the index row.

## S436 (source row facts)

- id: `S436` (registry max at freeze was `S435`, 372 ids, no duplicate; no `S436`
  present), computed from `corpus/SOURCES.md`.
- URL: `https://raw.githubusercontent.com/git/git/v2.56.0/Documentation/git-replace.adoc`
  (pinned to tag `v2.56.0`; host `git --version` = `git version 2.56.0`).
- Access date: `2026-11-03` (host local date; the run's UTC clock read
  `2026-11-04T00:36Z` — the lane's opened date follows local).
- Fetch: `curl -fsSL -o git-replace.adoc <URL>` → rc 0.
- sha256 of fetched bytes:
  `3f61be3f0ea0426cf1e075929819b9a6bce240c6955cfd25d99fb2c974640631`
  (5398 bytes, 168 lines). Independently re-fetched by R67ScoutSources with the
  same hash.
- Hero quote (21 words, `DESCRIPTION` lines 34-36): "Replacement references will
  be used by default by all Git commands except those doing reachability
  traversal (prune, pack transfer and fsck)."
- Second quote (16 words, lines 55-56): "The `GIT_NO_REPLACE_OBJECTS` environment
  variable can be set to achieve the same effect as the `--no-replace-objects`
  option."
- Screening: screened 1, included 1, rejected 0; no reject candidate and no flip
  row this round.
- kind `docs`, tier `A`, status `mined`, recheck `on-release`, used-by
  `corpus/lessons/round-67.md, corpus/knowledge/replace-ref-citation-boundaries-r67.md`.

## Row texts

SOURCES row (`draft/corpus/SOURCES-row.txt`, 11 cells, no literal or escaped pipe):

```
| S436 | git v2.56.0 Documentation — git-replace.adoc — https://raw.githubusercontent.com/git/git/v2.56.0/Documentation/git-replace.adoc | docs | A | lane-instrument object reads: what a refs/replace entry rewrites on git 2.56.0 (blob, tree and commit levels) and how a git child reads the real objects | DESCRIPTION + BUGS + CAVEATS, git-replace.adoc:20,22-24,26-27,29,31-32,34-36,38-39,55-56,151-153 @ tag v2.56.0 (git 2.56.0 host; fetched 2026-11-03, sha256 3f61be3f0ea0426cf1e075929819b9a6bce240c6955cfd25d99fb2c974640631, 5398 bytes) | "Replacement references will be used by default by all Git commands except those doing reachability traversal (prune, pack transfer and fsck)."; the replace ref is named for the replaced object with the replacement oid as content; --no-replace-objects and GIT_NO_REPLACE_OBJECTS make a command read the real objects | mined | 2026-11-03 | on-release | corpus/lessons/round-67.md, corpus/knowledge/replace-ref-citation-boundaries-r67.md |
```

README row (`draft/corpus/README-row.txt`, 3 cells, first cell a backticked
`knowledge/....md` path). Insertion point: immediately after the last
`` | `knowledge/...` `` row of the coverage-map table — line 89 at the freeze
(`knowledge/windows-displayconfig-r63.md`), before `## Quality bar`. Appending at
EOF lands outside the map and is read as `row-outside-map`.

```
| `knowledge/replace-ref-citation-boundaries-r67.md` (MADO-R67-1, round 67; lane tooling, git replacement refs) | What a `refs/replace` entry does to a lane git reader on the host's git 2.56.0, measured in scratch fixtures: at blob level, `cat-file`/`show` return the replacement's bytes while `ls-tree` still prints the stored original oid and `rev-parse <rev>:<path>` that same oid (listing and bytes disagree); at tree and commit level the replacement rewrites the listing and path resolution too (finding **F01** — "ls-tree ids are not rewritten" holds only for a replaced blob whose enclosing tree/commit is untouched); `GIT_NO_REPLACE_OBJECTS` is read for presence (unset reads forged; `1`, `0`, empty, `true`, `false` all read real) and `--no-replace-objects` agrees; the guard ignores but does not hide the ref (`for-each-ref refs/replace` still lists it). Census at freeze `061dc329`: 82 files under `quality/` and `tools/` mention a git command, 79 contain `show` or `cat-file`, 3 set the guard, with the standing instrument's four legs and the two C1 register counters tabulated by read shape and guard state. States what the round's C2 R control proves (a planted replacement does not move the used-by child's real verdict; deleting the added guard key line makes the mutant read the forged view) and what it does not (no protection against a repo already rewritten, no authenticity, no state-cell truth, no universal fault coverage, no detection, no clone/fetch arrival claim). | `source:` S436 in [SOURCES](SOURCES.md); host fixture receipt `.ufo/waves/round-67/w1/R67ScribeKnowledge/receipts/host-replace-fixtures.txt`; recheck on-release. |
```

## What the entry establishes

1. **Blob-level replacement** (the C2/R and r55 shape): `cat-file -p <orig>` and
   `show HEAD:f.txt` return the replacement's bytes; `ls-tree HEAD` still prints
   the stored original blob oid and `rev-parse HEAD:f.txt` that same oid.
2. **Tree/commit-level replacement**: `ls-tree -r` and `rev-parse <rev>:<path>` /
   `^{tree}` follow the replacement; the guard restores both. Finding **F01**
   records that the seat brief's "not ls-tree object ids" sentence is true only
   for a replaced blob whose enclosing tree/commit is untouched. The independent
   scout (R67ScoutSources) measured the same and sent a correction; the entry
   carries the measured two-level rule, not the brief's sentence.
3. **Guard semantics**: presence, not truthiness — unset reads forged; `1`, `0`,
   empty, `true`, `false` all read real. `--no-replace-objects` works in both
   positions on 2.56.0; `core.useReplaceRefs=false` also disables and a repo
   config cannot re-enable against the process guard.
4. **Guard ignores, does not hide**: `for-each-ref refs/replace` and `git replace -l`
   still enumerate the plant under `GIT_NO_REPLACE_OBJECTS=1`.
5. **Name resolution untouched**: `rev-parse HEAD` returns the same commit oid in
   both modes — a printed revision can be right while the bytes read under it are
   not.
6. **Lane census at `061dc329`**: 82 files under `quality/` + `tools/` mention a
   git command, 79 contain `show`/`cat-file`, 3 set the guard
   (`quality/landing-counters.sh`, `quality/counters/c1-r66-register.py`,
   `quality/counters/c1-r56-autoreload-entry.py`). The standing instrument's four
   legs and the two register counters are tabulated by read shape and guard state;
   the children build env from scratch, so the parent `export` does not reach
   them (matching `BASELINE_C2 usedby_guard=0 ledger_guard=0`).
7. **R scope**: proves the planted replacement does not move the used-by child's
   real `TARGET_MISSED` verdict and that deleting the added guard key line makes
   the mutant read the forged view; does not prove protection against a repo
   already rewritten, authenticity, state-cell truth, universal fault coverage,
   detection/reporting, or how a replacement ref arrives via clone/fetch.

## Commands and exit codes

- `curl -fsSL -o git-replace.adoc https://raw.githubusercontent.com/git/git/v2.56.0/Documentation/git-replace.adoc` → rc 0, 5398 bytes.
- `sha256sum git-replace.adoc` → rc 0, `3f61be3f…40631`.
- `bash /fast/scratch/hyaku/mado-r67/R67ScribeKnowledge/receipt.sh` → rc 0, fixture receipt (blob/tree/commit, env forms, config plane, enumeration, census, leg source lines).
- `bash …/check107.sh` (fixture repo: real `corpus/SOURCES.md` + the S436 row + the entry) → rc 0, `CHECK107: rows=8 covered=8 miss=0 verdict=OK` (all rows `eof=unchecked`, no `pin`).
- `python3 -I quality/check-index-rows.py --root tree2` (full corpus copy, symlinked `tools/` and `.ufo/`, row inserted after line 89) → rc 0, `MADO_INDEX_ROWS: root=tree2 rows=79 errors=0 warns=0`.
- `python3 -I quality/check-index.py --root tree2` → rc 0, `MADO_INDEX: root=tree2 indexed=79/79 missing=0 dangling=0 duplicates=0 coverage=10.0000/10`.
- Census (lane root, read-only): `git grep -l -E '(^|[^A-Za-z0-9_-])git([^A-Za-z0-9_-]|$)' 061dc329 -- quality tools | wc -l` → 82; the same shape with `(show|cat-file)` → 79; `git grep -l GIT_NO_REPLACE_OBJECTS 061dc329 -- quality tools` → 3 files, listed above.

Scratch: `/fast/scratch/hyaku/mado-r67/R67ScribeKnowledge/` removed before yield
(fixtures, scripts, `tree`, `tree2`, `work107`); the receipt file lives in the seat
directory, not scratch. No tool installed or upgraded; no pacman transaction; no
service touched.

## Handoff (integration requirements)

1. Append `SOURCES-row.txt` verbatim at the registry tail (it is `S436`; keep the
   11-cell shape and the anchor locator list that criterion 107 reads).
2. Insert `README-row.txt` after line 89 of `corpus/README.md` (the last map-table
   row), not at EOF.
3. Commit `receipts/host-replace-fixtures.txt` with the seat directory: the note
   and the index row cite it, and a judged revision without it turns that pointer
   into a missing cited path. The draft note is at
   `draft/corpus/knowledge/replace-ref-citation-boundaries-r67.md`.
4. The entry is C2 evidence only; it makes no C1 claim and no desktop claim.

## Out of scope / not done

- No edit to `corpus/SOURCES.md`, `corpus/README.md`, `corpus/knowledge/` or any
  production path; no commit, push, stage or checkout; no lane/fleet git mutation.
- No desktop/compositor/session/service probe (none named for this seat).
- No second source opened; no rejected row, so no flip row for `R67ScribeLesson`.
- The 76 unguarded files in the lexical content-reader set are named as a residual,
  not repaired.
