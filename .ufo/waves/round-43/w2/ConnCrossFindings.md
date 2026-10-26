# ConnCrossFindings — report (w2, round 43, 2026-10-26)

Seat: cross-read of all 38 w1 reports (`.ufo/waves/round-43/w1/*.md` + the six findings files they point to)
against the landed data commit `1959770657f1f8665097c1aed4be6c1cbb07139f`. Deliverable:
`.ufo/waves/round-43/w2/ConnCrossFindings/matrix.md` (finding | seat | severity | status | pointer); evidence:
`.ufo/waves/round-43/w2/ConnCrossFindings/probes-c2-leftovers.txt`.

## Anchors verified at 1959770

- `tools/mado-geometry.py` sha256 `e3c2e471505932f797a98ee2aa9ab1b04fc919f2140509282ef8472498135a99` — byte-identical
  to the round-42 reference `.ufo/waves/round-42/c1/ctl-ref-tool.py.txt` (also pinned in
  `receipts/live-geometry-host.txt`). Therefore every w1 finding about the tool (SentReDoS SR-1..7, RevRefTool
  V1-V8, MutRefSelftest, ExecC1ExtraMutants N48/N51, CritContract, ScoutSizeGrammar, CritC1Cheat) still holds at
  the data commit without re-measurement.
- C1 counter at 1959770 = freeze bytes `ed78d693…`; C2-v2 counter at 1959770 = freeze blob `9a834070…` (identical
  at 496340d and 1959770). L1 receipts `c1-after-data.txt` (37/37 MET) and `c2-after-data.txt` (v2 1/1 MET)
  present and consistent.
- `quality/check-locators.py` sha256 `c1ea52ad…` = the ExecLocatorGate deliverable (landed as-is).

## Status summary

- C1 side: tool byte-identical to reference and counter unchanged ⇒ all C1-tool/counter findings still hold.
  DECLARED: CritC1Cheat cheats 4 and 6 and CritClaimSizing C1 F1 (registration-v2.md); cheat 1, clause-g
  heuristic, sandbox-detectable, re≠RE2 value agreement (registration.md residuals). Everything else (including
  the ReDoS/liveness class, deep-JSON crash, broken pipe, fixture vacuity, timeout-breaker load-sensitivity,
  contract-vs-compositor grammar F1-F8) is OPEN at the data commit.
- C2 side: v2 (496340d) fixed the seven mechanical CritC2Cheat families (B1/C1/C2/E1/F1/F2/X2/X3), the G1/G2
  location-cell tradeoff (e+ true URLs), and enumerated the chain (i+ all-ten-PINS-cited — negative probe
  confirms X3 is now rejected). DECLARED residuals: A1/A2/D1/E2/H1/X1 (claim-to-quote binding), RevC2Counter F1
  (held-id receipt — the landing avoids it by pinning held S155/S158 gate receipts), ExecC2ExtraMutants F1
  (byte-identical GATE outside section) and F3 (two-digit ids).
- Still OPEN at 1959770, shown by probes run at the data commit (scratch clone + one mutation per fixture commit,
  counter `--rev HEAD`): RevC2Counter **F3** (`:10x` garbage suffix → admitted), **F5** (`recheck: 90d whatever
  junk` → admitted; `recheck_ok("90d and-never-recheck")=True`), **F6** (quote embedded mid-word → admitted),
  **F7** (`archive/deep/…` path-prefixed locator → admitted), **F8** (`elsewhere/host-gkeep.conf.bak` row
  location → admitted), and **F2 bypass 2** (fenced decoy GATE → admitted). The F4 junction-space off-by-one
  mechanism is unchanged (`quote_at` returns line 3 for words on line 4, unit probe).
- Prose findings: CritClaimSizing F4 (lowest-axis sentence still not enumerated) and F5 (separability greps
  unnamed) remain OPEN; F6 (seat count) FIXED in the lesson (38 seats). M43-1..8 all routed: the locator
  checker, live receipt, excerpt regeneration, criteria 77-81, and the v2 freeze cover them.

## Non-reporting rule

No w1 finding is re-reported as a new defect; the matrix shows each one's status at 1959770, with the pointer
where it was fixed or declared. Findings that still hold are backed by the byte-identity of the reviewed artifact
(C1) or by the probe receipts (C2).

## Tooling / safety

No tools installed; no pacman; no lane/fleet git mutation; no compositor verb. Scratch
`/fast/scratch/hyaku/mado-r43/ConnCrossFindings/` removed at seat end; nothing citable lives there.
