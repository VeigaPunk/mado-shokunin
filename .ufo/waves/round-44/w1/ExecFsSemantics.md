# ExecFsSemantics — C1 fullscreen/maximized semantics grounding (round 44, w1)

Status: **complete**. Seat dir `.ufo/waves/round-44/w1/ExecFsSemantics/`. No frozen file was edited
(`registration.md`, `quality/counters/*`, `ctl/*`, `c1/ctl-ref-tool.py.txt`, pins are untouched); writes are
this report, `finding.md`, `quotes.tsv`, `verify-quotes.py`, `pins/*`, `receipts/*` inside the seat dir.

## Deliverable

`finding.md` — answers the five questions with ≤25-word quotes, each located by a computed `grep -n` and
byte-checked. `verify-quotes.py` output: `QUOTES: rows=81 fails=0 uncovered=0` (exit 0); it re-reads every
pin, asserts the needle is on the stated line, asserts the needle is present in `receipts/greps.txt`, and
caps quotes at 25 words. Pins: 28 files at `efb50993780079460b0cbed1363e2166a2de1d9f` (sha256 in
`pins/SHA256SUMS.txt`, URL/path map in `pins/SOURCES.md`); frozen inputs re-hashed in
`receipts/frozen-inputs-sha256.txt` (they match the round-44 `receipts/fetch-sha256.txt` values for the three
`fetch-c1` files).

## Verdict

The C1 premise is **supported**: when `clients -j` reports `fullscreen` 1 or 2, the reported `size`/`at` are
layout/monitor quantities, never the rule's box, so FULLSCREEN/MAXIMIZED must precede TILED and AGREE/DIFFER.

1. **`.internal` is only 0/1/2.** `enum eFullscreenMode : int8_t` with three enumerators
   (`fetch-c1/Hyprland-FullscreenController.hpp:12-15`); every raw-int ingress is clamped to [0,2]
   (`FullscreenController.cpp:294`, `ConfigActions.cpp:294-295` for `dispatch fullscreenstate` and the
   `fullscreenstate` rule), all map stores are enum values (`FullscreenHandler.cpp:135-139`), and HyprCtl
   prints `sc<uint8_t>(… .internal)` (`HyprCtl.cpp:431`, `:451`) — a JSON integer, never bool/float, never 3/-1.
2. **Yes, the goal box is replaced.** fullscreen: `MONITOR->logicalBox()` → `setPositionGlobal(MONBOX)`
   (`FullscreenHandler.cpp:192,194`) → `setBox(m_box.logicalBox)` (`WindowTarget.cpp:94`); maximized:
   `workArea(target->floating())` → `setPositionGlobal(WORKAREA)` (`:196,198`) → `setBox(visualBox − reserved)`
   (`WindowTarget.cpp:105`). `setBox` writes `*m_realSize` (`GeometricMovableAnimated.cpp:45`) which sets
   `m_Goal` (`hyprutils 0.14.2 AnimatedVariable.hpp:244`), and `clients -j` prints `size(GEOMETRIC_GOAL)`
   (`HyprCtl.cpp:427-428`). Reported synchronously; no animation lag.
3. **Floating survives fullscreen.** No FS path writes `m_isFloating` (writers: `WindowTarget.cpp:291` via
   `setFloating`, `Window.cpp:2130`, `:2191`; `Group.cpp:133` copies the group's own value). The non-FS
   floating branch guards on `isFullscreen` instead of clearing the flag (`WindowTarget.cpp:70`). Hence round
   43 says DIFFER for a floating fullscreen client (the false report) and TILED for a *tiled* one — which is
   why the new order is necessary.
4. **On exit the size is restored, the position is not.** Enter: `rememberFloatingSize(target->position().size())`
   (`FullscreenHandler.cpp:130-131`, floating only, while the box is still the rule's). Exit: box untouched by
   the handler (`:182`); floating windows are re-centred from the remembered size
   (`FullscreenController.cpp:478,480` → `FloatingAlgorithm.cpp:21,26`). Tiled windows return to the layout;
   `newTarget` (`LayoutManager.cpp:19`) re-reads the `size` rule only on target add.
5. **No state with internal 1/2 and the rule's box** (table in `finding.md` §5: floating FS/max, tiled
   non-scrolling, scrolling, group, hidden workspace, work-area change, unmapped/no-monitor). Two honest
   divergences, neither breaking C1: (a) the **scrolling layout** handler's `setTargetSizeAndPosition` is an
   empty body (`ScrollingFullscreenHandler.cpp:301-303`, `:307`) — its box is the column geometry
   (`:197` fullscreen width = monitor/usable ratio, `:232` maximize width 1.F), not the monitor box/work area;
   (b) a *non-current* group member carries the group box with internal 0
   (`FullscreenHandler.cpp:41-44`, `WindowGroupTarget.cpp:34`) — the opposite asymmetry.

## Correction routed to the L1 (documentation only, no gate impact)

The mechanism sentence in `registration.md` (C1 "Why") and in the reference docstring — "a maximized window's
box to the work area and a fullscreen window's box to the monitor box" — is exact for the default handler and
**imprecise for `layout:scrolling`**, where the box comes from the scrolling column. No `PRED-C1-r44` clause
scores prose (clauses a/b/b4/f/g/r are behavioural), so the verdicts the counter measures are unaffected. If
the sentence is ever re-frozen, the accurate form is "the default handler sets the monitor box (2) or the work
area (1); the scrolling handler sizes a column (monitor-wide for 2, usable width for 1); in both the reported
size is a layout quantity, not the rule's".

## Evidence retained (seat-local)

- `finding.md` (the grounded answers), `quotes.tsv` (81 rows: pin path, line, needle), `verify-quotes.py`
  (exit 0), `receipts/greps.txt` (every computed locator, incl. negative greps `grep -c isHidden` = 0 for both
  box-setting files), `receipts/host-read.txt` (`hyprctl version` = v0.56.2 @ `efb50993…`; clients census;
  monitor 3440x1440 reserved [0,26,0,0]), `pins/SHA256SUMS.txt`, `pins/SOURCES.md`.

## Risks / limits (no blocker)

- **Not behaviour-verified on the host.** At reading time no live client had `fullscreen` 1 or 2
  (`receipts/host-read.txt`: three mapped clients, all `0 0`), and this seat may not dispatch or open a
  Wayland client. The live box therefore remains C1's declared residual; the ground is source, not observation.
- `m_Goal = v` is read from the installed hyprutils 0.14.2 header (the pinned commit only requires ≥0.14.0,
  `CMakeLists.txt:150`); if the host's 0.14.2 semantics differed the goal chain would need a re-pin.
- The pin set covers the files this question needed plus the repo tree listing; writers of `m_isFloating` or of
  a FS-handler map outside it (e.g. `hyprpm` plugins calling the public controller) are not excluded by
  exhaustiveness — only by the files read.
- No tool was installed or upgraded (no `pacman`, no `uv`, no binaries); scratch under
  `/fast/scratch/hyaku/mado-r44/ExecFsSemantics` was created, left empty and removed (`rm -rf`); host reads were
  `hyprctl version`, `hyprctl clients -j`, `hyprctl monitors -j` only — no dispatch, no client connection.
- Not my scope and not done: scoring `tools/mado-geometry.py` or the reference with `PRED-C1-r44`, and any edit
  to frozen counters/controls/registration (L1 is the integrator).

## Checks the parent should run after integration

`python3 -I .ufo/waves/round-44/w1/ExecFsSemantics/verify-quotes.py` (expect `fails=0`), and, if the L1 edits
the mechanism sentence, re-freeze so the docstring and `registration.md` agree with `finding.md` §5.
