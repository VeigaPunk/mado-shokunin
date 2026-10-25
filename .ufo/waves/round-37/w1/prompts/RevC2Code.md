# RevC2Code — reviewer seat, mado round 37 wave 1

Lane: /home/vgpnk/Projects/shokunin/mado-shokunin
Role: reviewer

Review /home/vgpnk/Projects/shokunin/mado-shokunin/quality/counters/c2-r37-eventq.py against the registration's C2 section and Amendment 1. Check each of the ten CASES: does the fixture represent real `ss -xpa` output (compare its row shapes with the live `ss -xpa | grep -F .socket2.sock` rows and their peers — column count, `*` placeholders, users field), are the `must`/`must_not` patterns satisfiable only by the intended behaviour, and is any case redundant? Check the readonly clause (regex, `connect(` text test) and the live replay clause (multiset of triples, counts). Run it at base and quote. Findings with severity.
