# Attack16 — W2 attack #16: C2 source claims versus runtime/host inference

Seat: `Attack16` (scout, leaf; no subagent dispatch). Wave `w2`, round 52, lane `mado-shokunin`.
Base `85d57a818c3707397e21c840b6498b105ba798aa`. Attacked claim: **C2 — coverage:
proposition-bound dispatcher source entry** (`claims-frozen.md` C2; `registration.md` C2).

Scope of this seat: the C2 candidate entry makes a family of claims about what the code does at
runtime — what a synthetic event "carries", what the seat "receives", what "targets whatever is
focused", how the argument split "caps". This round is source-only (no live reads, no probes, no
host mutation), so every runtime-behavior claim must be established by the pinned bytes or it is
inference. I attack each such claim against the pinned source and the pinned dependency bytes,
with compiled reproduction where semantics are in question.

Attacked artifacts (all read-only):

- Candidate entry: `.ufo/waves/round-52/w1/C2EntryDraft/entry-draft.md`
- Map: `.ufo/waves/round-52/w1/C2EntryDraft/proposition-map.tsv` (P01-P18)
- Pins (re-fetched this round by the draft seat, byte-equal to round-51 pins — I re-verified):
  `.ufo/waves/round-52/w1/C2EntryDraft/fetch/{Hyprland-legacy-DispatcherTranslator.cpp,
  Hyprland-ConfigActions.cpp, Hyprland-ConfigActions.hpp, Hyprland-KeybindManager.cpp}`
  sha256 `7248cbb8…` / `a83abeb5…` / `746c6f51…` / `8d8f35fc…` — 4/4 equal to
  `.ufo/waves/round-51/fetch/` (recomputed this seat).
- Dependency pins (round-51 fetch, held): `Hyprutils-VarList2.{hpp,cpp}` @ `a21e87b8`
  (v0.14.2; sha256 `0e484df5…`/`b8cacea7…`).
- Compiled reproductions: this dir, `optional_xtract_repro.cpp`/`.out`, `varlist2_repro.py`/`.out`.

Method note: no runtime, no compositor, no package query, no live host read, no install, no
git/jj mutation, no tracked-file write. The one compile executed (`g++ 16.2.1`, scratch only)
models a C++ standard semantic; it reads and writes only this seat's scratch/seat dir.

---

## Verdict summary

| # | attacked clause | verdict |
|---|---|---|
| A1 | P16 mechanism "null window replaced by focused window before delivery" | **NOT REPRODUCED — falsified** (engaged-optional semantics; compiled proof) |
| A2 | P16 support class `direct` | overstated (mechanism claim unsupported by its quote for this path) |
| A3 | P16 outcome "an empty selector targets whatever is focused" | outcome coincides; not source-establishable (host-state inference) |
| A4 | P13 "the synthetic event carries the timestamp … and keycode minus 8" | NOT REPRODUCED as event behavior — call-site fact only; seat implementation unpinned |
| A5 | P13 mask clause "asserted before delivery and cleared to 0 after" | true on uncited lines outside the anchor; binding carries it only via rationale |
| A6 | P13/P14 "timestamp of the last real input event" | true, grounded only in writers the map never cites (KeybindManager.cpp:385/:482-484) |
| A7 | P14 "the last key/mouse event's timestamp, defaulting to 0" | REPRODUCED true; binding is comment-only, writers uncited; mouse writer outside S373 scope |
| A8 | P01 rationale "the constructor caps the split at four fields" | **NOT REPRODUCED — falsified** against pinned hyprutils + held r51 ground |
| A9 | step 1 "splits its tail into at most four comma fields" | same mechanism error in prose (held-ground contradiction) |
| A10 | P06 rationale "the split is capped at three" | same mechanism error for sendshortcut |
| A11 | step 1 "a five-field sendkeystate tail fails on the first test" | REPRODUCED true via unbounded split → size 5; mechanism narration wrong; truth is a dependency-version inference |
| A12 | P17 "modifier and key events are still sent … bookkeeping skipped" | REPRODUCED at call level; client delivery remains seat-side inference |
| A13 | step 3 "repeat emits two press edges and no release" | REPRODUCED at call-sequence level; properly bounded |
| A14 | State-claims table "protocol message" rows (seat modifier/key state) | runtime protocol inference from call sites; seat code unpinned |
| A15 | Binding check cannot catch any of A1/A8-A11 | confirmed structurally (checker's own docstring; defects live in rationale/claim layer) |
| A16 | P12 translator-side claim | REPRODUCED (:582-586); correctly fenced from the P16 downstream story |
| A17 | P14 raw-vs-collapsed quote exposure (hpp:117 spacing) | confirmed on bytes; verdict depends on the frozen whitespace-collapsed policy |
| A18 | No SeatManager bytes in any pin | boundary condition: every "seat receives/sends" clause is inference beyond opened sources |

---

## A1 — P16 mechanism claim is falsified: the optional is engaged, `value_or` never fires

**Attacked clause** (proposition-map.tsv P16, entry-draft.md step 6):

> "A null window is replaced by the focused window before delivery, so an empty selector targets
> whatever is focused." — quote `static PHLWINDOW xtract(std::optional<PHLWINDOW> window) { return
> window.value_or(Desktop::focusState()->window()); }` (ConfigActions.cpp:47-49), support `direct`.

**Reproduction.** The call path is fixed by pinned bytes:

- Translator: `PHLWINDOW PWINDOW = regexp.empty() ? nullptr : …selector…runWindow();`
  (`Hyprland-legacy-DispatcherTranslator.cpp:584`), then `return wrap(Actions::pass(MOD, keycode, PWINDOW));` (:588).
- Callee signature: `ActionResult Actions::pass(uint32_t modMask, uint32_t key, std::optional<PHLWINDOW> w)`
  (`Hyprland-ConfigActions.cpp:1530`), body `auto window = xtract(w);` (:1531).
- `xtract` (:47-49): `return window.value_or(Desktop::focusState()->window());`.

For an empty selector, `PWINDOW` is a **null handle value** of type `PHLWINDOW`. Converting a
`PHLWINDOW` **value** into `std::optional<PHLWINDOW>` uses `optional`'s value-constructing
converter, which **engages** the optional regardless of the handle's nullness (`value_or` fires
only on `!has_value()`). So `xtract` returns the **null handle**; the `value_or` fallback never
runs for this path. Compiled proof (scratch; `g++ -std=c++23`, modeling `SP<CWindow>` as a
value type constructible from `nullptr`, mirroring `xtract`):

```
optional has_value after conversion from null PWINDOW = 1
xtract returned the focused window? 0  (0 = null handle returned, value_or did NOT fire)
xtract(std::nullopt, focused) returns focused? 1
optional<FakeWindow*> from null raw pointer has_value = 1
```

`optional_xtract_repro.cpp` / `.out` in this dir. The result is independent of whether `PHLWINDOW`
is `SP<CWindow>` or a raw pointer — engagement is a type-level rule; even `optional<CWindow*>`
constructed from a null pointer is engaged.

**Observed consequence in the pinned body.** With `window` null after `xtract`, `Actions::pass`
skips the `if (window)` focus-switch block (:1540-1552), executes `sendKeyboardMods`/`sendKeyboardKey`
(:1554-1576), then hits `if (!window) return {};` (:1578-1579). The entry's step-6 mechanism
("the `nullptr` an empty field produces is not an empty target downstream … so the delivery calls
target the focused window") is **wrong**: the null window survives `xtract`; the events are
delivered to whatever the *seat's then-current keyboard focus* is.

**Verdict: NOT REPRODUCED.** The mechanism "null window replaced by the focused window before
delivery" is false for `sendshortcut`'s call path. `C2Novelty` flagged exactly this
("for sendshortcut's call the optional is engaged with a null handle, so xtract's focused-window
branch never runs — the outcome coincides, the mechanism differs"); the entry recorded the dissent
but kept P16's wording and its `direct` class.

## A2 — P16 support class `direct` overstates

**Attacked clause.** P16's support class is `direct`: "each quote contains the construct the
proposition asserts" (entry's own checker semantics).

**Observation.** Under A1, the xtract quote does **not** do the work P16 assigns to it for this
call path: `value_or` demonstrably does not fire. The quote describes the helper's behavior for a
*disengaged* optional; the proposition asserts behavior for an *engaged-with-null* one. This is a
`chain`-class proposition at best (needs the call-site conversion semantics at :584/:588/:1530),
or a narrowed claim ("the null window skips the focus switch; the events reach the seat's current
focus").

**Verdict: reproduced as overstated.** Limitation: whether "outcome coincides" holds at any given
dispatch instant is host focus state (A3), so even the narrowed outcome claim is not purely
source-level.

## A3 — P16's outcome "targets whatever is focused" is itself host-state inference

**Attacked clause.** "…so an empty selector targets whatever is focused."

**Observation.** With `window == nullptr` after `xtract`, the delivery calls (`sendKeyboardKey`,
:1558) take no window argument at all — targeting is mediated by the seat's keyboard-focus state,
which is set elsewhere (real input, prior `setKeyboardFocus` calls) and lives in `SeatManager` /
`Desktop::focusState` code that is **not pinned and not opened this round**. "Targets whatever is
focused" coincides only while the seat's focus equals the compositor's focused window — a runtime
host invariant the source pins do not establish.

**Verdict: NOT REPRODUCED as a source fact** — host-state inference, disclosed by neither the
proposition nor the Limits. (The Limits exclude the *receiving client*, but not this.)

## A4 — P13 "the synthetic event carries…" is call-site fact, not event behavior

**Attacked clause** (P13): "The synthetic event carries the timestamp of the last real input event
and the keyboard keycode minus 8; …" — quote `g_pSeatManager->sendKeyboardKey(S.m_timeLastMs, key - 8,
WL_KEYBOARD_KEY_STATE_PRESSED);` (ConfigActions.cpp:1558), anchor span `:1558-1558`, support `direct`.

**Observation.** Grep across all four pins: `sendKeyboardKey` / `sendKeyboardMods` appear **only
as call sites** in `ConfigActions.cpp` (1489/1491/1494/1496/1499-1503, 1554/1558/1560/1563/…/1576).
Their definitions live in `src/managers/SeatManager.*` — **not pinned, not opened this round**.
The pins establish that the *call* passes `S.m_timeLastMs` and `key - 8`; they say nothing about
what the seat does with those arguments — whether the protocol event to the client carries the
same values, transforms them, or drops them. The entry's Limits disclose "the offset is claimed as
written, its receiver convention is `[INF]`", but P13 states "carries" as `direct` fact.

**Verdict: NOT REPRODUCED as event behavior.** The defensible direct claim is "the delivery call
is issued with arguments `S.m_timeLastMs, key - 8`". "The synthetic event carries" is runtime
inference beyond the opened sources. Same boundary applies verbatim to "the modifier mask is
asserted" (the `sendKeyboardMods` *calls* execute; the client-visible modifier effect is seat-side).

## A5 — P13's mask clause rides on lines outside its own anchor

**Attacked clause.** "…the modifier mask is asserted before delivery and cleared to 0 after."

**Reproduction.** P13's anchor span is `1558-1558` and its quote is the `sendKeyboardKey` line
only. The mask calls are `g_pSeatManager->sendKeyboardMods(modMask, 0, 0, 0);` (:1554) and
`g_pSeatManager->sendKeyboardMods(0, 0, 0, 0);` (:1576) — read from the pin this seat; both are
outside the anchor and absent from the quote. The proposition's second clause is carried entirely
by the rationale sentence naming uncited lines — the M51-2 pattern (claim broader than its cited
lines) that `C2Novelty` named and the frozen counter admits it cannot catch.

**Verdict: clause true on the bytes; binding overstated as `direct`.** Smallest safe fix: extend
the anchor to `:1554-1576` with a reflowed quote within the 25-word cap, or split the mask clause
into its own proposition.

## A6 — P13/P14 "timestamp of the last real input event" rests on uncited writers

**Attacked clause.** P13 "the timestamp of the last real input event"; step 7 "stamped with the
last real event's time, and 0 before any real input"; P14 "the last key/mouse event's timestamp".

**Reproduction.** `grep m_timeLastMs` over the pins finds exactly two write sites, both pinned and
both **uncited anywhere in the entry or map** (grep of `entry-draft.md` + `proposition-map.tsv`
for `385`, `484`, `onKeyEvent`, `onMouseEvent` returns nothing):

- `Hyprland-KeybindManager.cpp:385` — `Config::Actions::state()->m_timeLastMs = e.timeMs;` (key
  press path, `onKeyEvent` context, :369-395).
- `Hyprland-KeybindManager.cpp:482-484` — `m_lastMouseCode = e.button; m_lastCode = 0;
  m_timeLastMs = e.timeMs;` (mouse button path, `onMouseEvent`, :476-493).

The map's only binding for the "last real event" semantics is the hpp:117 comment
(`// timestamp of last key/mouse event`). The claim is **true** and better-grounded than the map
shows — the writers exist in pinned bytes — but the evidence chain the frozen counter checks
(quote at anchor) does not carry it, and the entry never cites :385/:482-484.

**Verdict: reproduced as true via uncited pinned lines.** Limitation: the mouse writer at
:482-484 sits outside the proposed S373 row scope (`stringToModMask` :221-240 + the cache member),
so a reviewer verifying P14 from S373's declared scope alone cannot confirm the "mouse" half.

## A7 — P14 is true; its binding is comment-only

**Attacked clause.** P14 quote `uint32_t m_timeLastMs = 0; // timestamp of last key/mouse event`
(hpp:117), support `direct`.

**Observation.** Default 0: grounded by the declaration itself. "last key/mouse event's
timestamp": grounded (in the bytes) only by the comment plus the uncited writers of A6. A code
comment is a claim, not proof; the proof exists in the same pinned file the round opened and was
not cited. The raw pin line is `uint32_t    m_timeLastMs    = 0;  // timestamp of last key/mouse
event` (multiple internal spaces) — the map quote is whitespace-collapsed, so it binds only under
the counter's frozen `whitespace-collapsed` policy and would fail a raw line-contains check
(`C2Novelty`'s policy point; I confirm the bytes).

**Verdict: REPRODUCED true; binding quality overstated.** No proposition falsified; the
proposition-counter's green receipt is insensitive to the gap.

## A8 — P01 rationale mechanism contradicts pinned hyprutils and held r51 ground

**Attacked clause** (P01 rationale): "The constructor caps the split at four fields and the size
test is the only gate before the state field is read…" — quote `CVarList2 ARGS(args, 4); if
(ARGS.size() != 4) return {.success = false, .error = "sendkeystate: invalid args"};`
(DispatcherTranslator.cpp:591-594).

**Reproduction.** The pinned dependency bytes are unambiguous: in
`Hyprutils-VarList2.cpp` @ `a21e87b8` (round-51 fetch), `construct(in, lastArgNo, delim,
removeEmpty, allowEscape)` **never references `lastArgNo`** — `grep -n lastArgNo` shows it only in
the three constructor signatures and the `construct` signature (:8-21). The header comment
documents a cap ("stop splitting after argv reaches maximum size"), but the implementation does
not implement one. This is already **held ground**: the round-51 entry's Limits state
(`corpus/knowledge/hyprland-dispatcher-dispatch-r51.md`, Limits bullet 5) that the pinned
hyprutils (v0.14.2, `a21e87b8`, "the version the host package reports as `0.14.2-1`") "shows the
cap implemented in `CVarList` … but **not implemented in `CVarList2`, whose `construct` never
reads its `lastArgNo` parameter**". P01's rationale asserts the opposite mechanism.

**Verdict: NOT REPRODUCED — the mechanism claim is falsified** against pinned bytes and the lane's
own held corpus. The proposition itself survives: with an unbounded split, any tail whose piece
count ≠ 4 fails `ARGS.size() != 4`, so "rejects any other count" is true — but true by the size
test over an unbounded split, not by "the constructor caps". The defect lives exactly where the
frozen counter cannot see it: the quote sits verbatim at its anchor while the rationale misreads a
dependency the entry never opened.

## A9 — step 1 repeats the same mechanism error in prose

**Attacked clause** (entry-draft.md step 1): "`sendkeystate` splits its tail into at most four
comma fields and refuses anything but four: `CVarList2 ARGS(args, 4); …`"

**Observation.** Under the pinned implementation the split is unbounded; "at most four" is false
as mechanism. Same held-ground contradiction as A8; the prose claim is not in the proposition map,
so no counter can ever flag it.

**Verdict: NOT REPRODUCED (mechanism false; behavioral residue true).**

## A10 — P06 rationale has the identical defect for sendshortcut

**Attacked clause** (P06 rationale): "The split is capped at three and the size test precedes every
parse step…" — quote `CVarList2 ARGS(args, 3); if (ARGS.size() != 3) …` (:531-535).

**Verdict: NOT REPRODUCED** — same inert-`lastArgNo` mechanism error as A8/A9; proposition true via
the size test over the unbounded split. This is a pattern (two propositions share the same false
mechanism narration), not an isolated slip.

## A11 — the five-field example is true, but its truth is a dependency-version inference

**Attacked clause** (step 1): "a five-field `sendkeystate` tail fails on the first test even though
its first three fields would be a valid `sendshortcut`."

**Reproduction.** Simulating the pinned `construct` loop verbatim in Python
(`varlist2_repro.py`, this dir): `mods,key,down,win,x` with `CVarList2(args, 4)` yields 5 args →
size 5 ≠ 4 → REJECT; the 3- and 4-piece cases behave as claimed. So the example's outcome holds —
**but only because the linked hyprutils build is the pinned one**, where `lastArgNo` is inert. On a
hypothetical hyprutils build implementing the documented cap, the same tail would lump to 4 args
and pass. Which behavior Hyprland 0.56.2 exhibits at runtime is therefore a **build/dependency
fact**, not a fact about the four opened files. The lane's evidence that the host package is
`0.14.2-1` is round-51's recorded host observation (held); this round banned live reads, so I could
not re-confirm the linked version — the truth of "rejects any other count" leans on held host
evidence, not on this round's pins.

**Verdict: REPRODUCED true under the pinned/inert dependency; mechanism narration wrong (A8);
residual dependency on held host evidence for runtime truth.**

## A12 — P17 is call-level true; "sent" remains seat-side

**Attacked clause** (P17): "When no window is focused at all, the modifier and key events are still
sent and only the focus bookkeeping is skipped." — quote `if (!window) return {};` (:1578-1579).

**Reproduction.** Read of the pin body: the modifier/key send calls (:1554-1574) execute in
program order before the `:1578-1579` return. The *calls* are reached on every path. Whether
clients receive anything is `SeatManager` behavior (unpinned, A4). "only the focus bookkeeping is
skipped" is exact for the surviving-null case: the return at :1578 precedes only the X11/focus
restore block (:1582-1598).

**Verdict: REPRODUCED at call level**; "events are still sent" is the strongest source-supported
wording and is what the proposition says. No defect beyond the A4 boundary.

## A13 — step 3's repeat claim is call-sequence true

**Attacked clause** (step 3): "`repeat` emits two press edges and no release" — each delegate call
with `m_passPressed == 1` takes the press branch (:1556-1560) and the repeat guard re-invokes
`sendshortcut` (:619-622).

**Reproduction.** Pinned body: with `m_passPressed == 1`, exactly one
`sendKeyboardKey(…, WL_KEYBOARD_KEY_STATE_PRESSED)` executes and no RELEASE call exists on that
branch; two guarded delegate calls ⇒ two PRESSED calls, zero RELEASE. Whether the seat or client
coalesces identical consecutive presses is runtime behavior the entry does not claim.

**Verdict: REPRODUCED at call-sequence level; properly bounded.** One note: "no release is sent"
is true of the *code path*; a release could still be observed by a client from seat-level state
machinery — outside the pins, not claimed.

## A14 — state-claims "protocol message" rows assert compositor→client behavior from call sites

**Attacked clause** (entry "State claims" table): `seat keyboard modifier state | mask | modMask
during the event, 0 after | … | protocol message`; `seat keyboard key state | event | one press,
one release, or both … | protocol message`.

**Observation.** "Protocol message" asserts what the compositor emits to clients. The pins show
only the manager-side calls; the protocol effect is `SeatManager`/protocol-code behavior, unpinned
this round. These rows are not in the proposition map (not counted as propositions), but they are
factual claims in the entry, and the qualifier `protocol message` is doing the work of an
unstated inference. Not a counter-visible defect; flagged for the outside source-truth reviewer's
sample.

**Verdict: runtime inference, bounded but real.**

## A15 — the binding check structurally cannot catch A1/A8-A11

**Attacked clause.** The draft checker's own contract (`.ufo/waves/round-52/w1/C2EntryDraft/check-quotes.py`
docstring): "This checks bindings, not entailment: a quote that sits at the anchor and says
something else still passes here."

**Observation.** Every defect above reproduces *with* a verbatim quote at its anchor and a green
binding run: P16's quote is exact at :47-49 while the mechanism claim attached to it is false
(A1); P01's quote is exact at :591-594 while its rationale misreads the dependency (A8). The
frozen r52 counter inherits the same boundary by design (`C2CounterDraft`: "It does not decide
whether a quote entails the proposition"). The independent non-author source-truth sample is
therefore load-bearing for exactly the claim family this seat attacked — and W1's sample
(`C2PinAudit`: 17/17 quotes verbatim, "every support/rationale line cite I checked resolves to
true bytes") checked that rationale *cites resolve to bytes*, not that rationale *mechanisms match*
bytes: A8's rationale clause "the constructor caps the split at four fields" resolves to no pin at
all (it cites the call, not the dependency), and A1's mechanism resolves to a pin that contradicts
the claim for the actual call shape.

**Verdict: REPRODUCED (structural blind spot confirmed).** This is a process finding for the
reviewer, not a claim against the counter's stated scope.

## A16 — P12's translator-side claim is reproduced

**Attacked clause** (P12): "An empty third field resolves to nullptr with no selector lookup; a
written selector that resolves to nothing is an error." — quote :582-586.

**Reproduction.** Pin read (:582-586): the ternary maps empty text to `nullptr` without running
`selector()`; the `:585-586` test returns `window not found` for a written selector with no match.
Verified verbatim. The proposition correctly fences the downstream story as P16's job — the defect
is in P16 (A1-A3), not here.

**Verdict: REPRODUCED.**

## A17 — P14's quote binds only under the frozen whitespace-collapsed policy

**Attacked clause.** P14 quote vs pin bytes.

**Reproduction.** Pin `Hyprland-ConfigActions.hpp:117` raw:
`uint32_t    m_timeLastMs    = 0;  // timestamp of last key/mouse event` (multiple internal
spaces). Map quote collapses them to single spaces. Under the counter's frozen
`quote_policy=whitespace-collapsed` it binds; under a raw line-contains policy it fails. The
verdict on P14 therefore depends on a policy choice, not on the bytes.

**Verdict: REPRODUCED as a policy exposure** (same observation as `C2Novelty` N4; bytes confirmed
independently this seat).

## A18 — boundary condition: no SeatManager bytes exist in any pin this round

**Attacked clause.** The entry's recurring runtime vocabulary: "the seat receives", "the seat
carries", "the modifier mask is asserted", "events are sent".

**Reproduction.** `grep -rn 'sendKeyboardKey\|sendKeyboardMods'` across
`.ufo/waves/round-52/w1/C2EntryDraft/fetch/` and `.ufo/waves/round-51/fetch/`: call sites only;
no definitions. The seat/input-manager source is not pinned in either round, and no proposed row
(S370-S373) covers it.

**Verdict: REPRODUCED.** Every runtime-behavior clause in the entry is inference beyond the opened
sources; the Limits disclose the receiver-convention part but the proposition map still asserts
"carries"/"sent" as `direct`. The honest landing shape: downgrade P13's event-language to
call-language (or add `chain` support), extend P13's anchor across :1554-1576, cite the
`m_timeLastMs` writers (:385/:482-484) in P13/P14 support, and rewrite P16 to the surviving-null +
seat-current-focus mechanism actually in the pins.

---

## Fairness record (what survived)

- P02, P03, P04, P05, P07, P08, P09, P10, P11, P12, P16's *existence* facts, P17, P18: quote
  bindings verified exact on the pins during this attack; their propositions are source-shape
  claims that do not depend on unpinned runtime behavior (P07's "silently mask 0" is grounded in
  the no-else parser over :221-242, confirmed by `C2SourceRecon`).
- Step 3 and step 7's timestamp/offset claims are call-level true (A12, A13, A6).
- The entry's Limits disclose more than most candidates would (byte-equality, receiver `[INF]`,
  the P16 correction record). The defects found live in the proposition map's `direct` labels and
  rationale mechanisms, not in wholesale fabrication.

## Limitations of this attack

- I did not run the entry's `check-quotes.py` or the draft counter (execution of sibling seat
  scripts is another seat's lane; `C2Novelty` followed the same rule). My verification is
  independent reads of the same pins plus two scratch-local reproductions.
- The A1 compile models `SP<CWindow>` minimally; the engagement result is a type-level C++ rule
  and holds for any `T` (the repro also tests a raw pointer), so it is robust to `PHLWINDOW`'s
  exact definition, but I did not read Hyprland's `defines.hpp` (not pinned) to confirm `PHLWINDOW`
  is `SP<CWindow>` rather than a raw pointer — immaterial to the verdict.
- A11's dependency-version point leans on round-51's held host observation (package `0.14.2-1`);
  live verification was banned this round, so it is recorded as held evidence, not re-measured.
- The seat spec bars host reads; all byte evidence is from the lane repo and its pinned fetches.
- Scratch `/fast/scratch/hyaku/mado-r52/Attack16/` held only the two repro drivers; cleaned on
  completion (copies live in this seat dir). No `/tmp` evidence, no install, no package query, no
  git/jj mutation, no network use, no live read, no tracked-file write outside this report and
  seat dir.

## Commands exercised (all read-only against lane bytes, plus scratch-local repro)

- `sha256sum` on the four round-52 fetch files vs the four round-51 pins → 4/4 equal.
- `grep -rn 'm_timeLastMs'` on the round-52 fetch → writes at KeybindManager.cpp:385/:482-484.
- `grep -rn 'sendKeyboardKey\|sendKeyboardMods'` on both fetch roots → call sites only.
- `grep -n lastArgNo Hyprutils-VarList2.cpp` → signatures only (:8-21).
- Range reads: DispatcherTranslator.cpp:575-630; ConfigActions.cpp:44-52, 1524-1603;
  KeybindManager.cpp:370-392, 472-490; VarList2.hpp/cpp; r51 entry :294-338.
- `g++ -std=c++23` compile + run of `optional_xtract_repro.cpp` (scratch only).
- `python3 varlist2_repro.py` — pinned-construct simulation (scratch only).

Report trailer:

```
seat=Attack16 wave=w2 round=52 lane=mado-shokunin base=85d57a818c3707397e21c840b6498b105ba798aa
claim=C2 coverage proposition-bound dispatcher source entry
target=C2 source claims versus runtime/host inference (candidate entry, not yet landed)
attacked=P16 mechanism+outcome+support-class; P13 carries/mask-anchor; P13/P14 timestamp writers; P01/P06 split-cap rationale; step1 five-field example; P17; step3 repeat; state-claims protocol rows; binding-check blind spot; P12; P14 quote policy; seat-pin boundary
verdicts=A1 falsified(optional engagement; compiled proof), A8/A9/A10 falsified mechanism vs pinned hyprutils+held r51 ground; A4/A3 not source-establishable (unpinned seat); A5/A6/A7 true-on-uncited-lines; A11/A12/A13/A16 reproduced at call level; A14/A15/A17/A18 reproduced as boundary findings
evidence=.ufo/waves/round-52/w2/Attack16/{optional_xtract_repro.cpp,optional_xtract_repro.out,varlist2_repro.py,varlist2_repro.out}
report=.ufo/waves/round-52/w2/Attack16.md
```
