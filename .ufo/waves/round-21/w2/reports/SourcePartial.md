# SourcePartial — round 21, w2

## Verdict

**Narrow match, not full descriptor coverage.** The current candidate's source path is consistent with S116 for a visible ordinary function wrapped by a class-body `functools.partialmethod(...)` and an explicit call such as `C().run()`: it resolves the underlying helper, accounts for the bound instance, and follows that helper at the call site. The source does not imply that defining the descriptor, constructing `C`, or defining other methods executes the wrapped body. The implementation does not resolve all semantically equivalent `partialmethod` spellings/descriptors; its recognition is syntactic.

## Reopened S116 and upstream quote

S116 identifies CPython v3.14.8 `Doc/library/functools.rst`, tagged raw URL: <https://raw.githubusercontent.com/python/cpython/v3.14.8/Doc/library/functools.rst>. I reopened the URL and the retained source body. The located quote is at line 429:

> “delegated to the underlying descriptor, and an appropriate”

The complete documented section is lines 417–436. Lines 426–430 describe delegation of `__get__` for a descriptor (including a normal Python function) and returning a partial object. Lines 432–436 separately describe non-descriptor callables and insertion of `self` before constructor-supplied arguments. These are binding rules, not a claim that storing a `partialmethod` or constructing an instance calls the wrapped function.

The tagged-source receipt records 32,022 bytes and SHA-256 `e938fb679d763ffc02472865a1ffbd816d0f4665068d1419b2d3ac6d1a9fbc31`; the reopened local body has the same SHA-256. S116 remains read-only; no source registry row was changed.

## Candidate source inspection

Inspected the current committed candidate `f499a8db7171b7476fe9f204ab9edbac5a956fa9` (not the earlier `2ac0f9b...`). Current bytes of `tools/mado-tripwire.py` SHA-256: `2e152f6dcd9a0d13ffc1d64e88bcc600548e66bd04c34f92dbc5a0808338372d`.

- `class_method_info` (`tools/mado-tripwire.py:1549–1574`) examines a class-body `Assign` whose value is a call and whose callee's final dotted component is literally `partialmethod`; it resolves the first argument and accepts it only when it is a helper. It marks the result `skip_first=True`, `bound_kind="instance"`, and carries the stored positional/keyword arguments.
- `callable_info` (`:1623–1637`) asks `class_method_info` for an attribute reached through a class or instance receiver. `spawn_scan` follows a resolved helper at an explicit call (`:2214–2219`, `:2248–2272`); `follow_helper` supplies the bound class/instance context (`:2185–2188`). This matches the direct `functools.partialmethod(worker)` plus `C().run()` shape in `.ufo/waves/round-21/oracle/inputs/PartialMethod.jsonl:1`.
- Construction has a distinct path (`:2276–2292`): it follows `__init__` if present and treats `__new__`/`__del__` as swept leads; it does not invoke every method. Other body sweeps also downgrade findings to leads (`:2106–2133`). Thus an instance construction or an unused method definition is not, by this path, evidence that every method executed.

A scope limitation is visible in the recognition predicate: `from functools import partialmethod as pm` produces the spelling `pm`, which does not satisfy the literal final-component check. The existing inert alias-shaped example is `.ufo/waves/round-21/w2/fixtures/AtkPartialMethod/partialmethod-alias.jsonl:1`; I did not execute it. Conversely, any unrelated callable whose final component is `partialmethod` passes that name test. The code does not resolve the callee binding to prove its identity is `functools.partialmethod`, and it does not cover the other descriptor forms enumerated in S116 through this branch. These are unverified/unsupported forms, not evidence that the direct case is wrong.

## Evidence and limits

- Repository commit observed: `f499a8db7171b7476fe9f204ab9edbac5a956fa9`.
- Code inspected: `tools/mado-tripwire.py`, SHA-256 above. No scanner, corpus, tests, or snippet was executed; there is no runtime output to report.
- S116 source body SHA-256 matches the registry/receipt value; the raw tagged URL was reopened and the located wording was present.
- No tool was installed. No LSP device/server route is exposed in the available tool inventory; search was used only to locate code, and findings above are based on the directly read source sections, not grep as semantic proof.
- Remaining unknowns: runtime disposition of the alias-shaped example; whether the intended detector contract includes imported aliases, arbitrary descriptor callables, or annotated class assignments. This report establishes neither detector completeness nor behavior outside the inspected code paths.
