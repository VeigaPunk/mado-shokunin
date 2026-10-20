# AttackU7Scope — does 7/7 read as domain mastery?

Seat `MadoR16.AttackU7Scope` (critic, leaf). Integrated working tree over
baseline `32c4fda`. Source reading only: no gate, measure, test or live probe
was run, and nothing was installed. Required reading done:
`corpus/lessons/round-15-verifier-spotcheck.md`.

Axes: **coverage** (C1 U7 credit scope), **calibration** (claim honesty),
**operability** (harm watch only; untouched here).

## Verdict

The note and the frontier text keep actual module text `[UNK]`. No artifact
claims the text is observed, closed or complete. The 7/7 credit is
admissible on the declared binary per-item rubric. Two scope gaps could still
let a later round read 10/10 as mastery, and both are fixable. Neither is a
rejection.

## Findings, most severe first

### F1 — 10/10 saturation and retirement are unguarded (moderate, fixable)

- **Counterexample.** `SCORECARD.md:272` sets the saturation line at 9.0 for
  every scored sub-axis. `AXES.md:36-38` lets a lane retire a saturated axis.
  `SCORECARD.md:236` sets a precedent: a finite rubric at 10/10 becomes
  "saturated on its finite denominator; harm watch only".
- **What follows.** After round 16, both coverage rubrics sit at 10:
  reachability and sourced ground. Coverage then has no active scored rubric.
  Next round, a lowest-axis walk under the QUALITY22 rule never ranks coverage
  as lowest. Actual module text, built-in module contracts and U1–U6 feature
  behaviour lose their scoring pressure.
- **What the round-16 text already says.** `SCORECARD.md:700-701` says "not
  full domain coverage". `LOG.md` says "No retirement … is declared". Neither
  says the axis is unsaturated, and neither says a new coverage rubric must be
  declared.
- **Smallest correction.** Add one sentence to the round-16 results:
  - 7/7 saturates only the finite seven-item documentary rubric.
  - That rubric moves to harm watch, with the item-set check before ⊆ after.
  - The coverage axis is neither saturated in the PROVINCE sense nor retired,
    and `Retired: none` is recorded.
  - Coverage cannot be ranked again until a new coverage rubric or sub-axis is
    declared.
- **Precedent wording.** Mirror `SCORECARD.md:52-53` ("can reach 10 on this
  finite corpus without saturating the province's broader coverage axis")
  and `:61`.

### F2 — U7 is credited by a custom-module-only route (moderate, naming)

- **The mismatch.** The rubric item is "U7 Waybar module text"
  (`SCORECARD.md:248`). The admitted route covers only the `custom` module:
  - Sources: S053 is `waybar-custom.5.scd` and S054 is `custom.cpp`.
  - The note discloses it: "Built-in module source paths were not opened for
    this route; their text contracts are not credited" (note `:77-78`).
  - `ALabel` base-class details are `[UNK]` (note `:73`).
- **The host config.** `waybar-walker-semantics.md` §3 lists 19 module rows
  (`SCORECARD.md:14`).
  - 9 are `custom/*`: omarchy, weather, update, voxtype,
    screenrecording-indicator, idle-indicator,
    notification-silencing-indicator, expand-icon, ai-usage.
  - 10 are built-in: `hyprland/workspaces`, `clock`, `clock#secondary`,
    `network`, `battery`, `bluetooth`, `pulseaudio`, `cpu`, `tray`,
    `group/tray-expander`.
  - Built-ins have no producer stdout, so the producer → parser stages do not
    apply to them.
- **Where the qualifier appears.** The README index row says "Tagged
  custom-module". The qualifier is missing from:
  - the SCORECARD C1 claim (`:696-701`);
  - the SKILL round-16 section (`:498-509`, "separate producer stdout …");
  - the README frontier bullet (`:111-116`).
- **The risk.** A reader of SKILL could apply the producer route to the
  clock, cpu or network modules.
- **Smallest correction.**
  - Name the result row "U7 documented custom-module text-observation route",
    following round-15 AttackMetric item 2 for U6.
  - Add one clause to the SKILL and README bullets: custom modules only; the
    text contracts of the 10 built-in host module entries are unsourced.
  - The binary 1/7 credit stays within the same convention used for U4–U6.

### F3 — A stale SKILL row still teaches producer-run reconstruction (low)

- **The stale row.** `SKILL.md:112` (config-plane map) still says "module text
  config-only, reconstruct via pure-read producers (`RUN`)". That is exactly
  the producer = shown-text conflation the note rejects (note `:28-30`,
  `:56-61`).
- **Why the existing fix falls short.** The supersession at `SKILL.md:503-504`
  is generic: "historical `RUN` route elsewhere". It is not linked from
  `:112`, and an agent reaches the earlier table first. `SKILL.md:147` and
  `:656` are consistent with the note.
- **Smallest correction.** Pick one:
  - append a pointer to the `:112` cell, e.g. "(producer output ≠ current
    label; see Waybar observation boundary r16)"; or
  - cite `:112` explicitly in the `:503` sentence.

### F4 — The counter cannot see the unknown being erased (low, declared counter limit)

- **The limit.** `measure.py:168-189` `u7_facets` requires only the heading
  set and a literal `[UNK]` token in `## Unexercised rendering`. A degraded
  note still passes, for example: "`[UNK]` none remains; live text
  reconstructed via producer RUN".
- **Same class as before.** This is the counterexample class D/E from round-15
  AttackMetric. Preservation in README, SCORECARD and SKILL is not measured at
  all.
- **Why it is not a defect.** It is a limit of a structural observation
  probe. The docstring at `:2`, `:34-36` says observation, not admission.
- **Smallest correction.** Do not widen the counter mid-round. In the result,
  L1 should record a hand facet check that the rendering section names current
  live text as `[UNK]`. It does today: note `:71` "Current live text …" and
  `:75-76` "Actual module text remains frontier".
- **Minor.** `u7_facets_observed` (`:286`) is last-candidate-wins. Per-candidate
  facets are still reported in `u7_candidates`.

## Attacks that failed (they hold)

- **The note preserves the unknown.** `:10-11` "closes a documentary route,
  not the ability to read arbitrary module text". `:71-76` keeps live text,
  tooltip, CSS, glyphs and pixels as `[UNK]`.
- **The README frontier still lists it.** `:78-80` keeps "Rendered UI, Waybar
  module text". `:113-116` keeps actual module text, GTK state, pixels and
  freshness unmeasured, and claims no capability to read the live bar.
- **The SCORECARD claim is bounded.** `:700-701`: "not full domain coverage
  or a claim to observe rendered module text".
- **SKILL and LOG agree.** SKILL `:509` says the rubric "can complete while
  these remain unknown". LOG says "actual text remains unknown".
- **The lesson rejects the conflation.** §Gate `:43-46` rejects producer
  output as rendered text and tagged source as binary equivalence.
- **S055 is never credited to U7.** `measure.py:203-206` requires
  `U7_SOURCES = ('S053','S054')`. The inverse join forces S055 to be cited
  only if it names the note, and S055 `used-by` is the lesson, not the note.
- **No closure phrasing anywhere.** A grep over corpus, SKILL, SCORECARD and
  LOG for module text near "closed", "complete", "covered" or "resolved"
  finds no closure claim.

## Impacted axes

| Axis | Impact |
|---|---|
| coverage | Credit is valid on the declared rubric. F1 and F2 are scope and saturation naming, needed so 10/10 is not read as domain mastery. |
| calibration | F1, F2 and F3 are honesty corrections to wording. No harm exists yet, because the results row is not written. |
| operability | Not touched. |

For the canonical judge, none of F1–F4 is a tradeoff to reject: each is fixed
by appended wording in L1-owned files.

No tool was installed or updated. No sibling or shared file was edited.
