# Reopen S166 — wave-2 falsification seat

- Lane: `/home/vgpnk/Projects/shokunin/mado-shokunin`, REV `39c596307333b8ca0a1e42b3f3b9a748bb8b208b` (round base `8e5d9369`).
- Attack target: SOURCES row **S166** (layer-rules wiki page) and the one claim row citing it,
  **A23** in `corpus/knowledge/rule-attribution-r24.md`.
- Read-only seat. No lane writes except this report; no git/jj write verbs; no installs (none needed);
  scratch only under `/fast/scratch/hyaku/mado-r24/w2/s166/`; every command under `timeout`.
- Instrument note: the `lsp` device is not mounted in this session (`read xd://lsp` → "No such tool:
  xd://lsp. Mounted devices: ast_edit, debug"). Symbol tracing below therefore uses text search on the
  read-only v0.56.2 clone; recorded here as the unavailability the doctrine asks for, not as semantic proof.

## 1. The row as committed

`corpus/SOURCES.md:178` at REV (full cell text, no truncation):

```
| S166 | Layer rules — https://raw.githubusercontent.com/hyprwm/hyprland-wiki/c66e8de21f5ecdc4bc5e278e7d94800ea10957af/content/configuring/core/rules/layer-rules.md | docs | A | layer-rule API, match property, effects, and handles | content/configuring/core/rules/layer-rules.md:18-22, 26-43, 68-76 @ c66e8de21f5ecdc4bc5e278e7d94800ea10957af, sha256:a513798fec803eed723678a2acf24c6e8bdb896fbc7358b01d3201aea2e19836, 2129 B | documents separate layer rules, shared window-rule syntax, namespace matching, effects, and enablement handles | mined | 2026-10-23 | on-release | corpus/knowledge/rule-attribution-r24.md |
```

11 cells; `status=mined`; `opened=2026-10-23`; `recheck=on-release`; `used-by` names the note.
`git status --porcelain` shows neither `corpus/SOURCES.md` nor the note modified, so the working-tree copy
equals the committed REV copy (`git show REV:...` used for every read below).

## 2. Fetch, hash, byte count (own re-fetch, network)

```
curl https://raw.githubusercontent.com/hyprwm/hyprland-wiki/c66e8de2.../content/configuring/core/rules/layer-rules.md
HTTP=200 SIZE=2129
sha256  a513798fec803eed723678a2acf24c6e8bdb896fbc7358b01d3201aea2e19836   2129 B   (re-fetched now)
sha256  a513798fec803eed723678a2acf24c6e8bdb896fbc7358b01d3201aea2e19836   2129 B   (.ufo/waves/round-24/fetch/S166.bin)
sha256  a513798fec803eed723678a2acf24c6e8bdb896fbc7358b01d3201aea2e19836   2129 B   (git show REV:.ufo/waves/round-24/fetch/S166.bin)
cmp re-fetch vs fetch/S166.bin -> BYTES_IDENTICAL
```

All four agree with the recorded `sha256:a513798f…, 2129 B`. The fetch blob is committed at REV
(`git cat-file -e` succeeds), so the counter's offline path and the network re-fetch resolve to one artifact.

## 3. Pin resolves

- Local read-only clone `/fast/scratch/hyaku/mado-r24/src/hyprland-wiki`: `git cat-file -t c66e8de2…` → `commit`;
  `git show c66e8de2…:content/configuring/core/rules/layer-rules.md` → sha256 `a513798f…`, `2129` bytes
  (identical to the re-fetch).
- `git ls-remote https://github.com/hyprwm/hyprland-wiki` → `c66e8de21f5ecdc4bc5e278e7d94800ea10957af` is
  both `HEAD` and `refs/heads/main`; commit date `Thu Oct 22 20:52:44 2026 +0800`; page last content change
  `c04680a 2026-09-18`.
- Anchor cell checks out against the bytes: `:18-22` = "## Layer Rules" intro, `:26-43` = props+effects tables,
  `:68-76` = handle sentence and its Lua example (quote at exactly `:68`).

So the row's pin is a 40-hex commit that resolves, and the bytes served at that URL are the bytes recorded.

## 4. Claim row A23 — line 57 of the note at REV

```
| A23 | The page says layer rules return a handle exposing `set_enabled()` and `is_enabled()` controls. | S166 | "Layer rules also return a handle with `set_enabled()`/`is_enabled()`:" |
```

S166 is cited only by A23 (plus the front-matter `source:` line), so one row to judge.

**(a) Quote occurs verbatim — HOLDS.** Byte 68 of the pinned bytes reads exactly
``Layer rules also return a handle with `set_enabled()`/`is_enabled()`:``. Exact-substring check true on raw
bytes and on whitespace-collapsed bytes; 8 words (≤25); contains the rule-topic word "rules"; quote is unique in
the note (counter raised no `duplicate-quote`).

**(b) Claim is TRUE of the quoted bytes, no overreach — HOLDS.**

- The sentence names a returned handle and both methods; the claim restates exactly that ("a handle exposing
  `set_enabled()` and `is_enabled()` controls"). Nothing is attributed that the page does not say.
- The claim's anchor clause is satisfied by the backticked-identifier disjunct, not the 4-word-run disjunct:
  longest run of quote words inside the claim cell = **0**, but both `` `set_enabled()` `` and `` `is_enabled()` ``
  are backticked in the claim and occur in the quote. Counter `anchored()` (`c1/count.py:46-52`) reads
  `any(len(t) >= 4 and t in quote …)`, so this is the intended path.
- Independent code corroboration that the statement is also *true of v0.56.2*, not wiki-main-only: the clone is
  exactly the tag (`git rev-parse HEAD` = `git rev-parse v0.56.2^{commit}` = `efb50993…`, matching the note's
  header). At that tag, `src/config/lua/objects/LuaLayerRule.cpp:62-64` binds exactly `set_enabled` and
  `is_enabled` on the `HL.LayerRule` metatable, and `src/config/lua/bindings/LuaBindingsConfigRules.cpp:1387`
  returns that handle from `hl.layer_rule`. Page and code agree.

**(c) Says something about rule attribution, not generic rule mechanics — PARTIAL.**

- What the row states is enablement API: a handle, a setter, a getter. It does **not** state which rule produced
  an effect, and it does not state that the handle exposes rule identity. Read alone it is generic rule mechanics.
- Its attribution value is the ablation inference the note makes one line up (table row 23: "enable or disable a
  rule to test it … whether the effect disappears when the rule is off"), and the code makes that inference real:
  `layerRuleSetEnabled` calls `rule->setEnabled()` then `ruleEngine()->updateAllRules()`
  (`LuaLayerRule.cpp:34-42`), and `updateAllRules` re-runs `propertiesChanged(RULE_PROP_ALL)` over every window and
  layer (`src/desktop/rule/Engine.cpp:34-48`), so a disabled rule's effects are recomputed. The ablations route works.
- The note is honest about the limits: same table cell says "this mutates compositor state — operator only, never
  a mado probe", and the handle's identity scope is narrower than "what exposes rule identity" — `layerRuleIndex`
  returns `nil` for every key except `set_enabled`/`is_enabled` (`LuaLayerRule.cpp:57-68`), i.e. no name, match or
  effect getter; the only identity is the opaque `HL.LayerRule(%p)` token held by the Lua caller that created the
  rule (`layerRuleToString`, `:20-30`). So A23 is a per-rule *lever*, not an observer-side identity readout.
- Net: it supports the note's ablation route and the note's negative claim ("Lua exports no attribution beyond
  that"), but the claim row itself is mechanics-anchored; the attribution statement lives in the note's prose, and
  the note labels its limits rather than hiding them. Partial under criterion (c), not a falsification of the row.

## 5. Counter cross-check (diagnostic)

`python3 -I .ufo/waves/round-24/c1/count.py 39c5963… --offline` (offline = diagnostic only, reads committed
fetch blobs): `A23  S166  PASS_ROW  -`; summary `PASS_ROW=23 distinct_sources=14 readme_indexed=True
verdict=TARGET_MET`. My own re-fetch above supplies the counted-mode proof for this one source.

## 6. Findings against the round

1. **S166 itself: no defect found.** Pin resolves; sha256 and byte count reproduce on a fresh network fetch, in
   the committed fetch blob, and in the pinned wiki commit; anchor lines match content; row is 11-cell, `mined`,
   opened 2026-10-23, `used-by` the note.
2. **A23: (a) and (b) hold; (c) partial.** The row is enablement mechanics used as an ablation lever. This does not
   threaten C1's target (23 passing rows / 14 sources; dropping A23 leaves 22/13), but a reader who takes the
   claim rows as the attribution evidence should know that the attribution content of A23 lives in the note's table
   row and its limit cell, not in the claim sentence.
3. Minor, not a defect: the quote keeps the page's word "also", implying window rules return the same handle; A23
   drops it and does not claim the window-rule half — that half is the note's A12–A14, out of scope here.

## 7. Remaining unknowns

- Whether ablating a layer rule on a live v0.56.2 compositor makes an already-applied effect visibly vanish was not
  exercised (host read-only; no `hyprctl` dispatch). The code path above is the documentary/static evidence only.
- `is_enabled()` on an expired rule handle returns `nil` rather than a boolean (`LuaLayerRule.cpp:51-55`); the page
  does not say so, and no claim row asserts otherwise — noted, not scored.

VERDICT: holds — S166's pin, sha256, byte count, committed fetch bytes, and A23's quote verbatimness and truth all
reproduce. Sub-verdict on A23 criterion (c): partial (mechanics-anchored row supporting attribution only through
the note's stated ablation inference).
