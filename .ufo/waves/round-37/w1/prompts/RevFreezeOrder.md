# RevFreezeOrder — reviewer seat, mado round 37 wave 1

Lane: /home/vgpnk/Projects/shokunin/mado-shokunin
Role: reviewer

Verify the freeze chronology from committed bytes: `git -C /home/vgpnk/Projects/shokunin/mado-shokunin log --format='%H %ad %s' --date=iso -5 master`; show that at 8f0a9e3f78120d00e5e9f32c909618d549f976b4 and at 893a8aadc80ab19bc163e366d674a8ac32feacd0 none of the target files exists (`git ls-tree` for the two entries, tools/mado-eventq.py, corpus/lessons/round-37.md); that the v2 amendment is append-only over v1 (`git diff 8f0a9e3 893a8aa -- .ufo/waves/round-37/registration.md` — only additions?); that the v1 receipts were kept; and QUALITY criterion 61 (registration commands run verbatim at the freeze, output committed) — run each command the registration names, verbatim, and compare with the committed receipts.
