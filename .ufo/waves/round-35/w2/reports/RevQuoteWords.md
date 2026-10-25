# RevQuoteWords — the eight gate-quote lines: word bound, once-per-id, and the located-copy direction

Seat: reviewer (leaf), round 35 wave 2, read-only. No subagent dispatch. No installs were
needed or made (pacman is host-paused; nothing was installed through any channel).

Artefacts written by this seat, all under
`.ufo/waves/round-35/scratch/RevQuoteWords/`: `mut/` (scored-tree replica), `A8_placeholder_all/`,
`A1_placeholder_one/`, `L_prefix_7w/`, `K_s205_data_3w/`, `B25_body_25w/`, `M_body_30w/`,
`C26_body_26w/`, `D_paraphrase/`, `E_noncontig/`, `H_crossid/`, `I_duplicate_line/`,
`J_shadow/`, `G_fabricated_receipt/`, `gen_mutants.py`, `measure.py`, `measure.out`.
No lane file, counter, control, `SOURCES.md`, jj state or Git index was touched; the eight
`fetch/S20*.receipt.txt` files were only read and their sha256 re-computed.

## Scope verified

| check | command | result |
|---|---|---|
| live C1 | `python3 -I .ufo/waves/round-35/c1/count.py --root . --frozen .ufo/waves/round-35/c1/frozen.json` | `closed_entries=3 closed_rows=8 open_cites=0 verdict=TARGET_MET` **exit 0** |
| replica of the scored tree, unmodified | same command with `--root .ufo/waves/round-35/scratch/RevQuoteWords/mut` | `... TARGET_MET` **exit 0** |
| receipt bytes vs frozen spec | `sha256sum .ufo/waves/round-35/fetch/S20*.receipt.txt` | all 8 hashes equal `c1/frozen.json` `receipts[sid].sha256` |
| entries vs w1 golden control | `diff -q corpus/knowledge/<entry> .ufo/waves/round-35/controls/golden/corpus/knowledge/<entry>` | identical, 3/3, exit 0 |
| registry rows | `awk -F'\|' '/^ *\| S20[3-9] \||^ *\| S210 /{print $2,"nf="NF-2}' corpus/SOURCES.md` | S203–S210 each `nf=11` |

## 1. Word counts — all inside the bound, under both counting conventions

The counter (`c1/count.py:127-135`) returns the whole line remainder after
`gate-quote: {sid} `, which still begins with `located: `. It then counts with
`quote.split()` (line 176). So the counter's "word" count includes the literal token
`located:`. Numbers below give both.

Command for the bare figure (task's `1<=n<=25`):
`grep '^gate-quote:' <entry> | awk '{print $2, NF-3}'`

| id | entry | line | bare words (`awk`) | counter words | `1<=ctr<=25` | full-line `NF` | headroom to 25 |
|---|---|---|---|---|---|---|---|
| S203 | idle-lock-never-asked-r12.md | 12 | 13 | 14 | yes | 16 | 11 |
| S204 | idle-lock-never-asked-r12.md | 13 | 12 | 13 | yes | 15 | 12 |
| S205 | idle-lock-chain-armed-r14.md | 11 | 16 | 17 | yes | 19 | 8 |
| S206 | idle-lock-offered-in-the-bar-r15.md | 15 | 12 | 13 | yes | 15 | 12 |
| S207 | idle-lock-offered-in-the-bar-r15.md | 16 | 14 | 15 | yes | 17 | 10 |
| S208 | idle-lock-offered-in-the-bar-r15.md | 17 | 13 | 14 | yes | 16 | 11 |
| S209 | idle-lock-offered-in-the-bar-r15.md | 18 | 12 | 13 | yes | 15 | 12 |
| S210 | idle-lock-offered-in-the-bar-r15.md | 19 | 14 | 15 | yes | 17 | 10 |

Bare range 12–16, counter range 13–17. Every value satisfies `1 <= n <= 25`. Measured by
`python3 -I .ufo/waves/round-35/scratch/RevQuoteWords/measure.py` (exit 0), stored at
`scratch/RevQuoteWords/measure.out`.

## 2. Exactly once per id per entry — holds for the space form

`grep -c '^gate-quote: S2xx '` per id, per entry (each printed `1`, exit 0):

```
S203 in idle-lock-never-asked-r12.md: 1        S207 in idle-lock-offered-in-the-bar-r15.md: 1
S204 in idle-lock-never-asked-r12.md: 1        S208 in idle-lock-offered-in-the-bar-r15.md: 1
S205 in idle-lock-chain-armed-r14.md: 1        S209 in idle-lock-offered-in-the-bar-r15.md: 1
S206 in idle-lock-offered-in-the-bar-r15.md: 1 S210 in idle-lock-offered-in-the-bar-r15.md: 1
```

File totals `grep -c '^gate-quote:'`: 2 / 1 / 5 = 8, and the id set is exactly the frozen
`entries` map (no stray or missing id). Quote-text occurrences: 1 per entry, 1 per receipt
(`measure.py` columns `once_entry`, `once_receipt`). Each quote also appears in no other
`corpus/` file (`grep -rlF` over `corpus/`).

The once-only property is live, not stylistic: adding a second well-formed line
`gate-quote: S203 located: install/first-run/ lists 12 scripts` to the r12 entry gives
`closed_entries=2 closed_rows=7 open_cites=1 verdict=TARGET_MISSED` **exit 1**
(`I_duplicate_line`). It is *not* live for the no-space form — `J_shadow` appends
`gate-quote:S203 shadow quote for the same id` and still prints `TARGET_MET` **exit 0**,
because `gate_quote()` matches `line.startswith("gate-quote: S203 ")`. This confirms, from
the once-per-id side, the adjacent w1 finding `att-quote-shadow`
(`w1/reports/RevC1Clause.md`); no delivered line uses the shadow form.

## 3. The other direction — not "any": **all eight** are the `located:` line copied whole

For every id, the extracted quote is byte-identical to the receipt's final `located:` line:

```
q.encode() == located_line.encode()   -> True for 8/8
```

and it is the receipt's **tail** — `offset + len(quote) + 1 == receipt_size` for 8/8:

| id | quote byte offset in receipt (counter convention, includes `located:`) | bare-text offset (+9) | quote bytes | receipt bytes | offset/size |
|---|---|---|---|---|---|
| S203 | 3033 | 3042 | 103 | 3137 | 96.7 % |
| S204 | 342 | 351 | 102 | 445 | 76.9 % |
| S205 | 1091 | 1100 | 102 | 1194 | 91.4 % |
| S206 | 817 | 826 | 111 | 929 | 87.9 % |
| S207 | 612 | 621 | 92 | 705 | 86.8 % |
| S208 | 662 | 671 | 105 | 768 | 86.2 % |
| S209 | 808 | 817 | 96 | 905 | 89.3 % |
| S210 | 302 | 311 | 82 | 385 | 78.4 % |

This is the wave-1 writing convention, stated by the seat that produced the receipts:
"the `located:` lines in each receipt are the gate-quote candidates for the entry seats"
(`w1/reports/ScribeRows.md:85-87`). So the 25-word bound is applied to a line that was
authored *in order to be* the gate-quote, i.e. a formality in the strict sense: it
constrains the author's summary style, never the evidence.

Four mutations on the replica make the formality explicit. Every run below is
`python3 -I .ufo/waves/round-35/c1/count.py --root <mutant> --frozen .ufo/waves/round-35/c1/frozen.json`:

| mutant | quote written into the entry | words | verdict | exit |
|---|---|---|---|---|
| `A8_placeholder_all` | `located:` on **all eight** ids | 1 | **TARGET_MET** | 0 |
| `A1_placeholder_one` | `located:` on S203 only | 1 | TARGET_MET | 0 |
| `L_prefix_7w` (dir name kept) | `located: install/first-run/ lists 12 scripts` (a prefix of the located line) | 5 | TARGET_MET | 0 |
| `K_s205_data_3w` (dir name kept) | `1667 /usr/bin/hypridle` (a raw probe row) | 2 | TARGET_MET | 0 |
| `B25_body_25w` | 25-word contiguous run appended to the receipt | 25 | TARGET_MET | 0 |
| `C26_body_26w` | the same run at 26 words | 26 | **TARGET_MISSED** | 1 |
| `M_body_30w` | 30-word contiguous run (reproduces `c1-quote-long`) | 30 | TARGET_MISSED | 1 |
| `D_paraphrase` | a faithful paraphrase, not a substring | 16 | TARGET_MISSED | 1 |
| `E_noncontig` | `custom/idle-indicator omarchy-toggle-idle` (two non-adjacent spots) | 2 | TARGET_MISSED | 1 |
| `H_crossid` | S205's located text planted on S206 | 16 | TARGET_MISSED | 1 |
| `I_duplicate_line` | second well-formed line for S203 | — | TARGET_MISSED | 1 |
| `J_shadow` | `gate-quote:S203 ...` (no space after colon) | — | TARGET_MET | 0 |
| `G_fabricated_receipt` | fabricated 2-line S203 receipt + matching quote | 10 | **TARGET_MET** | 0 |

Reading: the lower bound of 1 is satisfiable by the literal token `located:` — the same
token the counter's own extractor leaves on the front of the quote — so the minimum
passing artefact is a label, not evidence. `K` shows the clause *would* accept measured
bytes; `0/8` delivered quotes do, and `8/8` quote prose that the receipt's author wrote
after the measurement. `C26`/`M30` show the bound is genuinely failable (the r34 dead
clause really is repaired), but only in the direction of *length*: an author fails it by
quoting more than 25 words, never by quoting the wrong thing. Failability and
meaningfulness are different properties here.

## 4. The quote clause is not independent of the receipt — the digest is a dead store

`c1/count.py:174` computes `digest = sha256(blob)` and then never uses it; the closure
test at line 192 compares the **frozen** `receipt["sha256"]` against the **registry
anchor cell** (`cs[5]`), so receipt bytes on disk are bound to nothing.
Mutant `G_fabricated_receipt` replaces `fetch/S203.receipt.txt` in the replica with

```
# S203 receipt — fabricated
located: fabricated claim about the host that was never observed
```

rewrites the entry's quote to match, and still prints `closed_entries=3 closed_rows=8
open_cites=0 verdict=TARGET_MET` **exit 0**. Because the quote is the located line, a
receipt that supplies its own summary supplies its own valid quote: `gate-quote-substring`
can never fire on a fabricated-but-consistent pair. This is the quote-side demonstration
of the clause the w1 seat reported as `digest-match` dead-store
(`w1/reports/RevC1Clause.md`, "Summary" bullet 1); that report only asserted
`gate-quote-substring` falls *jointly* with it. It does — and here is the run.

## Findings by severity

1. **MEDIUM — the gate-quote is a self-quote in 8/8 cases, so `gate-quote-word-bound`
   certifies summary style, not evidence.** The quote is byte-identical to the receipt's
   own `located:` line, sits at its tail (offsets above), and `A8` proves even
   `located:` alone satisfies both quote clauses. No delivered quote carries a byte that
   is not already the receipt's authored claim about the data. The counter cannot see the
   difference; nothing in the lane's predicate does.
2. **MEDIUM — `gate-quote-substring` is not an evidence-integrity check.** `count.py:174`
   computes and discards the receipt digest, so receipt bytes are free; `G` rewrites a
   receipt wholesale and the row still closes (`TARGET_MET`, exit 0). The quote clause and
   the anchor clause are therefore not independent, and the predicate's wording ("the
   sha256 of the named receipt") is satisfied only in the spec-to-registry direction.
3. **LOW — "exactly one gate-quote line" holds only for the space form.** `J`
   (`gate-quote:S203 ...`) is invisible to `gate_quote()`; `TARGET_MET`, exit 0. No
   delivered line is malformed, so the claim as executed is true; the clause name
   overstates what is enforced. (Confirms w1 `att-quote-shadow`.)
4. **INFO — counting convention.** The counter counts `located:` as a word (13–17 here);
   the bare quote is 12–16. Either way the bound holds with 8–12 words of headroom, so no
   delivered line is near either edge and the convention choice cannot flip a verdict.

Nothing actionable was found in the mechanical claims themselves: 8/8 in bound, 8/8 once
per id per entry, 8/8 contiguous, 8/8 id-bound, contiguity and id binding both live
(`E`, `H` fail as they should).

## Residual risk and verification gaps

- **Not verified:** the truth of each quote against the host (each per-id seat owns that);
  C2's calibration counter (out of this seat's scope). Both are explicitly unrun here.
- **Not verified:** whether entries outside the three carry gate-quotes that are *not*
  located-line copies, so the 8/8 figure is scoped to this wave's corpus, not to the lane.
- **Residual risk:** because the located line is authored text, a quote can be a true
  substring, inside the bound, once-per-id, and still assert nothing the receipt does not
  already assert. Any future repair that only tightens the length bound or the substring
  test leaves finding 1 untouched; only a quote drawn from measurement bytes (which `K`
  shows is already permitted) or from the declared host source would change it.
