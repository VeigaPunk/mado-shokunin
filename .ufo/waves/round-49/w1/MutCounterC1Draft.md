# MutCounterC1Draft — r49 w1 — mutation-testing the C1 counter draft's clauses

status: COMPLETE (2026-10-27 ~02:20-03:00). All five clauses (f, g, s, r, t) killed: for each, a one-line
counter mutant + an exploit tool flip the verdict TARGET_MISSED → TARGET_MET. No unexploitable weakening
found. One design finding recorded (sandbox import closure), fixed by ExecCounterC1 during the round and
re-verified against the fixed draft.

## Target and versions

Counter under mutation: the round-49 C1 counter draft `c1-r49-keysym.py` (PRED-C1-r49), seat
`.ufo/waves/round-49/w1/ExecCounterC1/`. Three versions seen while working; the clause code under test
(t/s/f/g/r checks) is identical across all of them:

- `6f559c27bab3f5995d598a8b3a1b3c68082978760adb624b7fe0c78093ce1500` — embedded 57-fixture fallback only
- `3a9e46a922912073f980e7aad1cd4d1c8a4aafe23ec546acbd8c4e4df4f8d4bf` — 633-case fixture file authoritative
- `1a7fcc21b7508db46f6a22325de84f6ed115fd81b63607a364c1c4addd27b4fe` (732 lines) — sandbox `ldd` closure
  widened to every lib-dynload extension's deps (my finding 1, below, fixed); libxkbcommon absence asserted

My copies (pristine + 7 mutants) live in this seat dir; the original was never modified. Restoration
evidence: the original's sha256 re-checked at the end = `1a7fcc21…` (the version ExecCounterC1 published);
the fixture file `c1-r49-fixtures.json` sha256 `81836bfba624a0a4344c4787f7058219b45554fbcfc2da9d797846d96610e393`
unchanged; `git status --porcelain` on the lane shows only the L1's own round-49 harness files and the 47
known `*.synthetic` sidecars (routed item N1) besides wave seats — nothing of mine outside my seat dir.

## Method

For each clause: a one-line counter mutant weakening exactly that clause, plus an exploit tool that
violates the property the clause protects and conforms everywhere else. Pair killed = pristine counter
says TARGET_MISSED on the exploit and the mutant says TARGET_MET.

All runs at `--nonce 424242`, fixed so the exploit tables can cover the generated draws — declared: the
exploit tools are nonce-conditioned table tools, not keysym resolvers; with a random nonce the g clause
rightly stops them (that is exactly what the g pair demonstrates). Every run: `env -i` with
HOME/XDG_CACHE_HOME/XDG_CONFIG_HOME/XDG_DATA_HOME/XDG_STATE_HOME/TMPDIR under
`/fast/scratch/hyaku/mado-r49/MutCounterC1Draft/` (deleted at cleanup), `ulimit -f 65536`, work dir under
that scratch, never /tmp. Fixture repos: scratch git repos, `git init`, toplevel asserted equal to the
repo dir, throwaway identity per commit inside the repo only.

Answer table: 681 `(sha256(keymap bytes), arg) -> (rc, stdout bytes)` entries recorded from the pinned
judge (`/usr/lib/xkbcommon/xkbcli-how-to-type` sha `f6c0b122…`, keymaps from the pinned compile-keymap sha
`43b924f6…`, judge env replicated exactly: PATH=/usr/bin, HOME/XDG_CONFIG_HOME in scratch, LC_ALL=C).
Validation: all 633 fixture-file recorded sha256 reproduce (drift=none); all 60 nonce-424242 generated
draws compile and judge; no generated draw collides with any fixture pair, so the f-exploit's single
corrupted fixture cannot leak into clause g.

## Pairs and verdicts (counter base 1a7fcc21…, receipts `receipt-run2-*.txt`)

| clause | mutant (one-line weakening) | exploit tool | pristine | mutant |
|---|---|---|---|---|
| t | mode set gains `b"120000"` | x-t-clean committed as a SYMLINK blob (mode 120000), content = conforming table tool | MISSED (tool=absent) | MET |
| t2 (rev-addressing) | `git show REV:TOOL` → `open(repo/TOOL)` | repo-t2: broken tool committed, conforming tool only in the working tree | MISSED (g 0/60 on the committed tool) | MET |
| g | `GEN = 60` → `0` | x-g-fixtures-only: answers the 633 fixtures from the table, fixed garbage elsewhere | MISSED (generated=0/60, first_fail g000 arg=multiply) | MET |
| f | `f_ok += ok` → `f_ok += 1` | x-f-corrupt-fixture: table correct except fixture r49-c1-0399 (us/altgr-intl, slash) loses its last row, rc kept | MISSED (fixtures=632/633) | MET |
| s | `SELFTEST_MIN = 25` → `0` | x-s-weak-selftest: conforming table tool, `--selftest` prints `MADO_KEYSYM_SELFTEST: 3/3 passed` | MISSED (selftest=fail) | MET |
| r (no-process) | trip regex `^(PROC_SET)\(` → `^(socket\|connect)\(` | x-r-fork: conforming table tool that `os.fork()`s a child on every scored run | MISSED (trips=693 `clone(child_stack=NULL, flags=CLONE_CHILD_CLEARTID…`) | MET (trips=0) |
| r (no-write) | write-trip `elif` → `elif False and (…)` | x-r-append: conforming table tool that attempts `open(keymap, 'ab')` on every scored run | MISSED (trips=693 `write:openat(AT_FDCWD, "/fixture/keymap.xkb", O_WRONLY\|O_CREAT\|O_A…`) | MET (trips=0) |

Attribution is single-clause in every pristine run: the non-target clauses all pass (f 633/633, g 60/60,
selftest ok, refusals ok, trips=0 — see the receipts). The same pairs also killed on the pre-fix base
3a9e46a9… (receipts `receipt-run1-*.txt`), except its t runs which used the earlier base64-built exploit
that crashed inside the then-unfixed sandbox — superseded by the run2 set. Baseline: pristine counter at
a tool-absent rev → `tool=absent verdict=TARGET_MISSED` rc 1 (`receipt-run2-base-pristine.txt`), matching
ExecCounterC1's own receipts-base.

trips=693 = exactly one trip per scored run (633 fixtures + 60 generated), i.e. the tripwires see every
run, not an accident of one.

## Findings

1. **Sandbox import closure (clause i) — found, reported, fixed by ExecCounterC1, re-verified.** The
   clause-i mount set originally bound only the `ldd <python3>` closure + stdlib tree; stdlib extension
   modules needing libz.so.1/libssl.so.3 died inside the sandbox. Probe (one import per tool blob, the
   counter's own Box.run; receipt `receipt-sandbox-imports.txt`): sys/os/re/hashlib/json/struct/stat/
   tempfile/shutil/argparse/unicodedata ok; base64, zlib → `ImportError: libz.so.1`; ssl →
   `ImportError: libssl.so.3`. A conforming tool importing base64 failed every clause → false
   TARGET_MISSED. Reported to ExecCounterC1 with the receipt; the fix (ldd over the interpreter AND every
   lib-dynload .so, SONAME path + realpath bound, Setup error if the closure names libxkbcommon/xkbcli)
   landed in 1a7fcc21… and my full pair matrix re-ran green against it.
2. **No unexploitable weakening.** Every one of the five clauses (and the rev-addressing half of t) has
   an exploit that flips the verdict when and only when that clause is weakened. The counter's clause
   set is load-bearing as written.
3. **Declared limit of this audit (not a defect):** the exploit tools are table tools keyed on
   `(sha256(keymap bytes), arg)`; they pass g only for the nonce they were built for. A tool that
   precomputed the FULL reachable (RMLVO, arg) space would pass g for any nonce — the generated pool is
   finite and frozen in the counter source (62 layout pairs × 15 options × ~12.8k arg forms ≈ 12M pairs;
   the numeric ranges are dense and algorithmically computable). The docstring already names the
   "cached table" control; the freeze may want the g pool to include at least one input outside any
   table a tool could plausibly embed (e.g. draw ARG values outside the frozen pools, or hash the nonce
   into the RMLVO), or accept the residual explicitly. [INFERENCE on cost, not measured: I did not build
   the full-space table.]

## Artifacts (this seat dir)

- `c1r49-pristine.py` (sha 1a7fcc21…, byte-identical to the draft at copy time) and mutants
  `c1r49-mut-{t,t2,s,f,g,r1,r2}.py` (shas in `receipt-shasums.txt`)
- `receipt-run2-*.txt` — the authoritative pair matrix on 1a7fcc21… (13 runs, full counter stdout)
- `receipt-run1-*.txt` — the same pairs on the superseded base 3a9e46a9…
- `receipt-sandbox-imports.txt` — the import-closure probe (finding 1)
- `receipt-shasums.txt` — hash ledger: counter versions, mutants, exploit tools, answer table, fixture
  repo commits, pinned judge components
- repro assets: `build-table.py`, `gen-tools.py`, `table.json`, `x-t-clean.py` (the generator rebuilds
  all six exploit tools from the table; paths inside are scratch paths, adjust on reuse)
- `c1-r49-fixtures.json` — copy of the installed fixture file (sha matches the counter's pin)

Scratch `/fast/scratch/hyaku/mado-r49/MutCounterC1Draft/` deleted (12 MB freed). No tool installs were
needed (bwrap/strace/git/python3 already present; nothing added to PATH, nothing recorded for the
tool ledger).
