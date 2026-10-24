# round-33 pre-data control receipt

Scored before any corpus append. Predicate sentences match `registration.md`,
`c1/count.py`, `c1/frozen.json`, and `c2/count.py`.

```
PRED-C1-r33-v1 closed_entries=0 closed_rows=0 open_cites=4 verdict=TARGET_MISSED
exit=1
```

do-nothing, junk, rows-only, and entries-only each printed that line (exit 1).
hash-mismatch printed `closed_entries=1 closed_rows=3 open_cites=1 verdict=TARGET_MISSED` exit 1.
golden and extra-source each printed `closed_entries=2 closed_rows=4 open_cites=0 verdict=TARGET_MET` exit 0.

```
PRED-C2-r33-v1 claim_mismatch=1 reason=absent verdict=TARGET_MISSED
exit=1
PRED-C2-r33-v1 claim_mismatch=1 reason=mismatch published=3 measured=7 verdict_word=target-met rev=d9ed38166cc3be8ef4c52b41d66ad94010feb047 verdict=TARGET_MISSED
exit=1
PRED-C2-r33-v1 claim_mismatch=0 reason=match published=7 measured=7 verdict_word=honest-stop rev=d9ed38166cc3be8ef4c52b41d66ad94010feb047 verdict=TARGET_MET
exit=0
```

Skip-the-work controls do not meet either target.
