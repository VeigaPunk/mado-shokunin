# ReopenS155 — mado round 24 wave 2 (falsify)

Reviewer: MadoR24.ReopenS155 · 2026-10-23 · Scope: SOURCES row S155 only, plus claim rows A3–A6 citing it.
Lane: /home/vgpnk/Projects/shokunin/mado-shokunin @ 39c596307333b8ca0a1e42b3f3b9a748bb8b208b (round base 8e5d93691e2f7baa3d4a0a61c9428e5acb5d2122).
Tool installs: none (used preexisting curl/git/python3/coreutils; nothing to record per the 2026-10-19 tooling directive).

## 1. Source-row integrity (S155)

Row (corpus/SOURCES.md:167): `Hyprland v0.56.2 WindowRuleApplicator.cpp` — URL pinned to raw.githubusercontent.com/hyprwm/Hyprland at 40-hex commit `efb50993780079460b0cbed1363e2166a2de1d9f`, path `src/desktop/rule/windowRule/WindowRuleApplicator.cpp`; grade A; status `mined`; opened `2026-10-23`; recorded `sha256:fec33f9a0bc279ffc94ca27a6e9843964840d6269bc28d330d566e05fed3307b`, `27092 B`; used-by `corpus/knowledge/rule-attribution-r24.md`; cited ranges 81-84, 118-124, 151-158, 234-235, 378-509, 547-579.

Checks run (all commands executed this session):

| Check | Command | Result |
|---|---|---|
| Fresh fetch of pinned URL | `curl -fsSL` raw URL → /fast/scratch/hyaku/mado-r24/w2/s155/WindowRuleApplicator.cpp | HTTP 200; sha256 `fec33f9a0bc279ffc94ca27a6e9843964840d6269bc28d330d566e05fed3307b`; 27092 B |
| vs committed fetch bytes | `cmp` fresh fetch vs `.ufo/waves/round-24/fetch/S155.bin`; `sha256sum`/`wc -c` of S155.bin | byte-identical (`BYTES-IDENTICAL`); S155.bin sha256 `fec33f9a…3307b`, 27092 B |
| vs row's recorded values | read SOURCES.md:167 raw | sha256 and 27092 B match exactly |
| vs local clone blob | `git -C /fast/scratch/hyaku/mado-r24/src/Hyprland-v0.56.2 show efb5099…:src/desktop/rule/windowRule/WindowRuleApplicator.cpp \| sha256sum` | same `fec33f9a…3307b` |
| Pin resolves | `git cat-file -t efb5099…` → `commit`; `git log -1` → `[gha] Nix: update inputs`; `git describe --tags --exact-match` → `v0.56.2` | pinned commit exists and is exactly tag v0.56.2 |
| Host cross-check (read-only verb) | `hyprctl version` | "Hyprland 0.56.2 built from branch v0.56.2 at commit efb50993780079460b0cbed1363e2166a2de1d9f clean" — the running compositor is built from this exact pin |

Four independent byte sources agree: fresh fetch = committed fetch = row record = clone blob at pin. Pin resolves and is the v0.56.2 release commit. Row metadata (mined/opened/used-by/grade) present and consistent.

**VERDICT (row S155): holds**

## 2. Claim rows A3–A6 (corpus/knowledge/rule-attribution-r24.md:37-40)

Method: quotes checked for occurrence under the frozen predicate's own convention — whitespace-collapsed verbatim (`re.sub(r'\s+', ' ', s).strip()` on both sides, the `collapse()` in `.ufo/waves/round-24/c1/count.py` v2). Line numbers below refer to the pinned file (1-based, as printed by `nl -ba`). All four quote locations fall inside the row's cited ranges.

### A3 — "The static pass calls `matches` before applying static and dynamic effects for matching non-exec rules."
- Quote: `if (!wr->matches(m_window.lock(), true)) continue; if (wr->isExecRule()) { m_execRules.emplace_back(wr); continue; } applyStaticRule(wr); const auto RES = applyDynamicRule(wr);` (16 words ≤ 25; contains topic word `matches`).
- (a) Verbatim: YES — lines 498–507 of readStaticRules (cited range 378-509). Source has `const auto RES  =` (double space, line 507); predicate's whitespace-collapse covers this by design; raw byte-exact match would fail, which is expected under the frozen convention, not a defect.
- (b) TRUE of quoted bytes: YES. `matches` gate at 498 `continue`s non-matching rules; matching exec rules diverted to `m_execRules` at 501-504; for matching non-exec rules, `applyStaticRule(wr)` (506, static effects → `static_`) and `applyDynamicRule(wr)` (507, dynamic effects) run after the gate. Ordering claim exact. No overreach: claim's scope "for matching non-exec rules" matches this loop precisely; it does not deny the later exec-rule application at 517-519, which the quote doesn't cover and the claim doesn't contradict.
- (c) Rule attribution: YES (borderline-acceptable). This loop is the rule→effect application path gated by each rule's own matcher — an effect present on the window traces back to rules whose `matches` returned true, i.e., which rule produced the effect is determined here. Most mechanical of the four rows; judged attribution-relevant rather than generic traversal because per-rule gating + per-rule application is the attribution pathway itself.
- **VERDICT A3: holds**

### A4 — "The static read function loops over `ruleEngine()->rules()` after clearing prior static state."
- Quote: `bool CWindowRuleApplicator::readStaticRules(bool preRead) { if (!m_window) return false; static_ = {}; m_execRules.clear(); bool tagsWereChanged = false; for (const auto& r : ruleEngine()->rules()) {` (23 words ≤ 25; contains topic word `rules`).
- (a) Verbatim: YES — lines 483–492 (cited range 378-509), whitespace-collapse only.
- (b) TRUE of quoted bytes: YES. `readStaticRules` checks `m_window` (484-485), then `static_ = {};` at 487 clears prior static state before the `for (const auto& r : ruleEngine()->rules())` loop at 492. Ordering exactly as claimed. The claim does not mention the additional `m_execRules.clear()` (489); omitting it is not overreach — the claim is silent on exec rules, not wrong about static state.
- (c) Rule attribution: YES (defensible). Re-deriving the effect set from the engine's current rule register after a reset is what keeps the rule→effect mapping tracking currently-registered rules; stale-rule effects are wiped each read. Weakest attribution link of the four (state-reset mechanics), but it describes deriving the applied set from the rule list, which underpins "which rules are in force".
- **VERDICT A4: holds**

### A5 — "The handler passes `PRIORITY_WINDOW_RULE` as the second argument when setting allows-input."
- Quote: `m_allowsInput.first.set(std::get<bool>(value), Types::PRIORITY_WINDOW_RULE);` (2 words; ≤ 25).
- (a) Verbatim: YES — line 234 exactly (cited range 234-235), single line so byte-exact.
- (b) TRUE of quoted bytes: YES. `case WINDOW_RULE_EFFECT_ALLOWS_INPUT:` (233) → `m_allowsInput.first.set(std::get<bool>(value), Types::PRIORITY_WINDOW_RULE);` (234): second argument of `set` is `Types::PRIORITY_WINDOW_RULE`, value is the bool allows-input. "The handler" loosely names the ALLOWS_INPUT switch case in applyDynamicRule (not a named handler function) — minor wording, not false.
- (c) Rule attribution: YES — strong. The priority slot is provenance: the stored value records that a window rule set it (priority arbitration against other setters), i.e., what exposes rule identity at read time.
- Counter note (predicate-level, disclosed by the round): the quote contains no rule-topic word (`TOPIC_RE` of count.py v2 does not match — `RULE` inside `PRIORITY_WINDOW_RULE` has no word boundary; confirmed by my own run of the frozen regex). The round's own receipt `.ufo/waves/round-24/evidence/c1-after-cf86f9e0.txt` already records `A5 S155 FAIL_ROW quote-off-topic` (likewise A7/A8), and TARGET_MET stood on the other rows (23/26, 14 distinct sources). The row text itself is true and attribution-relevant; it merely earns no PASS_ROW under the frozen predicate. No concealment; no round-level defect.
- **VERDICT A5: holds** (substance a/b/c all pass; flagged as predicate-FAIL_ROW by the frozen counter, disclosed in the receipt)

### A6 — "The alpha field stores `rule->getPropertiesMask()` in its companion mask slot."
- Quote: `m_alpha.second = rule->getPropertiesMask();` (3 words; ≤ 25; contains topic word `rule`).
- (a) Verbatim: YES — line 156 (cited range 151-158), single line so byte-exact.
- (b) TRUE of quoted bytes: YES. Pair structure is established within the same cited range: `m_alpha.first = Types::COverridableVar(opacity.alpha, Types::PRIORITY_WINDOW_RULE);` (153) and `m_alpha.second = rule->getPropertiesMask();` (156) — `.second` is the companion mask slot paired with the overridable value in `.first`. "Stores" is accurate (alpha's mask uses `=`, unlike some siblings' `|=`). No overreach: claim does not assert COverridableVar tie semantics — and the row's own caveat ("does not establish COverridableVar tie semantics or host behavior") already excludes that.
- (c) Rule attribution: YES — strong. The mask records which rule property backs the alpha value, linking a live window property slot to the rule that set it; the same masks drive change-driven re-evaluation (`!(WR->getPropertiesMask() & props)` gate at 563), i.e., which rule's effect must be refreshed.
- **VERDICT A6: holds**

## 3. Findings by severity

No defects found in scope. Notes (non-defects):
1. [info] A5 is a disclosed `FAIL_ROW quote-off-topic` under frozen predicate v2 (receipt c1-after-cf86f9e0.txt). The corpus row is true and attribution-relevant; the topic-word clause is a counting predicate, and the round's TARGET_MET (23/26, ≥3 sources) does not depend on A5. Honesty of the 23/26 accounting confirmed against the receipt.
2. [info] A3/A4 quotes match only under the frozen predicate's whitespace-collapse (e.g., `RES  =` double space at line 507; multi-line joins), matching the documented convention in count.py v2; raw byte-exact matching is not the standard the round froze.
3. [info] A3 (and to a lesser degree A4) are the most mechanical of the attribution rows; judged in-scope for the note's theme because the per-rule `matches`-gated application path is the mechanism by which effects trace to rules.

## 4. Residual risk and verification gaps

- Host behavior not exercised: `hyprctl version` confirms the running build is the pinned commit, but no live-rule experiment (e.g., `hyprctl keyword windowrule` + `getprop`) was run — out of scope (host is read-only; write verbs forbidden). Claims A3–A6 are code-reading claims and were judged as such.
- `git ls-remote` against github.com was not used; pin resolution was proven via the local clone (`cat-file`/`describe --exact-match`) plus the identical blob hash, and the fresh raw.githubusercontent.com fetch itself resolving at that commit is independent network confirmation.
- Only S155 and rows A3–A6 were re-opened; S156/S157/S158 rows and their claims (A7–A11) are other seats' scope. A7/A8 share A5's off-topic-quote predicate status per the receipt and were not re-judged here.

**Overall: VERDICT: holds** — S155's pin, hash, size, and fetch provenance all verify against four independent byte sources; all four quote occurrences are verbatim under the frozen convention; claims A3, A4, A6 are true without overreach; A5 is true and attribution-relevant but correctly counted as FAIL_ROW (quote-off-topic) by the frozen counter, as the round's own receipt discloses.
