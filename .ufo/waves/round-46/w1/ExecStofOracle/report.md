# ExecStofOracle — scroll-factor arithmetic: `std::stof` + `std::clamp` + `std::format("{:.2f}")` vs the reference

Round 46 / w1, seat `ExecStofOracle`, 2026-10-26. Attacks the C1 claim's mouse half: the reference
`read_float()` + `"%.2f"` model in `.ufo/waves/round-46/l1-draft/mado-devices.py` against the real
Hyprland 0.56.2 parse/print chain for `device[name]:scroll_factor`.

**Verdict.** `59 394` cases, `2 871` verdict divergences.
For every ordinary decimal (1–7 places, halves at the third decimal, `repr()` round trips, long digit
strings, whitespace): **`47 697` / `47 697` bit-identical, zero divergence**. The two stages that can
never diverge are (a) finite `std::format("{:.2f}", float)` vs `"%.2f"` — `2 391 762` float32 values,
`0` mismatches — and (b) the reported-value round trip (`0` failures).
Every divergence comes from the *parse* model, and they fall into 7 classes. Six of them flip a
per-mouse `AGREE`/`DIFFER` line and/or the top verdict; the error is **one-sided**: reported
`scrollFactor` is ground truth read from the same value Hyprland stored, so the reference can only
report a false `DIFFER` / false `NOT_COMPARED` / hard `SETUP` failure, never a false `AGREE`.
The one class reachable from realistic input is D1 (>= 19-significant-digit decimals); the rest need
hex floats, `inf`/`nan` spellings, or subnormal/overflowing magnitudes.

## 1. The reproduced chain (all line numbers verified with `grep -n` on the pins)

| stage | source | behaviour |
|---|---|---|
| trim RHS | `fetch/hyprlang-config.cpp:723` | `RHS = trim(line.substr(equalsPos + 1))` |
| parse | `fetch/hyprlang-config.cpp:465-471` | `try { setFrom(std::stof(value)); } catch (std::exception&) { setError; return; }` |
| mark set | `fetch/hyprlang-config.cpp:513` | `m_bSetByUser = true` — **after** the switch, so a throwing parse leaves the key unset |
| guard | `fetch/Hyprland-ConfigManager.cpp:1125` | `deviceConfigExplicitlySet` = `getSpecialConfigValuePtr("device",val,dev) != nullptr && m_bSetByUser` |
| read | `fetch/Hyprland-ConfigManager.cpp:1139` | `getDeviceFloat` → `std::any_cast<Hyprlang::FLOAT>` (a `float`) |
| store | `fetch/Hyprland-InputManager.cpp:1379-1382` | `m_scrollFactor = std::clamp(getDeviceFloat(...), 0.F, 100.F)` else `std::nullopt` |
| print | `fetch/Hyprland-HyprCtl.cpp:770,773` | `"scrollFactor": {:.2f}` with `m->m_scrollFactor.value_or(-1)` |

Note the guard: a failed float parse yields `nullopt`, i.e. the field prints `-1.00`, and the global
`input:scroll_factor` fallback is never consulted (it is only read when the device block *did* set the
key). The reference's contract says the same (draft `mado-devices.py:12-13`), so that part is aligned.

## 2. Harness

Full copies next to this report in `receipts/`, hashes in `receipts/sha256.txt`.

### 2.1 `stmt.cpp` — the C++ side, exactly the production types

```cpp
#include <algorithm>
#include <bit>
#include <cstdint>
#include <cstring>
#include <format>
#include <iostream>
#include <optional>
#include <string>

int main() {
    std::string line;
    while (std::getline(std::cin, line)) {
        std::optional<float> scroll;                 // m_scrollFactor
        std::string          err;
        try {
            scroll = std::clamp(std::stof(line), 0.F, 100.F);   // hyprlang parse + std::clamp
        } catch (const std::invalid_argument&) { err = "invalid_argument";
        } catch (const std::out_of_range&)     { err = "out_of_range";
        } catch (const std::exception& e)      { err = std::string("other:") + e.what(); }
        if (!scroll) { std::cout << "UNSET\t" << err << "\t-\n"; continue; }
        // HyprCtl prints the optional<float> via value_or(-1)
        std::string printed = std::format("{:.2f}", scroll.value_or(-1));
        std::cout << "SET\t" << std::format("{:08x}", std::bit_cast<uint32_t>(*scroll)) << "\t"
                  << printed << "\n";
    }
}
```

### 2.2 `diff.py` — the comparison

Each side gets the text its own pipeline receives (hyprlang `trim` vs the reference's
`rhs.strip(WS)`; the two differed on 4 of 59 394 cases, all `\v`/`\f`, and no verdict changed).
Then the two meet at the dump, exactly as the reference does it:

```python
        cpp_text = t.strip(HYPR_TRIM)          # hyprlang-config.cpp:723
        kind, ref_raw = ref.read_float(text.strip(WS))   # reference contract
        exp = min(max(ref_raw, 0.0), 100.0) if kind == "ok" else -1.0
        real_field = printed if cpp_set else "-1.00"      # value_or(-1)
        broken = not json_ok('{"scrollFactor": %s}' % real_field)
        ref_reported = float(real_field)                  # JSON number read back
        ref_printed  = "%.2f" % exp
        ref_line  = "AGREE" if "%.2f" % ref_reported == ref_printed else "DIFFER"
        ref_top   = "NOT_COMPARED" if kind == "unsupported" else ("DIFFER" if ref_line == "DIFFER" else "OK")
        truth_line, truth_top = ("SETUP", "SETUP") if broken else ("AGREE", "OK")
```

`truth` is what a tool reaches when it knows the stored value: the field text *is* the stored value,
so the correct comparison is always `AGREE`; it is `SETUP` only when the field text is not JSON.
A case flips when `ref_line != truth_line` or `ref_top != truth_top`.

### 2.3 `gen.py` — corpus (59 394 cases, 21 categories)

`dec1` 3 051, `dec2` 6 101, `dec3` 2 227, `dec4..dec7` 4 800, `half3` 30 501 (every `x.xx5` in
[-5,300]), `half3r` 1 017 (`repr()` of the same), `prefix` 306 (`0.7x`, `1e`, `1e+`, `.5`, `5.`,
`+.5`, `-0x`, NBSP suffix …), `exp` 309 (`1e-50..1e44`, `3.4028235e38`, `4e38`, `1e999`),
`subnormal` 22, `hex` 14, `nonfinite` 20, `ws` 15, `longdigits` 7, `junk` 2 000, and 9 004
double-rounding constructions at every 2-decimal boundary:

```python
    m = (decimal.Decimal(lo) + decimal.Decimal(hi)) / 2   # exact float32 midpoint as a double
    s = format(m, "f")                                    # its exact decimal expansion
    add("dblround_above", s + "0" * 20 + "1")             # rounds float(s) to the midpoint ...
    add("dblround_at", s)
    add("dblround_below", ip + "." + fp2 + "9" * 20)      # ... from the other side
```

The construction targets the real defect: the reference converts decimal → **double** → float32
(`f32(float(s))`), two roundings, while `std::stof` → `strtof` rounds decimal → float32 once. At a
midpoint the double lands exactly on the tie, so ties-to-even picks one float and `strtof` picks the
other.

### 2.4 `fmtsweep.cpp` + `fmtcmp.py` — the formatting stage alone

`fmtsweep` prints `std::format("{:.2f}", bit_cast<float>(bits))` for a bit-pattern list; `fmtcmp`
generates 2 391 762 patterns (all denormal-band patterns both signs, ±2 ulp around every
2-decimal boundary in [-5,300], 200 000 uniform in [0,100], 50 000 uniform in [-5,300], 1 500 000
random 32-bit, plus ±inf/±nan/±0/FLT_MAX/FLT_MIN) and compares against `"%.2f"` of the same value.

### 2.5 `demo.py` — user-visible consequence

Builds the dump Hyprland would print for one mouse, runs the pinned reference CLI
(`--devices … --config …`) and prints its `MADO_DEV_MOUSE` line, summary line and exit code.

## 3. Results

### 3.1 Outcome classes (59 394 cases)

| class | n | line flips | top flips |
|---|---|---|---|
| `same_value` (identical float, identical text) | 55 229 | 0 | 0 |
| `value_ulp_diff` (both parse, different float) | 2 751 | 2 751 | 2 751 |
| `ref_refuses_cpp_stores` | 37 | 29 | 37 |
| `ref_refuses_cpp_both_unset` | 64 | 0 | 64 |
| `other` (ref stores 0.0, `std::stof` throws) | 19 | 19 | 19 |
| `both_unset` | 1 294 | 0 | 0 |

Total flips `2 871`: `2 770 × line DIFFER->AGREE (top DIFFER->OK)`, `29 × line DIFFER->AGREE (top
NOT_COMPARED->OK)`, `64 × top NOT_COMPARED->OK`, `8 × top NOT_COMPARED->SETUP`.

### 3.2 Zero-divergence categories (the realistic ones)

| category | clean |
|---|---|
| `dec1`/`dec2`/`dec3`/`dec4`/`dec5`/`dec6`/`dec7` | 16 179 / 16 179 |
| `half3` (`x.xx5`, third-decimal halves) | 30 501 / 30 501 |
| `half3r` (`repr()` forms) | 1 017 / 1 017 |
| `longdigits` (30–60 digit strings) | 7 / 7 |
| `ws` | 15 / 15 |
| `dblround_at` (exact midpoint decimal, no perturbation) | 3 000 / 3 000 |

`2.675`, `0.125`, `0.135`, `0.005`, `99.995`, `-3.5`, `250` all parse to the same float32 on both
sides and print the same text (`2.67`, `0.12`, `0.14`, `0.01`, `100.00`, `0.00`, `100.00`).

### 3.3 Formatting stage (`2 391 762` float32 values)

```
float32_values=2391762 mismatches=3020
  bits=ff801d74 value=nan cpp='-nan' py='nan'
...
non_nan mismatches = 0
```

`std::format("{:.2f}", float)` and `"%.2f"` agree on **every** value except the sign of NaN
(`-nan` vs `nan`). No finite case diverges, including the neighbouring floats of every
2-decimal boundary, so a 1-ulp parse error only becomes a text difference when the two floats
straddle a `.xx5` boundary — which is exactly what §2.3 constructs.

### 3.4 Reported-value round trip

`reported_roundtrip_failures = 0`: for all 59 394 cases `"%.2f" % float(<field text>)` reproduces the
field text, so the reference's re-formatting of the JSON number cannot drift on its own.

## 4. Divergence catalogue

### D1 — double rounding in `f32()` (2 751 cases; flips line and top to a false `DIFFER`)

`read_float` does `float()` → `struct.pack("<f")`, i.e. decimal → double → float32.
`std::stof` does decimal → float32 in one step. They differ at float32 midpoints that are exactly
representable as doubles, which is where a 2-decimal boundary lives.

```
cfg:  device[m]:scroll_factor = 0.00500000012107193470001220703125000000000000000000001
stmt: SET 3ba3d70b 0.01        (std::stof -> 0.005000000121..., prints 0.01)
ref : 0x3ba3d70a (0.004999999888241291) -> exp 0.00   (f32(float(s)) lands on the midpoint, ties-to-even)
tool: MADO_DEV_MOUSE: name="m" block=yes scroll_factor=0.00 reported=0.01 verdict=DIFFER
      MADO_DEVICES: ... mice_differ=1 ... verdict=DIFFER   rc=1
truth: 0.01 -> AGREE
```

2 751 / 9 004 constructions flip (`dblround_above` 1 430, `dblround_below` 1 320, one hand case
`2.6750000715255737304687499`). Trigger threshold: an RHS with enough digits that its double
rounds onto the midpoint, i.e. >= 19 significant digits for values around 1. A short decimal
(`2.675`, `0.125`) is never affected — verified by the 30 501-case `half3` sweep. **It can and does
flip AGREE↔DIFFER**, in the false-`DIFFER` direction, at both the mouse line and the top verdict.

### D2 — underflow to zero: reference stores 0.0, `std::stof` throws (19 cases; false `DIFFER`)

`read_float` refuses only when `v != 0.0 and abs(decimal) < FLT_MIN`, where `v` is the *rounded*
value. A decimal below the smallest subnormal rounds to `0.0`, so the guard does not fire and the
reference stores `0.0`. `strtof` reports underflow (`ERANGE`) and libstdc++ turns that into
`std::out_of_range`, so hyprland stores nothing.

```
cfg:  device[m]:scroll_factor = 1e-50
stmt: UNSET out_of_range            -> field -1.00   (hyprlang setError, m_bSetByUser false)
ref : ok 0.0 -> exp 0.00, MADO_DEV_BLOCK keys=1
tool: MADO_DEV_MOUSE: name="m" block=yes scroll_factor=0.00 reported=-1.00 verdict=DIFFER
      MADO_DEVICES: ... mice_differ=1 ... verdict=DIFFER   rc=1
truth: -1.00 -> AGREE
```

Also flips the `MADO_DEV_BLOCK keys=` count (0 vs 1). Observed texts: `1e-46`…`1e-50`, `2.5e-*`,
`-1e-*`, `1e-999`, `1e-230cx`, `7.006492321624085e-46`. Same mechanism, opposite sign of the error
at D3.

The contract text states the guard as "a nonzero value below 2**-126 in magnitude adds one to
`unsupported`" (draft `mado-devices.py:64-65`), but the code tests the *rounded* value:
`if math.isinf(v) or (v != 0.0 and abs(float(m.group(0))) < FLT_MIN)` (draft `:216`). A decimal that
rounds to `0.0` therefore never reaches the `unsupported` branch, which is what makes D2 and D3
disagree with `strtof` on opposite sides of `FLT_MIN`.

### D3 — the `FLT_MIN` boundary (1 case; false `DIFFER` line + false `NOT_COMPARED`)

`1.17549435e-38` is a decimal slightly *below* `FLT_MIN` whose correctly rounded float32 *is*
`FLT_MIN`. `strtof` returns the normal `FLT_MIN` (no `ERANGE`), so Hyprland stores it and prints
`0.00`; the reference compares the decimal magnitude with `FLT_MIN` and refuses.

```
stmt: SET 00800000 0.00        ref: unsupported, exp -1.00
tool: MADO_DEV_MOUSE ... scroll_factor=-1.00 reported=0.00 verdict=DIFFER
      MADO_DEVICES: ... unsupported=1 verdict=NOT_COMPARED   rc=5
truth: 0.00 -> AGREE, top OK
```

### D4 — hex floats (19 cases; false `DIFFER` line, forced `NOT_COMPARED`)

`strtof` accepts C99 hex floats; `SPECIAL_RE` (`[+-]?(inf|nan|0x)`) refuses every `0x…` spelling.
Real spellings from the corpus: `0x10` → **16.00**, `0X10` → 16.00, `0x1p3` → 8.00,
`0X1P-2` → 0.25, `0x.8p1` → 1.00, `0x1.999999p0` → 1.60, `-0x10` → 0.00, `0x1.fffffep127` →
100.00, `0x` / `0x0` / `0x0p0` / `0X` / `0XP` / `0xPc6.d+.` / `0xnan` → 0.00.

```
tool: MADO_DEV_MOUSE: name="m" block=yes scroll_factor=-1.00 reported=16.00 verdict=DIFFER
      MADO_DEVICES: ... unsupported=1 verdict=NOT_COMPARED   rc=5
```

So `scroll_factor = 0x10` really gives a 16× scroll and the tool calls it a mismatch plus refuses the
run. It cannot reach `AGREE` here.

### D5 — `inf` / `infinity` spellings (clamp to 100 / 0; forced `NOT_COMPARED`)

`inf`, `INF`, `Inf`, `infinity`, `INFINITY`, `+inf`, `+INFINITY`, `-inf`, `infinit` all parse on the
C++ side and `std::clamp` snaps them to **100.00** (or **0.00** for `-inf`); the reference refuses
(`SPECIAL_RE`), expects `-1.00`, and forces `NOT_COMPARED`. `9` of the 20 `nonfinite` cases are in
this arm; the other `9` flips of that category are 8 NaN spellings (D6) and `0xnan` (D4).

### D6 — NaN spellings break the dump itself (8 cases; hard `SETUP`, `rc=2`)

`nan`, `NaN`, `NAN`, `nan(1)`, `nan(chars)`, `nan()`, `+nan` → `"scrollFactor": nan`; `-nan` →
`"scrollFactor": -nan`. `std::format("{:.2f}", nan)` prints `nan` / `-nan` (`Hyprland-HyprCtl.cpp:770`
pastes it raw), which is **not valid JSON**, so `parse_devices` raises `bad_json`:

```
tool: MADO_DEVICES: SETUP bad_json    rc=2      (truth: the tool has no verdict at all)
```

The reference's own NaN refusal is therefore moot: the artifact that breaks is `hyprctl devices -j`
itself. This is the only class where the tool cannot even report `NOT_COMPARED`.

The frozen selftest cannot catch this: its `mouse-nan` case (draft `mado-devices.py:490-491`) pairs
`device[m]:scroll_factor = nan` with `dump([kb("k")], [mouse("m")])`, whose `scrollFactor` is `-1.0`,
so it asserts the parser's refusal and never materialises the `"scrollFactor": nan` field.
`python3 -I mado-devices.py --selftest` → `MADO_DEVICES_SELFTEST: 48/48 passed`.

### D7 — overflow / subnormal refusals are value-correct but force `NOT_COMPARED` (64 cases)

`1e39`, `4e38`, `3.4028236e38`, `1e999`, `1e-40`, `1.4012985e-45`, `1e-44` …: both sides store
nothing, the mouse line already says `AGREE` (`-1.00` vs `-1.00`), but the reference increments
`unsupported` and returns top verdict `NOT_COMPARED 5` where the truth is `OK 0` (hyprlang records a
config error but clears the value, `fetch/hyprlang-config.cpp:465-471` + `:513`; parsing continues,
`fetch/hyprlang-config.cpp:980-987`, so the rest of the config still applies). A false refusal, not a
false mismatch.

## 5. Why the error is one-sided, and why the C1 counter cannot see it

The compared number is read out of the dump, and the dump is produced from the same stored value the
tool is trying to predict. Therefore `ref exp == truth text` is exactly `AGREE`, and a modelling
error can only push the expected value away from the truth: false `DIFFER`, false `NOT_COMPARED`, or
`SETUP`. There is no configuration of `scroll_factor` in which the reference reports `AGREE` for a
genuinely different value — the false-negative arm is empty by construction.

Frozen counter `quality/counters/c1-r46-devices.py` clause `g` generates 150 nonce cases and judges
them **with the pinned reference**, so any divergence from Hyprland is invisible to it: the oracle is
the thing under test. The same holds for `f` (the 90 fixtures under `quality/counters/c1-r46-fixtures.json`,
which were authored as small fixed corpora judged by the same reference). Nothing in the counter
compares the reference against an independent C++ implementation — this seat is that independent
check, and it finds `2 871 / 59 394` (4.8 %) disagreements on the adversarial corpus and `0` on
realistic decimals.

## 6. Verdict on the claim's mouse half

- The **print** side is sound: `"{:.2f}"(float)` ≡ `"%.2f"` for every finite float32 tested
  (2 391 762 values) and for ±0 and ±inf; only the sign of NaN differs, and that case destroys the
  JSON either way.
- The **clamp** side is sound: `std::clamp(v, 0.F, 100.F)` ≡ `min(max(v,0),100)` including `-0.0`
  (both `-0.00`) and NaN (both propagate), because `value_or(-1)` supplies `-1.00` when unset and the
  reference's `-1.0` placeholder matches it.
- The **parse** side is a faithful model of `std::stof` for decimal text with <= 17 significant
  digits (47 697/47 697), and is not faithful in the 7 classes above. For the tool's stated purpose
  (compare a host's config against a live dump) the residual risk is a spurious `DIFFER` on
  hand-written >= 19-digit decimals, a spurious `NOT_COMPARED` on any hex/inf/out-of-range value, and
  a `SETUP bad_json` when a NaN ever reaches the field.

## 7. Limits and unverified points

- `trim()` used at `hyprlang-config.cpp:723` is defined in a header that is not in the pin set; this
  seat models it as `" \t\r\n"` and the reference as `" \t\r\n\v\f"`. The two disagreed on 4 cases
  (`\v`/`\f` only) and no verdict changed. `[INFERENCE]` the exact set is immaterial here.
- `std::stof`'s locale: `setlocale` does not appear anywhere in the pinned sources, so `strtof` runs
  in the `"C"` locale (`strtod`-style `"0,5"` was probed: both sides give `0.0`). `[INFERENCE]`
  limited to the files that were fetched.
- `std::from_chars`/`to_chars` implementations differ between libstdc++, libc++ and MSVC; only
  libstdc++ 16.2.1 + glibc 2.44 (this host, `receipts/versions.txt`) was exercised. `std::format`'s
  float path is specified as correctly rounded, and `strtof` is correctly rounded per C99, so the
  one-rounding statements hold regardless of library.
- No host compositor call was made; no `hyprctl` was run by this seat. The only live-relevant inputs
  are source lines from the pins.
- Counts are corpus-relative, not frequencies over a distribution of user configs.

## 8. Reproduce

```
S=/fast/scratch/hyaku/mado-r46/ExecStofOracle/w && mkdir -p "$S" && cd "$S"
g++ -std=c++23 -O1 -o stmt stmt.cpp && g++ -std=c++23 -O1 -o fmtsweep fmtsweep.cpp
python3 -I gen.py cases.tsv                      # cases=59394 categories=21
python3 -I diff.py cases.tsv ./stmt <draft>/mado-devices.py out.json
python3 -I fmtcmp.py ./fmtsweep 1500000
python3 -I demo.py ./stmt <draft>/mado-devices.py
```

Tooling: no installs. `g++ 16.2.1` (system), `python3 3.14.8` (system), `glibc 2.44`. Scratch root
`/fast/scratch/hyaku/mado-r46/ExecStofOracle/` (5.1 MB, deleted after receipts were copied).
