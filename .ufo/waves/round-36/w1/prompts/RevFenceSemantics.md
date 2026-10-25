# RevFenceSemantics — reviewer seat, mado round 36 wave 1

Lane: /home/vgpnk/Projects/shokunin/mado-shokunin
Role: reviewer

Check the round-36 `## Registry` fence against the fleet census's own E12 rule. Read /home/vgpnk/Projects/shokunin/scripts/sources-census.sh (E12 and its selftest fixtures, quote the lines) and LANE/.ufo/waves/round-36/c1/frozen.json plus the fence implementation path the repaired counter must take (the round-35 counter is at LANE/.ufo/waves/round-35/c1/count.py; the fence is described in the registration). Test the edge cases the census supports: 0–3 leading spaces on the heading, a row above `## Registry`, a second `## Registry`, `###` subheadings inside it, a registry with no rows, and a file with no `## Registry` at all. Report agreement or divergence per case, with the census's own fixture as the oracle.
