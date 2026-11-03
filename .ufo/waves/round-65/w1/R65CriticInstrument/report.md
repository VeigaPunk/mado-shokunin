# R65CriticInstrument — adversarial review of mado C2 instrument drafts

Scope: findings only. No rewrites. Drafts attacked: `R65ExecLandingCounters/landing-counters.sh` and `R65ExecC2Counter/c2-r65-landing-instrument.py`, against the frozen C2 policy in `.ufo/waves/round-65/claims-declaration-r65.md`. Lane HEAD `cb63ab13ccaf85191318701d5db5ace050bd5bd4`.

**Draft drift during review.** Both drafts changed on disk while I worked. First read: landing `42f620f1…`, driver `c7bb961f…`. Final bytes: landing `c12b72e2…` (9904 B), driver `b8658db6…`. Every BLOCKER and the cited SHOULD-FIX items were re-run against the final bytes. Line numbers below are from the final bytes.

**Trailer-path note.** The orchestrator trailer names `.ufo/waves/round-65/w1/R65CriticInstrument.md`, outside this seat dir. Write scope is the seat dir only, so the identical copy is `R65CriticInstrument/R65CriticInstrument.md`. The orchestrator should collect from there.

## Verdict per frozen policy line

| Policy line | Result | Basis |
|---|---|---|
| C1 scratch refusal, `/tmp`, `/tmp/`, `/var/tmp`, symlink→/tmp | PASS (rc=2, nothing created) | landing + driver probes below |
| C1 symlink root, trailing slash, non-tmp target | FAIL (S1) | landing rc=0, driver proceeds |
| C1 relative root / `/dev/shm` | NOTE (N4, N5) | accepted, spec silent |
| C2 per-leg rc captured and printed | PASS (landing); NOTE (driver) | `LANDING_LEG <leg> rc=N` lines |
| C2 citecheck leg is green on nothing | FAIL (B2) | rc=0, `files=0 citations=0 verdict=TARGET_MET` |
| C2 summary separates red from crash | FAIL (S5) | base run: 3 legs rc=2, summary exit 1 |
| C3 script-relative resolution | PASS at `quality/`; fragile (N2) | symlink, other-cwd, relative invoke all rc=0 |
| C4 hermetic, writes only under scratch | FAIL (B4, S3) | ambient GIT_DIR steers legs; host hook writes |
| C5 determinism | NOTE (N1) | counts 19/19 both runs; stdout differs on one line |
| C6 extraction list complete | PASS for the four legs; BLOCKER (B3) at integration | see below |
| C7 `/tmp` hardcode / writes outside scratch | PASS (N3) | grep + probes |

## Ranked defects

### BLOCKER

**B1. The citecheck leg reads the working tree, not committed bytes.**
- Draft: `landing-counters.sh:60-64` (`leg_citecheck`) defaults to `$REPO_ABS/.ufo/waves/round-65/receipts`. Citecheck `collect_files` (`tools/mado-receipt-citecheck.py:78-95`) does `os.walk` on disk.
- Failing case, fixture clone F3 at a committed rev, then an uncommitted receipt citing a missing path:
  `bash landing-counters.sh --repo F3 --rev $NEW --scratch-root … ` with the dirty file present gives `CITECHECK MISSING: corpus/NOPE-missing.md (from …/F3/.ufo/waves/round-65/receipts/zz-uncommitted-probe.txt)`, `LANDING_LEG citecheck rc=1`. After removing the file: `LANDING_LEG citecheck rc=0`.
- Violates the frozen C2 after-state "run from committed bytes extracted at that revision". Verdict depends on worktree state.

**B2. Citecheck leg is green on an empty evidence set.**
- `tools/mado-receipt-citecheck.py:94` turns a missing path into a note only. `:140` `return 0 if not missing else 1` ignores it.
- Failing case: `python3 tools/mado-receipt-citecheck.py --repo LANE --rev cb63ab13… --paths <nonexistent-dir>` gives `CITECHECK arg-not-found: …`, `MADO_CITECHECK: rev=… files=0 citations=0 resolved=0 missing=0 skipped_large=0 verdict=TARGET_MET`, rc=0.
- Landing `--citecheck-paths <nonexistent>` or an absent receipts dir therefore yields a citecheck leg that can pass vacuously. The frozen line "citecheck missing=0 TARGET_MET over .ufo/waves/round-65/receipts" is then meaningless.
- Note: in the draft-location run the leg reports rc=2 from the sibling path bug (N2), which masks this. Its rc=0 is shown with the citecheck tool directly.

**B3. Integration red: the instrument's own file is an uncovered ledger population path.**
- `quality/check-tool-ledger.py:78-82`: population includes `quality/counters/*.py`. The frozen counting command places the driver at `quality/counters/c2-r65-landing-instrument.py`. The frozen plan names no `quality/tool-ledger.md` row.
- Fixture landing commit `56ad1297ea430fb83b4ce61d31c6d3033dbee4d1` (lane + the two drafts, committed in scratch clone F3):
  `LEDGER-ROW reason=uncovered path=quality/counters/c2-r65-landing-instrument.py detail=no-row`, `LEDGER: population=105 ledger_rows=104 uncovered=1 … verdict=TARGET_MISSED`, `C6 ledger rc=1`.
  Driver: `MADO_R65_INSTRUMENT: selftest=0 landing=1 green=no verdict=TARGET_MISSED`.
- The landing commit must add a row. The pointer must name the basename in its bytes; `.ufo/waves/round-65/claims-declaration-r65.md` does (its frozen counting command), and the driver does not name itself (`grep -c c2-r65-landing-instrument` = 0 in the landing script).

**B4. Ambient `GIT_DIR` steers the landing legs; the driver's comment says it cannot.**
- Driver `c2-r65-landing-instrument.py:56-58` says GIT_* "must not steer object reads … the instrument children keep the caller's environment". The next line is the contradiction in practice: `run_leg` at `:113` calls `subprocess.run(argv, cwd=cwd, …)` with no `env=`, so children inherit `GIT_DIR`. Driver `git()` at `:70` strips GIT_* for its own calls only.
- Landing `leg_nav` git call at `:38` and citecheck git call inherit env too (the used-by and ledger legs whitelist env and are immune).
- Failing case, same committed rev `56ad1297…`:
  - clean: `LANDING_LEG nav rc=0`, `LANDING_LEG citecheck rc=0`.
  - `GIT_DIR=<empty repo>/.git`: `LANDING_LEG nav rc=1`, `LANDING_LEG citecheck rc=2`. Only the verdict-red from B3 hid the flip at the driver level. Once B3 is fixed, the same env turns a green rev red.
- Plausible trigger: git hooks export `GIT_DIR`.

### SHOULD-FIX

**S1. Trailing-slash symlink root accepted.**
- Landing `:190` `if [ -L "$SCRATCH" ]` and driver `:82` `os.path.islink(raw)` test the literal string. `lnk/` (a symlink to a non-tmp dir) follows the link and passes.
- Probes on final bytes: `bash landing-counters.sh --selftest --scratch-root $S/v/lnk/` → rc=0, `19/19 assertions passed`. Driver `--scratch-root $S/v/lnk/` → proceeds past refusal (rc=1 from the verdict, not 2). Without the slash both refuse (rc=2, "path is itself a symlink").
- Spec: the driver "refuses … one that is itself a symlink".

**S2. Existing citecheck tool bypasses its own /tmp refusal through a symlink.**
- `tools/mado-receipt-citecheck.py:223-224` uses `os.path.abspath`, not `realpath`.
- `--selftest --scratch-root <link→/tmp>` → rc=0 and `12/12 assertions passed`. strace: `mkdir("…/link_to_tmp/citecheck-selftest-…")` resolves into `/tmp`. Relative roots accepted (`rel-scratch` created under cwd). The harm-watch runs this selftest.

**S3. Landing selftest's fixture git inherits host config; a host hook writes outside scratch.**
- Landing fixture `git -C "$D" init` / `commit` at `:111`, `:116` with no `GIT_CONFIG_GLOBAL`/`NOSYSTEM` and no `core.hooksPath` override.
- Failing case: `HOME=<dir>` with `.gitconfig` `[core] hooksPath=<dir>/hooks` and a pre-commit that appends to a file outside scratch → `bash landing-counters.sh --selftest --scratch-root …` rc=0, marker written (`marker: ran`). Violates "writes only under its scratch root".

**S4. Host-guard assertion is advisory, not gating (not reproduced).**
- Landing `:114` `check_val "a5 fixture toplevel verified…"` only prints; `:115` `git -C "$D" add -A` and `:116` `commit` run regardless. Host guard requires the assertion before mutation. If init failed inside a scratch root nested in the lane, `add -A`/`commit` would hit an enclosing repo. Not reproduced because init does not fail here.

**S5. Red and crash are indistinguishable; selftest a9 cannot tell them apart.**
- Landing `:219` `[ "$verdict" = GREEN ]` → exit 1 for any non-green leg rc.
- Base run `bash landing-counters.sh --repo LANE --rev cb63ab13… --scratch-root …`: `LANDING_LEG usedby rc=2`, `ledger rc=2`, `citecheck rc=2` (sibling path failures) → `MADO_LANDING_COUNTERS: RED (nav=0 usedby=2 ledger=2 citecheck=2 …)`, exit 1. Identical exit to a genuine red.
- Selftest `:135` "a9 … exits 1 when a leg is red" passes on crashes.

**S6. Nav leg mis-handles non-ASCII note names (latent in this lane).**
- Landing `:38` `git ls-tree --name-only` without `-z`/`core.quotepath=off`; names with non-ASCII come back quoted and fail `.endswith(".md")`.
- Fixture note `corpus/knowledge/café.md` with a README row: `bash landing-counters.sh --repo <fx> --rev <rev> …` → `LANDING_LEG nav rc=1`, `ZeroDivisionError`. `quality/check-index.py --rev <rev> --repo <fx>` → rc=0, `indexed=1/1`.
- Lane check: `git ls-tree --name-only cb63ab13…:corpus/knowledge | grep -cP '[^ -~]|"|\\'` = 0 → latent. The nav leg is also a re-implementation, not the counter the spec names, so it can drift.

### NOTE

**N1. C5 stdout is not byte-deterministic (count is).**
- `selftest` ×2: both `19/19`, rc=0. `diff` differs on one line: `SELFTEST ok 6: a5 … (got=…/b/st1/selftest.314978/fixture)` vs `…/st2/selftest.316803/…` (`landing :114`). Also `a6` prints a commit prefix (time-dependent; equal here by chance). Drop the path from the message.

**N2. C3 script-relative resolution holds only at `quality/`.**
- `:22` `readlink -f "$0"`; `:25-27` `$SELF_DIR/../quality/…`, `$SELF_DIR/../tools/…` assume the script is one level below repo root.
- PASS at `quality/`: symlink invocation rc=0 (`19/19`), relative-path invocation, `cd /` absolute invocation rc=0.
- FAIL at draft location: `can't open file '…/R65ExecLandingCounters/../quality/counters/c3-r56-used-by.py'`, all three sibling legs rc=2. Fail-closed, but the base run looks like three crashes.

**N3. C7 `/tmp` audit: no writes outside scratch.**
- Landing `:91-94` (argv probe + read-only `[ -e /tmp/mado-r65-selftest-$$ ]`), `:190`/`:194` refusal lists. Driver `:53` refusal list. No hardcoded write to `/tmp`.

**N4. Relative scratch roots accepted; spec silent.**
- Landing `--scratch-root rel-s` rc=0, created under cwd. Driver relative → proceeds. Citecheck relative → accepted. Recommend resolving to absolute before any check, or refusing relative.

**N5. `/dev/shm` accepted by landing and driver; ledger refuses it.**
- `quality/check-tool-ledger.py:78` `REFUSED_WORK_PREFIXES = ("/tmp", "/var/tmp", "/dev/shm")`. Landing `--scratch-root /dev/shm/…` rc=0 (created). Driver `REFUSED_ROOTS` (`:53`) omits it. Inconsistent within the lane; spec says "/tmp-family".

**N6. Used-by counter has no /tmp refusal.** `quality/counters/c3-r56-used-by.py:59` `git_env(work)` and its selftest accept `--work /tmp/x` (rc=0). Not in the drafts; landing passes its own scratch. Relevant to harm-watch.

**N7. Selftest a10 tests only the aggregation.** The PATH shim replaces `python3` with `exit 0`, so all four legs (including the inline nav heredoc) pass with no output → GREEN. Proves rc plumbing, nothing about the legs.

**N8. Driver has no selftest.** Its refusal branches (S1, N4, N5) were only exercised by my probes.

**N9. C6 extraction list is complete for the four legs (PASS).**
- Landing calls: inline nav (no sibling), `c3-r56-used-by.py`, `check-tool-ledger.py`, `mado-receipt-citecheck.py`. All in `REQUIRED`. Used-by and ledger read `frozen-tables-v2.json` and `tool-ledger.md` from git objects at `--rev`, not from the extracted tree, so no hidden file dependency. The only integration red from C6 is B3, a population rule, not an extraction gap.

**N10. Per-leg rc capture.** Landing `:210-214` (`rc=$?` after `leg_$leg`, `printf 'LANDING_LEG %s rc=%d\n'`) prints every leg rc (verified). Driver prints only aggregate `selftest=<rc> landing=<rc>`; per-leg rcs survive only in the `landing.log` sidecar (`:221-226`, `:237`).

## Probes run (command → rc)
- `landing --selftest --scratch-root /tmp/x` → 2; `/tmp/x/` → 2; `/tmp/` → 2; `/var/tmp/x` → 2; no root → 2.
- `landing --selftest --scratch-root <link→/tmp>` → 2; `<link→/tmp>/` → 2; `<link→nontmp>` → 2; `<link→nontmp>/` → **0**; `rel-s` → 0; `/dev/shm/…` → 0.
- `selftest` ×2 → 0, 0; `cmp` → 1 (N1).
- Base landing `--repo LANE --rev cb63ab13…` → nav 0, usedby 2, ledger 2, citecheck 2 (N2/S5), exit 1.
- Citecheck direct, nonexistent path → 0, `TARGET_MET files=0` (B2). Citecheck `--selftest --scratch-root <link→/tmp>` → 0 (S2).
- Driver `--scratch-root /tmp/x` / `/tmp/x/` → 2; `<link→/tmp>` → 2; `<link→nontmp>/` → 1 (S1); relative → 1 (N4); no root → 2.
- Fixture landing `56ad1297…` (clone F3, toplevel asserted): driver → 1 `TARGET_MISSED` (B3); ledger → 1 uncovered py (B3); nav 0, usedby 0, citecheck 0.
- Dirty-worktree citecheck (B1) → 1; clean → 0.
- `GIT_DIR=<empty>` landing → nav 1, citecheck 2 (B4); clean → nav 0, citecheck 0.
- HOME hook selftest → 0, marker written (S3).
- Non-ASCII nav fixture: draft nav → 1 ZeroDivisionError (S6); `check-index.py` → 0, `indexed=1/1`.
- Symlink invocation of the landing script → 0 (N2, PASS). Other-cwd absolute → 0.

## Not verified
- A fully green landing at a rev where all four legs pass with no B3 row (the ledger row fix was not tested).
- Driver extraction `tar -x` edge cases (symlinks inside `REQUIRED`).
- Landing selftest a14/a15 child-exit cleanup beyond the run that passed.

## Installs / host
- No tools installed. No pacman. No ~/.local/bin writes.
- Fixture mutations were confined to scratch clone `…/R65CriticInstrument/f3` (`git rev-parse --show-toplevel` asserted before each commit). The lane was only read. `git -C LANE status --porcelain` = 7 before and after; HEAD unchanged `cb63ab13…`.
- Scratch `/fast/scratch/hyaku/mado-r65/w1/R65CriticInstrument` removed (`rm -rf` rc=0, `exists=no`). `/tmp` and `/dev/shm` residue from my probes: 0 (removed `/tmp/x`, `/dev/shm/mado-r65-critic`).
- Security: no r56-era material opened; no credential-shaped output.
