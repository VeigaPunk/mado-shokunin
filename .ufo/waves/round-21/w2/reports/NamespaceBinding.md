# Namespace binding — Round 21 W2

## Tested candidate and method

- Candidate commit: `f499a8db7171b7476fe9f204ab9edbac5a956fa9`.
- Exact scanner bytes: `tools/mado-tripwire.py` SHA-256 `2e152f6dcd9a0d13ffc1d64e88bcc600548e66bd04c34f92dbc5a0808338372d`.
- Probe fixture: `.ufo/waves/round-21/w2/fixtures/NamespaceBinding/closure-namespace-shadow.jsonl`, SHA-256 `7edbabb6189fc0ba30243be89487b913c4ad69b534ed67958fa64a34d776d30f`.
- Ran the existing `.ufo/waves/round-21/oracle/measure.py` `scan` API once; it launched one scanner child with the runner's 384 MiB address-space cap and 15-second timeout. The fixture is inert transcript JSONL; no snippet code was executed.
- Observed scanner result: exit `1`, `host_mutation: 2`, `eval_unparsed: 0`, `unparsed_spawns: 0`, and two findings both marked `evidence: observed`:
  - `pacman -S closure-shadow` (`NamespaceBinding-closure-shadow`)
  - `pacman -S namespace-shadow` (`NamespaceBinding-namespace-comparator`)
- No tools were installed.

## Findings (severity order)

### Medium — Returned closure can report a same-named module global as observed

The fixture sets module `argv` to `['pacman', '-S', 'closure-shadow']`; `make()` then assigns its own local `argv` to `['pacman', '-Q', 'safe-closure']`, defines `run()` to call `subprocess.run(argv)`, returns `run`, and invokes `make()()`. Under Python closure binding, `run` reads the local cell from `make`, so the command is the harmless `pacman -Q safe-closure`; that expected behavior is inferred from the inert source, not executed. The scanner instead emitted `pacman -S closure-shadow` as an **observed host_mutation**.

The resolver recognizes a directly returned nested helper (`tools/mado-tripwire.py:1613-1622`), but the capture handling binds only the outer call's formal arguments (`:2232-2235`). `follow_helper` seeds the returned helper's environment from the call-site environment and overlays only bound parameters (`:2189-2196`); it does not capture the outer helper's local assignment or shadow the corresponding module global. This makes a global binding look like the closure cell's observed argv. Preserve the closure's lexical bindings, or avoid claiming an observed literal when those bindings cannot be resolved.

### Medium — Namespace comparison with user-defined equality leaves a stale literal environment

The fixture sets module `argv` to `['pacman', '-S', 'namespace-shadow']`, then compares `Comparator() == globals()`. `Comparator.__eq__` assigns `namespace['argv'] = ['pacman', '-Q', 'safe-namespace']`; Python passes the live globals dictionary to that method, so the subsequent `subprocess.run(argv)` reads the safe query command. This expected behavior is inferred from the inert source, not executed. The scanner nevertheless emitted `pacman -S namespace-shadow` as an **observed host_mutation**.

`namespace_read_only` accepts any `ast.Compare` containing a `globals()`/`locals()`/`vars()` call as read-only (`:1440-1452`), although comparison can invoke arbitrary user `__eq__` code. Consequently `opaque_statement` does not clear the tracked environment after this compare (`:1476-1487`); `opaque_module_mutation` also skips function bodies while scanning (`:1455-1473`), so it does not account for the comparator's dictionary write. Do not treat arbitrary comparison as a read-only namespace use; invalidate literal bindings when the effect cannot be proven read-only.

Both rows are false observed evidence, not evidence that the fixture executed either command. The observed scanner payload is the concrete defect; the safe actual argv descriptions above are static Python-semantics conclusions from the inert fixture.

## Residual risk and verification gaps

- This falsification covers the two supplied constructs only; it is not an exhaustive proof for all closure, default-argument, `nonlocal`/`global`, rebinding, or namespace-access forms.
- The `lsp` device is unavailable in this seat (`xd://lsp` returned `No such tool`), so no LSP status, references, definition, or diagnostics checks were possible. Source review used the displayed scanner ranges; grep search was only navigational, not semantic proof.
- No full corpus or suite was run, per seat scope. No snippet was executed and no tools were installed.

## Verdict

**Candidate falsified for C1:** one bounded scanner-only probe produced two invented `observed` host-mutation argv findings from wrong closure/namespace bindings. Both are fail-closed false positives, but they violate the scanner's observed-evidence contract and can reject safe input or misstate what argv was observed.
