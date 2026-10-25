# RevCollisions — reviewer seat, mado round 37 wave 1

Lane: /home/vgpnk/Projects/shokunin/mado-shokunin
Role: reviewer

Re-run the assimilation id-collision check, the guard proof and the quarantine slice independently with the exact commands of the round prompt §10 (they are reproduced in /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-37/assimilation/renumber-map.md's header and in /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/prompts? — use /home/vgpnk/Projects/shokunin/.ufo/prompts/mado-round-37.md section 10), writing only to /dev/shm/mado37-RevCollisions/. Compare reg-ids/staged-ids/collisions/quarantine-slice byte-for-byte with /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-37/assimilation/. Then verify the renumber map by document: for each mapped row, the URL and sha256 of the bytes (/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-37/fetch/*) match the lane row (S189, S201) or the package row (S214→S212). Report agreement or each mismatch.
