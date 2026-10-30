# Survivor → fixture → kill

| Target/id | Fixture or detector | Pristine / mutant / restored | Verdict and level |
|---|---|---|---|
| harness/M13 | `suite/harness_killers.py:kill_M13` | PASS / FAIL / PASS | KILLED — unit/control-shape assertion |
| harness/M15 | `suite/harness_killers.py:kill_M15` | PASS / FAIL / PASS | KILLED — unit/control-shape assertion |
| harness/M24 | `suite/harness_killers.py:kill_M24` | PASS / FAIL / PASS | KILLED — unit/control-shape assertion |
| harness/M25 | `suite/harness_killers.py:kill_M25` | PASS / FAIL / PASS | KILLED — unit/control-shape assertion |
| harness/M26 | `suite/harness_killers.py:kill_M26` | PASS / FAIL / PASS | KILLED — unit/control-shape assertion |
| harness/M27 | `suite/harness_killers.py:kill_M27` | PASS / FAIL / PASS | KILLED — unit/control-shape assertion |
| harness/M29 | `suite/harness_killers.py:kill_M29` | PASS / FAIL / PASS | KILLED — unit/control-shape assertion |
| harness/M30 | `suite/harness_killers.py:kill_M30` | PASS / FAIL / PASS | KILLED — unit/control-shape assertion |
| harness/M32 | `suite/harness_killers.py:kill_M32` | PASS / FAIL / PASS | KILLED — unit/control-shape assertion |
| harness/M52 | `suite/harness_killers.py:kill_M52` | PASS / FAIL / PASS | KILLED — unit/control-shape assertion |
| harness/M36 | `suite/harness_killers.py:kill_M36` | PASS / FAIL / PASS | KILLED — control FAIL / effectiveness rejection |
| harness/M37 | `suite/harness_killers.py:kill_M37` | PASS / FAIL / PASS | KILLED — control FAIL / effectiveness rejection |
| harness/M38 | `suite/harness_killers.py:kill_M38` | PASS / FAIL / PASS | KILLED — control FAIL / effectiveness rejection |
| harness/M44 | `suite/harness_killers.py:kill_M44` | PASS / FAIL / PASS | KILLED — diagnostic |
| counter/CM01 | `suite/fixtures/counter/CM01.diff` | PASS / FAIL / PASS | KILLED — missed-leg |
| counter/CM03 | `suite/fixtures/counter/CM03.diff` | PASS / FAIL / PASS | KILLED — missed-leg |
| counter/CM04 | `suite/fixtures/counter/CM04.diff` | PASS / FAIL / PASS | KILLED — missed-leg |
| counter/CM06 | `suite/fixtures/counter/CM06.diff` | PASS / FAIL / PASS | KILLED — false-positive dangling |
| counter/CM07 | `suite/fixtures/counter/CM07.diff` | PASS / FAIL / PASS | KILLED — false-positive dangling |
| counter/CM08 | `suite/fixtures/counter/CM08.diff` | PASS / FAIL / PASS | KILLED — false-positive dangling |
| counter/CM11 | `suite/fixtures/counter/CM11.diff` | PASS / FAIL / PASS | KILLED — population/count |
| counter/CM12 | `suite/fixtures/counter/CM12.diff` | PASS / FAIL / PASS | KILLED — population/count |
| counter/CM19 | `suite/fixtures/counter/CM19.diff` | PASS / FAIL / PASS | KILLED — fail-closed |
| counter/CM25 | `suite/fixtures/counter/CM25.diff` | PASS / FAIL / PASS | KILLED — population/count |
| counter/CM28 | `suite/fixtures/counter/CM28.diff` | PASS / FAIL / PASS | KILLED — missed-leg |
| harness/M10 | Real-counter stdout+stderr comparison | identical to pristine | SURVIVED; prior equivalence argument, run-conditioned for M50 |
| harness/M12 | Real-counter stdout+stderr comparison | identical to pristine | SURVIVED; prior equivalence argument, run-conditioned for M50 |
| harness/M23 | Real-counter stdout+stderr comparison | identical to pristine | SURVIVED; prior equivalence argument, run-conditioned for M50 |
| harness/M31 | Real-counter stdout+stderr comparison | identical to pristine | SURVIVED; prior equivalence argument, run-conditioned for M50 |
| harness/M33 | Real-counter stdout+stderr comparison | identical to pristine | SURVIVED; prior equivalence argument, run-conditioned for M50 |
| harness/M35 | Real-counter stdout+stderr comparison | identical to pristine | SURVIVED; prior equivalence argument, run-conditioned for M50 |
| harness/M41 | Real-counter stdout+stderr comparison | identical to pristine | SURVIVED; prior equivalence argument, run-conditioned for M50 |
| harness/M43 | Real-counter stdout+stderr comparison | identical to pristine | SURVIVED; prior equivalence argument, run-conditioned for M50 |
| harness/M47 | Real-counter stdout+stderr comparison | identical to pristine | SURVIVED; prior equivalence argument, run-conditioned for M50 |
| harness/M49 | Real-counter stdout+stderr comparison | identical to pristine | SURVIVED; prior equivalence argument, run-conditioned for M50 |
| harness/M50 | Real-counter stdout+stderr comparison | identical to pristine | SURVIVED; prior equivalence argument, run-conditioned for M50 |
| counter/CM27 | Real git name domain; forged-git attempt | no distinguishing tree fixture | SURVIVED — unreachable 39-hex name with real git |
