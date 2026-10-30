# R56W3ExecProbeC3NewRows

## Attack and method
Attacked C3-v2 registry additions in both states requested: newly queued S396 with `used-by` `—`, and with `used-by` `corpus/lessons/round-56.md`. Read the frozen predicates in `claims-frozen-v2.md` and `registration-v2.md` first. Constructed two scratch repositories from `git archive 0f3a54361a9824484d0801679ceb1fd8ac7c32e1`, appended the census-valid row inside `## Registry`, committed each as `ctl@ctl`, and fetched the frozen C3 base commit object (required for the counter's lost-pairs check). Ran the counter and sources census validator against each committed revision.

## Evidence / results
Exact commands, output verdict lines and return codes are in `receipts/c3-newrows-a2.txt`.

- Case A: counter returned `entries=71 rows=333 missing=0 extra=0 dangling=0 conflict=0 stale=0 lost=0 exempt=24 verdict=TARGET_MET`, rc 0. Census validation returned `file ok <registry-path>`, rc 0.
- Case B: counter returned `entries=71 rows=333 missing=0 extra=0 dangling=0 conflict=0 stale=0 lost=0 exempt=24 verdict=TARGET_MET`, rc 0. Census validation returned `file ok <registry-path>`, rc 0.

The case-B input is the requested S396 row with `used-by=corpus/lessons/round-56.md`. It did not produce `extra=1` or `TARGET_MISSED`, contrary to assignment's expected behavior and C3-v2 definition of `extra` for any used-by path outside ENTRIES.

## Defect
- **Blocking the claim (for the requested converse probe):** a queued row carrying the non-entry path `corpus/lessons/round-56.md` is accepted as TARGET_MET instead of being counted extra. Input: case B registry at revision `593ecce9efca2979d6f95b8d83b952881e292e6f`; exact counter output in receipt. Both registry variants pass census validation. The required two-way behavior is therefore falsified; S396/S397 should not be landed with a non-empty invalid used-by on the basis of this probe. Case A supports landing a queued row with an empty used-by, as requested.

## Limits / cleanup
No lane files or external state were modified. Scratch directories were removed before yield. No build, lint, tests, formatter or other verification was run. Census warnings W01/W04 from existing rows appeared in full output; the decisive census verdict was file-ok with rc 0. Deliverables: `.ufo/waves/round-56/w3/R56W3ExecProbeC3NewRows.md` and `.ufo/waves/round-56/w3/R56W3ExecProbeC3NewRows/receipts/c3-newrows-a2.txt`.
