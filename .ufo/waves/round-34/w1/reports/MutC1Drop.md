# MutC1Drop — clause-drop mutation of c1/count.py (round-34)

Task: one mutant per dropped clause of `PRED-C1-r34-v1`, run against
`controls/golden`, `controls/symlink-crib`, `controls/extra/symlink-parent`.
Mutants live in `.ufo/waves/round-34/scratch/MutC1Drop/` (`count-M{1..6}.py`).
The committed counter `.ufo/waves/round-34/c1/count.py` was never edited —
verified: it still produces the original output below and `diff` against each
mutant shows exactly the intended single clause delta.

## Required verdicts (mutant × tree)

| Mutant | golden (must MET) | symlink-crib (must MISS) | symlink-parent (must MISS) | Wrongly METs |
|--------|-------------------|--------------------------|----------------------------|--------------|
| base   | MET (0)           | MISSED (1)               | MISSED (1)                 | —            |
| M1 nlink!=1 | MET (0)      | MISSED (1)               | MISSED (1)                 | none         |
| M2 symlink/NOFOLLOW | MET (0) | MISSED (1)              | MISSED (1)                 | none         |
| M3 sha256 | MET (0)        | MISSED (1)               | MISSED (1)                 | none         |
| M4 used-by | MET (0)       | MISSED (1)               | MISSED (1)                 | none         |
| M5 word-bound | MET (0)    | MISSED (1)               | MISSED (1)                 | none         |
| M6 component-walk | MET (0) | MISSED (1)              | **MET (0)**                | **extra/symlink-parent** |

## Per-mutant outcome

- **M1 (drop `st.st_nlink != 1`)** — no verdict change on the required trees:
  no tree exercises hardlinks. Supplemental scratch crib (below) proves the
  clause is **load-bearing** against nlink>1 fetch files.
- **M2 (drop `S_ISLNK` checks + `O_NOFOLLOW`)** — identical to baseline on all
  trees, committed and scratch. The clause is **redundant on this suite**:
  leaf symlinks still die on `!stat.S_ISREG(lstat)` and directory symlinks on
  `!stat.S_ISDIR(lstat)`; both checks read `lstat`, which never resolves
  symlinks. The only protection `O_NOFOLLOW`/`S_ISLNK` add beyond that is
  TOCTOU race safety between `lstat` and `open` — no static tree can kill it.
- **M3 (drop `digest == fetch["sha256"]`)** — no change on required trees (no
  tree corrupts bytes). Scratch crib proves **load-bearing** against
  out-of-quote corruption.
- **M4 (drop `used_by_tokens(rows[0]) == {entry_rel}`)** — no change on the
  three required trees, but wrongly **METs the committed control
  `extra/used-by-prefix`** (row uses `corpus/knowledge/waybar-module-text-route-r25.md-…`
  prefix token). Clause **load-bearing**.
- **M5 (drop `1 <= len(words) <= 25`)** — **provably dead code under this
  frozen.json**: `found == quote` already forces `words == quote.split()`;
  the frozen quotes are 8 and 1 words, inside [1,25], so the bound can never
  fail when `found == quote` holds. No crib can distinguish it without
  rewriting the frozen spec. Redundant for `PRED-C1-r34-v1` as frozen.
- **M6 (drop per-component walk)** — wrongly **METs `extra/symlink-parent`**
  where `.ufo/waves/round-34/fetch` is a symlink to `held-fetch/`; final-path
  `lstat` resolves through the intermediate symlink, so the leaf looks like a
  clean regular file. Clause **load-bearing**: the walk is the sole guard
  against symlinked intermediate directories. Still misses `symlink-crib`
  because leaf `lstat` catches leaf symlinks.

## Required-tree outputs (verbatim)

```
M1 | golden               exit=0  closed_entries=1 closed_rows=2 open_cites=0 TARGET_MET
M1 | symlink-crib         exit=1  closed_entries=0 closed_rows=0 open_cites=2 TARGET_MISSED
M1 | extra/symlink-parent exit=1  closed_entries=0 closed_rows=0 open_cites=2 TARGET_MISSED
M2 | golden               exit=0  closed_entries=1 closed_rows=2 open_cites=0 TARGET_MET
M2 | symlink-crib         exit=1  closed_entries=0 closed_rows=0 open_cites=2 TARGET_MISSED
M2 | extra/symlink-parent exit=1  closed_entries=0 closed_rows=0 open_cites=2 TARGET_MISSED
M3 | golden               exit=0  closed_entries=1 closed_rows=2 open_cites=0 TARGET_MET
M3 | symlink-crib         exit=1  closed_entries=0 closed_rows=0 open_cites=2 TARGET_MISSED
M3 | extra/symlink-parent exit=1  closed_entries=0 closed_rows=0 open_cites=2 TARGET_MISSED
M4 | golden               exit=0  closed_entries=1 closed_rows=2 open_cites=0 TARGET_MET
M4 | symlink-crib         exit=1  closed_entries=0 closed_rows=0 open_cites=2 TARGET_MISSED
M4 | extra/symlink-parent exit=1  closed_entries=0 closed_rows=0 open_cites=2 TARGET_MISSED
M5 | golden               exit=0  closed_entries=1 closed_rows=2 open_cites=0 TARGET_MET
M5 | symlink-crib         exit=1  closed_entries=0 closed_rows=0 open_cites=2 TARGET_MISSED
M5 | extra/symlink-parent exit=1  closed_entries=0 closed_rows=0 open_cites=2 TARGET_MISSED
M6 | golden               exit=0  closed_entries=1 closed_rows=2 open_cites=0 TARGET_MET
M6 | symlink-crib         exit=1  closed_entries=0 closed_rows=0 open_cites=2 TARGET_MISSED
M6 | extra/symlink-parent exit=0  closed_entries=1 closed_rows=2 open_cites=0 TARGET_MET   <-- wrongly MET
```

Baseline (`c1/count.py`, unedited): golden MET/exit 0; symlink-crib MISSED/exit 1;
symlink-parent MISSED/exit 1.

## Supplemental evidence (outside required scope)

Committed cribs `extra/used-by-prefix`, `symlink-entry`, `extra/symlink-sources`,
`rows-only`, `entries-only`: every mutant returns identical verdicts to baseline
**except M4 on `extra/used-by-prefix`**:

```
M4 | extra/used-by-prefix exit=0  closed_entries=1 closed_rows=2 open_cites=0 TARGET_MET   <-- wrongly MET
```

Two scratch cribs built under `scratch/MutC1Drop/cribs/` to exercise the
otherwise-untested clauses (golden copies; one defect each):

- `cribs/hardlink`: `fetch/S201.bin` hardlinked to `cribs/hardlink/held-S201.bin`
  (nlink=2). Baseline MISSED (`closed_rows=1 open_cites=1`); **M1 wrongly MET**
  (`exit=0, closed_entries=1 closed_rows=2 open_cites=0`). All other mutants
  still MISS.
- `cribs/corrupt`: last byte of `fetch/S201.bin` XOR-flipped (quote at offset
  1010 of 6550 untouched). Baseline MISSED (`closed_rows=1 open_cites=1`);
  **M3 wrongly MET** (`exit=0`). All other mutants still MISS.

## Mutant diffs vs `c1/count.py`

```diff
--- M1 (drop nlink!=1)
-        if not stat.S_ISREG(st.st_mode) or st.st_nlink != 1:
+        if not stat.S_ISREG(st.st_mode):
```

```diff
--- M2 (drop S_ISLNK checks and O_NOFOLLOW)
-    if stat.S_ISLNK(root_stat.st_mode) or not stat.S_ISDIR(root_stat.st_mode):
+    if not stat.S_ISDIR(root_stat.st_mode):
         return None
     cur = root
     for i, part in enumerate(parts):
         cur = cur / part
         try:
             st = cur.lstat()
         except OSError:
             return None
-        if stat.S_ISLNK(st.st_mode):
-            return None
         last = i == len(parts) - 1
         ...
-        fd = os.open(cur, os.O_RDONLY | os.O_NOFOLLOW)
+        fd = os.open(cur, os.O_RDONLY)
```

```diff
--- M3 (drop sha256 comparison)
                 and quote.encode() in blob
-                and digest == fetch["sha256"]
                 and len(rows) == 1
```

```diff
--- M4 (drop used-by equality)
                 and len(rows) == 1
-                and used_by_tokens(rows[0]) == {entry_rel}
             )
```

```diff
--- M5 (drop 1-25 word bound)
                 and found == quote
-                and 1 <= len(words) <= 25
                 and quote.encode() in blob
```

```diff
--- M6 (drop per-component walk; single lstat on joined leaf)
     cur = root
-    for i, part in enumerate(parts):
+    for part in parts:
         cur = cur / part
-        try:
-            st = cur.lstat()
-        except OSError:
-            return None
-        if stat.S_ISLNK(st.st_mode):
-            return None
-        last = i == len(parts) - 1
-        if not last:
-            if not stat.S_ISDIR(st.st_mode):
-                return None
-            continue
-        if not stat.S_ISREG(st.st_mode) or st.st_nlink != 1:
-            return None
     try:
+        st = cur.lstat()
+    except OSError:
+        return None
+    if stat.S_ISLNK(st.st_mode):
+        return None
+    if not stat.S_ISREG(st.st_mode) or st.st_nlink != 1:
+        return None
+    try:
         fd = os.open(cur, os.O_RDONLY | os.O_NOFOLLOW)
```

## Summary

- **Load-bearing** (some tree kills the mutant): M1 (scratch hardlink crib),
  M3 (scratch corrupt crib), M4 (committed `extra/used-by-prefix`),
  M6 (committed `extra/symlink-parent`).
- **Redundant on this suite**: M2 — `lstat`-based `S_ISREG`/`S_ISDIR` checks
  already reject every symlink position; dropped guards only matter against
  a TOCTOU race, untestable statically.
- **Dead clause**: M5 — implied by `found == quote` for the frozen spec;
  unkillable without editing `c1/frozen.json`.

Gap noted for the control suite: committed controls contain no hardlink crib
and no corrupt-bytes crib; M1/M3 needed scratch cribs to be killed. Adding
`controls/hardlink` and `controls/corrupt` (one-line each from golden) would
make the required tree set alone kill all distinguishable mutants.
