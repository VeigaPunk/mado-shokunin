# ReviewRepairsPlan — round-25 routed defects and carry items vs the round-26 w1 plan

author: MadoR26.ReviewRepairsPlan (reviewer, leaf — no spawns, no edits; this report is the only file written)
date: 2026-10-23 · lane: mado-shokunin · wave: round-26 w1 (pre-data)

## Verdict

**VERDICT: mapped — 8/8 routed defects (spot-check §7) and 2/2 actionable carry items have registered w1 owners (w1-spec.json = w1-run.json registry, 40/40 spawned); 2 mapping gaps found (F1 medium, F2 low) and 2 carry items intentionally ownerless (H2, QUALITY 33–35 survivors). `corpus/lessons/operator-*.md` matches zero files, so that check is vacuous; the one operator rule cited in-corpus (the "leg rule", M25-5) is not reflected in QUALITY.md or SKILL.md.**

## Method (read-only)

Read `corpus/lessons/round-25-verifier-spotcheck.md:198-212` (§7 items 1–8), `corpus/lessons/round-25.md:85-90`
(`## What to carry`) and its Mistakes rows (`:18-23` raw), `.ufo/waves/round-26/registration.md` (`## Repairs …
:97-104`, host-safety section, `## Controls`), `.ufo/waves/round-26/w1-spec.json` (all 40 item prompts) and
`.ufo/waves/round-26/w1-run.json` (`registry.members` keys = 40 names, `counts.spawn=40 total=40`). Anchored
claims with greps/reads of `harness/oracle.py`, `c1/count.py`, `c2/count.py`, `corpus/QUALITY.md` (324 lines),
`SKILL.md`, `SCORECARD.md:1695-1710`, `round-25/registration.md:85`, `round-25/evidence/c1-before-v4-41cc04c8.txt`
(tail), fleet `.ufo/l0-questions.md`. No counter, gate or selftest executed (host-safety rule); no Hyprland started.

## Table 1 — routed defects (spot-check §7) → plan

| # | Routed defect (anchor) | Repairs row | w1 owner(s) | Owned | Evidence / state |
|---|---|---|---|---|---|
| 1 | M25-2 label-free case paths (`round-25-verifier-spotcheck.md:200-201`) | R1 (`registration.md:99-100`) | K1LabelKeyed, K2LabelKeyed | yes | Repair already landed in bytes: `harness/oracle.py:21-22` ("every case tree lives in a directory with a random mkdtemp name … cases are run in a shuffled order"), `:144` (`mkdtemp(prefix="m26o-")`), `:230-234` (tool tree read-only at fixed `/snap/home`, source dir random — M25-2 named in the docstring). Able-to-fail credit still awaits the two label-keyed controls' red receipts (round-25 lesson `:22`: "the fix is not credited until shown able to fail"). |
| 2 | surviving counter mutants `skip-oracle-check`, `embed-threshold-1000`; drift-fault witness + embed fixture; "describe `embed_hits` as a plaintext audit only" (`:202-203`) | R2 (`registration.md:100`) | CounterSelftest (witnesses + fixtures + red runs); MutC1Counter, MutC2Counter (independent mutant attacks) | **partial — see F1** | CounterSelftest prompt covers: BASE-twice disagreement → exit 2 `ORACLE_UNSTABLE` (drift-fault witness), 40-char base-table arg → embed_hits≥1 (embed fixture a ≥1000 threshold misses), plus red runs against mutated scratch counters. The third clause of the routed defect (describe embed_hits as a plaintext audit only) is in no prompt and in no artifact text: grep `plaintext\|audit` over `registration.md`, `c1/count.py`, `c2/count.py` → no prose hit; `c2/count.py:34,170-174` are code (`EMBED_MIN=12`, `EMBED_HIT` prints); `registration.md:67-68` states only the target `embed_hits=0`. |
| 3 | population-equality clause → QUALITY 36 or successor criterion 37 + its check (`:204-205`; M25-4) | R3 (`registration.md:100-101`) | Q37Population | yes | Writes `round-26/quality/check-population.py` + `population-fixtures/` (green 41-CASE, red: CASE removed / denominator changed / registration total changed) and drafts the criterion-37 text in its report — QUALITY.md itself is not edited by the seat (integration step; QUALITY.md is 324 lines, still ends at criterion 36). |
| 4 | M25-3 fixtures killing the surviving `check-control-receipts.py` mutants + per-counter-version receipt filter (`:206`) | R4 (`registration.md:101-102`) | Q36Fixtures | yes | Successor checker at `round-26/quality/check-control-receipts.py` (old file stays) with `--counter-sha SHA`, fixtures under `round-26/quality/q36-fixtures/` for the five named survivors (non-strict `<`, ignore shapes, newest receipt, any `.md`, `updatedAt`), synthetic git repos under `/fast/scratch/hyaku/mado-r26/q36/`. |
| 5 | R8: `round-25/registration.md:85` claims hardened MutCheckRegOrder/MutCheckReceipt checks never landed; append a correction; QUALITY 33–35 survivors stay open (`:207-208`) | R5 (`registration.md:102-103`) | R5R6Corrections (part 1) | yes | False line verified in place: round-25 `registration.md:85` "Hardened checks for the named survivors (MutCheckRegOrder, MutCheckReceipt) under `round-25/quality/`, old checks kept." Seat drafts the dated correction paragraph (append-only, no edit). |
| 6 | bind tool: `{{…}}` arithmetic left literal; `source`/`$VAR` reads outside `--home` (`:209-210`) | R7 (`registration.md:104`) + C2 claim | C2 (w2 data) + this wave's controls K2BaseTool, K2DoNothing, K2BraceStrip, K2NaiveEval, K2EmbedReplay, K2LabelKeyed | yes | `{{…}}` is exactly claim C2 (`registration.md` "## C2"; outside-home stays a stated limit per R7, already documented in PROVINCE in round 25). w1 contributes the control receipts and CritC2Design; the resolver work is w2 and outside this wave's bounds. |
| 7 | C2 ledger `:1409`/`:1410` no second derivation; `:308` command cell not lane-relative (F2) (`:211`) | — none (see F2) | Rc1409, Rc1410 | yes | Re-runs of `python3 .ufo/waves/round-20/a2/a2-guards.py 41cc04c8 --fixtures-rev 6a7d9ca` in sandbox clones detached at `41cc04c8`, compared with the ledger cells and errata F5. The `:308` half is already discharged: errata F2 is appended at `SCORECARD.md:1705-1707` ("row `:308`'s command is the fleet script … not a lane-relative `scripts/sources-census.sh`"). |
| 8 | `evidence/c1-before-v4-41cc04c8.txt` carries no `exit=` line (`:212`) | R6 (`registration.md:103`) | R5R6Corrections (part 2) | yes | Verified: the receipt's last lines are `V3_MODEL_AGREE 41/41 …` / `PRED-C1 (v4) cases_pass=0/41 embed_hits=0 verdict=TARGET_MISSED` — no `exit=`. Seat drafts a note for the end of the round-26 lesson deriving exit 1 from the counter's code (receipt not rewritten). |

## Table 2 — `## What to carry` (round-25.md:85-90) → plan

| Carry item (anchor) | Round-26 owner | Owned? |
|---|---|---|
| "A counter that runs a tool in a sandbox must hide which case is running (M25-2)" (`:87`) | R1 (landed in `harness/oracle.py`) + K1LabelKeyed / K2LabelKeyed to show it can fail | yes |
| "QUALITY 36's check needs mutant-killing fixtures and a per-counter-version receipt filter (M25-3)" (`:88`) | Q36Fixtures | yes |
| "Carried, unchanged: H2 (L0 `.ufo/l0-questions.md:103`)" (`:89`) | none — operator-held L0 question (found at fleet `.ufo/l0-questions.md`, the mado round-23 precision-harm H2 row); deliberately not routed to the lane | no, by design |
| "QUALITY 33–35 check survivors (MutCheckRegOrder, MutCheckReceipt) were not hardened this round" (`:89-90`) | none hardens them this round; only the `:85` correction (R5R6Corrections) records the truth | no hardening owner — matches the routing ("stay open", spot-check `:208`); should re-enter a later plan |

## Findings (routed items with no owner / mapping gaps)

- **F1 (medium) — routed defect 2's "describe `embed_hits` as a plaintext audit only" has no owner.** The clause
  (spot-check `:202-203`) is absent from R2's one-line disposition (`registration.md:100` names only "drift-fault
  witness and embed fixture"), from the CounterSelftest prompt, and from all artifact prose: grep for
  `plaintext|audit` over `registration.md`, `c1/count.py`, `c2/count.py` returns no descriptive sentence
  (`c2/count.py:34,170-174` are code; `registration.md:67-68` only sets the target). Cheapest fix inside the round:
  one append-only sentence in CounterSelftest's receipt or the round-26 registration note/lesson stating that
  `embed_hits` is a plaintext substring audit of tool bytes, not a provenance proof (the round-25 spot-check §2.1
  already treats it that way after the `"resize" "windowpixel"` split-literal finding).
- **F2 (low) — routed defect 7 has no row in `registration.md`'s Repairs list.** `## Repairs` (`:99-104`) maps
  R1→defect 1, R2→2, R3→3, R4→4, R5→5, R6→8, R7→6 and skips defect 7, though Rc1409/Rc1410 own it in
  `w1-spec.json`. The work is owned; the registration's defect→item map is incomplete. Fix is one appended note
  (the kill rule allows appended notes, never edits above).
- **F3 (info, by design) — the two ownerless carry items.** H2 stays operator-held (L0 queue); the QUALITY 33–35
  survivors get documentation, not hardening, this round. Both match the round-25 routing verbatim; named here so
  closure cannot read Table 2 as "everything owned".
- **F4 (info) — M25-5 is routed nowhere, and needs no route this round.** Its process fix (append-only errata;
  counts from `ls`/`grep -c`, not memory) is followed structurally: R5R6Corrections drafts text without editing the
  judged files, and Q37Population drafts criterion-37 text without editing QUALITY.md.

## Operator lessons (`corpus/lessons/operator-*.md`) vs QUALITY.md / SKILL.md

- **The glob set is empty — nothing to reflect.** `corpus/lessons/` holds exactly 28 files, all `round-N*.md`
  (full listing read); `*/corpus/lessons/operator-*.md` across all fleet lanes, `/home/vgpnk/Projects/shokunin/corpus/lessons/operator-*.md`
  and `mado-shokunin/.ufo/operator-*.md` all return no match. No operator-lesson file has ever matched this pattern
  in this lane's tree at this tip.
- **Closest real operator rule cited in-corpus is not reflected.** round-25.md's M25-5 "captured-by" cell names the
  operator's leg rule — "never change the judged object after judgment (it covers after; this was during)".
  Grep for `judged object|leg rule|M25-5` over `corpus/QUALITY.md` and `SKILL.md`: no matches; the phrase appears
  only locally in `SCORECARD.md:1695` ("the ledger above is the judged object"). It is a one-paragraph candidate
  for a QUALITY criterion at integration. Not routed by the spot-check, so recorded as informational, not a defect.
- Mori's cross-lane lesson on forgeable oracle-visible fixtures (cited as M25-2's captured-by, round-25.md:22) is
  reflected in mado by the landed harness repair plus criterion 36's control regime, not by a dedicated criterion —
  adequate; no action.

## Residual risk and verification gaps

- This is a plan-level map made mid-wave: most w1 seats are still running, so no control receipt, red run or
  selftest output was verified here. In particular the M25-2 repair's credit depends on K1LabelKeyed/K2LabelKeyed
  red receipts that do not exist yet (`controls/` holds only early K1/K2 scratch files).
- `round-26/quality/` existed but was empty at read time; CounterSelftest, Q36Fixtures and Q37Population outputs
  (and their red/green runs) are unverified by me.
- The harness R1 claim rests on reading `harness/oracle.py` bytes (`:21-22`, `:144`, `:230-234`), not on a sandbox
  run; OracleDeterminism/SentinelHarness are the seats that exercise it.
- `w1-run.json` (`counts.spawn=40`, registry members = the 40 spec names) proves dispatch at read time, not
  liveness of every seat.
- QUALITY.md ends at criterion 36 (324 lines); criterion 37 exists only as Q37Population's draft until integration.

## Suggested checks for the integrator (main agent)

1. Confirm F1 lands somewhere append-only (CounterSelftest receipt or registration note) before data wave w2.
2. When appending the defect-7 note (F2), keep it outside the frozen sections per kill-rule clause 2.
3. At integration, land criterion 37 (Q37Population draft) and consider codifying the M25-5 leg rule alongside it.
4. Before closure, require the two label-keyed controls' red receipts as M25-2's shown-able-to-fail evidence.
