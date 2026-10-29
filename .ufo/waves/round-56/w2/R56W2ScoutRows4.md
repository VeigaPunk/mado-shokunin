# R56W2ScoutRows4 — independent re-open of registry rows S388 and S389 (wave w2, falsify)

Scored tree: 28fc86ac2359ec27406d8a2c63bef82ea6e947ed (lane /home/vgpnk/Projects/shokunin/mado-shokunin). All registry/entry/table content read via
`git show 28fc86ac:<path>`; the working tree was not used. Date of the re-check: 2026-10-28.

## Attack

Wave 1's row author wrote S388/S389 and the gate quotes from the pin files; nothing independent
had fetched the upstream bytes. I fetched both URLs myself, hashed them, re-located every quote in
the upstream bytes, and re-checked the rows' cells against what the lines show.

## Verdict

| row | upstream fetch | sha256 vs anchor cell | sha256 vs frozen-tables-v2.json | gate quotes located | K-row lines inside anchor | locator EOF bound | cells vs lines | verdict |
|---|---|---|---|---|---|---|---|---|
| S388 | HTTP 200, 29785 B, 844 lines | MATCH | MATCH | MATCH (65, 68) | PASS | PASS (68 ≤ 845) | PASS | **MATCH** |
| S389 | HTTP 200, 97582 B, 2346 lines | MATCH | MATCH | MATCH (1223, 1276) | PASS | PASS (1276 ≤ 2347) | PASS | **MATCH** |

No blocking defect found. Two cosmetic findings and one harness note below.

## What I did, commands, decisive output

### 1. Independent fetch + sha256 (attack core)

```
curl -sSL --max-time 90 -o up-MiscFunctions.cpp -w 'HTTP %{http_code} %{size_download}B\n' \
  'https://raw.githubusercontent.com/hyprwm/Hyprland/efb50993780079460b0cbed1363e2166a2de1d9f/src/helpers/MiscFunctions.cpp'
# HTTP 200 29785B ; sha256 065418241a3b40e21273bca1fd29036221942554cddb61e08422d86f0a13c1d9 ; 844 lines
curl -sSL --max-time 90 -o up-HyprCtl.cpp -w 'HTTP %{http_code} %{size_download}B\n' \
  'https://raw.githubusercontent.com/hyprwm/Hyprland/efb50993780079460b0cbed1363e2166a2de1d9f/src/debug/HyprCtl.cpp'
# HTTP 200 97582B ; sha256 798b7c6c4c1684557842463d46ac99c96629be4179e0e461dca77670247b91fa ; 2346 lines
```

- S388 anchor cell pin: `sha256:065418241a3b40e21273bca1fd29036221942554cddb61e08422d86f0a13c1d9`, `29785 B` — byte count and hash equal the fetched bytes.
- S389 anchor cell pin: `sha256:798b7c6c4c1684557842463d46ac99c96629be4179e0e461dca77670247b91fa`, `97582 B` — equal.
- frozen-tables-v2.json `c1.pin_sha256["Hyprland-MiscFunctions.cpp"]` / `["Hyprland-HyprCtl.cpp"]` — equal (file itself verified: sha256 9511151ac2f72097310780357b4a3018e799691cca11905bf75a7e5f6bd795e2, the committed value).
- Lane pin blobs at the scored commit (`git show 28fc86ac:.ufo/waves/round-56/fetch/…` | sha256sum) — equal to both. The wave-1 pins are today's upstream bytes; the attack premise (nothing independent fetched them) is answered: independent fetch reproduces them exactly.

### 2. Gate quotes located in the upstream bytes

gate.md (w1/R56ScribeSourcesA) claims, and the fetched bytes contain at exactly those lines:

- S388: line 65 `static const char* const ENVHOME = getenv("HOME");` and line 68 `auto currentDir = currentPath.substr(0, currentPath.find_last_of('/'));` — both exact substrings at those lines (grep -n).
- S389: line 1223 `if (COMMAND.contains("misc:disable_autoreload"))` (the `Config::watcher()->update();` call is on 1224) and line 1276 `Config::mgr()->reload();` — exact.

### 3. Every K/E row of the entry citing S388/S389 vs the rows' anchor ranges

Entry `corpus/knowledge/hyprland-config-autoreload-r56.md` cites S388 in K25 (Hyprland-MiscFunctions.cpp:65), K26 (:68), E01 (:66); S389 in K27 (Hyprland-HyprCtl.cpp:1223), K28 (:1276), E04 (:1190). No other entry rows cite these sids (grep).

- K rows (the anchor contract): K25@65 ∈ {65,68} ✓, K26@68 ✓, K27@1223 ✓, K28@1276 ✓. All four frozen quotes are exact substrings of the upstream lines at those numbers.
- E rows: **E01 cites line 66, outside S388's locators {65,68}; E04 cites line 1190, outside S389's locators {1223,1276}.** Both quoted lines do exist verbatim in the upstream bytes at the claimed numbers; only anchor coverage is missing.

Severity: **cosmetic** — this is the entry-wide convention, not a row-authoring error of S388/S389: the same entry's S387 E rows are likewise anchor-uncovered (E05@630, E06@1838, E07@2134 vs anchor `776,1070,1079-1080,1816,1835-1836,1844`), the frozen contract scopes the anchor rule to K rows (registration.md leg table `scope:<id>` is marked `(K)`; the counter applies scope only `if kind == "K"` and counts `d` over `c1["k"]`; claims-frozen-v2 M56-1 line 38 "scope leg … stands" refers to quoted K lines), and E01/E04 are not frozen anywhere in frozen-tables-v2.json (no entries exist for them). No committed claim asserts E-row anchor coverage, so nothing committed is falsified; a consumer navigating the entry by anchor cells alone would, however, miss the E-row lines.

Adjacent observation, same bucket: S388's teaches half "…as its directory" is grounded by lines 74-79 (currentDir used as base), which are also outside the anchor; K26 itself is fully grounded by pinned line 68 alone.

### 4. Anchor locators vs the files' last lines

registration-v2 E3 rule: every locator bounded by the pin's `len(blob.split(b"\n"))`.
MiscFunctions.cpp: 845 split-lines, max locator 68 — inside. HyprCtl.cpp: 2347 split-lines, max locator 1276 — inside. No locator runs past EOF. PASS.

### 5. tier / kind / scope / teaches / recheck cells vs the lines

Table header: `| id | source | kind | tier | scope | anchor | teaches | status | opened | recheck | used-by |`.

- S388: kind `code`, tier `A` — URL is a C++ source file; fine. scope "how absolutePath expands a leading ~ and resolves a relative path against the directory of the current file" and teaches "a leading ~ is replaced by the HOME environment value, and a relative path takes the text before the last slash of the current path as its directory" — exactly what lines 61-80 show (61 signature; 64 `value[0] == '~'`; 65 getenv("HOME"); 66 replace of the leading char; 67 relative branch; 68 currentDir = text before the last slash; 74-79 currentDir used as base). No overstatement found.
- S389: kind `code`, tier `A` — fine. scope "how the hyprctl request path reacts to a command naming misc:disable_autoreload, and where a non-full-reset request reaches the manager reload" and teaches "a command whose text contains misc:disable_autoreload calls Config::watcher()->update(), and the path that is not full-reset ends by calling Config::mgr()->reload()" — exactly what lines 1185-1278 show (keywordRequest: 1223 contains-test → 1224 watcher update; reloadRequest: 1262 `ends_with("full-reset")` branch returns "ok" at 1273; the fall-through reaches 1276 `Config::mgr()->reload();`). No overstatement found.
- status `mined`, opened `2026-10-28` (valid ISO date), recheck `on-release` (valid symbolic value), used-by names the entry path — all conform. URL ends with the frozen `pin_suffix` (`src/helpers/MiscFunctions.cpp`, `src/debug/HyprCtl.cpp`) and carries the `rev_rule` token `efb50993780079460b0cbed1363e2166a2de1d9f`. PASS.

### 6. sources-census.sh validate on a scratch copy

```
TMPDIR=<scratch> /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate \
  --file <scratch>/SOURCES-at.md
```

W/E lines mentioning the attacked rows (full output in receipts: census-validate.out):

- `W04 S388 duplicate url raw.githubusercontent.com/.../src/helpers/MiscFunctions.cpp across scopes` — partners S182, S321.
- `W04 S389 duplicate url raw.githubusercontent.com/.../src/debug/HyprCtl.cpp across scopes` — partners S158, S307, S320, S366.

Severity: **cosmetic, lane-wide, pre-existing** — W04 fires for ~25 rows across the registry (S030, S042, S097, …, S380, S381, S382, S384, S387 among them); the script's own comment says "warnings do not affect clean lanes". Not specific to the new rows.

- `E11 S388/S389 missing used-by corpus/knowledge/hyprland-config-autoreload-r56.md` — **harness artifact, not a lane defect**: in `--file` mode the census checks used-by paths on disk relative to the copy's directory (`[ -e "$dir/$path" ]`), so every mined row E11s (S001 through S391; 400+ E11 lines). The used-by blob exists at the scored commit: `git cat-file -e 28fc86ac:corpus/knowledge/hyprland-config-autoreload-r56.md` → EXISTS. Exit code was nonzero (1) in this mode because of those artifact E11s; a rerun produced byte-identical output (cmp exit 0). Reported because the seat asks for all W/E lines mentioning these rows; the lane itself is clean on this check.

## Not verified / notes

- The census exit code could not be echoed past the validator run (both attempts the wrapping shell terminated immediately after the script; output files were complete and byte-identical). Non-material: the decisive W/E lines are in the captured output.
- S390 (man7) is another seat's row; not attacked here.
- No tools installed (curl/git/python3 already present); no pacman transactions; no state-changing host commands; no writes outside my deliverable directory and scratch.
- Deliverables: this report; `R56W2ScoutRows4/receipts-fetch-quotes.md`; `R56W2ScoutRows4/census-validate.out`. Scratch removed before yield.

Report: .ufo/waves/round-56/w2/R56W2ScoutRows4.md
