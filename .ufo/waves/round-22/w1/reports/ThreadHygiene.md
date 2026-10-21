# ThreadHygiene — C1 static-truth proposal (round 22, w1)

Seat: `MadoR22.ThreadHygiene` · Leaf member, no delegation. Artifacts only; no production edits, no measurements, no payload execution.

## Deliverable

`/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-22/w1/proposals/ThreadHygiene.json` — one independent C1 variant, `expected_kind: "exact"`.

## Variant (verbatim cell)

```python
import subprocess
import threading


def __mado_thread_target__():
    subprocess.run(["pacman", "-Q", "r22-thg"])


def worker():
    __mado_thread_target__()


threading.Thread(target=worker).start()
```

## Static truth (Python 3.14 semantics, never executed)

- `threading.Thread(target=worker).start()` schedules `worker` on a new thread.
- Inside `worker`, `__mado_thread_target__` is an unbound `Name` → global load → resolves to the module-level `def __mado_thread_target__`. The dunder spelling is a legal identifier and a legal module-global function name.
- That function calls `subprocess.run(["pacman", "-Q", "r22-thg"])`; argv is fully literal; `shlex.join` → `pacman -Q r22-thg`; `pacman -Q` → `package_query`.
- Exactly one statically determined result: `{"class":"package_query","command":"pacman -Q r22-thg","evidence":"observed"}`; zero unparsed; `forbid_observed_commands` empty.

## F5 mechanism exercised (why this variant discriminates)

r21 `FinalBindingReview.md` F5: the thread-start path injects `__mado_thread_target__` into the followed worker body's binding namespace (tripwire 2299–2304) to carry the resolved target. r21's fixture shadowed a same-named global *binding* (`__mado_thread_target__ = subprocess.run`); this variant shadow-tests a same-named global *function* called from the worker.

- Detector still injecting the reserved key → body's call resolves to the synthetic binding (= `worker`, already on the resolution stack, 2376–2383) → recursion-lead or silent miss instead of the required observed `package_query`.
- Correct repair (node-carried `mado_resolved`, or a non-identifier key like `"<thread target>"`) → global load reaches the real def → observed row.

## Contract conformance

- `expected_kind: "exact"` requires exact rows + zero unparsed: satisfied by construction (single literal argv, no unresolved names).
- One expected result only; no unrelated unsupported forms; no invented argv; no `want` rows beyond the single determined finding.
- Proposal independent of detector results: authored from r21 residual text + Python semantics only; no detector source, fixtures, or measurements read beyond the cited residual document.
- Inert: payload is a parsed-only Python source string; subprocess argv is inert marker text (`r22-thg`, a nonexistent package name); cells never executed.
- Source text treated as data; nothing executed; no installs, no probes, no package queries, no git writes.

## Sources read

- `.ufo/waves/round-22/registration.md`, `.ufo/waves/round-22/audit-contract.json`
- `.ufo/waves/round-21/residual/FinalBindingReview.md` (F5 mechanism + hygiene answer)
- `.ufo/waves/round-21/residual/MadoR21-2.FinalBindingReview/thread-key-{hygiene,control,run-direct}.jsonl` (variant differentiation)

## Unknowns / limits

- Exact `want` row schema (`class`/`command`/`evidence` field names) follows the assignment's literal shape; sibling conventions not consulted (independence requirement).
- Whether the repaired scanner additionally emits a lead row for the `worker` thread-target follow itself is an implementation detail the proposal does not constrain; `want` lists only the single determined observed finding.

## Tools

None installed or updated. No pacman transactions (host-wide pause observed).
