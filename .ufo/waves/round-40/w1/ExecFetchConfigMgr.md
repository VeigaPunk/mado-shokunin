# Seat ExecFetchConfigMgr — round 40 w1 (leaf; no dispatch, no background jobs)

Assignment: source receipt for held row **S162 re-opened** — Hyprland `ConfigManager.cpp` gradient
handler at pinned commit `efb50993780079460b0cbed1363e2166a2de1d9f`.

## Files written (all inside the lane)

| path | what |
|---|---|
| `.ufo/waves/round-40/fetch/config-manager-efb5099.bin` | exact upstream bytes, 90963 B, sha256 `9db68cf44048d86557d8a53068dcc40b9bd7347c7d95f38edc501565f65be62b` |
| `.ufo/waves/round-40/fetch/config-manager-efb5099.http.txt` | HTTP/2 200 headers + sha256 + fetch timestamp (parity with the sibling `complex-data-types-efb5099.http.txt` receipt) |
| `.ufo/waves/round-40/w1/ExecFetchConfigMgr/quotes.md` | receipt metadata + the located quotes with line numbers and per-quote `grep -F` verification |
| `.ufo/waves/round-40/w1/ExecFetchConfigMgr.md` | this report |

No tracked file edited; no registry row touched (S162 re-open is the C2 seat's write).

## Fetch

- URL: `https://raw.githubusercontent.com/hyprwm/Hyprland/efb50993780079460b0cbed1363e2166a2de1d9f/src/config/legacy/ConfigManager.cpp`
- GET `HTTP=200 SIZE=90963` at `2026-10-25T20:48:45Z`; HEAD `HTTP/2 200`, `content-length: 90963`,
  `etag: "24e6f31260686d6b9a9aed89c5d55c487749b568c60daa3c9c476fb749c097ec"`.
- sha256 `9db68cf44048d86557d8a53068dcc40b9bd7347c7d95f38edc501565f65be62b`, 90963 B, 2184 lines.
- Exact bytes: an independent second GET into `mktemp -d` produced the same sha256 and `cmp` exit 0
  (`REFETCH_IDENTICAL`); scratch dir removed.

## Quotes located (each re-verified with `grep -n -F` on the delivered `.bin`)

Handler `configHandleGradientSet` = lines `103-160` (destroy `162-165`), registered as the
`gradient` custom type at `510` and `2178`.

1. **Colour clear** — `DATA->m_colors.clear();` at line `112` (`grep -n -F` → `112:`); context span
   `111-112` (`CVarList2  varlist(std::string(V), 0, ' ');` + the clear) verified multi-line, 6 words.
2. **Angle only when a `deg` token is present** — guard `if (var.find("deg") != std::string::npos) {`
   at line `117` (5 words), assignment at line `120`
   `DATA->m_angle = std::stoi(std::string(var.substr(0, var.find("deg")))) * (std::numbers::pi / 180.0); // radians`,
   branch `break;` at `126`.
3. **Max-colours-10 guard** — `if (DATA->m_colors.size() >= 10) {` at line `129` (5 words), log
   `Log::logger->log(Log::WARN, "Error parsing gradient {}: max colors is 10.", V);` at line `130`
   (10 words), `parseError = "Error parsing gradient " + V + ": max colors is 10.";` at `131`.
4. **Supporting (angle inheritance mechanism)** — `if (!*data)` / `*data = new Config::CGradientValueData();`
   at `106-107` (the value object is reused across redeclarations), and `m_angle` is assigned in this
   file **only** at line `120` (`grep -n -F 'm_angle'` → single hit). So a redeclaration without a
   `deg` token keeps the earlier angle — the mechanism behind the host reading `ffe68e0d 45deg`.

## S162 row status

`grep -n '^| S162 ' corpus/SOURCES.md` → line `174`.

- Names the **same URL and same commit** `efb5099378…` — yes.
- Recorded `sha256:9db68cf4…, 90963 B` — **equal** to this receipt.
- **Gap for the re-open:** the row's cited locations are `419-451,590-623,893-968,2016-2093` and do
  **not** cover the gradient handler. Re-opening must add `103-160` (+ destroy `162-165`). Row status
  field reads `mined`, date `2026-10-23`.

## Round-39 comparison

`cmp fetch/config-manager-efb5099.bin ../round-39/fetch/S162-r39.bin` → exit 0 (`CMP_IDENTICAL`);
both sha256 `9db68cf4…`, both 90963 B. **Bytes equal** — the pinned blob is unchanged between rounds,
so round 40 re-opens the same object round 39 receipted.

## Retained evidence (exact commands and results)

- `curl -sS -o fetch/config-manager-efb5099.bin -w 'HTTP=%{http_code} SIZE=%{size_download}' <URL>` → `HTTP=200 SIZE=90963`
- `sha256sum fetch/config-manager-efb5099.bin` → `9db68cf4…be62b`
- `cmp` vs round-39 receipt → identical; re-fetch into `mktemp -d` → same sha, `cmp` identical
- `grep -n -F` for each quote → `112:`, `117:`, `120:`, `129:`, `130:` (single hits, no misses)
- `grep -z -F` for the two-line `111-112` span → `MULTILINE_Q1_OK`
- `grep -n '^| S162 ' corpus/SOURCES.md` → line `174`
- word counts: `wc -w` → 6 / 5 / 10 for the three headline quotes (all inside 3-25)

## Risks / blockers

- None blocking. Declared residual (same class as C2's): committed bytes cannot prove what the
  server served; mitigated by two independent GETs, stable sha256, `content-length` equality, ETag.
- Line numbers are byte-file line numbers at this commit; upstream may renumber in other commits —
  quotes are pinned by commit, not by line.
- Scope note: this receipt covers the gradient handler only. It does **not** establish hyprlang
  block grammar, `ParserUtils::parseColor` internals, or `CGradientValueData::toString` formatting
  (those belong to S173 and the `ComplexDataTypes.hpp` row).

## Tooling

No installs (curl + coreutils present). No package transaction, no compositor verb, no socket of my
own beyond the two read-only HTTPS GET/HEAD to raw.githubusercontent.com.

Report: `.ufo/waves/round-40/w1/ExecFetchConfigMgr.md`
