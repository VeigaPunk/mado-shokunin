# R68ExecGate1 — replacement-ref guard on three standing gates

Seat: executor, round 68 / wave w1 / claim C2 (operability). Freeze
`e0727cda15621766c35dcf8b70c211b6531aab45`, lane base
`510100c81e6cf63fec6be380c2f2f9c670f32cbc`. Read-only on the lane: the lane worktree was not
modified; the three committed gates still hash exactly as at dispatch (§ Integrity). All writes
are drafts under this seat plus `/fast/scratch/hyaku/mado-r68/R68ExecGate1/` (removed at exit).
No commits, stages, pushes, checkouts or package transactions; no tool installed or upgraded.

## 1. Changes (drafts only)

| draft | guard construction (frozen census shape) | numstat |
|---|---|---|
| `draft/quality/check-anchor-cover.py` | dict-literal key `"GIT_NO_REPLACE_OBJECTS": "1"` added to the caller-built `env` (fresh env at old line 102) | +2 / −1 |
| `draft/quality/check-control-receipts.py` | subscript store `env["GIT_NO_REPLACE_OBJECTS"] = "1"` after `env = dict(os.environ, GIT_OPTIONAL_LOCKS="0")` (line 61) | +1 / −0 |
| `draft/quality/check-deliverables.py` | `env=dict(os.environ, GIT_NO_REPLACE_OBJECTS="1")` inside the two `subprocess.run` calls that read git objects (`git show`, old line 94; `git cat-file -e`, old line 113) | +4 / −2 |

Hunks (only guard lines added; no imports, no reformat, no argv/`capture_output`/`text` change):

```diff
--- quality/check-anchor-cover.py
+++ draft/quality/check-anchor-cover.py
@@ -100,7 +100,8 @@
         env = {"PATH": os.environ.get("PATH", "/usr/bin:/bin"), "HOME": args.work,
-               "TMPDIR": args.work, "LC_ALL": "C"}
+               "TMPDIR": args.work, "LC_ALL": "C",
+               "GIT_NO_REPLACE_OBJECTS": "1"}
```

```diff
--- quality/check-control-receipts.py
+++ draft/quality/check-control-receipts.py
@@ -59,6 +59,7 @@
     env = dict(os.environ, GIT_OPTIONAL_LOCKS="0")
+    env["GIT_NO_REPLACE_OBJECTS"] = "1"
     for k in ("GIT_DIR", "GIT_WORK_TREE", "GIT_INDEX_FILE"):
```

```diff
--- quality/check-deliverables.py
+++ draft/quality/check-deliverables.py
@@ -92,7 +92,8 @@
             blob = subprocess.run(("git", "-C", a.repo, "show", f"{a.rev}:{path}"),
-                                  capture_output=True, text=True)
+                                  capture_output=True, text=True,
+                                  env=dict(os.environ, GIT_NO_REPLACE_OBJECTS="1"))
@@ -111,7 +112,8 @@
                     if subprocess.run(("git", "-C", a.repo, "cat-file", "-e", f"{a.rev}:{c}"),
-                                      capture_output=True).returncode == 0:
+                                      capture_output=True,
+                                      env=dict(os.environ, GIT_NO_REPLACE_OBJECTS="1")).returncode == 0:
```

Notes. `check-anchor-cover.py` builds a fresh env (no `os.environ` inheritance was present
before, so no other variable's presence changed). `check-control-receipts.py` pops only
`GIT_DIR`/`GIT_WORK_TREE`/`GIT_INDEX_FILE` after the store, so the guard key survives.
`check-deliverables.py` now inherits a copy of `os.environ` at call time plus the guard (the
previous behaviour was inherited environment with no explicit `env`); every other key is
unchanged.

## 2. Proof a — census on a 20-file fixture

Fixture built from freeze bytes, not the worktree: population listed with
`git -C <lane> ls-tree -r --name-only e0727cda… -- quality`, filtered by
`^quality/check-[^/]+\.py$` (20 paths), each extracted with `git show e0727cda:<path>` into
`fixture.pyIe/quality/`, the three drafts overwritten in place, then
`git init` + `git -C "$D" -c user.name=r68 -c user.email=r68@example.invalid commit`. Scratch
toplevel was asserted equal to the fixture dir before the first commit.

```
python3 -I /home/vgpnk/Projects/shokunin/mado-shokunin/quality/counters/c2-r68-reader-guard.py \
  --repo /fast/scratch/hyaku/mado-r68/R68ExecGate1/fixture.pyIe --rev HEAD \
  --controls /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-68/controls/c2-controls.json
```

Exit 1 (expected at this partial state). Exact guard lines for the three repaired files:

```
MADO_R68_READER file=quality/check-anchor-cover.py reader=yes guard=yes
MADO_R68_READER file=quality/check-control-receipts.py reader=yes guard=yes
MADO_R68_READER file=quality/check-deliverables.py reader=yes guard=yes
```

Final contract line:

```
MADO_R68_READER_GUARD: population=20 readers=13 guarded=4 unguarded=9 controls=11/11 verdict=TARGET_MISSED rev=3ed5ce93d158288e03f472d534aec8ad40400c51
```

`controls=11/11` (all frozen classification cases, including `comment-only-mention`,
`docstring-only-mention`, `unrelated-dict-as-env`). `guarded=4` = my three + the base-guarded
`check-tool-ledger.py`. The remaining nine unguarded readers are the sibling seats' share:
`check-axis-scores.py`, `check-evidence-pointers.py`, `check-freeze-order.py`,
`check-index-rows.py`, `check-index.py`, `check-landed-contract.py`,
`check-round-outcome-first.py`, `check-session-material.py`, `check-wave-done.py`; the other
seven files are classified `reader=no`.

The census tool used is the freeze blob: `sha256(rev:e0727cda:quality/counters/c2-r68-reader-guard.py)`
= `8eb99a63e324fce18eda824d7aefa48d72650ff6abb7c4afa45def9191ce880e` = worktree hash.

## 3. Proof b — per-file test surfaces

None of the three files has a `--selftest` option (their argparse surfaces are listed below), so
each was checked with `py_compile`, `--help` parity, and real read-only invocations on the lane,
comparing committed bytes against the draft byte-for-byte (`diff -u` of stdout and stderr, plus
rc).

| file | argparse options | `py_compile` | `--help` | real invocation (committed vs draft) |
|---|---|---|---|---|
| `check-anchor-cover.py` | `--repo --rev --entry --registry --work` | rc 0 | rc 0, output identical | green: `--repo <lane> --rev e0727cda --entry corpus/knowledge/hyprland-config-autoreload-r56.md --work <s>/work107` → rc 0 both, stdout/stderr identical, final line `CHECK107: rows=39 covered=39 miss=0 verdict=OK` |
| | | | | red: `--rev 63f48dc1 --entry corpus/knowledge/hyprland-keyboard-repeat-numlock-r55.md` → rc 1 both, output identical, final line `CHECK107: rows=32 covered=25 miss=7 verdict=FAIL` |
| `check-control-receipts.py` | `--round --data-registry --repo --tip --shapes --seeds --receipt-glob --any-md --counter-sha` | rc 0 | rc 0, output identical | green: `--repo <lane> --round 25 --data-registry .ufo/waves/round-25/a3w2/reports/swarm-registry.json --tip ef94763c` → rc 0 both, identical, `CONTROL_RECEIPTS verdict=PASS` |
| | | | | red: same repo, `--round 24 --data-registry .ufo/waves/round-24/w1/reports/swarm-registry.json --tip 41cc04c8 --any-md` → rc 1 both, identical, `CONTROL_RECEIPTS verdict=FAIL` |
| `check-deliverables.py` | `--repo --rev --report --file --seat-dir --require-declaration` | rc 0 | rc 0, output identical | `--repo <lane> --rev e0727cda --report .ufo/waves/round-16/w1/reports/ExistingU7.md` → rc 0 both, identical, `CHECK101: reports=1 declared=1 exists=1 absent=0 undeclared=0 verdict=OK` (exercises both guarded calls: `show` + `cat-file -e` EXISTS path) |
| | | | | unresolved: `--report .ufo/waves/round-16/w1/reports/AbsentSeat.md` → rc 1 both, identical, `REPORT_UNRESOLVED … verdict=FAIL` |
| | | | | file mode: `--file <s>/ExistingU7.md --seat-dir .ufo/waves/round-16/w1/reports` → rc 1 both, identical |

No output, marker text, or exit code changed. `--work`/`--file` scratch paths are seat scratch.

Seat self-check, run from the lane root with the draft:
`python3 -I .ufo/waves/round-68/w1/R68ExecGate1/draft/quality/check-deliverables.py --file
.ufo/waves/round-68/w1/R68ExecGate1.md --seat-dir .ufo/waves/round-68/w1` →
`CHECK101: reports=1 declared=4 exists=4 absent=0 undeclared=0 verdict=OK`, rc 0. (`--file` resolves
relative candidates against the process cwd, so the same command from another directory reports
ABSENT — identical behaviour to the committed file.)

## 4. Proof c — diffs and draft hashes

`git diff --no-index --numstat <committed> <draft>`:

```
check-anchor-cover.py 2	1
check-control-receipts.py 1	0
check-deliverables.py 4	2
```

The added lines are exactly the guard constructions shown in § 1 (one split line in
`check-anchor-cover.py`, one line in `check-control-receipts.py`, the two `env=` continuations in
`check-deliverables.py`); nothing else was added, removed or reflowed.

```
46de6c3579c2e9d0e1a8053f98076d64f634985cd1f5346cb4bdbe35b4181e57  draft/quality/check-anchor-cover.py
2e19660e5601f4684dab35b0130a50df290746a72d7c8184821b054a0b8cbc64  draft/quality/check-control-receipts.py
159174b83b16186d39fe189d2b968724df13a931911bd3693200dc6300091626  draft/quality/check-deliverables.py
```

## 5. Runtime replace-ref probe (`check-deliverables.py`, auxiliary)

Scratch repo `replace.qirN`: `r.md` = `Report: missing.md` (real blob), `existing.md` present,
`forged.md` = `Report: existing.md`; `git replace <real-blob> <forged-blob>` planted, so
`git show HEAD:r.md` returns `Report: existing.md`.

| runner | result | rc |
|---|---|---|
| committed bytes | `DECLARATION report=r.md named=existing.md grammar=trailer status=EXISTS`, `verdict=OK` (reads the forged object) | 0 |
| draft bytes | `DECLARATION report=r.md named=r/missing.md grammar=trailer status=ABSENT`, `verdict=FAIL` (reads the real object) | 1 |

So the guard changes the bytes scored, not only the census classification.

## 6. Findings and risks

- **F1 — the frozen C2 counting command cannot run as published.** The declaration's C2 counting
  command passes `--scratch-root DIR`, but the frozen tool's CLI accepts only
  `--repo --rev --controls --selftest`. Replaying the declaration form at the freeze:
  `python3 -I quality/counters/c2-r68-reader-guard.py --repo . --rev e0727cda… --controls
  …/c2-controls.json --scratch-root <s>` → rc 2,
  `error: unrecognized arguments: --scratch-root …`. The seat-specified command (without
  `--scratch-root`) runs and scores. I did not touch the declaration, the control JSON or the
  counter; this needs an L1 decision (erratum vs counter CLI) outside my write scope.
- **F2 — partial census state is expected.** `guarded=4 unguarded=9` at a fixture carrying only
  my three repairs; the target `guarded=13 unguarded=0` requires the nine sibling repairs listed
  in § 2. `population=20 readers=13` already hold.
- **F3 — `check-anchor-cover.py`'s env is deliberately fresh** (PATH/HOME/TMPDIR/LC_ALL only); the
  guard was added inside that literal, so the gate keeps its bare-environment property and gains
  exactly one key.
- **F4 — no `--selftest` in these three gates**; parity was therefore established with compile,
  help, and six real read-only invocations (green and red paths each for anchor-cover,
  control-receipts and deliverables), all byte-identical to the committed runs.

## 7. Integrity

```
217d1625997627a6b7909198ad9954a51adaff1f01224adc37f1d86964a2c9a6  quality/check-anchor-cover.py
2233db1d489fa325c3b4bd9b5b1dccc68eb9311864a0d975303907463fa65af2  quality/check-control-receipts.py
6fe0a4b4122762dc0ea456c9ad44b35d66458c0d9c60672727d7f2d7d042e88f  quality/check-deliverables.py
```

All three equal the dispatch-time hashes: the lane files were not modified. Scratch
`/fast/scratch/hyaku/mado-r68/R68ExecGate1/` (fixture repos, probe repo, captured stdout) was
removed before this report was yielded.

## Deliverables

- `R68ExecGate1/draft/quality/check-anchor-cover.py`
- `R68ExecGate1/draft/quality/check-control-receipts.py`
- `R68ExecGate1/draft/quality/check-deliverables.py`

Report: .ufo/waves/round-68/w1/R68ExecGate1.md
