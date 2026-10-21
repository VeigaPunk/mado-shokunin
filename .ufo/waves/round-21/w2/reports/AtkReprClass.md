# ReprClass — scoped review

## Axes
- Frozen oracle truth for class, command, and evidence.
- Generality of the repair for this dispatch shape.
- Nearby class/instance representation boundary.

## Verdict
No actionable finding for the frozen `ReprClass` case. The frozen empty expectation is semantically warranted for the exact fixture. Advisory recommendation: retain `want: []` for this case.

## Evidence
- Current candidate: commit `f499a8db7171b7476fe9f204ab9edbac5a956fa9`.
- Tested scanner bytes: SHA-256 `2e152f6dcd9a0d13ffc1d64e88bcc600548e66bd04c34f92dbc5a0808338372d`.
- Frozen `expected.json`: SHA-256 `fd2bfbc868e1e1ee7a79302f6ccf6c3403709b132180864a0674f8212925576f`.
- Frozen fixture `inputs/ReprClass.jsonl`: SHA-256 `887639b0916be59a6d0853ac9de634c147e887190e0277541be38b672f739011`.
- The expected row at `oracle/expected.json:560-570` pins this case to `want: []`; its proposal hash is `41059c7ce4091475b65624b1c6febc1fc5bcb87a75a79a2e91b65dc621989656`.
- The existing `evidence/oracle-candidate.json` receipt is for measured commit `843d301d1b17af78427918f7845af336b2218de0` and tool SHA-256 `56ff93751ac09a75065534b5a8d7af5f94986369cee6963b49d27912fce73e11`, not this candidate. Its ReprClass row is therefore historical; the bounded probe below used the current scanner hash above.

The fixture defines `f()` with `subprocess.run(["pacman", "-Q", "r21-reprclass"])`, puts `f()` inside `C.__repr__`, and ends with `repr(C)`. `C` has the default metaclass and is not instantiated. Python invokes special methods through the represented object's type: the object passed to `repr` is the class object `C`, whose type is `type`, not an instance of `C`. Thus `C.__repr__` is not invoked, `f()` is unreachable, and there is no `package_query` command or evidence row. The frozen class/command/evidence expectation is correct.

The current code handles the form generically rather than matching fixture text. `eager_calls` records builtin `repr` arguments as `__repr__` protocol references (`tools/mado-tripwire.py:1845-1849`). `spawn_scan` follows that protocol only when the receiver is an instance or a call constructing the class (`:2371-2385`); the frozen argument is the class-name `Name` `C`, so it is not treated as an instance or constructor. For the nearby constructed-instance form, `callable_info` resolves the class method (`:1623-1637`) and the referenced body is swept (`:2136-2152`), which the scanner reports as `lead` (`:2129-2133`). No fixture ID, filename, or `r21-reprclass` string is used by this dispatch logic.

## One nearby variant probed
I changed only the final expression from `repr(C)` to `repr(C())`, preserving the helper and its `__repr__`. This is the boundary named in the proposal rationale (`w1/oracles/ReprClass.json:6`). It should reach the instance method. The inert JSONL was submitted through `measure.py`'s `scan` API (`oracle/measure.py:24-38`), which starts the scanner child with a 384 MiB address-space limit and 15-second timeout. The code string was parsed by the scanner; it was never executed. The JSONL held the frozen source as probe call 0 and this variant as call 1, each with `reset: true`.

Variant code:

```python
import subprocess

def f():
    subprocess.run(["pacman", "-Q", "r21-reprclass"])

class C:
    def __repr__(self):
        f()
        return "C()"

repr(C())
```

Observed scanner output (temporary JSONL path was deleted after the probe):

```json
{"exit":1,"payload":{"counts":{"host_mutation":0,"live_probe":0,"package_query":1,"tool_install":0,"vcs_write":0},"exit":1,"files":[{"bash_calls":0,"eval_calls":2,"eval_unparsed":0,"lines":2,"path":"/tmp/mado-reprclass-ndwsir4b.jsonl","sha256":"44b1b0f453285f6d37c616ac7bf54dad3681d6715b0e2d76746bc99fa7457374","unparsed_spawns":0}],"findings":[{"argv0":"pacman","class":"package_query","command":"pacman -Q r21-reprclass","evidence":"lead","file":"/tmp/mado-reprclass-ndwsir4b.jsonl","line":2,"rule":"pacman:-Q","timestamp":"None","tool":"eval","tool_call_id":"ReprClassProbe-1"}],"lead_findings":1,"observed_findings":0,"permitted":[],"schema":"mado-tripwire-verdict-v1","unpermitted":1},"stderr":""}
```

The exact frozen form in the same probe produced no finding; the variant produced the expected `package_query` lead and no parse/unparsed-spawn errors. The nonzero scanner exit is due to the one intentionally unpermitted finding in the variant, not a scan error. No counterexample was found in this one nearby variant; this is not a global claim.

## Residual risk and verification gaps
- The module-level limits at `tools/mado-tripwire.py:72-74` explicitly say metaclass/descriptor behavior is not resolved. This result establishes the frozen default-metaclass case and the constructed-instance boundary only; it does not establish handling for custom metaclasses.
- No `lsp` device is mounted: requesting `xd://lsp` returned `No such tool` and listed the mounted devices. Therefore no LSP status, references, definition, or diagnostics were available. Literal grep was used only to locate source call sites; semantic conclusions above come from source inspection, Python special-method semantics, and the bounded scanner-only probe, not grep.
- No full suite/corpus run was performed. No tools were installed or updated.
