# MutC2Clauses — mutation-tester seat, mado round 37 wave 1

Lane: /home/vgpnk/Projects/shokunin/mado-shokunin
Role: mutation-tester

Mutation-test /home/vgpnk/Projects/shokunin/mado-shokunin/quality/counters/c2-r37-eventq.py: in /dev/shm, mutants that (1) drop all must_not checks, (2) accept any rc, (3) drop the readonly regex, (4) drop the `connect(` test, (5) drop the replay comparison, (6) count CLIENT lines without the subscribers equality. Score each against the round's C2 controls (scratch copy of /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-37/controls.py pointed at the mutant). Expect several to survive because no passing tool exists yet — report which clauses are therefore unexercised before data, so the L1 knows which controls the post-data residual must add.
