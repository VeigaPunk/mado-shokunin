# ConnEvidenceResolve — Pointer Resolution and Synthesis Report (Round 39, Wave w1)

**Seat:** `ConnEvidenceResolve` (connector leaf)  
**Date:** 2026-10-25  
**Lane Root:** `/home/vgpnk/Projects/shokunin/mado-shokunin`  
**Base Revision:** `08be4eb7fd13358ed29b096e8924005d46ac409c`  
**Freeze / Current HEAD Revision:** `457d1b125932c1e0d797061a2156b917bcd7edaa`  

---

## 1. Scope & Execution Method

In accordance with the canonical assignment, this connector verified every planned report pointer across:
1. `ExecRecordChecks` (`.ufo/waves/round-39/w1/ExecRecordChecks/measurements.json`)
2. Report main draft (`.ufo/waves/round-39/w1/ScrReportMain/report-main.md`)
3. Scorecard draft (`.ufo/waves/round-39/w1/ScrScorecard/scorecard.md`)
4. Lesson draft (`.ufo/waves/round-39/w1/ScrLesson/round-39.md`)
5. Erratum draft (`.ufo/waves/round-39/w1/ScrErratum/erratum.md`)
6. SHONEN draft (`.ufo/waves/round-39/w1/ScrReportShonen/shonen.md`)
7. LOG entry draft (`.ufo/waves/round-39/w1/ScrLog/log-entry.md` & `ScrLog.md`)
8. SOURCES rows draft (`.ufo/waves/round-39/w1/ScrSourcesRows/rows.md`)
9. Knowledge entry draft (`.ufo/waves/round-39/w1/ScrKnowledgeEntry/config-option-table-r39.md`)
10. Dispatcher amendment draft (`.ufo/waves/round-39/w1/ScrDispatcherAmendment/dispatcher-amendment-section.md`)

Verification executed read-only checks: `git cat-file -e`, `git show`, `test -f`, `sha256sum`, and direct subprocess execution of every counting and gate command. No files outside this report were created or modified.

---

## 2. Command Reproductions & Gate Verification

| Command | Cited Rev | Observed Result | Exit | Match Status |
|---|---|---|:---:|:---:|
| **C1 Freeze/Tip Counting:** `python3 -I quality/check-r38-discrimination.py --c1 quality/counters/c1-r38-event-ground.py --c2 quality/counters/c2-r38-eventq.py --manifest .ufo/waves/round-39/c1/manifest.json --rev 457d1b125932c1e0d797061a2156b917bcd7edaa` | `457d1b12` | `MADO_R38_DISCRIMINATION: controls=19 correct=19/19 verdict=TARGET_MET` | 0 | REPRODUCED |
| **C1 Red-Before Counting:** `python3 -I quality/check-r38-discrimination.py --c1 quality/counters/c1-r38-event-ground.py --c2 quality/counters/c2-r38-eventq.py --manifest .ufo/waves/round-39/receipts/manifest-frozen-r38.json --rev 08be4eb7fd13358ed29b096e8924005d46ac409c` | `08be4eb7` | `MADO_R38_DISCRIMINATION: controls=19 correct=18/19 verdict=TARGET_MISSED` (`c1-duprow ok=0`) | 1 | REPRODUCED |
| **Gate 1 (Navigation Index):** `python3 -I quality/check-index.py --rev 457d1b125932c1e0d797061a2156b917bcd7edaa --repo .` | `457d1b12` | `MADO_INDEX: rev=457d1b1... indexed=55/55 missing=0 dangling=0 duplicates=0 coverage=10.0000/10` | 0 | REPRODUCED |
| **Gate 2 (Discrimination Control Replay):** (Identical to C1 freeze run above) | `457d1b12` | `controls=19 correct=19/19 verdict=TARGET_MET` | 0 | REPRODUCED |
| **Gate 3 (Axis Scores):** `python3 -I quality/check-axis-scores.py --repo . --rev 457d1b125932c1e0d797061a2156b917bcd7edaa` | `457d1b12` | `MADO_AXIS: checked=3 mismatched=0 rev=457d1b1...` (nav=55/55, cal=50/50, op=12/12) | 0 | REPRODUCED |
| **Gate 4 (Selftest):** `bash tools/mado-verify.sh --selftest` | HEAD | `MADO_SELFTEST: 460/460 assertions passed` | 0 | REPRODUCED |
| **Fleet Source Census:** `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin mado` | HEAD | `mado ok .../corpus/SOURCES.md` (W04 x7, W01 x1; baseline warnings identical) | 0 | REPRODUCED |
| **Eventq Counter:** `python3 -I quality/counters/c2-r38-eventq.py --repo . --rev 457d1b125932c1e0d797061a2156b917bcd7edaa` | `457d1b12` | `PRED-C2-r38-v3 fixtures=14/14 readonly=1 live=1 tool=present verdict=TARGET_MET` | 0 | REPRODUCED |
| **C2 Counting Command:** `python3 -I quality/counters/c3-r39-options.py --repo . --rev <rev>` | Pending | Evaluates to `fixtures=0/1 tool=absent verdict=TARGET_MISSED` at freeze `457d1b12` | 1 | BLOCKED on data commit |
| **C3 Counting Command:** `python3 -I quality/counters/c4-r39-options-entry.py --repo . --rev <rev>` | Pending | Script does not exist on disk or git index (`[Errno 2] No such file or directory`) | 2 | DEAD / UNIMPLEMENTED |

---

## 3. Verified Committed Pointers

The following committed paths, receipts, and revisions exist and resolve verbatim:

1. **Commit SHAs:**
   - Base commit: `08be4eb7fd13358ed29b096e8924005d46ac409c` (`git cat-file -t` → `commit`)
   - Freeze commit / HEAD: `457d1b125932c1e0d797061a2156b917bcd7edaa` (`git cat-file -t` → `commit`)
   - Round-38 freeze commit: `58e55ec` (`58e55ec90c74900da1bda70ea49e0c1598f80459`)
   - Round-38 counter patch: `859d0cf` (`859d0cf92c55dd7eb5962b8fa2f74ae4b54e3d93`)
   - Round-38 dispute record: `c46f868` (`c46f86821bcbe92dc1ea68370b4be935824c3d82`)
   - Round-38 freeze-pair resolution: `f551b70` (`f551b702ecbb6e92f7e75bb87b1c31c0397fcbb5`)
2. **Committed Base Paths:**
   - `.ufo/waves/round-38/controls/manifest.json` (sha256 `96965518dc8ad98b52b28b406d66841758c80fd75610f9b94e0239b8adf838c8`)
   - `quality/check-r38-discrimination.py`
   - `quality/counters/c1-r38-event-ground.py`
   - `quality/counters/c2-r38-eventq.py`
   - `quality/check-index.py`
   - `quality/check-axis-scores.py`
   - `tools/mado-verify.sh`
   - `corpus/SOURCES.md` (211 registry rows)
3. **Committed Freeze Paths:**
   - `.ufo/waves/round-39/registration.md`
   - `.ufo/waves/round-39/c1/manifest.json` (sha256 `96965518...`, byte-identical to round-38 landed controls at base)
   - `.ufo/waves/round-39/receipts/axis-base.txt`
   - `.ufo/waves/round-39/receipts/nav-base.txt`
   - `.ufo/waves/round-39/receipts/selftest-base.txt`
   - `.ufo/waves/round-39/receipts/census-before.txt`
   - `.ufo/waves/round-39/receipts/c1-redbefore.txt`
   - `.ufo/waves/round-39/receipts/c1-redbefore-out.txt`
   - `.ufo/waves/round-39/receipts/manifest-frozen-r38.json` (sha256 `14c49d9fec35dc9bc307fbdd5c732e2ce80fabeaadfe3327b9121f50b9553edb`)
   - Inherited seat reports: `.ufo/waves/round-38/w1/reports/{RevEntryBound,RevRegistry,ScoutS253}.md`
   - Historical fetch receipt: `.ufo/waves/round-24/fetch/S158.bin` (sha256 `798b7c6c4c1684557842463d46ac99c96629be4179e0e461dca77670247b91fa`)
4. **SHONEN Grounding Paths:**
   - `corpus/knowledge/executor-test-sufficiency.md` (lines verified)
   - `corpus/knowledge/config-health-report-r3.md` (verified)
   - `LOG.md` (verified)
   - `corpus/knowledge/province-accuracy-selfaudit.md` (verified)
   - `PROVINCE.md` (verified)
5. **Fetched Artifacts (Wave w1):**
   - `.ufo/waves/round-39/w1/ExecAssimFetches/S218.bin` (sha256 `400d18195020316c25e1874e567d868458b69e342a019b3ec8da6211d7222801`)
   - `.ufo/waves/round-39/w1/ExecAssimFetches/S220.bin` (sha256 `f9b51362f2440e02999089a255c5d7f3feb103f3cdeb6124c86a9f285c14b6e2`)

---

## 4. Dead Pointers & Fix Catalog

| Source File | Cited Pointer / Text | Defect Type | Root Cause | Exact Fix |
|---|---|---|---|---|
| **ScrScorecard** (`scorecard.md:16,39,55,57`) | `receipts/manifest-frozen-r38.json`<br>`receipts/c1-redbefore.txt`<br>`receipts/axis-base.txt`<br>`receipts/selftest-base.txt`<br>`receipts/census-before.txt` | Dead relative path | Omitted `.ufo/waves/round-39/` directory prefix; fails from repository root | Prepend `.ufo/waves/round-39/` to all base receipt paths |
| **ScrScorecard** (`scorecard.md:16,45,46,52,53,54,57,59`) | `w1/ExecC1After/after-freeze.txt`<br>`w1/ExecC1After/after-tip.txt`<br>`w1/ExecAssimFetches/S218.bin`<br>`w1/ExecAssimFetches/S220.bin`<br>`w1/ExecGateHealth/gate1-check-index.out`<br>`gate2-discrimination.out`<br>`w1/ExecEventqSnapshot/eventq-after.txt`<br>`w1/ExecCensusAfter/census-after.txt`<br>`w1/ExecEventqSnapshot/eventq-live-census.txt` | Dead relative path | Omitted `.ufo/waves/round-39/` directory prefix; `gate2-discrimination.out` also omitted seat subfolder `ExecGateHealth/` | Prepend `.ufo/waves/round-39/` (and `.ufo/waves/round-39/w1/ExecGateHealth/gate2-discrimination.out`) |
| **ScrLesson** (`round-39.md:21,101`) | `round-38 verifier spot-check :50`<br>`round-38-verifier-spotcheck.md :17` | Dead relative path | Omitted `corpus/lessons/` folder prefix | Replace with `corpus/lessons/round-38-verifier-spotcheck.md:17` and `:50` |
| **ScrLesson** (`round-39.md:20`) | `round-38 lesson :40-43` | Dead relative path | Omitted `corpus/lessons/` directory and `.md` extension | Replace with `corpus/lessons/round-38.md:40-43` |
| **ScrLesson** (`round-39.md:102`) | `RevCensusBefore.md :110` | Dead relative path | Omitted historical seat report directory | Replace with `.ufo/waves/round-38/w1/reports/RevCensusBefore.md:110` |
| **ScrLesson** (`round-39.md:102`) | `fleet round-38 report addendum 5 (9386c91f, 11:26:06)` | Unresolvable Git commit in lane repo | Commit `9386c91f` exists in the fleet repo (`/home/vgpnk/Projects/shokunin`), not in `mado-shokunin` | Qualify as fleet repo commit: `git -C /home/vgpnk/Projects/shokunin show 9386c91f` |
| **ScrLesson** (`round-39.md:34,49,62`) | `tools/mado-options.py@data-tip sha256=9787b53b298216aee93ec1193814e2972d9fef9125656ce9ed0bd03ed7fbcf59` | Stale hash | Tool was edited by `ExecOptionsTool`; current worktree hash is `cee78d99...` | Update sha256 to `cee78d99de2e3420572aa028f439240ac12e5eb6d595de75e2fc62e5ea9ce61e` (or recompute at data tip commit) |
| **ScrDispatcherAmendment** (`dispatcher-amendment-section.md:75`) | `S018:1309-1310 \| dispatchBatch → // split by ; ignores ; inside [] and adds ; on last command` | Line offset attribution | S158.bin line 1309 is the C++ function signature `static std::string dispatchBatch(...)`; comment is at line 1310 | Anchor comment explicitly to `S018:1310` (or retain `S018:1309-1310` with function signature noted) |
| **ScrDispatcherAmendment** (`dispatcher-amendment-section.md:9`) | `efb50993780079460b0cbed1363e2166a2de1d9f` | External git hash | Upstream Hyprland commit hash for tag `v0.56.2`, not in local git database | Clarify as upstream tag commit `hyprwm/Hyprland@efb5099`, bound locally via held receipt `.ufo/waves/round-24/fetch/S158.bin` |
| **ExecRecordChecks** (`measurements.json:79,187`) & **ScrReportMain** (`report-main.md:26`) | `quality/counters/c4-r39-options-entry.py` | Missing deliverable / broken pointer | Counter file was never authored or committed by any seat in w1 | Author and commit `quality/counters/c4-r39-options-entry.py` implementing `PRED-C4-r39-v1` before measuring C3 |
| **ExecRecordChecks** (`measurements.json:85,188`) & **ScrReportMain** (`report-main.md:7`) | `corpus/knowledge/config-option-table-r39.md` | Unlanded deliverable | Knowledge entry exists only as a seat draft (`.ufo/waves/round-39/w1/ScrKnowledgeEntry/config-option-table-r39.md`) | Copy draft into `corpus/knowledge/config-option-table-r39.md` at data commit |

---

## 5. Non-Obvious Move — UFO-FSD Connector Synthesis

### A. Evidence
1. **Contract Rupture on C2 (`quality/counters/c3-r39-options.py`):**
   `RevC2Counter` proved that `c3-r39-options.py` cannot bite positively (`TARGET_MISSED` unreachable) due to 3 clauses:
   - **Clause b:** Counter expects regex `(\d+)\s*/\s*(\d+)\s+assertions?`, but `tools/mado-options.py --selftest` prints `MADO_OPTIONS_SELFTEST: 69/69 passed` (`assertions=0` $\rightarrow$ fail).
   - **Clause c:** Counter copies only `run-fixtures.sh` into an isolated temp directory. `run-fixtures.sh` depends on sibling `expected.json` and `trees/` relative to `dirname "$0"`. In sandbox isolation, it fails (`fixtures=0/4`, rc=1 $\rightarrow$ fail).
   - **Clause d:** Counter requires stdout JSON marker `MADO_OPTIONS_ROWS:`, which `run-fixtures.sh` does not emit (`row_shape=0` $\rightarrow$ fail).
2. **Cross-Claim Coupling on C3 (`quality/counters/c4-r39-options-entry.py`):**
   `ConnCrossClaim` and `RevC3Sources` documented that C3's S219 own-work row requires the committed SHA256 of `tools/mado-options.py`. S219 remains unhashed because C2's tool has not been committed.
3. **Census Duplicate-URL Collision on S220:**
   `ScrSourcesRows` and `RevC3Sources` revealed that drafting S220 against `https://wiki.hypr.land/0.56.0/Configuring/Basics/Dispatchers/` duplicates existing row S196 (same URL and byte sha256 prefix `f9b51362`), risking a new fleet census W04 duplicate-URL warning.

### B. Affected Axes
- **Operability (`tools/mado-options.py` & `c3-r39-options.py`):** Currently blocked from achieving `TARGET_MET` (stuck at `fixtures=0/4 tool=present verdict=TARGET_MISSED`).
- **Calibration (Instrument Precedence & Control Validity):** Avoids committing a counter whose clauses are permanently stuck at 0.
- **Coverage (Sourced Knowledge Admission):** Unblocks C3 admission by stabilizing the C2 contract interface.

### C. Proposed Move
**Synthesized Three-Point Integration Alignment:**
1. **Standardize Selftest Output Marker (Clause b):**
   Update `tools/mado-options.py:1088` to print `MADO_OPTIONS_SELFTEST: 69/69 assertions passed` (matching the canonical `tools/mado-verify.sh --selftest` standard `MADO_SELFTEST: 460/460 assertions passed`).
2. **Bundle-Extract the Fixture Workspace (Clause c & d):**
   In `quality/counters/c3-r39-options.py`, modify `run_fixtures()` to extract the entire `.ufo/waves/round-39/w1/ExecOptionsFixtures/` directory tree (or use `git archive --format=tar <rev> .ufo/waves/round-39/w1/ExecOptionsFixtures/`) into the temp directory, preserving `expected.json` and `trees/`. In `.ufo/waves/round-39/w1/ExecOptionsFixtures/run-fixtures.sh`, append the emitted JSON row snapshot following `MADO_OPTIONS_ROWS:`.
3. **Consolidate S220 as S196 `used-by` Extension (C3 / Census Hygiene):**
   Instead of introducing duplicate URL row S220 (which triggers census W04 across scopes), extend held row S196's `used-by` column to include `corpus/knowledge/dispatcher-surface-and-request-grammar-r26.md`, exactly parallel to how held row S018 is extended. If the registration strictly mandates a new row ID S220, document the intentional W04 census warning in `corpus/lessons/round-39.md`.

### D. Risks & Second-Order Effects
- **Runtime Surface:** Changing `mado-options.py` selftest string has zero runtime risk for option parsing (it only affects `--selftest`).
- **Substrate Surface:** Extracting the fixture tree requires `expected.json` and fixture trees to be committed in git along with `run-fixtures.sh`.
- **Contract Surface:** Zero harm to C1 (discrimination pair uses separate files) and zero harm to existing navigation index (no new dangling entries).

### E. Verification Procedure
1. In a staging branch or scratch worktree, apply the selftest wording update and fixture extraction patch.
2. Run: `python3 -I quality/counters/c3-r39-options.py --repo . --rev HEAD` $\rightarrow$ verify output prints `clauses=b:1 c:1 a:1 d:1 e:1 f:0 g:1` and `fixtures=4/4 tool=present verdict=TARGET_MET` with exit code 0.
3. Re-run gate check: `python3 -I quality/check-axis-scores.py --repo . --rev HEAD` $\rightarrow$ exit code 0, 3/3 MATCH.

---

## 6. Verification Summary for Main Agent

- [x] All 8 base/freeze receipts confirmed present and verified byte-for-byte.
- [x] C1 discrimination reproduces: `19/19 TARGET_MET` at freeze/tip; red-before `18/19 TARGET_MISSED` at base.
- [x] All 4 gates reproduce: check-index (55/55), discrimination (19/19), axis-scores (3/3 MATCH), selftest (460/460).
- [x] Source census reproduces exit code 0.
- [x] Dead pointers cataloged with exact line-level fixes (11 distinct path, commit, and hash corrections).
- [x] Operability / C2 counter rupture diagnosed and resolution synthesized without harming any active axis.