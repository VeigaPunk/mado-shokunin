# RevIndexGate — reviewer seat, mado round 36 wave 1

Lane: /home/vgpnk/Projects/shokunin/mado-shokunin
Role: reviewer

Run `cd /home/vgpnk/Projects/shokunin/mado-shokunin && python3 -I quality/check-index.py --repo .` and `python3 -I quality/check-index-rows.py --repo .` (whichever exist; report if one is absent). Record the summary lines, the exit codes, and the count of knowledge notes at `master` (`git ls-tree --name-only master:corpus/knowledge | wc -l`).
