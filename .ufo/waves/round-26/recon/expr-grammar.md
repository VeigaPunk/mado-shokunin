# hyprlang 0.6.8 `{{…}}` expressions

Recon for round-26 C2 data seats. This is a reading of the grammar, not a resolver.

Pins:

- hyprlang tag `v0.6.8`. Tarball `https://github.com/hyprwm/hyprlang/archive/refs/tags/v0.6.8.tar.gz`, sha256 `d10a0778b646e04d83e8b90cc0f764fb96958c01a15c3c0678d95a40fc647ed5`. `VERSION` is `0.6.8`. `src/config.cpp` sha256 `fa1b6898f2f1676de73220450f18f09603f0c3f8833e4c0a7c42c12aebe1de3e`.
- hyprutils tag `v0.14.2` (the pin Hyprland v0.56.2 is built with). `src/string/ConstVarList.cpp` sha256 `0a83c560441914dfd3a8701ba3edb62275adfb9d95c268405814ffee713e51b7`. `src/string/String.cpp` sha256 `a92c131a45f41918388eece78f225dbeab7791bb3cd2d3761d840aefa1527bac`.
- Hyprland `efb50993780079460b0cbed1363e2166a2de1d9f` (v0.56.2). `src/config/legacy/ConfigManager.cpp` sha256 `9db68cf44048d86557d8a53068dcc40b9bd7347c7d95f38edc501565f65be62b`.
- Installed `libhyprlang.so.0.6.8` was built by GCC 16.1.1 20260625 (`.comment`). Probes below link that library. They are observations, not a tool.

`Math::CExpression` in Hyprland's `helpers/math/Expression.hpp` is a different evaluator (muParser). `ConfigManager.cpp` does not call it and does not search for `{{`. Ignore it for binds.

## Where `{{…}}` is recognised

Only in `CConfig::parseLine`, and only on the right-hand side of a line that contains `=` (`src/config.cpp:755-794`). The scan is `RHS.contains("{{")` then `RHS.find("{{")` / `RHS.find("}}")`. There is no quote state and no category state.

That RHS is every one of these, because they all go through `parseLine`:

- A variable assignment, `$NAME = …` (`config.cpp:730`, `:805-806`). The expanded text is what `parseVariable` stores (`:518-525`).
- A typed config value (int, float, vec2, string, custom) after expansion (`:831-836`, `:452-495`).
- A handler value. After expansion and escape-stripping, `h.func(LHS.c_str(), RHS.c_str())` (`:872`). Hyprland registers `bind` with `allowFlags = true` (`ConfigManager.cpp:607`), so `bind`, `bindd`, `bindl`, `bindr`, and the other flag spellings all take this path. The static wrapper (`ConfigManager.cpp:311-315`) forwards that already-expanded `v` into `CConfigManager::handleBind` (`:1492`).

Not recognised:

- The left-hand side. `$name` substitution does run on the LHS when the line is not itself a variable (`config.cpp:739-743`). `{{` on the LHS is never scanned.
- Category open/close lines (no `=`).
- A `#` comment. Comment stripping runs first (`:674-704`). A line whose first non-whitespace is `#` is a comment or a `# hyprlang` directive, not an expression.

Descriptions are not a hyprlang form. They are one comma field of a bind value, and only when the keyword carries flag `d` (`ConfigManager.cpp:1528`, `:1554-1586`). The description is expanded only because the whole RHS is expanded before `handleBind` splits on commas. Same for the dispatcher arg, the key, the mod, and the device field.

`hyprctl binds -j` was not read. `handleBind` stores the post-split strings into the keybind: dispatcher `HANDLER`, arg `COMMAND`, description `DESCRIPTION` (`ConfigManager.cpp:1630-1634`). Those strings are slices of the expanded RHS. Confidence that the handler sees the expanded text: high (source plus a library probe). Confidence that the JSON emitter copies those fields without a second parse: not checked.

## Shape of one expression

`parseExpression` (`config.cpp:619-667`) takes the bytes between `{{` and the next `}}`. The source comment says "only one per `$()`" (`:620-622`). That comment is stale. The `while (RHS.contains("{{"))` loop evaluates every non-escaped pair on the line, left to right, one operator each.

Splitting is `CConstVarList(s, 0, 's', true)` (`config.cpp:627`). Delimiter `'s'` means `std::isspace`, empty tokens dropped, each token trimmed (`hyprutils` `ConstVarList.cpp:8-25`). Space and tab both separate (probe: `{{1\t+\t2}}` → `3`).

The grammar is three tokens, not a precedence grammar:

1. Token 0 is the left operand.
2. Token 1 must be exactly `+`, `-`, `*`, or `/` (`config.cpp:629-630`). Anything else, including a missing token, is the error `Invalid expression type: supported +, -, *, /`.
3. Token 2 is the right operand.
4. Token 3 onward is ignored. Not an error. Probe: `{{1 + 2 + 3}}` → `3`, `{{1 + 2 * 3}}` → `3`. There is no precedence because the later operator is never read.

No parentheses. `(` and `)` are ordinary token characters. Probe: `{{(1 + 2)}}` errors (stof fails on `(1`); `{{( 1 + 2 )}}` errors (the operator is not the second token).

No juxtaposition. `{{1+2}}` is one token, so it errors. The operator must be its own whitespace-delimited token.

Unary minus is not an operator token. It works only as a prefix of a numeric token: `{{-2 + 5}}` → `3`. `{{- 2 + 5}}` errors.

`}}` is not escapable. The source says a `}}` escape would be an invalid expression anyway (`config.cpp:781`). The first `}}` closes the open `{{`. Nesting does not work: `{{ {{1 + 2}} + 3 }}` tries to parse ` {{1 + 2` and errors (probe).

Several pairs in one value are concatenation, not a list. `{{1 + 2}}{{3 + 4}}` → `37`. `a {{1 + 2}} b` → `a 3 b`. Quotes are not special: `"{{1 + 2}}"` → `"3"` (probe).

## Operands

Each operand (`config.cpp:632-656`):

- If the token's exact text equals some variable's `name`, use that variable's stored `value` and `std::stof` it. Failure: `Failed to parse expression: value 1 holds a variable that does not look like a number`.
- Otherwise `std::stof` the token itself. Failure: `Failed to parse expression: value 1 does not look like a number or the variable doesn't exist`.

Both messages say "value 1" for the right operand too (`:651`, `:655`). Copy-paste in the source. Empty expression, before the split: `Expression is empty` (`:624-625`). `{{ }}` is not empty; the split yields no tokens, so it is the invalid-operator error (probe).

`std::stof` does not require the whole token to be consumed. Probe: `{{2abc + 3}}` → `5`, `{{1, + 2}}` → `3`, `{{0x10 + 1}}` → `17`, `{{1e2 + 3}}` → `103`. It also accepts `inf` and `nan`.

Lookup is exact. Names are not prefixes and do not include `$`. The variable list at parse start is a copy of the environment (`clearState`, `config.cpp:1073-1074`), then user variables are inserted and the vector is re-sorted longest-name-first (`parseVariable`, `:525`). So `{{SHELL + 1}}` looks up the env var `SHELL` if it was copied in. A non-numeric value then fails stof.

## `$var` versus a bare name

Two different mechanisms, both real:

1. Bare name inside the braces: `{{MY_VAR + 2}}`. `parseExpression` looks the name up. Upstream test: `$MY_VAR = 1337`, `$EXPR_VAR = {{MY_VAR + 2}}`, `testExpr = {{EXPR_VAR - 4}}` stores int `1335` (`tests/config/config.conf:13-18`, `tests/parse/main.cpp:252`). Reproduced against `libhyprlang.so.0.6.8`.
2. Dollar form: `{{$MY_VAR + 2}}`. Before expressions, the same loop replaces every `$` + name in the RHS (`config.cpp:736-745`, `replaceInString` in hyprutils `String.cpp:86-94`). Longest name first, so `$MY_VAR_2` is not eaten by `$MY_VAR`. The replacement repeats up to 100 times (`:732`). On the 100th hit the line errors `Expanding variables exceeded max iteration limit` (`:799-801`). After substitution the expression sees a numeric literal. Probe: `$MY_VAR = 10` then `{{$MY_VAR + 2}}` → `12`, and `{{ MY_VAR + 2 }}` → `12`.

`$` substitution also rewrites text inside an escaped expression, because it runs before the escape test. Upstream: `$DYNAMIC_EXPRESSION = moved: {{$MOVING_VAR / 2}} expr: \{{$MOVING_VAR / 2}}` stores the number on the left and the literal `{{500 / 2}}` (after `$MOVING_VAR` was replaced) on the right (`config.conf:30-31`, `main.cpp:264`).

If a variable's stored value still contains `{{…}}`, the assignment that interpolates it will parse those braces, unless they are escaped. Escapes are not stripped on the variable line itself (see below), so a variable can hold `\{{10 + 10}}` and a later non-variable line turns that into the literal `{{10 + 10}}` (`config.conf:27-28`, `main.cpp:263`). Probe confirmed `imbed` → `{{10 + 10}}`.

## Arithmetic and the text that replaces the braces

The operation is IEEE binary32, not integer arithmetic (`config.cpp:635-662`): `std::stof` to `float`, then `+ - * /` on `float`. There is no divide-by-zero check. `{{5 / 2}}` is `2.5`, not `2`. `{{1 / 3}}` is `0.33333334`. `{{1 / 0}}` is `inf`, `{{-1 / 0}}` is `-inf`, `{{0 / 0}}` is `-nan` (all three observed from the installed library).

The float is spliced back with `std::format("{}", RESULT.value())` (`config.cpp:791`). That call was compiled into `libhyprlang.so` by GCC 16.1.1. On this host the observed strings are the shortest round-trip general format, not `printf %f` and not "always an integer":

| Expression | Text written into the RHS |
|---|---|
| `{{1 + 2}}` | `3` |
| `{{8 - 10}}` | `-2` |
| `{{4 / 2}}` | `2` |
| `{{5 / 2}}` | `2.5` |
| `{{1 / 3}}` | `0.33333334` |
| `{{1 / 1000}}` | `0.001` |
| `{{1 / 10000}}` | `1e-04` |
| `{{100000 + 0}}` | `1e+05` |
| `{{99999 + 1}}` | `1e+05` |
| `{{1000000 + 0}}` | `1e+06` |
| `{{1 / 0}}` | `inf` |
| `{{-1 / 0}}` | `-inf` |
| `{{0 / 0}}` | `-nan` |
| `{{-0 + 0}}` | `0` |

Upstream tests only pin whole numbers that stay decimal (`-2`, `5`, `13`, `500`, `250`, `1335`, `2678`). Do not assume every whole float stays decimal: `100000` becomes `1e+05`. Floats above 2^24 are not exact integers (`16777217` formats as `16777216` under the same `std::format`; that last row was a standalone format probe, not a library expression probe).

What happens to that text depends on the key:

- String, or any handler (including bind): the text is kept. A bind arg of `{{5 / 2}}` is the four characters `2.5`. A bind arg of `{{1000000 + 0}}` is `1e+06`.
- Float key: `std::stof` again (`config.cpp:467`). `2.5` works (probe).
- Int key: `configStringToInt` (`:185-274`, called at `:455`). After hex and `rgb`/`rgba`/`true`/`false` prefixes, `isNumber(VALUE, false)` must succeed (`:265`, hyprutils `String.cpp:50-84` with `allowfloat` false): optional leading `-`, then digits only, must end with a digit. Then `std::stoll`. So `3` and `-2` are accepted. `2.5`, `1e+05`, `1e+06`, `inf`, `-nan` are rejected with `cannot parse "<text>" as an int.` (probe). The expression itself succeeded; the int conversion is a second failure.
- Vec2: one space, then `stof` each side (`config.cpp:474-485`). `{{1 + 2}} {{4 + 5}}` stores `3` and `9` (probe). A comma is not the vec2 separator.

## Escaping

A `{{` is an expression only when the number of immediately preceding `\` is even, including zero (`config.cpp:757-776`). Odd means "this `{{` is literal; keep looking." The check is skipped when `{{` is at index 0, which is correct (nothing precedes it).

After the expansion loop, non-variable lines strip escapes (`:808-827`):

- `\\` becomes `\`.
- `\{` becomes `{`.
- `\}` becomes `}`.
- A backslash before any other character stays.
- A final lone `\` stays (the loop stops at `length - 1`).

Variable lines return at `:805-806`, before that strip. The backslashes are stored. They take effect when a later non-variable line interpolates the variable.

Observed, matching `tests/parse/main.cpp:256-264`:

| Source RHS | Stored string (non-variable key) |
|---|---|
| `\{{1 + 2}}` | `{{1 + 2}}` |
| `{\{1 + 2}}` | `{{1 + 2}}` (the `\{` is not the two-character sequence `{{`, so nothing evaluates, then the slash is stripped) |
| `\{\{3 + 8}}` | `{{3 + 8}}` |
| `\\{{10 - 5}}` | `\5` (even slash count, so the expression runs, then `\\` becomes `\`) |

A physical line that ends in `\` is a continuation, not an escape. `getNextLine` (`config.cpp:53-62`) deletes that backslash and concatenates the next line before `parseLine`. An escape backslash has to have a non-continuation character after it on the same physical line.

## Unclosed braces

If `}}` is missing, the loop `break`s (`config.cpp:792-793`) and the line is not an error. The literal `{{…` stays in the value. Probe: `{{1 + 2` is stored as `{{1 + 2`. A bind handler would see those characters. A following valid pair on the same line is not reached once an unclosed pair sits in front of it, because the search starts at the first unescaped `{{` and gives up when that one has no closer.

`#` interacts with this. Comment cutting happens first, so `{{1 + 2 # }}` loses the closer and is kept literal. `{{1 + 2}} # {{9 + 9}}` stores `3` (probe): the second pair is in the comment.

## Errors: rejected line, or literal kept

Closed but invalid: `parseLine` sets the error and returns immediately (`config.cpp:786-788`). The value is not written and the handler is not called. Escape stripping does not run for that line.

`parseFile` does not stop the file (`:1032-1039`). Hyprland builds the parser with `throwAllErrors = true` (`ConfigManager.cpp:486`), so every later error is appended as `Config error in file <path> at line <n>: <message>`. Earlier and later good lines still apply. Probe (stream, same `parseLine`): a bad `{{1+2}}` left the key at its default, and the next line `{{8 - 3}}` stored `5`. The good bind line had already called the handler.

`# hyprlang noerror true` is honored only by `parseFile` (`config.cpp:1034` checks `currentFlags.noError`; `parseRawStream` at `:982` does not). The flag stops the error from being recorded. It does not make the bad line apply. Hyprland parses files, not the stream API.

Expression errors a data seat will actually see:

- `Expression is empty`
- `Invalid expression type: supported +, -, *, /`
- `Failed to parse expression: value 1 holds a variable that does not look like a number`
- `Failed to parse expression: value 1 does not look like a number or the variable doesn't exist`
- `Expanding variables exceeded max iteration limit` (the `$` loop, not the operator parser)
- `cannot parse "<formatted>" as an int.` when the key is an int and the formatted float is not a plain integer token

Unclosed braces are the other outcome: no error, literal kept.

## What the bind handler sees

Yes. It sees the expanded string.

Order in `parseLine`: `$` substitution, then every `{{…}}` replacement, then (non-variables) backslash stripping, then the handler (`config.cpp:732-794`, `:808-827`, `:872`). `handleBind` (`ConfigManager.cpp:1492-1654`) never looks for `{{`. It splits the received value with `CVarList` on commas (`:1554`) into mod, key, optional device (`k`), optional description (`d`), dispatcher, and arg.

Library probe, handler registered as `bindd`:

```
bindd = SUPER, G, desc {{1 + 2}}, exec, notify {{4 + 5}}
```

The callback received `SUPER, G, desc 3, exec, notify 9`. Description and arg were both already numbers. `handleBind` would store description `desc 3` and arg `notify 9`.

Escaped or unclosed braces are the exception: the handler then sees the literal brace text, because hyprlang left it in the RHS on purpose.
