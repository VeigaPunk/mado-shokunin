# mado round 76 — lesson (SKELETON)

status: DRAFT skeleton by seat R76ScribeLesson (w1 scribe). `[brackets]` are placeholders the
closure fills; nothing here has been written into `corpus/`. Shape follows
`corpus/lessons/round-75.md` (Outcome and boundaries / Mistakes table / Gate / Assimilation).

author: [mado L1 — the scored instruments are the L1's own; the one w1 wave's seats attack them]
date: 2026-11-04 (America/Sao_Paulo)
base: `c3e0bc5f10b72964d54d18dc9b0706dc308dd1bf`
frozen declaration: `.ufo/waves/round-76/claims-declaration-r76.md`, freeze v2
`cb713254ee9926e036e594312fdc61b57825526b`; label set v3 sha256
`320f7e6b54e71776f2d5b179b9a8b09ee9185886e2aeb045af0ecc9171cc77ea` (16 real `bash` fixture
modes, one per mode, each labelled `expect_mz` + `expect_verdict`)
control sets: `.ufo/waves/round-76/controls/c1-outcome-cases-r76.json` sha256 `320f7e6b…` (16
cases) and `.ufo/waves/round-76/controls/c2-cases-r76.json` sha256
`df9e89841ed560613d7a05ad50f345b2d6bbf0d8e40a98f51e8b8134492b3948` (59 cases; the 47 round-75
cases carried byte-identically, hash-checked against `c2-cases-r75.json` sha256 `d99502ba…`)
pre-freeze baseline: `.ufo/waves/round-76/control-baseline-r76.txt` (held mz-only rule kills
0/4, `outcome_field_scored=no`; held round-75 classifier 55/59, missing exactly
`callee-del-literal,callee-del-store,dynamic-key-del,dynamic-key-module-const`)
measured content: C1 receipt `.ufo/waves/round-76/measurement-c1-r76.txt` at rev
`cb713254…` (harness `quality/counters/c1-r76-landing-controls.py` sha256 `b6003941…`);
C2 receipt `.ufo/waves/round-76/measurement-c2-r76.txt` at rev
`755b339f1f6ec18f45b494d40515aecdbe9ceb73`. The two claims measured at different revisions;
the report states the measurement revision and each instrument's last-change commit separately
(R5). [closure: the round's single measured-content rev, if one is named]

## Outcome and boundaries

[Two bounded claims, both frozen before any candidate data; both `TARGET_MET` at their measured
revisions with the do-nothing controls at their declared miss scores.]

- **C1 calibration — the successor counter certifies the contract outcome field, not only the
  `mz=` decision.** `quality/counters/c1-r76-outcome-field.py` scores both the `mz=` field and
  the `verdict=` field of `quality/counters/c1-r76-landing-controls.py` over the frozen
  sixteen-case label set v3. Receipt: `MADO_R76_OUTCOME_FIELD: cases=16 correct=16 mutants=4
  killed=4 base_killed=0 verdict=TARGET_MET rev=cb713254…`, rc 0. The four outcome-rule mutants
  are anchored at the single return line of the harness's named `outcome_green(...)`:
  `outcome-summary-only` 15/16 (separator `green-absent`), `outcome-killed-only` 15/16
  (`always-red`), `outcome-killed-any` 15/16 (`green-mutant`), `outcome-killed-or` 14/16
  (`always-red`); every one reads `base_score=16/16 base_killed=no` under the held mz-only
  rule, which therefore kills 0/4 (`control-baseline-r76.txt`:
  `HELD_R76_C1_MUTANT … killed_by_held_rule=no` for all four). Negative result carried into
  the claim: an echo-dropping outcome mutation is unobservable through `verdict=` (green
  requires `killed == 2`, and the M-Z kill already requires the echo), so the certificate
  covers the published field's `killed` and green conjuncts, not the echo term. Grammar/challenge
  guards carried from the design: G1 reads sixteen **or more** hex characters (over-long echo
  is a parsed mismatch); G2 draws the challenge by rejection sampling until it contains an
  `a-f` letter (deterministic uppercase oracle; closes M75-4).

- **C2 operability — the census counts an interprocedural cancellation and a dynamic key.**
  `quality/counters/c2-r76-shapes.py` adds D3 (a live `del m[KEY]` inside a local function
  `f(m)` cancels a guard on the mapping the caller hands to `f(env)`, under the dominance test:
  call line strictly between guard line and first launch use) and D4 (`del env[k]` where `k` is
  bound exactly once in the same scope, before the delete, to the guard key — literal or module
  constant). Receipt: `MADO_R76_GUARD_SHAPES: population=20 readers=13 guarded=13 unguarded=0
  controls=59/59 base_controls=55/59 verdict=TARGET_MET rev=755b339f…`, rc 0. The base
  (round-75) leg misses exactly `callee-del-literal`, `callee-del-store`, `dynamic-key-del`,
  `dynamic-key-module-const` (`leg=base … correct=no`), matching the pre-freeze baseline's
  `missed=` list.

**Not claimed.** [Per the declaration's § Declared limits, verbatim intent: the mutants patch
the outcome helper only, so the kill path stays correct by construction — that is why the held
rule cannot see them; the sixteen cases are rule separators, not fault coverage; the challenge
authenticates the echo, not the truth of the assertions. C2: line order is not execution order;
simple call shape, no aliases or call chains; callee delete keys are literals or module
constants; D3 is modelled in the env-named/subscript carriers, not the attribute flow; the
census is a syntactic approximation that does not interpret values. No live desktop, compositor,
service or session probe; no `[x]`, promotion or axis retirement.]

**Verbatim conflicts carried for the closure (recorded, not resolved, by this seat).**
- `control-baseline-r76.txt` prints `HELD_R76_C1 held_mz_correct=15/15` — a 15-case denominator
  against the frozen 16-case v3 set. The landed criteria's able-to-fail records carry the same
  15-denominator pre-v3 numbers (`correct=12/15` at `corpus/QUALITY.md:908-910`;
  four mutants `0/15` at `corpus/QUALITY.md:927-929`). Which mode joined the set at v3 is not
  re-derived by this seat. [closure: state the v1/v2→v3 population delta explicitly]
- C1 measured at `cb713254…`, C2 at `755b339f…` — see the measured-content note above.

## Mistakes

| mistake | class | evidence | captured-by | fix and the failure it can now show |
|---|---|---|---|---|
| M76-1: label set v1 (sha `ff97505f…`) modelled the harness's `verdict=` as summary-green only, so its labels encoded one field where the counter scores two; the first outcome-field measurement scored `correct=12/15` with `right`, `liar-success` and `green-mutant` disagreeing with their labels. | survivor — a label artifact the held denominator cannot see: the held rule scores `mz=` only and read v1 as consistent (`HELD_R76_C1 held_mz_correct=15/15`). | `claims-declaration-r76.md:42-47` (v1 disclosure); `corpus/QUALITY.md:906-913` (criterion 128's able-to-fail record, the 12/15 disagreement). Green: `receipts/label-derivation-r76.txt` — all 16 rows `expect==derived` on both fields from `MADO_R76_SELFTEST … green=` and `MADO_R76_MUTANT M-Z/M-R … killed=` lines, `DERIVATION: all labels re-derived`. | none at freeze time — criterion 121 scored labels against the held rule, which cannot read `verdict=`; the disagreement surfaced only through the first outcome-field measurement. Now captured by **QUALITY 128** (derivation source = the instrument's own evidence lines, never the contract row). | v3 labels re-derived per case from the harness's own evidence lines before the freeze. Failure it can now show: a label justified by the contract row's summary semantics while the instrument's own per-case lines disagree. |
| M76-2: label set v2 (sha `5a91d69e…`) corrected the field semantics but kept an echo-dropping outcome mutation the harness makes unobservable — `verdict=` is green only when `killed == 2`, and the M-Z kill already requires the echo, so the mutant produced the same field on every reachable case. | survivor — an oracle whose expected value is unreachable through the scored field (M75-4's cousin one level up: not the challenge's reachability, the field's). | `claims-declaration-r76.md:43-56` (disclosure + negative-result paragraph); `corpus/QUALITY.md:916-924` (criterion 129: the mutant scored 16/16 on every reachable case). Green: the frozen four-mutant table, each with a separator case whose scored field changes — `outcome-summary-only`→`green-absent` 15/16, `outcome-killed-only`→`always-red` 15/16, `outcome-killed-any`→`green-mutant` 15/16, `outcome-killed-or`→`always-red` 14/16 (`measurement-c1-r76.txt`). | none — criterion 127 covers a separator's determinism at the challenge, not observability through the scored field. Now captured by **QUALITY 129** (a mutation producing an identical field on every reachable case is a negative result, not a control). | The round scores the observable outcome-rule class (`killed` conjunct + green conjunct) and records the impossibility as a declared limit. Failure it can now show: a frozen mutant whose two-field score equals the correct implementation on every reachable case. |
| M76-3: the pre-freeze control's row regex required a trailing-field match (anchored to end-of-line while the rows carry a trailing `sha256=`), so it silently returned no lines and four mutants were reported `0/15` — killed by a rule that had observed nothing. | landing — a receipt-pipeline defect that still reported a green-looking score (M75-2's shape one layer out: the scored instrument passed; the evidence pipeline around it did not). | `corpus/QUALITY.md:926-931` (criterion 130's able-to-fail record). Green: `control-baseline-r76.txt` prints per-mutant scores over parsed rows (`mz_score=15/15 … killed_by_held_rule=no` for all four) — the observed-nothing direction now reported as not-killed, not as a kill. | none — no criterion required a zero-row parse to fail loudly or a per-leg score to print. Now captured by **QUALITY 130** (a control leg that parses no row fails loudly; the per-mutant score is printed). | Both regexes search the parsed line instead of anchoring it; per-mutant scores printed. Failure it can now show: a control leg reporting any score over zero parsed rows. |

A fix counts only on its named red/green evidence: M76-1's red is v1's `correct=12/15`
disagreement (`right`, `liar-success`, `green-mutant`) and its green the v3 per-case derivation
receipt with 16/16 agreement; M76-2's red is the echo-dropping mutant scoring 16/16 on every
reachable case and its green the four observable outcome-rule mutants (15/16, 15/16, 15/16,
14/16) with the impossibility recorded as a declared limit; M76-3's red is the silent `0/15`
killed-by-nothing report and its green the per-mutant baseline scores computed over parsed rows.

## Gate (placeholder)

Per `LEARNING.md:40-48`, discernment is checked from outside: a non-author — a fresh reviewer or
the operator (a lane-dispatched subagent is still the lane) — spot-checks a sample of this
round's gate decisions, **at least one admit and one reject**, and records `agree`/`disagree`
with a reason in this lesson.

- **Admit (≥1):** [candidate `S###`: document, URL, access date, three byte-identical fetches
  with sha256 + byte size and receipt paths under `.ufo/waves/round-76/fetch/`, located quote
  ≤25 words with `file:line`, and *why it grounds* the round's rules — D3 (a live `del m[KEY]`
  in a local callee cancels the guard on the mapping the caller hands over) and/or D4 (a
  same-scope name bound exactly once before the delete to the guard key). State whether the row
  repeats a held document at a new scope (documented non-failing W04 warning, no `supersedes`)
  or is new ground.]
- **Reject (≥1):** [candidate rejected with reason; if a prior registry row's count or scope is
  misstated, correct the record in place and log old → new (S446 precedent).]
- **Registry mechanics:** new rows enter `mined` with `used-by` naming their citing entries
  (R4); registry count old → new stated; census receipts (round start and round end) committed
  under `.ufo/waves/round-76/` with command, stdout and exit code (R2/R7); appended SOURCES rows
  pass the census at round end (exit 0).
- **Assimilation:** [`none` / what was adopted from the merge queue, with the connector's read
  recorded — round-75 wording kept.]

## Provenance note (per QUALITY 131)

Every number this skeleton quotes is **evidence-verified from committed bytes** read this round
(`control-baseline-r76.txt`, `receipts/label-derivation-r76.txt`, `measurement-c1-r76.txt`,
`measurement-c2-r76.txt`, `claims-declaration-r76.md`, `corpus/QUALITY.md:905-945`); none is
re-executed by this seat. [closure: label each quoted number `re-executed` or
`evidence-verified` in the final lesson and report]
