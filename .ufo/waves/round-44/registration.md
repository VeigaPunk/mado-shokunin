# mado round 44 — registration (frozen before any round-44 data)

Lane `mado-shokunin`, base `6a1a90528fe533cadee506a9fa3e9d13d15cc41f` (the round-43 tip plus its non-author closure commit; `jj-lane.sh state` at
round start: `local=remote=6a1a905… ahead=0 behind=0 tracked=0 untracked=0`). Host 2026-10-26: Hyprland 0.56.2-4 (`efb50993780079460b0cbed1363e2166a2de1d9f`),
gtk4 1:4.24.1-1, wayland-protocols 1.49-1. Shape: **two v1 waves** — `w1` (build + first falsifiers) and `w2` (falsify, after the data commit);
the seat counts are recorded from each wave's `*-results.json`. The §3 planner seat is held by the L1 (`MadoR44`); the planning data-walk rides a scout
seat of `w1`. No earlier attempt of round 44 exists (`.ufo/watchdog.log` has no `lane-dead-no-report mado round=44` line; launch line
`2026-10-26T13:00:54-03:00 launch mado round=44 … attempt=1`).

**Why these claims.** SCORECARD `### Planned (round 44)` item 1 (a live gkeep window) needs the operator to open gkeep — mado only reads — so it is
not claimable unattended. Item 3 (the gkeep-theme residue: `sendWindowSize`, `fetchClass`, the journal route) is C2. Item 2 (closing the round-43
predicate defects) is not a new axis-move; the routed closure defects D1-D7 are handled as frontier-step fixes and named in the report. C1 is new:
the round-43 tool reports a fullscreen or maximized gkeep window as DIFFER or TILED although Hyprland replaced the rule's box (a false report found
while reading the pinned HyprCtl.cpp for this round: `clients -j` prints `fullscreen` and the tool ignores it).

**Lowest-axis rule.** Every published axis ties at its maximum at base (`receipts/axis-base.txt`: navigation 60/60, calibration 68/68,
operability 12/12, `MADO_AXIS: checked=3 mismatched=0 rev=6a1a905…`), so each is a lowest axis. Lane axes: **operability** (C1) and **coverage** (C2).

## Claims

- **C1 — operability: `tools/mado-geometry.py` reports maximized and fullscreen clients as such.** Contract extension (the reference is
  `c1/ctl-ref-tool.py.txt`; its docstring and the counter docstring state it): fsmode = the `fullscreen` value when a JSON integer 1 or 2 (else 0);
  verdict order BADSIZE | FULLSCREEN | MAXIMIZED | TILED | AGREE | DIFFER; summary carries ` maximized=<n> fullscreen=<n>` exactly when their sum
  is > 0, otherwise the round-43 line is byte-identical. Grounding pins (`fetch-c1/`): `Hyprland-FullscreenController.hpp` (eFullscreenMode 0/1/2),
  `Hyprland-FullscreenHandler.cpp` (setTargetSizeAndPosition: monitor box / work area; rememberFloatingSize), `Hyprland-HyprCtl.cpp` (`fullscreen` =
  `.internal`). The TILED docstring sentence is narrowed (closure D3: pseudo-tiled clients).
  - **Predicate `PRED-C1-r44`**: the docstring of `quality/counters/c1-r44-geometry-states.py` (clauses a, f [26 fixtures: 12-case nonce lattice with
    fullscreen values + 14 fixed], b [selftest n >= 80], b4 [state teeth >= 75 % of >= 6 sites], g, r [the round-43 counter `PRED-C1-r42` still
    TARGET_MET on the same bytes — the no-harm clause]).
  - **Counting command:** `cd /home/vgpnk/Projects/shokunin/mado-shokunin && python3 -I quality/counters/c1-r44-geometry-states.py --repo . --rev <rev> --work <scratch>`
  - **Before** (base): `fixtures=12/26 tool=present verdict=TARGET_MISSED`, clauses `a:1 b:0 b4:0 g:1 r:1`, exit 1 (`receipts/c1-before-base.txt`;
    the lattice count varies with the nonce — 13/26 in `ctl-c1.txt` — the verdict does not).
  - **Target:** `fixtures=26/26 … verdict=TARGET_MET`, exit 0, at the data commit and at the tip. **Kill rule:** anything else at the data tip is a
    miss, reported as an honest stop; no narrowing, no re-registration after data.
- **C2 — coverage (sourced; assimilation of the gkeep-theme residue of `merge/mado/`): `corpus/knowledge/hyprland-gkeep-size-request-r44.md`** — what
  happens after the box is set: the compositor sends the size to the client (`CWindow::sendWindowSize` → `realToReportSize` → xdg `setSize` →
  `scheduleConfigure`, the pending-ack list and `onAck`; the X11 `configure` branch), what xdg-shell 1.49 lets the client do with a configure
  size, what GTK 4.24.1's Wayland toplevel does with it, and what gkeep (133b867) itself declares (`set_default_size(420, 500)`, no
  `set_size_request`). Base holds none of it: `git grep -ciE 'sendWindowSize|pendingSizeAcks|xdg_toplevel.configure|set_size_request' 6a1a905 -- corpus/knowledge PROVINCE.md SKILL.md tools`
  (recorded in `receipts/c2-ground-base.txt`). Staged predecessor: `gkeep-client-size-request-r12.md`.
  - **Predicate `PRED-C2-r44`**: the docstring of `quality/counters/c2-r44-gkeep-size-request.py` = `PRED-C2-r43-v2` with the round-44 constants
    (base, entry, lesson, fetch dir, five PINS, STAGED minus the round-43 admit) and clause h rebuilt as a client-side census (two lines recomputed
    from the pinned `gkeep-ui.py` and `Hyprland-Window.cpp`).
  - **Counting command:** `cd /home/vgpnk/Projects/shokunin/mado-shokunin && python3 -I quality/counters/c2-r44-gkeep-size-request.py --repo . --rev <rev>`
  - **Before:** `admitted=0/1 verdict=TARGET_MISSED`, exit 1 (`receipts/c2-before-base.txt`). **Target:** `admitted=1/1 verdict=TARGET_MET`, exit 0.
    **Kill rule:** as C1.
- **Separability.** C1 touches `tools/mado-geometry.py` (and its SKILL/PROVINCE rows); its counter reads only the tool and the round-42 counter. C2
  touches the entry, registry rows, the lesson `## Gate` and the README index; its counter reads no tool. Either lands without the other.

## Pre-wave fetches (`fetch/` = C2 PINS, `fetch-c1/` = C1 grounding; `receipts/fetch-sha256.txt`, 2026-10-26T13:07-03:00)

C2: `Hyprland-Window.cpp` (held row S164 holds this exact URL), `Hyprland-XDGShell.cpp` (src/protocols), `xdg-shell.xml` (wayland-protocols 1.49,
stable/xdg-shell), `gdktoplevel-wayland.c` (GTK 4.24.1, gdk/wayland), `gkeep-ui.py` (raw GitHub at 133b867, byte-identical to
`git -C ~/Projects/gkeep show 133b867:gkeep/ui.py`, sha256 `07a3c4a5…` — the full file of which held S297 is the 446-488 excerpt). Provisional
new ids S298-S301 for the four non-held documents (the lane registry tops at S297; final ids are assigned at the data commit, by document).

## Controls (committed receipts at this freeze)

- **C1:** `receipts/ctl-c1.txt` — `ctl/run-c1-controls.py`: REF (anchor) MET 26/26; do-nothing BASE-tool `fixtures=13/26` and ABSENT (`62dd798`)
  MISSED; 13 single-defect variants of the reference (no MAXIMIZED branch, fields always printed, bool as mode, TILED first, FULLSCREEN before
  BADSIZE, float as mode, any non-zero, `fullscreenClient` read, states counted as differ, swapped words, old summary, field order, new selftest
  cases removed) all MISSED; `CTL_C1 VERDICT: PASS (controls scoring TARGET_MET: 0 of 15; reference met: 1)`. K13 (selftest cases removed)
  scores fixtures 26/26 and misses only on clause b — the selftest clause is load-bearing, the fixtures alone are not.
- **C2:** `receipts/ctl-c2.txt` — `ctl/run-c2-controls.py`: base, the staged r12 file copied verbatim to the entry path (with README row and
  ADMIT/REFUSE lines), and a header-plus-correct-census shell: all `admitted=0/1`; `CTL_C2 VERDICT: PASS (controls scoring TARGET_MET: 0 of 3)`.
  No positive control exists at the freeze (round 43 inherited one from round 42); w1 builds and attacks both instruments.

## Residuals (declared)

- C1: a tool holding a model of the contract is an implementation; b4 counts sites only in functions naming `fullscreen`; the sandbox is detectable
  (round-43 cheat 6); whether a live maximized/fullscreen window reports the work-area/monitor box is the pinned source's fact, not scored.
- C2: the round-43 v2 residuals (claim-to-quote binding is the non-author reading; held S164's receipt is pinned here but held ids are not
  pin-checked by clause d); the two census lines are bookkeeping of pinned bytes, not of behaviour.
- A hole `w1` finds **before any data commit** re-registers as v2 with a new freeze; a hole found after data is an open predicate defect.

## Frontier step, assimilation, considerthese, closure items (§2b / §10 / §5)

- Assimilation theme: the gkeep residue (`gkeep-client-size-request-r12.md` admitted as predecessor; at least one of r9/r13/r14/r15 refused with
  reason and flip). Id guard (`assimilation/id-guard.md`: 0-3-space pattern fires on an indented scratch row, column-zero pattern does not;
  real collisions 42) and quarantine slice (13 rows) are in `assimilation/`; staged S311 → held S164, staged S312 → new row (by document).
- Mistake mining: the round-43 closure's routed defects D1-D7 (lesson errata, SKILL TILED licence, entry dating, registration seat count, missing
  tip axis receipt) and this round's own C1 finding (the tool shipped in round 43 reports a fullscreen window as DIFFER).
- considerthese: `considerthese/2026-10-25.md` proposal 1 ("track the domain-versus-meta ratio as a running number"), never implemented.
