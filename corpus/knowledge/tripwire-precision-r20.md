source: S099 (git v2.56.0 git-commit: --dry-run, -n = --no-verify); S100 (git-add -n/--dry-run); S101 (git-push -n/--dry-run); S102 (git.c --help rewrite, parse-options -h); S103 (jj v0.45.1 help before workspace load); S104 (jj git push --dry-run); S105 (CPython 3.14.8 builtins); S106 (collections); S107 (shlex.join); S108 (subprocess args); S109 (util-linux 2.42.4 unshare/mount); S110 (bash 5.3 set -e exceptions); S111 (CPython execution model, name resolution); S112 (man-pages 6.16 user_namespaces); S113 (CPython os Process Management); S114 (json.dumps); S115 (subprocess.list2cmdline)
verified-at: 2026-10-21; tool `tools/mado-tripwire.py` sha256 `a57d4fe9277ff06c9b5916fc731e91f05bcd69cf05639cb2090ebcb00b5b6458` at commit `a8960de` (v3.1; v3 `3610e3e` and the first repair `9613f510…` at `28c6837` are superseded); host git 2.56.0, jj 0.45.1, Python 3.14.8 and util-linux 2.42.4 equal the source tags; host bash 5.3.20 against the bash-5.3 manual (S110 does not establish patch-level identity)
recheck: on a tool change re-run `python3 -I .ufo/waves/round-20/tw-precision.py REV`, `.ufo/waves/round-19/tw-recall.py REV` and `python3 .ufo/waves/round-20/a2/a2-guards.py REV --fixtures-rev 6a7d9ca`; on a git/jj/CPython/bash/util-linux upgrade re-open the matching row (`on-release`); S112 every 180 days
scope: lane tooling — the post-hoc transcript tripwire and hermetic stub harnesses (not a host plane)

# Tripwire precision: observed vs lead, VCS help/dry-run, fail-closed harnesses — round 20

Round 19 raised tripwire recall with a rule that read any literal argv handed to an
unknown name as a command, and emitted it with the same shape as an observed command.
`BLOCK=frozenset(['pacman','-Q','hyprland'])` became a `package_query` finding (closure
`round-19-verifier-spotcheck.md:63-81`). This note states what a round-20 row means, and
which forms are and are not writes. The tripwire reads transcript text; it never runs it.

The first repair (`28c6837`) fixed precision by following only the calls on an execution
path — and silently dropped every body it did not follow: wave 2 found 49 real-execution
shapes (thread targets, `asyncio.run(coro())`, decorators, returned closures, dunders,
inline lambdas) that both older tools reported and `28c6837` did not, a ~N⁴ expansion on
self-recursive helpers (30 s vs 0.07 s), and a RecursionError at half the old depth. v3
(`3610e3e`) keeps the precision and restores the recall as `lead` rows (§1, "swept"); v3.1
(`a8960de`) stops any help/dry-run exemption in an unparsed segment after the corpus diff
from `28c6837` showed a next command's `-ohE` cluster hiding a real `git checkout`.

## 1. What a row means

| Row | Meaning | Example |
|---|---|---|
| `evidence: observed` | the transcript states the command and the path that runs it: bash text, `!`/`%%bash`, a literal spawn (subprocess/os/asyncio/`tool.bash`, including an alias such as `run = subprocess.run`, `functools.partial(subprocess.run, …)` or `sp = importlib.import_module('subprocess')`), or a helper whose body is visible in the same file and is called with bindable arguments — earlier py eval cells count until a `reset` cell | `W-WrapperCrossCell-r13-verbatim` (the real round-13 `run_record` defined in cell 1, called in cell 2) |
| `evidence: lead` (opaque callee) | a literal host argv handed to a callee whose body is not visible: an unbound name, a name imported from a non-stdlib module, a parameter, a spawn-named method (`run`, `Popen`, `system`, …) of an object the scan cannot resolve, or argv handed beside a spawn callable (`Thread(target=subprocess.run, args=(argv,))`) | `L-CaseLeadsInvisible-run-record` (the frozen `r13-root.jsonl:4` shape) |
| `evidence: lead` (swept body) | a visible body the executed text reaches without a followed call: a def/lambda/class handed on as a value, a bare decorator, a returned closure, an inline or immediately invoked lambda, the dunders of a constructed or used class, a coroutine created without `await`, a recursive call, a helper past the depth (four bodies) or the 2000-follow budget, a call whose arguments cannot be bound; parameters unknown, each body once per cell | w2 `AdvRecallShapes/ar11-thread-target-def` (`Thread(target=w).start()`), `ar01-asyncio-run-cse` |
| no row | the callee is provably data: a builtin not rebound in the text (S105; `frozenset`, `tuple`, …); a callable of a stdlib module that cannot start a process, run code text or call back (S113 names the process side; S106 `deque`, S107 `shlex.join`, S114 `json.dumps`, S115 `subprocess.list2cmdline`; `heapq`, `copy`, `os.path`, `logging`, …); a visible def/lambda/class whose body has no spawn; a body nothing in the executed text references | `P-CasePureBuiltins-frozenset-closure`; w2 `AdvPureShapes/AP-ap01-deepcopy` |

A lead stays in `findings` and exits 1 unless its class is permitted, and the verdict
counts `observed_findings` and `lead_findings` separately. Keeping it in `findings` is
deliberate: the registered recall counter reads that list, and a separate list would let
a demoted false positive pass the precision counter (w1 RevLeadExitSemantics). A report
states the split: `tw-recall.py` at `a8960de` flags 6/6 incident lines = **5 observed +
1 lead** (`r13-root.jsonl:4`). A `lead` row whose exact command is already `observed`
in the same tool call is dropped (w2 CorpusRuntime found such pairs); a lead for a
different command under the same rule stays (`L-AdoptW2-AdvHelperFn-c03`).

Name binding follows Python (S111): the binding in effect at the call wins; a call before
its `def` is a lead; `del` of a name that shadowed a builtin falls back to the builtin
(no row); a builtin rebound to a spawner (`print = lambda a: subprocess.run(a)`) is
judged by its binding. Keyword argv (`subprocess.run(args=[...])`) is the same command
slot as the positional one (S108). A class body executes when the class statement runs,
so a spawn there is observed. Reading `globals()`/`locals()`/`vars()` (discarded,
subscripted, tested with `in`, printed) rebinds nothing; any other use of the result
resets the bindings as before (w2 RevToolDiffLeads).

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
| `git add -n` / `--dry-run`, also in a short cluster (`-nv`, `-An`) | no | S100 `:67-70`; measured: index bytes unchanged; clusters measured by w2 AdvVcsForms (fixed in v3) |
| `git push -n` / `--dry-run` | no ref change; the pre-push hook still runs | S101 `:161-163`; measured |
| `git pull -n`, `merge -n`, `cherry-pick -n`, `add -N` | **yes** (`-n` is not dry-run there) | `git <sub> -h` output, w1 ScoutCorpusVcsNonWrites |
| `jj … -h` / `--help` | no — clap answers before any workspace load or snapshot | S103 `command_error.rs:1113-1115`; measured: 0 ops |
| `jj help …` | no — dispatched to `cmd_help`, which loads no workspace (not a clap answer) | S103; w2 ReopenJj; measured: 0 ops |
| `jj -R git --ignore-working-copy git push …`, `jj -R bookmark … bookmark create …` | **yes** — the subcommand is found by position, not by the first token spelling it | w2 RevToolDiffVcs measured a pushed ref and a created bookmark; missed at `28c6837`, found at `a8960de` |
| `jj describe -m --help` | no — jj refuses a hyphen-leading value (exit 2, 0 ops); `-m=--help` writes | measured |
| `jj git push --dry-run` | **yes** — the working copy is snapshotted before the dry-run return | S104 `push.rs:231`; measured: +1 op, `refs/jj/keep` |
| `jj --ignore-working-copy git push --dry-run` | no | measured: +0 ops |
| `jj <alias> --help` with a user alias | **can run the alias** | TwVcsHelp: a config alias forwarding to `util exec` ran its script; the tool keeps unknown/variable verbs as writes |

The exemption is decided per command segment before the per-tool-call de-duplication,
so `git add -n . && git add .` still reports the real add. No exemption applies in an
unparsed segment (shlex failed, the line was split on whitespace and its tokens may run
into the next command; rule suffix `/unparsed`): in
`git -C $C checkout -q --detach X; bash -c 'git grep -ohE …'` the cluster `-ohE` holds an
`h`, and v3 read the checkout as usage; v3.1 keeps it a write (corpus diff from
`28c6837`, `W3ReviewLore.jsonl:119`; lesson M15).

Installers (tool_install): for the uv/pip/cargo install, upgrade and uninstall forms an
exact `-h`/`--help` before `--` prints help and installs nothing (held-out fx8 measured
`uv tool install --help`: tool and cache dirs untouched); run forms (`uvx`, `npx`, `uv
tool run`, `pipx run`, `npm exec`) hand a trailing `--help` to the package they fetch, so
they stay findings. pip's `-h` is an inference from optparse, not a measurement.

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
   failures (four through PATH stubs, two real missing target/stub paths) over `/tmp`
   targets, a `/tmp` canary payload with an execution witness, and a positive control;
   controls are not exported to the harness. At `a8960de` the round-19 shape reads
   `FAIL_OPEN` in 5 of 6 modes, `isolate.sh` `FAIL_CLOSED` in all 6, and every committed
   adversarial harness (env-aware, masked, fake-cmp, canary-deleter) and mutant reads
   `FAIL_OPEN` in at least one mode (`a2/evidence/iso/crit29-*.txt`).
4. Fail-closed setup is not containment: unstubbed host paths and the compositor/session
   sockets stay reachable inside `isolate.sh`. It is no licence to run a host probe
   while the host pause binds.

## Limits

- The precision suite (175 cases) was written in the same round as the repair, by seats
  blind to the patch but under one contract; 172/175 pass at `28c6837` and at `a8960de`.
  The held-out set (12 cases outside the contract) reads 0/12 at `28c6837` and 2/12 at
  `a8960de` (installer `--help`). The wave-2 adversarial populations
  (`a2-guards.py`): recall losses 52 → 0, RecursionError flips 13 → 0, pure-data rows
  24 → 0, measured VCS non-writes flagged 31 → 20, measured writes missed 0 → 0.
- A swept `lead` says "this body may run"; it is not proof that it ran (a thread target
  may never start, a lambda may never be called). The depth (four bodies) and the
  2000-follow budget are cut-offs, past which bodies are swept, not followed.
- Not resolved: `getattr`/dynamic dispatch, inherited methods, metaclasses/descriptors,
  a decorator that replaces the function it wraps (the def body is still followed),
  and a `global` rebinding made inside a called helper (w2 AdvLeadMarks).
- Scripts written then run, shell aliases, JavaScript cells and other sessions are not
  analysed; `clean` bounds only the covered forms. Shell function bodies are classified
  where they are defined, called or not.
- git/jj option tables are pinned to git 2.56.0 and jj 0.45.1; a newer value-taking
  option missing from the table could hide a write. Abbreviated `--dry`/`--porcel` and
  `--dry-run=false` forms stay findings (20 measured non-writes still flagged).
