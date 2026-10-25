# RevShonen — SHONEN evidence-pointer check (round 35, wave 1)

Seat: RevShonen (leaf member, no dispatch). Base checked at HEAD
`19e4ab3171c1540c40d6b12097745af98053b07d` (round-35 freeze). Inputs:
`SHONEN.md` (12 lines, last touched by `7cd7f33`), `corpus/lessons/round-34.md`,
`git show --name-only 19e4ab3`, `git status --porcelain`.

## Findings — all four pointers resolve; all four stay `[~]`

| Box | Pointer | Resolves | Author-asserted | Mark stays |
|-----|---------|----------|-----------------|------------|
| 1 SKILL.md real tables/patterns/sources | `corpus/knowledge/executor-test-sufficiency.md` (MADO-R3-4) | YES — file present, last commit `f9f58c0`; content is the lane's own no-oral-context executor-test note | YES — lane-authored receipt; the SHONEN line itself says outside-lane verifier independence "is not established by the inherited record" | `[~]` |
| 2 ≥1 end-to-end domain task logged | `corpus/knowledge/config-health-report-r3.md` + LOG.md round 3 (VER-M3) | YES — both present; the report exists (§F register, 560+ lines); LOG.md:159-167 logs the round-3 dispatch and LOG.md:294 records VER-M3 closing box-3 | YES — the e2e task and the VER-M3 closure are lane-generated; SHONEN line names no new end-to-end task or outside-lane verification since fleet round 1 | `[~]` |
| 3 Instructions executable without oral context | `corpus/knowledge/executor-test-sufficiency.md` (MADO-R3-4) | YES — same file as box 1; its assignment line (`:3-7`) records "an executor lane with no oral context reads SKILL.md only" | YES — the executor was a lane-dispatched subagent; SHONEN line explicitly: "dispatched subagents do not satisfy the current outside-lane promotion rule" (consistent with AGENTS.md: a subagent the lane dispatched is still the lane) | `[~]` |
| 4 No cross-domain bleed (PROVINCE.md accurate) | `corpus/knowledge/province-accuracy-selfaudit.md` round-5 receipt (VER-M4B); PROVINCE.md | YES — selfaudit exists (claims C2–C7 all HOLDS); its appended 17:07Z block is the VER-M4B closure re-running the §8 commands; `PROVINCE.md` present | YES — VER-M4B is a lane-round receipt; the SHONEN line calls PROVINCE.md "the read-only boundary, not a fresh outside-lane approval" | `[~]` |

## Round-35 changes vs the pointers

- `git show --name-only 19e4ab3 | grep -v '^\.ufo/waves/round-35'` → empty
  (exit 1): the only round-35 commit touched nothing outside
  `.ufo/waves/round-35`. All pointer paths are byte-identical to their last
  commits; `git diff HEAD` on the five cited paths is clean.
- Round-35 wave-1 output so far is untracked scratch/reports under
  `.ufo/waves/round-35/` — no pointer path rewritten, moved, or deleted.
- `corpus/lessons/round-34.md` does not cite, amend, or supersede any SHONEN
  pointer; its frozen-counter and assimilation claims are orthogonal.

## Divergence worth naming (no pointer broken, but the ledgers disagree)

`LOG.md:294-295` and `LOG.md:417` still narrate "box-3 CLOSED (VER-M3)",
"box-4 CLOSED by VER-M4B — PROBATION COMPLETE 4/4". Current `SHONEN.md`
(last written by `7cd7f33`, the fleet-migration seed) downgraded all four
boxes to `[~]` because every verifier id (MADO-R3-4, VER-M3, VER-M4B) is a
lane-authored receipt, and the promotion gate requires non-author review —
the same rule stated in AGENTS.md ("a subagent the lane dispatched is still
the lane"). The LOG entries are historical narration, not a live mark
surface, so this is a retained-divergence, not a defect to sweep; noting it
because a reader grepping LOG.md could conclude 4/4 `[x]`.

## Verdict

4/4 pointers resolvable to committed bytes; 4/4 author-asserted; 4/4 `[~]`
under the promotion gate. Promotion remains blocked on outside-lane
verification, not on missing evidence.
