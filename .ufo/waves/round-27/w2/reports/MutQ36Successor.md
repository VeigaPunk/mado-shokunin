# MutQ36Successor — round-27 w2 mutation probe

MUTQ36 verdict: **6/8 killed, 2/8 survived, 0 inconclusive** by the unmodified full fixture runner. The 31 direct behavioral/parity cases kill 5/8; Q3 is detected only by the runner's nested mutation table. Both full-gate survivors have exercised contract-breaking witnesses.

Axes: contract fault exposure, detector discrimination, exact-byte restoration, host isolation.

## Scope and controls

- Lane subject read-only: `/home/vgpnk/Projects/shokunin/mado-shokunin/quality/check-control-receipts.py`; its hash matches the w1 receipt and is unchanged at return: `2233db1d489fa325c3b4bd9b5b1dccc68eb9311864a0d975303907463fa65af2`.
- Unmodified fixture builder: `/fast/scratch/hyaku/mado-r27/q36/run_fixtures.py`, SHA-256 `f32ea076e9764e49f1e67ae32c138dbb8d95476955298a3f358cf4683e42fe26`.
- Eight independent one-line mutants, each applied alone to `ROOT/<id>/subject.py`, where `ROOT=/fast/scratch/hyaku/mado-r27/mutq36`.
- Shared pristine full-run control: `ROOT/baseline.txt`, exit 0. It prints `QS36SEEDS lane_runs=5 fixtures=24 mutants_killed=9/9` and `Q36SUCCESSOR verdict=PASS`.
- Each mutant was run through the original CLI with `--checker` pointing to its copy. Every locus required by the runner's own nine mutations remained present, so no setup/locus failure was counted as a kill.
- After restoration, the original full CLI was run separately on all eight subjects: every run exited 0 with the same 24 fixtures and 9/9 internal kills. Before/mutated/restored hashes are recorded below.
- Separately, `ROOT/probe_detector.py` imports the original runner's `build_fixture`, `run_checker`, `fixture_problems`, lane declarations and legacy parity assertions. It runs 24 fixtures + 5 lane runs + 2 legacy runs without adding the runner's nine secondary mutations. All eight copies had pristine/mutated/restored passes through this identical direct detector. Four added witnesses are scored separately, never included in the original-suite verdict.

## Mutants and observed detector output

The full-run detector exit column is **pristine / mutated / restored**. Checker exit changes inside each case are distinct from detector exits.

| Single mutant | Smallest changed point | Expected detector / actual output | Full detector exits | Verdict |
|---|---|---|---|---|
| Q1-seed-double-count | 191: `sum(1 for name ...)` → `sum(2 for name ...)` | `red-seeds-short`: checker 1 → 0, `shape_counts=DoNothing:2,Junk:2,EmptyArray&#124;AllFalse:2`; PASS with only one receipt per shape. | 0 / 1 / 0 | killed |
| Q2-glob-case-sensitive | 97: `rel = rel.lower()` → `rel = rel` | All original checks still pass; uppercase-extension witness rejects valid receipts (see below). | 0 / 0 / 0 | survived |
| Q3-glob-no-basename | 98: `base = rel.rsplit("/", 1)[-1]` → `base = rel` | Direct 31 cases pass. Full runner fails only its nested M4 kill assertion: pristine=0, mutant=0, expected (0,1). | 0 / 1 / 0 | killed (meta-only) |
| Q4-marker-first-line | 85: `text.split("\n")` → `text.split("\n")[:1]` in `has_marker` | Legacy round-25: checker 0 → 1, qualifying receipts 19 → 1, all six default shapes missing. | 0 / 1 / 0 | killed |
| Q5-marker-case-insensitive | 85: `l.startswith("CONTROL ")` → `l.lower().startswith("control ")` | All original checks still pass; lowercase-marker witness is wrongly accepted (see below). | 0 / 0 / 0 | survived |
| Q6-chronology-grace-second | 178: `.timestamp()` → `.timestamp() + 1` | `equal-time`: checker 1 → 0, `order=ok gap_s=1`, PASS despite receipt time equalling createdAt. | 0 / 1 / 0 | killed |
| Q7-bad-tip-exit-one | 123: bad-tip `return 2` → `return 1` | `bad-tip`: actual checker exit=1, expected=2; output remains `UNEVALUABLE bad tip deadbeef00`. | 0 / 1 / 0 | killed |
| Q8-no-receipts-exit-two | 155: no-receipts `return 1` → `return 2` | `red-md-marker`: actual checker exit=2, expected=1; output remains `CONTROL_RECEIPTS verdict=FAIL reason=no-receipt-under-.ufo/waves/round-98/controls/`. | 0 / 1 / 0 | killed |

Q3 nuance: the full runner exits 1 solely with `FAILURE mutant M4-basename-only not killed by green-glob-subdir: pristine=0 mutant=0 expected (0, 1)`. It does **not** have a direct fixture showing the missing basename fallback. The nested M4 becomes behaviorally unchanged on this mutated subject. This is a full-gate kill, not a claim that its ordinary fixtures cover the defect. The added basename witness below exposes the missing direct coverage.

## Survivor witnesses

Witness fixtures are real scratch git histories built with the original `build_fixture()` function. Registry createdAt is `2026-10-22T00:05:00Z`; the three receipts land at `2026-10-22T00:01:00+0000`, after an initial registry commit. Names cover DoNothing, Junk and EmptyArray. Each witness was exercised on pristine, mutant and restored bytes with no stderr.

### Q2 — case-sensitive receipt selection survives the full gate

- Witness repository: `ROOT/Q2-glob-case-sensitive/mutated/repos/w-glob-uppercase` (tip `90174e0655f31753c695b706c4505cf2d2cacf10`).
- Three files: `K1DoNothing-seed1.TXT`, `K1Junk-seed1.TXT`, `K1EmptyArray-seed1.TXT` under `.ufo/waves/round-98/controls/`; contents `exit=1\n`. Default globs must match case-insensitively under the checker's documented contract.
- Full runner on this mutant: exit 0, `fixtures=24 mutants_killed=9/9`, `Q36SUCCESSOR verdict=PASS`.
- Witness checker exits: **0 / 1 / 0** (pristine / mutant / restored). Pristine/restored: `receipts=3`, `excluded_by_glob=0`, PASS. Mutant: `receipts=0`, `excluded_by_glob=3`, `CONTROL_RECEIPTS verdict=FAIL reason=no-receipt-under-.ufo/waves/round-98/controls/`.
- Exact checker commands, full stdout and expected exits: `ROOT/Q2-glob-case-sensitive/{before,mutated,restored}.txt` and corresponding JSON. The mutant also fails the basename witness because its `K1*.txt` pattern is lowercased but the path is not.

### Q5 — case-insensitive markdown marker survives the full gate

- Witness repository: `ROOT/Q5-marker-case-insensitive/mutated/repos/w-marker-lowercase` (tip `12d8284d4b151ca55537bfa614edbc848136c3c4`).
- Three `.md` receipts named for the shapes, each containing only `control Fixture control\n`. No valid case-sensitive `CONTROL ` / `# Control` marker exists; `--any-md` is not passed.
- Full runner on this mutant: exit 0, `fixtures=24 mutants_killed=9/9`, `Q36SUCCESSOR verdict=PASS`.
- Witness checker exits: **1 / 0 / 1**. Pristine/restored: `receipts=0`, FAIL. Mutant: `receipts=3`, `order=ok gap_s=240 shapes_missing=- seeds_short=-`, `CONTROL_RECEIPTS verdict=PASS`.
- Exact checker commands, stdout and expected exits: `ROOT/Q5-marker-case-insensitive/{before,mutated,restored}.txt` and JSON.

### Additional direct-coverage finding — Q3

- `ROOT/Q3-glob-no-basename/mutated/repos/w-glob-basename` (tip `579958ce24aee99505f346e799e47526e454373e`) has the three `.txt` receipts under `controls/v2/`, contents `exit=1\n`.
- With `--receipt-glob 'K1*.txt'`, witness checker exits are **0 / 1 / 0**. The mutant has `receipts=0 excluded_by_glob=3`; pristine/restored select all three. The contract explicitly allows basename matching at any depth.
- Q4's second-line-marker witness likewise has checker exits 0 / 1 / 0, but its legacy round-25 run already kills it. No survivor is reclassified as equivalent or permitted behavior.

## Exact commands and receipts

Pristine full-run command (executed; exit 0):

```sh
timeout --kill-after=5 600 env -i PATH=/usr/bin HOME=/fast/scratch/hyaku/mado-r27/mutq36/home prlimit --as=4000000000 --core=0 --fsize=16777216 -- python3 -I -B /fast/scratch/hyaku/mado-r27/q36/run_fixtures.py --checker /fast/scratch/hyaku/mado-r27/mutq36/pristine.py --scratch /fast/scratch/hyaku/mado-r27/mutq36/baseline --out /fast/scratch/hyaku/mado-r27/mutq36/baseline.txt
```

Every expanded mutant and restored command is recorded in `ROOT/mutation-ledger.json` (`full_mutated.command`, `full_restored.command`). They invoke the same unmodified runner under `timeout --kill-after=5 600`, `env -i`, and `prlimit --as=4000000000 --core=0 --fsize=16777216`, with `python3 -I -B`, a per-copy `--checker`, and isolated `--scratch`/`--out` paths.

- Full original-runner receipts: `ROOT/<id>/full-mutated.txt` and `ROOT/<id>/full-restored.txt` for all eight IDs in the table.
- Direct pristine/mutant/restored plus witness receipts: `ROOT/<id>/{before,mutated,restored}.{txt,json}`. Each records all exact subject commands and actual stdout/stderr.
- Mutation definitions, expected detectors, phase commands/exits, before/mutated/after hashes: `ROOT/mutation-ledger.json`. Full direct-case result objects also remain in `ROOT/phase-results.json`.
- Witness construction and direct detector source: `ROOT/probe_detector.py`; it leaves the original fixture builder unchanged.
- One initial async launch was refused by the host-wide background-job cap before execution; the synchronous pristine run succeeded. No refused launch is counted as a behavioral result.

## Restoration and safety

All eight assigned `subject.py` files began and ended with SHA-256 **2233db1d489fa325c3b4bd9b5b1dccc68eb9311864a0d975303907463fa65af2** (9,860 bytes). Restoration was in a `finally` block, including for nonzero detector exits. The original full runner passed on every restored copy.

| Copy | SHA-256 while mutated | Before = restored |
|---|---|---|
| Q1-seed-double-count | `5043acfc1e6ff1c3548521d9e019e83474e30fbcd3cd26a7c47aa99102c319c7` | `2233db1d489fa325c3b4bd9b5b1dccc68eb9311864a0d975303907463fa65af2` |
| Q2-glob-case-sensitive | `7ff7059b420ac42a7173344ad9563b81b8b5a50f4774f4f31725222a975a0803` | `2233db1d489fa325c3b4bd9b5b1dccc68eb9311864a0d975303907463fa65af2` |
| Q3-glob-no-basename | `6b928379b137ec4602de25d7cc012b5c4213a58cfbddec2c0f101e1f0dccda71` | `2233db1d489fa325c3b4bd9b5b1dccc68eb9311864a0d975303907463fa65af2` |
| Q4-marker-first-line | `5725f6d007e63b4561f70f12f4ffd0293a982f7ce6676acaaadb8259b07e539d` | `2233db1d489fa325c3b4bd9b5b1dccc68eb9311864a0d975303907463fa65af2` |
| Q5-marker-case-insensitive | `4e83fe2e1ac612a17ff494391132ad1a5ee208451351caa207141325f711e56c` | `2233db1d489fa325c3b4bd9b5b1dccc68eb9311864a0d975303907463fa65af2` |
| Q6-chronology-grace-second | `8c5266adb32605c01a4266657c344ddb2aa0e83719cfa2e3a7ed904d591100c4` | `2233db1d489fa325c3b4bd9b5b1dccc68eb9311864a0d975303907463fa65af2` |
| Q7-bad-tip-exit-one | `132e0e87117e3c098fea78fc1bc8bdda1191259be5cc7f6f2d97af78c4265dc0` | `2233db1d489fa325c3b4bd9b5b1dccc68eb9311864a0d975303907463fa65af2` |
| Q8-no-receipts-exit-two | `56ec9b8faf8c33ab5da2bad44d8a2cf1b6c9bda6df9bb9e77f57b1404c33181f` | `2233db1d489fa325c3b4bd9b5b1dccc68eb9311864a0d975303907463fa65af2` |

- Final hashes and coredump evidence: `ROOT/safety-and-restoration.json`. Lane checker and original fixture builder retain their starting hashes; the round-26 checker was only read.
- Hyprland coredumps: **1338 before, 1338 after, delta 0**. Counted `/usr/bin/Hyprland` rows from `coredumpctl list --no-pager --no-legend`; the initial raw output is `artifact://36821`, and the final cleared-environment command/count are saved in the safety receipt.
- No Hyprland, tinywl, bwrap, network, live compositor verb, tool installation/update, or service start was performed. All started subprocess groups completed and were reaped; no timeout or setup error was used as a kill.
- Every git write occurred in the per-phase fixture repositories under ROOT, using the original builder's cleared environment with GIT_DIR/GIT_WORK_TREE/GIT_INDEX_FILE absent. No git/jj write command touched the lane. `df -h /fast` before writes showed 73G free. Only this requested report was written in the lane.

**VERDICT: full gate killed=6/8 survived=2/8 inconclusive=0; direct existing cases killed=5/8; two full-gate survivor witnesses confirmed; all assigned bytes restored.**
