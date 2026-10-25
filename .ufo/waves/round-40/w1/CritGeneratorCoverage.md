# CritGeneratorCoverage — what a wrong tool can get right on the C1 generator

Seat: `CritGeneratorCoverage` (w1, round 40). Lane `/home/vgpnk/Projects/shokunin/mado-shokunin`.
Claims frozen at `5e7e885` (base `9fc511d`); lane tip at review `e2b51d3`.

**Verdict: the generator's value space is not the host's value space.** 16 mutations of the
frozen reference live tool, each wrong only on one real spelling/structural class the generator
never emits, all score **`fixtures=13/13`** on `PRED-C1-r40-v1` *and* mislabel the class when
driven against a stub that does emit it (`CGC: mutants=16 blind_and_wrong=16/16`). Three of
those classes are also mislabelled by the **frozen reference model itself** (which the counter
shares verbatim), so the counter cannot see them even in principle: the gradient alpha
conversion, numeric font weights, and the fifth reply form `vec2`. The `vec2` finding falsifies
two claim sentences and one clause-k property (details §D), and it is the only finding here
that is *not* a fixture-space gap but a live-behaviour defect.

Nothing in the lane, the fleet repo, a config tree or the compositor was mutated. No package
transaction. Tools installed: none (used the preinstalled `hyprctl`, `python3`, `curl`).

## Method (reproducible)

- Counter, unmodified: `python3 -I quality/counters/c1-r40-live.py --repo <lane> --rev master
  --tool <mutant>` — the same `--tool` switch the round's own controls use.
- Mutants are byte-derived from the frozen control `.ufo/waves/round-40/c1/ctl-ref-tool.py.txt`
  (the reachability proof, never delivered) with exactly one string replacement; the harness
  refuses a mutant whose target does not occur exactly once.
- Each mutant is then run `--live --hyprctl <stub>` on a hand-built `--home` that *does* use the
  class, and the row label is compared to the reference's. A class counts as proven when the
  reference says `agreement` (the truth: the declared value produces that live value) and the
  mutant does not.
- Harness + transcript: `.ufo/waves/round-40/w1/CritGeneratorCoverage/attack.py`,
  `.../attack.log`. Reference baseline re-derived: `REF fixtures=13/13`.
- Host evidence: read-only `hyprctl getoption -j KEY` (the only compositor verb used), the host
  config trees, the frozen `c1/native-capture.jsonl`, the fetched sources in
  `.ufo/waves/round-40/fetch/`, and upstream files at the pinned commit
  `efb50993780079460b0cbed1363e2166a2de1d9f` (`src/config/shared/parserUtils/ParserUtils.cpp`,
  `tests/config/shared/ParserUtils.cpp`, `src/config/values/ConfigValues.cpp`,
  `src/config/shared/complex/ComplexDataTypes.hpp`).

## A. What the generator actually emits (frozen counter, `quality/counters/c1-r40-live.py`)

| form | emitted spellings | where |
|---|---|---|
| int | 10 bool words incl. prefix forms `yes, please :)`, `on # note`; decimal `2..900`; negative `-5..-1`; `rgb(6hex)`; `rgb(r,g,b)`; `rgba(8hex RRGGBBAA)`; `rgba(r,g,b,a∈{1,0.8,0.4})`; `0x8hex ARGB` with alpha `0x10..0xff` | `:224-235`, `:251-282` |
| float | `%.2f` in `[0,3)` and `%d.%d0` (quirk) — **always exactly 2 decimals, non-negative** | `:275-277` |
| str | `w\d{5}` only | `:278-280` |
| custom/gradient | 1–3 colours, angle **last**, `∈{0deg,45deg,90deg}` or absent with inherited `∈{45,90,135,270}` | `:285-295` |
| custom/gap | 1–4 values, `0..40` | `:296-299` |
| custom/weight | the 12 lowercase names | `:235`, `:300` |
| keys | exactly one colon, one category level (`optN1:kind1`) | `:262` |
| tree | one flat file; `bind`, `env`, `#`-comment distractors | `:372-374` |
| reply | `{"option","set",form}` with form ∈ `("int","float","str","custom")` | `:99`, `:406` |

`ALPHAS = ("1", "0.8", "0.4")   # alpha*255 is an exact integer: no rounding ties` (`:228`) is
the generator admitting the exclusion that §C exploits.

## B. Real classes the generator never emits — 16 mutants, each 13/13 and wrong on the class

Tier **H** = observed in the host's own trees/replies now; **G** = accepted by the pinned
grammar (a real spelling a user can write), not present in the current host tree.

| # | class | tier | evidence | mutant | counter | probe (ref → mutant) |
|---|---|---|---|---|---|---|
| X01 | fifth reply form `vec2` | **H** | `hyprctl getoption -j decoration:shadow:offset` → `{"option": "decoration:shadow:offset", "vec2": [0,0], "set": false}` | unknown form → `return None` (config-only) instead of `CtlError` | 13/13 | rc5 → `config-only` |
| X02 | float declared with ≠2 decimals / bare int | **H** | `default/hypr/input.conf:11 sensitivity = 0` (live `0.0`); `.config/hypr/input.conf:34 scroll_factor = 0.4`; `looknfeel.conf:44,45,116` `0.60/0.75/0.49` | require `len(d.partition(".")[2]) == 2` | 13/13 | `agreement` → `mismatch` |
| X03 | empty str | **H** | `default/hypr/input.conf:4,5,7` `kb_variant/kb_model/kb_rules =` (live `"str": ""`) | `bool(d) and d == live` | 13/13 | `agreement` → `mismatch` |
| X04 | str containing spaces | G (+H value shape) | `.config/hypr/hyprlock.conf:29 font_family = JetBrainsMono Nerd Font`; `group:groupbar:font_family` is a getopt str key | compare `d.split()[0]` | 13/13 | `agreement` → `mismatch` |
| X05 | uppercase weight name | **G** | `ComplexDataTypes.hpp:163-169` `parseWeight` lowercases before lookup | drop `.lower()` | 13/13 | `agreement` → `mismatch` |
| X06 | numeric weight | **G** | `ComplexDataTypes.hpp:171` falls back to `std::stoi` | reject `d.isdigit()` | 13/13 | `mismatch` → `mismatch` (ref is already wrong, §C) |
| X07 | gradient with 4+ stops | **G** | `ConfigManager.cpp:129-131` handler allows up to 10 colours | truncate `cols[:3]` | 13/13 | `agreement` → `mismatch` |
| X08 | gap with negatives | **G** | `ComplexDataTypes.hpp:95` `toInt = std::stoi` (negatives kept) | shape guard `t.isdigit()` (no `-`) | 13/13 | `agreement` → `mismatch` |
| X09 | gap with 5+ values | G (error case) | `ComplexDataTypes.hpp:114-118` `default:` uses `varlist[0..3]` | reject `len(n) > 4` | 13/13 | `agreement` → `mismatch` |
| X10 | short `0x` hex (`0xff0000`, `0x1`) | **G** | `ParserUtils.cpp` `parseHex` → `strToNumber<uint64_t>`: any hex length; gtest `parseColor("1") == 0x1`. The generator itself writes `0x1` (`:364`) but only as a *shadow* declarer, never as a compared value | require `len(v) == 10` | 13/13 | `agreement` → `mismatch` |
| X11 | uppercase hex digits | **G** | `parseHex`/`strToNumber` are case-insensitive; gtest `parseColor("#DEFFaDAA") == 0xAADEFFAD` | reject `inner != inner.lower()` | 13/13 | `agreement` → `mismatch` |
| X12 | negative gradient angle | **G** | `ConfigManager.cpp:120` angle = `std::stoi(token before "deg")` | accept angle only if `.isdigit()` | 13/13 | `agreement` → `mismatch` |
| X13 | keys with two colons | **H** | 29 of the host's 70 keys (`native-capture.jsonl`: `decoration:blur:brightness`, `group:groupbar:*`, `input:touchpad:scroll_factor`) | collapse `a:b:c` → `a:c` in `declare` | 13/13 | `agreement` → row absent (wrong key queried) |
| X14 | `$variable` in a value | **H** | `.config/omarchy/current/theme/hyprland.conf:1,4` and `default/hypr/looknfeel.conf:4,15`; 6 of the 70 declared values arrive only after expansion (`general:col.*`, `group:col.border_*`), one of them a 2-stop gradient | skip the `$` substitution into `rhs` | 13/13 | `agreement` → `mismatch` |
| X15 | `source =` layering (incl. globs) | **H** | `.config/hypr/hyprland.conf:4-32`, incl. `:23 source = ~/.local/state/omarchy/toggles/hypr/*.conf`; every one of the 70 keys except the main file's arrives through it | `handle_source` returns without parsing | 13/13 | `agreement` → row absent |
| X16 | `{{ expr }}` arithmetic | **G** | hyprlang v0.6.8 `config.cpp:619` `parseExpression`; `ComplexDataTypes` gaps via `std::stoi` | skip `expand_expressions` | 13/13 | `agreement` → `mismatch` |

Consequences for the claim, in the claim's own words:

- "`--live` … native replies (forms `int|float|str|custom`, or the text `no such option`)
  compared after host-style conversion" — **false as a universal**: a fifth form `vec2` exists
  (X01, §D), and the "host-style conversion" is not one function: gradient tokens are
  `ParserUtils::parseColor` (`std::floor` on alpha, `#`-hex, bare-number), int options are
  hyprlang `configStringToInt` (`std::round`, no `.` in numbers). The model uses one `hl_int`
  with `round` for both (§C).
- The fixture space cannot distinguish any of X01–X16, so `fixtures=13/13` is not evidence that
  the tool's conversion is the host's.

## C. The reference model itself is wrong on three real classes (not mutants)

Same harness, reference tool only (`MODEL …` lines in `attack.log`). These are defects of
`hl_int`/`gradient_text` in `quality/counters/c1-r40-live.py:120-218`, shared by the reference
tool, so no mutant is needed — the counter's own model produces the wrong label.

1. **`P1-alpha-floor-vs-round`** — `general:col.active_border = rgba(20,21,22,0.5) 0deg`.
   Hyprland's gradient handler parses each token with `ParserUtils::parseColor`, whose comma
   branch is `std::floor(*a * 255.F)` (`ParserUtils.cpp:88`, fetched) and whose own gtest asserts
   `parseColor("rgba(20, 21, 22, 0.5)") == 0x7F141516`. The model does
   `int(round(float(a)*255.0))` → `0x80141516`. Against a stub emitting the true
   `"7f141516 0deg"` the reference reports **`mismatch`** where the truth is `agreement`.
   Same divergence for `0.9` (floor 229, model 230).
   The int-option path (`configStringToInt`) genuinely uses `std::round` — so the two paths
   *disagree with each other* on the same spelling, and one `hl_int` cannot serve both.
   On int options the model additionally uses Python's banker's rounding where C++ rounds half
   away from zero: `0.3` → 76.5 → C++ 77, model 76; `0.7` → 178.5 → C++ 179, model 178.
2. **`P2-numeric-weight`** — `group:groupbar:font_weight_active = 700`, live `"700"`.
   `parseWeight` lowercases, misses the name table, and falls back to `std::stoi`
   (`ComplexDataTypes.hpp:171`); out-of-range values clamp to 400 (`:172-173`). The model
   returns `-1` for anything that is not a name → **`mismatch`** where the truth is `agreement`.
3. **`P3-vec2-reply`** — see §D.

Because these three are inside the model, the declared residual ("a tool that hardcodes the
reference model's conversion tables for this generator's value space passes the fixtures") is
weaker than stated: hardcoding the model is not merely untested out-of-distribution, it is
**known-wrong** on three classes.

## D. Clause k cannot admit a truthful capture that contains a `vec2` reply

`capture_ok` (`:598`) requires `len(forms) == 1` with `forms ⊆ FORMS = ("int","float","str","custom")`
(`:99`). Direct check against the frozen module:

```
capture_ok(real 70-key capture)                       = True
capture_ok(70 keys, one real vec2 reply)              = False
```

The reply used is verbatim what the host answered:
`hyprctl getoption -j decoration:shadow:offset` → `{"option": "decoration:shadow:offset",
"vec2": [0,0], "set": false}` (also `input:tablet:region_size`,
`input:tablet:active_area_position`, `layout:single_window_aspect_ratio` — all `vec2`, all
`set:false` on this host; the option names are real: `ConfigValues.cpp:215,364-374,653`).
So: if the user declares any vec2 option, (a) the delivered tool exits **5** naming a key —
reporting a compositor failure on a healthy compositor — and (b) a capture that includes that
key fails clause k. The 70-key census avoids both only because no vec2 option is declared on
this host today.

## E. Examples from the task that are NOT real classes (tested, rejected)

- **`int` option spelled `1.0`** — hyprlang v0.6.8 `configStringToInt` ends with
  `if (VALUE.empty() || !isNumber(VALUE, false)) return error` (`config.cpp:265`), and
  `isNumber2(str, /*allowfloat=*/false)` returns false on any `.` (hyprutils
  `String.cpp`, fetched). `1.0` for an int option is a **parse error**, not a spelling. The
  mirror class *is* real and is covered by X02: a **float** option spelled `0`/`1` (host:
  `input:sensitivity = 0` → live `0.0`), because float options go through `std::stof`
  (`config.cpp:467`).
- **`#`-hex colours (`#fed`, `#DEFFaDAA`)** — `parseColor` accepts them
  (`tests/config/shared/ParserUtils.cpp`), but `#` opens a comment in the config grammar, so a
  `#`-colour can never survive into a declared value. Not a config class; do not add.
- **vec2** — confirmed, not rejected: see §D. It is a *reply* class (and a key class), never a
  value the generator's stub can produce.

## F. Realism caveat: declared + `set:false` has no host counterpart

Two of the nine generated kinds per fixture carry `set:false` **while being declared in the
fixture tree** (`Fixture.table`: `"set": o["lab"] != "unset"`, `:384`). On the host, every one of
the 70 declared keys reports `set:true` — including `input:kb_model`, whose declared value equals
the empty default (`native-capture.jsonl`). A valid declaration is therefore always `set:true`
in practice; the only route to declared+`set:false` is a line hyprlang rejects. Control M08
(`set` ignored) makes "derive `set` from my own parse" fail, i.e. the fixture rewards trusting
the reply's `set` over the tool's own parse — defensible, but it is a *synthetic* state, and it
is the one place where a host-faithful tool is scored as wrong. Not a defect to fix by
narrowing; record it as a declared design choice.

## G. Impacted axes and the smallest safe corrections

Operability (C1) is the axis at risk; coverage (C2) inherits the same fact.

1. **`vec2` (blocking, smallest fix):** add `"vec2"` to `FORMS` and to the reply parser, compare
   it component-wise as two floats (`[x,y]`), keep `no such option` as config-only, and reserve
   exit 5 for a *non-zero exit / non-JSON / malformed record*. Then extend `capture_ok` to admit
   a `vec2` record. Without this, the claim's form sentence is false and a user with
   `decoration:shadow:offset = 5, 5` gets a false compositor failure. (C2's entry must then not
   say "the four native forms" — see the hand-off below.)
2. **Split the conversion:** `parse_color_token` (gradient tokens: `std::floor(a*255)`, `#`-hex
   unreachable, bare numbers, `0x` any length, case-insensitive) vs `config_int` (int options:
   `std::round`, half away from zero, no `.`). Add one fixture kind per divergence: alpha `0.5`
   and `0.3`; a 4-stop gradient; a `0xff0000` token; `rgba(EE1A1AEE)`.
3. **Widen the spelling generator** (one new kind each, keeping the 13-fixture shape): float
   `0.4`/`0`/`1e-2`; str `''` and a spaced value; weight `700` and `Bold`; gap `-1` and
   `1 2 3 4 5`; a two-colon key; a `$var` indirection; a `source =` include (with a glob); one
   `{{ 2 + 3 }}` value. Each of X02–X16 becomes a scoring mutant the round can reuse.
4. **Do not** add `1.0`-as-int or `#`-hex fixtures (E).

## H. Hand-off (one line each)

- **C1 tool/L1:** §G.1 is a live-behaviour defect, not a fixture gap; it should be fixed in the
  delivered tool and reflected in the registration sentence, or the claim's form enumeration is
  false. §C.1 (floor vs round) changes the tool's *host* labels; §C.2 changes numeric weights.
- **C2 entry owner:** the entry's sentence "the four native forms and `no such option`" is
  falsified by host evidence (§D). Say "the four value forms of the declared option table, plus
  `vec2` for vec2-typed options (`decoration:shadow:offset`, `input:tablet:*`,
  `layout:single_window_aspect_ratio`), plus the text `no such option`". C2's clauses a–h do not
  test this sentence, so it can pass while being wrong — that is the premature-saturation risk
  this seat exists to flag.

## Files written (seat dir)

- `.ufo/waves/round-40/w1/CritGeneratorCoverage.md` (this report)
- `.ufo/waves/round-40/w1/CritGeneratorCoverage/attack.py` (harness, 16 mutants + 3 model probes)
- `.ufo/waves/round-40/w1/CritGeneratorCoverage/attack.log` (transcript:
  `REF fixtures=13/13`, `CGC: mutants=16 blind_and_wrong=16/16`, `MODEL … defect=1` ×3)
