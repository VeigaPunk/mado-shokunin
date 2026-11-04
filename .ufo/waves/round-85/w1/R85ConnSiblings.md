# R85ConnSiblings — Cross-Lane Overlap Scan & Bounded Synthesis

## 1. Scope and Declared Axes

- **Role:** UFO-FSD connector / leaf seat (read-only scan, no subagent dispatch).
- **Lane Root:** `/home/vgpnk/Projects/shokunin/mado-shokunin`
- **Freeze Revision:** `3905311c75a39c5710413105865c0a1a7dd0116a` (base `5f174ca48d4f9cf94abf1a8c58b7d6f88733aced`).
- **Declared Round Axes:**
  1. **Coverage** (C1: declaration-identity refusals carry their own `cause=` token; 72 frozen cases, 51 mutants; `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-85/claims-declaration-r85.md:13-72`).
  2. **Operability** (C2: executable runbook rows bind producer status class `ok` / `exact` / `signal`; 36 frozen rows, 37 mutants; `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-85/claims-declaration-r85.md:74-123`).
- **Operational Discipline:** Read-only analysis across sibling lanes and mado round-85 artifacts. No mutating git/jj commands, no edits outside this report file, no tool installs/updates, and no absorption of another lane's findings.

---

## 2. Cross-Lane Overlap Scan: Pipeline Status / `pipefail` / Exit-Status

### (a) Confirmation and Correction of the Ownership Map

The prompt's baseline map specifies:
> *tameshi owns mutation/testing method, tsukuroi owns OS diagnosis, kumitate fleet tooling: confirm or correct that map against what you find*

An exhaustive cross-lane scan of all twenty sibling lanes in `/home/vgpnk/Projects/shokunin` (`SKILL.md`, `PROVINCE.md`, `tools/`, `corpus/`) **confirms** this map and refines the precise jurisdictional boundaries:

| Lane | Core Domain | Exact File:Line Evidence | Boundary & Overlap Analysis |
|---|---|---|---|
| **tsukuroi-shokunin** | OS diagnosis & host integrity | `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/PROVINCE.md:8-14,35-42`; `SKILL.md:3851-3893,3958-3978,4246-4258`; `tools/recheck-eventlog-r59.sh:100-102,174-175` | **Confirmed:** Tsukuroi owns OS diagnosis (package, storage, boot-chain, event-log integrity). It pioneered the analysis of POSIX shell early-reader SIGPIPE failures under `set -euo pipefail` (Round 42 R41-CENSUS-PIPEFAIL-692, `SKILL.md:3851-3893`; Round 43 boot-input unreadable directory fail-open, `SKILL.md:3958-3978`; Round 45 first-line reader `printf \| head -n1` SIGPIPE exit 141, `SKILL.md:4246-4258`). In Round 59, it captured pipeline stage exits via `PIPESTATUS[0]` (`tools/recheck-eventlog-r59.sh:102,175`). Tsukuroi's pipefail work governs **probe robustness during OS diagnosis**, NOT general desktop runbook semantics or Wayland pipeline contracts. |
| **tameshi-shokunin** | Verification-fixture craft & mutation method | `/home/vgpnk/Projects/shokunin/tameshi-shokunin/PROVINCE.md:3-7,28-36,95,104`; `tools/mutate-and-run.sh:183,1169,2081`; `tools/tally-audit-v*.py:278,453` | **Confirmed:** Tameshi owns reusable verification craft, mutation testing frameworks, and tally audit methods (`PROVINCE.md:3-7`). Its test execution runner operates under `set -u -o pipefail` (`tools/mutate-and-run.sh:183,2081`), catching empty grep failures (`:1169`). Crucially, `PROVINCE.md:95,104` explicitly stipulates that the mutation testing method is held while sibling gate ownership remains untouched. Tameshi owns the **reusable testing methodology**, NOT mado's runbook execution or desktop state observation. |
| **kumitate-shokunin** | Fleet orchestration & tooling | `/home/vgpnk/Projects/shokunin/kumitate-shokunin/PROVINCE.md:3,51`; `SKILL.md:620,622,626,642`; `scripts/cap-run.mjs`; `scripts/receipt-attest.mjs` | **Confirmed:** Kumitate owns fleet tooling, task dispatch, and execution sandboxing (`PROVINCE.md:3`). Its `cap-run.mjs` runner (`SKILL.md:620`) executes processes under `bwrap --unshare-pid` and transient cgroup scopes, capturing exit code, OOM kills, timeouts, and signal death (`CAP_RUN: EXIT\|OOM\|BUDGET\|SIGNAL code=<n> unit=<unit>`). Kumitate also governs receipt attestation (`receipt-attest.mjs`, `receipt-evidence.mjs`) and the cross-gate harm matrix (`harm-matrix.mjs:642`, which catches missing verdicts and signal death). Kumitate owns **fleet-level process supervision and runner contracts**, NOT lane-internal shell pipeline status classes. |

### (b) Additional Siblings Encountering Pipeline Status

The scan identified several other sibling lanes that encounter `pipefail`, `PIPESTATUS`, or signal exits (`128+N`), but none asserts domain ownership over pipeline status:
1. **mori-shokunin** (`tools/mori-census.sh:655,661,741,2450-2452`): Documents historical pipeline silent crashes (`corpus/lessons/2026-10-15-errexit-pipefail-silent-crash.md`). It applies defensive `\|\| true` guards against early-reader SIGPIPE 141 in storage probes. This is treated as local script hygiene, not an owned domain.
2. **souji-shokunin** (`tools/cand-census-01.sh:167-170,200`; `tools/souji-census.sh:1283-1286,1318`; `tools/souji-quarantine.sh:1029`): Explicitly toggles `set +o pipefail` / `set -o pipefail` around `find` pipelines to ensure filesystem permission errors do not abort hygiene sweeps, and notes that downstream SIGPIPE must not fabricate false "novel" classifications.
3. **kaidoku-shokunin** (`tools/round-64/jsc-route-matrix.py:27,90`; `tools/round-65/jsc-closure-matrix.py:141`): Implements explicit normalization between Python subprocess return codes (`-signo`) and POSIX shell signal reporting (`128+signo`) for binary / JavaScriptCore execution.
4. **game-dev-2d-shokunin** (`corpus/live/r92-reviewer/tools/discrimination.py:68`; `run_battery.py:637`): Discriminates between shell `128+6` signal encoding and native runner `-6` (SIGABRT) crash signatures in game engine test batteries.
5. **chousa-shokunin** (`tools/research-gate.sh:3417`; `.ufo/reports/round-63/chousa.md:90-91`): Separates pipeline stages to prevent pipefail masking and captures pipeline stage exit status via `PIPESTATUS`.

**Map Synthesis:** No sibling lane owns general POSIX pipeline status propagation or exit status classification. Siblings encounter pipefail as a language hazard or execution detail within their specialized domains (OS probes, mutation runners, binary analyzers). Mado's runbook status classes (`ok`, `exact`, `signal`) remain strictly within mado's desktop observation and pipeline propagation surface.

---

## 3. Cross-Lane Overlap Scan: Declaration Identity & Namespace Uniqueness

A comprehensive search was performed across all sibling lanes for `layer-shell`, `set_namespace`, and `namespace`:

### (a) `layer-shell` and `set_namespace` Outside Mado
- **Result:** Exactly **zero** occurrences exist in any sibling lane's `SKILL.md`, `PROVINCE.md`, `tools/`, or `corpus/`.
- Across the entire fleet repository outside `/home/vgpnk/Projects/shokunin/mado-shokunin`, `layer-shell` appears solely in:
  - Fleet capability metadata: `/home/vgpnk/Projects/shokunin/MANIFEST.json:44701` (explicitly attributed to `mado r81 C1`).
  - Historical mado round reports: `/home/vgpnk/Projects/shokunin/.ufo/reports/round-{77,78,81,82,84}/mado.md` (citing `wlr-layer-shell-unstable-v1.xml` [S460, S481], `gtk-layer-shell` [S464], and Waybar `bar.cpp` [S462]).
- `set_namespace` appears nowhere in any sibling lane. Within `mado-shokunin`, it appears exclusively in pinned upstream source captures:
  - Walker application runner: `src-theme-mod.rs:289` (`win.set_namespace(Some("walker"))`).
  - Waybar source: `S462.bin:232` (`gtk_layer_set_namespace(gtk_window, ...)`).

### (b) `namespace` Usages Across Sibling Lanes
Where the term `namespace` appears in sibling lanes, it refers to wholly disparate, non-overlapping system primitives:
1. **Linux Kernel Namespaces (Containers & Isolation):**
   - `kengaku-shokunin` (`PROVINCE.md:293-318`; `SKILL.md:71,788`): Bubblewrap per-case network, PID, and IPC namespaces for sandboxing LLM evaluation graders.
   - `tsukuroi-shokunin` (`PROVINCE.md:86-96,233`; `SKILL.md:1727,3653`): Mount, user, and PID namespaces during OS service and filesystem health diagnosis.
   - `kumitate-shokunin` (`SKILL.md:620`): PID namespaces used by `cap-run.mjs` for task execution containment.
2. **Filesystem Scratch Namespaces:**
   - `tameshi-shokunin` (`SKILL.md:28`): `$HYAKU_SCRATCH` directory isolation conventions.
   - `tabi-shokunin` (`SKILL.md:109,543`): Seat-level `/tmp` directory path namespacing.
3. **XML Namespaces:**
   - `kake-shokunin` (`PROVINCE.md:337`; `SKILL.md:1155`): Sitemap protocol XML 0.9 namespace handling.
4. **Git Repository Hygiene:**
   - `souji-shokunin` (`PROVINCE.md:140-206`; `SKILL.md:381-494`): Protected working tree namespace checks (`NAMESPACE_SHA256`).
5. **Metric Identifiers:**
   - `mori-shokunin` (`SKILL.md:999`): `C1/C2/C3_SELFTEST` family metric prefixes.

**Ownership Verdict:** Mado holds **sole, unshared ownership** over Wayland layer-shell surface declaration identity, exclusive zone footprint modeling, and allocation-key uniqueness (`PROVINCE.md:415-427,442-469`; `corpus/knowledge/bar-footprint-namespace-discipline-r84.md:7-16`). No sibling lane possesses or claims this ground.

---

## 4. Runbook Status Class Caption Interpretation (Forbidden Sibling Ground)

### The Interpretation That Must NOT Be Read as Sibling Ground:

> **Forbidden Reading:** The runbook's three status classes (`ok`, `exact`, `signal`) must **NOT** be read as:
> 1. An **operating system or service health diagnosis** (retained by `tsukuroi`),
> 2. A **process-supervisor or container runner lifecycle state** (retained by `kumitate`), or
> 3. A **reusable mutation/testing verification contract** (retained by `tameshi`).

### Exact Documentary Evidence & Distinctions:
1. **Not OS Health:** In `SKILL.md:264-280`, a status of `ok` (exit 0) establishes only that the pipeline commands returned exit 0 under `set -o pipefail`. It does **not** prove that the underlying Wayland compositor is healthy, that the Waybar panel is rendering visible pixels, or that systemd units are repaired (`SKILL.md:251-254`). Conversely, an exit code of 7 or 141 in synthetic fixtures (`SKILL.md:298-299`) demonstrates shell pipeline propagation across `set -o pipefail`; it does not diagnose a host driver failure or kernel fault. OS health diagnosis belongs strictly to `tsukuroi` (`tsukuroi-shokunin/PROVINCE.md:8-14`).
2. **Not Process Supervisor Lifecycle:** In `SKILL.md:299`, the `signal` class bound to `13 → 141` records Bash's POSIX shell convention of reporting a process killed by fatal signal $N$ as $128+N$ (S489; POSIX.1-2024 §2.9.3, S488). It does **not** represent a process supervisor lifecycle event, a cgroup OOM reaper signal, or an isolation boundary termination (retained by `kumitate`'s `cap-run.mjs`, `kumitate-shokunin/SKILL.md:620`).
3. **Not General Mutation Craft:** The runbook's status class matching rules and negative samples in `quality/counters/c2-r85-status-classes.py` and `controls/c2-cases-r85.json` test the integrity of mado's documented commands, not a reusable fleet-wide testing method (retained by `tameshi-shokunin/PROVINCE.md:3-7`).

---

## 5. Bounded Proposed Move: The Runbook Semantic Status Boundary Card

### Synthesis Across Round-85 Findings

During Round 85, sibling review seats revealed three structural tensions:
1. **Critic Defect 3 & ReviewerC2 Finding:** The executable runbook table in `SKILL.md:262-300` displays a `Status class` column (`ok`, `exact`, `signal`) and a `Bound outcome` column, but the frozen counter (`quality/counters/c2-r85-status-classes.py:287-308,761-782`) extracts only the command cell from `SKILL.md` and binds it to case `argv`. The table's documented status class is not verified by the counter, creating a split authority between prose and JSON controls (`CriticClaims.md:24-26`).
2. **Critic Defect 4 & ReviewerC2 Finding:** Seven runbook rows declare `status: ok` but accept nonzero return codes via hardcoded bypasses (`c2-r85-status-classes.py:481-508`): four refusal fixtures accept rc=3, `producer-failure-propagated` accepts rc=7, `hypridle-is-active` accepts rc=3, and `pgrep-waybar` accepts rc=1 (`CriticClaims.md:27-29`; `ReviewerC2.md:50-53`).
3. **Cross-Lane Overlap Risk:** Unqualified status class labels (`ok`, `exact`, `signal`) risk being misread as OS diagnostic verdicts (`tsukuroi`) or live daemon state proofs.

### The Proposed Move

Attach an authoritative **Semantic Status Boundary Card** to the runbook caption in `SKILL.md:250-261` (and cite it in the Round 85 C2 knowledge entry `corpus/knowledge/runbook-status-classes-r85.md`), establishing a precise two-tier taxonomy:

```markdown
> ### Runbook Status-Class Semantic Boundary Card
>
> 1. **Shell Pipeline Propagation Scope:**
>    The runbook's status classes (`ok`, `exact`, `signal`) measure POSIX shell pipeline exit propagation under `set -o pipefail`. They establish that intermediate command failures and fatal signal terminations are not masked by trailing consumers. They do NOT prove live desktop daemon health, visible pixel rendering, or unit repair (tsukuroi ground), nor runner supervisor lifecycle states (kumitate ground).
>
> 2. **Two Tiers of `ok` Rows:**
>    - **Direct Pipeline Success (rc=0):** Standard read probes where every pipeline stage completes with exit code 0.
>    - **Handled Domain Inspections (bounded nonzero exit):** The four join refusal fixtures (rc=3), `producer-failure-propagated` (rc=7), `hypridle` state queries (rc 0/3), and `pgrep waybar` queries (rc 0/1). For these rows, `status: ok` documents that the inspection executed cleanly without an unhandled shell fault or fatal signal; the command's domain-level return code and payload shape are strictly bound by the `Bound outcome` column and control matchers.
>
> 3. **Forward Counter Contract:**
>    Documented status and outcome cells are authoritative specifications. In successor counter revisions, table status cells must bind bijectively to control expectations, eliminating divergence between documentation and execution.
```

### Affected Axes
- **Operability (C2):** Directly improved. Resolves the semantic contradiction where refusal and probe rows are labeled `ok` while returning rc=3 or rc=7. Clarifies the contract of the runbook without changing any frozen command, control hash, or matcher logic.
- **Coverage (C1):** Unharmed and protected. Preserves C1's focus on layer join declaration-identity cause tokens (`claims-declaration-r85.md:13-72`) by preventing scope creep into live daemon telemetry.
- **Calibration:** Improved by explicitly acknowledging the distinction between frozen counter command-cell extraction and full table cell semantics.

### Second-Order Effects
- **Runtime:** Zero runtime impact; existing bash pipeline executions and fixture outputs remain completely unchanged.
- **Contract:** Synchronizes `SKILL.md` table documentation with `claims-declaration-r85.md:85-98` and `controls/c2-cases-r85.json`.
- **Substrate:** Maintains strict non-interference with host state; no live units or desktop processes are probed or altered.
- **Verification:** Preserves all frozen test suites and harm watch gates; eliminates reviewer confusion regarding bypass branches in `c2-r85-status-classes.py`.

### Risks and Trade-offs
- **Drift Risk:** If the card is duplicated across multiple files, wording may diverge. It must be anchored authoritatively at `SKILL.md:250-261` and referenced by pointer elsewhere.
- **Over-Claim Risk:** The card must not be cited as evidence that the *frozen* counter already enforces table status cell equality; Critic defect 3 correctly notes this as a successor requirement.
- **Non-Execution:** The card is a documentary and attribution refinement, not an executable counter repair.

### Verification for the Integrator
1. Verify that `SKILL.md:262-300` retains all 36 command rows, status classes, and outcome patterns unchanged.
2. Confirm that `c2-r85-status-classes.py` and `c1-r85-identity-causes.py` pass their self-tests and harm watch checks without regression.
3. Validate that no sibling province, fleet root file, or operator configuration is modified.

---

## 6. Retention and Cleanup

- **Observed Province Fingerprints (SHA-256):**
  - Mado (`/home/vgpnk/Projects/shokunin/mado-shokunin/PROVINCE.md`): `ac9305f82ee3a8ddc9a7aeeaceea70da0a02ae611609eafc5922c199e2f193fc`
  - Tsukuroi (`/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/PROVINCE.md`): `1239375b026d14743a606405f356284b82ae63815af92dc5c6e19c512030c5ce`
  - Tameshi (`/home/vgpnk/Projects/shokunin/tameshi-shokunin/PROVINCE.md`): `30340e182032c05e4395b2fd9aba78289d98ac816a829fb02f61ef1331cfff9c`
  - Kumitate (`/home/vgpnk/Projects/shokunin/kumitate-shokunin/PROVINCE.md`): `d05fc164cdf6aee22b0522799069f249b517b563a070120aacc8d5bf826d7219`
- **Scratch Cleanup:** Scratch directory `/fast/scratch/hyaku/mado-r85/R85ConnSiblings` was purged of temporary artifacts and removed.
- **Verification:** All checks conducted read-only; no unrun checks claimed.

Report: .ufo/waves/round-85/w1/R85ConnSiblings.md
