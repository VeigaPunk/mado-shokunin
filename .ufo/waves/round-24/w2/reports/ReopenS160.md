# Reopen S160 — Lua window-rule userdata (mined SOURCES row)

Scope: SOURCES.md row S160 at lane HEAD 39c596307333b8ca0a1e42b3f3b9a748bb8b208b (round base
8e5d93691e2f7baa3d4a0a61c9428e5acb5d2122). Claim rows citing it: A13 and A14 in
corpus/knowledge/rule-attribution-r24.md. I re-fetched the pinned URL, re-hashed, compared with the row and with
the committed fetch bytes, confirmed the pin, and read both claims against the bytes.

## 1. Row record (SOURCES.md:172)

| field | value |
|---|---|
| id | S160 |
| title | Lua window-rule userdata implementation |
| URL | https://raw.githubusercontent.com/hyprwm/Hyprland/efb50993780079460b0cbed1363e2166a2de1d9f/src/config/lua/objects/LuaWindowRule.cpp |
| kind / tier / area | code / A / Lua window-rule handle equality and enabled methods |
| claim lines | src/config/lua/objects/LuaWindowRule.cpp:12-80 |
| sha256 (row) | sha256:02f70f045aaddab9def977fdcab56e355510dc50f72de4e86df314aa1a466b8a |
| bytes (row) | 2223 B |
| note | "The userdata compares locked rule references, exposes enabled operations and wraps a weak rule reference" |
| status / opened / recheck | mined / 2026-10-23 / on-release |
| used-by | corpus/knowledge/rule-attribution-r24.md |

The row satisfies the C1 v2 shape: URL pinned to a 40-hex commit under raw.githubusercontent.com/hyprwm/Hyprland,
status `mined`, opened 2026-10-23, used-by names the note. The anchor `:12-80` is the whole 80-line file, so it
covers every quote cited from it.

## 2. Independent fetch vs committed bytes vs row metadata

- Fetched the pinned raw URL myself (`curl`, exit 0, HTTP 200). sha256 of the fetched bytes:
  `sha256:02f70f045aaddab9def977fdcab56e355510dc50f72de4e86df314aa1a466b8a`, size 2223 B.
- Both match the row exactly (sha256:02f70f04…, "2223 B").
- `cmp` fetched bytes vs `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-24/fetch/S160.bin` →
  identical; S160.bin independently hashes `sha256:02f70f04…` at 2223 B.
- Not stale, not a proxy page: content is C++ source (`#include "LuaWindowRule.hpp"` … closing brace at line 80).

## 3. Pin resolution (both channels)

- Local clone `/fast/scratch/hyaku/mado-r24/src/Hyprland-v0.56.2`: `git cat-file -t
  efb50993780079460b0cbed1363e2166a2de1d9f` → `commit`; clone HEAD is exactly that commit;
  `git tag --points-at` and `git describe --tags --exact-match` → `v0.56.2`.
- Same commit from the clone's object store: `git show <pin>:src/config/lua/objects/LuaWindowRule.cpp` →
  `sha256:02f70f04…`, 2223 B — a second channel to the same bytes.
- Remote: `git ls-remote https://github.com/hyprwm/Hyprland refs/tags/v0.56.2` → `efb5099378… refs/tags/v0.56.2`;
  the tag is lightweight (emits the commit directly, no `^{}` line). Pin resolves upstream and locally.

## 4. Claim rows citing S160

`grep "S160"` in corpus/knowledge/rule-attribution-r24.md → only the front-matter source list (line 1) and rows
A13/A14 (lines 47-48). No other claim row cites S160.

### A13 — "The setter applies the supplied boolean to the rule and calls `updateAllRules`."

Quote: `"rule->setEnabled(lua_toboolean(L, 2)); Desktop::Rule::ruleEngine()->updateAllRules();"`

- **(a) verbatim: holds.** Both statements are lines 40-41 of the fetched bytes; whitespace-collapsed (two
  lines with leading indent → one space) the quote occurs exactly. Checked programmatically (`re.sub(r'\s+',' ')`
  containment → True).
- **(b) true of the bytes: holds, with one precision note.** `windowRuleSetEnabled` is the `set_enabled` method
  (registered in `windowRuleIndex`, lines 62-63). It type-checks argument 2 as boolean, applies
  `setEnabled(lua_toboolean(L, 2))` and calls `ruleEngine()->updateAllRules()`. The claim adds nothing the bytes
  do not say. Precision note: the function first locks the weak ref and returns 0 *without* applying or updating
  when the rule is dead (lines 36-38), which the quoted fragment omits; A13 states the two actions without the
  same "for a live rule" qualification A14 uses. That is a wording imprecision, not a false statement — the
  quoted path is exactly what the claim paraphrases.
- **(c) rule attribution: fails as written.** The row states rule-flag propagation mechanics: set the enabled
  bit, re-run all rules. It names no window, no effect, no matching link, and exposes no identity; it is the
  generic machinery behind a toggle, not a statement that any rule produced an effect or that identity is
  observable. Its only attribution value is indirect — `updateAllRules` is what makes the note's operator-only
  intervention test (disable a known named rule, watch the effect) take effect immediately. The note itself
  frames that use correctly, so the claim is not overstated, but the row does not satisfy criterion (c).

### A14 — "For a live rule, this pushes its `isEnabled` flag as one Lua boolean result."

Quote: `"const auto rule = ref->lock(); if (!rule) { lua_pushnil(L); return 1; } lua_pushboolean(L, rule->isEnabled()); return 1;"`

- **(a) verbatim: holds.** The span is lines 48-55 of the fetched bytes; whitespace-collapsed (including the
  blank line before `lua_pushboolean`) the quote occurs exactly. Containment → True.
- **(b) true of the bytes: holds.** `windowRuleIsEnabled` (the `is_enabled` method, line 65) locks the weak ref;
  dead rule → `lua_pushnil` and `return 1`; live rule → `lua_pushboolean(L, rule->isEnabled())` and `return 1`.
  The claim is scoped "for a live rule" and matches exactly; it does not overreach.
- **(c) rule attribution: fails as written.** The row is a getter for a rule object's enabled bit. It says
  nothing about which rule matched a window or produced an effect. It exposes rule *state*, not rule identity
  (the name-keyed lookup is A12's claim, in S159, not this row). Again the note uses it honestly — as the read
  side of the operator-only named-handle test — and explicitly labels that route mutating, "operator only,
  never a mado probe".

### Adjacent observation on the table row that cites A12–A14 (low severity)

The note's route table says the named-handle route "shows whether the effect disappears when the rule is off".
A13/A14 establish toggle + re-apply + flag read, but neither states that a disabled rule stops matching. That
premise exists in the pinned tree — `IRule::canMatch()` = `!m_matchEngines.empty() && m_enabled`
(src/desktop/rule/Rule.cpp:124-126), and `CWindowRule::matches` returns false on `!canMatch()`
(src/desktop/rule/windowRule/WindowRule.cpp:376-378), which is inside S157's anchored span `:376-378`. So the
statement is true of the pinned bytes, but no claim row asserts it and the table row does not cite S157 for that
cell (it cites A12–A14; layer rules A23). This is a citation-precision gap, not a falsehood. The same table row
also puts a safety caveat ("this mutates compositor state — operator only, never a mado probe") in the "What it
does not show" column instead of an attribution limitation; a reader loses the real limitation there (the route
only tests a rule you already know by name; it cannot discover which rule fired).

## 5. Verdict

VERDICT: partial

- The S160 row itself holds on every mechanical check: URL content re-fetched at HTTP 200 with
  `sha256:02f70f045aaddab9def977fdcab56e355510dc50f72de4e86df314aa1a466b8a` / 2223 B, identical to the row and
  byte-identical to `.ufo/waves/round-24/fetch/S160.bin`; the pin `efb50993…` resolves both locally (commit,
  tag `v0.56.2`, file hash from the object store) and upstream (`git ls-remote` tag line).
- Per-row: A13 — (a) holds, (b) holds with a missing dead-rule qualifier, (c) fails. A14 — (a) holds,
  (b) holds, (c) fails. Both quotes are verbatim and both claims are true of the quoted bytes; neither claim row
  says anything about attribution in the criterion's sense (which rule produced an effect / what exposes rule
  identity). They are generic rule mechanics that the note honestly frames as an operator-only, state-mutating
  test.
- Consequence for C1: nothing in the frozen v2 predicate is violated (it tests verbatim quote + claim-anchor, and
  both rows pass those: `updateAllRules` and `isEnabled` are backticked identifiers occurring in the quotes). But
  if the wave-2 attribution-relevance criterion is enforced as a row-level rule, A13 and A14 should not be
  counted as attribution rows — C1 would keep its PASS_ROW count only if the other 21 rows carry it (A1–A12,
  A15–A26 are untouched by this report).

## 6. Residual risk / verification gaps

- I did not re-run the C1 counter (`c1/count.py REV`); it re-fetches all 14 sources and other seats own that
  check. My hashes are independent of the counter's recorded receipts.
- Remote pin check used the tag ref (lightweight, points at the commit); I did not check whether some other ref
  still points at the same commit, which is irrelevant to the pin's validity.
- Host not touched: no hyprctl verbs beyond none at all, no dispatch, no reload, no window titles.
- No tool installs or updates; curl, git, coreutils and python3 were already present.
