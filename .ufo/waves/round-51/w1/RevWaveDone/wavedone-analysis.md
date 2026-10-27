# Wave-done checker analysis (D1)

## Scope and finding

Reviewed `quality/check-wave-done.py`. `scan()` enumerates committed `*.ready` markers at the requested revision and calls `check_wave()` for each; `run_check()` considers the round `OK` iff there is at least one marker and all discovered waves settle. CLI arguments require `--repo`, `--rev`, and `--round`; there is no expected-wave count or separate final-receipt/commit-tip requirement.

Therefore the sequence in the assignment can repeat D1: WAVE-DONE w1 and w2 are valid receipts over the commits at those moments, but the later integration commit is not constrained to include a receipt generated at that integration tip. A filed report asserting final validation is not checked by this gate. In particular, a previously committed receipt stays evidence about its old `--rev`, not the later tip. This is a checker-design gap, not evidence that the final sequence is blocked by any committed gate.

## Exact commands and outputs

Commands were run from `/home/vgpnk/Projects/shokunin`; scratch path was `/fast/scratch/hyaku/mado-r51/RevWaveDone`.

```sh
python3 /home/vgpnk/Projects/shokunin/mado-shokunin/quality/check-wave-done.py --repo /home/vgpnk/Projects/shokunin/mado-shokunin --rev 74782d39 --round 50 --work /fast/scratch/hyaku/mado-r51/RevWaveDone; printf 'exit=%s\\n' "$?"
```

```text
WAVE wave=w1 ready=1 results=present seats=54 dispatched=54 settled=54 verdict=OK reason=none
WAVE wave=w2 ready=1 results=present seats=32 dispatched=32 settled=32 verdict=OK reason=none
MADO_WAVE_DONE: round=50 waves=2 settled=2 verdict=OK
exit=0
```

At `74782d39`, the checker reads **waves=2**, not 1. This differs from the spot-check lesson's description of the `8dbbf61a` receipt's measured revision: the queried revision here is the later round-50 tip, at which both ready markers exist.

```sh
python3 /home/vgpnk/Projects/shokunin/mado-shokunin/quality/check-wave-done.py --repo /home/vgpnk/Projects/shokunin/mado-shokunin --rev 8dbbf61a --round 50 --work /fast/scratch/hyaku/mado-r51/RevWaveDone; printf 'exit=%s\\n' "$?"
```

```text
WAVE wave=w1 ready=1 results=present seats=54 dispatched=54 settled=54 verdict=OK reason=none
MADO_WAVE_DONE: round=50 waves=1 settled=1 verdict=OK
exit=0
```

```sh
python3 /home/vgpnk/Projects/shokunin/mado-shokunin/quality/check-wave-done.py --repo /home/vgpnk/Projects/shokunin/mado-shokunin --rev c12b588e --round 50 --work /fast/scratch/hyaku/mado-r51/RevWaveDone; printf 'exit=%s\\n' "$?"
```

```text
WAVE wave=w1 ready=1 results=present seats=54 dispatched=54 settled=54 verdict=OK reason=none
WAVE wave=w2 ready=1 results=present seats=32 dispatched=32 settled=32 verdict=OK reason=none
MADO_WAVE_DONE: round=50 waves=2 settled=2 verdict=OK
exit=0
```

The later `c12b588e` state has waves=2. A committed receipt at `8dbbf61a` remains a historical w1-only receipt; it does not change what the tip says. Querying `74782d39` likewise directly shows two waves because both markers are present there.

## Procedure addition (L1 adoption)

**After all integration changes are committed, run `python3 -I quality/check-wave-done.py --repo <lane> --rev HEAD --round <N> --work <scratch>`, require exit 0 and `waves=<expected> settled=<expected> verdict=OK`, commit that exact output as the final receipt, and only then file the report citing that receipt commit.**

## Verification boundary

The historical commands above were executed against the lane repository's committed bytes. The proposed procedure makes the required final-tip check and its receipt an explicit post-integration precondition; whether an external report gate independently enforces this procedure is not established here.
