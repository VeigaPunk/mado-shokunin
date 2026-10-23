# Round 24 wave 1 — wiki window rules source-opener

## Verdict and gate

Pinned wiki bytes fetched successfully. Four proposed claim rows passed the local quote, topic-word, word-count, and anchor checks below. This is one source and four proposed rows only; C1's aggregate target (at least six passing rows from at least three sources, plus the indexed note) is not evaluated or met by this seat alone. The frozen C1 counter was not run, and no row here is represented as an integrated `PASS_ROW`.

## Findings

### Observation — pinned page

The page documents `hl.window_rule()` syntax with an optional `name`, a `match` table, and an `effect` field (lines 6–15). Its matching-property table includes `class`, `title`, `tag`, workspace, focus, fullscreen, and other fields (22–44). It says static effects are evaluated once when a window opens and describes `initialTitle`/`initialClass` matching (63–64); dynamic effects are re-evaluated when a property changes (132–134, 315–316).

The page says window tags can be static or dynamic, dynamic tags use a `*` suffix, and `hyprctl clients` checks window tags (229–238). It distinguishes the static-tag dispatcher from the dynamic-tag `tag` window rule and says the dispatcher clears dynamic tags. Effects are processed top to bottom, with the last match taking precedence (315–321).

For naming, the syntax marks `name` optional (9–15); the later section says only named rules can be dynamically changed, enabled, or disabled. `hl.window_rule()` returns a handle, and `is_enabled()` queries its enabled status (328–342).

### Attribution boundary

The page explicitly documents tag inspection with `hyprctl clients` and a named rule handle's enabled-status query with `is_enabled()`. Neither statement identifies which rule produced a particular applied effect. **[INFERENCE]** Those documented observations are not, by themselves, effect-to-rule attribution; treating them as proof of the originating rule would overreach these bytes. Host behavior remains **[UNK]**.

A whole-file focused search used `functions.grep` on the fetched bytes with the case-insensitive pattern `(?i)hyprctl|applied|which.{0,20}rule|rule.{0,20}(applied|effect|name)|getprop|is_enabled`. Relevant output was:

```text
232:Dynamic tags have a suffix of `*`.
*233:Check window tags with `hyprctl clients`.
235:To add a static tag, use `hl.dsp.window.tag` dispatcher.
236:To add a dynamic tag, use `tag` window rule.
*243:hyprctl dispatch 'hl.dsp.window.tag({ tag = "+code" })' # Add tag to current window.
*244:hyprctl dispatch 'hl.dsp.window.tag({ tag = "-code" })' # Remove tag from current window.
*245:hyprctl dispatch 'hl.dsp.window.tag({ tag = "code" })'  # Toggle the tag of current window.
*248:hyprctl dispatch 'hl.dsp.window.tag({ tag = "+music", window = "class:Celluloid" })'
*342:myRule:is_enabled()        -- query status
```

The query produced no matching line for its `applied`, `getprop`, or `which...rule` alternatives. This is a scoped search of this page, not a claim about other upstream documentation or runtime interfaces.

## Proposed claim rows (provisional source id)

| A1 | The documented `hl.window_rule` syntax shows optional `name`, `match`, and `effect` fields. | S? | "hl.window_rule({ name? = string, match = { prop = some_prop_value, }, effect = some_effect_value, })" |
| A2 | The wiki says effects marked as _dynamic_ are re-evaluated whenever the matching property of the window changes. | S? | "Effects marked as _dynamic_ are re-evaluated whenever the matching property of the window changes." |
| A3 | The wiki states effects are processed top to bottom, and the _last_ match takes precedence. | S? | "Effects are processed top to bottom, and the _last_ match takes precedence." |
| A4 | The page states dynamic tags have a suffix of `*` and tells readers to check window tags with `hyprctl clients`. | S? | "Window tags can be static or dynamic. Dynamic tags have a suffix of `*`. Check window tags with `hyprctl clients`." |

## Provisional SOURCES row

| S? | Window Rules — https://raw.githubusercontent.com/hyprwm/hyprland-wiki/c66e8de21f5ecdc4bc5e278e7d94800ea10957af/content/configuring/core/rules/window-rules.md | docs | A | Window-rule syntax, matching props, effects, tags, order, and named-rule handles | content/configuring/core/rules/window-rules.md:6-15, 22-44, 63-64, 132-134, 229-238, 315-342 @ c66e8de21f5ecdc4bc5e278e7d94800ea10957af, sha256:9ecff146ada23ba11f44b0ddbda15bf82bb3b32bcec29f98388466def101ed95, 16200 B | Documents declaration and match syntax, static/dynamic effects, ordering, tag inspection, and named-rule enablement/status | mined | 2026-10-23 | on-release | corpus/knowledge/rule-attribution-r24.md |

## Commands and evidence

Fetch command:

```sh
timeout 45s curl -fsSL 'https://raw.githubusercontent.com/hyprwm/hyprland-wiki/c66e8de21f5ecdc4bc5e278e7d94800ea10957af/content/configuring/core/rules/window-rules.md' -o '/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-24/fetch/w1/MadoR24.WikiWindowRules-1.bin' && sha256sum '/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-24/fetch/w1/MadoR24.WikiWindowRules-1.bin' && wc -c '/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-24/fetch/w1/MadoR24.WikiWindowRules-1.bin'
```

Output:

```text
9ecff146ada23ba11f44b0ddbda15bf82bb3b32bcec29f98388466def101ed95  /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-24/fetch/w1/MadoR24.WikiWindowRules-1.bin
16200 /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-24/fetch/w1/MadoR24.WikiWindowRules-1.bin
```

The exact local validation command checked whitespace-collapsed quote membership in the decoded fetched bytes, the frozen C1 topic regex, quote length, claim length, and the C1 four-word/backticked-identifier anchor logic:

```sh
timeout 30s python3 -c 'import pathlib,re; p=pathlib.Path("/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-24/fetch/w1/MadoR24.WikiWindowRules-1.bin"); text=re.sub(r"\s+"," ",p.read_bytes().decode("utf-8")).strip(); rows=[("syntax","The documented `hl.window_rule` syntax shows optional `name`, `match`, and `effect` fields.","hl.window_rule({ name? = string, match = { prop = some_prop_value, }, effect = some_effect_value, })"),("dynamic","The wiki says effects marked as _dynamic_ are re-evaluated whenever the matching property of the window changes.","Effects marked as _dynamic_ are re-evaluated whenever the matching property of the window changes."),("ordering","The wiki states effects are processed top to bottom, and the _last_ match takes precedence.","Effects are processed top to bottom, and the _last_ match takes precedence."),("tags","The page states dynamic tags have a suffix of `*` and tells readers to check window tags with `hyprctl clients`.","Window tags can be static or dynamic. Dynamic tags have a suffix of `*`. Check window tags with `hyprctl clients`.")]; topic=re.compile(r"\b(?:window ?rules?|windowrules?(?:v2)?|layerrules?|rules?|getprop|props?|tags?|match(?:es|ing)?)\b",re.I); collapse=lambda x: re.sub(r"\s+"," ",x).strip();
for name,claim,quote in rows:
 w=collapse(quote).lower().split(); c=collapse(claim).lower(); anchored=any(" ".join(w[i:i+4]) in c for i in range(len(w)-3)) or any(len(t)>=4 and t in quote for t in re.findall(r"`([^`\s]+)`",claim)); print(f"{name}: quote_words={len(w)} <=25={len(w)<=25} quote_exact={collapse(quote) in text} topic={bool(topic.search(quote))} claim_words={len(c.split())} >=8={len(c.split())>=8} anchor={anchored}")'
```

Output:

```text
syntax: quote_words=15 <=25=True quote_exact=True topic=True claim_words=11 >=8=True anchor=True
dynamic: quote_words=14 <=25=True quote_exact=True topic=True claim_words=17 >=8=True anchor=True
ordering: quote_words=12 <=25=True quote_exact=True topic=True claim_words=15 >=8=True anchor=True
tags: quote_words=20 <=25=True quote_exact=True topic=True claim_words=20 >=8=True anchor=True
```

## Touched surfaces, limits, and scope

- Created source receipt: `.ufo/waves/round-24/fetch/w1/MadoR24.WikiWindowRules-1.bin`.
- Created this report: `.ufo/waves/round-24/w1/reports/WikiWindowRules.md`.
- No product code, `corpus/SOURCES.md`, knowledge note, wiki clone, or host configuration was changed. No packages/tools were installed; no host commands or compositor operations were run.
- No frozen counter, build, test, lint, or runtime check was run. The four local quote checks are evidence only for these proposed rows; they do not substitute for the counted-mode C1 counter or main integration.
- Provenance is the pinned raw wiki file at commit `c66e8de21f5ecdc4bc5e278e7d94800ea10957af`; this source does not establish behavior on the running host.
