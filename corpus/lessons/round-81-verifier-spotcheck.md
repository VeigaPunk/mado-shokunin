author: hyaku closure (non-author integrator, @m_zfl)

# round-81 verifier spot-check — mado (non-author)

Round 81, lane `mado`, base `c702094ace5dd9b2b5e152951b4b2f4dd578f8b6`, landing tip
`2cbd3a137d16ed8f81874ed9b566acc270b9cb79` (lane `master`, pushed). Verified from committed bytes;
the only executable run against the lane's surfaces is the fleet's read-only
`sources-census.sh` (PROTOCOL §Gate standard: a sibling gate is verified from its committed
evidence, never executed).

## Conformance (PROTOCOL §Round-robin step 1)

- **Report.** `.ufo/reports/round-81/mado.md` is committed in the fleet repo by the lane identity:
  `git log --format='%an %ae %H' -- .ufo/reports/round-81/mado.md` → `mado-shokunin
  mado@shokunin.local 3b42e0336ee4be6a12a2cfda18a9bcd12107dedd`, committed 2026-11-04 09:58:05
  -0300 — after the lane tip `2cbd3a13` (09:57:43) and before the driver's `complete` line
  (09:58:30). One commit only; the report was filed once, not rewritten.
- **SHONEN.** One `## SHONEN` heading; `grep -c '^- \[~\]'` → 4, `^- \[x\]` → 0, `^- \[ \]` → 0,
  matching the four boxes in `SHONEN.md`. Every `[~]` carries a pointer; no `[x]` is claimed.
- **Cited commits.** The eight hashes the report relies on — base `c702094a`, freeze `0e2ccd2a`,
  `6fffb0db`, `f3eb70c7`, `6006feb5`, `2034761b`, `6ac5863f`, tip `2cbd3a13` — all resolve and
  every one is an ancestor of `refs/heads/master` (`git merge-base --is-ancestor <hash> master`,
  tested against the branch ref, never `@{u}`).
- **Lane cleanliness.** `git -C mado-shokunin status --porcelain` is empty;
  `jj-lane.sh state` prints `branch=master local=2cbd3a13 remote=2cbd3a13 ahead=0 behind=0
  head=detached tracked=0 untracked=0`; `git ls-remote origin refs/heads/master` prints
  `2cbd3a137d16ed8f81874ed9b566acc270b9cb79`.
- **Prompt.** `.ufo/prompts/mado-round-81.md` renders `templates/round-prompt.md` with 0 content
  mismatches over the 140 template lines after substitution (only line 1's placeholder differs from
  my render; the file carries the real path) and then the hyaku addendum §6 (704 lines total).
  It carries the round-level contract — mission/axes binding (§1), the 1–3 claim rule (§2), the
  frontier step (§2b), the L2 floor of ≥8 seats in one batched call (§3, matching MISSION.md §L2
  concurrency; MISSION carries only the advisory bucket table, so no route-map conflict), the
  report contract (§4) — and all five child-lane items: report path/filename (§4),
  commit-then-push ordering (§5), `SHONEN` heading (§4), commit-hash citation rule (§4/§6.4), and
  lane write scope (§3).
- **Status.** `ok` — a real report naming committed round work. The defects below are
  status-neutral.

## Claims re-check (against 2cbd3a13)

### C1 — coverage (capability acquisition) — improved

Re-measured with plain counts over committed bytes:

- `git show 2cbd3a13:.ufo/waves/round-81/controls/c1-cases-r81.json | jq '.cases|length'` → **39**.
- `jq -S '.cases[0:33]'` of the r81 set vs `jq -S '.cases'` of
  `.ufo/waves/round-80/controls/c1-cases-r80.json` → `diff -q` empty: **33/33 carried
  parsed-equal**.
- New case names (`comm -23` of the two name lists): `auto-all-four-edge`, `auto-corner-edge`,
  `auto-dynamic-band-refused`, `auto-left-dock`, `auto-parallel-edge`, `overflow-tie-negative` —
  the six classes the report names.
- `MUTATIONS` in `quality/counters/c1-r81-overflow-auto.py` → **28** entries (`MUTANTS = 28`,
  `CASES = 39`, `CARRIED = 33`, `BASE_EXPECT = 33`).
- `sha256sum` of the control set → **ab8154a1d4bc5d2a0f58bef8aeb675605e50ecfe932406b39b0a0c2df0533d52**
  (matches the receipt's `MADO_R81_CONTROL` line and the report's `ab8154a1…`).
- `tools/mado-barfoot.py` `VERSION`: `r80-v1` at base → `r81-v1` at tip; `cbox_round` and
  `arranged_box` exist at the tip and not at the base; tool blob `0e9fa220…` at `f3eb70c7` equals
  the blob at `2cbd3a13`.

Evidence-verified (lane gate; not executed by the integrator): the committed
`receipts/control-c1-r81-at-base.txt` prints `cases=39 correct=33 mutants=28 killed=20
base_correct=33/39 carried=33/33 tool_selftest=111/111 verdict=TARGET_MISSED` rc 1 at
`rev=c702094a`; `receipts/measurement-c1-r81.txt` prints `correct=39 … tool_selftest=121/121
verdict=TARGET_MET` rc 0 at `rev=0e2ccd2a`; `receipts/measurement-c1-r81-at-tip.txt` prints the
same at `rev=f3eb70c7` with `tool_sha256=a129a435…`. The registry row `mado-r81-barfoot-counter`
(`SKILL.md:799`) is a gate with its verdict map and `--selftest` (72/72, committed in the row).
Because the tool blob is identical at `f3eb70c7` and the tip, the measured tool bytes are the
landing bytes. Verdict: **improved**.

### C2 — operability (capability acquisition) — improved

Re-measured:

- `jq '(.cases|length), ([.cases[].skill_anchor]|unique|length)'` →
  **26 cases / 26 distinct anchors**; 21 of the 26 cases carry a kind in the counter's
  `SHAPE_KINDS` (AST over the committed counter) = `SHAPES = 21`.
- Counter constants: `CASES = 26`, `CARRIED = 24`, `SHAPES = 21`, `MUTANTS = 23`; `MUTATIONS`
  holds **23** entries.
- `sha256sum` of the control set →
  **ae7ee90ebd1a6ff2c590c12ca3b8c925d26d8a47ca33bcd16af038f138c1a7f6** (matches the receipt's
  `MADO_R81_CONTROLS` line and the report's `ae7ee90e…`).
- The two new runbook rows are `SKILL.md:270-271` (action column, `pgrep -x waybar`); the three
  r81 registry rows are `SKILL.md:798-800`; the r80 rows are `:795-797` — the report's D2
  pointers are exact.
- Tree binding: `SKILL.md` blob `8f91a483…` and `tools/mado-barfoot.py` blob `0e9fa220…` are
  identical at `f3eb70c7` and at `2cbd3a13`, so the at-tip measurement's bound tree is the
  landing tree.

Evidence-verified (lane gate not executed): `receipts/measurement-c2-r81-at-tip.txt` prints
`cases=26 executed=26 matched=26 shapes=21/21 anchors=26/26 rows=26/26 control_new=0/2 mutants=23
killed=23 verdict=TARGET_MET tree=bound` rc 0 at `rev=f3eb70c7`, with the control line
`control_all=15/26` printed as an observation, never a predicate. The before-state is a setup
refusal, not an invented measurement: `receipts/control-c2-held-instrument-r81.txt` prints
`ERROR (stage=setup control set carries 26 cases, frozen target expects 24)` rc 2 and
`receipts/control-c2-r81-at-base.txt` prints `ERROR (stage=setup SKILL.md in the working tree is
not the measured revision's bytes)` rc 2. Registry row `mado-r81-runbook` (`SKILL.md:800`) is a
gate with its verdict map and `--selftest` (88/88, committed in the row). Verdict: **improved**.

### Harm watch

- `git diff c702094a 2cbd3a13 -- SCORECARD.md`: no axis row changed; the changes are an in-place
  paragraph edit in the round-80 section (defect R2 below) plus the appended round-81 section.
- Knowledge index **99/99 → 100/100**: `git ls-tree -r --name-only <rev> corpus/knowledge/ | wc -l`
  → 99 at base, 100 at tip; README `^\| \`knowledge/` rows → 99, 100.
- Instrument ledger **146 → 148**: `quality/tool-ledger.md` `^\| \`(tools|quality)/` rows → 146,
  148.
- Registry **412 → 415 rows** with **0 removed lines** in `corpus/SOURCES.md` (three appended rows,
  no older cell moved).
- Gate and held instruments byte-identical at base and tip: `quality/landing-counters.sh`
  `fd579df8…`, `check-tool-ledger.py` `2ab958bb…`, `check-axis-scores.py` `7ae3b8b2…`,
  `check-index.py` `ce58cbdd…`, `tools/mado-verify.sh` `7956c787…` (`git rev-parse <rev>:<path>`),
  plus the committed `receipts/harm-watch-r81.txt` (`MADO_SELFTEST: 460/460`,
  `MADO_AXIS: checked=3 mismatched=0`).
- The only in-place prior-round edit outside the section below is the blank-line removal before
  M80-6 in `corpus/lessons/round-80.md` (the round-80 closure's D4, disclosed in the report).

No axis is harmed.

## Axis verdicts (agree with the MANIFEST entry)

| axis | verdict | basis |
|---|---|---|
| coverage | improved | C1 39/39 vs held 33/39 on the frozen set, 28/28 mutants; one net-new admitted entry on new ground, index 99/99 → 100/100 |
| operability | improved | C2 26/26 cases/anchors, 21/21 shape-kind cases, 23/23 mutants; two new runbook rows and two new gate registry rows |
| depth | unchanged | no depth claim; existing rubrics and held instruments untouched |
| freshness | unchanged | no freshness claim; the live join is an observation, the dormant value stays operator-owned |
| calibration | unchanged | axis table `mismatched=0`; the report names its limits and the wave evidence gap |
| adjacency | unchanged | the connector seat found no sibling claim on either ground; no scope absorbed |

## Discernment spot-check (LEARNING.md — checked from outside)

| item | decision | re-opened source | agree/disagree | reason |
|---|---|---|---|---|
| S478 | admit | live `https://raw.githubusercontent.com/hyprwm/hyprutils/v0.14.0/src/math/Box.cpp` plus committed `fetch/S478.bin` | agree | live fetch sha256 `2d04de99…` equals the pin and the row; `CBox::round` at `:51-63`, quote `    double newW     = x + w - roundedX;` verbatim at `:54` (8 tokens, ≤25) |
| S479 | admit | live `https://raw.githubusercontent.com/hyprwm/Hyprland/efb50993780079460b0cbed1363e2166a2de1d9f/CMakeLists.txt` plus committed `fetch/S479.bin` | agree | live fetch sha256 `97b8028a…` equals the pin; `set(HYPRUTILS_MINIMUM_VERSION 0.14.0)` at `:150`, exactly the row's quote (1 token) |
| S480 | admit | live `https://raw.githubusercontent.com/hyprwm/hyprutils/v0.14.2/src/math/Box.cpp` plus committed `fetch/S480.bin` | agree | live fetch sha256 `2d04de99…`, byte-identical to S478 (`cmp` over the committed pins is empty); quote `    double newH     = y + h - roundedY;` at `:55` (8 tokens) |
| staged `knowledge/corpus/knowledge/host-bar-producers-r28.md` | reject | `/home/vgpnk/Projects/shokuknow/merge/mado/knowledge/corpus/knowledge/host-bar-producers-r28.md` (read) plus the lane registry and `assimilation/collisions` | agree | the entry amends `host-bar-and-idle-binding-r26.md`, which is absent from the lane's `corpus/knowledge/`, so adoption alone dangles the parent; S224/S228/S231 are absent from the lane registry (`reg=0`); its host-config claim rests on the 6354 B `.config/waybar/config.jsonc` read 2026-10-23; the flip (re-read the host, renumber by document, adopt both entries) is the correct condition |

Census: `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root
/home/vgpnk/Projects/shokunin mado` → **exit 0** (`ok`, the standing W04 duplicate-URL warnings and
W01 S277). Rows 412 → 415 at the tip.

## Trend verdicts (evidence)

- **expansion — improved.** One net-new admitted `corpus/knowledge/` entry on ground the coverage
  map did not hold (the composition's rounding and auto-zone gate), `source:` S478/S479/S480;
  index 99/99 → 100/100; registry 412 → 415; two capability rows demonstrated this round.
- **quality — improved.** The round-80 §11 limits for the overflow tie, the auto gate and the
  vertical zone are superseded by anchored accounts; five mistakes are mined (M81-1…M81-5), four
  of them with byte-exact pointers; 28 + 23 mutants are killed; the hermetic gate and every held
  instrument are byte-identical at base and tip; no admitted entry was found failing its re-check.
- **discernment — improved.** This non-author spot-check re-opens three admits and the reject and
  agrees on all four; the round's own rules were falsified against live output before the freeze
  (the entity rule and the `.strip()` matcher, M81-1/M81-2); the assimilation verdict is a refusal
  with a count (94 collisions) and a flip condition.

## Routed defects (lane fixes next round; status-neutral)

- **R1 — five attack seats empty.** Both reviewers, the critic, the mutation-tester and the
  sentinel settled with zero output (`w1-results.json` 14 seats, 5 with `output` length 0; no seat
  directory), so the claims have no independent attack artifact and the lane's `check-wave-done`
  gate reads `MISSING` (`dispatch-mismatch missing=5`, exit 1). The round discloses this; next
  round the attack seats must produce artifacts (or the wave must not seat them and the gate red
  must be resolved) before the claims are called attacked.
- **R2 — round-81 disclosure written into the round-80 SCORECARD section.** The tip's round-80
  `**Evidence.**` paragraph (under `## Round 80`, line 4615) now carries the round-81
  `w1-results.json` and the five-empty-seats/`wave-done-r81` sentence, while the round-81 section's
  Evidence block lacks it. Keep prior-round sections unedited; carry the disclosure in the
  round-81 section (append-only correction).
- **R3 — C2 counter docstring drift.** `quality/counters/c2-r81-runbook.py` still opens
  `PRED-C2-r79-v1` and its contract block says `cases=24 … shapes=19/19 … mutants=16`, while the
  code holds `CASES=26`, `SHAPES=21`, `MUTANTS=23`. The report's F6 names only the label; extend
  the F3/F6 repair to the contract block next round (the frozen bytes are cited by sha256 this
  round).
- **R4 — instrument selftest tallies lack a receipt.** `72/72` and `88/88` are committed in the
  `SKILL.md:799`/`:800` registry rows with their commands, but there is no committed
  observed-output receipt, and the report's work-item bullet states the tallies without a pointer.
  Add the `--selftest` transcript next round.
- **R5 — round-80 closure D1–D3 not evidenced as corrections.** No labelled erratum for the
  round-80 report's rewritten passages exists (history is `6fccb49` → `90895076` only), and the
  filed round-80 report still cites `corpus/README.md:180` (its row is at `:181` at the round-80
  tip) and `SKILL.md:786-789` (the r80 rows are `:792-794` at that tip). D2/D3 as worded describe
  the round-81 report's own pointers, not those supersessions. Append a labelled erratum naming the
  superseded text, or mark D1–D3 open.
- **R6 (minor) — wave counts carry no counting command.** The seat tally (14/9/5) and the
  4/14 = 28.6 % attack share point at `w1-results.json` and `w1-spec.json` but print no `jq`
  command; add one next round (they re-derive exactly: `jq '.results|length'` → 14,
  `jq '[.results[]|select((.output//"")|length==0)]|length'` → 5, roles → 2 reviewer / 1 critic /
  1 mutation-tester).

## Summary

Step 1 passes (`ok`); both claims were re-measured (counts, parity, hashes, tool/tree blobs) and
their gate evidence verified at the cited revisions without executing a sibling gate; no axis is
harmed; the non-author spot-check agrees with the gate's three admits and its reject. **Admit.**
