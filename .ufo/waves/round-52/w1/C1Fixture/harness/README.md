# C1Fixture — red/green fixture harness for the round-52 C1 counter (prototype)

Seat `C1Fixture`, mado round 52 w1. This directory holds the **harness only** — it
does not implement the C1 predicate and it does not implement a counter. It measures a
candidate counter against five fixtures and reports whether that counter shows the
discrimination the frozen claim requires.

## What the harness measures

| case | fixture | expected outcome |
|---|---|---|
| `green` | the lane cloned at the frozen base rev, production `quality/tool-ledger.md` untouched | exit 0, `verdict=TARGET_MET`, no defect field non-zero |
| `red` | the same clone with the frozen control `.ufo/waves/round-52/controls/c1-do-nothing.md` committed in place of the production ledger | exit 1, `verdict=TARGET_MISSED`, **and** a self-pointer defect and an instrument-specific-context defect named — a missing-ledger verdict does not count |
| `mut-selfptr` | one production row's accountability pointer redirected at `quality/tool-ledger.md` itself | exit 1, self-pointer signal |
| `mut-generic` | one production row's description replaced by `does things.` | exit 1, context signal |
| `mut-duprow` | one production row duplicated | exit 1 |

The red expectation is the discriminating one. `verdict=TARGET_MISSED` alone is
satisfied by any counter that simply notices the control ledger does not cover the
population; the frozen claim requires the failure to be *for the self-pointer and
context reason*. The harness therefore requires a self-pointer signal **and** a context
signal, taken either from a summary field or from a detail line, and it rejects a red
verdict whose only cause is `ledger=absent`.

The `mut-*` fixtures exist because the frozen control cannot separate the two defect
classes from each other: it fails for coverage reasons anyway. Each `mut-*` fixture
injects exactly one defect into an otherwise complete production ledger.

## Usage

```
python3 -I harness/c1-fixture-harness.py \
    --repo  /home/vgpnk/Projects/shokunin/mado-shokunin \
    --rev   85d57a818c3707397e21c840b6498b105ba798aa \
    --counter <absolute path to the candidate counter .py> \
    --control  /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-52/controls/c1-do-nothing.md \
    --profile  harness/profiles/default.json \
    --work     /fast/scratch/hyaku/mado-r52/C1Fixture/run \
    --out      .ufo/waves/round-52/w1/C1Fixture/receipts/<run-name> \
    [--cases green,red,mut-selfptr,mut-generic,mut-duprow] \
    [--overlay <repo-relative path>[,<repo-relative path>]] \
    [--expect-final <file with "case<TAB>exact final line">]
```

`--overlay` copies lane working-tree files into the fixtures and commits them there, for
a counter that needs a companion file (a checker, a helper) absent at the frozen base
revision. The ledger can never be overlaid.

`--expect-final` asserts the exact final line per case; see
`profiles/expect-r51-green.txt` for the base counter's green line.

Exit codes: `0` every case matched its expectation; `1` a case mismatched; `2` setup
error (bad arguments, clone/commit failure, unreadable inputs).

## Counter-agnostic by construction

The harness never imports the counter and never reads its source. It passes
`--repo <fixture> --rev <fixture-rev> --work <case-work>` and reads stdout, stderr and
the exit status only. The summary-line field names are matched through an **alias set**
in the profile JSON, so a counter author is free to spell the fields
`self_pointer=` or `selfptr=`, and `generic_context=` or `non_specific=`. If a counter
reports the defect only in `detail:` lines, the profile's `detail_self_regex` /
`detail_context_regex` pick it up instead.

`required_red_signals` in the profile says which signals each red-family case must
carry. It is a dict keyed by case, so a reviewer can relax or tighten the requirement
without touching the harness.

## No source-tree writes

* The lane repository is only ever read. Both fixtures are `git clone --shared
  --no-checkout` copies inside `--work`, and the fixture commits are built with plumbing
  (`hash-object`, `update-index`, `write-tree`, `commit-tree`), so they write into the
  fixture's own object store and not the lane's.
* Before every git mutation in a fixture the harness asserts
  `git rev-parse --show-toplevel` prints that fixture's own path.
* A git-native integrity snapshot of the lane working tree is taken before the cases
  and again after them: the index's blob ids for every tracked path, the unstaged diff
  path set, the staged diff path set, and the untracked path set outside the round's
  wave directory. `lane_unchanged` in `harness-summary.json` is the proof, and a
  mismatch fails the run. The wave directory is excluded because sibling seats write
  there concurrently; that exclusion is reported as a visible count
  (`wave_untracked_count`), not applied silently.
* The fixture working tree is empty by construction, so any file left there is a write.
  `fixture_worktree_residue` in the summary is that check. (`git status` cannot be used:
  on a `--no-checkout` clone every tracked path reads as deleted.)
* The counter runs with `HOME`, `TMPDIR` and the `XDG_*` homes redirected under the
  case's own `--work` directory, so a counter that writes a scratch file writes it
  inside the sandbox.
* `--work` must not be `/tmp`, `/var/tmp` or `/dev/shm`; the refusal happens before
  anything is created and exits 2.

## Self-test

`harness/selftest/` holds four throwaway counters used only to prove the harness itself
works. They are test assets, not candidate deliverables:

* `stub-correct.py` — green pass, red fail naming both defects: the harness must report
  `verdict=PASS`.
* `stub-always-accept.py` — always exit 0 with `verdict=TARGET_MET`: the harness must
  report `verdict=FAIL` on the red case.
* `stub-writes-source-tree.py` — writes into the watched repository (reached through the
  fixture's `origin` remote): the harness must report `lane_unchanged=False`.
* `stub-writes-in-work.py` — writes into the `--work` directory it was handed: the
  harness must list that file under `scratch_files_after`.

Run `harness/selftest/run-selftest.sh` to reproduce all four.
