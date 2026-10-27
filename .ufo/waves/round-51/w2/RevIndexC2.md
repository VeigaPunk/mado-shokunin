# RevIndexC2 — C2 index falsification

## Deliverables
- `w2/RevIndexC2/index-check.md` — base/data index counts, fidelity-gate output and independent README row assessment.

Report: `.ufo/waves/round-51/w2/RevIndexC2/index-check.md`

## Finding

**PASS — frozen C2 index clause (a) only.** `quality/check-index.py` reports base `indexed=66/66 missing=0 dangling=0 duplicates=0` and data `indexed=67/67 missing=0 dangling=0 duplicates=0`, both coverage 10/10. The data `quality/check-index-rows.py` reports `rows=67 errors=0 warns=3`; warnings concern old unrelated rows. Independent inspection of `corpus/README.md:78` finds the new row names the dispatcher execution surface, cites S364–S369 and held bind/parser grounding, with no apparent bad wording or source-ID mismatch. Full evidence and commands are in the seat deliverable.

## Residual risk / verification gaps

The index checks do not prove frozen C2 clauses (b)–(d), nor semantic correctness of the entry. This assignment did not replay the C2 frozen counter. No LSP device/server was available through the provided tool inventory; evidence here is direct checker output and row text inspection, not semantic LSP proof.
