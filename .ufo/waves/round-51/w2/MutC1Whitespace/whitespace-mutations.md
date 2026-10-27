# C1 whitespace and row-shape mutation results

Target: frozen PRED-C1-r51 counter at freeze revision. Every mutant applied only to a detached scratch clone; source lane ledger bytes were not edited.

### whitespace-only
- Mutation: Replace every populated description cell with whitespace-only content.
- Command: `python3 -I /fast/scratch/hyaku/mado-r51/MutC1Whitespace/whitespace-only-repo/quality/counters/c1-r51-ledger.py --repo /fast/scratch/hyaku/mado-r51/MutC1Whitespace/whitespace-only-repo --rev 56026fcb9800370ae04bc65952a6567181c398d0 --work /fast/scratch/hyaku/mado-r51/MutC1Whitespace/whitespace-only`
- Exit: 0
- stdout:
```
detail: checker selftest ok (ratio=50/50 form=with-work)
detail: checker ledger ok (rev=56026fcb9800370ae04bc65952a6567181c398d0)
C1_R51: population=82 ledger_rows=82 uncovered=0 dangling=0 bad_pointer=0 empty_desc=0 selftest=ok verdict=TARGET_MET rev=56026fcb9800370ae04bc65952a6567181c398d0
```
- stderr:
```

```
- SHA256 pristine=df5b3705d0291f967c35f0d69d6a908fe37a30d35e84599c4c0f897ca6469e0b; mutated=a443aff24ef63bca9bdcb8f6585b93df1df776d6d2c20d4863f56fee872942a7; restored=df5b3705d0291f967c35f0d69d6a908fe37a30d35e84599c4c0f897ca6469e0b; restored_exact=True

### punctuation-only
- Mutation: Replace every populated description cell with punctuation/marks only.
- Command: `python3 -I /fast/scratch/hyaku/mado-r51/MutC1Whitespace/punctuation-only-repo/quality/counters/c1-r51-ledger.py --repo /fast/scratch/hyaku/mado-r51/MutC1Whitespace/punctuation-only-repo --rev 56026fcb9800370ae04bc65952a6567181c398d0 --work /fast/scratch/hyaku/mado-r51/MutC1Whitespace/punctuation-only`
- Exit: 0
- stdout:
```
detail: checker selftest ok (ratio=50/50 form=with-work)
detail: checker ledger ok (rev=56026fcb9800370ae04bc65952a6567181c398d0)
C1_R51: population=82 ledger_rows=82 uncovered=0 dangling=0 bad_pointer=0 empty_desc=0 selftest=ok verdict=TARGET_MET rev=56026fcb9800370ae04bc65952a6567181c398d0
```
- stderr:
```

```
- SHA256 pristine=df5b3705d0291f967c35f0d69d6a908fe37a30d35e84599c4c0f897ca6469e0b; mutated=cba212bb5091b5f6a2f4d95a23882bb1800901c628ec3dd588224c5bebf66c17; restored=df5b3705d0291f967c35f0d69d6a908fe37a30d35e84599c4c0f897ca6469e0b; restored_exact=True

### duplicate-row
- Mutation: Duplicate an existing population row.
- Command: `python3 -I /fast/scratch/hyaku/mado-r51/MutC1Whitespace/duplicate-row-repo/quality/counters/c1-r51-ledger.py --repo /fast/scratch/hyaku/mado-r51/MutC1Whitespace/duplicate-row-repo --rev 56026fcb9800370ae04bc65952a6567181c398d0 --work /fast/scratch/hyaku/mado-r51/MutC1Whitespace/duplicate-row`
- Exit: 0
- stdout:
```
detail: checker selftest ok (ratio=50/50 form=with-work)
detail: checker ledger ok (rev=56026fcb9800370ae04bc65952a6567181c398d0)
C1_R51: population=82 ledger_rows=82 uncovered=0 dangling=0 bad_pointer=0 empty_desc=0 selftest=ok verdict=TARGET_MET rev=56026fcb9800370ae04bc65952a6567181c398d0
```
- stderr:
```

```
- SHA256 pristine=df5b3705d0291f967c35f0d69d6a908fe37a30d35e84599c4c0f897ca6469e0b; mutated=b33e6b86cba16e6ee1fcd044b2e60179334956b46bb5d88eaebf677feb1feda4; restored=df5b3705d0291f967c35f0d69d6a908fe37a30d35e84599c4c0f897ca6469e0b; restored_exact=True

### removed-row
- Mutation: Remove an existing population row.
- Command: `python3 -I /fast/scratch/hyaku/mado-r51/MutC1Whitespace/removed-row-repo/quality/counters/c1-r51-ledger.py --repo /fast/scratch/hyaku/mado-r51/MutC1Whitespace/removed-row-repo --rev 56026fcb9800370ae04bc65952a6567181c398d0 --work /fast/scratch/hyaku/mado-r51/MutC1Whitespace/removed-row`
- Exit: 0
- stdout:
```
detail: checker selftest ok (ratio=50/50 form=with-work)
detail: checker ledger ok (rev=56026fcb9800370ae04bc65952a6567181c398d0)
C1_R51: population=82 ledger_rows=82 uncovered=0 dangling=0 bad_pointer=0 empty_desc=0 selftest=ok verdict=TARGET_MET rev=56026fcb9800370ae04bc65952a6567181c398d0
```
- stderr:
```

```
- SHA256 pristine=df5b3705d0291f967c35f0d69d6a908fe37a30d35e84599c4c0f897ca6469e0b; mutated=933c73cdf437e850acb73c9f666fff4d63fe5e83e382adc65781bf4d2bd36ae4; restored=df5b3705d0291f967c35f0d69d6a908fe37a30d35e84599c4c0f897ca6469e0b; restored_exact=True
