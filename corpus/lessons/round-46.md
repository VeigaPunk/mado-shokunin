# Round 46 lesson — the input-device plane (2026-10-26, hyaku run 9)

Lane mado-shokunin. Claims: C1 operability (capability acquisition) `tools/mado-devices.py`, judged by `PRED-C1-r46-v3`
(registration `.ufo/waves/round-46/registration.md` -> `registration-v2.md` -> `registration-v3.md`, all before data);
C2 coverage (sourced) `corpus/knowledge/hyprland-input-devices-r46.md`, judged by `PRED-C2-r46-v2`. Base
`b22ea56bff2faec39ce9ff75d2107eaf4612ecbe`. Gate, registry changes and search log drafted by the w1 seat
`ScrLessonGate`, mistakes by `ScrMistakes`, both integrated by the L1; GATE lines regenerated from the v2 draft.
Quotes are matched on whitespace-collapsed receipts (the counter's rule): S316 and S319 collapse alignment spaces,
S320 spans `Hyprland-HyprCtl.cpp:769-770` and S325 spans `wiki-Keywords.md:67-68`; the start line is the locator.

## Gate

Candidates considered: the ten pins under `.ufo/waves/round-46/fetch/` (all fetched and opened by the L1 2026-10-26;
sha256 in `.ufo/waves/round-46/receipts/fetch-sha256.txt`), screened against the Hyprland tree at `efb50993` and the
hyprland-wiki at `ecc06f3` and at main (receipts `w1/ScrLessonGate/search-screen.txt` sections A-D2, plus
`w1/ScrLessonGate/registry-screen.txt` for the held-row screen).

Admitted: new rows S316-S325, tier A, status `mined`, opened 2026-10-26, used-by the entry; ten distinct receipts and
ten distinct quotes, each quote word-bounded and unique in its receipt with C/C++ comments removed (checks:
`w1/ScrLessonGate/quote-check.txt`, `QUOTE_CHECK: checked=10 failed=0`). Locators below are computed on the
whitespace-collapsed receipt (the counter's rule), never typed: the start line of the quote. S316 and S319 de-space a
source line, S320 spans `:769-770` and S325 spans `:67-68`; the start line is shown.

- S316 · `https://raw.githubusercontent.com/hyprwm/Hyprland/efb50993780079460b0cbed1363e2166a2de1d9f/src/managers/input/InputManager.cpp` (opened 2026-10-26) · `Hyprland-InputManager.cpp:1229` · `const auto LAYOUT = Config::mgr()->getDeviceString(devname, "kb_layout", "input:kb_layout");` — the per-keyboard lookup reads the device block first and the global option second.
- S317 · `https://raw.githubusercontent.com/hyprwm/Hyprland/efb50993780079460b0cbed1363e2166a2de1d9f/src/config/legacy/ConfigManager.cpp` (opened 2026-10-26) · `Hyprland-ConfigManager.cpp:1119` · `if ((!VAL || !VAL->m_bSetByUser) && !fallback.empty())` — a block value the user did not set does not shadow the global option.
- S318 · `https://raw.githubusercontent.com/hyprwm/Hyprland/efb50993780079460b0cbed1363e2166a2de1d9f/src/config/values/ConfigValues.cpp` (opened 2026-10-26) · `Hyprland-ConfigValues.cpp:272` · `MS<String>("input:kb_layout", "Appropriate XKB keymap parameter", "us",` — the built-in layout, while the other five keymap names default to the empty marker.
- S319 · `https://raw.githubusercontent.com/hyprwm/Hyprland/efb50993780079460b0cbed1363e2166a2de1d9f/src/devices/IKeyboard.cpp` (opened 2026-10-26) · `Hyprland-IKeyboard.cpp:113` · `m_currentRules.layout = "us";` — the stored layout after a keymap that does not compile.
- S320 · `https://raw.githubusercontent.com/hyprwm/Hyprland/efb50993780079460b0cbed1363e2166a2de1d9f/src/debug/HyprCtl.cpp` (opened 2026-10-26) · `Hyprland-HyprCtl.cpp:769` · `"defaultSpeed": {:.5f}, "scrollFactor": {:.2f}` — the pointer fields the devices request prints, two decimals.
- S321 · `https://raw.githubusercontent.com/hyprwm/Hyprland/efb50993780079460b0cbed1363e2166a2de1d9f/src/helpers/MiscFunctions.cpp` (opened 2026-10-26) · `Hyprland-MiscFunctions.cpp:782` · `case ',': return '-';` — a comma in a kernel device name becomes a dash, so a block written with "Razer DeathAdder V2" never matches.
- S322 · `https://raw.githubusercontent.com/hyprwm/Hyprland/efb50993780079460b0cbed1363e2166a2de1d9f/src/devices/VirtualKeyboard.cpp` (opened 2026-10-26) · `Hyprland-VirtualKeyboard.cpp:41` · `m_keymapOverridden = true;` — set when a virtual keyboard's client sends its keymap.
- S323 · `https://raw.githubusercontent.com/hyprwm/Hyprland/efb50993780079460b0cbed1363e2166a2de1d9f/src/protocols/VirtualKeyboard.cpp` (opened 2026-10-26) · `Hyprland-protocols-VirtualKeyboard.cpp:12` · `std::string name = "hl-virtual-keyboard";` — the name every virtual keyboard starts with; the process suffix is behind `misc:name_vk_after_proc`.
- S324 · `https://raw.githubusercontent.com/hyprwm/hyprlang/v0.6.8/src/config.cpp` (opened 2026-10-26) · `hyprlang-config.cpp:435` · `special category's first value must be the key.` — the error a `device` block without a leading `name` gets; the same parser holds the continuation, `##` and bracket-key rules.
- S325 · `https://raw.githubusercontent.com/hyprwm/hyprland-wiki/ecc06f3b6605e453c0ad533d979fccbefff788ef/content/Configuring/Keywords.md` (opened 2026-10-26) · `wiki-Keywords.md:67` · `It's worth noting that ONLY values explicitly changed will be overwritten.` — the documented rule the set-by-user test implements; the name, the page says, comes from `hyprctl devices`.

GATE S316 receipt=.ufo/waves/round-46/fetch/Hyprland-InputManager.cpp sha256=feedf32e2e3d23aeaed7a02ef4ab94be2d66f4b22873b3166026da1e9ece4765 quote="const auto LAYOUT = Config::mgr()->getDeviceString(devname, "kb_layout", "input:kb_layout");"
GATE S317 receipt=.ufo/waves/round-46/fetch/Hyprland-ConfigManager.cpp sha256=9db68cf44048d86557d8a53068dcc40b9bd7347c7d95f38edc501565f65be62b quote="if ((!VAL || !VAL->m_bSetByUser) && !fallback.empty())"
GATE S318 receipt=.ufo/waves/round-46/fetch/Hyprland-ConfigValues.cpp sha256=a76f05079454e1f6d4402144e1673cc1cb890d285fbeb947d5afdb004ad97754 quote="MS<String>("input:kb_layout", "Appropriate XKB keymap parameter", "us","
GATE S319 receipt=.ufo/waves/round-46/fetch/Hyprland-IKeyboard.cpp sha256=8a800efe9baa7f375a3781744372eecd98a88be2c4bedaae96c90a1102a1aa3d quote="m_currentRules.layout = "us";"
GATE S320 receipt=.ufo/waves/round-46/fetch/Hyprland-HyprCtl.cpp sha256=798b7c6c4c1684557842463d46ac99c96629be4179e0e461dca77670247b91fa quote=""defaultSpeed": {:.5f}, "scrollFactor": {:.2f}"
GATE S321 receipt=.ufo/waves/round-46/fetch/Hyprland-MiscFunctions.cpp sha256=065418241a3b40e21273bca1fd29036221942554cddb61e08422d86f0a13c1d9 quote="case ',': return '-';"
GATE S322 receipt=.ufo/waves/round-46/fetch/Hyprland-VirtualKeyboard.cpp sha256=bc6d984a4c9e62313501c1cdb4ace3659c16d3b77e029a3c082a77f21500ed86 quote="m_keymapOverridden = true;"
GATE S323 receipt=.ufo/waves/round-46/fetch/Hyprland-protocols-VirtualKeyboard.cpp sha256=43cbf7b39bf0910df6d933cef95f029fa336d5b432b0202280e6fc40d8db2f50 quote="std::string name = "hl-virtual-keyboard";"
GATE S324 receipt=.ufo/waves/round-46/fetch/hyprlang-config.cpp sha256=fa1b6898f2f1676de73220450f18f09603f0c3f8833e4c0a7c42c12aebe1de3e quote="special category's first value must be the key."
GATE S325 receipt=.ufo/waves/round-46/fetch/wiki-Keywords.md sha256=11c0842cb31ddbfd55298c772bc44d9ad8d29c0c91c69bef6010e39b3ebaf51e quote="It's worth noting that ONLY values explicitly changed will be overwritten."

Rejected:
- REJECT hyprland-wiki `content/Configuring/Keywords.md` at main: the path is gone (HTTP 404, `w1/ScrLessonGate/search-screen.txt` §B). The wiki's main branch has moved the config plane to Lua: `content/configuring/core/config.toml` and `content/configuring/core/config-options.md` (`hl.config({...})`) replace the page, and `content/configuring/core/devices.md:12-16` documents per-device config as `hl.device({ name = ..., sensitivity = ... })`, not as a `device { name = X }` block. The pin at `ecc06f3` is the last hyprlang-era statement. Flip: the host's main config becomes a `.lua` file.
- REJECT the same wiki's `content/Configuring/Variables.md` at `ecc06f3` as a second docs row: it prints the global option table (`kb_layout` default `us` at `:186`, `scroll_factor` at `:204`/`:265`) and delegates the per-device block to Keywords (`:311-313`); the census values the entry must carry are computed from the code by clause h, so a docs duplicate covers no surface the pin set lacks.
- REJECT Hyprland `src/devices/Keyboard.cpp` (56 lines): it wires aquamarine key and modifier events and calls `updateXkbStateWithKey`; zero hits for `getDeviceString|setKeymap|kb_layout|keymap` (`w1/ScrLessonGate/search-screen.txt` §D2). No config read, no keymap compile, so it cannot move any step of the chain.
- REJECT Hyprland `src/devices/Keyboard.hpp` (21 lines, 0 symbol hits) and `src/devices/IKeyboard.hpp` (137 lines, 9 hits): declarations only — `setKeymap` at `IKeyboard.hpp:68` and the `m_keymapOverridden` field at `:94` — while the behaviour that decides the dump is the definition in the pinned `IKeyboard.cpp` (S319). The field line is read as part of S319's scope instead of taking a row.
- REJECT Hyprland `src/config/ConfigManager.cpp` as a row: it is the manager selector — a `.lua` main config selects `Lua::CConfigManager`, otherwise `Legacy::CConfigManager` (`:33-50`, two Lua assignments at `:36` and `:47`) — and holds no device store or fallback. It does settle which manager this host runs (host `hyprland.conf` present, `hyprland.lua` absent, `search-screen.txt` §C), which is why the legacy pins are the live path here.
- REJECT Hyprland `src/config/lua/ConfigManager.cpp` as a row: the Lua manager re-implements the same device-first-then-global rule over its own store (`:983-1020`), so it is parallel semantics on the plane the entry excludes, not the host's path at `efb50993`.
- REJECT `src/managers/KeybindManager.cpp:296-313` as a row: it compiles the global `input:kb_*` options into the keybind translation state with no device lookup — the keybind keymap, not the rules the dump prints (this is also why a per-device layout leaves keybinds on the global keymap).
- REJECT `src/desktop/view/Window.cpp:1156-1161` and `src/desktop/rule/windowRule/WindowRuleApplicator.hpp:129-130` as rows: both consume the global `input:scroll_factor` as a window-scope scroll effect, and neither writes the pointer field the dump prints (`InputManager.cpp:1350-1383`).
- REJECT `src/devices/IPointer.hpp` as a row: `:116` holds `std::optional<float> m_scrollFactor = {}` — the storage that makes the nullopt branch print -1 is stated in the pinned `InputManager.cpp`/`HyprCtl.cpp` lines.
- REJECT the five accessor/value headers `src/config/ConfigManager.hpp:47-52`, `src/config/legacy/ConfigManager.hpp:52`, `src/config/lua/ConfigManager.hpp:67`, `src/config/values/ConfigValues.hpp:129`, `src/helpers/MiscFunctions.hpp:42`: pure-virtual accessors and value-table declarations whose definitions are pinned (S317, S318, S321); a row on a declaration would cite no behaviour.
- REJECT `src/config/lua/bindings/LuaBindingsConfigRules.cpp:257` as a row: the Lua-era option table's `scroll_factor` float bounds (0..100) restate a ceiling the dump's field obeys through the hyprlang clamp in S316's receipt.

Held rows on the same URLs, and why new rows rather than widened ones: `corpus/SOURCES.md` already holds three scopes on `debug/HyprCtl.cpp` — S018 (`getprop` dispatch, blob URL), S158 (raw URL; `clients` tags, `getprop`, `layers`), S307 (raw URL; the monitors request) — and two on `config/legacy/ConfigManager.cpp` — S162 (windowrule keyword handlers, named special-category reconstruction, reload traversal) and S303 (monitor line grammar); plus S215 on `config/values/ConfigValues.cpp` (the two log switches at `:629`/`:632`), S182 on `helpers/MiscFunctions.cpp` (workspace command normalizer, `:478-513`), S173 on the hyprlang `config.cpp` (RHS `{{…}}` expression parsing). The new S320 (devices request), S317 (the `device` category and the per-device fallback), S318 (the keyboard and scroll defaults at `:271-300`), S321 (the name normalizer at `:777-789`) and S324 (continuation, `##`, bracket key, first-value rule) sit on those files under scopes no held row names; five pins are first uses of their URL (InputManager.cpp, IKeyboard.cpp, devices/VirtualKeyboard.cpp, protocols/VirtualKeyboard.cpp, wiki Keywords.md). Widening a held row is not available to this predicate: clause c requires a held row's cells 1-9 to stay byte-equal (`quality/counters/c2-r46-input-device-entry.py:493-496`), so an edited scope cell would fail the round's own counter for the ids other entries cite. Cost, declared in the registration: two W04 duplicate-URL census warnings (S317 beside S162/S303; S320 beside S158/S307 — S018 carries a `github.com` blob URL, so the raw URL repeats only S158 and S307), the same class `receipts/census-before.txt` already prints at base for the round-45 rows.

## Registry changes

| surface | old | new |
|---|---|---|
| `corpus/SOURCES.md` | 252 rows, last `S315` at line 264 | 262 rows; `S316`-`S325` appended after the last `S` row (`.ufo/waves/round-46/l1-draft/build-pos.py:87-92`), each 11 cells, tier `A`, `mined`, opened `2026-10-26`, recheck `90d`, used-by `corpus/knowledge/hyprland-input-devices-r46.md` |
| `corpus/README.md` | 62 knowledge-index rows, last the round-45 row at line 73 | 63 rows; one three-cell row inserted after it, naming the entry, `draft`, and `S316-S325` (`build-pos.py:102-103`) |
| `corpus/knowledge/` | 62 files | 63 files (the entry) |
| `corpus/lessons/` | 66 files | 67 files (this lesson; `build-pos.py:94-98` writes a Gate-only positive-control copy — the integrator merges this draft's prose around those ten lines) |
| `tools/` | 13 files, `mado-monitors.py` the newest | 14 files (`mado-devices.py`; C1's surface, no registry row) |
| held rows `S018`, `S158`, `S162`, `S173`, `S182`, `S215`, `S303`, `S307` | cells 1-10 unchanged | unchanged; only the census gains the five W04 lines below |
| new duplicate-URL census lines | 0 for these URLs | 5 (`S317`, `S318`, `S320`, `S321`, `S324`; registration-v2.md erratum) |

## Search log

Question: how does Hyprland 0.56.2 at `efb50993` turn the `input` block and a `device` block into the XKB names a
keyboard stores and the scroll factor a pointer reports, and which files must a row cite to bind each step?

Where searched: the Hyprland tree at the host revision (blobless clone at tag `v0.56.2`, `rev-parse HEAD` =
`efb50993780079460b0cbed1363e2166a2de1d9f`); hyprlang `v0.6.8`; the hyprland-wiki at `ecc06f3` and at main; the lane's
registry `corpus/SOURCES.md`; the host read-only (`hyprctl` reads and the existence of the two config-manager
selectors); `receipts/` and `quality/counters/c2-r46-input-device-entry.py` for what the predicate can see.

Identified: 799 files under `src` at `efb50993`; 217 match a name filter (`input|keyboard|device|hyprctl|config|virtual`);
20 files under `src` carry at least one symbol of the plane, independently of the name filter (`getDeviceString`,
`getConfigValueSafeDevice`, `scrollFactor`, `scroll_factor`, `m_keymapOverridden`, `deviceConfigExists`,
`deviceNameToInternalString`, `addSpecialConfigValue("device"`, `virtualKeyboardNameForWlClient`, `"input:kb_`,
`hl-virtual-keyboard`; `w1/ScrLessonGate/search-screen.txt` §A). Out of the tree: 7 more candidates probed (§B-D2).

Screened: 27 probed files — the 20 symbol-bearing files read at their symbol lines and the 7 out-of-tree probes —
plus the 2 pins outside the Hyprland tree (hyprlang `v0.6.8` `config.cpp`, the wiki `Keywords.md` pin): 29 candidates,
and the Gate's Admitted and Rejected lists account for all 29.

Included: 10 — new rows S316-S325: 8 of the 20 (`InputManager.cpp`, legacy `ConfigManager.cpp`, `ConfigValues.cpp`,
`IKeyboard.cpp`, `HyprCtl.cpp`, `MiscFunctions.cpp`, devices/`VirtualKeyboard.cpp`, protocols/`VirtualKeyboard.cpp`) and
the 2 candidates outside the Hyprland tree (hyprlang `v0.6.8` `config.cpp`, the wiki `Keywords.md` pin).

Excluded: 19. Of the 20 symbol files, 12: seven declaration headers (`ConfigManager.hpp`, legacy `ConfigManager.hpp`,
lua `ConfigManager.hpp`, `ConfigValues.hpp`, `IKeyboard.hpp`, `IPointer.hpp`, `MiscFunctions.hpp`); the Lua manager and
its option-table binding (lua `ConfigManager.cpp`, `LuaBindingsConfigRules.cpp`; parallel semantics on the `.lua` path);
the two window-scope scroll consumers (`Window.cpp`, `WindowRuleApplicator.hpp`); the keybind translation state
(`KeybindManager.cpp`). Of the 7 probes, all 7: wiki main `Keywords.md` (404), wiki main `devices.md` and
`config-options.md` (Lua plane), wiki `Variables.md` at the pin (global table only), `Keyboard.cpp`, `Keyboard.hpp`, and
the manager selector `config/ConfigManager.cpp` (read as context, not a row). Each exclusion names its decisive line in
the Gate's Rejected block.

Registry screen: 252 rows at the freeze; the ten pin URLs are already held by S018, S158, S162, S173, S182, S215, S303
and S307 in eight other scopes, and by no row for the five first-use URLs (`w1/ScrLessonGate/registry-screen.txt`).

Stop: every step the tool compares — parse (S324), device category and fallback (S317), per-keyboard lookup (S316),
global defaults (S318), compile and the `us` fallback (S319), the dump fields (S320), the virtual name and its override
(S322, S323), the name normalizer (S321), the documented block (S325) — has a pinned line, and the remaining
symbol-bearing files are declarations, the Lua manager, or window/keybind consumers of the same global options; none of
them adds a step between the config and the printed fields. Re-open the search when `hyprctl version` leaves `efb50993`,
when hyprlang leaves 0.6.8, or when the host's main config becomes a `.lua` file (the Lua manager path becomes live and
this entry's form no longer describes it).

## Mistakes

**M46-1** · class `number-drift` · evidence: the frozen registration states two cross-scope URL repeats
(`.ufo/waves/round-46/registration.md:47`, "The two cross-scope URL repeats"), while the positive-control
tree prints **five** new W04 lines — S317 (with S162, S303), S318 (with S215), S320 (with S158, S307),
S321 (with S182), S324 (with S173): `receipts/census-pos.txt` (14 W04 lines at the positive tree) against
`.ufo/waves/round-46/receipts/census-before.txt` (9 W04 lines at base), and exact-URL row counts in `receipts/url-exact-pos.txt`
(ConfigManager 3 rows, ConfigValues 2, HyprCtl 3, MiscFunctions 2, hyprlang 2) · two independent seats reached
the same five (`CritRegistration.md:16`, F1 "F1 (wrong count)"; `CritPremise.md:20`, "5 duplicate-URL introductions declared as 2") ·
captured-by: QUALITY 10 and 14 — the sentence was hand-written, not emitted by the instrument that measures it ·
fix: the round lesson/errata carries the census delta (five) and names each new row with the held row(s) it
repeats; the frozen registration is not rewritten. Shown able to fail: the census is a command whose W04 line
count moves 9 → 14, so a sentence claiming two disagrees with its own instrument by three rows.

**M46-2** · class `vacuous` · evidence: the C2 control battery's first cut stopped before scoring — its
FALSE-URL fixture asserted global uniqueness of a URL the corpus holds twice
(`.ufo/waves/round-46/ctl/run-c2-controls.py:17`, "the first cut's single-occurrence assertion stopped the runner
before any score"; the assertion survives at `:126`, `assert reg.count(url) == 1`) · measured on the positive
tree (`receipts/harness-assert-demo.txt`): the MiscFunctions URL occurs **2** times (S182, S321) so the assertion
raises, while the protocols/VirtualKeyboard.cpp URL occurs **1** time (S323) so it holds; `receipts/url-exact-pos.txt`
shows both rows · why vacuous: a battery that stops after seven of its fifteen controls prints no `CTL_C2` verdict, so the
fifteen controls produced **no** evidence, and a relaxed `>= 1` would have rewritten a held row's URL (S182)
alongside the new row's — a control mutating outside its subject · captured-by: QUALITY 59 is adjacent (a
control that fails for a setup reason is not a kill) but it names the environment, not a corpus premise ·
fix: address the mutation by row identity (the row's own location cell) and assert on that cell, never a global
string count; the committed control mutates S323's unique URL and the counter rejects it
(`.ufo/waves/round-46/receipts/ctl-c2.txt:9`, "CTL_C2 FALSE-URL want=rejected got=rejected rc=1 ok", clause `e:0`).
Shown able to fail: `check87.py` scores the committed receipt `PASS` (15 controls, verdict present) and the
aborted shape `FAIL` (`scored=7 want=15 verdict_line=absent`, `receipts/check87-run.txt`).

**M46-3** · class `survivor` · evidence: a reference variant that undoes one modelled semantic — case-insensitive
device-name matching (V03) — met PRED-C1-r46 before the freeze (`registration.md:34`, "A pre-freeze run met V03
(case-insensitive names)"), i.e. the fixture lattice had no case-sensitivity class; the separating fixture was
added before data (`.ufo/waves/round-46/receipts/ctl-c1.txt:7`, "V03-case-insensitive-names rc=1 … fixtures=89/90
… verdict=TARGET_MISSED"; the fixture is `quality/counters/c1-r46-fixtures.json` index 22, label
`case-exact-dump-name`, file sha256 `027ed508…` = the counter's `FIXTURES_SHA256`, `receipts/fixtures-pin.txt`) ·
the pre-freeze run itself has no committed receipt — the evidence is the registration's sentence plus the
post-freeze control line, and `CritRegistration.md` §4 records that limit · captured-by: QUALITY 65 (fixtures from
a lattice on the tree index, one single-defect mutant per class; a survivor is a missing class) ·
fix: the case class is a fixture, not a comment. Shown able to fail: V03 scores 89/90 at the freeze and the
mutant matrix flips V03 to MET only when clause f's exactness is weakened (`MutC1Counter.md:33`, "V03
(case-insensitive names): fixture `case-exact-dump-name` FAIL in all three runs"; `:78`, "The control set's only
load-bearing channel is clause f's exactness") `[seat receipt]`.

**M46-4** · class `vacuous` · evidence: PRED-C2-r46 admits 10 of 12 crafted revisions a reader rejects, and
**six are undeclared** (`CritC2Forgery.md:10`, "10 were admitted"; `:14`, "6 admitted forgeries are NOT declared";
per-revision counter lines `CritC2Forgery/forge.out:3-15`) `[seat receipt]`. The two sharpest: F7 — the revision
authors its own live receipt under `.ufo/waves/round-46/receipts/` and cites it, clause i reading cited receipts at
REV; F10 — the whole chain replaced by 28 surface bullets while clause j stays `1`. Code paths (computed,
`receipts/c2-counter-sites.txt`): the duplicate-URL guard is keyed on the scope cell (`quality/counters/c2-r46-input-device-entry.py:587`),
the anchor cell is read for range shape only (`:610`), T3 walks fenced blocks only (`:423-430`), clause j binds a
locator and a keyword per surface (`:387`, `:417`) · captured-by: QUALITY 55 (a shape counter names the cribs that
fake its result) — the docstring names three residuals (`:70-74`) but not these six cribs ·
fix: seven tightening candidates A–G (`CritC2Forgery/tighten.py`, `tighten.out`): the positive control passes all
seven and each undeclared forgery fails the intended check (F5d fails two: `E=0 F=0`) (pos `A=1 B=1 C=1 D=1 E=1 F=1 G=1 PASS`; F4
`B=0`; F6 `A=0`; F7 `C=0`; F8 `D=0`; F5d `E=0 F=0`; F10 `G=0`). The frozen counter cannot be edited this round;
the candidates are the next counter's clauses. Shown able to fail: `check88.py` reads `PASS` on
forge.out+tighten.out with the declared set (F1,F2,F3,F9) and `FAIL` when only the positive line is committed
(`admitted_uncovered=F10,F4,F5d,F6,F7,F8`) and when no residual is declared (`admitted_passing=F1,F2,F3,F9`)
(`receipts/check88-run.txt`).

**M46-5** · class `provider` · evidence: the round-45 entry attributes the landed tool's live run to the L1
*reference's* receipt — entry `corpus/knowledge/hyprland-monitor-rule-r45.md:96` at `4d22eeb` cites
`.ufo/waves/round-45/receipts/live-monitors-host-l1.txt`, whose header at `:4` records tool sha256 `c6ac5fc2d35e40b34dcf031940222fbe5ec5f0ce4b07d6a41866b196843726be`,
while the landed tool at `4d22eeb` hashes
`2f007417ae9efa43c7c3e5bcf8e88710fb6cd6c856e49b4084c742a7ecff5609` (`git show 4d22eeb:tools/mado-monitors.py | sha256sum`) and its own receipt records that hash
(`.ufo/waves/round-45/receipts/live-monitors-host-r45.txt:4`; both bound in
`CritW2Entry/receipts/tool-hash-binding.txt`) · `CritW2Entry/report.md:64` (F2, "false provenance, claim true") `[seat receipt]` ·
captured-by: QUALITY 24 (a sentence that relies on a run receipt cites one whose own bytes name its producer);
the C2 counter cannot see it (declared residual, clause j binds a locator and a keyword, not the truth of the
sentence) · fix: cite `.ufo/waves/round-45/receipts/live-monitors-host-r45.txt`, or say "the reference reported…"; the entry is
landed data, so the correction is an appended erratum. Shown able to fail: one `git show <rev>:<tool> | sha256sum`
against each receipt's header line separates the two receipts (they differ).

**M46-6** · class `attribution` · evidence: the round-45 entry cites, for the mechanism that keeps a disabled
output out of the active list, the branch that *returns before* the event — entry `:84` cites
`Hyprland-Monitor.cpp:264` and `:389`; `:264` returns at `:271`, the only emit site is `:389`, and the veto is
`:275-287` (`CritW2Entry/report.md:40`, "the real gate is uncited (mis-located)"; the ledger's computed 262-290
dump in `CritW2Entry/receipts/verify-quotes.txt`) `[seat receipt]` · captured-by: **none** — `quality/check-locators.py`
(QUALITY 77) passes because the emit fragment occurs at the other cited line, so a range that contains the
identifier is not a range that carries the mechanism · fix: cite `275-287` and `389`. Shown able to fail: the
w2 sentence ledger (`CritW2Entry/receipts/verify-quotes.txt`, 71 probes, `found=71 not_found=0`) is the instrument
that caught it and is re-runnable on the corrected locator `[seat receipt]`.

**M46-7** · class `vacuous` · evidence: the round-45 privacy gate's own selftest passes while the shapes it exists
to catch pass invisibly — `CritW2Gate.md:14` ("the gate's own selftest is `passed=22/22 failed=0` while **22 of 22
attack shapes pass it"), the receipt's per-shape lines (`CritW2Gate/receipts.txt:21`, "caught 0/19", plus three
further misses = 0/22) and the legitimate-shape side (`:28`, "caught 5/6"; `CritW2Gate.md:15`, "5 of 6 legitimate
shapes are flagged"); scan caps: 20 000 stray braces make a dump clean with no truncation signal (`CritW2Gate/receipts.txt:36-39`);
the redaction markers the fleet uses are themselves flagged (`CritW2Gate/receipts.txt:45-52`); the receipt's own lane census reads
`files=17098 findings=102` (`:60`) `[seat receipt]`. M45-1 credited this gate as "shown able to fail" from two
projected files · captured-by: QUALITY 30 (a detector credited for recall is admitted only beside its precision
evidence) — a detector's own selftest is not that evidence · fix: the marker layer makes the false positives
triageable (base 97 findings → 48 with 49 waived; a planted real dump still flagged; a tampered waived fixture
re-flagged, `ExecSessionTriage.md` §3) `[seat receipt]` but does **not** close the 22-shape recall gap; the gate's
claim is narrowed to a policy instrument and `CritW2Gate/repro.py` is its recall measurement. Shown able to fail:
the frozen gate catches 0/22 attack shapes while its selftest reads 22/22 — the two numbers are one receipt apart.

**M46-8** · class `landing` · evidence: round-45 D4's remedy is half-done — `results.json` is gone from
`.ufo/waves/round-45/w1/MutC1Counter/`, but the 282 B replacement digest is itself untracked:
`receipts/d4-d5-state.txt` (`GIT_OPTIONAL_LOCKS=0 git status --porcelain` → `?? .ufo/waves/round-45/w1/MutC1Counter/results.digest.txt`;
`git ls-files` lists four files, not the digest) · `CritRegistration.md:55` (F3, "F3 (stale pointer)") · captured-by:
QUALITY 13 (evidence meant to outlive a round is a committed path) · fix: commit the digest in the round-46 data
commit. Shown able to fail: `git cat-file -e <data-rev>:<digest>` — the path is absent from the tree at the
revision a closure reads until it is committed.

**M46-9** · class `provider` · evidence: the round-45 wave results file is not evidence — 41 seats, 41
`output: null` (`receipts/d4-d5-state.txt`: `seats 41 n 41 null_outputs 41`); the seat report files are the only
record (`corpus/lessons/round-45-verifier-spotcheck.md:116`, D5) · captured-by: QUALITY 79 (a pointer that asserts
a run names a committed receipt) · fix: the wave README or the lesson says the seat `.md` files are the record, not
`w1-results.json`. Shown able to fail: the results rows carry no output, so no claim can cite them, while each seat
report is a committed path.

**M46-10** · class `number-drift` · evidence: M45-2 says the host monitor serial is in one held entry; it is in
**three** held entries and 21 wave copies — `receipts/d2-serial-count.txt`: the token common to the three cited
lines equals a live `monitors all -j` serial field (compared in-process; the value is never written), 24 tracked
files carry it, 3 under `corpus/` (`config-health-report-r3.md`, `hyprctl-verification-layer.md`,
`hyprland-config-plane.md`) and 21 under `.ufo/` · the corrected gate copy flags all 24 carriers
(`ExecSerialRule/receipts/base-scope-all-r5-r6.txt:49`, "R5_SERIAL_PROSE=24 R6_SERIAL_EXACT=24") `[seat receipt]` ·
captured-by: QUALITY 10 and 14 (a count names its command; a census names both sets) · fix: appended erratum
naming the three paths (removal from pushed history stays the operator's), plus the gate's R5/R6 prose rules.
Shown able to fail: base 24 findings → projected tree 0
(`ExecSerialRule/receipts/projected-scope-all-r5-r6.txt:1`, "findings=0 rev=cb46276e"), 45/45 selftest cases `[seat receipt]`.

**M46-11** · class `reference-drift` · evidence: the C2 draft entry's model of the parser and of the dump
drifted from the pins in the places the frozen clauses cannot see — a flat `device:kb_layout = x` is a hard config
error, not a silent no-op (`CritEntryContent.md:67`, "is a hard config error, not a silent no-op"; the entry's
step 2 concludes that the flat key has no device to land on), the UNK row is wrong because the dump prints `active_keymap`
(`CritEntryContent.md:46`, H2), and the `47 values` count is not inside its own cited range
(`ExecC2Census.md:151`, "count is not witnessed by its cited range": 519-565 carries the 47 registrations, 518-540
covers 22) `[seat receipt]`. A fourth unit omits a dump field the same file prints — `main`, which on this host is
true only for the virtual keyboard (`CritEntryContent.md:26`, H1) `[seat receipt]` · captured-by: **none** for the
mechanism sentences (clause j binds a locator and a keyword per surface, not the truth of the sentence); QUALITY 77
catches the narrow locator only because the count's identifier is outside the cited range · fix: the L1 corrects the
entry before the data commit (step 2's conclusion, the UNK row, the 47-value locator split into `518-540` +
`541-565` or dropped from the sentence, and one line on `main`). Shown able to fail: the two seats' own locator
scripts re-derive the counterexamples (`CritEntryContent/locators.txt`, 66 locator rows;
`ExecC2Census/independent-derivation.txt`), and both print the pin lines the draft sentence contradicts
`[seat receipt]`.

**M46-12** · class `vacuous` · evidence: C1's clause r ("no `hyprctl`/`libinput`/`journalctl`/`udevadm` run") is
a PATH-marker test, not an execution test — the marker stubs exist only on environments A/B's PATH, the selftest is
launched with `env={"PATH": "/usr/bin:/bin"` and no fake bin (`quality/counters/c1-r46-devices.py:375`), and
`sandbox()` binds no stub over `/usr/bin` (`:251-257`). Two tools that run `/usr/bin/hyprctl` — one by absolute path
on every run, one by bare name under `--selftest` — score `readonly=ok tool=present verdict=TARGET_MET` at nonce 46
(`SentTool/evidence/clause-r-bypass-absolute-path.txt:96-97`, `clause-r-bypass-selftest-path.txt:95-96`) `[seat receipt]` ·
captured-by: QUALITY 56 (a clause that cannot fail under its own spec is dead code) and 67 (a read-only claim is
stated over every argv element — here the *scored tool's* argv, which the clause never sees) ·
fix: bind the four stubs over their `/usr/bin` paths inside `sandbox()`, give the selftest environment A's PATH, and
fail the clause on any `execve` beyond the tool's own (`strace -f -e trace=execve`); the two committed bypass tools
are the red state and the green (both read `marker=present` → `readonly=fail`) has not been run — the next counter
must score them. Shown able to fail: today's receipt prints `clause=r marker=absent` for a tool that ran hyprctl, so the
clause's own observable is the defect. The in-flight v2 (`quality/counters/c1-r46-devices-v2.py`, untracked, 17:57)
closes two of the three shapes — the selftest env carries the fake bin first (`:403`) and a pipe tripwire replaces
the file marker (`:154-159`) — but `/usr` is still bound read-only (`:280`) with the stub only on PATH, so the
absolute-path shape stays open as written; binding the stub over `/usr/bin/<name>` or logging `execve` is still
needed (`receipts/c1-v2-carryover.txt`, a source reading, not a scored run).

**M46-13** · class `landing` · evidence: the counter promises "nothing in the lane is" written
(`quality/counters/c1-r46-devices.py:9`), while `load_model()` imports the pinned reference through `importlib`
(`spec.loader.exec_module(mod)`, `:99-101`) with no bytecode guard (`dont_write_bytecode`/`PYTHONDONTWRITEBYTECODE` absent,
`receipts/senttool-verify.txt`), so CPython writes
`.ufo/waves/round-46/l1-draft/__pycache__/mado-devices.cpython-314.pyc` — 40172 B, present in the frozen tree
(2026-10-26 17:23), hidden from `git status` by `.gitignore` · captured-by: **none** (criteria 13 and 63 govern
committed evidence, not a counter's own writes into the tree it scores) · fix: `sys.dont_write_bytecode = True` plus
`PYTHONDONTWRITEBYTECODE=1` in every env, and load the model with `compile(pinned_bytes, …)` + `exec` instead of
`importlib`. Shown able to fail: a tree observable of the two directories around one scoring run — today the run
gains a `.pyc` (the file is already there), after the fix it gains none; the red is visible in the frozen tree, the
green is not run here.

**M46-14** · class `scope` · evidence: clause i's isolation hides exactly three paths — `hidden_paths()` returns
`{realpath(repo), lane root, dirname(lane root)}` (`quality/counters/c1-r46-devices.py:241-243`) — so a scored tool
reaches `$HOME`, `/run/user/<uid>` and 25 sibling scratch dirs, and a unix socket on a `--ro-bind` is still
connectable: `sock_count=1`, `read_hypr_conf=yes`, `list_seat_scratch=25 other_seat_dirs_visible`, and `CONNECT_OK`
under both `--ro-bind` and `--bind` (`SentTool/evidence/sandbox-reachability.txt:6-10`, `socket-ro-bind.txt:3-5`)
`[seat receipt]` · captured-by: QUALITY 29's declared limit ("fail-closed setup is not containment") — clause i is
true as written and the safety sentence built on it is wider · fix: add `~` and `/run/user/<uid>` to `hidden_paths()`
so `sandbox()` tmpfs-mounts them (two lines, no contract change). Shown able to fail: the same reachability probe
under the fixed argv must print `sock_count=0` and `read_hypr_conf=no`; the red is the seat's receipt, the green is
not run here. The in-flight v2's allowlist root (no `/home`, `/run`, `/fast`; `:280-287`) is that fix in source form
(`receipts/c1-v2-carryover.txt`, a source reading, not a scored run).

**M46-15** · class `vacuous` · evidence: `PRED-C1-r46-v2`'s clause r (an inherited pipe the fake binaries write to)
was met by two of its own registered controls at the v2 freeze `2bcc335f` (`receipts/ctl-c1-v2.txt`: TRIP-ABSOLUTE-PATH
and TRIP-SELFTEST-ONLY `TARGET_MET`, `VERDICT: FAIL ... 2 of 40`): Python's `subprocess` closes inherited fds, so a
tool's own child could never reach the pipe · captured-by: the registered control set itself (criterion 86's controls
"include e[very] cheat") - the control battery caught it before any data · fix: `PRED-C1-r46-v3` puts the tripwire on
a unix socket the counter listens on outside the sandbox (`registration-v3.md`); shown able to fail: the same two
controls read `readonly=fail ... TARGET_MISSED` under v3 (`receipts/ctl-c1-v3.txt`).

**M46-16** · class `landing` · evidence: the S290-S297 supersession (round-43 D2, round-44 D6, round-45 D6) slips a
third time: `w1/ExecSupersede/rows.md` drafted S326-S333 census-clean on six mirror runs, but the round's budget went
to the two re-registrations and the rows are not landed · captured-by: none (considerthese 2026-10-26 proposal 3,
mined below, is the instrument that makes the age visible) · fix: next round lands the drafted rows under its own
registration first, before any new claim; age now 4 rounds (`w1/ScrRoutedAges/ages.md` R43-D2).

### Applications of existing criteria

- M46-1 and M46-10 → criteria 10 and 14 (a count is re-derived from its instrument; a census names both sets).
- M46-3 → criterion 65 (fixture lattice, one mutant per class).
- M46-4 → criterion 55 (a shape counter names the cribs that fake it); criterion 84 already covers pinning every
  receipt read and is the F7-shaped hazard one step over.
- M46-5 and M46-9 → criterion 24 (producer identity) and 79 (a pointer names a committed receipt).
- M46-6 → criterion 77 is adjacent but **does not catch it** (the identifier is in the other cited range); the
  non-author reading is the only instrument, which is why M46-6 is recorded as captured-by none.
- M46-7 → criterion 30 (precision evidence beside a recall claim).
- M46-8 → criterion 13 (evidence outliving a round is a committed path).
- M46-12 → criteria 56 (a clause that cannot fail under its own spec is dead code) and 67 (a read-only claim over
  every argv element — extended here to the *scored tool*); criterion 86 hides the judge, not the host.
- M46-14 → criterion 29's declared limit: fail-closed setup is not containment.
- M46-13 → no numbered criterion; a counter's own write into the tree it scores is the gap criteria 13/63 leave.

### Conflicts recorded for the judge

1. **False positives on the privacy gate, same revision, two readings.** `CritW2Gate.md:15` — "5 of 6 legitimate
   shapes are flagged" (documentation examples of the dump shapes, must-stay-clean) — against
   `ExecSessionTriage.md:47` — "False positives: **0**. Every match is a genuine dump-shaped object" (classified by
   provenance, synthetic vs real). Both measured at `4d22eeb`. The two seats count different populations (planted
   documentation examples vs the lane's existing findings); neither number refutes the other, and the lesson must
   name which population it quotes.
2. **Whether the anchor cell's shape read is a declared residual.** `CritC2Forgery.md:14` lists F6 (anchor cell
   naming the right file and the wrong lines) as **not** declared, while the counter's docstring says
   "registry cells 3-6 of a new row are not read except the scope cell" and then names the anchor ranges
   (`quality/counters/c2-r46-input-device-entry.py:72`). The seat reads "read" as "checked against the claim"; the
   docstring reads it as "parsed for range shape". The rule in M46-4's fix (candidate A) settles it for the next
   counter, not for this one.

## Round-45 closure items (`corpus/lessons/round-45-verifier-spotcheck.md` section 6)

- D1 (41 seats; w2 never ran): this round is one v2 wave of 66 seats, and 11 of them attacked the round-45 data:
  `w1/ExecW2Monitors` (five fresh nonces `fixtures=81/81 generated=150/150`, 22/22 adversarial configs),
  `w1/CritW2ToolSemantics`, `w1/CritW2Entry` (six non-supported sentence units in the round-45 entry, of which M46-5
  and M46-6 are two), `w1/CritW2Gate`, `w1/RevW2Rows`, `w1/RevW2Counters`, `w1/MutW2Tool`, `w1/SentW2Privacy`.
  The round-45 entry's sentence-level defects are recorded here; their errata are routed to round 47.
- D2 (M45-2 undercount): corrected in M46-10 (three held entries and 21 wave files; the serial is written nowhere).
  The prose serial rule for the gate is drafted at `w1/ExecSerialRule/` and not installed (routed).
- D3: the `mado-session-material` gate-registry row lands in `SKILL.md` this round; the triage of the 97 findings at
  `4d22eeb` is `w1/ExecSessionTriage/triage.tsv` (15 real, 82 synthetic); the synthetic-material marker layer is
  drafted (`w1/ExecSessionTriage/check-session-material.py`, both directions shown) and not installed (routed).
- D4: `.ufo/waves/round-45/w1/MutC1Counter/results.json` removed from the worktree; its digest line
  (`results.digest.txt`, sha256, size, entry count) is committed beside `summary.txt`.
- D5: `.ufo/waves/round-45/w1-results.json` holds `output: null` for its 41 seats (orchestrator kernel restart); the
  seat `.md` files are the only record of that wave. (Round 46's `w1-results.json` carries 66 outputs.)
- D6: S290-S297 supersession not landed (M46-16); round-44 `w2/ConnCalibration` errata drafted at
  `w1/ScrErrata/errata.md`, not landed (routed).

## considerthese

`considerthese/2026-10-26.md` proposal 3 ("Track routed defects until they close") mined by `w1/ScrRoutedAges`:
`ages.md` Table 1 classifies 45 routed bullets of the round-38..45 spot-checks (42 rows, 23 closed, 15 open, oldest 8
rounds at R38-3); it lands as QUALITY criterion 90 (below). Proposal 2 (a ledger of live-state tools) has a draft at
`w1/ConnToolFamily/`, not landed.

## Assimilation

None. `w1/ScoutShokuknow` and `w1/ExecIdGuard`: no staged `merge/mado/` theme touches the input-device plane (42
themes screened: 0 admit, 2 refuse, 40 none); the staged id space S203-S349 collides with 60 registry ids and covers
this round's own S316-S325 block, so any later adoption renumbers by document first.
