# ExecSrcChain — round 43 w1 (mado, inline v1)

Status: COMPLETE 2026-10-26.
Deliverable: `.ufo/waves/round-43/w1/ExecSrcChain/facts.md` — 65-row located-quote table
(`id | claim | quote | file:line | sha256`) for the entry's source chain, built only from the pinned
receipts S290–S296 in `.ufo/waves/round-43/fetch/`.

## Evidence

- `.ufo/waves/round-43/w1/ExecSrcChain/verify-facts.py` — greps every quote (fixed string, per 1-based
  line), re-checks each receipt's sha256, enforces the 25-word cap, and cross-checks the facts.md table
  against its own row list so the table cannot drift from what was verified.
- `.ufo/waves/round-43/w1/ExecSrcChain/verify-output.txt` — its output:
  `rows=65 failures=0 distinct_receipts=7`, `table_rows=65 table_failures=0`, exit 0.
  All seven receipts hashed as pinned; no sha mismatch.

## What the chain now stands on (each item is quoted at the cited line in facts.md)

- S290: `negative:` is stripped at construction (9 chars) and `match()` is
  `re2::RE2::FullMatch(other, *m_regex) != m_negative` — anchored whole-string match, negation flipped
  by the `!=`. (`Hyprland-RegexMatchEngine.cpp:7,9,16`)
- S291: `float`/`tile` write `static_.floating` from a bool; `size` takes exactly `Math::SExpressionVec2`
  (empty ⇒ `reset()`), stored **unevaluated and unclamped**; min/max are separate effects that do clamp
  (`clampWindowSize`) when `misc:size_limits_tiled` **or** the window is floating.
  (`Hyprland-WindowRuleApplicator.cpp:378,390,394,421–426,188–191,218–220`)
- S292: in `newTarget`, `desiredGeometry()` is fetched first, then gated on `m_firstMap` the rule size is
  evaluated into `windowGeometry.w/h`; a parse failure only logs. The box is then recentred in the work
  area **keeping its size**; no work-area or min/max clamp runs on it, and `fitBoxInWorkArea` is never
  called from `newTarget` (only from `movedTarget`, lines 160/170). Non-first maps use
  `lastFloatingSize` instead of the rule. (`Hyprland-DefaultFloatingAlgorithm.cpp:16,21,49,53–64,79–96,85–86,176,194`)
- S293: `ITarget::setPositionGlobal` stores the box and **rounds** the logical box; the CBox overload
  routes into `logicalBox`; `position()` returns the logical box. (`Hyprland-Target.cpp:10–17,65`)
- S294: `CWindowTarget::setPositionGlobal` → `updatePos`; for a floating non-fullscreen window it does
  `setBox(m_box.logicalBox)`, then `sendWindowSize()` when the `TARGET_UPDATE_NO_CLIENT_CONFIGURE` flag
  permits, then returns — the tiled `misc:size_limits_tiled` clamp is unreachable from there.
  `clampSizeForDesired` exists but is applied to *desired* geometry only.
  (`Hyprland-WindowTarget.cpp:36,39,50,70–77,297–313`)
- S295: `size(GEOMETRIC_GOAL)` is `m_realSize->goal()`, `GEOMETRIC_CURRENT` is `->value()`;
  `resize()`/`setBox()` write `m_realSize`, `finishAnimation()` warps it.
  (`Hyprland-GeometricMovableAnimated.cpp:19,20,40,45,50,58`)
- S296: `clients -j` fills `"size": [x, y]` from `w->size(GEOMETRIC_GOAL)` through `sc<int>`, in both the
  JSON and the text format. (`Hyprland-HyprCtl.cpp:395,400,427,428,448`)

Net: the rule size is a per-first-map override of the *goal* animation value, so `hyprctl clients -j`'s
`size` reports it while the client-facing configure is a separate call whose effect the receipts do not
observe.

## Quirks the L1 can cite (verified, easy to get wrong)

1. `newTarget` also warps the **(w,h) pair into the position animation** — "update for pos to work with
   size" (`Hyprland-DefaultFloatingAlgorithm.cpp:64`). Do not read that line as a position write.
2. The minsize case logs the text `"Invalid size for maxsize"` (`Hyprland-WindowRuleApplicator.cpp:214`).
3. The only match-engine mode is whole-string `FullMatch`; `^(...)$` in the host rule is redundant under it.
4. The tiled size clamp is behind `misc:size_limits_tiled` and is bypassed by the floating early return.

## What must not be asserted from these receipts (facts.md, "what the source does NOT say")

`sendWindowSize()` body / whether a client may decline; `CWindow::setBox`; `PHLANIMVAR`
`goal`/`value`/`operator=`/`warp` semantics; how rule text becomes `SExpressionVec2`; `calculateExpression`;
whether a rule size is ever clamped (no clamp call in `newTarget`); later user resize / float toggle;
monitor migration re-application; `sc<int>` rounding and logical-vs-pixel scaling; `MIN_WINDOW_SIZE` and
`clampWindowSize` bodies. The host rule text and the census are S297/S298, not quoted here.

## Risks / blockers

- None blocking. Two chain links are structurally outside the pinned set — S294:71 → `CWindow::setBox` and
  S295:45 → `PHLANIMVAR` — so the entry's final step ("the client's own request") has to rest on S297–S299,
  not on my receipts. Flagged in facts.md item 2.
- Tooling: nothing installed, no scratch tree created (`/fast/scratch/hyaku/mado-r43/ExecSrcChain/` never
  existed); only file reads of the pinned receipts, no compositor verb, no git/jj command, no write outside
  this seat directory and this report.
