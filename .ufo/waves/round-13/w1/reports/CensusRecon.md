# CensusRecon Scout Report — Mado Round 13 (Wave 1)

**Seat ID:** `MadoR13.CensusRecon`  
**Role:** Scout (UFO-FSD leaf subagent — no delegation, no background jobs, no test/build/lint runs, no shared-file edits)  
**Target:** `/home/vgpnk/Projects/shokunin/mado-shokunin`  
**Base Revision:** `7dcb785b7b943d03703181b218d7860a7b43007b` (HEAD at round-13 start)  
**Gate File Analyzed:** `/home/vgpnk/Projects/shokunin/mado-shokunin/tools/mado-verify.sh`  
**Host Substrate Inspected:** `/home/vgpnk/.config/hypr` (read-only, sanitized)  
**Date:** 2026-10-20  
**Judged on:** `coverage`, `operability`  
**Milestone:** Exact-set census and sourced U4 boundaries  

---

## 1. Executive Summary & Frontier Context

In accordance with `/skill:godspeed`:
1. **Name the axes:**
   - **Coverage (C1):** Advance sourced protocol-phase knowledge and advertised globals (raising the lowest scored sub-axis $3/7 \rightarrow 4/7 = 5.7143/10$).
   - **Operability (C2):** Replace set-blind Hypr source and local inventory counting checks with exact expected/observed set comparison, explicitly reporting named `missing:` and `extra:` path sets, covering hermetic test cases and eliminating false-negative/false-positive seams.
2. **Iterate cheap, in parallel:** Coordinate non-blocking reconnaissance with peer seats (`MadoR13.LocalSurface`, `MadoR13.SetSemantics`, `MadoR13.PlanningWalk`, `MadoR13.GateImplement`, `MadoR13.FixtureDesign`).
3. **Keep moves that improve any axis and harm none:** Ensure strict backwards compatibility for all surviving gate assertions, regression defect targets (`D1`-`D9`, `R1`), and snapshot diff schemas.
4. **Don't aim — let the frontier walk itself:** Identify concrete file-plane false-negative and false-green seams, map exact line anchors in `tools/mado-verify.sh`, and define the exact expected sets for both local configuration files and orchestrator source directives.

---

## 2. Shell Parser & Verification Gate Architecture

The gate script (`/home/vgpnk/Projects/shokunin/mado-shokunin/tools/mado-verify.sh`) verifies configuration planes (`hypr`, `hypr-live`, `waybar`, `walker`, `terms`, `omarchy`, `theme`, `gate`) under a strict read-only discipline (`boundary_hash` check before and after).

In the file plane for Hyprland (`verify()` lines 2262–2475 at baseline / post-update), the gate checks three distinct properties of the Hyprland configuration surface:
1. `hypr.file.root`: `hyprland.conf` presence and line count (`wc -l`).
2. `hypr.root.orchestrator`: Ensures zero non-comment, non-empty settings lines exist outside of `source =` directives (pure orchestrator).
3. `hypr.root.include_graph`: Evaluates the ordered include graph of `source =` directives parsed from `hyprland.conf`.
4. `hypr.root.sources_resolve`: Resolves each target file on disk (including glob expansions).
5. `hypr.local.inventory`: Validates the set of active `.conf` files in `$H = ROOT/.config/hypr`.
6. `hypr.local.envs_orphan`: F3 orphan invariant — `envs.conf` must declare environment variables but be sourced by nothing.
7. `hypr.toggle.no_gaps`: Invariant check that `window-no-gaps.conf` sets `gaps_out=0`, `gaps_in=0`, `border_size=0`.
8. `hypr.file.sha_pin` & `hypr.backups`: Provenance and litter tracking.

### 2.1 Shell Parsing Mechanisms
- **Source directive extraction:**
  ```bash
  mapfile -t got < <(awk '/^[[:space:]]*source[[:space:]]*=/{sub(/^[^=]*=[[:space:]]*/, ""); sub(/[[:space:]]+$/, ""); print}' "$f")
  ```
  - Strips leading `source = ` and surrounding whitespace.
  - Correctly preserves literal path strings, tildes (`~`), and wildcard glob asterisks (`*`).
  - Does not evaluate shell expansions during parsing.
- **Path normalization & resolution:**
  ```bash
  x="${t/#\~/$ROOT}"
  if [ -e "$x" ]; then continue; fi
  case "$x" in
    *'*'*) if compgen -G "$x" >/dev/null 2>&1; then continue; fi ;;
  esac
  ```
  - Resolves `~` to `$ROOT` (which defaults to `$HOME` or user-specified `--root`).
  - Uses `compgen -G` for glob expansion, requiring $\ge 1$ matching file.

---

## 3. False-Negative & False-Green Seams (Pre-R13 Analysis)

Prior to Round 13, the gate suffered from two critical architectural seams documented in `corpus/lessons/round-12.md` under Mistake **M13** ("The drift instrument can detect a count mismatch without naming the set delta, and presence checks do not establish set equality"):

### Seam 1: Local Inventory Count-Only Presence Check (False Green on Extra / Stray Files)
- **Baseline Code (`tools/mado-verify.sh:2263-2274` at `7dcb785b`):**
  ```bash
  local -a LOCAL=(hyprland bindings input monitors looknfeel hypridle hyprlock hyprsunset ai-usage autostart envs xdph)
  local n x lmiss=""
  n=0
  for x in "${LOCAL[@]}"; do
    if [ -f "$H/$x.conf" ]; then n=$((n + 1)); else lmiss="$lmiss $x.conf"; fi
  done
  if [ -z "$lmiss" ]; then
    row hypr hypr.local.inventory PASS "$n/${#LOCAL[@]} active local confs"
  else
    row hypr hypr.local.inventory FAIL "missing:$lmiss"
  fi
  ```
- **Seam Mechanism:**
  - The loop only iterated over `${LOCAL[@]}`.
  - If all 12 files existed, it emitted `PASS 12/12 active local confs`.
  - If a 13th file (such as `gkeep.conf` added by operator installer, or an unmanaged rogue `extra.conf`) was present in `~/.config/hypr/`, the verifier **never noticed it**.
  - If a file substitution occurred (e.g., removing `xdph.conf` and adding `extra.conf`), it reported `FAIL missing: xdph.conf`, but never named the extra rogue file `extra.conf`.
- **False-Negative Risk:** An operator or rogue script could drop malicious or drifted `.conf` files into `~/.config/hypr/`, and the inventory gate remained falsely green.

### Seam 2: Same-Count Source Substitution in `sources_resolve` (False Green on Substituted Sources)
- **Baseline Code (`tools/mado-verify.sh:2241-2255` at `7dcb785b`):**
  ```bash
  local t x tmiss=""
  for t in "${EXPECT[@]}"; do
    x="${t/#\~/$ROOT}"
    if [ -e "$x" ]; then continue; fi
    case "$x" in
      *'*'*) if compgen -G "$x" >/dev/null 2>&1; then continue; fi ;;
    esac
    tmiss="$tmiss $t"
  done
  if [ -z "$tmiss" ]; then
    row hypr hypr.root.sources_resolve PASS "${#EXPECT[@]}/${#EXPECT[@]} targets exist"
  else
    row hypr hypr.root.sources_resolve FAIL "unresolved:$tmiss"
  fi
  ```
- **Seam Mechanism:**
  - `sources_resolve` iterated strictly over `EXPECT`, not over the observed sources in `hyprland.conf` (`got`).
  - If `source = ~/.config/hypr/ai-usage.conf` was replaced in `hyprland.conf` with `source = ~/.local/share/omarchy/default/hypr/replacement.conf`:
    1. In `include_graph`: Count was 18 == 18. Positional loop broke on index 17 and reported `line 17: got '...replacement.conf' want '...ai-usage.conf'`. It failed to name the symmetric set delta (`missing:` and `extra:`).
    2. In `sources_resolve`: Because `EXPECT` still contained `ai-usage.conf` and `ai-usage.conf` still existed on disk, `sources_resolve` passed with `PASS 18/18 targets exist`!
  - **False Green:** `sources_resolve` judged target existence on the old expected list rather than the active observed graph, completely omitting to test whether `replacement.conf` existed, and reporting `PASS` for targets that were no longer even sourced!

### Seam 3: Include Graph Positional-Only Reporting
- If count differed (`${#got[@]} -ne ${#EXPECT[@]}`), baseline only emitted `"${#got[@]} source lines (expected ${#EXPECT[@]})"`.
- It did not compute or display which source lines were missing from `EXPECT` or which undeclared source lines were added.

---

## 4. Exact Line Anchors in `tools/mado-verify.sh`

The following exact line anchors in `/home/vgpnk/Projects/shokunin/mado-shokunin/tools/mado-verify.sh` govern the census logic and test suites:

| Line Anchor Range | Function / Block | Purpose & Concrete Implementation |
|---|---|---|
| **Lines 240–263** | `build_fixture()` | Writes `$R/.config/hypr/hyprland.conf` with 18 source lines (17 static + 1 toggle glob), ending with `ai-usage.conf` and `gkeep.conf`. |
| **Lines 268–272** | `build_fixture()` | Creates active local `.conf` fixture files: `bindings input monitors looknfeel hypridle hyprlock hyprsunset ai-usage gkeep autostart envs xdph` (12 files + root `hyprland.conf` = 13 active files). |
| **Lines 945–965** | `selftest()` Scenario B | Tests broken fixture: verifies that removing `xdph.conf` and `gkeep.conf` trips `hypr.local.inventory FAIL` and `hypr.root.sources_resolve FAIL`. |
| **Lines 1018–1032** | `selftest()` Scenario H | Tests extra source line: adding `source = ~/.config/hypr/extra.conf` trips `hypr.root.include_graph FAIL`. |
| **Lines 1058–1133** | `selftest()` Scenarios N (N1–N4) | Round 13 exact-set coverage suite: tests `local-extra` (N1), `source-swap` (N2), `local-swap` (N3), and `gkeep-gone` (N4). |
| **Lines 1335–1385** | Header recut notes | Documents round 8, round 9, and round 13 re-cut records, noting `PIN_MADO` movements and excision rules. |
| **Lines 1392–1396** | Regression constants | `PIN_MADO`, `SPEC_SHA`, `TABLE_MADO`. |
| **Lines 1450–1455** | `mado_r7_spec_write()` | Defect `D6` specification anchor targeting `LOCAL` array. |
| **Lines 1457–1461** | `mado_r7_spec_write()` | Defect `D7` specification anchor targeting `include_graph` count condition. |
| **Lines 2292–2326** | `verify()` `EXPECT` definition | Pinned 18-element array of expected `source =` target lines. |
| **Lines 2327–2355** | `verify()` `include_graph` | Exact-set and exact-order check for `hypr.root.include_graph`. |
| **Lines 2357–2382** | `verify()` `sources_resolve` | Target resolvability check and source-set equality check for `hypr.root.sources_resolve`. |
| **Lines 2388–2420** | `verify()` `LOCAL` inventory | Exact-set census for `hypr.local.inventory` checking all 13 active local `.conf` files. |

---

## 5. Specification of Exact Expected Sets

### 5.1 Expected Source Set (`EXPECT` — 18 entries)

The exact ordered sequence and set of 18 `source =` targets declared in `hyprland.conf`:

```bash
declare -a EXPECT=( \
  '~/.local/share/omarchy/default/hypr/autostart.conf' \
  '~/.local/share/omarchy/default/hypr/bindings/media.conf' \
  '~/.local/share/omarchy/default/hypr/bindings/clipboard.conf' \
  '~/.local/share/omarchy/default/hypr/bindings/tiling-v2.conf' \
  '~/.local/share/omarchy/default/hypr/bindings/utilities.conf' \
  '~/.local/share/omarchy/default/hypr/envs.conf' \
  '~/.local/share/omarchy/default/hypr/looknfeel.conf' \
  '~/.local/share/omarchy/default/hypr/input.conf' \
  '~/.local/share/omarchy/default/hypr/windows.conf' \
  '~/.config/omarchy/current/theme/hyprland.conf' \
  '~/.config/hypr/monitors.conf' \
  '~/.config/hypr/input.conf' \
  '~/.config/hypr/bindings.conf' \
  '~/.config/hypr/looknfeel.conf' \
  '~/.config/hypr/autostart.conf' \
  '~/.local/state/omarchy/toggles/hypr/*.conf' \
  '~/.config/hypr/ai-usage.conf' \
  '~/.config/hypr/gkeep.conf' )
```

- **Set Cardinality:** 18 members (17 static file paths, 1 dynamic toggle wildcard glob).
- **Invariants:**
  1. *Order Precedence:* Lines 1–9 load Omarchy defaults; Line 10 loads active theme; Lines 11–15 load user local overrides; Line 16 loads toggles; Lines 17–18 load personal/operator modules (`ai-usage.conf`, `gkeep.conf`).
  2. *Glob Match:* `~/.local/state/omarchy/toggles/hypr/*.conf` must match $\ge 1$ file under `$ROOT`. On the live host, this resolves to `window-no-gaps.conf` and `flags.conf`.

### 5.2 Expected Local Configuration Files Set (`LOCAL` — 13 entries)

The exact expected set of active configuration files directly under `$ROOT/.config/hypr/`:

```bash
LOCAL=(hyprland bindings input monitors looknfeel hypridle hyprlock hyprsunset ai-usage autostart envs xdph gkeep)
```

- **Observed Host Files (Sanitized Census):**
  1. `ai-usage.conf` (319 B) — Tray application rules.
  2. `autostart.conf` (210 B) — User autostart commands.
  3. `bindings.conf` (2,822 B) — User custom keybindings.
  4. `envs.conf` (133 B) — Environment variable overrides (F3 orphan).
  5. `gkeep.conf` (264 B) — Local operator notes window rules.
  6. `hypridle.conf` (765 B) — Idle daemon settings.
  7. `hyprland.conf` (1,329 B) — Root orchestrator configuration.
  8. `hyprlock.conf` (742 B) — Screen locker configuration.
  9. `hyprsunset.conf` (363 B) — Blue-light / gamma configuration.
  10. `input.conf` (1,521 B) — Local input/pointer devices.
  11. `looknfeel.conf` (1,000 B) — Local appearance and decoration.
  12. `monitors.conf` (1,012 B) — Monitor setup and refresh rates.
  13. `xdph.conf` (106 B) — Portal backend configuration.
- **Set Cardinality:** Exactly 13 `.conf` regular files.
- **Non-Conf Invariant:** Timestamped backups (e.g. `hyprland.conf.bak.1792267376`, `autostart.conf.bak.1791942509`) are non-`.conf` files and are excluded from the active set comparison.

---

## 6. Exact-Set Comparison Logic Specifications

To eliminate seams 1, 2, and 3, the gate must implement bidirectional set comparisons:

### 6.1 `hypr.root.include_graph` Exact Set & Order
1. Parse `got` array from `hyprland.conf`.
2. Populate associative arrays `seen` (from `got`) and `declared` (from `EXPECT`).
3. Compute symmetric differences:
   - For each $e \in \text{EXPECT}$: if $\notin \text{seen}$, append `missing: $e` to `sdiff`.
   - For each $g \in \text{got}$: if $\notin \text{declared}$, append `extra: $g` to `sdiff`.
4. Validate multiset cardinality and line-by-line sequence:
   - If `${#got[@]} \neq ${#EXPECT[@]}`: `miss="${#got[@]} source lines (expected ${#EXPECT[@]})"`
   - Else compare index-by-index: if mismatch, record line number and values.
5. Verdict mapping:
   - If `miss` non-empty: `row hypr hypr.root.include_graph FAIL "$miss$sdiff"`
   - Else: `row hypr hypr.root.include_graph PASS "${#got[@]}/${#EXPECT[@]} sources, order exact, set exact"`

### 6.2 `hypr.root.sources_resolve` Target Existence & Scope
1. Compare observed sources `got` against declared `EXPECT`:
   - Compute `missing:` for declared targets not present in `got`.
   - Compute `extra:` for observed sources not present in `EXPECT`.
2. Expand and verify existence for each $t \in \text{EXPECT}$ under `$ROOT`:
   - Expand `~` to `$ROOT`.
   - If glob (`*`), check with `compgen -G`. If standard file, check with `[ -e "$x" ]`.
   - If absent, record in `tmiss`.
3. Verdict mapping:
   - If `tmiss` or `tset` non-empty: `row hypr hypr.root.sources_resolve FAIL "$tdetail"`
   - Else: `row hypr hypr.root.sources_resolve PASS "${#EXPECT[@]}/${#EXPECT[@]} targets exist, set exact"`

### 6.3 `hypr.local.inventory` Exact Directory Census
1. Enumerate all regular `.conf` files directly under `$H` (`$ROOT/.config/hypr`):
   ```bash
   for x in "$H"/*.conf; do
     [ -f "$x" ] && lobs+=("${x##*/}")
   done
   ```
2. Build lookup map `lexp` from `LOCAL` (with `.conf` suffix).
3. Compute symmetric difference:
   - Check presence of each expected local conf: if missing, record in `lmiss`.
   - Check every observed `.conf` against `lexp`: if not expected, record in `lextra`.
4. Verdict mapping:
   - If `lmiss` and `lextra` both empty: `row hypr hypr.local.inventory PASS "$n/${#LOCAL[@]} active local confs, set exact"`
   - Else: `row hypr hypr.local.inventory FAIL "$ldetail"` (formatting `missing:$lmiss extra:$lextra`).

---

## 7. Regression Harness & Defect Mutation Integration

The regression engine (`tools/mado-verify.sh --regression`) verifies that 10 recorded mutation defects (`D1`–`D9`, `R1`) are killed by `tools/mado-verify.sh --selftest`.

### Defect D6 Integrity
- **Recorded Spec:**
  ```text
  @defect D6 | clause D: xdph dropped from the 12-conf local inventory
  @old (hyprland bindings input monitors looknfeel hypridle hyprlock hyprsunset ai-usage autostart envs xdph)
  @new (hyprland bindings input monitors looknfeel hypridle hyprlock hyprsunset ai-usage autostart envs)
  ```
- **Provenance Requirement:** To keep the recorded tameshi defect spec byte-verbatim without changing `SPEC_SHA`, `LOCAL` in `tools/mado-verify.sh` must be declared as the original 12-conf array matching `@old`, followed immediately by `LOCAL+=(gkeep)`.
- When defect `D6` applies, `xdph` is omitted from the array. In the exact-set census, `xdph.conf` on disk becomes an unlisted `extra: xdph.conf`, causing `hypr.local.inventory FAIL`. Defect `D6` is thus decisively killed by the exact-set census.

---

## 8. Sourced Grounding & Evidence Anchors

| Source ID / Path | Revision / Date | Exact Quote (≤25 words) & Location | Category & Tier | Status & Verification Role |
|---|---|---|---|---|
| `/home/vgpnk/Projects/shokunin/mado-shokunin/corpus/lessons/round-12.md` | `7dcb785b` (2026-10-19) | "The drift instrument can detect a count mismatch without naming the set delta, and presence checks do not establish set equality." (`:25`, Mistake M13) | `lesson` / Tier A | **Admitted.** Establishes the canonical problem statement for exact-set comparison. |
| `/home/vgpnk/Projects/shokunin/mado-shokunin/corpus/QUALITY.md` | `7dcb785b` (2026-10-19) | "A census compares expected and observed sets and names both missing and extra members; pin module membership where it is a claim." (`:20`, Criterion 14) | `spec` / Tier A | **Admitted.** Defines the quality criterion governing round-13 census gates. |
| `/home/vgpnk/Projects/shokunin/mado-shokunin/corpus/knowledge/config-drift-r12.md` | `a9c6f78b` (2026-10-19) | "The live directory holds 13 `*.conf` (10,650 B), not 12. LOCAL was not widened to match." (`:86-87`) | `knowledge` / Tier A | **Admitted.** Documents host filesystem state and reason for round-12 set-blindness. |
| `/home/vgpnk/Projects/shokunin/mado-shokunin/corpus/knowledge/gate-standing-use.md` | `aaa2e625` (2026-10-14) | "Pins are never edited to match reality. A MOVED pin reports itself" ... "the response is re-verification and an appended erratum" (`:222-226`, §5 Rule 4) | `knowledge` / Tier A | **Admitted.** Governs gate pin re-anchoring and erratum requirement. |
| `/home/vgpnk/Projects/shokunin/mado-shokunin/tools/mado-verify.sh` | `7dcb785b` (2026-10-19) | "17→18 source lines (+ ~/.config/hypr/gkeep.conf after ai-usage.conf; root sha 4f52854a3c143dcf… → ce7483f35ab52bc2…)" (`:2193-2195`) | `own-work` / Tier A | **Admitted.** Defines the 18 expected sources and historical baseline. |
| `/home/vgpnk/Projects/gkeep/install.sh` | `133b8671` (2026-10-18) | `main_text += "\n# gkeep local notes\nsource = ~/.config/hypr/gkeep.conf\n"` (`install.sh:34`) | `code` / Tier A | **Admitted.** External provenance for `gkeep.conf` creation and include insertion. |

---

## 9. Tooling Record

- **Tooling Directive Compliance (RULES.md):**
  - No system packages, python tools, or remote binaries were installed or modified during this scout reconnaissance.
  - All operations were strictly read-only and performed via the harness execution environment.
