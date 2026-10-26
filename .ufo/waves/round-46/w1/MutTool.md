# MutTool (MutTool-4) — C1 reference mutation testing, round 46 w1

Status: COMPLETE.

## What ran
- Target: `.ufo/waves/round-46/l1-draft/mado-devices.py` (sha256 `b229efd0…a33b`, matches the counter's frozen pin; verified before and after).
- Detector: in-process replay through the reference's own `selftest()` + all 90 frozen fixtures (`quality/counters/c1-r46-fixtures.json`, sha256 `027ed508…3fc1` verified) via `run()`, placeholders substituted with the counter's `names(46)`, `@BIG`/`@BIGDUMP` expanded as `run_fixture` does. Baseline pristine: selftest 48/48, fixtures 90/90, re-verified green after all mutants.
- 104 mutants (constants, operator/comparison swaps, branch deletions/inversions, off-by-one slices in comment/bracket/continuation parsing, arg parsing, I/O, format/rc mapping), one minimal edit each, all in scratch.

## Verdict
- **93 killed / 11 survived / 0 generation errors.**
- 9 genuine survivors = unpinned semantics, each with a demonstrated killing fixture (pristine vs mutant outputs in the receipt): B10 (non-finite reported scrollFactor prints inf/nan instead of ?), B36 (config decode errors=replace→ignore — **inexpressible in the fixture schema**, unpinned by the whole counter), C02 (trailing-`#` line → IndexError), J05 (chained backslash continuations), K09 (uppercase NaN/INF/0X), K13 (FLT_MIN binade (2⁻¹²⁶,2⁻¹²⁵)), P15 (two bracket groups in one key), P24 (rename-then-name creates a phantom block; escapes selftest because the selftest checks the summary only via `endswith("verdict=…")`), R05 (exactly 2⁻¹²⁶).
- 2 equivalent survivors (no coverage gap): P16 (`lb == rb` impossible), B38 (read_stdin loop bound redundant behind the post-loop too_large check; demonstrated identical on a MAX+1 stdin payload).
- Meta-findings for the L1: (1) B36 needs a raw-config-bytes fixture kind (`@RAW:<hex>` marker) — configs are always valid UTF-8 by construction in both fixtures and generated cases; (2) selftest summary check should compare the whole line, not `endswith`; (3) clause f's generated cases are judged by the reference itself, so they would kill the 9 mechanically but pin nothing the reference gets wrong — fixtures/selftest are the independent pin and these 9 are where it is missing; (4) fixture-shape gaps listed in report.md.
- Sentinel cross-ref: SentTool-3's F1/F2 (clause-r sandbox) do not affect this in-process detector; routed to the L1 per its findings.md.

## Evidence
- `evidence/receipt.txt` — timestamped consolidated run: baseline, all 104 verdicts with killers, survivor killing-input demonstrations, restoration sha256s.
- `evidence/index.json` — the 104 mutation sites; `evidence/results.json` — per-mutant verdicts.
- Restoration: reference and fixtures sha256 unchanged (receipt tail); lane files never written; scratch `/fast/scratch/hyaku/mado-r46/MutTool/` deleted after copying receipts. No tool installs (python3 only).

Report: .ufo/waves/round-46/w1/MutTool.md
