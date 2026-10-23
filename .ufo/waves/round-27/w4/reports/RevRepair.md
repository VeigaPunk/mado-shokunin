# RevRepair — audit of the round-27 w4 C2 repair candidates (suite A)

Seat: RevRepair, 2026-10-23. Reviewer seat; the only lane file this seat wrote is this
report. Scope: the suite-A repair candidates delivered under
`/fast/scratch/hyaku/mado-r27/repair/` and each seat's own class mutants. The sealed directory
`/fast/scratch/hyaku/mado-r27/heldout/` was **never read** (role forbids); the only sealed-set
signals used are the three public survivor names in
`evidence/c2-after-48b9434a.txt` (`HeldC2-extra-disjunction`, `HeldC2-unstable-conjunction`,
`HeldC2-embed-boundary`) and that receipt's public fields. No tool was installed or updated
(the standard system toolchain sufficed: git, python3, bwrap already present — none was needed).

## Baseline state (verified, not assumed)

* Committed suite A at measurement-1 REV `48b9434a0b0619b3896c9d80e8288ec2226c9ed8`:
  sha256 `7fd94b0431849d1be7dc99e120c2f5bd0105c6a1d122e9cd1a3327d30ef3c587`; byte-identical at
  lane tip `86f7355` (no repair has landed in the lane).
* Measurement-1 receipt: `green=17/17 b_valid=9 w_killed=15/15 h_killed=12/18 h_need=14
  h_valid=18 invalid=0 verdict=TARGET_MISSED`. Six suite-A H rows survived: three on the
  C1-counter subject (`held-c1v2-node-subset`, `held-c1v2-missing-version-guard`,
  `held-c1v2-extra-output-segment`) and the three C2-counter survivors named above, which are
  this wave's repair target. Math for re-measurement: h_killed must reach `ceil(0.75*18)=14`;
  killing all three HeldC2 survivors yields 15/18 ≥ 14.
* Sandbox: `git clone` of the lane to `/fast/scratch/hyaku/mado-r27/repair/RevLane` (tip
  `86f7355`); every efficacy run below is the **frozen** counter
  `python3 -I .ufo/waves/round-27/c2/count-v2.py 48b9434a… --suite-a-file <candidate>
  [--heldout D --seal F]` executed from that clone — i.e. the exact mechanism the committed
  suite is measured by (`env -i PATH=/usr/bin`, `timeout 300`, 4 GB RLIMIT_AS, bwrap with
  `/home` and `/fast` hidden except the run dir, `--no-local` inner clones, shuffled runs).
  Candidate-bytes seals were computed by this seat (`run-c2.sh`); receipts `out-*.txt`.
* Harness replication check (committed bytes as suite A, no heldout): `green=8/8
  w_killed=15/15` — identical to the public part of measurement 1 (`out-baseline.txt` line:
  `PRED-C2-r27-v2 green=8/8 b_valid=0 w_killed=15/15 …`).

## Independent reference mutants (RevRepair's own; yardstick, not a candidate)

Built only from the public subject `.ufo/waves/round-26/c2/count.py` and the three survivor
names (`ref-mutants/*.json`); `V3.compare` keys entries on all 18 `FIELDS`, so one changed
field ⇒ (nm=1, ne=1), which is why these survive the committed suite:

| id | edit | class represented |
|---|---|---|
| `rev-extra-disjunction` | verdict `(nm == 0 and ne == 0)` → `… or nm + ne <= 1` | added tolerance disjunct, invisible to all sum-2 probes |
| `rev-unstable-conjunction` | `if n1 or n2:` → `if n1 and n2:` | two-BASE-run stability guard weakened to a conjunction; committed `c2-drift` diverges both ways (1,1) so still fires |
| `rev-embed-boundary` | `EMBED_MIN = 12` → `13` | threshold shift; the committed 40-char `EMBED_ARG` fixture still caught |

Fidelity (committed suite vs these rows): all valid, all `rc=0 SURVIVED`
(`out-ref-vs-committed.txt`, `h_killed=0/3`, `invalid=0`) — genuine survivor-class
representatives. Sharper reference sets: `ref2-mutants` (`or nm + ne <= 2`, `if n1:`,
`if n2:`) and `ref3-mutants` (`or nm == 3`, `or ne == 3`).

## Audit axes

### (1) SEALED-DIR INTEGRITY — PASS for both candidates

Proof by construction (absolute non-contamination is unverifiable without reading the
sealed set; the admissible evidence is positive):

* Integrity greps over both candidate files: **0 hits** for `heldout`, `HeldC2`, `HeldC1v2`,
  `HeldChk`, `held-c1`, `/fast/scratch`, and all six public sealed-file hashes
  (`9bde3d5c…`, `ccb9af21…`, `422f1da7…`, `63cd2b75…`, `e1b55f97…`, `a83f1455…`)
  (`a1e.audit.txt`, `a2b.audit.txt`).
* Every new check is a synthetic `run_case`/`FakeOracle` probe parameterised by constants
  of the **public** subject (`EMBED_MIN = 12`, `nm/ne` semantics, `if n1 or n2:`) — the same
  derivation this seat performed with zero sealed knowledge, landing on identical regions to
  A1's mutants and inside A2's 12-mutant set.
* Neither suite pins subject bytes/hash/AST, reads new files, inspects env/process/timing
  (`open()`/`os.environ`/`subprocess` counts identical to committed: 7/1/1; no socket/urllib).
* Class mutants are derivable: A1's are single-defect copies of the pristine public subject
  (diffs: one token/one clause each); A2's `mutants.json` rows are `old→new` pairs whose
  `old` occurs exactly once in the public subject.

### (2) NO WEAKENING — PASS for both candidates

* Diff vs committed `7fd94b04…` is **purely additive** in both: no check deleted, no
  predicate relaxed, no `old`-text changed. `REQUIRED` 47→55 both, `TOTAL = len(REQUIRED)+1`
  preserved, the inventory gate unchanged, executed checks 48→56 both.
* CLI contract identical: `--c1/--c2/--rev` required, `--scratch/--keep` optional, exit
  0/1 semantics, `SELFTEST pass=N total=M` output — both diffs touch no argparse/main wiring.
* A1's new predicates are *stricter* than committed style (e.g. `got == 0`, `total == 51`,
  `eh >= 1` pinned). A2's match committed style. Neither removes/weakens an existing check.

### (3) EFFICACY — PASS for both candidates (A1 stronger)

Frozen-counter runs at REV `48b9434a` (receipts in `/fast/scratch/hyaku/mado-r27/repair/RevRepair/`):

| run | suite-A file | heldout rows | result |
|---|---|---|---|
| T1 | A1 `e36f12f2…` | — (public set) | `green=8/8 w_killed=15/15` (`out-a1-final.txt`) |
| T2 | A1 `e36f12f2…` | A1's own 3 | `h_killed=3/3`, all rows VALID (`out-a1-final.txt`) |
| T3 | committed `7fd94b04…` | A1's own 3 | `h_killed=0/3` — A1 mutants faithfully SURVIVE committed (`out-a1-T3.txt`) |
| T4 | A1 `7e30ca84…` | my `rev-*` 3 | `h_killed=3/3` (`out-a1-T4.txt`) |
| ref2 | A1 `7e30ca84…` | `tol-2`, `n1-only`, `n2-only` | `h_killed=3/3` (`out-a1-cand-ref2.txt`) |
| ref4 | A1 `e36f12f2…` | `or nm == 2`, `or ne == 2` | `h_killed=2/2` (`out-a1-final-ref4.txt`) |
| T1 | A2 `aa0e14d1…` | own 12 mutants + 6 benign | `green=13/13 b_valid=5 w_killed=15/15 h_killed=12/12` (`out-a2-final.txt`) |
| T3 | committed `7fd94b04…` | A2's own 12 | `h_killed=1/12` — 11/12 faithfully SURVIVE committed (`out-a2-T3f.txt`; matches their report's claim; `a2-unstable-conjunction-eq` is a degenerate `n1==n2` guard the committed suite already kills) |
| T4 | A2 `aa0e14d1…` | my `rev-*` 3 | `h_killed=3/3` (`out-a2-T4.txt`) |
| ref2 | A2 `aa0e14d1…` | `tol-2`, `n1-only`, `n2-only` | `h_killed=2/3` — **`rev2-guard-n1-only` (`if n1:`) SURVIVES** (`out-a2-final-ref2.txt`) |
| ref3 | both candidates | `or nm == 3`, `or ne == 3` | **0/2 for both** — shared residual (`out-a*-ref3.txt`) |

Label footnote: A1 rows marked `7e30ca84…` ran A1's parent revision (snapshot `a1-cand.py`);
the delivered final `e36f12f2…` differs from it by an unused `fail_nth` plumb-through only
(verified by diff — constructor default `None`, same records, same REQUIRED, same runtime
behaviour), and every decisive axis (greens+W, own mutants, ref4) was re-run on `e36f12f2…`
itself. A2's T4/ref2 rows ran snapshot `499c11e6…` (`a2-v3.py`), which differs from its final
`aa0e14d1…` by a docstring probe-count correction (`53→55`) only; the full own-mutants +
greens + W matrix was re-run on `aa0e14d1…` (`out-a2-final.txt`).

Representative receipt line (A1): `PRED-C2-r27-v2 green=8/8 b_valid=0 w_killed=15/15
h_killed=3/3 … verdict=TARGET_MISSED` (verdict is MISSED only because no sealed benign set is
present; MIN_B fails by construction — all my efficacy fields are what the seat controls).

### (4) Which candidate is superior — ExecRepairA1

Both pass every required gate; the discrimination is coverage breadth and delivery shape:

* **A1 kills strictly more stability-guard mutants.** A1 probes both one-directional drift
  shapes (`c2-drift-extra` = r2 has one *extra* entry, `c2-drift-missing` = r2 has one
  *missing* entry). A2 probes only the superset direction (`c2-drift-superset`). Empirically
  `if n1:` survives A2, is killed by A1; `if n2:` is killed by both. A single-direction
  conjunction guard `if n1:` is a plausible concrete shape of `unstable-conjunction`.
* **A1 covers exact-two tolerances.** A1 probes `±2` defects in both directions
  (`c2-two-missing`/`c2-two-extra`); A2's only `nm>0` probe is `missing-one` (`nm=1`).
  Empirically `or nm == 2` SURVIVES A2 (`out-a2-final-ref4.txt`) and is killed by A1
  (`out-a1-final-ref4.txt`); `or ne == 2` is killed by both.
* **A2 probes the embed boundary in the description field too** (`c2-embed-desc-at/below-threshold`)
  — a width A1 lacks; but the shape the class name denotes (threshold moved) is killed by A1's
  arg-side probes already, so this is redundancy, not a gap in A1.
* A1's new predicates are the stricter ones (`got == 0`, `got == total and total == 51` on
  embed-below). A2's are `got < total` (committed style) — weaker on exactly how far the
  counter may drift before the check fires.
* Delivery shape: A1 delivers at `repair/ExecRepairA1/counter-selftest.py` (the ticket's
  expected path); A2 delivers `candidate-counter-selftest.py` — a naming deviation that must
  be corrected at landing or the first-returned lookup misses it.
* Blemishes logged, none blocking: A1 carries dead scaffolding (`fail_nth` plumb-through,
  never used by any check — a leftover that should be cleaned if the seat revises); A2's
  own `benign.json` contains one row the frozen loader rejects
  (`a2-benign-comment INVALID AST equals pristine`, `out-a2-final.txt` line 9 — their
  report's "6 benign edits green" overcounts by one; the comment-only edit cannot differ in
  AST, it is their fixture's defect, not the suite's).

### Residual risk (shared by both candidates, stated honestly)

* Tolerance disjuncts of size ≥ 3 survive both repaired suites: `or nm == 3` and
  `or ne == 3` class mutants are valid, survive committed, and survive **both** candidates
  (`ref3` runs). Re-measurement stays TARGET_MET iff at least two of the three HeldC2
  survivors die (h_killed ≥ 14); an extra-disjunction in ≥3-tolerance shape would leave the
  kill margin at exactly one class of slack on the remaining two.
* Neither candidate addresses the three HeldC1v2 survivors (`node-subset`,
  `missing-version-guard`, `extra-output-segment`) — correctly out of this wave's stated
  scope (the ticket's target is the three HeldC2 classes), but recorded here so the
  re-measurement expectation is calibrated: best achievable h_killed from suite A repair
  alone is 15/18 ≥ 14 ✓ only if all three HeldC2 classes die.
* A1's finality is by evidence (file stable ~150 s over 10 polls, its own receipts show
  56/56 green + 3/3 kills at `repaired-*.out`, class mutants in `laneclone/…/c2/mut-*.py`);
  its w4 report was not yet in the lane at audit time. A2 declared final with its report.
  If the landing rule reads "first-returned" strictly as first-reported, A2's declaration
  order would take precedence — flagged so the L1 decides per the frozen flow.

## RECOMMENDATION

**Land ExecRepairA1's `counter-selftest.py`, sha256
`e36f12f2285bab956235b046f34b03a6da36f016af7a9dcc11d881115be38703`.**

Rationale: identical efficacy on every required axis (green 8/8, W 15/15, own classes 3/3,
behavioural-only mechanism, additive-only diff), and measurably broader coverage than
ExecRepairA2's candidate on the `unstable-conjunction` class (both drift directions probed —
its `c2-drift-extra`/`c2-drift-missing` kill `if n1:`/`if n2:` single-direction guards, one of
which survives A2) and on the `extra-disjunction` class (±2 tolerance probes), plus stricter
new predicates and the correct delivery path. Verified on the delivered bytes themselves via
the frozen counter.

Fallback: ExecRepairA2 `candidate-counter-selftest.py` sha256
`aa0e14d160b8429b945f12329e5673a1d484986d1b617a05920a92e77a1d4898` is acceptably repaired
(passes all required gates, is already declared final with its report) — but lands one fewer
stability direction, and must be renamed to `counter-selftest.py` at landing.

If neither may land per the frozen "first-returned" rule (i.e., if A1 is judged unreturned),
then A2 as delivered is the answer, with the `if n1:`-direction gap documented above as the
accepted residual.

Verification gaps: the sealed H set was not and cannot be exercised by this seat; the ≥3
tolerance residual is a verified limitation of both candidates' coverage, not speculation.

Report: .ufo/waves/round-27/w4/reports/RevRepair.md
