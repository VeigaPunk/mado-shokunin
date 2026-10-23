# ReopenS156 — SOURCES row S156 and the two claim rows citing it (A7, A8)

Seat: wave-2 reviewer `MadoR24.ReopenS156` (leaf; no subagents). Lane tip
`39c596307333b8ca0a1e42b3f3b9a748bb8b208b`, round base `8e5d9369`. Attack target:
`corpus/SOURCES.md` row S156 and `corpus/knowledge/rule-attribution-r24.md` rows A7 and A8.
Read-only: no lane file edited except this report; no git/jj write; no installs (none needed).

## 1. What the row claims (at 39c59630, byte-identical at cf86f9e0 where it was added)

`corpus/SOURCES.md:168`:

| field | value |
|---|---|
| source | Hyprland v0.56.2 `WindowRuleApplicator.hpp` — `https://raw.githubusercontent.com/hyprwm/Hyprland/efb50993780079460b0cbed1363e2166a2de1d9f/src/desktop/rule/windowRule/WindowRuleApplicator.hpp` |
| kind / tier | code / A |
| anchor | `src/desktop/rule/windowRule/WindowRuleApplicator.hpp:25-38,63-72,74-88,140-158 @ commit efb50993780079460b0cbed1363e2166a2de1d9f, sha256:334e1254a66e2df8ef243544e3ff99db398ed5ec6e48996d496d05ff7bf50f44, 9865 B` |
| status / opened / recheck / used-by | `mined` / `2026-10-23` / `on-release` / `corpus/knowledge/rule-attribution-r24.md` |

`git diff cf86f9e0 39c59630 -- corpus/SOURCES.md` is empty and the S156 line is byte-identical at
both revisions (`diff` of the two `git cat-file -p` extractions → `IDENTICAL_ROW_CF86F9E_TO_TIP`), so
no in-place mutation occurred after the row was opened.

## 2. Pin, re-fetch, sha256, byte count

Commands (scratch `/fast/scratch/hyaku/mado-r24/w2/ReopenS156`):

```
timeout 120 curl -sS -L -o S156.fetched.bin \
  https://raw.githubusercontent.com/hyprwm/Hyprland/efb50993780079460b0cbed1363e2166a2de1d9f/src/desktop/rule/windowRule/WindowRuleApplicator.hpp
# curl_exit=0
wc -c < S156.fetched.bin        -> 9865
sha256sum S156.fetched.bin      -> 334e1254a66e2df8ef243544e3ff99db398ed5ec6e48996d496d05ff7bf50f44
```

| artefact | bytes | sha256 |
|---|---|---|
| row's recorded pin | `9865 B` | `sha256:334e1254a66e2df8ef243544e3ff99db398ed5ec6e48996d496d05ff7bf50f44` |
| my re-fetch now | 9865 | `334e1254a66e…bf50f44` |
| committed `.ufo/waves/round-24/fetch/S156.bin` | 9865 | `334e1254a66e…bf50f44` |
| blob at pin in read-only clone | 9865 | `334e1254a66e…bf50f44` |

All four agree exactly. The committed fetch artefact is not a self-made byte string: it is
byte-identical to both a fresh fetch of the pinned URL and the clone's blob.

Pin resolution (both allowed routes; local clone is
`/fast/scratch/hyaku/mado-r24/src/Hyprland-v0.56.2`):

```
git rev-parse HEAD                       -> efb50993780079460b0cbed1363e2166a2de1d9f
git log -1 --format='%H %d %s' <pin>     -> efb5099…  (grafted, HEAD, tag: v0.56.2) [gha] Nix: update inputs
timeout 60 git ls-remote --tags origin 'refs/tags/v0.56.2*'
  -> efb50993780079460b0cbed1363e2166a2de1d9f  refs/tags/v0.56.2
git rev-parse <pin>:src/desktop/rule/windowRule/WindowRuleApplicator.hpp -> 202cf8d5d07fd374598576f0be06d54e679306be
```

The 40-hex pin is a real upstream **tag** commit (v0.56.2), not a floating branch, and the blob at
that commit hashes to the same bytes as the raw URL. Anchor spans cover the quoted lines: A7 at
line 77 (inside `74-88`), A8 at line 140 (start of `140-158`).

Corpus rows S153–S168 pin the same commit (note line 1), and the row's `used-by` names the note,
so the row is load-bearing for C1's `mined`/`opened 2026-10-23`/`used-by` predicate.

Tooling note: this seat has no `lsp` device in its tool inventory (no server could be started), so
symbol tracing below is by text search over the pinned clone plus direct reading of the pinned
bytes. Recorded as unavailability, not presented as semantic proof.

## 3. A7 — "Each generated property pairs a `COverridableVar` value with a rule-property mask."

Quote: `std::pair<Types::COverridableVar<type>, std::underlying_type_t<eRuleProperty>> m_##name = {def, RULE_PROP_NONE};`

**(a) Verbatim.** Yes. `WindowRuleApplicator.hpp:77` inside the `DEFINE_PROP` macro. Source line has
alignment padding after the `;` and a trailing `\`; the quote reproduces the internal spacing exactly
(`grep -n` at line 77; `awk 'NR==77' | cat -A` shows single spaces between template tokens). A
whitespace-collapsed check of the pinned bytes returns `verbatim_collapsed=True` for A7.
6 whitespace-separated tokens, well under the 25-word cap.

**(b) True of the quoted bytes, no overreach.** Holds. The macro emits
`private: std::pair<Types::COverridableVar<type>, std::underlying_type_t<eRuleProperty>> m_##name = {def, RULE_PROP_NONE};`
then `public:` accessors that return `.first` and an `name##Override` setter; 41 `DEFINE_PROP(…)`
invocations exist in the header and all go through this one macro (single `#define DEFINE_PROP`,
`#undef` at line 142). `eRuleProperty` is a genuine bit-flag enum
(`src/desktop/rule/Rule.hpp:13-35`, `RULE_PROP_CLASS = 1<<0 … RULE_PROP_EXEC_PID = 1<<19`,
`RULE_PROP_ALL = max`), and `IRule::getPropertiesMask()` (`src/desktop/rule/Rule.cpp:108-110`)
returns exactly that underlying type, so calling the second element a "rule-property mask" is not a
gloss. The claim is scoped to "generated property" — it does not claim every member of the class is
a pair (`m_dynamicTags`, `m_tagKeeper`, `m_execRules`, `m_otherProps`, `static_` are not), so it does
not overreach.

**(c) Attribution content.** Indirect, but it holds in the note's own frame. The row states what is
stored *beside* an effect value: a mask of `eRuleProperty` bits, i.e. the match-property signature
of the rule that fed the value, not a rule id/name/pointer. That is the storage-side fact behind the
note's line 24 ("which *match properties* a setting came through") and the identity negative. The
mask's rule-derived population is shown by S155/A6 (`m_alpha.second = rule->getPropertiesMask()`,
`WindowRuleApplicator.cpp:156`) and by 40 call sites in `WindowRuleApplicator.cpp`; A7 itself only
supplies the slot. So: attribution-relevant as "what is retained per effect", with the semantic
weight carried by A6, not by A7's sentence.

Precision caveats (not claim failures, see §5):
- `m_tonemap.second` is never assigned — `WINDOW_RULE_EFFECT_TONEMAP` at
  `WindowRuleApplicator.cpp:348-350` writes only `.first`; it is the one generated property out of 41
  with no mask write (40 distinct `m_*\.second` writes, `m_noAutoHDR` written twice, tonemap zero).
- The 40 per-property mask writes have **0 reads**: a classifier over
  `WindowRuleApplicator.cpp` finds 41 `.second` writes and 0 non-write occurrences; the members are
  `private:` (macro line 76) and the only accessors return `.first`; header has no `friend`; no other
  file in `src/` touches `m_<prop>.second`. The per-property masks are write-only state in v0.56.2.
  (The masks that *are* consulted are the separate ones: `m_dynamicTags` mask at
  `WindowRuleApplicator.cpp:67`, `m_otherProps` `propMask` at `:75`.)

## 4. A8 — "Dynamic tags use `m_dynamicTags` to pair each tag string with a property mask."

Quote: `std::vector<std::pair<std::string, std::underlying_type_t<eRuleProperty>>> m_dynamicTags;`

**(a) Verbatim.** Yes, `WindowRuleApplicator.hpp:140`. Source has alignment padding between `>>>`
and `m_dynamicTags` (od confirms `>>>` then spaces then the name); whitespace-collapsed check returns
`verbatim_collapsed=True`. 3 tokens.

**(b) True of the quoted bytes, no overreach.** Holds, and the call site makes the gloss exact:
`WindowRuleApplicator.cpp:162` (inside `applyDynamicRule`, defined at `:81`) runs
`m_dynamicTags.emplace_back(effect, rule->getPropertiesMask());` in `case WINDOW_RULE_EFFECT_TAG`,
with the same `effect` string handed to `m_tagKeeper.applyTag(effect, true)` at `:163` — so the
stored string is the tag, and the companion is the producing rule's property mask. The mask is then
read at `:66-70` (`el.second & props` → `m_tagKeeper.removeDynamicTag(el.first)`) to retract tags
when a matching property changes. `m_dynamicTags` has exactly three sites in the tree (declaration,
the `emplace_back`, the `erase_if`), so "pair each tag string with a property mask" is accurate; the
declaration alone would underdetermine "tag", but the field name plus the pinned call site settle it,
and nothing contradicts the claim. No overreach: the claim says nothing about export or reading by
the user, and the tag route's visible side is carried by A10/A22, not by A8.

**(c) Attribution content.** Indirect but on-topic. Dynamic tags are the data behind the note's only
positive attribution route (§Answer row 3: unique `tag` effect read from `hyprctl clients`), and this
row records that the tag's stored provenance is again a property mask, not the rule. It is a
declaration-level row, so it does not by itself show any user-visible identity — that is A10's job.

## 5. Findings against the round

1. **Note line 24 overstates what the per-property mask "shows", in two measured ways.** It says the
   applicator's per-property origin is "a value plus a rule-property mask and a priority class
   (A5–A8) | which *match properties* a setting came through". The bytes support "stores": the mask is
   written from `rule->getPropertiesMask()` at 40 call sites. They do not support "shows/uses": the 40
   per-property masks are never read anywhere (private, `.first`-only accessors, no `friend`, 0 reads
   in the only translation unit that owns them), and `m_tonemap` never records a mask at all (1 of 41
   generated properties). Suggested qualification for the note: "records the rule's match-property
   mask internally (40 of 41 properties; `tonemap` none); the masks are never consulted once written
   and are not exported." This is a **prose precision defect against C1**, not a claim-row failure:
   A7/A8 pass the frozen v2 predicate and both claim sentences are true of their bytes.
2. **A7 and A8 are the two weakest rows in the attribution set.** Both are declaration/layout
   statements; their attribution payload is delivered by A6/S155 (`rule->getPropertiesMask()`) and by
   the `.cpp` call sites, which are not in either row's quote. If a stricter reading of criterion (c)
   struck them, C1's target would still hold: `PASS_ROW` would drop from 23 to 21 (≥ 6), distinct
   sources from 14 to 13 (≥ 3), and the README coverage-map index is unaffected. So the C1
   `TARGET_MET` result is not sensitive to this judgement; the only thing at stake is how the note
   describes the mask.

No fabrication, no stale pin, no off-topic source, no self-made bytes: the S156 provenance chain is
exact end to end.

## 6. Per-row verdicts

| row | (a) verbatim | (b) true, no overreach | (c) attribution | row verdict |
|---|---|---|---|---|
| A7 | holds — line 77 | holds — 41 macro-generated pairs, mask is a real `eRuleProperty` bitmask; caveat: `m_tonemap.second` never written, all 40 per-prop masks write-only | holds, indirect (mask = rule-derived match-property origin; identity absent) | **holds** |
| A8 | holds — line 140 | holds — declaration + `cpp:162` (`emplace_back(effect, rule->getPropertiesMask())`), mask read at `cpp:66-70` | holds, indirect (dynamic-tag provenance record; visible side is A10) | **holds** |

VERDICT: holds — S156's pin resolves to tag v0.56.2 (`efb5099…`), the fresh fetch, the committed
`fetch/S156.bin` and the clone blob are all 9865 B / `sha256:334e1254…`, the row is unmutated since
`cf86f9e0`, and both A7/A8 quotes occur verbatim with true, non-overreaching claims about
rule-property masks; the only defect found is note-prose: the per-property masks are write-only
(40 of 41 properties; `tonemap` none) and line 24's "what it shows" should say "records internally,
never consulted", which does not change either row's standing or C1's target.
