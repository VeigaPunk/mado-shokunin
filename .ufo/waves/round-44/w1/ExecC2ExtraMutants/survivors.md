# C2 mutation population — survivors (ExecC2ExtraMutants, round 44 w1)

Instrument: frozen `quality/counters/c2-r44-gkeep-size-request.py` at the lane (sha256 `5b72c16d5f1bdef43a5374c4b3a0de0acef9bd0d4ed427776dd205ee47860a68`, read-only; never edited). Positive fixture:
`w1/ExecC2ExtraMutants/positive.patch` applied to the lane at `e2289516a9a857f55cda7be635933e89b931c3da` (fixture commit
`99ad0ddb9d7c4bee400f193ecb8cb22d9f51d377`), scored

    python3 -I quality/counters/c2-r44-gkeep-size-request.py --repo <fixture> --rev HEAD --base 6a1a90528fe533cadee506a9fa3e9d13d15cc41f
    -> PRED-C2-r44 hyprland-gkeep-size-request-r44.md clauses=a:1 b:1 c:1 d:1 e:1 f:1 g:1 h:1 i:1 admitted=1
    -> PRED-C2-r44: admitted=1/1 verdict=TARGET_MET rev=99ad0ddb9d7c4bee400f193ecb8cb22d9f51d377   (rc=0)

(`positive-score.txt`). Rebuilt from `positive.patch` alone in a second clone at the same lane revision it scores the same
(`admitted=1/1 verdict=TARGET_MET rev=f73972e357e08ffaa301995acadd9d4e21e31a2b`), so the fixture is the patch, not the seat's scripts.
51 single-defect mutants, each one edit cluster on that commit, each committed and scored (`scores.tsv`, one patch per
mutant in `mutants/`). **48 score 0/1. 3 score 1/1.**

## Survivors

| # | mutant | defect | score | clause that should have killed it | status |
|---|---|---|---|---|---|
| 51 | `51-census-prefix-hides-claim` | a body line `hyprland sendWindowSize S299 is the document that licenses this whole section` names a cited id with no quote and no locator | `admitted=1/1` | g — its exemption is a **prefix** test, not the exact census lines | **predicate defect** (measured fix below) |
| 50 | `50-row-kind-ownwork` | S300's registry `kind` cell changed `code` -> `own-work` for an upstream file | `admitted=1/1` | c (or h) — neither tests the `kind` cell | **predicate gap** (no clause covers the cell) |
| 49 | `49-misread-quote` | the S300 claim line keeps the true quote at the true locator but the prose around it asserts the opposite of what the quote says | `admitted=1/1` | none can: quote-to-claim binding is reading, not matching | **declared residual** (registration §Residuals; not a hole) |

### 51 — the clause-g exemption is a prefix, not the census line

The census lines are already excluded by exact equality (`l not in census_lines`, counter:561); the two `startswith` tests at counter:562-563 add
nothing for the intended lines and exempt **any** line that begins with `gkeep client ` or `hyprland sendWindowSize `. Mutant 51 hides a claim
naming S299 behind that prefix, so `all_body_lines_bound` (counter:354-367) never sees the line, clause g stays 1, and the entry is admitted.

Measured fix (seat copy `fix-counter.py`, **not** applied to the lane): drop the two `startswith` clauses, keep `l not in census_lines`.

    frozen counter, mutant 51 : admitted=1/1  verdict=TARGET_MET   rev=9c3547bd0d8235248e5299e3cc3a8289d79539f6
    fixed  counter, mutant 51 : admitted=0/1  verdict=TARGET_MISSED rev=9c3547bd0d8235248e5299e3cc3a8289d79539f6  (g:0)
    fixed  counter, positive  : admitted=1/1  verdict=TARGET_MET    rev=99ad0ddb9d7c4bee400f193ecb8cb22d9f51d377  (a..i all 1)

So the narrowing is free on the positive fixture and closes the hole. The clause-g burden ("neither line is a clause-g claim line",
counter:24-25) is what the exemption was for; exact equality already discharges it.

### 50 — no clause tests the registry `kind` cell

Clause c (counter:453-472) tests the status cell, the opened cell (new ids only), the used-by cell, the recheck cell, the 11-cell shape and the
location token of the source cell; clause e tests the location; clause i scans every cell for `BAD_LOC` only. The round-43 clause h test "exactly three new cited rows have kind own-work"
survives in the inherited text (counter:107) but the round-44 rebuilt h (counter:15-25) is a census over `gates`/`receipts_raw` and never looks
at a row's kind — `host_census(new_ids, …)` (counter:382) does not use its `new_ids` argument at all. A row can therefore call an upstream file
`own-work` and be admitted. This is docstring-consistent (the r44 clause c and h genuinely do not test the cell), so it is a coverage gap to
register, not a counter bug; the fix is one line in clause c (`cells[2] == "code"` for a row whose receipt basename is upstream) or restoring a
kind test inside h.

### 49 — the quote-to-claim binding (expected)

`49-misread-quote` leaves `**OBS** S300 … \`if (saved_size && !fixed_size && was_fixed_size)\` (gdktoplevel-wayland.c:656)` intact and edits only
the surrounding sentence. Every syntactic clause holds because every syntactic fact holds; the registration declares exactly this residual
("a real quote at a true locator can be cited for a claim it does not support"). It is listed here because the counter admits it, not because a
clause should have fired.

## Killed mutants, by the clause set that fires

48 mutants, none admitted. Every clause fires alone at least once: b 5, c 10, d 1, e 1, f 2, g 5, h 5, i 7. The coupling is one-way: when the
quote itself is unusable (in a comment, twice, too long, word-cut, wrong sha, receipt outside `fetch/`, Gate line missing/indented/duplicated/
moved) clause d fails, g fails with it (the id's claim line cannot carry a usable quote+locator) and i usually fails (the id drops out of
`receipts`, so the PINS coverage test no longer sees that receipt). 48 is the exception that proves the rule: its quote is valid in its own
receipt and only duplicated in another cited receipt, so d fires alone.

| clauses at 0 | count | mutants |
|---|---|---|
| b | 5 | 01-05 (verified-at pushed out of the 20-line header, sixth `source:` outside it, ghost `S999`, wrong date, `recheck: whenever`) |
| c | 10 | 06-09, 11-13, 40, 45, 47 (status, used-by, opened, 10 cells, S164 anchor/status/used-by, duplicate row, row deleted, renamed used-by path) |
| d | 1 | 48 (S164 quote also occurs in the S298 receipt) |
| e | 1 | 41 (S299 location set to S300's) |
| f | 2 | 25, 26 (README row missing / doubled) |
| g | 5 | 19, 20, 38, 39, 42 (locator off by one, locator start line late, second id on the claim line, claim line fenced, claim line deleted) |
| h | 5 | 21-24, 46 (x11 count, client size, census fenced, census duplicated, client census deleted) |
| i | 7 | 10, 27-31, 44 (BAD_LOC in a row, r11 admitted, wrong ADMIT target, no flip word, short reason, REFUSE = ADMIT, REFUSE deleted) |
| d+e+g+i | 3 | 32, 34, 36 (Gate line indented, duplicated, deleted) |
| d+g+h+i | 4 | 15-17, 35 (quote in a `//` comment, quote twice, 29-word quote, receipt from the round-43 dir) |
| d+g+i | 2 | 14, 18 (sha digit changed, quote starting inside a word) |
| d+e+g+h+i | 1 | 33 (Gate line moved out of `## Gate`) |
| b+c+i | 1 | 43 (three source lines only) |
| b+h+i | 1 | 37 (S301 left out of the header) |

The single-defect discipline held: each mutant carries one defect statement and its patch is the whole diff (`mutants/<name>.patch`).
