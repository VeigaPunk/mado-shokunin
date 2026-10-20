# SrcGitAddPushDoc — git v2.56.0 binds `-n` = `--dry-run` for both `add` and `push`; both write nothing, but `push -n` still runs pre-push

Round-20 C1/E4 support. Target root `/home/vgpnk/Projects/shokunin/mado-shokunin`.
All reads/copies under `/tmp/mado-r20-SrcGitAddPushDoc`; no git/jj write in the lane; no fixture code executed.

## Revision anchors (observed)

```
$ git ls-remote https://github.com/git/git refs/tags/v2.56.0 'refs/tags/v2.56.0^{}'
2478544319491bbd2a42cc57a83e3d2f4730a280	refs/tags/v2.56.0
a018953688f1b10bddf91bff8747068f5f4746a4	refs/tags/v2.56.0^{}
```

Host binary: `git version 2.56.0`, `/usr/bin/git` sha256
`2912a2a32f408c9b8122e476251b32f4b35f4c3f0c15961686ae87ca456d384c` — the same
release as the pinned manual, so the behavioral checks below bind to the documented version.

Fetched bodies (curl 8.23.0, all HTTP 200, receipts at
`.ufo/waves/round-20/fetch/SrcGitAddPushDoc/receipts.jsonl`, 9 lines):

| body | bytes | sha256 |
|---|---|---|
| `git-add.adoc` | 16,586 | `42089b80b378a7e9711dde024b7ec94a6863378164ea434a34c6af07632e65db` |
| `git-push.adoc` | 32,212 | `b68851f83be3624cba85e8e620e6271b566c4d5d818d44b4b59eb3335e6ec64c` |
| `git-commit.adoc` | 21,772 | `ec670cfacaf3df8745e9cfe2fa68b74247cb111e4208e1a0095036732cb5e717` |
| `githooks.adoc` | 29,873 | `c3aff48667535943bf368c0086567a0f313661bd0544abbb8a41ff90a0cfcdb1` |
| `add.c` | 20,606 | `c96956fdbba0943e3458fd19eaad9e5a21e9953b42f03109abb17b023f76c09b` |
| `push.c` | 27,877 | `a6c0dc07673363a9c5753f054711ed5879b29b00517208fe3e0ef616a5263779` |
| `parse-options.h` | 19,624 | `87e2be30e54631812165cf2e489116fe476e5edce7b92221dd1f4cdfa0e2d6d1` |
| `transport.c` | 49,476 | `760ca6713a06d54f8362dc14b606e3960cd87ac672d43886ae2b14182eafb412` |
| `read-cache.c` | 114,464 | `d4d9584c83c396b24307f6beb9d392f7a542bfd61235b6f73a72a72bea4bda62` |

Source paths are `Documentation/<name>.adoc`, `builtin/<name>.c`, and top-level
`parse-options.h`, `transport.c`, `read-cache.c`, all at tag `v2.56.0` (commit
`a018953688f1b10bddf91bff8747068f5f4746a4`).

## Findings (observed first, inference marked)

1. **`git add`: `-n` and `--dry-run` are one option, and it writes nothing.**
   `Documentation/git-add.adoc:11` synopsis `git add [--verbose | -v] [--dry-run | -n] …`;
   `:67-70` declares `-n`:: then `--dry-run`:: with the body
   "Don't actually add the file(s), just show if they exist and/or will be ignored."
   `builtin/add.c:262` `OPT__DRY_RUN(&show_only, N_("dry run"))`, and
   `parse-options.h:568` defines `#define OPT__DRY_RUN(var, h)  OPT_BOOL('n', "dry-run", (var), (h))`
   — so the short `-n` is the same parse-options entry, not a lookalike.
   No-write path in source: `add.c:571-573` sets `ADD_CACHE_PRETEND` from `show_only`;
   `read-cache.c:735` suppresses object writes (`hash_flags = pretend ? 0 : INDEX_WRITE_OBJECT`)
   and `:812-813` discards the cache entry instead of adding it; `add.c:691-692`
   `write_locked_index(…, COMMIT_LOCK | SKIP_IF_UNCHANGED)`.

2. **Behavior matches the doc, at the same release (observed, /tmp repo).**
   Payload was two text files in a fresh `/tmp/mado-r20-SrcGitAddPushDoc/repo`; commands are
   `git add -n b.txt` and a byte/mtime hash of `.git/index`:
   ```
   add -n rc 0  out: add 'b.txt'
   index same bytes: True   same mtime: True   lock left: False
   objects: count: 3   (unchanged: no blob written for b.txt)
   status: ?? b.txt      git ls-files --error-unmatch b.txt -> rc 1
   ```
   The `-N` counter-case is a write at the same release:
   ```
   git add -N b.txt   rc 0    git ls-files --error-unmatch b.txt -> rc 0
   ```
   `Documentation/git-add.adoc:157-163`: "Record only the fact that the path will be added
   later. An entry for the path is placed in the index with no content." So E4's add line must
   keep `-N` (capital) OUT of the non-write set. `:176-180` also makes `--ignore-missing`
   valid only with `--dry-run` (`add.c:523-524` dies otherwise).

3. **`git push`: `-n` and `--dry-run` are one option and it sends/records no update (observed).**
   `Documentation/git-push.adoc:12` synopsis `[-n | --dry-run]`; `:161-163` declares `-n`:: then
   `--dry-run`:: with "Do everything except actually send the updates."
   `builtin/push.c:716` `OPT_BIT('n', "dry-run", &flags, N_("dry run"), TRANSPORT_PUSH_DRY_RUN)`.
   Source: `transport.c:964` forwards the flag as `args.dry_run`; `:1599-1607` skips the
   `transport_update_tracking_ref` loop entirely under `TRANSPORT_PUSH_DRY_RUN`.
   Observed against a fresh bare repo at `/tmp/.../remote.git`:
   ```
   git push -n origin HEAD:master   rc 0
   stderr: To /tmp/mado-r20-SrcGitAddPushDoc/remote.git
            * [new branch]      HEAD -> master
   remote  refs/heads/master          -> rc 128 (absent)
   local   refs/remotes/origin/master -> rc 128 (absent)
   git push --dry-run origin HEAD:master -> same rc/out
   ```

4. **Caveat for E4 case authors: `push --dry-run` is not side-effect free (observed + source).**
   With `--dry-run` and no `--no-verify`, the pre-push hook still runs: a canary hook in
   `.git/hooks/pre-push` wrote its file on the dry-run (`canary exists: True`), because
   `transport.c:1525-1526` calls `run_pre_push_hook` gated only by `TRANSPORT_PUSH_NO_HOOK`.
   `Documentation/githooks.adoc:235-236` says the hook "is called by linkgit:git-push[1]" and
   gives no dry-run carve-out. `transport.c:1497` also fetches the remote ref list, so the remote
   *is* contacted; the doc's
   "everything except actually send the updates" covers exactly the update transmission.
   The tripwire's `vcs_write` class is about the command's own write; a fixture that asserts
   “no process/filesystem effect” for `git push --dry-run` would be wrong.

5. **Adjacent boundary, not in E4's list: `git add --refresh` does rewrite the index.**
   `Documentation/git-add.adoc:165-167` says "Don't add the file(s), but only refresh their
   stat() information in the index"; `add.c:599-601` routes it to `refresh()`, then `:691`
   writes the index. Observed after `touch`ing a tracked file without content change:
   `git add --refresh a.txt` → index bytes changed `True`, mtime changed `True`. Same repo,
   `git add -n a.txt` → index changed `False`. [INFERENCE] A strict “non-writing” reading must
   not fold `--refresh` into the dry-run exemption; E4's paragraph does not, and this evidence
   keeps it that way.

6. **`git commit -n` is a write, as E4 says.** `Documentation/git-commit.adoc:218-221`:
   `-n`:: / `--verify`:: / `--no-verify`:: "Bypass the `pre-commit` and `commit-msg` hooks."
   So the `-n` spellings are not symmetric across subcommands, and `git add -n` / `git push -n`
   must not be generalized to `git commit -n`. Observed doc text; not executed.

## Drafted source rows (11-column shape of `corpus/SOURCES.md`; ids assigned by L1)

| id | source | kind | tier | scope | anchor | teaches | status | opened | recheck | used-by |
|---|---|---|---|---|---|---|---|---|---|---|
| S1xx-pending (git-add) | git v2.56.0 manual — `git add` dry-run option — https://raw.githubusercontent.com/git/git/v2.56.0/Documentation/git-add.adoc | docs | A | `git add` `-n`/`--dry-run` at the v2.56.0 tag: one option that stages nothing, plus its `-N` and `--ignore-missing` boundaries (C1/E4 non-write) | tag v2.56.0 → commit a018953688f1b10bddf91bff8747068f5f4746a4 (tag object 2478544319491bbd2a42cc57a83e3d2f4730a280); Documentation/git-add.adoc:11, :67-70 (quote at :69-70), :157-163, :176-180; file 16,586 B sha256 42089b80b378a7e9711dde024b7ec94a6863378164ea434a34c6af07632e65db; binding builtin/add.c:262 + parse-options.h:568 (`OPT_BOOL('n', "dry-run", …)`), sha256 c96956fdbba0943e3458fd19eaad9e5a21e9953b42f03109abb17b023f76c09b / 87e2be30e54631812165cf2e489116fe476e5edce7b92221dd1f4cdfa0e2d6d1; no-write path read-cache.c:735, :812-817 | "Don't actually add the file(s), just show if they exist and/or will be ignored." (:69-70) — `-n` is the short form of `--dry-run`, adds no index entry and writes no object, while `-N` (intent-to-add) does write one; grounds E4’s add non-write row with its `-N` negative | queued | 2026-10-20 | on-release | — (draft, L1 assigns) |
| S1xx-pending (git-push) | git v2.56.0 manual — `git push` dry-run option — https://raw.githubusercontent.com/git/git/v2.56.0/Documentation/git-push.adoc | docs | A | `git push` `-n`/`--dry-run` at the v2.56.0 tag: one option that transmits no update and skips remote-tracking writes, while still contacting the remote and running pre-push (C1/E4 non-write) | tag v2.56.0 → commit a018953688f1b10bddf91bff8747068f5f4746a4; Documentation/git-push.adoc:12, :161-163 (quote at :163); file 32,212 B sha256 b68851f83be3624cba85e8e620e6271b566c4d5d818d44b4b59eb3335e6ec64c; binding builtin/push.c:716 (`OPT_BIT('n', "dry-run", …, TRANSPORT_PUSH_DRY_RUN)`), sha256 a6c0dc07673363a9c5753f054711ed5879b29b00517208fe3e0ef616a5263779; effects transport.c:964, :1497, :1525-1526, :1599-1607 | "Do everything except actually send the updates." (:163) — `-n` is the short form of `--dry-run`; it reports would-update refs, sends no update and skips remote-tracking writes, but still contacts the remote and runs the pre-push hook, so non-write ≠ no side effects | queued | 2026-10-20 | on-release | — (draft, L1 assigns) |

Quotes are 14 and 7 words (limit 25). Both rows are docs tier A at a release tag, so the
recheck clock is `on-release`, matching S018/S096-style anchors. `status=queued` reflects
“opened and read, not yet cited by a corpus document”; L1 flips it to `mined` and fills
`used-by` if a round-20 corpus/lesson file cites it.

## What this changes for C1/E4

- `git add -n`, `git add --dry-run`, `git push -n`, `git push --dry-run` are confirmed
  non-writing in the manual and in the same-release binary — E4's two rules are evidence-backed.
- Keep `git add -N` (intent-to-add) and `git commit -n` (`--no-verify`) as writes; both are
  observed in the pinned manuals, and `-N` was observed writing an index entry.
- Do not claim `git push --dry-run` is effect-free: the pre-push hook ran (observed) and the
  remote ref list is fetched (`transport.c:1497`). This is a limit on what a C1 case may assert,
  not a contradiction of the `vcs_write` classification.

## Limits

- Network behavior of `push --dry-run` was checked only against a local bare-path remote; the
  "contacts the remote" statement is from `transport.c:1497` and the manual, not observed over
  a network transport.
- Did not exercise `git add -n --ignore-missing`, `--pathspec-from-file`, `--chmod`, or
  `push --dry-run --porcelain/--force-with-lease` combinations; only the plain forms above.
- Did not empirically check `git add -n` exit status when a pathspec matches nothing
  (`add.c:651` dies); not needed for the text-scanning rule.
- `git commit -n` was read in the manual only; not executed (behavior well known, but not
  claimed here beyond the quoted text).
- No LSP server applies: the evidence is upstream `.adoc`/C text at a tag plus `/tmp` runs of
  the host `git`; no language server indexes borrowed docs, so claims are line-anchored text
  and observed command output, not semantic LSP results.
- Did not inspect jj, `git stash`, or other subcommands' `-n` spellings; out of scope.

## Installs

none.
