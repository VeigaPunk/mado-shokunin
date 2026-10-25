# DistillerFindings — simplifier seat, mado round 36 wave 1

Lane: /home/vgpnk/Projects/shokunin/mado-shokunin
Role: simplifier

Deduplicate the wave-1 findings. Read every report under LANE/.ufo/waves/round-36/w1/reports/ that exists when you run, extract each distinct finding (normalize by the file and clause it concerns), drop duplicates and merge restatements, and write one table: finding id, where it points, which claim it touches (C1/C2/frontier/harm-watch), and its status (open/refuted/needs L1). Report the count of raw rows, distinct rows and merged rows.
