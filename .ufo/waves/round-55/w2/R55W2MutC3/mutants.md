# R55W2MutC3 — mutation test of the C3 counter and its harness

Scope: `quality/counters/c3-r55-p19.py` (counter) and `quality/r55_ctl_c3.py` (harness, dispatched by `quality/check-r55-controls.py --claim c3`), lane revision `57584ed67716340b3d466fa04333ac0bab3fb79e`.

Method (all mutants are COPIES in scratch; nothing in the lane was edited, committed or reset):

- Unchanged baseline on a scratch repo `R` (objects fetched read-only from the lane, then a `ctl` commit `1f484da6285b5f38848945bc1c1d60d9e3383726` whose tree is `git archive 57584ed` and whose parent is the base `3b55b6e`; tree hash `feecf8d8…` equals the lane tree):
  - counter selftest: `41/41 passed`
  - harness: `good=ok controls=6/6 verdict=OK`
- Each counter mutant (one line changed; `receipts/R1-R9-decisive.txt` R9 counts 2 diff lines = one removed + one added line for every mutant) was run through (a) its own selftest `--selftest --repo R --rev G --work …` and (b) the independent harness `check-r55-controls.py --claim c3 --repo R --rev G --work … --counter <mutant>`.
- Each harness mutant (one edit to `r55_ctl_c3.py`, in a private tree with the unchanged dispatcher) was run against an always-green stub counter (`STUB-always-green.py`, prints the green line for any `--rev`) and against the targeted counter that the mutant would have to admit.
- Survivor = nothing catches the mutant. For each survivor a proposed kill test was built as a real commit and run on the UNCHANGED counter and on the survivor (`receipts/verify.json`).

Result: 38 counter mutants: 28 killed (27 by the counter's own selftest, 14 by the independent harness, 13 by both; C21 only by the harness), 8 survive both, 2 are equivalent (C10, C29). 8 harness mutants: 3 survive a targeted counter (H01, H03, H05), 1 survives the always-green stub (H06), 2 are equivalent (H02, H04). H01, H03 and H05 die to the always-green stub only because their other controls still fail. Per-mutant numbers and kill columns follow.

Legend: `st` = counter selftest (`MADO_P19_FIX_SELFTEST: n/41`); `h` = independent harness control(s) reporting FAIL (`CTL-k`) or `good` (the good tree itself failing). "killed by" names what fails the mutant; "risk" is survivor risk for the shipped pair.

## 1. Counter mutants (`mutants/C*.py`)

| ID | edit (one line; `old → new`) | st | h | killed by | survivor risk |
|---|---|---|---|---|---|
| C01 | drop prefix leg: `missed.append("prefix")` → `pass` | 36/41 | CTL-2 | selftest + harness CTL-2 | low |
| C02 | drop Q-row legs (keep heading): `missed += row_missed` → heading-only filter | 31/41 | CTL-3, CTL-4 | selftest + harness | low |
| C03 | drop heading leg: `row_missed.insert(0,"rows:heading")` → `pass` | 39/41 (`heading missing`, `heading only inside a fence`) | none | selftest only | medium: the independent harness has no heading control |
| C04 | drop pin leg: `missed.append("pin")` → `pass` | 38/41 (`pin tampered`, `pin absent`, `frozen-tables absent`) | none | selftest only | medium: no harness control changes the pin, so the pin leg is never exercised by the harness |
| C05 | drop p23 leg: `missed.append("p23")` → `pass` | 32/41 | CTL-1, CTL-2 | selftest + harness | low |
| C06 | drop stale leg: `missed.append("stale")` → `pass` | 39/41 (`CTL-5 …`) | CTL-5 | selftest + harness | low |
| C07 | drop readme leg: `missed.append("readme")` → `pass` | 38/41 | CTL-6 | selftest + harness | low |
| C08 | drop tables_sha leg: `missed.append("tables_sha")` → `pass` | 39/41 (`frozen-tables differs`, `absent`) | none | selftest only | medium |
| C09 | weaken stale to case-sensitive: `… in block.lower()` → `… in block` | 41/41 | none | **SURVIVES both** → killed by proposal V1 (§4) | **high**: a `Only when …` re-assertion that is not the verbatim P19 sentence passes |
| C10 | disable stale exact-sentence leg: `cl[2] and cl[2] in block:` → `cl[2] and False:` | 41/41 | none | **EQUIVALENT**: the P19 sentence contains `only when`, so leg 1 fires on every block that leg 2 would match | none |
| C11 | P23 token list: drop `b"RELEASED"` | 41/41 | none | **SURVIVES both** → V2 | medium |
| C12 | P23 token list: drop `b"== 0"` | 40/41 (`P23 lacks == 0`) | none | selftest only | low |
| C13 | P23 token list: drop `b"== 1"` | 41/41 | none | **SURVIVES both** → V3 | medium |
| C14 | P23 token list: drop `b"m_passPressed"` | 41/41 | none | **SURVIVES both** → V4 | medium |
| C15 | P23 alt list: drop `b"else"` | 41/41 | none | **SURVIVES both** → V5 (P23 row with `any other value` removed and `else` kept must be MET; C15 says MISSED) | medium |
| C16 | P23 alt list: drop `b"otherwise"` | 40/41 (`CTL-5 v2`) | CTL-5 | selftest + harness (accidental: the stuffed text's only alt word is `otherwise`) | low |
| C17 | P23 Pin:anchor check removed (`and c[4] == P23_ANCHOR`) | 41/41 | none | **SURVIVES both** → V6 (anchor `1554-1576 → 1554-1558`) | **high**: the anchor cell is a checked claim location and no control inspects it |
| C18 | P23 Supersedes check removed (`c[1] == b"P19"`) | 40/41 (`P23 supersedes P20`) | none | selftest only | medium |
| C19 | P23 Source-row check removed (`c[3] == b"S371"`) | 40/41 (`P23 wrong source row`) | none | selftest only | medium |
| C20 | P23 exactly-one relaxed to `>= 1` | 40/41 (`duplicated P23 row`) | none | selftest only | low |
| C21 | BASE constant: last hex digit `…d5` → `…d4` | 41/41 (selftest passes `base_commit` in-process, never reads `BASE`) | good=bad, CTL-1…6 all SETUP | harness only | medium: the selftest is blind to the BASE constant |
| C22 | Q id range `range(1, NQ + 1)` → `range(1, NQ)` (Q13 dropped) | 40/41 | good=bad, CTL-3…6 | selftest + harness | low |
| C23 | Q id range → `range(2, NQ + 1)` (Q01 dropped) | 40/41 | good=bad, CTL-3…6 | selftest + harness | low |
| C24 | CRLF accepted in prefix: `entry.startswith` → `entry.replace(b"\r\n", b"\n").startswith` | 39/41 (`prefix with CRLF …`, two cases) | none | selftest only | medium: no harness control |
| C25 | duplicate Q rows accepted: `len(rs) == 1` → `len(rs) >= 1` | 39/41 (`duplicated Q03 row`, `… elsewhere`) | none | selftest only | medium |
| C26 | Q pin:line anchor check removed | 40/41 (`Q row anchor line shifted`) | none | selftest only | medium |
| C27 | Q quote check removed | 39/41 | CTL-3 | selftest + harness | low |
| C28 | pin sha256 check removed (`if pb is not None:`) | 40/41 (`pin tampered`) | none | selftest only | medium |
| C29 | pin quote-at-line check removed | 41/41 | none | **EQUIVALENT under constants**: the sha256 check pins the pin bytes and the frozen quotes are frozen equal to those bytes | none |
| C30 | readme P23 requirement removed | 39/41 | CTL-6 | selftest + harness | low |
| C31 | heading ATX `#` requirement removed (`if HEADING in s:`) | 41/41 | none | **SURVIVES both** → V7 | medium |
| C32 | fenced code blocks not skipped (`if m:` → `if False:`) | 36/41 (5 fence cases) | none | selftest only | low |
| C33 | stale tested on whole entry (`… in entry.lower()`) | selftest crashes (`AttributeError`, entry None) | good=bad, CTL-3, 4, 6 | harness + crash | low |
| C34 | TABLES_SHA256 constant changed (one hex digit) | selftest `SETUP tables_missing_or_changed` (rc 2) | good=bad, CTL-1…6 | selftest + harness | low |
| C35 | P23 tokens `all()` → `any()` | 40/41 (`P23 lacks == 0`) | none | selftest only | low |
| C36 | tables sha check reduced to blob presence | 40/41 (`frozen-tables differs`) | none | selftest only | low |
| C37 | stale only-when leg removed (`stale = False`) | 41/41 | none (CTL-5's verbatim P19 sentence is still caught by leg 2) | **SURVIVES both** → V1 | **high**: the only-when leg has no control of its own |
| C38 | pin quote read one line late (`lines[ln]`) | 14/41 | good=bad, CTL-1, 4, 5, 6 | selftest + harness | low |

Targeted counters used against harness mutants (one line each):

| ID | edit | st | h (unmodified harness) | role |
|---|---|---|---|---|
| T01 | stale leg reported as `rows:heading` | — | CTL-5 FAIL (`unexpected row leg(s) ['heading']`) | H02 target |
| T02 | `if stale:` → `if stale or not readme_ok:` (CTL-6 over-reports `stale`, fields consistent) | — | CTL-6 FAIL (`unexpected leg(s) ['stale']`) | H03 target |

## 2. Harness mutants (`mutants/H*-r55_ctl_c3.py`, dispatcher unchanged)

| ID | edit | vs always-green stub | vs targeted counter (mutant harness / unmodified harness) | verdict |
|---|---|---|---|---|
| H01 | skip CTL-5 (`CONTROLS` loses the entry) | `controls=0/6 verdict=FAIL` (killed by CTL-1…4, 6) | counter C06 (stale dropped): mutant `controls=5/6 verdict=OK`; unmodified `controls=5/6 verdict=FAIL` | **SURVIVES**: the final check is `passed == len(CONTROLS)` while the printed denominator is the literal `6`, so a shorter control list is green |
| H02 | CTL-5 required leg `{"stale"}` → `set()` | `controls=0/6 verdict=FAIL` | T01: `5/6 verdict=FAIL` (mutant and unmodified) | **EQUIVALENT**: CTL-5 allows only `{stale}` and no rows; a nonempty `missed=` therefore forces `other == {stale}` |
| H03 | CTL-6 allowed set adds `pin,p23,stale,prefix` | `controls=0/6 verdict=FAIL` | T02: mutant `controls=6/6 verdict=OK`; unmodified `5/6 verdict=FAIL` | **SURVIVES** for `stale` (`pin` and `p23` are field-pinned, so over-reporting them is caught by the field check) |
| H04 | drop `if d["verdict"] != "TARGET_MISSED"` admission check | `controls=0/6 verdict=FAIL` (killed by each control's must-leg) | not run separately | **EQUIVALENT**: every control has a nonempty must-set, so a MET verdict with `missed=none` fails the must check anyway |
| H05 | skip CTL-6 | `controls=0/6 verdict=FAIL` (killed by CTL-1…5) | C07 (readme dropped): mutant `controls=5/6 verdict=OK`; unmodified `5/6 verdict=FAIL` | **SURVIVES**: same length-not-pinned gap as H01 |
| H06 | `passed == len(CONTROLS)` → `passed >= 0` | `controls=0/6 verdict=OK` (the six FAIL lines are still on stderr; the verdict line is what a predicate reads) | — | **SURVIVES the always-green stub**: the stub is caught only by this one comparison |

Unmodified harness against the always-green stub (`receipts/R1-R9-decisive.txt`, R7): `good=ok controls=0/6 verdict=FAIL`, rc 1. So the unmodified harness kills the stub; H06 is the one-line edit that does not.

## 3. Survivors and proposed kill tests (text; run in §4)

- **C09 / C37 (stale only-when leg)** → add control CTL-5b: keep P23 correct and append, outside any table, one prose line `Only when `m_passPressed == 1` does `Actions::pass` send a PRESSED keyboard key.` (no verbatim P19 sentence). Expect `TARGET_MISSED missed=stale`. Kills C09 (case-sensitive) and C37 (leg removed).
- **C11, C13, C14 (P23 token list)** → one control per dropped token: CTL-7a `RELEASED` → `released` in the `| P23 |` row (expect `missed=p23`); CTL-7b `== 1` → `is 1`; CTL-7c `m_passPressed` → `passPressed`.
- **C15 (P23 alt list)** → CTL-7d: remove `any other value` from the P23 row and keep `else` (expect MET; the mutant says MISSED).
- **C17 (Pin:anchor)** → CTL-7e: P23 Pin:anchor `…:1554-1576` → `…:1554-1558` (expect `missed=p23`).
- **C31 (ATX heading)** → CTL-8: `## Correction (round 55): …` → plain line `Correction (round 55): …` (expect `missed=rows:heading`).
- **H01 / H05 / H06 (control count)** → one assertion in the harness: `ok = … and passed == 6 == len(CONTROLS)` (or assert `len(CONTROLS) == 6` before running). Without it a shorter list or a `>= 0` comparison passes.
- **H03 (collateral legs)** → pin the allowed set per control to exactly the frozen expectation (drop the `allow` widening) and add a control that over-reports `stale` in CTL-6 (= T02) expecting FAIL.
- **Harness blind spots for counter legs** (killed only by the counter's own selftest, which is authored by the same agent, so not independent): C03, C04, C08, C12, C18, C19, C20, C24, C25, C26, C28, C32, C35, C36. Minimal independent controls would be: heading removed (for C03), a pin byte change (C04, C28), tables file change (C08, C36), a second `P23` row (C20), CRLF after the prefix (C24), duplicated `Q03` row (C25), Q03 anchor changed (C26), P23 `Supersedes` changed (C18), P23 source row changed (C19), a Q03 row inside a fence (C32), P23 token `== 0` removed (C12, C35).

## 4. Proposal verification (`receipts/verify.json`, `receipts/verify_proposals.py`)

Each input is a real ctl commit on top of the good tree. Columns: unchanged instrument, then survivor mutants. A proposal kills a survivor when that survivor's verdict differs from the unchanged verdict.

| proposal | unchanged | kills (mutant verdict ≠ unchanged) | not killed |
|---|---|---|---|
| V1 prose `Only when …` line, no verbatim sentence | MISSED `stale` | C09 (MET), C37 (MET) | C11, C13, C14, C15, C17, C31 (all MISSED `stale`) |
| V2 P23 row `RELEASED` → `released` | MISSED `p23` | C11 (MET) | others MISSED `p23` |
| V3 P23 row `== 1` → `is 1` | MISSED `p23` | C13 (MET) | others |
| V4 P23 row `m_passPressed` → `passPressed` | MISSED `p23` | C14 (MET) | others |
| V5 P23 row `any other value` → `remaining value` (`else` kept) | MET | C15 (MISSED `p23`) | others MET |
| V6 P23 Pin:anchor `1554-1576` → `1554-1558` | MISSED `p23` | C17 (MET) | others |
| V7 heading `## Correction …` → plain line | MISSED `rows:heading` | C31 (MET) | others MISSED `rows:heading` |

All seven inputs keep the frozen row grammar (three/seven-cell rows, same ids, same quotes), so they are grammar-valid inputs for the unchanged counter; none is a syntactic rejection (QUALITY 105).

## 5. Equivalent mutants (why they are not survivors)

- C10: every block that contains the frozen P19 sentence also contains `only when` in lower case, because the sentence itself does (`… sends a PRESSED keyboard key only when …`). Leg 1 therefore already covers leg 2 for any input leg 2 can match.
- C29: the counter checks `pin_sha256` first; with frozen quotes equal to the frozen pin bytes, the per-line quote equality cannot fail when the sha matches.
- H02: CTL-5's allowed set is `{stale}` and rows are not allowed, so a non-empty `missed=` forces `{stale}`; weakening its must-set changes nothing.
- H04: every control has a non-empty must-set; with `missed=none`, the must check already fails.

## 6. Observations about the pair (not new claims)

- The independent harness, as shipped, kills 14 of 38 counter mutants; the other 14 killed mutants are guarded only by the counter's own selftest. Eight survive both and two are equivalent.
- The harness's final verdict does not pin the number of controls: `ok = good == "ok" and passed == len(CONTROLS)` with a literal `6` in the printed line. H01 and H05 show a 5-control run printing `controls=5/6 verdict=OK`.
- The counter's selftest is blind to the BASE constant (`C21` passes 41/41), because `evaluate` receives `base_commit` in-process. Only the harness (through the real `3b55b6e` object) guards it.
- A repository built only from the exported tree (no `3b55b6e` object) cannot run either tool: `MADO_P19_FIX: SETUP base_commit_absent` and `MADO_R55_CONTROLS: SETUP base_entry_unreadable` (`receipts/R6-exported-tree-only.txt`). The harness therefore needs the base commit object at `--repo`; a receipt that only carries the tree cannot reproduce C3.

## 7. Files

- `mutants/C01…C38*.py`, `mutants/T01/T02*.py`: counter mutants and targeted counters (copies of the lane counter with one edit).
- `mutants/H01…H06*-r55_ctl_c3.py`: harness mutants (copies of the lane harness with one edit).
- `mutants/STUB-always-green.py`: always-green stub used for the harness runs.
- `receipts/`: `drive.py` (mutant generator and runner), `drive.log`, `summary.json`, `verify_proposals.py`, `verify.json`, `receipts.py`, `R1-R9-decisive.txt`, `R6-exported-tree-only.txt`, `unchanged-sha256.txt`, and the unchanged counter and harness copies.
