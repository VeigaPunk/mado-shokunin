# RevC1Code — reviewer seat, mado round 37 wave 1

Lane: /home/vgpnk/Projects/shokunin/mado-shokunin
Role: reviewer

Review /home/vgpnk/Projects/shokunin/mado-shokunin/quality/counters/c1-r37-event-ground.py against the registration's C1 section and Amendment 1 (/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-37/registration.md). For each clause a–g: does the code implement exactly the sentence (quote code lines)? Look for: fence looseness (`## Registry` exact match? `## Gate` exact?), quote matching on bytes vs decoded text, ids parsed from all `source:` lines in the first 15 lines only, used-by split, README first-cell test, the base-ground precondition, GIT_* scrub, exit-code coherence with the verdict token. Run it at base and at the freeze tip (`--rev 893a8aadc80ab19bc163e366d674a8ac32feacd0`) and quote outputs. List every divergence as a finding with severity.
