# ReviewC1Predicate — junk-tree attack on PRED-C1-r33-v1 (2026-10-24)

Seat: w1 leaf. Target: `.ufo/waves/round-33/c1/count.py` + `c1/frozen.json`.
Question: is there a junk tree that prints `TARGET_MET` while the frozen quotes
are **not** substrings of the frozen-hash blobs?

## Verdict

**The predicate survives.** No such tree is constructible without a sha256
collision.

## Why (code-binding argument)

1. **Single read, one bytes object.** `count.py` `main()` reads the blob once
   (`blob = blob_path.read_bytes()`); both `quote.encode() in blob` and
   `hashlib.sha256(blob).hexdigest() == fetch["sha256"]` consume that same
   in-memory object. There is no second read, no separate hash-path/content-path
   pair, no TOCTOU surface to desynchronize them.
2. **Second-preimage resistance.** Any file whose sha256 equals the frozen
   digest is, practically, byte-identical to the frozen blob. So a tree that
   passes necessarily contains `quote ⊆ blob-with-frozen-hash`. Printing
   `TARGET_MET` with quotes absent from frozen-hash blobs would require a sha256
   collision — out of reach.
3. **Escape hatches closed.**
   - Empty/missing blob → `blob = b""` → `digest = ""` ≠ any frozen digest.
   - Frozen quotes are all non-empty, so the `"" in blob` vacuous-truth path is
     unavailable.
   - `found == quote` ties the entry's `gate-quote:` line to the same frozen
     string used for containment; no independent quote source exists.

## Empirical proof (throwaway trees in /tmp, counter untouched)

Construction (both trees): entry files with exact `gate-quote: <sid> <quote>`
lines; `corpus/SOURCES.md` rows whose used-by cell contains the entry path;
blobs at the frozen relative paths.

- **Attack tree** `/tmp/revc1-attack` — blob bytes = real fetch bytes with the
  quote replaced by `[QUOTE-REMOVED]` (containment fails AND digest differs):

  ```
  $ python3 .ufo/waves/round-33/c1/count.py --root /tmp/revc1-attack --frozen .ufo/waves/round-33/c1/frozen.json
  PRED-C1-r33-v1 closed_entries=0 closed_rows=0 open_cites=4 verdict=TARGET_MISSED   (exit 1)
  ```

- **Control tree** `/tmp/revc1-control` — identical construction, blob bytes =
  real frozen fetch bytes:

  ```
  $ python3 .ufo/waves/round-33/c1/count.py --root /tmp/revc1-control --frozen .ufo/waves/round-33/c1/frozen.json
  PRED-C1-r33-v1 closed_entries=2 closed_rows=4 open_cites=0 verdict=TARGET_MET   (exit 0)
  ```

  The control passing proves the junk construction is otherwise complete; the
  quote↔digest binding is the sole blocker.

- **Real frozen blobs verified** (`.ufo/waves/round-33/fetch/S190.bin`,
  `S191.bin`, `S197.bin`, `.ufo/waves/round-32/fetch/S189.bin`):
  4/4 `hash_match=True`, 4/4 `quote_in_blob=True` — the coupling is meaningful
  on the real tree, not vacuous.

## Residual weaknesses observed (do not enable the asked decoupling)

- `used_by()` returns the whole last `|`-cell and the check is
  `entry_rel in used_by(row)` — a substring, not an exact-cell match. A row
  ending in `` | junkcorpus/knowledge/waybar-module-text-route-r25.md | `` would
  count. Registry identity is soft.
- `row_for()` accepts both `| SID |` and `|SID|` spacing; `gate_quote()` matches
  any line starting with `gate-quote: <sid> ` — first match wins.

## Live-state note (context only)

Real root currently prints `TARGET_MISSED closed_entries=0 closed_rows=0
open_cites=4`: both frozen entry files
(`corpus/knowledge/waybar-module-text-route-r25.md`,
`corpus/knowledge/event-delivery-limits-r26.md`) are absent from
`corpus/knowledge/`, and `corpus/SOURCES.md` has a row for S189 (`:201`) only —
round 33 is in flight. Not addressed here; this seat's brief was the predicate.

## Evidence index

- Counter read in full: `.ufo/waves/round-33/c1/count.py` (all functions),
  `.ufo/waves/round-33/c1/frozen.json`.
- Reproduce: `python3 .ufo/waves/round-33/c1/count.py --root /tmp/revc1-attack
  --frozen .ufo/waves/round-33/c1/frozen.json` (and `/tmp/revc1-control`).
- Scratch trees are disposable under `/tmp`; repo untouched, counter unedited.
