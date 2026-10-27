# C2SourceCritic — round-51 dispatcher entry source-truth critique + independent fact surface

Axes: coverage + operability. Claim under attack: **C2** (coverage: proposition-bound dispatcher
source entry). No claim or predicate edits; source-only round; no live reads, no host probes.

Method: every evidence claim in `corpus/knowledge/hyprland-dispatcher-dispatch-r51.md` (including
its round-51 w2 Errata) and every held-ground link was re-derived against the pinned bytes in
`.ufo/waves/round-51/fetch/` at pin `efb50993780079460b0cbed1363e2166a2de1d9f`. Line numbers below
are line numbers in those pinned files. Strongest available counterexamples were tested first.

## Pin integrity (precondition)

`sha256sum -c .ufo/waves/round-51/fetch/SHA256SUMS` from the lane root: **20/20 source pins OK**.
One failure: the manifest's self-referential entry
(`SHA256SUMS` recorded as `ab6c7355…`, actual `700fea66…`) — the manifest lists its own checksum
and does not match itself; all 20 fetched source files verify. Provenance note only; no pin
content is in doubt. The entry's own digest block (KeybindManager.cpp `8d8f35fc…`,
DispatcherTranslator.cpp `7248cbb8…`, HyprCtl.cpp `798b7c6c…`, ConfigActions.cpp `a83abeb5…`) matches
the verified pins.

## Verdict map (claims attacked, evidence, result)

| # | Entry claim (location in entry) | Attack | Result |
|---|---|---|---|
| 1 | Step 1: constructor brace list runs `{`exec`,` (:42) → `releaseinputcapture` (:112); all 71 names get the forwarding closure (:113) | Read full constructor :36–114; counted names :42–112 | **SUSTAINED.** 71 names, single assignment at :113. (First candidate counterexample tested and falsified.) |
| 2 | Step 1: both tables carry the same 71 names "in different order"; inner refusal unreachable from a keybind | Set diff + ordered diff of `m_dispatchers` names (:42–112) vs `m_dispMap` names (:797–867) | **SUSTAINED.** Sets identical (71/71); ordered diff shows exactly one placement difference (`moveintoorcreategroup`). `Bad dispatcher` at DispatcherTranslator.cpp:31–32 is unreachable from a keybind given the parse-time check at legacy-ConfigManager.cpp:1594–1598. |
| 3 | Step 1/2: map type hpp:137; HANDLER :1584, COMMAND :1586, `HANDLER = "mouse"` :1589, tolower :1592, find :1594, miss message :1598, stored :1624–1631, submap :1633, keyword write :1797–1798 | Read all cited lines | **SUSTAINED** (all exact; addKeybind spans :1624–1633, HANDLER :1630, COMMAND :1631, `m_currentSubmap` :1633). |
| 4 | Step 3: press lookup :785 (mouse rewrite), log :799, timers :131/:154, timer lookups bypass the rewrite | Read :118–157 and :770–851 | **SUSTAINED.** Long-press :128–131, repeat :145–156; both look up raw `k->handler` / `m_lastLongPressKeybind->handler`; neither writes `m_passPressed`. |
| 5 | Step 4: write :804, clear :814, hpp:114 three-valued comment, arg call :812, mouse prefix :810, strip :676, defaults SharedDefs.hpp:53–55, `res.passEvent \|= !found` :842, inhibitor :845–851 | Read all cited lines | **SUSTAINED** (all exact). |
| 6 | Step 5: `.submapAtPress` :396, `getCurrentSubmap` :599, SSubmap defaults hpp:25–26, gate :652, reset/empty write :1666, scan+named write :1674, refusal :1681, both breaks :775–778 and :816–819, reset-after-dispatch :820–823 | Read all cited lines | **SUSTAINED** (all exact). |
| 7 | Step 6: pass at ConfigActions.cpp:1465; branches :1487/:1492; both-edges :1499–1500; `:386` last-code write; special-dispatcher expression :782; emplace :795; erase :793; global :1634; mouse :1640/:1643 | Read all cited lines | **PARTIALLY SUSTAINED — see Attack B.** :1465/:1487/:1492/:1634/:1640/:1643 exact. Both-edges branch: `} else {` is at **:1497**, edges at :1500–1501; entry cites :1499–1500 (off-by-one on the second line, content true). |
| 8 | Step 7: five argument readings — sendshortcut :532–535, setprop :773, alterzorder :684, mouse :676, **exec :48–51** | Read all cited regions | **DEFECT — see Attack A.** Four locators exact; exec locator points at `windowFromArg`, not `exec`. |
| 9 | Step 8: registration :2036, strip :1128, Lua branch :1130–1141, first-space split :1143–1147, find :1149, `Invalid dispatcher` :1151, call+reply :1153–1157 | Read :1126–1158 and :2030–2040 | **SUSTAINED** (all exact). |
| 10 | Step 9 (post-errata): source-level Lua guard exists and returns before the table; host-branch claim withdrawn | Lua branch verified at :1130–1141; errata text present | **SUSTAINED as corrected.** Errata properly withdraws the running-host branch conclusion. |
| 11 | Held links: bind-table-r25.md:38/:52; keybind-rule-semantics.md:73/:55; dispatcher-surface-and-request-grammar-r26.md:48; hyprland-bind-key-match-r50.md:57; hyprland-config-era-r12.md:41 | Read each cited line | **SUSTAINED.** All seven held lines exist and say what the keys claim (rule-semantics:55 carries "`submap` is `""` on all 192 (no submaps in the plane)"; era:41 carries the `hyprland.lua`-selects-Lua row). |
| 12 | Census line: `special_handlers=5`; step 6 body: "one of the five names the press path handles specially" | Compare against entry's own Errata | **DEFECT — see Attack C.** Errata says the :782 expression names four dispatcher strings plus a boolean; the step 6 sentence and census count were never updated. |

## Attack A — step 7 exec locator is false (item attacked: step 7, "exec" bullet)

Entry: "`exec` does not split at all and hands the tail to the process executor
(Hyprland-legacy-DispatcherTranslator.cpp:48-51)".

Evidence: pinned DispatcherTranslator.cpp:45–49 is the `windowFromArg` helper
(`if (arg.empty() || arg == "active")`). The `exec` dispatcher is at **:65–70**
(`static SDispatchResult exec(const std::string& args) {` :65,
`Config::Supplementary::executor()->spawn(args);` :66). Claim content is true (the tail is handed
over whole); the locator does not show it. The w2 Errata re-audited step 7 but missed this one.

Impacted axis: coverage (a C2 counter binding quotes to pins would reject the 48–51 pin range for
this proposition). Smallest safe correction: change `48-51` to `65-70`; no wording change.

## Attack B — step 6 sendkeystate citation targets a table-unreachable function (item attacked: step 6, sendkeystate sentence)

Entry: "`sendkeystate` is the one dispatcher that writes the field itself, saving and restoring it
around its work (Hyprland-ConfigActions.cpp:1603-1615)".

Evidence: the cited lines are `Actions::sendKeyState` (ConfigActions.cpp:1601–1618), declared in
ConfigActions.hpp:64. Within the pinned tree it has **no caller**; the dispatch table entry
`m_dispMap["sendkeystate"] = ::sendkeystate;` (DispatcherTranslator.cpp:842) resolves to the
static dispatcher `::sendkeystate` at **DispatcherTranslator.cpp:591–627**, which does its own
save/override/restore (`const int oldPassPressed = …` :612, `m_passPressed = 1` :615, `= 0` :617,
restore :624) and then delegates to `sendshortcut(modifiedArgs)` at :619/:622 — never to
`Actions::sendKeyState`. So the quoted lines do not establish the claim about the table-reachable
path; the true mechanism lives one file over. What survives: among the 71 dispatcher
implementations, `sendkeystate` is indeed the only table-reachable writer of `m_passPressed`
(writer census across all pins: KeybindManager.cpp:804/:814 press path; ConfigActions.cpp:1606–1615
uncalled within pins; DispatcherTranslator.cpp:615–624 sendkeystate).

Impacted axis: coverage (quote-to-proposition binding would mis-bind). Smallest safe correction:
cite DispatcherTranslator.cpp:612–624 for the dispatcher claim (optionally noting the uncalled
action-level twin at ConfigActions.cpp:1601–1618).

## Attack C — residual "five special handlers" contradicts the entry's own Errata (item attacked: step 6 first sentence + census line)

Errata: "The expression at KeybindManager.cpp:782 names four special dispatcher strings … and also
tests the boolean releasePending; it is not five special dispatcher names." But step 6 still reads
"`pass` is one of the five names the press path handles specially" directly above the quote that
lists four, and the census still prints `special_handlers=5`. The errata says corrections
"supersede the earlier wording", so a reader can reconcile — but the uncorrected sentence and
census are exactly the kind of surface a round-52 proposition-counter must not transcribe.
Smallest safe correction: "five names" → "four names and a releasePending flag"; census `5` → `4`.

## Independent dispatcher fact surface (candidate grounding for the frozen C2 entry)

Distinctness: round-51's entry covers bind storage, the press path, the submap/`pass` handlers, and
the socket verb. Its Limits bullet 2 explicitly abandons repeat/long-press as `[INF]` ("neither
callback writes the press field, and whether `pass` accepts being combined with the repeat or
long-press flags at all was not traced"). The surface below is that abandoned trace, completed:
**the two event-loop timer callbacks are a third and fourth ingress into the same 71-name
`m_dispatchers` table, with different registration, cancellation, guard, and result-folding
semantics than either the press path or the socket verb.** All lines are in already-pinned files
(S364's `Hyprland-KeybindManager.cpp`, S368's `Hyprland-legacy-ConfigManager.cpp`, S367's
`Hyprland-ConfigActions.cpp`); no new fetch was needed and none was made. (Per the frozen
predicate these are candidate propositions for the author/executor seats to adopt or reject; this
report claims no entry and no row.)

Candidate propositions, each with a ≤25-word located quote and support rationale:

- **P1 — A long-press bind is not dispatched at press.** The match loop arms the timer with the
  keyboard's own repeat delay, records the bind, and `continue`s past hit collection
  (KeybindManager.cpp:764–770). Quote (:767–768): "m_longPressTimer->updateTimeout(
  std::chrono::milliseconds(PACTIVEKEEB->m_repeatDelay)); m_lastLongPressKeybind = k;" — rationale:
  the `continue` at :770 precedes `bindsHit.emplace_back(k)` at :773, so the bind never enters the
  press dispatch loop.

- **P2 — Every key event cancels both pending timer dispatches before matching.** Quote
  (KeybindManager.cpp:401/:403): "m_activeKeybinds.clear(); m_lastLongPressKeybind.reset();" —
  rationale: both statements sit at the top of the key-event handler (:398–403) before the match
  loop, so release-before-delay suppresses the long-press dispatch and any key event stops a
  repeating bind.

- **P3 — Repeat re-dispatch cadence is the keyboard's own rate/delay.** Registration quote
  (KeybindManager.cpp:827–832): "if (pressed && k->repeat) { … m_repeatKeyRate =
  KEEB->m_repeatRate; … m_repeatKeyTimer->updateTimeout(…m_repeatDelay); }" and cadence quote
  (:156): "self->updateTimeout(std::chrono::milliseconds(1000 / m_repeatKeyRate));" — rationale:
  per-keyboard values, not config-global; a repeat bind is also dispatched normally at press (it
  remains in `bindsHit`), the timer only re-dispatches.

- **P4 — Neither timer callback writes `m_passPressed`, so a timer-fired `pass` takes the
  both-edges branch.** Evidence: the full writer census across all pins lists only
  KeybindManager.cpp:804/:814 (press path), ConfigActions.cpp:1606–1615 (uncalled within pins),
  DispatcherTranslator.cpp:615–624 (sendkeystate); the callbacks at KeybindManager.cpp:118–157
  contain none. The both-edges branch quote (ConfigActions.cpp:1497–1500): "} else { …
  sendKeyboardKey(S.m_timeLastMs, S.m_lastCode - 8, WL_KEYBOARD_KEY_STATE_PRESSED);" — rationale:
  with the field at its `-1` default (ConfigActions.hpp:114), `pass` falls through both `== 1`
  (:1487) and `== 0` (:1492) tests into the branch that sends press and release in one call.

- **P5 — Parse law places no bar on combining `pass` with repeat or long-press.** Quote
  (legacy-ConfigManager.cpp:1545–1552): "(longPress || release) && repeat … mouse && (repeat ||
  release || locked) … click && drag" — rationale: the only flag-conflict checks involve repeat
  vs longPress/release, mouse vs repeat/release/locked, and click vs drag; nothing excludes a
  `pass` bind carrying `r` or `e`. P4's consequence is therefore parse-reachable, not
  counterfactual — which retires round-51's `[INF]` hedge ("whether `pass` accepts being combined
  with the repeat or long-press flags at all was not traced").

- **P6 — Timer dispatches bypass every press-path side effect.** The long-press callback
  (KeybindManager.cpp:121–131) has no `m_passPressed` write, no submap break, no
  `found`/`res.passEvent` folding (:842) and no inhibitor check (:845–851); its lookup uses the raw
  stored handler with no mouse rewrite (:128, contrast :785). Quote (:128–131): "const auto
  DISPATCHER = g_pKeybindManager->m_dispatchers.find(m_lastLongPressKeybind->handler); …
  DISPATCHER->second(m_lastLongPressKeybind->arg);" — rationale: a timer-fired dispatcher result
  cannot mark the event consumed, cannot be flipped by an inhibitor, and cannot switch submaps via
  the :820–823 reset path (that path lives in the press loop).

Secondary surfaces (noted for the record, not developed): the `sendkeystate` dispatcher itself
(DispatcherTranslator.cpp:591–627) is a sixth argument-grammar reading beyond round-51's five and
the only table-reachable writer of the press field (see Attack B); the mouse-bind mode machine
(`changeMouseBindMode`, KeybindManager.hpp:151, ConfigActions.cpp:1643–1660) is an unexplored
state machine behind the `mouse` name.

## Dissent and honest limitations

- Counterexample #1 (constructor population) was my strongest candidate defect and it **failed**:
  the 71-name claim is exactly right. Reported so the author seats do not re-litigate it.
- Attack A and Attack B are locator/provenance defects against true claim content; Attack C is an
  internal inconsistency the Errata missed. None reaches the w2 Errata's severity (the Errata's
  withdrawn claims — comma preservation, config-time `sendshortcut` error, host branch — are
  correctly withdrawn and I found no residue of them in the standing text).
- `Actions::sendKeyState` "uncalled" is asserted **within the pinned files only**; the unpinned
  Lua config path (`src/config/lua/`) was not read this round (source-only safety boundary), so a
  Lua-side caller cannot be excluded.
- All line numbers were verified against the pinned bytes at `efb50993`; nothing was executed,
  pressed, or dispatched; no host, process, or compositor state was read.
- No package installs were needed (none performed). Scratch:
  `/fast/scratch/hyaku/mado-r52/C2SourceCritic/` (working comparison files only, removed on
  exit; nothing copied into the lane).

# C2SourceCritic — source-truth critique of round-51 dispatcher entry; independent timer-ingress fact surface identified

Axes: coverage + operability.

## Deliverables
- `.ufo/waves/round-52/w1/C2SourceCritic.md` — this report (attacks A–C with exact pinned lines; six candidate propositions P1–P6 for the C2 entry's independent dispatcher fact surface).

## Finding
**Entry mostly source-true; three defects found.** Attack A: step 7 `exec` locator `DispatcherTranslator.cpp:48-51` points at `windowFromArg`; true site is `:65-70` (content true). Attack B: step 6 `sendkeystate` citation targets `Actions::sendKeyState` (ConfigActions.cpp:1601-1618), which the dispatch table never calls; the table-reachable dispatcher is `::sendkeystate` at DispatcherTranslator.cpp:591-627 (save/restore :612-624). Attack C: step 6 "five names" and census `special_handlers=5` contradict the entry's own Errata (four names + `releasePending` boolean). All other cited lines (steps 1-5, 8; seven held links; both 71-name tables) verified exact against verified pins. Independent fact surface: the repeat/long-press timer ingresses (P1-P6), which round-51 left `[INF]`, are fully source-grounded in already-pinned files. This report attacks evidence quality only; it does not amend the frozen C2 predicate.

## Verification gap
Line-level reads of pinned files only; `src/config/lua/` not read; no runtime dispatch or host observation performed.
