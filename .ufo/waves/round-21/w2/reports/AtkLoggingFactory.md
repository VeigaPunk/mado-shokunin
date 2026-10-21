# LoggingFactory (supplemental C1) — scoped review

## Verdict

**Frozen expectation is semantically warranted; positional repair is shape-general, not fixture-text keyed. One medium-severity nearby false negative remains:** a valid keyword-only `logging.config.dictConfig(config=...)` call bypasses the repair and its factory command is omitted.

## Identity and frozen row

L1 reported the current committed candidate as `f499a8db7171b7476fe9f204ab9edbac5a956fa9`; the reviewed `tools/mado-tripwire.py` bytes have SHA-256 `2e152f6dcd9a0d13ffc1d64e88bcc600548e66bd04c34f92dbc5a0808338372d`. The frozen `expected.json` SHA-256 is `fd2bfbc86897e1ee7a79302f6ccf6c3403709b132180864a0674f8212925576f` (matches `expected.sha256`). Its `LoggingFactory` row pins fixture SHA `b651f2eab377b9cb211e1c812fd744751a1788a2864bcf6dc82254dac508adb8` and proposal SHA `b7602fb961d23cbf83876617baaa177c746751185cea11891640ffd70187aff7`; both match the inspected files. The frozen wanted tuple is exactly `package_query / pacman -Q r21 / observed`, under strict multiset comparison of class, command, and evidence.

The supplemental JSONL contains a Python `logging.config.dictConfig` call with a literal handler mapping whose `"()"` factory is `subprocess.run` and whose `args` value is `['pacman', '-Q', 'r21']`. In the inspected Python 3.14 stdlib, `BaseConfigurator.configure_custom` takes `config.pop('()')`, includes valid config identifiers as kwargs, and synchronously calls `c(**kwargs)` (`/usr/lib/python3.14/logging/config.py:481-493`; handler configuration calls it at lines 694 and 736). The public `dictConfig(config)` entry point is at lines 945-947. Thus the `args` key is passed as `subprocess.run(args=...)`; this is a real synchronous process call, not merely a later logging validation error or a lead. The scanner's pacman mapping classifies `-Q` as `package_query` (`tools/mado-tripwire.py:737-780`). `observed` is therefore the warranted evidence label.

The existing candidate receipt's row passes with that exact tuple, but it is not a current-source receipt: it says `measured_commit=843d301d1b17af78427918f7845af336b2218de0` and its embedded `tool_sha256=56ff93751ac09a75065534b5a8d7af5f94986369cee6963b49d27912fce73e11`, unlike the reviewed source hash above. I treat it as historical corroboration only, not as a run of the current candidate.

## Generality of the repair

At `tools/mado-tripwire.py:2236-2247`, the scanner resolves the callable name `logging.config.dictConfig`, walks its config AST for dictionary entries with the API key `"()"`, and synthesizes a factory call from the remaining values as keyword arguments. That is structural handling of the stdlib API: it does not test the case ID, tool-call ID, command text, package name, or `r21` literal. For this positional literal-config shape, it generalizes beyond this fixture. Its boundary is narrower than all valid `dictConfig` calls, as the counterexample below shows.

## Nearby counterexample (one bounded scanner-only probe)

Variant input code (valid keyword invocation of the same API and identical factory/config):

```python
import logging.config, subprocess
logging.config.dictConfig(config={"version": 1, "handlers": {"probe": {"()": subprocess.run, "args": ["pacman", "-Q", "r21"]}}})
```

I wrapped that inert JSONL tool-call record with the existing `oracle/measure.py` `scan` API. It launched one capped scanner child (384 MiB address-space limit, 15-second timeout); the transcript code was never executed. Actual output:

```json
{"input_code":"import logging.config, subprocess\nlogging.config.dictConfig(config={\"version\": 1, \"handlers\": {\"probe\": {\"()\": subprocess.run, \"args\": [\"pacman\", \"-Q\", \"r21\"]}}})\n","scanner_result":{"exit":0,"payload":{"counts":{"host_mutation":0,"live_probe":0,"package_query":0,"tool_install":0,"vcs_write":0},"exit":0,"files":[{"bash_calls":0,"eval_calls":1,"eval_unparsed":0,"lines":1,"path":"/tmp/mado-r21-loggingfactory-__ylxfe1/LoggingFactory-keyword.jsonl","sha256":"40747dfa44bf38a3d292191277fb9c36666b7a011007ed890930ed982f26125d","unparsed_spawns":0}],"findings":[],"lead_findings":0,"observed_findings":0,"permitted":[],"schema":"mado-tripwire-verdict-v1","unpermitted":0},"stderr":""}}
```

This is a concrete scanner false negative: the stdlib signature `dictConfig(config)` accepts the keyword form, and its implementation still configures the mapping (source lines 945-947); the nested handler still invokes the same factory. The current special case requires `node.args` (`mado-tripwire.py:2236`), so keyword-only `config=` never reaches the factory synthesis at lines 2237-2246. This finding is specifically about the LoggingFactory/dictConfig shape, not a whole-tool assessment.

## Verification limits

- No LSP device/server is mounted: the initial lookup `read xd://lsp` returned “No such tool: xd://lsp” and enumerated mounted devices without LSP; no status, references, definition, or diagnostics route was available. Source inspection was used, and the literal `grep` fallback was limited to locating the stdlib `dictConfig` definition/call site.
- One current-source scanner-only keyword variant was run; the original candidate receipt is source-hash-stale as stated above. No full corpus/suite was run, and no command from either transcript was executed.
- Tools installed or updated: none.
