# ScoutScratch12 — round-33 scratch tree triage

**Deliverable:** `.ufo/waves/round-34/scratch/ScoutScratch12/table.md`

**Method:** `git hash-object` per scratch file vs. all 5916 unique blobs in
`git ls-tree -r HEAD`. `du -sb` per tree. `find -type l` / `-type d -empty`:
no symlinks, no empty dirs. Nothing moved or deleted.

**Scope caveat:** the named comparison paths (`round-33/w1/reports/` +
`round-33/controls/`) contain only report/control files — **zero** scratch
files match them; literally all 12 trees are UNIQUE vs. that scope. The
meaningful verdict uses the parenthetical "committed elsewhere" = any HEAD
blob.

## Verdicts

| Tree | Files | Bytes | Verdict |
|---|---|---|---|
| CriticC1FalseNeg | 7 | 63603 | UNIQUE — 3 corpus `.md` files uncommitted (4 `.bin` are committed fetch copies) |
| ExecAppendDraft | 1 | 3995 | UNIQUE |
| ExecCollision | 11 | 1816 | UNIQUE — only `guard-proof-{registry,staged}-fixture.md` (141 B) uncommitted |
| MutC1Counter | 1 | 3923 | UNIQUE — mutated `count.py` differs from committed `round-33/c1/count.py` |
| ReviewC2Predicate | 16 | 5327 | UNIQUE — all probe cards + transcript |
| ReviewRound30 | 1 | 4786 | UNIQUE |
| ScoutConsider | 1 | 2172 | UNIQUE |
| ScoutQuarantine | 1 | 637 | REDUNDANT — bytes at `round-3{2,3,4}/assimilation/quarantine-slice` |
| ScoutS189Quote | 1 | 1404 | UNIQUE |
| ScoutS190 | 1 | 6550 | REDUNDANT — bytes at `round-33/fetch/S190.bin` (= `round-34/fetch/S201.bin`) |
| ScoutS191 | 1 | 8324 | REDUNDANT — bytes at `round-33/fetch/S191.bin` (= `round-34/fetch/S202.bin`) |
| ScoutS197 | 1 | 41392 | REDUNDANT — bytes at `round-33/fetch/S197.bin` |

4 REDUNDANT · 8 UNIQUE (2 only partially). Uncommitted bytes live mostly in
doctored fixtures, probe cards, transcripts and mutated scripts — i.e. the
novel content, not the copied fetch binaries.
