# ConnSiblingClassifiers — help/dry-run is per command; a shared `-h` or `--dry-run` token is the wrong borrow

One move: teach `classify_git` / `classify_jj` a per-command flag walk (stop on exact help, consume values, split `-n` and `--dry-run` by command). Leave every sibling classifier's exit rule and wrapper table where it is.

Axes weighed: C1 precision (H clean, write negatives kept, L stays exit 1, P stays no row), the lose-0-findings guard against `9c54c56`, C2 untouched.

## What the lanes actually contain

Read-only scan of the twenty sibling trees under `/home/vgpnk/Projects/shokunin/*-shokunin` (not `mado-shokunin`), keywords `tripwire`, `classify`, `dry-run`, `lead`, then the tools those hits named. No sibling parses assistant `toolCall` text into observed execution versus a lead. `mado-shokunin/tools/mado-tripwire.py` itself has no `evidence` key (grep of that file: no matches). `helper_argv_leads` (`:1379-1390`) appends ordinary `classify_shell` hits. Tool sha256 `367be94773d8fec5e6df91f80ac777070c407c1128f7c75b3dcaa26cc83fdb4d` (matches SCORECARD.md round-20 baseline).

Shipped command-adjacent classifiers, and the empty lanes:

| Lane | What it classifies | Path |
|---|---|---|
| tsukuroi | Backticked/fenced/`procedure:` invocations of a forbidden *binary*. Prose names and shell comments are not invocations. | `tsukuroi-shokunin/tools/check-recheck-commands.py` sha256 `cbff0d4120b1d0d367fc9999c4047f9560bb3e8c2ab4e011c27eee6a5e8e493e` |
| mori | Misroot *candidates*. Exit 1, labeled not proof. | `mori-shokunin/tools/mori-misroot-sweep.py` sha256 `0a852fe67f14afa1da9f5f8e806c63fa640e8df2a90b87909e6a2453c66b3dca` |
| kagi | Secret-shaped transcript rows. HIT exits 1; WARN does not; `--classify` exits 0. | `kagi-shokunin/corpus/transcript-scan.sh` sha256 `2d60981b198cef41b9263a1427b41f92d98b65eb26ff71c28057bea0ad823a23` |
| souji | The quarantine tool's own `--dry-run`. Unsafe targets stay blocked. | `souji-shokunin/tools/souji-quarantine.sh` sha256 `83cc3ce1331bf75ed23b9148ad82b6f0881e9eda1d9a283a224f0318d6ab1de3` |
| kama | Offline Ollama JSON. The tool's `--help` is not a classification. | `kama-shokunin/tools/kama-ollama-evidence.py` sha256 `38d1f5d216181bdb7693582027da83eace707f111f42dd32785d386ffe78fb02` |
| kotodama | Policy-mention vs substantive mark. Docstring: never a verdict. | `kotodama-shokunin/tools/source-audit-inventory.py:152-164` sha256 `f617bb99318f501db2ff51c0c180daeacf548b1a36591b1a1a80c253197b2210` |
| game-dev-2d | Godot stdout/exit/signature. | `game-dev-2d-shokunin/corpus/fixtures/run_battery.py:2591-2608` |
| kumitate | Census member counts (`FROZEN`) and citation tokens (`classifyToken`). | `kumitate-shokunin/scripts/kimi-census.mjs:149`, `scripts/cite-check.mjs:898` |
| chousa | Claim `observed=refused` before a read. Isolation seat owns that. | `chousa-shokunin/tools/research-gate.sh:1369` |
| audio, game-dev-3d, kengaku, tabi | No `tools/` and no keyword hits in `*.py`/`*.sh`/`*.md`. | — |
| kaidoku, kake, kasegi, lore, revenger, tameshi, kotoba | Keyword hits are prose, mutation labels, or scratch clones. `kasegi` `ops/park-disposition.mjs` is named in `SKILL.md:477` and is not in the tree (glob `**/*park-disposition*` = 0). | — |

## Borrow

**Mori's candidate stays a failing result.** `RC_CANDIDATE = 1` (`mori-misroot-sweep.py:46`); a candidate returns that code (`:335`); the limit says a candidate is a review lead, not proof (`:26-27`, repeated `:791`). That is the exit shape E1 already requires for invisible-body leads: the row stays in `findings`, the verdict stays `findings` / exit 1, and `observed_findings` / `lead_findings` are counts on that same object. Round-19 R19-V3 (`corpus/lessons/round-19-verifier-spotcheck.md:151`) is this repair. Family P is the other direction: pure data gets no row (`SCORECARD.md:1250-1251`). Keeping `frozenset(...)` as a lead row would repeat the round-19 harm (ordinary `package_query`, no marker) in a new costume.

**Tsukuroi's context split, applied only as a walker shape.** `check-recheck-commands.py:32` — a prose mention ("never run pacman") is not an invocation. `:283-285` — bare prose is never a command; only backtick spans are. `:209-234` `command_word` skips assignments and wrappers, and a listed option consumes the next token. Mado's input is already a `toolCall` command, so switching the scanner to backtick extraction would drop `subprocess.run([...])` and fail family W. The walker shape (flag position versus consumed value) is what `classify_git` lacks.

**Mado already short-circuits one non-execution flag.** `strip_prefix` returns `[]` for `command -v` / `command -V` (`mado-tripwire.py:374-375`: "lookup only, nothing is executed"). Same idea as a help flag: the token means the words are not a run. The sudo table is a different idea (below).

## Do not copy

**`-h` already means "take the next word" on sudo, in two lanes.** Tsukuroi `WRAPPERS["sudo"]` is `({"-u", "-g", "-C", "-h", ...}, 0)` (`check-recheck-commands.py:78`). Mado `SUDO_ARG_OPTS` includes `"-h"` (`mado-tripwire.py:117-118`) and `first_verb` consumes the next token for members of that set (`:462-474`). Git's own parser does the opposite with the same spelling: while walking global options, exact `-h` / `--help` *breaks* and becomes the help command (`fetch/SrcGitHelpSource/git.c:171-173`, then `:973-974`). `git commit --help` is rewritten to `git help` when argv[1] is exactly `--help` (`git.c:762-770`). `--help` in `parse-options.c` is `!strcmp(arg + 2, "help")` (`:1130-1131`). A tripwire that adds `-h` to `GIT_ARG_OPTS` the way sudo lists it will swallow the following subcommand on `git -h commit` and still return `commit` for `git commit -h`, because `first_verb` returns the first positional and never looks past it (`RevengeVcsHelpIntent.md:9-11`, same tool sha).

**`-n` is not one flag.** Fetched git 2.56.0:

- commit: `OPT_BOOL('n', "no-verify", ...)` and `OPT_BOOL(0, "dry-run", ...)` — dry-run has no short `-n` (`fetch/SrcGitCommitDoc/builtin-commit-v2.56.0.c:1750-1751`; adoc `:218-222` and `:378-381`).
- add: synopsis `[--dry-run | -n]` (`fetch/SrcGitAddPushDoc/git-add.adoc:11`, `:67-70`).
- push: synopsis `[-n | --dry-run]` and a separate `--no-verify` (`git-push.adoc:12`, `:17`, `:161-163`, `:430-434`).
- The shared macro `OPT__DRY_RUN(var, h)` is `OPT_BOOL('n', "dry-run", ...)` (`parse-options.h:568`). Applying that macro to every git subcommand cleans `git commit -n`, which E4 and the commit source both keep as a write.

**`--dry-run` is not one flag either.** `ScoutJjHelpEmpirical.md:37` measured `jj git push --dry-run` on jj 0.45.1 as exit 0 and ops 6→7 (one `snapshot working copy`). The same report's help/version rows are 0 ops (`:24-36`), and `jj st` / `jj log -n 1` are the +1 controls (`:35-36`). E4's sentence lists `jj git push --dry-run` with the non-writes. The measurement contradicts that sentence. Clearing every `--dry-run` token would drop a real snapshot class (`jj:git` today, `JJ_GIT_WRITE` at `mado-tripwire.py:132` and `:516-518`). That can fail the lose-0-findings guard (`SCORECARD.md:1258-1259`) on any corpus line the `9c54c56` tool already reports. [INFERENCE] whether any corpus line is that command was not counted here.

**`jj describe -m --help` is not `git commit -m --help`.** Scout table (`ScoutJjHelpEmpirical.md:72-79`): jj exits 2 with 0 ops (clap rejects a hyphen-leading separate value); git 2.56.0 commits a subject `--help`. Commit's `-m <msg>` is a value slot (`git-commit-v2.56.0.adoc:186-188`). The "option value still writes" clause is the git fact. The same clause on jj over-reports an error that snapshots nothing. The forms that do write a `--help` description are the `=` forms (`-m=--help`, `--message=--help`), which a "any `--help` token is help" scan would miss (`ScoutJjHelpEmpirical.md:76-81`).

**Weaker class that leaves the exit code.** Kagi `--classify` prints `key_shaped` / `prose` and then `exit 0` (`transcript-scan.sh:117-129`, `:276`). WARN increments `warns` and the gate exits on `hits` only (`:155-165`, `:282`). Kotodama `classify` returns `policy-use-mention` and says "Never a verdict" (`source-audit-inventory.py:152-161`). Souji `--dry-run` still computes stage 1 and emits `DRY-RUN-BLOCKED` with exit 3 for a NOT-SAFE target (`souji-quarantine.sh:25-27`, `:92-95`, `:1568-1573`). Kama's epilog says the tool's own `--help` is plaintext, exit 0, and is not a classification (`kama-ollama-evidence.py:464-465`). None of those is E1. A side mode that exits 0 while leads exist fails family L. Souji's "dry-run still blocks" pasted onto `git commit --dry-run` fails family H. Kagi's WARN pasted onto `frozenset` keeps a row and fails family P.

**Do not replace `strip_prefix` with tsukuroi's `WRAPPERS`.** Mado peels `setsid` (`mado-tripwire.py:119`) and handles `env` / `nice` / `ionice` / `timeout` / `xargs` / `flock` in `strip_prefix` (`:386-458`). Tsukuroi's set has no `setsid` and folds sudo into the same table as `command` (`check-recheck-commands.py:77-91`). One shared table changes which host command is seen.

**Git's `ac == 2` help is narrower than E4.** `show_usage_with_options_if_asked` treats `-h` as help only when `ac == 2` (`parse-options.c:1504-1508`). The option loop also shows usage for a lone `-h` (`:1049-1051`) and for an *unknown* short whose current character is `h` (`:1070-1071`). E4's `git <sub> -h` examples are exact tokens. Clustered shorts (`-nh`) are [UNK] relative to the contract; this seat did not run them.

## Proposed move

Inside `classify_git` and `classify_jj` only, after the existing wrapper peel:

1. Walk tokens with the same consume/skip loop as `first_verb`, but **stop** when the token in flag position is exactly `-h` or `--help` (git.c:171-173 and :762-763; parse-options.c:1130). That invocation is not `vcs_write`. `jj help` / `jj version` stay on `JJ_NO_SNAPSHOT` (`mado-tripwire.py:133`, `:519-520`).
2. Git commit: `-m` / `--message` consume the next token (`git-commit-v2.56.0.adoc:186-188`). `--help` in that slot stays `git:commit`. `-n` stays `git:commit` (`builtin-commit-v2.56.0.c:1750`). `--dry-run` in flag position is not a write (`:1751`, adoc `:378-381`).
3. Git add and git push: flag-position `-n` and `--dry-run` are not writes (`git-add.adoc:11,67-70`; `git-push.adoc:12,161-163`). Push `--no-verify` stays a write (`:430-434`).
4. Jj help flags (`jj st -h`, `jj log --help`, `jj --help`) are not writes (0 ops, `ScoutJjHelpEmpirical.md:24-32`). `jj describe -m --help` is not a write (exit 2, 0 ops, `:72`). `jj describe -m=--help` stays a write (`:76`). `jj git push --dry-run` stays `jj:git` (`:37`, +1 snapshot op).
5. Leads stay on the scan verdict at exit 1, with `evidence` (mori `:46` / `:335`). Pure calls stay absent. Do not add a `--classify` mode.

`sudo -h <host>` keeps consuming the next word (`SUDO_ARG_OPTS`). A later real write in the same text stays its own hit (`classify_shell` is per segment).

## Affected axes

- **C1.** Improves H for git help, git add/push dry-run, and jj help flags, and keeps the write negatives the sources and the jj scout actually measured. Harmed if one `--dry-run` or one `-n` or one "value still writes" rule is applied to both git and jj: `git commit -n` goes clean, or `jj git push --dry-run` goes clean, or `jj describe -m=--help` goes clean, or `git commit -m --help` goes clean.
- **Lose-0-findings vs `9c54c56`.** Exempting `jj git push --dry-run` can drop a finding the old tool emits. Help-flag exemptions can too, if a corpus line is `jj log --help` and the old tool reports `jj:log`. The corpus diff is the check; this seat did not run it.
- **C2.** No change. Criterion 29 stays with the isolation seats (`ConnSiblingIsolation.md`).

## Risks

- `jj log -n 1` is a snapshot (+1 op, scout `:36`). An add/push-style "`-n` means dry-run" rule on jj cleans a real snapshot. Jj `-n` was not given a second meaning in this scan; treat it as [UNK] outside that measured form.
- `jj git push --dry-run` was measured without a remote (`ScoutJjHelpEmpirical.md:95`). The +1 op is the snapshot, which is already what `jj:git` names. Remote side effects of that flag are [UNK].
- Clustered git shorts and `git commit -h` with extra operands were not executed here. Exact-token stop matches the contract examples; prefix match (`--helper`, `-h` inside `-nh`) is out of the move.
- Copying tsukuroi's depth cap (`invocations` returns at `depth > 4`, `:247-248`) onto mado's helper walk (`depth < 4`, `mado-tripwire.py:1412`) is a different edit. This move does not touch it.

## Verification

L1, not this seat. `python3 -I .ufo/waves/round-20/tw-precision.py REV` on the H cases and the write negatives: `git commit -h`, `git --help commit`, `git commit --help`, `git commit --dry-run`, `git add -n`, `git push -n`, `git commit -n`, `git commit -m --help`, `jj log --help`, `jj st -h`, `jj describe -m --help`, `jj describe -m=--help`, `jj git push --dry-run`, plus a second segment that is a real `git commit` in the same text. Family L still exit 1 with `evidence=lead`. Family P still exit 0. `tw-recall.py` 6/6. Whole-corpus diff against `9c54c56` loses 0 findings. This seat did not run the tripwire, jj, or git.

## Limits

- No sibling tool was executed. Classifications above are source reads plus the already-written `ScoutJjHelpEmpirical` measurements.
- Scratch trees (`.ufo/waves/**/clone`, lore `.scratch`) were not treated as shipped classifiers.
- `game-dev-2d` `classify_process` was read; other `classify_*` helpers in that file were not.
- Jj behavior is the scout's 0.45.1 binary. Other versions are [UNK].
- Whether the live corpus contains `jj git push --dry-run` or `jj <sub> --help` was not counted.

## Installs

none
