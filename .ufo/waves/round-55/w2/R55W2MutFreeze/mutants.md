# R55W2MutFreeze -- mutation test of `quality/check-freeze-order.py`

Lane revision: `57584ed67716340b3d466fa04333ac0bab3fb79e`. Baseline instrument: `quality/check-freeze-order.py`
(sha256 `83d9eb2a2228d7dbf6eff628ea188d087046607bf98111ecec60efbec6038474`, copy in `receipts/baseline-check-freeze-order.py`).

## Method (what ran, what did not)

- Every mutant is a one-edit copy of the baseline, made in scratch (`/fast/scratch/hyaku/mado-r55/R55W2MutFreeze/mut/`).
  Nothing in the lane was edited; no lane git mutation was run. Mutant sources are in `mutants/M01.py`..`M17.py`,
  unified diffs in `mutants/M01.diff`..`M17.diff`. M06 is a 3-line insertion; M07 is a 2-line edit (regex + None branch) = 4 changed lines in the diff; all others are one line.
- Each mutant was scored three ways:
  1. **Instrument selftest** `python3 -I Mxx.py --selftest --work <scratch>` (baseline: rc 0, `MADO_FREEZE_ORDER_SELFTEST: OK`, 16 PASS).
  2. **Real runs** against a bare clone of the lane at `57584ed6` (`lane.git`, objects identical to the lane):
     `python3 -I Mxx.py --repo lane.git --rev 57584ed6... --round R --wave W --work <scratch>`
     Required: round 54 w1 = FAIL (rc 1), round 54 w2 = OK (rc 0), round 55 w1 = OK (rc 0). Baseline reads confirmed:
     - `round=54 wave=w1 freeze=350d30e4ec55 freeze_time=2026-10-27T14:11:10-03:00 launch=2026-10-27T17:05:25.338Z verdict=FAIL reason=freeze_after_launch` (rc 1)
     - `round=54 wave=w2 freeze=350d30e4ec55 freeze_time=2026-10-27T14:11:10-03:00 launch=2026-10-27T17:46:51.625Z verdict=OK reason=ok` (rc 0)
     - `round=55 wave=w1 freeze=54dacbd843d6 freeze_time=2026-10-28T18:46:52-03:00 launch=2026-10-28T21:50:15.231Z verdict=OK reason=ok` (rc 0)
  3. **Independent harness** `python3 -I quality/check-r55-controls.py --claim c1 --repo <scratch repo carrying Mxx at quality/check-freeze-order.py> --rev <commit> --work <scratch>`.
     The `--claim` value is the closest available entry point, not a claim for this instrument (the instruction said to ignore the placeholder). Baseline: `MADO_R55_CONTROLS: claim=c1 good=ok controls=7/7 verdict=OK`.
- The harness has no coupling to this instrument: `grep -ci freeze` over `quality/r55_ctl_c1.py`, `r55_ctl_c2.py`, `r55_ctl_c3.py` and `check-r55-controls.py` at `57584ed6` returns `0` for all four. It never reads or runs `check-freeze-order.py`, so its result is identical for every mutant (17/17, `controls=7/7 verdict=OK`, rc 0). It is recorded as "nothing" in every row; it is not a control for this instrument.
- Mutant selftests and real runs were executed with system `python3 -I` and host `git`. No tools were installed or upgraded for this seat.
- Not done: no mutant was run against a freshly built git repo of the full round-54/55 history other than the lane clone; no hyaku/fleet/sibling repo was touched.

## Table

Legend: "selftest" = instrument's own `--selftest` (FAIL = killed); "real" = the three real runs vs baseline (a change of verdict/rc = killed); harness = independent C1 harness (always unchanged, see above).

| mutant | edit (baseline line @57584ed6) | selftest | real runs 54w1 / 54w2 / 55w1 | harness c1 | killed by | survivor risk |
|---|---|---|---|---|---|---|
| M01 | author time instead of committer time: L140 `%cI` -> `%aI` | rc 1; FAIL: TRAP author 11:00Z<launch but committer 15:00Z; TRAP author 23:00Z>launch but committer 12:00Z | **54w1 FAIL->OK (rc 0)**, freeze_time 13:42:45-03:00; 54w2 OK (freeze_time changed); 55w1 OK (freeze_time changed) | nothing | selftest and real run (54w1) | none |
| M02 | compare `<=` instead of `<`: L164 | rc 1; FAIL: equal time -> FAIL | unchanged | nothing | selftest | low |
| M03 | drop freeze_edited blob comparison: L133 `edited = []` | rc 1; FAIL: freeze_edited:registration.md, freeze_edited:frozen-tables.json | unchanged | nothing | selftest | low |
| M04 | ignore first-parent restriction: L120 drop `--first-parent` | rc 1; FAIL: merged-in freeze (merge commit expected) | unchanged | nothing | selftest | low |
| M05 | drop `--full-history`: L120 | **rc 0, selftest OK** | unchanged | nothing | **nothing** | low: candidate-equivalent under `--first-parent`; 2 probe graphs identical (see below) |
| M06 | missing createdAt treated as OK: insert after L152 `if isinstance(doc, dict) and "createdAt" not in doc: verdict OK; return 0` | **rc 0, selftest OK** | unchanged | nothing | **nothing (SURVIVOR)** | HIGH: probe A false OK (see below) |
| M07 | parse createdAt without timezone, as UTC: L70 optional tz group; L75 `if tz in (None, "Z")` | **rc 0, selftest OK** | unchanged | nothing | **nothing (SURVIVOR)** | MEDIUM: probe B false OK (see below) |
| M08 | ignore committed offset: L80 fixed `"+00:00"` | rc 1; many FAIL (freeze_after_launch, equal time, TRAP) | **54w1 FAIL->OK** | nothing | selftest and real run (54w1) | none |
| M09 | string compare instead of datetime: L164 `ct < launch_raw` | rc 1; FAIL: freeze_after_launch, equal time, TRAP | **54w1 FAIL->OK** | nothing | selftest and real run (54w1) | none |
| M10 | last matching freeze commit instead of first: L132 `break` -> `pass` | rc 1; FAIL: edit-then-revert (freeze=aed7b39aba0e expected) | unchanged | nothing | selftest | low |
| M11 | drop registration.md from REQUIRED: L36 | rc 1; FAIL: no_freeze (registration.md absent) | unchanged | nothing | selftest | low |
| M12 | swallow git failure: L61 `if False and p.returncode != 0` | **rc 0, selftest OK** | unchanged on real runs; probe C: base `SETUP git_failed:ls-tree -z` rc 2 -> mutant `FAIL reason=no_freeze` rc 1 | nothing | **nothing (SURVIVOR)** | MEDIUM-LOW: error masked; no false OK found on the traced paths [INFERENCE from code] |
| M13 | updatedAt instead of createdAt: L153 | rc 1; many FAIL (createdAt-dependent cases) | unchanged (lane registries have updatedAt == createdAt) | nothing | selftest | low |
| M14 | launch read from hard-coded w1 registry: L146 `(tip, base, "w1")` | **rc 0, selftest OK** (selftest only ever uses w1) | **54w2 OK -> FAIL** (rc 1, freeze_after_launch, launch 17:05:25Z) | nothing | **real run only** | MEDIUM: any w2/w3 launch read is wrong and selftest does not see it |
| M15 | drop frozen-tables.json from freeze set: L116 `for n in REQUIRED` | rc 1; FAIL: freeze_edited:frozen-tables.json | unchanged | nothing | selftest | low |
| M16 | remove edited early return: L160 `return f, 1` -> `pass` | rc 1; FAIL: freeze_edited:registration.md, freeze_edited:frozen-tables.json | unchanged | nothing | selftest | low |
| M17 | first appearance as freeze anchor: L134 `anchor = first_any or freeze` | rc 1; FAIL: freeze_edited:registration.md (freeze field = 10:00 commit, expected 10:30) | unchanged | nothing | selftest | low |

Totals: 17 mutants. Killed by selftest: 12 (M01, M02, M03, M04, M08, M09, M10, M11, M13, M15, M16, M17). Killed only by real runs: 1 (M14), killed by both selftest and real runs: 3 (M01, M08, M09). Survivors (nothing catches): 4 (M05, M06, M07, M12). Harness control kills: 0 of 17.

## Survivors: what is unguarded, and the smallest kill test (text only)

**M06 -- registry without a `createdAt` key reads as OK (HIGH).**
Unguarded behaviour: a `swarm-registry.json` that parses but lacks `createdAt` should read `no_registry` (FAIL). The selftest only covers an absent file (case 6a) and an unparsable value `"yesterday"` (case 6b); a missing key is never fed.
Evidence (probe A, `receipts/probes-out.json` key `A_base_M06`): freeze committed 14:11:10-03:00 (17:11:10Z), registry `{"schema":"ufo-swarm-registry-v1","wave":"w1"}`:
- base: `... freeze=57ed6f3dc61f freeze_time=2026-10-27T14:11:10-03:00 launch=none verdict=FAIL reason=no_registry` rc 1
- M06: `... verdict=OK reason=ok` rc 0
Smallest kill test: selftest case 6c, FZ at 10:00-03:00, registry `json.dumps({"schema": "x"})`, expect regex `... launch=none verdict=FAIL reason=no_registry` and rc 1.

**M07 -- createdAt without a timezone is read as UTC (MEDIUM).**
Unguarded behaviour: `parse_iso` documents "ISO-8601 with Z or +hh:mm offset"; a naive timestamp must return None. Nothing feeds a naive timestamp.
Evidence (probe B, key `B_base_M07`): freeze 14:00-03:00 (17:00Z), registry `createdAt "2026-10-27T18:00:00"`:
- base: `... launch=none verdict=FAIL reason=no_registry` rc 1
- M07: `... launch=2026-10-27T18:00:00 verdict=OK reason=ok` rc 0
Smallest kill test: selftest case, same FZ commit, registry `createdAt "2026-10-27T14:00:00"` (naive), expect `launch=none verdict=FAIL reason=no_registry` rc 1.

**M12 -- swallowed git failure (MEDIUM-LOW).**
Unguarded behaviour: `git()` raising `Setup("git_failed:...")` is the only path that reports `SETUP` rc 2 for a failing git call. The selftest exercises only `rev-parse` (check=False) and a missing repo directory.
Evidence (probe C, key `C_base_M12`): delete the loose root-tree object of HEAD in a scratch repo:
- base: `MADO_FREEZE_ORDER: SETUP git_failed:ls-tree -z` rc 2
- M12: `... freeze=none freeze_time=none launch=none verdict=FAIL reason=no_freeze` rc 1
So the mutant misreports a repository error as a missing freeze. On the code paths I traced, a swallowed failure never yields `verdict=OK`: an empty `show -s` leaves `ct` empty and `parse_iso("")` is `None`, which crashes at the comparison rather than passing [INFERENCE from code, not executed].
Smallest kill test: `try: git(d, ["no-such-subcommand"], work)` must raise `Setup`; or the probe C corrupted-object repo must expect `SETUP git_failed:ls-tree -z` rc 2.

**M05 -- drop `--full-history` (LOW; candidate equivalent, not proven).**
Unguarded behaviour: none found. Two graphs were probed, both identical under base and M05:
- graph 1 (merge of a side branch carrying the freeze files, no main-line freeze): `log` lists only the merge; instrument `freeze=1960990452db ... verdict=FAIL reason=freeze_after_launch` (both).
- graph 2 (main freeze `claims` at 10:00, merge of side `new` resolved at 13:00): `log` lists merge and main commit; instrument `freeze=7b9370ae1aea ... reason=freeze_edited:claims-frozen.md` (both).
No killing test is proposed: a distinguishing graph would be a merge TREESAME to its second parent but not its first, under `--first-parent`, and neither probe produced one. Either document `--full-history` as a no-op under `--first-parent` (after checking git docs) or add a graph where the two flags diverge; I did not find one.

## Other findings from the run (not survivors)

- **M01 is the strongest single result.** Reading the author time instead of the committer time flips the round-54 w1 real run from FAIL to OK (author time 13:42:45-03:00 < launch 17:05:25Z). The round-54 FAIL is therefore carried entirely by the committer-date rule, which the docstring already declares author-controllable (a backdated committer date reads OK). The selftest's author/committer traps (cases 7, 7b) do catch M01, so this is covered.
- **M14 is only caught by the real run.** The selftest always passes `wave="w1"`. A test with `wave="w2"` (registry at `.ufo/waves/round-9/w2/swarm-registry.json`) would catch it in-process.
- **The independent harness is blind to this instrument.** All 17 mutants leave `check-r55-controls.py --claim c1` at `7/7 verdict=OK`. Any future "independent" control for this instrument must import or run `check-freeze-order.py` itself.

## Receipts

- `receipts/results/table.json`: all selftest, real-run and harness results per mutant.
- `receipts/results/M*-selftest.txt`, `receipts/results/M*-harness.txt`: full outputs per mutant.
- `receipts/baseline-selftest.txt`, `receipts/harness-baseline-c1.txt`: baseline outputs.
- `receipts/probes.py`, `receipts/probes-out.json`, `receipts/probes-stderr.txt`: the reproducible probes (run: `python3 -I probes.py <scratch> <mutant dir> <baseline checker>`).
- `receipts/results/probe-M05-*.log`, `probe-M05-scenario2.json`, `probe-survivors.json`: first-pass probe outputs.
- `receipts/baseline.sha256`: baseline digest.
