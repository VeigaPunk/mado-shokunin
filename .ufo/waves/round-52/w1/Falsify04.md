# Falsify04 — C1 counter isolation/scratch behavior

## Attacked clause

Frozen C1 operability predicate (`.ufo/waves/round-52/registration.md`, "Frozen predicates" §C1; `.ufo/waves/round-52/claims-frozen.md` §C1): a new counter for the tracked instrument ledger "runs at a requested pinned revision" and is scored by passing the production ledger at base `85d57a818c3707397e21c840b6498b105ba798aa` and failing `controls/c1-do-nothing.md` — under the round safety contract "Source checkout read-only" and lane scratch discipline. Target per seat assignment: the counter's **isolation/scratch behavior**, i.e. whether the bytes it measures and the directories it writes are actually governed by `--repo`/`--rev`/`--work` and confined to scratch.

Objects examined: committed predecessor `quality/counters/c1-r51-ledger.py` (the only C1 counter that exists at base), the gate `quality/check-tool-ledger.py`, and the two runnable round-52 counter drafts in-flight this wave: `.ufo/waves/round-52/w1/Falsify41/candidate-c1-r52.py` (273 lines, the fuller draft) and `.ufo/waves/round-52/w1/C1Simplify/c1-r52-ledger.py` (196-line no-scratch reference). The committed target counter is absent at base, so these drafts are the best available stand-ins for the artifact C1 will be scored on; findings 1–3 are demonstrated dynamically against the Falsify41 candidate, finding 4 against the committed r51 counter.

## Finding 1 — inherited `GIT_DIR` silently re-targets the measured repository (attribution hijack). Reproduced: YES

Source evidence: the candidate's `git()` (`.ufo/waves/round-52/w1/Falsify41/candidate-c1-r52.py:40-45`) runs `git -C <repo> …` **with no `env=` argument**, so every git subprocess inherits the caller's environment, including `GIT_DIR`/`GIT_WORK_TREE`, which override `-C` repository discovery. The committed r51 counter explicitly prevents exactly this: `git_env()` strips every `GIT_*` variable (`quality/counters/c1-r51-ledger.py:85-96`). The candidate drops that scrub.

Setup: two seat-local fixture repos under `/fast/scratch/hyaku/mado-r52/Falsify04/hijack/`: `green` (valid 1-row ledger, built by `build-fixture.sh`) and `red` (the frozen do-nothing control shape committed, 2 generic self-pointer rows). `GREEN_REV` only exists in `green`, `RED_REV=f56734f67c76…` only in `red`. Candidate: `Falsify41/candidate-c1-r52.py`.

Commands and actual results (receipts `e4a`, `e4c`):

```
# control, clean env
python3 -I candidate-c1-r52.py --repo green --rev $RED_REV --work w/c1
→ exit=2  C1_R52: setup=error detail=git rev-parse … failed        # red rev absent from green: correct

# attack, attacker/scorer environment exports GIT_DIR
GIT_DIR=red/.git python3 -I candidate-c1-r52.py --repo green --rev $RED_REV --work w/c3
→ exit=1  detail: dangling path=tools/mado-verify.sh (x2)
          detail: uncovered path=tools/x.py
          C1_R52: population=1 ledger_rows=2 uncovered=1 dangling=2 bad_pointer=0
                  self_pointer=0 no_context=0 dup=0 verdict=TARGET_MISSED rev=f56734f67c76
```

The revision resolved and the population/ledger/verdict all came from `red` (the GIT_DIR repo) although `--repo green` named a different repository that does not even contain the pinned revision. A verdict printed against `--repo` was in fact measured on an environment-selected repository, with no warning. Variants: adding `GIT_WORK_TREE=red` aborts at clone ("working tree … already exists", receipt `e4b`); `GIT_WORK_TREE` pointing at a nonexistent dir aborts at the clone-toplevel self-check (`e4d`). The red repo itself was left clean (HEAD and worktree unchanged). This bypasses the predicate clause "runs at a requested pinned revision" in the sense that the *measured object* is not the requested repository; it is an environment-inheritance defect the r51 lineage already fixed and the draft regressed.

## Finding 2 — `--work` aliasing `--repo` writes scratch inside the source checkout; abnormal exit leaves litter. Reproduced: YES

Source evidence: candidate `main` takes `--work`, `os.path.abspath` + `os.makedirs(exist_ok=True)` only (`candidate-c1-r52.py:197-198`) — no refusal policy (no `/tmp`, `/var/tmp`, `/dev/shm`, no home rule; grep: none), no writability guard (uncaught `PermissionError` traceback, exit 1, on a non-writable `--work`; receipt `e3`), no check that `--work` is disjoint from `--repo`. `clone_at` writes `clone-<uuid10>` into `--work` with `git clone --shared --no-checkout` (`:61-63`); cleanup happens only in the `finally` on graceful exit (`:236-238`).

Setup: tiny green fixture repo F (`build-fixture.sh`); run the candidate with `--repo F --rev HEAD --work F` (a natural scorer typo such as `--work .` against the lane). A git shim (`git-shim.py`) provides a deterministic kill window by sleeping before the first `git -C <clone> show`; driver `work_alias_attack.py` forks the counter so the clone name is known.

Results (receipts `e1a`, `e1b`):

- clean run: `clone-8d487fe8e0` observed **inside F** during the run; child exit 0 (`TARGET_MET` on the green fixture); clone removed at exit; `git status --porcelain` clean.
- SIGKILL mid-run (shim window): `clone-32d18dcfe9` observed inside F; child exit −9; litter persists: `litter-after-sigkill=['clone-32d18dcfe9']`, `git status --porcelain` → `?? clone-32d18dcfe9/`.

The counter therefore violates the source-readonly boundary the moment `--work` is (mis)placed at/inside the source repo, and only a graceful exit restores cleanliness. The committed r51 counter shares the flaw by construction — its argv trace (`e5-r51-git-argv-trace.txt`) shows `git -C <repo> clone … <repo>/clone-719174` with all reads against `<repo>/clone-719174`, and `r51_diag.py` observed `clone-729797` inside the repo at t=0.03s; r51 additionally uses a guessable `clone-<pid>` name and pre-deletes any same-named path (`quality/counters/c1-r51-ledger.py:106-124`).

## Finding 3 — the `--shared` scratch clone is not self-contained: all reads depend on the source object store. Reproduced: YES

`clone_at` uses `git clone --shared` (`candidate-c1-r52.py:63`; same in r51 `:113`), so `.git/objects/info/alternates` in the scratch clone points at the source repo; every `git show`/`ls-tree` during the run dereferences the *source* object store. Demonstrations:

- static mechanics: after `rm -rf` of the source repo, `git -C <clone> show <rev>:file.txt` fails, exit 128, "unable to normalize alternate object path" (receipt `e2b`).
- candidate live: driver `source_death_attack.py` waits for the clone, records `alternates=…/fixture-bin/repo/.git/objects`, deletes the source repo mid-run → candidate prints `C1_R52: setup=error detail=git ls-tree … unable to normalize alternate object path … fatal: not a tree object`, exit 2 (receipt `e2a`).

Impact: a verdict run is availability-coupled to the source repository for its whole lifetime (any prune/pack disturbance or disappearance of the source object store converts a measurement into setup error 2), and — combined with Finding 2 — the "isolated scratch clone" story is weaker than the docstrings imply. Integrity of reachable objects is not attacked (content-addressed); this is an isolation/robustness failure, honestly bounded as such.

## Finding 4 — scratch-root policy is advisory-only across the lineage (context, not a separate bypass)

The gate `quality/check-tool-ledger.py` refuses selftest work under `/tmp`, `/var/tmp`, `/dev/shm` and `$HOME` (`:70`, `resolve_work :414-428`). The r51 counter never enforces any of that for its own `--work`; `REFUSED_ROOTS` only selects a post-hoc hint printed when the selftest already failed (`quality/counters/c1-r51-ledger.py:68`, `:404-407`), and the candidate drops even the hint. If the round-52 counter claims no scratch-root policy this is harmless (cf. Falsify36's identical static note); it matters only if scored against the lane's scratch discipline. Reported for completeness; no dynamic reproduction added beyond Finding 2's placement tests.

## Production sanity (so findings are not an artifact of a broken candidate)

`python3 -I Falsify41/candidate-c1-r52.py --repo <lane> --rev 85d57a818c3707397e21c840b6498b105ba798aa --work <scratch>` → exit 0, `population=82 ledger_rows=82 … verdict=TARGET_MET` (receipt `e0-production-base.txt`), matching `.ufo/waves/round-52/receipts/c1-base.txt`. The candidate discriminates nothing about scratch placement — which is precisely the gap attacked above.

## Reproduced summary

| # | Failure mode | Object | Reproduced |
|---|---|---|---|
| 1 | inherited `GIT_DIR` re-targets measured repo (attribution hijack) | candidate-c1-r52.py | yes, dynamically |
| 2 | `--work`==`--repo` writes clone into source checkout; SIGKILL leaves litter | candidate (dynamic) + r51 (trace/diag) | yes, dynamically |
| 3 | `--shared` clone dies with source object store mid-run | candidate (dynamic) + static | yes, dynamically |
| 4 | scratch-root refusal advisory-only | r51 + candidate (static contrast with gate) | n/a (context) |

## Limitations and dissent

- The scored round-52 counter is absent at base; findings 1–3 attack the Falsify41 draft (`--shared` clone into `--work`, no env scrub) and the committed r51 predecessor, both representative of what C1 is converging on. If the delivered counter scrubs `GIT_*`, enforces `--work`≠`--repo`, or uses a local `--no-shared` clone, findings 1–3 close; nothing here claims otherwise.
- The C1Simplify reference draft is immune to findings 1–3 by design (no clone, no scratch, `git show` with inherited env — Finding 1's env-scrub gap still applies in principle, unexercised).
- Peer overlap checked: Falsify12 (checker-rev binding, static), Falsify36 (advisory refused-roots, static, declined execution), Falsify03 (control availability at base). All items above are distinct; findings 1–3 are dynamic reproductions.
- No tracked lane files, fleet files, source-checkout writes, git/jj mutations, installs, or producer/compositor actions. All fixtures and clones lived under `/fast/scratch/hyaku/mado-r52/Falsify04/` and were removed after receipt copies were made. No package queries or web access.

## Deliverables

- `.ufo/waves/round-52/w1/Falsify04.md` — this report.
- `.ufo/waves/round-52/w1/Falsify04/build-fixture.sh` — green fixture builder.
- `.ufo/waves/round-52/w1/Falsify04/git-shim.py` — deterministic kill-window git shim.
- `.ufo/waves/round-52/w1/Falsify04/git-trace-shim.py` — argv-logging git shim.
- `.ufo/waves/round-52/w1/Falsify04/work_alias_attack.py` — Finding 2 driver (clean + SIGKILL).
- `.ufo/waves/round-52/w1/Falsify04/source_death_attack.py` — Finding 3 driver.
- `.ufo/waves/round-52/w1/Falsify04/r51_diag.py`, `r51_work_alias_observe.py` — r51 observation drivers.
- `.ufo/waves/round-52/w1/Falsify04/receipts/` — evidence copies `e0`–`e5` named above.

## Report

- `.ufo/waves/round-52/w1/Falsify04.md`
