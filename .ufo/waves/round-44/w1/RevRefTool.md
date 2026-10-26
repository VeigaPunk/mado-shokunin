# Seat RevRefTool — C1 reference review (w1, round 44) — DONE

Target: diff of base `tools/mado-geometry.py` @ `6a1a9052…cc41f` vs `.ufo/waves/round-44/c1/ctl-ref-tool.py.txt`;
docstring-vs-pin truth; robustness; round-43 caller harm.

**Verdict: no blocking defect. Recommend the reference unchanged as the C1 instrument.**

Key evidence (full detail + locators in `.ufo/waves/round-44/w1/RevRefTool/findings.md`):
- Frozen counter on the reference: exit 0, `fixtures=26/26 clauses=a:1 b:1 b4:1 g:1 r:1
  verdict=TARGET_MET`; clause b selftest 91/91; clause b4 14/14 mutants killed (need 11);
  clause r `PRED-C1-r42: 37/37 TARGET_MET` — no round-43 harm (`counter-r44-ref.txt`).
- Pin support computed and quoted with grep -n locators: monitor box (FullscreenHandler.cpp:191-194),
  work area (:195-198), rememberFloatingSize (:130-131 inside setTargetFullscreenModeInternal :123),
  enum 0/1/2 (FullscreenController.hpp:12-15), `fullscreen` = `.internal` (HyprCtl.cpp:410, :431).
  Computed pin sha256s equal `receipts/fetch-sha256.txt:7-9`.
- Behavior probes (outputs in seat `probes/`): stateless stdout byte-identical to base (diff rc 0);
  state dump → `maximized=1 fullscreen=1 … verdict=OK` rc 0 stderr 0 with FULLSCREEN/MAXIMIZED client
  lines; nested `{"internal":2}` and `10**30` correctly fsmode 0; injection class JSON-escaped,
  newline class unmatched; >1 MiB → `SETUP too_large` rc 2 (one stdout line); 8300-client 1.02 MiB
  dump in 0.082 s (base 0.074 s, false `differ=8300` becomes `fullscreen=8300`); live
  `hyprctl clients -j` run reproduces the round-43 NO_MATCHING_CLIENT line byte-valid (rc 3).

Findings (by severity):
- F1 LOW — docstring "takes its size from its stored pseudo size": store sites pinned
  (Window.cpp:2394-2414) and dump pseudo-field absence pinned (0 hits in HyprCtl.cpp), but the
  apply site is in no pinned file (grep -i `pseudo` over the pins). Operative claim (TILED = not
  floating only; no pseudo field) is pinned and true. Pins are frozen; note for any v2.
- F2 LOW (inherited, absurd input) — a valid-JSON doc with a >4300-digit int is refused
  `SETUP bad_json` (CPython int-digit limit inside json.loads); `parse_clients` unchanged from
  base; clean rc 2, unreachable from real hyprctl output.
- F3 INFO (integration, not the reference) — SKILL.md :158/:225/:248-301/:287-290 still carry the
  round-43 verdict set; they stay true for stateless dumps, but C1's data commit must extend the
  SKILL/PROVINCE rows with FULLSCREEN/MAXIMIZED (registration already assigns those rows to C1).
- F4 INFO — residuals honestly declared (work-area/monitor-box is pinned-source fact, not
  runtime-scored; b4 names-only mitigated by 14/14 kills, state logic all in named functions).

Round-43 caller sweep: lane-wide `MADO_GEOMETRY:` grep — only the tool, frozen byte-exact
instruments (clause r proves r42 unharmed), historical `.ufo` evidence, and SKILL/PROVINCE quote
rows (stateless, byte-identical). No lane script parses the summary line. Nothing breaks.

Scratch `/fast/scratch/hyaku/mado-r44/RevRefTool/` deleted; all receipts copied to the seat dir.
No tools installed. Only allowed compositor reads used (`hyprctl clients -j`, once, piped to the
tool under `timeout 5`).

Report: .ufo/waves/round-44/w1/RevRefTool.md
