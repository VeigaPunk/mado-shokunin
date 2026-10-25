# ExecOracleHlInt — C1 integer conversion: the real hyprlang 0.6.8 parser vs the counter's Python model

Seat: `ExecOracleHlInt`, round-40 w1. Oracle only — no claim, no score, no lane file
outside `.ufo/waves/round-40/w1/ExecOracleHlInt/` was written.

Question attacked: `quality/counters/c1-r40-live.py` (PRED-C1-r40-v1, sha256
`192ff2d3d9de39b7a73ac439d4924e71ff8d308e0ecde38364f4e54c188115ea`) models
`hyprlang v0.6.8 configStringToInt` in Python (`hl_int`). How far does that model
agree with the real parser?

## Verdict

- The real library **is installed and links**: `pkg-config --modversion hyprlang` →
  `0.6.8`; `ldd oracle_int` → `libhyprlang.so.2 => /usr/lib/libhyprlang.so.2`
  (`readlink -f` → `/usr/lib/libhyprlang.so.0.6.8`,
  sha256 `51f1d29b396ed6320cbe74a9d13fd35841438cf51c3b76029a513ce33a1aa927`),
  `libhyprutils.so.13`. No standalone re-compile of `configStringToInt` was needed.
- **188-spelling corpus: 164 agree, 24 disagree** (69 native parse errors; every
  error leaves the option at its default `0`, verified `stored==0` in all 69).
- **Within the counter's own generator population: 0 disagreements.**
  Driving the frozen `Fixture` over 500 seeds yields 1401 distinct int-form
  spellings; native and model agree on **1401/1401** (`diff-gen.txt`).
  The model is therefore exact on everything the fixtures can emit — the
  divergences are all out-of-generator-space (OOD) or structural.
- Divergences are in four mechanisms: **int64 width** (Python bignums vs
  `stoll` throwing), **float32 + `std::round` vs float64 + banker's `round`** for
  the `rgba()` alpha byte, **`parseLine` pre-processing** (inline comments,
  `$variable` expansion, `{{a+b}}` expressions, last-declaration-wins) which the
  model does not model at all, and **`inf`/`nan` alpha** (UB in C++, model errors
  or raises).

## Method

`oracle_int.cpp` registers one `Hyprlang::INT` option `x`, writes the corpus
body to a temp file, and runs the real path
`CConfig(path, SConfigOptions{}).addConfigValue("x", INT{0}) → commence() →
parse()` — i.e. `parseLine` → `configSetValueSafe` → `configStringToInt`
(`src/config.cpp:669`, `:277`, `:185-264`). Per entry it records the exact file
bytes, whether the parse errored, the stored integer and the error string.
A fresh `CConfig` per entry; the temp dir is created with `mkdtemp` and removed.

`model_int.py` imports `hl_int` **from the frozen counter file** (importlib, no
copy, no edit) and applies it exactly as `model_equal(..., form="int")` does:
`d = declared.strip(); hl_int(d)`; `None` = the model says parse error.

`diff.py` joins the two JSONL streams by id and classifies every row
(`value-vs-value`, `value-vs-error`, `error-vs-value`, `model-raised`); error
*text* is never compared, only error-vs-value.

## Corpus (`corpus.tsv`, 188 entries)

| category | n | what |
|---|---|---|
| `hex` | 19 | `0x…` incl. `0x0`, `0X1`, `0x 1`, `0x-1`, `0x1_0`, `0x1.`, int64 boundary, overflow |
| `rgba_hex` | 15 | `rgba(8 hex)` incl. 7/9 hex, non-hex, `0x`-prefixed 8 chars, missing paren, uppercase fn |
| `rgba_csv` | 24 | `rgba(r,g,b,a)` incl. `a` ∈ {1, 0.8, 0.4, 0.5, 1.0, 4, −1, +0.5, inf, nan, 0.49999999}, 2/4 commas, empty 4th, hex components, `r=256`, spaces |
| `rgba_alpha` | 30 | alpha sweep 0.05…0.95 step .05, plus 1, 1.5, 2.5, 3.5, 4.5, 5.5, 0, −0.5, 0.333, 0.666, 255 |
| `rgb_hex` | 12 | `rgb(6 hex)` incl. 5/7 hex, non-hex, `0x1234`, spaces, missing paren |
| `rgb_csv` | 10 | `rgb(r,g,b)` incl. hex parts, `256`, `−1`, 1/3 commas, non-numeric |
| `bool` | 23 | `true/on/yes/false/off/no` + prefix forms (`yes, please :)`, `on # note`, `offscreen`, `nothing`, `yesterday`, `on-hold`, `yesno`, `NO`, `on#note`, `true#x`) |
| `dec` | 28 | plain, negative, `+5`, `007`, `00`, `-0`, `1.0`, `1e3`, `1_000`, `0b101`, `0o7`, `-`, `--5`, `.5`, `3.`, `1 2`, int64 boundary/overflow |
| `junk` | 15 | `#`, `##`, `a##b`, `x=y`, `"5"`, `5x`, `@`, interior tab, `1;2`, `(5)`, comment tails |
| `host` | 4 | the host's own bytes: `rgb(e68e0d)`, `rgba(33ccffee)`, `rgba(00ff99ee)`, `0xffe68e0d` |
| `raw` (structural) | 8 | `$v = 7` + `x = $v`; `{{ 2 + 2 }}`; `{{2+2}}`; redeclaration; comment tails; `$c = rgb(e68e0d)` + `x = $c` |

Every spelling is scored `gen` (the generator can emit it), `ood`, or
`structural`. The four host spellings convert exactly as the host prints them:
`rgb(e68e0d)` → `4293299725` = `0xffe68e0d`, `0xffe68e0d` → same,
`rgba(33ccffee)` → `0xee33ccff`, `rgba(00ff99ee)` → `0xee00ff99` (ARGB, as the
model also computes).

## Results

`diff.txt`:

```
ENTRIES: 188  agree: 164  disagree: 24
SCOPE gen        entries= 28 disagree= 0
SCOPE ood        entries=152 disagree=18
SCOPE structural entries=  8 disagree= 6
```

Native: 119 parse, 69 error. Classes: `value-vs-error` 10, `error-vs-value` 7,
`value-vs-value` 6, `model-raised` 1.

### A. int64 width — native errors, model returns a bignum (7)

| id | spelling | native | model |
|---|---|---|---|
| h05 | `0xffffffffffffffff` | `invalid hex 0xffffffffffffffff` | 18446744073709551615 |
| h06 | `0x1ffffffffffffffff` | `invalid hex …` | 36893488147419103231 |
| h08 | `0x8000000000000000` | `invalid hex …` | 9223372036854775808 |
| d19 | `9223372036854775808` | `stoll threw: stoll` | 9223372036854775808 |
| d21 | `-9223372036854775809` | `stoll threw: stoll` | -9223372036854775809 |
| d22 | `99999999999999999999` | `stoll threw: stoll` | 99999999999999999999 |
| h17 | `0x1_0` | `invalid hex 0x1_0` | 16 |

Mechanism: `parseHex` is `stoll(value, &position, 16)` and the decimal tail is
`std::stoll(VALUE)`; both throw `out_of_range` and the throw is turned into a
parse error (`src/config.cpp:186-194`, `:268-272`). Python ints are unbounded.
`h17` is a second Python-only acceptance: `int("0x1_0", 16) == 16` (underscore
digit separators) while `stoll` stops at `_` with `position != size`.
Boundary sanity: `0x7fffffffffffffff` (h07), `9223372036854775807` (d18) and
`-9223372036854775808` (d20) **agree**.

### B. alpha byte: float32 + half-away-from-zero vs float64 + half-to-even (6 value-vs-value, 1 error-vs-value, 1 raise)

Native `a = std::round(std::stof(alpha) * 255.f)` stored into `uint8_t`
(`src/config.cpp:209-218`); the model does `int(round(float(alpha) * 255.0)) & 0xFF`.

| id | spelling | native (ARGB) | model |
|---|---|---|---|
| a06 | `rgba(1,2,3,0.3)` | 1291911683 = `0x4d010203` (a=77) | 1275134467 = `0x4c010203` (a=76) |
| a14 | `rgba(1,2,3,0.7)` | 3003187715 = `0xb3010203` (a=179) | 2986410499 = `0xb2010203` (a=178) |
| a21 | `rgba(1,2,3,1.5)` | 2130772483 (a=127) | 2113995267 (a=126) |
| a23 | `rgba(1,2,3,3.5)` | 2097218051 (a=125) | 2080440835 (a=124) |
| a25 | `rgba(1,2,3,5.5)` | 2063663619 (a=123) | 2046886403 (a=122) |
| c24 | `rgba(1,2,3,0.49999999)` | 2147549699 (a=128) | 2130772483 (a=127) |
| c21 | `rgba(1,2,3,nan)` | 66051 = `0x00010203` (a=0) | ERROR |
| c20 | `rgba(1,2,3,inf)` | 66051 (a=0) | **raises** `OverflowError` |

Two distinct effects:
1. **Tie parity.** A 0.01 alpha sweep (`alpha-sweep.tsv`, 101 entries,
   `diff-alpha.txt`) gives `ENTRIES: 101 agree: 99 disagree: 2`. Exactly five
   products are `k+0.5` in float32 — `0.10→25.5, 0.30→76.5, 0.50→127.5,
   0.70→178.5, 0.90→229.5` — and the divergence is exactly the rows with **even
   `k`** (`0.30`, `0.70`): `std::round` rounds half away from zero, Python
   `round()` rounds half to even. Verified mechanically:
   `rule (diverge iff floor even): True`.
2. **float32 literal rounding.** `0.49999999f` rounds *up to* `0.5f`, so native
   computes `127.5 → 128` while float64 keeps `127.49999745 → 127`.
3. `inf`/`nan` are undefined behaviour in C++ (`round(inf)` cast to `uint8_t`
   yields 0 here); the model returns `None` for `nan` but **raises**
   `OverflowError` for `inf` — `hl_int` only catches `ValueError` around
   `round(float(part) * 255.0)`, so a fixture that ever declared `inf` would
   crash the counter rather than score a mismatch.

The generator's alpha literals are exactly `{1, 0.8, 0.4}` (`gen-space.tsv`,
measured), all of which are exact in both models — this is why the fixture space
never sees class B.

### C. `parseLine` pre-processing the model does not model (9 value-vs-error)

The real conversion never sees the raw declared text. Before
`configSetValueSafe`, `parseLine` (`src/config.cpp:669-810`) does:

- **inline comments** — the first unescaped `#` truncates the rest of the line;
  `##` is an escape yielding a literal `#`:
  `rgba(1,2,3,0.5) # note` → 2147549699 (j09), `0x1 # note` → 1 (j10),
  `0xff#note` → 255 (j11). The model errors on all three.
- **`$variable` substitution** from earlier declarations:
  `$v = 7` + `x = $v` → 7 (t01); `$c = rgb(e68e0d)` + `x = $c` → 4293299725
  (t07); with comment tails on both lines → 4293299725 (t08). Model: error.
- **`{{a + b}}` expressions** — `x = {{ 2 + 2 }}` → 4 (t03); the result is
  formatted with `std::format("{}", float)` and then converted. (`x = {{2+2}}`
  without spaces errors in *both* — the tokeniser needs spaces — so it agrees.)
- **last declaration wins** — `x = 0x1` then `x = 0x2` → 2 (t04);
  `x = 5 # c` then `x = 6 # c` → 6 (t05). Model: error.

## What this means for C1

- The model is **sufficient for the frozen fixtures** (1401/1401 on the
  generator's own int-form population) — no fixture-space disagreement can
  change the `13/13` target. This supports the declared residual ("a tool that
  hardcodes the reference model's conversion tables passes the fixtures") and
  does not contradict `ctl/run-c1-controls.py`'s `18/18`.
- The delivered `--live` tool runs on **host config text**, which is outside that
  population: the host theme declares `$activeBorderColor = rgb(e68e0d)` and
  `col.active_border = $activeBorderColor` (registration, provisional facts).
  A converter with only `configStringToInt` semantics — the model's shape —
  reports an **error** for `$activeBorderColor`, so the tool would mislabel that
  key. The real parser resolves the variable first (t07/t08 prove it:
  `x = $c` → `0xffe68e0d`).
  So the tool must model `parseLine` as well as `configStringToInt`: inline
  comments with the `##` escape, `$var` substitution from earlier declarations
  in the same tree, `{{a+b}}` formatting, last-declaration-wins.
- Two narrower correctness points for any port: clamp to **int64** and treat
  overflow as a parse error (class A), and if exotic alphas matter, reproduce
  **float32 + `std::round`** (class B); neither is reachable from the fixtures.

## Limits (declared)

- Covers the **INT** form only, as assigned. `float`, `str` and `custom`
  (gradient / CSS gap / font-weight) conversions are not exercised here, nor the
  compositor's printing of values, `set` semantics, special categories, or the
  host census.
- The corpus is finite and hand-built plus a 1401-spelling generator population;
  a spelling class I did not think of is not covered.
- `inf`/`nan` rows record this build's UB outcome; they are not portable
  semantics.
- Errors are compared as error-vs-value, never by message text.

## Reproduce

```
cd /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-40/w1/ExecOracleHlInt
g++ -std=c++23 -O2 oracle_int.cpp -o oracle_int $(pkg-config --cflags --libs hyprlang)
./oracle_int corpus.tsv out-native.jsonl
python3 -I model_int.py corpus.tsv out-model.jsonl
python3 -I diff.py out-native.jsonl out-model.jsonl > diff.txt
python3 -I gen_space.py gen-space.tsv        # 1401 distinct int-form spellings
./oracle_int gen-space.tsv out-gen-native.jsonl
python3 -I model_int.py gen-space.tsv out-gen-model.jsonl
python3 -I diff.py out-gen-native.jsonl out-gen-model.jsonl > diff-gen.txt
./oracle_int alpha-sweep.tsv out-alpha-native.jsonl
python3 -I model_int.py alpha-sweep.tsv out-alpha-model.jsonl
python3 -I diff.py out-alpha-native.jsonl out-alpha-model.jsonl > diff-alpha.txt
```

Source read (read-only, from the v0.6.8 tag): `src/config.cpp` (fetched to
`/tmp`, scratch, removed), `src/config.hpp`, `src/common.cpp`,
`src/public.hpp`; `hyprutils src/string/String.cpp` for `isNumber`
(`config.cpp:265` passes `allowfloat=false`, which is why `1.0`, `3.`, `.5`,
`1e3` error while `-5` parses).

## Artifacts (this seat dir)

| file | sha256 |
|---|---|
| `corpus.tsv` | `1fc834310920e310ac21d0d2f5dd6952be51bf1379375e8ae2cb3321f3d448b6` |
| `alpha-sweep.tsv` | `00e906646fbacfda11e6e545add7155798f16702c4eafab95848a8c4099399fe` |
| `gen-space.tsv` | `78826581ca81b9e9b2c15cffe97e95267421a6153cfb901588a3b5035921e7ce` |
| `oracle_int.cpp` | `60960810d4ab42a0ea241efb9fd2ffd17eb42198d0122ddac3f0937534673279` |
| `model_int.py` | `36c33739629330a5e5ca29928c359ed0c8c1ab300a7a2f2e0b0becd0d5bca259` |
| `diff.py` | `6223d8bd5bf78c655340346a4b984512640406978f071495f55466e4a68d6f14` |
| `gen_space.py` | `7adc3f7d2c5d341e2bc58fb4ffdf5e6354171590c4e8f0f370d34a99c85963b9` |
| `out-native.jsonl` | `91471f2ecdda03ac6c34adb7ce87c3a251f04d2aa805f1358655a05267860808` |
| `out-model.jsonl` | `a6c259c7098c6b54ebede9a211a54f6f783e026148e666122dd1d41b5dee95b0` |
| `out-gen-native.jsonl` | `614c9142d0a5d87d14b738a6d7f1c6324213b382e0e11c91b79ba14e0bb9bfc4` |
| `out-gen-model.jsonl` | `284407e67c920890f00a63683a066409483122fe1d19edccaf73664f98bfdaf3` |
| `out-alpha-native.jsonl` | `cd7a3d90fe1a715c290dafdeb05dc685fb06d17da60b428dd7cf196c3fa58caa` |
| `out-alpha-model.jsonl` | `c7ef1fb3ae96924a2ce0447a6d3745a3aa881ba91a643c78b6a016666e332866` |
| `diff.txt` | `f930678ccd182601c6a597b692235707c4ce620c2cf3f57613bed659bac6d900` |
| `diff-gen.txt` | `cc33c0b9a8ad6425f1661c9a57cfea969382322dd00a93fae31e5ec225788d0d` |
| `diff-alpha.txt` | `a947b5356eec33b7081fdd9bd0db8393380d3939537b78b5e8752ae5d247f913` |

Tooling: nothing installed, no package transaction (pacman paused host-wide).
Only read-only verbs were used; no compositor verb was needed for this seat.
Build products (`oracle_int`) and all temp dirs stay inside this seat dir or
`/tmp` (removed).
