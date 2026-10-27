# w1 / ExecCloneRecipe — seat clone recipe under a file-size cap + the owed clause-r mutant attack

Seat `ExecCloneRecipe`, round 49, wave w1 = BUILD. Lane `/home/vgpnk/Projects/shokunin/mado-shokunin`,
base `03e4ae76aff7a4be59cb69970dd553baa319695a`, measured at lane HEAD
`5f37c1b87b3ce5e438d19284e32b2e46fd548a92` (22,285 tracked entries, 37 symlinks, 22,248 regular files,
344,224,633 B worktree without `.git`).
Targets: **M48-13** (`corpus/lessons/round-48.md:269`, routed at `:285`) and the round-48 residual
"the new-mutant attack on clause r is not run this round" (`corpus/lessons/round-48.md:467`).

Nothing here scores a frozen predicate: the mutants below are scored against
`PRED-C1-r48-v2` as it stands at the lane tip (`quality/counters/c1-r48-terminal-cache-v2.py`,
sha256 `5bb9aead5d4bd311cc0e178746ef297f5f75d635b1d8b69be5df0dfa1372cf46`), which is the round-48 frozen
instrument, not a round-49 one.

Scratch: `/fast/scratch/hyaku/mado-r49/ExecCloneRecipe/` (removed before return). No lane file is written
except this report and this seat's own directory. No tool was installed; `hyprctl`/`xkbcli` not used;
`~/.cache/xdg-terminal-exec` is read only (stat + sha256) and is labelled operator-owned.

---

## 0. The unit bug that M48-13 was standing on

`ulimit -f` in GNU bash counts **1024-byte units**, not 512. Calibration
(`receipts/clone-recipes/summary.txt:5-7`, `bash 5.3.20(1)-release`, `git 2.56.0`):

```
$ bash -c 'ulimit -f 2048; ulimit -f; head -c 5000000 /dev/zero > cal.bin; echo rc=$?'
2048
rc=1                 # head: error writing 'standard output': File too large
cal.bin bytes=2097152
```

So the round-48 dispatch bound "`ulimit -f 2048` (512-byte units; 1 MiB per regular file)"
(`.ufo/waves/round-48/a4r1-dispatch.json:16`, repeated at `:21`, `:26`, `:31`) actually gave every a4r1
seat a **2 MiB** cap, and a true 1 MiB cap is `ulimit -f 1024`. Both caps are measured below, because the
premise ("1 MiB") and the value the seats really ran under ("2048") are different instruments.

Consequence for M48-13: the aborts were real *even at 2 MiB* — `git clone -q --shared` under
`ulimit -f 2048` exits 128 (section 2) — so the seat-side error quote "checkout could not complete because
RLIMIT_FSIZE=1 MiB rejects numerous committed large files"
(`.ufo/waves/round-48/a4r1-results.json:40`) was a correct observation under a wrongly named cap.

---

## 1. Recipe matrix (measured, `--shared` clone of the lane at `5f37c1b8`)

All runs are in `receipts/clone-recipes/` (`recipes2.sh` is the driver; every row is one run of it).
`rc` is the recipe's own exit status; "truncated" is counted by comparing each extracted regular file's
size with its blob size (`receipts/clone-recipes/verify-extracted.txt`).

| # | recipe (one shell, cap applied outside it) | cap 1024 = 1 MiB | cap 2048 = 2 MiB | cap 65536 = 64 MiB |
|---|---|---|---|---|
| R1 | `git clone -q --shared LANE c` (full checkout) | **rc=128**, 24 files refused, `.git/index` never written | **rc=128**, 14 files refused, `.git/index` never written | **rc=0**, index 3,061,833 B, largest file 4,207,542 B |
| R2 | `git clone -q --shared --no-checkout LANE c` | **rc=0**, 25 `.git` files / 28,692 B, no index | **rc=0** | — |
| R3 | R2 + `git archive REV -- tools quality/counters corpus/knowledge README.md \| tar -x` | **rc=0**, 126 regular files, **0 size mismatches** (max 299,141 B) | **rc=0**, 0 mismatches | — |
| R4 | R2 + `git archive REV \| tar -x` (every path) | **rc=2**, 24 files truncated at 1,048,576 B | **rc=2**, 14 files truncated at 2,097,152 B | rc=0, 0 mismatches |
| R5 | R2 + `git sparse-checkout set tools quality corpus/knowledge` + `git checkout REV` | **rc=128** `fatal: sha1 file …/.git/index.lock write error: File too large` | **rc=128**, same | rc=0, index 3,104,273 B |
| R6 | R5 with `-c index.version=4` | **rc=128**, same index wall | **rc=0**, index 1,951,445 B, 158 files, 0 mismatches | — |
| R7 | `git -C LANE archive REV -- tools quality/counters corpus/knowledge README.md \| tar -x` (**no clone at all**) | **rc=0**, 126 files, 0 mismatches, no `.git` written | — | — |
| R8 | `git show REV:<blob> > file` | rc=255 on the 4,207,542 B blob, file truncated at 1,048,576 B, **stderr empty**; rc=0 on `tools/mado-terminal.py` (68,940 B) | rc=255 / truncated at 2,097,152 B | rc=0 |
| R9 | R2 + `git read-tree HEAD` (index written, worktree untouched) | **rc=128**, `.git/index.lock` File too large | **rc=128**, same | — |

Logs: `clone-*.log`, `sparse-*.log`, `archive-*.log`, `show-*`, `noclone-archive-1024.log`;
per-run `rc`, file counts, byte counts and the files left exactly at the cap are in `summary.txt`;
the isolated index wall is `readtree-index.txt`.

`—` means not run at that cap because a strictly larger measured recipe already succeeded there (R3 ⊂ R4,
R2 ⊂ R1 at 64 MiB) or the row only discriminates below 64 MiB (R6, R7, R9).

---

## 2. The failing file, per recipe

* **R1 @1024** — git refuses exactly the **24 blobs larger than 1 MiB** (`blobs-gt-1mib.txt`) and names
  each one before aborting:
  ```
  error: unable to write file .ufo/waves/round-20/w2/AdvCrash/fixtures/huge_bash_cmd.jsonl
  …
  fatal: unable to checkout working tree
  warning: Clone succeeded, but checkout failed.
  ```
  The first one git names is `.ufo/waves/round-20/w2/AdvCrash/fixtures/huge_bash_cmd.jsonl`
  (blob 2,000,199 B, left at 1,048,576 B); the largest is
  `.ufo/waves/round-20/w2/CorpusRuntime/full-sweep.jsonl` (4,207,542 B).
* **R1 @2048** — exactly the **14 blobs larger than 2 MiB** (`blobs-gt-2mib.txt`), first
  `.ufo/waves/round-20/w2/CorpusDiffIndependent/corpus-diff-results.json` (2,167,818 B).
* **R4** — tar names every file it could not finish, e.g.
  `tar: .ufo/waves/round-20/w2/CorpusRuntime/full-sweep.jsonl: Wrote only 1536 of 10240 bytes`.
  At 1024: 22 `Wrote only …` lines + 2 `Cannot write: File too large`
  (`.ufo/waves/round-21/corpus/snapshot/files/.ufo/waves/round-20/w2/AdvCrash/fixtures/huge_eval_comment.jsonl`,
  `.ufo/waves/round-22/audit/fixtures/cases/AuditRawSnapshotAtLimit/root/snapshot.json`) = 24 = the blobs
  > 1 MiB; at 2048: 12 + 2 (`corpus-diff-results.json`, `evidence/corpus-comparison.json`) = 14 = the
  blobs > 2 MiB. No failing file is left unnamed by tar (checked against the blob-size table). Truncation
  is real, not just a log line: the extracted
  `full-sweep.jsonl` hashes `a74940a3…` while the blob hashes `c78a9de3…`.
* **R5/R6/R9** — the failing file is **`.git/index.lock`**, never a worktree file: the index for 22,285
  entries is **3,061,833 B** (default) / **3,104,273 B** (cone sparse) and cannot be written under either
  cap even when no worktree byte is written at all (R9).
* **R8** — the failing file is the redirect target itself: `git show` truncates it at the cap, exits 255
  and writes **nothing** to stderr, so the only trustworthy signal is the exit status.

**Two independent walls, not one.** R9 isolates the second: a recipe that only needs the index still
fails at both caps, so shrinking the checked-out path set is not sufficient — `--no-checkout` (which never
writes an index) is. Only `index.version=4` brings the sparse index under 2 MiB (1,951,445 B), and never
under 1 MiB.

---

## 3. Recipe to hand the next wave

Under **≥ 1 MiB per file, no `.git` needed** (read-only reads of a revision): R7, no clone at all —
`git -C LANE archive REV -- <paths> | tar -x -C <scratch>`; measured rc=0 with 0 mismatches at a 1 MiB cap.

Under **≥ 1 MiB, an object store needed** (the c1 counter takes `--repo/--rev`): R2 (`--no-checkout`,
28,692 B of `.git`, rc=0 at 1 MiB) + R3 for the paths the work needs; measured rc=0 and 0 mismatches.

Never: R1 (full clone) unless the cap exceeds both 4,207,542 B (largest blob) and 3,061,833 B (index) —
only 64 MiB was measured as passing; R5 (sparse checkout) unless the cap exceeds its 3,104,273 B index
(R6's `index.version=4` index is 1,951,445 B and passes at 2 MiB, measured); R9; or a bare
`git show REV:<blob> > file` anywhere near the cap (truncation with rc=255 and no message).

The wave-dispatch sentence to fix: "`ulimit -f 2048` (512-byte units; 1 MiB per regular file)" is
2 MiB in bash; a true 1 MiB cap is `ulimit -f 1024`, and a 64 MiB cap is `ulimit -f 65536`.

---

## 4. Clause-r mutant attack (`PRED-C1-r48-v2`, `--nonce 4848`)

### Method

* Clone: `git clone -q --shared LANE mut/c` under `ulimit -f 65536` (= recipe R1, rc=0);
  `git -C mut/c rev-parse --show-toplevel` printed exactly `/fast/scratch/hyaku/mado-r49/ExecCloneRecipe/mut/c`
  before the first commit. Commits carry a throwaway identity (`-c user.name=r49-w1 -c user.email=r49-w1@invalid.invalid`,
  `GIT_CONFIG_NOSYSTEM=1`, `HOME` in scratch); nothing was committed in the lane.
* Mutants: `mkmutants-r49.py` (beside this report) inserts ONE hook immediately before
  `if __name__ == "__main__":` of `tools/mado-terminal.py`; the hook runs at import on every invocation,
  performs one violation, reports on stderr (which the counter discards — `run_case`/`explain_case` keep
  stdout and rc only) and never touches stdout or the exit status. Diff: `receipts/mutants.diff`.
  The hooks' only write targets are `/tmp/r49-w1-probe`, a relative `r49-w1-probe` in the case root, and
  `tempfile.mkdtemp()` — all inside bwrap's own tmpfs. **`HOME` is never a write target**, so the M48-10
  class cannot recur even if a hook ran unsandboxed.
* Scored with the lane's frozen instrument,
  `quality/counters/c1-r48-terminal-cache-v2.py` (sha256 `5bb9aead…`), on the scratch clone:
  `python3 -I -B …/c1-r48-terminal-cache-v2.py --repo mut/c --rev <commit> --work <scratch>/work-<tag> --nonce 4848`,
  with `HOME`, `XDG_{CONFIG,CACHE,DATA,STATE}_HOME` and `TMPDIR` all under the seat scratch and
  `PYTHONDONTWRITEBYTECODE=1` (the lane's `__pycache__` is not written).
* Control: the clone's own tip `5f37c1b87b3ce5e438d19284e32b2e46fd548a92` (the unmutated tool) through the
  same invocation at the same nonce.

### Result

| run | rev | hook | clause `r` | functional clauses | verdict | rc | wall |
|---|---|---|---|---|---|---|---|
| `ref` (control) | `5f37c1b8` | none | `trips=0` | 190/190 · 228/228 · 418/418 · 230/230 · selftest ok | **TARGET_MET** | 0 | 186 s |
| `M-WRITE` | `2d71108c69446bac588321c49b3ab32a4a792e91` | writes `/tmp/r49-w1-probe`, cwd `r49-w1-probe`, `mkdtemp` | `trips=14840` `write:mkdir("/tmp/r49-w1-00tkhse0", 0700) = 0;…` | 190/190 · 228/228 · 418/418 · 230/230 · selftest ok | **TARGET_MISSED** | 1 | 179 s |
| `M-FORK` | `af43e9a61818424db1f34fa6fc3cb80ed0db2a49` | `os.fork()` + pipe | `trips=2969` `clone(child_stack=NULL, flags=CLONE_CHILD_CLEARTID\|…)` | 190/190 · 228/228 · 418/418 · 230/230 · selftest ok | **TARGET_MISSED** | 1 | 195 s |
| `M-SOCKET` | `e5940755cc058f168f11c1cc2991ed64cac69fc8` | `socketpair`, `AF_UNIX socket`+`connect` | `trips=8907` `connect(3, {sa_family=AF_UNIX, sun_path="/r49-w1-no-such.soc…;socket(AF_UNIX, …) = 3;socketpair(AF_UNIX, …)` | 190/190 · 228/228 · 418/418 · 230/230 · selftest ok | **TARGET_MISSED** | 1 | 202 s |

(Full clause lines, `clause=a/s/f/w/x/g/r` plus the final tally, are in `receipts/ref.txt`,
`receipts/M-WRITE.txt`, `receipts/M-FORK.txt`, `receipts/M-SOCKET.txt`; the reference run's tally is byte-identical
to the round-48 `receipts/v2/ctl/FINAL.txt` line, and its tool content hashes
`143820476403085d2ee71c1f12529efd8206ed24914703698e3584611d189f34` = the round-48 ctl `tool_sha256`.)

**Both directions hold at nonce 4848.** The two classes round-48 w2 measured as *blind* under v1
(`MutC1ReadOnly.md` §1: "M-WRITE … clause `r` `trips=0` … TARGET_MET" and "M-FORK … `trips=0` …
TARGET_MET") now trip under v2's write/process surface
(`quality/counters/c1-r48-terminal-cache-v2.py:162` `PROC_SET` includes `fork`/`vfork`/`clone`/`clone3`,
`:164` `WRITE_SET`, `:358` `check_trace`, `:1047` `readonly = "fail" if box.trips else "ok"`), and the
unmutated tool still MEETS on the same host, clone, work dir and nonce. Attribution is exact: every
functional clause stays at 100 % in all three mutants, so the miss is caused by clause `r` alone.

---

## 5. Operator-owned host state around the attack

| file | before (`receipts/operator-before.txt`, 01:39:28) | after (`receipts/operator-after.txt`, 01:52:31) |
|---|---|---|
| `~/.cache/xdg-terminal-exec` (operator-owned, M48-10 target) | sha256 `ddd94f6bca4bcd42c426da9bbeb9955ca5d77b8778b4e290fcfffcc984a1b3d5`, size 190, mtime 1793069967 | **identical** (same sha256, size and mtime) |

Read-only `stat` + `sha256sum` only; the content was never read, copied or committed. The before value is
also the L1's round-49 `receipts/operator-state-before.txt` value, so the lane did not disturb this file
between the L1's capture and this seat's.

---

## 6. What each finding attacks / supports

* **M48-13, the bound itself** — attacks `.ufo/waves/round-48/a4r1-dispatch.json:16`
  ("`ulimit -f 2048` (512-byte units; 1 MiB per regular file)"): `ulimit -f` in GNU bash 5.3.20 is
  1024-byte units, so the value the a4r1 seats ran under was 2 MiB (`receipts/clone-recipes/summary.txt:6-8`).
  The aborts were nevertheless real: `clone-full-2048` rc=128 with 14 blobs refused
  (`.ufo/waves/round-48/a4r1-results.json:40` records the seat-side error that the phrase was aimed at).
* **M48-13, the recipe** — supports `corpus/lessons/round-48.md:269` with a measured recipe set
  (section 1): the two walls are the 24/14 oversized blobs and the 3,061,833 B index, and the working
  recipes are R7 (no clone, `git archive -- <paths> | tar -x`, rc=0 at 1 MiB) and R2+R3
  (`--no-checkout` + archive, rc=0 at 1 MiB), not a smaller sparse checkout (R5 dies on `.git/index.lock`
  at both caps).
* **The owed clause-r attack** — attacks the round-48 residual
  `corpus/lessons/round-48.md:467` ("the new-mutant attack on clause r is not run this round") and the
  routed item `round-48-verifier-spotcheck.md` §6; supports `PRED-C1-r48-v2`'s clause `r` both ways
  (control MEETS, three mutants MISS with clause `r` as the only failing clause).

## 7. Risks and residuals of this seat's own evidence

* The mutants are scored against the **round-48 frozen** `PRED-C1-r48-v2`, not a round-49 predicate; w2 owns
  the attack on whatever round 49 freezes.
* `--nonce 4848` fixes the generated cases, so these four runs are not independent draws against the
  generator; the fixture clauses are the same 190 cold + 228 warm cases the instrument always runs.
* `PROC_SET` (`:162`) traces `clone`, so a tool that starts a **thread** (`clone` with `CLONE_THREAD`) trips
  clause `r` although no process is started. The reference tool has no threads, so this is a
  false-positive surface for a future compliant-but-threaded tool, not a present defect.
* `git show REV:<blob> > file` under a cap exits 255 with an **empty stderr** and a truncated file
  (`show-big-1024.out` 1,048,576 B, rc=255): a recipe that routes output through a redirect must check the
  exit status, because nothing else reports the truncation.
* `index.version=4` (R6) is a git-implementation detail (measured with git 2.56.0); the default index is what
  any seat gets, and it does not fit either cap.
* Cap semantics: RLIMIT_FSIZE bounds a single regular file, not a tree or a process total; the caps here do
  not bound total scratch bytes.
* The extracted-tree check compares 22,247 of 22,248 regular files (one path is skipped by the
  `ls-tree -l` name split); symlink entries are excluded from the comparison because their blob is the
  target string.

## 8. Cleanup, tooling and quote check

* Scratch `/fast/scratch/hyaku/mado-r49/ExecCloneRecipe/` (clone, recipe trees, work dirs) is removed before
  return; only the seat directory and this report remain in the lane (`git status --porcelain` shows the
  seat dir under `.ufo/waves/round-49/w1/` and no other new path of this seat).
* No tool installed or upgraded; `git 2.56.0`, `bash 5.3.20`, `python3`, `bwrap` and `strace` were already
  present. No compositor call, no package transaction, no GUI, no network.
* Every quote in this report is checked mechanically by `receipts/verify-quotes.sh` against a receipt in
  `receipts/`: `bash receipts/verify-quotes.sh` → `checked=34 missing=0` (`receipts/verify-quotes.txt`).
* Seat inventory: this report, `mkmutants-r49.py`, `receipts/{ref,M-WRITE,M-FORK,M-SOCKET}.txt`,
  `receipts/mutants.diff`, `receipts/operator-{before,after}.txt`, `receipts/clone-recipes/` (driver,
  per-recipe logs, `summary.txt`, blob tables, the extracted-tree check, the index-wall probe) and
  `receipts/verify-quotes.{sh,txt}`.
