# R76Critic — falsification review of round-76 claim framing

Seat: R76Critic (critic, leaf). Scope: attack the *framing* of C1/C2, not the code only.
Read: `claims-declaration-r76.md`; SCORECARD `Planned (round 76; intent only)` (SCORECARD.md:4254);
`control-baseline-r76.txt`; `measurement-c1-r76.txt`; `measurement-c2-r76.txt`;
`receipts/label-derivation-r76.txt`; controls `c1-outcome-cases-r76.json` (v3) and
`c2-cases-r76.json`; instruments `c1-r76-outcome-field.py`, `c1-r76-landing-controls.py`,
`c2-r76-shapes.py`, held `c1-r75-harness-witness.py`; proto `held-r76.py`,
`label-derivation-r76.py`; `corpus/knowledge/outcome-field-r76.md`; QUALITY 36/121; git history
(c3e0bc5f → 755b339f freeze v1 → cb713254 freeze v2 = HEAD). No files outside my dir and the
Report path were written.

## A. The six questions

| # | question | verdict | evidence | what would change the verdict |
|---|---|---|---|---|
| a | Does `killed=4/4` actually discriminate, or would a trivially wrong counter also reach it? | **Yes it discriminates the field-blind and degenerate counters; no it does not bound a mutation-oracle cheat; margins are minimal; and the threshold that produces 4/4 is not the frozen text's threshold (finding F1).** | Kill is implemented as `score < len(cases)` = any-miss out of 16 (c1-r76-outcome-field.py:393). Always-pass scores correct=0; always-fail scores 13/16; a label-echo counter gives mutants 16/16 → killed=0: all three fail the target arithmetic. A rev-diff counter (`if source != frozen: score-1`) passes — no cheat-shape control receipt exists for C1 (QUALITY 36 names the classes; only the do-nothing class has one). Internal evidence of genuine scoring: the four mutants score 15/16, 15/16, 15/16, 14/16 (three distinct values), not a uniform flag. | A committed control receipt showing the counter *misses* a cheat (e.g., an all-green counter scores <16 correct) would close the cheat half; per-mutant per-case rows would close the crash-vs-miss ambiguity; a kill rule requiring ≥15 parseable rows + ≥1 semantic miss would make kills crash-proof. |
| b | Is `base_killed=0` structural boilerplate rather than a control? | **Structural by construction; empirically it is an anchor check, not an independent control.** | All four mutants patch only `outcome_green`'s single return (MUTANTS c1-r76-outcome-field.py:79-92; `apply_mutants` asserts a unique anchor, :293-307); the harness's `mz=` field does not consume `outcome_green` (its only consumer is `verdict=` at c1-r76-landing-controls.py:230). Any mz-only scorer therefore necessarily returns 16/16 for every mutant → `base_killed=0` is predetermined; the measured base leg (measurement-c1:19-22, base_score=16/16 ×4) verifies the anchoring held, nothing more. The declaration admits this ("that is exactly why the held rule cannot see them"). The *held round-75 counter* never scored these four mutants at all — it parses only `MADO_R75_` rows (c1-r75-harness-witness.py:67-68) and its own 11-case contract (:30), so it cannot score the r76 harness; the pre-freeze receipt was produced by the port `proto/held-r76.py` (F2). | A mutant class that also moves the `mz=` field (making the base leg informative), or a committed receipt of the genuine held binary running the v3 set (it would score correct=absent — also "cannot reach", but then say so). |
| c | Does the label derivation depend on the candidate's contract row anywhere? | **No — verified. But that is exactly why `correct=16` has zero external content.** | `proto/label-derivation-r76.py` reads only `MADO_R76_SELFTEST … green=` and `MADO_R76_MUTANT (M-Z\|M-R) … killed=` lines from harness stdout; `expect_verdict := green ∧ M-Z ∧ M-R`, `expect_mz := M-Z`. The contract row (`verdict=TARGET_MET…`) is never parsed. Consequence: labels ≡ harness self-report; the derivation imports the *successor counter's own* `make_fixture`/`harness_run`, so counter, derivation and harness share fixture machinery. `correct=16` certifies parser self-agreement, not correctness (QUALITY 121's own limits line: "agreement is a lower bound on the label"). The knowledge entry's phrase "evidence-verified labels" overstates this. | Any label checked against an oracle that is neither the harness nor the contract row (e.g., a hand-computed outcome for one mode from the r72 generation spec) would give the leg external content. |
| d | Is "echo-dropping mutation unobservable" true for every reachable fixture, or is there a counterexample shape? | **True for every fixture reachable from this harness; the only counterexample shapes require a different harness or a closed hole.** | verdict green requires `killed == 2`; `killed==2` includes M-Z killed=yes; the M-Z kill requires the run's challenge echo to match; `green_with_witness` consumes the *same* `selftest_out` the kill term consumed (harness:137-146, 230). So `killed==2 ⟹ echo matched`, making an echo-only conjunct in the outcome redundant on every case, and when `killed<2` both rules emit fail. Counterexample shapes: (i) kill term and outcome reading *decoupled* echo sources (publication vs decision) — a different harness, not a fixture; (ii) a letterless challenge (uppercase = identity) — closed by G2 rejection sampling + the 200-draw selftest (`MADO_R76_CHALLENGE … has_letter=yes`, knowledge §3); (iii) a mode with mz=pass but witness absent — contradicts M-Z semantics. Set-relative: covers the frozen 16 modes; any new mode/harness needs a fresh derivation (labels change only via a new round, knowledge §5). | A fixture whose harness emits `killed=2/2` with `witness=mismatch`, or a harness refactor that splits the echo publication from the kill decision — either would make the echo conjunct observable and flip this verdict. |
| e | Is C2's `base_controls=55/59` a real do-nothing control or a construction of the new cases? | **Real control; the informative content is the *precision* of the miss set.** | The base leg extracts and executes the actual held census (`c2-r76-shapes.py:56` BASE_COUNTER; receipt `MADO_R76_BASE_COUNTER … sha256=0544c0ef… present=yes`; per-case `leg=base` rows in measurement-c2). It misses exactly the four designed positives (callee-del-literal, callee-del-store, dynamic-key-del, dynamic-key-module-const) and nothing else — no collateral miss on the 47 carried (hash-checked vs the r75 set) or the 8 new negatives. The four misses were designed, but a wrong held census would have missed more/differently; pre-freeze baseline agrees (control-baseline: HELD_R76_C2 55/59, same four) before freeze v1. | Only a demonstrated case where the held census misses a *different* set than designed would downgrade this; none exists in the receipt. |
| f | Do both claims satisfy the claim-sizing rule's two conjuncts (§9: do-nothing cannot reach it; instrument cannot pass fail-open)? | **Conjunct 1: yes for both (C2 stronger than C1). Conjunct 2: mostly yes, with one softness.** | Conjunct 1 — C2: held binary, exact frozen 59-case set, 55/59 < 59, measured pre-freeze (control-baseline). C1: held mz-only rule kills 0/4 vs required 4/4 — structural (F1/F2) and measured via the base leg; provenance caveat F2 (port, not held binary; the held binary would score correct=absent, also unreachable). Conjunct 2 — C1 counter fails closed on: absent candidate (rc 1, :353-356), controls sha mismatch/count (SetupError rc 2), unparseable rows (case counted incorrect), letterless challenge (challenge_ok gate, :402). C2 fails closed on absent base classifier (base_controls=0) and ties the population verdict to the 59-case controls. Softness: the C1 kill rule counts a runtime-crashing mutant as killed; `apply_mutants` rules out syntax crashes (:305-307) and this run's scores (15/16×3, 14/16) evidence execution, but the target arithmetic alone cannot distinguish a discriminate-kill from a crash-kill. | A kill rule requiring ≥1 parseable wrong row per mutant; a committed cheat-control receipt; a held-binary C1 baseline receipt over the v3 set. |

## B. Additional findings (framing defects a closure should see)

- **F1 (high) — frozen kill rule contradicts the measured verdict.** Declaration:67/69 kill
  rule: "killed iff its two-field score is below fifteen" (also "fifteen-case expectation",
  :26). Implementation: `is_killed = score < len(cases)` with len=16 (c1-r76-outcome-field.py:393,
  FROZEN_CASES=16 at :68). Three of the four killed mutants sit at exactly 15/16 — under the
  frozen text (score < 15 ⟺ ≤14) they survive, killed=1/4, and the round's own target
  (`killed=4`) is **unreachable as written**. The counter's own docstring is still the v1/v2
  scale end-to-end: "Fifteen REAL bash fixture lanes" (:10), "below fifteen" (:31), "Exit 0 iff
  cases == 15, correct == 15" (:39) — and its "every mutant's mz score stays fifteen" (:31-32)
  contradicts the receipt's base_score=16/16. M55-2 class (frozen contract unsatisfiable as
  written / reference-drift). Smallest correction: freeze v3 of the declaration sentence +
  counter docstring ("below sixteen"; sixteen cases) *before seat scores are integrated*, or an
  explicit erratum receipt declaring the implemented any-miss rule governing.
- **F2 (medium) — the "held rule" behind the C1 control is a port, run by the same wave.** The
  held round-75 counter cannot parse the r76 harness (MADO_R75_ row regexes, 11-case contract:
  c1-r75-harness-witness.py:30,67-75). `control-baseline-r76.txt` was produced by
  `proto/held-r76.py` (C76_ROW regex for r76 rows), which the receipt does not name (no command
  line — F3). In-measurement `base_killed` is a *third* implementation (the successor's own
  mz-only leg, :383-396). Conclusion survives a fortiori, but "the held round-75 scoring rule"
  as an authority is duplicated three ways; the receipt should name the executor and the report
  should say the held binary's own behavior on r76 artifacts is parse-failure/absent.
- **F3 (medium) — both committed receipts lack command + rc, reccurring the routed defect R7.**
  `control-baseline-r76.txt` (5 lines) and `receipts/label-derivation-r76.txt` (18 lines, table
  only) carry neither the generating command nor an exit code, against the round's own R7
  disposition. The derivation receipt also does not state the harness sha it derived from;
  `proto/label-derivation-r76.py` defaults to 755b339f (freeze v1) while the frozen harness is
  cb713254 (v2 changed it, 14 lines) — provenance is unverifiable as committed. Correction:
  append command/rc/sha lines, or regenerate with explicit args and commit the stdout.
- **F4 (medium) — the round's knowledge entry cites evidence that is not committed and numbers
  that no committed line holds.** `corpus/knowledge/outcome-field-r76.md`:36 attributes
  "scores 16/16 on mz= and kills 0/4" to `control-baseline-r76.txt`, which says 15/15 and names
  the v1 mutant set (outcome-term-dropped, prefix-match, first-witness-wins, case-insensitive)
  — not the four v3 names; :54 cites "the v2 receipt kept beside the final one" showing
  `outcome-term-dropped score=16/16 killed=no` — no such file exists anywhere in round-76
  (grep: only control-baseline + w1 siblings). R2 class (declared receipt, no committed stdout).
  (Sibling R76ScribeEntries.md:56 independently flags the name-set mismatch; this adds the
  16/16-vs-15/15 and the missing v2 receipt.)
- **F5 (low) — label-set v3 was frozen without a pre-freeze held-rule scoring of the v3 labels
  (letter of QUALITY 121).** The pre-freeze held run scored the v1/v2 15-case set (15/15) with
  v1 mutant names; v3 (added always-red; flipped right/liar-success verdict labels fail→pass;
  renamed the mutant set) was frozen at v2 without one. Mitigation: the held rule reads mz
  only, and 15 of 16 mz labels were pre-scored; the successor's base leg does the v3 arithmetic
  post-freeze. Correction: re-run `proto/held-r76.py` against the v3 json + v3 mutants and
  commit the receipt before integration.
- **F6 (low) — C2 control-file note miscounts and muddles its own taxonomy.**
  `c2-cases-r76.json:3` says "thirteen appended: three interprocedural cancellations …, one
  dynamic-key delete …, and eight negatives" — 3+1+8 = 12, and the receipt shows 4 positives
  missed by the held census (2 callee + 2 dynamic-key: dynamic-key-module-const is a positive
  the note's "one dynamic-key delete" does not cover). 47 carried + 12 appended = 59 ✓; the
  note's arithmetic and shape count are wrong inside a frozen file. R8-class doc defect;
  correct in a successor note, never in place.
- **F7 (info) — revision split is real but benign; must be disclosed (R5).** C1 measured at
  cb713254 (freeze v2 = HEAD); C2 at 755b339f (freeze v1). Verified via `git diff --stat
  755b339f cb713254`: only C1 artifacts changed (declaration, c1 controls json, derivation
  proto+receipt, c1 harness, c1 counter); the c2 instrument and c2 controls are byte-identical
  across both revs. The report must state this split and the equivalence argument.

## C. What the round does NOT certify (closure terms)

1. The **echo term** of the outcome field — certified only through `mz=`; the round-75
   echo-dropper (`green := r72_green`) remains unobservable and is *not among the four final
   mutants* (declared negative result; its only committed empirical trace is F4's missing v2
   receipt).
2. **Semantic correctness of any label** — all 16 labels are implementation-self-derived (A-c);
   `correct=16` is self-consistency, not correctness.
3. **Mutation classes outside the four anchored at `outcome_green`'s return** — denominator
   mutations, killed-counter mutations, M-R term mutations, selftest-parsing mutations are
   unscored.
4. **Counter cheat-resistance** — no committed all-false/label-keyed/fixture-keyed control
   receipts for C1 (QUALITY 36's class list unexercised beyond do-nothing).
5. **Robustness margin** — kills at margin 1 case (×3) and 2 cases (×1); the certificate is an
   exact-set result, not a neighborhood.
6. **C2 generalization** — function aliases/call chains, non-constant dynamic keys,
   comprehension/class/lambda scopes, attribute-carrier D3, execution order (declared); no
   fault-injection into the 20 real population files.
7. **Two case authorities in C2** — the counter embeds a same-named case table in code
   (c2-r76-shapes.py:1563+) beside the frozen JSON; drift between them is not controlled by any
   cited check (the JSON sha gate covers the JSON only).
8. **Landing-time no-harm** — gate 460/460, index 93/93, ledger rows, SOURCES census at round
   end are post-wave obligations, not certified by this wave.

## D. Smallest safe corrections, in order

1. F1: re-cut declaration kill-rule sentence + counter docstring to the implemented rule
   ("below sixteen" / sixteen cases) as freeze v3, before seat scores are integrated — or file
   the erratum receipt that declares the implemented rule governing.
2. F3: append command + rc + harness-sha lines to both receipts (or regenerate with explicit
   args and commit stdout).
3. F4: fix the knowledge entry's two citations (15/15, v1 mutant names; drop or commit the v2
   receipt) before it gets an index row.
4. F5: commit the held-rule run over the v3 set (proto/held-r76.py, v3 json, v3 mutants).
5. F6/F7: successor-note the c2 json count; state the C1/C2 revision split with the equivalence
   argument in the round report.
