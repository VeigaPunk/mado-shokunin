# CritEntryContent — attack on the C2 draft entry (round 46, w1)

Seat: `CritEntryContent` · lane `mado-shokunin` · 2026-10-26 · leaf, no dispatch.
Target: `.ufo/waves/round-46/l1-draft/entry.md` (71 lines, 10 source rows S316-S325, 7 steps, 10 OBS, census, live run, 4 bullets, 4 limits)
against the ten pins in `.ufo/waves/round-46/fetch/` (Hyprland `efb50993`, hyprlang `v0.6.8`, wiki `ecc06f3`).
Pin integrity first: `sha256sum -c <(awk '{print $1"  fetch/"$3}' receipts/fetch-sha256.txt)` → **10/10 OK**, so every
line number below is a line of the frozen bytes. Locators are computed, never typed: `w1/CritEntryContent/verify.py`
→ `w1/CritEntryContent/locators.txt` (66 locator rows, 10 OBS quote rows, the 47-value count, the host reads).

Verdict scale: **S** supported · **S!** supported but the citation is too narrow or the wording overstates ·
**W** wrong as written · **U** unpinned (no pin carries it).

Bottom line: the chain is broadly right and the three headline mechanisms (device-first lookup with a set-by-user
test, kb_file-then-names-then-us-fallback, normalised name as the join key) survive the attack. Three statements are
wrong as written (step 2's flat-device conclusion, step 6's virtual-keyboard name, the UNK row), one gate is
understated, four citations stop one to twenty-five lines short of what they claim, two OBS quotes
cannot be grepped at their claimed line, one literal and one forward claim have no pin, and the entry omits the two
fields of the dump that witness compilation and key ownership (`active_keymap`, `main`). None of this is caught by
PRED-C2-r46: clause j binds a locator and a keyword per surface, not the truth of the sentence — this seat is the
residual that covers it, so the L1 must fix the prose itself.

---

## 0. Headline findings, strongest counterexample first

### H1 `main` is unmentioned, and on this host it means the opposite of what a reader will assume (W)

The entry never says what `main` is, although the dump prints it for every keyboard
(`Hyprland-HyprCtl.cpp:797` `"main": {}`, value `(k->m_active ? "true" : "false")` at `801`).
The pins only ever **clear** the flag: `Hyprland-InputManager.cpp:1940` `k->m_active = false;` inside
`disableAllKeyboards(bool virt)` (`1934-1942`), called at `1193` from `setupKeyboard` with `virt = false`. The
initial value is not in the pins (it is declared in `IKeyboard.hpp`, which was not fetched — `[INFERENCE]`). Consequence, observed read-only on the
host (`hyprctl devices -j`, projected; no names):

```
cross-tab (is_virtual_keyboard, main): {(False, False): 9, (True, True): 1}
```

`main` is true **only on the fcitx5 virtual keyboard** and false on all nine physical keyboards. And
`hyprctl switchxkblayout main` selects the first keyboard with `m_active`
(`Hyprland-HyprCtl.cpp:1398-1404`), i.e. on this host the virtual keyboard. So a reader who is told nothing will
read `main: true` as "the primary hardware keyboard", which is false here. This is exactly the fact the ticket asks
for and the entry has no line about it. **Impacted surface: step 5 (T2 row), Limits.** It does not move C1 (the tool
does not compare `main`) and it does not fail C2 (no surface binds it) — it is a truth defect in the published entry.

### H2 The UNK row is wrong: the dump carries a witness of the compiled keymap (W)

Table row 5 says *"which keymap a virtual keyboard really uses | not answerable from the dump | UNK by design"*.
The dump prints `"active_keymap": "{}",` (`Hyprland-HyprCtl.cpp:794`) and `"active_layout_index": {},` (`793`), fed
from `k->getActiveLayout()` (`783`) → `IKeyboard::getActiveLayout` (`Hyprland-IKeyboard.cpp:306`) →
`xkb_keymap_layout_get_name(KEYMAP, i)` (`313`) on `KEYMAP = m_xkbKeymap`. For an overridden virtual keyboard
`m_xkbKeymap` **is** the client's keymap (`Hyprland-VirtualKeyboard.cpp:39-40` `m_xkbKeymap = xkb_keymap_ref(...)`,
then `41` `m_keymapOverridden = true;`). So `active_keymap` reports the layout name of the keymap actually
installed, not the config names. Host evidence, all ten keyboards:

```
('br', 'Portuguese (Brazil)', 0, '', '', '', 'compose:caps') x 10   # (layout, active_keymap, index, rules, model, variant, options)
```

Two facts fall out that the entry needs and does not have: (a) `layout` and `active_keymap` speak different
vocabularies (`br` vs `Portuguese (Brazil)`), so a reader who diffs them gets false DIFFERs; (b) the virtual
keyboard's `active_keymap` is a *partial* witness of its keymap (the active layout's name), so the honest row is
"the full keymap is UNK; the dump's `active_keymap` names the active layout of it". Step 6's last sentence
(*"the rules the dump prints for it are the config's names at creation, not a witness of the keymap in use"*) is
correct **about `rules`** and must stay — it is the UNK row and the omission of `active_keymap` that are wrong.

### H3 A flat `device:kb_layout = x` is a hard config error, not a silent no-op (W)

Step 2 ends: *"The current device is forgotten when the last category closes …, so a flat `device:kb_layout = x`
outside a block has no device to land on."* The reset is supported (`hyprlang-config.cpp:896-897`, inside the
`categories.empty()` branch at `895`), but the conclusion is not. With no current special category and no bracket,
`configSetValue` falls through to the dynamic-category branch (`393-441`), finds the trunk `kb_layout` inside the
`device` descriptor's defaults, creates a category, and then hits
`if (VALUEIT == PCAT->values.end() || VALUEIT->first != sc->key)` → `setError(... "special category's first value
must be the key. ...")` (`434-438`, message at `435`) and `return {true, result}`. Hyprland stores that in
`m_configErrors` (`Hyprland-ConfigManager.cpp:988`) and queues an error overlay (`988-990`). So the reader gets a
config error, not a dropped key. Two corollaries the sentence also loses: while a `device { }` block is still open,
a flat `device:kb_layout` **does** land on that block's device (via `currentSpecialCategory`,
`hyprlang-config.cpp:348-354`); and `device { name = }` with an empty value is the one way a flat key can match a
stored empty key (`372-376`). **Impacted surface: step 2.** This is the one defect a reference-tool model could
share, which clause g cannot see (declared C1 residual) — worth a C1 note, but my scope is the entry.

### H4 `hl-virtual-keyboard` naming: the gate is missing (W)

Step 6 sentence 1: *"A virtual keyboard … is named `hl-virtual-keyboard` plus its process name"*. The pin is
conditional:

```
 12    std::string name = "hl-virtual-keyboard";
 14    static auto PVKNAMEPROC = CConfigValue<Config::INTEGER>("misc:name_vk_after_proc");
 15    if (!*PVKNAMEPROC)
 16        return name;
 18    name += "-";
 24        const auto NAME     = deviceNameToInternalString(FILENAME);
 30    name += "unknown";
```

(`Hyprland-protocols-VirtualKeyboard.cpp:11-31`; default is `true`, `Hyprland-ConfigValues.cpp:487`
`Name virtual keyboards after the processes that create them.`, `true`). With `misc:name_vk_after_proc = 0` the name
is **exactly** `hl-virtual-keyboard` for every virtual keyboard — so the suffix is not "the process name" but
`"-"` + the normalised basename, or `"-unknown"`, and the tool's `virtual_prefix=hl-virtual-keyboard` test is the
only thing that still holds. A reader who cannot see the option cannot explain a bare `hl-virtual-keyboard` entry,
nor that with the option off two virtual keyboards collide and take the duplicate suffix of step 7.

### H5 Two OBS quotes cannot be grepped at their claimed line (S/U)

`locators.txt` §2 (quote grepped literally against the pin):

```
S320: claimed Hyprland-HyprCtl.cpp:769 quote-grep-hits=NONE -> NOT-ONE-LINE
S325: claimed wiki-Keywords.md:67     quote-grep-hits=NONE -> NOT-ONE-LINE
```

- S320 quotes `"defaultSpeed": {:.5f}, "scrollFactor": {:.2f}` — the pin has them on two lines (`769`, `770`).
- S325 quotes `It's worth noting that ONLY values explicitly changed will be overwritten.` — the wiki wraps it:
  `67 section. It's worth noting that ONLY values explicitly changed will be` / `68 overwritten.`
- Two more are whitespace-normalised rather than byte-exact (alignment spaces inside the pin):
  S316 `const auto LAYOUT   =` (three spaces, `Hyprland-InputManager.cpp:1229`) and S319
  `m_currentRules.layout  = "us";` (two spaces, `Hyprland-IKeyboard.cpp:113`).

The seat rule is that a quote is "verified by a script that greps your receipt"; these four fail that test as
written. Cheapest fix: quote the single pinned fragment (`"scrollFactor": {:.2f}` at 770; `ONLY values explicitly
changed will be` at 67; `getDeviceString(devname, "kb_layout", "input:kb_layout")` at 1229;
`m_currentRules.layout` + `"us"` at 113) or declare the two-line span explicitly (`67-68`, `769-770`). S317, S318,
S321-S324 are byte-exact single lines (`1119`, `272`, `782`, `41`, `12`, `435`).

### H6 Four citations stop short of the fact they carry (S!)

`locators.txt` §1, rows whose needle lands outside the claimed range:

| entry claim | cited | needle actually at | fix |
|---|---|---|---|
| step 1 `##` is one literal `#` | `hyprlang-config.cpp:674-700` | `701` (`line = line.substr(0, commentPos + 1) + line.substr(commentPos + 2);`) | cite `674-702` |
| step 2 "47 values" | `Hyprland-ConfigManager.cpp:518-540` | first value `519`, **last value `565`** (47 contiguous `addSpecialConfigValue("device", …)` calls) | cite `518-565` |
| step 2 three spellings "reach the same per-device store" | `hyprlang-config.cpp:291-320` | store write at `330` (`PCAT->values[sc->key].setFrom(CATKEY);`), override use at `342-348` | cite `291-330` |
| step 4 "kb_file … tried first", then the names | `Hyprland-IKeyboard.cpp:87-96` | names attempt at `97-99` (`if (!m_xkbKeymap)` / `xkb_keymap_new_from_names2`) | cite `87-99` |

The count itself is right: `locators.txt` §3 → `addSpecialConfigValue("device", ...) calls: 47 at
Hyprland-ConfigManager.cpp:519-565 (contiguous=True)`, matching the census `device_keys=47`. Note that the block-form
spelling `device[X] { … }` works through a mechanism the cited range cannot show: the block opener is pushed verbatim
(`hyprlang-config.cpp:908` `impl->categories.push_back(line);`), and the bracket is then cut out of the **composed**
value name (`292-299`), so `device[X]:kb_layout` and `device[X] { kb_layout = … }` take the same path. Both bracket
spellings are also absent from the wiki pin, which documents only `device {` / `name = ...` (`wiki-Keywords.md:73-74`,
example at `110-111`) — say so, or a reader will think the wiki sanctions them.

### H7 Two unpinned statements (U)

- Step 3: *"a stored `[[EMPTY]]` reads as the empty string"*. The semantics are pinned (`[[EMPTY]]` is never spelled
  in the pins): `getDeviceString` maps the value to `""` at `Hyprland-ConfigManager.cpp:1163-1164` (`if (VAL ==
  STRVAL_EMPTY)`), but `STRVAL_EMPTY` is defined outside the ten pins. The spelling is locally checkable —
  `strings /usr/bin/Hyprland | grep -c '^\[\[EMPTY\]\]$'` → `1` — which is not a pin. Either fetch the header that
  defines it and add it to `fetch/` + `fetch-sha256.txt`, or write "a sentinel (`STRVAL_EMPTY`, definition not in
  these pins)".
- Header `recheck:` (line 15): *"upstream main has moved to a Lua config, so a release past 0.56.x may drop the
  `device { }` block form"*. No pin carries this. Mark it `[INFERENCE]` or drop it; a recheck clause is exactly the
  place where an unverifiable claim ages badly.

### H8 Readers are missing these facts (list, with the line that carries each)

1. **What `main` means** — `IKeyboard::m_active`, printed at `Hyprland-HyprCtl.cpp:801`, read by
   `switchxkblayout main` at `1398-1404`, the only write to it in the pins clears it, in
   `disableAllKeyboards(false)` (`Hyprland-InputManager.cpp:1940`, called at `1193`); the initial value is not in the
   pins; host: the virtual keyboard is the sole `main`.
2. **`active_keymap` / `active_layout_index`** — the compiled witnesses (`Hyprland-HyprCtl.cpp:793-794`,
   `Hyprland-IKeyboard.cpp:306-320`); vocabulary differs from `layout` (`br` vs `Portuguese (Brazil)`).
3. **`capsLock` / `numLock`** — locked-modifier state, not the `numlock_by_default` option
   (`Hyprland-HyprCtl.cpp:795-796`, `getModState` at `751-759`); host: `numLock` true on 10/10, `capsLock` false.
4. **`address` and `defaultSpeed`** — the mouse block prints `address`, `name`, `defaultSpeed`, `scrollFactor`
   (`767-770`); `defaultSpeed` is libinput's *default* speed (`libinput_device_config_accel_get_default_speed`,
   `773`), not the configured `sensitivity`. The array is named `"mice"` (`Hyprland-HyprCtl.cpp:762`) but holds **every** pointer.
5. **The join key is `m_hlName`** — `applyConfigToKeyboard` starts from `devname = pKeyboard->m_hlName`
   (`Hyprland-InputManager.cpp:1214`), i.e. exactly the `name` the dump prints; the device lookups then compare that
   string to the block key with no normalisation (`Hyprland-ConfigManager.cpp:1117`), while `deviceConfigExists`
   additionally replaces spaces with dashes (`1197-1198`). "Exact name" in step 3 should read "exact normalised name".
6. **Duplicate blocks merge, they do not reset** — a second `device { name = X … }` finds the existing category by
   key value and overwrites only the keys it mentions (`hyprlang-config.cpp:372-382`), which is *why* the wiki's
   `ONLY values explicitly changed` sentence is true.
7. **`kb_file` details** — resolved relative to the current config file (`Hyprland-IKeyboard.cpp:88`
   `absolutePath(m_xkbFilePath, Config::mgr()->currentConfigPath())`); a missing file logs
   `Cannot open input:kb_file= file for reading` (`90`) and silently falls through to the names; and when the file
   **does** compile, `m_currentRules` has already been assigned the config names (`66`), so the printed
   `rules/model/layout/variant/options` describe nothing about the keymap in use. That second case is a DIFFER-free
   false AGREE for any tool that compares names only.
8. **`unknown-device`** — the fallback when the normalised name is empty (`Hyprland-InputManager.cpp:2124`), and the
   de-duplication domain is all HIDs (`2126`, `m_hids`), not pointers only. Host corroboration:
   `…-keyboard-1` and `…-1` appear in the L1 live receipt for two different device classes.
9. **`layout` may be a comma list** — `active_layout_index` selects which entry is live (the rule lists are split on `,` in `Hyprland-IKeyboard.cpp:232-235`); the failure path collapses
   the list to a single `us` (`Hyprland-IKeyboard.cpp:113`), so a FALLBACK erases the information about which
   entry failed.
10. **How a runtime change re-applies** — every `input:kb_*` option carries `.refresh = Supplementary::REFRESH_INPUT_DEVICES`
    (`Hyprland-ConfigValues.cpp:271-276`), and `keyword` is a registered command
    (`Hyprland-HyprCtl.cpp:2037`): that is the mechanism behind the bullet *"may have been changed at runtime with
    `hyprctl keyword`"*, which is currently uncited.

---

## 1. Sentence-by-sentence verdicts

Locators below are the computed ones in `locators.txt`; "cited" is what the draft prints.

| # | sentence (abridged) | verdict | the pin that decides it |
|---|---|---|---|
| S1.1 | file read line by line; backslash joins the next line (`44-66`) | S! | `hyprlang-config.cpp:52-63` (`getNextLine`, `line += nextLine;` at 62). Missing: only a **final** `\` continues (a trailing blank kills it), blanks/tabs before it are dropped (`54-55`), the next line is appended **verbatim** (its indentation survives, no space inserted) |
| S1.2 | `#` comments; `##` is one literal `#` (`674-700`) | S! | collapse at `701`, outside the cited range; wording "one literal `#` comment character" is self-contradictory — `##` contributes a literal `#` and does **not** start a comment (`688-702`). Also missing: `#` at column 0 is the directive channel `parseComment` (`674-679`) |
| S1.3 | a key's full name = category stack joined with `:` | S/*uncited* | `hyprlang-config.cpp:280-285` (`valueName += c + ':';`) |
| S2.1 | `device` is a keyed special category, key `name`, 47 values (`518-540`) | S! | key `addSpecialCategory("device", {"name"})` at `518`; 47 values at `519-565` (count recomputed) |
| S2.2 | three spellings reach the same store (`291-320`) | S! | cut at `292-299`, store write at `330`, override use at `342-348`; block form relies on `908` + the composed name. Undocumented in the wiki pin (`73-74`, `110-111`) |
| S2.3 | `device { }` whose first assignment is not `name` is an error (`420-440`) | S | `hyprlang-config.cpp:428-436`, message at `435` |
| S2.4 | current device forgotten at the last close (`885-899`); flat `device:kb_layout` has no device to land on | **W** (first half S) | reset at `896-897`; but `393-441` makes the flat key a **hard error**, and `348-354` makes it land on the still-open block. See H3 |
| S3.1 | six keymap names per keyboard (`1213-1238`) | S | `getDeviceString` ×6 at `1226-1231` (`Hyprland-InputManager.cpp`) |
| S3.2 | `kb_layout` asks the device first, global second (`1226-1231`) | S | `1229` byte-exact |
| S3.3 | device value counts only when the user set it (`1115-1123`) | S | `1119` byte-exact (`Hyprland-ConfigManager.cpp`) |
| S3.4 | the block exists when one carries the keyboard's exact name (`1196-1201`) | S! | function is there, but the name passed in is the **normalised** `m_hlName` (`Hyprland-InputManager.cpp:1214`) and the function itself space→dash-replaces (`1197-1198`); "exact" needs "normalised" |
| S3.5 | a stored `[[EMPTY]]` reads as the empty string (`1156-1168`) | S! + U | `1163-1164`; the literal is unpinned (H7) |
| S3.6 | defaults `us` for layout, empty for the rest (`271-276`) | S | `271-276` byte-exact, layout default at `272` |
| S3.7 | unchanged config → keyboard skipped (`1270-1280`) | S! | `1274`; the comparison also covers `m_xkbFilePath` and numlock/repeat, so an unchanged block is never recompiled |
| S4.1 | the five names go to `setKeymap` (`1282-1295`) | S | call at `1286`; `kb_file` is stored separately one line earlier (`1285`) — worth saying |
| S4.2 | non-empty `kb_file` tried first (`87-96`) | S! | `87` opens the file attempt, `93` compiles it, `97-99` is the names fallback — outside the cited range. See H8.7 |
| S4.3 | no keymap compiles → rules reset, layout `us`, rest empty (`101-116`) | S | `109-115`, `m_currentRules.layout  = "us";` at `113` |
| S4.4 | that is why a typo shows up as `us` | S | follows from `109-113`; no failure is observed on the host, as the entry honestly says |
| S5.1 | the dump prints the stored rules (rules/model/layout/variant/options) and `scrollFactor` with two decimals (`765-772`; `785-802`) | S! | all six fields are there (`788-792`, `770`), but the keyboard object prints 12 fields (`786-797`) and the pointer object 4 (`767-770`); "stored rules" is right (`m_currentRules`, `796`) |
| S5.2 | pointer factor = device-block `scroll_factor` clamped 0..100 only when explicitly set (`1376-1383`) | S | `1379-1380` (`std::clamp(…, 0.F, 100.F)`) |
| S5.3 | otherwise unset, printed as `-1` (`1379-1383`) | S! | `1382` `std::nullopt` + `770` `{:.2f}` → printed **`-1.00`** |
| S5.4 | global `input:scroll_factor` never reaches the field, nor `input:touchpad:scroll_factor` (`ConfigValues 290-300`) | S! | `296` (`min 0, max 2`); the device clamp is `0..100` — the two ranges differ and the entry does not say so |
| S6.1 | virtual keyboard named `hl-virtual-keyboard` plus its process name (`11-30`) | **W** | `12-31`; gated on `misc:name_vk_after_proc`, `-` join, normalised basename, `-unknown`. See H4 |
| S6.2 | client keymap marks the keymap overridden (`36-44`) | S | `41` byte-exact |
| S6.3 | `setKeymap` then returns early (`60-64`) | S | `60-64` byte-exact |
| S6.4 | so the printed rules are the config's names at creation, not a witness of the keymap in use | S | `m_currentRules = rules` is at `66`, i.e. **after** the early return, so the stored rules never follow the client keymap. Keep this sentence; it is the reason the tool's VIRTUAL verdict compares names only |
| S7.1 | name lower-cased, space/newline/comma → `-` (`777-789`) | S | `777-789` byte-exact (`782` comma) |
| S7.2 | duplicate gets `-1`, `-2` (`2119-2131`) | S! | `2124`; add the `unknown-device` fallback and the `m_hids` domain (`2126`) |
| S7.3 | kernel-style product name never matches; the lookup compares exactly | S | exact-key lookup at `Hyprland-ConfigManager.cpp:1117`; the name is normalised first (`777-789`) |
| S7.4 | wiki: copy the name from `hyprctl devices` (`79`); per-device overrides `input` (`64-70`) | S | `79` byte-exact; override sentence at `66-68`; the wiki's own example at `111` (`name = royuan-akko-multi-modes-keyboard-b`) is the better citation for normalisation |
| live run ¶ | 9 AGREE on `br`/`compose:caps`, 1 VIRTUAL, 4 pointers AGREE at -1.00, touchpad `input:touchpad:scroll_factor` is not the field | S | `receipts/live-devices-host-l1.txt`; I reproduced the shape independently (10 keyboards, 4 pointers, all `br`, 4 × `-1.00`) |
| DIFFER ¶ 1 | us+empty ⇒ compile failure, error overlay queues the rejected names | S | `Hyprland-IKeyboard.cpp:102-105` |
| DIFFER ¶ 2 | `hyprctl keyword`, a file the join does not read, an unfollowed `source =` | S/*uncited* | `keyword` handler `Hyprland-HyprCtl.cpp:2037` + refresh flags `Hyprland-ConfigValues.cpp:271-276`; `source` in `wiki-Keywords.md:42-56` |
| DIFFER ¶ 3 | kernel product name instead of the normalised name | S | as S7.1/S7.3 |
| DIFFER ¶ 4 | `switchxkblayout` moves the index, not the stored names | S/*uncited* | `Hyprland-HyprCtl.cpp:1378,1380,1392` (`updateModifiers(…, requestedLayout)`), `m_currentRules` untouched |
| Limits 1 | the XKB compile is not reproduced | S | honest; but the dump's `active_keymap` **is** a compiled witness — say why the join ignores it |
| Limits 2 | `repeat_rate … sensitivity, accel_profile` are per device but "the dump does not print them" | S! | true of the options, misleading as written: the dump prints `numLock`/`capsLock` and the pointer's `defaultSpeed` (not `sensitivity`) — H8.3/H8.4 |
| Limits 3 | variables/`{{ }}` not modelled | S | `hyprlang-config.cpp:518-533,730-781` |
| Limits 4 | the Lua config is out of scope | U | no pin; the same unpinned premise as H7 |

Census line: recomputed field by field — `default_layout=us` (`ConfigValues:272`), `fallback_layout=us`
(`IKeyboard:113`), `device_keys=47` (`ConfigManager:519-565`), `scroll_factor_max=100`
(`InputManager:1380`), `json_scroll_decimals=2` (`HyprCtl:770`), `virtual_prefix=hl-virtual-keyboard`
(`protocols:12`). **S** — the line is exactly what the pins say.

---

## 2. Smallest safe corrections, in order of value per line

1. **Step 5 + table row 5 (H1, H2):** replace the field list with the real one
   (`address, name, rules, model, layout, variant, options, active_layout_index, active_keymap, capsLock, numLock,
   main`; mice `address, name, defaultSpeed, scrollFactor`) and rewrite the UNK row as *"the full keymap is UNK; the
   dump's `active_keymap` names the active layout of the keymap actually installed"*. Add H8.1's `main` paragraph
   with the host cross-tab as the counterexample.
2. **Step 2 last sentence (H3):** replace "has no device to land on" with the measured outcome — a hard
   `first value must be the key` error (`434-438`) surfaced through `m_configErrors` (`ConfigManager:988`), plus the
   still-open-block exception (`348-354`).
3. **Step 6 sentence 1 (H4):** *"named `hl-virtual-keyboard`, plus `-` and the normalised client basename when
   `misc:name_vk_after_proc` is on (default, `ConfigValues:487`), plus `-unknown` when the basename is unavailable;
   with the option off every virtual keyboard is named exactly `hl-virtual-keyboard`"* (`protocols:12-31`).
4. **OBS block (H5):** make S320 and S325 two-line citations and de-pad S316/S319, so all ten quotes grep at their
   claimed line.
5. **Citations (H6):** `674-702`, `518-565`, `291-330`, `87-99`; add the missing locators for S1.3, DIFFER ¶2 and
   DIFFER ¶4.
6. **Unpinned (H7):** pin or generalise `[[EMPTY]]`; mark the Lua sentence `[INFERENCE]` or drop it.
7. **Add the facts in H8.5-H8.10** in one pass on steps 3, 4, 7 and Limits — they cost three sentences and remove
   the false-AGREE case (kb_file wins) and the "exact name" hand-wave.

## 3. Registry consequences for the L1 (integration, not my write)

- S318's scope cell reads *"the `input:kb_*` and `input:scroll_factor` options and defaults"*; the VK fix needs
  `misc:name_vk_after_proc` from the same pin (`ConfigValues:487`). Widen the scope cell or source that one fact
  from S323 minus the default.
- S316's cell reads *"per-keyboard and per-pointer config application, device naming"*; the `main` fact needs
  `InputManager:1940` (+`1193`) — widen to "…, device naming, the `m_active` flag".
- No new source row is required for any correction above; all of it is inside S316-S325 except the
  `STRVAL_EMPTY` definition, which needs an eleventh pin (or the generalised wording).

## 4. What I did not verify

- No XKB compile was run: whether `br` + `compose:caps` exists in xkeyboard-config is not checked (the entry's own
  Limits 1). `active_keymap` on the host is `Portuguese (Brazil)`, which is consistent with a successful compile and
  is the only compilation evidence I have.
- The `IKeyboard` initial value of `m_active` is **not** in the pins (`IKeyboard.hpp` was not fetched); the host
  cross-tab is the only evidence that it defaults true and that only physical keyboards are cleared. The entry must
  either fetch that header or publish `main` as UNK-in-pins with the host observation marked as such.
- `hyprctl devices -j` was read twice, projected to field names and counts only; no device name, window title,
  monitor serial or home path was written into this report. `hyprctl version` was read (0.56.2 / `efb50993`).
  Nothing was dispatched, reloaded, keyworded or injected; no package transaction was run.
- I did not run the C1 or C2 counters and did not touch the reference, the fixtures, or any tracked file.
