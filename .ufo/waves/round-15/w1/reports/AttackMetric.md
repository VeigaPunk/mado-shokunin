# AttackMetric — mado round 15, w1 (critic)

Status: read-only critique. No gate, selftest, `measure.py`, fixture, test, or live probe was run. No tools were installed or upgraded. The only write is this file.

The round-15 counter `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-15/measure.py` had **not landed** when I checked (04:26). This review therefore attacks two things:
- the predicate as specified in the MeasureBuild prompt (`.ufo/waves/round-15/w1/spec.json`, item MeasureBuild): "headings ## Layer ladder, ## Safe boundary, ## Unexercised delivery and [UNK] in last; cite S051/S052 in source header, both mined reciprocal";
- the round-14 implementation it is told to reuse: `.ufo/waves/round-14/measure.py:112-200`.

Axes: **coverage** (the scored sourced current-art join U1–U7) and **calibration/discernment** (whether a structural count is passed off as provenance).

## Counterexample (strongest)

A U6 note that inverts the safety boundary scores exactly the same as a correct one.

Method: I re-implemented `body_facets()` from round-14 `measure.py:123-143` in memory, with the U6 heading names swapped in, plus the head-15 header join from `:158-166`. I evaluated it on synthetic strings only. No repo code was executed and no file was written.

| Case | Content | Structural result |
|---|---|---|
| A | Header trio plus three empty headings plus a bare `[UNK]` | **pass** |
| B | `## Safe boundary` says "Run `sudo libinput record` and `libinput replay`; harmless read-only"; the last section says "No [UNK] remains: delivery verified on host." | **pass** |
| C | Body is Waybar (U7) prose; the three headings appear only inside a ``` fence | **pass** (the parser ignores fences) |
| D | Negated unknown: "There is no [UNK] here; all delivery observed." | **pass** |
| E | `[UNK]` only in the heading text (`## Unexercised delivery [UNK]`) with an empty body | **pass** (the heading is concatenated at `:141`) |
| F | `## Layer ladder (TODO)`, `## Safe boundary is unnecessary` | **pass** (prefix `re.match`) |
| G | `[UNK]` placed under `### Keyboard` beneath `## Unexercised delivery` | **fail** — false negative: `#{2,6}` splits every subheading into its own section |
| H | `source:` wrapped onto two lines, with S052 on the second | **fail** — false negative: only the first line is read (`:159`) |
| I | Header placed after a long title block | **fail** — false negative: only the first 15 lines are read |

Case B is a correct structural pass of content that this wave's contract forbids: recording, replay, and claimed delivery. The counter cannot tell a bounded route from an unsafe one.

## Evidence that the counter is not a semantic oracle

- **Self-attested joins.** `mined`, tier `A`/`B`, and `used-by` are cells that L1 writes in the same commit (`measure.py:106-109,166-168`). Reciprocity proves only that the registry and the note agree with each other. It does not prove that:
  - the URL resolves,
  - the revision is immutable,
  - any quote exists in the source.
- **Mutable precedent.** The existing row S007 points at a mutable `libinput/doc/latest/tools.html`, has status `queued`, and has `used-by` set to `—` (`corpus/SOURCES.md:19`). A versioned S051 URL differs as a string, so the URL-duplicate census (W04) will not flag that the two rows are semantically the same source. The counter is blind to this.
- **The two recipes already disagree.** The outside round-14 recipe (`corpus/lessons/round-14-verifier-spotcheck.md:51-78`) differs from the lane counter in four ways:
  - it searches `source:`/`covers:` anywhere in the file, not just the first 15 lines;
  - it does a substring test `path in used-by`;
  - it has no tier filter;
  - it checks no facets.

  Both happened to report 5/7. The semantic admission came from the reopened-source table and quote checks (`:88`, `:134-142`), not from either count.
- **Round-14 wording precedent defect.** `SCORECARD.md:513` credits "AttackCoverage's actual-note review" as the semantic hand check. AttackCoverage was a lane-dispatched seat, and QUALITY 12 (`corpus/QUALITY.md:18`) says such seats remain `[~]`, not independent clearance. Round 15 must not repeat that wording.

## Denominator limits that must be disclosed

1. **The `/7` list is author-chosen and finite.** It comes from the arc-synthesis §6 gap ledger plus an `[INFERENCE]`-tagged ART bullet (`SCORECARD.md:243-249,299`). 7/7 = 10 would not mean province saturation.
2. **Credit is binary per item.** The U6 label reads "kernel-input → Wayland debugging ladder" (`SCORECARD.md:248`). This round's route excludes kernel diagnosis, actual delivery, and IME. It earns the full 1/7 only as "U6 documented layer route", the same convention used for U4/U5 (`wayland-protocol-boundaries-r13.md` "closes the documented … route"). The SCORECARD row must use that name.
3. **Facet checks are uneven.** U1–U3 are counted on header joins alone, with no body facets. U4, U5 and U6 have structural facets. The checks are not uniform across items.
4. **A count can hide a swap.** Report the item **set** before and after and require before ⊆ after. Otherwise a lost U5 plus a gained U6 would read as an unchanged 5/7.
5. **Other figures are not coverage.** Navigation N/N grows with note count. Registry 50→52 is source volume.

## Smallest safe correction

**Required — fixes the false-provenance risk:**

1. **Name the output as candidates, not admissions.** The counter emits `coverage.items` only as *structural candidates*. Add `u6_candidates` (mirroring `u5_candidates`) with:
   - per-facet booleans,
   - the note blob id `git rev-parse <sha>:corpus/knowledge/<note>.md`,
   - `admission: "manual-required"`.

   Exit 0 stays non-admission.
2. **Admit manually, bound to the note blob.** An admission record bound to that blob id checks:
   - (a) every ladder row is class-tagged `[OBS]`, `[INF-docs]` or `[UNK]`;
   - (b) every quote is ≤25 words and is located at the pinned S051/S052 revision, with a byte digest;
   - (c) `## Safe boundary` lists debug-events, record, replay, evtest and uinput as **refused**, never recommended (case B);
   - (d) `[UNK]` affirmatively names unexercised delivery, IME/text and kernel layers, and is not negated (D/E);
   - (e) the headings are real Markdown, not fenced (C).

   Any later edit to the note changes the blob id and voids the admission.
3. **SCORECARD wording.** Use: "U1–U6 6/7 structural; semantic admission pending non-author closure (QUALITY 12)". Never cite lane seats as the semantic check.

**Optional hardening.** These fix defects but do not make the counter semantic:
- strip fenced blocks before parsing headings;
- require `[UNK]` in the section body, not the heading;
- fold `###` subsections into their parent section;
- document the single-line `source:` and head-15 formatting dependency.

Cases A, B, D and F still pass after hardening.

## Classification

- **Fixable defects:** C, E, G, H, I, the item-set check, and the SCORECARD:513-style lane-seat wording.
- **Irreducible tradeoff:** A, B, D and F cannot be detected structurally. The judge must reject any record that treats the counter's 6/7 as admission, or that credits U6 for kernel or delivery coverage.

Checks for main/L1 once MeasureBuild lands:
- `python3 .ufo/waves/round-15/measure.py <baseline>` and `<after>` (compare item sets);
- the non-author manual admission record bound to the U6 note blob id.

Report path: `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-15/w1/reports/AttackMetric.md`
