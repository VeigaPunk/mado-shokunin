# R55W2RevToolSource — source check of tools/mado-kbdopts.py (C2)

Seat: R55W2RevToolSource (falsify wave w2, round 55). Scored tool revision: lane 57584ed6…; the tool at that
revision is byte-identical to the working tree (sha256 9c69dd62…, `git show 57584ed…:tools/mado-kbdopts.py` vs file).
Tool self-test at that revision: `MADO_KBDOPT_SELFTEST: 83/83 assertions passed` (rc 0) — the self-test passes
on the wrong behaviour listed under D14 (see T-B1).

## 1. Pins vs upstream (what "source" means here)

Every cited pin is byte-identical to the upstream file at the stated tag (receipt `upstream-sha.txt`):

| pin (round-55/round-46 fetch) | upstream file | result |
|---|---|---|
| Hyprland-InputManager.cpp | Hyprland v0.56.2 `src/managers/input/InputManager.cpp` | IDENTICAL |
| Hyprland-legacy-ConfigManager.cpp | Hyprland v0.56.2 `src/config/legacy/ConfigManager.cpp` | IDENTICAL |
| Hyprland-ConfigValues.cpp | Hyprland v0.56.2 `src/config/values/ConfigValues.cpp` | IDENTICAL |
| Hyprland-IKeyboard.cpp | Hyprland v0.56.2 `src/devices/IKeyboard.cpp` | IDENTICAL |
| hyprlang-config.cpp (round-46) | hyprlang v0.6.8 `src/config.cpp` | IDENTICAL |

Tag v0.56.2 = commit efb50993780079460b0cbed1363e2166a2de1d9f (GitHub API ref), = `hyprctl version` on the host.
Host packages (query only, `pacman -Q`): hyprlang 0.6.8-5, hyprutils 0.14.2-1, hyprland 0.56.2-4.
Hyprland 0.56.2's CMake *requires* hyprlang>=0.6.7 and hyprutils>=0.14.0 (CMakeLists.txt); isNumber was taken from
hyprutils v0.14.0 `src/string/String.cpp:46-84` (the 0.7.1 copy has the same logic; both give identical harness output).

## 2. Cited line numbers (all verified against the identical pins/upstream)

- `InputManager.cpp:1282-1283` = `m_repeatRate = std::max(0, REPEATRATE)` / `m_repeatDelay = std::max(0, REPEATDELAY)`. SURVIVES.
- `legacy/ConfigManager.cpp:1115-1123` = getConfigValueSafeDevice (fallback used when the device value is absent OR not
  `m_bSetByUser`, and only when fallback non-empty). SURVIVES (the docstring's one-line paraphrase is accurate).
- `getDeviceInt` `:1131-1137` (the tool does not cite these; checked anyway): returns `int`, casts the hyprlang INT.
  SURVIVES, with the side-finding in D10 (int truncation).
- `ConfigValues.cpp:277-280`: 277 `MS<Bool>` numlock default false, no min/max; 279 repeat_rate 25, min 0 max 200;
  280 repeat_delay 600, min 0 max 2000. SURVIVES.
- `hyprlang-config.cpp:259-262`: true/on/yes -> 1 (259-260), false/off/no -> 0 (261-262). SURVIVES (lines), see D8 for
  what the paragraph omits.

## 3. Docstring statements — verdicts

Verdict key: SURVIVES = source agrees; BROKEN = source disagrees, or the tool's printed output contradicts source with
the docstring's own "unsupported, never guessed" rule; UNSOURCED = not backed by a pin/upstream cite;
OVERCLAIM = stated more strongly than the evidence.

- D1 (l.4-6) applyConfigToKeyboard stores max(0,rate), max(0,delay) at :1282-1283 — SURVIVES.
- D2 (l.5-7) per option, device block value when that block sets the key, else global; "keyboard's name" —
  rate/delay SURVIVE (InputManager.cpp:1220-1221). Numlock is also read at IKeyboard.cpp:120 (uncited, and the lock is
  at IKeyboard.cpp:122). The "keyboard's name" is `m_hlName` (InputManager.cpp:1214; HyprCtl.cpp:799 emits it as the
  keyboard `name` in `hyprctl devices`). The docstring never says which name to pass — UNSOURCED (omission).
- D3 (l.7-8) getConfigValueSafeDevice :1115-1123 "device value used when m_bSetByUser, else fallback" — SURVIVES.
- D4 (l.8-9) defaults 25, 600, false at ConfigValues.cpp:277-280 — SURVIVES (false is stored as INT 0, legacy:495-496).
- D5 (l.9-10) declared ranges 0..200 / 0..2000 are the table's `.min/.max` at :279-280 — SURVIVES as declarations.
- D6 (l.10-11) numlock 0..1 is "the lane's modelling rule, not a source range" (Bool, no min/max at :277) — SURVIVES
  as a disclosure. Its consequence is BROKEN: see D12/T-B3 (source keeps numlock=2 and does not lock; tool prints 1).
- D7 (l.11-12) "Which pinned Hyprland site enforces a range is not shown by the pins this round, so an out-of-range
  value is `unsupported` here, never guessed." — BROKEN in two clauses:
  (a) The pins DO show the answer for the path the tool models (`hyprland.conf` -> legacy): legacy/ConfigManager.cpp
      :488-514 registers every value with no range; InputManager.cpp:1282-1283 clamps only below 0; nothing validates
      input:repeat_rate. Upstream, min/max is enforced ONLY in the Lua path (src/config/lua/types/LuaConfigInt.cpp:15-21,
      52-60, PARSE_ERROR_OUT_OF_RANGE), reachable only for `.lua` configs (src/config/ConfigManager.cpp:33-45).
  (b) "never guessed": the tool's printed value for an out-of-range line is the pre-line value (25/600/0 or earlier
      line), which the source does not produce — harness: `input:repeat_rate = 300` -> source applies 300 (T-B5).
- D8 (l.12-14) configStringToInt "(hyprlang-config.cpp:259-262): true/on/yes -> 1 (checked first); false/off/no -> 0;
  else decimal digits" — PARTLY BROKEN: (a) lines 259-262 are correct for the bool prefixes but are NOT checked first:
  the `0x` branch (195-197) and `rgb(`/`rgba(` branches (198-258) come before them; (b) "else decimal digits" is wrong:
  the tail is `isNumber(VALUE,false)` then `stoll` (265-271), which accepts a leading `-` (isNumber2 59-62; "-0" -> 0);
  (c) the file name is the pin name — upstream path is src/config.cpp (v0.6.8). Source-positive examples: -0 -> 0 (T-B2),
  0x10 -> 16 (T-B4), 4294967316 -> stored as INT, cast to 20 by getDeviceInt (T-B6).
- D9 (l.15-16) "This tool models that for config text ... and joins ..." — OVERCLAIM: the model is a subset with
  silent divergences (D11-D14). The subset statement itself (l.26) is honest; "models that" is not.
- D10 (l.16-17) getoption line format `{"option", "int", "set"}` — SURVIVES: HyprCtl.cpp:1702 emits exactly
  `{"option": "...", "int": N, "set": B }`. Host cross-check: `hyprctl getoption` x3 -> tool `live=AGREE` on all 3
  (T-H1). Not stated in the docstring: getDeviceInt's int cast (T-B6).
- D11 (l.18-19) read-only; no process/socket/write — SURVIVES by code reading (os.open O_RDONLY|O_NONBLOCK, no writes).
- D12 (l.27-28) "decoded as UTF-8 ... split on \n; the category stack and the current device reset at each file's start"
  — BROKEN, two ways:
  (a) hyprlang joins backslash-continued lines before parsing (config.cpp:44-65, used by parseFile :1016-1030). A
      comment line ending in `\` swallows the next line: T-B7 (source 25; tool 30, unsupported=0; silent).
  (b) "current device reset at each file's start": parseFile clears only the category stack at EOF (:1044-1052);
      currentSpecialCategory survives, so a following file's `device {` with a key before `name` writes to the previous
      file's unclosed device: T-B8 (source a=50; tool a=25 flagged unsupported=1).
- D13 (l.28-29) trimmed chars; empty or `#`-first lines skipped — SURVIVES for values; omits that a `#` first line is
  parsed for `#hyprlang` directives (config.cpp:674-681, 567-617) — T-B9 (unmodelled conditional, silent).
- D14 (l.29-30) "exactly `}` pops; a line ending in `{` pushes its text before the `{`; anything else ignored" —
  BROKEN. hyprlang strips the trailing comment BEFORE these tests (config.cpp:672-706, then 713-716 and 881-909).
  `input { # c` opens the block (T-B1: source 30, tool 25, unsupported=0); `} # end` closes it (T-B1b: source
  repeat_delay=100, tool 600, unsupported=0). The tool's own self-test asserts the wrong result for `input { # c`
  (mado-kbdopts.py selftest "`{` with trailing comment not a push") and passes.
- D15 (l.31-33) LHS/RHS split on FIRST `=` — SURVIVES for values (config.cpp:711-723 same rule on the stripped line).
- D16 (l.33-34) "an LHS starting with $ and an LHS equal to source are ignored" — BROKEN for `source`: Hyprland registers
  a `source` handler (legacy/ConfigManager.cpp:614, 359-369, handleSource 1802-1850 = glob + parseFile of each match).
  The tool ignores it silently (T-B10: sourced `input:repeat_rate = 30` -> source 30, tool 25, unsupported=0).
  `$`-LHS variable definitions being ignored is correct as definitions, but see D17.
- D17 (l.38-40) relevant-line checks flag `$`, `{{`, backslash, `##` — SURVIVES as flags (conservative), with one hole:
  the `name = ...` line is handled BEFORE the relevance/`$` check (tool l.173-176), and hyprlang expands `$var` in RHS
  (config.cpp:737-745). T-B11: `$dev = mykbd` / `name = $dev` -> source keyboard mykbd repeat_rate=50; tool device
  `$dev`, mykbd=25, unsupported=0 (silent).
- D18 (l.37-38) bracket forms not modelled, flagged — SURVIVES (honestly unsupported; hyprlang supports them, config.cpp:291-333).
- D19 (l.38-41) device `name` cut at `#`; the device block merges — SURVIVES (T-C22, T-C25).
- D20 (l.41) RHS cut at first `#`, then parse — SURVIVES for values; the `$` in trailing comment flagged (T-C19) is a
  conservative choice that the docstring states — honest flagged over-approximation, not silent.
- D21 (l.41-42) classes: true/on/yes, false/off/no, all `[0-9]+`, else (hex, sign, float, empty, words) unsupported —
  effective values SURVIVE for +5, 3.5, 30abc, empty (all source errors -> line not applied; flagged) and for 007 (7).
  BROKEN for -0 (source 0; tool keeps prior value, flagged) and for 0x10 (source 16; tool keeps prior, flagged): the
  label `unsupported` is honest, but the printed effective value is a guess that source contradicts (see D7).
- D22 (l.42-43) ranges: "outside -> unsupported +1, line ignored" — BROKEN vs source: the legacy path applies 300 (T-B5),
  and 1 then 2 for numlock leaves numlock=2 (T-B3). The tool's ignore is a policy, not the source behaviour.
- D23 (l.43) device key with no current device -> unsupported, ignored — SURVIVES (T-C15: source error, value not set).
- D24 (l.43-45) "effective: device if set for NAME, else global, else default" — SURVIVES for the simple cases
  (T-C16, T-C22, T-C25); not for D11/D12(b)/D17 cases above.
- D25 (l.46-58) output and setup-failure formats — SURVIVE (code paths read; selftest covers them).
- D26 (l.60-61) "models source-level semantics" — OVERCLAIM (see D9, D11-D17).
- D27 (l.4) "Hyprland 0.56.2 (efb50993) ... hyprlang 0.6.8 as Hyprland 0.56.2 reads it" — SURVIVES for the installed
  pair (host hyprlang 0.6.8-5). UNVERIFIED for other hyprlang versions: 0.56.2's CMake minimum is hyprlang 0.6.7.
- D28 (l.21-22) control-byte NAME rejected "the contract is silent, this is an extension" — honest (code comment).

## 4. Targeted checks requested

- `-0`: source ACCEPTS (isNumber allows one leading '-', isNumber2 59-62; stoll("-0")=0) -> 0. Tool: "sign unsupported",
  line ignored, prints the prior value. Honest label, wrong printed value (T-B2). BROKEN as a printed result.
- `+5`: source REJECTS (isNumber rejects '+', line 64-66 path) -> parse error, value unchanged. Tool: unsupported, ignored.
  Effective result identical. SURVIVES (T-C05 / T-B-plus).
- `007`: source 7 (isNumber ok, stoll base 10). Tool 7. SURVIVES (T-C06).
- `3.5`: source REJECTS (isNumber(...,false) false) -> parse error, value unchanged. Tool unsupported, ignored. SURVIVES (T-C07).
- Out-of-range INT (rate 300, delay 2001, numlock 2): see D7/D22. On the path a `.conf` uses (legacy), the value is
  stored and applied: rate 300 -> applied 300 (std::max(0,...) does not cap the top). Enforcement exists only in Lua.
  The tool's "line ignored" is not the source behaviour. BROKEN.
- numlock 0..1 note: honest as a disclosure (no source range). Source behaviour: IKeyboard.cpp:122 locks only on `== 1`,
  so 2 stores 2 and does NOT lock (T-B3, T-C23). Tool prints numlock=1 when `1` then `2` (T-B3): wrong printed value. BROKEN.

## 5. Mechanical evidence (harness = unmodified hyprlang v0.6.8 + hyprutils v0.14.0 built from upstream)

Harness: scratch build of upstream hyprlang v0.6.8 `src/config.cpp`, `src/common.cpp` and hyprutils v0.14.0 string
sources, with the registration of Hyprland 0.56.2 legacy ConfigManager (addConfigValue/addSpecialCategory/
addSpecialConfigValue/registerHandler("source")/throwAllErrors), plus a re-implementation of getDeviceInt/applyConfigToKeyboard/
IKeyboard's `== 1` rule. Build-only change: one `#define HYPRLANG_END_MAGIC 0x1337BEEF` added to the scratch copy of
config.cpp, because hyprlang.hpp #undefs that macro before config.cpp uses it (no logic changed). Code: receipts/harness/driver.cpp.
Full side-by-side output: `harness/run14.txt` (run with hyprutils 0.14.0 build; the 0.7.1 build agreed on all rows).

| case (receipt cases/) | source (harness) | tool (C2 at 57584ed) | class |
|---|---|---|---|
| c01 `input { # c` / repeat_rate=30 | rate 30 | rate 25, unsupported=0 | SILENT WRONG (D14) |
| c02 `} # end` then `input:repeat_delay = 100` | delay 100 | delay 600, unsupported=0 | SILENT WRONG (D14) |
| c03 `4##0` | error, 25 | 25, unsupported=1 | consistent (flagged) |
| c04 `30` then `-0` | 0 | 30, unsupported=1 | WRONG VALUE (flagged) (D8/T-B2) |
| c05 `+5` | error, 25 | 25, unsupported=1 | consistent |
| c06 `007` | 7 | 7 | consistent |
| c07 `3.5` | error, 25 | 25, unsupported=1 | consistent |
| c08 `0x10` | 16 | 25, unsupported=1 | WRONG VALUE (flagged) |
| c09 numlock `1` then `2` | 2 (no lock) | 1, unsupported=1 | WRONG VALUE (flagged) |
| c10 rate `300` | 300 | 25, unsupported=1 | WRONG VALUE (flagged) |
| c11 `$dev` in device name | mykbd 50 | mykbd 25, unsupported=0 | SILENT WRONG |
| c12 `#hyprlang if NOPE` block | 25 | 30, unsupported=0 | SILENT WRONG |
| c13 `# disabled \` + `input:repeat_rate = 30` | 25 | 30, unsupported=0 | SILENT WRONG |
| c14 `source = sub.conf` (sub: rate 30) | 30 | 25, unsupported=0 (main file only) | SILENT WRONG |
| c15 device key before `name` | 25 (error) | 25, unsupported=1 | consistent |
| c16 plain block | 30 | 30 | consistent |
| c17 `online` / c18 `nope` | 1 / 0 | 1 / 0 | consistent |
| c19 `30 # $x` | 30 | 25, unsupported=1 | flagged conservative (declared) |
| c20 empty / c21 `30abc` | error, 25 | 25, unsupported=1 | consistent |
| c22 `name = a # kbd` | a 50 | a 50 | consistent |
| c23 numlock `2` alone | 2 (no lock) | 0, unsupported=1 | flagged; no lock both |
| c24 unclosed device in file A, `device{repeat_rate=50}` in file B | a=50 (stale device) | a=25, unsupported=1 | WRONG VALUE (flagged) (D12b) |
| c25 two `device a` blocks | a 50 / delay 100 | 50 / 100 | consistent |
| c26 rate `4294967316` | 20 (int cast) | 25, unsupported=1 | WRONG VALUE (flagged) |

Live host (read-only): `hyprctl getoption input:repeat_rate|repeat_delay|numlock_by_default -j` = 40 / 250 / 1; the tool
with `~/.config/hypr/input.conf` (sha 3769c92a…, same as the round-55 fixture) and the host keyboards gives
`live=AGREE` on all three options (receipt `live-getoption.jsonl`; output in `REPORT`). Harness on the host config shows
the expected 40/250/1 but prints config errors for options the harness does not register (kb_layout, touchpad:*) — a
harness limitation, not a tool issue.

## 6. Summary

The C2 tool is right on the ordinary path (plain global/device blocks, merge, comment-cut device name, leading zeros,
bool prefixes, float/empty/words errors, device-key-before-name), and its getoption join is right on the host.
It is WRONG, and in several cases silently WRONG, on: comment after `{`/`}` (D14), backslash continuation (D12a),
`#hyprlang if` blocks (D13), `source =` (D16), `$var` inside `name =` (D17), and the stale current device across files (D12b).
Its docstring's out-of-range policy ("unsupported, line ignored, never guessed") disagrees with the source for
rate/delay/numlock (D7, D22), and its numlock/`-0`/`0x` printed values are guesses that source contradicts (flagged,
not silent). The self-test (83/83) encodes the comment-brace error and so is not an oracle.

## 7. Label legend

Labels used in sections 3-6: T-B1 = c01, T-B1b = c02, T-B2 = c04, T-B3 = c09, T-B5 = c10, T-B6 = c26, T-B7 = c13, T-B8 = c24, T-B9 = c12, T-B10 = c14, T-B11 = c11, T-C<nn> = c<nn>, T-C05/T-C06/T-C07 = c05/c06/c07, T-H1 = live host check (receipt live-getoption.jsonl). Receipts: cases/, harness/ (driver.cpp, mkcases.py, run.py, run14.txt), upstream-sha.txt, excerpts.txt, tool-at-scored-rev.py.
