# SrcWindowView — round 24 wave 1 source opener

## Behavior observed

The bytes fetched from the pinned Hyprland commit show `CWindow` holding a `UP<Desktop::Rule::CWindowRuleApplicator>` member. Both XWayland and XDG factory paths create a `CWindowRuleApplicator` for the new window (`Window.cpp:103-108,141-146`). The map path reads `m_ruleApplicator->static_` and applies selected results into window state: monitor/workspace, floating, pseudo, initial-focus, pin, fullscreen, suppressed-event, group, content, size and `noclosefor` state (`Window.cpp:2143-2281,2402-2408`). If `readStaticRules()` requests a recheck, the code rechecks and applies the static properties again (`:2277-2281`).

Other sampled rule-driven values are read from the applicator when updating border colors, active/fullscreen/inactive alpha, dimming and rounding (`Window.cpp:1104-1115,1914-1938`). Metadata handling calls `propertiesChanged` with title/class flags (`:1484-1486`); the map path calls it with `RULE_PROP_ALL` (`:2497`). The header also declares `m_groupRules` as a `uint16_t` initialized to `GROUP_NONE` (`Window.hpp:271-273`), and a `Time::steady_tp m_closeableSince` member under a `noclosefor windowrule` comment (`:283-284`).

The tag-related surface in these two files is narrower than rule-tag attribution: `Window.hpp` includes `TagKeeper.hpp` (:11) and declares `xdgTag()` as an optional-string accessor (:417); its implementation returns the XDG toplevel's `m_toplevelTag` when the surface and toplevel exist (`Window.cpp:1791-1795`). These bytes do not establish how rule matching uses tags. The source retains a typed rule-applicator member, but this opener does not expose the applicator's matching internals or identify a particular matched configuration rule for any applied property. The workspace log text is generic; it is not a rule-source identifier. Host state and host behavior remain [UNK].

## Proposed C1 claim rows

The rows below are proposals using `S?` placeholders; the L1 integrator assigns final source IDs. Each quote is copied from the named fetched bytes. The local Python check below confirmed the whitespace-collapsed quote substring, topic-word, anchor, word-count, and delimiter conditions for each proposed row. This is not a frozen-counter verdict.

| A1 | CWindow declares a `m_ruleApplicator` field with the window-rule applicator type in its object state. | S? | "UP<Desktop::Rule::CWindowRuleApplicator> m_ruleApplicator;" |
| A2 | CWindow declares `m_closeableSince` as `Time::steady_tp` under the `noclosefor` windowrule comment. | S? | "// For the noclosefor windowrule Time::steady_tp m_closeableSince = Time::steadyNow();" |
| A3 | The `GROUP_OVERRIDE` constant's comment says it overrides other rules. | S? | "GROUP_OVERRIDE    = 1 << 6, // Override other rules" |
| A4 | CWindow log text says `Rule workspace matched by` and contains two `{}` placeholders before `applied`. | S? | "Rule workspace matched by {}, {} applied." |
| A5 | CWindow calls `propertiesChanged` with the title-specific `RULE_PROP_TITLE` rule-property flag. | S? | "m_ruleApplicator->propertiesChanged(Desktop::Rule::RULE_PROP_TITLE" |
| A6 | CWindow sets `m_groupRules` to `GROUP_OVERRIDE` after the comment says Clear existing rules. | S? | "// Clear existing rules m_groupRules = Desktop::View::GROUP_OVERRIDE;" |

## Proposed SOURCES rows

Draft-only, not written to `corpus/SOURCES.md`. The L1 integration message reserves final IDs from S153 onward.

| S? | Hyprland v0.56.2 CWindow declaration — https://raw.githubusercontent.com/hyprwm/Hyprland/efb50993780079460b0cbed1363e2166a2de1d9f/src/desktop/view/Window.hpp | code | A | CWindow rule-applicator member, group flags/state, noclosefor state, and xdgTag API | src/desktop/view/Window.hpp:11,50-60,235-236,271-284,417 @ commit efb50993780079460b0cbed1363e2166a2de1d9f, sha256:1f60b8ff0bc6b5a48af5c03cb2cac1108db677efc70b4424b56ef6f1f2d1cc81, 23988 B | CWindow's rule-applicator member and selected local state are declared; the xdgTag accessor is distinct from a demonstrated matched-rule identifier | mined | 2026-10-23 | on-release | corpus/knowledge/rule-attribution-r24.md |
| S? | Hyprland v0.56.2 CWindow implementation — https://raw.githubusercontent.com/hyprwm/Hyprland/efb50993780079460b0cbed1363e2166a2de1d9f/src/desktop/view/Window.cpp | code | A | CWindow applicator construction, static-rule application, and property-change hooks | src/desktop/view/Window.cpp:103-108,141-146,1484-1486,1791-1795,2143-2281,2497 @ commit efb50993780079460b0cbed1363e2166a2de1d9f, sha256:d735d454cc4b7983f19626514d310669047da46780c509ffae68ccf072211ded, 124226 B | Static applicator results feed window state, and propertiesChanged is called with property flags; the source does not identify a particular originating config rule | mined | 2026-10-23 | on-release | corpus/knowledge/rule-attribution-r24.md |

## Commands and receipts

Pins were supplied by the round registration: Hyprland v0.56.2 at commit `efb50993780079460b0cbed1363e2166a2de1d9f`. Both ordinary raw GitHub fetches exited normally with no stdout; no package or tool was installed.

```sh
timeout 10 mkdir -p /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-24/fetch/w1 && timeout 40 curl -fsSL https://raw.githubusercontent.com/hyprwm/Hyprland/efb50993780079460b0cbed1363e2166a2de1d9f/src/desktop/view/Window.hpp -o /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-24/fetch/w1/SrcWindowView-1.bin

timeout 10 mkdir -p /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-24/fetch/w1 && timeout 40 curl -fsSL https://raw.githubusercontent.com/hyprwm/Hyprland/efb50993780079460b0cbed1363e2166a2de1d9f/src/desktop/view/Window.cpp -o /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-24/fetch/w1/SrcWindowView-2.bin

timeout 10 sha256sum /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-24/fetch/w1/SrcWindowView-1.bin /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-24/fetch/w1/SrcWindowView-2.bin && timeout 10 wc -c /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-24/fetch/w1/SrcWindowView-1.bin /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-24/fetch/w1/SrcWindowView-2.bin
```

Observed metadata output:

```text
1f60b8ff0bc6b5a48af5c03cb2cac1108db677efc70b4424b56ef6f1f2d1cc81  /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-24/fetch/w1/SrcWindowView-1.bin
d735d454cc4b7983f19626514d310669047da46780c509ffae68ccf072211ded  /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-24/fetch/w1/SrcWindowView-2.bin
 23988 /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-24/fetch/w1/SrcWindowView-1.bin
124226 /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-24/fetch/w1/SrcWindowView-2.bin
148214 total
```

`timeout 10 wc -l /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-24/fetch/w1/SrcWindowView-1.bin /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-24/fetch/w1/SrcWindowView-2.bin` returned 542 and 2966 lines respectively (3508 total).

The first inline quote-check attempt exited nonzero with `NameError: name 'PASS' is not defined` because shell quoting split an f-string expression; it changed no files. The corrected final check command returned exit 0 and printed PASS for all six rows:

```sh
timeout 20 python3 -c 'import pathlib,re; base=pathlib.Path("/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-24/fetch/w1"); files={"hpp":base/"SrcWindowView-1.bin","cpp":base/"SrcWindowView-2.bin"}; rows=[("A1","hpp","CWindow declares a `m_ruleApplicator` field with the window-rule applicator type in its object state.","UP<Desktop::Rule::CWindowRuleApplicator> m_ruleApplicator;"),("A2","hpp","CWindow declares `m_closeableSince` as `Time::steady_tp` under the `noclosefor` windowrule comment.","// For the noclosefor windowrule Time::steady_tp m_closeableSince = Time::steadyNow();"),("A3","hpp","The `GROUP_OVERRIDE` constant\x27s comment says it overrides other rules.","GROUP_OVERRIDE    = 1 << 6, // Override other rules"),("A4","cpp","CWindow log text says `Rule workspace matched by` and contains two `{}` placeholders before `applied`.","Rule workspace matched by {}, {} applied."),("A5","cpp","CWindow calls `propertiesChanged` with the title-specific `RULE_PROP_TITLE` rule-property flag.","m_ruleApplicator->propertiesChanged(Desktop::Rule::RULE_PROP_TITLE"),("A6","cpp","CWindow sets `m_groupRules` to `GROUP_OVERRIDE` after the comment says Clear existing rules.","// Clear existing rules m_groupRules = Desktop::View::GROUP_OVERRIDE;")]; collapse=lambda s:re.sub(r"\s+"," ",s).strip(); topic=re.compile(r"\b(?:window ?rules?|windowrules?(?:v2)?|layerrules?|rules?|getprop|props?|tags?|match(?:es|ing)?)\b",re.I); texts={k:collapse(v.read_bytes().decode("utf-8","replace")) for k,v in files.items()}; failed=[]
for rid,key,claim,quote in rows:
 q=collapse(quote); words=q.lower().split(); c=collapse(claim).lower(); anchor=any(" ".join(words[i:i+4]) in c for i in range(len(words)-3)) or any(len(t)>=4 and t in quote for t in re.findall(r"`([^`\s]+)",claim)); ok=q in texts[key]; top=bool(topic.search(quote)); count=len(c.split()); passed=ok and top and anchor and count>=8 and len(words)<=25 and "|" not in claim and "|" not in quote; label="PASS" if passed else "FAIL"; print(f"{rid}: collapsed_substring={ok} topic={top} anchor={anchor} claim_words={count} quote_words={len(words)} no_delimiter={chr(124) not in claim and chr(124) not in quote} => {label}"); failed.append(not passed)
assert not any(failed)'
```

Output:

```text
A1: collapsed_substring=True topic=True anchor=True claim_words=14 quote_words=2 no_delimiter=True => PASS
A2: collapsed_substring=True topic=True anchor=True claim_words=10 quote_words=9 no_delimiter=True => PASS
A3: collapsed_substring=True topic=True anchor=True claim_words=9 quote_words=9 no_delimiter=True => PASS
A4: collapsed_substring=True topic=True anchor=True claim_words=15 quote_words=7 no_delimiter=True => PASS
A5: collapsed_substring=True topic=True anchor=True claim_words=9 quote_words=1 no_delimiter=True => PASS
A6: collapsed_substring=True topic=True anchor=True claim_words=12 quote_words=7 no_delimiter=True => PASS
```

## Gates, surfaces, and limits

- Gate run: the local six-row quote/topic/anchor check passed. The frozen C1 counter was not run: this report is a source opener, the claim IDs are placeholders, and no integration note or SOURCES rows were authored here. No C2 counter, build, tests, host probe, or compositor action was run.
- Touched surfaces: the two raw source receipts under `.ufo/waves/round-24/fetch/w1/` and this report only. No product code, `corpus/SOURCES.md`, note, README, or other lane file was edited. No installation or update occurred.
- Out of scope: reading the applicator implementation, identifying per-rule match references or rule-tag matching internals, mapping the `getprop` surface, and measuring host window behavior. Those remain unestablished here; host behavior stays [UNK].

VERDICT: Window.hpp and Window.cpp source opening is complete; six proposed quote rows passed the local byte/anchor checks. No wave-level C1 or C2 verdict is claimed.

Report: .ufo/waves/round-24/w1/reports/SrcWindowView.md
