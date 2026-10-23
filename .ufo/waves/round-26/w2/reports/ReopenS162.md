# ReopenS162 — re-open draft row S162 (legacy ConfigManager.cpp), plus co-scoped S158 quotes

Date: 2026-10-23. Item: `Reopen contract for draft row S162`. Per the assignment's "For S158/S162 (existing rows whose `used-by` is extended) check the new quotes against the row's pinned bytes", I re-opened both rows' URLs fresh and checked every quote in each backing w1 report (S162 → `w1/reports/SrcAnimConfig.md`; S158 → `w1/reports/SrcHyprctlAnims.md`). Source-opening only; no counter, control, or Hyprland instance was run.

## Row text (as committed at tip 1b0b91e9)

- **S162** (`corpus/SOURCES.md:174`): `https://raw.githubusercontent.com/hyprwm/Hyprland/efb50993780079460b0cbed1363e2166a2de1d9f/src/config/legacy/ConfigManager.cpp` — anchor `sha256:9db68cf44048d86557d8a53068dcc40b9bd7347c7d95f38edc501565f65be62b, 90963 B`.
- **S158** (`corpus/SOURCES.md:170`): `https://raw.githubusercontent.com/hyprwm/Hyprland/efb50993780079460b0cbed1363e2166a2de1d9f/src/debug/HyprCtl.cpp` — anchor `sha256:798b7c6c4c1684557842463d46ac99c96629be4179e0e461dca77670247b91fa, 97582 B`.

Draft line (`.ufo/waves/round-26/drafts/sources-rows.md:11`): in-place `used-by` extensions for S158 and S162, `+ corpus/knowledge/animation-table-r26.md`.

## Re-open receipts (fresh ordinary fetches, today)

All commands of the form `timeout 90 prlimit --as=4000000000 -- curl -fsSL <URL> -o <PATH> && sha256sum <PATH> && wc -c <PATH>`; all exit 0.

| Fetch | sha256 | bytes | vs pinned/recorded |
|---|---|---|---|
| `reopen/ReopenS162.bin` ← S162 URL | `9db68cf44048d86557d8a53068dcc40b9bd7347c7d95f38edc501565f65be62b` | 90963 | **matches row exactly** |
| `reopen/ReopenS162-S158.bin` ← S158 URL | `798b7c6c4c1684557842463d46ac99c96629be4179e0e461dca77670247b91fa` | 97582 | **matches row exactly** |
| `reopen/ReopenS162-varlist-hpp.bin` ← `hyprutils/v0.14.2/include/hyprutils/string/VarList.hpp` | `9ad2fcbd5de691166b7db95de09b6bd054c9b4313deb3187e84c914dab74fc43` | 1883 | matches report-recorded digest (no ledger row; supplemental) |
| `reopen/ReopenS162-varlist-impl.bin` ← `hyprutils/v0.14.2/src/string/VarList.cpp` | `b02df8d688519366e7f20de5c3c44d21c3832316e8262ced0d295e129b166a36` | 1189 | matches report-recorded digest |
| `reopen/ReopenS162-legacy-header.bin` ← `src/config/legacy/ConfigManager.hpp` | `32afb1719c61ccb94b89d07cb0e5e9e6885e2531b5a3ad0507d52e89660fca5b` | 8421 | matches report-recorded digest |
| `reopen/ReopenS162-dispatcher.bin` ← `src/config/ConfigManager.cpp` | `c10dc1ce6602a854121a79fb0192c9f43aa836a35f9acb98ff1789541b01f366` | 2597 | matches report-recorded digest |

Fetch artifacts under `/fast/scratch/hyaku/mado-r26/reopen/`; nothing written into the lane except this report.

## Quote verification (whitespace-collapsed substring of the re-fetched decoded bytes; words = whitespace-separated tokens)

**S162 / SrcAnimConfig.md — 4/4 pass:**

| Quote | Cited at | Substring | Words (≤25) | Cited lines match |
|---|---|---|---|---|
| Q1 `CVarList(const std::string& in, … removeEmpty = false);` | hyprutils VarList.hpp:14 | True | 18 | yes — line 14 is exactly this declaration |
| Q2 `nodeExists` + `"no such animation"` + `parseInt` block | legacy ConfigManager.cpp:1434–1438 | True | 24 | yes — lines 1434–1438 verbatim |
| Q3 `"invalid speed"` pair + `bezierName`/`"no such bezier"` | :1457–1467 | True | 24 | yes — lines 1457–1467 verbatim |
| Q4 `setConfigForNode` + `styleValidInConfigVar` + `return {}` | :1469–1478 | True | 20 | yes — lines 1469–1478 verbatim |

**S158 / SrcHyprctlAnims.md — 4/4 pass:**

| Quote | Cited at | Substring | Words (≤25) | Cited lines match |
|---|---|---|---|---|
| Q1 `ret += "[[";` | HyprCtl.cpp:947 | True | 3 | yes — line 947 verbatim |
| Q2 `ret += ",\n[";` (literal `\n` escape) | :964 | True | 3 | yes — line 964 verbatim |
| Q3 node-field template (`name`, `overridden`, `bezier`, `enabled`, `speed` `{:.2f}`, `style`) | :951–956 | True | 12 | yes |
| Q4 bezier-field template (`name`, `X0`–`Y1` all `{:.2f}`) | :970–974 | True | 10 | yes |

Method: `re.sub(r'\s+', ' ', text).strip()` on both haystack bytes and needle, substring test, `len(needle.split())` for words; cited lines printed and compared verbatim. Each w1 report's own counts (`S162`: 18/24/24/20; `S158` report states pass-booleans only) agree with re-measurement.

## Spot checks of report prose against the re-fetched bytes

- `::handleBezier`/`::handleAnimation` registered at lines 612–613 of the legacy impl: confirmed (`registerHandler(&::handleBezier, "bezier"…)` / `(&::handleAnimation, "animation"…)`).
- Static error-conversion callbacks present at :287– (`static Hyprlang::CParseResult handleBezier` at :287).
- `handleBezier` opens at :1389 with `const auto ARGS = CVarList(args)`; `handleAnimation` opens at :1426 likewise; closing `}` at :1479. Confirmed.
- Legacy header declarations at `ConfigManager.hpp:90–91` (both handler prototypes): confirmed on the re-fetched 8,421 B header.
- Dispatcher `src/config/ConfigManager.cpp` selects `Lua::CConfigManager` for `.lua` and the legacy manager otherwise (:33–49): consistent with the report's "config-manager selector" description.
- hyprutils `VarList.cpp` splits on the delimiter parameter and `trim`s each token: confirmed (quoted impl above).

## Consistency of the extension

- S162's proposed used-by (`rule-attribution-r24.md, bind-table-r25.md, animation-table-r26.md`) and S158's (`rule-attribution-r24.md, animation-table-r26.md`) each match the w1 reports' proposals, and the working-tree `corpus/SOURCES.md` rows already carry exactly these cells (uncommitted `M corpus/SOURCES.md` at tip `1b0b91e9`; draft still lists the extension). No text disagreement.
- Observation (not a defect): the new citations fall partly outside the rows' listed anchors — S162 quotes/cites :287–309 and :1389–1479 beyond the row's `419-451,590-623,893-968,2016-2093` (:612–613 does sit inside `590–623`); S158 cites :927–985,:2018 beyond `346-484,613-630,647-723,1463-1645,2003-2044`. Anchor is not an in-place cell (round-13 errata), so the knowledge article must carry its own line cites — which both w1 reports provide.

## Verdicts

- `REOPEN S162 agree` — re-fetched bytes reproduce the pinned sha256/90963 B; all 4 new quotes are whitespace-collapsed substrings, ≤25 words, at the cited lines; prose anchors spot-verified; used-by extension consistent.
- `REOPEN S158 agree` — re-fetched bytes reproduce the pinned sha256/97582 B; all 4 new quotes pass the same checks.

Limits: supplemental hyprutils/dispatcher files have no ledger rows; they were checked against the w1 report's recorded digests and (for quote 1) substring. A `REOPEN … agree` is a bytes/quote agreement finding, not an admission decision. Tool installs: none.
