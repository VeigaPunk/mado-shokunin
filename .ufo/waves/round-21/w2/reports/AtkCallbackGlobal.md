# CallbackGlobal C1 review

## Axes and scope

- **Semantic warrant:** whether the frozen class, command, and evidence label follow from the snippet.
- **Repair generality:** whether the current rule handles this callback shape without keying on fixture text.
- **Nearby falsifier:** one minimal callback/start variation.

Reviewed only CallbackGlobal, its frozen oracle row and proposal, and `/home/vgpnk/Projects/shokunin/mado-shokunin/tools/mado-tripwire.py`. No expectation was changed. At inspection, repository HEAD was `a8da015624c92f4cb4a7de92adbf6643a3f8b38a`; the tested `/home/vgpnk/Projects/shokunin/mado-shokunin/tools/mado-tripwire.py` bytes matched HEAD and the reported `f499a8db7171b7476fe9f204ab9edbac5a956fa9` candidate blob, SHA-256 `2e152f6dcd9a0d13ffc1d64e88bcc600548e66bd04c34f92dbc5a0808338372d`.

## Frozen row: semantically warranted

`/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-21/oracle/expected.json:60-74` and `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-21/w1/oracles/CallbackGlobal.json` agree on `host_mutation`, `pacman -S r21`, `observed`; their registered proposal/input digests match the files read (`d7bd98dbe728244bfcb90b40468feccbe16a21cfafca01e84f66ea4baeac4346` and `9a8360283570a78e028d8073200f57be1446e8ca6e5892729216a7b3ba7f9cc8`). The module-level `argv` is the literal vector `['pacman', '-S', 'r21']`; `worker` passes it to `subprocess.run`. Python's `Thread` documentation defines `target` as the callable invoked by `run()`, says `start()` arranges for `run()` to execute on another thread, and says the standard `run()` invokes `target`; `subprocess.run(args)` runs the command described by `args`. The main thread starts a normal non-daemon thread, so this is an explicit reachable path, not merely a dormant callback. The snippet was not executed.

The tripwire maps an unadorned `pacman -S` to `host_mutation` (`/home/vgpnk/Projects/shokunin/mado-shokunin/tools/mado-tripwire.py:737-780`), and the frozen `observed` label is appropriate for a statically followed explicit path. Here, “observed” is the scanner's evidence classification; it is not a claim of runtime execution. Official semantics: [threading.Thread](https://docs.python.org/3.14/library/threading.html#threading.Thread) and [subprocess.run](https://docs.python.org/3.14/library/subprocess.html#subprocess.run).

The primary repair is not fixture-text keyed: the source resolves a `threading.Thread`/`Timer` target and follows it when it finds a corresponding start call (`/home/vgpnk/Projects/shokunin/mado-shokunin/tools/mado-tripwire.py:2396-2429`). A bounded scan of the current bytes also returned the primary record as observed (see the baseline record in the probe below).

## Finding — Medium: aliasing the bound `start` method silently drops a reachable target

The start matcher requires a call whose `func` is an `ast.Attribute` named `start`, then recognizes either the constructor expression or a variable bound to that constructor (`/home/vgpnk/Projects/shokunin/mado-shokunin/tools/mado-tripwire.py:2398-2405`). In the variant below, `start()` is an `ast.Name` call. The matcher therefore leaves `scheduled` false and takes the `continue` at line 2405 while processing the `worker` target reference. No observed **or lead** finding is produced for that callback, although invoking the stored bound method starts the same thread. The evaluator's reference walk is at `/home/vgpnk/Projects/shokunin/mado-shokunin/tools/mado-tripwire.py:1813-1893`.

Retained inert input: `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-21/w2/fixtures/AtkCallbackGlobal-2/callback-global-start-alias.jsonl` (SHA-256 `540dee6e562ca6a7db4f9c7f08f68f6b1733cf77c6db05dc1cb2e8c4a3efcb5e`). It contains the original direct-start baseline and exactly one nearby variant; the variant's eval code is:

```python
import subprocess
import threading

argv = ["pacman", "-S", "r21"]

def worker():
    subprocess.run(argv)

thread = threading.Thread(target=worker)
start = thread.start
start()
```

This was a scanner-only call through the existing `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-21/oracle/measure.py` `scan()` API, with one scanner child capped at 384 MiB address space and 15 seconds. Neither eval payload was executed. Exact scan result:

```json
{"exit":1,"payload":{"counts":{"host_mutation":1,"live_probe":0,"package_query":0,"tool_install":0,"vcs_write":0},"exit":1,"files":[{"bash_calls":0,"eval_calls":2,"eval_unparsed":0,"lines":2,"path":"/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-21/w2/fixtures/AtkCallbackGlobal-2/callback-global-start-alias.jsonl","sha256":"540dee6e562ca6a7db4f9c7f08f68f6b1733cf77c6db05dc1cb2e8c4a3efcb5e","unparsed_spawns":0}],"findings":[{"argv0":"pacman","class":"host_mutation","command":"pacman -S r21","evidence":"observed","file":"/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-21/w2/fixtures/AtkCallbackGlobal-2/callback-global-start-alias.jsonl","line":1,"rule":"pacman:-S","timestamp":"None","tool":"eval","tool_call_id":"CallbackGlobalBaseline-0"}],"lead_findings":0,"observed_findings":1,"permitted":[],"schema":"mado-tripwire-verdict-v1","unpermitted":1},"stderr":""}
```

The sole result is for `CallbackGlobalBaseline-0`; `CallbackGlobalStartAlias-0` has no result, with no unparsed marker. The nonzero scanner exit is expected for the baseline's unpermitted finding, not a scan error. This is a concrete silent false negative for a nearby, directly expressed reachable callback shape. It does not invalidate the frozen primary row, but it shows the repair is not fully general across the callback's equivalent start invocation forms.

## Residual risk and verification gaps

- Only the primary and this one adjacent method-alias variant were scanned; no full suite or corpus was run.
- The existing `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-21/evidence/oracle-candidate.json` receipt is stale for this review: it records `measured_commit` `843d301d1b17af78427918f7845af336b2218de0` and tool SHA `56ff93751ac09a75065534b5a8d7af5f94986369cee6963b49d27912fce73e11`, not the tested tool bytes.
- No LSP device was mounted (`xd://lsp` returned “No such tool”; the mounted-device list omitted it), so references/definition/diagnostics were unavailable. Source reads and the scanner probe are the evidence here; no grep result is treated as semantic proof.
- No runtime execution or tool installation occurred.
