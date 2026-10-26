# ExecStofOracle — findings (round 46 / w1)

Scope: differential test of the scroll-factor arithmetic (`std::stof` → hyprlang `setFrom(float)` →
`std::clamp(0.F, 100.F)` → `std::format("{:.2f}")`, `Hyprland-InputManager.cpp:1379-1382` +
`Hyprland-HyprCtl.cpp:770,773`) against `read_float()` + `"%.2f"` in the pinned reference
`.ufo/waves/round-46/l1-draft/mado-devices.py`. Full harness, evidence and line-numbered sources:
`.ufo/waves/round-46/w1/ExecStofOracle/report.md`; runnable copies + `out.json` in
`.ufo/waves/round-46/w1/ExecStofOracle/receipts/`.

## Result

`59 394` RHS values, 21 categories, `g++ 16.2.1` / `glibc 2.44` / `python3 3.14.8`.
`2 871` verdict divergences (`2 751` parse, `120` refusal/`SETUP`); `0` divergences on the
`47 697` ordinary-decimal cases (`dec1..dec7`, every `x.xx5` half in [-5,300], `repr()` forms).

Stages that never diverge:
- **print**: `std::format("{:.2f}", float)` vs `"%.2f"` over `2 391 762` float32 values
  (all boundary neighbours, denormals, ±inf, ±0, 1.5 M random): `0` mismatches for finite values;
  the only difference is the sign of NaN (`-nan` vs `nan`), which is invalid JSON either way.
- **clamp**: `std::clamp(v,0.F,100.F)` ≡ `min(max(v,0),100)`, incl. `-0.0` (`-0.00` both) and NaN.
- **reported round trip**: `"%.2f" % float(<field text>)` reproduces the field text, `0`/`59 394`.

Stages that do diverge (each flips a verdict; all one-sided — false `DIFFER`, false
`NOT_COMPARED`, or hard `SETUP`, never a false `AGREE`, because the reported number *is* the stored
value):

| # | trigger | what Hyprland does | what the reference does | flip | n |
|---|---|---|---|---|---|
| D1 | decimal ≥19 significant digits that rounds to a float32 midpoint (`2.6750000715255737304687499`, `0.00500000012107193470001220703125000000000000000000001`) | `strtof` rounds decimal→float32 once | `f32(float(s))` rounds twice, ties-to-even on the double | mouse line + top: false `DIFFER` | 2 751 |
| D2 | decimal that underflows to `0.0` (`1e-46`…`1e-50`, `1e-999`) | `std::stof` throws `out_of_range`, key stays unset → field `-1.00` | stores `0.0`, expects `0.00`, `keys=1` | false `DIFFER` (line + top, rc 1) | 19 |
| D3 | `1.17549435e-38` (decimal just below `FLT_MIN`, rounds to `FLT_MIN`) | stores `FLT_MIN`, prints `0.00` | refuses by decimal magnitude → `-1.00` | false `DIFFER` line, top `NOT_COMPARED` | 1 |
| D4 | hex floats `0x10`/`0X1P-2`/`0x1p3`/`0x.8p1`/`-0x10`, and bare `0x`/`0X` | `strtof` accepts C99 hex (`0x10` → **16.00**) | `SPECIAL_RE` refuses | false `DIFFER` line, forced `NOT_COMPARED` | 19 |
| D5 | `inf`, `INF`, `infinity`, `+inf`, `-inf`, `infinit` | `strtof` → clamp to **100.00** (`-inf` → 0.00) | refuses | forced `NOT_COMPARED` | 9 |
| D6 | `nan`, `NaN`, `nan(1)`, `nan()`, `-nan` | field prints `nan` / `-nan` — **invalid JSON** | `parse_devices` raises `bad_json` | `MADO_DEVICES: SETUP bad_json`, rc 2 | 8 |
| D7 | `1e39`, `4e38`, `1e999`, `1e-40`, `1.4012985e-45` | parse error, value cleared (later lines still apply) | refuses → `NOT_COMPARED` | top `NOT_COMPARED` vs true `OK` | 64 |

(D3–D6 partition the 37-case `ref_refuses_cpp_stores` class exactly: 1+19+9+8 = 37; D1 is
`value_ulp_diff` 2 751, D2 is `other` 19, D7 is `ref_refuses_cpp_both_unset` 64, and the remaining
1 294 `both_unset` cases are clean, so the arms sum to 2 871.)

Evidence for the sharpest one (D1), reproduced through the real reference CLI:

```
cfg:  device { name = m
                scroll_factor = 0.00500000012107193470001220703125000000000000000000001 }
stmt: SET 3ba3d70b 0.01          ref: 0x3ba3d70a -> exp 0.00
ref : MADO_DEV_MOUSE: name="m" block=yes scroll_factor=0.00 reported=0.01 verdict=DIFFER
      MADO_DEVICES: ... mice_differ=1 ... verdict=DIFFER    rc=1
truth: 0.01 -> AGREE
```

and for D6 `MADO_DEVICES: SETUP bad_json rc=2`; for D2 `scroll_factor=0.00 reported=-1.00
verdict=DIFFER rc=1`; for D4/D5 `... unsupported=1 verdict=NOT_COMPARED rc=5`.

## What this attacks / supports

- Attacks the reading of the C1 mouse model as *exact*: it is exact for decimal text with ≤17
  significant digits and for the whole formatting stage, and wrong in the 7 enumerated classes above.
- Supports the C1 mouse model's two structural decisions: (a) the device block is the only source of
  `m_scrollFactor` (the global `input:scroll_factor` never reaches the field — guarded by
  `deviceConfigExplicitlySet`, `Hyprland-ConfigManager.cpp:1125`), and (b) an unset optional prints
  `-1.00`, which the reference's `-1.0` placeholder matches.
- Explains why the frozen counter cannot see any of it: clause `g` (150 nonce cases) and clause `f`
  (90 fixtures) judge the reference **with the reference**. Nothing in
  `quality/counters/c1-r46-devices.py` compares it against an independent C++ implementation; the
  frozen selftest likewise only asserts the parser's self-consistency (`mouse-nan` at draft
  `mado-devices.py:490-491` uses a dump whose `scrollFactor` is `-1.0`, never `nan`).
- Adversarial magnitude: 4.8 % of the corpus, 0 % of realistic decimals. Practical risk is a
  spurious `DIFFER` on a hand-written ≥19-digit decimal, a spurious `NOT_COMPARED` on any
  hex/`inf`/out-of-range value, and `SETUP bad_json` if a NaN ever reaches the field.

## Advisory (L1 owns integration; nothing frozen was touched)

1. `read_float` should convert decimal→float32 in one rounding (`Decimal` exact tie test against the
   float32 midpoint instead of `f32(float(s))`) — removes D1's 2 751 flips.
2. The underflow guard should test the *decimal* magnitude (`abs(Decimal(prefix)) < FLT_MIN`) so that
   underflow-to-zero is treated as `unset`, matching `std::stof` — removes D2; and the `FLT_MIN`
   boundary should compare the rounded value, not the decimal, to keep D3's `1.17549435e-38` stored.
3. Field text should be validated before `json.loads` (`nan`/`-nan` are structurally impossible JSON)
   so a NaN config yields a specific `SETUP` reason instead of the generic `bad_json` — D6.
4. Whatever the choice, the entry (`corpus/knowledge/hyprland-input-devices-r46.md`) should state that
   hyprlang accepts C99 hex and `inf`/`nan` via `std::stof` while the tool refuses them, so the
   `NOT_COMPARED` verdict is not mistaken for "this config value is inert".

## Retained evidence

- `receipts/out.json` (all classes, flips, examples), `receipts/out.json.rows.tsv` (59 394 rows),
  `receipts/fmt.txt` (format sweep), `receipts/commands.txt`, `receipts/sha256.txt`,
  `receipts/versions.txt`, and the harness sources `stmt.cpp`, `diff.py`, `gen.py`, `fmtsweep.cpp`,
  `fmtcmp.py`, `demo.py`.
- Reference under test: `l1-draft/mado-devices.py` sha256 `b229efd08d2d329dd60ced114598943d0419dac2f3cf05b1f6c1eb506c49a33b`,
  selftest `48/48`.
- No host compositor call, no `hyprctl`, no pacman, no installs; scratch
  `/fast/scratch/hyaku/mado-r46/ExecStofOracle/` removed after receipts were copied.

## Limits

- hyprlang's `trim()` is defined in a header outside the pin set; modelled as `" \t\r\n"`. It differed
  from the reference's `strip(" \t\r\n\v\f")` on 4 of 59 394 cases (`\v`/`\f` only), no verdict change.
  `[INFERENCE]` immaterial.
- Locale: no `setlocale` in the pinned sources → `strtof` in the `"C"` locale (`"0,5"` probed: both
  sides `0.0`). `[INFERENCE]` limited to the fetched files.
- Only libstdc++/glibc was exercised; the one-rounding statements are library-independent (C99
  `strtof` is correctly rounded, `std::format` float is specified correctly rounded).
- Counts are corpus-relative, not frequencies over user configs.
