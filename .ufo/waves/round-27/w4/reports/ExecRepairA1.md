CANDIDATE /fast/scratch/hyaku/mado-r27/repair/ExecRepairA1/counter-selftest.py
sha256:65aa2e24e698fa119803e4a7c93c72403b0ac7fe608a0f5484b097bb4ba3df25

# ExecRepairA1 — round-27 wave w4, C2 repair seat (suite A)

Repair of `quality/counter-selftest.py` (committed at 5c1d495; candidate-of-origin
`/fast/scratch/hyaku/mado-r27/data/ExecSuiteA1/counter-selftest.py`, sha256
`7fd94b0431849d1be7dc99e120c2f5bd0105c6a1d122e9cd1a3327d30ef3c587`). The gate over the
round-26 bind counter `.ufo/waves/round-26/c2/count.py` gained eight behavioural checks so
that the three surviving held-out classes — extra-disjunction, unstable-conjunction and
embed-boundary — are now caught. No existing check was removed; the CLI contract
(`--c1 PATH --c2 PATH --rev REV`, plus `--scratch`/`--keep`) is unchanged. The sealed
held-out directory was never read or executed; only the three public mutant names from the
measurement-1 receipt were used as signal.

## Per-class evidence

Mutant rows in `/fast/scratch/hyaku/mado-r27/repair/ExecRepairA1/mutants.json`; ready-to-use
subject copies under `mutants/`. Current-suite column = committed 5c1d495 suite
(`committed-baseline.py`); repaired column = the candidate. All runs via
`tools/matrix.py` on a sandbox clone (`laneclone/`, a `git clone` of the lane at REV
48b9434a; the lane itself was never mutated). Full transcript: `logs/final-matrix.txt`.

### extra-disjunction — `mutants/exec-repair-a1-extra-disjunction.py`

    old:            verdict[lab] = (nm == 0 and ne == 0, info, len(exp))
    new:            verdict[lab] = ((nm == 0 and ne == 0) or (nm == 1 and ne == 0), info, len(exp))

Why the committed suite misses it: every committed field-level probe changes one field of
one bind entry, which under `V3.compare` (keyed on all 18 FIELDS) produces one missing AND
one extra entry at the same time. No committed probe ever produces a one-sided difference
(nm=1,ne=0 or nm=0,ne=1), so a disjunct tolerating exactly one side is invisible.
Current-suite rc=0 (SURVIVED, pass=48/48). Repaired-suite rc=1, `FAILED c2-one-missing`
(pass=55/56) — KILLED.

### unstable-conjunction — `mutants/exec-repair-a1-unstable-conjunction.py`

    old:        if n1 or n2:
    new:        if n1 and n2:

Why the committed suite misses it: the two-BASE-run stability guard compares r1 against r2.
The committed `c2-drift` probe perturbs one field of one entry, which changes the entry's
18-field key on BOTH sides of the multiset difference at once, so n1=1 and n2=1 — the
conjunction still fires and the mutant survives. A one-directional disagreement (a table
that is a strict superset or subset, differing in exactly one entry) gives (1,0) or (0,1),
which `or` fires on and `and` does not. Current-suite rc=0 (SURVIVED, 48/48).
Repaired-suite rc=1, `FAILED c2-drift-extra,c2-drift-missing` (pass=54/56) — KILLED.

### embed-boundary — `mutants/exec-repair-a1-embed-boundary.py`

    old:            strs = {e[f] for e in base for f in ("arg", "description") if isinstance(e.get(f), str) and len(e[f]) >= EMBED_MIN}
    new:            strs = {e[f] for e in base for f in ("arg", "description") if isinstance(e.get(f), str) and len(e[f]) > EMBED_MIN}

Why the committed suite misses it: the committed embed fixtures use 40-character strings,
far from the EMBED_MIN=12 boundary, so the mutant's 12-char exclusion is never exercised.
The repaired suite adds fixtures at exactly 12 (must hit) and exactly 11 (must not) chars.
Current-suite rc=0 (SURVIVED, 48/48). Repaired-suite rc=1, `FAILED c2-embed-at-min`
(pass=55/56) — KILLED.

## New checks (8; names registered in REQUIRED, total 48 -> 56 probes)

- `c2-one-missing` / `c2-one-extra`: tool output off by exactly one bind entry (each side
  of the multiset difference isolated) → must be `rc=1`, `TARGET_MISSED`, `cases_pass<total`.
- `c2-two-missing` / `c2-two-extra`: same, two entries — kills wider tolerance disjuncts.
- `c2-drift-extra` / `c2-drift-missing`: second BASE oracle run returns a strict
  superset/subset table (one-directional difference) → must be `rc=2`, `ORACLE_UNSTABLE`.
- `c2-embed-at-min` (12-char base arg in tool bytes → `rc=1`, `embed_hits>=1`) and
  `c2-embed-below-min` (11-char base arg → `rc=0`, `embed_hits=0`, `TARGET_MET`).

## Independent cross-check shapes (also killed)

`crosscheck.json` contains four shapes not among my three class mutants — two taken from the
public RevRepair report plus both directions of the embed boundary. All killed:

    xref-extra-disjunction-sum    FAILED c2-one-missing,c2-one-extra
    xref-embed-boundary-constant  FAILED c2-embed-at-min            (EMBED_MIN 12->13)
    xref-embed-below-boundary     FAILED c2-embed-below-min         (12->11 direction)
    xref-unstable-conjunction-ne  FAILED c2-drift-extra,c2-drift-missing

## Green + W transcript (frozen counter `.ufo/waves/round-27/c2/count-v2.py`, REV 48b9434a,
`--suite-a-file` override)

    SUBJECT .ufo/waves/round-26/c1/count-v2.py              sha256:4ed70b54...
    SUBJECT .ufo/waves/round-26/c2/count.py                 sha256:b92c32da...
    SUBJECT .ufo/waves/round-26/quality/check-population.py sha256:803e0096...
    SUITE A override:.../counter-selftest.py sha256:65aa2e24e698fa119803e4a7c93c72403b0ac7fe608a0f5484b097bb4ba3df25
    GREEN pristine                       suite=A rc=0 PASS
    GREEN comment:count-v2.py            suite=A rc=0 PASS
    GREEN assign:count-v2.py             suite=A rc=0 PASS
    GREEN comment:count.py               suite=A rc=0 PASS
    GREEN assign:count.py                suite=A rc=0 PASS
    (suite-B rows omitted here; see logs/c2v2-repaired.txt — all PASS)
    W:c1-drop-bezier            KILLED   W:c1-accept-nonjson   KILLED
    W:c1-pass-90pct             KILLED   W:c1-skip-base-guard  KILLED
    W:c2-accept-nonjson         KILLED   W:c2-pass-90pct       KILLED
    W:c2-skip-base-guard        KILLED   W:c2-embed-min-1000   KILLED
    W:c2-drop-arg               KILLED   (6 suite-B W rows all KILLED)
    PRED-C2-r27-v2 green=8/8 w_killed=15/15 (no heldout supplied)

Benign-edit mechanism: six reconstructed semantics-preserving rewrites of the C2 subject
(the three named benign classes from the w1 report — null-demorgan, identity-negation,
return-inversion — plus guard/embed/met equivalence rewrites) all stay green under the
repaired suite (`tools/benign-check.py`, `logs/benign-check.txt`: BENIGN-FAILURES 0).

## Diff summary vs the committed suite

97 insertions, 1 deletion (full diff: `logs/diff-vs-committed.diff`):

- constants: `C2_DRIFT_EXTRA`, `C2_DRIFT_MISSING`, `C2_EMBED_12`, `C2_EMBED_11`,
  `MUT_ONE_MISSING`, `MUT_ONE_EXTRA`, `MUT_TWO_MISSING`, `MUT_TWO_EXTRA`;
- eight new `run_case`/`record` probes in `main()` plus their REQUIRED inventory entries
  (48 -> 56 total checks); docstring header count updated 45 -> 55 probes accordingly;
- nothing else: `FakeOracle`, `run_case`, `make_snapshot`, the C1 section and all 48
  existing checks are byte-identical. (An earlier draft added an unused `fail_nth`
  parameter; removed — the final file carries no dead plumbing.)

Note on landed state: sibling seat ExecRepairA2's repaired suite was already committed at
0b53bd8 (sha256 aa0e14d1...) before this seat returned. Independently, that landed file
also kills all three of my class mutants and all four cross-check shapes under
`tools/matrix.py` (pass=56/56 pristine; rc=1 on every mutant). This candidate is a
fully-verified backup with identical coverage of the three held-out classes.

## Tooling

No tools installed or upgraded; python3 stdlib only. All suite runs under
`env -i PATH=/usr/bin HOME=...` (isolated), in a scratch clone of the lane; the lane
working tree was never written except this report. No subagents; heldout never opened.

Report: .ufo/waves/round-27/w4/reports/ExecRepairA1.md
