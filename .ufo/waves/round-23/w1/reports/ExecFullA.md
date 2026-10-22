# ExecFullA — C1 tripwire candidate (round 23, wave 1)

**Status: comparison candidate, frozen mid-wave by L1. Report written under a
10-minute freeze constraint; not all guards were run.**

## What I did

- Worked only in my own clone:
  `/fast/scratch/hyaku/mado-r23/ExecFullA/clone`
  (branch `feature/r23-frame-owning-env`, base `a28e4815`).
- Implemented the prescribed two-part C1 fix (plus one small companion rule)
  in `tools/mado-tripwire.py`; see `design-note.md` for details.
- Verified syntax (`python3 -m py_compile` → OK) and ran the round-23 repair
  measure and the CritFrameNeighbour measure against the candidate.

## Candidate

- Patch: `.ufo/waves/round-23/w1/out/ExecFullA/candidate.patch`
  (`git diff a28e4815... -- tools/`, 285 lines, +121/−22 in one file).
- Candidate tool sha256: `91a1f8961200571916610ee1cee747864b40cdc16cf02450740a5284d8fbf4e3`
- Guards receipt: `.ufo/waves/round-23/w1/out/ExecFullA/guards.json`

## Verified results

| Guard | Command | Result |
|---|---|---|
| Round-23 repair set (C1) | `python3 -I .ufo/waves/round-23/repair/measure.py --tool <cand>` | **12/12 pass**, unparsed 0 on every case |
| CritFrameNeighbour (L1 extra) | `python3 -I .ufo/waves/round-23/w1/out/CritFrameNeighbour/measure.py --tool <cand>` | 3/3 `base-correct` (DecoratorWrapperCallsWrapped, HelperCalledFromLambda, HelperCalledFromMethod) |

The 12 repair cases include all six previously-failing cases:
ReturnedGlobalCallableShadow, ForwardExistingClosureWithoutFrameContamination,
ForwarderInvokesCallback, CallerLocalShadowsHelperGlobal,
ForwarderPassesCallerArgument, ForwarderInvokesFactoryClosure — all now
`True` with `unparsed=0` and exact expected rows.

## Not run (freeze) — must still be verified by the integration gate

- Round-22 primary 57/57 (`.ufo/waves/round-22/oracle/measure.py`).
- Round-21 oracle 35/35 + 17/17 (`.ufo/waves/round-22/replay.py --mode oracle`).
- Eleven legacy selftest suites 247/247 (`prlimit --as=402653184 --cpu=15 python3 -I <tool> --selftest <suite>`).
- Round-22 corpus comparator, 1356 files, vs base classifier (`.ufo/waves/round-22/replay.py --mode corpus --before-tool <base>`).
- Precision guard via local commit + `tw-precision.py` (166/175 same passing set).
- Round-21 and round-22 resource populations (module-main / cli).
- CritScheduledNeighbour: the provided `cases.py` regenerates **base** labels
  (it extracts the base commit's classifier), so it is not a candidate runner;
  I did not repurpose it under time pressure.
- CritEscapeNeighbour: `run.py` resolves `ROOT.parents[5]` relative to the
  lane; copying the dir to /tmp broke that path resolution, so it was not run
  (out dir copy safe; judge needs the original path).

## Risks / notes for the gate

- The `ctx["swept"]` follow-marking (rule 3) and the escape-guarded
  suppression (rule 2) alter sweep behavior and can change lead rows /
  unparsed counts; the corpus comparator and oracle must be re-run to
  adjudicate any added/removed groups. Zero error flips is a constraint, not
  yet demonstrated.
- `genv` threading touches every `spawn_scan` call path; deep/large files
  were not stress-tested under the 384 MiB / 15 s caps after the change.

**Verdict:** repair-set target met (12/12) and one extra neighbour set green;
all remaining no-harm guards are unrun and must be executed before landing.
