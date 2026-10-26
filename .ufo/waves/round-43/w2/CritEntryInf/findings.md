# CritEntryInf — the entry's INF/UNK lines against the full upstream tree

Seat `CritEntryInf`, mado round 43 wave `w2`, 2026-10-26. Lane repo `/home/vgpnk/Projects/shokunin/mado-shokunin`.
Target: `corpus/knowledge/hyprland-gkeep-geometry-r43.md` at data commit
`1959770657f1f8665097c1aed4be6c1cbb07139f` (base `a35cfdfcdeb3bd42d1a2cd960faf22ceac1bef3f`).
Attacked against the whole Hyprland tree at `efb50993780079460b0cbed1363e2166a2de1d9f` (v0.56.2), not the seven
pinned excerpts: shallow clone, `receipts/clone-identity.txt` (rev, git version, and a byte comparison of all seven
round-43 pinned files against `receipts/fetch-sha256.txt`: 7/7 MATCH). Every source file I quote is pinned whole in
`pins/` (sha256 in `pins/SHA256SUMS`); locators are line numbers in those pins, unchanged from the clone.

Entry-line numbering below is `corpus/knowledge/hyprland-gkeep-geometry-r43.md:<line>`.

## 0. Verdicts

| entry line | the INF/UNK claim (short) | verdict |
|---|---|---|
| 36 | FullMatch makes `^`/`$` redundant; dots match any character | **SUPPORTED**, one word to tighten (`.` excludes newline by default) |
| 48 | "A tiled window never takes this branch: the size rule only acts through the floating algorithm … inert" | **FALSIFIED** (F1) |
| 56 | `clients -j` `size` is the GOAL; current differs during the open animation; no read verb exposes current | **SUPPORTED** at source (host-scope caveat) |
| 62 | two agreeing numbers are not one observation | **SUPPORTED** (no upstream counterexample; epistemic) |
| 68 | UNK: no gkeep window seen on this host | **SUPPORTED** (census pin) |
| 79 | "the size rule is evaluated on first map only" | **FALSIFIED** (F2) |

Neither finding breaks C1's or C2's measured target; both are defects of the landed *reasoning text* (F1 also of C1's
TILED model text). Detail, evidence and the smallest correction follow.

## 1. F1 — a tiled window does read the size rule (entry:48 falsified)

The claim under attack:

- Q[corpus/knowledge/hyprland-gkeep-geometry-r43.md:48] A tiled window never takes this branch: the size rule only acts through the floating algorithm
- Q[corpus/knowledge/hyprland-gkeep-geometry-r43.md:48] so without `float on` the rule's 420x500 is inert and the tiler decides the box.

The narrow first clause is true: a tiled target never reaches the floating algorithm's branch. The conclusions drawn
from it are not.

Counterexample (strongest, a box that is exactly the rule's size while `floating` is false): put the host's `size`
rule on a tiled window and a `pseudo` rule beside it, or toggle pseudo later. `mapWindow` reads `static_.size` in its
**tiled** branch, evaluates it and stores it on the target as the pseudo size:

- Q[src/desktop/view/Window.cpp:2402] if (m_ruleApplicator->static_.size) {
- Q[src/desktop/view/Window.cpp:2403] const auto COMPUTED = calculateExpression(*m_ruleApplicator->static_.size);
- Q[src/desktop/view/Window.cpp:2408] m_target->setPseudoSize(*COMPUTED);

and the pseudo flag comes from the same rule set, at map:

- Q[src/desktop/view/Window.cpp:2192] m_target->setPseudo(m_ruleApplicator->static_.pseudo.value_or(m_target->isPseudo()));

`setPseudoSize` warps the target and recalculates (`pins/Target.cpp:93-96`), and the box then comes from the stored
pseudo size, replacing the tiler's box:

- Q[src/layout/target/WindowTarget.cpp:145] auto calcSize = m_box.visualBox.size();
- Q[src/layout/target/WindowTarget.cpp:197] if (isPseudo() && m_window && !Fullscreen::controller()->isFullscreen(m_window.lock())) {
- Q[src/layout/target/WindowTarget.cpp:215] calcSize   = m_pseudoSize;

which lands in the same animated size the IPC reads, because the target's box is written into it:

- Q[src/desktop/view/types/GeometricMovableAnimated.cpp:45] *m_realSize     = x.size();
- Q[src/layout/target/WindowTarget.cpp:251] m_window->setBox(wb);

A pseudo-tiled window therefore reports
`"floating": false` with `size` = the rule's `420 500` — the rule decided the box, the tiler did not.

The second read site, for completeness (the entry quotes it; the first is missing from the entry's "who reads it"):

- Q[src/layout/algorithm/floating/default/DefaultFloatingAlgorithm.cpp:55] if (WINDOW->m_ruleApplicator->static_.size) {
- Q[src/layout/algorithm/floating/default/DefaultFloatingAlgorithm.cpp:56] const auto COMPUTED = WINDOW->calculateExpression(*WINDOW->m_ruleApplicator->static_.size);
- Q[src/desktop/rule/windowRule/WindowRuleApplicator.cpp:426] static_.size = expr;

The tree-wide receipt `receipts/grep-static-size-src.txt` lists every `static_.size` occurrence in `src/`: one reset
and one write in the applicator, and exactly these two read sites (Window.cpp:2402-2403 and
DefaultFloatingAlgorithm.cpp:55-56, plus their two error log lines). No third consumer exists: `setFloating` toggles
through `movedTarget`, not `newTarget` (F2 below), and the scrolling algorithm's size-ish rule is a different field:

- Q[src/layout/algorithm/tiled/scrolling/ScrollingAlgorithm.cpp:723] static_.scrollingWidth;

What survives of entry:48: for a tiled window with **no** `pseudo` rule and no later `togglepseudo`, the tiler decides
the box, so the host's gkeep chain is unaffected (the host config sets `float on` anyway). What fails is the
generalisation: the value is stored as the pseudo size, so "only acts through the floating algorithm" and "inert" are
both false.

Impact beyond the entry (operability axis): `clients -j` has no pseudo field — 29 JSON fields, `HyprCtl.cpp:395-423`,
none of them pseudo — and the C1 reference emits TILED from `floating` alone:

- Q[tools/mado-geometry.py:210] elif not floating:
- Q[tools/mado-geometry.py:211] verdict = "TILED"

so a pseudo-tiled window whose box is the rule's size is reported TILED, and the tool's own docstring repeats the
false premise:

- Q[tools/mado-geometry.py:6] a tiled window never reads it.

That is an open defect of `PRED-C1-r42`'s model text (no re-registration after data). It does not touch the 37 scored
fixtures, none of which is pseudo, and it does not touch the live `NO_MATCHING_CLIENT` receipt.

Smallest safe correction (entry §2, replacing the INF at line 48):

> **INF** A tiled window never reaches the floating algorithm's branch. The rule is still read for a tiled window:
> `mapWindow` stores its evaluation as the target's pseudo size (Window.cpp:2402-2408), and that pseudo size decides
> the box when the target is pseudo-tiled (WindowTarget.cpp:197-215). Without `float on` and without `pseudo`, the
> tiler decides the box; the rule's `420x500` is not inert, it is the window's pseudo size. `clients -j` has no pseudo
> field, so a pseudo-tiled window's rule-sized box is reported with `floating: false`.

Do not edit the frozen `tools/mado-geometry.py`; report the TILED/pseudo residual to the L1 instead. (This does not
re-admit the refused staged r10: that claim made the rule a pseudo-size request *for the client*, which stays refused;
what is shown here is the compositor-side pseudo size of a tiled target.)

## 2. F2 — "first map only" is not once per window (entry:79 falsified)

- Q[corpus/knowledge/hyprland-gkeep-geometry-r43.md:79] the size rule is evaluated on first map only, per the branch quoted above.

`m_firstMap` is armed inside `mapWindow`, i.e. once per map event, and cleared at the end of the same function:

- Q[src/desktop/view/Window.cpp:2079] m_firstMap      = true;
- Q[src/desktop/view/Window.cpp:2513] m_firstMap = false;

`mapWindow` is the listener body for every surface map, not only the first:

- Q[src/desktop/view/Window.cpp:183] m_xdgSurface->m_events.map.listen([this] { mapWindow(); });
- Q[src/desktop/view/Window.cpp:760] (In case a window got remapped)

An unmap does not destroy the window: it drops the target from the space and only clears the mapped flag, so a later
map re-enters `mapWindow` with the same `CWindow` and a fresh `m_firstMap`:

- Q[src/desktop/view/Window.cpp:2644] m_isMapped = false;
- Q[src/desktop/view/Window.cpp:2383] g_layoutManager->newTarget(m_target, m_workspace->m_space);

and that chain reaches the guarded branch again, because a target re-add dispatches to the floating algorithm:

- Q[src/layout/target/Target.cpp:21] if (m_space == space && !m_ghostSpace)
- Q[src/layout/space/Space.cpp:45] m_algorithm->addTarget(t);
- Q[src/layout/algorithm/Algorithm.cpp:35] m_floating->newTarget(target);
- Q[src/layout/algorithm/floating/default/DefaultFloatingAlgorithm.cpp:49] if (target->window() && target->window()->m_firstMap) {

Counterexample: a floating gkeep resized by the user, then unmapped and remapped by its client (a GTK hide/show is a
remap of the same `CWindow`) is put back at the rule's 420x500, because the branch runs again. The static rule set is
re-read at each map as well, so a remap also picks up a rule changed in between:

- Q[src/desktop/view/Window.cpp:2277] const bool recheck = m_ruleApplicator->readStaticRules();
- Q[src/desktop/view/Window.cpp:2278] setStaticProps();

For a tiled window the pseudo-size read at Window.cpp:2402 is not guarded by `m_firstMap` at all, so it runs on every map.

What remains true of entry:79: while a window stays mapped, neither a user resize, nor a monitor change, nor a rule
reload re-evaluates the size expression. A reload re-applies only dynamic rule effects to mapped windows:

- Q[src/desktop/rule/Engine.cpp:40] w->m_ruleApplicator->propertiesChanged(RULE_PROP_ALL);

and a floating/ tiled toggle goes through `movedTarget`, never `newTarget`:

- Q[src/layout/algorithm/Algorithm.cpp:70] m_floating->movedTarget(target, focalPoint);

Smallest safe correction (entry line 79):

> - What happens after the map: the size rule is read at every map event (`m_firstMap` is re-armed in `mapWindow`,
>   Window.cpp:2079) and the tiled pseudo-size read is not guarded by it; a user resize, a monitor change or a rule
>   reload while mapped does not re-evaluate it.

## 3. entry:36 — SUPPORTED, one word to tighten

- Q[corpus/knowledge/hyprland-gkeep-geometry-r43.md:36] The `^`/`$` anchors are redundant under FullMatch but harmless.
- Q[corpus/knowledge/hyprland-gkeep-geometry-r43.md:36] the dots match any character

`RE2::FullMatch` requires the pattern to consume the whole subject:

- Q[src/desktop/rule/matchEngine/RegexMatchEngine.cpp:16] return re2::RE2::FullMatch(other, *m_regex) != m_negative;

Hyprland builds the matcher with default `RE2::Options` (compile-time defaults), so I tested the host pattern against
the anchors-stripped pattern with the same RE2 library:

- Q[src/desktop/rule/matchEngine/RegexMatchEngine.cpp:12] m_regex = makeUnique<re2::RE2>(regex);

(`receipts/re2-anchors.txt`, script `receipts/re2_anchors.py`, google-re2 1.1.20251105): 12 candidate classes,
identical results for `^(org.omarchy.gkeep)$` and `(org.omarchy.gkeep)` under both `one_line` settings (default false
and true), including trailing newline, embedded newline, leading newline, trailing space, `\r`, and the
`orgXomarchy.gkeep` / `org-omarchy-gkeep` decoys — `identical on all candidates: True`.

One over-generalisation: "the dots match any character" — RE2's `.` does not match `\n` unless `dot_nl` is set, and
Hyprland does not set it (default options). No host class contains a newline, so nothing turns on it; the smallest
correction is "any character except newline". The example (`orgXomarchy.gkeep` matches) is confirmed, and so is the
stronger decoy the entry does not name: `org-omarchy-gkeep` also matches.

## 4. entry:56 — SUPPORTED at source

- Q[corpus/knowledge/hyprland-gkeep-geometry-r43.md:56] while the open animation runs, the current value differs from the goal
- Q[corpus/knowledge/hyprland-gkeep-geometry-r43.md:56] no read verb of the request socket exposes the current value

- GOAL is the IPC field: Q[src/debug/HyprCtl.cpp:427] w->size(Desktop::View::IGeometric::GEOMETRIC_GOAL).x
- the accessor split: Q[src/desktop/view/types/GeometricMovableAnimated.cpp:19] case IGeometric::GEOMETRIC_GOAL: return m_realSize->goal();
- Q[src/desktop/view/types/GeometricMovableAnimated.cpp:20] case IGeometric::GEOMETRIC_CURRENT: return m_realSize->value();
- the drawn size is CURRENT: Q[src/render/Renderer.cpp:566] pWindow->size(Desktop::View::IGeometric::GEOMETRIC_CURRENT);
- the open animation separates the two: Q[src/desktop/view/animationControllers/WindowAnimationController.cpp:39] const auto ENDSIZE  = (GOALSIZE * minPerc).clamp({5, 5}, {GOALSIZE.x, GOALSIZE.y});
- Q[src/desktop/view/animationControllers/WindowAnimationController.cpp:43] ctx.size.from = ENDSIZE;
- Q[src/desktop/view/animationControllers/WindowAnimationController.cpp:190] m_parent->sizeAnimation()->setValueAndWarp(ctx.size.from);
- Q[src/desktop/view/animationControllers/WindowAnimationController.cpp:194] m_parent->resize(ctx.size.to);
- no read verb exposes CURRENT: `receipts/grep-geometric-current-hyprctl.txt` (0 matches of `GEOMETRIC_CURRENT`
  anywhere in `src/debug/`, while `:427-428` and `:447-448` both use GOAL).

Caveat to keep attached to the claim: the separation holds only while animations are on; with animations off the tick
warps whenever value equals goal, so the two coincide:

- Q[src/animation/AnimationManager.cpp:44] if (warp || av.value() == av.goal()) {

The host's `animations:enabled = 1` is w1's receipt (S309), which I did not re-measure; the entry cites the same w1
finding, so the citation is honest.

## 5. entry:62 and entry:68 — no counterexample

entry:62 ("Two agreeing numbers are not one observation") is an epistemic claim and no upstream source contradicts it;
the oracle cases it cites exist (`w1/ExecOracleGkeep/10-cases.txt`, `20-observation.txt`, `rules-*.conf`), which I did
not re-run. entry:68's census is exact in the pin: four mapped clients, none floating, none `org.omarchy.gkeep`
(`.ufo/waves/round-43/fetch/host-clients-r43.json`). The two `UNK` table rows are scope-honest ("UNK on the host"); the
GOAL-vs-drawn row is answered at source by §4 above, which the entry itself already states, so I do not treat the row as
a defect.

## 6. Impacted axes

| axis | impact | verdict effect |
|---|---|---|
| coverage (C2 entry) | INF:48 and line 79 misstate one link of the chain (who reads the stored size, and when) | counter still `admitted=1/1`; claim text is wrong, target stands |
| operability (C1) | TILED rationale and docstring premise are false; pseudo-tiled windows are a false-negative class the tool cannot see | 37/37 and the live `NO_MATCHING_CLIENT` receipt unaffected; open defect of `PRED-C1-r42` |

No scored fixture, host receipt or counter output is changed by either finding; both are reasoning defects in the
landed data, reported for the L1 to route (no re-registration after data).

## 7. What I did not establish / open

- No compositor run: neither counterexample was observed live. F1 and F2 are source-level counterexamples; the
  round-27 oracle could confirm both (a `pseudo` rule on the oracle gkeep, and a hide/show remap of a resized window),
  and was not used by this seat.
- The host was not touched: no dispatch, no input, no Wayland client, no package transaction.
- `PRED-C1-r42` and `PRED-C2-r43-v2` were not run; the counters, the tool, the entry and all receipts were read only.
- Tooling: `google-re2==1.1.20251105` installed with `uv pip` into a scratch venv under
  `/fast/scratch/hyaku/mado-r43/CritEntryInf/venv` (official PyPI wheel; reason: test RE2 `FullMatch` semantics
  exactly). Scratch directory removed after the receipts were copied here.

## 8. Reproduction

```
cd /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-43/w2/CritEntryInf
sha256sum -c pins/SHA256SUMS                 # 16 pins
python3 verify-quotes.py                     # -> VERIFY: PASS
python3 receipts/re2_anchors.py              # needs google-re2; see receipts/re2-anchors.txt
```
