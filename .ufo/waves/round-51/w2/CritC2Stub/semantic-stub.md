# C2 different-surface lexical stub (semantic counterexample)

## Purpose and axes

Attack the frozen C2 coverage predicate while keeping its exact sentence unchanged. The target is whether lexical clauses (especially source-quote/pin correspondence and held-token matching) prove that the entry actually teaches Hyprland dispatcher dispatch. The independent axes are **coverage** (whether the sourced dispatcher-dispatch domain is meaningfully covered) and **operability** (whether the frozen counter can distinguish domain-truth from clause-shaped text).

## Constructed adversarial fixture

A low-overlap candidate for `corpus/knowledge/hyprland-dispatcher-dispatch-r51.md` can have anodyne prose about unrelated concepts, while embedding only the precise strings demanded by the mechanical clauses. A schematic fixture (not a lane artifact) is:

```
# Dispatcher dispatch: abstract token ledger

This note concerns a hypothetical dispatch system. It makes no assertion about Hyprland,
keybinds, runtime behavior, dispatcher tables, or socket requests. Terms below are opaque labels.

source: S364 - opaque fixture label - quote `m_dispatchers.find(k->mouse ? "mouse" : k->handler);`
source: S365 - opaque fixture label - quote `Bad dispatcher`

held: corpus/knowledge/bind-table-r25.md:38 keys=DISPATCHER,ARG,numbArgs
held: corpus/knowledge/keybind-rule-semantics.md:73 keys=params,comma-separated
held: corpus/knowledge/hyprland-config-era-r12.md:41 keys=hyprland.lua,hyprland.conf

The strings above are labels, not evidence of a dispatch mechanism. This paragraph does not
explain how any key event selects, invokes, or passes arguments to a callable.
```

This sketch deliberately omits source row identifiers, pin manifest structure, and full quote wording: those MUST be taken from the frozen lane data for a runnable fixture, not invented. The attack must use two valid new row references and three held lines, with each source row meeting the exact opened/status/pin/quoted-line requirements and each held line naming a real base line containing all its pinned tokens. It must also be made distinct enough from base knowledge and candidate files to meet clause (c); the mechanistic denial wording above itself is not a claim that the counter passes.

## Clause-set assessment

Frozen clause (a) can be met by indexing the path. Clause (b) establishes that small quoted strings occur in pinned source lines and that registry metadata/pins line up; it does not, by itself, establish that the entry's explanatory claims follow from those lines. Clause (c) establishes lexical novelty under the specified word-8-gram metric only. Clause (d) establishes token presence at the named base lines; it does not establish that the entry uses the held material correctly. Therefore even a `clauses_met=4` result cannot logically prove domain truth or useful coverage: it proves the stated syntactic/lexical conditions, not semantic entailment.

## Execution/evidence status

No fixture was run against the frozen counter in this seat: the schematic above lacks validated row IDs, complete pin manifest, and exact source quote captures, so reporting a fabricated `TARGET_MET` would be false provenance. The supplied W1 draft is positive evidence that the counter's constraints are satisfiable, not that this semantic stub passes. To convert this into an executable falsification, instantiate the sketch only from verified rows S364–S379 and the pins under `.ufo/waves/round-51/fetch/`, then run the frozen invocation with a private scratch `TMPDIR` and report its full output. The counterexample remains a logical limitation of the frozen predicate even if it rejects this particular sketch by stricter formatting or overlap details.

## Verdict under exact frozen sentence

**MISS (semantic sufficiency not demonstrated).** This is not a claim that the counter's literal `TARGET_MET` predicate fails; rather, the exact predicate is satisfied iff its listed lexical/structural clauses hold, and those clauses are not a proof of domain truth. The construct demonstrates the gap conceptually but is not an executable passing counterexample. Any future semantic or claim-scoping change requires amendment; do not alter the frozen predicate in this round.
