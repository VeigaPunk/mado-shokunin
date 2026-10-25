# ScoutK2 — ExecK2Receipts inspection

Date: 2026-10-24. Scope: census `.ufo/waves/round-33/scratch/ExecK2Receipts/` and compare its receipt text files against committed `k2-*` controls. Read-only; nothing deleted.

## Census

- `du -sb` → **495,961,904 bytes** (~473 MiB)
- `find . -type f | wc -l` → **30,892 files** (three independent lane `git clone`s: `a-stale/`, `b-rederived/`, `c-perturb/`)
- Five largest files: three identical 18,414,193-byte `.git` packfiles (one per clone), then two 4,207,542-byte `full-sweep.jsonl` copies under `c-perturb/.ufo/waves/round-20|21/...`. Every largest file is byte-identical across all three clones.
- Full table: `.ufo/waves/round-34/scratch/ScoutK2/table.md`

## Receipt comparison — headline

**The scratch tree holds no captured k2 receipt files at all.** Verified three ways: `find -name '*k2*'` → empty; `grep -rl MADO_AXIS` → only pre-existing lane files; `git status` in all three clones → clean. Receipts exist only as text blocks pasted into the committed `w1/reports/ExecK2Receipts.md` / `w1/logs/ExecK2Receipts.log`; re-running `python3 -I quality/check-axis-scores.py` in each clone reproduces those blocks verbatim today.

Against committed `.ufo/waves/round-33/c2/controls/k2-{a,b,c}.txt` (commit `d40b35f90ad8bf630ad9404d25aeee1d9737f300`; the only other committed `k2-*` set, `.ufo/waves/round-32/c2/controls/k2-*.txt`, is byte-identical to it):

| Receipt | Byte-identical to committed? | Verdict |
|---|---|---|
| (a) stale — scratch @ `4590b980`, `mismatched=3` | No | Scratch receipt content nowhere committed. Committed k2-a cites `rev=ff9d6af9…` — resolves in **no** git object store on disk (lane + all 3 clones `git cat-file -t` → fatal); appends `a_exit=1` line the real capture lacks. |
| (b) re-derived — scratch @ `9a46ccf`, `mismatched=0` | No | Same: committed k2-b cites `rev=99eebf89…`, unresolvable everywhere; scratch rev `9a46ccf` is real (lane ancestor). |
| (c) perturb — scratch @ `a3a79ce`, `mismatched=1` | No | Same: committed k2-c cites `rev=91887e68…`, unresolvable everywhere; scratch rev `a3a79ce` lives only in clone c-perturb's `.git`. |
| 39 clone control files (`*/.ufo/waves/round-33/controls/*.txt` + `RECEIPT.md`, 13×3 clones) | Yes, all `cmp`-SAME vs `.ufo/waves/round-33/controls/` | Already committed byte-identically (C1/C2 inputs, not K2 outputs). |

Cross-check: md5 of all 26,304 non-`.git` scratch files vs the three committed k2 hashes → zero matches, either direction.

## Finding

The committed `k2-*.txt` receipts are a **different capture format** (no command line, `x_exit=` footer) and cite `rev=` hashes that resolve in no repository on disk. Commit `d40b35f` (21:08) predates the ExecK2Receipts run (21:12), so the committed receipts cannot be from that run — they record a run whose clones were never committed and whose HEADs exist nowhere. The scratch receipts themselves are honest (verified by live re-run) but remain uncommitted; per the ExecK2Receipts report, backfilling is an operator call.

## Evidence

- `du -sb`, `find … -printf '%s\t%p' | sort -rn`, `git status --porcelain`, `git cat-file -t`, `git merge-base --is-ancestor`, `git ls-tree -r 9a46ccf`, `cmp`, `md5sum` — commands as quoted above and in `table.md`.
- Live gate re-runs in all three clones at 2026-10-24 (outputs in transcript; byte-match the report's §(a)/(b)/(c) blocks).
- Scratch dir left untouched; only writes: `round-34/scratch/ScoutK2/table.md`, this report.
