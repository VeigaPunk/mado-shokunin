# Frozen counter v4 mutation probe

## Verdict

MUTCOUNTER v4: 1/5 mutants change a verdict; surviving: expected-live, skip-oracle-check, embed-threshold-1000, missing-only.

The original rejected both tools in every pristine and restored run. Mutant 5 accepted both despite `cases_pass=0/41`: the original fails closed where this mutant does not. The other four mutants survive this particular two-tool detector; that is a coverage limitation, not evidence that their weakened behavior satisfies PRED-C1 (v4).

## Scope and detector

Read registration.md, including its current Attempt 3 section, before probing. Axes: negative-control rejection, frozen-byte/isolation fidelity, and repeatable exact restoration. No implementation of `tools/mado-binds.py`, resolver, control parser, or corpus change was made.

Five independent scratch copies, one one-line behavior mutation per copy. Each copy ran the same complete counter CLI against both tools in three states: pristine, mutated, restored. These are real v4 runs using its nested-Hyprland oracle and bubblewrap tool sandbox, not mocked oracle results or a substitute comparator. Total: 30 counter runs, all on attempt 1; no setup errors, timeouts, or inconclusive probes. The negative-control detector expects `TARGET_MISSED`, exit 1, for each tool. A changed verdict kills a mutant only when the pristine and restored runs both reject that same tool.

Scratch root (`R` below): `/fast/scratch/hyaku/mado-r25a3/mut`.

Tools (both accept the required `--home` argument through argparse and otherwise do no work):

- `R/empty.py` prints `[]` followed by a newline, exit 0. SHA256 `bede4ed11930aba5bc69fa004233a691bc66614c87c0df75606f4769d677c578`.
- `R/junk.py` prints `junk` followed by a newline, exit 0. SHA256 `e18fa51cf016c63525a6d8cc625f10ec7bb706592c415ff4820f1b05186b34c7`. This is intentionally non-JSON junk, not a JSON superset or field-corrupted table.

Fixed seed `0123456789abcdef` deliberately holds generated cases constant across states. Revision resolved to `1ed41fa8301a4562d125503e5b881ec8eb5a1908`. All 30 receipts captured the same live table (192 binds), SHA256 `9a47199e2297617f1025d524fc1909a091a950d69261735f39aad1ec3100c779`, and the same 79-file snapshot digest `fe1b2d8ba8e61ec3756fac0820c88ddda861db7f833f1c47e371934efa983727`. Every run printed `ORACLE_CHECK base_vs_live missing=0 extra=0`.

## Copy layout and pin preservation

Preparation used Python `shutil.copy2` to copy the lane's `c1/count.py` and `c1/count-v3.py` into each `R/N/`, for N=1 through 5. It created these symlinks:

```text
R/N/lane/.git -> /home/vgpnk/Projects/shokunin/mado-shokunin/.git
R/N/lane/.ufo/waves/round-25/c1/count.py -> R/N/count.py
R/N/lane/.ufo/waves/round-25/c1/count-v3.py -> R/N/count-v3.py
```

Invoking the logical `.ufo/waves/round-25/c1/count.py` path preserves v3's five-directory LANE calculation as `R/N/lane`; its `.git` symlink permits read-only REV resolution. Neither LANE nor the generator was patched. Lane git/jj write commands were never run.

Frozen counter hash (`F4`): `323a384925d1cc259a6b80418630ef956bf0c651cacf615e4cd615bda4d342e2` (14,537 bytes).

Pinned generator hash (`F3`): `8532d3e96cc201ce2506a07d5f4b943e25b645e5ca1b461d9a35d08d4ff78375` (38,921 bytes).

Every receipt's generator hash was F3. Both source hashes were checked before copying and after restoration; they stayed F4 and F3.

## Mutants and observed verdicts

Line numbers refer to the frozen `c1/count.py`; scratch copies have the same line numbers.

| N / mutant | Sole mutation | Expected sensitivity of these two tools | Pristine: empty / junk | Mutated: empty / junk | Restored: empty / junk | Verdict differs? / original fails closed where mutant does not? |
|---|---|---|---|---|---|---|
| 1 / expected-live | :275 `exp = truth[label][0]` → `exp = live` | Neither tool supplies a table matching either expectation; likely survives. | MISSED exit 1 / MISSED exit 1 | MISSED exit 1 / MISSED exit 1 | MISSED exit 1 / MISSED exit 1 | No / no, survived |
| 2 / skip-oracle-check | :266 `if nm or ne:` → `if False:` | Needs actual BASE oracle drift to exercise the removed rejection; likely survives healthy-oracle runs. | MISSED exit 1 / MISSED exit 1 | MISSED exit 1 / MISSED exit 1 | MISSED exit 1 / MISSED exit 1 | No / no, survived |
| 3 / embed-threshold-1000 | :236 `len(e[f]) >= 12` → `len(e[f]) >= 1000` | Neither tool embeds a live arg/description, so this eligibility-length increase is not exercised. | MISSED exit 1 / MISSED exit 1 | MISSED exit 1 / MISSED exit 1 | MISSED exit 1 / MISSED exit 1 | No / no, survived |
| 4 / missing-only | :286 `ok = nm == 0 and ne == 0` → `ok = nm == 0` | Empty output still misses expected binds; invalid JSON never reaches comparison. | MISSED exit 1 / MISSED exit 1 | MISSED exit 1 / MISSED exit 1 | MISSED exit 1 / MISSED exit 1 | No / no, survived |
| 5 / final-threshold-reversed | :295 `met = npass == len(built) and embed_hits == 0` → `met = npass <= len(built) and embed_hits == 0` | The relational-operator defect accepts zero passing cases; both tools should detect it. | MISSED exit 1 / MISSED exit 1 | MET exit 0 / MET exit 0 | MISSED exit 1 / MISSED exit 1 | Yes, both tools / yes, killed |

All 30 runs reported `cases_pass=0/41 embed_hits=0`; only mutant 5 changed the final verdict/exit. Mutant 1 also changed `V3_MODEL_AGREE` from 41/41 to 5/41 and scored HARD cases against 192 live binds instead of each generated oracle table. This diagnostic difference is not counted as a changed verdict, because v4 explicitly makes model agreement non-predicate.

No drift or oracle-failure fault was injected. No embedded-table tool, extra-bind superset, keys-only comparator, sandbox-flag mutation, or ORACLE_FAIL-to-empty mutation was tested. The four survivors therefore describe the reach of the assigned empty/junk detector, not a general counter certification or authorization to change the contract.

## Exact commands and receipt locations

Working directory: `R`. `R/detect.py` is the retained Python-stdlib detector driver. It launches at most two counter commands concurrently, each with `--jobs 2`; the frozen six-slot host-wide lock still applies. It removes `GIT_DIR`, `GIT_WORK_TREE`, and `GIT_INDEX_FILE` from each child's environment. It retains combined stdout/stderr plus a literal `exit=N` trailer for each run.

The three phase commands executed were:

```sh
timeout --kill-after=20 3400 prlimit --as=4000000000 --core=0 python3 -I -B /fast/scratch/hyaku/mado-r25a3/mut/detect.py pristine
timeout --kill-after=20 3400 prlimit --as=4000000000 --core=0 python3 -I -B /fast/scratch/hyaku/mado-r25a3/mut/detect.py mutated
timeout --kill-after=20 3400 prlimit --as=4000000000 --core=0 python3 -I -B /fast/scratch/hyaku/mado-r25a3/mut/detect.py restored
```

For each phase, the driver ran the following exact command with each N in 1,2,3,4,5 and TOOL in empty,junk (ten concrete commands per phase; exact expanded argv is also recorded in the phase JSON):

```sh
timeout --kill-after=20 1200 prlimit --as=4000000000 --core=0 python3 -I -B /fast/scratch/hyaku/mado-r25a3/mut/N/lane/.ufo/waves/round-25/c1/count.py 1ed41fa8 --tool-file /fast/scratch/hyaku/mado-r25a3/mut/TOOL.py --seed 0123456789abcdef --jobs 2
```

One attempted asynchronous launch of the restored phase was refused by the tool with `Background job limit reached (100). Wait for running jobs to finish or cancel one.` It did not start a counter. The same command then completed synchronously. There were no additional behavioral attempts.

Complete stdout/stderr receipts (paths below relative to R):

| N | Pristine empty / junk | Mutated empty / junk | Restored empty / junk |
|---|---|---|---|
| 1 | `1/pristine-empty-1.txt`, `1/pristine-junk-1.txt` | `1/mutated-empty-1.txt`, `1/mutated-junk-1.txt` | `1/restored-empty-1.txt`, `1/restored-junk-1.txt` |
| 2 | `2/pristine-empty-1.txt`, `2/pristine-junk-1.txt` | `2/mutated-empty-1.txt`, `2/mutated-junk-1.txt` | `2/restored-empty-1.txt`, `2/restored-junk-1.txt` |
| 3 | `3/pristine-empty-1.txt`, `3/pristine-junk-1.txt` | `3/mutated-empty-1.txt`, `3/mutated-junk-1.txt` | `3/restored-empty-1.txt`, `3/restored-junk-1.txt` |
| 4 | `4/pristine-empty-1.txt`, `4/pristine-junk-1.txt` | `4/mutated-empty-1.txt`, `4/mutated-junk-1.txt` | `4/restored-empty-1.txt`, `4/restored-junk-1.txt` |
| 5 | `5/pristine-empty-1.txt`, `5/pristine-junk-1.txt` | `5/mutated-empty-1.txt`, `5/mutated-junk-1.txt` | `5/restored-empty-1.txt`, `5/restored-junk-1.txt` |

Machine-readable command, tool/counter/generator hashes, elapsed time, guard output, predicate, exit and receipt paths: `R/pristine-results.json`, `R/mutated-results.json`, `R/restored-results.json`. Complete receipt files total 301,338 bytes.

## Actual changed-verdict output

`R/5/pristine-empty-1.txt:7`:

```text
CASE BASE         FAIL missing=192 extra=0 oracle_binds=192 (unperturbed) v3_model=agree
```

Its final predicate and exit, also observed for every pristine/restored empty or junk run:

```text
PRED-C1 (v4) cases_pass=0/41 embed_hits=0 verdict=TARGET_MISSED

exit=1
```

`R/5/mutated-empty-1.txt:7` and `:130-133`:

```text
CASE BASE         FAIL missing=192 extra=0 oracle_binds=192 (unperturbed) v3_model=agree
```

```text
V3_MODEL_AGREE 41/41 (diagnostic, not the predicate)
PRED-C1 (v4) cases_pass=0/41 embed_hits=0 verdict=TARGET_MET

exit=0
```

`R/5/mutated-junk-1.txt:7` and `:48-51`:

```text
CASE BASE         FAIL stdout is not a JSON array of objects (unperturbed) v3_model=agree
```

```text
V3_MODEL_AGREE 41/41 (diagnostic, not the predicate)
PRED-C1 (v4) cases_pass=0/41 embed_hits=0 verdict=TARGET_MET

exit=0
```

## Hashes and exact restoration

Before every mutation and after every restoration the counter SHA256 was F4. Mutated-state counter hashes, independently recorded in both tool receipts/phase metadata:

| N | Before SHA256 | Mutated SHA256 | Restored SHA256 |
|---|---|---|---|
| 1 | F4 | `0252183e62efae3e25416b241652673e749d46ad40e512b09efad4b3b5b579c8` | F4 |
| 2 | F4 | `0cd3e5ed93560adece2757add398ca84788c10d3bb56e81038648c039b48d926` | F4 |
| 3 | F4 | `578ca2b3907142888baa98c1582c35e21557ffdad3eead631a9ce292c692b01a` | F4 |
| 4 | F4 | `b08c0aa8def9dfd60e9c3da2076fe230d41f4b47dca84e6dd1cb5524fd56ed63` | F4 |
| 5 | F4 | `490ec4e23f4b3e9bafeea39e9324a77ba6b0832bec24eab851db8d0a38f573e1` | F4 |

All five reverse edits completed before the restored phase. A final Python byte comparison returned `counter_bytes_equal=true` and `generator_bytes_equal=true` for N=1 through 5 against the untouched lane sources; their final SHA256 values were F4/F3. The restored behavioral phase then rejected both tools in all five copies, matching pristine behavior.

All 30 commands completed normally through the frozen oracle's process-group kill/wait cleanup. The detector additionally sends SIGKILL to its own timeout-command process group after collecting each run. A final `/proc/*/cmdline` scan found no processes containing this private scratch-root path. No live-compositor write verbs, package/service/config changes, or sibling-source edits were performed. No tools were installed or updated. Scratch copies and receipts are retained as evidence, with every copied counter and generator restored byte-for-byte.
