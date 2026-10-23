# Reopen S161 — Lua query bindings (queued SOURCES row)

Scope: SOURCES.md row S161 at lane HEAD 39c596307333b8ca0a1e42b3f3b9a748bb8b208b (round base 8e5d93691e2f7baa3d4a0a61c9428e5acb5d2122). Item is a queued row: no claim row in rule-attribution-r24.md cites it. Verification below re-opens the pinned source independently.

## 1. Row record (SOURCES.md:173)

| field | value |
|---|---|
| id | S161 |
| source | Lua query bindings |
| URL | https://raw.githubusercontent.com/hyprwm/Hyprland/efb50993780079460b0cbed1363e2166a2de1d9f/src/config/lua/bindings/LuaBindingsQuery.cpp |
| kind | code |
| claim lines | src/config/lua/bindings/LuaBindingsQuery.cpp:62-65,83-123,392-411 |
| sha256 (row) | af0d274b5616ae69b8f62bdf2534a29586eab2a3d20b28c1b0e620d313ca66db |
| bytes (row) | 12451 B |
| note | "`get_windows` filter inputs and tag-match behavior; no matched-rule result is listed in this file's query bindings" |
| status | queued (2026-10-23, on-release); knowledge column "—" |

## 2. Independent fetch vs committed bytes vs row metadata

- Fetched the pinned raw URL myself: `curl -fsSL https://raw.githubusercontent.com/hyprwm/Hyprland/efb50993780079460b0cbed1363e2166a2de1d9f/src/config/lua/bindings/LuaBindingsQuery.cpp` → exit 0.
- sha256 of fetched bytes: `af0d274b5616ae69b8f62bdf2534a29586eab2a3d20b28c1b0e620d313ca66db` — identical to the row.
- Byte count: 12451 — identical to the row's "12451 B".
- `cmp` fetched bytes vs committed `.ufo/waves/round-24/fetch/S161.bin` → IDENTICAL (committed fetch bytes are exactly the pinned-URL content; sha256 of S161.bin also af0d274b…, 12451 bytes, file(1) "C source, ASCII text").

## 3. Pin resolution

- Local clone `/fast/scratch/hyaku/mado-r24/src/Hyprland-v0.56.2` contains object `efb50993780079460b0cbed1363e2166a2de1d9f` (`git cat-file -t` → commit; `git log -1` → "[gha] Nix: update inputs", 2026-08-05). The pin resolves in Hyprland history. (Used the local-clone branch of the assignment's pin check, not remote `git ls-remote`; see gaps.)

## 4. Claim rows citing S161

- `grep "S161"` in corpus/knowledge/rule-attribution-r24.md → no matches. The file's front matter (line 1) enumerates its sources: S153–S168 excluding S161. Zero claim rows (A1–A26) cite S161.
- `grep "S161"` in .ufo/waves/round-24/registration.md → no matches.
- **Per-row verdicts: none exist.** There is no claim to judge for (a) verbatim quote, (b) truth/no-overreach, (c) rule-attribution relevance. The row is queued with no knowledge row, consistent with its "—" receipt column.

## 5. Sanity check of the queued note against the bytes (informational, not a claim verdict)

- 62-65: tag filter inside `windowMatchesQuery` — `if (query.tag) { if (!w->m_ruleApplicator || !w->m_ruleApplicator->m_tagKeeper.isTagged(*query.tag, true)) return false; }`. "Tag-match behavior" is accurate and touches rule machinery (`m_ruleApplicator`/`m_tagKeeper`).
- 83-123: `parseWindowQueryFromTable` (monitor/workspace/floating/mapped/class/title/tag) + `hlGetWindows` reading a filters table and calling `pushWindowsMatchingQuery`. "get_windows filter inputs" is accurate.
- 392-411: `Internal::registerQueryBindings` registers get_windows/get_window/get_active_window/get_workspaces/get_monitors… — no query binding exposes a matched-rule result.
- Whole-file scan for `rule|Rule|RULE`: only the include of `windowRule/WindowRuleEffectContainer.hpp` and the tag-keeper use at 62-65. "no matched-rule result is listed in this file's query bindings" is accurate for this file.
- Note: the file's only rule-attribution-adjacent surface is the tag filter's dependence on `m_ruleApplicator->m_tagKeeper`; a future mined claim citing S161 would need to stay on that (or on query-binding registration) to satisfy category-A relevance, and would not support stronger rule-attribution statements.

## 6. Verdict

VERDICT: holds — pinned URL content matches both the row metadata (sha256 af0d274b…, 12451 B) and the committed fetch bytes (.ufo/waves/round-24/fetch/S161.bin, byte-identical); the pin resolves in Hyprland history; and no claim row cites S161 (queued), so there are no per-row claims to falsify.

## 7. Residual risk / verification gaps

- Pin existence confirmed via the local clone's object store, not remote `git ls-remote`; a remote force-push that dropped the commit is not exercised (untested, low likelihood for this historical commit).
- No claim rows exist, so (a)/(b)/(c) judgments are vacuous for this wave; they become applicable when S161 is mined (on-release).
- No tool installs made (curl, git, coreutils pre-existing).
