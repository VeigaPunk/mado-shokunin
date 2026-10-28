# R55W2RevToolSource — report (wave w2, round 55, falsify)

Scope: check the C2 tool's model (tools/mado-kbdopts.py, docstring l.1-70 and the code) against SOURCE, not against the
registration. Full verdicts, the statement-by-statement table and the case matrix are in
`w2/R55W2RevToolSource/source-check.md`. Receipts are in `w2/R55W2RevToolSource/`.

## What ran

- Read the tool at the scored revision 57584ed6…: `git show 57584ed…:tools/mado-kbdopts.py` is byte-identical to the working tree (sha256 9c69dd62…). Read-only git only.
- Pins checked byte-for-byte against upstream at the stated tags (`upstream-sha.txt`): InputManager.cpp, legacy ConfigManager.cpp, ConfigValues.cpp, IKeyboard.cpp (Hyprland v0.56.2, commit efb50993 per GitHub API ref and `hyprctl version`), and hyprlang-config.cpp (= hyprlang v0.6.8 src/config.cpp). All IDENTICAL.
- isNumber from hyprutils v0.14.0 (Hyprland 0.56.2 CMake minimum; host has 0.14.2-1).
- Built an unmodified-source harness: hyprlang v0.6.8 + hyprutils v0.14.0 compiled with g++ 16.2.1 (pre-installed, not installed by me), registered as Hyprland 0.56.2's legacy ConfigManager does, plus a re-implementation of getDeviceInt / applyConfigToKeyboard / IKeyboard's `== 1` numlock rule. One build-only macro line added to the scratch copy (see harness/BUILD.txt).
- Ran 26 config cases (c01-c26, c14 run separately as a main file that sources a sub file) through both the harness and the tool (`w2/R55W2RevToolSource/harness/run14.txt`, `cases/`).
- Ran `python3 -I tools/mado-kbdopts.py --selftest` (result 83/83 passed).
- Host, read-only: `hyprctl version`, `hyprctl getoption input:repeat_rate|input:repeat_delay|input:numlock_by_default -j`, `hyprctl devices -j` (names only), `cat ~/.config/hypr/input.conf` (sha 3769c92a…, same as round-55 fixture), `pacman -Q hyprlang hyprutils hyprland`, `pkg-config --modversion`. No keyword/dispatch/reload; no config writes.
- Network: raw.githubusercontent.com for source files; api.github.com for tag trees and ref commit (disclosed: API, not raw).
- Tools: none installed or upgraded. No pacman transaction.
- Scratch `/fast/scratch/hyaku/mado-r55/R55W2RevToolSource/` is removed before yield. Nothing written inside the lane except `w2/R55W2RevToolSource/` and this report. No commit, no tracked-file edit.

## Decisive output (excerpts; full in run14.txt)

    c01 `input { # c` / repeat_rate = 30 :  source rate=30   | tool rate=25 unsupported=0          (SILENT)
    c02 `} # end` then input:repeat_delay=100 : source delay=100 | tool delay=600 unsupported=0   (SILENT)
    c11 `$dev = mykbd` / device{ name = $dev / repeat_rate=50 : source mykbd rate=50 | tool mykbd 25 unsupported=0 (SILENT)
    c12 `#hyprlang if NOPE` block : source 25 | tool 30 unsupported=0                              (SILENT)
    c13 `# disabled \` + `input:repeat_rate = 30` : source 25 | tool 30 unsupported=0              (SILENT)
    c14 `source = sub.conf` (sub: rate 30) : source 30 | tool 25 unsupported=0 (main file only)    (SILENT)
    c04 rate 30 then `-0` : source 0 | tool 30 unsupported=1                                       (flagged, wrong value)
    c08 `0x10` : source 16 | tool 25 unsupported=1                                                  (flagged, wrong value)
    c09 numlock 1 then 2 : source numlock=2, no lock (IKeyboard.cpp:122) | tool numlock=1 unsupported=1 (flagged, wrong value)
    c10 rate 300 : source 300 | tool 25 unsupported=1                                               (flagged, wrong value)
    c24 unclosed device in file A, `device{repeat_rate=50}` in B : source a=50 | tool a=25 unsupported=1 (flagged, wrong value)
    c26 rate 4294967316 : source 20 (getDeviceInt int cast) | tool 25 unsupported=1                 (flagged, wrong value)
    c05 `+5`, c07 `3.5`, c20 empty, c21 `30abc`, c15 device key before name : source = error, value kept | tool = unsupported, value kept   (consistent)
    c06 `007`: 7 / 7 ; c16, c17, c18, c22, c25 : consistent
    selftest: MADO_KBDOPT_SELFTEST: 83/83 assertions passed (its "`{` with trailing comment not a push" test asserts the c01 divergence)
    live host: option=input:repeat_rate config=40 live=40 AGREE ; repeat_delay 250/250 AGREE ; numlock 1/1 AGREE ; DONE live=AGREE

## Verdict per target

1. Cited file:line in the docstring (InputManager.cpp:1282-1283; legacy ConfigManager.cpp:1115-1123; ConfigValues.cpp:277-280; hyprlang-config.cpp:259-262) — **SURVIVES**. Paths exist at tag v0.56.2; lines match the identical files. getDeviceInt lines 1131-1137 verified (the docstring does not cite them).
2. getDeviceInt :1131-1137 semantics — **SURVIVES** for the lookup; **BROKEN** for the value range: it returns `int`, so a 64-bit INT is truncated (c26 → 20).
3. Value-prefix rules (true/on/yes, false/off/no) — **SURVIVES** for the bool prefixes. **BROKEN** as a description of configStringToInt: the 0x and rgb()/rgba() branches run first (config.cpp:195-258), and "else decimal digits" omits the leading `-` the source accepts (isNumber2 59-62).
4. `-0` — **BROKEN** (source accepts → 0; tool says unsupported and prints the prior value; c04).
5. `+5` — **SURVIVES** (source rejects, value kept; tool unsupported, value kept; c05).
6. `007` — **SURVIVES** (7; c06).
7. `3.5` — **SURVIVES** (source rejects; c07).
8. Out-of-range INT — **BROKEN**. Pins: the legacy (.conf) path registers every value with no range (legacy 488-514) and applyConfigToKeyboard clamps only below 0 (InputManager 1282-1283). Upstream min/max is enforced ONLY in the Lua path (src/config/lua/types/LuaConfigInt.cpp:15-21, 52-60), used only for `.lua` (src/config/ConfigManager.cpp:33-45). The docstring's "not shown by the pins" is therefore misleading, and its "line ignored / never guessed" policy disagrees with what hyprland.conf does (c10: 300 applied).
9. numlock 0..1 note — **SURVIVES** as a disclosure (no source range; Bool, no min/max). **BROKEN** in effect: source stores 2 and does not lock (IKeyboard.cpp:122 `== 1`), the tool prints 1 (c09).
10. Comment handling of `{`/`}` (docstring l.29-30) — **BROKEN** (c01, c02). Source strips the comment before the brace test (config.cpp:672-706, 713-716, 881-909).
11. Backslash continuation / "split on \n" (l.27-28) — **BROKEN** (c13; config.cpp:44-65, 1016-1030).
12. "current device reset at each file's start" (l.27-28) — **BROKEN** (c24; config.cpp:1044-1052 clears the stack but not currentSpecialCategory; 348-353).
13. `source` "ignored" (l.33-34) — **BROKEN** (c14). Hyprland registers a handler (legacy 614, handleSource 1802-1850) that parses the sourced files.
14. `$` in a `name =` line (not flagged) — **BROKEN** (c11; config.cpp:737-745 expands RHS, and the tool checks `$` only on relevant lines, l.173-176 vs 185).
15. `#hyprlang if/endif/noerror` — **BROKEN** by omission (c12; config.cpp:567-617, 683-684). The docstring treats `#`-first lines as skipped.
16. Device key before `name` → unsupported, ignored (l.43) — **SURVIVES** (c15).
17. Device merge, comment-cut device name (l.38-41) — **SURVIVES** (c22, c25).
18. Bracket forms `device[...]` flagged (l.37-38) — **SURVIVES** (honest unsupported; hyprlang supports them).
19. `$`/`{{`/`\`/`##` flagged as unsupported (l.38-40) — **SURVIVES** as flags. `##` is a source error (c03), `$` in a trailing comment is flagged conservatively (c19), both honest.
20. Getoption JSON format (l.16-17, l.50-53) — **SURVIVES** (HyprCtl.cpp:1702 `{"option","int","set"}`; live AGREE).
21. "models source-level semantics" (l.60-61) and "models that" (l.15-16) — **BROKEN** (overclaim; items 10-15).
22. Read-only claim (l.18-19) — **SURVIVES** by code reading.
23. Tool self-test as an oracle — **BROKEN**: 83/83 passes while asserting the c01 divergence.

## Residual risk / could not verify

- Only the installed hyprlang 0.6.8-5 pair was tested; Hyprland 0.56.2's declared minimum is hyprlang 0.6.7. Other versions UNVERIFIED.
- The harness re-implements Hyprland's getDeviceInt, applyConfigToKeyboard and the numlock rule (the code is pinned and cited, but the harness is not the Hyprland binary). The config parser itself is the unmodified hyprlang v0.6.8 source.
- The harness's `source` is the registered handler calling parseFile on a literal path; Hyprland's glob/absolutePath handling is not reproduced (irrelevant to the findings).
- Live host config cross-check covers only the host's three values (all AGREE); it does not exercise any divergent construct.
- Keyboard-name mapping: `hyprctl devices -j` keyboard `name` is m_hlName (HyprCtl.cpp:799), but the docstring never says so (unsourced omission).
- No keypress/compositor observation (declared out of scope by the tool).

No finding here required a mutation of any lane file. No mutation test was run. All harness work is in scratch and is removed before yield.
