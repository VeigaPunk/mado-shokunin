# Routed defect classes across rounds 39–44 — patterns (seat ConnLessonsPattern)

Author: seat ConnLessonsPattern (mado round 45, wave w1, hyaku run 9). Date: 2026-10-26.

Scope: `corpus/lessons/round-{39,40,41,43,44}-verifier-spotcheck.md` §6 (routed defects) plus the same rounds' lessons `## Mistakes`. Round 42 is excluded by assignment and has no lesson (M43-4); its closure items are seen through the round-43 lesson's "Round-42 closure items" section.

## 1. Corpus

| round | lesson M rows | §6 routed items |
|---|---|---|
| 39 | 2 (M39-1..2) | 3 (D1–D3) |
| 40 | 6 (M40-1..6) | 4 |
| 41 | 18 (M41-1..18) | 4 |
| 43 | 9 (M43-1..9) | 9 (D1–D7 + driver + open) |
| 44 | 9 (M44-1..9) | 7 (D1–D7) |

44 mistakes over 5 lessons; 27 routed items over 5 closures. Counts computed with `grep -cE '^\*\*M[34][0-9]-' corpus/lessons/round-*.md` (2/6/18/9/9).

## 2. Clusters (class → members → recurrence)

### C-A. Predicate health — holes, post-scoring repair, vacuous clauses (largest class, ~16 hits)
- M39-1 (a registration named counters its freeze commit did not hold) — round-39.md:94
- M40-2 (do-nothing control reaches target; unsandboxed judge) — round-40.md:94
- M40-5 / M41-7 / M41-9 (predicate repaired / falsified after seats scored; the same pattern realized three rounds) — round-40.md:127, round-41.md:138, round-41.md:153
- M41-10 (harness reads the fixture instead of executing it), M41-11 (teeth clause gameable via path tests/self-fingerprints), M41-14 (C2 gate admitted 8 fabrications + 29 mutants), M41-15 (control suite nonce-flaky) — round-41.md:169, :185, :224, :241
- M43-8 (coverage predicate counted citations instead of enumerating the chain) — round-43.md:183
- M44-6 (declared residuals left as prose, no kill rule; next round re-registered instead of building on them), M44-8 (four rounds of C2 pins digest-checked only for new ids — vacuous hold) — round-44.md:156, :178
- Routed: round-39 D1 (predicate variance), round-41 §6 item 2 (tighten C1/C2), round-43 D6 (open predicate defects), round-44 D5 (open predicate defects).

The freeze addresses specific holes (below) but not the process: each closure routes the surviving holes, and the next round re-registers. M44-6 names this: "declared residuals left as prose, with no kill rule."

### C-B. Evidence pointers — existence-at-revision, tip receipts, computed locators (~14 hits)
- M41-4 (tip observable claimed without committed receipt; the instrument naming the rule scoped to another round) — round-41.md:107
- M43-1 (prose locator named lines that do not contain the claim; typed, not computed), M43-7 (single-line locators for two-line quotes — computed for the start, read as the whole fact) — round-43.md:113, :174
- M43-3 (pointer to a LOG.md entry that was never written), M43-5 (excerpt header asserted, not computed) — round-43.md:135, :153
- M44-1 (refusal reason under-cites the links it asserts — the locator class in prose), M44-4 (bare-path citations to files that did not exist at the data commit; typed locator range) — round-44.md:107, :135
- M44-7 (no committed axis receipt at the closing tip) — round-44.md:171
- Routed: round-40 §6 item 2 (tip axis receipt), round-43 D1 (lesson locator), D4 (entry citations pre-landing), D7 (tip receipt), round-44 D3 (tip receipts name `74c606a`, not the tip `8ac15c41`), D7 (ConnCalibration w1 paths cited before they landed).

Criteria 69, 77, 79, 80, 83 cover slices; nonetheless D3 recurred despite criterion 69 (see §4, proposal B).

### C-C. Counts published without recompute/definition (~5 hits)
- M43-2 (control tally stated three ways), M44-5 (registration seat count under-counted; published mistake range stopped one short; lesson carried nine) — round-43.md:127, round-44.md:147
- M41-18 (relayed entry count wrong: eight vs nine) — round-41.md:275
- Routed: round-44 D2 (SCORECARD rows lack after values/verdicts), D4 (nonce-dependent base share — "a before number that does not reproduce is not a count").

Criterion 78 covers control tallies; the seat-count/mistake-range family (M44-5, D2) is not covered.

### C-D. Driver/wave-tree hygiene — untracked artifacts, lost results, completion-as-success (~5 hits)
- M41-3 (dispatch marker untracked again one round after round-40 §6 item 1), M41-16 (kernel restart dropped every w1-results.json entry), M43-6 (a driver `complete` line + clean `git status` read as success for a round that spawned zero seats) — round-41.md:96, :252, round-43.md:162
- Routed: round-39 D3 (three dead seats), round-40 §6 item 1 (untracked marker), round-41 §6 item 1 (two untracked scratch files).

Criteria 70 (markers) and 81 (closure rows from three channels) were the fixes; 81 landed after M43-6.

### C-E. Session material / privacy (1 routed, highest severity)
- Routed: round-44 D1 — two tracked live `clients -j` dumps at `8ac15c41` (`round-43/w1/ExecLiveHost/host-clients-live.json`, `round-43/w2/SentLiveRun/dump-now.json`) carrying 4 live window titles each; violates SKILL.md:343 rule 4 ("Session material stays shape-only").
- No lesson M row backs this class — itself a finding (see §4 proposal C).
- Precedent: considerthese/2026-10-26.md proposal 1 (a 190 KB host socket table committed to the public repo; rounds 38+).

### C-F. Supersession/premise wording (~3–4 hits)
- M44-2 (row title restates the refuted premise), M44-3 (tool licence row broader than the code under it), M44-9 (v1 registration called a documented report "a false report") — round-44.md:119, :128, :187
- Routed: round-43 D2 then round-44 D6 (S293 / S290–S297 cell supersession deferred twice).

## 3. What this round's freeze already addresses (registration.md, freeze 22a8ded)

- **Seeded counter (C1)** — default seed 45, seeded output names, "a bare run reproduces — round-44 closure D4": addresses D4 (nonce-dependent base share), M41-15 (nonce-flaky suite), M41-2 (deterministic one-fixture margin).
- **Locator width bound (C2 clause j, ≤30 lines)**: addresses round-44 D5's clause-j hole (whole-file locators admitted 7 forgeries) and the locator half of round-43 D6.
- **Do-nothing/forged controls rejected (C2)**: ctl-c2.txt P admitted, C2-BASE / R14-COPY / SHELL / WIDE-RANGE / HIDDEN-LINE / FORGED-PIN / FALSE-URL / PROSE-CENSUS / ANCHOR-PAST-EOF rejected — addresses M41-14, M44-8 (FORGED-PIN; T1–T4 carried from r44 v2), round-44 D5.
- **C1 clause r (no hyprctl/journalctl/wlr-randr/wayland-info on PATH)**: addresses the M40-4 class (read-only safety over every input that can reach the verb).
- Observation: C1's selftest floor `s` is ≥30, below the round-44 geometry-states precedent of 80 (set in M44-6 to make K13 fail). Floors are per-tool, but if uniformity was intended this is a regression of the raised-floor class; declared as an observation, not a gate.
- Not frozen (listed as "not claims" riding the round): D1/session material (planned as a QUALITY criterion + gate from considerthese proposal 1), D2 (SCORECARD after-values), D3 (tip receipts at the final tip), D6 (S290–S297 supersession), D7 (ConnCalibration errata).

## 4. Proposed criteria (≤3; next free numbers are 85–87, QUALITY currently ends at 84)

### Proposal A — criterion 85: open-predicate residuals carry a kill rule and a demonstrated fail
Text: a predicate registration that declares residuals names, for each residual, the exact committing input that exposes it (a cheat/mutant/forgery control or a named fixture class), its observed score, and the kill rule that would make it fail; a residual without such an input, or with an input that does not fail, is a freeze violation and the predicate is not reusable until re-registered before any scoring.

Backing rows: M44-6 (round-44.md:156), M41-14 (round-41.md:224), M43-8 (round-43.md:183); routed R43 D6, R44 D5. Able-to-fail demo: R43 D6's own pair — C1 cheats 4 and 6 reach MET, C2 v2 admits 14/14 do-nothing and 6/16 mutants, check-locators 12/37 mutants — was routed with no kill rule and recurred as R44 D5.

### Proposal B — criterion 86: tip receipts name the closing tip (extends 69)
Text: a receipt whose name ends in `-tip` and is cited by a round's report carries the closing tip's hex in its bytes (`rev=<tip>`) or an explicit equivalence statement naming both revisions; a receipt naming any earlier revision without the equivalence statement is a violation at the closing tip.

Backing rows: M44-7 (round-44.md:171), M41-4 (round-41.md:107); routed R40 §6 item 2 (round-40-verifier-spotcheck.md:92), R43 D7 (round-43-verifier-spotcheck.md:109), R44 D3 (round-44-verifier-spotcheck.md:110). Able-to-fail: R44 D3's own case — the after-tip receipts name `74c606a`, the closing tip is `8ac15c41`; criterion 69 passes because the token exists in some receipt, so the extension is what fails it.

### Proposal C — criterion 87: session material stays shape-only in tracked bytes
Text: no tracked file (fetch/receipt/seat output) carries session-identifying fields — window `title`/`initialTitle`, monitor serials/descriptions, `/proc/*`, keyring/ssh names, home-directory listings; a live dump is projected to its shape-only keys before commit, verified by scanning the round's committed bytes.

Backing: no Mistakes row exists yet (finding: round-44 D1 was routed but never mined into an M row). Evidence: round-44-verifier-spotcheck.md:98 (D1), SKILL.md:343 rule 4, considerthese/2026-10-26.md:47 proposal 1. Able-to-fail at base: `host-clients-live.json` and `dump-now.json` at `8ac15c41` (4 titles each). The registration plans this as the proposal-1 criterion + gate; this proposal gives it a concrete check.

## 5. Secondary candidates (not proposed)
- M44-1 reason-coverage criterion (the lesson itself names it "the first candidate for a quality/ criterion" — round-44.md:117).
- M44-5 count-recompute for seat counts/mistake ranges (extends 78).
- M43-9 INF-universal Basis rule (already a lesson rule — round-43.md:191 — could be promoted).

## 6. Risks
- The freeze's controls target the specific R44 D4/D5, M40-4, M44-8 holes; the class-level process (post-scoring re-registration) is not eliminated — C1's own kill rule explicitly permits a v2 re-registration when w1 finds a hole before data, so the M40-5/M41-7 disclosure pattern is likely to repeat; Proposal A is the only conversion of declared holes into kill rules.
- The round-42 lesson gap (M43-4) means one closure's routed items are only visible through round-43's closure-items section.
- Session material has no Mistakes row; minting one (e.g. M44-10) in the next append would give criterion 87 its canonical lesson backing.
