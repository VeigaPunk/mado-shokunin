# ClosureDebt — routed R15-V1/V2/R14-V1 and required round-16 responses

Seat: `MadoR16.ClosureDebt` (scout, leaf; no subagent dispatch).
Baseline: `32c4fda873c9cb47a84c549b24b80ead2bcaa1ea`.
Lane root: `/home/vgpnk/Projects/shokunin/mado-shokunin`.
Scope: read the prior rejected-harmed closure's three routed items and enumerate
what round 16 must answer. **No repair was performed**; this file is the only
write. No gate, selftest, `measure.py`, build, test, package, service,
compositor, input, screenshot or command-producer operation was run. No tool was
installed or updated, so the tooling record is empty.

Read first, as the round contract requires:
`corpus/lessons/round-15-verifier-spotcheck.md` (full). Supporting reads:
`corpus/lessons/round-14-verifier-spotcheck.md`,
`corpus/lessons/round-15.md`, `corpus/QUALITY.md`, `SKILL.md`, `SCORECARD.md`,
`PROVINCE.md`, `.ufo/waves/round-16/w1/{spec,dispatch}.json`,
`.ufo/waves/round-16/evidence/*`, and the in-flight round-16 seat reports named
below.

## Summary — minimum round-16 response set

- **R15-V1:** keep the forbidden partial upgrade open and operator-owned; run no
  package/service/compositor/packaged-plan operation and no live probe; land the
  append-only follow-through (QUALITY criterion superseding 20, SKILL pause
  instruction, lesson anchors) without claiming repair or no-harm clearance.
- **R15-V2:** keep the new-only/real-plan rule in every relevant seat context;
  label hard-coded fixtures as fixtures, never as a real `pacman -Sp` plan or
  installed-host census; run no install to satisfy review; carry the r15
  `hyprctl version` process debt forward unrewritten.
- **R14-V1:** keep the accepted correction landed and the full-gate authority
  withheld; bind every new selftest/frozen receipt to the actual committed
  executable and revision; do not replay, restamp or recover old provisional
  receipts.

## 0. Observed state at read time (not landed evidence)

- `git rev-parse HEAD` = `32c4fda…`; the tree is dirty with round-16 drafts:
  `M SCORECARD.md`, `M SKILL.md`, `M corpus/QUALITY.md`, `M corpus/SOURCES.md`,
  `?? .ufo/waves/round-16/`, `?? corpus/lessons/round-16.md`. Everything below
  marked “draft” is uncommitted advice, not a verified round result.
- Round-16 dispatch is one `taskCall` with a single shared `context`
  (`dispatch.json:421`, 2096 bytes) and 64 tasks, `resumeSends: []`. The context
  carries the host-wide pause, “do not install anything”, the future real
  `pacman -Sp --print-format '%n %v'` + complete installed-name comparison, and
  “Hard-coded fixture is not actual package validation.”
- Baseline evidence: `.ufo/waves/round-16/evidence/census-before.txt` binds
  `measured_commit=32c4fda…`, exit 0, the three retained W04 warnings
  S030/S042/S045; `.ufo/waves/round-16/evidence/source-bindings.json` records
  S053/S054 fetched bytes and SHA-256.
- `tools/mado-action-plan.py` and `.ufo/waves/round-16/measure.py` do **not**
  exist at baseline. C1/C2 are therefore unproven at read time.
- The only committed normative safety rules are QUALITY criterion 20
  (`corpus/QUALITY.md:72-78`) and the round-15 SKILL paragraph
  (`SKILL.md:473-481`); the r15 lesson and standing-use erratum are committed
  history. QUALITY 21 (`corpus/QUALITY.md:82+`), the SKILL
  round-16 instruction (`SKILL.md:483-491`), the round-16 lesson and the
  S053–S055 rows are current-tree drafts.

## 1. R15-V1 — unresolved forbidden partial upgrade

Routed text: `corpus/lessons/round-15-verifier-spotcheck.md:254-267`.
Routee: operator/host-safety owner, **with mado follow-through before any new
round**. Facts fixed by the route: libinput `1.31.3-1 -> 1.32.0-1` plus new
`libinput-tools 1.32.0-1`, `python-libevdev 0.13.1-1`, `python-pyudev
0.24.4-1`, `python-yaml 6.0.3-2`; udev-reload/system-update hooks; “M2 is not
resolved by a new paragraph” (`:266`). Disposition: **cannot be closed by round
16**; only the follow-through is scorable.

| ID | Required round-16 response | Anchor | Round-16 carrier at read time | Status |
|---|---|---|---|---|
| V1-R1 | State plainly that the partial upgrade remains unresolved and operator-owned; do not claim remediation, recovery, no-harm clearance or a repaired host. | `round-15-verifier-spotcheck.md:260-266`; `PROVINCE.md:13-15` (“Never mutates a running compositor state”; out of province → report) | `SCORECARD.md:692-694` (operator round, “not host remediation or live-health clearance”); lesson draft M1 | Carried in draft; report sentence still owed |
| V1-R2 | Run no package transaction, no fresh package plan, no package query, no service/compositor mutation, no downgrade/reinstall/removal/full upgrade/restart this round. | `:262-265`; round-16 dispatch context; `SKILL.md:483-486` draft | Dispatch context; `NoInstalls.md`; QUALITY 21 draft | Prohibition observed at read time; must be restated in report |
| V1-R3 | Run no live compositor/service/input/screenshot/command-producer probe. Old command examples are data, never permission. | Dispatch context; `round-15-verifier-spotcheck.md:275-278`; `SKILL.md:489-491` draft | Dispatch context; `NoLiveBreach`, `SourceReopen` assignments | Prohibition; no live probe observed by this seat |
| V1-R4 | Carry the learning append-only: a criterion superseding 20 while the pause holds, a current SKILL pause instruction, and lesson rows with exact anchors. Do not mark M2 resolved by text. | `SCORECARD.md:712-714`; `:266` | QUALITY 21 draft (`corpus/QUALITY.md:82-99`); SKILL draft (`:483-491`); lesson draft M1/M2 | Draft only; must be committed and not overclaim |
| V1-R5 | Keep C2 bounded: static classifier of declared JSON only; it must never execute supplied argv or inspect the host; it is not a sandbox, interception, immutability proof or repair. | SafetyGate dispatch prompt (“Gate must never execute supplied argv or inspect host”); `SCORECARD.md:708-709` | `SafetyGate.md` assignment; `HostHarm.md` attack | Gate absent at baseline; caveat must appear verbatim-equivalent |
| V1-R6 | Do not convert r15 `operability`/`quality` harm into “no harm” because a gate is green or unchanged; retain the prior verdict and dates. | `round-15-verifier-spotcheck.md:229-244`; `SCORECARD.md:665-680` | SCORECARD history (unmodified region); SHONEN seat | Must be checked in final report |
| V1-R7 | Leave the operator L0 channel intact; do not append a duplicate L0 line, re-own the decision or open a new operator question. | `:260-262`; `corpus/lessons/round-15.md:200` (“No duplicate L0 line is appended”) | Lesson draft (“R15-V1 host-recovery L0 remains open”); `SiblingBoundary` assignment | Carried; report must not create a new question |
| V1-R8 | Do not install a tool merely to read its help; report a missing prerequisite as missing. | Dispatch context (“This round do not install anything; report missing prerequisites”); `round-15-verifier-spotcheck.md:270-275` | `NoInstalls.md` (no installs; none needed); `SkillSafety.md` | Satisfied at read time; record “none” |

## 2. R15-V2 — procedural compliance

Routed text: `corpus/lessons/round-15-verifier-spotcheck.md:268-278`.
This is the “next authorized round” item; round 16 is that round. It has a
present-round half and a conditional future half.

| ID | Required round-16 response | Anchor | Round-16 carrier at read time | Status |
|---|---|---|---|---|
| V2-R1 | Retain the new-only dry-run requirement in every relevant seat context. | `:268-271`; dispatch context | Single shared context at `dispatch.json:421`, inherited by all 64 tasks; no per-item prompt contradicts it (grep: `pacman` appears only in SafetyGate/SafetyCases as static plan/policy data, not execution) | Carried for wave w1; conditional if a resume/second wave is dispatched |
| V2-R2 | Distinguish hard-coded predicate controls from actual plan/installed-package validation. Never call a fixture an actual plan, installed-host census or production guard. | `:269-274`; `:159-167` (“explicitly hard-coded in-memory controls, not real pacman dry-run output”) | QUALITY 21 draft (“a hard-coded new-only fixture never proves it ran”); `SafetyCases`/`SafetyReceipt` assignments; `MistakeDraft` R15-c | Distinction is drafted; the new safety cases are also fixtures and must be labelled so |
| V2-R3 | Conditional future only: after an explicit operator lift/authorization, preserve the real `pacman -Sp --print-format '%n %v'` plan and compare every planned name (including dependencies) with installed names; any overlap refuses to L0. | `:271-274`; QUALITY 20 (`corpus/QUALITY.md:72-77`) | `NewOnlyFuture.md` (future tense, no present run); QUALITY 21 draft | Drafted as future procedure; no present `-Sp` is permitted |
| V2-R4 | Perform no install merely to satisfy this review. | `:274-275`; dispatch context | `NoInstalls.md`; `SkillSafety.md` | Satisfied at read time |
| V2-R5 | Carry forward the disclosed `ReviewLibinput` `hyprctl version` call as process debt, not fresh claim evidence or regression proof; do not rewrite filed history. | `:275-278` | `MistakeDraft` R15-b (also cites r15 `ReviewDocsEra` `/proc` read and `pgrep` disclosures); lesson draft M2 | Drafted; report must disclose, not erase |
| V2-R6 | Do not describe a fixture’s green result as operational installation prevention. | `:159-167`; `:272-274` | QUALITY 21 draft; `SafetyReceipt`; `QualityGround.md` §1 finding 5 | Must be checked in final wording |
| V2-R7 | Supporting pause enforcement: persisted policy must be `paused=true`, and invalid/non-paused/malformed policy must be rejected fail-closed. | Dispatch SafetyGate/PolicyTamper prompts; `SCORECARD.md:712-716` | `PolicyTamper`, `PolicyScope`, `UnknownActions` assignments | Gate absent at baseline; unproven |

## 3. R14-V1 — receipt binding and correction limits

Origin: `corpus/lessons/round-14-verifier-spotcheck.md:169-171`.
Accepted and narrowed by `corpus/lessons/round-15-verifier-spotcheck.md:279-283`:
correction landed; provisional whole-gate preimages unrecoverable; standalone
full-gate authority permanently withheld; future mutation evidence must bind its
actual committed executable/revision without relabeling old runs.

| ID | Required round-16 response | Anchor | Round-16 carrier at read time | Status |
|---|---|---|---|---|
| V14-R1 | Do not replay or restamp the three provisional r14 receipts; do not recover or invent preimages; keep full-gate authority withheld. | `round-15-verifier-spotcheck.md:279-283`; `round-14-verifier-spotcheck.md:169-171`; `gate-standing-use.md:462-500` | `R14History` assignment; lesson draft (“No historical receipt or prior gate is rewritten or replayed”) | Drafted; report must repeat the limit |
| V14-R2 | Bind every new standalone mutation/selftest/frozen receipt to the actual committed executable/revision: measured commit, raw gate SHA-256, exact command, observed exit, input digests. Pre-commit runs are labelled provisional and re-bound at commit. | QUALITY 7/9/13 (`corpus/QUALITY.md:12-19`); `round-15-verifier-spotcheck.md:281-283` | `SafetyReceipt`, `FrozenDesign`, `SelftestTruth` assignments | No gate/receipt exists at baseline; sequencing risk below |
| V14-R3 | Frozen mode verifies `expected.json` input digests for plan/policy and returns exit 2 `snapshot_tampered` on tamper, not a changed verdict. | SafetyGate dispatch prompt; `FrozenInputs`, `ExitMap`, `FindingStability` assignments | Gate absent at baseline | Unproven |
| V14-R4 | Register the new gate with complete registry fields, including frozen mode and static-not-enforcement limits. | `GateRegistry` assignment; SKILL gate registry table | `GateRegistry.md` draft | Draft only |
| V14-R5 | Do not infer full-gate authority or broad regression coverage from the new narrow frozen run; old derived-target receipts remain historical. | `round-15-verifier-spotcheck.md:280-283`; `gate-standing-use.md:493-500` | `R14History`, `OldGateBoundary` assignments | Must be in report |
| V14-R6 | Retain the r14 bounds: symlink-to-directory/FIFO/socket, glob dangling links, missing mutation cases and S050 deferred apply paths are not acceptance criteria; no arbitrary-shell-analysis claim. | `round-14-verifier-spotcheck.md:171` | `ExecBasename`, `PolicyScope`, `SafetySimplify` assignments | Must constrain gate claims |
| V14-R7 | Keep SOURCES/QUALITY/LOG/lesson append-only; do not rewrite existing rows; S055 is own-work safety evidence, not external authority or host-health proof. | `AppendOnly` assignment; `SourcesDraft`; in-flight SOURCES diff shows no existing cell change | SOURCES draft rows S053–S055; lesson draft | Draft only; census must be run at start/end by L1 |

## 4. Consolidated prohibitions (must hold for every seat)

1. No `-S`, `-Sy`, `-Syu`, `-U`, `-R`, `-Sp`, `-Q*`, sync, cache download,
   downgrade/revert, install or service/compositor restart this round.
2. No `hyprctl`, `systemctl`, `omarchy`, `libinput`/`evtest`/`record`/`replay`,
   screenshot, input observer or command producer. No host ABI/`ldd`/package
   state/compositor-mapping inspection or no-regression inference.
3. No execution of plan argv by the new classifier; no host inspection by it.
4. No claim that a fixture, green gate, unchanged suite or clean file plane is
   host health, package immutability, installation prevention or remediation.
5. No duplicate L0 line, no new operator question, no re-owning recovery.
6. No rewrite of round-13/14/15 filed receipts, lessons, reports or verdicts.
7. No install to obtain a prerequisite; report the prerequisite instead.
8. No promotion, SHONEN clearance, next-round mission or admission claim from
   authoring seats; independent closure remains pending.

## 5. Round-16 report/artifact obligations arising from these routes

These are the closure-specific items; the general six-section contract is
ReportContract's scope, not repeated here.

- A single disposition paragraph for R15-V1/V2/R14-V1 with the exact anchors
  above, stating: V1 open/operator-owned; V2 carried and fixtures-not-real;
  R14 correction landed and future receipts bound to committed bytes.
- QUALITY 21 appended, criterion 20 left intact, grounded in R15-V1/V2, with
  fail controls, and explicit “not repair” language.
- SKILL current pause instruction superseding the round-15 future-install
  wording, source-only restriction, no live probes, no package query.
- Lesson `## Mistakes` rows for the r15 transaction, the process/live-read
  breach, and the fixture-vs-real-plan distinction, each with anchors; no row
  marked resolved.
- Gate registry row for `mado-action-plan` with `--selftest`, `--plan/--policy`,
  `--frozen`, exit map 0/1/2, and static-not-enforcement limits.
- New receipts (selftest, negative incident-shaped plan, frozen run) carrying
  measured commit, executable digest, input digests, exact command and observed
  exit; pre-commit captures labelled provisional and re-bound.
- Explicit “no tool installs/updates” record, or the exact tool/version/channel/
  reason if one somehow occurred.
- Process-debt disclosure: r15 `hyprctl version` and any additional disclosed
  live read; no fresh evidence value.
- C1 statement that U7 is a documentary producer/renderer observation boundary,
  not rendered-pixel verification; U1–U6 unchanged.
- C2 statement that capability is 0→1 only after actual self-invocation,
  negative and frozen checks, and that the old hermetic-suite score is not
  numerically rewritten.
- L0 unchanged; host recovery operator-owned; no package/service remediation.

## 6. Gaps, contradictions and sequencing risks observed

1. **Follow-through is in-flight, not landed.** At `32c4fda` only QUALITY 20 and
   the r15 SKILL paragraph are committed. QUALITY 21, the r16 SKILL block, the
   r16 lesson and S053–S055 are worktree drafts. The required R15-V1
   follow-through is therefore not yet verified.
2. **Sequencing ambiguity `[INFERENCE]`.** R15-V1 says follow-through “before
   any new round”, while round 16 was dispatched before those artifacts landed.
   The round's defense is the explicit operator authorization
   (`SCORECARD.md:692-694`) plus in-round follow-through. The report should
   state the sequence honestly rather than imply the artifacts preceded
   dispatch. This seat cannot settle whether the closure reader treats that as
   conformant.
3. **QUALITY 21 control target.** The drafted criterion's fail-control sentence
   names the static action-plan classifier (incident-shaped package-install,
   disguised executable, unknown kind, malformed action). That is the C2 gate,
   not the `-Sp` predicate. R15-V2's real-plan rule is carried as future text
   (“a hard-coded new-only fixture never proves it ran”) but has no executable
   control for the `-Sp` comparison. Do not report the classifier controls as
   validating pacman plans. `QualityGround.md` raises the same point and
   proposes a fuller future procedure; L1 adjudicates.
4. **Receipt binding sequencing.** Because seats do not run gates, L1's
   post-integration selftest/frozen receipts must either be produced after the
   content commit or be explicitly provisional and re-bound at commit. A
   pre-commit run must not be stamped with the later measured commit
   (`corpus/QUALITY.md:12-19`, `:67-68`; R14-V1).
5. **Context retention is single-wave.** The new-only rule lives only in the
   shared `taskCall.context`; per-item prompts do not repeat it. If L1 resumes
   or dispatches a second wave, the same context must be retained
   (`resumeSends` is empty at read time). R15-V2 says “every relevant seat
   context”, so this is a live obligation, not just a wave-1 fact.
6. **Finite classifier scope.** The gate denies a fixed basename list
   (`pacman,yay,paru,systemctl,hyprctl,omarchy,libinput,evtest,sudo,sh,bash,env`)
   for `read-source`/`repo-write`; wrappers, interpreters, absolute paths with
   other basenames, symlinks and executable contents are not analyzed. The
   report must not generalize this to arbitrary shell safety (R14 bounds;
   `ExecBasename`, `PolicyScope`).
7. **Incident-shaped input is data.** `SafetyCases`' “actual libinput sudo
   pacman transaction” is a declared JSON plan, not a pacman plan or an
   installed-host comparison. Label it accordingly (V2-R2/V2-R6).
8. **Passive log reads are not package operations.** `NoInstalls.md` and
   `MistakeDraft.md` read `/var/log/pacman.log` as text; that does not violate
   “no package operation”, but the report should label such reads as reads, not
   queries. `MistakeDraft` additionally cites r15 `ReviewDocsEra` `/proc` and
   `pgrep` disclosures beyond the routed `hyprctl` item; these are extra
   process debt, not new evidence, and must not be rewritten.
9. **Draft numbering can drift.** QUALITY 21 cites
   `lessons/round-16.md#mistakes M1/M2`; the current draft has two rows M1/M2,
   while `MistakeDraft.md` proposed three rows and flagged the conflict. If L1
   renumbers the lesson, the criterion citation must be repointed atomically.
10. **S055 is own-work.** `corpus/lessons/round-15-verifier-spotcheck.md` is not
    an external authority or host-health proof; its quote/anchor must be exact
    and its census handling must not pretend it is a fetched URL source.
11. **No independent clearance.** All round-16 seats are authoring-lane advice.
    SHONEN remains four `[~]`; no promotion or admission is derivable here.

## 7. Remaining unknowns

- The operator's recovery decision, its timing and any new L0 content. Not
  reopened or quoted beyond the existing routed line by this seat.
- Whether L1 lands the drafts verbatim, and whether QUALITY 21 is revised per
  QualityGround's control-target critique.
- Actual C1 and C2 results; no gate, measure, selftest, negative or frozen run
  exists at baseline.
- Whether a second wave or resume dispatch occurs and whether the shared
  context is retained.
- Whether any round-16 seat performs a live/package operation not visible in
  the files read here. None was observed; no process audit was performed.
- The final independent closure verdict and admission.

## 8. Confidence and limits

- **High confidence** in the routed text, its anchors, and the required-response
  inventory: direct reads of the committed closure and baseline files.
- **Medium confidence** in carrier status: it rests on uncommitted worktree
  drafts and seat reports that can change before integration.
- **No repair**, no execution, no host or package operation, no sibling edit.
- Exact limits: this report lists obligations; it does not judge whether round
  16 meets them, does not run the counter, and does not claim R15-V1 is
  resolved or R14-V1's withheld authority is recoverable.
