# CorpusDiff — stable corpus diff completed with no lost baseline rows

## Deliverables

- Added `.ufo/waves/round-20/corpus-diff.py`. It resolves the base revision and the new revision-or-path, copies both tripwire sources into a temporary directory, snapshots `.jsonl` paths and SHA-256 digests before and after scanning, scans each initial file with each copied tool in the temporary working directory, and excludes files whose bytes or path membership changed. It writes corpus-relative lost rows and grouped added rows with at most 20 command examples per group. The scanner subprocess is `python3 -I <tool> --scan <file>`; transcript code was parsed by the tripwire only and was never executed. Source pointers: `corpus-diff.py:24-51` (revision/path resolution), `:54-95` (file snapshots), `:98-124` (per-file scan), `:159-193` (temporary tool copies and stable-file filter), and `:195-239` (row comparison and examples).
- Wrote `.ufo/waves/round-20/w1/corpus/pre-vs-harmed.json`.

## Corpus comparison

Command run (exit 0):

```text
python3 -I /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-20/corpus-diff.py --base 9c54c56a6a7528675027b7f628f97a1b8d1b8e8d --new e629f73 --corpus /home/vgpnk/.omp/agent/sessions/-Projects-shokunin --out /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-20/w1/corpus/pre-vs-harmed.json
```

The command printed `{"added_groups":65,"files":5623,"lost_rows":0,"stable_files":5345,...}`. The JSON reports 91 files added and 278 changed during the scan; those 369 live-session files were excluded. The stable subset had 1,603 base findings and 7,058 harmed-tool findings: **0 lost rows**, 65 added groups, and 5,455 net added findings. The output records base tool SHA-256 `c1ae45a7573e536bdb8ad410f36782aaad9832ecae6a95b2f5c7f823d13c70cd` and harmed tool SHA-256 `367be94773d8fec5e6df91f80ac777070c407c1128f7c75b3dcaa26cc83fdb4d`.

The JSON is 104,356 bytes (under 2 MiB), SHA-256 `a85bc7fe8cb9f5923bb8b333973aa6013fa56d54570d621f987c91883ee9745f`. The script SHA-256 is `ded258752ee46cf0363c14bedde1294b268d331f499042617d0f01d2a71aeb33`. The `sha256sum`/`wc -c` output was:

```text
104356  .../w1/corpus/pre-vs-harmed.json
a85bc7fe8cb9f5923bb8b333973aa6013fa56d54570d621f987c91883ee9745f  .../w1/corpus/pre-vs-harmed.json
ded258752ee46cf0363c14bedde1294b268d331f499042617d0f01d2a71aeb33  .../round-20/corpus-diff.py
```

## HelperFn rule B review

**Non-spawn rule-B rows identified: 0; non-spawn callee names: none.** The three harmed-tool-added `package_query/pacman:-Q` eval rows were reviewed as follows:

- `2026-10-20T01-48-55-258Z_01a156ff-505a-7798-99c2-b47895c874f4/MadoR13.jsonl:470` calls `run_record` with a literal pacman argv. Its earlier same-file eval cell at `MadoR13.jsonl:437` defines `run_record`; AST inspection found `subprocess.run` in that body (code line 6) and `reset` was false. This candidate therefore has a visible spawn body, rather than a non-spawn data call.
- `.../MadoR14/MadoR14.SourceSafety.jsonl:152` and `:155` call `subprocess.run` directly.

A separate read-only AST pass over a later session snapshot also reported zero non-spawn plain-name calls with literal host-command argv across 6,174 eval cells in 5,679 unchanged files. This is supplemental evidence, not a same-snapshot re-scan. The exact `BLOCK=frozenset(['pacman','-Q','hyprland'])` regression example was not identified as a non-spawn eval call in that pass. [INFERENCE] The three package-query additions are not Rule B false positives because their logged code paths contain the spawn forms above.

## Limits

- The corpus was live: 91 new files and 278 changed files were excluded, and the result applies only to the 5,345 files byte-identical between the before/after snapshots. The script stores counts rather than a full per-file snapshot manifest in its JSON output.
- The broad AST-only pass used a later snapshot and is supporting evidence only; it did not execute transcript code and it is not a replacement for a same-snapshot row-to-source audit of every added category.
- This comparison reports row differences only; it does not establish that all 5,455 added findings are caused by HelperFn rule B. No build, lint, or test suite was run.

## Installs

none
