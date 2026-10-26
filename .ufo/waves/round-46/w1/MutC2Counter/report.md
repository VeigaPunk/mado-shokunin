# MutC2Counter — round 46 w1 — mutation probe of PRED-C2-r46 (summary)

10 mutants of `quality/counters/c2-r46-input-device-entry.py` (one clause weakened each), each scored by the
15 registered C2 controls via a scratch copy of `.ufo/waves/round-46/ctl/run-c2-controls.py` pointed at a
mutant repo. Baseline (pristine counter): CTL_C2 VERDICT PASS, 15/15 correct, P admitted a–j all 1.

Verdicts: 7 killed, 3 survived.

| mutant | weakened clause | verdict | killed by |
|---|---|---|---|
| M1-census-regex-uniq | h census-pattern uniqueness (counter.py:347) | **SURVIVED** | none of the 15 |
| M1b-census-devicekeys | h device_keys scope (counter.py:342) | killed | P (positive itself rejected, h:0) |
| M2-surface-width | j JWIDTH 30→1000000 (counter.py:100) | **SURVIVED** | none of the 15 |
| M3-quote-uniq | d quote uniqueness (counter.py:541,555-561) | **SURVIVED** | none of the 15 |
| M4-T1-census-prose | T1 prose census (counter.py:626) | killed | PROSE-CENSUS + PROSE-CENSUS-SPACED |
| M5-T2-supersede | T2 supersede words (counter.py:504) | killed | ROW-SUPERSEDES |
| M6-T3-fences | T3 fences (counter.py:685) | killed | FENCE-TABLE |
| M7-T4-verdict-tokens | T4 verdict tokens (counter.py:681) | killed | RECEIPT-CONTRADICT |
| M8-T4-anchor-range | T4 anchor range (counter.py:610) | killed | ANCHOR-PAST-EOF |
| M9-T5-readme-ids | T5 README ids (counter.py:660) | killed | README-IDS |

Survivor analysis (full detail in .ufo/waves/round-46/w1/MutC2Counter.md):
- M2 is the actionable gap: the locator span bound (b-a<=30) is pinned only by clause j; registered WIDE-RANGE is
  also killed by clause g (exact quote-line locator), so the suite passes with JWIDTH unbounded. Demonstrated kill:
  a WIDE-TAIL control (preserve each range start, widen span to :N-2315) is rejected by the pristine counter
  (j:0) and ADMITTED by the M2 mutant (j:1) — evidence/probe-widetail.txt.
- M1 is structurally unprobed at this freeze: the six census receipts are hash-pinned (PINS) and a non-PINS
  receipt cannot feed host_census's `need` set, so no constructible control isolates the census-pattern
  uniqueness sub-check; it is defense-in-depth behind the pin-hash root. M1b shows a census mutant that changes
  the computed value IS caught (by P).
- M3 correction (post-delivery, 2026-10-26): initially reported "structurally unprobed" — WRONG. ConnCrossClaim
  verified the pin_ok None-membership hole (counter.py:532-534: a non-PINS receipt name passes), and this seat
  then DEMONSTRATED a killing control: a new id S326 gated on a self-authored non-PINS receipt
  (fetch/r46-shared-quote.txt) sharing S319's quote — pristine counter rejects it solely via the uniqueness
  sub-check (clause=d id=S326 bound=0, the only unbound gate; d:0), the M3 mutant ADMITS it (all clauses 1).
  M3 still survives the registered 15-control suite, but a killing control IS constructible. See the Correction
  section in MutC2Counter.md; evidence/probe-sharedquote-{pristine,m3}.txt.

Integrity: lane counter and runner sha256-identical before/mid/after (evidence/lane-hashes.txt); all work in
/fast/scratch/hyaku/mado-r46/MutC2Counter (deleted afterwards); no installs (python3 stdlib + git only).
Evidence: .ufo/waves/round-46/w1/MutC2Counter/evidence/ (BASELINE.txt, 10 suite outputs, 2 probes, 10 diffs,
runner-copy.py, driver.sh).
