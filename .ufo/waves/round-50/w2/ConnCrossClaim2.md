# ConnCrossClaim2 — Cross-Claim Coupling, Gate Findings & Round-49 Counter Validity Audit

Seat `ConnCrossClaim2` (connector, leaf), mado round 50 / wave w2 = FALSIFY.
Scored revision: `b4a79843cc2545bbe800db9322e58f6e00436629` (landed tip).
Base revision: `8ae47b957034ae21012bbf09173cca2c48be345e`.
Lane repository: `/home/vgpnk/Projects/shokunin/mado-shokunin`.

---

## 1. Executive Verdict

1. **Predicate Independence Established (No Missed Coupling Defect):**
   Neither frozen counter depends on the other claim's substantive bytes. `PRED-C1-r50` (`c1-r50-bind-entry.py`) reads strictly C1 corpus artifacts, fetch pins, live receipts, and historical base markdown; it never opens or imports `quality/check-session-material.py` or any C2 instrument. `PRED-C2-r50` (`c2-r50-session-gate.py`) reads only `quality/check-session-material.py` at `--rev` and tests it against in-memory selftests and synthetic scratch fixture repositories; it never reads C1 files or executes on the lane tree.

2. **C1 Files Are 100% Clean Under Gate v3:**
   All 21 committed C1 files (knowledge entry `hyprland-bind-key-match-r50.md`, registry `SOURCES.md`, `README.md`, `round-50.md`, live receipt `binds-live-r50.txt`, and the 16 fetch pins) introduce **0 findings** under the installed v3 gate across all rules (`R1`-`R9`).

3. **New Gate Findings at Landed Tip (+7 Findings):**
   Comparing the v3 gate scan at base `8ae47b95` (228 findings, 52 waived across 48 files) against landed tip `b4a79843` (235 findings, 49 waived across 47 files) reveals **7 new un-waived findings**:
   - **New offender 1 (C2 seat copy):** `.ufo/waves/round-50/w1/ExecGateV3/check-session-material.py` (+3 findings: `R1_CLIENT_DUMP=4`, `R2_PROC_TABLE=3`, `R3_MONITOR_IDENT=1`), because the w1 seat committed a raw copy of the gate containing embedded test fixtures without registering a waiver.
   - **New offender 2 (w1 correction receipt):** `.ufo/waves/round-50/w1/ScrCorrectionsR50/receipts/d2-seat-state.txt` (+1 finding: `R8_ACCOUNT_COLUMN=2`), because lines 58–59 commit a raw `ls -l` directory listing with the unmasked host owner/group `vgpnk vgpnk`.
   - **Second-order ripple (historical waiver invalidation):** `.ufo/waves/round-48/w1/ExecSessionMarker/check-session-material.py` (+3 findings: `R1`, `R2`, `R3`), because upgrading `quality/check-session-material.py` from v2 to v3 broke the round-48 `kind=gate-copy` waiver with `reason=gate-source-mismatch`.

4. **Round-49 Counter Attacks Validity Answered:**
   The round-49 closure assertion that the candidate entry failed quote-binding and step quotes (`clauses b/c/d/e/j`) was an artifact of incomplete fixture staging in the scoring tree (missing registry rows and README rows), not a defect in the candidate text. As proven by w1/`ExecDoNothing` and w1/`ExecControlsC1R50`, the identical candidate artifacts score `TARGET_MET` (11/11 clauses) on the frozen round-49 counter when evaluated on a complete tree with its supporting rows committed.

---

## 2. File Read Audit of Frozen Counters (Task Part a)

### A. Counter `PRED-C1-r50` (`quality/counters/c1-r50-bind-entry.py`)
- **Frozen SHA256:** `e162d6717915f5585c40853afa8223d0398e50f0de37da4fd02004d2b08a84c0`
- **File path constants (lines 161–168):**
  - `ENTRY = "corpus/knowledge/hyprland-bind-key-match-r50.md"`
  - `REGISTRY = "corpus/SOURCES.md"`
  - `README = "corpus/README.md"`
  - `LESSON = "corpus/lessons/round-50.md"`
  - `FETCH = ".ufo/waves/round-50/fetch/"`
  - `HELD_FETCH = ".ufo/waves/round-46/fetch/"`
  - `RECEIPTS = ".ufo/waves/round-50/receipts/"`
  - `BASE_DEFAULT = "8ae47b957034ae21012bbf09173cca2c48be345e"`
- **Git objects fetched via `show(repo, rev, path)`:**
  - `rev:corpus/knowledge/hyprland-bind-key-match-r50.md` (line 1172)
  - `rev:corpus/SOURCES.md` (line 1176)
  - `base:corpus/SOURCES.md` (line 1178)
  - `rev:corpus/README.md` (line 1182)
  - `base:corpus/README.md` (line 1184)
  - `rev:corpus/lessons/round-50.md` (line 1188)
  - `rev:.ufo/waves/round-50/fetch/*` (line 1192 via `fetch_pins()`, reads all 16 pins)
  - `rev:.ufo/waves/round-46/fetch/*` and `base:.ufo/waves/round-46/fetch/*` (lines 1196, 1200, S319 pin)
  - `rev:.ufo/waves/round-50/receipts/binds-live-r50.txt` (line 734)
  - `base:.ufo/waves/round-50/receipts/binds-live-r50.txt` (line 737, asserts absent at base)
- **Dynamic tree traversal via `base_grams()` (lines 947–967):**
  - Enumerates `git ls-tree -r base`
  - Reads every blob starting with `corpus/knowledge/` or `corpus/lessons/` ending with `.md`
  - Ignores `quality/`, `tools/`, and `.ufo/` trees completely.
- **Runtime probe / IPC (clause r, lines 1068–1120):**
  - Invokes `hyprctl binds -j` and `hyprctl getoption input:resolve_binds_by_sym -j` via the compositor socket.
- **Filesystem access:**
  - Operates strictly under `tmp_root()` (`$TMPDIR`); refuses `/tmp`, `/var/tmp`, `/dev/shm`, and repository interior.
- **C2 Gate interaction:**
  - Zero reads, zero imports, zero subprocess calls to `quality/check-session-material.py`.

### B. Counter `PRED-C2-r50` (`quality/counters/c2-r50-session-gate.py`)
- **Frozen SHA256:** `1d52a62cd969aba59c2cd1f944212b6f9619212b5fb313c470c4c14ebd62b298`
- **File path constants (lines 67–70):**
  - `GATE_REL = "quality/check-session-material.py"`
  - `BASE_REV = "8ae47b957034ae21012bbf09173cca2c48be345e"`
  - `BASE_GATE_SHA256 = "82c9053ae2e8b7db2fb8c0e195c32b8b151a593cf9412dcae3589427ac2dfa6f"`
  - `V2_CASE_NAMES_SHA256 = "38a8b2c647665b68ae4d3b7692e7ffaf9ca959fc1cdfe03b21deb5bd8097e725"`
- **Git objects fetched from `--repo`:**
  - ONLY `rev:quality/check-session-material.py` via `read_gate()` (lines 240–248).
  - No other blob or tree in `--repo` is read.
- **Filesystem and fixture generation:**
  - Extracts gate script to `work/gates/gate-<sha>.py`.
  - Executes `gate --selftest` (runs in-memory self-tests).
  - Generates isolated temporary git repos in `work/fixtures-<nonce>/`:
    - `red-%03d-%s` (42 synthetic test repositories)
    - `green-%03d-%s` (44 synthetic test repositories)
    - `scope-outside-ufo` (synthetic test repository containing `docs/receipt.txt`)
  - Evaluates gate subprocesses against these temporary repos only.
- **C1 Interaction:**
  - Zero reads of `corpus/`, `receipts/`, `fetch/`, or any C1 entry/lesson. Counter never scans the lane repository.

---

## 3. Base-Scan vs Landed Round-50 Files (Task Part b)

### A. Gate v3 Summary Comparison
Command: `python3 -I quality/check-session-material.py --repo <clone> --rev <rev> --scope all`

| Metric | Base `8ae47b95` | Tip `b4a79843` | Delta | Notes |
|---|---:|---:|---:|---|
| **Files scanned** | 23,270 | 23,920 | +650 | New round-50 seat directories and deliverables |
| **Total findings** | **228** | **235** | **+7** | Sum of per-rule file counts |
| **Waived findings** | 52 | 49 | -3 | 3 waivers rejected due to gate upgrade |
| **Waived files** | 48 | 47 | -1 | Round-48 gate copy no longer waived |
| **Rejected waivers** | 2 | 5 | +3 | Round-48 gate-copy rejected |

### B. Rule-by-Rule Breakdown

| Rule | Base File Count | Tip File Count | Delta | Contributing Files |
|---|---:|---:|---:|---|
| **R1_CLIENT_DUMP** | 40 | 42 | **+2** | `.ufo/.../ExecGateV3/check-session-material.py`<br>`.ufo/.../ExecSessionMarker/check-session-material.py` |
| **R2_PROC_TABLE** | 40 | 42 | **+2** | `.ufo/.../ExecGateV3/check-session-material.py`<br>`.ufo/.../ExecSessionMarker/check-session-material.py` |
| **R3_MONITOR_IDENT** | 13 | 15 | **+2** | `.ufo/.../ExecGateV3/check-session-material.py`<br>`.ufo/.../ExecSessionMarker/check-session-material.py` |
| **R4_HOME_LISTING** | 3 | 3 | 0 | Unchanged |
| **R5_SERIAL_PROSE** | 25 | 25 | 0 | Unchanged |
| **R7_HOME_PATH_PREFIX** | 49 | 49 | 0 | Unchanged |
| **R8_ACCOUNT_COLUMN** | 54 | 55 | **+1** | `.ufo/.../ScrCorrectionsR50/receipts/d2-seat-state.txt` |
| **R9_EXEC_CACHE** | 4 | 4 | 0 | Unchanged |

### C. Attribution of the 7 New Findings

1. **`.ufo/waves/round-50/w1/ExecGateV3/check-session-material.py` (+3 rules: R1, R2, R3)**
   - *Line details:* Carries embedded positive test fixtures for R1 (`CLIENT_DUMP` json), R2 (`PROC_TABLE` ps output), and R3 (`MONITOR_IDENT` serials).
   - *Cause:* Seat deliverable committed a verbatim copy of the gate script into `.ufo/waves/` without creating a corresponding waiver entry in `quality/session-material-waivers.txt`.

2. **`.ufo/waves/round-50/w1/ScrCorrectionsR50/receipts/d2-seat-state.txt` (+1 rule: R8)**
   - *Line details:* Lines 58–59 carry unmasked `ls -l` table rows:
     ```
     drwxr-xr-x 1 vgpnk vgpnk    0 Oct 27 01:38 .
     drwxr-xr-x 1 vgpnk vgpnk 2468 Oct 27 02:18 ..
     ```
   - *Cause:* Unsanitized shell output logging host user and group names (`vgpnk vgpnk`), directly triggering `R8_ACCOUNT_COLUMN`.

3. **`.ufo/waves/round-48/w1/ExecSessionMarker/check-session-material.py` (+3 rules: R1, R2, R3)**
   - *Line details:* Pre-existing copy of the round-48 v2 gate.
   - *Cause (Second-Order Ripple):* In base `8ae47b95`, this file had a valid waiver in `quality/session-material-waivers.txt`:
     `.ufo/waves/round-48/w1/ExecSessionMarker/check-session-material.py 82c9053a... R1_CLIENT_DUMP,R2_PROC_TABLE,R3_MONITOR_IDENT kind=gate-copy`
     The gate's waiver verification logic (`check-session-material.py:908–910`) enforces:
     ```python
     gate_sha = sha256_hex(_git(repo, "show", "%s:%s" % (sha, gate_source_rel)))
     if gate_sha != marked_sha:
         rejected.append((path, rule, "gate-source-mismatch"))
     ```
     When C2 updated `quality/check-session-material.py` from v2 (`82c9053a...`) to v3 (`ffdc9d62...`), `gate_sha` changed to `ffdc9d62...`. Because the round-48 copy has digest `82c9053a...`, `gate_sha != marked_sha` fired, rejecting the waiver. Consequently, this untouched historical file became an active finding on R1, R2, and R3.

### D. Verification of C1 Committed Files
Scanning every C1 file committed between base and tip against gate v3:
- `corpus/knowledge/hyprland-bind-key-match-r50.md`: **CLEAN** (0 findings)
- `corpus/SOURCES.md`: **CLEAN** (0 findings)
- `corpus/README.md`: **CLEAN** (0 findings)
- `corpus/lessons/round-50.md`: **CLEAN** (0 findings)
- `.ufo/waves/round-50/receipts/binds-live-r50.txt`: **CLEAN** (0 findings)
- All 16 pins under `.ufo/waves/round-50/fetch/`: **CLEAN** (0 findings)

**Result:** C1 introduced zero gate violations.

---

## 4. Counter Independence vs Runtime Coupling (Task Part c)

- **Counter Independence:**
  Neither counter depends on the other's bytes. `PRED-C1-r50` scores `TARGET_MET` (`a:1 b:1 c:1 d:1 e:1 f:1 g:1 h:1 i:1 j:1 r:1 admitted=1/1`) without inspecting gate v3. `PRED-C2-r50` scores `TARGET_MET` (`selftest=94/94 red=42/42 green=44/44 scope=seen`) without inspecting C1 entry files.
- **Runtime Operability Coupling:**
  The coupling exists at the runtime verification layer. Gate v3 operates repository-wide (`--scope all`). If operators run gate v3 on the repository, any session material introduced by a corpus contributor immediately breaks the gate. Furthermore, updating gate v3 inherently mutates the verification state of all historical seat directories carrying gate copies.

---

## 5. The Round-49 Counter Attacks Validity Question

- **The Historical Assertion:**
  The round-49 closure (`corpus/lessons/round-49-verifier-spotcheck.md` §6 item 5 and `registration.md:27–29`) claimed that C2 stopped honestly because `hyprland-bind-key-match-r49.md` failed its counter on quote-binding and step quotes (`clauses b/c/d/e/j`).
- **The Ground Truth Revealed:**
  In round 50 w1, `ExecDoNothing` (receipts `controls-all.txt`, findings F1) and `ExecControlsC1R50` (receipts `controls-r49.txt`, findings F1) evaluated the exact candidate entry against the frozen round-49 counter `quality/counters/c2-r49-bind-entry.py`.
  When evaluated on a tree with its required registry rows (S352–S363), README index row, and Gate admit lines committed, the round-49 candidate entry scored:
  `PRED-C2-r49: clauses=a:1 b:1 c:1 d:1 e:1 f:1 g:1 h:1 i:1 j:1 r:1 admitted=1/1 verdict=TARGET_MET`
- **Root Cause of the Round-49 Stop:**
  The round-49 failure was an uncommitted-staging artifact: the candidate scoring tree omitted the registry rows in `corpus/SOURCES.md`, causing head IDs to evaluate to `rows=0`, cascading into failures in clauses b, c, d, e, and j. The candidate text itself was semantically sound and satisfied all quote-binding and topic-coverage constraints.

---

## 6. Connector Synthesis: Bounded Non-Obvious Move

### A. Evidence
1. Gate v3's `kind=gate-copy` waiver rule binds historical copies to the current HEAD gate:
   `gate_sha != marked_sha` in `quality/check-session-material.py:908–910`.
2. This design caused 3 synthetic findings to reappear on `.ufo/waves/round-48/w1/ExecSessionMarker/check-session-material.py` as an immediate side-effect of C2 landing.
3. Every future round upgrading the gate will continue to break all prior gate-copy waivers.

### B. Affected Axes
- **Operability (Primary):** The current waiver design creates artificial regression noise whenever quality tools evolve, undermining repository-wide hygiene tracking.
- **Coverage (Constraint):** Any change must maintain strict privacy enforcement without relaxing checks on genuine session material.

### C. Proposed Move: Version-Anchored Gate-Copy Waivers
Decouple `kind=gate-copy` waiver validation from the current revision's `quality/check-session-material.py` digest.
Instead of requiring `gate_sha == marked_sha` (where `gate_sha` is the scanned revision's gate), `check-session-material.py` should verify that:
1. The target file's content hash matches the `marked_sha` specified in `quality/session-material-waivers.txt`.
2. The `marked_sha` belongs to an approved, immutable set of recognized gate releases (e.g., `VALID_GATE_VERSIONS = {v1_sha, v2_sha, v3_sha}`).

### D. Second-Order Effects & Risks
- **Positive:**
  - Restores idempotence to historical audits: round-48 and round-50 seat deliverables carrying authentic gate copies are correctly waived.
  - Prevents the repo-wide finding count from inflating when upgrading quality instruments.
- **Risk & Mitigation:**
  - *Risk:* A malicious or careless seat might commit a modified gate that bypasses checks.
  - *Mitigation:* Requiring membership in an explicit, immutable list of historical gate release hashes (`VALID_GATE_VERSIONS`) guarantees that only exact, authentic copies of previously approved gates can ever be waived.

### E. Verification Protocol
1. Modify gate logic in a scratch clone to validate `marked_sha in VALID_GATE_VERSIONS`.
2. Re-run `--scope all` on tip `b4a79843`:
   - `.ufo/waves/round-48/.../check-session-material.py` returns to `WAIVED`.
   - R1/R2/R3 finding count drops by 3.
   - Genuine violations (like `d2-seat-state.txt` R8 account leakage) remain strictly flagged.

---

## 7. Deliverables & Receipts

All receipt files are committed in `.ufo/waves/round-50/w2/ConnCrossClaim2/` and verified with `SHA256SUMS`:

| Deliverable Path | Description | SHA256 Digest |
|---|---|---|
| `.ufo/waves/round-50/w2/ConnCrossClaim2/c1-reads.txt` | Complete read audit of `PRED-C1-r50` | `2df9f20108933b497cb324b1a4574945d82054ff8e75db7fc20c32729a657c79` |
| `.ufo/waves/round-50/w2/ConnCrossClaim2/c2-reads.txt` | Complete read audit of `PRED-C2-r50` | `a94ddbeff60601df5e7ec4e867b3ca961c0c8eb44a9fe31086c57f7d9c02ff4e` |
| `.ufo/waves/round-50/w2/ConnCrossClaim2/gate-scan-base.txt` | Baseline scan reproduction at `8ae47b95` | `e2a4ddba2b44452587dae6da206f658be4229c9cc2bb5d4ce657c38520844f2d` |
| `.ufo/waves/round-50/w2/ConnCrossClaim2/gate-scan-tip.txt` | Full repository scan at tip `b4a79843` | `a41a4a51eb5eb6db24beee7fe5092eb82e8f8045610ec1f2a36b3e7bc8ebc1fc` |
| `.ufo/waves/round-50/w2/ConnCrossClaim2/gate-scan-delta.txt` | Detailed base vs tip delta & offender attribution | `e685f02bc0b7df1a3c61b65b6eb0ae3b259d68dc7637841bb2f4e4e94b283dd9` |
| `.ufo/waves/round-50/w2/ConnCrossClaim2/c1-files-gate-check.txt` | Verification that all 21 C1 files are clean | `75317761cebe0c12853fcf138e4a9561b6fb8918ddf0c72f7e77a1197943d73f` |
| `.ufo/waves/round-50/w2/ConnCrossClaim2/counter-cross-check.txt` | Cross-claim independence & round-49 audit | `ce17336b9c9f0bce427ce33be92161b96d9ff28b0be466100c5c363b7829fbfa` |
| `.ufo/waves/round-50/w2/ConnCrossClaim2/SHA256SUMS` | Checksums for all receipts | `b0880373e047ca38e47bf1b658d55734bc179ae097f4fae9fcaae953683f2a87` |
| `.ufo/waves/round-50/w2/ConnCrossClaim2.md` | This report | — |
