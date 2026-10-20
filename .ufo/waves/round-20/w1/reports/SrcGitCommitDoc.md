# SrcGitCommitDoc — git v2.56.0 `git commit` docs pin `--dry-run` as a non-write and `-n` as `--no-verify` (a write); `--short`/`--porcelain`/`--long`/`-z` are non-writes the E4 list omits

Scope: the round-20 tripwire E4 non-write rule, sourced at the tag matching the host git.
No fixture/case was authored; this seat delivers one SOURCES row draft and the observations behind it.

## Version binding

- Host git observed: `git --version` → `git version 2.56.0`; `/usr/bin/git` 4,968,112 B, sha256 `2912a2a32f408c9b8122e476251b32f4b35f4c3f0c15961686ae87ca456d384c`; package `/var/lib/pacman/local/git-2.56.0-1/desc` (946 B, sha256 `17bb06f616f516850f40802ac26ed21fe0406418e2d34c21d0e3eea29673b092`, mtime `2026-10-20T09:16:37-0300`) says `%VERSION%` `2.56.0-1`. Arch's `-1` is the packaging revision of upstream 2.56.0.
- Tag pin: `git ls-remote https://github.com/git/git refs/tags/v2.56.0 'refs/tags/v2.56.0^{}'` →
  `2478544319491bbd2a42cc57a83e3d2f4730a280  refs/tags/v2.56.0` (annotated tag object) and
  `a018953688f1b10bddf91bff8747068f5f4746a4  refs/tags/v2.56.0^{}` (peeled commit). The tag is annotated, so the row cites the peeled commit, not the tag object.
- Fetched bodies (receipts in `.ufo/waves/round-20/fetch/SrcGitCommitDoc/receipts.jsonl`, 2 × HTTP 200):
  - `git-commit-v2.56.0.adoc` = `Documentation/git-commit.adoc` @ v2.56.0, 21,772 B, sha256 `ec670cfacaf3df8745e9cfe2fa68b74247cb111e4208e1a0095036732cb5e717`
  - `builtin-commit-v2.56.0.c` = `builtin/commit.c` @ v2.56.0, 62,305 B, sha256 `e566f2092ed52b6a1afa87ed62cd5bed7d18dd9723a990fcca9265ad46a18025`

## Observed facts in the fetched bytes

Documentation (`git-commit.adoc`, all line numbers in the fetched body):

- `:12` SYNOPSIS lists `[--dry-run]`.
- `:56-58` "The `--dry-run` option can be used to obtain a summary of what is included by any of the above for the next commit by giving the same set of parameters (options and paths)."
- `:378-381` `--dry-run`:: "Do not create a commit, but show a list of paths that are to be committed, paths with local changes that will be left uncommitted and paths that are untracked." → **non-write**.
- `:218-221` `-n`:: `--verify`:: `--no-verify`:: "Bypass the `pre-commit` and `commit-msg` hooks." → **`-n` is the no-verify synonym; the doc never ties `-n` to `--dry-run`**.
- `:144-146` `--short` "Implies `--dry-run`."; `:152-155` `--porcelain` "Implies `--dry-run`."; `:157-160` `--long` "is the default output of git-status[1]. Implies `--dry-run`."
- `:162-166` `-z`/`--null`: "If no format is given, implies the `--porcelain` output format."

Source (`builtin/commit.c`, corroboration that the doc's implications are real in code):

- `:1750` `OPT_BOOL('n', "no-verify", &no_verify, N_("bypass pre-commit and commit-msg hooks"))` — `-n` sets `no_verify`, never `dry_run`.
- `:1751` `OPT_BOOL(0, "dry-run", &dry_run, N_("show what would be committed"))`.
- `:1725` `OPT_BOOL('s', "signoff", &signoff, N_("add a Signed-off-by trailer"))` — **`-s` is sign-off, not `--short`**; `--short` is long-only in the commit table (`:1752` `OPT_SET_INT(0, "short", …)`).
- `:1316-1317` `parse_options(...)` then `finalize_deferred_config(s)`; `:1256-1267` maps `-z` with `STATUS_FORMAT_NONE|UNSPECIFIED` to `STATUS_FORMAT_PORCELAIN` (and dies on `--long -z`).
- `:1422-1423` `if (status_format != STATUS_FORMAT_NONE) dry_run = 1;` — so `--short`, `--porcelain`, `--long`, and (via the finalize step) `-z` all force the dry-run path.
- `:1836-1837` `if (dry_run) return dry_run_commit(...)` before `prepare_index`/commit creation.
- `:1810` resets `status_format = STATUS_FORMAT_NONE` before parsing, so the `:1422` test sees only this invocation's flags.

## Empirical check on host git 2.56.0 (fixtures never in the lane)

Fresh `git init` repo per flag under `/tmp/mado-r20-srcgitcommit2/<flag>`, one commit, then
`git commit --allow-empty <flag> -m t`; write = `git rev-list --count HEAD` increased:

| flag | rc | wrote |
|---|---|---|
| (none) | 0 | YES |
| `--dry-run` | 1 | no |
| `-n` | 0 | YES |
| `--short` | 1 | no |
| `--porcelain` | 1 | no |
| `--long` | 1 | no |
| `-z` | 1 | no |
| `--branch` | 0 | YES |
| `--ahead-behind` | 0 | YES |
| `--show-stash` | 129 | no — `error: unknown option 'show-stash'` (not a commit option) |
| `--no-verify` | 0 | YES |
| `-s` | 0 | YES |

Hook test (separate scratch `/tmp/mado-r20-srcgitcommit`): with an executable `pre-commit` hook that prints `HOOK-RAN` and exits 1, plain `git commit` returned rc 1 and wrote nothing; `git commit -n` returned rc 0, wrote the commit, and printed no `HOOK-RAN` — the doc's `-n` = `--no-verify` reading holds, and it still writes.

Observed: the table matches the source reading exactly, including the transitive `-z` → `--porcelain` → `--dry-run` chain. [INFERENCE] A repair can therefore key the exemption on "does this invocation set `status_format`" plus the literal `--dry-run`/help cases instead of per-flag guessing.

## Drafted SOURCES row (id reserved: S1xx-pending)

| S1xx-pending | git v2.56.0 `git commit` documentation — https://raw.githubusercontent.com/git/git/v2.56.0/Documentation/git-commit.adoc | docs | A | `git commit` dry-run vs write semantics for the round-20 tripwire E4 non-write rule, at the tag matching the host git (`git version 2.56.0`) | tag v2.56.0 → annotated tag object `2478544319491bbd2a42cc57a83e3d2f4730a280`, peeled commit `a018953688f1b10bddf91bff8747068f5f4746a4` (`git ls-remote` refs/tags/v2.56.0 and `refs/tags/v2.56.0^{}`); raw `Documentation/git-commit.adoc` 21,772 B sha256 `ec670cfacaf3df8745e9cfe2fa68b74247cb111e4208e1a0095036732cb5e717` — `--dry-run` at :378-381 ("Do not create a commit, but show a list of paths that are to be committed"), `-n`/`--verify`/`--no-verify` at :218-221 ("Bypass the `pre-commit` and `commit-msg` hooks"), `--short` :144-146 / `--porcelain` :152-155 / `--long` :157-160 ("Implies `--dry-run`"), `-z`/`--null` :162-166 ("If no format is given, implies the `--porcelain` output format"); corroborating `builtin/commit.c` 62,305 B sha256 `e566f2092ed52b6a1afa87ed62cd5bed7d18dd9723a990fcca9265ad46a18025` — `OPT_BOOL('n', "no-verify", …)` :1750, `OPT_BOOL(0, "dry-run", …)` :1751, `OPT_BOOL('s', "signoff", …)` :1725, `finalize_deferred_config` after `parse_options` :1316-1317 with `-z` → PORCELAIN at :1262-1267, `if (status_format != STATUS_FORMAT_NONE) dry_run = 1;` :1422-1423, early `dry_run_commit` return :1836-1837; host binding `/usr/bin/git` 4,968,112 B sha256 `2912a2a32f408c9b8122e476251b32f4b35f4c3f0c15961686ae87ca456d384c`, `git --version` → `git version 2.56.0`, `/var/lib/pacman/local/git-2.56.0-1/desc` `%VERSION%` `2.56.0-1`; observed on the host under `/tmp/mado-r20-srcgitcommit2` (fresh repo per flag): `--dry-run`, `--short`, `--porcelain`, `--long`, `-z` create no commit; `-n`, `--no-verify`, `-s`, `--branch`, `--ahead-behind` do | `--dry-run` is a non-write and `-n` is a synonym of `--no-verify`, not of `--dry-run`, so `git commit -n` writes (bypassing hooks); `--short`/`--porcelain`/`--long` imply `--dry-run` and `-z` implies `--porcelain`, so those four create no commit either — an E4 exemption list that only names the literal `--dry-run` still mislabels them; `-s` is `--signoff` (writes) and must not be read as `--short`; `--branch`/`--ahead-behind` write, `--show-stash` is not a commit option (rc 129) | mined | 2026-10-20 | on-release | corpus/knowledge/tripwire-precision-r20.md (draft), .ufo/waves/round-20/w1/reports/SrcGitCommitDoc.md |

Note on the `used-by` column: `corpus/knowledge/tripwire-precision-r20.md` is the ScribeProvince draft that already cites `S1xx-pending` for git help/dry-run; L1 should reconcile the id and the `used-by` list at integration.

## E4 implications (for TwVcsHelp / L1; the contract's enumerated list is not exhaustive)

1. **Missing non-writes.** Doc `:144-160` and source `:1422-1423` make `git commit --short`, `git commit --porcelain`, `git commit --long` dry runs; doc `:162-166` + source `:1316-1317`/`:1262-1267` make `git commit -z`/`--null` a dry run too. E4's governing clause ("no vcs_write row when the invocation … is a dry run") therefore requires clean rows for these four; the enumerated list only contains `--dry-run`. Host observation agrees (no commit for all four).
2. **`-n` stays a write.** Doc `:218-221` and source `:1750` put `-n` under `--verify`/`--no-verify`; the hook test shows it writes while bypassing hooks. E4's negative case is confirmed, and a classifier must not map `-n` to dry-run.
3. **`-s` is not `--short`.** Source `:1725` maps `-s` to `--signoff`; `--short` has no short letter in the commit table (`:1752`). A blanket "`-s` = short status" mapping would wrongly exempt a writing `git commit -s`. Host observation: `-s` writes.
4. **Status-ish flags that still write:** `--branch` and `--ahead-behind` (source `:1753`, `:1755-1756`) set only display fields, leave `status_format` NONE, and retain `dry_run = 0`; host observation: both write. Do not sweep them into the dry-run exemption. `--show-stash` is rejected by `git commit` (rc 129).
5. **Current lane tool has no exemption at all** (observed): `tools/mado-tripwire.py:138` lists `commit` in `GIT_WRITE`, and `classify_git` at `:524-529` returns `"git:"+verb` without inspecting options. Probe at tool sha256 `367be94773d8fec5e6df91f80ac777070c407c1128f7c75b3dcaa26cc83fdb4d` (the 1f7f995/e629f73 hash): `/tmp/sg-probe/probe.jsonl` (sha256 `b333d6a62e10ae4bbd31c4f758dc0250235b752dc6a2020d208a9d0ecff8913f`; three bash cells `git commit -m x`, `git commit --dry-run`, `git commit --help`) scanned by `python3 -I tools/mado-tripwire.py --scan` gives `{"counts": {"host_mutation": 0, "live_probe": 0, "package_query": 0, "tool_install": 0, "vcs_write": 3}, "exit": 1, ...}` with three rows `"rule": "git:commit"` at lines 1-3 and no `evidence` key. So at e629f73 every `git commit` line, including `--dry-run` and `--help`, is a `vcs_write` finding; the E4 repair owns that.
6. [INFERENCE] Combined/clustered short flags (e.g. `-sn`, `-n -a`, `-vz`) follow getopt letter parsing and need per-letter handling; I did not test clusters, so do not treat this as observed.

## Limits

- Not checked: `git commit -h` / `--help` / `git help commit` behavior and exit codes (generic parse-options/help path; belongs to the help side of E4 and to other seats), `jj` help/dry-run, `git add -n` / `git push -n` (separate source row owner), `--porcelain=v2`, clustered short options, `--fixup`/`--amend` combinations, hook-path/config interactions, and whether docs from the host package (`/usr/share/doc`) match the raw tag bytes (raw bytes used as the anchor instead).
- The `--show-stash` rc 129 is an observation about the commit option table, not about `git status`.
- No lane file was edited and no gate/regression was run. Fixtures live only in `/tmp/mado-r20-srcgitcommit{,2}` and never execute tripwire-scanned text.
- [UNK] Which SOURCES id L1 assigns (`S1xx-pending` here; S099-S110 are reserved to L1).

## Installs

none.
