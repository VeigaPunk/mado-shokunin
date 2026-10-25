# RevRecordIntact — reviewer seat, mado round 36 wave 1

Lane: /home/vgpnk/Projects/shokunin/mado-shokunin
Role: reviewer

Verify the `record_intact` guard is what stops a record rewrite from looking like a repair: read the gate's `SUPERSEDED_POINTERS` and the round-35 LOG entry that cites them; then in /tmp, delete those two pointer mentions from a copy of LOG.md and show the gate's `dangling_r35_closed` stays 0 (quote both runs).
