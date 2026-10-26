# ExecScaleOracle — differential test: Hyprland scale correction vs `expected_scale()`

Round 45 / w1 / seat `ExecScaleOracle`. Target: the C1 scale axis of
`.ufo/waves/round-45/l1-draft/mado-monitors.py` (`expected_scale`, draft:327-338) against Hyprland
0.56.2 (efb50993) `CMonitor::applyMonitorRule`, explicit-scale branch
(`.ufo/waves/round-45/fetch/Hyprland-Monitor.cpp:996-1050`).

**Verdict: 0 divergences over 445,875 case evaluations (+1,999,611 predicate samples).** The
transcription is bit-exact on every input the contract can express, so the 1e-4 agreement tolerance
cannot flip a verdict. What *can* and *does* flip a verdict is the separate `None` arm ("no clean
divisor"), which makes the tool skip the scale field exactly where Hyprland overrides the rule with
`getDefaultScale()` — a false AGREE, demonstrated end to end below.

---

## 1. What was transcribed

`applyMonitorRule` (explicit-scale branch, `autoScale == false`), kept literal:

| Hyprland | line | transcription |
|---|---|---|
| `Vector2D logicalSize = m_pixelSize / m_scale;` | 996 | double / (float promoted) |
| `logicalSize.x != std::round(logicalSize.x) \|\| ...` | 997 | `x != std::round(x)` per component (exact integrality) |
| `float searchScale = std::round(m_scale * 120.0);` | 1001 | double product, `std::round`, then **float** store |
| `double scaleZero = searchScale / 120.0;` | 1004 | float → double division |
| `if (logicalZero == logicalZero.round())` | 1007 | exact Vector2D equality |
| `for (size_t i = 1; i < 90; ++i)` | 1010 | same 1..89 window, up tested before down |
| `double scaleUp = (searchScale + i) / 120.0;` | 1011 | **`searchScale + i` evaluated in float** (float × size_t promotion), then double division |
| `m_scale = searchScale;` | 1048 | float result |
| `m_scale = getDefaultScale();` | 1035 | returned as state 0 (not a value) |

Dropped, as instructed: `autoScale` (`m_scale = getDefaultScale();` at :990), the notification
(:1039-1046), and `m_size = (xfmd / m_scale).round()` (:1059).

Faithful points that matter and are easy to lose: (a) `m_scale` and `searchScale` are `float`
(`Hyprland-MonitorRule.hpp:45`); (b) every comparison in the search is between **double** quotients
of a double divisor; (c) the search has **no** `z > 0` guard, so `scaleDown == 0` would divide by
zero and `std::round(inf) == inf` would accept scale 0 — the draft guards with `cand != 0` and `z > 0`.

## 2. Campaigns

Built with `g++ 16.2.1` (`-std=c++23 -O0 -ffp-contract=off -fno-fast-math`), so no float32
emulation was needed. All builds and case files under `/fast/scratch/hyaku/mado-r45/ExecScaleOracle`
(deleted at the end); receipts in `receipts/`.

| campaign | cases | divergence |
|---|---|---|
| `drive.py` — 6,488 distinct scales × 46 pixel modes, 8 families (0.01 grid, 6-dp k/120, exact 1/120, .5-ties, tie±eps, 3,000 random ≤6 dp, 2,000 low scales) | 291,960 | **0** (level 1 and level 2) |
| `sweep.py` — exact 1/120 grid k=30..360 × 445 pixel modes (46 curated + 400 random) | 147,295 | **0** |
| `probe_fallback.py` — 1/120 grid × 20 modes, fallback arm census | 6,620 | **0** |
| `pred_fuzz.py` — integrality predicate `whole(x)` vs `x == std::round(x)` | 1,999,611 finite doubles | **0** |

Comparison is on the raw IEEE-754 bit pattern of the resulting `float` (`%08x` of the float), not on
a tolerance. Case statistics from `drive.py` (`receipts/drive.txt`):
`state1=283,944` corrected, `state2=1,024` untouched (requested scale already integral),
`fallback=6,992`; the draft returned `None` on **exactly** those 6,992 and on no others
(`py_none=6,992`), `max_value_drift=0.0`, `parse_diff_count=0` (libstdc++ `std::stof` and Python's
double-rounded `struct.pack('<f', …)` produced the same float for all 6,488 literals).

`probe_fallback.py` (`receipts/fallback.txt`): the arm is reached only for `k ≥ 210`, i.e. requested
scale `≥ 1.75`; `sweep.py` agrees — `k_with_fallback = {min: 210, max: 360, count: 151}`,
`k_never_fallback.max = 209`, `mismatch_count = 0`, `nonpositive_count = 0`.

### Why the zero/negative branches are unreachable (proof, then measured)

`scaleDown == 0` needs `i == k` with `i ≤ 89`, i.e. `k ≤ 89`. But `d = 15` is always in the scanned
window at `i = k − 15` for `30 ≤ k ≤ 104`, and `d = 15` gives the exactly-representable scale
`0.125` with `w / 0.125 = 8w` integral for every integer `w`. The loop therefore always breaks on a
positive scale before `i = k` (for `k ≥ 105`, `i = k > 89` is out of the window entirely). Likewise
`d = 120` yields exactly `1.0` for `31 ≤ k ≤ 119` (up, `i = 120−k`) and `121 ≤ k ≤ 209` (down,
`i = k−120`), so the no-divisor arm is impossible for `k ≤ 209` — matching the measurement.
Consequently the draft's `cand != 0` / `z > 0` guards and Hyprland's missing guard never disagree.
Measured: 0 non-positive accepted scales in 147,295 sweep cases and 0 in 291,960 drive cases.

## 3. Divergences

**None.** Every divergence list is empty (`receipts/drive.txt`: `divergences_level1 = 0`,
`divergences_level2 = 0`; `receipts/sweep.txt`: `mismatches: []`).

The one behavioural difference found is not a value divergence but a *classification* difference:

- `Hyprland-Monitor.cpp:1035` — `m_scale = getDefaultScale();` — the arm taken when no 1/120
  candidate divides the pixel size. `getDefaultScale()` (`Hyprland-Monitor.cpp:1402-1420`) returns
  `2` when `PPI > 200`, `1.5` when `PPI > 140`, else `1`.
- The draft returns `None` there and the contract says (draft:73) "none found means the scale is not
  compared."

Both sides agree the correction failed; the tool then stops watching the field.

## 4. Can the 1e-4 tolerance flip a verdict?

**No — and the tolerance is not what protects the scale axis.**

1. Algorithm divergence is **0** (bit-identical floats), so the only residual gap is the decimal
   round-trip of the live value. `hyprctl` prints `m_scale` with `std::format("{}", float)` in the
   JSON template at `Hyprland-HyprCtl.cpp:254` (`"scale": {},`) — libstdc++ emits the **shortest
   round-tripping decimal for `float`**, which the tool re-parses as a double. Measured worst case
   over all candidate scales in [0.25, 3.0]: **1.144e-7** (`float 2.11999989` → `"2.12"` →
   `2.1200000000000001`, `receipts/json-float-format.txt`). The tolerance is 875× larger.
2. The smallest possible *real* disagreement is one candidate step: `1/120 = 8.333e-3`, which is
   **83.3×** the tolerance. So the tolerance can never absorb a wrong candidate, and no wrong
   candidate exists.
3. Therefore the tolerance is safe, and the reachable mis-verdict has a different cause: the
   `None` arm skips the field entirely, so **any** live scale passes.

**End-to-end witness** (`receipts/tool-false-agree.txt`, reference tool run read-only against
synthetic inputs in scratch, nothing installed):

```
$ mado-monitors.py --monitors mons.json --config cfg-2.5.conf     # live width=1234 height=567 scale=1.0
MADO_MON_RULE: n=1 sel="DP-1" mode=1234x567@60.00 pos=0x0 scale=2.5000 transform=0 mirror=- disabled=false
MADO_MON_OUTPUT: name="DP-1" rule=1 differ=- verdict=AGREE
MADO_MONITORS: lines=1 rules=1 v2=0 unsupported=0 badrules=0 outputs=1 matched=1 unruled=0 agree=1 differ=0 disabled=0 verdict=OK
exit=0
```

On a 1234x567 mode Hyprland can only run scale 1, 1.5 or 2 for a requested 2.5 — it replaces the
rule scale with `getDefaultScale()` — while the tool reports AGREE / OK / exit 0. The same holds for
requested 1.75, 1.8 and 2.0 on that mode (`cfg-1.75`, `cfg-1.8`, `cfg-2.0` in the receipt). The
control (the host's own `3440x1440@100, 0x0, 1` line) also prints AGREE, correctly, so the witness is
not a tool that agrees with everything.

**Scope:** 182/6,620 = 2.7% of the probe grid; 151/331 of the 1/120 grid scales (all ≥ 1.75);
27.4% of the `sweep.py` cases. This is the only scale-path false-AGREE mechanism I found, and it is
declared in the contract, so it is a modelling limit rather than a transcription defect — but it is
worth naming on the C1 scorecard because it silently disables the scale comparison for exactly the
rule scales an operator is most likely to have got wrong.

## 5. Harness

All files co-located in this directory; `run_all.sh` rebuilds and regenerates every receipt.

| file | role | sha256 (first 16) |
|---|---|---|
| `scale_oracle.cpp` | C++ transcription (below, full source) | `7f9afa7d45065aac` |
| `drive.py` | main campaign (below, full source) | `dc6b77e9a8b5f8bc` |
| `sweep.py` | exact-1/120-grid reachability sweep | `be451205a30df7e0` |
| `probe_fallback.py` | no-divisor arm census | `fb2e054749cf03c4` |
| `pred_fuzz.py` | predicate equivalence fuzz | `d1779ebe61298e73` |
| `probe_tool_agree.sh` | false-AGREE witness through the reference tool | — |
| `verify_quotes.sh` | computes every quote locator used here | — |

### `scale_oracle.cpp` (full)

```cpp
// scale_oracle.cpp - literal transcription of Hyprland 0.56.2 (efb50993)
// src/helpers/Monitor.cpp CMonitor::applyMonitorRule, explicit-scale branch
// (.ufo/waves/round-45/fetch/Hyprland-Monitor.cpp:989-1051).
//
// Kept: float m_scale and float searchScale, double Vector2D components,
// std::round (half away from zero), the `float + size_t` promotion in
// (searchScale +- i), the 1..89 search, the missing z>0 guard, and the
// "no clean divisor" fallback (autoScale == false -> getDefaultScale()).
// Dropped: autoScale branch (m_scale = getDefaultScale()) and the notification.
//
// stdin : one case per line, "S W H"  (S decimal text parsed with std::stof,
//         as CMonitorRuleParser::parseScale does; W,H integers)
// stdout: "SBITS RBITS FOUND" per case, lowercase hex 8 digits.
//         SBITS = bits of the parsed float rule scale, RBITS = bits of the
//         resulting m_scale, FOUND = 1 when a corrected scale was selected,
//         0 when the "failed to find a clean divisor" fallback ran (so RBITS is
//         getDefaultScale(), not modelled here), 2 when S was integral from the
//         start (m_scale untouched).
#include <cmath>
#include <cstdint>
#include <cstdio>
#include <cstring>
#include <string>

struct V2 {
    double x, y;
};

static V2 vdiv(V2 a, float s) { return V2{a.x / (double)s, a.y / (double)s}; }
static V2 vdiv(V2 a, double s) { return V2{a.x / s, a.y / s}; }
static V2 vround(V2 a) { return V2{std::round(a.x), std::round(a.y)}; }
static bool veq(V2 a, V2 b) { return a.x == b.x && a.y == b.y; }

struct Res {
    float    scale;
    int      state; // 1 corrected, 2 untouched, 0 fallback
};

static Res apply_scale(float m_scale, double wx, double hy) {
    V2 pixelSize{wx, hy}; // m_pixelSize = m_size, exact mode resolution
    V2 logicalSize = vdiv(pixelSize, m_scale);

    if (logicalSize.x != std::round(logicalSize.x) || logicalSize.y != std::round(logicalSize.y)) {
        float    searchScale = std::round(m_scale * 120.0);
        bool     found       = false;
        double   scaleZero   = searchScale / 120.0;
        V2       logicalZero = vdiv(pixelSize, scaleZero);

        if (veq(logicalZero, vround(logicalZero)))
            m_scale = scaleZero;
        else {
            for (size_t i = 1; i < 90; ++i) {
                double scaleUp   = (searchScale + i) / 120.0;
                double scaleDown = (searchScale - i) / 120.0;

                V2 logicalUp   = vdiv(pixelSize, scaleUp);
                V2 logicalDown = vdiv(pixelSize, scaleDown);

                if (veq(logicalUp, vround(logicalUp))) {
                    found       = true;
                    searchScale = scaleUp;
                    break;
                }
                if (veq(logicalDown, vround(logicalDown))) {
                    found       = true;
                    searchScale = scaleDown;
                    break;
                }
            }
            if (!found)
                return Res{m_scale, 0}; // autoScale == false -> getDefaultScale()
            m_scale = searchScale;
        }
        return Res{m_scale, 1};
    }
    return Res{m_scale, 2};
}

static uint32_t bits(float f) {
    uint32_t u;
    std::memcpy(&u, &f, 4);
    return u;
}

int main() {
    char sbuf[64];
    double w = 0, h = 0;
    while (std::scanf("%63s %lf %lf", sbuf, &w, &h) == 3) {
        float s = std::stof(std::string(sbuf));
        Res   r = apply_scale(s, w, h);
        std::printf("%08x %08x %d\n", bits(s), bits(r.scale), r.state);
    }
    return 0;
}
```

### `drive.py` (full)

```python
#!/usr/bin/env python3
"""drive.py - differential driver: C++ transcription of Hyprland 0.56.2 applyMonitorRule
explicit-scale correction vs expected_scale() of the round-45 l1 draft tool.

Case protocol with the binary: "S W H" -> "SBITS RBITS STATE".
STATE 1 = corrected scale selected, 2 = m_scale untouched (positive branch),
0 = "failed to find a clean divisor" fallback (autoScale == false -> getDefaultScale()).

Level 1 (algorithm) : expected_scale(f32(cpp_parsed_s), w, h) vs C++ bits.   s identical on both sides.
Level 2 (end-to-end): expected_scale(f32(struct(text)), w, h) vs C++ bits.   models the tool's own parse.
"""
import importlib.util
import json
import math
import random
import struct
import subprocess
import sys

DRAFT = "/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-45/l1-draft/mado-monitors.py"
BIN = sys.argv[1]
OUT = sys.argv[2]

spec = importlib.util.spec_from_file_location("mado", DRAFT)
mado = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mado)
expected_scale = mado.expected_scale


def f32_from_bits(b):
    return struct.unpack("<f", struct.pack("<I", b))[0]


def bits_of(x):
    return struct.unpack("<I", struct.pack("<f", x))[0]


def f32_of_text(t):
    return struct.unpack("<f", struct.pack("<f", float(t)))[0]


SIZES = [
    (640, 480), (800, 600), (1024, 768), (1024, 600), (1280, 720), (1280, 800), (1280, 1024), (1280, 480),
    (1366, 768), (1365, 767), (1440, 900), (1440, 2560), (1600, 900), (1600, 1200), (1680, 1050),
    (1920, 1080), (1919, 1079), (1920, 1200), (1920, 1440), (2048, 1152), (2160, 1440), (2560, 1080),
    (2560, 1440), (2560, 1600), (2560, 1920), (2880, 1800), (3200, 1800), (3440, 1440), (3441, 1439),
    (3840, 1080), (3840, 1600), (3840, 2160), (3840, 2400), (4096, 2160), (4096, 2304), (5120, 1440),
    (5120, 2160), (5120, 2880), (6016, 3384), (7680, 4320), (1080, 1920), (768, 1366), (1000, 1000),
    (1234, 567), (999, 777),
]

rng = random.Random(20261026)

scales = []          # (text, family)


def add(text, fam):
    scales.append((text, fam))


# A: 0.25 .. 3.00 in 0.01
for i in range(276):
    add("%.2f" % (0.25 + 0.01 * i), "A-0.01")
# B: k/120 as a 6-decimal literal a user could type
for k in range(30, 361):
    add("%.6f" % (k / 120.0), "B-k/120-6dp")
# D: f32 nearest of k/120, shortest decimal that round-trips
for k in range(30, 361):
    v = f32_of_text("%.9f" % (k / 120.0))
    for d in range(1, 10):
        t = "%.*f" % (d, k / 120.0)
        if f32_of_text(t) == v:
            break
    add(t, "D-1/120-exact")
# E: exact .5 ties in the *120 rounding
for m in range(30, 360):
    add("%.6f" % ((m + 0.5) / 120.0), "E-tie")
# F: either side of the tie
for m in range(30, 360, 3):
    add("%.7f" % ((m + 0.4999999) / 120.0), "F-tie-eps-down")
    add("%.7f" % ((m + 0.5000001) / 120.0), "F-tie-eps-up")
# C: random <= 6 decimals, full range
for _ in range(3000):
    add("%.6f" % rng.uniform(0.25, 3.0), "C-random")
# G: low scales (k <= 89) where the down-candidate reaches 0 and goes negative
for _ in range(2000):
    add("%.6f" % rng.uniform(0.25, 0.75), "G-low")

cases = []
for text, fam in scales:
    for w, h in SIZES:
        cases.append((text, w, h, fam))

inp = "".join("%s %d %d\n" % (t, w, h) for t, w, h, _ in cases)
proc = subprocess.run([BIN], input=inp, capture_output=True, text=True, check=True)
lines = proc.stdout.split("\n")
assert len(lines) - 1 == len(cases), (len(lines), len(cases))

div1, div2, parse_diff = [], [], []
stats = {"cases": len(cases), "state1": 0, "state2": 0, "fallback": 0,
         "py_none": 0, "cpp_nonpositive": 0, "py_nonpositive": 0, "nonpositive_both": 0}
max_drift = 0.0
for (text, w, h, fam), ln in zip(cases, lines):
    sb, rb, st = ln.split()
    sb, rb, st = int(sb, 16), int(rb, 16), int(st)
    s_cpp = f32_from_bits(sb)
    s_py = f32_of_text(text)
    if bits_of(s_py) != sb:
        parse_diff.append({"text": text, "cpp_bits": "%08x" % sb, "py_bits": "%08x" % bits_of(s_py)})
    cpp_val = f32_from_bits(rb)
    e1 = expected_scale(s_cpp, w, h)     # level 1: identical s
    e2 = expected_scale(s_py, w, h)      # level 2: tool's own parse
    stats["state1" if st == 1 else "state2" if st == 2 else "fallback"] += 1
    if e1 is None:
        stats["py_none"] += 1
    if st != 0 and cpp_val <= 0:
        stats["cpp_nonpositive"] += 1
    if e1 is not None and e1 <= 0:
        stats["py_nonpositive"] += 1
    if st != 0 and cpp_val <= 0 and e1 is not None and e1 <= 0:
        stats["nonpositive_both"] += 1
    if st == 0:
        if e1 is not None:
            div1.append({"text": text, "s": s_cpp, "w": w, "h": h, "fam": fam, "kind": "cpp-fallback-vs-py",
                         "cpp": "getDefaultScale()", "py": e1})
    else:
        if e1 is None:
            div1.append({"text": text, "s": s_cpp, "w": w, "h": h, "fam": fam, "kind": "cpp-value-vs-py-none",
                         "cpp": cpp_val, "py": None})
        elif bits_of(cpp_val) != bits_of(e1):
            d = abs(cpp_val - e1)
            max_drift = max(max_drift, d)
            div1.append({"text": text, "s": s_cpp, "w": w, "h": h, "fam": fam, "kind": "value-mismatch",
                         "cpp": cpp_val, "py": e1, "delta": d})
    if e2 is None:
        if st != 0:
            div2.append({"text": text, "w": w, "h": h, "fam": fam, "kind": "cpp-value-vs-py-none"})
    elif st != 0 and bits_of(cpp_val) != bits_of(e2):
        div2.append({"text": text, "w": w, "h": h, "fam": fam, "kind": "value-mismatch",
                     "cpp_bits": "%08x" % rb, "py_bits": "%08x" % bits_of(e2), "s_py_bits": "%08x" % bits_of(s_py)})

# --- tolerance analysis ---------------------------------------------------
# Spacing between adjacent admissible scales is 1/120; the live `scale` field is a float
# printed by std::format("{}") (shortest round-trip decimal for float), so the tool's
# parsed double can drift from the true float value.
def shortest_repr(v):
    for d in range(1, 10):
        t = "%.*g" % (d, v)
        if f32_of_text(t) == v:
            return t
    return "%.9g" % v


worst_repr = (0.0, None)
for k in range(30, 361):
    v = f32_of_text("%.9f" % (k / 120.0))
    t = shortest_repr(v)
    d = abs(float(t) - v)
    if d > worst_repr[0]:
        worst_repr = (d, (t, "%.9g" % v))
for i in range(276):
    v = f32_of_text("%.2f" % (0.25 + 0.01 * i))
    t = shortest_repr(v)
    d = abs(float(t) - v)
    if d > worst_repr[0]:
        worst_repr = (d, (t, "%.9g" % v))

res = {
    "stats": stats,
    "divergences_level1": div1,
    "divergences_level2": div2,
    "parse_diff_count": len(parse_diff),
    "parse_diff_examples": parse_diff[:5],
    "max_value_drift": max_drift,
    "candidate_spacing": 1.0 / 120.0,
    "tolerance": 1e-4,
    "worst_float_repr_drift": {"abs": worst_repr[0], "example": worst_repr[1]},
    "families": sorted({f for _, f in scales}),
    "distinct_scales": len(scales),
}
with open(OUT, "w") as fh:
    json.dump(res, fh, indent=1)
print(json.dumps({k: v for k, v in res.items() if not k.startswith("divergences")}, indent=1))
print("divergences_level1 =", len(div1))
print("divergences_level2 =", len(div2))
for d in div1[:10]:
    print("DIV1", d)
```

`sweep.py`, `probe_fallback.py`, `pred_fuzz.py`, `probe_tool_agree.sh` and `verify_quotes.sh` are in
this directory verbatim; the sha256 receipt is `receipts/harness-sha256.txt`.

## 6. Receipts

`receipts/`: `build.txt`, `harness-sha256.txt`, `drive.txt`, `sweep.txt`, `fallback.txt`,
`pred-fuzz.txt`, `smoke.txt`, `json-float-format.txt`, `tool-false-agree.txt`, `quotes.txt`.
Nothing was written outside this seat directory and `/fast/scratch/hyaku/mado-r45/ExecScaleOracle`
(scratch removed at the end). No compositor call was made and no tool was installed.
