# ScribeLessonD2 — C2 defect D2

## Behavior / axis

The existing Round-27 erratum at lesson lines 34–36 satisfies the requested C2 D2 prose: it records the malformed-row pointer, M27-2 / E01 (`NF!=13`), the location of the quotes in `## Gate`, and the sources seat's registry-repair responsibility. It was already present on this seat's first read, so this seat made no duplicate append or lesson edit; its authorship/history was not independently verified.

Observed section bytes (lesson lines 34–36, preceded by one blank line; copied verbatim):

```text
## Round-27 erratum (round 28)

The malformed two-cell S178–S182 quote rows were at `corpus/SOURCES.md:195-199`; they failed M27-2's E01 schema check (`NF!=13`). The located quotes live in this lesson's `## Gate` table, not in `SOURCES.md`. The round-28 sources seat repairs the registry rows themselves; this lesson does not edit `corpus/SOURCES.md`.
```

## Gate and findings

- Read-only predicate inspection: the observed lesson text contains both exact required literals; current working-tree `corpus/SOURCES.md:190-194` contains `| S178 |` through `| S182 |`. The frozen predicate is `.ufo/waves/round-28/c2/count.py:106-114`; it measures committed bytes at the supplied REV, which these reads do not establish.
- Requested scratch-clone run and D2 output line: **not run / unavailable**. The scribe role forbids invoking another runtime, so this seat did not execute `python3 -I .ufo/waves/round-28/c2/count.py <clone-rev>` or create a measurement clone. No frozen-counter `CHECK D2` line or clone measurement is claimed.
- Other D predicates: the D2 lesson block is on a different input path from D1 and D3–D9, whose predicates read other paths in the frozen counter. This seat made no product-file changes; other D statuses were not measured, and no claim is made about unrelated inherited changes.

## Touched surfaces / out of scope

- Read-only review: `/home/vgpnk/Projects/shokunin/mado-shokunin/corpus/lessons/round-27.md:34-36`; not edited by this seat.
- Report: `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-28/w1/reports/ScribeLessonD2.md`.
- Not edited: `corpus/SOURCES.md`, `.ufo/waves/round-28/c2/count.py`, and M27-1..M27-3. No tools were installed. No clone/counter execution or commit was performed; only the stated file reads were used to inspect the D2 literals.
