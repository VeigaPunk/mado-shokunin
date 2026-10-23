# Reopen S159 — review report (round 24 wave 2, falsify)

- Seat: `MadoR24.ReopenS159` (reviewer, leaf — no spawns).
- Reviewed lane: `/home/vgpnk/Projects/shokunin/mado-shokunin` at `39c596307333b8ca0a1e42b3f3b9a748bb8b208b` (jj colocated; commit resolves).
- Assigned item: re-open SOURCES row S159, re-fetch its pinned URL, verify sha256/byte count against row and committed fetch bin, confirm pin resolvability, and judge claim row A12 (quote verbatim, claim truth/no overreach, attribution axis).

## 1. Fetch identity — holds

| Check | Row S159 | Committed bin `.ufo/waves/round-24/fetch/S159.bin` | Fresh fetch (this seat) |
|---|---|---|---|
| sha256 | `157c3e45b364f3e41b6fd7cf13fd19e7477e8c03a6a75c6c46fde5e2b5715be9` | `157c3e45b364f3e41b6fd7cf13fd19e7477e8c03a6a75c6c46fde5e2b5715be9` | `157c3e45b364f3e41b6fd7cf13fd19e7477e8c03a6a75c6c46fde5e2b5715be9` |
| bytes | 61617 B | 61617 | 61617 |
| cmp | — | — | identical to committed bin |

- Fresh fetch (curl, raw.githubusercontent.com): `https://raw.githubusercontent.com/hyprwm/Hyprland/efb50993780079460b0cbed1363e2166a2de1d9f/src/config/lua/bindings/LuaBindingsConfigRules.cpp` → sha256 `157c3e45…`, 61617 B, byte-identical to committed S159.bin. Row's recorded sha256/size are truthful.

## 2. Pin resolvability — holds

- `git ls-remote https://github.com/hyprwm/Hyprland refs/tags/v0.56.2` → `efb50993780079460b0cbed1363e2166a2de1d9f`. The pinned commit is exactly tag v0.56.2 (the row's "Hyprland v0.56.2 = commit efb5099…" framing), and resolves upstream right now.
- Local read-only clone `/fast/scratch/hyaku/mado-r24/src/Hyprland-v0.56.2`: `cat-file -e efb5099…^{commit}` resolves; `git show efb5099…:src/config/lua/bindings/LuaBindingsConfigRules.cpp` → sha256 `157c3e45…`, 61617 B (matches row/bin). (S3 `git ls-remote` on the lane repo — not to be confused with upstream.)

## 3. Claim row A12 — per-clause judgment

Row: `| A12 | For non-empty names, `m_luaWindowRules` stores each rule by name before engine registration. | S159 | "if (!name.empty()) self->m_luaWindowRules[name] = rule; Desktop::Rule::ruleEngine()->registerRule(SP<Desktop::Rule::IRule>(rule));" |`

### (a) Quote occurs verbatim — holds
- Quote is exactly fetched-bytes lines 1194–1196 of `LuaBindingsConfigRules.cpp` (function `hlWindowRule`):
  - 1194 `if (!name.empty())`
  - 1195 `self->m_luaWindowRules[name] = rule;`
  - 1196 `Desktop::Rule::ruleEngine()->registerRule(SP<Desktop::Rule::IRule>(rule));`
- Whitespace-collapsed verbatim match: TRUE (whole-file ws-collapse contains the ws-collapsed quote; joint of the three lines equals the quote).
- Row anchor `src/config/lua/bindings/LuaBindingsConfigRules.cpp:1167-1198,1271-1274,1392-1399 @ efb5099…`: the quote's lines 1194–1196 lie inside 1167–1198 (the `hlWindowRule` binding). Anchors 1271–1274 (inside `hlLayerRule`) and 1392–1399 (`registerConfigRuleBindings` registration table) are other functions covered by the same row and were not required by A12; no mismatch seen in passing (layer-rule function at 1272+, register table at 1392+).
- v2 predicate clauses: quote = 6 words ≤ 25; contains rule-topic word (`rule`/`Rule`); claim-anchor clause satisfied via backticked identifier `` `m_luaWindowRules` `` (≥4 chars) occurring in the quote.

### (b) Claim TRUE of the quoted bytes; no overreach — holds
- Source context (`hlWindowRule`, 1167–1198):
  ```cpp
  SP<Desktop::Rule::CWindowRule> rule;
  if (!name.empty() && self->m_luaWindowRules.contains(name)) {
      rule = self->m_luaWindowRules[name];
  } else {
      rule = makeShared<Desktop::Rule::CWindowRule>(name);
      if (!name.empty())
          self->m_luaWindowRules[name] = rule;
      Desktop::Rule::ruleEngine()->registerRule(SP<Desktop::Rule::IRule>(rule));
  }
  rule->setEnabled(enabled);
  ```
- "For non-empty names": the store is guarded by `if (!name.empty())` — matches.
- "stores each rule by name": the only write site for `m_luaWindowRules` in the file is line 1195 (grep: 3 hits — 1190 contains-check, 1191 read, 1195 write). A named rule object is stored exactly once by name (the `contains` branch prevents overwrite-re-registration); unnamed rules are registered but not cached, which the claim's scoping correctly excludes. `m_luaWindowRules` is a `CConfigManager` member; no other window-rule store path exists in this file (line 490 `name.empty()` belongs to `hlEnv`, not a rule binding).
- "before engine registration": statement order in the quoted bytes is store (1195) then `registerRule` (1196) — matches, without implying anything about the reuse path (which does not re-register; nothing in the claim conflicts with that).
- No overreach: the claim is scoped to non-empty names and to the registered-new-rule path, and asserts only what the quoted lines do.

### (c) Rule-attribution axis (not generic mechanics) — holds (attribution substrate, weak end)
- The claim is not about generic rule mechanics (it does not describe how matching/ordering/effects work). It asserts the existence and semantics of the name-keyed identity store `m_luaWindowRules`: a named Lua window rule is retrievable by name (line 1191 reuse) — i.e., what exposes rule identity in the Lua/config-rule path. In the note's attribution table this is the "named rule handle" route: A12 is the first of the A12–A14 chain that lets the operator address a rule by name (`set_enabled`/`is_enabled`) — an identity/attribution capability, not an effect-mechanic fact. Caveat: the phrase "before engine registration" is ordering mechanics; the substantive content (name-keyed persistence) is the attribution-relevant part. Verdict: holds, weaker side of the axis.

## 4. Verdicts

- S159 row fidelity: **holds** (sha256, size, anchors, status `mined`, opened 2026-10-23, used-by naming the note — all consistent with the predicate).
- Pin: **holds** (upstream tag v0.56.2 == pinned commit; clone blob identical).
- A12: **holds** (quote verbatim; claim true, no overreach; attribution-axis content).

`VERDICT: holds` — no finding against round 24 from this item.

## 5. Residual risk / verification gaps

- Checks performed on the remote `raw.githubusercontent.com` URL at review time (2026-10-23); byte-identity with a pinned commit is stable by construction (content-addressed), so no drift risk beyond GitHub availability.
- Anchors 1271–1274 and 1392–1399 were cross-read but not required by A12; they belong to the same S159 row's topic cell but no A-row depends on quote line location there.
- I did not re-run the C1 counter (wave-1 receipt at cf86f9e0 already counts PASS_ROW=23/26); this seat's fetch/hash/quote checks reproduce the per-row verifiable part independently.
