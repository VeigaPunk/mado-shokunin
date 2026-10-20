# RevKnowledgeNote2 — holds: §2's git/jj distinctions reproduce on git 2.56.0 and jj 0.45.1, and the pinned tripwire agrees

## Findings

None. Each §2 row (knowledge note lines 45–57) matched the isolated measurements below; no table claim was falsified.

## Verification

- Reviewed snapshot: `/tmp/mado-r20w2-RevKnowledgeNote2/repo` at `a4046a8216080d4004de3f268c62cf142095ac07`. `git show --stat --oneline a4046a8216080d4004de3f268c62cf142095ac07` reported only `corpus/lessons/round-20.md | 6 +++---`; the requested note, source registry, and tool are in the snapshot but were not changed by that commit.
- Runtime versions in the isolated test environment: `git --version` → `git version 2.56.0`; `/home/vgpnk/.local/bin/jj --version` → `jj 0.45.1-7c41cdeb16b6b321c64e789a966b6adf723816a5`.
- **Lines 45–47 — Git help versus `-m` values:** in fresh repositories, `git commit --help` returned 0, printed the `GIT-COMMIT(1)` page, and left `HEAD` unchanged. `git commit -h`, `git commit -m x -h`, and `git commit -m x --help` returned 0 with usage and no commit. Conversely, `git commit -m --help` committed with subject `--help`, and `git commit -m -h` committed with subject `-h` (both rc 0). These match the first-argument rewrite/help and option-value distinction.
- **Line 48 — commit dry-run forms:** `git commit --dry-run`, `--short`, `--porcelain`, `--long`, and `-z` all returned 0 with `HEAD` unchanged and `git ls-files --stage` unchanged. For `--dry-run`, the raw `.git/index` SHA-256 changed from `94b596ec394ff835003d6c27d44815e56b44af00877ebd84192dfcf982ffe045` to `bd3af7574ed616d480d041c38511ba604ba0e34854a3b14348c782a5cc857fde`; this is consistent with the table's explicit index-cache caveat and does not indicate an index-entry change.
- **Line 49 — `git commit -n`:** `git commit -n -m probe` returned 0 and changed `HEAD`; the new subject was `probe`.
- **Line 50 — `git add -n` / `--dry-run`:** both returned 0, printed `add 'candidate.txt'`, and left the `.git/index` SHA unchanged. `git add -N candidate.txt` changed the index and produced an intent-to-add status.
- **Line 51 — `git push -n`:** against a local bare remote, `git push -n origin HEAD:refs/heads/probe` returned 0 and printed `* [new branch] HEAD -> probe`, while the remote still had no refs. A temporary `pre-push` hook wrote its `/tmp` canary (`ran`), confirming the stated hook side effect.
- **Line 52 — `-n`/`-N` on other subcommands:** `git pull -n` fast-forwarded the local branch and brought in the remote file; `git merge -n feature` moved `HEAD` to the merged branch; `git cherry-pick -n <commit>` left `HEAD` unchanged but staged the picked file; `git add -N candidate.txt` changed the index. The respective `-h` output included `pull -n`/`merge -n` “do not show a diffstat,” `cherry-pick -n, --no-commit`, and `add -N, --intent-to-add`.
- **Line 53 — jj help:** `jj help git push`, `jj describe --help`, and `jj --help` returned 0; the operation-log IDs before and after each were identical.
- **Line 54 — separated versus attached message:** `jj describe -m --help` returned 2 with `a value is required for '--message <MESSAGE>' but none was supplied`, and operation IDs were unchanged. `jj describe -m=--help` returned 0, changed the operation, and set the description to `--help`.
- **Line 55 — jj dry-run snapshot:** with a local bare remote and a pending working-copy file, `jj git push --dry-run` returned 0 (warning that the new bookmark was not tracked; `Nothing changed.`), added exactly one operation, and created a new `refs/jj/keep/<change>` ref. This reproduces the table's local snapshot/write claim; the push itself did not proceed.
- **Line 56 — jj ignore-working-copy:** with a pending file, `jj --ignore-working-copy git push --dry-run` left operation IDs unchanged.
- **Line 57 — user alias:** a temporary user alias `aliasprobe = ["util", "exec", "--", "sh", "-c", "printf ran > /tmp/.../alias-canary.txt"]` executed on `jj aliasprobe --help`; the canary contained `ran` (rc 0). This demonstrates why the unknown alias form remains classified as a write lead in the tripwire policy.
- **Tripwire scan:** copied `tools/mado-tripwire.py` from commit `28c6837` into the `/tmp` clone before running it; SHA-256 was `9613f510054043e71463a52b87178ee967dad8132a054159d43603876b85e27c`. Command: `python3 -I /tmp/mado-r20w2-RevKnowledgeNote2/repo/tools/mado-tripwire.py --scan /tmp/mado-r20w2-RevKnowledgeNote2/repo/experiments/table-calls.jsonl`. Output began `MADO_TRIPWIRE: findings`; totals were `vcs_write: 10`, all other classes 0, `observed_findings: 10`, `lead_findings: 0`, exit 1. Those 10 findings were exactly the measured write forms: `git commit -m --help`, `git commit -m -h`, `git commit -n`, `git pull -n`, `git merge -n`, `git cherry-pick -n`, `git add -N`, `jj describe -m=--help`, `jj git push --dry-run`, and the user alias `jj aliasprobe --help`. The help/dry-run/non-snapshot forms were absent. Scan input SHA-256: `26fc488059c3d52b25cdd921c14b282c2327b7648ea0a6d8c5a5ed80a74cc2bc` (27 tool-call records).
- **Source-row cross-check:** the table's cited S rows and anchors are present in `corpus/SOURCES.md:111-116`: S099 `:378-381` and `:218-221`; S100 `:67-70`; S101 `:161-163`; S102 `git.c:762-770` and its parse-options help/exit paths; S103 `command_error.rs:1113-1115` plus the dispatch/workspace anchors; S104 `push.rs:231` plus the workspace-helper and early-return anchors. These align with the source references in `tripwire-precision-r20.md:45-57`.

## Limits

- `read xd://lsp` returned `No such tool: xd://lsp`; no LSP server was available for status, references, definition, or diagnostics. No grep result is used as semantic proof.
- I checked the cited S099–S104 registry rows and their recorded anchors, but did not refetch or re-hash the upstream source bodies. The empirical tests were confined to fresh `/tmp` Git/JJ repositories, isolated `HOME`/config, and local bare remotes; they establish the pinned versions only.
- The scanner input is a constructed transcript of the corresponding tested command forms, not a captured live-session transcript.

## Installs

None.
