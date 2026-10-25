# LabratGateOracle — revenger seat, mado round 36 wave 1

Lane: /home/vgpnk/Projects/shokunin/mado-shokunin
Role: revenger

Bounded, read-only probe of one falsifiable hypothesis: *the gate's `correct == controls` target has a path to exit 0 without both instrument repairs*. Enumerate the gate's own decision path in LANE/quality/check-counter-discrimination.py (quote the lines), and try three probes in /tmp: a profile whose instrument path is a stub that delegates to the r35 counters; a manifest copy with the four c1 fabrication controls removed; a `--receipts` path that does not exist. Report each outcome with the exit code. One hypothesis, one receipt.
