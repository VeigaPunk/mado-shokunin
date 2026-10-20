# RevSpecVcsHelp — E4 needs explicit clean-dry-run and option-boundary wording

## Findings

### Medium — E4 must make help recognition invocation-local and stop at `--`

The tested Git write commands print usage when `-h` follows another option: `git commit -n -h`, `git push -n -h`, `git add -n -h`, and `git clean -n -h` each emitted a `usage:` line. `git --help commit` rendered the `GIT-COMMIT(1)` manual. Thus help suppression must recognize a real help flag for the current command, not treat any `-h`/`--help` text elsewhere in the transcript as help. Git's CLI manual explicitly warns that some subcommands behave differently when other arguments accompany `-h` (`gitcli` lines 114–131); `git grep -h` means “suppress [filename] output” when used with a pattern (`git-grep` lines 108–111), not help. The current `vcs_write` scope does not classify grep, but this is a concrete reason not to implement the broader wording as a transcript-wide token search.

Honor the option terminator too. In the temporary JJ repo, `jj diff -- --help` printed `Added regular file --help: (empty)`, and `jj help diff` says `[FILESETS]...` restricts the diff to paths. Therefore `--help` after `--` is a path/fileset, not a help flag. Git's `git add` and `git commit` manuals likewise document `--` followed by `<pathspec>` and say option parsing ends there. E4 should state that `-h`/`--help` counts only when parsed as an option before `--` and not consumed as an option value; preserve operands after `--` as paths. Existing examples `git commit -m --help` and “JJ help as a flag, not an option's value” point the right way, but the Git/JJ separator boundary should be explicit.

Evidence: `/tmp/mado-r20-RevSpecVcsHelp-evidence/git-commit-after-n.txt:1` SHA-256 `726786e8…`; `git-push-after-n.txt:1` `0825ce41…`; `git-add-after-n.txt:1` `27eb7f7b…`; `git-clean-after-n.txt:1` `a99332bf…` (all start with `usage:` after the preceding `-n`). Git CLI manual `/tmp/mado-r20-RevSpecVcsHelp-evidence/git-cli-manual.txt:114-131` SHA-256 `e98bfee8…`; grep manual `git-grep-manual.txt:108-111` `ef98bb74…`; JJ path probe `jj-path-help.txt:1-2` `c332b0d2…`; JJ diff help `jj-diff-help.txt:13-17` `1ad264ea…`; JJ help-after-option `jj-diff-after-option.txt:1` `67824cc1…` starts `Usage:`.

### Low — Record `git clean -n` as a dry-run, without silently widening `vcs_write`

The per-command `-n` meanings are not interchangeable: Git's commit manual says `-n`/`--no-verify` bypasses hooks (lines 213–214), while the distinct `--dry-run` says not to create a commit (lines 356–359); `git add -n`, `git push -n`, and `git clean -n` are each documented as dry-runs. JJ's local `jj help git push` also documents `--dry-run` as “Only display what will change on the remote.” E4's commit/add/push examples are correct; add `git clean -n|--dry-run` to the dry-run semantics/control list if the generic “is a dry run” clause is meant to cover all Git commands.

Scope caveat: the current tripwire contract explicitly excludes `git clean` from `vcs_write` at `tools/mado-tripwire.py:69-71` (source SHA-256 `367be94773d8fec5e6df91f80ac777070c407c1128f7c75b3dcaa26cc83fdb4d`). `git clean -n` therefore produces no `vcs_write` row under the existing class boundary regardless; do not present it as a current classifier defect unless the class scope is intentionally expanded. Never use a generic “`-n` means dry-run” exemption: `git commit -n` still commits when there is content to commit.

Evidence: `/tmp/mado-r20-RevSpecVcsHelp-evidence/git-commit-manual.txt:213-214,356-359` SHA-256 `6def726e…`; `git-add-manual.txt:57-59` `b4db0adf…`; `git-push-manual.txt:155-156` `03df718a…`; `git-clean-manual.txt:41-44` `bc5723fc…`; `jj-git-push-help.txt:103-110` `b5461011…`. Git executable: 2.56.0, SHA-256 `2912a2a32f408c9b8122e476251b32f4b35f4c3f0c15961686ae87ca456d384c`; JJ: 0.45.1-7c41cdeb16b6b321c64e789a966b6adf723816a5, SHA-256 `cd5efc3eb281d606bf9b5523167f79661da0f8c76a5aa32d61c07c7a351b6b44`. The temporary clone was at `e629f731172b8238caffe50f152217ce56535fb4`.

## Residual risk

These checks establish local Git 2.56.0 and JJ 0.45.1 behavior only. Help/parser behavior can vary by Git subcommand; the implementation must use the command-specific option grammar and preserve option values and post-`--` arguments.

## Verification gaps

This was a documentation/parser-semantics review, not a tripwire execution or fixture-suite run. The lane had no unstaged or staged diff for `tools/mado-tripwire.py` at review time; its HEAD was `e629f731172b8238caffe50f152217ce56535fb4`. The `lsp` device is not mounted (`read xd://lsp` returned “No such tool”), so no LSP status/references/definition/diagnostics were available. Literal search was used only to locate source text; no grep result is treated as semantic proof. No web sources were opened.

## Limits

Did not assess other VCS subcommand option grammars or run the round-20 precision/recall suites. The temporary `jj diff -- --help` probe used an empty file named `--help` inside the authorized `/tmp` clone; no lane files were changed.

## Installs

none
