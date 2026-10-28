# Callers of applyConfigToKeyboard / setKeyboardLayout and handlers of REFRESH_INPUT_DEVICES

Seat R55W2ScoutCallers, wave w2 (falsify), 2026-10-28. Re-issue of the w1 item that died on a provider limit.

- Commit: efb50993780079460b0cbed1363e2166a2de1d9f (the C1 pin commit).
- Method: one network read of the commit tarball (`codeload.github.com/hyprwm/Hyprland/tar.gz/<sha>`) into scratch; text grep over that single-commit tree. No C++ LSP server/device was available in this session, so semantic tracing was not possible; as compensation the tree was byte-compared against the lane pins: `cmp` says IDENTICAL for `Hyprland-InputManager.cpp`, `Hyprland-ConfigValues.cpp` and `Hyprland-legacy-ConfigManager.cpp` in `.ufo/waves/round-55/fetch/`, so every line number below is on the same bytes the entry pins (receipts/fetch-provenance.txt, receipts/SHA256SUMS-fetched.txt).
- Every hop below is OBSERVED (quoted from the tree) unless tagged [INFERENCE]. Quotes are single lines at the given line numbers; full numbered context is in receipts/*.excerpt.txt.
- The lane was not touched: no tracked-file edits, no git/jj commands against the lane, no mutation tests (research seat). Scratch `/fast/scratch/hyaku/mado-r55/R55W2ScoutCallers` is removed after this file and the seat report are written.

## 1. applyConfigToKeyboard

| Hop | Location | Quote | Status |
|---|---|---|---|
| Declaration | src/managers/input/InputManager.hpp:254 | `void               applyConfigToKeyboard(SP<IKeyboard>);` | OBSERVED |
| Definition | src/managers/input/InputManager.cpp:1213 | `void CInputManager::applyConfigToKeyboard(SP<IKeyboard> pKeyboard) {` | OBSERVED |
| Caller A | src/managers/input/InputManager.cpp:1195 | `    applyConfigToKeyboard(keeb);` | OBSERVED |
| Caller A enclosing function | src/managers/input/InputManager.cpp:1135 | `void CInputManager::setupKeyboard(SP<IKeyboard> keeb) {` | OBSERVED |
| Caller B | src/managers/input/InputManager.cpp:1208 | `        applyConfigToKeyboard(k);` | OBSERVED |
| Caller B enclosing function | src/managers/input/InputManager.cpp:1206 | `void CInputManager::setKeyboardLayout() {` | OBSERVED |

Whole-tree grep over the commit finds no third call site (src/ is the entire compositor; the `hyprctl` client speaks IPC, not C++). So applyConfigToKeyboard runs for exactly one keyboard at a time: on device setup, or from the setKeyboardLayout all-keyboards loop (:1207 `for (auto const& k : m_keyboards)`).

Caller A context (setupKeyboard, :1135-1204): the call at :1195 sits after the event wiring and `disableAllKeyboards(false);` (:1194) and before `g_pSeatManager->setKeyboard(keeb);` (:1197) and `keeb->updateLEDs();` (:1199). setupKeyboard is reached from three constructors:

| Path | Location | Quote | Status |
|---|---|---|---|
| Physical device (aquamarine event) | src/Compositor.cpp:474 | `        g_pInputManager->newKeyboard(dev);` | OBSERVED |
| — enclosing listener | src/Compositor.cpp:457 | `void CCompositor::initAllSignals() {` (listener `m_aqBackend->events.newKeyboard.listenStatic` at :473) | OBSERVED |
| Virtual keyboard protocol | src/managers/input/InputManager.cpp:90 | `        newVirtualKeyboard(keyboard);` (listener on `PROTO::virtualKeyboard->m_events.newKeyboard` registered at :89) | OBSERVED |
| newVirtualKeyboard → setupKeyboard | src/managers/input/InputManager.cpp:1130 | `    setupKeyboard(PNEWKEYBOARD);` | OBSERVED |
| newKeyboard(SP<IKeyboard>) → setupKeyboard | src/managers/input/InputManager.cpp:1114 | `    setupKeyboard(PNEWKEYBOARD);` | OBSERVED |
| newKeyboard(SP<Aquamarine::IKeyboard>) → setupKeyboard | src/managers/input/InputManager.cpp:1122 | `    setupKeyboard(PNEWKEYBOARD);` | OBSERVED |

The `newKeyboard(SP<IKeyboard>)` overload (:1111) has no caller inside src/ at this commit (grep `newKeyboard(` over the whole tree: only the aquamarine call at Compositor.cpp:474, the definitions and declarations). [INFERENCE] It exists for plugins or future internal use; whether any plugin calls it is UNVERIFIED (no plugin tree was fetched).

## 2. setKeyboardLayout

| Hop | Location | Quote | Status |
|---|---|---|---|
| Declaration | src/managers/input/InputManager.hpp:129 | `    void               setKeyboardLayout();` | OBSERVED |
| Definition | src/managers/input/InputManager.cpp:1206 | `void CInputManager::setKeyboardLayout() {` | OBSERVED |
| Body: all-keyboards apply | src/managers/input/InputManager.cpp:1207 | `    for (auto const& k : m_keyboards)` → :1208 `applyConfigToKeyboard(k);` | OBSERVED |
| Body: xkb state rebuild | src/managers/input/InputManager.cpp:1210 | `    g_pKeybindManager->updateXKBTranslationState();` | OBSERVED |

Five callers, all OBSERVED:

1. **Config reload, legacy parser (direct).** src/config/legacy/ConfigManager.cpp:977 `        g_pInputManager->setKeyboardLayout();` inside `CConfigManager::postConfigReload` (def :970), guarded by `if (!m_isFirstLaunch)` (:976). postConfigReload is called at the end of `CConfigManager::reload()` (:750 `postConfigReload(ERR.error || !monitorError.error ? ERR : monitorError);`, def :726). reload() is reached from (a) the config file watcher — init() def :1077, `Config::watcher()->setOnChange(...)` :1079, `reload();` :1081 — and (b) `hyprctl reload` — src/debug/HyprCtl.cpp:2028 registers `reloadRequest` (:1260), whose body runs `Config::mgr()->reload();` at :1274 (the `full-reset` variant re-inits the whole manager instead, :1262-1272).
2. **Compositor start, once.** src/config/supplementary/executor/Executor.cpp:49 `        g_pInputManager->setKeyboardLayout();` inside the `m_events.start` listener registered in `CExecutor::CExecutor()` (ctor :23, listener :24), after exec-once dispatch, guarded by `m_firstExecDispatched` (:25), comment at :48 `// set input, fixes some certain issues`.
3. **`hyprctl keyword` (legacy parser only).** src/debug/HyprCtl.cpp:1204 `        g_pInputManager->setKeyboardLayout();` inside static `dispatchKeyword` (def :1160), which is reached only by the legacy parser — guard :1162-1163: `return "keyword can't work with non-legacy parsers. Use eval.";`. The value is stored first by `mgr->parseKeyword(COMMAND, VALUE);` (:1190; legacy parseKeyword def src/config/legacy/ConfigManager.cpp:1089, `m_config->parseDynamic(...)` :1090), then the trigger is a NAME match at :1203: `if (COMMAND.contains("input") || COMMAND.contains("device") || COMMAND == "source") {`. Note the substring semantics: any command containing "input" or "device" trips it.
4. **`hyprctl -r <request>` (force flag).** src/debug/HyprCtl.cpp:2130 `        g_pInputManager->setKeyboardLayout();` inside `CHyprCtl::getReply` (def :2062) under `if (reloadAll) {` (:2126); the flag is set by the `r` character of a `/flags` request suffix (:2087-2088 `else if (c == 'r') reloadAll = true;`). This re-applies input configs after ANY hyprctl request, independent of the command.
5. **PropRefresher flag dispatch (see §3).** src/config/supplementary/propRefresher/PropRefresher.cpp:60 `        g_pInputManager->setKeyboardLayout();     // update kb layout` under the `REFRESH_INPUT_DEVICES` test (:59), inside `CPropRefresher::refreshProp` (def :55).

## 3. REFRESH_INPUT_DEVICES

| Hop | Location | Quote | Status |
|---|---|---|---|
| Flag definition (bit 1<<1) | src/config/supplementary/propRefresher/PropRefresher.hpp:11 | `        REFRESH_INPUT_DEVICES      = (1 << 1),` | OBSERVED |
| REFRESH_ALL = all bits | src/config/supplementary/propRefresher/PropRefresher.hpp:21 | `        REFRESH_ALL = std::numeric_limits<std::underlying_type_t<ePropRefreshProp>>::max(),` | OBSERVED |
| Handler (the only test of the bit) | src/config/supplementary/propRefresher/PropRefresher.cpp:59 | `    if (m_propsTripped & REFRESH_INPUT_DEVICES) {` → :60 `g_pInputManager->setKeyboardLayout();` (body also re-applies pointer/touch/tablet/tablet-tool, :61-64) | OBSERVED |
| Scheduler | src/config/supplementary/propRefresher/PropRefresher.cpp:29 | `void CPropRefresher::scheduleRefresh(PropRefreshBits prop) {` — ORs the bit (:31) and enqueues `refreshProp(true)` via doLater (:34-38) | OBSERVED |
| Immediate drain | src/config/supplementary/propRefresher/PropRefresher.cpp:44 | `int CPropRefresher::executeScheduledRefreshImmediately() {` | OBSERVED |
| Bits cleared after run | src/config/supplementary/propRefresher/PropRefresher.cpp:76-78 | `m_scheduled           = false;` / `m_scheduledRefreshSeq = 0;` / `m_propsTripped        = 0;` | OBSERVED |

Producers that schedule the bit (or a superset):

| Producer | Location | Quote | Status |
|---|---|---|---|
| Lua binding `hl.device{...}` (any evaluated device table) | src/config/lua/bindings/LuaBindingsConfigRules.cpp:1098 | `    Supplementary::refresher()->scheduleRefresh(Supplementary::REFRESH_INPUT_DEVICES);` (hlDevice def :1046) | OBSERVED |
| Lua binding `hl.config{...}`, per-key, dynamic parse only | src/config/lua/bindings/LuaBindingsConfigRules.cpp:1008 | `                        Supplementary::refresher()->scheduleRefresh(it->second->refreshBits());` (hlConfig def :969; guarded by `else if (self->isDynamicParse())` :1007) | OBSERVED |
| Per-option refresh mask source | src/config/values/types/IValue.cpp:18-19 | `Supplementary::PropRefreshBits IValue::refreshBits() const {` / `    return m_refreshProps;` | OBSERVED |
| Option flag: `input:numlock_by_default` | src/config/values/ConfigValues.cpp:277 | `MS<Bool>("input:numlock_by_default", "Engage numlock by default.", false, {.refresh = Supplementary::REFRESH_INPUT_DEVICES}),` | OBSERVED |
| Option flag: `input:repeat_rate` | src/config/values/ConfigValues.cpp:279 | `MS<Int>("input:repeat_rate", ..., 25, {.min = 0, .max = 200, .refresh = Supplementary::REFRESH_INPUT_DEVICES}),` | OBSERVED |
| Option flag: `input:repeat_delay` — **NO `.refresh`** | src/config/values/ConfigValues.cpp:280 | `MS<Int>("input:repeat_delay", "Delay before a held-down key is repeated, in milliseconds.", 600, {.min = 0, .max = 2000}),` | OBSERVED |
| Legacy full reload tail (superset REFRESH_ALL) | src/config/legacy/ConfigManager.cpp:1070 | `    Config::Supplementary::refresher()->scheduleRefresh(Supplementary::REFRESH_ALL);` (inside postConfigReload, def :970) | OBSERVED |
| Lua full reload tail (superset REFRESH_ALL) | src/config/lua/ConfigManager.cpp:850 | `    Config::Supplementary::refresher()->scheduleRefresh(Supplementary::REFRESH_ALL);` (inside lua postConfigReload, def :762) | OBSERVED |
| Immediate drain binding `exec_scheduled_prop_refresh_immediately` | src/config/lua/bindings/LuaBindingsToplevel.cpp:532 | `    return Supplementary::refresher()->executeScheduledRefreshImmediately();` (registered :548) | OBSERVED |
| Workspace rename / id change (superset REFRESH_ALL, adjacent) | src/desktop/Workspace.cpp:539, :558 | `    Config::Supplementary::refresher()->scheduleRefresh(Config::Supplementary::REFRESH_ALL);` | OBSERVED |

The lua-mode reload tail matters: the lua `postConfigReload` (def src/config/lua/ConfigManager.cpp:762) contains **no** direct `setKeyboardLayout` call (observed absence in :762-856), so under the lua parser a full reload re-applies input devices only through REFRESH_ALL → refreshProp. The legacy parser applies twice (direct :977 and via REFRESH_ALL :1070); the second pass re-reads unchanged values, so per keyboard it is expected to short-circuit at the unchanged-config early return the entry pins as K07 (:1271) — expected, not exercised: [INFERENCE].

Mechanism note (code shape, no runtime claim): `scheduleRefresh` only enqueues the doLater when `g_pEventLoopManager` already exists (:33); before that, a scheduled bit stays pending in `m_propsTripped` until some later scheduleRefresh flushes it.

## 4. WHEN the three options are re-applied (complete list at this commit)

For `input:repeat_rate`, `input:repeat_delay`, `input:numlock_by_default` (all read per keyboard by applyConfigToKeyboard at :1220, :1221, :1223; numlock also by IKeyboard::setKeymap at IKeyboard.cpp:120):

1. **New keyboard** — physical (Compositor.cpp:474 → newKeyboard :1122 → setupKeyboard :1135), virtual protocol (InputManager.cpp:89-90 → newVirtualKeyboard :1127 → setupKeyboard), or pre-built IKeyboard (:1114) → applyConfigToKeyboard at :1195. OBSERVED.
2. **Config file change / `hyprctl reload`, legacy parser** — watcher :1081 or reloadRequest :1274 → reload() :726 → postConfigReload :750 → direct setKeyboardLayout :977 (not on first launch, :976) plus REFRESH_ALL :1070 → refreshProp :60. OBSERVED.
3. **Config reload, lua parser** — reload → postConfigReload :762 → REFRESH_ALL :850 → refreshProp :60 only. OBSERVED (absence of direct call).
4. **`hyprctl keyword input:... value`, legacy parser only** — dispatchKeyword :1160 → parseKeyword :1190 stores the value → name-match :1203 → setKeyboardLayout :1204. Covers all three keys (substring "input"), any device block key (substring "device"), and `source`. OBSERVED.
5. **Dynamic config sets (lua parser: `hyprctl eval` / `repl`, HyprCtl.cpp:1110/1119, or dynamic lua config parse)** — hl.config per-key schedules the option's own refreshBits (:1008); hl.device always schedules REFRESH_INPUT_DEVICES (:1098) → refreshProp :60. This re-applies `numlock_by_default` (:277) and `repeat_rate` (:279). **`repeat_delay` declares no `.refresh` (:280), so a dynamic set of repeat_delay alone schedules no input refresh** and the value sits until the next full reload (REFRESH_ALL). The declarations and the mechanism are OBSERVED; the runtime consequence for repeat_delay is [INFERENCE] (not exercised on a running compositor).
6. **`hyprctl -r <any request>`** — getReply :2062, flag :2087-2088, `if (reloadAll)` :2126 → setKeyboardLayout :2130. OBSERVED.
7. **Compositor start, once** — Executor start listener :24 → setKeyboardLayout :49. OBSERVED.

Nothing else: no other caller of either function exists in the tree at this commit (whole-tree grep). In particular there is no re-apply on VT switch, on keymap events, or on device *removal*.

## 5. What the entry says, and whether it is right

Entry: corpus/knowledge/hyprland-keyboard-repeat-numlock-r55.md.

- Chain step 3 / E08 says: "applyConfigToKeyboard is called from setupKeyboard (E08)", E08 pinning InputManager.cpp:1195 `` `applyConfigToKeyboard(keeb);` `` and calling it "one of the callers".
  - SURVIVES. The quote is at :1195, the enclosing function is setupKeyboard (def :1135), and "one of the callers" is exactly right: the only other caller is the setKeyboardLayout loop (:1208).
- The entry is otherwise SILENT on reapplication. Precise greps over the entry file return no matches for `reload`, `refresh`, `keyword`, `setKeyboardLayout`, `dispatch`, `REFRESH_INPUT` (this seat's transcript; the two `reload`/`refresh` greps: "No matches found").
  - Coverage gap, not a broken claim: the entry answers "when re-applied" only for the device-setup path. §4 above is the complete map the entry could absorb, all at the same pinned commit, with the three line anchors the entry already pins (1195, 1206-1208, 1213, 1220-1223) byte-identical to the lane's fetch dir.
- New adjacent facts worth the entry author's attention (none are entry claims today):
  - Four further reapplication routes: reload (two parser modes, two mechanisms), `hyprctl keyword` (legacy only, name-substring trigger), dynamic/lua sets via refreshBits, `hyprctl -r`, plus the once-at-start executor call.
  - The `repeat_delay` asymmetry: has no `.refresh` flag (ConfigValues.cpp:280) while its two siblings do (:277, :279) — under the dynamic/lua path it is the one key of the three that is not re-applied until a full reload. [INFERENCE at runtime level]
  - Legacy reload applies input config twice (direct + REFRESH_ALL); harmless given the K07 gate, but a writer describing the reload path should know it.

## Receipts

- receipts/fetch-provenance.txt — source, commit, date, method, pin-identity results, lsp unavailability.
- receipts/SHA256SUMS-fetched.txt — sha256 of every cited file.
- receipts/*.excerpt.txt — numbered excerpts for every quote above (InputManager.cpp/.hpp, HyprCtl.cpp, legacy- and lua-ConfigManager.cpp, PropRefresher.cpp/.hpp, Executor.cpp, LuaBindingsConfigRules.cpp, LuaBindingsToplevel.cpp, ConfigValues.cpp, Compositor.cpp).
