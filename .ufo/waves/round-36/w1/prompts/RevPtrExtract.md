# RevPtrExtract — executor seat, mado round 36 wave 1

Lane: /home/vgpnk/Projects/shokunin/mado-shokunin
Role: executor

Write in /tmp four copies of LANE's LOG.md and SCORECARD.md with one planted defect each, and run LANE/quality/check-evidence-pointers.py against them via `--repo` on a /tmp git-init'ed copy (or `--rev` on a copy you commit there; do not touch LANE's git): (a) a pointer to a nonexistent file in a round-36 section; (b) a correction pair whose `new` does not exist; (c) the round-35 pointer lines deleted; (d) a pointer with a glob that matches nothing. Report each verdict and whether the gate caught the plant.
