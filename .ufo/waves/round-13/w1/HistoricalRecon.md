# Mado Round 13 — HistoricalReconnaissance (Scout Report)

**Seat:** `MadoR13.HistoricalRecon` (scout, leaf member)  
**Date:** 2026-10-20  
**Target Repository:** `/home/vgpnk/Projects/shokunin/mado-shokunin`  
**Base Revision:** `7dcb785b7b943d03703181b218d7860a7b43007b` (HEAD at round-13 start)  
**Axes:** Coverage (C1) and Operability (C2)  
**Milestone:** Exact-set census and sourced U4 boundaries  
**Lane Constraints:** Leaf member; strictly read-only on repo code and host configs; no delegation, no background jobs, no tests/build/lint/formatting execution; write findings only to assigned round-13 wave artifacts.

---

## 1. Executive Summary & Named Axes

Per the Godspeed directive and UFO-FSD scout contract:
- **Named Axes:**
  1. **Coverage (C1):** Sourced current-art ground expansion from U1–U3 ($3/7 \to 4.2857$) to U1–U4 ($4/7 \to 5.7143$), admitting an evidenced U4 entry that rigorously separates upstream protocol phases from compositor-advertised globals and unexercised behaviors.
  2. **Operability (C2):** Replacement of the set-blind Hyprland include graph and local `*.conf` inventory checks with an exact expected/observed set comparison that explicitly names missing and extra set members across four negative isolated scenarios, backed by hermetic fixture suites and a re-cut mutation regression target.

This scout investigation comprehensively audited the Round 12 verifier records, post-review adjudications, lesson catalogs, and registry contracts to identify every owed correction, cleanly bifurcating **mandatory fixes now (Round 13 implementation scope)** from **remaining unknowns and external debts (strictly bounded non-backlog)**.

---

## 2. Evidence Base & Re-opened Absolute Paths

All evidence was collected from committed or durable records under absolute paths:

### 2.1 Round 12 Lessons, Notes, & In-Lane Verifier Records
- `/home/vgpnk/Projects/shokunin/mado-shokunin/corpus/lessons/round-12.md` (Mines M1–M14, M01–M07 inference traps, R12-a–d in-round defects, S001–S039 Gate quotes, and post-review S030 rejection).
- `/home/vgpnk/Projects/shokunin/mado-shokunin/corpus/lessons/round-12-verifier-spotcheck.md` (Integrator/orchestrator outside spotcheck and adjudication at `8dbfc93cb` / `e3e6a8e`).
- `/home/vgpnk/Projects/shokunin/mado-shokunin/corpus/QUALITY.md` (Criteria 1–16, including round-12 additions 6–16 and post-integration provenance notes on criteria 15–16 and 8).
- `/home/vgpnk/Projects/shokunin/mado-shokunin/corpus/SOURCES.md` (39 rows, §Paths, §Search log, search log errata lines 88–93, and owed anchor tracking).
- `/home/vgpnk/Projects/shokunin/mado-shokunin/corpus/knowledge/config-drift-r12.md` (Drift re-anchor for `gkeep.conf` and open L0 condition).
- `/home/vgpnk/Projects/shokunin/mado-shokunin/corpus/knowledge/window-rule-effects-getprop.md` (U1 bounded effect-read and rule attribution limits).
- `/home/vgpnk/Projects/shokunin/mado-shokunin/tools/mado-verify.sh` (Lines 2193–2275: `EXPECT` source array, `LOCAL` 12-conf array, set-blind comparison logic, and Scenario B selftest fixture).
- `/home/vgpnk/Projects/shokunin/mado-shokunin/SCORECARD.md` (Round 12 results :276–314, planned round 13 items :315–324, and round 13 declared claims :329–353).
- `/home/vgpnk/Projects/shokunin/mado-shokunin/LOG.md` (Round 12 entry :656–761, post-integration fixes, and recovery of misplaced fleet-root log entry).
- `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/evidence/round-12/l2-reviewer.md` (Pre-registration review findings F1–F14).
- `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/evidence/round-12/l2-critic.md` (C1–C3 critique and operability harm watch).
- `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/evidence/round-12/l2-postreviewer.md` (Post-integration verification at commit `5174e15`).
- `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/evidence/round-12/l2-postcritic.md` (Post-integration critique at commit `5174e15`).
- `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/evidence/round-12/after.txt` (Durable measurement outputs at commit `6e3b75f`).

### 2.2 Outside-Lane / Fleet-Level Verification Reports
- `/home/vgpnk/Projects/shokunin/.ufo/waves/kaika-w3/mado-review.md` (Orchestrator non-author review by `W3ReviewMado` at commit `aeb33b5`, detailing blocking defect B1, medium defects M1–M2, and low/info findings).
- `/home/vgpnk/Projects/shokunin/.ufo/waves/kaika-w3/mado-critic.md` (Outside critic counterexamples on C1 criterion counting, C2 gkeep conditionality, C3 search-log exclusion accounting, and cross-cutting LOG misplacement).
- `/home/vgpnk/Projects/shokunin/.ufo/waves/kaika/SOURCES-CONTRACT-v1.md` (Contract rules 1–6 and normative census commands).

---

## 3. Audit of Round 12 Verifier Findings & Triage

A rigorous review of the verifier outputs establishes the exact disposition of each recorded issue:

| ID | Issue Origin | Summary of Finding | Resolution in Round 12 | Status for Round 13 |
|---|---|---|---|---|
| **B1** | `kaika-w3/mado-review.md:145` | `sources-census.sh validate` exited 1 (E04 duplicate URL: S030 re-registered S017 URL without supersedes). | Fixed in commit `8dbfc93cb`: S030 marked `rejected` in place, `used-by` moved to S017. Lesson updated. | **Resolved** (Follow-up: preserve E04 cleanliness in all new rows). |
| **M1** | `kaika-w3/mado-review.md:146` | Queued anchors S006, S008, S009, S010 carried access date only, no version/commit/publication date. | Disclosed in `corpus/SOURCES.md:92` search log errata. Rows remained `queued`. | **Mandatory Fix when Mining** (Must supersede with commit anchor). |
| **M2** | `kaika-w3/mado-review.md:147` | Integrator notes labeled depth/adjacency "unchanged" while SCORECARD marked them "unscored". | Disclosed in `round-12-verifier-spotcheck.md:17`. | **Clarified**: Explicitly excluded from Round 13 claims (`SCORECARD.md:353`). |
| **R12-a** | `corpus/lessons/round-12.md:104` | Intermediate `LOCAL+=(gkeep)` widening had no behavioral mutant (killed only by pin R10). | Dropped before commit `5174e15`. | **Rule Enforced**: Any gate list widening in R13 requires a covering behavioral mutant. |
| **R12-b** | `corpus/lessons/round-12.md:105,109` | Gate erratum and drift note cited `omarchy-drift-watch.md:284-287` instead of `gate-standing-use.md` §5 rule 4. | Acknowledged in lesson line 109–112 as round-13 work alongside M13. | **Mandatory Fix Now** (Update gate erratum citation). |
| **R12-c** | `corpus/lessons/round-12.md:106` | `after.txt` printed commands differing from run; three counts lacked commands. | Fixed via `after-measure.sh` producing verbatim command output in `after.txt`. | **Preserved standard** (All measurement scripts must echo verbatim commands). |
| **R12-d** | `corpus/lessons/round-12.md:107` | Criteria 15–16 (external traps) filed under "Criteria from mined mistakes". | Post-integration provenance notes appended to `QUALITY.md:26-30` and lesson errata. | **Resolved** (Keep external traps distinguished from lane incidents). |
| **Critic C1** | `kaika-w3/mado-critic.md:4` | Calibration measured criterion citation count, not discernment quality. | Outside spotcheck added to `round-12-verifier-spotcheck.md` and `round-12.md:114`. | **Resolved** (Score kept strictly as citation coverage; discernment reported separately). |
| **Critic C2** | `kaika-w3/mado-critic.md:10` | Gate agreement with EXPECT does not establish operator intent to keep gkeep. | C2 recorded as conditional on operator intent (L0 dependency) in SCORECARD and report. | **Remaining External Unknown** (L0 operator intent remains external). |
| **Critic C3** | `kaika-w3/mado-critic.md:15` | Portal search exclusion count used empty `printf '%s' '' \| wc -l` printing 0. | Disclosed and corrected in `corpus/SOURCES.md:88-90` search log errata. | **Resolved**. |
| **LOG append** | `kaika-w3/mado-review.md:119` | L1 seat accidentally appended post-review text to fleet-root `LOG.md` without `cwd`. | Fleet root restored to HEAD; text recovered and appended to lane `LOG.md` in commit `aeb33b5`. | **Resolved** (Strict enforcement: all tool calls specify explicit `cwd`). |
| **M13** | `corpus/lessons/round-12.md:25` | Set-blind census: presence checks ignore extra local files; include checks ignore set deltas. | Registered as mistake M13; captured by QUALITY criterion 14; planned for Round 13. | **Mandatory Fix Now (Milestone C2)**. |

---

## 4. Mandatory Fixes Now (Round 13 Implementation Scope)

These items are actionable, lane-owned, non-negotiable obligations for Round 13 execution:

### 4.1 Mandatory Fix 1: Exact-Set Census Implementation (Mistake M13 & Axis C2)
- **Problem Statement:**  
  In `/home/vgpnk/Projects/shokunin/mado-shokunin/tools/mado-verify.sh`:
  - `hypr.local.inventory` (lines 2262–2274) iterates strictly over the 12 expected files in `declare -a LOCAL=(hyprland bindings input monitors looknfeel hypridle hyprlock hyprsunset ai-usage autostart envs xdph)` and checks `if [ -f "$H/$x.conf" ]`. If extra unmanaged files exist on disk (such as `~/.config/hypr/gkeep.conf`, which is the 13th file currently on host), the check reports `PASS "12/12 active local confs"`, completely blind to the unmanaged file.
  - `hypr.root.include_graph` (lines 2225–2239) checks `${#got[@]} -ne ${#EXPECT[@]}` and then does positional index comparison. If counts match but contents are swapped, or if counts differ, it prints generic line counts without isolating and naming the set symmetric difference ($EXPECT \setminus got$ and $got \setminus EXPECT$).
  - `hypr.root.sources_resolve` (lines 2241–2255) checks whether each $t \in EXPECT$ exists, but does not assert set equality between observed sources and expected targets.
- **Mandatory Implementation Requirements:**
  1. **Exact Set Comparison in `hypr.local.inventory`:**
     - Observe actual local files matching `$H/*.conf`.
     - Compare observed set against expected set.
     - Emit `PASS` only when $observed = expected$.
     - On discrepancy, emit `FAIL` naming exact missing members (`missing: <list>`) and exact extra members (`extra: <list>`).
  2. **Exact Set Comparison in `hypr.root.include_graph` & `hypr.root.sources_resolve`:**
     - Maintain strict sequence/order verification, but enhance reporting to isolate missing and extra include statements.
  3. **Hermetic Test Suite Coverage (`--selftest`):**
     - Retain all 269 existing assertions.
     - Add four dedicated isolated test scenarios demonstrating detection of:
       - Scenario 1: Extra local `.conf` file present.
       - Scenario 2: Same-count replacement in local inventory (1 missing + 1 extra).
       - Scenario 3: Same-count replacement in source includes (1 missing + 1 extra).
       - Scenario 4: Missing expected `gkeep.conf` include.
     - Each scenario must assert stable row IDs, `FAIL` status, and exact named tokens in detail strings.
  4. **Mutation Regression Re-cut:**
     - Because gate logic in `/home/vgpnk/Projects/shokunin/mado-shokunin/tools/mado-verify.sh` will change, re-cut `PIN_MADO` using the established harness (`/home/vgpnk/Projects/shokunin/tameshi-shokunin/tools/mutate-and-run.sh`) and verify all 10 defect mutations D1–D10 are killed.

### 4.2 Mandatory Fix 2: Gate Erratum Citation Correction (Defect R12-b)
- **Problem Statement:**  
  In `/home/vgpnk/Projects/shokunin/mado-shokunin/tools/mado-verify.sh:2193-2202` and `/home/vgpnk/Projects/shokunin/mado-shokunin/corpus/knowledge/config-drift-r12.md`:
  The erratum documenting the `EXPECT` expansion to 18 sources cites `corpus/knowledge/omarchy-drift-watch.md:284-287`. As identified by reviewer finding F1 and documented in `corpus/lessons/round-12.md:109-112`, `omarchy-drift-watch.md` governs only its own tables; it does **not** govern gate `EXPECT`. The governing authority for gate pin changes is `/home/vgpnk/Projects/shokunin/mado-shokunin/corpus/knowledge/gate-standing-use.md` §5 rule 4 ("a MOVED pin … re-verification and an appended erratum", lines 222–226).
- **Mandatory Implementation Requirements:**
  - Update the in-code erratum comment above `declare -a EXPECT` in `tools/mado-verify.sh` to explicitly cite `corpus/knowledge/gate-standing-use.md:222-226` §5 rule 4.
  - Append a clarifying erratum in `corpus/knowledge/config-drift-r12.md` citing `gate-standing-use.md` §5 rule 4.

### 4.3 Mandatory Fix 3: Owed Anchors for U4 Mining (Axis C1 & Milestone U4)
- **Problem Statement:**  
  Four queued candidate rows in `/home/vgpnk/Projects/shokunin/mado-shokunin/corpus/SOURCES.md:92` carry only an access date (`2026-10-19`) without a source-repository commit, release tag, or publication revision:
  - `S006`: `Wayland debugging extras` (`https://wayland.freedesktop.org/extras.html`)
  - `S008`: `The Wayland Protocol` high-level design (`https://wayland-book.com/introduction/high-level-design.html`)
  - `S009`: `Wayland Architecture` (`https://wayland.freedesktop.org/architecture.html`)
  - `S010`: `Wayland Explorer` (`https://wayland.app/protocols/`, discovery only)
  *Note:* `S005` (`wayland-protocols README`) already carries a pinned revision: `@ main 3dac056d (2026-01-16)`.
- **Mandatory Implementation Requirements:**
  - Under `SOURCES-CONTRACT-v1.md` Rule 2, an `anchor` cell cannot be modified in place.
  - When mining any of `S006`, `S008`, or `S009` for U4 knowledge:
    1. Append a superseding row in `/home/vgpnk/Projects/shokunin/mado-shokunin/corpus/SOURCES.md` whose `teaches` cell opens with `supersedes S0NN —` and whose `anchor` cell provides the exact commit hash, release version, or canonical document revision.
    2. Transition the target status to `mined` and record the knowledge note path in `used-by`.
    3. Ensure the newly admitted U4 knowledge note in `corpus/knowledge/` includes `covers: U4`, header trio (`source:`, `verified-at:`, `recheck:`), and cites only valid `mined` rows.

### 4.4 Mandatory Fix 4: Contract Census & Duplicate-URL Prevention
- **Problem Statement:**  
  In Round 12, the fleet validator `sources-census.sh validate` failed with `E04` because row `S030` duplicated `S017`'s URL without a `supersedes` clause. Although resolved by marking `S030` rejected in `8dbfc93cb`, the current baseline retained census (`.ufo/waves/round-13/census-before.txt`) still reports `W04 S030 duplicate url wiki.hypr.land/Configuring/Basics/Window-Rules across scopes`.
- **Mandatory Implementation Requirements:**
  - When drafting registry additions for Round 13, perform a URL-duplicate check prior to fragment merge.
  - Never introduce duplicate URLs across rows unless the new row is an explicit correction whose `teaches` cell opens with `supersedes S0NN —`.
  - Ensure the SOURCES contract census checks (columns count = 13, enum checks for tier/status/kind, no tier-inflation `A+community`, and bidirectional `mined` $\leftrightarrow$ `used-by` join) execute cleanly.

### 4.5 Mandatory Fix 5: Instrument Registration in `SKILL.md`
- **Problem Statement:**  
  `SCORECARD.md:322` and `SCORECARD.md:347` plan the formal registration of the existing verdict gate (`tools/mado-verify.sh`) at its `SKILL.md` registry home in compliance with `PROTOCOL.md` §Gate standard.
- **Mandatory Implementation Requirements:**
  - Register `tools/mado-verify.sh` in `SKILL.md` with its exit codes (0 CLEAN, 1 DIVERGED, 2 syntax/execution error), invocation modes (live, `--no-live`, `--selftest`, `--regression`), and boundary assertions.

---

## 5. Remaining Unknowns & External Debts (Bifurcated from Current Scope)

The following items are explicitly **not** generic backlog; they are documented boundaries, external dependencies, or upstream limits that cannot be converted into lane-internal code changes in Round 13:

### 5.1 Unknown 1: Operator Intent Regarding `gkeep.conf` Permanence (External L0 Dependency)
- **Anchor:** `/home/vgpnk/Projects/shokunin/mado-shokunin/corpus/knowledge/config-drift-r12.md:91`; `SCORECARD.md:287`; `kaika-w3/mado-review.md:131`; `kaika-w3/mado-critic.md:10`.
- **Boundary & Evidence:**  
  The host configuration contains `~/.config/hypr/gkeep.conf` (installer execution epoch `1792267376` = `2026-10-17T20:02:56Z`). The gate pinned it in `EXPECT` to reflect observed reality without false failure alarms. However, mado cannot self-attest whether the operator considers `gkeep` a permanent system fixture or an ephemeral local test.
- **Disposition:**  
  Freshness credit (C2) remains formally conditional on operator ratification (L0). The gate handles its presence hermetically, but its permanent standing remains an external unknown.

### 5.2 Unknown 2: Rule Attribution in Hyprland 0.56.2 (`getprop` Upstream Limit)
- **Anchor:** `/home/vgpnk/Projects/shokunin/mado-shokunin/corpus/knowledge/window-rule-effects-getprop.md`; `corpus/lessons/round-12.md:20` (M8); `l2-postreviewer.md:18`.
- **Boundary & Evidence:**  
  While `hyprctl getprop <window> <property>` successfully reads effective window properties on Hyprland 0.56.2 (e.g. `opacity 0.97`), inspect of the tagged handler `src/debug/HyprCtl.cpp:1565-1566` (`alphaToString(PWINDOW->m_ruleApplicator->alpha(), true)`) proves that Hyprland evaluates rule properties into internal applicator variables without maintaining a trace or identifier of which rule matched.
- **Disposition:**  
  Rule attribution is an upstream architectural limitation. It is documented and tagged as `[UNK]`. No lane tool can fabricate rule attribution without upstream Hyprland modifications.

### 5.3 Unknown 3: Host Availability of Wayland/Input Diagnostic Binaries
- **Anchor:** `.ufo/evidence/round-12/l2-scout.md:3,10,12`; `SCORECARD.md:320-321`.
- **Boundary & Evidence:**  
  Neither `wayland-info` nor `libinput` is installed on the host workstation. `hyprctl` does not provide an equivalent interface for dumping Wayland globals.
- **Disposition:**  
  Round 13 U4 coverage must strictly ground its claims in upstream protocol specifications and documentation (`[INF-docs]`), framing globals and phases conceptually. It must **not** assert or simulate live host tool measurement.

### 5.4 Unknown 4: Upstream Protocol Guarantees vs. Host Compositor State (Traps M01–M07)
- **Anchor:** `/home/vgpnk/Projects/shokunin/mado-shokunin/corpus/lessons/round-12.md:28-41`; `corpus/QUALITY.md:21-22` (Criteria 15–16).
- **Boundary & Evidence:**  
  Upstream staging protocols (`staging`, `experimental`, `stable`), wlroots output management interfaces, XDPH portal implementations, and HDR graphics stacks are external specifications.
- **Disposition:**  
  Per QUALITY criterion 16, upstream documentation and releases support only dated `[INF-docs]`; they must never be promoted to installed-host facts without independent live measurement.

### 5.5 Unknown 5: Bounded Rubrics for Depth and Adjacency
- **Anchor:** `SCORECARD.md:323,353`; `kaika-w3/mado-review.md:147` (M2).
- **Boundary & Evidence:**  
  No bounded, verifiable mathematical rubric currently exists for scoring depth and adjacency in mado-shokunin. In Round 12, they were marked "unscored".
- **Disposition:**  
  As explicitly declared in `SCORECARD.md:353`, depth and adjacency expansion is not claimed in Round 13. They remain unscored pending formal rubric formulation.

### 5.6 External Debt 6: Fleet-Level Ledger & Report Bindings (Mistakes M12 & M14)
- **Anchor:** `/home/vgpnk/Projects/shokunin/mado-shokunin/corpus/lessons/round-12.md:24-26`.
- **Boundary & Evidence:**  
  M12 (fleet vs lane report placement) and M14 (fleet ledger manifest verdict binding) are process conventions belonging to the fleet orchestrator/integrator.
- **Disposition:**  
  Handled at the fleet integration boundary; excluded from lane worktree edits.

---

## 6. Verification & Invariants Checklist for Main Agent

Per the leaf contract, this scout executed no builds, tests, linters, or mutations. The following checklist is provided for the main agent (L1) to execute once after all seats complete:

1. **Sources Census Validation:**
   - Execute: `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin mado`
   - Assert exit code `0` and verify no `E04` duplicate URL errors.
2. **Hermetic Self-Test:**
   - Execute: `bash tools/mado-verify.sh --selftest`
   - Assert all assertions pass ($269 + 4 = 273$ or updated target $N/N$, exit code 0).
3. **Mutation Regression Verification:**
   - Execute: `MADO_VERIFY_HARNESS=/home/vgpnk/Projects/shokunin/tameshi-shokunin/tools/mutate-and-run.sh bash tools/mado-verify.sh --regression`
   - Assert `MADO_REGRESSION: PASS` with 10/10 defect mutants killed against the re-cut `PIN_MADO`.
4. **File-Plane Verification:**
   - Execute: `bash tools/mado-verify.sh --no-live`
   - Assert 0 `FAIL`, 0 `UNKNOWN`, and clean exact set matches for `hypr.root.include_graph`, `hypr.root.sources_resolve`, and `hypr.local.inventory`.
5. **Navigation Counter Invariant:**
   - Verify `REV=HEAD bash -s` against `SCORECARD.md` navigation fence block; assert 27/27 indexed notes, exit code 0.
6. **Append-Only Contract Conformance:**
   - Verify diffs in `LOG.md`, `corpus/QUALITY.md`, `corpus/SOURCES.md`, and `corpus/lessons/` are pure insertions (`git diff -U0 ... | grep -nE '^-[^-]'` returns empty).
