# MutC1AcceptAll — mutation-tester seat, mado round 36 wave 1

Lane: /home/vgpnk/Projects/shokunin/mado-shokunin
Role: mutation-tester

Write, in /tmp, a mutant of the C1 instrument that prints `PRED-C1-r36-v1 closed_entries=3 closed_rows=8 open_cites=0 verdict=TARGET_MET` and exits 0 on every root. Score it against the frozen manifest by running the gate with a /tmp copy of `quality/check-counter-discrimination.py` whose r36 c1 script path points at your mutant (copy the gate; do not edit LANE). Report the score and which controls kill it. Restore nothing in LANE — you wrote only /tmp.
