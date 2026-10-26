# Seat MutTool — round 45 w1 — REPORT (COMPLETE)

Mutation-test of the C1 reference tool `.ufo/waves/round-45/l1-draft/mado-monitors.py`
(sha256 `c6ac5fc2d35e40b34dcf031940222fbe5ec5f0ce4b07d6a41866b196843726be`, unchanged before/after — verified twice, frozen file only ever read).
Full matrix with per-mutant evidence: `.ufo/waves/round-45/w1/MutTool/matrix.md`; receipts under `.ufo/waves/round-45/w1/MutTool/receipts/`.

## Method
- 54 single-edit mutants (0 design errors; every old-string matched exactly once), spanning parse_line, parse_mode/parse_pos/parse_scale, add, effective, compare, expected_scale, verdict order, output formats, plus KEYS/V2_RE/MAX_BYTES/new_rule.
- Detector A: mutant `--selftest`. Detector B: frozen counter `quality/counters/c1-r45-monitors.py` on a scratch clone at the freeze commit `22a8dedd` (one commit per mutant; `rev-parse --show-toplevel` asserted before every commit; seed 45).
- Baseline control before any mutant: pristine reference → `fixtures=49/49 selftest=ok readonly=ok verdict=TARGET_MET` exit 0 (`receipts/ref-baseline.log`), agreeing with frozen `receipts/ctl-c1.txt` REF row. So detector B is sound; survivor verdicts are meaningful.

## Results (54 mutants)
- **18 KILLED_SELFTEST** (counter not run, per tasking) — matrix section D.
- **14 KILLED_FIXTURES only** (selftest 33/33 ok, counter TARGET_MISSED) — each with the failing fixture names and the missing selftest assertion — matrix section C. Recurrent hole: the selftest asserts only OUTPUT-line suffixes and the final verdict, never MADO_MON_RULE text or summary tokens, and has no case for `highres`, `disabled` spelling, `auto-left`, negative positions, tiny scales, ignored keys, `sdr_eotf`, or desc-contains-but-not-starts.
- **22 SURVIVED both** — matrix section B, split:
  - **19 coverage gaps**, each with a demonstrated distinguishing input (config + dump), reference output (= contract-expected) and mutant output, verified by running both binaries this session (`receipts/demo-evidence.json`). Highlights: rate tolerance `< 0.5` survives (no fixture with |Δrate| in [0.5,1.0) — e.g. rr=99.5 vs @100); scale tolerance `>= 0.001` survives (no fixture with |Δscale| in [1e-4,1e-3) — e.g. live 1.0005 vs S=1); 1/120-correction search depth `range(1,45)` survives (no fixture needs step >44 — w=3441,h=1441 with S=1.45 needs step 54); downward-only candidates dropped survive (E found at (K−i)/120); round-half-up vs floor survives (S=0.837501, 85x85: K=101 vs 100 give different E); `transform 7` accepted→rejected survives; `desc:` strip-of-spaces survives (`desc: DP-1` with space); `S <= 0.25` boundary survives; uppercase `PREF`/`HIGHRES`/`MODELINE` case handling survives; backslash-marker, two-`#` comment cut, CRLF strip, loose `monitorv2` token, 10× MAX_BYTES, bool-typed x/transform, stray `mirrorOf`, non-int mirror compare all survive.
  - **2 dead mutants** (unreachable state, byte-identical outputs demonstrated): `eff-empty-last` (add() erases same-selector rules → at most one empty-selector rule can exist, so "first empty rule" is untestable) and `vrd-order-swap` (differ>0 implies matched>0, so DIFFER-vs-NO_MATCHING_MONITOR precedence never decides). Contract observations, not fixture asks.
  - **1 equivalent-by-tolerance**: `scale-no-f32` — the "32-bit float" clause differs from float64 by ≤6e-8 relative, invisible under the 4-decimal print and 1e-4 compare (27/27 input pairs identical). Contract observation: that clause is unobservable through the tool's declared I/O.

## Missing-fixture asks (for the L1, if it wants to close gaps)
The 19 demonstrated inputs in matrix B are ready-made fixture cases (config text + dump + expected lines + rc). The two dead mutants and the f32 clause need no fixture — they need a contract note (or, for f32, a precision change) and are not implementation defects.

## Housekeeping
- Scratch `/fast/scratch/hyaku/mado-r45/MutTool/` deleted at the end (receipts copied out first). No /tmp evidence paths cited.
- No tool installs (none needed: python3 + git only; pacman untouched, host services untouched, no Wayland connection, no subagents/background jobs).
- Seat files: `MutTool.md` (this report), `MutTool/matrix.md`, `MutTool/receipts/` (ref-baseline.log, sweep-console.log, results.json, demo-evidence.json, mut-<id>.log ×54).
