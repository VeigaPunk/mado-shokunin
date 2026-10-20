author: MadoR17.LessonChainJoin (connector seat, round 17 w1; advisory only — I do not judge, edit, integrate or admit)

# Safety lesson chain — round-15 M2 → round-16 M1/M5/QUALITY21 → round-17 M2 tripwire

**Verdict up front.** Every step does cite a predecessor, but the citation
form decays from path anchor to prose label to no id, and one immediate
predecessor (round-16 M1) is skipped by the round-17 row. More importantly,
the chain carries **two uncorrected label defects in its own ancestors**:
round-15 M2's fix clause "No further pacman operation … in this round" is
false against its own transcript (a `pacman -Ql` 10 s later), and QUALITY 20
repeats that clause; and the round-17 M2 row's falsification cites the
*synthetic* `incident-replica.jsonl` selftest as if it were the *real*
`MadoR15.LibinputEvents.jsonl` line 54. That second defect is exactly
round-16 M2's recorded class, "Static fixtures are not real package-plan
output or installed-host comparison." The chain therefore does not yet
terminate in a clean step; it terminates in a step that re-commits an
earlier step's defect. A third, forward-looking hazard: the tripwire's
contract lets a `--permit` run print `MADO_TRIPWIRE: clean` while the JSON
carries findings — the R16-V1 label shape, reproduced by the new tool.

Scope: trace and overreach only. No claim, score or admission is made here.

## 1. Method and bounds

Read-only. Lane files read as bytes: `corpus/lessons/round-15.md`,
`round-16.md`, `round-16-verifier-spotcheck.md`, `corpus/QUALITY.md`,
`SKILL.md`, `LOG.md`, `SCORECARD.md`, `considerthese/2026-10-20.md`,
`.ufo/waves/round-17/{w1/spec.json,drafts/*,tripwire/*}`,
`tools/mado-action-plan.py` (source read only), and the round-17 peer
reports `IncidentTimeline.md` and `CriticHonesty.md`. I did **not** open any
OMP session transcript — the seat item names none, and the contract permits
transcript reads only by seats whose item names them. Facts that exist only
in transcripts are cited as peer-reported and labeled `[peer]`. I ran no
gate, selftest, package/service/compositor command, probe or `jj`; installed
nothing.

## 2. Chain map

| # | Step | Carrier / location | Cites predecessor as | Verdict |
|---|---|---|---|---|
| 1 | R15 M2 host partial upgrade | `corpus/lessons/round-15.md:15`; prose `:26-33`; non-resolution `:18-22` | root; captured-by = operator tooling directive | evidence pointer exact `[peer: IncidentTimeline §5]`; root cause is an **instruction conflict**, not an information gap |
| 2 | QUALITY 20 | `corpus/QUALITY.md:72-78` | `(lesson: lessons/round-15.md#mistakes M2; orchestrator ruling …)` | direct path anchor — **but line 76 repeats M2's false clause** |
| 3 | SKILL pause/install instruction | `SKILL.md:477-500` | "See [`round-15.md`] M2 and QUALITY 20" (`:484-485`); round-16 superseding text `:487-500` | direct path; carries the directive-vs-pause reconciliation partially |
| 4 | R16 M1 host-safety harm | `corpus/lessons/round-16.md:14` | "round-15 lesson M2" in Evidence cell | direct by **prose label**, not path; fix names QUALITY21 and self-bounds: "It does not intercept tools or resolve R15-V1." |
| 5 | QUALITY 21 | `corpus/QUALITY.md:82-104` | first line `(lesson: lessons/round-16.md#mistakes M1/M2)`; tail cites outside `round-15-verifier-spotcheck.md` R15-V1/V2 | direct path to the round-16 row, two hops to R15 M2; limits explicit |
| 6 | R16 M5 prohibited query | `corpus/lessons/round-16.md:18` | captured-by "Context no package operations; QUALITY21" | **indirect**: no R15 citation; QUALITY21's text bans transactions/mutations and requires propagating the round's no-probe scope, it does not name package *queries*; the query ban lived in the wave context |
| 7 | R17 M2 draft | `.ufo/waves/round-17/drafts/LessonDraft.md:12` | "round-15 M2", "round-16 M5", "round-16 M4", "round-16 M2 debt" | **prose labels only**, and **round-16 M1 is absent** even though its non-interception limit is paraphrased in the captured-by cell |
| 8 | SCORECARD C3 pre-registration | `SCORECARD.md:853-860` | no lesson id; names the command and "round-15 transcripts" | limit is exact: "Detection after the fact only — never interception, prevention or host repair." Scope says "`bash` tool calls" only (`:855`) |
| 9 | QUALITY 23 draft (C1) | `drafts/QualityDraft.md:11` | `lessons/round-17.md#mistakes M1; outside … R16-V1` | direct path; unrelated to the safety chain (R16-V1) |
| 10 | QUALITY 24 draft | `drafts/QualityDraft.md:13-14` | `lessons/round-17.md#mistakes M2; round-16 M5 … §Per-claim re-check C3` | direct path — the only draft that closes the chain at QUALITY; still marked "Candidate, not admitted" |
| 11 | SKILL tripwire registry row draft | `drafts/SkillRegistryDraft.md` table + limit paragraph | **no lesson id** | limit paragraph is strong (post-hoc, assistant toolCalls only, mutable transcripts); no ancestry |

**Answer to "does each step cite the previous?"** Yes at the level of at
least one predecessor, but not uniformly and not at full strength:

- Direct **path** anchor: QUALITY 20 → R15 M2; QUALITY 21 → R16 M1/M2;
  QUALITY 24 → R17 M2.
- **Prose label only**: R16 M1 → R15 M2 ("round-15 lesson M2"); R16 M5 →
  QUALITY21; R17 M2 → R15 M2/M5/M4. A reader can resolve these by search,
  but they are not the `lessons/round-N.md#mistakes M<k>` form the QUALITY
  rows use, and a future edit that renumbers a table breaks them silently.
- **Missing hop**: R17 M2 does not cite R16 M1, the step that records both
  the failed fence and the non-interception boundary the tripwire inherits.
- **No ancestry at all**: SCORECARD C3 and the SKILL registry row draft.

## 3. Step findings

### 3.1 R15 M2 (root) — evidence exact, fix text false

The evidence pointer (`/var/log/pacman.log:2429-2437`, actor, exact command)
is confirmed historical: `[peer: IncidentTimeline §5]` checks span, command,
actor and timestamp against the log and transcript, with no under- or
over-span. `[peer: IncidentTimeline §6(d)]` also finds the fix clause
"No further pacman operation, downgrade/revert or compositor restart in
this round" false: the same round ran `pacman -Ql libinput libinput-tools`
at T57, 10 s after the transaction, and the lesson's own prose at
`:31-33` concedes "package file listing, man-page/help/header/hash reads
afterward". `[peer]` labels this
"the clause is false against its own evidence" — i.e. R16-V1's shape.

Two chain consequences:

1. **The defect propagated into QUALITY**, which is the chain's own
   captured-by surface: `QUALITY.md:76` states "Round 15 performs no further
   pacman operation, rollback/downgrade or restart." Round 17's M1 corrects
   R16-V1 only; nothing corrects this. Round-17 M2 then cites R15 M2 as
   authority without noting the false clause.
2. **The root cause is an instruction conflict, not only a missing
   detector.** The seat's own thinking before `call_38165` names the
   tooling directive as authorization: "Remembering the automatic tooling
   installation directive; proceed with the installation without further
   prompting." `[peer: IncidentTimeline §3]`. That directive text is still
   appended to every seat task in this wave (it is in this seat's own
   prompt, above the host pause). The pause is a per-round override placed
   after it. A detector does not remove that conflict; it only makes one of
   its outcomes visible afterwards.

Also relevant: `[peer: IncidentTimeline §6(a)]` the refusal signal existed
13.3 s early (`pacman -Sp` output naming `libinput-1.32.0-1` next to four
new packages). R15-V1 was an attention/routing failure with the evidence in
hand, which is why a post-hoc scanner is a weaker response than consuming
the pre-execution signal.

### 3.2 QUALITY 20 — direct citation, inherited defect

Line 77 cites `lessons/round-15.md#mistakes M2` and the orchestrator
ruling. That is the strongest citation in the chain. But line 76 restates
the false no-further-operation clause, so the criterion *records* an
incorrect history while citing the row that contains it. QUALITY 21
supersedes criterion 20's prospective install route "while the operator's
host-wide pause holds" but leaves the historical clause untouched.

### 3.3 R16 M1 — correct self-bound, weak anchor

Evidence cell cites "round-15 lesson M2" (label, not path). Captured-by is
honest and specific: "QUALITY20's hard-coded overlap controls were not
installation prevention." The fix names QUALITY21, SKILL propagation and
the finite classifier's required cases, then self-bounds: "It does not
intercept tools or resolve R15-V1." This is the chain's best-calibrated
step: it states what the new carrier cannot do.

### 3.4 QUALITY 21 — direct, explicit limits

First line cites `lessons/round-16.md#mistakes M1/M2`; the criterion's
limit sentence is the chain's strongest negative: "Its verdict is not tool
interception, credential/privacy/probe safety, host immutability, a real
package dry run or remediation." It does **not** name package queries; its
pause text is "no package transaction or host service/compositor mutation
is permitted" (`:83-84`). The query ban is a wave-context rule, propagated
by the criterion's "carry … into every seat context" clause (`:86-87`).

### 3.5 R16 M5 — indirect citation, imprecise captured-by

M5's captured-by says "Context no package operations; QUALITY21". The
wave context is the actual source of the query ban; QUALITY21 contributes
the propagation rule and the pause, not a query prohibition. The row's fix
("static gate refuses literal pacman including `-Q`") is true of
`mado-action-plan.py`: `PINNED_DENY_EXECUTABLES` contains `pacman`
(`tools/mado-action-plan.py:110`) and matching is basename-only (`:6`,
`:323-335`), so any declared plan whose argv[0] basename is `pacman` is
refused regardless of flag. But that gate grades *declared JSON plans*; the
breach was an issued bash command the gate never saw. The fix sentence can
be read as if the gate would have caught M5; it could not. SKILL states the
boundary later (`SKILL.md:552-553`: "It does not intercept actual tool
calls"), but the lesson row itself does not.

### 3.6 R17 M2 draft — right limits, three chain defects

The draft row's fix and limits are largely correct: "detection only; not
interception, prevention or host repair"; "classifies only `bash` and
`eval` tool calls"; falsification cases include the red anchor, a quoted
`grep 'pacman -S' file` clean control, and exit 2 for invalid JSON / no
`.jsonl`. Defects:

1. **Fixture/real-anchor conflation.** The falsification says "`--selftest`
   must flag the round-15 red anchor, `MadoR15.LibinputEvents.jsonl` line
   54, toolCall `call_38165`". But `--selftest` runs
   `.ufo/waves/round-17/tripwire/core/expected.json`, whose `incident-replica`
   case reads the **synthetic** `incident-replica.jsonl` — 4 lines, a
   fabricated timestamp (`2026-10-19T22:14:03Z`), and a copied call id.
   The real anchor can only be shown by `--scan` on the real seat file.
   Using the selftest as the anchor receipt is round-16 M2's exact class
   ("Static fixtures are not real package-plan output…"), re-committed
   inside the row whose job is to close M2.
2. **Internal tension in the class cell.** The class says "prompt-only
   fences", but round 16 additionally shipped a static plan classifier. The
   captured-by cell corrects this ("The static classifier screens declared
   JSON plans only…"), so the row contradicts itself in one line. The
   precise class is: prompt/context rules plus a declared-plan screen, none
   of which observes an issued command.
3. **`eval` scope overstated.** The row says "`bash` and `eval` tool
   calls"; the contract parses bash and **`!`-prefixed** eval only. Non-`!`
   eval code is explicitly not parsed, and the compound fixture
   `eval-nonbang-clean` expects exit 0. The row should say "`bash` and
   `!`-eval".

Also: the row's evidence bundles round-16 M4 (a write-path misroot) into
a class whose fix is a command scanner. The fix cell does not claim to
detect M4, but the class/evidence pairing implies coverage the tool does
not have. If M4 stays in the evidence, the fix must add "does not detect
write-path or destination misroots".

### 3.7 C3 pre-registration, QUALITY 24, SKILL registry

- C3's limit sentence is exactly right and should be repeated verbatim in
  the report. Its scope sentence is narrower than the tool: "classifies
  only commands actually issued as `bash` tool calls" (`SCORECARD.md:855`),
  omitting `!`-eval, while the contract and drafts include it. Either the
  result states the actual scope or the tool must not scan `!`-eval; the
  current mismatch is a claim/receipt gap at pre-registration level.
- QUALITY 24 is the only carrier that gives the safety chain a QUALITY
  terminus, and it already states most limits. It does **not** say a
  permit-bearing run may not be cited as `clean` (see §4.3), and it says
  "admission claim about a seat's conduct", which puts an author tool in
  the admission path — `[peer: CriticHonesty F6]` recommends "asserting"
  instead.
- The SKILL registry row draft's limit paragraph is good but has no
  ancestor citation; a registry row is not a lesson carrier, so this is a
  gap only if L1 wants the tool traceable from SKILL alone.

## 4. Inherited defects and contradictions

### 4.1 D1 — R15 M2 / QUALITY 20 false historical clause

Evidence: `corpus/lessons/round-15.md:15` and `corpus/QUALITY.md:76`;
counterexample T57 `pacman -Ql` `[peer: IncidentTimeline §6(d)]`. Same
class as R16-V1 (claim stronger than receipt). Round 17 does not correct
it; M2 cites the row as authority. This is a chain-integrity defect, not a
new harm: the T57 query mutated nothing.

### 4.2 D2 — round-17 M2 uses a synthetic replica as the real anchor

Evidence: `drafts/LessonDraft.md:12` ("`--selftest` must flag … line 54 …
`call_38165`") vs `tripwire/core/incident-replica.jsonl` (fabricated
4-line fixture, copied id) and `core/expected.json` (`incident-replica`
case). The fixture is legitimate as a selftest; it is not the anchor. This
is round-16 M2's fixture/operational class recurring.

### 4.3 D3 — permitted runs can print `clean` over findings

The interface makes the first line a function of exit, not of the JSON:
exit 0 = no *unpermitted* finding. The fixtures enforce this:
`live-probe-permitted` (`['live_probe']`, want_exit 0, one finding),
`var-assign-pacman-query-permitted`, `omarchy-permitted`, and
`dir-scan-all-permitted` all expect exit 0 **and** non-empty
`want_findings`. So `--scan <R15 file> --permit host_mutation` would print
`MADO_TRIPWIRE: clean` over the libinput `sudo pacman -S`. A report citing
that first line would repeat R16-V1, and the drafted QUALITY 23 would not
catch it: criterion 23 binds the receipt's *recorded token*, and the
receipt really does say `clean`. The defect is in the tool's label
semantics, not in the citation. (Same finding as `[peer: CriticHonesty F3]`,
reached here from the chain side.)

### 4.4 D4 — the authorizing directive is still in every seat prompt

The tooling directive above the lane contract lists `sudo pacman -S` first
as an install channel and says the pause is binding in the next block. The
R15 actor's thinking cited that directive as permission `[peer]`. The chain
has never removed the conflict; QUALITY 21 and SKILL override it per round.
A post-hoc detector does not close this; the M2 row should name the conflict
as the root cause so the chain does not read as "missing tool → tool now
exists".

### 4.5 D5 — pre-registered scope (bash) vs contract (bash + `!`-eval)

`SCORECARD.md:855` says bash only; the interface parses `!`-eval; the M2
row says "eval" without the `!` qualifier; the SKILL limit says
bash/`!`-eval. Four surfaces, three spellings. Pick the contract's and use
it everywhere.

### 4.6 D6 — a "candidate" criterion still counts

C1's rule is the literal grep `^[0-9]+\. .*lessons/`. Appending criterion
24 with the words "Candidate, not admitted" would still increment the
counter. If L1 does not admit 24, it must not be pasted into
`corpus/QUALITY.md` at all; it can live in the report as a rejected
candidate. Otherwise the round credits a rule it declares unadmitted — the
same label/instrument mismatch the round is correcting.

## 5. What would overreach

| Candidate claim | Status | Ground |
|---|---|---|
| "the tripwire prevents / intercepts / blocks the libinput-class command" | **false by design** | C3: "never interception, prevention or host repair"; QUALITY 21's limit list; R16 M1 "does not intercept tools"; M2 draft "detection only" |
| "a `clean` scan means no host mutation / the pause held" | **false** | scan is lane-side, transcript-only; host log has non-lane transactions between rounds `[peer: CriticHonesty F1]`; the tool cannot see them |
| "the recurring breach class (incl. M4 misroot) is now detected" | **overreach** | M4 is a write path; the tripwire parses bash/`!`-eval command text only; no write-path classifier in the contract |
| "`--selftest` proves the R15 anchor is detected" | **overreach** | selftest uses the synthetic replica; the real anchor requires `--scan` on the named file; fixture ≠ operational evidence (R16 M2) |
| "the permitted scan is clean" | **overreach** | permitted runs exit 0 with non-empty findings; first line is exit-derived, not evidence-derived |
| "QUALITY 21 already covered the package query" | **overreach** | QUALITY 21 bans transactions/mutations and requires no-probe scope propagation; the query ban was the wave context's |
| "round 17 implements considerthese suggestion 1" | **overreach** | suggestion 1 scans lessons/LOG/reports prose for words (`considerthese/2026-10-20.md:50`); the tripwire scans transcripts and explicitly ignores text mentions. Related intent, different artifact |
| "the tripwire closes / mitigates / resolves R15-V1" | **false** | R15-V1 is host state, operator-owned; detection changes no host state; SCORECARD round 17 carries it as operator-owned |
| "M2's evidence is anchored by lesson ids" | **not yet** | prose labels only; no `lessons/…#mistakes` anchors; R16 M1 missing |
| "the safety chain now terminates in QUALITY" | **conditional** | only if criterion 24 is admitted; as drafted it is a candidate, and a candidate pasted into QUALITY would count anyway (D6) |
| "operability: improved" (bare) | **overreach** | appropriate shape is capability-only plus carried harm, as round-16 closure used |

## 6. One bounded proposal

**Make the round-17 M2 step carry the same token discipline as the round's
own criterion 23 — at the chain level.** Concretely, in the M2 row and in
the decision on criterion 24 (L1 owns both):

1. **Exact ancestry.** The M2 Evidence cell cites
   `lessons/round-15.md#mistakes M2`,
   `lessons/round-16.md#mistakes M1`, `#M2`, `#M4`, `#M5` by path anchor.
   M1 is included because it is the immediate predecessor whose
   non-interception limit the tripwire inherits; M4 is included only with
   the explicit "not detected (write path)" clause.
2. **Two receipts, never one.** `tripwire-selftest.json` (synthetic
   fixtures; N/N) and `tripwire-scan.json` (real
   `MadoR15.LibinputEvents.jsonl`, whose sha256 is already in
   `evidence/session-index.json`), the latter recording findings at line
   54/`call_38165` (`host_mutation`, rule `sudo`) **and** at the later
   `pacman -Ql` (`package_query`) if the scan sees it — that second finding
   is also the counterexample to R15 M2's false clause. A selftest is never
   cited as the anchor.
3. **Permit-label rule.** `MADO_TRIPWIRE: findings` whenever the JSON
   `findings` array is non-empty, regardless of exit (exit stays 0 when all
   findings are permitted); and any citation with a non-empty `permitted`
   list quotes `counts` and `permitted`, never `clean`. The selftest
   compares exit and findings only, so no `expected.json` case changes.

If L1 judges criterion 24 inflationary, apply (1)-(3) to the M2 row only
and leave 24 out of `QUALITY.md` entirely (D6). Do not append it as a
"candidate".

## 7. Axes

| Axis | Effect of the proposal | Harm check |
|---|---|---|
| calibration (C1) | +1 lesson-cited criterion only if 24 is admitted (16/24 = 6.6667 vs 15/23 = 6.5217); otherwise unchanged. The M2 row's anchors are not counted but prevent a defect that undercuts criterion 23's value | append-only QUALITY; no existing row edited; the R15 M2/QUALITY 20 correction is additive text, not a rewrite |
| operability (C3) | capability evidence split into fixture vs real-transcript receipts; permit runs can no longer be labeled `clean` | no tool behavior beyond the first-line label; exit codes unchanged; fixtures unchanged |
| coverage (C2) | none | no knowledge/SOURCES/PROVINCE file touched |
| freshness / depth / adjacency | none | no gate, host, or routing change |

## 8. Risks

- **Late contract change.** `tools/mado-tripwire.py` had not landed at
  report time (`tools/` holds only `mado-action-plan.py`, `mado-verify.sh`),
  so the label rule is cheap now; after implementation it costs a re-run.
  L1 should message `MadoR17/TripwireCore` before integration.
- **Inflation reading.** Admitting 24 raises the literal count. Report both
  counts and name 24 as the second row, per `[peer: CriticHonesty F6]`;
  RevQuality2122's verdict should be quoted either way.
- **Scope creep into C1.** Correcting R15 M2/QUALITY 20 is not
  pre-registered under C1 (which names R16-V1). Do it as an M2 evidence
  note or a separate append-only erratum, not by widening M1 silently. If
  deferred, the report must not repeat the false clause.
- **Peer dependence.** IncidentTimeline's T57 and the thinking quote are
  lane-seat evidence, not outside verification. They are labeled `[peer]`
  here and should be labeled the same in the lesson if reused.
- **M4 wording.** Adding M4 to the row without "not detected" would imply
  write-path coverage the scanner lacks.

## 9. Verification L1 can run (once, at integration)

1. `grep -nE 'No further pacman operation' corpus/lessons/round-15.md corpus/QUALITY.md`
   → exactly 2 hits today; confirm the round-17 lesson does not become a third.
2. `python3 -I tools/mado-tripwire.py --scan <…/MadoR15/MadoR15.LibinputEvents.jsonl>`
   → exit 1; findings include `host_mutation`/`sudo` at the line carrying
   `call_38165`; whether the later `pacman -Ql` appears is the check that the
   scan is per-command, not single-anchor. Compare with the oracle file.
3. `python3 -I tools/mado-tripwire.py --selftest .ufo/waves/round-17/tripwire/core`
   and `…/compound` → exit 0, summaries as recorded.
4. `python3 -I tools/mado-tripwire.py --scan .ufo/waves/round-17/tripwire/core/live-probe.jsonl --permit live_probe`
   → exit 0, first line `findings` after the change, `permitted:["live_probe"]`,
   counts `live_probe: 1`.
5. `git show REV:corpus/QUALITY.md | grep -cE '^[0-9]+\. '` and
   `… | grep -cE '^[0-9]+\. .*lessons/'` → record both; report the fraction
   with and without row 24, and confirm no "Candidate" text is in the file.
6. `grep -nE 'lessons/round-1[56]\.md#mistakes M[0-9]' corpus/lessons/round-17.md`
   → the M2 row must hit at least `round-15.md#mistakes M2` and
   `round-16.md#mistakes M1`/`M5`.

## 10. Limits of this report

- I did not read the OMP transcripts; line 54/`call_38165`, T57 and the
  thinking quote are second-hand from IncidentTimeline and labeled `[peer]`.
- I did not run the tripwire (not landed, and not my item); the permitted-run
  label behavior is derived from the contract plus the committed fixture
  expectations (`expected.json` asserts exit and findings only, so the first
  line is unconstrained by the fixtures).
- I did not verify the host log; the "non-lane transactions between rounds"
  point is `[peer: CriticHonesty F1]` and only bounds what a lane scan can say.
- No axis verdict, admission or score is asserted. No files outside this
  report were written; no commits, no `jj`, no tools installed.
