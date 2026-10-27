# C1 inventory-boundary mutation probe

## Frozen claim and axes

C1 is frozen as the inventory count of files under `tools/`, direct `quality/*.py`, and direct `quality/counters/*.py`; one ledger row per such file. Axes attacked: **coverage** (path classes included/excluded) and **operability** (counter's independent measurement and exact output).

## Mutation and detector

Built isolated git fixture `/fast/scratch/hyaku/mado-r51/MutC1ToolRename/repo`, checked out at frozen base `6ca8c559a4a3d6d361101592116eea2bc7452437`. No lane bytes changed. Added five candidate paths: `tools/edge.sh`, `tools/sub/extra.py`, `quality/edge.py`, `quality/sub/nested.py`, `quality/counters/edge.json`. The detector was the actual frozen C1 counter command, with its required `--repo`, `--rev HEAD`, and explicit scratch `--work`; records are in the output below. The synthetic repo necessarily has no base ledger/checker, so `TARGET_MISSED ledger=absent` on pristine baseline is not a killed mutant or evidence against the population filter. This makes the end-to-end ledger population portion inconclusive; the counter's printed population is still directly measured.

Command:

```sh
python3 -I /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-51/w1/ExecLedgerCounter/c1-r51-ledger.py --repo /fast/scratch/hyaku/mado-r51/MutC1ToolRename/repo --rev HEAD --work /fast/scratch/hyaku/mado-r51/MutC1ToolRename/work
```

## Actual outputs

Pristine frozen-base run (rc 1):

```text
C1_R51: verdict=TARGET_MISSED ledger=absent population=79 rev=6ca8c559a4a3d6d361101592116eea2bc7452437
```

After adding five paths, before ledger (rc 1):

```text
C1_R51: verdict=TARGET_MISSED ledger=absent population=82 rev=53302c795e70005f345cb3282310450aa819828d
```

Observed delta is +3: both tools paths and direct `quality/edge.py` counted; nested quality Python and quality/counters JSON excluded. Thus the tested population behavior **matches the frozen sentence**. The initial probe attempted to use the real lane ledger at base and failed because, as frozen, it is absent there; that scratch attempt was reset to base before the clean probe.

A subsequent isolated ledger attempt was **inconclusive**, not a kill: the scratch fixture based on the real repo's base has 79 additional required population files, omits those rows, and its pointer does not name its own checker. It yielded `population=83 ledger_rows=4 uncovered=79 bad_pointer=1 checker=failed verdict=TARGET_MISSED`. The attempt does not refute or validate the frozen claim's full-target gate; the exact class-boundary counter measurement is the useful result.

## Verdict

**PASS (boundary probe only), full predicate INCONCLUSIVE.** No mismatch found for these path classes: tool descendants of any extension are included, nested `tools/sub/extra.py` included, top-level `quality/*.py` included, nested `quality/sub/*.py` excluded, and `quality/counters/*.json` excluded. Existing implementation is at `quality/counters/c1-r51-ledger.py:133-148` (frozen source copy used by the command: `w1/ExecLedgerCounter/c1-r51-ledger.py`). The frozen sentence itself does not claim nested quality files or counter JSON are population members.

## Restoration evidence

Scratch fixture was restored to exact base commit `6ca8c559a4a3d6d361101592116eea2bc7452437` before the clean probe; its pristine output above confirmed the base path and count. Lane repository not mutated. Temporary fixture and driver reside solely under the assigned scratch root; delete that root after the record is secured.
