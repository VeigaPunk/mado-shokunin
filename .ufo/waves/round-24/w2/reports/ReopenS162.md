# Reopen S162 — Hyprland ConfigManager.cpp (mined SOURCES row) + claim rows A15, A16

Scope: SOURCES.md row S162 at lane REV 39c596307333b8ca0a1e42b3f3b9a748bb8b208b (round base
8e5d93691e2f7baa3d4a0a61c9428e5acb5d2122), and the two claim rows citing it in
corpus/knowledge/rule-attribution-r24.md: A15, A16. Verification is independent: the pinned raw URL was
fetched this seat, hashed, byte-compared with the committed fetch, and the pin was resolved in the local
clone; each quote and claim was then re-read against the fetched bytes.

Method note: this seat's harness mounts no `lsp` device (`read xd://lsp` → "No such tool … Mounted devices:
ast_edit, debug"), so no semantic definition/reference trace was possible. The assigned question is
byte-level (quote-in-bytes, sha256, pin), so literal comparison is the correct instrument here; it is not
presented as semantic proof of Hyprlang behaviour. Both the row and note are byte-identical at REV and at
current HEAD (`git diff --stat REV -- corpus/SOURCES.md corpus/knowledge/rule-attribution-r24.md` → empty).

## 1. Row record (SOURCES.md:174 at REV)

| field | value |
|---|---|
| id | S162 |
| source | Hyprland ConfigManager.cpp |
| URL | https://raw.githubusercontent.com/hyprwm/Hyprland/efb50993780079460b0cbed1363e2166a2de1d9f/src/config/legacy/ConfigManager.cpp |
| kind / tier | code / A |
| scope | Hyprlang-era legacy windowrule keyword handlers, named special-category reconstruction, and reload traversal |
| anchor | src/config/legacy/ConfigManager.cpp:419-451,590-623,893-968,2016-2093 @ efb50993780079460b0cbed1363e2166a2de1d9f |
| sha256 (row) | `sha256:9db68cf44048d86557d8a53068dcc40b9bd7347c7d95f38edc501565f65be62b` |
| bytes (row) | 90963 B |
| teaches | "Shows callback parsing, name-keyed category consumption, and local reload call sequence; does not establish Hyprlang block grammar or engine precedence" |
| status / opened / recheck | mined / 2026-10-23 / on-release |
| used-by | corpus/knowledge/rule-attribution-r24.md |

## 2. Independent fetch vs committed bytes vs row metadata

- Fetched the row's exact URL this seat: `curl` → **HTTP 200, 90963 bytes**.
- sha256 of fetched bytes: `9db68cf44048d86557d8a53068dcc40b9bd7347c7d95f38edc501565f65be62b` — **identical to the row's recorded sha256**.
- Byte count: **90963** — identical to the row's `90963 B`.
- Committed fetch `.ufo/waves/round-24/fetch/S162.bin`: sha256 `9db68cf4…65be62b`, 90963 B, and
  `refetch.bin == S162.bin` byte-for-byte (Python full-string compare → `True`). Tracked at both REV and HEAD
  as blob `4f1b11f25f227cca2a3e5b16c8de760b76231bf5` (identical blob at both revisions).
- All four artifacts (row sha256, row bytes, committed fetch, fresh fetch) agree.

## 3. Pin resolution

- URL is pinned to a 40-hex commit (`efb50993780079460b0cbed1363e2166a2de1d9f`), under
  `raw.githubusercontent.com/hyprwm/Hyprland`, satisfying the C1 pin rule.
- Local clone `/fast/scratch/hyaku/mado-r24/src/Hyprland-v0.56.2`: `git cat-file -t` → **commit**;
  `git describe --tags --exact-match` → **v0.56.2**; `git log -1` → `Wed Aug 5 14:13:21 2026 +0000
  [gha] Nix: update inputs`.
- Stronger than existence: `git show efb50993…:src/config/legacy/ConfigManager.cpp | sha256sum` →
  `9db68cf4…65be62b`, 90963 B. The clone blob at the pinned commit equals the fetched upstream bytes, so the
  pin is not merely resolvable but content-consistent with the row's hash.

## 4. Anchor spans re-read (row's `teaches` column)

- `:419-451` — static wrappers `handleWindowrule`, `handleWindowrulev2`, `handleLayerrule`,
  `handleLayerrulev2` ("keyword handlers").
- `:590-623` — `CConfigManager::CConfigManager()`: `// windowrule v3` `addSpecialCategory("windowrule",
  {.key = "name"})` at :591, `addSpecialConfigValue("windowrule", "enable", …)`, same for `layerrule`,
  `reloadRuleConfigs()`, then `registerHandler(&::handleWindowrule, "windowrule", …)`.
- `:893-968` — `addRuleFromConfigKey` / `addLayerRuleFromConfigKey` (name-keyed reconstruction) and
  `reloadRules()` (:946; loop at :950).
- `:2016-2093` — `CConfigManager::handleWindowrule` / `handleLayerrule` (inline keyword parsing into
  `m_keywordRules`; a `CWindowRule` is constructed with no name).
All four spans exist and match the row's `teaches` column; both quotes fall inside a declared span
(:591 ∈ 590-623, :950 ∈ 893-968).

## 5. Per-row judgments

### A15 — "This file declares the special `windowrule` category with `name` as its key."

- quote: `m_config->addSpecialCategory("windowrule", {.key = "name"});`
- **(a) verbatim: holds.** Exact character match in the fetched bytes, and match after whitespace collapse;
  exactly 1 occurrence, at line 591. 4 words (≤25), contains topic word `windowrule`. Claim contains
  backticked `windowrule` and `name`, both present in the quote (claim-anchor clause met).
- **(b) true / no overreach: holds.** The line is a literal `addSpecialCategory("windowrule", {.key =
  "name"})` call inside `CConfigManager::CConfigManager()`, `// windowrule v3`, paired with
  `addSpecialConfigValue("windowrule", "enable", …)`. The claim restates the call's own arguments — it says
  nothing about how Hyprlang interprets `.key`, and the row's `teaches` already disclaims "Hyprlang block
  grammar". Hyprlang headers are not vendored in the clone (`subprojects/` = hyprland-protocols, tracy,
  udis86), so no stronger semantic claim is available here, and none is made.
- **(c) attribution relevance: holds, narrowly.** This is identity-at-config, not generic mechanics: the
  category's key field is the string `name`, i.e. the field by which a block window rule is identified
  (prerequisite for the named-vs-anonymous ordering in A26 and for the note's "which rules exist | config
  bytes only" row). It exposes rule identity; it says nothing about which rule produced an effect, and the
  row does not pretend to.

### A16 — "This loop traverses `windowrule` names returned by the special-category key-list API."

- quote: `for (const auto& name : m_config->listKeysForSpecialCategory("windowrule")) {`
- **(a) verbatim: holds.** Exact character match and whitespace-collapsed match; exactly 1 occurrence, at
  line 950. 7 words (≤25), contains topic word `windowrule`. Claim contains backticked `windowrule`
  (claim-anchor clause met).
- **(b) true / no overreach: holds.** Line 950 is the first loop of `CConfigManager::reloadRules()`, whose
  body calls `addRuleFromConfigKey(name)` for each name (and the analogous `layerrule` loop at :955). The
  claim asserts only traversal of names from `listKeysForSpecialCategory("windowrule")`; it does not assert
  what the body does, so it does not overreach. (The body's reconstruction is real, but stays unclaimed.)
- **(c) attribution relevance: holds, narrowly — thinnest of the two.** The quoted line alone shows only a
  loop header; its attribution content is the object: `windowrule` **names** enumerated at reload, i.e. the
  config-side identity channel by which declared rules are addressable. It is identity machinery, not
  generic mechanics (compare A1's rule storage, which is generic), but it carries no effect→rule content.
  The note's own use is correctly scoped ("block rules are keyed by `name` (A15, A16)", the "which rules
  exist" row), so no overreach occurs at note level either.

## 6. Note-level observation (not a row failure)

- rule-attribution-r24.md:73 reads "inline `windowrule = …` lines are registered unnamed, block rules are
  keyed by `name` (A15, A16). Source: ScoutAttributionSweep (`legacy/ConfigManager.cpp:2019`)." A15/A16
  support the second half only. The first half is nonetheless true and covered by the same S162 row inside
  its declared span: `CConfigManager::handleWindowrule` (:2016-2050) constructs `CWindowRule` with no name
  (default arg `name = ""`, WindowRule.hpp:52), pushing it to `m_keywordRules`. So the sentence is sound and
  the sweep citation at :2019 is correct; only the `(A15, A16)` cross-ref, if read as covering both halves,
  is imprecise. Worth a one-line tightening at most; it does not make either row false.
- Neither A15 nor A16 supports "which rule produced an effect"; the note never uses them for that (its
  answer table assigns them to "which rules exist"). The two rows are the weakest attribution payload in the
  26-row set, but they occupy the identity half the note explicitly claims and are honestly scoped.

## 7. Verdict

VERDICT: holds — S162's pinned URL re-fetches to exactly the recorded content (SHA-256
`9db68cf44048d86557d8a53068dcc40b9bd7347c7d95f38edc501565f65be62b`, 90963 B), byte-identical to
`.ufo/waves/round-24/fetch/S162.bin` and to the clone blob at commit `efb50993…`, which resolves as tag
v0.56.2. A15 holds on (a), (b) and (c); A16 holds on (a), (b) and narrowly on (c) (identity-at-config only),
with the note's prose cross-ref at :73 noted as a minor imprecision that does not falsify either row.

## 8. Residual risks / untested

- No `lsp` device in this seat; definition/reference tracing of `addSpecialCategory` /
  `listKeysForSpecialCategory` was not possible. Hyprlang is an external dependency (not vendored), so its
  `.key` semantics are unverifiable from these bytes; A15 as worded does not depend on them.
- Pin resolved in the local clone, not by remote `git ls-remote`; a force-push removing this tagged commit is
  untested (low risk: it is the v0.56.2 release tag). `git ls-remote` would not have shown a non-tip commit
  anyway.
- The frozen C1 counter was not re-run by this seat (out of scope; wave-1 receipt
  `.ufo/waves/round-24/c1/` covers counted mode). The manual (a) check here is independent evidence, not a
  counter run.
- No tool installs or updates made this seat (curl, git, coreutils, python3 pre-existing).
