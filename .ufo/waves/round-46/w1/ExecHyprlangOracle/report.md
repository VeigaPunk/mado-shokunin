# Differential test of the C1 contract against the host's hyprlang 0.6.8

Seat `ExecHyprlangOracle`, mado round 46 wave w1, 2026-10-26. Lane `/home/vgpnk/Projects/shokunin/mado-shokunin`.
Claims frozen at `.ufo/waves/round-46/registration.md` (freeze `8c5434c6`, base `b22ea56b`). Seat dir:
`.ufo/waves/round-46/w1/ExecHyprlangOracle/`; evidence in `evidence/`; sources next to this file.

## 0. Result in one paragraph

A true oracle was built from the host's own parser (`g++ -std=c++23 -lhyprlang`, `/usr/lib/libhyprlang.so.0.6.8`,
headers `/usr/include/hyprlang.hpp`) that registers exactly what Hyprland 0.56.2 registers for the input-device plane
and reproduces the accessors the C1 reference models. **16,800 random configs (251,959 config lines, 15,215 of them
comparable — the other 1,585 the reference itself declines) were parsed by both models.** The reference agrees on
15,181 of 15,215 comparable configs (99.78 %). The 34 that diverge reduce to exactly **two contract bugs**, each with
a minimal repro below: (B1) a key Hyprland does not register, written inside a `device` block after a `device[X]:…`
line, silently re-targets the rest of the block to *another* device, which the reference's single "current device"
model cannot see; (B2) a `scroll_factor` decimal that underflows a 32-bit float to zero is modelled as `0.0` where
`std::stof` throws and never sets the key. Everything else the contract models — comments, `##`, continuations, CRLF,
`[[EMPTY]]`, empty RHS, the four device-line forms, merges, duplicate names, creation order, the `us`/empty default
chain, the `std::stof` prefix rule and the 0..100 clamp including `-0.00` — produced **zero** divergences.

The share of generated lines the reference counts `unsupported` is **0.89 %** (2,255 of 251,959); within the clean
grammar (224,565 lines) it is **0.000 %**. The gate is deliberate, not vestigial: 11 of the frozen 90 fixtures expect
it (`fixturescan.py` lists them — `mouse-nan`, `mouse-hex`, `mouse-overflow`, `variable`, `expression`, `directive`,
`flat-device-key`, `block-first-not-name`, `rename`, `bracket-name-key`, `not-compared-beats-differ`). It does not
hide the divergences in §3: both mechanisms live in configs the reference marks fully modelled.

## 1. The oracle (what makes it the truth for this plane)

`oracle.cpp` (Appendix A) does three things and nothing else:

1. **Registers what Hyprland registers.** `addSpecialCategory("device", {.key = "name"})` and the 47 device values
   with the exact types and defaults of `fetch/Hyprland-ConfigManager.cpp:518-565` (`kb_layout` default `"us"`,
   `scroll_factor` `FLOAT{-1}`, …), plus the six `input:kb_*` globals and `input:scroll_factor` with the defaults of
   `fetch/Hyprland-ConfigValues.cpp:271-276` (`fetch/Hyprland-ConfigValues.cpp:272` — `"us"`), and
   `input:touchpad:*` so a real `input { touchpad { … } }` stays error-free.
   `[[EMPTY]]` is the literal from `/usr/include/hyprland/src/macros.hpp:24`.
2. **Transcribes the accessors 1:1** from `fetch/Hyprland-ConfigManager.cpp:1115-1201`:
   `getConfigValueSafeDevice` = `getSpecialConfigValuePtr("device", val, dev)`; fall through to the global when the
   special value is missing or `!m_bSetByUser` and the fallback is non-empty
   (`:1117`, `:1128`); `getDeviceString` maps `[[EMPTY]]` to `""`; `deviceConfigExplicitlySet` = `VAL && m_bSetByUser`.
   Pointer: `fetch/Hyprland-InputManager.cpp:1379-1381` — `std::clamp(getDeviceFloat(dev, "scroll_factor",
   "input:scroll_factor"), 0.F, 100.F)` **only when** `deviceConfigExplicitlySet`, else `nullopt` → `-1`.
3. **Prints the observable** the way HyprCtl does: the five stored names, and `scrollFactor` with
   `fetch/Hyprland-HyprCtl.cpp:770` (`"scrollFactor": {:.2f}`) — so `-0.0` is `"-0.00"`, not `"0.00"`.

It parses the config files with `CConfig::parseFile` in argument order on one `CConfig`, which is what Hyprland's
`source =` handler does (`fetch/Hyprland-ConfigManager.cpp:1842`, `m_config->parseFile(value.c_str())`), so the
multi-file category-stack and carry-over semantics are the host's, not mine.

Boundary (deliberately not modelled): XKB compilation and the FALLBACK reset (`IKeyboard::setKeymap`), the virtual
keyboard's keymap takeover, `deviceNameToInternalString`, `source =` following, and runtime `hyprctl keyword` drift.
Those sit *downstream* of "config → expected names / scroll factor", which is the step the reference models and the
step this test exercises.

Cross-check on live data: `hostcheck.py` reads the lane's own live receipt
(`.ufo/waves/round-46/receipts/live-devices-host-l1.txt`), extracts its 10 keyboard names + 4 pointer names, runs the
oracle on `~/.config/hypr/input.conf` and diffs: **14/14 AGREE** (`evidence/hostcheck.txt`). Nothing from the host is
written into this report.

## 2. Corpus

`gen.py` (Appendix B) builds each case as a list of *pieces* (statements), splits pieces — never lines — over 1–3
files, then decorates lines with comments (`#`, `##`, `# a##b`) and backslash continuations, and joins with `\n` or
`\r\n`. Two grammars:

* **clean** — forms the reference models without `unsupported`: flat `input:kb_*` (with and without a bracket name),
  `input { … }` with a nested `touchpad` and a deeper `general { input { … } }`, `device { name = X … }`,
  `device[X] { … }`, `device[X]:k = v`, one `device:name = X` selector, merges and duplicate names, `[[EMPTY]]`,
  empty RHS, registered-but-irrelevant keys (`sensitivity`, `natural_scroll`, `tap-to-click`, …), one unregistered
  key, nested categories, noise lines, an unclosed category at EOF.
* **raw** — clean pieces plus exactly one tagged piece from the reference's `unsupported` list: `# hyprlang`
  directive, `$var`, `{{ }}`, interior backslash, selector-less `device:k`, a block whose first key is not `name`,
  a rename, `inf`/`nan`/hex/denormal `scroll_factor`, a flat `device:k` after a bracket line, a flat `device:k`
  after a file that ended with an unclosed block, a selector then a block, and a continuation whose backslash is
  followed by CRLF.

| corpus | cases | compared | declined | config lines | unsupported increments | B1 | B2 | unexplained |
|---|---|---|---|---|---|---|---|---|
| seed 46, 8000 clean + 800 raw | 8,800 | 8,008 | 792 | 131,897 | 1,116 | 13 | 5 | 0 |
| seed 7, 4000 clean + 400 raw | 4,400 | 4,004 | 396 | 65,823 | 570 | 6 | 2 | 0 |
| seed 46, 3200 clean + 400 raw | 3,600 | 3,203 | 397 | 54,239 | 569 | 7 | 1 | 0 |
| **total** | **16,800** | **15,215** | **1,585** | **251,959** | **2,255 (0.89 %)** | **26** | **8** | **0** |

Attribution is computed, not asserted: `attribute.py` re-derives, per diverging case, whether the divergence is a
name/`kb_file` mismatch or a `scroll_factor` mismatch carrying a decimal whose exact value is non-zero but whose
float32 is zero (`evidence/attribute.txt`). Form coverage inside the 8,008 comparable cases of the largest corpus
(`evidence/forms.txt`): CRLF 19.7 %, `[[EMPTY]]` 54.9 %, `device {` 75.4 %, `device[X] {` 35.6 %,
`device[X]:k` 38.7 %, backslash continuation 46.0 %, duplicate block names 18.8 %, empty RHS 49.7 %, `##` 56.6 %,
multi-file 34.1 %, nested category 40.3 %, an unregistered key 45.1 %.

Every comparison covers, per device name: the five XKB names in HyprCtl order (`layout, variant, options, model,
rules`), `kb_file` (set/`-`), the pointer scroll factor as printed with two decimals, block presence, and the device
special-category key list in creation order.

## 3. The two contract bugs

### B1 — an unregistered key re-targets the rest of the device block (26 of 15,215 configs)

**Mechanism (host).** hyprlang keeps *two* selection states per special category: `currentSpecialCategory` (the
category last touched) and `currentSpecialKey` (its key value). A bracket form sets the key unconditionally
(`fetch/hyprlang-config.cpp:297`); a block's `name =` line sets it **only when the category is created**
(`:438`), and it is cleared only when the category stack empties (`:896`). Every later value line first tries the
current category and, when the category has no such value, re-selects **by `currentSpecialKey`**
(`:376`). So a key Hyprland does not register — a typo, a key from another Hyprland version, or one of the 40 device
keys the reference deliberately ignores — silently moves the selection to whichever device `currentSpecialKey` still
names, and every *following* key of the block lands on that other device.

**Mechanism (reference).** One `cur` name, set by `name =` / `device:name =` and cleared when the stack empties; an
unknown key is ignored. It therefore attributes the rest of the block to the block's own device.

**Minimal repro A1 (`device` block form)** — `unsupported == 0` for the reference, so a scored run would compare it:

```
device[kbd] {
  kb_layout = de
}
device[mouse] {
  scroll_factor = 0.5
}
device[kbd]:kb_variant = intl
device {
  name = mouse
  tap-to-click = 0
  nope = 1
  kb_options = compose:caps
}
```

| device | reference expects | host stores | verdict the tool prints |
|---|---|---|---|
| `kbd` | `de intl "" "" ""` | `de intl compose:caps "" ""` | `differ=options DIFFER` (false) |
| `mouse` | `us "" compose:caps "" ""` | `us "" "" "" ""` | `differ=options DIFFER` (false) |

**A2 (flat selector form)** — same divergence with `device:name = mouse` + `device:nope = 1` +
`device:kb_options = compose:caps` instead of the block: reference `mouse: options=compose:caps`, host `kbd:
options=compose:caps`.

**A9 (a real typo)** — `tap_to_click = 1` (the registered key is `tap-to-click`) inside the block is enough:
reference `mouse: options=compose:caps`, host `kbd: options=compose:caps`.

**A4 (the same class on the pointer surface)** — with `scroll_factor = 0.5` after the unknown key: reference
`mouse: scrollFactor=0.50`, host `kbd: scrollFactor=0.50`, `mouse: -1.00`.

**A3 (empty-named block)** — `device { name = }` leaves `currentSpecialKey` at `""` when the block closes, and a
`device:name = b` that matches an existing block passes through the same path: `device:nope = 1` then
`device:kb_options = compose:caps` puts the option on the empty-named block, not on `b`.

Corpus instances of this class: 26 configs — 21 on the five XKB names, 4 on `kb_file`, 4 on `scroll_factor` (four
cases carry two surfaces). All 26 carry an unregistered key next to a bracket line, a selector line or an
empty-named block (`evidence/attribute.txt` splits B1/B2/unexplained per corpus; per-case trigger tags are in
`evidence/corpus-*.json`). The remaining 8 divergences are B2 below.

### B2 — `scroll_factor` literals that underflow to zero (8 of 15,215 configs)

**Mechanism (host).** `fetch/hyprlang-config.cpp:467` — `VALUEIT->second.setFrom(std::stof(value));`. For a decimal
whose magnitude is below the smallest subnormal float, `strtof` returns 0 with `ERANGE`, and `std::stof` throws
`out_of_range`; `configSetValueSafe` then returns an error with the value untouched, so `m_bSetByUser` stays false
and `deviceConfigExplicitlySet` is false → `scrollFactor` prints `-1.00`.

**Mechanism (reference).** `read_float` parses the longest numeric prefix (`:62`, `:64`) and rounds it to float32;
for `1e-46`/`1e-50`/`1e-999` the rounded float is `0.0`, so the "nonzero value below 2**-126" guard — which tests the
*rounded* value — does not fire, and the key is recorded as `0.0` instead of "unset". The wrong window is exactly
`0 < |literal| < 2**-150` (half the smallest subnormal `2**-149`, below which the float rounds to zero); the
reference's guard covers `[2**-150, 2**-126)` correctly. Measured: `1e-45` (rounds to `1.4e-45`), `1e-40`, `5e-39`,
`1e-38` are correctly declined; `1e-46`, `1e-50`, `1e-999` are wrongly accepted (`evidence/repro.txt` section C).

**Minimal repro A5/A6** (`unsupported == 0`, so a scored run would compare it):

```
device[mouse]:scroll_factor = 1e-999        # A5   (1e-50 behaves identically, A6)
```

| | reference | host |
|---|---|---|
| expected / printed `scrollFactor` | `0.00` | `-1.00` |
| key set by user | yes | no (`std::stof` threw) |

Tool-level: a mouse with such a line is reported `scroll_factor=0.00 reported=-1.00 verdict=DIFFER` → exit 1, a
false positive. Corpus instances: 8 configs (5 + 2 + 1 across the three runs), each with a `…e-…` literal that the
reference accepts.

### Float matrix (why nothing else in the float model diverges)

`evidence/repro.txt` section C walks 38 literals through `read_float` and the host. Agreement on: `0`, `-0`, `-0.0`,
`0e0`, `0.0000`, `.5`, `5.`, `1e-7`, `0.7x` (prefix), `12x34`, `fast` (unset both), `2.675` → `2.67`, `50.555` →
`50.56`, `99.999` → `100.00`, `250` → `100.00`, `-3` → `0.00`, `1e38`/`3.4e38` → `100.00`,
`1.1754943508222875e-38` (accepted, prints `0.00` both), `1e-38`/`1e-39`/`1e-40`/`1e-45` (reference declines; host
leaves unset). The reference *declines* `inf`/`-inf`/`nan`/`0x10`/`0X1p3` where the host sets `100.00`/`0.00`/`nan`/
`16.00`/`8.00` — an over-conservative decline, not a wrong expectation (see §4).

## 4. What the reference declines (1,585 configs) and what the host actually does

The reference prints `NOT_COMPARED` (exit 5) for any config with one unmodelled line. In my raw grammar **every**
declined class was in fact decided by the host parser; the reference's justification for two of them is not what the
parser does. `evidence/repro.txt` section B has a minimal config per class:

| class | incr./case | what the host does with it | reference |
|---|---|---|---|
| `# hyprlang if/endif` | 2 | the guarded line applies (`kbd: layout de`) | declined |
| `$lay = de` + `input:kb_layout = $lay` | 1 | substitutes → global `de` | declined |
| `{{ 1 + 2 }}` | 1 | evaluates → global `3` | declined |
| `a\{b` in a value | 1 | escape removal → `options = "a{b"` | declined |
| flat `device:kb_layout` with no selector | 2 | creates a device block literally named `0`; both keys land there | declined |
| block whose first key is not `name` | 2 | keeps **one** category, renamed by the later `name =` line | declined |
| a second `name =` (rename) | 2 | renames the category in place (`:348` first branch), one block | declined |
| `inf`/`nan`/`0x10`/`0X1p3`/denormal `scroll_factor` | 1 | `100.00`/`nan`/`16.00`/`8.00`/unset | declined |
| flat `device:kb_file` **after** `device[X]:…` | 1 | applies to `X` (`:297` left `currentSpecialKey = X`) | declined as "first value must be the key" |
| flat `device:kb_file` in the file after an unclosed block | 1 | applies to the carried-over device (state survives `parseFile`) | declined (per-file `cur` reset) |
| `device:name = A` then `device { name = B }` | 2 | renames `A` to `B` (one block) | declined as a rename |
| continuation whose `\` is followed by CRLF | 1 | keeps the literal backslash (`kb_model = "pc1\"`) | declined |

Consequence: the reference's `unsupported` set is **larger than the host's ambiguity set**. Three of these are
worth naming because the contract's own prose is wrong about them: the "first value must be the key" path does not
leave the parser without a device — it leaves it on a category named `0` (flat form) or renames the block (block-first
form) — and the per-file category reset does not exist in `parseFile`. These do not change any printed expectation
(the reference prints `NOT_COMPARED`), so they cost coverage, not correctness. `parseFile` clears the
category stack at end of file only (`fetch/hyprlang-config.cpp:1044`), which is why the carry-over class above is
decidable.

## 5. What this means for C1 and C2 (routed; I did not touch the frozen counters)

* **C1, clause g.** The registration already declares this residual: "clause g's oracle is the reference, so a
  contract error shared by reference and tool is invisible to it". This run quantifies it for config *parsing*: on a
  corpus the reference fully models, its disagreement rate with the host parser is **0.22 %** (34/15,215), in two
  mechanisms. `fixturescan.py` (read-only) checks the frozen 90 for both preconditions and finds none of either
  (`evidence/fixturescan.txt`), so the counter's verdict is unaffected — but a tool that implements the
  reference faithfully will emit a false `DIFFER`/exit 1 on a config with a typo'd device key after a bracket line,
  and a false `scroll_factor=0.00` on a sub-`2**-150` scroll factor. That is the honest statement of the contract's
  reach, and it is the L1's call whether to note it in the registration's residual or in the tool docstring.
* **C2.** The entry sentence "the device block whose name equals the keyboard's name when that block SETS the key"
  is exactly what B1 falsifies for a file that has an unregistered key after a bracket/selector line: the *value*
  then comes from a different block. If the entry describes how a `device` block becomes the keyboard's rules, the
  two selection states (`currentSpecialKey` vs `currentSpecialCategory`, `fetch/hyprlang-config.cpp:297`, `:376`,
  `:438`, `:896`) are the sourced detail that makes that sentence true; the counter's clause j only binds
  locator+keyword, so this is a content note for the entry author, not a gate.

## 6. Out-of-scope messages received at this seat (recorded, not acted on)

Two peer notes about the frozen C1 counter's sandbox arrived while this seat ran (from `SentTool` and
`ConnCrossClaim-3`): clause r can be bypassed by absolute-path execs and by the selftest's `PATH`, and `--ro-bind / /`
does not block `AF_UNIX` to the live compositor socket; both are in `.ufo/waves/round-46/w1/SentTool/findings.md`
(F1, F2). This seat neither edits nor scores the counters; the notes belong to the L1 / the counter author.

## 7. Reproduction

```sh
S=/fast/scratch/hyaku/mado-r46/<seat>            # anything outside the lane
D=/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-46/w1/ExecHyprlangOracle
g++ -std=c++23 -O2 -o "$S/oracle" "$D/oracle.cpp" -lhyprlang
cd "$D"                                            # gen.py, differ.py, repro.py, hostcheck.py import the reference
python3 differ.py "$S/c1" "$S/oracle" 8000 800 46   # corpus + comparison + results.json
python3 repro.py  "$S/r1" "$S/oracle"               # A/B/C receipts
python3 attribute.py "$S/a1" "$S/oracle" 46 8000 800
python3 hostcheck.py "$S/h1" "$S/oracle"            # live host cross-check
python3 verify_quotes.py                            # every quote in this report, by line number
```

## 8. Tooling, host safety, evidence

No tool was installed; no `pacman`, no package transaction, no compositor mutation, no input injection, no Wayland
client. Compositor reads used: `hyprctl version` (recorded in `evidence/build.txt`) — no `devices`/`monitors` dump was
needed for this seat. Reads only: the pinned `fetch/` files, `~/.config/hypr/input.conf`, the lane's own live receipt.
Build: `g++ (GCC) 16.2.1 20260810`, `-std=c++23 -O2 -lhyprlang`, linked against `/usr/lib/libhyprlang.so.0.6.8`
with `/usr/include/hyprlang.hpp` (`evidence/build.txt`).

| evidence | what it is |
|---|---|
| `evidence/build.txt` | compiler, soname, header, `hyprctl version` |
| `evidence/corpus-8800-seed46.json`, `-4400-seed7.json`, `-3200-seed46.json` | per-corpus totals, per-tag unsupported, divergence detail with trigger tags |
| `evidence/run-*.txt` | the printed summary of each corpus run |
| `evidence/attribute.txt` | B1/B2/unexplained attribution per corpus (0 unexplained) |
| `evidence/repro.txt`, `repro.json` | A1–A9 divergence repros, B1–B14 declined classes, the 38-literal float matrix |
| `evidence/forms.txt` | form coverage inside the 8,008 comparable cases |
| `evidence/fixturescan.txt` | read-only scan of the frozen 90 fixtures for both mechanisms (0 and 0) |
| `evidence/hostcheck.txt` | 14/14 live-host devices agree |
| `evidence/locators.txt` | `grep -n` for every cited source line |
| `evidence/quotes-verified.txt` | 17/17 quotes verified against the cited line |

Source hashes (sha256, this seat dir):

```
079a8d228e15655f47a822fa9a92bf80a130bc53751482762e3a67368e3a40b4  oracle.cpp
321d7051cca59c02e9f17658b4e7d3682a9a521aca48b4835c63c9b015e8f4f7  gen.py
347f360a38e092d479f3d8ee455c47f53f3c2f10f43421207684fc423ae9d987  differ.py
558c4adfc70acecb25881918f1abd1ddbe0ebe8b3c4e1405aa96eee952ae9ad1  repro.py
af33fe61eb093787d1a7d1ae3b4cf048731d2ca62cb211a99a8fb07b84514516  hostcheck.py
6736b8fde5fc84bb2de4c9d27a6244e965c649ae0734e87d5e00baa38e3488cc  attribute.py
64802adde1882a980467bac3c4ad70a004c4e60fb3d9a77fe07095f416b93b34  verify_quotes.py
ea54276abee6e20171e5a4dcd27632726a7ec4389fe47990dc7c1cecd9deaab4  fixturescan.py
```

## Appendix A — `oracle.cpp` (the true oracle; build: `g++ -std=c++23 -O2 -o oracle oracle.cpp -lhyprlang`)

```
// mado r46 / ExecHyprlangOracle - TRUE oracle for the C1 contract against the host's hyprlang 0.6.8.
//
// Registers exactly what Hyprland 0.56.2 registers for the input-device plane
// (fetch/Hyprland-ConfigManager.cpp:518-565 for the `device` special category,
// fetch/Hyprland-ConfigValues.cpp:271-276 for the input:kb_* globals), parses config files with the real
// libhyprlang.so, and prints what Hyprland's accessors would return:
//   getConfigValueSafeDevice / getDeviceString / deviceConfigExplicitlySet (fetch/Hyprland-ConfigManager.cpp:1115-1201)
//   InputManager.cpp:1379-1381 for the pointer scroll factor (clamp 0..100 when explicitly set, else -1)
//   InputManager.cpp:1227-1233 for the six keyboard strings.
//
// Build: g++ -std=c++23 -O2 -o oracle oracle.cpp -lhyprlang
// Input: a manifest (see gen.py). Output: one JSON object per queried device name, plus the device
// special-category keys in creation order and the parse-error count, per case.

#include <hyprlang.hpp>

#include <algorithm>
#include <any>
#include <cmath>
#include <cstdint>
#include <cstdio>
#include <cstring>
#include <fstream>
#include <iostream>
#include <sstream>
#include <string>
#include <vector>

using namespace Hyprlang;

static const char* EMPTY = "[[EMPTY]]";

// ---- Hyprland's accessors, transcribed 1:1 (fetch/Hyprland-ConfigManager.cpp:1115-1201) ----
static CConfigValue* safeDevice(CConfig& c, const std::string& dev, const std::string& val, const std::string& fallback) {
    CConfigValue* VAL = c.getSpecialConfigValuePtr("device", val.c_str(), dev.c_str());
    if ((!VAL || !VAL->m_bSetByUser) && !fallback.empty())
        return c.getConfigValuePtr(fallback.c_str());
    return VAL;
}

static std::string deviceString(CConfig& c, const std::string& dev, const std::string& val, const std::string& fallback) {
    CConfigValue* val2 = safeDevice(c, dev, val, fallback);
    if (!val2)
        return "";
    std::string s{std::any_cast<STRING>(val2->getValue())};
    if (s == EMPTY)
        return "";
    return s;
}

static bool explicitlySet(CConfig& c, const std::string& dev, const std::string& val) {
    CConfigValue* VAL = c.getSpecialConfigValuePtr("device", val.c_str(), dev.c_str());
    return VAL && VAL->m_bSetByUser;
}

static float deviceFloat(CConfig& c, const std::string& dev, const std::string& val, const std::string& fallback) {
    CConfigValue* v = safeDevice(c, dev, val, fallback);
    if (!v)
        return 0.F;
    return std::any_cast<FLOAT>(v->getValue());
}

// ---- registration: fetch/Hyprland-ConfigManager.cpp:518-565 + fetch/Hyprland-ConfigValues.cpp:271-276 ----
static void registerAll(CConfig& c) {
    // device special category: key "name", 47 values
    c.addSpecialCategory("device", SSpecialCategoryOptions{.key = "name"});
    c.addSpecialConfigValue("device", "sensitivity", CConfigValue(FLOAT{0.F}));
    c.addSpecialConfigValue("device", "accel_profile", CConfigValue(STRING{EMPTY}));
    c.addSpecialConfigValue("device", "rotation", CConfigValue(INT{0}));
    c.addSpecialConfigValue("device", "kb_file", CConfigValue(STRING{EMPTY}));
    c.addSpecialConfigValue("device", "kb_layout", CConfigValue(STRING{"us"}));
    c.addSpecialConfigValue("device", "kb_variant", CConfigValue(STRING{EMPTY}));
    c.addSpecialConfigValue("device", "kb_options", CConfigValue(STRING{EMPTY}));
    c.addSpecialConfigValue("device", "kb_rules", CConfigValue(STRING{EMPTY}));
    c.addSpecialConfigValue("device", "kb_model", CConfigValue(STRING{EMPTY}));
    c.addSpecialConfigValue("device", "repeat_rate", CConfigValue(INT{25}));
    c.addSpecialConfigValue("device", "repeat_delay", CConfigValue(INT{600}));
    c.addSpecialConfigValue("device", "natural_scroll", CConfigValue(INT{0}));
    c.addSpecialConfigValue("device", "tap_button_map", CConfigValue(STRING{EMPTY}));
    c.addSpecialConfigValue("device", "numlock_by_default", CConfigValue(INT{0}));
    c.addSpecialConfigValue("device", "resolve_binds_by_sym", CConfigValue(INT{0}));
    c.addSpecialConfigValue("device", "disable_while_typing", CConfigValue(INT{1}));
    c.addSpecialConfigValue("device", "clickfinger_behavior", CConfigValue(INT{0}));
    c.addSpecialConfigValue("device", "middle_button_emulation", CConfigValue(INT{0}));
    c.addSpecialConfigValue("device", "tap-to-click", CConfigValue(INT{1}));
    c.addSpecialConfigValue("device", "tap-and-drag", CConfigValue(INT{1}));
    c.addSpecialConfigValue("device", "drag_lock", CConfigValue(INT{0}));
    c.addSpecialConfigValue("device", "left_handed", CConfigValue(INT{0}));
    c.addSpecialConfigValue("device", "scroll_method", CConfigValue(STRING{EMPTY}));
    c.addSpecialConfigValue("device", "scroll_button", CConfigValue(INT{0}));
    c.addSpecialConfigValue("device", "scroll_button_lock", CConfigValue(INT{0}));
    c.addSpecialConfigValue("device", "scroll_points", CConfigValue(STRING{EMPTY}));
    c.addSpecialConfigValue("device", "scroll_factor", CConfigValue(FLOAT{-1.F}));
    c.addSpecialConfigValue("device", "transform", CConfigValue(INT{-1}));
    c.addSpecialConfigValue("device", "output", CConfigValue(STRING{EMPTY}));
    c.addSpecialConfigValue("device", "enabled", CConfigValue(INT{1}));
    c.addSpecialConfigValue("device", "region_position", CConfigValue(VEC2{0, 0}));
    c.addSpecialConfigValue("device", "absolute_region_position", CConfigValue(INT{0}));
    c.addSpecialConfigValue("device", "region_size", CConfigValue(VEC2{0, 0}));
    c.addSpecialConfigValue("device", "relative_input", CConfigValue(INT{0}));
    c.addSpecialConfigValue("device", "active_area_position", CConfigValue(VEC2{0, 0}));
    c.addSpecialConfigValue("device", "active_area_size", CConfigValue(VEC2{0, 0}));
    c.addSpecialConfigValue("device", "flip_x", CConfigValue(INT{0}));
    c.addSpecialConfigValue("device", "flip_y", CConfigValue(INT{0}));
    c.addSpecialConfigValue("device", "drag_3fg", CConfigValue(INT{0}));
    c.addSpecialConfigValue("device", "keybinds", CConfigValue(INT{1}));
    c.addSpecialConfigValue("device", "share_states", CConfigValue(INT{0}));
    c.addSpecialConfigValue("device", "release_pressed_on_close", CConfigValue(INT{0}));
    c.addSpecialConfigValue("device", "tags", CConfigValue(STRING{EMPTY}));
    c.addSpecialConfigValue("device", "eraser_button_mode", CConfigValue(INT{0}));
    c.addSpecialConfigValue("device", "eraser_button_override", CConfigValue(INT{0}));
    c.addSpecialConfigValue("device", "pressure_range_min", CConfigValue(FLOAT{-1.0}));
    c.addSpecialConfigValue("device", "pressure_range_max", CConfigValue(FLOAT{-1.0}));

    // globals Hyprland registers (fetch/Hyprland-ConfigValues.cpp:271-276 and neighbours the plane touches)
    c.addConfigValue("input:kb_model", CConfigValue(STRING{EMPTY}));
    c.addConfigValue("input:kb_layout", CConfigValue(STRING{"us"}));
    c.addConfigValue("input:kb_variant", CConfigValue(STRING{EMPTY}));
    c.addConfigValue("input:kb_options", CConfigValue(STRING{EMPTY}));
    c.addConfigValue("input:kb_rules", CConfigValue(STRING{EMPTY}));
    c.addConfigValue("input:kb_file", CConfigValue(STRING{EMPTY}));
    c.addConfigValue("input:scroll_factor", CConfigValue(FLOAT{1.F}));
    c.addConfigValue("input:touchpad:scroll_factor", CConfigValue(FLOAT{1.F}));
    c.addConfigValue("input:touchpad:natural_scroll", CConfigValue(INT{0}));
    c.addConfigValue("input:touchpad:tap-to-click", CConfigValue(INT{1}));
    c.addConfigValue("input:touchpad:disable_while_typing", CConfigValue(INT{1}));
    c.addConfigValue("input:touchpad:clickfinger_behavior", CConfigValue(INT{0}));
    c.addConfigValue("input:natural_scroll", CConfigValue(INT{0}));
    c.addConfigValue("input:sensitivity", CConfigValue(FLOAT{0.F}));
    c.addConfigValue("input:accel_profile", CConfigValue(STRING{EMPTY}));
    c.addConfigValue("input:repeat_rate", CConfigValue(INT{25}));
    c.addConfigValue("input:repeat_delay", CConfigValue(INT{600}));
    c.addConfigValue("input:left_handed", CConfigValue(INT{0}));
    c.addConfigValue("input:numlock_by_default", CConfigValue(INT{0}));
    c.addConfigValue("input:resolve_binds_by_sym", CConfigValue(INT{0}));
}

// ---- JSON string escaping (bytes pass through; controls escaped) ----
static std::string jstr(const std::string& s) {
    std::string o = "\"";
    for (unsigned char ch : s) {
        switch (ch) {
            case '"': o += "\\\""; break;
            case '\\': o += "\\\\"; break;
            case '\n': o += "\\n"; break;
            case '\r': o += "\\r"; break;
            case '\t': o += "\\t"; break;
            default:
                if (ch < 0x20) {
                    char b[8];
                    std::snprintf(b, sizeof b, "\\u%04x", ch);
                    o += b;
                } else
                    o += static_cast<char>(ch);
        }
    }
    o += "\"";
    return o;
}

static void emitName(CConfig& cfg, const std::string& nm) {
    static const char* KEY[5] = {"kb_layout", "kb_variant", "kb_options", "kb_model", "kb_rules"};
    static const char* FB[5]  = {"input:kb_layout", "input:kb_variant", "input:kb_options", "input:kb_model", "input:kb_rules"};
    std::string        v[5];
    for (int i = 0; i < 5; ++i)
        v[i] = deviceString(cfg, nm, KEY[i], FB[i]);
    const std::string kbf = deviceString(cfg, nm, "kb_file", "input:kb_file");
    const bool        sset = explicitlySet(cfg, nm, "scroll_factor");
    double            raw = 0.0, exp = -1.0;
    if (sset) {
        const float f = deviceFloat(cfg, nm, "scroll_factor", "input:scroll_factor");
        raw           = static_cast<double>(f);
        exp           = static_cast<double>(std::clamp(f, 0.F, 100.F));
    }
    const bool block = cfg.specialCategoryExistsForKey("device", nm.c_str());
    // printed exactly as HyprCtl does (fetch/Hyprland-HyprCtl.cpp:770 "{:.2f}"), so -0.0 stays "-0.00"
    char sf[64], sfr[64];
    std::snprintf(sf, sizeof sf, "%.2f", static_cast<double>(exp));
    std::snprintf(sfr, sizeof sfr, "%.9g", static_cast<double>(raw));
    std::printf("{\"name\":%s,\"block\":%s,\"layout\":%s,\"variant\":%s,\"options\":%s,\"model\":%s,\"rules\":%s,"
                "\"kb_file\":%s,\"kb_file_set\":%s,\"sf_set\":%s,\"sf\":%s,\"sf_raw\":%s}\n",
                jstr(nm).c_str(), block ? "true" : "false", jstr(v[0]).c_str(), jstr(v[1]).c_str(), jstr(v[2]).c_str(),
                jstr(v[3]).c_str(), jstr(v[4]).c_str(), jstr(kbf).c_str(), kbf.empty() ? "false" : "true",
                sset ? "true" : "false", jstr(sf).c_str(), jstr(sfr).c_str());
}

static void runCase(const std::string& id, const std::vector<std::string>& files, const std::vector<std::string>& names) {
    SConfigOptions opts{};
    opts.allowMissingConfig = 1;
    CConfig cfg("/nonexistent-mado-oracle-root.conf", opts);
    registerAll(cfg);
    cfg.commence();

    int errors = 0;
    for (const auto& f : files) {
        auto res = cfg.parseFile(f.c_str());
        if (res.error)
            ++errors;
    }

    std::printf("BEGIN %s\n", id.c_str());
    for (const auto& nm : names)
        emitName(cfg, nm);
    const auto KEYS = cfg.listKeysForSpecialCategory("device");
    std::string cats = "[";
    for (size_t i = 0; i < KEYS.size(); ++i) {
        if (i)
            cats += ",";
        cats += jstr(KEYS[i]);
    }
    cats += "]";
    std::printf("{\"categories\":%s,\"errors\":%d}\n", cats.c_str(), errors);
    std::printf("END %s\n", id.c_str());
}

int main(int argc, char** argv) {
    std::string manifest;
    for (int i = 1; i + 1 < argc; i += 2) {
        if (std::strcmp(argv[i], "--manifest") == 0)
            manifest = argv[i + 1];
    }
    if (manifest.empty()) {
        std::fprintf(stderr, "usage: oracle --manifest PATH\n");
        return 2;
    }
    std::ifstream mf(manifest);
    if (!mf.good()) {
        std::fprintf(stderr, "manifest unreadable: %s\n", manifest.c_str());
        return 2;
    }
    std::string line;
    while (std::getline(mf, line)) {
        if (line.rfind("CASE ", 0) != 0)
            continue;
        std::istringstream ss(line);
        std::string        tag, id;
        size_t             nf = 0, nn = 0;
        ss >> tag >> id >> nf >> nn;
        std::vector<std::string> files(nf), names(nn);
        for (auto& f : files)
            std::getline(mf, f);
        for (auto& n : names)
            std::getline(mf, n);
        runCase(id, files, names);
    }
    return 0;
}
```

## Appendix B — `gen.py` (the generator)

```
#!/usr/bin/env python3
"""Random config generator for the round-46 C1 contract differential test (ExecHyprlangOracle).

Two grammars:
  clean - the forms the reference (`l1-draft/mado-devices.py`) models without counting `unsupported`:
          flat `input:kb_*`, `input { ... }` (a nested touchpad, a deeper wrapper), `device { name = X ... }`,
          `device[X] { ... }`, `device[X]:k = v`, one `device:name = X` selector per case, merges and duplicate
          names, `[[EMPTY]]`, empty RHS, unknown keys, nesting, `#`/`##` comments, backslash continuations, CRLF,
          blank/noise lines, an unclosed category at EOF.
  raw   - clean pieces plus exactly one piece from a tag list of forms the reference counts `unsupported`
          (directives, `$`, `{{ }}`, interior backslash, a selector-less `device:k`, a block whose first key is
          not `name`, a rename, inf/nan/hex/subnormal scroll factors, and a flat `device:k` after a bracket line or
          after a file that ended with an unclosed device block). One tag per case makes the attribution exact.

Devices are just names: the oracle is queried by name, the same way `expected_names` is.
Pieces are kept whole when the case is split into 1-3 files, so structure stays balanced.
"""
import random

DEV_KEYS = ("kb_layout", "kb_variant", "kb_options", "kb_model", "kb_rules", "kb_file", "scroll_factor")
IRRELEVANT = ("sensitivity", "natural_scroll", "tap-to-click", "accel_profile", "rotation", "enabled", "unknown_key")

VALUES = {
    "kb_layout": ["us", "de", "br", "fr", "us,de", "dvorak", "", "[[EMPTY]]", " gb", "ca", "de,us,fr", "x y"],
    "kb_variant": ["intl", "azerty", "", "[[EMPTY]]", "nodeadkeys", "intl,azerty"],
    "kb_options": ["compose:caps", "grp:alts_toggle", "compose:caps,grp:alts_toggle", "", "[[EMPTY]]", "a##b", "x # y",
                   "caps:escape#tail"],
    "kb_model": ["pc105", "pc104", "", "[[EMPTY]]", "microsoft"],
    "kb_rules": ["evdev", "base", "", "[[EMPTY]]", "xorg"],
    "kb_file": ["~/x.xkb", "/tmp/none.xkb", "", "[[EMPTY]]", "relative.xkb"],
}
SF = ["0.5", "2", "-3", "250", "0", "100", "1e2", "0.7x", "  4 ", ".5", "5.", "1e-1", "+2.5", "0.005", "100.005",
      "99.999", "-0", "00012", "2.675", "1.005", "0.495", "-0.0", "1e0", "1E+2", "3.0e-2", "100.0049999",
      "1.2345678901234567890", "50.555", "0.015", "12x34", "0.1e1"]
FX_SPECIAL = ["inf", "-inf", "nan", "0x10", "0X1p3", "1e-40", "1e-45", "5e-39", "1.1754943508222875e-38",
              "1.1754943e-38", "1e999", "-1e999", "1e-999", "  inf  ", "+nan"]
NAMES = ["kbd", "kbd2", "Kbd", "razer-deathadder", "Razer DeathAdder", "hl-virtual-keyboard-fcitx5", "mouse",
         "touchpad-1", "x,y", "", "k b", "k.b", "hl-virtual-keyboard", "kbd-1"]
COMMENTS = ["# note", "#", "# a##b", "# x # y", "  # tail"]
NOISE = ["", "   ", "}\t", "garbage", "=", "device", "\t"]
RAWTAGS = ("directive", "variable", "expression", "backslash", "flat-no-selector", "block-first-not-name", "rename",
           "float-special", "bracket-then-flat", "crossfile-unclosed", "selector-then-block",
           "crlf-continuation")


def name_pool(rng, k):
    return rng.sample(NAMES, k)


def dev_pairs(rng, n):
    out = []
    for _ in range(n):
        if rng.random() < 0.25:
            key = rng.choice(IRRELEVANT)
            val = rng.choice(["1", "0", "2", "adaptive", "[[EMPTY]]", ""])
        else:
            key = rng.choice(DEV_KEYS)
            val = rng.choice(SF if key == "scroll_factor" else VALUES[key])
        out.append((key, val))
    return out


def stmt_input_block(rng, deep=False):
    lines = ["input {"]
    for _ in range(rng.randrange(0, 4)):
        k = rng.choice(["kb_layout", "kb_variant", "kb_options", "kb_model", "kb_rules", "kb_file"])
        lines.append("  %s = %s" % (k, rng.choice(VALUES[k])))
    if rng.random() < 0.4:
        lines += ["  touchpad {", "    scroll_factor = %s" % rng.choice(["0.4", "1", "2", "-1"]), "  }"]
    lines.append("}")
    if deep:
        return ["general {"] + ["  " + l for l in lines] + ["}"]
    return lines


def stmt_device_block(rng, name):
    lines = ["device {", "  name = %s" % name]
    for k, v in dev_pairs(rng, rng.randrange(0, 5)):
        lines.append("  %s = %s" % (k, v))
    if rng.random() < 0.15:
        lines += ["  nested {", "    kb_layout = de", "  }"]
    lines.append("}")
    return lines


def stmt_bracket_block(rng, name):
    lines = ["device[%s] {" % name]
    for k, v in dev_pairs(rng, rng.randrange(0, 4)):
        lines.append("  %s = %s" % (k, v))
    lines.append("}")
    return lines


def stmt_bracket_flat(rng, name):
    return ["device[%s]:%s = %s" % (name, k, v) for k, v in dev_pairs(rng, rng.randrange(1, 4))]


def stmt_selector(rng, name):
    out = ["device:name = %s" % name]
    for k, v in dev_pairs(rng, rng.randrange(0, 3)):
        out.append("device:%s = %s" % (k, v))
    return out


def stmt_flat_global(rng):
    k = rng.choice(["kb_layout", "kb_variant", "kb_options", "kb_model", "kb_rules", "kb_file"])
    if rng.random() < 0.15:
        return ["input:%s[%s] = %s" % (k, rng.choice(["g1", "x", ""]), rng.choice(VALUES[k]))]
    return ["input:%s = %s" % (k, rng.choice(VALUES[k]))]


def clean_piece(rng, names, allow_selector=True):
    r = rng.random()
    if r < 0.20:
        return stmt_flat_global(rng)
    if r < 0.38:
        return stmt_input_block(rng, deep=rng.random() < 0.2)
    if r < 0.62:
        return stmt_device_block(rng, rng.choice(names))
    if r < 0.74:
        return stmt_bracket_block(rng, rng.choice(names))
    if r < 0.88:
        return stmt_bracket_flat(rng, rng.choice(names))
    return stmt_device_block(rng, rng.choice(names))


def raw_piece(rng, names, tag):
    n = rng.choice(names) or "k"
    if tag == "directive":
        return ["# hyprlang if SOMEVAR"] + stmt_flat_global(rng) + ["# hyprlang endif"]
    if tag == "variable":
        return ["$lay = de", "input:kb_layout = $lay"]
    if tag == "expression":
        return ["input:kb_layout = {{ 1 + 2 }}"]
    if tag == "backslash":
        return ["input:kb_options = a\\{b"]
    if tag == "flat-no-selector":
        return ["device:kb_layout = de", "device:kb_file = /x"]
    if tag == "block-first-not-name":
        return ["device {", "  kb_layout = de", "  name = %s" % n, "}"]
    if tag == "rename":
        return ["device {", "  name = a", "  name = %s" % n, "  kb_layout = de", "}"]
    if tag == "float-special":
        return ["device[%s]:scroll_factor = %s" % (n, rng.choice(FX_SPECIAL))]
    if tag == "bracket-then-flat":
        return ["device[%s]:kb_layout = fr" % n, "device:kb_file = /x"]
    if tag == "crlf-continuation":
        return ["input:kb_model = pc1\\", "05"]
    if tag == "selector-then-block":
        return ["device:name = %s" % n, "device {", "  name = %s" % (rng.choice(names) or "k"), "  kb_layout = de", "}"]
    return ["device {", "  name = %s" % n, "  kb_layout = de"]  # crossfile-unclosed


def decorate(rng, lines, crlf=False):
    out = []
    for ln in lines:
        if ln and rng.random() < 0.30:
            ln = ln + " " + rng.choice(COMMENTS)
        if "=" in ln and len(ln) > 2 and not crlf and rng.random() < 0.12 and not ln.endswith("\\"):
            i = rng.randrange(1, len(ln))
            out.append(ln[:i] + "\\")
            out.append(ln[i:])
            continue
        out.append(ln)
    return out


def split_pieces(rng, pieces, nfiles):
    if nfiles <= 1 or len(pieces) < nfiles:
        return [pieces]
    cuts = sorted(rng.sample(range(1, len(pieces)), nfiles - 1))
    out, prev = [], 0
    for c in cuts:
        out.append(pieces[prev:c])
        prev = c
    out.append(pieces[prev:])
    return out


def build_case(rng, cid, raw):
    names = name_pool(rng, rng.randrange(2, 7))
    tag = rng.choice(RAWTAGS) if raw else None
    pieces = []
    for _ in range(rng.randrange(1, 7)):
        if rng.random() < 0.10:
            pieces.append([rng.choice(NOISE)])
        pieces.append(clean_piece(rng, names))
    special = rng.random()
    if not raw and special < 0.10:
        pieces.append(["device {", "  name = %s" % rng.choice(names), "  kb_layout = de"])
    elif not raw and special < 0.22:
        # a top-level `device:name = X` selector, last, so no later block renames it
        pieces.append(stmt_selector(rng, rng.choice(names)))
    nfiles = 1 if (raw and tag == "crossfile-unclosed") else rng.choices([1, 2, 3], weights=[6, 3, 1])[0]
    groups = split_pieces(rng, pieces, nfiles)
    if raw:
        if tag == "crossfile-unclosed":
            # file 0 keeps an unclosed device block, file 1 opens with a selector-less `device:k`
            groups = [groups[0] + [["device {", "  name = %s" % (rng.choice(names) or "k"), "  kb_layout = de"]],
                      [["device:kb_file = /x"]]]
        else:
            groups = groups + [[raw_piece(rng, names, tag)]]
    crlf = rng.random() < 0.2 or tag == "crlf-continuation"
    eol = "\r\n" if crlf else "\n"
    files = []
    for g in groups:
        lines = []
        for p in g:
            lines += p
        lines = decorate(rng, lines, crlf)
        files.append(eol.join(lines) + (eol if lines else ""))
    query = list(dict.fromkeys(names + [n for n in NAMES if n][:0] + rng.sample([n for n in NAMES if n], 2)))
    return {"id": cid, "files": files, "names": query, "tag": tag}


def generate(seed=46, n_clean=3200, n_raw=400):
    rng = random.Random(seed)
    cases = []
    for i in range(n_clean):
        cases.append(build_case(rng, "c%05d" % i, False))
    for i in range(n_raw):
        cases.append(build_case(rng, "r%05d" % i, True))
    return cases
```

## Appendix C — the other tools in this seat dir

`differ.py` — writes the corpus, runs the oracle once over a manifest, models the same configs with the reference
in-process (`parse_config` / `expected_names` / `State.devices`), compares the five names, `kb_file`, the two-decimal
scroll factor, block presence and the category order, then writes `results.json`.

`repro.py` — the hand-written receipts: section A the divergence repros (A1–A9), section B the declined classes
(B1–B14) with the host's answer, section C the 38-literal `scroll_factor` matrix against `read_float`.

`attribute.py` — re-derives the B1/B2/unexplained split over a corpus (used for the section 2 table).

`hostcheck.py` — joins the lane's live receipt with an oracle run on `~/.config/hypr/input.conf` (14/14 AGREE).

`verify_quotes.py` — asserts every quote in this report against its cited line number (17/17).

`fixturescan.py` — read-only scan of the frozen 90 fixtures for the B1/B2 preconditions (0 and 0).

All six scripts read the reference from `.ufo/waves/round-46/l1-draft/mado-devices.py` and the pins from
`.ufo/waves/round-46/fetch/`; the only files they write are `results.json` / `repro.json` next to themselves.
