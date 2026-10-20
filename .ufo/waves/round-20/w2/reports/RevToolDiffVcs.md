# RevToolDiffVcs — falsified: JJ option-value collisions can hide real writes, and Git option clusters/ambiguous prefixes produce false findings

Reviewed `a4046a8216080d4004de3f268c62cf142095ac07`; `tools/mado-tripwire.py` SHA-256 `9613f510054043e71463a52b87178ee967dad8132a054159d43603876b85e27c` (the `28c6837` tool blob matches).

## Findings

### P1 — JJ subcommand lookup can miss a real push with `--ignore-working-copy`

`classify_jj()` correctly locates the top-level verb with `verb_index()` at `tools/mado-tripwire.py:588-590`, but `sub_verb()` restarts from `args.index(verb)` at `:548-564` rather than the located verb index. If a global option value equals the command token, the first occurrence is the value, not the command. With `-R git`, `sub_verb(args, "git")` sees the repository value first and resolves `git` instead of nested `push`. `classify_jj()` then misses `JJ_GIT_WRITE` and its fallback at `:604-611` returns `None` because `--ignore-working-copy` is present. That flag suppresses working-copy snapshot/update, not the external push.

Reproduction in a fresh `/tmp` JJ-colocated repo, with HOME/XDG and Git config redirected under `/tmp`:

```text
jj -R git --ignore-working-copy git push --remote origin --bookmark probe-jj
Changes to push to origin:
  bookmark: probe-jj [add to ac7fdbe7b93c]
ac7fdbe7b93c3c2308142d70f0a4613871f06b90 refs/heads/probe-jj
```

The local bare remote acquired `refs/heads/probe-jj`. The same command in synthetic scan line 5 produced no finding; the six-line scan returned `vcs_write: 4`, with findings only on lines 1, 2, 3, and 6. It also missed `jj -R bookmark --ignore-working-copy bookmark create probe3` (line 4), which independently succeeded and appeared in `jj bookmark list`. Fixture SHA-256: `81d0a9248943a0ec302e0ccd29f179d70bde797bd68c50d5a258fffad03f2dac`; scanner SHA-256: `9613f510054043e71463a52b87178ee967dad8132a054159d43603876b85e27c`.

### P2 — Short-option clusters hide help/dry-run flags from the exemptions

`git_option_flags()` stores each entire short-option token as one flag (`tools/mado-tripwire.py:631-637`), while `git_prints_or_simulates()` tests only exact `-h` and `-n` tokens (`:651-672`). Thus valid clusters such as `-nv` and `-ah` are not recognized as containing `-n`/`-h`.

Against Git 2.56.0 in a fresh `/tmp` repo, `git push -nv origin HEAD:refs/heads/probe` exited 0, printed `* [new branch] HEAD -> probe`, and left the remote ref absent (`probe_ref=absent`); `git commit -ah` exited 0 with `ok --dry-run (--[no-]all files +0 -0)`. Nevertheless, the synthetic scan reports `git:push` and `git:commit` for those commands (lines 1–2). This is a precision regression for real no-write invocations.

### P2 — Long-option value matching accepts ambiguous prefixes as unique

The comment says long value options are skipped by *unique* abbreviation (`tools/mado-tripwire.py:617-620`), but `git_option_flags()` uses `any(t.startswith(a) for t in takes)` at `:628-630`; it does not establish uniqueness. On Git 2.56.0, `git commit --fi --dry-run` exits 129 with `error: ambiguous option: fi (could be --file or --fixup)` and prints usage. The classifier treats `--fi` as a value-taking option, consumes `--dry-run` as its value, and reports `git:commit` (synthetic scan line 3), despite Git rejecting the invocation before a commit. This breaks the promised parse-options behavior for ambiguous abbreviations.

## Reviewed behavior with no additional finding

- `--` handling: `git_option_flags()` stops at `--`/`--end-of-options` (`:623-637`), and JJ help/ignore-working-copy checks use tokens before `--` (`:568-585`). The 9-case VCS selftest passed, including JJ help after `--` remaining a finding and the Git pathspec case `git commit -m x -- --help` remaining a write.
- Alias verbs: `jj help` on JJ 0.45.1 listed the default aliases `b`, `ci`, `desc`, `st`, plus `evolog` and `op`; these are present in `JJ_HELP_VERBS` (`:162-170`). `jj b --help` returned bookmark help. No missing built-in/default help alias was found.
- Per-segment exemption/dedup ordering: `scan_file()` calls classification before deduplicating per tool call (`:2036-2067`). The VCS selftest's `dry-then-write` case passed; its `git add -n . && git add .` call reports the real `git add .` only. The custom scan likewise emitted one `git:add` for the final real segment, not for the dry-run segment.
- Value-option cases covered by the VCS selftest (e.g. `-m --help`, `-m --dry-run`, `-o -n`, and stash message values) passed; no separate missing table entry was confirmed in those cases.

## Verification

Ran from the isolated clone `/tmp/mado-r20w2-RevToolDiffVcs`:

```text
python3 -I /tmp/mado-r20w2-RevToolDiffVcs/tools/mado-tripwire.py --selftest /tmp/mado-r20w2-RevToolDiffVcs/.ufo/waves/round-20/w1/patches/TwVcsHelp-dev-cases
SELFTEST_SUMMARY: 9/9 passed failed=[]
SELFTEST_SCRIPT_SHA256: 9613f510054043e71463a52b87178ee967dad8132a054159d43603876b85e27c
```

Also ran the six-call synthetic `--scan` described above and the isolated Git/JJ CLI experiments in fresh `/tmp` repositories with configuration redirected under `/tmp`. No host-side package, service, compositor, or live-gate commands were run.

## Limits

No `lsp` device was mounted: reading `xd://lsp` returned `No such tool`, and the mounted-device listing contained no LSP route. Therefore no LSP status, references, definition, or diagnostics were available; source review and runtime experiments provide the evidence here. I did not run the full precision/recall, tally, isolation, or whole-corpus checks; this review was scoped to the VCS classifier and its help/dry-run exemptions.

## Installs

none
