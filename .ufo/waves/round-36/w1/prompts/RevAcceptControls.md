# RevAcceptControls — reviewer seat, mado round 36 wave 1

Lane: /home/vgpnk/Projects/shokunin/mado-shokunin
Role: reviewer

Verify the three accept controls are real and non-trivial. For `c1-live`, `c1-golden-r36` and `c2-live`: show each is byte-identical or byte-analogous to committed lane bytes (diff the crib tree against LANE where it should match; name every intended difference for `c1-golden-r36`, whose registry heading was added in round 36). Then verify each reject control differs from its nearest accept control in exactly one input: quote the differing bytes.
