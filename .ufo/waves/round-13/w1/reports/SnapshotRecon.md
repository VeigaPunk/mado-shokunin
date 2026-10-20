# SnapshotRecon Scout Report — Mado Round 13 (Wave 1)

**Seat ID:** `MadoR13.SnapshotRecon`  
**Role:** Scout (leaf member — no subagent dispatch, no background jobs, no state mutation)  
**Target:** `/home/vgpnk/Projects/shokunin/mado-shokunin`  
**Assignment:** Read gate snapshot expected formats and scope hashes; map changes needed when census detail strings change. No tests.  
**Acceptance Path:** `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-13/w1/SnapshotRecon.md`  
**Report Path:** `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-13/w1/reports/SnapshotRecon.md`  
**Status:** Complete  
**Date:** 2026-10-20  

---

## 1. Executive Summary & Core Findings

1. **Gate Snapshot Format Is Strict V1 Plain Text (`# mado-verify snapshot v1`):**
   - Implemented in `tools/mado-verify.sh:1640-2160` (enclosed within the excised `MADO-R8-BLOCK` marker pair).
   - Consists of an 8-line header (`# mado-verify snapshot v1`, `# created: ...`, `# tool: ...`, `# gate-sha256: ...`, `# root: ...`, `# scope: ...`, `# mode-line: ...`, `# counts: ...`, `# rows: ...`) followed by ordered pipe-delimited data rows: `row|<plane>|<check>|<status>|<detail>`.
   - Primary key for indexing and diffing is `plane|id` (e.g. `hypr|hypr.root.include_graph`, `hypr|hypr.local.inventory`).

2. **Scope Hashes & Scope Fields in Snapshot Machinery:**
   - **`gate-sha256`:** Full SHA-256 hash of `tools/mado-verify.sh` itself (`sha256sum "$MADO_R8_SELF"`). Recorded in the snapshot header; diffed under `DIFF_SCOPE gate-sha256: <old> → <new>` (increments `scope` counter).
   - **`boundary_hash`:** Combined SHA-256 of all config files under `$ROOT/.config` (`tools/mado-verify.sh:218-226`). Recorded as a row detail on `gate|boundary.readonly`.
   - **Scope Header Field:** Evaluates to either `live` or `file-plane`. Diffed under `DIFF_SCOPE scope: <old> → <new>` (increments `scope` counter).

3. **Impact of Census Detail String Changes on Snapshot & Diff Modes:**
   - **Status Unchanged (`PASS` → `PASS`):** Does NOT count as a row class regression or appearance. Diff classifies this as `DIFF_ROW detail <id>: <status> (detail changed)` and prints `DIFF_DETAIL <id> old:` / `new:`.
   - **Verdict Impact:** Emits `MADO_DIFF: DETAIL-CHANGED` (exit code `0`) if no other row classes or scope fields changed. If `gate-sha256` also changed (as happens across a gate edit), diff emits `MADO_DIFF: CHANGED` (exit code `1`) with `scope=1; detail-changed=...`.
   - **Critical Snapshot Invariant (One-Line Detail Rule):** Snapshot capture parses raw output line-by-line looking for `PASS|FAIL|UNKNOWN|SKIP|NOTE` in the 3rd whitespace token. **Multi-line detail strings cause immediate refusal (`MADO_SNAPSHOT: REFUSED`, exit 2)** because parsed row counts will fail to reconcile with `counts: pass=... fail=...`. Any proposed census detail string must strictly remain on a single line.

4. **Required Updates Across the Repository for C2 Census Changes:**
   - Selftest Scenario S (`tools/mado-verify.sh:1045-1157`) exercises snapshot generation and snapshot-diff between fixture A (clean) and fixture B (broken). Because Scenario S asserts row class transitions (`DIFF_ROW regressed hypr.root.orchestrator: PASS→FAIL`, etc.), updating census detail strings does not break Scenario S unless Scenario S explicitly asserts an exact census string match (none currently does; Scenario S1 asserts `hypr.root.orchestrator` detail only).
   - Knowledge base documentation and standing runbooks (`corpus/knowledge/snapshot-diff-receipt-r9.md`, `corpus/knowledge/gate-standing-use.md`) document the snapshot contract and must be preserved as historical receipts or updated with errata notes per the standing append-only rule.

---

## 2. Gate Snapshot Format Specifications

### 2.1 File Grammar & Structure

From `/home/vgpnk/Projects/shokunin/mado-shokunin/tools/mado-verify.sh:1874-1883`:

```
# mado-verify snapshot v1
# created: <ISO-8601 UTC timestamp | unavailable>
# tool: <First line of gate stdout, e.g. 'mado-verify.sh v1 (mado-shokunin round 5 / M5-2)'>
# gate-sha256: <64-hex SHA-256 of tools/mado-verify.sh>
# root: <Absolute directory path evaluated as config root>
# scope: <file-plane | live>
# mode-line: <Second line of gate stdout, e.g. 'mode: file-plane only | root: ...'>
# counts: pass=<p> fail=<f> unknown=<u> skip=<s> note=<n>
# rows: <total row count>
row|<plane>|<check>|<status>|<detail>
...
```

### 2.2 Parsing and Ingestion Rules (`mado_r8_load`, `:1903-2000`)

1. **Magic Header Line:** Line 1 MUST be verbatim `# mado-verify snapshot v1`. Missing or altered magic fails with `MADO_DIFF: SETUP (not a v1 snapshot (line 1): <file>)` (exit 2).
2. **Comment Lines:** Any line starting with `#` after line 1 is parsed for metadata keys (`created`, `tool`, `gate-sha256`, `root`, `scope`, `mode-line`, `counts`, `rows`).
3. **Data Lines:** Lines starting with `row|` are split on `|` into:
   - `tag` (`row`)
   - `plane` (e.g. `hypr`, `hypr-live`, `waybar`, `walker`, `terms`, `omarchy`, `theme`, `gate`)
   - `id` (e.g. `hypr.root.include_graph`, `hypr.local.inventory`)
   - `st` (status: `PASS`, `FAIL`, `UNKNOWN`, `SKIP`, `NOTE`)
   - `dt` (detail string: remainder of the line)
4. **Validation Invariants:**
   - Empty fields (`plane`, `id`, `st`, `dt`) yield `malformed row at line <n>`.
   - Duplicate `plane|id` yields `duplicate row <plane|id> in <file>`.
   - Sum of parsed row statuses MUST match the header `# counts:` numbers exactly.
   - Total parsed row count MUST match `# rows: <total>`.
   - Any violation aborts ingestion with `MADO_DIFF: SETUP (receipt does not reconcile...)` (exit 2).

---

## 3. Scope Hashes & Identity Fields

The snapshot mechanism explicitly tracks the execution scope and environmental state through four canonical fields:

| Field | Source / Origin | Diff Classification | Behavior on Change |
|---|---|---|---|
| `gate-sha256` | `sha256sum tools/mado-verify.sh` (`:1869-1871`) | `DIFF_SCOPE gate-sha256:` | Increments `scope` counter; exits 1 (`CHANGED`) |
| `scope` | Mode determination (`file-plane` vs `live`) (`:1790-1797`) | `DIFF_SCOPE scope:` | Increments `scope` counter; exits 1 (`CHANGED`) |
| `root` | Root argument (`--root <DIR>` or `$HOME`) (`:1798-1803`) | `DIFF_SCOPE root:` | Increments `scope` counter; exits 1 (`CHANGED`) |
| `tool` | First line of stdout (`VERSION_STR`) (`:1780-1789`) | `DIFF_SCOPE tool:` | Increments `scope` counter; exits 1 (`CHANGED`) |
| `created` | UTC ISO-8601 timestamp (`:1872-1873`) | Ignored in comparison | Provenance only; zero diff noise |
| `boundary.readonly` | Row detail containing `boundary_hash "$C"` (`:218-226`) | `DIFF_ROW detail` | Emits `detail (detail changed)`, exits 0 or 1 depending on scope |

### Key Scope Hash Nuance: Excision Invariant
The snapshot logic (`MADO-R8-BLOCK`, `:1640-2160`) and selftest scenario S (`:1045-1207`) are excised during regression target derivation (`mado_r7_target_build`, `:1377-1388`). Therefore:
- Changes to snapshot code *inside* `MADO-R8-BLOCK` do NOT invalidate `PIN_MADO`.
- Changes to census logic or detail strings *outside* the block (e.g. in `verify()`, `:2168-2274`) alter the excised target bytes and require a regression re-cut (`PIN_MADO`).

---

## 4. Impact of Census Detail String Changes

### 4.1 Relevant Hypr File Plane Rows

Under Milestone C2 (exact-set census), two existing rows in `tools/mado-verify.sh` are affected:

1. **`hypr.root.include_graph` (`:2225-2239`):**
   - *Baseline PASS detail:* `"${#got[@]}/${#EXPECT[@]} sources, order exact"` (e.g. `18/18 sources, order exact`)
   - *Baseline FAIL detail:* `"${#got[@]} source lines (expected ${#EXPECT[@]})"` or `"line $((i + 1)): got '${got[$i]}' want '${EXPECT[$i]}'"`
   - *C2 Proposed PASS detail:* `18/18 sources, set equal, order exact` (or similar exact-set indication)
   - *C2 Proposed FAIL detail:* `missing=[...] extra=[...] dup=[...]` (or `set equal (18/18); order: line N got '...' want '...'`)

2. **`hypr.local.inventory` (`:2263-2273`):**
   - *Baseline PASS detail:* `"$n/${#LOCAL[@]} active local confs"` (e.g. `12/12 active local confs` or `13/13 active local confs`)
   - *Baseline FAIL detail:* `"missing:$lmiss"`
   - *C2 Proposed PASS detail:* `13/13 active local confs, set exact`
   - *C2 Proposed FAIL detail:* `missing=[...] extra=[...]`

### 4.2 Snapshot-Diff Classification Rules (`mado_r8_diff_cli`, `:2080-2150`)

When a snapshot generated before the C2 change ($S_{\text{old}}$) is diffed against a snapshot generated after the C2 change ($S_{\text{new}}$) on a clean root:

1. **Row Identity Key:** `key="$plane|$id"`
   - Because row IDs remain unchanged (`hypr.root.include_graph` and `hypr.local.inventory`), rows are matched 1-to-1. No `appeared` or `vanished` row events are triggered.
2. **Status Comparison:** Both $S_{\text{old}}$ and $S_{\text{new}}$ report `PASS`.
   - Since $S_{\text{old}} = \text{PASS}$ and $S_{\text{new}} = \text{PASS}$, status class move functions (`mado_r8_class`: `regressed`, `recovered`, `flipped`, `relaxed`, `relabeled`) evaluate to none.
3. **Detail Comparison:** $D_{\text{old}} \neq D_{\text{new}}$:
   - Emits:
     ```
     DIFF_ROW detail hypr.root.include_graph: PASS (detail changed)
     DIFF_DETAIL hypr.root.include_graph old: 18/18 sources, order exact
     DIFF_DETAIL hypr.root.include_graph new: 18/18 sources, set equal, order exact
     DIFF_ROW detail hypr.local.inventory: PASS (detail changed)
     DIFF_DETAIL hypr.local.inventory old: 12/12 active local confs
     DIFF_DETAIL hypr.local.inventory new: 13/13 active local confs, set exact
     ```
   - Increments counter: `r_detail=$((r_detail + 1))`
4. **Scope Comparison:**
   - Gate file was edited to implement C2, so `gate-sha256` moves:
     ```
     DIFF_SCOPE gate-sha256: <old-sha> → <new-sha>
     ```
   - Increments counter: `scount=1`
5. **Final Diff Verdict & Exit Code:**
   - `class_total=$((rowcls + scount)) = 0 + 1 = 1`
   - Output line:
     ```
     MADO_DIFF: CHANGED (rows 60→60; regressed=0 recovered=0 flipped=0 relaxed=0 relabeled=0 appeared=0 vanished=0; detail-changed=2; scope=1)
     ```
   - Exit Code: **1** (exit code 1 signifies that revision scope changed; clean and expected per `gate-standing-use.md` §3).

---

## 5. Architectural Hazards & Failure Modes

### 5.1 Hazard 1: Multi-Line Detail Trap
- **Mechanism:** In `mado_r8_snapshot_cli` (`tools/mado-verify.sh:1827-1846`), the output parser processes line-by-line:
  ```bash
  while IFS= read -r line; do
    read -r f1 f2 f3 rest <<<"$line"
    case "$f3" in
      PASS | FAIL | UNKNOWN | SKIP | NOTE)
  ...
  ```
- **Consequence:** If a census detail formatted as JSON or indented list spans across newlines, lines 2+ do not have `PASS|FAIL|...` in `$f3`. They are skipped.
- **Reconciliation Failure:** At line 1847:
  ```bash
  if [ "$total" = 0 ] || [ "$rpass" != "$cpass" ] || ...; then
    printf 'MADO_SNAPSHOT: REFUSED (row parse does not reconcile...)\n'
    return 2
  fi
  ```
- **Mitigation Requirement:** Every detail string MUST be strictly single-line. Delimit multiple missing/extra elements using commas or brackets on the same line (e.g. `missing=[a.conf, b.conf] extra=[c.conf]`).

### 5.2 Hazard 2: Pipe Character (`|`) in Detail Strings
- **Mechanism:** The snapshot storage format uses pipe delimiters (`row|<plane>|<id>|<status>|<detail>`).
- During `mado_r8_load` (`:1928`):
  ```bash
  IFS='|' read -r tag plane id st dt <<<"$line"
  ```
  If `dt` contains a pipe character `|`, `read -r tag plane id st dt` will split `dt` at the first pipe and only put the remainder into `dt`.
- **Mitigation Requirement:** Detail strings MUST NOT use raw pipe characters (`|`). Use colons, semicolons, or commas (e.g. `missing=[...]; extra=[...]`).

### 5.3 Hazard 3: Selftest Scenario Ingestion Asserts
- In `tools/mado-verify.sh` selftest:
  - Scenario S1 (`:1065-1066`) explicitly tests:
    ```bash
    st_has "S1: rows are stored pipe-delimited" "$(cat "$S1")" \
      "row|hypr|hypr.root.orchestrator|PASS|0 settings lines (pure orchestrator)"
    ```
    This targets `hypr.root.orchestrator`, which is NOT modified by C2.
  - Scenario S3 (`:1078-1085`) tests:
    ```bash
    st_has "S3: the orchestrator regression is named" "$out" "DIFF_ROW regressed hypr.root.orchestrator: PASS→FAIL"
    st_has "S3: the walker regression is named" "$out" "DIFF_ROW regressed walker.config: PASS→FAIL"
    st_has "S3: a same-status detail move is classified detail" "$out" "DIFF_ROW detail hypr.file.sha_pin: NOTE (detail changed)"
    st_has "S3: the boundary-hash detail move is classified detail" "$out" "DIFF_ROW detail boundary.readonly: PASS (detail changed)"
    ```
    None of these assert the detail text of `hypr.root.include_graph` or `hypr.local.inventory`.
  - Scenario S10 (`:1160-1207`) tests crafted synthetic snapshots (`classes-a.snap` vs `classes-b.snap`) under fake plane `fix`. Completely insulated from gate census strings.

---

## 6. Required Mapping and Action Plan for C2 Implementers

To guarantee that the census changes land without breaking snapshot integrity:

1. **Detail String Formatting Contract:**
   - `hypr.root.include_graph`:
     - Clean PASS: `18/18 sources, set equal, order exact`
     - Order mismatch: `set equal (18/18); order: line <N> got '<got>' want '<want>'`
     - Set mismatch: `set: missing=[<comma-separated>] extra=[<comma-separated>] dup=[<comma-separated>]`
   - `hypr.local.inventory`:
     - Clean PASS: `13/13 active local confs, set exact`
     - Set mismatch: `set: missing=[<comma-separated>] extra=[<comma-separated>]`

2. **Snapshot Invariant Verification:**
   - Ensure neither string emits newlines or `|` characters.
   - Verify that `--snapshot <file>` captures both rows cleanly and `# rows:` equals the line count of `row|` entries.

3. **Standing Use Note & Historical Receipts:**
   - Update or errata `corpus/knowledge/gate-standing-use.md` §3 to document the updated detail signatures if live baseline snapshots are updated in subsequent rounds.
   - Note that historical receipts in `corpus/knowledge/snapshot-diff-receipt-r9.md` remain valid as historical records and MUST NOT be edited in place.

---

## 7. Tooling Record

- **Tooling Directive Compliance:**
  No tools were installed or upgraded during this scouting execution. Standard tools (`grep`, `read`, coreutils) were sufficient.
