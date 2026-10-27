# C2 dispatcher entry — source-locator truth audit

Scope: `corpus/knowledge/hyprland-dispatcher-dispatch-r51.md` against exact pinned bytes under `.ufo/waves/round-51/fetch/`. This is source truth review, not runtime testing. Axes: coverage + operability. No code/runtime or lane edits made.

## Verdict

**MISS (source-truth support incomplete).** Most main mechanisms are corroborated by cited pinned lines. However, the fixed-field bind parsing and preserved-tail/comma behavior are claimed more strongly than the S368 source locator permits; the entry's own Limits section concedes the splitter implementation evidence is unregistered. Several claims extrapolate from narrow citations to universal behavior. This is content/evidence failure; it does not alter or re-score the frozen C2 lexical predicate.

## Source locator-by-locator review

### Intro and source block (entry lines 1–24)

- Lines 3–8 are framing/editorial scope, not independent Hyprland mechanism claims.
- Lines 10–12: socket split is supported by `Hyprland-HyprCtl.cpp:1143-47`; dispatcher-specific argument reading is demonstrated at translator `:532-35, 676, 684-85, 773, 48-51`. For binds, `ConfigManager.cpp:1554-55` creates capped `CVarList`, `:1584-89` extracts/assigns fields, and `:1624-33` stores them. The “bind path never splits its argument” and raw-byte preservation depend on CVarList behavior, not proven by cited S368 locator `:1580-1601`; the entry itself says in Limits `:301-307` it did not use the unregistered Hyprutils VarList2 source as a claim. Held `bind-table-r25.md:38` and `keybind-rule-semantics.md:73` provide indirect grounds, but exact pin support for the splitting operation is missing from the sourced claim. This is the most substantive source-truth shortfall.
- Source block rows S364–S369 (lines 14–19) have accurate IDs/pins/quote locators: see registry `corpus/SOURCES.md:313-318`. Their descriptions are synopsis, not blanket support for every later statement.
- Line 20/24 state held provenance/editorial boundaries rather than new source mechanisms.

### Step 1, table population and translator (90–106)

- `KeybindManager.cpp:42-112` lists the outer names; `:113` installs the common forwarding closure. `KeybindManager.hpp:137` gives map type. Translator header `:19`, implementation `:797-867`, and `:31-34` support the inner map, table fill, rejection, and call.
- “both lists carry the same 71 names in different order” is a comparison/census, not a directly quoted line fact. Listed ranges allow checking it but no calculation/receipt is cited at this sentence. Evidence is plausible but not immediately reproducible as written.
- “inner refusal cannot be reached from a keybind” is properly narrowed only for normal config-accepted keybinds: parse-time outer lookup is `ConfigManager.cpp:1594-98`; however, “only from a caller that names the translator directly” claims exhaustive caller knowledge that these citations do not establish. It should be understood as an inference, not a source fact.

### Step 2, bind field extraction and validation (108–123)

- `ConfigManager.cpp:1584,1586,1589,1592,1594,1596-98,1624-33` support handler position, ordinary argument selection, mouse replacement, lowercasing, validation/rejection, and aggregate storage.
- The “argument keeps its bytes” / no-comma-touch statement is not proved by the quoted assignment alone; it rests on held capped-split knowledge and the absent splitter-source check above. Also, mouse mode assigns `COMMAND = HANDLER`, then replaces HANDLER with `mouse`; so the mouse action originally occupying the handler field becomes the argument. The narrative does describe this.
- “unknown one never reaches a key press” is supported for parsed config binds by parse rejection and the active path. Later line 129 correctly notes a miss is logged in dispatch, but the config-time validation guarantee presumes no other construction path creating invalid keybinds; citations do not establish all constructors.

### Step 3, direct press/timer branches (125–135)

- Mouse lookup rewrite is exactly `KeybindManager.cpp:785`. The log-only miss path is `:797-800`. Timer calls with stored args are at `:128-132` and `:147-155`, so the mechanism is sourced.
- “why an m-flag bind reports mouse in hyprctl binds” is not established by `:785`; that line changes the dispatch lookup key, not the serialization/reporting of `hyprctl binds`. The claim needs a bind-list serialization source locator or should be removed. This is a concrete source-locator mismatch.
- The repeat/long-press pass replay consequence is explicitly `[INF]`, so no finding against its labeling; the callbacks omit `m_passPressed` assignment, while normal dispatch writes/clears at `:804-14`. However `pass` bind eligibility/flag combinations were not traced (entry Limits :288-90), appropriately disclaimed.
- Caveat: the repeat path lookup uses `k->handler`, not mouse override. Mouse binds cannot combine repeat under `ConfigManager.cpp:1548-49`, so no demonstrated counterexample to that restricted path.

### Step 4, callback values/results (137–155)

- Normal path write/clear and argument calls are `KeybindManager.cpp:804,810-14`; `SharedDefs.hpp:52-55` confirms default fields. `setignoregrouplock` empty result is translator `:861`; `res.passEvent |= !found` is KbManager `:842`, inhibitor mutation `:844-50`.
- “a dispatcher that returns nothing counts as a success that does not swallow the event” correctly describes default-constructed `SDispatchResult`, though `found`/consumption remains caller logic as the next sentences show.
- The phrase “what the callable receives. Two things” is underspecified: it identifies state and string; citation support is present.

### Step 5, submap behavior (157–178)

- Captured bind submap is `ConfigManager.cpp:1633`; current submap keyword write is `:1795-99`; press event copy `KbManager.cpp:391-98`; read accessor `:598-600`; SSubmap defaults `KeybindManager.hpp:24-29`; filter `KbManager.cpp:652`. These support capture/read/gate.
- “At dispatch time the only writer is the submap action” overstates cited evidence. `ConfigActions.cpp:1664-82` is the setSubmap implementation, but the entry itself later identifies another writer: bind reset path `KeybindManager.cpp:820-23` (which invokes setSubmap). The state assignment may still be centralized in setSubmap; but “only writer is the submap action” should distinguish direct assignment sites from calls that effect reset. The cited lines show both reset path and action, so current wording can mislead.
- The reset/empty and named write/refusal behavior is accurately supported by `ConfigActions.cpp:1664-82`.
- “submap therefore exists because some bind named it” is too broad: `setSubmap` scans `m_keybinds` for any `k->submap.name == submap` (`:1672-74`), so it requires a registered bind under that submap; not necessarily a “bind named it” in a unique causal/config sense. More importantly, direct reset/empty forms can set empty without such bind. The prose scopes named form but sentence is broad.
- Both “break” rules are evidenced at KbManager `:775-78` and `:816-19`; they support lone dispatch behavior for submap handler hits. Reset behavior is supported at `:820-23`.

### Step 6, pass/mouse/special handlers (180–199)

- The actual `Actions::pass` implementation at ConfigActions `:1465-1505` supports selector-resolved window, focus changes, modifier resend, and press/release/both branches. Branches depend on `m_passPressed` as cited. Event-code source `KeybindManager.cpp:386` records key code; pointer variant uses last mouse code, also action lines :1501-03.
- “pass is one of five names the press path handles specially” is literally off: `SPECIALDISPATCHER` expression at `KeybindManager.cpp:782` names four dispatcher strings (`global`, `pass`, `sendshortcut`, `mouse`) plus the boolean condition `k->releasePending`. It is not five special handler names. This is a concrete wording/count defect.
- Remember/remove citations `:792-95` support special-bind tracking. `global` forwards marker at ConfigActions `:1634`; `mouse` reads marker at `:1639-43`; `sendkeystate` save/restore is translator `:612-24` (not ConfigActions :1603-15, which is Actions::sendKeyState, also valid for the parallel implementation). “one dispatcher that writes the field itself” is false/overstated: sendkeystate is one dispatcher, but it is not the only code that writes the field (the normal press path itself writes it at `KeybindManager.cpp:804,814`; wording context likely means special handler). Qualify as one of the dispatchers that overrides it.
- “mouse ... degrading to MBIND_INVALID otherwise” is supported by ConfigActions `:1640-43`; it accurately covers socket call with default marker only if default remains `-1` and no pre-existing state is altered; entry treats this as code inference.

### Step 7, dispatcher argument parsing (201–216)

- Individual implementations support the listed mechanics: sendshortcut `DispatcherTranslator.cpp:531-35`; setprop `:772-75`; alterzorder `:683-85`; mouse `:675-77`; exec `:48-51`. Line ranges are accurate.
- “sendshortcut ... rejects a fourth comma in its tail” needs care: parser checks CVarList2 size exactly 3; its comma-splitting behavior is evidenced by CVarList2 constructor call, but whether the splitter preserves/truncates separators is not shown in Hyprland source. Limits `:301-307` admits `VarList2::construct` behavior was only inspected in an unregistered pin. “config-time error” is incorrect: this is a dispatcher runtime return error, not config parsing. Concrete factual error: the `sendshortcut` call is through key/socket dispatch; its `.success=false` result and `sendshortcut: invalid args` are dispatcher-time, not config-time. The citations at `:532-35` do not establish config-time rejection.
- `setprop takes three space-separated fields and rejoins what follows` is supported by `CVarList2(args,3,' ')` at `:773`, with size check :774-75. “rejoins” requires helper semantics not included in cited Hyprland source.
- `alterzorder` uses `find_first_of(',')` and substrings, exactly at `:683-85`; it may not be described as a robust single split where comma absent without considering npos arithmetic; current “cuts once at first comma” is a fair source-level description.
- mouse strips one character, `:675-77`; exec direct tail is `:48-51` (would be stronger with function signature/body already in source pin). Claim about same shape refusing by sendshortcut is subject to above runtime-vs-config error and delimiter semantics caveat.

### Step 8, socket entry (218–232)

- Registration at HyprCtl `:2036`; strip at `:1126-28`; Lua branch/early return `:1130-41`; legacy split `:1143-47`; lookup/refusal/call/reply `:1149-57` are exact supporting lines. “one-line reply” from `return` expression is supported as output string, though transport framing is not cited.
- “same table” is direct: both bind path and socket access `m_dispatchers`; “same dispatcher sees same string” is conditional on same dispatcher and same textual arg, not an unconditional equivalence of binds and socket inputs.
- `m_passPressed` default is ConfigActions.hpp `:114`, socket path no write is apparent in `dispatchRequest` :1126-58; same table call. But “always takes both-edges branch” is not universally guaranteed by these lines alone: a dispatcher such as `sendkeystate` overrides the marker and restores its prior value, while `pass` itself follows the three-way branch. For `pass` specifically, `m_passPressed` could be pre-existing non-default process state because socket dispatch does not set/clear it; default `-1` is an initialization default, not proof that it is still -1 at arbitrary socket invocation. Thus “always” exceeds evidence and may be false if invoked reentrantly/during another dispatch; at minimum state that on ordinary idle path it uses default `-1`. The socket call's synchronous same-process operation and asynchronous reentrancy are not explored, so no runtime counterexample asserted.
- Socket `mouse` degrades if `m_passPressed != 1`, supported by `:1640-43`, but the same stale/non-default state caveat applies; also `mouse` action may parse its argument only after this guard, supported.
- Socket submap limitation supported by setSubmap scan/refusal `ConfigActions.cpp:1672-81`, but empty/reset exception exists (`:1665-69`): “a submap switch ... still has to name a submap some bind carries” is true only for nonempty named targets. Empty/reset bypasses the scan; clarify the scope.

### Step 9, host branch and docs contrast (234–243)

- Lua type guard exists at HyprCtl `:1130`; config-era held line `hyprland-config-era-r12.md:40-47` is a documentation rule (not source code). The directory-listing claim is an observation, not source citation. No cited source proves this host's live manager type; the entry labels this a host observation/inference.
- The specific inference “directory has no lua so the running manager is legacy” omits explicit-config-path and process-start timing caveats already stated in held config-era source (`:43,47`) and later in that same entry (`:42` restart requirement). A config-directory listing alone cannot prove which file a running compositor selected if it was launched with explicit config path or files changed since startup. The stated fact that a `.conf` exists plus no `.lua` does not rule out explicit startup config path. This is a material unsupported host conclusion; no runtime introspection receipt is cited in this article.
- Wiki contrast locators are pin lines but not registry rows, correctly disclosed. The claim that those docs describe only the other branch must be verified against exact pin lines; no defect established in this review because the fetched wiki pin ranges were not opened here.

### State table and observations (245–280)

- State claims table setter citations mostly point at appropriate writes, with `SKeybind::arg` aggregate value cited through `:1586` and `:1624-31`, `m_currentSubmap` setters at ConfigActions `:1666,1674`, `m_lastCode` assignment at KbManager `:386`.
- Row `m_passPressed` says `1 press, 0 release, -1 between`; code writes 1/0 before call and -1 after it (`KbManager.cpp:804,814`), but “between” default also supported by header. It elides `sendkeystate` temporarily overriding it, discussed above.
- OBS lines 261–276 each contain a valid cited exact line and generally accurate scope. “three distinct failure strings for a bad name, one per path” is slightly simplified: config parse error, direct translator `Bad dispatcher`, socket `Invalid dispatcher` are distinct contexts, but no universe of all call sites is proven. `return nothing success` supported by default `success=true`; passEvent false is S369 default.
- Census at 278–80 is a measured count, not independently evidenced by the cited source lines alone; the entry does provide the finite ranges elsewhere, but no calculation receipt here.

### Limits (282–316)

- Limits appropriately disclose no runtime dispatch, inferred repeat/long-press consequence, only five dispatcher readers examined, missing VarList2 registry row, unexamined Lua implementation, and socket submap not exercised.
- Lines 301–307 explicitly acknowledge the key source gap: hyprutils VarList2 implementation has no registry row and is not used for claim. This directly conflicts with presenting line 10–12 and line 213–15 as sourced fact that bind tail commas survive / sendshortcut rejects fourth comma, rather than distinguishing held-ground evidence from direct pinned source truth.
- Lines 314–16 correctly distinguish no host receipt for socket submap, but earlier step 8's unconditional “still has to name” omits reset/empty exception.

## Highest-priority concrete defects

1. **Runtime/config-time confusion:** step 7 line 205 calls `sendshortcut` invalid-args result a “config-time error”; code `DispatcherTranslator.cpp:531-35` returns `SDispatchResult{success=false}` from dispatcher execution. No config-time parse rejection is shown. This is definitively unsupported/incorrect.
2. **Wrong special-handler count:** step 6 lines 187–90 says five names, while cited expression has four named dispatchers plus `releasePending` boolean (`KeybindManager.cpp:782`).
3. **Mouse bind report citation mismatch:** step 3 line 128 attributes `hyprctl binds` reporting to dispatch lookup line 785; that line only chooses the called map key. A bind JSON serialization citation is needed.
4. **Socket pass “always” claim:** step 8 lines 228–30 infers the marker remains `-1` from absence of assignment in dispatch request. `-1` is a default in the action-state struct, not a per-call guarantee; the exact code only proves dispatchRequest itself does not write it. Qualify as idle/default-state inference.
5. **Submap named-target scope:** lines 170–71 and 231–32 omit empty/reset paths, which write empty without a registration scan (`ConfigActions.cpp:1665-69`); named target refusal is what `:1672-81` establishes.
6. **Host branch not proven by directory list alone:** step 9 lines 234–40 does not exclude explicit launch config or files changed after process startup; held config-era source explicitly scopes the no-file rule to default selection and says choice is not re-detected in-process (`hyprland-config-era-r12.md:42-47`).

## Verification gaps

No LSP device is mounted (`xd://lsp` returned “No such tool”), so no semantic references/definition/diagnostics were available; source lines were read from the frozen pin files. No runtime dispatch or live state was executed. This review does not assert whether the host fact in step 9 is false, only that its cited evidence is insufficient for the unrestricted running-manager conclusion.