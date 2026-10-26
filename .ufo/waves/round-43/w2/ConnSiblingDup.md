# ConnSiblingDup — w2 seat report (sibling-lane overlap)

Seat: `ConnSiblingDup` (w2, connector). Lane: mado-shokunin. Date: 2026-10-26.
Data commit: `1959770657f1f8665097c1aed4be6c1cbb07139f`. Base: `a35cfdfcdeb3bd42d1a2cd960faf22ceac1bef3f`.

Status: **complete**. Full deliverable: `.ufo/waves/round-43/w2/ConnSiblingDup/overlap.md`.

Scope: read-only re-scan of the 20 sibling lanes under `/home/vgpnk/Projects/shokunin/*-shokunin/`
(PROVINCE.md, SKILL.md, corpus/README.md, corpus/knowledge, tools) for holdings about window-rule
size/float, `hyprctl clients -j` size semantics, GEOMETRIC_GOAL, gkeep, compared against w1
`w1/ConnSiblingOverlap/overlap.md`.

Findings (short form; details and evidence anchors in overlap.md):

1. No new content overlap since w1. Term sweep (`windowrule|window rule|clients -j|set_default_size|gkeep|GEOMETRIC_GOAL|RE2|FullMatch|DefaultFloatingAlgorithm|FloatingAlgorithm`) and `float/floating` and `hypr` sweeps over all five surfaces of all 20 siblings: zero substantive hits outside the seven known adjacent holdings (game-dev-2d `run_love_probe.py` read verb; kake grokbot workspace; mori/tabi Hyprland session units; tsukuroi OUT-004; tameshi mutation service; kotoba census). All Python `re.fullmatch` hits are unrelated.
2. Sibling git logs 2026-10-25→26: no sibling commit touches any of these surfaces. The only new content is mado's own data commit (tool, entry, SKILL rows, PROVINCE tool row, lesson, QUALITY, locator checker).
3. mado's new SKILL decision row (`SKILL.md:158`), probe row (`:225`) and subsection "Rule size versus reported size" (`:246-295`) overlap no sibling routing row. Nearest routing rows: tsukuroi OUT-004 (contains the new row's surface — rules + display behavior — rather than conflicting), kumitate bind-oracle row (names `mado-binds.py`, disjoint vocabulary), tameshi mutation service (new candidate target: `mado-geometry.py`), kotoba census r74 (mado stays `none`).
4. w1's proposed move (a "Boundary transition" paragraph in the C2 entry's Limits naming game-dev-2d and kake) did **not** land: the landed entry `corpus/knowledge/hyprland-gkeep-geometry-r43.md` ("What this entry does not establish") names no sibling read-verb/workspace holder. Open adjacency-visibility item; not a PRED-C2-r43-v2 defect.
5. Contested surfaces: none new. Arbitration stands: kotoba (fleet sibling-overlap registrar), tsukuroi (ADJ registry, OUT-004), game-dev-2d (`clients -j` read-verb field claims), tameshi (mutation method over mado tools).

No tools installed (built-in read/grep only). No scratch dir used (read-only scan; no scratch needed).

Report trailer: `.ufo/waves/round-43/w2/ConnSiblingDup.md`
