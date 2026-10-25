# Seat RevModelVsSource — counter reference model vs upstream sources

Round 40 w1. Target: `hl_int`, `gradient_text` (incl. inherited-angle rule), `gap_text`, `WEIGHTS`
in `quality/counters/c1-r40-live.py`, attacked against hyprlang v0.6.8 `src/config.cpp` and Hyprland
efb50993780079460b0cbed1363e2166a2de1d9f (`src/config/legacy/ConfigManager.cpp`,
`src/config/shared/complex/ComplexDataTypes.hpp`, plus the transitive helpers the handlers call).

Method and evidence:

- Counter bytes reviewed = working tree, verified equal to the freeze commit:
  `git show 5e7e88525cc539563de7746361b2650802e81809:quality/counters/c1-r40-live.py | sha256sum`
  = `192ff2d3d9de39b7a73ac439d4924e71ff8d308e0ecde38364f4e54c188115ea` = `sha256sum` of the working
  file. Counter cited as `py:L` below.
- Upstream fetched from raw.githubusercontent.com (copies + sha256 in
  `.ufo/waves/round-40/w1/RevModelVsSource/`): hyprlang `v0.6.8` `src/config.cpp`
  (`fa1b6898…`; `src/ConfigManager.cpp` 404s at that tag — `src/config.cpp` is the file);
  Hyprland `hl_cm.cpp` (`9db68cf4…`), `hl_cdt.hpp` (`95733223…`), `src/helpers/Color.hpp/.cpp`
  (`2276a8cc…`/`0e7d472c…`), `src/config/shared/parserUtils/ParserUtils.{hpp,cpp}`
  (`115393e7…`/`86f21b76…`); hyprutils `main` `String.{hpp,cpp}`, `VarList2.{hpp,cpp}`,
  `Numeric.hpp` (hashes in seat dir). Cited as `hl_cm:L`, `cdt:L`, `cfg:L` (hyprlang), `pu:L`,
  `color:L`, `hu:L`.
- Numeric claims (angle table, alpha ties, channel round-trip) are computed, not eyeballed:
  float32 steps emulated with `struct.pack/unpack('f')`, `std::round`/`std::floor`/truncation
  modelled explicitly. One-time scratch in /tmp; nothing outside the lane written.
- No `lsp` device is mounted in this seat, so no semantic server checks; verification is direct
  source reading with line numbers. No tools installed (curl/python3 sufficed).

Bottom line: the four model pieces match the C++ for every input class the 13 fixtures and the
host tree use (details in "Confirmed matches"), so PRED-C1-r40-v1's fixture space is not weakened
by anything below. Against the sources as such, the model diverges in 10 places, two of them
structural (F1 wrong converter for gradient colours, F2 missing float32 angle round-trip). All
divergences live in the declared residual's space (out-of-distribution declareds); they are here
enumerated with concrete inputs.

## Findings (by severity)

### F1 (high) — gradient colour tokens are converted with the wrong upstream function

`gradient_text` converts each colour token with `hl_int` (`py:180`, a model of hyprlang
`configStringToInt`, `cfg:185-274`). The host's gradient handler does not call that function: it
calls `ParserUtils::parseColor` (`hl_cm:136`), which is a different converter (`pu:22-130`) with
its own rules. Concrete divergences for a token `t` in a declared gradient:

| Input | Host (`parseColor`) | Model (`hl_int`) |
|---|---|---|
| `#e68e0d`, `#rgb`, `#AARRGGBB` | parsed (`pu:25-64`, alpha `ff` for 6-form) | `None` (no `#` branch; falls to `py:164` regex → `None`) |
| `rgba(300,0,0,1)` r/g/b | `strToNumber<uint8_t>` strict (`pu:77-81`): 300 out of range → whole colour errors | 300 accepted, word `22c0000` (`py:132,139,186`) |
| `rgba(0x11,0,0,1)` | `strToNumber<uint8_t>` = `from_chars` base 10 (`hu_numeric.hpp:34-52`): rejects `0x` | recursion accepts → 17 |
| `rgba(1,2,3,0.5)` alpha | `std::floor(a*255.f)` (`pu:88`) → **127** | `int(round(...))` → **128** |
| `on`/`true`/`yes` token | no bool branch → `isNumber2` fails → colour errors (`pu:126-131`) | 1 → colour word `1` |
| `0xFFFFFFFFFFFFFFFF` | `parseHex` is `strToNumber<uint64_t>` (`pu:16-18`): accepted, then channel-masked by `CHyprColor` | `int(v,16)` unbounded (`py:125`), no mask |

Note the predicate sentence itself (counter docstring `py:27-31`, registration C1) names "Hyprland
gradient handlers" as the converter for gradients — the docstring is right; `gradient_text`'s code
is what deviates.

### F2 (high) — the angle is printed through a lossy float32 radian round-trip the model skips

Host: `m_angle = std::stoi(prefix) * (π/180.0)` stored in a **float** (`hl_cm:120`, `cdt:55`), and
`toString` prints `sc<int>(m_angle * 180.0 / M_PI)` — an int **truncation** of the round-trip
(`cdt:69-75`). The model keeps the declared integer and prints `"%ddeg" % angle` (`py:178,186`).
Computed over all integer degrees: **384 of 801 degrees in [-400,400] print shifted by 1**;
positive examples (declared → host prints): 1→0, 2→1, 4→3, 5→4, 8→7, 10→9, 13→12, 20→19, 29→28,
46→45, 91→90. Fixture/prior angles {0,45,90,135,270} are all in the safe set, and the live capture
contains only `0deg`/`45deg` (`native-capture.jsonl:12,21,22,27-32`), so neither the fixtures nor
the census see this — but any tree declaring e.g. `10deg` converts to `9deg` on the host and
`10deg` in the model.

### F3 (medium) — alpha rounding: `std::round` on float vs Python banker's `round` on double

hyprlang comma-form alpha: `a = std::round(std::stof(s) * 255.f)` → `uint8_t` (`cfg:211-213`):
half-away-from-zero, **float** arithmetic. Model: `int(round(float(s) * 255.0)) & 0xFF` (`py:134`):
half-to-even, **double** arithmetic. Exhaustive sweep over decimal alphas `0.00001..0.99999`
(step 1e-5) finds exactly 2 divergent strings: `"0.3"` → host 77, model 76; `"0.7"` → host 179,
model 178. So `rgba(1,2,3,0.3)` as an int-form declared converts to `…4d010203` on the host and
`…4c010203` in the model. Fixture alphas `1/0.8/0.4` are exact under both (`py:228` comment
acknowledges the tie dodge; verified 255/204/102 both ways). (F1 separately notes the *gradient*
path uses `std::floor`, a third rule, `pu:88`.)

### F4 (medium) — numeric font weights are legal host syntax; the model rejects all of them

`parseWeight` (`cdt:163-174`): map miss → `std::stoi(strWeight)` (`cdt:171`) — numeric declareds
parse without error: in 100..1000 → **`m_value` left unchanged** (keeps prior/default, `cdt:170-174`
assigns only on the out-of-range branch); outside → forced 400; `stoi`-tolerant (`"300abc"` → 300);
non-numeric non-map → throws → handler records parse error (`hl_cm:200-204`). Model
(`py:217-218`): `WEIGHTS.get(d.lower(), -1)` → every numeric declared labels mismatch. Divergent
labels: fresh option declared `400` → host live `400` (agreement), model mismatch; after `bold`,
declaring `700` → host live `700` (agreement), model mismatch. Host trees declare weights by name
(capture `:35-36` shows live `1000`/`400`), so the census is unaffected.

### F5 (medium) — strictness inversions, two of them crash the model rather than mislabeling

Host `std::stoi`/`std::stof` parse prefixes and ignore tails; model `int()` is all-or-nothing:

- gradient angle: `stoi("45.5")=45`, `stoi("4x5")=4` (`hl_cm:120`) vs `int("45.5")` → ValueError
  (`py:178`). In `model_equal` the ValueError is caught → `False` (`py:212-220`); in `live_of`
  (`py:316-330`, stub-table generation) it is **not** — a declared like `45.5deg` in a fixture
  generator input would crash the counter instead of scoring. Not reachable from the frozen
  generator (angles are generated from `("0deg","45deg","90deg",None)` and int priors).
- gap tokens: `stoi("5x")=5` (`cdt:95`) vs `int("5x")` ValueError (`py:190`) → caught → mismatch,
  while the host actually sets `5 5 5 5` (agreement truth).
- model-side crash: alpha `inf` → `int(round(inf))` raises **OverflowError**, which `py:133-136`
  does not catch (only ValueError) — `hl_int` crashes instead of returning `None`; host
  `std::stof("inf")` yields a value (implementation-defined cast, typically 0).

### F6 (medium) — the 10-colour cap is missing

Host keeps at most 10 colours and records a parse error beyond (`hl_cm:129-133`); `gradient_text`
is unbounded (`py:176-185`). An 11-colour declared: host toString has 10 words, model prints all
11 → mislabeled mismatch.

### F7 (medium) — channel masking, transparent fallback, and tokenizer semantics

- Host colours round-trip through `CHyprColor`: the ctor masks each byte
  (`((hex>>16)&0xff)/255.0`, `color.cpp:7-10,14-16`) and `getAsHex` truncates
  `sc<uint32_t>(x * 255.f)` (`color.cpp:30-33`). Verified lossless for all 256 in-range channel
  values (computed: zero losses), so sane words match. Out-of-range components diverge: `r=300` →
  host masks to 44 (0x2c), model prints the raw int (`py:186`).
- Zero-colour gradients: host falls back to one transparent black and still prints
  (`hl_cm:147-151`: `emplace_back(0)` → word `0`); model returns `None` (`py:184-185`).
- Tokenizer: handlers use `CVarList2(V, 0, ' ')` with default `removeEmpty=false`
  (`hl_cm:111,175`; `hu_varlist2.hpp:24-27`), so `"5  5"` splits to `["5","","5"]`
  (`hu_varlist2.cpp:57-59` keeps empties; each arg trimmed, backslash escapes processed) → gap
  size 3 → `stoi("")` throws → parse error, value stays `0 0 0 0` (`hl_cm:178-182`,
  `cdt:106-108`), while `declared.split()` (`py:176,190`) collapses to `[5,5]` → `5 5 5 5`.
  Single-space declareds tokenize identically. Gradient colour lists survive empty tokens (bad
  token skipped with parse error, `hl_cm:135-142`), so only the error flag differs there.

### F8 (low) — integer width: C++ throws where Python is unbounded

- hyprlang decimal path: `isNumber` gate then `std::stoll` (`cfg:265-271`) — `stoll` throws
  `out_of_range` beyond int64 → error; model `int(v)` (`py:165`) unbounded (e.g. declared
  `9223372036854775808` converts, host rejects).
- hyprlang hex path: `stoll(...,16)` inside `parseHex` (`cfg:186-194`) same; model `int(v,16)`
  (`py:125`) accepts `0xFFFFFFFFFFFFFFFF`.
- gap: `std::stoi` is 32-bit (`cdt:95`); `"3000000000"` throws → value unchanged; model produces
  `3000000000 3000000000 3000000000 3000000000`.

### F9 (low) — digit/whitespace character classes

- `isNumber2` allows `-` only at position 0 and ASCII `isdigit` only — no `+`, no whitespace, no
  Unicode (`hu_string.cpp:52-77`). Model `re.fullmatch(r"-?\d+", v)` (`py:164`): `\d` matches
  Unicode Nd — `"١٢"` converts to 12 in the model, errors on the host. `+12`/whitespace rejected
  by both (match).
- `trim` = `std::isspace` set (`hu_string.cpp:6-21`) vs Python `str.strip()`'s larger Unicode
  whitespace class (`py:129,132,148,151`): a trailing `\xa0` survives host trim (→ parse error)
  and is stripped by the model.

### F10 (low) — docstring citation drift (frozen text, so informational)

- `py:121` cites "config.cpp:185-264"; the function spans `cfg:185-274`.
- `py:170` cites "ConfigManager.cpp:103-170"; the gradient handler is `hl_cm:103-162` (destroy
  163-166; line 170 is inside `configHandleGapSet`).
- `py:20-22` cites ComplexDataTypes.hpp "69-77, 80-136, 154-175"; at efb5099 the actual anchors are
  gradient `toString` `cdt:69-77` (correct), gap class `cdt:80-136` (correct), weight class
  `cdt:138-174` (cited 154-175).

## Confirmed matches (the task's named checks that pass)

- rgba comma form precedence over the 8-hex form: comma-count check first in both — `cfg:201-220`
  vs `py:130-139` (and `parseColor` likewise comma-first, `pu:74-88`); 8-hex RGBA→ARGB shuffle
  `(x>>8) + 0x1000000*(x&0xFF)` identical `cfg:220-227` vs `py:140-145`.
- `starts_with("on")` semantics: exact prefix family match — `cfg:259-263`
  (`starts_with("true")||("on")||("yes")` → 1; `("false")||("off")||("no")` → 0) vs `py:160-163`;
  `only`→1, `normal`/`north`→0, `yes, please :)`→1, `on # note`→1 all agree; disjoint prefixes make
  order irrelevant (match).
- Negative numbers / isNumber rules: for ASCII in-range strings, `isNumber2` (`-` only at i==0,
  digits only, full consumption, `hu_string.cpp:52-77`) ≡ `re.fullmatch(r"-?\d+")` (`py:164`);
  `+`, spaces, empty, trailing junk rejected by both. Range (F8) and Unicode (F9) are the only
  escapes.
- Inherited-angle rule: confirmed in source. `*data` persists across declarations and is created
  once (`hl_cm:105-107`); `m_colors.clear()` every call (`hl_cm:112`); `m_angle` is written only
  inside the `deg` branch (`hl_cm:117-123`) and defaults to 0 on fresh data (`cdt:55`); the `deg`
  token is terminal (`break`, `hl_cm:127`) and detected by substring containment
  (`find("deg") != npos` ≡ `"deg" in tok`, `py:177`). Model's `inherited` param with default 0
  (`py:169,175`) matches fresh-vs-redeclare semantics exactly.
- toString shape: per-colour `"{:x} "` lowercase unpadded + `"{...}deg"` (`cdt:69-77`) ≡
  `" ".join("%x" % c) + " %ddeg" % angle` (`py:186`) — for in-range 8-bit colours and safe angles
  the strings are byte-identical (channel round-trip verified lossless, see F7).
- gap_text: CSS expansion via constructors (`cdt:82-86` ≡ `py:191-198`: 1→all, 2→v/h, 3→t/h/b,
  4→t/r/b/l) and >4 → first four with warning (`cdt:114-117` ≡ `py:197` `n[:4]`); toString
  `"{} {} {} {}"` of int64 (`cdt:133-135`) ≡ `str(int)` join.
- WEIGHTS: all 12 name→value pairs byte-identical (`cdt:158-161` ≡ `py:96-98`); case-insensitivity
  (`::tolower` map lookup, `cdt:164-168` ≡ `.lower()`, `py:218`); `toString` of int64 ≡ `str(int)`
  (`cdt:154-156`). (The numeric-`stoi` fallback is F4.)
- `hl_int` branch order and packing arithmetic otherwise mirror `cfg:185-274` 1:1 (0x → rgba( →
  rgb( → true-family → false-family → decimal), including recursive component parsing
  (`cfg:205-209,239-243` ≡ `py:132,150`) and `0xFF000000` defaulting for rgb forms
  (`cfg:247-251` ≡ `py:153,156,159`).

## Residual risk and verification gaps

- hyprutils sources were read from `main` (no exact pin exists: Hyprland efb5099 requires
  `hyprutils >= 0.14.0`, its CMakeLists:150; hyprlang v0.6.8 requires `>= 0.7.1`). `isNumber2`,
  `VarList2`, `strToNumber` behaviour is cited from `main` hashes; a materially older installed
  hyprutils could differ in these helpers (low risk: the functions are small and stable).
- hyprlang's handling of errored-but-mutated custom values (handler mutates `*data` *and* returns
  a parse error) is not traced here; it affects labels only for malformed declareds, which no
  fixture or host tree contains.
- strToNumber's integral branch is template code behind `std::from_chars` (libc++ fallback path
  unread); the x86/glibc host path is what I cite. `from_chars` for unsigned accepts `-` with
  wraparound — not reflected anywhere in the model, subsumed by F1/F8.
- The census numbers (62/8/0) and the live receipt are out of my scope and not re-derived; the
  capture spot-check (`0deg`/`45deg` only, 8-digit colours, named weights, canonical gaps) is
  consistent with none of F1-F9 biting the census.

## Claim impact

PRED-C1-r40-v1's fixtures deliberately avoid every divergent input class: alphas `1/0.8/0.4`
(`py:228`, exact under both rounding rules), angles {0,45,90,135,270} (safe set of F2), weight
names only (`WSPELL`, `py:235`), 1-4 single-space gap tokens, in-range 8-digit colours. The 13
fixtures and clause checks are therefore sound as declared, and the live host receipt is
consistent with the model on this tree. The findings extend the declared residual (a tool
"that hardcodes the reference model's conversion tables for this generator's value space") with
concrete out-of-distribution inputs and two upstream facts worth carrying into the C2 entry's
conversion text if the integrator chooses: gradient colours go through `ParserUtils::parseColor`
(not hyprlang `configStringToInt`), and printed angles pass through a truncating float32 radian
round-trip.
