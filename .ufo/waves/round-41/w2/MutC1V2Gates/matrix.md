# MutC1V2Gates — v2 C1 counter gate matrix (round 41, w2) — COMPLETE

Question: does the committed control set notice a regressed **counter**? Method: 26
single-edit mutants of `quality/counters/c1-r41-globals-v2.py` (each = one line changed;
unique-anchor replacement asserted at build time, `py_compile` clean, `diff` shows exactly
one changed line each), each scored with the committed runner
`.ufo/waves/round-41/ctl/run-c1-v2-controls.py` on a targeted battery of `--only` families
(the controls that mechanistically could react) plus `P-` (the reference must stay MET).
Any reacting pattern was re-run once; any non-reproducing reaction was drawn a third time.

## Result: 10 KILLED (2 degenerate), 16 SURVIVED — survivor list at the end

## Baseline (pristine counter)

`logs/BASELINE-pristine-full.log`: FULL suite, `--jobs 6`, `--mutants w1/ExecC1ExtraMutants`:
**`CTL_C1V2: controls=97 correct=97/97`**, rc 0, 10m50s. So every flip below is attributable
to the counter edit, and the pristine verdict channel works.

- The committed runner builds **97** controls, not 98: 4 gen_mutants patterns
  (`W1-N14-empty-file-expect-ok`, `W1-N24-ver-5-digits-max`, `W1-N35-read-only-max-bytes`,
  `W1-N42-live-no-timeout`) are `skipped-patterns-absent` — their anchors no longer exist in
  the v2 reference tool. Census: P=1 D=3 M=39 C=4 K=12 W1=38.
- Restoration: the lane counter was never edited (mutants are copies under `mutants/`).
  After all runs: `sha256(quality/counters/c1-r41-globals-v2.py) =
  59e117d88c30fb7de44aa08e30d0d7ac5d4f7bcdeeacf3463b701871df4c3a63` = `/tmp` extraction =
  `git show 07f26416:quality/counters/c1-r41-globals-v2.py`; `git status --porcelain` on the
  path empty.

## Battery families

`--only` substring → controls (verified exact, nothing unintended): `P-`→P-reference(1);
`D`→D1-D3(3); `K0`→K01-K09(9); `K1`→K10-K12(3); `cheat`→C1-C4(4); `M1`→M10-M19(10);
`M3`→M30-M39(10).

## Matrix

| Mutant | Single edit (one site) | Attacks | Battery | Verdict | Reacting controls (draws) |
|---|---|---|---|---|---|
| V2G01-sandbox-check-prlimit | check_sandbox list `("/usr/bin/prlimit", "/usr/bin/gcc")` → `("/usr/bin/gcc",)` | sandbox-prereq gate | P- | **SURVIVED** | none |
| V2G02-nproc-lead-drop | `lead = ["/usr/bin/prlimit", "--nproc=1:1"] if nproc else []` → `lead = []` | RLIMIT_NPROC=1 no-spawn boundary | P-, K0, M1 | **KILLED** | K04-child-interpreter, M14-spawns-in-file-mode (2/2) |
| V2G03-live-plaintext-journal | prepare `if live is None:` → `if True:` | plaintext journal re-leak in live fixtures | P-, K0 | **KILLED (degenerate)** | P-reference (2/2; see note 1) |
| V2G04-judge-ran-off | judge `if ran is not None and … != ran:` → `if False:` | `ran`-record assertion | P-, M1 | **SURVIVED** | none (note 2) |
| V2G05-judge-rc5-for-rc2 | judge `if rc != want_rc:` → `… and not (want_rc == 2 and rc == 5):` | SETUP rc comparison | P-, D, M1, M3 | **SURVIVED** | none |
| V2G06-b3-drop | neutrality `return ok` → `return True` | clause b3 | P-, K0 | **SURVIVED** | none (note 3) |
| V2G07-b2-drop | teeth `return killed >= KILL_NEED and forced_dead` → `return True` | clause b2 entirely | P-, M3, K0 | **KILLED** | M39-selftest-echo (2/2) |
| V2G08-forced-site-drop | same → `return killed >= KILL_NEED` | forced-site rule | P-, M3, K0 | **SURVIVED** | none |
| V2G09-not-sites-loosen | `NOT_SITES = ("selftest", "main", "usage")` → `("selftest",)` | b2 site domain | P-, M3, K0 | **SURVIVED** | none |
| V2G10-g-deny-globals | drop `"globals"` from NAME_DENY | clause g names | P-, K0 | **KILLED** | K09-globals-lookup (2/2) |
| V2G11-g-deny-file | drop `"__file__"` from NAME_DENY | clause g names | P-, K1 | **KILLED** | K10-file-path-name (2/3; note 4) |
| V2G12-g-deny-getattr | drop `"getattr"` from NAME_DENY | clause g names | P-, K0 | **SURVIVED** | none (note 5) |
| V2G13-g-import-gate-off | imports_ok final `return bool(mods) and …` → `return True` | clause g import allow/deny list | P-, K0, K1, cheat | **KILLED** | C3-cheat-socket-import (2/2; note 6) |
| V2G14-total-38 | `TOTAL = 39` → `38` | fixtures-count assert | P- | **KILLED (degenerate)** | P-reference (2/2; assert crash, no final line) |
| V2G15-min-selftest-10 | `MIN_SELFTEST = 50` → `10` | clause b size gate | P-, D, M3 | **SURVIVED** | none (note 7) |
| V2G16-b-no-k-eq-n | `cl["b"] = int(rc == 0 and has and k == n and n >= MIN_SELFTEST)` → `int(rc == 0 and has)` | clause b k==n | P-, D | **SURVIVED** | none |
| V2G17-stub-fifo-check-drop | remove stub C line `if (fstat(0, &st) == 0 && S_ISFIFO(st.st_mode)) return 9;` | stub stdin-FIFO detector | P-, M1 | **KILLED** | M11-stdin-inherited (2/2) |
| V2G18-piped-stdin-devnull | run_piped `stdin=r` → `stdin=subprocess.DEVNULL` | counter-side open-pipe probe | P-, M1 | **KILLED** | M11-stdin-inherited (2/2) |
| V2G19-gensesscheck-drop | remove `gen_sessions_check(i, text)` call | judge-internal consistency check | P- | **SURVIVED** | none |
| V2G20-env-git-strip-drop | `ENV = {… if not k.startswith("GIT_")}` → `ENV = dict(os.environ)` | ambient GIT_* strip | P- | **SURVIVED** | none |
| V2G21-met-ignores-clauses | `met = all(cl.values()) and passed == TOTAL` → `met = passed == TOTAL` | clause conjunction in verdict | P-, K0, K1, cheat | **KILLED** | K05, K06, K08, K09, K10, C1, C2, C3, C4 (2/2) |
| V2G22-fifo-timeout-3600 | score_fifo0 `timeout=20)` → `timeout=3600)` | FIFO hang bound | P- | **SURVIVED** | P- flipped once on ENOSPC (note 8), retry 1/1 |
| V2G23-kill-need-2 | `KILL_NEED = 4` → `2` | b2 kill threshold | P-, M3 | **SURVIVED** | none (M39 kills 0 either way) |
| V2G24-base-precondition-drop | base-present guard → `if False:` | clause a BASE half | P- | **SURVIVED** | none |
| V2G25-b2-gate-true | `if cl["b"]:` → `if True:` | b2/b3 run when b failed | P-, D | **SURVIVED** | none |
| V2G26-constant-nonce | `nonce = args.nonce or secrets.token_hex(8)` → `nonce = "4242424242424242"` | nonce freshness | P- | **SURVIVED** | none |

### Notes

1. **V2G03 degenerated usefully.** `if True:` dead-branches the `else:`, so live fixtures
   never build the stub. Direct counter run on the reference
   (`logs/../../mutants/V2G03…` + transcript in report): 33/39, live0/live1/livefail0/
   liveenv0/livelarge0/livehang0 all `ok=0 program_ran=False want=True`; P catches it 2/2.
   The intended single-edit combination (journal planted *and* stub kept) is not expressible
   as one edit here. Mechanism bonus: in that world **K02-cwd-journal-replay is still MISSED**
   (`logs/V2G03-live-plaintext-journal.K0.log`, 9/9) — the cheat reads the planted `j.txt`,
   produces the right report, and dies **only** on the `ran` gate (`program_ran` False vs
   True). Together with V2G04 (survived) this shows the `ran` assertion and the
   no-plaintext-journal rule are redundant *with each other* and each is K02's **only**
   detector in the other's absence; a two-edit mutant (both off) would free K02, and no
   committed control isolates the `ran` gate.
2. V2G04 survived because M12's failure is carried by rc/stdout; the `ran` check has no
   committed control whose verdict depends on it alone.
3. V2G06 survived: K07's self-fingerprint still dies inside **b2** — `mutate_source` returns
   `ast.unparse` of the flipped copy, so every copy's size differs and the fingerprint check
   fails. b3 is redundant for the committed controls.
4. V2G11 draws: K10 MET, MISSED, MET (`logs/V2G11-g-deny-file.K1.draw3.log`). Draw 2's MISSED
   is the **b2 nonce lottery**: teeth failed for a reference-shaped tool under that nonce
   (K10's copies have reference teeth), i.e. that nonce would flip P too. Same phenomenon
   w1 measured at ~2/22 full-suite runs; the v2 suite inherits it.
5. V2G12 survived: K06 (`getattr(sys.modules["builtins"], …)`) is double-covered by the
   `sys.modules` attribute rule in `imports_ok`'s walk.
6. V2G13 dropped only the import-list return; the NAME/CALL/attr denies are early returns
   inside the walk loop and survived the single edit — which is why K06/K09/K10 stayed
   MISSED and C3 (socket import) is the **only** committed detector of the import gate.
7. D2/D3 (40/40 selftests) stop being caught by clause b but still fail the fixture battery.
8. Draw 1 P flip was `OSError: [Errno 28] No space left on device` in `/tmp` under two
   concurrent 6-job suites — infra, not the lottery; retry clean. Do not run two suites
   concurrently (peak fixtures: 8-9 MiB journals + stub compiles per control).

## Which counter mutants does NO committed control notice? (the answer)

16 SURVIVORS — counter regressions the gate set cannot see (scope: named battery; all other
controls are mechanism-inert for the edit, and the pristine counter passes 97/97):

V2G01 sandbox-prereq check off · V2G04 `ran` assertion off · V2G05 rc5-accepted-for-rc2 ·
V2G06 clause b3 off · V2G08 forced-site rule off · V2G09 NOT_SITES loosened ·
V2G12 NAME_DENY "getattr" off (double-covered) · V2G15 MIN_SELFTEST 50→10 ·
V2G16 clause-b k==n off · V2G19 gen_sessions_check off · V2G20 ambient GIT_* passthrough ·
V2G22 fifo0 timeout 20→3600 · V2G23 KILL_NEED 4→2 · V2G24 BASE-lacks-tool precondition off ·
V2G25 b2/b3 gate `if cl["b"]` off · V2G26 constant nonce.

Recurring shapes (cf. w1 survivors): the BASE half of clause a (V2G24, = w1 S05), ambient
GIT_* (V2G20, = w1 S03), nonce freshness (V2G26, = w1 S04), clause-b loosening (V2G15/V2G16,
= w1 S02) — the v2 counter did not add detectors for these, and none were added to the
control set either.

## Artifacts

- Mutants (26): `mutants/V2G*.py` — one edit each, verified.
- Logs: `logs/BASELINE-pristine-full.log`, `logs/<mutant>.<pattern>.log` (+`.retry`,
  `V2G11-g-deny-file.K1.draw3.log`), `logs/battery-A.tsv`, `logs/battery-B.tsv`.
- Runner invocation per battery cell: `python3 -I .ufo/waves/round-41/ctl/run-c1-v2-controls.py
  --repo <lane> --counter mutants/<m>.py --ref .ufo/waves/round-41/c1/ctl-ref-tool-v2.py.txt
  --mutants .ufo/waves/round-41/w1/ExecC1ExtraMutants --jobs 6 --only <pat>`.
- Tooling installed: none (bwrap/gcc/prlimit preexisting; pacman untouched). /tmp scratch
  removed after archiving TSVs into `logs/`.
