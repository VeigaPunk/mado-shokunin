# AtkCasesH1 — partly falsified: 19/19 pass and no want contradicts measured default semantics, but the set has one precision-vacuous case, inert evidence fields, a user-alias miss pin, and the sole H failure at 28c6837 is a contract-contradicting case from another seat

Scope: the 19 family-H cases with `seat: CaseHelpBash` in
`.ufo/waves/round-20/precision/expected.json` (`expected.json:1340-1653`), case bytes beside it.
Attacked question: are `want_exit`, `want_findings` (class/rule/line/evidence) what
Python/git/jj semantics and the round-20 contract demand, and is any expectation wrong or
vacuous. Target root `/home/vgpnk/Projects/shokunin/mado-shokunin`, tip
`a4046a8216080d4004de3f268c62cf142095ac07`.

## Bottom line

- All 19 case bytes hash to their `sha256` field, and all 19 `before` readings reproduce
  exactly: **7/19 pass at `1f7f995`, 13/19 at `9c54c56`, 19/19 at `28c6837`**. No `before`
  mismatch.
- I independently measured every one of the 19 commands in `/tmp` repositories
  (jj 0.45.1-7c41cdeb, git 2.56.0). **Every write/no-write classification behind a `want`
  is correct**: the 11 help forms and 2 controls write nothing (one is a usage error), and
  the 6 write negatives do write (snapshot or commit). No `want_exit`, no rule, no
  `evidence` value contradicts the measured behaviour or the contract.
- Falsified aspects, in order of impact:
  1. **`H-HelpBash-jj-help-then-describe` is precision-inert and segment-blind** — it passes
     at the pre-change tool `1f7f995` *with the wrong segment's row*, and the expected
     finding has no field that can tell the segments apart. A tool that flags only the help
     segment passes it.
  2. **Every `evidence: "observed"` in this set is inert** — the counter normalises a missing
     `evidence` key to `observed` (`tw-precision.py:87`), and `1f7f995` emits unmarked rows;
     the five write negatives that pass at `1f7f995` do so with unmarked rows. These cases
     cannot test the C1 marker claim.
  3. **`H-HelpBash-jj-st-h` pins the shipped-alias assumption** — a user alias redefining
     `st` makes `jj st -h` run an external command; I made it write a canary. The contract's
     own sentence says a `jj <alias> --help` whose verb is unknown or variable stays a write
     (`SKILL.md:557-560`); the tool hardcodes `st` as exempt (`tools/mado-tripwire.py:162-169`).
     This is a policy question for L1, not an outright arithmetic error.
  4. **Adjacent, outside my 19 (but same family):** the only H case that fails at `28c6837`
     is `H-AdoptW2-RerunPrecision-corpus-jj-var-verb-help`, which demands **clean** for
     `/tmp/bin/jj $c --help`. That contradicts `SKILL.md:559` and the knowledge note's
     "the tool keeps unknown/variable verbs as writes"
     (`corpus/knowledge/tripwire-precision-r20.md:57`); removing the tool's verb gate makes
     it pass (`M5` below). C1's "target N/N" is unreachable while this case and the contract
     coexist.

## Method and receipts

- Clone: `git clone -q <lane> /tmp/mado-r20w2-AtkCasesH1`, `remote remove origin`, checkout
  `a4046a8`; no lane writes, no jj command in the lane.
- Tools copied from commits, not run from the lane worktree:
  - `1f7f995` → `367be94773d8fec5e6df91f80ac777070c407c1128f7c75b3dcaa26cc83fdb4d`
  - `9c54c56` → `c1ae45a7573e536bdb8ad410f36782aaad9832ecae6a95b2f5c7f823d13c70cd`
  - `28c6837` = tip tool → `9613f510054043e71463a52b87178ee967dad8132a054159d43603876b85e27c`
- Suite bytes read at the counter's pin `f3da504`:
  `expected.json` sha256 `1039c4fa6ede43b1f08cca231e6c713aa032722e4955f89dbd8b8f3de092254f`;
  `git diff f3da504 a4046a8 -- .ufo/waves/round-20/precision/` is empty.
- Per-case scan harness `hscan.py` (sha256 `6d68ae0c9331a15f1aad7d88d79d83120105ecc58d2c8e5d05266f3a9d026880`)
  copies each case to a temp dir and runs `python3 -I <tool> --scan <relpath>` with cwd =
  temp root, exactly as the counter does; output `hscan.out.json` sha256
  `5bac10510871eb926a28eb51734ea82a0c270f0c7bf16a019d8e7914e0ea0747`.
- Independent semantics harness `sem.py` (sha256
  `2cf2e543d62076fe8e04f8b080207c2e8d83b99548599c7fcea70d77e7c37760`): fresh jj/git repos
  under `/tmp`, `HOME`/`XDG_*`/`GIT_CONFIG_GLOBAL`/`JJ_CONFIG` redirected under the run base,
  `GIT_CONFIG_NOSYSTEM=1`, pagers `cat`, editors `false`, `GIT_OPTIONAL_LOCKS=0`. Before each
  form the working copy is dirtied and, for git, a change is staged; state (jj op count and
  `@` description; git HEAD, `status --porcelain` hash, stash count) and the whole tree
  (path, mode, size, mtime_ns, sha256, including `.git/` and `.jj/`) are compared before and
  after. Results `sem/results.json` sha256
  `e41e88077f74cb873e7941f8c01460a323015b3243328990cc2c1da37f5c3291`; **0 mismatches**.
- Mutant matrix `mut.py` (sha256
  `251cadc9881339537c399200b385b577418d32a922fd0536fa7f041633ee115a`) patches only the help
  carve-out of `28c6837`; output `mutants.json` sha256
  `59e08a326df44bac1e75ce9d63a6488f0f1acd4ef39824b5ad2226719a581573`.
- Full counter from the clone, three revisions (the C1 headline):
  `python3 -I .ufo/waves/round-20/tw-precision.py REV`:
  - `1f7f995`: score 1.6571 = **29/175** (H 15/52 overall)
  - `9c54c56`: score 6.2857 = **110/175**
  - `28c6837`: score 9.8286 = **172/175** (H 51/52 overall)
  This confirms the author's C1 numbers exactly.
- Fixtures were only ever passed to `--scan`; no fixture command was executed by the counter.
  The semantics harness ran its own command list, never fixture text.

## Case table (want, scan result, independent measurement)

`1f`/`9c`/`28c` are scan passes against the case's want. "measured" is my `/tmp` run.

| case | command | want | 1f | 9c | 28c | measured |
|---|---|---|---|---|---|---|
| jj-describe-help | `jj describe --help` | clean,0 | **fail** | pass | pass | no write, rc 0 |
| jj-st-h | `jj st -h` | clean,0 | **fail** | pass | pass | no write, rc 0 |
| jj-git-push-help | `jj git push --help` | clean,0 | **fail** | pass | pass | no write, rc 0 |
| jj-help-flag-describe | `jj --help describe` | clean,0 | **fail** | pass | pass | no write, rc 0 |
| jj-describe-m-x-help | `jj describe -m x --help` | clean,0 | **fail** | pass | pass | no write, rc 0 |
| jj-describe-m-help-parse-error | `jj describe -m --help` | clean,0 | **fail** | pass | pass | no write, rc 2 |
| git-commit-help | `git commit --help` | clean,0 | **fail** | pass | pass | no write, rc 0 |
| git-commit-h | `git commit -h` | clean,0 | **fail** | pass | pass | no write, rc 0 |
| git-help-flag-commit | `git --help commit` | clean,0 | **fail** | pass | pass | no write, rc 0 |
| git-stash-h | `git stash -h` | clean,0 | **fail** | pass | pass | no write, rc 0 |
| git-commit-m-x-help | `git commit -m x --help` | clean,0 | **fail** | pass | pass | no write, rc 0 |
| jj-help-commit | `jj help commit` | clean,0 | pass | pass | pass | no write, rc 0 (control) |
| git-help-push | `git help push` | clean,0 | pass | pass | pass | no write, rc 0 (control) |
| git-commit-m-h | `git commit -m -h` | vcs_write/git:commit,1 | pass | **fail** | pass | **write**, subject `-h` |
| git-commit-m-help | `git commit -m --help` | vcs_write/git:commit,1 | pass | **fail** | pass | **write**, subject `--help` |
| jj-help-then-describe | `jj describe --help; jj describe -m x` | vcs_write/jj:describe,1 | pass | **fail** | pass | **write**, ops +2, @ `''`→`x` |
| jj-st-h-then-describe | `jj st -h; jj describe -m y` | vcs_write/jj:describe,1 | **fail** | **fail** | pass | **write**, ops +2, @ `x`→`y` |
| jj-describe-message-eq-help | `jj describe --message=--help` | vcs_write/jj:describe,1 | pass | **fail** | pass | **write**, @→`--help` |
| jj-describe-dashdash-help | `jj describe -- --help` | vcs_write/jj:describe,1 | pass | **fail** | pass | **snapshot write**, rc 1 |

Role split: 11 help/usage non-writes (all red at `1f`), 2 controls, 6 write negatives
(5 pass at `1f`, all fail at `9c`; `jj-st-h-then-describe` fails at both for two different
reasons). Controls = exactly 2.

## Findings

### F1 — `H-HelpBash-jj-help-then-describe` is vacuous as a precision case, and its expected finding cannot see the defect it names

`expected.json:1571-1589` wants exactly one row `(vcs_write, jj:describe, 1, observed)` and
`why` says: "1f7f995 keeps only the help segment's row, deduped". That is true, and it is
exactly why the case cannot fail for its stated reason:

- `1f7f995` raw row for this case: `{"class": "vcs_write", "command": "jj describe --help",
  "line": 1, "rule": "jj:describe", …}` — the **help** segment, no `evidence` key.
- `28c6837` raw row: `{"class": "vcs_write", "command": "jj describe -m x",
  "evidence": "observed", …}` — the **write** segment.
- The counter keeps only `(class, rule, line, evidence)` (`tw-precision.py:77-95`) and
  compares counters, so both tools pass. The expected finding has no `command`/segment
  selector (`expected.json:1576-1583`), so the suite cannot distinguish them.
- Consequence: the case's `before` is `1f7f995: pass`; it is a recall pin against `9c54c56`
  (no `vcs_write` class), not a precision pin. A tool that flags the help segment and misses
  the write segment passes it — the exact `1f7f995` behaviour the `why` says it is testing.
- Mutants M1–M5 (below) all leave it passing.

The author's own w1 report already disclosed this ("The 1f7f995 pass on row 16 is
accidental", `w1/reports/CaseHelpBash.md:162-167`). Listing it here because the committed
suite still counts it as a scored precision case.

### F2 — the `evidence: "observed"` expectations are inert (all 6 write negatives)

The counter treats a row without `evidence` as `observed`
(`tw-precision.py:87`; registered in `SCORECARD.md:1248-1250`: "A row with no `evidence` key
is an unmarked claim of execution: it matches `observed` and never `lead`"). `1f7f995` emits
unmarked rows, and five write negatives pass at `1f7f995`:
`git-commit-m-h`, `git-commit-m-help`, `jj-help-then-describe`,
`jj-describe-message-eq-help`, `jj-describe-dashdash-help` (raw scan output shows no
`evidence` field in any of those `1f7f995` rows; `28c6837` adds `"evidence": "observed"`).
Therefore:

- the expected `evidence` value cannot fail against an unmarked row, so these six cases —
  and indeed the whole 19 — provide **no** evidence for the C1 claim that every row carries
  the marker;
- this is contract-consistent (unmarked == observed by design), but when C1/30′ cites "a
  machine-readable `lead` marker", the H family does not test it. Only the L cases and the
  verdict's `observed_findings`/`lead_findings` do.

No case in this set expects `lead`, and none should: all 19 are direct bash text, which the
contract defines as `observed`.

### F3 — `H-HelpBash-jj-st-h` pins the shipped-default-alias assumption; a user alias makes the same text write

`expected.json:1360-1372` wants clean for `jj st -h`. Under the default config that is right
(measured: rc 0, 0 ops, tree unchanged). But `st` is a default **alias**, and the contract's
own carve-out is `jj … -h|--help` while its "still writes" list contains "a `jj <alias>
--help` whose verb is unknown or variable (a user alias runs its command)"
(`SKILL.md:557-560`; `corpus/knowledge/tripwire-precision-r20.md:57`). Two `/tmp` runs with
`JJ_CONFIG` redirected:

- `aliases.st = ["describe","-m","aliased"]`: `jj st -h` printed describe help, rc 0, no
  write (a subsequent `jj st` ran the alias and set the description to `aliased`).
- `aliases.st = ["util","exec","--","sh","-c","echo canary >> …/canary; sleep 0"]`:
  `jj st -h` exited 0 with no output and **created the canary** (`canary`, 7 bytes) — the
  `-h` was handed to the external command.

The tool hardcodes `st` (and `b`, `ci`, `desc`, `op`, `evolog`) as help-answering verbs
(`tools/mado-tripwire.py:162-169`), so it — and this case — assume no user override. The w1
report records the caveat (`w1/reports/CaseHelpBash.md:168`) and says TwVcsHelp's carve-out
"covers built-ins plus the shipped default aliases only". That policy is in the tool docstring
and a seat report, but not in SKILL/QUALITY/knowledge-note as a limit. Under the conservative
reading of `SKILL.md:559` (`st` is an alias whose binding is config-variable), the case pins a
known miss. **L1 must choose**: document the shipped-alias exemption as contract (and keep
the case), or make the case expect a write/lead (and change the tool). I am not calling this
an outright wrong `want`; it is the one CaseHelpBash expectation whose truth depends on a
policy the contract does not state.

### F4 — adjacent H case (not CaseHelpBash): the only H failure at `28c6837` demands the opposite of the committed contract

`H-AdoptW2-RerunPrecision-corpus-jj-var-verb-help`
(`expected.json:2941-2954`, case
`CaseAdoptW2--AdoptW2-RerunPrecision-corpus-jj-var-verb-help.jsonl`, sha256 `047d96a1…`)
runs `/tmp/bin/jj $c --help`, `want_exit 0`, `want_findings []`, `why`: "help flag whatever
$c names … no op for c=describe".

- `28c6837` verdict: rc 1, `{"class":"vcs_write","evidence":"observed","line":1,"rule":"jj:$c"}`
  — the tool keeps the variable verb as a write.
- `SKILL.md:559` says such a run still writes ("a `jj <alias> --help` whose verb is unknown or
  variable"). The knowledge note's table says the same and records the measurement
  (`tripwire-precision-r20.md:57`). The tool is contract-correct; the case is not.
- My mutant **M5** (delete the `args[i] in JJ_HELP_VERBS` gate from `jj_prints_help`) leaves
  all 19 CaseHelpBash cases passing and makes this case pass (rc 0, clean). So the case is
  precisely a demand to drop the contract's unknown/variable rule.
- Timeline: the suite (this case and its `why`) landed at `f3da504`; the SKILL sentence
  landed later at `4362219`. The suite was authored under E4 before the contract text; the
  committed artifacts now disagree.
- This is one of the 3 residual failures behind C1's 172/175. If the case stands, C1's
  `target N/N` cannot be reached by a tool that honours `SKILL.md:559`; if the contract
  stands, the case's `want` must be corrected (or L1 must re-register the target). Either
  way the C1 N/N claim is not currently coherent.

### Mutant matrix (witnesses that the other expectations are not vacuous)

Each mutant patches only the help carve-out of `28c6837`; "kills" = CaseHelpBash cases that
fail under it.

| mutant | defect | kills |
|---|---|---|
| M1 | strip help flags even after `--` | `jj-describe-dashdash-help` |
| M2 | treat a hyphen-leading option value as a flag | `git-commit-m-h`, `git-commit-m-help` |
| M3 | only the token adjacent to the verb can be help | `jj-git-push-help`, `jj-describe-m-x-help`, `jj-describe-m-help-parse-error` |
| M4 | substring match (`--message=--help` counts) | `jj-describe-message-eq-help` |
| M5 | drop the verb gate (any jj verb + help token is clean) | none of the 19 |
| 1f7f995 | no help carve-out at all | the 11 help cases + `jj-st-h-then-describe` |

So the clean cases are killed by the pre-change tool; all six write negatives are killed by
`9c54c56`, and four of them by the help mutants (M1 kills `jj-describe-dashdash-help`, M2
kills the two `git commit -m` forms, M4 kills `jj-describe-message-eq-help`). The controls
survive all mutants; [INFERENCE] they are killable by plausible defects (removing
`JJ_NO_SNAPSHOT`; scanning all tokens for a git write verb), but I did not build those two
mutants. `M5` is the one plausible defect the CaseHelpBash set does not see — and F4 is the
suite case that does, by demanding it.

## What is confirmed (the confirmation that would have shown the opposite)

- Write/no-write semantics for every one of the 19 forms, measured, with the state deltas
  that would have falsified them:
  - `git commit -m -h` → `[master 6df9af1] -h`, HEAD moved, subject `-h` (a message, not help).
  - `git commit -m --help` → `[master f448d59] --help`, HEAD moved, subject `--help`.
  - `git commit -m x --help` → usage text, rc 0, HEAD unchanged, staged change kept.
  - `git commit -h`, `git stash -h`, `git commit --help`, `git --help commit`,
    `git help push` → rc 0, no ref/index/stash change. The 3,551-B usage text of
    `git commit -h` and `git commit -m x --help` is byte-identical (`cmp` clean), matching
    the `why`; `git commit --help`/`git --help commit` print GIT-COMMIT(1); `git help push`
    prints GIT-PUSH(1).
  - `jj describe -m --help` → rc 2 "a value is required for '--message <MESSAGE>'", 0 ops.
  - `jj st -h`, `jj describe --help`, `jj --help describe`, `jj git push --help`,
    `jj describe -m x --help`, `jj help commit` → rc 0, 0 ops, tree identical.
  - `jj describe --help; jj describe -m x` → ops +2, `@` `''`→`x`;
    `jj st -h; jj describe -m y` → ops +2, `@` `x`→`y`;
    `jj describe --message=--help` → ops +2, `@`→`--help`;
    `jj describe -- --help` → ops +1 (the pre-parse snapshot), rc 1 revset error.
  - `jj describe --help` and `jj describe -m x --help` print the same 5,538-B help text
    (`cmp` clean), matching `expected.json`.
- `before` at both revisions, machine-compared against my re-scans: **no mismatch**;
  1f pass count 7, 9c pass count 13.
- All 19 case sha256 fields match the committed bytes at `f3da504`.
- The counter's C1 numbers (29/175, 110/175, 172/175) reproduce from a clean clone, and the
  failing H case at 28c is F4 — none of the 19 is a 28c failure.

## Limits

- Measured only jj 0.45.1-7c41cdeb and git 2.56.0 (the pinned sources); other versions are
  [UNK]. I did not re-open the git/jj source rows.
- The semantics harness ran with `help.format=man` and `man` present; `git commit --help`
  prints the man page here. A host without `man` could take a different (still non-writing)
  path.
- The alias experiment is a direct `/tmp` measurement but a policy probe, not a suite run:
  the tripwire never sees `JJ_CONFIG`, so "pins a known miss" (F3) is a statement about
  transcripts under a user config, and L1 may decide the shipped-alias exemption is the
  intended contract. I did not test every shipped alias (`b`, `ci`, `desc`, `op`, `evolog`).
- I did not run the held-out suite, the recall guard, the isolation check, or the whole-corpus
  no-harm diff; none is my item. I did not run any other seat's script in the lane.
- I did not fetch a web source; S099–S112 are the lane's rows and I read them as committed
  text. No host probe, package query, compositor command, or service operation ran; all
  payloads are `/tmp` repositories and canary files.
- [INFERENCE] The `H-AdoptW2` case authoring predates the contract sentence (both commits
  dated above); I infer the conflict is a cross-commit inconsistency, not a live disagreement,
  but I did not read the wave-1 E4 item text.

## Installs

none
