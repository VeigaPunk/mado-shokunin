# ExecDigestCribs — executor seat, mado round 36 wave 1

Lane: /home/vgpnk/Projects/shokunin/mado-shokunin
Role: executor

Build four crib trees in /tmp from LANE/.ufo/waves/round-35/controls-content/c1-fabricated-payload (copy it) and run the round-35 counter and a /tmp copy of the round-36 design against each: (a) anchor cell carries the REAL sha256 but the receipt bytes are altered; (b) receipt bytes are the real ones but the anchor cell carries a wrong sha; (c) receipt length preserved, first byte flipped; (d) receipt replaced by a file of the right name at the right path with identical content (must still be accepted). Report the four verdicts under both counters. This is the byte-binding proof.
