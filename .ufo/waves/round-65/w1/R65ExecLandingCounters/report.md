# R65ExecLandingCounters — quality/landing-counters.sh (mado C2, seat draft)

Seat: `R65ExecLandingCounters` · lane `mado-shokunin` @ `cb63ab13ccaf85191318701d5db5ace050bd5bd4`
Frozen contract read first: `.ufo/waves/round-65/claims-declaration-r65.md` (C2 + instrument policy),
plus each sibling's `--help` (`c3-r56-used-by.py`, `check-tool-ledger.py`, `mado-receipt-citecheck.py`).

Deliverable (draft only — nothing written into `quality/`): `landing-counters.sh` in this seat dir.

    sha256  c12b72e20cfaeb92e7ff242b26f2a26eecd6184610e78287fb7b326a30fd5e9a  landing-counters.sh
    220 lines, mode 755

Evidence files in this seat dir: `evidence-selftest.out`, `evidence-landing-at-cb63.out`,
`evidence-simulated-landing.out`, `evidence-simulated-selftest.out`.

## What the script is

Four legs, each producer's own rc printed on its own `LANDING_LEG <name> rc=<n>` line (QUALITY 26),
then one verdict line and an rc computed from the four rcs:

1. **nav** — the SCORECARD `### Counting command` python body as an inline `python3` heredoc.
   Verified byte-identical: `sed -n '71,88p' SCORECARD.md` vs the heredoc body in the script,
   `diff -u` → rc 0 (no output). The body runs in a subshell that `cd`s to `--repo` (the body
   addresses git through cwd; `--rev` is passed as `REV`). It writes nothing.
2. **usedby** — `python3 "$SELF_DIR/../quality/counters/c3-r56-used-by.py" --repo "$REPO_ABS"
   --rev "$REV" --work "$SCRATCH_ABS/ub"`.
3. **ledger** — `python3 "$SELF_DIR/../quality/check-tool-ledger.py" --repo "$REPO_ABS" --rev "$REV"`.
4. **citecheck** — `python3 "$SELF_DIR/../tools/mado-receipt-citecheck.py" --repo "$REPO_ABS"
   --rev "$REV" --paths "$REPO_ABS/.ufo/waves/round-65/receipts"` (`--citecheck-paths PATH ...`
   overrides the path list; verified live, see below).

`SELF_DIR` is `$(cd "$(dirname "$(readlink -f "$0")")" && pwd)` — siblings are never resolved from cwd.
Summary: `MADO_LANDING_COUNTERS: GREEN|RED (nav=<rc> usedby=<rc> ledger=<rc> citecheck=<rc> rev=<REV>)`;
exit 0 iff all four rc=0, else 1. No `mktemp` (scratch-root only), no network, no sleeps,
scratch-root refusals (absent / `/tmp`-family / `/var/tmp`-family / symlink / unresolvable-to-tmp)
are one stderr line + exit 2 before anything is created.

## Commands and rcs (every number below is a producer rc)

| command | rc |
|---|---|
| `bash -n .ufo/waves/round-65/w1/R65ExecLandingCounters/landing-counters.sh` | 0 |
| `bash <draft> --selftest --scratch-root /fast/scratch/hyaku/mado-r65/w1/R65ExecLandingCounters/stF` | 0 (19/19) |
| `bash <extracted>/quality/landing-counters.sh --repo <lane> --rev cb63ab13… --scratch-root …/runF2` | 1 (expected pre-landing: citecheck cannot see the uncommitted instrument) |
| same, `--citecheck-paths <lane>/corpus/knowledge/request-socket-live-bound-r8.md` | 0 — `MADO_LANDING_COUNTERS: GREEN …`, 0.39 s |
| **simulated landing** (scratch clone @ cb63 + one commit adding this script, rev `aab42ecc…`), selftest then landing | selftest 0, landing **0 — GREEN, all four legs 0** |
| `--scratch-root /var/tmp/x-r65` | 2 (`must not be under /tmp or /var/tmp`), path not created |
| `--scratch-root …/notadir/sub` (parent is a file) | 2 (`does not exist and could not be created`) |
| `--selftest` without `--scratch-root` | 2 (`--scratch-root DIR is required`) |
| `--bogus` | 2 (`unknown argument: --bogus`) |

### Selftest output (verbatim, final bytes)

```
SELFTEST ok 1: a1 missing --rev refused (got=2)
SELFTEST ok 2: a2 scratch-root under /tmp refused (got=2)
SELFTEST ok 3: a2 nothing created under /tmp
SELFTEST ok 4: a3 symlinked scratch-root refused (got=2)
SELFTEST ok 5: a4 fixture git repo created (got=0)
SELFTEST ok 6: a5 fixture toplevel verified before commit (got=/fast/scratch/hyaku/mado-r65/w1/R65ExecLandingCounters/stF/selftest.314561/fixture)
SELFTEST ok 7: a6 fixture commit created (97390f39c003)
SELFTEST ok 8: a7 leg nav ran (rc captured)
SELFTEST ok 9: a7 leg usedby ran (rc captured)
SELFTEST ok 10: a7 leg ledger ran (rc captured)
SELFTEST ok 11: a7 leg citecheck ran (rc captured)
SELFTEST ok 12: a8 summary line carries all four rcs and the rev
SELFTEST ok 13: a9 fixture landing run exits 1 when a leg is red (got=1)
SELFTEST ok 14: a10 all four rc=0 yields GREEN
SELFTEST ok 15: a11 all four rc=0 exits 0 (got=0)
SELFTEST ok 16: a12 verdict arithmetic RED on mixed rcs (got=RED)
SELFTEST ok 17: a13 exit arithmetic 1 on mixed rcs (got=1)
SELFTEST ok 18: a14 exit-path child selftest rc (got=0)
SELFTEST ok 19: a15 selftest scratch removed on exit
MADO_LANDING_COUNTERS_SELFTEST: 19/19 assertions passed
```

stderr 0 bytes; scratch root left empty (`find <stF> -mindepth 1 | wc -l` → 0); runtime 0.07 s.
Fixture rule honoured: `git -C "$D"` on every git call, `git -C "$D" rev-parse --show-toplevel`
compared to `$(cd "$D" && pwd -P)` **before** the commit (a5). All-green is proved two ways: a
stubbed `python3` on `PATH` (a10/a11, end-to-end through the summary) and the verdict functions
directly (a12/a13). Cleanup is proved from a bounded child invocation of `--selftest` (a14/a15) —
that child mode is internal (`MADO_LANDING_SELFTEST_CHILD=1`), not a CLI surface.

### Landing run against the real lane at cb63 (final bytes)

```
revision=cb63ab13ccaf85191318701d5db5ace050bd5bd4 indexed=78/78 missing=0 dangling=0 duplicates=0 coverage=10.0000/10
LANDING_LEG nav rc=0
MADO_USED_BY: rev=cb63ab13… entries=78 rows=371 missing=0 extra=0 dangling=0 conflict=0 stale=0 lost=0 exempt=24 verdict=TARGET_MET missed=none
LANDING_LEG usedby rc=0
LEDGER: population=104 ledger_rows=104 uncovered=0 dangling=0 bad_pointer=0 empty_desc=0 verdict=TARGET_MET rev=cb63ab13…
LANDING_LEG ledger rc=0
MADO_CITECHECK: rev=cb63ab13… files=6 citations=10 resolved=9 missing=1 skipped_large=0 verdict=TARGET_MISSED (VERSION r64-v1)
LANDING_LEG citecheck rc=1
MADO_LANDING_COUNTERS: RED (nav=0 usedby=0 ledger=0 citecheck=1 rev=cb63ab13ccaf85191318701d5db5ace050bd5bd4)
```

rc 1, the only miss being `quality/landing-counters.sh` itself — the file the landing adds
(two receipts cite it). stderr 0 bytes; the sole scratch write is `runF2/ub`, the used-by work dir.

### Simulated landing (end-to-end C2 reachability)

Scratch clone `git clone --shared --no-checkout` of the lane (toplevel asserted), tree of `cb63ab13…`
+ `quality/landing-counters.sh` (these bytes, mode 100755) → commit `aab42ecc41b189d12c9fcfc226579dcb415dae01`
(`diff-tree --name-status cb63ab13 aab42ecc` → `A quality/landing-counters.sh`, nothing else).
Deps + instrument re-extracted at that rev into scratch `wt/`, then:

```
SIM selftest rc=0 → MADO_LANDING_COUNTERS_SELFTEST: 19/19 assertions passed
revision=aab42ecc… indexed=78/78 missing=0 dangling=0 duplicates=0 coverage=10.0000/10      → LANDING_LEG nav rc=0
MADO_USED_BY: … verdict=TARGET_MET                                                         → LANDING_LEG usedby rc=0
LEDGER: population=104 ledger_rows=104 … verdict=TARGET_MET                                → LANDING_LEG ledger rc=0
MADO_CITECHECK: rev=aab42ecc… files=6 citations=10 resolved=10 missing=0 verdict=TARGET_MET → LANDING_LEG citecheck rc=0
MADO_LANDING_COUNTERS: GREEN (nav=0 usedby=0 ledger=0 citecheck=0 rev=aab42ecc41b189d12c9fcfc226579dcb415dae01)
```

rc 0. Also cross-checked the file set the sibling counter `R65ExecC2Counter/c2-r65-landing-instrument.py`
extracts (`REQUIRED` = instrument, `quality/check-tool-ledger.py`, `quality/counters/c3-r56-used-by.py`,
`tools/mado-receipt-citecheck.py`): all three sibling paths resolve from `$SELF_DIR/../…` when the
instrument sits at `<wt>/quality/landing-counters.sh`, so that counter's extraction layout works.

## DEVIATION / implementation-note lines (for L1 + critic)

- DEVIATION(none-behavioural) **path normalization**: `--repo` and `--scratch-root` are resolved to
  absolute paths once (`REPO_ABS`, `SCRATCH_ABS`); the nav leg `cd`s to `REPO_ABS` (the SCORECARD body
  addresses git through cwd), and the other legs get the absolute paths. When the caller passes
  absolute paths (the C2 counter does) the leg commands are byte-identical to the frozen text.
- DEVIATION(additive) `--rev` starting with `-` is refused (arg-injection guard), `--repo` must be a
  directory (else the legs fail obscurely), `-h|--help` exits 0, unknown argument exits 2. None of
  these touches the four legs, the summary format or the rc arithmetic.
- DEVIATION(additive, selftest-only) `MADO_LANDING_SELFTEST_CHILD=1` runs only the scratch-setup +
  EXIT-trap path, so a15 can observe the cleanup of a real child process. Not a CLI surface.
- DEVIATION(counting) 19 assertions instead of the ten minimum labels: a4 split into repo-created /
  toplevel-verified, a5–a8 spelled out as four per-leg assertions, plus a9 (fixture exit rc=1),
  a10/a11 (stub all-green → GREEN and rc 0), a12/a13 (verdict/exit arithmetic), a14/a15 (exit-path
  cleanup). Predicates unchanged.
- No `mktemp` is used at all (the strongest reading of "prefer none"); `TMPDIR` is therefore never
  consumed. No tool installs, no pacman, no network, no host-state writes.

## Findings / risks

1. **citecheck's inputs are filesystem bytes, its resolution is git bytes.** `mado-receipt-citecheck.py`
   walks the `--paths` given (`collect_files`/`os.walk`) and resolves against
   `git -C repo ls-tree -r --name-only <rev>`. Consequence: run against a worktree-less clone the leg
   scans `files=0` and returns `TARGET_MET` *vacuously* (observed during the first simulation, before
   the receipts were placed in the clone's worktree; `files=6` after). The C2 counter passes the real
   lane repo, so the frozen invocation is correct, and the frozen arithmetic is left untouched — but a
   future caller that extracts to a bare clone would get a silent pass. Not defended in-script on
   purpose: changing it would alter the frozen `all four rc=0 → GREEN` predicate.
2. **Pre-landing expectation is RED by exactly one leg.** At any rev without the instrument,
   citecheck reports `missing=1` for `quality/landing-counters.sh` (both `before-state-r65.txt` and
   `control-c1-c2-base-r65.txt` cite it). So the C2 before-state stays `TARGET_MISSED`, and the
   instrument turns GREEN only once these bytes are committed.
3. **Defect found and fixed in this seat's own draft** (disclosed for the mistake ledger): the first
   EXIT trap was `trap 'rm -rf -- "$SW"' EXIT` with `SW` a function-`local`; at exit the variable is
   gone and `set -u` aborted the trap (`SW: unbound variable`) leaving the scratch tree behind.
   a15 caught it (18/19); fixed by `SELFTEST_WORK="$SCRATCH_ABS/selftest.$$"` as a global read by the
   trap. Re-run 19/19, scratch empty. Lesson shape: a trap must not close over a function-local.
4. Sibling instruments at cb63 all green on the lane: nav 78/78, used-by `entries=78 rows=371
   TARGET_MET`, ledger `population=104 ledger_rows=104 TARGET_MET` — the four legs are measurable at
   the frozen base without any extra scope.
5. Runtime bounded: selftest 0.07 s, landing 0.37–0.39 s; four counter children per landing run, none
   in the selftest beyond fixture git and the two bounded self-invocations.

## Bounds honoured

Only `landing-counters.sh`, `report.md` and the four `evidence-*.out` files were written, all inside
this seat dir; `quality/**`, `tools/**`, `PROVINCE.md`, `SCORECARD.md`, `LOG.md`, `corpus/**` untouched
(no mutating git command anywhere; the only commits are inside `/fast/scratch/.../laneclone`).
All scratch (`st`, `stF`, `run*`, `extract`, `laneclone`, `simwork*`, timing dirs) lived under
`/fast/scratch/hyaku/mado-r65/w1/R65ExecLandingCounters/` and was removed before yield. No r56-era
material opened, no credential-shaped output produced, no config tree or CLI-session state touched.
