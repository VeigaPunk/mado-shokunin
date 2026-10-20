# GapCensus Scout Report — Mado Round 15 (Wave 1)

- **Date:** 2026-10-20
- **Seat:** `MadoR15.GapCensus`
- **Role:** Scout (UFO-FSD leaf subagent — no delegation, no background jobs, no test/build/lint runs, no shared-file edits)
- **Target:** `/home/vgpnk/Projects/shokunin/mado-shokunin`
- **Baseline Revision:** `ea0446fcb4840089f0e541d96350144506fb5d1d` (Round 15 baseline)
- **Judged on:** `coverage`
- **Milestone:** U6 input evidence ladder and R14 ancillary provenance correction
- **Assigned Scope:** Read SCORECARD U1–U7 rubric and corpus README frontier; exact U6 absence sweep through corpus knowledge header metadata (no tests); report U7 retained gap.

---

## 1. Godspeed Principles & Axis Mapping

1. **Name the axes:**
   - **Coverage (primary active axis):** Sourced current-art ground rubric $10 \times \text{covered U-items} / 7$. Baseline is $5/7 = 7.1429/10$ (U1–U5 covered). Target is $6/7 = 8.5714/10$ by admitting a bounded U6 input-debugging layer route.
   - **Operability:** Retains hermetic selftest (372/372) and exact regular-target / set-census diagnostics; harm watch only.
   - **Freshness:** File-plane agreement (`tools/mado-verify.sh --no-live`); harm watch only.
   - **Calibration:** Lesson-grounded criteria; R14-V1 ancillary provenance correction is an unscored lesson-backed precision fix.
   - **Depth & Adjacency:** Unscored, retained boundaries.

2. **Iterate cheap, in parallel:**
   - Provide clean, deterministic census data to peer seats (`MadoR15.PlanningWalk`, `MadoR15.ScribeFrontier`, `MadoR15.ReviewCensus`, `MadoR15.ReviewSeat`, `MadoR15.ReviewQuotes`) without blocking on gate or build cycles.

3. **Keep moves that improve any axis and harm none:**
   - Establish that U6 is completely absent from all admitted knowledge headers so that Round 15's addition is strictly additive ($5/7 \rightarrow 6/7$) with no collisions, while preserving U7 as the explicitly retained gap.

4. **Don't aim — let the frontier walk itself:**
   - Rely solely on literal header metadata and registered gap ledgers from repo bytes, without inventing or inferring unverified capability.

---

## 2. SCORECARD U1–U7 Rubric Analysis

### 2.1 Rubric Specification
In `SCORECARD.md` (lines 237, 242–249, 334–338, 463–467, 600–612):
- **Scored sub-axis:** `coverage / sourced current-art ground`
- **Rubric formula:** $\text{Score} = 10 \times \frac{\text{covered U-items}}{7}$
- **Coverage criteria:**
  1. An admitted Markdown file exists in `corpus/knowledge/*.md`.
  2. The file's first 15 lines contain the provenance header trio:
     - `source:` citing one or more valid IDs in `corpus/SOURCES.md`.
     - `verified-at:` with an ISO date or timestamp.
     - `recheck:` with an explicit invalidation/review trigger.
  3. The header contains exactly one `covers: U<n>` line ($n \in \{1..7\}$).
  4. The cited source IDs join reciprocally to rows in `corpus/SOURCES.md` that have `status = mined`, Tier `A` or `B`, and list the knowledge file in their `used-by` column.

### 2.2 Pre-Registered U-Items Ledger
Pre-registered in Round 12 (`SCORECARD.md:242-249`), grounded in `corpus/knowledge/arc-synthesis.md` §6 and the kaika ART dossier:
- **U1 — Per-window rule effects:** Covered in Round 12 by `corpus/knowledge/window-rule-effects-getprop.md` (`covers: U1`, citing S002, S016–S020). Corrected arc's "no rule-read verb" via read-only `hyprctl getprop`.
- **U2 — Hyprland configuration-language era:** Covered in Round 12 by `corpus/knowledge/hyprland-config-era-r12.md` (`covers: U2`, citing S021–S029, S017). Pinned hyprlang $\rightarrow$ Lua transition.
- **U3 — XDG portal backend routing and ScreenCast lifecycle:** Covered in Round 12 by `corpus/knowledge/xdg-portal-routing-r12.md` (`covers: U3`, citing S031–S035, S037).
- **U4 — Wayland protocol phase and compositor-advertised globals:** Covered in Round 13 by `corpus/knowledge/wayland-protocol-boundaries-r13.md` (`covers: U4`, citing S005, S040–S043, S046). Required 3/3 structural facets (`phase`, `advertisement`, `unexercised_behavior`).
- **U5 — Output management / colour boundary:** Covered in Round 14 by `corpus/knowledge/output-colour-boundaries-r14.md` (`covers: U5`, citing S047, S048, S050, S041). Required reciprocal A/B joins and decision section facets.
- **U6 — Kernel-input → Wayland debugging ladder:** Target of Round 15 Claim C1. Bounded route from opened primary sources (e.g. S007, S008, S051, S052), requiring layer ladder, safe boundary, and unexercised delivery sections.
- **U7 — Waybar module text:** Retained gap ($1/7$). Uncovered in current and previous rounds.

---

## 3. Corpus README Frontier Analysis

In `/home/vgpnk/Projects/shokunin/mado-shokunin/corpus/README.md` (§ `## Frontier`, lines 72–102):
1. **Unresolved Surfaces Ledger:**
   - Index completeness does not retire underlying unresolved surfaces: rendered UI, Waybar module text, Walker socket protocol, dispatcher behavior, and per-window rule effects (derived from `arc-synthesis.md` §6).
   - "Still open: rule attribution, output-management behavior, the input debugging ladder and Waybar module text — study paths and queued sources in SOURCES." (`corpus/README.md:94-95`).
2. **Cumulative Frontier Progression:**
   - Round 12: Moved U1, U2, and U3 onto sourced ground.
   - Round 13: Moved U4 (protocol-phase and advertised-global diagnostic route) onto sourced ground.
   - Round 14: Moved U5 (documented output-management/colour boundary route) onto sourced ground.
   - Round 15: Targets U6 (input evidence ladder) as the sole active claim, leaving U7 explicitly unexercised.

---

## 4. Exact U6 Absence Sweep Through Corpus Knowledge Headers

A static inspection of the first 15 lines of all 28 knowledge notes in `/home/vgpnk/Projects/shokunin/mado-shokunin/corpus/knowledge/` yielded the following exhaustive inventory:

| Note Name | Header `covers:` | Header `source:` | Header `verified-at:` | Header `recheck:` | Admitted Status |
|---|---|---|---|---|---|
| `arc-synthesis.md` | *none* | Yes | Yes | Yes | Historical Arc Synthesis |
| `closeout-r11.md` | *none* | Yes | Yes | Yes | Historical Closeout |
| `config-drift-r12.md` | *none* | Yes | Yes | Yes | Drift Analysis |
| `config-health-report-r3.md` | *none* | *none* | *none* | *none* | Historical Round 3 Report |
| `executor-test-sufficiency.md` | *none* | *none* | *none* | *none* | Historical Round 3 Report |
| `gate-mutation-proof.md` | *none* | *none* | *none* | *none* | Historical Round 6 Proof |
| `gate-mutation-sweep-r8.md` | *none* | *none* | *none* | *none* | Historical Round 8 Sweep |
| `gate-standing-use.md` | *none* | Yes | Yes | Yes | Gate Invocation Standard |
| `hyprctl-verification-layer.md`| *none* | *none* | *none* | *none* | Historical Round 2 Layer |
| `hyprland-config-era-r12.md` | **U2** | Yes | Yes | Yes | **Admitted (U2)** |
| `hyprland-config-plane.md` | *none* | *none* | *none* | *none* | Historical Round 1 Plane |
| `idle-lock-plane.md` | *none* | *none* | *none* | *none* | Historical Round 4 Plane |
| `keybind-rule-semantics.md` | *none* | *none* | *none* | *none* | Historical Round 2 Semantics |
| `omarchy-drift-watch.md` | *none* | *none* | *none* | *none* | Historical Round 6 Watch |
| `output-colour-boundaries-r14.md` | **U5** | Yes | Yes | Yes | **Admitted (U5)** |
| `province-accuracy-selfaudit.md` | *none* | *none* | *none* | *none* | Historical Round 4/5 Audit |
| `remaining-planes-census.md` | *none* | *none* | *none* | *none* | Historical Round 6 Census |
| `snapshot-diff-receipt-r9.md` | *none* | *none* | *none* | *none* | Historical Round 9 Receipt |
| `terminals-and-omarchy.md` | *none* | *none* | *none* | *none* | Historical Round 1 Note |
| `theme-wallpaper-plane.md` | *none* | *none* | *none* | *none* | Historical Round 7 Plane |
| `walker-deep-r9.md` | *none* | *none* | *none* | *none* | Historical Round 9 Note |
| `walker-deep.md` | *none* | *none* | *none* | *none* | Historical Round 5 Note |
| `walker-live-surface.md` | *none* | *none* | *none* | *none* | Historical Round 7 Surface |
| `waybar-walker-plane.md` | *none* | *none* | *none* | *none* | Historical Round 1 Plane |
| `waybar-walker-semantics.md` | *none* | *none* | *none* | *none* | Historical Round 3 Semantics |
| `wayland-protocol-boundaries-r13.md` | **U4** | Yes | Yes | Yes | **Admitted (U4)** |
| `window-rule-effects-getprop.md` | **U1** | Yes | Yes | Yes | **Admitted (U1)** |
| `xdg-portal-routing-r12.md` | **U3** | Yes | Yes | Yes | **Admitted (U3)** |

### 4.1 Sweep Findings:
1. **Total Knowledge Notes:** 28 files.
2. **Notes with `covers:` tag:** Exactly 5 (`U1`, `U2`, `U3`, `U4`, `U5`).
3. **Notes with `covers: U6` in header:** Exactly **0**.
4. **Notes with `covers: U7` in header:** Exactly **0**.
5. **Occurrences of the literal string `U6` in corpus knowledge text:**
   - `config-health-report-r3.md:998`: Historical Round 3 internal item label (§8 U6).
   - `gate-mutation-proof.md:167`: Historical Round 6 scratch residual unknown U6.
   - `gate-mutation-sweep-r8.md:169`: Historical Round 8 scratch residual unknown U6.
   - `province-accuracy-selfaudit.md:341`: Historical Round 4 self-audit unknown U6.
   - `snapshot-diff-receipt-r9.md:169`: Historical Round 9 write-lock unknown U6.
   - `walker-deep.md:481, 494, 495`: Historical Round 1/3 launcher emergency unknowns.
   - `wayland-protocol-boundaries-r13.md:8`: Explicit non-coverage disclaimer ("It does not close protocol request behavior, output management/colour (U5), the kernel-input ladder (U6), or Waybar module text (U7).").
   - `output-colour-boundaries-r14.md:108`: Explicit non-coverage disclaimer ("These are explicit rejected inferences, not newly discovered failed host features. U6 input debugging and U7 Waybar module text remain outside this entry.").
6. **Verdict on U6 Absence:** Zero admitted notes cover U6. U6 is strictly open ground at baseline `ea0446fc`.

---

## 5. Report on U7 Retained Gap

### 5.1 Identity and Provenance of U7
- **Name:** U7 — Waybar module text.
- **Originating Ledger:** `corpus/knowledge/arc-synthesis.md` §6 (Gap ledger, line 301):
  ```text
  | waybar module text | no IPC/query verb in waybar 0.15.0 (r3 anti-claim branch) |
  ```
- **Semantic Root:** Established in `corpus/knowledge/waybar-walker-semantics.md` (MADO-R3-1) §2.3 and §6.8: Waybar version 0.15.0 exposes no IPC socket, query verb, or runtime introspection protocol to read rendered module contents.

### 5.2 Why U7 Stays an Unresolved Gap
1. **Introspection Boundary:** Waybar is a consumer of status information, not an introspection server. While individual read-only producers (such as custom scripts or command runners) can be sampled, the actual formatted, styled, and displayed widget text exists only within the Waybar process memory.
2. **Measurement Constraint:** Extracting live rendered text would require:
   - Visual capture (screenshots via `grim`) paired with OCR, which was evaluated in Round 1/2 as a one-off probe but explicitly barred as a repeatable verdict input.
   - Attaching debuggers or injecting code into the Waybar process, which violates the strict non-destructive, read-only shokunin contract.
3. **Anti-Claim Application:** Rather than fabricating synthetic or proxy claims, the lane maintains an explicit anti-claim: live rendered module text is classified as `[UNK]`.

### 5.3 Retained Gap Status in Round 15
- In Round 15, Claim C1 advances coverage from $5/7$ to $6/7$ by covering U6 (kernel-input $\rightarrow$ Wayland debugging ladder).
- **U7 is deliberately and explicitly retained as the remaining $1/7$ gap.**
- Retaining U7 ensures that the denominator of 7 remains sound, that no unverified or simulated visual inspection is claimed, and that the lane's coverage score accurately reflects the finite limit of non-intrusive current-art verification.

---

## 6. Sourced Grounding & Evidence Pointers

| Item / Path | Revision / Anchor | Quote (≤25 words) | Tier / Category | Role in Census |
|---|---|---|---|---|
| `SCORECARD.md` | `ea0446fc` (`:601-608`) | "C1 coverage, lowest non-retired current-art rubric: sourced U1–U5 5/7 (7.1429/10) → sourced U1–U6 6/7 (8.5714/10)." | Tier A / `spec` | Canonical definition of C1 target and baseline. |
| `corpus/README.md` | `ea0446fc` (`:94-95`) | "Still open: rule attribution, output-management behavior, the input debugging ladder and Waybar module text" | Tier A / `docs` | Current frontier definition confirming U6 and U7 open. |
| `arc-synthesis.md` | `a5b48331` (`:301`) | "waybar module text \| no IPC/query verb in waybar 0.15.0 (r3 anti-claim branch)" | Tier A / `knowledge` | Grounding for U7 gap classification. |
| `wayland-protocol-boundaries-r13.md` | `6459345a` (`:8`) | "It does not close protocol request behavior, output management/colour (U5), the kernel-input ladder (U6), or Waybar module text (U7)." | Tier A / `knowledge` | R13 boundary disclaimer confirming U6/U7 excluded. |
| `output-colour-boundaries-r14.md` | `bb2f150a` (`:108`) | "U6 input debugging and U7 Waybar module text remain outside this entry." | Tier A / `knowledge` | R14 boundary disclaimer confirming U6/U7 excluded. |

---

## 7. Tooling Record

- **Tooling Directive Compliance (RULES.md):**
  - No system packages, Python packages, cargo crates, npm modules, or external binaries were installed or updated.
  - All inspections were read-only queries of committed repository files.
  - Zero test runs, gates, linter executions, or live probes were initiated.
