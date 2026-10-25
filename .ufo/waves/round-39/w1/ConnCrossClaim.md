# ConnCrossClaim — Cross-Claim Shared-File Scan & Separability Synthesis
**Wave:** Round 39, Wave 1 (w1)  
**Lane:** `/home/vgpnk/Projects/shokunin/mado-shokunin`  
**Base Commit:** `08be4eb7fd13358ed29b096e8924005d46ac409c`  
**Freeze Commit:** `457d1b125932c1e0d797061a2156b917bcd7edaa` (HEAD)  
**Role:** UFO-FSD Connector (leaf)  

---

## 1. Executive Summary

This audit performs a systematic cross-claim shared-file scan across the three frozen claims of mado round 39:
- **C1 Calibration:** Re-registered repaired round-38 discrimination pair (`quality/check-r38-discrimination.py` + `.ufo/waves/round-39/c1/manifest.json` + `c1-r38-event-ground.py` + `c2-r38-eventq.py`). Target: `controls=19 correct=19/19 verdict=TARGET_MET`.
- **C2 Operability:** Config-option ownership table tool (`tools/mado-options.py`) + counting instrument (`quality/counters/c3-r39-options.py`) + fixture suite (`.ufo/waves/round-39/w1/ExecOptionsFixtures/`). Target: `fixtures=N/N tool=present verdict=TARGET_MET`.
- **C3 Coverage (Sourced):** Admitted knowledge entry (`corpus/knowledge/config-option-table-r39.md`) + `corpus/SOURCES.md` registry rows S218/S219 + lesson Gate lines (`corpus/lessons/round-39.md`) + counting instrument (`quality/counters/c4-r39-options-entry.py`). Target: `admitted=1/1 verdict=TARGET_MET`.

### Core Finding
A direct cross-claim verdict coupling exists between **C2** and **C3** on the file:
$$\mathbf{tools/mado\text{-}options.py}$$

- In **C2**, `tools/mado-options.py` is the active executable deliverable under test (evaluated for AST stdlib imports, selftest execution, and synthetic fixture evaluation).
- In **C3**, `tools/mado-options.py` is simultaneously declared as the provenance source and receipt for row `S219` (`| S219 | mado options tool — tools/mado-options.py | own-work | ...`), bound in `corpus/lessons/round-39.md` `## Gate` by SHA-256 and docstring quote.
- **Second-Order Verdict Coupling:** Any modification to `tools/mado-options.py` to fix C2 implementation defects (e.g., the blocker identified by `RevC2Counter` where `--selftest` outputs `69/69 passed` instead of `69/69 assertions`, or fixture runner path handling) alters the SHA-256 digest of `tools/mado-options.py`. This immediately breaks C3's pinned Gate receipt hash in `round-39.md`, flipping C3's admission verdict from `TARGET_MET` to `TARGET_MISSED`. Furthermore, deleting C2 breaks C3's receipt resolution.

A secondary substrate overlap exists on **`corpus/SOURCES.md`** between **C1** (which parses the entire `## Registry` table to verify uniqueness of S189/S201/S212–S217) and **C3** (which appends rows S218/S219/S220).

---

## 2. Cross-Claim File Matrix

The matrix below maps every file touched across deliverables, counting instruments, fixtures, evaluated substrate files, and evidence receipts.

| Path / File Pattern | C1 (Calibration) | C2 (Operability) | C3 (Coverage) | Cross-Claim Role & Coupling Status |
|---|---|---|---|---|
| `tools/mado-options.py` | — | **Deliverable / Executable Under Test** | **S219 Provenance Source & Bound Receipt** | **CRITICAL COUPLING (C2 ↔ C3):** C2 code changes invalidate C3 receipt SHA-256. |
| `corpus/SOURCES.md` | **Substrate Input** (read via `git show`, parses `## Registry`) | — | **Deliverable** (appends rows S218, S219, S220; edits S018 `used-by`) | **SUBSTRATE SHARING (C1 ↔ C3):** C1 parses table on accept path (`c1-live`). Disjoint ID namespaces prevent semantic clash if syntax is valid. |
| `.ufo/waves/round-39/registration.md` | Frozen contract / baseline | Frozen contract / baseline | Frozen contract / baseline | **SHARED GOVERNANCE:** Frozen at base commit `457d1b1`; read-only across all claims. |
| `quality/counters/c3-r39-options.py` | — | **Counting Instrument** | — | Isolated to C2. |
| `.ufo/waves/round-39/w1/ExecOptionsFixtures/*` | — | **Fixture Suite** (`run-fixtures.sh`, `expected.json`, `trees/`) | — | Isolated to C2. |
| `.ufo/waves/round-39/w1/ExecOptionsRealTree/*` | — | Real-tree evidence run | — | Isolated to C2. |
| `corpus/knowledge/config-option-table-r39.md` | — | — | **Deliverable** (Knowledge Entry) | Isolated to C3. |
| `quality/counters/c4-r39-options-entry.py` | — | — | **Counting Instrument** (`PRED-C4-r39-v1`) | Isolated to C3. |
| `corpus/lessons/round-39.md` | — | — | **Deliverable** (`## Gate` bindings for S218–S220) | Isolated to C3 (records C2/C3 intent). |
| `.ufo/waves/round-39/w1/ExecAssimFetches/S218.bin` | — | — | **S218 Fetch Receipt** (docs, Variables page) | Isolated to C3. |
| `.ufo/waves/round-39/w1/ExecAssimFetches/S220.bin` | — | — | **S220 Fetch Receipt** (docs, Dispatchers page) | Isolated to C3 / Assimilation. |
| `corpus/knowledge/dispatcher-surface-and-request-grammar-r26.md` | — | — | **Assimilation Deliverable** (appended section) | Isolated to C3 / Assimilation. |
| `.ufo/waves/round-24/fetch/S158.bin` | — | — | S018 held receipt (HyprCtl.cpp) | Isolated to C3 / Assimilation. |
| `corpus/README.md` | Substrate input (`## Coverage map`) | — | Harm-watch update (`quality/check-index.py`) | Disjoint sections: C1 reads `Coverage map`; C3 updates Index table. |
| `quality/check-r38-discrimination.py` | **Gate Runner** | — | — | Isolated to C1. |
| `quality/counters/c1-r38-event-ground.py` | **Counting Instrument** (c1) | — | — | Isolated to C1. |
| `quality/counters/c2-r38-eventq.py` | **Counting Instrument** (c2) | — | — | Isolated to C1. |
| `.ufo/waves/round-39/c1/manifest.json` | **Deliverable** (Re-frozen manifest) | — | — | Isolated to C1. |
| `.ufo/waves/round-39/receipts/c1-redbefore*.txt` | Red-before receipt | — | — | Isolated to C1. |
| `.ufo/waves/round-39/receipts/manifest-frozen-r38.json` | Comparison manifest | — | — | Isolated to C1. |
| `corpus/knowledge/event-delivery-limits-r26.md` | Evaluated substrate | — | — | Isolated to C1. |
| `corpus/knowledge/event-queue-observability-r37.md` | Evaluated substrate | — | — | Isolated to C1. |
| `corpus/lessons/round-37.md` | Evaluated substrate (`## Gate`) | — | — | Isolated to C1. |
| `tools/mado-eventq.py` | Evaluated substrate | — | — | Isolated to C1. |
| `.ufo/waves/round-38/receipts/eventq-live*` | Evaluated substrate | — | — | Isolated to C1. |
| `.ufo/waves/round-37/fetch/*` | Evaluated substrate receipts | — | — | Isolated to C1. |

---

## 3. Analysis of Cross-Claim Couplings

### Coupling 1: `tools/mado-options.py` (C2 ↔ C3)
1. **The Nature of the Coupling:**
   - C2 is an *operability claim*: it delivers `tools/mado-options.py` and verifies its behavior using `quality/counters/c3-r39-options.py`.
   - C3 is a *coverage claim*: it delivers `corpus/knowledge/config-option-table-r39.md`, which cites `source: S218, S219`. Row `S219` in `corpus/SOURCES.md` names `tools/mado-options.py` as an `own-work` source.
   - In `corpus/lessons/round-39.md`, `GATE S219` binds:
     ```
     GATE S219 receipt=tools/mado-options.py@data-tip sha256=<hash> quote="mado-options.py - static resolver of the config-tree option table."
     ```
2. **Empirical Evidence of Breakage:**
   - During Wave 1, `SimplDraftTrim.md` and `RevAssim.md` observed:
     - The draft lesson bound `sha256=9787b53b298216aee93ec1193814e2972d9fef9125656ce9ed0bd03ed7fbcf59`.
     - An executor update to `tools/mado-options.py` changed its worktree hash to `cee78d99de2e3420572aa028f439240ac12e5eb6d595de75e2fc62e5ea9ce61e`.
     - The S219 Gate line became instantly stale and false.
   - Furthermore, `RevC2Counter.md` demonstrated that C2 currently fails Clause `b` because `--selftest` prints `69/69 passed` instead of `69/69 assertions`. Fixing this single line in `tools/mado-options.py` will alter its SHA-256 again, once more invalidating C3's Gate line!
   - `CritSeparability.md` verified that deleting C2 artifacts (`tools/mado-options.py` and `c3-r39-options.py`) destroys S219's receipt target.

### Coupling 2: `corpus/SOURCES.md` (C1 ↔ C3)
1. **The Nature of the Coupling:**
   - In C1, `c1-r38-event-ground.py` executes `show(repo, rev, "corpus/SOURCES.md")` and parses the entire `## Registry` table (`registry_rows(sources)`) to evaluate clause `c` (unique mined rows with `used-by` binding the entries) for IDs `S189, S201, S212–S217`.
   - In C3, `corpus/SOURCES.md` is edited to append rows `S218`, `S219`, `S220` and extend `S018`.
2. **Coupling Assessment:**
   - This is substrate sharing rather than semantic coupling: C1 inspects only its own assigned ID set.
   - However, a syntactic defect in C3's append (e.g., misaligned pipes, NFC normalization failure, or duplicate ID) could compromise C1's parser or fail fleet census harm-watch (`scripts/sources-census.sh validate`).

---

## 4. Connector Synthesis & Proposed Move

### Affected Axes
- **Operability:** Impaired by coupling; C2 tool iteration is artificially constrained by C3's receipt pin.
- **Coverage:** Fragile; C3's admission check is held hostage to code revisions in C2.
- **Calibration:** Unaffected (C1 is structurally insulated from C2 and C3 logic).

### The Proposed Move: Decouple C3 Provenance from C2 Executable Code
**Move:** Split the role of `tools/mado-options.py` so that C3's provenance receipt binds an **immutable interface specification artifact** rather than the mutable Python script.

1. **Concrete Realization:**
   - Create a static contract specification artifact:  
     `.ufo/waves/round-39/receipts/options-table-spec.txt`  
     This receipt defines the static option-table precedence order (defaults $\rightarrow$ theme $\rightarrow$ user $\rightarrow$ toggles $\rightarrow$ ai-usage), parser boundaries, and the five-label divergence vocabulary (`agreement`, `agreement*`, `live-default`, `mismatch`, `config-only`) that `config-option-table-r39.md` actually grounds.
   - Update `S219` in `corpus/SOURCES.md`:
     - Set source to: `mado options tool specification — .ufo/waves/round-39/receipts/options-table-spec.txt`.
     - Anchor to the specification receipt bytes and its permanent SHA-256.
   - In `corpus/lessons/round-39.md`:
     - Bind `GATE S219 receipt=.ufo/waves/round-39/receipts/options-table-spec.txt sha256=<fixed-hash> quote="<verbatim-spec-quote>"`.
   - Keep `tools/mado-options.py` strictly as the **C2 executable deliverable**.

### Second-Order Effects & Benefits
- **Zero Cross-Claim Shared Files:** The verdict paths of C2 and C3 become 100% disjoint. C2 touches `tools/mado-options.py` and `c3-r39-options.py`; C3 touches `config-option-table-r39.md`, `options-table-spec.txt`, and `c4-r39-options-entry.py`.
- **Full Separability:** Deleting C2 completely (as tested in `CritSeparability`) leaves C3's receipt resolution, Gate binding, and admission counter completely intact.
- **Safe Iteration:** C2 executors can patch the selftest output format and fixture runner without risking race conditions or staleness in C3's lesson Gate line.

### Risks & Mitigations
- **Risk:** Divergence between `options-table-spec.txt` and `tools/mado-options.py` implementation.
- **Mitigation:** C2's fixture suite (`ExecOptionsFixtures/run-fixtures.sh`) and counter (`c3-r39-options.py`) already verify tool compliance against `expected.json`. The specification receipt is an exact excerpt of the interface contract tested by C2 fixtures.
- **Risk:** Registration re-interpretation.
- **Mitigation:** Registration §C3 states: "and S219 (`own-work` row for the options tool, opened this round); both mined, both with Gate lines in the round lesson binding a committed receipt by sha256 and a located quote." Binding the committed specification receipt satisfies the registration contract verbatim while eliminating the mutable code coupling.

---

## 5. Verification Plan

1. **Matrix Validation:**
   Verify that all paths listed in Section 2 accurately reflect git tree reads and counter implementations.
2. **Separability Sanity Check (Sandbox):**
   In a sandbox clone at tip:
   - Run C1: `python3 -I quality/check-r38-discrimination.py ...` $\rightarrow$ verify `controls=19 correct=19/19 verdict=TARGET_MET`.
   - Remove `tools/mado-options.py` and `quality/counters/c3-r39-options.py`.
   - Verify C3 verification (`c4-r39-options-entry.py` + census) evaluates to `TARGET_MET` without accessing `tools/mado-options.py`.
3. **Harm-Watch Integrity:**
   Ensure `scripts/sources-census.sh validate` and `quality/check-index.py` exit 0 with all new rows and entries present.
