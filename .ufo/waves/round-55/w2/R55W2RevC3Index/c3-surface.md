# R55W2RevC3Index — C3 landing surface attack

Scored revision: `57584ed67716340b3d466fa04333ac0bab3fb79e` (ancestor of HEAD `721ba9c`; `git diff --stat 57584ed HEAD -- corpus SKILL.md PROVINCE.md quality` is empty, so the surfaces below are identical at rev and HEAD). Lane tracked tree: 0 modified files at the time of the run. All reads are at the rev unless noted. Receipts: `receipts/` in this directory.

## T1 — README errata line (`corpus/README.md:81` at rev)

Holds: the errata filename `knowledge/hyprland-synthetic-dispatch-r52-errata-r53.md`, `P23`, and "round 55 appends P23, which supersedes P19" (verbatim, line 81).
The same row also carries the body sentence "(proposition P23, superseding P19) ... P19's \"only when `m_passPressed == 1`\" is withdrawn".

Verdict: **SURVIVES** (content matches the seat requirement).
Caveat, see T4/T5: nothing in the gate chain requires the "supersedes P19" words; the frozen counter accepts any README line naming the errata file with `P23`.

## T2 — Round-55 Frontier bullet (`corpus/README.md:118`)

Text: "its P19 said `Actions::pass` sends a PRESSED keyboard key only when `m_passPressed == 1`; the pinned `else` arm (`Hyprland-ConfigActions.cpp:1566-1569`) also sends PRESSED at line 1568. The correction block (P23, which supersedes P19) is in [the errata] ... Still open: a non-author sentence-to-pin audit of P23."

Pin check (`.ufo/waves/round-52/fetch/Hyprland-ConfigActions.cpp`, sha256 `a83abeb57175e65908d8d67ddc9802310134e5a4752fa3764f980401b48a7637`, identical to round-51's fetch copy):
`sed -n 1552,1578p` shows `} else {` at 1566 and `sendKeyboardKey(..., PRESSED)` at 1568, `RELEASED` at 1569. The Q-table line numbers in the errata (Q01 1554, Q02 1556, Q03 1558, Q04 1560, Q05 1561, Q06 1563, Q07 1565, Q08 1566, Q09 1568, Q10 1569, Q11 1571) match the pin by line.

Verdict: **SURVIVES**. The bullet itself declares the sentence-to-pin audit of P23 open, which this seat did not perform (out of scope).

## T3 — Other corpus text presenting P19's false sentence as current

Searches (run at the lane, read-only; outputs in `receipts/only-when-hits.txt`, `receipts/passpressed-hits.txt`):
- `grep -rn 'only when' corpus SKILL.md PROVINCE.md`: 79 hits in `corpus/` plus 3 in `SKILL.md` (340, 721, 726); 0 in `PROVINCE.md` (root file). Every hit except those listed below concerns another surface (walker, kitty, xkb, bind parsing, monitor, input devices, dispatch) and none states a PRESSED/`Actions::pass` claim.
- `grep -rn 'm_passPressed == 1'`: 13 hits (in `corpus/` plus `corpus/lessons/`). Full list in `receipts/passpressed-hits.txt`.
- `P19` grep over `corpus`, `SKILL.md`, root `PROVINCE.md`: hits only in README, the errata file, and lessons (below). `corpus/SOURCES.md` S371 row carries no P19 sentence.

P19-relevant hits:

| file:line | what it says | superseded marked? | verdict |
|---|---|---|---|
| `corpus/knowledge/hyprland-synthetic-dispatch-r52-errata-r53.md:17` | P19 row, "it sends a PRESSED keyboard key only when `m_passPressed == 1` ...", Support "direct" | **No.** The row has no status cell; the table is headed "Corrected propositions" and the withdrawal appears only as prose at :26–:30 and in README:81. | **BROKEN (minor landing defect)**: the false sentence stays in the live table with an unqualified support column. |
| `...errata-r53.md:28`, `:30` | "P23 supersedes P19 only ... P19 wording was false" | yes (prose) | SURVIVES |
| `...errata-r53.md:36` | P23 row, Supersedes = P19 | yes | SURVIVES |
| `...errata-r53.md:42, 51` | branch table and Q02 quote for `m_passPressed == 1` | n/a (P23 content) | SURVIVES (quotes match pin lines 1556) |
| `corpus/README.md:81` | errata index row, "P19's 'only when' ... is withdrawn" | yes | SURVIVES |
| `corpus/README.md:118` | Frontier bullet quoting P19 and its withdrawal | yes | SURVIVES |
| `corpus/knowledge/hyprland-dispatcher-dispatch-r51.md:185-187` | zero-argument `pass` overload (`Actions::pass(std::optional<PHLWINDOW>)`, `:1465` in r51 pin): `if (S.m_passPressed == 1)` at :1487, `== 0` at :1492, "a branch that sends both edges in one call (:1499-1500)" | not marked; it is not the P19 sentence | **NOT-REPRODUCED as a P19 restatement.** Its arm structure matches the r52 pin (:1499-1500 are two `sendKeyboardKey` calls, PRESSED then RELEASED). The phrase "in one call" is imprecise for two calls in one branch. Minor wording, no P19 claim. |
| `corpus/knowledge/hyprland-dispatcher-dispatch-r51.md:196` | `mouse` handler reads `m_passPressed == 1` as its PRESSED | n/a | unrelated to P19; NOT-REPRODUCED |
| `corpus/lessons/round-52-verifier-spotcheck.md:38`, `round-53-verifier-spotcheck.md:58` ("reject/supersede by P19–P20"), `round-54-verifier-spotcheck.md:61` ("existing r53 proposition remains"), `round-54.md:28` (M54-5, "pinned quote does not entail P19 proposition") | dated lesson/verifier records; `round-54.md:28` is the finding that caused the correction | lessons are append-only records, not corpus claims | HISTORICAL — not presented as current |
| `corpus/knowledge/hyprland-synthetic-dispatch-r52.md` (P16 row, :28) | P16 text "sends modifier state before the key event" | yes: README:80 says "P16–P18 are superseded" | SURVIVES (P16 is not the P19 sentence) |
| `SKILL.md`, root `PROVINCE.md`, `corpus/PROVINCE.md` (absent) | none | — | NOT-REPRODUCED (no P19 text) |

Verdict T3: **BROKEN (minor)** on the errata row at :17 (no in-row superseded marker on the live table row). No other current-surface presentation of P19's sentence found.

## T4 — `python3 -I quality/check-index.py --rev 57584ed… --repo …`

Output: `MADO_INDEX: rev=57584ed67716340b3d466fa04333ac0bab3fb79e indexed=70/70 missing=0 dangling=0 duplicates=0 coverage=10.0000/10`, exit 0. Re-counted independently: `git ls-tree` gives 70 `corpus/knowledge/*.md` blobs and the README has 70 `^| \`knowledge/...md\`` rows. Selftest: `MADO_INDEX_SELFTEST: 12/12 assertions passed`.

It is blind to content (its docstring says "navigation-completeness gate only ... says nothing about ... the semantic accuracy of the row text"). Controls on scratch copies (`receipts/check-index.txt`):
- control: errata row 81 deleted → `indexed=69/70 missing=1 ... missing: knowledge/hyprland-synthetic-dispatch-r52-errata-r53.md`, exit 1 (the gate can fail).
- mutant A: row 81 rewritten to drop "round 55 appends P23, which supersedes P19" from its header (P23 still in body) → `indexed=70/70 missing=0 ...`, exit 0.

Verdict T4: the index **is still complete at the rev** (SURVIVES as stated), but it is **not evidence** that the C3 correction landed: the gate passes when the supersession wording is removed.

## T5 — Frozen C3 counter's README leg (landing check for the seat requirement)

`quality/counters/c3-r55-p19.py` `readme_ok` (lines 234–241) = some README line contains `ENTRY_NAME` (`hyprland-synthetic-dispatch-r52-errata-r53.md`) AND `b"P23"`. `registration.md:123` defines the same leg ("no README line naming ... together with `P23`"). So the frozen contract does not require "supersedes P19".

Run at rev: `MADO_P19_FIX: rev=57584ed… prefix=identical rows=13/13 pin=ok p23=ok readme=ok verdict=TARGET_MET missed=none`, exit 0 (`receipts/c3-counter-rev.txt`).

Mutants, committed only in a scratch clone of the lane history (`receipts/c3-counter-mutants.txt`; the counter needs base commit `3b55b6e`, present in the clone):
- mutant A (commit `2e19ebec`): row 81 without "supersedes P19" → `readme=ok verdict=TARGET_MET`.
- mutant C (commit `254f4bdb`): row 81 replaced by "round 55 appends P23 as a non-binding note | P19 remains the current proposition; the round-55 P23 block is a non-binding note." → `readme=ok verdict=TARGET_MET`. The Frontier bullet at README:118 still says "P23, which supersedes P19", so the counter reads only the row it was built for.

Verdict T5: **BROKEN as a landing guard against the seat requirement** ("README line must say it supersedes P19"). The frozen predicate is satisfied by a row that asserts P19 is current. This is a gap between the seat requirement and the frozen predicate, not a rev defect (the rev's row is correct, T1). Reproducer: the commands in `receipts/c3-counter-mutants.txt`.

## Not verified / limits
- The P23 proposition's sentence-to-quote entailment (the bullet's own open item) was not audited.
- The `c3-r55-p19.py` self-test and the other C3 legs were not run; only the rev and mutant runs above.
- check-index was run at the rev, not at HEAD `721ba9c` (the diff over the checked paths is empty).
- No tool was installed. No host command beyond the lane reads was run; no hyprctl call was made.
