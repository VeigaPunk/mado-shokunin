# CaseLeadsInvisible — six L-family lead cases complete; all six fail before repair

## Findings

Added the assigned precision suite under `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-20/w1/cases/CaseLeadsInvisible/`: `cases.json` and six one- or two-line `.jsonl` fixtures. Registry entries are at `cases.json:5-15` (bare `run_record`), `:16-27` (imported `run_cmd`), `:28-39` (imported `classify_argv`), `:40-51` (opaque `run` assignment), `:52-62` (reset-cleared helper), and `:63-74` (aliased import). All case names use the `L-CaseLeadsInvisible-` prefix. Each wants exit 1 and one or two `lead` findings; the six red-before cases provide no controls.

The before comparison follows the counter rule: exit code and multiset `(class, rule, line, evidence)` must match, with a missing tool `evidence` field treated as `observed`, never `lead`. Every `1f7f995` scan found the argv as an ordinary, unmarked finding, while every `9c54c56` scan was clean. Thus both historical revisions fail every case for distinct reasons.

| Case and fixture evidence | Expected findings | Before `1f7f995` | Before `9c54c56` |
|---|---|---|---|
| `L-CaseLeadsInvisible-run-record`; `run-record.jsonl:1` | `package_query/pacman:-Q@1` (`lead`) | `fail`; exact output line: `MADO_TRIPWIRE: findings` (exit 1) | `fail`; exact output line: `MADO_TRIPWIRE: clean` (exit 0) |
| `L-CaseLeadsInvisible-import-run-cmd`; `import-run-cmd.jsonl:1` | `host_mutation/sudo@1`, `host_mutation/pacman:-S@1` (`lead`) | `fail`; exact output line: `MADO_TRIPWIRE: findings` (exit 1) | `fail`; exact output line: `MADO_TRIPWIRE: clean` (exit 0) |
| `L-CaseLeadsInvisible-import-classify-argv`; `import-classify-argv.jsonl:1` | `host_mutation/sudo@1`, `host_mutation/pacman:-S@1` (`lead`) | `fail`; exact output line: `MADO_TRIPWIRE: findings` (exit 1) | `fail`; exact output line: `MADO_TRIPWIRE: clean` (exit 0) |
| `L-CaseLeadsInvisible-opaque-runner`; `opaque-runner.jsonl:1` | `host_mutation/sudo@1`, `host_mutation/pacman:-S@1` (`lead`) | `fail`; exact output line: `MADO_TRIPWIRE: findings` (exit 1) | `fail`; exact output line: `MADO_TRIPWIRE: clean` (exit 0) |
| `L-CaseLeadsInvisible-reset-cleared-helper`; `reset-cleared-helper.jsonl:2` | `package_query/pacman:-Q@2` (`lead`) | `fail`; exact output line: `MADO_TRIPWIRE: findings` (exit 1) | `fail`; exact output line: `MADO_TRIPWIRE: clean` (exit 0) |
| `L-CaseLeadsInvisible-import-alias`; `import-alias.jsonl:1` | `host_mutation/sudo@1`, `host_mutation/pacman:-S@1` (`lead`) | `fail`; exact output line: `MADO_TRIPWIRE: findings` (exit 1) | `fail`; exact output line: `MADO_TRIPWIRE: clean` (exit 0) |

The import/classify fixture deliberately asserts a returned classification: because `classify_argv` is imported from an external module and its body is absent, the assertion proves only that literal argv was passed to an opaque callee, not that the command ran. The reset case defines `run_record` in JSONL line 1, then sets `reset: true` on the eval call in line 2; the prior helper body is no longer in scope at that call.

### Scan evidence

Historical tool bytes were copied from the requested revisions with:

```text
git -C /home/vgpnk/Projects/shokunin/mado-shokunin show 1f7f995:tools/mado-tripwire.py > /tmp/MadoR20.CaseLeadsInvisible-3/tool-1f7f995.py
git -C /home/vgpnk/Projects/shokunin/mado-shokunin show 9c54c56:tools/mado-tripwire.py > /tmp/MadoR20.CaseLeadsInvisible-3/tool-9c54c56.py
```

Each fixture was scanned, not executed, with `python3 -I /tmp/MadoR20.CaseLeadsInvisible-3/tool-<REV>.py --scan /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-20/w1/cases/CaseLeadsInvisible/<fixture>.jsonl`. Observed scan lines for every case are listed in the table. `sha256sum` observed these tool digests:

- `1f7f995` tool: `367be94773d8fec5e6df91f80ac777070c407c1128f7c75b3dcaa26cc83fdb4d`.
- `9c54c56` tool: `c1ae45a7573e536bdb8ad410f36782aaad9832ecae6a95b2f5c7f823d13c70cd`.

Fixture SHA-256 values, matching the scan verdict's `files[].sha256`:

- `run-record.jsonl`: `9bba75c7de435e99377fca27ef17ae49e3fc4f7ace96beb5377e80152ceb630e`
- `import-run-cmd.jsonl`: `385801d46d771829ca1fd32a0702f6c7716b1c7900655c46c5a182da0e1c1181`
- `import-classify-argv.jsonl`: `efb0f2af54e2fcc1d7a78e74f82beee427916eabde3f762cefd908270a5000e8`
- `opaque-runner.jsonl`: `85f55b108069e443dcb7f36bf1562f86fb60df7923dc74eb0efe18f5c97be690`
- `reset-cleared-helper.jsonl`: `917ee5120a2aa450457ec7bb23c5f0b6c4c7e341b6018f42d6f7add696b81947`
- `import-alias.jsonl`: `9877f9244fc627fa5ba7fc0e4fd42c5d6283b738196b472faa01f248f31dc1f6`

## Limits

Only the mandated historical `--scan` comparisons were performed. Fixture code was never executed. The integrated round-20 tool and suite were not checked; the parent owns post-integration verification.

## Installs

none.
