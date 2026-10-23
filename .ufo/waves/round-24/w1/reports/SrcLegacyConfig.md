# SrcLegacyConfig — round 24 wave 1

## Verdict

Opened the pinned Hyprland source and checked four proposed C1 rows against the fetched bytes. All four normalized quotes are present verbatim and are under 25 words. This is source-seat evidence only: the rows below use provisional `S?` IDs, are not added to `SOURCES.md` or the knowledge note, and do not establish the wave target or any host effect.

## Findings

**Observed in `src/config/legacy/ConfigManager.cpp`:**

- The constructor registers `windowrule` and `layerrule` special categories with `.key = "name"`; it registers `enable` with integer default `1` for each. The source comments label these “windowrule v3” and “layerrule v2” (590–596).
- It registers `handleWindowrule` and `handleLayerrule` as the respective keyword handlers, and registers `windowrulev2` / `layerrulev2` handlers that return explicit error messages (610–623; 431–452).
- The inline `handleWindowrule` callback passes its command and value to `CConfigManager::handleWindowrule`. That method builds a `CVarList2` from the value, visits each element, splits each element at its first space, recognizes a `match:` prefix and extracts the following property name, then validates that name against the available match properties. Otherwise it checks the first field against available window effects. A missing value, unknown property, unknown effect, or other field type returns an error; accepted property values and effects are registered on a newly created `CWindowRule` (419–429, 2016–2054).
- The special-category path obtains each `windowrule` key from `listKeysForSpecialCategory`, reads that key’s configured `match:*` and effect fields, constructs `CWindowRule(name)`, and registers it with the rule engine (893–916, 946–954). The `enable` check skips a rule only when its value was set by the user and is zero (894–896).
- `reloadRules()` clears existing engine rules, iterates listed `windowrule` keys, then listed `layerrule` keys, then iterates `m_keywordRules`, and finally calls `updateAllRules()` (946–967). The code establishes this call sequence. It does not specify the ordering contract of `listKeysForSpecialCategory` or the rule engine’s matching/precedence behavior.
- The keyword handler appends a completed inline rule to `m_keywordRules`; for the window-rule handler, a dynamic-keyword request also immediately registers the appended rule (2050–2054). This file does not show that ordinary configuration source order maps to a documented rule precedence.

**Inference and limits:** The special-category registration and subsequent lookup show how this manager consumes named category entries. The selected file does not implement or document Hyprlang’s block grammar, how block names are lexed, duplicate-key behavior, or the ordering guarantees of category-key enumeration. I therefore do not claim a specific brace syntax or runtime rule precedence from this source. The fetched source also cannot establish the host’s applied window/layer effects; host behavior and matching remain [UNK]. No negative-existence claim is made.

## Proposed C1 claim rows

| A1 | This file declares the special `windowrule` category with `name` as its key. | S? | "m_config->addSpecialCategory("windowrule", {.key = "name"});" |
| A2 | The inline handler sets `FIRST_IS_PROP` when an element starts with `match:`. | S? | "const bool FIRST_IS_PROP = el.starts_with("match:");" |
| A3 | This loop traverses `windowrule` names returned by the special-category key-list API. | S? | "for (const auto& name : m_config->listKeysForSpecialCategory("windowrule")) {" |
| A4 | This line appends the completed rule to `m_keywordRules`. | S? | "m_keywordRules.emplace_back(std::move(rule));" |

## Proposed SOURCES row

| S? | Hyprland ConfigManager.cpp — https://raw.githubusercontent.com/hyprwm/Hyprland/efb50993780079460b0cbed1363e2166a2de1d9f/src/config/legacy/ConfigManager.cpp | code | A | Hyprlang-era legacy windowrule keyword handlers, named special-category reconstruction, and reload traversal | src/config/legacy/ConfigManager.cpp:419-451,590-623,893-968,2016-2093 @ efb50993780079460b0cbed1363e2166a2de1d9f, sha256:9db68cf44048d86557d8a53068dcc40b9bd7347c7d95f38edc501565f65be62b, 90963 B | Shows callback parsing, name-keyed category consumption, and local reload call sequence; does not establish Hyprlang block grammar or engine precedence | mined | 2026-10-23 | on-release | corpus/knowledge/rule-attribution-r24.md |

## Commands, receipts, and touched surfaces

Source URL fetched (ordinary raw GitHub request): `https://raw.githubusercontent.com/hyprwm/Hyprland/efb50993780079460b0cbed1363e2166a2de1d9f/src/config/legacy/ConfigManager.cpp`.

Exact fetch command:

```sh
timeout 45 curl -fsSL 'https://raw.githubusercontent.com/hyprwm/Hyprland/efb50993780079460b0cbed1363e2166a2de1d9f/src/config/legacy/ConfigManager.cpp' -o '/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-24/fetch/w1/SrcLegacyConfig-1.bin' && sha256sum '/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-24/fetch/w1/SrcLegacyConfig-1.bin' && wc -c '/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-24/fetch/w1/SrcLegacyConfig-1.bin'
```

Outcome: exit 0; `sha256:9db68cf44048d86557d8a53068dcc40b9bd7347c7d95f38edc501565f65be62b`; `90963` bytes. Fetched-file line anchors used: 419–451, 590–623, 893–968, 2016–2093. Read-only discovery used the supplied clone `/fast/scratch/hyaku/mado-r24/src/Hyprland-v0.56.2` with the `windowrule|layerrule` search; source quotations were read from the fetched receipt above.

Exact successful quote-check command: `timeout 15 python3 -c 'from pathlib import Path; p=Path("/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-24/fetch/w1/SrcLegacyConfig-1.bin"); text=" ".join(p.read_bytes().decode("utf-8").split()); quotes=["m_config->addSpecialCategory(\"windowrule\", {.key = \"name\"});", "const bool FIRST_IS_PROP = el.starts_with(\"match:\");", "for (const auto& name : m_config->listKeysForSpecialCategory(\"windowrule\")) {", "m_keywordRules.emplace_back(std::move(rule));"]; print("\\n".join(str(len(q.split()))+" words; quote present="+str(" ".join(q.split()) in text)+": "+q for q in quotes))'`. Output: A1–A4 had `4`, `5`, `7`, and `1` whitespace-separated words respectively; every `quote present=True`. An earlier draft of the checker exited with a Python `SyntaxError` in its f-string before producing a check; the corrected checker passed.

Touched surfaces: wrote this report and the required fetch receipt only. No other lane files, including `corpus/SOURCES.md` or the knowledge note, were edited. No tools were installed or updated. No host state was changed; no build, tests, or counters were run. No source files outside the specified read-only clone and pinned raw fetch were modified.

Report: `.ufo/waves/round-24/w1/reports/SrcLegacyConfig.md`
Fetch receipt: `.ufo/waves/round-24/fetch/w1/SrcLegacyConfig-1.bin`
