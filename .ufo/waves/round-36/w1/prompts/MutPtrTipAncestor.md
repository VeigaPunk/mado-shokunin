# MutPtrTipAncestor — mutation-tester seat, mado round 36 wave 1

Lane: /home/vgpnk/Projects/shokunin/mado-shokunin
Role: mutation-tester

Mutate the C2 gate in /tmp to accept any `quality/receipts/axis-*.txt` whose name is 40 hex, without the ancestor test and without matching `rev=`. Build a /tmp copy of the lane with a fabricated receipt for a non-ancestor hash and show the mutant accepts it while the honest gate rejects it.
