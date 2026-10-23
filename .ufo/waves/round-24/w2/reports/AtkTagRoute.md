# AtkTagRoute — attack on the note's tag-route recommendation

**Attacked:** `corpus/knowledge/rule-attribution-r24.md:22`, the answer-table row

> `| which rule fired on a window | **tag route**: give the rule a unique `tag` effect, then read `tags` in `hyprctl clients` (A10, A22) | the tag set the applicator's tag keeper holds (A9, A10) | provenance when two rules add the same tag; dynamic tags carry a `*` suffix (A22) |`

and its limits cell. Assignment: from the v0.56.2 source and the pinned wiki — does a static `tag`
effect from a rule reach `hyprctl clients` `tags` (HyprCtl `getTagsData`, `CTagKeeper`, `applyTag`);
how do dynamic tags (`*`) and removal behave; can two rules' tags be told apart.

**Evidence base.** Hyprland clone at `efb50993780079460b0cbed1363e2166a2de1d9f` (rev-parse verified =
the pin); hyprland-wiki clone at `c66e8de21f5ecdc4bc5e278e7d94800ea10957af` (rev-parse verified = the
S165 pin); committed fetch bytes `S155.bin`/`S158.bin`/`S165.bin` re-opened at the cited lines; a fresh
fetch of `src/helpers/TagKeeper.cpp` from the pinned commit
(sha256:`9c2507e2f1d8a5c5ca1afb28c66cb09540555ea182b5d7bfaacd66ef7b6ab9ef`) is byte-identical to the
clone file; a harness compiled from that exact file. I ran no C1 counter and edited no lane file.

## What the source actually does

1. **There is no static tag effect from a rule.** `WINDOW_RULE_EFFECT_TAG` sits in the *dynamic* block
   of the enum (`WindowRuleEffectContainer.hpp:32-40`, tag at `:40`). `applyStaticRule` has no TAG
   case — TAG falls into its `default:` branch and is skipped with a TRACE line "Skipping effect …,
   not static" (`WindowRuleApplicator.cpp:378-386`). Only `applyDynamicRule` handles it
   (`:161-165`): `m_dynamicTags.emplace_back(effect, rule->getPropertiesMask()); m_tagKeeper.applyTag(effect, true);`.
   `effect` is `effectData.raw` (`:86`), the verbatim effect string from config (prefix included;
   `RuleWithEffects.hpp:22-30`, `ConfigManager.cpp:2017-2047`). The pinned wiki says the same:
   "To add a dynamic tag, use `tag` window rule" and "The `tag` rule can only manipulate dynamic tags"
   (`S165.bin:236,238`).
2. **`applyTag` makes `*` and interprets prefixes** (`TagKeeper.cpp:10-38`): with `dynamic=true` it
   appends `*` unless the string already ends in `*`; then `-x` erases, `+x` inserts if absent, bare
   `x` **toggles** (`setTag = !isTagged(tagReal, true)`). So every rule tag is stored as `<value>*`.
3. **`clients` prints the keeper set as-is.** `getTagsData` folds `m_tagKeeper.getTags()` into
   `"a", "b"` (no brackets, no escaping) inside `"tags": [{}]` (`HyprCtl.cpp:346-353`, format `:415`,
   arg `:433`). The keeper is a `std::set<std::string>` (`TagKeeper.hpp:13`), so output order is
   lexicographic, not rule order.
4. **Application and normalization.** `readStaticRules` clears static state, then calls
   `applyDynamicRule` for every matching non-exec rule (`WindowRuleApplicator.cpp:483-514`, call
   `:507`) and does **not** reset tags. It runs once on the initial commit (`Window.cpp:2718-2726`) and
   on every map (`Window.cpp:2052`, call `:2277`). But `mapWindow` later runs
   `propertiesChanged(RULE_PROP_ALL)` unconditionally (`Window.cpp:2497`; no `return` between `:2278`
   and `:2496`), and `propertiesChanged` (`:547-590`) is a reset-then-reapply: `resetProps` erases the
   `m_dynamicTags` entries whose recorded mask intersects the changed props and calls
   `removeDynamicTag(el.first)` (`:66-72`), then matching rules are re-applied. The same full reset
   runs from `updateAllRules` (`Engine.cpp:34-45`, all mapped windows, `RULE_PROP_ALL`).
5. **Removal is exact-match on `raw + "*"`, but the keeper holds the prefix-stripped string**
   (`TagKeeper.cpp:50-52`). Hence bare `term` is removed by `removeDynamicTag("term")` → `"term*"`,
   while `+term` is *not* removed by `removeDynamicTag("+term")` → it looks for `"+term*"`, which never
   exists. Bare tags therefore track the match; `+` tags become latches.
6. **The tag dispatcher is a different namespace.** `Actions::tag` calls `applyTag(tagStr, dynamic=false)`
   (`ConfigActions.cpp:633-641`), so it can create a bare static tag, or — spelled `"+term*"` — a
   string byte-identical to a rule tag. `TagMatchEngine` matches non-strict (`isTagged(tag)`, default
   `strict=false`), so `tag:term` matches `term*` (`TagMatchEngine.cpp:11-12`).

## Harness (real `TagKeeper.cpp` from the pin, no compositor)

Built and run in `/fast/scratch/hyaku/mado-r24/w2/tagroute/`:

```
g++ -std=c++20 -O0 -I <clone>/src/helpers harness.cpp <clone>/src/helpers/TagKeeper.cpp -o harness
```

The harness models the exact call sequences of `readStaticRules` (`applyTag(raw, true)`) and
`propertiesChanged` (`removeDynamicTag(raw)` then `applyTag(raw, true)`) per the call sites above.
Sources and outputs: `harness.cpp` sha256:`02ded236…`, binary sha256:`5f50af27…`, output
sha256:`afdc9f5e…`.

| # | sequence | keeper after |
|---|---|---|
| 1 | bare `term`, initial-commit read | `["term*"]` |
| 2 | bare `term`, map read (before the tail reset) | `[]` |
| 3 | bare `term`, map read **+ tail reset/reapply** | `["term*"]` |
| 4 | bare `term`, remap + tail reset/reapply | `["term*"]` |
| 5 | `+term` applied three times | `["term*"]` |
| 6 | `+term`, then `removeDynamicTag("+term")` (the `resetProps` call) | `["term*"]` |
| 7 | `+term`, rule stops matching (reset removal no-ops, no reapply) | `["term*"]` (sticky) |
| 8 | bare `term`, then `removeDynamicTag("term")` (rule stops matching) | `[]` |
| 9 | two matching rules, both bare `dup`, after reset/reapply | `[]` |
| 10 | two matching rules, both `+dup`, after reset/reapply | `["dup*"]` |
| 11 | bare `dup` then `+dup` | `["dup*"]` |
| 12 | `+dup` then bare `dup` | `[]` |
| 13 | dispatcher `+term*` vs rule entry `term*` | identical (strict lookup true) |
| 14 | rule `term*`, dispatcher `-term` | `["term*"]` (strict: no removal) |
| 15 | rule `term*`, dispatcher `-term*` | `[]` |
| 16 | rule bare `term` then rule `-term` | `[]` |
| 17 | `isTagged("term")` non-strict / strict against `term*` | `1` / `0` |

## Findings

**F1 — the "static tag" premise fails: a rule tag is never static.** Every rule tag is applied through
the dynamic path and stored with a `*` suffix (1, 2 above; harness row 1). A tag *without* `*` can only
come from the `tag` dispatcher (`hl.dsp.window.tag`, `Actions::tag` with `dynamic=false`). The note's
limits say "dynamic tags carry a `*` suffix" but never state that a rule tag can *only* be dynamic, so
a reader who greps `clients` for the configured string `<unique>` fails — the string is `<unique>*`.
The decisive sentence is in the pinned S165 bytes (`:236`, `:238`) and inside the S165 anchor range
(`:229-238`), but A22's quote stops at `:233`, so the note's own row does not carry it.

**F2 — the effect's form changes its lifecycle, and the note states neither.** Bare `<name>` is a
toggle by definition (2 above). It ends up *accurate* in v0.56.2 only because the applicator normalizes:
each map and every `updateAllRules` reset all dynamic tags and re-apply the matching rules (4 above), so
the harness's reset-then-reapply sequence ends `["term*"]` (rows 3-4). `+<name>` is idempotent but —
because `resetProps` cannot remove the prefixed raw string (5 above) — it is a **latch**: it survives
the rule ceasing to match (row 7). The pinned wiki's own examples use the `+` form
(`S165.bin:296,298`; the effect table at `:178` says "Use prefix `+`/`-` to set/unset, or no prefix to
toggle"). So the note's unspecified "unique `tag` effect" gives "matches now" if the reader writes it
bare, and "matched at least once" if the reader copies the wiki's form. Presence in `tags` means
neither unless the form is stated.

**F3 — two rules' tags are distinguishable only if their effect strings differ; duplicates do worse
than blur provenance.** The note's limit ("provenance when two rules add the same tag") understates
the behaviour. With one matching window and two matching rules sharing a **bare** string, the second
application toggles off what the first added, and the normalization cycle reproduces the same cancel —
the tag is **absent** at steady state (harness row 9). With `+` the two applications merge into one
entry (row 10), and a mixed bare/`+` pair is order-dependent (rows 11-12). Distinct strings do appear
separately, but the keeper is a set: no rule id, lexicographic order, and a rule matching on `tag` can
add a further tag, so "told apart" holds only by construction (you choose unique strings).

**F4 — the `*` suffix is a namespace marker, not provenance, and removal is namespace-strict.** The
dispatcher can mint a byte-identical `term*` (harness row 13; `ConfigActions.cpp:633-641`), so seeing
`term*` does not prove a rule set it. Dispatcher `-term` cannot remove a rule's `term*` (row 14) while
`-term*` can (row 15): the dispatcher's static/`-` namespace is strict-match, and only a rule's
`-term` effect reaches `term*` (row 16). The note mentions none of this.

**F5 — minor: tags are interpolated into JSON unescaped** (`HyprCtl.cpp:349-351` formats `"{}"` with
no `escapeJSONStrings`). A tag containing `"` or `\` makes `hyprctl clients -j` invalid JSON. A route
built on parsing that array should say so.

**F6 — sourcing gap for the route's load-bearing mechanism.** The route's mechanism is
`WindowRuleApplicator.cpp:161-165` plus `TagKeeper.cpp:10-52`. No counted claim row quotes either: A9
is the tag *match* engine, A10 the `clients` read, A22 the wiki suffix sentence. `TagKeeper.cpp` is not
a SOURCES row at all (`grep TagKeeper corpus/SOURCES.md` → no hit), so the toggle/prefix/`*` semantics
the recommendation depends on are outside the note's sourced set. Rows A1-A26 are not displaced by
this (I did not run the C1 counter); the defect is that the prose recommendation outruns its citations.

## What the route actually answers

- With a **unique bare** tag: presence of `"<name>*"` in `clients` means the rule currently matches
  (for a mapped window), because each map, each `updateAllRules`, and every property change that
  touches the rule's match properties reset and re-apply the tag set — **unless** another matching
  rule uses the same bare string, in which case the tag is absent.
- With a **unique `+`** tag: presence means the rule matched at least once since the tags were last
  cleared (`clear_tags`, window destruction, or a rule `-<name>` effect); it is not a live predicate.
- Neither form reports *which* rule produced any other effect, and neither is a rule id.

## Smallest safe correction

Replace the row at `rule-attribution-r24.md:22` with wording that keeps the route but names its form
and its limit:

> | which rule may have matched a window | **tag route**: give the rule `<unique-name>` (no prefix; a *bare* tag tracks the current match) or `+<unique-name>` (a latch), then read `"<unique-name>*"` in `tags` in `hyprctl clients` (A10, A22; source `WindowRuleApplicator.cpp:161-165`, `TagKeeper.cpp:10-52`) | bare: that this rule matches now (mapped window, tag set re-derived at map/reload/prop change); `+`: that it matched at least once since the last clear | rule identity (only your chosen string); anything if a second matching rule uses the same string — bare duplicates cancel, `+` duplicates merge, mixed prefixes are order-dependent; `*` does not prove a rule set it (the dispatcher can mint `<unique-name>*`) |

and add to Limits: rule tags are always dynamic (`<name>*`); bare toggles per application (v0.56.2's
reset-then-reapply at map/`updateAllRules` normally re-derives it); `+` tags survive the rule ceasing
to match because `resetProps` cannot remove the prefixed raw string; `-<name>` on a rule removes
`<name>*`; dispatcher `-<name>` only removes the static tag; `clear_tags` clears both; tag strings are
emitted into `clients` JSON unescaped.

## Impacted axes

- **coverage (C1 artifact):** the note's central route is uncited at its mechanism; `TagKeeper.cpp`
  is absent from SOURCES. The frozen v2 predicate counts rows only, so this is a note-quality finding,
  not a predicate failure.
- **depth:** the decision-table entry cannot be acted on as written — form, suffix, and duplicate
  behaviour are all unstated.
- **calibration:** the limits cell overstates what the reader can conclude from "two rules add the same
  tag" and says nothing about the `+` form's latch semantics.

No host actions ran in this seat (no `hyprctl` call at all, tag values never read), no lane file was
edited, no tool installed or updated, no git/jj write in the lane or fleet repo. Scratch artifacts:
`/fast/scratch/hyaku/mado-r24/w2/tagroute/{harness.cpp,harness,harness.out,TagKeeper.fetched.cpp}`.

VERDICT: partial
