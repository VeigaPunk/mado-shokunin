# W2 attack #23 — C2: "each proposition quote entails full claim"

Seat: `Attack23` (connector). Axes: **coverage** (primary, C2) and **operability** (counter integrity). Wave w2, attack lane — findings are reproductions against source pins and the committed counter, not non-author verdicts.

Attacked clause (claims-frozen.md, C2): *"each material factual proposition maps to a pinned source quote <=25 words and explicit support rationale"* — specifically whether each landed quote entails its full written proposition, and whether the committed counter checks that binding.

Artifacts under test (all untracked working-tree files at detached-base HEAD `85d57a8`):
- `corpus/knowledge/hyprland-synthetic-dispatch-r52.md` — landed entry, 18-row proposition table (layout: `ID | Proposition | Source row | Pin:anchor | Quote | Support class | Why it supports`)
- `quality/counters/c2-r52-proposition-entry.py` — landed counter
- Pins: `.ufo/waves/round-52/fetch/{Hyprland-legacy-DispatcherTranslator.cpp,Hyprland-ConfigActions.cpp,Hyprland-ConfigActions.hpp,Hyprland-KeybindManager.cpp}` — `sha256sum -c SHA256SUMS` all OK, bytes match SOURCES.md digests.

W1 signal checked: "C2 new pins and claim table require independent re-open and source truth" — this seat re-opened every anchor in the r52 fetch bytes rather than reusing the W1 audit, which covered only the *draft* TSV (different table, different propositions).

---

## F1 — P16's "quote" does not exist in the pinned file (REPRODUCED falsifier)

- **Claim attacked:** P16 — "The action sends modifier state before the key event, then clears the modifier state." Quote: `g_pSeatManager->sendKeyboardMods(modMask, 0, 0, 0); g_pSeatManager->sendKeyboardKey(S.m_timeLastMs, key - 8, WL_KEYBOARD_KEY_STATE_PRESSED);` anchored `Hyprland-ConfigActions.cpp:1554-1558,1576`.
- **Reproduction:** `grep` / contiguous-substring search of `fetch/Hyprland-ConfigActions.cpp` (whitespace-collapsed). The two quote fragments are separated by :1555-1557 (`if (S.m_passPressed == 1) { if (!isMouse)`). The spliced string occurs **nowhere** in the pin: `in_anchor=False`, `in_file=False`.
- **Observed:** the quoted text is a manufactured concatenation; the "then clears" half of the claim rests on :1576, which is inside the anchor spec but outside the quoted bytes. The W1 draft counter independently emits `miss=P16:quote_not_at_pin` (see F4).
- **Verdict:** reproduced — quote does not entail claim; the quote is not an "exact located quote" at all.
- **Limitation:** entailment judgment delegated to the non-author reviewer; this report establishes only that the bound text is absent from the pin and that the claim's second clause is unquoted.

## F2 — P17 misattributes the repeat branch (REPRODUCED falsifier)

- **Claim attacked:** P17 — "`sendshortcut`'s repeat branch can invoke its delegate twice for a successful repeat state." Quote `if (keyState == 2 && result.success) result = sendshortcut(modifiedArgs);` anchored `Hyprland-legacy-DispatcherTranslator.cpp:619-622` (verbatim-present).
- **Reproduction:** `grep -n "keyState\|repeat" Hyprland-legacy-DispatcherTranslator.cpp` → hits only at :597-621 inside `sendkeystate` (body :591-627). `sendshortcut` (body :531-589) contains neither `keyState` nor `repeat`; it is the *delegate* invoked at :619,:622 — the direction of invocation is opposite the proposition's.
- **Observed:** `sendshortcut` has no repeat branch and invokes no delegate; the quote lives inside `sendkeystate`, which P04 already describes correctly. P17 is a false duplicate of P04 (same anchor 619-622). The nearest real repeat branch in a same-named direction is `Actions::sendKeyState` (ConfigActions.cpp:1612), a different function pinned under S371, not S370.
- **Verdict:** reproduced — quote binds the lines but the proposition's subject is wrong; the claim as written is source-false.
- **Limitation:** charitable reading ("`sendshortcut`'s" = "the sendshortcut dispatcher family") is conceivable but contradicted by the S370 scope cell naming `sendshortcut` and `sendkeystate` as the two distinct subjects.

## F3 — Quote-coverage gaps: claim clause outside quoted bytes (anchor-supported, quote-unsupported)

Reproduction: substring check of each quote against its anchor range (script logged to scratch; all 18 rows tested). Rows whose decisive claim clause is **not in the quoted text** (though in the cited anchor):

| prop | claim clause needing evidence | where it actually lives |
|---|---|---|
| P01 | "rejects a different count" | `return … "invalid args"` at :594 — quote stops at `if (ARGS.size() != 4)` |
| P02 | "others are rejected" | error return at :598 — quote is only the `if` condition |
| P06 | "requires exactly three" | rejection at :534 — quote stops at `!= 3)` |
| P07 | "names" (plural modifiers) | only the SHIFT `contains` test is quoted; anchor 221-225 covers no second name |
| P10 | "the keyboard keycode range" | `keycode_min/max` bound to `KB->m_xkbKeymap` at :560-563, outside anchor and quote |
| P12 | "is rejected" | `window not found` return :585-586 — quote is only the ternary |

Verdict: reproduced as a class — 6 of 18 quotes are anchor-supported but do not themselves entail the full proposition. Consistent with the C2 carve-out ("not automated semantic-entailment proof"), but the "quote entails full claim" premise this seat was asked to test holds for only 11 of 18 rows verbatim (P03,P04,P05,P08,P09,P11,P13,P14,P15,P18 + P17 quote binds but claim is false). P18's "inside the scan" is additionally imprecise: the return at :573-574 sits *after* the `for` loop, inside the cache-miss `if`.

## F4 — Committed counter cannot evaluate the landed entry (REPRODUCED)

- **Claim attacked:** "a new committed counter checks proposition count, row/pin/quote bindings and complete mapping."
- **Reproduction (scratch fixture, own clone + commit):**
  1. `python3 quality/counters/c2-r52-proposition-entry.py --repo <fixture> --rev HEAD --work <scratch>` (default `--entry` = `corpus/knowledge/hyprland-synthetic-key-dispatch-r52.md`) → `entry=absent verdict=TARGET_MISSED` — default slug ≠ landed slug `hyprland-synthetic-dispatch-r52.md`.
  2. Same run with `--entry corpus/knowledge/hyprland-synthetic-dispatch-r52.md` → `props=0 rows=0 indexed=1 failures=1 verdict=TARGET_MISSED`, `miss=props`. The committed regex demands `P\d+` in column 1 **and** `S\d+` in column 2; the landed table puts the proposition text in column 2, so zero rows parse.
  3. Control: W1 draft counter (`w1/C2CounterDraft/c2-r52-proposition-entry.py`, the spec-shaped implementation) against the identical landed artifacts on a rev with base `85d57a8` reachable → `TARGET_MISSED`, clauses_met=2/5: `c rows_bound=0/18` (all `anchor_no_fetch_root` — landed anchors lack fetch-root paths/pin manifest), `d miss=P16:quote_not_at_pin` (confirms F1), `e miss=P01..P04+:id_not_referenced` (landed entry has no prose referencing proposition IDs).
- **Observed:** the committed counter (a) never opens a pin file, never searches a quote, never resolves an anchor — its "bindings" check is row-metadata regex only; (b) parses zero propositions from the landed entry; (c) defaults to a nonexistent slug. The landed artifacts are mutually inconsistent: the entry cannot pass the committed counter, and the committed counter checks none of what the frozen claim names.
- **Verdict:** reproduced — the "counter checks row/pin/quote bindings and complete mapping" premise is not demonstrated by the committed bytes; W1 `r-green` proved a synthetic fixture only, as signaled.
- **Limitation:** artifacts are untracked at detached-base HEAD; post-landing commits could repair slug/regex. Verdict concerns the present committed-candidate pair, not a final tree.

## F5 — Repeated-URL rows S370/S371/S373 (verified, QUALITY17 formally open)

`grep '^| S36[4-7]' corpus/SOURCES.md`: S370≡S365 URL, S371≡S367, S373≡S364 — but cited ranges are disjoint (S370 `:531-627` vs S365 `:30-35,797-867`; S371 `:1530-1616` vs S367 `:1664-1682`; S373 `:221-242` vs S364 `:41-113,602,782,785,798-823`), so distinct-scope is defensible on source evidence. SOURCES.md's own audit-trail line records "distinct-scope review remains outstanding" — consistent with the W1 flag; not falsified, but formally unresolved.

## Verified (not attacked)

- 16 of 18 landed quotes are whitespace-collapsed verbatim inside their cited anchors (P16 is the sole absent one); all ≤25 words (max 19). Raw-contiguous count is lower because source spans multiple lines — draft counter reports `quotes_raw=6/17` on the landed table.
- P13's quote is one of three same-shaped `sendKeyboardKey(m_timeLastMs, key-8, …)` calls (:1558/:1563/:1568-9); claim phrasing survives.
- P15 landed claim (save only) is consistent with its quote; the draft's restore half was dropped — narrowing, not falsity.

## Summary for the non-author reviewer

Two hard falsifiers against "each proposition quote entails full claim": **P16** (bound text absent from pin) and **P17** (subject misattribution — branch belongs to `sendkeystate`). Six further rows are anchor-true but quote-incomplete. The committed counter is structurally incapable of checking the landed table (0 props parsed, no pin/quote machinery, wrong default slug) — and the W1-specified control counter independently fails the landed entry 2/5 clauses. Reproduce: any entry → `python3 quality/counters/c2-r52-proposition-entry.py --repo <repo> --rev <rev> --work <dir> [--entry corpus/knowledge/hyprland-synthetic-dispatch-r52.md]`.

Lane: mado-shokunin. Round: 52. Wave: w2. Seat: Attack23. Scratch `/fast/scratch/hyaku/mado-r52/Attack23/` (fixture clone, counter runs) removed after reporting. No tracked edits, no installs, no host reads beyond the lane's own pinned bytes.
