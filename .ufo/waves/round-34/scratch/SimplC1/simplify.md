# SimplC1 — PRED-C1-r34-v1 sentence check

## The sentence

The counter accepts an admit as closed only when every path of the entry, its
fetch blobs, and `corpus/SOURCES.md` is a regular file reached through real
directories inside the scored root (no symlink, nlink=1), each fetch's bytes
hash to the frozen sha256, the entry holds a `gate-quote:` line of 1–25 words
per cited id that is a contiguous substring of those bytes, and the id's one
registry row lists the entry as a used-by token; TARGET_MET requires exactly
1 closed entry, 2 closed rows, 0 open cites.

## Verdict

The code implements this sentence with **three clauses stronger and one
clause weaker** — it is not an exact match. The stronger clauses produce real
false negatives (verified below); the weaker one admits fenced code as a
registry row.

## Stronger clauses → confirmed FALSE NEGATIVES

Each was tested by mutating `.ufo/waves/round-34/controls/golden/` (a known
TARGET_MET tree) and re-running:

```sh
python3 -I .ufo/waves/round-34/c1/count.py --root <mutant> --frozen .ufo/waves/round-34/c1/frozen.json
```

1. **`used_by_tokens(rows[0]) == {entry_rel}` (line 157) — set equality, not
   membership.** The sentence says the row "lists the entry path as a whole
   used-by token". The real registry already lists multiple comma-separated
   entries in one cell (`corpus/SOURCES.md:29`, S017). Mutating golden's used-by
   cell to `…-r25.md, corpus/lessons/round-34.md` — still a whole token —
   printed `closed_rows=0 open_cites=2 TARGET_MISSED`. **This is the highest-risk
   clause**: the corpus convention permits multi-token used-by cells, so the
   counter will miss a genuine admit the moment a second entry cites S201/S202.

2. **`line.startswith("gate-quote: {sid} ")` (line 112) — column 0, exactly one
   space.** The sentence says "contains a 1-25 word gate-quote line". A bulleted
   `- gate-quote: S201 …` in golden printed `closed_rows=1 open_cites=1
   TARGET_MISSED`. Markdown-idiomatic quote placement is rejected.

3. **`found == quote` (line 152) — verbatim tail.** Trailing whitespace after
   the quote (`…/tmp/hypr `) printed `closed_rows=1 open_cites=1 TARGET_MISSED`.
   Editors strip or add trailing spaces routinely; the quote remains a
   contiguous substring of the bytes, so the sentence still says closed.

## Stronger clauses → latent false negatives (not exercised above)

- **`MAX_BYTES = 8_000_000` (lines 31, 80):** silent byte cap not in the
  sentence. A genuine fetch > 8 MB returns `None` → open cite.
- **Duplicate gate-quote lines** (`gate_quote` returns `None` if two lines
  match, lines 110-114): the sentence requires "a line"; two identical lines
  still contain a line. Rejected.
- **`ROW_RE` requires the id in cell 1, indent ≤ 3** (line 32): a valid table
  row indented 4+ spaces, or with a leading index column, is invisible.
- **UTF-8 BOM:** `decode("utf-8","replace")` keeps `\ufeff`, so a BOM'd entry's
  first-line gate-quote misses the `startswith` needle.
- **Symlinked parent dirs:** `read_regular` rejects any symlink component even
  when the resolved path stays inside the root; the sentence's "every path
  component stays inside" reading of a within-root symlink tree is rejected.
  (Deliberately hardened — the `symlink-parent` control exists — but stronger
  than the sentence.)

## Weaker clause → false-positive direction (violates "none weaker")

- **`rows_for` is fence-blind.** A `| S201 | … |` line inside a fenced code
  block counts as "the registry row". Wrapping golden's whole SOURCES table in
  ```` ``` ```` still printed `TARGET_MET`. The sentence's "the registry row"
  implies a live table row; commentary or quoted examples are counted.
  (Second-order: `used_by_tokens` takes the *last* cell whatever its header,
  and a `| S201 | … |` row inside the entry file itself would count — but
  `rows_for` only scans SOURCES.md, so entry-file noise is safe.)

## Clauses that match the sentence

- Root containment (`..`, `.`, empty, absolute, leading `\` rejected) — exact.
- `S_ISREG` + `st_nlink != 1` + `O_NOFOLLOW` — exact.
- sha256 against `frozen.json` — exact.
- `1 <= len(words) <= 25` on `split()` — exact for the sentence's word count.
- `quote.encode() in blob` — exact substring check.
- `len(rows) == 1` — the sentence's "the registry row" (singular) supports it.
- Aggregate `closed_entries==1 ∧ closed_rows==2 ∧ open_cites==0` — exact.

## Other

- `KeyError` on a frozen.json missing `entries`/`fetches`/`quotes` → traceback,
  exit 1 (not exit 2). Robustness nit; frozen input is fixed, so no scoring
  impact.
- `nlink=1` is enforced on the leaf only; directory hardlinks are irrelevant on
  Linux. Consistent with the sentence.
