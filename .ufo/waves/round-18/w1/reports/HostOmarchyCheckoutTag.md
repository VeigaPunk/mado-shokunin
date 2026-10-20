# HostOmarchyCheckoutTag — is the on-disk omarchy checkout the upstream `v3.8.4` commit?

Seat: `MadoR18.HostOmarchyCheckoutTag` (scout, W1). Lane root `/home/vgpnk/Projects/shokunin/mado-shokunin`.
Target: `/home/vgpnk/.local/share/omarchy` — read as **file bytes only**; no git/jj command executed with that
checkout as repository (verified below: every local resolution comes from `packed-refs`, loose refs, reflogs,
and a hand-rolled zlib/pack-index parse). Network reads: `git ls-remote` (from a cwd outside the checkout) and
three `curl` bodies with receipts. No pacman/systemctl/omarchy-* invocation; no installs were needed.

## Verdict

| Question | Answer | Value |
|---|---|---|
| Does HEAD's commit equal the v3.8.4 (peeled) commit? | **YES** | `8fcc9d6048af4cb0e3af8512c78049857a3b53dd` |
| Is that the same commit `git ls-remote https://github.com/basecamp/omarchy refs/tags/v3.8.4*` returns? | **YES** | same OID, and it is the *only* line returned |
| Is v3.8.4 annotated or lightweight? | **lightweight** (no tag object) | packed-refs has no `^` peel line for it; GitHub ref API `object.type = "commit"` |

Confidence: **high** — three independent lines of evidence agree (on-disk ref bytes, locally decompressed commit
object whose SHA-1 recomputes to the reported OID, and remote `ls-remote` + GitHub API metadata).

Mechanical nuance worth carrying into the round: the checkout is **not detached at the tag**. `HEAD` is symbolic
to `refs/heads/master`, and the local branch `master` happens to point at the v3.8.4 commit. The remote no longer
advertises `refs/heads/master` at all; its default ref is now `refs/heads/quattro` (`3ac43659…`), which is **not**
this commit.

## Local evidence (file bytes)

`~/.local/share/omarchy/.git` is a real **directory** (`stat -c '%F' .git` → `directory`), not a gitfile or a
linked worktree; there is no `.git/worktrees` and no `objects/info/alternates`.

1. `HEAD` (23 bytes, `od -c`):
   ```
   r e f :   r e f s / h e a d s / m a s t e r \n
   ```
2. Loose `refs/heads/` is **empty**; the only loose ref anywhere is `refs/remotes/origin/HEAD`, containing
   `ref: refs/remotes/origin/quattro`.
3. `packed-refs` (40556 bytes, 518 lines, header `# pack-refs with: peeled fully-peeled sorted`) holds 517 refs:
   - line 2: `8fcc9d6048af4cb0e3af8512c78049857a3b53dd refs/heads/master` — exactly one occurrence.
   - line 508: `8fcc9d6048af4cb0e3af8512c78049857a3b53dd refs/tags/v3.8.4` — exactly one occurrence.
   - line 509 is `f0020448ca87329199de7cb12f2015ebc4a3e5e7 refs/tags/v4.0.0`; there is **no `^` line after 508**.
   - The file's single peeled line is line 512, `^13f18b2cb7286fb54f87daf571a031aa6af3d8f0`, attached to
     `refs/tags/v4.0.1` (line 511, `23ffe6792b297755f3c4a6dd799689388a884dff`). The pack-refs format therefore
     does emit peel lines for annotated tags here — v3.8.4 simply has none, i.e. it is a **lightweight tag whose
     target is the commit itself**. "Peeled commit" = `8fcc9d60…`.
4. `.git/refs/tags/` is an empty directory — no loose tag override of `v3.8.4`.
5. Reflogs (183 bytes each, single entry, zero-OID → `8fcc9d60…`, epoch `1784592575` = `2026-07-21T00:09:35Z`):
   - `.git/logs/HEAD`: `clone: from https://github.com/basecamp/omarchy.git`
   - `.git/logs/refs/heads/master`: same single `clone:` entry.
   No `checkout`, `reset`, `pull` or `commit` entry ever touched `HEAD`/`master` after the clone.
6. `ORIG_HEAD` = `8fcc9d60…`; `FETCH_HEAD` = `8fcc9d60…\t\tbranch 'master' of .` (a *self* fetch: `.git/config`
   has `[branch "master"] remote = .`, `merge = refs/heads/master`; `origin.url` = `https://github.com/basecamp/omarchy.git`).
7. The commit object is present **locally and byte-verifiable** without git: pack
   `.git/objects/pack/pack-de741f66….{idx,pack}` (1.2 GiB pack, idx v2, 72326 objects). Parsing the v2 index by
   bytes: OID found at slot 40507, pack offset 9390, pack entry header type code `1` (**commit**), declared
   uncompressed size 306. Decompressed payload is 306 bytes and SHA-1 over `"commit 306\0"+payload` recomputes to
   `8fcc9d6048af4cb0e3af8512c78049857a3b53dd` — the object at that OID *is* a commit, not a tag object, and it is
   exactly the object HEAD resolves to:
   ```
   tree 4c52b84cbfa5b477120e28c1bb492d45d2f86298
   parent 8e43c97610ee092e6e5ba4b603d1dbd5fc08fe08
   parent bc4eb93f59400e71f06fa00e00597b68fa34ad53
   author David Heinemeier Hansson <david@hey.com> 1784581535 -0700
   committer David Heinemeier Hansson <david@hey.com> 1784581535 -0700

   Merge branch 'master' into rc
   ```
8. No `refs/replace`, no `.git/info/grafts`, no `insteadOf` rewrite in global/system git config, no proxy env —
   so the `ls-remote` below really queried `github.com/basecamp/omarchy`.

Uniqueness guards: `grep -c 'refs/heads/master$'` = 1; `grep -c 'refs/tags/v3.8.4$'` = 1; loose `heads`/`tags`
dirs empty. There is no second ref that could shadow either value.

## Remote evidence

Executed from `/home/vgpnk/Projects/shokunin` (not from the checkout), 2026-10-20T15:40–15:41Z:

```
$ git ls-remote https://github.com/basecamp/omarchy 'refs/tags/v3.8.4*'
8fcc9d6048af4cb0e3af8512c78049857a3b53dd	refs/tags/v3.8.4
$ echo RC=$?
RC=0

$ git ls-remote --tags https://github.com/basecamp/omarchy 'v3.8.4*'
8fcc9d6048af4cb0e3af8512c78049857a3b53dd	refs/tags/v3.8.4

$ git ls-remote https://github.com/basecamp/omarchy 'refs/tags/v3.8.4^{}' refs/heads/master
(no output)

$ git ls-remote --symref https://github.com/basecamp/omarchy HEAD
ref: refs/heads/quattro	HEAD
3ac43659dcbf88e84d951e3ce979b48a60a7d1f2	HEAD

$ git ls-remote https://github.com/basecamp/omarchy | grep 8fcc9d60
8fcc9d6048af4cb0e3af8512c78049857a3b53dd	refs/tags/v3.8.4
```

Reading: the tag ref resolves to exactly `8fcc9d6048af4cb0e3af8512c78049857a3b53dd`; no `^{}` peeled companion is
advertised even when the peeled name is requested literally, and no other ref (branch or tag) points at that
commit; `refs/heads/master` no longer exists upstream.

GitHub API cross-checks (receipts below):
- `.../git/ref/tags/v3.8.4` → `"object": {"sha":"8fcc9d60…4b0e3af8512c78049857a3b53dd","type":"commit"}`. The
  response's canonical URL is `https://api.github.com/repositories/994093166/git/ref/tags/v3.8.4`: the
  `basecamp/omarchy` path redirects to repository id **994093166**, full name `omacom/omarchy`.
- `.../git/commits/8fcc9d60…` → `tree 4c52b84cbfa5b477120e28c1bb492d45d2f86298`, parents
  `8e43c97610ee092e6e5ba4b603d1dbd5fc08fe08`, `bc4eb93f59400e71f06fa00e00597b68fa34ad53`, author/committer
  `David Heinemeier Hansson <david@hey.com>`, `2026-07-20T21:05:35Z`, message `Merge branch 'master' into rc` —
  field-for-field identical to the locally decompressed commit object above.

## Nuance that matters for "host versions by file read": `version` says 3.8.3

`~/.local/share/omarchy/version` is exactly `3.8.3\n` (6 bytes, sha256
`0a5c29521592a324aa0381ac743c15dc552747cd89c5f5c9715e547df40258c6`). That is **not** a local divergence:
`https://raw.githubusercontent.com/basecamp/omarchy/v3.8.4/version` is byte-identical (same 6 bytes, same
sha256). The upstream v3.8.4 release commit simply still carries `version` = 3.8.3. So:
- Recording "omarchy checkout at tag v3.8.4" is correct (git ref evidence).
- Recording "omarchy version 3.8.3 (from `version` file)" is also correct but is the *release prior to the tag*;
  quoting it as 3.8.4 would be wrong, and quoting the tag alone without the file value would hide the split.
  Best is `tag v3.8.4 → commit 8fcc9d60…, whose version file reads 3.8.3`.

## Provenance timeline (observed timestamps, no git write)

- `2026-07-20T21:05:35Z` — v3.8.4 commit authored/committed by DHH (`1784581535 -0700`).
- `2026-07-21T00:09:35Z` — clone recorded in `.git/logs/HEAD` and `.git/logs/refs/heads/master`
  (`1784592575 +0000`), i.e. ~3 h after the tagged commit, with `master` created at `8fcc9d60…`.
- `2026-10-03T20:42:36Z` — filesystem ctimes of `.git/HEAD`, `.git/logs/HEAD`, `version` (`17:42 -0300`):
  the tree was materialized onto this host on 2026-10-03 (copy/rsync-like install), so fs timestamps do not
  reflect repository history.
- `2026-10-20T12:14:47Z` — `.git/logs/refs/remotes/origin/quattro` records
  `cc9a3aad… → 0a7beb7d…  ci <ci@local>  pull --autostash: fast-forward`; `packed-refs` mtime matches
  (`09:14:47 -0300`). This refreshed refs today. Note the fetched `origin/quattro` commit `0a7beb7d…` is **stale
  against upstream today** (`3ac43659…`), so local remote-tracking refs must not be read as "current upstream".
- `2026-10-20T12:49:22Z` — `ORIG_HEAD`/`FETCH_HEAD` rewritten (`09:49:22 -0300`) by a pull whose remote is `.`
  (self), `FETCH_HEAD` naming `branch 'master' of .` at `8fcc9d60…` — a no-op for HEAD.
- Throughout: `.git/logs/HEAD` still holds only the clone entry, so **HEAD has never moved since clone**.

## What this establishes / does not establish for round 18

Establishes:
- The checkout's commit is exactly upstream `v3.8.4` (`8fcc9d60…`), so any documentary note that cites
  `~/.local/share/omarchy` at tag v3.8.4 may key its source lines to that commit, not to a moving branch.
- The exact commit can be named by hash in route notes: `8fcc9d6048af4cb0e3af8512c78049857a3b53dd`.
- Lightweight tag: there is no annotated tag object and therefore no tag signature to cite.

Does not establish (kept **[UNK]**):
- **Working-tree cleanliness vs HEAD.** A git command inside the checkout is forbidden, so no `status`/`diff`
  was run. Only `version` was byte-compared (identical to the tag). `.git/index` mtime `2026-10-14 11:42:09
  -0300` shows some index refresh/checkout happened after clone; whether any tracked file was modified then is
  unverified.
- Installed omarchy **binaries/packages** and their versions — [UNK] here; this report is ref provenance only.
  (The `version`-file 3.8.3 fact above is the only content fact checked.)
- Upstream state after `2026-10-20T15:41Z`; tags are immutable objects but refs are movable, and `basecamp/omarchy`
  is a redirecting path to `omacom/omarchy` (id 994093166).

## Fetch receipts (R17-V3)

Directory: `.ufo/waves/round-18/fetch/MadoR18.HostOmarchyCheckoutTag/`; three lines in `receipts.jsonl`,
schema `mado-fetch-receipt-v1`, tool `curl 8.23.0 (x86_64-pc-linux-gnu) …`:

| body | http | bytes | sha256 |
|---|---|---|---|
| `gh-ref-tags-v3.8.4.json` | 200 | 368 | `a503d17da45fecbe7a5293c41d29a8b88fa0bf0f4b22293ca16f415f7ac9efd9` |
| `omarchy-v3.8.4-version.txt` | 200 | 6 | `0a5c29521592a324aa0381ac743c15dc552747cd89c5f5c9715e547df40258c6` |
| `gh-commit-8fcc9d60.json` | 200 | 1558 | `08df0a976a08c71f41d499b0be241063d607e1409aefa8e8474a5433485687d6` |

Requested URLs (final URLs recorded per line): `https://api.github.com/repos/basecamp/omarchy/git/ref/tags/v3.8.4`,
`https://raw.githubusercontent.com/basecamp/omarchy/v3.8.4/version`,
`https://api.github.com/repos/basecamp/omarchy/git/commits/8fcc9d60…`. All three are tag-pinned or commit-pinned;
the API URLs canonicalize to `repositories/994093166`, the same repo served under the `basecamp` path.

## Reproduction

```sh
# local refs, bytes only
cd ~/.local/share/omarchy
cat .git/HEAD; cat .git/packed-refs | sed -n '2p;508p;511,512p'
grep -c '^' .git/packed-refs; grep -c '^\^' .git/packed-refs
cat .git/logs/HEAD .git/logs/refs/heads/master
cat .git/ORIG_HEAD .git/FETCH_HEAD
# object proof (no git): idx v2 slot lookup -> pack offset 9390 -> type 1, size 306 -> sha1(commit 306\0+payload)
#   see the python snippet in the seat transcript; recomputed OID == 8fcc9d60…
# remote
git ls-remote https://github.com/basecamp/omarchy 'refs/tags/v3.8.4*'
git ls-remote --tags https://github.com/basecamp/omarchy 'v3.8.4*'
git ls-remote --symref https://github.com/basecamp/omarchy HEAD
git ls-remote https://github.com/basecamp/omarchy | grep 8fcc9d60
```

Tooling record: no install or upgrade performed (curl 8.23.0 already present); no pacman/systemctl/omarchy
commands were run; no git command was executed with the omarchy checkout as its repository.
