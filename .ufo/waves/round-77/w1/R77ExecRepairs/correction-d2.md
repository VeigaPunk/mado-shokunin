# D2 — stale C2 revision on SCORECARD.md:4339

Seat R77ExecRepairs, round 77, 2026-11-04. Lane HEAD `0fa69f41d81275db102bbe08cf5d6a86a5dfe8f7`.

## Defect

`SCORECARD.md:4339` (round-76 C2 row, raw) says:

> … at `5dade9b3` (its instrument's last change, the D3 parameter-binding repair): …

`5dade9b3` is **not** `quality/counters/c2-r76-shapes.py`'s last-change commit. It is the
D3 parameter-binding repair; two later wave-repair commits moved the file again
(`3588a527`, 30 insertions / 14 deletions later, per the round-76 spot-check D2). No
`rev=5dade9b3` receipt exists; the correct measurement revision is `3588a527`.

## Re-derivation (run at HEAD)

    $ cd /home/vgpnk/Projects/shokunin/mado-shokunin
    $ git log -1 --format=%H -- quality/counters/c2-r76-shapes.py
    3588a527eba555a94e497097b0467efc04274c6d

    $ git log --format='%h %s' -- quality/counters/c2-r76-shapes.py
    3588a527 round-76: wave-found repairs - C1 base-rev binding, C2 allowlisted child env and scope-local call cancellations, with receipts and the carried limits
    5dade9b3 round-76: C2 repair - D3 cancels only the argument bound to the deleted parameter (R76RevC2 P2, R76Mutant d3-anyarg), with the red-before/green-after receipt
    755b339f round-76: freeze - claims declaration, both frozen control sets, the pre-freeze do-nothing control, and the three successor instruments

## Correction (append-only; the row is not rewritten)

The landed correction is at `SCORECARD.md:4393-4398`, under the round-76 section
(`### Corrections (round 77, append-only)`), landed by `3e35d0a9`:

```markdown
### Corrections (round 77, append-only)

The C2 row above cites `5dade9b3` as its instrument's last change; the measured last change is
`3588a527` (`git log -1 --format=%H -- quality/counters/c2-r76-shapes.py` prints
`3588a527eba555a94e497097b0467efc04274c6d`). The counts are unchanged; the revision label was
stale (round-76 closure D2). The report carries the correct revision.
```

No uncommitted measurement revision is claimed: the counts are the round-76 receipts' counts
(`population=20 readers=13 guarded=13 unguarded=0 controls=59/59 base_controls=55/59
verdict=TARGET_MET`, rc 0); only the revision label is corrected.

## Executable consequence

The linked probe `check-cited-revisions-probe.py` (this seat) mechanizes exactly this class:

    $ python3 -I .ufo/waves/round-77/w1/R77ExecRepairs/check-cited-revisions-probe.py \
        --repo . --text .ufo/waves/round-77/w1/R77ExecRepairs/red-row.txt
    … RESULT red claims=1 mismatched=1          (exit 1; the row as landed)

    $ python3 -I .ufo/waves/round-77/w1/R77ExecRepairs/check-cited-revisions-probe.py \
        --repo . --text .ufo/waves/round-77/w1/R77ExecRepairs/green-row.txt
    … RESULT green claims=1 mismatched=0        (exit 0; the row with `5dade9b3` → `3588a527`)
