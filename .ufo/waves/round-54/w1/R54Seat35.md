# R54Seat35 — C1 source pins, exact-byte review

- Round 54, wave 1, seat `R54Seat35` (scribe/audit role; leaf, no dispatch).
- Lane root: `/home/vgpnk/Projects/shokunin/mado-shokunin`; base rev `e25149fec8152a3aabd2b18a0ee8663b23cf65aa` (`git rev-parse HEAD` → same; `.ufo/waves/round-52/` unmodified before and after this review, `git status --porcelain .ufo/waves/round-52/` empty).
- Assignment: review the **C1** errata pins with exact-byte checks; report hash/anchor discrepancies; **do not edit**. Item 35.
- Runtime class: static committed bytes only. No host read, no network, no package query, no producer/counter execution (no `c1-r54-*` counter exists at this rev: `ls quality/counters | grep r54` → empty).
- Lane writes: this report only. Nothing installed or updated (no tool channel used). Scratch `/fast/scratch/hyaku/mado-r54/R54Seat35` used and removed before yield.

Axis focus: **coverage + operability**. The measure this seat advances is the *operability* of PRED-C1-r54: whether its frozen sentence can be satisfied by a counter that obeys the registration's own definition of "verbatim". It cannot — see D1.

## 1. Inputs under test

| input | path | identity at base |
|---|---|---|
| C1 entry | `corpus/knowledge/hyprland-synthetic-dispatch-r52-errata-r53.md` | tracked, LF, no CRLF, no trailing whitespace |
| pins | `.ufo/waves/round-52/fetch/{Hyprland-ConfigActions.cpp,Hyprland-ConfigActions.hpp,Hyprland-KeybindManager.cpp,Hyprland-legacy-DispatcherTranslator.cpp}` | tracked blobs at base |
| recorded digests | `.ufo/waves/round-52/fetch/SHA256SUMS` | 5 entries (4 pins + `README.txt`) |
| frozen table | `.ufo/waves/round-54/registration.md:27-30` (quote/anchor/pin rows), `.ufo/waves/round-54/claims-frozen.md:19-45` (predicate) | frozen |

Pin bytes are the committed bytes, not a dirty worktree: `git ls-tree e25149fe .ufo/waves/round-52/fetch/` blob ids `cf388167…`/`95192458…`/`4ab407ec…`/`b534fec3…`/`e5303fd1…`/`c8e7bfee…` equal `git hash-object` of the working files (all six). So every byte result below holds equally for a `--rev`-reading counter.

## 2. Hash leg (C1 clause (c)) — 4/4 match, plus the round-52 record agrees with the freeze

```
$ cd .ufo/waves/round-52/fetch && sha256sum Hyprland-ConfigActions.cpp Hyprland-ConfigActions.hpp \
      Hyprland-KeybindManager.cpp Hyprland-legacy-DispatcherTranslator.cpp
a83abeb57175e65908d8d67ddc9802310134e5a4752fa3764f980401b48a7637  Hyprland-ConfigActions.cpp
746c6f517620eb039afbfbb9a4a0e2d5ba1c5eb117bcc8f396173f63091b7073  Hyprland-ConfigActions.hpp
8d8f35fc84c4a2f8de63ac2bf6f6531c651c6fa6d37b1aac7c8fc5d9342d4e40  Hyprland-KeybindManager.cpp
7248cbb89f898c783c50c89d068df9821a6b38aeb6abeb6064e92c1610fbe771  Hyprland-legacy-DispatcherTranslator.cpp
$ sha256sum -c SHA256SUMS   # at lane root
…ConfigActions.cpp: OK / …ConfigActions.hpp: OK / …KeybindManager.cpp: OK
…legacy-DispatcherTranslator.cpp: OK / …README.txt: OK      (rc=0)
```

Byte-for-byte, `SHA256SUMS` digest == `registration.md` pin table digest == recomputed digest for all four. Extra entry `README.txt` = `c53296ae…74ad0`, also OK. **No hash discrepancy.**

Byte hygiene of the pins (all four): LF only (`crlf=0`, lone CR=0), no BOM, no tab bytes, no trailing whitespace, final newline present; `Hyprland-KeybindManager.cpp` carries 2 non-ASCII bytes (outside the quoted regions). Line counts: 1772 / 122 / 975 / 868. None of these can perturb a byte-exact judge, except that no pin is CRLF — so a CRLF-tolerant normalizer is not needed and would be a hardening hole, not a necessity.

## 3. Quote leg (C1 clause (a)) — fails at byte level: 1/4

Exact byte containment of each frozen Quote cell in the pin named by its Pin:anchor cell:

| prop | pin | exact occurrences | span under whitespace-run collapse |
|---|---|---|---|
| P19 | `Hyprland-ConfigActions.cpp` | **0** | 1554–1558 |
| P20 | `Hyprland-ConfigActions.cpp` | 1 (line 1576, col 4–48) | 1576–1576 |
| P21 | `Hyprland-legacy-DispatcherTranslator.cpp` | **0** | 619–622 |
| P22 | `Hyprland-legacy-DispatcherTranslator.cpp` | **0** | 573–574 |

The cause is visible in the raw bytes. `ConfigActions.cpp`:

```
1554:     g_pSeatManager->sendKeyboardMods(modMask, 0, 0, 0);
1555: (blank)
1556:     if (S.m_passPressed == 1) {
1557:         if (!isMouse)
1558:             g_pSeatManager->sendKeyboardKey(S.m_timeLastMs, key - 8, WL_KEYBOARD_KEY_STATE_PRESSED);
```

`DispatcherTranslator.cpp`:

```
571:             }                                    <- scan closes (P22 "after line 571")
573:             if (!keycode)
574:                 return {.success = false, .error = "sendshortcut: key not found"};
…
619:     auto result = sendshortcut(modifiedArgs);
620: (blank)
621:     if (keyState == 2 && result.success)
622:         result = sendshortcut(modifiedArgs);
```

Each frozen quote is an **indentation-stripped, blank-line-dropped, space-joined** reconstruction of its span. Measured per span: P19 drops exactly 1 blank interior line (1555), P21 drops exactly 1 (620); P22 and P20 drop none. Consequences:

- "strip each line and join with a single space **keeping** the blank lines" gives `…0, 0, 0);  if (S.m_passPressed…` — a **double space** — and does not equal the quote for P19/P21.
- Only "drop blank lines, then join with one space" reproduces the quote (verified: `strip+drop-blank+join-space` equals the cell for P19/P21/P22; equality for P20 trivially).
- Consequently the registration's own allowance — `registration.md:51-53` "exact byte contiguity after single-space normalization of interior newlines ONLY where the frozen quote itself carries a newline (P19/P21/P22 are single logical lines)" — does **not** reach these quotes: they carry no newline, so by that sentence no normalization is allowed, and no normalization of newlines alone would work anyway because of the blank interior lines.

### Anchors themselves are correct (C1 clause (b))

Under the only oracle that admits the committed cells (collapse whitespace runs, then require the match span to equal the anchor), every anchor side-claim holds exactly:

| claim (`claims-frozen.md:25-28`) | observed |
|---|---|
| P19 at exactly `ConfigActions.cpp:1554-1558` | span `(1554, 1558)` ✓ |
| P20 at exactly `:1576` | span `(1576, 1576)`, unique in all four pins ✓ |
| P21 at exactly `DispatcherTranslator.cpp:619-622` inside 591–627 | span `(619,622)`; 591 ≤ 619 and 622 ≤ 627 ✓ |
| P22 at exactly `:573-574` after line 571 | span `(573,574)`; 573 > 571 ✓ |

Supporting side-claims in the entry's Support column also check out at byte level: `sendshortcut` declares at line 531 and its closing brace is line 589 (brace depth walked 531→589, returns to 0 at 589; line 588 is `return wrap(Actions::pass(MOD, keycode, PWINDOW));`) — so "`sendshortcut` ends at line 589" is true; `sendkeystate` declares at 591 and closes at 627 — so "inside lines 591–627" is true; line 571 is the `}` that closes the keycode scan loop — so "after line 571" is true.

### Entry ⇄ frozen-table cell equality

For all four propositions the entry's Pin:anchor cell and Quote cell are **byte-identical** to the frozen registration cells (pin ✓, anchor ✓, quote ✓ for each; quote lengths 182/45/115/80 bytes; no non-ASCII, no trailing space, no double space in either copy). Quote word counts 16/4/13/12, inside the entry's own "≤25 words" column header. So there is no drift between entry and freeze; the defect is in the freeze's text itself.

## 4. Discrepancies

**D1 — blocking, contract-internal: the frozen label `quotes=4/4` is unattainable under the frozen definition of "verbatim".**
`claims-frozen.md:24` requires each Quote cell "occurring verbatim and contiguous"; `registration.md:51-53` defines verbatim as exact byte contiguity with newline normalization available *only* when the quote itself carries a newline, and states P19/P21/P22 are single logical lines. At the scored revision the strict oracle yields **1/4** (only P20), and the strict oracle cannot be repaired by reading the entry differently: the entry cells equal the frozen cells byte-for-byte. A counter that prints the frozen line therefore must use whitespace-run collapse **plus blank-line dropping** and span equality — the normalization the registration forbids. Under a strict counter the predicate self-fails at every content revision, including the round's final one; the kill rule ("any real pin, quote, or anchor mis-verifies → MISSED") would fire on the base tree, not on executor work. This is the same defect class the correction was written to fix: `corpus/lessons/round-52-verifier-spotcheck.md` §2 line 38 ("P16 fails — the space-joined quote") describes a space-joined quote; P19/P21/P22 are again space-joined. Resolution belongs to L1 pre-data (new versioned claims/registration file, or an explicit judge ruling naming whitespace-collapse + span-equality), not to an executor.

**D2 — blocking if taken literally: the recorded-digest file is misnamed in the freeze.**
`registration.md:12` says the hashes come "from its committed `SHA256SUMS.txt`". `.ufo/waves/round-52/fetch/` contains **`SHA256SUMS`** (no extension); `SHA256SUMS.txt` exists only in `.ufo/waves/round-54/fetch/` (the C2 pins). A counter that opens the frozen name finds nothing at round 52 → `pins=0/4`. `claims-frozen.md:81` and the C1-CTL-3 row do use the correct `SHA256SUMS`.

**D3 — operability: dangling reference to a table that is not in that file.**
`claims-frozen.md:81` declares C1 reads "…`.ufo/waves/round-52/fetch/` (+SHA256SUMS) and the frozen table of this file." `claims-frozen.md` contains **no** proposition table (`grep -n '^| P19\|^| P20\|^| P21\|^| P22'` → no rows; the only hit at line 81 is the reference itself). The pin/anchor/quote table lives in `registration.md:27-30`. A counter that derives the expected table from the frozen claims file alone has no table to check against.

**D4 — operability: the absolute-path checksum file is blind to mutated copies.**
`SHA256SUMS` records absolute paths under the lane root. Copying the tree and appending bytes to a pin, then running `sha256sum -c SHA256SUMS` in the copy still verifies the **lane originals** and prints OK for all five:

```
$ cp -a .ufo/waves/round-52/fetch/. $SCRATCH/relocated/ && printf 'TAMPER\n' >> $SCRATCH/relocated/Hyprland-ConfigActions.cpp
$ cd $SCRATCH/relocated && sha256sum -c SHA256SUMS
…ConfigActions.cpp: OK … (5×OK, rc=0)          # tampered copy hash 051bf1e8f903…7be8, original a83abeb5…7637
```

So any hash leg implemented as `sha256sum -c` is blind to a pin-byte control (it passes by construction), and a leg that resolves the recorded absolute path verbatim fails on any relocated checkout. The hash leg must hash exactly the bytes it read from `--rev` objects and compare only the digest field, keyed by basename. (C1-CTL-3's nibble mutation is caught either way, because the *recorded* value is what changes.)

**D5 — control discriminative power depends on the oracle D1 forbids.**
Simulating the six frozen controls (`registration.md:36-47`) over in-memory mutated copies of entry/SHA256SUMS/pins (no lane writes):

| control | strict exact-byte oracle (base 1/4) | ws-collapse, no anchor (base 4/4) | ws-collapse + exact span equality (base 4/4) |
|---|---|---|---|
| base | 1/4 | 4/4 | **4/4** |
| C1-CTL-1 spliced-quote | 1/4 (**= base**, non-discriminative) | 3/4 rejected | 3/4 rejected |
| C1-CTL-2 shifted-anchor `:1576→:1575` | 0/4 | 4/4 **admitted** | 3/4 rejected |
| C1-CTL-3 hash-tamper | pins 3/4 rejected | pins 3/4 rejected | pins 3/4 rejected |
| C1-CTL-4 wrong-range `:573` | 1/4 (**= base**) | 4/4 **admitted** | 3/4 rejected |
| C1-CTL-5 dropped P22 row | propositions 3/4 rejected | 3/4 rejected | 3/4 rejected |
| C1-CTL-6 swapped-pin → KeybindManager.cpp | 1/4 (**= base**) | 3/4 rejected | 3/4 rejected |

Reading: only the strict oracle makes CTL-2/CTL-4 bite *and* it simultaneously kills the base claim (and makes CTL-1/CTL-4/CTL-6 indistinguishable from truth, i.e. the "do-nothing" requirement is unmeetable); only the ws-collapse oracle admits the base, and only when anchored by **exact span equality** does it reject CTL-2/CTL-4. A no-anchor substring design is admitted by both anchor controls.

**D6 — control gap found by this seat: truncate-quote-keep-anchor is unguarded.**
No frozen control shortens a Quote cell while leaving its anchor. Measured input: P19 truncated to `g_pSeatManager->sendKeyboardMods(modMask, 0, 0, 0); if (S.m_passPressed == 1) {` with anchor still `1554-1558` →

- byte-exact: rejected (as with the genuine cell);
- ws-collapse **containment** oracle: **admitted** (span `(1554,1556)` ⊂ `1554-1558`), i.e. the mutant scores 4/4 like the base;
- ws-collapse **span-equality** oracle: rejected (3/4).

Same shape for the P22 wrong branch: `… .error = "sendshortcut: invalid key"};` genuinely exists at lines **579–580**, so a quote-only oracle admits it under anchor `573-574`; span equality rejects it. Requirement for the counter: span **equality**, never containment, never first/last-token search — the P19 tail line `…sendKeyboardKey(S.m_timeLastMs, key - 8, WL_KEYBOARD_KEY_STATE_PRESSED);` occurs **twice** (1558 and 1568), so token-based anchoring is ambiguous. Because D6 is not among the six frozen controls, it cannot be scored this round; it is a hardening requirement, reported not adopted.

## 5. Distinct inputs exercised by this seat (not duplicated elsewhere)

1. **Four-oracle battery** on the committed cells: exact substring, ws-collapse (no anchor), ws-collapse + span equality, per-line membership. Base scores 1/4, 4/4, 4/4, 4/4 — pinning D1 to an exact count rather than a judgement.
2. **Blank-line accounting inside spans** — P19 and P21 each contain one blank interior line, which is why newline-only normalization can never match (double space). This is a byte-level fact no “quote is/isn't found” check exposes.
3. **Truncate-quote-keep-anchor** (D6) and **wrong-branch co-located quote** — mutants that survive a containment oracle yet are not the frozen claim.
4. **`sha256sum -c` relocation blind spot** (D4) with the tampered-copy transcript.
5. **Checksum-file naming** mismatch (D2) and **dangling frozen-table reference** (D3).

## 6. Verdict for item 35

- Hashes: **4/4 exact match**, freeze record == round-52 record == recomputed bytes; pins at base are the committed blobs. No discrepancy.
- Anchor coordinates: **4/4 correct** (`1554-1558`, `1576`, `619-622` within 591–627, `573-574` after 571); supporting boundary claims (589 / 591 / 627 / 571) verified by brace-depth walk. No discrepancy.
- Quote cells: **1/4 byte-contiguous** (P20 only). P19/P21/P22 are space-joined reconstructions. This is a frozen-text defect, not entry drift: entry cells are byte-identical to the freeze.
- Net: PRED-C1-r54's frozen `quotes=4/4` label is unimplementable under the freeze's own "verbatim" clause; the predicate is satisfiable only under whitespace-run collapse with blank-line dropping and exact span equality, which `registration.md:51-53` forbids. Reported for the canonical Rust judge / L1; **no file was edited**.

## 7. Out of scope / not verified

- Upstream re-fetch: pins are static committed bytes; no host/network read was made, so the pins' correspondence to Hyprland commit `efb50993780079460b0cbed1363e2166a2de1d9f` (per `fetch/README.txt`) is **not** verified here.
- No `c1-r54-errata-truth.py` exists at base, so no counter behaviour, selftest count, `--work` handling, or `controls=6/6` leg was executed; D5's control matrix is a simulation of plausible oracles over mutated copies, not a run of the (absent) product counter.
- C2 items, README/registry, SOURCES rows, lesson, LOG/SCORECARD: untouched, unevidenced by this seat.
- `mado-verify.sh --selftest`, navigation counter, sources census: not run (main-agent verification surface).

## 8. Reproduction (exact snippets used, scratch-only)

```python
# contiguity + span oracle; PIN = pin file text, Q = frozen Quote cell
ws = lambda s: re.sub(r"\s+", " ", s)                       # collapse every whitespace run
def span(text, q):                                          # line span of the ws-collapsed match
    coll, prev = [], False
    for i, ch in enumerate(text):
        if ch.isspace():
            if not prev: coll.append(i)
            prev = True
        else: coll.append(i); prev = False
    i = ws(text).find(ws(q))
    if i < 0: return None
    s, e = coll[i], coll[i + len(ws(q)) - 1]
    return (text.count("\n", 0, s) + 1, text.count("\n", 0, e) + 1)
# anchors: equality (never containment) against the frozen Anchor cell
```

Scratch scripts (`anchors.py`, `oracles.py`, `relocated/`) were removed after the run; every number above is reproduced from the outputs quoted in §2–§5.
