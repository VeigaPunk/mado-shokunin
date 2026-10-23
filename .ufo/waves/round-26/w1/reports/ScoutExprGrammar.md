# ScoutExprGrammar

Verdict: `{{…}}` is a one-operator float splice on the RHS of any `=` line, done inside hyprlang before Hyprland's bind handler runs. The handler sees the expanded string. Full write-up: `.ufo/waves/round-26/recon/expr-grammar.md`.

No resolver written. No counter run. Nothing under `tools/` touched.

## What I read

- hyprlang `v0.6.8` tarball `https://github.com/hyprwm/hyprlang/archive/refs/tags/v0.6.8.tar.gz`, sha256 `d10a0778b646e04d83e8b90cc0f764fb96958c01a15c3c0678d95a40fc647ed5`. Grammar is `src/config.cpp` (`parseExpression` at `:619-667`, RHS scan at `:755-794`, escape strip at `:808-827`, handler call at `:872`). File sha256 `fa1b6898f2f1676de73220450f18f09603f0c3f8833e4c0a7c42c12aebe1de3e`.
- hyprutils `v0.14.2` `src/string/ConstVarList.cpp` and `src/string/String.cpp` (`isNumber`, `replaceInString`).
- Hyprland `efb50993780079460b0cbed1363e2166a2de1d9f` `src/config/legacy/ConfigManager.cpp` (`handleBind` `:1492-1654`, `bind` registered `:607` with flags, `throwAllErrors = true` at `:486`).
- Installed `libhyprlang.so.0.6.8`, `.comment` = GCC 16.1.1 20260625. Probes linked that library from `/tmp` and were not kept in the lane.

`Math::CExpression` (muParser, Hyprland `Expression.hpp`) is a different system. `ConfigManager.cpp` does not mention `{{` or that type.

## Findings

Confidence high unless noted.

**Where.** Only the RHS of a `parseLine` that contains `=`. That covers variable values, typed config values, and every handler, including `bind` and flag forms (`bindd`, …). Not the LHS (except `$var` substitution), not category lines, not `#` comments. Descriptions are not hyprlang syntax. Flag `d` makes one comma field a description (`ConfigManager.cpp:1528`, `:1582`). It is expanded only because the whole RHS is expanded first.

**Operator.** Exactly three whitespace-separated tokens: operand, one of `+ - * /`, operand. Extra tokens are ignored, not a syntax error (`{{1 + 2 * 3}}` → `3`). No precedence, no parentheses, no `1+2` juxtaposition. Unary minus only as part of a number token (`-2`), not as its own token. The first `}}` closes the first `{{`; nesting errors. Several pairs on one line are left-to-right concatenation (`{{1 + 2}}{{3 + 4}}` → `37`). Quotes do not protect braces (`"{{1 + 2}}"` → `"3"`).

**Arithmetic.** binary32 via `std::stof` and float `+ - * /`. Not integer division: `{{5 / 2}}` → `2.5`. No divide-by-zero check: `inf`, `-inf`, `-nan`. The replacement text is `std::format("{}", float)` (`config.cpp:791`). Observed from this `libhyprlang.so`: whole small results stay decimal (`3`, `-2`, `2`); `1/3` is `0.33333334`; `100000` is `1e+05`; `1000000` is `1e+06`; `1/10000` is `1e-04`. An int key then requires `isNumber(text, false)` (optional `-`, digits only). `2.5` and `1e+05` fail the key with `cannot parse "…" as an int.` even though the expression succeeded. String keys and bind handlers keep the formatted text.

**`$var`.** Two forms. `{{MY_VAR + 2}}` looks the bare name up in the variable table (env copied in at `clearState`, `:1074`, plus user variables, longest name first). `{{$MY_VAR + 2}}` is rewritten by the `$` pass before the expression runs. Upstream test `$MY_VAR = 1337` / `{{EXPR_VAR - 4}}` is int `1335`; reproduced. `$` expansion also rewrites inside an escaped pair. Cap 100 iterations, then `Expanding variables exceeded max iteration limit`.

**Escaping.** Odd run of `\` immediately before `{{` means "not an expression" (`:757-776`). On non-variable lines only, `\\` → `\`, `\{` → `{`, `\}` → `}`. Variable assignments return before that strip (`:805`), so they can store a backslash that a later line interprets. `\{{1 + 2}}` stores `{{1 + 2}}`. `\\{{10 - 5}}` stores `\5`. A trailing `\` at end of a physical line is continuation (`getNextLine`, `:53-62`), not an escape.

**Unclosed.** No `}}`: not an error. The literal, including `{{`, stays and the handler would see it (`{{1 + 2` stored as itself). A `#` comment is cut first, so it can steal the closer.

**Errors.** Closed-but-invalid: line not applied, handler not called, file continues. Hyprland records every such line (`throwAllErrors`). Messages: `Expression is empty`; `Invalid expression type: supported +, -, *, /`; `Failed to parse expression: value 1 holds a variable that does not look like a number`; `Failed to parse expression: value 1 does not look like a number or the variable doesn't exist` (the right operand uses the same "value 1" wording, `:651` and `:655`). `# hyprlang noerror true` is honored by `parseFile` only (Hyprland's path): the error is not recorded, and the line still does not apply.

**Bind handler.** Yes, it sees the expanded string. Probe, handler on `bindd`: `SUPER, G, desc {{1 + 2}}, exec, notify {{4 + 5}}` was delivered as `SUPER, G, desc 3, exec, notify 9`. `handleBind` comma-splits that and stores description and arg from it (`:1630-1634`). It does not parse `{{` itself. Escaped and unclosed braces are the cases where the stored text still contains braces.

## Commands

```
curl -fsSL -o /tmp/mado-r26-hyprlang/v0.6.8.tar.gz \
  https://github.com/hyprwm/hyprlang/archive/refs/tags/v0.6.8.tar.gz
curl -fsSL -o /tmp/mado-r26-hyprlang/utils/ConstVarList.cpp \
  https://raw.githubusercontent.com/hyprwm/hyprutils/v0.14.2/src/string/ConstVarList.cpp
curl -fsSL -o /tmp/mado-r26-hyprlang/utils/String.cpp \
  https://raw.githubusercontent.com/hyprwm/hyprutils/v0.14.2/src/string/String.cpp
curl -fsSL -o /tmp/mado-r26-hyprlang/hl/ConfigManager.cpp \
  https://raw.githubusercontent.com/hyprwm/Hyprland/efb50993780079460b0cbed1363e2166a2de1d9f/src/config/legacy/ConfigManager.cpp
g++ -std=c++23 -O2 -o /tmp/mado-r26-hyprlang/probe /tmp/mado-r26-hyprlang/probe.cpp -lhyprlang
g++ -std=c++23 -O2 -o /tmp/mado-r26-hyprlang/probe2 /tmp/mado-r26-hyprlang/probe2.cpp -lhyprlang
```

Probe results are the tables above. No lane file other than this report and `recon/expr-grammar.md` was written.

## Unknowns

- The `hyprctl binds -j` serializer was not opened. The handler stores expanded arg and description; that the JSON copies those fields is unread.
- Shortest-roundtrip boundaries beyond the probed values were not enumerated. The string is whatever this library's `std::format("{}", float)` emits.
- `std::stof` / `std::isspace` follow the process C locale. hyprlang and `ConfigManager.cpp` do not call `setlocale`. The process entry point was not checked.
