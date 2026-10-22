# BasePrecision: C1 no-harm baseline, precision at base a28e4815

Seat: MadoR23.BasePrecision (leaf; no subagents). Judged on: operability.
Assigned base: `a28e4815aabfa85f55274884000fb2608355f8cf`. Lane master has since moved to `4de4464` (section 6); the result is the same at both.

## Verdict

PASS for the re-measurement. At base `a28e4815` the precision harness scores **166/175** with the registered nine failures (H5, L3, W1). The run repeats byte for byte. The pass set equals the round-22 receipt's for the same classifier bytes. The harness is operable: it takes no tool path, reads the classifier and the suite only from committed revisions, and fails closed on every bad input I probed. Three operability caveats are in section 7. None changes the number.

Verdict line: PASS: base a28e4815 re-measured at 166/175 (failures H5 L3 W1), byte-identical on repeat, same pass set as the round-22 receipt; tip 4de4464 identical; caveats 1-3 recorded.

## 1. Inputs, pinned by hash

| item | value |
|---|---|
| base commit | `a28e4815aabfa85f55274884000fb2608355f8cf` (rev-parse ok) |
| classifier at base, `git show REV:tools/mado-tripwire.py` | sha256 `cd9da20c2f562efbd30967e00c0c630026de6e6d06ef74399eb1a46ccf00ea84`; identical to blob at `e33ea304` and to the lane working-tree file |
| harness `.ufo/waves/round-20/tw-precision.py` | sha256 `bd3bdc23747a6d8f195e69528f532988202db4ab3476d141a8ff46871e42a8e7`; equals base blob; working tree clean for `tools/` and `.ufo/waves/round-20/` |
| suite pin | `f3da50488661509ce5d144c90f7780f8088e0903`; `expected.json` sha256 `1039c4fa6ede43b1f08cca231e6c713aa032722e4955f89dbd8b8f3de092254f`; 175 cases (P 66, S 17, W 22, H 52, L 18); all 175 fixture digests match at the pin; working-tree suite equals the pin |
| scratch copy of base classifier | `/fast/scratch/hyaku/mado-r23/BasePrecision/base-tool.py`, sha256 `cd9da20c...` (same as above) |

## 2. Harness flags checked first

- Usage, from source: `tw-precision.py REV [--suite-rev PIN] [--heldout]`. There is no tool-path argument. The harness reads the classifier from `git show REV:tools/mado-tripwire.py`, copies it to a temp directory, and runs `python3 -I <copy> --scan <case>` per case. The lane-relative tool path in the brief therefore did not apply, and none was passed.
- No `--help`. With no arguments it prints the usage line and exits 2. `--help` is taken as a REV and fails with `tool revision is not a commit: --help`.
- Classifier CLI (base-tool.py lines 129-141 and 3381-3390): `--scan PATH... [--permit CLASS...]`, `--frozen DIR`, `--selftest DIR`. Exit 0 = no unpermitted finding, 1 = at least one, 2 = could not evaluate. The harness accepts per-case exits 0 and 1 only.

## 3. Exact commands and exits

Caps on every harness or classifier process: `prlimit --as=402653184 --cpu=15` (384 MiB address space; 15 CPU-seconds per process), inside an outer `timeout --signal=KILL 600`. The caps are the registered caps used by round 21 (its precision receipts carry `outer_address_space_cap: 402653184`). Full command list: `out/BasePrecision/commands.txt`.

Measurement command (cwd = lane):

```
prlimit --as=402653184 --cpu=15 -- timeout --signal=KILL 600 python3 -I /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-20/tw-precision.py a28e4815aabfa85f55274884000fb2608355f8cf
```

| run | rc | wall | stdout | stderr | result |
|---|---|---|---|---|---|
| run 1 | 0 | 6.783 s | 39,340 B, sha256 `33d6e66e162a3662851babd209bf34a165ebe19d9ca744f094546d69167345f0` | 0 B | 166/175 |
| run 2 (same command) | 0 | 6.812 s | byte-identical to run 1 | 0 B | 166/175 |

Fail-closed probes (same wrapper; none reached a classifier child):

| probe | rc | wall | stdout | stderr |
|---|---|---|---|---|
| no arguments | 2 | 0.022 s | 0 B | `could_not_evaluate: usage: tw-precision.py REV [--suite-rev PIN] [--heldout]` |
| `--help` | 2 | 0.021 s | 0 B | `could_not_evaluate: tool revision is not a commit: --help` |
| REV `0000000000000000000000000000000000000001` | 2 | 0.023 s | 0 B | `tool revision is not a commit` |
| `--suite-rev 0000000000000000000000000000000000000001` | 2 | 0.024 s | 0 B | `suite revision is not a commit` |
| unknown flag `--bogus` | 2 | 0.019 s | 0 B | usage line |

Cap check: a child started through the same wrapper reports `RLIMIT_AS = (402653184, 402653184)` and `RLIMIT_CPU = (15, 15)`.

Installs and upgrades: none. Tool versions used: Python 3.14.8 (`/usr/bin/python3`); git 2.56.0; prlimit from util-linux 2.42.4-1; timeout from coreutils 9.12-2 (`/usr/bin/timeout`). `pacman` was used only read-only (`pacman -Qo`).

## 4. Result at base

166/175. By family: P 66/66, S 17/17, W 21/22, H 47/52, L 15/18. The harness's score field reads 9.4857 (ten times the fraction; see section 7.4).

Nine failing cases, names exactly as in the suite:

| family | case | got | want | what the fixture does |
|---|---|---|---|---|
| H | H-CaseDryRunBash-commit-dry-run | vcs_write observed, git:commit | exit 0, no finding | `git commit --dry-run -m x` |
| H | H-CaseHelpDryRunEval-pct-bash-dry-runs | vcs_write observed, git:commit | exit 0, no finding | `git commit --dry-run -m probe` in a %%bash cell |
| H | H-AdoptW2-AdvVcs-p33-git-dryrun | vcs_write observed, git:commit | exit 0, no finding | `git commit --dry-run -m x` |
| H | H-AdoptW2-RerunPrecision-corpus-jj-var-verb-help | vcs_write observed, jj:$c | exit 0, no finding | `/tmp/bin/jj $c --help` |
| H | H-AdoptW2-RerunPrecision-corpus-git-commit-a-dry-run-short | vcs_write observed, git:commit | exit 0, no finding | `git commit -a --dry-run --short` |
| L | L-CasePureCrossCell-reset-clears-helper | exit 0, none | exit 1, lead pacman:-Q line 3 | has `reset:true` |
| L | L-CaseLeadsInvisible-reset-cleared-helper | exit 0, none | exit 1, lead pacman:-Q line 2 | has `reset:true` |
| L | L-AdoptW2-AdvHelperFn-b14 | exit 0, none | exit 1, lead pacman:-Q line 1 | no reset; a literal argv handed to a callable parameter `run_case` |
| W | W-CaseWrapperForms-class-method-instance | observed pacman:-Q line 1 | exit 0, no finding | class method `Runner.run` spawns |

Against the registration's breakdown (five VCS index-write readings, three helper leads, one class-method case), the counts match. The registration's label "reset-cleared" fits two of the three L cases. `L-AdoptW2-AdvHelperFn-b14` has no reset in its fixture, so the label does not fit it. This comes from reading the fixture text; I did not trace the round-21 change that removed the lead.

## 5. Repeat, cross-checks, tamper probes

- Repeat: run 2 is byte-identical to run 1.
- Prior receipt: `.ufo/waves/round-22/evidence/resume/precision-final.json` (rev `579109a6812f4d0a2dd47572caca241075c6021d`, classifier sha256 `cd9da20c...`). Same 175 case names, the same pass flag for all 175, and the same got/want payloads for all 175. The passing set matches the registration's "identical passing-case set" for this classifier.
- Committed suite tamper (scratch clone `/fast/scratch/hyaku/mado-r23/BasePrecision/clone` only, never pushed): one newline appended to `.ufo/waves/round-20/precision/CasePureBuiltins--frozenset-closure.jsonl`, committed as `de7b464094dcda16db7af3e24d0054687e816de4`, then the same command with `--suite-rev de7b464094dcda16db7af3e24d0054687e816de4`. Result: rc 2 in 0.032 s, `could_not_evaluate: digest mismatch for ...: expected 14558b6d..., got 7801ea72...`, no stdout. The digest check runs before any classifier child.
- Working-tree-only classifier edit (clone checked out at base; one uncommitted comment line appended to `tools/mado-tripwire.py`; clone file restored afterwards): rc 0, output byte-identical to run 1, `tool_sha256` in the output `cd9da20c...`, 166/175. The harness reads the classifier from the revision only.
- Named defect classes, checked: wrong path, none found (no tool-path argument exists; the lane root comes from the harness's own file location and every git read succeeded); tamper failure, none found (no false digest failure on the clean suite, and the committed tamper was caught); nondeterminism, none found (run 1 equals run 2 byte for byte).

## 6. Lane master moved to 4de4464

`master` is now `4de44647f93bfd25ed5c979f61ff016b50456549` ("round-23: tighten C2/C3 counters and record registration clarifications"), one commit past base. Its diff from `a28e4815` touches only `.ufo/waves/round-23/` (`c2/count.py`, `c3/count.py`, two evidence JSON files, `registration.md`). `tools/` and `.ufo/waves/round-20/` are unchanged between the two, so the score's inputs are byte-identical. A capped run at the tip (`out/BasePrecision/precision-tip-4de4464.*`, rc 0, 6.46 s) gives 166/175, tool `cd9da20c...`, and per-case payloads identical to the base run for all 175 cases. On the parsed JSON, the two outputs differ only in the `rev` and `commit` fields.

## 7. Operability findings (ranked)

1. **Cap coupling (residual; no effect seen).** When `RLIMIT_AS` is at or below 512 MiB, `run_with_stack` (base-tool.py lines 3436-3440) lowers the classifier's worker-thread stack from 512 MiB to 64 MiB. So a capped run and an uncapped run have different recursion headroom. [INFERENCE] For this suite the effect is nil: the largest fixture is 1,577 bytes and the deepest bracket nesting is 9 (counted over raw text), far from any stack limit. I did not run the suite uncapped, because the brief's caps rule forbids classifier runs outside the caps, so capped-equals-uncapped is unverified.
2. **No wall deadline of its own.** `scan_case` hard-codes `timeout=120` per child, while the registered cap is a 15-second wall deadline (as in the sibling harnesses). Here the 15 s was enforced as per-process CPU through `prlimit --cpu=15`. The whole run took 6.8 s, so every child was under 15 s wall. A caller who needs the registered wall cap must wrap the harness.
3. **Receipts omit the harness hash.** The output carries `tool_sha256` and `suite_pin`, but not the sha256 of the harness file. The harness changed once since the suite landed: `SUITE_PIN = None` became `f3da5048...` in commit `28c6837` (`git diff f3da5048 a28e4815 -- .ufo/waves/round-20/tw-precision.py` is one line). Receipts should record the harness hash too.
4. **Cosmetic.** `--help` is not supported and produces a misleading message. `score` is ten times the pass fraction (9.4857), not a fraction.
5. **Process hazard for C1.** The classifier comes from REV only, so a candidate must be committed before it can be measured; an uncommitted edit is invisible (section 5). To re-measure a candidate: commit it, then run `prlimit --as=402653184 --cpu=15 -- timeout --signal=KILL 600 python3 -I .ufo/waves/round-20/tw-precision.py <committed-rev>` and check that the output's `tool_sha256` equals the candidate blob's sha256.

## 8. Lane state

- Before my work, `git --no-optional-locks status --porcelain` listed five untracked entries: `.ufo/waves/round-23/w1-assignments.json`, `w1-record.json`, `w1-run.json`, `w1-spec.json`, and `w1/`. No tracked change in `tools/` or `.ufo/waves/round-20/`. After my work, the same five entries, with nothing new added to tracked files.
- My writes inside the lane: `.ufo/waves/round-23/w1/out/BasePrecision/` and this report. Everything else is under `/fast/scratch/hyaku/mado-r23/BasePrecision/`, including the scratch clone (branch `tamper-probe-r23`, commit `de7b4640...`, not pushed).
- No jj command was run. No git write was run in the lane. Every lane git call was read-only (`--no-optional-locks` on each call except `git clone`, which only reads the lane; the scratch clone was made with `--no-hardlinks`).

## 9. Receipts

Directory `.ufo/waves/round-23/w1/out/BasePrecision/`:
- `commands.txt` (every command, in order), `summary.json` (all values above), `failing-names.tsv`, `base-tool.sha256`, `harness.sha256`
- `precision-base-run1.{stdout,stderr,meta.json}`, `precision-base-run2.{stdout,stderr,meta.json}`
- `precision-tip-4de4464.{stdout,stderr,meta.json}`
- `probe-no-args`, `probe-help-flag`, `probe-bogus-tool-rev`, `probe-bogus-suite-rev`, `probe-unknown-flag` (each `.stdout`, `.stderr`, `.meta.json`)
- `probe-tamper-suite-fixture.{stdout,stderr,meta.json}`, `probe-worktree-tool-edit.{stdout,stderr,meta.json}`

## 10. Residual risk and verification gaps

- Uncapped behavior not measured (section 7.1).
- Base commit `e33ea304` (the registration's base) not run. Its classifier bytes equal a28e4815's by sha256 only.
- Harness copied outside the lane (lane root derived from file location) not exercised.
- The category labels in section 4 rest on fixture text, not on tracing the classifier.
- Measured classifier bytes: only `cd9da20c...`, at `a28e4815` and at the tip `4de4464`. No other classifier bytes were run.
