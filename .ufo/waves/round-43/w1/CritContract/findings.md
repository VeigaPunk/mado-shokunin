# CritContract — C1 contract vs the real compositor: ambiguities, overclaims, misclassified rule forms

Seat: `CritContract` (leaf, round 43 wave w1). Target: the frozen C1 contract, i.e. the docstring of
`quality/counters/c1-r42-geometry.py` (sha256 `ed78d693…`) "restated … the code below being the same
sentence", with the reference `.ufo/waves/round-42/c1/ctl-ref-tool.py.txt` (sha256 `e3c2e471…`).
Read against the lane's pinned Hyprland 0.56.2 sources (`fetch/S290-S296`, `receipts/fetch-sha256.txt`),
the host's own config bytes, and the upstream 0.56.2 legacy parser at the same commit
(`efb50993780079460b0cbed1363e2166a2de1d9f`; seat-fetched, **not** lane pins — `receipts/upstream-cites.txt`).

Everything below was re-derived here. Quotes are ≤ 25 words, located, and checked against
`receipts/` by `check-quotes.py` (output `receipts/check-quotes.txt`). Severities: HIGH = can produce a
false `AGREE` (the verdict that claims capability) or silently drop a real rule; MEDIUM = wrong model for
valid configs; LOW = ambiguity or classification-granularity; EDITORIAL = wording.

## Summary

| # | Sev | What | Contract location | Decided by |
|---|---|---|---|---|
| F1 | HIGH | grammar demands effect-first, exactly two fields; legacy parser is order-free with any number of props/effects | contract:31-35 | **no** — and the contract's reading is wrong for valid host grammar |
| F2 | HIGH | "a tiled window never reads it" — the applicator reads and stores the rule for every matching window | ref:5-6, contract:46-47 | pinned source contradicts it |
| F3 | MED | "Rules apply in file order" — two readings; compositor order is named-first, keyword-in-parse-order | contract:44-45 | **no** fixture (order0 only orders its own argv) |
| F4 | MED | class-control-character guard is not RE2 behaviour, placed as if it were | contract:38-39 | ctlclass0 decides the tool reading, against the compositor |
| F5 | MED | space/tab runs as separators; the regex starts after the run — compositor splits at the first literal space | contract:29-30, 33-34 | space0 decides the tool reading, against the compositor |
| F6 | LOW/MED | no inline `#` comment handling (hyprlang strips it; docs' own examples carry trailing comments) | contract:26-29 | no fixture; host writes full-line comments only |
| F7 | LOW | `unsupported` conflates malformed lines with well-formed size rules the class join cannot use | contract:36-37 | host writes such rules (pip/system/steam) |
| F8 | LOW | two boundary sentences with two readings and no deciding fixture (1048577-byte stdin; repeated `--rules`) | contract:21, 16 | **no** |
| F9 | EDITORIAL | "the first / first token" duplicated across the line break | contract:29-30 | ref:29 has it once |

---

## F1 — HIGH — the rule grammar is narrower than the legacy parser (order and arity)

**Contract quote.** "it has exactly two fields; field 0 has exactly two argument tokens" and "field 1
fully matches `match:class[ \t]+(.+)`" (contract:31-35; same sentence at ref:30-33).

**What the compositor does.** `CConfigManager::handleWindowrule` splits the value on `,` and classifies
each element by `el.starts_with("match:")`: every element is either a prop or an effect, and the loop
accepts any number of each, in any order (`ConfigManager.cpp:2016-2050`, line 2030 is the `FIRST_IS_PROP`
test). The 0.54 page (the legacy-syntax page the current wiki points to) states it: the anonymous syntax
example is `windowrule = match:class my-window, border_size 10`, and "You can have as many props and
effects per rule as you please, in any order as you please" (`docs-cites.txt`). The host itself writes the
order-free form: `~/.config/hypr/input.conf:45` is `windowrule = match:class (Alacritty|kitty|foot),
scroll_touchpad 1.5`, and `~/.local/share/omarchy/default/hypr/apps/steam.conf:6` carries two props
(`match:class steam, match:title Steam`) — `receipts/host-rules.txt`.

**Impact (measured).** With the frozen reference:
`windowrule = size 420 500, match:class a` followed by `windowrule = match:class a, size 100 100` prints
`want=420x500 … verdict=AGREE` and `other=1` — but Hyprland's last matching size rule is the 100×100 one
(`receipts/ref-cases.txt`, case `false_agree_matchfirst`). The same false `AGREE` comes from a multi-effect
line `float on, size 100 100, match:class a` (case `false_agree_multieffect`; `unsupported=1`). A lone
match-first size line prints `NO_SIZE_RULES` (exit 4, `other=1`) although the compositor applies it
(case `match_first`). The contract's own "last matching size rule gives want" is therefore not the last
matching rule once a real host-grammar line is in the file.

**Amendment (Rules paragraph).** Split the body on `,`; each field is a prop iff it starts with `match:`
(the prop name is the text up to the first space, the value is the rest, verbatim), otherwise an effect
(name up to the first space, arguments the rest). Props and effects may appear in any order, any number,
at most one of each type (a repeat makes the line `unsupported`). A line is class-joinable iff it has
exactly one prop and it is `match:class`; every `size` effect with two `[0-9]{1,5}` tokens and every
`float` effect with `on`/`off` is a supported rule of that effect, in field order, and a line carrying both
yields two supported rules. A size/float effect failing these tests, or a prop other than `match:class`,
adds one to `unsupported`. New fixtures: `matchfirst0`, `multieffect0`.

## F2 — HIGH — "a tiled window never reads it" is false at the applicator

**Contract quote.** "a tiled window never reads it" (ref:5-6; the counter restates only the verdict
"TILED (not floating)", contract:46-47).

**What the source shows.** `CWindowRuleApplicator::readStaticRules` loops over every window rule that
matches the window and calls `applyStaticRule` with **no floating test**
(`WindowRuleApplicator.cpp:483-509`); the size effect writes `static_.size = expr`
(`:421-428`); `recheckStaticRules` re-applies static rules on property changes, again without a floating
test (`:526-543`). The only consumer in the pinned set is the default floating algorithm's first-map
branch, `if (target->window() && target->window()->m_firstMap)` (`DefaultFloatingAlgorithm.cpp:51-66`);
`grep static_\.size` over the seven pinned files hits only `:55-58` of that file (`receipts/pinned-cites.txt`).

**Impact.** The sentence is the kind of claim the C2 entry will want to copy; it overstates "never reads"
(reads and stores always, consumes only in the floating first-map path). It also hides the first-map
scope: a window floated after mapping takes `lastFloatingSize`, not the rule.

**Amendment.** "The applicator records a matching `size` rule's expression on every window, tiled or
floating; the only consumer in these sources is the default floating algorithm's first-map branch
(`static_` is read there), so a tiled window stores the rule and gets no geometry from it, and a window
floated after its first map keeps `lastFloatingSize`." Keep the TILED verdict as is. If the C2 entry
repeats the old sentence, the C2 clause check should reject it.

## F3 — MEDIUM — "Rules apply in file order": two readings, and the compositor's order is not file order

**Contract quote.** "Rules apply in file order: the last matching `size` rule gives want"
(contract:44-45).

**Two readings.** (a) the tool's `--rules` argument order (what the judge's model does); (b) the order the
compositor registers rules, i.e. the config tree's `source=` expansion order. The contract never says which.

**What the source shows.** `CRuleEngine::registerRule` appends (`Engine.cpp:14-15`) and `rules()` returns
that vector (`:54-55`); the applicator's last write wins (`WindowRuleApplicator.cpp:492-509`). But
`CConfigManager::reloadRules` registers **all** named `windowrule { … }` blocks first, then all keyword
`windowrule = …` lines in parse order (`ConfigManager.cpp:946-963`), and parse order follows `source=`
including a glob on this host (`~/.config/hypr/hyprland.conf:4-32`, glob at `:23`) —
`receipts/upstream-cites.txt`, `receipts/host-rules.txt`.

**No decider.** `order0` passes three files in the order the test intends and never models a config tree,
a named block, or a `source=` expansion (`quality/counters/c1-r42-geometry.py:709`).

**Impact.** A multi-file invocation can join against a different "last rule" than the compositor, and a
config that uses the named block form is invisible to the tool while being authoritative in the compositor.

**Amendment.** "Rules apply in the order given on the command line; this equals the compositor's order
only for `windowrule =` keyword lines read in `source=` expansion order. Hyprland registers named
`windowrule { … }` blocks before all keyword rules; this tool parses no named block and expands no
`source=`. A caller passing files in another order joins against a different last rule." (Optionally add a
`named-rule` fixture that must land in `unsupported`/be documented as unparsed.)

## F4 — MEDIUM — the class guard diverges from `RE2::FullMatch` while sitting next to it

**Contract quote.** "its class holds no character below U+0020 and `re.fullmatch(REGEX, class)` succeeds"
(contract:38-39).

**What the source shows.** The matcher is `re2::RE2::FullMatch(other, *m_regex) != m_negative`
(`RegexMatchEngine.cpp:16`). RE2's `.` is "any character, possibly including newline (s=true)"
(`receipts/upstream-cites.txt`, RE2 syntax doc line 5), i.e. by default every character except `\n`; Python `re`'s `.` has the same default.
So a class containing `\t`, `\r`, `\x01` **does** match `.` in both engines, and the guard is not an
agreement aid: it makes the tool disagree with the compositor. `ctlclass0` locks the guard in: classes
such as `"a\tb"` against rule `a.b` must not match (`quality/counters/c1-r42-geometry.py:748-750`).

**Impact.** A client whose class holds a C0 control (or any class a rule with `.` would match) is reported
unmatched — `NO_MATCHING_CLIENT`, exit 3 — where the compositor applies the rule.

**Amendment.** Delete the guard: "A client MATCHES a rule when `re.fullmatch(REGEX, class)` succeeds
(Hyprland: `RE2::FullMatch`; for this alphabet and `.` the two agree — both exclude only `\n`)." Then
change `ctlclass0`'s expectations. If the guard is kept, it must be stated as a deliberate conservative
restriction and the `RE2::FullMatch` parenthetical moved away from it.

## F5 — MEDIUM — space/tab runs vs the compositor's first literal space

**Contract quote.** "tokens being separated by runs of spaces and tabs only" (contract:29-30) and
"matches `match:class[ \t]+(.+)`, the capture being REGEX" (contract:33-34).

**What the source shows.** `handleWindowrule` requires a literal space in every field:
`spacePos = el.find(' ')`, and `if (spacePos == std::string::npos) return "invalid field … missing a
value"` (`ConfigManager.cpp:2026-2030`); the value is `el.substr(spacePos + 1)` — everything after the
**first** space, verbatim. Elements are trimmed only at their edges (`VarList2.cpp:67,78`).
Consequences the contract gets wrong in both directions:
(a) a tab-separated field is invalid in Hyprland but supported by the tool — the reference prints
`rules=1 … verdict=DIFFER` for `windowrule\t=\tsize\t1\t2\t,\tmatch:class\ta` (case `tab_separated`),
while Hyprland rejects the line;
(b) two spaces after `match:class` put a leading space **into the regex** in Hyprland (the rule then matches only a class
that begins with a space), but the tool swallows the run and matches — reference prints `AGREE` for
`match:class  ^(org.omarchy.gkeep)$` (case `double_space_after_match`).
`space0` locks in the tab reading (`quality/counters/c1-r42-geometry.py:683`).

**Impact.** Another route to a false `AGREE` (case b) and to a rule the tool thinks exists but the
compositor dropped (case a).

**Amendment.** Replace the run-based tokenisation: split each field at its first literal space; no space →
invalid; the value is the rest verbatim; then the existing alphabet check rejects a regex with an embedded
or leading space (→ `unsupported`) instead of normalising it away. Update `space0`.

## F6 — LOW/MEDIUM — inline `#` comments

**Contract quote.** "a line is stripped of spaces and tabs at both ends" + "The body is split on ','"
(contract:26-29) — there is no comment step.

**What the source shows.** hyprlang trims the line, then truncates at the first unescaped `#`
(`hyprlang config.cpp:686, 702-716`; `##` becomes a literal `#`). The 0.54 page's own Example Rules carry
trailing comments on rule lines, e.g. `windowrule = no_blur on, match:class firefox   # Disable blur for
firefox` (`docs-cites.txt`).

**Impact (measured).** `windowrule = size 420 500, match:class ^(org.omarchy.gkeep)$ # pinned` →
`unsupported=1`, `NO_SIZE_RULES`, exit 4 (case `inline_comment`), while Hyprland applies it. The host today
writes only full-line comments (`gkeep.conf:1`), which the tool correctly ignores —
`receipts/host-rules.txt`.

**Amendment.** "Before the field split, delete the first unescaped `#` and the rest of the line, turning
each `##` into a literal `#`; a line that becomes empty is ignored." Add `inlinecomment0`.

## F7 — LOW — `unsupported` conflates "malformed" with "real size rule outside the join"

**Contract quote.** "Any other size or float line adds one to `unsupported`." (contract:36-37)

**Host-grounded instances** (`receipts/host-rules.txt`): `pip.conf:6` `windowrule = size 600 338,
match:tag pip`; `system.conf:4` `windowrule = size 875 600, match:tag floating-window`;
`steam.conf:6-7` (class+title). These are live size rules for other windows that the class join cannot
attribute; the legacy effects table says the size effect takes two expressions — "Resizes a floating window to a
given size. Two expressions are space-separated." (`docs-cites.txt`).

**Impact.** On a config whose only size rules are tag/expression/class+title rules, the tool prints
`NO_SIZE_RULES` (exit 4) — which reads as "no size rules exist" — and the same `unsupported` bucket holds
real syntax errors. For the gkeep invocation nothing changes (`unsupported=0`), so this is not a
false-AGREE risk, only a misleading summary.

**Amendment.** Either split the counter (`outsider=<n>` for well-formed size/float lines the class join
cannot attribute, `unsupported=<n>` for malformed), or state: "`unsupported` also counts well-formed size
or float lines this tool cannot attribute; `NO_SIZE_RULES` means no class-joinable size rule."

## F8 — LOW — two boundary sentences with two readings and no deciding fixture

**(i) stdin bound.** Contract: "an input larger than 1048576 bytes is too_large" + "at most 1048577
bytes" (contract:20-21). The reference makes a 1048577-byte stdin `too_large` (`len > MAX_BYTES`), but the
sentence invites reading 1048577 as accepted. `stdinbig0` feeds 1048578 bytes
(`quality/counters/c1-r42-geometry.py:515-519`), so the exact boundary is untested. **No decider.**
Amendment: "a clients input of more than 1048576 bytes is too_large (stdin is read up to 1048577 bytes,
and a read of 1048577 bytes is too_large)."

**(ii) repeated `--rules`.** Contract: "`--rules V` one or more times" (contract:16). The reference
processes the same path twice — `rules=2` for two `--rules` flags on one file (case `duplicate_rules`) —
but no sentence and no fixture says whether duplicates are kept or deduped. **No decider.** Amendment:
"a repeated `--rules` path is read and numbered again, in argument order."

## F9 — EDITORIAL — duplicated word in the frozen restatement

"The effect is the first" / "first token of field 0" (contract:29-30) duplicates `first` across the line
break; the reference has it once (ref:29). Harmless for implementers, but the v2 restatement should read
"The effect is the first token of field 0". (The frozen file itself must not be edited.)

---

## Checked and confirmed (so the v2 author does not chase them)

- **`windowrulev2` ignored is correct.** The contract says `windowrulev2` lines are "ignored and counted
  nowhere" (contract:28). 0.56.2 registers `windowrulev2` as a handler that returns an error
  (`ConfigManager.cpp:431-435`), so such a line produces no rule; ignoring it matches the compositor
  (inert either way).
- **Full-line comments.** A line starting with `#` does not match `RULE_RE` and hyprlang parses it as a
  comment; both ignore it (`gkeep.conf:1`).
- **The host's actual gkeep line is the shape the contract accepts.** `gkeep.conf:4` is
  `windowrule = size 420 500, match:class ^(org.omarchy.gkeep)$`; the reference prints
  `arg=420x500 … AGREE` for a floating class client (case `baseline_effect_first`). The gkeep window is
  not open (`fetch/host-clients-r43.json`: 4 clients, all tiled), so no live join exists; this is the contract's happy path.
- **Last match wins for keyword lines in one file** is supported: registration order
  (`Engine.cpp:14-15,54-55`) + overwrite in `applyStaticRule` (`WindowRuleApplicator.cpp:421-428`,
  `:492-509`). The defect is only in the *file-order* sentence (F3), not in "last matching".
- **Reported client size is the animation goal.** `getWindowData` prints
  `w->size(GEOMETRIC_GOAL)` and `position(GEOMETRIC_GOAL)` (`HyprCtl.cpp:427-428`, `:448`) and `floating`
  is `m_isFloating` (`:429`). The contract's "the size the compositor reports" is accurate; if the C2
  entry or the tool's docstring names the field, it is `GEOMETRIC_GOAL` (the goal, not the current
  animated value).
- **`re.fullmatch` vs `RE2::FullMatch`** for the restricted alphabet is a fair equivalence
  (`RegexMatchEngine.cpp:16`); the `negative:` prefix is outside the alphabet and therefore
  `unsupported` — conservative, and consistent with the declared residual.
- **The counter's `int()` normalisation of size args** (`00420` → `arg=420x500`) is decided by `size0`
  (`quality/counters/c1-r42-geometry.py:660`) and is not ambiguous in practice.

## Residual of this review (not claimed)

- `CWindowRule::matches` guards on `canMatch()` (`WindowRule.cpp:376-379`); its body (WindowRule.hpp) was
  not fetched, so "a rule with no props is inert" is inferred from that guard plus the docs' "at least one
  prop", not read.
- hyprlang's `trim` (used at `config.cpp:686`) comes from hyprutils; its CR handling was not verified, so
  CRLF configs are not assessed (the host writes LF, `receipts/host-rules.txt`).
- `escapeJSONStrings`' treatment of control characters in `hyprctl clients -j` was not read; the F4 point
  is about `RE2::FullMatch`, not about whether real output could be invalid JSON.
- Named `windowrule { … }` blocks are absent from this host; F3's ordering point is source-level.
