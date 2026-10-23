# SrcWsRuleLegacy — source-opening report

## Behavior

The pinned legacy parser registers the `workspace` Hyprlang keyword and routes its callback to `CConfigManager::handleWorkspaceRules`. That handler splits the value at the first comma, trims and resolves the first field as the workspace identifier/name, then parses the remaining comma-separated rule list. For `gapsin:` and `gapsout:`, it builds a space-separated `CVarList2`, creates `CCssGapData`, and calls `parseGapData`; caught parse exceptions become workspace-rule errors. Successful parsing records the resolved workspace name and ID and calls `workspaceRuleMgr()->replaceOrAdd`.

`CCssGapData::parseGapData` is inline in `ComplexDataTypes.hpp`. Its constructors implement one integer as all four sides; two as vertical/horizontal; three as top/horizontal/bottom; and four as top/right/bottom/left. Each token is converted through `std::stoi`. The default switch branch warns about too many arguments and constructs from the first four tokens. These are source-code findings, not runtime measurements.

## Gates and exact actions

- Read `round-27/registration.md`, the `SOURCES.md` header and last rows, and the complete existing S162 row before opening the source. The inventory header says only `status`, `recheck`, and `used-by` change in place.
- Existing S162 URL was found in `SOURCES.md`. The `src/config/shared/complex/ComplexDataTypes.hpp` and `src/config/values/types/CssGapValue.hpp` path searches found no inventory rows.
- Fetch commands, each completed without stdout or reported error:

  ```sh
  mkdir -p /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-27/fetch && timeout 60 prlimit --as=4000000000 -- curl -fsSL https://raw.githubusercontent.com/hyprwm/Hyprland/efb50993780079460b0cbed1363e2166a2de1d9f/src/config/legacy/ConfigManager.cpp -o /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-27/fetch/SrcWsRuleLegacy.bin
  timeout 60 prlimit --as=4000000000 -- curl -fsSL https://raw.githubusercontent.com/hyprwm/Hyprland/efb50993780079460b0cbed1363e2166a2de1d9f/src/config/values/types/CssGapValue.hpp -o /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-27/fetch/SrcWsRuleLegacy-CssGapValue.hpp.bin
  timeout 60 prlimit --as=4000000000 -- curl -fsSL https://raw.githubusercontent.com/hyprwm/Hyprland/efb50993780079460b0cbed1363e2166a2de1d9f/src/config/shared/complex/ComplexDataTypes.hpp -o /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-27/fetch/SrcWsRuleLegacy-ComplexDataTypes.hpp.bin
  ```

- Python quote check read each fetched file as UTF-8, checked every quoted excerpt against whitespace-collapsed full-file bytes and its stated line range, and enforced at most 25 words per excerpt. All eight excerpts passed (`OK`); the excerpts and anchors are below.
- Coredump baseline command: `timeout 30 coredumpctl list --no-pager --no-legend | /usr/bin/grep -c /usr/bin/Hyprland` → `1338`.
- Same command after source opening → `1338`; delta `0`. No Hyprland process was started.
- No C1/C2 counter, tests, or compositor were run; no tool was installed.

## Provenance, anchors, and located quotes

### Existing source S162 — ConfigManager.cpp

URL: `https://raw.githubusercontent.com/hyprwm/Hyprland/efb50993780079460b0cbed1363e2166a2de1d9f/src/config/legacy/ConfigManager.cpp`  
Commit: `efb50993780079460b0cbed1363e2166a2de1d9f`  
Fetched artifact: `.ufo/waves/round-27/fetch/SrcWsRuleLegacy.bin`  
SHA-256: `9db68cf44048d86557d8a53068dcc40b9bd7347c7d95f38edc501565f65be62b`; 90,963 bytes; 2,184 lines. This matches the S162 digest and byte count.

Relevant new anchors: `src/config/legacy/ConfigManager.cpp:335-343` (callback wrapper), `:609` (keyword registration), and `:1676-1792` (workspace-rule handler).

- `ConfigManager.cpp:1678` — “`const auto FIRST_DELIM = value.find_first_of(',');`” This locates the selector/rule split at the first comma.
- `ConfigManager.cpp:1719` — “`wsRule.m_gapsIn->parseGapData(varlist);`” This shows the `gapsin` branch delegates token interpretation to `CCssGapData`.
- `ConfigManager.cpp:1781` — “`CVarList2 rulesList(std::string(rules), 0, ',', true);`” This anchors construction of the comma-separated rule list.

### Candidate new source — ComplexDataTypes.hpp

URL: `https://raw.githubusercontent.com/hyprwm/Hyprland/efb50993780079460b0cbed1363e2166a2de1d9f/src/config/shared/complex/ComplexDataTypes.hpp`  
Commit: `efb50993780079460b0cbed1363e2166a2de1d9f`  
Fetched artifact: `.ufo/waves/round-27/fetch/SrcWsRuleLegacy-ComplexDataTypes.hpp.bin`  
SHA-256: `95733223b115510dda23e753aae64e373205cc7081b0eeb204df866ea7e68807`; 6,116 bytes; 178 lines. Candidate anchors: `src/config/shared/complex/ComplexDataTypes.hpp:80-120`.

- `ComplexDataTypes.hpp:84` — “`CCssGapData(int64_t vertical, int64_t horizontal) : m_top(vertical), m_right(horizontal), m_bottom(vertical), m_left(horizontal) {};`” This specifies the two-value vertical/horizontal mapping.
- `ComplexDataTypes.hpp:85` — “`CCssGapData(int64_t top, int64_t horizontal, int64_t bottom) : m_top(top), m_right(horizontal), m_bottom(bottom), m_left(horizontal) {};`” This specifies how the third value maps in the three-value form.
- `ComplexDataTypes.hpp:94-95` — “`const auto toInt = [](std::string_view string) -> int { return std::stoi(std::string(string)); };`” This shows that each parsed token is converted through `std::stoi`.
- `ComplexDataTypes.hpp:114-116` — “`Log::logger->log(Log::WARN, "Too many arguments provided for gaps."); *this = CCssGapData(toInt(varlist[0]), toInt(varlist[1]), toInt(varlist[2]), toInt(varlist[3]));`” This anchors the warning and four-value construction in the default branch.

### Supporting declaration — CssGapValue.hpp (not a parser candidate)

URL: `https://raw.githubusercontent.com/hyprwm/Hyprland/efb50993780079460b0cbed1363e2166a2de1d9f/src/config/values/types/CssGapValue.hpp`  
Commit: `efb50993780079460b0cbed1363e2166a2de1d9f`  
Fetched artifact: `.ufo/waves/round-27/fetch/SrcWsRuleLegacy-CssGapValue.hpp.bin`  
SHA-256: `5780a6e1565ddc845e01924ed5155a547f31ab9a52c204c7a0428c5d043c3511`; 1,047 bytes; 35 lines. It leads to the complex type but does not define `parseGapData`, so no SOURCES row is proposed for it.

- `CssGapValue.hpp:26` — “`const Config::CCssGapData& value() const;`” This shows the value wrapper exposes the complex gap data by reference.
- `CssGapValue.hpp:33` — “`Config::CCssGapData m_default;`” This shows the wrapper stores a `CCssGapData` default value.

## SOURCES proposals

**S162 used-by extension:** retain the existing S162 row and append `corpus/knowledge/workspace-rules-r27.md` to its current `used-by` value (`corpus/knowledge/rule-attribution-r24.md, corpus/knowledge/bind-table-r25.md, corpus/knowledge/animation-table-r26.md`). The new handler anchors for the knowledge document are `ConfigManager.cpp:335-343,609,1676-1792`. No inventory file was edited; the existing source row's anchor cell is left untouched, consistent with the inventory header's in-place-change rule.

**Candidate new row** (the inventory ended at S177 when inspected; assign an ID at integration):

`| S? | Hyprland v0.56.2 CCssGapData parser — https://raw.githubusercontent.com/hyprwm/Hyprland/efb50993780079460b0cbed1363e2166a2de1d9f/src/config/shared/complex/ComplexDataTypes.hpp | code | A | Four-sided gap parsing called by legacy workspace-rule gapsin and gapsout | src/config/shared/complex/ComplexDataTypes.hpp:80-120 @ efb50993780079460b0cbed1363e2166a2de1d9f, sha256:95733223b115510dda23e753aae64e373205cc7081b0eeb204df866ea7e68807, 6116 B | Maps one to four integer fields to CSS-like top/right/bottom/left values; the default branch warns and constructs from the first four tokens | mined | 2026-10-23 | on-release | corpus/knowledge/workspace-rules-r27.md |`

## Touched surfaces, out of scope, and limits

Only the report and the three named fetched artifacts under `.ufo/waves/round-27/fetch/` were written. `corpus/SOURCES.md` was read only. The supporting `CssGapValue.hpp` fetch was used to follow the include to the parser definition; it is explicitly not proposed as an additional corpus source.

This opening establishes what the pinned source implements, not that every host uses this build, what Hyprlang accepts around these handlers, how `CVarList2` treats edge cases, the workspace-rule manager's later ordering/effect behavior, or what `hyprctl workspacerules -j` emits at runtime. No gate or runtime claim is made.