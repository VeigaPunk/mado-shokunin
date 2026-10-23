# SrcHyprlangExpr — source-opening report

## Result

Opened hyprlang v0.6.8 `src/config.cpp` and every `tests/config/*.conf` file listed at the release tag. The tag resolved to commit `3a1c1b25b059dae2c6bbc46991562ba1158d125c`. Of the five test configs, `config.conf` contains expression and escaping examples; the other four contain no `{{` expression examples. The exact source URL was not already present in `corpus/SOURCES.md` (the search returned no matches).

The evidence is source inspection only. I did not run hyprlang, Hyprland, `tools/mado-binds.py`, or either counter; no runtime or C2 score is claimed.

## Findings

- `parseExpression` treats an expression as two operands and one operator. The accepted operators are `+`, `-`, `*`, and `/`; operands resolve either by matching a variable name or by parsing a float with `std::stof`. The implementation has no precedence or expression-tree evaluation path. Division is direct `left / right`; there is no explicit zero check in this function.
- `parseLine` substitutes ordinary `$NAME` references before scanning expression starts. The expression evaluator looks up its operands by variable name; the test uses the bare name inside braces (`MY_VAR`, not `$MY_VAR`).
- For `{{` starts, the parser counts consecutive preceding backslashes: an odd count escapes the start, while an even count leaves it active. It does not require escaping `}}`. A missing closing `}}` breaks out without an expression parse error, so that occurrence is not replaced. For ordinary config values, the later escape pass removes escapes before braces and collapses escaped backslashes.
- A successful float result is inserted into the surrounding RHS using `std::format("{}", result)`, with no explicit precision/format specifier.
- Empty expressions, unsupported operators, and operands that cannot be parsed as numbers return errors. `parseLine` sets the parse error and returns; the config reader adds the source line to its `Config error at line ...` diagnostic. The checked `tests/config/*.conf` fixtures contain no expression-specific failure example, so error behavior here is grounded in source, not a fixture run.

## Located quotes

1. `src/config.cpp:630` — “`return std::unexpected("Invalid expression type: supported +, -, *, /");`” This identifies the supported operator set and shows unsupported operators become expression errors.
2. `tests/config/config.conf:17` — “`$EXPR_VAR = {{MY_VAR + 2}}`” This shows a config variable referenced by its bare name inside an expression.
3. `tests/config/config.conf:20` — “`testEscapedExpr = \{{testInt + 7}}`” This is the test fixture's escaped expression-start example.
4. `src/config.cpp:786-791` — “`if (!RESULT.has_value()) { result.setError(RESULT.error()); return result; } RHS = RHS.substr(0, BEGIN_EXPR) + std::format("{}", RESULT.value()) + RHS.substr(END_EXPR + 2);`” This shows parse errors propagate and successful results are formatted into the RHS.

Each quote is under 25 whitespace-separated words. Python collapsed whitespace with the regex for one-or-more whitespace characters before checking substring membership in each fetched, decoded file; all four checks returned `True` (word counts 9, 5, 5, and 18).

## Opened files and provenance

All six files were fetched from the raw v0.6.8 tag with `curl`; the tag resolves to the commit above. Hashes and byte counts below are for the fetched files. Anchors are source line ranges in those files.

| File | Raw URL | Anchors | SHA-256 | Bytes |
|---|---|---|---|---:|
| `src/config.cpp` | https://raw.githubusercontent.com/hyprwm/hyprlang/v0.6.8/src/config.cpp | 619-667, 755-827, 983-986 | `fa1b6898f2f1676de73220450f18f09603f0c3f8833e4c0a7c42c12aebe1de3e` | 43049 |
| `tests/config/config.conf` | https://raw.githubusercontent.com/hyprwm/hyprlang/v0.6.8/tests/config/config.conf | 17-32 | `96f3ad75dbbaa31c381f6f481dd1f7893b9402c15d8c5b62ddf6bfc0bd9fa7c2` | 3517 |
| `tests/config/colors.conf` | https://raw.githubusercontent.com/hyprwm/hyprlang/v0.6.8/tests/config/colors.conf | 1-5; no expression syntax | `a44d0f507fee1ee534bed30f55270dc235c04bd5752cf0dd108672e867903b27` | 103 |
| `tests/config/error.conf` | https://raw.githubusercontent.com/hyprwm/hyprlang/v0.6.8/tests/config/error.conf | 1-5; no expression syntax | `0b6a9501a964b70607916d42b07e8637157f9298905b2fba911454c975de082e` | 77 |
| `tests/config/invalid-numbers.conf` | https://raw.githubusercontent.com/hyprwm/hyprlang/v0.6.8/tests/config/invalid-numbers.conf | 1-15; invalid numeric/color examples, no expression syntax | `bab8cf2060861406db5df46ea916058b2d639a61900d505d4720f5554fda8867` | 280 |
| `tests/config/multiline-errors.conf` | https://raw.githubusercontent.com/hyprwm/hyprlang/v0.6.8/tests/config/multiline-errors.conf | 1-20; multiline error examples, no expression syntax | `fae59a6558dd3c8ed0da7850291601c372e2829ec8393ad2bb71b1b470eeee4b` | 492 |

## Draft SOURCES row

No row was added to `corpus/SOURCES.md`; latest existing row read was S172. Proposed 11-cell row:

| S? | Hyprlang v0.6.8 expression evaluation — https://raw.githubusercontent.com/hyprwm/hyprlang/v0.6.8/src/config.cpp | code | A | Hyprlang RHS `{{…}}` expression parsing relevant to bind config values; not bind-table semantics | `src/config.cpp:619-667,755-827,983-986 @ 3a1c1b25b059dae2c6bbc46991562ba1158d125c, sha256:fa1b6898f2f1676de73220450f18f09603f0c3f8833e4c0a7c42c12aebe1de3e, 43049 B; tests/config/config.conf:17-32 @ 3a1c1b25b059dae2c6bbc46991562ba1158d125c, sha256:96f3ad75dbbaa31c381f6f481dd1f7893b9402c15d8c5b62ddf6bfc0bd9fa7c2, 3517 B; tests/config/colors.conf:1-5 @ 3a1c1b25b059dae2c6bbc46991562ba1158d125c, sha256:a44d0f507fee1ee534bed30f55270dc235c04bd5752cf0dd108672e867903b27, 103 B; tests/config/error.conf:1-5 @ 3a1c1b25b059dae2c6bbc46991562ba1158d125c, sha256:0b6a9501a964b70607916d42b07e8637157f9298905b2fba911454c975de082e, 77 B; tests/config/invalid-numbers.conf:1-15 @ 3a1c1b25b059dae2c6bbc46991562ba1158d125c, sha256:bab8cf2060861406db5df46ea916058b2d639a61900d505d4720f5554fda8867, 280 B; tests/config/multiline-errors.conf:1-20 @ 3a1c1b25b059dae2c6bbc46991562ba1158d125c, sha256:fae59a6558dd3c8ed0da7850291601c372e2829ec8393ad2bb71b1b470eeee4b, 492 B` | Documents the single-operator float evaluator, variable lookup, escaped expression starts, default result formatting, and parse-error propagation; test config covers variable and escape forms | mined | 2026-10-23 | on-release | tools/mado-binds.py |

## Commands and outcomes

Working directory for the fetch and hash commands was `/home/vgpnk/Projects/shokunin/mado-shokunin`. The fetch chain completed with exit 0 and no stdout/stderr:

```sh
timeout 120 prlimit --as=4000000000 curl -fsSL https://raw.githubusercontent.com/hyprwm/hyprlang/v0.6.8/src/config.cpp -o /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-26/fetch/SrcHyprlangExpr.bin && timeout 120 prlimit --as=4000000000 curl -fsSL https://raw.githubusercontent.com/hyprwm/hyprlang/v0.6.8/tests/config/config.conf -o /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-26/fetch/SrcHyprlangExpr-config.conf.bin && timeout 120 prlimit --as=4000000000 curl -fsSL https://raw.githubusercontent.com/hyprwm/hyprlang/v0.6.8/tests/config/colors.conf -o /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-26/fetch/SrcHyprlangExpr-colors.conf.bin && timeout 120 prlimit --as=4000000000 curl -fsSL https://raw.githubusercontent.com/hyprwm/hyprlang/v0.6.8/tests/config/error.conf -o /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-26/fetch/SrcHyprlangExpr-error.conf.bin && timeout 120 prlimit --as=4000000000 curl -fsSL https://raw.githubusercontent.com/hyprwm/hyprlang/v0.6.8/tests/config/invalid-numbers.conf -o /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-26/fetch/SrcHyprlangExpr-invalid-numbers.conf.bin && timeout 120 prlimit --as=4000000000 curl -fsSL https://raw.githubusercontent.com/hyprwm/hyprlang/v0.6.8/tests/config/multiline-errors.conf -o /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-26/fetch/SrcHyprlangExpr-multiline-errors.conf.bin
```

Read-only tag resolution from `/tmp`:

```text
timeout 30 prlimit --as=4000000000 git ls-remote https://github.com/hyprwm/hyprlang.git refs/tags/v0.6.8 'refs/tags/v0.6.8^{}'
3a1c1b25b059dae2c6bbc46991562ba1158d125c  refs/tags/v0.6.8
```

Hash/size command was `sha256sum .ufo/waves/round-26/fetch/SrcHyprlangExpr*.bin && wc -lc .ufo/waves/round-26/fetch/SrcHyprlangExpr*.bin`; it returned the hashes and counts listed above (line/byte counts: 5/103, 191/3517, 5/77, 15/280, 20/492, and 1158/43049, respectively). The exact raw URL search in `corpus/SOURCES.md` returned `No matches found`. The expression-marker search over the five fetched `tests/config/*.conf` files found hits only in `config.conf` at lines 17-32.

One read-tool discrepancy: its initial bare-URL view reported `src/config.cpp` as 1,164 lines, while `wc -l` on the curl-fetched bytes reported 1,158. Line anchors and quote checks above are based on the fetched bytes. This discrepancy was reported to `xd://report_issue`.

## Surfaces, limits, and artifacts

- Wrote only this requested report and the six source snapshots under `.ufo/waves/round-26/fetch/`.
- Did not edit product code, counters, harness, or `corpus/SOURCES.md`; no control scoring, build, test, lint, or runtime execution was performed. No tools were installed.
- The source grounds Hyprlang expression parsing, not the full Hyprland bind resolver, source-file traversal, or equivalence to `hyprctl binds -j`.

Report: `.ufo/waves/round-26/w1/reports/SrcHyprlangExpr.md`
