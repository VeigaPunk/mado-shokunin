# R67CriticClaims — frozen-claim falsification (C1 calibration, C2 operability)

Seat: R67CriticClaims (critic). Lane: `/home/vgpnk/Projects/shokunin/mado-shokunin`.
Reviewed: base `0b28ffb4baac9586566d246c3f0986b2bb650a33`, lane tip `ac376ef3`, freeze
`061dc329b598b2723a224b6c7b305b436946ec91`. Read-only; every write confined to
`/fast/scratch/hyaku/mado-r67/R67CriticClaims/` (removed before yield), this seat directory, and the `Report:` path named by the seat spec.

Bytes reviewed (sha256, at review time; C1 draft moved twice during the review, this is the
final `58d6c0ab…` 325-line version):

| file | sha256 |
|---|---|
| `w1/R67ExecRegister/draft/quality/counters/c1-r67-register.py` | `58d6c0aba4281ba0c75f653ea0c1fa4d8c90b6450d49b681bec34247eba1c9ec` |
| `w1/R67ExecLanding/draft/quality/landing-counters.sh` | `4378fd8c278126111ad6d970ac20215c170238ffe1a796c5c7d03c9e5b3b93a9` |
| `w1/R67ExecChildren/draft/quality/counters/c3-r56-used-by.py` | `f54423eb8ab24eeb5a8cd51f2d38408fe02054797ba841c3940cde28d3903b3f` |
| `w1/R67ExecChildren/draft/quality/check-tool-ledger.py` | `1c96c4cfd69ad97fbfc9174c9fe4d27b1d157df69cbcbc2451067f1374febdfb` |
| `w1/R67ExecChildren/draft/tools/mado-receipt-citecheck.py` | `3b61fa42b77e9c8065ab05668247c330b537910b06f7209caba7afbd0b102ad0` |
| `w1/R67ExecHarness/draft/quality/counters/c2-r67-landing-controls.py` | `a4376fa739405a213ccd59847620be02bec5fd2a70584aa59dfbc916022d9b58` |

Reproduction scripts kept at `w1/R67CriticClaims/evidence/` (`fx-zero.sh`, `fx-ledger.sh`,
`fx2.py`, `c1-regression.py`, `mr-inherit.py`, `fx-fix.py`, `fx-c2.sh`). All recreate their own
scratch root.

---

## 1. Do-nothing control — does the pre-r67 tip already meet either target?

**No for both; neither claim is void on this ground.**

C1 (committed scorer, re-run):
```
python3 -I .ufo/waves/round-67/controls/score-baseline-c1.py --repo . \
  --base 0b28ffb4baac9586566d246c3f0986b2bb650a33 \
  --controls .ufo/waves/round-67/controls/c1-controls.json --scratch-root <S>/c1
```
rc 0; `correct=4/6`; `unreferenced-live-object accepted=True expect=reject correct=no`;
`live-in-state-cell-only accepted=True expect=reject correct=no`. Matches the receipt.

C2 (committed scorer, re-run): rc 1; `selftest_rc=0`, `zero_citation_case=0`,
`replace_ref_case=0`, `usedby_guard=0 ledger_guard=0`,
`child_env_read=forged guarded_read=real`, `killed=0/2`.

The candidate C2 counter run **at the base rev** (not a publication claim, a direct run):
`mz=fail mr=fail killed=0/2 verdict=TARGET_MISSED` rc 1 — M-R is `recipe=none` because
`guard_count=0`. The candidate C1 counter at base prints
`register=accept controls=6/6 … verdict=TARGET_MET` rc 0. So the C1 score is reachable, the C2
score is not reachable without the new control harness.

**Coverage versus behaviour (frozen question 1, sharpened).** Neither C2 defect is a live
landing-path defect at base:
- Z: the zero-citation guard already exists at base, `quality/landing-counters.sh:73`
  (`[ "$citations" -gt 0 ] && …`, byte-identical in the draft at line 73), and it works. Full
  base instrument against a citecheck child emitting
  `MADO_CITECHECK: rev=… citations=0 resolved=0 missing=0 … verdict=TARGET_MET` at rc 0:
  `LANDING_CONTRACT citecheck ERROR (rc=0; …)`, `MADO_LANDING_COUNTERS: ERROR`, rc 2
  (`evidence/fx-zero.sh`, base and draft give the same rc 2).
- R: the citecheck child at base passes no `env=` and therefore inherits the instrument's
  `export GIT_NO_REPLACE_OBJECTS=1` (`quality/landing-counters.sh:6-8`); with that inherited key
  it reads the real tree (`rc=1 TARGET_MISSED missing=1`), and reads the forged tree only when
  `GIT_*` is scrubbed (`rc=0 TARGET_MET missing=0`) — `evidence/mr-inherit.py`.
Therefore C2 is a **test-coverage** claim for Z and a **standalone-child hardening** claim for
R, not a repair of two observably-broken landing behaviours. The declaration's wording
("leaves both untested") is accurate; "defect mutants" and the M-R baseline sentence are not
(see B1).

## 2. Predicate-literal binding

| frozen literal | observed bytes | verdict |
|---|---|---|
| C1 line `MADO_R67_REGISTER: register=… controls=<n>/6 headings=… rows=… groups=…/8 live-cited=… verdict=… rev=…` | draft 319-321 prints `register=accept controls=6/6 headings=1 rows=8 groups=8/8 live-cited=yes verdict=TARGET_MET rev=…` | match (label set and order) |
| C1 exit `0 iff register=accept AND controls=6/6; 1 otherwise; 2 setup` | draft 319-321 (`return 0 if verdict == "TARGET_MET" else 1` at 321); 2 on `SetupError`/`GitError` (324-325) | match |
| C1 six case names/expectations | controls JSON and draft `selftest()` table | match; selftest is a 15-case superset, scored denominator is `CONTROL_CASES = 6` (line 81) |
| C2 line `MADO_R67_LANDING_CONTROLS: selftest=… mz=… mr=… killed=…/2 baseline=0/2 verdict=… rev=…` | counter 311-315 | match |
| C2 exit `0 iff selftest=0 AND killed=2/2; 1 otherwise; 2 setup` | 303-304, `main` wraps `UsageError`/`SetupError` to 2 | match |
| M-Z clause `` `[ "$citations" -gt 0 ] && ` `` | base line 73 = draft line 73; `clause_count=1`, deletion exact (counter 212-220), `bash -n` gate (426-428) | match |
| M-R key `GIT_NO_REPLACE_OBJECTS` | present once in each of the three children; counter binds `R_PATH = CITECHECK` (57-60) | literal match, **operand drift** (B1) |
| Z control marker `` `citations=0 resolved=0 missing=0 verdict=TARGET_MET` `` | contract requires `rev=$REV` first (draft line 64) and `files=`/`skipped_large=`; implemented fixture emits the full 7-field line (124) | **mismatch** (B5) |
| baseline `killed=0/2` | `score-baseline-c2.py:91` `killed = 0`, printed at 96 | **not a measurement** (B6) |

## 3. Causal separability

Counter inputs are disjoint: C1 reads `PROVINCE.md` + `c1-controls.json`; C2 reads
`quality/landing-counters.sh` + the three children at `--rev`. Neither imports the other.
Independent landing is **not** harmless: both claims place a new `quality/counters/*.py` direct
child into the ledger population that the *other* claim's ledger leg reads (B2). `grep` map:
`landing-counters.sh:41-43` dispatches the three children; `quality/counters/c2-r65-landing-instrument.py`
and `c2-r66-landing-instrument.py` extract and run the instrument; `quality/counters/c1-r51-ledger.py:65`
uses `check-tool-ledger.py` as `DEFAULT_CHECKER`.

## 4. Axis attribution

- C1 → calibration (register structural discrimination): holds; the counter is a new finite
  denominator (6) and the registers measured are the lane's own PROVINCE block.
- C2 → operability: the *scored* denominator (`killed/2`) is mutation coverage and is new, so
  the score attribution is sound. Two attribution defects: (a) Z's guard is already present and
  effective at base and M-R's child is already protected in the landing path (section 1), so the
  0→10 is coverage/hardening, not repair; (b) the declaration's operability row cites
  `bash tools/mado-verify.sh --selftest` 460/460, while the lane's axis gate re-derives
  operability from `quality/check-index.py --selftest` 12/12 (`quality/check-axis-scores.py:11-14`;
  published row `SCORECARD.md:2722`). Two operability instruments — duplicate authority for the
  same axis name.

## 5. No-harm (existing behaviour that changes)

- `quality/landing-counters.sh` selftest grows 58 → 62 assertions (verified: base 58/58 rc 0,
  draft 62/62 rc 0). No committed caller parses that count: `c2-r65/r66-landing-instrument.py`
  check rc only; only historical receipts/lessons mention `58/58`.
- The 4 added assertions pin the exact guard text (draft 157-172); a formatting-only rewrite of
  base line 73 turns the standing selftest red. Intended by the executor and consistent with the
  frozen literal, but it is a new maintenance constraint.
- Child env changes are additive (`GIT_NO_REPLACE_OBJECTS`): used-by fresh dict (draft 59-71),
  ledger whitelist (draft 101-112), citecheck `dict(os.environ, …)` (draft 103). No other key
  changes; no caller depends on the exact env key set (`grep` of `quality/`, `tools/`).
- **Break:** two new `quality/counters/*.py` files without ledger rows turn the standing
  instrument's ledger leg red at the measured revision (B2). The C2 counter cannot see this
  because it only runs the instrument's hermetic `--selftest` (`measure` 384-410), whose ledger
  leg is a shim.

## 6. Claim sizing

Finite denominators (6, 2), no universal fault-coverage clause in C2, kill rules stated in the
freeze commit before any candidate byte exists. One universal statement is contradicted by its
own table: `claims-declaration-r67.md:17-18` "Every published scored sub-axis sits at its finite
maximum … so no axis is distinctly lowest" versus line 25 `calibration / register structural
discrimination … 4/6 = 6.6667` (B4). The stated C2 kill rule ("exits nonzero on the mutant") is
weaker than the implemented rule for M-R (`forged_credit`, counter 489-490) and would admit a
crash-kill for M-Z without the implemented `bash -n` gate (B9).

## 7. Chronology

| commit | epoch | local | content |
|---|---|---|---|
| `0b28ffb4` | 1793751532 | 21:18:52 | pre-r67 base tip |
| `aa7fe5a1` | 1793751993 | 21:26:33 | r67 controls + do-nothing baseline receipt |
| `061dc329` | 1793751998 | 21:26:38 | claims declaration (only this file) |
| `ac376ef3` | 1793752203 | 21:30:03 | wave spec, dispatch, registry |

`git diff aa7fe5a1..061dc329 -- .ufo/waves/round-67/controls` empty (rc 0); same diff to `HEAD`
empty (rc 0) — expectations never changed after first scoring. `git show --stat 061dc329` is the
declaration alone, so no candidate bytes existed at freeze; drafts are mtime 21:31+ (after).
Baseline was scored against the pre-freeze base (`--base 0b28ffb4`) and committed in the parent
of the freeze commit: order is baseline → freeze, and no executable candidate data was scored
before the freeze. Caveat: the C1 receipt's base is correct; the C2 scorer's *default* base is a
different revision (B7).

---

## Blockers

### B1 — C2/M-R: the tested child is not the child the baseline measured; the hazard needs a scrubbed env (P1)

- `claims-declaration-r67.md:90-92` "M-R: the `GIT_NO_REPLACE_OBJECTS` guard removed from the
  git-reading landing child"; `c2-r67-landing-controls.py:57-60` binds `R_PATH = CITECHECK` =
  `tools/mado-receipt-citecheck.py`; `:118-120` `child_env()` returns `_base_env` (all inherited
  `GIT_*` scrubbed, no guard).
- At base the child passes no `env=` to `subprocess.run` and inherits the instrument's
  `export GIT_NO_REPLACE_OBJECTS=1` (`quality/landing-counters.sh:6-8`, dispatch at 43).
  Measured: with the inherited key `rc=1 TARGET_MISSED missing=1` (real); with the counter's
  scrubbed env `rc=0 TARGET_MET missing=0` (forged). `evidence/mr-inherit.py`.
- The baseline receipt's own operand is different: `control-baseline-r67.txt:18-19`
  `usedby_guard=0 ledger_guard=0` and `child_env_read=forged` from a *replica* of the used-by
  env (`score-baseline-c2.py:85-90`), not the citecheck child.
- Impact: C2's M-R half of the 0→10 is a standalone-tool/defense-in-depth hardening; as a
  landing-path claim it is false for the tested child (already protected by inheritance).
  Axis: operability (attribution overstated).
- Smallest safe correction: bind `R_PATH` to `quality/counters/c3-r56-used-by.py`, whose
  `git_env()` is a fresh dict (draft 59-71) so the mutant is vulnerable even when launched by
  the instrument, and give the R fixture a verdict that child is sensitive to; or amend the
  predicate to name `tools/mado-receipt-citecheck.py` and the scrubbed-env premise and delete
  "the pre-r67 tip … its child reads a planted replacement" for that child.

### B2 — C1+C2: new counters break the standing instrument's ledger leg at the measured revision (P1)

- `quality/check-tool-ledger.py:13` population includes `quality/counters/*.py` direct children
  (predicate 171-179). Real lane at base: `LEDGER: population=108 ledger_rows=108 uncovered=0 …
  TARGET_MET` rc 0.
- Fixture = base `tools/` + `quality/` + the C1 draft counter, no new ledger row:
  `LEDGER-ROW reason=uncovered path=quality/counters/c1-r67-register.py detail=no-row`,
  `LEDGER: population=109 ledger_rows=108 uncovered=1 … TARGET_MISSED`, rc 1
  (`evidence/fx-ledger.sh`; `bad_pointer` in this fixture is noise from the deliberately partial
  tree — the real base run above is green). The C2 counter adds a second population file → +2.
- The instrument's ledger leg is `landing-counters.sh:42`; at the measured revision it returns
  rc 1 → `MADO_LANDING_COUNTERS: RED`, while the C2 counter prints `TARGET_MET` because it only
  runs `--selftest` on fixtures. The declaration's file sets (`:108-111`) omit
  `quality/tool-ledger.md`.
- Correction: add one ledger row per new counter to `quality/tool-ledger.md` in the landing
  commit (same commit as the cutover) and add that file to both claims' touch lists; verify
  `python3 quality/check-tool-ledger.py --repo . --rev <measured>` gives
  `population == ledger_rows`, `uncovered=0`, rc 0.

### B3 — C1: residual loss of the r66 block-wide unresolved-receipt invariant (P2)

- r66 rejected any named receipt in the register block that does not resolve
  (`quality/counters/c1-r66-register.py:105-108`). The r67 draft checks only fourth-cell pointers
  (draft 164-171). A receipt path in a **probe** cell that does not resolve is accepted by r67
  and rejected by r66.
- Repro `evidence/fx2.py`: `r66 accept=False reasons=['receipt-unresolved=…not-committed.txt']`,
  `r67 accept=True reasons=[]`. The reviewer's earlier same-cell P1 is fixed
  (`evidence/c1-regression.py`: both reject when the dangling path is in the receipt cell).
- Correction: restore the block-wide `paths = receipts_in("\n".join(block))` loop. Verified
  harmless to the frozen denominator: `evidence/fx-fix.py` →
  `FROZEN_VERDICT_CHANGES=0` across all six cases.

### B4 — C1: declaration contradicts its own axis table (P2)

- `claims-declaration-r67.md:17-18` "Every published scored sub-axis sits at its finite maximum
  at the base revision, so no axis is distinctly lowest" versus line 25, a scored sub-axis at
  `4/6 = 6.6667`. Either the row is a base sub-axis (then it is the distinctly lowest and the
  sentence is false) or it is not (then it must not carry a base value).
- Correction: state that the r67 control set creates a new finite denominator whose do-nothing
  score is 4/6, and keep "no published base sub-axis below max" for the three 10.0000 rows only.

### B5 — C2: the frozen Z marker is a fragment the contract cannot accept (P2)

- `claims-declaration-r67.md:84-86` freezes a marker "carrying `citations=0 resolved=0
  missing=0 verdict=TARGET_MET`". `marker_valid` requires `rev=$REV` before the citecheck branch
  (draft/base line 64) and the regex needs `files=`/`skipped_large=` fields around the counters
  (line 71). A literal implementation of the quoted fragment is ERROR **with and without** the
  guard, so M-Z would never be killed.
- The implemented fixture emits the full line (`c2` fixture via draft line 124), so the kill is
  reproducible from the counter but not from the declaration text — the r66 M67-1 class
  (`corpus/lessons/round-67.md`, mistake row).
- Correction: freeze the complete 7-field marker bytes (`MADO_CITECHECK: rev=<rev> files=…
  citations=0 resolved=0 missing=0 skipped_large=0 verdict=TARGET_MET`).

### B6 — C2 baseline: kill count is a constant and the case inventories count the wrong literals (P3)

- `score-baseline-c2.py:91` `killed = 0`, printed at 96 as `killed={killed}/2` — asserted, not
  measured. `:67-68` `zero_citation_case = landing.count("citations=0")` and
  `replace_ref_case = landing.count("refs/replace")` count fixture literals, not the guards; the
  zero-citation guard is present at `landing-counters.sh:73` and the replace-ref parent export at
  line 8. `zero_citation_case=0` therefore does **not** mean zero-citation evidence was credited
  at base; the base instrument refuses it (section 1).
- Correction: derive the base kill count by running `c2-r67-landing-controls.py` at the base rev
  (now 0/2, rc 1, as measured) and label the inventory fields `fixture_literal_count`.

### B7 — C2 baseline scorer's default base is a different revision (P3)

- `score-baseline-c2.py:25` `BASE = "eafd500fa7be76dca59e729435e231a5032cc037"`;
  `quality/landing-counters.sh` there is `27a05b8d…` versus base `e4767ec7…` (`c3-r56-used-by.py`
  identical). The receipt passes `--base 0b28ffb4`, so the committed numbers are valid; a re-run
  without `--base` silently scores the wrong instrument.
- Correction: default to the frozen base or make `--base` required.

### B8 — C1: PROVINCE heading-prefix hazard at the measured revision (P3)

- `HEADING = "### Surface state register (2026-11-03"` (draft 69); `starts` scans all of
  PROVINCE (draft 132), and `heading-count != 1` is a rejection. Any round-67 PROVINCE append
  that repeats that heading prefix (instead of the r65/r66 bold-paragraph convention) makes
  `register=reject` at the measured revision even with 6/6 controls.
- Correction: keep the append convention and assert `register=accept` at the measured rev in the
  landing receipt.

### B9 — C2: the declared kill rule admits crash-kills; the implementation is stricter (P3)

- `claims-declaration-r67.md:96-99` "counts killed only when the control set exits nonzero on
  that exact mutant". A mutant that breaks the script (syntax/rename damage) also exits nonzero.
  The counter already does better: `bash -n` gate before the M-Z run (draft 426-428) and
  `forged_credit` for M-R (489-490, requires rc 0 + `TARGET_MET` + `missing=0`), plus
  `recipe=none killed=no` when the literal is not exactly once.
- Correction: adopt the implemented rule in the declaration text: killed = mutant is
  syntactically valid, the recipe applied exactly once, and the control fails in its designed
  classification (Z: refusal assertion red; R: forged credit observed).

---

## Confirmations (no finding)

- Neither target is met at the pre-r67 tip (section 1); both claims are measurable at a candidate.
- C1 draft: `MADO_R67_REGISTER: register=accept controls=6/6 headings=1 rows=8 groups=8/8
  live-cited=yes verdict=TARGET_MET` rc 0 at base; `--selftest` 15/15 rc 0; the frozen printed
  line matches label-for-label.
- C2 counter at the candidate rev (drafts copied to a scratch repo): `selftest=0 mz=pass mr=pass
  killed=2/2 baseline=0/2 verdict=TARGET_MET` rc 0; at base `killed=0/2` rc 1; mutant diffs are
  printed with sha256 (`evidence/fx-c2.sh`). M-R's mutant sha equals the committed base child
  (`414ca759…`), i.e. the mutant reproduces the pre-r67 artifact.
- C2 counter `--selftest` 47/47 rc 0; instrument draft `--selftest` 62/62 rc 0; base instrument
  `--selftest` 58/58 rc 0.
- Controls are immutable since first scoring (section 7); no candidate bytes existed at freeze.

## Scratch

`/fast/scratch/hyaku/mado-r67/R67CriticClaims/` removed after the final evidence run; no lane,
fleet, sibling-lane, `MANIFEST.json`, `.ufo/state` or operator-config write was made. No tool
install or upgrade was needed; no pacman transaction was attempted.
