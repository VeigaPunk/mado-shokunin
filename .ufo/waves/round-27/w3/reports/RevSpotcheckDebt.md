# mado round 27 — w3 rubric: what the round-27 report must satisfy (RevSpotcheckDebt)

Seat: `MadoR27.RevSpotcheckDebt` (reviewer, wave 3 residual), 2026-10-23. This is the checklist only — the
round-27 report does not exist yet and was not verified. It is the pass/fail rubric I will apply to
`.ufo/reports/round-27/mado.md` + `SCORECARD.md` when they land. No tools were installed or updated by this seat.

Sources (every item below names file:line):

- `corpus/lessons/round-26-verifier-spotcheck.md` — the outside discernment check of round 26. Duty to answer it:
  `.ufo/prompts/mado-round-27.md:329-332` ("turn every disagreement or routed defect into a lesson-backed
  `QUALITY.md` criterion or fix, or say in the report why not").
- `corpus/lessons/round-25-verifier-spotcheck.md` — prior round's check; cited only where the r26 spotcheck itself
  references it, or to mark an r25 thread closed (do not double-charge).
- `SHONEN.md` — the 4 promotion boxes.
- `.ufo/prompts/mado-round-27.md` (below: "prompt:") §4 report contract `:99-129`, §5 commit/push/L0 `:131-140`,
  §6 addendum items bearing on the report `:42-75`, `:169-172`, `:209-218`, `:265-271`, `:315-316`, `:325-334`,
  `:347-371`.

---

## 1. Open items from the r26 spotcheck the r27 report/SCORECARD must answer or explicitly carry forward

R26 `## 7. Routed defects` (`round-26-verifier-spotcheck.md:205-224`, items 1–8) plus the open defects embedded in
its body. "Carry forward" is valid ONLY as an explicit, reasoned statement in the report (prompt:330-332); silence
fails the item.

| ID | Open item — what r27 must show | r26 spotcheck source | Pass form in r27 report/SCORECARD | Carry-forward form (if not fixed) |
|----|-------------------------------|----------------------|-----------------------------------|-----------------------------------|
| D1 | M26-10 doc debt: `tools/mado-binds.py` docstring and PROVINCE must state that an environment `$NAME` stays literal and `source = $VAR` is not followed; optionally seeding restored behind an explicit flag; env-using cases in the next C2-family counter | r26:207-209 (ruling: r26:107-121) | Docstring/PROVINCE diff shows both limits documented; the r27 C2 counter (`.ufo/waves/round-27/c2/count-v2.py`) has env-using cases, or the omission is named | Report names which of the three sub-demands are deferred and why |
| D2 | M26-9 seed-count rule: a pre-data control receipt set is complete only at the registered seed count per control shape; the Q36 successor must count seeds per control shape | r26:210-211 (ruling: r26:77-82) | The r27 pre-data C1/C2 control receipts meet the registered seed counts under `PRED-C1-r27-v4`/`PRED-C2-r27-v2`, and the checker output showing per-shape seed counts is committed | Report says the checker change did not land, with the manual count shown instead |
| D3 | `PROVINCE.md:36-39` is stale (says the tool seeds from `os.environ`): append a round-26 correction; corrections sweep every mention | r26:212-213 | PROVINCE.md diff appends the correction and a quoted-sweep shows no remaining stale mention | Explicit carry-forward naming where the stale text remains |
| D4 | `SKILL.md` registry rows missing for `counter-selftest.py`, `check-population.py`, `check-control-receipts.py` (name, gate\|probe, entry command, verdict map, self-test, pinned path, write scope, owner); self-test must pin the active counter | r26:214-216 (evidence: r26:138-147, §2.4 gates table) | SKILL.md diff adds the three rows with all 8 fields; the self-test pin names the r27 active counter (C1 `count-v4.py`) | Explicit carry-forward; the three gates stay non-conformant under the §Gate standard until then (r26:147) |
| D5 | Q36 successor exits 1 on `.txt` receipts (it did on round 26): add a receipt-path option; commit the w2 survivor witnesses MutSelftest 6/10 and MutQ37 3/6 as fixtures (M26-8) | r26:217-218 | Checker runs green on the r27 `.txt` receipts (c1/c2 under `.ufo/waves/round-27/evidence/`); survivor fixtures committed | Explicit carry-forward with the red output quoted |
| D6 | SCORECARD's `check-population.py` "on both after-receipts → PASS" sentence had no committed run: commit the runs the sentence cites, or correct the sentence; also record the launcher environment on before-receipts as on after-receipts | r26:219-220 (also r26:165 calibration row; env gap r26:123-136) | For r27: population-check runs committed against the r27 after-receipts (`evidence/c1-after-48b9434a.txt`, `c2-after-48b9434a.txt`), and the r27 before-receipts carry the launcher env | Sentence corrected + env gap named |
| D7 | Harness: bwrap under `env -i` (M26-5); data seats must not feed known-crash inputs; each seat reports its own coredump delta (M26-6) | r26:221-222 (context: r26:123-136) | r27 measurement receipts carry `HOST_SAFETY` delta lines and the report shows per-seat coredump accounting or states no nested Hyprland was started | Explicit carry-forward naming which harness change is deferred |
| D8 | Protocol-lane defect (not mado's to fix): hyaku addendum §6.2 "taskCall unchanged" is byte-unsatisfiable under host `RULES.md` injection — carve out the operator suffix or have the validator emit a digest of the rendered text | r26:223-224 (ruling: r26:39-44, M26-4) | The report must not silently drop it: route it (L0 question or named protocol-lane hand-off), or state it stands routed from r26 | Explicit re-route counts as the answer |
| E1 | Three gates had no committed red/green evidence for their active-counter pin (`counter-selftest.py` pinned v1, not the active v2; `check-population.py` w2 survivors; `check-control-receipts.py` red on r26) — none conformant under the §Gate standard without the D4 registry rows | r26:138-147, table r26:140-146 | Each r27 gate row: committed green run against the active counter + red mutant receipts | Explicit carry-forward per gate |
| E2 | Calibration honesty: SCORECARD population sentence unbacked (same fact as D6, kept visible because r26's trend verdict `calibration: unchanged` rests on it) | r26:165, r26:190-192 | Any r27 SCORECARD sentence about a checker run has the committed run behind it | n/a — this is a pass/fail honesty item, not deferrable |

Supersession cross-references (context only; do not re-demand where r26 records them landed): r26:190-192 records
the r25 routed repairs landed with red/green evidence — r25 label-free case paths (r25:200-201), Q36-successor
fixtures (r25:206), `:1409`/`:1410` second derivations (r25:211), R8 correction (r25:207-208), R2/M25-4 encoded as
QUALITY 37 `check-population.py` (r25:204-205). Still-open threads that survive into D-items: env/`source` limits
(r25:209-210 → D1), before-receipt `exit=`/env recording (r25:212 → D6), survivor mutants (r25:202-203 → D5/E1).
R26 closure note: SHONEN box 3 promotion is operator-owned, never lane-written (r26:201-203; same in r25:194-196).

---

## 2. SHONEN boxes — what evidence a `[x]` / `[~]` needs this round

State rules (prompt:118-119): `[x]` only with a **named non-author verifier**; `[~]` with a **resolvable evidence
pointer**; `[ ]` if untouched. A pointer that does not resolve (file:line or receipt missing) fails the line. The
report must carry exactly one line per box (4 lines — SHONEN.md:5,7,9,11).

| Box | SHONEN.md line | `[x]` evidence needed this round | `[~]` evidence needed this round |
|-----|---------------|----------------------------------|----------------------------------|
| SKILL.md real decision tables, error patterns, checklists, cited sources | SHONEN.md:5-6 | Named non-author verifier on record who checked the SKILL.md artifacts (decision tables/error patterns/checklists/citations) — natural vehicle: D4's three gate registry rows, verified by a reviewer seat | Pointer to the landed SKILL.md rows/diff and their receipt (e.g. gate self-test output), or the standing historical assertion carried with this round's added artifact |
| ≥1 end-to-end domain task executed and logged in LOG.md | SHONEN.md:7-8 | Named non-author verifier over a LOG.md entry whose task ran end-to-end this round (e.g. a full C1/C2 counter run against the sandboxed Hyprland oracle) with its receipt | Pointer to the LOG.md entry + carrying commit + the receipt (the after-receipts `c1-after-48b9434a.txt` / `c2-after-48b9434a.txt` qualify if LOG cites them) |
| Instructions executable by an agent without oral context | SHONEN.md:9-10 | A named non-author verifier who actually ran the landed tool standalone with only in-repo context — both closures named the form: `python3 -I tools/mado-anims.py --home DIR` (r26:202-203) / `python3 -I tools/mado-binds.py --home DIR` (r25:195). Promotion itself is operator-owned: a lane-written `[x]` fails | Pointer to the runnable command + its committed receipt, showing no oral context was needed |
| No cross-domain bleed (PROVINCE.md still accurate) | SHONEN.md:11-12 | Named non-author verifier over a PROVINCE accuracy check | Pointer to the landed D3 correction (PROVINCE.md:36-39 region) + mention sweep. A `[~]` without the D3 correction landed (or explicitly carried) fails this round: PROVINCE is known-stale per r26:212-213 |

---

## 3. Required report sections — per-section pass/fail criteria (verifier's rubric)

Report path: `.ufo/reports/round-27/mado.md` on the fleet repo (prompt:101). Sections in order (prompt:104-119).
Verdict scale: **PASS** / **FAIL-marker** (section is a marker predicate → round failed, relaunch, prompt:121-125) /
**CONFORMANCE-DEFECT** (ok + one logged defect) / **CARRY-VALID** (explicit reasoned carry-forward).

1. **Work performed** (prompt:104-106) — PASS: opening names the declared claims (1–3) with target axes/capability;
   one bullet per work item; every bullet carries a resolvable evidence pointer (path:line, command output, or
   commit hash). FAIL-marker: section missing, placeholder, or pointers absent. Round-27 specifics: the wave-3
   residual work (counters C1/C2 run inline, receipts `c1-after-48b9434a.txt`/`c2-after-48b9434a.txt`, landed
   `tools/mado-wsrules.py` at rev `48b9434a`) must appear with pointers; inherited attempt-1 state (reuse vs
   discard, both named) per prompt:169-172.
2. **Landed changes** (prompt:107-108) — PASS: every landed change tied to a LOG.md entry AND to the commit hash
   carrying it; wave specs/registries under `.ufo/waves/round-27/` committed as evidence (prompt:209-210); only
   helper `landed <hash>` lines cited, never `rewritten` diagnostics (prompt:281-282, :302-303). FAIL-marker: missing
   section or changes without LOG+commit pairing.
3. **Before → after measurements** (prompt:109-110; claim-sizing prompt:350-371) — PASS per claim: one measurement
   with a pasteable counting command + the commit measured against (branch tip form, never bare `HEAD`,
   prompt:315-316); after-state is one concrete value re-derivable by one command over committed bytes
   (prompt:351-352); no universal clauses unless the command enumerates the full set (prompt:353-354); a calibration
   claim counts SCORECARD/SHONEN-vs-repo mismatches, not assertions (prompt:355-356); the frozen predicate is the
   same sentence in plan, counter code and receipt label (prompt:364-367); a do-nothing control receipt committed
   before data, and the target is one a no-op control cannot reach (prompt:359-363 — for r27: the C1/C2 control
   suites must pre-date the data receipts); ≥1 claim sourced on an `S###` row opened this round (prompt:73-74);
   targets never narrowed after landing (prompt:358). FAIL: a claim lacking before or after, an unpasteable
   command, or a narrowed target.
4. **Sources & frontier** (prompt:111-115; §2b prompt:42-75) — PASS: rows before→after with the census counting
   command; rows added by tier; rows touched old→new; frontier rows advanced; census start+end outputs with exit
   codes pasted, exit 0 required at round end (prompt:54-59); every new SOURCES row has Gate-recorded URL, access
   date, ≤25-word located quote (prompt:49-53); ≥1 mistake mined into `corpus/lessons/round-27.md` `## Mistakes`
   with class/evidence/captured-by/fix, or the empty-sweep paste (prompt:68-72). NOT a marker predicate: skipping it
   = `ok` + minimum-content conformance defect (prompt:121-125); a census fail is a conformance defect, not a pass
   (prompt:56-58), and the watchdog applies its census gate (prompt:127-129).
5. **Trend verdicts** (prompt:116-117) — PASS: exactly three verdicts — `expansion`, `quality`, `discernment` — each
   from {`improved`, `harmed`, `unchanged`, `unprovable-but-better`}, each with evidence, no scalar. NOT a marker
   predicate (prompt:121-125). Honesty override (prompt:347-349): a `harmed` or `unprovable` finding reported as
   `improved` fails the whole section regardless of form.
6. **SHONEN** (prompt:118-119; §2 above) — PASS: one line per box (4), states obey the state rules, every pointer
   resolves. FAIL-marker: missing/placeholder. A lane-written `[x]` without a named non-author verifier fails the
   line even if the section exists.
7. **Marker rule application** (prompt:121-125) — contentless report (placeholder text, any missing
   marker-predicate section — i.e. any of 1/2/3/6 — or no evidence pointers) → round **failed**. Real committed work
   but only 4/5 skipped → `ok` + one minimum-content conformance defect.
8. **Round-27 report extras** (prompt:333-334, :212-218, :265-271, :138-140, :325) — PASS requires: canonical Trend
   verdicts section (item 5); a `Stale-lane` line; every tool install recorded (tool/version/channel/reason);
   round shape + each wave's seat count, role mix, dead seats with last error text, any residual call, round total
   ≤128, and the planner-seat mapping record (prompt:212-218); misroot sweep result recorded under `## Mistakes`
   (prompt:265-271); open L0 questions noted without blocking (prompt:138-140); report lands last and cites the
   pushed lane hash (prompt:325, :133-137). Missing extras = conformance defects (ok + logged each), except a
   false/dead-seat omission, which is an honesty fail (prompt:347-349).

Verifier decision procedure: apply 1–6 in order; any FAIL-marker → round failed; collect conformance defects
separately; then check §1 D-items — each must be answered (fixed with evidence, or CARRY-VALID) and §2 boxes must
match the evidence standard. The report is admit-ready only when no FAIL-marker, all D-items answered, and no
honesty override triggered.
