# ExecClausePins — executor seat, mado round 36 wave 1

Lane: /home/vgpnk/Projects/shokunin/mado-shokunin
Role: executor

Build the clause-set fixtures in /tmp from LANE/.ufo/waves/round-36/c2/clauses.json: (a) one live clause deleted; (b) a live clause marked `not-load-bearing` with a reason (second declaration); (c) the toctou clause's declaration removed; (d) the retired id re-added to `live`; (e) the live list duplicated. Write a /tmp implementation of the round-36 C2 rule (from the frozen predicate text in LANE/.ufo/waves/round-36/c2/frozen.json) and report `uncovered`/`retired`/`tip_ok` per fixture. This is the pin's failing case.
