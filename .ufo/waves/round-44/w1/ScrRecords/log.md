# Draft — LOG.md Round 44 entry (append after the Round 43 entry; `<<L1>>` = value only the L1 can fill)

## Round 44, attempt 1 - state verdicts in the rule-size join and the gkeep size-request entry (2026-10-26)

- Freeze `e2289516a9a857f55cda7be635933e89b931c3da` (registration `.ufo/waves/round-44/registration.md`, base
  `6a1a90528fe533cadee506a9fa3e9d13d15cc41f`; `jj-lane.sh state` at round start `local=remote=6a1a905… ahead=0 behind=0
  tracked=0 untracked=0`): C1 re-registers the round-43 join with state verdicts under the new counter
  `quality/counters/c1-r44-geometry-states.py` (`PRED-C1-r44`, clause r keeps the round-43 counter
  `c1-r42-geometry.py` TARGET_MET on the same bytes as the no-harm clause); C2 registers the entry
  `corpus/knowledge/hyprland-gkeep-size-request-r44.md` under `quality/counters/c2-r44-gkeep-size-request.py`
  (`PRED-C2-r44` = `PRED-C2-r43-v2` with round-44 constants and clause h rebuilt as a client-side census). Frozen with
  the counters: the reference `c1/ctl-ref-tool.py.txt` (26/26; selftest `91/91`,
  `.ufo/waves/round-44/w1/ScrRecords/ref-selftest.txt` = `MADO_GEOMETRY_SELFTEST: 91/91 passed`), the two control drivers and the
  pre-wave receipts (`receipts/freeze-counter-check.txt`: all six files `present`).
- Pre-wave pins (`receipts/fetch-sha256.txt`, 2026-10-26T13:07:51-03:00; host Hyprland 0.56.2-4 / gtk4 1:4.24.1-1 /
  wayland-protocols 1.49-1): `fetch/` = C2 - `Hyprland-Window.cpp` (held row S164's own URL,
  `raw.githubusercontent.com/hyprwm/Hyprland/efb50993780079460b0cbed1363e2166a2de1d9f/src/desktop/view/Window.cpp`),
  `Hyprland-XDGShell.cpp` (same commit, `src/protocols`), `xdg-shell.xml` (1.49, `stable/xdg-shell`),
  `gdktoplevel-wayland.c` (GTK 4.24.1, `gdk/wayland`), `gkeep-ui.py` (133b867; byte-identical to
  `git -C ~/Projects/gkeep show 133b867:gkeep/ui.py`, sha256 `07a3c4a5…`, the full file of which held S297 is the 446-488
  excerpt); `fetch-c1/` = C1 ground - `Hyprland-FullscreenController.hpp`, `Hyprland-FullscreenHandler.cpp`,
  `Hyprland-HyprCtl.cpp` (same commit).
- The C1 ground, recomputed this round with `grep -n` on the `fetch-c1/` pins: `eFullscreenMode` is
  `FSMODE_NONE = 0, FSMODE_MAXIMIZED, FSMODE_FULLSCREEN` (`Hyprland-FullscreenController.hpp:12-15`), so the JSON integer
  2 means fullscreen and 1 maximized; `setTargetSizeAndPosition` returns early for `FSMODE_NONE` and otherwise sets the
  layout target to the monitor box (`Hyprland-FullscreenHandler.cpp:192,194`) or the work area
  (`:196,198`); `hyprctl clients -j` prints that mode as the `fullscreen` key (`Hyprland-HyprCtl.cpp:410`) from
  `getFullscreenModes(w).internal` (`:431`). The round-43 tool ignores the key, so a fullscreen gkeep window (monitor
  box vs. the rule's 420x500) is reported DIFFER - the false report C1 removes; the TILED sentence is narrowed to
  pseudo-tiled clients (closure D3).
- Controls at the freeze: `receipts/ctl-c1.txt` - `CTL_C1: rev=6a1a905… controls=15`, REF 26/26 MET, and 0 of 15
  non-reference runs TARGET_MET (do-nothing `fixtures=13/26`, ABSENT, 13 single-defect variants); K13 (selftest cases
  removed) scores `fixtures=26/26` and misses only clause b, which is what makes the selftest clause load-bearing.
  `receipts/ctl-c2.txt` - `CTL_C2: base=6a1a905… controls=3`: base, the staged `gkeep-client-size-request-r12.md` copied
  verbatim to the entry path, and a header-plus-correct-census shell are all `admitted=0/1`; **no positive control
  exists at the freeze** (round 43 inherited one from round 42) - w1 builds and attacks both instruments
  (`w1/<<L1>>`).
- Before-measurements at base `6a1a905`: C1 `fixtures=12/26 tool=present verdict=TARGET_MISSED`, clauses
  `a:1 b:0 b4:0 g:1 r:1`, exit 1 (`receipts/c1-before-base.txt`; the 12-case nonce lattice makes the fixture count move -
  13/26 in `receipts/ctl-c1.txt` - while the verdict does not); C2 `admitted=0/1 verdict=TARGET_MISSED`, clauses
  `a:0 … i:0`, exit 1 (`receipts/c2-before-base.txt`); ground at base `git grep -ciE
  'sendWindowSize|pendingSizeAcks|xdg_toplevel.configure|set_size_request' 6a1a905 -- corpus/knowledge PROVINCE.md
  SKILL.md tools` exit 1 (`receipts/c2-ground-base.txt`); census start `<<L1>>` (`receipts/census-before.txt`); the axis
  table ties at its maximum (`receipts/axis-base.txt`, `MADO_AXIS: checked=3 mismatched=0`).
- Wave `w1` spec/dispatch `<<L1>>`: 38 seats (build + first falsifiers; discipline split `<<L1>>`, per the dispatch). Findings that changed
  the round before any data: `<<L1>>` (the C2 positive control, `w1/ExecC2Positive`; the C1 falsifiers, `w1/<<L1>>`);
  re-registration, if any, is `<<L1>> - none expected: both registrations stand as frozen`.
- Data commit `<<L1>>`: `tools/mado-geometry.py` (state verdicts; summary ` maximized=<n> fullscreen=<n>` exactly when
  their sum > 0, round-43 line byte-identical otherwise); `corpus/knowledge/hyprland-gkeep-size-request-r44.md` (the
  chain `CWindow::sendWindowSize` -> `realToReportSize` -> xdg toplevel `setSize` -> `scheduleConfigure`, the pending-ack
  list and `onAck`, the X11 configure branch, what xdg-shell 1.49 permits, what GTK 4.24.1's Wayland toplevel does,
  and gkeep 133b867's `set_default_size(420, 500)` with no `set_size_request`; the pinned landing sites, recomputed with
  `grep -n`: `fetch/Hyprland-Window.cpp:1732` `sendWindowSize`, `:1685` `realToReportSize`, `:1753`
  `m_pendingSizeAcks.emplace_back(… setSize(REPORTSIZE) …)`, `:1514-1521` `onAck`, `:1547,1573`
  `m_xwaylandSurface->configure(box)`; `fetch/Hyprland-XDGShell.cpp:354-357` `setSize` -> `scheduleConfigure`, `:629`;
  `fetch/gkeep-ui.py:476` `window.set_default_size(420, 500)`; registry rows S298-S301 (append-only, 11 columns, status
  `mined`, opened 2026-10-26); `corpus/lessons/round-44.md`; README index row and Frontier bullet;
  PROVINCE.md, SKILL.md rows; QUALITY `<<L1>>`. Measured there: C1 `fixtures=26/26 tool=present verdict=TARGET_MET` exit 0
  (`receipts/<<L1>>`); C2 `admitted=1/1 verdict=TARGET_MET` exit 0 (`receipts/<<L1>>`); census `<<L1>>` exit 0.
- Round-43 closure defects (fix-forward; the Round 43 text is left as written where routed as supersession): D1 lesson
  reason under-cites S294/S158 and S310 maps to S295/S296/S297 - `<<L1>>`; D2 S293 title echoes the refuted premise -
  superseded with the other w2 row-cell defects `<<L1>>`; D3 SKILL.md TILED licence wrong for pseudo-tiled clients -
  corrected in the C1 change `<<L1>>`; D4 the entry cites `w1/ExecOracleGkeep` files absent at the data commit, and its
  receipt cites `gkeep-shm.c:156-164` (true 150-159) - `<<L1>>`; D5 SCORECARD says M43-1..8 while the lesson carries M43-9, and
  registration says 37 `w1` seats while 38 ran - the SCORECARD erratum line lands with this round's section; D6 open
  predicate defects re-registered as this round's counters `<<L1>>`; D7 tip axis receipt committed at `<<L1>>`.
- Wave `w2` `<<L1>>` seats dispatched after w1's WAVE-DONE (w1: `<<L1>>` of 38 reported, `<<L1>>` dead). Its
  falsifications and the post-data corrections `<<L1>>`; open predicate defects it reports (no re-registration after
  data) `<<L1>>`; the C1 and C2 counters' verdicts on the corrected bytes `<<L1>>`.
- Tip receipts at `<<L1>>`: C1 `fixtures=26/26 … TARGET_MET` (`receipts/<<L1>>`), C2 `admitted=1/1 … TARGET_MET`
  (`receipts/<<L1>>`), census `<<L1>>`, axis `MADO_AXIS checked=3 mismatched=0` (`receipts/<<L1>>`).
