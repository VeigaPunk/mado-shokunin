# survivor distinguishing-input evidence

## range-slice-offbyone
input: ['`epsilon` at `rec.cpp:9`']
expectation: last receipt line (9 = int epsilon = 9;) is never citable in the mutant
```
--- pristine ---
rc=0
LOC /tmp/mutprobe.t5_ar_m6/prose-range-slice-offbyone.md:1 rec.cpp:9 fragments=1 supported=1 verdict=OK
CHECK_LOCATORS: locators=1 miss=0
--- mutant range-slice-offbyone ---
rc=1
LOC /tmp/mutprobe.t5_ar_m6/prose-range-slice-offbyone.md:1 rec.cpp:9 fragments=1 supported=0 verdict=MISS
CHECK_LOCATORS: locators=1 miss=1
```

## token-len-4
input: ['`foo` at `rec.cpp:2`']
expectation: 3-char token foo absent from line 2: pristine MISS, mutant NOFRAG
```
--- pristine ---
rc=1
LOC /tmp/mutprobe.t5_ar_m6/prose-token-len-4.md:1 rec.cpp:2 fragments=1 supported=0 verdict=MISS
CHECK_LOCATORS: locators=1 miss=1
--- mutant token-len-4 ---
rc=0
LOC /tmp/mutprobe.t5_ar_m6/prose-token-len-4.md:1 rec.cpp:2 fragments=0 supported=0 verdict=NOFRAG
CHECK_LOCATORS: locators=1 miss=0
```

## token-lower-boundary
input: ['`lpha` at `rec.cpp:2`']
expectation: lpha occurs only inside alpha: pristine MISS, mutant OK
```
--- pristine ---
rc=1
LOC /tmp/mutprobe.t5_ar_m6/prose-token-lower-boundary.md:1 rec.cpp:2 fragments=1 supported=0 verdict=MISS
CHECK_LOCATORS: locators=1 miss=1
--- mutant token-lower-boundary ---
rc=0
LOC /tmp/mutprobe.t5_ar_m6/prose-token-lower-boundary.md:1 rec.cpp:2 fragments=1 supported=1 verdict=OK
CHECK_LOCATORS: locators=1 miss=0
```

## attr-before-inclusive
input: ['`alpha`rec.cpp:2']
expectation: fragment ends exactly at locator start: pristine OK, mutant NOFRAG
```
--- pristine ---
rc=0
LOC /tmp/mutprobe.t5_ar_m6/prose-attr-before-inclusive.md:1 rec.cpp:2 fragments=1 supported=1 verdict=OK
CHECK_LOCATORS: locators=1 miss=0
--- mutant attr-before-inclusive ---
rc=0
LOC /tmp/mutprobe.t5_ar_m6/prose-attr-before-inclusive.md:1 rec.cpp:2 fragments=1 supported=1 verdict=NOFRAG
CHECK_LOCATORS: locators=1 miss=0
```

## attr-after-exclusive
input: ['rec.cpp:2`alpha`']
expectation: fragment starts exactly at locator end: pristine OK, mutant NOFRAG
```
--- pristine ---
rc=0
LOC /tmp/mutprobe.t5_ar_m6/prose-attr-after-exclusive.md:1 rec.cpp:2 fragments=1 supported=1 verdict=OK
CHECK_LOCATORS: locators=1 miss=0
--- mutant attr-after-exclusive ---
rc=0
LOC /tmp/mutprobe.t5_ar_m6/prose-attr-after-exclusive.md:1 rec.cpp:2 fragments=1 supported=1 verdict=NOFRAG
CHECK_LOCATORS: locators=1 miss=0
```

## id-re-digit-lead
input: ['value `123` at `plain.conf:2`']
expectation: digit-leading token 123: pristine NOFRAG (no tokens), mutant MISS
```
--- pristine ---
rc=0
LOC /tmp/mutprobe.t5_ar_m6/prose-id-re-digit-lead.md:1 plain.conf:2 fragments=0 supported=0 verdict=NOFRAG
CHECK_LOCATORS: locators=1 miss=0
--- mutant id-re-digit-lead ---
rc=1
LOC /tmp/mutprobe.t5_ar_m6/prose-id-re-digit-lead.md:1 plain.conf:2 fragments=1 supported=0 verdict=MISS
CHECK_LOCATORS: locators=1 miss=1
```

## locator-no-lookbehind
input: ['-rec.cpp:2']
expectation: preceding '-' blocks a start at 'r' in pristine (name cannot start with '-'): pristine locators=0, mutant matches rec.cpp:2 mid-word
```
--- pristine ---
rc=0
CHECK_LOCATORS: locators=0 miss=0
--- mutant locator-no-lookbehind ---
rc=0
LOC /tmp/mutprobe.t5_ar_m6/prose-locator-no-lookbehind.md:1 rec.cpp:2 fragments=0 supported=0 verdict=NOFRAG
CHECK_LOCATORS: locators=1 miss=0
```

## locator-no-lookahead
input: ['`alpha` at rec.cpp:2x']
expectation: range bleeds into x: pristine locators=0, mutant checks rec.cpp:2
```
--- pristine ---
rc=0
CHECK_LOCATORS: locators=0 miss=0
--- mutant locator-no-lookahead ---
rc=0
LOC /tmp/mutprobe.t5_ar_m6/prose-locator-no-lookahead.md:1 rec.cpp:2 fragments=1 supported=1 verdict=OK
CHECK_LOCATORS: locators=1 miss=0
```

## no-re-escape
no distinguishing input exists today; classification: equivalent by construction: fragment_tokens only returns ID_RE matches, i.e. strings over [A-Za-z0-9_], and re.escape is the identity on exactly that set (verified by enumeration in this probe), so the mutated regex string equals the original for every reachable token

## summary-swapped
input: ['`beta` at `rec.cpp:2`', '`alpha` at `rec.cpp:5`']
expectation: two locators one miss: pristine locators=2 miss=1, mutant locators=1 miss=2
```
--- pristine ---
rc=1
LOC /tmp/mutprobe.t5_ar_m6/prose-summary-swapped.md:1 rec.cpp:2 fragments=1 supported=0 verdict=MISS
LOC /tmp/mutprobe.t5_ar_m6/prose-summary-swapped.md:2 rec.cpp:5 fragments=1 supported=1 verdict=OK
CHECK_LOCATORS: locators=2 miss=1
--- mutant summary-swapped ---
rc=1
LOC /tmp/mutprobe.t5_ar_m6/prose-summary-swapped.md:1 rec.cpp:2 fragments=1 supported=0 verdict=MISS
LOC /tmp/mutprobe.t5_ar_m6/prose-summary-swapped.md:2 rec.cpp:5 fragments=1 supported=1 verdict=OK
CHECK_LOCATORS: locators=1 miss=2
```

## teeth-one-direction
no distinguishing input exists today; classification: equivalent on every current input: the flipped run of the frozen 18-case table always breaks both ways (measured constants flips=11 ok_to_miss=4 miss_to_ok=5, all > 0), so the removed ok_to_miss/miss_to_ok clauses are tautologies today; latent missing assertion - a future table whose flip is one-directional would now pass selftest

## selftest-min-cases-dropped
no distinguishing input exists today; classification: equivalent on every current input: the frozen CASES table has k=18 >= 12, so the removed k >= 12 clause is a tautology today; latent missing assertion - a future table shorter than 12 cases would now pass selftest

## no-re-escape mechanical check
re.escape != identity on 0 of 254079 word-char strings of length 1-3
