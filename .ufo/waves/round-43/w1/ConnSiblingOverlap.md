# Seat ConnSiblingOverlap — round 43 w1 report

Status: DONE. Sibling-overlap scan complete; findings at
`.ufo/waves/round-43/w1/ConnSiblingOverlap/overlap.md` (written first, then refined).

Result summary:
- **No overlaps.** No sibling lane holds a C1 or C2 fact. `gkeep` appears in no sibling lane;
  the only `hyprctl clients -j` consumer outside mado is game-dev-2d (`run_love_probe.py:41-49`,
  presence fields only, no sizes/rules); the only Hyprland references elsewhere are workspace
  targeting (kake `ops-automation.md:83`), session/OOM lifecycle (mori, tabi), host-adjacency
  registry (tsukuroi OUT-004), and kotoba's fleet sibling-overlap census (mado row = `none`).
- **Nearest in-fleet holdings are in-lane** (rule-attribution-r24, keybind-rule-semantics,
  hyprland-config-plane §5, config-drift-r12, host-bar-producer-census-r40).
- **Arbiters (adjacency axis):** kotoba (sibling-overlap census registrar), tsukuroi (host-surface
  ADJ registry), tameshi (mutation/method service over mado tools), mori (host liveness),
  game-dev-2d (other `clients -j` consumer).
- **gkeep bounds:** mado may claim host rule text (S297), installer provenance
  (config-drift-r12), the app's source-declared `set_default_size(420,500)` (S299 — a deliberate
  boundary transition vs host-bar-producer-census-r40.md:37 "not owned"; entry should state it),
  and the host census (S298). May not claim live app behaviour/runtime size. No gkeep window in
  S298.
- **No registration contradictions;** base-tool absence confirmed (git ls-tree), S299 header fix
  confirmed.
- **Proposed move:** C2 entry carries a "Boundary transition" paragraph (source-declared vs live
  behaviour; first rule-body capture; name the two sibling read-verb/workspace holders in Limits).
- Tooling: no installs performed (standard fleet tools only). Scratch: none created (no clone/
  venv needed), so nothing to clean.
