# MeasureMutantsOut — `measure-mutants.py` no longer writes a receipt by default; lane `--out` is refused without `--force-lane-receipt`; measurement payload unchanged

## Change (one lane file)

`.ufo/waves/round-18/measure-mutants.py`

- old sha256 `075815bd5bbcf80fbf00a80ac9400ff9ec82082562a6691c1f5cc290da601d73`
- new sha256 `595a6a9be8b8e6bc7b43043f293f7ac3afc1672cf2d756a0830e4e6af3766687`
- `git diff --stat -- .ufo/waves/round-18/measure-mutants.py` → `1 file changed, 41 insertions(+), 16 deletions(-)`

What changed:

- `:21-27` docstring now states the stdout default and the refusal rule.
- `:46` dead `OUT_DEFAULT` deleted (no caller remained; `grep -n OUT_DEFAULT` → no match).
- `:494-501` `lane_worktree()`: `git -C <lane> rev-parse --show-toplevel` (falls back to `lane` only if git cannot name a worktree; the script already requires git for `archive`/`show`).
- `:506-527` `--out` is optional; `--force-lane-receipt` added; `out.resolve()` and the containment refusal run before any instrument run or write.
- `:589-592` human progress lines now go to stderr.
- `:671-679` without `--out` the payload JSON is the only stdout write and no file/dir is created; with `--out` the atomic sibling-tmp + `os.replace` write is unchanged, `wrote <path>` goes to stderr, and the summary JSON stays on stdout (previous stdout contract for `--out` runs).

Refusal condition: `out == worktree or worktree in out.parents` against `--lane`'s worktree, bypassed only by `--force-lane-receipt`.

## Evidence

All runs in `/tmp/mmclone-r19` (clone of the lane checked out at `17661e0fa83f978fb659f5bb8fef47f0969f6945`; `git rev-parse --show-toplevel` → `/tmp/mmclone-r19`; its `measure-mutants.py` sha256 `075815bd…`). No run used the real lane as `--lane`, and the real lane's `evidence/measure-mutants.json` is still `58929eeaf9e822042a43e45f2363885ce1b4094a3fa5e3531ca3e2845bb133e5`.

1. **Bare run writes nothing / prints JSON.** `python3 -I <lane>/.ufo/waves/round-18/measure-mutants.py --lane /tmp/mmclone-r19 > /tmp/mm-stdout.json 2> /tmp/mm-stdout.err` → rc 0, stdout is one parseable JSON document (56,449 bytes), stderr holds the six `M<n> BITES: …` lines, and `/tmp/mmclone-r19/.ufo/waves/round-18/evidence/` gained nothing (`…measure-mutants.json.tmp`: no such file; clone `git status --porcelain` clean).

2. **A/B on the reported incident shape.** Old script (`/tmp/measure-mutants-old.py`, extracted from `17661e0`, sha256 `075815bd…`) run bare with `--lane /tmp/mmclone-r19` rewrote the clone receipt: `58929eea…` → `f19c7e99…`, rc 0. After `git -C /tmp/mmclone-r19 checkout -- …/measure-mutants.json` (restored `58929eea…`), the new script run bare left it at `58929eea…`, rc 0.

3. **Refusals** (all rc 1, no file created, refusal before measurement):
   - absolute inside worktree: `refusing --out /tmp/mmclone-r19/.ufo/waves/round-18/evidence/refused.json: inside the git worktree being read (/tmp/mmclone-r19); pass --force-lane-receipt to write a lane receipt`
   - symlink into worktree (`/tmp/mm-escape-link -> /tmp/mmclone-r19/.ufo`): same refusal on the resolved path.
   - relative path from the real lane cwd: `python3 -I .ufo/waves/round-18/measure-mutants.py --out .ufo/waves/round-18/evidence/relative-refuse.json` → refusal naming `/home/vgpnk/Projects/shokunin/mado-shokunin`; `ls` → no such file.

4. **Allowed writes.** `--out /tmp/mm-out.json` (outside) → rc 0, file written atomically (no `.tmp` sibling), stdout summary JSON equals the file's `.summary`. Exact spelling intended for QUALITY 25, run from the clone root: `python3 -I <lane>/.ufo/waves/round-18/measure-mutants.py --out .ufo/waves/round-18/evidence/measure-mutants.json --force-lane-receipt` → rc 0, `wrote /tmp/mmclone-r19/.ufo/waves/round-18/evidence/measure-mutants.json` on stderr, receipt rewritten with `"sha256": "595a6a9b…"` (the new harness). Clone restored afterwards.

5. **Committed receipt comparison.** `committed['summary'] == new_bare_stdout['summary']` → `True`; both are
   `{"baselines_agree": true, "bites": 6, "expectations_met": 6, "expected_but_unmet": [], "mutants": 6, "no_bite": [], "unexpected_tight_only": []}`.
   Non-normalized new-vs-committed diff (deep JSON walk) has 11 leaves, all `mutants[*].mutant.{loose,tight}.stdout_sha256`; every summarized `c2` is identical. Cause is run identity, not the edit: the instrument's stdout embeds its own `rev` (`git show d9a5a18:.ufo/waves/round-17/measure.py` → `:307 'rev': rev`), and the throwaway mutant commits carry wall-clock dates. Two back-to-back new-script runs (`/tmp/mm-stdout.json` vs `/tmp/mm-stdout2.json`) differ in exactly those 11 leaves while `c2` is equal for all six mutants.

6. **Old vs new payload identity under fixed inputs.** With `GIT_AUTHOR_DATE=GIT_COMMITTER_DATE=2000-01-01T00:00:00+0000`, `--keep --workdir /tmp/mm-fixed` and explicit `--out`, old and new receipts were deep-compared over the whole document: differing leaves are exactly `generated_at`, `started_at`, `harness.path`, `harness.sha256`, `harness.argv[0]`, `harness.argv[4]` (the two `--out` spellings). `mutants` (including `diff_sha256`, `baseline_commit`, `mutant_commit`, instrument `stdout_sha256`, `c2`, `exit`, `expectation_met`) and `summary` compare equal. The fixed dates make the throwaway commit hashes deterministic, so this isolates the edit: no measurement byte moved.

## QUALITY 25 command spelling L1 should append

`corpus/QUALITY.md:139-140` still reads `python3 -I .ufo/waves/round-18/measure-mutants.py` → `.ufo/waves/round-18/evidence/measure-mutants.json`; that bare command now prints the JSON to stdout and writes no receipt. Proposed append-only correction (Criterion 25 block):

    Round-19 wave-1 correction (append-only): criterion 25's command no longer
    writes by default. Regenerate the lane receipt deliberately with
    `python3 -I .ufo/waves/round-18/measure-mutants.py --out .ufo/waves/round-18/evidence/measure-mutants.json --force-lane-receipt`
    (`no_bite` lists any tightening the loose instrument already rejects). A
    bare `python3 -I .ufo/waves/round-18/measure-mutants.py` prints the receipt
    JSON to stdout and writes nothing; `--out` inside the git worktree being
    read is refused unless `--force-lane-receipt` is given.

For a check that must not touch the lane at all, the equivalent is `python3 -I .ufo/waves/round-18/measure-mutants.py > /tmp/measure-mutants.json` (rc 0 iff all six bite; `.summary.no_bite` empty).

`SKILL.md:571` (`mado-measure-mutants` row) needs no edit for exit semantics: the bare command still exits 0 when all declared mutants meet expectations, and the listed fields (`bites`, `no_bite`) are in the printed JSON; only its implied receipt side-effect is gone.

## Risks

- The committed `.ufo/waves/round-18/evidence/measure-mutants.json` still records `harness.sha256 075815bd…`. That is truthful for the bytes that produced it and the measurement payload reproduces (item 6), but after the edit `git show <new-commit>:…/measure-mutants.py | sha256sum` is `595a6a9b…`, so a producer-identity reading of that receipt is stale. Regenerating with the spelling above changes that evidence file (timestamps, run-specific commit hashes, `stdout_sha256`) while leaving `summary`/`mutants` content equal; L1 decides whether to regenerate/commit or leave the historical receipt and cite the reproduction.
- Progress output moved from stdout to stderr for `--out` runs; stdout is now always one JSON document (full payload without `--out`, summary with `--out`). No repo consumer parses those human lines (`grep -rn measure-mutants tools/ scripts/` → none).
- The guard covers only the worktree named by `--lane`. A deliberate `--lane <clone> --out <real lane>/…` is not refused (it is not the worktree being read); the incident shape — default `--lane` real lane plus default `--out` — is gone because there is no default `--out`.

## Limits

- Did not run against the real lane and did not regenerate the lane receipt; the real `evidence/measure-mutants.json` remains `58929eea…` (confirmed before/after).
- Did not run `tools/mado-verify.sh`, round-18 suites, formatters or linters (wave rule; parent owns post-integration gates).
- Full byte-identical receipts across reruns are not achievable even with the old script: `generated_at`/`started_at`, the harness self-identity (`path`, `sha256`, `argv`), throwaway commit hashes, and instrument stdout hashes move per run. Only the measurement body is invariant, and that was shown invariant.
- [INFERENCE] No other in-lane script or gate invokes `measure-mutants.py`; based on `grep -rn` over `tools/ scripts/ corpus/ SKILL.md SCORECARD.md LOG.md PROVINCE.md` and the round-19 tree.

## Installs

none.
