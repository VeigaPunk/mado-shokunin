# R67ExecRegister — C1 register citation-to-live-object discrimination

Axis: calibration (C1). Claim: C1 only. L1 integrates; nothing in the lane was cut over here.
Lane tip while working: `ac376ef3fbf12d606f04dcd1e2be35312887d219`; measured revision: `061dc329b598b2723a224b6c7b305b436946ec91`.

- Draft (exact file to cut over): `.ufo/waves/round-67/w1/R67ExecRegister/draft/quality/counters/c1-r67-register.py`
  — 325 lines, mode 755, sha256 `58d6c0aba4281ba0c75f653ea0c1fa4d8c90b6450d49b681bec34247eba1c9ec`.
- First reviewed sha256 `d14fcad80922548f8b45225dc824bf69c5b5984aff1f920bf923b07ee78fbd8d` was superseded by the
  dangling-receipt fix below (reviewer repro `live-plus-unresolved-same-row`).

## What the counter measures (frozen predicate → field)

Every byte comes from `git -C <repo> show <rev>:<path>`; the worktree is never opened, no host probe runs,
`--scratch-root` is accepted for interface parity and unused (nothing is written).

| frozen clause | implementation |
|---|---|
| exactly one heading | count of lines starting `### Surface state register (2026-11-03` == 1 |
| exactly the 8 frozen group rows | 8 data rows; each group string exactly once in a first cell (exact equality, case-sensitive); any unknown first cell is a reason |
| every row's FOURTH cell names ≥1 resolving receipt | tokens of cell 4 only, `^\.ufo/waves/round-[0-9]+/receipts/[^ \|,)]+\.(txt\|json\|md\|sh)$`, one wrapper/punctuation run stripped; resolution = `git show <rev>:<path>` |
| live path inside a row's FOURTH cell | `LIVE_PATH` must be a token of some cell 4; state/probe/heading/prose mentions do not count (`live-cited`) |
| exact CLEAN line at LIVE_PATH | `LIVE_LINE` must equal a whole line of the object at `LIVE_PATH`; literal verified against committed bytes at `061dc329` (`LIVE_LINE_exact_committed_line=True`, `LIVE_LINE_matches_controls=True`) |
| git env | all `GIT_*` scrubbed; `GIT_OPTIONAL_LOCKS=0`, `GIT_NO_REPLACE_OBJECTS=1`, `GIT_PAGER=cat`, `LC_ALL=C` |

Retained r66 rule (stricter than the frozen minimum, changes no frozen expectation): a receipt token named in a
FOURTH cell that does not resolve is a reason (`receipt-unresolved-in-receipt-cell=<path>`), so a live pointer
beside an unresolved pointer is rejected, not passed.

## Measured results

| command (lane root) | rc | result |
|---|---|---|
| `python3 -I <draft> --selftest` | 0 | `MADO_R67_REGISTER_SELFTEST: PASS cases=15 failed=0` |
| `python3 -I <draft> --repo /home/vgpnk/Projects/shokunin/mado-shokunin --rev 061dc329b598b2723a224b6c7b305b436946ec91 --controls /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-67/controls/c1-controls.json` | 0 | `register=accept controls=6/6 … verdict=TARGET_MET` |
| `python3 -I -m py_compile <draft>` | 0 | syntax ok |
| reviewer harness `review.py <draft>` (R67RevRegister, independent) at sha `d14fcad…` | 0 | frozen 6/6 accepted, pairwise-distinct case hashes, linecheck ok, worktree poison no-op; final sha re-verified here by the measured run and forgery replay below |

Final printed line (exact):

```
MADO_R67_REGISTER: register=accept controls=6/6 headings=1 rows=8 groups=8/8 live-cited=yes verdict=TARGET_MET rev=061dc329b598b2723a224b6c7b305b436946ec91
```

Per-case lines (exact, stdout):

```
C1_R67 case=genuine verdict=accept expect=accept correct=yes headings=1 rows=8 groups=8/8 live-cited=yes
C1_R67 case=duplicate-heading verdict=reject expect=reject correct=yes headings=2 rows=8 groups=8/8 live-cited=yes
C1_R67 case=row-without-receipt verdict=reject expect=reject correct=yes headings=1 rows=8 groups=8/8 live-cited=yes
C1_R67 case=file-plane-only verdict=reject expect=reject correct=yes headings=1 rows=8 groups=8/8 live-cited=no
C1_R67 case=unreferenced-live-object verdict=reject expect=reject correct=yes headings=1 rows=8 groups=8/8 live-cited=no
C1_R67 case=live-in-state-cell-only verdict=reject expect=reject correct=yes headings=1 rows=8 groups=8/8 live-cited=no
```

Selftest cases (15 = the six frozen shapes + nine extras): `genuine`, `duplicate-heading`,
`row-without-receipt`, `file-plane-only`, `unreferenced-live-object`, `live-in-state-cell-only`,
`live-plus-unresolved-same-row`, `wrong-heading-date`, `seven-rows`, `nine-rows`,
`live-only-in-heading`, `missing-fourth-cell`, `duplicate-group`, `unresolved-receipt`,
`live-bytes-without-clean-line`; all PASS, hermetic (strings only, no subprocess, no file read).

Baseline context (read from the committed receipt, not re-run here): `control-baseline-r67.txt` records the
r66 counter at 4/6, accepting exactly `unreferenced-live-object` and `live-in-state-cell-only`; this draft
rejects both.

## Reviewer defect fixed (independent review, R67RevRegister)

Reviewer finding on `d14fcad…`: genuine fourth cell plus `.ufo/waves/round-65/receipts/not-committed.txt`
was accepted; r66 rejected all named unresolved receipts. Fix: the fourth-cell dangling-pointer loop above,
plus selftest case `live-plus-unresolved-same-row`. Replay of the reviewer's own `forgeries.json` against the
final sha:

```
REJECT heading-only
REJECT twice-cited-missing-line
REJECT probe-cell-only
ACCEPT receipt-trailing-punctuation        (non-defect: token normalization, see risks)
REJECT nine-rows
REJECT seven-rows
REJECT live-plus-unresolved-same-row :: receipt-unresolved-in-receipt-cell=.ufo/waves/round-65/receipts/not-committed.txt
REJECT duplicate-capitalization
REJECT sentinel-above-table
ACCEPT forged-state-known-nonclaim         (frozen non-claim: state-cell truth)
```

All six frozen cases keep their expectation and the real register still accepts after the fix.

## Adversarial fixtures (own scratch, non-authoritative)

Driver: `python3 -I adversarial.py` (fixture git repo under seat scratch; toplevel asserted after `init` and
before every commit). Result: `FIXTURE_SUMMARY: cases=9 failed=0`, driver rc 0.

| case | rc | evidence |
|---|---|---|
| worktree divergence (uncommitted genuine-looking PROVINCE.md, committed file-plane-only block) | 1 | `register=reject controls=6/6 … verdict=TARGET_MISSED`; `git show` still returns the committed bytes |
| planted `refs/replace` on `PROVINCE.md` blob | — | `guarded_has_forgery=False plain_has_forgery=True` (guard is effective) |
| same planted ref, counter with `GIT_NO_REPLACE_OBJECTS` deleted | 0 | `register=accept controls=6/6 … verdict=TARGET_MET` — guard is load-bearing |
| bad `--rev` | 2 | `C1_R67: setup=error detail=fatal: Needed a single revision` |
| non-repo `--repo` | 2 | `C1_R67: setup=error detail=fatal: cannot change to …` |
| missing controls file | 2 | `C1_R67: setup=error detail=controls-unreadable=…` |
| `--controls` omitted | 2 | `c1-r67-register.py: error: --rev and --controls are required unless --selftest is selected` |
| altered frozen `live_line` in a controls copy | 2 | `C1_R67: setup=error detail=controls-live-constants-disagree-with-counter` |
| genuine fixture (rows cite live, live object committed) | 0 | `register=accept controls=6/6 … verdict=TARGET_MET` |

## Risks / notes

- The counter requires `--controls` in normal mode (exit 2 without it): the frozen target is
  `register=accept AND controls=6/6`, so a register-only run cannot claim `TARGET_MET`. `--scratch-root` is
  accepted and ignored; the counter writes nothing and makes no scratch directory.
- `receipt-trailing-punctuation` is accepted by design: the tokenizer strips one markdown wrapper/punctuation
  run (same normalization as the r65 and r66 counters), so `` `LIVE`., `` still names the live path in cell 4.
  Rejecting it would fail legitimate prose-style cells and would be a behavior change against both predecessors.
- `forged-state-known-nonclaim` is accepted: the frozen kill rule explicitly excludes state-cell truth from
  this claim. Receipts and the CLEAN line do not establish current surface state.
- The dangling-pointer rule is stricter than the frozen minimum; all six frozen expectations and the real
  register are unchanged by it, and it restores the r66 nonregression.
- No tool installs or upgrades were needed; no pacman transaction was attempted.

## Scratch

`/fast/scratch/hyaku/mado-r67/R67ExecRegister` (fixture repo, mutant copy, driver) removed after collecting
the evidence above; `ls /fast/scratch/hyaku/mado-r67` no longer lists it.
