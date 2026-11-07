# `quality/tool-ledger.md` rows for round 97 (draft)

Row grammar enforced by `quality/check-tool-ledger.py --repo . --rev REV` (read from its own
docstring at base):

```
| `<repo-relative path>` | <one-line description> | `<pointer path>` |
```

- Population = files under `tools/` (any extension) + `quality/*.py` + `quality/counters/*.py`,
  derived from the tree at `--rev`. A row whose path is outside that population is `dangling`, so
  `quality/selftest-kills/check-receipt-presence.json` gets **no** row (it is `quality/selftest-kills/`, a
  `.json`, and not a `.py` child of `quality/` or `quality/counters/`).
- The pointer must name a tracked file that exists at `--rev` and whose bytes contain the row file's
  basename. The declaration names all three basenames, so it is a valid pointer for each row.

## Rows (append at the table's end)

```
| `tools/mado-filetype.py` | Read-only GIO 2.90.1 path content type (round 97): what `standard::content-type` and `standard::fast-content-type` answer for a PATH - the stat branches in order (symlink broken or nofollow, directory, character device, block device, FIFO, zero-size regular, socket), the alias rewrite every branch answer passes through, the basename-only guess and the three states that make it uncertain, and the sniff of `min(database max extent, 16384)` bytes taken only when not `--fast` and uncertain, with a failed open or read keeping the name-only answer; `--selftest` 20+ checks; a `lstat` that fails with an errno other than `EACCES` is refused per path with exit 2. | `.ufo/waves/round-97/claims-declaration-r97.md`, `corpus/knowledge/gio-content-type-file-r97.md` |
```

```
| `quality/counters/c1-r97-filetype.py` | Read-only C1 counter (round 97): scores `tools/mado-filetype.py` at a revision (pinned to the frozen candidate and the three sibling lane modules, structurally checked, every run under an audit-hook launcher with an empty `PATH`) against per-path labels from the installed `/usr/bin/gio` - 15 sha-pinned classes with at least 8 cases each, a fresh seeded leg, and the host's own paths and special files - and kills the frozen mutants by class while the do-nothing, naive, memoriser and library-asking forgery controls stay behind. | `.ufo/waves/round-97/claims-declaration-r97.md`, `.ufo/waves/round-97/receipts/c1-measured-r97.txt` |
```

```
| `quality/counters/c2-r97-counter-selftest.py` | Read-only C2 counter (round 97): scores the two round-96 counters' new `--selftest` mode at a revision - a frozen panel of single-check neutralisations each flagged with its declared finding id, the broken-input modes (missing input, wrong revision, mutated tool) each named with the declared id and exit, the base counter bytes refusing `--selftest`, an always-OK stub flagged on every neutralisation, and the `SKILL.md` registry rows for the four round-96 artifacts re-derived at `--rev`. | `.ufo/waves/round-97/claims-declaration-r97.md` |
```

## Notes for the L1

1. The C1 row's second pointer assumes the receipt name `.ufo/waves/round-97/receipts/c1-measured-r97.txt`
   (the round-96 precedent). If the receipt lands under another name, swap the cell: the checker
   refuses a pointer that does not exist at `--rev`, and the declaration alone satisfies the
   basename rule if the receipt path is uncertain.
2. `quality/check-tool-ledger.py --repo . --rev <rev>` must report `uncovered=0 dangling=0
   bad_pointer=0 empty_desc=0 verdict=TARGET_MET` after the round's `.py` files land. This draft
   does not run it (the files do not exist at base); the C2 predicate's clause (v) is the L1's run.
3. Descriptions are read from each instrument's own contract, never from its name: the tool's from
   the round-97 shared contract 1, the C1 counter's from the declaration's C1 predicate, the C2
   counter's from the declaration's C2 predicate. If a landed counter's docstring says something
   narrower, the row follows the docstring.
