# ExecC2Census — C2 census, surfaces and Gate quotes, independently re-derived (w1, round 45)

Status: **COMPLETE**. Lane read-only for me; I wrote only `.ufo/waves/round-45/w1/ExecC2Census/` (report + evidence) and
this file. Frozen bytes checked: counter `c2-r45-monitor-entry.py` `34fcc783…c75c51f6`, `l1-draft/entry.md`
`317e9fde…bc9fd6f0`, `l1-draft/build-pos.py` `7d8b54f8…1a2aff3f26`.

## Verdicts

| target | independent result |
|---|---|
| census line (clause h) | **MATCH** — `60 / 1 / 1/120 / 89 / 5 / 8` re-derived from the pins by grep/awk, byte-equal to `entry.md:72`, which is the only line carrying those six `name=` tokens |
| 17 SURFACES (clause j) | **17/17 cited** — anchors computed by plain containment in my own script; my computed line equals the counter's reported `line=` for all 17; every locator <= 30 lines on a keyword line; widest used is exactly 30 |
| 9 Gate quotes (clause d) | **9/9** exactly once raw and comment-stripped, 0 cross-receipt hits, 3-10 words, every entry locator contains the quote start line |
| positive control | **admitted=1/1 TARGET_MET**, rc 0, rev `1b30c051…` tree `a86472a8…` |
| base | `admitted=0/1 TARGET_MISSED`, rc 1, all clauses 0 |
| seeded mutants | **8/8 MISSED** with clause isolation (h only / j only / g only / d-cascade) |
| clause-h derivation | proven derivational: six single-token pin mutations each move exactly one field |
| clause-j truth residual | **measured survivor**: a nonsense sentence keeping the S305 quote+locator is still `admitted=1/1` |

## Census, with the pin evidence

`default_refresh=60` `Hyprland-MonitorRule.hpp:46`; `refresh_tolerance=1` `Hyprland-Monitor.cpp:837`; `scale_step=1/120`
`Hyprland-Monitor.cpp:1001` (base `:1004`); `scale_search=89` from `Hyprland-Monitor.cpp:1010`
`for (size_t i = 1; i < 90; ++i)` (steps = 90-1); `json_refresh_decimals=5` `Hyprland-HyprCtl.cpp:242`
`"refreshRate": {:.5f},`; `line_keys=8` in `Hyprland-legacy-ConfigManager.cpp:1293-1387` (block ends at the first line
that is exactly `}`, `:1387`) counting `ARGS[argno] == "`: mirror, bitdepth, cm, sdrsaturation, sdrbrightness, transform,
vrr, icc. Each primitive's regex hits **exactly one** line. The naive `90` reading is rejected (mutant M1 -> h=0 only).

## Findings against the entry (invisible to the frozen predicate; none moves the verdict)

- **F1 clipped locator.** `entry.md:44` `parsePosition (Hyprland-Parser.cpp:145-173)` then asserts the explicit branch,
  which is `Parser.cpp:174-189` (`stoi` at `:181-182`). The full function is 46 lines, so the 30-line bound forces a
  second locator; 173 stops at the end of the auto branch.
- **F2 clipped locator.** `entry.md:54` "then a built-in default (preferred, auto, auto)
  (Hyprland-MonitorRuleManager.cpp:96-106)" — 96-106 is the reverse search + empty-selector loop; the built-in default
  is `MonitorRuleManager.cpp:108-117` (`m_resolution = Vector2D{}`, `DIR_AUTO_RIGHT`, `m_scale = -1`).
- **F3 clipped locator.** `entry.md:70` "otherwise only the active list is printed (Hyprland-HyprCtl.cpp:313-321)" —
  313-321 is the argument parse and the `all` flag; the selection is `HyprCtl.cpp:327` (JSON) and `:335` (text):
  `allMonitors ? allMonitors() : monitors()`.
- **F4 `[INF]` from the pins.** `entry.md:33` "splits the line on commas" is graded **OBS** over
  `ConfigManager.cpp:1295` `CVarList2(std::string(args))`; `CVarList2`'s class is not pinned, and the only delimiter
  evidence is explicit-argument call sites (`:111` `' '`, `:1781` `','`, `Parser.cpp:15` `'s'`). True on the host,
  not established by the pins; either label it INF or pin the class.
- **F5 minor.** `entry.md:36` cites `Parser.cpp:110-139` for the `modeline` keyword; the dispatch is `:119` (inside), the
  keyword test is `:20` (outside).
- **F6 convention.** `entry.md:64` quotes `MonitorPositionController.cpp:27-29` with locator `27`; clause g defines the
  locator as the quote's start line, so this is correct, not a defect.

Everything else checked is exact: modifier body 1299-1343, add-then-error 1384-1386, add/erase 37-42, client override
45-84, `desc:` selector 1201-1211, short description 255-256, JSON args 277-288, mode choice 819-840 / keywords
784-817, scale correction 997-1027, fallback 1029-1036, notification 1038-1049, `isNumber`->`isNumber2` 46-84,
wiki format `:11`, `sdr_eotf` `:253`, monitorv2 block `ConfigManager.cpp:819-831`. Registry anchors: 26 ranges, all
inside their receipt line counts. PINS dict == `receipts/fetch-sha256.txt` 9/9; fetch blobs mode `100644`.

## Host §6 (read-only, projected fields only)

`live-monitors-host-l1.txt` gives `verdict=AGREE`, `verdict=OK`, `exit=0`; its config sha `69c9d899…` equals
`~/.config/hypr/monitors.conf`, its tool sha `c6ac5fc2…` equals `l1-draft/mado-monitors.py`; the config's only active
rule is `monitors.conf:10` `monitor = DP-1, 3440x1440@100, 0x0, 1`; `hyprctl monitors all -j` shows DP-1 3440x1440,
`"refreshRate": 99.99700`, 0x0, scale 1, transform 0, not disabled, `mirrorOf` none. No serial/description/model
retained anywhere.

## Risks / notes

- The predicate's clause j binds a keyword, not truth: F1-F3 pass j, and a truthless line passes too (survivor). This
  is the declared residual; tightening it after the freeze is the L1's call.
- L1 control P rev `2cbee932…` is not in the lane, so I could not diff trees; my P is an independent rebuild from freeze
  `22a8dedd` + the frozen drafts.
- Limits: pins are code at efb50993 / hyprutils v0.14.2, not runtime; C1 is another seat.

Evidence (in `.ufo/waves/round-45/w1/ExecC2Census/`): `report.md`, `quotecheck.py/.out`, `surfacecheck.py/.out`,
`counter-pos.out`, `mutate.out`, `clauses.out`, `hderive.py/.out`, `survivor.out`, `cross.out`, `keywords.out`,
`surfaces_diff.out`. No installs, no pacman, no mutating git; scratch `/fast/scratch/hyaku/mado-r45/ExecC2Census`
deleted.

Lane HEAD was `ebdba13f` (w1 dispatch) at the end of this seat; the counter and `l1-draft/entry.md` at HEAD hash to the
same digests as the bytes I verified, and the data entry was still absent — nothing I measured reads a landed data
commit.
