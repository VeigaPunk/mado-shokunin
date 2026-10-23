# Re-open S157 — reviewer seat ReopenS157 (wave 2, round 24, falsify)

Seat: MadoR24.ReopenS157. Target: SOURCES row S157 (`corpus/SOURCES.md:169`) and claim row A9
(`corpus/knowledge/rule-attribution-r24.md:43`), both read at lane tip `39c596307333b8ca0a1e42b3f3b9a748bb8b208b`.
All fetches and clone reads done fresh by this seat on 2026-10-23; no wave-1 receipt trusted without redo.
No tool installs (stock curl/git/awk/tr only).

## 1. Pin fidelity — holds

Row S157 pins:
`https://raw.githubusercontent.com/hyprwm/Hyprland/efb50993780079460b0cbed1363e2166a2de1d9f/src/desktop/rule/windowRule/WindowRule.cpp`
with `@ efb50993780079460b0cbed1363e2166a2de1d9f, sha256:7034c3325fee476cb501266af67999534ca36cf2841d83c9940db96d116d1f78, 19588 B`.

Measured now, four ways:

| Side | sha256 | bytes |
|---|---|---|
| Row cell (`corpus/SOURCES.md:169`) | `7034c3325fee476cb501266af67999534ca36cf2841d83c9940db96d116d1f78` | 19588 |
| Fresh `curl` of the pinned URL (this seat, 2026-10-23) | `7034c3325fee476cb501266af67999534ca36cf2841d83c9940db96d116d1f78` | 19588 |
| `.ufo/waves/round-24/fetch/S157.bin` | `7034c3325fee476cb501266af67999534ca36cf2841d83c9940db96d116d1f78` | 19588 |
| `git show <pin>:src/desktop/rule/windowRule/WindowRule.cpp` in the local clone | `7034c3325fee476cb501266af67999534ca36cf2841d83c9940db96d116d1f78` | — |

Fresh fetch vs `S157.bin`: `cmp` clean (byte-identical). Row status `mined`, opened `2026-10-23`, recheck
`on-release`, used-by `corpus/knowledge/rule-attribution-r24.md` — all present in the row as the C1 v2
predicate requires.

## 2. Pin resolves — holds

- Local clone `/fast/scratch/hyaku/mado-r24/src/Hyprland-v0.56.2`: `git cat-file -t efb5099…` → `commit`;
  `git describe --tags --exact-match efb5099…` → `v0.56.2`.
- Upstream: `git ls-remote https://github.com/hyprwm/Hyprland refs/tags/v0.56.2` →
  `efb50993780079460b0cbed1363e2166a2de1d9f refs/tags/v0.56.2`.

The "Hyprland v0.56.2" title and the 40-hex pin are the same commit; the blob at that commit hashes to the
recorded sha256.

## 3. Claim row A9 — per-criterion verdicts

Row: `| A9 | The `RULE_PROP_TAG` matcher tests the rule applicator tag keeper and rejects a failed engine
match. | S157 | "case RULE_PROP_TAG: if (!engine->match(w->m_ruleApplicator->m_tagKeeper)) return false;
break;" |`. S157 is cited by A9 only (table scan of the note; used-by cell agrees).

### (a) Quote occurs verbatim — holds

Whitespace-collapsed occurrence count of the exact quote string over the whole pinned file: **1** (same
method as the C1 counter; ≤25 words; contains rule-topic word). The quote is physically lines 407-410;
`RULE_PROP_TAG` occurs exactly once in the file, so there is no second-site misattribution risk.

### (b) Claim TRUE of the quoted bytes, no overreach — holds

Verified in the pinned bytes and the same commit's tree:

- `bool CWindowRule::matches(PHLWINDOW w, bool allowEvalLookup)` at :376 with gate `if (!canMatch())
  return false;` (:377-378), then `for (const auto& [prop, engine] : m_matchEngines)` (:380) — the case at
  :407-410 is exactly the quoted bytes.
- "tests the rule applicator tag keeper": `w->m_ruleApplicator->m_tagKeeper` — `m_tagKeeper` is a
  `CTagKeeper` member of the window's rule applicator (`src/desktop/rule/windowRule/WindowRuleApplicator.hpp:141`);
  `engine->match` resolves to `IMatchEngine::match(const CTagKeeper&)`
  (`src/desktop/rule/matchEngine/MatchEngine.hpp:23`, `MatchEngine.cpp:21`), implemented as
  `return keeper.isTagged(m_tag);` (`src/desktop/rule/matchEngine/TagMatchEngine.cpp:11-12`) — a genuine
  read-only predicate over the keeper, so "tests" is literal.
- "rejects a failed engine match": `if (!engine->match(...)) return false;` inside a bool `matches()`;
  callers treat false as rejection/skip: `if (!wr->matches(m_window.lock(), true))` at
  `WindowRuleApplicator.cpp:498,536,566` (same commit).

Every clause of the claim maps to quoted or directly supporting bytes; the claim asserts nothing further
(e.g. no tag-provenance claim) that would overreach.

### (c) Rule-attribution content, not generic mechanics — holds

The row identifies *what exposes rule-produced tag state*: the per-window applicator's tag keeper, and the
match property (`RULE_PROP_TAG`) that reads it. That is the exact component the note's attribution route is
built on — the note's table cites (A9, A10) for "the tag set the applicator's tag keeper holds", and A10
shows hyprctl `clients` exporting `getTags()` of that same keeper. It is not a generic mechanics line (not
ordering/evaluation-loop boilerplate). Honest scoping: A9 does not and does not claim to identify which rule
wrote a given tag; the note lists that gap itself ("provenance when two rules add the same tag" not shown).

## 4. Findings

1. **Minor — anchor span one line short for A9.** The row's anchor cell says `…:407-409`, but the A9
   quote's last token `break;` is line 410. The cell's other triplets follow the same case/if/return-false
   pattern (`451-453` likewise excludes the `break;` at :454; `376-378` and `456-458` are exact), so this
   reads as a consistent decisive-lines style rather than a wrong pointer — but a reader navigating to
   407-409 does not see the complete quoted statement. No C1 impact: v2 requires the quote verbatim in the
   pinned bytes, not inside the anchor, so the tip receipt (PASS_ROW=23/26 at cf86f9e0) is unaffected.
   SOURCES is append-only except `status`/`recheck`/`used-by`, so the correction path is a lesson note
   (r23 defect-5 precedent: S149 `:1014` → `:1013-1014`), not an in-place edit.
2. No other defect found: hash, byte count, status, opened date, used-by, quote uniqueness, claim truth and
   attribution content all check out.

## Verdict

S157 row: holds. A9: (a) holds, (b) holds, (c) holds. One minor anchor-precision note (407-409 vs 407-410),
non-counting.

VERDICT: holds
