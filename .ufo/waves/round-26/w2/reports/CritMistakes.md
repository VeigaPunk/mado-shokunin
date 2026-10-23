# CritMistakes — round 26 w2

## Scope and result

Reviewed the four `w1/reports/ScribeMistakes.md` candidates, registration's appended corrections/disclosures, and local counterexamples. Axes: **calibration** (true claims and capture attribution), **operability** (gates actually enforce their promises), **freshness/provenance**, and **coverage** (what the finite population establishes). Host safety and confidentiality are no-harm constraints, not benefits to exchange for a passing score.

**CRIT MISTAKES: amend M26-1 through M26-4; preserve the pilot arithmetic correction with an attribution qualification; withdraw the claimed numerical cache bound; add the omitted round-26 incidents below.** This is an advisory review, not a canonical judgment, admission decision, or counter receipt.

All short round paths below are relative to `.ufo/waves/round-26/`. `QUALITY` means `corpus/QUALITY.md`. A proposed failure experiment is **NOT SHOWN** unless an existing exercised receipt is identified. The scribe's future-tense “Show/Demonstrate” wording does not fabricate a run, but every fix cell should explicitly say `NOT SHOWN — proposed` before reuse in the lesson.

## Verdict per candidate row

### M26-1 — KEEP the incident; AMEND capture and fix status

- **Evidence:** round-25 `c1/count.py:132-138` supplies the host runtime/display to `Hyprland`; its `:44-46` explicitly acknowledges windows on the live session. `corpus/lessons/round-25-verifier-spotcheck.md:9-10` records the non-author's refusal to execute it. These establish the unsafe display boundary without rerunning it.
- **Captured-by:** `none` is defensible for an identified private-display/isolation gate. It should not become the broader assertion that round 25 had no safety rules whatsoever. Separate “no applicable isolation gate identified” from the actual detector: operator observation and the non-author's safety refusal. Do not credit a package/action-plan screen as an interceptor for these compositor launches.
- **Strongest counterexample to the proposed fix credit:** zero coredump delta and correct tables do not establish enforced isolation. C1 v1 `:284-288`, C1 v2 `:370-374`, and C2 `:220-225` print `HOST_SAFETY` but do not include its delta in acceptance. They also do not require a passing pilot receipt. Thus “block measurement unless isolation is established” describes a proposed gate, not the present acceptance condition.
- **Fix status:** positive containment evidence exists (`harness/pilot-receipt.txt:10-19`; `w1/reports/IsolationProbe.md:95-115`), but the proposed disposable-display negative control is **NOT SHOWN**. The observed absence of live-session effects is useful evidence, not a demonstrated rejecting guard. A negative test must use only a disposable display and must not recreate the operator-session failure.
- **Smallest safe correction:** retain the incident; distinguish the implemented sandbox method, observational receipts, and unshown fail-closed isolation gate. Identify the exact gate/artifact and its rejected unsafe witness before crediting that gate as repaired. Attribute the approximately 1,330 historical records to the registration/operator account, not to a newly established PID-by-PID causal mapping.
- **Impacted axes:** calibration, operability, provenance; host-safety no-harm.

### M26-2 — KEEP the pilot-period delta; AMEND capture, attribution, and failure demonstration

- **Evidence:** original `pilot-receipt.txt:3-8` lists four failures and a successful item 5 while claiming a five-record increase. The final method separately records `1335 -> 1335`, `PILOT ISOLATED_OK`, `exit=0` (`:13-19`). The scribe correctly refused to infer five individually evidenced failures from that original list.
- **Captured-by:** the host-safety requirement and before/after counts expose an aggregate observation, not a per-attempt accounting check. They would not reject “four attempts, each +1, total +5.” Name the actual manual detectors (`ScribeMistakes`, `ReviewRegistration.md:20-27`); use `none — no per-attempt reconciliation gate` for full capture. QUALITY 10 requires re-derived counts but the global catalog count alone still cannot assign a record to a particular pilot.
- **Counterexample:** another Hyprland process can contribute to the host-wide catalog, and a final stable catalog cannot reconstruct earlier attempts. `oracle.py:60-62` counts every matching executable, not this run's PIDs. It also ignores the catalog producer's return code; a failed query must not be treated as a measured zero (QUALITY 26).
- **Fix status:** the per-attempt ledger and its omission/misattribution test are **NOT SHOWN**. Requiring a real abort to yield exactly one catalog record is not a portable accounting test: catalog policy/timing and concurrent activity are separate from process outcome. The accounting fixture can be exercised offline with synthetic/recorded entries; do not deliberately add host compositor crashes to prove a lesson fix.
- **Smallest safe correction:** split (a) the admitted +5 pilot-period observation/containment incident from (b) the four-versus-five reporting error. Preserve the errata as an author correction, not as a reconstructed per-PID receipt. A demonstrated ledger check must reject a missing, duplicated, or misattributed attempt and separately distinguish successful cleanup from abort outcome.
- **Impacted axes:** calibration, provenance, operability; host safety.

### M26-3 — KEEP as historical precedent; AMEND `captured-by` and the inadequate fix

- **Evidence:** the cited spot-check `:117-131` establishes both object drift and a false count: exactly 12 `Rc*` files plus one residual derivation, not the claimed 14/15 or 15/15. The draft honestly labels this historical, not a fresh round-26 incident.
- **Captured-by:** `none` conflates missing automation with missing rules. QUALITY 9 (`:15`) already binds an audit verdict to a commit/frozen copy; QUALITY 10 (`:16`) addresses re-deriving the count instead of transcribing it. QUALITY 4 (`:7`) governs append-only errata. Their scopes should be stated separately: frozen-object binding controls review identity, not count correctness. Do not claim that the old “after judgment” wording literally prohibited an edit *during* review.
- **Counterexample:** freeze/hash the receipt and report while leaving “all 15 re-checks agree” false. A stale-hash check passes unchanged bytes; an appended correction with a new valid hash can still contain another false count. That is precisely the local failure class, not a hypothetical unrelated threat.
- **Fix status:** no claim verifier or stale-hash red/green receipt is supplied: **NOT SHOWN**. Hashing only the receipt also fails to freeze the prose object actually under review.
- **Smallest safe correction:** bind both reviewed statement and evidence to their frozen versions, and enumerate the distinct re-derived row identities before stating the count. The proposed test needs both a changed-object rejection and an unchanged-but-false-count rejection. Keep it a carried historical defect, not another newly incurred mistake.
- **Impacted axes:** calibration and provenance/freshness.

### M26-4 — KEEP as historical precedent; AMEND `captured-by` and proof strength

- **Evidence:** spot-check `:135-141,207-208` and `w1/reports/R5R6Corrections.md:7-11,27-34` support the missing hardened checks. Round-25 registration now has an appended correction at `:237-239`; that corrects the statement, not the checks.
- **Captured-by:** `none` is wrong for the requested “criterion or rule that should have caught it.” QUALITY 8 (`:14`) already requires existence at the named commit before treating a path as landed; QUALITY 7/24 bind committed producer identity. The manual spot-check actually detected the defect. None of that means a named automated claim gate ran.
- **Counterexample:** restore an arbitrary checker and an unrelated green receipt. An existence-only gate accepts both while the named `MutCheckRegOrder`/`MutCheckReceipt` survivors remain unhardened. Removing a file demonstrates an existence check, not the claimed hardening.
- **Fix status:** the draft's artifact-to-claim gate is **NOT SHOWN**. The correction paragraph is an observed documentation repair; it is not a mutation-killing implementation repair.
- **Smallest safe correction:** cite QUALITY 8 for the absent-artifact failure, distinguish actual manual detection, and require the relevant named-mutant red/green evidence tied to the checker/receipt identity before saying “hardened.” QUALITY 25 (`:138`) already sets the instrument-bite standard; do not establish a duplicate, weaker authority.
- **Impacted axes:** calibration, provenance, operability.

## Verdict per registration correction/disclosure

| Item | Verdict and evidence | Smallest safe correction / failure-proof status |
|---|---|---|
| Host-safety erratum, `registration.md:123-125` | **AGREE on correcting four to five; QUALIFY attribution.** `pilot-receipt.txt:21-25` adds the repeated unpatched-tinywl attempt. Parent history contains the two early pilots and successive unpatched/debug/protocol-debug attempts (`history://MadoR26:97,121,174,186,214`), consistent with the account. The original successful item 5 remains the success; this is five failed attempts *before* it, not reclassification of that success as failure. | Preserve the appended correction. It reconciles the arithmetic/narrative, but supplies no per-attempt coredump IDs or before/after ledger. “Each added one” and “this round's only coredumps” remain author attribution, not independently established by the final count. Ledger fix **NOT SHOWN**. |
| v1 cache-plus-delta weakness, `:129-131` | **AGREE with the stated uncertainty.** “Could meet” and “untested” do not manufacture a target receipt. The cited critic explicitly says no 41/41 shortcut was demonstrated. | Keep that qualification. A redesign is not evidence that the unbuilt shortcut was killed. |
| False all-changing guarantee, `:132-133` | **AGREE; an actual round-26 mistake missing from the draft rows.** `controls/K1SnapshotCache.txt:93,99-100` has unchanged C35 passing and 2/41 overall. This directly contradicts the old semantic-change guarantee without contradicting the comparator or population. | Add a mistake row, with manual `CritC1Design`/control-receipt detection. Existing receipts falsify the old explanation; they do not constitute a failed-guarantee gate. The v2 diagnostic is explicitly non-gating. |
| C1 oracle-version guard, `:146-147` | **PARTIAL REPAIR, not full provenance closure.** v2 `:325-340` requests BASE's version, checks its commit, and exits through `die()` on mismatch. `controls/v2/K1SnapshotCache.txt:7` records the expected commit. C2 `:156-166` still requests only binds and checks repeatability, not version. Parser dependency identity is also not established by that C1 commit check alone. | Credit the implemented C1 check narrowly. Wrong-version rejection is **NOT SHOWN by the cited registration/positive receipt**; do not infer it from a matching-version run or say both counters' authority gap is closed. |
| Claimed cache bound “at most … 21,” `:148-150` | **NOT ESTABLISHED as a numerical success ceiling.** Structural edits do not imply changed expected output. The committed v2 snapshot-cache receipt has `C28 PASS ... changed=no (EDIT:rewrite-animation+NEWSRC)` (`:37`). Thus at least one EDIT still accepts a baseline replay. | Say v2 includes destructive/independent substrates that attack the shortcut, not that every non-APPEND case necessarily rejects a cache. The C28 witness defeats the exclusion argument, **not** an observed 22/41 result; no such score is claimed. A strict ceiling requires a semantic proof or a scored, precisely defined shape. |
| C2 expression/no-harm qualification, `:154-157` | **AGREE as a scope correction.** It now names a 20-case regression sample, not exhaustive preservation, and admits omitted expression rules. `CritC2Design.md:64-95` supports those limits. | Keep finite scope and the original capability identity. This is honest calibration, not proof that omitted behavior is repaired or unchanged. Any observed regression remains harm; it cannot be traded for arithmetic gains. |

## Missing round-26 mistake rows

These are recommended additions by incident, not new permanent IDs assigned by this reviewer. “Captured-by” below distinguishes an applicable rule from an actually exercised detector.

### A. Rendered task bytes were not the complete delivered task

**Verdict: MISSING, CONFIRMED in two sampled deliveries.** The saved renderer task for `ScribeMistakes` (`w1-run.json#/taskCall/tasks/38/task`) ends with its `Report:` instruction. The delivered assignment at `history://MadoR26.ScribeMistakes:13-28` continues with the operator tooling-directive block, including pacman-first installation wording; `history://MadoR26.K1DoNothing:13-28` has the same difference. Shared validated context independently says all pacman transactions are paused. No unauthorized install is established by this review.

**Captured-by:** the swarm skill's as-rendered dispatch rule names the intended boundary, but its validator checks its own composition (`ufo-swarm-wave.mjs:1128-1147`) and emits that text (`:1282-1308`); it does not demonstrate equality to the later delivered envelope. No effective end-to-end comparison is evidenced. The observed suffix does not establish that the L1 manually rewrote a task; the injection point is not established here. These tasks have no terminal `| godspeed` marker, so this is not an observed marker-validation failure.

**Smallest safe correction:** record rendered bytes and authorized transport-added text as separate provenance, and have the authority owning composition reconcile the tooling directive with the specific host pause. Do not claim rendered bytes were delivered byte-for-byte, strip an authoritative operator instruction, or alter routing/contract from this review. A final-envelope comparison using an authorized synthetic appended block is **NOT SHOWN**. Axes: calibration, provenance, operability; host safety.

### B. Cleared child environment did not clear the launcher's proc-visible environment

**Verdict: MISSING, OBSERVED confidentiality boundary failure.** `w1/reports/K1LabelKeyed.md:21-40` reports 261 readable launcher-environment keys, including credential-valued variables, through `/proc/1/environ`, despite the tool's own small cleared environment. The sanitized `evidence-summary.json` independently has 261 keys for both baseline and generated probes. No secret value was read or reproduced by this review. `oracle.py:232-238` uses bwrap `--clearenv` but launches it without a minimal host-side `env=`.

**Captured-by:** the “cleared environment” sandbox promise and K1LabelKeyed's explicit leak-review assignment apply; the probe actually detected it. Random case directories only address logical labels. A 1–2/41 control miss is not evidence that confidentiality is intact. Conversely, this report does not claim a seed/case identity was recovered, credentials were used, a sandbox escape occurred, or the live display was reached.

**Smallest safe correction:** sanitize the launcher environment before starting the sandbox, not merely the eventual child environment, and retain only sanitized incident evidence. A non-secret sentinel-environment negative witness should demonstrate the boundary; it is **NOT SHOWN** for a repaired harness. This is distinct from the label-randomization repair and from compositor containment. Axes: calibration/provenance and operability; confidentiality no-harm.

### C. Pilot verdict is host-global rather than run-scoped

**Verdict: MISSING, OBSERVED false rejection and residue.** `evidence/isolation-probe-pilot.txt:5-8` records delta 0, six leftover directories, `PILOT NOT_OK`, exit 1. The audited receipt `isolation-probe-pilot2.txt:5-16` records four pre-existing empty orphans, the pilot's own runtime directory absent afterward, and again `NOT_OK`. `pilot.py:25-37,78-82` scans every matching process/runtime directory rather than its own run. Its acceptance expression also does not test the printed nested-process count or equality of the printed live-instance counts.

**Captured-by:** the literal pilot gate catches a host-wide leftover condition, not this pilot's failure. `IsolationProbe`'s run-scoped audit separated the causes. Do not substitute `ISOLATED_OK` for those receipts or dismiss the real orphans merely because the current run cleaned up.

**Smallest safe correction:** distinguish run-owned isolation/process cleanup from separately reported pre-existing/concurrent residue, and make the run-owned cleanup facts participate in acceptance. Existing evidence shows the false rejection, not a corrected gate's red/green pair: **NOT SHOWN**. Axes: operability, calibration; host safety/hygiene.

### D. The shared 4 GB hard cap prevented the oracle's own 8 GB limit

**Verdict: MISSING, OBSERVED setup failure.** w1 shared context prescribed `prlimit --as=4000000000`; `K1NaiveGrep.md:44-72` retains `sandbox exited rc=1`, `prlimit: failed to set the AS resource limit: Operation not permitted`, and exit 2. `:74-95` records successful extraction after correcting limit inheritance, then the explicit 4 GB soft / 8 GB hard scoring form.

**Captured-by:** ORACLE_FAIL/exit 2 actually catches setup failure; the rule to retain/retry such runs applies. This is not a tool miss or detector kill. **Correction exercised** in that seat's retained failed/successful commands, but not a newly implemented preflight gate. Align every later instruction with the documented soft/hard distinction; no new abstract wrapper is necessary. Axes: operability and calibration.

### E. Parent display-variable inheritance violated the literal launch rule

**Verdict: MISSING, ADMITTED process-boundary violation, without demonstrated desktop contact.** `K1NoValidation.md:240` identifies two development seeds whose parent Python inherited the session variables, then distinguishes sanitized retained runs. The w1 rule prohibited inheritance for anything started, not only the nested compositor.

**Captured-by:** that exact host-safety rule applies; the seat's disclosure caught the lapse. The downstream explicit oracle/helper environments limit consequences but do not make the parent launch compliant retroactively. Smallest correction: retain this disclosure and sanitize the parent launch as already done; a launcher rejection test is **NOT SHOWN**. Do not invent a live-session breach or erase the preliminary runs. Axes: calibration and operability; host safety.

### F. Overstated generation/provenance guarantees

**Verdict: MISSING as new-round lessons, partly corrected in prose.** Add the actual false all-changing assertion and the unsupported 21-case bound discussed above. Also retain the distinct authority gap: pinning Python/tinywl does not pin the promised Hyprland/hyprlang authority (`oracle.py:48-57,128-160`; C2 `:156-166`). The latter is a **static enforcement defect**, not an observation that the installed version is wrong.

**Captured-by:** QUALITY 3 distinguishes observation/inference; the frozen predicate's named authority is the requirement. `CritC1Design`/`CritC2Design` actually found these issues. Baseline agreement cannot detect a consistently wrong version. A C1 guard exists; C2 is unchanged. Mark any unexercised wrong-authority negative witness **NOT SHOWN**, and preserve frozen counters/receipts rather than repairing them invisibly. Axes: calibration, freshness/provenance, strength of coverage evidence.

The sentinel's additional conditional resource/symlink/locking findings remain risks, not observed incidents promoted into facts by this review (`w1/reports/SentinelHarness.md:9-57`). The concrete proc-environment leak and actual setup/pilot failures above must not be hidden among those hypotheticals.

## Evidence operations and limits

This review used file/JSON reads and targeted searches, not a counter or test run. Particularly decisive operations were:

- `read(.../w1/reports/ScribeMistakes.md:9-12:raw)` and `read(.../registration.md:121-157:raw)` for complete row/correction text.
- `read(.../w1-run.json?q=.taskCall.tasks[]|select(.name=="ScribeMistakes")|.task&raw=true)` versus `read(history://MadoR26.ScribeMistakes:1-65)`; repeated delivery comparison with `history://MadoR26.K1DoNothing:1-120`.
- `read(/fast/scratch/hyaku/mado-r26/K1LabelKeyed-3nzq7oyw/evidence-summary.json?q={baseline_launcher_keys:(.leaks.baseline.pid1_environment_keys|length),generated_launcher_keys:(.leaks.generated.pid1_environment_keys|length)})` returned `261` and `261`. Only sanitized summary fields were queried, not live process environments or credential values.
- `read(.../controls/v2/K1SnapshotCache.txt:1-8,24-51)` supplied the unchanged EDIT witness and `PRED-C1-r26-v2 cases_pass=4/41 verdict=TARGET_MISSED`, `exit=1`. This is the existing seat's receipt, not a fresh score by this reviewer.
- `read(.../evidence/isolation-probe-pilot.txt:1-30)` and `read(.../evidence/isolation-probe-pilot2.txt:1-35)` supplied the literal `NOT_OK`/exit-1 receipts.
- Source reads of `harness/oracle.py`, `harness/pilot.py`, the three counters' acceptance paths, QUALITY, the historical spot-check, and the cited w1 reports supplied the static rule/enforcement comparisons above.

No shell commands, compositor, oracle, counter, gate, build, lint, formatter, alternate judging/model runtime, or subagent were started. No tests were rerun to confirm reported failures. No tooling was installed or updated. Only this requested report was written; no registration, draft, harness, counter, tool, or peer-owned file was edited. There is no process tree from this review to clean up.

Report: `.ufo/waves/round-26/w2/reports/CritMistakes.md`
