# SkillSectionJoin — round 17 scoped report

Seat `MadoR17.SkillSectionJoin` (connector, leaf; no subagent dispatch). Report only: no
edits to SKILL.md or any product file, no commit, no `jj`, no gate/selftest run.
Lane root: `/home/vgpnk/Projects/shokunin/mado-shokunin`.

Target identity (measured before report): `SKILL.md` 1780 lines, sha256
`9a237472b07f8e8cf5d8055bbccf42d0ad3428bbcf7dded210b4b44f2c9a421e`; byte-identical to
`git show 0175f13:SKILL.md` and `git show 9dcf248:SKILL.md`; `git status --porcelain SKILL.md`
empty; last commit touching it `9dcf248`. `grep -ci tripwire SKILL.md` → 0, so no existing
tripwire text is being reconciled. Every line number below is against **that** file; if the
digest changes, recompute before applying.

## 1. Registry table end

| Element | Line(s) | Anchor text |
|---|---|---|
| `## Gate registry` heading | 525 | — |
| registry preamble (defines this file as registry home) | 527-530 | line 529: "Historical usage sections / below retain their original revisions, not current instrument pins." |
| table header / separator | 532 / 533 | `| name | gate/probe | entry command | …` |
| last row | **545** | `| mado-round16-measure | probe | python3 .ufo/waves/round-16/measure.py REV | …` |
| blank separator | 546 | — |
| first post-table note | 547-556 | `Round-16 classifier limit: …` |

**L1 insertion point for new rows: after line 545**, before the blank line at 546. Two rows
(`mado-tripwire`, `mado-label-check` per `.ufo/waves/round-17/drafts/SkillRegistryDraft.md`)
occupy new lines 546-547; the blank and the classifier-limit paragraph shift down by 2. Rows
must stay one physical line each (all existing rows are single lines; wrapping breaks the
8-column shape). Row text is SkillRegistryDraft's artifact, not this seat's.

**Limit paragraph insertion: after line 556** (end of the round-16 classifier-limit
paragraph), i.e. insert one blank line + the 5-line paragraph at 557-562; the existing blank
at 557 then separates it from the `mado-regression` note at 558. Alternative at 571 (end of
the last per-row note, before `## Evidence trail & sources` at 572) is also append-clean; the
556 point is preferred because per-tool limit notes then stay adjacent to their rows
(round-16 classifier-limit precedent).

## 2. Safety instruction section added in round 16

Round 16 added three safety-instruction blocks to SKILL.md (confirmed against
`git diff -U0 32c4fda 4bfb236 -- SKILL.md`: hunks `@@ -38,0 +39,7 @@`, `@@ -230,0 +238,3 @@`,
`@@ -476,0 +487,13 @@`):

| Block | Line(s) | Status |
|---|---|---|
| Standing-rules bullet `**Host-wide package pause until an explicit operator recovery decision:**` … `see QUALITY21/M1/M2` | **39-45** | the seat-facing mirror of the pause |
| `**Round-16 override:** no producer execution …` inside Safety rule 2 | **238-240** | producer-execution addendum (rule 2 starts 232, rule 3 starts 241) |
| `**Round-16 superseding instruction:** all pacman transactions are currently paused host-wide. … not editing its input to manufacture permission.` | **487-498** | **the canonical safety-instruction section added in round 16**; sits inside `### Input debugging and tooling safety (round 15)` (heading 458, section body 459-498), after the round-15 install rule at 477-485 |

The round-16 Waybar subsection (`### Waybar observation boundary (round 16)`, 505-523) is a
diagnostic boundary, not a safety instruction; it is only the precedent for *where a
round-17 boundary subsection goes* (see §3).

## 3. Where a tripwire usage instruction belongs

The tripwire is operational/current, so it must not land below line 525: lines 529-530
declare that usage sections below the registry retain their original (historical)
revisions. The live-series home is `## Current diagnostic boundaries (round 13)` (heading
409), whose subsections are one per round: `### Output/colour … (round 14)` at 421,
`### Input debugging and tooling safety (round 15)` at 458, `### Waybar observation boundary
(round 16)` at 505-523.

| Priority | Block | Insert after line | Result |
|---|---|---|---|
| **Primary** | new `### Post-hoc transcript tripwire (round 17)` subsection: CLI (`python3 -I tools/mado-tripwire.py --scan PATH [PATH …] [--permit CLASS …]`), first verdict line, one-line JSON verdict schema, class/rule vocabulary, exit map (0/1/2, 2 wins over 1), selftest invocation, and the limits (post-hoc detection only; assistant `toolCall` bash/eval inputs only, `!`-prefixed eval code as shell; quoted args are data; clean scan ≠ no host mutation; unlisted wrappers unclassified; transcripts are mutable host files; not interception, prevention or host repair) | **523** (last line of the Waybar subsection; blank 524 stays as separator) | new heading becomes 525; `## Gate registry` and everything after shifts down |
| Secondary | `**Round-17 addendum:**` one-paragraph pointer ("the round-15/16 pause breach is now detectable after the fact by …; detection is not remediation") appended to the safety chain | **498** (last line of the round-16 superseding instruction; blank 499 stays) | continues the round-15 (477-485) → round-16 (487-498) → round-17 sequence; same coordinate if L1 instead adds a sub-heading inside 458-498 |
| Optional | standing-rules one-liner pointer next to the pause bullet | **45** (last line of the bullet; blank 46 stays) | every fresh agent sees it where the pause is stated (round-16 put the pause there for this reason) |

Do **not** add the usage text as a new checklist step. `## Scoped verification` documents
steps 0-9 (264-299), and two existing lines assert that count: line 621 "per-step
sufficiency over steps 0–9" and line 679 "the manual equivalent stays this SKILL's Scoped
verification checklist (steps 0–9)". Appending a step 10 falsifies both without an edit.
Do not insert a traps-table row unless it states what a clean scan cannot settle; the
`## Error patterns & traps` table ends at 369 (heading 371).

## 4. Apply order (keeps all coordinates valid)

Insert bottom-up — each insertion shifts only lines below it, so the remaining
(lower-numbered) targets stay exact:

1. after **556** — tripwire limit paragraph (blank + 5 lines).
2. after **545** — two registry rows.
3. after **523** — `### Post-hoc transcript tripwire (round 17)` usage subsection.
4. after **498** — round-17 safety addendum paragraph.
5. after **45** — optional standing-rules pointer.

Expected end state: `1780 + 6 + 2 + len(usage) + len(addendum) + (1 if optional)` lines;
`grep -n '^| mado-tripwire \|^| mado-label-check \|^### Post-hoc transcript tripwire \|^Round-17' SKILL.md`
must resolve each block exactly once; lines 621 and 679 text unchanged; `grep -c '^|' SKILL.md`
grows by exactly 2.

## 5. Findings / risks for L1

1. **Line-number drift is the main integration risk**, not content: two other seats target the
   same region (SkillRegistryDraft at 545; this report's 556/523/498/45). Apply bottom-up and
   re-measure the digest before and after.
2. **Ambiguity resolved, not hidden:** round 16 added three safety blocks (39-45, 238-240,
   487-498). The "safety instruction section" is 487-498; 39-45 is its standing-rules
   mirror. If L1 wants a single insertion, use 498; the 45 pointer is optional.
3. **Historical-vs-current placement:** anything appended after line 525 reads as historical
   under the preamble at 529-530, so the usage block must go at 523, not in an append like
   `### Gate usage — tools/mado-verify.sh` (646, round-5 historical).
4. **Registry row is not verification** (round-16 precedents: 552-553 "It does not intercept
   actual tool calls … not prevented or repaired"; 564-565 "Registration alone is not
   verification"). The usage section should carry the same sentence so the row cannot be read
   as a green gate.
5. **No claim of prevention.** Per the round's C3 boundary, wording must keep the tripwire
   post-hoc only and must not imply host repair; R15-V1 stays operator-owned (39-45, 487-498).

## 6. Host-pause compliance / tooling

No pacman/yay/paru/sudo/systemctl/hyprctl/omarchy-*/libinput/evtest/wayland-info/hypridle/
hyprlock/alacritty/waybar/walker command, no live probe, screenshot or input/device probe, no
`~/.omp/agent/agent.db*` or credential access, no omp CLI process, no `jj` command. Read-only
`git show`/`git diff`/`git log`/`git rev-parse`/`git status` and file reads only.
Tool installs/upgrades: none (nothing needed).

## Out of scope

No SKILL.md/SCORECARD/LOG/PROVINCE/corpus edits, no drafts, no gate or selftest execution.
