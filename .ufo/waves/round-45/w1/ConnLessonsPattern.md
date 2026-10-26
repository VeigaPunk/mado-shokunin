# Seat ConnLessonsPattern — round 45 w1 report

Task: pattern across the lane's last six closures — which routed defect classes recur. Read `corpus/lessons/round-{39,40,41,43,44}-verifier-spotcheck.md` §6 and the lessons' `## Mistakes`, plus round-45 `registration.md` (freeze 22a8ded), `corpus/QUALITY.md` (criteria 65–84), `SKILL.md:343` (rule 4), `considerthese/2026-10-26.md` (proposal 1). Full deliverable: `.ufo/waves/round-45/w1/ConnLessonsPattern/patterns.md`.

## Findings (brief)

1. **44 mistakes / 5 lessons, 27 routed items / 5 closures.** Mistake counts per lesson (grep `^\*\*M[34][0-9]-`): 2/6/18/9/9 (rounds 39/40/41/43/44; round 42 had no lesson — M43-4).
2. **Six classes.** (A) predicate health — holes, post-scoring repair, vacuous clauses (~16 hits, the top class); (B) evidence pointers — existence-at-revision, tip receipts, computed locators (~14); (C) counts without recompute (~5); (D) driver/wave-tree hygiene (~5); (E) session material/privacy (1 routed, no M row); (F) supersession/premise wording (~3–4).
3. **Freeze addresses:** seeded counter (C1 default seed 45 → R44 D4, M41-15, M41-2); locator width bound ≤30 (C2 clause j → R44 D5); do-nothing/forged controls rejected (C2, 9 rejects + P → M41-14, M44-8); C1 clause r no-compositor-PATH (→ M40-4). Not frozen: D2 (SCORECARD after-values), D3 (tip receipts), D6 (supersession), D7 (errata); D1/proposal 1 planned as criterion+gate. Observation: C1 selftest floor ≥30 is below the r44 precedent (80, M44-6).
4. **Three criteria proposed (next numbers 85–87):** 85 open-predicate residuals must carry a kill rule and a demonstrated fail (backing M44-6, M41-14, M43-8); 86 tip receipts name the closing tip, extending 69 (backing M44-7, M41-4, routed R40 §6:2, R43 D7, R44 D3); 87 session material stays shape-only in tracked bytes (backing none — no M row exists; evidence round-44-verifier-spotcheck.md:98, SKILL.md:343, considerthese proposal 1).
5. **Secondary candidates:** M44-1 reason-coverage (lesson names it first candidate), M44-5 count-recompute, M43-9 INF-universal Basis rule.

## Evidence
- Locators for every cited M row and routed item are inside patterns.md §2/§4; key ones: M44-6 round-44.md:156; M44-7 round-44.md:171; M44-8 round-44.md:178; M41-4 round-41.md:107; M41-14 round-41.md:224; M43-1 round-43.md:113; M43-8 round-43.md:183; M39-1 round-39.md:94; §6 sections at round-39-verifier-spotcheck.md:91, round-40:89, round-41:75, round-43:95, round-44:96; R44 D1 at round-44-verifier-spotcheck.md:98; freeze claims at registration.md:21-22, :46-47, :64-67.

## Tools installed
None. Scratch: none created (no writes outside the seat dir and this report).
