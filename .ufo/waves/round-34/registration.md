# Round 34 registration — frozen before data

Author: Kimi fresh L1. Date: 2026-10-24. This file does not amend
`.ufo/waves/round-33/c1/count.py` or its frozen.json.

Axes are tied at 1.0 (round-32 table, re-stated in the round-33 SCORECARD
section). The stagnation nudge does not waive: a capability entered in round
32. The crib-rejecting claim is C1 on coverage, the axis round 33 missed.
C2 is calibration, the other tied-lowest axis, and does not read C1's files.

## C1 coverage

Surface: Waybar event-socket client, frontier → core. One entry,
`corpus/knowledge/waybar-module-text-route-r25.md`, citing S201 and S202.
The command that shows the surface unmoved is the same counter on a tree
that lacks that entry.

Predicate, identical in `c1/count.py`, `c1/frozen.json`, and this file:

PRED-C1-r34-v1: TARGET_MET iff closed_entries=1 AND closed_rows=2 AND open_cites=0, where a frozen cite is closed only when the entry path and the fetch path are both regular files (not symlinks, nlink=1) whose every path component stays inside the scored root, the fetch bytes read with O_NOFOLLOW have sha256 equal to the digest in c1/frozen.json, the entry contains a 1-25 word gate-quote line for that id that is a contiguous substring of those bytes, and the registry row for that id lists the entry path as a whole used-by token.

Counting command, from the lane repo:

```sh
python3 -I .ufo/waves/round-34/c1/count.py --root . --frozen .ufo/waves/round-34/c1/frozen.json
```

Kill: a symlink crib (fetch paths are symlinks to the real blobs) and a
do-nothing control (this command on the lane tree before the entry and rows
exist) both print TARGET_MISSED. A regular-file golden tree may meet; that
tree is not the claim measurement.

## C2 calibration

Surface: SCORECARD publication versus the pinned S189 fetch. The lesson's
line-128 claim is false; line 169 of `.ufo/waves/round-32/fetch/S189.bin`
strip-equals `const size_t MAX_QUEUED_EVENTS = 64;`.

Predicate, identical in `c2/count.py`, `c2/frozen.json`, and this file:

PRED-C2-r34-v1: TARGET_MET iff mismatch=0, where mismatch is 0 only when the last SCORECARD line matching r34-s189-line: publishes line=169 and line 169 of the regular-file fetch .ufo/waves/round-32/fetch/S189.bin opened with O_NOFOLLOW (nlink=1, sha256 eea605dfe5ce09e1f92a67ec478bf61a19894c6e0ee3302c0393521a2ee9540d) strip-equals const size_t MAX_QUEUED_EVENTS = 64; and line 128 of that file does not.

Counting command, from the lane repo:

```sh
python3 -I .ufo/waves/round-34/c2/count.py --repo . --scorecard SCORECARD.md --frozen .ufo/waves/round-34/c2/frozen.json
```

Kill: this command before the publication line exists prints TARGET_MISSED.
A card whose last marker tail is `line=128` prints TARGET_MISSED.
