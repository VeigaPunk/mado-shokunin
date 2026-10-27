# R54Seat28 — adversarial source-truth review of the r53 correction (wave 1, item 28)

Seat: `R54Seat28`, scribe, leaf member (no subagent dispatch). Lane root
`/home/vgpnk/Projects/shokunin/mado-shokunin`, base `e25149fec8152a3aabd2b18a0ee8663b23cf65aa`.
Governed by `.ufo/waves/round-54/claims-frozen.md` (PRED-C1-r54) and
`.ufo/waves/round-54/registration.md` (C1 fixture inventory, frozen table, controls).
Assigned item: *"Adversarial source-truth review plan for r53 correction: enumerate exact pin
propositions and whether registered quotes entail them."* This seat is **not** the non-author
closure reviewer; nothing here closes the correction (§ Limits).

Everything below is static: committed `corpus/` text, the committed round-52 pins under
`.ufo/waves/round-52/fetch/`, and committed `SHA256SUMS`. No host read, no network fetch, no
counter execution (no `c1-r54-*` counter exists at base — `ls quality/counters | grep -c r54` → `0`,
matching `receipts/before.txt`). Clauses (a)–(c) were replayed by an independent checker written
in this seat's scratch; clause (d) (the six controls) was **not** exercised by this seat.

## 1. Pin integrity first (otherwise every citation is void)

Command (cwd `.ufo/waves/round-52/fetch`):

```
sha256sum Hyprland-ConfigActions.cpp Hyprland-ConfigActions.hpp \
          Hyprland-KeybindManager.cpp Hyprland-legacy-DispatcherTranslator.cpp
```

Output (all four byte-identical to the recorded round-52 sums in `SHA256SUMS`, and to the four
rows of the frozen registration table):

```
a83abeb57175e65908d8d67ddc9802310134e5a4752fa3764f980401b48a7637  Hyprland-ConfigActions.cpp
746c6f517620eb039afbfbb9a4a0e2d5ba1c5eb117bcc8f396173f63091b7073  Hyprland-ConfigActions.hpp
8d8f35fc84c4a2f8de63ac2bf6f6531c651c6fa6d37b1aac7c8fc5d9342d4e40  Hyprland-KeybindManager.cpp
7248cbb89f898c783c50c89d068df9821a6b38aeb6abeb6064e92c1610fbe771  Hyprland-legacy-DispatcherTranslator.cpp
```

Pins: `4/4`. The errata entry's four `Quote` cells are byte-identical to the frozen table's
`Quote` cells (`4/4`, backticks included) — there is no row drift at base.

## 2. Enumerated propositions vs their registered quotes

Entry under test: `corpus/knowledge/hyprland-synthetic-dispatch-r52-errata-r53.md` (row shape
`ID | Supersedes | Proposition | Source row | Pin:anchor | Quote (≤25 words) | Support`).
Frozen table row shape: `ID | Pin file | Anchor | Quote (verbatim, contiguous)`.

| ID | Committed proposition (abridged) | Quote span located in pin (whitespace-collapsed) | What the quote ALONE entails | What only the surrounding pin adds | Pin truth | Quote entails proposition? |
|---|---|---|---|---|---|---|
| P19 | "`Actions::pass` sends modifier state before its delivery branch; it sends a PRESSED keyboard key **only when** `m_passPressed == 1` and the key is not a mouse button." | `ConfigActions.cpp` **1554–1558**, 1 occurrence | mods-send precedes the `==1` branch; under `!isMouse` a PRESSED key is sent | lines **1566–1573** (the `else` dynamic branch) also send PRESSED for `!isMouse` | **FALSE** (`:1568`) | **No** — not entailed and contradicted |
| P20 | "After the key/button delivery branch, `Actions::pass` clears modifier state." | `ConfigActions.cpp` **1576**, 1 occurrence (unique in file) | that a `mods(0,0,0,0)` call exists | branch body **1556–1574** precedes it | TRUE | **No** — "after" is an ordering relation; a point anchor cannot carry it |
| P21 | "`sendkeystate` calls `sendshortcut` again when its state is `repeat` and the first call succeeds." | `legacy-DispatcherTranslator.cpp` **619–622**, 1 occurrence | second call guarded by `keyState == 2 && result.success` | `keyState = 2` ← `"repeat"` at **603–604**; containment **591–627** | TRUE | **Partial** — "repeat" mapping is outside quote and outside the checked anchor side-claims |
| P22 | "When key resolution leaves `keycode` unset after the scan, `sendshortcut` returns the `key not found` error from its cache-miss branch." | `legacy-DispatcherTranslator.cpp` **573–574**, 1 occurrence | guarded `key not found` return | loop close **571**; cache test **559** | TRUE | **Partial** — "after the scan" is checked (`573 > 571`); "cache-miss branch" (559) is neither quoted nor checked |

Aggregate source-truth verdict: **3/4 propositions true, 1/4 (P19) false against the pin**;
**0/4 fully entailed by the quote alone**, because each proposition carries a scoping or ordering
qualifier that its ≤25-word excerpt does not contain.

### 2.1 P19 is false — exact evidence

`Hyprland-ConfigActions.cpp` (numbered):

```
1554|    g_pSeatManager->sendKeyboardMods(modMask, 0, 0, 0);
1555|
1556|    if (S.m_passPressed == 1) {
1557|        if (!isMouse)
1558|            g_pSeatManager->sendKeyboardKey(S.m_timeLastMs, key - 8, WL_KEYBOARD_KEY_STATE_PRESSED);
1559|        else
1560|            g_pSeatManager->sendPointerButton(S.m_timeLastMs, key, WL_POINTER_BUTTON_STATE_PRESSED);
1561|    } else if (S.m_passPressed == 0) {
1562|        if (!isMouse)
1563|            g_pSeatManager->sendKeyboardKey(S.m_timeLastMs, key - 8, WL_KEYBOARD_KEY_STATE_RELEASED);
...
1566|    } else {
1567|        if (!isMouse) {
1568|            g_pSeatManager->sendKeyboardKey(S.m_timeLastMs, key - 8, WL_KEYBOARD_KEY_STATE_PRESSED);
1569|            g_pSeatManager->sendKeyboardKey(S.m_timeLastMs, key - 8, WL_KEYBOARD_KEY_STATE_RELEASED);
1570|        } else {
...
1574|    }
1576|    g_pSeatManager->sendKeyboardMods(0, 0, 0, 0);
```

`Hyprland-ConfigActions.hpp:114` — the field's live value set is documented by the pin itself:

```
114|        int         m_passPressed   = -1; // -1 = dynamic (press+release), 0 = released, 1 = pressed
```

Reachability of `-1` and of non-`{0,1}` values (whole-pin scan, command
`awk '/m_passPressed/ {printf "%s:%d|%s\n", FILENAME, FNR, $0}' ...`):

```
Hyprland-ConfigActions.cpp:1487  if (S.m_passPressed == 1) {
Hyprland-ConfigActions.cpp:1492  } else if (S.m_passPressed == 0) {
Hyprland-ConfigActions.cpp:1556  if (S.m_passPressed == 1) {
Hyprland-ConfigActions.cpp:1561  } else if (S.m_passPressed == 0) {
Hyprland-ConfigActions.cpp:1603  ... oldPassPressed = ...m_passPressed;
Hyprland-ConfigActions.cpp:1606/1608  = 1; / = 0;
Hyprland-ConfigActions.cpp:1615  ...m_passPressed = oldPassPressed;
Hyprland-ConfigActions.hpp:114   int m_passPressed = -1; // -1 = dynamic (press+release)
Hyprland-KeybindManager.cpp:804  ...m_passPressed = sc<int>(pressed);
Hyprland-KeybindManager.cpp:814  ...m_passPressed = -1;
Hyprland-legacy-DispatcherTranslator.cpp:612/615/617/624  read, =1, =0, restore
```

Consequences, all static:

1. `Hyprland-KeybindManager.cpp:814` resets `m_passPressed` to `-1` **after every keybind
   dispatch**; the field's default is `-1` (`hpp:114`). Any `Actions::pass` reached outside a
   freshly pressed keybind therefore takes the line-1566 `else` branch, which sends a PRESSED
   keyboard key at `:1568` for `!isMouse`.
2. That path exists: `sendshortcut` is dispatcher-registered at
   `Hyprland-legacy-DispatcherTranslator.cpp:841` (`m_dispMap["sendshortcut"] = ::sendshortcut;`)
   and calls `wrap(Actions::pass(MOD, keycode, PWINDOW))` at `:588`. A `sendshortcut` dispatch
   with no preceding keybind press-set reaches `pass` with `m_passPressed == -1`.
3. Therefore "**only when** `m_passPressed == 1`" is false at the pin. The correct statement is:
   "…sends a PRESSED keyboard key when `m_passPressed == 1`, **and also in the dynamic branch
   (value ∉ {0,1} — the `-1` default) after the keybind handler resets it (`KeybindManager.cpp:814`),
   whenever `!isMouse`**."

The frozen P19 quote spans 1554–1558 and therefore cannot carry the universal; the entry's
`Support` cell ("direct — one contiguous excerpt carries the call order and branch condition") is
accurate about what the excerpt carries and simultaneously documents the gap: the excerpt carries
the `==1` branch only.

## 3. Findings

### F1 — (blocking, freeze) the frozen "verbatim" judge sentence is satisfiable only under one of two readings; the literal reading kills C1 on real data

Registration: *"Judge of 'verbatim': exact byte contiguity after single-space normalization of
interior newlines ONLY where the frozen quote itself carries a newline (P19/P21/P22 are single
logical lines)."*

No frozen quote contains a newline character (`0/4`; verified on both tables). Measured outcomes
over the committed pins:

```
collapsed_stripped_hits=4/4   (spans P19 1554–1558, P20 1576, P21 619–622, P22 573–574)
literal_stripped_hits=1/4     (only P20 — the single-line quote)
literal_raw_cell_hits=0/4     (cells carry backticks; see F5)
```

- Reading A ("collapse each maximal whitespace run, including newlines and indentation, to one
  space"): `quotes=4/4`, and each span lands exactly on its frozen anchor → clause (b) `anchors=4/4`.
- Reading B (the sentence as written — normalization only where the quote itself carries a
  newline, which none does): `quotes=1/4` → the frozen C1 line cannot be printed for the committed
  corpus, and the kill rule ("any real pin, quote, or anchor mis-verifies → `TARGET_MISSED`")
  fires on *real* data, not on a forged control.

Impact: a counter implemented to the sentence literally prints `quotes=1/4 verdict=TARGET_MISSED`
at every revision of the round; implemented to reading A it prints the frozen `TARGET_MET` line.
The freeze does not decide which. Repair belongs in a **pre-data** re-registration
(`claims-frozen-v2.md`, the file's own escape hatch) — this seat has not scored, so the repair is
still cheap — or an explicit reading fixed in the counter's documented contract before any seat
scores.

Minimal wording: *"verbatim = the frozen quote, once each maximal whitespace run (spaces, tabs,
newlines, indentation) is collapsed to a single space, occurs exactly once in the pin and that
occurrence spans exactly the frozen anchor lines."*

### F2 — (blocking, source truth) the r53 correction's P19 proposition is false at its own pin, and PRED-C1-r54 cannot see it

Evidence §2.1. The r53 entry is the artifact under test; the C1 predicate verifies quote
contiguity, anchor placement, pin hashes and control rejection — **not** proposition truth, and
the frozen table has no proposition column at all (F5). So C1 can print the frozen
`verdict=TARGET_MET` line while `corpus/knowledge/hyprland-synthetic-dispatch-r52-errata-r53.md`
asserts a contradicted universal. The claim label "errata **source-truth** verifier" therefore
overstates what is measured: it is a quote/anchor/pin verifier.

Operational fix is cheap because the audit trail is already correct: the P19 `Quote` and
`Pin:anchor` cells are right; only the `Proposition` sentence needs the dynamic branch added.
The errata entry's own `Limits and review state` paragraph already concedes that a non-author
reviewer must verify each proposition — that review has now been done (this seat) and P19 fails.

### F3 — (advisory) P20/P21/P22 are true, but each proposition's qualifier is checked by nothing

- P20: the anchor is a single line; `1556–1574` (the branch it is "after") is never read by any
  frozen clause. A proposition reading "**before** the delivery branch" with the identical
  ID/anchor/quote would pass every clause.
- P21: the anchor side-claims are only `591 ≤ 619` and `622 ≤ 627`. The `repeat → keyState == 2`
  mapping lives at `603–604` and is unchecked; a quote-correct row whose proposition said "state
  is `down`" would pass.
- P22: `573 > 571` is checked (good); the cache-miss scoping at `559` is not, so "from its
  cache-miss branch" versus "from its post-cache guard" is indistinguishable to the predicate.

Recommendation: extend the frozen anchor side-claims for P21 (`603 ≤ k ≤ 604` must be the only
`= 2` assignment) and P22 (574 inside the block opened at 559), or state in the entry that the
qualifier is reviewed by the non-author source-truth seat, not by the counter.

### F4 — (minor, source truth, outside predicate coverage) the Gate section's "exact quote" is not verbatim

Entry: *"Its exact quote at §2 line 38, “P16 fails — the space-joined quote” (6 words)"*.

Committed `corpus/lessons/round-52-verifier-spotcheck.md:38` reads
`**P16 fails** — the space-joined quote …`. Measured:

```
claimed-quote occurrence in line38: False
with bold markers present: True
word count of claimed quote (dash as token): 6
word count excluding dash: 5
```

The `**` markers intervene, so the string is not verbatim, and the "6 words" count only holds if
the em dash counts as a word. Same class of defect the entry exists to correct; PRED-C1-r54 reads
only the P19–P22 rows, so no clause can catch it.

### F5 — (blocking, implementability) the frozen table cannot be compared to the entry row "byte-for-byte"; the comparison target is undefined

```
entry cells per row: 7   | ID | Supersedes | Proposition | Source row | Pin:anchor | Quote (≤25 words) | Support |
frozen cells per row: 4  | ID | Pin file | Anchor | Quote (verbatim, contiguous) |
```

Registration says the counter "extracts the committed entry's P19–P22 rows and checks them against
THIS table byte-for-byte modulo trailing spaces". Row-wise byte comparison is impossible across
different column sets; the counter must pick fields. Two different counters result, with opposite
behaviour on a corrected proposition:

```
P19 ID/anchor/quote fields identical: True True True
P19 full-row string identical: False        (with the corrected proposition text)
```

So the freeze simultaneously (i) cannot forbid a false proposition, and (ii) can, under the
literal row comparison, reject a *true* correction as "drift". Both tables also wrap quotes in
backticks, so pin matching requires delimiter stripping — unspecified, and responsible for the
`literal_raw_cell_hits=0/4` line in F1.

Minimal wording: *"the counter reads the entry's `ID`, `Pin:anchor` and `Quote` cells
(backtick delimiters stripped); the `Proposition`, `Supersedes`, `Source row` and `Support` cells
are not compared, and their truth is not a C1 clause."*

### F6 — (note) the frozen anchor cell format

Frozen: `Pin file` = `` `Hyprland-ConfigActions.cpp` ``, `Anchor` = `` `:1554-1558` ``. Entry:
`Pin:anchor` = `Hyprland-ConfigActions.cpp:1554-1558`. Assembly is unambiguous, but the leading
colon in the frozen anchor cell must be stripped before integer parsing; record it in the
counter contract rather than in the frozen table.

## 4. Attacked predicate and the distinct input

- Attacked clauses: PRED-C1-r54 clause (a) as implemented through the registration's "Judge of
  'verbatim'" sentence (F1, F5), and the whole of clause (a)+(b) as a source-truth test (F2, F3).
- Distinct input vs other wave-1 seats (mutation-testers 24/25 own control rejection; executors
  30–32 own the do-nothing route and freeze omissions; reviewer seats own registration
  gameability; mutant seats mutate the counter): this seat supplies the **entailment plane** —
  the proposition text itself read against the pin — and the only input in the wave that uses a
  *real* pin defect rather than a forged fixture: P19's universal at `ConfigActions.cpp:1568`
  plus `KeybindManager.cpp:814`. A counter that passes controls 1–6 perfectly still prints
  `TARGET_MET` on this input; no control in the frozen inventory covers it.
- Second distinct input: the literal-normalization reading (F1), executed against the committed
  pins (`1/4` vs `4/4`), which shows the predicate's satisfiability depends on an unstated
  reading — not on any mutation.

## 5. Gates and limits observed by this seat

- No lane tracked edit; no git/jj mutation; no commit/push; no subagent/task/background job; no
  campaign tool; no counter execution; no host/domain read; no network. Scratch:
  `/fast/scratch/hyaku/mado-r54/R54Seat28` (cleaned before yield).
- Not exercised, by scope: the six frozen C1 controls (`controls=6/6` is **unverified** here),
  `--selftest`, C2 in any form, `tools/mado-verify.sh --selftest` (harm-watch number quoted from
  `receipts/before.txt`, not re-run), `corpus/README.md` navigation count.
- This seat is not the non-author closure reviewer for the r53 correction; it produces findings
  for that seat and for the L1 pre-data decision on F1/F5.

## 6. Verdict

Source-truth review of the r53 correction: **3/4 propositions true, P19 false** (F2); **0/4
entailed by quote alone**. PRED-C1-r54 as frozen is **not admissible without repair**: it is
unsatisfiable on real data under the literal judge sentence (F1) and undefined as a comparison
(F5), and even when implemented to the intended reading it cannot distinguish a true proposition
from a false one (F2/F3). None of this edits the freeze; it is reported for pre-data
re-registration.

## Trailer

- Report (relative to lane root): `.ufo/waves/round-54/w1/R54Seat28.md`
- Lane files written by this seat: none (report only)
- Scratch used and removed: `/fast/scratch/hyaku/mado-r54/R54Seat28` (outside the lane)
- Evidence base: `.ufo/waves/round-52/fetch/{Hyprland-ConfigActions.cpp,Hyprland-ConfigActions.hpp,
  Hyprland-KeybindManager.cpp,Hyprland-legacy-DispatcherTranslator.cpp,SHA256SUMS}`,
  `corpus/knowledge/hyprland-synthetic-dispatch-r52-errata-r53.md`,
  `corpus/lessons/round-52-verifier-spotcheck.md`,
  `.ufo/waves/round-54/{claims-frozen.md,registration.md,receipts/before.txt}`
- Tooling installed/updated by this seat: none
