# ConnCalibration — wave w2 seat report (round 44)

Seat: ConnCalibration. Task: count mismatches between SCORECARD.md Round 44 / SHONEN.md / the
round-44 lesson's statements and observed repo state at the data commit
e46789213830597348fe96a351ae004d10587385. Calibration: self-assessment vs repo state.

Method: every checkable statement extracted from the three surfaces was verified with read-only
commands at e4678921 (and at tip 290cddea where the claim names the tip; the tracked claim files
SCORECARD.md, SHONEN.md, corpus/lessons/round-44.md are byte-identical between the two commits —
`git diff e4678921 290cddea -- <paths>` empty). Evidence copies: `receipts/` next to this report.
## Verdict

- **4 content mismatches** (F1, F2, F5, F6), **1 stale-transcript defect** (F3),
  **1 pending-by-design** (F4).
- SHONEN.md: no mismatch. Its four checklist items carry historical assertions, not round-44
  numbers; all referenced paths exist (`corpus/knowledge/executor-test-sufficiency.md`,
  `corpus/knowledge/config-health-report-r3.md`, `corpus/knowledge/province-accuracy-selfaudit.md`).
- All SCORECARD Round-44 numeric claims verified consistent with repo state (details below).

## Findings

### F1 [LOW] LOG.md round-44 bullet undercounts the lesson's mistakes (the M44-5 class)
Attacks: LOG.md round-44 statement vs lesson state.
- LOG.md:2499: `routed into \`corpus/lessons/round-44.md\` (Mistakes M44-1..7, Round-43 errata E1-E4)`.
- Observed: `grep -c '^\*\*M44-' corpus/lessons/round-44.md` → 9 (M44-1..9), matching
  SCORECARD.md:2583 ("Mistakes M44-1..9 mined") and the lesson's own nine M44 headers.
- Reproduction: `grep -c '^\*\*M44-' corpus/lessons/round-44.md`. 
- Note: the LOG bullet is time-indexed to protocol load (before w1 added M44-8/M44-9 from w1
  findings), so it is a stale count, not a false claim about what was routed at load. The round-44
  SCORECARD line (2583) has the correct count; the LOG line was not updated.

### F2 [MEDIUM] The lesson and the id guard cite `assimilation/renumber-map.tsv`, which does not exist at the data commit or the tip
Attacks: lesson content (corpus/lessons/round-44.md:26, :71, :82) and
.ufo/waves/round-44/assimilation/id-guard.md:8.
- `corpus/lessons/round-44.md:26`: `maps the package by document (\`assimilation/renumber-map.tsv\`): staged S311 … → held S164 … staged S312 … → new S301`.
- `corpus/lessons/round-44.md:71`: `id mapping is by document (\`assimilation/renumber-map.tsv\`), never arithmetic`.
- `corpus/lessons/round-44.md:82`: `**Old→new for the staged document** (\`assimilation/renumber-map.tsv\`)`.
- Observed: no `assimilation/` directory or any `renumber-map*` file exists in the repo at
  e4678921 or at HEAD: `git ls-tree -r --name-only e4678921 assimilation/` → empty;
  `git ls-tree -r --name-only HEAD assimilation/` → empty; `git log --oneline --all -- assimilation/` → empty;
  `git grep -l 'renumber-map.tsv'` hits only prose (lesson, id-guard.md, w1 spec/dispatch, w1 evidence).
- The mapping content itself lives in prose (lesson :82-84) and in the w1 evidence
  (.ufo/waves/round-44/w1/ConnStagedVsRegistry/matrix.md B8 records the scratch file "3 lines incl.
  header, both rows name the same document on both sides"); the artifact was never committed.
- Reproduction: `git ls-tree -r --name-only HEAD | grep -c renumber` → 0; `git show e4678921:assimilation/renumber-map.tsv` → fatal.
- The w1 reviewer already flagged the wording (CritAssimilation/findings.md §5.4 item 4: "Reword
  the renumber map to "by registered location/receipt""); the L1 decides whether to commit the map
  or fix the wording in the lesson.

### F3 [LOW] SKILL.md's round-44 zone carries the round-43 host-run transcript (clients=4) directly under the round-44 exit-map/D3 additions; the round-44 live receipt records clients=3
Attacks: SKILL.md data-commit placement (not one of the three named surfaces, but inside the
round-44 landing zone).
- SKILL.md:293 (data commit): `Host run 2026-10-26, no gkeep window open: the gkeep rule file declares \`size 420 500\` and the dump holds four tiled`; SKILL.md:299: `… clients=4 matched=0 … verdict=NO_MATCHING_CLIENT`.
- Observed: the round-44 live receipt `receipts/live-geometry-host-r44.txt` records `clients=3
  matched=0` and three clients (`Alacritty`, `zcode`, `grok-bot`), every `fullscreen` 0, exit 3.
- The paragraph pre-existed at base 6a1a905 (lines 284/290) and was pushed below the round-44
  insertions unchanged; because both rounds ran on 2026-10-26, the same-dated transcript sits
  adjacent to round-44 rows and reads as a round-44 host run.
- Reproduction: `sed -n '293p;299p' SKILL.md` vs `grep -o 'clients=[0-9]*' .ufo/waves/round-44/receipts/live-geometry-host-r44.txt`.

### F5 [MEDIUM] SCORECARD Round-44 and the lesson cite w1 evidence paths that are empty/absent at the data commit (they land only at the tip)
Attacks: SCORECARD.md:2566, :2573; corpus/lessons/round-44.md:5, :7, :22, :165, :181-183, :189-190, :246.
- SCORECARD.md:2566: `after wave \`w1\` (38 seats) met both v1 predicates with cheats and forgeries (\`w1/CritC1Cheat.md\`, \`w1/CritC2Cheat.md\`, \`w1/CritClaimSizing.md\`, \`w1/RevC2Counter.md\`) and showed the v1 premise wording ("a false report") wrong (\`w1/CritFsPremise.md\`)`.
- SCORECARD.md:2573: `(\`w1/ConnCrossClaim.md\`, \`w1/CritClaimSizing.md\` F10)`.
- Lesson :5: `.ufo/waves/round-44/w1-results.json`; lesson :7: `w1/ScrLessonSkeleton`; lesson :181-183: `w1/CritC2Cheat/frozen-F2-FORGED-PIN.txt`, `w1/RevC2Counter/log-forged_s164.txt`; lesson :246: `w1/ScrLessonSkeleton/c1-demo/`.
- Observed: at e4678921, `git ls-tree -r --name-only e4678921 .ufo/waves/round-44/w1/` → **0 files** and `w1-results.json` is absent; the whole w1 tree (848 files incl. results, reports, handoff) first appears at 290cddea. The v2 freeze 03fa5c6 also has 0 w1 files (registration-v2's `w1-results.json` reference is likewise dangling at its own revision).
- This is the M44-4 class (pointer whose target is not committed at the cited revision), now policed by the round's own new QUALITY criterion 83 (landed at the same data commit).
- Reproduction: `git ls-tree -r --name-only e4678921 .ufo/waves/round-44/w1/ | wc -l` → 0; `git ls-tree e4678921 .ufo/waves/round-44/w1-results.json` → empty; `git ls-tree -r --name-only 290cddea .ufo/waves/round-44/w1/ | wc -l` → 848.

### F6 [LOW] QUALITY 83's check command cites `.ufo/waves/round-44/w1/ScrQualityCriteria/check83.py`, absent at the data commit
- corpus/QUALITY.md:413: `Check: \`python3 -I .ufo/waves/round-44/w1/ScrQualityCriteria/check83.py --repo . --rev <REV> --doc <PATH-IN-REPO> --prefix .ufo/\``.
- Observed: `git ls-tree -r --name-only e4678921 .ufo/waves/round-44/w1/ScrQualityCriteria/` → empty; the checker exists only at the tip (290cddea). Same class as F5/M44-4.
- Reproduction: `git ls-tree -r --name-only e4678921 .ufo/waves/round-44/w1/ScrQualityCriteria/` → empty.

### F4 [INFO, pending-by-design] Lesson-referenced tip receipts do not exist yet at the data commit/tip
- Lesson "Census and measurements": `At the data commit / tip: \`receipts/c1-after-data.txt\`, \`receipts/c1-after-tip.txt\``; M44-7 fix: axis receipt `at the tip (\`receipts/axis-tip.txt\`, committed with the round's last commit)`.
- Observed at 290cddea: `receipts/c1-after-tip.txt`, `receipts/c2-after-tip.txt`,
  `receipts/axis-tip.txt` absent (axis-data.txt present, 3 MATCH at e4678921). Consistent with the
  fix's own plan (round-close commit after w2), so not counted as a mismatch.

## Verified-match ledger (all SCORECARD Round-44 statements that were checked and passed)

- Freeze/base/data hashes exist: e2289516a9a857f55cda7be635933e89b931c3da, 03fa5c618b089064a657b3d79d3d4272ae4b6894, 6a1a90528fe533cadee506a9fa3e9d13d15cc41f, e46789213830597348fe96a351ae004d10587385; base is an ancestor of the v1 freeze (`git merge-base --is-ancestor` → YES via 241196df).
- w1 (verified at tip 290cddea, where the w1 evidence was committed — see F5): `w1-results.json` seats=38, results=38; 38 `w1/*.md` reports exist (`missing md: []`).
- `receipts/axis-base.txt`: 3 MATCH rows (navigation 60/60, calibration 68/68, operability 12/12) at 6a1a905; `receipts/axis-data.txt`: 3 MATCH rows (navigation 61/61, calibration 71/71, operability 12/12) at e4678921 — matches SCORECARD "Axis table re-derived … 61/61; 71/71; 12/12".
- C1 before: `receipts/c1-v2-before-base.txt` `fixtures=11/26 … verdict=TARGET_MISSED` exit 1; v1 before `receipts/c1-before-base.txt` `fixtures=12/26` exit 1. C2 before: `receipts/c2-v2-before-base.txt` `admitted=0/1` exit 1; v1 before `receipts/c2-before-base.txt` `admitted=0/1` exit 1.
- C1 after: `receipts/c1-after-data.txt` `fixtures=26/26 tool=present verdict=TARGET_MET` exit 0, clauses a/b/b4/b5/e/g/r all 1, `selftest=94/94`, clause r `37/37`; **re-run by this seat** at e4678921: identical (exit 0).
- C2 after: `receipts/c2-after-data.txt` `admitted=1/1 verdict=TARGET_MET` exit 0, clauses a-j all 1, clause=c S164(new=0)+S298-S301(new=1), clause=g locator lines 1687/455/1150/681/475, clause=j twelve surfaces (report-size 1685, send 1732, x11 1751, ack 1514, setsize 354, configure 455, zero 1154, ack_configure 560, gtk-store 681, gtk-constrain 525, gtk-0x0 647, gkeep-id 449); **re-run by this seat** at e4678921: identical (exit 0).
- Controls: `receipts/ctl-c1-v2.txt` `CTL_C1v2 VERDICT: PASS (controls scoring TARGET_MET: 0 of 20; reference met: 1)`; `receipts/ctl-c2-v2.txt` `CTL_C2v2 VERDICT: PASS (wrong=0 of 11; positive admitted=1)`; v1 `ctl-c1.txt:18` `0 of 15`, `:2` REF met; `ctl-c2.txt:5` `0 of 3`.
- Tool identity: `tools/mado-geometry.py` == `.ufo/waves/round-44/c1/ctl-ref-tool-v2.py.txt` == git blob at e4678921 (sha256 1da3ddaed0d6e3cca32d3724daeb4a7fbd14939946ad57ab8db34bc0b2e31ff4); at the v2 freeze the tool sha256 = e3c2e4715059… (matches registration-v2 `sha256 \`e3c2e471…\``); selftest run: `MADO_GEOMETRY_SELFTEST: 94/94 passed`.
- Live receipt `receipts/live-geometry-host-r44.txt`: `NO_MATCHING_CLIENT`, exit 3, `clients=3`, every `fullscreen` 0, tool sha begins 1da3ddaed…, hyprland 0.56.2 efb5099 — matches SCORECARD capability row and lesson.
- Sources: base 234 rows → data 238 (`grep -c '^| S'`), S298-S301 new (tier A, mined, opened 2026-10-26, used-by names the entry); S164 diff base→data changes only its row (used-by cell appended `corpus/knowledge/hyprland-gkeep-size-request-r44.md`); knowledge files 60 → 61; README index row (line 72) and Frontier `### Round-44 gkeep size-request route` (line 304).
- Pins: all 8 sha256 in `receipts/fetch-sha256.txt` match the pinned bytes; mode 100644; GATE quotes word-bounded, present at lines 1687/455/1150/681/475, absent from the other four pins (verified by script).
- Entry `corpus/knowledge/hyprland-gkeep-size-request-r44.md`: census lines at :32 (`hyprland sendWindowSize xdg_setSize=1 x11_configure=1`) and :58 (`gkeep client default_size=420x500 size_request_calls=0 application_id=org.omarchy.gkeep`); `## What the staged predecessor said` at :64 lists exactly three non-adopted r12 sentences; onAck OBS present; `verified-at: 2026-10-26`; `recheck: 90d`.
- Refusals r13/r14/r15/r9 at lesson :37-40 with reasons and flips.
- QUALITY.md criteria 82-84 exist; 82 quotes `DOMAIN_META: domain=12 meta=5 window=34-43 default=1`; `python3 -I quality/ratio-domain-meta.py --repo . --rev 03fa5c618b089064a657b3d79d3d4272ae4b6894 --from 34 --to 43` prints exactly that (re-run by this seat, exit 0); QUALITY 83 (check83.py path), 84 (FORGED-PIN) present. `quality/ratio-domain-meta.py` tracked at e4678921 (mode 100755).
- Mistakes: `grep -c '^\*\*M44-' corpus/lessons/round-44.md` → 9 (SCORECARD 2583 says M44-1..9); `grep -c '^\*\*M43-' corpus/lessons/round-43.md` → 9; SCORECARD.md:2548 says "Mistakes M43-1..8" and the round-44 section (2583) documents the D5 erratum with the 9 count — self-consistent.
- SKILL.md: FULLSCREEN/MAXIMIZED/NOT_COMPARED rows, exit-map note (exit 5, tested before OK), D3 TILED correction (`read TILED as "not floating" only`; count at e4678921 = 1).
- PROVINCE.md: geometry row edited base→data, appending `Round 44: also reads each client's \`fullscreen\` integer (1 maximized, 2 fullscreen) … (FULLSCREEN, MAXIMIZED; top verdict NOT_COMPARED, exit 5); still no compositor read of its own (`.ufo/waves/round-44/registration-v2.md`)`.
- Host versions: hyprland 0.56.2-4 at efb50993780079460b0cbed1363e2166a2de1d9f (`hyprctl version` + `/var/lib/pacman/local/hyprland-0.56.2-4`), gtk4 1:4.24.1-1, wayland-protocols 1.49-1.
- Lesson Gate headers: `grep -c '^## Gate'` → 1; `grep -c '^GATE S'` → 5.
- Census: `receipts/census-before.txt` == `receipts/census-after-data.txt` byte-identical (W04 ×7: S030 S042 S045 S097 S119 S120 S121; W01 S277; exit 0).
- id-guard (`.ufo/waves/round-44/assimilation/id-guard.md`): collisions 42 (S203..S297), 0-3-space guard fires on indented row, column-zero does not.
- `considerthese/2026-10-25.md` exists; w1 named evidence files exist at the tip (CritC1Cheat, CritC2Cheat, CritClaimSizing, RevC2Counter, CritFsPremise, ConnCrossClaim; absent at e4678921, see F5).

## Environment / tooling
- No tools installed (read-only checks only; python3 stdlib).
- Scratch `/fast/scratch/hyaku/mado-r44/ConnCalibration/` used and deleted before finish; citable evidence is `receipts/` in this seat dir.
