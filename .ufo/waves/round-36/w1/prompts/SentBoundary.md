# SentBoundary — sentinel seat, mado round 36 wave 1

Lane: /home/vgpnk/Projects/shokunin/mado-shokunin
Role: sentinel

Audit the lane's write boundary for this round so far. Run `git -C /home/vgpnk/Projects/shokunin status --porcelain` (no pathspec) and classify every line: lane-authored under mado-shokunin, another lane's, driver state, or a stray. Then `git -C /home/vgpnk/Projects/shokunin/mado-shokunin status --porcelain` and classify. Report any file outside the lane that names mado/round-36, and any path under `/home/vgpnk/Projects/shokunin/mado-shokunin` that a seat wrote outside its report/scratch. Read-only.
