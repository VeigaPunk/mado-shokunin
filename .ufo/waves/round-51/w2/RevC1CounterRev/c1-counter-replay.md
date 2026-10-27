# C1 counter replay — RevC1CounterRev

Axes: **coverage + operability**. Attack scope: frozen C1 counter/revision behavior; no lane code modified.

## Exact commands and output

Commands run from `/home/vgpnk/Projects/shokunin` against the current lane path, with distinct `--work` roots:

```sh
L=/home/vgpnk/Projects/shokunin/mado-shokunin
python3 -I "$L/quality/counters/c1-r51-ledger.py" --repo "$L" --rev 56026fcb9800370ae04bc65952a6567181c398d0 --work /fast/scratch/hyaku/mado-r51/RevC1CounterRev/freeze
```

```text
detail: checker selftest ok (ratio=50/50 form=with-work)
detail: checker ledger ok (rev=56026fcb9800370ae04bc65952a6567181c398d0)
C1_R51: population=82 ledger_rows=82 uncovered=0 dangling=0 bad_pointer=0 empty_desc=0 selftest=ok verdict=TARGET_MET rev=56026fcb9800370ae04bc65952a6567181c398d0
exit=0
```

```sh
python3 -I "$L/quality/counters/c1-r51-ledger.py" --repo "$L" --rev 6ca8c559a4a3d6d361101592116eea2bc7452437 --work /fast/scratch/hyaku/mado-r51/RevC1CounterRev/base
```

```text
detail: quality/tool-ledger.md absent at 6ca8c559a4a3
C1_R51: verdict=TARGET_MISSED ledger=absent population=79 rev=6ca8c559a4a3d6d361101592116eea2bc7452437
exit=1
```

Receipt comparison: frozen run is TARGET_MET and base run TARGET_MISSED, matching the exact frozen sentence and base receipt in `w1/ExecLedgerCounter/receipts/base-and-setup.txt`. The selftest result is `50/50` and the reported checker-ledger revision is exactly the selected freeze revision.

## Revision isolation and disagreement attack

The current worktree contains the later counter and ledger. The counter implementation explicitly resolves the requested revision, creates a clone from that revision, enumerates paths with `git ls-tree -r <rev>`, and reads files with `git show <rev>:<path>` (see `quality/counters/c1-r51-ledger.py`, functions `make_clone`, `listing`, `show`, and main lines 375–409). Therefore the predicate's assessed population/ledger/checker inputs are from the selected commit, not the caller worktree. The two executions yield the expected 82 files at freeze and 79 at base.

I did not run a mutation or create a mismatched repository whose requested rev resolves elsewhere; that is not necessary to establish whether the current-worktree-vs-selected-revision disagreement is noticed: the selected revision is explicitly printed and used for the assessment. **PASS** for frozen predicate and selected-revision isolation. The predicate's already-registered limitations (comment-only accountability pointers and repeated generic descriptions; registration lines 11) remain outside this revision replay and are not treated as newly falsified here.
