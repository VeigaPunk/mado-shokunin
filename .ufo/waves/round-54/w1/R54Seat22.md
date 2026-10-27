# R54Seat22 — C2 adversarial attack (item 22)

Axes: coverage, operability. Scope: frozen PRED-C2-r54 only; no predicate changes.

## Counterexample: duplicate host citation may satisfy the two-join threshold

Frozen claim clause (c) says the entry must carry “at least two host join citations among the frozen host set” (claims-frozen.md lines 63–65). Registration gives eight allowed host locations and requires “≥2 as `file:line`” (registration.md lines 71–76). Neither sentence requires distinct locations, distinct host files, or independent joins. Thus an entry repeating the same allowed `file:line` twice may meet a naive count of citation occurrences while evidencing only one join. This is a distinct threshold/identity bypass, not a quote mutation.

Exact attack input (illustrative entry lines):

```
Host joins: `~/.local/share/omarchy/default/hypr/autostart.conf:1`; `~/.local/share/omarchy/default/hypr/autostart.conf:1`.
```

The registration states no prohibition against repetition. This does not establish how an unlanded counter currently behaves; the C2 counter is absent in the inspected committed counter directory (glob listed prior counters, no `c2-r54-uwsm-entry.py`). Therefore classify this as a frozen-contract ambiguity / required adversarial fixture, not an observed implementation failure.

## Smallest safe correction

Interpret “two host join citations” as two distinct normalized `file:line` locations from the frozen set (at minimum require distinct locations); make the counter compare a set rather than citation occurrence count. If frozen wording must remain immutable after scoring, preserve it and report the ambiguity rather than silently changing the predicate. A stronger authority check that a claimed host path/line exists is not supported by this contract's explicit static-pin-only/no-host-read boundary and should not be added here.

## Evidence / commands

- Read `.ufo/waves/round-54/claims-frozen.md` lines 55–75: clause (c), frozen host set, and do-nothing controls.
- Read `.ufo/waves/round-54/registration.md` lines 71–90: host citation threshold and six frozen C2 controls.
- Read `quality/counters/` directory: no `c2-r54-uwsm-entry.py` is present among the listed entries; no producer executed and no host/config reads performed.
- No tools installed or updated.

Attack predicate: PRED-C2-r54 clause (c), specifically citation threshold semantics. Controls C2-CTL-1 through C2-CTL-6 do not exercise duplicate citation counting (registration.md lines 78–87).