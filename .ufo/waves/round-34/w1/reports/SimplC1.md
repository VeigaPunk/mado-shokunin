# SimplC1 — round-34 C1 coverage counter simplification review

Scope: `.ufo/waves/round-34/c1/count.py`, `c1/frozen.json`, `registration.md`
(found at `.ufo/waves/round-34/registration.md`; the brief's `c1/registration.md`
does not exist — the file lives at the round root).
Full analysis: `.ufo/waves/round-34/scratch/SimplC1/simplify.md`.

## Honest sentence

The counter accepts an admit as closed only when every path of the entry, its
fetch blobs, and `corpus/SOURCES.md` is a regular file reached through real
directories inside the scored root (no symlink, nlink=1), each fetch's bytes
hash to the frozen sha256, the entry holds a `gate-quote:` line of 1–25 words
per cited id that is a contiguous substring of those bytes, and the id's one
registry row lists the entry as a used-by token; TARGET_MET requires exactly
1 closed entry, 2 closed rows, 0 open cites.

## Verdict: not a faithful implementation

Three clauses stronger (all confirmed false negatives), one clause weaker
(fence-blind row counting). Verdict line on the live lane tree is
`closed_entries=1 closed_rows=2 open_cites=0 verdict=TARGET_MET` (exit 0), so
the counter works on the current admit — the risk is forward: the same counter
would miss a genuine admit under ordinary corpus formatting.

## FALSE NEGATIVES — verified by mutant runs on `controls/golden/`

| Mutation (still closed under the sentence) | Result |
|---|---|
| used-by cell `…-r25.md, corpus/lessons/round-34.md` (multi-token; corpus precedent at `SOURCES.md` S017) | `open_cites=2 TARGET_MISSED` |
| trailing space after gate-quote tail | `open_cites=1 TARGET_MISSED` |
| `- gate-quote:` bulleted line | `open_cites=1 TARGET_MISSED` |

Highest risk: the used-by **set equality** (`count.py:157`). The sentence asks
for membership; the code demands the entry be the *only* token. The corpus
contract already allows comma lists, so the first shared cite breaks the count.

Latent (not exercised): `MAX_BYTES` 8 MB silent cap, duplicate gate-quote lines
rejected, `ROW_RE` needs cell-1 id + indent ≤3, UTF-8 BOM breaks `startswith`,
symlinked parent dirs rejected even when resolved inside root.

## FALSE POSITIVE direction (none-weaker violated)

A `| S201 | …` row inside a fenced code block counts as the registry row:
golden SOURCES.md wrapped in ```` ``` ```` still printed `TARGET_MET`.

## Recommendation-shaped simplification

The counter's own `ok` conjunction is already one line per predicate clause;
the gap is format rigidity, not verbosity. Honest sentence ↔ code diff =
replace `used_by_tokens(rows[0]) == {entry_rel}` with `entry_rel in
used_by_tokens(rows[0])`, strip quote tails / allow list-item prefixes on
gate-quote lines, and skip fenced regions in `rows_for`. None required for the
current admit; all required before the counter is reused on corpus-shaped
entries.
