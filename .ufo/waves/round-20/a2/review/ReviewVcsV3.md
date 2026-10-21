# ReviewVcsV3 — falsified: v3.1 fixes the listed parser cases, but still misses real jj and Git database writes

## Findings

### SEVERE — parsed `--ignore-working-copy` suppresses jj repository mutations

**Reproduction input:** `../../../../../tmp/mado-r20a2-ReviewVcsV3/vcs-v3-forms.jsonl`, SHA-256 `4a93576c5f436c0ea58eadb672745d2dba6dbc2dd3c8c925d72a8f96e3dfbd4b` (lines 4–6). The scans were run with:

```sh
python3 -I ../../../../../tmp/mado-r20a2-ReviewVcsV3/tw-a8960de.py --scan ../../../../../tmp/mado-r20a2-ReviewVcsV3/vcs-v3-forms.jsonl
python3 -I ../../../../../tmp/mado-r20a2-ReviewVcsV3/tw-28c6837.py --scan ../../../../../tmp/mado-r20a2-ReviewVcsV3/vcs-v3-forms.jsonl
```

All three commands below were run in fresh jj repos with the temporary HOME/XDG/config environment described under Limits. The measured state changes are writes despite `--ignore-working-copy`:

- From `../../../../../tmp/mado-r20a2-ReviewVcsV3/measure2/jj`: `jj -R remote-add --ignore-working-copy git remote add origin remote-add-bare.git` exited 0. `jj git remote list` then returned `origin /tmp/mado-r20a2-ReviewVcsV3/measure2/jj/remote-add-bare.git`; the repo's Git remote configuration changed. Expected: a `vcs_write` finding. Observed at both `a8960de` and `28c6837`: `clean`.
- From the same cwd: `jj -R forget --ignore-working-copy bookmark forget probe` exited 0 with `Forgot 1 local bookmarks.` The `probe` bookmark, created immediately before the test, was absent from the subsequent `jj bookmark list`. Expected: a `vcs_write` finding. Observed at both revisions: `clean`.
- From the same cwd: `jj -R ws --ignore-working-copy workspace add workspace-added` exited 1 with `Error: This command must be able to update the working copy. Hint: Don't use --ignore-working-copy.` It nevertheless created the destination and registered `workspace-added`; subsequent `jj workspace list` showed that workspace. Expected: a `vcs_write` finding even on this partial-failure path. Observed at both revisions: `clean`.

The v3.1 implementation makes these misses reproducible: `tools/mado-tripwire.py:187-192` only enumerates bookmark writes set/move/create/delete and jj git writes push/fetch; `tools/mado-tripwire.py:623-649` then returns `None` for other parsed subcommands whenever `--ignore-working-copy` is present. This is not merely a working-copy snapshot: the tested commands change remote configuration, bookmark state, or workspace state. The workspace case also demonstrates a failed command can leave a write behind.

### SEVERE — Git dry-run classification misses object/index writes

**Reproduction input:** `../../../../../tmp/mado-r20a2-ReviewVcsV3/vcs-v3-forms.jsonl`, SHA-256 `4a93576c5f436c0ea58eadb672745d2dba6dbc2dd3c8c925d72a8f96e3dfbd4b` (lines 11 and 15).

- In a fresh Git 2.56.0 repo with untracked `new.txt`, `git add -Nn new.txt` exited 0 and printed `add 'new.txt'`. It left `new.txt` untracked and created no index entry, but added the empty-blob object `e69de29bb2d1d6434b8b29ae775ad8c2e48c5391` under `.git/objects`. Expected for a measured repository write: a `vcs_write` finding. Observed at `a8960de`: `clean`; at `28c6837`: `vcs_write:git:add`.
- In a fresh repo with a staged tracked-file modification, `git commit -zn` exited 0 and printed `M f\0`; HEAD stayed at `bb5bcd4ac57c71c1510fa6c3b816e839d623b45d`, so it did not create a commit. It nevertheless changed `.git/index` (SHA-256 `8b72d94e…` → `4820d285…`) and created an unreferenced tree object (`a1cf8f84…`). Expected for those measured repository database writes: a finding. Observed at `a8960de`: `clean`; at `28c6837`: `vcs_write:git:commit`.

At `tools/mado-tripwire.py:680-712`, `-n` suppresses add/push findings and commit `-z` sets the dry-run/null exemption; that classification misses these observed object/index writes. This is an explicit regression in the two fixtures relative to `28c6837`. Both commands left the commit/ref state unchanged, but the on-disk Git database changed. The tripwire docstring's dry-run note already permits unreferenced objects for commit dry-runs; here the index also changed, contrary to the source comment that the exemption leaves the index untouched. [INFERENCE] If the intended meaning of `vcs_write` excludes object-database writes and index refreshes, that narrower definition would need to be stated; the literal measured-write acceptance criterion counts them.

### MODERATE — `uv tool run --help` is flagged when it only prints the runner's help

**Reproduction input:** `../../../../../tmp/mado-r20a2-ReviewVcsV3/vcs-v3-forms.jsonl`, SHA-256 `4a93576c5f436c0ea58eadb672745d2dba6dbc2dd3c8c925d72a8f96e3dfbd4b` (line 37). `uv tool run --help`, with `UV_TOOL_DIR` and `UV_CACHE_DIR` under `/tmp`, exited 0 and printed uv's own usage; neither directory changed. Expected: no acquisition finding because the command has no package operand and performs no fetch/install. Observed at both `a8960de` and `28c6837`: `tool_install:uv:tool-run`.

`tools/mado-tripwire.py:996-1023` includes `run` in the uv tool-install classifier but excludes it from `HELP_EXEMPT_INSTALLS`, so the bare runner help form is always flagged. The package-operand variants were scan-only (see Limits); this finding is specifically the measured no-package command.

### LOW — v3.1 conservatively flags shell lines Bash rejects before running

**Reproduction input:** `../../../../../tmp/mado-r20a2-ReviewVcsV3/vcs-v3-forms.jsonl`, SHA-256 `4a93576c5f436c0ea58eadb672745d2dba6dbc2dd3c8c925d72a8f96e3dfbd4b` (lines 20–23). Each line was checked with `bash -n -c <line>` only (no command execution); all returned exit 2, `unexpected EOF while looking for matching \`'`, so these exact shell lines execute no VCS/installer command.

`a8960de` emits `git:add/unparsed`, `git:push/unparsed`, `jj:git/unparsed`, and `uv:tool-install/unparsed`; `28c6837` is clean for the first three and reports the installer line. Expected against measured shell behavior: no write/no finding for these malformed lines. This is a precision over-flag, not a missed-write case; the v3.1 result follows its stated conservative no-exemption rule for an unparsed segment.

## Per-form measurements

Host versions: `git version 2.56.0`; `jj 0.45.1-7c41cdeb16b6b321c64e789a966b6adf723816a5`. Git and jj tests used fresh repos under `../../../../../tmp/mado-r20a2-ReviewVcsV3/measure2` or `measure3`; HOME, XDG_CONFIG_HOME, GIT_CONFIG_GLOBAL, JJ_CONFIG, UV_TOOL_DIR, UV_CACHE_DIR, CARGO_HOME, PIP_CACHE_DIR, and npm cache were redirected into `/tmp`. The fixture is scanned as data only. `clean` means no per-line finding.

| Fixture line | Command form | Measured behavior | `a8960de` | `28c6837` |
|---:|---|---|---|---|
| 1 | `jj -R git --ignore-working-copy git push --remote origin --bookmark main` | Write: exit 0; remote `refs/heads/main` created and jj repo changed. | `vcs_write:jj:git` | clean |
| 2 | `jj -R bookmark bookmark create probe -r @` | Write: bookmark created. | `vcs_write:jj:bookmark` | `vcs_write:jj:bookmark` |
| 3 | `jj -R bookmark-iwc --ignore-working-copy bookmark create probe -r @` | Write: bookmark created. | `vcs_write:jj:bookmark` | `vcs_write:jj:bookmark` |
| 4 | `jj -R remote-add --ignore-working-copy git remote add origin remote-add-bare.git` | Write: remote configuration changed; command succeeded. | clean | clean |
| 5 | `jj -R forget --ignore-working-copy bookmark forget probe` | Write: local bookmark forgotten; command succeeded. | clean | clean |
| 6 | `jj -R ws --ignore-working-copy workspace add workspace-added` | Partial write: destination/workspace registered; command exited 1. | clean | clean |
| 7 | `jj -R drypush --ignore-working-copy git push --remote origin --bookmark main --dry-run` | No repo or remote change in the tested up-to-date case. | clean | clean |
| 8 | `git add -nv new.txt` | No repo change; printed `add 'new.txt'`. | clean | `vcs_write:git:add` |
| 9 | `git add -An new.txt` | No repo change; printed `add 'new.txt'`. | clean | `vcs_write:git:add` |
| 10 | `git push -nv origin main` | No local/remote content change; dry-run reported the new branch. | clean | `vcs_write:git:push` |
| 11 | `git commit -zn` | Write: index and unreferenced tree changed; HEAD unchanged. | clean | `vcs_write:git:commit` |
| 12 | `git commit -ah` | No repo change; printed usage/help. | clean | `vcs_write:git:commit` |
| 13 | `git commit -am msg` | Write: commit created. | `vcs_write:git:commit` | `vcs_write:git:commit` |
| 14 | `git commit -mfoo` | Write: commit created with message `foo`. | `vcs_write:git:commit` | `vcs_write:git:commit` |
| 15 | `git add -Nn new.txt` | Write: unreferenced empty blob created; no index entry. | clean | `vcs_write:git:add` |
| 16 | `git stash push -m x` | Write: stash saved and worktree/index state changed. | `vcs_write:git:stash` | `vcs_write:git:stash` |
| 17 | `git commit -nam msg` | Write: commit created (`-n` is no-verify here, not dry-run). | `vcs_write:git:commit` | `vcs_write:git:commit` |
| 18 | `git commit -am --dry-run` | Write: commit created with message `--dry-run` (`-m` consumed the next token). | `vcs_write:git:commit` | `vcs_write:git:commit` |
| 19 | `git pull -n` | Write: fast-forwarded to an incoming remote commit. | `vcs_write:git:pull` | `vcs_write:git:pull` |
| 20 | `git add -n 'unterminated` | Not executed; `bash -n` rejects the line. | `vcs_write:git:add/unparsed` | clean |
| 21 | `git push --help 'unterminated` | Not executed; `bash -n` rejects the line. | `vcs_write:git:push/unparsed` | clean |
| 22 | `jj -R git --ignore-working-copy git push 'unterminated` | Not executed; `bash -n` rejects the line. | `vcs_write:jj:git/unparsed` | clean |
| 23 | `uv tool install --help 'unterminated` | Not executed; `bash -n` rejects the line. | `tool_install:uv:tool-install/unparsed` | `tool_install:uv:tool-install/unparsed` |
| 24 | `uv tool install --help` | No tool/cache change; help exit 0. | clean | `tool_install:uv:tool-install` |
| 25 | `uv tool install ruff --help` | No tool/cache change; help exit 0. | clean | `tool_install:uv:tool-install` |
| 26 | `uv tool install -h` | No tool/cache change; help exit 0. | clean | `tool_install:uv:tool-install` |
| 27 | `uv tool upgrade ruff --help` | No tool/cache change; help exit 0. | clean | `tool_install:uv:tool-upgrade` |
| 28 | `uv tool uninstall ruff --help` | No tool/cache change; help exit 0. | clean | `tool_install:uv:tool-uninstall` |
| 29 | `uv pip install ruff --help` | No tool/cache change; help exit 0. | clean | `tool_install:uv:pip-install` |
| 30 | `pip install --help` | Not measured: no `pip` executable or Python pip module. | clean | `tool_install:pip:install` |
| 31 | `cargo install --help` | No tool/cache change; help exit 0. | clean | `tool_install:cargo:install` |
| 32 | `cargo uninstall ripgrep --help` | No tool/cache change; help exit 0. | clean | `tool_install:cargo:uninstall` |
| 33 | `uvx --help` | No tool/cache change; help exit 0. | clean | clean |
| 34 | `uvx package-that-is-not-run --help` | Not run: could fetch/install a package. | `tool_install:uvx` | `tool_install:uvx` |
| 35 | `npx --help` | Help exit 0; npm wrote debug-log files only under the redirected npm cache; no package installation was performed. | clean | clean |
| 36 | `npx package-that-is-not-run --help` | Not run: could fetch/install a package. | `tool_install:npx` | `tool_install:npx` |
| 37 | `uv tool run --help` | No tool/cache change; runner help exit 0. | `tool_install:uv:tool-run` | `tool_install:uv:tool-run` |
| 38 | `uv tool run package-that-is-not-run --help` | Not run: could fetch/install a package. | `tool_install:uv:tool-run` | `tool_install:uv:tool-run` |
| 39 | `pipx run --help` | Not measured: no `pipx` executable. | `tool_install:pipx:run` | `tool_install:pipx:run` |
| 40 | `pipx run package-that-is-not-run --help` | Not measured: no `pipx`; package form also not run to avoid installation. | `tool_install:pipx:run` | `tool_install:pipx:run` |
| 41 | `npm exec --help` | Help exit 0; npm wrote debug-log files only under the redirected npm cache; no package installation was performed. | clean | clean |
| 42 | `npm exec --package=package-that-is-not-run -- package-that-is-not-run --help` | Not run: could fetch/install a package. | `tool_install:npm:exec` | `tool_install:npm:exec` |

The two npm help invocations created only `npm-cache/_logs/*-debug-0.log` files; the log records `npm exec --usage`. [INFERENCE] These are diagnostic writes rather than package acquisition, so I do not count them as a `tool_install` false negative. The actual directory change is recorded above rather than hidden.

## Limits

- Package-taking `uvx`, `npx`, `uv tool run`, `pipx run`, and `npm exec` forms were scanned but not executed because they can install/fetch packages; no package was installed. `pip install --help` and all pipx runtime cases could not be measured because those binaries/modules are absent.
- Malformed fixture lines were checked with `bash -n` only; none of their VCS/installer commands were executed.
- No LSP device/server was exposed in this session. This assignment was limited to command behavior and scanner verdicts; no semantic references/diagnostics pass was available. Runtime/routing axes are not applicable to this CLI behavior matrix.

## Installs

None. No tool or package was installed or updated.
