RECHECK 311: agree

# Independent C2 recheck — `SCORECARD.md:311`

## Base and frozen rule

I cloned the lane repository into `/fast/scratch/hyaku/mado-r25a3/res/RcMutationRegression311/clone` with `GIT_DIR`, `GIT_WORK_TREE`, and `GIT_INDEX_FILE` unset, then checked out detached `41cc04c8d593837a0d5078bffaacdaa163d12897`. The gate matched the cited base bytes: `tools/mado-verify.sh` SHA-256 `050efc720599345a73bdce6c1d13d50eadeee9769c2ece02462223d0156703f1` (4,194 lines, 208,124 bytes). The consumed harness was SHA-256 `a7d3f2dd7d47511a4769aab610dd85d1a37e77b32f14fd763f3af638dd912eb9`; the round-24 manifest was SHA-256 `e02c76d1adb4f523fccf11e1e5ad4cd40f6d0da460b75c7f811b66306e188a02`.

The manifest entry `mutation regression with re-cut` specifies `bash {TREE}/tools/mado-verify.sh --regression`, the harness environment variable, timeout 600, exit 0, and at least one `MADO_REGRESSION: PASS (case=mado-verify-hardened; ...)` line. At base, the gate pins `367ff5ec9613701a6bbd90979edcfdd229d9440b824f7edc0a4bfd8d8b784f9e` and records D1–D9/R1 as KILLED.

## Fresh primary run

From the clone, I ran the required command with the assigned limits:

```sh
timeout 900 prlimit --as=4000000000 -- env \
  MADO_VERIFY_HARNESS=/home/vgpnk/Projects/shokunin/tameshi-shokunin/tools/mutate-and-run.sh \
  bash tools/mado-verify.sh --regression
```

Observed exit: **0** (wall time 128.56 s). Key output:

```text
REGRESSION_TARGET: ... sha256=367ff5ec9613701a6bbd90979edcfdd229d9440b824f7edc0a4bfd8d8b784f9e (recorded pin ...; match=yes)
REGRESSION_SWEEP mado-verify-hardened: MUTATE: DONE (... defects=10 killed=10 survived=0 inconclusive=0 kill-rate=100%)
REGRESSION_TABLE mado-verify-hardened: match=10/10 recorded-killed=10 measured-killed=10 survived=0 inconclusive=0 flips=0
REGRESSION_CASE mado-verify-hardened: PASS (recorded table reproduced: killed=10/10 flips=0 inconclusive=0 control=green restore=ok)
MADO_REGRESSION: PASS (case=mado-verify-hardened; target=367ff5ec9613701a6bbd90979edcfdd229d9440b824f7edc0a4bfd8d8b784f9e)
EXIT=0
```

## SETUP and printed re-cut clause

To recheck the second clause, I copied the gate to a scratch `moved-gate/moved.sh` and changed only the last hex digit of `PIN_MADO` (`…f9e` to `…f9d`). The copy SHA-256 was `3b532c53d739212a5bab305bfd948a6f367bd9c8204e0db7994e0fee7c980016`. Running it with the same harness and resource limits returned **exit 2**. It derived target `367ff5ec…f9e`, reported recorded pin `…f9d` and `match=no`, printed `REGRESSION_RECUT`, and ended:

```text
MADO_REGRESSION: SETUP (target pin mismatch — the gate moved outside the MADO-R7 blocks; re-cut, then update PIN_MADO/TABLE_MADO)
REGRESSION_WORKDIR: /tmp/mado-verify-regression.TuhUQn (kept)
EXIT=2
```

I ran the printed command's exact harness arguments under the same 900-second/4-GB limits. It returned **exit 0** (wall time 117.19 s): control GREEN with 355/355 self-test assertions; D1–D9 and R1 all KILLED; 10 killed, 0 survived, 0 inconclusive; `MUTATE_RESTORE: OK` with before, after, and pristine target SHA all `367ff5ec…f9e`; kill rate 100%.

## Comparison and governing pointers

- The a3w1 report's §6 ledger line says the primary run passes 10/10 at `367ff5ec…f9e`, and the pin-flipped copy returns SETUP 2 before its printed re-cut returns 10/10 with exit 0. My independent primary, SETUP, and re-cut observations agree on status, exit codes, target pin, and kill/restore results.
- The appended `## Current state (round 25)` ledger row keyed by base row `:311` likewise says PASS/10-of-10/exit 0, followed by pin-flipped SETUP exit 2 and printed re-cut 10/10 exit 0. It points to itself and round-24 row `:1578`; no discrepancy found.
- At the base blob, `SCORECARD.md:1578` says the same capability worked at `8e5d9369`. I independently confirmed `8e5d9369` is an ancestor of `41cc04c8`. `:1222` records the later `367ff5ec…` pin and gate `050efc72…`, both matching this run. The row's round-12 evidence refers to the then-current older `538d178b…` pin; the fresh run confirms the updated pin rather than relying on that historical pointer.
- The report's scope pointer `:1588-1596` matches the base text: the frozen round-24 C2 population is the 12 heading-scoped capability rows. `:1606` records 0/12 mismatches for that C2 calibration. These are scope/status context, not contrary claims about row 311.

The SETUP experiment changed only the pin, not substantive gate behavior; it rechecks refusal and the printed-command mechanics, not a future re-cut after a substantive gate edit. This has the same limitation disclosed in the a3w1 report.

## Receipts and cleanup

My receipts remain under `/fast/scratch/hyaku/mado-r25a3/res/RcMutationRegression311/`:

- `primary.out` SHA-256 `860125615736b05adf2c935415c356eff69304c5197bc4fddc14c0b7ce3262a6`
- `setup.out` SHA-256 `c24949575d80a496497de587c5c1a619aef9c751ff7cf9b15440e225fe963072`
- `recut.out` SHA-256 `bf8bf111d377cdaaa588dcc95bcd20f83723824bb1f0eca56714b803f7963333`

Deleted my clone, moved-gate copy, SETUP workdir, and the ten `/tmp/w5-mado-m52-selftest.*` fixture directories named by my re-cut output. No tools were installed or upgraded.
