# RevFleetMisroot — reviewer seat, mado round 36 wave 1

Lane: /home/vgpnk/Projects/shokunin/mado-shokunin
Role: reviewer

Sweep the fleet root for stray lane files: `git -C /home/vgpnk/Projects/shokunin status --porcelain` and `find /home/vgpnk/Projects/shokunin/.ufo/waves/round-36 -maxdepth 3 -type f` (if it exists) plus any file under the fleet root whose content names `mado` and `round-36`. Report every stray with its path and a byte-level note (size, first line). Read-only: the L1 repatriates.
