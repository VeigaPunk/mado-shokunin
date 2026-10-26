# Round-46 errata — round-44 closure D7 (w2/ConnCalibration), plus the round-45 D4 and D5 notes

Seat: `ScrErrata` (round 46, w1, leaf). Lane `mado-shokunin`, round-46 freeze `8c5434c60e03f147ee1f75ab195e8bc3f0db4dec`, lane tip at write
`e0be61e4f6e34896f8b1c329f9c6d129e5af81f7`. Read-only: no lane file is edited by this seat, no counter, fixture, control, pin or
registration is touched, no product code, no commit. Every statement below is the printed output of a command stored under
`receipts/` beside this file; every locator is a `grep -n` result, never typed; every quote is ≤ 25 words and checked by
`verify-quotes.py` against those receipts.

**Subjects.** Round-44 closure D7 (`corpus/lessons/round-44-verifier-spotcheck.md:118`) routes "`w2/ConnCalibration.md` content
mismatches … correct by appended errata". The calibration's finding list is F1, F2, F3, F5, F6, F4
(`receipts/findings-list.txt`: `22:### F1`, `32:### F2`, `50:### F3`, `61:### F5`, `70:### F6`, `75:### F4`). **Six findings, six
errata, E1-E6 in finding order** below. Round-45 closure D4 and D5
(`corpus/lessons/round-45-verifier-spotcheck.md:114`, `:116`) are answered by the two append-ready notes in Part B and Part C.

**Where the text goes.** Part A is append-only text for the **Round 46** section of `SCORECARD.md`, after its claims table and axis
line. No earlier SCORECARD line, LOG line, lesson line, `SKILL.md` line or `QUALITY.md` line is rewritten; where a document is now
ambiguous the erratum gives the reading, and the one suggested one-phrase insertion is marked as the L1's call, outside this seat's
write scope.

---

## Part A — APPEND-READY BLOCK for `SCORECARD.md` (begin)

### Errata — round-44 closure D7: `w2/ConnCalibration.md`, one entry per finding (added in round 46; nothing above is rewritten)

Scope: these correct what the calibration's six findings say about the round-44 documents. The calibration's own verdict — that the
SCORECARD Round-44 *numeric* claims reproduce — is untouched and its verified-match ledger is not re-litigated here. Three of the six
findings need restating: E2 withdraws F2's [MEDIUM] (the mapping artifact is committed, under a wave-relative path), E3
reclassifies F3 (both client counts are true and belong to different runs), E4 closes F4 (the receipts exist; the word "tip" was
wrong). The remaining three stand unchanged: F1 (E1), F5 (E5), F6 (E6).

#### E1 (F1) — `LOG.md`'s mistake range is a load-time snapshot, not the lesson's range

Attacks: `LOG.md:2499` vs the lesson and the SCORECARD.

- The line reads `(Mistakes M44-1..7, Round-43 errata E1-E4)` (`receipts/f1-log-range.txt`, `2499:` row).
- Truth: the lesson carries nine mistake headers — `grep -c '^\*\*M44-' corpus/lessons/round-44.md` → `9` (headers at `:107`,
  `:119`, `:128`, `:135`, `:147`, `:156`, `:171`, `:178`, `:187`), and the round's own publication states `Mistakes M44-1..9 mined`
  (`SCORECARD.md:2583`).

Read `LOG.md:2499`'s "M44-1..7" as the count at protocol load, written before w1 minted M44-8 and M44-9 — both name w1 seats as
their evidence (`M44-8`, `corpus/lessons/round-44.md:178`, cites `w1/CritC2Cheat.md`; `M44-9`, `:187`, cites `w1/CritFsPremise`);
the closed range is `M44-1..9` and its citation is `SCORECARD.md:2583`. Not a false statement about what was routed at load, so no document is
rewritten. The calibration's [LOW] grading stands.

#### E2 (F2) — the renumber map *is* committed; the lesson's path is wave-relative, which is why it "does not exist"

Attacks: `corpus/lessons/round-44.md:26`, `:71`, `:82`; `.ufo/waves/round-44/assimilation/id-guard.md:8`; and the calibration's F2
heading, `The lesson and the id guard cite \`assimilation/renumber-map.tsv\`, which does not exist at the data commit or the tip`
(`.ufo/waves/round-44/w2/ConnCalibration.md:32`).

- The cited path, relative to the lane root, does not exist at either revision:
  `git cat-file -e e4678921:assimilation/renumber-map.tsv` → `fatal: path … does not exist`; the same for `HEAD`
  (`receipts/f2-renumber.txt`).
- The artifact is committed, wave-relative: `git ls-tree e4678921 -- .ufo/waves/round-44/assimilation/renumber-map.tsv` →
  `100644 blob c9639ce84472eaccb9ea14007dbbc843e2e0e556`, the same blob at `HEAD`; it entered history in the round-44 freeze
  `e2289516` (`git log --diff-filter=A -- …`), and four renumber maps are tracked (`rounds 37, 41, 43, 44`).
- The map's rows match what the lesson states: staged `S311` → lane `S164`; staged `S312` → lane `S301 (provisional)`. The three
  citations name it as `assimilation/renumber-map.tsv` (`corpus/lessons/round-44.md:26`, `:71`, and the row headed
  "Old→new for the staged document" at `:82`), and `id-guard.md:8` says
  "Mapping is by document (renumber-map.tsv); no staged id is carried." — i.e. wave-relative, exactly as the committed tree lays it
  out.

Erratum: read the three lesson citations and `id-guard.md:8` with the `.ufo/waves/round-44/` prefix — the map is
`.ufo/waves/round-44/assimilation/renumber-map.tsv`, blob `c9639ce8…`, committed in the freeze before any data. F2's conclusion
("the artifact was never committed") is **withdrawn**; what remains is the M44-4 class one layer up (a bare path that resolves only
after the wave-directory prefix is supplied). Its [MEDIUM] is reduced to the path-prefix ambiguity, and the calibration's own
reproduction commands (`git ls-tree -r --name-only e4678921 assimilation/` → 0 rows) printed empty for exactly that reason.

#### E3 (F3) — both client counts are true; the paragraph is a round-43 transcript and the defect is adjacency

Attacks: `SKILL.md:295` and its transcript at `:301`, next to the round-44 exit-map additions.

- The paragraph's transcript line reads `clients=4 matched=0 … verdict=NO_MATCHING_CLIENT` (`SKILL.md:301`) and its lead says
  `the dump holds four tiled` (`SKILL.md:295`); the matching run is the round-43 receipt,
  `.ufo/waves/round-43/receipts/live-geometry-host.txt:10` → `clients=4 matched=0`.
- The round-44 run is `.ufo/waves/round-44/receipts/live-geometry-host-r44.txt:5` → `clients=3 matched=0`, same rules and same
  `exit=3`.
- The paragraph is not a round-44 edit: base `6a1a905` carries the same text at `SKILL.md:284` and `:290`
  (`git show 6a1a905:SKILL.md | grep -n` → `284:`, `290:`), and
  `git diff 6a1a905 e4678921 -- SKILL.md | grep -c '^[-+].*clients='` → `0`.

Erratum: read `SKILL.md:295-301` as the round-43 host run, not a round-44 measurement; the round-44 measurement is
`.ufo/waves/round-44/receipts/live-geometry-host-r44.txt` (`clients=3`). The round-44 zone pushed a same-dated transcript below its own insertions,
which is the defect — not the number. If the L1 wants it unambiguous on the page, append "(round 43)" to the first line; that is an
edit to a current file and is outside this seat's scope, and the reading above stands without it.

#### E4 (F4) — the tip receipts exist; the calibration's "tip" was the tip's grandparent

Attacks: the calibration's F4 heading, `Lesson-referenced tip receipts do not exist yet at the data commit/tip`, and its "at tip
290cddea" measurements.

- The three receipts are absent at `290cddea` (`git ls-tree 290cddea -- …/{c1-after-tip,c2-after-tip,axis-tip}.txt` → no rows) and
  present at `8ac15c41` (`axis-tip.txt` blob `486dbbe8…`, `c1-after-tip.txt` blob `8b3b3310…`, `c2-after-tip.txt` blob
  `89149342…`) — `receipts/f4-tip-receipts.txt`.
- `8ac15c41` is the round-44 lane tip; `8ac15c41^` = `74c606a`, `8ac15c41^^` = `290cddea`, and
  `git rev-list --count 74c606a..8ac15c41` → `1`. The receipts themselves name `rev=74c606a1c7fd52a6bb85bb1c786529c926040c73`
  (`axis-tip.txt:4`).

Erratum: every "tip" measurement in the calibration means `290cddea` — the tip's grandparent, not the tip. Read them as "at
`290cddea`". F4's pending-by-design status is **closed**: the receipts are committed at the tip `8ac15c41`, and they measure
`74c606a` (tip minus the one commit that adds only receipts and wave files). No content is corrected by this entry; the pointer
label is.

#### E5 (F5) — the w1 evidence pointers are `LATE`: cited at the data commit, committed one commit later

Attacks: `corpus/lessons/round-44.md:5`, `:7`, `:181-183`, `:246`; `SCORECARD.md:2566`, `:2573`.

- `.ufo/waves/round-44/w1/` holds `0` files at the data commit `e4678921` and `0` at the v2 freeze `03fa5c61`, and `848` from
  `290cddea` through `HEAD`; `.ufo/waves/round-44/w1-results.json` is absent at both pre-tip revisions and present from
  `290cddea` (`receipts/f5-w1-paths.txt`).
- The lesson's opening sentence points into that tree (`:5` names `.ufo/waves/round-44/w1-results.json`), and the SCORECARD's
  supersession sentence names five w1 seat files (`:2566`), with the separability sentence naming two more (`:2573`).

Erratum: these pointers are `LATE` in the QUALITY-83 sense — the claim was admitted at `e4678921` and the evidence arrived in
`290cddea`. Read them against the tree at `290cddea` or later, never at the data commit. The finding stands unchanged; the documents
are not rewritten.

#### E6 (F6) — criterion 83's check command names a file that lands after the commit that published the criterion

Attacks: `corpus/QUALITY.md:413`.

- The check line is `python3 -I .ufo/waves/round-44/w1/ScrQualityCriteria/check83.py --repo . --rev <REV> --doc <PATH-IN-REPO>
  --prefix .ufo/` (`QUALITY.md:413`).
- `check83.py` has `0` rows in the tree at `e4678921` and at `03fa5c61`, and `1` row from `290cddea` through `HEAD`; it was added by
  `290cddea` (`git log --diff-filter=A -- .ufo/waves/round-44/w1/ScrQualityCriteria/check83.py`).

Erratum: criterion 83 is checkable only from `290cddea` onward; at the commit that published it the check is unrunnable — the
criterion's own violation class applied to itself. The finding stands; the data commit is not rewritten, so this is recorded rather
than repaired.

#### Coverage note (beyond the six findings, stated because the calibration was asked to count statement-vs-repo mismatches)

The calibration's finding list is F1, F2, F3, F5, F6, F4 and none of them observes that the two Round-44 claim rows carry no after
*value*: `SCORECARD.md:2570` and `:2571` answer with pointers ("see `receipts/c1-after-data.txt`", "see `receipts/c2-after-data.txt`")
and both self-verdict cells say the value is recorded in the round report. Round-44 closure D2 routes exactly that — append the
values in the next SCORECARD section, never rewrite (`corpus/lessons/round-44-verifier-spotcheck.md:107`) — and the values
appended for it are the answer; this is a coverage gap, not a false statement, and it is not counted among the six.

## Part A — APPEND-READY BLOCK for `SCORECARD.md` (end)

---

## Part B — D4 note: retention of `.ufo/waves/round-45/w1/MutC1Counter/results.json`

Append-ready text (for the Round 46 section, or the round-46 lesson's Round-45 closure items):

> **D4 (round-45) — the 4 MB mutation ledger: digest committed, bytes not.** `.ufo/waves/round-45/w1/MutC1Counter/results.json`
> was never committed and is not in the worktree any more (`git log --all -- <path>` prints nothing; `git ls-files <path>` prints
> nothing; the directory holds `c1-r45-monitors.py`, `mutdrive.py`, `summary.txt`, `matrix.md` and `results.digest.txt`). The digest
> line beside `summary.txt` records `sha256 7325f816a1561a252dc562f8b9bb038f1ea213d653c95499ea067dc62ed58a55`, `4020571 bytes`,
> `dict 39 top-level entries`, and that the per-mutant verdicts are summarised in `summary.txt` and `matrix.md`. `summary.txt` is the
> machine-readable residue: 39 lines, five `|`-separated fields each — `mutant_id | class | fixtures=49/49 verdict=… | killing
> controls or - | missed=N/16` — with 29 `SURVIVOR`, 7 `OVER-STRICT` and 3 `GATE-BROKEN` (two of them `K02-STUB,K14-MIRROR-IGNORED`,
> one adding `K08-LIVE-HYPRCTL`), and `matrix.md:79` states the same tally: "39 = 1 baseline + 3 GATE-BROKEN (killed) + 7 OVER-STRICT (killed) + 3 equivalent survivors + 25 missing-control survivors". The file itself stays out of
> git: it is a 4 MB run log, and the digest, `summary.txt` and `matrix.md` are the citable record.

What I verified, and what I could not:

- Verified: absence from the worktree and from history, the tracked neighbours, the digest line's exact text, `summary.txt`'s 39
  lines / five fields / class tally, and `matrix.md`'s 153 lines with its method line naming
  "38 single-edit mutants + 1 identity baseline" and "551 counter runs" — `receipts/d4-results-retention.txt`.
- Corroborated, not verified: the digest's `4020571 bytes` matches round-45 closure D4's own observation, "4,020,571 B"
  (`corpus/lessons/round-45-verifier-spotcheck.md:28`), which also names the file whose bytes are gone.
- **Not verified: the sha256.** No copy survives — the file is not in git, not in the worktree, and no file of that size exists
  under `/fast/scratch/hyaku` (`find … -size 4020571c` → empty). The hash is the digest author's measurement; re-hashing requires the
  bytes. The digest line should be committed (it is untracked at write time: `git status --porcelain` shows
  `?? .ufo/waves/round-45/w1/MutC1Counter/results.digest.txt`) so the retention decision is itself in the record; committing it is
  the L1's action and outside this seat's write scope.

---

## Part C — D5 note: `.ufo/waves/round-45/w1-results.json` is not evidence

Append-ready text (the round-45 closure asks that this be said in the wave README or the next lesson):

> **D5 (round-45) — read the seat reports, not the results file.** `.ufo/waves/round-45/w1-results.json` records
> `seats 41`, `results 41`, and **all 41 entries carry `output: null`** — the orchestrator kernel restarted mid-wave and the seat
> outputs were delivered to the session but not retained. Each entry keeps the seat name, its agent role and a note reading
> "read the seat report file in the wave dir", so the file is a roster, not a transcript. The record of what the 41 seats found is
> the 41 committed `w1/<Seat>.md` reports (`git ls-tree --name-only HEAD .ufo/waves/round-45/w1/ | grep -c '\.md$'` → `41`); cite
> those. The closure's own routing says "the seat report files are the only record"
> (`corpus/lessons/round-45-verifier-spotcheck.md:116`). Round-46's `w1-results.json` should be treated the same way unless its `output` fields are non-null.

Verified: `seats 41 results 41 output_null 41`, the note text quoted above, and the count of 41 seat `.md` files at `HEAD`
(`receipts/d5-results-null.txt`).

---

## Verification

| check | command (outputs in `receipts/`) | result |
|---|---|---|
| finding list (six findings, in the calibration's own order) | `grep -n '^### F' .ufo/waves/round-44/w2/ConnCalibration.md` | `F1:22 F2:32 F3:50 F5:61 F6:70 F4:75` (`findings-list.txt`) |
| F1 range | `grep -n 'Mistakes M44' LOG.md`; `grep -c '^\*\*M44-' corpus/lessons/round-44.md`; `grep -n 'Mistakes M44-1..9' SCORECARD.md` | `2499:`; `9`; `2583:` (`f1-log-range.txt`) |
| F2 map | `git cat-file -e <rev>:assimilation/renumber-map.tsv` (128 both revs); `git ls-tree <rev> -- .ufo/waves/round-44/assimilation/renumber-map.tsv`; `git ls-files '*/renumber-map*'`; `git log --diff-filter=A -- <map>` | blob `c9639ce8…` at `e4678921` and `HEAD`; four maps; added by `e2289516` (`f2-renumber.txt`) |
| F3 client counts | `grep -n 'clients=4' SKILL.md`; round-43 receipt `:10`; round-44 receipt `:5`; `git diff 6a1a905 e4678921 -- SKILL.md \| grep -c '^[-+].*clients='` | `301:`; `clients=4`; `clients=3`; `0` (`f3-skill-clients.txt`) |
| F4 tip ancestry and receipts | `git rev-parse 8ac15c41^ 8ac15c41^^`; `git rev-list --count 74c606a..8ac15c41`; `git ls-tree <rev> -- …tip receipts`; `grep -n 'rev=' axis-tip.txt` | `74c606a`, `290cddea`; `1`; 0 rows at `290cddea`, 3 at `8ac15c41`; `4:… rev=74c606a1c7fd52…` (`f4-tip-receipts.txt`) |
| F5 late w1 evidence | `git ls-tree -r --name-only <rev> -- .ufo/waves/round-44/w1/ \| wc -l` for `e4678921 03fa5c61 290cddea 8ac15c41 HEAD` | `0 0 848 848 848`; `w1-results.json`: `0 0 1 1 1` (`f5-w1-paths.txt`) |
| F6 check83 | `grep -n 'check83.py' corpus/QUALITY.md`; same tree count for the script; `git log --diff-filter=A` | `413:`; `0 0 1 1 1`; added by `290cddea` (`f6-check83.txt`) |
| D4 retention | `ls -l` the dir; `git log --all -- <path>`; `git ls-files <path>`; `cat results.digest.txt`; `wc -l summary.txt`; `awk -F'\|' '{print NF}'`; class tally; `wc -l matrix.md`; `grep -n '551 counter runs\|38 single-edit mutants'` | as stated in Part B (`d4-results-retention.txt`) |
| D5 null output | `python3 -c` over `w1-results.json`; `git ls-tree --name-only HEAD .ufo/waves/round-45/w1/ \| grep -c '\.md$'` | `41 41 41`; `41` (`d5-results-null.txt`) |
| quotes | `python3 verify-quotes.py` (each quote ≤ 25 words; the named receipt holds a `<locator>:` line containing the quote verbatim, and the quote is present in this file) | `QUOTES: 17/17 verified` (`quotes-verify.txt`) |
| write footprint | `git status --porcelain -- .ufo/waves/round-44 .ufo/waves/round-45`; `git status --porcelain -- .ufo/waves/round-46/w1/ScrErrata` | the first prints only the pre-existing `?? …/round-45/w1/MutC1Counter/results.digest.txt`; the second prints `?? .ufo/waves/round-46/w1/ScrErrata/` — this seat's only write (`write-footprint.txt`) |

## Limits (declared)

- No clone, venv, fixture, build or counter work directory was created, so nothing was written under
  `/fast/scratch/hyaku/mado-r46/ScrErrata/` and there is nothing to delete; the only `/fast/scratch` access was a read-only `find`
  for a surviving copy of the D4 bytes. All evidence above is read-only output captured into `receipts/`.
- The D4 sha256 is **reported, not verified** (Part B); no surviving copy of the hashed bytes exists that this seat could find.
- `results.digest.txt` was present in the lane worktree at 17:33 before this seat opened; this seat did not author it and did not
  edit it (it lies in the round-45 wave tree, outside this seat's write scope). It is untracked at write time.
- The suggested one-phrase insertion at `SKILL.md:295` ("(round 43)") is offered to the L1, not applied: editing a current file is
  outside this seat's scope, and E3's reading holds without it.
- Not attempted, out of scope: the calibration's verified-match ledger, the entries' content, the pins, the counters, the controls,
  and any host or compositor read (no `hyprctl` of any kind was run by this seat).
- No tool was installed or upgraded by this seat; `git`, coreutils, `awk` and `python3` stdlib only.
