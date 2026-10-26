# ConnSiblingDup — sibling-overlap scan at the data commit (w2)

Seat: `ConnSiblingDup` (w2, connector). Date: 2026-10-26. Lane: mado-shokunin.
Data commit: `1959770657f1f8665097c1aed4be6c1cbb07139f` (base `a35cfdfcdeb3bd42d1a2cd960faf22ceac1bef3f`).
Scope: read-only re-scan of the 20 sibling lanes under `/home/vgpnk/Projects/shokunin/*-shokunin/` for
holdings overlapping C1 (rule-size vs reported-size join; `tools/mado-geometry.py`) or C2 (gkeep
window geometry, end to end; `corpus/knowledge/hyprland-gkeep-geometry-r43.md`), compared against w1
`w1/ConnSiblingOverlap/overlap.md`. "Anything new since?" — no. Details below.

## Method (all greps used the grep tool, case-insensitive, gitignore disabled)

1. Term sweep over the five surfaces (PROVINCE.md, SKILL.md, corpus/README.md, corpus/knowledge,
   tools) of all 20 siblings for
   `windowrule|window rule|clients -j|set_default_size|gkeep|GEOMETRIC_GOAL|RE2|FullMatch|DefaultFloatingAlgorithm|FloatingAlgorithm`.
2. `float/floating` sweep over the same five surfaces (catch window-rule float holdings that do not
   use the literal word `windowrule`).
3. `hypr` sweep over the same five surfaces (adjacent Hyprland holdings).
4. Fleet-wide `hyprctl` sweep over all 20 sibling lane roots.
5. Read-only `git log` (2026-10-25 → 2026-10-26) in each sibling for `-- PROVINCE.md SKILL.md
   corpus/README.md corpus/knowledge tools`.
6. Read of the landed C2 entry (`corpus/knowledge/hyprland-gkeep-geometry-r43.md`), mado
   `PROVINCE.md:22-48` (tool inventory), mado `SKILL.md:129-295` (routing table, decision row,
   probe row, subsection), tsukuroi `PROVINCE.md:119-143` + `adjacency-anchors-r19.json:47-73`,
   kotoba `sibling-overlap-census-round74.md:47-108` + `PROVINCE.md:68-72`, kumitate
   `.ufo/waves/round-50/r50/ConnMadoBind.md`, kake `ops-automation.md:74-98`, game-dev-2d
   `corpus/live/r79-boundary-exec/run_love_probe.py:41-49`.

## 1. Content overlap: none (w1 finding still holds at the data commit)

- No sibling lane holds a fact that C1's tool or C2's entry would duplicate or re-derive:
  - The only sibling occurrence of `hyprctl clients -j` remains game-dev-2d's
    `run_love_probe.py:41-49` — it reads **presence** fields (`class`/`initialClass`/`title`) to
    detect a love window; no `size`, no rule text, no join.
  - No sibling file on any of the five surfaces contains `windowrule`, `window rule`,
    `set_default_size`, `gkeep`, `GEOMETRIC_GOAL`, `RE2`, `FullMatch`, `DefaultFloatingAlgorithm`
    or `FloatingAlgorithm`. The only `fullmatch` hits elsewhere are Python `re.fullmatch`
    (audio fixtures, kaidoku/kama/chousa gates, kengaku grader, lore worked example) — unrelated.
  - The `float/floating` sweep hits are unrelated domains: audio sample levels, Godot
    `MOTION_MODE_FLOATING`, llama.cpp float32 field saturation, Java/JS `float` types.
  - The `hypr` sweep reproduces exactly the w1 adjacent holdings (rows A–G below), all unchanged.
- gkeep appears in **no** sibling lane. The only lane with gkeep knowledge is mado itself.

## 2. Adjacent sibling holdings (no content overlap; shared surface or arbitration claim unchanged)

| # | Lane | Holding (path:line) | What it touches | Relation to C1/C2 |
|---|---|---|---|---|
| A | game-dev-2d | `corpus/live/r79-boundary-exec/run_love_probe.py:41-49` | runs `hyprctl clients -j`, reads `class`/`initialClass`/`title` to find love windows | Same **read verb** as C1, disjoint fields (presence, not size); no rules; no geometry join |
| B | kake | `corpus/knowledge/ops-automation.md:83` | `grokbot start` spawns Grok Bot app on Hyprland workspace 3, silent/unfocused | Hyprland **workspace targeting**; no sizes, no rules, no client census |
| C | mori | `corpus/knowledge/observability-census-r1.md:93-94,142-146` | host cgroup scopes named `app-Hyprland-xdg-terminal-exec-…scope`; OOM kills | **Host liveness** observations; no window geometry |
| D | tabi | `corpus/knowledge/hygiene-sweep-r4.md:113-128`; `webbridge-daemon-disposition.md:271` | Hyprland session lifecycle (SIGSEGV, OOM restart) | **Session lifecycle** history; no window geometry |
| E | tsukuroi | `PROVINCE.md:124` (OUT-004), `corpus/knowledge/adjacency-anchors-r19.json:55-59` | ADJ anchor: "Mado owns the Hyprland, waybar, walker and terminal configuration plane, themes/wallpapers and screen/idle behavior." | Host-surface **adjacency registry** that assigns the Hyprland config plane to mado; no rule/size facts (see §4) |
| F | tameshi | `corpus/knowledge/mutation-case-mado-verify.md`; `fleet-suite-census.md:438-452`; `tools/mutate-and-run.sh` | mutation-testing **service** over mado's tools (`mado-verify.sh`; PATH-stub hyprctl scenarios) | Relationship lane for mado tools' quality; `tools/mado-geometry.py` is a **new candidate target** of this service |
| G | kotoba | `corpus/knowledge/sibling-overlap-census-round74.md:66,97`; `PROVINCE.md:69`; verifier `verifiers/check_sibling_census.py` | fleet sibling-overlap census (20 lanes), mado row `none` (skill file SKILL.md, arbitration `no`, delta +118/-0) | **Registrar/arbiter** for sibling-overlap claims, not a content holder |

Non-substantive hits: kumitate `kimi-session-state.md` (embedded JSON transcript), audio/kaidoku/
lore/kengaku (Python `re.fullmatch`), game-dev-3d (Godot `FLOATING`), kama (float32 API fields).

## 3. Anything new since w1? No

- Sibling `git log` restricted to the five surfaces, 2026-10-25→26, shows no commit touching any of
  them with C1/C2-relevant content: the active sibling rounds today are kaidoku r38 (RE/unblob),
  kama r44 (LLM serving), kasegi r35 (bounty), kengaku r39 (battery/LLM eval), souji r31/32
  (records hygiene), tabi r30 (browser), tsukuroi r40 (libalpm exec env, package state). None adds a
  window-geometry/gkeep/`clients -j`-size holding.
- The only new content in the fleet is mado's own data commit: `tools/mado-geometry.py`,
  `corpus/knowledge/hyprland-gkeep-geometry-r43.md`, rows S290-S297 in `corpus/SOURCES.md`,
  `corpus/lessons/round-43.md`, README index/Frontier, `PROVINCE.md:32` (tool row), SKILL.md
  decision row `:158` / probe row `:225` / subsection `:246-295`, QUALITY.md criteria 77-81,
  `quality/check-locators.py`.
- w1's proposed move (entry Limits should name game-dev-2d and kake as the sibling read-verb/workspace
  holders) did **not** land: the landed entry's "What this entry does not establish" (`hyprland-gkeep-geometry-r43.md:76-80`)
  lists UNK items but names no sibling holder. Open adjacency-visibility item; nothing in
  PRED-C2-r43-v2 requires it, so it is not a predicate defect.

## 4. Does mado's new SKILL decision row overlap a sibling's routing row? No (three proximate rows)

- **tsukuroi OUT-004** (`PROVINCE.md:124`; `adjacency-anchors-r19.json:55-59`) is an ownership
  locator whose quoted surface is `~/.config/hypr/` incl. "keybinds, rules", proposition
  "Mado owns the Hyprland, waybar, walker and terminal configuration plane, themes/wallpapers and
  screen/idle behavior." The new decision row (rule-size vs reported-size join) sits **inside** that
  registered plane — it deepens "rules" + "display behavior", it does not cross any boundary.
  tsukuroi itself declares the pins stale by design once a sibling commits (`PROVINCE.md:132`), so
  the r19 pin `a4046a821608` is not a live contradiction.
- **kumitate SKILL.md:622** (bind-oracle gate row: "requested **mount** binds — not the Hyprland
  `mado-binds.py` keybind file") and `corpus/knowledge/counter-amendment-discipline.md:82-83` +
  `mount-order-and-bind-scope.md:15` name a *different* mado tool (`mado-binds.py`, keybind table).
  Disjoint vocabulary (binds vs window geometry); no overlap with the decision row. `mado-geometry.py`
  is not named anywhere in kumitate.
- **tameshi** rows (`mutation-case-mado-verify.md:51`, `fleet-suite-census.md:448-451`) describe the
  mutation service over mado's tools and already anticipated new mado tools (w1 row F). The new
  `tools/mado-geometry.py` is a new candidate target of that service, not a contested surface.
- **kotoba** census r74 (`sibling-overlap-census-round74.md:66,97`) lists mado at `none` with skill
  file SKILL.md and scope quote `SKILL.md:8`; the new rows do not change the classification (no
  sibling holds the join surface).

## 5. Arbitration (contested surfaces: none new)

- **kotoba** — fleet sibling-overlap census (round 49, 74) + `check_sibling_census.py`: standing
  registrar/arbiter for any overlap/adjacency claim between lane skills/provinces.
- **tsukuroi** — host-operability lane; ADJ registry (OUT-004) anchors mado as owner of the Hyprland
  config plane; any host-surface boundary question routes through its adjacency anchors.
- **game-dev-2d** — the only other consumer of the `hyprctl clients -j` read verb; would arbitrate
  any claim about reading `clients -j` fields (currently disjoint: presence vs size).
- **tameshi** — owns the mutation-testing method over mado tools; arbitrates tool-quality/mutation
  claims, not facts (new candidate: `mado-geometry.py`).
- **mori** — host liveness/process observation (would arbitrate any claim about a live gkeep/hyprland
  process state; C2 currently makes none).

## 6. Confirmations at the data commit

- `PROVINCE.md:32`: `tools/mado-geometry.py` inventory row lands (reads `--rules` files ≤ 1 MiB and
  one `--clients` dump/`-`, stdout only, selftest writes nothing; no socket/network/process).
- SKILL.md probe row `:225` and subsection `:246-295` match the live receipt
  `receipts/live-geometry-host.txt` (`MADO_GEOMETRY: … verdict=NO_MATCHING_CLIENT`, rc 3) and the
  registration's host-run description; the decision row `:158` routes to the same two read-only
  inputs with `[OBS]`/`[UNK]` licences.
- The landed entry `hyprland-gkeep-geometry-r43.md` is internally consistent with PROVINCE/SKILL
  boundaries (rule text, source-declared client request, goal-box semantics; live rendered size and
  runtime behaviour stay `[UNK]`), matching w1 §5's "may/may not claim" split.

## 7. Proposed move (one, bounded — for the L1's consideration, no predicate touched)

Record the open w1 item in the round-43 lesson or README frontier (or carry it to round 44): the
landed C2 entry's Limits section never names the two sibling holders of the same read verb/workspace
(game-dev-2d `clients -j` presence reads; kake grokbot workspace targeting). Naming them would let
kotoba's census see the adjacency if either lane ever moves into the other's field. This is a
visibility/coverage-adjacency improvement only: it changes no frozen file, no counter input, no C1
tool, and no predicate; it harms no axis.

Evidence anchors: all paths above; w1 `ConnSiblingOverlap/overlap.md`; registration.md lines 18-34,
45-55; registration-v2.md lines 9-34.
