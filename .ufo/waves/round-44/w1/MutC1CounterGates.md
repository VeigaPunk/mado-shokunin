# MutC1CounterGates — mutation-test PRED-C1-r44's gates (round 44, w1)

Task: each gate of the frozen counter `quality/counters/c1-r44-geometry-states.py` must be able to fail. Method: 34 single-edit mutants (one behavior-bearing edit each, exact-match-once verified) run through the same bounded detector as the pristine and restored bytes: score subject files with `python3 -I <counter> --repo LANE --rev e2289516a9a857f55cda7be635933e89b931c3da --tool <subject> --nonce mutc1w1a`, judge rc + final line. Subjects: the reference `.ufo/waves/round-44/c1/ctl-ref-tool.py.txt` (must stay MET = not over-strict) and K01..K13 regenerated in scratch from the FROZEN `run-c1-controls.py` VARIANTS (imported, its scoring loop never run; all must stay MISSED). Full matrix: 34 × 14 = 490 runs + baseline + restoration rerun, 543 s wall at -P14.

## Verdicts
- Baseline OK: pristine counter → REF TARGET_MET 26/26 (a:1 b:1 b4:1 g:1 r:1), 13/13 controls TARGET_MISSED — matches frozen `receipts/ctl-c1.txt` pattern.
- **1 GATE BROKEN — B1-selftest-50**: `MIN_SELFTEST = 80 → 50` makes control **K13-no-new-selftest score TARGET_MET** (26/26, a:1 b:1 b4:1 g:1 r:1). K13's selftest is **73/73** (evidence/logs/B1-selftest-50__K13-no-new-selftest.log): the 80-floor is the *only* registered guard against a hollowed selftest. b4 does NOT backstop K13 — under the cut selftest its 14 state sites still kill 13/14 ≥ need 11, because flipping any `mode ==`/`f in (1, 2)` comparison changes every matched client's verdict, state case or not; clause r stays 37/37; fixtures stay 26/26. Coverage finding (not a contract change): no registered control carries a state-logic defect inside a selftest-consistent tool with n ≥ 80 — exactly the cheat b4 exists for; one such control would guard MIN_SELFTEST, KILL_FRACTION and b4 simultaneously.
- 12 KILLED over-strict (reference itself fails): D1 (judge accepts True/2.0 → fsvals0 23/26), D5 (18/26), V2 (25/26), V3 (23/26), S1 (10/26), S2 (19/26), B2 (selftest 91 < 200 → b:0), R1 (r:0, fixtures 26/26), P1 `old.model_out` patch removed (judge reverts to r42 model, 15/26 — the patch is load-bearing). Plus T1/T2/T3: any TOTAL/N_GEN drift trips `assert len(cases) == TOTAL` → rc=1 crash on all 14 subjects (brittle but fatal).
- 21 SURVIVED, classified in `w1/MutC1CounterGates/matrix.md`: 8 equivalent by construction with verdict-identical output on all 14 subjects (D2/D3/D4/D6 fsmode_of domain forms on the json type universe; V1 disjoint mode tests; S3 `a+b>0 ⇔ a or b`; R2/R3 — rc==0 ⇔ `verdict=TARGET_MET` in the r42 subprocess, c1-r42-geometry.py:999-1003); 3 equivalent-on-reference with declared residual (Y3 sites 14→14 killed 14; Y4 all 14 flips die via rc≠0/missing summary; G2 `"fullscreen": "absent"` → 0 on both sides); 10 missing-control/redundant findings (B3 drops `k == n` from b; S4/S5 MIN_STATE_SITES floor not load-bearing — b4 is skipped entirely when b=0; K14/K15 KILL_FRACTION not load-bearing — reference kills 14/14 so even `kill=1.0` passes; Y1 `state_teeth → True` survives; F1/F2 FS_POOL and G1 fullscreenClient sprinkle are redundant depth behind fsvals0/fsmany0/fsclient0; X1: fixture content is unobservable while tool and judge agree — a fixture IS the judge, only its count is asserted).

## Restoration evidence
- Lane bytes never touched; before/after sha256 identical: `c1-r44-geometry-states.py` f6b42b059b6b1f6f16657d37b0d15bd11541b04962e60154596f9037c614de65, `c1-r42-geometry.py` ed78d6930545aedc1b529f06dd3f9bce0d1ead88832ae3f53a125263a316ff99 (frozen copies preserved at `w1/MutC1CounterGates/evidence/`).
- Post-matrix pristine rerun on REF: TARGET_MET 26/26 rc=0 (restored-bytes detector run).

## Evidence (all in seat dir, scratch deleted)
- `w1/MutC1CounterGates/matrix.md` — full 34-row table (gate, REF outcome, controls MET, verdict, note).
- `w1/MutC1CounterGates/evidence/results.tsv` — 967 rows (14 pristine + 476 fresh mutant-subject rows; earlier 476 aborted rows superseded by the later run of the same keys).
- `w1/MutC1CounterGates/evidence/logs/` — PRISTINE__REF, PRISTINE__K13, B1-selftest-50__K13 (the gate-broken run), K15-kill-1__REF (need=14 kills=14), Y3-case-sensitive__REF.

## Notes
- Tools installed: none (system python 3.14.0, bwrap 0.11-adjacent 0.13.1, git already present; no pacman transactions).
- Scratch `/fast/scratch/hyaku/mado-r44/MutC1CounterGates` deleted at seat close; every claim above cites seat-dir files or frozen lane paths.
- Simulator note: log lines quoted in matrix.md are computed from results.tsv/logs, not retyped.
