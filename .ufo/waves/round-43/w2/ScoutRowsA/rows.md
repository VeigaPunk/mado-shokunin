# ScoutRowsA - rows S290 and S291, every cell re-opened 2026-10-26

Attacks: corpus/SOURCES.md:239 (S290), :240 (S291); corpus/lessons/round-43.md GATE lines 34 and 36.
Evidence in this seat dir: live-RegexMatchEngine.cpp, live-DefaultFloatingAlgorithm.cpp (fresh curl of the row URLs today),
upstream-Rule.cpp-lines52,98.txt, upstream-WindowRule.cpp-395-396.txt, upstream-Window.cpp-2398-2410.txt (from a `git clone --branch v0.56.2`, HEAD efb50993780079460b0cbed1363e2166a2de1d9f).

## Source identity (both rows)
- `curl` of each URL today: sha256 8ca65533...a3a282 (470 B) and f05f2561...632e91 (10359 B). Both equal fetch-sha256.txt lines and the row cells; `cmp` against the fetch/ receipts: byte-identical.
- `git ls-remote https://github.com/hyprwm/Hyprland refs/tags/v0.56.2` -> efb50993780079460b0cbed1363e2166a2de1d9f (tag commit as the rows say). `hyprctl version` on host: 0.56.2 at commit efb50993... (host runs the pinned build).

## S290 (SOURCES.md:239) - cell by cell (11 cells, split count verified)
| cell | verdict | evidence |
|---|---|---|
| id S290 | OK | next after S289, gap-free |
| source (title + URL) | OK | URL resolves, content as pinned; separator " - " matches S277-S289 style |
| kind `code` | OK | C++ source |
| tier `A` | OK | primary, host-pinned commit |
| scope | NEEDS-NARROWING (minor) | "The test a host `match:class` regex is put through" - the file alone does not show that `class` uses this engine; that link is Rule.cpp:52 `{RULE_PROP_CLASS, RULE_MATCH_ENGINE_REGEX}`, Rule.cpp:98 `makeUnique<CRegexMatchEngine>(s)`, WindowRule.cpp:395-396 `engine->match(w->m_class)` - none pinned as a row or in the anchor. TRUE upstream today, but unpinned (a reader cannot verify it from S290/S155). |
| anchor `:6-13 constructor, :15-17 match` | OK | grep -n: 6 `CRegexMatchEngine::CRegexMatchEngine(...) {`, 13 `}`; 15 `bool ...::match(...) {`, 17 `}`. "470 B", sha, tag, commit, receipt path all verified. |
| teaches | TRUE in each clause; one provenance defect | RE2::FullMatch whole-string: line 16. `negative:` prefix stripped via substr(9) ("negative:" = 9 chars) and `!= m_negative` inverts: lines 7-9,16 (m_negative default false, RegexMatchEngine.hpp:21). "the host rule's `^` and `$` are redundant while its unescaped dots still match any character": true of RE2 (FullMatch anchors both ends; `.` is any char but \n) but the host rule text `^(org.omarchy.gkeep)$` is S295 (host-gkeep.conf:2-4, sha 3726e488... equals live ~/.config/hypr/gkeep.conf today), not S290; the S290 cell mixes two sources. |
| status `mined` | OK | |
| opened `2026-10-26` | OK | valid date, today |
| recheck `on-release` | OK | cadence used by S155/S158/S278-S288 for release-pinned code |
| used-by | OK | `corpus/knowledge/hyprland-gkeep-geometry-r43.md` exists; cites S290 (lines 4, 34) |

Lesson GATE S290 (round-43.md:34): receipt path exists, sha256 equals the receipt (8ca65533...3a282), quote `return re2::RE2::FullMatch(other, *m_regex) != m_negative;` = 7 tokens, `grep -cF` on the receipt = 1 (line 16). EXACT.

### Exact fixes proposed (S290)
1. scope: replace with `The test a window-rule regex string is put through, and the `negative:` prefix` (drops the host-class claim the file does not show) - OR keep scope and add to anchor `; the class->regex binding is Rule.cpp:52,98 and WindowRule.cpp:395-396 at the same commit (not pinned)`.
2. teaches: replace `so the host rule's `^` and `$` are redundant while its unescaped dots still match any character` with `so a leading `^` and trailing `$` are redundant and an unescaped `.` matches any character (the host rule text is S295)`.

## S291 (SOURCES.md:240) - cell by cell
| cell | verdict | evidence |
|---|---|---|
| id | OK | |
| source | OVERSTATED TITLE | "who consumes a size rule" - the same `static_.size` is also consumed on the TILED path: Window.cpp:2402-2410 (`calculateExpression(*m_ruleApplicator->static_.size)` -> `setPseudoSize`, else-branch of `if (m_isFloating)`), and WindowRuleApplicator.cpp:178,207 evaluates expressions too. S291 is the floating consumer only. |
| kind/tier | OK | code / A |
| scope "first-map branch that evaluates the stored size expression and places the box" | OK | line 49 `if (target->window() && target->window()->m_firstMap) {` ... 56 evaluation ... 96/102 placement |
| anchor | OK | grep -n: :16 `constexpr const Vector2D DEFAULT_SIZE = {640, 400};`; :19-45 newTarget head through the desired-geometry if/else (26 `if (!DESIRED_GEOM)`, 36 default box, 41-44 desired box); :49-66 first-map, size warp 53, size eval 55-66, position warp 64; :79-84 center block; :90-103 `if (!posOverridden...)` through the final else/`}`. 10359 B/sha/tag/commit/receipt verified. Unclaimed lines (68-77 position rule, 85-88 lastFloatingSize) are honestly not cited. |
| teaches | PARTLY OVERSTATED | TRUE: first-map only (49); computes `static_.size` and overwrites `windowGeometry.w/.h` (56,60-61). OVERSTATED: (a) "then centers that box" is conditional - lines 79-84 run only if `static_.center.value_or(false)`, lines 90-91 only if `!posOverridden && (!DESIRED_GEOM \|\| !DESIRED_GEOM->pos)`; (b) the overwrite happens only if the expression parses (57-58 log an error and leave the client's size); (c) "outranks the size the client asked for" stops at the box this function builds - target->setPositionGlobal (:96,:102) is followed by the clamp path in WindowTarget.cpp:228-231 (rule min/max), which is S293, not S291. |
| status/opened/recheck | OK | mined / 2026-10-26 / on-release |
| used-by | OK | entry exists, cites S291 (lines 6, 42) |

Lesson GATE S291 (round-43.md:36): sha256 f05f2561...632e91 equals receipt; quote `const auto COMPUTED = WINDOW->calculateExpression(*WINDOW->m_ruleApplicator->static_.size);` (7 tokens) `grep -cF` = 1 (line 56). EXACT.
Entry cross-check: hyprland-gkeep-geometry-r43.md:42 ("evaluates that expression only inside its first-map branch ... (DefaultFloatingAlgorithm.cpp:56)") is correct for the algorithm and carries the right scope; the tiled consumer at Window.cpp:2403 does not contradict it.

### Exact fixes proposed (S291)
1. source title: `... default floating algorithm - who consumes a size rule on the floating path - <URL>`.
2. teaches: replace with `On a window's first map this algorithm computes the stored size expression and, if it parses, overwrites the box width and height; the box is centered only when the center rule is set or the client gave no position, so a size rule replaces the size the client asked for in this box (later clamps are S293)`.

## Findings summary
- No broken cell: hashes, byte counts, tag/commit, line anchors, status/opened/recheck, used-by, and both GATE lines are exact (all re-run today).
- Defects are wording-level: S290 scope/teaches carry a claim sourced elsewhere (class->regex binding unpinned; host regex text from S295); S291 title says "who consumes a size rule" though a tiled consumer exists (Window.cpp:2403), and its teaches drops three conditions (center, parse success, downstream clamp).
- Not attacked: S292-S297, S155, S158 (outside my named target). No tools installed. Scratch cleaned.
