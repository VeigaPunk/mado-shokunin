# RevSelftest — standing suite selftest, read-only

Seat: `L1Mado36.RevSelftest` (reviewer). Round 36, wave 1.
Lane root: `/home/vgpnk/Projects/shokunin/mado-shokunin`.
Assignment: run the lane's standing suite read-only, record it exactly, and
check whether `tools/mado-verify.sh` bytes are unchanged from the round-35 tip
(`7a068cb`).

## Items and verdicts

| # | Item | Verdict |
|---|------|---------|
| 1 | `bash tools/mado-verify.sh --selftest` runs and reports its final `MADO_SELFTEST:` line | PASS — `MADO_SELFTEST: 460/460 assertions passed` |
| 2 | Exit code of the selftest run | PASS — `0` |
| 3 | `sha256sum tools/mado-verify.sh` | recorded — `050efc720599345a73bdce6c1d13d50eadeee9769c2ece02462223d0156703f1` |
| 4 | `wc -l tools/mado-verify.sh` | recorded — `4194` |
| 5 | Tool bytes unchanged from round-35 tip `7a068cb` | PASS — working-tree blob equals `7a068cb:tools/mado-verify.sh` |

## Commands run and quoted output

All commands run from `/home/vgpnk/Projects/shokunin/mado-shokunin`.

### Selftest (run twice; identical both times)

    bash tools/mado-verify.sh --selftest; echo "EXIT_CODE=$?"

stdout (verbatim, complete — the script prints exactly one line):

    MADO_SELFTEST: 460/460 assertions passed
    EXIT_CODE=0

Second run captured to scratch:

    bash tools/mado-verify.sh --selftest > scratch-stdout.txt 2> scratch-stderr.txt

- stdout file: `.ufo/waves/round-36/scratch/RevSelftest/selftest-stdout.txt`
  contains `MADO_SELFTEST: 460/460 assertions passed` (+ appended `EXIT=0`).
- stderr file: `.ufo/waves/round-36/scratch/RevSelftest/selftest-stderr.txt`
  is empty (0 lines per `wc -l`).
- Wall times observed: ~15.6 s and ~22.2 s.

### File identity

    sha256sum tools/mado-verify.sh
    # 050efc720599345a73bdce6c1d13d50eadeee9769c2ece02462223d0156703f1  tools/mado-verify.sh

    wc -l tools/mado-verify.sh
    # 4194 tools/mado-verify.sh

### Round-35 tip comparison

    git rev-parse 7a068cb:tools/mado-verify.sh
    # 9113c7c05e586328f44ed6822a3d12ff34c47a36   (exit 0)

    git hash-object tools/mado-verify.sh        # working-tree bytes
    # 9113c7c05e586328f44ed6822a3d12ff34c47a36

    git rev-parse HEAD:tools/mado-verify.sh
    # 9113c7c05e586328f44ed6822a3d12ff34c47a36

    git status --porcelain tools/mado-verify.sh
    # (empty output — path clean)

    git log --oneline -1 7a068cb
    # 7a068cb round-35: close

    git rev-parse HEAD
    # dbf8b579aeac0f023aaf595770f1cb0049e4baa2   ("round-36: freeze both predicates…")

**Verdict: PASS** — the working-tree blob hash `9113c7c0…` is byte-identical to
`7a068cb:tools/mado-verify.sh`; the path is clean under `git status`. The gate is
untouched since before the round-35 close (last content change: round-19, per
`git log -- tools/mado-verify.sh`: `7b4839d … 460/460`).

## Interpretation against the registration

`registration.md` harm-watch line "bash tools/mado-verify.sh --selftest stays
green (the gate is not touched)" holds at the freeze commit `dbf8b57`: the gate
is green at 460/460, exit 0, and the bytes are the same blob committed at the
round-35 tip `7a068cb` ("round-35: close"). No finding.

## Scope compliance

- Read-only on every production file; the only writes are this report and
  `.ufo/waves/round-36/scratch/RevSelftest/{selftest-stdout.txt,selftest-stderr.txt}`.
- No installs or tool updates were needed or performed (all commands used
  stock `bash`, `git`, `sha256sum`, `wc`, `python3` already on the host).
- No `model` parameter passed; no compositor/config/service mutation; no
  sibling-lane or fleet-root writes.

## Verification gaps / residual risk

- The selftest line is a summary only (`460/460`); per-assertion detail is not
  printed by `--selftest`. A deeper audit of which assertions the 460 cover is
  out of this seat's scope.
- `460` is consistent with the last gate change note (`7b4839d`, round-19,
  "460/460"), so the count is not new this round — expected, since the gate is
  byte-identical to the round-35 tip.
