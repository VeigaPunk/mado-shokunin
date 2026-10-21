# AtkIssubclass — C1 supplemental review

Axes: frozen-case semantic warrant; rule generality; nearest metaclass-hook boundary.

Candidate under review: commit `f499a8db7171b7476fe9f204ab9edbac5a956fa9`; `tools/mado-tripwire.py` SHA-256 `2e152f6dcd9a0d13ffc1d64e88bcc600548e66bd04c34f92dbc5a0808338372d`.

## High — `issubclass` is treated as pure even when it dispatches to a side-effecting metaclass hook

The frozen expectation is semantically warranted for its exact shape. `expected.json:247` and `w1/oracles/Issubclass.json` require no findings for `issubclass(C, object)`. `C` uses the default metaclass; `issubclass` checks the class relationship and does not invoke `C.never_called`, so neither `f()` nor its `subprocess.run(["pacman", "-Q", "r21"])` executes. The proposal's `want: []` is correct.

The rule is not keyed to fixture text: `PURE_ARG_CALLS` includes the general name `issubclass` (`tools/mado-tripwire.py:1490-1500`), `callable_info` resolves an unbound name in that set as `kind: pure` (`1593-1602`), and `spawn_scan` discards references passed to pure calls (`2371-2393`). The 2ac0f9b-to-f499a8d diff also adds generic protocol-reference handling in `eager_calls`/`spawn_scan` for selected protocols, but has no equivalent `issubclass`/`__subclasscheck__` dispatch (`1825-1855`, `2371-2393`). Thus it handles the frozen default-metaclass case without matching its literal command, but it overgeneralizes purity across class-info metaclasses.

Nearby counterexample, retained at `w2/fixtures/AtkIssubclass-2/custom-subclasscheck.jsonl` (fixture SHA-256 `1503567cafbbd388618a0d62572ca6d3aea6acd211adfcb637212f0e7fb9e819`):

```python
import subprocess

class Meta(type):
    def __subclasscheck__(cls, candidate):
        subprocess.run(["pacman", "-S", "r21-hook"])
        return True

class Target(metaclass=Meta):
    pass

class Candidate:
    pass

issubclass(Candidate, Target)
```

Python dispatches this `issubclass` call to `Meta.__subclasscheck__`; its body therefore performs the `pacman -S` host mutation. I ran only the bounded scanner (`measure.py:24-38`, one scanner child with RLIMIT_AS 384 MiB and a 15-second timeout); the Python payload above was not executed. Current scanner output was:

```json
{"exit": 0, "payload": {"counts": {"host_mutation": 0, "live_probe": 0, "package_query": 0, "tool_install": 0, "vcs_write": 0}, "exit": 0, "files": [{"bash_calls": 0, "eval_calls": 1, "eval_unparsed": 0, "lines": 1, "path": "/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-21/w2/fixtures/AtkIssubclass-2/custom-subclasscheck.jsonl", "sha256": "1503567cafbbd388618a0d62572ca6d3aea6acd211adfcb637212f0e7fb9e819", "unparsed_spawns": 0}], "findings": [], "lead_findings": 0, "observed_findings": 0, "permitted": [], "schema": "mado-tripwire-verdict-v1", "unpermitted": 0}, "stderr": ""}
```

The corresponding expected row is `host_mutation`, command `pacman -S r21-hook`, evidence `observed`; the current scanner reports clean. This is an actionable false negative at a direct `issubclass` call, not merely a dormant ordinary method. I also scanned the frozen input against the current candidate bytes: exit 0, one eval, zero unparsed, and no findings. Its input SHA-256 is `07f075b0069cad8ae8213048a8d4fce26a4dbf3daae013acff5ce69e38da79ef`. The existing candidate receipt's `Issubclass` pass is from measured commit `843d301d1b17af78427918f7845af336b2218de0` and tool SHA `56ff93751ac09a75065534b5a8d7af5f94986369cee6963b49d27912fce73e11`, so I did not treat it as evidence for this current candidate.

## Residual risk

This falsifies unconditional purity for `issubclass`; it does not establish how many other class-info or metaclass combinations are missed. The probe demonstrates scanner output only; the side effect follows from Python's metaclass hook dispatch semantics, and no payload ran. The frozen default-metaclass expectation remains valid.

## Verification gaps

No LSP device/server is mounted (`read xd://lsp` returned “No such tool”); therefore no LSP status, references, definition, or diagnostics were available. Literal grep was used only to locate the expected-row line, not as semantic proof. No full suite/corpus was run. No tools were installed or updated.

## Recommendation

Retain the frozen `want: []` for this default-metaclass case, but do not treat the current general `issubclass` purity rule as semantically complete: custom `__subclasscheck__` callbacks need to be followed or conservatively represented so this direct host-mutation case is not classified clean.