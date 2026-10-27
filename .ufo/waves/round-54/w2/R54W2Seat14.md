# R54W2Seat14 — C1 in-process control self-assertion attack

Axes: falsifiability (controls independently demonstrated), provenance (receipts tied to actual execution), and operability (scored invocation performs the claimed tests).

## Counterexample
`controls=6/6` can be self-asserted without executing any of the six mutations. An implementation can unconditionally print the entire frozen success line and exit 0 on the real tree and every mutated tree. Thus the scored invocation's displayed count is not itself evidence that any control was constructed or rejected. This refutes the control-count observation if it is treated as a standalone result; it does not establish whether the eventual canonical judge executes hidden mutations itself.

Evidence from the prior item-14 report: `.ufo/waves/round-54/w1/R54Seat14.md:12-13,95-96` explicitly says no C1/C2 counter existed at base and no per-claim counter was run. The contemporaneous independent counterexample is `.ufo/waves/round-54/w1/R54Seat17.md:14-25`: it characterizes the gap as procedural, identifies only frozen output, committed per-control receipts and a self-reported selftest as observable surfaces, and states the do-nothing counter has identical good-tree output. Its recorded probe at lines 35-37 shows the unconditional success line and exit 0 on the base. Lines 42-46 propose an external grader-owned battery bound to counter hash and mutated tree IDs.

## Frozen contract / pin spans
`claims-frozen.md:19-30` freezes the command and line including `controls=6/6`, requiring clause (d) controls rejected. `claims-frozen.md:37-44` defines the kill rule and says the always-print counter fails because controls accept it. Registration `registration.md:36-47` defines controls as mutated trees and gives the six mutations; `registration.md:49-53` specifies command/selftest/quote judgment. The quoted anchored spans in registration `:27-34` are P19 1554–1558, P20 1576, P21 619–622 within 591–627, P22 573–574 after 571. These exact spans don't constrain a process that never reads inputs. Item-14's w1 report, `.ufo/waves/round-54/w1/R54Seat14.md:48-53`, independently flags that the quote judge is underdetermined, but this w2 attack is specifically on the control execution/provenance claim.

## Reproduction status and scope
No pinned C1 command was available to rerun: at the specified base the production counter is absent (`w1/R54Seat14.md:12`; `claims-frozen.md:32-33` says no `c1-r54-*` counter existed). I did not invent a result or construct/run a new counter or mutated fixture. The counterexample above is exact reasoning supported by the w1 report's observed do-nothing output, not a w2 execution. Accordingly the counterexample's cited output is **w1 evidence**, not reported as rerun here. No installs, host operations, or lane/source edits.

## Smallest safe correction
Have the canonical judge construct each of the six frozen mutations in isolated fixtures and invoke the scored counter against each; require nonzero/MISSED for every one. Bind each receipt to both the tested counter blob hash and mutated tree/revision identity. Then `controls=6/6` is judge-derived rather than an unaudited counter-authored number. Keep the frozen predicate and registration unchanged; this is a scoring/evidence correction, not a predicate edit.

## Exact commands / outputs
- `read claims-frozen.md` and `read registration.md` (tool reads; no process exit code applies): frozen spans and control definitions cited above.
- `read w1/R54Seat14.md` (tool read; no process exit code applies): prior report and absence-of-counter scope.
- `grep` over w1 reports (tool search; no process exit code applies): retrieved R54Seat17 counterexample and quoted line ranges above.
- `read quality/counters/c1-r54-errata-truth.py` → `Path ... not found` (tool response; no process exit code applies).
- Pinned command `python3 -I quality/counters/c1-r54-errata-truth.py --repo . --rev <rev>`: **NOT RUN / absent**; source does not exist in the inspected lane tree.
- Scratch creation: `mkdir -p /fast/scratch/hyaku/mado-r54/R54W2Seat14 && D=... && test -d "$D"` → `exit=0`.
- Scratch cleanup: `rm -rf /fast/scratch/hyaku/mado-r54/R54W2Seat14` → `exit=0` (cleanup performed before yield; no scratch remains).
