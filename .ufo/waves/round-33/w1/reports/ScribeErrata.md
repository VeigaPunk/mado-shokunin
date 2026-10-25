# ScribeErrata — round-33 w1 seat report

Scope: draft `.ufo/waves/round-33/scratch/ScribeErrata/errata.md` covering the twelve routed
defects in `corpus/lessons/round-32-verifier-spotcheck.md`, one sentence each, landable this
round **without editing the filed round-32 report** (`.ufo/reports/round-32/mado.md` untouched —
verified: no write issued against it).

## Verification (re-executed at write time, not copied)

- **D3 sizes.** `git ls-tree -r -l f5910876` → `.ufo/waves/round-32/scratch/` = **554 blobs /
  11.6 MB** committed; `git show 48f9fe09 --name-status` → **130 deleted paths**, all under
  `round-32/scratch/`, byte-sum at `f5910876` = **2,854,907 B = 2.7 MB**. The report's
  "187 MB … committed" (report lines 70, 229) published the on-disk figure.
- **D9 hash.** `git cat-file -t 256222890d935212874a09751ff9b7869943c2d7` → `commit`;
  `25622288` → `fatal: Not a valid object name`. `SCORECARD.md:2070-2071` cite `25622288`;
  minimal unique short hash is `2562228`.
- **D10 omitted commits.** Both resolve: `b1b740d16875b91ac37546b2958d5b016db97c06`
  (id-collision guard) and `50e6a8f32bfaf0487b2762eb3b5c9f51ed54b75c` (ExecCollisionGuard
  report); report lines 4–6 list round-32 commits "in order" without either.
- **D2 timestamps.** `git log --format='%ad %cd'` for `91862344..d9ed3816`: `50e6a8f3` has
  committer time 20:05:38 — the timestamp the report calls "the data commit" — while the data
  commit `f5910876` was committed at 20:22:50 (~14m50s after `CriticC1Predicate.md` mtime
  20:08:00) and claims row `a551f71c` at 20:27:38 (~19 min later).
- **D8 budget.** `.ufo/watchdog.log:1196` `19:56:38 launch mado round=32 attempt=1`, `:1203`
  `20:33:30 complete` → **36m52s wall**, under `ROUND_MAXTIME=170m`; report line 270 says
  "~35 minutes over".
- **D5.** `ls .ufo/waves/round-32/c2/controls/` → only `c1-predicate-attack`; no K2 receipts.
- **D7.** `git status --porcelain` in the lane repo → exactly the five round-30 paths (3
  modified, 2 untracked), matching the spotcheck.
- **D1/D11.** `SCORECARD.md:2070` still carries "target met … `cited_entries=3`" with no
  appended correction; report line 52 carries "No quarantined row was appended".

## Output

- Draft: `.ufo/waves/round-33/scratch/ScribeErrata/errata.md` — twelve entries, D1–D12, one
  sentence each; every repair is an append, a new file, or a hygiene action. Named items all
  present: 187 MB vs 11.6 MB/2.7 MB (D3), `25622288` vs `256222890d935212874a09751ff9b7869943c2d7`
  (D9), omitted `b1b740d1` + `50e6a8f3` (D10), S189 cleared-then-adopted wording (D11), budget
  19:56:38→20:33:30 = 36m52s under 170m (D8).

## Limits

- The corrections themselves (SCORECARD/LOG appends, gate registry row, K2 receipts commit,
  round-30 leftover resolution) belong to other seats this round; this seat drafted wording only.
- Statuses shown by `git status` (`.ufo/waves/round-33/controls/*`, this report) are expected
  in-flight round-33 work, not defects.
