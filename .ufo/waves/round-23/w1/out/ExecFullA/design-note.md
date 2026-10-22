# ExecFullA design note — C1 mado-tripwire candidate

Change set (3 surgical corrections in `tools/mado-tripwire.py`), following the
prescribed round-22 residual design “Smallest safe corrections”:

1. **Defining-frame env for callees (residual gap 1 / frame leak).**
   - Helper bindings now record the scope they were defined in
     (`update_bindings(..., scope=...)`; "module" for the module body,
     "function" inside a helper body, "class" inside a class body), and
     `prepare_eval_calls` threads that scope to every registration.
   - `spawn_scan`/`follow_helper` thread a `genv` map (module-global literal
     env per call node, taken from the top-level statement snapshots).
   - `follow_helper` builds the callee body env from its *defining frame*:
     `genv` for module/class/factory helpers (module globals as of the call +
     own `closure_env` overlay + bound args); `cenv` only for nested defs
     whose closure is the current frame (e.g. `NestedDefReadsDefiningFrame`).
     This stops caller locals (`forward(argv, ...)`'s `argv`,
     `caller()`'s local `argv`) from leaking into module-level callees.
   - Recursive `spawn_scan` calls (scheduled invoke, methodcaller, dictConfig)
     propagate `genv`.

2. **Non-escaping consumer callback sweep suppression (residual gap 2 /
   pin (b)).**
   - `parameter_escapes(fn, param)`: a parameter escapes when it is stored,
     returned, aliased or handed to another call (any use other than as the
     direct callee of a Call node inside the consumer).
   - After a consumer helper is followed with zero unparsed and no opaque
     statement, `consumer_unescaping_args` records the argument ids bound to
     parameters that *cannot* escape; the refs loop then skips sweeping those
     callback bodies (their analysis was already covered by the followed
     consumer). Callback stores (`hooks["k"] = callback`,
     `box.cb = callback`) still escape → sweep kept → lead rows preserved
     (CallbackStoredInDict/OnAttribute still pass as `present`).

3. **No redundant sweep of a body already followed in the same cell.**
   - `follow_helper` adds the followed body id to `ctx["swept"]` on success,
     so a later reference sweep of the same body is skipped. This removes
     duplicate analysis that only inflated `unparsed_spawns`
     (e.g. ForwardExistingClosureWithoutFrameContamination: the returned
     closure is followed via `job()` and was also swept as `forward`'s
     callback argument).

No changes to shell classification, frozen mode, selftest harness, or other
tools. Diff is confined to `tools/mado-tripwire.py` (+121/−22 lines).
