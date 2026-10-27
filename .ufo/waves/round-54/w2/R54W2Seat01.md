# R54W2Seat01 — C1 P19 quote-judge falsification

## Finding

**Specification ambiguity remains actionable:** the frozen registration's specific normalization rule makes P19 a literal-byte check, while the prior w1 counter report demonstrates that a whitespace-collapsed pin-region judge produces a different result. P19 is not literally contiguous in the pinned bytes; it matches only after whitespace collapse. This makes the contract's intended judge ambiguous, not a failure in the source pin.

## Frozen contract and evidence
- `registration.md:21-34` freezes the P19 row and quote at `:27`, its anchor `:1554-1558`, and the side-claim “P19 quote found spanning exactly lines 1554–1558” at `:32`. Its judge rule is at `registration.md:49-53`: exact byte contiguity after single-space normalization of interior newlines **only where the frozen quote itself carries a newline**; P19 is a single logical line.
- `claims-frozen.md:19-30` defines PRED-C1-r54 and requires each quote cell to occur “verbatim and contiguous” in its named pin; the predicate also requires the pinned bytes' hashes and exact anchor side-claims.
- The pinned `round-52/fetch/Hyprland-ConfigActions.cpp` lines 1554–1558 (read evidence) are, with original whitespace: line 1554 `    g_pSeatManager->sendKeyboardMods(modMask, 0, 0, 0);`; line 1555 blank; line 1556 `    if (S.m_passPressed == 1) {`; line 1557 `        if (!isMouse)`; line 1558 `            g_pSeatManager->sendKeyboardKey(S.m_timeLastMs, key - 8, WL_KEYBOARD_KEY_STATE_PRESSED);`.
- The frozen P19 quote contains **zero newline bytes**. Its literal byte sequence occurs **0** times in the pin; the raw bytes of the cited anchor differ from the quote. Collapsing whitespace across the exact anchor yields an exact match, and the quote occurs **once** in the whitespace-collapsed whole pin. Thus the normalized match spans precisely lines 1554–1558, while the literal judge rejects it. It is not merely a broader-range or wrong-anchor match.

This reproduces the distinction in `w1/R54Seat01.md` §1: its byte-exact counter reported `quotes=1/4 anchors=1/4 verdict=TARGET_MISSED` (exit 1), whereas its pin-region whitespace-collapsed judge reported `quotes=4/4 anchors=4/4 verdict=TARGET_MET` (exit 0). The w1 report further says each quote under the whitespace-collapsed reading occurred once and spanned its registered anchor. Its stated conclusion is that the “ONLY where the frozen quote itself carries a newline” wording selects the literal reading for single-line P19/P21/P22, despite the frozen table being derived under the whitespace-collapsed reading.

## Counter availability / verification

The assigned pinned command was **NOT RUN: absent**. At inspection, `quality/counters/` contained no `r54` counter; in particular `quality/counters/c1-r54-errata-truth.py` did not exist. No substitute or draft counter was run. This is an availability finding, not a verdict from the counter.

Exact measurement command (read-only):

```sh
python3 -I -c 'from pathlib import Path; import re; p=Path(".ufo/waves/round-52/fetch/Hyprland-ConfigActions.cpp").read_bytes(); q=b"g_pSeatManager->sendKeyboardMods(modMask, 0, 0, 0); if (S.m_passPressed == 1) { if (!isMouse) g_pSeatManager->sendKeyboardKey(S.m_timeLastMs, key - 8, WL_KEYBOARD_KEY_STATE_PRESSED);"; lines=p.splitlines(); collapse=lambda b: re.sub(rb"\\s+",b" ",b).strip(); anchor=b"\\n".join(lines[1553:1558]); full=collapse(p); needle=collapse(q); hits=[]; i=0
while (j:=full.find(needle,i))>=0: hits.append(j); i=j+1
print("literal pin occurrences:",p.count(q)); print("collapsed whole-pin occurrences:",len(hits)); print("collapsed anchor equals quote:",collapse(anchor)==needle); print("anchor raw bytes:",repr(anchor)); print("quote bytes:",repr(q)); print("quote newline_count:",q.count(bytes([10]))); print("anchor line range: 1554-1558");'
```

Output:

```text
literal pin occurrences: 0
collapsed whole-pin occurrences: 1
collapsed anchor equals quote: True
anchor raw bytes: b'    g_pSeatManager->sendKeyboardMods(modMask, 0, 0, 0);\n\n    if (S.m_passPressed == 1) {\n        if (!isMouse)\n            g_pSeatManager->sendKeyboardKey(S.m_timeLastMs, key - 8, WL_KEYBOARD_KEY_STATE_PRESSED);'
quote bytes: b'g_pSeatManager->sendKeyboardMods(modMask, 0, 0, 0); if (S.m_passPressed == 1) { if (!isMouse) g_pSeatManager->sendKeyboardKey(S.m_timeLastMs, key - 8, WL_KEYBOARD_KEY_STATE_PRESSED);'
quote newline_count: 0
anchor line range: 1554-1558
```

Exit: **0**.

## Scope and cleanup

No predicate, registration, lane/source, or sibling files were edited. No git mutation or fixture was needed. Assigned scratch `/fast/scratch/hyaku/mado-r54/R54W2Seat01` was created and removed before yield; no scratch remains. No installs; no disk-check failure or ENOSPC.

Report path (relative to lane root): `.ufo/waves/round-54/w2/R54W2Seat01.md`