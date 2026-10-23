# ReopenS176 — w2 re-open findings

Re-open contract executed for draft row S176 (w1 report `SrcAnimTree.md`) plus the
`used-by` extension checks for existing rows S158 (`SrcHyprctlAnims.md`) and S162
(`SrcAnimConfig.md`). All fetches were ordinary `curl -fsSL` to the pinned raw URLs;
no bot challenge or access control was touched.

## Commands and byte/digest receipts

```sh
mkdir -p /fast/scratch/hyaku/mado-r26/reopen
timeout 120 prlimit --as=4000000000 curl -fsSL 'https://raw.githubusercontent.com/hyprwm/Hyprland/efb50993780079460b0cbed1363e2166a2de1d9f/src/config/shared/animation/AnimationTree.cpp' -o /fast/scratch/hyaku/mado-r26/reopen/ReopenS176.bin
timeout 120 prlimit --as=4000000000 curl -fsSL 'https://raw.githubusercontent.com/hyprwm/hyprutils/v0.14.2/src/animation/AnimationConfig.cpp' -o /fast/scratch/hyaku/mado-r26/reopen/ReopenS176-hyprutils.bin
timeout 120 prlimit --as=4000000000 curl -fsSL 'https://raw.githubusercontent.com/hyprwm/Hyprland/efb50993780079460b0cbed1363e2166a2de1d9f/src/debug/HyprCtl.cpp' -o /fast/scratch/hyaku/mado-r26/reopen/ReopenS176-S158.bin
timeout 180 prlimit --as=4000000000 curl -fsSL 'https://raw.githubusercontent.com/hyprwm/Hyprland/efb50993780079460b0cbed1363e2166a2de1d9f/src/config/legacy/ConfigManager.cpp' -o /fast/scratch/hyaku/mado-r26/reopen/ReopenS176-S162.bin
timeout 120 prlimit --as=4000000000 curl -fsSL 'https://raw.githubusercontent.com/hyprwm/hyprutils/v0.14.2/include/hyprutils/string/VarList.hpp' -o /fast/scratch/hyaku/mado-r26/reopen/ReopenS176-varlist.bin
sha256sum /fast/scratch/hyaku/mado-r26/reopen/ReopenS176*.bin
wc -lc /fast/scratch/hyaku/mado-r26/reopen/ReopenS176*.bin
```

Results (every digest compared against the row's or report's pinned value):

| Scratch file | SHA-256 | Lines/Bytes | Pinned expectation | Match |
|---|---|---|---|---|
| `ReopenS176.bin` | `313ed20167618dfe163fceee8753e9a49d8ef356bc3f580963e07039839e7bae` | 83 / 3483 B | row S176: `313ed201…7bae`, 3483 B | yes |
| `ReopenS176-hyprutils.bin` | `dbb5d50a27f80ea947db92050af40ee87e0e9e0718add0520cbc96e32abe268e` | 70 / 2354 B | w1 provenance `dbb5d50a…268e`, 2354 B | yes |
| `ReopenS176-S158.bin` | `798b7c6c4c1684557842463d46ac99c96629be4179e0e461dca77670247b91fa` | 2346 / 97582 B | row S158: `798b7c6c…91fa`, 97582 B | yes |
| `ReopenS176-S162.bin` | `9db68cf44048d86557d8a53068dcc40b9bd7347c7d95f38edc501565f65be62b` | 2184 / 90963 B | row S162: `9db68cf4…e62b`, 90963 B | yes |
| `ReopenS176-varlist.bin` | `9ad2fcbd5de691166b7db95de09b6bd054c9b4313deb3187e84c914dab74fc43` | 65 / 1883 B | w1 provenance `9ad2fcbd…fc43`, 1883 B | yes |

## Quote verification

Method: each quote was whitespace-collapsed (`re.sub(r'\s+', ' ', …).strip()`) and
tested as a substring of the whitespace-collapsed decoded UTF-8 bytes; the
whitespace-separated word count was required to be ≤ 25; and each quoted line was
checked verbatim (after trim) against the cited line(s) of the decoded file.
Blank lines inside a quote had to land on blank file lines inside the cited span.

| ID | Quote (collapsed) | Cited at | Words | Substring | Cited lines | Result |
|---|---|---|---|---|---|---|
| AT-q1 | `m_animationTree.createNode("__internal_fadeCTM"); m_animationTree.createNode("global");` | AnimationTree.cpp:15-16 | 2 | yes | exact | PASS |
| AT-q2 | `m_animationTree.createNode("windowsIn", "windows");` | AnimationTree.cpp:35 | 2 | yes | exact | PASS |
| AT-q3 | `.pValues = (parentRef) ? parentRef->pValues : pConfig, .pParentAnimation = (parentRef) ? parentRef : pConfig,` | hyprutils AnimationConfig.cpp:24-25 | 14 | yes | exact | PASS |
| AT-q4 | `if (anim->pParentAnimation == PANIM && !anim->overridden) { // if a child isnt overridden, set the values of the parent` | hyprutils AnimationConfig.cpp:63-64 | 19 | yes | exact | PASS |
| HC-q1 | `ret += "[[";` | HyprCtl.cpp:947 | 3 | yes | exact | PASS |
| HC-q2 | `ret += ",\n[";` (literal backslash-n in the C++ source) | HyprCtl.cpp:964 | 3 | yes | exact | PASS |
| HC-q3 | `"name": "{}", "overridden": {}, "bezier": "{}", "enabled": {}, "speed": {:.2f}, "style": "{}"` | HyprCtl.cpp:951-956 | 12 | yes | exact | PASS |
| HC-q4 | `"name": "{}", "X0": {:.2f}, "Y0": {:.2f}, "X1": {:.2f}, "Y1": {:.2f}` | HyprCtl.cpp:970-974 | 10 | yes | exact | PASS |
| AC-q1 | `CVarList(const std::string& in, const size_t lastArgNo = 0, const char delim = ',', const bool removeEmpty = false);` | hyprutils VarList.hpp:14 | 18 | yes | exact | PASS |
| AC-q2 | `if (!Config::animationTree()->nodeExists(ANIMNAME)) return "no such animation"; // This helper casts strings like "1", "true", "off", "yes"... to int. int64_t enabledInt = ParserUtils::parseInt(ARGS[1]).value_or(0) == 1;` | ConfigManager.cpp:1434-1438 | 24 | yes | exact | PASS |
| AC-q3 | `return "invalid speed"; } } else { speed = 10.f; return "invalid speed"; } std::string bezierName = ARGS[3]; if (!Animation::mgr()->bezierExists(bezierName)) return "no such bezier";` | ConfigManager.cpp:1457-1467 | 24 | yes | exact | PASS |
| AC-q4 | `Config::animationTree()->setConfigForNode(ANIMNAME, enabledInt, speed, ARGS[3], ARGS[4]); if (!ARGS[4].empty()) { auto ERR = Animation::mgr()->styleValidInConfigVar(ANIMNAME, ARGS[4]); if (!ERR.empty()) return ERR; } return {};` | ConfigManager.cpp:1469-1478 | 20 | yes | exact | PASS |

Attribution note: SrcAnimTree's quotes 3-4 and SrcAnimConfig's quote 1 are attributed
by the w1 reports themselves to the hyprutils v0.14.2 files, not to the S176/S162 row
files; each was checked against its own pinned bytes. SrcAnimConfig quotes 2-4 are
the S162-pinned-byte quotes that justify the `used-by` extension; all pass.

## Additional falsification checks on the S176 bytes

- 35 `createNode(...)` calls found; the two unparented roots are `__internal_fadeCTM`
  and `global`, matching the report's "34 named nodes plus `__internal_fadeCTM`".
- Line 14 is `void CAnimationTreeController::reset() {` and line 66 is
  `m_animationTree.setConfigForNode("glowangle", 0, 1, "default");`, consistent with
  the cited anchor span `:14-66`.
- The literal `addAnimationConfig` does not appear anywhere in the 3483 bytes,
  confirming the report's negative finding.

## Registry state observed

`corpus/SOURCES.md` already contains S175-S177 as appended rows (S176 at line 188
with the identical digest/bytes/anchors checked here) and S158/S162 already carry the
extended `used-by` including `corpus/knowledge/animation-table-r26.md`. The draft in
`sources-rows.md` matches what landed; no drift detected.

## Limits and notes

- SrcHyprctlAnims quote 2 is shown in the report as `ret += ",\n[";`; the pinned
  bytes contain the two-character sequence backslash-n (a C++ escape), which is what
  was verified. Read literally as C++ source the quote is exact.
- Residual risk: line-3 of the S176 row's "strengths" column is prose, not bytes;
  it was sanity-checked against the node inventory (counts and roots) rather than a
  substring test.
- No counter, control, Hyprland instance, or compositor command was run. Scratch
  artifacts left at `/fast/scratch/hyaku/mado-r26/reopen/`; no lane file other than
  this report was written; no tool installed; no process left running.

Verdict: `REOPEN S176 agree` — digest, byte count, anchors, and every located quote
verify against freshly fetched pinned bytes; the S158/S162 `used-by` extensions rest
on quotes that likewise verify against their rows' pinned bytes.

Report: `.ufo/waves/round-26/w2/reports/ReopenS176.md`
