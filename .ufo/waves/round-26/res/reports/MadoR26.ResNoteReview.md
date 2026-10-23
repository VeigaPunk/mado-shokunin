# Residual review — corpus/knowledge/animation-table-r26.md (round 26, seat MadoR26.ResNoteReview)

2026-10-23. Read-only lane check: every bracketed citation in
`corpus/knowledge/animation-table-r26.md` was resolved against the fetched copies in
`.ufo/waves/round-26/fetch/`, and the landed-tool claims were checked against
`tools/mado-anims.py` @ 2b3487f7, `.ufo/waves/round-26/c1/count-v2.py`, and
`.ufo/waves/round-26/evidence/c1-after-v2-2b3487f7.txt`.

No `lsp` device is present in this session's tool inventory (and the S162/S158/S176
targets exist only as fetched `.bin` copies, not workspace files), so all citation
checks are text-exact `:raw` range reads of the fetch corpus. Nothing was written to
the lane except this report; no counters were run (receipts already present were
read, not re-measured).

## Verdict

`NOTE sound (0)`

## Citation-by-citation verification

Fetch identity map (sha256, line counts measured this session):
- `SrcAnimConfig-legacy-impl.bin` = `SrcAnimConfig.bin` (both `9db68cf4…be62b`, 2184 lines) = `src/config/legacy/ConfigManager.cpp` @ efb5099 (S162).
- `SrcHyprctlAnims.bin` (`798b7c6c…b91fa`, 2346 lines) = `src/debug/HyprCtl.cpp` @ efb5099 (S158).
- `SrcAnimTree.bin` (`313ed201…e7bae`, 83 lines) = `src/config/shared/animation/AnimationTree.cpp` (S176).
- `SrcAnimTreeHyprutils.bin` (`dbb5d50a…268e`, 70 lines) = hyprutils `src/animation/AnimationConfig.cpp` (S177 @ v0.14.2).
- `WikiAnimations-legacy.bin` (`f30f6bf4…4120b`, 115 lines) = legacy wiki `content/Configuring/Animations.md` (S175).

| doc line | citation | result |
|---|---|---|
| 15 | S175 `Animations.md:8-12,14-24` | OK — 8 keyword, 10-12 `animation = NAME, ONOFF, SPEED, CURVE [,STYLE]`; 14-15 `0`/`1` + omit-further-args-when-0; 23-24 unset nodes inherit parent's values. |
| 17 | S162 `ConfigManager.cpp:612-613` | OK — 612 `registerHandler(&::handleBezier, "bezier", …)`, 613 `registerHandler(&::handleAnimation, "animation", …)`, exactly those two lines. |
| 21 | S176 `AnimationTree.cpp:14-60`; S162 `1432-1435,1469` | OK — reset() creates all 35 nodes at 15-59; handler requires `nodeExists` (1434-1435) and only calls `setConfigForNode` (1469), no create. |
| 26-60 (tree) | (S176 14-60 implicit) | OK — parent/order of every listed node matches the createNode calls, incl. `borderangle`/`shadowangle`/`glowangle` under `global` and both roots. |
| 63 | S176 `61-66` | OK — 62 `global` (1, 8, "default"), 63 `__internal_fadeCTM` (1, 5, "linear"), 64-66 the three angles (0, 1, "default"). |
| 65 | S177 `AnimationConfig.cpp:9-28,35-48` | OK (against `SrcAnimTreeHyprutils.bin`) — 19 `overridden=false`, 14-16+25 parent link when present, 24 `pValues = parentRef->pValues : pConfig` (itself for a root); 41 `overridden=true`, 42-45 internal values, 47 parent link kept ("keep the parent!"). |
| 67 | S177 `61-70` | OK — setAnimForChildren recurses only `pParentAnimation == PANIM && !overridden` children, setting `pValues = PANIM->pValues`; overridden descendants skipped. |
| 71 | S162 `1389-1423` | OK — ARGS[0] name (1392), per-coordinate empty→`too few arguments` / `!isNumber`→`invalid point` (1394-1413), `std::stof` (1398-1412), nonempty ARGS[5]→`too many arguments` (1415-1416), `addBezierWithName` (1418); no nonempty-name or range check present. |
| 73 | S162 `1432-1447` | OK — `no such animation` (1434-1435); `ParserUtils::parseInt(ARGS[1]).value_or(0) == 1` verbatim (1438); the 0/1 check (1441-1442) is dead on the bool-promoted value; false branch sets disabled/1/"default" and returns success (1444-1447). |
| 75 | S162 `1449-1478` | OK — non-numeric or ≤0 speed → `invalid speed` (1452-1462); missing bezier → `no such bezier` (1466-1467); `setConfigForNode` (1469) precedes nonempty-style `styleValidInConfigVar` validation (1471-1475); error returned from there. |
| 77 | S162 `287-309` | OK — handleBezier (287-297) and handleAnimation (299-309) callbacks map a returned optional string to `CParseResult::setError`; scope hedge accurate. |
| 81 | S158 `947-964,2018`; S177 `18-26,40-48` | OK — 2018 registers `animations`→`animationsRequest` verbatim; 947 `[[`, node loop 948-961 with keys name/overridden/bezier/enabled/speed/style (951-956), `enabled` from `internalEnabled ? "true" : "false"` (959), speed `{:.2f}` (955); S177 18-26/40-48 define the internal fields and pValues. |
| 83 | S158 `951-976` | OK — bezier keys name/X0/Y0/X1/Y1 (969-973), controlPoints[1]/[2] (975), all `{:.2f}`; `escapeJSONStrings` on node bezier/style (959-960) and bezier names (975); node `name` (ac.first) is not escaped and the doc does not claim it is. |
| 85 | S158 `948-976`; S176 `14-60` | OK — node loop over `getAnimationConfig()` (948, = full 35-node map), bezier loop over `getAllBeziers()` (966); no `parent` key in either object shape. |
| 89-94 | (receipt claims) | OK — sha256 of `tools/mado-anims.py` = `2beda3f7…cab7d`, of `count-v2.py` = `4ed70b54…6428` (recomputed); 2b3487f7 lands exactly that file (commit message names seat ExecAnimToolA); receipt says `measured_at=2026-10-23T09:36:14Z`, rev/tool/counter hashes match, `PRED-C1-r26-v2 cases_pass=41/41 verdict=TARGET_MET`, `exit=0`; 41 = BASE + C00-C19 (20 APPEND) + C20-C29 (10 EDIT) + C30-C39 (10 SYNTH). |
| 96-98 | (uncited, flagged "not measured by the counter") | Supported as stated — counter's own header says "nested, headless, session-isolated instance" and `node_set`/`bez_set` (count-v2.py:256-261) compare field sets, matching "(the counter compares sets)"; tool output order is fixed (nodes in NODE_TABLE order, beziers in insertion order, `emit()` at tools/mado-anims.py). The `$VAR`-from-environment clause is corroborated by fetched hyprlang source (`SrcHyprlangExpr.bin:544-548`, `envVariables` seeded from `environ`); `{{…}}` and the `std::stof`-overflow abort remain data-seat report claims, which is exactly how the doc labels them. (The handlers' `std::stof` at ConfigManager.cpp:1398/1453 is indeed unguarded, consistent with an uncaught exception, but the abort behavior itself is outside the fetched sources.) |
| 100 (INF) | S162 `1469-1478,287-309`; S158 `948-976` | OK — setConfigForNode-before-style-check shows no rollback at that point; 287-309 stops at setError; 948/966 iterate unordered containers with no sort. Hedges are accurate. |

## Tool-behaviour cross-check (doc ¶ "Local tool and counter")

- `tools/mado-anims.py` `emit()` prints `[nodes, beziers]` with the six node fields and five bezier fields; speed/bezier coordinates via `round2` ({:.2f}-equivalent); initial node state mirrors hyprutils createNode (`overridden=false, enabled=-1, speed=0`) and `enabled` is emitted truthily (`enabled != 0`), matching HyprCtl's serialization of `-1`.
- "From config bytes only": `main` → `parse_file` (reads bytes, decodes, no socket/subprocess/compositor call) → `json.dumps(emit(st))`, exit 0.
- Handler transcription matches the cited C++: off-path writes disabled/1/"default" and returns; invalid speed / unknown bezier paths write nothing; the style write happens before the style check, matching ConfigManager.cpp:1469-1476.

## Findings

None. No false or unsupported bracketed statement found; all 14 cited ranges exist and say what their sentences say (several are line-exact, e.g. 612-613 and 2018).

## Residual risk / notes (non-defects)

1. Fetch-provenance: `SrcAnimConfig.bin` is byte-identical to `SrcAnimConfig-legacy-impl.bin` (both the 2184-line ConfigManager.cpp). The S177 target (`src/animation/AnimationConfig.cpp` @ v0.14.2) is stored only as `SrcAnimTreeHyprutils.bin`. Resolving citations by fetch filename alone would read the wrong file; the doc itself is unaffected because it cites source paths.
2. Doc line 65 paraphrase "pValues points at the parent's values" strictly means `parentRef->pValues` (the parent's effective values pointer); identical values-object semantics, not a defect.
3. The limits paragraph (doc 96-98) is report-sourced and explicitly marked unmeasured; `{{…}}` handling and the `std::stof` abort remain unverified by any artifact in the lane (the tool deliberately raises on float32 overflow instead of reproducing an abort).
4. Verification gaps: counters were not re-run (read-only residual call; existing receipt read as-is, its internal hashes re-verified); hyprutils v0.14.2 tag identity is asserted by the tool docstring/receipt corpus and not independently confirmed against the upstream tag.
