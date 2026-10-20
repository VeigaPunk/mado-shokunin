# MadoR19.RerunLanded — partial

Target: `.ufo/waves/round-19/landed-check.sh` (jj audit F16 non-claim repair) at lane tip
`01b80946d92b26370d3012a7da655d00dd135154`, baseline `9c54c56a6a7528675027b7f628f97a1b8d1b8e8d`.
Worktree bytes == committed bytes (sha256 `e6f48348cfd4a3ccdbe681824cff0a1aff1de91e48d0e819f6a3172f6884a07b`,
git blob `fb4c732c1281a3f4bdd718299a69b137e2998a78`, last touched by `df84807d8fc49f5d8fb4ec3060859e5b1992084c`).
Nothing in the lane was written except this report; all fixtures are under `/tmp/lc*`.

**Verdict: partial.** The core answer (is hash H on origin/master?) and the exit map hold, read-only holds,
`jj` is never invoked, `MISSING` works, the live verdict for both advertised hashes reproduces independently.
Two claims the wave advertises for this tool are **false**, and two more are conditional/narrow:

- **B1 (breaks):** the shallow warning is CWD-dependent — silent exactly in the documented invocation
  (from outside the lane), and it fires spuriously when the *caller's* CWD is some other shallow repo.
- **B2 (breaks, consequence of B1):** with the warning dead, a commit that **is** on origin/master is
  reported `LOCAL_ONLY … (ancestor of neither …)`, exit 1 — the "false LOCAL_ONLY possible" failure the
  warning exists to flag.
- **B3 (bounded):** `LANDED` is replace/graft-sensitive; a non-landed commit reports `LANDED` when a
  `refs/replace` graft exists. Lane currently has 0 replace refs and no `.git/info/grafts` → no live exposure.
- **B4 (conditional):** "`ls-remote` is time-bounded so a dead remote cannot hang a wave" (:26-27) is only
  true while `timeout(1)` is in PATH; without it the tool hangs indefinitely (>75 s observed).

---

## 1. Assigned run — headline receipt

```
$ bash /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-19/landed-check.sh \
       /home/vgpnk/Projects/shokunin/mado-shokunin \
       9c54c56a6a7528675027b7f628f97a1b8d1b8e8d 01b80946d92b26370d3012a7da655d00dd135154
landed-check.sh: origin/master = 01b80946d92b26370d3012a7da655d00dd135154 (object present locally)
LANDED 9c54c56a6a7528675027b7f628f97a1b8d1b8e8d
LANDED 01b80946d92b26370d3012a7da655d00dd135154
EXIT=0
```

Independent re-derivation (not the tool's own stderr):

```
$ git -C /home/vgpnk/Projects/shokunin/mado-shokunin ls-remote origin refs/heads/master
01b80946d92b26370d3012a7da655d00dd135154	refs/heads/master
$ git -C <lane> merge-base --is-ancestor 9c54c56 origin/master   → rc=0
$ git -C <lane> rev-parse HEAD → 01b8094…   (== origin tip)
```

Elapsed for the live pair: **411 ms** (`date +%s%N` bracketing, `/tmp` CWD). I made no lane write: the only lane
write in this whole item is this report file, and §2 below is a syscall-level proof that the tool itself opens
nothing writable under `.git`.

## 2. Write path / fetch path — none (strace, not just reading headers)

Full syscall trace of the live invocation incl. `execve`, `openat`, `creat`, `unlink`, `rename*`, `mkdir*`, `ftruncate`:

```
strace -f -qq -e trace=execve,openat,creat,unlink,rename,renameat2,mkdir,mkdirat,ftruncate \
  -o /tmp/lc/lane.log bash <script> <lane> 9c54c56 01b8094        # EXIT=0, 2×LANDED
$ grep -E 'O_WRONLY|O_RDWR|O_CREAT|O_TRUNC|O_APPEND' /tmp/lc/lane.log | grep -v '/dev/|pipe:|socket'
   (empty)
$ grep -E 'unlink|rename|mkdir' /tmp/lc/lane.log
   (empty)
$ grep -c '\.jj' /tmp/lc/lane.log            → 0
$ grep -c '\.git/index' /tmp/lc/lane.log     → 0
```

`execve` set seen (PATH search then real binary): `git`, `git-remote-https`, `git` (×9), `awk`, `timeout`.
Remote operations are `git ls-remote origin refs/heads/master` only — the network READ the header declares
(`.ufo/waves/round-19/landed-check.sh:28-30`). Confirmed no fetch: in a repo where the remote moved after the
clone, `FETCH_HEAD` stayed absent, `refs/remotes/origin/master` unchanged, loose object count unchanged
(`/tmp/lcb/stale`: objects 3→3, tracking stayed `df09cd29`).

Corollary, verified: the tool ignores a stale remote-tracking ref. In `/tmp/lc9/stale` the tracking ref was
forced back to C1 while origin had C2; the tool printed `origin/master = C2` and `LANDED C2` — live resolution holds.

## 3. `jj` — never invoked

Static: `jj` appears only in comments (`:5`, `:12`, `:30`), no `jj` command in executable text.
Dynamic, two independent proofs:

```
# PATH shim that logs any invocation
printf '#!/bin/sh\necho "JJ INVOKED: $*" >> /tmp/lc/jj.log\nexit 99\n' > /tmp/lc/shim/jj
PATH=/tmp/lc/shim:$PATH bash <script> /tmp/lc/B 88e85b7 3670536   → normal output
cat /tmp/lc/jj.log                                                → (no jj invocation)
grep -E 'execve\("[^"]*jj' /tmp/lc/strace.log                     → (no jj execve)
```

A colocated checkout is fine because the script only shells out to git: on the live lane (`.jj` and `.git`
both present) the trace shows **zero** accesses under `.jj`.

## 4. `MISSING` — correct; one narrow false statement

```
$ <script> <lane> deadbeefdeadbeefdeadbeefdeadbeefdeadbeef
MISSING deadbeefdeadbeefdeadbeefdeadbeefdeadbeef      EXIT=1
$ <script> <lane> ffff
MISSING ffff                                          EXIT=1
$ <script> <lane> zzzz
landed-check.sh: not a hex object name: zzzz          EXIT=2
```

Absent-locally-but-present-on-remote also reads `MISSING` (`/tmp/lcb/stale`, tip `c5bc5670…` pushed after the
clone: `MISSING c5bc5670…`), which matches the header's definition "object absent **locally**" (`:25`).

**B5 (narrow):** an *ambiguous* abbreviated object name is reported `MISSING`, although the object(s) exist.
Repro in `/tmp/lc/amb/W` (603 objects; two blobs share prefix `c266`):

```
$ git rev-parse --verify --quiet c266^{commit} → rc=1 ; git cat-file -e c266 → rc=128
    error: short object ID c266 is ambiguous
$ <script> /tmp/lc/amb/W c266
MISSING c266        EXIT=1
```

Cause: line `:133` treats any `cat-file -e` failure as absence. Only reachable for ambiguous 4–39-hex input;
full 40-hex names are unaffected. Statement "MISSING = object absent locally" is therefore not universally true.

## 5. B1/B2 — shallow warning is CWD-dependent (FALSIFIES the wave's claim)

The wave-1 report (`w1/reports/LandedCheck.md` §2) says: *"A shallow clone additionally gets a stderr warning
because ancestry is bounded by the shallow boundary (`:113-116`)."* It does not, unless the caller happens to
stand inside the lane.

```
$ git -C /tmp/lc2/shal rev-parse --git-path shallow
.git/shallow                       ← RELATIVE path
```
and `.ufo/waves/round-19/landed-check.sh:113-115` does `[ -f "$shallow" ]` **against the caller's CWD**, never
prefixed with `$LANE`.

Two-sided proof (`/tmp/lc2/sh` is a real `--depth=1` clone; `/tmp/lc8/lag` is a normal clone):

```
[A] shallow lane, caller CWD=/tmp/lc2   (documented usage: script LANE HASH)
    landed-check.sh: origin/master = 6fb792b7… (object present locally)
    LANDED 6fb792b74a127db278d0503b2342822598f71367
    → NO warning

[B] same lane, caller CWD=/tmp/lc2/sh   (inside the lane)
    landed-check.sh: warning: shallow clone — ancestry is bounded by the shallow boundary (false LOCAL_ONLY possible)
    → warning appears

[C] NOT-shallow lane /tmp/lc8/lag, caller CWD=/tmp/lc2/sh (an unrelated shallow repo)
    landed-check.sh: warning: shallow clone — …
    → SPURIOUS warning about a non-shallow lane
```

(A linked worktree is not affected: `rev-parse --git-path shallow` returns an absolute
`/tmp/lc2/seed/.git/shallow` there. The defect is specific to normal checkouts — which is what the live lane is.)

**B2 — the failure the warning exists for, reproduced with the warning dead:**

```
/tmp/lc2/sh: depth-1 clone; C3 = tip (6fb792b7), C1 = 8f29dfc8 fetched directly with --depth=1
  git -C /tmp/lc2/sh merge-base --is-ancestor C1 C3 → rc=1        (history cut)
  independent truth in the full clone: C1 is on origin/master → YES
  <script> /tmp/lc2/sh 8f29dfc8…        (caller CWD=/tmp/lc2, i.e. documented usage)
    LOCAL_ONLY 8f29dfc8… (ancestor of neither refs/heads/master nor origin/master 6fb792b7…)
    EXIT=1
  (no shallow warning on stderr)
```

So a landed commit is reported as "ancestor of neither" with exit 1, silently — the stdout reason is also a
false statement of fact (it *is* an ancestor of origin/master; the tool's view is truncated). The mitigation
the wave advertises does not run in the documented invocation. [INFERENCE] realistic trigger: a shallow lane
that has fetched more than one tip (`--depth=1 --no-single-branch`, or an extra `fetch --depth`), then
classifying a commit whose ancestry path to the tip was cut.

## 6. B3 — `LANDED` is replace/graft-sensitive (bounded, no live exposure)

`git merge-base --is-ancestor` honours `refs/replace/*` and `.git/info/grafts`; the script never sets
`GIT_NO_REPLACE_OBJECTS`. Demo `/tmp/lc3` (throwaway): origin master tip `T=c7c3e7bd…`; `X=fd2d2cdb…` is a
root commit that exists only locally (`git -C seed cat-file -e X` → absent):

```
$ git -C L replace --graft T X
$ git -C L merge-base --is-ancestor X T        → rc=0
$ <script> /tmp/lc3/L fd2d2cdb…                → LANDED fd2d2cdb…   EXIT=0   ← FALSE
$ GIT_NO_REPLACE_OBJECTS=1 <script> …          → LOCAL_ONLY fd2d2cdb… (ancestor of neither …)  EXIT=1
```

Live exposure check on the lane:

```
git -C <lane> for-each-ref refs/replace → (empty, 0 rows)
ls <lane>/.git/info/grafts              → No such file or directory
```

So today the lane cannot produce this; it is a latent overclaim of "LANDED = on origin/master", flippable by
ambient repo state the tool neither pins nor reports.

Related, same corrupt state, different wrong verdict (and the documented `ancestry test … errored rc=N` reason at
`:23`/`:152` was **not** reached):

```
/tmp/lc6/L: .git/refs/replace/<Q> points at absent 1111…
$ git -C L merge-base --is-ancestor Q Q → rc=128 (fatal: Not a valid commit name Q)
$ <script> /tmp/lc6/L Q
landed-check.sh: origin/master = bbdfc8ff… (object ABSENT locally; no fetch performed)
LOCAL_ONLY bbdfc8ff… (object present but not a commit)     EXIT=1
```

A genuine commit is declared "not a commit", and the exit is 1, not the exit-2 "could-not-evaluate" the header
promises for ancestry errors ([UNK] whether the rc=N branch is reachable at all: `rev-parse` fails first in both
constructions I tried).

## 7. B4 — the timeout bound is conditional and the fallback is silent

Live, `timeout` present: origin rewritten to blackholed `http://192.0.2.1/x.git`

```
$ time <script> /tmp/lc5/L <hash>
landed-check.sh: git ls-remote origin refs/heads/master failed in /tmp/lc5/L
EXIT=2      wall 60.08 s        ← bound holds (timeout 60)
```

Without `timeout(1)` in PATH (`/tmp/lc/bin` holds only `git`+`awk`; `command -v timeout` → NO-TIMEOUT):

```
$ PATH=/tmp/lc/bin timeout 75 /usr/bin/bash <script> /tmp/lc5/L <hash>
EXIT=124    elapsed=75 s        ← killed by MY outer timeout; the tool itself never returned
```

`tmo()` (`:66-72`) degrades to unbounded execution with no warning, so the header claim
*"`ls-remote` is time-bounded so a dead remote cannot hang a wave"* (`:26-27`) holds only on hosts with
coreutils `timeout`. This host has it, so no live break — but the claim as written is unconditional.

## 8. B6 — the printed hash token is not stable across verdicts

Header promises `one line per HASH, input order` with `LANDED <hash>` / `LOCAL_ONLY <hash>` / `MISSING <hash>`
(`:16-24`). Actually: `LANDED` and *commit* `LOCAL_ONLY` print the resolved **full** id (`:146`, `:163/166/169/176/179`);
non-commit `LOCAL_ONLY` and `MISSING` print the **input token** (`:134`, `:136`).

```
$ <script> /tmp/lc2/seed 6fb792b            → LANDED 6fb792b74a127db278d0503b2342822598f71367
$ <script> /tmp/lc2/seed 64a9fa3            → LOCAL_ONLY 64a9fa3 (object present but not a commit)
$ <script> /tmp/lc2/seed ffff               → MISSING ffff
$ <script> /tmp/lc2/seed 6fb792b | grep -c '^LANDED 6fb792b$'   → 0
$ <script> /tmp/lc2/seed 8a5b9208…(annotated tag on master)
  → LANDED 6fb792b74a127db278d0503b2342822598f71367   ← input tag object replaced by its commit
```

Any consumer keyed on its own input hash (the natural use: iterate hashes, parse the verdict line) silently
fails for abbreviated and tag inputs. Not a false verdict, but the line grammar is inconsistent and undocumented
for this case.

## 9. The w1 sentence "HEAD is never consulted" is false at the syscall level

`w1/reports/LandedCheck.md` §2 claims *"`HEAD` is never consulted (the lane's HEAD is detached …)"*. strace of
the live run shows `"/home/vgpnk/Projects/shokunin/mado-shokunin/.git/HEAD"` opened 9 times, and **every** git
invocation opens it once (git's repo-discovery plumbing):

```
git rev-parse --git-dir                 -> HEAD opens=1
git ls-remote origin refs/heads/master  -> HEAD opens=1
git rev-parse --verify --quiet …^{commit}-> HEAD opens=1
git rev-parse --git-path shallow        -> HEAD opens=1
git cat-file -e …                       -> HEAD opens=1
git merge-base --is-ancestor …          -> HEAD opens=1
```

The *behavioural* statement survives: with HEAD detached at `HEAD~2`, a landed tip still classifies by
master/origin (`LANDED`/`LOCAL_ONLY` unchanged). So this is an overstatement in the w1 report, not a functional
defect.

## 10. Contract points that survived the attack (independently reproduced)

| case | fixture | observed | exit |
|---|---|---|---|
| pushed+unpushed mix | `/tmp/lc/B` (C1,C2 pushed; C3 not) | `LANDED C1`, `LANDED C2`, `LOCAL_ONLY C3 (ancestor of refs/heads/master, not of origin/master …)` | 1 |
| tree / blob object | `c2176264…` / `4cb29ea3…` | `LOCAL_ONLY … (object present but not a commit)` | 1 |
| true stale (tip pushed after clone) | `/tmp/lcb/stale` | `LOCAL_ONLY E1 (… remote tip … absent locally, ancestry untestable without a fetch)`, `MISSING E2`, stderr `(object ABSENT locally; no fetch performed)`; no fetch performed | 1 |
| local master behind but fetched | `/tmp/lca/lag` | `LANDED D1`, `LANDED D2` (origin-based, not local-master-based) | 0 |
| `refs/heads/master` absent locally | `/tmp/lc/B` after `branch -D master` | `LOCAL_ONLY X (not an ancestor of origin/master …; refs/heads/master absent locally)` | 1 |
| SHA-256 object format (64-hex) | `/tmp/lc/s256` | `LANDED e05de9cf…` (64-hex) | 0 |
| UPPERCASE hex | input `1A7CB8FC444E…` (`/tmp/lc/B` C1) | `LANDED 1a7cb8fc444ee71e3392d57f11e27e6cf3607adf` (accepted, lowercase printed) | 0 |
| annotated tag input | `8a5b9208…` | peels to commit, `LANDED <commit>` | 0 |
| LANE = linked worktree (`.git` is a file) | `/tmp/lc2/wt` | `LANDED` | 0 |
| order + duplicates | `D2 D1 D2 ffff` | 4 lines, input order preserved | 1 |
| usage / not-a-repo / no-origin / origin-without-master / non-hex / length 3 / length 65 | `/tmp/lc/*` | `usage` / `not a git checkout` / `git ls-remote … failed` / `origin has no refs/heads/master` / `not a hex object name` / `object name length out of range (4..64 hex)` | 2 each |

## Verdict against the wave's stated confidence

The wave-1 report marshals this tool as a read-only, matrix-green landedness gate and explicitly advertises the
shallow warning as a mitigation. Read-only, no-fetch, no-`jj`, live-tip, `MISSING`, exit map: **hold**.
The shallow warning: **breaks** (B1) and therefore so does the mitigation it advertises (B2). Replace/graft
sensitivity (B3) and the conditional timeout (B4) are narrower but real overclaims of the tool's own header.
None of these change the headline lane verdict (`9c54c56` and `01b8094` are LANDED at
`origin/master = 01b80946d92b26370d3012a7da655d00dd135154`, independently confirmed).

## Fix pointers (for the owner, not applied)
- `:113-114`: prefix with the git dir, e.g. `[ -f "$(git -C "$LANE" rev-parse --git-path shallow 2>/dev/null)" ]`
  with `--git-path` absolutised (`git -C "$LANE" rev-parse --absolute-git-dir` + basename), or test
  `git -C "$LANE" rev-parse --is-shallow-repository` — the current relative-path test is CWD-bound.
- Set `GIT_NO_REPLACE_OBJECTS=1` (and reject `.git/info/grafts`) if `LANDED` is meant to be origin-history absolute.
- Distinguish ambiguity from absence (`git cat-file -e` exit 128 + "ambiguous" vs 1) if `MISSING` must mean absent.
- Document or normalise the printed hash token (`full` for every verdict is the least surprising).

## Limits
- The `ancestry test … errored rc=N` branch (`:152`) was not reached; both corrupt-state constructions failed
  earlier in `rev-parse`/`cat-file` ([UNK] reachable at all).
- Partial/promisor clones and the `GIT_NO_LAZY_FETCH=1` claim were not exercised (would need a promisor remote and
  a way to count lazy fetches) — [UNK], carries over from w1.
- Network tests used only `file://` remotes and one blackholed `192.0.2.1` (60 s bound, 75 s no-timeout run);
  no credentials, no GitHub write, no host operations.
- One early shallow fixture (`/tmp/lc/shal`) was perturbed by a parallel fixture mutation of my own; the
  reported shallow results are from the clean `/tmp/lc2/sh` set run sequentially. An early `/tmp/lc7` "stale"
  fixture was invalid (`echo 2>>f` redirected stderr) and was rebuilt correctly as `/tmp/lc9` and `/tmp/lcb`.
- Live-lane write proof is strace-based over my single invocation; peers were touching the lane concurrently, so
  I did not rely on `.git` mtime snapshots.
- Gate integration of the tool (`tools/mado-verify.sh` mapping exit 2 → UNKNOWN) was not in scope and not checked.

## Installs
none — `git 2.56.0`, `strace`, coreutils `timeout`, bash 5.3.20 were already present; no package manager, no
network fetch of tooling.
