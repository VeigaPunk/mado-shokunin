# SrcMatchEngine — round 24 C1 source-opener report

## Scope and verdict

Opened all 12 files listed under the pinned Hyprland v0.56.2 `src/desktop/rule/matchEngine/` directory. Each was fetched from its raw GitHub URL at commit `efb50993780079460b0cbed1363e2166a2de1d9f`, saved under `.ufo/waves/round-24/fetch/w1/`, hashed, and read. The source rows and claim rows below are drafts only; per L1’s instruction, global source IDs remain `S?` and `corpus/SOURCES.md` was not edited.

**Verdict:** this source set grounds typed matcher inputs and several matcher predicates. It does not by itself map rule keys such as `class` or `title` to those engines, nor establish live host behavior or rule attribution. No C1 counter was run; this report makes no gate-pass claim.

## Findings

### Observations from the pinned bytes

- `MatchEngine.hpp` declares engine kinds regex, bool, int, workspace, and tag, and `IMatchEngine` overloads `match` for `std::string`, `bool`, `int`, `PHLWORKSPACE`, and `CTagKeeper`. `MatchEngine.cpp` gives the base implementations of these overloads `false` returns.
- `CRegexMatchEngine` accepts a string. Its implementation recognizes the `negative:` prefix, stores a negative flag, and evaluates `re2::RE2::FullMatch(other, *m_regex) != m_negative`.
- `CTagMatchEngine` stores the supplied tag string and returns `keeper.isTagged(m_tag)`.
- `CBoolMatchEngine` initializes its stored boolean through `truthy(s)` and tests equality with the input boolean.
- `CIntMatchEngine` assigns `std::stoi(s)` to its stored integer, logs caught conversion failures, and tests equality with the input integer.
- `CWorkspaceMatchEngine` stores a string and returns `ws && ws->matchesStaticSelector(m_value)`.

### Bounded inference and unknowns

The tag engine directly establishes a tag-keeper predicate; the other interfaces establish value types, not named window properties. In particular, a `std::string` matcher input does not say whether its caller supplied a class, title, or another value. A case-insensitive sweep for `title` over the entire matchEngine directory returned no matches (command and output below); that is a bounded statement about this directory only, not a claim that Hyprland lacks title-based matching elsewhere.

The engine sources do not establish how a window-rule parser binds properties to engines, aliases accepted by that parser, what tag state is attached to a live window, which rules match a live client, or which rule caused an applied effect. Those questions remain `[UNK]` from this source set. The host compositor was not queried.

## Proposed SOURCES rows

The local aliases `ME-01`–`ME-12` connect each row and following claim table to its saved fetch. Replace each provisional `S?` with the global ID assigned by L1 during integration. Every proposed row uses the requested 11-cell shape.

| S? | source | kind | tier | scope | anchor | teaches | status | opened | recheck | used-by |
|---|---|---|---|---|---|---|---|---|---|---|
| S? | Hyprland v0.56.2 MatchEngine.hpp — https://raw.githubusercontent.com/hyprwm/Hyprland/efb50993780079460b0cbed1363e2166a2de1d9f/src/desktop/rule/matchEngine/MatchEngine.hpp | code | A | Match-engine enum and input overloads | src/desktop/rule/matchEngine/MatchEngine.hpp:8-23 @ commit efb50993780079460b0cbed1363e2166a2de1d9f, sha256:dd2ea4c9a63583a425abefa073dcf39a009905a7514f4e21bd38496140fdb582, 662 B | engine kinds and typed matcher inputs, not window-property bindings | mined | 2026-10-23 | on-release | corpus/knowledge/rule-attribution-r24.md |
| S? | Hyprland v0.56.2 MatchEngine.cpp — https://raw.githubusercontent.com/hyprwm/Hyprland/efb50993780079460b0cbed1363e2166a2de1d9f/src/desktop/rule/matchEngine/MatchEngine.cpp | code | A | Base match overload results | src/desktop/rule/matchEngine/MatchEngine.cpp:5-23 @ commit efb50993780079460b0cbed1363e2166a2de1d9f, sha256:298dd285d3896dc6ce9608ff44bf05f0488372c806e867d2cd07558502b50f66, 370 B | the base string and tag-keeper overloads return false; the file defines the same default for the other overloads | mined | 2026-10-23 | on-release | corpus/knowledge/rule-attribution-r24.md |
| S? | Hyprland v0.56.2 RegexMatchEngine.hpp — https://raw.githubusercontent.com/hyprwm/Hyprland/efb50993780079460b0cbed1363e2166a2de1d9f/src/desktop/rule/matchEngine/RegexMatchEngine.hpp | code | A | Regex matcher interface and stored state | src/desktop/rule/matchEngine/RegexMatchEngine.hpp:12-21 @ commit efb50993780079460b0cbed1363e2166a2de1d9f, sha256:1bd284a2bcf76e806a72c892dffdbba93fe181198ef23e5769a89c62a5b99099, 483 B | string-input override, RE2 object, and negative flag | mined | 2026-10-23 | on-release | corpus/knowledge/rule-attribution-r24.md |
| S? | Hyprland v0.56.2 RegexMatchEngine.cpp — https://raw.githubusercontent.com/hyprwm/Hyprland/efb50993780079460b0cbed1363e2166a2de1d9f/src/desktop/rule/matchEngine/RegexMatchEngine.cpp | code | A | Regex prefix handling and result predicate | src/desktop/rule/matchEngine/RegexMatchEngine.cpp:7-16 @ commit efb50993780079460b0cbed1363e2166a2de1d9f, sha256:8ca655336cd111df1136be76bbdf91bd6830e7e8891df4bb8c766f1e55a3a282, 470 B | the `negative:` flag and RE2 FullMatch comparison | mined | 2026-10-23 | on-release | corpus/knowledge/rule-attribution-r24.md |
| S? | Hyprland v0.56.2 TagMatchEngine.hpp — https://raw.githubusercontent.com/hyprwm/Hyprland/efb50993780079460b0cbed1363e2166a2de1d9f/src/desktop/rule/matchEngine/TagMatchEngine.hpp | code | A | Tag matcher interface and stored tag | src/desktop/rule/matchEngine/TagMatchEngine.hpp:7-15 @ commit efb50993780079460b0cbed1363e2166a2de1d9f, sha256:d9eb7f43a7d35c6c43aaa6e3ec05cab73663545fee0357c57cc7b99b31f7800f, 352 B | keeper-specific match overload and tag-string member | mined | 2026-10-23 | on-release | corpus/knowledge/rule-attribution-r24.md |
| S? | Hyprland v0.56.2 TagMatchEngine.cpp — https://raw.githubusercontent.com/hyprwm/Hyprland/efb50993780079460b0cbed1363e2166a2de1d9f/src/desktop/rule/matchEngine/TagMatchEngine.cpp | code | A | Tag matching implementation | src/desktop/rule/matchEngine/TagMatchEngine.cpp:7-12 @ commit efb50993780079460b0cbed1363e2166a2de1d9f, sha256:d30318effb1528cc7452f45e53a972fbea893958af99419fea9bcfc6b4e7fb23, 297 B | the configured string is checked with `CTagKeeper::isTagged` | mined | 2026-10-23 | on-release | corpus/knowledge/rule-attribution-r24.md |
| S? | Hyprland v0.56.2 BoolMatchEngine.hpp — https://raw.githubusercontent.com/hyprwm/Hyprland/efb50993780079460b0cbed1363e2166a2de1d9f/src/desktop/rule/matchEngine/BoolMatchEngine.hpp | code | A | Boolean matcher interface and stored value | src/desktop/rule/matchEngine/BoolMatchEngine.hpp:6-14 @ commit efb50993780079460b0cbed1363e2166a2de1d9f, sha256:2a6206671b8929c97bbf62c9329efc938071c75dd8b0e00c6203abd43cf844ca, 321 B | boolean-input override and stored boolean | mined | 2026-10-23 | on-release | corpus/knowledge/rule-attribution-r24.md |
| S? | Hyprland v0.56.2 BoolMatchEngine.cpp — https://raw.githubusercontent.com/hyprwm/Hyprland/efb50993780079460b0cbed1363e2166a2de1d9f/src/desktop/rule/matchEngine/BoolMatchEngine.cpp | code | A | Boolean parsing and comparison | src/desktop/rule/matchEngine/BoolMatchEngine.cpp:6-11 @ commit efb50993780079460b0cbed1363e2166a2de1d9f, sha256:183185289ba3955cd56b16c3bb777cdc0a18433c7dab18765c30d3f8b7f8d993, 273 B | `truthy` conversion followed by equality comparison | mined | 2026-10-23 | on-release | corpus/knowledge/rule-attribution-r24.md |
| S? | Hyprland v0.56.2 IntMatchEngine.hpp — https://raw.githubusercontent.com/hyprwm/Hyprland/efb50993780079460b0cbed1363e2166a2de1d9f/src/desktop/rule/matchEngine/IntMatchEngine.hpp | code | A | Integer matcher interface and stored value | src/desktop/rule/matchEngine/IntMatchEngine.hpp:6-14 @ commit efb50993780079460b0cbed1363e2166a2de1d9f, sha256:fc54001b331a09280119fa76aa19c6d3e36c9ff4f215628a07f696a3695878f5, 312 B | integer-input override, text constructor, and stored integer | mined | 2026-10-23 | on-release | corpus/knowledge/rule-attribution-r24.md |
| S? | Hyprland v0.56.2 IntMatchEngine.cpp — https://raw.githubusercontent.com/hyprwm/Hyprland/efb50993780079460b0cbed1363e2166a2de1d9f/src/desktop/rule/matchEngine/IntMatchEngine.cpp | code | A | Integer conversion error path and comparison | src/desktop/rule/matchEngine/IntMatchEngine.cpp:6-13 @ commit efb50993780079460b0cbed1363e2166a2de1d9f, sha256:f832b4380766dada25cfadba6f9ef5eead905608d4f772a635051c75c9985bb8, 368 B | `std::stoi` conversion, caught error logging, and integer equality | mined | 2026-10-23 | on-release | corpus/knowledge/rule-attribution-r24.md |
| S? | Hyprland v0.56.2 WorkspaceMatchEngine.hpp — https://raw.githubusercontent.com/hyprwm/Hyprland/efb50993780079460b0cbed1363e2166a2de1d9f/src/desktop/rule/matchEngine/WorkspaceMatchEngine.hpp | code | A | Workspace matcher interface and stored string | src/desktop/rule/matchEngine/WorkspaceMatchEngine.hpp:7-15 @ commit efb50993780079460b0cbed1363e2166a2de1d9f, sha256:07491505f65b747d31df5471a73d6832191b990b78ab4ae36250ec64a0586e83, 364 B | string member and `PHLWORKSPACE` input overload | mined | 2026-10-23 | on-release | corpus/knowledge/rule-attribution-r24.md |
| S? | Hyprland v0.56.2 WorkspaceMatchEngine.cpp — https://raw.githubusercontent.com/hyprwm/Hyprland/efb50993780079460b0cbed1363e2166a2de1d9f/src/desktop/rule/matchEngine/WorkspaceMatchEngine.cpp | code | A | Workspace matching implementation | src/desktop/rule/matchEngine/WorkspaceMatchEngine.cpp:6-11 @ commit efb50993780079460b0cbed1363e2166a2de1d9f, sha256:580c0aa8884d4742f7e94081f15a4f8a889ac560d41e6193c7c1950446fe09bc, 299 B | non-null workspace check and `matchesStaticSelector` call | mined | 2026-10-23 | on-release | corpus/knowledge/rule-attribution-r24.md |

## Proposed C1 claim rows

Each section’s `S?` refers to the corresponding provisional SOURCES row above. The 24 quotations were checked against the saved bytes using whitespace-collapsed substring comparison. The check used the frozen v2 topic-word expression and anchor predicate: every quote is at most 25 whitespace-separated words, contains a topic term, every claim has at least eight words, and each claim has a valid anchored identifier. Final check output: `rows 24 sources 12 errors []`.

### ME-01 — MatchEngine.hpp

| A1 | The header places `RULE_MATCH_ENGINE_TAG` ahead of its string-input `match` declaration in `IMatchEngine`. | S? | "RULE_MATCH_ENGINE_REGEX = 0, RULE_MATCH_ENGINE_BOOL, RULE_MATCH_ENGINE_INT, RULE_MATCH_ENGINE_WORKSPACE, RULE_MATCH_ENGINE_TAG, }; class IMatchEngine { public: virtual ~IMatchEngine() = default; virtual bool match(const std::string&);" |
| A2 | The base matcher declares distinct `match` overloads for string, boolean, integer, workspace, and tag-keeper inputs. | S? | "public: virtual ~IMatchEngine() = default; virtual bool match(const std::string&); virtual bool match(bool); virtual bool match(int); virtual bool match(PHLWORKSPACE); virtual bool match(const CTagKeeper& keeper);" |

### ME-02 — MatchEngine.cpp

| A3 | The base `IMatchEngine::match` implementation for a string input returns false. | S? | "bool IMatchEngine::match(const std::string&) { return false; }" |
| A4 | The base `IMatchEngine::match` implementation taking a tag keeper also returns false. | S? | "bool IMatchEngine::match(const CTagKeeper& keeper) { return false; }" |

### ME-03 — RegexMatchEngine.hpp

| A5 | The regex matcher overrides `match` for string input, without naming the originating window property. | S? | "virtual bool match(const std::string& other);" |
| A6 | The regex engine stores a RE2 object and a separate `m_negative` flag beside its string-input match override. | S? | "virtual bool match(const std::string& other); private: UP<re2::RE2> m_regex; bool m_negative = false;" |

### ME-04 — RegexMatchEngine.cpp

| A7 | The `negative:` prefix sets `m_negative`, and regex `match` compares RE2 `FullMatch` with that flag. | S? | "if (regex.starts_with("negative:")) { m_negative = true; m_regex = makeUnique<re2::RE2>(regex.substr(9)); return; } m_regex = makeUnique<re2::RE2>(regex); } bool CRegexMatchEngine::match(const std::string& other) { return re2::RE2::FullMatch(other, *m_regex) != m_negative;" |
| A8 | The regex matcher returns the `FullMatch` boolean inequality against its stored negative flag. | S? | "bool CRegexMatchEngine::match(const std::string& other) { return re2::RE2::FullMatch(other, *m_regex) != m_negative; }" |

### ME-05 — TagMatchEngine.hpp

| A9 | The tag matcher overrides `match` with a `CTagKeeper` input rather than a string. | S? | "virtual bool match(const CTagKeeper& keeper);" |
| A10 | The tag engine stores its selector in `m_tag` and exposes a keeper-specific `match` overload. | S? | "class CTagMatchEngine : public IMatchEngine { public: CTagMatchEngine(const std::string& tag); virtual ~CTagMatchEngine() = default; virtual bool match(const CTagKeeper& keeper); private: std::string m_tag;" |

### ME-06 — TagMatchEngine.cpp

| A11 | Tag matching delegates to the keeper’s tag test using the stored `m_tag` value. | S? | "bool CTagMatchEngine::match(const CTagKeeper& keeper) { return keeper.isTagged(m_tag); }" |
| A12 | The constructor stores the supplied tag string in `m_tag`; later `match` tests that value against the keeper. | S? | "CTagMatchEngine::CTagMatchEngine(const std::string& tag) : m_tag(tag) { ; } bool CTagMatchEngine::match(const CTagKeeper& keeper) { return keeper.isTagged(m_tag); }" |

### ME-07 — BoolMatchEngine.hpp

| A13 | The boolean matcher declares a `match` override that receives a boolean value. | S? | "virtual bool match(bool other);" |
| A14 | The boolean matcher accepts constructor text and keeps a boolean `m_value` for matching. | S? | "CBoolMatchEngine(const std::string&); virtual ~CBoolMatchEngine() = default; virtual bool match(bool other); private: bool m_value = false;" |

### ME-08 — BoolMatchEngine.cpp

| A15 | The boolean engine parses constructor text with `truthy`, then `match` compares input with stored `m_value`. | S? | "CBoolMatchEngine::CBoolMatchEngine(const std::string& s) : m_value(truthy(s)) { ; } bool CBoolMatchEngine::match(bool other) { return other == m_value; }" |
| A16 | `CBoolMatchEngine::match` returns true exactly when the input equals the stored boolean value. | S? | "bool CBoolMatchEngine::match(bool other) { return other == m_value; }" |

### ME-09 — IntMatchEngine.hpp

| A17 | The integer matcher declares a `match` override taking an `int` input. | S? | "virtual bool match(int other);" |
| A18 | The integer engine has an integer `m_value` field, a text-taking constructor, and an `int` match input. | S? | "CIntMatchEngine(const std::string&); virtual ~CIntMatchEngine() = default; virtual bool match(int other); private: int m_value = 0;" |

### ME-10 — IntMatchEngine.cpp

| A19 | `CIntMatchEngine::match` tests equality between `other` and `m_value`, not a range. | S? | "bool CIntMatchEngine::match(int other) { return m_value == other; }" |
| A20 | This snippet assigns `std::stoi(s)`, logs caught failures, and then the integer `match` body tests equality. | S? | "m_value = std::stoi(s); } catch (...) { Log::logger->log(Log::ERR, "CIntMatchEngine: invalid input {}", s); } } bool CIntMatchEngine::match(int other) { return m_value == other; }" |

### ME-11 — WorkspaceMatchEngine.hpp

| A21 | The workspace matcher provides a `match` overload whose input is `PHLWORKSPACE`. | S? | "virtual bool match(PHLWORKSPACE ws);" |
| A22 | The workspace engine declares a text-taking constructor and a string `m_value` field alongside its `PHLWORKSPACE` match argument. | S? | "class CWorkspaceMatchEngine : public IMatchEngine { public: CWorkspaceMatchEngine(const std::string&); virtual ~CWorkspaceMatchEngine() = default; virtual bool match(PHLWORKSPACE ws); private: std::string m_value = "";" |

### ME-12 — WorkspaceMatchEngine.cpp

| A23 | Workspace `match` requires a non-null pointer and delegates selector checking to `matchesStaticSelector`. | S? | "bool CWorkspaceMatchEngine::match(PHLWORKSPACE ws) { return ws && ws->matchesStaticSelector(m_value); }" |
| A24 | The configured selector is stored in `m_value` and checked through the workspace’s `matchesStaticSelector` method. | S? | "CWorkspaceMatchEngine::CWorkspaceMatchEngine(const std::string& s) : m_value(s) { ; } bool CWorkspaceMatchEngine::match(PHLWORKSPACE ws) { return ws && ws->matchesStaticSelector(m_value); }" |

## Fetch and validation receipts

Each fetch was an independent shell command, wrapped in `timeout 30s`, then hashed and byte-counted. These are the literal command lines executed:

```text
timeout 30s curl -fsSL https://raw.githubusercontent.com/hyprwm/Hyprland/efb50993780079460b0cbed1363e2166a2de1d9f/src/desktop/rule/matchEngine/MatchEngine.hpp -o /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-24/fetch/w1/SrcMatchEngine-1.bin && sha256sum /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-24/fetch/w1/SrcMatchEngine-1.bin && wc -c /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-24/fetch/w1/SrcMatchEngine-1.bin
timeout 30s curl -fsSL https://raw.githubusercontent.com/hyprwm/Hyprland/efb50993780079460b0cbed1363e2166a2de1d9f/src/desktop/rule/matchEngine/MatchEngine.cpp -o /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-24/fetch/w1/SrcMatchEngine-2.bin && sha256sum /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-24/fetch/w1/SrcMatchEngine-2.bin && wc -c /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-24/fetch/w1/SrcMatchEngine-2.bin
timeout 30s curl -fsSL https://raw.githubusercontent.com/hyprwm/Hyprland/efb50993780079460b0cbed1363e2166a2de1d9f/src/desktop/rule/matchEngine/RegexMatchEngine.hpp -o /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-24/fetch/w1/SrcMatchEngine-3.bin && sha256sum /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-24/fetch/w1/SrcMatchEngine-3.bin && wc -c /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-24/fetch/w1/SrcMatchEngine-3.bin
timeout 30s curl -fsSL https://raw.githubusercontent.com/hyprwm/Hyprland/efb50993780079460b0cbed1363e2166a2de1d9f/src/desktop/rule/matchEngine/RegexMatchEngine.cpp -o /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-24/fetch/w1/SrcMatchEngine-4.bin && sha256sum /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-24/fetch/w1/SrcMatchEngine-4.bin && wc -c /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-24/fetch/w1/SrcMatchEngine-4.bin
timeout 30s curl -fsSL https://raw.githubusercontent.com/hyprwm/Hyprland/efb50993780079460b0cbed1363e2166a2de1d9f/src/desktop/rule/matchEngine/TagMatchEngine.hpp -o /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-24/fetch/w1/SrcMatchEngine-5.bin && sha256sum /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-24/fetch/w1/SrcMatchEngine-5.bin && wc -c /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-24/fetch/w1/SrcMatchEngine-5.bin
timeout 30s curl -fsSL https://raw.githubusercontent.com/hyprwm/Hyprland/efb50993780079460b0cbed1363e2166a2de1d9f/src/desktop/rule/matchEngine/TagMatchEngine.cpp -o /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-24/fetch/w1/SrcMatchEngine-6.bin && sha256sum /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-24/fetch/w1/SrcMatchEngine-6.bin && wc -c /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-24/fetch/w1/SrcMatchEngine-6.bin
timeout 30s curl -fsSL https://raw.githubusercontent.com/hyprwm/Hyprland/efb50993780079460b0cbed1363e2166a2de1d9f/src/desktop/rule/matchEngine/BoolMatchEngine.hpp -o /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-24/fetch/w1/SrcMatchEngine-7.bin && sha256sum /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-24/fetch/w1/SrcMatchEngine-7.bin && wc -c /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-24/fetch/w1/SrcMatchEngine-7.bin
timeout 30s curl -fsSL https://raw.githubusercontent.com/hyprwm/Hyprland/efb50993780079460b0cbed1363e2166a2de1d9f/src/desktop/rule/matchEngine/BoolMatchEngine.cpp -o /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-24/fetch/w1/SrcMatchEngine-8.bin && sha256sum /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-24/fetch/w1/SrcMatchEngine-8.bin && wc -c /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-24/fetch/w1/SrcMatchEngine-8.bin
timeout 30s curl -fsSL https://raw.githubusercontent.com/hyprwm/Hyprland/efb50993780079460b0cbed1363e2166a2de1d9f/src/desktop/rule/matchEngine/IntMatchEngine.hpp -o /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-24/fetch/w1/SrcMatchEngine-9.bin && sha256sum /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-24/fetch/w1/SrcMatchEngine-9.bin && wc -c /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-24/fetch/w1/SrcMatchEngine-9.bin
timeout 30s curl -fsSL https://raw.githubusercontent.com/hyprwm/Hyprland/efb50993780079460b0cbed1363e2166a2de1d9f/src/desktop/rule/matchEngine/IntMatchEngine.cpp -o /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-24/fetch/w1/SrcMatchEngine-10.bin && sha256sum /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-24/fetch/w1/SrcMatchEngine-10.bin && wc -c /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-24/fetch/w1/SrcMatchEngine-10.bin
timeout 30s curl -fsSL https://raw.githubusercontent.com/hyprwm/Hyprland/efb50993780079460b0cbed1363e2166a2de1d9f/src/desktop/rule/matchEngine/WorkspaceMatchEngine.hpp -o /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-24/fetch/w1/SrcMatchEngine-11.bin && sha256sum /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-24/fetch/w1/SrcMatchEngine-11.bin && wc -c /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-24/fetch/w1/SrcMatchEngine-11.bin
timeout 30s curl -fsSL https://raw.githubusercontent.com/hyprwm/Hyprland/efb50993780079460b0cbed1363e2166a2de1d9f/src/desktop/rule/matchEngine/WorkspaceMatchEngine.cpp -o /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-24/fetch/w1/SrcMatchEngine-12.bin && sha256sum /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-24/fetch/w1/SrcMatchEngine-12.bin && wc -c /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-24/fetch/w1/SrcMatchEngine-12.bin
```

The digest and byte-count outputs are recorded in every corresponding proposed SOURCES row above. A whitespace-collapsed quote/anchor validation was run in Python against these saved files using the frozen C1 v2 topic and anchored-claim predicates; result: 12 files, 24 rows, `errors []`. No counter or host command was executed.

Negative-token sweep: `functions.grep(pattern="title", path="/fast/scratch/hyaku/mado-r24/src/Hyprland-v0.56.2/src/desktop/rule/matchEngine", case=false, gitignore=false, skip=0)` returned `No matches found`.

## Surfaces, limits, and out of scope

- Written artifacts: `.ufo/waves/round-24/fetch/w1/SrcMatchEngine-1.bin` through `SrcMatchEngine-12.bin`; this report at `.ufo/waves/round-24/w1/reports/SrcMatchEngine.md`.
- Read-only source checkout used for directory listing: `/fast/scratch/hyaku/mado-r24/src/Hyprland-v0.56.2/src/desktop/rule/matchEngine/`. All cited bytes came from the raw URLs above, not from a local checkout edit.
- Read the round registration and frozen C1 counter docstring. No source row was added to `corpus/SOURCES.md`; no note, product code, judge, or gate was changed. No packages were installed.
- C2 calibration, property-to-engine call sites outside this directory, host rule state, live client state, `hyprctl`, match attribution, applied-effect provenance, and full round integration are out of scope. Host behavior remains `[UNK]` here.
