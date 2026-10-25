# RevDedup — duplicate check for the eight new rows (S203–S210)

Scope: the eight staged registry rows in `.ufo/waves/round-35/controls/golden/corpus/SOURCES.md`
(canonical shape per the seat plan) checked against `corpus/SOURCES.md` (registry S001–S202,
ends at line 205; `## Paths` starts :206). Method: census's own patterns — `gawk` row-pass
(E03/E04/W04) plus `usedby_findings` (E11) via `scripts/sources-census.sh validate --file`
against a scratch mirror at `/tmp/revdedup-lane` (symlinked lane root, merged registry,
`--today 2026-10-24`). Path-column duplicates were additionally checked by direct grep, since
the census's `url_of()` only extracts `https?://` locators and returns "" for path sources.

## (a) Duplicate ids — none

- S203–S210 are distinct and none exist in the live registry (last row S202, `corpus/SOURCES.md:204`).
- Merged-registry `validate` prints zero `E03` lines.
- Note for the id-space seats, not a finding here: the merge package's own ids (S309, S310,
  S321, S329, S330, S331, S334, S336 per the seat plan) also do not collide with the lane set.

## (b) Within-scope duplicate URLs or document paths — none

- All eight rows carry path locators, no `https?://` source; `url_of()` yields "" for each, so
  E04/W04 can never fire on them. The W04s in validate output (S030, S042, S045, S097, S119,
  S120, S121) are pre-existing registry pairs, untouched by this append.
- Direct grep of the live registry for every new locator finds zero matches:
  `/home/vgpnk/.local/share/omarchy/bin/omarchy-first-run`,
  `/home/vgpnk/.local/share/omarchy/bin/omarchy-menu`,
  `/home/vgpnk/.local/share/omarchy/default/waybar/indicators/idle.sh`,
  `/home/vgpnk/.config/waybar/config.jsonc`, and `.ufo/waves/round-35/fetch/S203–S210.receipt.txt`
  appear nowhere in `corpus/SOURCES.md` (checked full file, including `## Paths` and search log).
- Within the eight: all eight source documents are distinct files. Scopes S206–S210 all concern
  the idle-lock offer, but each cites a different document (config.jsonc, idle.sh, omarchy-menu,
  the S209 backups receipt, the S210 toggle-dir receipt) — no within-scope document duplicate.
- Closest existing rows, no overlap: S020 (`~/.local/share/omarchy/default/hypr/*.conf`, scope =
  opacity effects), S073/S085–S089 (waybar/walker *upstream* files, different paths), S090
  (`/var/log/pacman.log`).

## (c) used-by paths that do not exist — 8 findings, all merge-order-dependent

Against the live lane tree today, every new row's `used-by` is dangling:

```
file  E11  S203 missing used-by corpus/knowledge/idle-lock-never-asked-r12.md
file  E11  S204 missing used-by corpus/knowledge/idle-lock-never-asked-r12.md
file  E11  S205 missing used-by corpus/knowledge/idle-lock-chain-armed-r14.md
file  E11  S206 missing used-by corpus/knowledge/idle-lock-offered-in-the-bar-r15.md
file  E11  S207 missing used-by corpus/knowledge/idle-lock-offered-in-the-bar-r15.md
file  E11  S208 missing used-by corpus/knowledge/idle-lock-offered-in-the-bar-r15.md
file  E11  S209 missing used-by corpus/knowledge/idle-lock-offered-in-the-bar-r15.md
file  E11  S210 missing used-by corpus/knowledge/idle-lock-offered-in-the-bar-r15.md
```

Three distinct missing targets; all eight rows are `mined`, so `usedby_findings` checks each.
The targets are the merge-package entries at
`/home/vgpnk/Projects/shokuknow/merge/mado/knowledge/corpus/knowledge/` (all three verified
present there, 23:26) that this round adopts — not yet copied into `corpus/knowledge/`.
In the post-merge mirror (three files copied in) the same validate run prints `ok` and exits 0
with zero E03/E04/E11/W01 findings for the new rows. **Ordering constraint for the append:
the three entries must land in `corpus/knowledge/` before or atomically with the registry
append; appending rows first produces 8 E11 errors against the live tree.**

## (d) Tier-C rows used as sole support — none

- All eight new rows are tier A (`own-work | A`); no tier-C row is introduced, so W01 cannot
  fire and no entry gains a tier-C supporter from this append.
- Conversely, the three target entries are supported only by tier-A rows — every one of the
  eight used-by citations is tier A.

## Out-of-scope observations (other seats)

- Golden fixture's S210 anchor sha256 is `ef282e38…` while the c1-digest control fixture carries
  `0000…` — deliberate control mutation, not a registry defect (RevReceipts' scope).
- Registry id space has a pre-existing gap S190–S200 (only S196, S201, S202 present); a gap is
  not a duplicate (CritIdSpace/RevengerId's scope).

Verdict: the eight rows are clean on (a), (b), (d). The only findings are the eight E11
dangling `used-by` references, all resolved by landing the three merge-package entries — a
landing-order requirement, not a row defect.
