# CritEntryInf — INF/UNK attack on the gkeep-geometry entry (round 43, w2)

Seat `CritEntryInf`, round 43 wave `w2`, 2026-10-26. Lane repo `/home/vgpnk/Projects/shokunin/mado-shokunin`.
Target: `corpus/knowledge/hyprland-gkeep-geometry-r43.md` at data commit
`1959770657f1f8665097c1aed4be6c1cbb07139f` (base `a35cfdfcdeb3bd42d1a2cd960faf22ceac1bef3f`), attacked against the
**whole** Hyprland tree at `efb50993780079460b0cbed1363e2166a2de1d9f` (v0.56.2), not the seven pinned excerpts.
Deliverable: `.ufo/waves/round-43/w2/CritEntryInf/findings.md` (48 located quotes, `verify-quotes.py` → `VERIFY: PASS`).

## Verdicts per INF/UNK line

| entry line | claim | verdict |
|---|---|---|
| 36 | FullMatch makes `^`/`$` redundant; dots match any character | **SUPPORTED** (one word to tighten: RE2 `.` excludes newline) |
| 48 | "A tiled window never takes this branch: the size rule only acts through the floating algorithm … inert" | **FALSIFIED** |
| 56 | `clients -j` `size` is the GOAL; current differs during the open animation; no read verb exposes current | **SUPPORTED** at source (host-scope caveat: animations on) |
| 62 | two agreeing numbers are not one observation | **SUPPORTED** (no upstream counterexample) |
| 68 | UNK: no gkeep window seen on this host | **SUPPORTED** (census pin: 4 clients, 0 floating, 0 gkeep) |
| 79 | "the size rule is evaluated on first map only" | **FALSIFIED** in the once-per-window sense |

## F1 — a tiled window does read `static_.size` (entry:48)

Two read sites exist in the tree, not one (`receipts/grep-static-size-src.txt`): the floating algorithm
(`DefaultFloatingAlgorithm.cpp:55-56`, which the entry quotes) and the **tiled** branch of `mapWindow`:

- `Window.cpp:2402` `if (m_ruleApplicator->static_.size) {` → `:2403` evaluates it → `:2408`
  `m_target->setPseudoSize(*COMPUTED);`
- the pseudo flag comes from the same rule set at map (`Window.cpp:2192`), static rules are read at `:2277`;
- the pseudo size replaces the tiler's box when the target is pseudo (`WindowTarget.cpp:145`, `:197`, `:215`) and
  lands in the animated size the IPC reads (`setBox` → `GeometricMovableAnimated.cpp:45`).

Counterexample: a `size` rule plus `pseudo` (or a later `togglepseudo`) on a **non-floating** window gives a
`clients -j` client with `floating: false` and `size` = the rule's `420 500` — the rule decided the box. So
"only acts through the floating algorithm" and "inert" are false. What survives: with neither `float on` nor
`pseudo`, the tiler decides the box, so the host's gkeep chain (host sets `float on`) is unaffected.

Impact: `clients -j` has no pseudo field (29 fields, `HyprCtl.cpp:395-423`), and the C1 reference emits TILED from
`floating` alone (`tools/mado-geometry.py:210-211`), repeating the same premise in its docstring (`:6`
"a tiled window never reads it."). A pseudo-tiled window whose box is the rule's size is therefore reported TILED —
an open defect of `PRED-C1-r42`'s model text. The 37 scored fixtures (none pseudo) and the live
`NO_MATCHING_CLIENT` receipt are unaffected, so C1's TARGET_MET stands.

Smallest safe correction (entry §2 INF at line 48): state that a tiled window never reaches the floating algorithm's
branch **but the rule is still read** for it — `mapWindow` stores its evaluation as the target's pseudo size, which
decides the box when the target is pseudo-tiled; without `float on` and without `pseudo` the tiler decides the box,
and the value is the window's pseudo size rather than inert. Do not edit the frozen tool; route the TILED/pseudo
residual to the L1. (This does not re-admit the refused staged r10: that made the rule a pseudo-size request for the
client; this is the compositor-side pseudo size of a tiled target.)

## F2 — "first map only" is not once per window (entry:79)

`m_firstMap` is armed inside `mapWindow` (`:2079`) and cleared at its end (`:2513`); `mapWindow` is the listener body
for every surface map (`:183`), and upstream expects remaps (`:760` "(In case a window got remapped)"). `unmapWindow`
keeps the `CWindow` and only clears `m_isMapped` (`:2644`); the next map re-runs `:2383` `newTarget`, which reaches
the guarded floating branch again through `Target.cpp:21`, `Space.cpp:45`, `Algorithm.cpp:35`, and
`DefaultFloatingAlgorithm.cpp:49`. Static rules are re-read at each map too (`Window.cpp:2277-2278`).

Counterexample: a floating gkeep the user resized, then unmapped and remapped (GTK hide/show) returns to the rule's
420x500. The tiled pseudo-size read at `Window.cpp:2402` is not `m_firstMap`-guarded at all and runs on every map.

What remains true: while mapped, a user resize, a monitor change or a rule reload does not re-evaluate the size
expression (reload re-applies dynamic effects only, `Engine.cpp:40`; float/tile toggles go through `movedTarget`,
`Algorithm.cpp:70`). Smallest correction: replace "evaluated on first map only" with "read at every map event
(`m_firstMap` is re-armed in `mapWindow`), plus the unguarded pseudo-size read for tiled windows".

## Supported lines (evidence in findings.md)

- entry:36 — `FullMatch` is whole-text (`RegexMatchEngine.cpp:16`), built with default options (`:12`); tested with
  the same RE2 library (`receipts/re2-anchors.txt`): 12 candidates, anchored vs bare pattern identical under both
  `one_line` settings. One over-generalisation: `.` does not match newline. Bonus decoy confirmed:
  `org-omarchy-gkeep` also matches.
- entry:56 — IPC uses GOAL (`HyprCtl.cpp:427-428`), accessors split at `GeometricMovableAnimated.cpp:19-20`, the
  renderer draws CURRENT (`Renderer.cpp:566`), popin separates from/goal (`WindowAnimationController.cpp:39,43,190,194`),
  and no `GEOMETRIC_CURRENT` appears anywhere in `src/debug/` (`receipts/grep-geometric-current-hyprctl.txt`). Caveat:
  with animations off, `AnimationManager.cpp:44` warps and the two coincide; the host's animations-on receipt is w1's
  S309, not re-measured here.
- entry:62 / entry:68 — no upstream counterexample; census pin exact.

## Impacted axes

- **coverage (C2)**: the entry's chain misstates who reads the stored size and when; the counter is structural and
  still `admitted=1/1`, so the target stands and the defect is in the claim text (the declared claim-binding residual).
- **operability (C1)**: TILED's stated rationale is false and pseudo-tiled windows are a false-negative class the tool
  cannot see from `clients -j`. No scored fixture or host receipt is wrong; reported as an open defect of
  `PRED-C1-r42` (no re-registration after data).

Neither finding kills or re-registers a claim; both are for the L1 to route.

## Receipts, tooling, hygiene

- `w2/CritEntryInf/findings.md`, `verify-quotes.py`, `verify-quotes.txt` (`quotes=48 fails=0`, 16 pins, 7 round-43
  fetch pins re-checked byte-identically), `pins/` (16 whole files + `SHA256SUMS`), `receipts/` (clone identity,
  RE2 test and its script, three grep receipts).
- Method: `git clone --filter=blob:none https://github.com/hyprwm/Hyprland`, `fetch --depth 1 origin efb5099…`,
  `checkout FETCH_HEAD`; rev and the seven-file byte comparison in `receipts/clone-identity.txt`.
- Tooling: `google-re2==1.1.20251105` via `uv pip` into a scratch venv under
  `/fast/scratch/hyaku/mado-r43/CritEntryInf/venv` (official PyPI wheel; reason: test RE2 `FullMatch` semantics on the
  exact library Hyprland links). No pacman, no host service, no compositor connection, no input, no dispatch.
- No counterexample was observed live: both findings are source-level. The round-27 bubblewrap oracle could confirm
  them (a `pseudo` rule on the oracle gkeep; a hide/show remap of a resized window) and was not used by this seat.
- Read-only on the lane: counters, tool, entry, registration and all receipts were never edited. Writes are confined
  to this seat's directory and this report; the scratch tree was removed after the receipts were copied here.
