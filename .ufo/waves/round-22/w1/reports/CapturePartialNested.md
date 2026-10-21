# CapturePartialNested — C1 truth proposal: stored returned partial from factory across eval cells

Seat: `MadoR22.CapturePartialNested` (revenger) · Wave mado-r22-w1 · Proposal: `.ufo/waves/round-22/w1/proposals/CapturePartialNested.json` · Author-lane freeze only; no production edits, no measurements, no payload execution.

## Godspeed axes

1. Proposal truth correctness (Python 3.14 semantics, exact and zero-unparsed).
2. Minimality / supported-form compliance (bounded static-source-shape agreement).
3. Falsification power against the r21 F1 partial defect.
4. Honest rejection of unsupported shapes instead of guessed expectations.
5. On-time delivery of exactly my named paths; no sibling or shared edits.

## Variant selected (minimal supported literal-source form)

- **Cell 1** — define module helper `run_pkg(cmd)` that calls `subprocess.run(cmd)`; define factory `make(cmd)` returning `functools.partial(run_pkg, cmd)`; create and **store** the returned partial: `stored = make(["pacman", "-S", "r22-pn-build"])`.
- **Cell 2** — rebind a module global with the same name as the factory parameter (`cmd = ["pacman", "-Q", "r22-pn-late"]`) and invoke the stored partial: `stored()`.

Storage plus cross-cell invocation is the point of the seat: the partial must be carried through the persistent eval namespace (cells run with `reset:false`) between its creation cell and its invocation cell, with a same-named global trap armed in the invocation cell.

## Frozen truth (static reasoning, never executed)

Exactly one row, everything else absent:

| class | command | evidence |
|---|---|---|
| `host_mutation` | `pacman -S r22-pn-build` | `observed` |

`expected_kind: "exact"` — zero unparsed. `functools.partial` copies its fixed argument objects when the `partial(...)` expression runs: inside `make`, the parameter `cmd` already holds the literal list object, so the partial freezes that object in its args tuple at construction. Cell 2's global rebinding rebinds only the name; the stored partial is unreachable by it. `stored()` therefore runs `run_pkg(["pacman","-S","r22-pn-build"])` → `subprocess.run(["pacman","-S","r22-pn-build"])`. Serialization is `shlex.join` tokens: `pacman -S r22-pn-build`. `forbid_observed_commands: []` per the exact template; under exact semantics any extra row already fails, and the wrong-value row is documented below.

## Counterexample this freezes (failure signature of r21 bytes)

At the reviewed bytes `46c82902896da0ec0ebd54254b1891667fa5da48f8cb297ee08bfb337e34c8c1` (sha256 re-verified in the working tree; lane HEAD `a963ce67…`, tool bytes unchanged — no changed code exists):

- `callable_info` partial branch (~1635–1638) stores the fixed arguments as **AST nodes** (`fixed_nodes=node.args[1:]`) when the wrapped callable is a helper, not as frozen creation-time values.
- The helper-follow site (~2384–2388) rebuilds the call from `fixed_nodes` and evaluates them in `cenv` — the **invocation** statement's environment.
- Cross-cell, `envs`/`binding_envs` persist (per FinalBindingReview, citing 2643–2644, 2685–2686), so cell 2's `cenv` resolves `cmd` to the late global `["pacman","-Q","r22-pn-late"]` and reports **observed `pacman -Q r22-pn-late`** while the true `pacman -S r22-pn-build` host mutation is missing. That is the F1 partial class ("Same class, by source, not probed" in round21 `residual/FinalBindingReview.md`).

Design consequence found while grounding: the r21 partial path only triggers when the partial wraps a **helper def** (`wrapped.get("kind") == "helper"`). A partial wrapping `subprocess.run` directly falls through as unresolved and is silently unfollowed. The proposal therefore wraps a module helper — the minimal form that is inside the declared supported shapes and actually exercises the F1-partial branch.

## Unsupported shapes rejected (honestly, not guessed)

| Rejected shape | Reason |
|---|---|
| `functools.partial(subprocess.run, cmd)` (no helper def) | Outside the followed partial shape at the reviewed bytes; would be a silent miss, not an exact-truth proposal. |
| Keyword-fixed partial args, invocation-time override (`partial(run_pkg, x=...)` then `stored(x=...)`) | CapturePartialOverride's variant; mixes override semantics with timing. |
| Partial wrapping a helper that reads a late module global in its own body | CapturePartialGlobal's variant; module-global late binding, a different mechanism than partial argument freezing. |
| Star/dict-splat or non-literal factory arguments, unknown keyword, missing required parameter | F2 territory: unbindable → uncertainty (lead/unparsed), never exact. |
| Stored-name rebound between cells (`stored = other`) before invocation | Callable-identity variant (F3 territory); changes which object is invoked. |
| Container/subscript storage, non-`Name` factory returns (`return a if c else b`) | Not examined by the round21 review; unsupported here. |
| `reset:true` between cells | Destroys the cross-cell persistence the seat exists to test. |
| Extra call-time args (`stored("-x")`), mutation of the captured list, alias imports of `functools` | Extra shape beyond the minimal supported form; excluded to keep one expected result. |

## Unknowns and limits

- Truth is static Python-semantics reasoning about `functools.partial` object construction; nothing was executed (payloads are inert scanner input by contract).
- No detector measurement, no probes, no fixture runs; reset flags, JSONL assembly, digests and expected.json are owned by the harness/executor seats, not this proposal.
- No tools installed or updated; no installs needed. Git used read-only (`rev-parse` only); no lane state touched.
- Grounding of lines 1635–1638 and 2384–2388 was read directly in the working-tree tool; the cross-cell persistence claims are taken from the round21 review (by-source, not probed there either).
