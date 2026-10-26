# Seat MutRefSelftest — report (mado round 43 w1, 2026-10-26)

Task: mutation-test the C1 reference tool's own selftest and fixtures
(`.ufo/waves/round-42/c1/ctl-ref-tool.py.txt`, frozen, sha256 `e3c2e471…35a99`, never modified —
re-verified byte-identical after the sweep). Full matrix + assertion list:
`.ufo/waves/round-43/w1/MutRefSelftest/matrix.md`; harness `mutate.py`, `counter_run.py` (same dir);
evidence copies under `evidence/`.

## What was done

77 single-edit mutants over all 11 functions except `selftest` (>= 40 required). Detector 1:
`python3 -I <mutant> --selftest`. Detector 2 on the 24 selftest-survivors: the frozen counter
`quality/counters/c1-r42-geometry.py --repo . --rev b2e2efd6… --tool <mutant>` with
`C1R42_TMP=/fast/scratch/hyaku/mado-r43/MutRefSelftest`. Pristine baselines: selftest 73/73 rc 0;
counter 37/37 TARGET_MET rc 0 (evidence/counter-pristine.txt).

## Findings

1. **Selftest alone kills 53/77 (69%).** Every function except `run`/`main` has selftest-killed
   mutants; 12 mutants die only by crash (uncaught exception), 3 by the `--selftest` invocation
   itself failing (A1, A3, A5, U7 — rc 2 SETUP before any assertion runs).
2. **Structural blind spot: the CLI layer.** The selftest calls `report`/`parse_args`/`read_regular`/
   `regex_ok`/`matches` in-process and never `run`/`main`, so 10 of the 24 survivors are `run`/`main`
   mutants. The counter's fixtures catch 8 of them; **U4** (strict UTF-8 decode of rules files) and
   **N1** (`except Setup` → `except Exception`) survive both detectors.
3. **Equivalent mutants (3, proofs in matrix.md):** C1 (`UnicodeDecodeError` ⊂ `ValueError`,
   `issubclass` verified), G6 (`re.I` cannot change compilability; `matches` recompiles unflagged),
   P2 (`windowrule[ \t]*=(.*)` — every prefix match is a full match; 200k-line fuzz, 0 diffs).
4. **Missing assertions (non-equivalent double-survivors):**
   - **U4**: no fixture feeds a non-UTF-8 rules file. Assertion 13 (matrix.md): rules file with a
     lone `\xff` line → pristine rc 3 `rules=1 … unsupported=0` (byte replaced, line ignored);
     mutant rc 1 traceback (evidence/u4.out vs u4.err).
   - **N1**: no fixture crashes the tool. Assertion 16: 60000-deep nested clients JSON → contract
     says `SETUP bad_json` exit 2. **The pristine reference fails this itself** (RecursionError
     traceback rc 1, evidence/n1.err) — a latent contract violation of the reference, reported, not
     scored; the mutant merely converts the crash into a differently-worded SETUP line.
   - **R5** (dropped `os.close`, fd leak): not equivalent in general, but **indistinguishable on this
     host** — verified with 2000 `--rules` files: pristine == mutant rc 3 `rules=2000` (host
     `ulimit -n` 524288; argv size caps the file count far below it). Killable only where
     RLIMIT_NOFILE ≈ 1024 (1100 files). Latent leak, declared.
5. **Counter-only kills (18)** — all fixture kills (clauses a/b/b2/b3/g stayed 1 in every run):
   boundary cases (R2, K1 ← boundary0/stdinok0), zero size (S4 ← size0/sizevals0/many0), control-char
   threshold (M4 ← ctlclass0), verdict-order E9 ← client0/gen4/gen5, tab field 0 (P13) and no-space
   `match:class` (K3) ← space0, bare `?` alphabet (G5) ← gen3/regex0, 5-digit sizes (K4) ← size0,
   FIFO blocking (R1 ← fifo0 timeout), stdin bound (U2, U3 ← stdinbig0), output/exit plumbing
   (U1 all 36, U5 34, U6 18), SETUP shape (N2, N3 ← all 6 SETUP fixtures), stdin type (N4 ← 7).

## Assertions to add to `selftest`

18-item unified-diff-free list in matrix.md (§ Assertions): 7 cheap in-process (zero size, tab class,
bare-`?` regex, 5-digit size, no-space match field, tab field 0, badsize-before-tiled), 2 SETUP-shape
checks via `main()` with patched argv/stdout, 6 needing tmp-file plumbing inside `selftest` (exact
1 MiB rules file, stdin upper bound, file-clients path, newline-separated stdout, run() exit codes,
non-UTF-8 rules file), 1 stdin.buffer check, plus 3 conditional ones (deep-nesting — only after the
pristine tool fix; many-files — only under small RLIMIT_NOFILE; FIFO — timeout-based). Adding 1-15
would leave only the three proven equivalents and the environment-conditional mutants undetected by
the selftest alone.

## Bounds and cleanup

Leaf seat: no subagents, no spawning by me outside the harness's own `subprocess.run` of the tool
under test and the counter (the counter itself sandboxes every tool run in bwrap). Scratch
`/fast/scratch/hyaku/mado-r43/MutRefSelftest` (2.6 MB peak, well under 2 GB) deleted at the end; all
cited artifacts copied to `evidence/` first. No pacman use; no tool installs. Frozen instruments
untouched; no lane file outside my seat dir written.
