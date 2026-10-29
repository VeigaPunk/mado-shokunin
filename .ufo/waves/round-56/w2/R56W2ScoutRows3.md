# R56W2ScoutRows3 — independent re-open of registry row S387 (falsification, wave 2)

Lane: mado-shokunin. Score tree: `28fc86ac2359ec27406d8a2c63bef82ea6e947ed` (working tree never scored).
Contract read first: `claims-frozen-v2.md`, `registration-v2.md`, `registration-v2-errata.md` (E12/E13/E14), `registration.md` §C1 where v2 is silent.
Seat scope: row **S387** only (`corpus/SOURCES.md` line 337 at the pin). Attack: wave 1 wrote the row and quoted from its own pin files; no independent seat had fetched the upstream bytes.

## Verdict

**S387: MATCH on every registered leg, with one defect (weakens, minor) and two cosmetic notes.**

| check | result | evidence |
|---|---|---|
| Independent fetch of the row URL | done | `curl -sSL https://raw.githubusercontent.com/hyprwm/Hyprland/efb50993780079460b0cbed1363e2166a2de1d9f/src/config/legacy/ConfigManager.cpp` → 90963 B, 2184 lines |
| sha256 vs anchor cell | MATCH | fetched `9db68cf44048d86557d8a53068dcc40b9bd7347c7d95f38edc501565f65be62b` = anchor cell `sha256:9db68cf4…` |
| sha256 vs `frozen-tables-v2.json` | MATCH | `c1.pin_sha256["Hyprland-legacy-ConfigManager.cpp"]` = same value (tables file sha256 verified `9511151a…795e2` first) |
| lane pin bytes vs upstream bytes | IDENTICAL | `git show <pin>:.ufo/waves/round-56/fetch/Hyprland-legacy-ConfigManager.cpp` `cmp` → identical (receipt) |
| URL commit is v0.56.2 as the source cell claims | MATCH | `git ls-remote https://github.com/hyprwm/Hyprland refs/tags/v0.56.2` → `efb50993780079460b0cbed1363e2166a2de1d9f` (single line = tag points straight at the commit) |
| gate quotes located in upstream bytes | MATCH | `w1/R56ScribeSourcesA/gate.md` S387: `Log::logger->log(Log::DEBUG, "CConfigManager: file {} modified, reloading", e.file);` → **line 1080**; `Log::logger->log(Log::WARN, "source= skipping directory {}", value);` → **line 1844**. Both byte-contained in the raw pin lines |
| entry K rows citing S387: quote at cited line, inside anchor | 8/8 MATCH | K17 1079, K18 1080, K19 1070, K20 776, K21 1836, K22 1835, K23 1844, K24 1816 — all quotes byte-contained at their cited lines; anchor set = {776, 1070, 1079-1080, 1816, 1835-1836, 1844} covers all 8 |
| entry E rows citing S387: inside anchor | **3/3 FAIL** | E05 line 630, E06 line 1838, E07 line 2134 — quotes verified byte-exact at those lines, but none of the three locators is in the anchor cell (defect D1 below) |
| anchor locators vs file last line | PASS | max locator 1844 ≤ 2184 lines (counter bound `len(blob.split(b"\n"))` = 2185); no overrun, registration-v2 E3 satisfied for this row |
| tier/kind/scope/teaches state only what the lines show | PASS | kind `code` (C++ source), tier `A` (primary upstream source; convention-consistent with S383-S386/S388/S389/S391). scope "watcher callback, which logs the modified file and reloads" = lines 1077-1082 (`init()` → `setOnChange` → log → `reload()`); "source= path that records each sourced config file" = lines 1816-1845 (`glob`, `is_regular_file` → `m_configPaths.emplace_back`, `is_directory` → WARN + skip). teaches: "callback registered in init logs the modified file and calls reload()" = 1077/1079/1080/1081; "source= globs, appends each regular file to m_configPaths, and skips directories with a warning" = 1816/1835/1836/1843-1844. No overstatement found |
| recheck cell valid | PASS | `on-release` = valid symbolic cadence (census E09 accepts ISO/NNd/symbolic; no E09 for S387). `opened` 2026-10-28 = gate access date; census E08 silent |
| `sources-census.sh validate` on scratch copy of the pin registry | 1 W, 0 E for S387 | `W04 S387 duplicate url …/src/config/legacy/ConfigManager.cpp across scopes` (note N1). No E01-E12 line mentions S387. Full output: receipt `census-validate.out` |

## Defects

**D1 — weakens the claim (minor): the anchor cell does not cover the entry's E rows.** The entry `corpus/knowledge/hyprland-config-autoreload-r56.md` cites S387 in three E rows whose quoted lines sit **outside** S387's anchor ranges `ConfigManager.cpp:776,1070,1079-1080,1816,1835-1836,1844`:
- E05 line 630 `resetHLConfig();` (constructor call — line verified inside `CConfigManager::CConfigManager()` which starts at line 480)
- E06 line 1838 `m_configCurrentPath          = value;` (sits between anchored 1836 and 1844 but in no listed range)
- E07 line 2134 `return m_configPaths;` (inside `getConfigPaths()`, line 2133)

All three quotes are byte-correct at the cited lines; the failure is anchor coverage, not quote identity. Mitigations, stated plainly: the frozen C1 `scope:<id>` leg evaluates **K rows only** (registration.md §C1 leg table: "(K) in the registry row's anchor cell…"), the frozen table `c1.k` contains exactly the 8 K rows, and no counted leg touches E rows — so this cannot flip any registered predicate; and the escape is systematic across the nine new rows, not S387-specific (E01 S388:66, E03 S383:106, E04 S389:1190 likewise outside; 6 of 9 E rows escape). The anchor was clearly built as exactly the K-line set. It still means three entry propositions rest on pin lines no row's anchor declares; a future row-open should extend the anchor (e.g. `…,630,1838,2134`) or the E rows should cite a covering row.

**N1 — cosmetic: census W04 (duplicate URL across scopes).** `sources-census.sh validate --today 2026-10-28 --file <pin copy>` prints `W04 S387 duplicate url raw.githubusercontent.com/hyprwm/Hyprland/efb5099…/src/config/legacy/ConfigManager.cpp across scopes`. The same URL at the same commit is already opened by S303, S317, S353, S368 (and siblings S384/S388/S389 get the same warning). W04 is a warning class the census docs define as not affecting lane cleanliness; no E04 (same URL **and** scope) fired — the scopes differ. No action forced by the contract.

**N2 — cosmetic: E05's quoted text is not unique in the pin.** `resetHLConfig();` occurs at lines 630, 731, 755. The entry disambiguates by line number and the proposition ("the constructor calls…") is correct for 630 (731/755 are inside `reload()`, which starts at 726). All other S387 quotes are unique in the file.

## Commands (decisive)

```
curl -sSL -o fetched.cpp 'https://raw.githubusercontent.com/hyprwm/Hyprland/efb50993780079460b0cbed1363e2166a2de1d9f/src/config/legacy/ConfigManager.cpp'
# → 90963 B; sha256 9db68cf44048d86557d8a53068dcc40b9bd7347c7d95f38edc501565f65be62b  (anchor cell = frozen-tables-v2 c1.pin_sha256 = MATCH)
git -C <lane> show 28fc86ac:.ufo/waves/round-56/fetch/Hyprland-legacy-ConfigManager.cpp | sha256sum
# → 9db68cf4… (identical); cmp pin fetched → IDENTICAL
git ls-remote https://github.com/hyprwm/Hyprland refs/tags/v0.56.2
# → efb50993780079460b0cbed1363e2166a2de1d9f  refs/tags/v0.56.2
/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --file <scratch>/regtree/corpus/SOURCES.md --today 2026-10-28
# → 33 W04 lines, 20 E11 lines, exit 1; only line mentioning S387: "W04 S387 duplicate url … across scopes"
```

The 20 E11 lines name S096-S339 only and are **artifacts of my partial scratch tree** (I archived only `corpus/` at the pin; every flagged path — `tools/mado-verify.sh`, `SKILL.md`, `quality/check-index.py`, `.ufo/waves/round-47/w1/ExecSupersede/rows.md`, etc. — was then verified present at the pin via `git cat-file -e 28fc86ac:<path>`: 8/8 EXIST). S387's used-by `corpus/knowledge/hyprland-config-autoreload-r56.md` resolves inside the archived tree; no E11 for S387.

## What I could not verify / limits

- Upstream bytes were fetched once (GitHub raw, 2026-10-28); a single fetch cannot rule out content negotiation or later upstream drift. The three-way hash agreement (fetch = anchor cell = frozen tables = lane pin) is the evidence; re-fetches on later dates would strengthen it.
- Census `validate` was run against a scratch copy of the registry at the pin with the `corpus/` tree of that commit staged (see E11 artifact note above). It did not run against the full lane tree.
- The count `len(blob.split(b"\n"))` (2185) is quoted because registration-v2 E3 uses that formula; `wc -l` gives 2184. Either bound leaves locator 1844 inside.
- Checks not run: none; every seat-assigned check ran. hyprctl/host reads: none needed. No tool installed or upgraded (system curl/git/python3/gawk only).

## Hygiene

- Lane read-only: `git show` / `git archive` (one archive: `corpus/`) / `git cat-file -e` / `git ls-remote` only. No commit/add/stash/checkout/reset anywhere near the lane or fleet repo; no fixture git repo was needed.
- Scratch `/fast/scratch/hyaku/mado-r56/R56W2ScoutRows3/` removed before yield (receipts copied first). No writes outside the seat deliverable paths and scratch. No credential material.

## Deliverables

- `.ufo/waves/round-56/w2/R56W2ScoutRows3.md` — this report
- `.ufo/waves/round-56/w2/R56W2ScoutRows3/sha256-receipts.txt` — fetch/pin/tables/registry hashes + cmp
- `.ufo/waves/round-56/w2/R56W2ScoutRows3/quote-checks.txt` — gate + K/E quote placement and anchor membership, per line
- `.ufo/waves/round-56/w2/R56W2ScoutRows3/census-validate.out` — full census validate output on the pin copy

Report: .ufo/waves/round-56/w2/R56W2ScoutRows3.md
