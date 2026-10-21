# UuidProcess — scoped falsification

Reviewed the current `tools/mado-tripwire.py` bytes (SHA-256 `2e152f6dcd9a0d13ffc1d64e88bcc600548e66bd04c34f92dbc5a0808338372d`). The repository log at inspection showed HEAD `a8da015624c92f4cb4a7de92adbf6643a3f8b38a` after the assigned `f499a8d` candidate change; this is not the earlier `2ac0f9b` source.

## Findings by severity

No actionable finding for the frozen `UuidProcess` case or the one nearby variant tested.

## Frozen expectation

The frozen row in `oracle/expected.json` (`UuidProcess`, input SHA-256 `b1cbf27dcc66ee2e5de5d9bd485fd3e111fdee3e189817b404c29b790095aee4`) expects `package_query`, `pacman -Q r21`, `lead`. That is semantically warranted. The input calls `uuid._get_command_stdout("pacman", "-Q", "r21")`; CPython's `/usr/lib/python3.14/uuid.py:424-452` resolves `pacman` through `shutil.which`, then passes the executable and arguments to `subprocess.Popen` (and returns `None` when resolution or process creation fails). Thus this code can issue the command, but the scanner cannot claim it ran: `lead` is the honest evidence level. Pacman's `-Q` operation is a query; the scanner's `classify_pacman` maps it to `package_query` (`tools/mado-tripwire.py:762-780`). The command string in the expectation preserves the actual argv.

The receipt at `evidence/oracle-candidate.json` contains this expected finding, but it is stale for the reviewed bytes: it records measured commit `843d301d1b17af78427918f7845af336b2218de0` and scanner SHA-256 `56ff93751ac09a75065534b5a8d7af5f94986369cee6963b49d27912fce73e11`. I do not attribute that receipt's run to the current source.

## Nearby variant and observed output

I retained one inert variant at `.ufo/waves/round-21/w2/fixtures/AtkUuidProcess-2/UuidFromImportAlias.jsonl` (SHA-256 `80fd5991836dc5253b9035c941a7bcb3dd8e8464f4b3523a1699a538d0cd8a0c`). Its code is:

```python
from uuid import _get_command_stdout as run_command
run_command("pacman", "-R", "uuid-alias-target")
```

This changes both the import/call spelling and the command operation/operand. The bounded scan of the inert JSONL produced: `host_mutation: 1`, `package_query: 0`, `eval_unparsed: 0`, `unparsed_spawns: 0`; one finding `{class: host_mutation, command: "pacman -R uuid-alias-target", evidence: lead, rule: "pacman:-R", tool_call_id: "UuidProcessAlias-0"}`. Scanner exit was 1 because this lead is unpermitted, not because parsing failed. No Python payload, uuid helper, shell, or pacman command was executed.

This supports generality beyond the frozen text for the tested literal-argument shape. `spawn_path` includes `uuid._get_command_stdout` (`:1540-1546`); `ImportFrom` bindings preserve that canonical name, including aliases (`:1736-1748`); the call branch classifies the actual literal argv through `classify_shell(shlex.join(values))` and labels resulting hits `lead` (`:2304-2310`). The changed operation was consequently classified as a mutation rather than being forced to the frozen query row. No counterexample was found in this single nearby variant; this is not a global no-counterexample claim.

## Residual risk and verification gaps

- The special case only classifies a nonempty vector of literal string arguments. Other arguments increment `unparsed` at `tools/mado-tripwire.py:2305-2310`; the tool's documented limits explicitly say non-literal spawn arguments are counted as `unparsed_spawns` and that a clean result is not proof no host command ran (`:32-37`). I did not test those dynamic forms, so this review makes no claim about their command identity.
- The retained variant was scanned with the existing `oracle/measure.py` `scan` API. That runner sets `RLIMIT_AS` to 384 MiB and a 15-second child timeout (`measure.py:12,24-38`). No full suite or corpus was run, and no actual process-spawning path was invoked.
- No LSP device was mounted: `read xd://lsp` returned “No such tool” and listed the available devices. LSP status/references/definition/diagnostics could not be obtained. Grep was used only to locate source; semantic conclusions above rely on direct source reads and the bounded scanner output.
- No tools were installed.

## Verdict

The frozen expected class, command, and `lead` evidence are correct. The repair is data-driven for the tested UUID helper call shape, including a direct-import alias and a changed Pacman operation. I found no actionable UuidProcess-scoped defect in that case or variant.

Report: .ufo/waves/round-21/w2/reports/AtkUuidProcess.md
