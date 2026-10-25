# Source receipt — Hyprland `ComplexDataTypes.hpp` @ `efb5099` (C2, round 40)

Source receipt for the new C2 registry row. Every quote below was checked with `grep -F` against
the saved bytes; the command and its output are pasted in §6. No quote is paraphrased.

## 1. Provenance

| field | value |
|---|---|
| url | `https://raw.githubusercontent.com/hyprwm/Hyprland/efb50993780079460b0cbed1363e2166a2de1d9f/src/config/shared/complex/ComplexDataTypes.hpp` |
| command | `curl -sSL -o complex-data-types-efb5099.bin -w 'HTTP_STATUS=%{http_code}\nSIZE=%{size_download}\nEFFECTIVE_URL=%{url_effective}\n' "$URL"` |
| fetched (UTC) | `2026-10-25T20:48:45Z` |
| HTTP status | `200` (curl exit `0`) |
| bytes | `6116` |
| sha256 | `95733223b115510dda23e753aae64e373205cc7081b0eeb204df866ea7e68807` |
| etag (HEAD, `2026-10-25T20:52:15Z`, HTTP/2 `200`) | `"b6a5a0bad5b4a0935662e9406639c539f59289984ef50851fe6e0112538027b6"` |
| content-length (HEAD) | `6116` |
| shape | 178 lines, ASCII, C++ header; last line `}` |

Receipt file: `.ufo/waves/round-40/fetch/complex-data-types-efb5099.bin` (exact response bytes, never
edited after the fetch). Sidecar: `.ufo/waves/round-40/fetch/complex-data-types-efb5099.http.txt`
(status, UTC date, size, effective URL, curl exit, HEAD headers).

Host pin corroboration (`hyprctl version`, read-only verb, `2026-10-25T20:51:38Z`):

```
Hyprland 0.56.2 built from branch v0.56.2 at commit efb50993780079460b0cbed1363e2166a2de1d9f clean ([gha] Nix: update inputs).
```

The fetched commit equals the commit the host reports for itself, so the receipt is the host's own
`ComplexDataTypes.hpp`.

## 2. Facts and located quotes

| # | fact | lines | words | gate-safe (§5) | quote |
|---|---|---|---|---|---|
| 1 | gradient `toString` appends the angle as `{}deg` | 75 | 8 | **no** | `result += std::format("{}deg", sc<int>(m_angle * 180.0 / M_PI));` |
| 1b | gradient colours print as lowercase hex (`{:x}`) — supporting | 72 | 5 | **no** | `result += std::format("{:x} ", c.getAsHex());` |
| 2 | gradient `reset()` sets the angle to 0 | 32–33 (in `void reset(CHyprColor col) {` at 30) | 4 | yes | `m_colors.emplace_back(col);` + `m_angle = 0;` |
| 3 | `CCssGapData` expands 1–4 values to four sides | 83 (siblings 84–86; switch 98/102/106/110; `default` 114) | 8 | yes | `CCssGapData(int64_t global) : m_top(global), m_right(global), m_bottom(global), m_left(global) {};` |
| 3b | gap `toString` prints the four ints top/right/bottom/left | 134 (signature 133) | 9 | yes | `return std::format("{} {} {} {}", m_top, m_right, m_bottom, m_left);` |
| 4 | font-weight table including `ultraheavy` | 158–160, quote is 160 | 12 | yes | `{"medium", 500}, {"semibold", 600},   {"bold", 700},  {"ultrabold", 800}, {"heavy", 900}, {"ultraheavy", 1000},` |
| 4b | font weight prints as a bare integer | 155 | 3 | yes | `return std::format("{}", m_value);` |
| 5 | weight parser falls back to 400 outside 100..1000 | 171–173 | 15 | yes | `int w_i = std::stoi(strWeight);` / `if (w_i < 100 || w_i > 1000)` / `m_value = 400;` |

Every quote occurs **exactly once** in the bytes (checked by byte count, §6/§7) and is 3–25 words.

## 3. Fact 1 — gradient `toString` format

Line 75, inside `CGradientValueData::toString()` (line 69):

```
            result += std::format("{}deg", sc<int>(m_angle * 180.0 / M_PI));
```

Quote (8 words): `result += std::format("{}deg", sc<int>(m_angle * 180.0 / M_PI));`

Supporting, line 72 (same function; the colour list is emitted as unpadded lowercase hex followed by
a space, the angle then appended — the shape the live host reads as `ffe68e0d 45deg`):

```
                result += std::format("{:x} ", c.getAsHex());
```

Note the angle is stored in radians (`float m_angle = 0;` line 55, comment line 54
`/* Float corresponding to the angle (rad) */`) and converted with `* 180.0 / M_PI` at print time.

## 4. Fact 2 — `reset()` zeroes the angle

Lines 30–33:

```
        void reset(CHyprColor col) {
            m_colors.clear();
            m_colors.emplace_back(col);
            m_angle = 0;
```

Quote (4 words, two lines): `m_colors.emplace_back(col);` (line 32) then `m_angle = 0;` (line 33).

`m_angle = 0;` also matches line 55 as a substring, but line 55 is the member declaration
`float m_angle = 0;`; the reset body hit is line 33 (§6 shows both hits and the contiguous block).

## 5. Facts 3–5

### (3) `CCssGapData` 1–4 value expansion — line 83

```
        CCssGapData(int64_t global) : m_top(global), m_right(global), m_bottom(global), m_left(global) {};
        CCssGapData(int64_t vertical, int64_t horizontal) : m_top(vertical), m_right(horizontal), m_bottom(vertical), m_left(horizontal) {};
        CCssGapData(int64_t top, int64_t horizontal, int64_t bottom) : m_top(top), m_right(horizontal), m_bottom(bottom), m_left(horizontal) {};
        CCssGapData(int64_t top, int64_t right, int64_t bottom, int64_t left) : m_top(top), m_right(right), m_bottom(bottom), m_left(left) {};
```

Quote (8 words, line 83): the one-value constructor that fills all four sides.

`parseGapData` (line 94) selects by token count: `case 1:` 98, `case 2:` 102, `case 3:` 106,
`case 4:` 110; `default:` 114 warns `Too many arguments provided for gaps.` (115) and still builds
from the first four tokens.

The gap `toString` (signature 133, body 134) prints the four ints top/right/bottom/left:

```
            return std::format("{} {} {} {}", m_top, m_right, m_bottom, m_left);
```

Quote (9 words, line 134): `return std::format("{} {} {} {}", m_top, m_right, m_bottom, m_left);`

### (4) font-weight table — line 160

```
        inline static const auto WEIGHTS = std::map<std::string, int>{          (158)
            {"thin", 100},   {"ultralight", 200}, {"light", 300}, {"semilight", 350}, {"book", 380},  {"normal", 400},   (159)
            {"medium", 500}, {"semibold", 600},   {"bold", 700},  {"ultrabold", 800}, {"heavy", 900}, {"ultraheavy", 1000},   (160)
```

Quote (12 words, line 160, raw spacing as in the bytes — the counter collapses whitespace):
`{"medium", 500}, {"semibold", 600},   {"bold", 700},  {"ultrabold", 800}, {"heavy", 900}, {"ultraheavy", 1000},`

The weight prints back as a bare integer (signature 154, body 155): quote (3 words, line 155)
`return std::format("{}", m_value);`.

### (5) parser fallback to 400 — lines 171–173

```
                int w_i = std::stoi(strWeight);
                if (w_i < 100 || w_i > 1000)
                    m_value = 400;
```

Quote (15 words, whitespace-collapsed single-line form): `int w_i = std::stoi(strWeight); if (w_i < 100 || w_i > 1000) m_value = 400;`

The member default is `int64_t                       m_value = 400; // default to normal weight`
(line 148); line 173 is the out-of-range fallback.

**Quirk (exact semantics; a "stays 400" phrasing is wrong).** The parser assigns in exactly two
places — a table hit (line 169) and the out-of-range branch (line 173). A numeric weight inside
100..1000 that is *not* in the table is parsed into `w_i` and then discarded, so `m_value` keeps
whatever it held **before** the call: 400 only when the value was still at its default (or was
constructed with `int64_t def` = 400), not unconditionally. Located quote (17 words, lines 167–171):

```
            auto weight = WEIGHTS.find(lcWeight);
            if (weight != WEIGHTS.end())
                m_value = weight->second;
            else {
                int w_i = std::stoi(strWeight);
```

Collapsed for a gate: `auto weight = WEIGHTS.find(lcWeight); if (weight != WEIGHTS.end()) m_value = weight->second; else { int w_i = std::stoi(strWeight);`
(gate-safe: yes — verified `norm(quote) in norm(blob)`). Unexercised on this host, so the *effect* on
a live read stays UNK in the entry; only the control flow above is sourced.

## 6. Verification log (`grep -F` on the saved bytes)

```
$ sha256sum complex-data-types-efb5099.bin
95733223b115510dda23e753aae64e373205cc7081b0eeb204df866ea7e68807  complex-data-types-efb5099.bin

$ grep -n -F 'result += std::format("{}deg", sc<int>(m_angle * 180.0 / M_PI));' complex-data-types-efb5099.bin
75:            result += std::format("{}deg", sc<int>(m_angle * 180.0 / M_PI));

$ grep -n -F 'result += std::format("{:x} ", c.getAsHex());' complex-data-types-efb5099.bin
72:                result += std::format("{:x} ", c.getAsHex());

$ grep -n -F 'void reset(CHyprColor col) {' complex-data-types-efb5099.bin
30:        void reset(CHyprColor col) {

$ grep -n -A3 -F 'void reset(CHyprColor col) {' complex-data-types-efb5099.bin
30:        void reset(CHyprColor col) {
31-            m_colors.clear();
32-            m_colors.emplace_back(col);
33-            m_angle = 0;

$ grep -n -F 'm_angle = 0;' complex-data-types-efb5099.bin
33:            m_angle = 0;
55:        float m_angle = 0;

$ grep -n -F 'CCssGapData(int64_t global) : m_top(global), m_right(global), m_bottom(global), m_left(global) {};' complex-data-types-efb5099.bin
83:        CCssGapData(int64_t global) : m_top(global), m_right(global), m_bottom(global), m_left(global) {};

$ grep -n -F 'CCssGapData(int64_t vertical, int64_t horizontal)' complex-data-types-efb5099.bin
84:        CCssGapData(int64_t vertical, int64_t horizontal) : m_top(vertical), m_right(horizontal), m_bottom(vertical), m_left(horizontal) {};
$ grep -n -F 'CCssGapData(int64_t top, int64_t horizontal, int64_t bottom)' complex-data-types-efb5099.bin
85:        CCssGapData(int64_t top, int64_t horizontal, int64_t bottom) : m_top(top), m_right(horizontal), m_bottom(bottom), m_left(horizontal) {};
$ grep -n -F 'CCssGapData(int64_t top, int64_t right, int64_t bottom, int64_t left)' complex-data-types-efb5099.bin
86:        CCssGapData(int64_t top, int64_t right, int64_t bottom, int64_t left) : m_top(top), m_right(right), m_bottom(bottom), m_left(left) {};

$ grep -n -F -e 'case 1: {' -e 'case 2: {' -e 'case 3: {' -e 'case 4: {' complex-data-types-efb5099.bin
98:                case 1: {
102:                case 2: {
106:                case 3: {
110:                case 4: {

$ grep -n -F 'Too many arguments provided for gaps.' complex-data-types-efb5099.bin
115:                    Log::logger->log(Log::WARN, "Too many arguments provided for gaps.");

$ grep -n -F '{"medium", 500}, {"semibold", 600},   {"bold", 700},  {"ultrabold", 800}, {"heavy", 900}, {"ultraheavy", 1000},' complex-data-types-efb5099.bin
160:            {"medium", 500}, {"semibold", 600},   {"bold", 700},  {"ultrabold", 800}, {"heavy", 900}, {"ultraheavy", 1000},

$ grep -n -F '{"heavy", 900}, {"ultraheavy", 1000},' complex-data-types-efb5099.bin
160:            {"medium", 500}, {"semibold", 600},   {"bold", 700},  {"ultrabold", 800}, {"heavy", 900}, {"ultraheavy", 1000},

$ grep -n -F 'if (w_i < 100 || w_i > 1000)' complex-data-types-efb5099.bin
172:                if (w_i < 100 || w_i > 1000)

$ grep -n -F 'm_value = 400;' complex-data-types-efb5099.bin
148:        int64_t                       m_value = 400; // default to normal weight
173:                    m_value = 400;

$ grep -n -A2 -F 'int w_i = std::stoi(strWeight);' complex-data-types-efb5099.bin
171:                int w_i = std::stoi(strWeight);
172-                if (w_i < 100 || w_i > 1000)
173-                    m_value = 400;

$ grep -n -F 'return std::format("{} {} {} {}", m_top, m_right, m_bottom, m_left);' complex-data-types-efb5099.bin
134:            return std::format("{} {} {} {}", m_top, m_right, m_bottom, m_left);

$ grep -n -A1 -B2 -F 'return std::format("{} {} {} {}", m_top, m_right, m_bottom, m_left);' complex-data-types-efb5099.bin
132-
133-        virtual std::string toString() const {
134:            return std::format("{} {} {} {}", m_top, m_right, m_bottom, m_left);
135-        }

$ grep -n -F 'return std::format("{}", m_value);' complex-data-types-efb5099.bin
155:            return std::format("{}", m_value);

$ grep -n -A10 -F 'void parseWeight(const std::string& strWeight) {' complex-data-types-efb5099.bin
163:        void parseWeight(const std::string& strWeight) {
164-            auto lcWeight{strWeight};
165-            std::ranges::transform(strWeight, lcWeight.begin(), ::tolower);
166-
167-            auto weight = WEIGHTS.find(lcWeight);
168-            if (weight != WEIGHTS.end())
169-                m_value = weight->second;
170-            else {
171-                int w_i = std::stoi(strWeight);
172-                if (w_i < 100 || w_i > 1000)
173-                    m_value = 400;
```

Word counts (`printf '%s' "<quote>" | wc -w`): fact 1 → 8, fact 1b → 5, fact 2 → 4 (collapsed),
fact 3 → 8, fact 3b → 9, fact 4 → 12, fact 4b → 3, fact 5 → 15 (collapsed), quirk → 17 (collapsed).
All inside the 3–25 word window.

## 7. Byte-exactness and uniqueness

`python3` over the saved bytes (exact multi-line blocks, offsets, 1-based line spans):

```
sha256=95733223b115510dda23e753aae64e373205cc7081b0eeb204df866ea7e68807 bytes=6116
(1) count=1 offset=2189 lines=75-75 words=8
(2) count=1 offset=842 lines=32-33 words=4
(3) count=1 offset=2447 lines=83-83 words=8
(4) count=1 offset=5506 lines=160-160 words=12
(5) count=1 offset=5970 lines=171-173 words=15
(1b) count=1 offset=2116 lines=72-72 words=5
(3b) count=1 offset=4604 lines=134-134 words=9
(4b) count=1 offset=5258 lines=155-155 words=3
(quirk) count=1 offset=5814 lines=167-171 words=17
```

Each quote is a contiguous byte block (`count=1`) — the multi-line quotes (2) and (5) include their
exact indentation, so they cannot match a different region.

## 8. Gate-safety: the counter's `norm()` deletes `<...>` spans — read before choosing a gate quote

`quality/counters/c2-r40-forms-entry.py` clause d admits a quote only if
`norm(quote) in norm(blob)`, where `norm()` strips `re.sub(r"<[^>]+>", "", t)` before collapsing
whitespace (counter lines 86-89). In this header the C++ comparison at line 62
(`for (size_t i = 0; i < m_colors.size(); ++i)`) opens a `<` that the regex closes at the `>` of
`sc<int>` on line 75, so `norm(blob)` **deletes lines 62–75**, including the whole
`CGradientValueData::toString()` body.

Measured:

```
F1 deg      words= 8 gate_safe=False normed='result += std::format("{}deg", sc(m_angle * 180.0 / M_PI));'
F1b hex     words= 5 gate_safe=False normed='result += std::format("{:x} ", c.getAsHex());'
F2 reset    words= 4 gate_safe=True  normed='m_colors.emplace_back(col); m_angle = 0;'
F3 gap      words= 8 gate_safe=True  normed='CCssGapData(int64_t global) : m_top(global), m_right(global), m_bot...'
F4 weights  words=12 gate_safe=True  normed='{"medium", 500}, {"semibold", 600}, {"bold", 700}, {"ultrabold", 80...'
F4b fontstr words= 3 gate_safe=True  normed='return std::format("{}", m_value);'
F3b gapstr  words= 9 gate_safe=True  normed='return std::format("{} {} {} {}", m_top, m_right, m_bottom, m_left);'
F5 parser   words=15 gate_safe=True  normed='int w_i = std::stoi(strWeight); if (w_i 1000) m_value = 400;'
quirk       words=17 gate_safe=True  normed='auto weight = WEIGHTS.find(lcWeight); if (weight != WEIGHTS.end()) ...'

norm(blob) around CGradientValueData::toString:
'l; } virtual eConfigValueDataTypes getDataType() { return CVD_TYPE_CSS_VALUE; } virtual std::string toString() const { return std::format("{} {} {} {}", m_top, m_right, m'
gradient toString body present in norm(blob)? False | deg token? False
```

`getAsHex` and the token `deg` are absent from `norm(blob)` entirely, so **facts 1 and 1b can never be
gate quotes** (clause d would reject them). Facts 2, 3, 3b, 4, 4b, 5 and the quirk block are gate-safe;
fact 5 stays valid because both sides lose `< 100 || w_i >` identically.

Consequence for the entry: state the `{}deg` / `{:x}` fact in prose, and bind the row with one of the
gate-safe quotes. Recommended primary gate quote: fact 4 (12 words) or fact 5 (15 words).

## 9. Registry integration notes (measured, not applied — the L1 owns the registry)

- An earlier row already registers this exact URL: **S180** (`mined`, `2026-10-23`,
  `used-by corpus/knowledge/workspace-rules-r27.md, tools/mado-wsrules.py`), whose location cell
  records `sha256:95733223b115510dda23e753aae64e373205cc7081b0eeb204df866ea7e68807, 6116 B` —
  byte-identical to this receipt. Independent corroboration of the fetched bytes; also a hazard.
- Clause e takes `loc = cells[1].split()[-1]` and requires `same == [i]`. S180's `cells[1]` **ends with
  the bare URL**, so a new row whose `cells[1]` also ends with the bare URL fails clause e
  (measured: that last token has exactly 1 user, S180). Unique endings verified against the 214
  registry rows: `:75`, `(gradient-toString)`, `src/config/shared/complex/ComplexDataTypes.hpp:75`,
  `efb50993780079460b0cbed1363e2166a2de1d9f:75` (all 0 users).
- Suggested row shape (11 cells, matching S180's column order): `cells[1]` ends with a unique token
  (e.g. `... ComplexDataTypes.hpp:75`), `cells[5]` carries
  `src/config/shared/complex/ComplexDataTypes.hpp:69-76,155-176 @ efb50993780079460b0cbed1363e2166a2de1d9f, sha256:9573..., 6116 B`,
  `cells[7]` `mined`, `cells[8]` `2026-10-25`, `cells[10]` must contain the entry path
  `corpus/knowledge/hyprctl-getoption-native-forms-r40.md` (clause c).
- This receipt is **not** the own-work census receipt (clause h needs the `forms int=…` /
  `labels agreement=…` lines and the tool sha256; another seat owns that file).

## 10. Ready-to-paste GATE lines (gate-safe quotes only)

`S<id>` must be the new row's id, and the same id must appear on an entry line that contains the
quote verbatim (whitespace-collapsed) — counter clause g.

```
GATE S<id> receipt=.ufo/waves/round-40/fetch/complex-data-types-efb5099.bin sha256=95733223b115510dda23e753aae64e373205cc7081b0eeb204df866ea7e68807 quote="{"medium", 500}, {"semibold", 600}, {"bold", 700}, {"ultrabold", 800}, {"heavy", 900}, {"ultraheavy", 1000},"
GATE S<id> receipt=.ufo/waves/round-40/fetch/complex-data-types-efb5099.bin sha256=95733223b115510dda23e753aae64e373205cc7081b0eeb204df866ea7e68807 quote="int w_i = std::stoi(strWeight); if (w_i < 100 || w_i > 1000) m_value = 400;"
GATE S<id> receipt=.ufo/waves/round-40/fetch/complex-data-types-efb5099.bin sha256=95733223b115510dda23e753aae64e373205cc7081b0eeb204df866ea7e68807 quote="CCssGapData(int64_t global) : m_top(global), m_right(global), m_bottom(global), m_left(global) {};"
GATE S<id> receipt=.ufo/waves/round-40/fetch/complex-data-types-efb5099.bin sha256=95733223b115510dda23e753aae64e373205cc7081b0eeb204df866ea7e68807 quote="m_colors.emplace_back(col); m_angle = 0;"
GATE S<id> receipt=.ufo/waves/round-40/fetch/complex-data-types-efb5099.bin sha256=95733223b115510dda23e753aae64e373205cc7081b0eeb204df866ea7e68807 quote="return std::format("{} {} {} {}", m_top, m_right, m_bottom, m_left);"
GATE S<id> receipt=.ufo/waves/round-40/fetch/complex-data-types-efb5099.bin sha256=95733223b115510dda23e753aae64e373205cc7081b0eeb204df866ea7e68807 quote="return std::format("{}", m_value);"
```

All six were re-checked against the counter's own `norm()`: `norm(quote) in norm(blob)` is `True`
for each, word counts 12/15/8/4/9/3, and the receipt path starts with `.ufo/waves/round-40/fetch/`.
The seventh gate-safe candidate is the quirk block (17 words) quoted in §5.
