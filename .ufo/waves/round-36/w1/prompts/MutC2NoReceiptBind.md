# MutC2NoReceiptBind — mutation-tester seat, mado round 36 wave 1

Lane: /home/vgpnk/Projects/shokunin/mado-shokunin
Role: mutation-tester

Write a /tmp variant of the round-36 C2 design whose receipt test is the round-35 token grep (`verdict=TARGET_MISSED` anywhere in the file). Run it against the generated fixtures `/tmp/mado-r36-mutants-r36/c2-receipt-token` and `/tmp/mado-r36-mutants-r36/c2-receipt-unbound` (generate them first if absent). Report each verdict and prove the binding is what kills them.
