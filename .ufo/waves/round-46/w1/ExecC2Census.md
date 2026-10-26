# ExecC2Census — C2 census / surfaces / Gate quotes re-derived from the pins

Seat: ExecC2Census (mado round 46, w1). Lane: /home/vgpnk/Projects/shokunin/mado-shokunin.
Claim attacked: **C2 coverage (sourced)** — entry `corpus/knowledge/hyprland-input-devices-r46.md`,
L1 draft `.ufo/waves/round-46/l1-draft/entry.md`, frozen counter
`quality/counters/c2-r46-input-device-entry.py` (PRED-C2-r46, clauses a–j).
Frozen base b22ea56bff2faec39ce9ff75d2107eaf4612ecbe, freeze commit 8c5434c60e03f147ee1f75ab195e8bc3f0db4dec.

Method: every value below was recomputed by my own script (`w1/ExecC2Census/check.py`, run with
`python3 check.py`, output `w1/ExecC2Census/independent-derivation.txt`) directly over the ten pins in
`.ufo/waves/round-46/fetch/`. The frozen counter was **not** used for the derivation; it was used only
afterwards, once, on a positive control and once on a two-defect mutant (below).

**Headline.** Census line reproduced exactly (6/6 fields). All 28 SURFACES anchors occur exactly once,
are cited on a keyword line with a locator of ≤ 30 lines that contains the anchor. All 10 Gate QUOTES
occur exactly once (whitespace-normalised, comments stripped) at the line number the entry's OBS
locator names. Positive control: `admitted=1/1 verdict=TARGET_MET`. **Two prose defects exist that the
frozen clause j cannot see** (D1, D2) — receipts prove the counter admits the entry with both defects
injected.

## 1. Census line: independent derivation vs the frozen line

| field | value | independent witness (grep/awk on the pin) |
|---|---|---|
| `default_layout` | `us` | `Hyprland-ConfigValues.cpp:272` `MS<String>("input:kb_layout", "Appropriate XKB keymap parameter", "us",` — third argument |
| `fallback_layout` | `us` | `Hyprland-IKeyboard.cpp:113` `m_currentRules.layout  = "us";` (unique assignment to `m_currentRules.layout` in the pin); corroborating second fallback `Hyprland-IKeyboard.cpp:256-259` `fallback to us` → `rules.layout = "us";` |
| `device_keys` | `47` | `grep -c 'm_config->addSpecialConfigValue("device", "'` = 47, and 47 **unique** key names; first `Hyprland-ConfigManager.cpp:519` `sensitivity`, last `:565` `pressure_range_max` |
| `scroll_factor_max` | `100` | `Hyprland-InputManager.cpp:1380` `..., 0.F, 100.F);` |
| `json_scroll_decimals` | `2` | `Hyprland-HyprCtl.cpp:770` `"scrollFactor": {:.2f}` |
| `virtual_prefix` | `hl-virtual-keyboard` | `Hyprland-protocols-VirtualKeyboard.cpp:12` `std::string name = "hl-virtual-keyboard";` (unique in the pin) |

Derived line (`independent-derivation.txt:9`) is byte-identical to the frozen line at `entry.md:53`:

```
hyprland input-device default_layout=us fallback_layout=us device_keys=47 scroll_factor_max=100 json_scroll_decimals=2 virtual_prefix=hl-virtual-keyboard
```

`FROZEN_MATCH : True` (`independent-derivation.txt:10`). Pin bytes themselves match the counter's
`PINS` table: 10/10 sha256 equal (`w1/ExecC2Census/pins-sha256.txt`, e.g. InputManager
`feedf32e…4765`, hyprlang `fa1b6898…1de3e`).

Note on `fallback_layout`: two independent fallback sites both yield `us` — the failed-compile reset at
`Hyprland-IKeyboard.cpp:107-115` (zeroed `XKBRULES`, stored layout `us`) and the per-group state
fallback at `Hyprland-IKeyboard.cpp:256-259`. The census value is stable under either reading, so the
field is not ambiguous in value.

## 2. The 28 SURFACES (clause j)

For each row: anchor line = my own `grep`-equivalent count over the pin (exactly one hit, column
`anchor`), entry line = the entry line carrying the locator, span = the cited range (≤ 30 lines,
contains the anchor), and the pin line that carries the sentence's claim. Keyword-on-line also holds
for all 28 (my checker re-evaluated each item's keyword regex, `independent-derivation.txt:14-98`; every quote in
this table is re-grepped against the named pin line by `w1/ExecC2Census/verify-quotes.py`
(`quote-verification.txt`, 44/44).

| # | label | receipt | anchor | entry | span | bearing line / short quote | verdict |
|---|---|---|---|---|---|---|---|
| 1 | apply-keyboard | InputManager.cpp | 1213 | 32 | 1213-1238 | `void CInputManager::applyConfigToKeyboard(SP<IKeyboard> pKeyboard) {` | supported; six `kb_*` lookups at 1226-1231 |
| 2 | kb-layout-lookup | InputManager.cpp | 1229 | 40 | 1229 | `const auto LAYOUT   = Config::mgr()->getDeviceString(devname, "kb_layout", "input:kb_layout");` | supported |
| 3 | set-keymap | InputManager.cpp | 1286 | 33 | 1282-1295 | `pKeyboard->setKeymap(IKeyboard::SStringRuleNames{LAYOUT, MODEL, VARIANT, OPTIONS, RULES});` | supported |
| 4 | unchanged-skip | InputManager.cpp | 1274 | 32 | 1270-1280 | `Log::logger->log(Log::DEBUG, "Not applying config to keyboard, it did not change.");` then `return;` | supported |
| 5 | scroll-explicit | InputManager.cpp | 1379 | 34 | 1379-1383 | `if (Config::mgr()->deviceConfigExplicitlySet(devname, "scroll_factor"))` | supported |
| 6 | scroll-nullopt | InputManager.cpp | 1382 | 34 | 1379-1383 | `m->m_scrollFactor = std::nullopt;` | supported |
| 7 | dup-name | InputManager.cpp | 2119 | 36 | 2119-2131 | `std::string CInputManager::getNameForNewDevice(std::string internalName) {`; suffix at 2124/2127 | supported |
| 8 | device-category | ConfigManager.cpp | 518 | 31 | 518-540 | `m_config->addSpecialCategory("device", {"name"});` | **partial — D1** |
| 9 | set-by-user | ConfigManager.cpp | 1119 | 41 | 1119 | `if ((!VAL || !VAL->m_bSetByUser) && !fallback.empty())` | supported |
| 10 | config-exists | ConfigManager.cpp | 1196 | 32 | 1196-1201 | `bool CConfigManager::deviceConfigExists(const std::string& dev) {` | supported (nuance D6) |
| 11 | strval-empty | ConfigManager.cpp | 1163 | 32 | 1156-1168 | `if (VAL == STRVAL_EMPTY)` → `return "";` | supported |
| 12 | kb-layout-default | ConfigValues.cpp | 272 | 32 | 271-276 | `MS<String>("input:kb_layout", "Appropriate XKB keymap parameter", "us",` | supported; rest `STRVAL_EMPTY` at 271/273-276 |
| 13 | global-scroll-factor | ConfigValues.cpp | 296 | 34 | 290-300 | `MS<Float>("input:scroll_factor", … 1, {.min = 0, .max = 2,` | partial — D3 |
| 14 | fallback-us | IKeyboard.cpp | 113 | 33 | 101-116 | `m_currentRules.layout  = "us";` after `memset(&XKBRULES, 0, sizeof(XKBRULES));` | supported for stored/reported rules (D4) |
| 15 | keymap-overridden | IKeyboard.cpp | 61 | 35 | 60-64 | `if (m_keymapOverridden) {` → `return;` | supported |
| 16 | kb-file | IKeyboard.cpp | 87 | 33 | 87-96 | `if (!m_xkbFilePath.empty()) {` | supported |
| 17 | json-scroll | HyprCtl.cpp | 770 | 34 | 765-772 | `"scrollFactor": {:.2f}` with `value_or(-1)` at 773 | supported |
| 18 | json-layout | HyprCtl.cpp | 800 | 34 | 785-802 | `escapeJSONStrings(k->m_currentRules.layout)` | supported (rules/model/layout/variant/options at 799-800) |
| 19 | virtual-override | VirtualKeyboard.cpp | 41 | 46 | 41 | `m_keymapOverridden = true;` | supported |
| 20 | virtual-name | protocols/VirtualKeyboard.cpp | 12 | 47 | 12 | `std::string name = "hl-virtual-keyboard";` | supported (condition D5) |
| 21 | name-normalizer | MiscFunctions.cpp | 777 | 36 | 777-789 | `case ' ':` / `case '\n':` / `case ',': return '-';` + `std::tolower(ch)` | supported |
| 22 | bracket-key | hyprlang-config.cpp | 291 | 31 | 291-320 | `if (valueName.contains('[') && valueName.contains(']')) {`, key cut at 296-299 | supported |
| 23 | first-value-key | hyprlang-config.cpp | 435 | 48 | 435 | `result.setError(std::format("special category's first value must be the key. …` | supported; guard `if (VALUEIT == PCAT->values.end() \|\| VALUEIT->first != sc->key)` at 434 |
| 24 | hash-escape | hyprlang-config.cpp | 691 | 30 | 674-700 | `if (line[commentPos + 1] == '#') {` | **partial — D2** |
| 25 | continuation | hyprlang-config.cpp | 53 | 30 | 44-66 | `while (line.length() > 0 && line.at(line.length() - 1) == '\\') {` | supported |
| 26 | special-reset | hyprlang-config.cpp | 896 | 31 | 885-899 | `impl->currentSpecialKey      = "";` under `if (impl->categories.empty()) {` after `pop_back()` at 893 | supported |
| 27 | wiki-override | wiki-Keywords.md | 66 | 36 | 64-70 | "Per-device config options will overwrite your options set in the `input`" (66) | supported |
| 28 | wiki-name | wiki-Keywords.md | 79 | 36 | 79 | "The `name` can be easily obtained by checking the output of `hyprctl devices`." (79) | supported |

Counts: 28/28 anchor-unique, 28/28 cited on a keyword line inside a ≤30-line locator that contains the
anchor (`surfaces_not_ok : 0`, `independent-derivation.txt:98`). 25 rows fully supported by the cited
lines; 3 partial (D1 device-category, D2 hash-escape, D3 global-scroll-factor).

## 3. The 10 Gate QUOTES

Count = word-boundary-aware occurrences in the collapsed pin, both raw and comment-stripped; `line` =
first character's line, computed from a per-character line map, not from a file scan.

| id | receipt | occ raw / no-comment | quote line | entry OBS line | locator |
|---|---|---|---|---|---|
| S316 | InputManager.cpp | 1 / 1 | 1229 | 40 | `Hyprland-InputManager.cpp:1229` ✓ |
| S317 | ConfigManager.cpp | 1 / 1 | 1119 | 41 | `:1119` ✓ |
| S318 | ConfigValues.cpp | 1 / 1 | 272 | 42 | `:272` ✓ |
| S319 | IKeyboard.cpp | 1 / 1 | 113 | 43 | `:113` ✓ |
| S320 | HyprCtl.cpp | 1 / 1 | 769 | 44 | `:769` ✓ (quote spans 769-770; first char on 769) |
| S321 | MiscFunctions.cpp | 1 / 1 | 782 | 45 | `:782` ✓ |
| S322 | VirtualKeyboard.cpp | 1 / 1 | 41 | 46 | `:41` ✓ |
| S323 | protocols/VirtualKeyboard.cpp | 1 / 1 | 12 | 47 | `:12` ✓ |
| S324 | hyprlang-config.cpp | 1 / 1 | 435 | 48 | `:435` ✓ |
| S325 | wiki-Keywords.md | 1 / 1 | 67 | 49 | `:67` ✓ (`It's worth noting…` starts mid-line 67) |

`quotes_not_ok : 0` (`independent-derivation.txt:131`). No quote is duplicated inside its receipt, so
none of the ten Gate rows can be satisfied by a second, unrelated occurrence. Cross-pin reuse: checked
over all 10 pins — every quote is present in exactly one pin, the one its Gate row names
(`w1/ExecC2Census/cross-pin-uniqueness.txt`, 10/10 `-> True`). Clause d of the counter agrees (10/10
`gates=1 bound=1`, `counter-poscontrol.txt:11-20`).

## 4. Positive control and mutant

Positive control (recipe from the wave context, verbatim clone→checkout→build-pos→commit):

```
D=$ scratch clone of the lane at 8c5434c6…, toplevel_ok
python3 -I .ufo/waves/round-46/l1-draft/build-pos.py "$D"   -> applied
commit                                                      -> 15e7b4ec5080b34d726b18e5e30f45918933e1dd
```

`w1/ExecC2Census/counter-poscontrol.txt:59-60`:

```
clauses=a:1 b:1 c:1 d:1 e:1 f:1 g:1 h:1 i:1 j:1 admitted=1
PRED-C2-r46: admitted=1/1 verdict=TARGET_MET rev=15e7b4ec5080b34d726b18e5e30f45918933e1dd
```

The counter's 28 clause-j lines report the **same** line numbers as my independent derivation
(1213, 1229, 1286, 1274, 1379, 1382, 2119, 518, 1119, 1196, 1163, 272, 296, 113, 61, 87, 770, 800, 41,
12, 777, 291, 435, 691, 53, 896, 66, 79) — two methods, one answer.

Mutant (same control tree, two prose defects injected, locators and anchors untouched),
`w1/ExecC2Census/counter-prose-mutants.txt:38,54,59-60`:

```
clause=j surface=device-category line=518 cited=1
clause=j surface=hash-escape   line=691 cited=1
clauses=a:1 … j:1 admitted=1
PRED-C2-r46: admitted=1/1 verdict=TARGET_MET rev=4745419f43ec6f54059f0c5f4b4e81b82b020d1a
```

So clause j binds *anchor presence + keyword + locator geometry*, not the truth of the sentence — which
is exactly the hole D1 and D2 fall through.

## 5. Defects (draft-side; none blocks the counter)

**D1 — `entry.md:31`: the `47 values` count is not witnessed by its cited range.**
The sentence reads "…registers it with `name` as its key and 47 values (…, Hyprland-ConfigManager.cpp:518-540
registers the device block)". The 47 `addSpecialConfigValue("device", …)` lines span
`Hyprland-ConfigManager.cpp:519-565` (first `sensitivity` at 519, last `pressure_range_max` at 565), so
the cited 518-540 covers 22 of the 47 value registrations. The number is true (verified independently)
but the locator cannot license it; a reader following only 518-540 sees 22 values. Fix for the
integrator: extend to `518-565` (48 lines — over the 30-line locator width) or split into two locators
(`518-540` + `541-565`), or drop "47" from this sentence and keep it only in the census line.

**D2 — `entry.md:30`: the `##` rule is contradicted by the cited lines themselves.**
"A `#` starts a comment unless it is doubled: `##` is one literal `#` comment character
(hyprlang-config.cpp:674-700)." `hyprlang-config.cpp:676-681` short-circuits first: when the first `#`
is at position 0 the whole line goes to `parseComment(line.substr(1))` and never reaches the doubling
branch at 690-703; `parseComment` (567-571) only reacts to `hyprlang…`, so a line starting `##` is
still fully commented. The doubling escape is therefore a mid-line rule, and its product is one literal
`#` in the value — not a "comment character". Both facts are visible inside the cited range, so the
sentence overstates its own evidence.

**D3 — `entry.md:34`: the "never reaches the printed field" warrant and the touchpad half.**
"The global `input:scroll_factor` therefore never reaches the printed field (Hyprland-ConfigValues.cpp:290-300,
input:scroll_factor is a separate global option)". `Hyprland-ConfigValues.cpp:296` shows only that the
option exists globally; the warrant for "never" is `Hyprland-InputManager.cpp:1379-1382` (cited in the
previous sentence), where the printed value is produced only under `deviceConfigExplicitlySet`. The
clause "and neither does `input:touchpad:scroll_factor`" has no cited witness at all — the nearest is
`Hyprland-InputManager.cpp:972` / `:980-981` (`PTOUCHPADSCROLLFACTOR`), which is not cited anywhere in
the entry.

**D4 — `entry.md:33`: "falls back to layout `us`" conflates stored and effective.**
`Hyprland-IKeyboard.cpp:107` zeroes `XKBRULES` and 115 re-compiles from the zeroed struct, i.e. the
retry keymap is libxkbcommon's default, while `:113` only stores `us` in `m_currentRules` for reporting.
For the entry's purpose (why the dump prints `us`) this is correct, but as a mechanism sentence it
attributes the fallback to the layout string.

**D5 — `entry.md:35`: the virtual-keyboard name omits its condition.**
`Hyprland-protocols-VirtualKeyboard.cpp:14-16` returns the bare prefix unless
`misc:name_vk_after_proc` is set; the suffix is then `-` + the normalised client binary name (`:18-27`).
The S323 row records the condition, step 6's sentence ("named `hl-virtual-keyboard` plus its process
name") does not.

**D6 (nuance, not a defect) — `entry.md:32` vs `Hyprland-ConfigManager.cpp:1196-1201`.**
"the keyboard's exact name" is right for the config key, but the cited function first replaces spaces
with `-` in the *device* name (1197-1198) before `specialCategoryExistsForKey`. Worth one clause if the
entry is revised, because a reader may take "exact" to mean byte-equal.

**Coverage gap outside the 28 surfaces (not a clause):** the entry's FALLBACK story covers only the
setKeymap reset (101-116) and so explains "prints `us` while config says otherwise". The converse site,
`Hyprland-IKeyboard.cpp:249-259`, falls a *layout group's* keymap back to `us` while `m_currentRules`
keeps the configured names — the dump then prints the config's names although that group's keymap is
`us`. The entry's step 4 / "Reading a DIFFER" section does not mention it, and the C1 tool cannot see it
(it compares printed rules only). Bounded impact: it is a per-group state detail, not a rule-name
divergence, so no C1 verdict changes.

## 6. What this does not establish

- The XKB compile is not reproduced; all statements are about stored names and printed JSON fields
  (matches the entry's own Limits).
- I did not run the counter against the lane itself (base expectation 0/1 comes from the controls
  receipt, not from me).
- The live-host numbers (nine AGREE, one VIRTUAL, four pointers at -1.00) are the L1's
  `receipts/live-devices-host-l1.txt`, not re-run here; this seat stayed read-only on the compositor.
- Clause-level truth of clauses a–i beyond census/surfaces/quotes (registry row shape, README row,
  lesson Gate sha binding, ProseKey scan) was exercised only through the positive control run, which
  reports every clause 1.

## 7. State / hygiene

- Wrote only `mado-shokunin/.ufo/waves/round-46/w1/ExecC2Census/` (4 receipts + my checker) and this
  report. No tracked file, counter, fixture, pin, registration or index touched; no git/jj mutation in
  the lane (only read-only `git -C <scratch clone>` and `git show` via the counter).
- Scratch: `/fast/scratch/hyaku/mado-r46/ExecC2Census/` (two fixture clones, 15e7b4ec control,
  4745419f mutant) — removed before finishing; no /tmp evidence is cited.
- Tools installed/updated: **none** (python3 stdlib, git, coreutils, grep/awk only). pacman untouched.

Evidence index in `w1/ExecC2Census/`: `independent-derivation.txt` + `check.py` (census, 28 surfaces,
10 quotes), `quote-verification.txt` + `verify-quotes.py` (44 lifted fragments re-grepped against the
pins), `cross-pin-uniqueness.txt`, `pins-sha256.txt`, `counter-poscontrol.txt`,
`counter-prose-mutants.txt`.
- Compositor reads: none by this seat (no `hyprctl` call issued).
