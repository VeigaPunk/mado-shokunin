# R79ExecC1Cases — independent re-derivation of the five new C1 expectations

Derived 2026-11-04 from source rules only, before any tool run:
- S465 `src/output/Monitor.cpp` (`fetch/S465.bin`):654 `m_reservedArea.setStatic(m_activeMonitorRule.m_reservedArea)` — a monitor's static reserved area is its (last matching) monitor rule's reserve; :1772-1773 `logicalBoxMinusReserved() { return m_reservedArea.apply(logicalBox()); }`.
- S466 `src/desktop/reserved/ReservedArea.cpp` `apply()`: `x += topLeft.x; y += topLeft.y; w -= topLeft.x + bottomRight.x; h -= topLeft.y + bottomRight.y` — usable box = logical box inset by (left, top, right, bottom); **no clamping** (only the initial static values clamp at ≥0 in the constructor).
- Arg order of the rule: `monitor = NAME, addreserved, TOP, BOTTOM, LEFT, RIGHT`; hyprctl `reserved` array order is `[left, top, right, bottom]` (carried cases confirm: `bottom-bar` rule-free bottom 30 → `[0,0,0,30]`).
- Last matching rule for a monitor wins; a rule binds only its named monitor (`m_activeMonitorRule` is selected per monitor).
- Band convention (grounded in carried cases, not the tool): extent = size + near margin + far margin (`top-margin-asym` 10+30+2=42; `left-margin` 6+40+6=52; `right-zero-margin` 40). Expected band on the bar's edge = `static[edge] + extent`.
- Verdicts: EQ/DIFFER compare computed band to observed `reserved[edge]`; exclusive=false → bar reserves nothing → NOT_APPLIED (would-be band still printed as `expected`); rc 0 clean, 1 DIFFER, 3 model refusal, 2 setup.

## Derivations (control cases 18-22)

| # | case | usable box (M1) | declared box | expected band | reserved verdict / rc |
|---|------|-----------------|--------------|---------------|----------------------|
| 18 | static-composed | x0 y26 w3440 h1414 (static top 26) | bar x4 y30 w3432 h26 | 26 + (26+4+4) = **60** | **EQ**, rc 0, MATCH, CLEAN |
| 19 | static-other-edge | x40 y0 w3400 h1440 (static left 40) | bar x40 y0 w3400 h26 | 0 + 26 = **26** (left 40 moves the box, not the top band) | **EQ**, rc 0, MATCH, CLEAN |
| 20 | static-exclusive-false | x0 y26 w3440 h1414 (static top 26) | bar x0 y26 w3440 h26 | would-be 26+26=**52** printed, bar reserves nothing | **NOT_APPLIED**, rc 0, MATCH, CLEAN |
| 21 | static-last-wins (`--monitor M1`) | x0 y26 w3440 h1414 (M1's newest rule 26; M2's rule irrelevant) | bar x0 y26 w3440 h26 | 26 + 26 = **52** | **EQ**, rc 0, MATCH, CLEAN |
| 22 | static-source-refused | n/a — `source =` line is not a monitor rule; rules tree unresolvable | n/a | n/a | **refusal rc 3, stage=model, error=true** |

All five derivations were written before reading or running `tools/mado-barfoot.py`.

## Adversarial fixtures (own, scratch) — correct answers derived from the same sources

| fixture | setup | correct answer from sources |
|---------|-------|------------------------------|
| A1 bottom-bar+static-bottom | 1920x1080, bar bottom h30 margin0, rule `addreserved,0,30,0,0` | band bottom = 30+30 = **60**; box h1050; EQ, MATCH, rc 0 |
| A2 left-bar+static-left | 1920x1080, bar left w26 margin0, rule `addreserved,0,0,26,0` | band left = 26+26 = **52**; box x26 w1894; EQ, MATCH, rc 0 |
| A3 margined-bottom-bar+static-top | 1920x1080, bar bottom h30 margin4, rule `addreserved,26,0,0,0` | band bottom = 0+(30+4+4) = **38** (static top 26 shifts box only); box y26 h1054; EQ, MATCH, rc 0 |
| A4 static==bar-band | 3440x1440, bar top h26 margin0, rule `addreserved,26,0,0,0` | band top = 26+26 = **52** (composition adds even when equal — `max()` would wrongly say 26); EQ, MATCH, rc 0 |
| A5 static>monitor | 3440x1440, bar top h26, rule `addreserved,2000,0,0,0` | apply() gives usable box y2000 h**-560** — degenerate, no bar fits; honest answers: model refusal (rc 3, stage=model) or empty-box/NOT_ARRANGEABLE verdict; never a clean EQ/MATCH/CLEAN |
