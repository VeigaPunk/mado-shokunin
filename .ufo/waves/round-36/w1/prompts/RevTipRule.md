# RevTipRule — reviewer seat, mado round 36 wave 1

Lane: /home/vgpnk/Projects/shokunin/mado-shokunin
Role: reviewer

Audit the computed tip rule and the tip-line guard. Verify `git -C /home/vgpnk/Projects/shokunin/mado-shokunin log --format=%H%x00%s` newest-first gives `6d754bd…` for the pattern `round-34`; verify the round-36 blob ledger LANE/.ufo/waves/round-36/ledger/RevFrozenBlobs-r36.md has ≥3 tip lines and that every tip-labelled 40-hex token equals the computed tip. Then construct two /tmp documents: one that adds `supersedes` to every tip line (the exemption), and one that keeps one stale token. State whether the `min_tip_lines` guard plus the row table defeats the first, quoting the exact lines.
