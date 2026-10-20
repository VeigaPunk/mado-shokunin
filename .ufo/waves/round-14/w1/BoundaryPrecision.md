# BoundaryPrecision — R13-V1/V2 Boundary Precision, Data Classification & Errata Text

**Seat:** `MadoR14.BoundaryPrecision` (connector, leaf)  
**Target:** `/home/vgpnk/Projects/shokunin/mado-shokunin`  
**Milestone:** U5 boundaries and regular-source targets  
**Axes:** `coverage` (C1), `operability` (C2)  
**Status:** Complete findings and draft errata/correction texts. Read-only observations only; no mutating commands, no shared-file edits.

---

## 1. Axes & Core Proposal

| Axis | Role & Impact | Non-Regressive Boundary |
|---|---|---|
| **coverage (C1)** | Clarifies the exact evidentiary limits of U4 (protocol phase & advertised globals). Delineates individual interface records from session-level capture metadata, preventing over-claiming of host properties or under-reporting of retained telemetry. | Knowledge notes maintain strict distinction: advertisement $\neq$ binding $\neq$ runtime feature execution. Upstream protocol phases are separate from host observations. |
| **operability (C2)** | Resolves the conflation between within-run execution isolation (`gate boundary.readonly`) and cross-revision artifact invariance. Protects test harness and gate provenance by retaining exact file-plane receipts without modifying historical gates or filed fleet reports. | Does NOT edit `tools/mado-verify.sh` boundary strings (which would invalidate gate SHA256 `037b05dc…` and break regression pins). Legitimate 29 PASS / 0 FAIL / 0 UNKNOWN results are fully preserved. |

### Summary of Non-Obvious Disconnects Addressed

1. **R13-V1 (Retained-Data Scope in U4):**
   In `corpus/knowledge/wayland-protocol-boundaries-r13.md:43`, the text asserted:
   > *"The retained S041 data is only registry interface/version headers: output identity, device paths, human-readable seat names, geometry, colourimetry and numeric registry names were discarded."*

   As identified by the independent integrator in `corpus/lessons/round-13-verifier-spotcheck.md:203` (R13-V1), this statement was overly broad. While the individual items in the `.globals[]` list contain strictly `interface` and `version`, the S041 capture file (`.ufo/waves/round-13/w1/globals.json`) also retains top-level sanitized metadata: probe parameters, package/tool versions, compositor commit/tag, socket identity (`wayland-1`), and correlation booleans. Later in the same note (`## Host point sample`, lines 45–47), this session correlation was acknowledged, creating an internal textual inconsistency.

2. **R13-V2 (Single-Run Boundary vs. Cross-Revision Output):**
   In the filed fleet report `.ufo/reports/round-13/mado.md:68`, the file-plane health table entry reads:
   > `| File-plane health | bash tools/mado-verify.sh --no-live | **29 PASS, 0 FAIL, 0 UNKNOWN, 8 SKIP, 4 NOTE**, CLEAN, exit 0; byte-identical before/after |`

   The trailing phrase `"byte-identical before/after"` is ambiguous out of context: an outside reader could interpret it as claiming that gate outputs or configuration trees are identical *across Git revisions* (before vs. after Round 13). In truth, `tools/mado-verify.sh:2703` executes a within-run boundary check (`gate boundary.readonly PASS`) confirming that `$ROOT/.config/hypr` has identical combined SHA-256 before and after *that specific run* (`3cb692751b4d…`). Across rounds, the configuration tree legitimately changed (Round 12 before: `364b4f5e672b…`; Round 12 after: `48c882b98e97…`; Round 13: `3cb692751b4d…`).

---

## 2. Technical Grounding & File Classification

### 2.1 Global Records vs. Metadata Envelope (`globals.json` / S041)

Analysis of `.ufo/waves/round-13/w1/globals.json` (SHA-256 `ced47240c2a1941bbbf1f125d9a1e41624cfeeb8218ab2a3a425eb335a08a949`):

- **Global Records (`.globals[]` array, 72 entries):**
  Each record contains exclusively:
  ```json
  {
    "interface": "<string>",
    "version": <integer>
  }
  ```
  Numeric registry object names (`name`), physical device paths, connector IDs, geometry coordinates, colorimetry profiles, and interface-specific attributes are completely stripped.
- **Top-Level Metadata Envelope:**
  Retains necessary provenance and environment parameters for falsifiability:
  - `schema`: `"mado-globals-capture-v1"`
  - `captured_utc`: ISO-8601 timestamp (`2026-10-20T04:10:03Z`)
  - `probe`: `command` (`"wayland-info"`), `return_code` (`0`), `stderr_bytes` (`0`), `display_socket` (`"wayland-1"`), sanitization policy
  - `tool`: package name (`"wayland-utils"`), version (`"1.3.0-1"`), binary sha256 (`d9d851d5…`), soname linkage
  - `compositor`: `name` (`"Hyprland"`), `version` (`"0.56.2"`), `tag` (`"v0.56.2"`), `commit` (`"efb50993780079460b0cbed1363e2166a2de1d9f"`), dirty flag, probe command/code
  - `global_count`: 72, `unique_interface_count`: 71, `multiplicity`: `wp_drm_lease_device_v1` (count 2)
  - `set_sha256`: `"9569d02fe2b04bf62079258b1d74f5d2ad8510c26ef0710a1a64c95f1a9becaa"`
  - `session_binding`: correlation booleans, instance count (`1`), `wl_socket` (`"wayland-1"`), probe return code
  - `excluded`: explicit audit list of omitted properties (e.g., `wl_output` geometry, `zxdg_output_manager_v1` logical IDs, `wp_color_manager_v1` colorimetry blocks)

**Classification Rule:**
Global records contain interface name and advertised version *only*. The top-level document structure retains sanitized provenance and session-correlation metadata. Neither layer stores raw device identities, hardware serials, user titles, or private runtime state.

### 2.2 Within-Run Byte Boundary vs. Cross-Revision Outputs

- **Within-Run Boundary Check (`tools/mado-verify.sh`):**
  - Line 2703 (and line 2854 in `--no-live`):
    `row gate boundary.readonly PASS "config plane byte-identical before/after (combined sha ${before:0:12}…)"`
  - Mechanism: hashes the target directory immediately before verification runs, hashes it immediately after all read-only checks finish, and confirms `$before == $after`.
  - Scope: proves *hermeticity and read-only non-mutation of the host during that execution*.
- **Cross-Revision State Differences:**
  - Receipts across project history show distinct combined config hashes:
    - Round 12 baseline: `364b4f5e672b…` (`.ufo/evidence/round-12/before-no-live.txt:44`)
    - Round 12 post-fix: `48c882b98e97…` (`.ufo/evidence/round-12/gate-no-live-after.txt:44`)
    - Round 13 verified: `3cb692751b4d…` (`.ufo/waves/round-13/evidence/gate-file-plane.txt:47`)
  - A claim of "byte-identical before/after" across revisions would be false and contradicted by committed evidence.

**Governing Operational Rule:**
- **Do not edit filed fleet report:** `.ufo/reports/round-13/mado.md` is an immutable, filed historical artifact at the fleet level.
- **Do not modify gate row text:** Editing `tools/mado-verify.sh:2703` alters the gate binary digest away from pinned `037b05dc…`, which would break the regression gate without authorization.
- **Apply corrections append-only:** Clarify precision via errata in the knowledge note, `gate-standing-use.md`, `LOG.md`, and the Round 14 lesson.

---

## 3. Exact Append-Only Erratum Text for U4

To be appended to `corpus/knowledge/wayland-protocol-boundaries-r13.md` (after line 104, below `## Limits`):

```markdown
## Errata (append-only — add blocks, never edit above)

### R13-V1 (round 14, 2026-10-20) — retained-data wording and scope
- Prior text (line 43, preserved above):
  > "The retained S041 data is only registry interface/version headers: output identity, device paths, human-readable seat names, geometry, colourimetry and numeric registry names were discarded."
- Correction and clarification:
  The global records array (`.globals[]`) in `.ufo/waves/round-13/w1/globals.json` retains exclusively `interface` and `version` pairs. The capture file envelope also retains sanitized provenance and session-correlation metadata: probe status (`wayland-info`), tool package/binary pins (`wayland-utils 1.3.0-1`), compositor build pins (`Hyprland 0.56.2 @ efb5099`), total/unique object counts, duplicate multiplicity, set digest, and the non-atomic session correlation (`wl_socket: wayland-1`), as documented under "Host point sample". The `excluded` array explicitly records the omitted device paths, numeric names, and colorimetry blocks.
- Invariant:
  This clarification confirms that no raw output identities, display geometry, or private device state were retained, and that advertisement discovery does not constitute feature execution.
```

---

## 4. Exact Correction Text for `LOG.md`

To be appended to `LOG.md` under the active Round 14 record section (or appended as a precision note to Round 13 closure):

```markdown
### 2026-10-20 — Errata & Precision Notes (R13-V1 & R13-V2)

- **R13-V1 (U4 S041 data retention precision):**
  Clarified `corpus/knowledge/wayland-protocol-boundaries-r13.md:43` append-only. The individual global records in `globals.json` are strictly interface/version pairs. Sanitized top-level metadata (probe return code, package/compositor commit pins, object counts, and correlated Wayland socket `wayland-1`) is also retained as documented in the capture schema. No raw hardware identifiers or colorimetric calibration data were retained.
- **R13-V2 (Boundary precision vs. cross-revision output):**
  Clarified the scope of `gate boundary.readonly PASS` in filed report `.ufo/reports/round-13/mado.md:68`. The receipt (`gate-file-plane.txt:47`, combined hash `3cb692751b4d…`) proves that the configuration plane is byte-identical before and after that single file-plane run (read-only execution fence). It does not assert byte-identity of configuration trees or gate outputs across Git revisions (Round 12 before `364b4f5e…`, Round 12 after `48c882b9…`, Round 13 `3cb69275…`). The legitimate 29 PASS / 0 FAIL / 0 UNKNOWN result is unchanged.
```

---

## 5. Exact Correction Text for Lesson (`corpus/lessons/round-14.md` / `round-13.md`)

For incorporation into `corpus/lessons/round-14.md` § Mistakes / Outside Corrections:

```markdown
### Outside Verifier Corrections (R13-V1 & R13-V2)

| id | class | evidence pointer | captured-by | fix |
|---|---|---|---|---|
| R13-V1 | data-boundary wording | `corpus/knowledge/wayland-protocol-boundaries-r13.md:43`; `round-13-verifier-spotcheck.md:203` | Outside integrator review | Appended erratum to U4 note distinguishing individual `globals[]` records (interface/version only) from top-level sanitized metadata (pins, counts, socket). Line 43 preserved verbatim. |
| R13-V2 | receipt scope precision | `.ufo/reports/round-13/mado.md:68`; `tools/mado-verify.sh:2703`; `gate-file-plane.txt:47` | Outside integrator review | Appended precision note to `gate-standing-use.md` and `LOG.md`. Reaffirmed that `boundary.readonly` confirms single-run read-only hermeticity, not cross-revision invariance. Filed fleet report and gate row strings preserved without edits. |
```

And companion append-only errata for `corpus/knowledge/gate-standing-use.md` (after line 402):

```markdown
## Errata — round 14, R13-V2 (2026-10-20): boundary scope precision

- Scope of `gate boundary.readonly PASS`: In a file-plane gate run, the target configuration directory digest taken immediately before execution matches the digest taken immediately after completion. Round-13 receipt: `.ufo/waves/round-13/evidence/gate-file-plane.txt:47`, combined SHA `3cb692751b4d…`; counts 29 PASS / 0 FAIL / 0 UNKNOWN / 8 SKIP / 4 NOTE, exit 0.
- Cross-revision distinction: This verification does not assert or imply that configuration state is byte-identical across revisions or separate historical runs. Committed hashes differ across milestones (Round 12 before `364b4f5e672b…`, Round 12 after `48c882b98e97…`, Round 13 `3cb692751b4d…`).
- Fleet report interpretation: The summary phrase "byte-identical before/after" in `.ufo/reports/round-13/mado.md:68` refers strictly to the within-run read-only invariant above. The filed report remains historical and unedited.
```

---

## 6. Acceptance Checklist for L1 Integration

- [x] **V1-1:** U4 knowledge note line 43 is unedited; exact append-only erratum block is drafted.
- [x] **V1-2:** Distinguishes global records (`interface`, `version`) from envelope metadata (`probe`, `tool`, `compositor`, `counts`, `session_binding`).
- [x] **V1-3:** Discarded categories verified against `excluded` in `globals.json`; no raw device/output identity retained.
- [x] **V2-1:** Boundary row text in `tools/mado-verify.sh` (`gate boundary.readonly PASS`) is left strictly untouched, protecting gate SHA256 pin `037b05dc…`.
- [x] **V2-2:** Filed fleet report `.ufo/reports/round-13/mado.md` is left strictly untouched in the fleet root.
- [x] **V2-3:** Clear distinction documented between single-run execution invariant and cross-revision hash deltas.
- [x] **V2-4:** Full preservation of legitimate Round 13 verdict: 29 PASS, 0 FAIL, 0 UNKNOWN, exit 0.
- [x] **V3 Connection:** Confirms that future standalone receipts will use the revision-bound `receipt.py` wrapper without retroactively mutating `gate-selftest.txt`.
