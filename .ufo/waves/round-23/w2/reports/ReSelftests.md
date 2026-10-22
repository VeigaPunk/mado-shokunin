# ReSelftests: round 23, wave 2 (C1 selftest guard, operability)

Seat: MadoR23.ReSelftests (leaf reviewer). Item: run the eleven legacy tripwire selftest suites against the classifier extracted from the landed tip `2f1134f38930fc8b067d2d7f5bba126338faabdd`. Judged on: operability.

## Verdict

PASS for the landed tip. The eleven suites give 247/247. Every child exits 0 with empty stderr. Two sequential passes are byte-identical. Per-case results match the round-22 legacy receipts case for case. A one-line mutant in the scan exit path is caught by exactly the 126 cases that should catch it, by name.

Operability flag (does not change the tip verdict): the lane's working copy of `tools/mado-tripwire.py` holds uncommitted edits and was still changing during this run. At 09:04:12 -0300 it differed from the tip by 97 insertions and 51 deletions. Lane-path runs therefore measure uncommitted bytes. The working copy also passes 247/247 at the moment I checked. See F1.

## What I ran

All classifier children ran one at a time as `prlimit --as=402653184 --cpu=15 python3 -I <tool> --selftest <suite dir>`, with the scratch directory as working directory and stdin closed.

1. Extract the tip classifier. This is the assigned command. My first attempt failed only because the scratch directory did not exist yet, so I created it and reran:
   `git -C /home/vgpnk/Projects/shokunin/mado-shokunin show 2f1134f38930fc8b067d2d7f5bba126338faabdd:tools/mado-tripwire.py > /fast/scratch/hyaku/mado-r23/w2/ReSelftests/tool.py`
   sha256 `41489991163627f56de79bc360d4f13454fa5d50787a5802927b9cac562ca009`, which matches the C1 pin. Fresh directory, no `__pycache__`.
2. Export the tip tree for the fixtures (read-only, nothing written to the lane):
   `git -C /home/vgpnk/Projects/shokunin/mado-shokunin archive --format=tar 2f1134f38930fc8b067d2d7f5bba126338faabdd | tar -x -C /fast/scratch/hyaku/mado-r23/w2/ReSelftests/tree`
3. Suite directories. Each legacy label `<round>/tripwire/<name>` maps to `tree/.ufo/waves/<round>/tripwire/<name>`. This is the same layout the legacy receipts used under the lane path.
4. Eleven runs in legacy order. Stdout and stderr are in `/fast/scratch/hyaku/mado-r23/w2/ReSelftests/logs/NN-<label>.out|.err`.

## Per-suite counts (tip tool 2f1134f3)

| # | Suite (legacy label) | Passed/cases | rc | Legacy receipt | Same CASE list as legacy | Wall s |
|---|---|---|---|---|---|---|
| 1 | round-17/tripwire/core | 9/9 | 0 | 9/9 | yes | 0.40 |
| 2 | round-17/tripwire/compound | 16/16 | 0 | 16/16 | yes | 0.67 |
| 3 | round-17/tripwire/hardening | 33/33 | 0 | 33/33 | yes | 1.33 |
| 4 | round-17/tripwire/w2-regressions | 30/30 | 0 | 30/30 | yes | 1.22 |
| 5 | round-18/tripwire/r18-failsafe | 1/1 | 0 | 1/1 | yes | 0.08 |
| 6 | round-18/tripwire/frozen | 31/31 | 0 | 31/31 | yes | 1.27 |
| 7 | round-19/tripwire/r19-bashcvar | 45/45 | 0 | 45/45 | yes | 1.83 |
| 8 | round-19/tripwire/r19-helperfn | 34/34 | 0 | 34/34 | yes | 1.41 |
| 9 | round-19/tripwire/r19-vcs | 17/17 | 0 | 17/17 | yes | 0.73 |
| 10 | round-19/tripwire/r19-frozen-f1f2 | 13/13 | 0 | 13/13 | yes | 0.55 |
| 11 | round-19/tripwire/r19-installers | 18/18 | 0 | 18/18 | yes | 0.77 |
| | **Total** | **247/247** | 0 each | 247/247 | | about 10 s |

Every child printed `SELFTEST_SCRIPT_SHA256: 41489991163627f5…`, the tip tool's hash. Stderr was empty in all runs.

## Findings, by severity

### F1 (medium, operability): the lane working copy holds uncommitted, still-changing edits to the classifier

Evidence, all read-only:
- Branch `master` is still `2f1134f38930fc8b067d2d7f5bba126338faabdd`. The committed blob for `tools/mado-tripwire.py` is `3f6e1766…`. The tip commit is dated 2026-10-22 08:49:48 -0300.
- The working copy changed twice during this run:
  - mtime 09:01:03 -0300, size 174005, sha256 `82d5ffa81c558ccc9a855d9ced7f50a2c97e31e647cbb2e7aa1f5957f8862a57`. Diff against the tip: 39 insertions, 33 deletions.
  - mtime 09:04:12 -0300, size 176289, sha256 `eeb6f515bf68ecdd11b16f03a0b622e90fac9aec3182c79f94a6fba7c0573bad`. Diff against the tip: 97 insertions, 51 deletions (`git diff --numstat 2f1134f3 -- tools/mado-tripwire.py`).
- `git status --short` also lists unstaged edits to `SKILL.md` and `corpus/README.md`, plus many untracked round-23 artifacts. I did not inspect those.
- The first uncommitted revision (saved as artifact `artifact://29082`) rewrites the body of `parameter_escapes` as an allowlist and adds a module-level `DYNAMIC_SCOPE_CALLS` set. Its docstring says it answers "round-23 wave-2 counterexamples". I did not read the 09:04 revision in full.

Effect on this item:
- Committed tip 2f1134f3: 247/247.
- Working copy at sha `82d5ffa8…`: 11 suites, all rc 0, 247/247, identical CASE lists to the tip.
- Working copy at sha `eeb6f515…`: copied and run through the same 11 suites. All rc 0, 247/247. Each child's printed hash equals the snapshot, and the lane file's hash was unchanged across the run.

Why it matters: the legacy receipts ran these suites through the lane path, `python3 -I <lane>/tools/mado-tripwire.py --selftest ...`. Anyone repeating that today tests uncommitted, changing bytes. Registration item 10 requires after-values on the classifier extracted from the landed tip. The executor contract says executors never touch the lane working copy. I did not identify the writer. The mtimes fall among other wave-2 reports written 08:58 to 09:03 -0300.

Recommendation for L1 (not acted on by me): identify the writer. Then either commit the edit through the lane with fresh pins and re-measure every guard it touches (repair set, round-21 oracle, round-22 primary, precision, the 1356-file comparator), or restore the tip bytes. Do not cite a lane-path selftest run as evidence for the tip until one of those happens.

### F2 (low to medium, coverage): the eleven suites do not exercise the C1 behaviour

- The eleven suite directories are byte-identical between base `e33ea30461f6` and tip `2f1134f38930`. `git diff --name-only e33ea304 2f1134f3 -- .ufo/waves/round-17/tripwire .ufo/waves/round-18/tripwire .ufo/waves/round-19/tripwire` printed nothing. The only tracked change under `tools/` or those trees is `tools/mado-tripwire.py`.
- So 247/247 shows that the tip gives the expected verdicts on the existing 247 cases, the same as base. It does not test the frame-leak repair or the callback-store recall. Those are the two behaviours C1 changes, and only the 12-case repair set covers them. This command does not run that set.
- F1 shows the limit directly: a substantive rewrite of the escape analysis passes all 247 cases unchanged. The suites cannot tell the two versions apart.
- Recommendation: if this guard is meant to protect later C1 work, add cases in a new suite. Do not edit the old expectations.

### F3 (low, operability): no committed command runs the eleven suites as a set

- I searched `tools/`, `.ufo/waves/round-22/replay.py`, `.ufo/waves/round-22/resource-closure-measure.py`, `.ufo/waves/round-23/repair` and `.ufo/waves/round-23/w1` for the suite names or `--selftest` loops. I found no enumeration. A wider search of committed `*.py` and `*.sh` files returned wave-prompt generators and per-round notes, and the output was truncated at 50 KB. I cannot claim absence with full certainty.
- `.ufo/waves/round-22/evidence/resume/legacy-selftests-summary.json` stores labels only. The per-suite receipts (`selftest-round-*.json`) store the argv, which uses the lane-path tool and lane suite directories with the same caps. Anyone reproducing the eleven runs must rebuild the loop by hand.
- Recommendation: a small committed runner that lists the eleven labels, runs them under the caps, and fails on any count mismatch.

### F4 (info): the two suites that survive a broken scan exit never reach the scan exit path

- Under the mutant in check 4, `round-18/tripwire/frozen` (31/31) and `round-19/tripwire/r19-frozen-f1f2` (13/13) still pass. Both contain only `mode: frozen` cases. `run_frozen` calls `verdict_of` directly (tool.py line 3493) and never reaches `run_scan` (line 3651). That split is intended, not a defect. It means only the scan-mode cases guard the scan exit path.

## Checks beyond the assigned run

1. Export completeness. The `git archive` of `2f1134f3` unpacked to 6204 regular files plus 14 symlinks, 6218 entries in total. That equals the `git ls-tree -r` count. Missing 0, extra 0. No `__pycache__` anywhere in scratch.
2. Lane suite directories against the export. `diff -rq` is clean for `round-17/tripwire`, `round-18/tripwire` and `round-19/tripwire` (rc 0 each). Within those three trees the lane working copy matches the tip byte for byte. The one known working-copy difference, the classifier in `tools/`, is outside these trees (F1).
3. Determinism. A second sequential pass on the tip tool gave stdout byte-identical to the first pass for all eleven suites. Every rc was 0 and stderr was empty.
4. Sensitivity (negative control). `tool-neg.py` (sha256 `4242364ebd2ddf0e8963dfb9d66f29f5d59a0da8ad7468ed46f48f723654da30`) equals the tip except at line 3178, where `return code` became `return 0` in `run_scan`. Result: 121 of 247 pass and 126 fail. Nine suites exit 1; the two frozen suites exit 0. The failing set, matched by name, equals exactly the 126 scan-mode cases with `want_exit: 1`. There are no extra failures and no misses. This shows the scan suites catch a broken exit mapping precisely. It is one mutant, not a mutation score.
5. Current working copy. The numbers in F1 for sha `eeb6f515…`.
6. Case modes across the eleven suites: scan with want_exit 1 = 126, scan 0 = 72, scan 2 = 4; frozen 0 = 8, frozen 1 = 7, frozen 2 = 30. Total 247.

## Residual risk and verification gaps

- Not run here: the repair set, the round-21 oracle, the round-22 primary and precision guards, the 1356-file comparator and the resource populations. Other items own these. I did not check whether the uncommitted working-copy edit changes any of them.
- Memory: I did not measure peak RSS of the children under the 384 MiB cap. No run reported an allocation failure, and stderr was empty throughout.
- The equivalence claims in checks 2 and 5 describe the moment I checked. The working copy changed twice during this run.
- Environment: Python 3.14.8 at `/usr/bin/python3`; util-linux `prlimit` 2.42.4 at `/usr/bin/prlimit`.

## Writes, reads, installs

- Writes: only `/fast/scratch/hyaku/mado-r23/w2/ReSelftests/` (`tool.py`, `tool-neg.py`, `tree/`, `logs/`, `wt/`, `receipt-ReSelftests.json`, `receipt-ReSelftests-determinism-mutant.json`) and this report. No other lane file was written.
- Lane reads, all read-only: `git show` (tip blob), `git archive` piped to `tar` in scratch, `git ls-tree -r -z`, `git ls-files -s`, `git diff` (names, numstat, stat, full), `git merge-base --is-ancestor`, `git log`, `git rev-parse`, `git status --short` (read-only per contract, though it may refresh the index's stat cache), `diff -rq`, `stat`, `sha256sum`, and one `cp` of the lane classifier into scratch.
- Installs or upgrades: none. I used the existing `prlimit` (util-linux 2.42.4) and `python3` (3.14.8).

## Verdict

PASS at the landed tip `2f1134f3`: eleven legacy suites, 247/247, rc 0 each. The runs are deterministic, match the round-22 receipts case for case, and are sensitive to a broken scan exit.

Operability flag: the lane working copy carries uncommitted, still-changing edits to `tools/mado-tripwire.py` (F1). Lane-path selftest results must not be cited as tip evidence until L1 resolves that.
