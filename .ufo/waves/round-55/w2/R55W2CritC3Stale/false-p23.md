# False P23 through the C3 counter (seat R55W2CritC3Stale)

Target: `quality/counters/c3-r55-p19.py` as committed at 57584ed67716340b3d466fa04333ac0bab3fb79e
(sha256 9259af01e43c5acdbefe4425d404e5592b00596f251d53582a2daf94a47d3859, identical to the working-tree file).
Driver: `receipts/attack.py`. Scratch repo: `git init` + alternates onto the lane's read-only object store; every
variant is one commit made with plumbing (`read-tree 57584ed`, `hash-object -w`, `update-index`, `write-tree`,
`commit-tree -p 57584ed -c user.name=ctl -c user.email=ctl@ctl`). The lane was not written. Each variant changes ONLY
the P23 row's proposition cell (or appends prose); `git diff` against 57584ed shows one changed line for V1
(`receipts/evidence.txt`).

## Result: a false P23 passes

Input (V1): the P23 row of the round-55 correction block, proposition cell replaced. Everything else byte-identical,
including the heading, all 13 Q rows, the Pin:anchor cell, the Source row cell and the README line. The false part:
the `else` arm is said to send only a keyboard RELEASED and never a keyboard PRESSED. The pin says the opposite
(`Hyprland-ConfigActions.cpp:1568` sends keyboard PRESSED, `:1569` keyboard RELEASED).

```
| P23 | P19 | `Actions::pass` sends modifier state (`sendKeyboardMods`) before its delivery branch and clears it after
that branch. The branch tests `m_passPressed`. When `m_passPressed == 1`, a non-mouse key sends a keyboard key PRESSED
and a mouse button sends a pointer button PRESSED. When `m_passPressed == 0`, a non-mouse key sends a keyboard key
RELEASED and a mouse button sends a pointer button RELEASED. When `m_passPressed` is any other value (the `else` arm),
the branch sends only a keyboard key RELEASED and never a keyboard key PRESSED. | S371 | Hyprland-ConfigActions.cpp:1554-1576 | Q01 to Q13 below | direct: ... |
```

Command: `python3 -I /fast/scratch/hyaku/mado-r55/R55W2CritC3Stale/c3-committed.py --repo <scratch> --rev 267088e79f61cb191f9df4441adbd4874066b307 --work <scratch>/w-V1`

Output (exit 0):
```
MADO_P19_FIX: rev=267088e79f61cb191f9df4441adbd4874066b307 prefix=identical rows=13/13 pin=ok p23=ok readme=ok verdict=TARGET_MET missed=none
```

Full predicate (`python3 -I quality/check-r55-controls.py --claim c3 --repo <scratch> --rev <same> --work <w> --counter <committed>`):
```
MADO_R55_CONTROLS: claim=c3 good=ok controls=6/6 verdict=OK      (exit 0)
```
So PRED-C3-r55, as frozen, is satisfied by a P23 that states something the pin refutes.

## Variants (counter line, exit code; full list in `receipts/results.json`)

| Variant | Attack | Counter verdict | Full predicate |
|---|---|---|---|
| V1 | else arm "only RELEASED, never PRESSED" | TARGET_MET, rc 0 | 6/6 OK |
| V2 | else arm "keyboard keys are never sent" | TARGET_MET, rc 0 | not run |
| V3 | P19 falsehood restated: "A keyboard key PRESSED is sent оnly when `m_passPressed == 1`" with Cyrillic U+043E; plus V1's else-arm claim | TARGET_MET, rc 0 | 6/6 OK |
| V4 | `only\u200bwhen` (zero-width space) restating P19 | TARGET_MET, rc 0 | 6/6 OK |
| V5 | `only\u00a0when` (NBSP) | TARGET_MET, rc 0 | not run |
| V6 | `only&#32;when` (HTML entity) | TARGET_MET, rc 0 | not run |
| V7 | `only  when` (double space) | TARGET_MET, rc 0 | not run |
| V8 | `only\twhen` (tab) | TARGET_MET, rc 0 | not run |
| V9 | `ONLY\tWHEN` | TARGET_MET, rc 0 | not run |
| V10 | fullwidth `ｏｎｌｙ ｗｈｅｎ` | TARGET_MET, rc 0 | not run |
| V11 | V1 with compact spacing `\|P23\|P19\|...` | TARGET_MET, rc 0 | **5/6 FAIL** (harness limitation: its `find_row` needs `\| P23 \|`; the counter itself passes) |
| V17 | true P23 + prose paragraph `only` NEWLINE `when` | TARGET_MET, rc 0 | not run |
| V18 | V1 row + prose paragraph `only` NEWLINE `when` restating P19, and "else arm sends only a keyboard key RELEASED" | TARGET_MET, rc 0 | 6/6 OK |

Controls that the counter DOES reject (so the bypass is specific, not a blanket pass):

| Variant | Input | Output |
|---|---|---|
| V12 | P23 with ASCII `only when` | TARGET_MISSED missed=stale, rc 1 |
| V13 | P23 with ASCII `ONLY WHEN` | TARGET_MISSED missed=stale, rc 1 |
| V19 | V1 row + P19 sentence verbatim in prose | TARGET_MISSED missed=stale, rc 1 |
| V14 | `==` followed by U+00A0 then `1` | TARGET_MISSED missed=p23, rc 1 (non-reproducing: syntactic rejection) |
| V15 | `Pressed` instead of `PRESSED` | TARGET_MISSED missed=p23, rc 1 (non-reproducing: syntactic rejection) |
| V16 | P23 row split across a line break | TARGET_MISSED missed=p23, rc 1 (non-reproducing: a markdown row cannot span lines; the counter reads the fragment as no row) |

## What the counter proves and what it does not

The lexical leg (`p23`) checks, for the one row whose first cell is `P23`: Supersedes = `P19`, Source = `S371`, Pin:anchor
= `Hyprland-ConfigActions.cpp:1554-1576`, and that the proposition cell contains the substrings `m_passPressed`,
`== 1`, `== 0`, `PRESSED`, `RELEASED` and one of `otherwise`/`any other`/`else` (case-sensitive, anywhere in the cell).
Every one of those is satisfied by V1 while the else-arm sentence is false. Those are facts about vocabulary and row
shape. Whether the proposition follows from the quoted pin lines is not a property the counter reads.

The `stale` leg checks only ASCII `only when` after ASCII lower-casing (Python `bytes.lower()`) and the exact base P19
proposition text. It misses every non-ASCII lookalike, every whitespace variant other than a single ASCII space, a
line break inside prose, and any restatement that changes one character of the P19 sentence. V3, V4, V5, V6, V7, V8,
V9, V10, V17 and V18 demonstrate this.

Therefore the truth of P23 rests entirely on the sentence-to-pin audit (R55W2RevP23), not on C3. Reading the pin
directly (`git show 57584ed:.ufo/waves/round-52/fetch/Hyprland-ConfigActions.cpp | sed -n 1566,1576p`, sha256 a83abeb5...)
refutes V1 and V2; that reading is mine, not an audit output, and it is the reading the audit must reproduce.

Not claimed: runtime delivery, the real lane's P23 wording beyond what these variants change.
