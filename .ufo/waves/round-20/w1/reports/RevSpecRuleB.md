# RevSpecRuleB — E1–E3 need precise call-path and binding rules before implementation

## Findings

### High — A name-only pure guard can erase genuine Rule-B findings after rebinding

E3 says rebinding defeats a pure-name exemption, but it does not state how the guard handles wildcard imports or opaque namespace mutation. Those are material: the current classifier's `PURE_ARG_CALLS` is a spelling-only set (`tools/mado-tripwire.py:1252-1257`), and the Rule-B branch suppresses a bare name unconditionally when its spelling is in that set (`:1430-1434`). `from x import *`, `globals()`, and `exec()` are recognized only as opaque changes to the literal-value environment (`:1220-1235`, `:1353-1367`); that does not taint the pure-name exemption. Attribute/subscript assignment targets yield no target name (`:1068-1079`).

[INFERENCE] A guard that newly exempts `frozenset` (required by E2 and absent from the current whitelist) by spelling alone would lose a current Rule-B lead in each of these forms when the imported/assigned target is a host-command wrapper:

```python
from x import *
frozenset(["pacman", "-Q", "hyprland"])
```

```python
globals()["frozenset"] = unknown_wrapper
frozenset(["pacman", "-Q", "hyprland"])
```

```python
exec("frozenset = unknown_wrapper")
frozenset(["pacman", "-Q", "hyprland"])
```

The first is a literal argv handed to an unknown imported callee, hence a lead under E1; the other two must not be declared pure merely from the callee spelling. Conversely, already-whitelisted `print` can be rebound by these same routes and is presently skipped by the spelling-only exemption. E3 should say that purity attaches to the binding at the callsite, not the identifier: recognize a proven pure binding as clean, a proven spawn binding as observed, an imported/opaque unknown binding as lead, and invalidate affected names after `import *`, `exec`/dynamic namespace writes, or builtins mutation. This preserves the current Rule-B lead while fixing the present `print` false-negative.

### High — E3's unconditional `del`/`reset` → lead rule contradicts builtin lookup

At module scope, deleting a global builtin spelling removes the explicit global binding; Python then resolves the name from builtins. A fresh kernel after reset likewise has its builtin namespace. Thus `print = unknown_wrapper; del print; print(["pacman", "-Q"])` and a reset followed by `print([...])` resolve to builtin `print`, not an unknown helper. E3's blanket “`del name` or a `reset` cell unbinds it (then ... lead)” would add a false lead for these cases. [INFERENCE] The correct distinction is: after `del`, resolve a builtin fallback when that spelling is a builtin and no opaque mutation defeats that proof; after reset restore the default builtin bindings and clear prior user bindings; only a non-builtin unresolved name is an unknown/unbound lead. Also define whether a name rebound to a *known pure callable* remains clean rather than treating every rebinding as lead.

### High — E1's required `observed` coverage is broader than the current helper/alias resolver

The current resolver recognizes imports from subprocess/os/asyncio in `aliases` (`tools/mado-tripwire.py:1339-1352`), but not assignments such as `run = subprocess.run`; Rule B sees a later `run([...])` as an unknown bare-name lead (`:1430-1434`). Yet E1 explicitly requires that alias to be observed. The same gap applies to `run = functools.partial(subprocess.run, ...)` and locally assigned aliases such as:

```python
def launch(argv):
    print = subprocess.run
    print(argv)
launch(["pacman", "-Q"])
```

[INFERENCE] The current `print` exemption hides the call in this example instead of observing the spawn reached through its binding. E1 should require ordered callable-binding resolution (including local aliases and partials) before assigning `observed`; otherwise the alias case is incorrectly demoted to `lead` or suppressed.

E1 also promises a helper body in an earlier eval cell of the same file, but helper definitions are rebuilt only from the current AST, and only undecorated synchronous top-level `FunctionDef`s are entered (`:1368-1374`). `scan_file` carries the literal-value environment across cells and clears it on reset (`:1544-1545`, `:1578-1583`), but does not carry helper definitions. [INFERENCE] A prior-cell `def launch(argv): subprocess.run(argv)` followed by `launch(["pacman", "-Q"])` is therefore not observed as E1 requires. Async defs, lambdas, nested defs, decorated defs, and generator functions likewise lack the promised helper resolution. E1 needs either corresponding support or an explicit unsupported-visible-helper outcome; do not mislabel such a case `observed` just because a body is textually present. In particular, an un-awaited async call and an un-iterated generator do not execute their bodies, while a decorator may replace or alter the binding. Specify that `observed` requires a statically selected path that actually invokes the spawn (await/iteration and decorator behavior included); define a conservative result when that path cannot be resolved.

### Medium — E3's “binding in effect” is not matched by the current definition map

The helper table is built from all eligible defs in the cell and keyed by spelling (`tools/mado-tripwire.py:1368-1372`); each call uses that table if its line is after the def (`:1411-1418`). It does not account for an intervening assignment/import/delete. [INFERENCE] For:

```python
def launch(argv):
    subprocess.run(argv)
launch = print
launch(["pacman", "-Q"])
```

the current table still selects the old `launch` body and can report `observed`, although the binding at the call is builtin `print`. The reverse ordering can miss a real later alias. E3 should explicitly require source-ordered binding state at each callsite, including rebinding between definition and invocation; conditional/opaque assignments must invalidate certainty rather than preserve a stale pure or helper binding.

### Medium — E2 needs a complete no-spawn set and must not equate “builtin” with “pure”

The current whitelist omits the motivating `frozenset` and listed example `type` (`tools/mado-tripwire.py:1252-1257`), as well as other builtins and imported aliases covered by E2. [INFERENCE] Consequently `frozenset(["pacman", "-Q"])` is currently treated as an unknown callee and Rule-B lead; `from shlex import quote as q; q([...])` is likewise not recognized as a pure stdlib callable because only bare spellings are checked. E2 should specify the exact pure-call inventory and resolve import aliases against the known-pure module/member list.

Conversely, “a Python builtin not rebound” is too broad if it includes `exec`/`eval`: they can execute arbitrary code. The existing list already contains both (`:1255`), while opaque detection only clears the literal environment and does not analyze a code string (`:1220-1235`, `:1358-1367`). [INFERENCE] `exec("subprocess.run(['pacman', '-Q'])")` is therefore not safely described as a pure call. Exclude dynamic code runners from the pure set and explicitly define their treatment (parse a safely literal body where supported, otherwise preserve an opaque/unparsed or lead outcome); do not silently call them pure.

## Residual risk

The working tool is still the harmful round-19 artifact: `sha256sum /home/vgpnk/Projects/shokunin/mado-shokunin/tools/mado-tripwire.py` returned `367be94773d8fec5e6df91f80ac777070c407c1128f7c75b3dcaa26cc83fdb4d`. Read-only `git -C /home/vgpnk/Projects/shokunin/mado-shokunin diff --no-ext-diff e629f73 -- tools/mado-tripwire.py` emitted no diff, so this is a specification review before the repair lands, not a review of an implementation diff. The current finding emitter also has no `evidence` field (`:1596-1602`); E1's output contract remains unimplemented here.

## Verification gaps

- These are source-derived findings; no fixture code was executed and no synthetic `--scan` probes or test suites were run. Statements marked [INFERENCE] are predicted from the AST branches cited above.
- No `lsp` endpoint is exposed in the available tool inventory, so LSP status/references/definition/diagnostics could not be queried. No grep output is used as semantic proof.
- No external sources or runtime behavior were checked.

## Limits

Reviewed the E1–E3 contract against the current tripwire source and the pre-registration revision only. Did not edit code, cases, sources, or other lane files. Did not inspect unrelated E4/C1/C2 work.

## Installs

none