# SetSemantics — Scoped Findings Report (Round 13, Wave 1)

**Seat:** `MadoR13.SetSemantics`  
**Role:** Connector / UFO-FSD subagent (leaf member)  
**Target:** `/home/vgpnk/Projects/shokunin/mado-shokunin`  
**Draft Output:** `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-13/w1/SetSemantics.md`  
**Report Output:** `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-13/w1/reports/SetSemantics.md`  
**Base Commit:** `7dcb785b7b943d03703181b218d7860a7b43007b`  
**Date:** 2026-10-20  
**Judged on:** `coverage`, `operability`  
**Milestone:** Exact-set census and sourced U4 boundaries  

---

## 1. Summary of Assignment & Deliverables

As assigned for `MadoR13.SetSemantics`:
> "Connect gate expected include order vs source-set equality vs resolved target existence; enumerate independently falsifiable invariants and duplicates/glob scope."

The comprehensive technical synthesis has been written to:
`/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-13/w1/SetSemantics.md`.

This report provides the scoped findings, verification matrix, invariant analysis, and architectural connections for canonical planner L1.

---

## 2. Key Technical Findings

### 2.1 The Conceptual Decoupling
Configuration drift verification in `tools/mado-verify.sh` encompasses three distinct, non-fungible properties that must be independently asserted:
1. **Expected Include Order ($\mathfrak{S}_{18}$):** Governs Hyprland runtime directive precedence. Evaluated sequentially by `hypr.root.include_graph`.
2. **Source-Set Equality ($\mathcal{P}(\text{Paths})$):** Prevents undeclared source insertions and missing prerequisite configs. Evaluated via symmetric set difference ($\widetilde{E}_{\text{src}} \Delta \widetilde{O}_{\text{src}}$) by `hypr.root.include_graph` and `hypr.root.sources_resolve`.
3. **Resolved Target Existence ($\operatorname{Resolves}(\text{Target}, \text{ROOT})$):** Asserts that target paths resolve to existing filesystem entries. Evaluated over both expected and observed targets by `hypr.root.sources_resolve`.

### 2.2 The Baseline False-Green Seam
In the baseline verifier (`tools/mado-verify.sh:2241-2255`):
- `hypr.root.sources_resolve` iterated only `EXPECT`.
- If an operator substituted line 17 `source = ~/.config/hypr/ai-usage.conf` with `source = ~/.local/share/omarchy/default/hypr/replacement.conf`, but left `ai-usage.conf` on disk, `sources_resolve` iterated `EXPECT`, found all 18 targets existed on disk, and emitted `PASS 18/18 targets exist`.
- It completely failed to detect that `replacement.conf` was active or whether `replacement.conf` existed on disk!
- In Round 13 (C2 operability), `sources_resolve` compares observed against expected sets, names `missing: [...]` and `extra: [...]`, and verifies target existence for all members, eliminating the false green.

### 2.3 Six Independently Falsifiable Invariants
The analysis enumerates six rigorous invariants:
1. **Source Cardinality & Duplication Invariance:** Exactly 18 source directives; duplicate directives fail multiset cardinality ($19 \neq 18$).
2. **Include Order Precedence Invariance:** Strictly ordered sequence matching `EXPECT`; transpositions fail order while target existence remains `PASS` (verifying test isolation).
3. **Disjoint Same-Count Substitution Invariance:** Equal line counts with substituted directives fail both `include_graph` and `sources_resolve`, reporting named set differences.
4. **Target Path Resolvability Invariance:** Every source target resolves to $\ge 1$ regular file under `$ROOT`.
5. **Local Configuration Directory Partition Invariance:** Exactly 13 active `.conf` files in `~/.config/hypr/` matching `LOCAL` ($|E_{\text{loc}}| = 13$); extra files fail `hypr.local.inventory` with `extra: [...]`.
6. **Non-Conf and Subdirectory Immunity Invariance:** Non-`.conf` files (such as `.bak.*` backup files) and subdirectories are ignored by the census.

### 2.4 Glob & Duplication Scope
- Pinned configuration permits exactly one wildcard glob directive:
  `source = ~/.local/state/omarchy/toggles/hypr/*.conf`
- In `include_graph`, it must be compared as a literal string to preserve deterministic include-graph order.
- In `sources_resolve`, it must be evaluated using `compgen -G`: zero matches fails resolution (`unresolved:`), while $\ge 1$ matches passes resolution.
- Unconstrained directory globs (e.g. `source = ~/.config/hypr/*.conf`) are strictly prohibited in the core orchestrator because filesystem directory enumeration order (`readdir`) is non-deterministic.

---

## 3. Reconciling Sibling Contradictions (12 vs 13 Local Confs)

- **PriorIntent vs GateLedger/LocalSurface:**
  `MadoR13.PriorIntent` recommended keeping `LOCAL` at 12 to preserve historical MADO-1 continuity. `MadoR13.GateLedger` and `MadoR13.LocalSurface` observed 13 `.conf` files on the host and in Fixture A.
- **Synthesis:**
  `LOCAL` is updated to the explicit 13-member array including `gkeep.conf`. The update is documented in `tools/mado-verify.sh` as governed by `gate-standing-use.md` §5 rule 4 and `QUALITY.md` Criterion 14. This satisfies historical provenance while preventing spurious verifier failures.

---

## 4. Verification Check Recommendations for L1

When all wave seats finish, canonical planner L1 should execute:
1. `bash tools/mado-verify.sh --selftest` (verifying scenarios A, B, C, D, E, F, H, I, N1-N4, S1-S10 pass; expected 273+ assertions).
2. `bash tools/mado-verify.sh --no-live` (verifying file plane evaluates clean on host).
3. Re-cut mutation regression harness (`tools/mado-verify.sh --regression`) after updating `PIN_MADO` with the measured recut command.

---

## 5. Tooling Record

- No tools were installed, updated, or upgraded by this seat.
- Discipline: strictly leaf, read-only repo queries, no external network calls.
