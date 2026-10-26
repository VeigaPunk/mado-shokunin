# ConnSiblingOverlap — sibling-overlap scan for round-43 C1/C2

Seat: `ConnSiblingOverlap` (w1). Date: 2026-10-26. Lane: mado-shokunin.
Scope: read-only scan of the other lanes under `/home/vgpnk/Projects/shokunin/*-shokunin/` for
holdings overlapping C1 (rule-size vs reported-size join; `tools/mado-geometry.py`) or C2
(gkeep window geometry, end to end; `corpus/knowledge/hyprland-gkeep-geometry-r43.md`).

Method (every grep used the grep tool, case-insensitive, gitignore disabled):

1. `grep -rli 'windowrule|window rule|clients -j|set_default_size|gkeep' */corpus/knowledge */tools */SKILL.md */PROVINCE.md` — fleet-wide (excluding mado), then per-lane `{PROVINCE.md,README.md,SKILL.md,tools,corpus}`.
2. `grep -rli 'RE2|FullMatch|GEOMETRIC_GOAL|set_default_size|DefaultFloatingAlgorithm|FloatingAlgorithm'` across all 20 sibling lanes.
3. `grep -rli 'hypr'` across sibling lanes' PROVINCE/README/SKILL/corpus-knowledge (find adjacent Hyprland holdings).
4. Word `gkeep` sweep across all 20 sibling lanes.
5. Verified the frozen fetch pins used by C2 (`fetch/host-gkeep.conf`, `fetch/host-clients-r43.json`, `fetch/gkeep-ui-excerpt.py`, `receipts/fetch-sha256.txt`).
6. Read-only git in mado: `git ls-tree a35cfdf… tools/` (no geometry tool at base) and `git status --short -- tools/` (`?? tools/mado-geometry.py` → build seat landed it this wave; consistent with registration lines 20-27).

## 1. Overlaps: none

No sibling lane holds a fact that C1's geometry tool or C2's entry would duplicate or re-derive:

- The only sibling occurrence of `hyprctl clients -j` is game-dev-2d's `run_love_probe.py` (see §2, row A). It uses the **presence** fields (class/initialClass/title) to detect a love window, not `size`; no rule text, no size join.
- No sibling lane contains `windowrule`, `set_default_size`, `RE2`, `FullMatch`, `GEOMETRIC_GOAL`, or a floating-algorithm reference (`grep` sweeps 1-4: zero substantive hits outside mado; the only `fullmatch` hits elsewhere are Python `re.fullmatch` in audio fixtures, unrelated).
- `gkeep` appears in **no** sibling lane. The only lane with gkeep knowledge is mado itself (config-drift-r12.md, host-bar-producer-census-r40.md, SKILL.md erratum, and now C2).
- mado's classification in kotoba's fleet sibling-overlap census is `none` (no adjacent lane): `sibling-overlap-census-round74.md:66` / `:97`, quote `SKILL.md:8` "desktop & compositor craft playbook — the Hyprland/waybar/walker/terminal config plane".

## 2. Adjacent sibling holdings (no content overlap, shared surface or arbitration claim)

| # | Lane | Holding (path:line) | What it touches | Relation to C1/C2 |
|---|---|---|---|---|
| A | game-dev-2d | `corpus/live/r79-boundary-exec/run_love_probe.py:41-49` | runs `hyprctl clients -j`, reads `class`/`initialClass`/`title` to find love windows; negative control without override | Same **read verb** as C1, different fields (presence, not size); no rules; no geometry join |
| B | kake | `corpus/knowledge/ops-automation.md:83` | `grokbot start` spawns Grok Bot app on Hyprland workspace 3, silent/unfocused | Hyprland **workspace targeting** in an ops automation; no sizes, no rules, no client census |
| C | mori | `corpus/knowledge/observability-census-r1.md:93-94,142-146` | host process/cgroup scopes named `app-Hyprland-xdg-terminal-exec-…scope`; OOM kills | **Host liveness** observations involving Hyprland session units; no window geometry |
| D | tabi | `corpus/knowledge/hygiene-sweep-r4.md:113-128`; `webbridge-daemon-disposition.md:271` | Hyprland session lifecycle (SIGSEGV, OOM restart) | **Session lifecycle** history; no window geometry |
| E | tsukuroi | `PROVINCE.md:124` (OUT-004), `corpus/knowledge/adjacency-anchors-r19.json:55-59`, `adjacency-anchors-r19.md:84` | ADJ registry anchors: "Mado owns the Hyprland, waybar, walker and terminal configuration plane…"; also `aur-risk-plane.md:199` lists `hyprland-preview-share-picker` package | Host-surface **adjacency registry** that already assigns the Hyprland config plane to mado; no rule/size facts |
| F | tameshi | `corpus/knowledge/mutation-case-mado-verify.md:1-63`; `service-limits.md:97-101`; mado `PROVINCE.md:28` | mutation-testing **service** over mado's tools (mado-verify.sh; PATH-stub hyprctl scenarios; live-plane gap recommendations) | Relationship lane for mado tools' quality; no content overlap; a future target for mado-geometry.py |
| G | kotoba | `corpus/knowledge/sibling-overlap-census-round49.md:82`, `…round74.md:66`, `PROVINCE.md:69`, verifier `verifiers/check_sibling_census.py` | fleet sibling-overlap census (20 lanes), mado row `none` | **Registrar/arbiter** for sibling-overlap claims, not a content holder |

Non-substantive hits: kumitate `kimi-session-state.md` (archived agent-session blob, 2026-10-03, token hit lies inside an embedded JSON transcript; no knowledge claim), kotodama/lore/kaidoku/audio/game-dev-3d (only generic words `geometry`/`floating` in unrelated domain entries).

## 3. Who arbitrates (adjacency axis)

- **kotoba** — fleet sibling-overlap census (round 49, 74) + `check_sibling_census.py` is the standing registrar for any overlap/adjacency claim between lane skills/provinces. Its round-74 census pins mado at `none`, so it is the neutral arbiter if a future sibling moves into the Hyprland geometry plane.
- **tsukuroi** — host-operability lane; its ADJ registry (OUT-004) already anchors mado as owner of the Hyprland config plane. Any host-surface boundary question (what is "config plane" vs "host package/service state") routes through its adjacency anchors.
- **tameshi** — owns the mutation-testing method over mado tools (consumed read-only, PROVINCE row). C1's tool becomes a candidate target of that service; tameshi arbitrates tool-quality/mutation claims, not facts.
- **mori** — host liveness/process observation (would arbitrate any claim about a live gkeep/hyprland process state; C2 currently makes none).
- **game-dev-2d** — the only other consumer of the `hyprctl clients -j` read verb; would arbitrate any claim about reading `clients -j` fields (currently disjoint: presence vs size).

## 4. Duplication verdict

- **C1 tool (`mado-geometry.py`)** duplicates no sibling-held fact. Its inputs (windowrule `size W H` lines; `hyprctl clients -j` `size` field) and its join are un-held by any other lane. Nearest sibling usage (game-dev-2d row A) uses the same command on disjoint fields.
- **C2 entry** duplicates no sibling-held fact. Its chain (rule text → RE2 FullMatch → size/float effects → floating algorithm → target/window box storage → animated GEOMETRIC_GOAL → client `set_default_size` → host census) maps to pinned Hyprland sources (S290-S296) and own-work receipts (S297-S299); the nearest in-fleet holdings are **in-lane** (rule-attribution-r24.md, keybind-rule-semantics.md, hyprland-config-plane.md §5, arc-synthesis.md, config-drift-r12.md, host-bar-producer-census-r40.md), not sibling.

## 5. gkeep: what mado may and may not claim

Prior in-lane boundaries (the entry must stay consistent with them):

1. `corpus/knowledge/config-drift-r12.md:9-11` — "The lane measures and reports it; the operator project `~/Projects/gkeep` owns its installer." (installer read, never executed; `:68` "That installer and its reload were read, not executed. No inference about an actual process invocation is promoted to observation.").
2. `config-drift-r12.md:50` — "`gkeep.conf` was counted only by bytes, lines, and directive kind; no rule contents were copied into this record." (round-12 deliberately did **not** record the rule body; round-43's S297 is the first capture — say so).
3. `corpus/knowledge/host-bar-producer-census-r40.md:37` — "Nothing about the gkeep or ai-usage packages' behaviour, install state or window rules: they are chain evidence (shim bytes and declared contract), not owned."
4. `PROVINCE.md:18` (round-19 refinement) — consumer configs of owned chains are "chain evidence only, their consumer configs not owned"; `PROVINCE.md:6-12` owns `~/.config/hypr/` (rules) read-only.

Consequently: **may** claim — host rule text (S297), installer provenance and its declared effects (install.sh bytes; config-drift-r12), the app's *source-declared* request (S299: `window.set_default_size(420, 500)` at gkeep 133b867, line 33 of the excerpt), and the host census (S298). **May not** claim — live app behaviour, runtime window size, or install state beyond what the pinned bytes state; no inference from installer presence to app runtime; no claim that the current host has a gkeep window (S298 has none, consistent with the provisional census in registration line 52).

Round-43 C2 asserts the app's own request from S299. That is a deliberate, sourced extension of the round-40 "not owned" wording — flag it as a boundary transition with a flip condition, not as a silent contradiction: the entry should state that it claims what the app's source declares (a static GTK default size), not observed runtime behaviour (which remains out of province; flip condition = an operator-approved runtime observation, reported, never scored).

## 6. Contradictions with registration: none found; confirmations

- Registration lines 20-21 (no geometry tool at base) confirmed: `git ls-tree a35cfdf… tools/` has no `mado-geometry.py`; the file is present now as untracked `??` (a w1 build seat landed it). No sibling holds an equivalent.
- Registration lines 51-55 (S297/S298/S299 pins; fixed excerpt header `446-488 (end of file)`, full-file sha256 `07a3c4a5…`) confirmed against the fetch receipts and `fetch-sha256.txt` (S299 header says `lines 446-488 (end of file)`; S297 byte-copy sha256 `3726e488…`; S298: 4 clients, all mapped/floating=false, size 1720×1414, no gkeep).
- Registration line 34 (no rendered-geometry knowledge at base) consistent with the in-lane corpus above (window rules and effects exist, but no rule-size vs reported-size join, and no gkeep geometry end-to-end).

## 7. Proposed move (one, bounded)

Have the C2 entry include a short "Boundary transition" paragraph that (a) states S299 is the first time the lane claims a *declared* gkeep app request and that it supersedes only the "not owned" wording of `host-bar-producer-census-r40.md:37` for source-declared behaviour, keeping live behaviour out of province; (b) records that S297 is the first capture of the gkeep.conf rule body (round-12 deliberately withheld it); and (c) names the two sibling read-verb/workspace holders (game-dev-2d, kake) in the entry's Limits section so a future sibling move into size joins is visible to kotoba's census. This keeps the entry self-consistent with PROVINCE/SKILL boundaries (coverage) and changes nothing about C1 (operability unharmed).

Evidence anchors: all paths above; registration.md lines 18-34, 45-55.
