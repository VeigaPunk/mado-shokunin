# GateRecon — Source Target Resolver, Directory False-Greens, Symlink Semantics, and Parser Boundary

**Seat:** `MadoR14.GateRecon` (UFO-FSD scout; leaf member — no subagent dispatch).  
**Target:** `/home/vgpnk/Projects/shokunin/mado-shokunin/tools/mado-verify.sh`  
**Axes:** coverage, operability.  
**Milestone:** U5 boundaries and regular-source targets.  
**Baseline commit:** `873ff081b2ac363df771261b0ed950cba50d8988` (blob `656f1918ad5d124dd0de5beb1b5b53ea495a5bf4`).  
**Worktree state:** In-flight edit by `GateImplement` landing regular-file resolver predicates and selftest scenarios N9–N12.

---

## 1. Executive Summary

This reconnaissance maps the baseline source target resolver in `tools/mado-verify.sh`, documents the exact mechanisms of direct and glob directory false-greens, establishes symlink dereferencing semantics, and defines the parser boundary with exact line anchors comparing baseline bytes (`HEAD`) against the landed worktree diff.

Key findings:
1. **Direct directory false-green:** Baseline line `2420` used `[ -e "$x" ]`, which evaluates to TRUE for directories. A directory substituted for any declared source passed target resolution without detection.
2. **All-directory glob false-green:** Baseline lines `2421–2423` used `compgen -G "$x"`, which evaluates to TRUE if pathname expansion yields $\ge 1$ entry of *any* file type. A glob matching only subdirectories passed resolution without detection.
3. **Mixed regular/directory glob false-green:** Baseline `compgen -G "$x"` returned on the presence of any expansion; any directory-shaped file alongside a regular `*.conf` file was ignored.
4. **Cross-plane inconsistency:** In baseline `tools/mado-verify.sh`, `hypr.local.inventory` (lines `2459–2460`, `2466`) strictly enforced `[ -f "$x" ]` documenting that "directories are not loadable confs", whereas `hypr.root.sources_resolve` (line `2420`) used `[ -e "$x" ]`.
5. **Symlink policy:** POSIX `[ -f "$x" ]` follows symlinks. A symlink pointing to a regular file is accepted. A symlink pointing to a directory evaluates to FALSE under `[ -f ]` and TRUE under `[ -e ]`, triggering `non-regular:` refusal. A dangling symlink evaluates to FALSE under both, keeping the existing `unresolved:` diagnostic.
6. **Parser boundary:** The gate enforces a line-oriented orchestrator contract on `~/.config/hypr/hyprland.conf`: `# hyprlang` directives fail `hypr.root.orchestrator` (conditional semantics unmodeled); non-comment/non-source lines fail `hypr.root.orchestrator`; source lines are extracted via `awk` stripping up to `=` and trailing whitespace. Source ordering is owned by `hypr.root.include_graph`; target type and resolution are owned by `hypr.root.sources_resolve`.

---

## 2. Line Anchor Comparison Matrix

| Component | Baseline (`HEAD:873ff08`) | Worktree (`tools/mado-verify.sh`) | Role & Semantic Invariant |
|---|---|---|---|
| Display helper `src_disp()` | *Absent* | Lines `222–229` | Replaces `$ROOT` prefix with `~` using `%q` escaping for stable diagnostic token reporting. |
| Pure orchestrator check | Lines `2321–2332` | Lines `2429–2440` | Rejects `# hyprlang` conditionals (`hyprd`) and non-source active lines (`off`). |
| Pinned `EXPECT` array | Lines `2351–2370` | Lines `2460–2478` | Pinned 18-element source list; includes 1 glob (`~/.local/state/omarchy/toggles/hypr/*.conf`). |
| Source extraction `awk` | Line `2372` | Line `2480` | `awk '/^[[:space:]]*source[[:space:]]*=/{sub(/^[^=]*=[[:space:]]*/, ""); sub(/[[:space:]]+$/, ""); print}'`. |
| Inclusion order & set check | Lines `2374–2402` | Lines `2482–2510` | Computes `missing:` / `extra:` set deltas; positional sequence walk owns `hypr.root.include_graph`. |
| Target resolver: direct test | Line `2420` (`[ -e "$x" ]`) | Lines `2553–2557` (`[ -f "$x" ]` / `[ -e "$x" ]`) | Baseline accepted directories (`-e`); worktree tests regular file (`-f`), routing directories to `tnr`. |
| Target resolver: glob test | Lines `2421–2423` (`compgen -G`) | Lines `2537–2552` (`mapfile -t gmatch`) | Baseline accepted any match; worktree tests every match with `[ -f ]`, routing directories to `tnr`. |
| Diagnostic tokens emitted | Lines `2433–2436` | Lines `2570–2575` | Baseline: `unresolved:` and `extra:`. Worktree adds `non-regular:` token for extant non-regular paths. |
| Local conf inventory | Lines `2444–2487` | Lines `2582–2625` | Exact 13-member set check using `[ -f ]`; ignores directories under `$H/*.conf`. |
| Selftest: N1–N4, N7–N8 | Lines `1056–1169` | Lines `1056–1180` | Pre-existing hermetic exact-set, missing gkeep, empty source, and hyprlang conditional fixtures. |
| Selftest: N9 (direct dir) | *Absent* | Lines `1190–1207` | Replaces `windows.conf` with directory; asserts `sources_resolve FAIL non-regular:`. |
| Selftest: N10 (all-dir glob) | *Absent* | Lines `1209–1229` | Replaces `window-no-gaps.conf` with directory; asserts `sources_resolve FAIL non-regular:` & `toggle NOTE`. |
| Selftest: N11 (mixed glob) | *Absent* | Lines `1231–1250` | Adds directory `dir.conf` alongside regular toggle; asserts `sources_resolve FAIL non-regular:`. |
| Selftest: N12 (source order) | *Absent* | Lines `1252–1277` | Swaps `monitors.conf` $\leftrightarrow$ `input.conf`; asserts `include_graph FAIL` and `sources_resolve PASS`. |

---

## 3. Detailed False-Green Mechanics in Baseline

### 3.1 Direct Directory False-Green
- **Baseline implementation (`tools/mado-verify.sh:2417–2420`):**
  ```bash
  case "$t" in
    '~'*) x="$ROOT${t#\~}" ;;
    *) x="$t" ;;
  esac
  if [ -e "$x" ]; then continue; fi
  ```
- **Flaw:** Under standard shell / POSIX test semantics, `[ -e "$x" ]` returns exit code 0 if `$x` exists, regardless of file type (regular file, directory, named pipe FIFO, Unix domain socket, character device, or block device).
- **False-green outcome:** If a declared direct target (such as `~/.local/share/omarchy/default/hypr/windows.conf`) is replaced with a directory named `windows.conf`, `[ -e "$x" ]` succeeds and executes `continue`. The path is not added to `tmiss`. Because `t` exists in `EXPECT` and was parsed from `hyprland.conf`, `tset` is empty. The gate outputs:
  ```text
  hypr hypr.root.sources_resolve PASS declared targets exist, member set exact
  ```
- **Isolation leak:** When a directory target is outside `~/.config/hypr/` (e.g., under `~/.local/share/omarchy/default/hypr/`), `hypr.local.inventory` does not observe it. `hypr.root.include_graph` observes the declared string unmodified. The gate emits an overall verdict of `MADO_VERIFY: CLEAN` (exit 0) on a configuration that Hyprland cannot load.

### 3.2 All-Directory Glob False-Green
- **Baseline implementation (`tools/mado-verify.sh:2421–2423`):**
  ```bash
  case "$x" in
    *'*'*) if compgen -G "$x" >/dev/null 2>&1; then continue; fi ;;
  esac
  ```
- **Flaw:** `compgen -G "$x"` runs Bash pathname expansion. If the directory contains subdirectories matching the pattern (for example, `~/.local/state/omarchy/toggles/hypr/window-no-gaps.conf/`), `compgen -G` finds at least one filesystem node and returns exit status 0.
- **False-green outcome:** The conditional branch executes `continue`. No entry is recorded in `tmiss`.
- **Collateral inspection:** Under baseline line `2512`, `hypr.toggle.no_gaps` checks:
  ```bash
  local tog="$ROOT/.local/state/omarchy/toggles/hypr/window-no-gaps.conf"
  if [ -f "$tog" ]; then ... else
    row hypr hypr.toggle.no_gaps NOTE "toggle absent — gaps fall back..."
  ```
  Because `$tog` is a directory, `[ -f "$tog" ]` is FALSE, emitting a record-level `NOTE`. NOTEs never flip the gate verdict (line `29–30`). Thus, `sources_resolve` PASSes, `toggle.no_gaps` is NOTE, and the entire gate emits `MADO_VERIFY: CLEAN` (exit 0).

### 3.3 Mixed Regular/Directory Glob False-Green
- **Flaw:** If `~/.local/state/omarchy/toggles/hypr/` contains valid regular file `window-no-gaps.conf` and an invalid directory `extra-toggle.conf/`, `compgen -G` exits 0.
- **False-green outcome:** Baseline code had no loop over glob matches; the presence of any single file masked invalid directory entries.
- **Worktree resolution (`tools/mado-verify.sh:2537–2552`):**
  Uses `mapfile -t gmatch < <(compgen -G "$x" 2>/dev/null)`. Every expanded match `m` is evaluated with `[ -f "$m" ]`. Any non-regular entry is appended to `tnr`, while dangling symlinks append to `tmiss`. Legitimate regular files continue without objection.

---

## 4. Symlink Semantics and Policy

### 4.1 Shell Primitive Behavior Matrix

| Target on Disk | `[ -L "$p" ]` | `[ -e "$p" ]` | `[ -f "$p" ]` | `[ -d "$p" ]` | Gate Status Class |
|---|:---:|:---:|:---:|:---:|---|
| Regular file | false | true | true | false | **Accepted** (regular) |
| Symlink to regular file | true | true | true | false | **Accepted** (`-f` follows symlink) |
| Directory | false | true | false | true | **Refused** (`non-regular:`) |
| Symlink to directory | true | true | false | true | **Refused** (`non-regular:`) |
| Dangling symlink | true | false | false | false | **Refused** (`unresolved:`) |
| Symlink loop ($A \to B \to A$) | true | false | false | false | **Refused** (`unresolved:`) |
| FIFO, Socket, Character/Block Dev | false | true | false | false | **Refused** (`non-regular:`) |

### 4.2 Policy Specification
1. **Dereferencing:** In accordance with the R14 specification (`spec.json:item 1`), the gate follows symlinks for file resolution. POSIX `[ -f "$x" ]` performs dereferencing natively.
2. **Directory symlinks:** A symlink resolving to a directory has `[ -f "$x" ]` evaluate to FALSE and `[ -e "$x" ]` evaluate to TRUE. It is correctly classified as `non-regular:` rather than `unresolved:`.
3. **Dangling symlinks:** If `$x` does not resolve to an extant filesystem node, `[ -e "$x" ]` evaluates to FALSE. It is classified under `unresolved:`, preserving backwards compatibility with baseline missing-target diagnostics.
4. **Read-only boundary fence:** The resolver performs filesystem stat/metadata probes only (`-f`, `-e`, `-L`, and `compgen -G`). It never opens file descriptors for write or mutation, preserving SKILL safety rule 3 and `boundary.readonly`.

---

## 5. Parser Boundary & Supported Grammar

### 5.1 Orchestrator Grammar Contract
`hyprland.conf` is evaluated strictly as an orchestrator containing include statements:
1. **Comment lines:** Matched by `^[[:space:]]*#`. Ignored unless matching `# hyprlang`.
2. **Conditional directives:** Matched by `^[[:space:]]*#[[:space:]]*hyprlang` (baseline line `2323`, worktree line `2431`). The gate immediately fails `hypr.root.orchestrator` with:
   `unsupported hyprlang directive at line N — conditional source semantics are not modelled`.
3. **Active non-source lines:** Any non-empty line not beginning with `#` or `source[[:space:]]*=` trips `grep -nEv` (baseline line `2324`, worktree line `2432`), failing `hypr.root.orchestrator`.
4. **Source statement syntax:**
   Extracted by:
   ```bash
   awk '/^[[:space:]]*source[[:space:]]*=/{sub(/^[^=]*=[[:space:]]*/, ""); sub(/[[:space:]]+$/, ""); print}'
   ```
   - Matches lines containing optional whitespace, keyword `source`, optional whitespace, and `=`.
   - Strips up to the first `=` and any subsequent leading whitespace.
   - Strips trailing whitespace.
   - Preserves intermediate whitespace (e.g., space-containing paths).
   - Does *not* unescape quotes, evaluate environment variables, or strip trailing inline comments. Any inline `#` comment on a source line would be parsed as part of the path.
   - Empty declaration `source =` extracts as `""`, failing exact-set verification as `extra: ''` (covered by fixture N7).

### 5.2 Ownership Separation: `include_graph` vs `sources_resolve`
The gate separates syntactic declaration ordering from target filesystem validity:
- **`hypr.root.include_graph`:**
  - Compares the extracted list `got` against `EXPECT` (lines `2351–2370` / `2460–2478`).
  - First verifies set equality (`missing:`, `extra:`).
  - Next performs a positional index walk (`for i in "${!EXPECT[@]}"`).
  - If identical members appear out of order (e.g. `monitors.conf` before `input.conf`), `include_graph` FAILS with `line 11: got '...' want '...'`.
  - `include_graph` does *not* probe disk files.
- **`hypr.root.sources_resolve`:**
  - Evaluates whether declared targets resolve on disk as regular files.
  - Verifies exact set equality between declared and observed sources.
  - An out-of-order declaration whose set is identical and whose targets all exist as regular files PASSes `sources_resolve` (covered by fixture N12).
  - A directory-shaped target FAILS `sources_resolve` with `non-regular: <target>`, while leaving `include_graph` PASS.

---

## 6. Fixture Isolation Analysis

| Fixture | Scenario | Target Path Modified | `sources_resolve` | `include_graph` | `local.inventory` | Collateral Rows |
|---|---|---|:---:|:---:|:---:|---|
| **N9** | Direct directory | `~/.local/share/omarchy/default/hypr/windows.conf` | **FAIL** (`non-regular:`) | PASS | PASS | None (isolated) |
| **N10** | All-directory glob | `~/.local/state/omarchy/toggles/hypr/window-no-gaps.conf` | **FAIL** (`non-regular:`) | PASS | PASS | `hypr.toggle.no_gaps NOTE` (asserted) |
| **N11** | Mixed glob | Adds `.../toggles/hypr/dir.conf/` | **FAIL** (`non-regular:`) | PASS | PASS | `hypr.toggle.no_gaps PASS` (asserted) |
| **N12** | Source order swap | Swaps lines 14 & 15 in `hyprland.conf` | PASS | **FAIL** (`line 11: ...`) | PASS | `theme.chain.hypr_include PASS` (line 13 held) |

- **Target selection in N9:** Using `windows.conf` under `omarchy/default/hypr/` ensures complete isolation. Modifying a target under `~/.config/hypr/*.conf` would inadvertently fail `hypr.local.inventory` (which checks regular `*.conf` files), and modifying `~/.config/omarchy/current/theme/hyprland.conf` would fail `theme.chain.hypr_include`.
- **Collateral status in N10:** Turning `window-no-gaps.conf` into a directory causes `[ -f "$tog" ]` at line `2512` to evaluate to FALSE, emitting `NOTE`. The fixture explicitly asserts `st_row_has "$n_out" hypr.toggle.no_gaps NOTE`.
- **Theme anchor preservation in N12:** Swapping `monitors.conf` (index 10, line 14) and `input.conf` (index 11, line 15) leaves line 13 (`~/.config/omarchy/current/theme/hyprland.conf`) intact, keeping `theme.chain.hypr_include PASS`.

---

## 7. Observed Facts, Inferences, and Unresolved Gaps

### 7.1 Observed Facts
- `tools/mado-verify.sh` at `HEAD:873ff08` lacked regular-file predicates in `sources_resolve`, relying on `[ -e "$x" ]` (line 2420) and `compgen -G "$x"` (line 2422).
- GateImplement has modified `tools/mado-verify.sh`, introducing `src_disp()` at line 222, `[ -f ]` and `compgen -G` match looping at lines 2537–2557, and fixtures N9–N12 at lines 1190–1277.
- Selftests N9, N10, N11, and N12 sit before `MADO-R8-BLOCK` (line 1279) and outside `MADO-R7-SELFTEST-BLOCK`.

### 7.2 Inferences
- [INFERENCE] Upstream Hyprland's `ConfigManager::configExists()` or parser fails or emits config errors when encountering a `source = <directory>` statement. (Inferred from standard Hyprlang behavior; unverified via live execution in this read-only round).

### 7.3 Unresolved Gaps & Next Steps (L1 Responsibility)
- Because `GateImplement` modified `tools/mado-verify.sh` outside the excised R7/R8 blocks, the derived regression target `mado-verify-hardened` has changed.
- Selftest R10 and `--regression` will report SETUP / exit 2 until the canonical planner (L1) re-cuts `PIN_MADO` and `TABLE_MADO` during final verification. GateImplement must not edit pins to force a match.

---

## 8. Source Citations & Located Quotes

1. **Gate source target resolver baseline:**  
   `file:///home/vgpnk/Projects/shokunin/mado-shokunin/tools/mado-verify.sh` @ `873ff081b2ac363df771261b0ed950cba50d8988`, line 2420:  
   > `if [ -e "$x" ]; then continue; fi`  
   *Scope/Tier:* Local implementation source. *Admit:* direct evidence of directory acceptance.

2. **Gate glob resolver baseline:**  
   `file:///home/vgpnk/Projects/shokunin/mado-shokunin/tools/mado-verify.sh` @ `873ff081b2ac363df771261b0ed950cba50d8988`, lines 2421–2422:  
   > `case "$x" in *'*'*) if compgen -G "$x" >/dev/null 2>&1; then continue; fi ;;`  
   *Scope/Tier:* Local implementation source. *Admit:* direct evidence of directory-blind glob expansion.

3. **Gate local inventory regular file invariant:**  
   `file:///home/vgpnk/Projects/shokunin/mado-shokunin/tools/mado-verify.sh` @ `873ff081b2ac363df771261b0ed950cba50d8988`, line 2445:  
   > `directories are not loadable confs and stay out of both sides of the census`  
   *Scope/Tier:* Local implementation comment/specification. *Admit:* established precedent for regular-file requirement.

4. **Gate include order authority:**  
   `file:///home/vgpnk/Projects/shokunin/mado-shokunin/tools/mado-verify.sh` @ `873ff081b2ac363df771261b0ed950cba50d8988`, line 2374:  
   > `The positional walk below stays the PASS criterion (MADO-1 §3 order).`  
   *Scope/Tier:* Local implementation comment. *Admit:* confirmation that `include_graph` owns order.

5. **Assignment directive:**  
   `file:///home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-14/w1/spec.json` @ item `GateImplement`:  
   > `use regular-file check following file symlink, preserve existing named missing/extra, order and read-only fence.`  
   *Scope/Tier:* Task specification. *Admit:* binding policy for round 14 resolution and symlink handling.

---

## 9. Tooling Record

- **Installs:** None.
- **Updates:** None.
- **Commands executed:** Read-only git diff observation (`git diff tools/mado-verify.sh`). No builds, test executions, linters, or mutations performed.
