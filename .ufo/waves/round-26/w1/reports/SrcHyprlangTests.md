# SrcHyprlangTests — hyprlang v0.6.8 expression test sources

## Scope and outcome

Opened the two requested raw test paths: `tests/config/config.conf` and `tests/parse/main.cpp` at hyprlang tag `v0.6.8` (tag commit `3a1c1b25b059dae2c6bbc46991562ba1158d125c`). These are source observations only; the upstream tests were not built or executed, and no C1/C2 counter or control was run. The source is relevant to `tools/mado-binds.py` as a pinned reference for expression input, returned typed values, and escaping.

The config sets `$MY_VAR = 1337`, assigns `$EXPR_VAR = {{MY_VAR + 2}}`, and then sets `testExpr = {{EXPR_VAR - 4}}` (config lines 13, 17–18). The C++ test expects `testExpr` to be 1335 (line 252). The test also changes `testExpr` dynamically to `{{EXPR_VAR * 2}}` and expects `1339L * 2` (lines 317–320).

Escaping is explicitly covered: `testEscapedExpr = \{{testInt + 7}}` is expected as the literal string `{{testInt + 7}}` (config line 20; C++ line 256). Further assertions cover backslash/expression combinations and embedded/dynamic escaped expressions (config lines 21–32; C++ lines 257–264, 313–315).

**Float limitation:** the opened fixture tests `testFloat = 123.456` as a float (`123.456f`, config line 10; C++ line 215), but that input is not a `{{…}}` expression. No float-expression input/result pair appears in these opened test files. This report does not infer float-expression behavior from the literal-float assertion.

## Located quotes

> `$EXPR_VAR = {{MY_VAR + 2}}`
> `testExpr = {{EXPR_VAR - 4}}`

`tests/config/config.conf:17-18`. With the earlier `MY_VAR = 1337` assignment at line 13, this gives the variable-dependent expression input whose expected `testExpr` value is asserted below.

> `EXPECT(std::any_cast<int64_t>(config.getConfigValue("testExpr")), 1335);`

`tests/parse/main.cpp:252`. This asserts the integer result 1335 for the chained variable/expression input in the config.

> `EXPECT(std::any_cast<float>(config.getConfigValue("testFloat")), 123.456f);`

`tests/parse/main.cpp:215`. This checks the ordinary decimal float fixture, not a braced arithmetic expression; the distinction is the float-coverage limit noted above.

> `EXPECT(std::any_cast<const char*>(config.getConfigValue("testEscapedExpr")), std::string{"{{testInt + 7}}"});`

`tests/parse/main.cpp:256`. This checks that the escaped config input at line 20 remains literal braces and text instead of being evaluated.

The four quotes above were checked with Python by whitespace-collapsing both quote and fetched source text and testing substring membership; the final check passed all four.

## Provenance and exact commands

Raw-source fetches (both commands returned successfully; `curl -f` emitted no body/status text because it was run with `-s`):

```text
mkdir -p /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-26/fetch && timeout 120 prlimit --as=4000000000 curl -fsSL --max-filesize 2097152 https://raw.githubusercontent.com/hyprwm/hyprlang/v0.6.8/tests/config/config.conf -o /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-26/fetch/SrcHyprlangTests-config.bin
mkdir -p /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-26/fetch && timeout 120 prlimit --as=4000000000 curl -fsSL --max-filesize 2097152 https://raw.githubusercontent.com/hyprwm/hyprlang/v0.6.8/tests/parse/main.cpp -o /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-26/fetch/SrcHyprlangTests-main.bin
```

Tag resolution command and observed output:

```text
timeout 30 prlimit --as=4000000000 git ls-remote https://github.com/hyprwm/hyprlang.git refs/tags/v0.6.8 'refs/tags/v0.6.8^{}'
3a1c1b25b059dae2c6bbc46991562ba1158d125c	refs/tags/v0.6.8
```

Digest and size command:

```text
timeout 20 prlimit --as=4000000000 sha256sum .ufo/waves/round-26/fetch/SrcHyprlangTests-config.bin .ufo/waves/round-26/fetch/SrcHyprlangTests-main.bin && timeout 20 prlimit --as=4000000000 wc -c -l .ufo/waves/round-26/fetch/SrcHyprlangTests-config.bin .ufo/waves/round-26/fetch/SrcHyprlangTests-main.bin
```

Observed output:

```text
96f3ad75dbbaa31c381f6f481dd1f7893b9402c15d8c5b62ddf6bfc0bd9fa7c2  .ufo/waves/round-26/fetch/SrcHyprlangTests-config.bin
ffedaa5e1f868084aca82017a9ad92afd8cdca9045cdd90b698ab3a85278f8ac  .ufo/waves/round-26/fetch/SrcHyprlangTests-main.bin
  191  3517 .ufo/waves/round-26/fetch/SrcHyprlangTests-config.bin
  452 26205 .ufo/waves/round-26/fetch/SrcHyprlangTests-main.bin
  643 29722 total
```

Quote-validation command and outcome (the first invocation used raw Python strings with escaped quotes and exited 1 with `AssertionError: SrcHyprlangTests-main.bin`; corrected quoting and the final four-quote check below both passed):

```text
timeout 30 prlimit --as=4000000000 python3 -I -c 'import pathlib,re; d=pathlib.Path(".ufo/waves/round-26/fetch"); qs=[("SrcHyprlangTests-config.bin", "$EXPR_VAR = {{MY_VAR + 2}}\ntestExpr = {{EXPR_VAR - 4}}"), ("SrcHyprlangTests-main.bin", "EXPECT(std::any_cast<int64_t>(config.getConfigValue(\"testExpr\")), 1335);"), ("SrcHyprlangTests-main.bin", "EXPECT(std::any_cast<float>(config.getConfigValue(\"testFloat\")), 123.456f);"), ("SrcHyprlangTests-main.bin", "EXPECT(std::any_cast<const char*>(config.getConfigValue(\"testEscapedExpr\")), std::string{\"{{testInt + 7}}\"});")]; norm=lambda s: re.sub(r"\s+", " ", s).strip(); [(None if norm(q) in norm((d/f).read_text()) else (_ for _ in ()).throw(AssertionError(f))) for f,q in qs]; print(f"PASS: {len(qs)} whitespace-collapsed source quotes are substrings")'
PASS: 4 whitespace-collapsed source quotes are substrings
```

The `SOURCES.md` header/row shape and latest registry rows through S172 were read. Searches for both source paths and for `hyprwm/hyprlang` in `corpus/SOURCES.md` returned no matches. No registry edit was made; this is a proposed row for the integrator:

```text
| S? | hyprlang v0.6.8 parser tests — https://raw.githubusercontent.com/hyprwm/hyprlang/v0.6.8/tests/config/config.conf; https://raw.githubusercontent.com/hyprwm/hyprlang/v0.6.8/tests/parse/main.cpp | code | A | `{{…}}` expression test inputs and typed values relevant to bind parsing | `tests/config/config.conf:13-24,30-32 @ 3a1c1b25b059dae2c6bbc46991562ba1158d125c, sha256:96f3ad75dbbaa31c381f6f481dd1f7893b9402c15d8c5b62ddf6bfc0bd9fa7c2, 3517 B; tests/parse/main.cpp:214-219,250-264,313-320 @ 3a1c1b25b059dae2c6bbc46991562ba1158d125c, sha256:ffedaa5e1f868084aca82017a9ad92afd8cdca9045cdd90b698ab3a85278f8ac, 26205 B` | Shows variable-driven integer arithmetic, dynamic expression parsing, and escaped-expression outputs; float coverage is a literal only, not a float expression | mined | 2026-10-23 | on-release | tools/mado-binds.py |
```

## Gates, touched surfaces, and limits

- No counter/control receipt exists for this source-opener item; no counter, oracle, Hyprland instance, upstream test executable, build, or test command was run.
- Touched only the item-owned report and two fetched source artifacts: `.ufo/waves/round-26/w1/reports/SrcHyprlangTests.md`, `.ufo/waves/round-26/fetch/SrcHyprlangTests-config.bin`, and `.ufo/waves/round-26/fetch/SrcHyprlangTests-main.bin`.
- No product code, counter/harness, or `corpus/SOURCES.md` file was edited; no tool was installed.
- The two requested raw file paths were probed/opened; this was not an exhaustive listing of the upstream `tests/` directory. Upstream test source is provenance for cases, not evidence that the cases passed in this run.
