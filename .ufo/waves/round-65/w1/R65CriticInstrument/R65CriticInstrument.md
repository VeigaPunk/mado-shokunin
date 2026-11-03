# R65CriticInstrument — copy of report.md

This file is an identical copy of `report.md` in the same seat dir. The orchestrator trailer path `.ufo/waves/round-65/w1/R65CriticInstrument.md` lies outside the seat-dir write scope, so the copy is kept here. See `report.md` for the full ranked defect list, probes, and evidence.

Headline (ranked):
- BLOCKER B1: citecheck leg reads the working tree, not committed bytes (landing-counters.sh:60-64; citecheck collect_files:78-95). Dirty receipt → rc=1; clean → rc=0.
- BLOCKER B2: citecheck returns TARGET_MET on an empty set (citecheck :94 note only; :140 ignores it). `--paths <nonexistent>` → rc=0, files=0 citations=0.
- BLOCKER B3: landing commit must add a quality/tool-ledger.md row for quality/counters/c2-r65-landing-instrument.py (check-tool-ledger.py:78-82 population). Fixture landing → ledger rc=1 uncovered, driver verdict TARGET_MISSED.
- BLOCKER B4: ambient GIT_DIR steers nav and citecheck legs (driver :113 subprocess.run inherits env; landing :38). GIT_DIR=empty repo → nav 0→1, citecheck 0→2.
- SHOULD-FIX S1: trailing-slash symlink root accepted (landing :190, driver :82). Landing selftest rc=0; driver proceeds.
- SHOULD-FIX S2: citecheck tool --scratch-root symlink→/tmp accepted (citecheck :223-224 abspath not realpath).
- SHOULD-FIX S3: landing selftest fixture git inherits host config; host hook writes outside scratch (landing :111, :116).
- SHOULD-FIX S4: host-guard toplevel assertion is advisory (landing :114-116); not reproduced.
- SHOULD-FIX S5: red vs crash indistinguishable; selftest a9 (:135) cannot tell (landing :219).
- SHOULD-FIX S6: nav leg non-ASCII note → ZeroDivisionError rc=1; check-index.py rc=0 (landing :38); latent in lane (0 such names).
- NOTE: N1 selftest stdout pid path (landing :114); N2 script-relative only at quality/ (PASS there); N3 /tmp audit clean; N4 relative scratch accepted; N5 /dev/shm accepted; N6 used-by no /tmp refusal; N7 a10 stubs all legs; N8 driver has no selftest; N9 C6 four-leg extraction complete (PASS); N10 landing per-leg rc captured (PASS).
