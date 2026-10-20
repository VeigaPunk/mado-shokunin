# PlanningWalk — Bounded Planning Data Walk & Connector Synthesis (Round 14 / W1)

**Seat:** `MadoR14.PlanningWalk` (UFO-FSD connector, leaf member; no subagent dispatch, no background jobs, no commits/push)  
**Target:** `/home/vgpnk/Projects/shokunin/mado-shokunin`  
**Milestone:** U5 boundaries and regular-source targets  
**Axes Judged On:** `coverage`, `operability`  
**Date:** 2026-10-20  
**Verification Mode:** Read-only observation of repository files and peer wave artifacts. No gate, test, build, lint, or runtime execution.

---

## 1. Six-Axis Current Scores & Lowest Non-Retired Axis Confirmation

From `/home/vgpnk/Projects/shokunin/mado-shokunin/SCORECARD.md` (lines 330–455) and current HEAD (`873ff081b2ac363df771261b0ed950cba50d8988`), the current six-axis status is:

| Axis / Sub-axis | Score (0–10) | Denominator & Status | Evidence Pointer |
|---|---|---|---|
| **coverage / sourced current-art ground** | **5.7143** | **4/7 covered U-items (U1–U4)**; lowest non-retired scored axis | `SCORECARD.md:387`, `corpus/knowledge/wayland-protocol-boundaries-r13.md` |
| coverage / admitted-note reachability | 10.0000 | 27/27 uniquely indexed knowledge notes | `SCORECARD.md:394`, `corpus/README.md` |
| operability / hermetic selftest pass fraction | 10.0000 | 310/310 assertions passed (`tools/mado-verify.sh --selftest`) | `SCORECARD.md:396` |
| operability / named-set census (R13 diagnostic subset) | 10.0000 | 4/4 isolated negative cases detected with named sets | `SCORECARD.md:390` |
| freshness / file-plane gate agreement | 10.0000 | 29/29 verdict rows PASS on `--no-live` (0 FAIL, 0 UNKNOWN) | `SCORECARD.md:399` |
| calibration / lesson-grounded admission criteria | 7.0588 | 12/17 criteria citing mined lessons (`corpus/QUALITY.md`) | `corpus/QUALITY.md:6-38` |
| depth | unscored | No bounded rubric established; maintained as technical depth in notes | `SCORECARD.md:414` |
| adjacency | unscored | No bounded rubric; report-not-absorb duty maintained | `SCORECARD.md:415` |

### Confirmation of Lowest Scored Non-Retired Axis
**Coverage / sourced current-art ground is confirmed as the lowest scored non-retired axis at 5.7143/10 (4/7 items).**
Under the canonical `AXES.md` contract (§SCORECARD.md contract and §Working the axes), Round 14 MUST claim an improvement on this lowest axis (C1: U1–U4 4/7 → U1–U5 5/7 = 7.1429/10).

---

## 2. Independent Causal Separability (C1 vs C2)

Round 14 declares two distinct claims:
1. **C1 (Coverage):** Admitting a substantive U5 knowledge note (`output-colour-boundaries-r14.md`) grounded in opened primary specifications S047 (`wlr-output-management-unstable-v1.xml`) and S048 (`color-management-v1.xml`), joined reciprocally in `corpus/SOURCES.md`, indexed in `corpus/README.md`, and explicitly bounding unexercised behavior as `[UNK]`.
2. **C2 (Operability):** Hardening `tools/mado-verify.sh`'s source resolver (`hypr.root.sources_resolve`) to refuse directory-shaped direct targets and glob matches (all-directory or mixed) with stable `non-regular:` diagnostics, supported by isolated negative fixtures and covering mutation tests.

### Proof of Independent Causal Separability
* **C1 can land and verify without C2:** The U5 knowledge note, registry rows S047/S048, and README index update touch only `corpus/` files. The verification of C1 via `.ufo/waves/round-14/measure.py` evaluates header citations, registry joins, markdown table decision facets, and navigation. It does not invoke or depend on `tools/mado-verify.sh`.
* **C2 can land and verify without C1:** The resolver modification, selftest additions, and mutation spec touch only `tools/mado-verify.sh` and wave fixture builders. C2 verification measures gate exit codes and owning-row detail strings (`hypr.root.sources_resolve FAIL non-regular: ...`) across isolated temp trees. It neither reads nor requires any U5 documentation note or S047/S048 registry entries.
* **Conclusion:** C1 and C2 are strictly causally separable. Neither claim creates an execution, syntactic, or verification dependency for the other. Broad replanning is unnecessary and avoided.

---

## 3. U5 Gap & Falsifiable Baseline Examples

### 3.1 C1 Gap: Uncovered Ground U5 (Output Management & Colour Boundaries)
* **Gap Definition:** The historical arc and rounds 12–13 left output configuration and color management as open frontier ground (`corpus/README.md:93-94`, `arc-synthesis.md` §6). S041 (`globals.json`) observed host advertisements `zwlr_output_manager_v1` (v4) and `wp_color_manager_v1` (v3), but these headers alone do not establish whether output management or color management can be executed.
* **Falsifiable Baseline:**
  * `corpus/SOURCES.md` ends at S046; S047 and S048 are absent.
  * Count of admitted `corpus/knowledge/*.md` notes with `covers: U5` and reciprocal mined A/B joins = **0**.
  * Baseline U-item join score: **4/7 = 5.7143/10**.

### 3.2 C2 Gap: Source Resolver Directory Blind Spot (`sources_resolve`)
* **Gap Definition:** In `tools/mado-verify.sh` (lines 2419–2424):
  ```bash
  case "$t" in '~'*) x="$ROOT${t#\~}" ;; *) x="$t" ;; esac
  if [ -e "$x" ]; then continue; fi
  case "$x" in *'*'*) if compgen -G "$x" >/dev/null 2>&1; then continue; fi ;; esac
  tmiss="$tmiss $t"
  ```
  `[ -e "$x" ]` returns TRUE for directories, FIFOs, and sockets. `compgen -G "$x"` returns TRUE if any match exists, even if all matches are directories.
* **Falsifiable Baseline Across the Three Scenarios:**
  1. **Case 1: Direct Directory (`~/.config/hypr/ai-usage.conf` replaced by a directory):**
     * Baseline behavior: `hypr.root.sources_resolve` evaluates `[ -e "$x" ]` → PASS ("declared targets exist, member set exact").
     * **Attribution Nuance (ReviewMeasure H1):** `ai-usage.conf` is also part of `LOCAL` census in `hypr.local.inventory` (line 2450), where `[ -f ]` fails, producing `hypr.local.inventory FAIL missing: ai-usage.conf` and overall exit 1. The baseline gate already exits 1, but the **owning row** `sources_resolve` false-greens!
  2. **Case 2: All-Directory Glob (`~/.local/state/omarchy/toggles/hypr/window-no-gaps.conf` replaced by directory):**
     * Baseline behavior: `compgen -G` matches the directory. `sources_resolve` PASS. Overall exit **0** (true false-green).
  3. **Case 3: Mixed Glob (regular file + directory `extra.conf` under toggles):**
     * Baseline behavior: `compgen -G` matches both. `sources_resolve` PASS. Overall exit **0** (true false-green).
  * Baseline C2 Score: **0/3 detected on the owning row (0.0000/10)**.

---

## 4. UFO-FSD Connector Synthesis & Non-Obvious Move

### Synthesis Across Round 14 Proposals
A review of artifacts from peer seats reveals three major cross-cutting contradictions and risks:

1. **Diagnostic Token Discrepancy (ReviewResolver/ReviewFixtures vs MeasureBuild):**
   * `MeasureBuild` implemented `.ufo/waves/round-14/measure.py` expecting `'non-regular:'` (with hyphen) and the affected basename in `src_detail` (lines 231–232).
   * `ReviewResolver` (F5) and `ReviewFixtures` (F1) proposed emitting `'nonregular:'` (no hyphen).
   * *Second-order consequence:* If `GateImplement` adopts `nonregular:`, the counter `measure.py` silently scores **0/3 (0.0000/10)**!
2. **S048 Upstream Pin Mismatch (ScribeFrontier vs ReviewSourceBar):**
   * `ReviewSourceBar` recommends S048 at `wayland-protocols` commit `35d9638cf0c3f0bbf0c42996580a284f3d8ce564` (sha256 `afa46ce1…`, version 3).
   * `ScribeFrontier` identifies that `3dac056d` (the S005 README pin) declares version 2 and recommends tag `1.49` (`ee78491a237eaff9389a0ccf8680521d074407d3`, version 3).
   * *Second-order consequence:* Reusing the round-13 S005 pin `3dac056d` would introduce a factual contradiction against host advertisement (v3). Both seats agree that version 3 must be pinned.
3. **Attribution Masking on Direct Directory (ReviewMeasure H1/H4 vs AttackMetric):**
   * Direct directory replacement on `ai-usage.conf` exits 1 at baseline via `hypr.local.inventory`. Claiming overall exit 1 as a round-14 detection improvement would be an invalid claim. The metric must strictly isolate `hypr.root.sources_resolve FAIL` containing `non-regular:`.

### The Proposed Move: "Unified Tri-Surface Boundary & Diagnostic Contract (UTBDC)"

We propose one bounded synthesis integrating the round's work across runtime, contract, and verification surfaces:

1. **Canonical Token Contract:**
   * Pin the diagnostic token in `tools/mado-verify.sh` exclusively to `non-regular:` (with hyphen, followed by space-separated targets/basenames).
   * Enforce that glob checking loops over every match: if any match is non-regular (`[ ! -f "$m" ]`), append `non-regular: $t` (or the specific non-regular match basename) and trigger `sources_resolve FAIL`.
2. **Attribution-Honest Scorecard Metrics:**
   * Record C2 as `3/3 named non-regular detections on hypr.root.sources_resolve` (0/3 → 3/3, 10.0000/10 on this finite diagnostic subset).
   * Report overall exit codes and `hypr.local.inventory` side-effects separately, explicitly noting that baseline `direct-directory` already exited 1 via local inventory while `sources_resolve` false-greened.
3. **Two-Phase Decision Fences in U5 Note:**
   * Author `output-colour-boundaries-r14.md` using the exact table-row semantic facets checked by `measure.py`: `output-management` (S047), `colour` (S048), and `feature unknown` / `unexercised` (`[UNK]`).
   * Structure the note around the three-question boundary table established by EvidenceChain, grounding transactional output configuration (`test` vs `apply` failure independence) and color capability negotiation (dynamic feature queries vs display reality).
4. **Resolution of Outside Rulings (R13-V1..V3):**
   * Apply R13-V1 as an append-only erratum to `corpus/knowledge/wayland-protocol-boundaries-r13.md` (specifying that `globals[]` carries only interface/version while sanitized probe/session metadata is also retained).
   * Apply R13-V2 as an append-only block to `corpus/knowledge/gate-standing-use.md` (clarifying that `boundary.readonly PASS` confirms within-run config stability, not cross-revision output equality).
   * Adopt `receipt.py` (built by `ReceiptBuild`) for forward-looking standalone receipts with source-worktree digest matching (R13-V3).
5. **Preservation Controls:**
   * Pin the isolated source-order swap fixture (`monitors.conf` and `input.conf` swapped) as an un-scored preservation control, confirming that positional ordering in `hypr.root.include_graph` remains active without claiming existing behavior as an improvement.

---

## 5. Risks and Mitigations

| Risk | Severity | Second-Order Impact | Mitigation |
|---|---|---|---|
| **Diagnostic Token Desynchronization** | High | `tools/mado-verify.sh` emits `nonregular:` while `measure.py` checks `non-regular:`, resulting in 0/3 score. | Contract strictly pins `non-regular:` across `GateImplement`, `measure.py`, and `regular-target.spec`. |
| **Regression Target Movement (PIN_MADO)** | High | Edits to `tools/mado-verify.sh` outside R7 blocks move the derived target; `--regression` reports SETUP (exit 2). | Expected by contract; `GateImplement` must not fake the pin. L1 performs the re-cut post-integration. |
| **All-Directory Glob Collateral Failure** | Medium | Removing `window-no-gaps.conf` from the fixture affects `hypr.toggle.no_gaps` (NOTE/FAIL). | Assert `hypr.toggle.no_gaps NOTE` as an explicit collateral expectation in selftest, or use mixed-glob as the primary discriminator. |
| **S048 Version Inconsistency** | Medium | Citing an upstream revision that defines version 2 while claiming version 3. | Pin S048 to `wayland-protocols` commit `35d9638c` or tag `1.49` (`ee78491a`), both verified to define `wp_color_manager_v1` v3. |
| **Overreach into Display / DRM Province** | Low | Confusing compositor Wayland protocols with kernel modesetting / DRM leases. | Strict boundary: DRM and KMS hardware diagnosis belongs to sibling `tsukuroi`; `mado` governs only compositor configuration and Wayland interfaces. |

---

## 6. Verification Plan for L1 Integration

1. **Gate Hermetic Selftest:**
   `bash tools/mado-verify.sh --selftest` (must pass all assertions, count ≥ 313 including N9, N10, N11).
2. **File Plane Agreement:**
   `bash tools/mado-verify.sh --no-live` (must remain 29 PASS, 0 FAIL, 0 UNKNOWN, 8 SKIP, 4 NOTE).
3. **C1 & C2 Revision-Bound Measurement:**
   `python3 .ufo/waves/round-14/measure.py <pinned-rev>`:
   * `coverage.count` = 5, `coverage.score` = 7.1429/10, U5 joined with S047 and S048.
   * `exact_set.detected` = 3/3, `exact_set.score` = 10.0000/10.
   * Controls `clean.exact_set_pass` = True, `order_swap.order_detected` = True, `order_swap.set_retained` = True.
4. **Standalone Receipt Validation:**
   `python3 .ufo/waves/round-14/receipt.py --selftest` (all 13 isolated assertions pass).
5. **Maintained Source Census:**
   `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin mado` (exit 0, `mado ok`, zero errors).
6. **Regression Re-Cut:**
   Re-cut `PIN_MADO` and `TABLE_MADO` via the printed command in `tools/mado-verify.sh --regression`, verifying 10/10 killed historical mutants and 8/8 covering mutants.
