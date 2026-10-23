# ExecQ37Checker — round 28 wave 2

Axis: C1 operability, Q37 registered-target/population agreement.

## Change

Repaired only `quality/check-population.py`: opened the Round-28 docstring on line 2 and removed the stale concatenated draft from old lines 296–434. The retained first draft is the full checker; its existing supported forms evaluate `green=all`, `h_killed>=ceil(0.75*h_valid)`, exact `cases_pass=N/T` with CASE count/registered total, and bare `>=` ratios. No target forms or other features were added. The first edit was rejected because its deletion range extended beyond the displayed lines; I reread the tail and reapplied the same scoped repair.

## Evidence

Commands ran from `/home/vgpnk/Projects/shokunin/mado-shokunin`. `SHELL_RC` below is the checker process exit code captured after each invocation.

Required Round-27 command:
```text
$ python3 -I quality/check-population.py --registration .ufo/waves/round-27/registration.md .ufo/waves/round-27/evidence/c2-after-0b53bd86.txt
POPULATION receipt=.ufo/waves/round-27/evidence/c2-after-0b53bd86.txt pred=PRED-C2-r27-v2 cases_pass=- case_lines=50 registered=- agree=ok
POPULATION verdict=PASS receipts=1 agree=1 mismatch=0 unreadable=0
exit=0
SHELL_RC=0
```

Frozen artifact:
```text
$ sha256sum .ufo/waves/round-26/quality/check-population.py
803e0096c994d301fa7fe9a9dd7e35255ee1f5bcf3f63d15956cdba8943d0f64  .ufo/waves/round-26/quality/check-population.py
SHELL_RC=0
```

Synthetic registration and receipts are under `/fast/scratch/hyaku/mado-r28/ExecQ37Checker/`. The passing receipt checks all four forms together; each failing receipt alters only its named form. Exact commands and decisive output:
```text
$ python3 -I quality/check-population.py --registration /fast/scratch/hyaku/mado-r28/ExecQ37Checker/targets-registration.md /fast/scratch/hyaku/mado-r28/ExecQ37Checker/targets-pass.txt
POPULATION receipt=/fast/scratch/hyaku/mado-r28/ExecQ37Checker/targets-pass.txt pred=PRED-Q37-ALL cases_pass=- case_lines=3 registered=- agree=ok
POPULATION receipt=/fast/scratch/hyaku/mado-r28/ExecQ37Checker/targets-pass.txt pred=PRED-Q37-CEIL cases_pass=- case_lines=3 registered=- agree=ok
POPULATION receipt=/fast/scratch/hyaku/mado-r28/ExecQ37Checker/targets-pass.txt pred=PRED-Q37-CASES cases_pass=3/3 case_lines=3 registered=3 agree=ok
POPULATION receipt=/fast/scratch/hyaku/mado-r28/ExecQ37Checker/targets-pass.txt pred=PRED-Q37-RATIO cases_pass=- case_lines=3 registered=- agree=ok
POPULATION verdict=PASS receipts=1 agree=4 mismatch=0 unreadable=0; exit=0; SHELL_RC=0
$ python3 -I quality/check-population.py --registration /fast/scratch/hyaku/mado-r28/ExecQ37Checker/targets-registration.md /fast/scratch/hyaku/mado-r28/ExecQ37Checker/targets-fail-all.txt
POPULATION receipt=/fast/scratch/hyaku/mado-r28/ExecQ37Checker/targets-fail-all.txt pred=PRED-Q37-ALL cases_pass=- case_lines=3 registered=- agree=MISMATCH legs=green
POPULATION verdict=FAIL receipts=1 agree=0 mismatch=1 unreadable=0; exit=1; SHELL_RC=1
$ python3 -I quality/check-population.py --registration /fast/scratch/hyaku/mado-r28/ExecQ37Checker/targets-registration.md /fast/scratch/hyaku/mado-r28/ExecQ37Checker/targets-fail-ceil.txt
POPULATION receipt=/fast/scratch/hyaku/mado-r28/ExecQ37Checker/targets-fail-ceil.txt pred=PRED-Q37-CEIL cases_pass=- case_lines=3 registered=- agree=MISMATCH legs=h_killed
POPULATION verdict=FAIL receipts=1 agree=0 mismatch=1 unreadable=0; exit=1; SHELL_RC=1
$ python3 -I quality/check-population.py --registration /fast/scratch/hyaku/mado-r28/ExecQ37Checker/targets-registration.md /fast/scratch/hyaku/mado-r28/ExecQ37Checker/targets-fail-cases.txt
POPULATION receipt=/fast/scratch/hyaku/mado-r28/ExecQ37Checker/targets-fail-cases.txt pred=PRED-Q37-CASES cases_pass=2/3 case_lines=3 registered=3 agree=MISMATCH legs=cases_pass
POPULATION verdict=FAIL receipts=1 agree=0 mismatch=1 unreadable=0; exit=1; SHELL_RC=1
$ python3 -I quality/check-population.py --registration /fast/scratch/hyaku/mado-r28/ExecQ37Checker/targets-registration.md /fast/scratch/hyaku/mado-r28/ExecQ37Checker/targets-fail-ratio.txt
POPULATION receipt=/fast/scratch/hyaku/mado-r28/ExecQ37Checker/targets-fail-ratio.txt pred=PRED-Q37-RATIO cases_pass=- case_lines=3 registered=- agree=MISMATCH legs=killed
POPULATION verdict=FAIL receipts=1 agree=0 mismatch=1 unreadable=0; exit=1; SHELL_RC=1
```

Negative controls:
```text
$ python3 -I quality/check-population.py --registration .ufo/waves/round-27/registration.md /fast/scratch/hyaku/mado-r28/ExecQ37Checker/r27-mutated-number.txt
POPULATION receipt=/fast/scratch/hyaku/mado-r28/ExecQ37Checker/r27-mutated-number.txt pred=PRED-C2-r27-v2 cases_pass=- case_lines=50 registered=- agree=MISMATCH legs=green; verdict=FAIL; exit=1; SHELL_RC=1
$ python3 -I quality/check-population.py --registration .ufo/waves/round-27/registration.md /fast/scratch/hyaku/mado-r28/ExecQ37Checker/r27-unregistered-pred.txt
POPULATION receipt=/fast/scratch/hyaku/mado-r28/ExecQ37Checker/r27-unregistered-pred.txt pred=PRED-C2-absent cases_pass=- case_lines=50 registered=- agree=MISMATCH legs=registration_total; verdict=FAIL; exit=1; SHELL_RC=1
$ python3 -I quality/check-population.py --registration .ufo/waves/round-27/registration.md /fast/scratch/hyaku/mado-r28/ExecQ37Checker/missing-receipt.txt
POPULATION receipt=/fast/scratch/hyaku/mado-r28/ExecQ37Checker/missing-receipt.txt verdict=UNREADABLE error=FileNotFoundError
POPULATION verdict=UNREADABLE receipts=1 agree=0 mismatch=0 unreadable=1; exit=2; SHELL_RC=2
```

Round-26 matrix replay with the successor (same registration/fixture paths as `quality/q37-population-red-green.txt`):
```text
$ python3 -I quality/check-population.py --registration .ufo/waves/round-26/registration.md .ufo/waves/round-26/quality/population-fixtures/receipt-c1-green.txt
POPULATION receipt=...receipt-c1-green.txt pred=PRED-C1-r26 cases_pass=41/41 case_lines=41 registered=41 agree=ok; verdict=PASS; exit=0; SHELL_RC=0
$ python3 -I quality/check-population.py --registration .ufo/waves/round-26/registration.md .ufo/waves/round-26/quality/population-fixtures/receipt-red-case-removed.txt
POPULATION receipt=...receipt-red-case-removed.txt pred=PRED-C1-r26 cases_pass=41/41 case_lines=40 registered=41 agree=MISMATCH legs=case_lines; verdict=FAIL; exit=1; SHELL_RC=1
$ python3 -I quality/check-population.py --registration .ufo/waves/round-26/registration.md .ufo/waves/round-26/quality/population-fixtures/receipt-red-denominator.txt
POPULATION receipt=...receipt-red-denominator.txt pred=PRED-C1-r26 cases_pass=41/42 case_lines=41 registered=41 agree=MISMATCH legs=denominator,cases_pass; verdict=FAIL; exit=1; SHELL_RC=1
$ python3 -I quality/check-population.py --registration .ufo/waves/round-26/quality/population-fixtures/registration-red-total.md .ufo/waves/round-26/quality/population-fixtures/receipt-c1-green.txt
POPULATION receipt=...receipt-c1-green.txt pred=PRED-C1-r26 cases_pass=41/41 case_lines=41 registered=42 agree=MISMATCH legs=denominator,case_lines,cases_pass; verdict=FAIL; exit=1; SHELL_RC=1
$ python3 -I quality/check-population.py --registration .ufo/waves/round-26/registration.md .ufo/waves/round-26/quality/population-fixtures/receipt-red-selfconsistent-40.txt
POPULATION receipt=...receipt-red-selfconsistent-40.txt pred=PRED-C1-r26 cases_pass=40/40 case_lines=40 registered=41 agree=MISMATCH legs=denominator,case_lines,cases_pass; verdict=FAIL; exit=1; SHELL_RC=1
$ python3 -I quality/check-population.py --registration .ufo/waves/round-26/registration.md .ufo/waves/round-26/evidence/c1-before-96101be5.txt
POPULATION receipt=...c1-before-96101be5.txt pred=PRED-C1-r26 cases_pass=0/41 case_lines=41 registered=41 agree=MISMATCH legs=cases_pass; verdict=FAIL; exit=1; SHELL_RC=1
$ python3 -I quality/check-population.py --registration .ufo/waves/round-26/registration.md .ufo/waves/round-26/evidence/c2-before-96101be5.txt
POPULATION receipt=...c2-before-96101be5.txt pred=PRED-C2-r26 cases_pass=22/51 case_lines=51 registered=51 agree=MISMATCH legs=cases_pass; verdict=FAIL; exit=1; SHELL_RC=1
$ python3 -I quality/check-population.py --registration .ufo/waves/round-26/registration.md .ufo/waves/round-26/quality/population-fixtures/missing-receipt.txt
POPULATION receipt=...missing-receipt.txt verdict=UNREADABLE error=FileNotFoundError
POPULATION verdict=UNREADABLE receipts=1 agree=0 mismatch=0 unreadable=1; exit=2; SHELL_RC=2
```

## Failed acceptance / risk

The stored r26 matrix expects both pre-fix evidence receipts (0/41 and 22/51) to PASS because the r26 checker checked population only. The requested exact `cases_pass=N/T` behavior compares the numerator too, so the successor correctly rejects those receipts against r26's registered 41/41 and 51/51 targets. Thus 6/8 r26 matrix verdicts match, but the two historical baseline verdicts do not; making them PASS would contradict the explicit exact-numerator requirement. No path/round-specific exception was added. This is the one unmet acceptance item to resolve at integration.

Files written: `quality/check-population.py`; this report; scratch files `targets-registration.md`, `targets-pass.txt`, `targets-fail-{all,ceil,cases,ratio}.txt`, `r27-mutated-number.txt`, and `r27-unregistered-pred.txt`. No tool installed. LSP was not available in the exposed tool inventory; no symbol refactor was needed.
