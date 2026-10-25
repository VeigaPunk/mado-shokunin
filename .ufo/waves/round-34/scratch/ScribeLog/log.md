## Round 34 — a new coverage counter frozen against the crib that killed its predecessor (2026-10-24, attempt 2 — attempt 1 froze the claims and landed the data, then died on a provider-route failure)

Motivation: the round-33 coverage counter PRED-C1-r33-v1 is dead as an
instrument. A symlink crib — fetch paths that are symlinks to the real
blobs, under a regular-file registry and entry — prints `TARGET_MET` on
it (committed receipt `.ufo/waves/round-34/controls/r33-counter-on-its-crib.txt`:
`closed_entries=2 closed_rows=4 open_cites=0 verdict=TARGET_MET`, exit 0,
while the honest lane tree prints `TARGET_MISSED`); the kill was first
shown on `.ufo/waves/round-33/scratch/CriticC1Junk/` in round 33. The
frozen predicate was not amended; a new counter was frozen instead. Axes
remain tied at 1.0 (round-32 table, re-stated in the round-33 SCORECARD
section) and the stagnation nudge does not waive because a capability
entered in round 32, so the wave carries the two tied-lowest axes: C1
coverage (the crib-rejecting claim) and C2 calibration, which does not
read C1's files.

Work: (1) C1 — PRED-C1-r34-v1 frozen at commit
`3420e827bd7b21b1374b23245526554ffd20d096` together with its pre-data
control receipts (`.ufo/waves/round-34/c1/count.py`, `c1/frozen.json`,
`registration.md`, `controls/`). The claim is one new entry
`corpus/knowledge/waybar-module-text-route-r25.md` — the Waybar
event-socket client, citing S201 and S202 with sha-pinned fetched bytes
(`.ufo/waves/round-34/fetch/S201.bin` `799bf02f6d18ae04…`,
`S202.bin` `5df496eb3cfe5cae…`). Every committed control ran before the
data: the do-nothing lane tree, entries-only, rows-only, symlink-crib,
symlink-entry, symlink-parent, symlink-sources, used-by-prefix and
hardlink (nlink=2) trees all print `closed_entries=0 closed_rows=0
open_cites=2 verdict=TARGET_MISSED` exit 1; only the regular-file golden
tree prints `TARGET_MET` — a control, not the claim measurement. The
data landed at commit `fa7ba11346116672352b5d41494141c5c4d738d0` (the
entry, SOURCES rows S201/S202, the README index row, the SCORECARD
publication line); the frozen counter on the lane tree at that tip
prints `closed_entries=1 closed_rows=2 open_cites=0 verdict=TARGET_MET`
exit 0. (2) C2 — PRED-C2-r34-v1 frozen in the same commit: the last
SCORECARD `r34-s189-line:` marker must publish `line=169` against the
sha-pinned `.ufo/waves/round-32/fetch/S189.bin` opened O_NOFOLLOW — the
round-32 lesson's line-128 claim was false (line 169 strip-equals
`const size_t MAX_QUEUED_EVENTS = 64;`; line 128 does not). Pre-data
receipts: absent marker and a `line=128` junk card both TARGET_MISSED;
the committed card at 169 TARGET_MET. The data commit publishes
`r34-s189-line: line=169` and the counter at tip prints
`published=169 measured=169 mismatch=0 verdict=TARGET_MET` exit 0.
(3) The axis table was re-derived at the data tree (navigation 47/47,
calibration resolved-active 41/41, operability selftest 12/12 — stated
as not an axis-score claim) so the existing gate does not go red when
the new note is indexed.

Repairs made to the coverage counter (r33-v1 → r34-v1): every path
component of the entry and fetch paths is lstat-walked and a symlink at
any level is refused; the leaf must be a regular file with `st_nlink=1`
(the hardlink crib is refused); the scored root itself must be a
non-symlink directory and paths must be relative with no `.`/`..`
components; bytes are opened `O_NOFOLLOW` and capped at 8 MB; the fetch
bytes are sha256-pinned in `c1/frozen.json`; the entry must carry a
`gate-quote: <id>` line of 1–25 words that is a contiguous substring of
the fetched bytes; and the registry row must list the entry path as a
whole used-by token, not a prefix. The r33 counter and its frozen.json
were not edited — the frozen kill rule stands as evidence, not
certification.

Honest notes: the claim measurement is the counter on the real lane
tree at the data commit; the golden tree's TARGET_MET is a control
receipt only. A rejected cite stays open rather than closing falsely —
every kill fixture prints `open_cites=2`, never a partial close. The
round-33 rows in SCORECARD.md were not rewritten; PRED-C1-r33-v1 remains
in the registry as a dead instrument. A post-landing seat re-ran the
counter against a fresh symlink crib built on the committed entry
(`.ufo/waves/round-34/w1/reports/ExecSymlinkCrib.md`) and it still
prints TARGET_MISSED. The verdict is self-measured at write time; a
non-author verifier spot-check is still owed under the protocol. Wave-1
seats ran after the data commit; their reports live under
`.ufo/waves/round-34/w1/reports/`.
