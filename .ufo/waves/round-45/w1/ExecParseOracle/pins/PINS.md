# Pins this seat pulled itself (the round's frozen `fetch/` is untouched)

All URLs fetched 2026-10-26 by ExecParseOracle; sha256 in `SHA256SUMS.txt` (computed with `sha256sum`,
not typed). Everything here is upstream source, kept verbatim for citation.

| file | URL | version |
|---|---|---|
| `src_string_VarList2.cpp` | `https://raw.githubusercontent.com/hyprwm/hyprutils/v0.14.2/src/string/VarList2.cpp` | hyprutils **v0.14.2** (the host's `hyprutils 0.14.2-1`) |
| `include_hyprutils_string_VarList2.hpp` | `…/v0.14.2/include/hyprutils/string/VarList2.hpp` | v0.14.2 |
| `include_hyprutils_string_String.hpp` | `…/v0.14.2/include/hyprutils/string/String.hpp` | v0.14.2 |
| `include_hyprutils_string_Numeric.hpp` | `…/v0.14.2/include/hyprutils/string/Numeric.hpp` | v0.14.2 |
| `hyprlang-v0.6.8-src-config.cpp` | `https://raw.githubusercontent.com/hyprwm/hyprlang/v0.6.8/src/config.cpp` | hyprlang **v0.6.8** (latest tag at fetch time) |
| `Hyprland-MiscFunctions.cpp` | `https://raw.githubusercontent.com/hyprwm/Hyprland/efb50993780079460b0cbed1363e2166a2de1d9f/src/helpers/MiscFunctions.cpp` | Hyprland **efb50993** (`0.56.2`) |

Two of these are load-bearing:

1. **`VarList2.cpp`** is the splitter `handleMonitor` runs on the value
   (`CVarList2(std::string(args))`, legacy ConfigManager.cpp:1295). Its `construct()` trims every field
   with `hyprutils::String::trim`, which uses `std::isspace`, and its escape rule is not a simple
   "backslash escapes the next character": it looks at the two characters before the delimiter. The model
   transcribes that loop, and `splitcheck.py` builds the pinned `.cpp` and compares the two on 4000 random
   strings (`receipts/splitcheck.txt`), so the transcription is checked against the source, not asserted.
2. **`hyprlang-v0.6.8-src-config.cpp`** decides what reaches the handler: `trim`, `#` comments, `##` as an
   escaped `#`, backslash line continuation, and the LHS/RHS split. This is why a comment is removed before
   `handleMonitor` ever sees the value (the tool tests the raw body for `$` and `##` before cutting the
   comment).

`Hyprland-MiscFunctions.cpp` is a **negative** pin: it contains no `isNumber`, so the unqualified
`isNumber(value)` calls in `Parser.cpp` (which has `using namespace Hyprutils::String;`) resolve to
hyprutils' `isNumber(const std::string&, bool allowfloat = false)`. That default is why
`parseTransform` rejects `3.0` but accepts `03` — see `report.md`, class T.

`varlist_driver.cpp` is mine (the C++ side of `splitcheck.py`), not upstream.

## Not pinned, therefore not claimed

* **hyprlang version actually linked by the host's Hyprland 0.56.2.** v0.6.8 is the latest tag, not
  proof of the host's build; every hyprlang statement in the report is limited to comment/trim/continuation
  behaviour that is identical in `main` and `v0.6.8` (both inspected).
* **`source =` includes, `env =`, and variable (`$name = …`) semantics.** The tool refuses any body with
  `$`, so the differential never depends on it.
* **wlr-output-management overrides** (`MonitorRuleManager.cpp:39-67`) and unsafe-fallback monitors: they
  change the rule after `get()`, which neither the tool nor this model can see in the dump.
