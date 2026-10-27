# R54Seat18 — C1 coordinated pin/manifest mutation attack

## Axes

Operability: the verifier must bind evidence to the frozen round-52 bytes, not merely self-consistent bytes in the scored tree. Coverage: exercise a distinct input beyond the six individually enumerated controls.

## Finding — untested coordinated digest substitution

**Attack:** change an irrelevant byte in one pinned source file (outside every frozen quote and anchor), then update that file's digest in the same revision's `.ufo/waves/round-52/fetch/SHA256SUMS.txt`. Keep the four cited excerpts and their line numbers intact. A counter that computes/compares each pin only to the checksum manifest read from `--rev` will still report `pins=4/4`, and all quote/anchor checks can remain true. Yet the modified pin bytes do not hash to the frozen round-52 recorded digest in `registration.md` (P19's expected SHA-256 is explicitly `a83abeb57175e65908d8d67ddc9802310134e5a4752fa3764f980401b48a7637`). That implementation would admit an input violating PRED-C1-r54 clause (c).

This is distinct from C1-CTL-3's one-nibble-only manifest mutation (`registration.md`, C1 controls): the frozen control catches a manifest-only tamper, but does not establish rejection when the pin and its mutable manifest entry are changed consistently. To satisfy the frozen predicate, the checker must compare against the frozen digest(s), not treat the revision's checksum file as the authority. Whether the eventual counter does so is **unverified**: the base receipt records no C1 r54 counter (`claims-frozen.md:32-35`; `receipts/before.txt:2-4`), and this seat did not run a producer.

### Exact reproduction recipe (isolated mutated-tree control)

Against a disposable fixture commit whose tree is otherwise the scored tree:

1. In `.ufo/waves/round-52/fetch/Hyprland-ConfigActions.cpp`, change one byte on a line outside `1554-1558` and `1576`; preserve line count and all registered quotes.
2. Recompute that file's SHA-256 and replace only its matching value in `.ufo/waves/round-52/fetch/SHA256SUMS.txt`.
3. Commit the fixture mutation, then invoke `python3 -I quality/counters/c1-r54-errata-truth.py --repo <fixture> --rev <fixture-rev>`.

Expected per the frozen contract: nonzero and `verdict=TARGET_MISSED` because that pin no longer hashes to the fixed P19/P20 round-52 digest. A counter that returns `TARGET_MET` demonstrates the bypass. This procedure is a test specification, **not a run result**; no fixture or mutation was made.

## Do-nothing/control reachability

The frozen contract makes the all-print/do-nothing implementation rejectable: controls C1-CTL-1 through C1-CTL-6 each alter a required input and require rejection (`registration.md`, C1 control table; `claims-frozen.md:41-44`). Thus a counter that emits the target line without reading the selected revision cannot satisfy `controls=6/6`; it will accept altered control trees. The base state confirms no implementation exists to test yet (`receipts/before.txt:2-4`). I therefore establish contract-level reachability, not an observed implementation result.

## Evidence and commands

- `read skill://godspeed` — read skill instructions.
- `cat /home/vgpnk/.omp/agent/RULES.md` — read required installation policy; no install/update performed.
- `read /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-54/claims-frozen.md` — C1 clauses and kill/do-nothing rule, lines 19–44.
- `read /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-54/registration.md` — frozen pin hashes and C1 control list.
- `read /home/vgpnk/Projects/shokunin/mado-shokunin/corpus/knowledge/hyprland-synthetic-dispatch-r52-errata-r53.md` — P19–P22 quote/anchor table; unchanged excerpts are the precondition of the coordinated substitution recipe.
- `read /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-54/receipts/before.txt` — baseline has zero r54 counters.
- `git -C /home/vgpnk/Projects/shokunin/mado-shokunin rev-parse HEAD` → `e25149fec8152a3aabd2b18a0ee8663b23cf65aa`; resolving the frozen base produced the same revision; `git ... status --short` showed untracked round-54 wave artifacts and the C2 entry, no C1 counter. Read-only queries only.
- `glob .../quality/counters` — listed existing counters; no `c1-r54-errata-truth.py`.

## Report trailer

Lane-relative report: `.ufo/waves/round-54/w1/R54Seat18.md`. No fixture, scratch artifact, git/jj mutation, producer execution, host/config/service/compositor mutation, package query, or tool installation/update. No tracked lane edits beyond this assigned report.
