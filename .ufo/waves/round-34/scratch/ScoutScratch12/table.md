# ScoutScratch12 — round-33 scratch tree triage

Method: `git hash-object` per file, compared against every blob committed in HEAD
(`git ls-tree -r HEAD`, 5916 unique blobs). Byte-identity match means the same
content exists at some committed path, regardless of filename. `du -sb` is the
apparent size of the tree. No tree contains symlinks or empty dirs. Nothing was
moved or deleted.

Scope note: the literal named scope (`round-33/w1/reports/` + `round-33/controls/`)
contains only report and control `.md`/`.txt` files — **zero** scratch-file bytes
match it (all 12 trees UNIQUE under that reading). The verdicts below use the
parenthetical's broader reading, "bytes already committed elsewhere" = any blob in
HEAD, which is the deletion-safety question this table exists to answer.

| Tree | Files | Bytes (du -sb) | Files committed elsewhere | Verdict |
|---|---|---|---|---|
| CriticC1FalseNeg | 7 | 63603 | 4/7 | UNIQUE (partial) |
| ExecAppendDraft | 1 | 3995 | 0/1 | UNIQUE |
| ExecCollision | 11 | 1816 | 9/11 | UNIQUE (partial) |
| MutC1Counter | 1 | 3923 | 0/1 | UNIQUE |
| ReviewC2Predicate | 16 | 5327 | 0/16 | UNIQUE |
| ReviewRound30 | 1 | 4786 | 0/1 | UNIQUE |
| ScoutConsider | 1 | 2172 | 0/1 | UNIQUE |
| ScoutQuarantine | 1 | 637 | 1/1 | REDUNDANT |
| ScoutS189Quote | 1 | 1404 | 0/1 | UNIQUE |
| ScoutS190 | 1 | 6550 | 1/1 | REDUNDANT |
| ScoutS191 | 1 | 8324 | 1/1 | REDUNDANT |
| ScoutS197 | 1 | 41392 | 1/1 | REDUNDANT |

## Per-file detail

### CriticC1FalseNeg — UNIQUE (partial)
- `golden/corpus/knowledge/event-delivery-limits-r26.md` (114 B) — UNIQUE
- `golden/corpus/knowledge/waybar-module-text-route-r25.md` (183 B) — UNIQUE
- `golden/corpus/SOURCES.md` (561 B) — UNIQUE
- `golden/.ufo/waves/round-32/fetch/S189.bin` (6479 B) — committed: `round-32/fetch/S189.bin`, `round-32/scratch/ScoutIPCEventMgr/EventManager.cpp`, `round-24/fetch/w1/ScoutAttributionSweep-src-managers-EventManager.cpp.bin`
- `golden/.ufo/waves/round-33/fetch/S190.bin` (6550 B) — committed: `round-33/fetch/S190.bin` (also `round-34/fetch/S201.bin` + 7 round-34 control copies)
- `golden/.ufo/waves/round-33/fetch/S191.bin` (8324 B) — committed: `round-33/fetch/S191.bin` (also `round-34/fetch/S202.bin` + 7 round-34 control copies)
- `golden/.ufo/waves/round-33/fetch/S197.bin` (41392 B) — committed: `round-33/fetch/S197.bin`

The three corpus `.md` files are doctored golden-fixture copies — nowhere committed.

### ExecAppendDraft — UNIQUE
- `append-block.md` (3995 B) — UNIQUE

### ExecCollision — UNIQUE (partial)
- `collisions.txt` (25 B) — committed: `round-33/assimilation/collisions`, `round-34/assimilation/collisions`, `round-32/assimilation/collisions`
- `guard-proof-collisions-col0.txt` (0 B) — committed (empty blob; 200+ paths, e.g. `round-33/assimilation/fixture-ids-col0`)
- `guard-proof-collisions-tolerant.txt` (5 B) — committed: `round-33/assimilation/fixture-ids`, `round-32/assimilation/f2`
- `guard-proof-reg-ids-col0.txt` (10 B) — committed: `round-32/assimilation/guard-proof-reg-ids-col0.txt`
- `guard-proof-reg-ids-tolerant.txt` (15 B) — committed: `round-32/assimilation/guard-proof-reg-ids-tolerant.txt`
- `guard-proof-registry-fixture.md` (97 B) — UNIQUE
- `guard-proof-staged-fixture.md` (44 B) — UNIQUE
- `guard-proof-staged-ids-col0.txt` (5 B) — committed: `round-33/assimilation/fixture-ids`, `round-32/assimilation/f2`
- `guard-proof-staged-ids-tolerant.txt` (5 B) — committed: `round-33/assimilation/fixture-ids`, `round-32/assimilation/f2`
- `reg-ids.txt` (950 B) — committed: `round-33/assimilation/reg-ids`, `round-34/assimilation/reg-ids`
- `staged-ids.txt` (660 B) — committed: `round-33/assimilation/staged-ids`, `round-32/assimilation/staged-ids`

Only the two `guard-proof-*-fixture.md` files (141 B total) are uncommitted.

### MutC1Counter — UNIQUE
- `count.py` (3923 B) — UNIQUE. Note: `round-33/c1/count.py` is committed but is a *different* blob (mutation target vs. mutated script).

### ReviewC2Predicate — UNIQUE
- All 16 files UNIQUE: 12 `case-*.card`, `control-pass.card`, `probe-frozen.card`, `probe-head.card`, `TRANSCRIPT.txt` (2309 B). Predicate-probe fixture cards exist nowhere else.

### ReviewRound30 — UNIQUE
- `verdict.md` (4786 B) — UNIQUE

### ScoutConsider — UNIQUE
- `note.md` (2172 B) — UNIQUE

### ScoutQuarantine — REDUNDANT
- `slice.txt` (637 B) — committed: `round-33/assimilation/quarantine-slice`, `round-32/assimilation/quarantine-slice`, `round-34/assimilation/quarantine-slice`

### ScoutS189Quote — UNIQUE
- `receipts.txt` (1404 B) — UNIQUE

### ScoutS190 — REDUNDANT
- `S190.bin` (6550 B) — committed: `round-33/fetch/S190.bin` (also `round-34/fetch/S201.bin` + 7 round-34 control copies)

### ScoutS191 — REDUNDANT
- `S191.bin` (8324 B) — committed: `round-33/fetch/S191.bin` (also `round-34/fetch/S202.bin` + 7 round-34 control copies)

### ScoutS197 — REDUNDANT
- `S197.bin` (41392 B) — committed: `round-33/fetch/S197.bin`
