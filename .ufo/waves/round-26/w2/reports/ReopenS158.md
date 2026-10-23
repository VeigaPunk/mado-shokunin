# ReopenS158 — re-open of draft row S158 and used-by-extension rows S158/S162

Date: 2026-10-23. Item: ReopenS158 (re-open contract, wave w2). Leaf seat; no subagents, no installs, no Hyprland/compositor contact, no lane edits except this report.

## What I did

1. Re-fetched S158's pinned URL and S162's pinned URL by ordinary fetch and compared digest/size with `corpus/SOURCES.md` rows (S158 at line 170, S162 at line 174).
2. Checked every quote in the w1 reports `SrcHyprctlAnims.md` (S158's new quotes) and `SrcAnimConfig.md` (S162's new quotes) against the re-fetched pinned bytes: whitespace-collapsed substring, word count ≤ 25, and presence at the cited line.
3. Spot-checked each report's behavioral narrative against the pinned bytes.

## Fetch receipts (exact commands)

```sh
df -h /fast   # 804G total, 145G avail before writes
mkdir -p /fast/scratch/hyaku/mado-r26/reopen
timeout 30s prlimit --as=4000000000 -- curl -fsSL "https://raw.githubusercontent.com/hyprwm/Hyprland/efb50993780079460b0cbed1363e2166a2de1d9f/src/debug/HyprCtl.cpp" -o /fast/scratch/hyaku/mado-r26/reopen/ReopenS158.bin
timeout 30s prlimit --as=4000000000 -- curl -fsSL "https://raw.githubusercontent.com/hyprwm/Hyprland/efb50993780079460b0cbed1363e2166a2de1d9f/src/config/legacy/ConfigManager.cpp" -o /fast/scratch/hyaku/mado-r26/reopen/ReopenS158-S162.bin
```

| Artifact | sha256 (fresh) | bytes (fresh) | row pins | match |
|---|---|---|---|---|
| `ReopenS158.bin` (S158) | `798b7c6c4c1684557842463d46ac99c96629be4179e0e461dca77670247b91fa` | 97582 | `798b7c6c4c1684557842463d46ac99c96629be4179e0e461dca77670247b91fa`, 97582 B | exact |
| `ReopenS158-S162.bin` (S162) | `9db68cf44048d86557d8a53068dcc40b9bd7347c7d95f38edc501565f65be62b` | 90963 | `9db68cf44048d86557d8a53068dcc40b9bd7347c7d95f38edc501565f65be62b`, 90963 B | exact |

Supplemental fetches for S162's out-of-row quote (see below):

```sh
timeout 30s prlimit --as=4000000000 -- curl -fsSL "https://raw.githubusercontent.com/hyprwm/hyprutils/v0.14.2/include/hyprutils/string/VarList.hpp" -o /fast/scratch/hyaku/mado-r26/reopen/ReopenS158-varlist-hyprutils.bin
timeout 30s prlimit --as=4000000000 -- curl -fsSL "https://raw.githubusercontent.com/hyprwm/Hyprland/efb50993780079460b0cbed1363e2166a2de1d9f/src/helpers/varlist/VarList.hpp" -o /fast/scratch/hyaku/mado-r26/reopen/ReopenS158-varlist-hyprland.bin
```

| Artifact | sha256 (fresh) | bytes | report's provenance table | match |
|---|---|---|---|---|
| `ReopenS158-varlist-hyprutils.bin` | `9ad2fcbd5de691166b7db95de09b6bd054c9b4313deb3187e84c914dab74fc43` | 1883 | same sha; 1,883 B | exact |
| `ReopenS158-varlist-hyprland.bin` | `79fe2000a24c5bb42e7b586840bed8ed358cb802db049d8c2d778d240be19e80` | 148 | same sha; 148 B | exact |

## Quote checks — S158 via SrcHyprctlAnims.md (new quotes for the used-by extension)

All four quotes re-checked independently with Python (whitespace-collapsed substring of the decoded UTF-8 bytes; word count; line location by collapsed-line match):

| # | Quote (collapsed) | substring | words | found at | cited | line ok |
|---|---|---|---|---|---|---|
| 1 | `ret += "[[";` | yes | 3 | 947 | 947 | yes |
| 2 | `ret += ",\n[";` | yes | 3 | 964 | 964 | yes |
| 3 | node fields block (`"name"`, `"overridden"`, `"bezier"`, `"enabled"`, `"speed": {:.2f}`, `"style"`) | yes | 12 | 951–956 | 951–956 | yes |
| 4 | bezier fields block (`"name"`, `"X0"/"Y0"/"X1"/"Y1": {:.2f}`) | yes | 10 | 970–974 | 970–974 | yes |

Narrative cross-checks against the pinned bytes: `animationsRequest` defined at line 927 (report: 927–985) and registered via `registerCommand(SHyprCtlCommand{"animations", true, animationsRequest});` at line 2018 (report: 2018) — both exact. Node array closed at 962 (`ret[ret.length() - 1] = ']';` — an in-place overwrite of the trailing comma, consistent with the report's "closing the node array at line 962"); both arrays closed by `ret += "]]";` at 981. The bezier loop iterates `Animation::mgr()->getAllBeziers()` (line 966) with `getControlPoints()` (967), matching "Bezier coordinates come from control points 1 and 2". The report's own claim `quote_1..4=True` reproduces.

## Quote checks — S162 via SrcAnimConfig.md (new quotes for the used-by extension)

| # | Quote (collapsed) | substring of pinned bytes | words | found at | cited | line ok |
|---|---|---|---|---|---|---|
| 2 | `if (!Config::animationTree()->nodeExists(ANIMNAME)) … int64_t enabledInt = ParserUtils::parseInt(ARGS[1]).value_or(0) == 1;` | yes | 24 | 1434–1438 | 1434–1438 | yes |
| 3 | `return "invalid speed"; … if (!Animation::mgr()->bezierExists(bezierName)) return "no such bezier";` | yes | 24 | 1457–1467 | 1457–1467 | yes |
| 4 | `Config::animationTree()->setConfigForNode(ANIMNAME, …) … return {};` | yes | 20 | 1469–1478 | 1469–1478 | yes |

Word counts match the report's own claims (24/24/20).

Quote 1 of SrcAnimConfig cites a *different* file — `include/hyprutils/string/VarList.hpp:14 @ hyprutils v0.14.2` — so it is not contained in S162's pinned bytes; this is expected and disclosed by the report's own citation. I verified it against a fresh fetch of the cited file: substring yes, exactly 18 words (report: 18), found exactly at line 14, and the digest matches the report's provenance table. The report's claim that Hyprland reaches this declaration through `src/helpers/varlist/VarList.hpp:3` also reproduces (line 3 is `#include <hyprutils/string/VarList.hpp>`).

Narrative cross-checks against S162's pinned bytes: `handleBezier`/`handleAnimation` registered at lines 612/613 (report: 612–613); disabled branch at 1444–1446 sets `setConfigForNode(ANIMNAME, enabledInt, 1, "default")` and returns success (report: "disabled with speed 1 and bezier `default`"); the ineffective post-boolean range check with its comment is at 1440–1442; speed gate `isNumber(ARGS[2], true)` at 1452 with `speed <= 0` → `"invalid speed"` at 1455–1457; bezier handler 1389–1424 contains `too few arguments` (1395), `invalid point` (1397), `std::stof` (1398), `too many arguments` (1419), and `addBezierWithName` (1421); lines 287–309 contain the `CParseResult`/`setError` conversion.

## used-by extension rows

`corpus/SOURCES.md` (lane tip 1b0b91e9) already carries the extensions described in `drafts/sources-rows.md`: S158's used-by is `corpus/knowledge/rule-attribution-r24.md, corpus/knowledge/animation-table-r26.md` (line 170) and S162's is `corpus/knowledge/rule-attribution-r24.md, corpus/knowledge/bind-table-r25.md, corpus/knowledge/animation-table-r26.md` (line 174), matching the SrcAnimConfig proposal verbatim. The new quotes motivating both extensions all verify against the rows' pinned bytes as shown above.

## Verdict

REOPEN S158 agree — fresh bytes byte-identical to the pinned digest/size; all 4 quotes are substrings at their exact cited lines, all ≤ 25 words; narrative claims (927–985, 947, 951–956, 962, 964, 970–974, 981, 2018) reproduce.
REOPEN S162 agree — fresh bytes byte-identical to the pinned digest/size; the 3 in-row quotes verify at their cited lines with the claimed word counts; the 4th quote correctly cites the supplemental hyprutils header and verifies there (line 14, 18 words, digest match); narrative claims (612–613, 1389–1424, 1440–1447, 1452–1457, 287–309) reproduce.

## Residual risk / gaps

- Both rows pin line *ranges* far wider than the animation content (S158: 346-484,613-630,647-723,1463-1645,2003-2044; S162: 419-451,590-623,893-968,2016-2093); the animation quotes (S158 927–985, S162 1389–1479) sit outside those row-pinned ranges, relying on the row's digest-level pin plus the w1 report. Digest equality makes this safe today; a future re-pin that changes bytes would need these ranges re-checked.
- S162 Q4's report caveat ("does not establish whether later config processing rolls the state back") remains open — out of scope for a re-open, no counter or runtime evidence involved here.
- Verification was static quote/digest work; no oracle, counter, or Hyprland instance was run, per contract.

Tool installs: none. All spawned processes were short-lived (`curl` under `timeout`/`prlimit`); nothing left running. Artifacts: `/fast/scratch/hyaku/mado-r26/reopen/{ReopenS158,ReopenS158-S162,ReopenS158-varlist-hyprutils,ReopenS158-varlist-hyprland}.bin`; this report.
