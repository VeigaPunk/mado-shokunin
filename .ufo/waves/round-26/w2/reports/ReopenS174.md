# ReopenS174 — re-open draft row S174; check S158/S162 `used-by` extension quotes

Date: 2026-10-23. Item: ReopenS174 (wave w2, DATA + FALSIFY). Method per the re-open
contract: ordinary `curl -fsSL` re-fetch of the row URL to
`/fast/scratch/hyaku/mado-r26/reopen/`, sha256/byte-count comparison with the row,
and whitespace-collapsed-substring checks (≤25 words, cited line) for every quote
in the w1 report. For S158/S162 (existing rows whose `used-by` the draft extends)
the new quotes — the w1 "Located quotes" that justify the extension plus the new
literal claims the consuming note draft attributes to those rows — were checked
against the rows' pinned bytes.

## S174 — agree

Draft row (`.ufo/waves/round-26/drafts/sources-rows.md`, also committed at
`corpus/SOURCES.md:186`):

```text
| S174 | hyprlang v0.6.8 parser tests — https://raw.githubusercontent.com/hyprwm/hyprlang/v0.6.8/tests/parse/main.cpp | code | A | `{{…}}` expression test inputs and typed values relevant to bind parsing | `tests/parse/main.cpp:214-219,250-264,313-320 @ 3a1c1b25b059dae2c6bbc46991562ba1158d125c, sha256:ffedaa5e1f868084aca82017a9ad92afd8cdca9045cdd90b698ab3a85278f8ac, 26205 B` | Asserts variable-driven integer arithmetic, dynamic expression parsing, and escaped-expression outputs; float coverage is a literal only, not a float expression | mined | 2026-10-23 | on-release | tools/mado-binds.py |
```

Re-fetch receipt:

```text
$ mkdir -p /fast/scratch/hyaku/mado-r26/reopen && timeout 120 prlimit --as=4000000000 curl -fsSL --max-filesize 2097152 https://raw.githubusercontent.com/hyprwm/hyprlang/v0.6.8/tests/parse/main.cpp -o /fast/scratch/hyaku/mado-r26/reopen/ReopenS174.bin && timeout 120 prlimit --as=4000000000 curl -fsSL --max-filesize 2097152 https://raw.githubusercontent.com/hyprwm/hyprlang/v0.6.8/tests/config/config.conf -o /fast/scratch/hyaku/mado-r26/reopen/ReopenS174-config.bin && sha256sum ReopenS174.bin ReopenS174-config.bin && wc -c ReopenS174.bin ReopenS174-config.bin
ffedaa5e1f868084aca82017a9ad92afd8cdca9045cdd90b698ab3a85278f8ac  ReopenS174.bin
96f3ad75dbbaa31c381f6f481dd1f7893b9402c15d8c5b62ddf6bfc0bd9fa7c2  ReopenS174-config.bin
26205 ReopenS174.bin
 3517 ReopenS174-config.bin
```

sha256 `ffedaa5e…78f8ac` and 26205 B match the row exactly; the committed w1
artifact `fetch/SrcHyprlangTests-main.bin` re-hashes to the same digest.
`git ls-remote https://github.com/hyprwm/hyprlang.git refs/tags/v0.6.8` re-resolved
the tag to `3a1c1b25b059dae2c6bbc46991562ba1158d125c` — the pinned commit.

Quotes (w1 report `.ufo/waves/round-26/w1/reports/SrcHyprlangTests.md`; fresh
`python3 -I` check, `re.sub(r"\s+"," ",s).strip()` substring + cited line):

| quote | cited | substr | words | at line |
|---|---|---|---|---|
| `$EXPR_VAR = {{MY_VAR + 2}}` | config.conf:17 | yes | 5 | yes |
| `testExpr = {{EXPR_VAR - 4}}` | config.conf:18 | yes | 5 | yes |
| `EXPECT(std::any_cast<int64_t>(config.getConfigValue("testExpr")), 1335);` | main.cpp:252 | yes | 2 | yes |
| `EXPECT(std::any_cast<float>(config.getConfigValue("testFloat")), 123.456f);` | main.cpp:215 | yes | 2 | yes |
| `EXPECT(std::any_cast<const char*>(config.getConfigValue("testEscapedExpr")), std::string{"{{testInt + 7}}"});` | main.cpp:256 | yes | 5 | yes |

Prose claims independently spot-checked: `$MY_VAR = 1337` at config.conf:13;
`testEscapedExpr = \{{testInt + 7}}` at config.conf:20; dynamic input
`{{EXPR_VAR * 2}}` parsed at main.cpp:318 with `1339L * 2` expected at :319.
The float-limitation claim holds: no `{{…}}` expression producing a float exists
in either file (the only float is the literal `testFloat = 123.456`, conf:10 /
main:215).

Scope note for the integrator: the w1 report proposed a two-URL row
(`config.conf` + `main.cpp`); the draft keeps only `main.cpp`. All
config.conf quotes above still verify against a byte-identical re-fetch
(`96f3ad75…`, 3517 B), but that file is not pinned by the row, so the static
inputs behind the asserted values (e.g. 1335) are provenance the row no longer
carries. The retained `main.cpp` alone still supports "variable-driven integer
arithmetic" and "dynamic expression parsing" via the inline inputs at
:307/:318, so the row is self-consistent as written.

Verdict: `REOPEN S174 agree` (row and every w1 quote verify; dropped second
URL is the only narrowing, noted above).

## S158 — agree (`used-by` extension to `corpus/knowledge/animation-table-r26.md`)

Registry row `corpus/SOURCES.md:170` already carries the extension
(`used-by: corpus/knowledge/rule-attribution-r24.md, corpus/knowledge/animation-table-r26.md`),
matching the draft note. Pinned bytes: `src/debug/HyprCtl.cpp @
efb50993780079460b0cbed1363e2166a2de1d9f`, sha256 `798b7c6c…b91fa`, 97582 B.
Committed artifact `fetch/SrcHyprctlAnims.bin` re-hashes identically, and a fresh
re-fetch (`ReopenS158.bin`) is byte-identical to the row pin.

New quotes for the extension (w1 `SrcHyprctlAnims.md`), all verified against the
pinned bytes, whitespace-collapsed, cited line:

| quote | cited | substr | words | at line |
|---|---|---|---|---|
| `ret += "[[";` | :947 | yes | 3 | yes |
| `ret += ",\n[";` (literal `\n` two-char source text) | :964 | yes | 3 | yes |
| node field block (`"name"…"style"`) | :951–956 | yes | 12 | yes |
| bezier field block (`"name"…"Y1"`) | :970–974 | yes | 10 | yes |

Structural claims verified line-exact: `animationsRequest` defined at :927;
`registerCommand{…"animations"…}` at :2018 (inside the row's declared anchor
2003–2044); `]]` close at :981. The consuming note draft
(`drafts/animation-table-r26.md`) adds claims this seat re-verified against the
pinned bytes: node/bezier objects emitted as a two-element top-level array
(:947–981); `enabled`/`overridden` serialized as `"true"/"false"` strings from
`internalEnabled`/`overridden` (:957–958); `escapeJSONStrings` applied to node
bezier/style strings and bezier names (:957–958, :974); all coordinates and speed
formatted `{:.2f}`; bezier coords read `controlPoints[1]`/`[2]`; node array
iterates `Config::animationTree()->getAnimationConfig()`, bezier array iterates
`Animation::mgr()->getAllBeziers()` (:948, :965).

Residual: the function body :927–985 lies outside the row's declared anchor
ranges (`:346-484,613-630,647-723,1463-1645,2003-2044`); the registration at
:2018 is anchored. The SOURCES header allows `used-by` to change in place, so
this is informational, not a defect — readers following only the anchor will not
see the animation writer.

## S162 — agree (`used-by` extension to `corpus/knowledge/animation-table-r26.md`)

Registry row `corpus/SOURCES.md:174` already carries
`…, corpus/knowledge/rule-attribution-r24.md, corpus/knowledge/bind-table-r25.md, corpus/knowledge/animation-table-r26.md`,
matching the w1 proposal (`SrcAnimConfig.md` §SOURCES ledger gate). Pinned bytes:
`src/config/legacy/ConfigManager.cpp @ efb50993780079460b0cbed1363e2166a2de1d9f`,
sha256 `9db68cf4…be62b`, 90963 B. `fetch/SrcAnimConfig.bin` and the exploratory
duplicate `SrcAnimConfig-legacy-impl.bin` re-hash identically; fresh re-fetch
(`ReopenS162.bin`) is byte-identical to the row pin.

New quotes for the extension (w1 `SrcAnimConfig.md`), verified:

| quote | cited | against | substr | words | at line |
|---|---|---|---|---|---|
| `CVarList(const std::string& in, const size_t lastArgNo = 0, const char delim = ',', const bool removeEmpty = false);` | hyprutils VarList.hpp:14 | `SrcAnimConfig-hyprutils-varlist.bin` (`9ad2fcbd…fc43`, 1883 B — supplemental artifact, correctly attributed as not part of the S162 pin) | yes | 18 | yes |
| `nodeExists(ANIMNAME)` / `"no such animation"` / `enabledInt = … == 1` block | :1434–1438 | pinned file | yes | 24 | yes |
| `"invalid speed"` / `speed = 10.f` / `bezierName` / `"no such bezier"` block | :1457–1467 | pinned file | yes | 24 | yes |
| `setConfigForNode(…)` + style-validation + `return {}` block | :1469–1478 | pinned file | yes | 20 | yes |

Structural claims verified line-exact: `handleBezier` at :1389 (checked args
1–4, `too few arguments`/`invalid point`, `std::stof`, `ARGS[5]` →
`too many arguments`, `addBezierWithName(bezierName, Vector2D(p1x,p1y), Vector2D(p2x,p2y))`);
`handleAnimation` at :1426 (`nodeExists` at :1434, the post-boolean range check
at :1440–1441, disabled branch `setConfigForNode(ANIMNAME, enabledInt, 1,
"default")` at :1443–1446, speed/bezier/style sequence :1449–1478);
registrations `bezier`/`animation` at :612–613 (inside the row anchor 590–623);
callback optional-error → `CParseResult::setError` at :287–309.

Residual: handler bodies :1389–1479 and the callback wrappers :287–309 lie
outside the row's declared anchor ranges (`:419-451,590-623,893-968,2016-2093`);
only the registrations are anchored. Same informational caveat as S158.

## Gate notes

- Reads: draft rows file, w1 reports, registry, committed fetch artifacts, the
  scribe's note draft. Writes: this report plus three fetch artifacts under
  `/fast/scratch/hyaku/mado-r26/reopen/` (`ReopenS174.bin`,
  `ReopenS174-config.bin`, `ReopenS158.bin`, `ReopenS162.bin`). No lane file
  other than this report was touched; no counter, control, oracle, Hyprland
  instance, or host compositor command was run.
- Network use was ordinary `curl -fsSL` to raw.githubusercontent.com and one
  `git ls-remote`; no challenge or access control was bypassed.
- No tools installed or upgraded (curl/python3/git already present).

Report: .ufo/waves/round-26/w2/reports/ReopenS174.md
