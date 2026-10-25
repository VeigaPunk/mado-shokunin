# ExecFetchHyprlang — round 40, w1

Target: source receipt for held row S173 re-opened — hyprlang v0.6.8 `src/config.cpp`, `configStringToInt`.
Status: COMPLETE. No blockers. No tool installs (none needed; `curl`, `grep`, `sha256sum`, `cmp` only).
No writes outside `.ufo/waves/round-40/fetch/` and `.ufo/waves/round-40/w1/ExecFetchHyprlang/`.

## Fetch receipt

| field | value |
|---|---|
| URL | `https://raw.githubusercontent.com/hyprwm/hyprlang/v0.6.8/src/config.cpp` |
| destination | `.ufo/waves/round-40/fetch/hyprlang-config-v0.6.8.bin` |
| HTTP status | **200** (`curl -w '%{http_code}'`, curl_rc=0) |
| content-type | `text/plain; charset=utf-8` |
| fetched (UTC) | **2026-10-25T20:48:47Z** (`date -u` taken immediately before the request) |
| size | **43049 bytes**, 1158 lines |
| sha256 | **`fa1b6898f2f1676de73220450f18f09603f0c3f8833e4c0a7c42c12aebe1de3e`** |
| md5 | `b88997b264c7b9245a7ffe75d3314702` |
| `file` | `C source, ASCII text` |

Exact command:

```
curl -sS --max-time 60 -o .ufo/waves/round-40/fetch/hyprlang-config-v0.6.8.bin \
  -w 'HTTP_STATUS=%{http_code}\nSIZE=%{size_download}\n' \
  https://raw.githubusercontent.com/hyprwm/hyprlang/v0.6.8/src/config.cpp
```

## Quotes file

`.ufo/waves/round-40/w1/ExecFetchHyprlang/quotes.md` (7978 B) — verbatim, line-numbered, `grep -F`-verified
quotes (3–25 words each; match count 1 = unique) for every branch the row needs:

| branch | line | words | quote (abbrev. here; full text in quotes.md) |
|---|---|---|---|
| function anchor | 185 | 7 | `static std::expected<int64_t, std::string> configStringToInt(const std::string& VALUE) {` |
| `rgba(` | 198 | 7 | `} else if (VALUE.starts_with("rgba(") && VALUE.ends_with(')')) {` |
| `rgba(` comma-4 → ARGB | 219 | 14 | `return (a * (Hyprlang::INT)0x1000000) + (r.value() * …) + b.value();` |
| `rgba(` hex-8 → RGBA→ARGB | 227 | 10 | `return (RGBA.value() >> 8) + (0x1000000 * (RGBA.value() & 0xFF));` |
| `rgb(` | 232 | 7 | `} else if (VALUE.starts_with("rgb(") && VALUE.ends_with(')')) {` |
| `rgb(` comma-3 | 248 | 12 | `return (Hyprlang::INT)0xFF000000 + (r.value() * …) + b.value();` |
| `rgb(` hex-6 | 255 | 4 | `return RGB.value() + 0xFF000000;` |
| true/on/yes → 1 | 259 | 9 | `} else if (VALUE.starts_with("true") \|\| VALUE.starts_with("on") \|\| VALUE.starts_with("yes")) {` |
| false/off/no → 0 | 261 | 9 | `} else if (VALUE.starts_with("false") \|\| VALUE.starts_with("off") \|\| VALUE.starts_with("no")) {` |
| `0x` hex | 195 | 3 | `if (VALUE.starts_with("0x")) {` |
| `0x` comment | 196 | 6 | `// Values with 0x are hex` |

Adjacent line references (below the 3-word quote floor, so recorded as line refs, not quotes): `return 1;` at 260
(branch body of the true/on/yes test), `return 0;` at 262 (false/off/no body; other `return 0;` at 41 and 273),
`return parseHex(VALUE);` at 197. Reject paths: 230 (`rgba()` arity error), 258 (`rgb()` arity error),
266 (`cannot parse … as an int.`), 193 (`invalid hex`). Fallthrough guard `isNumber(VALUE, false)` at 265,
`stoll` at 269.

Verified command per quote (`matches` is `grep -cF`, `words` is `wc -w`):

```
grep -nF -- '<quote>' .ufo/waves/round-40/fetch/hyprlang-config-v0.6.8.bin   # one line, matches=1
```

Test order in the function (what a re-opened row must cite): `0x` (195) → `rgba(` (198) → `rgb(` (232) →
`true|on|yes` (259) → `false|off|no` (261) → number fallthrough (265–272). Both boolean arms use `starts_with`
prefix matching, not equality.

## Held row S173 check

`grep -n '^| S173 ' corpus/SOURCES.md` → **`corpus/SOURCES.md:185`** (row text reproduced in quotes.md).

- **Names this URL: YES** — the row's title field is exactly
  `Hyprlang v0.6.8 expression evaluation — https://raw.githubusercontent.com/hyprwm/hyprlang/v0.6.8/src/config.cpp`.
- **sha256 agrees:** row records `sha256:fa1b6898f2f1676de73220450f18f09603f0c3f8833e4c0a7c42c12aebe1de3e`
  = fetched sha256.
- **size agrees:** row records `43049 B` = `stat -c %s` of the fetched bytes.
- **Location gap for re-opening:** the row's location field is `src/config.cpp:619-667,755-827,983-986 @
  3a1c1b25b059dae2c6bbc46991562ba1158d125c` (expression evaluation). That range does **not** cover
  `configStringToInt` (185–273). The re-opened use must add lines 185–273; the existing range stays valid for
  what it already supports. The row's `@ <commit>` is the release-tag commit; this receipt is pinned by the tag
  URL, not by that commit (the commit hash was not re-derived here — it is a git object, not bytes in the file).
- **Round-39 byte equality: YES.** `cmp .ufo/waves/round-40/fetch/hyprlang-config-v0.6.8.bin
  .ufo/waves/round-39/fetch/S173-r39.bin` → exit 0 (`CMP_EQUAL`); both files sha256
  `fa1b6898…e1de3e`. The round-40 receipt is byte-identical to the round-39 receipt, so the re-opened source
  is stable across the two rounds.

## Supports / attacks

- Supports C2 (`corpus/knowledge/hyprctl-getoption-native-forms-r40.md`) held-row S173 re-open: the
  `configStringToInt` forms (`0x`, `rgba(`, `rgb(`, boolean names, decimal fallthrough) are the conversion the
  entry's "declared string → native form" section needs, quoted from bytes whose sha256 equals the row's
  recorded sha256.
- Supports the C1 conversion model only indirectly (host-style conversion is Hyprland's handler side); no C1
  fixture or counter was run or modified by this seat.
- Nothing attacked: this seat produced no counter run, no tool edit, no registry edit.

## Risks

1. The row's cited line range does not include `configStringToInt`; if the C2 entry cites S173 for lines
   619-667 only, the re-open is cosmetic. The entry should cite `src/config.cpp:185-273` explicitly.
2. The `@ 3a1c1b25…` commit in the row was not verified against the tag (git object, out of scope for a byte
   receipt); pinning is by URL tag `v0.6.8`.
3. The 2-word lines (`return 1;`, `return 0;`, `return parseHex(VALUE);`) cannot satisfy a 3-word quote floor;
   they are recorded as line refs. If the C2 counter demands the `return 1;`/`return 0;` statement itself as a
   quote, use the branch-condition lines 259/261 (each carries the same semantics via the adjacent line).

## Coordination (ScrFormsEntryA, S173 Gate line)

ScrFormsEntryA asked for a verified 3–25 word quote for the S173 Gate line. Re-checked all three of its
candidates against the receipt; best pick **line 226, 13 words, matches=1**:
`// now we need to RGBA -> ARGB. The config holds ARGB only.` (no `<…>` normalisation hazard).
Line 185 (7 words) and line 198 (6 words, `else if (VALUE.starts_with("rgba(") && VALUE.ends_with(')')) {`)
also verified matches=1. Gate sha binds to `.ufo/waves/round-40/fetch/hyprlang-config-v0.6.8.bin`
(`fa1b6898…e1de3e`). Recorded in quotes.md § "Scribe candidate check".

## Files changed (all new, all inside the lane)

- `.ufo/waves/round-40/fetch/hyprlang-config-v0.6.8.bin` (43049 B)
- `.ufo/waves/round-40/w1/ExecFetchHyprlang/quotes.md`
- `.ufo/waves/round-40/w1/ExecFetchHyprlang.md` (this report)

Scratch: only `/tmp/r40-fetch-date.txt` (timestamp helper). No git/jj mutation run; only read-only
`git -C . status/rev-parse` was used (HEAD `e2b51d3`, unrelated to this seat's writes).
