# K2ASTPin — AST-PIN C2 control

## Verdict
CONTROL K2ASTPin best: PRED-C2-r27 green=5/8 w_killed=15/15 h_killed=0/0 h_need=0 h_valid=0 h_invalid=0 verdict=TARGET_MISSED — not met

Both fresh-seed runs produced that exact PRED line and `exit=1`. No exit-2 run occurred. The control kills all 15 W mutants, but rejects all three behavior-preserving unused assignments. It therefore misses the green requirement independently of the unmeasured held-out requirement. This is not evidence of behavioral checking.

## Scope and implementation

Axes: strict AST equality, no behavioral execution, isolated repeatability, bounded host impact.

Wrote only the two assigned standard-library suites, the two stdout receipts, and this report. Suite A accepts `--c1 PATH --c2 PATH --rev REV` and compares both subjects' `ast.dump(ast.parse(subject_bytes))` with complete literal dumps pinned from `5ddc5885188a1de8606464526d636c9e2fc433e6`. Suite B accepts `--checker PATH` and compares its subject likewise. Exact match returns 0; mismatch or an unreadable/unparseable subject returns 1. Neither suite imports or executes a subject, calls its CLI, filters AST nodes, ignores unused assignments, or consults W/H mutant text. Ordinary comments are ignored naturally by `ast.parse`.

Pristine pins were obtained using read-only `git show 5ddc5885:<subject>` commands, each under a cleared environment, `timeout 30`, `prlimit --as=4000000000 --core=0`, with cwd set to the lane.

| Pristine subject | SHA-256 | Bytes |
|---|---|---:|
| `.ufo/waves/round-26/c1/count-v2.py` | `4ed70b5427f2e223a8d816679e6d1fad7d2e76d2ed57aa0fe7f135496e836428` | 18537 |
| `.ufo/waves/round-26/c2/count.py` | `b92c32da632bc9cfaeae72b6a0be2202e5a25653274cc0b33fc0ae3f37a716a8` | 10924 |
| `.ufo/waves/round-26/quality/check-population.py` | `803e0096c994d301fa7fe9a9dd7e35255ee1f5bcf3f63d15956cdba8943d0f64` | 7499 |

## Commands and receipts

The following independent runs were launched concurrently, with separate fresh random seeds. The commands' environments contained no `WAYLAND_DISPLAY`, `HYPRLAND_INSTANCE_SIGNATURE`, or Git override variables.

```sh
cd /home/vgpnk/Projects/shokunin/mado-shokunin && env -i PATH=/usr/bin HOME=/home/vgpnk timeout 1800 python3 -I .ufo/waves/round-27/c2/count.py 5ddc5885 --suite-a-file /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-27/controls/K2ASTPin-suite-a.py --suite-b-file /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-27/controls/K2ASTPin-suite-b.py --seed bad4519b3978bbd3 --jobs 6
```

```sh
cd /home/vgpnk/Projects/shokunin/mado-shokunin && env -i PATH=/usr/bin HOME=/home/vgpnk timeout 1800 python3 -I .ufo/waves/round-27/c2/count.py 5ddc5885 --suite-a-file /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-27/controls/K2ASTPin-suite-a.py --suite-b-file /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-27/controls/K2ASTPin-suite-b.py --seed 7a0d6f6b10eb19d0 --jobs 6
```

| Run | Seed | Exit | Verbatim stdout receipt | Receipt SHA-256 |
|---|---|---:|---|---|
| 1 | `bad4519b3978bbd3` | 1 | `.ufo/waves/round-27/controls/K2ASTPin-seed1.txt` | `5ff290d7c60c83f9cf9dfbb0ddcf2ebe4b84df2d2392e57ad1c2b6e5ec1583c5` |
| 2 | `7a0d6f6b10eb19d0` | 1 | `.ufo/waves/round-27/controls/K2ASTPin-seed2.txt` | `70cd1b9356ce56f654f1243a8081f3a3fc1b8365432c609f1a504c8f9c776ab1` |

Both receipts contain all 23 case lines and the final `exit=1`; both stderr streams were empty. The frozen counter hash observed before scoring and in both receipts was `2e180ed29c31abcb3421d7e57a147d05ac9d2982ebe4dbc555747b287e754dc7`. Both receipts report W hash `0ad0e46c1a6e61f369c30ab08d6a998f6dce7d16436087b5df57fb8f22323608`.

## Actual detector output

The expected AST detector accepts pristine subjects and appended comments, rejects any AST-changing edit, and performs no behavioral check. Both runs agreed:

| Cases | Actual result |
|---|---|
| Suite A pristine; suite B pristine | Both `rc=0 PASS` |
| Appended comment on each of the three subjects | All three `rc=0 PASS` |
| Inserted unused assignment on each subject | All three `rc=1 FAIL`, respective `AST_PIN ... MISMATCH` |
| Nine counter W mutants | All nine `rc=1 KILLED` |
| Six population-checker W mutants | All six `rc=1 KILLED` |
| Held-out mutants | Not supplied, read, or scored; `h_valid=0` |

```text
PRED-C2-r27 green=5/8 w_killed=15/15 h_killed=0/0 h_need=0 h_valid=0 h_invalid=0 verdict=TARGET_MISSED
exit=1
```

For the frozen W detector, the pristine baselines passed, so its 15/15 killed tally is not caused by a failing baseline. It remains purely syntactic sensitivity: the benign-assignment failures prevent this control from meeting C2.

## Byte preservation and restoration evidence

| Control | SHA-256 before scoring | SHA-256 after both scores |
|---|---|---|
| `controls/K2ASTPin-suite-a.py` | `b1e7bd4ff760c6726da21c4c31fe4e791f9fb67ede17578baaed05f767c38571` | `b1e7bd4ff760c6726da21c4c31fe4e791f9fb67ede17578baaed05f767c38571` |
| `controls/K2ASTPin-suite-b.py` | `cd000383087e21fbc18fe000f9e6ad5b1b2552002e8bdbc9d1e8064bbbe0f17e` | `cd000383087e21fbc18fe000f9e6ad5b1b2552002e8bdbc9d1e8064bbbe0f17e` |

Paths in this table are under `.ufo/waves/round-27/`. Post-run hashes came from a bounded `sha256sum` call. The suites were unchanged between the two scores. No lane subject, counter, harness, W-set file, or sibling source was modified. The assigned mutation exercise was the frozen counter's W scoring in fresh disposable clones under `/fast/scratch/hyaku/mado-r27/c2`; its inspected `run_suite` and top-level `finally` blocks delete those clones. No separate manual mutation or restored-byte detector was run, and no manual restoration was necessary. Both counter processes completed with exit 1; the controls themselves spawn no child processes.

## Host safety and tooling

Before writing, bounded `df -h /fast` reported:

```text
Filesystem      Size  Used Avail Use% Mounted on
/dev/nvme1n1p2  804G  689G  115G  86% /fast
```

Before and after scoring, ran `coredumpctl list --no-pager --no-legend` under `timeout 30`, a cleared environment and `prlimit --as=4000000000 --core=0`, counting output lines containing `/usr/bin/Hyprland` in Python. Both calls exited 0: before=1338, after=1338, delta=+0. These suites do not launch Hyprland, contact the live compositor, access DRM nodes, or start a service. Counter runs used the prescribed 1800-second bound; their suite subprocesses carry the frozen counter's 300-second, 4-GB, core-disabled limits.

No tools were installed or updated. No build, linter, formatter, additional behavior suite, or held-out check was run.

## C2 v2 re-score — unchanged control
CONTROL K2ASTPin v2 best: PRED-C2-r27-v2 green=5/8 b_valid=0 w_killed=15/15 h_killed=0/0 h_need=0 h_valid=0 h_min_per_subject=0 invalid=0 verdict=TARGET_MISSED — not met

L1 retired counter v1 before data and requested this re-score under counter v2. The preceding v1 results remain historical receipts. Neither control suite was changed.

Ran these commands concurrently with two fresh seeds and no held-out directory:

```sh
cd /home/vgpnk/Projects/shokunin/mado-shokunin && env -i PATH=/usr/bin HOME=/home/vgpnk timeout 1800 python3 -I .ufo/waves/round-27/c2/count-v2.py a4dc0da0 --suite-a-file /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-27/controls/K2ASTPin-suite-a.py --suite-b-file /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-27/controls/K2ASTPin-suite-b.py --seed 7711d387341b6a9d --jobs 6
```

```sh
cd /home/vgpnk/Projects/shokunin/mado-shokunin && env -i PATH=/usr/bin HOME=/home/vgpnk timeout 1800 python3 -I .ufo/waves/round-27/c2/count-v2.py a4dc0da0 --suite-a-file /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-27/controls/K2ASTPin-suite-a.py --suite-b-file /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-27/controls/K2ASTPin-suite-b.py --seed 6694ed23a6b74e8c --jobs 6
```

Both runs resolved REV to `a4dc0da0394a71badf506e9c72144cd1b8ca7281` and reported counter SHA-256 `4dfb34b5551a908aa7fd56e75526417b43659018c47fa5993ad39a72b6b109d3`, also observed in the pre-run bounded `sha256sum` call. The three subject hashes and W hash matched the earlier pins.

| Run | Seed | Exit | Verbatim stdout receipt | Receipt SHA-256 |
|---|---|---:|---|---|
| 1 | `7711d387341b6a9d` | 1 | `.ufo/waves/round-27/controls/v2/K2ASTPin-seed1.txt` | `88136f8c4254754ee18955a5ca3775ef73e0bd57a32c5b1651d55153d1b0317b` |
| 2 | `6694ed23a6b74e8c` | 1 | `.ufo/waves/round-27/controls/v2/K2ASTPin-seed2.txt` | `ee957c36f7b68d1da394ed17168ca802f73a1ecf92a4a47f977e73da653527f5` |

Each receipt is 3,562 bytes and contains all 23 case lines and `exit=1`. Both stderr streams were empty; no exit-2 rerun was necessary. Both pristine runs and all three comment edits passed. The three unused-assignment edits failed with `rc=1` and the respective `AST_PIN ... MISMATCH`; all 15 W mutants were killed with `rc=1`. Thus the passing pristine baselines support the W tally, but the syntactic detector still fails the green requirement. Sealed benign edits and held-out mutants were not supplied, read, or scored; `b_valid=0` and `h_valid=0` are not passes.

Both runs ended with:

```text
PRED-C2-r27-v2 green=5/8 b_valid=0 w_killed=15/15 h_killed=0/0 h_need=0 h_valid=0 h_min_per_subject=0 invalid=0 verdict=TARGET_MISSED
exit=1
```

### V2 preservation and host safety

Bounded `sha256sum` calls before and after both runs reported identical control hashes:

| Control | Before and after SHA-256 |
|---|---|
| `K2ASTPin-suite-a.py` | `b1e7bd4ff760c6726da21c4c31fe4e791f9fb67ede17578baaed05f767c38571` |
| `K2ASTPin-suite-b.py` | `cd000383087e21fbc18fe000f9e6ad5b1b2552002e8bdbc9d1e8064bbbe0f17e` |

Counter v2 uses disposable no-local clones under `/fast/scratch/hyaku/mado-r27/c2v2`, per-run directories, bubblewrap, and clone cleanup in its inspected `finally` blocks. No lane subject was modified, so no manual restoration was needed. The only new writes were the two assigned v2 receipts and this report append. Both counter processes completed; the unchanged AST suites spawn no child processes.

Pre-run bounded `df -h /fast` reported 804G total, 695G used, 109G available, 87% usage. The same bounded, cleared-environment coredump counting procedure used above exited 0 before and after: Hyprland count 1338 to 1338, delta=+0. No Hyprland instance was started by the controls. No tools were installed or updated; no other checks were run.

PRED-C2-r27-v2 green=8/8 b_valid=0 w_killed=15/15 h_killed=0/0 h_need=0 h_valid=0 h_min_per_subject=0 invalid=0 verdict=TARGET_MISSED
PRED-C2-r27-v2 green=8/17 b_valid=9 w_killed=15/15 h_killed=18/18 h_need=14 h_valid=18 h_min_per_subject=6 invalid=0 verdict=TARGET_MISSED
