# JjIncidentScan — live-lane VCS writes exist in three surfaces; the eval-argv surface owns the `.jj` birth and survives the backout

Read-only scan of OMP transcripts under `/home/vgpnk/.omp/agent/sessions/-Projects-shokunin`
for assistant tool calls that invoke `jj` or `git` write verbs against the live
`/home/vgpnk/Projects/shokunin/mado-shokunin` lane. No lane working-tree file outside this
report was changed; no `jj`, `git` write, or host command was run. Scratch scanner lives in `/tmp/r19_jjscan2.py`; raw hit dump in
`/tmp/r19_jj_hits2.jsonl`. Paths below are relative to the session root unless absolute.

## Verdict

1. **The lane's `.jj` did not appear idly.** An **eval Python pilot** at
   `2026-10-19T20-36-43-523Z_01a155e1-7d83-74e9-8383-9ee7c15d7c99.jsonl:1725`
   (`2026-10-19T23:38:42Z`) ran `jj git init --colocate` plus three `jj config set --repo`
   commands in the live mado repo via `subprocess.run(..., cwd=repo)`. `[INFERENCE]` this is
   F17's origin: it is the only init command targeting the live repo before the audit-era
   op-log init timestamp, and it is invisible to any `bash arguments.command` matcher.
2. **The audit's "three `jj log` runs" is a floor, not a count.** The live lane saw at least
   **20 non-helper jj invocations**: 5 mutating repo writes (init + four repo `config set`) and
   15 read/snapshot calls. Three match the audit op-log entries by local-time conversion, now
   mapped to transcript lines (below).
3. **The 15:18Z "backout" did not de-colocate the lane.** At
   `2026-10-20T15:18:07.972Z` one command deleted `refs/jj`, removed `.jj` and the jj repo
   config, ran `git reset -q`, then called `inline.sh closure mado`; that wrapper's
   `lane_vcs_init` re-ran `jj-lane.sh init` and `.jj` was re-created at
   `2026-10-20T15:18:08.062Z` (90 ms later). Current `.jj` is a **helper-born** repo, not the
   audit-era one.
4. **Plain git writes are mostly a round 13–17 phenomenon, with two eval-surface exceptions.**
   70 `git` write invocations (add 27, commit 26, push 15, pull 1, reset 1) across 29 bash call
   lines, 04:46–15:18Z; separately the eval surface merged into the live lane at `01:04:36Z`
   and issued a push of it to `origin` at `01:09:41Z` (lines 2422/2472). After the backout there are no
   direct `git` write verbs to the lane in any transcript; every later write is
   `jj-lane.sh commit` (9 commits) or `jj-lane.sh state` (11 reads).
5. **`TwVcsClass` needs four target-resolution axes** that a literal-path regex misses:
   eval argv lists, tool-`cwd`, loop/shell variables, and helper-subcommand semantics. Real
   examples for each are in the tables.

## Method and counts

- Corpus: **4,310** `.jsonl` transcripts modified on/after 2026-10-19, **3,547,903,434 bytes**
  total; every session's recorded `cwd` is `/home/vgpnk/Projects/shokunin`.
- Parsed **209,329** assistant `toolCall` records. Shell text came from `bash`/`shell`/
  `process` `arguments.command`; eval text from `arguments.code` (`!` lines and literal
  `subprocess` argv lists / `await tool.bash` calls).
- Shell parsing is quote- and heredoc-aware. Targets were resolved through `cd`, `git -C`,
  `git --git-dir`, `GIT_DIR`, and simple `$VAR` assignments; a hit counts only when the
  resolved path is the lane or a subdirectory of it. `/tmp`, `/fast/scratch`, `.tower/jj-probe`,
  and other lanes were excluded.
- First lexical pass produced 274 candidate rows; the quote-aware pass reduced this to
  **52 bash call lines / 96 invocations** plus **5 call lines** whose target is outside the
  resolved shell inventory (eval argv lists and one loop variable) below. The drop is
  mostly quoted `grep` patterns and heredoc prose (`'git add|jj file track'`, `'jj log'`) that a
  word-boundary regex misreads as commands.
- `effect` classification: `jj` reads without `--ignore-working-copy` are marked **SNAPSHOT**
  because jj snapshots the working copy and writes an op; `jj op log --ignore-working-copy` is a
  pure read. Helper `state` is pure git (documented in `scripts/hyaku/jj-lane.sh:155`), helper
  `commit`/`init` are writes.

| class | invocations | call lines | notes |
|---|---|---|---|
| git write verbs (bash) | 70 | 29 | add 27, commit 26, push 15, pull 1, reset 1 |
| `jj-lane.sh` helper | 20 | 19 | state 11 (read), commit 9 (write) |
| `jj` direct (bash) | 6 | 5 | log 3, op log 2, file annotate 1 |
| `jj` via eval argv | 12 | 2 | 1725/1728: init 1 + config set 4 (write); 7 read/snapshot |
| `jj` via bash loop var | 2 | 1 | 218: `log` snapshot + `config list` read |
| eval `git merge` | 1 | 1 | verb outside the requested set; included as adjacent mutation |
| eval `git push` loop | 1 loop | 1 | 21 lane repos; mado path/remote confirmed by inventory artifact |

## Incident timeline

All times UTC; JjAuditMado printed local `-0300`, so its `20:38:49` = `23:38:49Z`,
`04:24:40` = `07:24:40Z`, `10:21:51` = `13:21:51Z`.

| # | when | event | transcript evidence |
|---|---|---|---|
| 1 | 2026-10-19T23:38:42Z | eval pilot initializes colocation in mado (`jj git init --colocate`, then 3 `config set`, then status/log/diff), gate selftest before/after | `…01a155e1…jsonl:1725` |
| 2 | 2026-10-19T23:38:57Z | eval pilot reruns mado-only `config get`, `config set immutable_heads`, status/log/diff | `…01a155e1…jsonl:1728` |
| 2a | 2026-10-20T01:04:36Z | eval merges remote into live mado (`merge --no-ff --no-commit`) | `…01a155e1…jsonl:2422` |
| 2b | 2026-10-20T01:09:41Z | eval issues a push of live mado `master` to `origin` (inventory `push_remote`); success not re-checked | `…01a155e1…jsonl:2472` |
| 3 | 2026-10-20T05:41:05Z | `jj log` + `jj file annotate` in lane (snapshot side effect) | `MadoR14/MadoR14.AttackCoverage.jsonl:42` (tool `cwd` = lane) |
| 4 | 2026-10-20T05:43:06Z | `jj --ignore-working-copy op log` (pure read) | `MadoR14/MadoR14.Safety.jsonl:62` |
| 5 | 2026-10-20T05:47:50Z | `jj --ignore-working-copy op log` (pure read) | `MadoR14/MadoR14.Safety.jsonl:118` |
| 6 | 2026-10-20T07:24:40Z | `jj log -r '@|@-|@--'` **= audit op entry 04:24:40 local** | `MadoR15/MadoR15.AttackMetric.jsonl:37` (tool `cwd` = lane) |
| 7 | 2026-10-20T07:28:39Z | `jj --no-pager -R . log -r '@'` (snapshot) | `MadoR15/MadoR15.AttackSource.jsonl:122` |
| 8 | 2026-10-20T13:21:50Z | loop `for d in tameshi mado; do (cd $d-shokunin && jj … log; jj … config list --repo)` **= audit op entry 10:21:51 local** | `…01a15963…jsonl:218` |
| 9 | 2026-10-20T15:18:07Z | backout: delete `refs/jj`, `rm -rf .jj` + jj config, `git reset -q`, then `inline.sh closure mado` | `…01a15963…jsonl:731` |
| 10 | 2026-10-20T15:18:08Z | helper re-init: `.jj` mtime `15:18:08.072Z`, `config-id` `15:18:08.082Z`; earliest op `15:18:08.065Z` | filesystem stat, read-only |
| 11 | 2026-10-20T16:59:52Z | last helper commit; op store latest mtime `16:59:54.463Z` (68 ops total) | `MadoR19.jsonl:89`; filesystem stat |

Current on-disk state (read as bytes only):

```
.jj                              2026-10-20T15:18:08.072Z
.jj/repo/config-id               2026-10-20T15:18:08.082Z  (0c6bba4313e6b57d66ba)
.jj/repo/store/git_target        2026-10-20T15:18:08.062Z  (../../../.git)
.jj/working_copy/tree_state      2026-10-20T16:59:52.846Z
ops                             68 files, first 15:18:08.065Z, last 16:59:54.463Z
```

Two op files sampled with `strings` (`0241dad2…`, `42cb2d1a…`) both carry
`@jj --config 'snapshot.auto-track="none()"' git init --colocate .B` — the exact argv shape of
`jj-lane.sh cmd_init` (`scripts/hyaku/jj-lane.sh:420`). `hyaku.env:10` is `HYAKU_VCS=jj`, and
`scripts/hyaku/inline.sh:38-40,90,145` call `lane_vcs_init` on dispatch/closure; the backout's own
`inline.sh closure mado` therefore re-initialized the lane. `[INFERENCE]` from code + sub-100 ms
mtime alignment; no live command was run to re-test.

## Per-hit inventory

Each row is one assistant tool-call line; `invocations` lists every matching invocation parsed
from that line. Commands are redacted and excerpted to ≤200 characters; no full transcript line
is copied. When a line carries multiple invocations, the excerpt shows the **last** matching one,
so the `invocations` column is the authoritative list. `session-root` means the transcript is the
top-level session file (no seat subdir).

Helper status per table: **A** and **D** contain no `jj-lane.sh` invocation; **B** lists helper
invocations (`state` = read, `commit` = write; its row 1 also carries the surrounding `git reset`,
shown in `invocations`); **C** is plain `git`, except row 29, which also invokes
`jj-lane.sh state`. `effect` is the mutating/read verdict.

### A. jj invocations in the live lane (bash)

| # | transcript:line | ts (UTC) | seat | invocations | effect | command excerpt (≤200 chars) |
|---|---|---|---|---|---|---|
| 1 | `2026-10-20T01-48-55-258Z_01a156ff-505a-7798-99c2-b47895c874f4/MadoR14/MadoR14.AttackCoverage.jsonl:42` | 2026-10-20T05:41:05 | `MadoR14.AttackCoverage` | jj log, jj file annotate | SNAPSHOT (`jj file annotate`, no --ignore-working-copy); SNAPSHOT (`jj log`, no --ignore-working-copy) | `jj file annotate .ufo/waves/round-13/w1/globals.json 2&gt;&1 \| cut -c1-80 \| sort -u -k1,1 \| cut -c1-40 \| uniq \| sed -n 1,3p` |
| 2 | `2026-10-20T01-48-55-258Z_01a156ff-505a-7798-99c2-b47895c874f4/MadoR14/MadoR14.Safety.jsonl:62` | 2026-10-20T05:43:06 | `MadoR14.Safety` | jj op log | read (`jj op log`) | `jj --ignore-working-copy op log --no-graph -n 6 -T 'id.short() ++ " " ++ time.start() ++ " " ++ description ++ "\n"' 2&gt;&1 \| head -12; pacman -Qi wlr-protocols 2&gt;&1 \| grep -E '^(Name\|Version\|Install Da` |
| 3 | `2026-10-20T01-48-55-258Z_01a156ff-505a-7798-99c2-b47895c874f4/MadoR14/MadoR14.Safety.jsonl:118` | 2026-10-20T05:47:50 | `MadoR14.Safety` | jj op log | read (`jj op log`) | `jj --ignore-working-copy op log --no-graph -n 4 -T 'id.short() ++ " " ++ time.start() ++ " " ++ description ++ "\n"' 2&gt;&1; git --version; ls -ld /tmp/hl-src-ahn /tmp/wlr-protocols /tmp/ac14 /tmp/srcsa` |
| 4 | `2026-10-20T01-48-55-258Z_01a156ff-505a-7798-99c2-b47895c874f4/MadoR15/MadoR15.AttackMetric.jsonl:37` | 2026-10-20T07:24:40 | `MadoR15.AttackMetric` | jj log | SNAPSHOT (`jj log`, no --ignore-working-copy) | `jj log -r '@\|@-\|@--' --no-graph 2&gt;/dev/null \| cut -c1-200; git log --oneline -5` |
| 5 | `2026-10-20T01-48-55-258Z_01a156ff-505a-7798-99c2-b47895c874f4/MadoR15/MadoR15.AttackSource.jsonl:122` | 2026-10-20T07:28:39 | `MadoR15.AttackSource` | jj log | SNAPSHOT (`jj log`, no --ignore-working-copy) | `jj --no-pager -R . log -r '@' --no-graph -T 'commit_id ++ " " ++ description.first_line()' 2&gt;/dev/null; git -C . log --oneline -3` |

### B. jj-lane.sh helper invocations

| # | transcript:line | ts (UTC) | seat | invocations | effect | command excerpt (≤200 chars) |
|---|---|---|---|---|---|---|
| 1 | `2026-10-20T12-57-31-587Z_01a15963-70c3-7390-a1b4-7911b9506d07.jsonl:731` | 2026-10-20T15:18:07 | `session-root` | git reset, jj-lane.sh state | read (helper state) | `jj-lane.sh state $M; git -C $M status --porcelain \| cut -c1-2 \| sort \| uniq -c` |
| 2 | `2026-10-20T12-57-31-587Z_01a15963-70c3-7390-a1b4-7911b9506d07/ClosureMadoR17.jsonl:30` | 2026-10-20T15:19:03 | `ClosureMadoR17` | jj-lane.sh state | read (helper state) | `jj-lane.sh state /home/vgpnk/Projects/shokunin/mado-shokunin; echo "rc=$?"; git -C $L status --porcelain; echo ---; git -C $L ls-remote origin refs/heads/master; git -C $L log --format='%h %an &lt;%ae&gt; %` |
| 3 | `2026-10-20T12-57-31-587Z_01a15963-70c3-7390-a1b4-7911b9506d07/ClosureMadoR17.jsonl:139` | 2026-10-20T15:28:10 | `ClosureMadoR17` | jj-lane.sh commit | MUTATING (helper commit) | `jj-lane.sh commit /home/vgpnk/Projects/shokunin/mado-shokunin --as protocol -m "round-17 verifier spot-check (integrator, hyaku): non-author admit/reject" -- corpus/lessons/round-17-verifier-spotcheck` |
| 4 | `2026-10-20T12-57-31-587Z_01a15963-70c3-7390-a1b4-7911b9506d07/ClosureMadoR17.jsonl:142` | 2026-10-20T15:28:20 | `ClosureMadoR17` | jj-lane.sh state | read (helper state) | `jj-lane.sh state $L; date -u +%Y-%m-%dT%H:%M:%SZ; sed -n 1,60p /home/vgpnk/Projects/shokunin/scripts/hyaku/append-closure.py \| grep -n 'def \\|required\\|verdict\\|trend' \| head -30` |
| 5 | `2026-10-20T12-57-31-587Z_01a15963-70c3-7390-a1b4-7911b9506d07/MadoR18.jsonl:22` | 2026-10-20T15:30:45 | `MadoR18` | jj-lane.sh state | read (helper state) | `jj-lane.sh state /home/vgpnk/Projects/shokunin/mado-shokunin; git -C mado-shokunin status --porcelain \| head -30; grep -n "mado" .ufo/watchdog.log \| tail -5` |
| 6 | `2026-10-20T12-57-31-587Z_01a15963-70c3-7390-a1b4-7911b9506d07/MadoR18.jsonl:102` | 2026-10-20T15:34:53 | `MadoR18` | jj-lane.sh commit | MUTATING (helper commit) | `jj-lane.sh commit /home/vgpnk/Projects/shokunin/mado-shokunin --as mado -m "round-18: pre-registration (claims C1-C3, baselines)" -- SCORECARD.md .ufo/waves/round-18/evidence/census-start.txt` |
| 7 | `2026-10-20T12-57-31-587Z_01a15963-70c3-7390-a1b4-7911b9506d07/MadoR18/MadoR18.RevJjTrialFindings.jsonl:9` | 2026-10-20T15:40:00 | `MadoR18.RevJjTrialFindings` | jj-lane.sh state | read (helper state) | `jj-lane.sh state /home/vgpnk/Projects/shokunin/mado-shokunin 2&gt;&1; echo "RC=$?"` |
| 8 | `2026-10-20T12-57-31-587Z_01a15963-70c3-7390-a1b4-7911b9506d07/MadoR18.jsonl:235` | 2026-10-20T15:55:36 | `MadoR18` | jj-lane.sh commit | MUTATING (helper commit) | `jj-lane.sh commit /home/vgpnk/Projects/shokunin/mado-shokunin --as mado -m "round-18: wave-1 integration (frozen tripwire gate entry, gate rc fix + PIN re-cut, P3/P5 routes + S072-S095, QUALITY 24-26,` |
| 9 | `2026-10-20T12-57-31-587Z_01a15963-70c3-7390-a1b4-7911b9506d07/MadoR18.jsonl:258` | 2026-10-20T15:56:38 | `MadoR18` | jj-lane.sh commit | MUTATING (helper commit) | `jj-lane.sh commit /home/vgpnk/Projects/shokunin/mado-shokunin --as mado -m "round-18: receipts at 4c103b5 (measure before/after, tripwire re-cut r13-r16+anchor with producer header, frozen match/tampe` |
| 10 | `2026-10-20T12-57-31-587Z_01a15963-70c3-7390-a1b4-7911b9506d07/MadoR18.jsonl:297` | 2026-10-20T16:22:12 | `MadoR18` | jj-lane.sh state | read (helper state) | `jj-lane.sh state /home/vgpnk/Projects/shokunin/mado-shokunin; python3 - &lt;&lt;'EOF' import json,os d=json.load(open('.ufo/waves/round-18/w2/dispatch.json')) have=set(f[:-3] for f in os.listdir('.ufo/waves` |
| 11 | `2026-10-20T12-57-31-587Z_01a15963-70c3-7390-a1b4-7911b9506d07/MadoR18.jsonl:361` | 2026-10-20T16:25:11 | `MadoR18` | jj-lane.sh commit | MUTATING (helper commit) | `jj-lane.sh commit /home/vgpnk/Projects/shokunin/mado-shokunin --as mado -m "round-18: wave-2 integration (frozen hardening: reachability/unknown+dup keys/symlinked dir, failsafe pacman op; receipt-che` |
| 12 | `2026-10-20T12-57-31-587Z_01a15963-70c3-7390-a1b4-7911b9506d07/MadoR18.jsonl:400` | 2026-10-20T16:27:44 | `MadoR18` | jj-lane.sh commit | MUTATING (helper commit) | `jj-lane.sh commit /home/vgpnk/Projects/shokunin/mado-shokunin --as mado -m "round-18: final receipts at be886a3, lesson Gate (24/24 non-author re-opens) + M7/M8, SCORECARD results/capability/planned, ` |
| 13 | `2026-10-20T12-57-31-587Z_01a15963-70c3-7390-a1b4-7911b9506d07/MadoR18.jsonl:462` | 2026-10-20T16:47:14 | `MadoR18` | jj-lane.sh commit, jj-lane.sh state | MUTATING (helper commit); read (helper state) | `jj-lane.sh state /home/vgpnk/Projects/shokunin/mado-shokunin` |
| 14 | `2026-10-20T12-57-31-587Z_01a15963-70c3-7390-a1b4-7911b9506d07.jsonl:1133` | 2026-10-20T16:48:31 | `session-root` | jj-lane.sh state | read (helper state) | `jj-lane.sh state mado-shokunin` |
| 15 | `2026-10-20T12-57-31-587Z_01a15963-70c3-7390-a1b4-7911b9506d07/ClosureMadoR18.jsonl:22` | 2026-10-20T16:49:04 | `ClosureMadoR18` | jj-lane.sh state | read (helper state) | `jj-lane.sh state /home/vgpnk/Projects/shokunin/mado-shokunin; echo "porcelain:"; git -C $L status --porcelain; git -C $L log --format='%h %an %s' d9a5a18..refs/heads/master` |
| 16 | `2026-10-20T12-57-31-587Z_01a15963-70c3-7390-a1b4-7911b9506d07/ClosureMadoR18.jsonl:137` | 2026-10-20T16:53:34 | `ClosureMadoR18` | jj-lane.sh commit | MUTATING (helper commit) | `jj-lane.sh commit /home/vgpnk/Projects/shokunin/mado-shokunin --as protocol -m "round-18 verifier spot-check (integrator, hyaku): non-author admit/reject" -- corpus/lessons/round-18-verifier-spotcheck` |
| 17 | `2026-10-20T12-57-31-587Z_01a15963-70c3-7390-a1b4-7911b9506d07/ClosureMadoR18.jsonl:140` | 2026-10-20T16:53:40 | `ClosureMadoR18` | jj-lane.sh state | read (helper state) | `jj-lane.sh state $L; git -C $L status --porcelain; sed -n 1,40p /home/vgpnk/Projects/shokunin/scripts/hyaku/append-closure.py \| grep -n 'arg\\|usage\\|--' \| head` |
| 18 | `2026-10-20T12-57-31-587Z_01a15963-70c3-7390-a1b4-7911b9506d07/MadoR19.jsonl:18` | 2026-10-20T16:54:48 | `MadoR19` | jj-lane.sh state | read (helper state) | `jj-lane.sh state /home/vgpnk/Projects/shokunin/mado-shokunin; git status --porcelain; git log --oneline -8 master; ls; ls corpus corpus/lessons \| tail -40; grep -n "mado" /home/vgpnk/Projects/shokunin` |
| 19 | `2026-10-20T12-57-31-587Z_01a15963-70c3-7390-a1b4-7911b9506d07/MadoR19.jsonl:89` | 2026-10-20T16:59:52 | `MadoR19` | jj-lane.sh commit | MUTATING (helper commit) | `jj-lane.sh commit /home/vgpnk/Projects/shokunin/mado-shokunin --as mado -m "round-19: pre-registration (claims C1-C3, sub-axis rubrics, baselines, counters)" -- SCORECARD.md .ufo/waves/round-19/tw-rec` |

### C. git write verbs in the live lane (bash)

| # | transcript:line | ts (UTC) | seat | invocations | effect | command excerpt (≤200 chars) |
|---|---|---|---|---|---|---|
| 1 | `2026-10-20T01-48-55-258Z_01a156ff-505a-7798-99c2-b47895c874f4/MadoR13.jsonl:515` | 2026-10-20T04:46:14 | `MadoR13` | git add, git commit | MUTATING (git add); MUTATING (git commit) | `git -C /home/vgpnk/Projects/shokunin/mado-shokunin commit -m "round-13: protocol boundaries and exact-set census" -- LOG.md SCORECARD.md SKILL.md corpus/QUALITY.md corpus/README.md corpus/SOURCES.md c` |
| 2 | `2026-10-20T01-48-55-258Z_01a156ff-505a-7798-99c2-b47895c874f4/MadoR13.jsonl:530` | 2026-10-20T04:48:51 | `MadoR13` | git add, git commit, git push | MUTATING (git add); MUTATING (git commit); MUTATING (git push) | `git -C /home/vgpnk/Projects/shokunin/mado-shokunin push && git -C /home/vgpnk/Projects/shokunin/mado-shokunin rev-parse HEAD && git -C /home/vgpnk/Projects/shokunin/mado-shokunin status --porcelain` |
| 3 | `2026-10-20T01-48-55-258Z_01a156ff-505a-7798-99c2-b47895c874f4/CloseMadoR13.jsonl:197` | 2026-10-20T04:59:51 | `CloseMadoR13` | git add, git commit, git push | MUTATING (git add); MUTATING (git commit); MUTATING (git push) | `git -C /home/vgpnk/Projects/shokunin/mado-shokunin push` |
| 4 | `2026-10-20T01-48-55-258Z_01a156ff-505a-7798-99c2-b47895c874f4/MadoR14.jsonl:498` | 2026-10-20T06:03:28 | `MadoR14` | git add, git commit | MUTATING (git add); MUTATING (git commit) | `git -C /home/vgpnk/Projects/shokunin/mado-shokunin -c user.name=mado-shokunin -c user.email=mado@shokunin.local commit -m 'round-14: output-colour boundaries and regular-source policy' -- tools/mado-v` |
| 5 | `2026-10-20T01-48-55-258Z_01a156ff-505a-7798-99c2-b47895c874f4/MadoR14.jsonl:542` | 2026-10-20T06:10:29 | `MadoR14` | git add, git commit, git push | MUTATING (git add); MUTATING (git commit); MUTATING (git push) | `git -C /home/vgpnk/Projects/shokunin/mado-shokunin push && git -C /home/vgpnk/Projects/shokunin/mado-shokunin status --porcelain && git -C /home/vgpnk/Projects/shokunin/mado-shokunin rev-parse HEAD` |
| 6 | `2026-10-20T01-48-55-258Z_01a156ff-505a-7798-99c2-b47895c874f4/CloseMadoR14.jsonl:178` | 2026-10-20T06:21:01 | `CloseMadoR14` | git add, git commit, git push | MUTATING (git add); MUTATING (git commit); MUTATING (git push) | `git -C /home/vgpnk/Projects/shokunin/mado-shokunin push` |
| 7 | `2026-10-20T01-48-55-258Z_01a156ff-505a-7798-99c2-b47895c874f4/MadoR15.jsonl:319` | 2026-10-20T07:35:06 | `MadoR15` | git add, git commit | MUTATING (git add); MUTATING (git commit) | `git -C /home/vgpnk/Projects/shokunin/mado-shokunin commit -m "round-15: input diagnostic ladder and honest partial-upgrade stop" -- LOG.md SCORECARD.md SKILL.md corpus/README.md corpus/QUALITY.md corp` |
| 8 | `2026-10-20T01-48-55-258Z_01a156ff-505a-7798-99c2-b47895c874f4/MadoR15.jsonl:322` | 2026-10-20T07:35:13 | `MadoR15` | git push | MUTATING (git push) | `git -C /home/vgpnk/Projects/shokunin/mado-shokunin push` |
| 9 | `2026-10-20T01-48-55-258Z_01a156ff-505a-7798-99c2-b47895c874f4/MadoR15.jsonl:345` | 2026-10-20T07:38:09 | `MadoR15` | git add, git commit, git push | MUTATING (git add); MUTATING (git commit); MUTATING (git push) | `git -C /home/vgpnk/Projects/shokunin/mado-shokunin push && git -C /home/vgpnk/Projects/shokunin/mado-shokunin rev-parse HEAD && git -C /home/vgpnk/Projects/shokunin/mado-shokunin status --short` |
| 10 | `2026-10-20T01-48-55-258Z_01a156ff-505a-7798-99c2-b47895c874f4/CloseMadoR15.jsonl:154` | 2026-10-20T07:47:43 | `CloseMadoR15` | git add, git commit, git push | MUTATING (git add); MUTATING (git commit); MUTATING (git push) | `git -C /home/vgpnk/Projects/shokunin/mado-shokunin push` |
| 11 | `2026-10-20T01-48-55-258Z_01a156ff-505a-7798-99c2-b47895c874f4/MadoR16.jsonl:528` | 2026-10-20T08:59:59 | `MadoR16` | git add, git commit, git push | MUTATING (git add); MUTATING (git commit); MUTATING (git push) | `git -C /home/vgpnk/Projects/shokunin/mado-shokunin push` |
| 12 | `2026-10-20T01-48-55-258Z_01a156ff-505a-7798-99c2-b47895c874f4/MadoR16.jsonl:556` | 2026-10-20T09:01:48 | `MadoR16` | git add, git commit, git push | MUTATING (git add); MUTATING (git commit); MUTATING (git push) | `git -C /home/vgpnk/Projects/shokunin/mado-shokunin push` |
| 13 | `2026-10-20T01-48-55-258Z_01a156ff-505a-7798-99c2-b47895c874f4/MadoR16.jsonl:577` | 2026-10-20T09:04:36 | `MadoR16` | git add, git commit, git push | MUTATING (git add); MUTATING (git commit); MUTATING (git push) | `git -C /home/vgpnk/Projects/shokunin/mado-shokunin push && git -C /home/vgpnk/Projects/shokunin/mado-shokunin rev-parse HEAD && git -C /home/vgpnk/Projects/shokunin/mado-shokunin status --porcelain=v1` |
| 14 | `2026-10-20T12-57-31-587Z_01a15963-70c3-7390-a1b4-7911b9506d07/ClosureMadoR16.jsonl:95` | 2026-10-20T13:18:29 | `ClosureMadoR16` | git pull, git add, git commit, git push | MUTATING (git add); MUTATING (git commit); MUTATING (git pull); MUTATING (git push) | `git push -q && git rev-parse HEAD && git status -sb \| head -1 && git log -1 --format='%an %H'` |
| 15 | `2026-10-20T12-57-31-587Z_01a15963-70c3-7390-a1b4-7911b9506d07/MadoR17.jsonl:83` | 2026-10-20T13:56:28 | `MadoR17` | git add, git commit | MUTATING (git add); MUTATING (git commit) | `git commit -q -m "round-17: pre-register claims and census start" && git log --oneline -1` |
| 16 | `2026-10-20T12-57-31-587Z_01a15963-70c3-7390-a1b4-7911b9506d07/MadoR17.jsonl:209` | 2026-10-20T14:11:09 | `MadoR17` | git add, git commit | MUTATING (git add); MUTATING (git commit) | `git commit -q -m "round-17: bind rubric-V measure instrument before integration" && H=$(git rev-parse HEAD) && mkdir -p .ufo/waves/round-17/evidence && for r in 27cd06f $H; do python3 .ufo/waves/round` |
| 17 | `2026-10-20T12-57-31-587Z_01a15963-70c3-7390-a1b4-7911b9506d07/MadoR17.jsonl:223` | 2026-10-20T14:11:36 | `MadoR17` | git add, git commit | MUTATING (git add); MUTATING (git commit) | `git commit -q -m "round-17: tighten rubric-V instrument (exact surface line, pinned legacy, relevance, facet floor)" && git rev-parse --short HEAD && sha256sum .ufo/waves/round-17/measure.py && cat .u` |
| 18 | `2026-10-20T12-57-31-587Z_01a15963-70c3-7390-a1b4-7911b9506d07/MadoR17.jsonl:230` | 2026-10-20T14:11:52 | `MadoR17` | git add, git commit | MUTATING (git add); MUTATING (git commit) | `git commit -q -m "round-17 C2: sourced P6 idle/lock and P4 terminal documentary routes (S056-S070)" && H=$(git rev-parse HEAD) && echo $H && python3 .ufo/waves/round-17/measure.py $H &gt; .ufo/waves/roun` |
| 19 | `2026-10-20T12-57-31-587Z_01a15963-70c3-7390-a1b4-7911b9506d07/MadoR17.jsonl:248` | 2026-10-20T14:12:41 | `MadoR17` | git add, git commit | MUTATING (git add); MUTATING (git commit) | `git commit -q -m "round-17: wave-1 evidence receipts (recut, oracles, session index, schema census, measures)" && git rev-parse HEAD && sed -n 69,73p corpus/lessons/round-16-verifier-spotcheck.md && p` |
| 20 | `2026-10-20T12-57-31-587Z_01a15963-70c3-7390-a1b4-7911b9506d07/MadoR17.jsonl:254` | 2026-10-20T14:13:04 | `MadoR17` | git add, git commit | MUTATING (git add); MUTATING (git commit) | `git commit -q -m "round-17: label-check want-side mutant fixture" && python3 -I .ufo/waves/round-17/label-check.py; echo "exit=$?"` |
| 21 | `2026-10-20T12-57-31-587Z_01a15963-70c3-7390-a1b4-7911b9506d07/MadoR17.jsonl:278` | 2026-10-20T14:14:37 | `MadoR17` | git add, git commit | MUTATING (git add); MUTATING (git commit) | `git commit -q -m "round-17 C1: QUALITY 23 receipt-label criterion, R16-V1 erratum, label check red/green" && H=$(git rev-parse HEAD) && echo $H && python3 .ufo/waves/round-17/measure.py $H &gt; .ufo/wave` |
| 22 | `2026-10-20T12-57-31-587Z_01a15963-70c3-7390-a1b4-7911b9506d07/MadoR17.jsonl:293` | 2026-10-20T14:15:08 | `MadoR17` | git add, git commit | MUTATING (git add); MUTATING (git commit) | `git commit -q -m "round-17: pre-measurement corrections (lowest axis, instrument binding, C1/C3 pins, host pause fact)" && git rev-parse --short HEAD` |
| 23 | `2026-10-20T12-57-31-587Z_01a15963-70c3-7390-a1b4-7911b9506d07/MadoR17.jsonl:384` | 2026-10-20T14:50:30 | `MadoR17` | git add, git commit | MUTATING (git add); MUTATING (git commit) | `git commit -q -m "round-17 C3: post-hoc transcript tripwire capability, suites and real-transcript receipts" && git rev-parse HEAD && python3 .ufo/waves/round-17/measure.py HEAD &gt; .ufo/waves/round-17/` |
| 24 | `2026-10-20T12-57-31-587Z_01a15963-70c3-7390-a1b4-7911b9506d07/MadoR17.jsonl:387` | 2026-10-20T14:50:33 | `MadoR17` | git push | MUTATING (git push) | `git push -q 2&gt;&1 \| tail -2; git rev-list --count @{u}..HEAD; git status --porcelain \| head` |
| 25 | `2026-10-20T12-57-31-587Z_01a15963-70c3-7390-a1b4-7911b9506d07/MadoR17.jsonl:498` | 2026-10-20T15:09:20 | `MadoR17` | git add, git commit | MUTATING (git add); MUTATING (git commit) | `git commit -q -m "round-17: wave-2 corrections (tripwire fixes + regression suite, S066/S059/S061/S062/S070 anchors, S071, note scope/anchors, label-check/measure hardening, wave reports)" && git rev-` |
| 26 | `2026-10-20T12-57-31-587Z_01a15963-70c3-7390-a1b4-7911b9506d07/MadoR17.jsonl:511` | 2026-10-20T15:10:20 | `MadoR17` | git add, git commit, git push | MUTATING (git add); MUTATING (git commit); MUTATING (git push) | `git push -q 2&gt;&1 \| tail -1; git rev-parse HEAD; git rev-list --count @{u}..HEAD; git status --porcelain \| head -3` |
| 27 | `2026-10-20T12-57-31-587Z_01a15963-70c3-7390-a1b4-7911b9506d07/MadoR17.jsonl:528` | 2026-10-20T15:13:47 | `MadoR17` | git add, git commit, git push | MUTATING (git add); MUTATING (git commit); MUTATING (git push) | `git push -q && git rev-parse HEAD && git rev-list --count @{u}..HEAD` |
| 28 | `2026-10-20T12-57-31-587Z_01a15963-70c3-7390-a1b4-7911b9506d07/MadoR17.jsonl:542` | 2026-10-20T15:17:36 | `MadoR17` | git add, git commit, git push | MUTATING (git add); MUTATING (git commit); MUTATING (git push) | `git push -q && git rev-parse HEAD && git status --porcelain \| head -3` |
| 29 | `2026-10-20T12-57-31-587Z_01a15963-70c3-7390-a1b4-7911b9506d07.jsonl:731` | 2026-10-20T15:18:07 | `session-root` | git reset, jj-lane.sh state | MUTATING (git reset) | `... rm -rf $M/.jj "$HOME/.config/jj/repos/$cfg" && git -C $M reset -q && echo "after backout:"; scripts/hyaku/inline.sh closure mado ...; scripts/hyaku/jj-lane.sh state $M` |

### D. Invocations outside the resolved shell inventory (eval argv + unresolved loop target)

`…01a155e1…` = `2026-10-19T20-36-43-523Z_01a155e1-7d83-74e9-8383-9ee7c15d7c99.jsonl`;
`…01a15963…` = `2026-10-20T12-57-31-587Z_01a15963-70c3-7390-a1b4-7911b9506d07.jsonl`.

| # | transcript:line | ts (UTC) | seat | invocations | effect | target resolution / excerpt |
|---|---|---|---|---|---|---|
| 1 | `…01a155e1…jsonl:1725` | 2026-10-19T23:38:42 | `session-root` | jj git init, jj config set ×3, jj status, jj log, jj diff | MUTATING (init + repo config) + SNAPSHOT reads | `for l,gate in [('mado',…),('tameshi',…)]: repo=FR+'/'+l+'-shokunin'; … subprocess.run(cmd,cwd=repo,…); for cmd in [['jj','git','init','--colocate'],['jj','config','set','--repo','user.name',…],…]` |
| 2 | `…01a155e1…jsonl:1728` | 2026-10-19T23:38:57 | `session-root` | jj config get, jj config set, jj status, jj log, jj diff | MUTATING (one repo config set) + SNAPSHOT reads | `repo=FR+'/mado-shokunin'; … for cmd in [['jj','config','get','user.name'],['jj','config','set','--repo','revset-aliases."immutable_heads()"',…],['jj','status'],…]` |
| 3 | `…01a155e1…jsonl:2422` | 2026-10-20T01:04:36 | `session-root` | git merge | MUTATING (`merge --no-ff --no-commit`; adjacent verb) | `for p in [p for p in merge_plans if p['id'] in {'mado','tameshi'}]: repo=p['path']; … git('-c','maintenance.auto=false','merge','--no-ff','--no-commit',oid,cwd=repo)`; `merge_plans` built from live `FR+'/'+l+'-shokunin'` paths |
| 4 | `…01a155e1…jsonl:2472` | 2026-10-20T01:09:41 | `session-root` | git push (loop) | MUTATING (network push attempt to `origin`) | `cmd=['git','-C',r['path'],'push','--porcelain',r['push_remote'],…]` over `inventory['repos']` filtered to `lanes`, `assert len(lane_push_repos)==21`; `local/kaika-publish-inventory.json` records mado `path` = live lane, `push_remote` = `origin`, destination `github.com/VeigaPunk/mado-shokunin`; mado's inclusion in the loop set is `[INFERENCE]` from the 21-lane assertion |
| 5 | `…01a15963…jsonl:218` | 2026-10-20T13:21:50 | `session-root` | jj log, jj config list --repo | SNAPSHOT (`jj log`) + read (`config list`) | `for d in tameshi mado; do … (cd $d-shokunin && jj --no-pager log -r '@ \| @- \| trunk()' …; jj --no-pager config list --repo …)` |

Adjacent but excluded from the counts above: `…01a155e1…jsonl:2401` (`2026-10-20T00:58:38Z`)
runs `git -C r['path'] fetch --no-tags <push_remote> …` over the same lane inventory (writes
remote-tracking refs only), and `…01a155e1…jsonl:2413` creates `omp worktree add` for publication
lanes but explicitly excludes `mado`/`tameshi` (`parallel_merge_plans = [p for p in merge_plans
if p['id'] not in {'mado','tameshi'}]`).

## Findings for TwVcsClass fixture design

Observed real cases the classifier must reproduce; each cites a row above.

1. **Eval argv list (no shell text).** `…:1725`, `…:1728` carry `jj git init --colocate` and
   `jj config set --repo …` only inside Python lists passed to `subprocess.run(cmd,cwd=repo)`.
   A fixture that parses `bash arguments.command` alone reports the lane clean at exactly the
   moment `.jj` was born. Case `eval-subprocess-argv`.
2. **Tool `cwd` supplies the target.** `MadoR14.AttackCoverage:42` and
   `MadoR15.AttackMetric:37` contain no lane path; their bash argument `cwd` is the lane. Case
   `tool-cwd-target`.
3. **Loop/variable target.** `…01a15963…:218` is `for d in tameshi mado; do (cd $d-shokunin &&
   jj … log …)`. A literal `mado-shokunin` path regex sees neither `cd $d-shokunin` nor the
   target. Case `loop-var-target`. The same class appears as shell `$M`/`$L`/`repo=FR+'/'+l+'-shokunin'`
   in the eval rows.
4. **Helper subcommand semantics.** `jj-lane.sh state` is pure git and read-only; `commit` and
   `init` write. Treating the string `jj-lane.sh` as a write (or as harmless because it is the
   sanctioned helper) is wrong in both directions. Case `helper-subcommand`.
5. **Snapshot reads.** `jj log` and `jj file annotate` without `--ignore-working-copy` snapshot
   the working copy and write an op; only the two `op log --ignore-working-copy` rows are pure
   reads. Case `jj-snapshot-read`.
6. **Destructive backout sequence.** `…01a15963…:731` combines
   `git for-each-ref refs/jj | xargs … update-ref -d`, `rm -rf .jj "$HOME/.config/jj/repos/$cfg"`,
   `git reset -q`, `inline.sh closure mado`, `jj-lane.sh state`. A fixture that only looks for
   `git reset` misses the ref deletion and `.jj` removal; one that only looks for `jj` misses
   the git reset. Case `destructive-vcs-backout`.
7. **Heredoc-before-verb.** The MadoR17 rows (`MadoR17.jsonl:83,209,223,230,248,254,278,293,
   384,498,511,528,542`) append prose through `<<'EOF'` and then run `git add`/`git commit`;
   a line-oriented scanner that gives up at the heredoc terminator misses the write. Case
   `heredoc-before-verb`.
8. **`git -C <lane>` vs `cd <lane>`** both occur (rounds 13–16 use `-C`; ClosureMadoR16:95 uses
   `cd … && git pull --ff-only && git add …`). Case `git-C-vs-cd`.
9. **Helper re-init is structural.** Any closure dispatch after `.jj` deletion re-creates it
   because `inline.sh` calls `lane_vcs_init` when `HYAKU_VCS=jj`. A fixture expecting `.jj`
   absence after a backout is unsatisfiable while `hyaku.env:10` stays `HYAKU_VCS=jj`; test the
   re-init path instead (`wrapper-reinit`).

## F17 disposition

- **Superseded fact:** JjAuditMado's "colocated since 2026-10-19 20:38:49" refers to the
  audit-era repo, which was destroyed at `2026-10-20T15:18:07.972Z`. The current `.jj` was
  created by the helper re-init at `15:18:08.062Z`; its op store has 68 ops from `15:18:08` to
  `16:59:54`, not the 12 ops the audit read.
- **Op-log mapping (time-based):** the audit's three op-log commands correspond to the eval
  init (`…:1725`, `23:38:42Z`), `MadoR15.AttackMetric:37` (`07:24:40Z`), and
  `…01a15963…:218` (`13:21:50Z`). The audit's count was therefore not exhaustive; transcripts
  show 20 non-helper jj invocations in the lane.
- **Current risk surface:** after `15:18:08Z`, no direct `jj` or git write verb targets the lane;
  only `jj-lane.sh commit` (9) and `state` (11). The helper is the sole VCS writer, and helper
  commits also snapshot (`.jj/working_copy/tree_state` mtime matches the 16:59:52 commit).
- **Disposition:** classify colocation as durable, not removable. The enforceable invariants are
  (a) no non-helper `jj` in the lane, (b) no direct git write verb after the round-17 cutover,
  (c) helper `commit` only on the sanctioned paths, (d) `jj-lane.sh state` treated as read. A
  "remove `.jj`" remediation should be rejected unless `HYAKU_VCS` is changed and the closure
  wrapper stops calling `lane_vcs_init`.
- **Evidence durability:** the audit-era op store is gone; only JjAuditMado and these transcripts
  preserve it. A future F17 check must not cite the current op store for pre-15:18 ops.

## Limits

- Eval extraction is regex-based. Dynamically built argv (`git(*a)`, `[JJ, *args]`, variables
  assembled at runtime) is only counted when a literal list or literal first token is visible;
  helper functions such as `git('merge', …, cwd=repo)` were found manually, not generically.
- Wrapper internals are not expanded per invocation: `inline.sh`/`fleet-commit.sh` are known to
  commit/init lanes (`inline.sh:38-40,90,145`), but their internal git/helper calls are not
  separate rows. VCS writes performed inside `omp worktree` or other binaries are out of scope.
- Current op store: 68 files; only the two init-argv files were decoded with `strings`. Whether
  any op other than helper commits/bookmarks appears after `15:18:08Z` is `[UNK]`.
- Scan scope: only `sessions/-Projects-shokunin/**/*.jsonl` with mtime ≥ 2026-10-19, and only
  assistant `toolCall` records. Other session roots (`-Projects-shokunin-*`), non-JSONL logs
  (`*.bash.log`, `*.read.log`), and user messages were not scanned.
- Persistent shell `cwd` across tool calls is not modeled. A supplementary pass over every
  `Mado*`/`ClosureMado*`/`CloseMado*` tool call looked for bare `git <write>` with neither a
  lane path in the command nor a lane `cwd`; it found 8, all under `cd /tmp/...` sandboxes
  (`MadoR17.AttackSeparability:102`, `MadoR18.RevSeparability18:113,361,366`,
  `MadoR18.CriticC1W2:54,81`, `MadoR18.ReviewQuality2426:159`, `MadoR18.W3NumbersAudit:251`).
- Timestamps are transcript event timestamps, not shell start times; ordering is reliable at the
  second, not millisecond, level.
- `git fetch` (`…:2401`) and `omp worktree add` (`…:2413`, mado excluded) are noted but not
  counted as git write verbs; `git merge` (`…:2422`) is outside the assignment's verb list but
  included as an adjacent mutation.
- Redaction: token-like strings were replaced defensively; no credential, URL userinfo, or
  session key appeared in any excerpt. No full command or transcript line was copied into the
  lane.

## Installs

none. No packages, binaries, or host commands were installed or updated; `.jj` was read as file
bytes only.
