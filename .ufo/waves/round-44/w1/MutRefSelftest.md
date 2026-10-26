# MutRefSelftest — round 44 w1 (final)

Seat: mutation-test `client_fsmode` in the frozen reference `.ufo/waves/round-44/c1/ctl-ref-tool.py.txt` (>=30 mutants), detector = its own `--selftest` (python3 -I); selftest survivors scored against the frozen counter `quality/counters/c1-r44-geometry-states.py` (26/26 target).

## Result

**33 mutants, 15 killed by the selftest, 18 selftest-survivors, 0 counter-only kills, 0 counter-killed survivors.** All 18 survivors score `PRED-C1-r44: fixtures=26/26 … verdict=TARGET_MET` (clause b selftest 91/91, clause b4 all comparison sites killed, clause r round-42 regression 37/37). Classification: **14 equivalent (proofs in matrix)**, **4 downstream-equivalent but unit-distinguishable — missing assertions given**:

- M07 `f in (1, 2, 4)`: `client_fsmode({"fullscreen": 4})` -> expect 0, mutant returns 4.
- M08 `f in (1, 2, -1)`: `client_fsmode({"fullscreen": -1})` -> expect 0, mutant returns -1 (counter feeds -1 in fsvals0 but -1 is verdict-equivalent to 0, so fixtures cannot kill it).
- M27 `return 0.0`: `client_fsmode({})` -> expect 0 of type int, mutant returns 0.0 (selftest `chk` compares with `==`, so 0.0 == 0 passes; killed only by a type-strict assertion).
- M28 `return False`: `client_fsmode({"fullscreen": 3})` -> expect 0 of type int, mutant returns False (same `==`-masking).

## Findings

1. Selftest >= counter on `client_fsmode`: the unit checks `fsmode-values`/`fsmode-absent` (reference lines 458-459) pin the mapping tighter than any end-to-end fixture, because the verdict chain only tests `fsmode == 2` / `fsmode == 1` (line 230 callsite, lines 233/235 comparisons).
2. The reference's gate-then-membership structure makes whole mutation classes vacuous: widening the membership tuple with wrong-typed values (`"2"`, `"1"`, `1.0`, `True`) or switching to a chained range `1 <= f <= 2` is unreachable behind the isinstance gates — 5 mutants I predicted would be killed survived for this reason. The type guards, not the tuple, carry the discrimination.
3. `chk` uses `==`, so return-type mutants (0.0/False) are invisible to the selftest; a type-strict unit assertion would close it.
4. The counter's load-bearing teeth on this function are clause b4 (14 sites flipped, 14/14 selftest-killed on every survivor receipt), not the fixtures.
5. No assertion gap in state-verdict behavior itself: every mutant changing a verdict on any fed input is killed (15/15).

## Evidence

- Matrix with all 33 rows, hashes, failing-check names, counter nonces, proofs/assertions: `.ufo/waves/round-44/w1/MutRefSelftest/matrix.md`
- Raw receipts (copied out of scratch before deletion): `.ufo/waves/round-44/w1/MutRefSelftest/evidence/selftest.json` (per-mutant sha256, selftest tails, probe grids) and `evidence/counter_M*.txt` (18 full counter runs).
- Restoration: pristine sha256 `8e871a00fcf1a615e3683ebe5204f67cfe679182ff15d008b83fed34131c788d` before and after all runs, byte-identical to the frozen file; pristine selftest `91/91 passed` rc 0 after all mutations. Mutants were separate files under scratch; the frozen reference, counter, controls, registration and every other lane file were never written.

## Method notes

- All work dirs under `/fast/scratch/hyaku/mado-r44/MutRefSelftest/` (mutants in `mut/`, outputs in `out/`); scratch deleted at the end per operator directive; only seat-dir files cited.
- Each mutant = one edit applied to a separate copy of pristine bytes, `old` verified unique within the `client_fsmode` slice (def line 195 to next top-level def); no other function touched.
- Counter invoked exactly as tasked: `cd /home/vgpnk/Projects/shokunin/mado-shokunin && python3 -I quality/counters/c1-r44-geometry-states.py --repo . --rev e2289516a9a857f55cda7be635933e89b931c3da --tool <mutant> --work /fast/scratch/hyaku/mado-r44/MutRefSelftest`; random nonce per run (recorded per row).
- No tools installed; no pacman; no host-service or compositor mutation; no subagents, no background jobs beyond the shell's own batching.
