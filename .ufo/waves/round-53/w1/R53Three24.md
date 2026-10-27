# R53Three24 — cross-claim/source overlap scan

## Axes and evidence

Axes: operability (C1 instrument-ledger accountability counter) and coverage (C2 proposition-bound synthetic-dispatch repair). C1 and C2 target different artifacts and predicates; neither should receive credit for the other's success. This is a source-only synthesis, not an execution, validation, judgment, or admission.

[OBS] The frozen contract explicitly says C1 is “a bounded structural accountability check, not semantic proof” and C2 requires correcting P16–P18 against opened pinned bytes plus counter rejection/acceptance and independent source review (`.ufo/waves/round-53/claims-frozen.md:5-13`). It also says the claims are causally separate (`:13`).

[OBS] Routed r52 evidence exposes a shared governance hazard, not a shared technical predicate: Attack19 reports the integrated C1 counter was a new 78-line artifact unlike either tested W1 draft, and its naive row parser counted a fenced example as a real ledger row; its no-work control failed through empty/malformed row shape rather than the required self-pointer/context defects (`.ufo/waves/round-52/w2/Attack19.md:8-12,23-48,55-76`). Attack07 records C2 landed-counter parse/default-path failures, fabricated quote acceptance, and P16 splicing/P17 false subject/P18 false localization (`.ufo/waves/round-52/w2/Attack07.md:25-32,55-58,66-84`). These are historical reports, not assumptions about current bytes.

[OBS] Source registry already distinguishes the domains: S370–S373 register synthetic-dispatch source files/revisions and the path S370→S371→S372→S373 (`corpus/SOURCES.md:320-327`); README indexes the r52 knowledge entry as source-level only and explicitly excludes dispatcher execution/client receipt (`corpus/README.md:79-80`). QUALITY requires freeze-time smoke output, durable ephemeral oracle basis, and population agreement (criteria 49–51; `corpus/QUALITY.md:355-357`), and prohibits silent repair of inherited gaps without separate declared claims (criterion 52, `:358`).

## One bounded move

**Propose a single shared, pre-data artifact-identity manifest/checkpoint, not a merged counter:** for each C1/C2 predicate, register the exact production artifact path and SHA-256, the exact frozen counter path and SHA-256, the no-work/forgery fixture identities, and the proposition/source-pin evidence root (C2 only); require the pre-data smoke to emit the loaded identities alongside every verdict. The two counters remain independently specified, evaluated, and credited. This moves the common failure boundary—draft/landed artifact substitution—into a visible, falsifiable identity check without blending C1 structural-accountability into C2 source entailment. Keep source review independently responsible for quote truth; identity binding alone proves no semantic claim.

Why bounded: prior failures show counter and entry shape/path changed between tested drafts and landed bytes (Attack07), and integrated C1 counter differed from both tested drafts (Attack19). The manifest addresses this concrete cross-claim process overlap while preserving claim separation and preventing a C1 green from laundering C2 coverage (or vice versa). It does not alter frozen predicates or confer admission.

## Risks / contradictions

- The frozen claims call C1/C2 causally separate, while this proposal shares only a provenance/checkpoint mechanism. If “causally separate” is interpreted to forbid shared instrumentation/provenance, do not adopt; retain separate identity records with identical schema instead. This interpretation is unresolved by the claim text.
- Hash identity can make a bad artifact reproducibly identifiable; it cannot prove parser soundness, correct population, quote entailment, source correctness, or control load-bearing power. Exact controls still need distinct TARGET_MISSED demonstrations for the predicates they are meant to test.
- A checkpoint/manifest adds upkeep and can itself be stale or self-referential; counter must compare measured bytes to registered digest, and freeze receipt should be committed before data per QUALITY criterion 49. None of these steps were run here.
- Do not treat S370–S373's existing registry rows as independent source review: r52 Attack07 noted repeated source URLs / distinct-scope review concern; the current round's opened pinned bytes and fresh reviewer remain necessary.

## Verification proposal

For each claim separately, have the counter print loaded artifact/counter identities and exact revision; assert them against pre-data registered hashes. Then run frozen production and each committed negative control: expected production TARGET_MET and control TARGET_MISSED, with output showing the intended predicate—not merely malformed input—caused rejection. For C2 additionally verify quote bytes are contiguous and within the registered source pin, proposition attribution/localization is accurate, and corrected-entry acceptance versus old-entry rejection is bound to the exact landed entry. Source-truth reviewer must inspect pinned source independently. No such command was run by this seat; no current counter or landed r53 artifact was inferred.

## Trailer

- Report: `.ufo/waves/round-53/w1/R53Three24.md` (relative to `/home/vgpnk/Projects/shokunin/mado-shokunin`).
- Attacked predicate: cross-claim claim-separation and whether r52 failure classes justify a common provenance move. Exact source commands/output: none; this seat performed no commands against counters, fixtures, or source checkout. Evidence is read-only lane artifacts cited inline.
- No new external source opened; URLs/dates/quotes: not applicable.
- Scratch: `/fast/scratch/hyaku/mado-r53/R53Three24` created for permitted work; no fixtures or other files created. No installs, live reads, producer execution, tracked edits, git/jj mutations, or campaign tools.
