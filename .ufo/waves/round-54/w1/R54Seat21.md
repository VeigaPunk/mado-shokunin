# R54Seat21 — C2 citation-context bypass

## Axes
Coverage: whether clause (c) demonstrates genuine call-site joins. Operability: whether a counter can distinguish citations from incidental text.

## Counterexample
A candidate entry can place two exact frozen host strings only in a disclaimer or quoted negative example, while making no affirmative host-join claim:

```text
Not asserted as joins (examples only):
`~/.local/share/omarchy/default/hypr/autostart.conf:1`
`~/.config/hypr/bindings.conf:2`
```

A counter that merely searches the entry text for two allowed `file:line` strings admits this as clause (c), despite the strings being explicitly disclaimed. Frozen clause (c) says the entry “carries at least two host join citations”; registration says the entry must cite ≥2 locations as `file:line` (claims-frozen.md:63-65; registration.md:71-76). Neither specifies that citations must occur in an affirmative host-join assertion or be linked to a stated fact. The six registered controls test missing joins, not incidental/negated occurrences (registration.md:78-90). This is distinct from repeated-citation counting (Seat22) and unsupported runtime inference from valid call-site citations (Seat36): here two distinct allowed locations are present, but only as explicitly non-evidentiary text.

## Smallest safe correction
At implementation/reporting time, require two distinct frozen identifiers in the entry's affirmative host-join section or in sentences that assert the corresponding launcher declarations; do not count code examples, quoted counterexamples, or explicit disclaimers. Keep the entry's interpretation narrow: citations ground declarations only, not execution or delivered environment. If frozen wording cannot be clarified post-score, treat this as an admission ambiguity and report honestly rather than silently changing the predicate.

## Evidence and commands
- `read skill://godspeed` — read the required axes/iteration instructions.
- `read .ufo/waves/round-54/claims-frozen.md` — read C2 predicate and causal input boundary; clause (c) at lines 55-65 and C2 inputs at 82-84.
- `read .ufo/waves/round-54/registration.md` — read frozen host set and controls, lines 71-90.
- `read .ufo/waves/round-54/w1/swarm-registry.json:128-133` — confirmed R54Seat21 is registered as critic.
- `grep 'counter.*host|host.*citation|frozen host|C2-CTL-6|PRED-C2' .ufo/waves/round-54` — observed frozen predicate/control references and sibling reports; no claim of counter implementation inspection.
- `glob quality/counters` — listed counter directory; the visible first page does not establish whether the round-54 counter exists (no implementation or producer was executed).
- `read /home/vgpnk/.omp/agent/RULES.md` — read tool-install policy; no tool installed or updated.

Attack: PRED-C2-r54 clause (c), specifically false-positive host-join evidence from incidental or expressly negated citations. No predicate changes made.

## Report trailer
Lane-relative report: `.ufo/waves/round-54/w1/R54Seat21.md`. No tracked lane edits, fixture or scratch artifacts, git/jj mutations, host/config/domain reads, package queries, producer execution, or tool updates.