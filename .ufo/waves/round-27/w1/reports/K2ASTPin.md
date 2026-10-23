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
