# ConnCalibration — self-assessment mismatches at base 0c89478

Base: `0c89478af821a6424c9ac922eafe02e39630cf4f` (round-45 base; commit "round-44
verifier spot-check", parent `8ac15c41` = round-44 lane tip). All checks ran
read-only on a scratch clone of the lane at the base commit
(`git clone -q --shared <lane> "$D"; git -C "$D" checkout -q --detach
0c89478…`; `git -C "$D" rev-parse --show-toplevel` = `$D`).

## Mismatches

### M1 — LOG.md round-44 bullet undercounts the lesson's mistakes (round-44 D7 F1: still open)
- Claim: LOG.md:2499 — `routed into \`corpus/lessons/round-44.md\` (Mistakes M44-1..7, Round-43 errata E1-E4)`.
- Observed: the lesson has 9 M44 mistakes: `grep -c '^\*\*M44-' corpus/lessons/round-44.md` → 9
  (M44-1..9, matching SCORECARD.md:2583 "Mistakes M44-1..9 mined").
- Command: `grep -c '^\*\*M44-' corpus/lessons/round-44.md`.
- Status: open; LOG never updated (LOG.md ends at line 2503, no append).

### M2 — lesson and id-guard cite `assimilation/renumber-map.tsv`, which is absent at base (round-44 D7 F2: still open)
- Claim: corpus/lessons/round-44.md:26, :71, :82 and
  .ufo/waves/round-44/assimilation/id-guard.md:8
  (`Mapping is by document (renumber-map.tsv); no staged id is carried.`).
- Observed: no such file in the tree: `git ls-tree -r --name-only 0c89478 assimilation/` → empty;
  `git ls-tree -r --name-only 0c89478 | grep -c renumber` → 0 (8 hits are prose mentions only).
- Command: `git ls-tree -r --name-only 0c89478 assimilation/`; `git show 0c89478:assimilation/renumber-map.tsv` → fatal.
- Status: open; no mapping artifact was ever committed.

### M3 — SCORECARD Round 44 claim rows carry no after value/verdict (round-44 D2: still open)
- Claim: SCORECARD.md:2570 (C1) and :2571 (C2): after-state cell =
  `-> see \`receipts/c1-after-data.txt\`` / `-> see \`receipts/c2-after-data.txt\``;
  self-verdict = `recorded in the round report from the receipts`.
- Observed: the values exist in the receipts: c1-after-data.txt
  `fixtures=26/26 tool=present verdict=TARGET_MET` exit 0; c2-after-data.txt
  `admitted=1/1 verdict=TARGET_MET` exit 0 — but are not published in the table.
- Command: `sed -n '2570,2571p' SCORECARD.md`; `cat .ufo/waves/round-44/receipts/c1-after-data.txt | tail -3`.
- Status: open (D2 fix was "append the values in the next SCORECARD section"; none appended).

### M4 — tip receipts name `74c606a`, not the lane tip (round-44 D3: still open)
- Claim (receipts' own rev fields): c1-after-tip.txt `rev=74c606a1c7fd52a6bb85bb1c786529c926040c73`;
  c2-after-tip.txt `rev=74c606a…`; axis-tip.txt `rev=74c606a…`.
- Observed: the lane tip at base is `8ac15c41` (base's parent;
  `git log --oneline -2 0c89478`). `74c606a` ≠ `8ac15c41`. No receipt states the
  equivalence: `grep -l '8ac15c41\|equivalent' .ufo/waves/round-44/receipts/*` → none.
- Command: `grep -H 'verdict=TARGET_MET rev=' .ufo/waves/round-44/receipts/*after-tip.txt`;
  `git log --oneline -2 0c89478`.
- Note: the equivalence itself holds de facto — `git diff --name-only 74c606a 8ac15c41 | grep -v '^.ufo/waves/round-44/'` → empty — but is unstated in the receipts.
- Status: open.

### M5 — SCORECARD Round 43 section says "Mistakes M43-1..8"; the round-43 lesson has 9 (round-43 closure D5 erratum: acknowledged, unamended)
- Claim: SCORECARD.md:2548 — `Mistakes M43-1..8 mined; …`.
- Observed: `grep -c '^\*\*M43-' corpus/lessons/round-43.md` → 9 (M43-1..9).
- Command: `grep -c '^\*\*M43-' corpus/lessons/round-43.md`.
- Status: acknowledged as erratum in the round-44 section (SCORECARD.md:2583
  "Erratum (round-43 closure D5): the Round 43 section's … should read M43-1..9"),
  but the Round 43 claim itself is unamended at base.

### M6 — PROVINCE tool inventory does not cover every tracked file under tools/ (PROVINCE vs `git ls-tree tools/`)
- Claim: PROVINCE.md:34 — `the inventory above covers every tracked file under \`tools/\``
  (round-23 wave-2 correction); table rows at PROVINCE.md:24-32 list 9 tools.
- Observed: `git ls-tree -r --name-only 0c89478 tools/` has 12 tracked files;
  `tools/mado-eventq.py`, `tools/mado-options.py`, `tools/mado-wsrules.py` appear in no
  PROVINCE row and no addendum
  (`grep -n -iE 'eventq|options\.py|wsrules' PROVINCE.md` → 0 hits; the only addendum
  heading is `## Round-38 addendum` at PROVINCE.md:86).
- Command: `git ls-tree -r --name-only 0c89478 tools/`; `grep -n -iE 'eventq|options\.py|wsrules' PROVINCE.md`.
- Status: open (three tracked lane tools unaccounted in the province inventory).

## Round-44 closure D2/D3/D7 — status

- D2 (SCORECARD rows lack after values): **open** (M3).
- D3 (tip receipts named 74c606a, not the tip): **open** (M4).
- D7 (w2/ConnCalibration.md content mismatches — recorded in lesson round-44
  "Routed defects" item 7, fix "correct by appended errata"):
  - F1 LOG mistake range (M44-1..7 vs 9): **open** (M1).
  - F2 renumber-map.tsv citations: **open** (M2).
  - F5 w1 paths cited before they landed: resolved temporally — at base all
    848 files under .ufo/waves/round-44/w1/ exist (incl. CritC1Cheat.md,
    CritC2Cheat.md, CritClaimSizing.md, RevC2Counter.md, CritFsPremise.md,
    ConnCrossClaim.md, ExecIndepA.md, ExecIndepB.md) and w1-results.json exists.
  - F6 QUALITY 83 check path absent at data commit: resolved temporally —
    `.ufo/waves/round-44/w1/ScrQualityCriteria/check83.py` exists at base.
  - F3 SKILL.md round-44 zone carries the round-43 host transcript (clients=4)
    vs round-44 live receipt clients=3: still present as a placement artifact
    (SKILL.md:225), not counted as a claim mismatch (w2's own class).
  - No appended errata found (lesson has no round-44 errata section; no
    ConnCalibration mention in corpus/lessons/round-44.md).

mismatches=6
