# C2 held-line mutants

## Scope and baseline

Frozen claim: `claims.md` PRED-C2-r51 clause (d), requiring ≥3 distinct `held:` citations naming a base knowledge file line, with every pinned key token on that line. Counter: `quality/counters/c2-r51-dispatch-entry.py`. Attack ran only in `/fast/scratch/hyaku/mado-r51/MutC2HeldLines/fixture`, a no-hardlinks clone checked out at `a0e34387b30538372a1bb219eb3ccdc74013d458`.

Pristine counter command (same command used for all trials):

```sh
TMPDIR=/fast/scratch/hyaku/mado-r51/MutC2HeldLines python3 -I quality/counters/c2-r51-dispatch-entry.py --repo /fast/scratch/hyaku/mado-r51/MutC2HeldLines/fixture --rev <trial-rev>
```

Pristine data revision output: exit 0; `d ok=1 held=7/3 lines=8 untargeted=1 tokens=14`; final `clauses=abcd clauses_met=4 admitted=1/1 verdict=TARGET_MET rev=a0e34387b30538372a1bb219eb3ccdc74013d458`. Thus the baseline is valid.

## Mutants

Each mutant substituted the original entry's seven targeted held lines with the listed line(s), retaining the unrelated, untargeted `held (cited...)` line. All mutations committed only in the scratch clone.

| Mutant | Held lines inserted | Counter output | Verdict |
|---|---|---|---|
| Duplicate one valid citation 3x | `held: corpus/knowledge/bind-table-r25.md:38 keys=DISPATCHER,ARG,numbArgs` repeated three times | exit 1; `d ok=0 held=1/3 lines=4 untargeted=1 tokens=3`; final clauses_met=3, TARGET_MISSED | Killed. Identical `(file,line)` counts once; `seen` de-duplicates locations. |
| Absent file | `held: corpus/knowledge/absent-r51-mutant.md:1 keys=dispatcher` | exit 1; `d ok=0 held=0/3 lines=2 untargeted=1 tokens=0 miss=file_absent:corpus/knowledge/absent-r51-mutant.md`; clauses_met=3, TARGET_MISSED | Killed. |
| Out-of-range line | `held: corpus/knowledge/bind-table-r25.md:999999 keys=DISPATCHER` | exit 1; `d ok=0 held=0/3 lines=2 untargeted=1 tokens=0 miss=line_out_of_range:bind-table-r25.md:999999`; clauses_met=3, TARGET_MISSED | Killed. |
| One token absent | `held: corpus/knowledge/bind-table-r25.md:38 keys=DISPATCHER,ZZZmutant` | exit 1; `d ok=0 held=0/3 lines=2 untargeted=1 tokens=0 miss=token_missing:bind-table-r25.md:38:ZZZmutant`; clauses_met=3, TARGET_MISSED | Killed. |

Full counter outputs also had clauses a,b,c `ok=1` in all mutants, isolating misses to d. Mutant revisions respectively: `91a44cf6ddd3effd8d5d18f73f5c41aeba1d13a4`, `6186e275166ec3d29587c601bdf17fa5b1b8ad4f`, `1e579843de4d4295b2f2a68fd05dd71a1b69731b`, `38911c5c39facbc56b3f844f1cf57232adb4ce63`.

## Exact-predicate result

**PASS / all four mutants killed under the frozen clause-(d) sentence and the W1 counter fixture.** Duplicate citations are not distinct: the counter keys accepted cites by `(name, line)` and skips a key already seen (`clause_d`, lines 529–533), then checks `len(cites) >= MIN_HELD`.

W1 fixture-builder caveat: invoking `w1/ExecCounterC2/make-fixture.py --mode pass` at the C2 data revision aborts at line 156 because S364 already exists after S363. This setup failure was not treated as baseline evidence. The clone of the real data revision itself provided a pristine baseline that TARGET_MET, followed by all requested isolated mutations.

Restoration: after each mutation the clone was checked out back to `a0e34387b30538372a1bb219eb3ccdc74013d458`; restored counter run again TARGET_MET. Restored entry blob SHA-256: `77eee0d5e0c8c80aa60f8aa4501cb6a0858e63ccaa1a89dea83e427ad97e046a` (read from the pinned revision). `git status --short` was empty after restore.
