# R100MExecCounterC1 -- the C1 counter for PRED-C1-r100-v1

Seat: executor (counter build). Lane `mado`, round 100, wave w1, base
`43309e6af9a3b57f1bc839a826bef1f8eb7495e4`.

## 1. Deliverables and bytes

| artifact | path | sha256 |
|---|---|---|
| counter | `.ufo/waves/round-100/build/c1-r100-launchenv-path.py` | `2a930048c459316e6308ecb991d695afae394d0ccc8b37766cb1e2ec5f703699` |
| receipt | `.ufo/waves/round-100/receipts/c1-counter-selftest-r100.txt` | this seat's selftest output + instrument evidence |
| report | `.ufo/waves/round-100/w1/R100MExecCounterC1.md` | this file |

The counter is stdlib-only, ASCII-only, 1880 lines, and self-contained (the round-99
counter was read for its scoring helpers; nothing is imported from it). No file outside my
seat scope was written: `tools/`, `quality/`, `corpus/`, `plans/`, the git index and jj
state are untouched, and no commit, push or mutating git/jj command was run. No tool was
installed or upgraded (so there is no install record to make).

Separability: the counter is an **instrument** (it spawns read-only `git rev-parse`/`git
show`, the candidate/mutants/control through `python3 -I`, and the frozen fresh generator
through `python3 -I`; the generator may itself run the pinned `/usr/bin/gio`, being the
oracle's instrument). Nothing in it shells out to answer a modelled question on the
candidate's behalf, and it never launches a host application.

## 2. What the counter scores (exactly the seven frozen conjuncts)

```
TARGET_MET iff  default_cases            >= 6
           AND  default_classes          >= 3
           AND  cases_correct            == cases_total
           AND  fresh_correct            == fresh_total        (fresh_total >= 8)
           AND  mutants_killed           == mutants_counted    (mutants_counted >= 4)
           AND  base_set_default_cases   == 0
           AND  control_unset_as_empty_correct < cases_total
```

`met=` on the verdict line prints each of the seven as `name:0|1`; there is no eighth
clause. rc map: 0 TARGET_MET, 1 TARGET_MISSED, 2 SETUP_ERROR. The verdict line prefix is
`MADO_C1_R100:` as the seat item requires.

* `default_cases` / `default_classes` are computed from the frozen case file by class prefix
  `path-default` (count of such cases; count of distinct such class strings).
  `default_null_path_cases` (cases of that class whose `path` is `null`) is printed as
  evidence, not scored.
* `cases_*`, `fresh_*`, `mutants_*` come from one shared case leg over the frozen cases, the
  seeded fresh generation and the counted mutant population.
* `base_set_default_cases` is the do-nothing control: the count of `path-default` cases in
  the round-99 case file (default path
  `.ufo/waves/round-99/controls/launchenv-cases-r99.json`, `--base-cases` to override,
  optional `--expect-base-cases-sha256` to bind it). Doing nothing this round leaves it 0.
* `control_unset_as_empty_correct` is a copy built from the **candidate prefix** (cut at
  `def selftest(`) with `path = DEFAULT_SEARCH_PATH` replaced by `path = ''` under
  `if path is None:`, plus the untouched tail so the copy is runnable; it is scored through
  the same leg over the frozen cases and must lose at least one.

## 3. The one leg that had to change from round 99: PATH absent vs set-but-empty

Round 99 ran every case with a forced empty process `PATH` and passed `--path` only when the
case's `path` was not `null`. For a `path: null` case that makes the candidate read
`PATH=""` -- **set-but-empty** -- so the unset-default branch is unobservable and the mandated
mutant m2 could never be killed. The counter therefore runs a `path: null` case with **no
`PATH` key at all** in the child env and no `--path` (contract 1: no `--path` and no `PATH` =
PATH unset), and every other case with a poison `PATH=""` plus `--path <entries>` (so an
empty PATH entry is the case's own set-but-empty path). This mirrors the oracle, which
already launches `path: null` cases with `env` carrying only `LC_ALL`/`HOME`/`PROBE_OUT`.

Materialisation stays the oracle's (M98-8): `launchenv-probe-r99.py` is loaded by
`importlib`, hashed against BOTH envelope pins (`renderer_sha256` == `oracle_sha256`), and
its `build_root`/`path_string`/`sub_placeholders` drive every leg. The search order is
beside the `--cases` file first, then `<repo>/.ufo/waves/round-99/controls/`; both paths are
exercised (the selftest uses the beside path, the full-scale run below used the fallback).

## 4. Mutants: the frozen population plus four mandated probes

`mutants_counted` is the frozen mutant file's list plus four **required probes**, de-duplicated
on the exact `(find, replace)` pair, so a file that already carries them counts them once:

| probe | mutation | defect |
|---|---|---|
| m1 | `DEFAULT_SEARCH_PATH = '/bin:/usr/bin:.'` -> `...'/bin:/usr/bin'` | trailing dot dropped |
| m2 | `if path is None: path = DEFAULT_SEARCH_PATH` -> `path = ''` | unset read as empty |
| m3 | the walk's `if working_dir is not None and not _is_abs(startp): startp = _join2(...)` -> `if False:` | working-dir join disabled |
| m4 | the `if entry == '': startp = program else: startp = entry + '/' + program` collapse | empty-entry rule collapsed |

A kill needs a **new wrong answer against the candidate's own baseline** on at least one case
(r70 rule); a crash is `crashed_not_killed`, never a kill. A probe whose anchor is absent from
the candidate prefix is **unbuildable**: it stays counted and uncounted-as-killed, so the run
is TARGET_MISSED with `unbuildable=N` -- never a green from a mutant that was not built.

## 5. Refusals (SETUP_ERROR, exit 2) -- all exercised by the selftest

pin format for all six pins (plus the optional base-cases pin), rev/base-rev format, jobs and
fresh-count format; missing cases/mutants/genseed/base-cases; each input sha mismatch;
`--expect-tool-sha256`/`--expect-execargv-sha256` mismatch at the measured rev; the tool or
sibling absent at the measured rev; the tool **absent at the base rev** (the round-100
before-state says the branch *is* modelled there, so its absence is a refusal, not a green);
gio missing/other binary; case envelope (version/round/oracle/gio/glib2/classes/renderer
pins/cases) and per-case schema; renderer absent or off-pin; mutant file schema, duplicated
anchors, anchors that do not occur exactly once in the non-selftest prefix, and
`candidate_sha256` != the tool bytes at the measured rev; fresh generator rc/summary/pin
violations. An incomplete input is always a refusal.

## 6. Evidence

Counter selftest on the landed bytes (receipt sec 1): `checks=24 failed=0`, rc 0, wall 10.29 s
at load average 88.67 on 32 cores.

The 24 checks are: `st-fixture-build`, `st-target-met`, `st-result-line-format`,
`st-conjuncts-listed`, `st-tool-pin`, `st-execargv-pin`, `st-cases-pin`, `st-mutants-pin`,
`st-genseed-pin`, `st-gio-pin`, `st-setup-missing`, `st-renderer-missing`,
`st-base-tool-absent`, `st-rev-not-commit`, `st-case-mismatch`, `st-mutant-survives`,
`st-mutant-crash`, `st-required-probe-unbuildable`, `st-base-set-control-fails`,
`st-default-cases-floor`, `st-fresh-seed-override`, `st-fresh-seed-random`,
`st-unset-branch-discriminated`, `st-scratch-clean`. Each miss check asserts rc **1** and the
specific line field (e.g. `survived=1`, `crashed_not_killed=1`, `unbuildable=1`,
`base_set_default_cases=1`, `default_cases=0` with `met=default_cases:0`).

Full-scale instrument run (receipt sec 2, exit 0, wall 6.29 s): the round-99 frozen 67 cases
merged with **seven path-default cases this seat measured twice with the round-99 oracle**
(labels agreeing both runs), 74 cases / 34 classes, against the lane worktree candidate:

```
default_cases=7 default_classes=3 default_null_path_cases=3
cases_total=74 cases_correct=74
fresh=8/8 fresh_seed=f49fe8c1d8bf028e
mutants_counted=4 mutants_killed=4/4 crashed_not_killed=0 survived=0 unbuildable=0
  req-m1 killed by pd-dot-unset; req-m2 by pd-dot-unset (+1)
  req-m3 by tpath-xte (+2);   req-m4 by pe-empty-str (+1)
control_unset_as_empty_correct=72/74
base_cases=67 base_set_default_cases=0 base_cases_correct=67/67
base_branch_sensitive_cases=0
met=default_cases:1,default_classes:1,cases:1,fresh:1,mutants:1,base_set:1,control:1
MADO_C1_R100: TARGET_MET
```

This is **instrument evidence, not the frozen case file**: the merged file, the smoke mutant
file and the smoke fresh generator lived only in this seat's scratch and were removed. The
seven measured labels are preserved in receipt sec 3 so the cases seat and the L1 can cross-check
their own measurement; three are refusals (`load`) and four are launches, including the
measured `argv[0] = {root}/./probe.sh` shape the L1 reported for the unset default.

Two further facts from the same run, worth recording:

* the **before-state is measured, not asserted**: the base revision's tool bytes
  (`a63c20c8...`) score 67/67 on the round-99 case file and **zero** of those cases change
  answer when that tool reads an unset PATH as empty (`base_branch_sensitive_cases=0`), and
  the round-99 file carries zero `path-default` cases (`base_set_default_cases=0`);
* the candidate answered all 74 cases both before and after the tool seat's selftest-only
  edit of `tools/mado-launchenv.py` (worktree `a63c20c8...` then `3b29dc65...`), so the edit did
  not disturb the default-path branch.

## 7. Handover notes for the L1 (no target move, no new conjunct)

1. `--expect-tool-sha256` must be the bytes **at the measured rev**. The tool is being edited
   this wave (worktree `3b29dc65...` at the time of writing; base rev `a63c20c8...`). The
   mutant file's `candidate_sha256` binds the same bytes: a file written for other tool bytes
   refuses with `setup-mutants-candidate-sha256` (observed twice this seat).
2. The four required probes anchor on literal candidate lines (`DEFAULT_SEARCH_PATH = ...`, the
   `if path is None:` block, the walk's working-dir join, the `if entry == '':` block). They
   exist in both the base and worktree bytes today. If a later edit rewrites them, the probe
   becomes `unbuildable` and the run reports TARGET_MISSED -- loud, never silent.
3. `--base-cases` defaults to the round-99 file inside `--repo`; if that file is not present
   the counter refuses (the do-nothing control would be unmeasured). Pass
   `--expect-base-cases-sha256 14b4cc57...82acd` to bind it.
4. `--fresh-count` defaults to 8 (the frozen floor, r99's generator emits exactly `--count`
   cases). Raise it if the L1 wants a larger fresh population; the floor stays 8.
5. Every `path: null` case in the frozen file must be measured by the oracle with PATH
   **absent** (the r99 oracle's env does this) and is scored by the counter the same way; a
   case that means "PATH set but empty" must carry `"path": [""]` (or `[]`), not `null`.
6. The renderer is looked up beside the cases file first, then in the round-99 controls
   directory; either way it must hash to both envelope pins.

## 8. Scratch

`/fast/scratch/hyaku/mado-r100/R100MExecCounterC1` was created for this seat, held the
counter's development copy, the oracle measurement roots and the smoke fixtures, and is
removed before this seat yields. No scratch tree is left on disk.

## 9. Coordination observation (not a defect of this seat's artifact)

At 02:22 -- the same minute this seat landed its build artifact -- a *different* C1 counter
appeared at the canonical path `quality/counters/c1-r100-launchenv-path.py`: 20364 bytes,
457 lines, sha256
`3cbcd82fee36140ed795fe9b523f8451e2d987056c4cb7bf876ff91fa77c566a`. It is not this seat's
bytes (mine are `2a930048c459316e6308ecb991d695afae394d0ccc8b37766cb1e2ec5f703699`, 91543
bytes, 1880 lines, at the build path this seat's item names), and I did not modify it:
`quality/` is outside my write scope.

Both files carry the same seven conjuncts, the same `MADO_C1_R100:` verdict prefix and the
same PATH-absent vs set-but-empty correction. The difference that matters for
PRED-C1-r100-v1 is the mandated mutant population: the 457-line copy carries no m1--m4
required probes of its own and scores only the frozen mutant file, so if that file omits one
of the four the predicate's `mutants_counted >= 4` rests on the file alone. This seat's
artifact adds the four probes and reports an anchor that cannot be built as `unbuildable`
(TARGET_MISSED, never a green). The L1 decides which bytes land at the canonical path; the
declaration's counting command runs whatever sits there.
