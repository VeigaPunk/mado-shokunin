# RevTarget — do-nothing reachability test for PRED-C1-r35-v1

Seat: `RevTarget` (round-35 w1). Target under attack:
`closed_entries=3 AND closed_rows=8 AND open_cites=0`
(`PRED-C1-r35-v1`, counter `.ufo/waves/round-35/c1/count.py`, spec `c1/frozen.json`).

## Verdict

**The counter accepts a do-nothing tree — twice over.**

1. `quote-only` — the three real knowledge-entry paths exist but carry **only the
   gate-quote lines and zero prose** — `TARGET_MET`, exit 0. Entry prose is not scored.
2. `fake-all` — receipt files are **fabricated** (sha256 ≠ frozen for all 8, zero real
   fetched bytes) and the gate-quote lines are invented — `TARGET_MET`, exit 0. The
   frozen digest never binds the blob bytes (dead `digest`, count.py:174).

The only thing the target cannot reach is literal nothing: `empty` (zero-byte entries,
real receipts) and the live lane root both print `TARGET_MISSED`. So C1 is not
vacuous at zero work — but it is reachable at **shape-only** work, including a
shape-only tree whose evidentiary payload is entirely fabricated.

## Observed counter output

```
=== quote-only ===
PRED-C1-r35-v1 closed_entries=3 closed_rows=8 open_cites=0 verdict=TARGET_MET
exit=0
=== fake-all ===
PRED-C1-r35-v1 closed_entries=3 closed_rows=8 open_cites=0 verdict=TARGET_MET
exit=0
=== empty ===
PRED-C1-r35-v1 closed_entries=0 closed_rows=0 open_cites=8 verdict=TARGET_MISSED
exit=1
=== live lane root (do-nothing baseline) ===
PRED-C1-r35-v1 closed_entries=0 closed_rows=0 open_cites=8 verdict=TARGET_MISSED
exit=1
```

Command (verbatim, per tree):

```
python3 -I .ufo/waves/round-35/c1/count.py --root <tree> --frozen .ufo/waves/round-35/c1/frozen.json
```

Trees live under `.ufo/waves/round-35/scratch/RevTarget/{quote-only,fake-all,empty}/`.
Each carries a copy of the golden `corpus/SOURCES.md` (all 8 rows, valid cells) so the
row-side clauses are satisfied identically across trees.

| tree | entries | receipts | expected / observed |
|---|---|---|---|
| `quote-only` | `gate-quote:` lines only, no prose (grep-extracted from golden) | real bytes (digests = frozen) | MET / MET |
| `fake-all` | invented `gate-quote:` lines | fabricated bytes; `comm -12` fake∩frozen digests = 0 | MET / MET |
| `empty` | zero-byte files | real bytes | MISSED / MISSED |
| `.` (lane root) | real corpus (no S203–S210 entries yet) | real fetches | MISSED / MISSED |

## How the counter actually decides (count.py, read 2026-10-24)

Per sid, `ok` (lines 185–196) needs:

- blob readable via `read_regular` at the frozen receipt path (lines 173, 186);
- exactly one registry row (`rows_for`, line 177), 11 cells (line 180);
- `used_by` token set == the admitted citing entries (line 189);
- `cs[7] == "mined"` (line 190); `valid_recheck(cs[9])` (line 191);
- **`receipt["sha256"] in cs[5]`** — the *frozen digest string* occurs inside the row's
  anchor cell (line 192);
- exactly one `gate-quote: <sid> ` line, 1–25 words, `quote.encode() in blob`
  (lines 193–195).

`closed_entries` counts entries whose file is a readable regular path **and** all of
whose rows closed (lines 170, 197–203). Nothing else about the entry is examined —
no headings, no prose, no minimum length. One line per sid is the whole requirement.

## Findings

1. **Entry prose is a free variable.** `gate_quote` (lines 127–135) scans only lines
   starting `gate-quote: <sid> `; every other byte of the entry is ignored. `quote-only`
   is the provable minimum: strip an entry to its 1–5 gate lines, keep nothing else,
   still `closed_entries=3`. The r35 predicate text ("the entry carries exactly one
   gate-quote line…") literally licenses this — but the round's *intent* (knowledge
   entries carrying the mined finding) is not what the counter measures.

2. **The frozen digest binds the row's text, not the receipt's bytes.** Line 174:
   `digest = hashlib.sha256(blob).hexdigest()` — `digest` is **never read again**
   (checked through line 203; it appears in no subsequent expression). The only
   digest check is `receipt["sha256"] in cs[5]`: substring membership of the frozen
   value in the row's anchor cell. `fake-all` proves the consequence: all 8 blobs
   are fabricated, all 8 rows still close, `TARGET_MET`. A row that *says* the right
   digest beats a receipt that *is* the right digest.

3. **No control covers the gap.** `controls/c1-digest` differs from `golden` only in
   `SOURCES.md` line 10 — the S210 row's digest *string* replaced by 64 zeros; the
   S210 receipt file is untouched. `c1/clauses.json` `live` has ten clauses; none
   names blob-digest-vs-frozen, so the hole is not covered by any load-bearing
   clause. Suggested: wire `digest == receipt["sha256"]` into `ok` (the r33 counter's
   `blob's sha256 equals the digest frozen` behavior) and add a blob-mismatch
   control — the r33 suite's `hash-mismatch` control tested exactly this and was
   dropped in r34/r35's row-text pivot.

4. **Bounds that DO hold** (checked while building): empty entries → `open_cites=8`
   (a cite needs its gate-quote line); absent/mismatched row shape is covered by
   `row-unique`, `row-well-formed`, `used-by-exact`, `status-mined`, `recheck-valid`;
   symlink/hardlink entry paths die in `read_regular` (`S_ISLNK` walk + `st_nlink != 1`,
   lines 80–87). The row-grammar side of the predicate is enforced; the
   entry-content and blob-integrity sides are not.

## Write-scope note

All writes under `.ufo/waves/round-35/scratch/RevTarget/` (probe trees) and this
report; `c1/`, `controls/`, `corpus/`, `LOG.md`, `SCORECARD.md` untouched.
