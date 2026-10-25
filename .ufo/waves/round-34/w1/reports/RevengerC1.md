# RevengerC1 — falsification of the round-34 c1 coverage claim

Target: `.ufo/waves/round-34/c1/count.py` + `frozen.json`. Trees under
`.ufo/waves/round-34/scratch/RevengerC1/`. Committed counter unmodified.
Sibling `RevC1PathEscape.md` covered lexical/symlink path escapes; this report
covers **content binding** — what `TARGET_MET` actually certifies about the
scored tree.

Command for every tree:

    python3 .ufo/waves/round-34/c1/count.py --root <tree> --frozen .ufo/waves/round-34/c1/frozen.json

## Baseline (lane root)

```
PRED-C1-r34-v1 closed_entries=1 closed_rows=2 open_cites=0 verdict=TARGET_MET
rc=0
```

## A0 control — byte-identical copy of real entry + registry + blobs

```
PRED-C1-r34-v1 closed_entries=1 closed_rows=2 open_cites=0 verdict=TARGET_MET
rc=0
```

Establishes the tree-construction harness is not the defect.

## A1 right names, wrong content — **BROKE THE CLAIM**

`a1-imitator/`: fabricated entry whose only true lines are the two frozen
gate-quotes; fabricated `corpus/SOURCES.md` citing `fabricated://never-fetched-*`
sources with both rows hidden **inside a fenced code block**; real fetch bytes.

```
PRED-C1-r34-v1 closed_entries=1 closed_rows=2 open_cites=0 verdict=TARGET_MET
rc=0
real entry sha256 : 1236017410947e74f7dd679a6a8e2c93219ce915834d00a482b775ad76133e3f
A1   entry sha256 : faf77548350758959a24fe2b87d4eec37ee456d448f1466f3d3af257898c96d6  (differs)
```

`TARGET_MET` on a corpus that was never admitted and asserts fabricated claims.
Root cause: the predicate pins exactly two line-strings per entry
(`gate_quote`, `found == quote`), one digest per blob, and one row shape per
sid. Entry body, registry provenance, other columns, and whether rows live in
prose or a code fence (`ROW_RE` matches `^ {0,3}\|` — fences are invisible) are
all unpinned. `--root` is also caller-supplied: nothing binds the verdict to
the lane root at all.

## A2 entry symlink to file outside root — refused

`a2-entry-symlink/`: `SOURCES.md` regular, entry → `/tmp/revengerC1-outside-entry.md`.

```
PRED-C1-r34-v1 closed_entries=0 closed_rows=0 open_cites=2 verdict=TARGET_MISSED
rc=1
```

`read_regular` `lstat`s the leaf: `S_ISLNK` → `None` → both cites open.

## A3 right sha blob, different in-blob quote line — refused

`a3-alt-quote/`: S201's gate-quote line replaced by
`// socket path, specified by EventManager` — a 5-word string that is a real
substring of the S201 blob. Blob digest untouched.

```
PRED-C1-r34-v1 closed_entries=0 closed_rows=1 open_cites=1 verdict=TARGET_MISSED
rc=1
```

`found == quote` compares against the **frozen** quote, not against blob
content. Exact pinning holds.

## A4a used-by = entry path among other tokens — refused

`a4a-extra-token/`: S201's used-by cell `corpus/lessons/round-13.md,
corpus/knowledge/waybar-module-text-route-r25.md`.

```
PRED-C1-r34-v1 closed_entries=0 closed_rows=1 open_cites=1 verdict=TARGET_MISSED
rc=1
```

`used_by_tokens(rows[0]) == {entry_rel}` is exact set equality.

## A4b used-by = same token twice — **PASSED (set-collapse laxity)**

`a4b-dup-token/`: used-by cell
`corpus/knowledge/waybar-module-text-route-r25.md,corpus/knowledge/waybar-module-text-route-r25.md`.

```
PRED-C1-r34-v1 closed_entries=1 closed_rows=2 open_cites=0 verdict=TARGET_MET
rc=0
```

The comma-token set collapses duplicates. A malformed row that names the entry
twice counts as "the entry path as a whole used-by token". Weak break —
predicate letter holds, registry semantics violated — but it shows the cell is
parsed, never validated.

## A5 fetch blob hardlinked (nlink=2) — refused

`a5-hardlink/`: real corpus bytes, S201 blob hardlinked to `decoy/S201-copy.bin`.

```
PRED-C1-r34-v1 closed_entries=0 closed_rows=1 open_cites=1 verdict=TARGET_MISSED
rc=1
```

`st_nlink != 1` rejection works.

## A6 single-file bind mount from outside root — **BROKE THE CLAIM**

`a6-bindmount/`: real corpus copies; `corpus/knowledge/waybar-module-text-route-r25.md`
bind-mounted over `/tmp/revengerC1-outside-entry.md` (371 bytes of fabricated
content, sha256 `7f41b2f9…ce0ea`, everything outside the two gate-quote lines
different). `sudo -n mount --bind`, counter, `umount`.

```
PRED-C1-r34-v1 closed_entries=1 closed_rows=2 open_cites=0 verdict=TARGET_MET
counter_rc=0
umount_rc=0
1236017410947e74f7dd679a6a8e2c93219ce915834d00a482b775ad76133e3f  <entry restored after umount>
```

`lstat`/`O_NOFOLLOW` verify inode *shape* (regular, nlink=1, path components
inside root). A single-file bind mount satisfies all of that while the bytes
live outside the scored root. The "path components stay inside" wording is
satisfied; the "inside the scored root" intent is not.

## Verdict

**The coverage claim is falsified.** `TARGET_MET` does not certify that the
scored tree is the admitted corpus — it certifies only the pinned surfaces:
frozen paths are regular nlink=1 files, fetch bytes digest-match `frozen.json`,
the entry contains the exact frozen quote lines, and exactly one `| Sid |`-like
row per sid carries a last-cell token-set equal to the entry path. A1 shows the
rest of the corpus can be arbitrary; A6 shows even the entry bytes need not
live inside the root; A4b shows registry cells are parsed but not validated.

Refused attempts confirmed the pinning is *exact* where it exists: symlinked
leaves, alternative quotes, extra used-by tokens, and hardlinks all miss.

Three strongest attacks: **A1** fabricated-content impostor tree → MET;
**A6** bind-mount content-lives-outside-root → MET; **A4b** duplicated used-by
token → MET.
