# CaseDryRunBash — 12 H cases on the bash surface, 7 red at 1f7f995; every expectation measured in /tmp; one E4 item corrected by evidence (L1 accepted)

## Deliverable

Dir `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-20/w1/cases/CaseDryRunBash/`: 12 one-line `.jsonl` fixtures plus `cases.json` (schema `mado-tw-precision-cases-v1`, seat `CaseDryRunBash`, sha256 `fad412af03fb5d2267f9f1984780079115288ee15b0336f41890cc1b18b76dcd`). Each fixture is one assistant message in the envelope of `round-19/tripwire/r19-helperfn/py-lead-cross-cell-literal.jsonl`, except the toolCall is `bash {command}`. All findings are on line 1. The fixture text holds no paths, secrets or hosts.

## Cases and `before` (counter rule: exit equal AND multiset of (class, rule, line, evidence) equal; a row with no evidence key counts as `observed`)

| # | name | command | want | 1f7f995 | 9c54c56 | fixture sha256 |
|---|---|---|---|---|---|---|
| 1 | H-CaseDryRunBash-commit-dry-run | `git commit --dry-run -m x` | 0, [] | **fail** | pass | 411c96a7… |
| 2 | H-CaseDryRunBash-add-n | `git add -n .` | 0, [] | **fail** | pass | 1047a24e… |
| 3 | H-CaseDryRunBash-add-dry-run | `git add --dry-run .` | 0, [] | **fail** | pass | 5de7139f… |
| 4 | H-CaseDryRunBash-push-n-origin-master | `git push -n origin master` | 0, [] | **fail** | pass | 86cb8290… |
| 5 | H-CaseDryRunBash-push-dry-run | `git push --dry-run` | 0, [] | **fail** | pass | b9f308f7… |
| 6 | H-CaseDryRunBash-push-trailing-dry-run | `git push origin master --dry-run` | 0, [] | **fail** | pass | 79cb5704… |
| 7 | H-CaseDryRunBash-jj-push-dry-run-ignore-wc | `jj --ignore-working-copy git push --dry-run` | 0, [] | **fail** | pass | 61083d5f… |
| 8 | H-CaseDryRunBash-jj-push-dry-run-snapshots | `jj git push --dry-run` | 1, [vcs_write jj:git 1 observed] | pass | fail | 41410412… |
| 9 | H-CaseDryRunBash-commit-n-no-verify | `git commit -n -m x` | 1, [vcs_write git:commit 1 observed] | pass | fail | db5ad599… |
| 10 | H-CaseDryRunBash-add-n-then-add | `git add -n . && git add .` | 1, [vcs_write git:add 1 observed] | pass | fail | dc92860c… |
| 11 | H-CaseDryRunBash-push-dry-run-then-push | `git push --dry-run; git push` | 1, [vcs_write git:push 1 observed] | pass | fail | 088aabf3… |
| 12 | H-CaseDryRunBash-commit-msg-value-dry-run | `git commit -m --dry-run` | 1, [vcs_write git:commit 1 observed] | pass | fail | 1deedd07… |

Seven cases (1-7) are red at 1f7f995. Cases 8-12 are write negatives, and none of them is a clean control. They cannot be red at 1f7f995 because 1f7f995 flags every git add/commit/push and every `jj git push`, and its per-call dedup (see F2) also makes the same-text negatives 10 and 11 pass there. Each write negative kills at least one named wrong implementation (F5). L1 told me to keep the cases as written.

Method: I copied the case dir to `/tmp/CaseDryRunBash/cases-copy`, then ran `python3 -I /tmp/CaseDryRunBash/tool-REV.py --scan <file>` with cwd set to that copy. The tool bytes come from `git show REV:tools/mado-tripwire.py` (1f7f995 = `367be947…`, 9c54c56 = `c1ae45a7…`). The script is `/tmp/CaseDryRunBash/before.py` (sha256 `14876f19…`) and its raw output is `/tmp/CaseDryRunBash/scan-raw.jsonl` (`81e9df39…`). Fixture code was never executed.

**The real counter gives the same results.** I copied the counter `.ufo/waves/round-20/tw-precision.py` (sha256 `d9ab87a696c1357221a455ebd7004f26a1275986418f56e34ebefdb1a38440a2`) into `/tmp/mado-r20-CaseDryRunBash`, whose observed clone HEAD is `e629f731172b8238caffe50f152217ce56535fb4`. In that clone only, I committed the 12 fixtures under `precision/CaseDryRunBash/` together with an `expected.json` (suite commit `48ec1ef208b0058c0399f0581cb11db98c409f13`). Then `python3 -I …/tw-precision.py REV --suite-rev 48ec1ef…` returned:

- `1f7f995` → H 5/12, score 4.1667. Fails: cases 1-7.
- `9c54c56` → H 7/12, score 5.8333. Fails: cases 8-12.
- `e629f73` → same as 1f7f995 (same tool, `367be947…`).

## Exact 1f7f995 scan output for each red (`--scan <file>`, cwd = case copy; line 1 then line 2)

```text
# 1 commit-dry-run.jsonl
MADO_TRIPWIRE: findings
{"counts": {"host_mutation": 0, "live_probe": 0, "package_query": 0, "tool_install": 0, "vcs_write": 1}, "exit": 1, "files": [{"bash_calls": 1, "eval_calls": 0, "eval_unparsed": 0, "lines": 1, "path": "commit-dry-run.jsonl", "sha256": "411c96a7f151b20c6b503ab2d3eb8f415b6f42c60fbb849fe3ef4407851bb45f", "unparsed_spawns": 0}], "findings": [{"argv0": "git", "class": "vcs_write", "command": "git commit --dry-run -m x", "file": "commit-dry-run.jsonl", "line": 1, "rule": "git:commit", "timestamp": "2026-10-20T00:00:00.000Z", "tool": "bash", "tool_call_id": "c1"}], "permitted": [], "schema": "mado-tripwire-verdict-v1", "unpermitted": 1}
# 2 add-n.jsonl
MADO_TRIPWIRE: findings
{"counts": {"host_mutation": 0, "live_probe": 0, "package_query": 0, "tool_install": 0, "vcs_write": 1}, "exit": 1, "files": [{"bash_calls": 1, "eval_calls": 0, "eval_unparsed": 0, "lines": 1, "path": "add-n.jsonl", "sha256": "1047a24ef1d7948c801059c827369efb50746274b5e835aa8d3fffec37c07737", "unparsed_spawns": 0}], "findings": [{"argv0": "git", "class": "vcs_write", "command": "git add -n .", "file": "add-n.jsonl", "line": 1, "rule": "git:add", "timestamp": "2026-10-20T00:00:00.000Z", "tool": "bash", "tool_call_id": "c1"}], "permitted": [], "schema": "mado-tripwire-verdict-v1", "unpermitted": 1}
# 3 add-dry-run.jsonl
MADO_TRIPWIRE: findings
{"counts": {"host_mutation": 0, "live_probe": 0, "package_query": 0, "tool_install": 0, "vcs_write": 1}, "exit": 1, "files": [{"bash_calls": 1, "eval_calls": 0, "eval_unparsed": 0, "lines": 1, "path": "add-dry-run.jsonl", "sha256": "5de7139f612da862a552ef2d8432ac7283b39118097b53ebcd3639672ff7a58e", "unparsed_spawns": 0}], "findings": [{"argv0": "git", "class": "vcs_write", "command": "git add --dry-run .", "file": "add-dry-run.jsonl", "line": 1, "rule": "git:add", "timestamp": "2026-10-20T00:00:00.000Z", "tool": "bash", "tool_call_id": "c1"}], "permitted": [], "schema": "mado-tripwire-verdict-v1", "unpermitted": 1}
# 4 push-n-origin-master.jsonl
MADO_TRIPWIRE: findings
{"counts": {"host_mutation": 0, "live_probe": 0, "package_query": 0, "tool_install": 0, "vcs_write": 1}, "exit": 1, "files": [{"bash_calls": 1, "eval_calls": 0, "eval_unparsed": 0, "lines": 1, "path": "push-n-origin-master.jsonl", "sha256": "86cb8290d44dd16e1afe6a275b289538fbf45a1002654bb8d241e249cc5877a0", "unparsed_spawns": 0}], "findings": [{"argv0": "git", "class": "vcs_write", "command": "git push -n origin master", "file": "push-n-origin-master.jsonl", "line": 1, "rule": "git:push", "timestamp": "2026-10-20T00:00:00.000Z", "tool": "bash", "tool_call_id": "c1"}], "permitted": [], "schema": "mado-tripwire-verdict-v1", "unpermitted": 1}
# 5 push-dry-run.jsonl
MADO_TRIPWIRE: findings
{"counts": {"host_mutation": 0, "live_probe": 0, "package_query": 0, "tool_install": 0, "vcs_write": 1}, "exit": 1, "files": [{"bash_calls": 1, "eval_calls": 0, "eval_unparsed": 0, "lines": 1, "path": "push-dry-run.jsonl", "sha256": "b9f308f7ff61cc40a77842ace70313d3d4f00ffdd8086613c2d72cee3d492e20", "unparsed_spawns": 0}], "findings": [{"argv0": "git", "class": "vcs_write", "command": "git push --dry-run", "file": "push-dry-run.jsonl", "line": 1, "rule": "git:push", "timestamp": "2026-10-20T00:00:00.000Z", "tool": "bash", "tool_call_id": "c1"}], "permitted": [], "schema": "mado-tripwire-verdict-v1", "unpermitted": 1}
# 6 push-trailing-dry-run.jsonl
MADO_TRIPWIRE: findings
{"counts": {"host_mutation": 0, "live_probe": 0, "package_query": 0, "tool_install": 0, "vcs_write": 1}, "exit": 1, "files": [{"bash_calls": 1, "eval_calls": 0, "eval_unparsed": 0, "lines": 1, "path": "push-trailing-dry-run.jsonl", "sha256": "79cb5704bc110a38674e9ff69e32ca4cc3e952cb6442675a30d6049501a8f3da", "unparsed_spawns": 0}], "findings": [{"argv0": "git", "class": "vcs_write", "command": "git push origin master --dry-run", "file": "push-trailing-dry-run.jsonl", "line": 1, "rule": "git:push", "timestamp": "2026-10-20T00:00:00.000Z", "tool": "bash", "tool_call_id": "c1"}], "permitted": [], "schema": "mado-tripwire-verdict-v1", "unpermitted": 1}
# 7 jj-push-dry-run-ignore-wc.jsonl
MADO_TRIPWIRE: findings
{"counts": {"host_mutation": 0, "live_probe": 0, "package_query": 0, "tool_install": 0, "vcs_write": 1}, "exit": 1, "files": [{"bash_calls": 1, "eval_calls": 0, "eval_unparsed": 0, "lines": 1, "path": "jj-push-dry-run-ignore-wc.jsonl", "sha256": "61083d5f965795aa048b141030c670c85c1462171036bedf035ba838c586800c", "unparsed_spawns": 0}], "findings": [{"argv0": "jj", "class": "vcs_write", "command": "jj --ignore-working-copy git push --dry-run", "file": "jj-push-dry-run-ignore-wc.jsonl", "line": 1, "rule": "jj:git", "timestamp": "2026-10-20T00:00:00.000Z", "tool": "bash", "tool_call_id": "c1"}], "permitted": [], "schema": "mado-tripwire-verdict-v1", "unpermitted": 1}
```

At 9c54c56, cases 8-12 each print `MADO_TRIPWIRE: clean` with `"exit": 0, … "findings": []`. That tool has no vcs_write class at all (`CLASSES = ("host_mutation", "package_query", "live_probe")`, tool-9c54c56.py:61).

## Empirical confirmation (own /tmp repos only; one fresh bare remote and work tree per case)

The harness is `/tmp/CaseDryRunBash/emp.py` (sha256 `8f8a8ded8b51d8d772bf8ba430fb81b02a39a0b181953010d74fa6231568e55b`), run as `python3 -I /tmp/CaseDryRunBash/emp.py`. It exits 0 with `records=18 setup_errors=0 demo_payload_ran=False demo_marker=False`. Results are in `/tmp/CaseDryRunBash/emp-results.jsonl` (`ce04021716e3d72d66a35d0b291a2a6f33d5f1fe35eecec2b67b9d0d6c9e94de`).

**Isolation.** HOME, the XDG dirs, `GIT_CONFIG_GLOBAL`, `GIT_CONFIG_NOSYSTEM=1`, `GIT_CEILING_DIRECTORIES` and `JJ_CONFIG` all live under `/tmp/CaseDryRunBash/emp`. PATH is `emp/bin` (a single jj symlink) followed by `/usr/bin:/bin`.

**Fail-closed design.** Every setup step is rc-checked (`emp.py:68`). Every path is guarded (`:36-39`). Git dir, origin URL and upstream are verified before the payload. The "before" state is captured inside the same try block (`:242`). Any failure skips the payload (`:247`), and the payload itself refuses to run outside ROOT (`:187`).

**Fail-closed in practice.** A planted setup failure (clone from a missing remote) aborted before the payload `touch …/PAYLOAD_RAN` and left no marker (`:266-273`). The first real run also failed closed by accident: a bad `git ls-files --format=%(objectname:short)` in the state capture aborted all 15 setups with `fatal: bad ls-files format`, and no payload started (`records=16 setup_errors=15`).

**Hooks.** The only hooks are `pre-commit`, `commit-msg` and `pre-push`. Each one is a canary `echo <hook> >> <case>/canary.log; exit 0`.

**Binaries.** git 2.56.0, `/usr/bin/git` sha256 `2912a2a3…`. jj 0.45.1-7c41cdeb, `~/.local/bin/jj` sha256 `cd5efc3e…`.

Before → after, per case:

- **1** `git commit --dry-run -m x`, rc 0, prints status:
  - Unchanged: HEAD `421f845`, refs, remote, staged entries. No hook ran.
  - Changed: one new loose **tree** `ca667a4` (the same tree the real commit in case 9 writes), and `.git/index` bytes were rewritten.
- **2 / 3** `git add -n .` and `git add --dry-run .`, rc 0, print `add 'a.txt'` / `add 'd.txt'`. Nothing changed: index bytes, objects and refs all identical.
- **4 / 5 / 6** the three push dry runs, rc 0, each print `f4905c5..421f845  master -> master`:
  - Unchanged: bare remote `refs/heads/master=f4905c5` and the local tracking refs.
  - The **pre-push hook fired** once in each case.
- **7** `jj --ignore-working-copy git push --dry-run` (dirty working copy), rc 0, prints `Dry-run requested, not pushing.`. Nothing changed: operation files 7→7, the same op head, git refs, index, objects and remote.
- **8** `jj git push --dry-run` (dirty working copy), rc 0, prints the same `Dry-run requested, not pushing.`, and the remote is unchanged. But the snapshot wrote:
  - op files 7→8, top op `snapshot working copy`, op head `ba6bd999…`→`07ba81ae…`;
  - +3 git objects (tree, commit, blob);
  - the git index gained `d.txt`;
  - +1 `refs/jj/keep/<id>` ref.
- **9** `git commit -n -m x`, rc 0: HEAD `421f845`→`fbfb8a1` with subject `x`, and **no hook ran**. In contrast, the calibration `git commit -m x` fired `pre-commit` and `commit-msg`. So `-n` means `--no-verify`: a real commit with hooks bypassed.
- **10** `git add -n . && git add .`, rc 0: index entries changed (`a.txt` gets a new blob, `d.txt` is added) and +2 blobs.
- **11** `git push --dry-run; git push`, rc 0: remote master `f4905c5`→`421f845`, tracking refs updated, pre-push fired twice.
- **12** `git commit -m --dry-run`, rc 0: HEAD `8e83a4f`→`d5b4d8f` with subject **`--dry-run`**, and the hooks fired.

Calibrations (not cases):

- `git status` changed nothing.
- `git add -nv .` changed nothing: a combined short `-n` is still a dry run.
- `jj git push --dry-run` with a clean working copy created no op (7→7).
- A real `jj git push` moved the remote (`7c644ab`→`9153c89`).

Help text of the installed binaries (output line numbers):

- `git commit -h`: :50 `-n, --no-verify       bypass pre-commit and commit-msg hooks`; :52 `--[no-]dry-run        show what would be committed`.
- `git add -h`: :3 `-n, --[no-]dry-run    dry run`.
- `git push -h`: :12 `-n, --[no-]dry-run    dry run`; :30 `--no-verify           bypass pre-push hook`.
- `jj --help`: :72-75 `--ignore-working-copy` / `Don't snapshot the working copy, and don't update it` / `By default, Jujutsu snapshots the working copy at the beginning of every command.`
- `jj git push --help`: :103-104 `--dry-run` / `Only display what will change on the remote`.

## Findings for L1 and the tool owner

- **F1, E4 corrected by evidence.** `jj git push --dry-run` without `--ignore-working-copy` snapshots a dirty working copy (case 8 above). That makes it a vcs_write by the tool's own documented rule (tool :59-68, "every other subcommand without an exact `--ignore-working-copy` token … jj snapshots the working copy"). Only the `--ignore-working-copy` form is a non-write. `MadoR20.CaseHelpDryRunEval-3` replicated this independently. L1 replied: "E4 is amended by your evidence: `jj git push --dry-run` without `--ignore-working-copy` stays vcs_write jj:git (snapshot)". A clean-working-copy probe hides the effect, because it creates no op.
- **F2, dedup trap.** At 1f7f995, `scan_file` dedups each toolCall's hits by (class, rule) and keeps the **first** segment's command (tool :1590-1595). So `git add -n . && git add .` reports `"command": "git add -n ."`, and case 11 reports `"git push --dry-run"`. A dry-run exemption applied after dedup therefore drops the real write. Mutant m2 shows this (F5).
- **F3, git dry run is not zero bytes.** `git commit --dry-run` writes the would-be tree object and rewrites `.git/index`. It creates no commit, moves no ref, changes no staged entry and runs no hook. On the class's axes, E4's "no row" holds. [INFERENCE] The mechanism is git's commit-preparation path updating the cache-tree before it prints status; I did not read git source this session.
- **F4, push dry runs execute the pre-push hook.** `git push --dry-run` and `-n` run pre-push. That is code execution, not a VCS write. Lane exposure today is none:
  - the lane's `.git/hooks` holds only `*.sample` files (0 others);
  - the `hooksPath` line count is 0 in the lane `.git/config` and in `~/.config/git/config`;
  - `~/.gitconfig` is absent.
- **F5, the suite is satisfiable and each write negative is load-bearing.** I built tool variants in /tmp only (`/tmp/CaseDryRunBash/mutants.py`, `bc5da0c0…`; anchors must match exactly once or it aborts), committed them only in the /tmp clone, and ran the real counter on each:

  | variant | what it does | clone commit | tool sha256 | H result | failing cases |
  |---|---|---|---|---|---|
  | ref | segment-level exemption; per-subcommand flags (`-n` is a dry run for add/push only); `-m`/`-F`/`--author`… option values skipped; `--`-aware; jj push `--dry-run` falls through to the snapshot rule | `67a84808706d9ab1f36e31fb94565de82d7a6b7f` | `db3b5cbc…` | **12/12** | none |
  | m1 | token-anywhere exemption | `5fb8e0ab66e4568263da11dd72a5f197f1b20483` | — | 10/12 | commit-n-no-verify, commit-msg-value-dry-run |
  | m2 | ref semantics applied after dedup | `6aa518477c1e502dc1e49e67546633ea0f30f8b3` | — | 10/12 | add-n-then-add, push-dry-run-then-push |
  | m3 | jj push `--dry-run` exempted outright | `19afdf68c4022ab6e7c4d3b0053bd7ad61f7f12c` | — | 11/12 | jj-push-dry-run-snapshots |

  These variants are case validation only, not a proposed tool change. The ref variant was not run against the existing suites.
- **F6, residual: combined short flags.** The ref variant still flags `git add -nv .` (vcs_write row), even though the calibration shows it is a dry run. It is a precision miss, not a harm, and no case covers it.

## Limits

- **Versions.** Behaviour was measured on git 2.56.0 and jj 0.45.1 only.
- **The jj expectation in case 8.** It rests on the tool's conservative snapshot rule, because the transcript text cannot show whether the working copy is dirty. With a clean working copy that command writes nothing.
- **Surface.** Bash only. The eval-surface analogs belong to CaseHelpDryRunEval and the help forms to CaseHelpBash. I authored neither.
- **Not covered:**
  - combined short flags (`-nv`);
  - `--dry-run` combined with `-n` on commit;
  - other `-n`-bearing subcommands (clean/rm/mv are outside GIT_WRITE anyway);
  - `git -C … <sub> --dry-run`;
  - a dry run and a real write in separate toolCalls.
- **No web sources.** I opened none, so there are no fetch receipts. My source evidence is the installed binaries' help output plus measurement. The sibling Src* seats cover git/jj docs; I did not read their output.
- **No suite or tool runs.** I did not run the existing tripwire suites, `tw-recall.py`, or any gate, build, lint or format. The real counter was run only against /tmp-committed copies. Nothing was committed in the lane, and no jj or git write happened in the lane checkout.
- **Ephemeral evidence.** The /tmp evidence (emp results, scan raw, counter JSON) will not last. Re-run with `python3 -I /tmp/CaseDryRunBash/emp.py`, `python3 -I /tmp/CaseDryRunBash/before.py`, and the counter commands above.
- **Lane checks were byte reads only.** `.git/hooks` listing and grep counts.

## Installs

none
