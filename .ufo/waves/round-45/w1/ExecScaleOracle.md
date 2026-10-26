# ExecScaleOracle — round 45 / w1

**Target.** Differential test of the C1 scale axis: `expected_scale()`
(`.ufo/waves/round-45/l1-draft/mado-monitors.py:327-338`) against a C++ transcription of Hyprland
0.56.2 (efb50993) `CMonitor::applyMonitorRule`, explicit-scale arm
(`.ufo/waves/round-45/fetch/Hyprland-Monitor.cpp:996-1050`). `g++ 16.2.1` at `/usr/bin/g++`, so no
float32 emulation was needed.

**Result: 0 divergences over 445,875 case evaluations (bit-exact `float` comparison), plus 1,999,611
predicate samples.** The 1e-4 agreement tolerance cannot flip a verdict on this axis: the algorithm
drift is 0 and the decimal round-trip of the live `scale` (shortest-round-trip `float` printing,
worst case measured 1.144e-7) is 875× below the tolerance, while a genuine candidate disagreement
would be 1/120 = 8.333e-3, i.e. 83.3× above it.

## Campaigns (3 runs, receipts in `w1/ExecScaleOracle/receipts/`)

| source | cases | divergences |
|---|---|---|
| `drive.py`: 6,488 scales (0.01 grid, 1/120 grid, .5-ties, tie±eps, 3,000 random ≤6 dp, 2,000 low) × 46 modes | 291,960 | 0 (`divergences_level1 = 0`, `divergences_level2 = 0`) |
| `sweep.py`: exact 1/120 grid k=30..360 × 445 modes | 147,295 | 0 (`mismatch_count: 0`, `nonpositive_count: 0`) |
| `probe_fallback.py`: 1/120 grid × 20 modes | 6,620 | 0 |

Case mix (`receipts/drive.txt`): `state1=283,944` corrected, `state2=1,024` untouched,
`fallback=6,992` — and the draft returned `None` on exactly those 6,992 and no others
(`py_none=6,992`). `max_value_drift=0.0`. `parse_diff_count=0`: libstdc++ `std::stof` and Python's
double-rounded `struct.pack('<f', …)` agreed bit-for-bit on all 6,488 literals.

Same predicate: `whole(x)` (draft:323) vs `x == std::round(x)` (Monitor.cpp:997) — 0 differences over
1,999,611 finite doubles with |x| ≤ 1e6 (`receipts/pred-fuzz.txt`); the plane's domain bound is
30,720. They differ only at `inf` (tool `False`, Hyprland `True`), which is unreachable: `scaleDown == 0`
needs `i == k ≤ 89`, but `d = 15` (scale 0.125, `8w` always integral) is scanned at `i = k−15` for
`30 ≤ k ≤ 104`, so the loop always breaks on a positive scale first; for `k ≥ 105` the `i = k` slot is
outside the 1..89 window. Hence the draft's `cand != 0` / `z > 0` guards and Hyprland's missing guard
never disagree (measured: 0 non-positive accepted scales in 439,255 grid cases).

## The one real defect found (scale axis, contract level — not a divergence)

The "no clean divisor" arm is a verdict blind spot. `Hyprland-Monitor.cpp:1035` sets
`m_scale = getDefaultScale();` and `getDefaultScale()` (`:1402-1420`) returns `2` (PPI > 200), `1.5`
(PPI > 140) or `1` — never the requested scale. The draft returns `None` there and the contract
(draft:73) says "none found means the scale is not compared". End-to-end witness
(`receipts/tool-false-agree.txt`, reference tool run read-only on synthetic inputs in scratch):

```
# live: width=1234 height=567 scale=1.0 ; config: monitor = DP-1, 1234x567, 0x0, 2.5
MADO_MON_OUTPUT: name="DP-1" rule=1 differ=- verdict=AGREE
MADO_MONITORS: ... agree=1 differ=0 disabled=0 verdict=OK          exit=0
```

Hyprland cannot run 2.5 on 1234x567 (it would force 1/1.5/2); the tool reports AGREE / OK / exit 0.
Same for requested 1.75, 1.8 and 2.0 on that mode. Reach: 182/6,620 probe cases (2.7%), 151/331 of
the 1/120 grid (all k ≥ 210, i.e. requested scale ≥ 1.75), 27.4% of the sweep cases. Control: the
host's own `3440x1440@100, 0x0, 1` line also prints AGREE, correctly — the witness is not a tool that
agrees with everything.

This is declared in the contract, so it is a modelling limit rather than a transcription defect; it
still means the scale field is silently unchecked exactly where Hyprland overrides the rule. Route to
the C1 owner as a decision (compare against `1|1.5|2` in the `None` arm, or emit a distinct
`not-compared` note), not as a bug in `expected_scale`.

## Files

- `w1/ExecScaleOracle/report.md` — full report with the harness source inline.
- `w1/ExecScaleOracle/{scale_oracle.cpp,drive.py,sweep.py,probe_fallback.py,pred_fuzz.py,probe_tool_agree.sh,run_all.sh,verify_quotes.sh}`
- `w1/ExecScaleOracle/receipts/{build,harness-sha256,drive,sweep,fallback,pred-fuzz,smoke,json-float-format,tool-false-agree,quotes}.txt`

No lane file outside this seat directory was touched; no compositor command was run; no tool was
installed; scratch `/fast/scratch/hyaku/mado-r45/ExecScaleOracle` removed after the receipts were
copied. Quote locators are computed by `verify_quotes.sh` into `receipts/quotes.txt`.
