# ScrErrata — round-46 w1 seat report

Seat: `ScrErrata` (leaf). Lane `mado-shokunin`, round-46 freeze `8c5434c60e03f147ee1f75ab195e8bc3f0db4dec`, lane tip at write
`e0be61e4f6e34896f8b1c329f9c6d129e5af81f7`. Read-only seat: no commit, no product code, no counter/fixture/control/pin/registration
edit, no host or compositor read, no tool installed.

## Deliverable

`.ufo/waves/round-46/w1/ScrErrata/errata.md` — three parts:

- **Part A, append-ready SCORECARD block**: **six errata, E1-E6, one per round-44 `w2/ConnCalibration.md` finding** (F1, F2, F3,
  F4, F5, F6 — numbered in finding order, one-to-one with E1-E6). Each names what it attacks (`path:line`), the command that shows the truth and its
  output, and the reading the L1 should append. Nothing above is rewritten; no earlier line of `SCORECARD.md`, `LOG.md`, the round-44
  lesson, `SKILL.md` or `QUALITY.md` is edited.
- **Part B, the D4 note** (round-45 closure `:114`): digest line for `.ufo/waves/round-45/w1/MutC1Counter/results.json` — sha256,
  size, what `summary.txt` holds — with the file itself kept out of git.
- **Part C, the D5 note** (round-45 closure `:116`): `.ufo/waves/round-45/w1-results.json` holds `output: null` for all 41 seats; the
  41 committed seat `.md` files are the record.

## The six errata (what each one changes)

| # | finding | subject | ruling |
|---|---|---|---|
| E1 | F1 | `LOG.md:2499` says `Mistakes M44-1..7`, the lesson holds nine | stands; read as the protocol-load count; closed range cited from `SCORECARD.md:2583` |
| E2 | F2 | the lesson / `id-guard.md:8` cite `assimilation/renumber-map.tsv` | **withdrawn as stated**: the map is committed at `.ufo/waves/round-44/assimilation/renumber-map.tsv`, blob `c9639ce8…`, added in freeze `e2289516`; the citation is wave-relative, so the [MEDIUM] reduces to a path-prefix ambiguity |
| E3 | F3 | `SKILL.md:295-301` carries `clients=4` next to round-44 rows | **reclassified**: both counts are true and belong to different runs (round-43 receipt `:10` = 4; round-44 receipt `:5` = 3); the paragraph is unchanged from base `6a1a905` (`:284`/`:290`), so the defect is adjacency, not the number |
| E4 | F4 | "tip receipts do not exist yet at the data commit/tip" | **closed**: absent at `290cddea`, present at `8ac15c41`; the calibration's "tip" is the tip's grandparent (`8ac15c41^` = `74c606a`, `^^` = `290cddea`) |
| E5 | F5 | five w1 evidence pointers in the lesson, two in the SCORECARD | stands: `LATE` — `.ufo/waves/round-44/w1/` holds 0 files at `e4678921` and `03fa5c61`, 848 from `290cddea` |
| E6 | F6 | `QUALITY.md:413` names `…/w1/ScrQualityCriteria/check83.py` | stands: 0 rows at `e4678921`/`03fa5c61`, 1 from `290cddea` — criterion 83 is unrunnable at the commit that published it |

Plus one **coverage note** inside Part A, explicitly not counted among the six: the calibration never observed that the two Round-44
claim rows carry no after *value* (`SCORECARD.md:2570`, `:2571`) — round-44 closure D2 (`:107`) routes exactly that.

## Evidence

All in `.ufo/waves/round-46/w1/ScrErrata/receipts/`, produced by `make-receipts.sh` (read-only; every block prints the command, its
output and its exit code):

| receipt | covers |
|---|---|
| `findings-list.txt` | the calibration's six finding headers (`22/32/50/61/70/75`), its verdict block, round-44 closure D7 (`:118`) and D2 (`:107`) |
| `f1-log-range.txt` | `LOG.md:2499`; `grep -c '^\*\*M44-'` → 9; `SCORECARD.md:2583`; the nine headers `:107…:187`; M44-8/M44-9 evidence seats |
| `f2-renumber.txt` | `git cat-file -e` on the bare path (rc 128 at `e4678921` and `HEAD`); the wave-relative blob at both revs; four tracked maps; freeze `e2289516`; the three lesson citations + `id-guard.md:8`; the map's rows; the calibration's own repro commands (empty) |
| `f3-skill-clients.txt` | `SKILL.md:295`/`:301`; round-43 receipt `:10` and round-44 receipt `:5`; `git diff 6a1a905 e4678921 -- SKILL.md \| grep -c … clients=` → 0; base locators `:284`/`:290` |
| `f4-tip-receipts.txt` | `git rev-parse 8ac15c41^ ^^`; `git rev-list --count 74c606a..8ac15c41` → 1; tip-receipt tree rows (0 at `290cddea`, 3 at `8ac15c41`); `rev=` inside `axis-tip.txt:4` |
| `f5-w1-paths.txt` | w1 tree counts `0 0 848 848 848`; `w1-results.json` `0 0 1 1 1`; every pointer line in the lesson and the SCORECARD |
| `f6-check83.txt` | `QUALITY.md:413`; `check83.py` tree counts `0 0 1 1 1`; the adding commit `290cddea` |
| `d4-results-retention.txt` | directory listing; `git log --all` / `git ls-files` empty; the digest line; `summary.txt` 39 lines / five fields / class tally; `matrix.md:79` totals; `git status` showing the digest untracked; closure D4 lines `28`/`114` |
| `d5-results-null.txt` | `seats 41 results 41 output_null 41`; 41 seat `.md` files; closure D5 (`:116`) |
| `d5-note-line.txt` | the per-entry `note` text located by `grep -n` over the pretty-printed JSON (first at `:11` of that projection) |
| `quotes-verify.txt` | `QUOTES: 17/17 verified`, `[rc=0]` |
| `write-footprint.txt` | `git status` for `.ufo/waves/round-44`, `round-45` (only the pre-existing untracked `results.digest.txt`) and for this seat's directory |

Quote discipline: `quotes.tsv` (17 rows: receipt, locator, quote) and `verify-quotes.py` check each quote is ≤ 25 words, that the
named receipt holds a `<locator>:` line containing it verbatim (so the locator came from a `grep -n`), and that it appears in
`errata.md`. Result `17/17`, exit 0.

## Gates

- Documentation-only seat: no claim counter applies. No counter, axis checker or gate was run — deliberately, since D7 is an errata
  task and the round-46 counters measure C1/C2 only. Nothing here is offered as a counter result.
- Round-46 claim C1/C2 surfaces were **not** touched; `registration.md`, the reference, the counters, the fixtures, the pins and the
  round-46 `l1-draft/` were read only where a truth check needed a revision.

## Touched surfaces

- Written (all new, untracked): `.ufo/waves/round-46/w1/ScrErrata/{errata.md, make-receipts.sh, quotes.tsv, verify-quotes.py,
  receipts/*.txt}` and this report `.ufo/waves/round-46/w1/ScrErrata.md`.
- Read-only: `.ufo/waves/round-44/w2/ConnCalibration.md`; `.ufo/waves/round-44/{assimilation/*, receipts/live-geometry-host-r44.txt}`;
  `.ufo/waves/round-43/receipts/live-geometry-host.txt`; `LOG.md`; `SCORECARD.md`; `SKILL.md`; `corpus/QUALITY.md`;
  `corpus/lessons/{round-44,round-44-verifier-spotcheck,round-45-verifier-spotcheck}.md`; `.ufo/waves/round-45/w1-results.json`;
  `.ufo/waves/round-45/w1/MutC1Counter/*`.
- No write outside the seat directory and the report; no host-service/compositor action; no `hyprctl` of any kind; no tool installed.

## Out of scope / not done

- **Round-44 closure D6** (S290-S297 supersession) is not addressed: the seat spec names D7 errata plus the D4/D5 notes only. It stays
  carried-open as round-45 closure D6 records.
- The suggested one-phrase insertion at `SKILL.md:295` ("(round 43)") is offered to the L1 and **not applied** — editing a current file
  is outside this seat's scope; the errata's reading holds without it.
- Committing `results.digest.txt` (untracked, round-45 tree) is the L1's action, outside this seat's write scope.

## Findings / limits

1. **The D4 sha256 is reported, not verified.** The digest line claims `7325f816…`, `4020571 bytes`; the bytes are gone — not in git
   (`git log --all` empty), not in the worktree, and no file of that size survives under `/fast/scratch/hyaku`
   (`find -size 4020571c` → empty). The size agrees with round-45 closure D4's own observation (`:28`), which corroborates but does
   not hash. Stated in Part B rather than upgraded.
2. **`results.digest.txt` is not mine.** It was in the worktree at 17:33 before this seat opened (mtime `Oct 26 17:33`), is untracked,
   and this seat neither authored nor edited it — it lies in the round-45 tree, outside the seat's write scope.
3. **F2's erratum is a real change of ruling, not a rewording.** The calibration's reproduction commands searched the lane root
   (`git ls-tree -r --name-only e4678921 assimilation/`), which cannot see `.ufo/waves/round-44/assimilation/`; the map is committed
   there and its rows match the lesson's mapping (S311→S164, S312→S301 provisional). Any reader who follows the lesson's bare path
   will still get a 404 from `git cat-file`, which is why the erratum keeps the path-prefix point rather than dropping F2.
4. **F3's erratum does not blame the number.** Equality with the round-43 receipt was verified line-for-line for the `clients=4`
   transcript; the round-44 run is `clients=3`. The leftover risk is a future reader taking the paragraph as a round-44 measurement,
   which is what the appended reading prevents.
5. **The round-44 SCORECARD claim rows' missing after-values** (coverage note) were not re-measured here; that is round-44 D2's
   territory and the values are already appended in the SCORECARD Round 45 section by that round.
6. **No scratch directory was created**, so there is nothing to delete; the only `/fast/scratch` access was a read-only `find` for a
   surviving copy of the D4 bytes. No tool was installed or upgraded (git, coreutils, awk, python3 stdlib).
