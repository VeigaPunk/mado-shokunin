# Source receipt quotes — hyprlang v0.6.8 `src/config.cpp` (held row S173 re-opened)

Receipt bytes: `.ufo/waves/round-40/fetch/hyprlang-config-v0.6.8.bin`
- URL: `https://raw.githubusercontent.com/hyprwm/hyprlang/v0.6.8/src/config.cpp`
- HTTP 200, `content-type: text/plain; charset=utf-8`, fetched 2026-10-25T20:48:47Z, 43049 bytes, 1158 lines.
- sha256 `fa1b6898f2f1676de73220450f18f09603f0c3f8833e4c0a7c42c12aebe1de3e`
- md5 `b88997b264c7b9245a7ffe75d3314702`

Every quote below is verbatim from that file, located by line number, and was verified with
`grep -nF -- '<quote>' .ufo/waves/round-40/fetch/hyprlang-config-v0.6.8.bin` (each reported match count is the
`grep -cF` result: 1 = unique in the file). Word counts are `printf '%s' "<quote>" | wc -w`.

## Function anchor

| line | words | quote |
|---|---|---|
| 185 | 7 | `static std::expected<int64_t, std::string> configStringToInt(const std::string& VALUE) {` |

`configStringToInt` body spans lines 185–273 (the `0x` branch is first, then `rgba(`, then `rgb(`, then the
boolean names, then `stoll`).

## `rgba(` branch

| line | words | quote |
|---|---|---|
| 198 | 7 | `} else if (VALUE.starts_with("rgba(") && VALUE.ends_with(')')) {` |
| 202 | 7 | `if (std::count(VALUEWITHOUTFUNC.begin(), VALUEWITHOUTFUNC.end(), ',') == 3) {` |
| 213 | 6 | `a = std::round(std::stof(trim(rolling.substr(0, rolling.find(',')))) * 255.f);` |
| 219 | 14 | `return (a * (Hyprlang::INT)0x1000000) + (r.value() * (Hyprlang::INT)0x10000) + (g.value() * (Hyprlang::INT)0x100) + b.value();` |
| 227 | 10 | `return (RGBA.value() >> 8) + (0x1000000 * (RGBA.value() & 0xFF));` |
| 230 | 14 | `return std::unexpected("rgba() expects length of 8 characters (4 bytes) or 4 comma separated values");` |

Branch shape: 4 comma-separated values → `(a<<24)|(r<<16)|(g<<8)|b`; 8 hex chars → RGBA→ARGB rotation; anything
else is an error. (Line 230 is the branch's reject path; it names the accepted shapes.)

## `rgb(` branch

| line | words | quote |
|---|---|---|
| 232 | 7 | `} else if (VALUE.starts_with("rgb(") && VALUE.ends_with(')')) {` |
| 236 | 7 | `if (std::count(VALUEWITHOUTFUNC.begin(), VALUEWITHOUTFUNC.end(), ',') == 2) {` |
| 248 | 12 | `return (Hyprlang::INT)0xFF000000 + (r.value() * (Hyprlang::INT)0x10000) + (g.value() * (Hyprlang::INT)0x100) + b.value();` |
| 255 | 4 | `return RGB.value() + 0xFF000000;` |
| 258 | 14 | `return std::unexpected("rgb() expects length of 6 characters (3 bytes) or 3 comma separated values");` |

Branch shape: 3 comma-separated values or 6 hex chars, opaque alpha `0xFF` forced in both arms.

## `true` / `on` / `yes` → 1

| line | words | quote |
|---|---|---|
| 259 | 9 | `} else if (VALUE.starts_with("true") || VALUE.starts_with("on") || VALUE.starts_with("yes")) {` |

The branch's single statement is `return 1;` on line 260 (verified: `grep -nF 'return 1;'` → `260:        return 1;`;
2 words, below the 3-word floor, so quoted here as an adjacent line reference rather than as a quote).
Note the test is `starts_with`, not equality: any value beginning with `true`/`on`/`yes` converts to 1.

## `false` / `off` / `no` → 0

| line | words | quote |
|---|---|---|
| 261 | 9 | `} else if (VALUE.starts_with("false") || VALUE.starts_with("off") || VALUE.starts_with("no")) {` |

The branch's single statement is `return 0;` on line 262 (verified: `grep -nF 'return 0;'` → `41:`, `262:`, `273:`;
262 is the one inside this branch). Same `starts_with` prefix semantics.

## `0x` hex branch

| line | words | quote |
|---|---|---|
| 195 | 3 | `if (VALUE.starts_with("0x")) {` |
| 196 | 6 | `// Values with 0x are hex` |
| 197 | 2 | `return parseHex(VALUE);` (2 words — below floor; listed as adjacent line reference, not a quote) |

The `0x` arm delegates to the `parseHex` lambda at lines 186–194 (`auto   result = stoll(value, &position, 16);` at
189 with a full-length check at 190, else `return std::unexpected("invalid hex " + value);` at 193). It is tested
**first**, before any colour or boolean form.

## Order of tests (what a re-opened row must cite)

1. line 195 `0x` → hex
2. line 198 `rgba(` → ARGB
3. line 232 `rgb(` → opaque ARGB
4. line 259 `true|on|yes` → 1
5. line 261 `false|off|no` → 0
6. lines 265–272 fallthrough: `if (VALUE.empty() || !isNumber(VALUE, false))` (265), error
   `return std::unexpected("cannot parse \"" + VALUE + "\" as an int.");` (266), then `std::stoll(VALUE)` (269)

## Scribe candidate check (requested by ScrFormsEntryA, Gate line for S173)

| line | words | matches | quote |
|---|---|---|---|
| 226 | 13 | 1 | `// now we need to RGBA -> ARGB. The config holds ARGB only.` |

Preferred Gate quote: line 226 — 13 words, unique, and free of `<…>` so no HTML-ish normalisation hazard.
`static std::expected<int64_t, std::string> configStringToInt(const std::string& VALUE) {` (line 185, 7 words,
matches=1) is confirmed too but carries `<int64_t, std::string>`; line 198 (`else if (VALUE.starts_with("rgba(") &&
VALUE.ends_with(')')) {`, 6 words, matches=1) is confirmed verbatim and safe.

## grep -F verification log (all run against the round-40 receipt)

```
198:    } else if (VALUE.starts_with("rgba(") && VALUE.ends_with(')')) {           matches=1 words=7
202:        if (std::count(VALUEWITHOUTFUNC.begin(), VALUEWITHOUTFUNC.end(), ',') == 3) {   matches=1 words=7
213:                a = std::round(std::stof(trim(rolling.substr(0, rolling.find(',')))) * 255.f);  matches=1 words=6
219:            return (a * (Hyprlang::INT)0x1000000) + (r.value() * (Hyprlang::INT)0x10000) + (g.value() * (Hyprlang::INT)0x100) + b.value();  matches=1 words=14
227:            return (RGBA.value() >> 8) + (0x1000000 * (RGBA.value() & 0xFF));   matches=1 words=10
230:        return std::unexpected("rgba() expects length of 8 characters (4 bytes) or 4 comma separated values");  matches=1 words=14
232:    } else if (VALUE.starts_with("rgb(") && VALUE.ends_with(')')) {            matches=1 words=7
236:        if (std::count(VALUEWITHOUTFUNC.begin(), VALUEWITHOUTFUNC.end(), ',') == 2) {   matches=1 words=7
248:            return (Hyprlang::INT)0xFF000000 + (r.value() * (Hyprlang::INT)0x10000) + (g.value() * (Hyprlang::INT)0x100) + b.value();  matches=1 words=12
255:            return RGB.value() + 0xFF000000;                                    matches=1 words=4
258:        return std::unexpected("rgb() expects length of 6 characters (3 bytes) or 3 comma separated values");  matches=1 words=14
259:    } else if (VALUE.starts_with("true") || VALUE.starts_with("on") || VALUE.starts_with("yes")) {   matches=1 words=9
261:    } else if (VALUE.starts_with("false") || VALUE.starts_with("off") || VALUE.starts_with("no")) {  matches=1 words=9
195:    if (VALUE.starts_with("0x")) {                                             matches=1 words=3
196:        // Values with 0x are hex                                              matches=1 words=6
185:static std::expected<int64_t, std::string> configStringToInt(const std::string& VALUE) {  matches=1 words=7
```

## S173 row check

`grep -n '^| S173 ' corpus/SOURCES.md` → line 185 of `corpus/SOURCES.md`:

```
| S173 | Hyprlang v0.6.8 expression evaluation — https://raw.githubusercontent.com/hyprwm/hyprlang/v0.6.8/src/config.cpp | code | A | Hyprlang RHS `{{…}}` expression parsing relevant to bind config values; not bind-table semantics | `src/config.cpp:619-667,755-827,983-986 @ 3a1c1b25b059dae2c6bbc46991562ba1158d125c, sha256:fa1b6898f2f1676de73220450f18f09603f0c3f8833e4c0a7c42c12aebe1de3e, 43049 B` | Documents the single-operator float evaluator, variable lookup, escaped expression starts, default result formatting, and parse-error propagation | mined | 2026-10-23 | on-release | tools/mado-binds.py, corpus/knowledge/config-option-table-r39.md |
```

- **URL:** yes — the row names exactly `https://raw.githubusercontent.com/hyprwm/hyprlang/v0.6.8/src/config.cpp`.
- **sha256:** yes — the row records `fa1b6898…e1de3e`, equal to the fetched bytes' sha256.
- **size:** yes — the row records `43049 B`, equal to the fetched `stat -c %s`.
- **located lines:** the row cites `619-667,755-827,983-986` (expression evaluation), which does **not** include
  `configStringToInt` at 185–273. The re-opened use needs the location above added; the row's existing lines stay
  valid for what they already support.
- **r39 receipt equality:** `cmp .ufo/waves/round-40/fetch/hyprlang-config-v0.6.8.bin .ufo/waves/round-39/fetch/S173-r39.bin`
  → exit 0 (`CMP_EQUAL`); both sha256 `fa1b6898f2f1676de73220450f18f09603f0c3f8833e4c0a7c42c12aebe1de3e`. Bytes are identical.
