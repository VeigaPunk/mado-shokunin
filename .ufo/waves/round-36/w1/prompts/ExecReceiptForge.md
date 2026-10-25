# ExecReceiptForge — executor seat, mado round 36 wave 1

Lane: /home/vgpnk/Projects/shokunin/mado-shokunin
Role: executor

Try to cover an uncovered clause honestly. In /tmp, copy LANE/.ufo/waves/round-36/c2/clauses.json and the receipts directory, then write four forged receipts for one clause: (a) the exact text the gate emits but with the wrong clause id; (b) right clause, wrong `control=` id; (c) right tokens embedded in prose with no measured verdict; (d) the real receipt of a *different* clause. Point a /tmp copy of a C2 implementation at each (the round-36 design is described in the registration; the round-35 one is LANE/.ufo/waves/round-35/c2/count.py). Report which forgeries pass under each and what the round-36 binding costs.
