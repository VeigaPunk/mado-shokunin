# Native `getoption` forms over the WHOLE option set — census summary

Seat `ExecAllOptionsForms`, mado round 40 / hyaku run 7 / w1, 2026-10-25.
Host: Hyprland 0.56.2, commit `efb50993780079460b0cbed1363e2166a2de1d9f`, hyprlang 0.6.8.

## Method (all read-only)

1. `hyprctl descriptions -j` → 353 option names (`descriptions-r40.json`, sha256
   `4aa2745c11b92d36abbf5355f2dc9217ed54e143a2f0621e0cc7a2b3e2652aab`; byte-identical on a
   second invocation). 353 names, 353 unique, every name a non-empty string; entry keys are
   `{name, description, default, current, min, max, map}`.
2. `hyprctl getoption -j <name>` once per name, serially, in `descriptions` order →
   `raw-census.jsonl` (353 rows: `i`, `name`, `rc`, `stdout`, `stderr`). Second full pass →
   `raw-census-2.jsonl`; the two files are byte-identical (sha256
   `c1e82034000f53c8b9eb6e687e27cf4408cfe38e7f6da842e0884a48bd8fbcf5`).
3. Strict parse: `JSONDecoder.raw_decode` on the stripped reply, then require the remainder to be
   empty (so "exactly one JSON object, nothing else") and the value to be a `dict`.

## Result — 353/353 answered

| form | all 353 | declared 70 | not in capture (283) |
|---|---|---|---|
| `int` | 264 | 44 | 220 |
| `float` | 34 | 5 | 29 |
| `str` | 28 | 8 | 20 |
| `custom` | 21 | 13 | 8 |
| **`vec2`** | **6** | **0** | **6** |
| total | 353 | 70 | 283 |

- `rc` = 0 for all 353; `stderr` empty for all 353.
- Replies that are not exactly one JSON object: **0**.
- Replies with **no** form: **0**. Replies with **more than one** of the four forms: **0**.
  Under the counter's four-form lens (`int|float|str|custom`) the "no form" list is **not** empty:
  it is exactly the six `vec2` keys below, and nothing else.
- `option` field always equals the requested name (0 mismatches). `set` present in all 353:
  70 `true` (exactly the declared table) / 283 `false`.
- Value types: `int` → JSON int (264), `float` → JSON number (34), `str` → JSON string (28),
  `custom` → JSON string (21), `vec2` → **JSON array** (6).

## The fifth form: `vec2`

Six keys answer `{"option": K, "vec2": [x, y], "set": false}`:

```
decoration:shadow:offset            [0,0]
input:tablet:region_position        [0,0]
input:tablet:region_size            [0,0]
input:tablet:active_area_size       [0,0]
input:tablet:active_area_position   [0,0]
layout:single_window_aspect_ratio   [0,0]
```

Corroboration that this is a first-class type, not an artifact:
- `hyprlang.hpp:282-288` — `enum eDataType { CONFIGDATATYPE_EMPTY, INT, FLOAT, STR, VEC2,
  CUSTOM }`; `VEC2` is `SVector2D` (`hyprlang.hpp:45`).
- `/usr/include/hyprland/src/config/values/types/Vec2Value.hpp:20` — `class CVec2Value`, i.e. the
  same value registry `descriptions -j` enumerates. `ConfigValues.hpp:25-26` validates `Config::VEC2`.
- `descriptions -j` independently marks these six by `"default"`/`"current"` being JSON arrays
  (`[0, 0]`) while every scalar option carries a scalar there.

## Does "exactly four forms" hold?

- Over the 70 declared keys and over the frozen capture: **yes, exactly**. Re-derived from the
  live compositor: `int 44 / float 5 / custom 13 / str 8` — the provisional fact verbatim. The
  70-key subset of the census agrees with `.ufo/waves/round-40/c1/native-capture.jsonl` on form,
  `set` and value for **all 70 keys, 0 disagreements** (floats compared parsed, not as text).
- Over the whole option set: **no**. There are **five** reply forms, `vec2` being the fifth, on 6
  of 353 names. So `FORMS = ("int","float","str","custom")`
  (`quality/counters/c1-r40-live.py:99`) and the docstring's "the four forms captured from the
  real compositor" are census-scoped truths, not properties of the compositor's option set.

## Keys the frozen capture could not have contained

283 names — every option not declared in the host config tree (`not-in-capture.tsv`). The capture
is exactly the declared-70 set (verified both directions: 0 capture keys undeclared, 0 declared
keys missing). Of the 283, six carry `vec2`; none is `set: true`.

## Files

| file | sha256 |
|---|---|
| `forms.tsv` (name, form, set, value; 353 rows + header) | `e26deb4aac35939bfd6343b093975227049d0fff173c4e3ada1f40138a8b2c66` |
| `raw-census.jsonl` / `raw-census-2.jsonl` (identical) | `c1e82034000f53c8b9eb6e687e27cf4408cfe38e7f6da842e0884a48bd8fbcf5` |
| `descriptions-r40.json` | `4aa2745c11b92d36abbf5355f2dc9217ed54e143a2f0621e0cc7a2b3e2652aab` |
| `not-in-capture.tsv` (283 rows) | `47362ef8585b5428d8f03b72ef58338ae69001b91c5a49295d81efadd600bab9` |
| `summary.json` | `5a2ba509fde2e1b575906c737fa8de7fb099d47ede76b9bca73ec15c6520341a` |

TSV hygiene: every row has exactly 3 tabs; no value contains a tab or newline; 4 `str` values are
legitimately empty (`general:locale` set=false, `input:kb_model`, `input:kb_variant`,
`input:kb_rules` set=true) — the empty string is a real reply, not a parse failure.

## Boundary (honest limits)

- One host, one compositor state, one moment. `set` reflects the loaded config.
- All six `vec2` keys are **unset**; a *set* `vec2` value was never observed, and producing one
  would need a compositor mutation, which is out of bounds here. Whether a set `vec2` prints
  `[x,y]` under the same `vec2` form is `[INFERENCE]`, not measured.
- `CONFIGDATATYPE_EMPTY` was never observed as a reply form (0 keys without a form), so the
  theoretical sixth shape is unmeasured.
- Source-level completeness beyond the 50 names quoted in
  `/usr/include/hyprland/src/config/values/ConfigValues.hpp` is not checkable here: only headers
  are installed, no `HyprCtl.cpp`/`ConfigValues.cpp`. All 50 header names are inside the 353.
- `no such option` is plain text with exit 0 — reproduced on `nosuch:option` and
  `general:nosuch`. No name from `descriptions -j` produced it.
