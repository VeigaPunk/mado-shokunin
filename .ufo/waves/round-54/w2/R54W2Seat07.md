# R54W2Seat07 — C1 second-table laundering

## Verdict

**Concrete parser weakness reproduced in the relevant w1 prototype; current frozen counter NOT RUN (absent).** A parser that scans all `Pin:anchor` tables / all P-rows across the entire entry can accept a valid second table after the first table has lost P22. A parser that binds validation to the canonical table rejects the same input. This is not evidence about a landed counter: there is no `quality/counters/c1-r54-errata-truth.py` at the inspected path, so no current implementation was available to attack.

## Frozen contract and exact fixture

`claims-frozen.md:19-30` requires each of the four corrected propositions **P19–P22** to verify, including each quote in the pin named by its `Pin:anchor` cell, exact anchor side-claims and pin integrity. The exact frozen spans in `registration.md:25-34` are:

- P19: `Hyprland-ConfigActions.cpp:1554-1558`.
- P20: `Hyprland-ConfigActions.cpp:1576`.
- P21: `Hyprland-legacy-DispatcherTranslator.cpp:619-622` (within 591–627).
- P22: `Hyprland-legacy-DispatcherTranslator.cpp:573-574` (after 571).

The registration's frozen rows are at `registration.md:20-34`; control C1-CTL-5 removes P22 (`registration.md:40-47`). A second valid table cannot satisfy the missing P22 in the canonical first table without violating the required P19–P22 inventory; the entire-entry scan is the laundering route.

## Attack evidence from the relevant w1 report

The directly relevant prior result is `w1/R54Seat05.md:186-222` (X-CTL-E). It defines the exact attack: drop P22 from the first table, append P19–P22 in a second `Pin:anchor`/`Quote` table. Its recorded outcomes are:

- Whole-file P-row scanner: finds P19–P22 in the decoy table and can falsely pass the four-proposition test.
- Canonical-table-bound parser: rejects with `props=3/4` and the explicit diagnostic `additional Pin:anchor table(s) (ambiguous)`.

The w1 report states X-CTL-E: `MISSED|3|3|3|4|True` for its prototype and explains that the added table is rejected as ambiguous. This is a prior scratch-prototype result, not a run of the present counter. Related item-specific corroboration: `w1/R54Seat05.md:173-200` explains why row-count/entry-derived membership is insufficient; P22 must be a required ID, not replaced by arbitrary P-row content.

## Current run / availability

Exact command:

```sh
if test -f /home/vgpnk/Projects/shokunin/mado-shokunin/quality/counters/c1-r54-errata-truth.py; then printf 'PRESENT\\n'; else printf 'ABSENT\\n'; fi
```

Exact output: `ABSENT`  
Exit: `0`.

Therefore the frozen invocation `python3 -I quality/counters/c1-r54-errata-truth.py --repo . --rev <rev>` and the second-table mutation against that implementation are **NOT RUN / absent**. No parser verdict for the current scored revision is claimed. No fixture or source file was changed by this seat.

## Scratch and write scope

Scratch created explicitly at `/fast/scratch/hyaku/mado-r54/R54W2Seat07` and removed before yield; remaining scratch: none. Only report written: `.ufo/waves/round-54/w2/R54W2Seat07.md`.

## Report trailer

- Attacked finding: C1 second-table laundering (whole-file scan versus canonical-table binding).
- Frozen evidence: `claims-frozen.md:19-30`; `registration.md:20-34,40-47`.
- Relevant w1 evidence: `w1/R54Seat05.md:173-222`, especially X-CTL-E at `:205-222`.
- Availability command/output/exit: shown above; `ABSENT`, exit 0.
- Frozen counter execution: NOT RUN / absent.
- Scratch remaining: none.
