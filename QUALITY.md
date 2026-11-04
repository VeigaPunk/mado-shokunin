
## Criteria from the round-73 control-set and census work (round 73)

**118. A frozen declaration's counting command is replayed verbatim before the receipt is filed,
and every required argument is named in the declaration itself.** (a) A declaration that prints a
counting command must print the exact argv the receipt will run, flags included; (b) the round
replays that line once before the instrument's receipt lands, and a usage error is a defect of the
declaration, not of the counter.
Shown able to fail: round 73's §C1 line omits `--controls`; replaying it exits 2 with
`--repo, --rev and --controls are required` and no contract line (the wave's `R73RevC1` F1), while
the corrected invocation prints `killed=4 base_killed=2 verdict=TARGET_MET` rc 0 — the defect and
its repair are erratum E1 in `.ufo/waves/round-73/claims-declaration-r73.md` and M73-1 in
`corpus/lessons/round-73.md`.
Limits: a replay proves the argv parses and the arguments are present; it does not prove the
counter's verdict and it is not a substitute for the do-nothing control.

**119. A regression fixture's expected label is derived from the rule's declared bound, not from
the behaviour the author wishes the rule had; a label that assumes a stronger rule must fail the
harness selftest.**
Shown able to fail: the first `r73-global-rebind-after-use` case in
`quality/counters/c2-r73-shapes.py` labelled a store-then-later-call program `(True, False)` while
the line-order classifier answers `(True, True)`; the selftest printed
`FAIL: review regression r73-global-rebind-after-use is (True, False)` until the case was replaced
by `r73-global-rebind-replaced-between`, which the declared bound does refuse (M73-2 in
`corpus/lessons/round-73.md`).
Limits: the embedded table is the lane's own, not an independent control set; the selftest checks
that the label and the classifier agree, not that the declared bound is the right approximation.


> Round 74: criteria 118–119 in this fragment were appended to the canonical
> `corpus/QUALITY.md` (the bar `corpus/README.md` points at) and this fragment is retained
> only as history; read `corpus/QUALITY.md`.
