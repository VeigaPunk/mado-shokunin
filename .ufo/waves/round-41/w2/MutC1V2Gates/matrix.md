# MutC1V2Gates — v2 C1 counter gate matrix (round 41, w2)

Question: does the committed control set notice a regressed **counter**? Method: 26
single-edit mutants of `quality/counters/c1-r41-globals-v2.py` (each = one line changed,
verified by diff and by unique-anchor replacement at build time), each scored with the
committed runner `.ufo/waves/round-41/ctl/run-c1-v2-controls.py` on a targeted battery of
`--only` families (the controls that mechanistically could react) plus `P-` (the reference
must stay MET). Any reacting pattern is re-run once (w1 found a ~1-in-10 nonce lottery:
spurious single flips that do not reproduce).

## Baseline (pristine counter)

`logs/BASELINE-pristine-full.log`: FULL suite, `--jobs 6`, `--mutants w1/ExecC1ExtraMutants`:
**`CTL_C1V2: controls=97 correct=97/97`**, rc 0, 10m50s.
- Note: the committed runner builds **97** controls, not 98: 4 gen_mutants patterns
  (`W1-N14-empty-file-expect-ok`, `W1-N24-ver-5-digits-max`, `W1-N35-read-only-max-bytes`,
  `W1-N42-live-no-timeout`) are reported as `skipped-patterns-absent` — their anchors no
  longer exist in the v2 reference tool. Family census: P=1 D=3 M=39 C=4 K=12 W1=38.
- Pristine counter sha256 `/tmp` extraction `59e117d88c30fb7d…` (first 16); lane worktree
  file verified byte-identical to DATA commit 07f26416 blob before any run
  (`git status --porcelain` empty on the path; `diff -q` clean).

## Battery families

`--only` substring → controls: `P-`→P-reference(1); `D`→D1-D3(3); `K0`→K01-K09(9);
`K1`→K10-K12(3); `cheat`→C1-C4(4); `M1`→M10-M19(10); `M3`→M30-M39(10). Verified to match
exactly those families, nothing else.

## Matrix

Verdicts: **KILLED** = ≥1 control flips (expect≠got) and reproduces on retry;
**SURVIVED** = no reaction anywhere in the battery (P- stays MET) — a coverage finding:
no committed control notices this counter regression. Scope of every SURVIVED claim is the
named battery (families whose mechanism the mutation touches); families outside it are
mechanistically inert for that edit (argument in the table).

| Mutant | Single edit (old → new, one site) | Attacks | Battery | Verdict | Reacting controls |
|---|---|---|---|---|---|
| V2G01-sandbox-check-prlimit | `("/usr/bin/prlimit", "/usr/bin/gcc")` → `("/usr/bin/gcc",)` in check_sandbox | env gate: sandbox prereq no longer verified | P- | (pending) | |
| V2G02-nproc-lead-drop | `lead = ["/usr/bin/prlimit", "--nproc=1:1"] if nproc else []` → `lead = []` | RLIMIT_NPROC=1 boundary for file mode (no-spawn rule) | P-, K0, M1 | (pending) | |
| V2G03-live-plaintext-journal | `if live is None:` → `if True:` in prepare | live fixtures re-leak the journal plaintext (v1 K02 hole) | P-, K0 | (pending) | |
| V2G04-judge-ran-off | `if ran is not None and os.path.exists(...ran) != ran:` → `if False:` | ran-record assertion in judge | P-, M1 | (pending) | |
| V2G05-judge-rc5-for-rc2 | `if rc != want_rc:` → `if rc != want_rc and not (want_rc == 2 and rc == 5):` | SETUP rc comparison loosened | P-, D, M1, M3 | (pending) | |
| V2G06-b3-drop | neutrality `return ok` → `return True` | clause b3 neutral-edit check | P-, K0 | (pending) | |
| V2G07-b2-drop | teeth `return killed >= KILL_NEED and forced_dead` → `return True` | clause b2 entirely | P-, M3, K0 | (pending) | |
| V2G08-forced-site-drop | same → `return killed >= KILL_NEED` | forced-site rule (summary function must be covered) | P-, M3, K0 | (pending) | |
| V2G09-not-sites-loosen | `NOT_SITES = ("selftest", "main", "usage")` → `("selftest",)` | site-exclusion domain of b2 | P-, M3, K0 | (pending) | |
| V2G10-g-deny-globals | drop `"globals"` from NAME_DENY | clause g name denylist | P-, K0 | (pending) | |
| V2G11-g-deny-file | drop `"__file__"` from NAME_DENY | clause g name denylist | P-, K1 | (pending) | |
| V2G12-g-deny-getattr | drop `"getattr"` from NAME_DENY | clause g name denylist (K06 double coverage?) | P-, K0 | (pending) | |
| V2G13-g-drop | imports_ok `return bool(mods) and ...` → `return True` | clause g entirely | P-, K0, K1, cheat | (pending) | |
| V2G14-total-38 | `TOTAL = 39` → `38` | fixtures-count assertion (degenerate: counter crashes) | P- | (pending) | |
| V2G15-min-selftest-10 | `MIN_SELFTEST = 50` → `10` | clause b size gate | P-, D, M3 | (pending) | |
| V2G16-b-no-k-eq-n | `cl["b"] = int(rc == 0 and has and k == n and n >= MIN_SELFTEST)` → `int(rc == 0 and has)` | clause b k==n gate | P-, D | (pending) | |
| V2G17-stub-fifo-check-drop | remove stub C line `if (fstat(0, &st) == 0 && S_ISFIFO(st.st_mode)) return 9;` | stub stdin-FIFO detector | P-, M1 | (pending) | |
| V2G18-piped-stdin-devnull | run_piped `stdin=r` → `stdin=subprocess.DEVNULL` | counter-side open-pipe probe | P-, M1 | (pending) | |
| V2G19-gensesscheck-drop | remove `gen_sessions_check(i, text)` call | judge-internal consistency check | P- | (pending) | |
| V2G20-env-git-strip-drop | `ENV = {… if not k.startswith("GIT_")}` → `ENV = dict(os.environ)` | ambient GIT_* strip | P- | (pending) | |
| V2G21-met-ignores-clauses | `met = all(cl.values()) and passed == TOTAL` → `met = passed == TOTAL` | clause conjunction in verdict | P-, K0, K1, cheat | (pending) | |
| V2G22-fifo-timeout-3600 | score_fifo0 `timeout=20)` → `timeout=3600)` | FIFO hang bound (v1 hang regression) | P- | (pending) | |
| V2G23-kill-need-2 | `KILL_NEED = 4` → `2` | b2 kill threshold | P-, M3 | (pending) | |
| V2G24-base-precondition-drop | base-present `if git(...)` guard → `if False:` | clause a BASE half | P- | (pending) | |
| V2G25-b2-gate-true | `if cl["b"]:` → `if True:` | b2/b3 run even when b failed | P-, D | (pending) | |
| V2G26-constant-nonce | `nonce = args.nonce or secrets.token_hex(8)` → `nonce = "4242424242424242"` | nonce freshness | P- | (pending) | |

## Raw evidence

- Battery logs: `logs/<mutant>.<pattern>.log` (+ `.retry` where a reaction was seen).
- TSV digests: `/tmp/v2g-results-A.tsv`, `/tmp/v2g-results-B.tsv` (copied below when runs land).
