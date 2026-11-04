# R79ExecC1Cases — independent re-derivation of the five new C1 expectations

Seat: executor, round mado 79 wave 1. Derived from source rules only, before any tool run; then ran `tools/mado-barfoot.py` (sha256 `c9aa139152643020acf27b5aef8026ae5b8a5f70372e86abb4a032c82bed86de`, re-hashed locally = frozen) per case and compared. Scratch `/fast/scratch/hyaku/mado-r79/R79ExecC1Cases/` deleted before finish. No repo file outside my write dir touched; no git/jj mutation.

## Source rules used (no tool source read before derivation)

- S465 `src/output/Monitor.cpp` (`fetch/S465.bin`):654 `m_reservedArea.setStatic(m_activeMonitorRule.m_reservedArea)` — a monitor's static reserved area is its (last matching) monitor rule's reserve; :1772-1773 `logicalBoxMinusReserved() { return m_reservedArea.apply(logicalBox()); }`.
- S466 `src/desktop/reserved/ReservedArea.cpp` `apply()`: `x += topLeft.x; y += topLeft.y; w -= topLeft.x + bottomRight.x; h -= topLeft.y + bottomRight.y` — usable box = logical box inset by (left, top, right, bottom); **no clamping** in `apply()` (only initial static values clamp ≥0 in the constructor).
- Rule arg order `monitor = NAME, addreserved, TOP, BOTTOM, LEFT, RIGHT`; hyprctl `reserved` array order is `[left, top, right, bottom]` (carried cases confirm: `bottom-bar` bottom 30 → `[0,0,0,30]`).
- Last matching rule per monitor wins; a rule binds only its named monitor (`m_activeMonitorRule` is selected per monitor).
- Band convention grounded in carried cases: extent = size + near margin + far margin (`top-margin-asym` 10+30+2=42; `left-margin` 6+40+6=52; `right-zero-margin` 40). Expected band on the bar's edge = `static[edge] + extent`.
- Verdicts: EQ/DIFFER compare computed band to observed `reserved[edge]`; exclusive=false → bar reserves nothing → NOT_APPLIED (would-be band printed as `expected`); rc 0 clean, 1 DIFFER, 3 model refusal, 2 setup.

## Part 1 — re-derived vs tool (the five new cases, controls/c1-cases-r79.json indexes 18-22)

| case | re-derived (usable box / declared box / band / verdict+rc) | tool (`MADO_BARFOOT_RESULT` / rc) | agree? |
|------|-------------------------------------------------------------|-----------------------------------|--------|
| static-composed | box x0 y26 w3440 h1414; bar x4 y30 w3432 h26; band 26+(26+4+4)=**60**; EQ, MATCH, rc 0 CLEAN | `box=MATCH reserved=EQ band=60 expected=60 verdict=CLEAN` rc 0 | **yes** |
| static-other-edge | box x40 y0 w3400 h1440; bar x40 y0 w3400 h26; band 0+26=**26** (left 40 moves the box, not the top band); EQ, MATCH, rc 0 | `box=MATCH reserved=EQ band=26 expected=26 verdict=CLEAN` rc 0 | **yes** |
| static-exclusive-false | box x0 y26 w3440 h1414; bar x0 y26 w3440 h26; band **26**, would-be **52** printed; NOT_APPLIED, MATCH, rc 0 | `box=MATCH reserved=NOT_APPLIED band=26 expected=52 verdict=CLEAN` rc 0 | **yes** |
| static-last-wins (`--monitor M1`) | M1's newest rule 26 (first M1 rule 10 overridden; M2's rule binds only M2); box y26; bar y26; band 26+26=**52**; EQ, MATCH, rc 0 | `box=MATCH reserved=EQ band=52 expected=52 verdict=CLEAN` rc 0 | **yes** |
| static-source-refused | `source =` line is not a monitor rule; rules tree unresolvable → **refusal rc 3, stage=model** | `MADO_BARFOOT: ERROR (stage=model the rules file carries a `source =` line (line 1); a sourced file is not followed, so the static reserve is unknown)` rc 3 | **yes** |

5/5 agree with the frozen `expect` blocks; 0 divergences in Part 1.

## Part 2 — five own adversarial fixtures

| fixture | setup | correct answer from sources | tool answer | agree? |
|---------|-------|------------------------------|-------------|--------|
| A1a bottom-bar+static-bottom, bar at physical edge | 1920x1080; bar bottom h30 margin0 at y1050; `monitor = M1, addreserved, 0, 30, 0, 0`; observed reserved [0,0,0,60] | band bottom = 30+30 = **60** EQ; but the frozen claim sentence says the bar is arranged *inside* the static-reduced usable box (y0..1050) — a bar at y1050 overlaps the static strip, so the box axis must not claim MATCH | `box=DIFFER reserved=EQ band=60 expected=60 verdict=DIFFER` rc 1 | **partial — honest**: band composes (EQ), box axis correctly refuses MATCH for an edge-overlapping bar |
| A1b same, bar inside the box (y1020..1050) | as A1a but layer y=1020 | band **60** EQ MATCH rc 0 | `box=MATCH reserved=EQ band=60 expected=60 verdict=CLEAN` rc 0; debug `MADO_BARFOOT_STATIC: monitor=M1 top=0 right=0 bottom=30 left=0 source=rules` | **yes** |
| A2 left-bar+static-left | 1920x1080; bar left w26 margin0 at x26; `addreserved, 0, 0, 26, 0`; observed [52,0,0,0] | band left = 26+26 = **52**; box x26 w1894; EQ MATCH rc 0 | `box=MATCH reserved=EQ band=52 expected=52 verdict=CLEAN` rc 0 | **yes** |
| A3 margined-bottom-bar+static-top | 1920x1080; bar bottom h30 margin4 at y1046 x4 w1912; `addreserved, 26, 0, 0, 0`; observed [0,26,0,38] | band bottom = 0+(30+4+4) = **38**; static top 26 shifts the box only (bar y1046..1076 inside y26..1080); EQ MATCH rc 0 | `box=MATCH reserved=EQ band=38 expected=38 verdict=CLEAN` rc 0 | **yes** |
| A4 static reserve exactly equal to the bar band | 3440x1440; bar top h26 margin0 at y26; `addreserved, 26, 0, 0, 0`; observed [0,52,0,0] | band = 26+26 = **52** — composition **adds** even when equal; a `max()` model would wrongly answer 26; EQ MATCH rc 0 | `box=MATCH reserved=EQ band=52 expected=52 verdict=CLEAN` rc 0 | **yes** |
| A5 static reserve larger than the monitor | 3440x1440; bar top h26 at y2000; `addreserved, 2000, 0, 0, 0`; observed [0,2026,0,0] | `apply()` → usable box y2000 h**-560**, degenerate, no bar fits → honest answers: model refusal (rc 3 stage=model) or empty-box verdict; never a clean EQ/MATCH/CLEAN | `MADO_BARFOOT: ERROR (stage=model the static reserved area leaves no usable box (3440x-560))` rc 3 | **yes** |

## Divergences (with fixture inline)

Exactly one, A1a — and it is a fixture-semantics observation, not a missed expectation:

```json
{"name":"A1a-bottombar-static-bottom","config":{"height":30,"layer":"top","position":"bottom"},
 "monitors":[{"height":1080,"name":"M1","reserved":[0,0,0,60],"scale":1.0,"transform":0,"width":1920}],
 "layers":{"M1":{"levels":{"0":[],"1":[],"2":[{"alpha":1.0,"h":30,"namespace":"waybar","pid":4242,"w":1920,"x":0,"y":1050}],"3":[]}}},
 "rules":"monitor = M1, addreserved, 0, 30, 0, 0\n"}
```
Tool: `box=DIFFER reserved=EQ band=60 expected=60 verdict=DIFFER` rc 1. Re-derived per the frozen claim's "arranged inside the static-reduced usable box": the bar at the physical edge overlaps the static strip, so box=DIFFER is the model-correct refusal; the band axis still composes correctly (60, EQ). The inside-box variant A1b (y=1020) is `MATCH EQ band=60 rc 0`. Data for the L1: in host reality a bottom waybar with static `addreserved` bottom sits at the physical edge, so that real posture scores box=DIFFER under the r79 model — a candidate follow-up case, not a round-79 defect against the frozen contract.

## Retained evidence

- Instrument re-hash: `sha256sum tools/mado-barfoot.py` → `c9aa139152643020acf27b5aef8026ae5b8a5f70372e86abb4a032c82bed86de` (== frozen r79-v1); counter `48ebfab6cc40402058d74c2f56cfe5438dd1ccefdec31bbb5510f6ca96a26cb0`.
- Frozen receipt (copied to `w1/R79ExecC1Cases/measurement-c1-r79.txt`): `MADO_R79_BARFOOT: cases=23 correct=23 mutants=12 killed=12 base_correct=18/23 carried=18/18 tool_selftest=43/43 verdict=TARGET_MET rev=5eb8f20fe291603c74973fa94cc55723ac8089a4 tool_sha256=c9aa1391…`; `MADO_R79_CONTROL: sha256=5f7ebb3c47c68dedcd113f29f63f995fccdb201e16eb949a4a450be892252eb7 carried=18/18` — matches the frozen control hash prefix in the round contract. My independent per-case runs reproduce the receipt's five `static-*` rows exactly.
- No tool installation was needed (python3 only). No pacman, no host write, no service touched. Host probes: none (all inputs synthetic fixtures).
