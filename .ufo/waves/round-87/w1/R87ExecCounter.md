# R87ExecCounter — C1 counter report (round 87, w1)

Seat: executor. Written: `quality/counters/c1-r87-mako-criteria.py` (NEW, sha256
`71aa92738256b6eb5eebd92909d8586dea127fa6f524394fa59bbfabc5508fe0`, 686 lines).
Not run against the lane's real REV (L1 runs it after the wave). Not committed.

## Predicate

Docstring carries the declaration's C1 sentence verbatim: "TARGET_MET iff the candidate tool's correct count
equals N, all M mutants are killed, and both do-nothing controls score strictly below N." Score = 10 × correct / N.

## Implementation summary

- Git: every call uses a scrubbed env (GIT_DIR, GIT_WORK_TREE, GIT_INDEX_FILE, GIT_OBJECT_DIRECTORY,
  GIT_ALTERNATE_OBJECT_DIRECTORIES removed; GIT_NO_REPLACE_OBJECTS=1). REV resolved with `rev-parse --verify REV^{commit}`.
- Tool bytes: `git show REV:tools/mado-mako.py`. Mutants: `git show REV:.ufo/waves/round-87/controls/mako-mutants-r87.json`
  unless `--mutants PATH` is given.
- Verdict per case: exit 0 AND JSON stdout with `effective` object and `refusals` list AND every `expect.effective`
  key equal (type-strict, canonical JSON) AND refusals empty for "none" / non-empty for "present". 20 s timeout → incorrect.
- Controls (in-counter, never call the tool): naive-toplevel, globals-include. Control values are compared as text
  (bool → true/false, other non-strings → JSON text); a missing key or any refusal expectation scores incorrect.
- Mutants: `old` must occur exactly once in the tool text, else status `setup-error count=N`, counted not killed.
  Killed iff the per-case correct vector differs from the unmutated vector.
- Generation directory `mkdtemp(prefix="mado-mako-r87-", dir=<scratch-root>)`, removed in `finally`. Tool TMPDIR is the
  generation directory (inside the scratch root). Nothing is written inside the repo.
- Exit: 0 TARGET_MET, 1 TARGET_MISSED, 2 setup error (stderr `MADO_MAKO_CRITERIA: SETUP_ERROR ...`, no verdict line).
  Setup errors include: bad REV, non-directory repo, scratch root missing, unreadable cases, schema mismatch, unsafe
  paths, N outside 20..24, mutant count ≠ 10 (declared M = 10).

## Assumptions to check when the lane files land (not yet present at seat time)

The lane has no `.ufo/waves/round-87/controls/mako-cases-r87.json`, no `mako-mutants-r87.json` at REV and no
`tools/mado-mako.py` yet (controls/ is empty). The counter therefore encodes this case schema, which the L1 must
confirm against the scout's file before the real run:

    {"schema": "mako-cases-r87-v1", "cases": [
      {"id": "kebab-id", "config": "rel/path", "home_files": {"rel/path": "text" | {"symlink_to": "rel/path"}},
       "args": {"app-name": str, "urgency": "low|normal|critical", "mode": str|[str]},
       "expect": {"effective": {key: value}, "refusals": "none" | "present"}}]}

and the tool stdout contract `{"effective": {...}, "refusals": [...]}`. Mutant schema:
`[{"id", "old", "new"}]` or `{"mutants": [...]}`. A different shape is a setup error (exit 2), not a silent miscount.

## Selftest (run once, TMPDIR = scratch)

Command: `TMPDIR=/fast/scratch/hyaku/mado-r87/R87ExecCounter python3 -I quality/counters/c1-r87-mako-criteria.py --selftest`
Exit code: 0. Output:

    PASS fixture toplevel equals fixture dir
    PASS scrubbed env resolves REV although GIT_DIR points at a decoy
    PASS git environment sets GIT_NO_REPLACE_OBJECTS=1
    PASS git show returns the committed tool bytes
    PASS fixture case set loads with N=2
    PASS fixture mutants load from REV
    PASS correct fixture tool scores N/N
    PASS section-ignored mutant is killed
    PASS non-unique old is a setup error and not killed
    PASS an unkilled mutant makes the verdict TARGET_MISSED
    PASS do-nothing controls score below N on fixture
    PASS evaluate leaves the scratch root as it found it
    PASS all mutants killed with correct tool gives TARGET_MET
    PASS deliberately wrong tool scores below N
    PASS exit map: TARGET_MET=0, TARGET_MISSED=1, setup=2
    PASS CLI: bad REV exits 2
    PASS CLI: missing scratch root exits 2
    PASS CLI: unreadable cases exits 2
    PASS CLI: N=2 outside 20..24 exits 2
    SELFTEST: passed=19/19

Scope note: the exit-code 0 and 1 paths are asserted through `exit_for` plus the fixture verdicts; the CLI is exercised
for the 2-paths only, because the real N range (20..24) cannot be satisfied by a 2-case fixture.
The selftest fixture was built in a fresh `mktemp -d` fixture repo under scratch, with
`git -c user.name=mado-selftest -c user.email=selftest@invalid commit`; the fixture repo was removed with the scratch.

## Installs

None. Python 3.14.8 (host) and git only. No pacman use.

## Scratch

`/fast/scratch/hyaku/mado-r87/R87ExecCounter` removed after the selftest; listing of the seat dir is empty.

## Not done (by item scope)

- Counter not run against the lane REV (L1 duty).
- No mutating git/jj run anywhere; only `git -C ... init/add/commit` inside the fixture repo and read-only `show`/`rev-parse`.
