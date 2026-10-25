# ExecFetchComplexTypes — seat report (mado round 40, w1)

**Status: COMPLETE.** Source receipt for the new C2 row (Hyprland `ComplexDataTypes.hpp` at the
host commit) fetched, hashed, and quoted; all five required facts carry a verbatim `grep -F`-verified
quote with line numbers. Two integration hazards found and measured (see §5) — neither blocks the row.

## 1. Files written (only these)

| path | what |
|---|---|
| `.ufo/waves/round-40/fetch/complex-data-types-efb5099.bin` | exact response bytes, 6116 B, sha256 `95733223b115510dda23e753aae64e373205cc7081b0eeb204df866ea7e68807` |
| `.ufo/waves/round-40/fetch/complex-data-types-efb5099.http.txt` | sidecar: UTC date, HTTP status, size, effective URL, curl exit, HEAD headers (etag, content-length) |
| `.ufo/waves/round-40/w1/ExecFetchComplexTypes/quotes.md` | the receipt document: sha256, 5 located quotes, full `grep -F` log, gate-safety analysis, ready-to-paste GATE lines |
| `.ufo/waves/round-40/w1/ExecFetchComplexTypes.md` | this report |

No tracked file edited; no config tree, compositor state, registry, entry, counter, control or fleet
path touched. Lane `git status --porcelain` shows only untracked round-40 wave paths.

## 2. Fetch provenance (exact)

```
$ curl -sSL -o complex-data-types-efb5099.bin -w 'HTTP_STATUS=%{http_code}\nSIZE=%{size_download}\nEFFECTIVE_URL=%{url_effective}\n' "$URL"
DATE_UTC=2026-10-25T20:48:45Z
HTTP_STATUS=200
SIZE=6116
EFFECTIVE_URL=https://raw.githubusercontent.com/hyprwm/Hyprland/efb50993780079460b0cbed1363e2166a2de1d9f/src/config/shared/complex/ComplexDataTypes.hpp
CURL_EXIT=0
```

HEAD at `2026-10-25T20:52:15Z`: `HTTP/2 200`, `content-length: 6116`,
`etag: "b6a5a0bad5b4a0935662e9406639c539f59289984ef50851fe6e0112538027b6"`.

Host pin corroboration (read-only `hyprctl version`, `2026-10-25T20:51:38Z`):
`Hyprland 0.56.2 built from branch v0.56.2 at commit efb50993780079460b0cbed1363e2166a2de1d9f clean`
— the fetched commit is the host's own commit. No other compositor verb was run.

## 3. Quotes (all verified verbatim, each occurs exactly once in the bytes)

| # | fact | lines | words | gate-safe |
|---|---|---|---|---|
| 1 | gradient `toString` appends `{}deg` | 75 | 8 | **no** (§5a) |
| 1b | gradient colours print as `{:x}` lowercase hex (supporting) | 72 | 5 | **no** (§5a) |
| 2 | gradient `reset()` sets `m_angle = 0` | 32–33 (`reset` at 30) | 4 | yes |
| 3 | `CCssGapData` 1–4 value expansion | 83 (siblings 84–86, switch 98/102/106/110, default 114) | 8 | yes |
| 3b | gap `toString` prints four ints top/right/bottom/left | 134 (signature 133) | 9 | yes |
| 4 | font-weight table incl. `ultraheavy` | 160 (table 158–160) | 12 | yes |
| 4b | font weight prints as a bare integer | 155 | 3 | yes |
| 5 | weight parser falls back to 400 outside 100..1000 | 171–173 | 15 | yes |
| quirk | parser assigns only on a table hit or out-of-range | 167–171 | 17 | yes |

Byte-level uniqueness proof (`count=1` for each contiguous block, with offsets and 1-based spans):

```
(1) count=1 offset=2189 lines=75-75 words=8
(2) count=1 offset=842  lines=32-33 words=4
(3) count=1 offset=2447 lines=83-83 words=8
(4) count=1 offset=5506 lines=160-160 words=12
(5) count=1 offset=5970 lines=171-173 words=15
(1b) count=1 offset=2116 lines=72-72 words=5
(3b) count=1 offset=4604 lines=134-134 words=9
(4b) count=1 offset=5258 lines=155-155 words=3
(quirk) count=1 offset=5814 lines=167-171 words=17
```

Full command/output log is §6 of `quotes.md`; the multi-line quotes include their exact indentation.

## 4. Evidence that this receipt binds to the C2 counter

Simulated the counter's own clause d (imported `quality/counters/c2-r40-forms-entry.py`, used its
`GATE_RE`, `FETCH`, `norm`, and `hashlib`) over the six ready-to-paste GATE lines in `quotes.md` §10:

```
words=12 path_in_fetch=True sha_ok=True norm_in=True | {"medium", 500}, {"semibold", 600}, {"bold", 700}, {"ult
words=15 path_in_fetch=True sha_ok=True norm_in=True | int w_i = std::stoi(strWeight); if (w_i < 100 || w_i > 1
words= 8 path_in_fetch=True sha_ok=True norm_in=True | CCssGapData(int64_t global) : m_top(global), m_right(glo
words= 4 path_in_fetch=True sha_ok=True norm_in=True | m_colors.emplace_back(col); m_angle = 0;
words= 9 path_in_fetch=True sha_ok=True norm_in=True | return std::format("{} {} {} {}", m_top, m_right, m_bott
words= 3 path_in_fetch=True sha_ok=True norm_in=True | return std::format("{}", m_value);
SIMULATED_CLAUSE_D: 6/6
```

The sha256 is of the delivered bytes; the counter reads the blob at `rev:path`, so the L1 must commit
this file unmodified (I do not commit).

## 4b. Scribe coordination (`ScrFormsEntryA`)

`ScrFormsEntryA` asked whether the receipt holds the bytes for two entry-cited quotes and named the
path+sha. Confirmed:

- bytes are at `.ufo/waves/round-40/fetch/complex-data-types-efb5099.bin`, sha256
  `95733223b115510dda23e753aae64e373205cc7081b0eeb204df866ea7e68807`, 6116 B (unchanged since fetch).
- their candidate 1 `result += std::format("{:x} ", c.getAsHex());` — verified, line 72, count 1,
  **not gate-safe** (§5a: `norm()` deletes lines 62–75).
- their candidate 2 `return std::format("{} {} {} {}", m_top, m_right, m_bottom, m_left);` — verified,
  line 134 (signature 133), count 1, 9 words, **gate-safe**; added to the receipt as fact 3b with a
  ready GATE line (the counter simulation scores 6/6).
- their parseWeight quirk is directionally right but the phrasing "leaves m_value at 400" is wrong:
  the parser assigns only on a table hit (169) or out-of-range (173), so an in-range numeric string
  absent from the table is parsed and discarded and `m_value` keeps its *previous* value — 400 only
  while untouched since the default. Located quote lines 167–171, 17 words, gate-safe; the *effect* on
  a live read remains UNK (unexercised on this host), as the entry states.

## 5. Integration hazards (measured; the L1 decides)

**(a) `norm()` deletes `<...>` spans, so facts 1 and 1b cannot be gate quotes.**
`c2-r40-forms-entry.py` clause d requires `norm(quote) in norm(blob)`, and `norm` applies
`re.sub(r"<[^>]+>", "", t)`. The C++ comparison at line 62
(`for (size_t i = 0; i < m_colors.size(); ++i)`) opens a `<` that the regex closes at the `>` of
`sc<int>` on line 75, so `norm(blob)` deletes lines 62–75 — the whole
`CGradientValueData::toString()` body. Measured: `'getAsHex' in norm(blob)` → `False`, `'deg' in
norm(blob)` → `False`, and `gate_safe=False` for both the `{}deg` and `{:x}` quotes, while facts 2–5
are `gate_safe=True`. Consequence: state the `{}deg`/`{:x}` fact in the entry's prose and bind the row
with a gate-safe quote (fact 4, 12 words, or fact 5, 15 words, are the strongest). Fact 5 remains
valid because both sides lose `< 100 || w_i >` identically.

**(b) S180 already registers this exact URL — clause e will collide on a bare-URL location cell.**
`corpus/SOURCES.md:192` (S180, `mined`, `2026-10-23`) records the same URL and
`sha256:95733223b115510dda23e753aae64e373205cc7081b0eeb204df866ea7e68807, 6116 B` — independent
byte-identity corroboration of what I fetched, and a hazard for clause e
(`loc = cells[1].split()[-1]`, `same == [i]`). S180's `cells[1]` ends with the bare URL; that last
token has exactly 1 user. Measured over all 214 registry rows (all well-formed, 11 cells): these
endings have 0 users — `:75`, `(gradient-toString)`,
`src/config/shared/complex/ComplexDataTypes.hpp:75`,
`efb50993780079460b0cbed1363e2166a2de1d9f:75`. Suggested `cells[5]`:
`src/config/shared/complex/ComplexDataTypes.hpp:69-76,155-176 @ efb50993780079460b0cbed1363e2166a2de1d9f, sha256:9573…, 6116 B`;
`cells[7]` `mined`, `cells[8]` `2026-10-25`, `cells[10]` containing the entry path.

This receipt is **not** the own-work census receipt (clause h's `forms int=…` / `labels agreement=…`
lines and the tool sha belong to another seat's file).

## 6. Behaviour facts the entry may rely on (all read from the bytes above)

- Gradient: colours as unpadded lowercase hex, each followed by a space, then
  `std::format("{}deg", sc<int>(m_angle * 180.0 / M_PI))` — the live `ffe68e0d 45deg` shape; angle
  stored in radians (line 54-55) and truncated to int degrees at print time.
- Gap: 1 → all four sides, 2 → vertical/horizontal, 3 → top/horizontal/bottom, 4 → top/right/bottom/left;
  >4 warns (`Too many arguments provided for gaps.`, line 115) and uses the first four tokens;
  `toString` prints `{} {} {} {}` top/right/bottom/left.
- Font weight: table 158–160 (`thin` 100 … `ultraheavy` 1000, including `semilight` 350 and
  `book` 380); member default 400 (line 148); a table hit assigns, otherwise `std::stoi` and only
  `w_i < 100 || w_i > 1000` forces 400. So an in-range integer absent from the table is parsed and
  discarded — `m_value` keeps whatever it held *before* the call (400 only while untouched since the
  default), it is **not** reset to 400. Prints back as a bare integer (line 155).

## 7. Tooling

None installed or updated (no package transaction, no network tool added); only `curl`, `grep -F`,
`sha256sum`, `wc`, `od` and stdlib `python3` were used. Scratch: none created (no `/tmp` use).

## 8. Risks / open items

- Byte identity is only as good as the one fetch; the recorded etag lets the L1 re-HEAD and compare
  (cache `max-age=300`, so a later HEAD may carry a different etag without the content differing —
  the sha256 of the saved bytes is the binding value).
- Facts 1/1b are quotable in the entry but not admissible as gate quotes (hazard (a)); if the L1
  insists on the `{}deg` gate quote, clause d will fail — that is a property of the counter, not of
  the receipt.
- Blockers: none.
