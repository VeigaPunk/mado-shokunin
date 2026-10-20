# SetSemantics — Exact Include Order vs Source-Set Equality vs Resolved Target Existence

**Seat ID:** `MadoR13.SetSemantics`  
**Role:** Connector / UFO-FSD subagent (leaf member — no subagent dispatch, no background jobs, no tests/build/lint/formatting)  
**Target:** `/home/vgpnk/Projects/shokunin/mado-shokunin`  
**Base Revision:** `7dcb785b7b943d03703181b218d7860a7b43007b` (HEAD at round-13 start)  
**Date:** 2026-10-20  
**Status:** Complete  
**Judged on:** `coverage`, `operability`  
**Milestone:** Exact-set census and sourced U4 boundaries  

---

## 1. Executive Summary & Non-Obvious Move

### 1.1 The Tripartite Decoupling
A subtle flaw in gate design is treating "include graph", "source set", and "target existence" as interchangeable or conflated checks. When verified as a single compound test or with incomplete set semantics, subtle regressions create false greens:
1. **Expected Include Order:** An ordered sequence $S = \langle s_1, s_2, \dots, s_n \rangle$. In Hyprland, include order governs configuration precedence (later source directives overwrite earlier options, variables, and default bindings; or bind rules in sequence). Order is a sequence property ($\mathfrak{S}_n$), not a set property.
2. **Source-Set Equality:** An unordered mathematical set $O_{\text{src}} = \{ s \mid s \in \text{hyprland.conf} \}$ compared against declared set $E_{\text{src}} = \text{EXPECT}$. Set equality ($O_{\text{src}} \equiv E_{\text{src}}$) requires both $\text{Missing} = E_{\text{src}} \setminus O_{\text{src}} = \emptyset$ and $\text{Extra} = O_{\text{src}} \setminus E_{\text{src}} = \emptyset$.
3. **Resolved Target Existence:** A predicate on path resolution and filesystem state: $\forall s \in O_{\text{src}}, \operatorname{Resolves}(s, \text{ROOT}) \ge 1$.

### 1.2 The Non-Obvious Move: Decoupling Set Membership from Sequential Traversal
In baseline `tools/mado-verify.sh:2222-2255`, `hypr.root.include_graph` checked count equality, then checked index-by-index equality. If count matched, but an undeclared file replaced a declared file (e.g. `replacement.conf` replaced `ai-usage.conf`), `include_graph` reported a positional mismatch at that index (`line 17: got 'replacement.conf' want 'ai-usage.conf'`), hiding the set delta. Meanwhile, `hypr.root.sources_resolve` iterated only `EXPECT` on disk, observing that `ai-usage.conf` still existed on disk, and returned `PASS 18/18 targets exist`. The verifier thus produced a **false green** on target existence for an undeclared source, and completely failed to evaluate whether `replacement.conf` existed on disk!

The move that improves **operability** (eliminating false greens on same-count replacements, duplicate insertions, and unresolvable substitutions) without harming **coverage** or runtime stability is:
- Make `hypr.root.include_graph` report **both** set equality and exact sequence order.
- Make `hypr.root.sources_resolve` bind strictly to the **observed source set** $O_{\text{src}}$ and the expected set $E_{\text{src}}$, validating target existence for every declared and observed target, surfacing named `missing:`, `extra:`, and `unresolved:` deltas.
- Decouple **literal paths** from **wildcard glob expansions** (`*.conf`), establishing distinct falsification criteria for zero-match globs versus expanded set cardinality.

---

## 2. Formal Analysis: Order vs Set Equality vs Target Existence

Let:
- $E_{\text{src}} = \langle e_1, e_2, \dots, e_m \rangle$ be the pinned sequence of expected source directives declared in `EXPECT` ($m = 18$).
- $O_{\text{src}} = \langle o_1, o_2, \dots, o_k \rangle$ be the ordered sequence of `source =` right-hand sides extracted from `hyprland.conf`.
- $\widetilde{E}_{\text{src}} = \{ e_1, \dots, e_m \}$ and $\widetilde{O}_{\text{src}} = \{ o_1, \dots, o_k \}$ be their underlying sets.
- $E_{\text{loc}} = \{ \text{ai-usage}, \dots, \text{xdph}, \text{gkeep} \}$ be the expected set of active `.conf` files in `$H = \text{ROOT}/.config/hypr` ($|E_{\text{loc}}| = 13$).
- $O_{\text{loc}} = \{ f \mid f \in \text{basename}(\operatorname{glob}(H/*.conf)) \land \operatorname{is\_file}(H/f) \}$ be the observed local `.conf` files.

### 2.1 The Verification Matrix

| Property | Evaluated By (Row ID) | Mathematical Condition | Failure Mode Detected | Baseline Seam (Pre-R13) | R13 Gate Behavior |
|---|---|---|---|---|---|
| **Source Set Equality** | `hypr.root.include_graph` | $\widetilde{O}_{\text{src}} \setminus \widetilde{E}_{\text{src}} = \emptyset \land \widetilde{E}_{\text{src}} \setminus \widetilde{O}_{\text{src}} = \emptyset$ | Substituted sources, extra sources, missing sources | Set-blind: reported line index or count only, never named set delta | Names exact `missing: [...]` and `extra: [...]` |
| **Source Include Order** | `hypr.root.include_graph` | $k = m \land \forall i \in \{1,\dots,m\}: o_i = e_i$ | Transposed sources, precedence inversion | Positional only; if count differed, order check was skipped | If set matches but order differs, reports exact line index |
| **Observed Target Existence** | `hypr.root.sources_resolve` | $\forall s \in \widetilde{O}_{\text{src}}: \operatorname{Resolves}(s) \ge 1$ | Dangling source, typo in filename, missing symlink | **Blind**: iterated $E_{\text{src}}$, never checked if $o \in \widetilde{O}_{\text{src}} \setminus \widetilde{E}_{\text{src}}$ existed | Validates that all observed and expected targets exist |
| **Expected Target Existence** | `hypr.root.sources_resolve` | $\forall s \in \widetilde{E}_{\text{src}}: \operatorname{Resolves}(s) \ge 1$ | Deleted prerequisite component, unmounted shared asset | Checked $E_{\text{src}}$ only | Preserved: reports `unresolved: $tmiss` |
| **Local File Set Equality** | `hypr.local.inventory` | $O_{\text{loc}} \setminus E_{\text{loc}} = \emptyset \land E_{\text{loc}} \setminus O_{\text{loc}} = \emptyset$ | Stray unmanaged `.conf` file, dropped required local config | **Blind**: checked $E_{\text{loc}}$ presence only; stray file read `PASS 12/12` | Names exact `missing: [...]` and `extra: [...]` |

---

## 3. Independently Falsifiable Invariants

We enumerate six independently falsifiable invariants governing the configuration plane:

### Invariant 1: Source Cardinality & Duplication Invariance
- **Claim:** Each expected source directive appears exactly once in `hyprland.conf`:
  $$\forall e \in \widetilde{E}_{\text{src}}, \quad \operatorname{count}(e, O_{\text{src}}) = 1 \quad \land \quad |O_{\text{src}}| = |\widetilde{O}_{\text{src}}| = 18$$
- **Falsification Case:** Duplicate inclusion. An operator appends `source = ~/.config/hypr/input.conf` a second time at the end of `hyprland.conf`.
- **Verdict Behavior:**
  - $|O_{\text{src}}| = 19 \neq 18$.
  - $\widetilde{O}_{\text{src}} \setminus \widetilde{E}_{\text{src}} = \emptyset$ (no new path string introduced), but multiset cardinality differs.
  - Gate must emit `FAIL 19 source lines (expected 18)` and isolate the duplicate or surplus entry.

### Invariant 2: Include Order Precedence Invariance
- **Claim:** The sequence of source declarations strictly matches `EXPECT`:
  $$\forall i \in \{1, \dots, 18\}, \quad O_{\text{src}}[i] = E_{\text{src}}[i]$$
- **Falsification Case:** Permutation / Transposition. Swapping line 1 (`autostart.conf`) and line 2 (`bindings/media.conf`).
- **Verdict Behavior:**
  - Set equality holds: $\widetilde{O}_{\text{src}} \equiv \widetilde{E}_{\text{src}}$.
  - Cardinality holds: $|O_{\text{src}}| = 18$.
  - Gate must emit `FAIL line 1: got '~/.local/share/omarchy/default/hypr/bindings/media.conf' want '~/.local/share/omarchy/default/hypr/autostart.conf'`.
  - Crucially: Target resolution (`sources_resolve`) must remain `PASS` (verifying isolation).

### Invariant 3: Disjoint Same-Count Substitution Invariance
- **Claim:** No source directive may be substituted for another file, even if line count is preserved:
  $$\forall s \in O_{\text{src}}, \quad s \in E_{\text{src}}$$
- **Falsification Case:** Same-count swap with existing target. Line 17 `source = ~/.config/hypr/ai-usage.conf` is replaced with `source = ~/.local/share/omarchy/default/hypr/replacement.conf`, where `replacement.conf` exists on disk.
- **Verdict Behavior:**
  - Cardinality holds: $|O_{\text{src}}| = 18$.
  - `include_graph` emits `FAIL line 17: got '...replacement.conf' want '...ai-usage.conf' missing: ~/.config/hypr/ai-usage.conf extra: ~/.local/share/omarchy/default/hypr/replacement.conf`.
  - `sources_resolve` emits `FAIL missing: ~/.config/hypr/ai-usage.conf extra: ~/.local/share/omarchy/default/hypr/replacement.conf`.
  - Baseline would have emitted `PASS 18/18 targets exist` on `sources_resolve` (the false-green defect).

### Invariant 4: Target Path Resolvability Invariance
- **Claim:** Every source target resolves to at least one readable filesystem entry under `$ROOT`:
  $$\forall s \in E_{\text{src}} \cup O_{\text{src}}, \quad \operatorname{Matches}(s, \text{ROOT}) \ge 1$$
- **Falsification Case:** A declared source file is deleted (e.g. removal of `$ROOT/.config/hypr/gkeep.conf` as in selftest scenario B / N4).
- **Verdict Behavior:**
  - `include_graph` remains `PASS` if `hyprland.conf` was not edited (isolation).
  - `sources_resolve` emits `FAIL unresolved: ~/.config/hypr/gkeep.conf`.
  - `local.inventory` emits `FAIL missing: gkeep.conf`.

### Invariant 5: Local Configuration Directory Partition Invariance
- **Claim:** The set of active `.conf` regular files directly under `$ROOT/.config/hypr/` equals $E_{\text{loc}}$ ($|E_{\text{loc}}| = 13$):
  $$O_{\text{loc}} = E_{\text{loc}} = \{ \text{ai-usage}, \text{autostart}, \text{bindings}, \text{envs}, \text{gkeep}, \text{hypridle}, \text{hyprland}, \text{hyprlock}, \text{hyprsunset}, \text{input}, \text{looknfeel}, \text{monitors}, \text{xdph} \}$$
- **Falsification Case:** An untracked configuration file `old-bindings.conf` or `extra.conf` is dropped into `$ROOT/.config/hypr/`.
- **Verdict Behavior:**
  - All 13 expected files exist ($n = 13$).
  - Baseline verifier emitted `PASS 12/12 active local confs` (completely blind to extra files).
  - R13 Gate emits `FAIL extra: extra.conf`.

### Invariant 6: Non-Conf and Subdirectory Immunity Invariance
- **Claim:** The local census is strictly scoped to top-level regular files matching `*.conf`. Non-`.conf` files (such as `.bak.*` backup files, `.txt` notes) and subdirectories are outside the inventory claim:
  $$\forall f \in \text{readdir}(H), \quad f \notin O_{\text{loc}} \iff (f \not\sim \text{*.conf} \lor \operatorname{is\_dir}(f))$$
- **Falsification Case:** Existence of timestamped backup files:
  - `/home/vgpnk/.config/hypr/hyprland.conf.bak.1792267376`
  - `/home/vgpnk/.config/hypr/autostart.conf.bak.1791942509`
- **Verdict Behavior:**
  - These files are present on the host filesystem.
  - The gate ignores them without error or warning. `hypr.local.inventory` evaluates only the 13 active `.conf` files.

---

## 4. Duplicates and Glob Scope Analysis

### 4.1 The Dynamic Toggle Glob: `~/.local/state/omarchy/toggles/hypr/*.conf`
Line 16 of `EXPECT` declares a pattern with wildcard:
```text
source = ~/.local/state/omarchy/toggles/hypr/*.conf
```
This is the only glob directive in `EXPECT`. Its operational semantics require precise separation:

#### A. Expansion Semantics vs Literal String Matching
- In `hyprland.conf`, the directive is written literally as `source = ~/.local/state/omarchy/toggles/hypr/*.conf`.
- In `include_graph`, the string comparison must compare the literal glob expression against `EXPECT[15]`. Expanding the glob at this step would corrupt the include graph order check, because the number of matching toggle files on disk fluctuates at runtime (e.g. 0, 1, or 2 files).
- In `sources_resolve`, the glob must be tested for resolution:
  ```bash
  case "$x" in
    *'*'*) if compgen -G "$x" >/dev/null 2>&1; then continue; fi ;;
  esac
  ```
- **Zero-Match Glob:** If no `.conf` files exist in `~/.local/state/omarchy/toggles/hypr/`, `compgen -G` returns false ($rc \neq 0$). The glob fails resolution: `unresolved: ~/.local/state/omarchy/toggles/hypr/*.conf`.
- **Positive-Match Glob:** On host, the glob expands to 2 files:
  - `/home/vgpnk/.local/state/omarchy/toggles/hypr/window-no-gaps.conf`
  - `/home/vgpnk/.local/state/omarchy/toggles/hypr/flags.conf`
  `compgen -G` succeeds, satisfying resolvability.

#### B. Scope Limitation: Why Globs Must Not Permeate the Core Include Graph
Allowing arbitrary globs in `hyprland.conf` (e.g. `source = ~/.config/hypr/*.conf`) would destroy deterministic configuration precedence. In Hyprland, glob inclusion order depends on filesystem directory traversal order (`readdir()`), which is inode-dependent and unstable across systems or backups.
- Pinned architecture requires 17 explicit static includes and exactly 1 scoped toggle glob.
- Any attempt to replace static includes with wildcards must be rejected by `include_graph` as `extra:` and `missing:`.

### 4.2 Duplicate Directive Analysis in Source Declarations
If an identical source directive appears multiple times:
```text
source = ~/.config/hypr/input.conf
source = ~/.config/hypr/input.conf
```
- In Hyprland, sourcing a file twice executes its directives twice. For keybindings (`bind = ...`), this can result in duplicate key handlers or shadow bindings. For variable assignments (`$var = ...`), it re-executes assignments.
- Set-only comparisons using naive hash maps (`seen["$line"]=1`) would collapse duplicates into a single key, falsely judging $\{ s_1, s_1 \} \equiv \{ s_1 \}$.
- The gate must check multiset cardinality:
  `if [ "${#got[@]}" -ne "${#EXPECT[@]}" ]; then miss="${#got[@]} source lines (expected ${#EXPECT[@]})"; fi`
  Because `${#got[@]} = 19 \neq 18`, the gate rejects duplicates immediately on line count, while the symmetric diff reveals the duplicate entry.

---

## 5. Trace of Second-Order Effects

### 5.1 Substrate & Live Compositor Immunity
- The verification gate runs with read-only primitives (`wc`, `awk`, `grep`, `sha256sum`, `find`, `test`).
- No IPC socket write is performed; `hyprctl dispatch` is never invoked.
- Verifying exact set semantics on disk prevents compositor configuration reload panics: an unnoticed stray `.conf` or unresolvable include could crash Hyprland upon automatic inotify reload (`hyprctl reload`).

### 5.2 Verification & Regression Harness (`--regression`)
- The regression harness excises marked blocks and tests whether mutation defects `D1` through `D9` and `R1` are killed.
- Defect `D6` mutates the local inventory array:
  ```text
  @defect D6 | clause D: gkeep dropped from the 13-conf local inventory
  @old (hyprland bindings input monitors looknfeel hypridle hyprlock hyprsunset ai-usage gkeep autostart envs xdph)
  @new (hyprland bindings input monitors looknfeel hypridle hyprlock hyprsunset ai-usage autostart envs xdph)
  ```
- By establishing exact set semantics, removing `gkeep` from the expected array in `tools/mado-verify.sh` while `gkeep.conf` exists in fixture A immediately causes `hypr.local.inventory FAIL extra: gkeep.conf`.
- Thus, exact set semantics strictly hardens mutant kill detection: `D6` is killed with 100% certainty.

### 5.3 Snapshot Freshness Receipts (`--snapshot-diff`)
- Snapshot receipts record row IDs and status strings in pipe-delimited format:
  `row|hypr|hypr.local.inventory|PASS|13/13 active local confs, set exact`
- Maintaining stable row IDs (`hypr.root.include_graph`, `hypr.root.sources_resolve`, `hypr.local.inventory`) ensures that snapshot diffs do not trigger spurious `appeared` or `vanished` row warnings. Only the status transitions (`recovered`, `regressed`) and detailed deltas are reported.

---

## 6. Sourced Grounding & Evidence Anchors

The following primary sources ground the exact-set and include-order findings:

| Source Identifier / Absolute Path | Revision / Date | Exact Primary Quote (≤25 words) & Location | Category & Tier | Admission Status & Role |
|---|---|---|---|---|
| `/home/vgpnk/Projects/shokunin/mado-shokunin/corpus/lessons/round-12.md` | `7dcb785b` (2026-10-19) | "The drift instrument can detect a count mismatch without naming the set delta, and presence checks do not establish set equality." (`:25`, Mistake M13) | `lesson` / Tier A | **Admitted.** Identifies the canonical problem statement and defect mechanism. |
| `/home/vgpnk/Projects/shokunin/mado-shokunin/corpus/QUALITY.md` | `7dcb785b` (2026-10-19) | "A census compares expected and observed sets and names both missing and extra members; pin module membership where it is a claim." (`:20`, Criterion 14) | `spec` / Tier A | **Admitted.** Establishes the quality standard for all round-13 census gates. |
| `/home/vgpnk/Projects/shokunin/mado-shokunin/corpus/knowledge/config-drift-r12.md` | `a9c6f78b` (2026-10-19) | "The live directory holds 13 `*.conf` (10,650 B), not 12. LOCAL was not widened to match." (`:86-87`) | `knowledge` / Tier A | **Admitted.** Documents host filesystem state and why `LOCAL` remained at 12 in round 12. |
| `/home/vgpnk/Projects/shokunin/mado-shokunin/corpus/knowledge/gate-standing-use.md` | `aaa2e625` (2026-10-14) | "Pins are never edited to match reality. A MOVED pin reports itself" ... "the response is re-verification and an appended erratum" (`:222-226`, §5 Rule 4) | `knowledge` / Tier A | **Admitted.** Governs the re-anchoring of `LOCAL` to 13 members in round 13. |
| `/home/vgpnk/Projects/shokunin/mado-shokunin/tools/mado-verify.sh` | `ea798ad0` (2026-10-20) | "17→18 source lines (+ ~/.config/hypr/gkeep.conf after ai-usage.conf; root sha 4f52854a3c143dcf… → ce7483f35ab52bc2…)" (`:2193-2195`) | `own-work` / Tier A | **Admitted.** Provides the exact anchor for the 18 expected sources and gkeep addition. |

---

## 7. Tooling Record

- **Compliance with Operator Tooling Directive (2026-10-19):**
  - No new external packages, npm modules, or cargo binaries were installed or updated during this analysis.
  - Standard repository reading and file inspection tools were employed under full read-only discipline.
