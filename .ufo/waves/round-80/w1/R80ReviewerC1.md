{
  "seat": "R80ReviewerC1",
  "task": "adversarial re-derivation of C1 (round 80)",
  "verdict": "C1 SUPPORTED as measured; no falsifying finding",
  "counter_rerun": {
    "result": "cases=33 correct=33 mutants=22 killed=22 base_correct=23/33 carried=23/23 tool_selftest=111/111 verdict=TARGET_MET rc=0",
    "counter_selftest": "60/60",
    "hashes_verified": [
      "counter 6268667c…",
      "controls 17c27157…",
      "tool@6c302a5 c3eb5fbe…",
      "base tool bytes 9e274157…"
    ]
  },
  "cases_rederived": {
    "same-level-order": {
      "status": "SUPPORTED",
      "arithmetic": "order desc stable_sort quoted (S470:2686-2688); panel(10) before waybar(default) → panel y=6 (margin 6), applyExclusive 30+6=36, waybar y=36, +26 → reserved top 62; all frozen fields match incl. snapshot y=36 and attr_ns panel top:36",
      "caveat": "order().valueOrDefault() default (bar order 0) not in fetched bytes; any default ≤10 reproduces; 0 is tool convention"
    },
    "overlay-compose-top": {
      "status": "SUPPORTED",
      "arithmetic": "level-ascending exclusive pass: waybar 26 then overlay panel auto-zone 40 → 66; snapshot panel y=26 matches"
    },
    "ls-area-invalid": {
      "status": "SUPPORTED",
      "arithmetic": "waybar 26 + panel exclusive 2000 → usable {0,2026,1000,-1226}; guard quoted (ReservedArea.cpp:19-31, sha 0a52e145… = held S459/S466 bytes); decisive fork: CBox::empty() = |w|<ε ∨ |h|<ε (hyprutils Box.cpp:47-49) so the NEGATIVE-h child is NOT empty → not-contained branch → m_ok=false → ls INVALID, whole reserve zeroed",
      "empty_child_answer": "exactly-empty child takes the FIRST early return → all four sides 0 with ok() still TRUE, and because S470:2696 composes ONE CReservedArea{ORIGINAL,usable} for all surfaces it zeroes the WHOLE layer reserve (valid bar's 26 included), not only the delta; static addreserved band untouched"
    },
    "empty-box-skip": {
      "status": "SUPPORTED",
      "arithmetic": "continue quoted (S470:2655-2658, before applyExclusive and setBox): h = 774−1000 = −226 ≤ 0 → skip; zone untouched by the skipped surface → boxes MATCH,SKIP, band 26, reserved [0,26,0,0]",
      "caveat": "state is live-unreachable (S471 commit guard errors desired height 0 without both-vert anchors); case validates the guard's arithmetic on a declared state"
    },
    "full-box-vs-usable": {
      "status": "SUPPORTED",
      "arithmetic": "dock(40,bottom) then waybar(26,top) shrink usable; panel exclusive −1 skipped in exclusive pass, arranged on full_area → (800,700,200,100), applyExclusive early-returns (exclusive ≤ 0) → reserved [0,26,0,40], boxes MATCH,MATCH,MATCH"
    }
  },
  "predicate_honesty": {
    "base_ceiling": "HONEST — r79 tool has no --surfaces argument (argparse at e10f7e9) and cannot emit boxes/attr_ns/attributed which all 10 composition cases require; friendliest-invocation probe (base tool without --surfaces) still fails every composition case (anchor-unmatched passes band but fails boxes/attr_ns/attributed; same-level-order fails band 26 vs 62); counter pins base_correct==23 by equality",
    "killed_22": "single-anchor only, by construction — apply_mutation enforces source.count(anchor)==1; no multi-site mutant exists; composition still covered: 10 mutants sit in composition paths, discriminators are the new cases (e.g. level-bottom-swap killed by exactly bottom-level-first, opposite-margin-dropped by all 10); 22/22 killed=yes observed, none killed=no"
  },
  "findings": [
    {
      "sev": "minor",
      "what": "frozen counter docstring contract line says cases=30/base_correct=23/30 while code enforces and prints 33/23-of-33; stale doc in a frozen instrument, non-scoring, for the scribe"
    },
    {
      "sev": "minor",
      "what": "boundary-label divergence: tool ls_valid labels an exactly-empty composed box INVALID where source empty() branch zeroes with ok()==true (VALID); same numbers; no frozen case on the boundary"
    },
    {
      "sev": "note",
      "what": "epistemic gaps outside fetched bytes: order default, m_layerSurfaceLayers enumeration order (level-ascending corroborated by snapshots+zwlr enum), CBox::empty/containsPoint verified against hyprutils main"
    },
    {
      "sev": "note",
      "what": "S472 span metadata off-by-one (empty cases :39-52 not :40-52) already self-corrected by S477 this round"
    }
  ],
  "report_paths": [
    ".ufo/waves/round-80/w1/R80ReviewerC1/findings.md",
    ".ufo/waves/round-80/w1/R80ReviewerC1.md"
  ],
  "scratch": "removed (/fast/scratch/hyaku/mado-r80/R80ReviewerC1)",
  "bounds": "no writes outside seat dir + report path; no host mutation; read-only git show only"
}
