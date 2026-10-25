# MutC2HardcodedTip — mutation-tester seat, mado round 36 wave 1

Lane: /home/vgpnk/Projects/shokunin/mado-shokunin
Role: mutation-tester

Write a /tmp variant of C2 with the round-35 tip logic (hardcoded `dff3941…` substring test plus spec-derived blob ids). Run it against `/tmp/mado-r36-mutants-r36/c2-tip-stale`, `c2-tip-one-copy`, `c2-blob-corrupt`, `c2-blob-row-deleted`. Report which survive under the old logic and which the round-36 rule kills.
