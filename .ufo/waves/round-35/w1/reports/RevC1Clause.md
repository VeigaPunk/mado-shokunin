# RevC1Clause — clause-by-clause attack on PRED-C1-r35-v1

Seat: RevC1Clause (leaf). Date: 2026-10-24. Frozen counter:
`.ufo/waves/round-35/c1/count.py` (not modified); frozen spec:
`.ufo/waves/round-35/c1/frozen.json`. Every tree lives under
`.ufo/waves/round-35/scratch/RevC1Clause/trees/`; each run's counter
line is committed at `scratch/RevC1Clause/receipts/<tree>.txt`; the
builder is `scratch/RevC1Clause/build_trees.py` (23 trees, deterministic).

Sanity: `golden-lite` — a minimal honest tree (no `## Registry`
heading, 11-cell rows, `mined`, `on-change`, frozen digests,
`located:`-line quotes) — prints

```
PRED-C1-r35-v1 closed_entries=3 closed_rows=8 open_cites=0 verdict=TARGET_MET   (exit=0)
```

so the harness is live and my constructions isolate single clauses.

## Verdicts

| clause | result | evidence |
|---|---|---|
| entry-regular | not broken | att-entry-{symlink,dir-symlink,hardlink,fifo} all TARGET_MISSED |
| row-unique | **broken** | att-row-bom-dup, att-row-quote-dup, att-row-indent-dup: TARGET_MET with two row-shaped carriers; break-row-unique-section: TARGET_MET with zero registry-section rows (arguable) |
| row-well-formed | not broken | att-row-{pipe,escpipe}: TARGET_MISSED |
| used-by-exact | not broken | att-usedby-extra: TARGET_MISSED; att-usedby-dup: TARGET_MET but clause's own "token set" wording is satisfied (documented) |
| status-mined | not broken | att-status-case: TARGET_MISSED |
| recheck-valid | **broken** | break-recheck-iso: recheck=`2026-02-30` → TARGET_MET; census validate → `E09 S203 recheck=2026-02-30` |
| digest-match | **broken** | break-digest-append, break-digest-fabricate: TARGET_MET while anchor sha ≠ sha256 of the file at the receipt path; `digest` in count.py:174 is a dead store |
| gate-quote-substring | **broken** (jointly with digest-match) | break-digest-fabricate: quote is substring of fabricated bytes, not of the authentic receipt |
| gate-quote-word-bound | not broken | att-quote-26 (26-word contiguous receipt substring), att-quote-empty: TARGET_MISSED |

## Break 1 — `digest-match` (clause 7), first violation found

`count.py` computes `digest = hashlib.sha256(blob).hexdigest()` (line 174)
and never compares it to anything; `ok` uses the *spec constant*
`receipt["sha256"] in cs[5]`. The blob's own hash is a dead store, so the
anchor cell binds the row to the frozen spec but nothing binds the file
at the receipt path to that spec.

Tree `break-digest-append` is `golden-lite` plus one appended byte-string
(`\n# tampered byte\n`) in `S203.receipt.txt`. Counter output
(`receipts/break-digest-append.txt`):

```
PRED-C1-r35-v1 closed_entries=3 closed_rows=8 open_cites=0 verdict=TARGET_MET   (exit=0)
```

Evidence the clause is violated — the anchor cell carries a sha256 that
is not the sha256 of the receipt file present at the named path:

```
$ sha256sum trees/break-digest-append/.ufo/waves/round-35/fetch/S203.receipt.txt
c237f8108bd4ae804a97a2dc02f99d161a69447ba1b942749bc178a7e332d82f   (actual file)
spec sha256 (frozen.json) and anchor cell: 1b7fa87ffe933990ee59acf3629ffbe3a90106bc9ebcce082237f7f495dd1646
```

Under the reading "sha256 of the named receipt = sha256 of the file the
predicate names", the clause is violated while TARGET_MET stands. Under
the narrowest possible reading "spec-recorded sha256", clause 7 is
satisfied but then the file is not the named receipt at all, so the
S203 quote is not a substring of the named receipt's bytes and clause 8
is violated instead. The code mixes the two readings — anchor binds the
spec, quote binds the file — and the clause text does not admit a
reading that makes both pass on this tree.

Tree `break-digest-fabricate` removes the ambiguity: every receipt is
replaced wholesale by fabricated bytes containing only a header and the
planted `located:` line. Counter output
(`receipts/break-digest-fabricate.txt`):

```
PRED-C1-r35-v1 closed_entries=3 closed_rows=8 open_cites=0 verdict=TARGET_MET   (exit=0)
```

Here the quote is a substring of the file bytes but not of the authentic
receipt — the authentic S203 bytes (sha256 1b7fa87f…) exist nowhere in
the tree — while anchors still carry the spec digests.
`break-digest-fabricate/.ufo/waves/round-35/fetch/S203.receipt.txt`
in full:

```
# fabricated receipt body for S203
located: install/first-run/ lists 12 scripts; the omarchy-first-run body runs all 12; none is idle-lock
```

## Break 2 — `recheck-valid` (clause 6)

Counter: `ISO_DATE = ^\d{4}-\d{2}-\d{2}$` — shape only. The census rule
the counter claims to mirror (`scripts/sources-census.sh:663-667`,
function `epoch()` at 583-590) round-trips the date through `mktime`/
`strftime`, so `2026-02-30` is `E09`-invalid there.

Tree `break-recheck-iso` is `golden-lite` with the S203 row's recheck
cell set to `2026-02-30`. Counter output (`receipts/break-recheck-iso.txt`):

```
PRED-C1-r35-v1 closed_entries=3 closed_rows=8 open_cites=0 verdict=TARGET_MET   (exit=0)
```

Census on the same SOURCES.md (fixture `/tmp/census-r35/recheck2`, rows
placed under `## Registry` so validation reaches E09):

```
a	E09	S203 recheck=2026-02-30
```

`2026-02-30` is not an ISO date on any calendar, so "the recheck cell is
an ISO date, an NNd cadence or a symbolic cadence" is false while
TARGET_MET stands. Siblings that also pass the counter and fail the
census: `2026-13-45` (month 13), `0000-01-01` (census rejects `y==0`).
The `symbolic()` regexes are identical on both sides, so the only seam
is the calendar check.

## Break 3 — `row-unique` (clause 2)

`rows_for()` counts lines matching `^ {0,3}\|\s*(S[0-9]+)\s*\|`.
Anything before the `|` — even a zero-width character — takes the row
out of the count while leaving it row-shaped to a reader.

Tree `att-row-bom-dup` is `golden-lite` plus a second `| S203 | …` row
prefixed with U+FEFF. Counter output (`receipts/att-row-bom-dup.txt`):

```
PRED-C1-r35-v1 closed_entries=3 closed_rows=8 open_cites=0 verdict=TARGET_MET   (exit=0)
```

The file holds two row-shaped lines carrying the id:

```
$ grep -nF '| S203 |' trees/att-row-bom-dup/corpus/SOURCES.md
3:| S203 | src-S203 | own-work | A | scope | receipt .ufo/wa…
11:﻿| S203 | src-S203 | own-work | A | scope | receipt .ufo/wa…   (line 11 starts with ef bb bf)
```

`att-row-quote-dup` (`> | S203 | …` blockquote duplicate) and
`att-row-indent-dup` (4-space-indented duplicate) also print TARGET_MET;
both are weaker — whether quoted/code lines are "registry rows" is
debatable — while the BOM line is byte-identical to a real row after the
first three bytes.

Also run, and reported as arguable rather than clean: tree
`break-row-unique-section` puts a real `## Registry` section holding a
dummy S999 row and places all eight cited rows under `## Notes`; counter
output (`receipts/break-row-unique-section.txt`):

```
PRED-C1-r35-v1 closed_entries=3 closed_rows=8 open_cites=0 verdict=TARGET_MET   (exit=0)
```

and `sources-census.sh validate` flags all eight `E12 row outside
Registry section`. Under the fleet contract (real `corpus/SOURCES.md`
uses `## Registry`, `## Paths`, `## Search log`, `## Leads`) the
registry holds zero rows for each cited id. Under the counter's own
model — the whole file is the registry, as its committed golden control
also lacks the heading — the clause reads on lines and is not violated
by this tree; the BOM variant is the clean break.

## Clauses not broken

**entry-regular** — every non-regular/linked form is killed by the
`lstat` component walk or the nlink/regular checks:

```
att-entry-symlink     closed_entries=2 closed_rows=6 open_cites=2 verdict=TARGET_MISSED  (exit=1)
att-entry-dir-symlink closed_entries=0 closed_rows=0 open_cites=8 verdict=TARGET_MISSED  (exit=1)
att-entry-hardlink    closed_entries=2 closed_rows=3 open_cites=5 verdict=TARGET_MISSED  (exit=1)
att-entry-fifo        closed_entries=2 closed_rows=6 open_cites=2 verdict=TARGET_MISSED  (exit=1)
```

`..`/absolute paths and a symlinked root are rejected textually before
the walk; remaining surfaces are TOCTOU-only, which the frozen split
already declares non-load-bearing (`o-nofollow-open`).

**row-well-formed** — `cells()` is a naive `|` split; literal and
escaped pipes both add fields, and the count matches the census's
`NF-2` on every row shape tried:

```
att-row-pipe     (cell 'teaches with a literal | pipe')  → open_cites=1 TARGET_MISSED  (exit=1)
att-row-escpipe  (cell 'teaches with an escaped \| pipe')→ open_cites=1 TARGET_MISSED  (exit=1)
```

**used-by-exact** — exact string-set equality on both sides; an extra
citing token fails, a duplicated token collapses in the set (the
clause's own wording is "token set", so `att-usedby-dup`'s TARGET_MET is
compliant, not a break):

```
att-usedby-extra  (cited entry + extra path)      → open_cites=1 TARGET_MISSED  (exit=1)
att-usedby-dup    (same path listed twice)        → TARGET_MET, no violation     (exit=0)
```

**status-mined** — `cs[7] == "mined"` after strip; census uses the same
closed enum `queued|mined|rejected`. `Mined` fails:

```
att-status-case  (status cell 'Mined')  → open_cites=1 TARGET_MISSED  (exit=1)
```

**gate-quote-substring** — unbreakable in isolation: `quote.encode() in
blob` against authentic receipt bytes fails as designed

```
att-quote-absent  (26 words not in receipt)  → open_cites=1 TARGET_MISSED  (exit=1)
```

It only falls together with `digest-match` via receipt fabrication
(break 1), since no clause pins the receipt bytes to the frozen sha256.
Adjacent finding, filed for the record because no clause names it: the
predicate's "exactly one gate-quote line" condition is format-strict —
a second assertion `gate-quote:S203 shadow quote for the same id`
(no space after the colon) is invisible to `startswith` and
`att-quote-shadow` prints TARGET_MET (exit=0). Whether a malformed line
is "a gate-quote line for the id" is debatable; reported as arguable.

**gate-quote-word-bound** — `split()` counting agrees with every word
shape available inside an authentic receipt substring:

```
att-quote-26     (26-word contiguous receipt substring)  → open_cites=1 TARGET_MISSED  (exit=1)
att-quote-empty  ('gate-quote: S203 ' bare)              → open_cites=1 TARGET_MISSED  (exit=1)
```

Unicode-separator tricks (ZWSP-glued words) cannot be smuggled through
an authentic receipt without fabricating it, which shifts the violation
to clause 7/8 as above.

## Summary

- Broken: **digest-match** (dead-store `digest`; anchor binds the spec,
  never the bytes), **gate-quote-substring** (only reachable together
  with digest-match via fabricated receipts), **recheck-valid**
  (calendar-invalid `2026-02-30`), **row-unique** (BOM-prefixed
  duplicate invisible to the anchored `ROW_RE`).
- Not broken: entry-regular, row-well-formed, used-by-exact,
  status-mined, gate-quote-word-bound.
- Arguable, recorded: section-scoped registry reading of row-unique
  (`break-row-unique-section`, E12 evidence) and the unnamed
  "exactly one gate-quote line" check (`att-quote-shadow`).
- Common root cause: the counter binds three different subjects —
  spec constants (anchor), file bytes (quote), line shapes (rows) —
  and the clause text does not name a reading under which all three
  are enforced.
