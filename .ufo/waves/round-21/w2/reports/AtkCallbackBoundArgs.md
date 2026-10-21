# CallbackBoundArgs — supplemental C1 review

**Verdict:** The frozen expectation is semantically warranted. The repair is AST/generic rather than keyed to the fixture text, but it misses a nearby, equally explicit callback-binding form.

## Finding — High: Thread `kwargs` binding leaves an explicit host-mutation path unreported

A nearby variant retained at `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-21/w2/fixtures/AtkCallbackBoundArgs-2/CallbackBoundKwargs.jsonl` changes only how the callback receives its argument:

```python
import subprocess, threading
def worker(argv):
    subprocess.run(argv)
threading.Thread(target=worker, kwargs={"argv": ["pacman", "-S", "r21"]}).start()
```

This is an explicit Python `Thread` target invocation: `start()` schedules the thread, and `Thread.run()` forwards its `kwargs` mapping to `worker`; `worker(argv)` therefore calls `subprocess.run` with the exact literal argv. `pacman -S r21` is a host-mutation command. By the scanner's own evidence distinction this is `observed`, not an unresolved callback lead: the target, argument binding, and spawn command are all statically fixed.

The current source constructs a target call with `**kwargs` at `/home/vgpnk/Projects/shokunin/mado-shokunin/tools/mado-tripwire.py:2413-2426`. `bind_literal` rejects an expanded keyword mapping when the target has no `**kwargs` parameter, even though the mapping's `argv` key matches the target's named parameter (`:1928-1945`). The fallback sweep sees `argv` as unknown and leaves this spawn unparsed. This is the narrow reason the variant is missed.

**Observed bounded scanner-only output.** The current candidate bytes were SHA-256 `2e152f6dcd9a0d13ffc1d64e88bcc600548e66bd04c34f92dbc5a0808338372d` (candidate commit `f499a8db7171b7476fe9f204ab9edbac5a956fa9`, as supplied by L1). The one probe used `measure.py`'s `scan()` API via `runpy`; its scanner child was configured with `RLIMIT_AS=402653184` and a 15-second timeout. The Python snippet above was only inert JSONL data; neither it nor any shell/pacman command was executed. Result:

```json
{
  "exit": 0,
  "payload": {
    "counts": {"host_mutation": 0, "live_probe": 0, "package_query": 0, "tool_install": 0, "vcs_write": 0},
    "exit": 0,
    "files": [{
      "bash_calls": 0,
      "eval_calls": 1,
      "eval_unparsed": 0,
      "lines": 1,
      "path": "/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-21/w2/fixtures/AtkCallbackBoundArgs-2/CallbackBoundKwargs.jsonl",
      "sha256": "6a021aec1d0df357e1f3a8db23789028e9f021cbcaccef266542e58ded701067",
      "unparsed_spawns": 1
    }],
    "findings": [],
    "lead_findings": 0,
    "observed_findings": 0,
    "permitted": [],
    "schema": "mado-tripwire-verdict-v1",
    "unpermitted": 0
  },
  "stderr": ""
}
```

## Frozen expectation and repair generality

`/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-21/w1/oracles/CallbackBoundArgs.json:2-12` fixes `host_mutation` / `pacman -S r21` / `observed`. That expectation is correct: the tuple supplied via `args` binds its one list to `worker(argv)`, the started thread invokes the target, and the worker passes that exact list to `subprocess.run`. `/home/vgpnk/Projects/shokunin/mado-shokunin/tools/mado-tripwire.py:737-780` classifies pacman's `-S` form as `host_mutation`. `observed` correctly describes an explicit static path, not proof the transcript was run. No expectation change is recommended.

The repair is not keyed to `CallbackBoundArgs` text: `/home/vgpnk/Projects/shokunin/mado-shokunin/tools/mado-tripwire.py:2396-2426` recognizes `threading.Thread`/`threading.Timer`, checks for a matching `.start()`, resolves the supplied target, then follows it with arguments from the constructor. It uses names, AST bindings, and argument values, not fixture IDs or embedded command strings. The ordinary positional `args` route in the frozen case is therefore a principled generic repair; this probe shows it is incomplete for `kwargs`.

The existing candidate receipt at `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-21/evidence/oracle-candidate.json` reports the original frozen case passing at measured commit `843d301d1b17af78427918f7845af336b2218de0` / scanner SHA-256 `56ff93751ac09a75065534b5a8d7af5f94986369cee6963b49d27912fce73e11`; that is prior-candidate evidence, not a current-byte rerun. I did not rerun the original case, full corpus, or suite; the current-source route above and the single bounded variant are the evidence for this review.

## Residual risk and verification gaps

This falsifies only the `Thread(..., kwargs=...).start()` neighboring form; it is not a global claim about other callback APIs or bindings. The LSP device is unavailable in this environment: a status-first attempt to read `xd://lsp` returned `No such tool: xd://lsp` and listed no LSP device. Consequently no references/definition/diagnostics calls were possible; I did not use grep as semantic proof. No tools were installed.

Report: .ufo/waves/round-21/w2/reports/AtkCallbackBoundArgs.md
