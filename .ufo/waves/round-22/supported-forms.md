# C1 pre-seal supported forms and boundary guards

This specification is written before implementation/measurement from W1 static truth and CriticScope findings. Original registration and all original expected proposals remain. No later counterexample may be excluded by inventing an unsupported classification after measurement.

## Exact-result forms claimed

- Straight-line, visible factory definitions with positional, keyword, literal-default, statically known star/double-star literal arguments; local literal rebinding before the first executed return; returned helper identity from executed Name/alias/chained bindings, not a def-name index.
- Stored and immediately invoked factory results in one eval cell or across persistent per-file eval cells; multiple same-factory instances must keep distinct lexical frames. Enclosing factory locals stay distinct from module globals; globals are read at invocation.
- Direct returned functools.partial wrapping a visible helper or spawn callable, fixed literal args/kwargs bound at creation, invocation kwargs override stored keywords; unbound free globals inside the helper remain late-bound. Plain nested factories and partial factories across cells remain part of the frozen finite test population, not post-result exclusions.
- Newly constructed stdlib Thread/Timer target/args/kwargs, stored/inline/aliased standard .start/.run, distinct instance target capture, no same-source-name collision. Timer cancellation, repeated invocation and a factory closure passed as Thread target are explicit adversarial guards, not a claim that every possible concurrent schedule is statically known.
- Uncalled same-scope function definitions do not execute merely because a factory returns another helper. Statements after a return do not change its returned identity.

## Uncertainty must not become invented observation

- A dynamic starred or double-starred factory argument may be unresolved. Its lexical parameter can NEVER borrow a same-named module literal at any evidence tier. The uncertainty oracle must forbid the borrowed command at all tiers; retain explicit lead/unparsed uncertainty where runtime binding could succeed.
- A definitely invalid call (missing required parameter, unknown keyword without **kwargs) raises before the factory body. Exact no rows/no invented command is a valid semantic expectation; do not require uncertainty merely to appease a detector. Any expected_kind normalization from an independent proposal is recorded before sealing, never from tool output.
- Shared mutable captured objects, later nonlocal cell mutation, opaque mutation or namespace reset may prevent exact static reconstruction. Do not print a stale pre-mutation command as observed. Boundary fixtures may require uncertainty/no-stale-observation rather than global semantic completeness. Preserve the independently stated exact truth separately; do not silently replace an exact proposal's denominator after measurement.
- Unknown cancellation/races, user subclasses overriding run, arbitrary descriptors, conditional/non-Name returns, arbitrary recursive return evaluators and external callbacks remain outside exact-result support. Their visible bodies/commands cannot be certified safe by absence of a finding; parse/error/lead outcomes remain uncertainty. These exclusions never authorize dropping a true prior finding on the frozen corpus.

## Identity and oracle rules

Exact cases compare complete sorted class/command/evidence row multisets and zero error counters, not subset containment. Unknown cases forbid every named invented command at ALL tiers when specified, forbid stale observed commands, and require an explicit uncertainty signal only when semantically warranted by their presealed truth. One original fixture is a passing control, not six independent original failures. F1–F5 name defect families; a finite pass closes only the named tested forms, never all possible family triggers.

F5 also requires fresh structural review: synthetic resolved callable metadata must not be stored under ANY legal source identifier in a source binding namespace. Renaming the old reserved key to another legal identifier is not repair even if the known collision fixture passes.
