# RevengeVcsHelpIntent — the suite tested `jj help`, not subcommand help flags

## Reconstructed contract

Under round-20 E4, help-only invocations (`jj ... -h|--help` as a flag, and `jj help ...`) are clean. The tripwire does not implement that contract for a help flag attached to a subcommand: `jj log --help` is classified as `vcs_write / jj:log` unless it also has `--ignore-working-copy`. This is a conservative snapshot heuristic firing on a help-only invocation, not evidence that the invocation actually writes.

## Evidence chain

- **The route into the false positive is direct in the classifier.** In `tools/mado-tripwire.py:462-474`, `first_verb` skips any dash-prefixed token and returns the first positional token. For args `log --help`, that yields `log`. The current tool SHA-256 is `367be94773d8fec5e6df91f80ac777070c407c1128f7c75b3dcaa26cc83fdb4d`.
- **The exemption tests the selected verb, not help flags.** `tools/mado-tripwire.py:127-136` defines `JJ_NO_SNAPSHOT = {"help", "version"}`. `classify_jj` at `tools/mado-tripwire.py:503-521` returns clean when there is no verb (`:506-507`) or the selected verb is in that set (`:519-520`); otherwise its final fallback returns `jj:<verb>` unless `--ignore-working-copy` is present (`:521`). Thus `jj help log` is exempt because its verb is `help`, and bare `jj --help` has no verb, but `jj log --help` has verb `log` and reaches the fallback. The comment at `:506` names only top-level `jj`, `jj --version`, and `jj --help`; it does not implement a general help-flag exemption.
- **What round 19 actually tested:** `.ufo/waves/round-19/tripwire/r19-vcs/jj-ignore-working-copy-clean.jsonl:2-8` contains four `--ignore-working-copy` commands, then `jj help` (line 6), `jj --version` (line 7), and bare `jj` (line 8). Its expected case is clean with no findings (`expected.json:58-62`). It contains neither `jj --help` nor a subcommand followed by `-h`/`--help`. SHA-256: `be66ca1cb53d71f8cf4bd46623b9c121b8055cb14360afad883ab951b584189e`.
- `.ufo/waves/round-19/tripwire/r19-vcs/jj-snapshot-reads.jsonl:2-9` tests seven ordinary commands (`log`, `status`, `diff`, `bookmark list`, `op log`, `show`, `file list`, and `--repository … log`); it has no help option. The expected rows are the corresponding `jj:*` findings at lines 2-9 (`expected.json:42-55`). SHA-256: `6ff114f39e378439a964ebf51d3b27e0fab1df295deaa70b75c38ebf85f414be`.
- The suite's own summary says the clean case is one of the five negative controls, and the report says mutant M3 (“drop the `help`/`version` exemption”) is killed by `jj-ignore-working-copy-clean` (`.ufo/waves/round-19/w1/reports/TwVcsClass.md:46,57-62`). This establishes that help was tested in the narrow `jj help` command form; it does not establish coverage of help flags following subcommands. The report's behavior summary also describes `help`/`version` exceptions and the fallback separately (`:27-28`). Report SHA-256: `c19adab459f552b7cd0f96e5150eae14c201a0702b1aa9c6455c30bd6ead1224`.
- A source-level search of the r19 VCS suite for `jj` followed by `-h`/`--help`, or `jj help`, returned the root `jj help` fixture occurrence, but no `jj <sub> -h|--help` occurrence. The string is also absent from the snapshot-read fixture. This agrees with the fixture bytes above.

## Divergence and fixture that would have caught it

The code's “help/version” exemption is keyed to the *verb* (`help` or `version`), while help after a subcommand is an *option* and does not change the verb selected by `first_verb`. The fallback then treats any remaining non-exempt `jj` subcommand as a working-copy snapshot. That explains why the docstring/comment can mention top-level help while `jj <sub> --help` still gets reported.

A minimal regression case would add one assistant `bash` toolCall with command `jj log --help` (JSONL line 2 after a session header) as `jj-subcommand-help-clean.jsonl`, and an expected entry like:

```json
{
  "name": "jj-subcommand-help-clean",
  "args": ["jj-subcommand-help-clean.jsonl"],
  "want_exit": 0,
  "want_label": "clean",
  "want_findings": []
}
```

Against the current source, the predicted mismatch is exit 1 and `[{"class":"vcs_write","rule":"jj:log","line":2}]`, from the branch trace above. To pin the flag-position behavior more broadly, the same fixture could include `jj status -h` and `jj --help log`; the single `jj log --help` invocation is sufficient to catch the defect named in the question. No fixture was added, per the report-only scope.

## Confidence

High confidence in the classifier path and historical suite gap: the source and exact fixture/expected bytes are present and consistent with the report's M3 note. The round-20 E4 non-write expectation is the stipulated contract; I did not invoke `jj` to independently verify CLI behavior. No runtime test was performed.

## Limits

- The LSP device is unavailable here (`read xd://lsp` returned “No such tool”); definitions and behavior were reconstructed from the source text. Grep was used only to locate strings, not as semantic proof.
- I did not invoke `jj`, run the tripwire, or execute any fixture.
- I did not inspect jj's upstream implementation or runtime help output; therefore actual CLI behavior is not independently established beyond the round-20 contract.

## Installs

none.
