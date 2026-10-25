# RevLogEvidence — round-35 LOG.md evidence-pointer audit (w2)

Seat: reviewer, read-only. Scope: attack the round-35 `LOG.md` entries; open every
named file/line/hash and confirm it exists and says what the entry says; report
broken pointers with the exact path tried; confirm the LOG entry names the frozen
commit `19e4ab3` and the claim rows.

Lane root: `/home/vgpnk/Projects/shokunin/mado-shokunin`.
LSP: no `lsp` device is mounted in this seat, so callsite/semantic checks that would
normally go through a language server fell back to `grep`/`read`. Recorded, not
presented as semantic proof.
Installs: none (no pacman/uv/npm transaction was needed or run).

## Axes

1. Pointer resolvability (path exists, line exists, text says what is claimed).
2. Hash/identity integrity (sha256, blob ids, commit ids).
3. Claim-row presence (frozen commit `19e4ab3`; C1 `closed_entries=3 closed_rows=8
   open_cites=0`; C2 `uncovered=0 retired=1 toctou_declared=1 ledger_tip_ok=1`).
4. Internal consistency of the r35 blocks against committed round-35 evidence.

## Headline: the LOG entry the assignment asks about does not exist

`LOG.md` contains **two** round-35 blocks, both wave-1 seat-scratch notes, and **no**
round-35 claim entry:

- `LOG.md:1999-2014` — "Round 35 — SimplifyCounter seat scratch"
- `LOG.md:2016-2033` — "Round 35 — MutC1Drop seat scratch"

```
$ grep -c '19e4ab3' LOG.md
0            # exit 1 — no match
$ grep -c 'closed_entries=3' LOG.md
0            # exit 1 — no match
$ grep -c 'uncovered=0' LOG.md
0            # exit 1 — no match
$ grep -c 'toctou_declared' LOG.md
0            # exit 1 — no match
$ git show HEAD:LOG.md | grep -c 'Round 35'
0            # exit 0 — the freeze commit's LOG.md has no round-35 block at all
```

The 36 lines of the two scratch blocks are a **working-tree modification only**
(`git diff LOG.md` → `@@ -1995,3 +1995,39 @@`); at `19e4ab3` the file ends with the
round-34 entry. So:

- **Frozen commit `19e4ab3` named in the round-35 LOG entry: FAIL.** No r35 block
  names any commit. The only "untouched" claim (`LOG.md:2004`) is a statement about
  the counter, not a freeze pin.
- **Claim rows named in the round-35 LOG entry: FAIL.** Neither `closed_entries=3`
  nor `uncovered=0`/`retired=1`/`toctou_declared=1`/`ledger_tip_ok=1` appears
  anywhere in `LOG.md`.

The only artifact that carries a round-35 narrative entry is the unpublished draft
`.ufo/waves/round-35/scratch/ScribeLog/draft.md` (64 lines, not in `LOG.md`). It does
name the freeze (`draft.md:10`, `19e4ab3171c1540c40d6b12097745af98053b07d`) but its
C1 claim row is an unfilled placeholder (`draft.md:24`, `[<data commit hash here>]`)
and its wave-count row is `[<settled counts at closure …>]` (`draft.md:51`). Nothing
in `LOG.md` can be confirmed against the two claim rows until that entry is written
and the data commit exists.

Verified current claim values, for the closure text:

```
$ python3 -I .ufo/waves/round-35/c1/count.py --root . --frozen .ufo/waves/round-35/c1/frozen.json
PRED-C1-r35-v1 closed_entries=3 closed_rows=8 open_cites=0 verdict=TARGET_MET
exit=0
$ python3 -I .ufo/waves/round-35/c2/count.py --repo . --frozen .ufo/waves/round-35/c2/frozen.json
PRED-C2-r35-v1 uncovered=0 retired=1 toctou_declared=1 ledger_tip_ok=1 verdict=TARGET_MET
exit=0
```

Caveat the LOG must carry: C1 currently passes only because the three entries and the
eight `corpus/SOURCES.md` rows live in the **uncommitted** worktree
(`git status --porcelain` → `?? corpus/knowledge/idle-lock-*.md` ×3, ` M
corpus/SOURCES.md`; registry count `grep -c '^| S[0-9]' corpus/SOURCES.md` → `200`).
There is no data commit hash for the LOG to name yet.

## Pointer audit — zero broken pointers, three imprecise ones

Every file/hash named by the two existing r35 blocks resolves:

| Entry | Pointer | Command run | Result |
|---|---|---|---|
| SimplifyCounter | `.ufo/waves/round-35/c1/count.py` | `wc -l`, `sha256sum` | 218 lines; `78c2589286a2d70c9b109672c85cd4e9bcb85438bc80ab888d10b73ad12abad6` |
| SimplifyCounter | `PRED-C1-r35-v1` | `grep -n PRED-C1-r35-v1 c1/count.py` | present at :2, :6, :34, :52, :211 |
| SimplifyCounter | `scratch/SimplifyCounter/count-min.py` | `wc -l` | 104 lines (`104 vs 218` accurate) |
| SimplifyCounter | `scratch/SimplifyCounter/analysis.md` | `ls -la` | present, 4755 B |
| SimplifyCounter | `controls/golden` + ten c1 trees | `ls controls/` | 11 dirs: `golden` + 10 `c1-*` (`ten` accurate) |
| SimplifyCounter | "tampered and missing `--frozen` both exit 2" | tampered copy in scratch; nonexistent path | `error=predicate-drift` exit 2; `error=frozen-missing` exit 2 |
| SimplifyCounter | `.ufo/waves/round-35/w1/reports/SimplifyCounter.md` | `wc -l` | present, 54 lines |
| MutC1Drop | `scratch/MutC1Drop/mutants/` (15) | `ls \| wc -l` | 15 files `m01..m15` |
| MutC1Drop | `gen_and_run.py` | `ls -la` | present, 10137 B |
| MutC1Drop | "all 11 frozen control trees" | `results.json` | baseline has 11 keys; every mutant has 11 runs |
| MutC1Drop | "Baseline reproduced all committed `.txt` receipts" | field compare of 11 baseline runs vs `controls/<tree>.txt` | 0 mismatches (rc + stdout line) |
| MutC1Drop | `sha256 78c25892…d12abad6` | `sha256sum c1/count.py` | exact match; `git status --porcelain .ufo/waves/round-35/c1/` → 0 lines (untouched) |
| MutC1Drop | seven verdict-live 1:1 conjuncts | recomputed flips from `results.json` | m02→row-duplicate, m04→usedby-extra, m05→status-queued, m06→recheck-prose, m07→digest, m09→quote-long, m10→quote-absent; each flips exactly one tree and its rc; no cross-kills |
| MutC1Drop | dead list (`row-well-formed`, `entry-regular`, `blob is not None`, `st_nlink != 1`, `entry_closed`, `S_ISLNK` walk, `O_NOFOLLOW`) | recomputed flips | m01, m03, m08, m11, m12, m13, m14, m15 all zero verdict flips |
| MutC1Drop | "`quote is not None` … counter-live on `c1-entry-symlink` (8/0 vs 7/1)" | re-ran committed counter and `m08-quote-exists.py` | baseline `closed_entries=2 closed_rows=7 open_cites=1`; m08 `closed_entries=2 closed_rows=8 open_cites=0` — claim correct |
| MutC1Drop | `.ufo/waves/round-35/w1/reports/MutC1Drop.md` | `wc -l` | present, 102 lines |

Imprecise pointers (not false claims, but not literally resolvable as written):

- **`LOG.md:2006` "gave 21/21 identical stdout/exit pairs" — not reproducible.**
  I re-ran the full differential matrix (committed `c1/count.py` vs
  `scratch/SimplifyCounter/count-min.py`, same `--frozen`, over every
  `controls/*/`, every `controls/*.txt`, and `--root .`):

  ```
  $ .ufo/waves/round-35/scratch/RevLogEvidence/diffcheck.sh
  ...
  TOTAL n=24 same=24 diff=0
  exit=0
  ```

  24 legs were run and all 24 agree (`controls/` holds 11 dirs and 12 `.txt`), so
  the equivalence is stronger than claimed but **21 is not the cardinality of the
  set as described**. 21 is reachable only by counting 11 dirs + 10 `c1-*.txt` and
  silently dropping `--root .` (and `golden.txt`/`c2-donothing.txt`). The LOG
  sentence should either say 24/24 or state the subset. Fixed evidence:
  `.ufo/waves/round-35/scratch/RevLogEvidence/diffcheck.out`.
- **`LOG.md:2011` `c1/clauses.json` and `LOG.md:2005` `controls/golden` do not
  resolve from the lane root** (`test -e c1/clauses.json` → MISS;
  `test -e controls/golden` → MISS). They resolve only under
  `.ufo/waves/round-35/` (both OK). Given the preceding absolute path this is
  readable shorthand, but the entry should prefix the round-35 root once.
- **`LOG.md:2002` "the nine live clauses" vs the ledger's own field.** `clauses.json`
  has `live` = **10** objects (9 with a named control + `o-nofollow-open` carrying
  `not-load-bearing`), `retired` = 1. "Nine" counts load-bearing seats, not the
  ledger's `live` list. One-word fix: "nine load-bearing clauses (ten live)".

## Substantive finding the pending LOG entry would import

The unpublished draft's C2 justification says:

> the `S_ISLNK` component walk stays load-bearing (`c1-entry-symlink` kills it)
> — `scratch/ScribeLog/draft.md:41-42`

That is **falsified by committed round-35 evidence**:

```
$ python3 -I .ufo/waves/round-35/scratch/MutC1Drop/mutants/m13-sislnk-walk.py \
    --root .ufo/waves/round-35/controls/c1-entry-symlink \
    --frozen .ufo/waves/round-35/c1/frozen.json
PRED-C1-r35-v1 closed_entries=2 closed_rows=7 open_cites=1 verdict=TARGET_MISSED
exit=1                      # identical to baseline and to m11
```

`results.json` agrees (`m13-sislnk-walk` → `flip=false` on all 11 trees; `m11` too).
`LOG.md:2029` in the MutC1Drop block already states the walk is masked
("S_ISLNK walk (masked by S_ISREG+O_NOFOLLOW for leaf links)"). `SCORECARD.md:2154`
also already recorded the pair as "redundant against every static tree
(TOCTOU-only)". If `draft.md` lands verbatim, the round-35 LOG entry would
contradict a round-35 LOG block committed in the same file.

Corollary for the C2 claim row: `toctou_declared=1` is satisfied by exactly one
declaration (`o-nofollow-open`; `c2/frozen.json` `toctou_clause` = `o-nofollow-open`),
while the frozen C2 predicate (`c2/count.py:17-18`, mirrored at :43-44) describes
"the S_ISLNK/O_NOFOLLOW pair" as never counted load-bearing. `entry-regular` — the clause that contains the S_ISLNK walk — stays in
`live` with `control: controls/c1-entry-symlink`, and `uncovered=0` is satisfied
because the **receipt** records `TARGET_MISSED`, not because dropping the clause
changes the verdict. Under the frozen definition `uncovered=0` is true; as prose it
must not be published as "nine clauses covered", because m03 (`row-well-formed`) and
m11 (`entry-regular`) are verdict-dead. This is the exact defect `LOG.md:2025-2027`
already reports for C1; the C2 row must not contradict it.

## Severity list

- **HIGH** — No round-35 claim entry in `LOG.md`; the frozen commit `19e4ab3` and both
  claim rows are absent from the file (`grep` counts 0). The two r35 blocks are
  uncommitted wave-1 seat scratch. Assignment's two explicit confirmations: FAIL.
- **HIGH** — The only drafted entry (`scratch/ScribeLog/draft.md`) cannot supply the
  C1 claim row: `[<data commit hash here>]` placeholder (`draft.md:24`); the data is
  worktree-only (3 untracked entries, modified `SOURCES.md`, registry 200 rows).
- **MEDIUM** — `draft.md:33-34` "S_ISLNK walk stays load-bearing (`c1-entry-symlink`
  kills it)" is false; m13/m11 and `results.json` show it dead. Adopting the draft
  verbatim imports a false clause into `LOG.md` and contradicts `LOG.md:2029`.
- **LOW** — `LOG.md:2006` "21/21" is not the reproducible cardinality; the re-run
  matrix is 24/24 SAME (`diffcheck.out`).
- **LOW** — `LOG.md:2002` "nine live clauses" vs `clauses.json` `live`=10,
  `retired`=1, `not-load-bearing`=1.
- **LOW** — `LOG.md:2005,2011` bare `controls/golden` / `c1/clauses.json` do not
  resolve from the lane root (MISS); they resolve only under `.ufo/waves/round-35/`.
- **LOW** — `w1/reports/ScribeLog.md` cites `.ufo/waves/round-35/seat-plan.tsv` as
  wave-dispatch evidence; that path is **MISSING**. `dispatch.out`
  ("launching 64 seats concurrently"), `w1-taskcall.json` (`counts.spawn=64`), and
  `w1-spec.json` do exist and agree on 64.
- **INFO** — `LOG.md`'s `--root .` differential was pre-data (`open_cites=8`); the same
  run today is `TARGET_MET` because the data is in the worktree. Identity between the
  two counters still holds either way (24/24 SAME). Not a false statement, but the
  LOG must not quote the pre-data root verdict as current.

## Residual risk / verification gaps

- The entry that the assignment asks me to confirm simply does not exist; I verified
  its absence three ways (`grep` in worktree, `git show HEAD:LOG.md`, `git diff`).
  What exists instead is an unpublished draft with two unfilled placeholders, so the
  claim rows are **unverified in `LOG.md`, not merely unquoted**.
- The C1 claim is currently only worktree-true. Re-checking it after the data commit
  lands will require re-running `c1/count.py` at that commit; the LOG must carry that
  command and exit code, not the worktree result.
- No language server was available in this seat; the audit is textual (`grep`, `read`,
  `git`, `wc`, `sha256sum`) plus executed counters/mutants. No claim above rests on
  grep alone where an executable check existed — every counter/mutant statement has a
  quoted command and exit code.

## Files

- Scratch evidence: `.ufo/waves/round-35/scratch/RevLogEvidence/`
  (`diffcheck.sh`, `diffcheck.out`, `frozen-tampered.json`).
- Lane files read (not modified): `LOG.md`, `corpus/SOURCES.md`,
  `.ufo/waves/round-35/{registration.md,c1/*,c2/*,controls/*,fetch/*,ledger/*,
  w1/reports/{SimplifyCounter.md,MutC1Drop.md,ScribeLog.md},
  scratch/{SimplifyCounter/*,MutC1Drop/*,ScribeLog/draft.md}}`, `SCORECARD.md`.
