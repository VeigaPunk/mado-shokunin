# ConnCrossClaim — round 44 w1 status

Seat: ConnCrossClaim (leaf, cross-claim patterns C1×C2; separability). Done.

Deliverable: `.ufo/waves/round-44/w1/ConnCrossClaim/cross.md` (claims-vs-sources
matrix + the four required findings). Evidence receipts in the same dir:
`cross-c1-ref-run.txt`, `cross-c2-base-run.txt`, `cross-separability-grep.txt`.

## Findings (all grounded; pin line numbers computed by grep -n)

1. **Shared fact (Q1): the compositor's goal box.** C1's tool joins the rule
   against `clients -j` `size`, which HyprCtl.cpp:427-428 prints as
   `w->size(GEOMETRIC_GOAL)`; C2's chain transmits the same box —
   `sendWindowSize` reports `realToReportSize()` = `m_realSize->goal()` for xdg
   (Window.cpp:1741, 1685-1687). Consistent both ways; both reads are the
   monitor/work-area box when the internal mode rewrites the goal
   (FullscreenHandler.cpp:192-198). Numeric echo: the C1 fixture rule 420×500
   (c1-r44-geometry-states.py:179) equals gkeep's `set_default_size(420, 500)`
   (gkeep-ui.py:476). Boundary: the `GEOMETRIC_GOAL` accessor itself is not in
   the pinned bytes ([INFERENCE]); X11 reporting diverges (clamp {1,1},
   force_zero_scaling) but gkeep is xdg.
2. **Contradiction (Q2): none hard.** Three near-misses stated in cross.md §3:
   (a) C1 synthetic fixture `fsagree0` vs pinned live-box behavior — disjoint
   scopes, registration residual says the live fact is not scored; (b)
   xdg-shell 1.49 calls the configure size "a hint" (:1150) and reserves 0×0
   for the client, while Hyprland's sendWindowSize never emits 0×0 — spec
   permits, compositor does differently; risk is wording, not fact; (c) X11
   clamp divergence, unreachable for gkeep. All six Hyprland pins share commit
   efb5099 — no version skew.
3. **Cross-need (Q3): neither direction.** C1's FULLSCREEN verdict needs only
   fetch-c1 (enum :12-15, `.internal` print HyprCtl.cpp:431, box-setting
   FullscreenHandler.cpp:192-198, remember :131). C2's gate-checked sentences
   bind only to the five fetch/ pins; the counter enforces this — a GATE citing
   fetch-c1 fails pin_ok (c2-r44:495-499, PINS :167-173).
4. **Separability (Q4): shown.** Grep: C1 counter's only knowledge/fetch hits
   are docstring prose (line 14); runtime it opens only the tool bytes
   (:336/:351), as does the imported c1-r42 (:963/:965). C2 counter has zero
   references to mado-geometry/tools (grep exit 1); its only subprocess is git
   (:194). One run each: C1 reference tool → 26/26 TARGET_MET, clauses a:1 b:1
   b4:1 g:1 r:1, exit 0, r42 regression 37/37; C2 on base → admitted=0/1
   TARGET_MISSED, exit 1. Either lands without the other.

## Connector move (bounded, in cross.md §6)

The C2 entry's riskiest sentence is spec-generalizing the shared fact: bind
client-behavior claims to the GTK pin (gdktoplevel-wayland.c:606-706) and keep
the xdg-shell pin for permission/obligation only (must ack_configure; size is a
hint). Saves the w2 admission from a "hint"-quote falsifier; no counter edit.

## Tool state / safety

No installs needed (python3 stdlib only). No writes outside the seat dir and
this report; counters/controls/registration/pins/reference untouched; no
mutating git/jj. Scratch dir /fast/scratch/hyaku/mado-r44/ConnCrossClaim
contained only counter --work tempdirs (auto-removed by the counters) and the
run receipt, copied into the seat dir first; scratch deleted on exit.

Checks for main agent: none required — the two counter runs above are the only
verification and both receipts are committed in the seat dir.

Report: .ufo/waves/round-44/w1/ConnCrossClaim/cross.md
