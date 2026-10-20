# AtkCasesH2 — partly falsified: all 24 H expectations in the two named seats are semantically correct and pass at `28c6837`, but three are vacuous for the axis their `why` names (they pass at `1f7f995` with the row carried by the dry-run command), and the suite has no negative for combined short dry-run flags, which the tip tool still flags.

Seat: `MadoR20.AtkCasesH2`. Target: the 24 H cases authored by `CaseDryRunBash` (12) and `CaseHelpDryRunEval` (12) in
`.ufo/waves/round-20/precision/expected.json`, plus the 3 W cases the same seats landed (checked for context, not scored as H).
Everything below was measured in `/tmp`; the lane checkout was read-only git only and no jj command was run in it.

## Method

- Clone: `git clone -q /home/vgpnk/Projects/shokunin/mado-shokunin /tmp/mado-r20w2-AtkCasesH2`
  (`HEAD a4046a8216080d4004de3f268c62cf142095ac07`), origin removed.
- Tool bytes, from the lane object store (never executed from the lane):
  - `1f7f995:tools/mado-tripwire.py` sha256 `367be94773d8fec5e6df91f80ac777070c407c1128f7c75b3dcaa26cc83fdb4d`
  - `9c54c56:tools/mado-tripwire.py` sha256 `c1ae45a7573e536bdb8ad410f36782aaad9832ecae6a95b2f5c7f823d13c70cd`
  - `28c6837:tools/mado-tripwire.py` sha256 `9613f510054043e71463a52b87178ee967dad8132a054159d43603876b85e27c` (= lane `tools/mado-tripwire.py`)
- Every case scanned with both required revisions: `python3 -I tool-<rev>.py --scan case.jsonl`, cwd = a temp dir, one fresh temp dir per case
  (same invocation the counter uses). Fixture bytes only; nothing in a fixture was executed.
- Counter, from the clone: `python3 -I .ufo/waves/round-20/tw-precision.py REV` (lane copy gives byte-identical per-case verdicts).
- Semantics probes in `/tmp` with `HOME=/tmp/r20h2-home`, `GIT_CONFIG_NOSYSTEM=1`, `GIT_AUTHOR/COMMITTER` set; git 2.56.0, jj 0.45.1-7c41cdeb.
  jj op state read from `.jj/repo/op_heads/heads/` on the filesystem, never via a jj command that would itself snapshot
  (this trap is real: `jj op log` snapshots, which hid the first measurement of case 8 until I read the op-head files directly).

## Headline reproduction (author claims confirmed)

| reading | command | result |
|---|---|---|
| C1 after | `python3 -I .ufo/waves/round-20/tw-precision.py 28c6837` | score `9.8286`, 172/175; fails `W-CaseWrapperForms-class-method-instance`, `L-AdoptW2-AdvHelperFn-b14`, `H-AdoptW2-RerunPrecision-corpus-jj-var-verb-help` (all outside these two seats) |
| C1 baseline | `… 1f7f995` | score `1.6571`, 29/175; families P 7/66, S 2/17, W 4/22, H 15/52, L 1/18 |
| C1 pre-harm | `… 9c54c56` | score `6.2857`, 110/175; families P 66/66, S 7/17, W 1/22, H 35/52, L 1/18 |
| these seats at `28c6837` | counter `cases[]` | CaseDryRunBash 12/12, CaseHelpDryRunEval 15/15 (12 H + 3 W) |
| these seats at `1f7f995` | counter `cases[]` | CaseDryRunBash H 5/12, CaseHelpDryRunEval H 2/12, W 0/3 |
| these seats at `9c54c56` | counter `cases[]` | CaseDryRunBash H 7/12, CaseHelpDryRunEval H 7/12, W 0/3 |
| `before` metadata | per-case compare of `before.{1f7f995,9c54c56}` with measured `pass` | 0/175 mismatches |
| held-out | `… 1f7f995 --heldout` / `… 28c6837 --heldout` | 0/12 both, as claimed |
| suite immutability | `git diff f3da504 a4046a8 -- .ufo/waves/round-20/precision/` | empty; `expected.json` sha256 `1039c4fa…` at `f3da504` = worktree |
| counter immutability | `git diff f3da504 28c6837 -- .ufo/waves/round-20/tw-precision.py` | one line only: `SUITE_PIN = None` → `"f3da504…"` |

So the counter change at the repair commit is only the pin, not scoring logic. [INFERENCE] Nothing in the measurement pipeline is
self-serving; the defects below are in what the cases *can* discriminate, not in arithmetic.

## Per-case verdicts (24 H cases)

`PASS`/`fail` below is the counter verdict. "Semantics" is my own `/tmp` measurement of the command's real effect, not a re-run of the fixture.
`E4` = the round-20 contract paragraph (`SCORECARD.md:1250-1253`) and its amendment (`SCORECARD.md:1311-1316`).

### CaseDryRunBash (12 H)

| case | command | want | 28c | 1f7 | semantics measured | verdict |
|---|---|---|---|---|---|---|
| `H-CaseDryRunBash-commit-dry-run` | `git commit --dry-run -m x` | 0, [] | PASS | fail | HEAD/refs/staged entries unchanged, 0 hook runs (`pre-commit`/`commit-msg` canaries); writes one loose tree + `.git/index` cache-tree | correct under E4 (class-scoped non-write; note N2) |
| `H-CaseDryRunBash-add-n` | `git add -n .` | 0, [] | PASS | fail | index sha256 identical before/after, no new objects | correct |
| `H-CaseDryRunBash-add-dry-run` | `git add --dry-run .` | 0, [] | PASS | fail | index sha256 identical | correct |
| `H-CaseDryRunBash-push-n-origin-master` | `git push -n origin master` | 0, [] | PASS | fail | bare remote `refs/heads/master` and local tracking refs unchanged (pre-push hook does run; note N3) | correct |
| `H-CaseDryRunBash-push-dry-run` | `git push --dry-run` | 0, [] | PASS | fail | remote + tracking unchanged | correct |
| `H-CaseDryRunBash-push-trailing-dry-run` | `git push origin master --dry-run` | 0, [] | PASS | fail | git accepts the flag after the refspec; remote + tracking unchanged | correct |
| `H-CaseDryRunBash-jj-push-dry-run-ignore-wc` | `jj --ignore-working-copy git push --dry-run` | 0, [] | PASS | fail | dirty wc; op head and whole `.jj`+`.git` state hash unchanged (`47ea49a540cf7e45` before/after) | correct |
| `H-CaseDryRunBash-jj-push-dry-run-snapshots` | `jj git push --dry-run` | 1, `vcs_write jj:git 1 observed` | PASS | PASS | dirty wc: op head `f2127fb8…`→`ce4ce2a9…`; clean wc: no op | correct per amended E4 (state-conditional; note N1) |
| `H-CaseDryRunBash-commit-n-no-verify` | `git commit -n -m x` | 1, `git:commit 1 observed` | PASS | PASS | commit created (`HEAD` subject `x`), 0 hook runs; a normal `git commit -m` runs the hook once | correct |
| `H-CaseDryRunBash-add-n-then-add` | `git add -n . && git add .` | 1, `git:add 1 observed` | PASS | **PASS** | 28c row command `git add .`; 1f7 row command `git add -n .` — **the dry run** — and the counter still passes | **VACUOUS (D1)** |
| `H-CaseDryRunBash-push-dry-run-then-push` | `git push --dry-run; git push` | 1, `git:push 1 observed` | PASS | **PASS** | 28c row command `git push`; 1f7 row command `git push --dry-run` — counter still passes | **VACUOUS (D2)** |
| `H-CaseDryRunBash-commit-msg-value-dry-run` | `git commit -m --dry-run` | 1, `git:commit 1 observed` | PASS | PASS | commit created with subject `--dry-run` | correct |

### CaseHelpDryRunEval (12 H)

| case | command (cell) | want | 28c | 1f7 | semantics measured | verdict |
|---|---|---|---|---|---|---|
| `H-CaseHelpDryRunEval-run-add-n` | `subprocess.run(['git','add','-n','.'])` | 0, [] | PASS | fail | index/objects unchanged | correct |
| `H-CaseHelpDryRunEval-bang-jj-help-flags` | `!jj st --help` / `!jj describe -h` | 0, [] | PASS | fail | dirty wc; op head unchanged for both; control `jj st` changes it | correct |
| `H-CaseHelpDryRunEval-check-output-help-before-sub` | `check_output(['git','--help','push'])`, `(['git','-C',DIR,'--help','commit'])` | 0, [] | PASS | fail | both print the man page, rc 0, `.git` unchanged | correct |
| `H-CaseHelpDryRunEval-popen-push-dry-runs` | `Popen(['git','push','-n','origin','master'])`, `Popen([…'--dry-run'])` | 0, [] | PASS | fail | remote + tracking unchanged | correct |
| `H-CaseHelpDryRunEval-helper-commit-h-late-help` | visible `def sh`; `sh(['git','commit','-h'])`, `sh(['git','commit','-m','probe','--help'])` | 0, [] | PASS | fail | both print usage, rc 0; HEAD unchanged, no `.git` change | correct |
| `H-CaseHelpDryRunEval-tool-bash-jj-commit-help` | `await tool.bash({'command':'cd … && jj commit --help'})` | 0, [] | PASS | fail | dirty wc; op head unchanged | correct |
| `H-CaseHelpDryRunEval-pct-bash-dry-runs` | `%%bash`: add `--dry-run`; commit `--dry-run -m probe`; `jj describe --help` | 0, [] | PASS | fail | all three verified individually above | correct |
| `H-CaseHelpDryRunEval-n-two-meanings` | L1 `add -n`; L2 `git commit -n -m wip` | 1, `git:commit L2 observed` | PASS | fail | L1 writes nothing; L2 commits, hooks skipped | correct |
| `H-CaseHelpDryRunEval-help-flag-vs-value` | same cell: `!jj describe --help`; `git commit -m --help` | 1, `git:commit L1 observed` | PASS | fail | jj prints help (no op); git commits with subject `--help` | correct |
| `H-CaseHelpDryRunEval-jj-push-dry-run-snapshot` | L1 `jj --ignore-working-copy git push --dry-run`; L2 `jj git push --dry-run` | 1, `jj:git L2 observed` | PASS | fail | L1 no state change; L2 op head change (dirty wc) | correct |
| `H-CaseHelpDryRunEval-ctl-dry-then-push-same-cell` | one cell: `git push -n origin master`; `git push origin master` | 1, `git:push L1 observed` | PASS | **PASS** | 28c row command `git push origin master`; 1f7 row command `git push -n origin master` — counter still passes | **VACUOUS for attribution (D3)**; valid cell-suppression control |
| `H-CaseHelpDryRunEval-ctl-commit-m-dry-run-value` | `git commit -m --dry-run` | 1, `git:commit L1 observed` | PASS | PASS | commit created with subject `--dry-run` | correct |

Context only (not H): `W-CaseHelpDryRunEval-vararg-def-commit-n`, `-lambda-vararg-jj-commit`, `-cross-cell-vararg-dry-then-n`
all pass at `28c6837`; their `observed` rows are literal visible-body spawns (`git commit -n` / `jj commit`), which I verified are
real writes, so their expectations are correct too.

## Defects

Defect fixtures (sha256, from `expected.json`, verified by the counter's digest check):
`add-n-then-add` `dc92860c85a5a7288f7a7f7b8fabfd3185a25893396818a1a1fd2bcec647f214`,
`push-dry-run-then-push` `088aabf32425c01896ba6d469c179e2dd6113509bbcacf82e6ccfb59ff6990da`,
`ctl-dry-then-push-same-cell` `e810515de626022a72feea188d6169524c7d7ba65917f17360f08db90a965eb1`.

### D1 `H-CaseDryRunBash-add-n-then-add` — vacuous for the dry-run/real-write distinction
`why` says: "A dry run followed by a real add in the same text: exactly one git:add row (the real one)." (`.ufo/waves/round-20/precision/expected.json`, case `H-CaseDryRunBash-add-n-then-add`).

Measured at the baseline revision named in `before`:

```
$ python3 -I tool-1f7.py --scan case.jsonl      # case = precision/CaseDryRunBash--add-n-then-add.jsonl
rc 1
{"findings": [{"argv0": "git", "class": "vcs_write", "command": "git add -n .", "line": 1, "rule": "git:add", ...}]}
```

One `git:add` row at line 1 — **from the dry run** — and the counter calls the case `pass` at `1f7f995`
(`before: {"1f7f995": "pass"}`; my counter run reproduces it). The comparison tuple is only
`(class, rule, line, evidence)` (`tw-precision.py:98-100`, used at `:195`), so the case cannot see that the retained command is the wrong one.
The 1f7 keep-first dedup is `key = (cls, rule)` (`tool-1f7.py:1592-1594`); the tip key is `(cls, rule, evidence)` (`tool-28c.py:2064`).

Mutant proof: I disabled the per-segment add dry-run exemption in the tip tool (`git_prints_or_simulates` returns `False` for `add`,
`/tmp/mado-r20w2-AtkCasesH2/M-add.py`) — this is precisely the error the case exists to bound — and the case still PASSes
(the dedup collapses `git add -n .` + `git add .` to one row). It fails only under cell-level suppression (`M-cell-suppress`) or under
the author's own post-dedup exemption mutant m2. So it tests "a row survives suppression", not "the row is the real add".

Fix (no schema change): put the dry run and the real add in two JSONL messages and expect the row on line 2.
Then `M-add` fails the case (two rows: line 1 and line 2) and 1f7 fails it (line 1 only).

### D2 `H-CaseDryRunBash-push-dry-run-then-push` — same shape for push
`why`: "A dry run followed by a real push in the same text: exactly one git:push row (the real one)."

```
$ python3 -I tool-1f7.py --scan case.jsonl      # precision/CaseDryRunBash--push-dry-run-then-push.jsonl
rc 1
{"findings": [{"command": "git push --dry-run", "rule": "git:push", "line": 1, ...}]}
```

Baseline counter: `pass`. Tip: `command: "git push"`. Disabling the push dry-run exemption (`M-push`) leaves the case PASSing
(same dedup collapse), so it cannot fail for the reason stated. Same line-split fix.

### D3 `H-CaseHelpDryRunEval-ctl-dry-then-push-same-cell` — row-existence control, not an attribution test
`why`: "control: a dry run followed by a real write in the same text still writes (E4); guards against cell-level suppression."

```
$ python3 -I tool-1f7.py --scan case.jsonl      # precision/CaseHelpDryRunEval--ctl-dry-then-push-same-cell.jsonl
rc 1
{"findings": [{"command": "git push -n origin master", "rule": "git:push", "line": 1, ...}]}
```

Baseline counter: `pass`; the retained row is the dry run. Tip: `command: "git push origin master"`.
Because both invocations are in one cell/line, no line-split can separate them; with the current tuple the case can only ever
assert "some git:push row exists". It does guard cell-level suppression (my `M-cell-suppress2`: whole-cell suppression when the cell text
contains a dry token → `rc 0, findings []` → the case fails), and it does kill the author's post-dedup-drop mutant m2. It cannot
distinguish "real push detected" from "dry run flagged", which is the first half of its `why`. The author's own report states the
1f7 row is `git push -n origin master` (`.ufo/waves/round-20/w1/reports/CaseHelpDryRunEval.md`, "Controls at 1f7f995").

Fix options: (a) extend the case schema/counter to compare `command` (or `argv0`) — then this case fails at 1f7 and passes at
`28c6837`, and no case file changes; (b) keep a same-cell cell-suppression control but do not claim real-write attribution in `why`.

### Impact of D1–D3 on the reported numbers
Each of the three pins a known miss: its expected `(class, rule, line, evidence)` tuple is exactly the tuple the baseline produces
for the wrongly-flagged dry run, so a green at `1f7f995` is indistinguishable from the defect. They do not change `28c6837`
(172/175; H 51/52 — all three rows are the real commands at the tip). They inflate the **baseline**:
if these three were made discriminating, `1f7f995` would read 26/175 = 1.4857 with H 12/52 (CaseDryRunBash H 3/12,
CaseHelpDryRunEval H 1/12) instead of 29/175 = 1.6571 with H 15/52. Three of the H family's 15 baseline passes are therefore
not evidence for the H rule; they are evidence that a dry-run row exists.

### D4 (suite blind spot, not an expectation) combined short dry-run flags are still false positives at the tip
The H suite has no case for a short-option cluster. Measured:

```
$ git add -nv .            # -n -v ; rc 0 ; .git/index sha256 unchanged  → dry run
$ tool-28c6837 --scan      → rc 1, vcs_write git:add observed            → FP
$ git add -vn .            → same: rc 1, git:add observed                 → FP
$ git push -nv origin master  # rc 0, bare remote refs/heads/master unchanged → dry run
$ tool-28c6837 --scan      → rc 1, vcs_write git:push observed            → FP
```

`git add -N .` (intent-to-add, a write per E4) is correctly flagged, so the miss is specifically the cluster form.
No case in `precision/` or `precision-heldout/` contains `-nv`/`-vn` (`grep -rn 'nv' precision/*.jsonl` finds only unrelated text).
`CaseDryRunBash.md` §F6 discloses the `git add -nv` residual but the suite does not test it, and the push form is not mentioned there either.
Under criterion 30′ ("committed negatives of the shapes the new rule could misread", `SCORECARD.md:1299-1309`) a short cluster is
exactly such a shape; 172/175 should not be read as "dry-run forms are handled".

## Notes (documented, not counted as defects)

- **N1 `jj git push --dry-run` is `observed` only conditionally.** On a dirty working copy the command writes a snapshot
  (op head `f2127fb8…`→`ce4ce2a9…`, `.jj`+`.git` state hash changed); on a clean working copy it writes nothing (op count 5→5,
  state hash unchanged). Amended E4 (`SCORECARD.md:1311-1313`) makes the row unconditional, so the expectation is contract-correct,
  but the fixture text cannot show working-copy state and the `why`'s "snapshots a dirty working copy first" is a premise, not a fact
  of the fixture. The author records this in `CaseDryRunBash.md` Limits (case 8).
- **N2 `git commit --dry-run` is not a byte-level no-write.** Measured: one new loose tree object (`objects/04/a59185a0…`) and a
  rewritten `.git/index` (cache-tree), no HEAD/ref/log/hook change. This matches the author's F3 and E4's class-scoped "no row".
- **N3 `git push -n|--dry-run` runs the pre-push hook** (author F4): measured +1 hook invocation per dry push. The class `vcs_write`
  is about VCS state, so `want_findings []` is correct for the class; it is not a claim that no code ran.

## Confirmations (commands whose opposite would have been visible)

All checks below were run in `/tmp` and are the basis for "correct" above; each could have shown the opposite.

- `git commit -m --help` → rc 0, `HEAD` subject `--help` (commit exists) — the `help-flag-vs-value` / `ctl-commit-m-dry-run-value` rows are real writes.
- `git commit -m probe --help` → rc 0, full usage text printed, `HEAD` unchanged, `git status` unchanged — late `--help` is usage, no commit (`helper-commit-h-late-help`).
- `git commit -m --dry-run` → rc 0, subject `--dry-run` (`commit-msg-value-dry-run`).
- `git commit --dry-run -m x` → rc 0, HEAD unchanged, 0 hook runs, one loose tree + index write (`commit-dry-run`).
- `git commit -n -m x` → rc 0, commit created, 0 hook runs; positive control `git commit -m normal` → 1 hook run (`commit-n-no-verify`).
- `git add -n .` / `--dry-run` → rc 0, `.git/index` sha256 identical, no objects (`add-n`, `add-dry-run`, `run-add-n`, `n-two-meanings` L1).
- `git push -n origin master`, `git push --dry-run`, `git push origin master --dry-run` → rc 0, remote `refs/heads/master` and tracking refs unchanged (`push-n`, `push-dry-run`, `push-trailing`, `popen`).
- `jj --ignore-working-copy git push --dry-run` (dirty) → op heads, `.git/index`, `.git` refs, `.jj` state all unchanged (`jj-push-dry-run-ignore-wc`, `jj-push-dry-run-snapshot` L1).
- `jj git push --dry-run` (dirty) → op head changed; `jj --ignore-working-copy diff -r @` shows the change snapshotted into `@` (`jj-push-dry-run-snapshots`, `jj-push-dry-run-snapshot` L2).
- `jj st --help`, `jj describe -h`, `jj describe --help`, `jj commit --help` (dirty) → op head unchanged; control `jj st` changes it (`bang-jj-help-flags`, `tool-bash-jj-commit-help`, `pct-bash`).
- `git --help push`, `git -C DIR --help commit` → man page, rc 0, `.git` unchanged (`check-output-help-before-sub`).
- Counter immutability: `git diff f3da504 28c6837 -- .ufo/waves/round-20/tw-precision.py` is the `SUITE_PIN` line only; `expected.json` sha256 unchanged since `f3da504`.

## Limits

- git 2.56.0 and jj 0.45.1 only; all probes in `/tmp` repos with `HOME`/`GIT_CONFIG_NOSYSTEM` redirected. Working-copy state is what
  the scanner never sees, so N1 cannot be decided from a fixture.
- I did not run the authors' `/tmp` harnesses or mutants (`/tmp/CaseDryRunBash/emp.py`, `/tmp/CaseHelpDryRunEval/emp*.sh`); my mutants
  are my own minimal edits of the committed tip tool, applied only in `/tmp`. The author's m2 result is quoted from their report, not re-run.
- The counter is the wave-1 file plus the pin; I did not modify it. The "26/175" figure above is arithmetic on the three known
  wrong-attribution passes, not a measured run of a modified counter.
- The whole-corpus no-harm diff vs `9c54c56` (SCORECARD "pending (wave 2)") was not run by this seat; it is not this item.
- I did not evaluate the other 28 H cases (other seats) or the held-out set except to confirm 0/12 at both revisions.

## Installs

none.
