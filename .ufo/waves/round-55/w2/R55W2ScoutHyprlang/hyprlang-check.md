# R55W2ScoutHyprlang — hyprlang / hyprutils source check of the C2 model (`tools/mado-kbdopts.py`)

Seat: R55W2ScoutHyprlang (w2, falsify, read-only research). Lane: `/home/vgpnk/Projects/shokunin/mado-shokunin`.
Scope: verify the source claims in the C2 docstring and `registration.md` §C2 (v1, frozen `54dacbd8`) and the
errata `registration-v2.md` (E7) against upstream source, pinned sources and runtime behaviour.
No lane file was edited. All scratch work was under `/fast/scratch/hyaku/mado-r55/R55W2ScoutHyprlang/` (removed after
receipts were copied). Receipts: `receipts/` in this directory.

## 0. Sources and what they are

| label | what | how obtained | status |
|---|---|---|---|
| H0.6.8 | hyprlang tag **v0.6.8**: `src/config.cpp` (43049 B), `src/common.cpp`, `include/hyprlang.hpp`, `src/config.hpp`, `src/public.hpp`, `CMakeLists.txt`, `README.md` | `curl -fsSL https://raw.githubusercontent.com/hyprwm/hyprlang/v0.6.8/<path>` | fetched; `receipts/src/src_config.cpp` sha256 `fa1b6898f2f1676de73220450f18f09603f0c3f8833e4c0a7c42c12aebe1de3e` |
| HU0.7.1 | hyprutils tag **v0.7.1**: `src/string/String.cpp` (1657 B), `include/hyprutils/string/String.hpp` | raw.githubusercontent.com | fetched; sha256 `78be183a35d50d33c8e685336d22f839b22f30255e1ec1b9b6bb9c03638b7aad`. hyprlang v0.6.8 `CMakeLists.txt` requires `hyprutils>=0.7.1` |
| R46 pin | `.ufo/waves/round-46/fetch/hyprlang-config.cpp` | lane pin | **byte-identical** to H0.6.8 `src/config.cpp` (both sha256 `fa1b6898…`). Every line citation below valid in both |
| EFB | Hyprland **efb50993780079460b0cbed1363e2166a2de1d9f** (v0.56.2): `src/config/values/ConfigValues.cpp/.hpp`, `types/IntValue.*`, `types/IValue.hpp`, `ConfigValue.hpp`, `config/lua/types/LuaConfigInt.cpp`, `config/values/ConfigValues.cpp` | raw.githubusercontent.com (single files); full-tree search via a `codeload.github.com` tarball of the same commit (50.8 MB, read-only download, disclosed) | fetched |
| PIN | round-55 fetch pins: `Hyprland-ConfigValues.cpp` (sha256 `a76f0507…`, identical to EFB), `Hyprland-InputManager.cpp`, `Hyprland-legacy-ConfigManager.cpp`, `Hyprland-IKeyboard.hpp` | lane pins | used as cited |
| HOST | installed `hyprlang 0.6.8-5`, `hyprutils 0.14.2-1` (`pacman -Q`), `libhyprlang.so.0.6.8` imports `Hyprutils::String::isNumber(const std::string&, bool)` (`nm -D`) | host, read only | host isNumber checked on 10 tokens (`receipts/isnum-host.txt`) — same results as HU0.7.1 |

Hyprland EFB requires `hyprlang>=0.6.7` (`hl/CMakeLists.txt:148`, `HYPRLANG_MINIMUM_VERSION 0.6.7`). The v0.6.8 source
was verified, not the exact binary; the host package is `0.6.8-5`. [INFERENCE] that the installed library is built
from the v0.6.8 tag; the `isNumber` import and the token table agree with it.

## 1. Requested checks — facts with file:line and single-line quotes

Line numbers are H0.6.8 `src/config.cpp` (= R46 pin) unless marked.

### 1.1 `configStringToInt` prefix handling — OBSERVED (source + compiled run)

- `src/config.cpp:185`: `static std::expected<int64_t, std::string> configStringToInt(const std::string& VALUE) {`
- Order of the checks (source order, first match wins):
  1. `src/config.cpp:195`: `if (VALUE.starts_with("0x")) {` → `parseHex` = `stoll(value, &pos, 16)` with a full-consumption check (`config.cpp:187-193`). Lower-case `0x` only.
  2. `src/config.cpp:198`/`:232`: `rgba(` / `rgb(` branches (colour functions, returns ARGB int). **Not modelled by the tool**.
  3. `src/config.cpp:259`: `} else if (VALUE.starts_with("true") || VALUE.starts_with("on") || VALUE.starts_with("yes")) {` → `return 1;`
  4. `src/config.cpp:261`: `} else if (VALUE.starts_with("false") || VALUE.starts_with("off") || VALUE.starts_with("no")) {` → `return 0;`
  5. `src/config.cpp:265`: `if (VALUE.empty() || !isNumber(VALUE, false))` → error `cannot parse "…" as an int.`
  6. `src/config.cpp:269`: `const auto RES = std::stoll(VALUE);` → decimal; a throw gives `stoll threw: …`.
- Booleans are prefix matches, case-sensitive: confirmed by the run (`onion`→1, `nope`→0, `true1`→1, `yes123`→1).
- Hex: `0x10`→16 (OBSERVED), `0X10` → error (OBSERVED: `cannot parse "0X10" as an int.`).

Compiled from the exact `configStringToInt` body (`sed` extract of `src/config.cpp` 185–…; `isNumber`/`trim` from HU0.7.1) and run
(`receipts/token-table.txt`, harness `receipts/main.cpp`):

```
"0x10" -> OK 16          "0X10" -> ERR cannot parse "0X10" as an int.
"+5" -> ERR              "007" -> OK 7           "-3" -> OK -3
"3.5" -> ERR             "5." -> ERR             ".5" -> ERR
"true" -> OK 1           "on" -> OK 1            "yes123" -> OK 1
"false" -> OK 0          "no" -> OK 0            "nope" -> OK 0
"25 " -> ERR             "   25" -> ERR          "" -> ERR
"-0x10" -> ERR           "--5" -> ERR            "1e3" -> ERR
"999999" -> OK 999999    "1000000" -> OK 1000000 "123456789012345678901" -> ERR stoll threw: stoll
```

### 1.2 What `isNumber` accepts — OBSERVED (HU0.7.1 source + compiled + host library)

- `hyprutils/src/string/String.cpp:25`: `bool Hyprutils::String::isNumber(const std::string& str, bool allowfloat) {`
- `:34`: `if (i == 0 && str.at(i) == '-') {` — a leading `-` is accepted.
- `:39`: `if (!isdigit(c)) {` — with `allowfloat=false` (the only call, `config.cpp:265`) any non-digit after the sign is rejected.
- `:58`: `return isdigit(str.back()) != 0;` — the last character must be a digit.

| input | isNumber(allowfloat=false) | configStringToInt result | host libhyprutils 0.14.2 isNumber |
|---|---|---|---|
| `+5` | false | ERR `cannot parse "+5" as an int.` | 0 |
| `007` | true | OK 7 | 1 |
| `-3` | **true** | OK -3 | 1 |
| `3.5` | false | ERR | 0 |
| `0x10` | false (never reaches `isNumber`: `0x` branch at :195) | **OK 16** | 0 |
| `-0` | true | OK 0 | 1 |
| `""`, `-` | false | ERR | 0, 0 |

### 1.3 `.min` / `.max` enforcement for INT options — OBSERVED: **not enforced on the hyprlang path**

- The option table declares the ranges: `EFB src/config/values/ConfigValues.cpp:279` `MS<Int>("input:repeat_rate", … 25, {.min = 0, .max = 200, …`
  and `:280` `MS<Int>("input:repeat_delay", … 600, {.min = 0, .max = 2000}),` (PIN line 279/280 identical).
- Readers of `m_min`/`m_max` in the whole EFB tree (grep `m_min|m_max` over `src/`): the legacy path reads them only in
  `ConfigValues.cpp:54/68/82` (`opt(x->m_min), opt(x->m_max)` — dump/JSON printing) and in luminance rules
  (`legacy/ConfigManager.cpp:862-868`, which are values not option bounds). `values/types/IntValue.cpp` stores them; nothing compares.
- The **only** comparison site is the Lua path: `src/config/lua/types/LuaConfigInt.cpp:55`
  `if (m_max.has_value() && data > *m_max)` / `:56` `…"value {} is more than the maximum of {}"`. `:52` is the matching
  `m_min` check. This applies when the config is `.lua`; the hyprlang (`.conf`) path does not reach it.
- The hyprlang parser does not validate option bounds (CIntValue registers only the default: `legacy/ConfigManager.cpp` maps
  `CIntValue` → `registerConfigVar(NAME, Hyprlang::INT{p->defaultVal()})`, no range). Observed run: `input:repeat_rate = -3`,
  `input:repeat_delay = 5000`, `input:numlock_by_default = 7` are stored verbatim (`receipts/driver-out.txt` t3: `global: rate=-3 delay=5000 numlock=7`; s5: `rate=-3 delay=5000`).
- So **the frozen text's range source is wrong as an enforcement claim**: `.min/.max` are declarations, enforced by Lua only.
  The effect on a hyprlang config is in §1.6 (`max(0,·)` clamp).
- **Enforcing site for the `.conf` path: none found** in H0.6.8, HU0.7.1, EFB (full-tree search). [INFERENCE: absence over the whole tree at efb50993; the Hyprland 0.56.2 binary was not built, so a dynamic path is not excluded.]

### 1.4 Special-category merge for repeated device blocks — OBSERVED

- `src/config.cpp:368`: `// When parsing the key field itself, match by the value being set.`
- `src/config.cpp:376`: `if (existingKeyValue != impl->currentSpecialKey)` (non-key fields match the category whose key equals the current block key).
- `src/config.cpp:438`: `impl->currentSpecialKey = value;` (set by the block's first `name` line).
- Runs: `t1.conf` (two `device { name = k1 … }` blocks, one `repeat_rate`, one `repeat_delay`) → `device[k1]: rate=50 (set) delay=800 (set)` (merged); `s1.conf` (same key set in both blocks, 50 then 70) → `rate=70 (set)` — **the later write of the same key wins** (this was the unpinned point in the C2 ambiguity review; now observed).
- Tool on the same inputs (`receipts/tool-probe-out.txt`): t1 `keyboard=k1 repeat_rate=50 repeat_delay=800 numlock=0 from=D/D/- unsupported=0`; s1 `keyboard=k1 repeat_rate=70 repeat_delay=600 numlock=0 from=D/-/- unsupported=0`. **Agree.**

### 1.5 The "first value must be the key" rule — OBSERVED

- `src/config.cpp:434`: `if (VALUEIT == PCAT->values.end() || VALUEIT->first != sc->key) {`
- `src/config.cpp:435`: `result.setError(std::format("special category's first value must be the key. Key for <{}> is <{}>", PCAT->name, PCAT->key));`
- Run `t2.conf` (`device { repeat_rate = 50 ; name = k1 }`): `parse error: YES: Config error in file … at line 2: special category's first value must be the key. Key for <device> is <name>`; `device[k1]: rate=25 (unset)`.
- The rule applies when the category is **created** by its first line (the non-matching path at `:415-441`). A same-name block that already exists goes through the merge path (§1.4).
- The tool does not implement it as an error: a device key with no current device is counted `unsupported +1` and ignored (C2 text). **Agrees on the effective value (device unset); disagrees on the channel (hyprlang reports a config error, the tool a count).** The registration does not state the rule at all.

### 1.6 Consequence for the ranges — `applyConfigToKeyboard` clamp — OBSERVED in the pin, INFERRED at runtime

- PIN `Hyprland-InputManager.cpp:1282`: `pKeyboard->m_repeatRate  = std::max(0, REPEATRATE);`
- PIN `:1283`: `pKeyboard->m_repeatDelay = std::max(0, REPEATDELAY);`
- PIN `:1284`: `pKeyboard->m_numlockOn   = NUMLOCKON;` — `m_numlockOn` is `int` (`Hyprland-IKeyboard.hpp:123`: `int m_numlockOn = -1;`).
- So for `input:repeat_rate = -3` Hyprland's stored rate is **0** [INFERENCE: stored value -3 OBSERVED in hyprlang; the clamp is pinned]; for `repeat_delay = 5000` the stored delay is **5000** (no upper clamp).
  `numlock_by_default = 7` stores `m_numlockOn = 7` [INFERENCE on the consumer; the consumer of `m_numlockOn` is not in the pins].
- The C2 text says the clamp is "a no-op on the modelled range" — true for 0..200 / 0..2000, but it is not a no-op for the values the tool rejects.

## 2. Every place the C2 docstring / registration §C2 contradicts or goes beyond the source

Class: **CONTRADICTS** = the text states something the source does not do; **BEYOND** = the text models a rule the source
does not state (a conservative choice, fine if declared); **MISSING** = a source behaviour the text does not mention.
Observed = run or quoted line. Each row names the attack input when one exists.

| # | text (docstring / registration §C2) | source fact (file:line / run) | class | attack / evidence |
|---|---|---|---|---|
| 1 | "hex, sign, float, empty, words → `unsupported`" (registration §C2 and docstring `parse_value`) | hex `0x10` → **16** (`config.cpp:195-197`, run); sign `-3` → **-3** (`hyprutils String.cpp:34`, run); `+5`, `3.5`, `0X10` → error (run) | CONTRADICTS (hex and `-`) | `s4`/`t4`: tool reports `repeat_rate=25 … unsupported=1` for `repeat_rate = 0x10`, hyprlang gives 16. Flagged, not silent. |
| 2 | "matches `[0-9]+` → that decimal integer" | `isNumber` accepts a leading `-` then digits (`String.cpp:34,58`); `007`→7 (run) | CONTRADICTS (for `-digits`) | `s5.conf`: `input:repeat_rate = -3` → tool `unsupported=2`; hyprlang stores -3, effective 0 (§1.6). |
| 3 | range "0..200", "0..2000" "the table's own `.min`/`.max`" (registration §C2 and docstring) | `.min/.max` not enforced on the `.conf` path; enforced by Lua only (`LuaConfigInt.cpp:55-56`); hyprlang stored 5000 / -3 / 7 (run `t3`, `s5`) | CONTRADICTS (enforcement claim) | `t3.conf` → tool `repeat_rate=25 … from=- unsupported=3` (flagged). The cited basis (`ConfigValues.cpp:277-280`) declares, does not enforce. |
| 4 | "numlock_by_default 0..1" with the range attributed to ConfigValues.cpp:277 (registration v1) | `PIN ConfigValues.cpp:277`: `MS<Bool>("input:numlock_by_default", "Engage numlock by default.", false,` — a Bool with no `.min/.max`; stored as INT (run `numlock=7`) | CONTRADICTS in v1; **v2 E7 already retracts it** ("a lane modelling rule, not a source range") | `t3`: numlock 7 → tool `numlock=0 … unsupported` (flagged). |
| 5 | "a device-block key line with no current device → `unsupported +1`, ignored" | hyprlang: config **error** `special category's first value must be the key` (`config.cpp:434-435`, run `t2`); device value unset | BEYOND/MISSING (the error and the rule are not in the text) | `t2.conf` → tool `unsupported=1`; the effective value agrees, the channel (config error) is absent from the tool. |
| 6 | "A line ... `source` ... LHS equal to `source` … ignored" (docstring: "an LHS equal to `source` are ignored") | PIN `legacy/ConfigManager.cpp:614`: `m_config->registerHandler(&::handleSource, "source", {false});`; `:1802` `CConfigManager::handleSource(…)` reads the file. The tool ignores it and does not count it (A19 in ambiguity review). | CONTRADICTS (silent: the source is read by Hyprland) | Not run (no sourced file in the lane). [INFERENCE for effect: sourced keys apply in Hyprland, the tool reports `unsupported=0`.] Recommend the tool count `source` as unsupported. |
| 7 | "a line whose first character is `#` is skipped" | `config.cpp:683`: `if (!impl->currentFlags.ifDatas.empty() && impl->currentFlags.ifDatas.back().failed)` — `#hyprlang if VAR` directives gate the following lines (`parseComment`, `config.cpp:555-603`) | MISSING (conditional blocks) and then **silent wrong value** | `s3.conf` (below): tool `repeat_rate=60 from=G unsupported=0`, hyprlang `rate=25` (line skipped). **BROKEN.** |
| 8 | (grammar) "A line without `=`: … a line ending in `{` pushes its text before the `{` (stripped)" | `config.cpp:674`: `auto commentPos = line.find('#');`, `:698`: `line = line.substr(0, commentPos);` — hyprlang removes an unescaped `#` comment **before** the block test (`:713`, `:901`) | CONTRADICTS (`input { # c` opens a block in Hyprland; not in the tool) | `t5.conf` below. **BROKEN, silent.** |
| 9 | "the RHS containing `##` adds one" (docstring) | `config.cpp:691-702`: `##` is an escape: the second `#` is kept and the comment is not cut. `on##` → **1** (run `t6`) | BEYOND (the rule is conservative; the docstring gives no hyprlang basis) | `t6.conf`: tool `unsupported=1` (flagged); hyprlang gives 1. Flagged, not silent. |
| 10 | "a line containing `$`, `{{` or a backslash adds one" | `$V = 40` definitions and `$V` expansion (run `s4`: `input:repeat_rate = $V` → **40**) | BEYOND (conservative, flagged) | `s4.conf`: tool `repeat_rate=25 … unsupported=1`. Flagged, not silent. |
| 11 | "`configStringToInt` … `true`/`on`/`yes` → 1 (checked first)" | `config.cpp:259,261` (true/on/yes → 1; false/off/no → 0), prefix-matched | SURVIVES | run: `onion`→1, `nope`→0, `yes123`→1 |
| 12 | `KEY is the stack joined with ':' then ':' then LHS` (v1); v2 E7 "KEY is LHS when the stack is empty" | `config.cpp:` key build is `valueName += c + ':'` for each category, then `+= command` (`:283-285`) — with an empty stack there is no leading `:` | v1 CONTRADICTS (leading colon); v2 SURVIVES | F10 (lane) and the ambiguity review A12 |
| 13 | Device NAME = "RHS with a trailing `#` comment cut and stripped" | `config.cpp:698` cuts a single `#`; `name = kbd#1` → `kbd` (run `s2`), tool `--keyboard kbd` → `repeat_rate=50 from=D` | SURVIVES | run `s2`: `device[kbd]: rate=50 (set)`; tool `keyboard=kbd repeat_rate=50 … from=D/-/-` |
| 14 | "`applyConfigToKeyboard` clamps the stored rate and delay with `std::max(0, …)` — a no-op on the modelled range" | PIN `Hyprland-InputManager.cpp:1282-1283` (quoted §1.6); on negative input the clamp is **not** a no-op (-3 → 0) | SURVIVES as stated, MISSING the negative effect | §1.6; the tool reports `unsupported` (not 0) for `-3` |
| 15 | "`getDeviceInt` uses the device value when the user set it, else the global option" | PIN `legacy/ConfigManager.cpp:1119`: `if ((!VAL || !VAL->m_bSetByUser) && !fallback.empty())` | SURVIVES | run `t1`/`t5`: `(set)`/`(unset)` tracks `m_bSetByUser` |
| 16 | "`rgba(…)` / `rgb(…)`" are not mentioned | `config.cpp:198,232` — colour functions return an int | MISSING | `s6.conf`: `input:repeat_rate = rgba(10,20,30,1.0)` → hyprlang stores **4278850590**; tool `unsupported=1` (flagged). |
| 17 | (grammar) "decimal … `[0-9]+` → that integer" | `config.cpp:269` `std::stoll`; a value above int64 → `stoll threw` (config error) | MISSING (error channel) | run `123456789012345678901` → `stoll threw: stoll`; tool maps large digits to 10**6 → `unsupported` (flagged). |

## 3. Silent wrong values found (C2 "never guessed" rule broken) — attack inputs and outputs

Both are inside the frozen input grammar: no frozen sentence forbids them, the committed fixtures and the hold-out contain
**no** inline `{ #` / `} #` and **no** `#hyprlang` directive (`grep -rnE '\{ *#|\} *#|#hyprlang' fixtures/c2 fixtures/c2-holdout` → empty;
`~/.config/hypr/input.conf` also empty). The tool is unchanged; it was run read-only on scratch copies (`python3 -I`).

### A-t5 — inline comments on block lines

Input `receipts/cases/t5.conf` (bytes as written):
```
input { # main
    repeat_rate = 30
} # end
device {
    name = k1
    repeat_rate = 50
} # keep
repeat_delay = 400
```
Tool, `--keyboard k1 --keyboard k2 --keyboard kbd`:
```
MADO_KBDOPT: keyboard=k1 repeat_rate=50 repeat_delay=400 numlock=0 from=D/D/- unsupported=0
MADO_KBDOPT: keyboard=k2 repeat_rate=25 repeat_delay=600 numlock=0 from=-/-/- unsupported=0
MADO_KBDOPT: DONE keyboards=3 unsupported=0 live=NONE
```
Hyprlang 0.6.8 (compiled from the fetched source, `receipts/driver-out.txt`):
```
parse error: no
global: rate=30 delay=600 numlock=0
device[k1]: rate=50 (set) delay=600 (unset)
```
Effective per Hyprland's rule (`getDeviceInt`, PIN `:1119`): k1 = 50 D / 600 `-` / 0 `-`; k2 = 30 G / 600 `-` / 0 `-`.
The tool says k1 delay = **400 D** (a top-level `repeat_delay` line that Hyprland never applies, `input:` is not set) and k2 rate = **25 `-`** (the `input {` block was never opened, so `repeat_rate = 30` was dropped). Two wrong values, `unsupported=0`, no flag. **BROKEN.**
Cause: the tool's rule "a line ending in `{`" does not cut the comment first; `} # end` is not `}` and is ignored, so the stack stays open and the later `device {` is nested. Source: `config.cpp:674,698,713,901`.

### A-s3 — `#hyprlang if` conditional directives

Input `receipts/cases/s3.conf`:
```
#hyprlang if NOPE
input:repeat_rate = 60
#hyprlang endif
input:repeat_delay = 700
```
Tool: `keyboard=k1 repeat_rate=60 repeat_delay=700 numlock=0 from=G/G/- unsupported=0` (same for k2, kbd).
Hyprlang: `global: rate=25 delay=700 numlock=0` (the line under the failed `if` is not applied; `config.cpp:683`; directive parse `:555-603`).
The tool applies 60; Hyprland applies 25. **BROKEN, silent.** The frozen rule "everything outside it is unsupported, never guessed" should have counted the directive (`#hyprlang`) as unsupported; it treats it as a comment.

## 4. Verdicts for the requested checks

| target | verdict | evidence pointer |
|---|---|---|
| configStringToInt prefix handling (true/on/yes, false/off/no, 0x, decimal) | **SURVIVES** for booleans (prefix, case-sensitive, checked first); **BROKEN** for the docstring's "hex → unsupported" (hex parses to 16) | §1.1; `receipts/token-table.txt`; `src/config.cpp:195-197,259-269` |
| isNumber on `+5`, `007`, `-3`, `3.5`, `0x10` | `+5` rejected (SURVIVES), `007`→7 (SURVIVES), `3.5` rejected (SURVIVES), **`-3` accepted** (BROKEN vs "sign → unsupported"), `0x10` never reaches isNumber, parses 16 (BROKEN vs "hex → unsupported") | §1.2; `hyprutils/String.cpp:25,34,39,58`; `receipts/isnum-host.txt` |
| Hyprland enforcement of `.min/.max` for INT options | **NOT ENFORCED on the `.conf` path**; enforced only by Lua (`LuaConfigInt.cpp:52-56`). The frozen "outside → unsupported" is a tool choice, not a Hyprland behaviour; the cited basis is a declaration only | §1.3; `receipts/driver-out.txt` (t3); `receipts/tool-probe-out.txt` (t3) |
| special-category merge for repeated device blocks | **SURVIVES**: same-name blocks merge (by `name`); a later write of the same key wins | §1.4; `config.cpp:368-376,438`; `receipts/driver-out.txt` t1, s1 |
| "first value must be the key" rule | **SURVIVES** as source behaviour (error at `config.cpp:434-435`); the registration does not state it; the tool counts instead of erroring | §1.5; `receipts/driver-out.txt` t2 |
| C2 docstring/registration claims in §2 | 9 rows CONTRADICT or go BEYOND the source (rows 1–6, 8, 9, 10, 12 v1); 2 silent-wrong results (§3: A-t5, A-s3) | §2, §3 |

## 5. Not verified / limits

- Hyprland runtime was not built or run: the numlock consumer of `m_numlockOn`, and the keyboard repeat effect, are [INFERENCE] from the pins, not observed.
- The installed `libhyprlang.so.0.6.8` was not run; the v0.6.8 tag source was compiled against the host `libhyprutils.so` 0.14.2 (the same `isNumber` symbol), and the 10-token host check agreed with HU0.7.1.
- The Lua path was not run (no `.lua` config); its enforcement is read from source only.
- `source` (row 6) was not executed: no sourced file exists in the lane and the receipts do not cover it.
- I did not run the lane's frozen counters/harness or the committed/hold-out fixtures; the "fixtures contain no inline `{ #`/`#hyprlang`" statement is a `grep`, not a run.
- No tool was installed or upgraded. Used pre-installed `g++`, `curl`, `python3`, `nm`, `sed`, `grep`. No `hyprctl` keyword/dispatch/reload was run.

## 6. Receipts (in `receipts/`)

- `token-table.txt` — configStringToInt on 37 tokens (exact source body).
- `isnum-host.txt` — host libhyprutils isNumber on 10 tokens.
- `driver-out.txt` / `driver.cpp` — hyprlang v0.6.8 built from the fetched sources: t1–t6 (merge, key-before-name, ranges, hex/`+`, inline comments, `on##`).
- `driver2-out.txt` / `driver2.cpp` — s1–s6 (override, `kbd#1`, `#hyprlang if`, `$V`, `-3`/5000, `rgba`).
- `tool-probe-out.txt` — `python3 -I tools/mado-kbdopts.py --config <case> --keyboard k1 --keyboard k2 --keyboard kbd` on each case (read-only; tool not modified); selftest `83/83`.
- `cases/*.conf` — the probe inputs. `quotes.txt` — exact quoted source lines. `host-receipts.txt` — `hyprctl version`, `hyprctl getoption … -j` (read verbs), `input.conf` lines 14–18.
- `src/` — fetched sources (`src_config.cpp`, `String.cpp`, `ConfigValues.cpp`, `IntValue.*`, `LuaConfigInt.cpp`, `Hyprland-efb-values-ConfigValues.cpp`); `SHA256SUMS-fetched.txt`.

Host (read only): `hyprctl version` → Hyprland 0.56.2 (efb50993…). `hyprctl getoption input:repeat_rate -j` → 40, `input:repeat_delay` → 250, `input:numlock_by_default` → 1. `~/.config/hypr/input.conf` (54 lines) sets `repeat_rate = 40`, `repeat_delay = 250`, `numlock_by_default = true` inside `input {` (lines 14–18); no inline comment on a block line (grep empty).
