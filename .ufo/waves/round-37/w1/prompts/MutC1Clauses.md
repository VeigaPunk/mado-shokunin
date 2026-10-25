# MutC1Clauses — mutation-tester seat, mado round 37 wave 1

Lane: /home/vgpnk/Projects/shokunin/mado-shokunin
Role: mutation-tester

Mutation-test /home/vgpnk/Projects/shokunin/mado-shokunin/quality/counters/c1-r37-event-ground.py: in /dev/shm, make one mutant per clause (a, b, c, d, e, f, g — each mutant forces that clause to 1) plus a mutant that drops the `## Registry` fence and one that drops the `## Gate` fence. Score each mutant with a scratch copy of /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-37/controls.py pointed at the mutant (change only the C1 path). Report a kill table: mutant → controls that kill it; any surviving mutant is a finding (a clause no control exercises).
