# AttackCoverageCeiling — round 16 w2 critic

Seat: `MadoR16.AttackCoverageCeiling` (critic, leaf, no dispatch). Lane
`/home/vgpnk/Projects/shokunin/mado-shokunin`, baseline `32c4fda8`, integrated
worktree as of 2026-10-20 (uncommitted L1 edits to SCORECARD/LOG/SKILL/README/
QUALITY/SOURCES, untracked U7 note, lesson, measure.py).
Read first: `corpus/lessons/round-15-verifier-spotcheck.md`.

Target: does U1–U7 7/7 (10.0000) saturate or retire coverage, or erase the
PROVINCE-wide frontier?

What I ran: source reads, plus read-only greps and an in-memory Python parse of
worktree `corpus/SOURCES.md` `used-by` cells. I did **not** run measure.py, the
action-plan gate, selftest, frozen replay, or any live/host/package probe. I
installed or updated nothing. No tooling prerequisite is missing for this review.

## Verdict

My attack does not falsify the bounded C1 delta (6/7 → 7/7). It does find a
**fixable saturation/retirement defect**. The integrated text keeps the frontier
only in prose. No SCORECARD record yet marks the U1–U7 rubric as hitting its
ceiling, converts it to harm watch, or names a successor denominator.

If the pending results block calls coverage "complete", "saturated axis" or
"retired", or says "no frontier", that is calibration overreach. The judge
should reject it. If it carries the one-paragraph correction below, nothing
here blocks C1.

## A1 — Strongest counterexample: the U-denominator is not PROVINCE

AXES.md:12 defines coverage as the "fraction of the domain's real surfaces …
PROVINCE.md lists every surface; none unexplored without reason". PROVINCE.md:6-9
names the surface groups. The README province-route table (`corpus/README.md:55-63`)
lists seven groups: Hyprland, Waybar, Walker, terminals, themes/wallpapers,
screen/idle/lock, and Omarchy docs.

I parsed the `used-by` cells in worktree SOURCES (55 rows). Mined rows name only
these knowledge notes:

- window-rule-effects-getprop
- hyprland-config-era-r12
- xdg-portal-routing-r12
- wayland-protocol-boundaries-r13
- output-colour-boundaries-r14
- input-debugging-boundaries-r15
- waybar-observation-boundaries-r16
- config-drift-r12 (gkeep/gate drift)

**No mined row names any note for these surfaces:**

- Walker: `walker-deep`, `walker-live-surface`, `walker-deep-r9`
- Terminals: `terminals-and-omarchy`
- Themes: `theme-wallpaper-plane`
- Idle/lock: `idle-lock-plane`
- Omarchy: `omarchy-drift-watch`

Every queued row (S006–S010, S036, S038, S039) is Wayland, libinput or portal
material. The registry has **no queued study candidate** for those five surface
groups.

Using the PROVINCE groups as an illustrative denominator, sourced current-art
ground is 2/7 (Hyprland; Waybar custom module only) = 2.8571. The U1–U7 rubric
reads 10.0000. This is `[INFERENCE]`, an illustrative counter, and **must not be
scored or substituted this round** (QUALITY 22 forbids silent rubric change). It
shows that U1–U7 was chosen from the arc gap ledger plus the ART dossier
(SCORECARD.md:242-249), not from PROVINCE. Six of seven U-items sit on
Hyprland/Wayland plumbing.

## A2 — 10.0000 crosses the 9.0 saturation line with no ceiling record

- SCORECARD.md:272-274 sets saturation at 9.0 on every scored sub-axis.
- AXES.md:36-38 lets a saturated axis be retired or split.
- AXES.md:68-73 waives the lowest-axis rule when all axes are ≥ the line.

The integrated round-16 declared block (SCORECARD.md:696-702) says only "This is
not full domain coverage". LOG says "No retirement or next-round mission is
declared". SKILL says "The seven-item documentary rubric can complete while these
remain unknown".

None of these marks the sub-axis as being at its ceiling and converted to harm
watch. None states that the coverage **axis** stays open, or names what a later
planner should measure. The correct precedent exists: navigation 22/22 was
recorded as "saturated on its finite denominator; harm watch only"
(SCORECARD.md:236), with "Retired: none … broader coverage … open"
(SCORECARD.md:60-61).

`adjudication.json:8` accepts "MetricInflation … wider frontier retained", but
its F2 sentence has not landed. The results block is still pending.

This round, calibration's literal counter reads baseline 12/20 = 6.0000 and
worktree 14/22 = 6.3636 (my grep, not measure.py). The nudge cannot trigger now.
Next round, though, coverage will sit at 10.0000 on its only active current-art
rubric. Without the record, it silently drops out of lowest-axis selection.

## A3 — Instrument ceiling in measure.py

- `measure.py` matches `^covers: (U[1-7])$`.
- It scores `round(10 * len(covered) / 7, 4)`.
- A note with `covers: U8` sets `item=None` and hits `continue` before any
  candidate list. It produces no candidate, no warning, and exit 0.

Each round's counter has been copied forward (rounds 13→16). Reused as is, this
counter cannot see frontier growth and would read 10.0000 flat forever. That is
acceptable for C1 this round. It must not become the next coverage instrument.
Widening it in place (7 → 8 denominator) would be an undeclared rubric change;
QUALITY 22 forbids that.

## A4 — The "remaining frontier" chain ends in SOURCES

- SOURCES path tails name the next open ground: `:83` "U5–U7 remain frontier",
  `:87` "U6/U7 remain open", `:94` "U7 … remain frontier".
- The U7 path (`:95-98`) names none. It is also still headed "Waybar module
  observation boundary", not custom-module. This is a MetricInflation F4
  residual; the note title (`:6`) and README coverage row are already
  custom-qualified.
- README `:111-112` likewise says "U7's documentary observation route" without
  the custom-module qualifier.

## A5 — Retained correctly (attack failed)

- README:78-80: the top frontier bullet still lists "Waybar module text" and
  "per-window rule effects". FrontierDraft 3a's rewrite was not applied.
- README:113-116 limits the supersession to "only that finite route".
- Note `:10-11` and `:75-78`: a documentary route only; built-in module text
  contracts are not credited.
- Of the arc gap ledger's 12 unknowns (`arc-synthesis.md:336-341`), U1–U7 touch
  only window-rule effects (read route) and custom-module text (documentary).
  Ten remain untouched, and README still points at the ledger.
- LOG: "PROVINCE stays unchanged" and "No retirement". There is no false
  saturation statement anywhere in the integrated text.

## A6 — Structural limit, routed, not a round-16 fix

PROVINCE.md:1-18 has Domain/Owns/Refuses only. It has no Core/Frontier/Adjacent
split (LEARNING.md:73-77). The nudge's destination, "move PROVINCE.md frontier
ground into core" (AXES.md:71-72), therefore has no PROVINCE frontier to draw
from. With U1–U7 exhausted, frontier retention depends entirely on README
`## Frontier` prose and the arc ledger.

This predates round 16. Changing PROVINCE scope is an adjacency/operator-visible
decision. I record it as a planned item, not a demand on this round.

## Impacted axes

- **coverage**: inflation and retirement risk, not falsification. The bounded
  delta holds structurally on my read.
- **calibration**: integrity of next-round selection (A2/A3). Overreach if the
  results block says saturated/retired/complete.
- **adjacency**: PROVINCE frontier structure (A6), report-only.
- **operability / freshness / depth**: no finding.

## Smallest safe correction (L1-owned text only; no score or code change)

1. **SCORECARD round-16 results block.** Add one paragraph:

   > The sourced documented-route sub-axis saturates its fixed seven-item
   > U1–U7 denominator at 10.0000 (≥9.0). From here it is harm watch only, as
   > navigation is (SCORECARD:236). Retired: none. The coverage axis
   > (AXES.md:12, PROVINCE surfaces) stays open. Frontier: behavior layers of
   > U1–U7; ten arc gap-ledger unknowns; Waybar built-in module text; five
   > PROVINCE surface groups with no mined source (Walker, terminals,
   > themes/wallpapers, idle/lock, Omarchy docs). Before coverage is claimed
   > again, pre-register a successor coverage sub-axis with its own baseline.
   > The round-16 counter's `U[1-7]`/7 ceiling is not that instrument.

2. **SOURCES U7 path (`:95-98`).** Qualify it as custom-module, and append the
   same frontier tail: no queued source exists for those five surfaces.
3. **Planned (intent only).** Route PROVINCE Core/Frontier structure to a later
   operator-visible decision. Do not absorb it this round.
