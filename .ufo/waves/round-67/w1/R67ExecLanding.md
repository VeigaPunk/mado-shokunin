# R67ExecLanding — C2 zero-citation control coverage

Axis: operability (C2). Claim: C2, control Z only. L1 integrates; nothing in the lane was cut over here.

- Lane tip while working: `ac376ef3fbf12d606f04dcd1e2be35312887d219`
- Instrument bytes unchanged since base: `git diff --stat 0b28ffb4 HEAD -- quality/landing-counters.sh` empty;
  committed blob `fac1a7c8d251ad67bc10d42aed936cfc7ff28f12`, sha256 `e4767ec74f1ff481a826573c7880f6107734ad31bd3b085e0eaba45415d82c4f`.
- Draft (exact file to cut over): `.ufo/waves/round-67/w1/R67ExecLanding/draft/quality/landing-counters.sh`
  — 280 lines, mode 755, sha256 `4378fd8c278126111ad6d970ac20215c170238ffe1a796c5c7d03c9e5b3b93a9`.

## Change — two hunks, nothing else

1. `SHIM` heredoc, `citecheck` arm: new `zero` mode prints exactly the frozen marker at rc 0
   `MADO_CITECHECK: rev=$FIXTURE_REV files=1 citations=0 resolved=0 missing=0 skipped_large=0 verdict=TARGET_MET`;
   `green`/`red`/`skip`/`crash`/`duplicate` output is byte-identical to the committed shim.
2. `run_selftest`, after the 21-case leg×mode matrix: one dedicated `citecheck zero` case asserting
   `rc=2` and all four witnesses `nav,usedby,ledger,citecheck`, then two source assertions on the
   instrument under test: the frozen guard clause `[ "$citations" -gt 0 ] && ` occurs exactly once in
   the file and exactly once inside `marker_valid`.

The guard needle is assembled from shell fragments (`'[ "$citations" -gt '"0"' ] && '`) so the
selftest's own source line cannot match itself; the contiguous frozen string still occurs exactly
once, in `marker_valid`. `marker_valid`, the 0/1/2 exit map, `--round` requirement, external-path
refusal, scratch safety and every child marker are untouched.

## Measured results

| command | rc | result |
|---|---|---|
| `bash -n draft/quality/landing-counters.sh` | 0 | syntax ok |
| `bash <draft> --selftest --scratch-root /fast/scratch/hyaku/mado-r67/R67ExecLanding/st` | 0 | `MADO_LANDING_COUNTERS_SELFTEST: 62/62 assertions passed` |
| `bash quality/landing-counters.sh --selftest --scratch-root .../base-st` (committed, same host) | 0 | `58/58 assertions passed` |
| label-set diff base→draft | 0 | 4 added, 0 removed, 0 `SELFTEST FAIL` |
| `<draft> --repo <lane> --rev 0b28ffb4 --round 66 --scratch-root .../real/run` (draft + real sibling scripts copied into scratch) | 0 | `MADO_LANDING_COUNTERS: GREEN (nav=0 usedby=0 ledger=0 citecheck=0 rev=0b28ffb4...)`, identical to the committed instrument |

New case lines (assertions 43–46):

```
SELFTEST ok 43: citecheck zero citations refused
SELFTEST ok 44: citecheck zero citations all execution witnesses
SELFTEST ok 45: zero-citation guard occurs exactly once
SELFTEST ok 46: zero-citation guard sits inside marker_valid
```

Retained zero-case instrument output (scratch reproduction, witnesses `nav,usedby,ledger,citecheck`, rc 2):

```
LANDING_LEG citecheck rc=0
LANDING_CONTRACT citecheck ERROR (rc=0; missing, malformed or inconsistent child marker)
MADO_LANDING_COUNTERS: ERROR (nav=0 usedby=0 ledger=0 citecheck=0 rev=<fixture rev>)
```

## M-Z kill probe (local, scratch, non-authoritative)

Copied the draft, deleted the exact frozen clause once (`text.count(needle) == 1`), `bash -n` passed,
ran its `--selftest`: **rc 1**, `59/62`, failing

```
SELFTEST FAIL 43: citecheck zero citations refused want=2 got=0
SELFTEST FAIL 45: zero-citation guard occurs exactly once want=1 got=0
SELFTEST FAIL 46: zero-citation guard sits inside marker_valid want=1 got=0
```

Mutant sha256 `a6255a00262cc2f1790f813927dd5fa8ed9910e74d1ec19a8662e88df0fe0118`. The authoritative
mutant run is C2's counter (`c2-r67-landing-controls.py`), not this probe; no counter was written or scored here.

## Risks / notes

- The guard assertions are source-text assertions, so a formatting-only rewrite of the guard line would
  make the selftest red. That is intended: M-Z is an exact-text deletion of that clause, and the frozen
  predicate says the clause must still occur exactly once in `marker_valid`.
- `zero` is a citecheck-only shim mode; no other leg's `zero` behaviour is used or asserted.
- Running the draft in place inside the seat dir returns rc 2 because sibling children
  (`counters/c3-r56-used-by.py`, `check-tool-ledger.py`, `../tools/mado-receipt-citecheck.py`) do not
  exist there; with the real siblings the run is GREEN (row above). Cutover at the standing path restores them.
- No tool installs or upgrades were needed. No pacman transaction was attempted.

## Scratch

`/fast/scratch/hyaku/mado-r67/R67ExecLanding` removed after collecting the evidence above (fixture repos,
mutant copy, shim harness and captured stdout all deleted).
