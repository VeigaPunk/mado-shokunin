# ConnJjFleetFixes — helper-owned vs lane-owned jj findings, and the cross-lane fix census

Seat: `MadoR18.ConnJjFleetFixes` (connector, leaf) · item from `.ufo/waves/round-18/w1/spec.json`
· read-only; the only file written is this report · snapshot `2026-10-20T15:44:59Z`
(= `12:44:59 -03`), with two later re-reads noted where the fleet changed under me.

Sources read: all 67 `Jj*.md` reports in `/home/vgpnk/Projects/shokunin/.ufo/waves/hyaku/jj-w1/reports/`,
`scripts/hyaku/jj-lane.sh` (installed), its two untracked `.new` drafts, `.ufo/waves/hyaku/PHASE2.md`,
and the round-18 W1 plan (`gen_w1.py`). Lane state read with `git show|diff|ls-tree|rev-parse|cat-file`,
`git check-ignore`, `stat`, `sha256sum`, `strings` on jj op-store bytes. No `jj` command was run in any
repo; no gate/selftest was run; no lane file was written.

---

## 0. Bottom line

1. **The jj helper is fleet-wide, single-owner, and unchanged.** `scripts/hyaku/jj-lane.sh` sha256
   `2479041653c6a77c6cca099a37948d6c16361173c68fb14c8c2e2feae9dc2b1d` (the exact bytes audited by
   `JjSentinelHelper` and `JjCriticRollback`). All nine `JjSentinelHelper` defects (F1–F9) are still
   armed in the installed file, plus eleven further helper-owned defects reported by other lanes
   (H10–H20 below). No lane owns these; every lane that the driver colocates inherits them.
2. **Two independent helper rewrites exist, neither landed.** `scripts/hyaku/jj-lane.sh.new` and
   `jj-lane-selftest.sh.new` are untracked fleet-root files, **still being edited during this read**
   (sha changed from `d8f19474…` to `c94af548…` between 15:41Z and 15:44Z). `JjCriticRollback` keeps a
   second, narrower 144-line patch in `/fast/scratch/…/patched/jj-lane.sh` whose official selftest is
   **15/16** (case `i`). Neither is the tool; neither is citable.
3. **Mado's lane-owned surface is three read-only git calls** in `tools/mado-verify.sh` (:3382, :3391,
   :3406). Of these, only `:3406` can produce a *wrong* verdict (F10); `:3382`/`:3391` degrade to
   UNKNOWN/false-FAIL only if the omarchy checkout is ever colocated. The routed fix (GateRcFix) has
   **not been applied**: the file is byte-identical at HEAD and in the worktree, sha `fba82a66…`.
4. **No lane has fixed the pipe-rc class.** Mado (`tools/mado-verify.sh:3406`), tameshi
   (`tools/mutate-and-run.sh:1594,1629`) and souji (`tools/souji-quarantine.sh:310`) all still hash a
   failed git producer. Souji's `set -euo pipefail` does **not** fix it (`|| true` + non-empty
   `e3b0c442…` defeat both guards — measured, §4). The only `PIPESTATUS` use in any lane tool is
   unrelated (`souji-shokunin/tools/impl-37.sh:719-720`, `find`/`awk`).
5. **Exactly one lane has the `.ufo/state/` ignore committed: kotodama** —
   `kotodama-shokunin/.gitignore:1`, present since root commit `a527120` (blame `^a527120`). Mado,
   kama and tameshi carry the line only as **uncommitted worktree edits** made at `12:40:25`/`12:41:00`
   (`git show HEAD:.gitignore` has no `.ufo/state`). And the ignore rule is **not** a fix for helper F3:
   the helper's `file track --include-ignored` commits a `.ufo/state` path even when ignored.

---

## 1. Fleet state at read time

### 1.1 Colocation footprint (7 of 21 lanes)

```
$ for d in *-shokunin; do [ -d "$d/.jj" ] && stat -c '%n .jj=%y' "$d"; done
kaidoku-shokunin   2026-10-20 11:51:47
kama-shokunin      2026-10-20 11:16:57
mado-shokunin      2026-10-20 12:18:08
souji-shokunin     2026-10-20 12:29:49
tabi-shokunin      2026-10-20 12:24:02
tameshi-shokunin   2026-10-20 11:50:14
tsukuroi-shokunin  2026-10-20 12:29:51
```

The migration is live, not prospective: each colocation inherits every helper defect below at the
moment `inline.sh` runs `lane_vcs_init` (`scripts/hyaku/inline.sh:38-41`).

### 1.2 Mado refs and pre-registration

```
$ git -C mado-shokunin rev-parse master origin/master
d3a00003e6ef0b1e3c7b4faf52d592eb293857ba
d3a00003e6ef0b1e3c7b4faf52d592eb293857ba
$ git -C mado-shokunin rev-list --count origin/master..master
0
```

`d9a5a18` = round-17 lesson commit (12:28:10 -03); `d3a0000` = pre-registration (12:34:53 -03),
pushed 12:34:55. Both were created **through the helper**, per the jj op store (below).

### 1.3 Mado jj op store (read as bytes; no jj command)

`mado-shokunin/.jj/` was recreated `12:18:08`; `op_store/operations/` records, with mtimes:

| time (-03) | operation args (verbatim from op bytes) |
|---|---|
| 12:18:08 | `jj --config 'snapshot.auto-track="none()"' git init --colocate .` |
| 12:18:08 | `jj --ignore-working-copy bookmark track master@origin` |
| 12:28:10 | `jj --config 'user.name=protocol-shokunin' --config 'user.email=protocol@shokunin.local' metaedit --update-author` |
| 12:28:10 | `jj --config 'user.name=protocol-shokunin' … commit -m 'round-17 verifier spot-check (integrator, hyaku): non-author admit/reject' -- corpus/lessons/round-17-verifier-spotcheck.md` |
| 12:28:10 | `jj --ignore-working-copy bookmark set master -r d9a5a18e…` |
| 12:28:13 | `jj git push --remote origin --bookmark master` |
| 12:34:53 | `jj --config 'user.name=mado-shokunin' … commit -m 'round-18: pre-registration (claims C1-C3, baselines)' -- SCORECARD.md .ufo/waves/round-18/evidence/census-start.txt` |
| 12:34:55 | `jj --ignore-working-copy bookmark set master -r d3a00003…` |
| 12:34:55 | `jj git push --remote origin --bookmark master` |

This is the helper's `cmd_commit` sequence exactly (`metaedit --update-author` → `commit` →
`bookmark set` → `push`), i.e. `inline.sh`/L1 integration, not a seat. Repo config
(`~/.config/jj/repos/0c6bba4313e6b57d66ba/config.toml`, mtime 12:29:32, mode read-only bytes):

```
[revset-aliases] "trunk()" = "master@origin"
[snapshot] auto-track = "none()"
[user] name = "mado-shokunin"  email = "mado@shokunin.local"
```

So mado's pre-existing `.jj` **has** been repaired (contrary to `JjAuditMado` §8's inference that
`init` cannot repair it): installed `cmd_init` writes the repo config unconditionally after the
`.jj` check (`jj-lane.sh:145-155`), and the config currently holds all three keys. What `init`
cannot do is untrack scratch already in `@`; it only warns (`:156-160`).

---

## 2. Fleet-wide (helper-owned) findings

These are defects in `scripts/hyaku/jj-lane.sh` itself; they are not owned by any lane and cannot be
fixed from a lane repo. `fixed?` records whether either pending rewrite closes them, not whether the
live helper is fixed (it is not).

| ID | Defect (installed helper lines) | Report evidence | `.new` status | critic patch |
|---|---|---|---|---|
| H1 | **Non-fast-forward push.** Push is attempted with no ancestry guard, so a moved branch is pushed backwards/sideways — deletes remote commits with rc 0. (`:100-132`, push `:109`) | `JjSentinelHelper.md:32` F1 (repro); `JjDocPush.md:493-500` §9.2; `JjCriticRollback.md:18` F1 | fixed: `:201-202` merge-base guard | fixed (T1h) |
| H2 | **Wrong branch after detach.** `detect_branch` re-resolves from `origin/HEAD` after the first jj mutation; a non-default lane branch pushes its work onto `main`. (`:54-67`, used `:178,242`) | `JjSentinelHelper.md:76` F2; `JjAuditInlineSh.md:370-376` R6 | fixed: branch from `trunk()` alias (`:96-120`) | fixed (T1b) |
| H3 | **Spelling-based path guard.** `.`/`.ufo`/`.ufo/state`/`./.ufo/state/<f>` pass; `file track --include-ignored` then commits driver runtime. (`:180-185`, `:210`) | `JjSentinelHelper.md:112` F3; `JjAuditWatchdog.md:203-226` F7; `JjAuditPromptText.md:325` B6; `JjAuditFleetCommit.md:119-135` F4 | fixed: canonical path, all four spellings refused (`:509`), post-commit check (`:600-601`), test `z4` (`:359-371`) | not in 144-line patch |
| H4 | **Non-canonical lock + shared error file.** Lock keyed on `basename`, so `.` and the absolute path do not exclude; all lanes share `$STATE/jj-push.err`. (`:86`, `:109`, `:130`) | `JjSentinelHelper.md:142` F4; `JjAuditFleetCommit.md:201-202` | fixed: lock/err on physical path (`:130-140`) | fixed (T4e) |
| H5 | **Provisional `committed` hash + identity drop.** Retry rebase rewrites the printed `committed` hash and stamps the repo identity, not `--as`. (`:121`, `:227-235`) | `JjSentinelHelper.md:167` F5; `JjCriticRollback.md:275-278` F17 | fixed: `landed <hash>` verified by `ls-remote` (`:225-249`), rebase carries identity (`:295-318`) | fixed (identity gate) |
| H6 | **External force-push re-lands a cited commit.** Fetch+rebase covers previously pushed commits; the helper republishes them with rc 0. (`:117-124`) | `JjSentinelHelper.md:188` F6; `JjCriticRollback.md:35` F18 | fixed: old remote tip must be ancestor of new (`:279-284`) | fixed (T6b) |
| H7 | **`nothing to commit` prints a stale `pushed <hash>` and exits 0.** (`:218-219`, `:238`) | `JjSentinelHelper.md:215` F7; `JjAuditPromptText.md:311` B5; `JjCriticRollback.md:29` F13 | fixed: prints no hash (`:553`, usage `:60`) | fixed (T1e) |
| H8 | **`--as` not bound to the lane.** Any `[a-z0-9-]+` id accepted. (`:176-177`) | `JjSentinelHelper.md:231` F8 | fixed: lane id or `protocol` only (`:493-494`) | n/a |
| H9 | **`bookmark track` failure swallowed** (`|| true`, `:163`). | `JjSentinelHelper.md:237` F9 | fixed: hard fail unless remote bookmark exists (`:433-437`) | n/a |
| H10 | **`state` is not read-only.** `git status --porcelain` (`:78`) rewrites `.git/index`; the "pure git, read-only" claim is false. | `JjAuditTabi.md:163-178` F5; caller text `closure-prompt.md:25` | **not fixed** — `.new:167-169` still calls `git status`, no `GIT_OPTIONAL_LOCKS=0` anywhere | not fixed |
| H11 | **Deletions dropped.** `[ -e "$p" ] || git ls-files --error-unmatch` filters a `git mv`/`git rm` source; quarantine publishes half a move. (`:191-197`) | `JjAuditSouji.md:55-80` F1, `:380` risk 1 | fixed: HEAD-tracked paths admitted via `git cat-file -e refs/heads/$branch:$q` (`:520`) | not in patch |
| H12 | **Conflicted tree disagreement.** `validate` says clean; `do_push` refuses a conflicted bookmark → exit 3. (`:104-107`) | `JjAuditSourcesCensus.md:239-241` | unchanged (still a design choice) | unchanged |
| H13 | **Unborn `refs/jj/root` accepted as branch.** `symbolic-ref --short HEAD` returns `jj/root`; `state` shows `branch=jj/root local=-`. (`:55`) | `JjAuditInlineSh.md:370-376` R6 | fixed: only `refs/heads/*` or `origin/HEAD`, plus `valid_branch` rejects `jj/*` (`:86-100`) | n/a |
| H14 | **Fleet root is a valid "lane".** `init`/`commit` only require `.git`; pointing the helper at `/home/vgpnk/Projects/shokunin` is accepted. | `JjSentinelHelper.md:299-302` rec 8 | fixed: `lane_realdir` refuses the fleet root (`:74-82`) | not in patch |
| H15 | **`init` cannot clean pre-existing `@` additions.** It warns only (`:156-160`); a lane colocated under default auto-track keeps seat scratch in `@` until a commit sweeps it. | `JjAuditFleetCommit.md:119-135` F4; `JjAuditMado.md` §8 | changed: `.new:444-455` **untracks** every `@` addition absent from the branch tip (behavior change; see §6) | not in patch |
| H16 | **`pushed` can be stale on "already matches".** Exit 0 may mean no push occurred; the printed hash may predate the real remote tip. | `JjDocPush.md:524-533` §9.5 | fixed by `report_landed` (`:225-249`) | partly |
| H17 | **Push-recovery leaves conflicted ancestors unfixable.** jj refuses to push conflicted ancestors; the "resolve in the lane, retry" advice loops on exit 3. | `JjSentinelHelper.md:250-253` (checked/holding) | unchanged | unchanged |
| H18 | **Retry rebase uses `--ignore-immutable`.** Installed helper lifts the lane's `::bookmarks()` alias for the recovery rebase (`:121`). | `JjConnectorProvinces.md:118`; `JjSentinelHelper.md:188` F6 | fixed: per-command alias narrowed to remote bookmarks, `--ignore-immutable` never used (`:295-300`) | fixed |
| H19 | **Doc/helper drift in the closure protocol.** `closure-prompt.md:25` calls `state` "pure git, read-only"; `lane-addendum.md:127-128` says a named directory keeps ignored content out. Both false (H10, H3). | `JjAuditPromptText.md:634-636`; `JjAuditTabi.md:163` | docs unchanged | docs unchanged |
| H20 | **Two writers split the op log.** `.` vs absolute path in two concurrent helper calls produced 10 reconciles, 10 divergent commits, 5/12 files never pushed, all rc 0. | `JjCriticRollback.md:29-30` F12 | fixed: canonical lock (H4) + divergent-tip refusal (`:290-300`) | fixed |

Additional helper-owned observation, not a numbered report finding: the installed helper has **no jj
version assertion** (`JjConnectorProvinces.md:114`); all sandbox work used 0.45.1, and the push
semantics H1/H16 are version-sensitive.

---

## 3. Lane-owned findings for mado (JjAuditMado F1–F17, §9 recs)

Owner key: **M** = mado lane code/doc · **H** = helper · **X** = external host/omarchy checkout (read-only
to this lane) · **F** = fleet driver (`inline.sh`).

| F | Subject | Owner | State at 15:44Z | Round-18 disposition |
|---|---|---|---|---|
| F1 | only two executables; `mado-action-plan.py` has no git | M | holds | none needed |
| F2 | 3 git invocations, all `mado-verify.sh`, class D | M | holds | `:3406` (F10) + stub (F14) in flight; `:3382`/`:3391` unassigned |
| F3 | omarchy checkout is plain git (`v3.8.4`, `8fcc9d60`, no `.jj`) | X | holds | re-check at run time |
| F4 | live gate passes all 3 git rows (unrelated walker-pin red) | M | holds | not a jj defect |
| F5 | colocated checkout at the tagged commit: 2/3 rows still work | X | latent | none |
| F6 | `jj new` → empty HEAD → tag UNKNOWN, head false-FAIL | X/M | **armed, not firing** (checkout plain git) | rec 2 (resolve branch tip) unassigned |
| F7 | no class-A markers | M | holds | none |
| F8 | class-C recipes (`git diff --numstat`) index-sensitive | M | latent (SKILL.md:1046,1226,1370) | unassigned |
| F9 | `[ -d "$tree/.git" ]` misses worktree checkouts (`:3347`) | M | not fixed | rec 3 unassigned |
| F10 | pipe-rc: `git show … \| sha256sum` hashes empty input, false "local edit" (`:3406`; dead `-z` at `:3408`) | M | **not fixed** (sha `fba82a66…` = HEAD) | **GateRcFix** (in flight) |
| F11 | no hooks | M/X | holds | none |
| F12 | no attributes; LFS filters inert | X | holds | none |
| F13 | jj bypasses hooks/attributes | H/jj | latent | document only |
| F14 | selftest git stub always exits 0 (`:668-670`); UNKNOWN arms untested | M | **not fixed** | **GateRcFix** |
| F15 | selftest hardcodes `/tmp`; SKILL count stale (`268/268` vs `372/372`) | M | not fixed | unassigned; update with gate commit |
| F16 | no lane landedness check; lane was 8 ahead | M | **not fixed**; now `ahead=0` (`d3a0000` pushed) | rec 4 unassigned |
| F17 | lane already colocated; jj had run in it | F | **continuing by design** (op log §1.3) | none (driver-owned) |

Rec 5 (`init` must repair pre-existing `.jj`) is **already implemented** in the installed helper
(`:145-160`): config is re-applied unconditionally; only pre-tracked scratch is left (H15).
Rec 6 ("keep jj out of live lanes") conflicts with the documented `inline.sh` path (`PHASE2.md:57-66`)
— see §6.

---

## 4. Named question A — has any lane already fixed the pipe-rc?

**No.** Census of every lane tool at HEAD (`git grep 'PIPESTATUS\|pipefail' HEAD -- tools`), plus a
targeted read of each `git`-producer-into-`sha256sum` site:

| Lane | Site (at HEAD) | Code | Set options | Same defect? |
|---|---|---|---|---|
| mado | `tools/mado-verify.sh:3406` | `blob=$(tmo git -C "$tree" show "HEAD:$OMARCHY_SKILL_REL" 2>/dev/null \| sha256sum \| cut -d' ' -f1)` | `:82 set -u` (no pipefail) | **yes** — `e3b0c442…` compared; `:3408 -z` unreachable |
| tameshi | `tools/mutate-and-run.sh:1594`, `:1629` | `exec_sha=$(git -C "$grepo" show "$rev:exec.sh" \| sha256sum \| cut -d' ' -f1)` | `:162 set -u -o pipefail` (no `-e`) | **yes** — non-empty digest; no rc branch before use |
| souji | `tools/souji-quarantine.sh:310` | `blob_sha=$(git … cat-file blob "$intro:$REL" 2>/dev/null \| … sha256sum \| cut -d' ' -f1 \|\| true)` | `:140 set -euo pipefail` | **yes** — `\|\| true` discards the pipeline rc; `-n` cannot see `e3b0c442…` was not content |
| souji | `tools/impl-37.sh:719-720` | `find_rc=${PIPESTATUS[0]}; awk_rc=${PIPESTATUS[1]}` | `:62 set -euo pipefail` | no — unrelated `find`/`awk`, and correctly scoped |

Only mado's site was listed as a routed round-17 defect; the other two are *same-class* sites no
round-18 item currently owns. No lane has a committed fix; the only fix attempt is mado's GateRcFix
(not yet written).

### 4.1 Measured shell semantics (local bash, no repo touched)

```
$ bash -c 'set -euo pipefail; x=$(false | sha256sum | cut -d" " -f1 || true); printf "x=[%s]\n" "$x"'
x=[e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855]      # pipefail + || true does NOT help
$ bash -c 'x=$(false | cat); rc=$?; echo "n=${#PIPESTATUS[@]} PS0=${PIPESTATUS[0]} dollarq=$rc"'
n=1 PS0=0 dollarq=0                                                        # naive ${PIPESTATUS[0]} sees the parent
$ bash -c 'x=$(set -o pipefail; false | sha256sum | cut -d" " -f1); rc=$?; printf "x=[%s] rc=%s\n" "$x" "$rc"'
x=[e3b0c442…] rc=1                                                         # rc is honest, digest still empty-input
```

Consequences for GateRcFix (and for any census that recommends a form):

1. `blob=$(… | sha256sum …); grc=${PIPESTATUS[0]}` is **wrong**: after an assignment there is one
   `PIPESTATUS` element (the assignment, rc 0), so the guard never fires. The suggestion in
   `JjAuditMado.md:478` ("capture `${PIPESTATUS[0]}`") is literally wrong as written.
2. The two sound forms are `out=$(git show …); grc=$?` (hash `out` only when `grc=0`) or
   `blob=$(set -o pipefail; git show … | sha256sum | cut …); grc=$?` (as tested). Prefer the first:
   it keeps the digest out of the failure path entirely.
3. The `-z "$blob"` guard at `:3408` is unreachable and cannot be made reachable by rc handling — a
   legitimate empty blob hashes to `e3b0c442…` too. Route `grc≠0` to UNKNOWN before any comparison and
   delete the `-z` arm (or keep it as a belt for an empty *variable*, which `sha256sum` never yields).
4. Do **not** turn on global `set -o pipefail` in `mado-verify.sh`: it has 16 `$(… | sha256sum|wc|cut)`
   pipelines and many `| head -1` pipelines whose rc semantics would all change. Scope pipefail to the
   substitution or use form (1).

---

## 5. Named question B — has any lane already fixed the `.ufo/state` ignore?

Committed in **exactly one** lane; three more have it only in the worktree:

| Lane | Path:line | In HEAD? | Evidence |
|---|---|---|---|
| kotodama | `kotodama-shokunin/.gitignore:1` (also `:2 .ufo/watchdog.log`) | **yes**, since root `a527120` | `git show HEAD:.gitignore` prints `.ufo/state/` as line 1; blame `^a527120` |
| mado | `mado-shokunin/.gitignore:2` | **no** | `git diff HEAD -- .gitignore` adds the line; blame `Not Committed Yet 2026-10-20 12:40:25`; `git show HEAD:.gitignore` = one line |
| kama | `kama-shokunin/.gitignore:2` (+ `:3 __pycache__/`) | **no** | same shape; blame `Not Committed Yet 2026-10-20 12:41:00`; `git show HEAD:.gitignore` = one line |
| tameshi | `tameshi-shokunin/.gitignore:2` (also `:3 .ufo/watchdog.log`, `:4 __pycache__/`) | **no** | same; blame `12:41:00`; HEAD = one line |

No lane puts the pattern in `.git/info/exclude` or a global excludes file (`core.excludesFile` unset;
`grep -l ufo/state *-shokunin/.git/info/exclude` → none). The mado worktree rule is active now:

```
$ git -C mado-shokunin check-ignore -v .ufo/state/x .ufo/watchdog.log
.gitignore:2:.ufo/state/	.ufo/state/x
```

(`.ufo/watchdog.log` is still **not** ignored in mado.)

### 5.1 Second-order: the ignore rule does not close the helper hole

Helper F3 commits `.ufo/state` through three routes the ignore cannot stop:
`jj file track --include-ignored -- .ufo/state/<f>` (`jj-lane.sh:210`), the directory spelling
`.ufo/state` (`:182` matches only `.ufo/state/*`), and `./` (whole repo). The `.gitignore` line narrows
`git status`/`jj status` noise and closes the *default-auto-track* hazard
(`JjAuditFleetCommit.md:119-135`), but it is **not** evidence the "never commit driver runtime"
invariant holds. Only helper H3 (installed guard + post-commit `diff` check) closes it.

---

## 6. Contradictions — stated, not smoothed

1. **Contract text vs actual landing path.** The round-18 contract says "NO git or jj write of any
   kind in the lane … and no jj command at all". The mado op store (§1.3) shows `jj-lane.sh`-driven jj
   writes in the live lane at 12:18, 12:28 and 12:34, including two pushes, and `d3a0000` — the
   pre-registration commit the round depends on — *is* one of them. `PHASE2.md:57-66` documents this
   as the intended integration path (`inline.sh` colocates at dispatch/closure; L1s and closures
   commit only through the helper; git writes are forbidden). Read together: the ban is on **seats**
   and on **git**; L1/orchestrator helper writes are the designed path. If L1 intends the ban to bind
   L1 too, the pre-registration landing already breached it. This needs an explicit ruling, because
   the helper is also the vector for H1/H5/H6/H7.
2. **`state` is advertised as read-only in three places** (`jj-lane.sh:70`, `closure-prompt.md:25`,
   `lane-addendum.md:138`) and is not: `git status` rewrites `.git/index` (Tabi F5). Both the installed
   file and the `.new` draft keep it (`jj-lane.sh:78`, `jj-lane.sh.new:167`). Any seat told to run
   `jj-lane.sh state` perturbs the index under a concurrent jj writer.
3. **The `.new` draft is not a drop-in.** It changes `init` from "warn about pre-tracked `@`
   additions" to "**untrack** every addition absent from the branch tip" (`:444-455`). That mutates
   `@` in pre-existing lanes (mado, tameshi, kama, kaidoku, souji, tabi, tsukuroi). Whether that is
   desired is a lane decision, not a helper detail. It also still carries H10 (`git status` in
   `state`) and H12 (conflicted push). Its selftest `.new` was **being rewritten during this read**
   (12:35 → 12:43), so no run result exists for the current bytes.
4. **The critic's patched helper fails its own selftest 15/16** (case `i`, `JjCriticRollback.md:313`):
   its identity gate refuses a commit the old test expects to publish. Two competing rewrites
   (737 changed lines in `.new`, 144-line `guards.diff`) fix overlapping sets; installing either without deciding
   the identity-vs-case-`i` question re-opens H5/H6 or the selftest.
5. **`.ufo/state` is "fixed" in three lanes and committed in none of them.** A report that says
   "ignored" is true of the worktree at 12:41 but false of every commit in mado/kama/tameshi; only
   kotodama can be cited from HEAD.
6. **`RevJjTrialFindings` expects `check-ignore .ufo/state/x` to return no match** (`gen_w1.py:133`).
   That expectation is now stale: the uncommitted mado line makes it match. A reviewer running the
   literal check will report a false regression unless it distinguishes HEAD from worktree.
7. **The routed PIN_MADO re-cut is coupled to GateRcFix's edit.** `PIN_MADO` is derived from the file
   bytes (`mado-verify.sh:1639`, `:1723`); the current file sha `fba82a66…` is what the pin names.
   Any gate edit invalidates the pin, so the re-cut must be taken from the **post-edit** bytes and the
   selftest assertion count must move if F14 adds scenarios (F15's `268/268` is already stale vs
   `372/372`).

---

## 7. What L1 should do (ordered, smallest first)

1. **Cite the installed helper, never the drafts.** Any claim about helper behavior names sha
   `24790416…` (`scripts/hyaku/jj-lane.sh`). `.new` and `/fast/scratch/.../patched` are not the tool;
   both are untracked and the former is actively churning.
2. **GateRcFix:** use `out=$(git show …); grc=$?` then hash `out` only on `grc=0`, or a
   substitution-scoped `set -o pipefail`; never `PIPESTATUS` after an assignment (§4.1). Route rc≠0 to
   `UNKNOWN "cannot read HEAD:<rel> (rc=N)"`; delete or justify the `-z` arm; add the three rc-knob
   scenarios and recompute `PIN_MADO` from the edited bytes.
3. **Do not credit the `.ufo/state` ignore until it is committed in mado**, and never as a helper fix
   (§5.1). If the L1 commit includes it, the check is
   `git -C mado-shokunin show HEAD:.gitignore | grep -qx '.ufo/state/'`.
4. **Keep seats off `jj-lane.sh` and off `git status` in the lane.** The contract's read-only list is
   `log/show/diff/ls-tree/rev-parse/cat-file`; `state` is outside it (H10). Landedness for F16 can be
   read with `git rev-list --count refs/remotes/origin/<b>..refs/heads/<b>` (read-only) instead.
5. **Decide the helper rewrite as one artifact, or not at all.** If either patch is installed, run its
   own selftest on a clone first and resolve the identity-vs-case-`i` conflict; otherwise H1–H9 stay
   armed and any mado hash landed through the helper (including future round-18 commits) inherits the
   rewrite risk.
6. **Update the two protocol sentences** that are false today: `state` is not read-only (H10), and a
   named directory does not keep `.ufo/state` out (H3). This is documentation, not code.

---

## 8. Verification performed / not performed

Performed (read-only): read/grepped all 67 `Jj*.md` (full text of `JjAuditMado`, `JjTrialMado`,
`JjSentinelHelper`, and the audit/push/rollback sections of the rest; targeted greps for every
helper-line citation across the remainder); `grep`/`sed` on the installed helper and both
`.new` drafts; `bash -n` on installed and `.new` helper (both OK); `sha256sum` of helper/`.new`; `git
show|diff|ls-tree|rev-parse|cat-file|check-ignore|blame|rev-list` on mado, kama, tameshi, kotodama;
`stat` on `.jj` trees, op-store operation files, and jj repo config; `strings` on op-store bytes;
four local `bash -c` semantic probes. No tool installs or upgrades.

Not performed (by contract): no `jj` invocation anywhere; no `jj-lane-selftest.sh` run (it drives jj);
no lane gate or `mado-verify.sh --selftest`; no write outside this report; no `git status` in any
lane (one `git status --porcelain scripts/hyaku/` ran in the fleet root's own tree; lane state was
read only via `show`/`diff`/`check-ignore`/`rev-list`).

## 9. Inference

- [INFERENCE] The highest live risk to mado is **H1 + H5**, not F10: every mado landing goes through
  the helper (op log §1.3), and a recovery rebase rewrites the `committed` hash a report might already
  cite. F10 is a wrong-row verdict; H1/H5 are wrong-history verdicts.
- [INFERENCE] Souji's `pipefail` looks like a fix in `grep` and is not one at `:310`: `|| true` and the
  non-empty empty-input digest defeat it. A census that treats `pipefail` presence as "checked" would
  produce a false clearance.
- [INFERENCE] tameshi's two sites are selftest fixture pins, not gate rows, so the practical blast
  radius there is a mutant test with a wrong expected digest (could mask a killed/survived flip); not
  measured.
- [INFERENCE] `.new`'s init-untrack behavior would silently change `@` contents in seven colocated
  lanes; it was not executed, so its effect on mado's current `@` is UNK.
