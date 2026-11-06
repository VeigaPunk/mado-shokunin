# R90MMutC2 — C2 receipt-presence: mutants the frozen expectation set does NOT kill

Seat `R90MMutC2`, wave `w1`, round mado-90 (hyaku 15, attempt 1). Lane
`/home/vgpnk/Projects/shokunin/mado-shokunin`. Base revision `5041acf99e27263872bf0441ad5f9d4316152605`.
Scratch `S=$HYAKU_SCRATCH/mado-r90/R90MMutC2` (`/fast/scratch/hyaku/mado-r90/R90MMutC2`), removed on exit.
**All runs below are DRAFT** (`--draft-check`, exit 3): no measurement, nothing written under
`/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-90/receipts/`, controls untouched.

Artifacts (sha256, before = after, nothing under test was edited):

| file | sha256 |
|---|---|
| `.ufo/waves/round-90/build/check-receipt-presence.c2.py` | `300e50290d4ba4be806177b85d72785d90f200361dbf87e16ab22781fec60f4e` |
| `.ufo/waves/round-90/controls/receipt-presence-set-r90.json` | `15c57903b26a780858da3de3cc8975d7e6b00c234d53b8c45fbd4b9741f3d0fd` |
| `.ufo/waves/round-90/controls/receipt-mutants-r90.json` | `1f9f9adf58bea8b151994b70286586d85f0d7f444b3c11adb903b4687c4f5892` |
| `.ufo/waves/round-90/w1/mutants-extra-c2-r90.json` (delivered) | `e6b1af5fb9daefc78dfefaf16211484cc86c4f283a6923a80948f64718c93b83` |

## Result

Of 19 probes written against the candidate, **17 survive the frozen expectation set** and are
delivered in `.ufo/waves/round-90/w1/mutants-extra-c2-r90.json` (17 mutants, same JSON shape as the
frozen file, every `find` occurs exactly once — the counter would abort with `SETUP_ERROR` otherwise,
and it did not).

- Frozen set + delivered mutants: `DRAFT_TARGET_MISSED … expectations=15 met=15 mutants=17 killed=0`
  (exit 3). The frozen set kills none of the 17; its 15 expectations all still pass under every mutant.
- Frozen set + the frozen 13 mutants (baseline control of the harness): `DRAFT_TARGET_MET … met=15
  killed=13` (exit 3), so the harness itself is sound and the 17 are genuine survivors, not a broken run.
- 12 of the 17 are killed by a fixture of **exactly the set's shape** (13 such fixtures below;
  scratch-only extension of the set, `met=28/28 killed=12`, exit 3).
- 5 of the 17 survive even that: their behaviour is not expressible in the current expectation schema.
  Each gets an extension argument below. That is the finding for the L1: PRED-C2's frozen instrument
  observes only `rc`, the missing-citation set, and `cited >= min_cited`.

## Surviving mutants

`file:line` are lines of the candidate `.ufo/waves/round-90/build/check-receipt-presence.c2.py`.

| id | point | defect modelled | frozen set | killing fixture (same shape) |
|---|---|---|---|---|
| E01 | 40 (`CITE`) | lookbehind loses `/`: a citation preceded by a path separator (`mado-shokunin/receipts/x.txt`, real text at `498855cb:LOG.md` line 318 was `W/receipts/cleanup-r85.json`) is counted | survived | **X1** |
| E02 | 40 (`CITE`) | trailing lookahead loses `-`: `receipts/census-end-r90.txt-old` is counted as `receipts/census-end-r90.txt` | survived | **X2** |
| E03 | 40 (`CITE`) | grammar widened with `png`: a screenshot name under `receipts/` is demanded as a receipt | survived | **X3** |
| E04 | 120 | untracked scan keeps no record-file filter: every untracked file's lines are read as records | survived | **X4** |
| E05 | 116 | untracked scan drops `--exclude-standard`: `.gitignore`d records are scanned | survived | **X5** |
| E06 | 133 | `present()` trusts any on-disk `quality/receipts/…` regardless of `--commit-path` | survived | **X6** |
| E07 | 126 | `--commit-path` keeps its trailing `/`, so a directory commit path matches nothing | survived | **X7** |
| E08 | 72 | a full `.ufo/waves/round-N/…` citation falls back to `quality/receipts/<basename>` | survived | **X8** |
| E09 | 78 | a `-r<k>` bare name is also resolved against the change round (suffix round must win alone) | survived | **X9** |
| E11 | 164 | `present=` never incremented (summary lies, `missing=`/rc stay right) | survived | extension **P1** |
| E12 | 156 | `records=` counts cited lines instead of record files | survived | extension **P2** |
| E13 | 59 | every miss reports `:0` instead of the hunk's new-file line | survived | extension **P3** |
| E14 | 129 | worktree `present()` consults `HEAD` instead of `--base`'s tree | survived | extension **P4** |
| E15 | 145 | rev mode never derives the round from the commit subject (`m = None`) | survived | extension **P5** |
| E16 | 39 (`RECORD_FILES`) | `corpus/lessons/[^/]+` → `.+`: a lesson nested in a subdirectory is scanned as a record | survived | **X10** |
| E17 | 80 | a bare receipt name is also accepted at the repository root | survived | **X11** |
| E19 | 41 (`SUFFIX`) | `-r<k>` recognised only for `.txt`/`.json`: `receipts/census-r89.csv` resolves against the change round | survived | **X13** |

Reproducing input for the killed ones is the fixture content itself (e.g. E01: added line
`` - provenance `mado-shokunin/receipts/ghost-r90.txt` `` in `SCORECARD.md`, `--round 90`,
`--commit-path SCORECARD.md`, the file absent → the check must exit 0 with `cited=0`; the mutant
exits 1 with `missing receipts/ghost-r90.txt`).

## Why the 5 survive the whole schema (extension arguments)

The counter can observe only three things (`quality/counters/c2-r90-receipt-presence.py`):
line 34 `MISS = ^missing (\S+) -> ` (the citation, never the resolved path, never `file:line`),
line 35 `SUMMARY = … cited=(\d+) …verdict=(OK|MISSING)`, and the rc (lines 79, 84). Lines 82 fix
`--base HEAD` for every fixture. Consequences, one per survivor:

- **P1 (E11, `present=`)** and **P2 (E12, `records=`)**: the summary regexp captures `cited` and
  `verdict` only; `present=`/`records=` are documented output (`--rev` docstring: `records=K cited=N
  present=P missing=M`) but asserted nowhere. Kraft a kill with `"expect_present"`/`"expect_records"`
  on a fixture (e.g. W1-carried: `present=1 records=1`) or on C88/C89 whose true values the labels
  would have to record. Until then a check that miscounts its own denominators is invisible.
- **P3 (E13, `file:line`)**: `MISS` stops at `->`, so the location half of the documented
  `missing <citation> -> <resolved> <file>:<line>` is unobserved. Kill with `"expect_location"` per
  expected miss (W1-style fixture: `SCORECARD.md:2`). A wrong line number sends a reader to the wrong
  record line — the defect rounds 88/89 were about precisely that kind of pointer.
- **P4 (E14, `--base` tree)** — the strongest of the five. Every fixture is scored with `--base HEAD`
  (counter line 82), and `build_fixture` makes the base commit `HEAD`, so `{base}:{p}` and `HEAD:{p}`
  are the same tree and the mutant is a no-op on the whole set. It is *not* a no-op in production:
  `--worktree --base <B>` is the declared use on a records change, and with the atomic mutation a
  file added in a commit made *after* B (or already present at HEAD only) is silently "carried" —
  exactly the D88/D89 defect the check exists to catch, reintroduced on the worktree path. Kill:
  a fixture field `"base_ref"` (the counter passes it instead of `HEAD`) plus a fixture whose base
  commit lacks the receipt and a second, later commit carries it; e.g. W2 with the receipt committed
  after B must still exit 1.
- **P5 (E15, subject-derived round)**: all four revision expectations come from lane commits whose
  bare citations all carry an `-r<NN>` suffix (`498855cb` cites `receipts/c1-measured-A-r88.txt`, …),
  so `candidates()` never falls through to `round_no` derived from the subject (candidate line
  145-147), and every fixture is scored with an explicit `--round`. Kill: a revision-mode expectation
  whose cite is bare without a suffix (`receipts/plain.txt` in a `round-88: …` commit), or a fixture
  mode without `--round`. As frozen, half of the documented round resolution (commit subject,
  docstring lines 15-17) is untested.

These five are **not** permission to change the contract; they are coverage findings against
PRED-C2-r90-v1 as frozen. Two further probes were written and are **not** delivered because the
frozen set already kills them: **E10** "only the first citation of a line is counted"
(`for m in CITE.finditer(text):` → `…[:1]`) is killed by **D88** (a line whose second citation is
the missing `receipts/harm-final-r88.txt`), and **E18** "full-path branch chosen by substring"
(`if not cite.startswith("receipts/")` → `if "receipts/" not in cite`) is killed by **D88** (a
present `.ufo/waves/round-88/receipts/…` citation stops resolving).

## Killing fixtures (same shape as `controls/receipt-presence-set-r90.json`)

Thirteen fixtures; each kills exactly one mutant in the scratch extension (X12 was built for E18 and
is kept as the positive full-path case; it kills nothing among the 17). Verified together with the
frozen 15 expectations: `expectations=28 met=28 mutants=17 killed=12` (exit 3). Append to
`"fixtures"` after the freeze decision; `id` must be unique.

```json
[
 {"id":"X1-slash-prefixed-path-not-a-citation","round":90,"base":{"SCORECARD.md":"# s\n"},
  "work":{"SCORECARD.md":"# s\n- provenance `mado-shokunin/receipts/ghost-r90.txt`\n"},
  "commit_paths":["SCORECARD.md"],"expect_rc":0,"expect_missing":[]},
 {"id":"X2-hyphen-continuation-not-a-receipt","round":90,"base":{"SCORECARD.md":"# s\n"},
  "work":{"SCORECARD.md":"# s\n- renamed `receipts/census-end-r90.txt-old`\n"},
  "commit_paths":["SCORECARD.md"],"expect_rc":0,"expect_missing":[]},
 {"id":"X3-png-not-a-receipt","round":90,"base":{"SCORECARD.md":"# s\n"},
  "work":{"SCORECARD.md":"# s\n- screenshot `.ufo/waves/round-90/receipts/shot-r90.png`\n"},
  "commit_paths":["SCORECARD.md"],"expect_rc":0,"expect_missing":[]},
 {"id":"X4-untracked-non-record-ignored","round":90,"base":{"SCORECARD.md":"# s\n"},
  "work":{"SCORECARD.md":"# s\n","notes.md":"# n\n- `receipts/ghost-r90.txt`\n"},
  "commit_paths":["SCORECARD.md"],"expect_rc":0,"expect_missing":[]},
 {"id":"X5-ignored-untracked-not-scanned","round":90,"base":{"SCORECARD.md":"# s\n",".gitignore":"corpus/knowledge/\n"},
  "work":{"corpus/knowledge/ignored.md":"# i\n- `receipts/ghost-r90.txt`\n"},
  "commit_paths":["SCORECARD.md"],"expect_rc":0,"expect_missing":[]},
 {"id":"X6-quality-on-disk-not-carried","round":90,"base":{"SCORECARD.md":"# s\n"},
  "work":{"SCORECARD.md":"# s\n- axis `quality/receipts/qr-r90.txt`\n","quality/receipts/qr-r90.txt":"q\n"},
  "commit_paths":["SCORECARD.md"],"expect_rc":1,"expect_missing":["quality/receipts/qr-r90.txt"]},
 {"id":"X7-commit-path-trailing-slash","round":90,"base":{"SCORECARD.md":"# s\n"},
  "work":{"SCORECARD.md":"# s\n- harm: `receipts/harm-final-r90.txt`\n",".ufo/waves/round-90/receipts/harm-final-r90.txt":"ok\n"},
  "commit_paths":["SCORECARD.md",".ufo/waves/round-90/receipts/"],"expect_rc":0,"expect_missing":[]},
 {"id":"X8-full-path-no-quality-fallback","round":90,"base":{"SCORECARD.md":"# s\n","quality/receipts/shared-r90.txt":"q\n"},
  "work":{"SCORECARD.md":"# s\n- `.ufo/waves/round-90/receipts/shared-r90.txt`\n"},
  "commit_paths":["SCORECARD.md"],"expect_rc":1,"expect_missing":[".ufo/waves/round-90/receipts/shared-r90.txt"]},
 {"id":"X9-suffix-round-wins","round":90,"base":{"LOG.md":"# l\n",".ufo/waves/round-90/receipts/ghost-r89.txt":"g\n"},
  "work":{"LOG.md":"# l\n- carried `receipts/ghost-r89.txt`\n"},
  "commit_paths":["LOG.md"],"expect_rc":1,"expect_missing":["receipts/ghost-r89.txt"]},
 {"id":"X10-nested-lesson-not-a-record","round":90,"base":{"SCORECARD.md":"# s\n"},
  "work":{"corpus/lessons/sub/deep.md":"# d\n- `receipts/ghost-r90.txt`\n"},
  "commit_paths":["SCORECARD.md"],"expect_rc":0,"expect_missing":[]},
 {"id":"X11-repo-root-not-a-receipt-home","round":90,"base":{"SCORECARD.md":"# s\n","harm-final-r90.txt":"x\n"},
  "work":{"SCORECARD.md":"# s\n- harm `receipts/harm-final-r90.txt`\n"},
  "commit_paths":["SCORECARD.md"],"expect_rc":1,"expect_missing":["receipts/harm-final-r90.txt"]},
 {"id":"X12-full-path-present","round":90,"base":{"LOG.md":"# l\n",".ufo/waves/round-90/receipts/kept-r90.txt":"k\n"},
  "work":{"LOG.md":"# l\n- `.ufo/waves/round-90/receipts/kept-r90.txt`\n"},
  "commit_paths":["LOG.md"],"expect_rc":0,"expect_missing":[]},
 {"id":"X13-suffixed-csv-name","round":90,"base":{"LOG.md":"# l\n",".ufo/waves/round-89/receipts/census-r89.csv":"c\n"},
  "work":{"LOG.md":"# l\n- carried `receipts/census-r89.csv`\n"},
  "commit_paths":["LOG.md"],"expect_rc":0,"expect_missing":[]}
]
```

Each was checked against the *pristine* candidate first: all 13 new expectations pass on the
unmutated check (`expect X1…X13 ok`, `met=28/28`), so they are expectations the check meets, not
fixtures that already fail. Then each was checked to kill its mutant (`mutant E01 killed by X1`,
`E02→X2`, `E03→X3`, `E04→X4`, `E05→X5`, `E06→X6`, `E07→X7`, `E08→X8`, `E09→X9`, `E16→X10`,
`E17→X11`, `E19→X13`).

## Verification ledger (every command run, with exit code)

All draft. `C` = `python3 -I quality/counters/c2-r90-receipt-presence.py --repo …/mado-shokunin --rev
master --base-rev master --set … --mutants … --expect-set-sha256 … --expect-mutants-sha256 …
--scratch-root $S/ctrN --draft-check …/build/check-receipt-presence.c2.py`.

| # | variants | stdout tail | exit |
|---|---|---|---|
| 1 | frozen set, frozen 13 mutants | `DRAFT_TARGET_MET expectations=15 met=15 defects_detected=2/2 mutants=13 killed=13 base_check=absent` | 3 |
| 2 | frozen set, 15 first probes | `DRAFT_TARGET_MISSED … met=15 mutants=15 killed=1` | 3 |
| 3 | frozen set, 16 probes | `DRAFT_TARGET_MISSED … met=15 mutants=16 killed=0` | 3 |
| 4 | scratch set+13 fixtures, 18 probes | `DRAFT_TARGET_MISSED … expectations=28 met=28 mutants=18 killed=13` | 3 |
| 5 | frozen set, 17 delivered mutants | `DRAFT_TARGET_MISSED … expectations=15 met=15 mutants=17 killed=0` | 3 |
| 6 | scratch set+13 fixtures, 17 delivered | `DRAFT_TARGET_MISSED … expectations=28 met=28 mutants=17 killed=12` | 3 |

Hash before and after all runs: candidate `300e5029…fec60f4e` (unchanged), set `15c57903…1f3d0fd`,
frozen mutants `1f9f9adf…4f5892`. Delivered file is byte-identical to the measured one (copied, then
re-hashed `e6b1af5f…c93b83`). No `git`/`jj` mutation ran; the only repo write is the delivered JSON.
No installs, no pacman, no host service touched, no oracle needed for this seat.

Defect check: scratch `S` was removed with `rm -rf` after the runs (report and mutants copied into
`w1/` first); no scratch remains on disk.
