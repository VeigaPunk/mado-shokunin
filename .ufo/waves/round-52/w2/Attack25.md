# Attack25 — W2 attack on C2 quote location and ≤25-word binding

Seat: `Attack25` (reviewer), wave `w2`, round 52, lane `/home/vgpnk/Projects/shokunin/mado-shokunin`.
Axes: **coverage** attacked (C2); **operability** (C1) untouched.

**Attacked clauses** (`claims-frozen.md` C2 / `registration.md` C2):
1. "each material factual proposition maps to a pinned source quote <=25 words" — an "exact
   located quote" per the frozen predicate.
2. "A new committed counter checks proposition count, row/pin/quote bindings and complete
   mapping" — the premise that a *quote binding* is enforced.
3. Premise that W1 audit receipts cover the landed artifact.

**Artifact under attack (what actually landed, working tree at HEAD `85d57a81`):**
`corpus/knowledge/hyprland-synthetic-dispatch-r52.md` (untracked `??`), rows S370–S373 in
`corpus/SOURCES.md` (modified `M`), index row in `corpus/README.md` (`M`),
`quality/counters/c2-r52-proposition-entry.py` (untracked `??`). Pins:
`.ufo/waves/round-52/fetch/Hyprland-{legacy-DispatcherTranslator.cpp,ConfigActions.cpp,ConfigActions.hpp,KeybindManager.cpp}`
— all four sha256-recomputed **equal** to `fetch/SHA256SUMS` (checked locally, no fetch).

---

## Findings by severity

### F1 — HIGH — NOT REPRODUCED: P16's "quote" is a fabricated splice, not a located quote

`hyprland-synthetic-dispatch-r52.md:28`, row P16:
- claim: "The action sends modifier state before the key event, then clears the modifier state."
- pin: `Hyprland-ConfigActions.cpp:1554-1558,1576` (a **discontiguous** anchor)
- quote: `g_pSeatManager->sendKeyboardMods(modMask, 0, 0, 0); g_pSeatManager->sendKeyboardKey(S.m_timeLastMs, key - 8, WL_KEYBOARD_KEY_STATE_PRESSED);`

Reproduction (exact source bytes, pin verified against SHA256SUMS):

```
$ sed -n '1554,1576p' .ufo/waves/round-52/fetch/Hyprland-ConfigActions.cpp
1554:  g_pSeatManager->sendKeyboardMods(modMask, 0, 0, 0);
1555:
1556:  if (S.m_passPressed == 1) {
1557:      if (!isMouse)
1558:          g_pSeatManager->sendKeyboardKey(S.m_timeLastMs, key - 8, WL_KEYBOARD_KEY_STATE_PRESSED);
...
1576:  g_pSeatManager->sendKeyboardMods(0, 0, 0, 0);
```

Independent checker (collapse-whitespace contiguous-substring policy, the same policy
`w1/C2CounterDraft` froze for clause (d)):

```
P16 FAIL row=S371 pin=Hyprland-ConfigActions.cpp:[(1554,1558),(1576,1576)] words=9 found=False
ctx='} sendKeyboardMods(modMask, 0, 0, 0); if (S.m_passPressed == 1) { if (!isMouse)
      sendKeyboardKey(S.m_timeLastMs, key - 8, WL_KEYBOARD_KEY_STATE_PRESSED); else …'
```

The quote concatenates line 1554 and line 1558, **silently eliding `if (S.m_passPressed == 1) {`
and `if (!isMouse)`** — the two guards that make the key event conditional. `grep -n
'sendKeyboardMods\|sendKeyboardKey'` on the pin shows the spliced pair appears contiguously
**nowhere** in the file (call sites: 1485/1489, 1554/1558, 1576 — always separated). The
`:1576` clear call the anchor names is not quoted at all. Under the frozen
whitespace-collapsed verbatim policy this is `quote_not_at_pin`: the "exact located quote"
clause fails for a material proposition (the seat-delivery ordering). Honest weaker reading:
it is two excerpts presented as one quote with no ellipsis — still not "exact located" by the
lane's own convention.

### F2 — HIGH — NOT REPRODUCED: the landed counter checks no quote binding and cannot read the landed table

`quality/counters/c2-r52-proposition-entry.py` is a 47-line script, **not** the 965-line W1
draft (`w1/C2CounterDraft/c2-r52-proposition-entry.py`). Three concrete defects demonstrated
in a scratch clone (`git rev-parse --show-toplevel` asserted before staging; lane untouched):

(a) **No quote-location check exists.** The only quote test is `:39`
    `len(quote.split())>25` plus a non-empty rationale; no pin file is ever opened
    (the script only `git show`s entry/README/SOURCES). Proof: a reordered table with a
    fabricated quote `zzz fabricated words never present anywhere in pin` on P03:

```
$ python3 -I quality/counters/c2-r52-proposition-entry.py --repo <clone> --rev HEAD \
    --work <scratch> --entry corpus/knowledge/hyprland-synthetic-dispatch-r52.md
C2_R52: props=18 rows=4 indexed=1 failures=0 verdict=TARGET_MET   exit=0
```

    A fabricated quote **admits** → "checks … quote bindings" is falsified. (The ≤25-word
    check does work *when reached*: a 27-word P01 mutant → `miss=quote/rationale:P01`, exit 1.)

(b) **The counter parses 0 propositions on the landed entry.** Its row regex
    `^\|\s*(P\d+)\s*\|\s*(S\d+)\s*\|…` demands the source row as the *second* cell; the landed
    table's second cell is the claim (`| P01 | <claim> | S370 | …`). Measured:

```
C2_R52: props=0 rows=0 indexed=1 failures=1 verdict=TARGET_MISSED rev=HEAD
miss=props
```

    On the real artifact every per-proposition check — including the ≤25-word check — is dead
    code. The landed counter would `TARGET_MISS` a perfect entry written in the landed table
    shape.

(c) **Stale default entry path.** `--entry` defaults to
    `corpus/knowledge/hyprland-synthetic-key-dispatch-r52.md` (the W1 draft slug); the landed
    slug is `hyprland-synthetic-dispatch-r52.md`. Run as documented it reports
    `entry=absent verdict=TARGET_MISSED` — the required "production pass" cannot be
    demonstrated by the documented invocation.

Note: at frozen tip `85d57a81` all four artifacts are uncommitted (`git status`: `??` entry +
counter, `M` README/SOURCES). "New committed counter" is unproven at HEAD; counter runs above
required committing the working tree into a scratch clone first. Base control
(`--rev 85d57a81…`) correctly misses `entry=absent`, reproducing the no-work control.

### F3 — MEDIUM — NOT REPRODUCED: P17 attributes sendkeystate's repeat logic to `sendshortcut`

`hyprland-synthetic-dispatch-r52.md:29`, P17: "`sendshortcut`'s repeat branch can invoke its
delegate twice for a successful repeat state", pinned `DispatcherTranslator.cpp:619-622`,
quote verbatim (13→9 words). But `sendshortcut` spans `:531-589` and `sendkeystate` spans
`:591-627`; `keyState` occurs **only** inside sendkeystate (`grep -n keyState`:
600,602,604,614,621). The cited lines are *sendkeystate's* repeat logic
(`keyState == 2 ⇔ STATE == "repeat"`); `sendshortcut` has no repeat branch and no `keyState`.
The quote is correctly located but cannot support a claim whose subject is `sendshortcut` —
a material factual proposition is false on source truth, the class of defect C2's
non-author-truth clause exists to catch. P17 also recites P04's fact (identical span
`:619-622`, near-synonymous claims); the "ids and claims distinct" bar is met only by string
inequality, weakening the 18-proposition count's substance.

### Reproduced (verified, not attacked further)

- 17/18 quotes verbatim (whitespace-collapsed contiguous) inside their cited spans; all 18
  ≤25 whitespace words (max 19, P03; min 5). Byte-exact single-line: 6/18 (P02, P05, P11, P13,
  P15, P18) — the rest are reflowed multi-line excerpts, consistent with the frozen policy.
- All four pins sha256-equal to `fetch/SHA256SUMS`; S370–S373 rows carry `mined`,
  `2026-10-27`, 40-hex `efb50993…`, and `used-by` naming the landed entry.
- P16's W1-audit lineage does not cover the landed row: the audited draft TSV's P16 was the
  `xtract` proposition at `ConfigActions.cpp:47-49`; the landed table rewrote P16–P18 and
  renumbered anchors. W1 "all quotes verbatim" receipts apply to a different artifact.

## Residual risk and verification gaps

- P12's second conjunct ("a written selector without a result is rejected") rests on lines
  585–586, inside the cited span `:582-586` but outside the quote text; same unquoted-second-
  half pattern as P16's `:1576` clear call. Flagged, not scored (entailment-side).
- My location policy is whitespace-collapsed **contiguous** substring. Under a token-
  subsequence policy P16 would pass; the lane's frozen convention (per `w1/C2CounterDraft`)
  is contiguous-collapsed, which fails it. No entailment judgment taken — F3 is a
  subject-attribution error evidenced by location, not an entailment verdict.
- Counter experiments ran against a scratch clone (`/fast/scratch/hyaku/mado-r52/Attack25`,
  removed after report); lane working tree never modified by this seat. `python3 -I`, `git`,
  `sha256sum`, `grep`, `sed` only; no installs, no network, no host probes.

## Errors and verdicts

| item | verdict |
|---|---|
| C2 "exact located quote" clause | **not reproduced** — F1 (P16 splice), F3 (P17 wrong subject) |
| C2 "≤25 words" clause | **reproduced** for all 18 cells (max 19) |
| counter "checks quote bindings" premise | **not reproduced** — F2a (fabricated quote admits), F2b (0 props parsed), F2c (stale default slug) |
| W1 verbatim receipts cover landed table | **not reproduced** — landed P16–P18 are new content |
| no-work control (base) | reproduced — `entry=absent` at `85d57a81` |

Report trailer:

```
seat=Attack25 wave=w2 round=52 lane=mado-shokunin base=85d57a818c3707397e21c840b6498b105ba798aa
claim=C2 coverage — quote location + <=25 words
entry=corpus/knowledge/hyprland-synthetic-dispatch-r52.md (untracked at HEAD)
counter=quality/counters/c2-r52-proposition-entry.py (untracked at HEAD)
pins=.ufo/waves/round-52/fetch/ 4/4 sha256 EQUAL to SHA256SUMS
quotes_verbatim=17/18 max_words=19 fabricated=P16 mislocated_subject=P17
counter_runs=5 (stale-slug MISS, landed-table props=0 MISS, fabricated-quote MET, overlong-quote MISS, base MISS)
verdict=C2 quote-binding clause NOT REPRODUCED (F1,F2,F3); word-cap clause reproduced
scratch=/fast/scratch/hyaku/mado-r52/Attack25 (cleaned)
report=.ufo/waves/round-52/w2/Attack25.md
```
