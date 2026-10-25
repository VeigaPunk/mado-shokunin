# ConfigManager.cpp @ efb5099 — source receipt and located quotes

Seat: `ExecFetchConfigMgr` (round 40, w1). Task: source receipt for held row **S162 re-opened**.
All quotes below were located in the delivered receipt bytes and each was re-verified with
`grep -n -F` against that same file (the command and its hit are recorded per quote).

## Receipt

| field | value |
|---|---|
| URL | `https://raw.githubusercontent.com/hyprwm/Hyprland/efb50993780079460b0cbed1363e2166a2de1d9f/src/config/legacy/ConfigManager.cpp` |
| local path | `.ufo/waves/round-40/fetch/config-manager-efb5099.bin` |
| HTTP status | `200` (HTTP/2; `content-type: text/plain; charset=utf-8`; `content-length: 90963`) |
| fetch time (UTC) | `2026-10-25T20:48:45Z` (GET), `2026-10-25T20:49:45Z` (HEAD) |
| sha256 | `9db68cf44048d86557d8a53068dcc40b9bd7347c7d95f38edc501565f65be62b` |
| size | `90963` B |
| ETag (HEAD) | `"24e6f31260686d6b9a9aed89c5d55c487749b568c60daa3c9c476fb749c097ec"` |
| commit | `efb50993780079460b0cbed1363e2166a2de1d9f` (Hyprland v0.56.2 tree) |
| independent re-fetch | second GET to `mktemp -d` gave the same sha256 and `cmp` reported identical bytes |

Exact-byte evidence: two independent GETs, `cmp` clean, `content-length` equal to the on-disk size,
sha256 stable across both fetches. (Committed bytes cannot prove what the server served; this is the
same declared residual as C2.)

## Located quotes (gradient handler, `configHandleGradientSet`, lines 103-160; destroy at 162-165)

Handler definition: `103: static Hyprlang::CParseResult configHandleGradientSet(const char* VALUE, void** data) {`
Bound as the `gradient` custom type at `510` and `2178`:
`Hyprlang::CConfigCustomValueType{&configHandleGradientSet, configHandleGradientDestroy,`.

### Q1 — the handler clears colours before parsing (line 112, with line 111 context)

```
    CVarList2  varlist(std::string(V), 0, ' ');
    DATA->m_colors.clear();
```
lines `111-112`; 6 words; `grep -z -F` multi-line match `1` (`MULTILINE_Q1_OK`).
The single line `DATA->m_colors.clear();` matches at `112` (`grep -n -F` → `112:`).

### Q2 — the angle is set only when a `deg` token is present (line 117 guard, line 120 assignment)

```
if (var.find("deg") != std::string::npos) {
```
line `117`; 5 words; `grep -n -F` → `117:        if (var.find("deg") != std::string::npos) {`

```
DATA->m_angle = std::stoi(std::string(var.substr(0, var.find("deg")))) * (std::numbers::pi / 180.0); // radians
```
line `120`; `grep -n -F` → `120:                DATA->m_angle = ...`. The `deg` branch ends with `break;`
(line `126`; the other `break;` in the handler is `132`), so tokens after the angle are not parsed as
colours.

### Q3 — the max-colours-10 guard (lines 129-131)

```
if (DATA->m_colors.size() >= 10) {
```
line `129`; 5 words; `grep -n -F` → `129:        if (DATA->m_colors.size() >= 10) {`

```
Log::logger->log(Log::WARN, "Error parsing gradient {}: max colors is 10.", V);
```
line `130`; 10 words; `grep -n -F` → `130:            Log::logger->log(Log::WARN, "Error parsing gradient {}: max colors is 10.", V);`
line `131` sets `parseError = "Error parsing gradient " + V + ": max colors is 10.";` and breaks.

### Q4 — supporting: the value object is reused, so an unmentioned angle survives

```
if (!*data)
    *data = new Config::CGradientValueData();
```
lines `106-107`; the `if (!*data)` guard matches at `106` (also `171`, `194` — other handlers) and
`*data = new Config::CGradientValueData();` at `107`. `m_angle` is assigned in this file **only** at
line `120` (`grep -n -F 'm_angle'` returns that single hit), so a redeclaration without a `deg`
token leaves the previously parsed angle in place — the mechanism behind the host reading
`ffe68e0d 45deg` for a theme that declares only `rgb(e68e0d)`.
Fallback when nothing parsed: `146: if (DATA->m_colors.empty()) {` … `151: DATA->m_colors.emplace_back(0); // transparent`.

## Held row S162 check

`grep -n '^| S162 ' corpus/SOURCES.md` → line `174`:

- URL: names `https://raw.githubusercontent.com/hyprwm/Hyprland/efb50993780079460b0cbed1363e2166a2de1d9f/src/config/legacy/ConfigManager.cpp` — **same URL and same commit**.
- Recorded `sha256:9db68cf44048d86557d8a53068dcc40b9bd7347c7d95f38edc501565f65be62b, 90963 B` — **equal** to this receipt.
- Cited locations: `src/config/legacy/ConfigManager.cpp:419-451,590-623,893-968,2016-2093` — these do
  **not** include the gradient handler at `103-160` (plus destroy `162-165`). Re-opening must extend the
  location set with `103-160` (and may keep the existing ranges). The row's status field reads `mined`; the row is
  held, so this seat changes no registry bytes — the C2 seat re-opens it.

## Round-39 receipt comparison

| | sha256 | bytes |
|---|---|---|
| round-39 `fetch/S162-r39.bin` | `9db68cf44048d86557d8a53068dcc40b9bd7347c7d95f38edc501565f65be62b` | 90963 |
| round-40 `fetch/config-manager-efb5099.bin` | `9db68cf44048d86557d8a53068dcc40b9bd7347c7d95f38edc501565f65be62b` | 90963 |

`cmp fetch/config-manager-efb5099.bin ../round-39/fetch/S162-r39.bin` → exit 0 (`CMP_IDENTICAL`).
The bytes are **equal**: the pinned commit's blob did not change between rounds, so round-39's
receipt and this one are the same object.

## What this supports

- S162 (ConfigManager.cpp gradient handler) re-opened: the three required behaviours (colour clear,
  angle only on a `deg` token, 10-colour guard) are present verbatim at lines `112`, `117`/`120`,
  `129`/`130` in the pinned bytes.
- The angle-inheritance rule stated in the round-40 registration and the host census model: the
  reused `CGradientValueData` plus the single `m_angle` assignment at `120` means an angle survives
  a redeclaration that has no `deg` token.

## Limits

- Line numbers are those of the receipt bytes; the file is 2184 lines.
- This receipt establishes the gradient handler only; it does not establish hyprlang block grammar,
  colour parsing inside `ParserUtils::parseColor`, or `CGradientValueData::toString` formatting
  (those are S173 and the `ComplexDataTypes.hpp` row).
