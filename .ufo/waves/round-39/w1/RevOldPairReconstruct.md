# RevOldPairReconstruct — round-39 w1 seat report

Seat: RevOldPairReconstruct (leaf; no subagents). Task: reconstruct the old frozen-pair
behavior (C1 narrative). Date 2026-10-25. All reads were read-only git (`show`/`log`/
`diff`/`ls-tree`/`rev-parse`/`cat-file`); no lane git/jj mutation, no installs.

## Findings (evidence-backed)

1. **Old frozen pair identity.** Freeze commit `58e55ec`; frozen manifest
   `.ufo/waves/round-38/controls/manifest.json` sha256 `14c49d9f…` (byte-identical to
   receipt `.ufo/waves/round-39/receipts/manifest-frozen-r38.json`); frozen c1 counter sha
   `41eb2419…`, c2 counter sha `194a45c6…` (unchanged to HEAD).
2. **Why 18/19.** The `c1-duprow` control in the old frozen manifest writes the duplicate
   S189 row with `{"op":"append",…}` → gate `_append` (check-r38-discrimination.py:76-77,
   128-130) puts it at EOF of `corpus/SOURCES.md` (line 458, after `## Leads (unopened)`),
   outside `## Registry` (lines 9-220). The counter's `section()` (c1-r38-event-ground.py:
   122-132) stops at the next `## ` heading, so `registry_rows()` never sees the dup;
   clause `j` (line 226) then passes with the single held row → control observes
   `TARGET_MET` instead of expected `TARGET_MISSED` → `correct=18/19`, the sole failure
   (receipt `c1-redbefore.txt` lines 5, 20).
3. **Repaired control.** op `py` splices the dup immediately after the `| S217 |` row
   (inside `## Registry`; @base line 219), so the parser sees two rows → `j=0` → MISSED.
   Round-39 re-frozen manifest `.ufo/waves/round-39/c1/manifest.json` sha256 `96965518…`
   is a byte copy of the repaired base manifest.
4. **Cross-pairing** (from round-38 replay evidence, f551b70/e072af6): frozen counter ×
   frozen manifest = 18/19; either counter × landed manifest = 19/19; the `859d0cf` counter
   patch (clause-c uniqueness) is verdict-no-op for this control — the failure scope is the
   manifest write placement alone.

## Artifacts written (only files this seat wrote)

- `narrative.md` — full line-level pointer narrative (in `.ufo/waves/round-39/w1/RevOldPairReconstruct/`).
- This report.

## Verification note for main agent

Re-run for C1 at the freeze commit:
`python3 -I quality/check-r38-discrimination.py --c1 quality/counters/c1-r38-event-ground.py --c2 quality/counters/c2-r38-eventq.py --manifest .ufo/waves/round-39/c1/manifest.json --rev <freeze commit>` → expect `controls=19 correct=19/19 verdict=TARGET_MET`, exit 0.
