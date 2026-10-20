source: S1xx-pending (git-commit: git-commit usage, `-n`/`--no-verify` and `--dry-run` options); S1xx-pending (git-add/git-push: `add -n|--dry-run`, `push -n|--dry-run`); S1xx-pending (git.c: `-h`, `--help`, `help` dispatch); S1xx-pending (jj help: `jj help`, `-h|--help` on jj subcommands); S1xx-pending (Python builtins: `frozenset`, `callable`, name binding); S1xx-pending (shlex: `shlex.join`, `shlex.quote`); S1xx-pending (bash manual: `set -e` exemptions for `&&`/`||` lists and `if`); local observations listed in § Local checks (git 2.56.0, jj 0.45.1, bash 5.3.20, Python 3.14.8, util-linux unshare 2.42.4 present but not run)
verified-at: 2026-10-20; source rows are reserved S099-S110 and are not yet opened or assigned, so every upstream statement below is [INFERENCE] until its S1xx row lands; local behaviour was observed in /tmp scratch only (no lane write, no host command)
recheck: when S099-S110 land, re-open each row, replace `S1xx-pending` with its id, and re-run the § Local checks commands at the revision named in the round report; re-scan the synthetic fixtures at 1f7f995 and 9c54c56 with the tool copies whose sha256 is recorded there
surface: mado tripwire (`tools/mado-tripwire.py`, transcript scanner; not a host plane)

# Tripwire precision and the help/dry-run boundary — round 20

This note records what the mado tripwire can and cannot tell, the git and jj
forms whose help or dry-run output is not a write, and the fail-closed rule for
any isolation harness. It is a method note: it makes no claim about the host.
The tripwire reads transcript text; it never runs it. Fixture code is never
executed, and neither is any command a fixture names.

Two states are kept apart throughout. **Observed** means a command was run in
scratch or the tool was run on a synthetic transcript at a named revision.
**Target** means the round-20 contract (E1-E4 in the round declaration), which no
revision has been observed to satisfy yet.

## 1. What the tripwire can tell

Classes: `host_mutation`, `package_query`, `live_probe`, `tool_install`,
`vcs_write`. A row is a finding, not a verdict about execution.

| Question | Answer at 1f7f995 (red baseline) | Answer at 9c54c56 (pre-harm) |
|---|---|---|
| Does a bash `command` naming `pacman -Q` produce a row? | yes, `package_query`, `pacman:-Q` | yes |
| Does `BLOCK=frozenset(['pacman','-Q','hyprland'])` in an eval cell produce a row? | yes, `package_query`, `pacman:-Q`, **no `evidence` key** (observed) | no (`clean`, observed) |
| Does a literal `['pacman','-Q','hyprland']` handed to an unbound name `run_record(...)` produce a row? | yes, `package_query`, **no `evidence` key** (observed) | no (`clean`, observed) |
| Does a same-text `def show(argv): return str(argv)` called with that argv produce a row? | no (`clean`, observed): the body has no spawn | no |
| Does a same-text `def frozenset(argv)` whose body spawns, called with a literal argv, produce a row? | yes, `package_query`, unmarked (observed): the rebound name loses its exemption and the call's literal argv reaches the visible body's spawn | no (`clean`, observed; the spawn argument is non-literal inside the body, `unparsed_spawns=1`) |
| Does `git commit -m x` in an eval `subprocess.run([...])` produce a row? | yes, `vcs_write`, `git:commit` (observed) | `vcs_write` class does not exist at this revision (`counts` has no key) |

Reading the table:

- A row without an `evidence` key counts as **observed** under the counter rule.
  At 1f7f995 every row is unmarked, so the frozenset harm and the unbound-helper
  lead are indistinguishable from a bash command the seat typed.
- `clean` means no row in the covered forms. It never means no host command ran
  (see § 4).
- The 9c54c56 tool has no `vcs_write` class. Its `clean` for `git commit -n` is
  class absence, not a precision judgement. Do not read it as "git commit -n is
  safe to scan clean".

Target (E1): a literal argv handed to a callee whose body is **not** visible is a
`lead`, not `observed`. A visible helper whose body reaches a spawn is
`observed`. Lead rows stay in `findings` and exit 1, and the verdict carries
`lead_findings` next to `observed_findings`. Not yet observed at any revision.

## 2. git and jj: which forms are not writes

Forms the target (E4) must exempt. Each row was run in a scratch repository under
`/tmp` unless marked otherwise.

| Form | Observed effect (scratch) | Target treatment | Upstream statement |
|---|---|---|---|
| `git commit -h` | prints usage, rc=0 | no `vcs_write` row | S1xx-pending (git.c: `-h` dispatch) [INFERENCE] |
| `git help commit` | rc=0, no commit | no row | S1xx-pending (git.c: `help` dispatch) [INFERENCE] |
| `git --help push` | opens the man page through the pager; with `MANPAGER=cat` it printed `GIT-PUSH(1)` | no row; note it invokes a viewer | S1xx-pending (git.c) [INFERENCE] |
| `git commit --dry-run -m t` | history unchanged (2 commits before and after); rc=1 when nothing was staged | no row | S1xx-pending (git-commit: `--dry-run`) [INFERENCE] |
| `git add -n file` | prints `add 'file'`, rc=0; the file stays untracked (`?? nf`) | no row | S1xx-pending (git-add: `-n|--dry-run`) [INFERENCE] |
| `git push --dry-run origin main` | not run (no remote in scratch); the tripwire already flags the text | no row (target) | S1xx-pending (git-push: `-n|--dry-run`) [INFERENCE] |
| `git commit -n -m t` | **a real commit**: history grew 1 to 2 | **row**: `-n` is `--no-verify`, not dry-run | S1xx-pending (git-commit: `-n` is `--no-verify`) [INFERENCE] |
| `jj help git push` | prints help, rc=0; no `.jj` directory created in a plain directory | no row | S1xx-pending (jj help) [INFERENCE] |
| `jj git push --help` | prints help, rc=0; no `.jj` directory created | no row (target) | S1xx-pending (jj help: `-h|--help` as a flag) [INFERENCE] |

Rules the target must keep:

- `-m --help` is a commit message, not help. `--help` as an option's value is a
  write.
- A dry run followed by a real write in the same text is a write. The
  E4 carve-out covers the dry-run invocation only.
- `git commit -n` is a write. The `-n` letter means two different things by
  subcommand: `commit -n` = `--no-verify`; `add -n` and `push -n` = dry run.

Observed limit at 1f7f995: `git commit --dry-run -m t; git commit -m real` gives
**one** `vcs_write` row, named `git commit --dry-run -m t`, on line 1. The real
commit is not reported. `git commit -m a && git commit -m b` also gives one row,
naming `git commit -m a`. So one bash call yields one row, and the row names the
first match. A reader who looks only at the row sees the dry run and misses the
write. Target E4 keeps a dry run followed by a write as a write; the row for that
case must name the write, not the dry run. Not yet observed at any revision.

## 3. Python names and shlex

- `frozenset`, `callable`, `set`, `list`, and the other builtins are present in
  `builtins` (observed, Python 3.14.8). A builtin name is pure only while the text
  does not rebind it (E3).
- A rebinding `def frozenset(...)` loses the exemption. At 1f7f995 the rebound
  name with a spawn body is reported when called with a literal argv (observed);
  the rebound name with a non-spawn body is clean.
- `shlex.join(["git","commit","-m","a b"])` returns `git commit -m 'a b'`
  (observed). `shlex` is pure data here (E2). The tripwire's own limit is that
  `shlex` is not bash (see the tool docstring), so quoting that `shlex` accepts
  may still hide a command from the bash parser.
- A same-text helper whose body only formats its argv is clean at 1f7f995
  (observed). That is correct under E2 and must stay clean.
- An undefined callee handed a literal `['prog', ...]` argv is a **lead**
  under E1, not an observed run. At 1f7f995 it is an unmarked finding (observed).

## 4. What "clean" does not mean

The tool docstring lists the gaps. Those that matter for a precision claim:

- Detection is after the fact. It is not interception, sandboxing or repair.
- A transcript that writes a script and then runs it is not analysed as the
  script's contents.
- Aliases, shell functions defined in one text and called in another, and
  `python -c` bodies are not analysed.
- Non-literal spawn arguments are counted as `unparsed_spawns`, not as findings.
- Issued is not executed. A refused call and a successful call both count.

A verdict of `clean` therefore means no finding in the covered forms, and nothing
more. Pair it with an independent window (for example the package log) when the
question is whether a host command ran.

## 5. Isolation harnesses fail closed

Round 19 routed a fail-open harness. Its shape, as recorded in the round-19
closure (`corpus/lessons/round-19-verifier-spotcheck.md`, § Incidents):

```text
unshare --user --map-current-user --mount --propagation private \
  /tmp/sgp/inns.sh bash -c '... /usr/bin/hyprctl probe; echo rc=$?'
```

The setup was a mount step chained with `&&` before the payload. When the setup
failed, the payload still ran. The closure recorded a real probe reaching the
host command.

Local reproduction, canary only (observed, no `unshare`, no host binary):

```text
bash -c 'set -e; false && echo setup-ok; echo payload > /tmp/.../canary-open'
  -> payload written (canary exists), rc=0
```

Why: under `set -e`, bash does not exit when a failing command is a non-final
element of an `&&` or `||` list, and a function called in a `||` context has
errexit suppressed for its body (observed: `inner-after` printed after a failing
`false` inside `f || ...`). `set -e` therefore does not protect a chain that
continues on a setup failure. [INFERENCE] for the exact bash-manual wording,
which lands with S1xx-pending (bash manual: errexit).

Fail-closed form (observed in the same scratch):

```text
bash -c 'set -e; if ! false; then echo "setup failed: abort" >&2; exit 1; fi; echo payload > /tmp/.../canary-closed'
  -> abort, canary absent, rc=1
bash -c 'set -e; false || { echo abort >&2; exit 1; }; echo payload > /tmp/.../canary-closed2'
  -> abort, canary absent, rc=1
```

Rules:

1. Setup and payload are separate steps. The payload line is reachable only
   through an explicit `if ! setup; then exit 1; fi` or `setup || { exit 1; }`.
2. A setup check must test the state it claims. Testing that a path exists is
   not a mount check; confirm the mount, or abort.
3. Payloads are canary writes into `/tmp`. A harness never invokes a host
   binary as its payload while the host pause binds.
4. `set -e` is not a fail-closed mechanism on its own. Use explicit guards.
5. Scripts written then run are invisible to the scanner. A harness that is
   tripwired must be named in the report as a written script, with its contents
   read as data.

Not run here: `unshare` itself. Its exit status when the user namespace or the
mount is unavailable is [UNK] until the harness is tested with a canary.

## Local checks

All were run in `/tmp/mr20-scribe` (scratch), read-only on the lane:

- Tool copies: `git show 9c54c56:tools/mado-tripwire.py` and `git show
  1f7f995:tools/mado-tripwire.py` extracted to `/tmp`; sha256 prefixes `c1ae45a7…`
  (9c54c56) and `367be947…` (1f7f995), matching the round-19 closure.
- Synthetic transcripts: one JSON envelope per file, the frozenset, unbound-helper,
  same-text helper, rebound-builtin, eval `subprocess.run`, and bash git/jj forms
  above. Scanned with `python3 -I <tool> --scan <file>`. The fixture text was
  never executed.
- Versions: git 2.56.0, jj 0.45.1, bash 5.3.20, Python 3.14.8, util-linux
  unshare 2.42.4 (present, not run).

## Limits

- No S1xx row is opened. Every upstream statement is [INFERENCE] until its source
  lands and is re-read.
- Target behaviour (E1-E4) is not observed at any revision; only 1f7f995 and
  9c54c56 behaviour is recorded here.
- The synthetic corpus is small. It does not measure precision across the lane.
- `git push --dry-run` and the `git --help <sub>` man path were not run against a
  remote or a real pager.
- `unshare` was not run. The fail-closed rules are tested with canaries only.
