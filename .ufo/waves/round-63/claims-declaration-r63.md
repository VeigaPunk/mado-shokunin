# Round 63 claims — declared before the formal receipt runs

Base `cb442f663ca616c0825ed10beccece26bf920b35` (the r62 verifier
spot-check). Declared 2026-11-01, before the probe/tool receipt runs and
before any source row was written. Axis posture: saturation 9.0 / window
N=3, last capability r62 (gap 1 < 3), so the stagnation nudge does not
apply; every published scored sub-axis sits at its finite maximum at base
(before-state-r63.txt: navigation 77/77 = 10.0000, SOURCES 360 rows, ledger
102/102 TARGET_MET), no axis is distinctly lowest — the same posture as
rounds 56 and 58-62. The round works the open ground the r62 closure routed
in (the six drift fixes, C1) plus real axis moves on sourced coverage (C2)
and operability (C3, a capability acquisition). L1-only round again (no
dispatch surface on this host; disclosed since r57, L0 open).

- **C1 calibration** — the r62 carry-in corrections, append-only: the
  closure's six routed number-shape defects (all M62-1 class, in the round's
  own report records), each dispositioned beside its re-derivation command
  in one `## Corrections (round 63)` block in `corpus/lessons/round-62.md`
  plus the lane-owned defect-site restatements: (1) the total-range
  mislabel "34 files +1806/−1" — measured 35 files +1830/−1 for the
  receipts-tip range `4c5435d8→4fe4544`, 34 files +1806/−1 only for
  `4c5435d8→bd06d021`, 35 files +1860/−1 for the true final
  `4c5435d8→df415ef3` (the r62 SCORECARD/LOG amendment sentences print the
  bd06d021 figure while naming the final range); (2) "wave receipts +441" —
  measured 21 files +359 (receipts-only) / 23 files +466 (wave total) at
  `4fe4544`, 22 files +442 at `bd06d021`; 441 matches neither; (3) "18
  receipt files" — measured 20 at `19407ef2` (22 wave files including the
  wave-root before-state + claims-declaration); (4) "Four commits" — five
  first-parent commits in `4c5435d8..df415ef3`; (5) the census-range
  endpoint "161-170 in every committed execution" — the committed probe
  run 2 records `top_level` 160 (all-run committed range 160–170; the
  load-bearing invariants hold in every committed run), corrected in the
  entry H22 site via an appended erratum block plus the SKILL/SCORECARD
  restatements (the fleet-root report file is not lane-edited); (6) the
  declaration named S418-S422 while the landing carried S418-S423 — noted
  for the record beside the same block (no predicate changed after
  scoring). Defect bytes stay untouched (ORIGINAL_PRESERVED checks against
  base line counts).
- **C2 coverage (sourced)** — the DisplayConfig path/target plane: the
  CCD (client-side configuration) view of the live topology beside r61's
  GDI mode layer — buffer sizing + active-path query
  (`GetDisplayConfigBufferSizes` + `QueryDisplayConfig`, `QDC_ONLY_ACTIVE_PATHS`),
  the per-path target refresh rational (`DISPLAYCONFIG_PATH_TARGET_INFO.refreshRate`),
  the mode-table target vSync rational (`DISPLAYCONFIG_TARGET_MODE` →
  `DISPLAYCONFIG_VIDEO_SIGNAL_INFO.vSyncFreq`), and the documented
  DPI-virtualization non-participation — the second documented refresh
  getter the r62 D04 route named. Entry
  `corpus/knowledge/windows-displayconfig-r63.md`; source rows S424-S434,
  opened in full via fetch BEFORE any row was written (one bounded sweep;
  one enum decoded from its page after the sweep caught the remembered
  SOURCE/TARGET values in the wrong order — the M58-2 discipline working,
  recorded in the search log).
- **C3 operability (capability acquisition)** —
  `tools/mado-win-displayconfig.py`, the durable read-only DisplayConfig
  observer: selftest (assertion count fixed at authoring, red runs
  disclosed if any) exit 0; live twice with byte-identical verdict lines
  rc=0; `--from-file` re-derives from the committed snapshot; malformed
  snapshot → `MADO_WINDISPLAYCONFIG: ERROR (stage=parse …)` rc=2, raw
  bytes never echoed; crosscheck against the independently executed probe;
  no Set*/Change* verb exists in the tool; tool ledger population 102 →
  103; capability row enters the SCORECARD table the same round.

All three claims are causally separable: C1 verifies on the r62 lesson and
the numstat/counter re-derivations alone; C2 verifies on the new entry, the
registry rows and the counters alone; C3 verifies on the tool's own runs
alone. No claimed improvement touches another claim's evidence.
