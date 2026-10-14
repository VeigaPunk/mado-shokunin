# Gate mutation proof — mado-verify.sh hardened (M6-1, round 6)

Date 2026-10-14 (training round 6, lane M6-1). This note records the three
ordered steps of the mado round-6 plan §(a): (1) tameshi's read-only sweep of
the round-5 gate, (2) the selftest additions that kill its survivors, (3) the
re-run of the same defect spec against the hardened revision. Marks: **O** =
observation (command output, file:line, re-quoted measured cell); **I** =
inference; **U** = unknown. All runs single-host (bash 5.3.15, python 3.14.7,
Linux 7.2.3-arch1-3, 2026-10-14).

Pins at write time (O):

- Sweep note (spec source): `tameshi-shokunin/corpus/knowledge/
  mutation-case-mado-verify.md` — 323 L / 24,534 B / sha256
  `f2d53d495e6c1d8b2c18e7bc0eac54955d477455958b10866c5f8712b2086bf3`
  (uncommitted, append-only; re-pin before quoting).
- Harness: `tameshi-shokunin/tools/mutate-and-run.sh`; tameshi's sweep ran
  `597e1419…f6331b`, this lane's re-run `b56c6e57…22bcb` (the tool moved
  mid-round; each run's `MUTATE_TOOL` line is the pin it is tied to).
- Target, **before**: `tools/mado-verify.sh` `d7edaab4…d0e13`, 1,098 L,
  45,334 B, selftest 28/28.
- Target, **after**: `tools/mado-verify.sh` `c4c1afb7…a5171`, 1,186 L,
  50,126 B, selftest 53/53 — `git diff --numstat` = **+88/−0** lines; the
  diff is inside `selftest()` only (no verify-path edit).
- Suite channel (both sweeps): `bash "$MUTANT" --selftest`. The landed
  selftest invokes `$0`, so it exercises the mutant copy directly — the
  "cannot take a target path" gap named in the plan does not exist (O).
  No mutant run reads a substrate; the live plane is reached only under
  PATH-stub conditions the suite itself constructs.

## 1. Re-run — tameshi's 10-defect spec against the hardened gate (O)

Command (scratch `/tmp/w6-mado-m61/`; spec = byte copy of tameshi's
`/tmp/w6-tameshi-mado-verify/spec/mado-verify.defects.spec`, sha
`c7ee75b97c38ac8f88410165a574ad1cba7f4653bd09d35e6814267a12df1dd8`):

    bash tameshi-shokunin/tools/mutate-and-run.sh \
      --target mado-shokunin/tools/mado-verify.sh \
      --defects /tmp/w6-mado-m61/sweep/tameshi.spec \
      --suite 'bash "$MUTANT" --selftest' \
      --workdir /tmp/w6-mado-m61/sweep/work-realtameshi --label mado-verify-hardened

- Control: `CONTROL: GREEN (exit=0 …)` + `MADO_SELFTEST: 53/53 assertions
  passed` (log `/tmp/w6-mado-m61/sweep/realtameshi-sweep.log`).
- **Headline: killed 10 / survived 0 / inconclusive 0 — kill-rate 100 %**
  (same spec on the round-5 revision: 4/10, 40 %). `MUTATE_RESTORE: OK
  (target-sha256 before=c4c1afb7…a5171 after=c4c1afb7…a5171
  pristine-sha256=c4c1afb7…a5171)`. The target file was also re-hashed after
  the runs: unchanged.
- Per-defect verdicts; failing assertions verbatim from
  `work-realtameshi/evidence/<id>.out` (count = passed/failed of 53):

| # | clause | injected defect (site on d7edaab4) | verdict | failing assertions |
|---|---|---|---|---|
| D1 | A verdict token | file-plane `CLEAN` token → `OK` (`:1088`) | KILLED 52/1 | `A: CLEAN verdict` |
| D2 | B UNKNOWN arm | UNKNOWN guard dropped (`:1086`) | KILLED 47/6 | `C: exit 1` · `C: DIVERGED` · `C: no fake CLEAN` · `E ×3` (same shape) |
| D3 | B status vocabulary | skipped-live row `SKIP`→`PASS` (`:588`) | KILLED 52/1 | `A (live layer not executed) (want row live.plane SKIP)` |
| D4 | C exit map | DIVERGED path `exit 1`→`0` (`:1098-1099`) | KILLED 48/5 | `B/C/E/H/I: exit 1` (five scenarios) |
| D5 | C exit map | failing `--selftest` returns 1 not 2 (`:429`) | KILLED 52/1 | `F: failing selftest exits 2 (got '1' want '2')` |
| D6 | D census | `xdph` dropped from local inventory (`:522`) | KILLED 52/1 | `B (want row hypr.local.inventory FAIL)` |
| D7 | D census | include-graph count `-ne`→`-lt` (`:484`) | KILLED 49/4 | `H: exit 1` · `H: DIVERGED` · `H (exact census, no tolerance)` · `H: no fake CLEAN` |
| D8 | E sha comparison | sha-pin comparison always "matches" (`:574`) | KILLED 52/1 | `A: sha pin names the round-1 pin` |
| D9 | E boundary proof | boundary comparison always byte-identical (`:738`) | KILLED 49/4 | `I: exit 1` · `I: DIVERGED` · `I (safety row, FAIL direction)` · `I: no fake CLEAN` |
| R1 | F reader fallback | tomllib-unavailable arm `PASS` not `UNKNOWN` (`:651`) | KILLED 52/1 | `E (reader fallback) (want row walker.config UNKNOWN)` |

The six survivors of tameshi's sweep (D3, D5, D7, D8, D9, R1) are each killed
by a case added in this round; the four already-killed defects (D1, D2, D4,
D6) stay killed and now fire in more scenarios (D2 ×6, D4 ×5 — the new
scenarios re-detect the verdict/exit mutants, not only the original ones).

## 2. The hardening — six survivors → six cases (O/I)

All additions live inside `selftest()`; helpers `st_row_detail` (row id +
status + detail substring) and `st_counts_agree` (the report `counts:` line
must equal the row table, derived, not hardcoded). Cases E/F/H/I extend the
suite from A–D to A–D + 4; assertion count 28 → 53.

1. **D3 →** A asserts the skipped-live row: `live.plane SKIP` (a fake PASS on
   an unexecuted layer is now red the moment the row is read). The counts-line
   agreement in A/B/C/E/H/I also makes the counters a checked claim
   (row/status/counts must agree; catches counter swaps, e.g. skip/note).
2. **D8 →** A reads the `sha_pin` NOTE row: the detail must carry the
   **measured** 12-hex prefix of the fixture file and must name the round-1
   pin as drifted (a fixture can never match `4f52854a3c14`, so a
   "matches"-always mutant fails; a cut-length mutant fails on the prefix).
3. **R1 →** **scenario E**: a PATH sandbox without `python3`; the reader
   degradation arms must read `UNKNOWN` (`waybar.config.parse`,
   `walker.config`, `term.alacritty.toml`), exit 1, no fake CLEAN.
4. **D5 →** **scenario F**: the suite runs its own child in a `sha256sum`-less
   PATH (child fails on the sha/boundary asserts) and asserts the child's
   **exit 2** plus the `FAILED` line. The child carries
   `MADO_SELFTEST_NESTED=1` so the probe cannot recurse; the child's kept
   fixture is removed by exact path.
5. **D7 →** **scenario H**: clean fixture + one undeclared 18th
   `source =` line; the include-graph census must read `FAIL` and exit 1
   (exact count, no tolerance).
6. **D9 →** **scenario I**: a PATH-stub `sha256sum` whose stdin-mode output
   carries an incrementing counter, so the before/after boundary hashes
   differ mid-run; the boundary proof must read `FAIL`, exit 1, no fake CLEAN.
   (The same case incidentally kills a `cut -c1-16` truncation of the
   boundary hash — the truncated form hides the injected difference.)

## 3. Residual findings (recorded, not smoothed)

- **rc 6 arm is dead code (O).** `row_from_rc`'s `6) … UNKNOWN` arm (`:105`)
  is reachable by no check — nothing in the file exits 6 (grep count 0; same
  observation as the sweep note §3.3). A `6) UNKNOWN → PASS` mutant is an
  equivalent edit under any black-box suite; this lane's probe D05 survived
  the hardened suite for that reason. Kill requires a white-box pin or
  removing the branch — owner decision, recorded unabsorbed.
- **Exit-flatten family (I, bounded by the harness).** A mutant that flattens
  the suite's own failure exit (`return 2`→`return 0`, or `exit $?`→`exit 0`
  in main) cannot be killed by an exit-code-judged harness: the hardened
  suite runs it **red** (probe D15: `MADO_SELFTEST: FAILED — 52 passed, 1
  failed`), but the mutant's own exit is 0 by construction, so the harness
  records SURVIVED. The D5 shape (`return 2`→`return 1`) *is* killed (exit 1
  is non-zero). A future harness that also reads suite stdout would close
  this class.
- **Live-plane body still unexercised (O).** 51 of 106 row sites sit under
  `hypr-live`; the suite reaches only the two guard rows. Tameshi §8
  recommendation #1 (a PATH-stub `hyprctl` scenario) is the highest-yield
  remainder and is **not** absorbed here (it kills no swept survivor); this
  lane's probe M16 (live-branch `CLEAN` token) accordingly survives.
- **Minor residuals from this lane's own probe set** (not part of tameshi's
  spec; at the hardened revision): out-of-band usage exits `--root` without a
  value and a bad `MADO_VERIFY_LIVE` still read-through (exit 2→1 mutants
  survive; the swept exit channel D5 is covered); the version string and
  boundary-hash remaining cosmetics are unpinned. Recorded; no widening
  ships unproven.

## 4. Spot-checks (three, all re-run 2026-10-14)

1. `bash tools/mado-verify.sh --selftest` → `MADO_SELFTEST: 53/53 assertions
   passed`, rc 0 (was 28/28). Fixtures under `/tmp/w5-mado-m52-selftest.*`;
   the suite's own kept-fixture paths from this lane's failing runs were
   removed by exact path (90 paths); foreign directories left untouched.
2. Re-run of tameshi's spec → §1 table: 10/10 KILLED, control GREEN,
   `MUTATE_RESTORE: OK`, target sha `c4c1afb7…a5171` before = after.
3. End-to-end, read-only: `--no-live` → `MADO_VERIFY: CLEAN (17 pass, 2
   notes)` rc 0, `counts: pass=17 fail=0 unknown=0 skip=1 note=2`; live run →
   `MADO_VERIFY: CLEAN (35 pass, 4 notes)` rc 0, `counts: pass=35 fail=0
   unknown=0 skip=0 note=4`; `boundary.readonly` PASS both (combined sha
   `bb2639d9a980…`); the gate file sha is unchanged by the runs.

## 5. Re-pin (supersedes round-5 identities)

The round-5 record's gate identity (SKILL.md `:487`, 1,098 L /
`d7edaab4bf108625…`) and its selftest count (`:480`, 28/28) are superseded by
the hardened identity: **1,186 L · 50,126 B · sha256
`c4c1afb75dd1c8aa4d8ff9b808ddbeb2a05ac0e3ab1095dd7d067cff1a625171` ·
selftest 53/53**. Downstream stages (b)/(c) and the round-6 record should
cite this pin; no other file was edited by this lane (write scope = the gate
file plus this note).

## 6. Unknowns

- U1 — single host/toolchain; the PATH-stub mechanisms (E, F, I) may behave
  differently under other shells (suite note's U5 shape).
- U2 — harness verdict is exit-only; the flatten family (§3) is a harness
  boundary, not a suite gap (each such mutant's suite run was measured red).
- U3 — tameshi's sweep table is tied to tool `597e1419…`; this re-run to
  `b56c6e57…`. Reproducing §1 under the current tool revision was measured
  here; reproducing *tameshi's* table under it was not re-cut (their U3).
- U4 — the live plane's 51 row sites remain unmeasured; tameshi §8 #1 open.
- U5 — the sweep note itself may move (uncommitted); all citations here are
  against `f2d53d49…` at 17:58Z.
- U6 — foreign `/tmp/w5-mado-m52-selftest.*` directories (44 at cleanup
  time) belong to other writers; attribution unknown, none removed.