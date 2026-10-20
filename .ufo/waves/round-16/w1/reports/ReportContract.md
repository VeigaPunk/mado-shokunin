# ReportContract — mado round 16 six-section checklist (C1 / C2, closure pending)

Seat: ReportContract (scribe, read-only leaf). Wave: mado-r16-w1. Lane root: /home/vgpnk/Projects/shokunin/mado-shokunin. Baseline: 32c4fda873c9cb47a84c549b24b80ead2bcaa1ea.
Scope: draft the round-16 report checklist. No edits outside this file, no commits, no build/lint/test/gate/measure execution, no live probes, no package or service operations, no `~/.omp/agent/agent.db*` or credential access, no subagent dispatch. Message peers: none sent.

## 0. Axes and claims (named)

| Label | Axis | Declared move (SCORECARD.md round-16 block, ~L690–717) | Rubric state at baseline (as recorded, not re-measured here) |
|---|---|---|---|
| C1 | coverage / sourced documented routes | U1–U6 6/7, 8.5714/10 → U1–U7 7/7, 10/10 | 6/7 recorded at round-15 content `9ebd737` by the non-author closure (`corpus/lessons/round-15-verifier-spotcheck.md` §Claim re-check, L116) |
| C2 | operability / capability acquisition | absent (0) → demonstrated (1): bounded static action-plan classifier | 0 — `tools/mado-action-plan.py` does not exist in the tree at read time |
| — | expansion / quality / discernment | trend verdicts only, no scalar | per round-16 prompt §4; not pre-scored here |

Independence: C1 and C2 are causally separable (SCORECARD L711–712). Neither claim may be credited from the other's evidence. Hermetic-suite score (`tools/mado-verify.sh --selftest`) is NOT rewritten numerically by C2 (SCORECARD L708).

Trees observed at read time (not verified by execution):
- `corpus/knowledge/`: `covers:` tags present for U1–U6 only; zero `covers: U7` matches.
- `corpus/SOURCES.md`: highest id S052; S053, S054, S055 unused (reserved in the wave spec).
- `tools/`: only `mado-verify.sh` present; `mado-action-plan.py` absent.
- `.ufo/waves/round-16/`: `evidence/` and `w1/` only; `measure.py` absent.
- Working tree dirty with sibling/L1 edits (`git status`: `SCORECARD.md` modified, `corpus/QUALITY.md` +22 lines, one further file in a 3-file diff). Any measurement must bind to a committed revision, never to the working tree.

## 1. Section checklist — "Work performed"

Pass condition: opens by naming the declared claims (C1, C2) with target axes; then one bullet per work item, each with path:line, command output, or commit hash. Unexercised surfaces stated as retained unknowns.

- [ ] C1 item: U7 Waybar module text observation boundary note. Evidence: path of new `corpus/knowledge/*.md` with first 15 lines containing `source:`/`verified-at:`/`recheck:` provenance trio, `covers: U7` exactly, four level-2 headings in order: `## Producer contract`, `## Renderer boundary`, `## Safe observation`, `## Unexercised rendering`; `[UNK]` inside the final section. Must state "not rendered verification".
- [ ] C1 item: source opening for S053 (Waybar 0.15.0 `man/waybar-custom.5.scd`, tag path raw.githubusercontent.com/Alexays/Waybar/0.15.0/) and S054 (`src/modules/custom.cpp`, same tag). Each: exact URL, byte count, SHA-256 of fetched bytes, one ≤25-word located quote. Quote must be opened this round.
- [ ] C2 item: `tools/mado-action-plan.py` with `--selftest`, `--plan PLAN --policy POLICY`, `--frozen DIR` modes. Evidence: committed path, commit hash, self-invocation assertion count, exit codes for each mode, negative actual-incident-shaped plan result, persisted paused-policy file path.
- [ ] C2 item: frozen run directory and digest binding (sha256 of classifier + policy + plan fixtures).
- [ ] Bounded-claim statement for C2: "grades declared JSON actions; neither intercepts tools nor repairs the host." Must appear verbatim-equivalent.
- [ ] Host-pause statement: all pacman transactions paused host-wide; no `-Sy`/`-Syu`/`-U`/`-R`; no downgrade or service restart this round. Any `pacman -Sp` plan is out of scope this round (only operator-authorized future install may use real `-Sp --print-format '%n %v'`).
- [ ] Process-debt disclosure carried forward: round-15 `ReviewLibinput` `hyprctl version` call (per round-15 closure L274–277). Round 16 must disclose any live call it makes; default expectation is none.

## 2. Section checklist — "Landed changes"

Pass condition: each change tied to a LOG.md entry and to the commit hash carrying it.

- [ ] LOG.md entry per landed file (L1 owns LOG.md).
- [ ] `corpus/SOURCES.md` rows S053, S054 added with tier and status; S055 reserved (closure own-work safety) — row content owned by L1, not this seat.
- [ ] `corpus/knowledge/` U7 note committed; `corpus/README.md` U7 entry (L1).
- [ ] `tools/mado-action-plan.py` committed (C2).
- [ ] `corpus/QUALITY.md`: append-only criterion superseding criterion 20 (L72 currently: "Before a future tool install, obtain `pacman -Sp …`") in response to R15-V1/V2. Existing criterion text must remain; superseding is append-only.
- [ ] `SKILL.md`: current safety instruction (SKILL.md ~L483 "Round-16 superseding instruction", present in working tree at read time; committed status not established by this seat).
- [ ] Commit `round-16` in lane repo; fleet-repo report committed separately.
- [ ] Tool installs/updates record: "Tool installs/updates: none" unless an install occurred. Round prompt and host pause forbid installs this round; any install must be listed as tool, version, channel, reason.

## 3. Section checklist — "Before → after measurements"

Pass condition: one per claim (C1, C2), each with counting command and measured commit. Before = `32c4fda…` (baseline). After = integrated committed revision. Both measured by L1 once after integration; seats do not run measurements.

- [ ] C1 before: `python3 .ufo/waves/round-16/measure.py 32c4fda873c9cb47a84c549b24b80ead2bcaa1ea` → must print U1–U6 set and 6/7; expected from round-15 closure = 8.5714 — but re-measure, do not copy. NOTE: `measure.py` does not yet exist.
- [ ] C1 after: same command at integrated revision → must print U1–U7 set, 7/7, 10.0000 only if provenance trio, reciprocal S053/S054 mined joins, exact four headings and `[UNK]`-in-final-section facets all pass.
- [ ] C1 counter-caveat: a `covers:` marker count alone is insufficient (round-15 closure L98). Report the facet checks separately from the marker count.
- [ ] C2 before: `tools/mado-action-plan.py` absent → capability 0. C2 after: `--selftest` pass, `--plan/--policy` exit codes, `--frozen DIR` digest match at the integrated revision. Capability 0→1 only with all four present.
- [ ] Harm watch: `bash tools/mado-verify.sh --selftest` count reported before/after (last recorded in SCORECARD ~L650–653: 372/372, round-15 content). Round-16 must not drop it; any change is reported as-is, not as a score.

## 4. Section checklist — "Sources & frontier"

Pass condition: `SOURCES:` line naming the state; census command run at round start and end with outputs and exit codes pasted; exit 0 at end.

- [ ] Start census: `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin mado` — output and exit code (L1 runs once after integration; seats do not). Historical duplicate warnings (S030, S042, S045) remain visible; not a warning-free verdict.
- [ ] End census: same command, exit 0 required.
- [ ] Rows before→after: 52 → 54 expected if S053/S054 land (S055 is reserved; do not count it unless its row lands).
- [ ] Rows touched old→new logged in lesson.
- [ ] At least one claim cites an `S###` row opened this round with a ≤25-word quote (S053 or S054 satisfies).
- [ ] Mined-mistake entry for round 16 in `corpus/lessons/round-16.md ## Mistakes` (class · evidence pointer · captured-by · fix). Note: `corpus/lessons/round-16.md` does not exist at read time; checked by this seat.
- [ ] Frontier rows advanced: U7 (C1) and the action-plan gate (C2). Source-era/sibling boundary: no sibling repo edits.

## 5. Section checklist — "Trend verdicts"

Pass condition: exactly three verdicts (expansion, quality, discernment), each one of improved / harmed / unchanged / unprovable-but-better, with evidence; no scalar.

- [ ] expansion: evidence = U7 note admitted + reciprocal joins. Expected candidate verdict if C1 verifies: improved. Not pre-decided by this seat.
- [ ] quality: evidence = C2 classifier + QUALITY criterion. Candidate verdicts depend on C2 result and on whether the host-safety harm from round 15 (R15-V1) remains unresolved. Round-15 closure marked quality harmed on that event; do not silently reset.
- [ ] discernment: evidence = this round's outside/non-author spot-check. `unprovable-but-better` requires a named non-author reviewer and reasons. None is named at read time → cannot be used by the lane itself.

## 6. Section checklist — "SHONEN"

Pass condition: one line per SHONEN.md box (currently four), all `[~]` at read time.

- [ ] Box 1 (SKILL decision tables/error patterns/checklists/cited sources): keep `[~]` unless a named non-author verifier confirms. Pointer: `corpus/knowledge/executor-test-sufficiency.md`.
- [ ] Box 2 (end-to-end domain task logged): keep `[~]`. Pointer: `corpus/knowledge/config-health-report-r3.md`, LOG.md round 3. Round-16 U7 is source-only: not an end-to-end desktop task.
- [ ] Box 3 (executable without oral context): keep `[~]`. Pointer: `corpus/knowledge/executor-test-sufficiency.md`.
- [ ] Box 4 (no cross-domain bleed): keep `[~]`. Pointer: `corpus/knowledge/province-accuracy-selfaudit.md`, `corpus/knowledge/output-colour-boundaries-r14.md`.
- [ ] `[x]` for any box requires a named non-author verifier: none exists → no `[x]` this round.

## 7. Findings (observations, not fixes)

F1. No U7 entry exists yet (`covers: U7` count = 0). C1 is open.
F2. S053/S054/S055 unused in SOURCES.md; highest id S052. Reserved-id collision check needed before L1 writes rows.
F3. `tools/mado-action-plan.py` and `.ufo/waves/round-16/measure.py` both absent at read time. C2 and the C1 counter are open.
F4. Working tree dirty (SCORECARD.md and corpus/QUALITY.md at least). Any measurement must be made at committed revisions; `measure.py REV` takes a revision argument.
F5. The round-15 closure independently reproduced C1 6/7 at `9ebd737` (not at `32c4fda`); baseline must be re-measured at `32c4fda`.
F6. `corpus/lessons/round-16.md` does not exist; mined-mistake requirement pending.
F7. Round-15 process debt (`hyprctl version` in ReviewLibinput) is disclosed, not repeated; round 16 must not repeat it.

## 8. Gates (this seat)

- Read-only; no gate, selftest, measure, census, or verification executed by this seat.
- Sources consulted (read-only): `corpus/lessons/round-15-verifier-spotcheck.md`, `.ufo/waves/round-16/w1/spec.json` and `dispatch.json` (ReportContract item and context), `SCORECARD.md` round-16 block, `.ufo/prompts/mado-round-16.md` §4, `.ufo/waves/round-15/w1/reports/ReportAudit.md` §2 (six-section precedent), `SHONEN.md`, `corpus/QUALITY.md` criterion 20, `SKILL.md` pacman lines, `/home/vgpnk/.omp/agent/RULES.md`.

## 9. Touched surfaces

- Written: `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-16/w1/reports/ReportContract.md` (this file only).
- Not touched: all lane docs, corpus, tools, SCORECARD/SHONEN/LOG, fleet repo, sibling lanes, `~/.omp` state.

## 10. Out-of-scope items

- Writing the fleet report `.ufo/reports/round-16/mado.md` (L1).
- Any host pacman planning (`pacman -Sp`), install, update, downgrade, service or compositor action. Host recovery is operator-owned.
- Any live probe (compositor, input device, screenshot, command producer).
- Any closure verdict: independent closure is pending and is not performed by this seat.

## 11. Closure status (independent, pending)

- Closure: NOT RUN. Requires a non-author integrator (the round-15 precedent is the hyaku closure, `corpus/lessons/round-15-verifier-spotcheck.md`).
- Required for admission: integrated commit; L1 single verification pass (census, measure at 32c4fda and integrated revision, selftest, file-plane gate); a non-author reviewer reproducing C1 counts and C2 mode exits; disclosure of any sibling-owned file touched.
- Seat verdict: checklist drafted; no claim admitted, none credited.

Tool installs/updates this seat: none.
