STATUS: defect

# R83ReviewerC1 — C1 causal proof

Axes: causal discrimination, explicit-precedence coverage, deterministic identity/order handling. Reviewed frozen tool diff from base 67dd2b667b72f7f72309340d488b355d543841a5 to dbc09269fe547ab13541e722dd7d2ba33015f348; inspected all eleven added cases. Tool SHA256: 8b17706014e6708a11413f0bd6c3398ca4e1b95b40b9c2d51f80f5064c677207. Experiments used frozen counter/cases/tool bytes extracted read-only, not the concurrently modified working-tree counter.

## Findings, by severity

### P1 — Non-bar live-box echo survives every frozen case

Affected evidence: `tools/mado-barfoot.py:808-814` allocation resolution; `.ufo/waves/round-83/controls/c1-cases-r83.json` cases `extra-dyn-band-top`, `extra-dyn-band-dock`, `extra-dyn-band-bottom`, `extra-dyn-band-explicit`, `alloc-two-namespaces`; `quality/counters/c1-r83-surface-band.py:run_cases/expected_ok`.

Concrete mutant `extra-live-band`: immediately after the existing `spec[axis] = band_of(spec, allocation)`, insert:

```python
            if spec is not bar_spec:
                observed = find_layer(layers, monitor, spec["level"], spec["namespace"])
                if observed is not None:
                    spec[axis] = int(observed["h" if axis == "height" else "w"])
```

Observed result: **58/58 correct**, no failing cases. Mutant SHA256: c889681c1e5531779c6ac76a50c1d794ac2189d0706872eb035e79785331bd7c. This keeps allocation validation/refusals but replaces the actual non-bar band with the observed box axis. Every added positive non-bar fixture makes allocation equal that observed axis. Both V7 discrepancy cases instead perturb only the bar, leaving the newly expanded class unprotected.

Independent discriminator: take `extra-dyn-band-top`, keep panel allocation 40 and monitor top reserved 66, change only live panel height from 40 to 46. Original: rc=1, boxes=MATCH,DIFFER, reserved=EQ, expected=66, attr=0,66,0,0. Survivor: rc=1, boxes=MATCH,MATCH, reserved=DIFFER, expected=72, attr=0,72,0,0. Same final DIFFER/rc does not imply correct causality; the frozen suite currently cannot distinguish these implementations on its existing inputs.

Required coverage direction: a non-bar allocation/live disagreement, with boxes, expected reserve and attribution pinned independently. This is a counter proof gap, not an observed defect in the frozen implementation.

### P2 — Explicit exclusive-zone precedence is not discriminated for allocated extras

Affected evidence: `tools/mado-barfoot.py:604-611` preserves an explicit exclusive integer; case `extra-dyn-band-explicit` sets allocation=40 AND exclusive=40.

Concrete mutant `extra-allocation-overrides-zone`: after resolving a dynamic band, insert:

```python
            if spec is not bar_spec and isinstance(spec["exclusive"], int) and spec["exclusive"] > 0:
                spec["exclusive"] = spec[axis]
```

Observed: **58/58 correct**. The declared band and explicit exclusive zone are separate quantities, but this fixture makes them indistinguishable.

Discriminator: take `extra-dyn-band-explicit`, retain allocation/live height 40, set exclusive=12 and monitor top reserve=38. Original: rc=0, boxes=MATCH,MATCH, expected=38, attributed=38, reserved=EQ, CLEAN. Survivor: rc=1, boxes=MATCH,MATCH, expected=66, attributed=66, reserved=DIFFER. A case with different explicit zone and allocation would kill this mutant.

### P2 — Non-bar explicit size precedence has no conflicting allocation fixture

Affected evidence: `tools/mado-barfoot.py:459-475,808-814`; carried case `alloc-explicit-ignored` checks the bar only.

Concrete mutant `extra-allocation-overrides-explicit`: before the existing dynamic-band condition insert:

```python
        if spec is not bar_spec and spec[axis] > 0 and spec["namespace"] in allocation:
            spec[axis] = allocation[spec["namespace"]]
```

Observed: **58/58 correct**, no failing cases. SHA256: e5e902a8440a92bb64ac29f5489fd95658b16ffb611fd16c6de60f9f34bebe98. This breaks explicit declared-size precedence for extras while preserving the bar-only precedence fixture. Add a positive explicit extra size with a differing allocation to distinguish it. No failing production example is alleged here: this is a demonstrated surviving mutation.

## Checks that held

- Single-reader live extent substitution (`edge_extent(bar, live_box, usable)`): 57/58; killed exactly by `alloc-live-band-differs`.
- Replacing every resolved composition band with its live axis: 57/58; killed exactly by `alloc-live-box-differs-composed`. Thus the bar discriminators genuinely work; their scope is the issue.
- Named `same-level-order-ignored`: 57/58; killed by `same-level-order`.
- Named `alloc-explicit-overridden`: 38/58; includes failure of `alloc-explicit-ignored`. This protects bar precedence, not the non-bar variant above.
- `find_layer` rejects duplicate live namespace hits at the same monitor/level: observed model refusal `more than one 'panel' layer on monitor M1 level 3` (`tools/mado-barfoot.py:951-962`). Declaration ordering is explicitly `(level, -order, index)`, with exclusive-positive pass first (`:815-833`). No ordering implementation defect found.
- Duplicate allocation JSON keys are last-wins: `parse_allocation(b'{"panel":40,"panel":46}')` returned `{'panel': 46}` because `load_json` uses plain `json.loads` (`:219-227,439-456`). Surface declarations do not impose namespace uniqueness (`:649-718`); no uniqueness contract was found, so this is a residual input ambiguity, not an asserted violation.

## Receipt and verification gaps

Frozen dbc09269 counter has `MUTANTS = 38` but 39 mutation entries. Existing `.ufo/waves/round-83/receipts/measurement-c1-r83.txt` honestly ends `mutants=38 killed=39 ... verdict=TARGET_MISSED`. The working-tree counter was already changed to 39 during review; that known clerical correction was not edited or remeasured by this seat. Updating the constant does not close the three surviving mutations above.

Executed only the requested scratch mutation/case probes and duplicate parsing/lookup probes. Counts above are frozen `run_cases` correctness, NOT full counter admission, selftest success, mutation-of-mutation saturation, or a fresh base/control run. The supplied receipt is prior evidence, not this seat's rerun. No saturation claim is warranted.

Semantic device unavailable: `read xd://lsp` returned `No such tool`; no references/definition/diagnostics server could be used. Source and frozen diff inspection are textual evidence, not semantic proof. Resume/rerouting contracts are outside this tool diff and seat scope.

Scratch `/fast/scratch/hyaku/mado-r83/R83ReviewerC1` removed before handoff. No instruments edited, git/jj mutations, installs, host captures, service operations, or other-runtime invocation. Only this report persists. Recommendation only, not a lane-admission vote.

Report: .ufo/waves/round-83/w1/R83ReviewerC1.md
