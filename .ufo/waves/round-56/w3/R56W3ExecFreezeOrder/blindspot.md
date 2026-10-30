# D4 freeze-order blind-spot receipt

Scratch clone: `/fast/scratch/hyaku/mado-r56/R56W3ExecFreezeOrder/lane`; test revision `d703850070fcf5078a1ad844e8e094de1e70bdc0`. The clone's top-level was asserted before fixture commits. The fixture moved the w1 registry `createdAt` to `2026-10-29T00:22:47.615Z`, then committed a modification to `.ufo/waves/round-56/claims-frozen-v2.md` at committer date `2026-10-30T12:00:00Z` (after launch). Thus a v2 contract file changed after launch.

Commands (from fleet root; lane untouched):
```
D=/fast/scratch/hyaku/mado-r56/R56W3ExecFreezeOrder/lane
# clone --shared /home/vgpnk/Projects/shokunin/mado-shokunin; switch -c d4-blindspot
python3 -I -c '... set w1 registry createdAt/updatedAt to 2026-10-29T00:22:47.615Z ...'
git -C "$D" add .ufo/waves/round-56/w1/swarm-registry.json
git -C "$D" -c user.name=ctl -c user.email=ctl@ctl commit -q -m 'fixture: backdate registry launch' --date='2026-10-29T00:22:47Z'
printf '\n<!-- scratch D4 post-launch mutation -->\n' >> "$D/.ufo/waves/round-56/claims-frozen-v2.md"
git -C "$D" add .ufo/waves/round-56/claims-frozen-v2.md
GIT_COMMITTER_DATE='2026-10-30T12:00:00Z' git -C "$D" -c user.name=ctl -c user.email=ctl@ctl commit -q -m 'fixture: change v2 contract after launch' --date='2026-10-30T12:00:00Z'
python3 -I /home/vgpnk/Projects/shokunin/mado-shokunin/quality/check-freeze-order.py --repo "$D" --rev d703850070fcf5078a1ad844e8e094de1e70bdc0 --round 56 --wave w1
```

Decisive output:
```
MADO_FREEZE_ORDER: round=56 wave=w1 freeze=3423ae285676 freeze_time=2026-10-28T21:19:17-03:00 launch=2026-10-29T00:22:47.615Z verdict=OK reason=ok
```

The checker returns OK despite the v2 contract edit after launch. Reason observed in `quality/check-freeze-order.py`: `REQUIRED` contains only `claims-frozen.md` and `registration.md`; optional `frozen-tables.json`; it never binds v2 contract files. (This version's registry path is used only to parse `createdAt`; it is not a contract manifest.)

Routed round-57 proposal: Extend freeze-order verification to bind all versioned frozen-contract files and their digests/commit order, including `claims-frozen-v2.md`, `registration-v2.md`, `frozen-tables-v2.json`, and `c3-name-only.tsv`; reject any post-launch mutation.
