# MutC2NoClausePin — mutation-tester seat, mado round 36 wave 1

Lane: /home/vgpnk/Projects/shokunin/mado-shokunin
Role: mutation-tester

Write a /tmp variant of the round-36 C2 design with the frozen `expected_live_clause_ids` cross-check removed (a deleted clause is skipped, as in round 35). Generate fixtures with `python3 -I .ufo/waves/round-36/c2/gen-mutants.py --profile r36 --repo /home/vgpnk/Projects/shokunin/mado-shokunin --out /tmp/w36-m2 --` then run your variant against `/tmp/w36-m2/c2-clause-deleted`. Report whether `uncovered` stays 0 (fail-open reproduced) and what the pin costs.
