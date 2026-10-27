# R54W2Seat02 — w2 falsification: item 2, the C1 P21 quote judge (raw bytes vs registered normalization)

Seat: `R54W2Seat02`, wave `w2`, lane root `/home/vgpnk/Projects/shokunin/mado-shokunin`.
Base `e25149fec8152a3aabd2b18a0ee8663b23cf65aa`; freeze commit `350d30e4ec5531f65ce99a57efeb8216f38e678a`
(measured `git rev-parse HEAD` → same; base is its parent). Item 2 of the w2 dispatch: **the P21
quote judge of PRED-C1-r54** — literal vs whitespace-normalized matching, and the exact anchor.

Compliance: read-only against the lane — the only file written is this report; no git/jj mutation,
no fixtures were needed (all measurements come from git blobs via `git show` plus the frozen wave
files in memory), no subagent, no install, no producer/host probe. Scratch
`/fast/scratch/hyaku/mado-r54/R54W2Seat02` was created explicitly, held only `p21_probe.py`
(stdlib-only, `python3 -I`), and was removed before yield (removal receipt in the seat result).

## 1. Ground re-measured (two revs; all byte-level)

`git status --porcelain`: only ` M corpus/SOURCES.md` (C2 integration surface, not this item) plus
untracked wave dirs — every file this seat reads is clean, so worktree bytes equal the freeze
commit for `registration.md`/`claims-frozen.md`; the entry and pins were read **from git objects**
at both revs.

```
$ git -C <lane> show e25149fe:.ufo/waves/round-52/fetch/<pin> | sha256sum
Hyprland-ConfigActions.cpp                  a83abeb57175e65908d8d67ddc9802310134e5a4752fa3764f980401b48a7637   match_frozen=True
Hyprland-ConfigActions.hpp                  746c6f517620eb039afbfbb9a4a0e2d5ba1c5eb117bcc8f396173f63091b7073   match_frozen=True
Hyprland-KeybindManager.cpp                 8d8f35fc84c4a2f8de63ac2bf6f6531c651c6fa6d37b1aac7c8fc5d9342d4e40   match_frozen=True
Hyprland-legacy-DispatcherTranslator.cpp    7248cbb89f898c783c50c89d068df9821a6b38aeb6abeb6064e92c1610fbe771   match_frozen=True
$ git -C <lane> show 350d30e4:corpus/knowledge/hyprland-synthetic-dispatch-r52-errata-r53.md | sha256sum
764f48679447fd62858e9773607a3c0bee5395b6182bdf9f30f5d7c95f4d0b65     # identical at e25149fe and 350d30e4
```

Entry P21 row raw bytes (entry line 19, 7 cells; `cat -A` shows the only non-ASCII bytes are the
en/em dashes of the trailing note cell — none enter the quote cell):

```
| P21 | P17 | `sendkeystate` calls `sendshortcut` again when its state is `repeat` and the first
call succeeds. | S370 | Hyprland-legacy-DispatcherTranslator.cpp:619-622 | `auto result =
sendshortcut(modifiedArgs); if (keyState == 2 && result.success) result =
sendshortcut(modifiedArgs);` | direct — the repeat branch is inside `sendkeystate` (lines 591–627);
`sendshortcut` ends at line 589. |
```

- Entry pin:anchor cell = `Hyprland-legacy-DispatcherTranslator.cpp:619-622` (plain cell;
  `rsplit(":", 1)` → pin basename + `619-622`).
- Entry quote cell is byte-equal **RAW** to the frozen P21 cell of `registration.md:29` — not
  merely modulo trailing spaces; trailing-space drift `0` (entry) / `0` (frozen).
- Frozen quote P21: 115 bytes, ASCII, **no newline, no tab**. All four frozen quotes carry no
  newline: P19=182 B, P20=45 B, P21=115 B, P22=80 B (measured on `registration.md:26-30`).

## 2. Finding F1 (falsification-grade): the registered judge sentence, read literally, fails the honest base

Attacked sentence — `registration.md:51-53`:

> Judge of "verbatim": exact byte contiguity after single-space normalization of interior newlines
> ONLY where the frozen quote itself carries a newline (P19/P21/P22 are single logical lines).

Measured: **no frozen quote carries a newline**, so the rule's conditional normalization never
fires; all four quotes must occur byte-exact. Raw-byte occurrence counts of each frozen quote in
the pin named by its own row (git blobs, both revs identical):

| quote | pin | raw byte-exact count | registered-rule (REG) count | newline→space (NL) count |
|---|---|---|---|---|
| P19 | ConfigActions.cpp | **0** | **0** | 0 |
| P20 | ConfigActions.cpp | 1 | 1 | 1 |
| P21 | legacy-DispatcherTranslator.cpp | **0** | **0** | **0** |
| P22 | legacy-DispatcherTranslator.cpp | **0** | **0** | 0 |

→ under the literal registered judge, `quotes=1/4` → `verdict=TARGET_MISSED` at the honest base,
contradicting `claims-frozen.md:22-24` ("Quote cell occurring verbatim and contiguous") which the
same freeze makes the target. Even the stronger newline→space rewrite (ignoring the quote-carries-
newline condition) finds nothing: the pin region carries 4/8-space indentation that survives.

Why: the frozen quotes are **whitespace-collapsed renderings of multi-line pin regions**. P21's
pin region raw bytes (`repr`, LF-terminated, no CRLF — `p.count(b"\r")=0`, non-ASCII `0`):

```
  618: b''
  619: b'    auto result = sendshortcut(modifiedArgs);'
  620: b''
  621: b'    if (keyState == 2 && result.success)'
  622: b'        result = sendshortcut(modifiedArgs);'
  623: b''
  626: b'    return result;'
  627: b'}'
```

The frozen P21 cell is lines 619+621+622's content joined with single spaces, indentation dropped,
blank 620 collapsed away. The parenthetical "(P19/P21/P22 are single logical lines)" is true of the
**entry cells** (measured: no newline in any quote cell) and **false of the pin regions** (P21
spans 4 physical lines, P19 five, P22 two). The sentence cannot be satisfied as written and its
own factual premise is wrong about the pins.

Under the only matching judge that keeps "verbatim" meaningful — **N1: collapse every pin
whitespace run to one space, then require the quote byte-verbatim and contiguous in the collapsed
text** (line span recovered via a char→line map) — all four quotes are found at unique, exact
spans: P19 `1554-1558`, P20 `1576`, P21 `619-622`, P22 `573-574` → `quotes=4/4`. Full judge table
(this rev; identical at both revs):

| judge | quotes leg | per-proposition |
|---|---|---|
| A_raw (byte-exact) | **1/4** | P19 MISS, P20 ok, P21 MISS, P22 MISS |
| REG (registration.md:51-53 literal) | **1/4** | same |
| NL (newline→space, indentation kept) | **1/4** | same |
| N1 (pin \s-run collapse, quote verbatim) | **4/4** | all ok at exact frozen spans |
| N2 (collapse both sides) | 4/4 | spans equal, but see §4 |
| N3 (`\s+`-joined regex from quote) | 4/4 | spans equal, but see §4 |

Per `claims-frozen.md:5-7` this falsifies the **registered judge sentence as written** (not the
claim: the predicate stays reachable under N1). Fixing it is a pre-data v2 re-registration wording
matter for the L1 — no predicate/registration file may be edited now, and this seat edited none.

## 3. P21 exact anchor, quantified (under N1, the only satisfying judge)

- **Uniqueness**: exactly one N1 match in the pin — `hits=[(619, 622)]`. Although
  `sendshortcut(` occurs on lines `[531, 619, 622]`, line 531 cannot form the quote (the quote
  requires the `if (keyState == 2 && result.success)` guard between two calls); the anchor is
  unambiguous.
- **Exact span**: `(619, 622) == (619, 622)` → True (exact-span equality, not containment).
- **Side-claims** (`claims-frozen.md:26-27`, `registration.md:33-34`): `591 ≤ 619` True — line 591
  is ``b'static SDispatchResult sendkeystate(const std::string& args) {'``; `622 ≤ 627` True —
  line 627 is ``b'}'`` (with `626: b'    return result;'`). The repeat branch is measurably inside
  `sendkeystate` 591–627, as the entry's note cell asserts (`sendshortcut` closes at 589:
  ``b'}'`` — also measured).
- **Cross-pin**: the P21 quote is absent from the other three pins under raw **and** N1 matching
  (counts 0/0 for ConfigActions.cpp, ConfigActions.hpp, KeybindManager.cpp) — the CTL-6 semantics
  (`registration.md:47`) hold for P21's row, not just P19's.
- **CTL-4 (`registration.md:45`) — NOT RUN as a control (no counter exists; see §5), derived
  statically**: with the entry anchor moved to `:573`, the located span (619,622) ≠ (573,573) and
  `573 < 591`, so the side-claim fails and the anchors leg drops — but only under **exact-span**
  equality. Containment-only or ±1-tolerant anchor judges cannot be discriminated by CTL-4 alone
  (w1 Finding 3, `w1/R54Seat02.md:162-194`); w2 re-affirms that derivation from today's measured
  span, without re-running mutated trees (no counter → nothing to run it against).

## 4. Gameability of each normalization (quantified, in-memory variants of the entry quote)

Four re-spaced variants of the P21 entry quote were matched against the honest pin
(V1 `;  if (` double space, V2 `)  result` double space, V3 leading tab before `=`, V4 NBSP inside
`if (keyState`); the frozen-table leg is `registration.md:21-23` (entry rows checked
"byte-for-byte modulo trailing spaces" against the frozen table):

| variant | A_raw | N1 (pin collapsed, quote VERBATIM) | N2 (both collapsed) | N3 regex | table leg drops |
|---|---|---|---|---|---|
| V1 `;  if (` | 0 | **[] reject** | match @619-622 | match @619-622 | True |
| V2 `)  result` | 0 | **[] reject** | match @619-622 | match @619-622 | True |
| V3 tab | 0 | **[] reject** | match @619-622 | [] (tab is literal in the regex) | True |
| V4 NBSP | 0 | [] | [] | [] | True |

Reading: N1 is the only judge that rejects every re-spacing **at the quotes leg itself**. N2/N3
admit V1–V3 — the quote the entry does not carry verbatim "verifies" — and the tree is still
rejected only because the frozen-table comparison fires (`propositions=3/4`). That is safe
end-to-end but migrates the failure from `quotes` to `propositions`: a builder that skips the
frozen-table check and uses N2/N3 is exploitable by a one-character re-spacing (w1 Finding 2,
`w1/R54Seat02.md:140-160`, re-confirmed quantitatively). V4 (NBSP) is rejected by every judge in
bytes mode — NBSP folding must **not** be added, or the verbatim judge degrades to N2.

## 5. Pinned command status: NOT RUN — counter absent

```
$ cd /home/vgpnk/Projects/shokunin/mado-shokunin && ls quality/counters | grep -c r54
0        (grep exit 1 — no r54 counters)
$ test -f quality/counters/c1-r54-errata-truth.py ; echo $?
1        (file absent)
```

`python3 -I quality/counters/c1-r54-errata-truth.py --repo . --rev e25149fe…` — **NOT RUN / absent**
at HEAD `350d30e4`. Consistent with the frozen before-state (`claims-frozen.md:32-33`: no
`c1-r54-*` counter at base, `receipts/before.txt` TARGET_MISSED by absence). No control run, no
counter output exists to re-verify; nothing was invented to fill that gap.

## 6. Frozen-contract citations used

- `claims-frozen.md:22-30` — clause (a) verbatim+contiguous, clause (b) P21 "at exactly
  DispatcherTranslator.cpp:619-622 inside lines 591–627", clause (c) hashes, clause (d) controls.
- `claims-frozen.md:5-7` — no post-score edits; falsified predicate ⇒ honest stop or NEW v2 file.
- `claims-frozen.md:32-33` — before-state (counter absent).
- `registration.md:21-23` — frozen-table leg (byte-for-byte modulo trailing spaces; drift ⇒ MISSED).
- `registration.md:29` — frozen P21 row (pin/anchor/quote cells).
- `registration.md:33-34` — P21 side-claims `591 ≤ 619`, `622 ≤ 627`.
- `registration.md:45` — C1-CTL-4 wrong-range; `registration.md:47` — C1-CTL-6 swapped-pin.
- `registration.md:51-53` — the attacked judge sentence.
- w1: `.ufo/waves/round-54/w1/R54Seat02.md:79-138` (F1 non-contiguity), `:140-160` (F2 table leg
  load-bearing), `:162-194` (F3 exact-span anchor), `:322-331` (open question 1 — judge ambiguity).

## 7. Verdict, residual risk, verification gaps

**Item-2 verdict**: the P21 quote judge sentence `registration.md:51-53` is **falsified as
written** — under its literal reading the honest base scores `quotes=1/4 → TARGET_MISSED`
(measured at both `e25149fe` and `350d30e4`; pins hash-verified; entry cell byte-identical to the
frozen table). The predicate itself is **reachable** only under the pin-whitespace-collapse reading
(N1), under which every quote is unique and every anchor span is exactly the frozen one — P21 at
`619-622`, unambiguous, inside `sendkeystate` 591–627. This is exactly the ambiguity w1 Finding 1
flagged; w2 re-derived it independently, byte-for-byte, and adds the quantified judge/gameability
table (§2, §4). Per `claims-frozen.md:5-7` the resolution belongs to a v2 re-registration
sentence, not to any seat's edit.

**Residual risk / gaps**: (1) the six frozen controls were not re-executed — no counter exists to
run them against; §3's CTL-4 statement is a static derivation, not a control run. (2) The quotes
leg under N1 was verified against the committed pins at two revs; a future re-pin would need
re-measurement (clause (c) hash leg binds the bytes, measured matching). (3) `corpus/SOURCES.md`
was modified in the worktree by another seat (C2 surface); none of this item's inputs read it.
No scratch remains; no ENOSPC observed (`df -h /fast`: 580 G available at seat start).
