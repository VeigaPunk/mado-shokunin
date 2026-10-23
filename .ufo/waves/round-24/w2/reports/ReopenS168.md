# Wave-2 reopen — SOURCES S168 and claim rows A25, A26

Seat: `MadoR24.ReopenS168` (reviewer, leaf). Lane `/home/vgpnk/Projects/shokunin/mado-shokunin`,
master at `39c596307333b8ca0a1e42b3f3b9a748bb8b208b`, round base `8e5d9369`. No file edited except this
report. No tool installed or updated. All commands under `timeout`; scratch fetch in
`/fast/scratch/hyaku/mado-r24/w2/S168/`; read-only clones under `/fast/scratch/hyaku/mado-r24/src/`.

**Instrument note.** The `lsp` device is not mounted in this session (`read xd://lsp` → "No such tool:
xd://lsp. Mounted devices: ast_edit, debug"). Symbol checks below are literal text search over the pinned
read-only v0.56.2 clone, recorded as fallback, not as semantic proof.

Attack target: SOURCES row S168 (`corpus/SOURCES.md:180` at REV), which documents the wiki's rules
overview, and the only two claim rows citing it, A25 and A26 (`corpus/knowledge/rule-attribution-r24.md:59-60`
at REV).

## 1. Row as committed (11 cells, no truncation)

```
| S168 | Rules — https://raw.githubusercontent.com/hyprwm/hyprland-wiki/c66e8de21f5ecdc4bc5e278e7d94800ea10957af/content/configuring/core/rules/_index.md | docs | A | Rule match and evaluation semantics | content/configuring/core/rules/_index.md:6-20 @ c66e8de21f5ecdc4bc5e278e7d94800ea10957af, sha256:46fee4dba2801e2bb5554df13cbabf1e6476dec948de180e88c687c1a307b789, 953 B | Defines props, effects, all-props matching, rule order, and two clients-output field meanings | mined | 2026-10-23 | on-release | corpus/knowledge/rule-attribution-r24.md |
```

`status=mined`, `opened=2026-10-23`, `recheck=on-release`, `used-by` names the note; URL pins a 40-hex
commit under `raw.githubusercontent.com/hyprwm/hyprland-wiki`; sha256 carries the `sha256:` label. Eleven
cells, matching the `## Registry` header at `corpus/SOURCES.md:10`. The note text read from the working
tree equals `git show REV:corpus/knowledge/rule-attribution-r24.md` (A25/A26 at 59/60, ordering sentence
at 27-28).

## 2. Fetch, hash, byte count — own network re-fetch

URL: `https://raw.githubusercontent.com/hyprwm/hyprland-wiki/c66e8de21f5ecdc4bc5e278e7d94800ea10957af/content/configuring/core/rules/_index.md`

| Check | Row says | Observed by this seat |
|---|---|---|
| fetch | — | `http=200 size=953`, ordinary curl, no auth/challenge |
| sha256 | `sha256:46fee4dba2801e2bb5554df13cbabf1e6476dec948de180e88c687c1a307b789` | `46fee4dba2801e2bb5554df13cbabf1e6476dec948de180e88c687c1a307b789` — match |
| bytes | 953 B | 953 B — match |
| `.ufo/waves/round-24/fetch/S168.bin` read at REV (`git show REV:…`) | — | sha256 `46fee4db…`, 953 B — identical |
| wave-1 seat copy `fetch/w1/WikiDebugging-4.bin` | — | sha256 `46fee4db…`, 953 B — identical |
| pinned wiki clone `content/configuring/core/rules/_index.md` | — | blob `9750956…`; `git cat-file -p` sha256 `46fee4db…`, 953 B — identical |

One artifact in four places: my fresh network fetch, the committed fetch blob at REV, the wave-1 seat's
download, and the pinned wiki commit's blob. No self-made-bytes pattern (the fetched bytes reproduce from
the pinned upstream URL itself).

## 3. Pin resolves

- Local clone `/fast/scratch/hyaku/mado-r24/src/hyprland-wiki`: `HEAD` = `c66e8de21f5ecdc4bc5e278e7d94800ea10957af`;
  `git cat-file -t c66e8de2…` → `commit`; commit metadata `2026-10-22T14:52:44+02:00`.
- Network: `git ls-remote https://github.com/hyprwm/hyprland-wiki HEAD refs/heads/main` →
  `c66e8de21f5ecdc4bc5e278e7d94800ea10957af HEAD` and same for `refs/heads/main`.
  GitHub API `/repos/hyprwm/hyprland-wiki/commits/c66e8de…` → `http=200`, `"sha": "c66e8de21f5ecdc4bc5e278e7d94800ea10957af"`.
  The raw URL at that SHA also answers 200 (above), which a nonexistent SHA would not.
- Noted, not absence: `git ls-remote <url> <40-hex sha>` returns nothing because ls-remote patterns refs,
  not commits; the clone and API checks are the resolving evidence.
- Anchor `:6-20` against the bytes: line 6 = "Rules can be used to enforce specific options…", 10-12 =
  props/effects split, 14 = the A26 order sentence, 16 = the A25 all-props sentence, 20 = the
  `fullscreen`/`fullscreenClient` sentence. Both quoted lines and every item named in the row's `teaches`
  cell fall inside `:6-20`.

## 4. Claim row A25 — matching precondition

```
| A25 | The wiki states: _All_ props must match for a rule to be applied. | S168 | "_All_ props must match for a rule to be applied." |
```

**(a) Quote verbatim — HOLDS.** `grep -nF` on the re-fetched bytes: one occurrence, line 16, exact text
including the markdown underscores. 10 quote words (≤25), contains the topic word "rule", single occurrence
in the note (no `duplicate-quote`).

**(b) TRUE of the quoted bytes, no overreach — HOLDS.** The claim is the quote with an explicit "The wiki
states:" attribution; it asserts nothing the sentence does not say. Independent check of the substance in
the pinned release: `CWindowRule::matches` (`src/desktop/rule/windowRule/WindowRule.cpp:376-…`) walks
`m_matchEngines` and `return false` on the first failed engine, returning true only after all pass — so
all-props matching is also v0.56.2 behaviour, not wiki-only wording. (Unknown/unregistered prop entries hit
a `default:` "skipping prop entry" branch, but those are not user-facing `match` props.)

**(c) Rule attribution vs generic mechanics — FAILS.** This row states a matching precondition: when a
rule *may* be applied. It does not say which rule produced an effect, does not expose rule identity, and
names no observation channel. It is the archetype of generic rule mechanics. Worse, the note cites it as
ordering support — `rule-attribution-r24.md:27-28`: "Ordering still decides which value wins: named rules
first, then anonymous, top to bottom, last match wins (A21, A25, A26)" — but A25 says nothing about order;
the ordering content of that sentence comes from A26 (named/anonymous, top-to-bottom) and A21 (last match
wins). A25 is a stray citation there.

## 5. Claim row A26 — evaluation order

```
| A26 | Rules are evaluated top to bottom, but all named rules are evaluated first, then all anonymous ones. | S168 | "Rules are evaluated top to bottom, but all named rules are evaluated first, then all anonymous ones." |
```

**(a) Quote verbatim — HOLDS.** One occurrence at line 14, exact text; 17 quote words (≤25), topic word
"rule", unique in the note.

**(b) TRUE of the quoted bytes, no overreach — HOLDS.** The claim cell is the quote verbatim. Host-era
cross-check (pinned clone `v0.56.2` = `efb50993…`): the named-first order is real for the hyprlang config
path the host runs — `CConfigManager::reloadConfig` parses then calls `reloadRules()`
(`src/config/legacy/ConfigManager.cpp:743-748`), which registers all special-category `windowrule` block
(named) rules, then layer rules, then the inline `m_keywordRules`
(`ConfigManager.cpp:948-963`; inline rules are appended there at `:2050-2052`); `CRuleEngine::registerRule`
just appends (`src/desktop/rule/Engine.cpp:14-16`), and `CWindowRuleApplicator::readStaticRules` iterates
`ruleEngine()->rules()` in that insertion order (`src/desktop/rule/windowRule/WindowRuleApplicator.cpp:493`),
skipping non-window rules. So named window rules precede anonymous ones at the pinned tag.
Caveat, not a quote-vs-claim overreach: the Lua path in the same release registers each `hl.window_rule`
immediately in call order (`src/config/lua/bindings/LuaBindingsConfigRules.cpp:1190-1196`), and no sort or
partition of `m_rules` exists anywhere in `src/desktop` or `src/config` (only prop-table and config-path
sorts). The bare phrasing "Rules are evaluated…" therefore states a hyprlang-path fact as general; the
note's own era caveat ("Wiki rows are `[INF-docs]` for this host") is what covers that, not the row.

**(c) Rule attribution vs generic mechanics — PARTIAL.** Evaluation order decides precedence: when several
rules match, the later-evaluated rule's effects win, and that is the premise behind the note's
"attribution by reasoning" sentence. But the row itself names no rule, states no identity, and exposes no
channel; it is precedence mechanics, one inference step short of "which rule produced the effect". Partial,
not a pass.

## 6. Counter cross-check (diagnostic)

`python3 -I .ufo/waves/round-24/c1/count.py 39c5963… --offline` (offline reads the committed fetch blobs):
`A25 S168 PASS_ROW -`, `A26 S168 PASS_ROW -`; summary `PASS_ROW=23 distinct_sources=14 readme_indexed=True
verdict=TARGET_MET`, counter sha256 `b2f37c571455e3aecedef3605cbf5d7844ce2ab7a273a9cb36cc57fec37efc66`.
My network fetch above supplies the counted-mode byte proof for S168 (re-fetched sha256 equals the recorded
sha256), so both rows pass the frozen v2 predicate; the downgrade in this report is the wave-2 criterion
(c), which the predicate does not encode (its topic regex accepts any `rule`-word line).

## 7. Findings against the round

1. **S168 row: no defect found.** Pin resolves locally and remotely; sha256 and byte count reproduce on a
   fresh fetch, in the committed fetch blob at REV, in the wave-1 copy, and in the pinned wiki blob; the
   anchor spans every taught item; the row is 11 cells, `mined`, opened 2026-10-23, used-by the note.
2. **A25: not an attribution row; (c) fails.** It is a matching precondition and is mis-cited at
   `rule-attribution-r24.md:27-28` as ordering support, which it does not provide. (a) and (b) hold.
3. **A26: precedence mechanics; (c) partial.** It supplies the order premise for inferring which value
   wins but states no rule identity or exposure channel; its bare-fact wording also universalizes a
   hyprlang-path fact in v0.56.2 (Lua call order is not reordered), covered by the note's `[INF-docs]`
   era label. (a) and (b) hold.
4. **Impact on C1 is arithmetic-free.** Both rows count under the frozen predicate, and both are among the
   23 passing rows. Dropping both leaves 21/26 rows from 13 distinct sources — still above the
   ≥6-rows/≥3-sources target. So this finding is about the attribution content of the claim rows, not the
   target's satisfaction.
5. The wave-1 seat was transparent: `WikiDebugging.md` says its rules-overview findings "are rules
   semantics, not a documented rule-attribution log format." The note's own S168 scope cell likewise says
   "Rule match and evaluation semantics". The defect is that the note then leans on A25/A26 in its
   ordering/attribution-by-reasoning sentence without flagging that neither row is an attribution row.

## 8. Remaining unknowns

- Live-host truth of named-first was not exercised (no `hyprctl` dispatch/reload; host is read-only and its
  config provider is hyprlang per the round-12 note). The code-order evidence above is static.
- Whether the newest-git wiki commit and the v0.56.2 tag agree on the Lua path's ordering was not tested
  beyond v0.56.2's own bindings; the wiki labels itself latest git, which the note already scopes.
- The same (c) reading would touch other mechanics rows (A1–A9, A12–A17); out of this seat's scope, which
  is S168 only.

VERDICT: partial — S168's pin, sha256, byte count, committed fetch bytes, anchor, and 11-cell fields all
reproduce and hold; A25 (a)(b) hold but (c) fails (generic matching mechanics, mis-cited as ordering
support); A26 (a)(b) hold, (c) partial (precedence mechanics feeding attribution-by-reasoning, no identity
or exposure statement).
