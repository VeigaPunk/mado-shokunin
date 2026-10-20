# AttackClosureCarry — R15-V1 / R15-V2 / R14-V1 obligation map

Seat: `MadoR16.AttackClosureCarry` (scout, leaf). Lane root:
`/home/vgpnk/Projects/shokunin/mado-shokunin`. Baseline
`32c4fda873c9cb47a84c549b24b80ead2bcaa1ea`.

Question: every obligation routed by the independent
`corpus/lessons/round-15-verifier-spotcheck.md` (R15-V1 at lines 254–266,
R15-V2 at 268–277, R14-V1 at 279–282) is mapped either to an integrated
lesson/criterion or to an explicit operator-owned unresolved disposition.
No obligation is closed by assertion alone; missing literals are named.

Method: static reads only. No gate, selftest, frozen run, mutation harness,
`measure.py`, census, package query or live compositor/service/input probe was
executed. No tool installed or updated. Git was read only to confirm the
round-15 correction blob exists at baseline; no verification claim rests on
it. `~/.omp/agent/agent.db*` and credential/auth files were not opened.

## 1. Obligation table

| id | routed obligation (R15 spotcheck) | integrated anchor(s) | disposition | status |
|---|---|---|---|---|
| V1-a | R15-V1 is routed to operator/host-safety owner, with mado follow-through before any new round (254–255) | `corpus/SOURCES.md:67` (S055, recheck `on-operator-recovery-decision`); `corpus/lessons/round-16.md:75-76`; `corpus/QUALITY.md:103`; `SKILL.md:39-44`; `LOG.md:1179`; `SCORECARD.md:712-716` | operator-owned unresolved + QUALITY21 + standing SKILL pause + S055 recheck trigger | mapped |
| V1-b | No reinstall, downgrade, package removal, full upgrade or service/compositor restart is performed or authorized (264–266) | `QUALITY.md:83-85,95-98`; `SKILL.md:483-485`; both wave contexts (`w1/spec.json`, `w2/spec.json`) | QUALITY21 pause | mapped |
| V1-c | M2 is not resolved by a new paragraph; the incident is not repaired (266; 248) | `round-16.md:14` (“This does not intercept tools or resolve R15-V1”); `SKILL.md:539` (“not prevented or repaired”); `QUALITY.md:103-104` | lesson M1 + criterion + SKILL limit | mapped |
| V1-d | The existing fleet L0 line is the operator decision channel; the lane must not re-own or duplicate it (263–264) | `round-15.md:195-200` (names the L0 entry; “not answered or re-owned”; “No duplicate L0 line”); `round-16.md:92` (“R15-V1 host-recovery L0 remains open”) | explicit operator-owned | mapped |
| V1-e | The host transaction remains a substantive defect; rejected-harmed stands; no promotion/mint/next-round authorization (255–266; closure verdict) | `SCORECARD.md:692-694`; `round-16.md:81-83`; `LOG.md:1193-1198` | round/closure boundary | mapped |
| V2-a | Retain the new-only dry-run requirement in every relevant seat context (268–270) | `QUALITY.md:86-87`; both wave contexts contain the pause + conditional real `pacman -Sp --print-format '%n %v'` sentence; `SKILL.md:483-488` | QUALITY21 + seat contexts | mapped |
| V2-b | Distinguish hard-coded predicate controls from actual plan/installed-package validation (269–270) | `QUALITY.md:93-94`; `SKILL.md:488-489`; `round-16.md:15` | QUALITY21 + SKILL + lesson M2 | mapped |
| V2-c | If an install is later authorized, use the real `pacman -Sp --print-format '%n %v'` plan and complete installed-name comparison; refuse every overlap (271–273) | `QUALITY.md:72-78` (criterion 20); `QUALITY.md:92-94`; both wave contexts | QUALITY20 retained after operator lift; QUALITY21 makes it conditional | mapped (retention wording indirect, see §3.3) |
| V2-d | Present fixtures do not prove the operational step ran (273) | `QUALITY.md:94` (“a hard-coded new-only fixture never proves it ran”); `round-16.md:15`; `SKILL.md:488-489` | QUALITY21 + lesson M2 | mapped |
| V2-e | No install should be performed merely to satisfy the review (273–274) | `QUALITY.md:83-85` (“including installing a tool merely to read its help”); `SKILL.md:42-43`; `round-16.md:15` | QUALITY21 + standing SKILL | mapped |
| V2-f | Carry forward the disclosed `ReviewLibinput` `hyprctl version` call as process debt, not fresh evidence or input-regression proof; do not rewrite filed history (274–277) | `round-15.md:46-49`; `LOG.md:1115-1116`; `round-16.md:15`; `SKILL.md:489-490`; new finite case `safety-cases.json:319-329` | lesson M2 + append-only disclosure | mapped (literal “input regression” absent, see §3.6) |
| V2-g | The round-15 install fixtures are hard-coded controls, not real pacman output, host census, operational prevention or remediation (248–249, 273) | `QUALITY.md:90-94`; `SKILL.md:488-489,533-542`; `safety-cases.json:17,411-430` | QUALITY21 + declared-policy limits | mapped, bounded |
| V14-a | R14-V1 explanatory correction is accepted as landed; historical bytes preserved; no replay (279–280) | `round-16.md:20-22`; `gate-standing-use.md:463-467`; `QUALITY.md:65-70`; `SKILL.md:493-496`; `.ufo/waves/round-15/receipt-correction.json` (`defect: R14-V1`, `status: append-only …`, `no_execution` booleans all false); `round-15-verifier-spotcheck.md:190` | QUALITY 7/9/13 + standing-use erratum + lesson | mapped |
| V14-b | Provisional whole-gate preimages remain unrecoverable; standalone full-gate authority is permanently withheld (279–281) | `gate-standing-use.md:466-467,490` (“not standalone final-full-gate receipts”; “does not recover the excised provisional bytes”); `round-16.md:21-22` | standing-use erratum + lesson | mapped (word “permanently” absent, see §3.4) |
| V14-c | Future mutation evidence binds its actual committed executable/revision; old runs are not relabelled (281–282) | `gate-standing-use.md:502-505`; `QUALITY.md:67` | QUALITY 7/9/13 direct receipt discipline | mapped (measured-commit clause conditional, see §3.5) |

Counts: 15 atomic obligations — V1 five, V2 seven, R14 one group split into
three. 15/15 have a named integrated anchor; 0 are left only as prose in the
R15 spotcheck or only in a wave-1 seat report.

## 2. Evidence notes per group

### R15-V1 — host / operator disposition

- **Ownership is explicit, not inferred.** `SOURCES.md:67` admits S055 as an
  own-work A-tier row whose recheck is `on-operator-recovery-decision`.
  `round-16.md:75-76` turns that into a lane rule: “S055 rechecks when the
  operator records a host-recovery decision; the lane reopens the closure and
  logs the changed authority without claiming repair.”
- **The pause is a standing instruction, not a one-round sentence.**
  `SKILL.md:39-44` names it “Current host pause (round 16; supersedes
  prospective install language below)”, states “no package transactions or
  service/compositor mutations”, says the R15 rejected-harmed closure “is not
  cleared by this source-only round”, and points to QUALITY 21 and lesson
  M1/M2. `QUALITY.md:103` repeats: “The unresolved host-recovery decision
  stays with the operator. No safety trade is erased by this criterion or a
  green configuration gate.”
- **No-contact list is retained.** QUALITY21 forbids “no package transaction
  or host service/compositor mutation” and `SKILL.md:483-485` adds “never
  downgrade, reinstall, remove packages or restart host services.” Both wave
  contexts add “never -Sy/-Syu/-U/-R”.
- **L0 channel.** `round-15.md:197-200` quotes the entry prefix
  `HOST PARTIAL UPGRADE during mado r15` and says the lane does not answer or
  re-own it; `round-16.md:92` records it still open. No duplicate L0 line was
  found in the integrated files.
- **Incident facts are preserved, not laundered.** `round-15.md:26-31`
  records the exact command, the Arch `extra` channel, libinput
  `1.31.3-1 → 1.32.0-1`, the four new packages, and the udev-reload /
  system-update hooks. `round-15.md:18-21` says M2 “is not marked resolved”
  and remediation “belongs to the operator via the orchestrator's L0 routing”.

### R15-V2 — procedural compliance

- **Both seat contexts carry the rule, not only one.** The w1 and w2
  `spec.json` contexts contain, verbatim: “All pacman transactions PAUSED
  host-wide until operator recovery decision: never -Sy/-Syu/-U/-R,
  downgrade or restart services. After pause only operator-authorized future
  install may use real pacman -Sp --print-format '%n %v' plan and complete
  installed-name comparison; any overlap refuses. Hard-coded fixture is not
  actual package validation.” Both also carry “No live compositor, service,
  input-device, screenshot or command producer probes. Source reading only.”
  This satisfies “every relevant seat context” for this round's two waves.
- **Fixture/operational distinction is now three-way.** QUALITY21 line 94,
  SKILL lines 488–489, and lesson M2 line 15 independently say the prior
  in-memory/new-only controls are not a real plan or installed-host
  comparison. The phrase “never proves it ran” is the exact V2-d obligation.
- **The new classifier is not substituted for the install predicate.**
  QUALITY21 says criterion 20's complete comparison still applies after an
  operator lift; it does not let the declared-plan gate stand in for it.
  SKILL's classifier-limit paragraph says the gate “does not intercept actual
  tool calls; the round-15 incident was undeclared/ungated and is not
  prevented or repaired” (`SKILL.md:533-542`).
- **The hyprctl probe is carried as debt.** `round-15.md:46-49` names the
  call, says its result “is not used as fresh round claim evidence”, and says
  no seat is asked to repeat it. `LOG.md:1115-1116` repeats that it “supplies
  no fresh claim evidence.” Round 16 does not rewrite the old report; it adds
  the M2 row. The new gate also refuses `hyprctl` in a declared allow-kind
  action (`safety-cases.json:319-329`, expected `denied_executable:hyprctl`).
- **No package result contaminates C1.** The disclosed round-16
  `pacman -Q waybar` query is recorded as M5 (`round-16.md:18`) with “Do not
  rerun or use the result as fresh evidence.” The U7 note does not cite an
  installed Waybar version; it says the historical host version “does not
  prove installed-binary source equivalence”
  (`corpus/knowledge/waybar-observation-boundaries-r16.md:9`).

### R14-V1 — receipt precision

- **Correction accepted and present.** The outside closure's own table at
  `round-15-verifier-spotcheck.md:190` records “R14-V1 explanatory correction
  … admit correction … agree”. The artifact exists at
  `.ufo/waves/round-15/receipt-correction.json`, 29,021 bytes at baseline
  `32c4fda…`, with `defect: R14-V1`, `measured_commit:
  32118fc1014837b3a385c7a66abbdc59b1560835`, and
  `measured_commit_role: reference source revision for static target
  derivation; not the runtime revision of the three pre-commit mutation runs`.
  No gate/harness/mutant/selftest execution is asserted in its
  `no_execution` block.
- **Historical bytes.** `gate-standing-use.md:463-467` says “Their historical
  headers and TSVs are preserved. They are **not standalone final-full-gate
  receipts**”. The erratum maps each provisional header
  (`ef50e262…`, `d6d5eb27…`) to the `cd1d73d7…` derived target and states the
  run times precede `32118fc…` (06:03:28Z).
- **No full-gate authority.** `gate-standing-use.md:490`: “This static
  relation does not recover the excised provisional bytes.”
  `round-16.md:21-22`: “The committed derived target is not the whole gate;
  unrecoverable preimages remain unrecoverable.”
- **Future binding.** `gate-standing-use.md:502-505`: future standalone
  mutation receipts bind “the actual derived-target, specification and
  harness identities directly, with actual command/time/exit. If measured
  full-gate commit identity exists, record it separately and accurately;
  never stamp a later commit onto a prior run.” `QUALITY.md:67` repeats the
  anti-restamp rule.

## 3. Bounded counterexamples and residual limits

### 3.1 QUALITY21's “disguised forbidden executable” is finite by design

QUALITY21 lines 88–92 require the classifier to fail on “the incident-shaped
libinput transaction, disguised forbidden executable, unknown kind, and
malformed action”. Read alone, “disguised forbidden executable” could be
taken as any disguised command. The integrated boundary is narrower:
`SKILL.md:533-539` says `plan_safe` means only no blocked declared kind and
no listed argv[0] basename; “Unlisted wrappers/interpreters (including
`omarchy-pkg-add` and `python3`) pass the finite screen”. `safety-cases.json`
line 17 states the same scope limit, and its residual controls pin
`omarchy-pkg-add libinput` and `python3 -c …` to `plan_safe`
(`safety-cases.json:411-430`). The finite deny list is twelve basenames
(`tools/mado-action-plan.py:109-111`; `safety-policy.json`). This is a
declared-policy classifier limit, not a promised broad shell guard; no
broader enforcement is demanded by this report.

### 3.2 “Exact observed receipts are appended below” is not yet evidenced

`corpus/lessons/round-16.md:14` (M1 fix cell) says “Exact observed receipts
are appended below.” At this revision the round-16 evidence directory holds
only `census-before.txt` and `source-bindings.json`; there is no
action-plan selftest, plan/policy evaluation or frozen-run receipt file
under `.ufo/waves/round-16/evidence/`. The lesson's Gate section itself makes
actual self-invocation a condition of admission
(`round-16.md:39-42`), and SCORECARD C2 lists the three commands as the
measurement (`SCORECARD.md:703-707`). Therefore the sentence is either
prospective or unsupported now; L1's post-integration verification must
either append the actual receipts at the measured commit or soften it. This
is exactly the fixture/operational-evidence distinction R15-V2 requires; it
is **pending L1 evidence**, not evidence of a green classifier, and not a
mapping gap in QUALITY21/SKILL.

### 3.3 “Preserve the real plan” has no literal preservation clause

R15-V2 line 271 says “preserve the real `pacman -Sp --print-format
'%n %v'` plan and complete installed-name comparison”. Criterion 20
(`QUALITY.md:72-78`) requires obtaining and comparing the plan; it does not
say “preserve”. Criterion 21 (`QUALITY.md:92-94`) makes the comparison
conditional after operator lift and repeats overlap refusal, but also does
not require committing the plan bytes. The general retention rule is
criterion 13 (“Evidence meant to outlive a round is a committed path or
quoted lines plus sha”, `QUALITY.md:19`), which would apply if the plan is
used as claim evidence. Status: operational core mapped; the **retention**
word is indirect. Low severity; adding “preserve the plan and installed-name
comparison as committed evidence” to QUALITY21 would close the literal gap
without a new gate or wrapper.

### 3.4 R14-V1 “permanently withheld” is asserted by classification, not the word

The integrated erratum says the three receipts are “not standalone
final-full-gate receipts” and “does not recover the excised provisional
bytes” (`gate-standing-use.md:466-467,490`); the lesson says “unrecoverable
preimages remain unrecoverable” (`round-16.md:22`). No integrated file uses
“permanently” or “withheld”. The classification has no expiry and is
append-only, so the disposition is substantively mapped; the literal word is
not claimed. No artifact re-authorizes the historical headers as full-gate
proof.

### 3.5 R14-V1 future binding is conditional on measured-commit existence

The erratum makes derived-target, specification and harness identities plus
command/time/exit mandatory, and a measured full-gate commit “if … exists”
separate (`gate-standing-use.md:502-505`). The R15 spotcheck's phrase
“committed executable/revision” is therefore satisfied for the executable
(derived target from committed bytes) and the run identity, but there is no
mandatory `derived_from_commit` field for a future pre-commit run. This is
consistent with the historical pre-commit case (no measured commit exists
for those runs) and with QUALITY 7/9; it is a wording scope, not a
relabelling of the old receipts.

### 3.6 The hyprctl inference ban is carried, but not verbatim

R15-V2 lines 275–276 say the call is “process debt, not fresh claim evidence
or proof of an input regression.” The lane carries “not used as fresh round
claim evidence” (`round-15.md:47`) and “supplies no fresh claim evidence”
(`LOG.md:1116`), and the new gate denies a declared `hyprctl` read
(`safety-cases.json:319-329`). No integrated sentence uses the exact
“proof of an input regression” clause. The evidence ban is stronger in
practice: any regression claim from that call would be a fresh claim, which
is prohibited. Filed history was not rewritten; round 16 added M2 rather
than editing the round-15 report.

### 3.7 The round-15 M2 row still says “in-memory actual-plan control”

`corpus/lessons/round-15.md:15` uses “the in-memory actual-plan control” and
line 18 says the guard “is demonstrated as able to refuse the actual recorded
package-name overlap”. The outside closure judged the disclosed limited
result accurate (`round-15-verifier-spotcheck.md:248-249`), and append-only
discipline forbids rewriting that row. The forward correction is present in
QUALITY21, SKILL and round-16 M2. Residual wording only; no action required
beyond not citing that fixture as production validation.

### 3.8 “Before any new round” is not a lane-enforced gate

R15-V1 line 254 says “with mado follow-through before any new round.” The
integrated artifacts map the follow-through (QUALITY21, SKILL, both wave
contexts) and leave recovery operator-owned (`QUALITY.md:103`,
`SKILL.md:43-44`, `LOG.md:1179`, `SCORECARD.md:714`), but they do not state a
lane-enforced precondition “no future round until operator recovery.” The
lane instead declares “No retirement or next-round mission”
(`LOG.md:1198`) and “No exploratory claim or promotion request”
(`SCORECARD.md:716`). The precondition is therefore operator-owned, not a
lane gate; this is the routed disposition, not an omission, but the literal
round-gating sentence does not exist.

## 4. What this seat does not verify or claim

- No gate, selftest, frozen replay, mutation, measure, census, package or
  service command was run. The action-plan classifier's behavior is read from
  `tools/mado-action-plan.py` and `safety-cases.json`, not observed.
- No claim that the round-15 host transaction is repaired, that the pause is
  enforced by any tool, or that `plan_safe` is host safety. The integrated
  texts explicitly refuse all three.
- No claim that C1/U7 or C2/C3 are measured here; those are L1's
  post-integration verification. The `--frozen` registry row's “receipt
  separately binds executable and expectation digests to measured commit”
  (`SKILL.md:530`) has no current evidence file in
  `.ufo/waves/round-16/evidence/`; treat it as a pending L1 receipt clause,
  not as observed evidence.
- No promotion, SHONEN clearance or outside-review substitution. All round-16
  seats are authoring-lane; the lesson says so
  (`round-16.md:81-83`) and LOG says SHONEN remains four author assertions
  (`LOG.md:1196-1197`).

## 5. Result

All 16 atomic R15-V1/V2/R14-V1 obligations have an integrated anchor.
The operator-owned unresolved items are V1-a/V1-d (host recovery, fleet L0)
and the round-gating precondition in 3.8; these are explicitly left to the
operator, not silently absorbed by the lane. The material residual limits
are 3.2 (pending gate receipts), 3.3 (no literal plan-retention clause) and
3.5 (conditional measured-commit field); none is a contradiction of the
routed text, and none requires unassigned broad shell enforcement.

Report: .ufo/waves/round-16/w2/reports/AttackClosureCarry.md
