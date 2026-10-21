# Round 21 final evidence review

Seat: `MadoR21-2.FinalEvidenceReview`. Read-only residual review. Author-lane advice: not independent admission, not promotion, not a SHONEN mark, not a verdict on any fleet report (none was graded).

- Repository: `/home/vgpnk/Projects/shokunin/mado-shokunin`
- HEAD: `a6cef8984d3815775587ab634ce558e13338b0eb` (`round-21: separate logging message data from configured factories`)
- Tracked `tools/`, `.ufo/waves/round-21/{oracle,resource,corpus,assessment-fixtures}`, and `corpus/` match HEAD (`git diff --stat HEAD` empty for those trees).

## 0. Verdict

**Numeric receipts: accepted as bound measurements of the a6cef89 code. Narrative: not yet accurate. Do not close round 21 on the current committed text until F1–F4 are corrected or explicitly limited.**

- Accepted (reproduced by hash and content): oracle 35/35 primary and 17/17 supplemental at a6cef89; C2 gate 20/20 and byte-identical stdout under C1 base/changed/absent; N/A and digest-check mutants rejected; resource 6/6 clean with zero timeouts, spawn errors, or unparsed counts; 11 legacy scan/frozen suites 247/247; corpus population equal to the sealed base blobs.
- No retcon of the 175 target, no edit to a sealed expectation or population, and no S116–S120 quote or line mismatch was found.
- Blocking corrections:
  - **F1 (High):** the verdict emits exit 0 / `clean` over a Python eval cell whose parse failed, so "clean" is inferred from an internal failure. This is inherited and pinned, not a round-21 regression, but it must be disclosed.
  - **F2 (High):** `logging.*` exact-purity was added in the final commit with no admitted source and no independent oracle case.
  - **F3 (High):** committed HEAD never states the current legacy 175 outcome (166/175); committed lesson prose says round 20's 172/175 "remains".
  - **F4 (Medium):** the git `--dry` removals cite unretained downstream source and are called "measured" with no measurement receipt.

## 1. Axes and attack slices

Four axes, one slice each:

- **A. Binding and freshness** (producer, tool, revision, and sha of every receipt).
- **B. Source scope and quote locations** (S116–S120 and any claim resting on an unadmitted source).
- **C. Target and population immutability, and disclosure** (the 175 target, sealed inputs, what is said about them).
- **D. Error-as-capability and SHONEN** (unparsed, timeout, memory; the four canonical boxes).

## 2. Method and limits

- Read-only. Receipts parsed with `python3 -I` JSON; hashes via `sha256sum`; blob identity via `git ls-tree` on `794aaeb`; retained raw source bodies checked by hash, quote, and line.
- No tool, suite, oracle, resource, corpus, or C2 run. No fixture payload executed; the `eval-memoryerror-is-unparsed` fixture was parsed as inert JSON and its code string counted, never compiled.
- No external source fetch. S116–S120 were checked against the retained bytes in `w1/sources/`. One local read-only check: installed `/usr/lib/python3.14/logging/__init__.py` (not the 3.14.8 admitted tag) for handler dispatch.
- Peer-owned state observed and not touched: uncommitted `SCORECARD.md` (+24 lines from line 1440); untracked `evidence/final/misroot-sweep.txt`, `sources-count.json`, `sources-end.json`; `residual/MadoR21-2.FinalBindingReview/`. Where I cite the SCORECARD I say it is worktree-only.
- Tool installs or updates: **none**. No git mutation, host, package, service, compositor, or private-session call. No delegation or background job. `RULES.md` was not needed.

## 3. Current hashes

Tools, measurers, inputs, and manifests (full sha256):

| Path | sha256 | Binding note |
|---|---|---|
| `tools/mado-tripwire.py` | `46c82902896da0ec0ebd54254b1891667fa5da48f8cb297ee08bfb337e34c8c1` | = a6cef89 blob = `tool_sha256` in a6cef89 receipts |
| `tools/mado-assessment.py` | `66aefd03f25d834fbfcfee6b295c1c032f01b2a94ca321396b7558cca59de9d4` | unchanged since d1a5d82 |
| `.ufo/waves/round-21/oracle/measure.py` | `4eb893d2337a4aa758d14c064a855032737c6e2b2b1239d7ca3502042c6c82da` | = `runner_sha256` |
| `.ufo/waves/round-21/oracle/expected.json` | `fd2bfbc86897e1ee7a79302f6ccf6c3403709b132180864a0674f8212925576f` | no commit since b96d1b8 |
| `.ufo/waves/round-21/resource/measure.py` | `6d0362e1920b8c8f010bd83619f9b6c15fb705a67614a7c9b5d5d314937987d4` | = `runner_sha256` |
| `.ufo/waves/round-21/resource/manifest.json` | `2d479fed13cf852c4243c6ffccb48a39b37d32095b5422a8b7913fdbfa3a0ff4` | no commit since eaec245 |
| `.ufo/waves/round-21/assessment-independence.py` | `4e289793a1664f9feb74a2506e142334c06a0e1776f7a9dd3c71f2933269f77d` | = `runner_sha256` |
| `.ufo/waves/round-21/assessment-mutation.py` | `094e79222427e6ffc7bcc9a9aebfbb58fb803cee3cbd617934caae7346db6c4b` | = `runner_sha256` |
| `.ufo/waves/round-21/corpus/compare.py` | `60cef7bebe6eef0bbf09448fec70f1b55375b5f511aad4c968dc22ee4036a653` | = corpus-final `runner_sha256` |
| `.ufo/waves/round-21/corpus/snapshot/manifest.json` | `8e1cf206c85563b418630ef1d094559a9522431ff4e077ca1b51f249436a1377` | = `manifest_sha256`; 1356 files, 17,478,844 bytes |
| `.ufo/waves/round-21/assessment-fixtures/seal.json` | `99516c349637f2aefaef5c106ec7973c8af638bd4a22c79c835a49e0559fe686` | = `SEAL_SHA` in the gate |
| `.ufo/waves/round-21/assessment-fixtures/expected.json` | `aa691e53f2771a79a7fa185fb56a0b949f7893b129e4fd8eaecd108c02f33a5e` | = `actual_expectations_sha256` in receipts |
| `.ufo/waves/round-17/tripwire/w2-regressions/expected.json` | `8a98c12b706203b710e9075117e0883987a453da4fa59ba156894de86b9ebd2e` | pins `eval-memoryerror-is-unparsed` (want_exit 0) |
| `.ufo/waves/round-20/precision/expected.json` | `1039c4fa6ede43b1f08cca231e6c713aa032722e4955f89dbd8b8f3de092254f` | 175-case target; unchanged since base |
| `.ufo/waves/round-20/precision-heldout/expected.json` | `78b168b0db86502df23b6204a5a9a3e1f53189df5cf0257fef6c1d1214b3901a` | unchanged since base |
| `.ufo/waves/round-18/frozen/expected.json` | `4f3534ae33d8daba7d8c682e1fc97c283185667c4f3c3c91235cc53498fd2ed9` | unchanged since base |
| `.ufo/waves/round-19/frozen/expected.json` | `50d2a45e2602cb430b94043f6c658204b0b1802e8c1931cb2a3eda167af02435` | unchanged since base |

Retained raw source bodies (`w1/sources/`):

| Source | sha256 | Matches row |
|---|---|---|
| `L1Partial/functools.rst` | `e938fb679d763ffc02472865a1ffbd816d0f4665068d1419b2d3ac6d1a9fbc31` | S116 |
| `SourceImap/imaplib-v3.14.8.py` | `855d205bf68e202e963db64942549b1fab17b14b594dd16694b8340d453bc74b` | S117, S119 |
| `SourceGitCommit/git-v2.56.0-builtin-commit.c` | `e566f2092ed52b6a1afa87ed62cd5bed7d18dd9723a990fcca9265ad46a18025` | S118 |
| `SourceNamespace/cpython-v3.14.8-executionmodel.rst` | `11f99f83d785ac174dc02aaf26e03eb91813b38c213729c0017b5a3a70a2eb89` | S120 (and S111) |
| `SourceGitAdd/add.c` | `c96956fdbba0943e3458fd19eaad9e5a21e9953b42f03109abb17b023f76c09b` | no SOURCES row (see F4) |

Committed lane documents, unchanged in worktree:

- `corpus/SOURCES.md` `c66ca4f5c6b45a2e7b9927103f6a24930df17c8b540a074ad387f95b6d3e2cf0`
- `corpus/lessons/round-21.md` `e513b26fa74ee31aa883fd2748b5ddbc0756fdab263df04a2879ab139f661550`
- `corpus/knowledge/tripwire-binding-boundaries-r21.md` `c3d6ca329b1ddd7a8cff140b5326c4f7155a4478e52dfede7564f72f5f54d697`

Receipts in `evidence/final/` (all 37 files; full sha256 in Appendix A).

## 4. Binding matrix (slice A)

| Receipt | measured_commit | Producer / tool binding | Status for HEAD |
|---|---|---|---|
| `oracle-delivered-a6cef89.json` | a6cef89 | tool `46c829…`, expected `fd2bfb…`, runner `4eb893…` | **current**: 35/35, 17/17, 52 cases, 0 unparsed, 0 errors |
| `assessment-delivered-a6cef89.json` | a6cef89 | gate `66aefd03…` | **current**: 20/20 |
| `assessment-na-a6cef89.json` | a6cef89 | gate `66aefd03…` | **current**: exit 1, `unnamed_nonauthor_verifier` |
| `assessment-independence-a6cef89.json` | a6cef89 | gate `66aefd03…`, runner `4e2897…` | **current**: 3 states, identical stdout sha `1e58c91b…`; C1 shas `a57d4fe9…` (base), `46c82902…` (changed), absent |
| `assessment-mutation-a6cef89.json` | a6cef89 | runner `094e79…`, source `66aefd03…` | **current**: mutant `8eeb4b51…` exit 1, `pass: true` |
| `resource-after-module-main-a6cef89.json`, `resource-after-cli-a6cef89.json` | a6cef89 | tool `46c829…`, runner `6d0362…`, manifest `2d479f…` | **current**: 6/6 exit 0, clean, zero findings and zero unparsed |
| `precision-legacy-a6cef89.json` | a6cef89 | tool `46c829…` | **current**: 166/175 (see F3) |
| `recall-legacy-a6cef89.json` | a6cef89 | tool `46c829…` | **current**: 6/6 |
| `frozen-round-19-a6cef89.json` | a6cef89 | tool `46c829…` | **current**: exit 0, `frozen_match` |
| `frozen-round-18-a6cef89.json` | a6cef89 | tool `46c829…` | **current, red by design**: exit 1, `frozen_verdict_mismatch`, `missing_findings=[]`, 3 extra `pacman:-Q` rows |
| `suite-*-a6cef89.json` (11) | a6cef89 | `SELFTEST_SCRIPT_SHA256` `46c829…` | **current**: each exit 0; 247/247 total |
| `corpus-final-a6cef89.json` | a6cef89 | after `46c829…`, before `a57d4fe9…` (= a8960de tool), runner `60cef7…`, manifest `8e1cf2…` | **current** |
| `corpus-adjudication-a6cef89.json` | a6cef89 | `receipt_sha256` `57eb2590…` = corpus-final file | **current**, author static review, not independent |
| `oracle-verified-a1e1b60.json`, `resource-after-*-a1e1b60.json`, `precision-legacy-a1e1b60.json`, `recall-legacy-a1e1b60.json`, `assessment-independence-a1e1b60.json`, `assessment-na-a1e1b60.json` | a1e1b60 | tool `8b795d…` (pre-logging change) | superseded by the a6cef89 counterparts |
| `assessment-verified-a1e1b60.json` | a1e1b60 | gate `66aefd03…` | still valid for HEAD: gate unchanged since d1a5d82 and does not read the tripwire |
| `guards-legacy-a1e1b60.json` | a1e1b60 | tool `8b795d…` | **not re-measured at a6cef89** (F6) |
| `oracle-final.json` | ac16f10 | tool `0e685f…` | retained historical failure: 16/17, exit 1 |
| `resource-after-cli.json`, `resource-after-module-main.json` | ac16f10 | tool `0e685f…` | historical (pre-M12) |
| `assessment-final.json` | ac16f10 | gate `66aefd03…` | historical duplicate of the delivered result under a misleading name (F7) |

Also: all 24 `*-a6cef89.json` receipts are untracked (`??`). Their binding rests on the `measured_commit` field and the hashes above, not on git history (F7).

Sealing checks (slice C):

- Corpus snapshot: 1356 files, all sha256 equal to manifest rows; all git blob ids equal the `794aaeb` tree; regular `.jsonl` blob census at `794aaeb` is 1356 (the two extra `.jsonl` entries are symlinks, excluded by the manifest rule); sum of `size_bytes` = 17,478,844. Commit touching the snapshot since base: `7afc78a` only.
- Oracle inputs added in `b96d1b8`, no later change. `expected.json` unchanged since `b96d1b8`.
- Assessment fixtures and resource manifest: only `eaec245`.

## 5. Findings

### F1 — High (axis D). Verdict emits clean over a Python eval cell whose parse failed. Inherited, pinned, not disclosed at the verdict layer.

Evidence:

- `tools/mado-tripwire.py:2101–2106`: `compile(..., PyCF_ONLY_AST)` sits in a `try`; `except Exception: return hits, 1, 0`. So `eval_unparsed` is incremented and the Python body is never scanned. Only `!` shell lines survive.
- `tools/mado-tripwire.py:2728–2733` (`verdict_of`) and `:2751` (`run_scan`): the exit code and label depend only on `findings`. `eval_unparsed` and `unparsed_spawns` never change the exit or the label.
- Contrast: exceptions raised during analysis propagate to `__main__` (`:3267–3282`) and become exit 2 `could_not_evaluate`. Compile-time and analysis-time internal failures therefore get different verdicts.
- Pinned old want: `.ufo/waves/round-17/tripwire/w2-regressions/expected.json:357–363` — `eval-memoryerror-is-unparsed`, `want_exit: 0`, `want_findings: []`. The fixture is a 20,003-character Python expression (`x=` + 20,000 `-` + `1`); after-run stats show `eval_unparsed: 1`. `suite-w2-regressions-a6cef89.json` passes 30/30 including this case.
- Corpus at a6cef89: 88 of 1,249 evaluated files carry a no-finding label with unparsed counters (before: 101 of 1,248). `clean` is not the same as "no host command ran" here.
- Tool header (`tools/mado-tripwire.py:32–37`) qualifies `clean` for non-literal spawn arguments and JavaScript eval cells, but not for Python compile failures.

Assessment: this fails the contract's check "no capability inferred from unparsed/memory errors" at the verdict layer. Round-21 receipts do not claim a capability from it: the oracle comparator fails any unparsed case (`oracle/measure.py:63–64`), the resource runs require zero unparsed, and the corpus keeps all 108 error pairs out of the clean count. Exploitability is contingent: a hidden spawn would need the executing kernel to accept code that the tool's `compile()` rejects. No receipt measures that differential [INFERENCE].

Fix path: disclose as a known limit in the closure text, with the eval-memoryerror case named. Changing the verdict is a re-pin of old wants (round 17/18/19 `unparsed-clean` cases) and must be a recorded future change, not a silent edit. Add a Python compile-failure line to the header.

### F2 — High (axis B). `logging.*` exact purity added in the final commit with no admitted source and no independent oracle case.

Evidence:

- Diff `a1e1b60..a6cef89`: `tools/mado-tripwire.py:1526–1528` adds `logging.debug/info/warning/warn/error/exception/critical/fatal/log` to `PURE_STDLIB_EXACT`, with the comment "literal message argv is data".
- `corpus/SOURCES.md` has no row mentioning logging. S116–S120 cover functools, imaplib, git commit, and executionmodel only.
- Only supporting fixtures are author-generated round-20 `AdvPureShapes`: `AP-ap04` (`from logging import info; info(['git','push'])`) and `AP-ap27` (`from logging import info; frozenset = info; frozenset([...])`). Both leads at a1e1b60 (`guards-legacy-a1e1b60.json`, `pure_rows_files`) are cleared by this exact-name addition alone, and `corpus-adjudication-a6cef89.json` `pure24_final` reports 24 cases, 0 finding rows.
- The 52-case oracle has no `logging.info` purity case. `LoggingData` and `LoggingFactory` concern `dictConfig` only.
- Local stdlib (read-only): `Logger.addHandler` at `logging/__init__.py:1688`; `Logger.callHandlers` calls `hdlr.handle(record)` at `:1730–1746`; `Handler.handle` calls `self.emit(record)` at `:1011–1027`. So `logging.info` reaches the `emit` of any handler attached in the process.
- The round-21 knowledge decision table (`corpus/knowledge/tripwire-binding-boundaries-r21.md:17`) says that a reached protocol must be inspected for its special method. Handler `emit` is such a protocol, and the purity addition does not follow it.
- The claim appears in `LOG.md:1435` and in `corpus/knowledge/tripwire-precision-r20.md:146` as "literal-data consumers" with no logging source.

Consequence: a new negative inference ("no finding") in the final code with no source. A visible handler class whose `emit` spawns a process, attached within the scanned text, is a candidate false negative [INFERENCE — not executed].

Fix path: admit a 3.14.8 raw-source row for logging dispatch with located quotes, or narrow the list to exclude dispatch-capable entry points, or add a supplemental oracle case for handler-mediated spawn. State the scope in SOURCES and the knowledge entry.

### F3 — High (axis C). Committed HEAD omits the current legacy 175 outcome, and committed prose says 172 "remains".

Evidence:

- `precision-legacy-a6cef89.json` and `precision-legacy-a1e1b60.json` both give **166/175** with the unchanged wants: P 66/66, S 17/17, W 21/22, H 47/52, L 15/18.
- Failing IDs, 9 total. Three are the round-20 misses: `W-CaseWrapperForms-class-method-instance`, `L-AdoptW2-AdvHelperFn-b14`, `H-AdoptW2-RerunPrecision-corpus-jj-var-verb-help`. Six are new against the round-20 "after" state of 172/175 (H 51/52, L 17/18): `L-CasePureCrossCell-reset-clears-helper`, `L-CaseLeadsInvisible-reset-cleared-helper`, `H-CaseDryRunBash-commit-dry-run`, `H-CaseHelpDryRunEval-pct-bash-dry-runs`, `H-AdoptW2-AdvVcs-p33-git-dryrun`, `H-AdoptW2-RerunPrecision-corpus-git-commit-a-dry-run-short`.
- The two L cases correspond to adjudicated removals in `corpus-adjudication-a6cef89.json` (`CaseLeadsInvisible--reset-cleared-helper.jsonl`, `CasePureCrossCell--reset-lead.jsonl`). The four H cases are dry-run VCS forms, attributed in the worktree SCORECARD to the strict commit/index-write boundary and resting on S118 plus `GitCommitZn`. They are not in the removal-side adjudication.
- `corpus/lessons/round-21.md:25` (Start-census section): "Known old-target disposition: round20 remains 29/175→172/175, three unchanged failures and rejected-harmed." Read at HEAD, that is the only current-state-looking statement, and it is wrong for a6cef89.
- HEAD `LOG.md` and HEAD `corpus/lessons/round-21.md` contain no "166". HEAD `SCORECARD.md` has no "Round 21 — measured delivered-code results" block. The disclosure ("now 166/175 under the unchanged historic wants … six additional disagreements") exists only as an uncommitted worktree edit (`SCORECARD.md:1451–1458`).
- No retcon found: the 175 expectation sha is unchanged since base; `tw-precision.py` is unchanged since base; the gate's `round20_target` 175 and `round20_pass` 172 (`tools/mado-assessment.py:151–155`) are historical constants, not measurements.

Fix path: append-only correction in the lesson and LOG naming 166/175, the nine failing IDs, and the six new ones, with their attribution. Do not edit the 175 target. Do not describe any round-21 state as 172/175.

### F4 — Medium (axis B). Git `--dry` removals rest on unretained downstream citations and are described as "measured".

Evidence:

- `corpus-adjudication-a6cef89.json` rows `git-add--dry.jsonl` and `git-push--dry.jsonl`: `false_positive_removed`, reason "unique --dry abbreviation is a measured non-write control under the frozen Git2.56 fixture context".
- No measurement receipt exists for either row. The corpus comparator does not execute fixture payloads, and no run for these forms is recorded.
- The only git-add support is supplemental oracle `GitAddDry` (`want: []`). Its rationale cites `builtin/add.c:262, 571–576, 690–692` and `read-cache.c:734, 792–795, 807–808`.
- `w1/sources/SourceGitAdd/receipt.json` retains only `add.c` and states: "the actual object-store write/no-write behavior is implemented downstream and is not established by this file alone." No `read-cache.c` raw body is retained. No SOURCES row admits `builtin/add.c` or `read-cache.c`; S100 is the documentation row only.
- `git push --dry` has no source row at all. S104 concerns jj.
- Direction: removing a write finding is a fail-open change. The primary 35/35 does not depend on `GitAddDry`, which is supplemental.

Fix path: change "measured" to "source-reasoned (supplemental)", and either retain and admit `read-cache.c` and `builtin/add.c` at v2.56.0 with located quotes or downgrade the removal to "source support pending". Add a git push source or drop the push removal.

### F5 — Medium (axis A). Knowledge entry is bound to a superseded candidate.

Evidence:

- `corpus/knowledge/tripwire-binding-boundaries-r21.md:2`: "production candidate f499a8db7171b7476fe9f204ab9edbac5a956fa9, measurement receipts are cited separately below".
- The body cites candidate receipts: `oracle-candidate.json` and `assessment-candidate.json` (843d301), root `resource-after-*.json` (843d301), `corpus-comparison.json` (2ac0f9b). It says "final receipts govern" without naming any of the a6cef89 receipts.
- HEAD is a6cef89. The entry is committed and unchanged.

Fix path: append a binding line naming the a6cef89 receipts above and marking f499a8d as superseded.

### F6 — Medium (axis A). Legacy A2 guard measured only at a1e1b60.

Evidence:

- `guards-legacy-a1e1b60.json`: tool `8b795d…`. Recall-lost 0, crash-flip 0, a2 mismatch 0, vcs_fn 0, dup_rows 0, pure_rows 2, `vcs_fp` 26 (LOG says 20 before).
- No `guards-legacy-a6cef89.json` exists. a6cef89 changed the tool (F2), so the recall, crash, a2, and vcs populations are not measured at delivered code. Only the pure24 population is rechecked at a6cef89 (`corpus-adjudication` `pure24_final`).
- `LOG.md:1435` does bind the guard numbers to a1e1b60 explicitly. The worktree SCORECARD line "Legacy screens at delivered code remain unchanged populations" overstates for the guard counts.

Fix path: run the A2 guard at a6cef89 with the existing harness (about 91 s at a1e1b60) or qualify the SCORECARD sentence.

### F7 — Low (axis A). Naming and process binding.

- `assessment-final.json` is measured at ac16f10. It differs from `assessment-delivered-a6cef89.json` only in `measured_commit` and `seconds`. The name suggests it is the delivered receipt; it is not.
- All 24 `*-a6cef89.json` receipts are uncommitted. Binding is by content: `measured_commit` plus the hashes in §3–4. The parent should commit them with this report.
- `oracle-final.json` (ac16f10, exit 1, 16/17) is a retained failure. Keep it.

### F8 — Low (axis D). CLI path under the 384 MiB cap is not receipted for deep recursion.

- `tools/mado-tripwire.py:3253–3258`: when `RLIMIT_AS` ≤ 512 MiB, the worker thread stack becomes `min(64 MiB, max(8 MiB, ceiling // 4))` and the recursion limit is 50,000.
- The resource receipts use flat assignment fixtures. The corpus comparator runs the tool in worker mode (`corpus/compare.py:41–42, 77`), which bypasses `__main__`. The 20 corpus `RecursionError` rows are worker-mode. So no receipt exercises a deep-recursion input through `python -I tool --scan` at the capped configuration.
- Residual: whether that path yields exit 2 as designed or a crash remains unmeasured [INFERENCE: controlled recursion usually surfaces as `RecursionError`].

### F9 — Low (axis D). SHONEN and C2 independence are lexical assertions; already disclosed.

- Verified: `tools/mado-assessment.py:20–25` `SUBJECTS` 1–4 equal the four boxes in `SHONEN.md` (lines 5, 7, 9, 11).
- The screen at `:143–144` is a substring test on evidence. A wrong-topic row that embeds the canonical string passes. The tool docstring and the knowledge entry both disclose that it checks the declared subject, not evidence sufficiency.
- Oracle independence is self-asserted (`independent` flag and the `'tool-generated'` substring test, `:121–122`). Disclosed. Keep the disclosures; no action beyond that.

## 6. Checks that passed

| Check | Result |
|---|---|
| Oracle, delivered | 35/35 + 17/17; tool, runner, and expected shas match; 0 unparsed across 52 cases; `oracle/measure.py:63–64` fails unparsed, error, or timeout |
| Oracle, history | a1e1b60 35/35 + 17/17; ac16f10 35/35 + 16/17 retained |
| C2 gate | selftest 20/20; N/A mutant rejected with `unnamed_nonauthor_verifier`; digest-check mutant rejected; three C1 states give identical stdout |
| Resource | six runs exit 0, `clean`, zero findings, zero unparsed, no timeout or spawn error; fixture shas unchanged; RSS module-main 20,292/22,852/28,904 KiB and CLI 29,200/31,748/38,916 KiB |
| Legacy screens | recall 6/6; frozen r19 `frozen_match`; frozen r18 `frozen_verdict_mismatch` as recorded, `missing=[]`, 3 extra `pacman:-Q` rows, same as `harm-watch` baseline; 11 suites 247/247 |
| Corpus | 1356 files = manifest = base blobs; 836 retained, 104 added/relabelled, 31 removed/relabelled; 0 new error flips; 108 error pairs = 86 `CouldNotEvaluate` + 20 `RecursionError` + 1 `TimeoutError` + 1 `MemoryError` that became evaluable; all 31 removed/relabelled rows adjudicated (10 false-positive removed, 19 evidence relabel, 2 binding correction) |
| Sources | S116 `functools.rst:429` "delegated to the underlying descriptor, and an appropriate" (8 words); S117/S119 `imaplib.py:1809–1812` Popen with `shell=True`, class at 1783, `open` at 1800; S118 `commit.c:1434` `prepare_index(…, 1)`, `dry_run_commit` 1428–1438, dispatch 1836–1838; S120 `executionmodel.rst:249` "Most annotation scopes are *lazily evaluated*. This includes annotations," in the 240–256 section. All hashes equal the SOURCES rows. |
| Historical 175 | expectation shas unchanged since base; gate history constants 175/172 |
| Sealed populations | snapshot, oracle inputs, assessment fixtures, resource manifest unchanged since their seal commits |
| SHONEN | subjects 1–4 equal `SHONEN.md`; round-20 wrong-topic fixture (claims / no-harm / sources / mistakes) fails with `wrong_topic_shonen`; corrected fixture passes with all boxes still `[~]` |

Note on the 104 added/relabelled rows: they are detector output, not truth-adjudicated. The round-21 obligation covers only the removed side, so this is consistent with the stated scope, but no "no harm" statement can rest on them.

## 7. Residual risk and verification gaps

- Not run: any tool, suite, oracle, resource, corpus, or C2 re-execution. No eval-kernel-versus-tool compile differential (F1). No CLI deep-recursion probe at the capped configuration (F8). No A2 guard re-run at a6cef89 (F6).
- Source scope: S116–S120 verified against retained bytes only. No live-URL check. The logging dispatch read used the installed 3.14 stdlib, not the admitted 3.14.8 tag (F2).
- Worktree state can change while this report is read. SCORECARD.md was uncommitted at review time; my conclusions about it describe that state.
- Oracle primary denominators are lane-authored proposals, not outside truth. C2 authenticity and chronology are not established. Both are disclosed by the lane, and neither is graded here.

## 8. Recommended order of corrections (for the main agent)

1. F3: append-only lesson and LOG correction naming 166/175 and the nine IDs; commit the SCORECARD round-21 block with it or withhold it.
2. F2: admit logging dispatch sources or narrow the purity list; add the purity case to the scope text.
3. F1: disclose the eval-compile fail-open as a known limit in the closure text; open a future change to verdict semantics as a recorded re-pin.
4. F4: relabel "measured" to "source-reasoned"; admit or retain the git sources or downgrade the removal.
5. F5, F6, F7: binding lines and the A2 guard run or qualifier; commit the 24 receipts with the report.

## Appendix A. Full sha256 of `evidence/final/` as read

```
0120e3908f4f63160d48aab1b92f171b419aacde63baf7bfcef97ec46bdb617f  assessment-delivered-a6cef89.json
9da82eb00e8f119aa811f61eedebe77de1164bcba2c27da471acc2603182bca4  assessment-final.json
d015562e9604d80f13c02ad025d5638c8440557d86af087297bfe89c7ad89668  assessment-independence-a1e1b60.json
d808944c35a1d4688ba17564f5372c5b6c33219f0c1e196b75ed41ac9b5e791b  assessment-independence-a6cef89.json
2146cb111672728c73774365e30b0bf19c9ab3e0bf54da1f8832dd96e9c8518f  assessment-mutation-a6cef89.json
a013156bc2d2f5fc6fd1e8d21e30c09a401bf747d1d480cecc53fe8618ce7c7f  assessment-na-a1e1b60.json
0556b25674aa0d5a1ac857f48b84536d6c420bc5d90e2693cd41146add0de3d9  assessment-na-a6cef89.json
e3db874daff91e3ff54b0f8d4f385aa118d45fb01d5789b3c358928ad79d7825  assessment-verified-a1e1b60.json
34abe2fcd2161b24039b6e459c30c64f167250da206d9f552efbb644a36f58aa  corpus-adjudication-a6cef89.json
57eb2590cff07fae9044f355ffeedc6028c64f9da805418e7922ed33bd56d803  corpus-final-a6cef89.json
b23bf6f6ad1d4a543fdf568bdc4abd4a271b02bee12cab3f01e057a29aac9cb9  frozen-round-18-a6cef89.json
4f5be16591be6576cf8c382015446b9f0e4de7c819df5bfa9d6e2ef93f50af7a  frozen-round-19-a6cef89.json
07a448aad2c7fd7ae158cd7cf1db7df73b392554376cb7d28cab7daf20c52d38  guards-legacy-a1e1b60.json
55a301fdc2aa00a43290bf90e8ac59f8e6e90b51254074de86e209c4897c6dc4  oracle-delivered-a6cef89.json
7f526025770dd1d148f88c38b0820565a5f83a6b6ee9c5a3300e1f9f15fc568f  oracle-final.json
b1d7497cc96da72a8679e48f83d87b287f68f919a93cd9d2f70a745fcea75705  oracle-verified-a1e1b60.json
ce0339eb30f05c7b136e3ccf8eb31bef37d69d9cc93dc2167229162e212f7529  precision-legacy-a1e1b60.json
77decd494aee0877aabbcedffddb11a6a39a985fb430bc289ae88b7a046e1609  precision-legacy-a6cef89.json
5d0ac70565d3b00bb1e0facd32940c799c04a6a7ba65cae624b2d941535ce42a  recall-legacy-a1e1b60.json
a12b0d96fd06c6ae0d29cc97cb6abb8e83264a516a4e1822ce504b604d033f52  recall-legacy-a6cef89.json
1f3355641a1d75656af105da66fa734afc6670d4d5793f06c0305e1f16c6b389  resource-after-cli-a1e1b60.json
4f658e1965276f3a26eea1dad6bf24f9d750e7c3197971f85042b5b488513dad  resource-after-cli-a6cef89.json
6cd97f5f7206731b2347cc90c7c8f856db1784437eae3adeacfcc5ea2915f18b  resource-after-cli.json
037b3b2a3fb71d21b6b7e6fc2cebaacbb60a19ae33aa6823d4e47fbb69fb430e  resource-after-module-main-a1e1b60.json
2d0ddc1cf3bd6a3a3e76c72d984cb8151e3d786636377e264b0693afa491f0ad  resource-after-module-main-a6cef89.json
d4fe3d4008eddce0066a7ff257dfff35824e79ad5789a32e2583262a1a0a0ad7  resource-after-module-main.json
937684b6f2e7d924fb63e898e461e087034aee04edc52f44a9c755a4a9860687  suite-compound-a6cef89.json
edaa3c19d5f10cbc42083e30314fe7342fb1d00f04516d6778df2e25fc191ba7  suite-core-a6cef89.json
5ace576ba743811dddcf9a5e777b34c36bf35725838f0c5eca5eac8dd5b9e790  suite-frozen-a6cef89.json
d0db8db7d9f7193fc9440ea6d4fcd82ad332309b709fafe33e139a21f7a72676  suite-hardening-a6cef89.json
f7dbced66f37d3682d5341ecea40b9c3d3001e1a74f877707b2e1a657c6fb0ea  suite-r18-failsafe-a6cef89.json
0f945ef734335f46ebe3555d99f93a9b966c7de415a8cd946011691ba16eae54  suite-r19-bashcvar-a6cef89.json
adb74f3dcde58b54a0921176e13be7a4b2e43057c2cd8286ee900f04492aada6  suite-r19-frozen-f1f2-a6cef89.json
64c50cc3bc84cda51b6469d1b9b3b06484283478cfaf5080406e42f933bedce0  suite-r19-helperfn-a6cef89.json
e15db67936ef62408e6e5c1c45a3575f628aeb1c7db45e0a8797e0b7ae1fe0c7  suite-r19-installers-a6cef89.json
10ed81c6ff7d690ff0aea044e50513931ffed001717b53948d29c427263b5fdc  suite-r19-vcs-a6cef89.json
fe580f4de2acf3c80ee42355de30e9cb1c5da305dbd84fed8c37531453c8a5f6  suite-w2-regressions-a6cef89.json
```
