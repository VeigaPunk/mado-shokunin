# ScrErrataCal — round-47 w1 seat report

Seat `ScrErrataCal` (leaf; no subagent, no background job). Target **R4c**: the round-44 `w2/ConnCalibration.md` errata — confirm each
mismatch over committed bytes and draft the append-only SCORECARD erratum text, one line each.

Lane `mado-shokunin`. Round-47 base `60edb66e2f1cb90acc6e9442fc93ded0ca42d750`; every check ran at lane tip
`c24adef2632672325a4eef3e3492f6716ccb6d14`, whose `SCORECARD.md`, `LOG.md`, `SKILL.md`, `corpus/QUALITY.md` and the round-44/46 lesson
files are byte-identical to the round-47 base (`git diff --numstat 60edb66e c24adef2 -- <those paths>` → empty; the one commit between
them adds only `.ufo/waves/round-47/*`). Read-only seat: no lane file edited, no commit, no counter/fixture/control/pin/registration
touched, no host or compositor read, no tool installed.

## Deliverable

`.ufo/waves/round-47/w1/ScrErrataCal/errata.md` — three parts:

- **Part A, append-ready block for the Round 47 section of `SCORECARD.md`**: **six errata, E1-E6, one physical line each**, one per
  calibration finding in the calibration's own order (F1, F2, F3, F5, F6, F4), plus one coverage line **N1** that is explicitly not
  counted among the six. Nothing above is rewritten; no earlier `SCORECARD.md`, `LOG.md`, `SKILL.md`, `QUALITY.md` or lesson line is
  edited.
- **Part B**: the confirmation table — finding, command, observed output, verdict, receipt — for all six.
- **Part C**: six precision points this seat adds to the round-46 long-form draft.

## What was confirmed, and how

All commands are read-only git/grep/sed over committed bytes; each receipt prints the command, its output and its exit code
(`make-receipts.sh`, rerunnable, writes only into `receipts/`).

| # | ruling reached | decisive observation | receipt |
|---|---|---|---|
| E1 (F1) | stands: load-time count, not a false claim | `LOG.md:2499` "Mistakes M44-1..7, Round-43 errata E1-E4"; `grep -c '^\*\*M44-' corpus/lessons/round-44.md` → `9` (headers `107…187`); `SCORECARD.md:2583` publishes M44-1..9; M44-8 `:178`/M44-9 `:187` name w1 seats (`:181`, `:189`) | `e1-log-range.txt` |
| E2 (F2) | conclusion **withdrawn**: the map is committed wave-relative; [MEDIUM] → path-prefix ambiguity | bare `assimilation/renumber-map.tsv` → rc 128 at `e4678921` and `HEAD`; `git ls-tree <rev> -- .ufo/waves/round-44/assimilation/renumber-map.tsv` → blob `c9639ce84472eaccb9ea14007dbbc843e2e0e556` at both; added by freeze `e2289516`; four tracked renumber maps; rows S311→S164, S312→S301 (provisional) | `e2-renumber.txt` |
| E3 (F3) | reclassified: both counts true, defect is adjacency | `SKILL.md:301` (data commit `:299`) equals round-43 `.ufo/waves/round-43/receipts/live-geometry-host.txt:10` (`clients=4`); round-44 `.ufo/waves/round-44/receipts/live-geometry-host-r44.txt:5` is `clients=3`; `git diff 6a1a905 e4678921 -- SKILL.md \| grep -c '^[-+].*clients='` → `0`; base carries the text at `:284`/`:290`; `SKILL.md:225` also carries `clients=4` | `e3-skill-clients.txt` |
| E5 (F5) | stands: `LATE` | w1 tree files `0 0 848 848 848` and `w1-results.json` `0 0 1 1 1` at `e4678921 03fa5c61 290cddea 8ac15c41 HEAD`; the seven cited w1 paths exist at `HEAD` | `e5-w1-paths.txt` |
| E6 (F6) | stands: criterion 83 unrunnable where published | `corpus/QUALITY.md:413`; `check83.py` per-file counts `0 0 1 1 1`; added by `290cddea`; the directory holds nine files there | `e6-check83.txt` |
| E4 (F4) | **closed**: the receipts exist; "tip" meant the tip's grandparent | absent at `290cddea`, three blobs at `8ac15c41` (`486dbbe8…`, `8b3b3310…`, `89149342…`); `8ac15c41^` = `74c606a`, `^^` = `290cddea`; `git rev-list --count 74c606a..8ac15c41` → `1`; `axis-tip.txt:4` → `rev=74c606a…`; `8ac15c41` is the round-44 tip, ancestor of `HEAD`, and `74c606a..8ac15c41` is 599 files, 0 outside `.ufo/` | `e4-tip-receipts.txt` |
| N1 (coverage, not one of the six) | the Round-44 claim rows carry no after *value* | `SCORECARD.md:2570`/`:2571` answer with pointers; values are `fixtures=26/26 tool=present verdict=TARGET_MET` (`c1-after-data.txt:53`) and `admitted=1/1 verdict=TARGET_MET` (`c2-after-data.txt:29`); round-44 D2 `:107` routes the append | `n1-claim-rows.txt` |

Routing and draft status (receipt `findings-list.txt`): the calibration's finding list is `F1:22 F2:32 F3:50 F5:61 F6:70 F4:75`;
D7 is at `corpus/lessons/round-44-verifier-spotcheck.md:118` (its "correct by appended errata" clause at `:119`); the round-46 draft is
committed (`git ls-files .ufo/waves/round-46/w1/ScrErrata/errata.md` → 1 row) and round-46 recorded it "not landed (routed)"
(`corpus/lessons/round-46.md:361`); `SCORECARD.md` has **no** errata block yet (`grep -n 'Errata — round-44 closure D7' SCORECARD.md` →
no row, rc 1) and round-47's planned item 3 names the landing (`SCORECARD.md:2652`).

## Gates

- Documentation-only seat: **no claim counter applies** and none was run. Nothing here is offered as a counter result, and no axis
  checker was executed.
- Quote gate: `quotes.tsv` (18 rows) + `verify-quotes.py` — each quote ≤ 25 words, the named receipt holds a `<locator>:` line
  containing it verbatim (so the locator came from a `grep -n`), and the quote appears in `errata.md` → `QUOTES: 18/18 verified`,
  exit 0 (`receipts/quotes-verify.txt`). One row failed on first run (D7's clause is on `:119`, not `:118` — the D7 item wraps); the
  receipt was extended rather than the quote softened.
- Write-footprint gate: `git status --porcelain` in the lane shows only the pre-existing untracked round-46 `out.json.rows.tsv`, the
  round-47 dispatch files, sibling seats' round-47 directories, and this seat's directory (`receipts/footprint.txt`).

## Touched surfaces

- Written (all new, untracked): `.ufo/waves/round-47/w1/ScrErrataCal/{errata.md, make-receipts.sh, quotes.tsv, verify-quotes.py,
  receipts/*.txt}` and this report `.ufo/waves/round-47/w1/ScrErrataCal.md`.
- Read-only: `.ufo/waves/round-44/w2/ConnCalibration.md`; `.ufo/waves/round-46/w1/ScrErrata/{errata.md, receipts/*}`;
  `.ufo/waves/round-44/{assimilation/id-guard.md, assimilation/renumber-map.tsv, receipts/{c1-after-data,c2-after-data,live-geometry-host-r44,axis-tip}.txt}`;
  `.ufo/waves/round-43/receipts/live-geometry-host.txt`; `LOG.md`; `SCORECARD.md`; `SKILL.md`; `corpus/QUALITY.md`;
  `corpus/lessons/{round-44,round-44-verifier-spotcheck,round-46}.md`; git object reads at `e4678921`, `03fa5c61`, `290cddea`,
  `74c606a`, `8ac15c41`, `6a1a905`, `e2289516`, `HEAD`.
- No write outside the seat directory and the report; no `hyprctl` of any kind; no tool installed or upgraded.

## Out of scope / not done

- Round-44 **D6** (S290-S297 supersession), round-46 **R1** (entry `:57` citation), **R2** (`out.json.rows.tsv` digest) and **R3**
  (synthetic-material marker) are other R4 items and other seats' targets; not addressed here.
- The calibration's verified-match ledger, the entries' content, the pins, the counters and the controls were not re-litigated.
- The Part A lines are **drafts for the L1**: this seat wrote no lane file, so `SCORECARD.md` is unchanged by it.

## Findings / limits

1. **The round-46 draft's rulings hold**, with six precision points recorded in `errata.md` Part C: tip-vs-data-commit locator drift on
   `SKILL.md` (`:295`/`:301` vs `:293`/`:299`); `SKILL.md:225` also carries `clients=4`; `check83.py` per-file count `1` vs the
   nine-file `ScrQualityCriteria/` directory; the draft was never appended (so it is bytes, not a SCORECARD row); E2's shape
   (including the calibration's own empty `assimilation/` tree query); and the tip's identity with the 599-file/0-outside-`.ufo/`
   measure of `74c606a..8ac15c41`.
2. **F2 remains a real [MEDIUM]-class defect even though its conclusion is withdrawn**: a reader who follows the lesson's bare path gets
   rc 128 from `git cat-file`, exactly as the calibration saw. The erratum supplies the prefix; it does not repair the lesson.
3. **N1 is a coverage gap, not a false statement**, and is kept out of the six on purpose, matching the round-46 draft's own accounting.
4. **No line of Part A was executed as a counter or gate**; each is backed by the receipt row named in Part B.
5. Scratch `/fast/scratch/hyaku/mado-r47/ScrErrataCal/` (one extracted `SKILL.md`, 2095 lines) is deleted; no scratch path is cited as
   evidence. No tool installed (git, coreutils, python3 stdlib only).
