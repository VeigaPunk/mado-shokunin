# R74ScribeC2 scoped findings

## Behavior and artifact

Drafted `guard-carrier-twohop-environ-alias-r74.md` in this directory for L1 application. It preserves source/verified-at/recheck frontmatter, cites S451/S452 and own-work receipts, describes both carrier implementations and dominance bounds, lists the new frozen case expectations, and attributes empirical counts to the exact counting command and committed receipt.

Axes: C2 operability; calibration/evidence fidelity; no-harm lane isolation.

## Evidence and gates

Read, without rewriting, the frozen declaration, committed C2 measurement, held baseline, existing round-73 entry, carrier function implementations, new case bodies, fetched source excerpts, and located source registry rows. The committed receipt records `population=20 readers=13 guarded=13 unguarded=0 controls=36/36 base_controls=32/36 verdict=TARGET_MET` at `b73db773aaf67c9b26c8cf1a4cd567dec3af11f4`. The assignment supplies rc 0; receipt text contains no rc field. No measurement, selftest, validator, build, or no-harm gate was executed by this seat.

Exact shell commands executed:
- `mkdir -p /fast/scratch/hyaku/mado-r74/R74ScribeC2` — successful, no output.
- `rmdir /fast/scratch/hyaku/mado-r74/R74ScribeC2` — successful, no output; owned scratch removed.

No installs or updates. No git/jj mutation, product-code edits, live host inspection, credential access, sibling writes, or runtime invocation.

## Findings and bounds

- Specialised `environ_alias_guard` handles local deletion cancellation, but generic env-named deletion cancellation remains unmodelled; the entry explicitly refuses a whole-classifier deletion guarantee.
- `environ-alias-rebound` has no guard store, so that frozen negative is not an isolated stored-guard/rebinding experiment.
- Line-order approximation, a single alias edge with no chains, and no value interpretation remain declared limitations.
- Source semantics are not treated as runtime or classifier-completeness evidence.

## Conflicting report paths (verbatim)

“Your ONLY write directory is /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-74/w1/<your name>/.”

“Report: write your scoped findings to .ufo/waves/round-74/w1/R74ScribeC2.md”

The latter path is outside the hard-bounded directory. Findings are instead written here; the requested knowledge-entry trailer path is inside the allowed directory. No outside-path write was attempted. Frozen declaration says “ONE v1 wave of 12 seats”; assignment says “ONE v1 wave (13 seats)”. Neither was changed or promoted into an executed seat census.

## Self-evaluation

Accuracy 4/5: source and receipt distinctions are explicit; exit status is assignment-provided, not independently recorded. Completeness 4/5: knowledge-entry requirements covered; conflicting outer findings path intentionally not written. Clarity 4/5: labelled M binds all empirical counts, at the cost of a lookup. Actionability 4/5: complete draft and exact recheck command; L1 still owns application and gates. Conciseness 4/5: caveats add length but prevent overstating the evidence. Overall 4.0/5. Improvements: L1 should resolve the outer report-path conflict and preserve the provenance distinctions when applying. Would the user agree? Expected yes, subject to that path decision.

## Out of scope

Applying or committing the draft, changing instruments/cases, judging, publishing, and rerunning gates belong to neither this scribe report nor its execution evidence.
