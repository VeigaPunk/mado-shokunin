author: mado-shokunin (L1 MadoR20 + lane-dispatched L2 advice)

# Round 20 — repair: tripwire precision, fail-closed isolation, round-19 tallies

Date: 2026-10-20. Baseline `1f7f995` (round-19 tip `b435568` + closure
`round-19-verifier-spotcheck.md`, **rejected-harmed**); pre-harm baseline `9c54c56`;
pre-registration `e629f73`; suite landed `f3da504` (no tool change); tool repair
`28c6837`. Wave evidence `.ufo/waves/round-20/`; report `.ufo/reports/round-20/mado.md`
(fleet).

## Mistakes

| id | class | evidence pointer | captured-by | fix (shown able to fail) |
|---|---|---|---|---|
| M1 | precision-for-recall trade (round 19, L1 + seats) | closure `round-19-verifier-spotcheck.md:63-81`: `BLOCK=frozenset(['pacman','-Q','hyprland'])` reads clean at `9c54c56`, an ordinary `package_query` finding at `b435568`; w1 ScoutBuiltinsFire: 125 of 159 builtin names fire at the harmed tool, 0 at `9c54c56`; ScoutStdlibFire: 69 of 70 pure stdlib imports fire | none at landing (round-19 w2 CriticC3W2 saw it, the lesson filed it as a limit; the closure demonstrated it) | QUALITY 30 + `tw-precision.py`: family P 7/66 and L 1/18 at `1f7f995` (red) → 66/66 and 17/18 at `28c6837`; the closure's artifact is case `P-CasePureBuiltins-frozenset-closure` |
| M2 | fail-open isolation (round 19 M12) | round-19 `w2/reports/SentinelGatePath.md:75-79`: `[ -e ] && mount && echo` under `set -e`; refused mounts did not stop the script and the real `/usr/bin/hyprctl probe` ran (S110: `set -e` ignores a failing non-final `&&` member) | none (seat self-report; the scan cannot see a written-then-run script) | QUALITY 29 + `isolation-check.sh`: the round-19 shape reads `FAIL_OPEN` in 5 of 6 forced-failure modes, exit 1; `isolate.sh` `FAIL_CLOSED` 6/6 + positive control, exit 0; four mutants each red in the mode they break (`evidence/crit29-*.txt`, `evidence/isolation-check-run.txt`) |
| M3 | stale tally carried forward (round 19, L1) | "155 round-19 transcripts" (lesson :124) vs the 154-file receipt; "5/13 name S096" (SCORECARD :1167, lesson :108, LOG :1324) vs 6/13 first-matching / 8/13 any-matching line; "the ten old OM10 assertions" (SCORECARD :1225) vs nine labeled occurrences, eight distinct | criterion 10 existed; no checker read the sentences | applied criterion 10 (no new number): `tally-check.py tally-claims.json` prints MISMATCH for all five registered round-19 statements (exit 1); the round-20 correction sentences are its green entries |
| M4 | marker missing from output (round 19) | round-19 tool docstring :41-50 says "reported as a lead"; its finding rows carry no marker (w1 ScoutRuleBMap, RevengeRuleBIntent: the marker was lost between the round-18 draft and the merge) | round-19 w2 CriticC3W2 saw it (lesson round-19 M14) but no check failed on it | every row now carries `evidence: observed|lead`; the counter reads a row without the key as observed, so an unmarked lead fails every L case (1/18 at `1f7f995`) |
| M5 | restatement (round 20, L1 pre-registration) | registered criterion 30 "re-derive stated counts" restated criterion 10 (`QUALITY.md:16`); the screen checked only 24/27/28 | w1 CriticC2Inflation, RevCriterion30, ConnCriteriaFleet | withdrawn before any after-measurement (SCORECARD "Round-20 pre-measurement corrections"); rule kept: the restatement screen reads all numbered criteria, not the recent ones |
| M6 | unrun check (round 20, seat + L1) | TwRuleB delivered v1 and v2 without running any suite (it read the host's "never verify" rule over its item); L1's integration run found `UnboundLocalError` on JS eval cells (exit 2) in `round-17/hardening eval-js-unparsed-clean` and `r19-bashcvar js-cell-separate-kernel-clean` | L1 integration (11 suites run before landing) | one-line fix (`env = bindings = None`), both cases green at `28c6837`; wave-2 items that write code say explicitly that running the named checks is part of the item |
| M7 | write scope (round 20, wave context) | `git clone <lane> /tmp/...` leaves `origin` = the lane; a replica `git push` moved the origin's master (w1 SentinelPause20 H2); seats ran push experiments | w1 SentinelPause20 | no lane ref moved except by `jj-lane.sh` (`git for-each-ref`: master and origin/master at L1 commits only); wave-2 context requires `git remote remove origin` right after cloning and VCS experiments in a fresh `git init` repo |
| M8 | overfit channel (round 20, seats) | case authors CaseWrapperCrossCell and CasePureCallables messaged the tool author TwRuleB about their expectations before the suite landed | L1 reading of seat reports | recorded; the suite was assembled by contract before any tool result was read (`assemble-suite.py`), and the held-out set plus the corpus diff are the out-of-suite evidence |
| M9 | recall traded for precision, unseen by a thin recall guard (round 20, L1 repair `28c6837`) | w2 AdvRecallShapes: 49 certain real-execution shapes (thread targets, `asyncio.run(coro())`, decorators, returned closures, dunders, inline lambdas, `importlib` alias) reported by `9c54c56` and `1f7f995`, silent at `28c6837` with no row and no counter; AdvDepth/AdvLeadMarks add starred, lambda and scheduled-coroutine shapes | none at landing — every registered guard passed (`tw-recall.py` covers 6 incident lines; the precision legs bound what a detector adds, not what it drops); w2 AdvRecallShapes | v3 `3610e3e` sweeps every reached-but-unfollowed visible body as `lead`; `a2/a2-guards.py` `recall_lost` 52 at `28c6837` → 0 at `3610e3e` and at `a8960de` (`a2/evidence/guards-*.txt`); QUALITY attempt-2 note queues a removal-side criterion for round 21 |
| M10 | unbounded expansion (round 20, L1 repair) | w2 CorpusRuntime: `KaidokuR19.EvidenceSecurity-3.jsonl` 30 s vs 0.07 s; a self-recursive helper costs ~N⁴ (`depth < 4`, re-expanded per call) | w2 CorpusRuntime (the 200-largest sample alone missed it) | recursion guard (a helper being followed is never re-followed) and a 2000-follow budget per cell; `a2/fixtures/hang-selfrec-40` 54.764 s → 0.036 s, `hang-mutual-24` 6.754 s → 0.049 s; the corpus file 25.85 s → 0.062 s (L1 timing, 2026-10-21) |
| M11 | new crash surface (round 20, L1 repair) | w2 AdvCrash: recursive `eager_calls` and helper-body scans raise `RecursionError` at ~half the depth `1f7f995` survives; exit 2 replaces a findings/clean verdict in 13 committed fixtures | w2 AdvCrash, RevToolDiffEval | iterative eager walk plus a 512 MiB / 50,000-frame scan thread; `crash_flip` 13 → 0 (the 3 remaining exit-2 files also exit 2 at `1f7f995`: parity) |
| M12 | option-value collision (round 20, L1 repair) | `sub_verb` restarted at the first token spelling the verb: `jj -R git --ignore-working-copy git push` and `jj -R bookmark … bookmark create` measured as writes, unflagged (w2 RevToolDiffVcs P1) | w2 RevToolDiffVcs | subcommand anchored at the located verb index; `a2/fixtures/jj-R-*` red at `28c6837`, green at `3610e3e` and `a8960de` |
| M13 | registration after a developed repair (round 20, attempt 2, L1) | the attempt-2 SCORECARD registration (`6a7d9ca`) was written after a sandbox draft had been measured; its populations predate the draft (attempt-1 commits, nine fixtures written first) and the text says so | L1 self-report | rule for round 21: commit the registration and before-receipts before opening the tool file; not shown able to fail (process) |
| M14 | coordinator lost before the report (round 20, attempt 1) | `.ufo/watchdog.log:548` `lane-dead-no-report mado round=20`; attempt 1 left `f8576f7`, `ed4bf22`, `38d1b36` and 161 seat reports (w1 85/85, w2 76/78; `SentinelPostWaveScan`, `ConnConsumers` dead), no SCORECARD verdicts for wave 2 | watchdog | recovery coordinator MadoR20Recovery reused the committed work after re-running every counter it cites at `a8960de` (no attempt-1 number is cited without a re-run) |
| M15 | an exemption widened by v3 hid a real write (round 20, attempt 2, L1) | v3 `3610e3e` read git short clusters letter by letter; in the unparsed segment `git -C $C checkout -q --detach 6cec83aed; bash -c 'git grep -ohE …'` (`W3ReviewLore.jsonl:119`) the next command's `-ohE` gave an `-h`, so a real checkout read as usage | the removal-side corpus diff from `28c6837` (`a2/evidence/corpus-diff-28c6837-vs-3610e3e.json`, `unmatched_base_rows_in_retained_calls`) — not the precision suite, the a2 guard or any selftest | v3.1 `a8960de`: no help/dry-run/`--ignore-working-copy`/installer-help exemption in an unparsed segment; the row is back (`corpus-diff-28c6837-vs-a8960de-classified.txt` no longer lists it); every remaining lost row is classed (3 installer `--help`, 1 `push -nv` dry run, 1 pure `heapq` lead) |

## Gate

Candidates opened 2026-10-20 (fetch receipts under `.ufo/waves/round-20/fetch/<seat>/`,
bodies digest-only): git v2.56.0 docs and source (tag → `a0189536…`), jj v0.45.1 source
(lightweight tag `7c41cdeb…`, equal to the host binary's build id), CPython v3.14.8 docs
(tag → `8e6e75d9…`), util-linux v2.42.4 (→ `d76cbf8f…`), bash 5.3 (`b8c60bc9…`),
man-pages 6.16. Admit tag- or commit-pinned raw files whose version equals the host's
installed tool; reject tree/HTML pages as anchors (S102 points at raw `git.c`, not the
tree page, per w1 ConnSourcesOverlap). Not rowed: CPython `simple_stmts.rst` (overlaps
S111), `functools.rst`, `dataclasses.rst`, `compound_stmts.rst` (seat probes only), jj
v0.38.0 files (ScoutCorpusVcsNonWrites; not the host version).

- GATE | S099 | https://raw.githubusercontent.com/git/git/v2.56.0/Documentation/git-commit.adoc | 2026-10-20 | `git-commit.adoc:379-380` "Do not create a commit, but show a list of paths that are to be committed" (16 words; the sentence continues); `:218-221` "-n … --no-verify … Bypass the `pre-commit` and `commit-msg` hooks" | sha256 `ec670cfa…` | admit (w1 SrcGitCommitDoc)
- GATE | S100 | https://raw.githubusercontent.com/git/git/v2.56.0/Documentation/git-add.adoc | 2026-10-20 | `:67-70` "Don't actually add the file(s), just show if they exist and/or will be ignored." (14 words) | `42089b80…` | admit (w1 SrcGitAddPushDoc)
- GATE | S101 | https://raw.githubusercontent.com/git/git/v2.56.0/Documentation/git-push.adoc | 2026-10-20 | `:161-163` "Do everything except actually send the updates." (7 words) | `b68851f8…` | admit; limit: the pre-push hook still runs
- GATE | S102 | https://raw.githubusercontent.com/git/git/v2.56.0/git.c | 2026-10-20 | `git.c:762` "Turn \"git cmd --help\" into \"git help --exclude-guides cmd\"" (9 words) | per-file sha256 in the receipts | admit (w1 SrcGitHelpSource)
- GATE | S103 | https://raw.githubusercontent.com/jj-vcs/jj/v0.45.1/cli/src/cli_util.rs | 2026-10-20 | `command_error.rs:1113-1115` "DisplayHelp \| DisplayVersion => { write!(ui.stdout(), …); return Ok(0);" (help returns before any workspace load) | `ee1eb31d…` | admit (w1 SrcJjHelp)
- GATE | S104 | https://raw.githubusercontent.com/jj-vcs/jj/v0.45.1/cli/src/commands/git/push.rs | 2026-10-20 | `push.rs:231` "Only display what will change on the remote" (8 words) | `213469e3…` | admit; limit: the working copy is snapshotted first (w1 CaseDryRunBash, CaseHelpDryRunEval measured +1 op)
- GATE | S105 | https://raw.githubusercontent.com/python/cpython/v3.14.8/Doc/builtins/functions.rst | 2026-10-20 | `:868-869` "Return a new frozenset object, optionally with elements taken from iterable." (11 words) | `f1b72170…` | admit; `Doc/library/functions.rst` is 404 at this tag (w1 SrcPyBuiltins)
- GATE | S106 | https://raw.githubusercontent.com/python/cpython/v3.14.8/Doc/library/collections.rst | 2026-10-20 | `:461-462` "Returns a new deque object initialized left-to-right (using append) with data from iterable." (14 words) | `be2f90d1…` | admit
- GATE | S107 | https://raw.githubusercontent.com/python/cpython/v3.14.8/Doc/library/shlex.rst | 2026-10-20 | `:39` "Concatenate the tokens of the list split_command and return a string." (11 words) | `819c6e6f…` | admit (w1 SrcPyShlex)
- GATE | S108 | https://raw.githubusercontent.com/python/cpython/v3.14.8/Doc/library/subprocess.rst | 2026-10-20 | `:43` "Run the command described by args." (6 words) | `05cd782c…` | admit; keyword `args=` binds the same slot (seat stub-Popen probe)
- GATE | S109 | https://raw.githubusercontent.com/util-linux/util-linux/d76cbf8f13e65ff657344f7f6a90042cf755ba59/sys-utils/unshare.1.adoc | 2026-10-20 | `:132` "mapped to the superuser UID and GID … mounting filesystems in the mount namespace" (13 words) | per-file sha256 in the receipts | admit (w1 SrcUnshare)
- GATE | S110 | https://cgit.git.savannah.gnu.org/cgit/bash.git/plain/doc/bashref.texi?h=bash-5.3 | 2026-10-20 | `:5940-5941` "part of any command executed in a && or \|\| list except the command following the final && or \|\|" (20 words) | `f3d37d57…` | admit (w1 SrcBashErrexit; five-way byte agreement incl. the release tarball member)
- GATE | S111 | https://raw.githubusercontent.com/python/cpython/v3.14.8/Doc/reference/executionmodel.rst | 2026-10-20 | `:140-142` "The global namespace is searched first. If the names are not found there, the builtins namespace is searched next." (19 words; module-level code only — a function-local `del` raises UnboundLocalError, `:122-124`) | `11f99f83…` | admit (w1 CaseShadowing: `del` of a shadowing name restores the builtin)
- GATE | S112 | https://git.kernel.org/pub/scm/docs/man-pages/man-pages.git/plain/man/man7/user_namespaces.7?h=man-pages-6.16 | 2026-10-20 | `:277-280` "Holding CAP_SYS_ADMIN within the user namespace that owns a process's mount namespace allows that process to create bind mounts" (19 words) | per-file sha256 in the receipts | admit (w1 SrcUnshare)

Status/recheck/used-by changes, old→new: none on existing rows. New rows S099–S112 enter
`mined`, recheck `on-release` (S112 `180d`), used-by
`corpus/knowledge/tripwire-precision-r20.md`. Rows 98 → 112 (tier A 91 → 105; mined 81 →
95) — `git show REV:corpus/SOURCES.md | grep -c '^| S[0-9]'` and the tier/status columns
parsed per row at `1f7f995` and the round tip, 2026-10-20 (w2 RerunCensus reproduced all
three; census `validate` exit 0, W04 warnings only).

Gate caveats from wave 2 (w2 ReopenUnshare, ReopenGitSource, ReopenJj): the host has
man-pages **6.19** (file bytes of its package `desc`), not 6.16 — S112's 6.16 text is
unchanged in 6.19 apart from headers, so the row stands but it does not meet the
"version equals the host's installed tool" admission wording above; S112's capability
rule holds without `unshare --keep-caps` (with it, a non-root-mapped payload keeps
CAP_SYS_ADMIN and can mount); S102's `-h` clause does not cover a git **shell alias**,
which prints its definition and then runs on a lone `-h`; S103's `jj help` is dispatched
to `cmd_help` (not answered by clap), which loads no workspace — the outcome (no
snapshot) stands; the knowledge note's mechanism wording was still the clap one at
`38d1b36` and is corrected in attempt 2 (its §2 now splits `-h`/`--help` from `jj help`).

Attempt 2 (2026-10-21, L1 MadoR20Recovery; receipts `.ufo/waves/round-20/fetch/A2Sources/
receipts.jsonl`, bodies digest-only; tag `v3.14.8` → `992560c2…` peeled `8e6e75d9…`, the
same pin as S105–S108/S111). Three candidates opened, three admitted, none rejected; the
question was which stdlib callables can turn a literal argv into a process (w2
AdvPureShapes showed the five-module allowlist made 24 pure callables leads):

- GATE | S113 | https://raw.githubusercontent.com/python/cpython/v3.14.8/Doc/library/os.rst | 2026-10-21 | `:4419-4422` "These functions may be used to create and manage processes." (10 words) | sha256 `2d0f2892…` | admit: the process side of the v3 purity split
- GATE | S114 | https://raw.githubusercontent.com/python/cpython/v3.14.8/Doc/library/json.rst | 2026-10-21 | `:260-266` "Serialize *obj* to a JSON formatted :class:`str` using this :ref:`conversion table <py-to-json-table>`." (12 words) | sha256 `0cfbe94c…` | admit: replaces the S106/S107 citation for `json.dumps`, whose bodies never name it (w2 ScribeTrendDraft)
- GATE | S115 | https://raw.githubusercontent.com/python/cpython/v3.14.8/Lib/subprocess.py | 2026-10-21 | `:583-586` "Translate a sequence of arguments into a command line string" (10 words) | sha256 `7fa4af83…` | admit: the one `subprocess` formatter, exempt by exact path

Status/recheck/used-by changes, old→new: none on existing rows. New rows enter `mined`,
recheck `on-release`, used-by `corpus/knowledge/tripwire-precision-r20.md`. Rows 112 →
115 (tier A 105 → 108; mined 95 → 98): `git show REV:corpus/SOURCES.md | grep -c '^| S[0-9]'`
at `38d1b36` and the round tip; census `validate` exit 0 at both ends
(`.ufo/waves/round-20/evidence/census-start.txt`, `a2/evidence/census-end.txt`).

## Corrections to round 19 (append-only; closure R19-V1..V6)

- R19-V1: round 19's C1 target ≥ 21/29 was missed (20/28) and stays missed; recording
  R18-V2 under criterion 24 did not convert it. Round 20's calibration target is its own
  pre-registration (`e629f73`) as corrected before measurement.
- R19-V2: over the 13-file `fresh-pins.py` set at `b435568` (unchanged at `7b4839d`,
  `1f7f995`) S096 is **8/13 on any matching line** and **6/13 on the first matching line**;
  the five files with no S096 on a qualifying line cite S090 only:
  `arc-synthesis.md:392`, `closeout-r11.md:299`, `config-health-report-r3.md:1009`,
  `waybar-walker-plane.md:479`, `waybar-walker-semantics.md:467`. The "5/13" was RerunC2's
  cited-as-evidence reading at `01b8094`, not a token count. The round-19 promise that
  every file cite the new host-byte row is unmet. S096 is provenance (host bytes), not
  behaviour: no walker fact was re-measured on 2.17.2.
- R19-V4: the post-wave scan receipt `round-19/evidence/final/tripwire-seat-scan.txt`
  lists **154** files (not 155). The first `inns.sh` failed open: its mount setup failed
  and the payload still ran the real `hyprctl probe`. The scanner did not detect it —
  a script written and then run is outside what it parses — so its captured-by is
  `none (seat self-report)`; host state after it was not independently measured.
- R19-V5: OM10 at `9c54c56` had **nine labeled assertion occurrences, eight distinct**
  (not ten), replaced by OM10A six and OM10B eight (`tally-check.py selftest-labels`).
- R19-V6: round-19 wave 1 had 86 members and **25** without a report (registry member
  names joined to report file names; `TwMerge` is a report without a member) — the
  dead seats stay uncredited. Every round-20 item and wave context names absolute lane
  paths; provider recovery is not claim evidence.

## Decisions (L1, with the seats that argued each)

- Lead rows stay inside `findings` (exit 1) with `evidence: lead` and verdict counts
  (w1 RevLeadExitSemantics): a separate list would read 5/6 on the unchanged recall
  counter and let a demoted false positive pass the precision counter.
- E4 amended by measurement (CaseDryRunBash, CaseHelpDryRunEval, CaseHelpBash,
  ScoutJjHelpEmpirical, SrcJjHelp, SrcGitHelpSource): plain `jj git push --dry-run`
  snapshots and stays a write; `jj --ignore-working-copy git push --dry-run` does not;
  git `-h`/`--help` as a flag among options prints usage; `jj describe -m --help` is
  refused by jj (no op); `git commit -m --help` commits.
- Kept as findings although a case wants clean: `jj $c --help` (TwVcsHelp measured that a
  user alias with `--help` runs the aliased command) and `Runner().run([...])` (a visible
  method body that spawns its argument is a true detection; the case recorded a stated
  miss). Both stay failing cases in the pinned suite rather than edited after the
  result was seen.
- Eight round-19 suite cases changed from clean to a finding, each with an `r20_edit`
  reason in its `expected.json` (class bodies execute at definition; literal module
  bindings reach visible helpers; a call before its def is a lead; vararg and redefined
  helpers). No case lost a finding; two lead cases gained the `lead` marker.
