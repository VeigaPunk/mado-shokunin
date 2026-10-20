# CriticJjDisposition — attack on the "why not" dispositions for F6, F9, F16, F17

Seat `MadoR18.CriticJjDisposition` (critic, leaf). Target: the planned dispositions in `gen_w1.py:82`
and the scribe draft `.ufo/waves/round-18/drafts/JjDisposition.md` (+ its report
`w1/reports/JjDisposition.md`). The source findings are `JjAuditMado.md` F6/F9/F16/F17 and §9 recs 2–6,
plus the related `JjTrialMado.md` items.
Observed 2026-10-20 ~15:30–15:47Z. Lane `refs/heads/master` = `d3a00003e6ef…` (git HEAD detached at the same hash).

## Verdict up front

| Finding | Planned / drafted disposition | Verdict | Owner | Fix now? |
|---|---|---|---|---|
| F6 HEAD-vs-tip (`:3382/:3391` → now `:3430/:3439`) | OPEN, because "the omarchy checkout is plain git and read-only to this lane". The draft recommends `rev-parse --verify refs/heads/master`. | **Disposition holds, but the reason is wrong, and the recommended fix is a regression (it creates a false PASS).** | lane (gate code) | **No.** Do not apply rec 2. |
| F9 `[ -d "$tree/.git" ]` (now `:3395`) | OPEN (latent). The draft recommends `git -C "$tree" rev-parse --git-dir`. | **Disposition holds, but the recommended fix is a regression on this host (`~/.git` exists).** | lane (gate code) | Optional. The only safe form is `[ -e "$tree/.git" ]`. |
| F16 landedness | "HOLDS for helper; OPEN for gate". R4's why-not says "a gate row changes gate bytes and needs a PIN re-cut". | **Belongs elsewhere (fleet), but for a different reason. Landedness also holds against the real remote.** | fleet (helper + closure-prompt) | No gate row. The lane only needs a receipt. |
| F17 prior jj runs (+ R5, R6, T1, T4, H1, H7) | CONFLICT. Live config is "absent / UNVERIFIED / CONTRADICTED". | **False provenance. The repo config exists and is correct. The "conflict" is already resolved by the fleet rule.** | fleet (helper, lane-addendum §4) | Correct the draft now (a text fix, L1). |

No finding among the four needs a lane **code** fix this round. Two drafted recommendations (rec 2, rec 3) must
be marked **rejected, with counterexample**. The F17 row and its corollaries must be rewritten before L1 integrates.

---

## F6 — HEAD vs branch tip

**Attack on the reason.** "Read-only to this lane" is not a why-not. The code is `tools/mado-verify.sh`, which the lane
owns. Nothing in the fix touches the checkout. The real why-not has three parts:

- **The rows fail closed.** Under colocation the outcome is UNKNOWN or FAIL, never a false PASS (audit §8).
- **The target is not colocated.** `~/.local/share/omarchy/.git` is a directory, `.git/HEAD` = `ref: refs/heads/master`, and there is no `.jj` (bytes read; no git run there).
- **No plan colocates that tree.** Colocation in `scripts/hyaku/lane-addendum.md:116-140` covers lane repos. The omarchy checkout is a domain source tree, read-only per PROTOCOL.md §Push scope (`:484-486`).

**Counterexample to the drafted fix (`rev-parse --verify refs/heads/master`): it creates a false PASS.**
The host's own omarchy tooling switches branches:
- `~/.local/share/omarchy/bin/omarchy-branch-set:4,18`, which reads `# omarchy:args=<master|rc|dev>` … `git -C $OMARCHY_PATH switch $branch` (sha256 `a6cf1564…`)
- `bin/omarchy-update-branch:26`, which reads `git -C "$OMARCHY_PATH" switch "$branch"` (sha256 `0c06e530…`).

I reproduced it in a /tmp plain-git repo (git 2.56.0): tag `v3.8.4` on master, then `git switch -c dev` plus one commit.
```
C HEAD=06b8d92b refs/heads/master=0646ff82 pin=0646ff82
C describe tip(master): v3.8.4 ; describe HEAD: fatal: no tag exactly matches '06b8d92b…'
```
Rows built on the tip would print `HELD: v3.8.4` and `HELD: <pin>` while the worktree is `dev`. The current
HEAD-based rows correctly go UNKNOWN or FAIL. `omarchy.skill.vs_head` compares the worktree with the HEAD blob, so it also PASSes on dev. Two of
the three identity rows would then be false-green. The pin's own meaning is written in the gate:
`MOVED … (every pin held at the old HEAD needs re-verification)` (`:3446`) and `== HEAD:version blob at the pinned HEAD`
(`:3353`). The pin is about what is checked out, not about where `master` points.

**Smallest safe correction if F6 is ever needed** (not this round): compare **tree identity**, not commit identity.
Use `git rev-parse 'HEAD^{tree}'` against a pinned tree id, or against `v3.8.4^{tree}`. Measured in the same /tmp repo:
```
D (empty jj-like WC commit on top of the tag, detached) HEAD^{tree}=a7b1043b tag^{tree}=a7b1043b   → would PASS (correct)
C' (dev branch)                                         HEAD^{tree}=bdf8a552 vs tag^{tree}=a7b1043b → would FAIL (correct)
```
This needs a new tree pin, which is a new fact to anchor. That is out of scope for round 18.
**Disposition text to use:** "OPEN by design: fail-closed (UNKNOWN/FAIL only), target not colocated and not a colocation
target. Rec 2 rejected: `refs/heads/master` false-PASSes after `omarchy-branch-set dev` (reproduced /tmp). Future
form: HEAD tree identity."
Drop the clause "The fix changes gate bytes, so PIN_MADO must be re-cut". GateRcFix re-cuts PIN_MADO this round anyway, so this is no reason.
Impacted axes: verdict honesty (gate), harm-watch (selftest counts) if anyone applies rec 2.

**The lane repo's own HEAD** is detached (`git symbolic-ref -q HEAD` rc=1; HEAD = master = `d3a0000`), so F6 does apply to the lane.
The fleet already governs it: lane-addendum `:139-140` says "record measured/pinned revisions as the branch tip, never bare `HEAD`", and `closure-prompt.md:22-23` tests ancestry
"against the branch ref". `measure.py` takes an explicit REV (`:51-64`). No lane tool reads lane `HEAD`.
Lane-owned residue: round-18 receipts (`harm-watch.sh`, re-cut receipts) must write `measured_commit` as a
resolved hash of `refs/heads/master`. `harm-watch.sh:314` reads `git -C "$FLEET" rev-parse HEAD` for the **fleet** repo, which is
git-only (no `.jj` there). That is acceptable, but it is the same idiom and should be noted.

## F9 — `.git` as a worktree file

**The lane owns it.** The disposition OPEN (latent, fail-closed UNKNOWN) is defensible: the host `.git` is a directory, and the omarchy installer
clones. One honesty wart: for a worktree checkout the row text says "no git checkout at $tree", which is false. The verdict
(UNKNOWN) is still correct.

**Counterexample to the drafted fix (`git -C "$tree" rev-parse --git-dir`):** the host home directory is a git repo.
`~/.git/HEAD` = `ref: refs/heads/master` (bytes read). Git discovery walks upward, so a tree without a `.git` gets
attributed to the dotfiles repo. Reproduced in /tmp with a `home` git repo and a `.local/share/omarchy` with no `.git`:
```
A rev-parse --git-dir: /tmp/critjj.…/home/.git rc=0
A rev-parse HEAD: 1a1bdd45… (home=1a1bdd45…)
```
With rec 3, the head row would report `MOVED: rev-parse HEAD → <dotfiles HEAD>`, which is wrong evidence about the
wrong repository. Today it reports an honest `UNKNOWN no git checkout`.

**The safe form is `[ -e "$tree/.git" ]`** (a directory or a gitdir file, and no discovery). A broken gitfile does **not** fall back upward:
```
B [-d]=0 [-e]=1; rev-parse --git-dir: fatal: gitfile does not point to a valid repository … rc=128
```
That rc=128 now lands on the UNKNOWN arms (`:3442`, and the `vs_head` rc arm `:3463-3464` in the GateRcFix worktree bytes).
It is optional: it can ride GateRcFix's single re-cut only if GateRcFix also adds an OM scenario where `.git` is a file. Note that the
stub ignores `-C` (`:662-664`), so the scenario tests the precondition only. Otherwise put it in Planned (round 19). Either way,
the disposition must say **rec 3 rejected**: `~/.git` makes upward discovery misattribute.

## F16 — landedness

**Measured now. It holds against the real remote, not just the cached ref:**
```
git ls-remote https://github.com/VeigaPunk/mado-shokunin.git refs/heads/master → d3a00003e6ef0b1e3c7b4faf52d592eb293857ba  (rc=0, 2026-10-20T15:46:32Z)
refs/heads/master = refs/remotes/origin/master = d3a0000; rev-list --left-right --count 0 0; is-ancestor rc=0
```
`refs/remotes/origin/master` mtime is `12:34:55.196`, which matches the op-store entry `push bookmark master to git remote origin`
(`12:34:55.201`). The ref was written by a successful push, not by a stale fetch. The draft's caveat "not re-fetched" is
therefore weaker than the evidence, and the evidence is now stronger still (ls-remote).

**The draft's why-not for R4 is the wrong reason.** "Changes gate bytes / needs re-cut" is not a reason, because the re-cut happens anyway this round.
The right reasons:
1. `mado-verify.sh` is the **host config plane** gate (`$ROOT/.config`, `$ROOT/.local/share/omarchy`). Lane-repo push state is
   a different subject. A row there would turn the gate red during every round by design, because commits are ahead before the helper pushes.
2. **Duplicate authority.** The fleet already owns landedness. `closure-prompt.md:22-26` (step 1) requires
   `merge-base --is-ancestor <hash> <branch>` and `jj-lane.sh state` → `ahead=0`. `lane-addendum.md:127-131` says to cite only
   the helper's `landed`/`pushed <hash>`, never `committed`.

**The lane-owned residue is a receipt, not a gate.** L1's round report should cite the helper's `landed/pushed` hash and
record one landedness receipt at round end: the `ls-remote` line plus `rev-list --left-right --count` and `is-ancestor`,
with a UTC time. The draft's conflict #3 also needs re-scoping. The `:3310` "Never `git status`" rule is about the **omarchy
checkout**. `lane-addendum.md:136` explicitly lists `status` as allowed read-only git in a lane. The round's stricter Contract list
binds seats, not the fleet helper. Flag it at most as fleet-owned.

## F17 — prior jj runs (and R5 / R6 / T1 / T4 / H1 / H7)

**Counterexample: the draft's central premise is false.** The draft says "`.jj/repo/config.toml` is absent … helper's `--repo`
keys … not confirmed in the live lane" and derives from it: R5 "NOT HOLDING live", T4 "CONTRADICTED", H1 "UNVERIFIED",
and H7 "a jj commit made outside the helper would be authored as the operator". In jj 0.45 the repo config is not
stored there. All of the following were read as bytes, with no jj run:
- `.jj/repo/config-id` = `0c6bba4313e6b57d66ba`
- `~/.config/jj/repos/0c6bba4313e6b57d66ba/metadata.binpb` names `/home/vgpnk/Projects/shokunin/mado-shokunin/.jj/repo`
- the `config.toml` beside it (mtime 12:29:32) holds:
  ```
  "trunk()" = "master@origin" · auto-track = "none()" · name = "mado-shokunin" · email = "mado@shokunin.local"
  ```

The only other config dir that names a `mado-shokunin/.jj/repo` is `2205afd3…`, which points to
`/home/vgpnk/Projects/shokunin/.tower/jj-probe/mado-shokunin`, not the live lane. So the live lane runs with exactly the helper's settings. Repo
config overrides the user identity, which falsifies H7. The index is clean: `git diff-index --cached refs/heads/master` shows 0 entries, and
`ls-files --stage` count = `ls-tree -r` count = 904.

**What actually happened.** The op store's 16 operations (command strings read with `strings`) all match helper code paths:
- 12:18:08: `jj --config 'snapshot.auto-track="none()"' git init --colocate .` (`jj-lane.sh:145`), followed by
  `--ignore-working-copy bookmark track master@origin` (`:163`).
- 12:28:10–12:28:13: `file track --include-ignored`, `diff --summary`, `metaedit --update-author`, `commit -m 'round-17 verifier spot-check …'` under `--config user.name=protocol-shokunin`, `bookmark set master -r d9a5a18…`, and `git push`.
- 12:34:53–12:34:55: the same sequence for `round-18: pre-registration …` (mado-shokunin), then push.

There is **no `jj log` or other seat-style command** since 12:18. Ten ops are the two helper commit sequences; the rest are init bookkeeping.
The fresh-init line proves `.jj` was **absent** just before 12:18:08 (the helper inits only `if [ ! -d .jj ]`, `:142`).
So the old store, which held the 04:24 and 10:21 `jj log` ops the audit transcribed, was deleted. **Who deleted it is `[UNK]`.**
The audit's F17 op-log quote is now the **only** surviving evidence of those runs.
Do not write "F17 holds / no jj ran" from the current op log: the current op log cannot see before 12:18:08.

**The "CONFLICT" between rec 6, T1 and the operator directive is already resolved.** `lane-addendum.md:116-140` makes the
helper the sole jj caller ("never run a mutating jj command yourself … the helper is the only writer … Read-only jj only with
`--ignore-working-copy`"). `closure-prompt.md:27-28` says "Never run a jj command in the lane except through the helper". This
round's "no jj at all" binds seats. L1's commits go through the helper, and the op args prove it. So R6/T1 → **HOLDS by fleet rule**, and
F17 → **fleet-owned, resolved by re-init. Historic `jj log` runs are recorded in the audit only. The deleter is UNK.**

**A lane-owned gap, not for now.** The lane's own detector says jj is out of class: `SKILL.md:537` reads "breaches outside its classes (jj, /proc
reads, file misroots) are not findings". A seat running `jj log` in the lane would be invisible to `mado-tripwire`.
Adding a jj class this round would change the classifier under C3's frozen pin, which is a moving target (CriticHonesty
already says to freeze the classifier). Put it in Planned (round 19) as a candidate tripwire class (`vcs_mutation`: bare `jj` without
`--ignore-working-copy`, git writes in a lane) with fixtures, and name it as a known miss in the round report.

**The commit identity of `d9a5a18` is intentional, not a finding.** It is authored `protocol-shokunin` by the helper's `--as protocol`, as the integrator's
non-author spot-check. Record it as such so nobody reads it as an identity drift.

## Incidental: the draft's PENDING rows are stale

`tools/mado-verify.sh` worktree sha256 is now `2bdf5e8a…`, while `refs/heads/master` is `fba82a66…`. The worktree has
`STUB_GIT_REVPARSE_RC` / `STUB_GIT_SHOW_RC` (`:675-679`), the `set -o pipefail` rc capture (`:3460-3464`), and OM9
(`:822-826`). The draft's "F10/F14 PENDING — sha unchanged `fba82a66`" was true at its read time and is false now. L1 must re-read
at integration. The draft's F2/F6/F9 line numbers also shifted by about +48 (`:3347` → `:3395`).

## Smallest safe corrections for L1 (text only; no code change required)

1. F6 / R2: keep OPEN with the fail-closed reason. Replace the recommendation with "rec 2 rejected (false PASS after `omarchy-branch-set
   dev`). The future form is a HEAD tree-identity pin." Drop "read-only to this lane" and "needs re-cut" as reasons.
2. F9 / R3: keep OPEN, or ride GateRcFix with `[ -e "$tree/.git" ]` plus a gitfile OM scenario. Mark rec 3 rejected (upward discovery
   to `~/.git`).
3. F16 / R4: "belongs to fleet (closure-prompt step 1, helper `landed` hash). A gate row would be a duplicate authority and out of the gate's plane."
   Add one landedness receipt at round end, including the `ls-remote` tip.
4. F17 / R5 / R6 / T1 / T4 / H1 / H7: rewrite as "live repo config present at `~/.config/jj/repos/0c6bba43…/config.toml` with
   auto-track none(), mado identity, trunk. `.jj` re-inited 12:18:08 by the helper path, with 16 helper-only ops since. The pre-12:18 store is gone
   (deleter UNK). Historic `jj log` runs are evidenced only by the audit." Remove CONFLICT. Add the tripwire jj class to Planned (round 19).

## Commands run and limits

- **Read-only lane git:** `symbolic-ref -q`, `rev-parse`, `rev-list --left-right --count`, `merge-base --is-ancestor`,
  `check-ignore -v`, `ls-files --stage`, `ls-tree -r`, `diff-index --cached`, `diff --stat` (.gitignore), `log`, `reflog`, `show`,
  and `config --get`.
- **One network read-only call:** `ls-remote` to the lane's own public remote, with `GIT_TERMINAL_PROMPT=0 -c credential.helper=` (no credential use).
- **Bytes only:** the `.jj` op store with `strings`, and `~/.config/jj/repos/*/{config.toml,metadata.binpb}`.
- **omarchy checkout, bytes only:** `cat .git/HEAD`, `ls`, `grep`, `cat -n` of two `bin/` scripts, and `sha256sum`. No git command was run there, and no omarchy command was run.
- **/tmp experiments:** `/tmp/critjj.*` with `HOME` redirected, `GIT_CONFIG_NOSYSTEM=1` and a cwd assertion; the directory was removed after the run.
- **Not run:** no jj command, no `mado-verify.sh` (live or `--no-live`), no `git status`, no pacman/sudo/host probes, and no transcript reads.
- **Installs:** none.
- **[INFERENCE]:** I inferred that jj 0.45 resolves repo config only through `config-id` → `~/.config/jj/repos/<id>/config.toml`. The evidence is the matching `metadata.binpb` path. `jj config set` leaves no op entry, so which helper run wrote `config.toml` at 12:29:32 cannot be read from the op store. I did not confirm this by running jj.
