## Source census — round 66 start/end instructions

Tool: `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh`
(exit 0 clean/warnings; 1 finding/overdue; 2 usage/missing registry — the header states this).

Run from the fleet root, against the real lane tree (never `--file` on a scratch copy:
round-65 F3 showed `validate --file <scratch>/SOURCES.md` produces false `E11 missing
used-by` because used-by paths resolve against the copied file's own tree).

Start (already taken by L1, 2026-11-03):

    cd /home/vgpnk/Projects/shokunin
    scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin mado \
      > mado-shokunin/.ufo/waves/round-66/census-start-r66.txt; echo "exit=$?" >> ...

Observed at start: `exit=0`, 36 `W04` duplicate-URL + 1 `W01` tier-C line (37 total), terminal
`mado ok <lane>/corpus/SOURCES.md`.

Re-check performed by this seat (same command, receipt kept in seat scratch, not in the
lane): `exit=0`, same 36 `W04` + 1 `W01` lines, `diff` against `census-start-r66.txt` differs only in
the recorded command line and `exit=0` trailer. So the start state and the pre-integration
state are identical, and the draft row S435 cannot have introduced a line (registry untouched).

End (after L1 integrates S435 and the lesson):

    cd /home/vgpnk/Projects/shokunin
    scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin mado \
      > mado-shokunin/.ufo/waves/round-66/census-end-r66.txt; echo "exit=$?" >> ...

Acceptance at end:
- `exit=0` (a non-zero rc means a finding or an unreadable registry — route, do not smooth).
- Warning set must equal the start set; the new row must not add a `W04 duplicate url S435`
  or an `E11` line. Any *new* warning naming S435 is a regression in this seat's draft.
- Shape delta, measured on the A/B fixture: rows 371 → **372**, `tier.A` 357 → **358**,
  `status.mined` 350 → **351**, `tier.B`/`tier.C`/`queued`/`rejected` unchanged.
- Receipts live at the round root, **outside** `.ufo/waves/round-66/receipts/`, so the C2
  landing dirty-guard and citecheck do not read this round's own measurement output as lane
  content (round-65 addendum: measurement outputs live outside the scanned receipts tree).

Pre-integration check already run by this seat (re-runnable: `evidence.sh` §6): two mirror
lane dirs — one with the committed registry, one with S435 inserted after S434 plus a
placeholder `corpus/lessons/round-66.md`; every other corpus entry and top-level lane entry is
a symlink into the live lane, and both are validated with the lane dir passed explicitly
(`validate --root <mirror> <mirror>/lane-*`). Result: both rc=0, 36 `W04` + 1 `W01` each,
normalized output differing only in the terminal `ok` path, no finding naming S435. This is a
delta check only — the mirror must never be used with `--file`, which r65 showed yields false
`E11` on any copy.

