# CritC1FalseNeg — false-MET attack on PRED-C1-r34-v1

Date: 2026-10-24. Counter under test: `.ufo/waves/round-34/c1/count.py`
(frozen spec `.ufo/waves/round-34/c1/frozen.json`, predicate PRED-C1-r34-v1).
Mission: build trees that are NOT the claimed corpus and check whether the
counter wrongly prints `TARGET_MET`. Five avenues, each a full minimal tree
under `.ufo/waves/round-34/scratch/CritC1FalseNeg/`, each run as:

```sh
python3 -I .ufo/waves/round-34/c1/count.py --root <tree> --frozen .ufo/waves/round-34/c1/frozen.json
```

Every tree carries a forged `corpus/SOURCES.md`, a forged
`corpus/knowledge/waybar-module-text-route-r25.md` (gate-quote lines copied
verbatim), and fetch bins. None of them is the claimed corpus.

## Results

| Tree | Exit | Counter output | Wrong MET? |
|---|---|---|---|
| `baseline` (forged but well-formed lookalike) | 0 | `closed_entries=1 closed_rows=2 open_cites=0 verdict=TARGET_MET` | No — predicate genuinely satisfied by construction; the counter scores shape, not corpus identity. |
| `a-fetch-hardlink` (S201.bin hardlinked to `scratch/CritC1FalseNeg/outside-a/foreign-S201.bin`, bytes correct) | 1 | `closed_entries=0 closed_rows=1 open_cites=1 verdict=TARGET_MISSED` | No. `read_regular` lstats each component; `st_nlink=2` on the leaf → rejected. Correct per spec (`nlink=1` clause). Verified `stat -c %h`: nlink=2 on both names of the inode. |
| `b-entry-hardlink` (entry file hardlinked to `outside-b/foreign-entry.md`) | 1 | `closed_entries=0 closed_rows=0 open_cites=2 verdict=TARGET_MISSED` | No. Same `nlink != 1` guard; entry bytes never read, both cites open. Correct. |
| `c-usedby-trailspace` (used-by cell = `corpus/knowledge/waybar-module-text-route-r25.md `, trailing space inside cell, both S201 and S202 rows) | 0 | `closed_entries=1 closed_rows=2 open_cites=0 verdict=TARGET_MET` | **No defect — token semantics.** `used_by_tokens()` splits on `|` then `.strip()`s each cell and each `,`-token, so the compared set is exactly `{entry_rel}`. Markdown table-cell whitespace is conventional padding; the predicate's phrase "lists the entry path as a whole used-by token" is about token identity, not byte equality of the cell. `cat -A` confirms the space is on the wire (`...r25.md  |$`). |
| `d-usedby-case` (used-by cells in different case: `CORPUS/KNOWLEDGE/...` and `Corpus/Knowledge/Waybar-Module-Text-Route-r25.Md`) | 1 | `closed_entries=0 closed_rows=0 open_cites=2 verdict=TARGET_MISSED` | No. Set membership is a byte-exact string compare; case-mangled token ≠ `entry_rel`. Correct on a case-sensitive FS. |
| `e-dup-rows` (S201 appears in TWO registry rows: decoy row with used-by `corpus/other/PLACEHOLDER.md`, then a correct row) | 1 | `closed_entries=0 closed_rows=1 open_cites=1 verdict=TARGET_MISSED` | No. `rows_for()` collects every line matching `^ {0,3}\|\s*(S[0-9]+)\s*\|`; `len(rows) == 1` fails → open cite, entry not closed. Correct — predicate says "the registry row for that id" (singular). |

Control for calibration: the claimed corpus (lane root `.`) prints
`closed_entries=1 closed_rows=2 open_cites=0 verdict=TARGET_MET`, exit 0.

## Verdict

**No defect found.** Zero of five avenues produced a wrongful `TARGET_MET`.

The avenue-C tree does MET — but that is correct scoring, not a false
positive: after Markdown-conventional cell/token trimming its used-by token
is byte-identical to the frozen entry path, so every predicate clause holds
on that tree. Only if the predicate were re-read as demanding raw byte
equality of the cell would it be drift; "whole used-by token" plus the
counter's comma-tolerant tokenization make trim-then-compare the defensible
reading. Flagged here so the interpretation is on record.

## Why the hardline avenues cannot work against this counter

- `read_regular()` (count.py:40-85) enforces, per path component:
  `lstat` → reject symlink → non-leaf must be dir → leaf must be
  `S_ISREG` **and** `st_nlink == 1`, then opens with `O_NOFOLLOW`.
  A hardlink to a foreign inode always shows `nlink ≥ 2` → `None` →
  open cite. Byte-identical contents are irrelevant.
- Relative-path guard rejects absolute paths and any `""`/`"."`/`".."`
  component (lines 41-44), pinning resolution under `--root`.
- Registry matching is byte-exact on the S-id (`m.group(1) == sid`),
  requires exactly one matching row, and compares the full token set to
  the singleton `{entry_rel}` (lines 149-157). Extra rows, extra tokens,
  or case drift all fail.

## Residual gaps observed (not exercised into a wrong MET)

- `used_by_tokens()` assumes the **last** `|`-cell is the used-by column;
  a row whose last cell is the entry path while the real used-by cell
  says something else still closes the cite. Shape-consistent with the
  corpus's fixed column order, but it is column-name-blind.
- `rows_for()` regex-counts `| S201 |`-looking lines anywhere in the file,
  including inside fenced code blocks — i.e. it is table-unaware. In the
  exercised dup-row avenue this fails closed (more rows → MISS), so no
  false-MET path was found through it.
- `gate_quote()` is prefix-based per line (`gate-quote: <sid> `); two
  matching lines return `None` and the cite opens — also fail-closed.

## Evidence artifacts

Trees and the foreign files they link to are left in place under
`.ufo/waves/round-34/scratch/CritC1FalseNeg/` (`baseline/`,
`a-fetch-hardlink/`, `b-entry-hardlink/`, `c-usedby-trailspace/`,
`d-usedby-case/`, `e-dup-rows/`, `outside-a/`, `outside-b/`). Outputs
quoted above were captured live from the runs at write time.
