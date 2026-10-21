# CaptureReturnedChain — C1 static-truth variant specification

Seat: `MadoR22.CaptureReturnedChain` (reviewer) · Lane: `/home/vgpnk/Projects/shokunin/mado-shokunin` · Wave: mado-r22-w1.
Independent truth specification only. No production edits, no detector measurements, no payload execution, no package queries. Source text treated as data.

## Deliverable

`/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-22/w1/proposals/CaptureReturnedChain.json` — valid JSON, single eval cell, `expected_kind: "exact"`.

## Variant and seat interpretation

Assigned variant: **"returned local name follows chained alias rebinding."** Among the three returned-family seats, the split I adopted:

- `CaptureReturnedAlias` — a nested `def` assigned to a returned alias name before `return` (aliasing, no rebinding).
- `CaptureReturnedRebound` — two nested `def`s, the returned name rebound directly to the second (`a = b; return a`), the literal r21 F3 repro shape.
- `CaptureReturnedChain` (mine) — the returned name is reached through an **intermediate alias that was itself rebound**: `relay = alpha; relay = beta; chosen = relay; return chosen`.

"Follows" is read as *the returned name's resolution must traverse the alias chain and take each name's binding in effect at its own binding point, replayed in statement order* — so the rebinding `relay = beta` wins because the copy `chosen = relay` happens after it.

### Cell (verbatim)

```python
import subprocess
def make():
    def alpha():
        subprocess.run(["pacman", "-Q", "r22-chain-alpha"])
    def beta():
        subprocess.run(["pacman", "-S", "r22-chain-beta"])
    relay = alpha
    relay = beta
    chosen = relay
    return chosen
make()()
```

## Static trace (Python 3.14 semantics, nothing executed)

1. `def alpha` binds `alpha` to function object A (argv `["pacman","-Q","r22-chain-alpha"]`); `def beta` binds `beta` to object B (argv `["pacman","-S","r22-chain-beta"]`). Function definition is a name-binding operation (executionmodel §Naming and binding).
2. `relay = alpha` binds `relay` to A.
3. `relay = beta` **rebinds** `relay` to B (simple_stmts: "The name is rebound if it was already bound").
4. `chosen = relay` binds `chosen` to the object `relay` denotes *at this point* — B. Names refer to objects, not to other names; `chosen` does not alias the name `relay` (executionmodel: "Names refer to objects").
5. `return chosen` returns B; `make()()` invokes B exactly once → `subprocess.run(["pacman","-S","r22-chain-beta"])` executes once. A is never invoked.

One cell keeps the case inside a single file's binding scope and avoids any cross-cell staleness dimension; one factory/one invocation yields exactly one statically determined row.

## Expected result

- `expected_kind: "exact"` — every argv is a list literal and every name resolves statically; no unresolved spawn exists, so nothing can legitimately be unparsed and no `lead` is defensible.
- `want`: `[{"class": "host_mutation", "command": "pacman -S r22-chain-beta", "evidence": "observed"}]`. `pacman -S` is a host mutation (matches the r21 convention where `-S` rows classify `host_mutation` and `-Q` rows classify `package_query`). `command` is the exact `shlex.join` serialization of the argv tokens (verified by computation: `shlex.join(["pacman","-S","r22-chain-beta"])` → `pacman -S r22-chain-beta`).
- `forbid_observed_commands`: `["pacman -Q r22-chain-alpha"]` — declared as a discriminating guard: observing the alpha command is precisely the F3-sibling defect of resolving the returned name to its first/def-adjacent binding instead of the post-rebinding binding.

## Defects this variant discriminates

An F3 repair passes only if it resolves `return chosen` by replaying the factory body in order with alias following:

- **Fails to pass:** keeping r21 behavior — returning A (`pacman -Q r22-chain-alpha` observed). Violates `want` and `forbid_observed_commands`.
- **Fails to pass:** resolving `chosen` to its RHS name `relay` but returning `relay`'s *first* binding A (a snapshot-at-first-binding table).
- **Fails to pass:** resolving `chosen` to `relay` but refusing to follow the `relay` → def-name step (repair that only handles `a = b` where `b` is itself the def name) — emits nothing/unparsed where an exact row exists.
- **Fails to pass:** resolving `chosen` to `relay`'s binding *at `return` time* — same answer here (B), so this cell alone does not distinguish late-chasing of the intermediate; that converse (copy-then-rebind, truth = A) is the natural sibling variant but was intentionally not conflated into this one ("prefer one expected result").

## Independence and sources

Expectation derived from Python 3.14 language semantics, not from detector code or output. `tools/mado-tripwire.py` was not read (no changed code exists to read). Read-only uses:

- `.ufo/waves/round-21/residual/FinalBindingReview.md` — F3 mechanism and the `returned-rebound` fixture shape this generalizes.
- `.ufo/waves/round-21/residual/MadoR21-2.FinalBindingReview/returned-rebound.jsonl` — fixture encoding precedent.
- `.ufo/waves/round-21/w1/oracles/CalledClosure.json` + `.ufo/waves/round-21/oracle/inputs/CalledClosure.jsonl` — prior frozen proposal conventions.
- `.ufo/waves/round-22/w1/sources/SourceClosure/cpython-3.14.8-Doc-reference-{executionmodel,simple_stmts}.rst` — binding semantics (fetched by SourceClosure; upstream `docs.python.org/3.14`, tag `v3.14.8` pinned in `git-ls-remote-v3.14.8.txt`).

## Checks performed

- Proposal parses as JSON; all six required keys present; the single cell byte-compiles under `compile(..., 'exec')` (syntax check only, never executed).
- `shlex.join` serialization of both marker argv lists verified by pure computation.

## Limits / unknowns

- The converse ordering (`chosen = relay` before `relay = beta`, truth = alpha) is a different seat-style variant; reported here as an interpretation note, not a second cell, per "prefer one expected result."
- Whether the eventual repair replays bindings correctly is outside this seat — this artifact is truth input only.
- No installs, no measurements, no probes, no git mutations. LSP not needed; reads + literal grep only.
