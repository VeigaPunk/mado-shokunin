# LoggingData supplemental C1 falsification

## Findings, by severity

### Medium — an unused data dictionary containing `()` becomes a false **observed** process finding

**Location:** `/home/vgpnk/Projects/shokunin/mado-shokunin/tools/mado-tripwire.py:2236-2247`.

The new `logging.config.dictConfig` branch walks **every** dictionary below the first argument, finds a literal `()` key, synthesizes a call to its value, and recursively scans that call. It does not establish that the dictionary occupies a configuration position where `DictConfigurator` invokes a factory. An ignored top-level data field therefore becomes executable to the scanner merely by containing the factory-shaped dictionary below.

One nearby variant was constructed and scanned; its Python payload was **not executed**:

```text
import logging.config, subprocess
logging.config.dictConfig({"version": 1, "handlers": {}, "example": {"()": subprocess.run, "args": ["pacman", "-Q", "r21"]}})
```

Semantic expectation for this variant is `[]`, just as for LoggingData. The only change in the logging configuration is replacing the unused `example` list with an unused factory-shaped dictionary; importing and referencing `subprocess.run` does not call it. CPython's `BaseConfigurator.__init__` stores a `ConvertingDict`, whose conversion is access-driven. `DictConfigurator.configure` processes the recognized configuration sections and never accesses the arbitrary top-level `example` field. `configure_custom` calls `c(**kwargs)` only when a configured object reaches it; a `()` key anywhere in arbitrary data is not sufficient. Sources inspected independently: [CPython 3.14 configuration traversal, lines 535–690](https://github.com/python/cpython/blob/3.14/Lib/logging/config.py#L535-L690), [lazy converting containers, lines 320–353](https://github.com/python/cpython/blob/3.14/Lib/logging/config.py#L320-L353), [configurator initialization, lines 385–411](https://github.com/python/cpython/blob/3.14/Lib/logging/config.py#L385-L411), and [conversion/custom factory implementation, lines 458–493](https://github.com/python/cpython/blob/3.14/Lib/logging/config.py#L458-L493).

**Observed contradiction:** scanner exit `1`, one `package_query` finding for `pacman -Q r21`, rule `pacman:-Q`, evidence `observed`; no parse/unknown-spawn counters and no stderr. The synthetic invocation supplies `args` as a keyword, which the process scanner accepts at `/home/vgpnk/Projects/shokunin/mado-shokunin/tools/mado-tripwire.py:2332-2338,2362-2365`. The ordinary finding path assigns `observed` when a hit has no explicit evidence marker at `/home/vgpnk/Projects/shokunin/mado-shokunin/tools/mado-tripwire.py:2571-2588`. This is an assertion of execution from data, not merely a conservative unresolved lead.

**Impact and recommendation:** the repair passes the list-shaped control but retains a nearby false positive at the exact data-versus-factory boundary. Restrict factory following to configuration positions and modes that actually dispatch factories, rather than indiscriminately walking nested dictionaries. This is advisory; production and frozen expectations were not edited.

## Scope, axes, and tested identity

- Scope is only supplemental C1 **LoggingData**, its proposed empty class/command/evidence multiset, the corresponding repair, and the one variant above. No C2 assessment or round/promotion admission is supplied.
- Review axes: **operability** (the C1 claim axis: bounded scanner completion and usable results), **semantic calibration/precision** (data must not acquire observed command evidence), and **shape generality** (the rule must not depend on fixture names or command text). These are review dimensions, not additional round claims.
- Parent's advanced production revision: `f499a8db7171b7476fe9f204ab9edbac5a956fa9`.
- Observed checkout HEAD at inspection: `a8da015624c92f4cb4a7de92adbf6643a3f8b38a`.
- Exact source SHA-256 **tested**: `2e152f6dcd9a0d13ffc1d64e88bcc600548e66bd04c34f92dbc5a0808338372d` for `/home/vgpnk/Projects/shokunin/mado-shokunin/tools/mado-tripwire.py`. The committed file at `f499a8db7171b7476fe9f204ab9edbac5a956fa9` had that same SHA-256; the probe also recorded that hash immediately before its scan. Thus the different checkout HEAD is not treated as different scanner bytes.
- Actual diffs reviewed: the initial repair from `a8960de655e6ea8c0a3bf74f5542041d9fe25b39` to `843d301d1b17af78427918f7845af336b2218de0`, and subsequent source changes through `f499a8db7171b7476fe9f204ab9edbac5a956fa9`. The logging traversal was added by the initial repair and remains in the tested source.

## Frozen expectation and generality assessment

The sealed row at `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-21/oracle/expected.json:326-335` specifies `want: []`, no normalizations, input SHA-256 `c332e9d1ce29ce4b73802321453f22bdc2a49c05c3a08cd9f2914c0297b05e94`, and proposal SHA-256 `d1a32bf2b2e8d66d3dd57c83d4374a999e683dffdbea74c91ea68d611746440f`. The proposal at `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-21/w1/oracles/LoggingData.json:1-9` contains:

```text
import logging.config
logging.config.dictConfig({"version": 1, "handlers": {}, "example": ["pacman", "-Q", "r21"]})
```

The empty expected multiset is **semantically warranted**: no process callable is evaluated, there are no configured handlers or factories, and the command-shaped list is in an ignored top-level field. There should be neither a `package_query` class/command row nor `observed`/`lead` process evidence. `dictConfig` does affect in-process logging configuration; this is not a claim that it has no Python side effects.

The supplied receipt at `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-21/evidence/oracle-candidate.json`, decoded from its `stdout`, records LoggingData passing with `findings: []`, exit `0`, `eval_unparsed: 0`, and `unparsed_spawns: 0`. **That receipt names source SHA-256 `56ff93751ac09a75065534b5a8d7af5f94986369cee6963b49d27912fce73e11`, not the tested current source hash.** It is historical evidence for this case, not a fresh execution receipt for `f499a8db7171b7476fe9f204ab9edbac5a956fa9`. Current-source reasoning supports the original empty result: neither its outer dictionary nor any nested dictionary contains `()`, so this branch synthesizes no invocation. The original case was not rerun by this seat.

The implementation is **not keyed to LoggingData, `r21`, or the `example` field**. The source branch discriminates on the resolved canonical callable name `logging.config.dictConfig`, AST dictionary nodes, and `()`; it has no special exemption for this fixture or its command. Callable resolution at `/home/vgpnk/Projects/shokunin/mado-shokunin/tools/mado-tripwire.py:1638-1658` uses the active module binding. A literal fallback search found no `LoggingData`, `r21`, or `ignored-factory` literals in the scanner. The original list-data behavior therefore generalizes beyond the exact fixture text, but the observed variant demonstrates that the generalization is semantically too broad for nested factory-shaped data.

## Retained counterexample and complete observed output

Inert fixture: `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-21/w2/fixtures/AtkLoggingData/ignored-factory.jsonl`.

Fixture SHA-256: `842a8d367ca07d3167a9725fb427fd84e4da3cf643b3075ca7105833e772a5db`.

The fixture is one assistant `eval` transcript record containing the text shown above. It was treated only as scanner input. The new probe used `runpy.run_path` to obtain the existing `scan` API from `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-21/oracle/measure.py:12-38`. Only the in-memory scanner wrapper was prefixed with `sys.dont_write_bytecode=True`, to avoid scanner-import cache writes; no runner file was modified. The API retained its isolated scanner child, `RLIMIT_AS = 402653184` bytes, subprocess timeout `15` seconds, and concurrency `1`. No transcript Python or shell payload was executed.

```json
{
  "fixture_sha256": "842a8d367ca07d3167a9725fb427fd84e4da3cf643b3075ca7105833e772a5db",
  "scan": {
    "exit": 1,
    "payload": {
      "counts": {
        "host_mutation": 0,
        "live_probe": 0,
        "package_query": 1,
        "tool_install": 0,
        "vcs_write": 0
      },
      "exit": 1,
      "files": [
        {
          "bash_calls": 0,
          "eval_calls": 1,
          "eval_unparsed": 0,
          "lines": 1,
          "path": "/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-21/w2/fixtures/AtkLoggingData/ignored-factory.jsonl",
          "sha256": "842a8d367ca07d3167a9725fb427fd84e4da3cf643b3075ca7105833e772a5db",
          "unparsed_spawns": 0
        }
      ],
      "findings": [
        {
          "argv0": "pacman",
          "class": "package_query",
          "command": "pacman -Q r21",
          "evidence": "observed",
          "file": "/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-21/w2/fixtures/AtkLoggingData/ignored-factory.jsonl",
          "line": 1,
          "rule": "pacman:-Q",
          "timestamp": "None",
          "tool": "eval",
          "tool_call_id": "AtkLoggingData-ignored-factory-0"
        }
      ],
      "lead_findings": 0,
      "observed_findings": 1,
      "permitted": [],
      "schema": "mado-tripwire-verdict-v1",
      "unpermitted": 1
    },
    "stderr": ""
  },
  "tool_sha256": "2e152f6dcd9a0d13ffc1d64e88bcc600548e66bd04c34f92dbc5a0808338372d"
}
```

## Residual risk, verification gaps, and verdict

- LSP was unavailable: requesting `xd://lsp` returned `No such tool`, with no LSP device among mounted tools. Server status, references, definitions, and diagnostics therefore could not be obtained. Fallback source inspection and literal searches are not presented as semantic reference proof; the bounded scanner receipt is direct behavioral evidence.
- Exactly one new variant scan was exercised. No full suite, corpus run, historical unsafe resource failure, Python logging runtime, live package command, compositor/service operation, or alternate production runtime was invoked. CPython semantics were checked from official source rather than by executing the payload. The fetched `3.14` source is a branch URL, not a content-pinned vendor snapshot.
- No resume, rerouting, or runtime-identity changes occur in the scoped logging branch. No broader continuity or saturation claim is made. Other dictConfig forms and the rest of the scanner were not assessed.
- No tools installed or updated. Only this advisory report and its explicitly inert fixture were created; production, frozen expectations, and VCS state were not edited.

**Advisory verdict:** retain the frozen LoggingData expectation unchanged. The repair is not fixture-text-specific and supports the original list control, but its general data-versus-factory precision claim is **falsified by the retained nearby variant**. The observed false `observed` finding remains actionable; this is not a round-admission or promotion decision.

Report: .ufo/waves/round-21/w2/reports/AtkLoggingData.md
