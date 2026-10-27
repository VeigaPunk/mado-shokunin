# Falsify30 — C2 proposition-map completeness

## Deliverables

- This report: `.ufo/waves/round-52/w1/Falsify30.md`

## Finding

- **Attacked item/predicate:** C2, proposition-to-source support and complete material-proposition mapping (claims-frozen.md §C2; registration.md §Frozen predicates).
- **Concrete bypass:** the existing C2 counter’s `bind_row`/`clause_b` checks source-row binding at the *line* granularity, not the proposition/rationale granularity. `bind_row` accepts a quote paired with the locator or *any* quote on that same line if it occurs in the pinned span (`quality/counters/c2-r51-dispatch-entry.py:329-375`). `clause_b` then marks a row verified if any prose line mentioning its ID succeeds (`:407-424`); it has no check that the quote supports the line’s proposition, nor a count/map of propositions. Thus the counter can report valid source binding while a material proposition on the same line remains unsupported/unmapped.
- **Reproducible setup/command:** source-only inspection, from lane root:
  `python3 -c 'from pathlib import Path; p=Path("quality/counters/c2-r51-dispatch-entry.py").read_text().splitlines(); print("\\n".join(f"{i+1}:{p[i]}" for i in range(328,375))); print("\\n".join(f"{i+1}:{p[i]}" for i in range(406,424)))'`
  This prints the exact acceptance path and requires no producer, package query, host read, or mutation. I additionally checked the existing round-51 entry’s source-row lines (`corpus/knowledge/hyprland-dispatcher-dispatch-r51.md:14-19`) against its multi-step factual claims (`:90-106`): row-level verified quotes do not establish proposition-level mapping.
- **Actual result:** reproduced by code-path inspection: a single matching quote on an S-row prose line suffices to mark that row verified; separate or additional factual propositions on the line are not examined by the counter. **Reproduced: yes (structural bypass);** no new adversarial fixture was executed.
- **Source evidence:** local source, `quality/counters/c2-r51-dispatch-entry.py`, lines above; local example entry, `corpus/knowledge/hyprland-dispatcher-dispatch-r51.md`. No external source candidate opened; no URL/access date/quote applicable.
- **Axis:** coverage is at risk: row/pin/quote presence is not equivalent to every material proposition being mapped. Operability: no demonstrated harm; source-only attack adds no runtime or producer dependency.
- **Limitations / dissent:** the frozen predicate separately requires an outside reviewer to judge source truth. This attack establishes that the counter alone does not enforce proposition completeness; it does not establish that the outside reviewer missed any unsupported claim or that C2 fails overall. No frozen claim or predicate edited.
- **Verification:** inspection only; no tests or producers run. Scratch not created; no tooling installed.

## Report

Report: `.ufo/waves/round-52/w1/Falsify30.md`

