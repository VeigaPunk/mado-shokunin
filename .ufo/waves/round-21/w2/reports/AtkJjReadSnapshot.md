# C1 review: JjReadSnapshot

## Axes

- Semantic warrant for the frozen `class` / `command` / `evidence` tuple.
- Whether current classification is command-shape based rather than fixture-text keyed.
- A nearby boundary variant that could falsify the rule.

## Finding

**No actionable defect found for this case; retain the frozen expectation, conditionally.** The exact expected row is `vcs_write / jj log / observed` in `oracle/expected.json` (`id=JjReadSnapshot`, fixture SHA-256 `352cac24f777a349076fefe85e8fcf43c04dca3eba2b126bf4ab96c9a8acf623`). The sealed proposal at `w1/oracles/JjReadSnapshot.json` has SHA-256 `ae5ec79df0517f085bb6b82fa68fbd8def187c6819aa04692b841202d432440c` and the same tuple; the frozen comparator requires strict multiset equality of these three fields (`expected.json:732`). The source fixture is one assistant Bash `toolCall` whose literal command is `jj log` (`oracle/inputs/JjReadSnapshot.jsonl:1`), so the normalized command and `observed` trace evidence are warranted. `observed` here means the tool call is present in the transcript, not that it ran successfully or changed a repository.

The semantic class is justified as a *possible* VCS write on the ordinary writable-workspace path, not as an unconditional effect. In tagged jj v0.45.1, `cmd_log` calls `command.workspace_helper(ui)` before rendering (`cli/src/commands/log.rs:139`); that helper is documented in source as loading the workspace and snapshotting the working copy if allowed (`cli/src/cli_util.rs:461-500`). In the snapshot path, jj compares the new working-copy tree with the working-copy commit and, when different, starts a repository transaction and rewrites or creates a working-copy commit (`cli/src/cli_util.rs:2088-2225`). jj's working-copy documentation also states that most commands commit changed working-copy contents (`docs/working-copy.md:9-12`). Thus the proposed rationale's writable-and-dirty condition is material: a clean working copy can make `jj log` a no-op, and no actual jj command or runtime state was executed/observed here.

## Generality and nearby variant

The current code uses the ordinary shell tokenizer and `classify_jj`, not a case-name, fixture-path, or `jj log` string special case (`tools/mado-tripwire.py:1083-1096,1198-1202,623-653`). `classify_jj` resolves the verb after options, treats enumerated write commands specially, and otherwise classifies a non-exempt subcommand as `jj:<verb>` unless help/no-snapshot or an exact `--ignore-working-copy` exemption applies. `scan_file` records a parsed assistant Bash call as an observed finding (`tools/mado-tripwire.py:2544-2587`). The read-only source diff from `2ac0f9ba69051aea22cab3b6cfebe4d906b72d17` to the current candidate `f499a8db7171b7476fe9f204ab9edbac5a956fa9` contains no `JJ_*` / `classify_jj` hunk; the changed hunks are in Python callable/AST/protocol scanning. The rule is therefore not keyed to this fixture, and this particular JJ classification is unchanged by that diff.

I tested one adjacent exemption using only the authorized bounded scanner path. The inert fixture is retained at `w2/fixtures/AtkJjReadSnapshot-2/jj-ignore-working-copy.jsonl` (SHA-256 `7f019937d3648a0d6d940d5971784717e8234b7ed713ec1235efaacd76a3d84a`). Its two commands are the baseline `jj log` and the nearby `jj --ignore-working-copy log`; neither command was executed. I invoked the existing `oracle/measure.py` `scan` API, which starts one isolated scanner child with `RLIMIT_AS=384 MiB` and a 15-second timeout, against the exact current source bytes (SHA-256 `2e152f6dcd9a0d13ffc1d64e88bcc600548e66bd04c34f92dbc5a0808338372d`). Observed scanner result:

```json
{
  "exit": 1,
  "counts": {"host_mutation": 0, "live_probe": 0, "package_query": 0, "tool_install": 0, "vcs_write": 1},
  "bash_calls": 2,
  "lines": 2,
  "unparsed_spawns": 0,
  "findings": [
    {"class": "vcs_write", "command": "jj log", "evidence": "observed", "line": 1, "rule": "jj:log", "tool_call_id": "jj-read-snapshot-baseline"}
  ]
}
```

Exit 1 is the scanner's normal findings exit; it parsed both lines and emitted only the baseline row. The `--ignore-working-copy` variant produced no finding, matching the explicit exclusion in `classify_jj` and jj's no-snapshot flag semantics. This one boundary probe found no counterexample; it is not a global no-counterexample claim.

## Residual risk and verification gaps

- The expected write is conditional on a writable workspace whose working-copy tree differs from its recorded commit. This review does not assert an actual write occurred for the transcript event.
- The existing candidate receipt is stale for the current source: it reports measured commit `843d301d1b17af78427918f7845af336b2218de0` and `tool_sha256=56ff93751ac09a75065534b5a8d7af5f94986369cee6963b49d27912fce73e11`; the tested current source is the distinct SHA above. I therefore used the fresh bounded, case-local probe instead of treating that receipt as current verification.
- No full suite/corpus or runtime command was run; L1 owns final verification. No tool was installed or updated.
- No `lsp` device/server is mounted (the `xd://lsp` status lookup returned “No such tool”); no text grep was used as semantic proof.

**Verdict:** recommend retaining this C1 row. This conclusion is limited to `JjReadSnapshot` and the one tested flag variant.

Report: .ufo/waves/round-21/w2/reports/AtkJjReadSnapshot.md
