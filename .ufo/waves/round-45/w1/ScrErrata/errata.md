# Round-45 errata for round-44 closure D2, D3, D7 — append-ready text

Seat: `ScrErrata` (round 45, w1). Lane `mado-shokunin`, base `0c89478af821a6424c9ac922eafe02e39630cf4f`, round-45 freeze
`22a8dedd02f507689c567777e0f20b5e645c8ce0`. Read-only seat: no lane file is edited, no product code, counter, controls,
registration or pin is touched. Every statement below is a `grep -n`, `git` or counter output stored under
`receipts/` next to this file; quotes are ≤ 25 words with a computed locator, checked by `verify-quotes.py`.

**What this file is.** Three append-only blocks for the L1 to paste into the Round 45 section of `SCORECARD.md`
(after that section's claims table and axis line). Nothing above is rewritten: the Round 44 rows at
`SCORECARD.md:2570-2571` stay byte-identical, and D2 is answered by appended values, not by editing a row.

---

## APPEND-READY BLOCK — begin

### Errata — round-44 closure D2, D3, D7 (added in round 45; no earlier text is changed)

#### ER-D2 — Round 44's after values and verdicts (the rows gave pointers, not values)

The Round 44 table answered both claim rows with a pointer — the C1 cell reads "see `receipts/c1-after-data.txt`", the C2
cell "see `receipts/c2-after-data.txt`" (`SCORECARD.md:2570`, `:2571`) — and both self-verdict cells read "recorded in the
round report from the receipts". The values themselves, as published in the receipts and re-measured at the lane tip:

| Round 44 claim | After at the data commit `e4678921` | After at `74c606a` (the tip receipts' rev) | After at the lane tip `8ac15c41` (measured in round 45) | Verdict |
|---|---|---|---|---|
| C1 `PRED-C1-r44-v2` (operability) | `PRED-C1-r44-v2: fixtures=26/26 tool=present verdict=TARGET_MET rev=e46789213830597348fe96a351ae004d10587385`, clauses `a:1 b:1 b4:1 b5:1 e:1 g:1 r:1`, exit 0 (`.ufo/waves/round-44/receipts/c1-after-data.txt:53`) | `PRED-C1-r44-v2: fixtures=26/26 tool=present verdict=TARGET_MET rev=74c606a1c7fd52a6bb85bb1c786529c926040c73`, same clauses, exit 0 (`receipts/c1-after-tip.txt:53`) | same line with `rev=8ac15c412051874836e0db36b1178723ade6c340`, exit 0 (`.ufo/waves/round-45/w1/ScrErrata/receipts/c1-tip-8ac15c41.txt`) | **TARGET_MET** |
| C2 `PRED-C2-r44-v2` (coverage) | `PRED-C2-r44-v2: admitted=1/1 verdict=TARGET_MET rev=e46789213830597348fe96a351ae004d10587385`, clauses a-j all 1, exit 0 (`.ufo/waves/round-44/receipts/c2-after-data.txt:29`) | `PRED-C2-r44-v2: admitted=1/1 verdict=TARGET_MET rev=74c606a1c7fd52a6bb85bb1c786529c926040c73`, exit 0 (`receipts/c2-after-tip.txt:29`) | same with `rev=8ac15c412051874836e0db36b1178723ade6c340`, exit 0 (`…/ScrErrata/receipts/c2-tip-8ac15c41.txt`) | **TARGET_MET** |
| axis table (3 axes) | `MADO_AXIS: checked=3 mismatched=0 rev=e46789213830597348fe96a351ae004d10587385` (navigation 61/61, calibration 71/71, operability 12/12) (`.ufo/waves/round-44/receipts/axis-data.txt:4`) | `MADO_AXIS: checked=3 mismatched=0 rev=74c606a1c7fd52a6bb85bb1c786529c926040c73` (`receipts/axis-tip.txt:4`) | `checked=3 mismatched=0 rev=8ac15c412051874836e0db36b1178723ade6c340` (`…/ScrErrata/receipts/axis-tip-8ac15c41.txt`) | **MATCH** |

Both after-states are therefore published as **met** at the data commit, at the revision the tip receipts name, and at the
tip; the self-verdict cells' "recorded in the round report" is answered by the verdict column above.

#### ER-D3 — the tip receipts name the tip's parent; measured equivalence at `8ac15c41`

`.ufo/waves/round-44/receipts/c1-after-tip.txt`, `c2-after-tip.txt` and `axis-tip.txt` carry
`rev=74c606a1c7fd52a6bb85bb1c786529c926040c73` (`axis-tip.txt:4`) — the closure lesson names the gap itself:
they name `74c606a`, "not the lane tip `8ac15c41`" (`corpus/lessons/round-44-verifier-spotcheck.md:110`) — i.e. the
parent of the lane tip
(`git rev-parse 8ac15c41^` → `74c606a1c7fd52…`), one commit behind it (`git rev-list --count 74c606a..8ac15c41` → `1`).
The equivalence is structural and now also measured:

- structural: `git diff --name-only 74c606a 8ac15c41` lists 599 files and **0** outside `.ufo/waves/round-44/`; the seven
  surfaces the two counters and the axis read (`tools/mado-geometry.py`, `corpus/knowledge/hyprland-gkeep-size-request-r44.md`,
  `corpus/SOURCES.md`, `SKILL.md`, `corpus/lessons/round-44.md`, `corpus/QUALITY.md`, `SCORECARD.md`) show an empty
  `git diff --stat`, so each is byte-identical at `74c606a` and at the tip. This is the closure lesson's own reading
  (`corpus/lessons/round-44-verifier-spotcheck.md:111`: "commit touches only `.ufo/waves/round-44/`"), which closed D3 as
  "equivalent here" (`:110`) without executing it at the tip.
- measured at the tip: `PRED-C1-r44-v2: fixtures=26/26 tool=present verdict=TARGET_MET rev=8ac15c41…` (clauses
  `a:1 b:1 b4:1 b5:1 e:1 g:1 r:1`, clause r `37/37`), `PRED-C2-r44-v2: admitted=1/1 verdict=TARGET_MET rev=8ac15c41…`
  (clauses a-j all 1), `MADO_AXIS: checked=3 mismatched=0 rev=8ac15c41…`, all exit 0, in a `--shared` clone of the lane
  checked out at `8ac15c41`; receipts `…/ScrErrata/receipts/{c1-tip,c2-tip,axis-tip}-8ac15c41.txt`.

The tip receipts are correct as written; the only erratum is the word "tip": they measure `74c606a`, not
`8ac15c41`. Read them as "at the tip minus its evidence commit" and cite the measurement above for `8ac15c41` itself.

#### ER-D7 — `w2/ConnCalibration.md` (round 44) errata, one entry per finding

Scope note: these correct the calibration's findings, not the round's data; the calibration's verdict "All SCORECARD
Round-44 numeric claims verified consistent with repo state" remains true. Two of its six findings do not survive
re-check as stated (F2 withdrawn, F3 reclassified); three stand (F1, F5, F6); F4 is closed by the tip and its premise
corrected.

**ER-D7.1 — F1 stands, with its time index stated.** The calibration attacks `LOG.md:2499`, where the round-44 bullet
reports "Mistakes M44-1..7" (`.ufo/waves/round-44/w2/ConnCalibration.md:24`). The truth: the lesson holds nine
(`grep -c '^\*\*M44-' corpus/lessons/round-44.md` → `9`) and the round's own SCORECARD line records
"Mistakes M44-1..9 mined" (`SCORECARD.md:2583`). Erratum: `LOG.md:2499`'s "M44-1..7" is the protocol-load count
(written before w1 minted M44-8/M44-9); read it as a load-time snapshot, never as the lesson's range, and cite
`SCORECARD.md:2583` for the closed range.

**ER-D7.2 — F2 is withdrawn: the mapping artifact is committed.** The calibration's F2 states there is
"no `assimilation/` directory or any `renumber-map*` file exists in the repo at" `e4678921` or HEAD
(`.ufo/waves/round-44/w2/ConnCalibration.md:38`) and concludes the artifact was never committed. That is false:
`git ls-tree e4678921 -- .ufo/waves/round-44/assimilation/renumber-map.tsv` → `100644 blob c9639ce8…`, the same blob at
`0c89478`, landed in the round-44 freeze `e2289516` (`git log --oneline -- .ufo/waves/round-44/assimilation/renumber-map.tsv`),
and `git ls-files | grep renumber-map` lists four such files (rounds 37/41/43/44). Its own reproduction commands are
lane-root-relative (`git ls-tree -r --name-only e4678921 assimilation/` → 0 rows), which is why they printed empty.
Erratum: the citations at `corpus/lessons/round-44.md:26`, `:71`, `:82` ("Old→new for the staged document") and
`.ufo/waves/round-44/assimilation/id-guard.md:8` are wave-relative and resolve to
`.ufo/waves/round-44/assimilation/renumber-map.tsv` (blob `c9639ce8…`, committed in the freeze); read them that way.
F2's [MEDIUM] is withdrawn; what remains is a path-prefix ambiguity, and QUALITY 83's checker at the data commit does
not flag it (13 citations, 1 violation — the `w1-results.json` LATE row of ER-D7.4).

**ER-D7.3 — F3 is reclassified: the number is right, the adjacency is the defect.** The calibration's F3 heading says
the paragraph "carries the round-43 host-run transcript (clients=4)" and that the round-44 receipt records clients=3
(`.ufo/waves/round-44/w2/ConnCalibration.md:50`). Both numbers are true and they belong to different runs: the paragraph
quotes `.ufo/waves/round-43/receipts/live-geometry-host.txt:10` → `… clients=4 matched=0 …` and its text is unchanged
from base `6a1a905` (no `clients=` line at all in `git diff 6a1a905 e4678921 -- SKILL.md`; the paragraph is at
`6a1a905:SKILL.md:284` and `SKILL.md:295`); the round-44 run is
`.ufo/waves/round-44/receipts/live-geometry-host-r44.txt:5` → `… clients=3 matched=0 …`. Erratum: `SKILL.md`'s host-run
paragraph is a round-43 quote — `SKILL.md:295` opens "the dump holds four tiled", and the round-43 receipt's dump is
that one; append "(round 43)" to its first line so the round-44 receipt beside it cannot be misread as its source. Not a
content error.

**ER-D7.4 — F5 stands.** The w1 evidence that the lesson and the SCORECARD point at landed after the data commit: at
`e4678921`, `.ufo/waves/round-44/w1/` holds 0 files, and it holds 0 files at the v2 freeze `03fa5c61` too
(`git ls-tree -r --name-only <rev> -- .ufo/waves/round-44/w1/ | wc -l` → `0`), while `290cddea` and `8ac15c41` hold 848.
The lesson's closing clause names a file in that tree — the sentence reads
`` `.ufo/waves/round-44/w1-results.json`) broke both v1 predicates `` — and the tree is empty at the data commit
(`corpus/lessons/round-44.md:5`). Erratum: the
pointers at `corpus/lessons/round-44.md:5`, `:7`, `:181-183`, `:246` and `SCORECARD.md:2566`, `:2573` are `LATE` — the
claims were admitted at `e4678921` and their evidence arrived in `290cddea`. QUALITY 83's checker reports one LATE
citation at the data commit (`w1-results.json`); the other pointers are prose paths it does not parse, so its PASS would
not have caught them.

**ER-D7.5 — F6 stands.** Criterion 83's check line is
`python3 -I .ufo/waves/round-44/w1/ScrQualityCriteria/check83.py --repo . --rev <REV> --doc <PATH-IN-REPO> --prefix .ufo/`
(`corpus/QUALITY.md:413`), and the file it names is absent at `e4678921`
(`git ls-tree -r --name-only e4678921 -- .ufo/waves/round-44/w1/ScrQualityCriteria/check83.py` → 0 rows) and present from
`290cddea` (same command at `290cddea` and `8ac15c41` → 1 row). Erratum: criterion 83 is checkable from `290cddea` only;
at the commit that published it the check is unrunnable — the criterion's own violation class, recorded rather than
repaired, because the data commit is not rewritten.

**ER-D7.6 — F4 is closed, and its "tip" needs correcting.** The calibration left as pending-by-design that the three
tip receipts are not yet committed; its observation names `receipts/axis-tip.txt` absent (`:78`) at what it calls "at
tip 290cddea where the claim names the tip" (`:8`). Both
halves are now settled: the three tip receipts are absent at `290cddea` and committed at `8ac15c41`
(`git ls-tree 290cddea -- .ufo/waves/round-44/receipts/{c1-after-tip,c2-after-tip,axis-tip}.txt` → 0 each; at `8ac15c41`
→ 1 each), and `290cddea` is not the tip: the lane tip is `8ac15c41`, its parent `74c606a`, its grandparent `290cddea`.
Erratum: read every "tip" measurement in the calibration (`:8`, and its "at tip 290cddea, where the w1 evidence was
committed" at `:84`, F4's "at the data commit/tip") as "at `290cddea`";
F4's pending status is resolved by the tip commit, and ER-D3 above supplies the measurement at the true tip.

**ER-D7.7 — coverage gap: D2 was not flagged.** The calibration's finding list is F1, F2, F3, F5, F6, F4
(`grep -n '^### F' .ufo/waves/round-44/w2/ConnCalibration.md`); none of them is that the two Round 44 claim rows carry
no after value (`SCORECARD.md:2570`, `:2571`, both self-verdict cells "recorded in the round report from the receipts"),
although counting statement-vs-repo mismatches was the seat's task. Its verdict is about numeric claims, and these rows
carry none, so this is a gap in coverage rather than a false statement. ER-D2 above answers it.

## APPEND-READY BLOCK — end

---

## Verification

| check | command (all outputs in `receipts/`) | result |
|---|---|---|
| after values at data commit / tip-parent | `grep -n 'fixtures=26/26 …'` and `grep -n 'admitted=1/1 …'` over `.ufo/waves/round-44/receipts/{c1,c2}-after-{data,tip}.txt` | lines 53/53 and 29/29, exit 0 (`receipts/d2-after-values.txt`) |
| after values at the lane tip | `python3 -I quality/counters/c1-r44-geometry-states-v2.py --repo <clone@8ac15c41> --rev HEAD --work …  --nonce 4515d3c3e0e0`; same for `c2-r44-gkeep-size-request-v2.py`; `quality/check-axis-scores.py --rev 8ac15c41` | `26/26 MET`, `1/1 MET`, `3/3 MATCH`, all exit 0 (`receipts/*-tip-8ac15c41.txt`) |
| receipts unchanged tip→base | `git diff --name-only 8ac15c41 0c89478 -- .ufo/waves/round-44/receipts/` | empty |
| D3 structure | `git rev-parse 8ac15c41^`, `git rev-list --count 74c606a..8ac15c41`, `git diff --name-only 74c606a 8ac15c41 \| wc -l`, `… \| grep -vc '^\.ufo/waves/round-44/'`, `git diff --stat … -- <7 surfaces>` | `74c606a…`, `1`, `599`, `0`, empty (`receipts/d3-structure.txt`) |
| D7 truths | `grep -c '^\*\*M44-'`, `git ls-tree … renumber-map.tsv`, `git ls-files \| grep renumber-map`, `git diff 6a1a905 e4678921 -- SKILL.md \| grep -c '^[-+].*clients='`, `git ls-tree -r --name-only <rev> -- .ufo/waves/round-44/w1/ \| wc -l` (0/0/848/848), the check83.py tree counts, the tip-receipt tree counts | as stated above (`receipts/d7-truths.txt`) |
| QUALITY 83 at the data commit | `python3 -I .ufo/waves/round-44/w1/ScrQualityCriteria/check83.py --repo . --rev e4678921 --doc corpus/lessons/round-44.md --prefix .ufo/` | `CHECK83: verdict=FAIL citations=13 violations=1 outside=7 rev=e467892`, exit 1 — the one violation is the `w1-results.json` LATE row (`receipts/d7-check83.txt`) |
| lesson line numbers (they are cited at both revisions) | `git diff --stat e4678921 0c89478 -- corpus/lessons/round-44.md`; `grep -n` at the data commit and in the working tree | +14 lines, all appended at the end; locators 5, 26, 71, 82 identical at both (`receipts/lesson-lines.txt`) |
| quotes | `python3 verify-quotes.py` (each quote ≤ 25 words, locator recomputed by `grep -nF` in `receipts/quotes-grep.txt`, and present in this file) | `QUOTES: 28/28 verified` |

## Limits (declared)

- The tip measurements used the frozen counters and axis checker as committed at the round-45 base; no counter was
  edited, and the clone was `--shared --no-checkout` at `/fast/scratch/hyaku/mado-r45/ScrErrata/`, deleted before the
  report. The C1 run used a fixed `--nonce 4515d3c3e0e0` so its line is reproducible; the receipted run's nonce is quoted
  verbatim and the D4 base-share question is untouched here.
- `check83.py` was taken from the tip and run against the data commit; that is the only way to execute criterion 83 on
  `e4678921`, and it is stated rather than hidden.
- Not attempted, out of scope: the entry's content, the pins, the controls, the host (no `hyprctl`, no compositor or
  service action of any kind), and any rewrite of the corrected documents.
- No tool installed; `python3` stdlib and `git` reads only.
