# MutPtrExistingOnly — mutation-tester seat, mado round 36 wave 1

Lane: /home/vgpnk/Projects/shokunin/mado-shokunin
Role: mutation-tester

Mutate the C2 gate in /tmp so `dangling` counts only pointers that exist (a vacuous counter). Score it against the round-35 record (where two pointers are absent) and show it reports 0 dangling while naming one absent pointer by hand.
