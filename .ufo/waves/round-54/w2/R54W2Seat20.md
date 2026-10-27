# R54W2Seat20 — C2 S375 quote/span

**Axes:** C2 coverage — source quote fidelity and precise pin-span correctness; report evidence reproducibility.

## Finding

Frozen contract S375 (registration.md:61–65) gives the quote `Difference between environment state before and after preparation is exported into systemd user manager (and D-Bus activation environment if reference D-Bus implementation is used)` and location `uwsm-0.27.1-README.md:117-118`. The exact pin contents at lines 117–119 are:

```text
117 - Difference between environment state before and after preparation is exported
118   into systemd user manager (and D-Bus activation environment if reference D-Bus
119   implementation is used)
```

The quoted words are an exact contiguous match when line wrapping/indentation is joined, but the full quote occupies physical lines 117–119, not 117–118. The frozen location omits the final line of the quote. This is a span precision defect, not evidence of quote fabrication. Since C2 clause (b) requires the located quote to occur verbatim in its pin, S375 as registered is not fully supported by its cited 117–118 span; it is supported by 117–119. A counter treating the location as an exact span should reject the real row; a counter only checking quote presence can admit it while overlooking the span mismatch.

## Evidence and prior wave

- Frozen contract: `registration.md:61-65`, specifically S375 at line 63; row requirements at 67–69.
- Frozen C2 predicate: `claims-frozen.md:57-65`; rows must have located quotes in their pinned sources.
- Pin observed: `.ufo/waves/round-54/fetch/uwsm-0.27.1-README.md:117-119` (read directly). The displayed wording shows the quote's final `implementation)` on line 119.
- Relevant prior report: `w1/R54Seat20.md:5-9, 44-50` concerns C1 and does not address S375 or this span; it reports a pin-only counterexample to C1 controls, not evidence about this C2 quote.

## Commands / limits

No existing pinned C2 counter is present in `quality/counters/` (the available C2 counters listed there are historical r51 and older), so the frozen command `python3 -I quality/counters/c2-r54-uwsm-entry.py --repo . --rev <rev>` was **NOT RUN / absent**. No fixture or predicate alteration was needed. No package/tool installation.

Pin inspection performed using the repository read operation for `.ufo/waves/round-54/fetch/uwsm-0.27.1-README.md:110-124`; it returned lines 117–119 as quoted above. This was a read, not a shell command; no exit status applies.

**Smallest safe correction:** if pre-data re-registration is permitted under the frozen honesty rules, record S375's location as `:117-119` in a new versioned registration. Do not edit the frozen registration after scoring. The quote itself should remain unchanged.

**Scratch:** `/fast/scratch/hyaku/mado-r54/R54W2Seat20` created as required; contained no fixture files and was removed before yield. No scratch remains.

**Report trailer:** `.ufo/waves/round-54/w2/R54W2Seat20.md` relative to lane root. No tracked lane changes, source/registration edits, git/jj mutations, producer execution, host reads, or tool updates.