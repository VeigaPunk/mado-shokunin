# mado-shokunin — Promotion checklist

Promotion to shokunin requires all of:

- [x] SKILL.md contains real decision tables, error patterns, checklists, cited sources
  MADO-R3-4 (non-author executor lane) — corpus/knowledge/executor-test-sufficiency.md: executed the SKILL's checklist/tables/scale end-to-end as its only domain source; verdict "Sufficient, end-to-end, against the version read"; SKILL sha `ef4c29e3374c…` (396 L) frozen at the round-3 commit
- [~] At least one end-to-end domain task executed and logged in LOG.md
  corpus/knowledge/config-health-report-r3.md (MADO-R3-2 — full-plane health pass, divergence register F1–F10, operator recommendations §7) + LOG.md round-3 entry; counts re-verified by MADO-B4 (`/tmp/mado-b4-r3b/verify.log`)
- [x] Instructions executable by an agent without oral context
  MADO-R3-4 (non-author executor lane) — corpus/knowledge/executor-test-sufficiency.md: SKILL.md sole domain source; per-step sufficiency classes over steps 0–9; carried gaps (jq unnamed, block-scope namespacing) resolved in-pass and reported to the SKILL lane
- [~] No cross-domain bleed (PROVINCE.md still accurate)
  corpus/knowledge/config-health-report-r3.md §1 — every PROVINCE-declared surface re-verified live read-only this pass, no cross-domain claim absorbed; lane-asserted mark (no auditor verdict recorded in-repo this round)
