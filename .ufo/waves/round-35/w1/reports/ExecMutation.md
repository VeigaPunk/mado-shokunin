# ExecMutation — S_ISLNK walk / O_NOFOLLOW mutation harness

Executor seat. Harness: `.ufo/waves/round-35/scratch/ExecMutation/` — copies of
`c1/count.py` (the committed file at `78c25892…` sha256 was never edited; all
mutants are scratch copies, py_compile-clean). Controls: every tree under
`.ufo/waves/round-35/controls/` — 11 directories (`golden` + 10 defect trees);
the `*.txt` siblings are committed receipts, not trees, and were excluded.

## Claim under test

> The S_ISLNK component walk is load-bearing; the open-time O_NOFOLLOW flag is
> TOCTOU-only and no static tree can kill it.

This is the r35 repair split declared in `registration.md` / `c1/clauses.json`
(reviewed in `w1/reports/ConnR34.md` §Defect 2): `entry-regular` (the walk,
`count.py:73-88`) names `c1-entry-symlink` as its failing control;
`o-nofollow-open` (`count.py:90`) is declared `not-load-bearing`.

## Mutants

| script | sha256 prefix | mutation |
|---|---|---|
| `baseline.py` | `78c25892` | unmodified copy |
| `mutantA.py`  | `24a81227` | **Mutant A** — component walk (lines 73–88) removed; `cur = root.joinpath(*parts)`; open+O_NOFOLLOW is the only remaining guard. Root-lstat and rel-path hygiene retained. |
| `mutantA1.py` | `5b11a25c` | S_ISLNK check only (lines 80–81) removed; S_ISDIR/S_ISREG/nlink checks retained — disambiguates "the S_ISLNK check" vs "the walk". |
| `mutantB.py`  | `b0dd0420` | **Mutant B** — `os.O_NOFOLLOW` removed from the open (line 90). |
| `mutantC.py`  | `7b11d11c` | A+B combined — walk removed and flag removed. |

Command per cell: `python3 -I <script> --root <control> --frozen ../../c1/frozen.json`.
Full transcript: `scratch/ExecMutation/results.tsv` (55 rows + 12 .txt noise rows).

## Results — verdicts

| control | baseline | mutantA | mutantA1 | mutantB | mutantC |
|---|---|---|---|---|---|
| golden              | MET 0 | MET 0 | MET 0 | MET 0 | MET 0 |
| c1-digest           | MISSED 1 | MISSED 1 | MISSED 1 | MISSED 1 | MISSED 1 |
| c1-donothing        | MISSED 1 | MISSED 1 | MISSED 1 | MISSED 1 | MISSED 1 |
| c1-entry-symlink    | MISSED 1 (2/7/1) | MISSED 1 (2/7/1) | MISSED 1 (2/7/1) | MISSED 1 (2/7/1) | MISSED 1 (2/7/1) |
| c1-quote-absent     | MISSED 1 | MISSED 1 | MISSED 1 | MISSED 1 | MISSED 1 |
| c1-quote-long       | MISSED 1 | MISSED 1 | MISSED 1 | MISSED 1 | MISSED 1 |
| c1-recheck-prose    | MISSED 1 | MISSED 1 | MISSED 1 | MISSED 1 | MISSED 1 |
| c1-row-duplicate    | MISSED 1 | MISSED 1 | MISSED 1 | MISSED 1 | MISSED 1 |
| c1-row-extra-field  | MISSED 1 | MISSED 1 | MISSED 1 | MISSED 1 | MISSED 1 |
| c1-status-queued    | MISSED 1 | MISSED 1 | MISSED 1 | MISSED 1 | MISSED 1 |
| c1-usedby-extra     | MISSED 1 | MISSED 1 | MISSED 1 | MISSED 1 | MISSED 1 |

**No mutant changes any control's verdict — including the counter values
(2/7/1) on the one symlink control.** All four mutants are silent at the
verdict level.

## Mechanism evidence — why c1-entry-symlink stays MISSED

Probe on `controls/c1-entry-symlink/corpus/knowledge/idle-lock-chain-armed-r14.md`
(symlink → `idle-lock-never-asked-r12.md`):

```
lstat mode: 0o120777  S_ISLNK: True  S_ISREG: False
open O_RDONLY|O_NOFOLLOW → OSError errno=40 (ELOOP)
open O_RDONLY            → OK, read 2078 bytes
target contains 'gate-quote: S205 ': False   (gate-quote count: 2, for S203/S204)
```

Three independent kills act on this static tree:

1. **O_NOFOLLOW open (count.py:90)** — fires `ELOOP` on the leaf symlink with no
   race involved. With the walk deleted (mutantA), the open alone still kills
   the entry path → identical MISSED.
2. **Walk leaf check** — under mutantA1 (S_ISLNK line removed), the symlink
   still fails `S_ISREG` at line 87; under mutantB it still fails the S_ISLNK
   line at 80. The `S_ISLNK` line itself is dead code on static trees: every
   case it rejects is also rejected by `S_ISDIR` (intermediate) or `S_ISREG`
   (leaf) two lines below.
3. **Predicate clause** — under mutantC (walk+flag both gone) the open follows
   the link and reads `never-asked-r12.md`'s 2078 bytes, but that file carries
   no `gate-quote: S205` line → the cite is still open. The control is
   overdetermined: it is simultaneously a symlink defect *and* a missing-quote
   defect for the same entry.

## Verdict on the claim

- **"The S_ISLNK walk is load-bearing" — NOT SUPPORTED by this control set.**
  The walk's removal (both readings: whole walk, or just the S_ISLNK check)
  changes no verdict. `c1-entry-symlink`, the control `clauses.json` names as
  the walk's failing case, is killed at least two other ways: the O_NOFOLLOW
  ELOOP and the missing S205 quote. `entry-regular` is still not
  differentially covered.
- **"O_NOFOLLOW is TOCTOU-only; no static tree can kill it" — REFUTED at the
  mechanism level, vacuously true at the verdict level.** The probe shows
  `open(O_NOFOLLOW)` raising `ELOOP` on the committed static symlink — a static
  tree does kill through it, whenever the walk is gone (mutantA vs mutantC on
  `c1-entry-symlink` differ in *which* clause fires, not in the verdict). Its
  `not-load-bearing` marking survives only because the walk redundantly covers
  the same tree — the two guards are mutually redundant on the controls, not
  independent.
- The pair is **redundant as a pair**: each alone suffices to kill the only
  symlink tree; both together also do; the predicate's missing-quote clause
  makes even the fully weakened mutantC a non-detector.

## Where the walk actually is uniquely load-bearing (gap, not tested)

Statically, the walk has exactly one coverage region nothing else covers:
**symlinked intermediate path components** (e.g. `corpus` or `fetch` itself a
symlink). O_NOFOLLOW guards only the final component; a mid-path symlink is
invisible to it. No committed control exercises this — `c1-entry-symlink`'s
link is a leaf. Likewise `st.st_nlink != 1` (hardlinks) and the mid-path
`S_ISDIR` check (regular file as directory) have no controls; under mutantA
both checks vanish silently. A walk-killing control needs a symlink at an
intermediate component — or a symlinked leaf whose target is a fully-closing
entry, which no current fixture provides.

## Artifacts

- `scratch/ExecMutation/{baseline,mutantA,mutantA1,mutantB,mutantC}.py` — copies
  of `c1/count.py` with the mutations above (committed file untouched).
- `scratch/ExecMutation/results.tsv` — raw matrix transcript (script, control,
  exit, stdout line).
- Probe transcript quoted verbatim above; rerunnable:
  `python3` heredoc against `controls/c1-entry-symlink/` as shown.
