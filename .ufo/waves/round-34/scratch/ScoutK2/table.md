# ScoutK2 — ExecK2Receipts census & receipt-vs-committed comparison

Date: 2026-10-24. Read-only; nothing deleted.

## Directory census — `.ufo/waves/round-33/scratch/ExecK2Receipts/`

| Metric | Value | Command |
|---|---|---|
| `du -sb` size | 495,961,904 bytes | `du -sb .` |
| File count | 30,892 | `find . -type f \| wc -l` (26,304 non-`.git` + 4,588 inside the three clone `.git/` dirs) |
| Top-level layout | `a-stale/`, `b-rederived/`, `c-perturb/` — three independent `git clone`s of the lane (report §Method, `.ufo/waves/round-33/w1/reports/ExecK2Receipts.md`) | `ls` |

Five largest files (sorted by size, first five rows of `find . -type f -printf '%s\t%p\n' | sort -rn`):

| Size (bytes) | Path |
|---|---|
| 18,414,193 | `c-perturb/.git/objects/pack/pack-151d941dc3fff354a69af19ce49e8e6a9f4ded6e.pack` |
| 18,414,193 | `b-rederived/.git/objects/pack/pack-151d941dc3fff354a69af19ce49e8e6a9f4ded6e.pack` |
| 18,414,193 | `a-stale/.git/objects/pack/pack-151d941dc3fff354a69af19ce49e8e6a9f4ded6e.pack` |
| 4,207,542 | `c-perturb/.ufo/waves/round-21/corpus/snapshot/files/.ufo/waves/round-20/w2/CorpusRuntime/full-sweep.jsonl` |
| 4,207,542 | `c-perturb/.ufo/waves/round-20/w2/CorpusRuntime/full-sweep.jsonl` |

(Each largest-file size is shared across all three clones — identical content replicated 3×; the three .pack files and all six `full-sweep.jsonl` copies are byte-identical triples.)

## What "receipt text files" the directory holds

The ExecK2Receipts task produced **no captured k2 receipt files inside the scratch tree**. Verified:

- `find . -name '*k2*' -not -path '*/.git/*'` → empty.
- `grep -rl 'MADO_AXIS' . | grep -v '/.git/'` → only pre-existing lane files (`SCORECARD.md`, `LOG.md`, round-32 reports/fixtures) — no captured run output.
- `git status --porcelain` in all three clones → clean; no untracked receipt captures.
- No clone contains `.ufo/waves/round-33/c2/controls/` — the dir does not exist at their HEADs (each clone's `.ufo/waves/round-33/c2/` holds only `count.py`).

The receipts exist only as **text blocks pasted into the committed report/log** (`w1/reports/ExecK2Receipts.md`, `w1/logs/ExecK2Receipts.log`). Re-running the gate live in each scratch clone reproduces those blocks verbatim (verified 2026-10-24).

## Per-receipt comparison — scratch receipts vs committed `k2-*`

Committed comparator set: `.ufo/waves/round-33/c2/controls/k2-{a,b,c}.txt` (committed `d40b35f90ad8bf630ad9404d25aeee1d9737f300`, mado-shokunin). Only other committed `k2-*` files: `.ufo/waves/round-32/c2/controls/k2-{a,b,c}.txt` — `cmp` shows each is **byte-identical** to its round-33 twin (same single commit added all six).

| Receipt (scratch source) | Scratch content | Committed counterpart | Byte-identical? | Verdict |
|---|---|---|---|---|
| (a) stale — clone `a-stale` @ `4590b980…` | 4 MADO_AXIS lines, `mismatched=3 rev=4590b9803cbbb276f942054d2120d54c4851c757`, `exit=1` | `k2-a.txt` | **No** | **Content nowhere committed.** Committed `k2-a.txt` cites a different `rev=ff9d6af91b7bd3c48e4f33d67ca59ed9edb66152` that resolves in **no** git object store on disk (lane repo + all 3 clones: `git cat-file -t` → fatal), and appends an `a_exit=1` line absent from the real capture. Row text matches; rev/footer differ. |
| (b) re-derived — clone `b-rederived` @ `9a46ccf…` | 4 MADO_AXIS lines, `mismatched=0 rev=9a46ccf3282117f960b8d53cd71599a91f388ee3`, `exit=0` | `k2-b.txt` | **No** | **Content nowhere committed.** Committed `k2-b.txt` cites `rev=99eebf891a3d97690d51e8fbcb91e0e4f902a722` — not a git object anywhere on disk; real scratch rev `9a46ccf` IS the lane object store. Same `b_exit=0` footer difference. |
| (c) perturb — clone `c-perturb` @ `a3a79ce…` | 4 MADO_AXIS lines, `mismatched=1 rev=a3a79cee6a48e9a7294edce538ee410a12f5d402`, `exit=1` | `k2-c.txt` | **No** | **Content nowhere committed.** Committed `k2-c.txt` cites `rev=91887e68378198914cbf2907989231a81fc5c85f` — not a git object anywhere on disk; real scratch rev `a3a79ce` exists only in clone `c-perturb`'s `.git`. Same `c_exit=1` footer difference. |
| Round-33 control texts — `{a,b,c}-*/.ufo/waves/round-33/controls/*.txt` + `RECEIPT.md` (13 files × 3 clones = 39) | c1/c2 control inputs | `.ufo/waves/round-33/controls/` (committed) | **Yes — all 39 `cmp` SAME** | Already committed byte-identically. These are the only `.txt`-class receipt-named files in the tree; they are C1/C2 *inputs*, not K2 outputs. |

Exhaustive check: md5 of all 26,304 non-`.git` files under `ExecK2Receipts/` vs the three committed `k2-*` hashes (`87912b3b…`, `687272e3…`, `af3fc421…`) → **zero matches**. No file in the scratch tree is byte-identical to any committed k2 receipt, in either direction.

## Timing

Commit `d40b35f` (21:08:35 -0300) predates the ExecK2Receipts scratch creation (dir mtime 21:12, report mtime 21:13:18) — the committed k2 receipts were **not** produced by this run; they record a different, untraceable run whose three `rev=` hashes exist in no object store on disk. Clone `b-rederived`'s HEAD `9a46ccf` is an ancestor of `d40b35f` (`git merge-base --is-ancestor` → true) whose tree contains zero `k2-*` paths (`git ls-tree -r 9a46ccf | grep -c k2-` → 0) — consistent with all three clones lacking `.ufo/waves/round-33/c2/controls/`.

