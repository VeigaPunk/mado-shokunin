# R55W2RevConformance — round 55 landing conformance pre-check (w1)

Scored revision: `57584ed67716340b3d466fa04333ac0bab3fb79e`. Lane HEAD at check time: `721ba9c1` (one commit later: w2 spec generator, 37 seats). All reads are from committed bytes at the scored rev unless marked otherwise. No lane file was edited; no git mutation was run.

Receipts (copied into this directory): `receipts/check-wave-done-r55.txt`, `receipts/check-deliverables-w1.txt`, `receipts/trailer-check-w1.txt`, `receipts/status.txt`, `receipts/stub-records.txt`. Reproducer: `trailer-check.py` (`python3 -I trailer-check.py <lane> <rev> .ufo/waves/round-55/w1`).

## Results per item

| # | Item | Verdict | Evidence |
|---|---|---|---|
| 1 | Every w1 seat has a report sidecar or a documented absence | **BROKEN** (2 seats) | 38 of 40 trailer paths exist at rev. `R55ScoutCallers` and `R55ScoutHyprlang` have no report file and no documented absence at rev. |
| 2 | Every wave has a `results.json` | **SURVIVES for w1; w2 not committed** | `w1-results.json` at rev: `lane=mado round=55 wave=w1`, `seats=40 == len(results)=40`, no duplicate names. w2 has no results file (not launched to completion). |
| 3 | `check-wave-done.py` at the scored rev | **BROKEN as a conformance signal** | Prints `WAVE wave=w1 ... seats=40 dispatched=40 settled=40 verdict=OK` and `MADO_WAVE_DONE: round=55 waves=1 settled=1 verdict=OK`, rc=0. The round's own account is 38 settled + 2 dead. |
| 4 | `check-deliverables.py` over the 39 w1 `.md` reports | **FAIL (tool), with a stated cause** | `CHECK101: reports=39 declared=31 exists=30 absent=1 undeclared=28 verdict=FAIL`, rc=1. |
| 5 | Untracked wave markers | **FINDING** | `w2.ready` and `w2.ready.dispatched` are untracked in the lane. `w2/R55W2CritEntryProse/` and `w2/R55W2RevScope17/` hold untracked output. |
| 6 | Misrooted seat files at the fleet root naming mado/r55 | **NOT-REPRODUCED** | Fleet status has 45 entries. The only match for `r55\|round-55\|mado` is ` A .scratch/closure-mado-r50.json`, which names mado and r50, not r55. Nothing was touched. |
| 7 | w1 seats whose output is a stub | **FOUND: 2** | `R55ScoutCallers` (123 chars) and `R55ScoutHyprlang` (298 chars). Both are preamble narration with no tool output and no error text. |
| 8 | w1 name collisions (R55RevC1Contract vs -2) | **BROKEN** for `R55RevC1Contract`; others UNVERIFIED | Two writers in `w1/R55RevC1Contract/`. Details below. |

## Item 1: report sidecars and absences

Per-seat check (`receipts/trailer-check-w1.txt`): the trailer path of every dispatched seat (`Report: write your scoped findings to ...`, read from `w1-dispatch.json`) was tested with `git cat-file -e <rev>:<path>`.

- `dispatched=40 results=40 trailer_reports_at_rev=38 missing=2`
- Missing: `.ufo/waves/round-55/w1/R55ScoutCallers.md`, `.ufo/waves/round-55/w1/R55ScoutHyprlang.md`.
- Both are recorded in `w1-results.json` with `agent=scout`, `note=null`, and a non-empty `output` (see `receipts/stub-records.txt`).
- A documented absence exists only at HEAD, not at the scored rev. `w2-dispatch.json` (committed in `721ba9c1`) says "RE-ISSUE of the w1 item that died on a provider limit". At the scored rev the only record is the dispatch and results JSON.
- The cause "provider limit" is **UNVERIFIED** from the artifacts. The recorded outputs contain no error text.

## Item 2: results.json

- `w1-results.json` exists at the scored rev with `lane=mado`, `round=55`, `wave=w1`, `seats=40`, and 40 records. Names are unique. The shape matches the dispatcher's `{lane, round, wave, seats, results}`.
- w2 has no `w2-results.json` at the scored rev or at HEAD. Expected while w2 runs, and not a w1 defect.

## Item 3: check-wave-done.py

Command: `python3 -I quality/check-wave-done.py --repo <lane> --rev 57584ed6... --round 55 --work <scratch> [--verbose]`. Output (rc=0):

```
WAVE wave=w1 ready=1 results=present seats=40 dispatched=40 settled=40 verdict=OK reason=none
MADO_WAVE_DONE: round=55 waves=1 settled=1 verdict=OK
```

The same output appears at HEAD `721ba9c1`.

Why the gate is green: `seat_state` (quality/check-wave-done.py:234-266) returns `settled` for any record with no `status` and a non-empty string `output`. Probe (`seat_state` imported in place and called on the real stub record): `{'name': 'R55ScoutCallers', 'agent': 'scout', 'output': "I'll read the godspeed skill ...", 'note': None}` returned `('settled', 'output')`. The gate has no way to see a provider death that leaves a narration string in `output`. Its selftest (58/58, run here) has no preamble-only case.

Round-level scope: `waves=1` means only `.ready` files **committed** at the rev are scored. `w2.ready` exists on disk and is untracked, so the round line reads `verdict=OK` while w2 is launched and running. The gate is correct by its own definition. The round-level OK is not a statement about w2.

## Item 4: check-deliverables.py

Usage read first (`--repo --rev --report ... --file ... --seat-dir --require-declaration`). Command run over the 39 `.md` files at the rev with `--require-declaration`:

```
CHECK101: reports=39 declared=31 exists=30 absent=1 undeclared=28 verdict=FAIL
```

- The one ABSENT is `R55RevC1Contract-2.md`, whose Deliverables bullet reads `` `.../w1/R55RevC1Contract-2.md` ``. The elided `.../` is not a real path, so the resolver cannot find it. The file exists at the rev as `.ufo/waves/round-55/w1/R55RevC1Contract-2.md`. The ABSENT is a report-text defect, not a missing file.
- `undeclared=28`: the w1 seat reports carry no `Report:` trailer. The trailer lives in the dispatch task text. This tool therefore cannot prove 28 of 39 reports, and the trailer check (item 1) is the usable substitute.

## Item 5: untracked wave markers

`git status --porcelain --untracked-files=all` in the lane (`receipts/status.txt`):

- `?? .ufo/waves/round-55/w2.ready`
- `?? .ufo/waves/round-55/w2.ready.dispatched`
- w2 seat output, growing while this check ran: `w2/R55W2CritEntryProse/` and `w2/R55W2RevScope17/` at first capture; 304 untracked `w2/` paths in `receipts/status.txt`, 380 at a later re-run.

No w1 path is untracked. The w2 launch marker is untracked, so the committed-bytes gate cannot see w2. The order that the claims-frozen contract requires (freeze committed before `.ready`) is not checked here.

## Item 6: fleet root

`git -C /home/vgpnk/Projects/shokunin status --porcelain --untracked-files=all` lists 45 entries. None names `r55`, `round-55` or a mado round-55 seat. The one match is ` A .scratch/closure-mado-r50.json` (mado, round 50). Those entries are not touched. `ls /home/vgpnk/Projects/shokunin | grep -i r55` is empty.

## Item 7: stub seats

| seat | output chars | note | report file at rev |
|---|---|---|---|
| R55ScoutCallers | 123 | null | absent |
| R55ScoutHyprlang | 298 | null | absent |

Both outputs are the first sentence of a tool plan ("I'll read the godspeed skill ... then fetch ..."). These are the two provider deaths in the round's account. Their settled status was not checked by any gate (item 3).

## Item 8: name collisions

`w1.ready.dispatched` (line 2) maps 11 spawned names to suffixed identities:

| name | spawned id |
|---|---|
| R55ScribeEntryB | R55ScribeEntryB-2 |
| R55ScribeP19a | R55ScribeP19a-3 |
| R55ScribeP19b | R55ScribeP19b-3 |
| R55ScribeIndex | R55ScribeIndex-2 |
| R55ExecC1CounterA | R55ExecC1CounterA-3 |
| R55ExecC1Harness | R55ExecC1Harness-4 |
| R55ExecC3CounterA | R55ExecC3CounterA-2 |
| R55ExecTool1 | R55ExecTool1-2 |
| R55ExecTool4 | R55ExecTool4-2 |
| R55ScoutWayland | R55ScoutWayland-3 |
| R55RevC1Contract | R55RevC1Contract-2 |

**R55RevC1Contract (BROKEN):**
- Two writers used `w1/R55RevC1Contract/`.
- `R55RevC1Contract.md` (heading `# Seat R55RevC1Contract`) is the file the dispatch trailer names. It is not the recorded identity. Its Deliverable is `attack.md`, and it has a `## Result` and `## Defects / ambiguities for L1`.
- `R55RevC1Contract-2.md` is the report of the recorded identity (`results.json` output: `"seat": "R55RevC1Contract-2"`). It declares `attack-2.md` and `R55RevC1Contract-2.md`. It says in its own text that a peer with the same name wrote into the same directory.
- Result: the trailer-named file belongs to a seat with no results record. The recorded seat's report is at a path no trailer names. An integrator who reads the trailer path reads the unrecorded writer's C1 attack.
- `results.json` has no duplicate names. The collision is hidden by the name-unique record.

**Other 10 renamed seats:** UNVERIFIED for a second writer. Each has its trailer report at the base name. I did not check their sidecar directories for another identity's files.

## Other observations

- `check-wave-done.py --selftest` ran 58/58 (matches `SELFTEST_CHECKS = 58`). No selftest case covers preamble-only output.
- Lane HEAD is past the scored rev. The gate at rev and at HEAD both read `waves=1 settled=1 verdict=OK`.
- Per the instruction, nothing was run against the fleet root or sibling lanes beyond read-only `git status` and `ls`. No hyprctl call was made.

## Verdict summary

- **BROKEN:** 2 w1 seats without report sidecar or documented absence at the scored rev (item 1); `check-wave-done` reports 40/40 settled where the round account says 38 (item 3); R55RevC1Contract trailer path owned by an unrecorded writer (item 8).
- **FAIL (tool):** `check-deliverables` CHECK101 on w1 reports, caused by one elided path and 28 reports with no trailer.
- **FINDING:** w2 launched but uncommitted, so the committed-bytes gate omits it.
- **SURVIVES:** w1 `results.json` present and shape-valid; trailer reports exist for 38/40 seats.
- **NOT-REPRODUCED:** misrooted fleet-root seat files naming mado/r55.
- **UNVERIFIED:** cause of the two provider deaths; the 10 other suffixed seats for second writers.

## Not verified

- The provider-limit cause for the two stub seats.
- Whether any other renamed seat wrote into another identity's directory.
- Round-55 w2 conformance (no w2 results exist; the w2 wave was in progress).
- The claims-frozen freeze-before-`.ready` order (outside this item).
