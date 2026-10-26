# CritToolSemantics — C1 contract vs Hyprland 0.56.2 (efb50993)

Seat: mado round 45, w1, critic. Full findings: `.ufo/waves/round-45/w1/CritToolSemantics/findings.md`.
Receipts: `.ufo/waves/round-45/w1/CritToolSemantics/receipts/{tool-runs.txt,quote-check.sh,quote-check.txt}`.

## Verdict

The C1 contract is **substantially faithful** — 14 checked statements are exact, including rule storage
(`MonitorRuleManager.cpp:38-42`), last-match/first-empty lookup (`:96-108`), `desc:` prefix matching,
the short-vs-long description split (`Monitor.cpp:250-256`, `HyprCtl.cpp:277`), the 60 Hz default
(`MonitorRule.hpp:46`), the 89-step `k/120` search, the `< 0.25 → 1.0` scale rule, the `< 1` mode bound,
literal explicit positions, unknown-key drop and `mirrorOf`/`disabled` JSON semantics. It is **not**
correct on four points, and each of them can print a verdict Hyprland's own behaviour contradicts.

## Wrong verdicts (evidence, with the exact input)

1. **Scale integrality is computed in double; Hyprland's is float32.** Input
   `monitor = DP-1, 3440x1440@100, 0x0, 0.32` with live scale 0.32 → tool `differ=scale verdict=DIFFER`,
   exit 1 (`tool-runs.txt` R2). Hyprland: `Vector2D logicalSize = m_pixelSize / m_scale;` at
   `Monitor.cpp:996` is float32 → 10750.0 / 4500.0, both equal `round`, so the correction block at `:997`
   is never entered and `m_scale` stays 0.32 (`:992`). Same for 0.48/1920x1080 (tool E=0.5, R4),
   0.64/3440x1440 (E=0.625, R5), and the family {0.32,0.48,0.64,0.96,1.28,1.92,2.56,3.84} on ten common
   modes — 38 of the 54 computed `(scale,w,h)` divergences over 2-decimal scales 0.25-4.00; the other 16
   are the reverse direction (0.3/0.6/1.2/2.4) and depend on `Vector2D`'s unpublished division precision.
   Common 1.25/1.5/1.6/1.75/2.0 are unaffected.
2. **`transform` modifier grammar.** Input `monitor = DP-1, transform, 07` after a normal rule, live
   transform 7 → `badrules=1`, rule keeps transform 0, `differ=transform verdict=DIFFER` (R6); the control
   `transform, 7` is AGREE (R7). Hyprland: `isNumber("07")` → `stoi` → `clamp(0,7)` passes
   (`Parser.cpp:214-221`), the named rule is copied with transform 7 and re-added
   (`ConfigManager.cpp:1310-1314`). `transform, -0` is the same class (R8). The drop is **ungated**:
   `badrules` is not one of the top-verdict gates (`mado-monitors.py:434`), so the run still claims DIFFER.
3. **`addreserved` numbers are `std::stoi`, not `-?[0-9]{1,6}`.** Input `addreserved, +5, 0, 0, 0` with an
   empty-selector fallback → `badrules=1`, no rule → the output falls to the fallback rule and the tool
   prints DIFFER (R9). Hyprland parses `+5` as 5 (`ConfigManager.cpp:1323`) and, with no such rule, adds a
   default rule (`:1341`); the exact Hyprland-equivalent input `addreserved, 5` yields AGREE (R10). Also
   ungated.
4. **"No clean divisor" is skipped, not reported.** Input scale `14.166667` on 1920x1200, live scale 1 →
   the tool drops the scale field from the comparison and prints **AGREE**, exit 0 (R15). Hyprland's search
   window `[1611,1789]` holds no divisor of both sizes, so it applies `getDefaultScale()`
   (`Monitor.cpp:1029-1036`, `:1402-1417`), which is 1, 1.5 or 2 — never 14.166667. The docstring declares
   the skip, but the declaration is wrong about what Hyprland does.

Conditional, unproven by the pins: the mirror target is resolved by the monitor **query**
(`Monitor.cpp:1335 configString(mirrorOf)`), not by name equality; the tool matches `name` only, so
`mirror, desc:Acme` prints `differ=mirror` (R18). Whether `configString` accepts `desc:`/description forms
needs `State::MonitorState`/`Desktop::Query`, which is **not** among the frozen pins → [INFERENCE].

## Missing verdicts (gated, no false claim)

Hyprland parses mode/position/scale with `stoi`/`stof` (`Parser.cpp:124-138,175-183,197-205`) and still
adds the rule when a field fails, whereas the contract's regexes refuse the line. `@1000` and `@1e2` both
reach `unsupported=1 … verdict=NOT_COMPARED`, exit 5 (R12/R13) — safe, but the docstring presents those
regexes as Hyprland's grammar, which they are not. A CRLF config makes every line `unsupported` (R14) even
though hyprutils' `trim` strips `\r`. The valid `< 0.25` sentence **is** exact (`Parser.cpp:203-206`).

## Documented limits whose disclosure is incomplete

`debug:disable_scale_checks` (`Monitor.cpp:721,997`) is not mentioned, and it invalidates every corrected
expectation; `hyprctl monitors -j` omits disabled outputs (`HyprCtl.cpp:321-339`), so a `disable` rule
vanishes and the top verdict stays OK (R16 vs R17) — the contract shows `monitors all -j` in usage but never
states the precondition; vrr/bitdepth/cm/sdr*/icc are consumed but never compared; the wlr-output-management
override mutates the rule before it is applied (`MonitorRuleManager.cpp:46-80`), so the printed rule is not
the applied rule (the DIFFER itself stays honest); the hardcoded no-rule fallback (`:108-115`) means
Hyprland's UNRULED output is still driven by a rule — the tool's UNRULED is a config-only statement and the
docstring should say so.

## Impacted axes

- **Operability (C1):** the tool's output is the claim's after-state, so a false DIFFER (1) and a false
  AGREE (4) are operability defects, not cosmetic ones. The counter's 49 fixtures encode the same
  double-precision scale model and the same one-digit transform grammar as the reference, so 49/49 TARGET_MET
  cannot detect any of them (registration residual: "the fixtures are the contract's cases, not Hyprland's
  runtime" — now demonstrated).
- **Coverage (C2):** unaffected in isolation, but if the entry states the correction step as a double test
  or the one-digit transform grammar, it repeats the same error; the entry's §4 should cite
  `Monitor.cpp:996` (float32) and `Parser.cpp:214-221` (isNumber/stoi/clamp) verbatim.
- **Registry/pins:** no new rows needed; the four findings are inside held pin scopes (S302-S310 would cover
  them if the L1 chooses to record them).

## Smallest safe correction (ranked, all inside the docstring + reference, no new surface)

1. `expected_scale`: run the integrality tests on float32 (`f32(w / f32(s))` vs `f32(round(...))`) for the
   first test and each `k/120` candidate; add fixtures 0.32/3440x1440 and 0.48/1920x1080.
2. `transform_value` (and the modifier path): accept the integer forms `isNumber` accepts (`-` only at
   index 0, digits only) and clamp 0..7, i.e. `07`/`-0` are valid; anything else stays `badrules`.
3. No-divisor scale: never print AGREE with the scale field dropped — either compare against {1, 1.5, 2} or
   route the run to NOT_COMPARED.
4. `addreserved`: accept `stoi`-prefix integers (`+5`, `5.5`, `10abc`) so the line is modelled, not dropped.
5. Docstring text: state that `mirror` is resolved by the monitor query (or "name only"), that `monitors all
   -j` is required for DISABLED, that vrr/bitdepth/cm/sdr*/icc are consumed but not compared, and that
   `debug:disable_scale_checks` disables the correction.

None of these changes the top-verdict grammar or the output format; 1-4 change only accepted inputs and the
scale expectation, so the counter re-scores cleanly if the fixtures are extended.

## Tool state

Nothing installed, nothing on PATH, no package transaction, no host read, no compositor command, no Wayland
client. All work in `/fast/scratch/hyaku/mado-r45/CritToolSemantics/` (removed after the receipts were
copied here). Wrote only this file, `findings.md` and `receipts/` inside
`.ufo/waves/round-45/w1/CritToolSemantics/`.

Report: .ufo/waves/round-45/w1/CritToolSemantics.md
