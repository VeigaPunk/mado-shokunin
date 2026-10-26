# ScoutRowsC - rows S294, S155, S158 re-opened 2026-10-26 (data commit 1959770657f1f8665097c1aed4be6c1cbb07139f)

Method: curl of each row URL today into scratch (deleted after), sha256 against `.ufo/waves/round-43/receipts/fetch-sha256.txt`
and the pinned `.ufo/waves/round-43/fetch/` receipts; `git show 1959770:corpus/SOURCES.md` vs `git show a35cfdfcdeb3bd42d1a2cd960faf22ceac1bef3f:corpus/SOURCES.md`
for the held-row diff; `git ls-remote https://github.com/hyprwm/Hyprland refs/tags/v0.56.2` -> `efb50993780079460b0cbed1363e2166a2de1d9f`.
Column order of the registry (SOURCES.md:11): id | source | kind | tier | scope | anchor | teaches | status | opened | recheck | used-by.

## Fetch compare (all three EXACT)
| row | live curl sha256 | pinned (fetch-sha256.txt) | row anchor | bytes (live / row) |
|---|---|---|---|---|
| S294 | 649f1a8d...a207d | 649f1a8d...a207d | same | 1576 / 1576 |
| S155 | fec33f9a...3307b | fec33f9a...3307b | same | 27092 / 27092 |
| S158 | 798b7c6c...91fa | 798b7c6c...91fa | same | 97582 / 97582 |
Tag v0.56.2 resolves to efb5099... (lightweight tag, no peeled entry) - the `@ tag v0.56.2 commit efb50993...` wording holds.

## S294 (new row, SOURCES.md:243)
| cell | verdict | evidence |
|---|---|---|
| id | OK | exactly one `^| S294 ` row now; base a35cfdf has none (git grep S294 at base: no hit in corpus/quality/tools/PROVINCE/SKILL). Old S294 hits in round-32/40/41 wave files are staging-package ids, not registry rows. |
| source (title+URL) | OK | URL returns 200; path `src/desktop/view/types/GeometricMovableAnimated.cpp`; class is `CGeometricMovableAnimated` (line 8). |
| kind=code, tier=A | OK | upstream source at a pinned commit, same as S290-S293/S155/S158. |
| scope | OK | file defines `position/size/geometricBox(eGeometricValueType)` switching `GEOMETRIC_GOAL` / `GEOMETRIC_CURRENT`. |
| anchor lines | OK | :8-15 `position`, :17-24 `size`, :26-33 `geometricBox`, :39-41 `resize`, :53-59 `positionAnimation`+`sizeAnimation` (the two handles); file is 59 lines, 1576 B. Omits :35-37 move, :43-46 setBox, :48-51 finishAnimation (warp) - not claimed, not needed. |
| teaches | OK on the code half, INFERENCE on the tail | "one of two values, goal or current" is directly in :19-20. "...and can differ from what is on screen" is not shown by this file (it never says what is drawn); it is carried by the entry's INF at hyprland-gkeep-geometry-r43.md §3 and the w1 ExecGoalVsValue finding. Suggested exact text (optional): `A size read is one of two values, the animation's goal (m_realSize->goal()) or its current value (m_realSize->value()), so a reader that asks for GEOMETRIC_GOAL reports the target being approached, not the value the animation holds now` |
| status=mined | OK | opened and read. |
| opened=2026-10-26 | OK | today; consistent with lesson Access date. |
| recheck=on-release | OK | same cadence token as held upstream rows S155/S158. |
| used-by | OK | `corpus/knowledge/hyprland-gkeep-geometry-r43.md` exists and cites S294 at §3 (:52 of the entry). |
| lesson GATE (round-43.md:39) | OK | receipt sha matches the receipt file; quote `case IGeometric::GEOMETRIC_GOAL: return m_realSize->goal();` is 1 contiguous occurrence, at line 19 (the entry cites :19) - unique (the goal() text on :10,:28 differs); 4 whitespace tokens, well under 25 words. |

## S155 (held, SOURCES.md:167)
Diff base->data on the row: ONLY cell 11 changed (`rule-attribution-r24.md` -> `rule-attribution-r24.md, hyprland-gkeep-geometry-r43.md`); cells 1-10 byte-identical (diff of the `|`-split rows prints only line 12). Matches the lesson's "one item appended".
| cell | verdict | evidence |
|---|---|---|
| source/URL/sha/bytes | OK | live sha = row sha = pin; 27092 B. |
| kind/tier | OK | code / A. |
| scope "matching, static and dynamic application, property masks, reset, setter priority" | OK with one nit | applyDynamicRule :81, applyStaticRule :378, readStaticRules :483 with `wr->matches(...)` :498, `.second |= rule->getPropertiesMask()` :119/:123, `PRIORITY_WINDOW_RULE` :118/:122. NIT: `resetProps`/`resetRuleProp` bodies (:18-79) are not in the anchor; "reset" is evidenced only by the call at :552 (inside :547-579) - no fix required, the word is supported. |
| anchor 81-84, 118-124, 151-158, 234-235, 378-509, 547-579 | OK | 81-84 = applyDynamicRule opening + effect loop; 118-124 rounding/roundingPower set with priority + mask; 151-158 opacity COverridableVar + masks; 234-235 allowsInput; 378-509 = applyStaticRule (378-480) + readStaticRules start (483-509, ends after `RES` line; closer :510 outside); 547-579 = propertiesChanged up to the loop closer :579 (function ends :590). The new use `static_.size = expr;` is :426, inside 378-509; `Math::SExpressionVec2` :423, `static_.size.reset()` :425. |
| teaches | OK (not wrong; stale vs new use) | still true; "does not establish COverridableVar tie semantics or host behavior" still true - nothing in this round contradicts it. The new used-by fact (static size kept as an unevaluated expression, :420-428) is not named in teaches, but scope says "static application" and the anchor covers it; no fix required (cells 1-10 are frozen by the lesson). Optional text if the L1 wants it: append `; stores a size rule unevaluated as static_.size = expr (:426)`. |
| status/opened/recheck | OK | mined / 2026-10-23 / on-release, untouched. |
| used-by | OK | only citers of S155 in corpus/knowledge are rule-attribution-r24.md and hyprland-gkeep-geometry-r43.md (grep -rlE '\bS155\b'); entry cites S155 at §2 (:40). |
| lesson GATE (round-43.md:35) | OK | sha matches; quote `static_.size = expr;` = 1 occurrence, line 426 (entry cites :426). Short (3 words) but unique in the file. |

## S158 (held, SOURCES.md:170)
Diff base->data: ONLY cell 11 changed (appended `corpus/knowledge/hyprland-gkeep-geometry-r43.md`); cells 1-10 identical.
| cell | verdict | evidence |
|---|---|---|
| source/URL/sha/bytes | OK | live sha = row sha = pin; 97582 B. |
| kind/tier | OK | code / A. |
| scope | OK | `clients` JSON `getTagsData` :346, `getprop` :1463, `layersRequest` :647, `workspaceRulesRequest` :613, registrations :2003+. |
| anchor 346-484, 613-630, 647-723, 1463-1645, 2003-2044 | OK, three one-line closer nits (pre-existing, round-24) | 346-484 = getTagsData..clientsRequest body, ends at `return result;` :484, closing `}` is :485; 613-630 same shape (`}` :631); 647-723 ends on `}` :723 exact; 1463-1645 exact (`}` :1645); 2003-2044 ends at `startHyprCtlSocket();` :2044, `}` :2045. No fix needed: ranges cover all content lines; edits to anchor cells are outside the lesson's allowed in-place changes. The new use (getWindowData JSON size args :426-428 and text :447-448) is inside 346-484. |
| teaches | OK | "client tag-state and property-value reads plus a workspace-rule list; no dedicated window/layer attribution verb": registrations at :2003-2044 include clients, layers, workspacerules, getprop, getoption, binds, animations, no window/layer rule listing verb (grep for rules verb: only `"rules": "{}"` at :788 in devices). Still true. Not mentioned: the `size` fields are the GOAL value (:426-428, :447-448) - scope/teaches do not claim otherwise, so not wrong. |
| status/opened/recheck | OK | mined / 2026-10-23 / on-release, untouched. |
| used-by | OK for what it lists; INCOMPLETE pre-existing | all six listed entries exist and cite S158 (grep counts: r24 yes, animation-table-r26 yes, workspace-rules-r27 yes, request-socket-live-bound-r8 yes, getoption-native-forms-r40 yes, geometry-r43 yes). Not listed but citing S158: `corpus/knowledge/hyprctl-verification-layer.md`, `hyprctl-flags-r28.md`, `request-limits-upstream-r31.md` (grep -rlE '\bS158\b' corpus/knowledge). Predates this round; the used-by cell is a mutable cell, so exact fix if the L1 wants it: append `, corpus/knowledge/hyprctl-verification-layer.md, corpus/knowledge/hyprctl-flags-r28.md, corpus/knowledge/request-limits-upstream-r31.md`. |
| lesson GATE (round-43.md:40) | **MISS as a literal string; OK whitespace-normalised** | sha matches. The quote is not a contiguous substring of the receipt: it spans HyprCtl.cpp:428-429 (line 428 ends `WORKSPACE_INVALID,` newline + 12 spaces, 429 starts `escapeJSONStrings(!w->m_workspace ...`). Literal `str.count(q)` = 0; after `re.sub(r'\s+',' ',s)` count = 1. Same class as S293's quote. A grep-based/literal GATE verifier fails it. Exact fix (single-line, 6 whitespace-separated tokens, unique, line 428 only; verified literal count 1): replace the quote with `sc<int>(w->size(Desktop::View::IGeometric::GEOMETRIC_GOAL).y), w->m_workspace ? w->workspaceID() : WORKSPACE_INVALID,` - literal count 1 at line 428 (verified: line 428 is exactly that text plus leading spaces). The entry's citation `(Hyprland-HyprCtl.cpp:428-429)` is right for the longer quote and can stay or become `:428`. |

## Summary
- All three upstream bytes re-fetched today equal the pins (sha256 and byte counts) and the tag resolves.
- Cell defects: (1) S158 GATE quote spans a line break (literal-match fails) - fix text above; (2) S294 teaches tail "can differ from what is on screen" is an inference not in the file - optional reword above.
- Nits, no fix required: S155 resetProps body not in anchor; S158 three anchor ranges stop one line before the closer; S158 used-by omits three pre-existing citers.
- Not re-reported: any w1 finding.
