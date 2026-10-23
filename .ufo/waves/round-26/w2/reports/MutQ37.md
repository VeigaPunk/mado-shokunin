# MutQ37 — population-checker mutation probe

## Verdict

`MUTQ37 fixtures: KILLED 3/6, SURVIVED 3/6, INCONCLUSIVE 0/6; fixtures + supplemental witnesses: KILLED 6/6.`

The on-disk population fixtures miss **counting CASE anywhere (M2), checking only the first PRED summary (M4), and returning success on an unparseable receipt (M6)**. Three separate scratch witnesses expose those defects without changing the checker contract. No checker or fixture repair was made.

The unchanged checker accepts both committed before receipts, separately and together: C1 population **41**, C2 population **51**, process exit **0** in all three invocations. This verifies population equality, not either claim's target success.

## Scope and method

Axes: defect sensitivity, pristine/restored reproducibility, and host/lane safety.

Target: `.ufo/waves/round-26/quality/check-population.py` (W1 Q37Population). All mutations were confined to six independent copies under `/fast/scratch/hyaku/mado-r26/MutQ37/mutants/`. Registration, all five fixture files, and the two committed before receipts were snapshotted before testing. Original lane inputs were not edited.

Each mutant changes one behavior-bearing point. The **same fixed eight-case detector** ran on each copy's pristine, mutated, and restored bytes. Its assertions require the expected process status, matching final `exit=N`, matching final `POPULATION verdict=...`, no stderr, and no timeout. All 48 pristine checks and all 48 restored checks passed. A killed mutant requires those baseline/restoration passes, a different mutant hash, and a behavioral assertion failure on the mutated copy. No baseline failure was credited as a kill.

Every checker invocation used `timeout --kill-after=1 5 prlimit --as=4000000000 -- python3 -I ...`; the driver additionally imposed an eight-second child wait and killed the child's process group on overrun. There were **147 checker invocations**: 6 copies × 8 cases × 3 byte states, plus three runs on the original lane checker and committed receipts. All completed without stderr or timeout. All children were waited for; no service or persistent process was started.

### Fixed detector cases

F1–F5 are byte-copies of the existing files under `quality/population-fixtures/`; they were not strengthened. Their registration is the round-26 registration except F4, which uses the existing red-registration fixture.

| ID | Registration / receipt | Expected process exit |
|---|---|---:|
| F1 | actual registration + `receipt-c1-green.txt` | 0 |
| F2 | actual registration + `receipt-red-case-removed.txt` | 1 |
| F3 | actual registration + `receipt-red-denominator.txt` | 1 |
| F4 | `registration-red-total.md` + `receipt-c1-green.txt` | 1 |
| F5 | actual registration + `receipt-red-selfconsistent-40.txt` | 1 |
| S1 | scratch total 2; one real CASE line and one `NOTE CASE ...` diagnostic; denominator 2 | 1 |
| S2 | scratch total 2; two CASE lines; first summary `2/2`, second summary `2/3` | 1 |
| S3 | scratch total 2; two CASE lines; only summary has `cases_pass=not-a-number` | 2 |

S1–S3 were created **before** the pristine run and included unchanged in every byte state. They exercise the existing contract: CASE lines start with CASE, every parsed summary must agree, and a receipt with no parseable population is unevaluable (`check-population.py:10-26,132-150,162-171`). They are scratch witnesses, not landed fixtures.

## Mutants and kill table

Line numbers refer to the pristine checker. K = behavioral detector kills; S = survives the five existing fixture cases. The output vectors are **actual process exit codes**, ordered F1–F5 and S1–S3 respectively.

| ID | Small defect | F1–F5 actual exits | Existing fixtures | S1–S3 actual exits | Supplemental kills |
|---|---|---|---|---|---|
| M1 | L145: `registered = populations[pred]` → `registered = den` (ignore the registered numeric total for known predicates) | `0 1 1 0 0` | K: F4, F5 | `1 1 2` | none |
| M2 | L45: `r"^CASE[ \t]"` → `r".*CASE[ \t]"` (match CASE anywhere in a line) | `0 1 1 1 1` | **S** | `0 1 2` | S1 |
| M3 | Remove L149–150, the denominator-versus-registration comparison (compare only CASE count and registered total) | `0 1 0 1 1` | K: F3 | `1 0 2` | S2 |
| M4 | L138: iterate `summaries[:1]` instead of `summaries` | `0 1 1 1 1` | **S** | `1 0 2` | S2 |
| M5 | L137: add 1 to the CASE-line tally | `1 0 1 1 1` | K: F1, F2 | `0 1 2` | S1 |
| M6 | L163: `verdict, rc = "UNREADABLE", 2` → `"UNREADABLE", 0` | `0 1 1 1 1` | **S** | `1 1 0` | S3 |

For **every** pristine and restored copy the actual vectors were `0 1 1 1 1` and `1 1 2`.

These verdicts distinguish the **fixture directory** from the whole historical W1 exercise: `w1/reports/Q37Population.md:59` also records an ad hoc nonexistent-receipt check, outside those five fixture cases. The M6 mutation reaches the same final unreadable-status branch; the fixture-only survival is not a claim that W1's separate missing-file command would miss M6.

### Actual distinguishing outputs

Full stdout, stderr, command arguments and process statuses for all 147 invocations are retained in the receipt files listed below. Selected actual output fields:

| Mutant / witness | Pristine → mutant → restored process exit | Mutated checker output |
|---|---|---|
| M1 / F4 | `1 → 0 → 1` | `cases_pass=41/41 case_lines=41 registered=41 agree=ok`; `POPULATION verdict=PASS receipts=1 agree=1 mismatch=0 unreadable=0`; `exit=0` |
| M1 / F5 | `1 → 0 → 1` | `cases_pass=40/40 case_lines=40 registered=40 agree=ok`; final PASS, `exit=0` |
| M2 / S1 | `1 → 0 → 1` | `cases_pass=1/2 case_lines=2 registered=2 agree=ok`; final PASS, `exit=0` |
| M3 / F3 | `1 → 0 → 1` | `cases_pass=41/42 case_lines=41 registered=41 agree=ok`; final PASS, `exit=0` |
| M4 / S2 | `1 → 0 → 1` | Prints only the agreeing `cases_pass=2/2` summary; `POPULATION verdict=PASS receipts=1 agree=1 mismatch=0 unreadable=0`; `exit=0` |
| M5 / F1 | `0 → 1 → 0` | `cases_pass=41/41 case_lines=42 registered=41 agree=MISMATCH legs=case_lines`; final FAIL, `exit=1` |
| M5 / F2 | `1 → 0 → 1` | `cases_pass=41/41 case_lines=41 registered=41 agree=ok`; final PASS, `exit=0` |
| M6 / S3 | `2 → 0 → 2` | `reason=no PRED-... cases_pass=N/T summary line`; `POPULATION verdict=UNREADABLE receipts=1 agree=0 mismatch=0 unreadable=1`; `exit=0` |

For S1, the pristine/restored checker reports `case_lines=1 registered=2 agree=MISMATCH legs=case_lines`. For S2, it evaluates both summaries and reports `cases_pass=2/3 case_lines=2 registered=2 agree=MISMATCH legs=denominator`. For S3, it reports the same unreadable reason but correctly finishes `exit=2`.

The three fixture survivors are coverage findings, not grounds to weaken the contract. The scratch witnesses demonstrate reachability of all three missed behaviors. No supplemental survivor remained among these six mutations; this is not an exhaustive mutation claim.

## Committed round-26 before receipts

The **original lane checker**, not a mutant, was run directly on the two original evidence files and the original registration. Complete individual stdout:

```text
POPULATION registration=/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-26/registration.md predicates=PRED-C1-r26,PRED-C1-r26-v2,PRED-C2-r26
POPULATION receipt=/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-26/evidence/c1-before-96101be5.txt pred=PRED-C1-r26 cases_pass=0/41 case_lines=41 registered=41 agree=ok
POPULATION verdict=PASS receipts=1 agree=1 mismatch=0 unreadable=0
exit=0
```

Actual process exit: **0**; stderr empty.

```text
POPULATION registration=/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-26/registration.md predicates=PRED-C1-r26,PRED-C1-r26-v2,PRED-C2-r26
POPULATION receipt=/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-26/evidence/c2-before-96101be5.txt pred=PRED-C2-r26 cases_pass=22/51 case_lines=51 registered=51 agree=ok
POPULATION verdict=PASS receipts=1 agree=1 mismatch=0 unreadable=0
exit=0
```

Actual process exit: **0**; stderr empty. The combined invocation printed both agreeing population rows, then:

```text
POPULATION verdict=PASS receipts=2 agree=2 mismatch=0 unreadable=0
exit=0
```

Combined actual process exit: **0**; stderr empty. The C1 receipt remains the original `PRED-C1-r26` / counter-v1 before receipt; this run does not relabel it as v2 evidence or re-run either counter/oracle.

## Hashes and exact restoration

All six scratch copies had the same before **and** restored SHA-256:

```text
803e0096c994d301fa7fe9a9dd7e35255ee1f5bcf3f63d15956cdba8943d0f64
```

The unchanged lane checker had that hash before and after, with **7,499 bytes** in both states. The driver restored all six copies in a `finally` block by copying pristine bytes, then ran the identical eight-case detector on each restored copy. Direct byte comparisons recorded `exact_bytes_restored=true` for all six.

| Mutant | SHA-256 while mutated |
|---|---|
| M1 | `104125da9a8859af19ecb7ae88b667482dfa80ae7f8eab45933dec1b3fa10a07` |
| M2 | `d61abdca3634cb2622ffc42559c2aabdbf1f864769a4bd8c93278cb16e6b7b1a` |
| M3 | `c4d62c78a8b18742b390ce91ed4598f8e9cd8a5c74b73f7d6efa20e86fd4e06f` |
| M4 | `86f190e80f29b28da9a4fed52bb4e7cb32f5134167a80efe9ba40658807d340d` |
| M5 | `693fc87ccf0ab041242b315c381f5ad507cd5771a2f97cee2110458cb77123b3` |
| M6 | `aa8c8006f5cf3eabde8cb63093e09415aa480ce97e614b71ae9d61e614a93292` |

Other original input hashes, identical before and after (direct byte equality to their snapshots also true):

| Input | Bytes | Before = after SHA-256 |
|---|---:|---|
| `registration.md` | 12447 | `1fa28245f34b48bae4200ad0485e9956799861f3441b5e5d61e43c87f0b13e7f` |
| `evidence/c1-before-96101be5.txt` | 2738 | `55e1ddfaf9286852022e8c5120d74133d540b77f0f1a37f4b630906246bfd86e` |
| `evidence/c2-before-96101be5.txt` | 12478 | `63c0c1030fde5af98821b9bb53f0a39d60d0f8ea620202d167a76841e327aa4e` |
| `receipt-c1-green.txt` | 2419 | `45c04c00aea88e1ab71f8eb7c002748fd043bb7e1b7558e883b469ccf111e58f` |
| `receipt-red-case-removed.txt` | 2389 | `bbbeda734e73bdf3d6f98ac6a56a98335de91614bda143f2740a8af60c62bf8d` |
| `receipt-red-denominator.txt` | 2419 | `21e47a997ca2e2d8797e518566cd644388a2956481b63ae1f70452e31fff8041` |
| `registration-red-total.md` | 9574 | `3cc95b6d37f003aeea6927686cc6de13dcda0cb9646a15ce25fc0a7233527d07` |
| `receipt-red-selfconsistent-40.txt` | 2389 | `89043adaa73bde06d09a35b0d69e07b8b7ca915c48078eac33d371cad2625512` |

## Commands and receipt paths

Preparation, copying and execution are in the retained standard-library driver `/fast/scratch/hyaku/mado-r26/MutQ37/probe.py`. It makes no textual checker edits. The six mutations above were applied with the surgical edit tool between these two commands, run from the lane root:

```text
env -u WAYLAND_DISPLAY -u HYPRLAND_INSTANCE_SIGNATURE timeout --kill-after=2 120 prlimit --as=4000000000 -- python3 -I /fast/scratch/hyaku/mado-r26/MutQ37/probe.py baseline
env -u WAYLAND_DISPLAY -u HYPRLAND_INSTANCE_SIGNATURE timeout --kill-after=2 120 prlimit --as=4000000000 -- python3 -I /fast/scratch/hyaku/mado-r26/MutQ37/probe.py mutate-restore
```

Observed driver output ended:

```text
BASELINE_DETECTOR=PASS
```

and:

```text
MUTANT=M6-parse-exit-zero FIXTURES=SURVIVED FULL=KILLED
LANE_EXACT_BYTES_UNCHANGED=True SCRATCH_EXACT_BYTES_RESTORED=True
```

Each checker child's **exact command argument list**, captured stdout/stderr, expected and actual process exits, timeout flag and detector result is stored in:

- `/fast/scratch/hyaku/mado-r26/MutQ37/logs/baseline.json`
- `/fast/scratch/hyaku/mado-r26/MutQ37/logs/mutated.json`
- `/fast/scratch/hyaku/mado-r26/MutQ37/logs/restored.json`
- `/fast/scratch/hyaku/mado-r26/MutQ37/logs/committed-before.json`

Hash/verdict receipts:

- `/fast/scratch/hyaku/mado-r26/MutQ37/logs/manifest.json`
- `/fast/scratch/hyaku/mado-r26/MutQ37/logs/results.json`
- `/fast/scratch/hyaku/mado-r26/MutQ37/logs/restoration.json`

The four supplemental input files are retained under `/fast/scratch/hyaku/mado-r26/MutQ37/inputs/` (`registration-probe.md`, `receipt-probe-case-anywhere.txt`, `receipt-probe-second-summary.txt`, `receipt-probe-unparseable.txt`). Source snapshots and restored copies remain there for inspection.

Before scratch writes, `df -h /fast` reported 146G available (82% used). No tools were installed or updated. No git/jj command, subagent, other model runtime, compositor/oracle, live-session operation, device node, service restart or package transaction was used. Child environments were explicit and contained neither WAYLAND_DISPLAY nor HYPRLAND_INSTANCE_SIGNATURE. The only lane write was this requested report.
