# Seat RevC1Counter — Report (w1, round 44, 2026-10-26)

**Status: COMPLETE.** Scoped findings: `.ufo/waves/round-44/w1/RevC1Counter/findings.md`
(receipts `measure.out`, `measure2.out`, `probeA.out`, `probeB.out` beside it).

## Verdict on the frozen counter `quality/counters/c1-r44-geometry-states.py`

No false-pass hole found. The counter is faithful to its docstring and to PRED-C1-r42; the
model, fixtures, clauses and the no-harm regress clause all check out under measurement. Three
LOW findings (crash-path exit codes, docstring final-line format mismatch, unguarded regress
timeout) are routed as counter-defect candidates for the L1 — none can flip a TARGET_MET
verdict for a correct tool or admit a wrong one.

## Findings summary

- **LOW-1** — non-Setup I/O failures (`--work` missing dir `:343`, `--tool` missing path `:336`)
  crash with traceback, exit 1, no final line, against docstring `:48` "setup failure exit 2".
  Probes A/B reproduce both (receipts in seat dir).
- **LOW-2** — docstring `:46` puts `clauses=<...>` inside the Final line; code prints clauses on
  a separate line (`:373`) and the final line (`:374-376`) has no such token. PRED-C1-r42's
  docstring (`:85-86`) makes no such claim — the r44 docstring diverged from the inherited
  layout.
- **LOW-3** — `regress` `subprocess.run(..., timeout=1800)` (`:313-315`) is unguarded: a hung
  r42 subprocess aborts the whole counter with a traceback after ≤30 min; regress also runs
  ungated by the 3-timeout circuit breaker on an already-doomed run.
- **INFO-1** — sgen lattice: each fixture is state-blind on 60-78% of 50 sampled nonces
  (state-reach 11-21/50), but 0/50 nonces are fully blind (min 2 state clients) and 8 FIXED
  slots + edge probes carry the state contract deterministically. Predicted r43-tool pass
  distribution {11:1,12:5,13:10,14:13,15:11,16:9,17:1} contains both observed base scores
  (12/26, 13/26) — simulation validated against the frozen receipts.
- **INFO-2** — b4 quantified on the reference: 14 sites (client_fsmode:1, evaluate:8, report:5),
  need 11. Correct-tool false-negative surface is structural (logic outside `fullscreen`-naming
  functions, or <6 comparisons); wrong-tool passage is blocked by fixtures (all 13 K-variants
  missed; K13 caught by b/b4 alone). Docstring `:50-52` declares the helper-hiding residual.
- **Verified-OK** — model vs independent docstring re-derivation: 0 mismatches / 2000
  adversarial cases; monkeypatch (`old.model_out = model_out_states`, `:173`) proven NOT to leak
  into the regress subprocess (fresh `python3 -I` load of OLD_PATH judges with the ORIGINAL r43
  model); regress runs the same bytes with a derived replayable nonce (`:310-318`); fixed
  fixtures each have a distinct kill role; scratch handling matches the docstring (`:342-343`,
  `:370-371`); clause-by-clause conformance a/f/b/b4/g/r traced.

## Safety and tooling record

- Writes: only `.ufo/waves/round-44/w1/RevC1Counter/` (findings.md + 4 receipts) and this
  Report. No tracked file touched; no git/jj mutation anywhere; no pacman or package
  transaction; no tool installed (none needed); no subagents (leaf); no host-service or
  compositor mutation; no hyprctl calls at all.
- Scratch `/fast/scratch/hyaku/mado-r44/RevC1Counter/` — all receipts copied into the seat dir
  first; scratch directory deleted at seat completion (reaper-safe: nothing citable left there).
- Counter runs were probe-shaped (`--tool` on read-only files, scratch under the seat path);
  the frozen controls receipt `receipts/ctl-c1.txt` was used as ground truth for kill behavior
  instead of re-running the 15-control campaign.
