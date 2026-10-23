# SrcAnimConfig — Hyprland v0.56.2 legacy handlers

Date: 2026-10-23. Scope: source opening only; no control was built and no counter or Hyprland instance was run.

## Findings

`src/config/ConfigManager.cpp` at the requested commit is only the config-manager selector: its includes point to `legacy/ConfigManager.hpp` and it chooses the legacy manager for non-Lua config. The actual `animation` and `bezier` callbacks are in `src/config/legacy/ConfigManager.cpp`; both are registered there (lines 612–613). The declarations are in `src/config/legacy/ConfigManager.hpp` (lines 90–91).

Both handlers call `CVarList(args)`. Hyprland's `src/helpers/varlist/VarList.hpp` includes `<hyprutils/string/VarList.hpp>`; the v0.14.2 dependency declares comma as the default delimiter and `removeEmpty=false`. Its implementation splits on that delimiter and trims each token. Thus animation fields are positional comma-separated tokens, with empty positions retained: `[0]` node, `[1]` enabled, `[2]` speed, `[3]` bezier, `[4]` style. The same split applies to `bezier =`: `[0]` name, `[1..4]` control-point numbers.

Animation behavior (`src/config/legacy/ConfigManager.cpp:1426–1479`):

- A node absent from `Config::animationTree()` returns `no such animation`.
- The enabled expression is `parseInt(ARGS[1]).value_or(0) == 1`. Despite the following range-check and its comment, the expression is already boolean before assignment to `int64_t`, so the `0`/`1` check cannot reject another value. Unparsed/missing values fall back to zero and take the disabled branch. That branch sets the node to disabled with speed `1` and bezier `default`, then returns success; it skips speed, bezier, and style checks.
- For enabled nodes, speed must pass `isNumber(..., true)` and be greater than zero. A non-number or nonpositive value returns `invalid speed`; the local fallback assignments immediately precede those returns. The named bezier must exist or the handler returns `no such bezier`.
- It calls `setConfigForNode(node, enabled, speed, bezier, style)` before validating a nonempty style with `styleValidInConfigVar`. A style error is returned after that call; this handler source does not establish whether later config processing rolls the state back.

Bezier behavior (`:1389–1424`): it checks each of the four coordinate slots for missing input (`too few arguments`) and numeric form (`invalid point`), converts accepted values with `std::stof`, and reports `too many arguments` if `ARGS[5]` is nonempty. After these checks it calls `addBezierWithName`. This handler has no explicit nonempty-name or coordinate-range check.

For either keyword, the static Hyprlang callback converts a returned optional error string into `CParseResult::setError` (`:287–309`). This establishes the handler-to-parser error path, not whole-file rollback or user-visible logging behavior.

## Located quotes

Quotes below were checked with Python: each whitespace-collapsed quote is a substring of the whitespace-collapsed decoded source bytes. Counts are whitespace-separated words.

1. `include/hyprutils/string/VarList.hpp:14 @ hyprutils v0.14.2` — 18 words:

   ```cpp
        CVarList(const std::string& in, const size_t lastArgNo = 0, const char delim = ',', const bool removeEmpty = false);
   ```

   This teaches that the default split delimiter is a comma and that empty tokens are not removed; Hyprland reaches this declaration through `src/helpers/varlist/VarList.hpp:3`.

2. `src/config/legacy/ConfigManager.cpp:1434–1438 @ efb50993780079460b0cbed1363e2166a2de1d9f` — 24 words:

   ```cpp
       if (!Config::animationTree()->nodeExists(ANIMNAME))
           return "no such animation";

       // This helper casts strings like "1", "true", "off", "yes"... to int.
       int64_t enabledInt = ParserUtils::parseInt(ARGS[1]).value_or(0) == 1;
   ```

   This ties the first field to a real animation node and shows the enabled token's parse/default rule; see lines 1440–1447 for the ineffective post-boolean range check and disabled assignment.

3. `src/config/legacy/ConfigManager.cpp:1457–1467 @ efb50993780079460b0cbed1363e2166a2de1d9f` — 24 words:

   ```cpp
               return "invalid speed";
           }
       } else {
           speed = 10.f;
           return "invalid speed";
       }

       std::string bezierName = ARGS[3];

       if (!Animation::mgr()->bezierExists(bezierName))
           return "no such bezier";
   ```

   This shows the speed error and the required existing bezier; the positive-number test and nonpositive-speed branch are at lines 1452–1457.

4. `src/config/legacy/ConfigManager.cpp:1469–1478 @ efb50993780079460b0cbed1363e2166a2de1d9f` — 20 words:

   ```cpp
       Config::animationTree()->setConfigForNode(ANIMNAME, enabledInt, speed, ARGS[3], ARGS[4]);

       if (!ARGS[4].empty()) {
           auto ERR = Animation::mgr()->styleValidInConfigVar(ANIMNAME, ARGS[4]);

           if (!ERR.empty())
               return ERR;
       }

       return {};
   ```

   This shows the field order and that a nonempty style is validated after `setConfigForNode`; a nonempty validation error is returned to the callback.

## SOURCES ledger gate

Read `corpus/SOURCES.md` header and final rows before drafting. The proposed handler URL is already present as S162, so I did not draft a duplicate row or edit the ledger. S162 currently covers window-rule handlers and has used-by `corpus/knowledge/rule-attribution-r24.md, corpus/knowledge/bind-table-r25.md`. Proposed used-by-only extension:

`corpus/knowledge/rule-attribution-r24.md, corpus/knowledge/bind-table-r25.md, corpus/knowledge/animation-table-r26.md`

The initial `src/config/ConfigManager.cpp` URL and the supplemental hyprutils v0.14.2 VarList URL were not found in the ledger. The supplemental dependency source is recorded below for provenance; no second row is proposed for this scoped handler item.

## Fetch commands and provenance

The first fetch attempt failed because `.ufo/waves/round-26/fetch` did not exist:

```sh
timeout 90 prlimit --as=4000000000 -- curl -fsSL https://raw.githubusercontent.com/hyprwm/Hyprland/efb50993780079460b0cbed1363e2166a2de1d9f/src/config/ConfigManager.cpp -o .ufo/waves/round-26/fetch/SrcAnimConfig.bin && sha256sum .ufo/waves/round-26/fetch/SrcAnimConfig.bin && wc -c .ufo/waves/round-26/fetch/SrcAnimConfig.bin
```

Outcome: `curl: (23) client returned ERROR on write of 1369 bytes`; command exit 23. I then ran `mkdir -p .ufo/waves/round-26/fetch` and repeated that command successfully (2,597 bytes, SHA-256 `c10dc1ce6602a854121a79fb0192c9f43aa836a35f9acb98ff1789541b01f366`). That initial file was later replaced at `SrcAnimConfig.bin` with the actual handler file; the dispatcher source was re-fetched to `SrcAnimConfig-dispatcher.bin`.

Every successful raw fetch below used the exact command form `timeout 90 prlimit --as=4000000000 -- curl -fsSL <URL> -o <PATH> && sha256sum <PATH> && wc -c <PATH>`; the URL and output path shown are the literal values. Hash and byte count are the command outputs. All source files are under the named fetch directory.

| Output path | Raw URL | SHA-256; bytes | Located anchors |
|---|---|---|---|
| `.ufo/waves/round-26/fetch/SrcAnimConfig.bin` | `https://raw.githubusercontent.com/hyprwm/Hyprland/efb50993780079460b0cbed1363e2166a2de1d9f/src/config/legacy/ConfigManager.cpp` | `9db68cf44048d86557d8a53068dcc40b9bd7347c7d95f38edc501565f65be62b`; 90,963 B | `:287–309, :612–613, :1389–1479` |
| `.ufo/waves/round-26/fetch/SrcAnimConfig-dispatcher.bin` | `https://raw.githubusercontent.com/hyprwm/Hyprland/efb50993780079460b0cbed1363e2166a2de1d9f/src/config/ConfigManager.cpp` | `c10dc1ce6602a854121a79fb0192c9f43aa836a35f9acb98ff1789541b01f366`; 2,597 B | `:1–4, :15–50` |
| `.ufo/waves/round-26/fetch/SrcAnimConfig-legacy-header.bin` | `https://raw.githubusercontent.com/hyprwm/Hyprland/efb50993780079460b0cbed1363e2166a2de1d9f/src/config/legacy/ConfigManager.hpp` | `32afb1719c61ccb94b89d07cb0e5e9e6885e2531b5a3ad0507d52e89660fca5b`; 8,421 B | `:3, :14, :90–91` |
| `.ufo/waves/round-26/fetch/SrcAnimConfig-legacy-impl.bin` | `https://raw.githubusercontent.com/hyprwm/Hyprland/efb50993780079460b0cbed1363e2166a2de1d9f/src/config/legacy/ConfigManager.cpp` | `9db68cf44048d86557d8a53068dcc40b9bd7347c7d95f38edc501565f65be62b`; 90,963 B | `:287–309, :612–613, :1389–1479` (initial exploratory copy; same bytes as `SrcAnimConfig.bin`) |
| `.ufo/waves/round-26/fetch/SrcAnimConfig-complex.bin` | `https://raw.githubusercontent.com/hyprwm/Hyprland/efb50993780079460b0cbed1363e2166a2de1d9f/src/config/shared/complex/ComplexDataTypes.hpp` | `95733223b115510dda23e753aae64e373205cc7081b0eeb204df866ea7e68807`; 6,116 B | `:94` (search lead only; `CVarList2`, not the handler splitter) |
| `.ufo/waves/round-26/fetch/SrcAnimConfig-manager-header.bin` | `https://raw.githubusercontent.com/hyprwm/Hyprland/efb50993780079460b0cbed1363e2166a2de1d9f/src/config/ConfigManager.hpp` | `26b118b5adf233dc0620e914f63581ced38599c23e5706f22ee71d8eb39da38a`; 2,972 B | `:3–10` |
| `.ufo/waves/round-26/fetch/SrcAnimConfig-shared-types.bin` | `https://raw.githubusercontent.com/hyprwm/Hyprland/efb50993780079460b0cbed1363e2166a2de1d9f/src/config/shared/Types.hpp` | `337556a3fbedda3e34f31f600f4a44d4e85f53a04220f3c90d8394f98d1eb638`; 486 B | `:3–20` |
| `.ufo/waves/round-26/fetch/SrcAnimConfig-varlist.bin` | `https://raw.githubusercontent.com/hyprwm/Hyprland/efb50993780079460b0cbed1363e2166a2de1d9f/src/helpers/varlist/VarList.hpp` | `79fe2000a24c5bb42e7b586840bed8ed358cb802db049d8c2d778d240be19e80`; 148 B | `:1–7` |
| `.ufo/waves/round-26/fetch/SrcAnimConfig-hyprutils-varlist.bin` | `https://raw.githubusercontent.com/hyprwm/hyprutils/v0.14.2/include/hyprutils/string/VarList.hpp` | `9ad2fcbd5de691166b7db95de09b6bd054c9b4313deb3187e84c914dab74fc43`; 1,883 B | `:9–14, :33–36` |
| `.ufo/waves/round-26/fetch/SrcAnimConfig-hyprutils-varlist-impl.bin` | `https://raw.githubusercontent.com/hyprwm/hyprutils/v0.14.2/src/string/VarList.cpp` | `b02df8d688519366e7f20de5c3c44d21c3832316e8262ced0d295e129b166a36`; 1,189 B | `:8–26` |

## Gates, touched surfaces, and limits

- Gate result: handler URL already registered as S162; propose only the used-by extension above. `corpus/SOURCES.md` was read/searched, not edited.
- Touched surfaces: created `.ufo/waves/round-26/fetch/` with the listed source snapshots and `.ufo/waves/round-26/w1/reports/SrcAnimConfig.md`.
- Out of scope: product changes, control implementation, counter runs, host compositor inspection/runtime, and a SOURCES ledger edit.
- Limits: no Hyprland instance or tests were run; the source establishes handler return strings and callback error conversion, but not end-to-end config reload/rollback or user-visible diagnostics.
- Tool installs: none.
