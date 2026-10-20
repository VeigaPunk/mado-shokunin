# RevJjTrialFindings — read-only verification of the jj-trial claims (`mado` lane)

Seat: `MadoR18.RevJjTrialFindings`. Date: 2026-10-20 (observations 15:38–15:44Z / 12:38–12:44 -0300).
Lane: `/home/vgpnk/Projects/shokunin/mado-shokunin`. No git or jj write; **no jj command executed**
(all jj facts below are file bytes; version read from the binary, not by running it).
Inputs verified against: `JjTrialMado.md` (reports dir), `JjAuditMado.md`, live bytes.

---

## 1. Answers to the four assigned checks

### 1.1 `git check-ignore -v .ufo/state/x`

At **15:38Z the result was no match (rc=1)** and `.gitignore` had one line. At **15:40Z it matched**:

```
$ git check-ignore -v .ufo/state/x
.gitignore:2:.ufo/state/	.ufo/state/x          RC=0
```

The file changed between the two calls: `.gitignore` mtime `2026-10-20 12:40:04.637 -0300`
(= 15:40:04Z). A concurrent seat (L1's routed fix) edited it mid-verification. Both observations
are true; the first is timestamped.

### 1.2 `.gitignore` contents (bytes)

```
$ od -c .gitignore
. u f o / i n t e r a c t i v e - s e s s i o n s / \n . u f o / s t a t e / \n
$ sha256sum .gitignore
0c60d3e695ea2dc11f70edef05931225f785cdac8200266e1cdba3a93ffb95fe   (39 B)
```

Committed version (`git rev-parse HEAD:.gitignore` / worktree `git hash-object`):

```
HEAD blob  614fb1e0179170954047b31df06c1cb2338c06d8   <- one line only
worktree   065507fecae69a673130f1bdbad81f2934f587fb
$ git diff --numstat -- .gitignore
1	0	.gitignore
```

**The rule is in the worktree only, not in `HEAD` (= `master` = `origin/master`).**
Pattern semantics, measured: `.ufo/state` → not ignored (rc=1); `.ufo/state/`, `.ufo/state/x`,
`.ufo/state/x/y` → ignored. Directory-only form, which is correct for files.
`git ls-files .ufo/state` = 0 entries, so no tracked-but-ignored path is created.
`.ufo/state/` does not exist yet, as the trial said.

### 1.3 `.jj/repo/config.toml`

**It does not exist.** `ls`/`cat` both ENOENT. This is not a missing config: jj 0.45.1 keeps
per-repo config **beside the user config**, keyed by `.jj/repo/config-id`. The binary's own docs
say so:

```
$ strings ~/.local/bin/jj | grep -i 'per-repo config'
Per-repo config is stored in the same directory as your user config for security reasons.
```

Resolution chain from lane bytes (no jj run):

```
$ cat .jj/repo/config-id
0c6bba4313e6b57d66ba
$ strings -n 3 ~/.config/jj/repos/0c6bba4313e6b57d66ba/metadata.binpb
4/home/vgpnk/Projects/shokunin/mado-shokunin/.jj/repo     <- id -> lane mapping
$ cat ~/.config/jj/repos/0c6bba4313e6b57d66ba/config.toml   (200 B, mtime 12:29:32 -0300)
[revset-aliases]
"trunk()" = "master@origin"

[snapshot]
auto-track = "none()"

[user]
name = "mado-shokunin"
email = "mado@shokunin.local"
```

So the helper's four `jj config set --repo` keys **are** present and correct. This **closes
`JjAuditMado` §8's UNK** ("reading it requires running jj in the live lane") — the config is
plaintext TOML outside the repo, locatable from `.jj/repo/config-id` + `metadata.binpb`.
It also independently confirms `JjTrialMado` step 2's config readback.

Residual hazard: the safety-critical `snapshot.auto-track = "none()"` lives **outside the lane
repo** — not committed, not cloned, invisible to `git show`. A fresh clone used with jj before
`jj-lane.sh init` runs would get jj's default `all()` (the trial measured 105 files entering `@`
under it). Only the helper's idempotent `init` establishes it; `cmd_init` re-applies the four
`config set --repo` calls even when `.jj` already exists (verified in
`/home/vgpnk/Projects/shokunin/scripts/hyaku/jj-lane.sh`, the `if [ ! -d .jj ]` guard covers only
`git init --colocate`).

### 1.4 `jj-lane.sh state` output

```
$ scripts/hyaku/jj-lane.sh state /home/vgpnk/Projects/shokunin/mado-shokunin
state branch=master local=d3a00003e6ef0b1e3c7b4faf52d592eb293857ba
      remote=d3a00003e6ef0b1e3c7b4faf52d592eb293857ba ahead=0 behind=0
      head=detached tracked=0 untracked=3
```

Cross-check (read-only git, explicit refs, **no `git status`**):

```
HEAD = master = origin/master = d3a0000   (ahead 0 / behind 0)
git symbolic-ref -q HEAD -> rc=1          (detached, as reported)
git rev-parse --abbrev-ref HEAD -> HEAD
git diff-tree --stat d9a5a18 d3a0000 -> SCORECARD.md (+55), census-start.txt (+5)  (NON-empty)
```

Two precision notes:
- HEAD is detached **at the branch tip**, not at an empty working-copy commit. The audit's F6
  false-FAIL shape (`HEAD` = empty `@`) is not the current state; a HEAD-pinning row reading this
  repo would see the right commit. `@{u}`/`symbolic-ref` consumers still break, and `state` handles
  that via `detect_branch` + `head=detached`.
- `untracked=3` is **directory-collapsed**, not a file count: `git ls-files --others
  --exclude-standard` returns 45 files (the 3 `??` entries at 15:38Z were
  `drafts/`, `evidence/`, `fetch/`). Do not read `untracked=N` as N files.

---

## 2. jj store provenance (supports trial Rec 1)

`.jj` was **re-created today**, after the audit snapshot: birth `2026-10-20 12:18:08.062 -0300`.
The op store holds 17 operations, one op head, all from 12:18:08–12:34:55 -0300. Decoded op arg
strings (protobuf `strings`, no jj run) include, in order:

```
jj --config 'snapshot.auto-track="none()"' git init --colocate .
track remote bookmark master@origin
jj file track --include-ignored -- SCORECARD.md .ufo/waves/round-18/evidence/...
snapshot working copy
edit commit metadata for commit f9174ce2...
commit b37cc6ba...
point bookmark master to commit d3a00003e6ef0b1e3c7b4faf52d592eb293857ba
push bookmark master to git remote origin
```

`git show -s d3a0000` → author **and** committer `mado-shokunin <mado@shokunin.local>`, matching
the helper's per-command identity. `SCORECARD.md` declares "Lane VCS is jj-colocated; commits only
through `scripts/hyaku/jj-lane.sh`". So **trial Rec 1 (adopt the helper) is actioned**, and
`JjAuditMado` F17's ".jj created 2026-10-19 20:38:49" and its three stray `jj log` ops describe the
*previous* store, not this one — the current op log has no read-only `jj log` op.

Contrast: `d9a5a18` (round-17 closure) was committed through jj as `protocol-shokunin`; the current
pre-registration commit is `mado-shokunin`. Both are in this repo's op log; neither mutated remote
history.

---

## 3. Routed jj-migration fixes — current byte state

| routed item | state at 15:44Z | evidence |
|---|---|---|
| `.ufo/state/` in `.gitignore` | **worktree only, uncommitted** | §1.1/§1.2; diff `1 +`; mtime 12:40:04 |
| `:3406` rc capture | **NOT landed** | `tools/mado-verify.sh:3406` still `blob=$(tmo git ... show ... \| sha256sum \| cut ...)`; `grep -n PIPESTATUS tools/mado-verify.sh` = no hits; `cat-file blob` absent; dead guard still at `:3408`; false "local edit" arm still at `:3413` |
| failing git-stub scenario | **NOT landed** | `:670` `show) cat "${STUB_GIT_BLOB:-/dev/null}"; exit 0 ;;`; no `STUB_GIT_RC`/per-verb rc anywhere |
| measured `PIN_MADO` re-cut | **not yet due** | `PIN_MADO='cd1d73d7…'` (`:1639`); `:3406` bytes unchanged, so the audit's derivation still applies. Re-cut becomes mandatory with the fix. |

Related audit recommendations, also checked:
- Rec 2 (`refs/heads/master` instead of HEAD at `:3382`/`:3391`): not applied. Those rows do capture
  `grc` and route to UNKNOWN, so the remaining exposure is F6's false FAIL, not a false PASS.
- Rec 4 (landedness row): absent — no `origin/master`, `merge-base` or `is-ancestor` in
  `tools/mado-verify.sh`. Nothing detects ahead/behind drift; it happens to be 0/0 now.
- Rec 5 (pre-existing `.jj`): handled in the helper — config is re-applied unconditionally and
  `jj-lane-selftest.sh:75` covers a pre-existing immutable alias surviving init. Moot for this
  `.jj`, which is fresh.

---

## 4. Which trial recommendations still need action

1. **Rec 1 — adopt `jj-lane.sh`: DONE.** Op log proves init/commit/push through the helper;
   identity and ancestry hold; ahead=0/behind=0.
2. **Rec 2 — `.ufo/state/` ignore: INCOMPLETE.** Rule present in worktree; must be committed via
   `jj-lane.sh commit -- .gitignore`. Post-commit check must read the **blob**, not the worktree:
   `git cat-file -p HEAD:.gitignore | grep -x '.ufo/state/'` and re-run
   `git check-ignore -v .ufo/state/x` after `git cat-file` (git ignores are read from the worktree,
   so only the HEAD blob proves the branch carries it).
3. **Rec 3 — fleet/seat doc note "must not `git add`": NOT DONE.** `SKILL.md` has no
   `jj-lane`/`colocat`/`snapshot.auto-track` text; its only `jj` occurrence is `:537`, where `jj` is
   a *breach class* for seats. The doctrine survives only in helper comments and the SCORECARD
   sentence. A seat reading SKILL.md alone will not learn that staged entries vanish on any jj
   mutation or that `jj file track` replaces `git add`.
4. **Rec 4 — no per-lane config beyond init: VERIFIED, no action.** The four keys are in
   `~/.config/jj/repos/0c6bba4313e6b57d66ba/config.toml`. Because that file is host-local, a
   review receipt should cite its path + sha256 if it is credited anywhere.
5. **Rec 5 — tooling: no action.** jj present at `~/.local/bin/jj`, version bytes
   `0.45.1-7c41cdeb16b6b321c64e789a966b6adf723816a5M`; git-lfs present; **no install performed**,
   no pacman/sudo command run (host pause respected).

Exactly **two** trial recommendations remain: Rec 2 (commit the ignore rule) and Rec 3 (seat-facing
doc note). The three routed gate repairs (§3) remain open as well; `PIN_MADO` re-cut is contingent
on the `:3406` fix.

---

## 5. Residual risk and verification gaps

**Residual risk**
- `auto-track=none()` is uncommitted host state outside the lane. A clone, CI runner or operator
  shell without `jj-lane.sh init` would run jj with default `all()` and sweep untracked seat
  scratch into `@`. Mitigation is procedural (always init), not git-verifiable from the lane.
- Until `.gitignore` is committed, `master` does not carry the ignore rule; a reviewer reading the
  branch (or another clone) sees no fix, and `.ufo/state/` could be committed by path explicitly.
- `state` under-reports scratch by construction (directory-collapsed `??`), so 45 untracked files
  read as `untracked=3`.
- `tools/mado-verify.sh:3408` is still dead code and `:3413` still converts an unreadable HEAD blob
  into a "local edit" verdict; the finding that motivated the routed fix is live in the bytes.

**Verification gaps**
- No jj command was run anywhere (mandate); `@`'s tree and `jj status` were not read. The config is
  proven by TOML bytes and the id→repo mapping by `metadata.binpb`; the absence of a jj op after
  12:34:55 plus the git index matching `HEAD` shows the 12:40 `.gitignore` edit has not been
  snapshotted by jj.
- `tools/mado-verify.sh` was not executed (seats do not run lane gates). The F10 judgment is from
  the unchanged code path plus `printf '' | sha256sum` → `e3b0c442…`; the audit's sandbox
  reproduction (`JjAuditMado` F10) supplies the end-to-end observation and the code is byte-identical
  to what it measured.
- `.gitignore` changed during the verification window; timestamps for both observations are given
  in §1.1 so a later reader can reconcile a different current byte state.
