# MutC1Counter — C1 counter mutation testing (round 45 w1) — DONE

Target attacked: `quality/counters/c1-r45-monitors.py` (PRED-C1-r45), frozen sha256
`c69ddee44a9fa3c442b910541038a9440ac72c2b5f21fe4899cb8f5df9213f34` — byte-identical before and after the
campaign (mutants lived only in scratch copies; lane untouched).

## What ran

38 single-edit mutants + identity baseline, each anchor-verified unique in the frozen text, run at seed 45
against the REF control and all 16 registered bad controls (K00/K01/K02 + K03–K15) rebuilt in scratch with
the frozen `run-c1-controls.py` build/VARIANTS logic (17 repos, toplevel asserted, BASE
`0c89478af821a6424c9ac922eafe02e39630cf4f`). 551 counter runs; zero crashes; every control death clean.
Baseline reproduced the registered outcome: REF TARGET_MET 49/49, 0 of 16 controls MET.

## Verdict

- 3 **GATE-BROKEN** (killed): M1/M2 (forcing `fixtures_ok`) and M5 (`met` and→or) let K02-STUB and/or
  K14-MIRROR-IGNORED (and K08 for M5 — 2/49 fixtures, readonly=fail, still MET) score TARGET_MET.
  The met-aggregation is genuinely guarded by the panel.
- 7 **OVER-STRICT** (killed): E1–E5 (fixture-expectation edits) and R5/R6 (timeouts→1ms) break REF
  certification — the contract encoding cannot be silently relaxed.
- 28 **SURVIVORS** (REF MET, 16/16 MISSED): 3 equivalent with proofs (V2 marker-name single-variable;
  A2 blob check redundant given the mode set; N1 dedupe provably inert at seed 45 — identical names table,
  latent divergence on 9/200 seeds), and **25 missing-control survivors**: every single-edit weakening of
  SELFTEST_MIN (S1/S2), the selftest parse (S3–S7), the fixture rc/stderr/timeout checks (R1–R4), the
  readonly clause (V1/V3/G3), clause-a mode check (A1), the met s/r conjuncts (M3/M4), the substitution and
  seed/name plumbing (E6/N2–N5) and the env pins (G1/G2/G4) is invisible to the current panel — those
  checks are never any control's sole killer (attribution: K02/K08/K14 pass selftest and die only on
  clause-f exact bytes; K03–K13/K15/K01 are double-killed s+f; K08 double-killed f+r; K00 dies on a alone).

Full matrix, per-survivor adjudication, proofs and 7 one-control coverage fixes:
`.ufo/waves/round-45/w1/MutC1Counter/matrix.md`.

Report: .ufo/waves/round-45/w1/MutC1Counter/matrix.md
Receipts: .ufo/waves/round-45/w1/MutC1Counter/{results.json,summary.txt,mutdrive.py,c1-r45-monitors.py}

Tooling: nothing installed (python3 3.14.8, stdlib only). Scratch purged after receipts were copied.
