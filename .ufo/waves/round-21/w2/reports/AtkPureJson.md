# AtkPureJson — scoped C1 critique

## Axes

- **Frozen-oracle soundness:** `PureJson`'s `want: []` is semantically warranted for its pinned input.
- **Repair generality:** the exemption is resolved-callable-path-based, not keyed to the fixture text.
- **Callback coverage:** the unqualified `json.dumps` exemption suppresses a real process-query callback in one nearby variant.

## Verdict

**[INFERENCE] Keep the frozen `PureJson` expected result; do not treat every `json.dumps` call as effect-free.** The pinned program only formats a literal list and never invokes its dormant `C.__add__`, so there is no expected finding. The repair is general to calls resolved as `json.dumps` (including imported aliases), but it also hides callable side effects supplied through `default=`. The retained nearby variant is a concrete false negative, not a reason to change the frozen expectation.

## Frozen expected row

[INFERENCE] Its only `f()` call is inside `C.__add__`; the transcript constructs `C` but performs no addition, so the method is not called. The final `json.dumps` receives only a built-in list of strings. The Python JSON API documents `dumps` as serialization to a JSON string; in this call it has no custom encoder or `default` callback and cannot reinterpret the command-looking strings as argv. No process-query class/command/evidence is warranted for this exact fixture.

I freshly scanned that pinned input against the current candidate: exit `0`, `findings: []`, `observed_findings: 0`, `lead_findings: 0`, `eval_unparsed: 0`, `unparsed_spawns: 0`, stderr empty. This is one bounded scan, not a suite/corpus result.

## Generality and source path

The implementation is not matching `PureJson` text. `/home/vgpnk/Projects/shokunin/mado-shokunin/tools/mado-tripwire.py:1506-1537` declares `json.dumps` pure in `PURE_STDLIB_EXACT` and resolves pure stdlib paths. `update_bindings` in `/home/vgpnk/Projects/shokunin/mado-shokunin/tools/mado-tripwire.py:1730-1747` resolves `from json import dumps as encode` to `json.dumps`; `callable_info` in `/home/vgpnk/Projects/shokunin/mado-shokunin/tools/mado-tripwire.py:1641-1651` returns that resolved binding. `spawn_scan` unconditionally skips calls classified `pure` in `/home/vgpnk/Projects/shokunin/mado-shokunin/tools/mado-tripwire.py:2293-2294`, and its reference walk skips a reference handed to a pure parent call in `/home/vgpnk/Projects/shokunin/mado-shokunin/tools/mado-tripwire.py:2386-2393`. The alias-form probe below exercises the general path rule rather than relying on the fixture's exact source text.

## One nearby counterexample

Retained inert scanner input: `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-21/w2/fixtures/AtkPureJson/PureJsonAlias.jsonl` (SHA-256 `6d9972a23a363c06b22485ec22c62179e15c9a86de41497b2a36535f76ca501f`). Its eval code is:

```python
from json import dumps as encode
import subprocess

def f(_obj):
    subprocess.run(["pacman", "-Q", "r21"])

class C:
    def __add__(self, other):
        f(other)

C()
encode(C(), default=f)
```

[INFERENCE] This is effectful: `C()` is not a JSON-native value, so `json.dumps` calls its supplied `default` function; the JSON API specifies that `default` is called for objects that cannot otherwise be serialized. `f` accepts that object and launches `pacman -Q r21`; the callback returns `None`, a JSON-encodable value. The scanner instead reports `exit: 0`, all five finding counts `0`, `findings: []`, `observed_findings: 0`, `lead_findings: 0`, `eval_unparsed: 0`, `unparsed_spawns: 0`, stderr empty. If followed, this command is `package_query` under the tool's pacman `-Q` classification (`/home/vgpnk/Projects/shokunin/mado-shokunin/tools/mado-tripwire.py:737-771`). The probe scanned the inert JSONL only; the Python payload was never executed. The gap is specifically the no-argument-sensitive purity exemption and callback reference skip, not the frozen formatter case.

## Reproducibility and limits

- Candidate revision observed: `f499a8db7171b7476fe9f204ab9edbac5a956fa9`.
- Exact `/home/vgpnk/Projects/shokunin/mado-shokunin/tools/mado-tripwire.py` bytes scanned: SHA-256 `2e152f6dcd9a0d13ffc1d64e88bcc600548e66bd04c34f92dbc5a0808338372d`.
- Probe used the existing `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-21/oracle/measure.py` `scan` API, which launches one scanner child with its 384 MiB address-space limit and 15-second timeout. No payload execution, full suite, or corpus run.
- The `lsp` device was unavailable (`xd://lsp` returned “No such tool”); text search only located source symbols/lines. Semantic conclusions are from the inspected source and the Python docs: [JSON encoder `default` parameter](https://docs.python.org/3/library/json.html#json.dump), [Python data model](https://docs.python.org/3/reference/datamodel.html).
- No tools installed or updated. This is one scoped counterexample, not a whole-tool completeness claim.

Report: `.ufo/waves/round-21/w2/reports/AtkPureJson.md`
