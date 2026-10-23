# CritC1Claim — round 27 w3

REVIEW: The completed receipt for the assigned REV records **19/41 TARGET_MISSED**, not the registered 41/41. Predicate identity and byte-preserving landing are supported; neither compensates for that miss. The missing second implementation and unarchived live-HOME input are separate contractual/provenance risks. This is advisory criticism, not a canonical judgment or admission decision.

## Scope and evidence notation

- `R/` = `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-27/`.
- `L/` = `/home/vgpnk/Projects/shokunin/mado-shokunin/`.
- `F/` = `/home/vgpnk/Projects/shokunin/`.
- `D/` = `/fast/scratch/hyaku/mado-r27/data/`.
- Fixed subject: `REV=48b9434a0b0619b3896c9d80e8288ec2226c9ed8`, tool SHA-256 `722c7ae47eaee57eda4c6a223f4dad6fc585018453c2f7a2fd26c52d1e006008`, counter `R/c1/count-v4.py`.

Read registration first, including all retirements, then the three assigned w2 reports. Read the completed after-receipt, counter/harness, landed tool, source rows, four w1 Src reports, relevant fetched source ranges, and v4 control labels. Runtime results below are attributed to existing receipts/reports. No counter, tool, test, compositor, build, or judgment runtime was executed by this seat.

## 0. Strongest actual counterexample: the assigned after-state misses its own finite predicate

`R/evidence/c1-after-48b9434a.txt:1-6` identifies the exact assigned REV, tool SHA, frozen v4 counter SHA `635ae788fd897c8f1fba88e4ab2ffcb95e7f79a88703b82e49a8729ce7d271a1`, seed `b16462f05aa28929`, snapshot digest, and Hyprland v0.56.2 commit. Its final lines are:

```text
HOST_SAFETY hyprland_coredumps_before=1338 after=1338 delta=0
PRED-C1-r27-v4 cases_pass=19/41 verdict=TARGET_MISSED
exit=1
```

Evidence: `R/evidence/c1-after-48b9434a.txt:48-50`. There are 41 case rows (`:7-47`), including 22 FAIL rows, so this is not an absent receipt, setup guard, or partial output.

A concrete implementation defect explains a very strong failure signature. `L/tools/mado-wsrules.py:572-577` finds `on-created-empty:` and passes `field[delimiter + 16:]` to its command normalizer. That prefix has **17 characters**; the slice retains its colon. The pinned handler instead computes the prefix's `.length()` and slices after it (`R/fetch/SrcWsRuleLegacy.bin:1703-1704,1753-1755`); its normalizer forms `[workspace NAME] cmd` (`R/fetch/SrcBoolAndExec-MiscFunctions.bin:478-509`).

**[INFERENCE from the inspected code/source, not a new execution]:** the safe tree `workspace = 1, on-created-empty:kitty` yields tool command `[workspace 1] :kitty`, versus source-derived expected `[workspace 1] kitty`. This shape is inside v4's generated language (`R/c1/count-v4.py:46,118-120`). Every FAIL in the after-receipt bears ONEMPTY; every PASS lacks it (`:7-47`). Correlation plus the slice defect is strong evidence, but does not prove that one repair alone would make all cases pass.

The peer subsequently persisted an execution of that scratch witness: `R/w3/reports/MutWsTool.md:198-213` records pristine tool output `"onCreatedEmpty": "[workspace 1] :kitty"`. That empirically reproduces the tool-side colon retention without running the counter or a new oracle; the expected string remains grounded in the pinned source above. The same report `:183-214` notes that none of its 13 scout trees contains on-created-empty, so passing those probes cannot exonerate this defect. This execution was the mutation seat's, not mine.

**Impacted axes:** C1 coverage correctness; honesty of the after-state claim. **Smallest safe correction:** report the miss without changing the target, seed, population, or receipt. The slicing defect is technically small to fix, but a later repair/new measurement cannot be substituted for this REV's first-returned bytes and one-measurement result. The frozen data rule is `R/registration.md:68-73`; the canonical assignment also says a post-landing miss is an honest stop (`F/.ufo/prompts/mado-round-27.md:350-367`). No repair or replacement was made here.

## (a) Predicate identity: same inherited sentence and implemented condition; same receipt label, not a full sentence in the receipt

### Registration quotation

`R/registration.md:170-172` says:

> **PRED-C1-r27-v4**: the PRED-C1-r27-v2 sentence above, word for word, with the counter `c1/count-v4.py`; target: cases_pass=41/41. Every C1 control (now 13 shapes) is re-scored under v4 with two fresh seeds before any data seat (`controls/v4/<Control>-seed{1,2}.txt`).

The inherited sentence, `R/registration.md:93-99`, is:

> At REV, the committed bytes of tools/mado-wsrules.py, run in the tool sandbox (no network, no /run, cleared environment, the case tree read-only at /snap/home from a randomly named directory), print for the unperturbed snapshot of the four Hyprland config roots and for each of 40 generated cases (25 that add workspace rules to the snapshot, 15 independent trees that contain none of the snapshot's files; cases carry unsourced decoy files, nested and glob sources and source lines placed among rule lines) a JSON array equal, entry by entry and in order, to the array Hyprland v0.56.2 itself prints with `hyprctl workspacerules -j` for the same tree (a nested, headless, session-isolated instance run by the counter on a copy with exec lines removed); target: cases_pass=41/41.

### Counter quotation

`R/c1/count-v4.py:6-14`, under `PRED-C1-r27-v4`, says:

> At REV, the committed bytes of tools/mado-wsrules.py, run in the tool sandbox (no network, no /run, cleared environment, the case tree read-only at /snap/home from a randomly named directory), print for the unperturbed snapshot of the four Hyprland config roots and for each of 40 generated cases (25 that add workspace rules to the snapshot, 15 independent trees that contain none of the snapshot's files; cases carry unsourced decoy files, nested and glob sources and source lines placed among rule lines) a JSON array equal, entry by entry and in order, to the array Hyprland v0.56.2 itself prints with `hyprctl workspacerules -j` for the same tree (a nested, headless, session-isolated instance run by the counter on a copy with exec lines removed); target: cases_pass=41/41.

Those two expanded sentences agree after line-wrap whitespace is normalized. The operative code also agrees: extract the committed tool at REV (`:346-357`), construct BASE + 25 APPEND + 15 SYNTH (`:361-369`), compare JSON lists type-strictly through canonical JSON (`:397-404`), and require every case (`:411-421`). Sandbox details match `R/harness/oracle.py:231-239`; the oracle copies the case and strips exec lines (`:136-145`). The four v4 additions remain explicitly documented in registration `:163-166` and implemented at counter `:152-156,289-315`; inheritance does not erase those population amendments.

### Receipt quotation

`R/evidence/c1-after-48b9434a.txt:49` says:

> PRED-C1-r27-v4 cases_pass=19/41 verdict=TARGET_MISSED

It carries the **same v4 identifier**, not a full English predicate. Thus “all three contain the same sentence” is not literally true; “same sentence in registration/docstring, same implemented condition, same receipt label” is supported. This is the distinction in `F/.ufo/prompts/mado-round-27.md:364-367`, not permission to rewrite an artifact's contents. The printed numerator is an observed result, not a relaxation to a 19/41 target.

### Redesign chain is disclosed, not one unchanged experiment

- v1 retired after FlatScan reached 41/41 twice by scanning every file without following sources (`R/registration.md:81-104`).
- The v2 type-strict comparison/VARREDEF amendment is separately disclosed (`:106-113`); its initial and amended pins must not be conflated.
- v2 retired after PrefixKeyed reached 41/41 twice using the fixture's `$wsr` convention (`:142-154`).
- v3 retired after GlobalOnce and FileScope each reached 41/41 twice; v4 adds VAREMBED, SRCDEF, USEBEFOREDEF and TWICE (`:156-168`).
- The prior control audit agrees with these receipt-based retirements (`R/w2/reports/ReviewControlsC1.md:11-16`). The v2 FlatScan pilot path was overwritten, so the original 9/41 pilot is not independently retained at that path (`:43`); that disclosed historical blemish does not change the present v4 pin or after-result.

**Impacted axes:** claim identity, evidence provenance, premature saturation. **Smallest safe correction:** always name v4 and its pin; retain predecessor retirements and distinguish their scores. Predicate/label identity is a **non-blocker** on the inspected evidence; claiming a v4 success despite the receipt is not.

## (b) Data rule: honest A selection is not the same as completing two implementations

The exact registered rule is `R/registration.md:70-73`:

> C1: two executor seats build `tools/mado-wsrules.py` independently; the first file returned lands unmodified and is measured once with a fresh seed; the other stays a second implementation.

**What is supported:**

1. Two separate executor items and distinct candidate paths were assigned (`R/w2-spec.json:6-14`; `R/w2-run.json:26-37`). Both scratch trees contain source-research artifacts; B's directory contains only `src/`, no returned `mado-wsrules.py`. This supports two attempted builds, not two completed implementations or independent correctness results.
2. The assignment identifies A as first returned at 09:32:04 -03. Its on-disk candidate has mtime `2026-10-23 09:32:04.745151586 -0300`, size 29661. A file mtime corroborates byte finalization; by itself it is not a transport-return receipt.
3. Read-only commit metadata for `48b9434a0b0619b3896c9d80e8288ec2226c9ed8` records: `ExecWsToolA first-returned bytes unmodified (sha256 722c7ae4); ExecWsToolB died with phase-4 orchestrator, no bytes returned`. AuthorDate is 09:32:44 -0300; CommitDate is 15:13:55 -0300. These are disclosed metadata, not an independent proof of return order.
4. This seat directly hashed A's candidate, the lane file, and `git show REV:tools/mado-wsrules.py`: all three equal `722c7ae47eaee57eda4c6a223f4dad6fc585018453c2f7a2fd26c52d1e006008`. The after-receipt independently names that blob (`R/evidence/c1-after-48b9434a.txt:2`). There is no byte-selection discrepancy.
5. `F/.ufo/watchdog.log:931` records the dead mado round-27 attempt and approximate orchestrator death `~09:30 -03`; `:943` records attempt 2 launching at 15:10:22 -03. This is compatible with the assignment's approximate 09:30–09:35 death window, not a second-resolution death certificate. B's source-directory mtime is 09:32:49.750401139 -0300; neither that nor A's mtime establishes a more exact death boundary.
6. The after-receipt is complete and records one seed (`:3,49-50`). It is evidence of this measurement, not independently a global proof that no other run ever occurred or that a supplied seed was fresh.

**Finding:** landing the first returned A bytes unmodified is honest selection under the stated rule. The rule does not require waiting for B to finish before A is selected/measured. But it says the other **stays a second implementation**, not “a source directory counts if the executor dies.” The retained artifacts establish no such second implementation. There is no registered death waiver, best-of-two selection, repair-in-place permission, or authority to replace A after seeing 19/41. Sharing a counter/source contract between seats is normal; it is not evidence of two independent working algorithms.

**Impacted axes:** provenance and fidelity to the pre-data experiment, not the numerical comparator. **Smallest safe correction:** disclose “two builds attempted; A returned and landed byte-identically; B died without an implementation.” Do not describe that as two completed implementations or treat a later post-result candidate as the original B result. Missing B is a **blocker to an unconditional assertion that every data-rule clause was fulfilled**; whether the canonical judge treats that shortfall as dispositive is its decision. It does not make the observed A bytes dishonest or erase their measured miss.

## (c) Controls defeat the documented shortcuts, not the whole cheap-shortcut space

### What the controls actually establish

The 13 names are DoNothing, Junk, Echo, LabelKeyed, StaticBase, NaiveGrep, RootOnly, NoMerge, NoVariables, FlatScan, PrefixKeyed, GlobalOnce and FileScope (`R/w2/reports/ReviewControlsC1.md:7,20-34`). **GlobalOnce and FileScope are already included in the 13**, not two extra independent controls. The audit records 26 v4 seed receipts, plus three pilots, all on the frozen pin (`:7-9`). I also read all 26 seed verdict/header records: every one says TARGET_MISSED; best is FileScope 32/41.

The two requested critic-found pilots are directly confirmed:

| Control | v4 pilot | v4 two-seed rescore |
|---|---|---|
| GlobalOnce | `R/controls/v4/K1GlobalOnce-L1pilot.txt:49-50`: 18/41, exit 1 | `K1GlobalOnce-seed{1,2}.txt:49`: 17/41, 17/41 |
| FileScope | `R/controls/v4/K1FileScope-L1pilot.txt:49-50`: 24/41, exit 1 | `K1FileScope-seed{1,2}.txt:49`: 29/41, 32/41 |

The population genuinely attacks their defects: embedded variables, position-sensitive use-before-definition, definitions escaping a sourced file, and parsing a file twice (`R/c1/count-v4.py:152-156,289-315`). However, StaticBase and DoNothing are behaviorally duplicate on this empty snapshot (`R/w2/reports/ReviewControlsC1.md:40-41`); BASE is a free pass for an `[]` printer. Thirteen named controls are neither thirteen independent semantic distinctions nor an exhaustion proof.

### Strongest remaining paper bypass: ExactBool

**Construction:** an otherwise-correct resolver uses exact alias sets `true/yes/on` and `false/no/off`, with the usual numeric fallback, instead of Hyprland's prefix recognition. This is a short, natural parser shortcut, not fixture-name sniffing or an answer lookup. It exploits the **absence of non-exact boolean-prefix values** from v4: `BOOLS_T/F` contain only exact aliases (`R/c1/count-v4.py:47-48`), and `boolv`/rule generation only select from those sets (`:95-97,123-127`). VAREMBED and source/variable traps move these values around but do not introduce `trueish` or `nope`.

A decisive local witness exists outside that generator:

```text
workspace = 2, persistent:nope, border:trueish
```

The pinned source accepts lowercase prefixes (`R/fetch/SrcBoolAndExec.bin:134-149`); the scout's oracle output keeps this row with `persistent:false, border:true` (`R/w2/reports/ScoutOracleWsSemantics.md:309-328`). An exact-alias parser drops it. The separate w3 mutation report empirically confirms this exact shortcut is killed by the `bools` probe, with 12/13 probe passes (`R/w3/reports/MutWsTool.md:49-60,64-68,136-149`), and explicitly identifies the v4-generator blind spot (`:165-181`). Those are peer-recorded probe results, not my execution or a v4 score.

**[INFERENCE, not a demonstrated TARGET_MET control]:** on v4's generated values this shortcut is observationally equivalent to prefix recognition, so it can skip real semantics without a generator witness. A complete target-met claim would additionally have to establish behavior on the exact snapshot and all other semantics. The unperturbed snapshot's empty table alone does not prove its source bytes contain no unusual rule attempts. The landed tool itself is not an ExactBool shortcut (`L/tools/mado-wsrules.py:205-213`) and already misses the target for an exercised ONEMPTY defect. I do not claim the peer's mutant, or any new control, has scored 41/41 under v4.

A second corroborating blind spot is **exact-key dispatch** instead of substring dispatch: the generator emits canonical keys (`R/c1/count-v4.py:100-127`), whereas the oracle treats `notgapsin:4` as `gapsIn=4` and `myborder:false` as `border=false` (`R/w2/reports/ScoutOracleWsSemantics.md:116-136`; pinned handler `R/fetch/SrcWsRuleLegacy.bin:1713-1733`). Invalid-line transactional rollback and bracketed on-created-empty commands likewise are not established merely by the listed control scores. The scout explicitly did not probe on-created-empty (`:334-339`), so its successful semantic probes cannot override the after-counter's ONEMPTY failures.

**Impacted axes:** discriminating power of coverage evidence; premature saturation if the finite result is promoted to complete Hyprlang semantics. **Smallest safe correction:** retain the frozen finite claim and disclose these boundaries; use the existing scout/source witnesses for diagnosis, not as replacement scoring. No new measured target-met bypass is established here, so the kill rule is not mechanically triggered by this paper argument. Enlarging/replacing v4 now would be a new rule, not a safe way to rescue this measurement. Residual untested semantics are a **non-blocker for an accurately bounded finite claim**, but a blocker to a universal-correctness or “cheap-shortcut space exhausted” assertion.

## (d) Live-HOME input: digest visible, replay bytes not supplied by REV + seed

`R/w2/reports/CritClaimsPreData.md:75-83` raised this exact counterexample: hold REV and seed fixed, change the invoking HOME's Hyprland files, and the population changes.

It remains true in v4. The counter calls `O.snapshot(os.path.expanduser("~"), snap0)` (`R/c1/count-v4.py:358-363`), derives BASE and 25 APPEND trees from it (`:364-369`), then removes its entire temporary tree (`:422-423`). The harness enumerates four live config roots, copies eligible files and hashes relative paths plus content hashes (`R/harness/oracle.py:34-35,65-90`). It does not load an input snapshot from REV or a snapshot archive named by the receipt.

**The digest is visible**, at `R/evidence/c1-after-48b9434a.txt:4`:

```text
snapshot files=79 digest sha256:fe1b2d8ba8e61ec3756fac0820c88ddda861db7f833f1c47e371934efa983727
```

It equals the two requested critic pilots' snapshot digests (`R/controls/v4/K1GlobalOnce-L1pilot.txt:4`; `K1FileScope-L1pilot.txt:4`) and the prior audit's common control digest (`R/w2/reports/ReviewControlsC1.md:9`). This is valuable continuity evidence, not the 79 files themselves. A hash cannot reconstruct missing bytes. No snapshot/archive/manifest-named artifact was found under the round-27 lane directory; more importantly, the frozen command has no snapshot-loading option and deletes its own copy. I have not asserted that no matching copy exists anywhere on the host.

**Answer:** closure cannot re-derive this exact result from REV + seed alone. It also needs the exact external snapshot, the pinned oracle prerequisites, and the recorded tool/counter/harness. A current HOME that happens to have the same digest may permit replay, but that is an additional input condition, not committed-byte reproducibility. Printing the digest solves identification, not availability.

**Impacted axes:** reproducibility/provenance of coverage evidence. **Smallest safe correction:** preserve the exact matching 79-file snapshot if recoverable, identify its digest and immutable location, and make the closure explicitly bind that input. Any counter/input-interface change must be handled openly under the frozen-rule contract; do not silently patch v4 or imply that preserving today's files recreates a different past snapshot. This is a **blocker to the REV+seed/committed-bytes closure claim** (`F/.ufo/prompts/mado-round-27.md:350-352`), not a reason to conceal the already-observed 19/41.

## (e) Sourced status: five genuine openings, necessary supporting sources, no correctness guarantee

`R/drafts/sources-rows.md:7-11` provides five distinct pinned URLs with hashes, sizes, opened dates, scopes, anchors and tool/note consumers. Their roles agree with the opener reports:

| Row | Grounded semantics | Opener/file:line evidence |
|---|---|---|
| S178 | Historical Hyprlang-era assignment/selector documentation, keys and on-created-empty trigger; documentation, not this binary's measured output | `R/w1/reports/SrcWikiWsRules.md:5-23` |
| S179 | Exact-selector replace-or-add versus merging all matching selectors at workspace lookup | `R/w1/reports/SrcWsRuleCode.md:5-27`; `R/fetch/SrcWsRuleCode.bin:25-52` |
| S180 | CSS-like 1–4 gap expansion and `std::stoi` conversion | `R/w1/reports/SrcWsRuleLegacy.md:41-51` |
| S181 | Lowercase prefix boolean/int parsing, not strict aliases | `R/w1/reports/SrcBoolAndExec.md:7-8,16,25,45`; `R/fetch/SrcBoolAndExec.bin:134-149` |
| S182 | Command trimming and bracketed workspace-rule replacement/appending | `R/w1/reports/SrcBoolAndExec.md:9,17-19,26,46`; `R/fetch/SrcBoolAndExec-MiscFunctions.bin:478-513` |

The current registry contains those five rows (`L/corpus/SOURCES.md:190-194`) with the same source identities as the consolidated draft. Temporary S?/S178 proposals in individual opener reports are not extra opened sources or competing final IDs.

**Sufficient for what:** these are real, located foundations for the new workspace-rule operation. Together with already-opened S162 (actual legacy handler) and S158 (JSON serializer), they ground the bounded workspace-specific design. S162's handler was fetched and located this round (`R/w1/reports/SrcWsRuleLegacy.md:28-39`); S158's serializer/iteration anchors are explicitly identified (`R/w1/reports/SrcBoolAndExec.md:10`). The inspected serializer actually includes optional `onCreatedEmpty` (`D/ExecWsToolA/src/HyprCtl.cpp:522-548`). The tool names these sources and limits (`L/tools/mado-wsrules.py:31-58`).

**Not sufficient alone for every tool assertion:** S178–S182 do not establish Hyprlang comments, variables, expression evaluation and source traversal, or the exact serialized table. Those require the additional sources the tool cites (S158/S162/S172/S173 and hyprutils), with their own locators. S182's consolidated row anchors only `MiscFunctions.cpp:478-513`, while the tool docstring also invokes `getWorkspaceIDNameFromString` (`L/tools/mado-wsrules.py:42-44`), which starts at fetched source line 125. This is a traceability boundary, not proof that an opening was fabricated. Existing registry `used-by` cells also do not yet enumerate every tool dependency: S158/S162 name the new note, while S172/S173 still list older consumers (`L/corpus/SOURCES.md:170,174,184-185`). Record exact additional locators/consumer extensions where applicable without rewriting immutable old source anchors (`:5-7`).

The wiki is intentionally historical; it must not override pinned code or oracle observations where they differ (`R/w2/reports/ScoutOracleWsSemantics.md:330-340`). The draft itself labels missing serializer-level claims as inference (`R/drafts/workspace-rules-r27.md:48-58`). Most decisively, the properly opened S182 behavior exposes rather than excuses the landed tool's ONEMPTY slicing error. “Sourced” is not equivalent to “correct,” and JSON equality would not by itself prove source provenance either.

**Impacted axes:** sourced-claim provenance and semantic scope. **Smallest safe correction:** retain the five genuine source openings, distinguish wiki/source/oracle evidence, and close precise extra locator/consumer gaps in the final account. Source-opening identity is a **non-blocker** on the inspected evidence; treating those openings as proof that the failed implementation is correct is not supportable.

## C1-admission risk list

These are review risk classifications, not the canonical Rust judgment.

| Risk | Blocker? | Smallest safe disposition |
|---|---|---|
| Assigned REV records 19/41, target is 41/41 | **BLOCKER to C1 target-met admission** | Preserve and report `TARGET_MISSED`; do not narrow, reroll, replace the candidate, or relabel the receipt. |
| ONEMPTY +16 versus 17-character prefix | **BLOCKER to this implementation's asserted exact semantics**; fixable code defect | Diagnose against the pinned handler; any future correction has a different byte identity and must not be substituted for this experiment. |
| No completed second implementation survives B's death | **BLOCKER to unconditional full data-rule compliance**; canonical treatment reserved | State attempted versus completed builds exactly; no invented B result or post-result best-of-two replacement. |
| A first-returned byte identity | **NON-BLOCKER** | Candidate, committed blob and lane file match; timing precision/return transport is not independently reconstructed by mtimes. |
| REV + seed omits live-HOME snapshot bytes | **BLOCKER to committed-byte replay/closure assertion** | Pin and preserve matching input bytes; digest is already visible but is not an archive. |
| Registration/counter/receipt identity | **NON-BLOCKER** | Same inherited sentence/condition and v4 label; receipt does not literally print the full sentence. Keep v1–v3 retirements explicit. |
| ExactBool/exact-key semantic blind spots; duplicate StaticBase control | **NON-BLOCKER for the finite predicate as written**; blocker to exhaustion/general-correctness rhetoric | Disclose limits. No new target-met bypass was measured; do not change the frozen population after data. |
| S178–S182 openings and supporting S158/S162 | **NON-BLOCKER as source provenance** | Keep scopes and extra locators honest; source validity does not turn 19/41 into 41/41. |

## Review actions and boundaries

Only this assigned report was created; its path did not previously exist. No product, registry, counter, harness, receipt, or sibling report was edited. No tools were installed/upgraded. No git/jj mutation, runtime dispatch, tests, counter rerun, or Hyprland invocation occurred.

Static inspection used `read`, `grep`, `glob` and the following read-only fact commands (absolute paths):

```sh
sha256sum /fast/scratch/hyaku/mado-r27/data/ExecWsToolA/mado-wsrules.py /home/vgpnk/Projects/shokunin/mado-shokunin/tools/mado-wsrules.py && git -C /home/vgpnk/Projects/shokunin/mado-shokunin show 48b9434a0b0619b3896c9d80e8288ec2226c9ed8:tools/mado-wsrules.py | sha256sum

git -C /home/vgpnk/Projects/shokunin/mado-shokunin show -s --format=fuller 48b9434a0b0619b3896c9d80e8288ec2226c9ed8 && stat --printf='%n | size=%s | mtime=%y\n' /fast/scratch/hyaku/mado-r27/data/ExecWsToolA/mado-wsrules.py /fast/scratch/hyaku/mado-r27/data/ExecWsToolB /fast/scratch/hyaku/mado-r27/data/ExecWsToolB/src
```

The first command returned the same full tool digest for all three byte sources; the second returned the commit message/dates and mtimes quoted in (b). Receipt safety delta 0 is the counter's recorded observation, not an independently measured coredump delta by this read-only critic.
