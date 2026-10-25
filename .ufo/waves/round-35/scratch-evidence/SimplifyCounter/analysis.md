# SimplifyCounter — minimal form of PRED-C1-r35-v1

Target: `.ufo/waves/round-35/c1/count.py` (218 lines, commit
`19e4ab3171c1540c40d6b12097745af98053b07d`). Proposal: `count-min.py` in this
directory — 104 lines, same predicate string, same exit-code contract
(0 MET / 1 MISSED / 2 usage-or-drift), all nine live clauses intact.

## Where each of the nine live clauses lives in the minimal form

| Clause | Minimal expression |
|---|---|
| entry-regular | `regular_bytes()` — `lstat` walk: every ancestor component must `S_ISDIR`, leaf must `S_ISREG`; symlinks fail those tests directly |
| row-unique | `len(rs) == 1` on the `rows` dict (all matching lines collected per id) |
| row-well-formed | `len(cs) == 11` — literal/escaped pipes still covered by field count, per clauses.json |
| used-by-exact | `{t for t in (s.strip() for s in cs[10].split(",")) if t} == citing[sid]` |
| status-mined | `cs[7] == "mined"` |
| recheck-valid | `RECHECK.match(cs[9])` — the three census E09 alternatives folded into one alternation |
| digest-match | `rc["sha256"] in cs[5]` |
| gate-quote-substring | `len(qs) == 1` (exactly one line) + `qs[0].encode() in blob` |
| gate-quote-word-bound | `1 <= len(qs[0].split()) <= 25` |

Short-circuit order keeps every `and`-chain safe: `len(cs)==11` precedes `cs[10]`,
`len(qs)==1` precedes `qs[0]`, `blob is not None` precedes `qs[0].encode() in blob`.

## Drops

**Provably dead — no observable change on any tree:**

- `hashlib` import + `digest = sha256(blob)` — computed but never read; the clause is
  `receipt["sha256"] in cs[5]` (frozen digest in the anchor cell), not recomputation.
- `import os` — only used by the dropped fd/O_NOFOLLOW path.
- `from __future__ import annotations` — `X | None` is native on the required py3.10+.
- `rows_for()` — replaced by one `rows` dict built once; per-sid `list` retention keeps
  `len(rs)==1` semantics identical (dup row → `len(rs)>1` → `rs[0]` never read).
- `gate_quote()` — 8 lines → a comprehension collecting all `needle` matches;
  `len(qs)==1` encodes "exactly one" (0 or 2+ → `None` before, fail now — same outcome).
- `valid_recheck()` — ISO/CADENCE/SYMBOLIC union folded into `RECHECK` alternation.
- `cs[5]..cs[10]` named locals — indexed directly in the conjunction.
- `s.strip()`-comprehension is verbatim the original `used_by` construction.
- Two drift `die`s merged into `predicate-or-target-drift`: message text differs,
  exit 2 preserved; string is diagnostic-only, not contract.
- Verbose docstrings → one-line summaries. Clause semantics now live in clauses.json.

**Defence outside the predicate's scope — dropped, each safe because no clause or
control names it, and the predicate's own words cover the residual risk:**

- `MAX_BYTES` + chunked `os.read` loop → `cur.read_bytes()`. The cap is a memory guard,
  not a predicate term; a >8MB receipt still only passes if it contains the quote.
  Only change: memory use on giant trees.
- `st.st_nlink != 1` — hardlink rejection. "Regular file inside the scored root" does
  not exclude hardlinks; the clause stays satisfied/failed by regularity, not link
  count. Divergence: a hardlinked entry now counts as regular — a broader reading of
  the same words, and no control tree hardlinks anything.
- Explicit `S_ISLNK` branches — redundant under `lstat`: symlinks fail `S_ISDIR`
  (interior) and `S_ISREG` (leaf) already. c1-entry-symlink still kills it.
- `O_NOFOLLOW` open — declared non-load-bearing in clauses.json (`o-nofollow-open`),
  TOCTOU-only; the static-tree walk is the load-bearing half.
- Root `lstat` gate — non-dir roots already fail via `NotADirectoryError`/`OSError`
  on the first component walk (proven: `.txt` receipts passed as `--root` give
  identical output). Divergence: a *symlinked* root is now followed instead of
  rejected — outside clause scope, same class of extra-strictness as `nlink`.
- `entry = entry_bytes.decode(...)` split variables → inlined `eb`.

## Equivalence evidence

`count-min.py` vs committed `count.py`, run over `controls/golden` + all ten c1
control trees + every `.txt` receipt dir-miss + the lane root `.`:

- 21/21 identical stdout and exit codes (golden: `TARGET_MET` exit 0;
  every control: `TARGET_MISSED` exit 1 with identical counts; `.`: MISSED,
  open_cites=8 — frozen entries don't exist under the lane root).
- Drift: tampered frozen → `error=predicate-or-target-drift` exit 2;
  missing frozen → `error=frozen-missing` exit 2; argparse usage error exits 2.

Residual divergences (none clause-visible): symlinked scored root now accepted,
hardlinked files now accepted, >8MB files now fully read, drift message text merged.
Each is listed above with its safety argument.
