# R2 digest — `out.json.rows.tsv` (round-46 seat file, untracked)

Seat: ExecR2Digest (round 47, wave w1). Target:
`.ufo/waves/round-46/w1/ExecStofOracle/receipts/out.json.rows.tsv`, the round-46 leftover named in
`corpus/lessons/round-46-verifier-spotcheck.md:28` and `:111`. Nothing in this seat's target was edited,
moved or deleted; all measurement was read-only and the two reproduction builds ran under
`/fast/scratch/hyaku/mado-r47/ExecR2Digest/` (removed at the end).

## 1. File identity (measured, not typed)

| property | value | how |
|---|---|---|
| path | `.ufo/waves/round-46/w1/ExecStofOracle/receipts/out.json.rows.tsv` | — |
| sha256 | `6573f76b5a61c6d0270ae4bfb9b3f37d7e95825c6fbfb13858a78fe54d6d3238` | `sha256sum` |
| bytes | 3 282 451 | `wc -c` |
| lines | 59 395 (1 header + 59 394 data rows), LF, newline-terminated | `wc -l`, byte split |
| encoding | UTF-8; no CR anywhere; 11 rows carry U+00A0 (NBSP) | byte scan |
| longest line | 108 bytes, line 49142 | byte scan |
| git state | untracked (`?? …`), **not** gitignored (`git check-ignore` exit 1) | `git status --porcelain`, `git check-ignore -v` |
| committed neighbour | `receipts/out.json`, 2 172 bytes, sha256 `946ed60daefc26da105dc358cde1601446330b50279fb531f50ed9994a759627` | `sha256sum` |

Column header (byte-verified against line 1 by `receipts/verify-locators.sh`):

```
cat	cls	ref_line	truth_line	ref_printed	truth_printed	text
```

## 2. Row count per class column

Correct parse (`line.split("\t", 6)`, 59 394 rows), cross-checked with `awk -F'\t' 'NR>1{c[$2]++}'`
(identical numbers, because `cls` is column 2 for every row):

| `cls` | rows | line_flip | top_flip | print_differs |
|---|---:|---:|---:|---:|
| same_value | 55 229 | 0 | 0 | 0 |
| value_ulp_diff | 2 751 | 2 751 | 2 751 | 2 751 |
| both_unset | 1 294 | 0 | 0 | 0 |
| ref_refuses_cpp_both_unset | 64 | 0 | 64 | 0 |
| ref_refuses_cpp_stores | 37 | 29 | 37 | 37 |
| other | 19 | 19 | 19 | 19 |
| **total** | **59 394** | **2 799** | **2 871** | **2 807** |

Category column: 21 values, in file order `dec1 3051, dec2 6101, dec3 2227, dec4 1200, dec5 1200,
dec6 1200, dec7 1200, half3 30501, half3r 1017, prefix 306, exp 309, subnormal 22, hex 14, nonfinite 20,
ws 15, longdigits 7, dblround_above 3000, dblround_at 3000, dblround_below 3000, dblround_hand 4,
junk 2000`. 16 of the 21 categories are contiguous blocks; `dblround_above/at/below` interleave
one row each (`gen.py:140-145` emits the triple per iteration, lines 48392-57391), followed by the
contiguous `dblround_hand` (57392-57395) and `junk` (57396-59395).
There is no case-index column: row order is `cases.tsv` order.

## 3. Relation to the committed `out.json` beside it

Producer (verified locators, `diff.py` in the seat root, sha256
`b8d5c1a2fee4e2ee004beaf8a1d66d27cca5413c9a73e9fc2f95de7970fe3d9a`, identical to the `receipts/` copy):
`diff.py:167` appends one dict per case (`cat, text, cls, ref_line, truth_line, ref_printed,
truth_printed, kind`); `diff.py:185` writes `out.json`, then `diff.py:187-188` opens `out.json.rows.tsv`
with the header and `diff.py:191` writes 7 of those 8 fields per row. **The TSV is the `rows` list with
`kind` dropped** — nothing else is filtered or reordered.

Re-derivation of every committed aggregate from the TSV alone (script `receipts/derive.py`, output
`receipts/analysis.txt`, machine copy `receipts/rederived.json`). Top-level key order is
`cases, categories, classes, flips, examples, dump_json_breaks, dump_json_break_examples,
trim_mismatch_unverified, reported_roundtrip_failures`.

| out.json field | committed | re-derived from TSV | equal |
|---|---|---|---|
| `cases` | 59 394 | 59 394 | yes |
| `categories` | 21 | 21 | yes |
| `classes` (all 6, `n`/`line_flip`/`top_flip`/`print_differs`) | see §2 | identical dict | yes |
| `flips.total` | 2 871 | 2 871 | yes |
| `flips.by_class` | 5 keys: `other\|line:DIFFER->AGREE\|top:DIFFER->OK` 19, `ref_refuses_cpp_both_unset\|line:AGREE->AGREE\|top:NOT_COMPARED->OK` 64, `ref_refuses_cpp_stores\|line:DIFFER->AGREE\|top:NOT_COMPARED->OK` 29, `ref_refuses_cpp_stores\|line:SETUP->SETUP\|top:NOT_COMPARED->SETUP` 8, `value_ulp_diff\|line:DIFFER->AGREE\|top:DIFFER->OK` 2 751 | identical | yes |
| `examples` keys and their first 3 elements (`text`, `ref_printed`, `truth_printed`) | 5 keys, 5-tuples | 5 keys, 3-tuples | keys yes, 3/5 fields yes |
| `dump_json_breaks` | 8 | 8 | yes |
| `dump_json_break_examples` | 8 triples (`nonfinite`: `nan`, `NaN`, `NAN`, `nan(1)`, `nan(chars)`, `-nan`, `+nan`, `nan()`) | identical | yes |
| `trim_mismatch_unverified` | 4 | 4 (`text.strip(" \t\r\n\v\f") != text.strip(" \t\r\n")`) | yes |
| `reported_roundtrip_failures` | 0 | 0 | yes |

Two fields are **not literal columns**, so they were recomputed, not read:
`ref_top`/`truth_top` (needed for `top_flip`, the `flips` keys) do not exist in the TSV; they follow
from `diff.py:123-135` once `kind` is recovered from `cls` (the class assignment at `diff.py:139-150`
is a bijection on `kind` × `cpp_set`: `same_value`/`value_ulp_diff`/`other` are `kind==ok`,
`ref_refuses_cpp_stores`/`ref_refuses_cpp_both_unset` are `kind==unsupported`,
`ref_unset_cpp_stores`/`both_unset` are `kind==unset`), and `truth_top` is `SETUP` iff `truth_line` is `SETUP`.
`cpp_bits`/`cpp_reason` appear only inside committed `examples` (e.g. `value_ulp_diff` carries
`1000593163`); the TSV prints `truth_printed` with `"%.2f"`, so the f32 bit pattern is not
recoverable from it — the 2 trailing example fields are the only committed data this file cannot
supply. Conversely `kind` per row is *not* in the TSV, but is implied by `cls` as above.

## 4. What only this file holds (and why deleting it is still lossless)

The TSV is the only artifact that identifies individual cases: which 2 871 rows flipped and which 8
rows carry the non-finite (invalid-JSON) field. `out.json` keeps one example per flip pattern only.
That identity is nevertheless reproducible: this seat re-ran the committed pipeline in scratch —

```
g++ -std=c++23 -O1 -o stmt stmt.cpp
python3 -I gen.py cases.tsv                     # cases=59394 categories=21, cases.tsv sha256 fb355339…
python3 -I diff.py cases.tsv ./stmt <lane>/.ufo/waves/round-46/l1-draft/mado-devices.py out.json
```

with `gen.py`, `stmt.cpp`, `diff.py` copied from the seat root (sha256 per `receipts/sha256.txt`) and the
reference `l1-draft/mado-devices.py` sha256 `b229efd08d2d329dd60ced114598943d0419dac2f3cf05b1f6c1eb506c49a33b`,
g++ 16.2.1 (`receipts/versions.txt`). Result (`receipts/repro-sha256.txt`): `out.json` sha256
`946ed60d…` and `out.json.rows.tsv` sha256 `6573f76b…`, **both byte-identical to the worktree copies**
(`cmp -s` exit 0, 59 395 lines, 3 282 451 bytes). `gen.py` uses a fixed seed (`random.Random(46)`), so
the corpus is deterministic; the only environment pin is the toolchain in `receipts/versions.txt`.

## 5. Consumer caveats (measured)

- 8 rows contain **literal tabs inside `text`** — lines 47945-47949 (`\t5`, `\t5.`, `\t.5`, `\t5.0`,
  `\t0.25`), 48373 (`\t0.5`), 48374 (`0.5\t`), 48375 (`\t\t0.5\t`). `awk -F'\t'`/`cut` give `NF` 8
  (7 rows) and 10 (line 48375); columns 1-6 stay correct, only `text` is truncated. Parse with
  `split("\t", 6)`.
- 11 rows carry U+00A0 in `text` (lines 47718, 47739, 47760, 47781, 47802, 47823, 47844, 47865, 47886,
  47907, 47928; the `prefix` category's `"\u00a0"` suffix from `gen.py`). A latin-1 reader sees `\xc2\xa0`.
- No CR, no embedded newline: every record is exactly one line, so `wc -l` bounds the row count.

## 6. Digest line the L1 commits in place of the file

> `out.json.rows.tsv` (round-46 `ExecStofOracle/receipts/`, untracked, not gitignored): sha256
> `6573f76b5a61c6d0270ae4bfb9b3f37d7e95825c6fbfb13858a78fe54d6d3238`, 3 282 451 bytes, 59 395 LF lines
> = 1 header `cat cls ref_line truth_line ref_printed truth_printed text` + 59 394 rows; rows per class
> `same_value` 55 229 (0/0 flips) / `value_ulp_diff` 2 751 (line 2 751, top 2 751, print 2 751) /
> `both_unset` 1 294 (0/0) / `ref_refuses_cpp_both_unset` 64 (line 0, top 64) / `ref_refuses_cpp_stores`
> 37 (line 29, top 37) / `other` 19 (19/19) over 21 categories (`half3` alone 30 501, `dec2` 6 101); the
> file is `diff.py:167`'s per-case `rows` list serialized at `diff.py:187-191` with the `kind` field
> dropped, and every scalar field of the committed `out.json` (`cases` 59 394, `categories` 21, the six
> class counters, `flips.total` 2 871 with all five `by_class` keys, `dump_json_breaks` 8 with all eight
> `nan` triples, `trim_mismatch_unverified` 4, `reported_roundtrip_failures` 0) re-derives exactly from
> it, the sole committed residue not recoverable being the two `examples` fields `cpp_bits`/`cpp_reason`;
> the only per-case information it uniquely held — the identity of the 2 871 flipped rows and the 8
> non-finite rows — is byte-reproducible from committed `gen.py`+`stmt.cpp`+`diff.py` plus
> `l1-draft/mado-devices.py` `b229efd0…` on g++ 16.2.1 (regenerated `out.json` `946ed60d…` and
> `rows.tsv` `6573f76b…`, both `cmp`-identical), so this line plus the committed harness replaces the
> 3.3 MB file with no loss; consumers must split `text` with `maxsplit 6` (8 rows contain literal tabs)
> and read the file as UTF-8 (11 rows contain U+00A0).

## Retained evidence (this seat)

- `receipts/analysis.txt` — full re-derivation run (file identity, field histogram, per-field equality,
  class/flip/category tables).
- `receipts/rederived.json` — the summary rebuilt from the TSV alone.
- `receipts/derive.py` — the re-derivation script (`python3 -I derive.py <rows.tsv> <out.json>
  [<out-rebuilt.json>]`; no hardcoded paths, rechecked to reproduce `receipts/rederived.json` byte-for-byte).
- `receipts/repro-sha256.txt` — regenerated `out.json` / `out.json.rows.tsv` / `cases.tsv` / `stmt` hashes
  plus the worktree copies they were compared against.
- `receipts/verify-locators.sh`, `receipts/locators.txt` — every `diff.py` / header locator above
  recomputed by `grep -n` from the live files (`7/7 ok`).
