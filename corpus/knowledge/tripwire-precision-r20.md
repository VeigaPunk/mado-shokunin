source: S099 (git v2.56.0 git-commit: --dry-run, -n = --no-verify); S100 (git-add -n/--dry-run); S101 (git-push -n/--dry-run); S102 (git.c --help rewrite, parse-options -h); S103 (jj v0.45.1 help before workspace load); S104 (jj git push --dry-run); S105 (CPython 3.14.8 builtins); S106 (collections); S107 (shlex.join); S108 (subprocess args); S109 (util-linux 2.42.4 unshare/mount); S110 (bash 5.3 set -e exceptions); S111 (CPython execution model, name resolution); S112 (man-pages 6.16 user_namespaces)
verified-at: 2026-10-20; tool `tools/mado-tripwire.py` sha256 `9613f510054043e71463a52b87178ee967dad8132a054159d43603876b85e27c` at commit `28c6837`; host git 2.56.0, jj 0.45.1, bash 5.3.20, Python 3.14.8, util-linux 2.42.4 (versions equal the source tags)
recheck: on a tool change re-run `python3 -I .ufo/waves/round-20/tw-precision.py REV` and `.ufo/waves/round-19/tw-recall.py REV`; on a git/jj/CPython/bash/util-linux upgrade re-open the matching row (recheck `on-release`)
surface: lane tooling — the post-hoc transcript tripwire and hermetic stub harnesses (not a host plane)

# Tripwire precision: observed vs lead, VCS help/dry-run, fail-closed harnesses — round 20

Round 19 raised tripwire recall with a rule that read any literal argv handed to an
unknown name as a command, and emitted it with the same shape as an observed command.
`BLOCK=frozenset(['pacman','-Q','hyprland'])` became a `package_query` finding (closure
`round-19-verifier-spotcheck.md:63-81`). This note states what a round-20 row means, and
which forms are and are not writes. The tripwire reads transcript text; it never runs it.

## 1. What a row means

| Row | Meaning | Example (precision-suite case at `28c6837`) |
|---|---|---|
| `evidence: observed` | the transcript states the command and the path that runs it: bash text, `!`/`%%bash`, a literal spawn (subprocess/os/asyncio/`tool.bash`, including an alias such as `run = subprocess.run` or `functools.partial(subprocess.run, …)`), or a helper whose body is visible in the same file — earlier py eval cells count until a `reset` cell | `W-WrapperCrossCell-r13-verbatim` (the real round-13 `run_record` defined in cell 1, called in cell 2) |
| `evidence: lead` | a literal host argv handed to a callee whose body is not visible: an unbound name, a name imported from a non-stdlib module, a parameter | `L-CaseLeadsInvisible-run-record` (the frozen `r13-root.jsonl:4` shape) |
| no row | the callee is provably data: a builtin not rebound in the text (S105; `frozenset`, `tuple`, …), a pure stdlib callable (S106, S107; `deque`, `Counter`, `namedtuple`, `shlex.join`, `json.dumps`), a visible def/lambda/class whose body has no spawn, or an attribute call such as `pytest.param(...)` | `P-CasePureBuiltins-frozenset-closure` |

A lead stays in `findings` and exits 1, and the verdict counts `observed_findings` and
`lead_findings` separately. Keeping it in `findings` is deliberate: the registered recall
counter reads that list, and a separate list would let a demoted false positive pass the
precision counter (w1 RevLeadExitSemantics). A report states the split:
`tw-recall.py` at `28c6837` flags 6/6 incident lines = **5 observed + 1 lead**
(`r13-root.jsonl:4`, whose `run_record` is defined only in the full transcript, not in
the frozen snapshot).

Name binding follows Python (S111): the binding in effect at the call wins; a call before
its `def` is a lead; `del` of a name that shadowed a builtin falls back to the builtin
(no row); a builtin rebound to a spawner (`print = lambda a: subprocess.run(a)`) is
judged by its binding. Keyword argv (`subprocess.run(args=[...])`) is the same command
slot as the positional one (S108). A class body executes when the class statement runs,
so a spawn there is observed.

## 2. git and jj: which invocations write

Measured on host git 2.56.0 and jj 0.45.1 in seat-owned `/tmp` repositories (w1
ScoutGitDryEmpirical, ScoutJjHelpEmpirical, CaseHelpBash, CaseDryRunBash,
CaseHelpDryRunEval, TwVcsHelp); semantics from the pinned sources.

| Form | Writes? | Source / measurement |
|---|---|---|
| `git <sub> --help` (first argument) | no — rewritten to `git help` before the subcommand runs | S102 `git.c:762` |
| `git <sub> … -h` or `--help` as a flag among options | no — usage, exit 0 | S102 parse-options; `git commit -m x --help` measured: no commit |
| `git commit -m --help`, `git commit -m -h` | **yes** — the token is the message | measured: commit with subject `--help` |
| `git commit --dry-run` (also `--short`, `--porcelain`, `--long`, `-z`) | no ref or index entry change (a tree object and the index cache may be rewritten) | S099 `:378-381`; measured |
| `git commit -n` | **yes** — `-n` is `--no-verify` | S099 `:218-221`; measured |
| `git add -n` / `--dry-run` | no | S100 `:67-70`; measured: index bytes unchanged |
| `git push -n` / `--dry-run` | no ref change; the pre-push hook still runs | S101 `:161-163`; measured |
| `git pull -n`, `merge -n`, `cherry-pick -n`, `add -N` | **yes** (`-n` is not dry-run there) | `git <sub> -h` output, w1 ScoutCorpusVcsNonWrites |
| `jj … -h` / `--help`, `jj help …` | no — clap answers before any workspace load or snapshot | S103 `command_error.rs:1113-1115`; measured: 0 ops |
| `jj describe -m --help` | no — jj refuses a hyphen-leading value (exit 2, 0 ops); `-m=--help` writes | measured |
| `jj git push --dry-run` | **yes** — the working copy is snapshotted before the dry-run return | S104 `push.rs:231`; measured: +1 op, `refs/jj/keep` |
| `jj --ignore-working-copy git push --dry-run` | no | measured: +0 ops |
| `jj <alias> --help` with a user alias | **can run the alias** | TwVcsHelp: a config alias forwarding to `util exec` ran its script; the tool keeps unknown/variable verbs as writes |

The exemption is decided per command segment before the per-tool-call de-duplication,
so `git add -n . && git add .` still reports the real add.

## 3. Fail-closed isolation harnesses

Under `set -e`, bash does not exit when the failing command is "part of any command
executed in a && or || list except the command following the final && or ||" (S110
`bashref.texi:5940-5941`). Round 19's first harness armed each stub with
`[ -e "$p" ] && mount --bind … && echo armed`; the mounts failed (unprivileged
`--map-current-user` gives no CAP_SYS_ADMIN in the mount namespace's owner; S109, S112)
and the payload — a real `hyprctl probe` — ran. Rules:

1. Test each setup step on its own and abort before the payload: `mount … || exit 125`,
   then verify the target now holds the stub (`cmp … || exit 125`).
2. A missing target or stub is a setup failure, not a skip.
3. Check a harness with `bash .ufo/waves/round-20/isolation-check.sh HARNESS`: six forced
   failures through PATH stubs over `/tmp` targets, a `/tmp` canary payload, a positive
   control. The round-19 shape reads `FAIL_OPEN` in 5 of 6 modes; `isolate.sh` reads
   `FAIL_CLOSED` in all 6.
4. Fail-closed setup is not containment: `isolate.sh` keeps the caller's environment and
   the compositor/session sockets stay reachable inside it. It is no licence to run a
   host probe while the host pause binds.

## Limits

- The precision suite (175 cases) was written in the same round as the repair, by seats
  blind to the patch but under one contract; 172/175 pass at `28c6837`. The held-out set
  (12 cases outside the contract: bash function shadowing, pipes into `xargs`/`bash`,
  `jj log --version`, installer `--help`) reads 0/12 before and after.
- A visible body is resolved to depth 4; `**kw`, starred and vararg forwarding are
  resolved only when the call states literal values.
- Scripts written then run, shell aliases, `python -c` bodies, JavaScript cells and other
  sessions are still not analysed; `clean` bounds only the covered forms.
- git/jj option tables are pinned to git 2.56.0 and jj 0.45.1; a newer value-taking
  option missing from the table could hide a write.
