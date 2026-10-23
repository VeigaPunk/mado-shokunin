# SrcHyprCtl — round 24 C1 source-opener report

## Scope and receipt

Opened only the pinned Hyprland source file requested. The existing round-12 `corpus/knowledge/window-rule-effects-getprop.md` was read to avoid repeating its value examples; this report focuses on whether any of these source paths attribute effects to a matching rule.

- Raw URL: `https://raw.githubusercontent.com/hyprwm/Hyprland/efb50993780079460b0cbed1363e2166a2de1d9f/src/debug/HyprCtl.cpp`
- Fetch command: `timeout 30 curl -fsSL https://raw.githubusercontent.com/hyprwm/Hyprland/efb50993780079460b0cbed1363e2166a2de1d9f/src/debug/HyprCtl.cpp -o /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-24/fetch/w1/SrcHyprCtl-1.bin`
- Outcome: curl succeeded; `sha256sum` returned `798b7c6c4c1684557842463d46ac99c96629be4179e0e461dca77670247b91fa`; `wc -c` returned `97582`; `splitlines()` counted 2346 source lines (the decoded text has 2347 newline-count-plus-one).
- Saved bytes: `.ufo/waves/round-24/fetch/w1/SrcHyprCtl-1.bin`
- Commit: `efb50993780079460b0cbed1363e2166a2de1d9f` (Hyprland v0.56.2).
- Read anchors: `getTagsData` and window JSON `346-456`; `clientsRequest` `458-484`; workspace-rule listing `613-630`; layer response `647-723`; `dispatchGetProp` `1463-1645`; command registration `2003-2044`.

No package/tool installation. No compositor command was run. No product file or `SOURCES.md` was edited. The only created files are this report and the fetched source bytes above.

## Source observations

- **`clients` JSON and tags.** `clientsRequest` calls `getWindowData` for each included window. Its JSON object contains ordinary state/identity fields (`address`, `workspace`, `class`, `title`, etc.) and a `tags` field (`376-435`, `458-484`). `getTagsData` obtains the tags from `w->m_ruleApplicator->m_tagKeeper.getTags()` and serializes them (`346-353`). The field is current tag data; this response does not say which rule assigned a tag or identify a matching rule. The round-12 host capture intentionally projected only four fields and omitted tags; that capture limitation is not a claim that the source JSON lacks tags.
- **`getprop`.** `dispatchGetProp` resolves the requested window selector and property, with `not enough args` and `window not found` error returns (`1463-1477`). Its property branches return per-window property values through value-formatting helpers; for example, `opacity` passes the selected window's rule-applicator alpha to `alphaToString` (`1493-1504`, `1548-1560`, `1565-1644`). The helper returns the alpha value (or its override flag for the corresponding override property); JSON mode wraps the property value in a property-keyed object. These are property/effect reads, not a rule identity or match record.
- **Layers.** The `layers` JSON response groups layer surfaces by monitor and level and emits `address`, geometry (`x`, `y`, `w`, `h`), `alpha`, `namespace`, and `pid` (`647-723`). Those fields describe layer state, not a `layerrule` identity or match result.
- **Rule-list commands.** The registered `workspacerules` command calls `workspaceRulesRequest`, which iterates `Config::workspaceRuleMgr()->getAllWorkspaceRules()` (`2005`, `613-630`). The full registration sweep below contains no dedicated window-rule or layer-rule listing/match-result verb. This is bounded to the command registrations and handlers in this pinned `HyprCtl.cpp`, not every possible external or dynamic instrumentation surface.

### Observation versus inference

- **[OBS]** The `clients` object schema includes tags; tag values come from the window's rule-applicator tag keeper. The clients schema contains no field naming a matched rule or match trace.
- **[OBS]** `getprop`'s response paths return property values or request errors. The opacity branch reads the selected window's rule-applicator alpha; the source response path has no rule-name or matched-condition result.
- **[OBS]** `layers` returns geometry, alpha, namespace, and pid. The `workspacerules` handler lists workspace rules. No dedicated window-/layer-rule query is registered in the inspected command registry.
- **[INF]** These are evidence of a state/tag read, an effect-value read, and a workspace-rule list—not of which window or layer rule caused an applied effect. Current tag labels may be useful input when reasoning about rules, but are not attribution evidence.
- **[UNK]** This source inspection does not measure host clients, tags, actual rule matches, effect values, layer state, or runtime output. It does not establish that another interface or plugin cannot expose attribution.

The response-schema, handler-return, and command-registration sweeps used for the bounded negative observations are reproduced here with their outputs.

## Sweep commands and outputs

### Source-schema, handler-return, and command-registration sweep

Command:

```sh
python3 -I -c 'from pathlib import Path; import re; p=Path("/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-24/fetch/w1/SrcHyprCtl-1.bin"); lines=p.read_bytes().decode("utf-8").splitlines();
def span(a,b): return [(n,lines[n-1]) for n in range(a,b+1)]
print("clients JSON keys, source lines 386-424:");
for n,line in span(386,424):
 m=re.match(r"\s*\"([^\"]+)\":",line)
 if m: print(str(n)+":"+m.group(1))
print("layers JSON keys/templates, source lines 650-678:");
for n,line in span(650,678):
 m=re.search(r"\"([^\"]+)\"\s*:",line)
 if m: print(str(n)+":"+m.group(1))
print("dispatchGetProp return statements, source lines 1463-1645:");
for n,line in span(1463,1645):
 if "return " in line: print(str(n)+":"+line.strip())
print("command registration sweep, source lines 2003-2044:");
for n,line in span(2003,2044):
 if "registerCommand(SHyprCtlCommand{" in line: print(str(n)+":"+line.strip())'
```

Output:

```text
clients JSON keys, source lines 386-424:
389:address
390:mapped
391:hidden
392:visible
393:acceptsInput
394:at
395:size
396:workspace
397:id
398:name
400:floating
401:monitor
402:class
403:title
404:initialClass
405:initialTitle
406:pid
407:xwayland
408:pinned
409:pinFullscreened
410:fullscreen
411:fullscreenClient
412:fullscreenHandler
413:allowedOverFullscreen
414:grouped
415:tags
416:swallowing
417:focusHistoryID
418:inhibitingIdle
419:xdgTag
420:xdgDescription
421:contentType
422:tearingHint
423:stableId
layers JSON keys/templates, source lines 650-678:
655:{}
656:levels
664:{}
670:address
671:x
672:y
673:w
674:h
675:alpha
676:namespace
677:pid
dispatchGetProp return statements, source lines 1463-1645:
1467:return "not enough args";
1475:return "window not found";
1485:return std::format("{} {}", sizeValue.x, sizeValue.y);
1489:return std::format(R"({{"{}": [{},{}]}})", PROP, xSizeString, ySizeString);
1496:return std::format("{}", alpha.valueOrDefault().alpha);
1498:return std::format("{}", alpha.valueOrDefault().overridden);
1501:return std::format(R"({{"{}": {}}})", PROP, alpha.valueOrDefault().alpha);
1503:return std::format(R"({{"{}": {}}})", PROP, alpha.valueOrDefault().overridden);
1529:return borderColorString;
1531:return std::format(R"({{"{}": "{}"}})", PROP, borderColorString);
1542:return borderColorString;
1544:return std::format(R"({{"{}": "{}"}})", PROP, borderColorString);
1550:return std::format("{}", prop.valueOrDefault());
1552:return std::format(R"({{"{}": {}}})", PROP, prop.valueOrDefault());
1558:return animationStyle.valueOr("(unset)");
1560:return std::format(R"({{"{}": "{}"}})", PROP, animationStyle.valueOr(""));
1562:return sizeToString(true);
1564:return sizeToString(false);
1566:return alphaToString(PWINDOW->m_ruleApplicator->alpha(), true);
1568:return alphaToString(PWINDOW->m_ruleApplicator->alphaInactive(), true);
1570:return alphaToString(PWINDOW->m_ruleApplicator->alphaFullscreen(), true);
1572:return alphaToString(PWINDOW->m_ruleApplicator->alpha(), false);
1574:return alphaToString(PWINDOW->m_ruleApplicator->alphaInactive(), false);
1576:return alphaToString(PWINDOW->m_ruleApplicator->alphaFullscreen(), false);
1578:return borderColorToString(true);
1580:return borderColorToString(false);
1582:return windowPropToString(PWINDOW->m_ruleApplicator->allowsInput());
1584:return windowPropToString(PWINDOW->m_ruleApplicator->decorate());
1586:return windowPropToString(PWINDOW->m_ruleApplicator->focusOnActivate());
1588:return windowPropToString(PWINDOW->m_ruleApplicator->keepAspectRatio());
1590:return windowPropToString(PWINDOW->m_ruleApplicator->nearestNeighbor());
1592:return windowPropToString(PWINDOW->m_ruleApplicator->noAnim());
1594:return windowPropToString(PWINDOW->m_ruleApplicator->noBlur());
1596:return windowPropToString(PWINDOW->m_ruleApplicator->noDim());
1598:return windowPropToString(PWINDOW->m_ruleApplicator->noFocus());
1600:return windowPropToString(PWINDOW->m_ruleApplicator->noMaxSize());
1602:return windowPropToString(PWINDOW->m_ruleApplicator->noShadow());
1604:return windowPropToString(PWINDOW->m_ruleApplicator->noShortcutsInhibit());
1606:return windowPropToString(PWINDOW->m_ruleApplicator->opaque());
1608:return windowPropToString(PWINDOW->m_ruleApplicator->dimAround());
1610:return windowPropToString(PWINDOW->m_ruleApplicator->RGBX());
1612:return windowPropToString(PWINDOW->m_ruleApplicator->syncFullscreen());
1614:return windowPropToString(PWINDOW->m_ruleApplicator->tearing());
1616:return windowPropToString(PWINDOW->m_ruleApplicator->xray());
1618:return windowPropToString(PWINDOW->m_ruleApplicator->renderUnfocused());
1620:return windowPropToString(PWINDOW->m_ruleApplicator->noFollowMouse());
1622:return windowPropToString(PWINDOW->m_ruleApplicator->noScreenShare());
1624:return windowPropToString(PWINDOW->m_ruleApplicator->noVRR());
1626:return windowPropToString(PWINDOW->m_ruleApplicator->noAutoHDR());
1628:return windowPropToString(PWINDOW->m_ruleApplicator->persistentSize());
1630:return windowPropToString(PWINDOW->m_ruleApplicator->stayFocused());
1632:return windowPropToString(PWINDOW->m_ruleApplicator->idleInhibitMode());
1634:return windowPropToString(PWINDOW->m_ruleApplicator->borderSize());
1636:return windowPropToString(PWINDOW->m_ruleApplicator->rounding());
1638:return windowPropToString(PWINDOW->m_ruleApplicator->roundingPower());
1640:return windowPropToString(PWINDOW->m_ruleApplicator->scrollMouse());
1642:return windowPropToString(PWINDOW->m_ruleApplicator->scrollTouchpad());
1644:return "prop not found";
command registration sweep, source lines 2003-2044:
2004:registerCommand(SHyprCtlCommand{"workspaces", true, workspacesRequest});
2005:registerCommand(SHyprCtlCommand{"workspacerules", true, workspaceRulesRequest});
2006:registerCommand(SHyprCtlCommand{"activeworkspace", true, activeWorkspaceRequest});
2007:registerCommand(SHyprCtlCommand{"clients", true, clientsRequest});
2008:registerCommand(SHyprCtlCommand{"kill", true, killRequest});
2009:registerCommand(SHyprCtlCommand{"activewindow", true, activeWindowRequest});
2010:registerCommand(SHyprCtlCommand{"layers", true, layersRequest});
2011:registerCommand(SHyprCtlCommand{"version", true, versionRequest});
2012:registerCommand(SHyprCtlCommand{"devices", true, devicesRequest});
2013:registerCommand(SHyprCtlCommand{"splash", true, splashRequest});
2014:registerCommand(SHyprCtlCommand{"cursorpos", true, cursorPosRequest});
2015:registerCommand(SHyprCtlCommand{"binds", true, bindsRequest});
2016:registerCommand(SHyprCtlCommand{"globalshortcuts", true, globalShortcutsRequest});
2017:registerCommand(SHyprCtlCommand{"systeminfo", true, systemInfoRequest});
2018:registerCommand(SHyprCtlCommand{"animations", true, animationsRequest});
2019:registerCommand(SHyprCtlCommand{"rollinglog", true, rollinglogRequest});
2020:registerCommand(SHyprCtlCommand{"configerrors", true, configErrorsRequest});
2021:registerCommand(SHyprCtlCommand{"locked", true, getIsLocked});
2022:registerCommand(SHyprCtlCommand{"descriptions", true, getDescriptions});
2023:registerCommand(SHyprCtlCommand{"submap", true, submapRequest});
2024:registerCommand(SHyprCtlCommand{"status", true, statusRequest});
2026:registerCommand(SHyprCtlCommand{.name = "reloadshaders", .exact = false, .fn = reloadShaders});
2027:registerCommand(SHyprCtlCommand{"monitors", false, monitorsRequest});
2028:registerCommand(SHyprCtlCommand{"reload", false, reloadRequest});
2029:registerCommand(SHyprCtlCommand{"plugin", false, dispatchPlugin});
2030:registerCommand(SHyprCtlCommand{"notify", false, dispatchNotify});
2031:registerCommand(SHyprCtlCommand{"dismissnotify", false, dispatchDismissNotify});
2032:registerCommand(SHyprCtlCommand{"getprop", false, dispatchGetProp});
2033:registerCommand(SHyprCtlCommand{"seterror", false, dispatchSeterror});
2034:registerCommand(SHyprCtlCommand{"switchxkblayout", false, switchXKBLayoutRequest});
2035:registerCommand(SHyprCtlCommand{"output", false, dispatchOutput});
2036:registerCommand(SHyprCtlCommand{"dispatch", false, dispatchRequest});
2037:registerCommand(SHyprCtlCommand{"keyword", false, dispatchKeyword});
2038:registerCommand(SHyprCtlCommand{"setcursor", false, dispatchSetCursor});
2039:registerCommand(SHyprCtlCommand{"getoption", false, dispatchGetOption});
2040:registerCommand(SHyprCtlCommand{"decorations", false, decorationRequest});
2041:registerCommand(SHyprCtlCommand{"[[BATCH]]", false, dispatchBatch});
2042:registerCommand(SHyprCtlCommand{"eval", false, evalRequest});
2043:registerCommand(SHyprCtlCommand{"repl", false, evalRequest});
```

### Quote/predicate check for the proposed rows

The frozen v2 docstring was read at `.ufo/waves/round-24/c1/count.py:7-17`; its anchor helper was read at `:46-56`. I checked the quote bytes using whitespace-collapsed containment and checked topic, quote length, claim length, and the v2 anchor clause. Exact check command:

```sh
python3 -I -c 'from pathlib import Path; import re; p=Path("/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-24/fetch/w1/SrcHyprCtl-1.bin"); s=p.read_bytes().decode("utf-8"); qs=["const auto tags = w->m_ruleApplicator->m_tagKeeper.getTags();", "if (PROP == \"opacity\") return alphaToString(PWINDOW->m_ruleApplicator->alpha(), true);"]; cs=["Each `clients` JSON entry includes its tags, sourced from that window\x27s `m_ruleApplicator` tag keeper.", "The `getprop` opacity branch tests `PROP` and passes the selected window\x27s `m_ruleApplicator` alpha to `alphaToString`."]; collapse=lambda x: re.sub(r"\s+", " ", x).strip(); topic=re.compile(r"\b(?:window ?rules?|windowrules?(?:v2)?|layerrules?|rules?|getprop|props?|tags?|match(?:es|ing)?)\b", re.I);
for i,(q,c) in enumerate(zip(qs,cs),1):
 ids=re.findall(r"`([^`\s]+)`", c); words=collapse(q).split(); anchored=any(" ".join(words[j:j+4]) in collapse(c).lower() for j in range(len(words)-3)) or any(len(x)>=4 and x in q for x in ids); print("A"+str(i), "quote-collapsed-substring="+str(collapse(q) in collapse(s)), "quote-words="+str(len(words)), "topic="+str(bool(topic.search(q))), "claim-words="+str(len(c.split())), "anchor="+str(anchored))'
```

Output:

```text
A1 quote-collapsed-substring=True quote-words=5 topic=True claim-words=14 anchor=True
A2 quote-collapsed-substring=True quote-words=7 topic=True claim-words=15 anchor=True
```

## Proposed claim rows (provisional S?; not written to `SOURCES.md`)

| A1 | Each `clients` JSON entry includes its tags, sourced from that window's `m_ruleApplicator` tag keeper. | S? | "const auto tags = w->m_ruleApplicator->m_tagKeeper.getTags();" |
| A2 | The `getprop` opacity branch tests `PROP` and passes the selected window's `m_ruleApplicator` alpha to `alphaToString`. | S? | "if (PROP == "opacity") return alphaToString(PWINDOW->m_ruleApplicator->alpha(), true);" |

## Draft SOURCES row (provisional S?; integration owner assigns final ID)

| S? | HyprCtl.cpp — https://raw.githubusercontent.com/hyprwm/Hyprland/efb50993780079460b0cbed1363e2166a2de1d9f/src/debug/HyprCtl.cpp | code | A | `clients` JSON tags, `getprop` property response, `layers` output, registered rule-list commands | src/debug/HyprCtl.cpp:346-484, 613-630, 647-723, 1463-1645, 2003-2044 @ efb50993780079460b0cbed1363e2166a2de1d9f, sha256:798b7c6c4c1684557842463d46ac99c96629be4179e0e461dca77670247b91fa, 97582 B | Establishes client tag-state and property-value reads plus a workspace-rule list; no dedicated window/layer attribution verb appears in the registration sweep | mined | 2026-10-23 | on-release | corpus/knowledge/rule-attribution-r24.md |

## Gates, touched surfaces, and limits

- **Source opener gate:** pinned raw bytes saved; source checksum/size and anchors recorded; both proposed quote checks passed the stated quote-topic and claim-anchor checks. The S? rows are proposals only; the final `S###` ID, indexed note, counted C1 predicate, and counter result remain integration/main-agent work. No C1 target or counter pass is claimed here.
- **Touched surfaces:** created `.ufo/waves/round-24/fetch/w1/SrcHyprCtl-1.bin` and this report. No other lane file was changed; no `SOURCES.md` row was committed by this seat.
- **Out of scope:** host runtime behavior and actual rule matches, source files outside `src/debug/HyprCtl.cpp`, wiki claims, and any claim that no other API/plugin/instrumentation can expose attribution. No `hyprctl` command was run.
- **Verdict:** pinned source opener complete; findings are source-only and bounded to the inspected Hyprland commit. Rule-to-effect attribution and host behavior remain `[UNK]` from this source path.
