# Q36Fixtures — repair R4 (M25-3 survivors) + `--counter-sha` filter

Date: 2026-10-23. Seat: `MadoR26.Q36Fixtures` (leaf executor). No labrat was used: the tool set
carries no spawn/task tool, so the single permitted dispatch was unavailable.

**Verdict: `Q36FIXTURES verdict=PASS — Q36MUTANTS killed=8/8 fixtures=10`, legacy parity ok.**
The five named M25-3 survivors are all red→killed by synthetic fixtures, and the new
`--counter-sha` behaviour has three mutants of its own, also killed.

## Files written (mine only; no lane file outside this list)

| Path | State | sha256 |
|---|---|---|
| `.ufo/waves/round-26/quality/check-control-receipts.py` | new successor, executable | `351127bd0d735665f899129fa3ad408b8d23c85d9f71969b44e3b63d86b6d3b4` |
| `.ufo/waves/round-26/quality/q36-fixtures/fixtures.py` | new fixture/mutant declarations | `96e6c05a538645bcadefa66947955861f0626381e4fb7f1442e65f5044dc0b43` |
| `.ufo/waves/round-26/quality/q36-fixtures/run_fixtures.py` | new builder + matrix runner | `13c115cd2cb1b02c7ab5301be038a16768c12b342fbca723304dd75034654e97` |
| `.ufo/waves/round-26/quality/q36-mutants.txt` | receipt (280 lines) | `8689bc5eaf1b028692614e8e08ca05d955726586bd842249491564a5cae54405` |
| `.ufo/waves/round-26/w1/reports/Q36Fixtures.md` | this report | — |

The round-25 checker is untouched and still `90542cad47d9004eaad83508ca2a3bfa81b15b4a932642d58942d23e58471f72`
(read back in the receipt header). Scratch: `/fast/scratch/hyaku/mado-r26/q36/{repos,checkers,home}`.
No fixture repo is under the lane; only the four files above were written there.

## Successor behaviour

Same CLI and same verdict semantics as round-25, plus one option:

- `--counter-sha SHA` — repeatable; each value must be 64 hex (lower-cased on input; a bad value
  is an argparse error, exit 2). When given, a `.md` qualifies only if its **first line** contains
  the full 64-hex value, case-insensitively; with several values a receipt qualifying for **any**
  of them counts. Without the flag the filter is off and the two historical lane cases reproduce
  their round-25 verdicts exactly (see parity below).
- New diagnostic fields `counter_sha=…` and `excluded_by_counter_sha=N` print on the `tip=` line;
  `excluded_by_counter_sha` counts marker-qualified `.md` files the sha filter removed, so a
  receipt shows the filter both matched and excluded something.
- Unchanged on purpose: the `CONTROL `/`# Control` marker requirement (with `--any-md` as the
  explicit escape hatch), strict `first[1] < cts` ordering, oldest receiver via
  `git log --reverse --diff-filter=A`, `createdAt` only (never `updatedAt`), shape coverage by
  receipt **file name**, and exit codes 0/1/2.

## Mutant kills (all on the successor, one mutation per scratch copy)

| Mutant | Behaviour-bearing change | Legacy r24 | Legacy r25 | green | Killer fixture | pristine→mutant | Verdict |
|---|---|---:|---:|---:|---|---:|---|
| M1-nonstrict | L140 `first[1] < cts` → `<=` | 1 | 0 | 0 | equal-time (createdAt == receipt second) | 1→0 | killed |
| M2-ignore-shapes | L149 `ok = order_ok and not missing` → `ok = order_ok` | 1 | 0 | 0 | missing-shape (no NoReader name) | 1→0 | killed |
| M3-newest-receipt | L111 drop `"--reverse",` from `git log` | 1 | 0 | 0 | later-receipt (2nd receipt commit after data) | 0→1 | killed |
| M4-any-md | L100 marker predicate → `if False:` | 1 | 0 | 0 | nonreceipt-md (only `.md` has no marker) | 1→0 | killed |
| M5-updatedAt | L132 `["createdAt"]` → `["updatedAt"]` | 1 | 0 | 0 | updated-at (createdAt late, updatedAt early) | 0→1 | killed |
| M6-ignore-counter-sha | L65 sha gate → `if True:` | 1 | 0 | 0 | sha-late (sha-X receipt lands after data) | 1→0 | killed |
| M7-sha-anywhere | L67 first line → whole file | 1 | 0 | 0 | sha-not-first-line (sha on line 3) | 1→0 | killed |
| M8-sha-prefix | L68 full 64 → 12-hex prefix | 1 | 0 | 0 | sha-prefix (first line has 12 hex only) | 1→0 | killed |

The `legacy` columns are the same mutant run on the two real lane cases: all stay `1` and `0`, so
the legacy pair cannot see any of these mutants — the kill comes only from the synthetic fixture.
The `green` column is a no-harm gate: every mutant must leave the all-shapes/before-data baseline
at exit 0, which all do. Each mutated copy is `ast.parse`d before it runs, so no "kill" is a
syntax-error exit; every run's stderr is asserted empty.

`equal-time` and `updated-at` are the two fixtures whose design is forced: git committer time is
whole seconds, so a mutant reading `updatedAt` can only flip a PASS baseline if `updatedAt` is
*earlier* than the receipt commit (hence earlier than `createdAt`). That artificial field order is
the point of the fixture, not a claim about real registries.

Fixture baselines (pristine successor, all as declared): `green` 0, `equal-time` 1
(`order=LATE gap_s=0`), `missing-shape` 1 (`shapes_missing=NoReader`), `later-receipt` 0
(receipt commit = the **first** receipt commit `588f100934a0`), `nonreceipt-md` 1
(`receipts=0`, `reason=no-receipt-under-…`), `updated-at` 0, `sha-green` 0, `sha-not-first-line` 1
(`excluded_by_counter_sha=1`), `sha-prefix` 1, `sha-late` 1 (`receipts=1 order=LATE`).

## Exact commands and outcomes

Regenerate the receipt (the one recorded in it):

```sh
cd /home/vgpnk/Projects/shokunin/mado-shokunin
timeout 600 prlimit --as=4000000000 --nofile=4096 python3 -I -B \
  .ufo/waves/round-26/quality/q36-fixtures/run_fixtures.py \
  --out .ufo/waves/round-26/quality/q36-mutants.txt
# exit=0 ; Q36MUTANTS killed=8/8 fixtures=10 ; Q36FIXTURES verdict=PASS
```

Two consecutive runs of the current bytes (`/fast/scratch/hyaku/mado-r26/q36/run3.txt`,
`run4.txt`) differ only in `generated_utc=` and the `--out` path in the recorded argv; everything
else is byte-identical. The committed receipt equals `run3.txt` once those two lines are dropped.

Legacy parity inside the receipt (read-only lane history, merged into the same command run):

```sh
python3 -I -B .ufo/waves/round-26/quality/check-control-receipts.py --repo <lane> --round 24 \
  --data-registry .ufo/waves/round-24/w1/reports/swarm-registry.json --tip 41cc04c8 --any-md
# order=LATE gap_s=-1083 shapes_missing=EmptyArray|AllFalse,Echo,LabelKeyed, exit=1, parity ok
python3 -I -B .ufo/waves/round-26/quality/check-control-receipts.py --repo <lane> --round 25 \
  --data-registry .ufo/waves/round-25/a3w2/reports/swarm-registry.json --tip ef94763c
# order=ok gap_s=7695 shapes_missing=-, exit=0, parity ok
```

Parity compares `receipt_commit=`, `order=`, `CONTROL_RECEIPTS verdict=` and `exit=` with
`round-25/quality/q36-red-round24.txt` and `q36-green-round25.txt`; the only added text is the
`counter_sha=- excluded_by_counter_sha=0` suffix on the `tip=` line. This legacy run is the only
place the lane is touched at all, and it is read-only (`git rev-parse/show/log` on committed
history); no fixture repo is created there and nothing is written.

Feature edge checks (manual, scratch fixtures):

```sh
# two --counter-sha values, only the second matches → PASS, exit 0
# upper-case 64-hex argument matches the lower-case receipt → PASS, exit 0
# --any-md on nonreceipt-md → PASS, exit 0 (deliberate escape hatch still works)
# --counter-sha deadbeef → argparse error, exit 2
# absent registry at tip → "UNEVALUABLE data registry … absent at tip", exit 2
# bad --tip → "UNEVALUABLE bad tip nosuchrev", exit 2
```

## Risks and limits

- **Scratch is not committed.** The repos and mutated copies live under
  `/fast/scratch/hyaku/mado-r26/q36/`; the declarative fixtures are in `fixtures.py`, so a wipe
  costs one rerun of the command above, not the evidence.
- **`--counter-sha` semantics are pinned here**: full 64 hex, case-insensitive, first line only,
  any-of across repetitions. A control receipt that names the counter sha only on a later line
  does **not** qualify (fixture `sha-not-first-line`). If the parent wants prefix or whole-file
  matching instead, the fixtures would have to change with it.
- **`--any-md` remains an escape hatch**: the `nonreceipt-md` kill is for a mutant that silently
  drops the marker requirement, not for the documented flag.
- Legacy parity covers the two historical lane cases only; no round-26 data registry exists yet
  in this wave, so the successor has not been exercised against a round-26 data wave.
- The fixture runner rebuilds every repo with fixed committer dates (`2026-10-22T00:00/00:01/00:09Z`)
  and a scratch `HOME`, `GIT_CONFIG_NOSYSTEM=1`, `GIT_OPTIONAL_LOCKS=0`; no display variable is
  inherited and no host state is touched.
- No blockers. Nothing was built, linted or run beyond this checker, its mutated copies, and the
  read-only lane git history; the parent owns the post-integration gate.
