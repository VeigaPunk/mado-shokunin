# Round-47 errata — round-44 closure D7: `w2/ConnCalibration.md`, confirmed at committed bytes, one SCORECARD line each

Seat `ScrErrataCal` (round 47, w1, leaf). Lane `mado-shokunin`; all checks ran at lane tip
`c24adef2632672325a4eef3e3492f6716ccb6d14`, whose `SCORECARD.md`, `LOG.md`, `SKILL.md`, `corpus/QUALITY.md`,
`corpus/lessons/round-44.md`, `corpus/lessons/round-44-verifier-spotcheck.md` and `corpus/lessons/round-46.md` are byte-identical to
the round-47 base `60edb66e` (`git diff --numstat 60edb66e c24adef2 -- <those paths>` → empty; the one commit between them adds only
`.ufo/waves/round-47/*`). Read-only seat: no lane file edited, no commit, no counter/fixture/control/pin/registration touched, no
host or compositor read, no tool installed.

**Subjects.** Round-44 closure D7 (`corpus/lessons/round-44-verifier-spotcheck.md:118`) routes "`w2/ConnCalibration.md` content
mismatches … correct by appended errata". The calibration's finding list is F1, F2, F3, F5, F6, F4
(`receipts/findings-list.txt`, locators `22`, `32`, `50`, `61`, `70`, `75`). The long-form draft
`.ufo/waves/round-46/w1/ScrErrata/errata.md` is committed (`git ls-files` → 1 row) and round-46 recorded it
"not landed (routed)" (`corpus/lessons/round-46.md:361`); `SCORECARD.md` still carries no errata block
(`grep -n 'Errata — round-44 closure D7' SCORECARD.md` → no row, rc 1). Round-47's planned item 3 names the same landing
(`SCORECARD.md:2652`).

This file confirms **each of the six mismatches** against committed bytes and gives the **append-only SCORECARD text, one line per
finding**, plus one coverage line that is explicitly not among the six.

---

## Part A — append-ready lines for the Round 47 section of `SCORECARD.md` (begin)

### Errata (round 47) — round-44 closure D7: `w2/ConnCalibration.md` mismatches, one line each (append-only; nothing above is rewritten; long form `.ufo/waves/round-46/w1/ScrErrata/errata.md`, every line re-confirmed at `c24adef2`)

E1 (F1) `LOG.md:2499`'s "Mistakes M44-1..7" is the protocol-load snapshot, not the lesson's range: `grep -c '^\*\*M44-' corpus/lessons/round-44.md` → `9` (headers `:107`…`:187`), `SCORECARD.md:2583` publishes "Mistakes M44-1..9 mined", and M44-8 (`:178`, evidence `w1/CritC2Cheat.md` at `:181`) and M44-9 (`:187`, `w1/CritFsPremise` at `:189`) were minted after load — read the closed range as M44-1..9; F1 stands and no file is rewritten.

E2 (F2) the renumber map is committed, wave-relative: `git cat-file -e e4678921:assimilation/renumber-map.tsv` → rc 128, but `git ls-tree e4678921 -- .ufo/waves/round-44/assimilation/renumber-map.tsv` → blob `c9639ce84472eaccb9ea14007dbbc843e2e0e556` (added in freeze `e2289516`, same blob at `HEAD`; rows S311→S164 and S312→S301 (provisional)) — read `corpus/lessons/round-44.md:26` ("maps the package by document"), `:71`, `:82` and `.ufo/waves/round-44/assimilation/id-guard.md:8` ("Mapping is by document (renumber-map.tsv)") with the `.ufo/waves/round-44/` prefix; F2's "the artifact was never committed" is withdrawn and its [MEDIUM] reduces to the path-prefix ambiguity (QUALITY 83 class, one directory up).

E3 (F3) both client counts are true and belong to different runs: `SKILL.md:301` (at the data commit `:299`) reproduces the round-43 receipt `.ufo/waves/round-43/receipts/live-geometry-host.txt:10` (`clients=4 matched=0`), while the round-44 run is `.ufo/waves/round-44/receipts/live-geometry-host-r44.txt:5` (`clients=3 matched=0`); the paragraph pre-exists at base `6a1a905` (`SKILL.md:284`,`:290`; `git diff 6a1a905 e4678921 -- SKILL.md | grep -c '^[-+].*clients='` → `0`) and the same `clients=4` sits in the capability row `SKILL.md:225`, so read `SKILL.md:295-301` ("the dump holds four tiled") as the round-43 host run — the defect is adjacency, not the number.

E4 (F4) the tip receipts exist and the calibration's "tip" was the tip's grandparent: absent at `290cddea`, present at `8ac15c41` (`axis-tip.txt` blob `486dbbe821394d56e2fd031334ac9cf86924f13f`, `c1-after-tip.txt` `8b3b3310c7ef6ae8bbdbdcdad66b7484d5f714f8`, `c2-after-tip.txt` `89149342fdcd38d74af49928934aea611d0bb50e`), with `8ac15c41^` = `74c606a` and `8ac15c41^^` = `290cddea` (`git rev-list --count 74c606a..8ac15c41` → `1`) and `axis-tip.txt:4` naming `rev=74c606a1c7fd52a6bb85bb1c786529c926040c73` (the one commit `74c606a..8ac15c41` adds 599 files, 0 outside `.ufo/`) — read every calibration "tip" measurement as `290cddea`; F4 is closed.

E5 (F5) the w1 evidence pointers are `LATE`: `.ufo/waves/round-44/w1/` holds `0` files at `e4678921` and `03fa5c61`, `848` from `290cddea` through `HEAD`, and `.ufo/waves/round-44/w1-results.json` is absent at both pre-tip revisions — read `corpus/lessons/round-44.md:5` ("broke both v1 predicates"), `:7`, `:246` (`w1/ScrLessonSkeleton/c1-demo/`) and `SCORECARD.md:2566`,`:2573` against the tree at `290cddea` or later, never at the data commit; the finding stands unchanged.

E6 (F6) criterion 83 is unrunnable at the commit that published it: `corpus/QUALITY.md:413` names `.ufo/waves/round-44/w1/ScrQualityCriteria/check83.py` in its check line (`check83.py --repo . --rev <REV> --doc <PATH-IN-REPO> --prefix .ufo/`), which has `0` rows at `e4678921` and `03fa5c61` and `1` from `290cddea` (added by `290cddea`; the directory holds nine files there) — checkable only from `290cddea` onward; recorded, not repaired.

N1 (coverage, not one of the six) the two Round-44 claim rows carry no after *value*: `SCORECARD.md:2570` and `:2571` "give the after-state as" pointers ("see `receipts/c1-after-data.txt`", "…`c2-after-data.txt`"), while the receipts hold `fixtures=26/26 tool=present verdict=TARGET_MET` (`c1-after-data.txt:53`) and `admitted=1/1 verdict=TARGET_MET` (`c2-after-data.txt:29`); round-44 D2 (`corpus/lessons/round-44-verifier-spotcheck.md:107`) routes that append — a coverage gap, not a false statement.

## Part A — append-ready lines for the Round 47 section of `SCORECARD.md` (end)

---

## Part B — confirmation of each mismatch over committed bytes

Each row: the calibration's finding, the command that decides it, the observed output, and the verdict this seat reaches. Every
command and output is in `receipts/` (generated by `make-receipts.sh`, which prints command, output and exit code per block).

| # | finding (locator in `w2/ConnCalibration.md`) | command | observed | verdict |
|---|---|---|---|---|
| F1 | `LOG.md` round-44 bullet undercounts the lesson's mistakes (`:22`) | `grep -n 'Mistakes M44' LOG.md`; `grep -c '^\*\*M44-' corpus/lessons/round-44.md`; `grep -n 'Mistakes M44-1..9' SCORECARD.md` | `2499:` carries "Mistakes M44-1..7, Round-43 errata E1-E4"; count `9`; `2583:` publishes M44-1..9 | **mismatch confirmed** (a load-time count, correctly graded [LOW]) |
| F2 | the lesson and `id-guard.md` cite `assimilation/renumber-map.tsv`, "which does not exist" (`:32`) | `git cat-file -e <rev>:assimilation/renumber-map.tsv`; `git ls-tree <rev> -- .ufo/waves/round-44/assimilation/renumber-map.tsv`; `git log --diff-filter=A` | bare path rc `128` at `e4678921` and `HEAD`; wave-relative blob `c9639ce8…` at both; added by `e2289516`; map rows S311→S164, S312→S301 (provisional) | **path confirmed, conclusion withdrawn**: the artifact is committed; [MEDIUM] reduces to the path-prefix ambiguity |
| F3 | `SKILL.md`'s round-44 zone carries the round-43 `clients=4` transcript (`:50`) | `grep -n 'clients=4' SKILL.md`; `grep -n 'clients=' .ufo/waves/round-43/receipts/live-geometry-host.txt .ufo/waves/round-44/receipts/live-geometry-host-r44.txt`; `git diff 6a1a905 e4678921 -- SKILL.md \| grep -c '^[-+].*clients='` | `SKILL.md:301` (data commit `:299`) = round-43 `:10` (`clients=4`); round-44 `:5` is `clients=3`; diff count `0` (grep rc 1); base `6a1a905` carries the same text at `:284`/`:290`; `SKILL.md:225` also carries `clients=4` | **both counts true, defect is adjacency** — reclassified, not a wrong number |
| F5 | SCORECARD and the lesson cite w1 evidence absent at the data commit (`:61`) | `git ls-tree -r --name-only <rev> -- .ufo/waves/round-44/w1/ \| wc -l` and the `w1-results.json` count for `e4678921 03fa5c61 290cddea 8ac15c41 HEAD` | w1 files `0 0 848 848 848`; results `0 0 1 1 1`; all seven cited w1 paths exist at `HEAD` | **mismatch confirmed**: `LATE` in the QUALITY-83 sense |
| F6 | criterion 83's check cites `…/ScrQualityCriteria/check83.py`, absent at the data commit (`:70`) | `grep -n 'check83.py' corpus/QUALITY.md`; per-file `git ls-tree --name-only <rev> -- …/check83.py \| wc -l`; `git log --diff-filter=A` | `QUALITY.md:413`; per-file counts `0 0 1 1 1`; added by `290cddea` | **mismatch confirmed**: the criterion violates its own class at publication |
| F4 | tip receipts "do not exist yet at the data commit/tip" (`:75`) | `git rev-parse 8ac15c41^ 8ac15c41^^`; `git rev-list --count 74c606a..8ac15c41`; `git ls-tree <rev> -- …{c1-after-tip,c2-after-tip,axis-tip}.txt`; `grep -n 'rev=' axis-tip.txt` | `8ac15c41^` = `74c606a`, `^^` = `290cddea`; count `1`; 0 rows at `290cddea`, 3 blobs at `8ac15c41` and `HEAD`; `axis-tip.txt:4` → `rev=74c606a…` | **pending-by-design closed**: "tip" meant `290cddea` |

Coverage note (Part A, N1), not counted among the six: `sed -n '2570,2571p' SCORECARD.md` shows both Round-44 claim rows answering with
pointers; the values are in `receipts/c1-after-data.txt:53` and `receipts/c2-after-data.txt:29`; D2 (`:107`) routes the append.

---

## Part C — what this seat adds to the round-46 draft

The round-46 draft's rulings hold on re-reading. Five precision points differ or are new, and they are why the lines in Part A are
worded as they are:

1. **Locator drift.** The calibration cites `SKILL.md:293`/`:299` (its data-commit locators, still correct at `e4678921`); the round-46
   draft cites `:295`/`:301` (tip locators). Part A gives the tip locators and the data-commit ones in parentheses, so the line
   resolves at both revisions (`receipts/e3-skill-clients.txt`).
2. **`SKILL.md:225` carries the same `clients=4`** in the geometry capability row, at base `6a1a905` and at `HEAD`. The round-46 draft
   named only the prose paragraph, which understates how far the round-43 transcript reaches into the round-44 zone.
3. **`check83.py` count vs directory count.** The round-46 draft wrote "`0 0 1 1 1`" for the script; the `ScrQualityCriteria/`
   directory itself holds nine files at `290cddea` (`check82.py`…`check86.py`, `criteria.md`, `receipts.txt`, `run-checks.sh`,
   `verify-quotes.py`). Part A states the per-file count and the directory size separately so neither reads as the other.
4. **The block was never appended.** `grep -n 'Errata — round-44 closure D7' SCORECARD.md` → no row (rc 1); round-46's own lesson
   records the draft "not landed (routed)" (`corpus/lessons/round-46.md:361`); round-47 plans the landing (`SCORECARD.md:2652`). The
   round-46 text is therefore committed bytes at `.ufo/waves/round-46/w1/ScrErrata/errata.md`, not a SCORECARD row.
5. **E2's shape.** Confirmed as the draft states (blob `c9639ce8…`, freeze `e2289516`, four tracked renumber maps, rows S311→S164 and
   S312→S301 (provisional)), and the calibration's own reproduction `git ls-tree -r --name-only e4678921 -- assimilation/` prints
   nothing — the empty output that produced the [MEDIUM] (`receipts/e2-renumber.txt`).
6. **The "tip" is a commit, and the calibration's was not it.** `8ac15c41` is the round-44 tip ("round-44: w2 evidence (33 seat
   reports, results), tip receipts …"), an ancestor of `HEAD`; `74c606a..8ac15c41` is 599 files, all under `.ufo/` (0 outside), so
   the receipts' own `rev=74c606a…` measures the tip minus exactly that commit (`receipts/e4-tip-receipts.txt`).

---

## Verification

| check | command (outputs in `receipts/`) | result |
|---|---|---|
| finding list, D7 routing, draft status | `grep -n '^### F' .ufo/waves/round-44/w2/ConnCalibration.md`; `grep -n 'ConnCalibration' corpus/lessons/round-44-verifier-spotcheck.md`; `grep -n 'not landed (routed)' corpus/lessons/round-46.md`; `grep -n 'Errata — round-44 closure D7' SCORECARD.md` | `F1:22 F2:32 F3:50 F5:61 F6:70 F4:75`; `118:`; `361:`; no row, rc 1 (`findings-list.txt`) |
| E1 | `grep -n 'Mistakes M44' LOG.md`; count and headers; `grep -n 'Mistakes M44-1..9' SCORECARD.md`; M44-8/M44-9 evidence seats | `2499:`; `9` with headers `107…187`; `2583:`; `181:`, `189:` (`e1-log-range.txt`) |
| E2 | bare-path `git cat-file -e` (rc 128 twice); `git ls-tree` wave-relative (blob `c9639ce8…` twice); adding commit; four maps; three lesson citations + `id-guard.md:8`; map rows | as in Part B (`e2-renumber.txt`) |
| E3 | `grep -n 'clients=4' SKILL.md` (225, 301); `four tiled` (295); data-commit extraction (299); round-43 receipt `:10`; round-44 receipt `:5`; base `:225`/`:290`; diff count `0` | as in Part B (`e3-skill-clients.txt`) |
| E4 | `git rev-parse 8ac15c41^ 8ac15c41^^`; `git rev-list --count`; `git ls-tree` at `290cddea` and `8ac15c41`; `axis-tip.txt:4` | `74c606a`, `290cddea`; `1`; 0 rows vs 3 blobs; `rev=74c606a1c7fd…` (`e4-tip-receipts.txt`) |
| E5 | tree counts for five revisions; `w1-results.json` counts; lesson and SCORECARD pointer locators; existence of the seven cited w1 paths at `HEAD` | `0 0 848 848 848`; `0 0 1 1 1`; `5:`, `7:`, `246:`, `2566:`, `2573:`; seven × `1` (`e5-w1-paths.txt`) |
| E6 | `grep -n 'check83.py' corpus/QUALITY.md`; per-file counts for five revisions; adding commit; directory listing at `290cddea` | `413:`; `0 0 1 1 1`; `290cddea`; nine files (`e6-check83.txt`) |
| N1 | `sed -n '2570,2571p' SCORECARD.md`; the two after-data values; D2 locator | pointers; `fixtures=26/26 … TARGET_MET`, `admitted=1/1 … TARGET_MET`; `107:` (`n1-claim-rows.txt`) |
| quotes | `python3 verify-quotes.py` — each quote ≤ 25 words, the named receipt holds a `<locator>:` line containing it verbatim, and it appears in this file | `QUOTES: 18/18 verified` (`quotes-verify.txt`) |
| write footprint | `git status --porcelain -- .ufo/waves/round-47/w1/ScrErrataCal`; `git status --porcelain` | `?? .ufo/waves/round-47/w1/ScrErrataCal/`; lane shows only the pre-existing untracked round-46 `out.json.rows.tsv` and the round-47 dispatch files (`footprint.txt`) |

## Limits

- Documentation-only seat: no claim counter applies and none was run; nothing here is offered as a counter result.
- The lines in Part A are drafts for the L1. This seat wrote no lane file; `SCORECARD.md`, `LOG.md`, `SKILL.md`, `QUALITY.md` and the
  three lesson files are untouched (`git status` in `footprint.txt`).
- The calibration's verified-match ledger, the entries' content, the pins, the counters and the controls are out of scope; so is the
  round-44 D6 supersession and the round-45 entry's six sentence units (other R4 items, other seats).
- No host read, no `hyprctl`, no compositor action, no terminal launched, no tool installed or upgraded.
- Scratch `/fast/scratch/hyaku/mado-r47/ScrErrataCal/` held one extracted `SKILL.md` (2095 lines) and is deleted before this seat
  closes; no scratch path is cited as evidence.
