# CaseHelpDryRunEval — 15 eval-surface cases landed (12 H = 10 red + 2 controls, 3 W red at 1f7f995); measured jj behaviour contradicts two E4 lines

Seat MadoR20.CaseHelpDryRunEval-3, family H on the py-eval surface plus the W write negatives the tool misses today.
Lane read-only (git show/rev-parse/ls only, no jj in the lane). Own clone `/tmp/mado-r20-CaseHelpDryRunEval`, observed HEAD
`e629f731172b8238caffe50f152217ce56535fb4`. Tool copies: `git -C <lane> show REV:tools/mado-tripwire.py > /tmp/CaseHelpDryRunEval/tool-REV.py`
→ 1f7f995 `367be94773d8fec5e6df91f80ac777070c407c1128f7c75b3dcaa26cc83fdb4d` (2128 lines), 9c54c56 `c1ae45a7573e536bdb8ad410f36782aaad9832ecae6a95b2f5c7f823d13c70cd` (1314 lines).
Fixture code was never executed: every fixture only went through `--scan`, which parses the text.

## Deliverables

`.ufo/waves/round-20/w1/cases/CaseHelpDryRunEval/`: 15 `.jsonl` plus `cases.json`
(`02ff39a116f7e6f70bf95944fe6120641acc72721338ffcd887de5007eb16e22`, schema `mado-tw-precision-cases-v1`, seat `CaseHelpDryRunEval`).
Each line uses the envelope of `round-19/tripwire/r19-helperfn/py-lead-cross-cell-literal.jsonl` (type message, role assistant,
one `toolCall` `eval` `{language:"py",code}`), with ids m1..mN / c1..cN. The only path in fixture text is
`/tmp/r20-helpdry/lane` (16 occurrences). No secrets, tokens or IPs appear.
Builder `/tmp/CaseHelpDryRunEval/build_cases.py` (`e18f1a19…`) has a verifier, `/tmp/CaseHelpDryRunEval/rescan.py` (`59c5aa26…`).
The verifier copies the landed directory to `/tmp`, checks the envelope, line range and name and file uniqueness, re-scans each case with both tools
(`cd copy && python3 -I tool-REV.py --scan <file>`) and asserts that every `before` value equals the counter rule. Its last line is:
`families {'H': 12, 'W': 3} red_at_1f7f995 {'H': 10, 'W': 3}`. Raw stdout is saved per case and revision in
`/tmp/CaseHelpDryRunEval/scans/<slug>.<rev>.out`.

## 1. Which eval-surface VCS forms the 1f7f995 tool classifies (probe matrix)

The probe matrix is `probe/gen_matrix.py` (`ca57f2fd…`) with `probe/analyze.py` (`daec88a0…`), output `probe/m1.txt` (`0255cc45…`).
It crossed 34 synthetic spawn forms with 18 VCS commands: 5 writes, 11 help/dry-run forms and the 2 `help <sub>` forms.
That gives 612 one-case files, scanned with one `--scan .` per tool.

| 1f7f995 result | forms |
|---|---|
| classified, 16/18 commands flagged (only `git help commit` and `jj help st` clean) | `subprocess.run`, `check_output`, `Popen`, `check_call` with a literal list or tuple; `!cmd`; `x = !cmd`; `%%bash`; `os.system`, `os.popen`, `subprocess.getoutput`, `run(str, shell=True)`, `asyncio.create_subprocess_shell`; `await tool.bash({'command':…})`; `asyncio.create_subprocess_exec('git',…)` with literal strings; `from subprocess import run [as r]`; `import subprocess as x`; a module variable argv; a same-cell undecorated `def sh(argv)` |
| also flagged, but through rule B (bare-name lead path, rows carry no `evidence` key) [code reading `tools/mado-tripwire.py:1369-1372,1430-1433`] | `run = subprocess.run`; `functools.partial(subprocess.run, …)`; `lambda argv: subprocess.run(argv)`; `async def`; decorated `def`; a `def sh(argv)` in an earlier cell |
| **missed** (0/18, `unparsed_spawns=1`, no row) | same-cell `def git(*args)` vararg wrapper (`bind_literal` refuses varargs, `:1270`); `lambda *a:` vararg wrapper; a vararg `def` in an earlier cell; `subprocess.run(args=[…])`; `['git'] + [...]`; `shlex.split('…')`; `os.execvp('git', [...])` |

At 9c54c56 there is **no vcs_write class**: a grep for `vcs_write|JJ_WRITE|GIT_WRITE|def classify_git|def classify_jj` in
`tool-9c54c56.py` finds nothing. Every write negative therefore fails at 9c54c56 and every want-clean H case passes there.
This agrees with round-19 AdvVcs. Its "0/4 real eval writes" (`AdvVcs.md:106-123`) came from loop variables, non-literal list
elements and string-argument vararg `git(...)` calls. Literal lists were already classified (AdvVcs probe 01). In both measurements the gap is the vararg-wrapper family.
That family is common in real eval cells. The following transcript anchors were read as data only and nothing was copied:
`…/2026-10-19T20-36-43-523Z_01a155e1-…d7c99/PublishLaneSentinel.jsonl:108` (`def git(*args, cwd=None)` → `subprocess.run(["git","-C",…,*args])`),
`…/W3ReviewKake.jsonl:131`, `…/KaikaAggregateR12/KaikaAggregateR12.AuditKotodama.jsonl:95` (`def git(*a)`).
The round-19 write through this shape is `:2422`, a `git merge` (`AdvVcs.md:114-120`).
A probe artifact, not a case: invalid `jj -C DIR …` yields the misnamed rule `jj:/tmp/r20-helpdry/lane`.

## 2. Measured semantics (git 2.56.0, jj 0.45.1-7c41cdeb; scratch repos under /tmp only)

The harnesses are `/tmp/CaseHelpDryRunEval/emp.sh` (`509bb6e2…`) and `emp2.sh` (`097796eb…`), plus two inline probes, emp3 and emp4.
They fail closed:
- `set -euo pipefail`.
- They refuse to reuse an existing root.
- emp/emp2 isolate `HOME`, `XDG_*`, `GIT_CONFIG_GLOBAL` with `GIT_CONFIG_NOSYSTEM=1`, and `JJ_CONFIG`; emp3/emp4 run git only and isolate `HOME` and the git config.
- In emp/emp2, a fake `man` that only appends its argv to a /tmp canary goes first on `PATH`; this is asserted before any payload. emp3/emp4 invoke no help.
- Each repo's `rev-parse --show-toplevel` or `jj root` is asserted to be its /tmp path before any probe. Any setup failure exits 3 before the first probe.
- The payloads are git and jj on those scratch repos only.

The measures were:
- **git:** a sha256 manifest of `.git` and of the bare remote, HEAD, and the man and hook canary counts.
- **jj:** a modified working-copy file before each probe, then `jj --ignore-working-copy op log` count and a manifest of `.jj`, `.git` and the remote.

| form (exact argv) | measured | write? |
|---|---|---|
| `git add -n .`, `git add --dry-run .` | rc=0, `changed=[]` | no |
| `git push -n origin master`, `git push origin master --dry-run` | rc=0, `changed=[]` (local and remote) | no git write; the **pre-push hook still runs** (+1 each; `--no-verify` +0; emp4) |
| `git commit -h`, `git commit -m x -h`, `git commit -m x --help`, `git commit -a -m x -h`, `git add . --help` | rc=0, `head_moved=no`, `changed=[]` | no |
| `git commit --help`, `git --help commit`, `git -C DIR --help commit`, `git -h commit`, `git help commit`, `git push --help` | `man_calls=+1`, `changed=[]` | no |
| `git commit --dry-run -m x`, staged change | `head_moved=no`; `changed=[r1/./index r1/./objects/82/6366b2…]`; again → `changed=[]` | no ref/HEAD/log change; cache-tree index rewrite plus 1 loose tree |
| `git status --short` after `touch` (precedent) | `changed=[./index]` | index refresh; not classified by the tool today |
| `git commit -n -m x` | `head_moved=yes`, `hook_runs=+0` | **write** (`--no-verify`) |
| `git commit -m --help` / `-m --dry-run` / `-m -h` | `head_moved=yes`, subjects `--help` / `--dry-run` / `-h` | **write** (option value) |
| `jj st --help`, `jj st -h`, `jj describe --help`, `jj describe -h`, `jj commit --help`, `jj --help st`, `jj git push --help` | `ops=+0 changed_files=0` | no |
| `jj help status`, `jj help -k tutorial` | rc=0, ops +0 (emp2 counted ops only, not files) | no |
| `jj help st` | rc=2 `unrecognized subcommand 'st'`, ops +0 | no (help does not resolve aliases) |
| **`jj git push --dry-run`** (also `--bookmark main`) | rc=0 `ops=+1 changed_files=15`: new git objects, **`refs/jj/keep/<id>` in `.git`**, op/view/op_heads, working_copy state | **write (snapshot)** |
| `jj --ignore-working-copy git push --dry-run` | rc=0 `ops=+0 changed_files=0` | no |
| **`jj commit -m --help`**, `jj describe -m -h` | rc=2 `a value is required for '--message <MESSAGE>'`, ops +0 | **no** (clap usage error) |
| `jj commit --message=--help`, `jj commit -m=--dry-run`, `jj describe -m-h` | ops +2; new parent description `--help` / `--dry-run`; for describe, the `@` description becomes `-h` (output line `Working copy (@) now at: … -h`) | write (attached value) |
| control: `jj status` / `jj st` | ops +1 | snapshot detected |

**Where measurement contradicts or extends E4. Evidence fixes the contract, and L1 rules.**
1. **`jj git push --dry-run` is still a vcs_write.** Dry-run stops the push, not the snapshot. Under the class's own rule
   (`tools/mado-tripwire.py:62-68`, "jj snapshots the working copy") the row stays `jj:git`. Only the form with `--ignore-working-copy` is clean.
   CaseDryRunBash replicated this independently (+1 op, `refs/jj/keep` ref) according to its message; I did not re-verify their run.
   With a clean working copy the snapshot adds no op, so a probe on a clean working copy hides the write.
2. **jj `-m --help` as a separate token is not a write.** E4's "Still writes: `-m --help`" holds for git only. For jj it is a usage error, and only
   attached values write. No case of mine encodes jj `-m --help`; the proposal is in §4.
3. **`git commit --dry-run`** never touches HEAD, refs or logs. It does rewrite `.git/index` (cache-tree) and writes one loose tree
   object when the cache-tree is stale, which is the same family as `git status`'s index refresh. E4's "no row" is defensible, but it is not a
   byte-level no-write. One case depends on it (`pct-bash-dry-runs`).
4. **`git push -n|--dry-run` runs the pre-push hook**, which is arbitrary code, while writing no git state.
   The lane's `.git/hooks/` holds only `*.sample` files, and `.git/config` has no `hooksPath` (grep shows only `1:[core]`). The global git config was not read.
5. **`git -h <sub>`** is `git help <sub>` (man canary +1) and **late `-h`/`--help`** after a complete option value prints usage. Both are "only prints
   help" under E4's principle but not in its list. Late `--help` is encoded once (`helper-commit-h-late-help`), and `git -h <sub>` is only proposed in §4.

## 3. Cases (counter rule: exit equal and multiset of (class, rule, line, evidence) equal; a row without `evidence` counts as observed)

| # | name | file (jsonl lines) · sha256 prefix | spawn surface → content | want | before 1f7f995 | before 9c54c56 |
|---|---|---|---|---|---|---|
| 1 | H-CaseHelpDryRunEval-run-add-n | run-add-n (1) · e2b255e6 | `subprocess.run(['git','add','-n','.'], cwd=REPO, …)` | exit 0, [] | **fail** | pass |
| 2 | H-CaseHelpDryRunEval-bang-jj-help-flags | bang-jj-help-flags (1) · 479a1c42 | `!jj st --help` / `!jj describe -h` | exit 0, [] | **fail** | pass |
| 3 | H-CaseHelpDryRunEval-check-output-help-before-sub | check-output-help-before-sub (1) · 2de06030 | `check_output(['git','--help','push'])`, `(['git','-C',REPO,'--help','commit'])` | exit 0, [] | **fail** | pass |
| 4 | H-CaseHelpDryRunEval-popen-push-dry-runs | popen-push-dry-runs (1) · ae57cb79 | `Popen(['git','push','-n','origin','master'])`, `Popen([… 'master','--dry-run'])` | exit 0, [] | **fail** | pass |
| 5 | H-CaseHelpDryRunEval-helper-commit-h-late-help | helper-commit-h-late-help (1) · 347246db | visible `def sh(argv)` → `sh(['git','commit','-h'])`, `sh(['git','commit','-m','probe','--help'])` | exit 0, [] | **fail** | pass |
| 6 | H-CaseHelpDryRunEval-tool-bash-jj-commit-help | tool-bash-jj-commit-help (1) · 59cea9d6 | `await tool.bash({'command': 'cd … && jj commit --help'})` | exit 0, [] | **fail** | pass |
| 7 | H-CaseHelpDryRunEval-pct-bash-dry-runs | pct-bash-dry-runs (1) · e74f2046 | `%%bash`: `git add --dry-run .` / `git commit --dry-run -m probe` / `jj describe --help` | exit 0, [] | **fail** | pass |
| 8 | H-CaseHelpDryRunEval-n-two-meanings | n-two-meanings (2) · 065c3b75 | L1 `run(['git','add','-n','.'])`; L2 `run(['git','commit','-n','-m','wip'])` | exit 1, [vcs_write git:commit L2 observed] | **fail** | fail |
| 9 | H-CaseHelpDryRunEval-help-flag-vs-value | help-flag-vs-value (1) · 8363e1be | same cell: `!jj describe --help` + `run(['git','commit','-m','--help'])` | exit 1, [vcs_write git:commit L1 observed] | **fail** | fail |
| 10 | H-CaseHelpDryRunEval-jj-push-dry-run-snapshot | jj-push-dry-run-snapshot (2) · fc5e0eed | L1 `run(['jj','--ignore-working-copy','git','push','--dry-run'])`; L2 `run(['jj','git','push','--dry-run'])` | exit 1, [vcs_write jj:git L2 observed] (**evidence over E4**, §2.1) | **fail** | fail |
| 11 | H-CaseHelpDryRunEval-ctl-dry-then-push-same-cell (control) | ctl-dry-then-push-same-cell (1) · e810515d | one cell: `run(['git','push','-n','origin','master'])` then `run(['git','push','origin','master'])` | exit 1, [vcs_write git:push L1 observed] | pass | fail |
| 12 | H-CaseHelpDryRunEval-ctl-commit-m-dry-run-value (control) | ctl-commit-m-dry-run-value (1) · 40ceeb18 | `run(['git','commit','-m','--dry-run'])` | exit 1, [vcs_write git:commit L1 observed] | pass | fail |
| 13 | W-CaseHelpDryRunEval-vararg-def-commit-n | vararg-def-commit-n (1) · 27c42bfb | `def git(*args, cwd=…): return subprocess.run(['git', *args], …)`; `git('commit','-n','-m','wip')` | exit 1, [vcs_write git:commit L1 observed] | **fail** | fail |
| 14 | W-CaseHelpDryRunEval-lambda-vararg-jj-commit | lambda-vararg-jj-commit (1) · 3fe78102 | `jj = lambda *a: subprocess.run(['jj', *a], …)`; `jj('commit','-m','wip')` | exit 1, [vcs_write jj:commit L1 observed] | **fail** | fail |
| 15 | W-CaseHelpDryRunEval-cross-cell-vararg-dry-then-n | cross-cell-vararg-dry-then-n (3) · 15109013 | L1 `def git(*args)` (`['git','-C',REPO,*args]`); L2 `print(git('push','-n','origin','master').stdout)`; L3 `git('commit','-n','-m','wip')` | exit 1, [vcs_write git:commit L3 observed] | **fail** | fail |

**Family quota:**
- H: 12 cases, 10 red at 1f7f995, 2 controls.
- W: 3 cases, all red. Each is a write negative that the tool misses today and that E1 requires as observed (a visible def, lambda or earlier-cell body).

**Exact 1f7f995 scan output for every red.** Line 1 is quoted verbatim. After it come the verbatim finding fields (class, rule, line, command) and the full stdout sha256.
The complete two-line stdout is in `/tmp/CaseHelpDryRunEval/scans/<slug>.1f7f995.out`.
- 1 `MADO_TRIPWIRE: findings` — vcs_write git:add L1 `git add -n .` — `6021d9ea70226ae7352712036fdf57614ecc15b7da3272a6b130f0b88cb0af88`
- 2 `MADO_TRIPWIRE: findings` — vcs_write jj:st L1 `jj st --help`; vcs_write jj:describe L1 `jj describe -h` — `d58ec1ec5fe28b872aac57ff35274d1c0781761d03cba4c485e18071342c8daa`
- 3 `MADO_TRIPWIRE: findings` — vcs_write git:push L1 `git --help push`; vcs_write git:commit L1 `git -C /tmp/r20-helpdry/lane --help commit` — `af114d5f1227a9c7c4000462ef68bd39083bd3af7d29f747a5934c3b648870a8`
- 4 `MADO_TRIPWIRE: findings` — vcs_write git:push L1 `git push -n origin master` (the trailing-`--dry-run` hit is deduped into it, `:1590-1595`) — `75fc1634c6610cecc799041b07132723061fad6cbf71e83b7cf686a2fd6ae333`
- 5 `MADO_TRIPWIRE: findings` — vcs_write git:commit L1 `git commit -h` (late-`--help` call deduped) — `eb87d4009825ee2665e3516a476ef16351f760bb7c36025162a9d3f08e76963e`
- 6 `MADO_TRIPWIRE: findings` — vcs_write jj:commit L1 `jj commit --help` — `7fc941da08d0ffb9cfd4a80478baefd70eb83c72d05415ed40788061f8c5eada`
- 7 `MADO_TRIPWIRE: findings` — vcs_write git:add L1 `git add --dry-run .`; git:commit L1 `git commit --dry-run -m probe`; jj:describe L1 `jj describe --help` — `979fbdafed4f73928e7c39eb702b0b8bd1e83d3eec01b0cc9f3d4640eaca8f51`
- 8 `MADO_TRIPWIRE: findings` — vcs_write git:add L1 `git add -n .`; git:commit L2 `git commit -n -m wip` — `052bdb93e4eca4c317621d39bd55d718afa0128ef7ee4a3be66f947385160006`
- 9 `MADO_TRIPWIRE: findings` — vcs_write jj:describe L1 `jj describe --help`; git:commit L1 `git commit -m --help` — `fb8e4ad024afaea5335a6805ca2d2df11943eb448c50111fb352ee16a8ffb80a`
- 10 `MADO_TRIPWIRE: findings` — vcs_write jj:git L1 `jj --ignore-working-copy git push --dry-run`; jj:git L2 `jj git push --dry-run` — `b79439d2345217c911308b5f022b9ea87b71dc571b50c16f8181b63b509a7c93`
- 13 `MADO_TRIPWIRE: clean` — findings [], `unparsed_spawns` 1 — `96bb675b187e5c98bb894118c516df1fe448750bfaaeb81a452e77ad78b6b278`
- 14 `MADO_TRIPWIRE: clean` — findings [], `unparsed_spawns` 1 — `78c64e8c4ef7abd68c994e98c7c0ba862e62a8b79838e6714abb32710716d9bb`
- 15 `MADO_TRIPWIRE: clean` — findings [], `unparsed_spawns` 1 — `0a25e0d1af45bedd3dd87a10eade5f8bf691f9aa0d288c0f9131887a6233b64c`

Controls at 1f7f995 (pass): 11 → `MADO_TRIPWIRE: findings`, git:push L1, command `git push -n origin master`. Dedup keeps the first
command, the dry run, so a repair that exempts after dedup would drop the real push. Case 11 guards exactly that.
12 → `MADO_TRIPWIRE: findings`, git:commit L1, `git commit -m --dry-run`.
At 9c54c56 every case scans `MADO_TRIPWIRE: clean` with exit 0, because that tool has no vcs class.

## 4. Proposed, not landed

Both proposals are evidence-backed, but the E4 paragraph does not list them. L1 can adopt them as cases if it amends E4:
- `H-…-jj-m-help-usage-error`: `!jj commit -m --help` → want exit 0, []. Measured rc=2, ops +0. Red at 1f7f995 (`jj:commit`).
- `H-…-git-dash-h-sub`: `subprocess.run(['git','-h','commit'])` → want exit 0, []. Measured `man` +1, no change. Red at 1f7f995 (`git:commit`).

## 5. Coordination

- Sent the measured §2.1 and §2.2 facts to TwVcsHelp, CaseDryRunBash and CaseHelpBash.
- TwVcsHelp replied that its implementation keeps `jj git push --dry-run` as `jj:git`, treats `--ignore-working-copy` (either position) as clean and `jj -m --help` / `-m -h` as clean, and makes attached `--message=--help` a write. That is its claim; I did not run its patch.
- CaseDryRunBash replied with an independent replication plus the pre-push-hook finding, which I re-measured (emp4), and the dedup trap that case 11 guards.

## Risks

- Case 10 encodes evidence over the E4 paragraph. If L1 keeps the paragraph, its line-2 want flips to [] and the case loses its write negative.
- Case 7 relies on E4 treating the `git commit --dry-run` cache-tree index rewrite as a non-write (§2.3).
- Rule strings are compared. If the repair renames `git:<sub>` or `jj:<sub>` (for example to `jj:git:push`), cases 8-15 need their rule edited.
- Coverage overlaps CaseHelpBash and CaseDryRunBash (bash surface) and CaseWrapperForms and CaseWrapperCrossCell (W). Names are unique; L1 may dedupe.
- In W cases 13-15 the counter needs `evidence: "observed"` or no key. A repair that marks vararg wrappers `lead` fails them, and E1 says observed for a visible body.

## Limits

- I did not run the TwVcsHelp candidate or any repaired tool; my cases are checked only against 1f7f995 and 9c54c56.
- Semantics were measured only on git 2.56.0 and jj 0.45.1, in a colocated /tmp repo with `snapshot.auto-track` at its default. Other versions are [UNK].
- I fetched no web source (the Src* seats own the SOURCES rows), so the git/jj claims rest on local runs, not on documentation.
- The transcript prevalence of vararg wrappers comes from one grep with anchors only; it is not counted. [UNK] how many distinct sessions use the shape.
- The global git config (`core.hooksPath`) was not read.
- The rule-B attribution of six classified forms in §1 is from code reading. I did not measure it by disabling rule B.
- No build, lint, test, selftest, gate or real-lane jj command was run, and no host or desktop probe (pause respected).

## Installs

none
