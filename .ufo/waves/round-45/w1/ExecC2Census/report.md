# ExecC2Census — C2 census line, 17 surfaces and 9 Gate quotes re-derived independently

Seat: ExecC2Census (w1, mado round 45). Lane: `/home/vgpnk/Projects/shokunin/mado-shokunin` (read-only for me; I wrote
only this seat dir and my Report file). Date: 2026-10-26.

**Result.** C2's frozen census line is exactly re-derived from the pins; all 17 surfaces are cited with a <= 30-line
locator on a keyword line; all 9 Gate quotes occur exactly once (raw and comment-stripped) with entry locators at the
quote start line; the positive control is admitted `1/1 TARGET_MET` (rc 0), base and 8 seeded mutants are `MISSED`.
Three entry locators clip the fact they carry and one sentence is `[INF]` from the pins; none of these moves the
predicate (they are invisible to clauses g/j by design). One clause-j survivor is demonstrated (truthless line still
admitted) — the declared residual, measured.

## 0. Bytes verified (provenance)

| artifact | sha256 |
|---|---|
| `quality/counters/c2-r45-monitor-entry.py` (frozen, unmodified) | `34fcc783b6e652b44f751fceb3af71626868d265758a6657f2af409cc75c51f6` |
| `.ufo/waves/round-45/l1-draft/entry.md` | `317e9fde55eca64ceb6e0850595a0460f0f3891c43be7629a6b0fe18bc9fd6f0` |
| `.ufo/waves/round-45/l1-draft/build-pos.py` | `7d8b54f887c5ccd75337d73943a2edd0255f9f4a5a12322f4beebc1a2aff3f26` |

`.ufo/waves/round-45/fetch/` (9 files): `sha256sum *` equals `receipts/fetch-sha256.txt` 9/9 (byte-identical table,
checked mechanically), all mode `100644` in the positive-control commit, smallest file 2700 B (`hyprutils-String.cpp`),
total 343333 B.

The lane HEAD moved from the freeze `22a8dedd` to the w1 dispatch commit `ebdba13f` while this seat ran (read-only
check): `git show HEAD:quality/counters/c2-r45-monitor-entry.py` and `…:l1-draft/entry.md` hash to the same two digests
above, and `corpus/knowledge/hyprland-monitor-rule-r45.md` is absent at HEAD — no data commit had landed when I
measured.

## 1. Census line re-derived by grep/awk (the counter was not run)

The primitives are named by clause h's own spec; each was then located and counted in the pinned bytes by hand-run
`grep -n`/`grep -cE`/`awk`, and the arithmetic (steps = N-1, key-block end at the first exact `}`) was recomputed here.

| token | pin:line | primitive | unique occurrences |
|---|---|---|---|
| `default_refresh=60` | `Hyprland-MonitorRule.hpp:46` | `float … m_refreshRate   = 60; // Hz` | 1 (`grep -cE 'float[[:space:]]+m_refreshRate[[:space:]]*=[[:space:]]*[0-9]+…;'`) |
| `refresh_tolerance=1` | `Hyprland-Monitor.cpp:837` | `!DELTALESSTHAN(bestMode->refreshRate / 1000.f, RULE->m_refreshRate, 1))` | 1 |
| `scale_step=1/120` | `Hyprland-Monitor.cpp:1001` | `float    searchScale = std::round(m_scale * 120.0);` (step base at `:1004` `scaleZero = searchScale / 120.0`) | 1 (`std::round\(m_scale \* [0-9]+\.0\)`) |
| `scale_search=89` | `Hyprland-Monitor.cpp:1010` | `for (size_t i = 1; i < 90; ++i)` — first such loop after `:1001`; steps = 90-1 = **89** | 1 |
| `json_refresh_decimals=5` | `Hyprland-HyprCtl.cpp:242` | `"refreshRate": {:.5f},` | 1 (`"refreshRate": \{:\.[0-9]f\}`) |
| `line_keys=8` | `Hyprland-legacy-ConfigManager.cpp:1293-1387` | `ARGS[argno] == "` occurrences from the `handleMonitor` signature to the first line that is exactly `}` (that `}` is `:1387`) | 8 |

The eight keys, in file order (offsets 60-81 from line 1293, i.e. `ConfigManager.cpp:1352,1355,1358,1361,1364,1367,1370,1373`):
`mirror`, `bitdepth`, `cm`, `sdrsaturation`, `sdrbrightness`, `transform`, `vrr`, `icc` — the entry's §1 list matches
exactly, and the unknown-key path is `ConfigManager.cpp:1378` (`return "invalid syntax at \"" + …`), which returns
before `monitorRuleMgr()->add` at `:1384`, so the line is dropped.

**Frozen line** at `entry.md:72`, byte-equal to the derivation:

```
hyprland monitor-rule default_refresh=60 refresh_tolerance=1 scale_step=1/120 scale_search=89 json_refresh_decimals=5 line_keys=8
```

`grep -n` on the entry: that line occurs once (`:72`); each of the six `name=` tokens occurs on no other line
(`default_refresh lines=[72] … line_keys lines=[72]`, `surfacecheck.out` tail). **MATCH**, no arithmetic slack: the
naive `scale_search=90` reading is caught (mutant M1 below).

## 2. The 17 SURFACES, anchor lines computed independently

Anchors were located with plain containment (`grep -F`, then re-run in my own script; no counter import). My transcribed
`SURFACES` table was compared mechanically to the counter's literal list: **17 rows, identical, 0 diffs**
(`surfaces_diff.out`). Each entry line is outside raw line 20 and unfenced.

| surface | receipt | anchor L | entry line | locator | width | keyword matched |
|---|---|---|---|---|---|---|
| parse-mode | Hyprland-Parser.cpp | 110 | 38 | 110-139 | 29 | `Mode` |
| parse-position | Hyprland-Parser.cpp | 145 | 44 | 145-173 | 28 | `Position` |
| parse-scale | Hyprland-Parser.cpp | 193 | 46 | 193-211 | 18 | `Scale` |
| handle-monitor | Hyprland-legacy-ConfigManager.cpp | 1293 | 34 | 1293-1299 | 6 | `handleMonitor` |
| invalid-syntax | Hyprland-legacy-ConfigManager.cpp | 1378 | 36 | 1351-1379 | 28 | `invalid syntax` |
| add-erase | Hyprland-MonitorRuleManager.cpp | 38 | 52 | 38, 37-42 | 0, 5 | `erase` |
| get-reverse | Hyprland-MonitorRuleManager.cpp | 96 | 54 | 96-106 | 10 | `reverse` |
| default-60 | Hyprland-MonitorRule.hpp | 46 | 42 | 46 | 0 | `60` |
| selector | Hyprland-Monitor.cpp | 1201 | 56 | 1201-1211 | 10 | `selector` |
| closeness | Hyprland-Monitor.cpp | 837 | 60 | 819-840 | 21 | `Hz` |
| scale-search | Hyprland-Monitor.cpp | 1001 | 62 | 1001, 997-1027 | 0, 30 | `scale` |
| json-refresh | Hyprland-HyprCtl.cpp | 242 | 68 | 241-242 | 1 | `refreshRate` |
| monitors-all | Hyprland-HyprCtl.cpp | 320 | 70 | 313-321 | 8 | `all` |
| explicit-position | Hyprland-MonitorPositionController.cpp | 27 | 64 | 27 | 0 | `explicit` |
| is-number | hyprutils-String.cpp | 50 | 48 | 50-79 | 29 | `number` |
| wiki-format | wiki-Monitors.md | 11 | 76, 78 | 11 and 7-12 | 0, 5 | `wiki` |
| wiki-sdr-eotf | wiki-Monitors.md | 253 | 78 | 253 | 0 | `sdr_eotf` |

17/17 covered; the widest range actually used is exactly `JWIDTH` (997-1027 = 30). My L values equal the counter's
reported `line=` values for all 17 (`counter-pos.out`), computed by a different code path.

## 3. The nine Gate quotes

`QUOTES` was extracted from `build-pos.py` with `ast.literal_eval` (no transcription). Receipt text was whitespace-collapsed
(newlines -> single space, mapped back to 1-based lines) and searched word-bounded; the comment-stripped pass removes
`/* */` and `//` for `.cpp/.hpp`.

| id | receipt | hits raw | hits stripped | words | quote start | entry locator |
|---|---|---|---|---|---|---|
| S302 | Hyprland-Parser.cpp | 1 | 1 | 5 | 134 | 134 |
| S303 | Hyprland-legacy-ConfigManager.cpp | 1 | 1 | 3 | 1345 | 1345 |
| S304 | Hyprland-MonitorRuleManager.cpp | 1 | 1 | 10 | 38 | 38 |
| S305 | Hyprland-MonitorRule.hpp | 1 | 1 | 4 | 46 | 46 |
| S306 | Hyprland-Monitor.cpp | 1 | 1 | 6 | 1001 | 1001 |
| S307 | Hyprland-HyprCtl.cpp | 1 | 1 | 4 | 241 | 241-242 |
| S308 | Hyprland-MonitorPositionController.cpp | 1 | 1 | 5 | 27 | 27 |
| S309 | hyprutils-String.cpp | 1 | 1 | 9 | 59 | 59 |
| S310 | wiki-Monitors.md | 1 | 1 | 6 | 11 | 11 |

- **9/9** exactly one occurrence raw and stripped; **0** cross-receipt hits (each quote searched against all nine fetch
  files: `cross.out`).
- Word counts 3-10, all inside the 3-25 bound (`S303` is exactly 3 tokens — the boundary case).
- Every entry locator contains the quote start line. `S307` is a range: the quote begins at the `"physicalHeight"` line
  `HyprCtl.cpp:241` and ends on `:242`, so `241-242` is the correct start-line locator.
- Registry anchor ranges in `build-pos.py` are all inside their receipt's line count (26 ranges checked, e.g.
  `Hyprland-Monitor.cpp:719-1082` in a 2816-line file) — no `ANCHOR-PAST-EOF`.

## 4. Positive control, base and the counter run

Recipe from the card, scratch under `/fast/scratch/hyaku/mado-r45/ExecC2Census`:
`git clone -q --shared --no-checkout <lane> "$D"` -> `rev-parse --show-toplevel == "$D"` (asserted) ->
`checkout --detach 22a8dedd…` -> `build-pos.py "$D"` (prints `applied`) -> `git add -A` -> commit
`-c user.name=seat -c user.email=seat@scratch.invalid`.

- **P**: `PRED-C2-r45: admitted=1/1 verdict=TARGET_MET rev=1b30c05185f080c1eda1dcdea8e681bf789ec5ed`
  (tree `a86472a8270504d401c34a4abbc564ba711d233a`), rc 0, clauses `a:1 … j:1` (`counter-pos.out`).
- **base** (`--rev 0c89478a…`): `admitted=0/1 verdict=TARGET_MISSED`, rc 1, every clause 0 (`clauses.out`).
- **8 seeded mutants** (each a fresh copy of P, one edit, one commit, counter at HEAD) — all `MISSED`
  (`mutate.out`), with clause isolation (`clauses.out`):

| mutant | edit | failing clause |
|---|---|---|
| M1 | census `scale_search=89` -> `90` | h only (a-g, i, j = 1) |
| M2 | census `json_refresh_decimals=5` -> `2` | h (same pattern) |
| M3 | census `line_keys=8` -> `7` | h |
| M4 | census line repeated twice | h (exactly-once) |
| M5 | `Hyprland-Parser.cpp:110-139` -> `110-141` (width 31) | j only, `surface=parse-mode … cited=0` |
| M6 | Gate quote S303 `ARGS[3]` -> `ARGS[4]` | d, with the expected cascade d/e/g/h/i = 0 |
| M7 | S302 locator `:134` -> `:133` | g only, `id=S302 obs=0 locator_line=134` |
| M8 | stray `scale_search=90 elsewhere` line | h |

- **Clause h is a derivation, not a constant** (`hderive.out`): importing the frozen counter as a module (main is
  guarded) and calling `host_census` on in-memory receipt bytes reproduces the entry line with `ok=True`; then six
  single-token byte mutations each move exactly one field and break the match — `60`->`50`, tolerance `1`->`2`,
  `* 120.0`->`* 240.0` (step 1/240), `i < 90`->`i < 75` (search 74), `{:.5f}`->`{:.3f}` (3), and one key branch
  removed (`8`->`7`; renaming the key string does *not* change the count, because the counter counts the
  `ARGS[argno] == "` prefix).
- **Survivor (declared residual, measured)**: replacing the S305 sentence with
  `**OBS** S305 - nothing here explains the monitor plane at all:` while keeping its quote and locator is still
  **admitted 1/1** (`survivor.out`, `surface=default-60 line=46 cited=1`). The round-44 D5 width bound closes the
  whole-file-locator hole but not the "keyword, not truth" hole; the constraint says so in clause j's residual, and it
  is load-bearing (a nonsense line passes). Cheap tightening if the L1 wants it: require the surface keyword to sit in
  the same sentence as the locator *and* require the surface's own name (e.g. `refreshRate`, `60 Hz`, `desc:`) —
  not required by the frozen predicate, so no change is proposed post-freeze.

## 5. Findings against the L1 entry (all invisible to the predicate; none moves the verdict)

**F1 (clipped locator, real).** `entry.md:44`: `parsePosition (Hyprland-Parser.cpp:145-173)` then asserts both branches,
but the explicit branch is `Parser.cpp:174-189` (`if (!value.contains("x"))`, two `stoi` calls at `:181-182`). The 30-line
bound makes the full function (145-191 = 46 lines) unrepresentable, so the sentence needs a second locator
(`Hyprland-Parser.cpp:174-189`). Clause j is satisfied by 145-173 because it only needs the anchor line 145.

**F2 (clipped locator, real).** `entry.md:54`: "…then a built-in default (preferred, auto, auto)
(Hyprland-MonitorRuleManager.cpp:96-106)". 96-106 holds the reverse search and the empty-selector loop; the built-in
default is `MonitorRuleManager.cpp:108-117` (`fallbackRule.m_resolution = Vector2D{}`, `m_autoDir = DIR_AUTO_RIGHT`,
`m_scale = -1`). The S304 anchor cell (`:44-117`) covers it; the entry line does not.

**F3 (clipped locator, real).** `entry.md:70`: "…otherwise only the active list is printed
(Hyprland-HyprCtl.cpp:313-321)". 313-321 holds the argument parse and the `all` flag; the selection is
`HyprCtl.cpp:327` (JSON: `allMonitors ? allMonitors() : monitors()`) and `:335` (text). Add `Hyprland-HyprCtl.cpp:327`.

**F4 (`[INF]` from the pins).** `entry.md:33`: "the handler splits the line on commas" is stated **OBS** over
`ConfigManager.cpp:1295` `CVarList2(std::string(args))`. `CVarList2`'s defining class is not in the pins; the only
delimiter evidence is explicit-delimiter call sites (`ConfigManager.cpp:111` `' '`, `:1781` `','`, `Parser.cpp:15`
`'s'`). On this host a comma line works, so the claim is true in practice, but the comma default is not pinned —
label it `[INF]` or pin the class. **Observation, not a defect in the counted data.**

**F5 (minor).** `entry.md:36` cites `Hyprland-Parser.cpp:110-139` for "a `modeline` keyword parses a custom DRM mode";
the dispatch `parseModeLine(value, m_rule.m_drmMode)` is at `:119` (inside), the keyword test `if (keyword != "modeline")`
is at `:20` (outside). Fine for the counter; a reader may want `:14-24` as well.

**F6 (convention, not a defect).** `entry.md:64` quotes three statements (`MonPos:27,28,29`) with locator `27`. Clause g
defines the locator as the quote's start line, so this is correct; noting it because the quote is 3 lines long.

Everything else I checked against the pins is exact: handleMonitor modifier body 1299-1343 (transform copy 1309-1316,
addreserved fall-through 1335-1341), parse-error-then-add 1384-1386 (dispatch returns ignored at 1345-1347), add =
erase-then-append 37-42, client override lambda 45-84, `matchesStaticSelector` 1201-1211 (`desc:` at 1202, 1206),
shortDescription 255-256, JSON args 277-288 (`scale` 282, `disabled` 285, `mirrorOf` "none" 286), mode choice 819-840
and keyword modes 784-817, scale correction 997-1027 (89-step loop), fallback 1029-1036, notification 1038-1049,
`isNumber` delegation `String.cpp:46-48` -> `isNumber2` 50-84 (`.` not first 71, last char digit 83), wiki format
`Monitors.md:11`, `sdr_eotf` `:253`, monitorv2 block `ConfigManager.cpp:819-831`.

## 6. Host §6 claim (read-only, session material shape-only)

- Receipt `.ufo/waves/round-45/receipts/live-monitors-host-l1.txt`: `MADO_MON_OUTPUT: … verdict=AGREE`,
  `MADO_MONITORS: … agree=1 differ=0 disabled=0 verdict=OK`, `# exit=0`. Config sha in receipt `69c9d899…` equals the
  current `~/.config/hypr/monitors.conf`; tool sha `c6ac5fc2…` equals `l1-draft/mado-monitors.py`.
- `~/.config/hypr/monitors.conf:10` is `monitor = DP-1, 3440x1440@100, 0x0, 1` (one active rule).
- `hyprctl monitors all -j`, projected to `name,width,height,refreshRate,x,y,scale,transform,disabled,mirrorOf`:
  `DP-1, 3440, 1440, 99.997, 0, 0, 1, 0, false, none`; raw text `"refreshRate": 99.99700` (the exact five-decimal form
  the entry quotes). Description/serial/make/model were dropped before anything was printed or written.

## 7. Limits of this seat

- C1 (`tools/mado-monitors.py`, its counter and 49 fixtures) is not mine and was not run.
- The pins are the trust root: everything above is code-read at efb50993 / hyprutils v0.14.2, not Hyprland runtime.
- The L1's control P commit `2cbee932…` is not in the lane (scratch deleted), so I could not compare trees; my P is an
  independent rebuild from the same freeze and the same frozen drafts (content-addressed tree recorded above).
- Clause c/e/f/i were spot-checked (rows `mined`/used-by, README row at `corpus/README.md:73`, no `BAD_LOC` marker in
  entry or rows — 0 hits, Gate receipts = the 9 pins) but not re-implemented; the counter's own output is the record.

## Hygiene

No package operations (pacman paused, untouched), no installs, no mutating git in the lane or fleet, no compositor
mutation — only `hyprctl monitors all -j` (allowed read). Fixture clones lived under
`/fast/scratch/hyaku/mado-r45/ExecC2Census/` with `-C "$D"` on every git call and a toplevel assertion; the scratch dir
(including the P clone and all mutant clones) is deleted. Evidence copies are in this seat dir:
`quotecheck.py/.out`, `surfacecheck.py/.out`, `counter-pos.out`, `mutate.out`, `clauses.out`, `hderive.py/.out`,
`survivor.out`, `cross.out`, `keywords.out`, `surfaces_diff.out`.
