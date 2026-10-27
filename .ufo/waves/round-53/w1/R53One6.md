# R53One6 — cross-claim/source overlap scan

Axes: operability (C1) and coverage (C2).

## Evidence

- Frozen claims say C1 is a structural ledger counter requiring exact population coverage, accountable non-self pointers, explicit selftest and TARGET_MET/MISSED controls; C2 repairs proposition grounding in an indexed r52 dispatcher entry with pinned source quotes and proposition bindings. The freeze explicitly says these are causally separate and forbids exploratory claim credit. (`.ufo/waves/round-53/claims-frozen.md:5-13`)
- Existing `quality/counters/c1-r51-ledger.py` describes its population as all files under `tools/` plus direct `quality/*.py` and `quality/counters/*.py`; its pointer check is basename-presence in a repo file, not proof of the target artifact's substantive accountability (`quality/counters/c1-r51-ledger.py:16-40`). This is useful C1 context, not evidence the round-53 counter passes.
- Prior routed C2 attack report documents that the draft counter's map completeness was one-directional (unmapped prose IDs pass), exact-text-only dedup misses paraphrase, and the committed artifact differed from the draft and accepted fabricated quote fixtures; the report states its own scratch-only fixture commands and limitations (`.ufo/waves/round-52/w2/Attack15.md:91-172`). Those are reported prior findings, not independently re-executed observations here.
- A notable cross-claim risk is the shared word “accountability/binding”: a row-to-path/basename relation for C1 cannot establish a C2 proposition-to-source-quote entailment, and a C2 proposition counter cannot establish C1's complete tool population. Treating one generic ledger counter as proof for both predicates would collapse distinct evidence obligations and conceal gaps.

## One bounded move

Keep the C1 and C2 checks explicitly orthogonal in the final evidence ledger: for each claim, record its own attacked predicate, exact command/output, input revision/digests, and controls. For C1, make pointer validity require a target distinct from the ledger/counter row's own artifact and retain per-population cardinality evidence; for C2, bind each proposition independently to a pin and quote and check both directions between proposition mentions and mapped rows. Do not reuse a single green summary as joint admission evidence. This improves operability by making the result auditable and coverage by preserving proposition-level mappings without harming either axis.

## Risks and verification

- Pointer self-reference avoidance may still accept a merely basename-containing but semantically irrelevant file; label C1 as structural accountability only, as the frozen claim already requires.
- C2 semantic distinctness and entailment are not mechanical facts; retain independent non-author source review and do not promote structural counter success into semantic truth.
- Verify on the exact registered final revision, not a draft or staged surrogate: production ledger TARGET_MET, no-work and every frozen forgery TARGET_MISSED; corrected C2 entry passes while the old entry fails, with all proposition/quote/pin bindings reviewed against opened source bytes. This is a proposal, not verification performed by this seat.

## Evidence boundary

Source-only read. No domain source URL was opened in this scan; no new source quote asserted. No live reads, producer execution, installs, or repository mutations. Attempted disk guard at `/home/vgpnk/.omp/agent/disk-guard` returned `command not found`; `df -h /fast/scratch` reported 596G available. No scratch artifacts created.

```
claim=C1 operability accountable instrument ledger counter; C2 coverage proposition-bound dispatch entry repair
attacked=C1 structural population/cardinality/pointer/selftest contract; C2 proposition-map completeness and quote/pin binding; cross-claim conflation risk
command=read frozen claims, quality/counters/c1-r51-ledger.py, and round-52 Attack15.md; observed anchors cited above
output=distinct predicates require distinct evidence; prior Attack15 reports C2 counter/landing defects but this seat did not reproduce them
source_url=none newly opened; no source URL/date/quote applicable
verdict=one bounded proposed move only; no admission judgment
report=.ufo/waves/round-53/w1/R53One6.md
scratch=/fast/scratch/hyaku/mado-r53/R53One6 (not created)
```