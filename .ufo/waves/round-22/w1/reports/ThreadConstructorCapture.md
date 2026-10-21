# ThreadConstructorCapture — scoped seat report

Seat: `MadoR22.ThreadConstructorCapture` · Lane: `/home/vgpnk/Projects/shokunin/mado-shokunin` · Wave: mado-r22-w1.

## Deliverable

`/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-22/w1/proposals/ThreadConstructorCapture.json` — one independent static-truth C1 proposal, inert, never executed.

## Variant

A single eval cell. `cmd` names list `["pacman","-S","r22-ctor"]`; `threading.Thread(target=worker, args=(cmd,))` is constructed; `cmd` is then rebound to `["pacman","-Q","r22-ctor-late"]`; `t.start()` is called. This is the scheduled-call analogue of residual F1: does the detector capture the `args` object at `Thread(...)` construction or re-evaluate the name at the scheduled-call site?

## Frozen expectation

- `expected_kind`: `exact`
- `want`: one row — `host_mutation`, command `pacman -S r22-ctor` (shlex.join of `["pacman","-S","r22-ctor"]`), evidence `observed`. Zero unparsed required: every argument is statically determined.
- `forbid_observed_commands`: `pacman -Q r22-ctor-late` — the rebound decoy is never passed to any callable; an observed row naming it is a fabrication.

## Static reasoning (Python 3.14.8)

1. `(cmd,)` is evaluated inside the `Thread(...)` call at construction time; the tuple stores the list object, not the name.
2. `Lib/threading.py:925-928` — `self._target = target`, `self._args = args`, `self._kwargs = kwargs`, stored by reference in `__init__`.
3. `cmd = [...]` rebinding creates a new list and rebinds the name; the captured object is unchanged (simple_stmts.rst: assignment "(re)bind names to values").
4. `t.start()` → `Thread.run` (`Lib/threading.py:1023-1024`) invokes `self._target(*self._args, **self._kwargs)` = `worker(["pacman","-S","r22-ctor"])` → `subprocess.run` sees only the construction-time argv. `pacman -S` → `host_mutation`.

## Sources

- Pinned: `.ufo/waves/round-22/w1/sources/SourceThread/threading-v3.14.8.py`, CPython `Lib/threading.py` @ v3.14.8, sha256 `5323909624ec2165e70b6d31333e4191b63d383d2dc5a7d7d516a3475ea2b7e3` (peeled commit `8e6e75d9…`, blob `c03b0b53…`); sibling seat `SourceThread`'s receipt verified lines 925-928, 1023-1024, 1082.
- `.ufo/waves/round-22/w1/sources/SourceClosure/cpython-3.14.8-Doc-reference-simple_stmts.rst:83-84` (rebinding).
- `.ufo/waves/round-21/residual/FinalBindingReview.md` F1 (read for defect context only, as authorized).

## Unknowns / limits

- `want` vs `forbid_observed_commands` consumption is defined by the seat prompt's schema, not by an observed comparator; the harness contract for "exact" (set-equality vs required-subset) is not visible to this seat.
- No detector output was consulted; proposal is independent of any measurement. Cell content is inert ast-scanner input only.
- Mutating-in-place decoys (`cmd[:] = ...`, `cmd.append`) are intentionally out of scope — rebinding only, per the seat's assigned variant.
- `.join()` omitted to keep the cell inside the minimal Thread+start supported shape.

## Compliance

- No production edits, no detector runs, no payload execution, no package queries, no installs, no probes, no delegation, no Git mutation. Git untouched.
- Tools installed/updated: none.
