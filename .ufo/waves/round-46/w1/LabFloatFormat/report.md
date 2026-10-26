# w1/LabFloatFormat — is Python `%.2f` equal to `std::format("{:.2f}", float)` on every value the tool can see?

**Verdict: NOT FALSIFIED.** 0 counterexamples in 2,640,408 compared rows (2,326,323 distinct f32 patterns) plus
1,325,976 end-to-end joins through the frozen reference. Both sides also equal an independent exact-decimal oracle
(570,649 rows). Receipts: `receipts/run.txt` (sha256 `cdcccdd5b46f09374f389d5a9d5aa8461763b90ff39e5e954c93fa2846690d80`),
re-read by `receipts/verify.sh` → `receipts/verify.txt`.

## The hypothesis, and where it comes from

HyprCtl.cpp:770 emits the mouse field as `"scrollFactor": {:.2f}` and :773 passes `m->m_scrollFactor.value_or(-1)`.
The value type is `float`: `InputManager.cpp:1380` assigns it `std::clamp(Config::mgr()->getDeviceFloat(...), 0.F, 100.F)`
and `getDeviceFloat` returns `float` (`ConfigManager.cpp:1139`), so the compositor formats a **float**.
`mado-devices.py:395` then compares by string:
`if is_num(r) and "%.2f" % r == "%.2f" % exp:`, with `exp` the clamped config value (`mado-devices.py:393`).
The join is correct only if the two formatters agree on the f32 in `[-1] ∪ [0,100]` — that is the hypothesis.

## Attempts to falsify, in order of strength

| # | value set | rows | `%.2f` ≠ `std::format` |
|---|---|---|---|
| a | every 3-decimal config value `0.000`..`100.000`, parsed by `std::stof` (gcc, clang) | 100,001 ×2 | 0 |
| b | every exact 2-decimal midpoint reachable in binary: `j/8`, j odd, 1..799 = 0.125 … 99.875 | 400 | 0 |
| c | every midpoint `k/200` (k odd) in [0,100] and its 3 nearest f32 neighbours on **each** side, plus 0.0, −0.0, −1.0 | 70,003 | 0 |
| d | 10^5 random finite f32 bit patterns, seed 46 (gcc, clang) | 100,000 ×2 | 0 |
| e | 10^5 random f32 uniform in [0,100], seed 46 | 100,000 | 0 |
| f | supplementary: 10^6 random bit patterns seed 7, 10^6 uniform-in-range seed 2026 | 2,000,000 | 0 |

Sets a–c are the only places a difference could start: a formatter that is correctly rounded is a function of the
value's relation to the midpoints, so (c) covers every decision point of the tool's range, and (b) covers the tie rule.
Ties are exactly `{j/8 : j odd}`: a 2-decimal midpoint is `k/200` with k odd, and a dyadic rational equals it only when
25 | k, i.e. `k = 25j`, which collapses it to `j/8`. Both sides round those half-to-even — e.g. 0.125 → `0.12`,
0.375 → `0.38`, 0.625 → `0.62`, 0.875 → `0.88`, 99.875 → `99.88` (`receipts/ties-both.tsv`, 400/400 agree), which is
what the frozen fixture `mouse-round-half-even` pins (`quality/counters/c1-r46-fixtures.json:1553`, `scroll_factor =
0.125`, dump `0.12`).

Two robustness checks that also came out empty: the `float` and `double` columns of the C++ output never differ
(`float_vs_double=0` everywhere, 2.6M rows), so the hypothesis survives if the optional ever becomes `double`; and
gcc vs clang and `-O0/-O1/-O2/-O3/-Os` produce byte-identical 100,001-row outputs (`receipts/run.txt`, "IDENTICAL").

## Independent leg: both are *correctly* rounded, not merely equal

Equal-and-wrong would also pass the table above, so `receipts/oracle.py` computes the exact binary value with
`Decimal(float)` and quantizes to 0.01 with `ROUND_HALF_EVEN` — sharing no code with either formatter. Over 570,649
values (all of a–c plus a 20 % sample of f): `python_vs_exact=0 float_vs_exact=0`.

## The implementation under test is the one Hyprland runs

`objdump -T /usr/bin/Hyprland | c++filt` lists `std::to_chars(char*, char*, float, std::chars_format, int)` as an
undefined reference at `GLIBCXX_3.4.29`; `/usr/lib/libstdc++.so.6.0.36` (the file behind Hyprland's
`libstdc++.so.6`, per `ldd`) defines that symbol at `0x1a3950`. `std::format`'s fixed-precision float path is that
entry point, so the code exercised here is the code that prints the host's `scrollFactor`, not a look-alike.
Toolchain: g++ 16.2.1, clang 23.1.3 (libstdc++; libc++ is not installed here), Python 3.14.8.

## End-to-end join through the frozen reference

Dumps were written by hand carrying the **C++ string verbatim** as `"scrollFactor": <text>` (what hyprctl prints),
with a config line that `std::stof` maps back to the same bits, then judged by
`.ufo/waves/round-46/l1-draft/mado-devices.py`:

```
REFERENCE-JOIN rows=359061   no_block_rows=1 skipped=91908  batches=90  mice=267153   differ=0 bad_run=0
REFERENCE-JOIN rows=1978229  no_block_rows=0 skipped=919406 batches=353 mice=1058823  differ=0 bad_run=0
```

1,325,976 mice, 0 `mice_differ`, 0 bad runs. Values outside [0,100] were skipped by construction (Hyprland clamps
before printing, so the tool cannot see them); the `-1.00` case was modelled as a mouse with no device block, which is
the only way that text is produced (`HyprCtl.cpp:773`, `value_or(-1)`).

## By-product observation (not a falsifier, but it is what the join rests on)

`-0.0` prints `-0.00` on **both** sides, and the reference distinguishes it from `0.00`: `config=-0, dump=-0.00` → AGREE,
`config=-0, dump=0.00` → DIFFER (`receipts/negzero.txt`). That is faithful, not over-strict, because the compositor
preserves the sign: hyprlang parses the float with `std::stof` (`hyprlang-config.cpp:467`, CONFIGDATATYPE_FLOAT branch)
and `std::clamp(-0.0f, 0.f, 100.f)` returns `-0.0f` since `-0.0f < 0.f` is false (`InputManager.cpp:1380`). Also note
`max(-0.0, 0.0)` in Python returns `-0.0`, so the tool's own clamp keeps the sign. No correction needed; recorded in
case a future fixture feeds `scroll_factor = 0` and a dump of `-0.00` and wonders whether the tool invented the sign.

## Impact on the claims

- **Supports** C1's model at `mado-devices.py:395`: the string comparison reproduces the compositor's own number
  exactly over the whole `[0,100]` grid at f32 resolution, including ties and both ends.
- **Supports** C2's census field `json_scroll_decimals=2` (`quality/counters/c2-r46-input-device-entry.py:49`): the
  pinned producer really is a two-decimal `{:.2f}` on a float.
- **No attack lands.** The nearest thing to a defect is coverage, not semantics: `l1-draft/mado-devices.py --selftest`
  prints `MADO_DEVICES_SELFTEST: 48/48 passed` yet contains no tie value at all (`grep -c 125` = 0 on the reference),
  so the half-even behaviour is pinned only by clause f's fixture `mouse-round-half-even`
  (`quality/counters/c1-r46-fixtures.json:1553`, config `scroll_factor = 0.125` at :1555, dump `0.12`). A selftest
  line for `0.125` would put the tie rule under clause s instead of relying on the fixture set.

## Residual limits (declared, not measured away)

- Not exhaustive over 2^32 f32 patterns. The argument is structural: the decision set (all 10,000 midpoints in
  [0,100] ±3 ulp, all 400 exact ties) is covered, so a counterexample would need an implementation error ≥ 4 ulp from
  any midpoint, which correct rounding excludes and which 2.3M distinct samples did not show.
- One library family (libstdc++). That matches the host: Hyprland links `libstdc++.so.6`. A libc++-built Hyprland
  would have to be re-run.
- Rounding mode and locale are held fixed at the default: no `fesetround` and no `setlocale` occurs in any pin under
  `.ufo/waves/round-46/fetch/` (grep count 0), and `std::format` is locale-independent for numbers. A process that
  changes either is outside this hypothesis.

## Reproduction

`receipts/run.sh` under `/fast/scratch/hyaku/mado-r46/LabFloatFormat/` (seeds 46, 7, 2026; ~45 s) regenerates every
table row and writes `receipts/run.txt`; `receipts/verify.sh` re-reads that transcript and prints the verdict line.
The scratch directory was removed after the run (operator directive 2026-10-25); to replay, recreate it, copy the
`*.cpp`/`*.py`/`run.sh` from `receipts/`, and run `bash run.sh`.
No host service, compositor call or package transaction was used. Files: `fmt.cpp`, `compare.py`, `join.py`,
`oracle.py`, `run.sh`, `verify.sh` (all in `receipts/`, sha256 in `run.txt`).
