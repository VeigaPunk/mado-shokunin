# ScribeShonen — holds: all four round-20 SHONEN lines stay `[~]` with pointers that resolve; no `[x]` is earned

Draft: `.ufo/waves/round-20/w2/ScribeShonen/shonen.md` (4 lines). Pointer check log: `.ufo/waves/round-20/w2/ScribeShonen/pointer-check.txt`. Nothing else written; the lane checkout was read-only (`git show`, `git log`, `git diff`, `git grep`, `sha256sum`, `sed`, `grep`).

## Findings

1. **No `[x]` in round 20.** The round-19 closure (`corpus/lessons/round-19-verifier-spotcheck.md`, `1f7f995`, integrator ClosureMadoR19) is a non-author record, but it edits no box and says "SHONEN boxes are **not all newly checkable from this review**" (`:143`). Its adjacency row (`:139`) is not a PROVINCE accuracy check. Round-20 SCORECARD/LOG/QUALITY/knowledge changes name no SHONEN scope: `git diff --stat 1f7f995 a4046a8 -- PROVINCE.md SHONEN.md corpus/knowledge/province-accuracy-selfaudit.md corpus/knowledge/executor-test-sufficiency.md corpus/knowledge/config-health-report-r3.md .ufo/waves/round-19/evidence/final` is empty; `grep -n -i shonen` over the round-20 SCORECARD section (`:1228` onward) and the round-20 LOG entry (`:1340` onward) returns nothing.

2. **Wave-1 draft has pointer defects; the w2 draft corrects them** (`.ufo/waves/round-20/w1/drafts/ScribeShonen.md`):
   - Box 1 cites `SKILL.md:572-577` as the probe registry rows. Those lines are the gate-registry intro. The rows are at `SKILL.md:603` (`mado-anchor-durability`) and `:608` (`mado-fresh-pins`).
   - Box 1 cites `SKILL.md:1853-1855` as the round-19 errata with walker 2.17.2. Those lines hold the "Append-only disposition" note only. The walker errata block is `SKILL.md:1884`–`:1892`.
   - Box 3's bare `evidence/final/*.txt` is replaced by the lane-relative `.ufo/waves/round-19/evidence/final/` (14 entries, `harm/` included; verified by `ls | wc -l`).

3. **Box 4 pointer is stale for the current PROVINCE text.** `PROVINCE.md:18` ("Round-19 refinement … theme/wallpaper route") was introduced by `df84807`, after the box-4 receipt's commit `eead56b` (round 5). `corpus/knowledge/province-accuracy-selfaudit.md` has sha256 `7c0a5820…` (matches the SCORECARD pin), so the receipt does not re-verify `PROVINCE.md:18`. This is a finding against the `[~]` pointer, not against the box mark.

4. **Box 4 attribution text is not in its pointer file.** `grep -c VER-M4B corpus/knowledge/province-accuracy-selfaudit.md` → `0`. The addendum at `:267` is labelled "M5-1". The verdict is quoted in-repo at `plans/round-5-record-draft.md:114`–`:117`, while the verdict file `/tmp/w5-ver-m4b-work/VERDICT.md` is ephemeral (SCORECARD row 5). The draft line says so.

5. **Box 2 record-length mismatch.** `corpus/knowledge/config-health-report-r3.md` is 1017 L at `a4046a8`. The MADO-R3-2 commit `f9f58c0` recorded 550 L; `3d9ba45` was 1005 L, `61eaa07` 1017 L, `df84807` 1013 L. The path resolves; the "550 L" figure in the records is out of date. Not resolved further [UNK].

6. **Conflicting status statements outside SHONEN.md (for the integrator; not edited).** `SCORECARD.md:28` ("Probation 4/4 `[x]` since round 5 (`SHONEN.md`)") and `LOG.md:295` / `:417` ("PROBATION COMPLETE 4/4") contradict `SHONEN.md:5,7,9,11` (all `[~]` since `7cd7f33`, 2026-10-15) and `SCORECARD.md:40`. The file is the authority, per `SKILL.md:700`–`:702`. The `[x]` text comes from the `c03c249`/`eead56b` closure that `7cd7f33` reverted.

## Evidence (sha256, read-only)

- `SHONEN.md` `c723b741…3e99` (12 L; same as `e629f73`).
- `corpus/lessons/round-19-verifier-spotcheck.md` `dcb7a913…fea0a0`.
- `PROVINCE.md` `1b25bb1e…7464b`.
- `corpus/knowledge/province-accuracy-selfaudit.md` `7c0a5820…` (345 L).
- `corpus/knowledge/executor-test-sufficiency.md` `4c34f884…`.
- `corpus/knowledge/config-health-report-r3.md` `fc089810…` (1017 L).
- Pointer check: 24 `PATH:LINE` pointers printed their expected line text and 7 path pointers exist (`pointer-check.txt`); 0 missing.

## Limits

- Pointers were checked for existence and for the quoted text only. I did not re-verify the claims behind SKILL decision tables, error patterns or checklists [UNK].
- The 67 round-19 wave-2 reports were counted, not read.
- The VER-M3 and VER-M4B verdicts were not reproduced; they are ephemeral. I did not confirm the round-19 closure's reviewer seats (GateOm10Check, TripwireCaseCheck, IncidentCheck, DiscernmentCheck) beyond the header statement.
- I did not run any gate, selftest, regression, measure, probe, or census command. No code was built or run, so no `/tmp` clone was made. No host, pacman, sudo, systemctl, hyprctl or compositor command ran.
- The lane working tree has an uncommitted change to `.ufo/waves/round-20/w1/reports/SimplifyRuleB.md` (not mine; left alone). `SHONEN.md` is clean.

## Installs

none
