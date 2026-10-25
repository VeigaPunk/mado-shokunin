# ExecLesson — round-35 `## Mistakes` draft

Date: 2026-10-24. Scope: draft the round-35 lesson's `## Mistakes` rows — the four
routed defects of the round-34 closure plus one row produced by this round's own
work. Draft only; nothing appended to the lane corpus.

## Output

Draft written to `.ufo/waves/round-35/scratch/ExecLesson/draft.md` — five rows in
the round-34 lesson's row format (`class / evidence / captured-by / fix`).

## Rows and their evidence

| # | Routed defect | class | Primary evidence pointer | Captured-by | Fix status |
|---|---|---|---|---|---|
| 1 | Dead `1 <= len(words) <= 25` clause in `PRED-C1-r34-v1` | instrument | `corpus/lessons/round-34-verifier-spotcheck.md` routed defect 1; `.ufo/waves/round-34/w1/reports/MutC1Drop.md` M5 | r34 clause-drop mutation suite | Retired: `c1/clauses.json` `retired: r34-word-bound-1-25`; replacement `gate-quote-word-bound` live over a free-variable quote; failing case `controls/c1-quote-long.txt` (TARGET_MISSED, open_cites=1) |
| 2 | `S_ISLNK`/`O_NOFOLLOW` pair TOCTOU-only | instrument | `MutC1Drop.md` M2 — identical to baseline on all trees | r34 clause-drop mutation suite | Split: `S_ISLNK` walk load-bearing (`controls/c1-entry-symlink.txt` kills it); `o-nofollow-open` carries the single `not-load-bearing` declaration in `c1/clauses.json`; `PRED-C2-r35-v1` `toctou_declared=1` counts it; header `c1/count.py:59-61` records TOCTOU-only |
| 3 | `RevFrozenBlobs.md` stale tip label | ledger | `.ufo/waves/round-34/w1/reports/RevFrozenBlobs.md` (measured `fa7ba113`, labelled "lane tip"); real tip `dff394109f3cc3d851309ad7c67dd3b35b46adf2` | Closure's re-verification of all seven blobs at `dff3941` — conclusion stood, label wrong | Re-issued (not rewritten): `.ufo/waves/round-35/ledger/RevFrozenBlobs-r35.md`; `PRED-C2-r35-v1` `ledger_tip_ok` re-verifies each blob id at that revision |
| 4 | Merge-package stale id-remap base | id-space | `merge/mado/ID-REMAP.md` remap base "registry ends at S196" vs live S202; repeats S186–S189 URLs as S199/S200/S260 | None lane-side; filed L0 `ae2c52b82018904ad891c304ba023c846a19bd8e` (fleet `.ufo/l0-questions.md`, `mado \| round-34`), operator-routed | Not duplicated: lane keeps S203–S210 re-pointed by document; package ids (S309, S310, S321, S329, S330, S331, S334, S336) named at `.ufo/waves/round-35/registration.md:123-125`; L0 open |
| 5 | Explicit pipe clause subsumed by field count | instrument | `c1/count.py:109-115` `cells()` splits on `|` honouring no escape → any pipe adds a field → killed by `nf_ok = len(cs) == 11` at `c1/count.py:180` | `c1/clauses.json` `row-well-formed` `why` records the subsumption; literal-pipe failing case committed `controls/c1-row-extra-field.txt` (TARGET_MISSED) | Recorded not hidden: field count is the load-bearing clause; spec wording stands because the count implies it |

## Verification performed

- `c1/clauses.json`: `r34-word-bound-1-25` under `retired`; `o-nofollow-open` the
  sole `not-load-bearing` entry; `row-well-formed` `why` states the field count
  covers both literal and escaped pipe. Confirmed against committed JSON.
- `c1/count.py`: `cells()` is `line.split("|")` with no escape handling
  (lines 109–115); `nf_ok = len(cs) == 11` (line 180); the `ok` conjunction has no
  separate pipe scan (lines 185–196) — the redundancy is structural, not
  asserted.
- All nine live-clause control receipts read: each prints `verdict=TARGET_MISSED`
  `exit=1` (`controls/c1-*.txt`); `controls/c1-donothing.txt` prints
  `closed_entries=0 closed_rows=0 open_cites=8`.
- `.ufo/waves/round-35/ledger/RevFrozenBlobs-r35.md` names `dff3941...` as the
  round-34 tip and lists the same seven frozen paths with blob ids.
- Routed-defect source: `corpus/lessons/round-34-verifier-spotcheck.md` lines
  299–324 (defects 1–4 quoted; defect 5 — three open L0s — is operator-owned and
  out of lesson scope).
- L0 citation: commit `ae2c52b8...` per `round-34-verifier-spotcheck.md:239-242`
  (3 added lines, all `mado | round-34`); fleet `.ufo/l0-questions.md` round-34
  rows verified present at fleet root.

## Bounds

- Leaf member: no subagents dispatched (the labrat was not needed — every
  pointer was verifiable by direct read).
- Read-only sources: `round-34-verifier-spotcheck.md`, `MutC1Drop.md`,
  `RevFrozenBlobs.md`, fleet `.ufo/l0-questions.md` — none edited.
- Draft lives in scratch; the ScribeLesson seat owns the actual lesson append.
