# MetricInflation — critic report (round 16, w1)

Seat: `MadoR16.MetricInflation` (critic, leaf member, no dispatch). Source reading only.
Read first: `corpus/lessons/round-15-verifier-spotcheck.md` (U7 absent/absent; "U7 … remain
unmeasured"; "this closure does not silently broaden it"). Baseline/HEAD `32c4fda8`; worktree
carries L1's uncommitted SCORECARD/SKILL/QUALITY/SOURCES edits, the untracked note
`corpus/knowledge/waybar-observation-boundaries-r16.md` and `corpus/lessons/round-16.md`.
I wrote only this file. I made no edits, ran no gate, measure.py, selftest, build or live/host
probe, and installed or updated nothing. Calibration counts below come from in-memory parses of
`git show <rev>:corpus/QUALITY.md` and the worktree file. That is reading, not a checker run.

Attack target: whether 7/7 (10.0000) gets read as full desktop coverage, a saturated or
retired coverage axis, or "no remaining frontier". Axes: coverage (inflation), calibration
(lowest-axis selection), and the discernment trend.

## Verdict

The **bounded structural 7/7 holds**. The integrated U7 note passes the declared facets on my
read: header lines 1–4 have the trio, and `covers: U7` appears once. The four exact level-2
headings are at `:13,:28,:50,:65`, and `[UNK]` sits inside `## Unexercised rendering` at `:67-68`.
S053/S054 are mined, tier A and used-by the note, and S055's used-by is
`corpus/lessons/round-16.md`, so the inverse join holds. The note body is real, not just
headings. Four inflation risks remain, and each has a small fix. L1 should apply them before
the SCORECARD/README text lands. None of them is a reason to reject C1's bounded delta.

## F1 — "lowest active rubric" is false; calibration is lower (fixable, calibration axis)

Counterexample: `SCORECARD.md:696` calls C1 the "lowest active finite rubric" at 8.5714. The
calibration rubric is registered at `SCORECARD.md:234,286` as lesson-grounded QUALITY criteria,
and it was never retired (`SCORECARD.md:216-218,325-327,454`, "Retired: none"). It scores lower:

| Revision | Criteria | Literal registered grep `^[0-9]+\. .*lessons/` | Block-level (citation anywhere in the criterion) |
|---|---|---|---|
| `ea0446fc` (r15 baseline) | 19 | 12 → 6.3158 | 14 → 7.3684 |
| `9ebd737a` / `32c4fda8` | 20 | 12 → 6.0000 | 15 → 7.5000 |
| worktree (criterion 21 added) | 21 | 12 → **5.7143** | 16 → **7.6190** (upper bound before citation resolution) |

- On either reading, calibration is below 8.5714. After C1 lands, calibration is the lowest
  scored axis by a wide margin.
- Round 15 made the same error: its 7.1429 baseline was above calibration's 6.0 (literal) or
  7.5 (block). This round's PlanningWalk §2 found this independently. I add the next point.
- New point: the literal command stops at the first line of each criterion. Criteria 18–21 are
  multi-line and cite `lessons/` on a later line. So appending criterion 21 **lowers** the
  literal-command score from 6.0000 to 5.7143, even though the corpus gained a lesson-grounded
  criterion. The registered counter undercounts. The calibration rubric value is therefore
  ambiguous, not merely unmeasured.
- AXES.md:33-34 requires one claim on the lowest-scoring non-retired axis. The stagnation nudge
  cannot waive that, because calibration is below the 9.0 line.

Smallest safe correction (L1-owned text; no new claim needed):
- Change `SCORECARD.md:696` to "lowest coverage sub-axis" (or "lowest active coverage rubric").
- Record calibration as the lowest scored axis, at literal 12/21 (5.7143) and block 16/21
  (≤7.6190).
- Disclose that the AXES lowest-axis obligation is unmet this round. Leave that tradeoff to the
  operator/judge; do not hide it.
- Do not claim calibration "improved" from QUALITY 21. Under the registered literal command it
  dropped, so state it as unscored, or as moved −0.2857 on the literal reading.
- Name the multi-line counter defect as a lesson or frontier item. Do not silently switch to the
  block-level count.

## F2 — 10.0 crosses the 9.0 saturation line with no retirement or harm-watch record (fixable, coverage)

Counterexample: `SCORECARD.md:272-274` sets saturation at 9.0 on every scored sub-axis.
AXES.md:36-38 says a saturated axis "may retire". The round-16 declared block
(`SCORECARD.md:690-717`) says "not full domain coverage", but it says nothing about saturation,
retirement or the remaining frontier. A later planner could read coverage 10.0 as saturated and
retire coverage, or count it toward the "every axis ≥ 9.0" nudge condition. There is direct
precedent for doing this correctly: navigation 22/22 was recorded as "saturated on its finite
denominator; harm watch only" (`SCORECARD.md:236`), with "Retired: none … broader coverage …
open" (`SCORECARD.md:60-61`).

Smallest safe correction: put one sentence in the result block. Say the U1–U7
documented-route rubric is saturated on its seven-item denominator and becomes harm watch only.
Say "Retired: none": the coverage axis stays open and its frontier is named (F3). Say depth and
adjacency are still unscored, so they cannot meet the nudge's "every axis at or above" condition.

## F3 — 7/7 is not "no remaining frontier": the denominator is a chosen subset (fixable wording, coverage)

Counterexamples from local evidence:

1. **Gap-ledger unknowns outside U1–U7.** The gap ledger lists 12 unknowns
   (`arc-synthesis.md:336-341`). U1–U7 maps to at most three of them: window-rule effects (U1),
   Waybar module text (U7, documentary route only) and part of the rendered-UI boundary. U2–U6
   came from the ART dossier, not the ledger (`SCORECARD.md:242-249,299`). These stay untouched
   by any U item:
   - rendered UI
   - Walker socket protocol
   - idle/lock transitions
   - dispatcher behaviour
   - exec-once results
   - compositor env vars live
   - hypridle/hyprsunset stop-cause
   - tree-wide omarchy cleanliness
   - battery device
   - Walker edit-without-restart
2. **Each covered U item is a documentary route, not behaviour.** The lane's own limits say so:
   rule attribution is still open (`README.md:95`), as are U4 feature behaviour (`:99`), U5
   test/apply and HDR (`:101-103`), and U6 delivery and IME (`:107`). U7's note closes "a
   documentary route, not the ability to read arbitrary module text"
   (`waybar-observation-boundaries-r16.md:10-11`).
3. **README frontier erasure risk.** The current first frontier bullet (`README.md:77-79`)
   lists "Waybar module text". FrontierDraft's proposed 3a rewrites that clause to "now has a
   documented contract route", moving rendered output to a sub-bullet. If L1 lands it, keep an
   explicit open item for rendered and built-in module text (see F4) in the top-level bullet, so
   index completeness keeps carrying it (`README.md:75`).

Smallest safe correction: one sentence in the SCORECARD result and the README round-16
frontier bullet: "7/7 completes the finite U1–U7 documented-route rubric only; the arc gap
ledger's ten other unknowns and every U item's behaviour layer remain frontier." Do not write
"all ground covered", "coverage complete" or "no frontier".

## F4 — U7 is covered by a custom-module-only route; built-in module text is outside it (fixable scope, coverage)

Counterexample: U7's ground is "Waybar module text" in general. The gap-ledger entry is "no
IPC/query verb in waybar 0.15.0" (`arc-synthesis.md:301`; `SCORECARD.md:248`). S053/S054 are
the `custom` module's manual and `custom.cpp` only (`SOURCES.md` rows S053/S054,
"custom-module"). The host's recorded bar (`waybar-walker-semantics.md:119-154`) has 19
module rows:

| Kind | Count | Modules |
|---|---|---|
| `custom/*` | 9 | omarchy, update, weather, voxtype, screenrecording-indicator, idle-indicator, notification-silencing-indicator, expand-icon, ai-usage |
| Non-custom | 10 | `hyprland/workspaces`, `clock`, `clock#secondary`, `group/tray-expander`, `tray`, `bluetooth`, `network`, `pulseaudio`, `cpu`, `battery` |

The non-custom modules produce their text in-process through other module sources that were
not opened. The integrated note's title and framing are scoped to all modules: "Waybar module
text — producer data is not rendered output" (`:6`). The SOURCES path heading reads "Waybar
module observation boundary (U7, round 16)" (`SOURCES.md:95`). Only the body (S053 quote,
`Custom::update`) shows the route is custom-only.

The structural counter still credits U7, as declared. That is acceptable for a finite
documented-route rubric, but the scope should be stated. Smallest safe correction:
- Title and intro: "Waybar custom-module text".
- In `## Unexercised rendering`, add one `[UNK]` line: "Text routes of the built-in modules
  (clock, network, pulseaudio, bluetooth, battery, cpu, hyprland/workspaces, tray) — their
  sources were not opened."
- SCORECARD/README: say "U7 custom-module documented route".

## F5 — navigation harm-watch trap in the pending README draft (fixable, harm watch)

FrontierDraft's proposed coverage-map row points at `knowledge/waybar-module-text-boundaries-r16.md`
(FrontierDraft.md:37,47). The integrated file is `waybar-observation-boundaries-r16.md`.
Pasting the draft verbatim would make navigation report missing 1 and an extra or dangling 1
instead of 30/30. That harms the harm-watch counter, which is `measure.py` `nav`, an exact
filename join. Correction: use the real filename. README currently has no U7 row, so it must be
added for 30/30.

## Structural counter limits (retain, do not overclaim)

`u7_facets` (`measure.py:160-181`) keys on exact level-2 headings and a literal `[UNK]` token.
A header-only note with S053/S054 mined rows would score U7. The semantic hand check stays
L1's, as the round-15 closure required (L98). My spot read finds the body substantive:
- hide/parse/format/`set_markup` ordering at `:30-36`
- a four-row layer table at `:38-43`
- non-execution boundaries at `:52-57`

One minor body imprecision, not inflation: `:18` lists the JSON fields as
text/tooltip/class/percentage and omits `alt`. `alt` appears at `:32`, and the WaybarDraft
source reading (`waybar-draft.txt:18`) includes it. If convenient, also note that `{icon}` can
key on `alt`.

## Impacted axes

- **coverage**: bounded improvement verifies structurally. The inflation risks are F2, F3 and
  F4, and F5 is a harm-watch risk. All are wording or index fixes.
- **calibration**: F1. The wrong lowest axis is named, and the registered literal counter fell
  from 6.0000 to 5.7143. This must be disclosed, not traded silently.
- **discernment trend**: improved only if F1–F4 are recorded as rejected inferences. The
  rejected readings are 7/7 = full Waybar or desktop coverage, 7/7 = saturated or retired
  coverage, and 7/7 = no frontier.
- **operability, freshness, depth, adjacency**: no metric-inflation finding (C2 is out of this
  seat's scope).

## Missing prerequisites / tooling

None for this review. No tools were installed or updated, and no package, service, compositor,
producer or input operation was performed.
