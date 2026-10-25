# MutC1NoDigest — mutation-tester seat, mado round 36 wave 1

Lane: /home/vgpnk/Projects/shokunin/mado-shokunin
Role: mutation-tester

Take LANE/.ufo/waves/round-35/c1/count.py (which lacks the digest binding) and write a /tmp instrument that is the round-36 design minus exactly the `digest == receipt["sha256"]` conjunct. Score it against the manifest through a /tmp copy of the gate. Report which controls catch the missing conjunct and which still pass — the pass set is the fabrication class the binding is worth.
