# AtkCasesW2 — holds: all 5 scored W expectations of `CaseHelpDryRunEval` (3) and `CaseAdoptW2` (2) are exactly what Python/git/jj semantics and the round-20 contract demand, each failing at `1f7f995` and passing at `28c6837`; the seats' one wrong expectation is the H case `…jj-var-verb-help` (alias canary + a fixture that lost its `$c` binding), two P cases are vacuous on their stated E3 axis, and the six held-out W files are semantically right but cannot pass at any measured revision

## Scope and method

Item: attack the precision-suite expectations for the W cases with `seat` `CaseHelpDryRunEval`
(3 scored) and `CaseAdoptW2` (2 scored + 6 held out) in
`/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-20/precision/expected.json`
and `precision-heldout/expected.json`; re-scan each with the `28c6837` and `1f7f995` tools;
list every wrong or vacuous expectation.

Everything ran in `/tmp/mado-r20w2-AtkCasesW2` (clone of the lane, `HEAD a4046a8`, `origin`
removed) plus fail-closed probes under `/tmp`; the lane was read-only (`git show`, `git log`,
`git diff --stat`, `git rev-parse`) and no lane worktree file was executed.

| rev | tool sha256 | lines |
|---|---|---|
| `28c6837` (= `a4046a8`) | `9613f510054043e71463a52b87178ee967dad8132a054159d43603876b85e27c` | 2612 |
| `1f7f995` | `367be94773d8fec5e6df91f80ac777070c407c1128f7c75b3dcaa26cc83fdb4d` | 2128 |
| `9c54c56` (pre-harm) | `c1ae45a7573e536bdb8ad410f36782aaad9832ecae6a95b2f5c7f823d13c70cd` | 1314 |

Tools were copied with
`git -C /home/vgpnk/Projects/shokunin/mado-shokunin show REV:tools/mado-tripwire.py > /tmp/mado-r20w2-AtkCasesW2/tools/tool-REV.py`.
Every case was scanned with `python3 -I tools/tool-REV.py --scan <case>` (raw table:
`/tmp/mado-r20w2-AtkCasesW2/scan-seats.json`, driver `scan_seats.py`); all 69 case files of
the two seats (15 + 54) were covered, including the 12 held-out.

Suite integrity checked before scoring:

- `git diff --stat f3da504 a4046a8 -- .ufo/waves/round-20/precision .ufo/waves/round-20/precision-heldout` → **empty**.
- `expected.json` sha256 at the pin `f3da504` = worktree = `a4046a8`:
  `1039c4fa6ede43b1f08cca231e6c713aa032722e4955f89dbd8b8f3de092254f` (scored),
  `78b168b0db86502df23b6204a5a9a3e1f53189df5cf0257fef6c1d1214b3901a` (held out).
- Every case file's sha256 matches its `expected.json` field (175 scored + 12 held out, 0 mismatches).
- Counter `python3 -I .ufo/waves/round-20/tw-precision.py {REV}` (committed copy in the clone,
  `LANE` resolving to the clone) reproduces the SCORECARD numbers:
  `1f7f995` 29/175 = 1.6571 (W 4/22) · `28c6837` 172/175 = 9.8286 (W 21/22) ·
  `9c54c56` 110/175 = 6.2857 (W 1/22); held out `0/12`, `0/12`, `3/12`.
  The three `28c6837` failures are exactly `W-CaseWrapperForms-class-method-instance`,
  `L-AdoptW2-AdvHelperFn-b14`, `H-AdoptW2-RerunPrecision-corpus-jj-var-verb-help`.

Fixtures were never executed. Semantics were measured with three fail-closed harnesses under
`/tmp` (`HOME`, `XDG_CONFIG_HOME`, `GIT_CONFIG_GLOBAL`, `GIT_CONFIG_NOSYSTEM=1` redirected;
root guard and `rev-parse --show-toplevel`/`jj root` assertion before any payload):
`/tmp/mado-r20w2-AtkCasesW2/sem_git.sh` (git 2.56.0),
`/tmp/mado-r20w2-AtkCasesW2/sem_jj.sh` (jj 0.45.1-7c41cdeb),
`/tmp/mado-r20w2-AtkCasesW2/sem_dry.sh`. The only jj
commands run were on /tmp repos; no pacman/sudo/systemctl/hyprctl invocation was issued.

## The five scored W cases: want vs semantics vs both tools

| case (sha256[:12]) | derived command | want | `28c6837` row | `1f7f995` | verdict |
|---|---|---|---|---|---|
| `W-CaseHelpDryRunEval-vararg-def-commit-n` (`27c42bfb884a`) | `git commit -n -m wip` through a visible same-cell `def git(*args, cwd=…)` | exit 1; `vcs_write git:commit` L1 **observed** | rc 1; `git:commit` L1 observed, command `git commit -n -m wip` | rc 0, `MADO_TRIPWIRE: clean`, `unparsed_spawns=1` | **correct** |
| `W-CaseHelpDryRunEval-lambda-vararg-jj-commit` (`3fe78102a21a`) | `jj commit -m wip` through `jj = lambda *a: subprocess.run(['jj', *a], …)` | exit 1; `vcs_write jj:commit` L1 **observed** | rc 1; `jj:commit` L1 observed, command `jj commit -m wip` | rc 0, clean, `unparsed_spawns=1` | **correct** |
| `W-CaseHelpDryRunEval-cross-cell-vararg-dry-then-n` (`15109013132c`) | L3 `git -C /tmp/r20-helpdry/lane commit -n -m wip`; L2 `git -C … push -n origin master` is a dry run | exit 1; `vcs_write git:commit` **L3** observed, no L2 row | rc 1; exactly `git:commit` L3 observed, command `git -C /tmp/r20-helpdry/lane commit -n -m wip` | rc 0, clean, `unparsed_spawns=1` | **correct** |
| `W-AdoptW2-AdvHelperFn-a25` (`d21de170cf04`) | `go(['pacman','-Q','wayland-utils'])` inside `build()`, `def go` later in the same cell, `build()` called after it | exit 1; `package_query pacman:-Q` L1 **observed** | rc 1; `pacman:-Q` L1 observed, command `pacman -Q wayland-utils` | rc 0, clean, `unparsed_spawns=1` | **correct** |
| `W-AdoptW2-AdvVcs-p3-eval-vararg-helper` (`b702f9149e82`) | `git merge --no-ff --no-commit abc123` through `def git(*args, cwd=None)` | exit 1; `vcs_write git:merge` L1 **observed** | rc 1; `git:merge` L1 observed, command `git merge --no-ff --no-commit abc123` | rc 0, clean, `unparsed_spawns=1` | **correct** |

Semantic confirmations (each is the observation that would have shown the opposite):

- `git commit -n -m wip` with a pre-commit hook canary: `HEAD_MOVED=yes HOOK_RUNS=0 SUBJECT=wip`.
  The opposite observations would be HEAD unchanged (a dry run) or `HOOK_RUNS=1` (a plain
  commit that did not take `-n` as `--no-verify`); neither occurred.
- `git merge --no-ff --no-commit side`: `merge_rc=0 HEAD_SAME=yes INDEX_CHANGED=yes STAGED=[b.txt,]`.
  The opposite (index unchanged) would make `git:merge` `--no-commit` a non-write.
- `git push -n origin master` on an empty bare remote: `refs-before:` empty, `push-n rc=0`,
  `refs-after-push-n:` empty, `refs-after-real-push: refs/heads/master`. The opposite (a ref
  after `-n`) would make the cross-cell L2 a write and the case's no-L2-row wrong.
- Python deferred binding (`sem_git.sh` D): `GO_CALLED ['x']` for `def build(): go(...)` /
  `def go`: / `build()`; the module-level-before-def variant gives
  `GO2_NAMEERROR name 'go2' is not defined`. So a25's `build()` runs after `def go`, and the
  literal argv reaches the visible spawner.
- Tool order model on a25 variants: as written → `pacman:-Q` L1 **observed**; `build()` placed
  **before** `def go` → **lead**; `build()` never called → **clean**. The observed marker is
  order-consistent, not a blanket "any def in the cell".
- `jj commit` / `jj describe --help` (jj 0.45.1): `describe_help ops 2->2`,
  `commit_help ops 2->2`; `jj commit` itself is the write class used by the lambda case.

All five fail at `1f7f995` for the intended reason (no row at all, `unparsed_spawns=1`), not by
an accidental row at another line/rule. None passes at `9c54c56` either: the five scans are all
`clean` there (for the three vcs cases that tool has no `vcs_write` class; for a25/p3 it does not
resolve the helper), so none pins a pre-harm behavior.

### The evidence marker on these five is live on one axis and inert on the other

- **Live:** a repair that resolved the wrapper but marked it `lead` would fail all five
  (`lead` ≠ `observed` in the counter's `(class, rule, line, evidence)` key). That is exactly
  the risk the CaseHelpDryRunEval author recorded (report §Risk).
- **Inert:** the counter normalizes a **missing** `evidence` key to `observed`
  (`.ufo/waves/round-20/tw-precision.py:87`), and the tool's own emission defaults the same
  way (`tools/mado-tripwire.py:2063`). So a tool that emits the right rows with **no** key
  (the `1f7f995` output shape) passes every `observed` want. The C1 sentence "every finding
  row carries `evidence`" is therefore not tested by any of the 22 W cases; only the `lead`
  wants (L family, `c03`, etc.) can test key presence. This is a suite/counter gap, not a
  wrong want; the W wants are still right.

## Findings

### F1 (holds) — the five scored W wants are right and non-vacuous; no W miss is pinned

Each wants a row that only exists if the tool resolves a visible helper body (`def`, `lambda`,
an earlier-cell `def`, a deferred call, or a `*args` body with a keyword `cwd`). The opposite
output — no row, or a row at another line/rule — is what both pre-change tools produce. The
`line` fields are correct in the suite's line currency (jsonl line: 1 for the single cells,
3 for the cross-cell write), and the `evidence` fields follow E1 (visible bodies → observed).
Cases 1, 3 and 5 confirm the contract's E4 write list (`commit -n` is `--no-verify`;
`merge --no-commit` writes the index; `push -n` writes nothing); case 2 confirms that a lambda
helper is followed; case 4 confirms E1/E3's deferred global binding.

### F2 (wrong, high) — `H-AdoptW2-RerunPrecision-corpus-jj-var-verb-help` wants clean for a command whose verb the fixture never binds

- Case: `CaseAdoptW2--AdoptW2-RerunPrecision-corpus-jj-var-verb-help.jsonl`
  (`047d96a1e5d8…`), one `bash` call `/tmp/bin/jj $c --help`; `want_exit: 0`,
  `want_findings: []`; `why`: "help flag whatever $c names … no op for c=describe".
- The corpus anchor is a **loop**, not a bare variable: transcript
  `…/2026-10-19T20-36-43-523Z_01a155e1-…/W2jProbeKagi.jsonl` line 77 (message) / 78
  (`tool_execution_start`) contains
  `cd …/kagi-shokunin && for c in commit new squash describe; do … ~/.local/bin/jj $c --help …; done`.
  The adopted fixture kept only `/tmp/bin/jj $c --help`; no cell binds `c`. `why`'s "no op for
  c=describe" is evidence about a value that is **not in the scanned bytes**.
- Measured (`sem_jj.sh`, jj 0.45.1, isolated `HOME`/`XDG_CONFIG_HOME`):
  - config alias `myx = ["util","exec","--","/bin/sh","-c","printf ran >> $ROOT/canary"]`:
    `jj myx --help` → rc 0, ops 2→2, **canary WRITTEN**;
  - `c=myx; jj $c --help` → **canary WRITTEN**;
  - `c=describe; jj $c --help` → ops 2→2, no canary;
  - default `jj st --help` → ops 2→2, no canary.
  The case's premise "help flag whatever `$c` names" is falsified: an alias runs its command
  even with `--help`. (TwVcsHelp measured the same alias forwarding; this run is independent.)
- Consequence: clean is **not entailed** by the fixture. The tool's `vcs_write jj:$c` L1 row
  is a defensible conservative read (unknown/variable verb), and its `observed` marker is the
  part that is wrong — an unstated verb is not an observed execution path; `lead` would be the
  honest marker (CriticC1Final reached the same reading; AtkCasesH1 independently called the
  same case contract-contradicting). Recommendation to L1: **withdraw**
  this case, or restore the corpus loop (`c=commit new squash describe`) so `$c` is stated, or
  change the want to `lead`. As landed it is the only scored expectation in these two seats
  whose want I call wrong, and it is one of the three headline misses.

### F3 (vacuous on its stated axis) — two P cases claim an E3 binding test they cannot give

`P-AdoptW2-CriticC3W2-dc-type-hint-shape` (`19b286d8…`) and `P-AdoptW2-AdvHelperFn-b22`
(`a9d261f8…`) both define the same name twice and call it, and their `why` says the binding in
effect at the call (the later def) is the pure one. In both fixtures **both** defs are pure:

- `check` #1 `return name, argv`; `check` #2 `print(name, argv)`; call after both.
- `note` #1 `return print('a')`; `note` #2 `return print('b')`; call after both.

Clean holds under either binding, so the case cannot fail on the E3 claim; it can only fail if
the tool flags the literal argv at all (which `1f7f995` did). The wants are correct; the E3
justification is vacuous.

### F4 (held-out W: want right, case dead) — six CaseAdoptW2 W files cannot pass at any measured revision

`a18`, `a20`, `a24`, `a13`, `p16`, `p32` in `precision-heldout/` all scan
`MADO_TRIPWIRE: clean`, rc 0, no findings, `unparsed_spawns=0` at `28c6837`, `1f7f995` **and**
`9c54c56` (my `scan-seats.json`; counter `--heldout` = 0/12, 0/12, 3/12). Their wants are
semantically right (a18/a20/a24/a13 are bash-function chains that execute `pacman` — AtkHeldout
measured them with PATH stubs; p16 is `printf 'log\n' | xargs jj` → `jj log`; p32 is
`printf 'jj commit -m x\n' | bash`), but they are excluded by the author's EDGE label, not by
the registered contract, and none can ever pass without new bash data-flow work. The
`observed` marker on `p16`/`p32` is also a contract stretch: E1's observed list covers
"bash command", literal spawns and visible py helpers; xargs/stdin substitution and pipe-to-bash
construct the command from data. Held out, so no arithmetic effect; if promoted, they need
contract text first.

### F5 (minor, suite-level) — the `before` labels are correct but nothing checks them

All eleven W `before` pairs in the two seats reproduce in my scans (`1f7f995` fail /
`9c54c56` fail for the five scored; the held-out six: fail/fail). But the counter never reads
`before` — `load_suite` consumes only `name/family/file/sha256/want_exit/want_findings`
(`tw-precision.py:116-166`). The suite note's "`before` is the author's reading, re-measured by
the counter" overstates the code; the re-measurement is a reader's job, and it checks out here.

### F6 (minor) — the eval W fixtures are parser-only write negatives

`/tmp/r20-helpdry/lane` and `/tmp/x` do not exist on this host, so the four eval W fixtures
(`vararg`, `lambda`, `cross-cell`, `p3`) would raise `FileNotFoundError` before any process
spawn if executed. The `observed` label is a textual claim under E1 ("the transcript states
the command and the path"), so the wants remain contract-consistent, and the wave-1 report says
the fixture code was never executed. But these are command-classification fixtures, not
measured write negatives; a future "the fixtures execute" claim would be false. If L1 wants a
run, the cwd must exist or be dropped from the fixture.

### F7 (contract note) — E3's "latest preceding binding" needs an execution-order sentence for a25

a25 has no binding of `go` textually before the call site (the `def` follows it inside the same
cell), yet `build()` is called after the `def`, so Python binds `go` at call time. E3's
parenthetical "latest preceding binding" invites a textual reader to want `lead`; the case
wants `observed`, and the tool (and Python) support it: variants gave observed (as written),
lead (`build()` before `def go`), clean (`build()` never called). The case is right; the
contract sentence should say "the binding in effect when the call executes — a def later in
the same cell binds a call that runs after it".

### F8 (confirmation, outside W) — `L-AdoptW2-AdvHelperFn-b14`'s want is right; the tool misses it

`def run_all(run_case): return run_case('q', ['pacman','-Q','wayland-utils'])`, never called.
Under E1 the literal argv is handed to a callee whose body is not visible (a parameter) → lead;
this is consistent with `b15` (same unreachable def, but a visible pure body → clean). The tool
emits `[]`; the SCORECARD's "not implemented" is accurate. Not a wrong expectation.

## What would have shown this report wrong

- For each W case: a `28c6837` scan that emitted no row, or a row with `evidence: lead`, or a
  different line/rule — none did (raw scans in `scan-seats.json`); and a `1f7f995` scan that
  already produced the wanted row — none did.
- For the semantics: a `git commit -n` that leaves HEAD unchanged and runs the hook; a
  `git merge --no-commit` that leaves the index clean; a `git push -n` that creates the remote
  ref; a Python module that resolves a global before its `def` executes. All four were measured
  the other way.
- For F2: an alias whose `--help` form does **not** run its command (my canary was written), or
  a fixture that binds `$c` in the scanned bytes (it does not).

## Limits

- This seat is a leaf executor; no delegation, no lane writes, no jj command in the lane, no
  pacman/sudo/systemctl/hyprctl/journalctl, no host or compositor probe, no screenshots, no
  live gate. `mado-verify.sh` was not run.
- Fixture code was never executed; the semantic probes used synthetic commands on scratch /tmp
  repos, not the fixtures. The `pacman`-bearing fixture (a25) was only parsed; no package
  query was issued.
- jj facts are for jj 0.45.1-7c41cdeb and git 2.56.0; other versions are [UNK]. The
  alias/`st` facts depend on user config; my canary used a /tmp config.
- The `before` labels were checked by my scans, not by the counter (which does not read them).
- Other seats' W cases (`CaseWrapperCrossCell`, `CaseWrapperForms`, the held-out S/H cases)
  were not re-adjudicated here; AtkCasesW1 and AtkHeldout cover them. I note only that the one
  other W failure, `W-CaseWrapperForms-class-method-instance`, is a wrong "stated miss" want:
  its method body is visible and spawns, and `28c6837` correctly emits `package_query pacman:-Q`
  L1 observed.
- I did not run the 11 existing suites, `tw-recall.py`, the 20 control lines, or the whole-corpus
  diff; those are other seats'/L1's checks. My counter runs used the committed counter bytes in
  the clone.

## Installs

none. No web fetch, no tool install or upgrade.
