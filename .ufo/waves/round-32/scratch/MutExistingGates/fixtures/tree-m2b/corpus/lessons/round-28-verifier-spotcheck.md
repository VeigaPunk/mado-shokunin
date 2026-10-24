author: hyaku closure (non-author integrator, @m_kfc)

# mado round 28 — non-author verifier spot-check

Date: 2026-10-24. Lane tip at closure: `3565f13786ca563f29021db733c2d436d70c77cd` (branch `master`,
ahead=0, working tree clean). Report: `.ufo/reports/round-28/mado.md` @ fleet `6c0119f` (author
`mado-shokunin`). Round judged on the frozen registration `.ufo/waves/round-28/registration.md`
(bytes identical at 5198cc8, 123d8cd, and tip — `diff` clean).

## Step-1 conformance

| check | result |
|---|---|
| report committed by lane identity | PASS — `git log --format='%an %H' -- .ufo/reports/round-28/mado.md` → `mado-shokunin 6c0119facc452518fad181c66aff2d1a65f5c518` |
| SHONEN heading, one line per box | PASS — 4 lines, all `[~]` with pointers |
| cited commits exist + ancestor of branch | PASS — `git merge-base --is-ancestor <h> master` for 317ff19c, b84348d, 56ef773, 5198cc8, 123d8cd, 4f61006, 317ff19, 77cdda86, 9ea706c3, 3565f13, 77cdda869ec…, dac4aef, 20022a65 — all ok (HEAD detached as expected for jj colocated repo; tested vs `master`) |
| no uncommitted round work / pushed | PASS — `git status --porcelain` empty; `jj-lane.sh state` → `ahead=0 behind=0` |
| prompt carries template contract | PASS — `.ufo/prompts/mado-round-28.md` = canonical `templates/round-prompt.md` §§1–5 verbatim (all five child-lane items: report path, commit-before-report, SHONEN heading, landed-hash citation rule, write scope) + hyaku addendum §6 |

No conformance defects that change status. Trivial: `evidence/census-end.txt` dropped the literal
`exit=0` trailer line vs the start receipt's format (warnings + `ok` line byte-identical; census
re-run by this closure exits 0).

## Per-claim re-check (commands run by this closure, outputs observed)

Counters frozen pre-data: `c1/count.py` sha256 `dcca084f…` and `c2/count.py` sha256 `c0415c9a…`
from `4f61006` (before the data commit `317ff19`) through tip — verified by `git show <rev>:path | sha256sum`
across 5198cc8/123d8cd/4f61006/317ff19/77cdda86/9ea706c3/3565f13. Registration unchanged since 123d8cd.

### C2 calibration (lowest axis) — verified

- Before: `controls/K2DoNothing.txt` (rev 123d8cd) — observed `CHECK D1..D8 FAIL`, `D9 PASS`,
  `verdict=TARGET_MISSED`, exit 1. Matches report (1/9).
- After: `evidence/c2-after-77cdda86.txt` (rev 77cdda869ec…) — observed `CHECK D1..D9 PASS`,
  `verdict=TARGET_MET`, exit 0. Matches report (9/9).
- Spot reads: D1 — SKILL.md rows 633–635 now carry `mado-r27-control-receipts` /
  `mado-r27-counter-selftest` / `mado-r27-population-suite` as LANDED (no `pending`). D8 — rows
  630–635 region carries the corrected citation block. Honest framing confirmed in SCORECARD
  (row ~1813): D9 retained (not an r28 gain), lesson-citation rubric 26/35 = 7.4286 explicitly
  NOT re-scored by this claim.
- Grade: **improved** (re-measured over committed evidence: receipts read + conditions spot-read;
  the lane-owned counter itself not executed, per §Gate standard closure consequence).

### C1 operability (sourced S183) — improved on committed evidence; frozen composite predicate MISSED

- Before: `evidence/c1-before.txt` (rev 123d8cd) — observed all six legs FAIL
  (`h1-rotation FAIL … h_killed=15/18`, `boolword-v5 FAIL normal=missing mutant=missing`,
  h2/refpub/q36/q37 FAIL). Matches report.
- After: `evidence/c1-after-77cdda86.txt` (rev 77cdda869…) — observed verbatim:
  `h2-rotate PASS seal-at-rev=True rc=0 TARGET_MET`; `refpub-kills PASS h_killed=12/12 h_valid=12
  h_min_per_subject=4`; `q36-witness PASS rc=0 names=True`; `q37-open-ended PASS r26sha=803e0096c994`;
  `h1-rotation FAIL rc=2 no-tally`; `boolword-v5 FAIL normal=missing mutant=missing`;
  `PRED-C1-r28 verdict=TARGET_MISSED`, exit 1. Matches report exactly.
- Independent re-derivations:
  - Seals: `sha256sum -c` inside `c2/heldout2/` and `c1/refpub/` — all 12 files OK.
  - refpub shape: 3 subjects × 4 mutants (`ref-{c1v2,c2,chk}.json`, each a 4-row list) + 3 benign
    files × 2 rows = 12 mutants, 6 benign rows. Matches "12 mutants, 4 per public subject".
  - Frozen r26 artifact: `sha256sum .ufo/waves/round-26/quality/check-population.py` →
    `803e0096c994…d0f64` — matches the frozen pin (untouched).
  - q36 receipts: `quality/q36-successor-receipts.txt` names both survivors
    (`Q2-glob-case-sensitive`, `Q5-marker-case-insensitive`), `Q36WITNESS rows=4 failed=0`.
  - Guard-pin defect (M28-1): `count.py:100` pins count-v4.py at `3d7d301f…`; observed committed
    bytes `635ae788…` at 5198cc8 (freeze), 20022a65 (r27 tip), 77cdda86, and tip — the pin never
    matched, so the boolword leg was vacuously dead inside the composite from freeze. Report's
    claim verified.
  - h1-rotation after-state: committed w2 receipt `w2/reports/ReviewerSuiteMonotone.md` — new suite
    `h_killed=18/18 verdict=TARGET_MET`, green 17/17, w 15/15, exactly the three `held-c1v2`
    survivors flip SURVIVED→KILLED, monotone + behavioural. Matches report.
- Defect (routed): the standalone boolword-v5 green runs (`cases_pass=41/41 boolword_pass=2/2
  TARGET_MET`; mutant `0/2 TARGET_MISSED`) are quoted in the report and LOG but have **no committed
  receipt** — grep for `cases_pass=41` over `.ufo/waves/round-28/` finds only code/spec/registration.
  Inline committed quotes are evidence, but weaker than this lane's own receipt convention.
- Judgment: the frozen composite predicate (`exit 0 + TARGET_MET`) did not hold at the measured
  revision. Both causes are registration-declared or pre-existing (ephemeral-H1 boundary stated in
  the registration; guard pin dead at freeze), no leg rule changed after data, and the miss is
  published verbatim with L0 questions filed — but per the frozen predicate the claim missed:
  **the round is a rejected-honest-stop, not an admission.** The operability surface itself
  improved on committed evidence.

## Per-axis verdicts

- calibration — **improved** (C2: 1/9 → 9/9, verified; bounded honest framing).
- operability — **improved** (four legs pass on committed bytes; blind-spot suite kills 18/18 per
  committed w2 receipt; refpub 12/12; q36/q37 green; v5 standalone quoted green, receipt routed as
  a defect). No operability surface regressed; the composite AND-bit miss is recorded at round level.
- coverage / freshness / depth / adjacency — unchanged (diff 317ff19..3565f13 touches only
  records, refpub, receipts; no SKILL/PROVINCE/coverage-map changes; no cross-domain writes —
  fleet-root status shows only foreign lanes' files).

## Discernment spot-check (LEARNING.md — from outside)

| item | decision | re-opened source | agree/disagree | reason |
|---|---|---|---|---|
| S183 admit (round-28 Gate) | admit — title-only grounding | `curl -LH "Accept: application/vnd.citationstyles.csl+json" https://doi.org/10.1145/2635868.2635929` → title "Are mutants a valid substitute for real faults in software testing?", Just et al., FSE 2014, issued 2014-11-11 | **agree** | Title, venue, and date reproduce exactly; the 11-word gate quote is verbatim from the title; the lane explicitly attributes no result to the inaccessible text — honest tier-A-for-question scoping. |
| S062 reject (standing registry; round-28 Gate considered no reject) | reject — demonstrable version error | re-fetched `https://linuxjunkies.org/guides/configure-alacritty`: page states "Starting with 0.12, Alacritty switched to TOML"; `alacritty/alacritty` CHANGELOG v0.13.0 line 36 "Configuration file now uses TOML instead of YAML"; v0.12.0 changelog has no TOML entry | **agree** | The page's 0.12 boundary is false (true boundary 0.13); one false boundary disqualifies its other version claims, matching the row's reason and flip. |
| SOURCES.md S183 row | row claim | row at `corpus/SOURCES.md:195`, 11 columns, tier A scoped to the paper's question, status mined, used-by exists | **agree** | Row shape, tier scoping, and used-by path verify; census re-run exit 0 (183 rows; A=176 B=1 C=6; mined=164 queued=10 rejected=9 — all match the report). |

Observation (minor): round-28's Gate section records a single candidate (S183); no reject was
considered this round, so the ≥1-reject outside sample rides the standing registry (S062). If the
operator expects a per-round reject sample, the lane should record "none considered" explicitly.

## Trend verdicts

- expansion — **improved**: first public reference mutant set (12/12, sealed, committed), restored
  byte-identical oracle enabling the v5 measurement, capability row "rotating held-out mutation
  gate" entered in SCORECARD (row ~1840), sources 182 → 183 (+S183 mined).
- quality — **improved**: nine-defect record audit 9/9 PASS (verified), the three round-27 survivor
  classes close (committed monotone receipt 18/18), q37 reads open-ended targets with the frozen
  r26 artifact untouched (sha verified), no admitted entry left failing.
- discernment — **improved**: the lane mined its own vacuous-check and stale-premise defects
  (M28-1 guard pin; M28-2 ephemeral input) into grounded QUALITY criteria 38–40 (verified in
  corpus/QUALITY.md), published the composite TARGET_MISSED verbatim, kept C2's D9 framing honest,
  and this outside spot-check agrees with both sampled gate decisions.

## Routed defects and items for round 29

1. **C1 composite AND-bit (operator ruling requested via L0):** the frozen claim stands missed at
   77cdda86. r29 pre-data registration must fix the count-v4 guard pin to the committed bytes
   (`635ae788…`) and smoke-run the composite once at freeze, committing the full output (QUALITY 38).
2. **Ephemeral-input preservation (L0 open):** H1 was cleaned before closure; leg 1 verified only
   from the committed w2 receipt. r29 must either preserve registered ephemeral inputs through
   adjudication or adopt the named-committed-receipt basis (QUALITY 39).
3. **Standalone boolword-v5 receipts missing:** commit receipts for the standalone leg runs next
   round (41/41 green; mutant 0/2) — quoted-only evidence does not meet this lane's receipt
   convention.
4. **Residual §6.6 tenth record defect** (docstring-citation overclaim): real, unclaimed, carried
   by the lane to r29 intent (RevengerNineDefects.md) — keep it on the routed queue.
5. **Operator note (promotion-owned):** SHONEN boxes 1 and 3 (SKILL tables current through r28 —
   rows 633–635 verified; frozen registration + counters re-ran without oral context, receipts
   committed) look checkable to `[x]` by a non-author verifier; box 2's "no new live-desktop task"
   and box 4's outside-lane verifier independence remain open. Promotion is operator-owned; this is
   a note only.

Dispatch/complete digest (from `.ufo/watchdog.log`, mutable — copied per protocol):
2026-10-23T19:47:47 lane-dead-no-report mado round=28; retry (attempt=1: L1 dispatched under
executor leaf role) · 19:47:53 launch attempt=2 · 19:57:07 lane-dead (parent froze; L1 never ran) ·
19:57:27 launch attempt=3 · 20:17:39 lane-dead (second freeze) · 20:17:57 launch attempt=1 ·
20:33:23 lane-dead (parent SIGSEGV) · 20:33:34 launch attempt=2 · 2026-10-24T02:24:08 launch
attempt=1 · 03:01:57 complete mado round=28. Seven deaths, then a completing attempt that inherited
the 2026-10-23 committed work (tip 317ff19) and finished the round.

Closure verdict: **rejected-honest-stop** — C2 verifies (9/9); C1's frozen composite predicate
missed with both causes declared/evidenced and no leg rule changed after data; no axis harmed;
trends improved/improved/improved on verified evidence.
