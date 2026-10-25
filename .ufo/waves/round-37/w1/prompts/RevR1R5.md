# RevR1R5 — reviewer seat, mado round 37 wave 1

Lane: /home/vgpnk/Projects/shokunin/mado-shokunin
Role: reviewer

Verify the five routed defects of /home/vgpnk/Projects/shokunin/mado-shokunin/corpus/lessons/round-36-verifier-spotcheck.md §5 at committed bytes and the live tree: R1 (`git -C /home/vgpnk/Projects/shokunin/mado-shokunin status --porcelain`; size and mtime of the DistillerFindings file; is it lane-authored — read its header), R2 (`grep -n 64979ef /home/vgpnk/Projects/shokunin/.ufo/reports/round-36/mado.md`; the receipts' named revision), R3 (`grep -c` criteria 57–61 in `git show a5aaa09:corpus/QUALITY.md`), R4 (`git -C /home/vgpnk/Projects/shokunin/mado-shokunin cat-file -s` of the S211 receipt at a3094c9 and a5aaa09 — find its path), R5 (how `inherited_dirty` is computed in /home/vgpnk/Projects/shokunin/mado-shokunin/quality/check-evidence-pointers.py, cite lines). For each: still live / already fixed / wrong, with the command output.
